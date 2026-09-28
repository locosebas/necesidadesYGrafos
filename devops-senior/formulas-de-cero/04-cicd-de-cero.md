# Fórmula 04 — CI/CD de cero a que funcione

**Resumen en una línea:** *repo y ramas → CI (lint, test, build, scan) →
artefacto inmutable → CD por entornos con aprobación → autenticación OIDC →
estrategia de deploy → rollback → métricas del pipeline.*

---

## Paso 0 — Requisitos

- ¿Qué se despliega (contenedor, función, infra)? ¿Dónde (K8s, Container Apps, Lambda)?
- ¿Cuántos entornos? ¿Frecuencia de deploy deseada? ¿Aprobaciones/compliance?

## Paso 1 — Repositorio y flujo de ramas

- **Trunk-based**: ramas cortas → PR → `main` siempre desplegable.
- Protección de `main`: PR obligatorio, checks verdes, 1–2 aprobaciones,
  CODEOWNERS, commits firmados (opcional).

## Paso 2 — CI (en cada PR)

1. Lint + formato (ruff/black, eslint, hadolint para Dockerfile).
2. **Tests unitarios** + cobertura.
3. **SAST** (CodeQL, Semgrep) y **escaneo de dependencias** (Dependabot, Trivy, Snyk).
4. **Detección de secretos** (gitleaks, GitHub secret scanning).
5. Build de la imagen (multi-stage, cache de capas).
6. **Escaneo de la imagen** (Trivy) — falla si hay CVEs críticas con fix.
7. Tests de integración (docker compose / testcontainers).

## Paso 3 — Artefacto inmutable

- Imagen con tag = **SHA del commit** (+ semver en releases), nunca `latest`.
- Push a **ECR / ACR / Artifact Registry**.
- **Firma** (cosign) + SBOM (syft). *Build once, deploy many*: la misma
  imagen pasa por dev → stg → prod; solo cambia la configuración.

## Paso 4 — CD por entornos

```
merge a main → deploy automático a dev → tests de humo
            → deploy a stg → tests e2e / carga
            → aprobación manual (GitHub Environments) → deploy a prod
```

- En K8s: **GitOps** (CI actualiza el tag en el repo de manifiestos, Argo CD despliega).
- En PaaS: `az containerapp update`, `gcloud run deploy`, `aws ecs update-service`, etc.
- Infra y app en pipelines separados (ciclos de vida distintos).

## Paso 5 — Autenticación sin secretos: OIDC

1. En la nube se crea una identidad que **confía en el emisor OIDC de GitHub**
   (`token.actions.githubusercontent.com`):
   - Azure: App registration / **User-assigned Managed Identity** + *federated credential*.
   - AWS: **IAM OIDC provider** + rol con trust policy.
   - GCP: **Workload Identity Pool + Provider** + service account.
2. La condición restringe `sub` (repo, rama o environment).
3. El workflow pide `permissions: id-token: write` y hace login con la
   acción oficial → recibe credenciales **temporales**. Cero claves guardadas.

```yaml
permissions: { id-token: write, contents: read }
steps:
  - uses: azure/login@v2
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

## Paso 6 — Estrategia de deploy

| Estrategia | Cómo | Cuándo |
|---|---|---|
| Rolling | Reemplaza pods de a poco | Default, cambios compatibles |
| Blue/Green | Dos entornos, se cambia el tráfico de golpe | Rollback instantáneo, cuesta el doble |
| Canary | 5% → 25% → 100% midiendo errores/latencia | Servicios críticos de alto tráfico |
| Feature flags | Se despliega apagado, se prende por usuario | Separar deploy de release |

Base de datos: migraciones **compatibles hacia atrás** (expand → migrate → contract).

## Paso 7 — Rollback y seguridad del proceso

- Rollback = redeploy de la imagen anterior (o `git revert` en GitOps).
- Canary con **análisis automático** (Argo Rollouts / Flagger) que revierte solo.
- Mínimo privilegio para el pipeline; runners efímeros; acciones de terceros
  fijadas por **SHA**.

## Paso 8 — Métricas (DORA)

- **Frecuencia de deploy**, **lead time** de cambios, **tasa de fallos de
  cambio**, **tiempo de recuperación** (MTTR). Decir esto en una entrevista suma.

## Prueba "funciona"

PR con un cambio → checks verdes → merge → aparece en dev solo → se aprueba
→ llega a prod → el endpoint devuelve la versión nueva (`/version` muestra el SHA)
→ rompo algo a propósito → el rollback deja la versión anterior.
