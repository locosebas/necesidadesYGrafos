# Diagramas C4 - Entrevista Chubb (Cloud Engineer Ops, L1)

Un diagrama C4 (Context, Containers, Components, Code) por idea. Están en Mermaid. Los usa el
[libreto](libreto-diapositivas.md) y el generador de la [presentación](presentacion.html).

Convenciones de color (modelo C4). El generador agrega solo los `classDef`, por eso aquí no se repiten:

- **Azul oscuro** (`person`): persona.
- **Azul medio** (`system`): sistema propio.
- **Azul claro** (`container`): contenedor (servicio, pipeline, base de datos).
- **Gris** (`ext`): sistema externo.
- **Recuadro punteado**: límite (empresa, cuenta, red, ambiente).

Íconos: cada `ico:nombre` es un logo de [iconos/](iconos/) (Iconify). En GitHub se ven como texto.

**Parte A** = presentación personal (DA*). **Parte B** = preguntas preparadas (D1… D22).

---

# Parte A · Presentación personal

## DA1 · Contexto: mi recorrido profesional

Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Sebastián Díaz<br/>Cloud / DevOps Engineer"]:::person
  subgraph biz["Bizagi · ene 2022 - jun 2024"]
    bz["ico:azure-icon<br/>Plataforma Bizagi en Azure<br/>CI/CD, releases, observabilidad"]:::system
  end
  subgraph meli["MercadoLibre · jun 2024 - ago 2026"]
    mp["ico:aws ico:google-cloud<br/>PaaS interno de cómputo<br/>Mercado Pago (banca regulada)"]:::system
  end
  subgraph chubb["Chubb · siguiente paso"]
    ch["ico:google-cloud ico:azure-icon<br/>Plataforma cloud global<br/>operación + nueva plataforma GCP"]:::container
  end
  yo -->|"Azure Pipelines, Jenkins,<br/>Grafana, SSO con Entra ID"| bz
  yo -->|"Terraform, Kubernetes, ECS,<br/>operators en Go, incidentes"| mp
  bz -->|"aprendí a operar<br/>un producto regulado"| mp
  mp -->|"traigo plataforma,<br/>IaC y operación"| ch
```

## DA2 · Contenedores: lo que construí en Bizagi

Tipo: Contenedores.

```mermaid
flowchart LR
  dev["ico:account-group<br/>Equipos de desarrollo"]:::person
  subgraph az["Azure · Bizagi"]
    pipe["ico:azuredevops ico:jenkins<br/>Pipelines CI/CD<br/>build once, deploy anywhere"]:::container
    art["ico:package-variant-closed<br/>Artefacto versionado"]:::container
    stg["ico:server<br/>Stage<br/>unos días antes"]:::container
    prd["ico:server<br/>Varios ambientes<br/>de producción"]:::container
    graf["ico:grafana<br/>Grafana + alertas<br/>onboarding automatizado"]:::container
  end
  entra["ico:microsoft-icon<br/>Entra ID + proveedores<br/>SSO / OIDC"]:::ext
  dev -->|"commit / PR"| pipe
  pipe -->|"crea una vez"| art
  art -->|"despliega"| stg
  stg -->|"solo si stage está sano"| prd
  prd -.->|"métricas y alertas"| graf
  prd -->|"inicio de sesión"| entra
```

## DA3 · Contenedores: plataforma de cómputo en MercadoLibre

Tipo: Contenedores.

```mermaid
flowchart LR
  apps["ico:account-group<br/>Equipos de Mercado Pago"]:::person
  subgraph paas["PaaS interno · equipo de cómputo"]
    tf["ico:terraform-icon<br/>Módulos Terraform compartidos<br/>state, backends, migraciones"]:::container
    k8s["ico:kubernetes ico:aws-ecs<br/>Kubernetes y ECS<br/>cómputo de los servicios"]:::container
    op["ico:cog-sync<br/>Operators en Go y Python<br/>reconciliation loop"]:::container
    alr["ico:alert<br/>Alertas de utilización<br/>reactiva + predictiva + LLM"]:::container
    tk["ico:claude<br/>Diagnóstico de tickets<br/>RAG + MCP, no auto-resuelve"]:::container
  end
  cloud["ico:aws ico:google-cloud<br/>AWS y GCP"]:::ext
  obs["ico:datadog ico:grafana<br/>Observabilidad"]:::ext
  apps -->|"piden infraestructura"| tf
  tf -->|"aprovisiona"| cloud
  apps -->|"despliegan servicios"| k8s
  op -->|"automatiza recursos"| k8s
  k8s -.->|"métricas"| obs
  obs -->|"dispara"| alr
  apps -->|"abren tickets"| tk
```

## DA4 · Contexto: por qué encajo en este cargo

Tipo: Contexto (mapa de requisitos de Chubb contra mi experiencia).

```mermaid
flowchart LR
  subgraph req["Lo que pide Chubb"]
    r1["ico:kubernetes<br/>Kubernetes, AKS, EKS"]:::ext
    r2["ico:terraform-icon ico:jenkins<br/>IaC y pipelines de infraestructura"]:::ext
    r3["ico:fire-alert<br/>Escalamientos e incidentes mayores"]:::ext
    r4["ico:google-cloud ico:azure-icon<br/>Azure hoy, nueva plataforma GCP"]:::ext
    r5["ico:shield-lock<br/>Gobierno, IAM y seguridad"]:::ext
  end
  subgraph yo["Lo que traigo"]
    e1["ico:kubernetes<br/>K8s en AKS y en MercadoLibre,<br/>operators propios"]:::system
    e2["ico:terraform-icon<br/>Módulos compartidos, state,<br/>Jenkins y Azure Pipelines"]:::system
    e3["ico:fire-alert<br/>On-call, postmortems,<br/>banca regulada"]:::system
    e4["ico:google-cloud<br/>Azure en Bizagi,<br/>AWS y GCP en MercadoLibre"]:::system
    e5["ico:shield-lock<br/>SSO/OIDC con Entra ID,<br/>RBAC, mínimo privilegio"]:::system
  end
  r1 --- e1
  r2 --- e2
  r3 --- e3
  r4 --- e4
  r5 --- e5
```

---

# Parte B · Preguntas preparadas

## D1 · Contexto: Azure como lo operé (landing zone)

Pregunta: experiencia en Azure. Tipo: Contexto / Despliegue.

```mermaid
flowchart TB
  entra["ico:microsoft-icon<br/>Entra ID<br/>identidades, grupos, SSO"]:::ext
  subgraph mg["Management Groups · herencia de RBAC y Policy"]
    subgraph sub1["Suscripción de producción"]
      rg1["Resource Groups<br/>AKS, App Services, SQL"]:::container
    end
    subgraph sub2["Suscripción de stage"]
      rg2["Resource Groups<br/>misma topología"]:::container
    end
  end
  pol["ico:shield-check<br/>Azure Policy + RBAC<br/>asignados arriba, se heredan"]:::system
  mon["ico:chart-line<br/>Azure Monitor / Grafana"]:::system
  entra -->|"autentica"| mg
  pol -->|"aplica a"| mg
  rg1 -.->|"telemetría"| mon
  rg2 -.->|"telemetría"| mon
```

## D2 · Contexto: jerarquía de recursos en GCP

Pregunta: cómo construirías la nueva plataforma GCP (landing zone). Tipo: Contexto.

```mermaid
flowchart TB
  org["ico:google-cloud<br/>Organization<br/>chubb.com"]:::system
  subgraph fold["Folders · por ambiente o unidad de negocio"]
    fprod["Folder prod"]:::container
    fnon["Folder non-prod"]:::container
    fshr["Folder shared"]:::container
  end
  subgraph proj["Projects · unidad de facturación y de IAM"]
    p1["Project app-a-prod"]:::container
    p2["Project app-a-stage"]:::container
    host["Host project<br/>Shared VPC"]:::container
    logp["Project logging<br/>y seguridad"]:::container
  end
  opol["ico:shield-lock<br/>Organization Policies<br/>se heredan hacia abajo"]:::ext
  iam["ico:account-group<br/>IAM con grupos<br/>nunca usuarios sueltos"]:::ext
  org --> fprod
  org --> fnon
  org --> fshr
  fprod --> p1
  fnon --> p2
  fshr --> host
  fshr --> logp
  opol -.->|"aplica en"| org
  iam -.->|"roles por folder/project"| fold
  host -.->|"comparte subredes"| p1
  host -.->|"comparte subredes"| p2
```

## D3 · Dinámico: plan para la landing zone de GCP

Pregunta: cómo construirías la nueva plataforma GCP. Tipo: Dinámico.

```mermaid
flowchart LR
  a["1 · Identidad<br/>Cloud Identity + SSO<br/>con Entra ID"]:::container
  b["2 · Jerarquía<br/>Org, Folders, Projects<br/>+ Org Policies"]:::container
  c["3 · Red<br/>Shared VPC, hub-and-spoke,<br/>Interconnect / VPN"]:::container
  d["4 · Seguridad y logs<br/>log sinks, SCC,<br/>KMS"]:::container
  e["5 · Project factory<br/>Terraform + pipeline<br/>autoservicio"]:::container
  f["6 · Cómputo<br/>GKE con Workload Identity<br/>y golden paths"]:::container
  g["7 · Operación<br/>monitoreo, FinOps,<br/>runbooks"]:::container
  a --> b --> c --> d --> e --> f --> g
```

## D4 · Contexto: Cloud Adoption Framework de Microsoft

Pregunta: qué es el Cloud Adoption Framework. Tipo: Contexto (metodologías).

```mermaid
flowchart LR
  s["ico:target<br/>Strategy<br/>por qué ir a la nube"]:::system
  p["ico:clipboard-list<br/>Plan<br/>inventario, 5 Rs, equipos"]:::system
  r["ico:sitemap<br/>Ready<br/>landing zone"]:::system
  subgraph adopt["Adopt"]
    mi["ico:swap-horizontal<br/>Migrate"]:::container
    inn["ico:flash<br/>Innovate"]:::container
  end
  subgraph cont["Transversales, todo el tiempo"]
    gov["ico:scale-balance<br/>Govern"]:::container
    sec["ico:shield-lock<br/>Secure"]:::container
    man["ico:cog-sync<br/>Manage"]:::container
  end
  s --> p --> r --> adopt
  adopt -.-> cont
```

## D5 · Contenedores: estructura de un repositorio de Terraform

Pregunta: cómo organizas Terraform para varios ambientes. Tipo: Contenedores.

```mermaid
flowchart LR
  subgraph mods["Repositorio de módulos · versionados con tags"]
    m1["ico:terraform-icon<br/>módulo network"]:::container
    m2["ico:terraform-icon<br/>módulo gke / aks"]:::container
    m3["ico:terraform-icon<br/>módulo project / subscription"]:::container
  end
  subgraph envs["Repositorio de ambientes · una carpeta y un state por ambiente"]
    stg["stage<br/>módulo v1.4.0 + variables"]:::system
    prd["prod<br/>módulo v1.3.2 + variables"]:::system
  end
  be["ico:database<br/>Backend remoto<br/>GCS / Blob / S3 con locking"]:::ext
  mods -->|"source = ...?ref=v1.4.0"| stg
  mods -->|"versión fijada"| prd
  stg -->|"state propio"| be
  prd -->|"state propio"| be
```

## D6 · Dinámico: pipeline de infraestructura en Jenkins

Pregunta: CI/CD para infraestructura con Terraform y Jenkins. Tipo: Dinámico.

```mermaid
flowchart LR
  pr["ico:source-pull<br/>1 · Pull request"]:::person
  ci["ico:jenkins<br/>2 · fmt, validate,<br/>tflint, checkov"]:::container
  pl["ico:terraform-icon<br/>3 · terraform plan<br/>publicado en el PR"]:::container
  rv["ico:account-tie<br/>4 · Revisión humana<br/>+ cambio en ServiceNow"]:::person
  ap["ico:terraform-icon<br/>5 · apply en stage"]:::container
  ok["ico:check-decagram<br/>6 · stage sano<br/>pruebas de humo"]:::container
  pd["ico:terraform-icon<br/>7 · apply en prod<br/>mismo plan revisado"]:::container
  pr --> ci --> pl --> rv --> ap --> ok --> pd
```

## D7 · Dinámico: drift en Terraform

Pregunta: alguien cambió algo a mano en la consola. Tipo: Dinámico.

```mermaid
flowchart LR
  a["ico:alert<br/>1 · plan programado<br/>detecta diferencias"]:::container
  b["ico:magnify-scan<br/>2 · ¿quién y por qué?<br/>Activity Log / Audit Logs"]:::container
  c{"3 · ¿el cambio<br/>era correcto?"}
  d["ico:terraform-icon<br/>4a · llevarlo al código<br/>o terraform import"]:::container
  e["ico:terraform-icon<br/>4b · apply para revertir<br/>al estado declarado"]:::container
  f["ico:shield-lock<br/>5 · prevenir<br/>quitar permisos de escritura"]:::system
  a --> b --> c
  c -->|"sí"| d --> f
  c -->|"no"| e --> f
```

## D8 · Contexto: Terraform vs. Ansible

Pregunta: cuándo usar Terraform y cuándo Ansible. Tipo: Contexto.

```mermaid
flowchart LR
  tf["ico:terraform-icon<br/>Terraform<br/>declarativo, con state<br/>crea la infraestructura"]:::system
  an["ico:ansible<br/>Ansible<br/>agentless por SSH / WinRM<br/>configura lo que ya existe"]:::system
  subgraph nube["Nube"]
    vm["ico:server<br/>VMs, redes,<br/>clústeres"]:::container
    os["ico:linux-tux ico:microsoft-windows-icon<br/>Sistema operativo,<br/>paquetes, parches"]:::container
  end
  tf -->|"1 · aprovisiona"| vm
  an -->|"2 · configura e<br/>idempotente"| os
  vm --- os
```

## D9 · Contenedores: arquitectura de Kubernetes

Pregunta: arquitectura de Kubernetes. Tipo: Contenedores.

```mermaid
flowchart LR
  user["ico:account<br/>kubectl / pipeline"]:::person
  subgraph cp["Control plane"]
    api["kube-apiserver"]:::system
    etcd["ico:database<br/>etcd"]:::system
    sch["kube-scheduler"]:::system
    cm["kube-controller-manager"]:::system
    ccm["cloud-controller-manager"]:::system
  end
  subgraph wk["Worker node"]
    kl["kubelet"]:::container
    kp["kube-proxy"]:::container
    rt["containerd"]:::container
    pod["ico:docker-icon<br/>Pods"]:::container
  end
  user --> api
  api --- etcd
  sch --> api
  cm --> api
  ccm --> api
  kl --> api
  kl --> rt --> pod
  kp -.->|"reglas de red<br/>de los Services"| pod
```

## D10 · Contexto: AKS, EKS y GKE

Pregunta: diferencias entre Kubernetes administrados. Tipo: Contexto.

```mermaid
flowchart TB
  k8s["ico:kubernetes<br/>Mismo Kubernetes<br/>control plane administrado"]:::system
  aks["ico:azure-icon<br/>AKS<br/>Entra ID + Azure RBAC<br/>Azure CNI, Workload Identity"]:::container
  eks["ico:aws-eks<br/>EKS<br/>IAM + IRSA / Pod Identity<br/>VPC CNI, Karpenter"]:::container
  gke["ico:google-cloud<br/>GKE<br/>Autopilot o Standard<br/>Workload Identity, VPC-native"]:::container
  k8s --> aks
  k8s --> eks
  k8s --> gke
```

## D11 · Dinámico: un Pod en CrashLoopBackOff

Pregunta: troubleshooting de un Pod que se reinicia. Tipo: Dinámico.

```mermaid
flowchart LR
  a["ico:kubernetes<br/>1 · kubectl get pods<br/>CrashLoopBackOff"]:::container
  b["ico:magnify-scan<br/>2 · kubectl describe pod<br/>eventos, exit code"]:::container
  c["ico:file-document-multiple<br/>3 · kubectl logs --previous"]:::container
  d{"4 · causa"}
  e["OOMKilled · exit 137<br/>subir limits o<br/>arreglar la fuga"]:::system
  f["Config / secret<br/>faltante"]:::system
  g["Probe mal<br/>configurada"]:::system
  h["ico:history<br/>5 · prevención<br/>alerta + postmortem"]:::system
  a --> b --> c --> d
  d --> e --> h
  d --> f --> h
  d --> g --> h
```

## D12 · Dinámico: incidente mayor en producción

Pregunta: cómo manejas una escalación o un incidente mayor. Tipo: Dinámico.

```mermaid
flowchart LR
  a["ico:fire-alert<br/>1 · Detectar y triage<br/>severidad, impacto"]:::container
  b["ico:account-voice<br/>2 · Roles<br/>incident commander,<br/>comunicación"]:::person
  c["ico:backup-restore<br/>3 · Mitigar primero<br/>rollback, failover,<br/>escalar"]:::container
  d["ico:magnify-scan<br/>4 · Diagnosticar<br/>causa raíz"]:::container
  e["ico:check-decagram<br/>5 · Resolver<br/>y verificar"]:::container
  f["ico:history<br/>6 · Postmortem<br/>sin culpas, acciones"]:::container
  sn["ico:ticket-outline<br/>ServiceNow<br/>incidente + cambio<br/>de emergencia"]:::ext
  a --> b --> c --> d --> e --> f
  b -.->|"registro"| sn
  c -.->|"cambio de emergencia"| sn
```

## D13 · Contenedores: monitoreo con Prometheus y ELK

Pregunta: monitoreo y logging. Tipo: Contenedores.

```mermaid
flowchart LR
  subgraph k8s["Clúster Kubernetes"]
    app["ico:docker-icon<br/>Pods con /metrics<br/>y logs a stdout"]:::container
    fb["Agente de logs<br/>Filebeat / Fluent Bit"]:::container
  end
  subgraph met["Métricas"]
    prom["ico:prometheus<br/>Prometheus<br/>pull + PromQL"]:::system
    am["ico:alert<br/>Alertmanager"]:::system
    gr["ico:grafana<br/>Grafana"]:::system
  end
  subgraph logs["Logs · ELK"]
    ls["ico:logstash<br/>Logstash"]:::system
    es["ico:elasticsearch<br/>Elasticsearch"]:::system
    kb["ico:kibana<br/>Kibana"]:::system
  end
  oncall["ico:account-voice<br/>On-call"]:::person
  prom -->|"scrape"| app
  prom --> am -->|"página"| oncall
  prom --> gr
  app --> fb --> ls --> es --> kb
```

## D14 · Dinámico: gestión de cambios con ServiceNow

Pregunta: change management. Tipo: Dinámico.

```mermaid
flowchart LR
  rfc["ico:ticket-outline<br/>1 · RFC en ServiceNow<br/>riesgo, plan, rollback"]:::container
  t{"2 · Tipo de cambio"}
  st["Standard<br/>preaprobado,<br/>bajo riesgo"]:::system
  no["Normal<br/>revisión del CAB"]:::system
  em["Emergency<br/>ECAB, durante<br/>un incidente"]:::system
  ex["ico:jenkins<br/>3 · Ejecutar en la<br/>ventana, por pipeline"]:::container
  pir["ico:clipboard-check<br/>4 · Verificar y cerrar<br/>revisión posterior"]:::container
  rfc --> t
  t --> st --> ex
  t --> no --> ex
  t --> em --> ex
  ex --> pir
```

## D15 · Contenedores: gobierno como código

Pregunta: políticas de seguridad y gobierno en Azure (y GCP). Tipo: Contenedores.

```mermaid
flowchart LR
  repo["ico:git-icon<br/>Repositorio de políticas<br/>Terraform"]:::person
  pipe["ico:jenkins<br/>Pipeline<br/>prueba en modo audit"]:::container
  subgraph az["Azure"]
    ap["ico:shield-check<br/>Azure Policy<br/>Deny, Audit, Modify,<br/>DeployIfNotExists"]:::system
  end
  subgraph gcp["GCP"]
    op["ico:shield-lock<br/>Organization Policies<br/>restricciones heredadas"]:::system
  end
  subgraph k["Kubernetes"]
    gk["ico:shield-check<br/>OPA Gatekeeper<br/>admisión de manifiestos"]:::system
  end
  rep["ico:view-dashboard<br/>Reporte de cumplimiento"]:::ext
  repo --> pipe
  pipe --> ap
  pipe --> op
  pipe --> gk
  ap -.-> rep
  op -.-> rep
```

## D16 · Despliegue: red hub-and-spoke

Pregunta: diseño de red en la nube. Tipo: Despliegue.

```mermaid
flowchart LR
  onp["ico:server-network<br/>Datacenter / oficinas"]:::ext
  subgraph hub["Hub · red compartida"]
    fw["ico:shield-lock<br/>Firewall central"]:::system
    gw["ico:lan-connect<br/>VPN / ExpressRoute /<br/>Interconnect"]:::system
    dns["DNS privado"]:::system
  end
  subgraph s1["Spoke app A · prod"]
    a1["ico:kubernetes<br/>subred privada"]:::container
  end
  subgraph s2["Spoke app B · prod"]
    b1["ico:database<br/>subred privada<br/>private endpoints"]:::container
  end
  onp --> gw --> fw
  fw ---|"peering"| a1
  fw ---|"peering"| b1
```

## D17 · Contenedores: IAM sin llaves de larga duración

Pregunta: diseño de IAM y mínimo privilegio. Tipo: Contenedores.

```mermaid
flowchart LR
  hum["ico:account-group<br/>Personas<br/>grupos de Entra ID"]:::person
  sso["ico:microsoft-icon<br/>SSO / OIDC<br/>MFA"]:::ext
  subgraph cloud["Nube"]
    rb["ico:shield-check<br/>Roles por grupo<br/>mínimo privilegio, scope"]:::system
    pim["ico:timer-sand<br/>Acceso privilegiado<br/>just-in-time (PIM)"]:::system
    wi["ico:kubernetes<br/>Workload Identity /<br/>Managed Identity"]:::container
    sec["ico:lock<br/>Key Vault /<br/>Secret Manager"]:::container
  end
  ci["ico:jenkins<br/>Pipeline<br/>federación OIDC"]:::ext
  hum --> sso --> rb
  rb --> pim
  wi -->|"sin llaves en el código"| sec
  ci -->|"token corto, sin secretos"| rb
```

## D18 · Contexto: autoservicio para los equipos de aplicación

Pregunta: cómo construirías autoservicio (self-service). Tipo: Contexto.

```mermaid
flowchart LR
  team["ico:account-group<br/>Equipo de aplicación"]:::person
  subgraph plat["Plataforma cloud · golden path"]
    cat["ico:book-open-variant<br/>Catálogo de servicios<br/>formulario o PR"]:::system
    mods["ico:terraform-icon<br/>Módulos aprobados<br/>seguros por defecto"]:::container
    pipe["ico:jenkins<br/>Pipeline<br/>plan, políticas, apply"]:::container
    docs["ico:school<br/>Documentación<br/>y sesiones"]:::container
  end
  cloud["ico:google-cloud ico:azure-icon<br/>Proyecto o suscripción<br/>listo con red, IAM, logs"]:::ext
  team -->|"pide"| cat --> mods --> pipe --> cloud
  team -.->|"aprende"| docs
```

## D19 · Dinámico: optimización de costos (FinOps)

Pregunta: gestión de costos. Tipo: Dinámico.

```mermaid
flowchart LR
  a["ico:currency-usd<br/>1 · Visibilidad<br/>etiquetas obligatorias<br/>por equipo y app"]:::container
  b["ico:chart-line<br/>2 · Mostrar el costo<br/>showback por equipo"]:::container
  c["ico:content-cut<br/>3 · Optimizar<br/>rightsizing, apagar<br/>no-prod de noche"]:::container
  d["ico:cash<br/>4 · Descuentos<br/>Reservations / CUDs<br/>para lo estable"]:::container
  e["ico:alert<br/>5 · Presupuestos<br/>y alertas"]:::container
  a --> b --> c --> d --> e
  e -.->|"ciclo continuo"| a
```

## D20 · Despliegue: resiliencia y recuperación ante desastres

Pregunta: patrones de resiliencia. Tipo: Despliegue.

```mermaid
flowchart LR
  user["ico:account-group<br/>Usuarios"]:::person
  glb["ico:web<br/>Balanceador global<br/>health checks"]:::ext
  subgraph r1["Región primaria"]
    z1["ico:kubernetes<br/>Zona 1"]:::container
    z2["ico:kubernetes<br/>Zona 2"]:::container
    db1["ico:database<br/>Base de datos<br/>alta disponibilidad"]:::container
  end
  subgraph r2["Región secundaria · DR"]
    z3["ico:kubernetes<br/>Capacidad mínima<br/>o IaC lista"]:::container
    db2["ico:database<br/>Réplica / backups"]:::container
  end
  user --> glb
  glb --> z1
  glb --> z2
  glb -.->|"failover"| z3
  db1 -.->|"replicación<br/>define el RPO"| db2
```

## D21 · Contexto: estrategias de migración (las Rs)

Pregunta: cómo evalúas una aplicación para migrarla a cloud native. Tipo: Contexto.

```mermaid
flowchart LR
  app["ico:server<br/>Aplicación actual"]:::person
  ev["ico:magnify-scan<br/>Evaluación<br/>dependencias, estado,<br/>datos, equipo"]:::system
  r1["Rehost<br/>lift and shift"]:::container
  r2["Replatform<br/>a contenedores o<br/>servicios administrados"]:::container
  r3["Refactor<br/>cloud native"]:::container
  r4["Rebuild / Replace<br/>SaaS"]:::container
  r5["Retire / Retain"]:::container
  app --> ev
  ev --> r1
  ev --> r2
  ev --> r3
  ev --> r4
  ev --> r5
```

## D22 · Dinámico: troubleshooting en Linux y Windows

Pregunta: operación en Linux y Windows. Tipo: Dinámico.

```mermaid
flowchart LR
  s["ico:alert<br/>1 · Síntoma<br/>disco lleno, CPU,<br/>servicio caído"]:::container
  subgraph lx["Linux"]
    l1["ico:linux-tux<br/>df -h, du, lsof +L1<br/>journalctl, ulimit -n"]:::system
  end
  subgraph wn["Windows"]
    w1["ico:microsoft-windows-icon<br/>Event Viewer, PowerShell<br/>Get-Service, perfmon"]:::system
  end
  f["ico:check-decagram<br/>2 · Arreglo<br/>reiniciar con cuidado,<br/>liberar, rotar logs"]:::container
  p["ico:ansible<br/>3 · Prevención<br/>alerta + automatización"]:::container
  s --> l1 --> f
  s --> w1 --> f
  f --> p
```
