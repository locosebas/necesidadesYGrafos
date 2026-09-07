# Infrastructure as Code: Terraform, Bicep, CloudFormation/CDK, Deployment Manager

Ya sabés IaC (Terraform en producción, en Azure y AWS). El objetivo es que
puedas escribir y leer con soltura la herramienta nativa de **cualquiera** de
las tres nubes, entendiendo qué es transferible (el concepto de IaC
declarativo, módulos, estado) y qué es específico de cada una.

## Objetivos

- Explicar el concepto de **estado** (state) y por qué cada herramienta lo
  maneja distinto.
- Escribir un módulo equivalente (red + cómputo + un servicio gestionado) en
  Terraform, y traducirlo mentalmente a Bicep y a CloudFormation/CDK.
- Saber justificar cuándo conviene la herramienta **nativa del cloud** vs.
  Terraform (multi-cloud, un solo lenguaje, gran ecosistema de providers).

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Herramienta nativa | **Bicep** (compila a ARM JSON) | **CloudFormation** (YAML/JSON) o **CDK** (código imperativo → CloudFormation) | **Deployment Manager** (legacy) o Terraform (el estándar de facto en GCP) |
| Multi-cloud / agnóstico | **Terraform** ✅ ya lo dominás | **Terraform** ✅ | **Terraform** ✅ |
| Manejo de estado | Sin state propio (usa Azure Resource Manager) | CloudFormation: stack gestionado por AWS. CDK: igual, sintetiza a CloudFormation | Terraform: state file (local o remoto en GCS) |
| Unidad de despliegue | Resource Group / deployment scope | Stack | Deployment / Terraform workspace |
| Módulos reutilizables | Bicep modules / **Azure Verified Modules (AVM)** | CloudFormation nested stacks / **CDK constructs** | Terraform modules / **Google Cloud Foundation Fabric** |

## Subtemas

1. Sintaxis básica de Bicep (`param`, `var`, `resource`, `module`) — ver detalle abajo
2. CloudFormation: templates YAML, intrinsic functions (`!Ref`, `!GetAtt`), stack sets para multi-cuenta
3. AWS CDK: por qué existe (código real — Python/TypeScript — en vez de YAML declarativo puro), síntesis a CloudFormation
4. Terraform en GCP: providers, `terraform import`, remoto state en GCS bucket
5. Comparación de manejo de drift (detección de cambios manuales fuera de IaC) en las 4 herramientas

## Detalle: Bicep (Azure)

- Sintaxis: `param`, `var`, `resource`, `output`, `module`, loops (`for`), condicionales
- `existing` resources (referenciar recursos ya creados — equivalente a `data` en Terraform)
- Despliegue: `az deployment group create`, scopes (resourceGroup, subscription, managementGroup)

## Recursos

- Bicep: https://learn.microsoft.com/azure/azure-resource-manager/bicep/
- CloudFormation: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
- AWS CDK: https://docs.aws.amazon.com/cdk/v2/guide/home.html
- Terraform (repaso): https://developer.hashicorp.com/terraform/docs
- Terraform provider de GCP: https://registry.terraform.io/providers/hashicorp/google/latest/docs

## Lab sugerido

Tomá un módulo Terraform simple (VNet/VPC + subnet + firewall/NSG + storage)
y reescribilo en **Bicep** y en **CDK (Python)**, sin mirar el original hasta
el final. Compará las tres versiones.

## Autoevaluación

Pedime: *"Dame un examen de IaC multi-cloud (Bicep/CloudFormation/Terraform) nivel intermedio"*.
