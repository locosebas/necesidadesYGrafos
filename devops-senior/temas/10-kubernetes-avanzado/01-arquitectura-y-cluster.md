# Arquitectura de Kubernetes y cómo se arma un clúster

Punto de partida real del tema: antes de trouble-shootear hay que saber qué
hay debajo de un pod. Este archivo va primero — incluso si ya usaste
Kubernetes en producción (MercadoLibre), es para tener el vocabulario exacto
de **arquitectura** que se pide en una entrevista de nivel arquitecto, no
solo el uso diario.

## Objetivos

- Nombrar y explicar el rol de cada componente del control plane y de cada nodo.
- Explicar el ciclo de vida de un objeto (manifest → API server → etcd → controller → kubelet) — el "reconciliation loop", la idea central de todo Kubernetes.
- Diferenciar quién gestiona qué en self-managed (kubeadm) vs. managed (AKS/EKS/GKE) vs. serverless-node (GKE Autopilot/Fargate profiles).
- Explicar el modelo de red de Kubernetes (CNI) y de storage (CSI) a alto nivel.

## Control plane (el "cerebro" del clúster)

| Componente | Qué hace |
|---|---|
| **kube-apiserver** | Única puerta de entrada: valida y persiste cambios; todo (kubectl, controllers, kubelets) habla con el clúster a través de él, nunca directo a etcd |
| **etcd** | Base de datos clave-valor distribuida donde vive el estado completo del clúster (la "fuente de la verdad") |
| **kube-scheduler** | Decide en qué nodo va cada pod nuevo (según requests/limits, afinidad, taints/tolerations) |
| **kube-controller-manager** | Corre los "reconciliation loops" (Deployment controller, ReplicaSet controller, Node controller, etc.) — compara estado deseado vs. real y corrige |
| **cloud-controller-manager** | Traduce objetos de K8s a recursos de la nube (un Service tipo LoadBalancer → un Load Balancer real de Azure/AWS/GCP) |

## Componentes de nodo (worker)

| Componente | Qué hace |
|---|---|
| **kubelet** | Agente en cada nodo; le habla al api-server y garantiza que los contenedores que le tocan estén corriendo |
| **kube-proxy** | Implementa las reglas de red de los Services (iptables/IPVS) en cada nodo |
| **Container runtime (CRI)** | Quien realmente crea/corre los contenedores — containerd o CRI-O (Docker Engine ya no se usa como runtime nativo desde K8s 1.24+) |

## El "reconciliation loop" (idea central de todo Kubernetes)

1. Aplicás un manifest (`kubectl apply -f deployment.yaml`) → va al **api-server**.
2. El api-server valida y lo guarda en **etcd** como "estado deseado".
3. El **controller-manager** nota la diferencia entre deseado y real, y crea los objetos que faltan (ej.: Deployment → crea ReplicaSet → crea Pods).
4. El **scheduler** asigna cada Pod nuevo a un nodo.
5. El **kubelet** de ese nodo ve que le asignaron un Pod y le pide al **container runtime** que lo corra.
6. Todo el tiempo, todos los componentes vuelven a comparar deseado vs. real — así se recupera solo un pod que muere (esto es la base de por qué un `CrashLoopBackOff` se reintenta solo).

## Cómo se levanta un clúster

| Método | Quién gestiona el control plane | Cuándo se usa |
|---|---|---|
| **kubeadm** | Vos (self-managed, on-prem o VMs propias) | Aprender de verdad cómo se arma un clúster, o requisito de no usar nube gestionada |
| **AKS / EKS / GKE (Standard)** | La nube gestiona el control plane; vos gestionás los nodos (VMs) | La mayoría de los casos productivos |
| **GKE Autopilot / Fargate profiles / ACA** | La nube gestiona control plane Y nodos (no ves VMs) | Cero mantenimiento de nodos — el modo más usado al construir una plataforma self-service |

## Networking: CNI (Container Network Interface)

- Kubernetes no trae red propia — delega en un **plugin CNI** (Calico,
  Cilium, Azure CNI, VPC CNI de AWS) que le da IP a cada pod y conecta los
  nodos entre sí.
- Dos redes distintas, no confundir: **red de pods** (cada pod tiene su
  propia IP) y **red de Services** (IPs virtuales estables, resueltas por
  kube-proxy vía iptables/IPVS).
- **Cilium** es el CNI más mencionado hoy porque además puede reemplazar
  kube-proxy con eBPF (más rápido) y hacer de service mesh liviano — se
  conecta con `03-networking-service-mesh.md` (Istio) de este mismo tema.

## Storage: CSI (Container Storage Interface)

- Igual que CNI pero para disco: un **plugin CSI** conecta Kubernetes con el
  storage real de la nube (Azure Disk/Files, EBS/EFS, Persistent Disk).
- Objetos clave: **PersistentVolume (PV)** (el disco real), **PersistentVolumeClaim (PVC)** (el pedido de un pod), **StorageClass** (la "receta" para crear un PV dinámicamente).

## API y objetos: la base de todo

- Todo en Kubernetes es un objeto con `apiVersion`, `kind`, `metadata`,
  `spec` (deseado) y `status` (real, lo llena el controller).
- **CRD (Custom Resource Definition)**: le enseña al api-server un `kind`
  nuevo que no viene de fábrica.
- **Operator**: un controller custom que reconcilia un CRD — el patrón para
  "enseñarle" a Kubernetes a operar algo con lógica propia (ej.: un operador
  de PostgreSQL que sabe hacer failover). Detalle en `04-operators-crds-managed-k8s.md`.

## Recursos

- Kubernetes Components: https://kubernetes.io/docs/concepts/overview/components/
- kubeadm: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/
- CNI spec: https://github.com/containernetworking/cni
- Cilium: https://cilium.io/
- CSI: https://kubernetes-csi.github.io/docs/

## Lab sugerido

Levantá un clúster local de un solo nodo (kind o minikube) y compará con uno
armado a mano con **kubeadm** (en VMs o contenedores). Anotá qué tuviste que
instalar/configurar vos que en AKS/EKS/GKE viene gestionado por la nube.

## Autoevaluación

Pedime: *"Dame un examen de arquitectura de Kubernetes (componentes y cómo se arma un clúster)"*.
