# CI/CD con GitHub Actions + OIDC hacia Azure

Ya tenés CI/CD sólido (Azure Pipelines, Jenkins). Acá el foco es GitHub Actions
específicamente, y sobre todo **autenticación sin secretos** vía OIDC (OpenID
Connect) federado — el estándar actual para evitar guardar credenciales de
Service Principal en GitHub Secrets.

## Objetivos

- Explicar por qué OIDC es preferible a un Service Principal con secret guardado
  en GitHub Secrets (sin credenciales de larga duración, tokens de corta vida).
- Configurar Federated Identity Credentials en Entra ID para un repo/branch/environment específico.
- Escribir workflows de GitHub Actions con `azure/login@v2` usando OIDC.
- Diseñar pipelines multi-stage: build → test → push a ACR → deploy (con
  aprobaciones/environments para producción).
- Reusable workflows y composite actions (evitar duplicación entre repos).

## Subtemas

1. `permissions: id-token: write` y por qué es necesario
2. Federated Identity Credential: subject claims (`repo:org/repo:ref:refs/heads/main`, `environment:prod`, etc.)
3. `azure/login`, `azure/cli`, `azure/webapps-deploy`, `azure/container-apps-deploy-action`
4. GitHub Environments (protection rules, required reviewers) como equivalente a stages con aprobación en Azure Pipelines
5. Secrets management: qué va en GitHub Secrets vs qué debería ir en Key Vault
6. Self-hosted runners vs GitHub-hosted (cuándo justifica el costo/mantenimiento)

## Recursos

- Configurar OIDC de GitHub Actions a Azure: https://learn.microsoft.com/azure/developer/github/connect-from-azure
- GitHub Actions docs: https://docs.github.com/actions
- Security hardening de GitHub Actions: https://docs.github.com/actions/security-guides/security-hardening-for-github-actions

## Lab sugerido

Configurá desde cero (en un repo de prueba) login a Azure vía OIDC, sin ningún
secret de larga duración, y un workflow que construya una imagen, la suba a
ACR y despliegue a Container Apps solo si el push es a `main`.

## Autoevaluación

Pedime: *"Dame un examen de GitHub Actions y OIDC nivel senior"*.
