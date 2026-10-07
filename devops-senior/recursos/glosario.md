# Glosario rápido

Términos que aparecen seguido en los temas de este repo. Referencia rápida,
no reemplaza leer el tema completo. Incluye el equivalente en las tres nubes
cuando aplica — ver también las tablas de equivalencias dentro de cada tema.

| Término (Azure) | Equivalente AWS | Equivalente GCP | Definición corta |
|---|---|---|---|
| ACA (Container Apps) | Fargate (sobre ECS/EKS) | Cloud Run | Serverless containers |
| ACR | ECR | Artifact Registry | Registro privado de imágenes de contenedor |
| Managed Identity | IAM Role | Service Account | Identidad gestionada para un recurso, sin credenciales manuales |
| RBAC (Azure) | IAM Policies | Cloud IAM | Autorización basada en roles/policies sobre un scope de recursos |
| Private Endpoint | VPC Endpoint / PrivateLink | Private Service Connect | Acceso privado a un servicio PaaS/gestionado sin salir a internet |
| NSG | Security Group / NACL | Firewall Rules | Reglas de firewall a nivel de red |
| VNet | VPC | VPC (global) | Red virtual privada |
| Key Vault | Secrets Manager | Secret Manager | Gestión de secretos/keys/certificados |
| Cosmos DB | DynamoDB | Firestore / Bigtable | Base de datos NoSQL gestionada |
| RU (Request Unit) | RCU/WCU | — (facturado por operación) | Unidad de throughput en Cosmos DB / DynamoDB |
| Azure Monitor | CloudWatch | Cloud Monitoring | Paraguas de métricas/logs/alertas |
| Application Insights | AWS X-Ray | Cloud Trace | APM / tracing distribuido |
| KQL | CloudWatch Logs Insights QL | Cloud Logging query language | Lenguaje de consulta de logs |
| Durable Functions | Step Functions | Workflows | Orquestación de workflows con estado |
| Bicep | CloudFormation / CDK | Deployment Manager (o Terraform) | IaC nativo del proveedor |
| AKS | EKS | GKE | Kubernetes gestionado |
| Azure AI Foundry | Amazon Bedrock | Vertex AI | Plataforma para usar/desplegar modelos de IA generativa (LLMs) |
| Azure Machine Learning | SageMaker AI | Vertex AI (Training/Pipelines) | Plataforma de MLOps: entrenar, registrar y desplegar modelos propios |
| Azure AI Search | OpenSearch Serverless / Bedrock Knowledge Bases | Vertex AI Vector Search / RAG Engine | Búsqueda vectorial/híbrida para RAG |
| Azure AI Content Safety | Bedrock Guardrails | Model Armor | Guardrails: filtros de entrada/salida de un LLM |
| Azure AI Foundry Agent Service | Bedrock Agents / AgentCore | Vertex AI Agent Engine | Servicio gestionado para correr agentes de IA |

## Términos generales (no específicos de una nube)

| Término | Definición corta |
|---|---|
| OIDC | OpenID Connect — protocolo de federación de identidad; permite que GitHub Actions se autentique sin secretos de larga duración |
| IaC | Infrastructure as Code |
| Terraform | Herramienta de IaC multi-cloud (HashiCorp); mantiene su propio state file |
| KEDA | Kubernetes Event-Driven Autoscaling — escalado basado en eventos externos (colas, HTTP), usado en ACA/AKS/EKS/GKE |
| Orchestrator function | Función que coordina un workflow con estado; debe ser determinística en modelos tipo Durable Functions |
| LLM | Large Language Model — modelo de lenguaje grande (Claude, GPT, Gemini, Llama) |
| Token | Unidad en la que un LLM lee/escribe texto (aprox. ¾ de palabra); se cobra por token |
| Context window | Cantidad máxima de tokens que el modelo puede "ver" en una llamada |
| Embedding | Vector numérico que representa el significado de un texto; permite búsqueda por similitud |
| RAG | Retrieval-Augmented Generation — buscar documentos relevantes y dárselos al LLM para responder |
| Fine-tuning | Reentrenar parcialmente un modelo con datos propios |
| Tool use / function calling | El LLM pide ejecutar una función tuya y usa el resultado |
| Agente | LLM que elige herramientas en loop hasta cumplir un objetivo |
| MCP | Model Context Protocol — estándar para exponer herramientas y datos a agentes de IA |
| Evals | Tests automáticos de calidad para apps de IA (equivalente a tests unitarios) |
| Prompt injection | Ataque que mete instrucciones maliciosas en el input del LLM |
| vLLM | Motor open source para servir LLMs con alto rendimiento |
| MLflow | Herramienta open source de MLOps: tracking de experimentos y model registry |
| Istio | Service mesh: mTLS entre servicios, gestión de tráfico (canary) y observabilidad, sin tocar el código |
| ArgoCD | Herramienta de GitOps: sincroniza el cluster de Kubernetes con lo que hay en Git |
| GitOps | Git como fuente de verdad del estado deseado; un agente (ArgoCD, Flux) lo aplica |
| Keycloak | Identity Provider open source (OIDC/SAML, SSO), self-hosteable |
| OPA / Rego | Open Policy Agent: motor de policy as code; Rego es su lenguaje. Gatekeeper lo aplica en Kubernetes |
| AlloyDB | Base de datos de GCP compatible con PostgreSQL, de alto rendimiento |
| ESO | External Secrets Operator: sincroniza secretos del gestor de la nube a Secrets de Kubernetes |
| Atlas (Ariga) | Migraciones de schema de base de datos como código (no confundir con MongoDB Atlas) |
| Valkey | Cache key-value en memoria, fork open source de Redis |
| Flipt | Plataforma open source de feature flags |
| Redpanda | Plataforma de event streaming compatible con la API de Kafka, sin JVM ni ZooKeeper |
| Temporal | Motor de workflows durables (workflows + activities), agnóstico de nube |
| HL7 v2 / FHIR | Estándares de intercambio de datos de salud: HL7 v2 (mensajes legacy), FHIR (API REST + JSON) |
| IDP (Internal Developer Platform) | Plataforma interna que da self-service a los equipos de producto |
| Métricas DORA | Deployment frequency, lead time, change failure rate, time to restore |
| Well-Architected Framework | Marco de 5 pilares (Reliability, Security, Cost, Operational Excellence, Performance) — versión propia en Azure, AWS y GCP |

## Enlaces generales

- Microsoft Learn (certificaciones Azure): https://learn.microsoft.com/certifications/
- AWS Certification: https://aws.amazon.com/certification/
- Google Cloud Certification: https://cloud.google.com/certification
- Azure Architecture Center: https://learn.microsoft.com/azure/architecture/
- AWS Architecture Center: https://aws.amazon.com/architecture/
- Google Cloud Architecture Center: https://cloud.google.com/architecture
