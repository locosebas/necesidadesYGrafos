# Fase 4: Kubernetes, instalación desde cero y kit de producción

**Objetivo:** operar un clúster propio de grado producción: instalarlo,
completarlo con herramientas, asegurarlo, observarlo y recuperarlo.

Los conceptos de arquitectura (control plane, reconciliation loop, CNI, CSI)
ya están en `../10-kubernetes-avanzado/01-arquitectura-y-cluster.md`. Este
archivo se concentra en lo **práctico**: instalar y equipar el clúster.

**Siglas**: CNI (Container Network Interface) · CSI (Container Storage
Interface) · CRI (Container Runtime Interface) · HPA (Horizontal Pod
Autoscaler) · PDB (PodDisruptionBudget) · CRD (Custom Resource Definition) ·
RBAC (Role-Based Access Control) · mTLS (mutual TLS).

## 1. Formas de instalar Kubernetes

| Opción | Uso | Dificultad |
|---|---|---|
| **kind** (Kubernetes in Docker) | Clústeres en contenedores, pruebas y CI | ⭐ |
| **minikube** | Aprender en tu PC | ⭐ |
| **k3s** | Ligero; producción pequeña, edge, Raspberry Pi | ⭐⭐ |
| **kubeadm** | El "oficial", a mano. **El que más enseña** | ⭐⭐⭐ |
| **Talos Linux / RKE2** | Producción on-prem endurecida | ⭐⭐⭐ |
| **EKS / GKE / AKS** | Gestionado en la nube (Fase 5) | ⭐⭐ |

### Opción rápida 1: kind multinodo

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64 && chmod +x kind && sudo mv kind /usr/local/bin/
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/

cat <<EOF > kind.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF
kind create cluster --name lab --config kind.yaml
kubectl get nodes
```

### Opción rápida 2: k3s en VMs

```bash
# Servidor (control plane)
curl -sfL https://get.k3s.io | sh -
sudo cat /var/lib/rancher/k3s/server/node-token     # token para unir nodos

# Cada worker
curl -sfL https://get.k3s.io | K3S_URL=https://IP_SERVIDOR:6443 K3S_TOKEN=EL_TOKEN sh -
```

## 2. kubeadm con alta disponibilidad, paso a paso (la recomendada para aprender)

**Topología** (reutiliza HAProxy + keepalived de la Fase 1):

```
                 ┌──────────────────────────────┐
                 │ HAProxy + keepalived (VIP)   │  k8s-api.nubeshop.lab:6443
                 └──────┬─────────┬─────────┬───┘
                   cp1  │    cp2  │    cp3  │      ← 3 control planes (con etcd)
                 ───────┴─────────┴─────────┴───
                   w1        w2        w3          ← workers
```

Requisitos: 2 CPU y 2 GB de RAM o más por nodo, hostnames únicos,
conectividad completa entre nodos, puertos 6443, 2379-2380, 10250 abiertos
entre ellos.

### Paso 1: preparar TODOS los nodos

```bash
# 1. Desactivar swap
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# 2. Módulos del kernel y sysctl (lo aprendido en la Fase 1)
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
sudo modprobe overlay && sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system

# 3. Runtime: containerd con driver de cgroups systemd
sudo apt-get update && sudo apt-get install -y containerd apt-transport-https ca-certificates curl gpg
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl restart containerd && sudo systemctl enable containerd

# 4. kubeadm, kubelet, kubectl (cambia v1.34 por la versión estable actual)
K8S=v1.34
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/$K8S/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/$K8S/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update && sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable kubelet
```

> En containerd 2.x el archivo `config.toml` cambió de formato: verifica
> que `SystemdCgroup = true` quedó aplicado (`grep SystemdCgroup /etc/containerd/config.toml`).

### Paso 2: iniciar el primer control plane (cp1)

```bash
sudo kubeadm init \
  --control-plane-endpoint "k8s-api.nubeshop.lab:6443" \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

La salida imprime **dos `kubeadm join`**: uno para control planes (con
`--control-plane --certificate-key ...`) y otro para workers. Guárdalos.

### Paso 3: red de pods (CNI)

Sin CNI los nodos quedan `NotReady`. Recomendado: **Cilium**.

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

helm repo add cilium https://helm.cilium.io && helm repo update
helm install cilium cilium/cilium -n kube-system \
  --set ipam.operator.clusterPoolIPv4PodCIDRList=10.244.0.0/16
kubectl -n kube-system rollout status ds/cilium
```

Alternativa clásica: **Calico** (con el *tigera-operator*).

### Paso 4: unir el resto de nodos

```bash
# cp2 y cp3
sudo kubeadm join k8s-api.nubeshop.lab:6443 --token ... --discovery-token-ca-cert-hash sha256:... \
     --control-plane --certificate-key ...
# w1, w2, w3
sudo kubeadm join k8s-api.nubeshop.lab:6443 --token ... --discovery-token-ca-cert-hash sha256:...

# Si el token expiró
kubeadm token create --print-join-command
```

### Paso 5: verificar

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl run test --image=nginx --restart=Never && kubectl get pod test -o wide
```

### Operación del clúster kubeadm

```bash
# Backup de etcd (en un control plane)
sudo ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-$(date +%F).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Actualizar una versión menor
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.XX.Y       # primer control plane; luego "kubeadm upgrade node" en el resto
kubectl drain NODO --ignore-daemonsets   # antes de actualizar kubelet en cada nodo
kubectl uncordon NODO

# Certificados del control plane
sudo kubeadm certs check-expiration
sudo kubeadm certs renew all
```

## 3. Kit de herramientas de producción

Un Kubernetes recién instalado está **desnudo**: sin balanceador, sin
certificados, sin almacenamiento persistente, sin métricas ni GitOps.

| Capa | Recomendada | Alternativas | Para qué |
|---|---|---|---|
| **Red (CNI)** | **Cilium** | Calico, Flannel | Red de pods, NetworkPolicies, eBPF, visibilidad con Hubble |
| **LoadBalancer on-prem** | **MetalLB** | Cilium LB-IPAM, kube-vip | IPs reales para Services `LoadBalancer` |
| **Entrada HTTP** | **Gateway API** + **Envoy Gateway** o **Traefik** | Cilium Gateway, NGINX Gateway Fabric | Enrutar dominios y rutas. ⚠️ *ingress-nginx* se retiró en 2026: en clústeres nuevos usar Gateway API |
| **Certificados TLS** | **cert-manager** | — | Let's Encrypt o CA interna con renovación automática |
| **Almacenamiento** | **Longhorn** | Rook-Ceph, OpenEBS, local-path, NFS CSI | Volúmenes persistentes replicados |
| **Bases de datos** | **CloudNativePG** | Percona, Zalando | PostgreSQL HA, backups y failover automático |
| **Empaquetado** | **Helm** + **Kustomize** | — | Plantillas y variantes por entorno |
| **GitOps** | **Argo CD** | Flux | Git como fuente de verdad |
| **Métricas** | **metrics-server** + **kube-prometheus-stack** | VictoriaMetrics | `kubectl top`, HPA, Prometheus, Grafana, Alertmanager |
| **Logs** | **Loki** + Grafana Alloy | EFK (Elasticsearch, Fluent Bit, Kibana) | Logs centralizados |
| **Trazas** | **OpenTelemetry** + **Tempo** | Jaeger | Trazabilidad distribuida |
| **Autoescalado** | **HPA**, **KEDA**, **Karpenter** / Cluster Autoscaler | VPA | Escalar pods (CPU, colas, eventos) y nodos |
| **Secretos** | **External Secrets** + Vault/OpenBao | Sealed Secrets, SOPS | Cero secretos en texto plano en Git |
| **Políticas** | **Kyverno** | OPA Gatekeeper | "Prohibido `latest`", "obligatorio limits" |
| **Seguridad** | **Trivy Operator** + **Falco** | Kubescape, kube-bench | CVEs, CIS benchmark, detección en tiempo de ejecución |
| **Service mesh** | **Linkerd** o **Istio** (ambient) | Cilium mesh | mTLS, reintentos, canary, observabilidad L7 |
| **Backups** | **Velero** | Kasten | Respaldo de objetos y volúmenes |
| **Despliegues progresivos** | **Argo Rollouts** | Flagger | Canary y blue/green con análisis automático |
| **Productividad** | **k9s**, kubectx/kubens, stern, Headlamp/Lens, krew | — | Operar con comodidad |

### Instalación del kit base con Helm

```bash
# MetalLB
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb -n metallb-system --create-namespace
cat <<EOF | kubectl apply -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata: { name: pool, namespace: metallb-system }
spec: { addresses: ["10.10.20.200-10.10.20.220"] }
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata: { name: l2, namespace: metallb-system }
EOF

# Gateway API + Envoy Gateway
helm install eg oci://docker.io/envoyproxy/gateway-helm -n envoy-gateway-system --create-namespace

# cert-manager
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager -n cert-manager --create-namespace --set crds.enabled=true

# metrics-server (en laboratorio puede requerir --kubelet-insecure-tls)
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server -n kube-system

# Longhorn (requiere open-iscsi en cada nodo)
helm repo add longhorn https://charts.longhorn.io
helm install longhorn longhorn/longhorn -n longhorn-system --create-namespace

# Observabilidad
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki -n monitoring -f loki-values.yaml   # modo monolítico para laboratorio

# GitOps
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace

# PostgreSQL con operador
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm install cnpg cnpg/cloudnative-pg -n cnpg-system --create-namespace

# Políticas y secretos
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace

# Autoescalado por eventos
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda -n keda --create-namespace

# Backups (requiere bucket S3, ej. MinIO)
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm install velero vmware-tanzu/velero -n velero --create-namespace -f velero-values.yaml
```

💡 Con Argo CD instalado, **reinstala todo lo anterior a través de Argo CD**
(patrón *app of apps*): el clúster entero queda definido en Git.

## 4. Retos de arquitectura

**4.A Clúster HA desde cero**: kubeadm con 3 control planes + 3 workers
detrás del HAProxy + keepalived de la Fase 1.
- Apaga `cp1`: ¿responde la API? ¿Por qué con 3 nodos de etcd toleras perder 1 y no 2?
- Backup de etcd, destruye el clúster y restáuralo.
- Actualiza una versión menor sin caída de las apps.
- Renueva certificados del control plane.

**4.B NubeShop v3 en Kubernetes**:
- Namespaces `nubeshop-dev`, `-staging`, `-prod` con ResourceQuota y LimitRange.
- `frontend` y `api` como Deployments con probes, requests/limits, anti-affinity, PDB y HPA.
- `worker` escalado con **KEDA** según la cola de RabbitMQ (escala a 0).
- **PostgreSQL con CloudNativePG**: 3 instancias, backups continuos a MinIO/S3, PITR.
- Redis y RabbitMQ como StatefulSets o con operador.
- **Gateway API**: `shop.nubeshop.lab` → frontend, `api.nubeshop.lab` → api, TLS con cert-manager.
- **NetworkPolicies** *default deny*: solo la API habla con PostgreSQL.
- Chart de Helm propio + overlays de Kustomize por entorno.

**4.C Plataforma GitOps**:
- Repo `platform/` (todo el kit) y repo `apps/` (NubeShop) con Argo CD (*app of apps* o ApplicationSets).
- Push a `main` → CI construye y firma → actualiza la etiqueta en Git → Argo CD sincroniza.
- **Argo Rollouts**: canary 10 % → 50 % → 100 %, rollback si la tasa de errores en Prometheus supera el 1 %.
- Secretos con External Secrets desde Vault/OpenBao.

**4.D Seguridad y multi-equipo**:
- RBAC: `devs` despliega en `dev` y solo lee `prod`; `ops` es admin; la CI usa una ServiceAccount mínima.
- Kyverno: prohibido `latest`, prohibido root, obligatorios los limits, solo imágenes firmadas de Harbor.
- Pod Security Standards `restricted`; Falco alerta si alguien abre un shell en producción.
- kube-bench (CIS): corrige al menos 10 hallazgos.

**4.E Observabilidad completa**:
- Dashboards de *golden signals*, SLO de 99,9 % con alertas de *burn rate*.
- Loki + Tempo correlacionados: de un error 500 a la traza y a la línea de log.
- Alertas: CrashLoopBackOff, PVC al 80 %, certificado por vencer, nodo `NotReady`, lag de réplica.

**4.F DR del clúster**:
- Velero respaldando en MinIO **fuera** del clúster.
- Destruye el clúster, crea uno nuevo y restaura NubeShop; mide el RTO real.
- ¿Qué recuperas con Velero, qué con GitOps y qué con el backup de CloudNativePG? ¿Dónde se solapan?

**4.G Clúster inmutable con Talos Linux**:
- Segundo clúster con **Talos** (3 control planes + 2 workers), migra NubeShop con Velero o GitOps.
- ¿Cómo diagnosticas un nodo Talos sin SSH (`talosctl`)?
- ¿Cómo actualizas el sistema operativo de 50 nodos sin caída (cordon, drain, PDB, actualizaciones A/B)?

## 5. Preguntas (de a una)

**Conceptos**
1. Paso a paso, ¿qué ocurre desde `kubectl apply -f deploy.yaml` hasta que el contenedor corre?
2. Deployment vs. StatefulSet: ¿cuándo es obligatorio el StatefulSet?
3. ¿Qué pasa si un pod supera su *limit* de memoria? ¿Y el de CPU?
4. Readiness vs. liveness probe: ¿qué desastre causa una liveness mal configurada?
5. ¿Cómo enruta kube-proxy (o Cilium) el tráfico de un Service a los pods?
6. ¿Por qué etcd necesita número impar de nodos?
7. Ingress vs. Gateway API: ¿qué problemas resuelve la segunda?
8. ¿Por qué un Operator es mejor que un StatefulSet a mano para PostgreSQL?
9. ¿Por qué kubeadm exige desactivar swap y cargar `br_netfilter`?
10. ¿Qué pasa si containerd usa `cgroupfs` y kubelet usa `systemd` como driver de cgroups?

**Diagnóstico**
11. Pod en `Pending`: 6 causas y cómo verificar cada una.
12. `CrashLoopBackOff`: tu secuencia exacta de comandos.
13. `ImagePullBackOff` con registry privado: ¿qué falta?
14. El Service no responde aunque los pods están `Running` (selectors, endpoints, readiness, NetworkPolicy).
15. Nodo `NotReady`: ¿qué miras en el nodo? (kubelet, containerd, disco, red: Fase 1.)
16. El HPA no escala: ¿por qué? (metrics-server, requests sin definir.)
17. PVC en `Pending` para siempre: ¿qué revisas?
18. Tras actualizar el clúster los pods se reinician en bucle: plan de rollback.
19. Los nodos quedan `NotReady` justo después de `kubeadm init`: ¿qué olvidaste?

**Diseño**
20. 50 equipos en un clúster: namespaces, cuotas, RBAC, políticas, costes. ¿Cuándo conviene tener varios clústeres?
21. Black Friday: tráfico x20 en 1 hora. Diseña el escalado de pods, nodos, base de datos y caché.
22. ¿PostgreSQL dentro o fuera de Kubernetes? Argumenta ambas posturas.
23. Migración de base de datos incompatible sin caída (patrón *expand/contract*).
24. ¿Cómo garantizas que un nodo comprometido no lea secretos de otros namespaces?
25. ¿Qué gana y qué pierde un clúster con Talos frente a uno con Ubuntu + kubeadm?

✅ **Criterio para pasar de fase:** instalas el clúster con kubeadm, lo
recuperas de la pérdida de un control plane y de etcd, y todo NubeShop se
despliega solo desde Git.
