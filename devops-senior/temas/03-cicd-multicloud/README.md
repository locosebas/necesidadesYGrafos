# CI/CD multi-cloud: GitHub Actions + OIDC hacia Azure/AWS/GCP

Ya tenés CI/CD sólido (Azure Pipelines, Jenkins). El foco acá es GitHub
Actions como orquestador **común a las tres nubes**, con autenticación
**sin secretos de larga duración** vía OIDC federado en cada una.

## Objetivos

- Explicar por qué OIDC es preferible a credenciales estáticas guardadas en
  GitHub Secrets, en cualquier nube.
- Configurar federación de identidad OIDC en Azure (Entra ID), AWS (IAM
  Identity Provider) y GCP (Workload Identity Federation).
- Escribir workflows de GitHub Actions que se autentiquen contra cada una sin
  ningún secret de larga duración.
- Diseñar pipelines multi-stage con aprobaciones (GitHub Environments) —
  equivalente a stages con aprobación en Azure Pipelines/otros.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Mecanismo de federación OIDC | Federated Identity Credential (Entra ID) | IAM OpenID Connect Identity Provider + IAM Role | Workload Identity Federation (Workload Identity Pool + Provider) |
| Acción oficial de login | `azure/login@v2` | `aws-actions/configure-aws-credentials@v4` | `google-github-actions/auth@v2` |
| Identidad resultante | Service Principal (vía Entra ID) | IAM Role asumido (`AssumeRoleWithWebIdentity`) | Service Account impersonado |
| Claim que se valida | `repo:org/repo:ref:refs/heads/main` o `environment:prod` | `sub` del token OIDC de GitHub, condición en el Trust Policy del Role | `attribute.repository` en el mapeo de atributos del pool |

## Subtemas

1. `permissions: id-token: write` — por qué es necesario en las tres integraciones
2. GitHub Environments (protection rules, required reviewers) para aprobar despliegues a producción
3. Reusable workflows y composite actions (evitar duplicar pipeline por cada nube/repo)
4. Qué va en GitHub Secrets vs. qué debería vivir en Key Vault / Secrets Manager / Secret Manager
5. Self-hosted runners vs. GitHub-hosted (costo/mantenimiento vs. acceso a red privada)

## Recursos

- OIDC de GitHub Actions a Azure: https://learn.microsoft.com/azure/developer/github/connect-from-azure
- OIDC de GitHub Actions a AWS: https://docs.github.com/actions/security-guides/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
- OIDC de GitHub Actions a GCP: https://github.com/google-github-actions/auth#workload-identity-federation
- GitHub Actions docs: https://docs.github.com/actions

## Lab sugerido

Configurá, en un repo de prueba, tres workflows separados que hagan login sin
secretos a Azure, AWS y GCP respectivamente vía OIDC, cada uno desplegando el
mismo contenedor a su respectivo servicio serverless (tema 02).

## Autoevaluación

Pedime: *"Dame un examen de GitHub Actions + OIDC multi-cloud nivel senior"*.
