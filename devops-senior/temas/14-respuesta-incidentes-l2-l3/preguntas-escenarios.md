# Banco de preguntas — Respuesta a incidentes L2/L3

Material de práctica del tema 14. La teoría completa está en [`README.md`](README.md).

**Cómo se usa** (según las preferencias del roadmap): **una pregunta por
vez**. Pedime *"tomame el tema 14"* (o un bloque puntual, ej. *"bloque C"*)
y te hago las preguntas de a una, corrijo cada respuesta y recién después
pasamos a la siguiente. Si practicás solo, tapá la respuesta (está oculta
en cada `▶ Respuesta esperada`) y respondé en voz alta antes de abrirla.

Los **escenarios del bloque H** son los más parecidos a una entrevista real:
se juegan por etapas — te doy la situación, me decís qué hacés, y yo te
revelo qué encontrás.

Objetivo para pasar de tema: **≥ 80%**, y poder recitar las 5 fases + el
hilo de comunicación **sin mirar**.

Bloques:
- [A. Conceptos base](#a-conceptos-base)
- [B. Fase 1 — Recibir y clasificar](#b-fase-1--recibir-y-clasificar)
- [C. Fase 2 — Mitigar](#c-fase-2--mitigar)
- [D. Fase 3 — Diagnosticar](#d-fase-3--diagnosticar)
- [E. Fase 4 — Resolver y verificar](#e-fase-4--resolver-y-verificar)
- [F. Comunicar y escalar](#f-comunicar-y-escalar)
- [G. Fase 5 — Post-mortem](#g-fase-5--post-mortem)
- [H. Escenarios completos (role-play)](#h-escenarios-completos-role-play)
- [I. Preguntas de criterio (trampas de entrevista)](#i-preguntas-de-criterio-trampas-de-entrevista)

---

## A. Conceptos base

**A1. Diferencia entre L1, L2 y L3. ¿Qué entrega cada uno?**
<details><summary>▶ Respuesta esperada</summary>

- **L1**: primera línea. Recibe, clasifica, aplica runbooks conocidos.
  Entrega: problema resuelto por runbook **o** escalamiento con buen handoff.
- **L2**: especialista / SRE / plataforma. Diagnóstico profundo con
  observabilidad, config e infraestructura. Entrega: **servicio restaurado**
  (mitigación) y escalamiento documentado si la causa está en el código.
- **L3**: equipo dueño del sistema. Entrega: **fix definitivo** (código / diseño) y causa raíz.
- (Bonus) **L4**: proveedor externo (AWS, Azure, GCP, vendor).
</details>

**A2. Nombrá las 5 fases de respuesta a incidentes en orden, y el hilo transversal.**
<details><summary>▶ Respuesta esperada</summary>

1. Recibir y clasificar (triage)
2. Mitigar
3. Diagnosticar
4. Resolver y verificar
5. Aprender (post-mortem)

Hilo transversal: **comunicar y escalar** durante todo el proceso.
Frase: *"Clasifico, freno, entiendo, arreglo, aprendo — y aviso todo el tiempo."*
</details>

**A3. ¿Por qué se mitiga antes de diagnosticar? ¿Hay excepciones?**
<details><summary>▶ Respuesta esperada</summary>

Porque cada minuto de diagnóstico con el servicio caído es impacto real
(usuarios, dinero, error budget). Restaurar el servicio es la prioridad; la
causa raíz se busca después con calma.

Excepciones / matices:
- Si **no hay una mitigación obvia** (no hubo cambios, no hay a qué hacer
  rollback), hay que diagnosticar lo mínimo para saber **qué** mitigar.
- **Incidente de seguridad**: antes de "restaurar" hay que **contener** y
  **preservar evidencia** forense (no borrar la instancia comprometida).
- Diagnóstico y mitigación muchas veces van **en paralelo** con más de una persona.
</details>

**A4. ¿Qué son las golden signals? ¿Y RED / USE?**
<details><summary>▶ Respuesta esperada</summary>

- **Golden signals**: Latency, Traffic, Errors, Saturation.
- **RED** (para servicios): Rate, Errors, Duration.
- **USE** (para recursos como CPU, disco, pool de conexiones): Utilization, Saturation, Errors.
</details>

**A5. Diferencia entre SLI, SLO y SLA. ¿Qué es el error budget?**
<details><summary>▶ Respuesta esperada</summary>

- **SLI**: la métrica medida (ej. % de requests exitosos en < 300 ms).
- **SLO**: objetivo interno sobre el SLI (ej. 99,9% mensual).
- **SLA**: compromiso contractual con el cliente, con penalidades; suele ser más laxo que el SLO.
- **Error budget**: 100% − SLO. Con 99,9% mensual ≈ 43 min de falla permitidos.
  Si se consume, se priorizan trabajos de confiabilidad sobre features nuevas.
</details>

**A6. Definí MTTD, MTTA y MTTR. ¿Cuál mejorarías con mejores alertas? ¿Y con runbooks?**
<details><summary>▶ Respuesta esperada</summary>

- **MTTD**: inicio del problema → detección (alerta).
- **MTTA**: alerta → ack del on-call.
- **MTTR**: inicio → resuelto / recuperado.
- Mejores **alertas** (basadas en síntomas / SLO) → bajan el **MTTD**.
- Mejores **runbooks** y rollback automatizado → bajan el **MTTR** (y el MTTM).
- Mejor **rotación de on-call** / escalation policy → baja el **MTTA**.
</details>

**A7. ¿Qué roles hay en un incidente SEV1 y qué NO debe hacer el Incident Commander?**
<details><summary>▶ Respuesta esperada</summary>

- **Incident Commander (IC)**: coordina, decide, asigna, mantiene el foco.
- **Ops / Tech Lead**: ejecuta el diagnóstico y las acciones técnicas.
- **Comms Lead**: updates a stakeholders, status page, soporte.
- **Scribe**: timeline con horas exactas.

El **IC no debe ponerse a debuggear**: si lo hace, nadie coordina, nadie
comunica y se pierde la visión global.
</details>

**A8. ¿Qué tiene que existir ANTES de un incidente para que el on-call funcione?**
<details><summary>▶ Respuesta esperada</summary>

Rotación de on-call con primario y secundario + escalation policy; alertas
accionables (con dueño, severidad y runbook); runbooks actualizados;
dashboards con golden signals; **accesos probados** (VPN, consola,
`kubectl`, break-glass); canal y plantilla de incidentes listos.
</details>

---

## B. Fase 1 — Recibir y clasificar

**B1. Te suena el pager. Enumerá en orden lo que hacés en los primeros 5 minutos.**
<details><summary>▶ Respuesta esperada</summary>

1. **Ack** de la alerta.
2. Leer el contexto / handoff de L1 (síntoma, desde cuándo, a quién, qué se probó).
3. **Confirmar que es real** en el dashboard (descartar falso positivo).
4. Estimar **alcance (blast radius)**.
5. Asignar **severidad**.
6. Si es SEV1/SEV2: **declarar el incidente** (canal, IC, timeline, primer update).
</details>

**B2. ¿Qué información mínima tiene que traer un escalamiento de L1 a L2?**
<details><summary>▶ Respuesta esperada</summary>

Síntoma e impacto; desde cuándo; a quién afecta (alcance); severidad
estimada; qué se probó y con qué resultado; links (alerta, ticket,
dashboard, logs); cómo reproducirlo si aplica.
</details>

**B3. Clasificá la severidad: (a) el checkout falla para el 100% de usuarios; (b) latencia ×3 solo en una región, sin errores; (c) un dashboard interno de finanzas no carga; (d) disco de un nodo al 75%.**
<details><summary>▶ Respuesta esperada</summary>

- (a) **SEV1** — caída total de un flujo que mueve dinero.
- (b) **SEV2** — degradación fuerte, acotada (podría ser SEV3 si la latencia sigue dentro del SLO).
- (c) **SEV3** — interno, con workaround, sin impacto al cliente.
- (d) **SEV4** — sin impacto; ticket (salvo que esté creciendo rápido → anticipar).
</details>

**B4. No sabés si algo es SEV1 o SEV2. ¿Qué hacés y por qué?**
<details><summary>▶ Respuesta esperada</summary>

Declarar la **más alta (SEV1)** y bajarla cuando haya más información. Bajar
una severidad es barato (se desmoviliza gente); subirla tarde es caro (se
perdió tiempo con menos gente y sin comunicación a stakeholders).
</details>

**B5. Te llega una alerta, mirás el dashboard y la métrica está normal. ¿Qué hacés?**
<details><summary>▶ Respuesta esperada</summary>

- Verificar que estás mirando **la misma métrica / ventana / región** que la alerta.
- Revisar si la alerta es **flapping** (se dispara y se resuelve sola) o si
  fue un pico corto real.
- Mirar señales relacionadas (logs de errores, otros servicios).
- Si es falso positivo: resolverla, **anotarlo** y abrir ticket para ajustar
  la alerta (umbral, ventana, condición). Una alerta ruidosa entrena a la gente a ignorarla.
</details>

**B6. ¿Qué es "declarar un incidente" concretamente? ¿Qué se pone en marcha?**
<details><summary>▶ Respuesta esperada</summary>

Formalizarlo en la herramienta de incidentes: se crea el canal (war room),
se asigna **IC** y roles, se abre el documento de **timeline**, se fija la
**severidad**, se envía el **primer update** a stakeholders y se define la
cadencia de comunicación. Si hay impacto al cliente, se actualiza la **status page**.
</details>

---

## C. Fase 2 — Mitigar

**C1. ¿Cuál es "la pregunta mágica" al empezar a mitigar? ¿Qué revisás para responderla?**
<details><summary>▶ Respuesta esperada</summary>

**"¿Qué cambió?"** Revisar: deploys (propios y de dependencias), cambios de
config / feature flags / secretos, cambios de infraestructura (Terraform,
upgrades, DNS, firewall), tráfico (picos, bots, campañas), estado del
proveedor cloud y causas por tiempo (certificados, tokens, cron jobs).

Dónde: historial de CI/CD, auditoría (Activity Log / CloudTrail / Cloud
Audit Logs), canal de deploys, status page del proveedor.
</details>

**C2. Hubo un deploy hace 12 minutos y los errores empezaron hace 10. ¿Qué hacés?**
<details><summary>▶ Respuesta esperada</summary>

**Rollback** inmediato a la versión anterior (o cortar el canary). Anunciarlo
en el canal antes de ejecutarlo, verificar que las métricas se recuperan, y
**después** investigar qué tenía el deploy. No ponerse a leer el diff con
los usuarios afectados.
</details>

**C3. ¿Cuándo NO harías rollback y harías roll-forward?**
<details><summary>▶ Respuesta esperada</summary>

- El deploy incluyó una **migración de base de datos no reversible** (la
  versión vieja no entiende el nuevo esquema).
- La versión anterior tiene un problema peor (ej. vulnerabilidad de seguridad).
- Hubo cambios de contrato con otros servicios que ya dependen de la nueva versión.
- El fix es trivial y el pipeline de hotfix es más rápido y seguro que el rollback.
</details>

**C4. Nombrá 6 palancas de mitigación y cuándo usar cada una.**
<details><summary>▶ Respuesta esperada</summary>

1. **Rollback** — empezó con un deploy.
2. **Feature flag off / revertir config** — empezó con un cambio de config o feature.
3. **Failover / sacar del balanceador** — una región, zona o nodo falla.
4. **Escalar** (horizontal / vertical) — saturación.
5. **Circuit breaker / degradar funcionalidad** — una dependencia lenta arrastra todo.
6. **Rate limiting / WAF** — pico de tráfico o abuso.
7. (Bonus) **Reiniciar** — proceso colgado / leak, guardando evidencia antes.
</details>

**C5. ¿Por qué "un cambio a la vez"?**
<details><summary>▶ Respuesta esperada</summary>

Si cambiás varias cosas y se arregla, no sabés cuál funcionó (no sabés qué
dejar y qué revertir, y el post-mortem pierde la causa). Si empeora, no
sabés cuál lo empeoró. Además, cada cambio bajo presión es un riesgo nuevo.
</details>

**C6. Antes de reiniciar un pod / servicio que está colgado, ¿qué hacés?**
<details><summary>▶ Respuesta esperada</summary>

**Preservar evidencia**: `kubectl describe pod`, `kubectl logs` (y
`--previous`), thread dump / heap dump si es JVM u otro runtime con esa
opción, métricas del momento, snapshot si aplica. Opcional: sacar un pod del
Service (quitarle el label) para analizarlo vivo sin tráfico. Después reiniciar.
</details>

**C7. Una dependencia externa (API de un proveedor de pagos) está lenta y tus threads quedan esperando hasta que tu servicio entero deja de responder. ¿Cómo mitigás?**
<details><summary>▶ Respuesta esperada</summary>

- **Timeouts** más cortos hacia esa dependencia.
- **Circuit breaker**: cortar llamadas a esa dependencia y responder rápido
  con error controlado / fallback.
- **Graceful degradation**: deshabilitar solo esa funcionalidad (ej. ese
  medio de pago) vía feature flag, y que el resto funcione.
- **Bulkhead**: aislar los recursos (pool de threads / conexiones) de esa
  dependencia para que no agote los del resto.
- Avisar al proveedor (L4) y revisar su status page.
</details>

**C8. El servicio se está recuperando pero se vuelve a caer cada vez que vuelve a levantar. Los logs muestran una avalancha de requests de clientes internos. ¿Qué pasa y qué hacés?**
<details><summary>▶ Respuesta esperada</summary>

**Retry storm / thundering herd**: todos los clientes reintentan al mismo
tiempo y rematan al servicio apenas levanta.

Mitigación: **rate limiting** / *load shedding* en la entrada; levantar el
tráfico de forma gradual; pedir a los clientes que corten retries o
desactivarlos por config. Fix a futuro: retries con **exponential backoff +
jitter**, límite de reintentos y circuit breakers en los clientes.
</details>

---

## D. Fase 3 — Diagnosticar

**D1. ¿Cuáles son las 4 preguntas para acotar un problema?**
<details><summary>▶ Respuesta esperada</summary>

**¿Qué?** (síntoma exacto), **¿Dónde?** (servicio, región, endpoint),
**¿Cuándo?** (hora de inicio, constante o intermitente), **¿A quién?**
(todos o un subconjunto). Y comparar con lo que **sí** funciona.
</details>

**D2. Describí el "camino del request" y cómo lo usás para diagnosticar.**
<details><summary>▶ Respuesta esperada</summary>

Usuario → DNS → CDN / WAF → Load Balancer → Ingress → Servicio →
Dependencias (DB, cache, colas, APIs) → Infra (nodos, red, disco).

Se recorre **de afuera hacia adentro**, verificando en cada salto si el
request llega y si sale bien. El primer salto que falla localiza el
problema. Las trazas distribuidas (Application Insights / X-Ray / Cloud
Trace / Jaeger / Datadog APM) muestran este recorrido.
</details>

**D3. ¿Cómo se trabaja con hipótesis durante el diagnóstico?**
<details><summary>▶ Respuesta esperada</summary>

1. Formular **una** hipótesis concreta.
2. Definir qué evidencia la confirma o la descarta **antes** de mirar.
3. Mirar esa evidencia.
4. Confirmada → actuar. Descartada → **anotarla** en la timeline y pasar a la siguiente.

Ordenar las hipótesis por probabilidad × facilidad de verificar.
</details>

**D4. Un pod está en `CrashLoopBackOff`. ¿Qué comandos corrés y en qué orden?**
<details><summary>▶ Respuesta esperada</summary>

1. `kubectl describe pod <pod>` → Events, último estado, **exit code**, motivo (OOMKilled, probe fallida).
2. `kubectl logs <pod> --previous` → logs del contenedor **que crasheó** (sin `--previous` ves el que acaba de arrancar).
3. `kubectl get events --sort-by=.lastTimestamp`.
4. `kubectl rollout history deploy/<app>` → ¿hubo un cambio de versión?
5. Revisar ConfigMaps / Secrets / variables de entorno si los logs indican config faltante.

Exit codes: **137** = OOMKilled / SIGKILL; **143** = SIGTERM; **1** = error de la app.
</details>

**D5. Exit code 137 y estado `OOMKilled`. ¿Qué significa y qué opciones tenés?**
<details><summary>▶ Respuesta esperada</summary>

El contenedor superó su **memory limit** y el kernel lo mató. Opciones:
- **Mitigar**: subir el memory limit temporalmente / más réplicas para repartir carga.
- **Diagnosticar**: ¿leak (memoria crece sin parar) o limit muy bajo para la
  carga real? Mirar la curva de memoria en el tiempo y si coincide con un deploy.
- **Resolver**: fix del leak (L3) o ajustar requests / limits según el consumo real.
</details>

**D6. Los usuarios reportan errores de "certificado no válido" desde hace 20 minutos. ¿Qué revisás?**
<details><summary>▶ Respuesta esperada</summary>

- **Fecha de vencimiento** del certificado (`openssl s_client -connect host:443 | openssl x509 -noout -dates`).
- Si se renovó: ¿se desplegó en **todos** los endpoints (LB, CDN, ingress)? ¿La cadena intermedia está completa?
- ¿El hostname coincide con el certificado (SAN)?
- Automatización de renovación (cert-manager, ACM, Key Vault) — ¿falló?

Mitigación: renovar / subir el certificado válido. Action item: **alerta de
vencimiento** con anticipación (ej. 30 y 7 días) y renovación automática.
</details>

**D7. Un servicio falla solo para usuarios de una región, y solo desde las 14:00. Ninguna alerta de infraestructura. ¿Por dónde empezás?**
<details><summary>▶ Respuesta esperada</summary>

- **¿Qué cambió a las 14:00** en esa región? (deploy regional, cambio de config, DNS, reglas de red).
- **Status page del proveedor cloud** para esa región / zona.
- Comparar la región afectada vs. una sana: misma versión, misma config, mismas dependencias.
- DNS / routing: ¿los usuarios de esa región resuelven a un endpoint distinto?
- Dependencias regionales (réplica de DB, cache regional).
- Mitigación posible mientras tanto: **failover** del tráfico de esa región a otra sana.
</details>

**D8. Latencia alta en la API pero CPU y memoria normales. ¿Qué causas considerás?**
<details><summary>▶ Respuesta esperada</summary>

El cuello de botella no es cómputo; está en algo que **espera**:
- **Dependencia lenta** (DB, API externa, cache) → mirar trazas: qué span crece.
- **Pool de conexiones / threads agotado** (los requests hacen cola).
- **Base de datos**: query sin índice, locks, réplica atrasada.
- **Red / DNS**: resolución lenta, pérdida de paquetes, NAT gateway saturado (puertos SNAT agotados en Azure).
- **Throttling** del proveedor cloud (cuotas, límites de API).
- Garbage collection pausando el proceso (no siempre se ve como CPU alta).
</details>

**D9. ¿Dónde mirás "quién cambió qué" en Azure, AWS y GCP?**
<details><summary>▶ Respuesta esperada</summary>

- **Azure**: Activity Log.
- **AWS**: CloudTrail.
- **GCP**: Cloud Audit Logs.

Más: historial del pipeline de CI/CD, `git log`, `terraform` state / plan
history, `kubectl rollout history`, canal de deploys.
</details>

---

## E. Fase 4 — Resolver y verificar

**E1. Hiciste rollback y los errores bajaron. ¿Ya está? ¿Qué falta?**
<details><summary>▶ Respuesta esperada</summary>

No. El incidente está **mitigado**, no resuelto:
1. **Verificar** que las métricas se mantienen estables un período (15–30 min o un ciclo).
2. Confirmación de quien reportó.
3. Pasar a "mitigado / monitoreando".
4. **Causa raíz** del deploy fallido (L3) → fix con test → nuevo deploy controlado (canary).
5. Post-mortem si es SEV1/SEV2.
</details>

**E2. ¿Qué criterios usás para decir que un incidente está resuelto?**
<details><summary>▶ Respuesta esperada</summary>

Métricas (errores, latencia) normalizadas y estables dentro del **SLO**;
prueba sintética o manual del flujo afectado OK; confirmación del afectado /
L1; alertas resueltas solas (no silenciadas); sin mitigaciones temporales
pendientes sin registrar.
</details>

**E3. Durante el incidente subiste las réplicas de 4 a 20 y apagaste un feature flag. ¿Qué hacés con eso al cerrar?**
<details><summary>▶ Respuesta esperada</summary>

Registrarlas como **mitigaciones temporales** con dueño: decidir si se
revierten (bajar réplicas cuando pase el riesgo, reactivar el feature flag
cuando esté el fix) o se vuelven permanentes (ajustar el HPA / autoscaling).
Si nadie las revierte, se convierten en costo y en deuda invisible.
</details>

**E4. ¿Qué diferencia hay entre el fix de L2 y el de L3? Dame un ejemplo de cada uno para el mismo incidente.**
<details><summary>▶ Respuesta esperada</summary>

Incidente: OOMKilled por un leak de memoria introducido en un deploy.
- **L2**: rollback, o subir el memory limit y las réplicas para estabilizar → servicio restaurado.
- **L3**: encontrar el leak en el código, corregirlo con un test, desplegar con canary → causa raíz eliminada.
</details>

---

## F. Comunicar y escalar

**F1. Escribí un update de incidente para stakeholders.**
<details><summary>▶ Respuesta esperada</summary>

Debe tener: **severidad y estado** (investigando / mitigado / resuelto),
**impacto** en lenguaje de negocio, **qué sabemos**, **qué estamos
haciendo**, **próximo update** con hora, **IC**. Ejemplo:

```
[SEV2] [MITIGADO] Pagos con tarjeta en MX
Impacto: ~15% de pagos con tarjeta fallaron entre 14:05 y 14:31.
Qué sabemos: coincide con deploy de payments-api v3.2 a las 14:02.
Qué hicimos: rollback a v3.1 a las 14:28; tasa de error normal desde 14:31.
Próximo paso: monitoreo 30 min y análisis de causa raíz.
Próximo update: 15:00. IC: <nombre>
```
</details>

**F2. Pasaron 40 minutos, no hay novedades. ¿Mandás update?**
<details><summary>▶ Respuesta esperada</summary>

**Sí.** La cadencia es fija aunque no haya novedades: *"Sin novedades,
seguimos investigando X, descartamos Y, próximo update a las HH:MM"*. El
silencio genera ansiedad, gente que pregunta por privado (interrumpiendo) y
pérdida de confianza.
</details>

**F3. ¿Cuándo escalás? Dame 4 criterios.**
<details><summary>▶ Respuesta esperada</summary>

1. ~15–30 min **sin progreso** (time-box).
2. Fuera de tu área, acceso o conocimiento.
3. La **severidad sube** (más impacto, dinero, datos, seguridad).
4. La acción necesaria es **riesgosa o irreversible** y requiere aprobación.

Escalar a tiempo es una fortaleza, no un fracaso.
</details>

**F4. Tu turno termina en medio del incidente. ¿Qué le entregás a quien te reemplaza?**
<details><summary>▶ Respuesta esperada</summary>

Handoff completo: síntoma e impacto actual; desde cuándo y severidad; qué se
**descartó** (y cómo); qué se **intentó** y resultados; hipótesis actual;
mitigaciones temporales aplicadas; links (dashboard, logs, ticket, canal,
timeline). Idealmente en voz (llamada corta) + por escrito.
</details>

**F5. Un gerente entra al war room y pide explicaciones técnicas detalladas mientras el equipo trabaja. ¿Qué hacés (si sos IC)?**
<details><summary>▶ Respuesta esperada</summary>

Proteger al equipo técnico: redirigir al gerente al **canal de
stakeholders** / al **Comms Lead**, darle un resumen de impacto y próximo
update, y mantener el war room enfocado. Separar audiencias.
</details>

---

## G. Fase 5 — Post-mortem

**G1. ¿Qué significa "blameless" y por qué importa?**
<details><summary>▶ Respuesta esperada</summary>

Se asume que la gente actuó bien con la información que tenía; se busca qué
del **sistema / proceso** permitió el error. Importa porque si la gente teme
ser culpada esconde información, y sin información el sistema no mejora.
"Un humano se equivocó" nunca es una causa raíz: la pregunta es por qué el
sistema lo permitió y no lo detectó.
</details>

**G2. ¿Qué secciones tiene un post-mortem?**
<details><summary>▶ Respuesta esperada</summary>

Resumen; impacto (duración, usuarios, dinero, SLO / error budget); timeline;
causa raíz y factores contribuyentes; qué salió bien / mal / dónde tuvimos
suerte; action items con **dueño y fecha**.
</details>

**G3. Aplicá los 5 porqués a: "un ingeniero borró por error una tabla de producción".**
<details><summary>▶ Respuesta esperada (una posible)</summary>

1. ¿Por qué se perdieron los datos? → Se ejecutó un `DROP TABLE` en producción.
2. ¿Por qué se ejecutó en producción? → El ingeniero creía estar conectado a staging.
3. ¿Por qué no lo distinguió? → Las dos conexiones se ven idénticas y usa las mismas credenciales.
4. ¿Por qué tiene permisos de `DROP` en producción? → No hay separación de privilegios; todos usan un usuario admin.
5. ¿Por qué tardamos en recuperar? → El backup no se probaba y el restore tardó horas.

Causa raíz: **falta de controles del sistema** (privilegios, separación de
entornos, backups probados), no "el ingeniero".
</details>

**G4. ¿Cuáles son los 3 tipos de action items? Dame un ejemplo de cada uno para G3.**
<details><summary>▶ Respuesta esperada</summary>

- **Prevenir**: usuario de solo lectura por defecto en producción; acceso de escritura vía break-glass auditado.
- **Detectar**: alerta ante sentencias DDL en producción; prompt / color distinto en la terminal de producción.
- **Mitigar**: point-in-time restore habilitado y **restore probado** periódicamente; runbook de restauración.
</details>

**G5. ¿Qué hace que un action item sea bueno?**
<details><summary>▶ Respuesta esperada</summary>

Concreto y verificable (no "tener más cuidado"), con **dueño**, **fecha**,
**prioridad**, y enlazado a un ticket que se sigue. Que ataque la causa
sistémica y no solo el síntoma.
</details>

**G6. El mismo incidente se repitió 3 veces en 2 meses, cada vez con post-mortem. ¿Qué está fallando?**
<details><summary>▶ Respuesta esperada</summary>

Los **action items no se ejecutan** (sin dueño, sin prioridad, se pierden en
el backlog) o atacan síntomas en vez de la causa raíz. Solución: seguimiento
formal de action items (revisión semanal, métricas de cierre), escalar la
prioridad usando el **error budget** consumido, y revisar si el análisis de
causa raíz fue profundo (¿llegaron al último porqué?).
</details>

---

## H. Escenarios completos (role-play)

Se juegan **por etapas**. En la sesión te doy solo la situación inicial; cada
"Revelación" la doy recién después de que digas qué hacés. Si practicás solo,
no leas más allá de la etapa en la que estás.

### H1. Checkout caído después de un deploy (el clásico)

**Situación:** 21:40, viernes. PagerDuty: *"checkout-api error rate 35%"*.
L1 escaló: *"Clientes no pueden pagar, en todos los países"*.

<details><summary>▶ Etapa 1 — ¿Qué hacés primero?</summary>

Ack → mirar dashboard (confirmar 35% de 5xx) → alcance: todos los países,
flujo de dinero → **SEV1** → declarar incidente (canal, IC, primer update) →
**"¿qué cambió?"**.

**Revelación:** el canal de deploys muestra `checkout-api v5.8` desplegado a las 21:31.
</details>

<details><summary>▶ Etapa 2 — Con esa información, ¿qué hacés?</summary>

Anunciar y ejecutar **rollback** a v5.7 (`kubectl rollout undo` / pipeline
de rollback / volver el tráfico a blue). Guardar antes logs de algún pod de la v5.8.

**Revelación:** el rollback termina a las 21:50, pero el error rate solo baja de 35% a 30%.
</details>

<details><summary>▶ Etapa 3 — El rollback no resolvió. ¿Qué hacés?</summary>

No asumir que la v5.8 era la causa: **correlación ≠ causalidad**.
- Confirmar que todos los pods corren efectivamente la v5.7.
- Volver a "¿qué cambió?" más amplio: ¿la v5.8 incluyó una **migración de
  DB** que el rollback no revierte? ¿Cambió algo más a las ~21:30 (config,
  dependencias, proveedor de pagos)?
- Acotar: ¿qué endpoints / qué errores? Mirar trazas.
- Update a stakeholders: rollback hecho, impacto parcial persiste.

**Revelación:** las trazas muestran timeouts en las llamadas al proveedor de
pagos externo; su status page reporta degradación desde las 21:28.
</details>

<details><summary>▶ Etapa 4 — ¿Y ahora?</summary>

- Es una dependencia externa (**L4**): abrir caso con el proveedor.
- Mitigar de nuestro lado: **circuit breaker** / timeouts cortos para no
  agotar threads; si hay un **proveedor de pagos alternativo**, hacer
  failover vía feature flag; mensaje claro al usuario (*"reintentá en unos minutos"*).
- Decidir si se re-despliega la v5.8 (el rollback no era necesario) — no
  urgente, mejor estabilizar primero.
- Seguir updates con la cadencia de SEV1.

**Post-mortem**: dos causas coincidentes (deploy + proveedor) confundieron
el diagnóstico; action items: alerta específica por dependencia externa,
dashboard de latencia por proveedor, failover automático de proveedor de pagos.
</details>

### H2. Disco lleno en la base de datos

**Situación:** 03:10. Alerta: *"orders-db: free storage < 5%"*. Unos minutos
después: *"orders-api error rate 12%"*.

<details><summary>▶ Etapa 1 — ¿Qué hacés?</summary>

Ack → confirmar → alcance (pedidos fallan = dinero) → **SEV1 / SEV2** →
declarar. La relación es clara: DB sin espacio → escrituras fallan.

**Mitigación inmediata**: **ampliar el almacenamiento** (en servicios
gestionados como RDS / Azure SQL / Cloud SQL suele poder hacerse en caliente;
habilitar storage autoscaling si existe).

**Revelación:** ampliaste, los errores bajan. El espacio había crecido 40%
en las últimas 3 horas.
</details>

<details><summary>▶ Etapa 2 — Diagnóstico: ¿qué causa un crecimiento así?</summary>

Hipótesis: logs / binlogs / WAL acumulándose (réplica caída o slot de
replicación trabado), tabla temporal o job batch que genera datos masivos,
bucle de inserciones por un bug, backups locales, índices nuevos.
Verificar: qué tablas / archivos crecieron, jobs que arrancaron hace ~3 h,
deploys recientes.

**Revelación:** un job nuevo de auditoría, desplegado esa tarde, inserta una
fila por cada lectura de pedido.
</details>

<details><summary>▶ Etapa 3 — Resolución y post-mortem</summary>

- Pausar el job (feature flag / scale a 0 del cronjob) — mitigación definitiva del crecimiento.
- L3: rediseñar el job (muestreo, otro storage como un data lake, retención).
- Limpiar los datos generados (con cuidado, tras validar con el dueño).
- Action items: **alertas por tasa de crecimiento** (no solo por umbral
  fijo), storage autoscaling, revisión de impacto en DB para jobs nuevos,
  política de retención.
</details>

### H3. Intermitencia sin cambios aparentes

**Situación:** soporte reporta que *"a veces"* la app tarda 30 segundos o da
error. Error rate global: 2% (normal: 0,1%). Nadie desplegó nada hoy.

<details><summary>▶ Etapa 1 — ¿Cómo encarás algo intermitente?</summary>

- Severidad: degradación parcial → **SEV2** (subir si crece).
- **Acotar**: ¿qué tienen en común los requests que fallan? Agrupar errores
  por endpoint, región, **pod / nodo / zona**, cliente, versión de la app.
  La intermitencia casi siempre es "una parte del sistema está mal".
- "¿Qué cambió?" más amplio: infraestructura, proveedor, tráfico, tiempo.

**Revelación:** todos los errores vienen de pods corriendo en **un mismo nodo**.
</details>

<details><summary>▶ Etapa 2 — ¿Qué hacés?</summary>

- **Mitigar**: `kubectl cordon <nodo>` + `kubectl drain <nodo>` → los pods se
  reprograman en nodos sanos. El error rate debería volver a lo normal.
- Antes del drain (o en paralelo), juntar evidencia del nodo: `kubectl
  describe node` (conditions: MemoryPressure, DiskPressure,
  NetworkUnavailable), métricas del nodo, logs del kubelet.
- Diagnóstico posterior: hardware / VM degradada (status del proveedor),
  red del nodo, disco, kernel.
- Action items: alerta por error rate **por nodo**, node problem detector,
  reemplazo automático de nodos no saludables.
</details>

### H4. Fuga de credenciales (incidente de seguridad)

**Situación:** GitHub secret scanning avisa que una **access key de AWS** se
publicó en un repo público hace 2 horas.

<details><summary>▶ Etapa 1 — ¿Qué hacés? (ojo, el orden cambia)</summary>

Un incidente de **seguridad** cambia las prioridades: **contener** y
**preservar evidencia**, sin borrar rastros.
1. **SEV1 de seguridad**; involucrar al equipo de seguridad (no resolverlo solo).
2. **Desactivar / rotar la credencial de inmediato** (desactivar la access
   key en IAM; crear una nueva y actualizar a los consumidores legítimos).
3. Revisar en **CloudTrail** qué se hizo con esa key desde que se filtró
   (creación de recursos, lectura de S3, nuevos usuarios IAM, minería).
4. Eliminar el secreto del repo **y del historial** (pero la credencial ya se
   considera comprometida aunque se borre).

**Revelación:** CloudTrail muestra que alguien creó 30 instancias EC2 GPU en otra región.
</details>

<details><summary>▶ Etapa 2 — ¿Y ahora?</summary>

- Contener: **detener** (no borrar todavía si seguridad quiere evidencia
  forense; snapshot) las instancias; buscar **persistencia** (usuarios IAM,
  roles, access keys nuevas, Lambdas) y eliminarla.
- Contactar a **AWS Support** (L4) — por costos y por el abuso.
- Evaluar si hubo **acceso a datos** (obligaciones legales de notificación).
- Post-mortem: cómo llegó la key al código; action items: **sin access keys
  de larga duración** (OIDC / roles / Managed Identity), pre-commit hooks y
  secret scanning en CI (shift-left), SCP para limitar regiones, alertas de
  costo / anomalías.
</details>

### H5. Todo se cae a la vez: DNS

**Situación:** 10:00. Alertas de **muchos servicios distintos** a la vez:
timeouts y errores de conexión. Los pods están `Running`, CPU normal.

<details><summary>▶ Etapa 1 — ¿Qué te dice que fallen muchos servicios a la vez?</summary>

Cuando muchas cosas fallan juntas, buscar el **componente compartido**:
DNS, red (VPC, NAT, firewall), service mesh / ingress, proveedor de
identidad / auth, una dependencia común (DB, cache, cola), o el proveedor
cloud. Declarar **SEV1**, un IC único (no un incidente por servicio).

**Revelación:** los logs muestran `no such host` / `i/o timeout` al resolver nombres internos.
</details>

<details><summary>▶ Etapa 2 — ¿Qué hacés?</summary>

- Verificar **DNS del cluster**: `kubectl get pods -n kube-system -l k8s-app=kube-dns`
  (CoreDNS), sus logs y consumo; probar resolución desde un pod (`nslookup`).
- "¿Qué cambió?": cambios en CoreDNS / ConfigMap, zona DNS privada, reglas de red.
- **Mitigar**: escalar CoreDNS / revertir el cambio de config / reiniciar los
  pods de CoreDNS si están saturados o colgados.
- Action items: autoscaling de CoreDNS, NodeLocal DNSCache, alertas de
  latencia / errores de DNS, cambios de DNS por pipeline con revisión.
</details>

### H6. Escalamiento desde L1 con poca información

**Situación:** te llega un ticket de L1: *"El cliente ACME dice que la API no
anda. Prioridad alta."* Nada más.

<details><summary>▶ ¿Qué hacés?</summary>

- No asumir. **Completar el triage** que faltó: ¿qué endpoint?, ¿qué error
  (código HTTP, mensaje)?, ¿desde cuándo?, ¿todos sus requests o algunos?,
  request ID / timestamp de un ejemplo.
- Mientras tanto, mirar **por tu cuenta**: dashboards filtrados por ese
  cliente (tenant ID / API key), logs de errores de ese cliente, estado general de la API.
- Si solo afecta a ACME: probable config / credenciales / cuota / rate limit
  de ese cliente, o un cambio del lado de ellos.
- Si afecta a más clientes: subir severidad y declarar incidente.
- Feedback a L1 (sin culpar): qué datos incluir en el próximo escalamiento → mejorar la plantilla de handoff.
</details>

---

## I. Preguntas de criterio (trampas de entrevista)

**I1. "¿Qué hacés si el rollback falla?"**
<details><summary>▶ Respuesta esperada</summary>

No insistir a ciegas. Ver por qué falló (pipeline, imagen vieja borrada del
registry, migración incompatible). Alternativas: desplegar el artefacto
anterior manualmente, **roll-forward** con hotfix mínimo, mitigaciones que
no requieren deploy (feature flag, failover, desviar tráfico). Escalar a L3 y
anotarlo: **"rollback no probado"** es un action item del post-mortem.
</details>

**I2. "El dueño del servicio no responde y la única mitigación es una acción riesgosa en su sistema. ¿Qué hacés?"**
<details><summary>▶ Respuesta esperada</summary>

Seguir la **escalation policy** (secundario, manager del equipo). Si nadie
responde y el impacto lo justifica, el **IC** decide; documentar la decisión
y su razón en la timeline; preferir la opción **más reversible**; pedir una
segunda opinión si es posible. Nunca acciones irreversibles (borrar datos,
inactivar recursos productivos) sin aprobación explícita.
</details>

**I3. "Encontraste la causa raíz a los 5 minutos: un bug en el código. El fix es de una línea. ¿Lo desplegás directo a producción?"**
<details><summary>▶ Respuesta esperada</summary>

No directo sin control. Si existe una mitigación más segura (rollback,
feature flag), **primero esa**. El fix va por el pipeline normal (o de
hotfix) con revisión de otra persona, tests y despliegue **canary**. Un
"fix de una línea" bajo presión es una fuente clásica de un segundo incidente.
</details>

**I4. "¿Qué hacés si te equivocás durante el incidente y empeorás las cosas?"**
<details><summary>▶ Respuesta esperada</summary>

Decirlo **inmediatamente** en el canal, revertir tu acción si es posible, y
anotarlo en la timeline con hora. La transparencia es clave en una cultura
blameless; esconderlo hace que el equipo diagnostique un problema que no entiende.
</details>

**I5. "¿Cómo reducirías la cantidad de escalamientos de L1 a L2?"**
<details><summary>▶ Respuesta esperada</summary>

Analizar los escalamientos más frecuentes y para cada uno: **runbook** claro
para L1, **automatizar** la remediación (auto-remediation, self-healing),
mejorar la observabilidad que tiene L1, darle a L1 los permisos mínimos
necesarios, y eliminar la causa raíz de los problemas recurrentes (reducir **toil**).
</details>

**I6. "Contame un incidente real que hayas manejado."** (pregunta comportamental)
<details><summary>▶ Estructura esperada</summary>

Usar **STAR** + las fases:
- **S**ituación: qué sistema, qué impacto, severidad.
- **T**area: tu rol (on-call, IC, L2, L3).
- **A**cción: cómo clasificaste, qué mitigaste, cómo diagnosticaste, a quién escalaste, cómo comunicaste.
- **R**esultado: tiempo de resolución, impacto evitado, y **qué cambió después** (action items del post-mortem).

Prepará 2 historias propias (ej. de MercadoLibre) con este formato antes de la entrevista.
</details>
