# Kubernetes — repaso nivel senior

Esta es tu fortaleza (uso en producción de alto volumen en MercadoLibre). El
objetivo acá no es aprender desde cero, sino cerrar huecos específicos que
suelen aparecer en entrevistas senior y no en el uso diario.

## Objetivos (auto-chequeo — si ya dominás esto, saltá directo al examen)

- Scheduling avanzado: affinity/anti-affinity, taints/tolerations, topology spread constraints.
- Resource management: requests vs limits, QoS classes (Guaranteed/Burstable/BestEffort), qué pasa cuando un nodo tiene memory pressure.
- Networking: cómo funciona un Service (ClusterIP/NodePort/LoadBalancer) a nivel de iptables/IPVS, Network Policies, Ingress vs Gateway API.
- Autoscaling: HPA vs VPA vs Cluster Autoscaler — cuándo se pisan entre sí.
- RBAC de Kubernetes (distinto del RBAC de Azure/IAM de AWS/GCP — no confundir en la entrevista, son capas separadas).
- Troubleshooting: `CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff` — causa raíz de cada uno.
- Operators y CRDs (concepto, aunque no hayas escrito uno).
- Diferencias operativas entre AKS, EKS y GKE (lo que ya usaste en AWS/GCP).

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
"a mano" sin haberlas puesto en palabras.

## Recursos

- Kubernetes docs: https://kubernetes.io/docs/home/
- Kubernetes API concepts: https://kubernetes.io/docs/reference/using-api/
- AKS docs: https://learn.microsoft.com/azure/aks/
- EKS docs: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html
- GKE docs: https://cloud.google.com/kubernetes-engine/docs

## Autoevaluación

Pedime: *"Dame un examen de Kubernetes nivel senior/troubleshooting"*.
Este es un buen tema para pedir preguntas **de escenario** ("un pod está en
CrashLoopBackOff, ¿qué revisás primero?") en vez de teóricas puras.
