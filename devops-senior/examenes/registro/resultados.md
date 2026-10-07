# Registro de resultados

| Fecha | Tema | Nivel | Formato | % Aciertos | Puntos débiles detectados |
|---|---|---|---|---|---|
| 2026-09-08 | Diagnóstico general (12 temas, tema 13 MELI excluido) | Panorama | Preguntas abiertas, de a una | ~5/12 sólidas, 2/12 parciales, 5/12 débiles | IAM/Managed Identity, consistencia de bases NoSQL, Durable Functions (activity/orchestrator), Kubernetes troubleshooting, DevSecOps/shift-left |

**Fortalezas confirmadas en el diagnóstico:** IaC (Terraform/Bicep), CI/CD +
OIDC, Networking (Private Endpoint + DNS privado), FastAPI async/await,
Well-Architected trade-offs (buen ejemplo propio con HPA).

> Se completa cada vez que rendís un examen de autoevaluación. Pedime que lo
> actualice al terminar un examen, o hacelo vos mismo siguiendo el formato.

## Pendientes de profundización (retomar después)

- **Durable Functions — `activity` vs. `orchestrator`**: entendido el mecanismo
  de `replay`/determinismo en general, pero el rol específico de una
  `activity` (por qué no se repite en el replay) quedó para repasar con más
  ejemplos. Ver `../../temas/09-orquestacion-serverless/`.
- **Kubernetes — troubleshooting (`CrashLoopBackOff`, `OOMKilled`, exit codes)**:
  tema declarado como no manejado (nunca lo hizo en la práctica). Ver
  `../../temas/10-kubernetes-avanzado/` — el objetivo "Troubleshooting" de ese
  tema es justo esto, hacer una sesión dedicada con varios escenarios de
  `describe pod`/`logs --previous`/exit codes reales.
- **Identidad — Managed Identity system-assigned vs. user-assigned**: no lo
  tenía claro (adivinó), quedó explicado pero conviene repasar con ejemplo
  práctico. Ver `../../temas/04-identidad-iam/`.
- **Consistencia de bases NoSQL (Cosmos DB/DynamoDB/Firestore)**: no conocía
  el concepto de "nivel de consistencia" en absoluto. Ver `../../temas/06-datos-secretos/`.
- **DevSecOps / "shift-left"**: no conocía el término ni herramientas como
  **Trivy**; el concepto general de seguridad temprana sí, pero la
  terminología específica no. Ver `../../temas/11-seguridad-devsecops/`.
- **Cumplimiento PCI-DSS / SOC 2** (surgió en postulaciones, Rapyd): trabajó
  dentro del entorno PCI-DSS de Mercado Pago pero no recuerda los controles.
  Repasar qué exige PCI-DSS a infraestructura (segmentación, cifrado, logs,
  accesos) y en qué se diferencia SOC 2. Ver `../../temas/11-seguridad-devsecops/`.
- **HashiCorp Vault / Open Policy Agent** (surgió en postulaciones, Endava):
  exposición poca; reforzar antes de una entrevista. Vault: motores de
  secretos, secretos dinámicos, auth con Kubernetes/OIDC. OPA: políticas como
  código (Rego, Gatekeeper). Ver `../../temas/06-datos-secretos/` y
  `../../temas/11-seguridad-devsecops/`.
- **Zabbix 6.x/7.x** (surgió en postulaciones, Mainsoft — lo piden como
  indispensable): sin experiencia. Templates, LLD (Low Level Discovery),
  triggers y macros, proxies y Zabbix Agent 2, API JSON-RPC para automatizar
  altas/bajas de hosts, integración de alertas con Teams/Slack/Jira. Montar un
  laboratorio con Docker y monitorear un par de VMs. Ver
  `../../temas/07-observabilidad-multicloud/`.
- **Argo Workflows** (surgió en postulaciones, AgileEngine — obligatorio):
  exposición poca; conoce ArgoCD pero no el motor de workflows. Diferencia con
  ArgoCD, `Workflow`/`WorkflowTemplate`, DAGs y steps, artefactos en S3,
  troubleshooting de pods de un workflow. Ver `../../temas/10-kubernetes-avanzado/`
  y `../../temas/21-event-streaming-workflows/`.
- **PyTorch / TensorFlow** (surgió en postulaciones, Aprio): solo en proyectos
  personales. Repasar entrenamiento y evaluación básicos y cómo se empaqueta
  un modelo para servirlo. Ver `../../temas/18-mlops-llmops/` y
  `../../temas/19-serving-modelos-gpu/`.
- **Vertex AI y AWS Bedrock** (surgieron en postulaciones, Centraprise, EPAM y
  Aptonet): Vertex sin experiencia, Bedrock poca. Ya están dentro de los temas
  15-18; priorizarlos cuando se estudien (agentes en Vertex AI Agent Builder,
  Bedrock Agents/Knowledge Bases).
- **Amazon Connect y Twilio** (surgieron en postulaciones, Rappi y EPAM):
  exposición poca. Contact center en la nube, flujos de contacto, integración
  con Lambda y con LLMs para voz/chat. Ver `../../temas/15-desarrollo-apps-llm/`.
- **Zapier** (surgió en postulaciones, HKR.TEAM): exposición poca. Zaps,
  webhooks y cuándo conviene frente a n8n o Logic Apps; vale para la oferta de
  servicios de automatización.
- **Full-stack con React** (surgió en postulaciones, Strider): tiene
  aplicaciones propias y en producción (referencia: repo `ElGerente`), pero el
  frontend con React es lo más flojo. Repasar React + TypeScript lo suficiente
  para armar la interfaz de un POC sobre una API FastAPI.

## Diagnóstico general de IA pendiente

Con la fusión DevOps + IA del roadmap (2026-10-07) se agregaron los temas
14-20 (IA). Falta rendir el **diagnóstico general de IA** (Fase 0, parte IA)
— mismo formato que el de DevOps: preguntas abiertas, de a una.

## Ronda de vocabulario pendiente

El usuario pidió una ronda rápida de repaso de términos/nombres de
herramientas (sin conceptos nuevos) una vez cerrado el diagnóstico general —
pendiente de hacer.
