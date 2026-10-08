# Clave de respuestas (uso de Claude para calificar — ¡no la abras antes de terminar!)

Puntos clave que debe mencionar cada respuesta. Nota = proporción de puntos cubiertos y bien explicados.

1. Git = sistema de control de versiones distribuido (local, CLI). GitLab = plataforma web que aloja repos Git + colaboración (issues, MR) + CI/CD + registry + seguridad (DevOps todo en uno).
2. MR vs PR; CI/CD integrado (.gitlab-ci.yml) vs Actions; self-hosted fuerte (CE/EE); enfoque DevSecOps todo en uno; jerarquía de grupos/subgrupos.
3. Self-managed = lo instalas/operas tú (control, cumplimiento, on-prem); GitLab.com = SaaS operado por GitLab; también Dedicated (single-tenant). Planes: Free, Premium, Ultimate.
4. Group = contenedor de proyectos y miembros, con permisos heredados; subgroups = jerarquía (equipos/áreas); project = repo + issues + MR + pipelines + wiki. Agrupar sirve para herencia de permisos, variables/runners compartidos, organización.
5. Guest < Reporter < Developer < Maintainer < Owner (+ Minimal Access). Maintainer: push/merge en ramas protegidas, gestiona settings del proyecto, CI/CD variables, protected branches, miembros, runners de proyecto.
6. merge preserva historia y crea merge commit; rebase reaplica commits → historial lineal pero reescribe SHAs. No rebase en ramas compartidas/públicas (rompe a otros, requiere force push).
7. fetch descarga cambios sin integrarlos; pull = fetch + merge (o rebase).
8. revert crea un commit inverso (seguro, no reescribe historia) → en main. reset mueve el puntero y puede borrar commits → solo local/no publicado.
9. stash: guardar cambios a medias para cambiar de rama (ej. hotfix urgente). cherry-pick: traer un commit puntual a otra rama (ej. llevar un fix a release).
10. Traer base (merge/rebase de main en la rama) localmente, editar marcadores <<<<<<< ======= >>>>>>>, probar, commit y push; o resolver en la UI del MR si es simple. Hablar con el autor del otro cambio si hay duda.
11. Solicitud para fusionar rama origen en destino: diff, discusión/comentarios en línea, revisores, aprobaciones, pipeline, estado de merge, squash, issues relacionados, draft.
12. Issue → rama (desde el issue) → commits → push → MR (Closes #N) → pipeline → revisión/aprobación → merge → issue cerrado automáticamente.
13. GitLab Flow: main + ramas de ambiente/release, simple. Git Flow: develop, feature, release, hotfix (pesado, releases planificados). Trunk-based: ramas cortas, integración continua a main, feature flags.
14. Ramas que restringen push/merge/force push por rol. main: allowed to merge Maintainers, allowed to push No one, sin force push, + MR obligatorio con approvals y "Pipelines must succeed", code owner approval.
15. Archivo CODEOWNERS asigna dueños por ruta; con "Require approval from code owners" en la protected branch, sus aprobaciones son obligatorias. Approval rules definen cuántas aprobaciones y de quién (Premium).
16. Stage = fase; stages en secuencia. Job = tarea con script; jobs del mismo stage en paralelo. Si un job falla, normalmente no avanza al siguiente stage.
17. Agente que ejecuta jobs (gitlab-runner). Tipos: instance/shared, group, project. Executors: Docker, Shell, Kubernetes, Docker Autoscaler/Machine, VirtualBox, SSH. Se seleccionan con tags.
18. artifacts: pasan resultados entre jobs/stages, se pueden descargar, garantizados. cache: acelera dependencias entre pipelines, no garantizado.
19. Predefinidas ($CI_COMMIT_BRANCH, $CI_COMMIT_SHA, $CI_PIPELINE_SOURCE, $CI_REGISTRY_IMAGE…). Custom en Settings > CI/CD > Variables (proyecto/grupo/instancia). masked: oculta en logs. protected: solo en ramas/tags protegidos. Secretos nunca en el YAML.
20. rules: - if: $CI_PIPELINE_SOURCE == "merge_request_event"
21. needs crea DAG: el job arranca al terminar sus dependencias sin esperar a todo el stage → más rápido; también limita qué artifacts descarga.
22. environment: production; rules: - if: $CI_COMMIT_BRANCH == "main" (o $CI_DEFAULT_BRANCH) con when: manual dentro de la regla; idealmente protected environment.
23. include: importar YAML de archivos locales, otros proyectos, templates o remotos (reutilización, CI components). extends: heredar configuración de un job (a menudo oculto .template).
24. No hay runner que coincida con los tags, runner offline/pausado, runner de proyecto no asignado, runners ocupados (concurrency), job protegido sin runner protegido. Revisar Settings > CI/CD > Runners.
25. cache de dependencias, needs/DAG, paralelizar (parallel/matrix), imágenes ligeras/preconstruidas, rules:changes, interruptible, dividir tests, runners con más recursos/autoscaling, shallow clone (GIT_DEPTH).
26. Registro Docker por proyecto. docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY; docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA; docker push. (kaniko/buildah/dind)
27. SAST: código fuente estático. DAST: app en ejecución. Dependency: librerías vulnerables. Container: imagen/SO. Secret Detection: credenciales en el código. Se activan con include de templates; resultados en MR/vulnerability report.
28. Environment: destino de deploy con historial; Review App: ambiente dinámico por MR (environment name con $CI_COMMIT_REF_SLUG + on_stop). Rollback: re-deploy de un deployment anterior desde la UI.
29. Token efímero generado por job, ligado al usuario que dispara el pipeline, permisos limitados, expira al terminar el job, controlado por allowlist. No hay que guardarlo ni rotarlo; un PAT es de larga duración y si se filtra es un riesgo.
30. /etc/gitlab/gitlab.rb; sudo gitlab-ctl reconfigure (y restart si aplica). Helm values si es Kubernetes.
31. NGINX (entrada), Workhorse (proxy, cargas pesadas), Puma (Rails/web/API), Sidekiq (jobs en background), Gitaly (repos Git), PostgreSQL (datos), Redis (cache/colas), (Praefect/Gitaly Cluster, Registry, Prometheus).
32. sudo gitlab-backup create (DB, repos, uploads, artifacts, LFS, registry...). NO incluye /etc/gitlab/gitlab-secrets.json ni gitlab.rb ni certificados → respaldar aparte. Probar restauraciones.
33. Leer release notes y upgrade path oficial (paradas obligatorias), backup previo, probar en staging, verificar background migrations terminadas antes de cada salto, ventana de mantenimiento, plan de rollback, verificar después (gitlab:check).
34. /var/log/gitlab/: gitlab-rails/api_json.log, production_json.log, exceptions_json.log, sidekiq, nginx, gitaly. gitlab-ctl tail. Correlation ID.
35. LDAP: autenticación contra directorio (on-prem, sync de grupos). SAML: SSO vía IdP (Okta, Azure AD). SCIM: aprovisionamiento/desaprovisionamiento automático de usuarios (no autentica).
36. Antes: registration token compartido (deprecated). Ahora: se crea el runner en la UI/API (create_runner) → authentication token glrt- por runner, trazable y con dueño; migración de runners existentes.
37. Admin Mode: el admin debe re-autenticarse para acciones administrativas (protege sesiones). Audit Events: registro de quién hizo qué (tokens creados/revocados, cambios de permisos) → cumplimiento, investigación de incidentes, streaming a SIEM.
38. PAT humano (se rompe al irse, licencia, permisos excesivos), bot manual (licencia, password, sin dueño), Project/Group Access Token (alcance limitado a uno), CI_JOB_TOKEN (solo dentro de CI), Deploy tokens/keys (limitados), Service Account (la buena).
39. Usuario no humano, sin login UI/password, solo tokens, no consume licencia (Premium/Ultimate), membresía en grupos/proyectos con rol, nivel instancia (admin) o grupo (Owner top-level), creación por API/UI, independiente de empleados.
40. GAT/PAT de proyecto: un grupo/proyecto, bot ligado al token, simple. SA: varias membresías y tokens, integraciones transversales, identidad estable.
41. Reporter (20) en el proyecto/grupo; scope read_registry (y quizás read_api). Nada de api/write.
42. Tokens sin expiración se vencieron/obtuvieron fecha (365 días); máximo 1 año por defecto (Ultimate puede acortar política). Implica rotación obligatoria, monitoreo de expiración.
43. curl --request POST --header "PRIVATE-TOKEN: $TOKEN" --data "user_id=555&access_level=20" "https://gitlab.example.com/api/v4/groups/42/members"
44. API GET /personal_access_tokens?state=active (admin) o Credentials Inventory; last_used_at, scopes, nombre, dueño; api_json.log (IP, user-agent, horarios); preguntar a dueños; matriz token→sistema→acción.
45. Cuenta bloqueada → PATs inválidos (401). Hoy: crear SA, membresía mínima, token, actualizar secreto, relanzar. Permanente: inventario y migración, offboarding revisa tokens, política sin PATs humanos en automatización.
46. Inventario → diseño (naming, una SA por sistema, mínimo privilegio, secretos en Vault, rotación) → piloto → olas (crear, asignar, token, cutover, monitorear, revocar) → limpieza (licencias) → gobierno (política, alertas, runbook, revisiones). Rollback y comunicación.
47. Consumidores desconocidos; esperar a que last_used_at deje de moverse (periodo de gracia); rollback fácil.
48. Escalonar expiraciones, rotación automatizada (/rotate + Vault, job programado), monitoreo/alertas propias, inventario con dueños.
49. Revocar inmediato → evaluar impacto (audit events, logs) → generar nuevo y actualizar consumidores → limpiar historial (opcional) → prevenir (Secret Detection, push rules/secret push protection) → postmortem.
50. STAR: Situación (contexto, escala), Tarea (su responsabilidad), Acción (pasos concretos: inventario, piloto, olas, comunicación, automatización), Resultado (métricas: % migrado, licencias liberadas, 0 incidentes), aprendizaje.
