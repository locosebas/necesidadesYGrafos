# Contenedores serverless: Container Apps, ECS/Fargate, Cloud Run

Partís de una base sólida de Docker y Kubernetes (K8s "real" en las tres
nubes: AKS/EKS/GKE se ven en `10-kubernetes-avanzado`). Acá el foco es la capa
**serverless de contenedores** — más simple que gestionar un clúster propio.

## Objetivos

- Explicar cuándo conviene serverless-containers vs. Kubernetes gestionado
  (AKS/EKS/GKE) vs. Kubernetes self-managed.
- Dominar el ciclo de vida de un despliegue (revisiones/versiones, blue/green,
  traffic splitting) en al menos dos de las tres nubes.
- Autoscaling basado en eventos (KEDA en Azure, App Auto Scaling en AWS,
  autoscaling nativo en Cloud Run).
- Push/pull seguro de imágenes con identidad gestionada (no credenciales sueltas).

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Serverless containers | **Container Apps** (sobre K8s/KEDA/Dapr) | **Fargate** (sobre ECS o EKS, sin gestionar nodos) | **Cloud Run** (sobre Knative) |
| Kubernetes gestionado | AKS | EKS | GKE (Autopilot o Standard) |
| Registro de imágenes | **ACR** (Azure Container Registry) | **ECR** (Elastic Container Registry) | **Artifact Registry** |
| Autoscaling basado en eventos | KEDA (nativo en Container Apps) | Application Auto Scaling / KEDA sobre EKS | Cloud Run autoscaling nativo (requests concurrentes) |
| Revisiones / versiones con tráfico dividido | Revisions (traffic splitting) | ECS: task definitions + CodeDeploy blue/green | Cloud Run: revisions (traffic splitting nativo, muy similar a ACA) |
| Identidad para pull de imagen | Managed Identity + rol `AcrPull` | IAM Task Role | Service Account de GCP |

## Subtemas

1. Azure Container Apps: Environment, revisions, ingress interno/externo, scale rules KEDA
2. AWS Fargate: task definitions, services, ALB/NLB integration, cluster capacity providers
3. GCP Cloud Run: services, revisions, concurrency, min/max instances, Cloud Run jobs (batch)
4. Autenticación sin credenciales estáticas: Managed Identity (Azure) / IAM roles (AWS) / Service Accounts (GCP) — mismo principio, distinta implementación
5. Escaneo de imágenes: Defender for Containers (Azure) / Amazon Inspector (AWS) / Artifact Analysis (GCP)

## Recursos

- Container Apps: https://learn.microsoft.com/azure/container-apps/overview
- AWS Fargate: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/what-is-fargate.html
- Cloud Run: https://cloud.google.com/run/docs

## Lab sugerido

Tomá la misma imagen Docker y desplegala en **Container Apps** y en
**Cloud Run** (las dos más parecidas conceptualmente). Compará: cómo se
configura el traffic splitting entre revisiones y cómo se define el
autoscaling en cada una.

## Autoevaluación

Pedime: *"Dame un examen de contenedores serverless (ACA/Fargate/Cloud Run) nivel senior"*.
