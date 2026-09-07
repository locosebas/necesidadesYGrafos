# Roadmap de estudio

Orden sugerido. Cada bloque es aprox. 1-2 semanas de estudio part-time
(mientras trabajás). Ajustalo a tu ritmo real — lo importante es no saltar
el examen de autoevaluación al final de cada tema.

## Metodología: de general a específico

Objetivo final: llegar a una entrevista técnica (o certificación) y poder
resolver la prueba, no solo "haber leído sobre el tema". Por eso cada nivel
sigue el mismo patrón general → específico:

1. **General (panorama):** examen diagnóstico amplio que toca los 13 temas a
   nivel conceptual, para medir dónde estás parado hoy en la práctica (no
   solo lo que infiere el CV). Esto define qué temas se profundizan primero.
2. **Específico (por tema):** dentro de cada tema, primero repaso el concepto
   general (qué es, para qué sirve, cómo se relaciona con lo demás) y recién
   después vamos a detalle técnico (sintaxis, configuración, troubleshooting).
3. **Examen del tema:** mezcla teoría + escenario, nivel creciente
   (básico → intermedio → senior) hasta llegar a ≥ 80%.
4. **Repaso mixto/entrevista:** una vez cubiertos varios temas, exámenes que
   combinan temas y simulan formato de entrevista técnica o prueba de
   certificación (preguntas encadenadas, sin decirte de antemano el tema).

## Fase 0 — Diagnóstico general (arranca acá)

Antes de la Fase 1: un examen general de panorama (1-2 preguntas por cada uno
de los 13 temas, nivel conceptual). Con el resultado ajustamos el orden real
de estudio — las brechas del `gap-analysis.md` son una hipótesis basada en el
CV, el diagnóstico general la confirma o la corrige con datos reales.

## Fase 1 — Fundamentos Azure que hoy tenés flojos (semanas 1-4)

1. `temas/05-networking-azure` — VNet, Subnets, NSG, Private Endpoints, Private DNS
2. `temas/04-identity-entra-id-rbac` — Entra ID, Managed Identity, RBAC
3. `temas/06-keyvault-cosmosdb` — Key Vault, Cosmos DB

Al final de la Fase 1 deberías poder explicar de memoria cómo una app en Azure
llega a una base de datos sin exponer secretos ni tráfico a internet público.

## Fase 2 — IaC y despliegue de contenedores (semanas 5-7)

4. `temas/01-iac-terraform-bicep` — traducir tu Terraform a Bicep
5. `temas/02-azure-container-apps-acr` — Container Apps, ACR, revisiones, scaling

## Fase 3 — CI/CD, cómputo serverless y observabilidad (semanas 8-10)

6. `temas/03-cicd-github-actions-oidc` — GitHub Actions + OIDC federation a Azure
7. `temas/09-azure-durable-functions` — orchestrator/activity functions
8. `temas/07-observabilidad` — Azure Monitor, App Insights, Log Analytics

## Fase 4 — Consolidación de nivel Senior (semanas 11-13)

9. `temas/08-python-fastapi-docker` — repaso y hardening de APIs
10. `temas/11-seguridad-devsecops` — shift-left security, escaneo de imágenes/IaC
11. `temas/12-arquitectura-costos-well-architected` — Well-Architected Framework, FinOps
12. `temas/10-kubernetes-avanzado` — repaso senior (ya es tu fortaleza, cerrar huecos)

## Fase 5 — Certificación y entrevista

- Rendir la certificación elegida (ver `certificaciones/README.md`).
- Repasar `temas/13-mercadolibre-scopes-cosmos` si aplica a una entrevista interna.
- Simulacro de entrevista técnica con Claude usando `examenes/` en modo mixto
  (preguntas de varios temas, formato entrevista).

## Cómo avanzar de fase

No avances de fase hasta tener **≥ 80% en el examen de cada tema** de la fase
anterior (ver `examenes/registro/`). Si un tema queda débil, se repite antes de
seguir — la idea es no acumular huecos.
