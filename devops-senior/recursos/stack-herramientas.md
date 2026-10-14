# Stack de herramientas — DevOps / Plataforma

Herramientas agrupadas por categoría y ordenadas, dentro de cada categoría,
de la que más conoces a la que menos. Versión visual con buscador y filtro
por nivel: [stack-herramientas.html](stack-herramientas.html).

## Escala

| Nivel | Significado | Herramientas |
|---|---|---|
| 🔵 | Senior | 0 |
| 🟢 | Sólido | 47 |
| 🟡 | Intermedio | 27 |
| 🔴 | Novato (visto en el plan, sin poner a prueba) | 56 |
| ⬜ | No visto | 109 |

Fuentes de la calificación: `examenes/registro/progreso.md` (desempeño en
repasos), tu experiencia laboral confirmada en postulaciones y los temas del
plan donde aparece cada herramienta. Una herramienta solo mencionada en un
tema que todavía no estudias queda en ⬜.

## 1. CI/CD (Integración y Entrega Continuas)

- 🟢 GitHub Actions — producción, Terraform plan/apply por PR
- 🟢 Jenkins — experiencia real
- 🟢 Azure DevOps (Azure Pipelines) — experiencia real
- 🟡 GitLab CI — usado en Bizagi; en el plan sigue 🔴 sin verificar
- ⬜ CircleCI
- ⬜ Bitbucket Pipelines
- ⬜ TeamCity
- ⬜ AWS CodePipeline / CodeBuild
- ⬜ Google Cloud Build
- ⬜ Tekton

## 2. GitOps y despliegue

- 🟢 Helm — uso profesional desde 2022
- 🟡 Argo CD — modelo pull claro; falta configuración práctica
- 🔴 Argo Rollouts — progressive delivery, tema Davivienda
- 🔴 Flagger — progressive delivery, tema Davivienda
- 🔴 Flux
- 🔴 Kustomize
- 🔴 LaunchDarkly — feature flags, Dapta
- 🔴 Unleash — feature flags, Dapta
- ⬜ Spinnaker

## 3. Infraestructura como código (IaC)

- 🟢 Terraform — state, locking, backends
- 🟡 Terragrunt — explicado; poco uso real
- 🟡 Ansible — fundamentos, roles, idempotencia
- 🔴 Crossplane — tema 23
- ⬜ OpenTofu
- ⬜ Bicep — hueco del roadmap
- ⬜ ARM Templates
- ⬜ AWS CloudFormation — hueco del roadmap
- ⬜ AWS CDK — hueco del roadmap
- ⬜ Pulumi
- ⬜ Chef
- ⬜ Puppet
- ⬜ Packer

## 4. Contenedores y orquestación

- 🟢 Kubernetes — troubleshooting 🔵; operators en MercadoLibre
- 🟢 Docker
- 🟢 AWS ECS / Fargate — ECS 2 años en MercadoLibre; Fargate 🟡
- 🟢 EKS
- 🟢 AKS
- 🟡 GKE
- 🟡 Istio
- 🟡 containerd — arquitectura de K8s
- 🟡 Azure Container Apps
- 🟡 Google Cloud Run
- 🟡 ECR
- 🔴 KEDA
- 🔴 Linkerd
- 🔴 ACR
- 🔴 Artifact Registry
- ⬜ Podman
- ⬜ Karpenter
- ⬜ Harbor

## 5. Nube

- 🟢 AWS
- 🟢 Azure
- 🟢 AWS Lambda — Lambda + API Gateway + SQS/SNS
- 🟢 Azure Functions / Durable Functions — replay del orchestrator
- 🟡 GCP
- 🟡 AWS Step Functions — tema 09
- ⬜ Google Cloud Functions

## 6. Networking — AWS

- 🟢 VPC — modelo de 3 capas, subredes pública/privada
- 🟢 Security Groups — experiencia real
- 🟢 NACLs (Network ACLs) — experiencia real
- 🟢 Route Tables — enrutamiento de VPC, experiencia real
- 🟢 Internet Gateway — subred pública
- 🟢 NAT Gateway — salida a internet de subred privada
- 🟢 AWS PrivateLink / VPC Endpoints
- 🟢 AWS WAF
- 🟢 AWS Direct Connect — lo configuraste
- 🟢 Amazon API Gateway — experiencia real
- 🟡 ALB / NLB / GWLB (Elastic Load Balancing) — fallado en entrevista EY, repasado
- 🟡 AWS Network Firewall — firewall centralizado como concepto
- 🔴 Transit Gateway — tema 05
- 🔴 VPC Peering — tema 05
- 🔴 Route 53 — tema 05
- ⬜ Amazon CloudFront
- ⬜ AWS Global Accelerator
- ⬜ AWS Shield
- ⬜ AWS Site-to-Site VPN — no la has configurado
- ⬜ AWS Client VPN
- ⬜ VPC Flow Logs
- ⬜ VPC Lattice

## 7. Networking — Azure

- 🟢 VNet (Virtual Network) — modelo de 3 capas
- 🟢 NSG (Network Security Group)
- 🟢 Private Endpoint
- 🟢 NAT Gateway
- 🟡 Azure Firewall — firewall centralizado como concepto
- 🔴 VNet Peering — tema 05
- 🔴 UDR (User-Defined Routes) — tema 05
- 🔴 Private DNS Zones — tema 05
- 🔴 Network Watcher — tema 05
- ⬜ Azure Load Balancer — ≈ NLB
- ⬜ Application Gateway (+ WAF) — ≈ ALB + AWS WAF
- ⬜ Azure Front Door — ≈ CloudFront + WAF global
- ⬜ Traffic Manager — ≈ Route 53 por DNS
- ⬜ Virtual WAN (hub-and-spoke) — ≈ Transit Gateway
- ⬜ VPN Gateway
- ⬜ ExpressRoute — ≈ Direct Connect 🟢
- ⬜ Service Endpoints
- ⬜ Private Link Service
- ⬜ Azure Bastion
- ⬜ Azure DDoS Protection — ≈ AWS Shield
- ⬜ API Management — ≈ API Gateway 🟢
- ⬜ Azure DNS

## 8. Networking — GCP

- 🟢 Private Service Connect
- 🟡 VPC (global) — como en AWS, pero una VPC abarca todas las regiones
- 🔴 VPC Firewall Rules — tema 05
- 🔴 VPC Network Peering — tema 05
- 🔴 Cloud DNS — tema 05
- 🔴 Network Connectivity Center — tema 05
- ⬜ Cloud NAT — ≈ NAT Gateway 🟢
- ⬜ Cloud Load Balancing — ≈ ALB/NLB
- ⬜ Cloud Armor — ≈ WAF
- ⬜ Cloud CDN — ≈ CloudFront
- ⬜ Shared VPC
- ⬜ Cloud Router
- ⬜ Cloud VPN
- ⬜ Cloud Interconnect — ≈ Direct Connect 🟢
- ⬜ API Gateway / Apigee

## 9. Seguridad

- 🟢 OPA / Gatekeeper — policy-as-code
- 🟡 Trivy — mecanismo bien; nombre débil
- 🔴 Snyk
- 🔴 Semgrep
- 🔴 Dependabot
- 🔴 Renovate
- 🔴 Checkov
- 🔴 tfsec
- 🔴 Gitleaks
- 🔴 GitHub Secret Scanning
- 🔴 Cosign / Sigstore
- 🔴 Kyverno
- 🔴 Microsoft Defender for Cloud
- 🔴 AWS GuardDuty
- ⬜ SonarQube — en tu lista de estudio
- ⬜ OWASP ZAP
- ⬜ Burp Suite
- ⬜ CodeQL
- ⬜ Checkmarx
- ⬜ Fortify
- ⬜ OWASP Dependency-Check
- ⬜ Mend
- ⬜ Nuclei
- ⬜ Grype
- ⬜ Clair
- ⬜ Docker Scout
- ⬜ KICS
- ⬜ Terrascan
- ⬜ TruffleHog
- ⬜ Syft (SBOM)
- ⬜ SLSA
- ⬜ Falco
- ⬜ Wiz
- ⬜ Prisma Cloud

## 10. Identidad y secretos

- 🟢 AWS IAM — IRSA sin ayuda
- 🟢 Azure Key Vault
- 🟢 AWS Secrets Manager
- 🟡 Keycloak — Realm, Client, SSO
- 🟡 Microsoft Entra ID (Azure AD) — Managed Identity, RBAC
- 🟡 GCP Secret Manager
- 🔴 HashiCorp Vault
- 🔴 External Secrets Operator
- 🔴 Okta
- ⬜ Auth0
- ⬜ Sealed Secrets

## 11. Carga y performance

- 🔴 k6 — en tu lista de estudio
- 🔴 JMeter — en tu lista de estudio
- ⬜ Gatling
- ⬜ Locust
- ⬜ Artillery
- ⬜ Vegeta
- ⬜ wrk
- ⬜ hey
- ⬜ Azure Load Testing
- ⬜ Distributed Load Testing on AWS

## 12. Observabilidad

- 🟢 AWS CloudWatch / X-Ray — CloudWatch sí; X-Ray poco
- 🟡 OpenTelemetry — señales bien; el Collector por dentro sigue 🔴
- 🟡 Datadog — uso real como consumidor
- 🟡 Grafana — uso real como consumidor
- 🟡 ELK / Elastic Stack — usado, no a fondo
- 🔴 Prometheus
- 🔴 Loki
- 🔴 Tempo
- 🔴 Zipkin
- 🔴 Splunk
- 🔴 New Relic
- 🔴 Dynatrace
- 🔴 Azure Monitor / Application Insights / Log Analytics
- 🔴 PagerDuty
- 🔴 Opsgenie
- ⬜ Thanos
- ⬜ Mimir
- ⬜ VictoriaMetrics
- ⬜ Fluentd / Fluent Bit
- ⬜ Jaeger
- ⬜ Elastic APM
- ⬜ Google Cloud Operations
- ⬜ Alertmanager

## 13. Chaos engineering

- 🔴 Chaos Mesh — concepto de chaos engineering 🔴
- ⬜ LitmusChaos
- ⬜ AWS Fault Injection Service
- ⬜ Azure Chaos Studio

## 14. Datos y mensajería

- 🟢 Kafka — log retenido, replay, Outbox
- 🟢 AWS SQS / SNS — experiencia real
- 🟢 PostgreSQL
- 🟢 Cosmos DB — niveles de consistencia
- 🟢 DynamoDB — niveles de consistencia
- 🟡 Redis — usado, no a fondo
- 🟡 MySQL — relacional administrada
- 🔴 RabbitMQ
- 🔴 Azure Service Bus / Event Hubs
- 🔴 Google Pub/Sub
- 🔴 MongoDB
- 🔴 Temporal
- ⬜ Airflow

## 15. Platform Engineering

- 🟢 Backstage — IDP, golden path
- 🔴 Crossplane — tema 23
- ⬜ Port

## 16. IA / MLOps / LLMOps

- 🟢 MCP (Model Context Protocol) — has construido servidores MCP
- 🟡 KServe — solo proyectos personales
- ⬜ MLflow
- ⬜ Kubeflow
- ⬜ SageMaker
- ⬜ Azure ML
- ⬜ Vertex AI
- ⬜ vLLM
- ⬜ Ollama
- ⬜ LangChain
- ⬜ LlamaIndex
- ⬜ pgvector — RAG/embeddings 🟢 como concepto
- ⬜ Pinecone
- ⬜ Qdrant
- ⬜ Azure AI Search
- ⬜ Langfuse
- ⬜ LangSmith
- ⬜ Promptfoo

## 17. Lenguajes y scripting

- 🟢 Python — lenguaje principal, 5 años
- 🟢 Go — MercadoLibre
- 🟢 FastAPI — hardening, BOLA
- 🟢 Bash
- 🟢 YAML
- 🟢 HCL (HashiCorp Configuration Language) — Terraform
- ⬜ PowerShell
