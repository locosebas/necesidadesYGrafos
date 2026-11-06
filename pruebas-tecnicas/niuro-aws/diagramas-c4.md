# Diagramas C4 - Entrevista Niuro (AWS Infrastructure Engineer)

Un diagrama C4 (Context, Containers, Components, Code) por idea, uno o más por pregunta de la
entrevista ([README.md](README.md)). Están en Mermaid, así que GitHub los dibuja directo. Los usa el
[libreto](libreto-diapositivas.md) y el generador de la [presentación](presentacion.html).

Convenciones de color (las del modelo C4):

- **Azul oscuro**: persona.
- **Azul medio**: sistema propio.
- **Azul claro**: contenedor (servicio, base de datos, pipeline).
- **Gris**: sistema externo.
- **Recuadro punteado**: límite (cuenta, VPC, zona, ambiente).

Íconos: cada `ico:nombre` es el logo de la herramienta, guardado en [iconos/](iconos/) (logos de
[Iconify](https://icon-sets.iconify.design/): sets `logos`, `mdi`, `devicon` y `simple-icons`). En GitHub
se ven como texto; en la presentación HTML se ven como logos.

Tipos de diagrama C4 que aparecen: **Contexto** (el sistema y quién lo usa), **Contenedores** (las
piezas que se despliegan), **Componentes** (el interior de una pieza), **Dinámico** (pasos numerados en
orden) y **Despliegue** (dónde corre cada cosa en la infraestructura).

---

## D1 · Contexto: mi rol en dos plataformas

Pregunta 1. Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Sebastián Díaz<br/>DevOps / Infraestructura cloud"]:::person
  subgraph meli["MercadoLibre · jun 2024 - ago 2026"]
    mp["ico:mercadopago<br/>Plataforma de infraestructura<br/>Mercado Pago (línea bancaria)"]:::system
  end
  subgraph biz["Bizagi · ene 2022 - jun 2024"]
    bz["ico:dotnet<br/>Plataforma Bizagi (.NET)<br/>con cumplimiento de salud"]:::system
  end
  aws["ico:aws ico:google-cloud<br/>AWS y GCP"]:::ext
  az["ico:azure-icon<br/>Azure"]:::ext
  obs["ico:datadog ico:grafana<br/>Datadog / Grafana"]:::ext
  yo -->|"Terraform, ECS, Kubernetes,<br/>postmortems"| mp
  yo -->|"CI/CD, release management,<br/>on-call"| bz
  mp -->|"corre sobre"| aws
  bz -->|"corre sobre"| az
  mp -.->|"monitoreo"| obs
  bz -.->|"monitoreo"| obs
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D2a · Contexto: cargas financieras sensibles en AWS

Pregunta 2. Tipo: Contexto.

```mermaid
flowchart LR
  cli["ico:account-group<br/>Cliente de Mercado Pago"]:::person
  dev["ico:account-group<br/>Equipo DevOps"]:::person
  svc["ico:aws-ecs ico:kubernetes<br/>Servicios financieros<br/>en contenedores"]:::system
  tf["ico:terraform-icon<br/>Terraform<br/>módulos con línea base segura"]:::system
  aws["ico:aws<br/>AWS<br/>VPC, ECS, EKS, RDS, KMS, IAM"]:::ext
  sec["ico:aws-secrets-manager<br/>Gestor de secretos"]:::ext
  dr["ico:backup-restore<br/>Región secundaria<br/>recuperación ante desastres"]:::ext
  cli -->|"HTTPS / TLS"| svc
  dev -->|"pull request + plan"| tf
  tf -->|"aprovisiona"| aws
  svc -->|"corre en"| aws
  svc -->|"lee secretos en ejecución"| sec
  aws -.->|"réplica"| dr
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D2b · Contenedores: aislamiento y menor privilegio

Pregunta 2. Tipo: Contenedores.

```mermaid
flowchart LR
  cli["ico:account-group<br/>Cliente"]:::person
  subgraph vpc["VPC (Virtual Private Cloud)"]
    subgraph pub["Subred pública"]
      alb["ico:aws-elb<br/>ALB<br/>balanceador de aplicaciones"]:::container
    end
    subgraph priv["Subred privada de aplicación"]
      s1["ico:aws-ecs ico:aws-iam<br/>Servicio A en ECS<br/>rol IAM propio"]:::container
      s2["ico:kubernetes ico:aws-iam<br/>Servicio B en Kubernetes<br/>rol IAM propio"]:::container
    end
    subgraph data["Subred de datos"]
      db[("ico:aws-rds<br/>Base de datos<br/>cifrada con KMS")]:::container
    end
  end
  sm["ico:aws-secrets-manager<br/>Gestor de secretos"]:::ext
  kms["ico:aws-kms<br/>KMS<br/>llaves de cifrado"]:::ext
  cli -->|"443 TLS"| alb
  alb --> s1
  alb --> s2
  s1 -->|"TLS"| db
  s2 -->|"TLS"| db
  s1 -.->|"secretos"| sm
  s2 -.->|"secretos"| sm
  db -.->|"cifrado en reposo"| kms
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D3a · Contenedores: blue/green con base de datos compartida

Pregunta 3. Tipo: Contenedores.

```mermaid
flowchart LR
  u["ico:account-group<br/>Usuarios"]:::person
  lb["ico:aws-elb<br/>Balanceador<br/>decide a quién va el tráfico"]:::container
  blue["ico:docker-icon<br/>BLUE v1<br/>lee y escribe columnas viejas"]:::container
  green["ico:docker-icon<br/>GREEN v2<br/>escribe en viejas y nuevas,<br/>lee de las nuevas"]:::container
  db[("ico:postgresql<br/>Base de datos compartida<br/>esquema EXPANDIDO:<br/>viejo + nuevo a la vez")]:::container
  mig["ico:git-icon<br/>Pipeline de migraciones<br/>versionadas, antes del deploy"]:::system
  u --> lb
  lb -->|"tráfico actual"| blue
  lb -.->|"tráfico tras el switch"| green
  blue --> db
  green --> db
  mig -->|"solo cambios aditivos"| db
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D3b · Dinámico: las cinco fases de expand/contract

Pregunta 3. Tipo: Dinámico.

```mermaid
flowchart LR
  e1["ico:database<br/>1 EXPAND<br/>agregar columnas o tablas<br/>nulas o con default"]:::container
  e2["ico:docker-icon<br/>2 DEPLOY GREEN<br/>doble escritura,<br/>lectura con fallback"]:::container
  e3["ico:timer-sand<br/>3 BACKFILL<br/>migrar histórico<br/>en lotes pequeños"]:::container
  e4["ico:swap-horizontal<br/>4 SWITCH<br/>tráfico a green;<br/>rollback a blue seguro"]:::container
  e5["ico:check-decagram<br/>5 CONTRACT<br/>borrar lo viejo<br/>en un release posterior"]:::system
  e1 --> e2 --> e3 --> e4 --> e5
  e4 -.->|"si falla"| rb["ico:backup-restore<br/>Rollback a blue<br/>el esquema viejo sigue intacto"]:::ext
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D4a · Contenedores: módulos, ambientes y estado remoto de Terraform

Pregunta 4. Tipo: Contenedores. Ambientes reales: **stage + varios de producción, sin dev**.

```mermaid
flowchart TB
  dev["ico:account<br/>Ingeniero DevOps"]:::person
  mods["ico:terraform-icon ico:git-icon<br/>Repositorio de módulos<br/>red, cómputo, BD, IAM<br/>versionados con tags"]:::system
  envs["ico:terraform-icon<br/>Repositorio de ambientes<br/>stage, prod-1 ... prod-N<br/>fijan versión del módulo"]:::system
  pipe["ico:circleci ico:jenkins<br/>Pipeline<br/>plan y apply con rol mínimo"]:::container
  subgraph state["Estado remoto"]
    s3[("ico:aws-s3<br/>S3: un estado por<br/>ambiente y componente<br/>versionado + cifrado")]:::container
    lock[("ico:aws-dynamodb<br/>Bloqueo<br/>DynamoDB o lock nativo S3")]:::container
  end
  subgraph cuentas["Cuentas AWS"]
    stg["ico:aws<br/>Stage"]:::ext
    p1["ico:aws<br/>Producción 1"]:::ext
    pn["ico:aws<br/>Producción N"]:::ext
  end
  dev -->|"pull request"| envs
  envs -->|"usa vX.Y"| mods
  envs --> pipe
  pipe <-->|"lee / escribe"| s3
  pipe -->|"toma lock"| lock
  pipe -->|"apply primero"| stg
  pipe -->|"apply después"| p1
  pipe -->|"apply después"| pn
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D4b · Dinámico: promoción de un cambio de infraestructura

Pregunta 4. Tipo: Dinámico.

```mermaid
flowchart LR
  a["ico:source-pull<br/>1 Pull request"]:::container --> b["ico:terraform-icon<br/>2 terraform plan<br/>en el pipeline"]:::container
  b --> c["ico:magnify-scan<br/>3 Revisión del plan<br/>¿destroys inesperados?"]:::container
  c --> d["ico:terraform-icon<br/>4 apply en STAGE"]:::container
  d --> e["ico:timer-sand<br/>5 Unos días<br/>en observación"]:::container
  e --> f{"6 ¿Stage sano?<br/>con evidencia"}
  f -->|"sí"| g["ico:check-decagram<br/>7 apply en los<br/>ambientes de producción"]:::system
  f -->|"no"| h["Corregir y volver<br/>a empezar"]:::ext
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D5a · Dinámico: build once, deploy anywhere (.NET)

Pregunta 5. Tipo: Dinámico. Así era en **Bizagi y en MercadoLibre**.

```mermaid
flowchart LR
  subgraph crear["CREAR VERSIÓN (una sola vez)"]
    c1["ico:github-icon<br/>1 Commit / PR"]:::container --> c2["ico:dotnet ico:azuredevops ico:jenkins<br/>2 dotnet build Release<br/>+ pruebas unitarias"]:::container
    c2 --> c3["ico:package-variant-closed<br/>3 Artefacto versionado<br/>ej. 4.12.0"]:::system
  end
  repo[("ico:package-variant-closed<br/>Repositorio de artefactos")]:::container
  subgraph desplegar["DESPLEGAR LA MISMA VERSIÓN"]
    d1["ico:server<br/>4 Deploy en STAGE<br/>+ integración y humo"]:::container --> d2["ico:timer-sand<br/>5 Días en stage"]:::container
    d2 --> d3{"6 ¿Sin problemas?"}
    d3 -->|"sí"| d4["ico:check-decagram<br/>7 Deploy en<br/>producción 1 ... N"]:::system
  end
  c3 --> repo --> d1
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D5b · Contenedores: despliegue sin tiempo de inactividad

Pregunta 5. Tipo: Contenedores.

```mermaid
flowchart LR
  u["ico:account-group<br/>Usuarios"]:::person
  lb["ico:aws-elb<br/>Balanceador"]:::container
  old["ico:server<br/>Versión actual 4.11.0"]:::container
  new["ico:server<br/>Versión nueva 4.12.0<br/>levantada en paralelo"]:::container
  hc{"Health checks<br/>+ pruebas de humo"}
  repo[("ico:package-variant-closed<br/>Repositorio de artefactos<br/>4.11.0 sigue guardada")]:::container
  graf["ico:grafana<br/>Grafana<br/>salud y logs desde el día 1"]:::ext
  u --> lb
  lb -->|"tráfico"| old
  new --> hc
  hc -->|"OK: pasar tráfico"| lb
  hc -.->|"falla: rollback =<br/>redesplegar 4.11.0"| repo
  new -.-> graf
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D6a · Componentes: construcción de una imagen endurecida

Pregunta 6. Tipo: Componentes.

```mermaid
flowchart LR
  subgraph df["Dockerfile multi-stage"]
    b1["ico:docker-icon<br/>Etapa build<br/>SDK y herramientas"]:::container
    b2["ico:docker-icon ico:lock<br/>Etapa final<br/>base distroless o slim<br/>fijada por digest<br/>usuario no root"]:::container
    b1 -->|"solo copia el binario"| b2
  end
  scan{"Escáner de<br/>vulnerabilidades"}
  reg[("ico:docker-icon<br/>Registro de imágenes")]:::container
  run["ico:shield-check<br/>Contenedor en ejecución<br/>FS solo lectura<br/>sin capabilities extra"]:::system
  sm["ico:aws-secrets-manager<br/>Gestor de secretos"]:::ext
  b2 --> scan
  scan -->|"sin críticas"| reg
  scan -.->|"crítica: build falla"| x["ico:alert<br/>Bloqueado"]:::ext
  reg --> run
  sm -->|"secretos en ejecución,<br/>nunca en la imagen"| run
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D6b · Componentes: límites de recursos y alertas de capacidad

Pregunta 6. Tipo: Componentes. Lo de las alertas lo construí en MercadoLibre.

```mermaid
flowchart LR
  subgraph k8s["Kubernetes / ECS"]
    pod["ico:kubernetes ico:aws-ecs<br/>Pods o tareas<br/>requests y limits<br/>de CPU y memoria"]:::container
    hpa["ico:kubernetes<br/>Autoescalado<br/>HPA o ECS autoscaling"]:::container
    hpa -->|"más o menos réplicas"| pod
  end
  met[("ico:aws-cloudwatch ico:datadog<br/>Métricas de uso real")]:::container
  subgraph alert["Alertas de utilización"]
    r["ico:chart-line<br/>Capa reactiva<br/>uso actual"]:::system
    p["ico:chart-line<br/>Capa predictiva<br/>entrenada con histórico"]:::system
    l["ico:robot<br/>Análisis con LLM<br/>picos fuera de estacionalidad"]:::system
  end
  pod --> met
  met --> r
  met --> p
  p --> l
  r -->|"sobreaprovisionado<br/>o sin capacidad"| aj["Ajuste de requests<br/>y límites con datos"]:::ext
  l --> aj
  aj -.-> pod
  oom["ico:alert<br/>OOMKilled si el<br/>límite de memoria es corto"]:::ext
  pod -.-> oom
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D7a · Contenedores: un clúster ECS con los dos tipos de lanzamiento

Pregunta 7. Tipo: Contenedores.

```mermaid
flowchart TB
  subgraph ecs["Clúster ECS con capacity providers"]
    subgraph fg["Fargate"]
      f1["ico:aws-fargate<br/>Tarea A<br/>entorno aislado propio"]:::container
      f2["ico:aws-fargate<br/>Tarea B<br/>entorno aislado propio"]:::container
    end
    subgraph ec2["EC2 launch type"]
      h["ico:aws-ec2 ico:gpu<br/>Instancias EC2<br/>AMI endurecida, agentes,<br/>GPU si hace falta"]:::container
      t1["ico:aws-ecs<br/>Tarea C"]:::container
      t2["ico:aws-ecs<br/>Tarea D"]:::container
      h --- t1
      h --- t2
    end
  end
  awsr["ico:aws<br/>AWS parchea y opera el host"]:::ext
  you["ico:account-group<br/>Mi equipo parchea, endurece<br/>y escala las instancias"]:::person
  fg -.-> awsr
  ec2 -.-> you
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D7b · Dinámico: árbol de decisión EC2 vs Fargate

Pregunta 7. Tipo: Dinámico (decisión).

```mermaid
flowchart TB
  q0["ico:lock<br/>Servicio financiero sensible"]:::system --> q1{"¿Necesita GPU, modo privilegiado,<br/>acceso al kernel o agentes<br/>en el host por cumplimiento?"}
  q1 -->|"sí"| ec2a["ico:aws-ec2<br/>EC2"]:::container
  q1 -->|"no"| q2{"¿Carga estable y grande<br/>donde la densidad baja costos?"}
  q2 -->|"sí"| ec2b["ico:aws-ec2 ico:currency-usd<br/>EC2 con Savings Plans<br/>o Reserved Instances"]:::container
  q2 -->|"no"| fg["ico:aws-fargate<br/>FARGATE<br/>opción por defecto"]:::system
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D8 · Despliegue: VPC en tres zonas de disponibilidad

Pregunta 8. Tipo: Despliegue.

```mermaid
flowchart TB
  inet["ico:web<br/>Internet"]:::ext --> igw["ico:aws-vpc<br/>Internet Gateway"]:::container
  subgraph pub["Subredes públicas · ruta al Internet Gateway"]
    pa["ico:aws-elb<br/>Zona A<br/>ALB + NAT A"]:::container
    pb["ico:aws-elb<br/>Zona B<br/>ALB + NAT B"]:::container
    pc["ico:aws-elb<br/>Zona C<br/>ALB + NAT C"]:::container
  end
  subgraph app["Subredes privadas de app · salen solo por NAT"]
    aa["ico:aws-ecs<br/>Zona A<br/>tareas"]:::container
    ab["ico:aws-ecs<br/>Zona B<br/>tareas"]:::container
    ac["ico:aws-ecs<br/>Zona C<br/>tareas"]:::container
  end
  subgraph dat["Subredes aisladas de datos · SIN ruta a internet"]
    da[("ico:aws-rds<br/>Zona A<br/>RDS primaria<br/>Multi-AZ")]:::container
    db2[("ico:aws-rds<br/>Zona B<br/>RDS standby<br/>Multi-AZ")]:::container
    dc["ico:lock<br/>Zona C<br/>reservada"]:::container
  end
  igw --> pa & pb & pc
  pa --> aa
  pb --> ab
  pc --> ac
  aa --> da
  ab --> db2
  ac --> dc
  dat ~~~ extras["ico:aws-vpc ico:aws-cloudwatch ico:aws-systems-manager<br/>VPC Endpoints: S3, KMS, Secrets Manager<br/>VPC Flow Logs · SSM Session Manager sin bastión"]:::system
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D9 · Contenedores: cadena de security groups

Pregunta 9. Tipo: Contenedores. Cada salto solo acepta tráfico del security group anterior.

```mermaid
flowchart LR
  inet["ico:web<br/>Internet"]:::person
  alb["ico:aws-elb ico:aws-certificate-manager<br/>ALB<br/>sg-alb<br/>certificado ACM"]:::container
  app["ico:aws-ecs<br/>Backend: targets<br/>sg-app"]:::container
  db[("ico:aws-rds<br/>RDS<br/>sg-db")]:::container
  vpce["ico:aws-vpc<br/>VPC Endpoints"]:::ext
  cfg["ico:aws-config<br/>AWS Config / Security Hub<br/>detecta reglas abiertas"]:::ext
  inet -->|"entra 443<br/>desde 0.0.0.0/0"| alb
  alb -->|"8080 solo desde sg-alb<br/>incluye health checks"| app
  app -->|"5432 solo desde sg-app"| db
  app -->|"443 salida"| vpce
  cfg -.->|"audita"| alb
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```
