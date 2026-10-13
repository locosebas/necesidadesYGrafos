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
    L.box(70, 50, 320, 120, "*① SLO del pago QR\n+ Error Budget\nqué es estar bien")
    L.box(610, 50, 320, 120, "*② Quality Gate en CI/CD\nfrena despliegues malos\nprotege el SLO")
    L.box(610, 390, 320, 120, "*③ OpenTelemetry + MCP\ndatos limpios y sin PII\npara la IA: explica el SLO")
    L.box(70, 390, 320, 120, "*④ Incident Commander\n+ post-mortem blameless\nlas personas aprenden")
    L.flecha(390, 110, 605, 110)
    L.flecha(770, 170, 770, 385)
    L.flecha(610, 450, 395, 450)
    L.flecha(230, 390, 230, 175, "acciones →\nmejores SLOs", 130, 260, color="#2e7d32", ancho=4)
    L.box(400, 225, 340, 110, "*Una sola causa:\nfalta un 'estar bien' medible\ny datos estandarizados", "c", 17)
    return L.svg()


def d2():
    L = Lienzo(2)
    L.box(350, 200, 300, 150, "*Plataforma de pagos\n*de Banco Plus\nmicroservicios en Kubernetes\nAWS (EKS) + GCP (GKE)", "b", 18)
    for y, t in [(40, "Cliente en la app\n[persona]"), (245, "Tribus de desarrollo\n[persona]"), (450, "Incident Commander\n/ on-call [persona]")]:
        L.box(30, y, 230, 75, t, "d")
    for y, t in [(40, "Comercio\n[persona]"), (175, "Core bancario\n[sistema externo]"), (310, "Transferencias CBU\ny otros bancos [externo]"),
                 (450, "Observabilidad actual\ndel banco [sistema]")]:
        L.box(740, y, 230, 75, t, "d" if y == 40 else "g")
    L.flecha(260, 78, 350, 215, "paga con QR", 345, 112)
    L.flecha(260, 282, 345, 282, "reto 1:\nsin freno", 302, 230, color="#c62828")
    L.flecha(650, 215, 740, 80, "confirma", 630, 140)
    L.flecha(650, 250, 738, 212, "reto 3: la traza\nse corta aquí", 700, 262, color="#c62828", dash=True)
    L.flecha(650, 320, 738, 345, "transferencia en\ntiempo real", 665, 362)
    L.flecha(600, 350, 760, 448, "reto 2: telemetría sin\nestándar, paga por volumen", 600, 405, color="#c62828")
    L.flecha(260, 500, 735, 500, "reto 3: diagnostica con MTTR largo · reto 4: la IA no entiende datos desordenados", 498, 535, color="#c62828")
    return L.svg()


def d3():
    L = Lienzo(3)
    L.texto(500, 30, "Error Budget del pago QR (SLO de partida 99,9% en 30 días, se calibra en la Fase 0)", "#0b2a4a", 19, True)
    L.box(40, 60, 300, 150, "*🟢 Sano\nCanary por defecto\n(la estrategia que\nmenos presupuesto gasta)", "v", 18)
    L.box(350, 60, 300, 150, "*🟡 En riesgo\nSolo canary lento\ny análisis estricto", "y", 18)
    L.box(660, 60, 300, 150, "*🔴 Crítico\nCongelado salvo\narreglos de confiabilidad", "r", 18)
    L.flecha(340, 135, 350, 135)
    L.flecha(650, 135, 660, 135)
    L.texto(500, 235, "← se va gastando el presupuesto →   ·   umbrales de cada zona: se negocian con negocio, con datos", "#5b6470", 16, italica=True)
    L.box(40, 270, 920, 60, "*Error Budget Policy de conservación, firmada con negocio\nsiempre la estrategia de despliegue que menos Error Budget gasta", "l", 16)
    L.texto(500, 370, "Dependencias en serie: la disponibilidad se multiplica", "#0b2a4a", 18, True)
    for i, t in enumerate(["Servicio A\n99,9%", "Servicio B\n99,9%", "Servicio C\n99,9%"]):
        L.box(60 + i * 230, 400, 180, 80, t, "w", 18)
        L.flecha(240 + i * 230, 440, 285 + i * 230, 440)
    L.box(750, 400, 200, 80, "*0,999³ ≈ 99,7%", "c", 20)
    L.texto(500, 520, "→ las dependencias críticas necesitan un SLO más exigente o redundancia", "#5b6470", 16, italica=True)
    return L.svg()


def d4():
    L = Lienzo(4)
    for x, t in [(20, "ANTES · plantilla"), (350, "DURANTE · canary"), (680, "DESPUÉS")]:
        L.box(x, 15, 300, 390, "", "w")
        L.texto(x + 150, 40, t, "#0b2a4a", 17, True)
    L.box(45, 65, 250, 55, "Commit", "g")
    L.box(45, 145, 250, 75, "Build, pruebas, seguridad\n(mínimos + lo de la tribu)", "g", 16)
    L.box(45, 245, 250, 95, "*Gate 1\ndeployment protection rule\n¿hay Error Budget?", "b", 16)
    L.flecha(170, 120, 170, 140)
    L.flecha(170, 220, 170, 240)
    L.box(45, 355, 250, 40, "⛔ congelado: no se despliega", "r", 15)
    L.flecha(170, 340, 170, 352, color="#c62828")
    L.box(375, 65, 250, 60, "Canary: % pequeño\n(Argo Rollouts o Flagger)", "b", 15)
    L.box(375, 150, 250, 95, "*Gate 2\nanálisis automático\ncanary vs. estable", "b", 16)
    L.box(375, 270, 250, 50, "Pasos crecientes → 100%", "v", 16)
    L.box(375, 340, 250, 50, "↩ empeora: rollback automático", "r", 15)
    L.flecha(500, 125, 500, 145)
    L.flecha(500, 245, 500, 265, color="#2e7d32")
    L.flecha(295, 290, 372, 95)
    L.box(705, 65, 250, 95, "*Gate 3\nverificación posterior\ndel burn rate", "b", 16)
    L.box(705, 190, 250, 95, "Evento 'cambio desplegado'\n→ registro de cambios\n(lo consulta el MCP)", "c", 16)
    L.flecha(830, 160, 830, 185)
    L.flecha(625, 295, 702, 112)
    L.texto(500, 440, "Alertas multi-window, multi-burn-rate (valores del SRE Workbook de Google)", "#0b2a4a", 18, True)
    for i, t in enumerate(["14,4× en 1 h → page", "6× en 6 h → page", "1× en 3 días → ticket"]):
        L.box(40 + i * 320, 470, 280, 60, t, "y" if i < 2 else "w", 18)
    return L.svg()


def d5():
    L = Lienzo(5)
    L.box(15, 20, 770, 300, "", "w", dash=True, borde=3)
    L.p[-1] = L.p[-1].replace('stroke="#9aa5b1"', 'stroke="#d32f2f"')
    L.texto(400, 45, "🔒 Red del banco · igual en AWS (EKS) y en GCP (GKE) · ninguna PII sale", "#c62828", 17, True)
    L.box(30, 90, 160, 150, "*Apps\nenmascaran\nsu PII\n(plantilla)\nOTel Operator", "d", 16)
    L.box(215, 90, 160, 150, "*Agente\nDaemonSet\npor nodo\nmetadatos K8s\nbota health checks", "b", 16)
    L.box(400, 90, 160, 150, "*Gateway\n*capa 1\nloadbalancing\npor traceID", "b", 16)
    L.box(585, 70, 185, 230, "*Gateway capa 2\n(imagen OCB)\n\nredaction\n(seguridad extra PII)\n\nspanmetrics +\nservicegraph (100%)\n\ntail_sampling", "b", 15)
    for x in (190, 375, 560):
        L.flecha(x, 165, x + 22, 165)
    L.box(820, 120, 165, 120, "*Backend que\n*ya tenga el banco\n(ej.: Mimir,\nTempo, Loki)\nvía OTLP + mTLS", "g", 14)
    L.flecha(770, 180, 817, 180)
    L.box(30, 380, 200, 80, "Conector del core\ninstrumentado", "b", 16)
    L.box(330, 380, 200, 80, "Core bancario", "g", 18)
    L.flecha(230, 420, 327, 420, "traceparent", 280, 400, fs=14)
    L.flecha(110, 240, 110, 377, "llamadas al core", 175, 300, fs=14)
    L.box(600, 380, 380, 80, "*Auditoría regulatoria\npipeline aparte · sin muestreo · inmutable", "c", 16)
    L.texto(500, 515, "Exporta al backend actual: no se cambia de proveedor. La traza ya no se corta en el core.", "#5b6470", 16, italica=True)
    return L.svg()


def d6():
    L = Lienzo(6)
    L.box(20, 140, 230, 200, "*1. Estudio de\n*línea base\n\nGB/día por señal\ny por servicio\nmayores emisores\nfactura actual", "d", 16)
    L.texto(500, 40, "2. Palancas", "#0b2a4a", 19, True)
    L.box(300, 65, 400, 110, "*Trazas → tail_sampling\n100% errores · 100% más lentos que el SLO\nun porcentaje pequeño de exitosos", "b", 16)
    L.box(300, 190, 400, 85, "*Logs → Log-to-Metrics\n(connector count) + filter de DEBUG", "b", 16)
    L.box(300, 290, 400, 85, "*Métricas → cardinalidad\nningún ID de cliente como etiqueta", "b", 16)
    L.box(750, 140, 230, 200, "*3. Medir antes\n*y después\n\nmeta del caso: −30%\nshowback por tribu", "v", 16)
    L.flecha(250, 240, 296, 240)
    L.flecha(700, 240, 746, 240)
    L.box(280, 392, 440, 60, "spanmetrics antes del muestreo:\nmétricas exactas al 100%", "c", 15)
    L.box(20, 475, 960, 65, "*Referencias públicas: Capital One ~70% menos volumen de trazas con OpenTelemetry ·\nPismo (pagos) ~80% menos costo de observabilidad con tail sampling", "l", 16)
    return L.svg()


def d7():
    L = Lienzo(7)
    L.box(20, 40, 190, 70, "📟 Alerta de\nburn rate", "y", 17)
    L.box(20, 160, 190, 170, "*🤖 Agente de RCA\ndentro del banco\n\nmodelo (ej. Claude\no Gemini) vía\nBedrock / Vertex AI", "d", 15)
    L.flecha(115, 110, 115, 155, "webhook", 160, 133, fs=14)
    L.box(270, 20, 330, 400, "", "w")
    L.texto(435, 45, "Servidor MCP propio", "#0b2a4a", 18, True)
    L.texto(435, 70, "solo lectura · cada llamada auditada", "#5b6470", 14, italica=True)
    for i, t in enumerate(["1. obtener_grafo", "2. consultar_slo", "3. buscar_trazas", "4. buscar_logs(trace_id)", "+ cambios_recientes"]):
        L.box(295, 95 + i * 62, 280, 48, t, "b" if i < 4 else "c", 16)
    L.flecha(210, 245, 266, 245)
    L.box(660, 60, 320, 120, "*Telemetría nueva\nOpenTelemetry + Semantic\nConventions, sin PII", "g", 16)
    L.box(660, 200, 320, 100, "*Telemetría heredada\nadaptadores temporales\n(strangler fig)", "w", 16, dash=True)
    L.box(660, 320, 320, 80, "Registro de cambios\ndel Quality Gate", "c", 16)
    L.flecha(600, 150, 656, 120)
    L.flecha(600, 230, 656, 250, dash=True)
    L.flecha(600, 360, 656, 360)
    L.box(20, 460, 960, 70, "*🔒 Hipótesis rankeadas con evidencia → el Incident Commander decide (humano en el bucle)", "d", 18)
    L.flecha(115, 330, 115, 455)
    return L.svg()


def d8():
    L = Lienzo(8)
    L.box(20, 15, 420, 385, "", "w", dash=True)
    L.p[-1] = L.p[-1].replace('fill="#f4f6f9"', 'fill="#fdecec"').replace('stroke="#9aa5b1"', 'stroke="#c62828"')
    L.texto(230, 38, "💥 Radio de explosión (BFS)", "#c62828", 16, True)
    L.box(30, 60, 200, 80, "*cambios_recientes:\nAntifraude v2.3.1\nhace 12 min", "c", 15)
    L.box(255, 60, 165, 60, "App QR\n🔴 anómalo", "r", 16)
    L.box(255, 170, 165, 70, "API pagos 🔴\nel que más grita:\nvíctima", "r", 15)
    L.box(40, 290, 230, 90, "*Antifraude 🔴\ndependencias sanas\n→ causa raíz candidata", "r", 15, borde=5)
    L.p[-4] = L.p[-4].replace('stroke="#8e0000"', 'stroke="#ffd600"')
    L.box(490, 300, 160, 60, "Saldos\n🟢 sano", "v", 16)
    L.box(720, 170, 200, 60, "Notificaciones\n🟢 sano", "v", 16)
    L.box(40, 460, 230, 60, "BD de reglas 🟢 sana", "v", 16)
    L.box(490, 460, 160, 60, "Conector\ndel core 🟢", "v", 15)
    L.box(720, 460, 200, 60, "Core bancario\n🟢 sano", "v", 15)
    L.flecha(337, 120, 337, 165, "DFS", 368, 142, color="#d9a400", ancho=5)
    L.flecha(300, 240, 200, 286, "DFS", 222, 252, color="#d9a400", ancho=5)
    L.flecha(400, 240, 520, 296)
    L.flecha(420, 205, 716, 200)
    L.flecha(155, 380, 155, 456)
    L.flecha(570, 360, 570, 456)
    L.flecha(650, 490, 716, 490)
    L.flecha(130, 140, 130, 286, dash=True, color="#c17900")
    L.texto(820, 330, "Causa = nodo anómalo más profundo", "#5b6470", 15, italica=True)
    L.texto(820, 352, "con dependencias sanas", "#5b6470", 15, italica=True)
    return L.svg()


def d9():
    L = Lienzo(9)
    x = lambda m: 200 + m * 12.5
    L.p.append(f'<line x1="{x(0)}" y1="500" x2="{x(60)}" y2="500" stroke="#33414f" stroke-width="2"/>')
    for m in (0, 10, 20, 30, 40, 50, 60):
        L.texto(x(m), 522, f"{m}'", "#5b6470", 15)
    L.texto(x(30), 548, "minutos desde las 12:30 de un día de quincena", "#5b6470", 14, italica=True)
    for y, t, c in [(80, "Incident\nCommander", "d"), (195, "Agente de RCA\n(automático)", "y"),
                    (305, "Responsable\ntécnico", "b"), (420, "Comunicaciones\n(SEV1)", "g")]:
        L.box(10, y - 32, 170, 64, t, c, 15)
        L.p.append(f'<line x1="{x(0)}" y1="{y}" x2="{x(60)}" y2="{y}" stroke="#d5dbe2" stroke-width="2"/>')

    def hito(m, y, t, arriba, c="#08427b", ancla="middle"):
        L.p.append(f'<circle cx="{x(m)}" cy="{y}" r="9" fill="{c}"/>')
        for i, l in enumerate(t.split("\n")):
            L.texto(x(m), y + (-36 if arriba else 28) + i * 18, l, c, 15, True, ancla)

    def barra(a, b, y, t, c, tc="#fff"):
        L.p.append(f'<rect x="{x(a)}" y="{y - 15}" width="{x(b) - x(a)}" height="30" rx="6" fill="{c}"/>')
        L.texto((x(a) + x(b)) / 2, y, t, tc, 14, True)

    hito(0, 80, "0' alerta", True, "#c62828", "start")
    hito(3.5, 80, "2–5' SEV1 y roles", False, ancla="start")
    hito(10, 80, "10' decide rollback", True, "#c62828", "start")
    hito(60, 80, "post-mortem", True, ancla="end")
    barra(0, 8, 195, "hipótesis", "#f9a825", "#1b1b1b")
    L.texto(x(8) + 10, 172, "→ en el canal antes de que llegue el on-call", "#c17900", 14, True, "start", True)
    barra(5, 10, 305, "revisa", "#1168bd")
    barra(10, 20, 305, "rollback", "#c62828")
    barra(20, 60, 305, "monitoreo hasta que esté estable", "#2e7d32")
    hito(20, 305, "20' SLI recuperado", False, "#2e7d32")
    barra(15, 60, 420, "comunicados con hechos, frecuencia fija", "#8a8a8a")
    hito(15, 420, "15' primer comunicado", True, "#6b6b6b", "start")
    return L.svg()


def d10():
    L = Lienzo(10)
    L.texto(230, 25, "El ciclo se cierra", "#0b2a4a", 18, True)
    for i, t in enumerate(["① SLO + Error Budget", "② Quality Gate", "③ OpenTelemetry + MCP", "④ Incident Commander"]):
        L.box(20, 50 + i * 80, 260, 55, t, "b", 16)
        if i < 3:
            L.flecha(150, 105 + i * 80, 150, 127 + i * 80)
    L.box(20, 380, 260, 110, "*Post-mortem blameless\n≤ 5 días hábiles\nacciones con dueño y fecha", "d", 15)
    L.flecha(150, 345, 150, 376)
    L.p.append('<path d="M280,435 C360,435 360,77 285,77" fill="none" stroke="#2e7d32" stroke-width="4" marker-end="url(#m10' + '2e7d32)"/>')
    L.colores = getattr(L, "colores", set()) | {"#2e7d32"}
    L.texto(410, 255, "acciones", "#2e7d32", 15, True)
    L.texto(410, 275, "→ Eje 1", "#2e7d32", 15, True)
    L.texto(700, 25, "Hoja de ruta · piloto: pago QR", "#0b2a4a", 18, True)
    pasos = [("*Fase 0 (2–4 semanas)\ncaracterizar lo que existe", "c"), ("*30 días\nSLO calibrado + burn rate", "b"),
             ("*60 días\nQuality Gate + gateway con PII", "b"), ("*90 días\ntail sampling medido + MCP", "b")]
    for i, (t, c) in enumerate(pasos):
        L.box(470, 50 + i * 85, 460, 62, t, c, 16)
        if i < 3:
            L.flecha(700, 112 + i * 85, 700, 132 + i * 85)
    L.box(470, 400, 460, 130, "*Indicadores de éxito\nChange Failure Rate y Time to Restore\ncontra la línea base · costo: meta −30%\ntoil por debajo del 50%", "v", 16)
    return L.svg()


DIAGRAMAS = {i: f() for i, f in enumerate([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10], start=1)}
