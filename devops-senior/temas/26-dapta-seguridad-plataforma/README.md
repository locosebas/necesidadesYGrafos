# Proceso de selección Dapta — Seguridad de infraestructura ("defensa")

> ⚠️ Este repo es **público** en GitHub. Aquí solo va información pública de Dapta (su web y su
> trust center) y lo que tú decidas contar de la entrevista. Nada que te hayan compartido como
> confidencial (nombres de clientes, incidentes, arquitectura interna sensible).

## Origen

- **2026-10-13 (aprox.)**: primera entrevista. El equipo de ingeniería se divide en **"ataque"** y
  **"defensa"**; el cargo es de **defensa**: organizar todo el proceso de seguridad de infraestructura.
- Dolor que te contaron: **les cuesta certificarse**, y sus compradores les exigen ciertas certificaciones.
- Tamaño: **~14 desarrolladores**.

**Objetivo de esta ruta:** no llegar como "alguien que sabe", sino como alguien que **ya trae una
propuesta de valor**: (1) caracterizar la necesidad, (2) proponer la solución, (3) defenderla.
Mismo formato que la prueba Davivienda (rama `davivienda-sre-prueba-tecnica`, tema 25).

Ruta y avance: [roadmap-express.md](roadmap-express.md) · **Chuleta de nombres: [chuleta-nombres.md](chuleta-nombres.md)** · Caracterización: [caracterizacion.md](caracterizacion.md) · **Propuesta: [propuesta-valor.md](propuesta-valor.md)**

## Qué es Dapta (fuentes públicas, revisadas el 2026-10-14)

| Dato | Valor | Fuente |
|---|---|---|
| Producto | Agentes de IA (Inteligencia Artificial) de **voz y texto** para ventas: recepcionista, calificador de leads, cobranza, soporte, selección de candidatos de RR. HH. Canales: llamada telefónica, WhatsApp, SMS, chat web. También "Dapta MCP" (Model Context Protocol) | dapta.ai |
| Clientes | Pymes, sobre todo en EE. UU.; verticales: educación, SaaS, finca raíz, **fintech**, **abogados**, **seguros**, **cobranza**, servicios del hogar | dapta.ai |
| Escala que declaran | "50.000+ empresas" (la cifra varía según la fuente: 30.000 a 120.000 cuentas) | dapta.ai, Portafolio, página de empleos |
| Fundador | Nicolás Rojas (antes Imagine Apps); pasó por 500 Startups (2023) | Forbes Colombia, GrowthTalent |
| Financiación | Pre-semilla de USD 1,2 M; GrowthTalent habla de USD 5,4 M en total | ENTER.CO, El Referente, GrowthTalent |
| Sedes | Phoenix (Arizona) y Bogotá | página de empleos |
| Precios | Gratis → Pro USD 99 → Scale Up USD 499 → Prime USD 1.499/mes | dapta.ai |

### Lo que dice su trust center (`trust.dapta.ai`, plataforma **Vanta**)

| Marco | Estado |
|---|---|
| **SOC 2 Type II** (System and Organization Controls 2) | "Verified", bajo NDA (Non-Disclosure Agreement). Auditor: Advantage Partners. **Periodo observado: 26-may → 26-ago-2026 (solo 3 meses). Emitido: 10-sep-2026** |
| ISO 27001, ISO 42001, HIPAA, GDPR, PCI DSS | **No aparecen** |

- **79 controles** publicados, todos de la plantilla estándar de SOC 2 de Vanta (acceso, MFA, logs,
  respuesta a incidentes, DR, gestión de proveedores...). El propio sitio dice que siguen en estado
  **"Draft"** hasta que un revisor de Dapta los verifique.
- **Ningún control menciona IA ni LLM** (Large Language Model), a pesar de que el producto es 100% IA.
- **30 subprocesadores**, entre ellos: AWS (Amazon Web Services), Cloudflare, LiveKit, Twilio,
  Deepgram, OpenAI, Anthropic, Gemini, Groq, Temporal, Grafana Labs, PostHog, Metabase, WorkOS,
  KnowBe4, GitHub, Stripe, y uno llamado **"Medical AI"**.
- La política de privacidad es mínima: no nombra subprocesadores, ni retención de grabaciones de
  llamadas, ni ubicación del dato; no menciona GDPR, CCPA, HIPAA ni la Ley 1581 de 2012 (Colombia).

### Lectura inicial (hipótesis, se valida en la caracterización)

1. **SOC 2 Type II ya lo tienen, pero recién salido y con la ventana mínima de 3 meses.** El reto
   ya no es "sacarlo" sino **mantenerlo vivo** (siguiente auditoría de 12 meses) sin que dependa de
   una sola persona ni de controles "en papel".
2. Si los compradores siguen pidiendo certificaciones, lo más probable es que pidan **otras**:
   ISO 27001 (Europa/LatAm/enterprise), **HIPAA** (salud: "Medical AI" en los subprocesadores),
   **PCI DSS** (cobros por teléfono en cobranza/fintech), **ISO 42001** (gestión de IA) o
   respuestas a **cuestionarios de seguridad** de clientes grandes.
3. El riesgo propio del producto (voz + LLM) **no está cubierto por ningún control**: consentimiento
   de grabación, PII (Personally Identifiable Information) en transcripciones, datos enviados a
   proveedores de LLM, prompt injection por teléfono, suplantación de voz, TCPA (Telephone Consumer
   Protection Act) en EE. UU.

### Hallazgos de la segunda búsqueda (2026-10-14)

| Dato | Valor | Fuente |
|---|---|---|
| **Ronda semilla de USD 6 M** anunciada el **13-oct-2026** (un día antes de esta nota) | Lidera Chingona Ventures; también Crew Capital, Broom Ventures, Cometa VC, 500 Global, Fen Ventures. Total levantado: USD 7,4 M. Uso: expansión EE. UU. + LatAm, producto y **crecimiento del equipo** | GlobeNewswire, FinSMEs |
| Tracción | Dapti con +200 mil usuarios (+4 mil por semana); ingresos se duplicaron en 6 meses; ingreso anual esperado > USD 4 M | GlobeNewswire |
| **Plan Enterprise** | "Enterprise-grade security", **despliegue on-premise**, soporte premium **con SLAs** (Service Level Agreements). Precio por consumo | docs.dapta.ai (Plans and Pricing) |
| Status page | `status.dapta.ai` (Qodex). Componentes: Dapta, Text Agents, **Flow Studio**. Flow Studio tuvo **5 incidentes de ~30 min entre el 8 y el 12 de octubre**, y aun así marca 100,0% de uptime | status.dapta.ai |
| Dapta MCP | Servidor MCP con **139 herramientas** (112 de lectura, 8 de escritura aditiva, 19 destructivas con "preview → commit"); login OAuth o API keys (máx. 10 por workspace); 60 llamadas/min; está en el directorio de conectores de Claude | docs.dapta.ai (Dapta MCP) |
| Enlaces de grabación | Interruptor "Public call link": si está encendido, cualquiera con el enlace `files.dapta.ai/calls/...` escucha la grabación y lee la transcripción | docs.dapta.ai |
| Changelog reciente | Variables de credenciales tipo "vault" en Flow Studio (sep.), grabaciones servidas por `files.dapta.ai` sin exponer el almacenamiento (sep.), login OAuth en el MCP con auditoría por usuario (oct.) | changelog.dapta.ai |
| Producto | Voice Agents, Text Agents (WhatsApp vía Meta), **Flow Studio** (automatizaciones), Dapta Databases, Sales Intelligence (notetaker), Dapti (asistente) | docs.dapta.ai |

Fuentes nuevas: https://www.globenewswire.com/news-release/2026/10/13/3379778/0/en/dapta-raises-6m-to-accelerate-the-adoption-of-ai-sales-agents-to-smbs-across-the-u-s-and-latin-america.html ·
https://www.finsmes.com/2026/10/dapta-raises-6m-in-seed-funding.html · https://status.dapta.ai · https://changelog.dapta.ai · https://docs.dapta.ai/llms.txt

## Fuentes

- https://dapta.ai · https://dapta.ai/privacy-policy · https://trust.dapta.ai/en · https://trust.dapta.ai/en/controls
- https://www.portafolio.co/tecnologia/ia-de-dapta-automatiza-ventas-en-empresas-de-colombia-632969
- https://www.enter.co/?p=553260 · https://elreferente.es/america/inversiones/dapta-recauda-1m-ronda-inversion-pre-semilla
- https://forbes.co/emprendedores/nicolas-rojas-imagine-apps-y-dapta · https://www.growthtalent.org/insights/nicolas-rojas-profile
