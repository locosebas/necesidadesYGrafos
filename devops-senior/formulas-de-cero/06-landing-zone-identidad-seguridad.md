# Fórmula 06 — Landing zone: empresa nueva en la nube (cuentas, identidad, red, secretos, seguridad)

**Resumen en una línea:** *jerarquía de cuentas → identidad (SSO + grupos +
mínimo privilegio) → guardrails → red hub-spoke → logging central y
seguridad → secretos → costos → todo con IaC.*

---

## Paso 1 — Jerarquía de cuentas / suscripciones / proyectos

| | Azure | AWS | GCP |
|---|---|---|---|
| Raíz | Tenant (Entra ID) | Organization (cuenta management) | Organization (dominio) |
| Agrupación | **Management Groups** | **Organizational Units (OUs)** | **Folders** |
| Unidad de aislamiento | **Subscription** | **Account** | **Project** |
| Contenedor de recursos | Resource Group | (tags / stacks) | (el proyecto) |
| Acelerador | Azure Landing Zones (CAF) | **Control Tower** | Cloud Foundation / Fabric FAST |

Estructura típica: `Platform` (identidad, conectividad, logging, seguridad)
+ `Workloads/prod` + `Workloads/nonprod` + `Sandbox`. **Prod en cuentas
separadas de dev** (límite de blast radius y de permisos).

## Paso 2 — Identidad

- Un **IdP** (Entra ID, Okta, Google Workspace) con **SSO + MFA** obligatorio.
- Acceso por **grupos**, no por usuarios. Roles con **mínimo privilegio**.
- AWS: IAM Identity Center + permission sets. Azure: RBAC en el scope
  correcto (MG / suscripción / RG). GCP: IAM en org/folder/proyecto.
- Acceso privilegiado **just-in-time** (Azure PIM, break-glass con alerta).
- **Workloads sin secretos**: Managed Identity (Azure), IAM roles / IRSA /
  Pod Identity (AWS), service accounts + Workload Identity (GCP).
  Para CI externos: **federación OIDC**.

## Paso 3 — Guardrails (lo que nadie puede hacer, ni siquiera un admin de la cuenta)

- AWS **SCPs**, **Azure Policy**, GCP **Organization Policies**.
- Ejemplos: solo regiones permitidas, prohibido IP pública en VMs,
  cifrado obligatorio, no desactivar CloudTrail/logs, tags obligatorias.

## Paso 4 — Red

- **Hub-and-spoke** (Azure VNet peering / Virtual WAN; AWS **Transit Gateway**;
  GCP **Shared VPC** o NCC).
- Hub: firewall central, VPN/ExpressRoute/Direct Connect, DNS resolver.
- Acceso privado a PaaS: **Private Endpoints + Private DNS zones** (Azure),
  **VPC endpoints / PrivateLink** (AWS), **Private Service Connect** (GCP).
- NSG / Security Groups / firewall rules con deny by default.
- Plan de IPs sin solapamiento con on-prem (fórmula 02).

## Paso 5 — Logging y seguridad centralizados

- Cuenta/suscripción de **log archive** inmutable: CloudTrail org trail,
  Azure Activity Log → Log Analytics, GCP Audit Logs → sink.
- Seguridad: **Defender for Cloud**, **Security Hub + GuardDuty**,
  **Security Command Center**. SIEM (Sentinel, Splunk…).
- Cifrado en reposo con KMS / Key Vault (CMK si compliance lo pide), TLS en tránsito.

## Paso 6 — Secretos

- **Key Vault / Secrets Manager / Secret Manager**, acceso por identidad
  (RBAC), nunca en código, variables de pipeline o imágenes.
- Rotación automática; preferir identidades sin secreto sobre secretos rotados.
- Detección: secret scanning en los repos.

## Paso 7 — Costos (FinOps)

- Presupuestos y alertas por cuenta/suscripción, tags obligatorias
  (`owner`, `env`, `cost-center`), reportes por equipo.
- Reservas / Savings Plans / CUDs para carga base, spot para tolerante,
  apagar dev fuera de horario.

## Paso 8 — Todo con IaC

La landing zone entera vive en Terraform (fórmula 03), en capas `global/org`,
`global/identity`, `network-hub`, etc. Las cuentas nuevas se crean por
pipeline ("account vending").

## Prueba "funciona"

Un equipo pide una cuenta nueva → el pipeline la crea con red conectada al
hub, logs al archivo central, guardrails aplicados y grupo de acceso por SSO →
intento crear una VM con IP pública en una región no permitida → **la
política lo bloquea**.
