# Identidad y autorización: Entra ID/RBAC, AWS IAM, GCP IAM

Base de seguridad de todo lo demás. Un Senior DevOps/Platform Engineer debe
poder diseñar el modelo de identidad completo de una plataforma, en cualquier
nube, no solo "crear un usuario".

## Objetivos

- Diferenciar **identidad** (quién sos) de **autorización** (qué podés hacer) en cada nube.
- Explicar identidad gestionada sin credenciales estáticas: Managed Identity
  (Azure), IAM Roles (AWS), Service Accounts (GCP) — mismo principio.
- Diseñar permisos de mínimo privilegio (roles built-in vs. custom) en las tres.
- Entender el scope jerárquico de las asignaciones en cada nube.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Identidad para humanos | Entra ID (usuarios, grupos) | IAM Users / IAM Identity Center (SSO) | Cloud Identity / Google Workspace |
| Identidad para recursos/apps | **Managed Identity** (system o user-assigned) | **IAM Role** (asumido vía instance profile, task role, etc.) | **Service Account** |
| Autorización sobre recursos | **RBAC de Azure** (roles asignados a un scope) | **IAM Policies** (adjuntas a user/role/resource) | **Cloud IAM** (roles asignados a un recurso/proyecto) |
| Jerarquía de scope | Management Group → Subscription → Resource Group → Resource | Organization → OU → Account → Resource | Organization → Folder → Project → Resource |
| Acceso temporal/privilegiado | PIM (Privileged Identity Management) | IAM Roles con `sts:AssumeRole` + sesión temporal | IAM Conditions + Temporary elevated access |
| Definición de rol custom | JSON con `Actions`/`NotActions`/`DataActions` | JSON policy con `Effect`/`Action`/`Resource`/`Condition` | YAML/JSON con `includedPermissions` |

## Subtemas

1. Azure: tenant, App Registration, Service Principal, Managed Identity — cómo se relacionan entre sí
2. AWS: diferencia entre Identity-based policies y Resource-based policies; `AssumeRole` y trust policies
3. GCP: Service Account keys (por qué evitarlas) vs. Workload Identity / impersonation
4. Principio de mínimo privilegio: cómo auditarlo en cada nube (Access Advisor en AWS, IAM Recommender en GCP, Access Reviews en Entra ID)
5. Roles built-in más usados de cada nube (equivalentes a Reader/Contributor/Owner de Azure)

## Herramienta que piden las ofertas (startup): Keycloak

**Keycloak** es un **Identity Provider (IdP) open source** (CNCF) que se
self-hostea: login, SSO, usuarios, roles, **OIDC** y **SAML** para las
aplicaciones. Cumple el rol de Entra ID / Cognito / Identity Platform cuando
la empresa no quiere depender de la nube o necesita correrlo dentro de su
Kubernetes.

| Concepto | Keycloak | Azure | AWS | GCP |
|---|---|---|---|---|
| IdP para usuarios de las apps | **Keycloak** (realm, clients, users) | Entra ID / Entra External ID | **Cognito** | Identity Platform |

Subtemas extra:
- Conceptos de **Keycloak**: *realm*, *client*, *roles*, *groups*, *identity brokering* (login con Google/Entra ID).
- Flujos **OIDC** (Authorization Code + PKCE, Client Credentials) — los mismos que usa GitHub Actions en el tema 03.
- Proteger una API FastAPI validando el JWT que emite **Keycloak**.
- Operar **Keycloak** en Kubernetes (Keycloak Operator, base de datos Postgres, alta disponibilidad).

- Keycloak: https://www.keycloak.org/documentation

## Recursos

- Entra ID: https://learn.microsoft.com/entra/
- Azure RBAC: https://learn.microsoft.com/azure/role-based-access-control/overview
- AWS IAM: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html
- GCP IAM: https://cloud.google.com/iam/docs/overview

## Lab sugerido

Diseñá el mismo modelo de identidad (una app con acceso de solo-lectura a una
base de datos y de escritura a un bucket/storage) en las tres nubes: Managed
Identity + RBAC en Azure, IAM Role + Policy en AWS, Service Account + IAM
binding en GCP. Compará cuánto código/configuración toma cada una.

## Autoevaluación

Pedime: *"Dame un examen de identidad y permisos (Entra ID/IAM/GCP IAM) nivel senior"*.
