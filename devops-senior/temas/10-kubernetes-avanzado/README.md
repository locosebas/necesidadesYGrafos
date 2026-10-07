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

## Herramienta que piden las ofertas (startup): Istio (service mesh)

**Istio** es un **service mesh**: agrega una capa de red entre los servicios
de Kubernetes sin cambiar el código de las apps. Da tres cosas:

1. **Seguridad**: **mTLS** automático entre servicios (cifrado + identidad de cada servicio) y `AuthorizationPolicy` (qué servicio puede hablar con cuál).
2. **Gestión de tráfico**: `VirtualService` y `DestinationRule` para canary releases, retries, timeouts, circuit breaking.
3. **Observabilidad**: métricas y trazas de cada llamada entre servicios (se integra con **OpenTelemetry**, tema 07).

| Concepto | Istio | Azure | AWS | GCP |
|---|---|---|---|---|
| Service mesh | **Istio** (modo *sidecar* con Envoy, o modo **ambient** sin sidecar) | **Istio-based service mesh add-on para AKS** | Istio en EKS (AWS App Mesh fue discontinuado) | **Cloud Service Mesh** (basado en Istio) |

Subtemas extra:
- Sidecar (Envoy) vs. **ambient mode** (ztunnel + waypoint): costo de recursos y complejidad.
- `PeerAuthentication` (mTLS STRICT vs. PERMISSIVE) y `AuthorizationPolicy`.
- Canary con `VirtualService` (por ejemplo, 90/10) — combinable con **ArgoCD** (tema 03) y Argo Rollouts.
- Troubleshooting de **Istio**: `istioctl analyze`, `istioctl proxy-status`, errores 503 típicos.
- Cuándo **no** poner un service mesh (pocos servicios, equipo chico).

- Istio: https://istio.io/latest/docs/

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
