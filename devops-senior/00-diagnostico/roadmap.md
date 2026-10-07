# Roadmap de estudio — DevOps + IA (un solo camino)

Objetivo: ser **experto en DevOps/Platform multi-cloud y en IA** (desarrollo
de aplicaciones con IA + operación de IA en producción, MLOps/LLMOps). No son
dos planes separados: cada fase combina un bloque **Ops** y un bloque **IA**
que se apoyan entre sí (por ejemplo, Kubernetes primero y después servir
modelos con GPU sobre Kubernetes).

Orden sugerido. Cada fase es aprox. 3-4 semanas de estudio part-time
(mientras trabajás). Ajustalo a tu ritmo real — lo importante es no saltar
el examen de autoevaluación al final de cada tema.

## Actualización de objetivo (2026-09-14): de "Senior DevOps" a "Arquitecto de plataforma"

El objetivo dejó de ser solo "cerrar brechas para calificar a una vacante" y
pasó a ser **poder diseñar y construir una self-service developer platform
completa desde cero (0→1)**, como la del posting de Vule Human Talent
(Senior DevOps/Platform Engineer, startup de salud, GKE + Terraform + ArgoCD
+ Istio + GitLab CI + Keycloak + OPA + AlloyDB + OpenTelemetry, sept. 2026).

Esto cambia el orden de estudio en dos puntos concretos:

1. **Kubernetes se adelanta y se abre en capas.** Antes de repasar
   troubleshooting (que ya estaba pendiente), hace falta la **arquitectura**
   del clúster (control plane, nodos, CNI, CSI, cómo se levanta un clúster) —
   sin eso, troubleshooting es memorizar recetas sueltas en vez de entender
   qué componente falló. Ver `temas/10-kubernetes-avanzado/README.md`, que
   ahora es un índice ordenado (arquitectura → scheduling/recursos →
   networking/mesh → operators/managed-k8s → troubleshooting, al final).
2. **Se agrega un tema de cierre: `temas/23-platform-engineering/`** (antes
   numerado `16-platform-engineering`). Saber cada herramienta suelta no
   alcanza para ser arquitecto — hace falta el marco que explica cómo se
   combinan (Internal Developer Platform, golden paths, Team Topologies,
   production readiness) y un diagrama de referencia que ubica cada tema del
   plan dentro de la arquitectura completa del posting.

## Metodología: de general a específico

Objetivo final: llegar a una entrevista técnica (o certificación) y poder
resolver la prueba, no solo "haber leído sobre el tema". Por eso cada nivel
sigue el mismo patrón general → específico:

1. **General (panorama):** examen diagnóstico amplio que toca todos los temas (Ops e IA) a
   nivel conceptual, para medir dónde estás parado hoy en la práctica (no
   solo lo que infiere el CV). Esto define qué temas se profundizan primero.
2. **Específico (por tema):** dentro de cada tema, primero repaso el concepto
   general (qué es, para qué sirve, cómo se relaciona con lo demás) y recién
   después vamos a detalle técnico (sintaxis, configuración, troubleshooting).
3. **Examen del tema:** mezcla teoría + escenario, nivel creciente
   (básico → intermedio → senior) hasta llegar a ≥ 80%.
4. **Repaso mixto/entrevista:** una vez cubiertos varios temas, exámenes que
   combinan temas y simulan formato de entrevista técnica o prueba de
   certificación (preguntas encadenadas, sin decirte de antemano el tema).

## Preferencia pedagógica: repetición de términos

Una de las falencias que identificaste vos mismo: se te olvidan los **términos
y nombres de herramientas**, no los conceptos. Por eso, al enseñar/evaluar,
Claude debe ser **redundante a propósito**: repetir el nombre exacto de cada
término/herramienta varias veces en la misma explicación (en vez de decir
"esto" o "dicho servicio", repetir "Managed Identity", "Managed Identity" de
nuevo), en vez de evitar la repetición por estilo. Es una decisión deliberada
de este plan, no un descuido de redacción — no "corregir" esto a un estilo
más variado en el futuro.

## Preferencia pedagógica: interacción de a poco (problemas de atención)

El usuario también avisó que tiene problemas de atención. Consecuencia
práctica: **nunca tirar una lista larga de preguntas juntas** (por ejemplo,
un examen de 13 preguntas de una sola vez). Las sesiones de examen/enseñanza
deben ser de ida y vuelta — **una pregunta por vez** (excepcionalmente dos si
son muy cortas), esperar la respuesta, corregir/explicar esa respuesta
puntual, y recién ahí pasar a la siguiente. Nada de monólogos largos ni de
tandas de preguntas en batch. Esto aplica a exámenes, explicaciones de temas,
y cualquier interacción de enseñanza en este plan.

## Preferencia pedagógica: siglas siempre con su significado al lado (2026-09-16)

El usuario pidió explícitamente que, cada vez que aparezca una sigla (VNet,
NSG, ACA, FaaS, CNI, etc.), se escriba **al lado** su nombre completo (en
inglés y, si ayuda, su traducción) — no asumir que ya la recuerda solo
porque se explicó una vez antes en la sesión. Es la misma lógica que la
preferencia de "repetición de términos" de arriba, pero aplicada
específicamente a siglas: "**NSG (Network Security Group)**", nunca solo
"NSG" a secas la primera vez que se la nombra en una explicación.

Más preferencias pedagógicas (nombres, selección múltiple, lista numerada
calificada) están documentadas en `/CLAUDE.md`, que aplica siempre que se
trabaje en este repo.

## Pista paralela: Claude Certified Architect (CCA-F)

No es parte de la grilla Ops/IA de abajo — es una certificación de
**Anthropic**, no de una nube, sobre arquitectura de sistemas con IA agéntica
(MCP, Claude Code, gestión de contexto). Corre **en paralelo** a las fases
numeradas, sin ocupar un número de fase propio.

- **Qué certifica**: Claude Certified Architect — Foundations (**CCA-F**).
  Examen proctoreado, 60 preguntas, Pearson VUE. Detalle completo (temario,
  pesos, precio, links) en `certificaciones/README.md`.
- **Estado (2026-10-04)**: ✅ primera pasada completa por las 5 áreas del
  examen — ver `examenes/registro/`. 🔁 **Pendiente**: repaso mixto
  (preguntas encadenadas de las 5 áreas sin avisar el tema) antes de
  considerar rendir el examen real.

## Tablero de avance (mirá acá cómo vas)

Estados: ⬜ sin empezar · 🟡 parcial/tocado, sin examen a fondo · ✅ completo
(ver `examenes/registro/progreso.md` para el nivel exacto por sub-tema) · 🔁
hueco puntual pendiente dentro de un tema ya mayormente cubierto. Se
actualiza cada vez que avanza una sesión de estudio (ver
`../examenes/registro/resultados.md` para el detalle).

| Fase | Bloque | Tema | Estado |
|---|---|---|---|
| 0 | Ops | Diagnóstico general DevOps (temas 01-12) | ✅ hecho 2026-09-08 |
| 0 | IA | Diagnóstico general IA (temas 14-20) | ⬜ — los fundamentos se cubrieron enseñando directo, sin el examen diagnóstico formal |
| 0 | Ops | Diagnóstico de herramientas startup (Istio, ArgoCD, Keycloak, OPA, ESO, Valkey, Redpanda, Temporal…) | ⬜ |
| 1 | Ops | 01 — IaC multi-cloud | ✅ Terraform + Ansible (agregado fuera del roadmap original); 🔁 Bicep/CloudFormation/CDK nunca visto |
| 1 | Ops | 10 — Kubernetes avanzado | ✅ completo, incluido troubleshooting (`CrashLoopBackOff`/`OOMKilled`/`ImagePullBackOff`, nivel 🔵 Senior) |
| 1 | Ops | 02 — Contenedores serverless | 🟡 tocado vía la curva de cómputo (VM→K8s→serverless→FaaS→PaaS), sin examen dedicado |
| 1 | IA | 14 — Fundamentos de IA, ML y LLMs | ✅ entrenamiento/inferencia, pre-entrenamiento/fine-tuning, RAG/agentic RAG, embeddings, visión por computador, NLP, IA Responsable |
| 2 | Ops | 03 — CI/CD multi-cloud | ✅ panorama (push vs. pull, ArgoCD, OIDC); 🔁 configuración práctica de ArgoCD pendiente; GitLab CI por autoestudio propio, sin verificar profundidad |
| 2 | Ops | 08 — Python / FastAPI + Docker | ✅ hardening: BOLA y contenedor sin privilegios de root |
| 2 | IA | 15 — Desarrollo de apps con LLMs | ⬜ |
| 3 | Ops | 04 — Identidad e IAM | ✅ Managed Identity/IAM Role/Service Account, Keycloak, federación OIDC K8s↔AWS IAM (IRSA), RBAC scope/herencia |
| 3 | Ops | 05 — Networking multi-cloud | ✅ VNet/VPC, Private Endpoint/PrivateLink/Private Service Connect |
| 3 | Ops | 11 — Seguridad / DevSecOps | ✅ shift-left, Trivy (nombre débil, ver registro), OPA/Gatekeeper |
| 3 | IA | 20 — Seguridad y gobernanza de IA | ⬜ |
| 4 | Ops | 06 — Datos y secretos | ✅ Key Vault/Secrets Manager + Managed Identity, consistencia NoSQL, relacional administrada (AlloyDB/RDS/Cloud SQL) |
| 4 | IA | 16 — RAG y bases vectoriales | 🟡 RAG/agentic RAG/embeddings y búsqueda semántica ✅ (conceptual, ver tema 14); bases vectoriales hands-on (pgvector, AI Search, etc.) sin ver |
| 4 | Ops | 09 — Orquestación serverless | ✅ Durable Functions (`orchestrator` replay, `activity` con ejecución única vía historial) |
| 4 | Ops | 21 — Event streaming y workflows durables (Redpanda, Temporal) | 🟡 Kafka/Redpanda vs. SQS (log retenido, multi-consumidor, replay) ✅ conceptual; hands-on de Redpanda/Temporal sin ver — **profundización pendiente a pedido propio** |
| 4 | IA | 17 — Agentes de IA y MCP | ⬜ como tema IA general — pero **MCP sí está cubierto a fondo** dentro de la pista paralela del CCA-F |
| 5 | Ops | 07 — Observabilidad multi-cloud | ✅ OpenTelemetry (métricas/logs/traces), traces vs. alertas |
| 5 | IA | 18 — MLOps y LLMOps | ⬜ |
| 5 | IA | 19 — Serving de modelos y GPUs | ⬜ |
| 5 | Ops | 12 — Arquitectura y costos multi-cloud | 🟡 Well-Architected Framework (6 pilares), FinOps; repaso estricto de los 6 pilares falló (2/6) — 🔁 pendiente de reintento |
| 5 | Ops | 23 — Platform engineering | ✅ |
| 6 | Dominio | 22 — Salud: HL7/FHIR (solo si apuntás a healthtech) | ⬜ |
| 6 | — | Certificaciones + simulacros de entrevista (DevOps, IA y mixtos) | ⬜ — metas confirmadas: **AWS Certified AI Practitioner** + **CCA-F** (ver arriba y `certificaciones/README.md`) |

**Pendientes puntuales que no son un tema completo** (ver `examenes/registro/`
para el detalle de cada uno): profundizar Kafka/Redpanda vs. SQS y diseño de
arquitectura de red según necesidad (a pedido propio), repaso de nombre de
Trivy, repaso espaciado general con preguntas exigentes (formato selección
múltiple para nombres), y la hoja de vida pendiente de actualizar.

## Fase 0 — Diagnóstico general (arranca acá)

Antes de la Fase 1: un examen general de panorama (1-2 preguntas por tema,
nivel conceptual). Con el resultado ajustamos el orden real de estudio — las
brechas del `gap-analysis.md` son una hipótesis basada en el CV, el
diagnóstico general la confirma o la corrige con datos reales.

- **Parte Ops (temas 01-12):** ✅ hecha el 2026-09-08.
- **Parte IA (temas 14-20):** los fundamentos (tema 14) ya se cubrieron
  enseñando directo durante la Fase 1, sin pasar primero por el examen
  diagnóstico formal — si querés, pedime *"Dame el diagnóstico general de
  IA"* para confirmar con un examen que no quedaron huecos.
- **Herramientas de ofertas startup** (Istio, ArgoCD, Keycloak, OPA, AlloyDB,
  OpenTelemetry, ESO, Atlas, Valkey, Flipt, Redpanda, Temporal, platform
  engineering): ⬜ pendiente. Pedime *"Dame el diagnóstico de herramientas
  startup"*. El tema 22 (salud) no entra, igual que el 13.

## Herramientas de ofertas startup (dónde está cada una)

Agregadas a partir de una oferta de startup (healthtech) del 2026-10-07. No
son un bloque aparte: cada herramienta vive en el tema donde se entiende.

| Herramienta | Tema | Fase |
|---|---|---|
| **Istio** (service mesh) | 10 — Kubernetes avanzado | 1 |
| **ArgoCD** (GitOps), **Flipt** (feature flags) | 03 — CI/CD | 2 |
| **Keycloak** (Identity Provider) | 04 — Identidad | 3 |
| **OPA** (policy as code) | 11 — DevSecOps | 3 |
| **AlloyDB**, **ESO**, **Atlas**, **Valkey** | 06 — Datos y secretos | 4 |
| **Redpanda**, **Temporal** | 21 — Event streaming y workflows (nuevo) | 4 |
| **OpenTelemetry** (hands-on: Collector, OTLP) | 07 — Observabilidad | 5 |
| Equipo de platform engineering | 23 — Platform engineering (nuevo) | 5 |
| **HL7/FHIR**, **Medplum**, **HAPI FHIR**, **OIE** | 22 — Salud (nuevo, dominio) | 6 |

**Cómo se encastra la IA:** cada tema de IA va en la fase donde ya viste la
base Ops que necesita. Desarrollo con LLMs va junto con FastAPI (una API de IA
es una API FastAPI que llama a un modelo); RAG va junto con datos (una base
vectorial es otra base de datos); agentes van junto con orquestación (un
agente es un orquestador donde decide el modelo); MLOps va junto con
observabilidad y CI/CD; serving de modelos va después de Kubernetes y antes
de costos (las GPUs son lo más caro de la factura).

## Fase 1 — Infraestructura base + fundamentos de IA (semanas 1-4) ✅ en su mayoría

Lo más pedido en las ofertas, y donde ya tenés más base (Terraform, Docker, K8s).
En paralelo, el vocabulario de IA que vas a usar en todas las fases siguientes.

- **Ops**
  1. `temas/01-iac-multicloud` — ✅ Terraform (+ Ansible agregado); 🔁 Bicep, y de paso CloudFormation/CDK (AWS) todavía sin ver
  2. `temas/10-kubernetes-avanzado` — ✅ completo: arquitectura, scheduling, networking/mesh, operators/managed-k8s, y troubleshooting (🔵 Senior)
  3. `temas/02-contenedores-serverless` — 🟡 Container Apps / Fargate / Cloud Run tocado, sin examen dedicado
- **IA**
  4. `temas/14-fundamentos-ia-llm` — ✅ ML, LLMs, tokens, embeddings, prompting vs. RAG vs. fine-tuning

## Fase 2 — CI/CD + desarrollo de apps con IA (semanas 5-8) 🟡 parcial

- **Ops**
  5. `temas/03-cicd-multicloud` — ✅ GitHub Actions + OIDC federado; GitOps con ArgoCD (🔁 configuración práctica pendiente); GitLab CI por autoestudio propio, sin verificar
  6. `temas/08-python-fastapi-docker` — ✅ hardening: BOLA (Broken Object Level Authorization) y contenedores sin privilegios de root
- **IA**
  7. `temas/15-desarrollo-apps-llm` — ⬜ APIs de LLMs, structured output, tool use, streaming

Al final de la Fase 2 deberías tener **una API FastAPI de IA desplegada con
CI/CD** (GitHub Actions + OIDC) en Container Apps / Fargate / Cloud Run —
pendiente, falta construirlo.

## Fase 3 — Identidad, seguridad y networking (incluida la seguridad de IA) (semanas 9-12) 🟡 parcial

- **Ops**
  8. `temas/04-identidad-iam` — ✅ Entra ID/RBAC, AWS IAM, GCP IAM, Managed Identity, Keycloak
  9. `temas/05-networking-multicloud` — ✅ VNet/VPC, Private Endpoints/PrivateLink/Private Service Connect
  10. `temas/11-seguridad-devsecops` — ✅ shift-left security, Trivy, OPA/policy-as-code
- **IA**
  11. `temas/20-seguridad-gobernanza-ia` — ⬜ prompt injection, guardrails, OWASP Top 10 para LLMs

Al final de la Fase 3 deberías poder explicar de memoria cómo una app llega a
una base de datos **y a un modelo de IA** sin exponer secretos ni tráfico a
internet público — **en cualquiera de las tres nubes**. La mitad Ops ya
quedó demostrada sin ayuda (Managed Identity/IAM Role → Key Vault/Secrets
Manager → Private Endpoint/PrivateLink); la mitad de IA (seguridad de
modelos) todavía no se vio.

## Fase 4 — Datos, orquestación, RAG y agentes (semanas 13-18) 🟡 parcial

- **Ops**
  12. `temas/06-datos-secretos` — ✅ Key Vault/Secrets Manager/Secret Manager, Cosmos DB/DynamoDB/Firestore (consistencia), AlloyDB/RDS/Cloud SQL
- **IA**
  13. `temas/16-rag-bases-vectoriales` — 🟡 RAG, embeddings, búsqueda vectorial e híbrida cubiertos a nivel conceptual (ver tema 14); falta la parte hands-on de bases vectoriales reales
- **Ops**
  14. `temas/09-orquestacion-serverless` — ✅ Durable Functions / Step Functions / Workflows (mecanismo de replay/historial)
  15. `temas/21-event-streaming-workflows` — 🟡 **Redpanda**/Kafka vs. SQS cubierto conceptual; Temporal (workflows durables) cubierto vía Durable Functions; falta hands-on — profundización pendiente a pedido propio
- **IA**
  16. `temas/17-agentes-ia` — ⬜ como tema IA general (multi-agente, Foundry/Bedrock/Vertex Agent); MCP en sí ya está cubierto a fondo en la pista paralela del CCA-F

## Fase 5 — Operación de IA en producción + nivel Senior (semanas 19-24) 🟡 parcial

- **Ops**
  17. `temas/07-observabilidad-multicloud` — ✅ Azure Monitor, CloudWatch, Cloud Logging/Monitoring, OpenTelemetry (métricas/logs/traces)
- **IA**
  18. `temas/18-mlops-llmops` — ⬜ ciclo de vida de modelos, evals en CI, observabilidad de LLMs
  19. `temas/19-serving-modelos-gpu` — ⬜ vLLM/KServe, GPUs en Kubernetes, autoscaling de inferencia
- **Ops**
  20. `temas/12-arquitectura-costos-multicloud` — 🟡 Well-Architected/Architecture Frameworks, FinOps explicados; repaso estricto de los 6 pilares falló (2/6, ver registro) — 🔁 reintento pendiente
  21. `temas/23-platform-engineering` — ✅ IDP, golden paths, Backstage, Team Topologies/carga cognitiva, multi-tenancy, métricas DORA (junta todo lo anterior)

## Fase 6 — Dominio salud + certificaciones

- Repasar `temas/13-mercadolibre-scopes-cosmos` si aplica a una entrevista interna.
- Repasar `temas/22-datos-salud-hl7-fhir` si la oferta es de salud / healthtech.
- Rendir las certificaciones elegidas (ver `certificaciones/README.md` — ruta
  única que intercala certificaciones DevOps y de IA). Metas confirmadas:
  **AWS Certified AI Practitioner** + **CCA-F**.
- Simulacros de entrevista técnica con Claude usando `examenes/` en modo mixto:
  DevOps, IA, y **mixtos DevOps + IA** (por ejemplo, *"diseñá la plataforma
  para servir un RAG a 10.000 usuarios en AWS"*), formato entrevista.

## Proyecto integrador (atraviesa todas las fases) — ⬜ sin empezar

Para que todo quede junto y tengas algo para mostrar en entrevistas, los labs
de cada fase construyen **una sola aplicación** que va creciendo. Todavía no
se arrancó a construir — lo visto hasta ahora es conceptual/examinado, no
código corriendo:

1. Fase 1: infraestructura con Terraform/Bicep + cluster/contenedor base.
2. Fase 2: API FastAPI que llama a un LLM, con CI/CD y OIDC.
3. Fase 3: identidad gestionada, acceso privado al modelo, guardrails.
4. Fase 4: RAG sobre documentos propios + un agente con herramientas (MCP).
5. Fase 5: evals en el pipeline, observabilidad de tokens/costo/latencia, y
   (opcional) un modelo abierto servido con vLLM en Kubernetes.

## Cómo avanzar de fase

No avances de fase hasta tener **≥ 80% en el examen de cada tema** de la fase
anterior (ver `examenes/registro/`), tanto de los temas Ops como de los de IA.
Si un tema queda débil, se repite antes de seguir — la idea es no acumular
huecos. Actualizá el **tablero de avance** de arriba al cerrar cada tema.

## Fuentes de la investigación de mercado (sept. 2026)

Estas fuentes ya no determinan el **orden** de las fases (eso ahora lo define
la arquitectura de la plataforma objetivo), pero siguen sirviendo para saber
qué certificación/skill tiene más demanda real:

- [Azure DevOps and Security in 2026: Career Path, Skills & Certs — CloudThat](https://www.cloudthat.com/resources/blog/azure-devops-and-security-roadmap-for-2026-skills-and-certifications)
- [Senior DevOps Engineer Job Description: Skills, Salary, & More — iMocha](https://www.imocha.io/job-description/senior-devops-engineer)
- [Job Opening - Senior Azure DevOps / Cloud Platform Engineer — Randstad USA](https://www.randstadusa.com/jobs/4/1343959/senior-azure-devops-cloud-platform-engineer_woburn/)
- [Top 10 DevOps Certifications Engineers Choose in 2026 — KodeKloud](https://kodekloud.com/blog/top-10-devops-certifications-courses-engineers-are-choosing/)
- [AZ-400 Certification (2026 Guide) — CertDemand](https://certdemand.com/certs/az-400)
- [Platform Engineering Certifications 2026 — ExamCert](https://www.examcert.app/blog/platform-engineering-certifications-2026/)

> Nota: son fuentes secundarias (blogs/agregadores), no un estudio estadístico
> formal. Sirven de contexto de mercado — el `gap-analysis.md` (basado en tu
> CV real) y el diagrama de plataforma del tema 23 son la referencia real
> para saber qué tan profundo tenés que ir en cada tema.
