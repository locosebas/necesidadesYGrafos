# Brecha técnica — prueba Davivienda vs. lo estudiado

Cruce de `caso-de-uso-especialista-i-plataforma-confiabilidad.md` (y de la rúbrica, por si el cargo es
Especialista II / Tech Lead) contra `../../examenes/registro/progreso.md` al 2026-10-08.
Escala: ⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior.

## Lo que ya tienes y sirve para la prueba

| # | Tema (progreso.md) | Nivel | Dónde suma en la prueba |
|---|---|---|---|
| 1 | Kubernetes troubleshooting (#50) | 🔵 | Eje 4: mitigación inmediata como Incident Commander |
| 2 | Kubernetes arquitectura y networking, Istio (#1, #3) | 🟢 | Eje 2: dónde corre el OTel Collector (DaemonSet vs. Deployment) |
| 3 | Kafka/Redpanda vs. SQS (#49) | 🟢 | Rúbrica ítem 1: propagar contexto de trazas por colas/MQ |
| 4 | Platform Engineering, IDP, Team Topologies (#51) | 🟢 | Rúbrica ítems 6 y 7: habilitador, autoservicio |
| 5 | RAG, embeddings (#32, #33) | 🟢 | Eje 3: base para hablar de telemetría consumida por IA |
| 6 | CI/CD tradicional (#21) | 🟢 | Eje 1: el pipeline donde vive el Quality Gate |
| 7 | Key Vault + Managed Identity, OPA, Trivy (#44, #42, #41) | 🟢/🟡 | Seguridad del diseño (DevSecOps está en la mesa) |
| 8 | OpenTelemetry — señales, traces vs. alertas (#47) | 🟡 | Eje 2. **Solo consumo**, nunca configuraste la instrumentación |
| 9 | MCP (CCA-F área 18) | 🟡 | Eje 3 |
| 10 | FinOps / Well-Architected (#52) | 🟡 | Eje 2 y rúbrica ítem 4 |
| 11 | GitOps / ArgoCD, OIDC (#22, #23) | 🟡 | Eje 1: rollback automático |
| 12 | GitLab CI (#24) | 🔴 | Eje 1 lo nombra junto a GitHub Actions |
| 13 | Métricas DORA (#51b) | 🔴 | Eje 1 y 4: Change Failure Rate y Time to Restore (MTTR) son exactamente los dolores del caso |

## Lo que la prueba pide y nunca se ha visto (⬜)

| # | Concepto | Eje / ítem | Prioridad |
|---|---|---|---|
| 14 | SLI, SLO, SLA, Golden Signals | Eje 1 | 🔥 Crítica |
| 15 | Error Budget y alertas por burn rate (multi-window) | Eje 1 | 🔥 Crítica |
| 16 | Quality Gate que consulta el Error Budget + rollback automático (canary analysis) | Eje 1 | 🔥 Crítica |
| 17 | OTel Collector por dentro: receivers → processors → exporters, agente vs. gateway | Eje 2, rúbrica 1 | 🔥 Crítica |
| 18 | Head-based vs. tail-based sampling, filtrado en el borde | Eje 2, rúbrica 4 | 🔥 Crítica |
| 19 | Incident Command (roles IC / Ops / Comms), severidades, post-mortem blameless | Eje 4 | 🔥 Crítica |
| 20 | Semantic conventions de OTel + grafo de topología + IA causal vs. correlación (AIOps) | Eje 3, rúbrica 5 | Alta |
| 21 | MCP aplicado a observabilidad (servidor MCP que expone métricas/trazas a un agente de RCA) | Eje 3 | Alta |
| 22 | Diagramas C4 (Context, Container, Component, Code) | Formato | Alta |
| 23 | PII masking en el Collector (norma SFC), Log-to-Metrics | Rúbrica 3 y 4 | Media (solo si es Tech Lead) |
| 24 | Dual-shipping y Trace Context W3C/B3 hacia legacy (AS400) | Rúbrica 1 | Media (solo si es Tech Lead) |
| 25 | Toil, on-call, Runbook as Code, chaos engineering | Rúbrica 7 | Media (solo si es Tech Lead) |
| 26 | InnerSource y bots de actualización (Renovate/Dependabot) | Rúbrica 3 | Baja |

## Lectura

- La base de plataforma (Kubernetes, CI/CD, seguridad, Platform Engineering) ya es defendible.
- El hueco es **SRE como disciplina** (14, 15, 16, 19): no existe en el roadmap.
- Observabilidad pasó de "no visto" a 🟡, pero solo como consumidor: falta el lado de **construir** la
  telemetría (17, 18).
- DORA (#13) está 🔴 y conecta directo con el caso: conviene cerrarlo junto con SLOs.

## Plan hasta el lunes 12 de octubre

Ver [roadmap-express.md](roadmap-express.md) (plan por días) y [banco-preguntas.md](banco-preguntas.md).
