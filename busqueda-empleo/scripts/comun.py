"""Utilidades comunes para postular por lotes con salida mínima.

Datos privados (contacto, salario, reglas de respuesta) viven SOLO en la carpeta local
C:/Users/diazt/Documents/Postulaciones/lote/ (datos_privados.json y reglas.json), nunca en el repo.
"""
import asyncio, json, os, re, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
CDP = "http://localhost:9222"


def cargar(nombre):
    return json.load(open(os.path.join(BASE, nombre), encoding="utf-8"))


DATOS = cargar("datos_privados.json")
REGLAS = cargar("reglas.json")


def destrabar():
    """Despierta (activa, sin cerrar) las pestañas que no responden: si una pestaña está
    congelada, connect_over_cdp se queda esperando para siempre."""
    import websockets
    tabs = [t for t in json.loads(urllib.request.urlopen(CDP + "/json/list", timeout=8).read()) if t["type"] == "page"]

    async def responde(t):
        try:
            async with websockets.connect(t["webSocketDebuggerUrl"], max_size=None, open_timeout=4) as ws:
                await ws.send('{"id":1,"method":"Runtime.evaluate","params":{"expression":"1"}}')
                await asyncio.wait_for(ws.recv(), 3)
                return True
        except Exception:
            return False

    async def colgadas():
        return [t for t in tabs if not await responde(t)]

    for t in asyncio.run(colgadas()):
        urllib.request.urlopen(CDP + "/json/activate/" + t["id"], timeout=8)


def responder(pregunta, opciones=None):
    """Devuelve la respuesta según reglas.json, o None si ninguna regla aplica (pregunta nueva:
    se le pregunta a Sebastián, nunca se improvisa)."""
    p = pregunta.lower()
    for r in REGLAS:
        if not re.search(r["si"], p):
            continue
        if r.get("bloquea"):
            return None
        if opciones:
            for quiero in r.get("opcion", []):
                for o in opciones:
                    if o.strip().lower() == quiero.lower():
                        return o
            continue
        if r.get("texto"):
            return r["texto"]
    return None


def linea(id_, estado, detalle=""):
    """Una línea por vacante: es lo único que debe ver el chat."""
    print(f"{estado:9} {id_} {detalle}"[:160])


def vacantes(carpeta, prefijo):
    """Lee el export del tablero (ArtifactData con out_dir) y devuelve las vacantes del prefijo."""
    d = os.path.join(carpeta, "vacantes") if os.path.isdir(os.path.join(carpeta, "vacantes")) else carpeta
    out = []
    for f in sorted(os.listdir(d)):
        if f.startswith(prefijo) and f.endswith(".json"):
            v = json.load(open(os.path.join(d, f), encoding="utf-8"))
            v["id"] = f[:-5]
            out.append(v)
    return sorted(out, key=lambda v: -(v.get("encaje") or 0))
