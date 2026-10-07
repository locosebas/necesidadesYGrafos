# Seguridad / DevSecOps

Lo que separa a un DevOps Senior de uno mid es diseñar seguridad desde el
principio (shift-left), no parchearla después.

## Objetivos

- Escaneo de imágenes de contenedor (vulnerabilidades de dependencias/OS base)
  integrado al pipeline, no manual.
- Escaneo de IaC (Bicep/Terraform/CloudFormation) antes del deploy (secrets
  hardcodeados, recursos públicos por default, roles demasiado permisivos).
- Supply chain: SBOM (Software Bill of Materials), firma de imágenes.
- Principio de mínimo privilegio aplicado de punta a punta (ya lo venís viendo
  en el tema 04 — acá se junta todo).
- OWASP Top 10 a nivel conceptual (relevante si tocás las APIs con FastAPI).
- Manejo de secretos: por qué nunca en variables de entorno planas ni en git,
  siempre el gestor de secretos de la nube (tema 06) + identidad gestionada.

## Equivalencias multi-cloud (postura de seguridad nativa)

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Posture management / CSPM | Microsoft Defender for Cloud | AWS Security Hub | Security Command Center |
| Detección de amenazas | Defender for Containers/Servers | Amazon GuardDuty | Security Command Center (Event Threat Detection) |
| Escaneo de imágenes | Defender for Containers | Amazon Inspector | Artifact Analysis |
| Secrets/credential scanning en el repo | GitHub Advanced Security | GitHub Advanced Security | GitHub Advanced Security |

Herramientas open-source, agnósticas de nube (usalas igual en las tres):
**Trivy** (imágenes), **Checkov** / **tfsec** (IaC: Terraform, CloudFormation,
Bicep), **gitleaks** (secrets en el repo).

## Subtemas

1. Escaneo de imágenes: Trivy (multi-cloud) + la herramienta nativa de cada nube
2. Escaneo de IaC: Checkov/tfsec (soportan Terraform, CloudFormation y Bicep)
3. Network security como defensa en profundidad (conecta con tema 05, en cualquier nube)
4. Secrets scanning en el propio repo (gitleaks, GitHub secret scanning)
5. OWASP Top 10: https://owasp.org/www-project-top-ten/

## Herramienta que piden las ofertas (startup): OPA (policy as code)

**OPA (Open Policy Agent)** es un motor de políticas de propósito general
(CNCF): las reglas se escriben en el lenguaje **Rego** y se evalúan donde
haga falta. Es **policy as code**: las reglas de seguridad/compliance viven
en Git, se testean y se versionan como cualquier código.

Dónde se usa **OPA**:
- **Kubernetes**: **OPA Gatekeeper** (admission controller) rechaza recursos que no cumplen (por ejemplo, contenedores corriendo como root, imágenes de registries no aprobados, falta de `resources.limits`).
- **CI**: **Conftest** evalúa Terraform, manifiestos de Kubernetes o Dockerfiles en el pipeline, antes del deploy (*shift-left*).
- **Apps / APIs**: autorización fina (por ejemplo, una API FastAPI le pregunta a **OPA** si el usuario puede hacer una acción).

| Concepto | Agnóstico | Azure | AWS | GCP |
|---|---|---|---|---|
| Políticas sobre recursos de nube | **OPA** / Conftest | **Azure Policy** (usa Gatekeeper para AKS) | AWS Config rules / SCPs | Organization Policy / **Policy Controller** (basado en Gatekeeper) |
| Políticas en Kubernetes | **OPA Gatekeeper**, Kyverno | Azure Policy for AKS | Gatekeeper / Kyverno en EKS | Policy Controller (GKE) |

- OPA: https://www.openpolicyagent.org/docs/
- Gatekeeper: https://open-policy-agent.github.io/gatekeeper/

## Lab sugerido

Agregá al pipeline de GitHub Actions del lab del tema 03 un paso de escaneo de
la imagen Docker (Trivy) y uno de escaneo del IaC (Checkov, sobre el Bicep o
Terraform del lab del tema 01), que falle el build si encuentra hallazgos críticos.

## Autoevaluación

Pedime: *"Dame un examen de seguridad/DevSecOps nivel senior"*.
