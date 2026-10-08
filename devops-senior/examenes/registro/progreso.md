# Nivel de dominio por tema — organizado por Fase

Esto **no es** "visto / no visto" a nivel binario de tema — es qué tan
sólido estás en cada tema **hoy**, medido por cómo respondiste la última
vez que se puso a prueba (examen, repaso espaciado, o una entrevista real).
Sube o baja con el tiempo; nunca queda fijo en 100% solo porque se explicó
una vez.

> **Nota sobre numeración de fases (2026-10-07):** el roadmap se
> reestructuró para fusionar DevOps + IA en un solo camino (Fases 0-6,
> bloques Ops/IA combinados, temas renumerados 14-23 — ver
> `../../00-diagnostico/roadmap.md`, sección "Tablero de avance" para el
> mapeo actualizado y autoritativo). Las fases numeradas 1-10 de **este**
> archivo son las del esquema **anterior** (solo-DevOps) — se conservan tal
> cual porque el detalle de cada corrección sigue siendo válido, pero para
> saber en qué Fase/tema del roadmap actual cae cada cosa, guiate por el
> tablero del roadmap, no por los números de acá abajo.

## Escala

| Nivel | Qué significa | Valor para % dominado |
|---|---|---|
| ⬜ **No visto** | Nunca se tocó en este plan todavía | 0% |
| 🔴 **Novato** | Recién visto, no se puso a prueba todavía | 0% |
| 🟡 **Intermedio** | Repasado, quedan dudas puntuales o no se testeó a fondo | 50% |
| 🟢 **Sólido** | Defendible en una entrevista real, sin ayuda | 85% |
| 🔵 **Senior** | Lo puede explicar con matices/trade-offs, enseñarlo, sin dudar | 100% |

**% Visto** de una fase = temas tocados (cualquier nivel, incluido ⬜ no
cuenta) ÷ total de temas de esa fase. **% Dominado** = promedio del valor
de la tabla de arriba entre todos los temas de la fase (⬜/🔴 = 0%).

## Resumen por fase

| Fase | Tema | % Visto | % Dominado | Estado |
|---|---|---|---|---|
| 0 | Diagnóstico general | — | — | ✅ Hecho |
| 1 | Kubernetes — arquitectura y fundamentos | 100% | 68% | ✅ Cubierta |
| 2 | IaC multi-cloud (+ Ansible agregado) | 89% | 52% | ✅ Cubierta, con huecos (Bicep/CFN) |
| ↳ | *Interrupción: Claude Certified Architect (CCA-F)* | 100% | 72% | 🟡 Falta repaso mixto; recall de la lista de 5 áreas falló 0/5 |
| 3 | CI/CD y GitOps | 100% | 46% | ✅ Cubierta, GitLab CI por autoestudio sin verificar |
| 4 | Identidad | 100% | 68% | ✅ Cubierta |
| ↳ | *Interrupción: entrevista GitLab Admin / Service Accounts (tema 24)* | 100% | 52% | 🟡 Lecciones 1-24 hechas; faltan lección 25, recall del plan y examen de 50 preguntas |
| ↳ | *Interrupción: Ruta IA/MLOps (fundamentos)* | 100% | 72% | 🟡 Nivel técnico sin empezar |
| 5 | Networking avanzado y seguridad | 100% | 73% | ✅ Cubierta |
| 6 | Datos y secretos | 100% | 76% | ✅ Cubierta |
| 7 | Observabilidad y async/orquestación | 100% | 73% | ✅ Cubierta |
| 8 | Kubernetes — troubleshooting | 100% | 100% | ✅ Cubierta |
| 9 | Arquitectura de plataforma (capstone) | 100% | 55% | ✅ Cubierta, con hueco real en métricas DORA (repaso estricto dio 0/4) |
| 10 | Certificación y entrevista final | 0% | 0% | ⬜ Sin empezar |

**Promedio del plan completo (Fases 1-10, peso igual por fase): ~89% visto,
~60% dominado.** Son dos números distintos a propósito — "visto" mide
cobertura del temario completo, "dominado" mide qué tan defendible es lo
que ya se tocó. Las dos interrupciones (CCA-F, IA/MLOps) corren en paralelo
y no cuentan en este promedio de las 10 fases numeradas.

---

## Fase 1 — Kubernetes: arquitectura y fundamentos

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 1 | Arquitectura (control plane, nodos, reconciliation loop) | 🟢 Sólido | 2026-09-14/15, sesión guiada completa |
| 2 | Scheduling/recursos (QoS, HPA/VPA, RBAC de K8s) | 🟡 Intermedio | Tocado vía `Pending`, sin examen dedicado |
| 3 | Networking (Services, Headless, NetworkPolicy, Istio, kube-proxy) | 🟢 Sólido | 2026-09-16/17, varias correcciones bien asimiladas |
| 4 | Operators/CRDs — concepto general | 🟡 Intermedio | Mencionado, no testeado a fondo |
| 5 | Distribuciones de Kubernetes (AKS/EKS/GKE/OpenShift/k3s) | 🟢 Sólido | Diste la respuesta correcta en inglés sin ayuda |
| 6 | Proxies (NGINX/HAProxy/Envoy) e Ingress | 🟡 Intermedio | Explicado a fondo, sin repaso |

## Fase 2 — IaC multi-cloud (+ Ansible agregado)

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 7 | Terraform — State file, locking, drift, import | 🟢 Sólido | 2026-09-24/25, buenas respuestas propias antes de la corrección |
| 8 | Terraform — Backends multi-cloud (S3/Blob/GCS) | 🟢 Sólido | Explicaste vos mismo el mecanismo de DynamoDB |
| 9 | Terraform — Buenas prácticas y ecosistema (Terragrunt, tflint, Terratest, Atlantis, Infracost) | 🟡 Intermedio | Recién explicado en profundidad, sin repaso |
| 10 | Bicep / CloudFormation / CDK | ⬜ No visto | Nunca se tocó — hueco real del roadmap |
| 11 | Contenedores serverless (Container Apps/Fargate/Cloud Run) | 🟡 Intermedio | Visto como parte de la curva de cómputo, sin examen dedicado |
| 12 | Ansible — Fundamentos (vs. Terraform, vs. Docker) | 🟡 Intermedio | 2026-09-29, corrigió solo tras un par de confusiones puntuales |
| 13 | Ansible — Arquitectura agentless (Inventory, Playbook, Módulos) | 🟡 Intermedio | 2026-09-29, buenas respuestas propias |
| 14 | Ansible — Idempotencia (`ok` vs. `changed`) y Handlers | 🟡 Intermedio | 2026-09-29, confundió `ok` inicialmente, corregido |
| 15 | Ansible — Roles, variables (`defaults`/`vars`), plantillas Jinja2 | 🟡 Intermedio | 2026-09-29, respuestas correctas sin ayuda |

### ↳ Interrupción: Claude Certified Architect (CCA-F)

| # | Área del examen (peso) | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 16 | Arquitectura y Orquestación Agéntica (27%) | 🟢 Sólido | Loop ReAct, señal de terminación, 4 razones de sub-agentes — corrección menor |
| 17 | Configuración y Workflows de Claude Code (20%) | 🟢 Sólido | PreToolUse vs. Stop hooks, alcance de `CLAUDE.md`, sin ayuda |
| 18 | Diseño de Tools e Integración MCP (18%) | 🟡 Intermedio | Varias rondas de aclaración sobre mecánica cliente/servidor y determinismo |
| 19 | Prompt Engineering y Structured Output (20%) | 🟡 Intermedio | Intuición correcta, necesitó ejemplo completo de *forced tool use* |
| 20 | Gestión de Contexto y Confiabilidad (15%) | 🟢 Sólido | Sub-agentes, idempotencia/"check-before-act" sin ayuda |

**Pendiente**: repaso mixto (preguntas encadenadas de las 5 áreas sin avisar
el tema) antes de considerar rendir el examen real.

**Repaso estricto de la lista de las 5 áreas (2026-10-07):** 0/5 exactos,
3 parciales (tocó la idea sin el nombre completo: "los mcps" → área 18;
"agentes y herramientas" → mezcla vaga de áreas 16 y 18; "Harness"/"hooks"
→ subtemas del área 17, no el nombre), 1 inventado ajeno al examen
("reinforcement learning vs. fine-tuning", de la ruta IA/MLOps), ningún
peso % correcto, y faltaron completas las áreas 19 y 20. Importante: esto
es un hueco de **recordar la lista como lista**, no de mecanismo — cada
área individual (16-20 arriba) ya se evaluó por separado con buen nivel.
Pendiente de reintento.

## Fase 3 — CI/CD y GitOps

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 21 | CI/CD tradicional (push, pipelines build/test/deploy) | 🟢 Sólido | Experiencia real previa (Jenkins/Azure Pipelines) |
| 22 | GitOps — modelo pull, dónde vive ArgoCD, ventana de despliegue | 🟡 Intermedio | 2026-09-30, corrigió solo tras confusión sobre ubicación de ArgoCD |
| 23 | OIDC (autenticación sin secretos fijos) | 🟡 Intermedio | 2026-09-30, necesitó precisión del mecanismo de dos pasos |
| 24 | GitLab CI | 🔴 Novato | 2026-10-05, el usuario reporta autoestudio fuera de esta sesión ("lo avancé rápido"), pero no se confirmó profundidad — pendiente de verificar con preguntas antes de subir el nivel |

**Pendiente**: configuración práctica de ArgoCD (instalación, `Application`/
`AppProject`, sync policies) — pospuesto a pedido propio.

## Fase 4 — Identidad

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 25 | Managed Identity / IAM Role / Service Account (equivalencias) | 🟡 Intermedio | 2026-10-01/02, corrigió el eje real (ciclo de vida/compartibilidad) |
| 26 | Keycloak (Realm, Client, SSO, User Federation) | 🟡 Intermedio | 2026-10-01, tema nuevo desde cero |
| 27 | Federación OIDC Kubernetes↔AWS IAM (IRSA) | 🟢 Sólido | 2026-10-04, cerró la síntesis completa de los 5 pasos sin ayuda |
| 28 | RBAC — scope jerárquico en Azure y herencia | 🟢 Sólido | 2026-10-04, respondió bien sin ayuda |

### ↳ Interrupción: Ruta IA / MLOps — fundamentos

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 29 | Entrenamiento vs. inferencia (pesos/parámetros) | 🟡 Intermedio | 2026-10-03, corrigió inferencia tras una confusión |
| 30 | LLM (*Large Language Model*) — qué es | 🟢 Sólido | 2026-10-03, descripción correcta sin ayuda |
| 31 | Pre-entrenamiento vs. fine-tuning | 🟡 Intermedio | 2026-10-03, tema nuevo, quedó claro con la explicación |
| 32 | RAG y "agentic RAG" | 🟢 Sólido | 2026-10-03, identificó RAG sin ayuda y aportó la variante agéntica |
| 33 | Embeddings y búsqueda semántica | 🟢 Sólido | 2026-10-03, explicó correctamente sin ayuda |
| 34 | Visión por computador (Image Classification, Object Detection, transfer learning) | 🟢 Sólido | 2026-10-03/04, caso real propio (clasificador de flores) |
| 35 | NLP (Sentiment Analysis, NER, pre-built vs. propio vs. prompting) | 🟢 Sólido | 2026-10-04, razonamiento correcto sin ayuda |
| 36 | Principios de IA Responsable (6 pilares) | 🔴 Novato | 2026-10-04, no los recordaba de memoria, aplicó bien una vez definidos. **Repaso estricto 2026-10-07: 0/6, no arriesgó ningún intento esta vez** — segunda falla del mismo recall, prioridad real para el próximo repaso |

**Meta de certificación confirmada**: AWS Certified AI Practitioner (motivo
comercial) + CCA-F en paralelo. **Nivel técnico** (AI-102/AWS ML Engineer
Associate/GCP ML Engineer) — ⬜ sin empezar.

## Fase 5 — Networking avanzado y seguridad

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 37 | VNet/VPC, modelo de 3 capas, NSG | 🟢 Sólido | 2026-09-16/17, con diagrama de apoyo |
| 38 | Private Endpoint / PrivateLink / Private Service Connect (equivalencias multi-cloud) | 🟢 Sólido | 2026-10-05, reconoció el nombre vía selección múltiple |
| 39 | NAT Gateway, WAF, Firewall centralizado; diseño según necesidad (subredes pública/privada, Load Balancer/Ingress vs. NAT Gateway, dirección de tráfico por iniciador) | 🟢 Sólido | 2026-10-07, profundización a pedido propio con caso real (API pública + BD privada); corrigió solo la confusión inicial de creer que el Load Balancer también resuelve la salida; identificó bien que subredes distintas pueden convivir en la misma VPC/VNet y razonó correctamente la regla de "quién inicia la conexión" para el tráfico de respuesta a un GET |
| 40 | AWS Load Balancers (ALB/NLB/GWLB) | 🟡 Intermedio | Repasado tras fallarlo en entrevista real (EY) |
| 41 | Shift-left security, Trivy (escaneo de imágenes/CVEs) | 🟡 Intermedio | 2026-10-05, funcionamiento bien explicado; **nombre débil** (dijo "Stribi") — prioridad de repaso |
| 42 | OPA/Gatekeeper (policy-as-code) | 🟢 Sólido | 2026-10-05, no recordó el nombre a la primera, lo reconoció bien tras la descripción |

**Nota**: la frase de cierre del roadmap ("app a BD sin exponer secretos")
se termina de cerrar en la Fase 6 (Key Vault/Secrets Manager).

## Fase 6 — Datos y secretos ✅ completa (2026-10-05)

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 43 | Replicación vs. sharding de bases de datos (teoría general) | 🟡 Intermedio | Explicado, sin repaso |
| 44 | Key Vault / Secrets Manager / Secret Manager (+ integración con Managed Identity/IAM Role) | 🟢 Sólido | 2026-10-05, cerró sin ayuda la síntesis completa: Managed Identity/IAM Role → lee Key Vault/Secrets Manager → conecta a la BD por Private Endpoint/PrivateLink |
| 45 | Cosmos DB / DynamoDB / Firestore — niveles de consistencia (fuerte vs. eventual) | 🟢 Sólido | 2026-10-05, respondió bien sin ayuda; cierra el hueco marcado desde el diagnóstico inicial (2026-09-08) |
| 46 | AlloyDB / RDS / Cloud SQL (relacional administrada) | 🟢 Sólido | 2026-10-05, identificó bien la ventaja de gestión reducida (parches/backups/HA) sin ayuda |

## Fase 7 — Observabilidad y async/orquestación ✅ completa (2026-10-06)

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 47 | Observabilidad — OpenTelemetry (métricas/logs/traces), traces vs. alertas | 🟡 Intermedio | 2026-10-06, buena experiencia real previa en consumo (Grafana/Datadog), pero nunca configuró la instrumentación; confundió inicialmente alertas con traces, corregido con el ejemplo de los 5 microservicios |
| 48 | Orquestación serverless — Durable Functions (`orchestrator` replay, `activity` con ejecución única vía historial) | 🟢 Sólido | 2026-10-06, cierra el hueco del diagnóstico inicial (2026-09-08); corrigió solo tras una confusión de fraseo ("no tienen idempotencia" → en realidad el framework garantiza ejecución única) |
| 49 | Streaming de eventos — Kafka/Redpanda (log retenido, multi-consumidor, replay) vs. cola tradicional (SQS) | 🟢 Sólido | 2026-10-06, buena base real con SQS; identificó sin ayuda la ventaja de múltiples consumidores independientes. **Profundización 2026-10-07** (a pedido propio): caso de 3 consumidores de un mismo evento, retention configurable en Kafka/Redpanda, y patrón Transactional Outbox (RDS/S3 + SNS+SQS) como alternativa real sin Kafka — conectó correctamente su propia experiencia previa (RDS+SNS+SQS) con la teoría; corrigió solo un matiz (creer que Kafka "garantiza la transacción" en vez de durabilidad+replay) y una idea equivocada sobre la escalabilidad de Kafka (es al revés: escala mejor, no peor) |

## Fase 8 — Kubernetes: troubleshooting ✅ completa (2026-10-06)

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 50 | Troubleshooting — `CrashLoopBackOff`, `OOMKilled` (vs. `Evicted` a nivel de nodo, terminación graceful `SIGTERM`/143, preemption), `ImagePullBackOff` | 🔵 Senior | 2026-10-06/07, sesión dedicada completa. Distinguió sin ayuda `OOMKilled` (límite del contenedor) de `Evicted` (presión del nodo completo) — matiz que muchos confunden |

## Fase 9 — Arquitectura de plataforma (capstone)

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 51 | Platform Engineering — IDP, golden path, Backstage, Team Topologies/carga cognitiva, multi-tenancy en K8s (Namespace/RBAC/NetworkPolicy/ResourceQuota) | 🟢 Sólido | 2026-10-07, buena síntesis propia (sobreventa de recursos con plan de contingencia, no enseñado explícitamente); corrigió solo un lapsus puntual (pensó que los Pods NO se ven entre sí por defecto — se re-confirmó que la red es plana/abierta) |
| 51b | Métricas DORA (4 métricas: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service) | 🔴 Novato | 2026-10-07, repaso estricto dio **0/4** — no recordaba ni siquiera que el tema era DORA. Re-explicado desde cero el mismo día; separado como sub-tema propio por el tamaño real de la brecha; pendiente de reintento |
| 52 | Arquitectura/costos multi-cloud (Well-Architected, FinOps) | 🟡 Intermedio | 2026-10-07, FinOps (visibilidad de costos cruzando equipos, negociación de descuentos por volumen) respondido bien sin ayuda. **Lista de los 6 pilares de Well-Architected — repaso estricto #1 (2026-10-07): 2/6 correctos, 1 parcial, 1 inventado ("Simplicity"), 3 ausentes.** **Repaso estricto #2 (2026-10-07, mismo día): 3/6 correctos (Reliability, Security, Sustainability), 1 parcial ("cost eficiente" por Cost Optimization), 0 inventados, 2 ausentes (Operational Excellence, Performance Efficiency) — mejora real, sigue sin ser 6/6, reintentar más adelante** |
| 53 | Python/FastAPI/Docker — hardening: BOLA (OWASP API #1, autorización a nivel de objeto) y contenedor sin privilegios de root | 🟢 Sólido | 2026-10-07, distinguió sin ayuda que un contenedor non-root no previene BOLA (error de lógica de app), solo limita el daño si el atacante escala más allá — con ejemplo propio (modificar un feature flag) |
| 54 | Arquitectura completa propia (diagrama frontend+backend construido en sesión) | 🟡 Intermedio | Construida junto con vos, no evaluada de forma independiente |

## ↳ Interrupción: Prueba técnica Davivienda — SRE y observabilidad (8–12 oct. 2026)

Ver `../../temas/24-davivienda-sre-observabilidad/roadmap-express.md` (detalle y meta por ítem) y
`banco-preguntas.md` (preguntas). Niveles al arrancar:

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 55 | SLI/SLO/SLA, Golden Signals, RED/USE | ⬜ No visto | — |
| 56 | Error Budget y matemáticas de disponibilidad | ⬜ No visto | — |
| 57 | Alertas por burn rate (multi-window, multi-burn-rate) | ⬜ No visto | — |
| 58 | Error Budget Policy, Quality Gate en CI/CD, progressive delivery (Argo Rollouts/Flagger) | ⬜ No visto | — |
| 59 | OpenTelemetry Collector por dentro (receivers/processors/exporters/connectors) | ⬜ No visto | — |
| 60 | Collector agente vs. gateway, dos capas, multi-cloud | ⬜ No visto | — |
| 61 | Head-based vs. tail-based sampling | ⬜ No visto | — |
| 62 | Propagación de contexto (W3C `traceparent`, B3, span links en Kafka/MQ) | 🟡 Intermedio | Base de Kafka (#49), sin la parte de trazas |
| 63 | FinOps de telemetría (cardinalidad, Log-to-Metrics, retención) | ⬜ No visto | — |
| 64 | Enmascaramiento de PII en el Collector (SFC, Ley 1581, PCI DSS) | ⬜ No visto | — |
| 65 | Semantic Conventions, exemplars, service graph | ⬜ No visto | — |
| 66 | AIOps, correlación vs. causalidad, MCP aplicado a observabilidad | 🟡 Intermedio | MCP por el CCA-F (#18) |
| 67 | (Opcional) Teoría de grafos para RCA | ⬜ No visto | — |
| 68 | Incident Command, mitigación, post-mortem blameless | ⬜ No visto | — |
| 69 | Toil, on-call, Runbook as Code, chaos engineering | ⬜ No visto | — |
| 70 | Temas aledaños: idempotencia, backoff + jitter, RTO/RPO, percentiles, Ley de Little | ⬜ No visto | — |
| 71 | Modelo C4 y presentación | ⬜ No visto | — |

## Fase 10 — Certificación y entrevista final

Sin empezar — depende de cerrar las fases anteriores primero.

## Interrupción — GitLab Admin / migración a Service Accounts (tema 24, entrevista)

Lecciones de `../../temas/24-gitlab-admin-service-accounts/lecciones.md`
(nota por lección ahí mismo). Promedio de las lecciones 1-24: **7.7/10**;
repasos que mezclan varias lecciones: **5.5/10** (sabe las piezas, le cuesta
conectarlas sin ayuda).

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 55 | Identidades para automatización (PAT personal, bot manual, Group/Project Access Token, `CI_JOB_TOKEN`, Service Account) y R-P-L-A | 🟡 Intermedio | 2026-10-05, buena regla propia ("Service Account para lo externo a GitLab, `CI_JOB_TOKEN` para lo interno"); repaso mixto 6/10 (asumió que un script corre en CI sin preguntar dónde corre) |
| 56 | Service Accounts — nivel instancia vs. grupo ("AI y GO": Admin → Instancia, Grupo → Owner) | 🟡 Intermedio | 2026-10-05, falló dos veces (3/10 y 5/10: creía que el Admin no puede crear las de grupo); en el repaso respondió bien sin ayuda que el Admin de self-managed puede crear ambas |
| 57 | API: roles numéricos (10/20/30/40/50), scopes, membresía, los 3 pasos (Contratar → Abrir puertas → Entregar llave) | 🟡 Intermedio | 2026-10-05, roles y scopes 10/10 (Reporter + `read_registry`); al escribir la URL mezcló las 3 llamadas en una y usó `/groups/77` para un proyecto |
| 58 | Expiración de tokens (GitLab 16.0) y rotación automática (`/rotate`, Vault, alertas propias) | 🟡 Intermedio | 2026-10-05/08, propuso bien la rotación automática; olvidó el riesgo de vencimiento masivo el mismo día y que la Service Account no lee correos |
| 59 | Plan de migración en 5 fases (Inventario → Diseño → Piloto → Olas → Gobierno) | 🟡 Intermedio | 2026-10-08, piloto 10/10 y periodo de gracia 9/10 por separado, pero el plan completo dio 5/10 (propuso una Service Account por segmento, olvidó el piloto) y el segundo intento fue mirando la tabla. 🔁 Pendiente: recall sin ayuda |
| 60 | Administración self-managed: `gitlab.rb` + `gitlab-ctl reconfigure`, backups y `gitlab-secrets.json`, logs (`api_json.log`, `audit_json.log`) | 🟢 Sólido | 2026-10-08, 9/10, 8/10 y 10/10 sin ayuda |
| 61 | Arquitectura de GitLab (NGINX, Workhorse, Puma, Sidekiq, Gitaly, PostgreSQL, Redis) y diagnóstico por denominador común | 🟡 Intermedio | 2026-10-08, dudó entre Workhorse y Gitaly (5/10); se enseñó la técnica de descartar lo que sí funciona |
| 62 | Upgrades (paradas obligatorias, background migrations), LDAP/SAML/SCIM, tokens de runners (`glrt-`) | 🟢 Sólido | 2026-10-08, 8/10 en los tres; buena frase propia: "migración controlada en vez de migración de emergencia" |
| 63 | Migración entre instancias con Direct Transfer (Service Accounts y tokens no migran) | 🔴 Novato | Enseñado el 2026-10-08, pregunta de la lección 25 sin responder |

---

**Cómo se actualiza**: cada vez que se hace un repaso espaciado o un examen
de práctica, se revisa este archivo — un tema sube de nivel si lo
respondiste bien **sin ayuda**, se mantiene si tuviste que pensarlo mucho, y
puede bajar si quedó claro que se te olvidó. Pendiente de definir la
frecuencia del repaso espaciado con el usuario (ver `resultados.md`).
