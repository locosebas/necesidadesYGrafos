#!/usr/bin/env python3
"""Genera presentacion.html a partir de libreto-diapositivas.md y diagramas-c4.md.

Uso: python3 generar_presentacion.py

- Cada diapositiva del libreto va separada por una línea '---'.
- '**Diagrama:** D2a, D2b' inserta esos diagramas (bloques mermaid de diagramas-c4.md).
- 'ico:nombre' en un diagrama se reemplaza por iconos/nombre.svg embebido (data URI),
  así el HTML funciona sin la carpeta de íconos. Mermaid se carga desde CDN (requiere internet).
"""
import base64
import html
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LIBRETO = AQUI / "libreto-diapositivas.md"
DIAGRAMAS = AQUI / "diagramas-c4.md"
ICONOS = AQUI / "iconos"
SALIDA = AQUI / "presentacion.html"


def cargar_diagramas():
    texto = DIAGRAMAS.read_text(encoding="utf-8")
    patron = re.compile(r"^## (D\w+) · (.+?)\n(.*?)```mermaid\n(.*?)```", re.S | re.M)
    out = {}
    for m in patron.finditer(texto):
        ident, titulo, _, codigo = m.groups()
        out[ident] = {"titulo": titulo.strip(), "codigo": con_iconos(codigo)}
    return out


USADOS = {}


def con_iconos(codigo):
    """Cambia 'ico:nombre' por un <img> corto; el logo se carga después de dibujar.

    Así el texto del diagrama queda pequeño y no supera el límite de tamaño de Mermaid
    (los logos en base64 dentro del diagrama hacían fallar D1 en algunos navegadores).
    """
    def img(m):
        nombre = m.group(1)
        if nombre not in USADOS:
            ruta = ICONOS / f"{nombre}.svg"
            if not ruta.exists():
                raise SystemExit(f"Falta el ícono {ruta}")
            USADOS[nombre] = "data:image/svg+xml;base64," + base64.b64encode(ruta.read_bytes()).decode()
        return f"<img class='ico' data-i='{nombre}' width='28' height='28'/>"

    return re.sub(r"ico:([\w-]+)", img, codigo)


def en_linea(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def cargar_diapositivas(diagramas):
    texto = LIBRETO.read_text(encoding="utf-8")
    bloques = re.split(r"^---\s*$", texto, flags=re.M)[1:]  # el primero es la introducción del archivo
    diapos = []
    for b in bloques:
        titulo, seccion, ids, vinetas, guion = "", "", [], [], []
        for linea in b.strip().splitlines():
            if linea.startswith("## "):
                titulo = linea[3:].strip()
            elif linea.startswith("**Sección:**"):
                seccion = linea.split(":**", 1)[1].strip()
            elif linea.startswith("**Diagrama:**"):
                ids = [x.strip() for x in linea.split(":**", 1)[1].split(",") if x.strip()]
            elif linea.startswith("- "):
                vinetas.append(linea[2:])
            elif linea.startswith(">"):
                guion.append(linea.lstrip("> ").strip())
        for i in ids:
            if i not in diagramas:
                raise SystemExit(f"El libreto pide el diagrama {i}, que no existe en {DIAGRAMAS.name}")
        diapos.append({"titulo": titulo, "seccion": seccion, "ids": ids,
                       "vinetas": vinetas, "guion": " ".join(guion)})
    return diapos


def html_diapositiva(n, d, diagramas):
    figs = "".join(
        f'<figure><pre class="mermaid">{html.escape(diagramas[i]["codigo"])}</pre>'
        f'<figcaption>{i} · {en_linea(diagramas[i]["titulo"])}</figcaption><div class="desliza">desliza el diagrama →</div></figure>'
        for i in d["ids"])
    lis = "".join(f"<li>{en_linea(v)}</li>" for v in d["vinetas"])
    clase = "slide con-diagrama" if d["ids"] else "slide solo-texto"
    if d["ids"] and all("flowchart LR" in diagramas[i]["codigo"] for i in d["ids"]):
        clase += " apilado"
    portada = " portada" if n == 0 else ""
    cuerpo = (f'<div class="diagramas">{figs}</div>' if figs else "") + f'<ul class="puntos">{lis}</ul>'
    return (f'<section class="{clase}{portada}" data-n="{n}">'
            f'<header><span class="kicker">{en_linea(d["seccion"])}</span><h1>{en_linea(d["titulo"])}</h1></header>'
            f'<div class="cuerpo">{cuerpo}</div>'
            f'<aside class="notas"><b>Guion:</b> {en_linea(d["guion"])}</aside></section>')


CSS = """
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#0d1b2a;font-family:Segoe UI,Arial,sans-serif;color:#1b2733}
#deck{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
.slide{display:none;width:min(96vw,calc(92vh*16/9));height:min(92vh,calc(96vw*9/16));background:#fff;border-radius:14px;
 padding:2.2% 3%;flex-direction:column;box-shadow:0 10px 40px #0008;position:relative;overflow:hidden}
.slide.activa{display:flex}
header{border-bottom:3px solid #1168bd;padding-bottom:.5em;margin-bottom:1em}
.kicker{color:#1168bd;font-weight:700;text-transform:uppercase;font-size:clamp(10px,1.1vw,15px);letter-spacing:.08em}
h1{margin:.15em 0 0;font-size:clamp(18px,2.3vw,34px);color:#08427b}
.cuerpo{flex:1;display:flex;gap:2.5%;min-height:0}
.con-diagrama .diagramas{flex:1.9;display:flex;flex-direction:column;gap:.6em;min-width:0;min-height:0;justify-content:center}
.con-diagrama .puntos{flex:1}
figure{margin:0;flex:1;display:flex;flex-direction:column;min-height:0;justify-content:center}
figure pre.mermaid{margin:0;flex:1;display:flex;align-items:center;justify-content:center;min-height:0;background:none;visibility:hidden}
figure pre.mermaid[data-processed]{visibility:visible}
figure svg{max-width:100%!important;max-height:100%;height:auto}
figcaption{text-align:center;color:#6b7785;font-size:clamp(9px,.9vw,13px)}
.puntos{margin:0;padding-left:1.1em;font-size:clamp(11px,1.35vw,21px);line-height:1.45;overflow:auto}
.puntos li{margin:.3em 0}.puntos strong{color:#08427b}
.solo-texto .puntos{font-size:clamp(13px,1.8vw,28px);max-width:85%;margin:auto 0}
.portada{background:linear-gradient(135deg,#08427b,#1168bd);color:#fff}
.portada header{border-color:#fff4}.portada h1,.portada .kicker,.portada .puntos strong{color:#fff}
.portada h1{font-size:clamp(26px,4vw,58px)}
code{background:#eef3f8;padding:0 .25em;border-radius:4px;font-size:.92em}
.portada code{background:#fff3}
.notas{display:none;position:absolute;left:0;right:0;bottom:0;background:#fffbe6;border-top:3px solid #f0b400;
 padding:1em 3%;font-size:clamp(11px,1.2vw,18px);line-height:1.45;max-height:45%;overflow:auto;color:#3a2f00}
body.ver-notas .notas{display:block}
.nodeLabel img.ico,.label img.ico{width:30px!important;height:30px!important;min-width:30px;display:inline-block!important;vertical-align:middle;margin:0 2px 4px;background:#fff;border-radius:6px;padding:3px}
.apilado .cuerpo{flex-direction:column;gap:1%}
.apilado .diagramas{flex:1}
.apilado .puntos{flex:none;columns:2;column-gap:3em;font-size:clamp(10px,1.15vw,18px);line-height:1.35;max-height:34%}
.apilado .puntos li{break-inside:avoid;margin:.15em 0}
#barra{position:fixed;left:0;bottom:0;height:4px;background:#f0b400;transition:width .2s}
#contador{position:fixed;right:14px;bottom:10px;color:#9fb3c8;font-size:13px}
#ayuda{position:fixed;left:14px;bottom:10px;color:#9fb3c8;font-size:13px}
#nav{position:fixed;right:12px;bottom:28px;display:none;gap:8px;z-index:5}
#nav button{font:600 15px Segoe UI,Arial,sans-serif;border:0;border-radius:22px;padding:10px 16px;background:#1168bd;color:#fff;box-shadow:0 3px 10px #0006}
#nav button#bn{background:#f0b400;color:#3a2f00}
@media (max-width:820px),(pointer:coarse){
 #nav{display:flex}#ayuda{display:none}
}
@media (max-width:820px) and (orientation:portrait){
 #deck{position:static;display:block;padding:10px 8px 90px}
 .slide{width:100%;height:auto;min-height:calc(100vh - 110px);border-radius:10px;padding:16px 14px}
 h1{font-size:22px}.kicker{font-size:11px}
 .cuerpo,.apilado .cuerpo{flex-direction:column;gap:12px}
 .diagramas{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e3eaf2;border-radius:8px;padding:6px}
 figure pre.mermaid{display:block}
 .slide,.cuerpo,.diagramas,figure{min-width:0;max-width:100%}
 .diagramas{width:100%;flex:none!important}
 figure{flex:none}
 figure pre.mermaid{flex:none;width:max-content}
 figure svg{width:680px!important;max-width:none!important;height:auto!important;max-height:none!important}
 figcaption{font-size:11px}
 .puntos,.apilado .puntos,.solo-texto .puntos{columns:1;font-size:16px;max-height:none;max-width:none;overflow:visible}
 .portada .puntos{font-size:18px}.portada h1{font-size:30px}
 .notas{position:static;max-height:none;font-size:15px;margin:12px -14px -16px;border-radius:0 0 10px 10px}
 #contador{bottom:auto;top:6px;right:10px}
 .desliza{display:block!important}
}
.desliza{display:none;font-size:11px;color:#6b7785;text-align:right;margin-top:2px}
@media print{body{background:#fff}.slide{display:flex!important;page-break-after:always;box-shadow:none}#barra,#contador,#ayuda{display:none}}
"""

JS = """
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:'base',maxTextSize:5000000,
  flowchart:{htmlLabels:true,useMaxWidth:true,curve:'basis'},
  themeVariables:{fontFamily:'Segoe UI, Arial',fontSize:'16px',lineColor:'#5b6b7c',
    clusterBkg:'#f5f9fd',clusterBorder:'#7a9cc0',edgeLabelBackground:'#ffffff'}});
const S=[...document.querySelectorAll('.slide')];let i=0;
async function ver(n){
  i=Math.max(0,Math.min(S.length-1,n));
  S.forEach((s,k)=>s.classList.toggle('activa',k===i));
  document.getElementById('contador').textContent=(i+1)+' / '+S.length;
  document.getElementById('barra').style.width=((i+1)/S.length*100)+'%';
  history.replaceState(null,'','#'+(i+1));
  const pend=[...S[i].querySelectorAll('pre.mermaid:not([data-processed])')];
  if(pend.length){
    await mermaid.run({nodes:pend});
    // mermaid marca subgrafos punteados como límites C4
    S[i].querySelectorAll('.cluster rect').forEach(r=>r.setAttribute('stroke-dasharray','6 4'));
    S[i].querySelectorAll('img[data-i]').forEach(im=>{const u=ICOS[im.dataset.i];if(u)im.src=u});
  }
}
document.addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();ver(i+1)}
  else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();ver(i-1)}
  else if(e.key==='Home')ver(0);else if(e.key==='End')ver(S.length-1);
  else if(e.key.toLowerCase()==='n')document.body.classList.toggle('ver-notas');
});
document.getElementById('deck').addEventListener('click',e=>{
  if(e.target.closest('.notas')||matchMedia('(pointer:coarse)').matches)return;ver(e.clientX>innerWidth/2?i+1:i-1)});

const movil=()=>matchMedia('(max-width:820px) and (orientation:portrait)').matches;
document.getElementById('ba').onclick=e=>{e.stopPropagation();ver(i-1);scrollTo(0,0)};
document.getElementById('bs').onclick=e=>{e.stopPropagation();ver(i+1);scrollTo(0,0)};
document.getElementById('bn').onclick=e=>{e.stopPropagation();document.body.classList.toggle('ver-notas')};
let x0=null,y0=null;
document.addEventListener('touchstart',e=>{if(e.target.closest('.diagramas')){x0=null;return}x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
document.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;
  if(Math.abs(dx)>60&&Math.abs(dx)>2*Math.abs(dy)){ver(dx<0?i+1:i-1);scrollTo(0,0)}x0=null},{passive:true});
ver((parseInt(location.hash.slice(1))||1)-1);
"""


def main():
    diagramas = cargar_diagramas()
    diapos = cargar_diapositivas(diagramas)
    secciones = "\n".join(html_diapositiva(n, d, diagramas) for n, d in enumerate(diapos))
    doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CI/CD seguro · HITSS Claro</title><style>{CSS}</style></head>
<body><div id="deck">
{secciones}
</div><div id="barra"></div><div id="contador"></div><div id="nav"><button id="ba">←</button><button id="bn">Guion</button><button id="bs">→</button></div><div id="ayuda">← → navegar · N guion · clic izq/der</div>
<script>const ICOS={json.dumps(USADOS)};</script><script type="module">{JS}</script></body></html>
"""
    SALIDA.write_text(doc, encoding="utf-8")
    usados = sorted({i for d in diapos for i in d["ids"]})
    sin_usar = sorted(set(diagramas) - set(usados))
    print(json.dumps({"diapositivas": len(diapos), "diagramas": len(diagramas),
                      "sin_usar": sin_usar, "salida": str(SALIDA), "kb": SALIDA.stat().st_size // 1024}))


if __name__ == "__main__":
    main()
