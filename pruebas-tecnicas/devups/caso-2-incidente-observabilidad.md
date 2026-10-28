# Caso 2 — Incidente productivo y observabilidad (DevUps)

## Enunciado

API productiva en **ECS (Elastic Container Service) Fargate** detrás de un **ALB (Application Load
Balancer)**, con **Aurora** como base de datos. Hay **CloudWatch** y **AWS X-Ray**.

| | Normal | Durante el incidente |
|---|---|---|
| Latencia promedio | 200 ms | **3 s** + usuarios con timeouts |
| CPU de los containers | 35% | sin cambio significativo |
| Memoria | 50% | sin cambio significativo |
| AWS X-Ray | — | **~80% del tiempo de cada request esperando a Aurora** |

Se pide: cómo gestionar el incidente desde la alerta — información inicial, métricas y logs, hipótesis,
análisis de Aurora, mitigación rápida, momento del RCA (Root Cause Analysis, análisis de causa raíz) y
medidas posteriores.

---

## 0. Panorama: qué dicen los síntomas

- **CPU y memoria de los containers normales + latencia alta** → la aplicación **no está trabajando
  más, está esperando**. El cuello de botella no está en ECS.
- **AWS X-Ray dice que el 80% del tiempo es Aurora** → el problema está en la base de datos **o en el
  camino hacia ella** (pool de conexiones, red, locks).
- Conclusión inmediata y clave: **escalar ECS no arregla nada y puede empeorarlo** (más tareas = más
  conexiones y más queries contra una Aurora ya saturada).

El orden de trabajo de un incidente: **detectar → coordinar → mitigar → estabilizar → RCA →
prevenir**. Primero se **devuelve el servicio**, después se entiende por qué falló.

## 1. Desde que llega la alerta (primeros 5 minutos)

1. **Reconocer la alerta** (ack) para que el equipo sepa que alguien la tiene.
2. **Evaluar impacto y declarar severidad** (ej.: SEV-1/SEV-2): ¿cuántos usuarios?, ¿todos los
   endpoints o algunos?, ¿flujos críticos (pagos, login)?
3. **Roles**: Incident Commander (coordina y decide), responsable técnico, responsable de
   comunicación. Canal de incidente dedicado (Slack/Teams) y actualización a la **status page** /
   negocio cada 15-30 min.
4. **Bitácora con hora** de cada hallazgo y acción → será la línea de tiempo del postmortem.

## 2. Información que revisaría inicialmente

- **¿Qué cambió?** — la pregunta que resuelve la mayoría de incidentes:
  - Despliegues recientes de ECS (nueva task definition), **migraciones de base de datos**, cambios de
    Terraform, cambios de parámetros de Aurora.
  - **AWS CloudTrail** para cambios de infraestructura; historial del pipeline de CI/CD.
  - **Eventos de RDS** (failover, reinicio, mantenimiento, cambio de instancia).
- **¿Cuándo empezó exactamente?** y si coincide con un deploy, un job programado (batch, reporte,
  backup) o un pico de tráfico.
- **¿Alcance?**: todos los endpoints o uno; todas las tareas o algunas; todas las AZ (Availability
  Zones) o una.

## 3. Métricas y logs

**ALB (CloudWatch)**:

- `TargetResponseTime` en **percentiles p50 / p95 / p99**, no solo el promedio (el promedio de 3 s
  puede esconder un p99 de 30 s = los timeouts).
- `HTTPCode_Target_5XX_Count`, `HTTPCode_ELB_5XX_Count` (los **504** son timeouts),
  `RequestCount` (¿hay más tráfico de lo normal?), `TargetConnectionErrorCount`.

**ECS**:

- CPU y memoria (ya sabemos que normales), `RunningTaskCount`, reinicios de tareas, health checks
  fallando.

**Aurora (CloudWatch + Performance Insights / CloudWatch Database Insights)**:

- `DBLoad` (sesiones activas promedio) vs. número de vCPU de la instancia.
- `CPUUtilization`, `FreeableMemory`, `DatabaseConnections` vs. `max_connections`.
- `ReadLatency`, `WriteLatency`, `CommitLatency`, `DiskQueueDepth`, `ReadIOPS`/`WriteIOPS`.
- `BufferCacheHitRatio` (si cae, se está leyendo de disco), `Deadlocks`, `AuroraReplicaLag`.

**AWS X-Ray**:

- **Service map** y **traces** de las requests lentas: ¿qué query/segmento SQL consume el tiempo?,
  ¿todas las rutas o una sola?, ¿el tiempo es de la query o de **esperar una conexión** del pool?

**Logs (CloudWatch Logs Insights)**:

- Logs de la aplicación: `timeout`, `connection pool exhausted`, `too many connections`,
  `deadlock`, `lock wait timeout`, reintentos.
- Logs de Aurora exportados a CloudWatch: **slow query log**, error log
  (PostgreSQL: `log_min_duration_statement`, `log_lock_waits`).

## 4. Hipótesis (de más a menos probable)

1. **Query lenta / regresión de plan**: un deploy introdujo una query sin índice, el plan de ejecución
   cambió (estadísticas desactualizadas, crecimiento de datos) → full table scans.
2. **Bloqueos (locks)**: una transacción larga, una **migración DDL (Data Definition Language)** que
   bloquea una tabla (`ALTER TABLE`), o contención sobre las mismas filas → las demás queries esperan.
3. **Agotamiento del pool de conexiones**: las queries lentas retienen conexiones, el pool de la app se
   llena y las nuevas requests **esperan una conexión** (X-Ray lo cuenta como tiempo de base de datos).
   O se llegó a `max_connections` de Aurora.
4. **Saturación de la instancia de Aurora**: CPU, memoria (buffer cache), IOPS — por ejemplo, un
   **job batch o reporte** pesado corriendo sobre el writer.
5. **Más tráfico o *retry storm***: los clientes reintentan por los timeouts y multiplican la carga.
6. **Evento de infraestructura**: failover de Aurora, mantenimiento, instancia degradada,
   autovacuum/bloat (PostgreSQL), backups.

## 5. Qué analizaría específicamente en Aurora

- **Performance Insights / Database Insights**: `DBLoad` desglosado por **wait events** — dice *en
  qué* espera la base:
  - `CPU` → queries costosas; `IO:DataFileRead` → lecturas de disco (falta índice o cache);
  - `Lock:transactionid` / `Lock:tuple` (PostgreSQL) o `synch/...innodb` / `row_lock_wait` (MySQL) →
    bloqueos; `Client:ClientRead` → la aplicación tiene transacciones abiertas sin avanzar.
- **Top SQL** por carga: la query (o las pocas queries) que concentran el tiempo.
- **Sesiones y bloqueos en vivo**:
  - PostgreSQL: `pg_stat_activity` (queries activas, duración, `wait_event`), `pg_locks` +
    `pg_blocking_pids()` para encontrar **quién bloquea a quién**, `pg_stat_statements`.
  - MySQL: `SHOW PROCESSLIST`, `SHOW ENGINE INNODB STATUS`, `performance_schema`,
    `information_schema.innodb_trx`.
- **`EXPLAIN` / `EXPLAIN ANALYZE`** de las queries top para ver el plan (seq scan vs. index scan).
- Conexiones: cuántas, de qué host/usuario, cuántas en `idle in transaction`.
- **Eventos de RDS** y parámetros cambiados recientemente.
- Si hay **réplicas de lectura**: lag y si las lecturas están yendo al writer por error.

**Preservar evidencia**: guardar capturas de `pg_stat_activity`/locks y de Performance Insights
**antes** de matar sesiones o reiniciar — sin eso, el RCA queda a ciegas.

## 6. Acciones para reducir rápido el impacto (mitigación)

Primero lo **reversible y de menor riesgo**:

- **Rollback** del último deploy o migración si coincide con el inicio del incidente (ECS: volver a la
  task definition anterior).
- **Matar la sesión que bloquea** o la query desbocada (`pg_terminate_backend(pid)` / `KILL`).
- **Detener el job batch/reporte** que está saturando el writer, o moverlo a una réplica.
- **Feature flag**: apagar la funcionalidad que genera la query pesada.
- **Proteger la base**: reducir concurrencia (tamaño del pool), **rate limiting / load shedding** en el
  borde (AWS WAF, API Gateway si existe), y frenar los reintentos agresivos.
- **Escalar Aurora**: crear una instancia más grande y hacer failover hacia ella (escalado vertical
  ~minutos), o agregar **réplicas de lectura** si la app ya separa lecturas.
- **NO escalar ECS** hacia afuera: más tareas = más conexiones = peor.

Comunicar cada acción y su efecto en el canal del incidente; confirmar la recuperación con la latencia
**p99** y la tasa de errores volviendo a la línea base, no solo con "parece que ya".

## 7. ¿Cuándo hacer el RCA?

- **Durante el incidente**: solo el diagnóstico necesario para **mitigar** + preservar evidencia. No se
  busca la causa raíz profunda mientras los usuarios están afectados.
- **Después de estabilizar** (servicio en línea base y monitoreado un tiempo): **postmortem blameless**
  (sin culpables) en las siguientes 24-72 horas, con:
  - línea de tiempo (de la bitácora), impacto (usuarios, minutos, error budget consumido),
  - causa raíz con técnicas como **5 Whys** (5 porqués): ¿por qué la query fue lenta? → faltaba índice →
    ¿por qué llegó a producción? → no había revisión de planes ni prueba de carga → ...,
  - qué funcionó y qué no en la respuesta,
  - **acciones con dueño y fecha**.

## 8. Medidas después del incidente (prevención)

**Detección (observabilidad)**:

- Alertas sobre **percentiles (p99)** y tasa de errores, idealmente **SLO (Service Level Objective)
  con burn rate**, no sobre promedios.
- Alarmas sobre `DBLoad` > vCPU, `DatabaseConnections` cerca del máximo, `Deadlocks`, slow queries.
- **Performance Insights** habilitado con retención suficiente, slow query log exportado a
  CloudWatch Logs, dashboards app + ALB + Aurora en una sola vista.

**Resiliencia en la aplicación**:

- **Timeouts** en el cliente de base de datos (`statement_timeout`, `lock_timeout`) y en la app.
- **Circuit breaker** y **reintentos con backoff exponencial + jitter** (evitar retry storms).
- Pool de conexiones bien dimensionado y **Amazon RDS Proxy** para multiplexar conexiones y
  absorber picos.
- **Caché** (Amazon ElastiCache) para lecturas repetidas; separar lecturas hacia réplicas.

**Cambios seguros**:

- Revisión de queries y `EXPLAIN` en el code review; migraciones **online** (sin locks largos,
  índices `CONCURRENTLY`), con `lock_timeout`.
- **Despliegues progresivos** (canary / blue-green con ECS + CodeDeploy) con rollback automático
  por alarmas.
- **Pruebas de carga** con volúmenes de datos realistas antes de producción.
- Jobs batch fuera del writer (réplica) o en ventanas de baja carga.

**Proceso**:

- **Runbook** de "latencia alta por base de datos" con estos pasos, y practicarlo en GameDays.

---

## Resumen de 30 segundos (para decir en voz alta)

> "CPU y memoria normales con latencia alta me dicen que la app está **esperando**, y X-Ray confirma que
> espera a Aurora — así que **no escalo ECS**, eso solo suma conexiones. Reconozco la alerta, declaro
> severidad, abro canal y comunico. Primera pregunta: **¿qué cambió?** — deploys, migraciones, jobs.
> Reviso el ALB en **p99** y 5xx, y en Aurora uso **Performance Insights** para ver los **wait events** y
> el top SQL: locks, query sin índice, pool de conexiones agotado o instancia saturada. Mitigo con lo
> reversible: **rollback**, matar la sesión bloqueante, frenar el batch, feature flag, escalar Aurora.
> Preservo evidencia y hago el **postmortem blameless** cuando el servicio está estable. Después: alertas
> por percentiles y SLO, timeouts, circuit breakers, **RDS Proxy**, migraciones online y despliegues
> canary."
