# Microsoft Entra ID, Managed Identity y RBAC

Base de seguridad de todo lo demás en Azure. Un Senior Platform Engineer debe
poder diseñar el modelo de identidad de una plataforma completa, no solo
"crear un usuario".

## Objetivos

- Diferenciar **Entra ID** (identidad) de **RBAC de Azure** (autorización sobre recursos) —
  son sistemas separados que se combinan.
- Explicar Managed Identity: **system-assigned** vs **user-assigned**, y cuándo usar cada una.
- Diseñar asignaciones de rol con mínimo privilegio (roles built-in vs custom roles).
- Entender el scope de las asignaciones: Management Group → Subscription → Resource Group → Resource.
- Service Principals vs Managed Identities vs App Registrations — de qué se
  compone cada uno y cuándo usar cada uno.

## Subtemas

1. Tenant, App Registration, Service Principal, Enterprise Application (relación entre los cuatro)
2. Managed Identity: system-assigned (ligada al ciclo de vida del recurso) vs user-assigned (recurso independiente, reutilizable)
3. Azure built-in roles clave: Reader, Contributor, Owner, `AcrPull`, `Key Vault Secrets User`, etc.
4. Custom roles (JSON de definición, `Actions`/`NotActions`/`DataActions`)
5. Conditional Access (a nivel conceptual — relevante para RBAC de usuarios humanos)
6. PIM (Privileged Identity Management) — acceso just-in-time, nice to have para senior

## Recursos

- Entra ID docs: https://learn.microsoft.com/entra/
- Azure RBAC overview: https://learn.microsoft.com/azure/role-based-access-control/overview
- Managed identities overview: https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview

## Lab sugerido

Diseñá (en un diagrama o en Bicep/Terraform) el modelo de identidad completo
de una app típica: Container App con user-assigned Managed Identity, con
`AcrPull` sobre el ACR y `Key Vault Secrets User` sobre un Key Vault específico,
sin ningún secreto embebido en la app.

## Autoevaluación

Pedime: *"Dame un examen de Entra ID y RBAC nivel senior"*.
