# Kubernetes — de arquitectura a troubleshooting

Kubernetes es tu fortaleza en el uso diario (producción de alto volumen en
MercadoLibre). Este tema se dividió en varios archivos, en el **orden en el
que conviene estudiarlos** — arquitectura primero, troubleshooting al final:

1. **[`01-arquitectura-y-cluster.md`](01-arquitectura-y-cluster.md)** —
   componentes del control plane y de nodo, el reconciliation loop, cómo se
   arma un clúster (kubeadm vs. managed vs. serverless-node), CNI, CSI.
   **Empezar siempre por acá**, incluso si ya te sentís cómodo con K8s: es
   el vocabulario exacto de arquitectura que se pide a nivel senior/arquitecto.
2. **[`02-scheduling-recursos-autoscaling.md`](02-scheduling-recursos-autoscaling.md)** —
   affinity/taints, requests/limits/QoS, HPA/VPA/Cluster Autoscaler, RBAC de K8s.
3. **[`03-networking-service-mesh.md`](03-networking-service-mesh.md)** —
   Services, Network Policies, Ingress vs. Gateway API, service mesh (Istio).
4. **[`04-operators-crds-managed-k8s.md`](04-operators-crds-managed-k8s.md)** —
   Operators/CRDs, y diferencias operativas entre AKS/EKS/GKE.
5. **[`05-troubleshooting.md`](05-troubleshooting.md)** — `CrashLoopBackOff`,
   `OOMKilled`, `ImagePullBackOff`, orden de diagnóstico, exit codes. **Va
   último a propósito**: con `01`-`04` sólidos, troubleshooting deja de ser
   memorizar comandos sueltos y pasa a ser "entender qué componente falló".

## Por qué este orden (y no ir directo al troubleshooting)

Troubleshooting sin arquitectura es memorizar recetas ("si ves X corré Y").
Con la arquitectura clara, cada síntoma se explica solo: un `OOMKilled` es
el kernel matando el proceso porque superó el **limit** (`02`); un pod que no
arranca puede ser el **scheduler** sin nodo candidato (`01`+`02`) o el
**kubelet** sin poder bajar la imagen (`01`); un servicio inalcanzable puede
ser el **Service/NetworkPolicy** (`03`) o el sidecar de Istio caído (`03`).
Por eso se reordenó: primero construir el modelo mental completo, recién
después practicar diagnóstico de síntomas.

## Estado (2026-10-06/07, ✅ cubierto completo)

Arquitectura, scheduling, networking/mesh y operators ya eran 🟢 Sólido desde
antes. **Troubleshooting** (`05-troubleshooting.md`) se cerró a nivel **🔵
Senior**: mecanismo y exit codes de `CrashLoopBackOff` (proceso cayéndose,
no `Ready`), `OOMKilled` (137, cgroups, sin gracia) vs. **`Evicted`**
(presión de recursos a nivel de todo el nodo — matiz distinguido sin ayuda),
terminación graceful (`SIGTERM`/143) y preemption, e `ImagePullBackOff`
(autenticación a un registry privado vía Managed Identity/IAM Role). Ver
`../../examenes/registro/`.

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

## Cómo pedir examen

Cada archivo tiene su propia sección de Autoevaluación al final — pedime el
examen del archivo específico que acabás de repasar (uno por vez, siguiendo
tu preferencia de a una pregunta).
