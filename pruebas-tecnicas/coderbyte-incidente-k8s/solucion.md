# Caso: incidente de confiabilidad y observabilidad en Kubernetes

**Escenario (resumen):** aplicación crítica en Kubernetes. En los últimos 30 minutos la latencia p95
pasó de 250 ms a 2,8 s y los errores HTTP 5xx del 0,2 % al 7 %. Dos pods se reinician con eventos
`OOMKilled`, la memoria de la aplicación crece de forma progresiva y la CPU (Central Processing Unit)
de los nodos está moderada. Dynatrace alerta latencia, Splunk muestra errores intermitentes y todavía
nadie los ha correlacionado. Todo empezó después de un despliegue hecho con Jenkins. SLO (Service
Level Objective) de disponibilidad: 99,9 %. El Error Budget se está consumiendo rápido.

---

## 0. Hipótesis inicial y cadena causal (diagrama en texto)

La evidencia apunta a una **fuga de memoria (memory leak)** o a un **límite de memoria mal
dimensionado** que llegó con el despliegue de Jenkins:

```text
Despliegue Jenkins (versión N+1)
        │
        ▼
Memoria del contenedor sube sin parar  ──►  GC (Garbage Collector) trabaja más ──► latencia sube
        │
        ▼
Llega al limit de memoria del contenedor (cgroup)
        │
        ▼
Kernel mata el proceso: OOMKilled (exit code 137) ──► el pod se reinicia (CrashLoopBackOff si se repite)
        │
        ├──► las peticiones en curso de ese pod se pierden ──► 5xx (502/503 desde el Ingress)
        └──► quedan menos pods Ready ──► los pods sanos reciben más carga ──► p95 sube a 2,8 s
```

**Por qué la CPU moderada no descarta nada:** `OOMKilled` es un límite **del contenedor**, no del
nodo. Un nodo puede tener CPU y memoria libres y, aun así, el contenedor muere por pasar su
`resources.limits.memory`. Si fuera presión del nodo veríamos pods `Evicted` y la condición
`MemoryPressure` en el nodo, no `OOMKilled`.

---

## 1. Primeros 15 minutos: estabilizar y limitar el impacto

Objetivo: **primero restaurar el servicio, después la causa raíz.** Antes de tocar nada se guarda la
evidencia, porque un rollback o un reinicio la borra (logs de los pods, estado de los contenedores).

| Minuto | Acción | Para qué |
|---|---|---|
| 0–2 | Declarar el incidente (severidad alta, servicio crítico con SLO en riesgo), nombrar un **Incident Commander** y abrir un canal único del incidente. | Una sola persona decide y un solo lugar para la información. |
| 0–2 | **Congelar despliegues** en Jenkins para este servicio (desactivar el job o activar un *deploy freeze*). | Que nadie meta otro cambio encima del problema. |
| 2–5 | Confirmar el alcance: ¿solo este servicio o también otros? ¿Todas las rutas o algunas? ¿Todos los pods o solo los de la versión nueva? (Dynatrace: service flow y pods afectados.) | Saber si el problema es del despliegue o de una dependencia compartida. |
| 2–5 | Confirmar la correlación con el despliegue: hora del build de Jenkins vs. hora en que empezó a subir la memoria/latencia (`kubectl rollout history`, historial del job). | Es la base para decidir el rollback. |
| 5–8 | **Guardar evidencia**: `kubectl describe` de los pods afectados, `kubectl logs --previous`, eventos del namespace y, si se puede, un *heap dump* de un pod que esté cerca del límite. | Que el rollback no nos deje sin datos para el postmortem. |
| 8–12 | **Mitigar**: si se cumplen los criterios de la sección 4, **rollback** a la versión anterior. Mientras se ejecuta, se puede ganar tiempo escalando réplicas (`kubectl scale`) para repartir la carga. | Cortar el consumo del Error Budget. |
| 12–15 | Verificar la recuperación: p95 baja hacia 250 ms, 5xx hacia 0,2 %, cero reinicios nuevos y memoria plana. Enviar el primer comunicado a stakeholders (impacto, acción tomada, próxima actualización en 15–30 min). | Cerrar la fase de contención con datos, no con intuición. |

**Mitigaciones temporales, solo si el rollback no se puede hacer de inmediato:**

- Escalar réplicas: `kubectl scale deploy/mi-app -n prod --replicas=<actual x 2>`. Con una fuga de
  memoria esto solo compra tiempo, porque cada pod nuevo también va a crecer hasta morir.
- Subir temporalmente `limits.memory`: alarga el tiempo entre OOMKilled, pero no arregla la fuga.
  Cualquier cambio en caliente se registra en el canal y se lleva al código (Jenkins/Git) después.

---

## 2. Comandos, eventos y métricas en Kubernetes y Linux

### 2.1 Kubernetes

```bash
NS=prod; APP=mi-app

# Estado de los pods: reinicios, nodo donde corre cada uno, edad
kubectl get pods -n $NS -l app=$APP -o wide

# Último estado del contenedor: buscar "Last State: Terminated, Reason: OOMKilled, Exit Code: 137"
kubectl describe pod <pod> -n $NS

# Eventos ordenados por tiempo: OOMKilled, BackOff, Unhealthy (probes fallando), Killing
kubectl get events -n $NS --sort-by=.lastTimestamp | tail -40

# Logs del contenedor ANTERIOR (el que murió), que es donde está el error real
kubectl logs <pod> -n $NS --previous --tail=200

# Consumo real vs. lo configurado (requiere metrics-server)
kubectl top pods -n $NS -l app=$APP --containers
kubectl get deploy $APP -n $NS -o jsonpath='{.spec.template.spec.containers[*].resources}'

# ¿Qué cambió en el despliegue? (imagen, limits, variables, flags de la JVM, etc.)
kubectl rollout history deploy/$APP -n $NS
kubectl rollout history deploy/$APP -n $NS --revision=<N>     # comparar N vs. N-1

# Cuántos pods están realmente recibiendo tráfico (Ready)
kubectl get endpointslices -n $NS -l kubernetes.io/service-name=$APP

# Autoscaling: ¿el HPA (Horizontal Pod Autoscaler) intenta escalar?
kubectl get hpa -n $NS

# Nodos: descartar presión del nodo (MemoryPressure) y ver memoria asignada
kubectl top nodes
kubectl describe node <nodo> | grep -A8 -E "Conditions|Allocated resources"
```

**Qué busco con estos comandos:**

- `Reason: OOMKilled` + `Exit Code: 137` → el contenedor pasó su límite de memoria.
- Reinicios solo en los pods de la **revisión nueva** → el problema viaja con el despliegue.
- `kubectl rollout history` muestra un cambio de imagen, de `limits.memory` o de una variable de
  memoria (por ejemplo, `-Xmx` o `-XX:MaxRAMPercentage` en una JVM, Java Virtual Machine).
- Pocos endpoints Ready → explica por qué los pods sanos se saturan y sube la latencia.

### 2.2 Linux (en el nodo)

```bash
# Entrar al nodo sin SSH (Secure Shell): pod de debug con el filesystem del nodo en /host
kubectl debug node/<nodo> -it --image=busybox -- chroot /host sh

# Mensajes del kernel sobre el OOM killer: qué proceso mató y cuánta memoria tenía
dmesg -T | grep -i -E "oom|killed process"
journalctl -k --since "40 min ago" | grep -i oom

# Memoria del nodo en general (para descartar que sea el nodo)
free -m
top -o %MEM            # o: ps aux --sort=-rss | head

# cgroup v2 del contenedor: memoria actual, límite y contador de OOM kills
cat /sys/fs/cgroup/kubepods.slice/.../memory.current
cat /sys/fs/cgroup/kubepods.slice/.../memory.max
cat /sys/fs/cgroup/kubepods.slice/.../memory.events     # campo oom_kill
```

### 2.3 Métricas clave

| Métrica | Qué confirma |
|---|---|
| Memoria working set del contenedor vs. `limits.memory` | Si la curva sube en "diente de sierra" (crece → OOM → reinicio → crece), es fuga de memoria. |
| Reinicios por pod y por versión | Si solo reinicia la versión nueva. |
| Pausas/tiempo de GC (Garbage Collector) | Si la latencia sube **antes** del OOM (el GC trabaja cada vez más). |
| Latencia p95 y tasa de 5xx por pod y por versión | Si la degradación se concentra en los pods nuevos. |
| Pods Ready / endpoints | Si la capacidad real bajó por los reinicios. |
| CPU del nodo, `MemoryPressure`, evictions | Descartar que el problema sea del nodo. |

---

## 3. Correlación entre Dynatrace, Splunk y OpenTelemetry

La idea es armar **una sola línea de tiempo** con las tres fuentes y usar **llaves comunes** para
saltar entre ellas: hora, nombre del pod, versión desplegada y `trace_id`.

### 3.1 Línea de tiempo (lo que espero ver si la hipótesis es correcta)

```text
T0        Jenkins despliega la versión N+1           (Jenkins / kubectl rollout history)
T0+5m     La memoria de los pods nuevos empieza a subir   (Dynatrace: métrica de memoria del proceso/contenedor)
T0+15m    La latencia p95 sube (más GC)               (Dynatrace: alerta de latencia)
T0+20m    Primer OOMKilled y reinicio                 (Kubernetes events / dmesg)
T0+20m    Picos de 5xx justo en los segundos del reinicio  (Splunk: logs del Ingress y de la app)
```

Si los picos de 5xx de Splunk caen en los mismos minutos de los OOMKilled, y la memoria creciente solo
aparece en la versión N+1, la hipótesis queda bien sustentada.

### 3.2 Dynatrace

- **Problem / Davis AI:** revisar qué entidades agrupa el problema (servicio, proceso, pods) y la
  causa raíz que propone.
- **Evento de despliegue:** ver si el despliegue de Jenkins aparece en la línea de tiempo del
  servicio. Si no aparece, es una acción preventiva (sección 5).
- **Memoria del proceso** de los pods nuevos vs. los viejos; en Java, el *memory profiling* y las
  métricas de GC.
- **PurePath / distributed traces:** abrir trazas lentas y ver dónde se va el tiempo (código propio,
  base de datos, llamadas externas).

Ejemplo de métricas a graficar (selector de métricas):

```text
builtin:service.response.time:percentile(95)       # p95 del servicio
builtin:service.errors.server.rate                 # tasa de errores 5xx
builtin:containers.memory.residentSetBytes         # memoria del contenedor
```

### 3.3 Splunk (SPL, Search Processing Language)

```spl
# 1) Errores por minuto y por pod: ¿se concentran en algunos pods?
index=k8s namespace=prod app=mi-app (status>=500 OR level=ERROR)
| timechart span=1m count by pod

# 2) Errores más frecuentes, separados por versión
index=k8s namespace=prod app=mi-app level=ERROR
| stats count by version, error_message
| sort -count

# 3) OOM del kernel en los nodos (si se envían los logs de sistema a Splunk)
index=linux sourcetype=syslog ("Out of memory" OR "oom-kill" OR "Killed process")
| table _time host _raw
```

### 3.4 OpenTelemetry (si está disponible)

- Que los logs lleven el **`trace_id`** y el **`span_id`** de OpenTelemetry. Así, desde una traza
  lenta en Dynatrace (que puede recibir trazas por OTLP, OpenTelemetry Protocol) se busca el mismo
  `trace_id` en Splunk y se ven los logs exactos de esa petición.
- Usar los atributos de recurso de OpenTelemetry para **segmentar**: `service.version`,
  `k8s.pod.name`, `k8s.deployment.name`, `deployment.environment`. Comparar latencia y errores entre
  `service.version = N` y `service.version = N+1` es la prueba más directa contra el despliegue.

```spl
index=k8s trace_id="<trace_id de la traza lenta en Dynatrace>"
| table _time pod version level message
```

### 3.5 Pseudocódigo de la correlación

```text
t_deploy  = hora del build de Jenkins que llegó a producción
pods_new  = pods con la versión N+1
pods_old  = pods con la versión N (si quedan)

para cada pod:
    curva_memoria = memoria(pod) desde t_deploy
    oom_times     = eventos OOMKilled(pod)
    errores_5xx   = errores por minuto(pod) en Splunk

si curva_memoria(pods_new) crece de forma lineal y curva_memoria(pods_old) es plana
   y los picos de errores_5xx coinciden con oom_times
   y el inicio de la degradación es posterior a t_deploy
entonces hipótesis = "fuga de memoria / límite mal dimensionado en la versión N+1"
si no:
    revisar dependencias (base de datos, servicios externos) y cambios de infraestructura en la misma ventana
```

---

## 4. Criterios para decidir el rollback

**Regla general:** si el problema empezó con el despliegue y el rollback es seguro, se hace rollback
**primero** y se investiga después con la evidencia ya guardada. No hace falta tener la causa raíz
confirmada para volver a una versión que sabemos que funciona.

| Criterio | ¿Favorece el rollback? |
|---|---|
| La degradación empezó **después** del despliegue de Jenkins (correlación en la línea de tiempo). | Sí |
| Los síntomas (memoria, reinicios, errores) se concentran en los pods de la **versión nueva**. | Sí |
| El impacto es alto: 7 % de 5xx contra un SLO de 99,9 % es un **burn rate** de unas 70x (cálculo abajo). | Sí, es urgente |
| No hay un arreglo rápido y seguro (por ejemplo, apagar una *feature flag*) en menos de 10–15 minutos. | Sí |
| El rollback es **seguro**: no hay migraciones de base de datos irreversibles ni cambios de esquema incompatibles con la versión anterior. | Condición necesaria |
| El problema empezó **antes** del despliegue, o afecta también a servicios que no se desplegaron. | No: buscar en dependencias o infraestructura |
| La versión nueva tiene una migración irreversible. | No: *roll forward* (hotfix) o *feature flag* |

**Cálculo del Error Budget:**

- 99,9 % en 30 días → 0,1 % de 43.200 minutos = **43,2 minutos** de "error total" al mes.
- Burn rate actual = 7 % / 0,1 % = **70x**. A ese ritmo, el presupuesto del mes entero se acaba en
  unas **10 horas**.
- 30 minutos con 7 % de errores ≈ 30 × 0,07 = 2,1 minutos de error total ≈ **5 % del Error Budget
  mensual** (es una cota superior, porque los errores subieron de forma progresiva).

**Cómo ejecutar el rollback:**

1. Preferido: volver a ejecutar el pipeline de Jenkins con el **tag/digest de la imagen anterior**. Así
   queda registrado y el estado de Jenkins/Git sigue siendo la fuente de verdad.
2. Plan B (break-glass): `kubectl rollout undo deploy/mi-app -n prod` y
   `kubectl rollout status deploy/mi-app -n prod`. Luego se alinea Jenkins/Git para que el próximo
   despliegue no vuelva a meter la versión con el problema.
3. Verificar: memoria plana, cero OOMKilled nuevos, p95 y 5xx de vuelta a la línea base.

---

## 5. Acciones correctivas y preventivas (después del incidente)

### 5.1 Correctivas (arreglar esta causa)

- Encontrar la fuga con el *heap dump* o el *memory profiling* de Dynatrace sobre la versión N+1 en un
  ambiente de pruebas (por ejemplo: caché sin límite, conexiones que no se cierran, listas que crecen).
- Revisar `requests`/`limits` de memoria contra el consumo real (Dynatrace, o las recomendaciones del
  VPA, Vertical Pod Autoscaler, en modo solo recomendación). En la JVM, ajustar el heap al límite del
  contenedor (`-XX:MaxRAMPercentage`).
- Revisar las probes: que la `readinessProbe` saque al pod del balanceo antes de que colapse, y que
  la `livenessProbe` no reinicie pods solo por lentitud.

### 5.2 Preventivas: pipeline de Jenkins

- **Enviar un evento de despliegue a Dynatrace** desde Jenkins (Events API v2, tipo
  `CUSTOM_DEPLOYMENT`, con versión, build y commit). Así el próximo incidente ya trae la correlación
  con el despliegue hecha.
- **Canary o despliegue progresivo**: primero un porcentaje pequeño del tráfico, comparar memoria,
  latencia y errores contra la versión estable, y **rollback automático** si empeora.
- **Prueba de carga larga (soak test)** antes de producción: las fugas de memoria no se ven en una
  prueba de 5 minutos, se ven en una de 1–2 horas.
- Imágenes por **digest** o tags inmutables, para que el rollback siempre vuelva exactamente a lo
  mismo.

### 5.3 Alertas

| Alerta | Condición (ejemplo) | Tipo |
|---|---|---|
| Burn rate rápido del SLO | burn rate > 14,4x en 1 h **y** en 5 min (gasta 2 % del presupuesto en 1 hora) | Page (despertar a alguien) |
| Burn rate medio del SLO | burn rate > 6x en 6 h **y** en 30 min | Page |
| Burn rate lento del SLO | burn rate > 1x en 3 días **y** en 6 h | Ticket |
| Memoria cerca del límite | memoria del contenedor > 90 % de `limits.memory` durante 10 min | Ticket / aviso temprano |
| Tendencia de memoria | la memoria crece de forma sostenida después de un despliegue | Aviso al equipo dueño |
| Reinicios / OOMKilled | más de 3 reinicios en 15 minutos o cualquier OOMKilled en producción | Aviso |

Las ventanas dobles (larga + corta) del burn rate son el patrón de alertas **multi-window,
multi-burn-rate** del *SRE Workbook* de Google: la ventana larga evita falsas alarmas y la corta hace
que la alerta se apague rápido cuando el servicio se recupera.

### 5.4 Runbook "OOMKilled y latencia después de un despliegue"

```text
1. Confirmar síntomas: p95, 5xx, reinicios (Dynatrace + kubectl get pods)
2. Congelar despliegues en Jenkins
3. ¿Coincide con un despliegue? (evento de Dynatrace / kubectl rollout history)
4. Guardar evidencia: describe, logs --previous, events, heap dump
5. Si coincide y el rollback es seguro → rollback por Jenkins (plan B: kubectl rollout undo)
6. Verificar recuperación: memoria plana, 0 OOMKilled, p95 y 5xx en la línea base
7. Comunicar y registrar el consumo de Error Budget
8. Abrir el postmortem
```

### 5.5 Seguimiento del Error Budget y postmortem

- **Postmortem sin culpables (blameless)** en 48–72 horas: línea de tiempo, causa raíz, qué funcionó,
  qué no, y acciones con dueño y fecha.
- **Política de Error Budget**: si el consumo del mes pasa un umbral acordado (por ejemplo, 50 %), se
  frenan los despliegues de nuevas funcionalidades y el equipo prioriza confiabilidad hasta que el
  presupuesto se recupere.
- Tablero de SLO en Dynatrace con el presupuesto restante y el burn rate, revisado cada semana con el
  equipo dueño del servicio.
- Medir **MTTD** (Mean Time To Detect) y **MTTR** (Mean Time To Recover) de este incidente y de los
  siguientes, para comprobar que las alertas y el runbook realmente bajan esos tiempos.
