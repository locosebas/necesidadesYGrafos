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


# --- Compuertas: filtros duros que se revisan ANTES de postular -------------------------------
# Política: cantidad primero; la calidad (revisor, ATS, investigación) llega con la entrevista.
# Los pisos de salario son privados: viven en datos_privados.json -> "compuertas"
# {"presencial_min_cop": ..., "hibrido_min_cop": ..., "cop_por_usd": ...}.
# Resultado de compuerta(): ("PASA", "") | ("DESCARTADA", motivo) | ("MARCADA", motivo para Sebastián).

COLOMBIA = r"colombia|bogot|medell[ií]n|\bcali\b|barranquilla|bucaramanga|pereira|cartagena|manizales|cundinamarca|antioquia|sop[oó]"
REGION_OK = r"latam|latin ?am[eé]rica|am[eé]rica latina|sudam[eé]rica|south america|centroam[eé]rica|cualquier pa[ií]s|mundial|worldwide|anywhere|global"
PAISES = (r"argentin|bolivia|brasil|brazil|chile|per[uú]\b|m[eé]xico|mexico|ecuador|uruguay|paraguay|venezuela|costa rica|panam"
          r"|guatemala|espa[ñn]a|spain|portugal|estados unidos|united states|\busa?\b|canad|india|polan|polonia|alemania|germany|reino unido|\buk\b")
IDIOMA_EXIGIDO = r"(fluent|native|nativo|fluido|avanzado|required|obligatorio|indispensable)"
OTROS_IDIOMAS = r"(portugu[eé]s|portuguese|alem[aá]n|german|franc[eé]s|french|italian[oa]?|japan[eé]se?|japon[eé]s|mandar[ií]n|chinese|chino|polish|polaco|russian|ruso)"


def clasificar_modalidad(texto):
    t = (texto or "").lower()
    if re.search(r"opci[oó]n h[ií]brida", t):
        return "remoto"
    if re.search(r"h[ií]brid|d[ií]as? (en )?oficina|visitas a oficina|presencial y remoto|presencial/", t):
        return "hibrido"
    if "presencial" in t or "on-site" in t or "onsite" in t:
        return "presencial"
    if re.search(r"remot|remote|freelance|desde casa", t):
        return "remoto"
    return "desconocida"


def _numero(tok):
    tok = re.sub(r"[.,]\d{2}$", "", tok) if re.search(r"\d[.,]\d{3}[.,]\d{2}$|^\d{1,3}[.,]\d{2}$", tok) else tok
    return int(re.sub(r"[.,]", "", tok))


def salario_mensual_cop(texto, cop_por_usd):
    """Lo máximo que paga al mes, en COP. None si no se publica o no es comparable
    (por hora, precio fijo, otra moneda). La 'aspiración' es de Sebastián, no de la vacante."""
    t = re.split(r"aspiraci[oó]n", (texto or "").lower())[0]
    if re.search(r"por hora|per hour|/ ?hour|/ ?hora|/h\b|hourly|precio fijo|fixed|\b(eur|cad|inr|gbp)\b", t):
        return None
    montos = [_numero(m) for m in re.findall(r"\d[\d.,]*\d|\d", t)]
    montos = [m for m in montos if m >= 100]
    if not montos:
        return None
    m = max(montos)
    usd = bool(re.search(r"usd|us\$|dólar|dolar", t)) or m < 100_000
    if usd:
        if re.search(r"al a[ñn]o|anual|annual|per year|/year|a year", t) or m >= 50_000:
            m /= 12
        return round(m * cop_por_usd)
    if re.search(r"al a[ñn]o|anual", t):
        m /= 12
    return round(m)


def compuerta_ubicacion(ubicacion):
    t = (ubicacion or "").lower()
    if not t or re.search(COLOMBIA, t) or re.search(REGION_OK, t):
        return "PASA", ""
    if re.search(PAISES, t):
        return "DESCARTADA", f"ubicación sin Colombia: {ubicacion[:60]}"
    return "PASA", ""


def compuerta_idioma(texto):
    """Inglés: se declara C1 siempre; solo se marca si piden C2 o nativo."""
    t = (texto or "").lower()
    if re.search(rf"{OTROS_IDIOMAS}[^.\n]{{0,40}}{IDIOMA_EXIGIDO}|{IDIOMA_EXIGIDO}[^.\n]{{0,25}}{OTROS_IDIOMAS}", t):
        return "DESCARTADA", "exige otro idioma: " + re.search(OTROS_IDIOMAS, t).group(0)
    if re.search(r"(english|ingl[eé]s)[^.\n]{0,30}(\bc2\b|native|nativo)|(\bc2\b|native|nativo)[^.\n]{0,25}(english|ingl[eé]s)", t):
        return "MARCADA", "pide inglés C2 o nativo"
    return "PASA", ""


def compuerta_modalidad_salario(modalidad, salario):
    c = DATOS.get("compuertas") or {}
    if not c:
        return "PASA", "sin pisos en datos_privados.json"
    modo = clasificar_modalidad(modalidad)
    paga = salario_mensual_cop(salario, c["cop_por_usd"])
    if paga is None or modo in ("remoto", "desconocida"):
        return "PASA", ""
    if modo == "presencial" and paga <= c["presencial_min_cop"]:
        return "DESCARTADA", f"presencial y paga {paga / 1e6:.1f} M"
    if modo == "hibrido" and paga < c["hibrido_min_cop"]:
        return "DESCARTADA", f"híbrido y paga {paga / 1e6:.1f} M"
    return "PASA", ""


def compuerta(v, texto_vacante=""):
    """Aplica todas las compuertas a una vacante del tablero. texto_vacante (opcional) es el texto
    de la página, para la compuerta de idioma. Devuelve la primera que no pase."""
    for estado, motivo in (compuerta_ubicacion(v.get("ubicacion")),
                           compuerta_modalidad_salario(v.get("modalidad"), v.get("salario")),
                           compuerta_idioma(texto_vacante)):
        if estado != "PASA":
            return estado, motivo
    return "PASA", ""
