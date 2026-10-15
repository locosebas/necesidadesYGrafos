# Entrevista PayU (Rapid) — 2026-09-22

Notas post-entrevista: preguntas que salieron, respuesta "modelo" para cada
una y autoevaluación. Se va completando a medida que recuerdes más preguntas
(sección [Pendientes de recordar](#pendientes-de-recordar)).

> Complemento: [`herramientas-y-arquitectura.md`](herramientas-y-arquitectura.md)
> — mapa de herramientas por categoría, framework para responder "diseñá una
> arquitectura", arquitectura de referencia de pagos en AWS y plan de práctica.
>
> Práctica: [`preguntas-rapidas.md`](preguntas-rapidas.md) — 57 preguntas con
> respuesta de 1-3 líneas + fórmula para sonar con expertise.

| # | Tema | Cómo me sentí | Tema de estudio relacionado |
|---|---|---|---|
| 1 | Terraform: componentes, buenas prácticas, multi-plataforma, despliegue correcto | Bien | `../01-iac-multicloud/` |
| 2 | Kubernetes: qué componentes se instalan | **Flojo** | `../10-kubernetes-avanzado/` |
| 3 | Troubleshooting: buenas prácticas | — | `../10-kubernetes-avanzado/`, `../07-observabilidad-multicloud/` |
| 4 | AWS multi-cuenta: por qué y cómo | — | `../04-identidad-iam/`, `../12-arquitectura-costos-multicloud/` |
| 5 | CI/CD: qué debe tener sí o sí un pipeline | — | `../03-cicd-multicloud/` |
| 6 | Pipelines para Terraform | — | `../01-iac-multicloud/`, `../03-cicd-multicloud/` |

---

## 1. Terraform

### ¿Qué componentes tiene (o debe tener) un proyecto de Terraform?

**Componentes del lenguaje / herramienta:**

- **Providers**: plugins que hablan con la API de cada plataforma (`aws`,
  `azurerm`, `google`, `kubernetes`, `helm`, `datadog`...). Se fija versión en
  `required_providers` y se bloquea con `.terraform.lock.hcl` (commitearlo).
- **Resources**: lo que se crea (`aws_s3_bucket`, `aws_eks_cluster`...).
- **Data sources**: lo que se *lee* y ya existe (una VPC creada por otro equipo,
  una AMI, el account ID actual).
- **Variables** (`variables.tf`, con `type`, `description`, `validation`,
  `sensitive`), **locals** (valores derivados, naming, tags comunes) y
  **outputs** (lo que se expone a otros módulos/stacks).
- **Modules**: unidades reutilizables y versionadas (red, clúster, base de datos).
- **State**: el mapa entre el código y los recursos reales.
- **Backend remoto** para el state: S3 + lock (DynamoDB, o `use_lockfile` en
  versiones recientes), Azure Storage (lock por blob lease), GCS, o Terraform
  Cloud/HCP. Nunca state local en equipo.

**Estructura típica de repo:**

```
infra/
├── modules/                 # módulos reutilizables, versionados (tags semver)
│   ├── network/
│   ├── eks/
│   └── rds/
└── live/                    # "stacks" que instancian módulos
    ├── dev/
    │   ├── network/  (backend.tf, main.tf, terraform.tfvars)
    │   └── eks/
    ├── staging/
    └── prod/
```

Frase para la entrevista: *"Separo módulos (el qué) de stacks por ambiente (el
dónde), cada stack con su propio state para reducir el blast radius."*

### Buenas prácticas

1. **State remoto, con locking, cifrado y versionado** (S3 con versioning +
   encryption, acceso restringido por IAM). Un state por ambiente y por
   componente (red ≠ clúster ≠ apps): menos blast radius y `plan` más rápido.
2. **Fijar versiones**: `required_version` de Terraform, providers con `~>`,
   módulos por tag (`?ref=v1.4.0`), lock file commiteado.
3. **Módulos pequeños y con interfaz clara** (inputs/outputs documentados);
   no módulos "dios". Nada de valores hardcodeados: todo por variables.
4. **Ambientes aislados**: carpetas/stacks por ambiente o workspaces — en la
   práctica prefiero **carpetas + cuentas separadas** (los workspaces comparten
   backend y credenciales, es fácil equivocarse de ambiente).
5. **Secretos fuera del código**: nada en `.tfvars` commiteados; usar Secrets
   Manager / Key Vault / Vault y marcar variables como `sensitive`. Recordar
   que el state puede contener secretos → proteger el state.
6. **Naming y tagging consistentes** (`default_tags` en el provider de AWS:
   owner, env, cost-center, repo).
7. **Calidad automática**: `terraform fmt`, `terraform validate`, `tflint`,
   escaneo de seguridad (`checkov`, `tfsec`/`trivy config`), policy-as-code
   (OPA/Conftest, Sentinel), estimación de costos (`infracost`).
8. **Protección de recursos críticos**: `lifecycle { prevent_destroy = true }`,
   `deletion_protection` en bases de datos, revisar cualquier `destroy`/
   `replace` en el plan.
9. **Drift detection**: `terraform plan` programado (nightly) que alerte si
   alguien cambió algo "a mano" en la consola.
10. **Refactors seguros**: bloques `moved {}` e `import {}` en vez de
    manipular el state a mano con `terraform state mv`.

### Terraform multi-plataforma (multi-cloud)

- Terraform es **agnóstico de la herramienta, no del recurso**: un
  `aws_eks_cluster` no sirve para GKE. Lo que se reutiliza es el flujo
  (plan/apply, state, módulos, pipeline, políticas), no el código de recursos.
- **Un módulo por nube con una interfaz común** (ej. `module "k8s_cluster"`
  con inputs `name`, `node_count`, `region`) si realmente se necesita
  abstracción; no forzar abstracciones "mínimo común denominador".
- **Providers con alias** para varias regiones/cuentas en el mismo stack
  (`provider "aws" { alias = "us_east_1" }`).
- **States separados por nube** (y por cuenta/suscripción/proyecto).
- **Autenticación sin claves estáticas**: OIDC desde el CI hacia AWS (IAM
  role), Azure (federated credential) y GCP (Workload Identity Federation).
- Herramientas de orquestación cuando crece: **Terragrunt** (DRY de backends
  y dependencias entre stacks), Terraform Cloud/Spacelift/Atlantis.

### ¿Cómo hacer un despliegue correcto con Terraform?

1. Cambio en una **rama** → **Pull Request**.
2. El CI corre `fmt -check`, `validate`, `tflint`, `checkov`/`trivy`,
   `infracost`, y **`terraform plan -out=tfplan`**; publica el plan como
   comentario en el PR.
3. **Revisión humana del plan** (sobre todo `destroy` / `must be replaced`).
4. Merge → `terraform apply tfplan` **del mismo plan guardado** (lo que se
   revisó es lo que se aplica). Promoción **dev → staging → prod**, con
   **aprobación manual** (environment protection) antes de prod.
5. Solo el pipeline tiene permisos de escritura en prod (nadie hace `apply`
   desde su laptop). Concurrencia controlada: un solo `apply` por state a la vez.
6. Post-apply: smoke tests / checks, y drift detection periódico.
7. Rollback = revertir el commit y volver a aplicar (Terraform no tiene
   "rollback" nativo); para cambios riesgosos, `create_before_destroy`.

---

## 2. Kubernetes — ¿qué componentes se instalan? ⚠️ (punto débil)

La respuesta ordenada es por **capas**. Si instalás un clúster "a mano" (ej.
con `kubeadm`) en una máquina:

### a) Prerrequisitos del sistema operativo

- **Deshabilitar swap** (históricamente obligatorio para el kubelet).
- Módulos de kernel `overlay` y `br_netfilter`; sysctl
  `net.ipv4.ip_forward=1` y `net.bridge.bridge-nf-call-iptables=1`.
- Paquetes auxiliares: `conntrack`, `socat`, `iptables`/`ipset`, `ebtables`.
- Puertos abiertos: 6443 (API server), 2379-2380 (etcd), 10250 (kubelet),
  30000-32767 (NodePorts).

### b) Container runtime (en todos los nodos)

- **containerd** (lo más común) o **CRI-O** — implementan la **CRI**.
- **runc** (el runtime de bajo nivel que realmente crea el contenedor).
- Desde Kubernetes 1.24 **ya no se usa Docker Engine directamente**
  (se eliminó *dockershim*); las imágenes de Docker siguen funcionando.
- `crictl` para depurar el runtime.

### c) Binarios de Kubernetes que descargás

- **`kubeadm`**: arma (bootstrap) el clúster (`kubeadm init` / `kubeadm join`).
- **`kubelet`**: agente en cada nodo (corre como servicio systemd).
- **`kubectl`**: CLI cliente.

### d) Control plane (los levanta `kubeadm` como *static pods*)

| Componente | Qué hace |
|---|---|
| **kube-apiserver** | Puerta de entrada; todo pasa por la API (autenticación, autorización, admission). |
| **etcd** | Base clave-valor donde vive **todo** el estado del clúster. Se respalda. |
| **kube-scheduler** | Decide en qué nodo va cada pod (recursos, affinity, taints). |
| **kube-controller-manager** | Loops de reconciliación: Deployments/ReplicaSets, nodos, endpoints, jobs... |
| **cloud-controller-manager** | (Solo en nube) crea load balancers, rutas, volúmenes del cloud provider. |

### e) Componentes de cada worker node

| Componente | Qué hace |
|---|---|
| **kubelet** | Recibe los pods asignados y le pide al runtime que los corra; reporta estado; ejecuta probes. |
| **kube-proxy** | Implementa los Services (reglas iptables/IPVS). Algunos CNIs como Cilium lo reemplazan con eBPF. |
| **Container runtime** | containerd/CRI-O + runc. |

### f) Add-ons "obligatorios en la práctica" (no vienen solos)

- **CNI plugin** — sin él los nodos quedan `NotReady` y CoreDNS en `Pending`:
  **Calico**, **Cilium**, Flannel, Weave; en nube: AWS VPC CNI, Azure CNI.
  También los `cni-plugins` base (bridge, loopback, host-local).
- **CoreDNS** — DNS interno (`mi-svc.mi-ns.svc.cluster.local`). kubeadm lo instala.
- **metrics-server** — necesario para `kubectl top` y para el **HPA**.
- **Ingress controller** (NGINX, Traefik, AWS Load Balancer Controller) o Gateway API.
- **CSI driver** para volúmenes persistentes (EBS CSI, Azure Disk, GCE PD) y StorageClass.
- Opcionales frecuentes: Helm, cert-manager, external-dns, Cluster Autoscaler
  / Karpenter, Prometheus/Grafana, Dashboard.

### g) Si la pregunta es "en mi computador" (desarrollo local)

- **minikube**, **kind** (Kubernetes in Docker), **k3s/k3d**, **Docker Desktop**
  o **Rancher Desktop**. Todos instalan igualmente: un runtime, kubelet, los
  componentes del control plane (en uno o pocos nodos), un CNI simple, CoreDNS
  y `kubectl`.
- En **EKS/AKS/GKE** el control plane lo gestiona el proveedor: vos solo
  gestionás nodos (kubelet + runtime + kube-proxy + CNI del proveedor) y add-ons.

**Respuesta de 30 segundos para la próxima vez:**
> "Instalo un container runtime compatible con CRI —containerd con runc—, y los
> binarios kubeadm, kubelet y kubectl. Con kubeadm init se levanta el control
> plane: kube-apiserver, etcd, scheduler y controller-manager. En cada nodo
> corren kubelet, kube-proxy y el runtime. Después tengo que instalar sí o sí
> un CNI —Calico o Cilium— porque sin él los nodos quedan NotReady; kubeadm
> trae CoreDNS, y agrego metrics-server para HPA, un ingress controller y un
> CSI driver para storage."

---

## 3. Troubleshooting — buenas prácticas

**Metodología (independiente de la tecnología):**

1. **Entender el impacto y el alcance**: ¿qué falla, desde cuándo, a quién
   afecta, todos los usuarios o una región/versión?
2. **¿Qué cambió?** — deploys, cambios de config/infra, feature flags. La
   mayoría de incidentes vienen de un cambio. Si hay impacto: **mitigar primero**
   (rollback, escalar, failover), investigar después.
3. **Observabilidad**: métricas (RED/USE, golden signals: latencia, tráfico,
   errores, saturación) → logs → traces. De lo general a lo particular.
4. **Hipótesis y descarte de a una variable**, de afuera hacia adentro (DNS →
   LB → ingress → service → pod → app → dependencia/DB).
5. **Documentar** en el canal del incidente con timestamps.
6. **Postmortem blameless** con acciones concretas (alerta que faltó, runbook,
   test) para que no se repita.

**En Kubernetes, el flujo concreto:**

```bash
kubectl get pods -n <ns> -o wide              # estado, reinicios, nodo
kubectl describe pod <pod> -n <ns>            # Events: scheduling, pull, probes, OOM
kubectl logs <pod> -n <ns> [-c <container>]   # logs actuales
kubectl logs <pod> -n <ns> --previous         # logs del contenedor que murió
kubectl get events -n <ns> --sort-by=.lastTimestamp
kubectl top pod / kubectl top node            # consumo (requiere metrics-server)
kubectl get endpoints <svc>                   # ¿el Service tiene pods detrás?
kubectl exec -it <pod> -- sh / kubectl debug  # entrar o usar contenedor efímero
```

| Síntoma | Causa típica | Dónde mirar |
|---|---|---|
| `Pending` | Sin recursos, taints, affinity, PVC sin bindear | `describe pod` → Events |
| `ImagePullBackOff` | Nombre/tag mal, registry privado sin `imagePullSecret`/permisos | `describe pod` |
| `CrashLoopBackOff` | La app arranca y muere: config/env faltante, error de código, liveness probe mal configurada | `logs --previous`, exit code |
| `OOMKilled` (exit 137) | Supera el `limits.memory` | `describe pod` → Last State |
| Exit code 1 / 127 / 143 | Error de app / comando no encontrado / SIGTERM | `describe pod` |
| Service no responde | Selector no coincide con labels → endpoints vacíos, readiness fallando, NetworkPolicy | `get endpoints`, `describe svc` |
| Nodo `NotReady` | kubelet caído, CNI, disco/memoria llenos | `describe node`, `journalctl -u kubelet` |

---

## 4. AWS multi-cuenta — por qué y cómo

**¿Por qué?**

- **Blast radius / aislamiento**: la cuenta es el límite de aislamiento más
  fuerte de AWS. Un error o compromiso en dev no toca prod.
- **Seguridad y permisos**: IAM más simple por cuenta; en prod poca gente,
  en dev más libertad.
- **Límites de servicio (quotas)** separados por cuenta: una prueba de carga en
  dev no consume las quotas de prod.
- **Costos**: facturación separada por cuenta → chargeback claro por equipo/ambiente.
- **Compliance** (clave en **pagos / PCI-DSS**, muy relevante para PayU):
  aislar el entorno que procesa datos de tarjeta reduce el alcance de la auditoría.

**¿Cómo?**

- **AWS Organizations** + **Control Tower** (landing zone) o Account Factory
  (incluso con Terraform: AFT).
- **OUs** típicas: `Security` (Log Archive, Audit/Security Tooling),
  `Infrastructure` (Network/Shared Services), `Workloads` (dev/staging/prod
  por separado), `Sandbox`, `Suspended`.
- **SCPs** (Service Control Policies) como guardrails: prohibir desactivar
  CloudTrail, restringir regiones, bloquear usuarios IAM con access keys, etc.
- **IAM Identity Center** (SSO) para humanos, con permission sets; nada de
  usuarios IAM por cuenta.
- **Logging centralizado**: CloudTrail de organización + Config → cuenta Log
  Archive; GuardDuty / Security Hub con cuenta administradora delegada.
- **Red**: Transit Gateway o VPC compartidas (RAM) desde la cuenta de Network.
- **CI/CD**: el pipeline asume un rol por cuenta destino (OIDC → rol en la
  cuenta de tooling → `sts:AssumeRole` a dev/staging/prod).

Equivalentes: Azure → Management Groups + Subscriptions + Azure Policy;
GCP → Organization + Folders + Projects + Org Policies.

---

## 5. CI/CD — qué debe tener sí o sí un pipeline

**CI (en cada PR):**

1. Checkout + build **reproducible** (versiones fijadas, cache de dependencias).
2. **Lint / formato** y análisis estático (SAST: Semgrep, SonarQube, CodeQL).
3. **Tests** unitarios (y de integración) con umbral de cobertura.
4. **Seguridad**: escaneo de dependencias (SCA: Dependabot/Snyk/Trivy),
   **secret scanning** (gitleaks), escaneo de la imagen (Trivy/Grype).
5. **Build del artefacto una sola vez**, versionado (tag = SHA/semver),
   publicado en un registry (ECR/ACR/GAR); opcional SBOM + firma (cosign).

**CD:**

6. **Promoción del mismo artefacto** dev → staging → prod (build once, deploy many).
7. **Aprobaciones / gates** para prod (environments protegidos).
8. **Estrategia de despliegue segura**: rolling, blue/green o canary, con
   health checks y **rollback automático** si fallan métricas.
9. **Smoke tests** post-deploy y notificaciones (Slack).
10. **Credenciales sin secretos estáticos**: OIDC hacia la nube; secretos en
    un vault; principio de mínimo privilegio para el runner.
11. **Trazabilidad**: quién desplegó qué versión, cuándo (auditoría).
    Opcional GitOps (Argo CD / Flux): el cluster se sincroniza con git.

---

## 6. Pipelines para infraestructura con Terraform

```yaml
# GitHub Actions — esquema
on:
  pull_request:   { paths: ["infra/**"] }
  push:           { branches: [main], paths: ["infra/**"] }

permissions: { id-token: write, contents: read, pull-requests: write }

jobs:
  plan:
    steps:
      - checkout
      - configure-aws-credentials (OIDC → rol de solo lectura/plan)
      - terraform fmt -check -recursive
      - terraform init   (backend remoto)
      - terraform validate
      - tflint ; checkov/trivy config ; infracost
      - terraform plan -out=tfplan   → subir como artifact + comentar en el PR
  apply:
    if: push a main
    environment: prod          # aprobación manual requerida
    concurrency: tf-prod       # nunca dos applies sobre el mismo state
    steps:
      - OIDC → rol con permisos de escritura
      - terraform apply tfplan  (el plan revisado, no uno nuevo)
```

Puntos a mencionar:

- **Plan en PR, apply al mergear**; el `apply` usa el plan guardado.
- **Roles distintos** para plan (lectura) y apply (escritura), por cuenta.
- **Matriz por ambiente/stack** y promoción dev → staging → prod.
- **Detectar solo stacks cambiados** (paths filters) en monorepos.
- **Drift detection** programado (`plan -detailed-exitcode`, exit 2 = drift).
- Alternativas: **Atlantis** (plan/apply por comentarios en el PR), Terraform
  Cloud/HCP, Spacelift, env0.

---

## Pendientes de recordar

Otras preguntas de la entrevista que todavía no anotaste. Agregalas acá y
completamos la respuesta modelo:

- [ ] ...

## Qué repasar antes de la próxima entrevista

- [ ] Kubernetes: poder recitar los componentes del control plane y del nodo,
      y el rol del CNI (sección 2). Hacer un clúster con `kind` o `kubeadm`
      en una VM para verlo en la práctica.
- [ ] Kubernetes troubleshooting con escenarios reales (ya estaba pendiente en
      `../../examenes/registro/resultados.md`).
- [ ] AWS Organizations/Control Tower y SCPs: saber dar un ejemplo de SCP.
