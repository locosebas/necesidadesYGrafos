# Nivel de dominio por tema

Esto **no es** "visto / no visto" — es qué tan sólido estás en cada tema
**hoy**, medido por cómo respondiste la última vez que se puso a prueba
(examen, repaso espaciado, o una entrevista real). Sube o baja con el
tiempo; nunca queda fijo en 100% solo porque se explicó una vez.

## Escala

| Nivel | Qué significa |
|---|---|
| 🔴 **Novato** | Recién visto, no se puso a prueba todavía |
| 🟡 **Intermedio** | Repasado, quedan dudas puntuales o no se testeó a fondo |
| 🟢 **Sólido** | Defendible en una entrevista real, sin ayuda |
| 🔵 **Senior** | Lo puede explicar con matices/trade-offs, enseñarlo, sin dudar |

## Kubernetes

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Arquitectura (control plane, nodos, reconciliation loop) | 🟢 Sólido | 2026-09-14/15, sesión guiada completa |
| Scheduling/recursos (QoS, HPA/VPA, RBAC de K8s) | 🟡 Intermedio | Tocado vía `Pending`, sin examen dedicado |
| Networking (Services, Headless, NetworkPolicy, Istio, kube-proxy) | 🟢 Sólido | 2026-09-16/17, varias correcciones bien asimiladas |
| Troubleshooting (`CrashLoopBackOff`, `Pending`, `OOMKilled`) | 🟡 Intermedio | Repasado vía preguntas reales de entrevista, falta sesión dedicada (Fase 8) |
| Operators/CRDs, AKS vs EKS vs GKE | 🟡 Intermedio | Mencionado, no testeado a fondo |

## Redes

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| VNet/VPC, modelo de 3 capas, NSG | 🟢 Sólido | 2026-09-16/17, con diagrama de apoyo |
| Private Endpoint / Private DNS Zone | 🟢 Sólido | Corregiste vos mismo el error de ubicación tras la explicación |
| NAT Gateway, WAF, Firewall centralizado | 🟡 Intermedio | Recién explicado, sin repaso |
| AWS Load Balancers (ALB/NLB/GWLB) | 🟡 Intermedio | Repasado tras fallarlo en entrevista real (EY) |
| Private Endpoint — equivalencias multi-cloud (Azure Private Endpoint / AWS PrivateLink / GCP Private Service Connect) | 🟢 Sólido | 2026-10-05, reconoció el nombre correcto vía selección múltiple tras describir bien el funcionamiento; identificó solo que "Private Endpoint" es específico de Azure |

## Seguridad / DevSecOps

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Shift-left security, Trivy (escaneo de imágenes/CVEs) | 🟡 Intermedio | 2026-10-05, describió bien el funcionamiento sin ayuda; no recordó el nombre exacto (dijo "Stribi") — prioridad de repaso de NOMBRE |
| OPA/Gatekeeper (policy-as-code) | 🟢 Sólido | 2026-10-05, no recordó el nombre a la primera, pero tras la descripción completa lo reconoció correctamente |

**Fase 5 completa (2026-10-05)** dentro de lo que le corresponde — la frase
de cierre completa del roadmap ("app a BD sin exponer secretos") se termina
de cerrar en la Fase 6 (Key Vault/Secrets Manager).

## Terraform

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| State file, locking, drift, import | 🟢 Sólido | 2026-09-24/25, buenas respuestas propias antes de la corrección |
| Backends multi-cloud (S3/Blob/GCS) | 🟢 Sólido | Explicaste vos mismo el mecanismo de DynamoDB |
| Buenas prácticas y ecosistema (Terragrunt, tflint, Terratest, Atlantis, Infracost) | 🟡 Intermedio | Recién explicado en profundidad, sin repaso |

## Ansible

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Fundamentos (gestión de configuración vs. provisioning de Terraform, vs. Docker) | 🟡 Intermedio | 2026-09-29, sesión guiada desde cero; corrigió solo tras un par de confusiones puntuales (Docker vs. Ansible, "Terraform no depende de estado") |
| Arquitectura agentless (nodo de control, Inventory, Playbook, Módulos) | 🟡 Intermedio | 2026-09-29, buenas respuestas propias (rol del Inventory para agrupar servidores, capa del sistema operativo) |
| Idempotencia (`ok` vs. `changed`) y Handlers | 🟡 Intermedio | 2026-09-29, confundió inicialmente `ok` con "se ejecutó la acción", quedó claro tras la corrección |
| Roles, variables (`defaults`/`vars`) y plantillas Jinja2 | 🟡 Intermedio | 2026-09-29, respuestas correctas sin ayuda (variable en vez de hardcodear, `template` vs. `copy`) |

## CI/CD y GitOps

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| CI/CD tradicional (push, pipelines de build/test/deploy) | 🟢 Sólido | Experiencia real previa (Jenkins/Azure Pipelines), buena descripción propia con correcciones menores de orden |
| GitOps — modelo pull, dónde vive ArgoCD, ventana de despliegue | 🟡 Intermedio | 2026-09-30, corrigió solo tras una confusión sobre la ubicación de ArgoCD; identificó bien solo dónde cabe la aprobación manual (merge a main) |
| OIDC (*OpenID Connect*, autenticación sin secretos fijos) | 🟡 Intermedio | 2026-09-30, buena intuición inicial (mínimo privilegio, tiempo corto), necesitó precisión sobre el mecanismo de dos pasos (JWT firmado + credencial temporal) |

**Pendiente de profundizar**: configuración práctica de ArgoCD (instalación, objetos `Application`/`AppProject`, políticas de sincronización) — pospuesto a pedido propio para una sesión futura.

## Identidad

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Managed Identity system-assigned vs. user-assigned (y equivalencias AWS IAM Role / GCP Service Account) | 🟡 Intermedio | 2026-10-01/02, corrigió el eje real (ciclo de vida/compartibilidad, no duración) tras una confusión inicial; identificó bien el trade-off de blast radius en un caso concreto (5 VMs) |
| Keycloak (Realm, Client, SSO, User Federation) | 🟡 Intermedio | 2026-10-01, tema nuevo desde cero; confundió Client único vs. uno por app (corregido con el mismo argumento de blast radius) |
| Federación OIDC Kubernetes↔AWS IAM (IRSA): Identity Provider, trust policy con `Principal`+`Condition` sobre `sub`, ServiceAccount, `AssumeRoleWithWebIdentity` | 🟢 Sólido | 2026-10-04, cerró la síntesis completa de los 5 pasos sin ayuda (incluido qué pasa si se borra el ServiceAccount) |
| RBAC — scope jerárquico en Azure (Management Group→Subscription→Resource Group→Resource) y herencia | 🟢 Sólido | 2026-10-04, respondió bien sin ayuda que la herencia es automática hacia abajo |

**Fase 4 completa (2026-10-04).**

## IA / MLOps — Fundamentos

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Entrenamiento vs. inferencia (pesos/parámetros, red neuronal) | 🟡 Intermedio | 2026-10-03, buena descripción propia del entrenamiento; corrigió inferencia tras una confusión (pensaba que era ajuste manual de pesos) |
| LLM (*Large Language Model*) — qué es | 🟢 Sólido | 2026-10-03, descripción correcta sin ayuda |
| Pre-entrenamiento vs. fine-tuning | 🟡 Intermedio | 2026-10-03, tema nuevo, no sabía qué significaba "pre"; quedó claro con la explicación |
| RAG (*Retrieval-Augmented Generation*) y "agentic RAG" (búsqueda vía tool call) | 🟢 Sólido | 2026-10-03, identificó RAG sin ayuda y agregó por cuenta propia la variante de búsqueda determinística vía tool call, conectándolo correctamente con Tool Design/MCP del CCA-F |
| Embeddings y búsqueda semántica | 🟢 Sólido | 2026-10-03, explicó correctamente y sin ayuda por qué una búsqueda por coincidencia exacta de palabras falla donde un embedding no |
| Visión por computador (Image Classification, Object Detection) | 🟢 Sólido | 2026-10-03/04, experiencia real propia (clasificador de calidad/conteo de pétalos de flores); identificó correctamente que usó **transfer learning vía feature extraction**, no fine-tuning real, tras una duda propia bien fundamentada |
| NLP — Sentiment Analysis, NER, y cuándo usar servicio pre-construido vs. modelo propio vs. prompting a un LLM | 🟢 Sólido | 2026-10-04, razonamiento correcto de costo/tiempo sin ayuda |
| Principios de IA Responsable (Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, Accountability) | 🟡 Intermedio | 2026-10-04, identificó bien Reliability & Safety aplicado a su propio caso (cámaras) una vez se le dieron las definiciones; no los recordaba de memoria |

## Arquitectura / Platform Engineering

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Arquitectura completa (frontend+backend, diagrama grande) | 🟡 Intermedio | Construida junto con vos, no evaluada de forma independiente |
| Compute hierarchy y curva de costos (VM→K8s→serverless→FaaS→PaaS) | 🟡 Intermedio | Explicado con gráfico, sin examen |
| Variante serverless de la arquitectura | 🟡 Intermedio | Explicado, sin repaso |

## Claude Certified Architect (CCA-F) — 2026-09-25 a 09-29

| Área del examen (peso) | Nivel | Última vez puesto a prueba |
|---|---|---|
| Arquitectura y Orquestación Agéntica (27%) | 🟢 Sólido | Explicaste el loop ReAct, la señal de terminación, y 4 razones reales de sub-agentes (contexto, especialización, paralelización, aislamiento) — con una corrección menor en el mecanismo exacto de cierre del loop |
| Configuración y Workflows de Claude Code (20%) | 🟢 Sólido | Razonaste bien PreToolUse vs. Stop hooks, y el alcance de `CLAUDE.md` (global/proyecto/directorio) sin ayuda |
| Diseño de Tools e Integración MCP (18%) | 🟡 Intermedio | Buenas preguntas de seguimiento (infraestructura de un MCP server, prompt/tag injection), pero necesitaste varias rondas de aclaración sobre la mecánica cliente/servidor y el determinismo |
| Prompt Engineering y Structured Output (20%) | 🟡 Intermedio | Intuición correcta sobre "restringir la respuesta", pero el mecanismo exacto de *forced tool use* necesitó un ejemplo completo para asentarse |
| Gestión de Contexto y Confiabilidad (15%) | 🟢 Sólido | Sub-agentes para archivos grandes, y respuesta correcta de "check-before-act"/idempotencia sin ayuda |

## Otros

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Distribuciones de Kubernetes (AKS/EKS/GKE/OpenShift/k3s) | 🟢 Sólido | Diste la respuesta correcta en inglés sin ayuda |
| Proxies (NGINX/HAProxy/Envoy) | 🟡 Intermedio | Explicado a fondo, sin repaso |
| Replicación vs. sharding de bases de datos | 🟡 Intermedio | Explicado, sin repaso |

---

**Cómo se actualiza**: cada vez que se hace un repaso espaciado o un examen
de práctica, se revisa este archivo — un tema sube de nivel si lo
respondiste bien **sin ayuda**, se mantiene si tuviste que pensarlo mucho, y
puede bajar si quedó claro que se te olvidó. Pendiente de definir la
frecuencia del repaso espaciado con el usuario (ver `resultados.md`).
