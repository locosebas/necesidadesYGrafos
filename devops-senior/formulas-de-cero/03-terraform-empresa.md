# Fórmula 03 — Proyecto Terraform que gestiona toda la infra de una empresa

**Resumen en una línea:** *decisiones → bootstrap del estado remoto →
estructura de repo (módulos + entornos + capas) → convenciones → módulos
reutilizables → CI/CD con OIDC (plan en PR, apply con aprobación) → seguridad
y políticas → drift, import y refactor → prueba.*

---

## Paso 0 — Decisiones (decilas antes de escribir código)

- ¿Una nube o varias? (Terraform brilla en multi-cloud: un lenguaje, muchos providers).
- **Blast radius**: dividir en muchos estados chicos, no un monolito.
  Criterio: *lo que cambia junto y tiene el mismo dueño, va en el mismo estado*.
- ¿Quién aplica? **Solo el pipeline** (humanos solo leen/planean).
- ¿Herramienta de orquestación? GitHub Actions / Azure Pipelines, o
  Atlantis, HCP Terraform (Terraform Cloud), Spacelift, env0.
- ¿Terraform u **OpenTofu**? (fork open source, compatible).

## Paso 1 — Bootstrap del estado remoto (el problema del huevo y la gallina)

El backend (bucket donde vive el estado) no puede crearse con un estado que
todavía no existe. Solución:

1. Carpeta `bootstrap/` con **estado local** que crea: bucket/storage account
   con **versionado + cifrado + bloqueo de acceso público**, y la identidad
   del pipeline (rol OIDC).
2. Luego se agrega el bloque `backend` y se migra:
   `terraform init -migrate-state`.

Backends por nube:

| Nube | Backend | Lock |
|---|---|---|
| AWS | S3 | `use_lockfile = true` (lock nativo en S3, Terraform ≥ 1.10; antes se usaba DynamoDB) |
| Azure | `azurerm` (Storage Account, container `tfstate`) | Lease del blob (automático) |
| GCP | `gcs` | Automático |

> El estado **contiene secretos en texto plano** (passwords generadas, etc.)
> → bucket cifrado, acceso mínimo, versionado para recuperar.

## Paso 2 — Estructura del repo

```
infra/
├── bootstrap/                   # estado local: bucket de state + roles OIDC
├── modules/                     # bloques reutilizables (sin backend, sin provider config)
│   ├── network/                 # VPC/VNet, subnets, NAT, rutas
│   ├── eks-cluster/             # o aks-cluster / gke-cluster
│   ├── postgres/                # RDS / Azure Flexible Server / Cloud SQL
│   ├── iam-role/
│   └── tagging/                 # convención de nombres y tags
└── live/                        # lo que realmente se despliega
    ├── global/
    │   ├── org/                 # cuentas/suscripciones/proyectos, SCP/políticas
    │   ├── identity/            # SSO, grupos, roles
    │   └── dns/                 # zonas públicas
    ├── dev/
    │   ├── 10-network/          # cada carpeta = un estado independiente
    │   ├── 20-data/
    │   ├── 30-k8s/
    │   └── 40-apps/
    ├── stg/ …                   # misma forma que dev
    └── prod/ …
```

- **Capas numeradas** = orden de despliegue y dependencias (red antes que
  cluster, cluster antes que apps).
- **Entornos por directorio** (más explícito y seguro que `terraform workspace`
  para separar prod de dev; workspaces sirven para copias idénticas efímeras).
- Las capas se pasan datos con `data "terraform_remote_state"`, o mejor,
  con *data sources* del recurso real o parámetros (SSM / App Config), para
  no acoplarse al estado de otra capa.
- Para reducir repetición entre entornos: **Terragrunt** o **Terraform Stacks**.

## Paso 3 — Archivos estándar de cada root module

`live/prod/10-network/`:

```hcl
# versions.tf — fijar versiones SIEMPRE
terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
  backend "s3" {
    bucket       = "empresa-tfstate-prod"
    key          = "prod/10-network/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

# providers.tf
provider "aws" {
  region = var.region
  default_tags {
    tags = { env = "prod", owner = "platform", managed_by = "terraform", cost_center = "infra" }
  }
}

# main.tf — el root solo compone módulos
module "network" {
  source   = "git::https://github.com/empresa/tf-modules.git//network?ref=v1.4.0"
  name     = "prod"
  cidr     = "10.100.0.0/16"
  azs      = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# outputs.tf
output "vpc_id"             { value = module.network.vpc_id }
output "private_subnet_ids" { value = module.network.private_subnet_ids }
```

`terraform.tfvars` para valores por entorno, **sin secretos** (esos van en
el secret manager y se leen con data source o por variable de entorno
`TF_VAR_...` en el pipeline; en versiones nuevas: *ephemeral values* y
argumentos *write-only* para que no queden en el estado).

## Paso 4 — Un módulo bien hecho

`modules/network/`:

```hcl
# variables.tf — interfaz mínima, tipada y validada
variable "name" { type = string }
variable "cidr" {
  type = string
  validation {
    condition     = can(cidrhost(var.cidr, 0))
    error_message = "cidr debe ser un bloque CIDR válido."
  }
}
variable "azs" { type = list(string) }

# main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr
  enable_dns_hostnames = true
  tags                 = { Name = var.name }
}

resource "aws_subnet" "private" {
  for_each          = { for i, az in var.azs : az => i }
  vpc_id            = aws_vpc.this.id
  availability_zone = each.key
  cidr_block        = cidrsubnet(var.cidr, 4, each.value)       # /20 por AZ
  tags              = { Name = "${var.name}-private-${each.key}", tier = "private" }
}

resource "aws_subnet" "public" {
  for_each                = { for i, az in var.azs : az => i }
  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.key
  cidr_block              = cidrsubnet(var.cidr, 8, 200 + each.value) # /24 chicas
  map_public_ip_on_launch = false
  tags                    = { Name = "${var.name}-public-${each.key}", tier = "public" }
}
# + internet gateway, NAT gateways, route tables…

# outputs.tf
output "vpc_id"             { value = aws_vpc.this.id }
output "private_subnet_ids" { value = [for s in aws_subnet.private : s.id] }
```

Reglas de un buen módulo:
- **`for_each` > `count`** (con `count`, borrar un elemento del medio recrea los siguientes).
- Sin `provider` ni `backend` adentro; el que llama decide.
- Versionado con **tags de git** (`?ref=v1.4.0`) o registry privado.
- README generado con `terraform-docs`; tests con `terraform test` (≥ 1.6).
- En vez de reinventar: módulos de la comunidad (terraform-aws-modules,
  **Azure Verified Modules**, Cloud Foundation Fabric) si cumplen.

## Paso 5 — CI/CD con OIDC (nadie aplica desde su laptop)

Flujo:

```
PR   → fmt -check → validate → tflint → checkov/trivy (seguridad) → plan
       → plan publicado como comentario del PR (+ Infracost: costo del cambio)
merge→ plan de nuevo → aprobación manual (environment "prod") → apply del MISMO plan
cron → plan -detailed-exitcode nocturno para detectar drift (exit 2 = hay cambios)
```

```yaml
# .github/workflows/terraform.yml (resumido)
name: terraform
on:
  pull_request: { paths: ["infra/**"] }
  push: { branches: [main], paths: ["infra/**"] }
permissions:
  id-token: write        # necesario para OIDC
  contents: read
  pull-requests: write
jobs:
  plan-apply:
    runs-on: ubuntu-latest
    environment: ${{ github.event_name == 'push' && 'prod' || 'plan' }}  # prod exige aprobación
    defaults: { run: { working-directory: infra/live/prod/10-network } }
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111111111111:role/gha-terraform-prod
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check -recursive
      - run: terraform init -input=false
      - run: terraform validate
      - run: terraform plan -input=false -out=tfplan
      - if: github.event_name == 'push'
        run: terraform apply -input=false tfplan
```

- Azure: `azure/login` con `client-id`/`tenant-id`/`subscription-id` y federated
  credential; GCP: `google-github-actions/auth` con Workload Identity Federation.
- Rol de **plan** (solo lectura) distinto del rol de **apply** (escritura, solo desde `main`).
- La trust policy del rol restringe el `sub` del token OIDC a
  `repo:empresa/infra:ref:refs/heads/main` / `environment:prod`.

## Paso 6 — Seguridad y gobierno

- Escaneo estático: **Checkov**, **Trivy** (ex tfsec), **tflint**.
- Políticas como código: **OPA/Conftest** o Sentinel (HCP Terraform):
  "no buckets públicos", "tags obligatorias", "solo regiones permitidas".
- Protección de rama + CODEOWNERS (cambios en `prod/` los aprueba plataforma).
- `prevent_destroy` en recursos críticos (bases de datos, estado).
- Guardrails de la nube además del IaC (SCPs, Azure Policy, Org Policies).

## Paso 7 — Operaciones del día a día

| Situación | Cómo |
|---|---|
| Recurso creado a mano que querés gestionar | bloque `import { to = ..., id = ... }` (≥ 1.5) + `terraform plan -generate-config-out=generated.tf` |
| Renombrar/mover un recurso sin recrearlo | bloque `moved { from = ..., to = ... }` (antes: `terraform state mv`) |
| Dejar de gestionar sin destruir | bloque `removed` (≥ 1.7) o `terraform state rm` |
| Drift | plan programado; decidir: ¿se corrige el código o se revierte el cambio manual? |
| Forzar recreación | `terraform apply -replace=aws_instance.x` |
| Lock trabado | `terraform force-unlock <id>` (solo si estás seguro de que nadie está aplicando) |
| Actualizar provider | cambiar versión → `terraform init -upgrade` → plan en dev primero |

## Paso 8 — Prueba "funciona"

1. `bootstrap` aplicado: existe el bucket de estado con versionado.
2. Un PR que agrega una subnet muestra el **plan en el comentario** y pasa los checks.
3. Al mergear, se pide **aprobación** y el apply usa el plan guardado.
4. Cambio algo a mano en la consola → el job nocturno de drift lo detecta.
5. `terraform plan` en todas las capas da **"No changes"** (código = realidad).

## Preguntas típicas y respuesta corta

- **¿Qué es el estado?** El mapa entre tu código y los IDs reales; permite
  calcular el diff. Se guarda remoto, cifrado, con lock.
- **¿Workspaces o directorios?** Directorios para entornos distintos
  (prod aislado, backends/permisos distintos); workspaces para copias idénticas.
- **¿Terraform vs Bicep/CloudFormation?** Nativas: sin estado propio, soporte
  día 0. Terraform: multi-cloud, un lenguaje, ecosistema enorme, plan legible.
- **¿`count` vs `for_each`?** `for_each` indexa por clave estable → evita recreaciones.
- **¿Cómo evitás que un cambio rompa todo?** Estados chicos, plan en PR,
  aprobación, dev→stg→prod, `prevent_destroy`, políticas.
