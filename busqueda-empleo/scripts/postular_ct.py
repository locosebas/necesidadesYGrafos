"""Postula por lotes en Computrabajo a vacantes ya aprobadas en el tablero.

Uso: python postular_ct.py CARPETA_EXPORT [--max N] [--enviar]
  CARPETA_EXPORT: carpeta donde ArtifactData guardó las vacantes aprobadas (out_dir).
  Sin --enviar llega hasta las preguntas de filtro y no envía (prueba en seco).
Salida: una línea por vacante y resultados_ct.json para actualizar el tablero.
Estados: ENVIADA | YA | DESCARTADA/MARCADA (compuertas) | PREGUNTAS (hay preguntas sin regla: se le preguntan a Sebastián) | BLOQUEADA.
"""
import json, os, re, sys
from playwright.sync_api import sync_playwright
from comun import compuerta, destrabar, responder, linea, vacantes, BASE

args = sys.argv[1:]
carpeta = args[0]
maximo = int(args[args.index("--max") + 1]) if "--max" in args else 10
enviar = "--enviar" in args

LEER_KQ = """() => {
  const grupos = {};
  document.querySelectorAll('[name$=".OpenQuestion"], [name$=".ClosedQuestion"]').forEach(e => {
    const i = e.name.match(/\\[(\\d+)\\]/)[1];
    (grupos[i] = grupos[i] || []).push(e);
  });
  return Object.entries(grupos).map(([i, els]) => {
    let n = els[0];
    while (n.parentElement && [...n.parentElement.querySelectorAll('[name$=".OpenQuestion"], [name$=".ClosedQuestion"]')].every(x => x.name.includes('[' + i + ']'))) n = n.parentElement;
    const radios = els.filter(e => e.type === 'radio');
    const ops = radios.map(r => (r.labels[0] ? r.labels[0].innerText : r.value).trim());
    let q = n.innerText.replace(/\\s+/g, ' ').trim();
    ops.forEach(o => { q = q.replace(o, ''); });
    q = q.replace(/\\(máximo \\d+ caracteres\\)/, '').trim();
    let s = n;
    while (q.length < 5 && s) { const pr = s.previousElementSibling; if (pr) { q = pr.innerText.replace(/\\s+/g, ' ').trim(); } s = pr ? null : s.parentElement; }
    return {i: +i, q, tipo: radios.length ? 'radio' : 'texto', ops};
  });
}"""

resultados = []
destrabar()
with sync_playwright() as p:
    ctx = p.chromium.connect_over_cdp("http://localhost:9222").contexts[0]
    for v in vacantes(carpeta, "ct-")[:maximo]:
        pg = ctx.new_page()
        r = {"id": v["id"], "estado": "BLOQUEADA", "detalle": ""}
        try:
            pg.goto(v["url"], wait_until="domcontentloaded", timeout=40000)
            pg.wait_for_timeout(2500)
            cuerpo = pg.inner_text("body")
            filtro, motivo = compuerta(v, cuerpo)
            if re.search(r"Ya (te )?(aplicaste|postulaste)", cuerpo):
                r["estado"] = "YA"
            elif filtro != "PASA":
                r.update(estado=filtro, detalle=motivo)
            else:
                btn = pg.locator("a:visible, button:visible").filter(has_text=re.compile(r"^\s*(Postularme|Aplicar)\s*$", re.I))
                if not btn.count():
                    r["detalle"] = "sin botón Aplicar (oferta cerrada o externa)"
                else:
                    btn.first.click()
                    pg.wait_for_timeout(4500)
                    if "postapply" in pg.url:
                        r["estado"] = "ENVIADA"
                    elif "candidate/kq" in pg.url:
                        preguntas = pg.evaluate(LEER_KQ)
                        faltan = []
                        for q in preguntas:
                            q["r"] = responder(q["q"], q["ops"] if q["tipo"] == "radio" else None)
                            if q["r"] is None:
                                faltan.append(q["q"][:200])
                        if faltan:
                            r.update(estado="PREGUNTAS", detalle=f"{len(faltan)} sin regla", preguntas=faltan)
                        else:
                            for q in preguntas:
                                if q["tipo"] == "texto":
                                    pg.locator(f'[name="KillerQuestions[{q["i"]}].OpenQuestion"]').fill(q["r"][:500])
                                else:
                                    for rd in pg.locator(f'[name="KillerQuestions[{q["i"]}].ClosedQuestion"]').all():
                                        if rd.evaluate("e => (e.labels[0] ? e.labels[0].innerText : e.value).trim()") == q["r"]:
                                            rd.evaluate("e => (e.labels[0] || e).click()")
                            r["respuestas"] = [[q["q"][:80], q["r"][:80]] for q in preguntas]
                            if enviar:
                                pg.click("#btnKiller")
                                pg.wait_for_timeout(4500)
                                r["estado"] = "ENVIADA" if "postapply" in pg.url else "BLOQUEADA"
                                if r["estado"] == "BLOQUEADA":
                                    r["detalle"] = "no confirmó tras enviar"
                            else:
                                r.update(estado="LISTA", detalle="prueba en seco: respuestas llenas, sin enviar")
                    else:
                        r["detalle"] = "redirige fuera del flujo normal (" + pg.url[:60] + ")"
        except Exception as e:
            r["detalle"] = "error: " + type(e).__name__
        finally:
            pg.close()
        resultados.append(r)
        linea(r["id"], r["estado"], r["detalle"])

json.dump(resultados, open(os.path.join(BASE, "resultados_ct.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
