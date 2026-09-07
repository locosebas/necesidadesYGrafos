# IaC: de Terraform a Bicep

Ya sabés IaC (Terraform en producción). El objetivo acá no es aprender el
concepto, es traducir tu modelo mental a la sintaxis y particularidades de Bicep,
porque la vacante lo pide como IaC principal.

## Objetivos

- Leer y escribir Bicep con soltura (módulos, parámetros, outputs, loops).
- Entender qué resuelve Bicep que ARM templates no (sintaxis declarativa,
  compilación a ARM JSON, sin estado propio).
- Saber explicar la diferencia clave con Terraform: **Bicep no mantiene state
  file propio** (usa el estado de Azure Resource Manager); Terraform sí.
- Migrar mentalmente un módulo Terraform típico (red + Container App + Key Vault)
  a Bicep.

## Subtemas

1. Sintaxis básica: `param`, `var`, `resource`, `output`, `module`
2. Loops (`for`) y condicionales
3. Módulos y organización de archivos (comparar con `modules/` de Terraform)
4. `existing` resources (referenciar recursos ya creados, equivalente a `data` en Terraform)
5. Despliegue: `az deployment group create`, scopes de deployment (resourceGroup, subscription, managementGroup)
6. Bicep vs Terraform vs ARM JSON: tabla comparativa (cuándo usar cada uno)
7. Bonus: Azure Verified Modules (AVM) — módulos oficiales reutilizables

## Recursos

- Microsoft Learn — Bicep: https://learn.microsoft.com/azure/azure-resource-manager/bicep/
- Ruta de aprendizaje oficial "Fundamentals of Bicep": https://learn.microsoft.com/training/paths/fundamentals-bicep/
- Terraform docs (repaso): https://developer.hashicorp.com/terraform/docs

## Lab sugerido

Tomá un módulo Terraform que ya hayas escrito en el trabajo (o uno simple: VNet
+ subnet + NSG + storage account) y reescribilo en Bicep desde cero, sin mirar
el original hasta el final. Comparalo.

## Autoevaluación

Pedime: *"Dame un examen de Bicep nivel intermedio"* (ver `../../examenes/README.md`).
