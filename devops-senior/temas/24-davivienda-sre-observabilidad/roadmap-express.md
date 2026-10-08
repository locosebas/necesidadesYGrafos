# Roadmap express — Prueba técnica Davivienda (8 al 12 de octubre de 2026)

Objetivo: llegar a la exposición (20 min + 10 min de preguntas ante SRE, Arquitectura, DevSecOps y
Operaciones) siendo **experto** en los temas marcados, no "haberlos leído".

**Criterio de experto** para marcar un ítem 🟢/🔵 (misma escala de `../../examenes/registro/progreso.md`):
1. Dices el **nombre** de la técnica/herramienta sin pista cuando te describen el mecanismo.
2. Lo explicas con **números** (porcentajes, minutos, costos) y con al menos un **trade-off**.
3. Lo aplicas al caso de Banco Plus (pagos QR / transferencias en tiempo real).

Preguntas para cada ítem: [`banco-preguntas.md`](banco-preguntas.md) (se hacen **de a una**).
Escala: ⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior.

## Bloque A — SRE: SLOs, Error Budgets y Quality Gates (jueves 8) → Eje 1

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| A1 | SLI (Service Level Indicator), SLO (Service Level Objective), SLA (Service Level Agreement); Golden Signals, métodos RED y USE | ⬜ | 🔵 |
| A2 | Error Budget y matemáticas de disponibilidad (los "nueves", dependencias en serie y en paralelo) | ⬜ | 🔵 |
| A3 | Alertas por burn rate (multi-window, multi-burn-rate) | ⬜ | 🟢 |
| A4 | Error Budget Policy + Quality Gate en CI/CD (GitHub Actions / GitLab CI) + progressive delivery (Argo Rollouts / Flagger) | ⬜ | 🔵 |
| A5 | Métricas DORA (DevOps Research and Assessment) — reintento | 🔴 | 🟢 |

## Bloque B — OpenTelemetry por dentro y FinOps de telemetría (viernes 9) → Eje 2

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| B1 | OpenTelemetry Collector: receivers → processors → exporters, connectors, pipelines | ⬜ | 🔵 |
| B2 | Despliegue del Collector: agente (DaemonSet/sidecar) vs. gateway, arquitectura de dos capas, multi-cloud | ⬜ | 🔵 |
| B3 | Head-based vs. tail-based sampling y sus políticas | ⬜ | 🔵 |
| B4 | Propagación de contexto: W3C `traceparent`/`baggage`, B3, span links en Kafka/MQ | 🟡 (base Kafka 🟢) | 🟢 |
| B5 | FinOps de telemetría: cardinalidad, Log-to-Metrics, retención por niveles, filtrado en el borde | ⬜ | 🟢 |
| B6 | Enmascaramiento de PII (Personally Identifiable Information) en el Collector — SFC y Ley 1581 | ⬜ | 🟢 |

## Bloque C — Telemetría AI-Ready, MCP e IA para RCA (sábado 10 mañana) → Eje 3

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| C1 | Semantic Conventions y resource attributes de OpenTelemetry | ⬜ | 🟢 |
| C2 | Grafo de topología de servicios (service graph) a partir de trazas | ⬜ | 🟢 |
| C3 | AIOps: correlación vs. causalidad, RCA (Root Cause Analysis) asistido | ⬜ | 🟢 |
| C4 | MCP (Model Context Protocol) aplicado a observabilidad + sus riesgos | 🟡 (CCA-F) | 🔵 |
| C5 | *(Opcional)* Teoría de grafos para acelerar el troubleshooting — ver [`grafos-troubleshooting.md`](grafos-troubleshooting.md) | ⬜ | 🟡 |

## Bloque D — Incidentes y cultura (sábado 10 tarde) → Eje 4

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| D1 | Incident Command: roles, severidades, comunicación | ⬜ | 🔵 |
| D2 | Mitigar primero: rollback, feature flags, failover, load shedding, circuit breaker | 🟡 (troubleshooting K8s 🔵) | 🔵 |
| D3 | Post-mortem blameless y acciones accionables | ⬜ | 🔵 |
| D4 | Toil, on-call, Runbook as Code, chaos engineering | ⬜ | 🟢 |

## Bloque E — Temas aledaños: la ronda de preguntas de la mesa (domingo 11 mañana)

Lo que no está en los 4 ejes pero puede salir en los 10 minutos de preguntas.

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| E1 | Confiabilidad en pagos: idempotencia, reintentos con backoff + jitter, timeouts | ⬜ | 🟢 |
| E2 | Recuperación ante desastres: RTO/RPO, activo-activo multi-región / multi-cloud | ⬜ | 🟢 |
| E3 | Percentiles, histogramas y cardinalidad (Prometheus) | 🟡 | 🟢 |
| E4 | Capacidad: Ley de Little, autoscaling, saturación | 🟡 | 🟢 |
| E5 | Seguridad de la plataforma de observabilidad (mTLS, supply chain, prompt injection por logs) | 🟡 | 🟢 |
| E6 | Regulación: SFC, Ley 1581 de 2012, PCI DSS (Payment Card Industry Data Security Standard) | ⬜ | 🟡 |
| E7 | Well-Architected — pilar de confiabilidad | 🟡 | 🟢 |

## Bloque F — Entregable (domingo 11 tarde – lunes 12)

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| F1 | Diagramas C4 (Context, Container, Component, Code) | ⬜ | 🟢 |
| F2 | Guion de las 10 diapositivas (una historia: SLO → telemetría → IA → incidente) | ⬜ | ✅ |
| F3 | Ensayo cronometrado de 20 min + simulacro de 10 min de preguntas | ⬜ | ✅ |

## Hilo conductor de la presentación

Los 4 ejes son una sola historia, no cuatro temas sueltos:

```
SLOs del pago QR  ──►  Quality Gate frena despliegues malos        (Eje 1)
      │
      ▼
OTel Collector: datos limpios, muestreados y sin PII, más baratos  (Eje 2)
      │
      ▼
Semantic Conventions + grafo de topología ──► IA causal vía MCP    (Eje 3)
      │
      ▼
Incident Commander usa todo lo anterior → post-mortem → nuevos SLOs (Eje 4)
```
