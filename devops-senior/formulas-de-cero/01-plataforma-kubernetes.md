# Fórmula 01 — Plataforma Kubernetes de cero a que funcione

**Resumen en una línea:** *requisitos → red → clúster gestionado con IaC →
add-ons base → GitOps → multi-tenancy y seguridad → CI/CD de apps →
observabilidad → resiliencia y costos → golden path → prueba end-to-end.*

---

## Paso 0 — Requisitos (preguntalos en voz alta)

- ¿Cuántos equipos/servicios? ¿Multi-tenant (varios equipos en un clúster)?
- ¿Tipo de carga? (APIs stateless, jobs batch, stateful, GPU).
- ¿SLO / disponibilidad? → define multi-AZ, multi-región, número de clústeres.
- ¿Nube o on-prem? ¿Compliance? ¿Presupuesto?
- ¿Cuántos clústeres? Regla típica: **uno por entorno** (dev / stg / prod),
  como mínimo prod separado. Más clústeres = más aislamiento, más costo operativo.

## Paso 1 — Fundaciones: cuenta + red

- Cuenta/suscripción/proyecto dedicado por entorno (ver fórmula 06).
- **VPC/VNet** con subnets **privadas** para nodos en ≥ 3 zonas de disponibilidad.
- Salida a internet por **NAT Gateway** (los nodos no tienen IP pública).
- **Planificá IPs para pods** (el error clásico):
  - EKS con VPC CNI: cada pod consume una IP de la VPC → subnets grandes
    o *prefix delegation*.
  - AKS: **Azure CNI Overlay** (pods en un CIDR aparte, no gasta IPs de la VNet).
  - GKE: VPC-native con **rangos secundarios** para pods y services.
- DNS privado, y si hay on-prem, que los CIDR **no se solapen**.

## Paso 2 — El clúster (siempre gestionado y con IaC)

- **EKS / AKS / GKE** con Terraform (fórmula 03). No armes control plane a
  mano salvo que sea on-prem (ahí: kubeadm, Rancher/RKE2, OpenShift).
- Endpoint de la API **privado** o restringido por IP.
- Versión soportada + estrategia de upgrade (release channels en GKE,
  auto-upgrade channel en AKS, manual en EKS).
- **Node pools separados:**
  - *system pool* (CoreDNS, add-ons) con taint `CriticalAddonsOnly`.
  - *user pools* para apps, uno de **spot/preemptible** para cargas tolerantes.
- Autoscaling de nodos: **Cluster Autoscaler** o **Karpenter** (EKS),
  node auto-provisioning (GKE), o modo sin nodos (GKE Autopilot, EKS Auto Mode).
- Cifrado de Secrets de K8s con **KMS** (envelope encryption).
- Logs de auditoría del control plane activados.

## Paso 3 — Add-ons base (la "plataforma" en sí)

| Necesidad | Add-on típico |
|---|---|
| Red de pods + NetworkPolicy | CNI de la nube + **Cilium** o Calico |
| Métricas para HPA | **metrics-server** |
| Entrada HTTP(S) | **Gateway API** (recomendado) o un Ingress controller (AWS LB Controller, AGIC, GKE Ingress, Traefik…). *ingress-nginx de la comunidad fue retirado en 2026 → no lo elijas para algo nuevo.* |
| Certificados TLS | **cert-manager** + Let's Encrypt / CA interna |
| Registros DNS automáticos | **external-dns** |
| Almacenamiento | CSI driver (EBS/Azure Disk/PD) + `StorageClass` por defecto |
| Identidad pod → nube | **IRSA / EKS Pod Identity**, **AKS Workload Identity**, **GKE Workload Identity** |
| Secretos | **External Secrets Operator** o Secrets Store CSI → Key Vault / Secrets Manager |
| Políticas | **Kyverno** u OPA **Gatekeeper** |
| Backups | **Velero** |

## Paso 4 — GitOps (cómo se instala todo lo anterior y las apps)

- **Argo CD** (o Flux) instalado por Terraform/Helm como único bootstrap manual.
- Repo `platform-gitops/` con patrón **app-of-apps** / ApplicationSets:
  add-ons de plataforma versionados, un directorio por clúster/entorno.
- Nada se aplica con `kubectl apply` a mano: **Git es la fuente de verdad**,
  Argo detecta y corrige el drift.

## Paso 5 — Multi-tenancy y seguridad (lo que diferencia a un senior)

Por cada equipo:

1. **Namespace** propio (`team-pagos-prod`).
2. **RBAC**: `RoleBinding` a **grupos del IdP** (Entra ID / IAM Identity
   Center / Google Groups), nunca a usuarios sueltos.
3. **ResourceQuota** (tope de CPU/mem del namespace) + **LimitRange**
   (requests/limits por defecto).
4. **NetworkPolicy default-deny** y abrir solo lo necesario.
5. **Pod Security Admission** en nivel `restricted`
   (sin root, sin privileged, sin hostPath).
6. Políticas de Kyverno: imágenes solo del registry corporativo, firmadas,
   con `requests/limits` y labels obligatorias.

Recordá: **RBAC de Kubernetes ≠ IAM de la nube**. Son dos capas: IAM decide
quién llega a la API del clúster; RBAC de K8s decide qué puede hacer adentro.

## Paso 6 — CI/CD de las aplicaciones

```
push → CI: test → build imagen → scan (Trivy) → firma (cosign) → push al registry
     → CI actualiza el tag en el repo GitOps (Helm values / Kustomize)
     → Argo CD sincroniza → (opcional) Argo Rollouts: canary con análisis de métricas
```

- Imágenes **inmutables** (tag = SHA del commit, nunca `latest`).
- Autenticación de CI a la nube con **OIDC**, sin claves (fórmula 04).

## Paso 7 — Observabilidad

- **kube-prometheus-stack** (Prometheus + Alertmanager + Grafana) o el
  servicio gestionado (Managed Prometheus en AWS/Azure/GCP).
- Logs: **Fluent Bit** → Loki / CloudWatch / Log Analytics / Cloud Logging.
- Trazas: **OpenTelemetry** Collector → Tempo / X-Ray / App Insights / Cloud Trace.
- Alertas sobre **SLOs** de las apps + salud de plataforma (nodos NotReady,
  pods en CrashLoop, certificados por vencer, PVC llenos).

## Paso 8 — Resiliencia

- Cada Deployment: `requests/limits`, **readiness + liveness probes**,
  `replicas ≥ 2`, **PodDisruptionBudget**, **topologySpreadConstraints** por zona.
- **HPA** para pods, Cluster Autoscaler/Karpenter para nodos.
  (Ojo: HPA y VPA sobre la misma métrica de CPU/mem se pisan.)
- Backups con Velero + **prueba de restore**.
- Upgrades: primero dev → stg → prod; node pools con surge; para cambios
  grandes, **blue/green de clúster**.

## Paso 9 — Costos

- Requests bien dimensionados (el scheduler reserva por *requests*, no por uso).
- Spot para cargas tolerantes, **OpenCost/Kubecost** para costo por namespace/equipo.
- Labels obligatorias `team`, `env`, `cost-center`.

## Paso 10 — Golden path (developer experience)

- Template de servicio (repo con Dockerfile, chart Helm, pipeline, dashboards).
- Portal tipo **Backstage** opcional.
- Documentación: "cómo desplegar tu primer servicio en 15 minutos".

---

## Prueba "funciona" (lo último que decís)

Manifiesto mínimo que demuestra que la plataforma entera anda:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: hello, namespace: team-demo, labels: { app: hello, team: demo } }
spec:
  replicas: 2
  selector: { matchLabels: { app: hello } }
  template:
    metadata: { labels: { app: hello, team: demo } }
    spec:
      securityContext: { runAsNonRoot: true }
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector: { matchLabels: { app: hello } }
      containers:
        - name: hello
          image: registry.empresa.com/hello:3f9c2a1   # tag = SHA, nunca latest
          ports: [{ containerPort: 8080 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { memory: 256Mi }
          readinessProbe: { httpGet: { path: /healthz, port: 8080 } }
          livenessProbe:  { httpGet: { path: /healthz, port: 8080 }, initialDelaySeconds: 10 }
---
apiVersion: v1
kind: Service
metadata: { name: hello, namespace: team-demo }
spec: { selector: { app: hello }, ports: [{ port: 80, targetPort: 8080 }] }
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: hello, namespace: team-demo }
spec: { minAvailable: 1, selector: { matchLabels: { app: hello } } }
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: hello, namespace: team-demo }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: hello }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny, namespace: team-demo }
spec: { podSelector: {}, policyTypes: [Ingress, Egress] }
```

(Además: una `HTTPRoute`/`Ingress` con TLS de cert-manager, y NetworkPolicies
que permitan el tráfico del gateway y el DNS a CoreDNS.)

Checklist de validación:

```bash
kubectl get nodes -o wide                 # nodos Ready, en 3 zonas
kubectl -n team-demo get pods,svc,hpa,pdb # pods Running, HPA leyendo métricas
kubectl -n team-demo describe pod <pod>   # eventos: sin FailedScheduling
curl -I https://hello.empresa.com         # 200 con certificado válido
kubectl auth can-i create deploy -n team-otro --as=<usuario-demo>  # debe ser "no"
```

+ ver el pod en Grafana, sus logs en el backend de logs, y matar un pod para
confirmar que se recrea y que la alerta dispara.

## Troubleshooting que te van a preguntar

| Síntoma | Causa típica | Primer comando |
|---|---|---|
| `Pending` | Faltan recursos, taints sin toleration, PVC sin bind, affinity imposible | `kubectl describe pod` → Events |
| `CrashLoopBackOff` | La app arranca y muere (config, env faltante, error de código, liveness muy agresiva) | `kubectl logs <pod> --previous` |
| `OOMKilled` | Superó el **limit** de memoria | `describe` → Last State; subir limit o arreglar leak |
| `ImagePullBackOff` | Tag inexistente, registry privado sin credenciales/permiso | `describe` → Events |
| Service no responde | Selector no matchea labels, readiness falla, NetworkPolicy bloquea | `kubectl get endpoints <svc>` |
| DNS falla | CoreDNS caído o NetworkPolicy sin egress a puerto 53 | `kubectl run -it --rm debug --image=busybox -- nslookup kubernetes` |
