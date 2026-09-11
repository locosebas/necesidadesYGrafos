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

## Términos de Chaos Engineering / SRE (tema 14)

| Término | Definición corta |
|---|---|
| Chaos Engineering | Disciplina de provocar fallas controladas en un sistema para descubrir debilidades antes de que las encuentre un usuario real |
| Blast radius | Radio de impacto de un experimento de chaos engineering; se empieza acotado (un pod, un % chico de tráfico) y se expande gradualmente |
| Steady-state hypothesis | Hipótesis de "comportamiento normal" del sistema, medida antes y después del experimento para saber si la falla tuvo impacto |
| Litmus | Herramienta de chaos engineering nativa de Kubernetes (proyecto CNCF), basada en CRDs (`ChaosEngine`) |
| Chaos Mesh | Herramienta de chaos engineering nativa de Kubernetes (proyecto CNCF), basada en CRDs (`PodChaos`, `NetworkChaos`) |
| Chaos Monkey | Herramienta pionera de Netflix que termina instancias al azar en producción; origen histórico de la disciplina |
| Gremlin | Plataforma comercial (SaaS) de chaos engineering, con certificación propia y controles de "halt" de emergencia |
| OpenTelemetry | Estándar abierto de instrumentación (trazas, métricas, logs) neutral de vendor; puede exportar a Prometheus, Elastic u otros backends |
| Elastic Stack (ELK) | Elasticsearch (búsqueda/almacenamiento) + Logstash/Beats (ingesta) + Kibana (visualización); logging centralizado |
| AIOps | Aplicación de IA/ML a operaciones: detección de anomalías, correlación automática de alertas, reducción de alert fatigue |

## Términos generales (no específicos de una nube)

| Término | Definición corta |
|---|---|
| OIDC | OpenID Connect — protocolo de federación de identidad; permite que GitHub Actions se autentique sin secretos de larga duración |
| IaC | Infrastructure as Code |
| Terraform | Herramienta de IaC multi-cloud (HashiCorp); mantiene su propio state file |
| KEDA | Kubernetes Event-Driven Autoscaling — escalado basado en eventos externos (colas, HTTP), usado en ACA/AKS/EKS/GKE |
| Orchestrator function | Función que coordina un workflow con estado; debe ser determinística en modelos tipo Durable Functions |
| Well-Architected Framework | Marco de 5 pilares (Reliability, Security, Cost, Operational Excellence, Performance) — versión propia en Azure, AWS y GCP |

## Enlaces generales

- Microsoft Learn (certificaciones Azure): https://learn.microsoft.com/certifications/
- AWS Certification: https://aws.amazon.com/certification/
- Google Cloud Certification: https://cloud.google.com/certification
- Azure Architecture Center: https://learn.microsoft.com/azure/architecture/
- AWS Architecture Center: https://aws.amazon.com/architecture/
- Google Cloud Architecture Center: https://cloud.google.com/architecture
