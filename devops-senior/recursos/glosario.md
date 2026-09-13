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
| — | RDS | Cloud SQL | Base relacional gestionada (Postgres/MySQL) |
| — | Aurora | AlloyDB | Base relacional de alto rendimiento compatible con Postgres |
| Event Hubs | MSK / Kinesis Data Streams | Pub/Sub | Log de eventos gestionado (Kafka-compatible solo Event Hubs/MSK) |

## Términos generales (no específicos de una nube)

| Término | Definición corta |
|---|---|
| OIDC | OpenID Connect — protocolo de federación de identidad; permite que GitHub Actions se autentique sin secretos de larga duración |
| IaC | Infrastructure as Code |
| Terraform | Herramienta de IaC multi-cloud (HashiCorp); mantiene su propio state file |
| KEDA | Kubernetes Event-Driven Autoscaling — escalado basado en eventos externos (colas, HTTP), usado en ACA/AKS/EKS/GKE |
| Orchestrator function | Función que coordina un workflow con estado; debe ser determinística en modelos tipo Durable Functions |
| Well-Architected Framework | Marco de 5 pilares (Reliability, Security, Cost, Operational Excellence, Performance) — versión propia en Azure, AWS y GCP |
| GitOps | Patrón de CD donde un repo Git es la única fuente de verdad y un operador dentro del clúster aplica los cambios (pull), no el pipeline (push) |
| ArgoCD | Controlador de GitOps para Kubernetes; sincroniza manifiestos de un repo Git hacia el clúster |
| GitLab CI | Orquestador de CI/CD de GitLab, mismo rol que GitHub Actions |
| Keycloak | IAM open-source y self-hosteable (OIDC/SAML); realms, clients, roles y groups |
| Service mesh | Capa de red entre pods vía sidecar proxy (Envoy); da mTLS, traffic splitting y observabilidad sin tocar el código de la app |
| Istio | Implementación más conocida de service mesh para Kubernetes |
| OPA (Open Policy Agent) | Motor de policy-as-code (lenguaje Rego); en K8s se usa vía Gatekeeper como admission controller |
| Rego | Lenguaje de políticas de Open Policy Agent |
| Temporal | Motor de orquestación de workflows open-source/cloud-agnostic, mismo modelo que Durable Functions (Workflow + Activity) pero en código |
| Kafka | Log de eventos distribuido (topics, partitions, offsets, consumer groups); estándar de facto de streaming |
| Redpanda | Reescritura de Kafka en C++, API wire-compatible, sin JVM/ZooKeeper |
| FHIR | Estándar moderno (HL7) de interoperabilidad de datos de salud, API REST con recursos JSON/XML |
| HL7 | Familia de estándares de intercambio de datos clínicos; FHIR es su versión moderna |

## Enlaces generales

- Microsoft Learn (certificaciones Azure): https://learn.microsoft.com/certifications/
- AWS Certification: https://aws.amazon.com/certification/
- Google Cloud Certification: https://cloud.google.com/certification
- Azure Architecture Center: https://learn.microsoft.com/azure/architecture/
- AWS Architecture Center: https://aws.amazon.com/architecture/
- Google Cloud Architecture Center: https://cloud.google.com/architecture
