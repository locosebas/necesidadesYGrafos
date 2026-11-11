# Diagramas C4 - Entrevista técnica Gorilla Logic (Senior Platform DevOps)

Un diagrama C4 (Context, Containers, Components, Code) por idea, sacados de los 5 escenarios del
assessment de Canditech (4 nov 2026) y de la posición "DevOps GCP" que mencionó la reclutadora. Están
en Mermaid, así que GitHub los dibuja directo. Los usa el [libreto](libreto-diapositivas.md) y el
generador de la [presentación](presentacion.html).

Convenciones de color (las del modelo C4):

- **Azul oscuro**: persona.
- **Azul medio**: sistema propio.
- **Azul claro**: contenedor (servicio, paso, almacén).
- **Gris**: sistema externo.
- **Rojo**: lo que falla o el riesgo.
- **Verde**: la corrección o el estado sano.
- **Recuadro punteado**: límite (zona, clúster, repositorio).

Íconos: cada `ico:nombre` es un logo guardado en [iconos/](iconos/) (de
[Iconify](https://icon-sets.iconify.design/)). En GitHub se ven como texto; en la presentación HTML se
ven como logos.

---

## D1 · Contexto: los 5 escenarios del assessment y el método común

Panorama. Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Yo · Senior Platform<br/>DevOps de guardia"]:::person
  sh["ico:account-tie<br/>Stakeholders<br/>PM, marketing, product"]:::person
  subgraph esc["5 escenarios"]
    e1["ico:cart<br/>1 · E-commerce en AWS<br/>4x tráfico"]:::container
    e2["ico:terraform-icon<br/>2 · Terraform en producción<br/>plan, lock, drift"]:::container
    e3["ico:argo-icon<br/>3 · Incidente EKS<br/>tras sync de Argo CD"]:::container
    e4["ico:swap-horizontal<br/>4 · Canary<br/>progressive delivery"]:::container
    e5["ico:python<br/>5 · platformctl<br/>CLI interna"]:::container
  end
  met["ico:check-decagram<br/>Método<br/>1 estabilizar · 2 diagnosticar<br/>3 corregir en Git · 4 prevenir"]:::ok
  yo -->|"resuelve"| esc
  sh -->|"presiona por atajos"| yo
  esc --> met
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
```

## D2 · Contenedores: la arquitectura del e-commerce

Bloque 1. Tipo: Contenedores.

```mermaid
flowchart LR
  u["ico:account-group<br/>Clientes<br/>10.000/día → 4x"]:::person
  alb["ico:aws-elb<br/>Application<br/>Load Balancer"]:::system
  subgraph vpc["VPC en EE. UU. · 2 Availability Zones"]
    subgraph eks["EKS en subredes privadas"]
      web["ico:server<br/>web"]:::container
      pay["ico:credit-card<br/>payment"]:::container
      img["ico:image<br/>image"]:::container
    end
    db["ico:database<br/>Base de datos"]:::container
  end
  gw["ico:credit-card<br/>Pasarela de pago<br/>externa"]:::ext
  u -->|"HTTPS"| alb --> web
  web -->|"HTTP"| pay
  web -->|"HTTP"| img
  pay --> db
  web --> db
  pay -->|"cobro"| gw
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D3 · Dinámico: sitio lento con 4x tráfico, los 4 pasos

Bloque 1. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  p1["ico:alert<br/>1 · Incident management<br/>Incident Commander<br/>updates cada 15–30 min"]:::container
  p2["ico:speedometer<br/>2 · Mitigar<br/>kubectl scale, más nodos<br/>proteger checkout"]:::container
  p3["ico:magnify-scan<br/>3 · Causa raíz<br/>Four Golden Signals<br/>capa por capa"]:::container
  p4["ico:check-decagram<br/>4 · Prevenir<br/>HPA + Karpenter, CDN,<br/>caché, load testing"]:::ok
  p1 -->|"1"| p2 -->|"2"| p3 -->|"3"| p4
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
```

## D4 · Contenedores: usuarios en Asia y la CDN

Bloque 1. Tipo: Contenedores.

```mermaid
flowchart LR
  asia["ico:earth<br/>Usuarios en Asia<br/>150–250 ms por viaje"]:::person
  subgraph edge["CDN · edge locations en Asia"]
    cf["ico:aws-cloudfront<br/>CloudFront<br/>Cache-Control, Origin Shield"]:::system
  end
  s3["ico:aws-s3<br/>S3<br/>imágenes WebP/AVIF"]:::container
  ga["ico:aws-route53<br/>Global Accelerator /<br/>Route 53 latency-based"]:::ext
  us["ico:aws-elb<br/>Región EE. UU.<br/>ALB + EKS"]:::container
  asia -->|"imágenes y estáticos"| cf
  cf -->|"origin"| s3
  asia -->|"contenido dinámico"| ga --> us
  cf -.->|"dinámico por backbone de AWS"| us
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D5 · Componentes: cortar el efecto dominó

Bloque 1. Tipo: Componentes.

```mermaid
flowchart LR
  subgraph websvc["web service"]
    to["ico:timer-sand<br/>Timeout"]:::container
    rt["ico:undo-variant<br/>Retry con<br/>backoff + jitter"]:::container
    cb["ico:electric-switch<br/>Circuit breaker<br/>closed · open · half-open"]:::ok
  end
  subgraph bh["Bulkhead · recursos aislados"]
    pay["ico:credit-card<br/>payment<br/>requests/limits, node group,<br/>pool de conexiones propio"]:::bad
  end
  deg["ico:check-decagram<br/>Degradación elegante<br/>el resto del sitio sigue"]:::ok
  to --> rt --> cb
  cb -->|"closed: llama"| pay
  cb -->|"open: falla rápido"| deg
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D6 · Dinámico: la compra asíncrona con cola

Bloque 1. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  web["ico:cart<br/>web<br/>orden PENDING"]:::container
  q["ico:aws-sqs<br/>Cola<br/>SQS / Kafka"]:::system
  w["ico:server<br/>payment workers<br/>idempotency key"]:::container
  gw["ico:credit-card<br/>Pasarela<br/>Stripe / Adyen"]:::ext
  st["ico:database<br/>Orden<br/>PAID / FAILED"]:::ok
  dlq["ico:tray-full<br/>DLQ<br/>Dead Letter Queue"]:::bad
  web -->|"1 · encola"| q -->|"2 · consume"| w -->|"3 · cobra una sola vez"| gw
  w -->|"4 · actualiza"| st
  q -.->|"falla N veces"| dlq
  st -.->|"Saga: compensar si falla"| web
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D7 · Contenedores: Terraform en producción con CI

Bloque 2. Tipo: Contenedores.

```mermaid
flowchart LR
  dev["ico:account<br/>Ingeniero"]:::person
  pr["ico:source-pull<br/>Pull request<br/>revisión + CODEOWNERS"]:::container
  ci["ico:github-actions<br/>CI<br/>plan · policy-as-code · apply"]:::system
  subgraph be["Backend remoto"]
    st["ico:aws-s3<br/>State en S3<br/>con versionado"]:::container
    lk["ico:aws-dynamodb<br/>Lock en DynamoDB"]:::container
  end
  aws["ico:aws<br/>AWS<br/>VPC, IAM, EKS, node groups"]:::ext
  bg["ico:key-chain<br/>Break-glass<br/>rol de emergencia auditado"]:::bad
  dev --> pr --> ci
  ci -->|"lee / escribe"| st
  ci -->|"toma el lock"| lk
  ci -->|"apply"| aws
  bg -.->|"solo emergencias, codificar en 24–48 h"| aws
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D8 · Componentes: revisar el plan, split / rework

Bloque 2. Tipo: Componentes.

```mermaid
flowchart LR
  subgraph plan["terraform plan contra producción"]
    r1["ico:aws-iam<br/>-/+ IAM role de nodos<br/>address changed"]:::bad
    r2["ico:ip-network<br/>- subnet us-east-1b<br/>+ subnet use1-az2"]:::bad
    r3["ico:shield-check<br/>SG rule api_old → api_new"]:::bad
    r4["ico:aws-ec2<br/>GPU launch template 12 → 13<br/>cambio real"]:::container
  end
  pa["ico:file-code<br/>PR A · moved blocks<br/>plan = 0 / 0 / 0"]:::ok
  pb["ico:wrench<br/>PR B · GPU v13<br/>ventana controlada, PDB"]:::ok
  pol["ico:shield-check<br/>Policy-as-code<br/>OPA/Conftest, Checkov, Sentinel"]:::ok
  r1 --> pa
  r2 --> pa
  r3 --> pa
  r4 --> pb
  pa --> pol
  pb --> pol
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D9 · Dinámico: state lock huérfano, 7 pasos antes de force-unlock

Bloque 2. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  s1["ico:lock<br/>1 · Congelar<br/>pausar pipeline, un dueño"]:::container
  s2["ico:server<br/>2 · ¿Proceso vivo?<br/>runner-17, SIGINT"]:::container
  s3["ico:file-lock<br/>3 · Backup<br/>state pull, errored.tfstate"]:::container
  s4["ico:aws-cloudtrail<br/>4 · ¿Qué cambió?<br/>CloudTrail + plan guardado"]:::container
  s5["ico:key-chain<br/>5 · force-unlock<br/>solo si todo se cumple"]:::bad
  s6["ico:scale-balance<br/>6 · Reconciliar<br/>plan -refresh-only, import"]:::container
  s7["ico:check-decagram<br/>7 · Reanudar por CI<br/>postmortem"]:::ok
  s1 -->|"1"| s2 -->|"2"| s3 -->|"3"| s4 -->|"4"| s5 -->|"5"| s6 -->|"6"| s7
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D10 · Dinámico: drift por un CIDR agregado a mano

Bloque 2. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  em["ico:alert<br/>02:14 cambio manual<br/>+ 10.55.8.0/24 en el SG"]:::bad
  no["ico:alert-octagon<br/>NO ignore_changes<br/>NO apply normal"]:::bad
  ver["ico:magnify-scan<br/>1 · Verificar<br/>CloudTrail, Flow Logs,<br/>dueño del CIDR"]:::container
  cod["ico:file-code<br/>2 · Codificar en Terraform<br/>import block, plan limpio"]:::ok
  gr["ico:radar<br/>3 · Guardrails<br/>drift detection nocturno,<br/>AWS Config, CODEOWNERS"]:::ok
  em --> no
  em -->|"1"| ver -->|"2"| cod -->|"3"| gr
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D11 · Contenedores: el 503 después del sync de Argo CD

Bloque 3. Tipo: Contenedores.

```mermaid
flowchart LR
  argo["ico:argo-icon<br/>Argo CD sync 14:01<br/>Service → ClusterIP"]:::system
  alb["ico:aws-elb<br/>ALB · 503<br/>0 healthy / 6 unhealthy"]:::bad
  subgraph eks["EKS"]
    node["ico:aws-ec2<br/>Nodos<br/>target-type: instance<br/>espera un NodePort"]:::container
    svc["ico:kubernetes<br/>Service ClusterIP<br/>sin NodePort"]:::bad
  end
  subgraph sub["Subredes privadas · IPs libres"]
    a["ico:ip-network<br/>a = 3 · b = 1"]:::bad
    c["ico:ip-network<br/>c = 900"]:::ok
  end
  argo --> svc
  alb -->|"health check al NodePort ✗"| node
  node -.-> svc
  node -.->|"VPC CNI: sin IP para pods nuevos"| a
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D12 · Contenedores: el canary que también dañó al stable

Bloque 4. Tipo: Contenedores.

```mermaid
flowchart LR
  ar["ico:argo-icon<br/>Argo Rollouts<br/>abort → 100% stable"]:::system
  subgraph svc["Servicio"]
    st["ico:server<br/>stable · 90%<br/>¿jaló el tag nuevo?"]:::container
    ca["ico:server<br/>canary · 10%<br/>más 5xx"]:::bad
  end
  dep["ico:database<br/>Dependencia downstream<br/>compartida · latencia"]:::bad
  ecr["ico:docker-icon<br/>ECR<br/>tag empujado varias veces"]:::ext
  git["ico:git-icon<br/>Repo de entorno<br/>revert + image@sha256"]:::ok
  ar --> st
  ar --> ca
  ca -->|"retry storm"| dep
  st --> dep
  ecr -.->|"tag mutable"| ca
  ecr -.-> st
  git -->|"Argo CD reconcilia"| svc
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D13 · Dinámico: expand-contract, para que el rollback siempre sea seguro

Bloque 4. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  x1["ico:database<br/>1 · Expand<br/>solo agregar columnas/tablas"]:::container
  x2["ico:file-code<br/>2 · Migrar el código<br/>lee y escribe ambos"]:::container
  x3["ico:database<br/>3 · Contract<br/>borrar lo viejo en<br/>un release posterior"]:::ok
  rb["ico:undo-variant<br/>Rollback de la app<br/>seguro en 1 y 2"]:::ok
  x1 -->|"1"| x2 -->|"2"| x3
  x2 -.-> rb
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
```

## D14 · Componentes: platformctl v1 y sus 4 riesgos

Bloque 5. Tipo: Componentes.

```mermaid
flowchart LR
  subgraph v1["platformctl v1 (Python)"]
    f1["ico:key-chain<br/>1 · log de dict(os.environ)<br/>filtra secretos"]:::bad
    f2["ico:target<br/>2 · find_context()<br/>substring, sin paginar,<br/>ENV=prod por defecto"]:::bad
    f3["ico:console<br/>3 · shell=True + grep<br/>command injection"]:::bad
    f4["ico:alert<br/>4 · siempre imprime done<br/>sin límites ni dry-run"]:::bad
  end
  k8s["ico:kubernetes<br/>Clúster equivocado<br/>o producción"]:::ext
  f2 --> k8s
  f3 --> k8s
  f4 --> k8s
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
  classDef bad fill:#c62828,stroke:#8e0000,color:#fff
```

## D15 · Componentes: diseño de platformctl v2

Bloque 5. Tipo: Componentes.

```mermaid
flowchart LR
  op["ico:account<br/>On-call<br/>--env --namespace<br/>--deployment --reason"]:::person
  subgraph v2["platformctl v2"]
    cfg["ico:file-code<br/>Config versionada<br/>env → cluster, cuenta, región"]:::container
    sts["ico:aws-iam<br/>sts get-caller-identity<br/>verifica la cuenta"]:::container
    dry["ico:magnify-scan<br/>Dry-run por defecto<br/>N de M réplicas, PDB"]:::ok
    ev["ico:undo-variant<br/>Eviction API<br/>lotes pequeños, espera Ready"]:::ok
    out["ico:console<br/>Exit codes 0–5<br/>--output json · stdout/stderr"]:::ok
  end
  k8s["ico:kubernetes<br/>EKS<br/>RBAC mínimo"]:::ext
  op --> cfg --> sts --> dry -->|"--execute + confirmar"| ev --> k8s
  ev --> out
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
  classDef ok fill:#2e7d32,stroke:#1b5e20,color:#fff
```

## D16 · Contexto: equivalencias AWS → GCP para la posición "DevOps GCP"

GCP. Tipo: Contexto.

```mermaid
flowchart LR
  subgraph aws["AWS"]
    a1["EKS"]:::container
    a2["IAM roles · IRSA"]:::container
    a3["ECR"]:::container
    a4["ALB · CloudFront"]:::container
    a5["S3 · SQS"]:::container
    a6["CloudWatch · CloudTrail"]:::container
  end
  subgraph gcp["GCP · Google Cloud"]
    g1["GKE"]:::system
    g2["IAM service accounts · Workload Identity"]:::system
    g3["Artifact Registry"]:::system
    g4["Cloud Load Balancing · Cloud CDN"]:::system
    g5["Cloud Storage · Pub/Sub"]:::system
    g6["Cloud Monitoring/Logging · Audit Logs"]:::system
  end
  a1 --- g1
  a2 --- g2
  a3 --- g3
  a4 --- g4
  a5 --- g5
  a6 --- g6
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
```
