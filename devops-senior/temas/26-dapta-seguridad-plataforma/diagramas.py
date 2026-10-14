"""Diagramas SVG de la presentación (uno por diapositiva). Los usa generar-presentacion.py.

Cada diagrama se dibuja en un lienzo de 1000 x 560 con cajas y flechas; el texto va en líneas separadas por
"\\n" y una línea que empieza con "*" sale en negrita.
"""
from html import escape

COL = {  # relleno, borde, texto
    "b": ("#1168bd", "#0b4884", "#fff"), "d": ("#08427b", "#052e56", "#fff"),
    "g": ("#8a8a8a", "#6b6b6b", "#fff"), "w": ("#f4f6f9", "#9aa5b1", "#1b1b1b"),
    "v": ("#2e7d32", "#1b5e20", "#fff"), "y": ("#f9a825", "#c17900", "#1b1b1b"),
    "r": ("#c62828", "#8e0000", "#fff"), "c": ("#fff8e1", "#c17900", "#1b1b1b"),
    "l": ("#dbe8f6", "#9cc0e6", "#0b2a4a"),
}


class Lienzo:
    def __init__(self, n):
        self.n, self.p = n, []

    def box(self, x, y, w, h, texto, c="b", fs=17, dash=False, borde=2):
        f, s, t = COL[c]
        da = ' stroke-dasharray="7 5"' if dash else ""
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{f}" stroke="{s}" stroke-width="{borde}"{da}/>')
        lineas = texto.split("\n")
        y0 = y + h / 2 - (len(lineas) - 1) * fs * 0.62
        for i, l in enumerate(lineas):
            negrita = l.startswith("*")
            self.texto(x + w / 2, y0 + i * fs * 1.24, l.lstrip("*"), t, fs, negrita)

    def texto(self, x, y, t, color="#1b1b1b", fs=16, negrita=False, ancla="middle", italica=False):
        fw = ' font-weight="700"' if negrita else ""
        fi = ' font-style="italic"' if italica else ""
        self.p.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{fs}" text-anchor="{ancla}" '
                      f'dominant-baseline="middle"{fw}{fi}>{escape(t)}</text>')

    def flecha(self, x1, y1, x2, y2, et=None, ex=None, ey=None, color="#33414f", dash=False, ancho=2.5, fs=15):
        da = ' stroke-dasharray="7 5"' if dash else ""
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{ancho}"{da} '
                      f'marker-end="url(#m{self.n}{color[1:]})"/>')
        self.colores = getattr(self, "colores", set()) | {color}
        if et:
            for i, l in enumerate(et.split("\n")):
                self.texto(ex if ex is not None else (x1 + x2) / 2, (ey if ey is not None else (y1 + y2) / 2 - 12) + i * fs * 1.2,
                           l, color, fs, italica=True)

    def svg(self):
        marcas = "".join(
            f'<marker id="m{self.n}{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for c in getattr(self, "colores", set()))
        return (f'<svg viewBox="0 0 1000 560" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,Roboto,sans-serif">'
                f'<defs>{marcas}</defs>{"".join(self.p)}</svg>')


def d1():
    L = Lienzo(1)
    dolores = [("*Certificaciones\nlos compradores\npiden evidencia", "b"), ("*Estabilidad\ndependencias externas\nen tiempo real", "b"),
               ("*DORA\nsin línea base, no se\nsabe si mejora", "b"), ("*IA de voz\nningún control\nla cubre hoy", "d")]
    for i, (t, c) in enumerate(dolores):
        L.box(20 + i * 245, 30, 220, 110, t, c, 17)
    for x1, x2 in [(130, 330), (375, 450), (620, 550), (865, 670)]:
        L.flecha(x1, 140, x2, 215)
    L.box(250, 220, 500, 100, "*Una sola causa:\nlo seguro y lo estable dependen\nde personas, no de la plataforma", "c", 18)
    L.box(30, 390, 400, 120, "*La ventana\nmigración a Kubernetes + Temporal\nronda semilla · plan Enterprise", "w", 17)
    L.box(530, 390, 440, 120, "*Carretera pavimentada (golden path)\nseguro por defecto\n+ evidencia automática para el auditor", "v", 17)
    L.flecha(430, 450, 525, 450)
    L.flecha(700, 320, 740, 385, "se arregla en", 800, 350, color="#2e7d32")
    return L.svg()


def d2():
    L = Lienzo(2)
    L.box(345, 185, 310, 180, "*Plataforma Dapta\nagentes de voz y texto\nFlow Studio · Dapta MCP\nsobre AWS, migrando a\nKubernetes + Temporal", "b", 17)
    for y, t in [(40, "Clientes pymes\n[persona]"), (235, "Compradores Enterprise\nexigen evidencia [persona]"),
                 (430, "14 desarrolladores\n[persona]")]:
        L.box(15, y, 235, 80, t, "d", 16)
    for y, t in [(20, "Proveedores de voz\nTwilio · LiveKit\nDeepgram"), (145, "Proveedores de LLM\nOpenAI · Anthropic\nGemini · Groq"),
                 (280, "Temporal\n[subprocesador]"), (410, "Vanta + auditor\n[cumplimiento]")]:
        L.box(745, y, 240, 95, t, "g", 16)
    L.flecha(250, 80, 343, 200, "usan los agentes", 215, 175)
    L.flecha(250, 275, 341, 275, "① piden\nevidencia", 296, 222, color="#c62828", fs=14)
    L.flecha(250, 470, 380, 368, "③ despliegan sin\nlínea base", 280, 395, color="#c62828", fs=14)
    L.flecha(655, 205, 741, 75, "② tiempo real", 690, 120, color="#c62828", fs=14)
    L.flecha(655, 255, 741, 200, "④ datos", 690, 215, color="#c62828", fs=14)
    L.flecha(655, 310, 741, 325)
    L.flecha(620, 365, 741, 450, "① evidencia\na mano", 640, 430, color="#c62828", dash=True, fs=14)
    L.texto(500, 540, "Una sola causa: lo seguro y lo estable dependen de personas, no de la plataforma", "#8e0000", 17, True)
    return L.svg()


def d3():
    L = Lienzo(3)
    L.texto(250, 25, "La escalera de certificaciones", "#0b2a4a", 18, True)
    L.box(20, 400, 300, 95, "*✓ SOC 2 Type II\nventana de 3 meses\nemitido en sep. 2026", "v", 17)
    L.box(80, 235, 340, 105, "*SOC 2 Type II de 12 meses\n+ criterio de Availability\n(por los SLAs de Enterprise)", "b", 17)
    L.box(150, 55, 330, 130, "*Siguiente: la escoge\n*el contrato que espera\nISO 27001 · HIPAA (BAA)\nISO 42001 (IA)", "d", 17)
    L.flecha(170, 400, 210, 345)
    L.flecha(250, 235, 290, 190)
    L.texto(760, 25, "¿Cómo se mantiene vivo?", "#0b2a4a", 18, True)
    L.box(530, 50, 450, 120, "*✗ Control de papel\ncaptura de pantalla, alguien se acuerda\nse cae en una observación de 12 meses", "c", 16)
    L.texto(755, 220, "✓ Evidencia continua", "#2e7d32", 17, True)
    for x, t in [(530, "GitHub"), (685, "AWS"), (840, "Kubernetes")]:
        L.box(x, 245, 140, 55, t, "w", 16)
    L.box(620, 350, 270, 55, "*Vanta", "b", 17)
    L.box(620, 455, 270, 55, "*Auditor (SOC 2)", "d", 17)
    for x1, x2 in [(600, 690), (755, 755), (910, 820)]:
        L.flecha(x1, 300, x2, 346, color="#2e7d32")
    L.flecha(755, 405, 755, 451, color="#2e7d32")
    L.texto(250, 535, "Regla: un control sin evidencia automática no existe", "#5b6470", 16, italica=True)
    return L.svg()


def d4():
    L = Lienzo(4)
    L.texto(500, 25, "Un solo camino a producción, igual para todos los servicios", "#0b2a4a", 19, True)
    pasos = ["*Pull request\nrulesets\nCODEOWNERS", "*Plantilla de CI\nDependabot\nsecret scanning\nTrivy",
             "*OIDC\ncredenciales\ntemporales\nsin llaves", "*Amazon ECR\nimagen\nescaneada",
             "*Argo CD\nGit manda\nsin kubectl\na mano", "*Amazon EKS\nproducción"]
    for i, t in enumerate(pasos):
        x = 10 + i * 165
        L.box(x, 55, 145, 115, t, "d" if i in (0, 4) else "b", 15)
        if i < 5:
            L.flecha(x + 145, 112, x + 163, 112)
    controles = {0: "Change management\nprocedures\nenforced", 1: "Vulnerabilities\nscanned and\nremediated",
                 2: "Production\ndeployment access\nrestricted", 4: "Production\ndeployment access\nrestricted"}
    for i, t in controles.items():
        x = 10 + i * 165
        L.flecha(x + 72, 170, x + 72, 206, dash=True, color="#5b6470")
        L.box(x, 210, 145, 80, t, "l", 13)
        L.flecha(x + 72, 290, x + 72, 366, color="#2e7d32")
    L.texto(660, 330, "↑ control del SOC 2 que evidencia cada paso", "#5b6470", 14, italica=True, ancla="start")
    L.box(10, 370, 970, 60, "*Todo deja rastro → Vanta (ya integrada con GitHub y AWS) → auditor", "v", 18)
    L.texto(500, 470, "El historial de Git es la evidencia: sin capturas de pantalla", "#0b2a4a", 18, True)
    L.texto(500, 510, "Terraform con el plan visible en el pull request · ambiente production con aprobación", "#5b6470", 15, italica=True)
    return L.svg()


def d5():
    L = Lienzo(5)
    for y, t in [(50, "*GitHub\npull requests\ny despliegues"), (150, "*Argo CD\nsincronizaciones\ny rollbacks"), (250, "*Incidentes\ninicio y fin")]:
        L.box(15, y, 200, 85, t, "g", 15)
        L.flecha(215, y + 42, 256, 190)
    L.box(260, 135, 150, 110, "*Tablero\nen Grafana\n(ya lo tienen)", "d", 16)
    for y, titulo, a, b, c in [(20, "Velocidad", "Deployment\nFrequency", "Lead Time\nfor Changes", "b"),
                               (190, "Estabilidad", "Change Failure\nRate", "Time to Restore\nService", "v")]:
        L.box(450, y, 535, 150, "", "w")
        L.texto(717, y + 22, titulo, "#0b2a4a", 17, True)
        L.box(470, y + 45, 235, 90, "*" + a.replace("\n", "\n*"), c, 17)
        L.box(730, y + 45, 235, 90, "*" + b.replace("\n", "\n*"), c, 17)
    L.flecha(410, 175, 446, 100)
    L.flecha(410, 210, 446, 260)
    L.box(15, 395, 290, 90, "*Semanas 1–2\nlínea base medida", "c", 17)
    L.box(355, 395, 290, 90, "*Cada cambio de proceso\nse compara con ella", "w", 17)
    L.box(695, 395, 290, 90, "*Palancas\nlotes pequeños · trunk-based\nfeature flags (PostHog)", "l", 16)
    L.flecha(305, 440, 351, 440)
    L.flecha(645, 440, 691, 440)
    L.texto(500, 530, "Regla: la seguridad no puede empeorar las métricas DORA", "#0b2a4a", 18, True)
    return L.svg()


def d6():
    L = Lienzo(6)
    L.box(15, 190, 160, 90, "*Argo CD\nsincroniza\ndesde Git", "b", 16)
    L.box(210, 180, 175, 110, "*Kyverno\nAudit → Enforce\nno root, límites", "y", 16)
    L.flecha(175, 235, 206, 235)
    L.flecha(385, 235, 416, 235)
    L.texto(200, 330, "Audit: reporta, no bloquea", "#5b6470", 15, italica=True)
    L.box(420, 50, 330, 380, "", "w")
    L.texto(585, 78, "Amazon EKS", "#0b2a4a", 18, True)
    L.box(445, 105, 280, 100, "*namespace: servicios\nagentes, APIs", "l", 16)
    L.box(445, 280, 280, 100, "*namespace: workers\nde Temporal", "l", 16)
    L.texto(585, 243, "NetworkPolicy entre namespaces", "#c62828", 15, True)
    L.texto(585, 412, "los mismos charts de Helm on-premise", "#5b6470", 14, italica=True)
    L.box(790, 20, 195, 90, "*AWS\nvía EKS Pod Identity\nsin llaves guardadas", "g", 15)
    L.flecha(725, 130, 786, 70)
    L.box(790, 140, 195, 95, "*AWS Secrets Manager\n→ External Secrets\ntokens OAuth de CRM", "d", 15)
    L.flecha(788, 190, 729, 175)
    L.box(790, 290, 195, 75, "*Payload Codec\ncifra antes de salir", "y", 15)
    L.flecha(725, 328, 786, 328)
    L.box(790, 410, 195, 95, "*Temporal Cloud\nsolo ve\ntexto cifrado", "d", 15)
    L.flecha(887, 365, 887, 406, "mTLS", 925, 390, fs=14)
    L.texto(330, 535, "Lo inseguro no corre, y nadie tiene que acordarse", "#0b2a4a", 18, True)
    return L.svg()


def d7():
    L = Lienzo(7)
    L.texto(500, 25, "El camino de una llamada y dónde se mide", "#0b2a4a", 19, True)
    caja = [(10, 140, "*Quien llama\nteléfono,\nWhatsApp", "g"), (180, 150, "*Twilio /\nLiveKit", "g"),
            (360, 280, "*Agente de voz\nDeepgram: voz a texto\n→ LLM → respuesta", "b"), (670, 170, "*Flow Studio\nsobre Temporal", "b"),
            (870, 120, "*CRM del\ncliente", "g")]
    for i, (x, w, t, c) in enumerate(caja):
        L.box(x, 55, w, 100, t, c, 16)
        if i < 4:
            L.flecha(x + w, 105, caja[i + 1][0] - 4, 105)
    L.box(180, 180, 150, 50, "① conecta", "v", 16)
    L.box(370, 180, 175, 55, "② responde rápido\n(percentil)", "v", 15)
    L.box(670, 180, 170, 55, "③ el workflow\ntermina bien", "v", 15)
    L.flecha(600, 155, 600, 296, "failover", 640, 250, fs=14)
    for i, t in enumerate(["OpenAI", "Anthropic", "Gemini", "Groq"]):
        L.box(210 + i * 170, 300, 150, 50, t, "w", 16)
        if i < 3:
            L.texto(370 + i * 170, 325, "⇄", "#33414f", 20, True)
    L.texto(500, 380, "timeouts + circuit breaker + failover entre proveedores · reintentos durables con Temporal", "#5b6470", 15, italica=True)
    L.box(10, 410, 980, 60, "*SLO interno (más exigente que el SLA) → Error Budget → alertas de burn rate + status page", "l", 17)
    L.texto(500, 510, "Alertas del SRE Workbook de Google: 14,4× en 1 h → page · 1× en 3 días → ticket", "#5b6470", 15, italica=True)
    L.texto(500, 540, "Canary con Argo Rollouts: todavía no (sin SLO medido no sabe cuándo devolver)", "#0b2a4a", 15, True)
    return L.svg()


def d8():
    L = Lienzo(8)
    flujo = [(10, 150, "*Quien llama", "g"), (200, 170, "*Agente de voz", "b"), (410, 170, "*Transcripción\ny grabación", "b"),
             (620, 170, "*Proveedores\nde LLM", "g"), (830, 160, "*Herramientas\ndel agente\nCRM, calendario", "b")]
    for i, (x, w, t, c) in enumerate(flujo):
        L.box(x, 40, w, 90, t, c, 16)
        if i < 4:
            L.flecha(x + w, 85, flujo[i + 1][0] - 4, 85)
    riesgos = [(80, 200, "⚠ prompt injection\npor voz o WhatsApp", 180), (410, 170, "⚠ PII en la\ngrabación", 495),
               (620, 170, "⚠ datos a\nterceros", 705), (830, 160, "⚠ fuga entre\nclientes", 910)]
    for x, w, t, xo in riesgos:
        L.flecha(xo, 130, x + w / 2, 186, color="#c62828", dash=True)
        L.box(x, 190, w, 65, t, "r", 15)
    controles = [(40, 280, "*Mínimo privilegio\nguardrails · evals\nOWASP Top 10 for LLM"), (380, 230, "*Deepgram redact\nretención definida\nenlaces públicos apagados"),
                 (625, 190, "*ZDR y no\nentrenamiento\nregistro dato → proveedor"), (830, 160, "*Pruebas de\naislamiento por\ntenant en el\npipeline")]
    for (x, w, t), (rx, rw, _, _) in zip(controles, riesgos):
        L.flecha(rx + rw / 2, 255, x + w / 2, 296, color="#2e7d32")
        L.box(x, 300, w, 115, t, "v", 14)
    L.texto(500, 470, "Ninguno de los 79 controles publicados menciona IA: este es el diferencial", "#0b2a4a", 18, True)
    L.texto(500, 510, "+ consentimiento de grabación y TCPA por defecto (EE. UU.)", "#5b6470", 16, italica=True)
    return L.svg()


def d9():
    L = Lienzo(9)
    L.box(60, 30, 330, 140, "*① Detectar\nCloudTrail · GuardDuty\nSecurity Hub → Slack\nalertas de burn rate", "b", 17)
    L.box(610, 30, 330, 140, "*② Responder\nIncident Commander\nmitigar antes\nde diagnosticar", "d", 17)
    L.box(610, 370, 330, 140, "*③ Aprender\npost-mortem blameless\n≤ 5 días hábiles\nacciones con dueño", "b", 17)
    L.box(60, 370, 330, 140, "*④ Mejorar la plataforma\npolítica de Kyverno\npaso del pipeline\nSLO más fino", "v", 17)
    L.flecha(390, 100, 605, 100)
    L.flecha(775, 170, 775, 365)
    L.flecha(610, 440, 395, 440)
    L.flecha(225, 370, 225, 175, color="#2e7d32", ancho=4)
    L.box(370, 215, 260, 110, "*Cada vuelta deja\n*evidencia para Vanta\nsimulacro cada trimestre", "c", 16)
    L.texto(500, 540, "SIEM completo: todavía no (es para cuando haya alguien que lo mire)", "#5b6470", 16, italica=True)
    return L.svg()


def d10():
    L = Lienzo(10)
    L.texto(245, 25, "Qué traigo y qué no", "#0b2a4a", 18, True)
    for x, t, c in [(10, "*Ya lo tienen\n\nGitHub\nAWS\nVanta\nPostHog\nGrafana", "v"), (170, "*Nuevo\n\nArgo CD\nKyverno", "b"),
                    (330, "*Todavía no\n\nArgo Rollouts\nservice mesh\nSIEM", "g")]:
        L.box(x, 50, 150, 300, t, c, 17)
    L.box(10, 390, 470, 120, "*7 preguntas por herramienta + un ADR\ndolor · lo que ya hay · costo · operación\nreversibilidad · evidencia · adopción", "c", 16)
    L.texto(755, 25, "90 días · un servicio piloto", "#0b2a4a", 18, True)
    pasos = [("*Días 1–30: entender y apagar incendios\ninventario · línea base DORA · MFA · OIDC", "c"),
             ("*Días 31–60: la carretera con un piloto\nplantilla · Argo CD · Kyverno Audit · Payload Codec", "b"),
             ("*Días 61–90: todos por el camino nuevo\nKyverno Enforce · simulacro · siguiente certificación", "b")]
    for i, (t, c) in enumerate(pasos):
        L.box(520, 50 + i * 95, 470, 72, t, c, 15)
        if i < 2:
            L.flecha(755, 122 + i * 95, 755, 141 + i * 95)
    L.box(520, 340, 470, 170, "*Indicadores de éxito\n100% de despliegues por el pipeline\nDORA igual o mejor que la línea base\ncontroles de Vanta en verde\nmenos tiempo por cuestionario de seguridad", "v", 16)
    return L.svg()


DIAGRAMAS = {i: f() for i, f in enumerate([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10], start=1)}
