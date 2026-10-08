# Operators, CRDs y diferencias entre Kubernetes gestionado (AKS/EKS/GKE)

## Objetivos

- Operators y CRDs (concepto, aunque no hayas escrito uno) — repaso desde `01-arquitectura-y-cluster.md`.
- Diferencias operativas entre AKS, EKS y GKE (lo que ya usaste en AWS/GCP).

## Operators y CRDs, en más detalle

- Un **CRD** agrega un `kind` nuevo a la API de Kubernetes (ej.: `PostgresCluster`).
- Un **Operator** es el controller que reconcilia ese CRD: mira el estado
  deseado (`spec` del CRD) y ejecuta la lógica de negocio para lograrlo
  (crear pods, hacer backup, promover una réplica a primaria en un failover).
- Por qué importa para "arquitecto de plataforma": un operator es lo que le
  permite a una self-service developer platform ofrecer "una base de datos"
  o "un cluster de Kafka" como un simple YAML, sin que el equipo de
  producto sepa operarlo — la complejidad queda escondida en el operator.
- Ejemplos conocidos: Argo CD tiene su propio CRD (`Application`), cert-manager
  (`Certificate`), Prometheus Operator (`ServiceMonitor`).

## Kubernetes gestionado: AKS vs EKS vs GKE

| Aspecto | AKS (Azure) | EKS (AWS) | GKE (GCP) |
|---|---|---|---|
| Control plane | Gratis | Con costo por clúster | Gratis (1 clúster) / con costo desde el 2do |
| Modo "sin gestionar nodos" | Container Apps (fuera de AKS) o virtual nodes | Fargate profiles sobre EKS | **Autopilot** (el más maduro de los tres en este modelo) |
| Identidad de pods hacia servicios cloud | Workload Identity (Azure AD federado) | IRSA (IAM Roles for Service Accounts) | Workload Identity (GCP) |
| Upgrade de versión | Manual o auto-upgrade channel | Manual (más control, más responsabilidad) | Release channels (Rapid/Regular/Stable) |
| Add-on de ingress | AGIC (App Gateway) o NGINX | AWS Load Balancer Controller | GKE Ingress nativo o Gateway API |

Ya usaste AKS/EKS/GKE en la práctica (MercadoLibre: AWS/GCP con K8s) — este
cuadro es para verbalizar en la entrevista las diferencias que quizás usás
"a mano" sin haberlas puesto en palabras. El posting de Vule es
específicamente sobre **GKE** — repasar la fila de Autopilot con más
profundidad si esa vacante sigue en pie.

## Recursos

- AKS docs: https://learn.microsoft.com/azure/aks/
- EKS docs: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html
- GKE docs: https://cloud.google.com/kubernetes-engine/docs
- Operator pattern: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/

## Autoevaluación

Pedime: *"Dame un examen de Operators/CRDs y diferencias AKS/EKS/GKE"*.
