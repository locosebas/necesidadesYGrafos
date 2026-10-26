# Pendientes de estudio (desde la búsqueda de empleo)

Lista de cosas que aparecen en vacantes reales y que Sebastián quiere estudiar
porque todavía no tiene suficiente experiencia en ellas. Se alimenta cuando él
dice algo como "no tengo tanta experiencia, agrégalo a la lista de estudios",
ya sea en el chat o en las respuestas del tablero de postulaciones
([Mesa de Postulaciones](https://claude.ai/artifact/1TA5UUU7Tq6bmW71Gp5XaE)).

Los pendientes que salen de los exámenes de autoevaluación siguen en
[`examenes/registro/resultados.md`](examenes/registro/resultados.md).

## Cómo se registra cada punto

- **Qué:** la herramienta o el concepto.
- **Por qué:** la vacante que lo pidió y cuánto pesaba (obligatorio o deseable).
- **Nivel actual:** lo que Sebastián dijo que sabe hoy.
- **Dónde estudiarlo:** el tema de [`temas/`](temas/) donde encaja, o "tema nuevo" si no encaja en ninguno.
- **Estado:** pendiente, en curso o visto.

## Prioridad alta

- **Siglas y conceptos de las ofertas de IA** (pedido el 2026-10-02): leer el
  [glosario de IA para ofertas](glosario-ia-ofertas.md) antes que el resto de la
  lista. Explica cada sigla (LLM, RAG, MCP, LoRA, vLLM, evals, etc.) dentro de
  su capa del sistema, marca cuáles ya tienes y termina con un orden sugerido
  de estudio.

## Lista

| Fecha | Qué | Por qué (vacante) | Nivel actual | Dónde estudiarlo | Estado |
|---|---|---|---|---|---|
| 2026-09-30 | AWS Organizations, Control Tower, SCPs y landing zone multi-cuenta | Aló Credit, DevOps Senior ($16 M): obligatorio, es el centro del rol | "Uff no, honestamente no" | [`temas/04-identidad-iam/`](temas/04-identidad-iam/) y [`formulas-de-cero/06-landing-zone-identidad-seguridad.md`](formulas-de-cero/06-landing-zone-identidad-seguridad.md) | pendiente |
| 2026-09-30 | ECS Fargate vs. ECS sobre EC2 (diferencias y cuándo usar cada uno) | Aló Credit, DevOps Senior: obligatorio (ECS Fargate) | Usó ECS, pero no tiene clara la diferencia | [`temas/02-contenedores-serverless/`](temas/02-contenedores-serverless/) | pendiente |
| 2026-09-30 | Bases de datos de series de tiempo (TimescaleDB, InfluxDB, Amazon Timestream) | GME International, Líder de Plataforma AWS + IoT: parte del flujo de telemetría | No las ha usado | [`temas/06-datos-secretos/`](temas/06-datos-secretos/) (tema nuevo dentro de datos) | pendiente |
| 2026-09-30 | SonarQube (calidad y seguridad de código en el pipeline) | Accenture, DevOps/Cloud: requerido junto con Artifactory | No lo ha usado | [`temas/11-seguridad-devsecops/`](temas/11-seguridad-devsecops/) | pendiente |
| 2026-09-30 | SLOs, SLIs y error budgets (definir confiabilidad con métricas) | Mobile Wave (vía Ndeavour), SRE/DevOps: central en el rol | "No tengo claro qué es"; tiene experiencia cercana con umbrales de alerta y capacidad | [`temas/07-observabilidad-multicloud/`](temas/07-observabilidad-multicloud/) | pendiente |
| 2026-09-30 | Pruebas de carga y rendimiento (k6, JMeter, Locust) | Mobile Wave (vía Ndeavour), SRE/DevOps: deseable | "No tengo claro qué es" | [`temas/07-observabilidad-multicloud/`](temas/07-observabilidad-multicloud/) (tema nuevo dentro de confiabilidad) | pendiente |
| 2026-09-30 | ISO/IEC 27001 (controles y auditorías de seguridad) | Kuvasz Solutions, Cloud Engineer: deseable | Trabajó bajo ese marco en Bizagi, pero quiere estudiarlo bien | [`temas/11-seguridad-devsecops/`](temas/11-seguridad-devsecops/) | pendiente |
| 2026-09-30 | Stack ELK (Elasticsearch, Logstash, Kibana), Redis y Cassandra | GoReel, Senior Cloud Delivery Engineer: requerido | Los ha usado, pero no a profundidad | [`temas/07-observabilidad-multicloud/`](temas/07-observabilidad-multicloud/) y [`temas/06-datos-secretos/`](temas/06-datos-secretos/) | pendiente |
| 2026-09-30 | AWS X-Ray (trazas distribuidas) | Rekluti, Senior DevOps AWS: requerido | "Poco, pero sé del tema" | [`temas/07-observabilidad-multicloud/`](temas/07-observabilidad-multicloud/) | pendiente |
| 2026-10-02 | **[PRIORIDAD ALTA]** Siglas de IA: LLMOps, RAG, evals, fine-tuning (SFT/LoRA/QLoRA), model serving (vLLM, KServe, Triton), bases vectoriales, frameworks de agentes | Todas las ofertas de IA del tablero (Robots & Pencils, Mariposa, BC, Niuro, Improving, Curotec, Accelerant, Blupax, Lemon.io) | Tiene LLM en producción y MCP; RAG en proyecto propio; fine-tuning y evals conocidos pero no practicados | [`glosario-ia-ofertas.md`](glosario-ia-ofertas.md) (tema nuevo) | pendiente |
| 2026-10-26 | LangChain y LlamaIndex (frameworks de LLM y RAG) en un proyecto personal: cadenas, retrievers, embeddings y una base vectorial | Devlane (Sr. AI Engineer) y Palo Alto Networks (AI & Automation Engineer): los piden por nombre | Llevó un LLM (Claude) a producción con harness, hooks y MCP en el triage de MercadoLibre, con recuperación de runbooks y casos anteriores (RAG); LangChain/LlamaIndex por nombre no los ha usado | [`temas/16-rag-bases-vectoriales/`](temas/16-rag-bases-vectoriales/) y [`temas/15-desarrollo-apps-llm/`](temas/15-desarrollo-apps-llm/) | pendiente |

## Pendientes de las rondas de postulaciones del 2 y el 7 de octubre

Venían en una rama aparte (`claude/estudio-desde-postulaciones`); se trajeron aquí al limpiar ramas el 2026-10-15.

- **Cumplimiento PCI-DSS / SOC 2** (surgió en postulaciones, Rapyd): trabajó
  dentro del entorno PCI-DSS de Mercado Pago pero no recuerda los controles.
  Repasar qué exige PCI-DSS a infraestructura (segmentación, cifrado, logs,
  accesos) y en qué se diferencia SOC 2. Ver `temas/11-seguridad-devsecops/`.
- **HashiCorp Vault / Open Policy Agent** (surgió en postulaciones, Endava):
  exposición poca; reforzar antes de una entrevista. Vault: motores de
  secretos, secretos dinámicos, auth con Kubernetes/OIDC. OPA: políticas como
  código (Rego, Gatekeeper). Ver `temas/06-datos-secretos/` y
  `temas/11-seguridad-devsecops/`.
- **Zabbix 6.x/7.x** (surgió en postulaciones, Mainsoft — lo piden como
  indispensable): sin experiencia. Templates, LLD (Low Level Discovery),
  triggers y macros, proxies y Zabbix Agent 2, API JSON-RPC para automatizar
  altas/bajas de hosts, integración de alertas con Teams/Slack/Jira. Montar un
  laboratorio con Docker y monitorear un par de VMs. Ver
  `temas/07-observabilidad-multicloud/`.
- **Argo Workflows** (surgió en postulaciones, AgileEngine — obligatorio):
  exposición poca; conoce ArgoCD pero no el motor de workflows. Diferencia con
  ArgoCD, `Workflow`/`WorkflowTemplate`, DAGs y steps, artefactos en S3,
  troubleshooting de pods de un workflow. Ver `temas/10-kubernetes-avanzado/`
  y `temas/21-event-streaming-workflows/`.
- **PyTorch / TensorFlow** (surgió en postulaciones, Aprio): solo en proyectos
  personales. Repasar entrenamiento y evaluación básicos y cómo se empaqueta
  un modelo para servirlo. Ver `temas/18-mlops-llmops/` y
  `temas/19-serving-modelos-gpu/`.
- **Vertex AI y AWS Bedrock** (surgieron en postulaciones, Centraprise, EPAM y
  Aptonet): Vertex sin experiencia, Bedrock poca. Ya están dentro de los temas
  15-18; priorizarlos cuando se estudien (agentes en Vertex AI Agent Builder,
  Bedrock Agents/Knowledge Bases).
- **Amazon Connect y Twilio** (surgieron en postulaciones, Rappi y EPAM):
  exposición poca. Contact center en la nube, flujos de contacto, integración
  con Lambda y con LLMs para voz/chat. Ver `temas/15-desarrollo-apps-llm/`.
- **Zapier** (surgió en postulaciones, HKR.TEAM): exposición poca. Zaps,
  webhooks y cuándo conviene frente a n8n o Logic Apps; vale para la oferta de
  servicios de automatización.
- **Full-stack con React** (surgió en postulaciones, Strider): tiene
  aplicaciones propias y en producción (referencia: repo `ElGerente`), pero el
  frontend con React es lo más flojo. Repasar React + TypeScript lo suficiente
  para armar la interfaz de un POC sobre una API FastAPI.
