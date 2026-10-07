# Gap Analysis — CV actual vs. vacante Azure Platform Engineer

Fuente de los requisitos: mensaje de Julieta García (PlatformX Solutions),
2026-09-07.

> Este análisis es específico de esa vacante puntual (Azure). El repo en
> general no es Azure-only — ver `temas/` para las equivalencias en AWS y GCP
> de cada tema, y `certificaciones/README.md` para rutas de certificación en
> las tres nubes. Este documento sirve como caso concreto de referencia, no
> como límite del alcance de estudio.

## Requisitos de la vacante

| # | Requisito | Nivel actual | Estado |
|---|---|---|---|
| 1 | Azure Container Apps + ACR | Experiencia con Kubernetes/Docker, pero no específicamente ACA | 🟡 Brecha media |
| 2 | Bicep / IaC | IaC fuerte, pero principalmente **Terraform** (Bizagi, MercadoLibre). Bicep conocido pero no es lo principal | 🟡 Brecha media |
| 3 | GitHub Actions + CI/CD + OIDC | CI/CD fuerte (Azure Pipelines, Jenkins). GitHub Actions y federación OIDC específicamente: por reforzar | 🟡 Brecha media |
| 4 | Microsoft Entra ID, Managed Identity, RBAC | Administración de recursos Azure con Python/PowerShell (Bizagi). Profundidad en Entra ID/Managed Identity: por confirmar | 🟡 Brecha media |
| 5 | Azure Networking: VNet, Private Endpoints, Private DNS, NSG | No mencionado explícitamente en el CV | 🔴 Brecha alta |
| 6 | Key Vault, Cosmos DB, Azure Monitor, App Insights, Log Analytics | Prometheus/Grafana sí; Cosmos DB y Key Vault no aparecen en el CV | 🔴 Brecha alta (Cosmos DB, Key Vault) / 🟡 media (Monitor/AppInsights) |
| 7 | Python/FastAPI + Docker | Python fuerte (AgroTec, APIs serverless). FastAPI específicamente: por confirmar | 🟢 Brecha baja |
| 8 | Azure Durable Functions | Serverless con AWS (AgroTec) pero no Durable Functions de Azure | 🔴 Brecha alta |

## Fortalezas a favor (no pierdas esto en la entrevista)

- **Terraform** de nivel productivo (Bizagi + MercadoLibre) — vale más que Bicep en
  la mayoría de roles senior; solo falta traducir ese conocimiento a sintaxis Bicep.
- **Multi-cloud real**: Azure, AWS y GCP en producción — poco común y muy valorado.
- **CI/CD end-to-end**: Azure Pipelines, Jenkins, y administración con Python/PowerShell.
- **Kubernetes + Docker** en producción de alto volumen transaccional (MercadoLibre).
- **Experiencia end-to-end de software**: no sos "solo infra", también desarrollás
  APIs y arquitecturas event-driven — encaja con el pedido de Python/FastAPI.

## Prioridad de estudio (de mayor a menor brecha)

1. Azure Networking (VNet, Private Endpoints, Private DNS, NSG) — tema nuevo, base para todo lo demás en Azure.
2. Azure Durable Functions — patrón nuevo (orchestrator/activity functions).
3. Cosmos DB + Key Vault — servicios PaaS específicos no usados antes.
4. Bicep — convertir tu conocimiento de Terraform (ya tenés el modelo mental de IaC).
5. Azure Container Apps + ACR — extensión natural de tu experiencia con K8s/Docker.
6. GitHub Actions + OIDC federation — extensión de tu experiencia con Jenkins/Azure Pipelines.
7. Entra ID / Managed Identity / RBAC — profundizar lo que ya usás parcialmente.
8. Azure Monitor / App Insights / Log Analytics — extensión de tu experiencia con Prometheus/Grafana.
9. FastAPI — consolidar (partís de una base sólida de Python).

Ver el orden de estudio semana a semana en `roadmap.md`.

## Brechas de IA (hipótesis — falta diagnóstico)

El objetivo del plan ya no es solo DevOps: también es IA (desarrollo de apps
con IA y operación de IA en producción). Esta parte todavía **no tiene
diagnóstico real** — se confirma con el diagnóstico general de IA (Fase 0 del
roadmap). Hipótesis inicial:

| Área | Base que ya tenés | Estado supuesto |
|---|---|---|
| Fundamentos de IA/LLMs (tema 14) | — | 🔴 por diagnosticar |
| Desarrollo de apps con LLMs (tema 15) | Python fuerte + APIs (FastAPI) | 🟡 base fuerte, falta la parte LLM |
| RAG y bases vectoriales (tema 16) | Bases de datos en producción | 🔴 por diagnosticar |
| Agentes y MCP (tema 17) | Orquestación serverless (parcial) | 🔴 por diagnosticar |
| MLOps / LLMOps (tema 18) | CI/CD + observabilidad fuertes | 🟡 base Ops fuerte, falta el ciclo de vida de modelos |
| Serving y GPUs (tema 19) | Kubernetes productivo | 🟡 base K8s fuerte, falta GPU/inferencia |
| Seguridad de IA (tema 20) | Seguridad cloud (parcial) | 🔴 por diagnosticar |

Tu ventaja diferencial: venir de Ops. MLOps, LLMOps y serving de modelos
son justamente las áreas donde la mayoría de los perfiles de IA son débiles.

## Oferta startup healthtech (2026-10-07) — requisitos "nice to have"

Segunda oferta de referencia. Pide experiencia de startup con estas
herramientas. Estado **por confirmar** con el diagnóstico de herramientas
startup (Fase 0 del roadmap).

| Requisito | Tema | Base que ya tenés | Estado supuesto |
|---|---|---|---|
| Istio | 10 | Kubernetes productivo (MELI) | 🟡 por confirmar |
| ArgoCD (GitOps) | 03 | CI/CD fuerte | 🟡 por confirmar |
| Keycloak | 04 | OIDC (GitHub Actions) | 🔴 por confirmar |
| OPA | 11 | — | 🔴 por confirmar |
| AlloyDB | 06 | GCP + bases de datos | 🟡 por confirmar |
| OpenTelemetry (hands-on) | 07 | Prometheus/Grafana | 🟡 por confirmar |
| ESO | 06 | Kubernetes + secretos | 🟡 por confirmar |
| Atlas (migraciones de schema) | 06 | — | 🔴 por confirmar |
| Valkey / Redis | 06 | — | 🟡 por confirmar |
| Flipt (feature flags) | 03 | — | 🔴 por confirmar |
| Redpanda / Kafka, Temporal | 21 | Arquitecturas event-driven (CV) | 🟡 por confirmar |
| HL7/FHIR, Medplum/HAPI, OIE | 22 | — | 🔴 dominio nuevo |
| Equipo de platform engineering para varios equipos de producto | 23 | MELI (por confirmar si encaja como historia) | 🟡 preparar historias STAR |
| Título universitario (Ing. en Computación / Sistemas o equivalente) | — | por confirmar | — no es de estudio en este plan |
