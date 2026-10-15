# Respuesta a incidentes — trabajo de L2/L3 (on-call, troubleshooting, post-mortem)

En una entrevista de Senior DevOps / SRE / Platform Engineer casi siempre
aparece un escenario del tipo *"son las 3am, se cayó X, ¿qué hacés?"*. No
evalúan si adivinás la causa: evalúan **si seguís un proceso ordenado**.
Este tema es ese proceso, paso a paso, para que lo puedas recitar y aplicar
sin pensar.

Es cloud-agnóstico (sirve para Azure, AWS, GCP y Kubernetes). El caso
específico de MercadoLibre (Scopes/CoSMOS) está en
`../13-mercadolibre-scopes-cosmos/` — este tema es la base general sobre la
que se apoya ese.

Banco de preguntas y escenarios para practicar: [`preguntas-escenarios.md`](preguntas-escenarios.md).

---

## Repaso rápido: niveles de soporte

| Nivel | Quién | Qué hace | Cuándo escala |
|---|---|---|---|
| **L0** | Autoservicio | Documentación, runbooks públicos, bots | — |
| **L1** | Primera línea (help desk, NOC) | Recibe la alerta o el ticket, clasifica, aplica runbooks conocidos | Cuando el runbook no alcanza o no existe |
| **L2** | Soporte técnico especializado / SRE / equipo de plataforma | Diagnóstico profundo con observabilidad, config e infraestructura. Mitiga | Cuando la causa está en el código o en el diseño |
| **L3** | Equipo dueño del sistema (desarrolladores) | Fix de código, causa raíz, cambio de diseño | Cuando la causa está en un proveedor |
| **L4** | Proveedor externo (AWS, Azure, GCP, un vendor) | Problemas en su plataforma | — |

**L2** = restaurar el servicio con lo que hay (config, infraestructura, rollback).
**L3** = arreglarlo de verdad (código, diseño).
En equipos de plataforma, la misma persona suele hacer de **L2 y L3**.

---

## El modelo mental: 5 preguntas en orden + 1 hilo que nunca se corta

Memorizá esto. Todo el resto del documento es el detalle de cada línea.

| # | Fase | La pregunta que responde | Regla de oro |
|---|---|---|---|
| 1 | **Recibir y clasificar** (*triage*) | ¿Es mío? ¿Qué tan grave es? | Ack rápido. Ante la duda, severidad **más alta** |
| 2 | **Mitigar** | ¿Cómo paro el daño **ya**? | Restaurar el servicio **antes** que entender la causa |
| 3 | **Diagnosticar** | ¿Por qué pasó? | Acotar → hipótesis → probar **una** a la vez |
| 4 | **Resolver y verificar** | ¿Está arreglado **de verdad**? | Las métricas lo confirman, no tu intuición |
| 5 | **Aprender** (*post-mortem*) | ¿Cómo evito que vuelva a pasar? | **Blameless**: se buscan fallas del sistema, no culpables |
| ∞ | **Comunicar y escalar** | ¿Quién necesita saber? ¿Necesito ayuda? | Silencio = peor que una mala noticia |

Frase para recordar el orden:
> **"Clasifico, freno, entiendo, arreglo, aprendo — y aviso todo el tiempo."**

Error más común en entrevista: saltar directo a la **fase 3 (diagnosticar)**
sin pasar por la **fase 2 (mitigar)**. Si hay un deploy de hace 10 minutos y
todo empezó hace 10 minutos, **primero rollback**, después investigás.

---

## Fase 0 — Antes del incidente (lo que hace que el resto funcione)

Te pueden preguntar *"¿qué tiene que existir para que un on-call funcione bien?"*:

- **Rotación de on-call** definida, con primario y secundario (*escalation policy*
  en PagerDuty / Opsgenie / incident.io).
- **Alertas accionables**: cada alerta tiene dueño, severidad y **runbook**
  enlazado. Alertar sobre **síntomas** que ve el usuario (latencia, errores,
  basados en **SLO**), no sobre cualquier métrica interna.
- **Runbooks** actualizados: pasos concretos, copy-paste, con comandos.
- **Dashboards** de cada servicio con las **golden signals**.
- **Accesos probados de antemano**: VPN, consola cloud, `kubectl`, permisos
  *break-glass*. Descubrir a las 3am que no tenés acceso es un fallo de proceso.
- **Canal de incidentes** y plantilla de comunicación listos.

---

## Fase 1 — Recibir y clasificar (T+0 a T+5 min)

### Pasos

1. **Ack** de la alerta (PagerDuty / Opsgenie) → frena el escalamiento
   automático y avisa que alguien lo tiene. Objetivo: minutos.
2. **Leer el handoff de L1**: qué síntoma, desde cuándo, a quién afecta, qué
   ya se probó, ticket o alerta de origen.
3. **Confirmar que es real**: mirar el dashboard. ¿La métrica realmente se
   movió? ¿Hay otras alertas relacionadas? (descartar falso positivo o alerta
   *flapping*).
4. **Estimar el alcance (blast radius)**: ¿un cliente, una región, un
   servicio, todo? ¿Afecta dinero, pagos, login, datos?
5. **Asignar severidad (SEV)** con la matriz de abajo.
6. **Declarar el incidente** si es SEV1/SEV2: abrir canal (Slack / Teams),
   nombrar **Incident Commander (IC)**, avisar a stakeholders, abrir el
   documento de timeline.

### Matriz de severidad (típica, cada empresa ajusta los nombres)

| SEV | Criterio | Ejemplo | Respuesta |
|---|---|---|---|
| **SEV1** | Caída total o pérdida de dinero o datos; muchos usuarios | Checkout caído, base de datos corrupta, fuga de datos | Todos a bordo ya, IC dedicado, updates cada 15–30 min, ejecutivos informados |
| **SEV2** | Degradación fuerte o funcionalidad crítica caída para una parte | Latencia ×5 en una región, pagos con tarjeta X fallan | On-call + equipo dueño, IC, updates cada 30–60 min |
| **SEV3** | Impacto menor, hay workaround | Un reporte interno no carga | On-call en horario, ticket |
| **SEV4** | Sin impacto al usuario | Alerta de disco al 70% | Ticket, backlog |

> **Regla**: ante la duda, **declarás la severidad más alta** y después la
> bajás. Bajar una severidad es barato; subirla tarde es caro.

### Roles en un incidente grande (SEV1/SEV2)

| Rol | Qué hace | Qué **no** hace |
|---|---|---|
| **Incident Commander (IC)** | Coordina, decide, asigna tareas, mantiene el foco | No se pone a debuggear (si lo hace, nadie coordina) |
| **Ops / Tech Lead** | Ejecuta el diagnóstico y las acciones técnicas | No comunica afuera |
| **Comms Lead** | Updates a stakeholders, status page, soporte al cliente | No toca sistemas |
| **Scribe** | Anota la timeline con horas exactas | — |

En incidentes chicos, una persona hace todo — pero **sabe** que está
cumpliendo los cuatro roles.

---

## Fase 2 — Mitigar (T+5 a T+30 min)

### Principio

> **Restaurar el servicio > encontrar la causa raíz.**
> El usuario no quiere saber por qué se cayó; quiere que funcione.

La mitigación puede ser "fea" (rollback, apagar una feature, escalar a lo
bruto). Está bien: la solución definitiva viene en la fase 4.

### La pregunta mágica: **"¿Qué cambió?"**

El ~70–80% de los incidentes vienen de un **cambio**. Revisar en este orden:

1. **Deploys** recientes de la app (y de sus dependencias).
2. **Cambios de configuración** / feature flags / secretos rotados.
3. **Cambios de infraestructura** (Terraform apply, upgrade de cluster, cambio de DNS, reglas de firewall / Security Groups).
4. **Tráfico**: pico, campaña, bot, cliente nuevo, Hot Sale / Black Friday.
5. **Dependencias externas**: status page del proveedor cloud, APIs de terceros.
6. **Tiempo**: certificados vencidos, tokens expirados, cron jobs, cambio de horario, fin de mes.

Si algo cambió **justo** cuando empezó el problema → candidato número uno a revertir.

### Menú de palancas de mitigación

| Situación | Palanca |
|---|---|
| Empezó con un deploy | **Rollback** al artefacto anterior (o cortar el canary / volver el tráfico a blue) |
| Empezó con una config / feature flag | Revertir la config o **apagar el feature flag** |
| Una región / zona / nodo falla | **Failover** / sacar del balanceador / *cordon + drain* del nodo |
| Saturación (CPU, memoria, conexiones) | **Escalar** horizontal (más réplicas) o vertical; subir límites temporalmente |
| Una dependencia lenta arrastra todo | **Circuit breaker**, timeouts más cortos, degradar la funcionalidad (*graceful degradation*) |
| Pico de tráfico / abuso | **Rate limiting**, bloquear IPs / bot en WAF, cola |
| Proceso colgado / leak | Reiniciar pods / instancias (**después de** guardar evidencia) |
| Base de datos saturada | Matar queries largas, failover a réplica, desactivar jobs batch no críticos |

### Rollback vs. roll-forward

- **Rollback** (volver a la versión anterior): primera opción por defecto. Es
  rápido, conocido y probado.
- **Roll-forward** (hotfix nuevo para adelante): solo cuando el rollback **no
  es posible o es peor** — por ejemplo, hubo una **migración de base de datos
  no reversible**, o la versión anterior tiene un bug de seguridad.

### Reglas de la fase de mitigación

1. **Un cambio a la vez.** Si tocás tres cosas y se arregla, no sabés cuál fue.
2. **Anunciar antes de tocar** en el canal: *"Voy a hacer rollback de X a la v1.2.3"*.
3. **Preservar evidencia** antes de reiniciar: logs, `kubectl describe`,
   heap dump / thread dump, snapshot. Reiniciar borra pistas.
4. **Time-box**: si en ~15 min una mitigación no avanza, probar la siguiente o escalar.

---

## Fase 3 — Diagnosticar (en paralelo o después de mitigar)

### Paso 1: Acotar el problema (las 4 W)

- **¿Qué?** síntoma exacto (errores 5xx, latencia, timeouts, datos incorrectos).
- **¿Dónde?** qué servicio, región, zona, cluster, endpoint, cliente.
- **¿Cuándo?** hora exacta de inicio (el gráfico la muestra), ¿es constante o intermitente?
- **¿A quién?** todos los usuarios o un subconjunto (un país, una versión de la app, un tenant).

Comparar contra lo que **sí** funciona: *"falla en us-east-1 pero no en
us-west-2"* ya descarta media lista de causas.

### Paso 2: Mirar las señales con un método

**Golden signals** (Google SRE) — para cualquier servicio:
- **Latency** (latencia, separando requests exitosos de fallidos)
- **Traffic** (tráfico: RPS)
- **Errors** (tasa de errores)
- **Saturation** (saturación: qué tan lleno está el recurso)

**RED** — para servicios / APIs: **R**ate, **E**rrors, **D**uration.
**USE** — para recursos (CPU, disco, red, pool de conexiones): **U**tilization, **S**aturation, **E**rrors.

### Paso 3: Recorrer el camino del request (de afuera hacia adentro)

```
Usuario → DNS → CDN / WAF → Load Balancer → Ingress → Servicio → Dependencias (DB, cache, colas, APIs externas) → Infra (nodos, red, disco)
```

En cada salto: ¿llega el request? ¿Sale bien? El primer salto que falla es
donde está el problema. Las **trazas distribuidas** (Application Insights,
X-Ray, Cloud Trace, Jaeger, Datadog APM) hacen este recorrido por vos.

### Paso 4: Hipótesis → prueba → descartar

1. Formular **una** hipótesis concreta: *"el pool de conexiones a la DB está agotado"*.
2. Definir qué evidencia la confirma o la descarta: *"si es eso, veo `too many connections` en logs y conexiones activas = máximo"*.
3. Mirar esa evidencia.
4. Confirmada → actuar. Descartada → anotarla en la timeline (también es información) y pasar a la siguiente.

### Herramientas por nube (dónde mirar)

| Qué | Azure | AWS | GCP | Neutral |
|---|---|---|---|---|
| Métricas | Azure Monitor Metrics | CloudWatch Metrics | Cloud Monitoring | Prometheus + Grafana, Datadog |
| Logs | Log Analytics (KQL) | CloudWatch Logs Insights | Cloud Logging | Loki, Splunk, Elastic |
| Trazas | Application Insights | X-Ray | Cloud Trace | Jaeger, Tempo, Datadog APM |
| Quién cambió qué (auditoría) | Activity Log | CloudTrail | Cloud Audit Logs | Historial de CI/CD, Git |
| Estado del proveedor | Azure Status / Service Health | AWS Health Dashboard | Google Cloud Status | — |

### Kubernetes: secuencia mínima

```bash
kubectl get pods -n <ns> -o wide              # estado, reinicios, en qué nodo
kubectl describe pod <pod> -n <ns>            # Events: OOMKilled, FailedScheduling, ImagePullBackOff, probes fallando
kubectl logs <pod> -n <ns> --previous         # logs del contenedor ANTERIOR (el que crasheó)
kubectl get events -n <ns> --sort-by=.lastTimestamp
kubectl top pods -n <ns> / kubectl top nodes  # consumo real vs. requests/limits
kubectl rollout history deploy/<app> -n <ns>  # qué versión está y cuál había antes
kubectl rollout undo deploy/<app> -n <ns>     # rollback
```

| Estado / señal | Causa típica |
|---|---|
| `CrashLoopBackOff` | La app arranca y muere: error de config, variable faltante, dependencia caída al arrancar. Ver `logs --previous` |
| `OOMKilled` (exit code 137) | Superó el **memory limit**. Leak o limit muy bajo |
| `ImagePullBackOff` | Imagen o tag inexistente, sin permisos al registry |
| `Pending` | No hay nodo con recursos suficientes, taints, PVC sin bindear |
| Readiness probe fallando | Pod vivo pero fuera del Service → menos capacidad, 503 |
| Exit code 1 | Error de la aplicación |
| Exit code 143 | SIGTERM (terminado ordenadamente — ej. scale-down, deploy) |

### Causas raíz frecuentes (tener la lista en la cabeza)

- Deploy con bug / config errónea.
- Certificado TLS vencido.
- DNS (cambio, TTL, resolución interna).
- Recursos agotados: disco lleno, memoria, file descriptors, pool de conexiones, cuotas del proveedor cloud.
- Dependencia lenta sin timeout → **cascada** (los threads quedan esperando).
- **Retry storm**: todos reintentan a la vez y rematan al servicio que se estaba recuperando (solución: retries con *exponential backoff + jitter*).
- Thundering herd: cache expira y todos van a la DB al mismo tiempo.
- Secreto o token rotado / expirado.
- Problema del proveedor cloud (región, zona, servicio gestionado).

---

## Fase 4 — Resolver y verificar

### Quién hace qué

- **L2**: fix operativo — config, infraestructura, escalar de forma permanente, aplicar runbook.
- **L3**: fix de código — hotfix, PR con test que reproduce el bug, deploy controlado (canary).

### Verificación (no se cierra "porque parece que anda")

1. **Métricas normalizadas** durante un período razonable (ej. 15–30 min
   estables, o un ciclo completo si el problema era intermitente).
2. Tasa de errores y latencia de vuelta al **SLO**.
3. **Prueba sintética** o prueba manual del flujo afectado.
4. **Confirmación de quien reportó** (L1, el cliente, el equipo afectado).
5. Alertas resueltas solas (no silenciadas a mano).

### Cierre

- Pasar a estado **"resuelto / monitoreando"** antes de "cerrado".
- Anotar en la timeline qué arregló el problema y a qué hora.
- Dejar registradas las **mitigaciones temporales** que hay que deshacer
  (réplicas extra, límites subidos, feature flag apagado) — si no, se vuelven deuda.
- Último update a stakeholders: resuelto, impacto, próximos pasos (post-mortem).

---

## Fase 5 — Aprender (post-mortem / RCA)

### Cuándo

Siempre para SEV1 y SEV2; opcional para SEV3 que se repiten. Borrador en los
primeros días (típicamente dentro de los 5 días hábiles), mientras está fresco.

### Principio **blameless**

Se asume que todos actuaron bien con la información que tenían. La pregunta
no es *"¿quién se equivocó?"* sino *"¿qué del sistema permitió que el error
llegara a producción y no lo detectamos antes?"*. Si la gente teme ser
culpada, esconde información y el sistema no mejora.

### Estructura del documento de post-mortem

1. **Resumen**: qué pasó en 2–3 líneas.
2. **Impacto**: duración, usuarios / transacciones afectadas, dinero, SLO / error budget consumido.
3. **Timeline**: hora por hora — detección, ack, declaración, mitigación, resolución.
4. **Causa raíz** y **factores contribuyentes** (casi nunca hay una sola causa).
5. **Qué salió bien / qué salió mal / dónde tuvimos suerte.**
6. **Action items**: cada uno con **dueño y fecha**, priorizados.

### 5 porqués (técnica para llegar a la causa raíz)

Ejemplo:
1. ¿Por qué se cayó el checkout? → La API de pagos devolvía 500.
2. ¿Por qué? → No podía conectarse a la base de datos.
3. ¿Por qué? → El pool de conexiones estaba agotado.
4. ¿Por qué? → Un deploy agregó una query sin índice que tardaba 30 s y retenía conexiones.
5. ¿Por qué llegó a producción? → No hay test de performance en el pipeline ni alerta de queries lentas.

La causa raíz real es la del **último porqué** (proceso / sistema), no la del primero.

### Tipos de action items (cubrir los tres)

| Tipo | Pregunta | Ejemplo |
|---|---|---|
| **Prevenir** | ¿Cómo evito que vuelva a pasar? | Test de performance en CI, revisión de migraciones |
| **Detectar** | ¿Cómo me entero antes (o antes que el cliente)? | Alerta de queries lentas, alerta de pool de conexiones al 80% |
| **Mitigar** | ¿Cómo lo arreglo más rápido la próxima? | Runbook nuevo, rollback automático por canary |

### Métricas de respuesta a incidentes

| Métrica | Mide | Desde → hasta |
|---|---|---|
| **MTTD** (Mean Time To Detect) | Qué tan rápido nos enteramos | Inicio del problema → alerta |
| **MTTA** (Mean Time To Acknowledge) | Qué tan rápido responde el on-call | Alerta → ack |
| **MTTM** (Mean Time To Mitigate) | Qué tan rápido frenamos el daño | Inicio → impacto detenido |
| **MTTR** (Mean Time To Resolve / Recover) | Qué tan rápido lo arreglamos | Inicio → resuelto |
| **MTBF** (Mean Time Between Failures) | Cada cuánto falla | Entre incidentes |

Relación con **SLO** y **error budget**: si el SLO es 99,9% mensual, el error
budget son ~43 minutos de indisponibilidad por mes. Un incidente que consume
mucho error budget justifica frenar features y priorizar confiabilidad.

---

## El hilo transversal — Comunicar y escalar

### Comunicación

- **Cadencia fija** según severidad (SEV1: cada 15–30 min), **aunque no haya
  novedades**: *"Sin novedades, seguimos investigando X, próximo update 10:45"*.
- **Separar audiencias**: canal técnico (el war room) vs. canal de
  stakeholders vs. clientes (status page). No mezclar.
- Hablar de **impacto** y **próximos pasos**, no de detalles técnicos internos, hacia afuera.

**Plantilla de update:**
```
[SEV2] [INVESTIGANDO | MITIGADO | RESUELTO] Pagos con tarjeta en MX
Impacto: ~15% de pagos con tarjeta fallan en México desde las 14:05.
Qué sabemos: coincide con deploy de payments-api v3.2 a las 14:02.
Qué estamos haciendo: rollback a v3.1 en curso.
Próximo update: 14:45 o antes si cambia algo.
IC: <nombre>
```

### Escalamiento — cuándo y cómo

**Escalá cuando:**
- Pasaron ~15–30 min **sin progreso** (time-box).
- El problema está fuera de tu área / acceso / conocimiento.
- La severidad sube (más usuarios, más dinero, riesgo de datos o seguridad).
- La acción necesaria es riesgosa o irreversible y necesita aprobación.

**Escalar no es fracasar.** En una entrevista, *"escalo a tiempo"* suma
puntos; *"me quedé dos horas solo hasta resolverlo"* (modo héroe) resta.

**Handoff al escalar (o al cambiar de turno)** — lo que tiene que recibir el siguiente:
1. Síntoma e impacto actual.
2. Desde cuándo y severidad.
3. Qué se descartó (y cómo).
4. Qué se intentó y qué resultado tuvo.
5. Hipótesis actual.
6. Links: dashboard, logs, ticket, canal, timeline.

---

## Antipatrones (lo que te resta puntos en una entrevista)

| Antipatrón | Qué hacer en cambio |
|---|---|
| Debuggear la causa raíz mientras los usuarios siguen afectados | Mitigar primero (rollback / failover / feature flag) |
| Cambiar varias cosas a la vez | Un cambio por vez, anunciado y anotado |
| Reiniciar todo sin guardar evidencia | Capturar logs / describe / dump, después reiniciar |
| Silencio durante el incidente | Updates con cadencia fija aunque no haya novedades |
| Modo héroe (no pedir ayuda) | Time-box y escalar |
| El IC se pone a debuggear | El IC coordina; delega lo técnico |
| Cerrar porque "parece que anda" | Verificar con métricas + confirmación del afectado |
| Post-mortem con culpables | Blameless, foco en el sistema y el proceso |
| Action items sin dueño ni fecha | Cada action item con dueño, fecha y prioridad |
| Acciones destructivas o irreversibles bajo presión | Pedir segunda opinión / aprobación, preferir lo reversible |

---

## Checklist de bolsillo

```
☐ 1. ACK de la alerta
☐ 2. Leer handoff de L1 — ¿qué, desde cuándo, a quién, qué se probó?
☐ 3. ¿Es real? → dashboard
☐ 4. Alcance (blast radius) → SEV (ante la duda, más alta)
☐ 5. SEV1/2 → declarar incidente: canal, IC, timeline, primer update
☐ 6. ¿QUÉ CAMBIÓ? → deploy, config, infra, tráfico, proveedor, tiempo
☐ 7. MITIGAR: rollback / feature flag / failover / escalar / rate limit
       (un cambio a la vez, anunciado, evidencia guardada)
☐ 8. DIAGNOSTICAR: acotar (qué/dónde/cuándo/a quién) → golden signals
       → camino del request → hipótesis de a una
☐ 9. ¿15–30 min sin progreso? → ESCALAR con handoff completo
☐ 10. RESOLVER: fix L2 (config/infra) o L3 (código)
☐ 11. VERIFICAR: métricas estables + SLO + prueba + confirmación
☐ 12. Deshacer mitigaciones temporales, último update, cerrar
☐ 13. POST-MORTEM blameless: timeline, impacto, causa raíz (5 porqués),
       action items (prevenir / detectar / mitigar) con dueño y fecha
☐ ∞  Comunicar con cadencia fija durante TODO el proceso
```

---

## Glosario rápido

| Término | Significado |
|---|---|
| **On-call** | Persona de guardia responsable de responder alertas en su turno |
| **Ack (acknowledge)** | Confirmar que tomaste la alerta; frena el escalamiento automático |
| **Triage** | Clasificar: ¿es real?, ¿de quién es?, ¿qué tan grave? |
| **SEV (severidad)** | Nivel de gravedad del incidente (SEV1 = máximo) |
| **Incident Commander (IC)** | Quien coordina el incidente; decide, no debuggea |
| **War room** | Canal o sala donde se trabaja el incidente |
| **Blast radius** | Alcance del impacto (cuánto y a quién afecta) |
| **Mitigación** | Acción que frena el impacto sin ser necesariamente la solución definitiva |
| **Rollback / roll-forward** | Volver a la versión anterior / arreglar con una versión nueva |
| **Feature flag** | Interruptor para prender o apagar una funcionalidad sin deploy |
| **Failover** | Pasar el tráfico a otra instancia / región / réplica sana |
| **Circuit breaker** | Corta las llamadas a una dependencia que falla para no arrastrar al resto |
| **Graceful degradation** | Seguir funcionando con menos funcionalidad en vez de caerse entero |
| **Runbook** | Pasos concretos para resolver una alerta o situación conocida |
| **Golden signals** | Latency, Traffic, Errors, Saturation |
| **RED / USE** | Rate-Errors-Duration (servicios) / Utilization-Saturation-Errors (recursos) |
| **SLI / SLO / SLA** | Indicador medido / objetivo interno / contrato con el cliente (con penalidades) |
| **Error budget** | Cuánta falla te "permite" el SLO (100% − SLO) |
| **Post-mortem / RCA** | Análisis posterior al incidente (Root Cause Analysis) |
| **Blameless** | Sin culpables: foco en el sistema, no en las personas |
| **MTTD / MTTA / MTTR** | Tiempo medio para detectar / reconocer / resolver |
| **Toil** | Trabajo manual repetitivo que debería automatizarse |
| **Break-glass** | Acceso de emergencia con privilegios elevados, auditado |
