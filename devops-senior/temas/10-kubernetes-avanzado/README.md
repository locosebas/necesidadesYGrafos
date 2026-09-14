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

## Recursos generales

- Kubernetes docs: https://kubernetes.io/docs/home/
- Kubernetes API concepts: https://kubernetes.io/docs/reference/using-api/

## Cómo pedir examen

Cada archivo tiene su propia sección de Autoevaluación al final — pedime el
examen del archivo específico que acabás de repasar (uno por vez, siguiendo
tu preferencia de a una pregunta).
