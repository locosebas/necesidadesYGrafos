# Entrevista DevOps — 2026-11-04 (mañana)

Preguntas que envió el reclutador para preparar. La entrevista es en
**inglés**, así que cada pregunta tiene: **respuesta modelo en inglés** (para
decirla en voz alta, 30-90 segundos) + **notas en español** con los puntos
clave que no pueden faltar.

| # | Pregunta | Bloque | Tu nivel previo (`progreso.md`) | Material relacionado |
|---|---|---|---|---|
| 1 | Experience in Kubernetes | Kubernetes | 🟢 (experiencia real) | `../../presentacion-experiencia/` |
| 2 | Tool for orchestration | Kubernetes | 🟢 | `../10-kubernetes-avanzado/` |
| 3 | Kubernetes architecture | Kubernetes | 🟢 Sólido (#1) | `../10-kubernetes-avanzado/` |
| 4 | Master node (control plane) components | Kubernetes | 🟢 Sólido (#1) | `../29-entrevista-payu/` (salió flojo allá) |
| 5 | Rate yourself in Jenkins | Jenkins | 🟢 (experiencia real, #21) | `../03-cicd-multicloud/` |
| 6 | Disk full but `du` shows low usage | Linux | sin examen dedicado | `../27-linux-distros-infraestructura/` |
| 7 | "Too many open files" error | Linux | sin examen dedicado | `../27-linux-distros-infraestructura/` |
| 8 | S3 bucket versioning not enabling | AWS | sin examen dedicado | `../06-datos-secretos/` |
| 9 | `AccessDenied ... sts:AssumeRole` | AWS IAM | 🟡/🟢 (#25, #27) | `../04-identidad-iam/` |
| 10 | What is a Pod? | Kubernetes | 🟢 | `../10-kubernetes-avanzado/` |
| 11 | How to create a Pod | Kubernetes | 🟢 | `../10-kubernetes-avanzado/` |
| 12 | Purpose of `kubectl` | Kubernetes | 🟢 | — |
| 13 | Master and worker in Jenkins | Jenkins | sin examen dedicado | `../03-cicd-multicloud/` |

> Ojo: en el correo dice "cubs kubectl" — es un error de tipeo, se refiere a
> **`kubectl`** (se pronuncia "kube-control", "kube-C-T-L" o "kube-cuttle").

**Fórmula para troubleshooting (preguntas 6–9):** nunca saltar a la solución.
Decir en voz alta: **1) confirmar el síntoma → 2) hipótesis más probable →
3) comando para comprobarla → 4) arreglo → 5) prevención (monitoreo/IaC)**.
Eso es lo que distingue a un senior de alguien que se sabe el comando.

---

## 1. Tell me about your experience in Kubernetes

**Model answer (EN):**
> I've worked with Kubernetes for several years in two different contexts.
> First, at [empresa Azure], I managed Kubernetes on Azure — AKS (Azure
> Kubernetes Service) — together with the CI/CD (Continuous Integration /
> Continuous Delivery) pipelines in Azure Pipelines and Jenkins that deployed
> to it. Then at Mercado Libre I was part of the compute team of the internal
> PaaS (Platform as a Service): Kubernetes and AWS ECS (Elastic Container
> Service) were the main compute platforms, with infrastructure on AWS and GCP
> provisioned with Terraform. There I wrote Kubernetes operators in Go and
> Python, handled day-to-day troubleshooting — CrashLoopBackOff, OOMKilled,
> evictions, scheduling issues — and supported Mercado Pago, which is a
> regulated banking environment, so security and reliability were critical.

**Notas:** estructura **contexto → qué hacías → algo diferenciador
(operadores en Go) → resultado/impacto**. Si te preguntan "¿qué es un
Operator?": un **Operator** = CRD (Custom Resource Definition) + un
controlador propio que ejecuta un *reconciliation loop* para un recurso
de dominio. Ten listo **un incidente concreto** contado en 4 frases
(síntoma, diagnóstico, arreglo, prevención).

## 2. What tool do you use for orchestration?

**Model answer (EN):**
> For container orchestration, mainly Kubernetes — managed versions like AKS,
> EKS (Elastic Kubernetes Service) and GKE (Google Kubernetes Engine) — and
> also AWS ECS for simpler workloads. On top of Kubernetes I use Helm for
> packaging and GitOps tools like Argo CD for deployments. For pipeline
> orchestration, Jenkins and Azure Pipelines; and for infrastructure,
> Terraform.

**Notas:** "orchestration" es ambiguo → **cubre los tres sentidos**:
contenedores (**Kubernetes**, **ECS**), despliegue/pipelines (**Jenkins**,
**Argo CD**), infraestructura (**Terraform**). Solo menciona Argo CD/Helm si
puedes sostener una repregunta.

## 3. Do you know about the architecture in Kubernetes?

**Model answer (EN):**
> Yes. Kubernetes has two parts: the **control plane** (historically called
> the master) and the **worker nodes**. The control plane is the brain: it
> stores the desired state and makes decisions. The worker nodes run the
> actual workloads in Pods. Everything goes through the **API server**, and
> the core idea is the **reconciliation loop**: you declare the desired state
> in YAML, and controllers continuously compare it with the actual state and
> act to close the gap.
>
> On each worker node there is the **kubelet**, which talks to the API server
> and makes sure the containers of its Pods are running; **kube-proxy**,
> which programs the network rules for Services; and a **container runtime**,
> usually **containerd**. Plus add-ons like **CoreDNS** and a **CNI**
> (Container Network Interface) plugin for Pod networking.

## 4. Components of the master node (control plane)

**Model answer (EN):**
> The control plane has five main components:
> 1. **kube-apiserver** — the front door; every component and kubectl talks
>    to it via REST; it handles authentication, authorization (RBAC) and
>    admission control.
> 2. **etcd** — a distributed key-value store; the single source of truth for
>    the cluster state. Only the API server talks to etcd directly.
> 3. **kube-scheduler** — assigns new Pods to nodes based on resource
>    requests, affinity, taints and tolerations.
> 4. **kube-controller-manager** — runs the controllers (Deployment,
>    ReplicaSet, Node, Job controllers…) that execute the reconciliation loop.
> 5. **cloud-controller-manager** — integrates with the cloud provider: load
>    balancers, volumes, node lifecycle.

**Notas:** en PayU esto salió **flojo** → es la pregunta #1 a memorizar.
Regla: **"solo el kube-apiserver habla con etcd"**. En AKS/EKS/GKE el control
plane lo administra el proveedor (tú no ves esos nodos) — buen comentario
senior para cerrar.

## 5. How do you rate yourself in Jenkins?

**Model answer (EN):**
> I'd say around 7 out of 10. I administered Jenkins in production together
> with Azure Pipelines: I built and maintained pipelines with Jenkinsfiles —
> declarative pipelines with build, test and deploy stages — managed
> plugins, credentials and agents, and set up quality gates so a change
> couldn't move forward if tests failed. What keeps me from a 10 is the
> deeper administration side, like large-scale controller tuning or writing
> custom plugins. More recently I've worked with GitOps-style tools, but the
> pipeline concepts are the same.

**Notas:** **nunca digas 10/10** (invita a preguntas trampa) ni menos de 6
si la usaste en producción. Da número + evidencia + qué te falta. Términos
que pueden repreguntar: **Jenkinsfile**, *declarative* vs *scripted*
pipeline, **shared libraries**, **credentials binding**, *multibranch
pipeline*, *webhooks*.

## 6. Disk space is full but `du` shows low usage

**Model answer (EN):**
> The classic cause is **files that were deleted but are still held open by
> a process** — for example a log file deleted while the application keeps
> writing to it. `du` walks the directory tree, so it doesn't see them, but
> `df` reports the blocks as still used. I'd confirm with
> `lsof +L1` (or `lsof | grep deleted`), identify the process, and then
> restart it or reload it so it releases the file — or truncate it via
> `/proc/<pid>/fd/<n>` if I can't restart. Prevention: proper log rotation
> with `copytruncate` or signaling the app.
>
> Other causes I'd check: **inode exhaustion** with `df -i` — many tiny
> files fill the inodes even if bytes are free; **files hidden under a mount
> point** — data written to a directory before a volume was mounted over it;
> and the **reserved blocks for root** in ext4 (about 5%).

**Notas — orden de diagnóstico:** `df -h` → `du -sh /*` (no cuadra) →
`lsof +L1` (borrados abiertos, causa #1) → `df -i` (**inodos**) → montajes
ocultos. Palabras clave: **"deleted but open file descriptor"** e **"inode
exhaustion"**.

## 7. "Too many open files" error

**Model answer (EN):**
> That means the process hit its **file descriptor limit** — in Linux,
> sockets also count as files. First I'd check whether it's a real need or
> a **leak**: `ls /proc/<pid>/fd | wc -l` or `lsof -p <pid>` over time — if
> the number keeps growing, the application is not closing files or
> connections, and that's a code fix.
>
> If it's a legitimate load, I raise the limit at the right layer: check the
> current one with `ulimit -n` or `cat /proc/<pid>/limits`; for a systemd
> service set `LimitNOFILE` in the unit file; for user sessions,
> `/etc/security/limits.conf`; and the system-wide limit with the sysctl
> `fs.file-max`. In containers, the limit comes from the container runtime
> configuration. Then restart the service and monitor the FD count.

**Notas:** dos causas → **fuga (leak)** vs **límite muy bajo**. Trampa
común: cambiar `limits.conf` y que no surta efecto porque el servicio corre
con **systemd** (necesita `LimitNOFILE`). Siglas: **FD = File Descriptor**.

## 8. S3 bucket versioning not enabling

**Model answer (EN):**
> I'd go layer by layer:
> 1. **Permissions** — the identity needs `s3:PutBucketVersioning`; check
>    for an explicit deny in the IAM policy, a **permissions boundary**, an
>    **SCP** (Service Control Policy) at the AWS Organizations level, or the
>    bucket policy. CloudTrail shows the exact denied call.
> 2. **Verify the actual state** with
>    `aws s3api get-bucket-versioning --bucket <name>` — if it returns
>    nothing, versioning was never enabled; `Suspended` means it was
>    enabled before. Note that once enabled, versioning can only be
>    **suspended, never fully disabled**.
> 3. **MFA Delete** — if it's configured, changing versioning requires the
>    root account's MFA (Multi-Factor Authentication) via CLI/API, not the
>    console.
> 4. **IaC drift/conflicts** — in Terraform AWS provider v4+, versioning is
>    a separate resource, `aws_s3_bucket_versioning`; if it's still set
>    inline or two resources manage it, one overwrites the other.
> 5. **Object Lock** requires versioning and prevents suspending it — so
>    that explains "can't change it" in the other direction.
> 6. Also the change can take a few minutes to propagate.

**Notas:** lo más probable en la vida real: **permisos (IAM/SCP)** y
**Terraform**. Frase clave: *"versioning can be suspended but never disabled"*.

## 9. `AccessDenied: Not authorized to perform sts:AssumeRole`

**Model answer (EN):**
> AssumeRole needs **two sides to agree**:
> 1. **The caller's identity policy** must allow `sts:AssumeRole` on that
>    role's ARN (Amazon Resource Name).
> 2. **The role's trust policy** must trust the caller as a principal.
>
> So I'd first confirm who I really am with `aws sts get-caller-identity` —
> very often the wrong profile or credentials are being used. Then I check
> the role ARN for typos or the wrong account, the trust policy's
> `Principal`, and any **conditions** — `sts:ExternalId`, MFA required,
> `aws:PrincipalOrgID`, source IP. Then check the guardrails: an **SCP**
> or a **permissions boundary** with an explicit deny. **CloudTrail** shows
> the failed AssumeRole event with the exact principal. For cross-account,
> both accounts must allow it.
>
> In Kubernetes with IRSA (IAM Roles for Service Accounts) the call is
> `AssumeRoleWithWebIdentity`, and the usual culprit is the trust policy's
> `sub` condition not matching `system:serviceaccount:<namespace>:<sa>`, or
> the OIDC (OpenID Connect) provider not being registered in IAM.

**Notas:** frase que vende: **"two sides: identity policy + trust policy"**.
Esto conecta con tu tema #27 (IRSA, 🟢).

## 10. What is a Pod?

**Model answer (EN):**
> A Pod is the **smallest deployable unit** in Kubernetes. It's a wrapper
> around one or more containers that **share the same network namespace** —
> same IP address, they talk via localhost — and can share **volumes**.
> Usually it's one main container, plus optional sidecars or init
> containers. Pods are **ephemeral**: if one dies, it isn't repaired, it's
> replaced with a new one with a new IP — that's why we don't create bare
> Pods in production but manage them through Deployments, StatefulSets or
> DaemonSets, and expose them with a Service.

## 11. How do you create a Pod?

**Model answer (EN):**
> Two ways. **Imperative**, for a quick test:
> `kubectl run nginx --image=nginx`. **Declarative**, which is what I use in
> real work — a YAML manifest applied with `kubectl apply -f pod.yaml`:
>
> ```yaml
> apiVersion: v1
> kind: Pod
> metadata:
>   name: nginx
>   labels:
>     app: nginx
> spec:
>   containers:
>     - name: nginx
>       image: nginx:1.27
>       ports:
>         - containerPort: 80
>       resources:
>         requests: { cpu: 100m, memory: 128Mi }
>         limits:   { memory: 256Mi }
> ```
>
> Tip: `kubectl run nginx --image=nginx --dry-run=client -o yaml` generates
> the YAML skeleton. In production, though, I'd wrap it in a Deployment so
> it gets self-healing and rolling updates.

**Notas:** los 4 campos raíz de todo manifiesto: **apiVersion, kind,
metadata, spec**. Mencionar **requests/limits** suma puntos.

## 12. What is the purpose of `kubectl`?

**Model answer (EN):**
> `kubectl` is the **command-line client for the Kubernetes API**. It
> doesn't do anything on the nodes itself — it sends REST requests to the
> kube-apiserver, authenticated with the kubeconfig file (`~/.kube/config`),
> which holds the clusters, users and contexts. I use it to apply manifests
> (`apply`), inspect (`get`, `describe`), troubleshoot (`logs`, `exec`,
> `get events`, `top`), and manage rollouts (`rollout status/undo`).

**Notas:** clave senior: **"kubectl solo habla con el API server"**. Comandos
de troubleshooting en orden: `get pods` → `describe pod` → `logs
--previous` → `get events`.

## 13. Master and worker in Jenkins

**Model answer (EN):**
> Yes — today they're called **controller** and **agents** (formerly master
> and slave). The **controller** is the central server: it hosts the UI,
> stores configuration, jobs, credentials and plugins, schedules builds and
> keeps the history. The **agents** are the machines that actually
> **execute** the builds; each agent has a number of **executors**, and jobs
> are routed to them with **labels** (for example `linux`, `docker`).
>
> Agents connect over **SSH** (the controller initiates) or as **inbound
> agents** via JNLP (Java Network Launch Protocol) or WebSocket (the agent
> initiates — useful behind a firewall). Best practice is to set the
> controller's executors to **zero** so builds never run on it — for
> security and stability — and use **ephemeral agents**, for example the
> Kubernetes plugin, which spins up a Pod per build and deletes it after.
>
> In a Jenkinsfile: `agent { label 'linux' }` or `agent { kubernetes { ... } }`.

**Notas:** decir **"controller/agent"** (terminología actual) y aclarar que
antes se llamaba master/slave → demuestra que estás actualizado. Conecta con
Kubernetes (agentes efímeros en Pods) — puente natural entre las dos
herramientas que pregunta esta entrevista.

---

## Prioridad de repaso para esta noche

1. **#4 componentes del control plane** (salió flojo en PayU).
2. **#6 y #7 Linux** (sin examen dedicado — más riesgo).
3. **#9 `sts:AssumeRole`** y **#8 S3 versioning**.
4. **#13 Jenkins controller/agent**.
5. Ensayar en voz alta **#1 y #5** (preguntas de experiencia, sin
   respuesta "correcta" pero dan la primera impresión).

## Resultado de la práctica

(Se completa durante la sesión de práctica.)
