# Gorilla Logic · Senior Platform DevOps (assessment de Canditech + entrevista técnica)

Proceso con **Gorilla Logic**: llamada con la reclutadora (3 nov, posición "DevOps GCP"), assessment de
Canditech (4 nov) y **Technical Screening con Carlos Suárez el 11 nov 2026, 4:30–6:00 pm**. Consejo de
la reclutadora: ser uno mismo, no leer una presentación y contar la experiencia real.

## Presentación de repaso

- [diagramas-c4.md](diagramas-c4.md): 16 diagramas C4 con íconos.
- [libreto-diapositivas.md](libreto-diapositivas.md): las 25 diapositivas con el guion en inglés.
- [presentacion.html](presentacion.html): la presentación (← → para navegar, **N** para ver el guion).
  Versión para el celular (privada): https://claude.ai/artifact/JwP9oCmUxaMm9UeUEryaqE.
  Se regenera con `python3 generar_presentacion.py`.

## Prueba técnica (assessment)

Entrenamiento/prueba técnica resuelto el 4 nov 2026. Rol: Senior DevOps / Platform Engineer sobre AWS
(Amazon Web Services), EKS (Elastic Kubernetes Service), Terraform y GitOps con Argo CD. Mezcla
respuestas escritas en texto plano y videos cortos (30–60 segundos) respondiendo a stakeholders.

Los enunciados están resumidos con mis palabras; las respuestas son las que preparé para pegar o grabar.

| # | Bloque | Tema | Archivo |
|---|---|---|---|
| 1 | E-commerce en AWS (campaña de marketing con 4x tráfico) | Lentitud, latencia en Asia, caída en cascada del payment service | [01-ecommerce-escalado.md](01-ecommerce-escalado.md) |
| 2 | SaaS en EKS con Terraform | Revisión de `terraform plan`, state lock huérfano, drift por cambio de emergencia, stakeholder pidiendo `-auto-approve` (video) | [02-terraform-produccion.md](02-terraform-produccion.md) |
| 3 | Incidente en EKS tras un sync de Argo CD | Nota de incidente (503 + IP exhaustion), cambios en vivo fuera de GitOps (video), rollback vs investigar (video) | [03-incidente-eks-argocd.md](03-incidente-eks-argocd.md) |
| 4 | Canary con progressive delivery | Primeras 4 acciones, hot-fix directo (video), rollback vs roll-forward con migración de base de datos (video) | [04-canary-gitops.md](04-canary-gitops.md) |
| 5 | Herramienta interna `platformctl` en Python | 4 problemas del script, diseño de CLI v2, restart amplio en producción (video) | [05-platformctl.md](05-platformctl.md) |

## Nombres clave para repasar

- **Escalado:** HPA (Horizontal Pod Autoscaler), Cluster Autoscaler / Karpenter, Four Golden Signals.
- **Latencia geográfica:** CDN (Content Delivery Network) → CloudFront + S3, Global Accelerator, Route 53 latency-based routing.
- **Resiliencia:** cascading failure, circuit breaker, bulkhead, timeouts + retries con backoff y jitter, cola (SQS/Kafka), idempotency keys, DLQ (Dead Letter Queue), Saga.
- **Terraform:** `moved` block, `terraform state mv`, `prevent_destroy`, `errored.tfstate`, `force-unlock`, `plan -refresh-only`, `import` block, SIGINT, drift detection, policy-as-code (OPA/Conftest, Checkov, Sentinel).
- **EKS:** VPC CNI e IP exhaustion, `target-type: instance` necesita NodePort (no ClusterIP).
- **GitOps:** Argo CD self-heal, Argo Rollouts abort, image digest vs tag mutable, ECR tag immutability.
- **Bases de datos:** rollback vs roll-forward, expand-contract (parallel change).
- **CLI segura:** dry-run por defecto, Eviction API + PodDisruptionBudgets, exit codes documentados, `--output json`, stdout vs stderr.
