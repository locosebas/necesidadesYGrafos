# Nivel de dominio por tema — organizado por Fase

Esto **no es** "visto / no visto" a nivel binario de tema — es qué tan
sólido estás en cada tema **hoy**, medido por cómo respondiste la última
vez que se puso a prueba (examen, repaso espaciado, o una entrevista real).
Sube o baja con el tiempo; nunca queda fijo en 100% solo porque se explicó
una vez. Las fases son las de `../../00-diagnostico/roadmap.md`.

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
| ↳ | *Interrupción: Claude Certified Architect (CCA-F)* | 100% | 72% | 🟡 Falta repaso mixto |
| 3 | CI/CD y GitOps | 100% | 46% | ✅ Cubierta, GitLab CI por autoestudio sin verificar |
| 4 | Identidad | 100% | 68% | ✅ Cubierta |
| ↳ | *Interrupción: Ruta IA/MLOps (fundamentos)* | 100% | 72% | 🟡 Nivel técnico sin empezar |
| 5 | Networking avanzado y seguridad | 100% | 68% | ✅ Cubierta |
| 6 | Datos y secretos | 100% | 76% | ✅ Cubierta |
| 7 | Observabilidad y async/orquestación | 0% | 0% | ⬜ Sin empezar |
| 8 | Kubernetes — troubleshooting | 100% | 50% | 🟡 Superficial, falta sesión dedicada |
| 9 | Arquitectura de plataforma (capstone) | 50% | 25% | 🟡 Parcial, ad-hoc |
| 10 | Certificación y entrevista final | 0% | 0% | ⬜ Sin empezar |

**Promedio del plan completo (Fases 1-10, peso igual por fase): ~74% visto,
~45% dominado.** Son dos números distintos a propósito — "visto" mide
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
| 36 | Principios de IA Responsable (6 pilares) | 🟡 Intermedio | 2026-10-04, no los recordaba de memoria, aplicó bien una vez definidos |

**Meta de certificación confirmada**: AWS Certified AI Practitioner (motivo
comercial) + CCA-F en paralelo. **Nivel técnico** (AI-102/AWS ML Engineer
Associate/GCP ML Engineer) — ⬜ sin empezar.

## Fase 5 — Networking avanzado y seguridad

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 37 | VNet/VPC, modelo de 3 capas, NSG | 🟢 Sólido | 2026-09-16/17, con diagrama de apoyo |
| 38 | Private Endpoint / PrivateLink / Private Service Connect (equivalencias multi-cloud) | 🟢 Sólido | 2026-10-05, reconoció el nombre vía selección múltiple |
| 39 | NAT Gateway, WAF, Firewall centralizado | 🟡 Intermedio | Recién explicado, sin repaso |
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

## Fase 7 — Observabilidad y async/orquestación

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 47 | Observabilidad (Azure Monitor/CloudWatch/Cloud Logging, OpenTelemetry) | ⬜ No visto | — |
| 48 | Orquestación serverless (Durable Functions/Step Functions/Workflows, Temporal) | ⬜ No visto | — |
| 49 | Streaming de eventos (Kafka/Redpanda, Event Hubs, Kinesis, Pub/Sub) | ⬜ No visto | — |

## Fase 8 — Kubernetes: troubleshooting

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 50 | Troubleshooting (`CrashLoopBackOff`, `Pending`, `OOMKilled`) | 🟡 Intermedio | Repasado vía preguntas reales de entrevista, falta sesión dedicada |

## Fase 9 — Arquitectura de plataforma (capstone)

| # | Tema | Nivel | Última vez puesto a prueba |
|---|---|---|---|
| 51 | Platform Engineering (Internal Developer Platform, golden paths, Team Topologies) | ⬜ No visto | — |
| 52 | Arquitectura/costos multi-cloud (Well-Architected, FinOps) | 🟡 Intermedio | Compute hierarchy y curva de costos explicados, sin examen |
| 53 | Python/FastAPI — repaso y hardening de APIs | ⬜ No visto | — |
| 54 | Arquitectura completa propia (diagrama frontend+backend construido en sesión) | 🟡 Intermedio | Construida junto con vos, no evaluada de forma independiente |

## Fase 10 — Certificación y entrevista final

Sin empezar — depende de cerrar las fases anteriores primero.

---

**Cómo se actualiza**: cada vez que se hace un repaso espaciado o un examen
de práctica, se revisa este archivo — un tema sube de nivel si lo
respondiste bien **sin ayuda**, se mantiene si tuviste que pensarlo mucho, y
puede bajar si quedó claro que se te olvidó. Pendiente de definir la
frecuencia del repaso espaciado con el usuario (ver `resultados.md`).
