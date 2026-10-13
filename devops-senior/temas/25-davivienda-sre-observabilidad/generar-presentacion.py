"""Genera presentacion.html a partir de presentacion-libreto.md.

Uso: python3 generar-presentacion.py
Por diapositiva toma el título, el contenido, el primer diagrama Mermaid y el guion (notas del orador).
Teclas: ← → cambian de diapositiva · N guion · D (o clic en el diagrama) diagrama a pantalla completa · F pantalla completa.
Para PDF: imprimir desde el navegador (una diapositiva por página).
"""
import html
import re
from pathlib import Path

AQUI = Path(__file__).parent
md = (AQUI / "presentacion-libreto.md").read_text(encoding="utf-8")


def inline(t: str) -> str:
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"<i>\1</i>", t)


def bullets(bloque: str) -> str:
    items, actual = [], ""
    for linea in bloque.splitlines():
        if linea.startswith("- "):
            if actual:
                items.append(actual)
            actual = linea[2:]
        elif linea.strip():
            actual += " " + linea.strip()
    if actual:
        items.append(actual)
    return "".join(f"<li>{inline(i)}</li>" for i in items)


slides = []
for parte in re.split(r"(?m)^## Diapositiva ", md)[1:]:
    cab = parte.splitlines()[0]
    num, resto = cab.split(" — ", 1)
    eje = re.sub(r"\s*\(.*?min\)\s*$", "", resto)
    tiempo = re.search(r"\(([\d,]+ min)\)", cab).group(1)
    titulo = re.search(r"\*\*Título:\*\* (.+)", parte).group(1)
    contenido = re.search(r"\*\*Contenido:\*\*\n(.*?)\n\n", parte, re.S).group(1)
    diagrama = re.search(r"```mermaid\n(.*?)```", parte, re.S)
    guion = re.search(r"\*\*Guion:\*\*\n(.*?)\n\n\*\*", parte, re.S).group(1)
    slides.append(f"""
<section class="slide">
  <header><span class="eje">{num} · {inline(eje)}</span><span class="t">{tiempo}</span></header>
  <h1>{inline(titulo)}</h1>
  <div class="cuerpo">
    <ul>{bullets(contenido)}</ul>
    {f'<div class="diag"><pre class="mermaid">{html.escape(diagrama.group(1))}</pre></div>' if diagrama else ''}
  </div>
  <aside class="notas">{inline(guion.strip().strip('"')).replace(chr(10), '<br>')}</aside>
</section>""")

pagina = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Banco Plus — Confiabilidad del pago QR</title>
<style>
:root {{ --azul:#1168bd; --oscuro:#0b2a4a; --gris:#5b6470; --fondo:#ffffff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#e9edf2; font-family:system-ui,Segoe UI,Roboto,sans-serif; color:#1b1b1b; }}
.slide {{ display:none; width:100vw; height:100vh; padding:3vh 4vw 2vh; background:var(--fondo); flex-direction:column; }}
.slide.activa {{ display:flex; }}
header {{ display:flex; justify-content:space-between; color:var(--gris); font-size:1.6vh; text-transform:uppercase; letter-spacing:.05em; border-bottom:3px solid var(--azul); padding-bottom:.8vh; }}
h1 {{ color:var(--oscuro); font-size:3.6vh; margin:1.6vh 0; }}
.cuerpo {{ display:flex; gap:2vw; flex:1; min-height:0; }}
ul {{ flex:0 0 30%; margin:0; padding-left:1.2em; font-size:2vh; line-height:1.45; overflow:auto; }}
li {{ margin-bottom:1vh; }}
code {{ background:#eef2f7; padding:0 .25em; border-radius:3px; font-size:.9em; }}
.diag {{ flex:1; min-width:0; min-height:0; height:100%; display:flex; overflow:hidden; cursor:zoom-in; }}
.diag pre {{ margin:0; flex:1; display:flex; }}
.diag svg {{ width:100%; height:100%; }}
body.zoom .cuerpo ul {{ display:none; }}
body.zoom .diag {{ cursor:zoom-out; }}
.cuerpo:not(:has(.diag)) ul {{ flex:1; font-size:2.4vh; }}
.notas {{ display:none; margin-top:1vh; max-height:24vh; overflow:auto; background:#fff8e1; border-left:4px solid #c17900; padding:1vh 1vw; font-size:1.7vh; line-height:1.4; }}
body.ver-notas .notas {{ display:block; }}
nav {{ position:fixed; bottom:1.5vh; right:2vw; display:flex; gap:.6em; align-items:center; font-size:1.6vh; color:var(--gris); }}
nav button {{ border:0; background:var(--azul); color:#fff; border-radius:4px; padding:.5em .9em; cursor:pointer; font-size:1.6vh; }}
@media (max-width:800px) {{ .cuerpo {{ flex-direction:column; }} ul {{ flex:none; }} }}
@media print {{
  @page {{ size:landscape; margin:0; }}
  body {{ background:#fff; }} nav, .notas {{ display:none !important; }}
  .slide {{ display:flex !important; page-break-after:always; height:100vh; }}
}}
</style></head>
<body>
{''.join(slides)}
<nav><button id="ant" aria-label="Anterior">◀</button><span id="cont"></span><button id="sig" aria-label="Siguiente">▶</button>
<button id="nt" title="Guion (N)">Guion</button></nav>
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({{ startOnLoad:false, theme:"default", securityLevel:"loose", themeVariables:{{ fontSize:"18px" }},
  flowchart:{{ useMaxWidth:false }}, gantt:{{ useMaxWidth:false, fontSize:16 }} }});
const s=[...document.querySelectorAll(".slide")]; let i=0;
const ir=n=>{{ i=Math.max(0,Math.min(s.length-1,n)); s.forEach((x,k)=>x.classList.toggle("activa",k===i));
  document.getElementById("cont").textContent=`${{i+1}} / ${{s.length}}`; location.hash=i+1; }};
document.getElementById("ant").onclick=()=>ir(i-1);
document.getElementById("sig").onclick=()=>ir(i+1);
document.getElementById("nt").onclick=()=>document.body.classList.toggle("ver-notas");
addEventListener("keydown",e=>{{
  if(["ArrowRight","PageDown"," "].includes(e.key)) ir(i+1);
  if(["ArrowLeft","PageUp"].includes(e.key)) ir(i-1);
  if(e.key==="d"||e.key==="D") document.body.classList.toggle("zoom");
  if(e.key==="n"||e.key==="N") document.body.classList.toggle("ver-notas");
  if(e.key==="f"||e.key==="F") document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();
}});
s.forEach(x=>x.classList.add("activa"));
await mermaid.run({{ querySelector:".mermaid" }});
document.querySelectorAll(".diag svg").forEach(v=>{{ v.removeAttribute("style"); v.setAttribute("width","100%");
  v.setAttribute("height","100%"); v.setAttribute("preserveAspectRatio","xMidYMid meet"); }});
document.querySelectorAll(".diag").forEach(d=>d.onclick=()=>document.body.classList.toggle("zoom"));
ir((parseInt(location.hash.slice(1))||1)-1);
</script>
</body></html>"""

(AQUI / "presentacion.html").write_text(pagina, encoding="utf-8")
print(f"presentacion.html: {len(slides)} diapositivas")
