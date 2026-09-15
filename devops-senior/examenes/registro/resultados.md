# Registro de resultados

| Fecha | Tema | Nivel | Formato | % Aciertos | Puntos débiles detectados |
|---|---|---|---|---|---|
| 2026-09-08 | Diagnóstico general (12 temas, tema 13 MELI excluido) | Panorama | Preguntas abiertas, de a una | ~5/12 sólidas, 2/12 parciales, 5/12 débiles | IAM/Managed Identity, consistencia de bases NoSQL, Durable Functions (activity/orchestrator), Kubernetes troubleshooting, DevSecOps/shift-left |
| 2026-09-14/15 | Kubernetes — arquitectura (`10-kubernetes-avanzado/01-arquitectura-y-cluster.md`) | Fundamentos, desde cero | Guiado, de a una pregunta | Base real de partida: no conocía Kubernetes más allá de "un motor de contenedores ordenado" (confundía con Docker). Al cierre: entendió correctamente las 7 piezas del clúster (kube-apiserver, etcd, kube-scheduler, kube-controller-manager, kubelet, kube-proxy, container runtime), el reconciliation loop, y las 3 formas de levantar un clúster (kubeadm/managed/serverless-node) | Ninguno pendiente de este archivo — completado en la sesión |
| 2026-09-14/15 | Entrevista real (EY) — feedback | — | Feedback post-entrevista, no autoevaluación | Se trabó en 2 preguntas reales: tipos de Load Balancer de AWS (ALB/NLB/GWLB) y Kubernetes Pod en estado `Pending`. Ambos repasados en la sesión | AWS Load Balancers: revisar con examen formal más adelante (`temas/02-contenedores-serverless`/`temas/05-networking-multicloud`) |

**Fortalezas confirmadas en el diagnóstico:** IaC (Terraform/Bicep), CI/CD +
OIDC, Networking (Private Endpoint + DNS privado), FastAPI async/await,
Well-Architected trade-offs (buen ejemplo propio con HPA).

> Se completa cada vez que rendís un examen de autoevaluación. Pedime que lo
> actualice al terminar un examen, o hacelo vos mismo siguiendo el formato.

## Pendientes de profundización (retomar después)

- **Durable Functions — `activity` vs. `orchestrator`**: entendido el mecanismo
  de `replay`/determinismo en general, pero el rol específico de una
  `activity` (por qué no se repite en el replay) quedó para repasar con más
  ejemplos. Ver `../../temas/09-orquestacion-serverless/`.
- **Kubernetes — troubleshooting (`CrashLoopBackOff`, `OOMKilled`, exit codes)**:
  tema declarado como no manejado (nunca lo hizo en la práctica). Ver
  `../../temas/10-kubernetes-avanzado/05-troubleshooting.md` — sesión dedicada
  con varios escenarios de `describe pod`/`logs --previous`/exit codes
  reales. **Reordenado (2026-09-14)**: antes de esta sesión, repasar primero
  `01-arquitectura-y-cluster.md` a `04-operators-crds-managed-k8s.md` del
  mismo tema (arquitectura del clúster) — ver `../../00-diagnostico/roadmap.md`,
  troubleshooting pasó a la Fase 8.
- **Identidad — Managed Identity system-assigned vs. user-assigned**: no lo
  tenía claro (adivinó), quedó explicado pero conviene repasar con ejemplo
  práctico. Ver `../../temas/04-identidad-iam/`.
- **Consistencia de bases NoSQL (Cosmos DB/DynamoDB/Firestore)**: no conocía
  el concepto de "nivel de consistencia" en absoluto. Ver `../../temas/06-datos-secretos/`.
- **DevSecOps / "shift-left"**: no conocía el término ni herramientas como
  **Trivy**; el concepto general de seguridad temprana sí, pero la
  terminología específica no. Ver `../../temas/11-seguridad-devsecops/`.

## Ronda de vocabulario pendiente

El usuario pidió una ronda rápida de repaso de términos/nombres de
herramientas (sin conceptos nuevos) una vez cerrado el diagnóstico general —
pendiente de hacer.
