# GitLab Admin / Platform Engineer: lecciones cortas

**Cómo lo usamos:** vemos una lección a la vez. Claude explica la idea clave, te hace la pregunta rápida, tú respondes y pasamos a la siguiente.

**Progreso:** Lecciones 1-24 hechas (promedio 7.7/10) · Pendiente: responder la lección 25, repetir el plan de 5 fases sin ayuda y la respuesta personal de herramientas

## Notas por lección

### Parte 1: Identidades · promedio 7.2/10
| Lección | Nota | Qué faltó |
|---|---|---|
| 1 | 7/10 | Olvidó la licencia; "se rompe" quedó impreciso (es cuando lo bloquean o se va) |
| 2 | 8/10 | Bien: superficie de ataque y costo. Faltó lo concreto: la contraseña permite login por la UI y, sin dueño, nadie la rota ni la vigila |
| 3 | 7/10 | Buen criterio (mantenimiento, crecimiento). Faltó nombrar la alternativa (Service Account) y concretar: 15 tokens que rotar, 15 bots, sin una identidad única |
| 4 | 8/10 | Elección correcta y muy buena distinción interno/externo. Faltó: el riesgo real del token de SA es que es de larga duración (hay que guardarlo y rotarlo, y puede filtrarse); agregar el proyecto a la allowlist |
| 5 | 7/10 | P y A bien. R impreciso: la SA no está ligada al ciclo de vida de ninguna persona. L incorrecto: NO usa la licencia de su creador, no consume ninguna |
| Repaso P1 | 6/10 | Job de CI → CI_JOB_TOKEN bien. Script de María: asumió que corre en CI; hay que preguntar dónde corre (fuera de CI → SA). No entendió el ci-bot manual → migrar a SA y bloquear el bot |

### Parte 2: Service Accounts y la API · promedio 7.0/10
| Lección | Nota | Qué faltó |
|---|---|---|
| 6 | 3/10 | Invirtió los niveles: en GitLab.com, como Owner, solo puede crear a nivel GRUPO; nivel instancia = solo admin de self-managed. Mnemotecnia: "AI y GO" (Admin→Instancia, Grupo→Owner). Repetir la pregunta más adelante |
| 6b | 5/10 | Acertó instancia, pero el admin de self-managed puede crear AMBAS (el admin tiene poder de Owner en todos los grupos). Modelo: el poder es acumulativo, Admin ⊃ Owner. Volver a preguntar en el repaso de la Parte 2 |
| 7 | 8/10 | 20 correcto. Faltó el porqué de no dar 30: podría hacer push, y si el token se filtra, un atacante modificaría código (mínimo privilegio) |
| 8 | 10/10 | Perfecto: /service_accounts = instancia; /groups/:id/service_accounts = grupo |
| 9 | 8/10 | user_id=555 y access_level=30 correctos. Faltó decir explícitamente que la ruta cambia de /groups/ a /projects/77/members |
| 10 | 10/10 | Reporter (20) + read_registry. Perfecto, aplicó los dos candados |
| 11 | 6/10 | Rotación automática con un job, bien. Faltó el problema central: vencen las 120 el MISMO día (caída masiva). Solución: escalonar fechas + rotación automática + alertas propias. "Artefacto" no es el término (es la salida de un job de CI) |
| Repaso P2 | 6/10 | ✅ Ambos tipos (AI y GO superado) y ✅ Reporter + read_registry. ❌ URL: mezcló 3 llamadas en una y usó /groups/77 cuando 77 es un proyecto. Son 3 pasos separados: crear SA → /projects/77/members → token con scopes |

### Parte 3: Plan de migración · promedio 7.8/10
| Lección | Nota | Qué faltó |
|---|---|---|
| 12 | 7/10 | Horarios: muy bien, con matiz. IPs: integración = IP fija de servidor; persona = IPs variables (casa, VPN, móvil). Faltó el user-agent (python-requests, curl, Jenkins vs navegador) y el uso en noches o fines de semana |
| 13 | 6/10 | Buen uso de R-P-L-A. P (suma de permisos) y A correctas. L NO aplica (las SA no consumen licencia). Olvidó R: un solo token filtrado o rotado afecta a los 3 sistemas a la vez (radio de impacto) |
| 14 | 10/10 | Bot de Slack: bajo impacto y reversible; facturación difícil de revertir; producción afecta la fiabilidad. Excelente |
| 15 | 9/10 | Muy bien: proceso automático, descartar ataque, migrarlo. Faltó el CÓMO (api_json.log: IP y user-agent) y reiniciar el periodo de gracia; si es un ataque, revocar de inmediato |
| 16 | 8/10 | Idea correcta (buscar el patrón). Faltó escalarlo: un patrón fijo permite detección automática sin falsos positivos (Secret Detection en CI, Secret Push Protection bloquea el push) y hay que revisar el historial de Git, no solo el código actual |
| 17 | 7/10 | Solución correcta (rotación automática). Faltó el porqué: la SA no tiene un buzón que alguien lea. Faltó también la red de seguridad: un job que consulte expires_at por API y alerte a Slack o PagerDuty del equipo dueño |
| Repaso P3 | 5/10 | Inventario implícito (bien: "no sabemos quién las ejecuta"). ❌ Una SA por segmento contradice "una SA por sistema" (segmentar sirve para las olas, no para las cuentas). Faltaron el piloto y el periodo de gracia con revocación. Gobierno parcial (checklist semiautomática → automatizar). La IA es un extra, no una fase. Repetir con la mudanza |
| Repaso P3b | 5/10 | Orden correcto (I-D-P-O-G), pero miró la tabla y no dio una idea clave por fase. ⏰ PREGUNTAR DE NUEVO al final, sin ayuda visible |

### Parte 4: Administración de la instancia · promedio 8.0/10 (lecciones 18-24)
| Lección | Nota | Qué faltó |
|---|---|---|
| 18 | 9/10 | Correcto. Decir el comando completo: `sudo gitlab-ctl reconfigure`. Dato extra: .rb = Ruby (GitLab es Ruby on Rails); reconfigure usa Chef/Cinc para generar la configuración de todos los servicios |
| 19 | 8/10 | Causa correcta. Faltó el porqué (contiene las llaves de cifrado de las variables de CI y del 2FA) y la solución: restaurar el gitlab-secrets.json original + reconfigure + restart. Si se perdió, esos datos son irrecuperables. Probar las restauraciones periódicamente |
| 20 | 10/10 | audit_json.log para quién revocó; api_json.log para la IP. Perfecto. Extra: los Audit Events también se ven en la UI (Admin Area) |
| 21 | 5/10 | Dudó entre Workhorse y Gitaly. Es Gitaly: es el denominador común (la UI muestra archivos vía Puma→Gitaly; el clone pasa por Workhorse o SSH→Gitaly). Si Workhorse fallara, ni la web cargaría, porque todas las peticiones pasan por él. Técnica: descartar lo que SÍ funciona y buscar el denominador común |
| 22 | 8/10 | Muy bien: no saltar directo, ir por pasos, cuestionar el tiempo. Término correcto: "paradas obligatorias" (required upgrade stops), no "versiones estables". El tiempo se estima ensayando en staging (las background migrations pueden tardar horas o días). Faltó mencionar backup, rollback y comunicación |
| 23 | 8/10 | Muy bien: los scripts mueren y conviene una migración controlada en vez de una de emergencia. Faltó el porqué de la urgencia: SCIM desactiva al instante y sin intervención humana, así que nadie revisa los tokens antes. "SCIM convierte un riesgo latente en un incidente seguro" |
| 24 | 8/10 | Aplicó bien el patrón (mínimo privilegio, trazabilidad, se rompe si se revoca). Faltó el ataque concreto: con el token filtrado, alguien registra un runner malicioso que recibe jobs y roba secretos de CI y código |

## Para memorizar

- **R-P-L-A** (problemas del token de una persona): **R**ompe, **P**ermisos de más, **L**icencia, **A**uditoría confusa.
- **Árbol de decisión:** ¿corre dentro de un pipeline de GitLab? → `CI_JOB_TOKEN` · ¿corre fuera de GitLab? → Service Account · ¿es una persona? → su propio usuario.
- **"AI y GO":** **A**dmin → **I**nstancia, **G**rupo → **O**wner. El poder es acumulativo: el Admin de self-managed puede crear las dos.
- **Roles:** "**G**ente **R**ara **D**esarrolla **M**ucho **O**cio" → Guest 10, Reporter 20, Developer 30, Maintainer 40, Owner 50.
- **Los 3 pasos de la API: Contratar → Abrir puertas → Entregar llave**
  1. Crear la SA: `POST /groups/:id/service_accounts` (o `/service_accounts` como admin) → devuelve su ID
  2. Membresía (el **rol** va aquí): `POST /projects/77/members` con `user_id` y `access_level`
  3. Token (el **scope** va aquí): `POST /groups/:id/service_accounts/:user_id/personal_access_tokens` con `scopes[]` y `expires_at` (como admin: `POST /users/:user_id/personal_access_tokens`)
- **Plan en 5 fases = una mudanza** (cadena lógica: ¿Qué tengo? → ¿Cómo lo quiero? → ¿Funciona? → Hazlo con todo → Que no se repita):
  1. **Inventario**: qué hay en cada cuarto (tokens, dueños, sistemas, `last_used_at`)
  2. **Diseño**: los planos de la casa nueva (`svc-` naming, una SA por sistema, mínimo privilegio, Vault, dueño)
  3. **Piloto**: mudar una caja de prueba (integración de bajo impacto y reversible)
  4. **Olas**: cuarto por cuarto (crear → acceso → token → cambio → periodo de gracia → revocar el viejo y bloquear los bots)
  5. **Gobierno**: reglas de la casa nueva (política, rotación automática, alertas, revisiones)
- **Diagnóstico:** descarta lo que SÍ funciona y busca el denominador común de lo que falla (ej.: repos y `git clone` fallan → Gitaly).

**Glosario:** *Integración* = cualquier sistema externo o script que se conecta a GitLab automáticamente, sin una persona (ArgoCD, Jenkins, un bot de Slack, Terraform, sincronización con Jira…). Cada una necesita una credencial (token).

## Herramientas complementarias a GitLab (pregunta frecuente)
| Categoría | Herramientas | Para qué en este puesto |
|---|---|---|
| Secretos | HashiCorp Vault, AWS Secrets Manager, Azure Key Vault | Guardar tokens de SA; Vault + `id_tokens` (OIDC) en CI |
| IaC | Terraform (provider de GitLab), Ansible | SA, membresías y grupos como código; instalar y configurar self-managed |
| Contenedores | Docker, Kubernetes, Helm | Runners en K8s (GitLab Runner chart), GitLab en Helm |
| GitOps / CD | ArgoCD, Flux | Despliegues que leen repos (integración típica a migrar) |
| Scripting / API | Bash, Python (`python-gitlab`), curl + jq, `glab` CLI | Inventario de tokens, automatizar la rotación |
| Observabilidad | Prometheus + Grafana, ELK / Loki / Splunk | Métricas de GitLab, análisis de `api_json.log`, alertas |
| Identidad | Okta, Entra ID (Azure AD), Active Directory | SAML/SSO, SCIM, LDAP |
| Alertas / comunicación | PagerDuty, Slack / Teams, Jira | Alertas de expiración, notificaciones, tickets |
| Migración | Direct Transfer, Congregate | Mover grupos y proyectos entre instancias |

**Regla:** 4 o 5 herramientas por categoría relevante, cada una con "para qué la usé". Solo las que de verdad usaste.

**Regla:** pocas herramientas, cada una con "para qué la usé". Solo las que de verdad usaste.

## Índice de lecciones

| Parte | Lecciones |
|---|---|
| 1. Identidades (el problema) | 1-5 |
| 2. Service Accounts y la API | 6-11 |
| 3. Plan de migración | 12-17 |
| 4. Administración de la instancia | 18-25 |

---

## Parte 1: Identidades

### Lección 1: El problema del PAT personal
**Idea clave:** muchas integraciones (deploys, bots, scripts) usan el **Personal Access Token (PAT)** de una persona. Si esa persona se va de la empresa, se bloquea su cuenta y **todos sus tokens dejan de funcionar**: se cae todo lo que dependía de ella.
Además: el token tiene **todos** los permisos de la persona, ocupa una licencia y la auditoría dice "lo hizo Juan" cuando en realidad fue un script.
**Pregunta rápida:** Menciona 2 problemas de usar el PAT de un empleado en un deploy.
**Respuesta:** Se rompe si el empleado se va o lo bloquean. Además tiene permisos excesivos, ocupa licencia y la auditoría queda confusa.

### Lección 2: El "bot" manual
**Idea clave:** la solución vieja era crear un usuario normal tipo `ci-bot@empresa.com`. Es mejor que un PAT personal, pero **consume licencia**, tiene contraseña (alguien puede iniciar sesión con él) y casi nunca tiene un dueño claro.
**Pregunta rápida:** ¿Por qué un bot manual cuesta dinero?
**Respuesta:** Porque es un usuario normal y ocupa una licencia (seat).

### Lección 3: Project / Group Access Tokens
**Idea clave:** es un token creado **dentro de un proyecto o grupo**. GitLab crea por debajo un usuario bot (`project_bot`). Su alcance se limita a **ese** proyecto o grupo, y si borras el token, el bot desaparece.
**Pregunta rápida:** Una integración necesita acceso a 15 grupos distintos. ¿Te sirve un Group Access Token?
**Respuesta:** No es lo ideal: necesitarías 15 tokens distintos. Mejor una Service Account agregada como miembro en los 15 grupos.

### Lección 4: CI_JOB_TOKEN
**Idea clave:** es un token **temporal** que GitLab genera solo mientras corre un job de CI y que expira al terminar. No hay que guardarlo ni rotarlo. Su limitación es que solo existe dentro de los pipelines y tiene permisos limitados.
**Pregunta rápida:** Un job necesita clonar otro repo interno. ¿Qué usas primero?
**Respuesta:** `CI_JOB_TOKEN` (agregando el proyecto a la allowlist del otro repo). Solo si no alcanza, el token de una service account.

### Lección 5: Service Account, la solución
**Idea clave:** es un usuario **no humano oficial** de GitLab (desde la versión 16.1):
- No inicia sesión por la UI ni tiene contraseña: funciona solo con tokens.
- **No consume licencia** en Premium/Ultimate.
- No depende de ningún empleado.
- Se agrega como **miembro** de grupos o proyectos con el rol que necesite.
**Pregunta rápida:** Dime 3 características de una service account.
**Respuesta:** Cualquiera de estas: no es humana, no hace login, solo usa tokens, no ocupa licencia, no depende de personas, se le asigna un rol como miembro.

---

## Parte 2: Service Accounts y la API

### Lección 6: Dos niveles de Service Account
**Idea clave:**
- **Nivel instancia** (self-managed): la crea un **administrador**.
- **Nivel grupo**: la crea el **Owner** de un grupo de nivel superior. Es la opción en GitLab.com.
**Pregunta rápida:** Trabajas en GitLab.com y no eres admin de la instancia. ¿Qué tipo puedes crear?
**Respuesta:** De nivel grupo, si eres Owner del grupo de nivel superior.

### Lección 7: Roles y sus números
**Idea clave:** en la API los roles son números: **10** Guest · **20** Reporter · **30** Developer · **40** Maintainer · **50** Owner (y **5** Minimal Access).
- Reporter: lee código, issues y registry.
- Developer: hace push a ramas no protegidas.
- Maintainer: administra el proyecto y las ramas protegidas.
**Pregunta rápida:** ¿Qué número le das a una integración que solo necesita leer?
**Respuesta:** 20 (Reporter).

### Lección 8: Crear la Service Account por API
**Idea clave:**
```bash
curl -X POST -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.example.com/api/v4/groups/123/service_accounts" \
  --data "name=CI Deployer&username=svc-ci-deployer"
```
A nivel instancia (como admin) el endpoint es `POST /api/v4/service_accounts`.
**Pregunta rápida:** ¿Qué header se usa para autenticarse en la API?
**Respuesta:** `PRIVATE-TOKEN: <token>` (o `Authorization: Bearer <token>`).

### Lección 9: Darle acceso (membresía)
**Idea clave:** una service account recién creada no tiene acceso a nada. Hay que **agregarla como miembro**:
```bash
curl -X POST -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.example.com/api/v4/groups/42/members" \
  --data "user_id=555&access_level=20"
```
**Pregunta rápida:** ¿Qué cambiarías para darle acceso a un **proyecto** en vez de a un grupo?
**Respuesta:** La ruta: `/projects/<id>/members` en vez de `/groups/<id>/members`.

### Lección 10: Tokens y scopes
**Idea clave:** la service account necesita un token, y ese token tiene **scopes** (lo que puede hacer):
- `api`: acceso total. Evitarlo.
- `read_api`: solo lectura.
- `read_repository` / `write_repository`: lectura o escritura del repo.
- `read_registry` / `write_registry`: lectura o escritura de imágenes Docker.

El acceso real es la **combinación** del rol (membresía) y los scopes (token).
```bash
POST /api/v4/groups/123/service_accounts/555/personal_access_tokens
  name=deploy-2026  scopes[]=read_registry  expires_at=2027-10-01
```
**Pregunta rápida:** Un sistema solo descarga imágenes Docker. ¿Qué rol y qué scope?
**Respuesta:** Reporter (20) con `read_registry`.

### Lección 11: Expiración y rotación
**Idea clave:** desde **GitLab 16.0** ya no existen los tokens eternos. Los que no tenían fecha pasaron a vencer en 365 días, y el máximo por defecto es 1 año. Por eso se necesita **rotación**: `POST .../personal_access_tokens/<id>/rotate` genera uno nuevo y revoca el anterior.
**Pregunta rápida:** ¿Qué pasa si nadie rota los tokens?
**Respuesta:** Vencen y las integraciones se caen, a veces muchas el mismo día.

---

## Parte 3: Plan de migración

### Lección 12: Fase 1, inventario
**Idea clave:** antes de migrar, hay que saber qué existe:
- `GET /api/v4/personal_access_tokens?state=active` (como admin) o el **Credentials Inventory**.
- Revisar `last_used_at`, los scopes y el dueño de cada token.
- Mirar `api_json.log` para ver IPs y horarios: un uso a las 3 a.m. todos los días es un script.

El resultado es una tabla: token → dueño → sistema → acción.
**Pregunta rápida:** ¿Qué campo te dice si un token todavía se usa?
**Respuesta:** `last_used_at`.

### Lección 13: Fase 2, diseño
**Idea clave:**
- Nombres consistentes: `svc-<equipo>-<sistema>`.
- **Una service account por sistema**, nunca una compartida para todo.
- Mínimo privilegio: el rol más bajo y los scopes mínimos.
- Secretos en **Vault** o en variables de CI masked y protected.
- Un dueño humano documentado.
**Pregunta rápida:** ¿Por qué no usar una sola service account para todas las integraciones?
**Respuesta:** Si se filtra su token, se compromete todo. Además tendría demasiados permisos y no sabrías qué sistema hizo cada acción.

### Lección 14: Fase 3 y 4, piloto y olas
**Idea clave:** primero se migran 1 o 2 integraciones de bajo riesgo (piloto). Después, por olas:
1. Crear la service account.
2. Darle membresía.
3. Crear el token.
4. Guardarlo en Vault.
5. Cambiar la integración.
6. Monitorear.
7. Revocar el token viejo.
**Pregunta rápida:** ¿Por qué empezar con un piloto?
**Respuesta:** Para validar el proceso y encontrar problemas con poco riesgo antes de escalar.

### Lección 15: No revocar de inmediato
**Idea clave:** después del cambio, el token viejo **sigue vivo** durante un periodo de gracia (por ejemplo, 2 semanas). Si su `last_used_at` sigue moviéndose, hay un consumidor que no conocías. Además, mientras exista, hacer rollback es tan simple como volver a poner el secreto viejo.
**Pregunta rápida:** Revocaste el token viejo y se cayó algo que nadie conocía. ¿Qué te faltó?
**Respuesta:** El periodo de gracia, monitoreando `last_used_at` antes de revocar.

### Lección 16: Riesgos típicos
**Idea clave:**
- Integraciones "fantasma" no documentadas.
- Webhooks y mirrors configurados con credenciales de una persona.
- Tokens hardcodeados en scripts o en Jenkins.
- Muchos tokens que vencen el mismo día.
**Pregunta rápida:** ¿Cómo encuentras tokens escritos dentro del código?
**Respuesta:** Con **Secret Detection**: los PAT empiezan con `glpat-`, lo que facilita detectarlos.

### Lección 17: Gobierno posterior
**Idea clave:**
- Política: prohibido usar PATs humanos en automatizaciones.
- Rotación automática (un job programado que llama a `/rotate` y guarda el resultado en Vault).
- Alertas propias de expiración (las service accounts no leen correos).
- Revisiones de acceso periódicas y un runbook documentado.
**Pregunta rápida:** ¿Por qué no basta con los correos de expiración que envía GitLab?
**Respuesta:** Porque la service account no tiene un buzón que alguien lea.

---

## Parte 4: Administración de la instancia

### Lección 18: Configuración
**Idea clave:** en self-managed (Omnibus), la configuración vive en `/etc/gitlab/gitlab.rb` y se aplica con `sudo gitlab-ctl reconfigure`. Otros comandos útiles: `gitlab-ctl status`, `restart` y `tail`.
**Pregunta rápida:** Editaste `gitlab.rb` y no pasa nada. ¿Qué olvidaste?
**Respuesta:** Ejecutar `gitlab-ctl reconfigure`.

### Lección 19: Backups (pregunta trampa)
**Idea clave:** `sudo gitlab-backup create` respalda la base de datos, los repos, los uploads y los artifacts, pero **NO** respalda `/etc/gitlab/gitlab-secrets.json` ni `gitlab.rb`. Sin `gitlab-secrets.json`, las variables de CI y el 2FA quedan inservibles.
**Pregunta rápida:** ¿Qué archivo debes respaldar aparte sí o sí?
**Respuesta:** `/etc/gitlab/gitlab-secrets.json` (y también `gitlab.rb`).

### Lección 20: Logs
**Idea clave:** los logs están en `/var/log/gitlab/`:
- `gitlab-rails/api_json.log`: llamadas a la API (útil para el inventario de tokens).
- `production_json.log`: peticiones web.
- `audit_json.log`: auditoría.

Para verlos en vivo: `gitlab-ctl tail`.
**Pregunta rápida:** ¿Qué log revisas para saber qué IP usa un token?
**Respuesta:** `api_json.log`.

### Lección 21: Arquitectura
**Idea clave:**
- NGINX: la entrada.
- Workhorse: proxy para cargas pesadas.
- Puma: la aplicación Rails.
- Sidekiq: tareas en segundo plano.
- Gitaly: guarda los repos.
- PostgreSQL: los datos.
- Redis: cache y colas.

Para alta disponibilidad: Gitaly Cluster y **Geo** (réplicas y recuperación ante desastres).
**Pregunta rápida:** ¿Qué componente guarda los repositorios Git?
**Respuesta:** Gitaly.

### Lección 22: Upgrades
**Idea clave:** sigue la **upgrade path** oficial, porque no se pueden saltar versiones con paradas obligatorias. Haz backup antes, prueba en staging y verifica que las **background migrations** terminaron antes del siguiente salto.
**Pregunta rápida:** ¿Puedes ir directo de la 15.0 a la 17.0?
**Respuesta:** No. Hay que pasar por las paradas obligatorias de la upgrade path.

### Lección 23: Autenticación
**Idea clave:**
- **LDAP**: login contra el directorio de la empresa.
- **SAML**: inicio de sesión único (SSO) con Okta o Azure AD.
- **SCIM**: crea y desactiva usuarios automáticamente.
- **Admin Mode**: el administrador se reautentica antes de hacer tareas sensibles.
**Pregunta rápida:** ¿Cuál de los tres desactiva automáticamente a un empleado que se fue?
**Respuesta:** SCIM.

### Lección 24: Tokens de runners
**Idea clave:** el viejo **registration token** compartido está deprecado. Ahora se crea el runner en la UI o por API y recibe su propio **authentication token** (`glrt-...`). Es otra migración típica de identidades.
**Pregunta rápida:** ¿Qué prefijo tiene el nuevo token de runner?
**Respuesta:** `glrt-`.

### Lección 25: Migración entre instancias
**Idea clave:** para mover grupos de self-managed a GitLab.com, o a otra instancia, se usa **Direct Transfer**. Las service accounts y los tokens **no se migran**: hay que recrearlos en el destino. Las contribuciones de los usuarios se reasignan mediante usuarios placeholder.
**Pregunta rápida:** Después de un Direct Transfer, ¿funcionan los tokens de las integraciones?
**Respuesta:** No. Hay que crear de nuevo las service accounts y los tokens en el destino.
