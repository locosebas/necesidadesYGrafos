# Libreto de diapositivas - Entrevista Chubb (Cloud Engineer Ops, L1)

Plan de la presentación. Cada diapositiva tiene:

- `Sección`: Parte A (presentación personal) o Parte B (pregunta preparada).
- `Diagrama`: el o los diagramas de [diagramas-c4.md](diagramas-c4.md).
- `**EN:**` viñetas en inglés (lo que ves en pantalla por defecto) y `**ES:**` las mismas en español.
- `> EN:` lo que dices en voz alta, en inglés. `> ES:` el mismo guion en español, para entenderlo.

En la presentación: **L** cambia inglés/español, **N** muestra el guion en los dos idiomas.
Se regenera con `python3 generar_presentacion.py`.

Regla de oro (corrección del 5 nov 2026, aplica a Bizagi y MercadoLibre): **no había dev**; había
**stage** y **varios ambientes de producción**, stage iba **unos días antes** y para pasar a producción
había que **demostrar que stage estaba sano**. Siempre **build once, deploy anywhere**.

Regla de honestidad: Chubb pide 15 años y experiencia liderando transformación en GCP. Tú tienes unos
5 años intensos. No lo escondas ni lo infles: muestra profundidad práctica y velocidad de aprendizaje.

---

## Chubb · Cloud Engineer Ops · L1 Interview
**Sección:** Portada
**EN:**
- Sebastián Díaz · Cloud / DevOps Engineer
- **Part A**: who I am · **Part B**: prepared questions
- Keys: ← → move · **L** English/Spanish · **N** script
**ES:**
- Sebastián Díaz · Ingeniero Cloud / DevOps
- **Parte A**: quién soy · **Parte B**: preguntas preparadas
- Teclas: ← → moverse · **L** inglés/español · **N** guion

> EN: Interview on Monday November 9th, 2:30 pm Bogotá time, Webex, with Andre Meireles and Luis Arévalo.
> ES: Entrevista el lunes 9 de noviembre, 2:30 pm hora de Bogotá, por Webex, con Andre Meireles y Luis Arévalo. Organiza Paloma Muñoz Quintero. Duración: 30 minutos. Respira: es una conversación técnica, no un examen.

---

## What Chubb is looking for · Qué busca Chubb
**Sección:** Antes de empezar
**EN:**
- Chubb is moving apps to **containers** and building a **new GCP platform**, on top of a strong **Azure** base
- **Operate** the cloud platform: escalations, major production issues
- **Self-service** with **CI/CD for infrastructure**: Terraform, Ansible, Bash, Jenkins
- **Governance** and security policies as code, **Cloud Adoption Framework**
- **Kubernetes** (AKS, EKS), **ELK**, **Prometheus**, **ServiceNow**, **FinOps**
**ES:**
- Chubb está pasando aplicaciones a **contenedores** y construyendo una **nueva plataforma en GCP**, sobre una base fuerte en **Azure**
- **Operar** la plataforma cloud: escalamientos e incidentes mayores de producción
- **Autoservicio** con **CI/CD (Continuous Integration / Continuous Delivery) de infraestructura**: Terraform, Ansible, Bash, Jenkins
- **Gobierno** y políticas de seguridad como código, **Cloud Adoption Framework**
- **Kubernetes** (AKS, EKS), **ELK** (Elasticsearch, Logstash, Kibana), **Prometheus**, **ServiceNow**, **FinOps**

> EN: Every answer should connect to one of these five lines: operate, automate, govern, containers, cost.
> ES: Cada respuesta debe conectarse con una de estas cinco líneas: operar, automatizar, gobernar, contenedores y costos. Si te pierdes en una respuesta, vuelve a esta diapositiva mentalmente.

---

## Who I am · Quién soy
**Sección:** Parte A · Presentación personal
**Diagrama:** DA1
**EN:**
- **Cloud / DevOps Engineer**, about **5 years** of hands-on experience
- **Bizagi** (Jan 2022 – Jun 2024): DevOps Engineer on **Azure**
- **MercadoLibre** (Jun 2024 – Aug 2026): compute team of the internal **PaaS**, supporting **Mercado Pago** (regulated banking) on **AWS and GCP**
- Available **immediately**
**ES:**
- **Ingeniero Cloud / DevOps**, unos **5 años** de experiencia práctica
- **Bizagi** (ene 2022 – jun 2024): DevOps Engineer en **Azure**
- **MercadoLibre** (jun 2024 – ago 2026): equipo de cómputo del **PaaS (Platform as a Service)** interno, dando soporte a **Mercado Pago** (banca regulada) en **AWS y GCP**
- Disponible **de inmediato**

> EN: Hi, I'm Sebastián Díaz, a Cloud and DevOps engineer with about five years of hands-on experience. Until August I worked at Mercado Libre, in the compute team of the internal platform, the PaaS, supporting Mercado Pago, which is a regulated banking environment, on AWS and GCP. Before that I spent two and a half years at Bizagi as a DevOps engineer on Azure. So I've operated cloud platforms in two clouds that Chubb cares about, Azure and GCP, in regulated industries. I'm available immediately.
> ES: Hola, soy Sebastián Díaz, ingeniero Cloud y DevOps con unos cinco años de experiencia práctica. Hasta agosto trabajé en MercadoLibre, en el equipo de cómputo de la plataforma interna, el PaaS, dando soporte a Mercado Pago, que es un entorno bancario regulado, en AWS y GCP. Antes estuve dos años y medio en Bizagi como DevOps engineer en Azure. O sea, he operado plataformas cloud en las dos nubes que le importan a Chubb, Azure y GCP, en industrias reguladas. Estoy disponible de inmediato.

---

## Bizagi: Azure, CI/CD and observability · Bizagi: Azure, CI/CD y observabilidad
**Sección:** Parte A · Presentación personal
**Diagrama:** DA2
**EN:**
- **CI/CD** with **Azure Pipelines** and **Jenkins**: build once, deploy anywhere
- **Stage** first, a few days before **several production environments**
- **Grafana** dashboards and alerts, with **automated onboarding** I led; **on-call**
- **SSO / OIDC** integrations with **Entra ID** and external identity providers
- Platform under **health-industry compliance** standards
**ES:**
- **CI/CD** con **Azure Pipelines** y **Jenkins**: build once, deploy anywhere (se crea la versión una vez y se despliega esa misma)
- Primero **stage**, unos días antes que los **varios ambientes de producción**
- Tableros y alertas en **Grafana**, con **onboarding automatizado** que lideré; **on-call** (guardias)
- Integraciones **SSO / OIDC** (Single Sign-On / OpenID Connect) con **Entra ID** y proveedores de identidad externos
- Plataforma bajo estándares de **cumplimiento del sector salud**

> EN: At Bizagi I owned the delivery path. The pipeline built one versioned artifact, deployed it first to stage, and only when stage was proven healthy for a few days did that same version go to the production environments. I also led the automated onboarding to Grafana, so every service had dashboards and alerts from day one, and I was part of the on-call rotation. And I built SSO integrations with Entra ID and external providers using OIDC.
> ES: En Bizagi yo era responsable del camino de entrega. El pipeline creaba un artefacto versionado, lo desplegaba primero en stage, y solo cuando se demostraba que stage estaba sano durante unos días, esa misma versión iba a los ambientes de producción. También lideré el onboarding automatizado a Grafana, para que cada servicio tuviera tableros y alertas desde el primer día, y estuve en la rotación de on-call. Y construí integraciones de SSO con Entra ID y proveedores externos usando OIDC.

---

## MercadoLibre: platform engineering at scale · MercadoLibre: plataforma a escala
**Sección:** Parte A · Presentación personal
**Diagrama:** DA3
**EN:**
- **Shared Terraform modules**: state, backends, migrations without downtime
- **Kubernetes** and **ECS** as the compute layer; **Kubernetes operators** in **Go** and **Python**
- Daily troubleshooting: **CrashLoopBackOff**, **OOMKilled**, evictions; **postmortems**
- **Utilization alerts**: reactive + predictive + LLM analysis
- **Ticket diagnosis with Claude** (RAG + MCP): gives certainties and hypotheses, **does not auto-resolve**
**ES:**
- **Módulos Terraform compartidos**: state, backends, migraciones sin downtime (tiempo de inactividad)
- **Kubernetes** y **ECS** (Elastic Container Service) como capa de cómputo; **operators de Kubernetes** en **Go** y **Python**
- Troubleshooting diario: **CrashLoopBackOff**, **OOMKilled**, evictions; **postmortems**
- **Alertas de utilización**: reactiva + predictiva + análisis con LLM (Large Language Model)
- **Diagnóstico de tickets con Claude** (RAG, Retrieval-Augmented Generation + MCP, Model Context Protocol): da certezas e hipótesis, **no auto-resuelve**

> EN: At Mercado Libre I was in the compute team of the internal platform. We maintained shared Terraform modules used by many teams, so I dealt a lot with state, backends and migrations without downtime. The workloads ran on Kubernetes and ECS, and I wrote Kubernetes operators in Go and Python. I did daily troubleshooting and postmortems, built utilization alerts with a reactive layer, a predictive layer and LLM analysis, and a ticket diagnosis assistant with Claude that suggests a diagnosis but never auto-resolves: a human always decides.
> ES: En MercadoLibre estaba en el equipo de cómputo de la plataforma interna. Manteníamos módulos de Terraform compartidos que usaban muchos equipos, así que trabajé mucho con state, backends y migraciones sin downtime. Las cargas corrían en Kubernetes y ECS, y escribí operators de Kubernetes en Go y Python. Hacía troubleshooting diario y postmortems, construí alertas de utilización con una capa reactiva, una predictiva y análisis con LLM, y un asistente de diagnóstico de tickets con Claude que sugiere un diagnóstico pero nunca auto-resuelve: siempre decide una persona.

---

## Why I fit this role · Por qué encajo
**Sección:** Parte A · Presentación personal
**Diagrama:** DA4
**EN:**
- Kubernetes in production, including **AKS** and my own **operators**
- **IaC** with Terraform + pipelines in **Jenkins** and **Azure Pipelines**
- **Operations mindset**: on-call, incidents, postmortems in a **regulated** business
- **Azure** (Bizagi) + **GCP and AWS** (MercadoLibre): useful for Chubb's **new GCP platform**
- Security by default: **SSO/OIDC**, **RBAC**, least privilege
**ES:**
- Kubernetes en producción, incluido **AKS** (Azure Kubernetes Service) y mis propios **operators**
- **IaC** (Infrastructure as Code) con Terraform + pipelines en **Jenkins** y **Azure Pipelines**
- **Mentalidad de operación**: on-call, incidentes, postmortems en un negocio **regulado**
- **Azure** (Bizagi) + **GCP y AWS** (MercadoLibre): útil para la **nueva plataforma GCP** de Chubb
- Seguridad por defecto: **SSO/OIDC**, **RBAC** (Role-Based Access Control), mínimo privilegio

> EN: What I read in the role is: operate the platform today, mostly Azure, and help build the new GCP platform with automation and governance. That's exactly the combination I've worked in: Azure at Bizagi, GCP and AWS at Mercado Libre, always with Terraform, pipelines and an operations mindset. Insurance, like banking and healthcare, is regulated, and I'm used to that level of control.
> ES: Lo que leo en el cargo es: operar la plataforma hoy, sobre todo Azure, y ayudar a construir la nueva plataforma GCP con automatización y gobierno. Esa es justo la combinación en la que he trabajado: Azure en Bizagi, GCP y AWS en MercadoLibre, siempre con Terraform, pipelines y mentalidad de operación. Los seguros, como la banca y la salud, son regulados, y estoy acostumbrado a ese nivel de control.

---

## Q1 · Tell me about yourself · Háblame de ti
**Sección:** Parte B · Preguntas personales
**Diagrama:** DA1
**EN:**
- Structure: **present → past → why here** (60–90 seconds)
- Present: platform and operations, Kubernetes, Terraform, two clouds
- Past: Bizagi on Azure, then MercadoLibre on AWS and GCP
- Why here: Chubb's **GCP build** + **Azure operations**
**ES:**
- Estructura: **presente → pasado → por qué aquí** (60–90 segundos)
- Presente: plataforma y operación, Kubernetes, Terraform, dos nubes
- Pasado: Bizagi en Azure, luego MercadoLibre en AWS y GCP
- Por qué aquí: la **construcción en GCP** de Chubb + la **operación en Azure**

> EN: I'm a cloud and DevOps engineer focused on platforms and operations. In my last role at Mercado Libre I was part of the compute team of the internal PaaS, running Kubernetes and ECS on AWS and GCP with Terraform, and supporting Mercado Pago, a regulated banking product. Before that, at Bizagi, I worked on Azure with Azure Pipelines and Jenkins, Grafana monitoring and SSO integrations. What attracts me to Chubb is the combination of operating a large Azure estate and building a new GCP platform, with automation and governance from the start.
> ES: Soy ingeniero cloud y DevOps enfocado en plataformas y operación. En mi último cargo, en MercadoLibre, estaba en el equipo de cómputo del PaaS interno, corriendo Kubernetes y ECS en AWS y GCP con Terraform, y dando soporte a Mercado Pago, un producto bancario regulado. Antes, en Bizagi, trabajé en Azure con Azure Pipelines y Jenkins, monitoreo con Grafana e integraciones SSO. Lo que me atrae de Chubb es la combinación de operar un entorno grande en Azure y construir una nueva plataforma en GCP, con automatización y gobierno desde el principio.

---

## Q2 · Why Chubb? Why this role? · ¿Por qué Chubb?
**Sección:** Parte B · Preguntas personales
**EN:**
- **Transformation moment**: new GCP platform, apps moving to containers
- Global company, **regulated** industry: reliability and security matter
- The role mixes **operations** and **engineering**: what I enjoy most
- I want to grow toward **platform architecture**
**ES:**
- **Momento de transformación**: nueva plataforma GCP, aplicaciones pasando a contenedores
- Empresa global, industria **regulada**: la confiabilidad y la seguridad importan
- El cargo mezcla **operación** e **ingeniería**: lo que más disfruto
- Quiero crecer hacia **arquitectura de plataforma**

> EN: Two reasons. First, timing: Chubb is building a new GCP platform and moving applications to containers, and joining at the beginning of a platform is where you can have the most impact. Second, the role itself mixes day-to-day operations with engineering and self-service, which is exactly what I enjoy, and it's the path I want to follow toward platform architecture.
> ES: Dos razones. Primero, el momento: Chubb está construyendo una nueva plataforma GCP y pasando aplicaciones a contenedores, y entrar al principio de una plataforma es donde más impacto se puede tener. Segundo, el cargo mezcla operación del día a día con ingeniería y autoservicio, que es justo lo que disfruto, y es el camino que quiero seguir hacia arquitectura de plataforma.

---

## Q3 · Your experience with Azure · Tu experiencia en Azure
**Sección:** Parte B · Azure
**Diagrama:** D1
**EN:**
- **Entra ID** for identity: groups, SSO, OIDC
- Hierarchy: **Management Groups → Subscriptions → Resource Groups**
- **RBAC** and **Azure Policy** assigned high, **inherited** below
- **AKS**, Azure Pipelines, Azure Monitor + **Grafana**
- Separate subscriptions for **stage** and **production**
**ES:**
- **Entra ID** para identidad: grupos, SSO, OIDC
- Jerarquía: **Management Groups → Subscriptions → Resource Groups**
- **RBAC** y **Azure Policy** asignados arriba y **heredados** hacia abajo
- **AKS**, Azure Pipelines, Azure Monitor + **Grafana**
- Suscripciones separadas para **stage** y **producción**

> EN: At Bizagi, Azure was our main cloud. Identity lived in Entra ID, and access was always given to groups, not individuals. We organized resources in management groups, subscriptions and resource groups, and assigned RBAC roles and Azure Policy at the highest level that made sense, so they were inherited. Stage and production were separate subscriptions. We ran workloads on AKS and app services, and monitored with Azure Monitor and Grafana.
> ES: En Bizagi, Azure era nuestra nube principal. La identidad vivía en Entra ID y los accesos siempre se daban a grupos, no a personas. Organizábamos los recursos en management groups, suscripciones y resource groups, y asignábamos roles de RBAC y Azure Policy en el nivel más alto que tuviera sentido, para que se heredaran. Stage y producción eran suscripciones separadas. Corríamos cargas en AKS y App Services y monitoreábamos con Azure Monitor y Grafana.

---

## Q4a · GCP resource hierarchy · Jerarquía de recursos en GCP
**Sección:** Parte B · GCP
**Diagrama:** D2
**EN:**
- **Organization** → **Folders** (environment or business unit) → **Projects** (app + environment)
- **Organization Policies** and **IAM** are **inherited** downward
- **Shared VPC**: one **host project** shares subnets with service projects
- Same idea as Azure: Management Groups → Subscriptions → Resource Groups
**ES:**
- **Organization** → **Folders** (ambiente o unidad de negocio) → **Projects** (aplicación + ambiente)
- Las **Organization Policies** y el **IAM** se **heredan** hacia abajo
- **Shared VPC**: un **host project** comparte subredes con los service projects
- Misma idea que en Azure: Management Groups → Subscriptions → Resource Groups

> EN: In GCP everything hangs from the organization. Below it, folders, usually by environment or business unit, and below them projects, one per application and environment. Policies and IAM roles granted at a folder are inherited by every project inside. The network usually lives in a host project with a Shared VPC, and application projects use its subnets. It's the same idea as management groups, subscriptions and resource groups in Azure.
> ES: En GCP todo cuelga de la organización. Debajo, folders, normalmente por ambiente o unidad de negocio, y debajo de ellos projects, uno por aplicación y ambiente. Las políticas y los roles de IAM dados en un folder los heredan todos los projects de adentro. La red suele vivir en un host project con una Shared VPC, y los projects de aplicación usan sus subredes. Es la misma idea que management groups, suscripciones y resource groups en Azure.

---

## Q4b · How would you build the new GCP platform? · ¿Cómo construirías la nueva plataforma GCP?
**Sección:** Parte B · GCP
**Diagrama:** D3
**EN:**
- **Resource hierarchy**: Organization → Folders → Projects
- **Organization Policies** + **IAM by groups** at folder level
- **Shared VPC** in a host project; hybrid with **Interconnect / VPN**
- **Project factory** in Terraform = self-service
- **GKE** with **Workload Identity**; central **logging** and **Security Command Center**
**ES:**
- **Jerarquía de recursos**: Organization → Folders → Projects
- **Organization Policies** + **IAM por grupos** a nivel de folder
- **Shared VPC** en un host project; conexión híbrida con **Interconnect / VPN**
- **Project factory** en Terraform = autoservicio
- **GKE** (Google Kubernetes Engine) con **Workload Identity**; **logging** central y **Security Command Center**

> EN: I'd start with the landing zone before any workload. First identity: Cloud Identity federated with Entra ID, so people use the same SSO. Then the hierarchy: organization, folders per environment or business unit, and projects per application and environment, with Organization Policies and IAM roles granted to groups at folder level. Then networking with a Shared VPC in a host project, connected to on-premises and to Azure. Then centralized logging and security. And then a project factory in Terraform, so application teams get a ready project through a pipeline. Only after that, GKE clusters with Workload Identity and golden paths.
> ES: Empezaría por la landing zone antes de cualquier carga. Primero identidad: Cloud Identity federado con Entra ID, para que la gente use el mismo SSO. Luego la jerarquía: organización, folders por ambiente o unidad de negocio y projects por aplicación y ambiente, con Organization Policies y roles de IAM dados a grupos a nivel de folder. Luego la red con una Shared VPC en un host project, conectada al datacenter y a Azure. Luego logging y seguridad centralizados. Y después una project factory en Terraform, para que los equipos reciban un proyecto listo por pipeline. Solo después, clústeres GKE con Workload Identity y golden paths.

---

## Q5 · What is the Cloud Adoption Framework? · ¿Qué es el Cloud Adoption Framework?
**Sección:** Parte B · Gobierno
**Diagrama:** D4
**EN:**
- Microsoft's guidance to adopt the cloud **in a controlled way**
- Phases: **Strategy → Plan → Ready → Adopt** (Migrate / Innovate)
- Continuous: **Govern**, **Secure**, **Manage**
- **Ready** = the **landing zone**; GCP has its own equivalent (Google Cloud Adoption Framework)
**ES:**
- La guía de Microsoft para adoptar la nube **de forma controlada**
- Fases: **Strategy → Plan → Ready → Adopt** (Migrate / Innovate)
- Continuas: **Govern**, **Secure**, **Manage**
- **Ready** = la **landing zone**; GCP tiene su equivalente (Google Cloud Adoption Framework)

> EN: The Cloud Adoption Framework is Microsoft's methodology to adopt Azure in a controlled way. You define the strategy, the business reason, then you plan: inventory, which applications move and how. Ready is preparing the landing zone. Then Adopt, either migrating or innovating. And three disciplines run all the time: Govern, Secure and Manage. In practice, for an application team, it means: use the landing zone, follow the policies, tag your resources, and design for the standards, not around them.
> ES: El Cloud Adoption Framework es la metodología de Microsoft para adoptar Azure de forma controlada. Defines la estrategia, la razón de negocio; luego planeas: inventario, qué aplicaciones se mueven y cómo. Ready es preparar la landing zone. Luego Adopt, ya sea migrar o innovar. Y tres disciplinas corren todo el tiempo: Govern, Secure y Manage. En la práctica, para un equipo de aplicación significa: usar la landing zone, seguir las políticas, etiquetar los recursos y diseñar dentro de los estándares, no alrededor de ellos.

---

## Q6 · How do you structure Terraform? · ¿Cómo organizas Terraform?
**Sección:** Parte B · Infraestructura como código
**Diagrama:** D5
**EN:**
- **Small modules**, versioned with **tags**; each environment **pins** a version
- **One state per environment and component** → smaller blast radius
- **Remote backend** with **locking** (GCS, Azure Blob, S3)
- Differences go in **variables**, not duplicated code
**ES:**
- **Módulos pequeños**, versionados con **tags**; cada ambiente **fija** una versión
- **Un state por ambiente y componente** → menor blast radius (radio de impacto)
- **Backend remoto** con **locking** (bloqueo) (GCS, Azure Blob, S3)
- Las diferencias van en **variables**, no en código duplicado

> EN: I separate modules from environments. Modules are small, versioned with tags, and each environment pins the version it uses, so I can test a new module version in stage before production. Every environment and component has its own state in a remote backend with locking, which reduces the blast radius. Differences between environments are variables, never copied code. At Mercado Libre our shared modules were used by many teams, so versioning was critical.
> ES: Separo los módulos de los ambientes. Los módulos son pequeños, versionados con tags, y cada ambiente fija la versión que usa, así pruebo una versión nueva del módulo en stage antes de producción. Cada ambiente y componente tiene su propio state en un backend remoto con locking, lo que reduce el blast radius. Las diferencias entre ambientes son variables, nunca código copiado. En MercadoLibre nuestros módulos compartidos los usaban muchos equipos, así que el versionado era crítico.

---

## Q7 · CI/CD for infrastructure with Jenkins · CI/CD de infraestructura con Jenkins
**Sección:** Parte B · Infraestructura como código
**Diagrama:** D6
**EN:**
- **Pull request** → `fmt`, `validate`, **tflint**, **Checkov** (security scan)
- `terraform plan` published in the PR → **human review**
- Change registered in **ServiceNow**
- `apply` in **stage** → smoke tests → `apply` in **prod** with the **same reviewed plan**
- Nobody applies from a laptop
**ES:**
- **Pull request** → `fmt`, `validate`, **tflint**, **Checkov** (escaneo de seguridad)
- `terraform plan` publicado en el PR → **revisión humana**
- Cambio registrado en **ServiceNow**
- `apply` en **stage** → pruebas de humo → `apply` en **prod** con el **mismo plan revisado**
- Nadie hace apply desde su portátil

> EN: Every infrastructure change starts as a pull request. Jenkins runs format, validate, tflint and a security scan like Checkov, then runs terraform plan and posts it in the pull request, so the reviewer sees exactly what will change. After approval, and with the change registered in ServiceNow, the pipeline applies to stage, runs smoke tests, and then applies to production. The pipeline is the only identity with write permissions, nobody applies from a laptop.
> ES: Todo cambio de infraestructura empieza como un pull request. Jenkins corre format, validate, tflint y un escaneo de seguridad como Checkov, luego corre terraform plan y lo publica en el pull request, para que el revisor vea exactamente qué va a cambiar. Después de la aprobación, y con el cambio registrado en ServiceNow, el pipeline aplica en stage, corre pruebas de humo y luego aplica en producción. El pipeline es la única identidad con permisos de escritura; nadie hace apply desde su portátil.

---

## Q8 · Someone changed a resource manually · Alguien cambió algo a mano (drift)
**Sección:** Parte B · Infraestructura como código
**Diagrama:** D7
**EN:**
- **Detect**: scheduled `terraform plan` shows **drift**
- **Investigate**: Activity Log (Azure) / Audit Logs (GCP): who and why
- Correct change? → bring it into code or `terraform import`
- Wrong change? → `apply` to go back to the declared state
- **Prevent**: remove manual write access, use policies
**ES:**
- **Detectar**: un `terraform plan` programado muestra el **drift** (desviación)
- **Investigar**: Activity Log (Azure) / Audit Logs (GCP): quién y por qué
- ¿Cambio correcto? → llevarlo al código o `terraform import`
- ¿Cambio incorrecto? → `apply` para volver al estado declarado
- **Prevenir**: quitar el acceso de escritura manual, usar políticas

> EN: First I detect it, ideally with a scheduled plan that alerts on drift. Then I don't overwrite blindly: I check the activity or audit logs to understand who changed it and why, because maybe it was an emergency fix during an incident. If the change was right, I bring it into the code; if it was wrong, I apply to return to the declared state. And then I prevent it: people get read access in production and changes go through the pipeline.
> ES: Primero lo detecto, idealmente con un plan programado que alerte sobre drift. Luego no sobrescribo a ciegas: reviso los logs de actividad o auditoría para entender quién lo cambió y por qué, porque quizá fue un arreglo de emergencia durante un incidente. Si el cambio era correcto, lo llevo al código; si era incorrecto, aplico para volver al estado declarado. Y después lo prevengo: la gente tiene acceso de lectura en producción y los cambios pasan por el pipeline.

---

## Q9 · Terraform vs. Ansible · Terraform contra Ansible
**Sección:** Parte B · Infraestructura como código
**Diagrama:** D8
**EN:**
- **Terraform**: declarative, keeps **state**, **provisions** infrastructure
- **Ansible**: **agentless** (SSH / WinRM), **configures** what already exists
- Ansible is **idempotent**: `ok` vs. `changed`; reusable **roles**
- Together: Terraform creates the VM → Ansible configures OS, packages, patches
**ES:**
- **Terraform**: declarativo, guarda **state**, **aprovisiona** la infraestructura
- **Ansible**: **agentless** (sin agente) (SSH / WinRM), **configura** lo que ya existe
- Ansible es **idempotente**: `ok` contra `changed`; **roles** reutilizables
- Juntos: Terraform crea la VM → Ansible configura sistema operativo, paquetes y parches

> EN: Terraform is for provisioning: it's declarative and keeps state, so it knows what exists and what to change. Ansible is for configuration: it's agentless, connects over SSH to Linux or WinRM to Windows, and runs idempotent tasks, so running it twice gives the same result. They work together: Terraform creates the virtual machines and the network, and Ansible configures the operating system, installs packages and applies patches, which matters a lot at Chubb because the role includes Windows and Linux.
> ES: Terraform es para aprovisionar: es declarativo y guarda state, así que sabe qué existe y qué cambiar. Ansible es para configurar: es agentless, se conecta por SSH a Linux o por WinRM a Windows, y corre tareas idempotentes, así que correrlo dos veces da el mismo resultado. Trabajan juntos: Terraform crea las máquinas virtuales y la red, y Ansible configura el sistema operativo, instala paquetes y aplica parches, lo que importa mucho en Chubb porque el cargo incluye Windows y Linux.

---

## Q10 · Kubernetes architecture · Arquitectura de Kubernetes
**Sección:** Parte B · Kubernetes
**Diagrama:** D9
**EN:**
- **Control plane**: kube-apiserver, etcd, kube-scheduler, kube-controller-manager, cloud-controller-manager
- **Worker node**: kubelet, kube-proxy, container runtime (**containerd**)
- Everything goes through the **API server**
- Core idea: the **reconciliation loop** (desired state vs. actual state)
**ES:**
- **Control plane**: kube-apiserver, etcd, kube-scheduler, kube-controller-manager, cloud-controller-manager
- **Worker node**: kubelet, kube-proxy, container runtime (**containerd**)
- Todo pasa por el **API server**
- Idea central: el **reconciliation loop** (estado deseado contra estado real)

> EN: Kubernetes has a control plane and worker nodes. The control plane has the API server, the front door for everything; etcd, the key-value store with the state; the scheduler, which decides on which node each Pod runs; the controller manager, which runs the reconciliation loops; and the cloud controller manager, which talks to the cloud provider for load balancers and disks. On each worker, the kubelet makes sure the Pods are running, kube-proxy programs the network rules for Services, and containerd runs the containers. In AKS, EKS or GKE the provider manages the control plane for you.
> ES: Kubernetes tiene un control plane y worker nodes. El control plane tiene el API server, la puerta de entrada para todo; etcd, la base clave-valor con el estado; el scheduler, que decide en qué nodo corre cada Pod; el controller manager, que corre los reconciliation loops; y el cloud controller manager, que habla con el proveedor cloud para balanceadores y discos. En cada worker, el kubelet se asegura de que los Pods estén corriendo, kube-proxy programa las reglas de red de los Services y containerd corre los contenedores. En AKS, EKS o GKE el proveedor administra el control plane por ti.

---

## Q11 · AKS vs. EKS vs. GKE · Diferencias entre AKS, EKS y GKE
**Sección:** Parte B · Kubernetes
**Diagrama:** D10
**EN:**
- Same Kubernetes API; the difference is the **integration with each cloud**
- **Identity**: Entra ID + Workload Identity (AKS), IAM + IRSA / Pod Identity (EKS), Workload Identity (GKE)
- **Networking**: Azure CNI, VPC CNI, VPC-native
- **GKE Autopilot**: Google also manages the nodes
**ES:**
- La misma API de Kubernetes; la diferencia es la **integración con cada nube**
- **Identidad**: Entra ID + Workload Identity (AKS), IAM + IRSA / Pod Identity (EKS), Workload Identity (GKE)
- **Red**: Azure CNI, VPC CNI, VPC-native (CNI: Container Network Interface)
- **GKE Autopilot**: Google también administra los nodos

> EN: The Kubernetes API is the same, so manifests and Helm charts are portable. What changes is the integration: identity, networking, load balancers and upgrades. In AKS, identity comes from Entra ID and pods use Workload Identity; in EKS, IAM roles for service accounts or Pod Identity; in GKE, Workload Identity too. GKE also offers Autopilot, where Google manages the nodes. For Chubb that means we can define one standard way to deploy and keep the cloud-specific parts inside Terraform modules.
> ES: La API de Kubernetes es la misma, así que los manifiestos y los Helm charts son portables. Lo que cambia es la integración: identidad, red, balanceadores y actualizaciones. En AKS la identidad viene de Entra ID y los pods usan Workload Identity; en EKS, roles de IAM para service accounts (IRSA) o Pod Identity; en GKE, también Workload Identity. GKE además ofrece Autopilot, donde Google administra los nodos. Para Chubb eso significa que podemos definir una forma estándar de desplegar y dejar las partes específicas de cada nube dentro de módulos de Terraform.

---

## Q12 · A Pod is in CrashLoopBackOff · Un Pod en CrashLoopBackOff
**Sección:** Parte B · Kubernetes
**Diagrama:** D11
**EN:**
- `kubectl get pods` → `kubectl describe pod` (events, **exit code**)
- `kubectl logs --previous` → logs of the **crashed** container
- **Exit 137 / OOMKilled** → memory limit or a leak
- Missing **config / secret**, or a bad **liveness probe**
- Then: alert + **postmortem** so it doesn't repeat
**ES:**
- `kubectl get pods` → `kubectl describe pod` (eventos, **exit code**)
- `kubectl logs --previous` → logs del contenedor **que se cayó**
- **Exit 137 / OOMKilled** → límite de memoria o una fuga
- **Configuración o secret** faltante, o una **liveness probe** mal configurada
- Después: alerta + **postmortem** para que no se repita

> EN: CrashLoopBackOff means the container starts and dies repeatedly. I run describe pod to see the events and the exit code, and logs with the previous flag to see why the last container died. Exit code 137 with OOMKilled means memory: either the limit is too low or there's a leak. Other common causes are a missing config map or secret, or a liveness probe that kills a slow application. I fix the cause, not the symptom, and then add an alert and write the postmortem. I did this kind of troubleshooting daily at Mercado Libre.
> ES: CrashLoopBackOff significa que el contenedor arranca y muere una y otra vez. Corro describe pod para ver los eventos y el exit code, y logs con la opción previous para ver por qué murió el último contenedor. Exit code 137 con OOMKilled significa memoria: o el límite es muy bajo o hay una fuga. Otras causas comunes son un config map o un secret faltante, o una liveness probe que mata a una aplicación lenta. Arreglo la causa, no el síntoma, y luego agrego una alerta y escribo el postmortem. Este tipo de troubleshooting lo hacía a diario en MercadoLibre.

---

## Q13 · How do you handle a major production incident? · ¿Cómo manejas un incidente mayor?
**Sección:** Parte B · Operación
**Diagrama:** D12
**EN:**
- **Triage**: severity and business impact
- **Roles**: incident commander, communications
- **Mitigate first** (rollback, failover, scale), then find the root cause
- Register in **ServiceNow**: incident + **emergency change**
- **Blameless postmortem** with action items
**ES:**
- **Triage**: severidad e impacto en el negocio
- **Roles**: incident commander (quien coordina), comunicaciones
- **Mitigar primero** (rollback, failover, escalar), luego buscar la causa raíz
- Registrar en **ServiceNow**: incidente + **cambio de emergencia**
- **Postmortem sin culpas** con acciones concretas

> EN: First, triage: how many users and which business process is affected, and that sets the severity. Then roles: someone coordinates as incident commander and someone communicates, so engineers can focus. The priority is to mitigate, not to find the perfect root cause: roll back the last change, fail over, or scale. Everything is recorded in ServiceNow, and if I need to change production during the incident, it's an emergency change. Once it's stable, we find the root cause, and we finish with a blameless postmortem with concrete actions. As the engineering escalation, my job is to bring the platform knowledge to the support team.
> ES: Primero, triage: cuántos usuarios y qué proceso de negocio está afectado, y eso define la severidad. Luego los roles: alguien coordina como incident commander y alguien comunica, para que los ingenieros se concentren. La prioridad es mitigar, no encontrar la causa raíz perfecta: revertir el último cambio, hacer failover o escalar. Todo queda registrado en ServiceNow, y si necesito cambiar producción durante el incidente, es un cambio de emergencia. Cuando está estable, buscamos la causa raíz y terminamos con un postmortem sin culpas con acciones concretas. Como escalamiento de ingeniería, mi trabajo es aportar el conocimiento de la plataforma al equipo de soporte.

---

## Q14 · Monitoring and logging: Prometheus and ELK · Monitoreo y logs: Prometheus y ELK
**Sección:** Parte B · Operación
**Diagrama:** D13
**EN:**
- **Prometheus**: **pull** model, scrapes `/metrics`, queries with **PromQL**
- **Alertmanager**: routes alerts to on-call; **Grafana** for dashboards
- **ELK**: **Elasticsearch** stores, **Logstash** processes, **Kibana** visualizes; agent **Filebeat** / **Fluent Bit**
- Alert on **symptoms** the user feels (latency, errors), not only on CPU
**ES:**
- **Prometheus**: modelo **pull**, hace scrape de `/metrics`, consultas con **PromQL**
- **Alertmanager**: enruta las alertas a on-call; **Grafana** para tableros
- **ELK**: **Elasticsearch** guarda, **Logstash** procesa, **Kibana** visualiza; agente **Filebeat** / **Fluent Bit**
- Alertar por **síntomas** que siente el usuario (latencia, errores), no solo por CPU

> EN: For metrics, Prometheus uses a pull model: it scrapes the metrics endpoint of each service and you query it with PromQL. Alertmanager routes the alerts to the on-call engineer, and Grafana shows the dashboards. For logs, the ELK stack: an agent like Filebeat or Fluent Bit ships logs to Logstash, which parses them, Elasticsearch stores and indexes them, and Kibana is where you search. My rule is to alert on what the user feels, like latency and error rate, and use resource metrics for diagnosis. I worked with Grafana at Bizagi and Datadog and Grafana at Mercado Libre.
> ES: Para métricas, Prometheus usa un modelo pull: hace scrape del endpoint de métricas de cada servicio y lo consultas con PromQL. Alertmanager enruta las alertas al ingeniero de on-call y Grafana muestra los tableros. Para logs, el stack ELK: un agente como Filebeat o Fluent Bit envía los logs a Logstash, que los procesa; Elasticsearch los guarda e indexa, y Kibana es donde buscas. Mi regla es alertar por lo que siente el usuario, como latencia y tasa de errores, y usar las métricas de recursos para diagnosticar. Trabajé con Grafana en Bizagi y con Datadog y Grafana en MercadoLibre.

---

## Q15 · Change management with ServiceNow · Gestión de cambios con ServiceNow
**Sección:** Parte B · Operación
**Diagrama:** D14
**EN:**
- **RFC** (Request for Change): risk, plan, **rollback plan**, window
- **Standard**: pre-approved, low risk, repeatable
- **Normal**: reviewed by the **CAB** (Change Advisory Board)
- **Emergency**: during an incident, **ECAB**, documented after
- Executed **by pipeline**, not by hand
**ES:**
- **RFC** (Request for Change, solicitud de cambio): riesgo, plan, **plan de rollback**, ventana
- **Standard**: preaprobado, bajo riesgo, repetible
- **Normal**: lo revisa el **CAB** (Change Advisory Board, comité de cambios)
- **Emergency**: durante un incidente, **ECAB** (Emergency CAB), se documenta después
- Se ejecuta **por pipeline**, no a mano

> EN: In ServiceNow every change is a request for change with the risk, the implementation plan, the rollback plan and the window. There are three types: standard changes, which are pre-approved and repeatable, normal changes, reviewed by the Change Advisory Board, and emergency changes during an incident. I like to automate the link: the pipeline references the change number, and repeatable, low-risk infrastructure changes become standard changes, so governance doesn't slow teams down.
> ES: En ServiceNow cada cambio es una solicitud de cambio con el riesgo, el plan de implementación, el plan de rollback y la ventana. Hay tres tipos: cambios standard, preaprobados y repetibles; cambios normales, revisados por el Change Advisory Board; y cambios de emergencia durante un incidente. Me gusta automatizar el vínculo: el pipeline referencia el número de cambio, y los cambios de infraestructura repetibles y de bajo riesgo se vuelven cambios standard, para que el gobierno no frene a los equipos.

---

## Security layer (1/3): identity · Capa de seguridad (1/3): identidad
**Sección:** Glosario rápido de seguridad
**EN:**
- **Entra ID** (Azure) / **Cloud Identity** (GCP): the **directory** of users and groups → one place to manage who exists
- **SSO** (Single Sign-On): **one login** for many apps → fewer passwords, central control
- **OIDC** (OpenID Connect) / **SAML**: the **protocols** that carry the login between systems → federation between Entra ID, GCP and apps
- **MFA** (Multi-Factor Authentication): password **+ a second factor** → a stolen password is not enough
- **Federation**: GCP **trusts** Entra ID → people use the same corporate login in both clouds
**ES:**
- **Entra ID** (Azure) / **Cloud Identity** (GCP): el **directorio** de usuarios y grupos → un solo lugar para manejar quién existe
- **SSO** (Single Sign-On): **un solo inicio de sesión** para muchas aplicaciones → menos contraseñas, control central
- **OIDC** (OpenID Connect) / **SAML** (Security Assertion Markup Language): los **protocolos** que llevan el inicio de sesión entre sistemas → federación entre Entra ID, GCP y las aplicaciones
- **MFA** (Multi-Factor Authentication): contraseña **+ un segundo factor** → robar la contraseña no basta
- **Federación**: GCP **confía** en Entra ID → la gente usa el mismo login corporativo en las dos nubes

> EN: Identity answers "who are you". Entra ID is the directory, SSO gives one login, OIDC is the protocol behind it, MFA protects the login, and federation lets GCP trust Entra ID.
> ES: La identidad responde "¿quién eres?". Entra ID es el directorio, SSO da un solo inicio de sesión, OIDC es el protocolo que lo hace posible, MFA protege el inicio de sesión y la federación hace que GCP confíe en Entra ID. Truco: autenticación = quién eres; autorización (siguiente diapositiva) = qué puedes hacer.

---

## Security layer (2/3): permissions · Capa de seguridad (2/3): permisos
**Sección:** Glosario rápido de seguridad
**EN:**
- **RBAC** (Role-Based Access Control): **role + who + scope** → what you can do and where; e.g. *Reader* on a subscription
- **Least privilege**: only the permissions needed, at the **smallest scope** → limits the damage of a mistake or a stolen account
- **PIM** (Privileged Identity Management): admin rights **just-in-time**, for hours, with approval → nobody is admin permanently
- **Managed Identity** (Azure): an identity **for a resource** (VM, app, AKS) managed by Azure → the app reaches Key Vault or SQL **without passwords or keys**
- **Workload Identity** (AKS / GKE): links a Kubernetes **service account** to a cloud identity → each **Pod** gets its own permissions, no keys
- **Service account** (GCP): the identity of an application → avoid downloading its **JSON keys**
**ES:**
- **RBAC** (Role-Based Access Control): **rol + quién + scope (alcance)** → qué puedes hacer y dónde; ej. *Reader* en una suscripción
- **Mínimo privilegio**: solo los permisos necesarios, en el **scope más pequeño** → limita el daño de un error o de una cuenta robada
- **PIM** (Privileged Identity Management): permisos de administrador **just-in-time**, por horas y con aprobación → nadie es admin de forma permanente
- **Managed Identity** (Azure): una identidad **para un recurso** (VM, app, AKS) que administra Azure → la aplicación entra a Key Vault o a SQL **sin contraseñas ni llaves**
- **Workload Identity** (AKS / GKE): une una **service account** de Kubernetes con una identidad de la nube → cada **Pod** tiene sus propios permisos, sin llaves
- **Service account** (GCP): la identidad de una aplicación → evitar descargar sus **llaves JSON**

> EN: Permissions answer "what can you do". RBAC assigns a role to a group at a scope. Least privilege keeps it small. PIM makes admin temporary. And for applications, Managed Identity and Workload Identity replace passwords and keys: the cloud gives the app a short-lived token automatically.
> ES: Los permisos responden "¿qué puedes hacer?". RBAC le asigna un rol a un grupo en un scope. El mínimo privilegio lo mantiene pequeño. PIM hace que el administrador sea temporal. Y para las aplicaciones, Managed Identity y Workload Identity reemplazan contraseñas y llaves: la nube le da a la aplicación un token de corta duración automáticamente. Frase para la entrevista: "no long-lived keys".

---

## Security layer (3/3): secrets, policies and network · Capa de seguridad (3/3): secretos, políticas y red
**Sección:** Glosario rápido de seguridad
**EN:**
- **Key Vault** (Azure) / **Secret Manager** (GCP): **safe** for secrets, certificates and keys → nothing secret in code or pipelines
- **KMS** (Key Management Service) / **CMEK** (customer-managed keys): **encryption keys** → encrypt data at rest with keys the company controls
- **Azure Policy** / **Organization Policies**: **rules** applied to the whole hierarchy → block what is not allowed (public IPs, wrong regions)
- **OPA Gatekeeper**: policies **inside Kubernetes** → rejects insecure manifests (root, no limits)
- **NSG** (Network Security Group) / **firewall rules**: who can talk to whom on the network
- **Private Endpoint** / **Private Service Connect**: reach PaaS services **through a private IP** → databases never exposed to the internet
**ES:**
- **Key Vault** (Azure) / **Secret Manager** (GCP): **caja fuerte** para secretos, certificados y llaves → nada secreto en el código ni en los pipelines
- **KMS** (Key Management Service) / **CMEK** (Customer-Managed Encryption Keys): **llaves de cifrado** → cifrar los datos en reposo con llaves que controla la empresa
- **Azure Policy** / **Organization Policies**: **reglas** aplicadas a toda la jerarquía → bloquear lo que no se permite (IPs públicas, regiones no autorizadas)
- **OPA Gatekeeper** (Open Policy Agent): políticas **dentro de Kubernetes** → rechaza manifiestos inseguros (root, sin limits)
- **NSG** (Network Security Group) / **firewall rules**: quién puede hablar con quién en la red
- **Private Endpoint** / **Private Service Connect**: llegar a servicios PaaS **por una IP privada** → las bases de datos nunca quedan expuestas a internet

> EN: The rest of the security layer: Key Vault or Secret Manager keep secrets, KMS keeps encryption keys, policies stop bad configurations before they exist, NSGs and firewall rules control traffic, and private endpoints keep data services off the internet.
> ES: El resto de la capa de seguridad: Key Vault o Secret Manager guardan los secretos, KMS guarda las llaves de cifrado, las políticas frenan las malas configuraciones antes de que existan, los NSG y las firewall rules controlan el tráfico, y los private endpoints mantienen los servicios de datos fuera de internet. Resumen en capas: identidad → permisos → secretos → políticas → red.

---

## Q16 · Security policies and governance as code · Gobierno y políticas como código
**Sección:** Parte B · Gobierno y seguridad
**Diagrama:** D15
**EN:**
- **Azure Policy** effects: **Deny**, **Audit**, **Modify**, **DeployIfNotExists**
- **GCP Organization Policies**: inherited constraints
- In Kubernetes: **OPA Gatekeeper** for admission
- Policies in **Git**, deployed by **pipeline**, start in **Audit** then **Deny**
- Built **with the security team**
**ES:**
- Efectos de **Azure Policy**: **Deny**, **Audit**, **Modify**, **DeployIfNotExists**
- **GCP Organization Policies**: restricciones heredadas
- En Kubernetes: **OPA Gatekeeper** (Open Policy Agent) para admisión
- Políticas en **Git**, desplegadas por **pipeline**, empiezan en **Audit** y luego **Deny**
- Construidas **con el equipo de seguridad**

> EN: I treat policies like code: they live in Git and are deployed by a pipeline with Terraform. In Azure, Azure Policy with effects like Deny, Audit, Modify, or DeployIfNotExists, for example to force diagnostic settings. In GCP, Organization Policies, like restricting regions or forbidding public IPs. In Kubernetes, OPA Gatekeeper to reject insecure manifests. The important part is the rollout: first in Audit mode to see the impact, talk with the affected teams, and then switch to Deny.
> ES: Trato las políticas como código: viven en Git y se despliegan por pipeline con Terraform. En Azure, Azure Policy con efectos como Deny, Audit, Modify o DeployIfNotExists, por ejemplo para forzar los diagnostic settings. En GCP, Organization Policies, como restringir regiones o prohibir IPs públicas. En Kubernetes, OPA Gatekeeper para rechazar manifiestos inseguros. Lo importante es el despliegue: primero en modo Audit para ver el impacto, hablar con los equipos afectados y luego pasar a Deny.

---

## Networking layer (1/2): the building blocks · Capa de red (1/2): las piezas
**Sección:** Glosario rápido de networking
**EN:**
- **VNet** (Azure) / **VPC** (Virtual Private Cloud, GCP/AWS): your **private network** in the cloud → isolates your resources
- **Subnet** + **CIDR** (e.g. `10.20.0.0/16`): a slice of the network and its **IP range** → separate tiers (public, app, data); ranges must **not overlap**
- **Route table** / **UDR** (User-Defined Route): decides **where traffic goes** → e.g. force everything through the firewall
- **NAT Gateway** / **Cloud NAT**: lets private resources **go out** to the internet without a public IP → outbound only, nobody can come in
- **NSG** (Network Security Group) / **firewall rules**: allow or deny by IP, port and protocol → **who talks to whom**
- In GCP a **VPC is global** and its subnets are regional; in Azure a **VNet is regional**
**ES:**
- **VNet** (Virtual Network, Azure) / **VPC** (Virtual Private Cloud, GCP/AWS): tu **red privada** en la nube → aísla tus recursos
- **Subred** + **CIDR** (Classless Inter-Domain Routing, ej. `10.20.0.0/16`): un pedazo de la red y su **rango de IPs** → separar capas (pública, aplicación, datos); los rangos **no se pueden cruzar**
- **Route table** / **UDR** (User-Defined Route): decide **por dónde va el tráfico** → ej. obligar a que todo pase por el firewall
- **NAT Gateway** / **Cloud NAT** (Network Address Translation): deja que los recursos privados **salgan** a internet sin IP pública → solo salida, nadie puede entrar
- **NSG** (Network Security Group) / **firewall rules**: permiten o niegan por IP, puerto y protocolo → **quién habla con quién**
- En GCP la **VPC es global** y sus subredes son regionales; en Azure la **VNet es regional**

> EN: The network starts with a VNet or VPC, split into subnets with non-overlapping IP ranges. Route tables decide the path, NAT gives private resources outbound internet, and NSGs or firewall rules filter the traffic.
> ES: La red empieza con una VNet o una VPC, partida en subredes con rangos de IP que no se cruzan. Las route tables deciden el camino, el NAT les da salida a internet a los recursos privados, y los NSG o las firewall rules filtran el tráfico. Ojo con la diferencia que suelen preguntar: en GCP la VPC es global; en Azure y AWS es regional.

---

## Networking layer (2/2): connecting and exposing · Capa de red (2/2): conectar y exponer
**Sección:** Glosario rápido de networking
**EN:**
- **Peering**: connects two VNets/VPCs **privately** → the base of **hub-and-spoke**; it is **not transitive**
- **Shared VPC** (GCP): a **host project** owns the network, other projects use its subnets → central network team, many apps
- **VPN Gateway**: encrypted tunnel **over the internet** to the datacenter → quick and cheap
- **ExpressRoute** (Azure) / **Cloud Interconnect** (GCP): **dedicated private link** → more bandwidth, stable latency
- **Load balancer**: **L4** (TCP/UDP) or **L7** (HTTP: Application Gateway, Cloud Load Balancing) → spreads traffic, health checks
- **WAF** (Web Application Firewall): protects HTTP apps from attacks (SQL injection, XSS)
- **Private DNS zones**: resolve **private names** → needed for **Private Endpoints** to work
**ES:**
- **Peering**: conecta dos VNets/VPCs **en privado** → la base del **hub-and-spoke**; **no es transitivo** (A↔B y B↔C no da A↔C)
- **Shared VPC** (GCP): un **host project** es dueño de la red y los demás projects usan sus subredes → un equipo central de red, muchas aplicaciones
- **VPN Gateway**: túnel cifrado **por internet** hacia el datacenter → rápido y barato
- **ExpressRoute** (Azure) / **Cloud Interconnect** (GCP): **enlace privado dedicado** → más ancho de banda, latencia estable
- **Load balancer** (balanceador): **L4** (TCP/UDP) o **L7** (HTTP: Application Gateway, Cloud Load Balancing) → reparte el tráfico, health checks
- **WAF** (Web Application Firewall): protege las aplicaciones HTTP de ataques (SQL injection, XSS)
- **Zonas DNS privadas**: resuelven **nombres privados** → necesarias para que funcionen los **Private Endpoints**

> EN: To connect networks: peering between VNets or VPCs, Shared VPC in GCP, and VPN or ExpressRoute or Interconnect to the datacenter. To expose apps: load balancers at layer 4 or 7, with a WAF in front of web apps. And private DNS so private endpoints resolve correctly.
> ES: Para conectar redes: peering entre VNets o VPCs, Shared VPC en GCP, y VPN o ExpressRoute o Interconnect hacia el datacenter. Para exponer aplicaciones: balanceadores de capa 4 o de capa 7, con un WAF delante de las aplicaciones web. Y DNS privado para que los private endpoints resuelvan bien. Detalle que demuestra experiencia: el peering no es transitivo, por eso en hub-and-spoke el tráfico entre spokes pasa por el firewall del hub.

---

## Q17 · Cloud network design · Diseño de red en la nube
**Sección:** Parte B · Gobierno y seguridad
**Diagrama:** D16
**EN:**
- **Hub-and-spoke**: shared services in the hub, one spoke per app or environment
- Hub: **firewall**, **VPN / ExpressRoute / Interconnect**, private **DNS**
- Workloads in **private subnets**; data through **private endpoints**
- Plan **IP ranges** early, so they don't overlap with on-premises
**ES:**
- **Hub-and-spoke**: servicios compartidos en el hub, un spoke por aplicación o ambiente
- Hub: **firewall**, **VPN / ExpressRoute / Interconnect**, **DNS** privado
- Cargas en **subredes privadas**; datos por **private endpoints**
- Planear los **rangos de IP** desde el principio, para que no se crucen con el datacenter

> EN: The common pattern is hub-and-spoke. The hub has the shared services: the central firewall, the connection to on-premises with VPN, ExpressRoute in Azure or Interconnect in GCP, and private DNS. Each application or environment is a spoke connected by peering. Workloads stay in private subnets, and databases are reached through private endpoints. And something that is hard to fix later: plan the IP address ranges from the beginning, so they don't overlap between clouds and the datacenter.
> ES: El patrón común es hub-and-spoke. El hub tiene los servicios compartidos: el firewall central, la conexión al datacenter con VPN, ExpressRoute en Azure o Interconnect en GCP, y el DNS privado. Cada aplicación o ambiente es un spoke conectado por peering. Las cargas quedan en subredes privadas y a las bases de datos se llega por private endpoints. Y algo difícil de arreglar después: planear los rangos de IP desde el principio, para que no se crucen entre nubes y el datacenter.

---

## Q18 · IAM design and least privilege · Diseño de IAM y mínimo privilegio
**Sección:** Parte B · Gobierno y seguridad
**Diagrama:** D17
**EN:**
- People: **groups** from **Entra ID**, **SSO** + **MFA**
- Roles at the **right scope**, least privilege; **just-in-time** admin (PIM)
- Workloads: **Managed Identity** / **Workload Identity**, **no keys**
- Pipelines: **OIDC federation**, short-lived tokens
- Secrets in **Key Vault** / **Secret Manager**
**ES:**
- Personas: **grupos** de **Entra ID**, **SSO** + **MFA** (Multi-Factor Authentication)
- Roles en el **scope correcto**, mínimo privilegio; administrador **just-in-time** (PIM, Privileged Identity Management)
- Cargas: **Managed Identity** / **Workload Identity**, **sin llaves**
- Pipelines: **federación OIDC**, tokens de corta duración
- Secretos en **Key Vault** / **Secret Manager**

> EN: For people, access is always through groups synchronized from Entra ID, with SSO and MFA, and roles at the smallest scope that works. Admin rights are just-in-time with PIM, not permanent. For workloads, no long-lived keys: managed identities in Azure, Workload Identity in GKE. Pipelines authenticate with OIDC federation and get short-lived tokens. And the few secrets that remain live in Key Vault or Secret Manager. I built SSO and OIDC integrations with Entra ID at Bizagi, so this is familiar ground.
> ES: Para personas, el acceso siempre es por grupos sincronizados desde Entra ID, con SSO y MFA, y roles en el scope más pequeño que funcione. Los permisos de administrador son just-in-time con PIM, no permanentes. Para cargas, nada de llaves de larga duración: managed identities en Azure, Workload Identity en GKE. Los pipelines se autentican con federación OIDC y reciben tokens de corta duración. Y los pocos secretos que quedan viven en Key Vault o Secret Manager. En Bizagi construí integraciones SSO y OIDC con Entra ID, así que es terreno conocido.

---

## Q19 · Self-service for application teams · Autoservicio para los equipos de aplicación
**Sección:** Parte B · Plataforma
**Diagrama:** D18
**EN:**
- A **catalog**: the team asks through a form or a pull request
- **Approved Terraform modules**, secure by default
- **Pipeline** with plan, **policy checks**, apply
- Result: a project or subscription **ready** with network, IAM, logs
- **Docs and sessions** to educate teams (part of the role)
**ES:**
- Un **catálogo**: el equipo pide por formulario o por pull request
- **Módulos Terraform aprobados**, seguros por defecto
- **Pipeline** con plan, **revisión de políticas**, apply
- Resultado: un proyecto o suscripción **listo** con red, IAM y logs
- **Documentación y sesiones** para educar a los equipos (es parte del cargo)

> EN: Self-service means the application team doesn't open a ticket and wait two weeks. They choose from a catalog, through a form or a pull request, and behind it there are approved Terraform modules that are secure by default, and a pipeline that runs plan, checks the policies and applies. They receive a project or subscription ready with network, identity and logging. That's a golden path: the easy way is also the compliant way. And it needs documentation and regular sessions with the teams, which is also part of this role.
> ES: Autoservicio significa que el equipo de aplicación no abre un ticket y espera dos semanas. Escoge de un catálogo, por formulario o pull request, y detrás hay módulos de Terraform aprobados y seguros por defecto, y un pipeline que corre plan, revisa las políticas y aplica. Reciben un proyecto o suscripción listo con red, identidad y logging. Eso es un golden path: el camino fácil es también el que cumple las normas. Y necesita documentación y sesiones regulares con los equipos, que también es parte de este cargo.

---

## Q20 · Cost optimization (FinOps) · Optimización de costos (FinOps)
**Sección:** Parte B · Plataforma
**Diagrama:** D19
**EN:**
- **Visibility** first: mandatory **tags** per team and application
- **Showback**: each team sees its own cost
- **Rightsizing**, turn off **non-prod** at night, delete orphan resources
- **Reservations / Savings Plans** (Azure), **CUDs** (Committed Use Discounts, GCP) for stable workloads
- **Budgets** and alerts; it's a continuous cycle
**ES:**
- Primero **visibilidad**: **etiquetas** obligatorias por equipo y aplicación
- **Showback**: cada equipo ve su propio costo
- **Rightsizing** (ajustar el tamaño), apagar **no-producción** de noche, borrar recursos huérfanos
- **Reservations / Savings Plans** (Azure), **CUDs** (Committed Use Discounts, GCP) para cargas estables
- **Presupuestos** y alertas; es un ciclo continuo

> EN: You can't optimize what you can't see, so first visibility: mandatory tags enforced by policy, so every cost has an owner. Then showback: each team sees its cost. Then optimization with the application teams: rightsizing based on real usage, shutting down non-production at night, deleting orphan disks and IPs. For stable workloads, reservations in Azure or committed use discounts in GCP. And budgets with alerts. In Kubernetes, setting requests from measured usage is one of the biggest savings.
> ES: No puedes optimizar lo que no ves, así que primero visibilidad: etiquetas obligatorias forzadas por política, para que cada costo tenga un dueño. Luego showback: cada equipo ve su costo. Luego optimización con los equipos de aplicación: rightsizing según el uso real, apagar no-producción de noche, borrar discos e IPs huérfanos. Para cargas estables, reservations en Azure o committed use discounts en GCP. Y presupuestos con alertas. En Kubernetes, definir los requests según el uso medido es uno de los mayores ahorros.

---

## Q21 · Resilience and disaster recovery · Resiliencia y recuperación ante desastres
**Sección:** Parte B · Plataforma
**Diagrama:** D20
**EN:**
- **Availability zones** inside a region for high availability
- A **second region** for disaster recovery
- **RTO** (how long to recover) and **RPO** (how much data you can lose) decide the design
- **Global load balancer** with health checks; database **replication**
- **Test** the failover; a DR plan never tested doesn't exist
**ES:**
- **Zonas de disponibilidad** dentro de una región para alta disponibilidad
- Una **segunda región** para recuperación ante desastres (DR, Disaster Recovery)
- El **RTO** (Recovery Time Objective, cuánto tardas en recuperar) y el **RPO** (Recovery Point Objective, cuántos datos puedes perder) deciden el diseño
- **Balanceador global** con health checks; **replicación** de la base de datos
- **Probar** el failover; un plan de DR que nunca se probó no existe

> EN: I separate high availability from disaster recovery. High availability is spreading across availability zones in one region, so a zone failure is invisible. Disaster recovery is a second region, and the design depends on the RTO and the RPO the business needs: from backups and infrastructure as code ready to deploy, to a warm standby with replication. With Terraform, rebuilding a region is much faster. And the most important part: test the failover regularly.
> ES: Separo alta disponibilidad de recuperación ante desastres. Alta disponibilidad es repartir entre zonas de disponibilidad en una región, para que la caída de una zona sea invisible. Recuperación ante desastres es una segunda región, y el diseño depende del RTO y el RPO que necesite el negocio: desde backups e infraestructura como código lista para desplegar, hasta un warm standby con replicación. Con Terraform, reconstruir una región es mucho más rápido. Y lo más importante: probar el failover con regularidad.

---

## Q22 · Moving an application to cloud native · Llevar una aplicación a cloud native
**Sección:** Parte B · Plataforma
**Diagrama:** D21
**EN:**
- **Assess** first: dependencies, state, data, team skills, business value
- **Rehost** (lift and shift), **Replatform** (containers, managed services), **Refactor**
- Also **Replace** (SaaS), **Retire**, **Retain**
- Usual sweet spot: **replatform** to containers, then refactor step by step
**ES:**
- Primero **evaluar**: dependencias, estado, datos, habilidades del equipo, valor de negocio
- **Rehost** (lift and shift), **Replatform** (contenedores, servicios administrados), **Refactor**
- También **Replace** (SaaS), **Retire** (retirar), **Retain** (mantener)
- Punto medio habitual: **replatform** a contenedores y luego refactorizar paso a paso

> EN: I'd assess the application first: does it keep state on local disk, what are its dependencies, how does it handle configuration and secrets, and what's its business value. Then pick a strategy: rehost, replatform, refactor, replace with SaaS, retire, or retain. For many applications the sweet spot is replatform: put it in a container, externalize the configuration, use a managed database, and then refactor step by step. The goal is to give the team a clear path, not a big-bang rewrite.
> ES: Primero evaluaría la aplicación: si guarda estado en disco local, cuáles son sus dependencias, cómo maneja configuración y secretos, y cuál es su valor de negocio. Luego escoger una estrategia: rehost, replatform, refactor, reemplazar con SaaS, retirar o mantener. Para muchas aplicaciones el punto medio es replatform: meterla en un contenedor, sacar la configuración, usar una base de datos administrada y luego refactorizar paso a paso. El objetivo es darle al equipo un camino claro, no una reescritura de golpe.

---

## Q23 · Linux and Windows operations · Operación en Linux y Windows
**Sección:** Parte B · Operación
**Diagrama:** D22
**EN:**
- Formula: **symptom → hypothesis → command → fix → prevention**
- Linux: `df -h` vs. `du`; `lsof +L1` (deleted files still open); `ulimit -n`; `journalctl`
- Windows: **Event Viewer**, **PowerShell** (`Get-Service`, `Get-EventLog`), **perfmon**
- Prevention: alerts + automation with **Ansible**
**ES:**
- Fórmula: **síntoma → hipótesis → comando → arreglo → prevención**
- Linux: `df -h` contra `du`; `lsof +L1` (archivos borrados que siguen abiertos); `ulimit -n`; `journalctl`
- Windows: **Event Viewer**, **PowerShell** (`Get-Service`, `Get-EventLog`), **perfmon**
- Prevención: alertas + automatización con **Ansible**

> EN: I always follow the same formula: confirm the symptom, make a hypothesis, check it with a command, fix it, and prevent it. For example, the disk is full but du shows little usage: the hypothesis is a deleted file that a process still has open, so I run lsof plus L1, and restart or reload that process. On Windows, I start with Event Viewer and PowerShell. And prevention is an alert plus automation, for example log rotation configured with Ansible.
> ES: Siempre sigo la misma fórmula: confirmar el síntoma, plantear una hipótesis, comprobarla con un comando, arreglar y prevenir. Por ejemplo, el disco está lleno pero du muestra poco uso: la hipótesis es un archivo borrado que un proceso todavía tiene abierto, así que corro lsof +L1 y reinicio o recargo ese proceso. En Windows empiezo por el Event Viewer y PowerShell. Y la prevención es una alerta más automatización, por ejemplo la rotación de logs configurada con Ansible.

---

## Q24 · The role asks for 15 years · El cargo pide 15 años
**Sección:** Parte B · Preguntas difíciles
**EN:**
- Be **honest**: about **5 intense years**, not 15
- **Depth**: production platforms in 3 clouds, regulated industries
- **Proof of learning speed**: operators in Go, LLM tools, multi-cloud
- Offer **value now**: operations, Terraform, Kubernetes from day one
**ES:**
- Ser **honesto**: unos **5 años intensos**, no 15
- **Profundidad**: plataformas en producción en 3 nubes, industrias reguladas
- **Prueba de velocidad de aprendizaje**: operators en Go, herramientas con LLM, multi-cloud
- Ofrecer **valor desde ya**: operación, Terraform y Kubernetes desde el primer día

> EN: You're right, I have about five years, not fifteen. But they were intense years in production: two regulated industries, three clouds, shared platforms used by many teams. I can contribute from day one in operations, Terraform and Kubernetes, and I learn fast: I went from operating Kubernetes to writing operators in Go. For the leadership parts of the role, I'd love to grow into them with the team.
> ES: Tienes razón, tengo unos cinco años, no quince. Pero fueron años intensos en producción: dos industrias reguladas, tres nubes, plataformas compartidas que usaban muchos equipos. Puedo aportar desde el primer día en operación, Terraform y Kubernetes, y aprendo rápido: pasé de operar Kubernetes a escribir operators en Go. Para las partes de liderazgo del cargo, me encantaría crecer en ellas con el equipo.

---

## Q25 · A failure you learned from · Un error del que aprendiste
**Sección:** Parte B · Preguntas difíciles
**EN:**
- Use **STAR**: Situation, Task, Action, Result
- Choose a **real** incident: symptom, diagnosis, fix, prevention
- End with **what changed** in the process (alert, test, runbook)
- Never blame people: **blameless**
**ES:**
- Usar **STAR**: Situation, Task, Action, Result (situación, tarea, acción, resultado)
- Escoger un incidente **real**: síntoma, diagnóstico, arreglo, prevención
- Terminar con **qué cambió** en el proceso (alerta, prueba, runbook)
- Nunca culpar a personas: **blameless** (sin culpas)

> EN: Prepare one real story in four sentences: what happened, what I did to mitigate, what the root cause was, and what we changed so it never happened again. For example, a service that kept getting OOMKilled after a release: we rolled back, found the memory limit was set without measuring real usage, and changed the process so requests and limits come from measured data, plus an alert before reaching the limit.
> ES: Prepara una historia real en cuatro frases: qué pasó, qué hice para mitigar, cuál fue la causa raíz y qué cambiamos para que no volviera a pasar. Por ejemplo, un servicio que se seguía cayendo por OOMKilled después de un release: hicimos rollback, encontramos que el límite de memoria se había puesto sin medir el uso real, y cambiamos el proceso para que los requests y limits salgan de datos medidos, más una alerta antes de llegar al límite. Ajusta el ejemplo a un caso que de verdad hayas vivido.

---

## Questions for them · Preguntas para ellos
**Sección:** Cierre
**EN:**
- How is the work split between the **operations** and **engineering** teams?
- Where is the **GCP platform** today: landing zone ready, or still being designed?
- What does **on-call** look like for this role?
- How do you measure success in the **first 90 days**?
- What are the next steps in the process?
**ES:**
- ¿Cómo se divide el trabajo entre los equipos de **operación** e **ingeniería**?
- ¿En qué punto está la **plataforma GCP**: la landing zone ya está lista o todavía se está diseñando?
- ¿Cómo es el **on-call** en este cargo?
- ¿Cómo miden el éxito en los **primeros 90 días**?
- ¿Cuáles son los siguientes pasos del proceso?

> EN: Ask two or three of these, not all. The GCP question shows interest in the main project, and the 90 days question tells you what they really expect.
> ES: Haz dos o tres de estas, no todas. La pregunta de GCP muestra interés en el proyecto principal, y la de los 90 días te dice qué esperan de verdad. Cierra agradeciendo a Andre y a Luis por su tiempo.
