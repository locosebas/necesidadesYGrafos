# Scheduling, gestión de recursos y autoscaling

Segundo paso: una vez que entendiste los componentes (`01-arquitectura-y-cluster.md`),
esto es cómo el **scheduler** y los **controllers** deciden dónde y cuántas
copias de cada cosa corren.

## Objetivos

- Scheduling avanzado: affinity/anti-affinity, taints/tolerations, topology spread constraints.
- Resource management: requests vs. limits, QoS classes (Guaranteed/Burstable/BestEffort), qué pasa cuando un nodo tiene memory pressure.
- Autoscaling: HPA vs. VPA vs. Cluster Autoscaler — cuándo se pisan entre sí.
- RBAC de Kubernetes (distinto del RBAC de Azure/IAM de AWS/GCP — no confundir en la entrevista, son capas separadas).

## Scheduling avanzado

- **Node affinity/anti-affinity**: preferencia o requisito de que un pod vaya (o no vaya) a nodos con ciertas labels.
- **Pod affinity/anti-affinity**: un pod quiere estar cerca (o lejos) de otros pods — ej.: no poner dos réplicas del mismo servicio en el mismo nodo.
- **Taints/tolerations**: un nodo se "ensucia" (taint) para rechazar pods por default; solo los pods con la "tolerancia" correspondiente pueden ir ahí (ej.: nodos con GPU reservados).
- **Topology spread constraints**: repartir pods de forma pareja entre zonas de disponibilidad/nodos, sin ser tan rígido como affinity.

## Resource management

- **Requests**: lo que el scheduler garantiza reservar para el pod (usado para decidir en qué nodo entra).
- **Limits**: el techo — si el pod lo supera en CPU se lo throttlea, si lo supera en memoria se lo mata (`OOMKilled`).
- **QoS Classes** (se calculan solas según requests/limits):
  - **Guaranteed**: requests == limits en CPU y memoria — el último en ser desalojado.
  - **Burstable**: tiene requests pero limits distintos (o solo en un recurso).
  - **BestEffort**: sin requests ni limits — el primero en ser desalojado bajo presión de memoria.

## Autoscaling: quién hace qué

| Mecanismo | Qué escala | Basado en |
|---|---|---|
| **HPA** (Horizontal Pod Autoscaler) | Número de réplicas de un pod | CPU/memoria, o métricas custom/externas (con KEDA, eventos) |
| **VPA** (Vertical Pod Autoscaler) | Requests/limits de un pod existente | Historial de uso real |
| **Cluster Autoscaler** | Número de **nodos** del clúster | Pods que no entran por falta de capacidad (pending) |

**Dónde se pisan**: HPA y VPA sobre el mismo pod pueden entrar en conflicto
(HPA quiere más réplicas iguales, VPA quiere réplicas más grandes) — no se
recomienda combinarlos sobre el mismo recurso sin cuidado. Cluster Autoscaler
reacciona *después* de que HPA ya pidió más pods y no entraron.

## RBAC de Kubernetes

- Objetos: **Role**/**ClusterRole** (qué se puede hacer) + **RoleBinding**/**ClusterRoleBinding** (quién puede hacerlo).
- Scope: `Role` es por namespace, `ClusterRole` es todo el clúster.
- **No es lo mismo** que el RBAC de Azure, las IAM Policies de AWS o el Cloud IAM de GCP (tema 04) — son capas completamente separadas: una autoriza sobre la API de Kubernetes, la otra sobre la API de la nube. Un Service Account de Kubernetes puede además tener una identidad de nube asociada (Workload Identity/IRSA) — ahí es donde se cruzan las dos capas.

## Recursos

- Assigning Pods to Nodes: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
- Resource Management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- HPA: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- RBAC: https://kubernetes.io/docs/reference/access-authn-authz/rbac/

## Autoevaluación

Pedime: *"Dame un examen de scheduling/recursos/autoscaling de Kubernetes nivel senior"*.
