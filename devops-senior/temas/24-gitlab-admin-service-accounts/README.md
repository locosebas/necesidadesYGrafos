# GitLab Admin / Platform Engineer — migración a Service Accounts

Tema agregado el 2026-10-05 para preparar una entrevista real de **GitLab
Administrator / Platform Engineer** enfocada en **Service Account
Migration**: pasar las integraciones (scripts, Jenkins, ArgoCD, bots, etc.)
de tokens personales y bots manuales a **Service Accounts** de GitLab, sin
romper nada en producción.

Complementa a `03-cicd-multicloud` (que cubre GitLab CI solo por autoestudio
propio, sin verificar): este tema pone el foco en **administración de la
instancia, identidades y tokens**, no en escribir pipelines.

## Objetivos

- Explicar los problemas de usar el PAT (Personal Access Token) de una persona
  en una automatización con **R-P-L-A**: **R**ompe, **P**ermisos de más,
  **L**icencia, **A**uditoría confusa.
- Elegir la identidad correcta con el árbol de decisión: dentro de un pipeline
  de GitLab → `CI_JOB_TOKEN`; fuera de GitLab → Service Account; una persona →
  su propio usuario.
- Crear una Service Account por API en 3 pasos (**Contratar → Abrir puertas →
  Entregar llave**) con mínimo privilegio: rol (membresía) + scopes (token).
- Saber quién puede crear cada tipo de Service Account (**"AI y GO"**:
  **A**dmin → **I**nstancia, **G**rupo → **O**wner).
- Diseñar y defender el plan de migración en 5 fases: **Inventario → Diseño →
  Piloto → Olas → Gobierno**.
- Administrar GitLab self-managed: `gitlab.rb` + `gitlab-ctl reconfigure`,
  backups (y `gitlab-secrets.json`), logs, arquitectura, upgrades, LDAP/SAML/
  SCIM y tokens de runners (`glrt-`).

## Archivos

| Archivo | Qué tiene |
|---|---|
| `lecciones.md` | 25 lecciones cortas (idea clave + analogía + pregunta rápida + respuesta), la nota de cada respuesta, mnemotecnias, glosario y herramientas complementarias |
| `examen.md` | Examen de 50 preguntas en 8 bloques (fundamentos → migración), para responder de a una; aquí se anota la nota de cada pregunta |
| `clave-respuestas.md` | Puntos clave esperados de cada pregunta del examen (para calificar; no abrir antes de responder) |

## Subtemas

1. Identidades para automatización: PAT personal, bot manual, Project/Group Access Token, `CI_JOB_TOKEN`, Service Account
2. Service Accounts: niveles instancia vs. grupo, roles numéricos (10/20/30/40/50), scopes (`api`, `read_api`, `read_registry`…)
3. API de GitLab: crear la Service Account, membresía (`/groups|projects/:id/members`), token, rotación (`/rotate`)
4. Expiración de tokens desde GitLab 16.0 y rotación automática
5. Plan de migración: inventario (`last_used_at`, `api_json.log`), diseño, piloto, olas con periodo de gracia, gobierno
6. Administración self-managed: configuración, backups, logs, arquitectura (Gitaly, Sidekiq, Puma…), upgrades, autenticación
7. Migración entre instancias con Direct Transfer (las Service Accounts y los tokens no migran)

## Recursos

- Service Accounts: https://docs.gitlab.com/user/profile/service_accounts/
- API de Service Accounts: https://docs.gitlab.com/api/service_accounts/
- Personal Access Tokens: https://docs.gitlab.com/user/profile/personal_access_tokens/
- Backups y restauración: https://docs.gitlab.com/administration/backup_restore/
- Upgrade path: https://docs.gitlab.com/update/upgrade_paths/
- Direct Transfer: https://docs.gitlab.com/user/group/import/

## Autoevaluación

- Pedime: *"Sigamos con las lecciones de GitLab"* (retoma en `lecciones.md`).
- Pedime: *"Dame el examen de GitLab"* (50 preguntas de a una, en `examen.md`).
