# Caso 3 — Arquitectura AWS e Infrastructure as Code (DevUps)

## Enunciado

Una organización necesita una plataforma para **dos equipos de desarrollo**, con **tres ambientes
independientes** (Desarrollo, QA, Producción), usando AWS, ECS (Elastic Container Service) sobre
Fargate, ALB (Application Load Balancer), Aurora, Terraform y Terragrunt. Producción requiere **alta
disponibilidad** y **toda la infraestructura debe estar como código**.

Se pide: separación de ambientes, organización de cuentas, VPC (Virtual Private Cloud) y subnets,
distribución en AZ (Availability Zones), módulos de Terraform, Terragrunt, Terraform State, secretos y
credenciales, y cómo evitar/detectar cambios manuales (*drift*).

---

## 0. Panorama: tres capas de decisión

1. **Organización (cuentas)** → dónde vive cada ambiente y quién puede tocar qué.
2. **Arquitectura (red + cómputo + datos)** → cómo se ve cada ambiente por dentro, con producción en
   alta disponibilidad.
3. **IaC (Infrastructure as Code)** → cómo se escribe, versiona, promueve y protege el código Terraform/
   Terragrunt que crea todo lo anterior.

Principio que guía todo: **los tres ambientes son el mismo código con distintos parámetros**. La
diferencia entre Desarrollo y Producción está en los *inputs* (tamaños, cantidad de AZ, réplicas), no
en código distinto.

## 1. Separación de ambientes y organización de cuentas AWS

**Una cuenta AWS por ambiente** dentro de **AWS Organizations**, idealmente montada con **AWS Control
Tower** (landing zone):

| OU (Organizational Unit) | Cuenta | Para qué |
|---|---|---|
| Root | **Management** | Solo facturación, Organizations, SCPs. Nadie despliega aquí. |
| Security | **Log Archive** | CloudTrail organizacional, AWS Config, logs centralizados (inmutables). |
| Security | **Security / Audit** | GuardDuty, Security Hub, acceso de auditoría. |
| Infrastructure | **Shared Services** | ECR (Elastic Container Registry) central, runners de CI/CD, buckets de Terraform State (opcional). |
| Workloads / NonProd | **Dev** | Ambiente de Desarrollo. |
| Workloads / NonProd | **QA** | Ambiente de QA. |
| Workloads / Prod | **Prod** | Producción. |

Por qué cuentas separadas y no solo VPC o tags:

- **Límite de seguridad fuerte**: un error o credencial comprometida en Dev **no puede** tocar Prod.
- **Blast radius** (radio de impacto) y **cuotas** independientes: un loop en Dev no consume los
  límites de Prod.
- **Costos** claros por ambiente y **SCPs (Service Control Policies)** distintas por OU (Prod más
  restrictiva).

**Los dos equipos**: comparten las cuentas de ambiente, pero se aíslan **dentro** de cada una:

- Cada equipo tiene sus **propios servicios ECS**, target groups / reglas del ALB, IAM roles de tarea,
  secretos y **su propio Terraform State** por servicio.
- Acceso humano con **IAM Identity Center (SSO)** y *permission sets* por equipo y ambiente
  (ej.: Team-A-Developer en Dev, ReadOnly en Prod).
- Tags obligatorios (`team`, `env`, `service`, `managed-by=terraform`) para costos y políticas.
- Si los equipos necesitaran aislamiento fuerte (regulación, cargas muy distintas): **una cuenta por
  equipo y ambiente** (6 cuentas). Lo propondría solo si hay una razón concreta, porque duplica la
  operación.

## 2. Red: VPC, subnets públicas y privadas

**Una VPC por cuenta/ambiente**, con **CIDR (Classless Inter-Domain Routing) que no se solapen** entre
ambientes (gestionados con **Amazon VPC IPAM**), para poder conectarlas en el futuro (Transit Gateway,
VPN) sin re-direccionar.

Tres capas de subnets en cada AZ:

| Capa | Qué vive aquí | Ruta a internet |
|---|---|---|
| **Pública** | ALB, NAT Gateways | Internet Gateway |
| **Privada de aplicación** | Tareas ECS Fargate | Solo salida, vía NAT Gateway |
| **Privada de datos** (aislada) | Aurora | **Ninguna** |

Además:

- **Security Groups encadenados**: el SG del ALB acepta 443 desde internet; el SG de ECS acepta solo
  desde el SG del ALB; el SG de Aurora acepta el puerto de la base solo desde el SG de ECS.
- **VPC Endpoints** (ECR api/dkr, S3 gateway, CloudWatch Logs, Secrets Manager) → menos tráfico por NAT
  (menos costo) y el tráfico no sale a internet.
- **AWS WAF (Web Application Firewall)** delante del ALB, certificado de **ACM (AWS Certificate
  Manager)** y **VPC Flow Logs** enviados a Log Archive.

## 3. Distribución en Availability Zones (alta disponibilidad)

| | Dev | QA | **Prod** |
|---|---|---|---|
| AZ | 2 | 2 | **3** |
| NAT Gateway | 1 (ahorro) | 1 | **1 por AZ** (si cae una AZ, las otras siguen saliendo) |
| ECS | 1 tarea por servicio | 1-2 | **mínimo 1 tarea por AZ (3)**, Auto Scaling, *deployment circuit breaker* con rollback |
| Aurora | Serverless v2 o instancia pequeña, sin réplica | 1 writer + 1 reader | **1 writer + réplicas en otras AZ** (failover automático ~30 s), deletion protection, backups + PITR (Point-In-Time Recovery) |
| ALB | Multi-AZ (siempre) | Multi-AZ | Multi-AZ, cross-zone |

- ECS Fargate reparte las tareas entre las subnets de las AZ configuradas; el ALB solo envía tráfico a
  tareas sanas (health checks).
- Aurora guarda **6 copias de los datos en 3 AZ** a nivel de almacenamiento; las réplicas en otras AZ
  permiten que el failover del writer sea rápido.
- Dev y QA se pueden **apagar fuera de horario** (ECS en 0, Aurora pausada) para ahorrar.

## 4. Organización de módulos Terraform

**Dos repositorios** (patrón clásico de Terragrunt):

1. **`infra-modules`** — módulos reutilizables, **versionados con tags semánticos** (`v1.4.0`):

   ```text
   modules/
     network/         # VPC, subnets, NAT, endpoints, flow logs
     alb/             # ALB, listeners, certificados, WAF
     ecs-cluster/     # cluster, capacity providers, logs
     ecs-service/     # task definition, servicio, autoscaling, SG, IAM de tarea
     aurora/          # cluster, instancias, parameter groups, backups, SG
     iam-baseline/    # roles de CI/CD, permission boundaries
     observability/   # alarmas, dashboards
   ```

   - Cada módulo: `variables.tf` con validaciones, `outputs.tf`, `README`, ejemplos.
   - Pueden **envolver** módulos comunitarios (`terraform-aws-modules/vpc/aws`) fijando versiones.
   - CI del repo: `terraform fmt`, `terraform validate`, **tflint**, **Checkov/Trivy** (seguridad),
     `terraform test` o **Terratest**.
   - El módulo `ecs-service` es el "producto" que usan los dos equipos: un equipo crea un servicio
     nuevo con ~15 líneas de inputs.

2. **`infra-live`** — la configuración **real** de cada ambiente con Terragrunt (siguiente punto).

## 5. Uso de Terragrunt

Terragrunt resuelve tres problemas de Terraform puro: **repetir** la configuración del backend y del
provider en cada carpeta, **conectar** componentes entre sí y **ejecutar** muchos a la vez.

```text
infra-live/
  root.hcl                     # remote_state + generate "provider" (una sola vez para todos)
  _envcommon/                  # inputs comunes por componente (ej.: ecs-service.hcl)
  dev/
    account.hcl                # account_id, rol a asumir
    env.hcl                    # env = "dev", tamaños
    us-east-1/
      region.hcl
      network/terragrunt.hcl
      aurora/terragrunt.hcl
      ecs-cluster/terragrunt.hcl
      alb/terragrunt.hcl
      services/
        team-a-api/terragrunt.hcl
        team-b-api/terragrunt.hcl
  qa/   ...misma estructura...
  prod/ ...misma estructura...
```

Piezas clave:

- **`include`** del `root.hcl` → backend y provider definidos **una vez** (DRY, Don't Repeat Yourself).
- **`terraform { source = "git::.../infra-modules.git//modules/aurora?ref=v1.4.0" }`** → cada ambiente
  fija **qué versión** del módulo usa. **Promoción**: se sube el `ref` primero en Dev, luego QA y por
  último Prod.
- **`dependency`** → `aurora` lee los `outputs` de `network` (IDs de subnets) sin hardcodearlos, y
  Terragrunt calcula el **orden** de ejecución.
- **`read_terragrunt_config` / locals** para leer `account.hcl`, `env.hcl`, `region.hcl`.
- **`terragrunt run --all plan`** (antes `run-all`) para planear un ambiente completo.

## 6. Manejo de Terraform State

- **Backend remoto en S3**, generado por Terragrunt desde `root.hcl`:
  - **Un bucket por cuenta/ambiente** (o en Shared Services con prefijos por cuenta), con
    **Versioning**, **cifrado con KMS (Key Management Service)**, **Block Public Access** y política
    que solo permite el rol de CI/CD.
  - **Locking**: tabla **DynamoDB**, o el **lock nativo de S3** (`use_lockfile = true`, Terraform ≥ 1.10)
    → evita dos `apply` simultáneos.
- **Un state por componente por ambiente** (`prod/us-east-1/aurora/terraform.tfstate`): un `apply` del
  servicio del equipo A no puede romper la red ni la base del equipo B, y los planes son rápidos.
- El state **puede contener datos sensibles** → tratarlo como un secreto: acceso mínimo, auditado con
  CloudTrail. Versioning permite recuperar un state corrupto.

## 7. Secretos y credenciales

**Secretos de la aplicación**:

- **AWS Secrets Manager** (o SSM Parameter Store SecureString para configuración), un **KMS key por
  ambiente**.
- **Aurora con `manage_master_user_password = true`**: RDS genera la contraseña, la guarda en Secrets
  Manager y la **rota**; la contraseña **nunca pasa por el código ni por el Terraform State**.
- En Terraform reciente: **ephemeral resources** y argumentos *write-only* (`password_wo`) para lo
  que sí deba pasar por Terraform sin quedar en el state.
- ECS inyecta los secretos en el container con el bloque **`secrets`** de la task definition
  (referencia al ARN); el **task execution role** solo puede leer los secretos de *ese* servicio.
- Nunca secretos en `.tfvars`, en Git ni en variables de entorno en texto plano; **secret scanning**
  (gitleaks / GitHub secret scanning) en el CI.

**Credenciales para desplegar**:

- **CI/CD con OIDC (OpenID Connect)**: GitHub Actions / GitLab asume un **IAM role por cuenta** con
  credenciales temporales — **cero access keys de larga duración**.
- Rol de *plan* (solo lectura) para los PR y rol de *apply* (escritura) solo para la rama principal y
  con aprobación manual en Prod.
- **Humanos**: IAM Identity Center (SSO) con MFA; en Prod solo lectura + un rol **break-glass**
  auditado para emergencias.

## 8. Evitar y detectar cambios manuales (*drift*)

**Evitar (prevención)**:

- **Todo cambio entra por Pull Request**: `plan` automático comentado en el PR → revisión → `apply`
  desde el pipeline (GitHub Actions o **Atlantis**). Nadie corre `apply` desde su laptop en Prod.
- **Sin permisos de escritura en consola** en QA/Prod: permission sets de solo lectura.
- **SCPs** que niegan modificar recursos con tag `managed-by=terraform` a cualquier principal que no
  sea el rol del pipeline (y niegan quitar ese tag).

**Detectar**:

- **Detección de drift programada**: job nocturno con `terragrunt run --all plan -detailed-exitcode`
  en cada ambiente; **exit code 2 = hay diferencias** → alerta a Slack / ticket.
  (Alternativas gestionadas: HCP Terraform drift detection, Spacelift.)
- **AWS Config** (registro de cambios de configuración y reglas de cumplimiento) y **CloudTrail +
  EventBridge**: regla que alerta cuando un recurso es modificado por un usuario humano y no por el rol
  del pipeline.

**Corregir**: o se **re-aplica** Terraform para volver al estado del código, o, si el cambio manual era
correcto (ej.: un hotfix en un incidente), se **lleva al código** (bloque `import` / actualizar el
módulo) para que el código siga siendo la fuente de verdad.

---

## Resumen de 30 segundos (para decir en voz alta)

> "Separo los ambientes en **cuentas AWS distintas** bajo **AWS Organizations / Control Tower**, más
> cuentas de Log Archive, Security y Shared Services; los dos equipos comparten las cuentas pero se
> aíslan por servicio, rol, secretos y state. Cada ambiente tiene su **VPC** con subnets **públicas**
> (ALB, NAT), **privadas de app** (ECS Fargate) y **privadas de datos** (Aurora), con Security Groups
> encadenados. Producción va en **3 AZ**, NAT por AZ, tareas repartidas y Aurora con réplicas para
> failover. El código se divide en un repo de **módulos versionados** y un repo **live con
> Terragrunt** que reutiliza backend y provider, conecta componentes con `dependency` y promueve
> versiones de Dev a Prod. **State en S3** cifrado y con lock, uno por componente. Secretos en
> **Secrets Manager** (Aurora gestiona su propia contraseña), CI/CD con **OIDC**. Drift: cambios solo
> por PR, consola de solo lectura, SCPs, y un **plan nocturno** con `-detailed-exitcode` más **AWS
> Config** para detectarlo."
