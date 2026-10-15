# Brecha de conocimiento — lo que Dapta necesita vs. lo que dominas hoy

Cruce de los **3 dolores confirmados en la entrevista** (certificaciones, estabilidad, métricas DORA) contra
`../../devops-senior/examenes/registro/progreso.md` al 2026-10-14.
Escala: ⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior. Prioridad: 🔥 crítica · ⬆️ alta · ➖ media.

## Hilo conductor — Deuda técnica (mencionada mucho en la entrevista)

| # | Tema | Nivel | Prioridad | Por qué en Dapta |
|---|---|---|---|---|
| 0a | Deuda técnica: principal e interés, cuadrante de Fowler, cómo priorizar | ⬜ | 🔥 | Es la causa común de los 3 dolores |
| 0b | Strangler Fig, criterio de salida, "lift and shift" como deuda nueva | ⬜ | 🔥 | Las migraciones a Kubernetes y Temporal |
| 0c | Hotspots (code churn × complejidad), registro de deuda, Boy Scout Rule, capacidad fija por sprint | ⬜ | ⬆️ | Cómo medir y pagar sin frenar producto |

## Dolor 1 — Certificaciones

| # | Tema | Nivel | Prioridad | Por qué en Dapta |
|---|---|---|---|---|
| 1 | **SOC 2 por dentro**: los 5 Trust Services Criteria, Type I vs. Type II, ventana de observación, *bridge letter*, excepciones y opinión con salvedades, *system description* | ⬜ | 🔥 | Ya tienen el Type II de 3 meses; el siguiente (12 meses) es el que se cae si los controles son de papel |
| 2 | **Compliance automation con Vanta**: integraciones, *tests* automáticos, evidencia, políticas, gestión de proveedores, trust center | ⬜ | 🔥 | Es su herramienta; hay que hablar de ella con propiedad |
| 3 | **Cuestionarios de seguridad** de clientes (SIG Lite, CAIQ) y paquete de seguridad para ventas | ⬜ | ⬆️ | Es donde se pierden los contratos Enterprise |
| 4 | **ISO 27001:2022**: SGSI (Sistema de Gestión de Seguridad de la Información), Anexo A (93 controles), Declaración de Aplicabilidad, auditoría etapa 1 y 2, auditorías de seguimiento; diferencias con SOC 2 | ⬜ | ⬆️ | Lo piden empresas de Europa y LatAm; reutiliza ~70-80% de SOC 2 (verificar cifra) |
| 5 | **Gestión de riesgos y modelado de amenazas** (STRIDE) | ⬜ | ⬆️ | Los controles "Risk assessments performed" y la base de cualquier certificación |
| 6 | HIPAA (BAA), PCI DSS (pagos por voz), GDPR / DPA, Ley 1581, LGPD, LFPDPPP | 🔴 (regulación 3/10, #79) | ➖ | Verticales de salud, cobranza y expansión a LatAm |
| 7 | **Cumplimiento de telefonía en EE. UU.**: TCPA, STIR/SHAKEN, A2P 10DLC, políticas de Meta para WhatsApp | ⬜ | ➖ (diferenciador) | Llamadas salientes masivas; casi ningún candidato lo va a traer |
| 8 | ISO 42001 (gestión de IA), OWASP Top 10 for LLM, seguridad de servidores MCP | 🟡 (MCP #75) | ➖ (diferenciador) | Su MCP tiene 139 herramientas y 19 destructivas |

## Dolor 2 — Estabilidad

| # | Tema | Nivel | Prioridad | Por qué en Dapta |
|---|---|---|---|---|
| 9 | SLI / SLO / SLA, Golden Signals | 🟡 (#64) | 🔥 | Prometen SLAs en Enterprise; la status page marca 100% con 5 incidentes |
| 10 | Error Budget y burn rate | 🟡 (#65, #66) | 🔥 | Decide cuándo frenar features y cuándo arreglar |
| 11 | **Error Budget Policy + progressive delivery** (Argo Rollouts, canary, rollback automático) | 🔴 (#67) | 🔥 | Une estabilidad con DORA: desplegar seguido sin romper |
| 12 | **Temporal**: workflows deterministas, activities, retries, timeouts, versionado, workers en Kubernetes, Temporal Cloud | ⬜ (puente: Durable Functions 🟢 #48) | 🔥 | Migración en curso; Flow Studio es el que tiene los incidentes |
| 13 | Gestión de incidentes y post-mortem blameless | 🟡 (#77) | ⬆️ | 5 incidentes en 5 días sin descripción pública |
| 14 | Resiliencia con dependencias externas: timeouts, circuit breaker, failover entre proveedores de LLM y de voz | 🟡 (#79) | ⬆️ | Dependen de OpenAI, Gemini, Groq, Deepgram, Twilio, LiveKit |
| 15 | **Infraestructura de voz en tiempo real**: WebRTC, SIP, LiveKit, latencia de punta a punta | ⬜ | ⬆️ | Es el corazón del producto y nunca lo has visto |
| 16 | Observabilidad: OpenTelemetry por dentro | 🟡/🔴 (#47, #68) | ➖ | Tienen Grafana; base para medir SLOs |
| 17 | Toil, on-call, chaos engineering | 🔴 (#78) | ➖ | 14 desarrolladores sin equipo de operaciones |

## Dolor 3 — Métricas DORA y el proceso de desarrollo

| # | Tema | Nivel | Prioridad | Por qué en Dapta |
|---|---|---|---|---|
| 18 | **Las métricas DORA** y su evolución (Time to Restore → Failed Deployment Recovery Time; *rework rate* en el modelo reciente) | 🔴 (#51b, 0/4 en el repaso estricto) | 🔥 | Te lo dijeron como dolor directo |
| 19 | **Cómo medir DORA** desde GitHub y Argo CD (Four Keys, o herramientas como LinearB / Sleuth) | ⬜ | 🔥 | Sin línea base no hay propuesta creíble |
| 20 | **Trunk-based development, feature flags** (LaunchDarkly / Unleash), lotes pequeños | ⬜ | 🔥 | Las palancas reales para subir la frecuencia y bajar las fallas |
| 21 | Estrategia de pruebas: pirámide de pruebas, ambientes efímeros por pull request, pruebas de contrato, **evaluaciones (evals) de agentes de IA** en el pipeline | ⬜ | ⬆️ | Un cambio de prompt también es un despliegue que puede romper |
| 22 | GitOps con Argo CD en la práctica | 🟡 (#22) | ⬆️ | Pilar 1 de la propuesta |
| 23 | GitHub Actions avanzado: reusable workflows, OIDC hacia AWS, environments con aprobación | 🟡 (#21 🟢, #23 🟡) | ⬆️ | Pilar 1 de la propuesta |

## Lo que ya tienes y sostiene la propuesta

| Tema | Nivel |
|---|---|
| Kubernetes: troubleshooting, arquitectura, networking (#50, #1, #3) | 🔵 / 🟢 |
| IRSA, RBAC, Key Vault/Secrets Manager (#27, #28, #44) | 🟢 |
| OPA / políticas como código (#42) | 🟢 |
| Terraform: state, backends (#7, #8) | 🟢 |
| Platform Engineering, golden path (#51) | 🟢 |
| CI/CD tradicional (#21) | 🟢 |

## Lectura

- **La base de plataforma es tu fuerte** (Kubernetes, IAM, políticas, Terraform): la migración a Kubernetes juega a tu favor.
- **Los tres dolores de Dapta caen justo en tus zonas más débiles**: certificaciones (todo ⬜), DORA (🔴) y la
  parte "dura" de estabilidad (Error Budget Policy 🔴, Temporal ⬜).
- Orden sugerido de estudio: **18 → 19 → 20** (DORA, el dolor más directo y el más fácil de cerrar) →
  **1 → 2** (SOC 2 y Vanta) → **12** (Temporal) → **9 → 10 → 11** (repaso de lo de Davivienda, aplicado a Dapta).
