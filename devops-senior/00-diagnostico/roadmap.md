# Roadmap de estudio — DevOps + IA (un solo camino)

Objetivo: ser **experto en DevOps/Platform multi-cloud y en IA** (desarrollo
de aplicaciones con IA + operación de IA en producción, MLOps/LLMOps). No son
dos planes separados: cada fase combina un bloque **Ops** y un bloque **IA**
que se apoyan entre sí (por ejemplo, Kubernetes primero y después servir
modelos con GPU sobre Kubernetes).

Orden sugerido. Cada fase es aprox. 3-4 semanas de estudio part-time
(mientras trabajás). Ajustalo a tu ritmo real — lo importante es no saltar
el examen de autoevaluación al final de cada tema.

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

## Tablero de avance (mirá acá cómo vas)

Estados: ⬜ sin empezar · 🟡 en curso · ✅ aprobado (≥ 80% en el examen del
tema) · 🔁 repasar. Se actualiza cada vez que rendís un examen (ver
`../examenes/registro/resultados.md` para el detalle).

| Fase | Bloque | Tema | Estado |
|---|---|---|---|
| 0 | Ops | Diagnóstico general DevOps (temas 01-12) | ✅ hecho 2026-09-08 |
| 0 | IA | Diagnóstico general IA (temas 14-20) | ⬜ |
| 0 | Ops | Diagnóstico de herramientas startup (Istio, ArgoCD, Keycloak, OPA, ESO, Valkey, Redpanda, Temporal…) | ⬜ |
| 1 | Ops | 01 — IaC multi-cloud | ⬜ |
| 1 | Ops | 10 — Kubernetes avanzado | 🔁 troubleshooting pendiente |
| 1 | Ops | 02 — Contenedores serverless | ⬜ |
| 1 | IA | 14 — Fundamentos de IA, ML y LLMs | ⬜ |
| 2 | Ops | 03 — CI/CD multi-cloud | ⬜ |
| 2 | Ops | 08 — Python / FastAPI + Docker | ⬜ |
| 2 | IA | 15 — Desarrollo de apps con LLMs | ⬜ |
| 3 | Ops | 04 — Identidad e IAM | 🔁 Managed Identity pendiente |
| 3 | Ops | 05 — Networking multi-cloud | ⬜ |
| 3 | Ops | 11 — Seguridad / DevSecOps | 🔁 shift-left pendiente |
| 3 | IA | 20 — Seguridad y gobernanza de IA | ⬜ |
| 4 | Ops | 06 — Datos y secretos | 🔁 consistencia NoSQL pendiente |
| 4 | IA | 16 — RAG y bases vectoriales | ⬜ |
| 4 | Ops | 09 — Orquestación serverless | 🔁 activity vs. orchestrator pendiente |
| 4 | Ops | 21 — Event streaming y workflows durables (Redpanda, Temporal) | ⬜ |
| 4 | IA | 17 — Agentes de IA y MCP | ⬜ |
| 5 | Ops | 07 — Observabilidad multi-cloud | ⬜ |
| 5 | IA | 18 — MLOps y LLMOps | ⬜ |
| 5 | IA | 19 — Serving de modelos y GPUs | ⬜ |
| 5 | Ops | 12 — Arquitectura y costos multi-cloud | ⬜ |
| 5 | Ops | 23 — Platform engineering | ⬜ |
| 6 | Dominio | 22 — Salud: HL7/FHIR (solo si apuntás a healthtech) | ⬜ |
| 6 | — | Certificaciones + simulacros de entrevista (DevOps, IA y mixtos) | ⬜ |

## Fase 0 — Diagnóstico general (arranca acá)

Antes de la Fase 1: un examen general de panorama (1-2 preguntas por tema,
nivel conceptual). Con el resultado ajustamos el orden real de estudio — las
brechas del `gap-analysis.md` son una hipótesis basada en el CV, el
diagnóstico general la confirma o la corrige con datos reales.

- **Parte Ops (temas 01-12):** ✅ hecha el 2026-09-08.
- **Parte IA (temas 14-20):** ⬜ pendiente — es lo próximo a hacer. Pedime:
  *"Dame el diagnóstico general de IA"*. Mismo formato: una pregunta por vez.
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

## Orden de las fases: priorizado por demanda real del mercado

El orden de las fases 1-5 no sigue solo el gap-analysis basado en tu CV — se
reordenó según qué aparece con más frecuencia en ofertas reales de Senior
DevOps Engineer / Azure Platform Engineer (búsqueda de mercado, sept. 2026,
ver fuentes al final del archivo). Señal consistente en las tres búsquedas:

1. **IaC (Terraform/Bicep/ARM)** — "core requirement across most postings"
2. **CI/CD** (Azure DevOps / GitHub Actions, YAML pipelines)
3. **Contenedores/Kubernetes** (AKS, Container Apps, Docker, Helm)
4. **Identidad y seguridad** (RBAC, compliance, identity management) — engloba networking/Private Endpoints como parte de "seguridad de red"
5. **Observabilidad** (monitoring, alerting)
6. Certificación de mayor señal combinada: **CKA + Terraform Associate + AZ-400**
   ("highest-signal combination" según la investigación de mercado)

Esto no anula tus brechas reales (Networking y Durable Functions siguen siendo
temas nuevos para vos) — simplemente prioriza primero lo que más se repite en
procesos de selección, para llegar antes a poder rendir pruebas técnicas.

**Cómo se encastra la IA:** cada tema de IA va en la fase donde ya viste la
base Ops que necesita. Desarrollo con LLMs va junto con FastAPI (una API de IA
es una API FastAPI que llama a un modelo); RAG va junto con datos (una base
vectorial es otra base de datos); agentes van junto con orquestación (un
agente es un orquestador donde decide el modelo); MLOps va junto con
observabilidad y CI/CD; serving de modelos va después de Kubernetes y antes
de costos (las GPUs son lo más caro de la factura).

## Fase 1 — Infraestructura base + fundamentos de IA (semanas 1-4)

Lo más pedido en las ofertas, y donde ya tenés más base (Terraform, Docker, K8s).
En paralelo, el vocabulario de IA que vas a usar en todas las fases siguientes.

- **Ops**
  1. `temas/01-iac-multicloud` — Bicep, y de paso CloudFormation/CDK (AWS) y Terraform en GCP
  2. `temas/10-kubernetes-avanzado` — repaso senior + diferencias AKS/EKS/GKE (incluye el troubleshooting pendiente)
  3. `temas/02-contenedores-serverless` — Container Apps / Fargate / Cloud Run
- **IA**
  4. `temas/14-fundamentos-ia-llm` — ML, LLMs, tokens, embeddings, prompting vs. RAG vs. fine-tuning

## Fase 2 — CI/CD + desarrollo de apps con IA (semanas 5-8)

- **Ops**
  5. `temas/03-cicd-multicloud` — GitHub Actions + OIDC federado a Azure, AWS y GCP
  6. `temas/08-python-fastapi-docker` — repaso y hardening de APIs (base para la parte IA)
- **IA**
  7. `temas/15-desarrollo-apps-llm` — APIs de LLMs, structured output, tool use, streaming

Al final de la Fase 2 deberías tener **una API FastAPI de IA desplegada con
CI/CD** (GitHub Actions + OIDC) en Container Apps / Fargate / Cloud Run.

## Fase 3 — Identidad, seguridad y networking (incluida la seguridad de IA) (semanas 9-12)

- **Ops**
  8. `temas/04-identidad-iam` — Entra ID/RBAC, AWS IAM, GCP IAM
  9. `temas/05-networking-multicloud` — VNet/VPC, Private Endpoints/PrivateLink/Private Service Connect
  10. `temas/11-seguridad-devsecops` — shift-left security, escaneo de imágenes/IaC
- **IA**
  11. `temas/20-seguridad-gobernanza-ia` — prompt injection, guardrails, OWASP Top 10 para LLMs

Al final de la Fase 3 deberías poder explicar de memoria cómo una app llega a
una base de datos **y a un modelo de IA** sin exponer secretos ni tráfico a
internet público — **en cualquiera de las tres nubes**.

## Fase 4 — Datos, orquestación, RAG y agentes (semanas 13-18)

- **Ops**
  12. `temas/06-datos-secretos` — Key Vault/Secrets Manager/Secret Manager, Cosmos DB/DynamoDB/Firestore
- **IA**
  13. `temas/16-rag-bases-vectoriales` — RAG, embeddings, búsqueda vectorial e híbrida
- **Ops**
  14. `temas/09-orquestacion-serverless` — Durable Functions / Step Functions / Workflows
  15. `temas/21-event-streaming-workflows` — **Redpanda**/Kafka y **Temporal** (workflows durables agnósticos de nube)
- **IA**
  16. `temas/17-agentes-ia` — agentes, tool use en loop, MCP, multi-agente

## Fase 5 — Operación de IA en producción + nivel Senior (semanas 19-24)

- **Ops**
  17. `temas/07-observabilidad-multicloud` — Azure Monitor, CloudWatch, Cloud Logging/Monitoring
- **IA**
  18. `temas/18-mlops-llmops` — ciclo de vida de modelos, evals en CI, observabilidad de LLMs
  19. `temas/19-serving-modelos-gpu` — vLLM/KServe, GPUs en Kubernetes, autoscaling de inferencia
- **Ops**
  20. `temas/12-arquitectura-costos-multicloud` — Well-Architected/Architecture Frameworks, FinOps (incluido costo de IA/GPU)
  21. `temas/23-platform-engineering` — IDP, golden paths, multi-tenancy, métricas DORA (junta todo lo anterior)

## Fase 6 — Certificación y entrevista

- Rendir las certificaciones elegidas (ver `certificaciones/README.md` —
  ruta única que intercala certificaciones DevOps y de IA).
- Repasar `temas/13-mercadolibre-scopes-cosmos` si aplica a una entrevista interna.
- Repasar `temas/22-datos-salud-hl7-fhir` si la oferta es de salud / healthtech.
- Simulacros de entrevista técnica con Claude usando `examenes/` en modo mixto:
  DevOps, IA, y **mixtos DevOps + IA** (por ejemplo, *"diseñá la plataforma
  para servir un RAG a 10.000 usuarios en AWS"*), formato entrevista.

## Proyecto integrador (atraviesa todas las fases)

Para que todo quede junto y tengas algo para mostrar en entrevistas, los labs
de cada fase construyen **una sola aplicación** que va creciendo:

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

- [Azure DevOps and Security in 2026: Career Path, Skills & Certs — CloudThat](https://www.cloudthat.com/resources/blog/azure-devops-and-security-roadmap-for-2026-skills-and-certifications)
- [Senior DevOps Engineer Job Description: Skills, Salary, & More — iMocha](https://www.imocha.io/job-description/senior-devops-engineer)
- [Job Opening - Senior Azure DevOps / Cloud Platform Engineer — Randstad USA](https://www.randstadusa.com/jobs/4/1343959/senior-azure-devops-cloud-platform-engineer_woburn/)
- [Top 10 DevOps Certifications Engineers Choose in 2026 — KodeKloud](https://kodekloud.com/blog/top-10-devops-certifications-courses-engineers-are-choosing/)
- [AZ-400 Certification (2026 Guide) — CertDemand](https://certdemand.com/certs/az-400)
- [Platform Engineering Certifications 2026 — ExamCert](https://www.examcert.app/blog/platform-engineering-certifications-2026/)

> Nota: son fuentes secundarias (blogs/agregadores), no un estudio estadístico
> formal. Sirven para priorizar el orden de estudio, no como verdad absoluta —
> el `gap-analysis.md` (basado en tu CV real) sigue siendo la referencia para
> saber qué tan profundo tenés que ir en cada tema.
