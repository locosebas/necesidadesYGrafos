# Banco de preguntas — Prueba Davivienda (SRE / Observabilidad)

Acompaña a [`roadmap-express.md`](roadmap-express.md). Cada pregunta lleva el código del ítem que evalúa.

**Cómo se usa:**
- En sesión se hacen **de a una**: respondes, se corrige esa respuesta y se pasa a la siguiente.
- Las marcadas **[Nombre]** describen un mecanismo y piden el nombre: no abras la respuesta antes de intentarlo.
- Las marcadas **[Mesa]** son del estilo de la ronda de 10 minutos de preguntas.
- La respuesta esperada está plegada en "Respuesta"; ábrela **solo después** de responder.

---

## Bloque A — SLOs, Error Budgets y Quality Gates

**A1.1** Si tuvieras que medir "qué tan bien funciona" el pago con QR de Banco Plus **desde el punto de vista del cliente**, no de los servidores, ¿qué medirías?
<details><summary>Respuesta</summary>

Indicadores centrados en el cliente: **disponibilidad** (proporción de pagos aceptados sin error de sistema), **latencia** (proporción de pagos confirmados en menos de X ms, medido en percentil, no en promedio), **corrección** (sin cobros dobles ni montos errados) y **frescura** (la notificación llega en menos de N segundos). Se miden lo más cerca posible del cliente: el balanceador de carga o API Gateway de entrada, o monitoreo sintético; no la CPU de un pod.
</details>

**A1.2** [Nombre] ¿Cómo se llama la *medida* (por ejemplo, "% de pagos exitosos"), cómo se llama la *meta interna* sobre esa medida ("99,9% en 30 días") y cómo se llama el *compromiso contractual con penalidad*?
<details><summary>Respuesta</summary>

**SLI** (Service Level Indicator) es la medida, **SLO** (Service Level Objective) es la meta interna y **SLA** (Service Level Agreement) es el contrato con penalidad. Regla: el SLA siempre es **más laxo** que el SLO, para que el equipo reaccione antes de incumplir el contrato. Fórmula típica del SLI: eventos buenos ÷ eventos válidos.
</details>

**A1.3** [Nombre] Hay cuatro señales que Google recomienda vigilar en todo servicio de cara al usuario. ¿Cómo se llaman en conjunto y cuáles son?
<details><summary>Respuesta</summary>

**Golden Signals**: **Latency** (latencia), **Traffic** (tráfico), **Errors** (errores) y **Saturation** (saturación). Vienen del libro *Site Reliability Engineering* de Google.
</details>

**A1.4** [Nombre] Un método resume la salud de un **servicio** con tasa de peticiones, errores y duración; otro resume la de un **recurso** (CPU, disco, cola) con utilización, saturación y errores. ¿Cómo se llama cada uno?
<details><summary>Respuesta</summary>

**RED** (Rate, Errors, Duration, de Tom Wilkie) para servicios y **USE** (Utilization, Saturation, Errors, de Brendan Gregg) para recursos. Las Golden Signals son prácticamente RED + saturación.
</details>

**A1.5** [Mesa] "¿Por qué no ponemos un SLO del 100% al pago QR, si es crítico?"
<details><summary>Respuesta</summary>

1. Es inalcanzable: el cliente depende de su red móvil, su celular y otros bancos, que no llegan al 100%.
2. Congela la innovación: cero presupuesto de errores significa cero despliegues con riesgo.
3. El costo crece exponencialmente con cada nueve.

El SLO correcto es el punto en el que el cliente **deja de notar** la diferencia, y se acuerda con negocio.
</details>

**A2.1** ¿Cuántos minutos de indisponibilidad al mes (30 días) permite un SLO de 99,9%? ¿Y de 99,95% y 99,99%?
<details><summary>Respuesta</summary>

30 días = 43.200 min. 99,9% → **43,2 min**; 99,95% → **21,6 min**; 99,99% → **4,32 min**; 99,5% → 3,6 h; 99% → 7,2 h.
</details>

**A2.2** [Nombre] La diferencia entre el 100% y el SLO, vista como "margen para fallar que el equipo puede gastar en lanzar cosas", ¿cómo se llama?
<details><summary>Respuesta</summary>

**Error Budget** (presupuesto de errores) = 1 − SLO. Con 99,9% es 0,1% de las peticiones válidas o 43,2 min/mes. Alinea a desarrollo y operaciones: mientras quede presupuesto se despliega rápido; si se agota, se prioriza la confiabilidad.
</details>

**A2.3** El pago QR depende en serie de 3 componentes, cada uno con 99,9% de disponibilidad. ¿Cuál es la disponibilidad máxima del pago? ¿Y si pones dos réplicas independientes de un componente de 99%?
<details><summary>Respuesta</summary>

En serie se multiplican: 0,999³ ≈ **99,7%**. Ningún servicio puede prometer más que el producto de sus dependencias críticas. En paralelo e independientes: 1 − (1 − 0,99)² = **99,99%**. Ese es el argumento para tener redundancia multi-zona o multi-cloud.
</details>

**A2.4** [Mesa] "¿Por qué una ventana de 28 o 30 días *móvil* y no el mes calendario?"
<details><summary>Respuesta</summary>

La ventana móvil no "resetea" el presupuesto el día 1. Un incidente grande pesa los 28/30 días siguientes, lo que evita gastar todo a fin de mes porque "igual se renueva". Se eligen 28 días para que todas las ventanas tengan los mismos días de semana.
</details>

**A3.1** [Nombre] Si la tasa de error actual consume el presupuesto 14,4 veces más rápido de lo que permite el SLO, ¿cómo se llama esa razón y cuánto dura el presupuesto mensual a ese ritmo?
<details><summary>Respuesta</summary>

**Burn rate** = tasa de error observada ÷ (1 − SLO). Con 14,4, el presupuesto de 30 días se agota en 30/14,4 ≈ **2,1 días**; en 1 hora se gasta el **2%** del presupuesto mensual.
</details>

**A3.2** ¿Por qué alertar por burn rate es mejor que alertar "si la tasa de error > 1%"? ¿Qué son las alertas multi-window, multi-burn-rate?
<details><summary>Respuesta</summary>

Un umbral fijo despierta a alguien por picos de 2 minutos que no ponen en riesgo el SLO, y no detecta fugas lentas. El burn rate liga la alerta al impacto real sobre el SLO. **Multi-window**: se exige que la ventana larga (1 h) y una corta (5 min) superen el umbral, para detectar rápido y dejar de alertar rápido cuando se arregla. **Multi-burn-rate** (SRE Workbook): 14,4× en 1 h → page; 6× en 6 h → page; 1× en 3 días → ticket.
</details>

**A4.1** [Nombre] ¿Cómo se llama el documento acordado con negocio que dice qué pasa cuando se agota el Error Budget (por ejemplo, congelar lanzamientos salvo arreglos de confiabilidad)?
<details><summary>Respuesta</summary>

**Error Budget Policy**. Sin esta política firmada por negocio, el Error Budget es solo un número en un dashboard. Es lo que le da dientes al Quality Gate.
</details>

**A4.2** Describe paso a paso un Quality Gate en GitHub Actions que detenga el despliegue del servicio de pagos si el Error Budget está crítico.
<details><summary>Respuesta</summary>

1. El pipeline llega al job de despliegue a producción.
2. Un paso previo consulta la fuente de SLOs (API de Prometheus con reglas generadas por **Sloth**/**Pyrra**, o la API de Datadog/Dynatrace) y obtiene el presupuesto restante y el burn rate.
3. Si el presupuesto restante es menor que X% o el burn rate es mayor que el umbral, el paso termina con `exit 1` y el despliegue no corre. Se puede hacer como *deployment protection rule* del environment de GitHub.
4. Excepción documentada: los commits etiquetados como arreglo de confiabilidad o hotfix pasan, con aprobación manual.
5. Se registra la decisión (auditoría) y se avisa al equipo.

Complemento clave: el gate **previo** evita desplegar con el presupuesto agotado; el análisis **posterior** (canary) revierte el despliegue si el cambio nuevo quema presupuesto (ver A4.3).
</details>

**A4.3** [Nombre] Una herramienta de Kubernetes despliega la versión nueva a un 5% del tráfico, consulta métricas en Prometheus durante unos minutos y, si empeoran, revierte sola. ¿Qué técnica es y qué herramientas la implementan?
<details><summary>Respuesta</summary>

**Canary release con análisis automático**, dentro de **progressive delivery**. Herramientas: **Argo Rollouts** (recurso `AnalysisTemplate` con proveedor Prometheus) y **Flagger** (con Istio/Linkerd/NGINX). Encaja con ArgoCD (GitOps) y responde al reto 1 del caso: que CI/CD "detenga o revierta automáticamente".
</details>

**A4.4** [Mesa] "Se acabó el Error Budget, pero negocio exige lanzar una campaña el viernes. ¿Qué haces?"
<details><summary>Respuesta</summary>

No es un "no" técnico: se aplica la Error Budget Policy acordada. Se escala al dueño del servicio y de negocio con datos (presupuesto en −X%, riesgo cuantificado) y se ofrecen alternativas: lanzar detrás de un **feature flag** a un porcentaje pequeño, ventana de bajo tráfico, canary con rollback automático, o aceptar el riesgo formalmente por escrito. El objetivo es convertir la discusión en una decisión de riesgo explícita.
</details>

**A5.1** [Nombre — repaso estricto] Recita de memoria las métricas DORA, sin pistas.
<details><summary>Respuesta</summary>

Las 4 clásicas: **Deployment Frequency**, **Lead Time for Changes**, **Change Failure Rate** y **Time to Restore Service** (en 2023 renombrada *Failed Deployment Recovery Time*). En 2021 se agregó una quinta: **Reliability** (operational performance). Conexión con el caso: Change Failure Rate se baja con el Quality Gate, Time to Restore se baja con mejor telemetría y Incident Command.
</details>

---

## Bloque B — OpenTelemetry por dentro y FinOps

**B1.1** [Nombre] En el Collector de OpenTelemetry, ¿cómo se llaman los componentes que (a) reciben datos, (b) los transforman, filtran o muestrean y (c) los envían a un backend? ¿Y el que une dos pipelines (por ejemplo, de trazas a métricas)?
<details><summary>Respuesta</summary>

(a) **Receivers** (por ejemplo, `otlp`, `prometheus`, `filelog`), (b) **Processors** (`memory_limiter`, `batch`, `attributes`, `transform`, `filter`, `tail_sampling`, `redaction`), (c) **Exporters** (`otlp`, `otlphttp`, `prometheusremotewrite`, `loadbalancing`) y **Connectors** (`spanmetrics`, `servicegraph`, `count`, `routing`), que actúan como exporter de un pipeline y receiver de otro. Todo se conecta en `service.pipelines` por señal (traces, metrics, logs).
</details>

**B1.2** ¿En qué orden pondrías `memory_limiter` y `batch` en un pipeline y por qué?
<details><summary>Respuesta</summary>

`memory_limiter` **primero**: rechaza datos antes de que el Collector se quede sin memoria (aplica backpressure en vez de dejar morir el proceso). `batch` **al final**, justo antes de los exporters: agrupa para enviar menos peticiones y comprimir mejor.
</details>

**B1.3** [Nombre] ¿Cómo se llama el protocolo nativo de OpenTelemetry y cuáles son sus puertos por defecto?
<details><summary>Respuesta</summary>

**OTLP** (OpenTelemetry Protocol): **4317** sobre gRPC y **4318** sobre HTTP.
</details>

**B2.1** Explica la diferencia entre desplegar el Collector como **agente** y como **gateway**, y cuándo usar cada uno.
<details><summary>Respuesta</summary>

**Agente**: un Collector por nodo (DaemonSet) o por pod (sidecar), cerca de la app. Recibe OTLP local, agrega metadatos de Kubernetes (`k8sattributes`), lee logs de archivo y hace el filtrado barato. **Gateway**: un Deployment centralizado y escalable, por clúster o región. Concentra el muestreo por cola, el enmascaramiento de PII, el enrutamiento a varios backends y las credenciales del proveedor. Lo típico en un banco multi-cloud es **ambos**: agentes en cada clúster de AWS y GCP → gateway regional → backends.
</details>

**B2.2** [Mesa] "¿Qué pasa si el Collector gateway se cae? ¿Perdemos telemetría en plena crisis?"
<details><summary>Respuesta</summary>

Mitigaciones:
- Gateway con **varias réplicas** detrás de un balanceador, con HPA (Horizontal Pod Autoscaler).
- `sending_queue` con **almacenamiento persistente** (`file_storage`) y reintentos en los exporters.
- `memory_limiter` para degradar en vez de caerse.
- Los agentes también hacen buffer.
- **Meta-monitoreo**: el Collector expone sus propias métricas (datos aceptados, rechazados, encolados) y se alerta sobre ellas.

"¿Quién observa al observador?" se responde con un stack de monitoreo independiente y mínimo.
</details>

**B2.3** [Nombre] Un operador de Kubernetes despliega Collectors y, con un recurso llamado `Instrumentation`, inyecta la auto-instrumentación en los pods sin tocar su código. ¿Cómo se llama?
<details><summary>Respuesta</summary>

**OpenTelemetry Operator**. Habilita "instrumentación sin cambiar código" para Java, .NET, Node.js y Python mediante anotaciones en los pods. Es clave para la adopción en 400 repositorios.
</details>

**B3.1** [Nombre] Una estrategia decide si guardar una traza **al inicio**, en el primer servicio, con un porcentaje fijo; otra la decide **al final**, cuando ya llegaron todos los spans, para quedarse con las lentas y las de error. ¿Cómo se llama cada una?
<details><summary>Respuesta</summary>

**Head-based sampling** (al inicio; se propaga en el flag `sampled` del `traceparent`; es barato pero puede descartar justo la traza del error) y **Tail-based sampling** (al final, en el Collector con el processor `tail_sampling`; guarda el 100% de errores y lentas y un porcentaje pequeño de las exitosas, pero exige memoria y espera).
</details>

**B3.2** ¿Qué problema de arquitectura tiene el tail sampling cuando el gateway tiene varias réplicas y cómo se resuelve?
<details><summary>Respuesta</summary>

Todos los spans de una misma traza deben llegar a **la misma réplica**; si no, ninguna ve la traza completa. Se resuelve con **dos capas**: la primera usa el exporter **`loadbalancing`** con enrutamiento por `traceID` y la segunda ejecuta `tail_sampling`. Se configura `decision_wait` (por ejemplo, 10 s) y políticas como `status_code` (errores), `latency` (> 2 s), `probabilistic` (2–5% del resto), `string_attribute` (por ejemplo, clientes VIP) y `composite`.
</details>

**B3.3** [Mesa] "Si descartas el 95% de las trazas, ¿no quedan mal las métricas de latencia y volumen?"
<details><summary>Respuesta</summary>

Solo si las métricas se calculan desde trazas ya muestreadas. Las métricas RED se generan **antes** del muestreo con el connector **`spanmetrics`** (o se emiten directamente desde el SDK como métricas), así que las métricas son 100% exactas y solo se muestrean las trazas, que son el detalle para depurar.
</details>

**B3.4** [Mesa] "¿Y si auditoría o un regulador piden una transacción cuya traza se descartó?"
<details><summary>Respuesta</summary>

La telemetría **no es el registro de auditoría**. La evidencia regulatoria (logs de auditoría y transaccionales) va por un pipeline separado que **nunca** se muestrea, con retención legal y almacenamiento inmutable. El muestreo aplica solo a la observabilidad operativa.
</details>

**B4.1** [Nombre] ¿Cómo se llama el header estándar W3C que lleva el identificador de la traza entre servicios? ¿Qué formato tiene? ¿Y el header que lleva pares clave-valor de negocio?
<details><summary>Respuesta</summary>

**`traceparent`**: `00-<trace-id de 32 hex>-<parent-id de 16 hex>-<flags de 2 hex>`; `01` significa muestreada. **`tracestate`** lleva datos propios del proveedor. **`baggage`** lleva contexto de negocio (por ejemplo, `canal=qr`). **B3** es el formato heredado de **Zipkin** (`X-B3-TraceId` o el header único `b3`); el Collector y los SDK pueden aceptar ambos durante una migración.
</details>

**B4.2** ¿Cómo mantienes la traza cuando el pago pasa por Kafka o por una cola MQ hacia el core bancario?
<details><summary>Respuesta</summary>

El productor **inyecta** `traceparent` en los **headers del mensaje** (de Kafka o propiedades de MQ) y el consumidor lo **extrae**. Como el consumo es asíncrono (puede procesar en lote, mucho después), se usan **span links** en vez de una relación padre-hijo directa. Si el sistema legacy (AS400) no se puede instrumentar, se instrumenta el **adaptador o puente MQ** de entrada y salida y se correlaciona por un ID de negocio (número de transacción).
</details>

**B5.1** [Nombre] Un equipo agrega a una métrica de Prometheus la etiqueta `user_id` y la base de series explota en memoria y costo. ¿Cómo se llama el problema?
<details><summary>Respuesta</summary>

**Explosión de cardinalidad** (high cardinality): cada combinación única de etiquetas es una serie temporal nueva. Los identificadores únicos (usuario, transacción) van en **trazas o logs**, no como etiquetas de métricas. Es una de las mayores palancas de costo de FinOps en observabilidad.
</details>

**B5.2** Propón tres medidas concretas para bajar 30% el costo de telemetría sin perder visibilidad de errores.
<details><summary>Respuesta</summary>

1. **Tail sampling**: 100% de errores y lentas, 2–5% de exitosas. Es lo que más ahorra en trazas.
2. **Log-to-Metrics** en el borde: convertir logs repetitivos ("pago OK") en contadores con el connector `count` o métricas derivadas, y quitar logs DEBUG en producción con el processor `filter`.
3. **Control de cardinalidad** y retención por niveles (caliente 7–15 días, fría en almacenamiento de objetos barato).

Bonus: **showback** del costo de telemetría por equipo (FinOps) para que cada Tribu vea lo que ingiere. Siempre medir antes y después (línea base de GB/día).
</details>

**B6.1** ¿Dónde y cómo enmascaras números de tarjeta o cédulas para que nunca salgan de la red del banco hacia un SaaS (Software as a Service) de observabilidad?
<details><summary>Respuesta</summary>

En el **Collector**, dentro de la red del banco (agente o gateway), **antes del exporter**: processor **`redaction`** (lista blanca de atributos permitidos y expresiones regulares de valores bloqueados), **`transform`** con OTTL (OpenTelemetry Transformation Language; por ejemplo, `replace_pattern`) o `attributes` (delete/hash). Nunca en la consola del SaaS: ahí el dato ya salió. Marco: **Ley 1581 de 2012** (habeas data), circulares de la **SFC** (Superintendencia Financiera de Colombia) sobre seguridad de la información y ciberseguridad, y **PCI DSS** para datos de tarjeta (mostrar como máximo los primeros 6 y últimos 4 dígitos del PAN, Primary Account Number).
</details>

---

## Bloque C — Telemetría AI-Ready, MCP e IA para RCA

**C1.1** [Nombre] ¿Cómo se llama la especificación de OpenTelemetry que estandariza los nombres de atributos (`service.name`, `http.response.status_code`, `db.system`…) para que todos los equipos llamen igual a lo mismo?
<details><summary>Respuesta</summary>

**Semantic Conventions**. Junto con los **resource attributes** obligatorios del banco (`service.name`, `service.version`, `deployment.environment.name`, equipo dueño, `business.journey`) son lo que hace la telemetría "AI-Ready": un modelo de IA no puede razonar sobre datos donde un equipo dice `status`, otro `http_code` y otro `resp`.
</details>

**C1.2** [Nombre] ¿Cómo se llama el mecanismo que, en un punto de una métrica (por ejemplo, un pico de latencia p99), guarda el `trace_id` de una traza de ejemplo para saltar de la métrica a la traza?
<details><summary>Respuesta</summary>

**Exemplars**. Conectan métricas → trazas → logs (los logs llevan `trace_id`/`span_id`) y bajan el MTTR porque el ingeniero salta del síntoma al detalle en un clic.
</details>

**C2.1** ¿Cómo obtienes automáticamente el mapa de qué servicio llama a cuál, sin dibujarlo a mano?
<details><summary>Respuesta</summary>

De las trazas: cada span cliente → servidor es una **arista** del grafo. En el Collector, el connector **`servicegraph`** genera métricas de aristas (peticiones, errores y latencia entre pares de servicios). Lo visualizan Grafana Tempo (service graph), Kiali (con Istio) o los service maps de Datadog/Dynatrace. Es el "grafo de topología vivo" que menciona la rúbrica.
</details>

**C3.1** [Mesa] "Diez servicios alertan al mismo tiempo. ¿Cómo sabe la IA cuál es la causa y no solo un síntoma?"
<details><summary>Respuesta</summary>

**Correlación ≠ causalidad**: todos se correlacionan con la falla. Se usa la **topología**: un candidato a causa raíz es un nodo anómalo cuyas **dependencias están sanas** (la anomalía nace ahí y se propaga hacia quienes lo llaman). Se cruza con **eventos de cambio** (despliegues, cambios de configuración y feature flags en la ventana) y con el orden temporal. Eso reduce 10 alertas a 1–2 hipótesis. La IA **propone y explica**; el humano decide (o se automatiza solo lo de bajo riesgo). Detalle en `grafos-troubleshooting.md`.
</details>

**C3.2** [Nombre] ¿Cómo se llama agrupar 200 alertas de un mismo incidente en un solo caso, y el área de IA aplicada a operaciones que lo hace?
<details><summary>Respuesta</summary>

**Correlación / deduplicación de alertas** (event correlation, noise reduction), dentro de **AIOps** (Artificial Intelligence for IT Operations). La rúbrica advierte que AIOps **no** es "prender las alertas predictivas que vienen por defecto en la herramienta".
</details>

**C4.1** Explica cómo MCP (Model Context Protocol) encaja en la observabilidad del banco.
<details><summary>Respuesta</summary>

MCP es el protocolo estándar para que un agente de IA (cliente MCP) use **herramientas** expuestas por un **servidor MCP**. Se construye o adopta un servidor MCP de observabilidad (existen para Grafana, Datadog y Prometheus) con herramientas como `consultar_slo(servicio)`, `buscar_trazas(error, ventana)`, `dependencias(servicio)` y `cambios_recientes(servicio)`. El agente de RCA navega esas herramientas en vez de recibir todos los logs en el prompt: menos costo, menos alucinación y respuestas trazables. Los Semantic Conventions hacen que las herramientas devuelvan datos homogéneos.
</details>

**C4.2** [Mesa — DevSecOps] "¿Darle a un agente de IA acceso a la telemetría de producción de un banco no es un riesgo?"
<details><summary>Respuesta</summary>

Sí, y se controla así:
1. **Solo lectura** y mínimo privilegio en el servidor MCP; las acciones de remediación pasan por aprobación humana.
2. Telemetría **ya enmascarada** (sin PII) en el Collector.
3. **Prompt injection por logs**: un log puede contener texto controlado por un atacante (por ejemplo, el campo "descripción" de una transferencia), así que el agente trata los datos como datos, nunca como instrucciones.
4. Auditoría de cada llamada a las herramientas.
5. Modelo desplegado en una región o red aprobada por el banco.
</details>

**C5.1** *(Opcional)* Si modelas el sistema como un grafo dirigido de dependencias, ¿qué algoritmo usarías para calcular el "radio de explosión" de una base de datos caída y cuál para rankear causas raíz probables?
<details><summary>Respuesta</summary>

Radio de explosión: **BFS/DFS** (Breadth-First Search / Depth-First Search) sobre el grafo **invertido** (quién depende de mí), O(V+E). Ranking de causas: **random walk / PageRank personalizado** sobre el grafo ponderado por anomalías (técnica de papers como MicroRCA). Ver `grafos-troubleshooting.md`.
</details>

---

## Bloque D — Incidentes y cultura

**D1.1** [Nombre] En un incidente grave, ¿cómo se llaman los roles que (a) coordina y decide sin tocar teclado, (b) ejecuta los cambios técnicos, (c) informa a negocio y clientes y (d) documenta la línea de tiempo?
<details><summary>Respuesta</summary>

(a) **Incident Commander** (IC), (b) **Operations Lead** (Ops Lead), (c) **Communications Lead** (Comms Lead) y (d) **Scribe**. Vienen del ICS (Incident Command System) de los bomberos de EE. UU., adaptado por Google y PagerDuty. El IC delega y no depura: si se pone a depurar, nadie coordina.
</details>

**D1.2** Son las 12:30 de un día de quincena y el pago QR falla en un 30%. Eres el Incident Commander. ¿Qué haces en los primeros 15 minutos?
<details><summary>Respuesta</summary>

1. **Declarar** el incidente y la severidad (SEV1: impacto masivo a clientes) y abrir el canal o puente.
2. **Asignar roles**: Ops Lead, Comms Lead, Scribe.
3. **Evaluar el impacto** con el SLO y el burn rate: cuántos clientes y desde cuándo.
4. **Preguntar qué cambió** (despliegues, configuración, feature flags, proveedor externo) usando el grafo de topología.
5. **Mitigar antes de diagnosticar**: rollback del último despliegue, apagar el feature flag, failover a la otra nube o región, load shedding.
6. **Comunicar** cada 15–30 minutos a negocio y canales (página de estado) con hechos, no especulación.
7. Tras estabilizar: confirmar la recuperación con el SLI, hacer handoff y programar el post-mortem.
</details>

**D2.1** [Nombre] Un patrón deja de llamar a una dependencia que está fallando durante un tiempo, devuelve un error rápido o un fallback y luego prueba de nuevo. ¿Cómo se llama? ¿Y el que rechaza parte del tráfico a propósito para salvar el resto?
<details><summary>Respuesta</summary>

**Circuit Breaker** (estados cerrado → abierto → semi-abierto) y **Load Shedding** (descartar tráfico de baja prioridad, por ejemplo consultas de saldo, para proteger el pago). Relacionado: **Bulkhead** (aislar recursos por tipo de tráfico) y **Rate Limiting**.
</details>

**D3.1** ¿Qué debe tener un post-mortem y qué significa que sea "blameless"?
<details><summary>Respuesta</summary>

Contenido: resumen e impacto (clientes, minutos, presupuesto consumido), línea de tiempo (detección → mitigación → resolución), causa raíz y **factores contribuyentes**, qué salió bien, qué salió mal, dónde tuvimos suerte, y **acciones** con dueño y fecha clasificadas en prevenir, detectar y mitigar. **Blameless**: se asume que las personas actuaron razonablemente con la información que tenían; se arregla el **sistema** que permitió el error, no se busca culpable. Si no, la gente oculta información y se pierde el aprendizaje.
</details>

**D3.2** [Mesa] "¿Los 5 porqués no bastan?"
<details><summary>Respuesta</summary>

Son útiles pero lineales: llevan a **una** causa, y los sistemas complejos fallan por **varios factores contribuyentes** a la vez. También sesgan hacia el último humano en la cadena. Se complementan con análisis de factores contribuyentes y preguntas como "¿qué hizo que esto pareciera razonable en el momento?".
</details>

**D4.1** [Nombre] ¿Cómo se llama el trabajo operativo manual, repetitivo, automatizable, sin valor duradero y que crece linealmente con el servicio? ¿Qué límite recomienda Google?
<details><summary>Respuesta</summary>

**Toil**. Google recomienda que el toil sea **menos del 50%** del tiempo de un SRE; el resto es ingeniería. Herramientas para reducirlo: autoservicio en el IDP, **Runbook as Code** (runbooks ejecutables), auto-remediación de bajo riesgo.
</details>

**D4.2** [Nombre] ¿Cómo se llama inyectar fallas controladas en producción o preproducción para validar una hipótesis de "estado estable", y qué herramientas conoces?
<details><summary>Respuesta</summary>

**Chaos Engineering** (nació en Netflix con Chaos Monkey). Herramientas: **LitmusChaos**, **Chaos Mesh** (Kubernetes), **AWS FIS** (Fault Injection Service), **Azure Chaos Studio**. Se practica con **Game Days** y se empieza con un radio de explosión pequeño.
</details>

---

## Bloque E — Temas aledaños (la ronda que puede dejarnos mal parados)

**E1.1** [Nombre] El celular del cliente reenvía el mismo pago porque no recibió respuesta. ¿Qué mecanismo evita cobrar dos veces?
<details><summary>Respuesta</summary>

**Idempotency Key** (clave de idempotencia): el cliente envía un ID único por intención de pago; el servidor guarda el resultado por esa clave y, ante un reintento, devuelve el mismo resultado sin reprocesar. Es obligatorio en pagos y es lo que hace seguros los reintentos.
</details>

**E1.2** [Nombre] Mil clientes reintentan exactamente al mismo tiempo tras una caída y vuelven a tumbar el servicio. ¿Cómo se llama el problema y cuál es la técnica de reintento correcta?
<details><summary>Respuesta</summary>

**Retry storm / thundering herd**. Solución: **exponential backoff con jitter** (esperas crecientes con aleatoriedad), límite de reintentos o *retry budget*, timeouts bien escalonados (el de afuera mayor que la suma de los de adentro) y circuit breaker.
</details>

**E2.1** [Nombre] ¿Cómo se llaman (a) el tiempo máximo aceptable para recuperar el servicio y (b) la cantidad máxima de datos que se acepta perder, medida en tiempo?
<details><summary>Respuesta</summary>

(a) **RTO** (Recovery Time Objective) y (b) **RPO** (Recovery Point Objective). Para pagos el RPO tiende a 0 (replicación síncrona o transaccional), lo que encarece y añade latencia. Activo-activo multi-cloud baja el RTO pero complica la consistencia de datos (ver consistencia fuerte vs. eventual, tema 06).
</details>

**E3.1** [Mesa] "Tenemos el p99 de cada pod. ¿Promediamos los p99 para obtener el p99 del servicio?"
<details><summary>Respuesta</summary>

**No**: los percentiles no se promedian. Se usan **histogramas** (en Prometheus, `histogram_quantile(0.99, sum by (le) (rate(..._bucket[5m])))`), que sí se agregan entre pods. Los *summaries* calculan el percentil en el cliente y no se pueden agregar. Tampoco se usa el promedio para SLOs de latencia: esconde la cola.
</details>

**E4.1** [Nombre] ¿Qué ley relaciona peticiones concurrentes en el sistema = tasa de llegada × tiempo en el sistema, y para qué sirve en capacidad?
<details><summary>Respuesta</summary>

**Ley de Little**: L = λ × W. Ejemplo: 2.000 pagos/s × 0,25 s = 500 peticiones concurrentes. Sirve para dimensionar pools de conexiones, hilos y réplicas, y muestra por qué cuando sube la latencia (W) se saturan los recursos aunque el tráfico no cambie.
</details>

**E5.1** [Mesa — DevSecOps] "¿Cómo aseguras la propia plataforma de observabilidad?"
<details><summary>Respuesta</summary>

- **mTLS** (mutual TLS) entre agentes, gateway y backends.
- Autenticación de los receivers (extensiones `bearertokenauth`/`oidc`).
- Credenciales del SaaS en Key Vault o Secrets Manager con Managed Identity / IAM Role, nunca en el YAML.
- Imágenes del Collector escaneadas (Trivy) y construidas solo con los componentes necesarios (**OCB**, OpenTelemetry Collector Builder), lo que reduce la superficie de ataque.
- Políticas OPA para que nadie despliegue un Collector sin el processor de redaction.
- Prompt injection por logs si hay IA (ver C4.2).
</details>

**E6.1** [Mesa] "¿Qué regulación colombiana afecta este diseño?"
<details><summary>Respuesta</summary>

- **Ley 1581 de 2012** (protección de datos personales / habeas data).
- Instrucciones de la **SFC** sobre seguridad de la información y gestión del riesgo de ciberseguridad (por ejemplo, la Circular Externa 007 de 2018). Antes de citar una circular específica en la exposición, verificar su número vigente.
- **PCI DSS** si hay datos de tarjeta.
- Si preguntan por "transferencias en tiempo real" en Colombia: **Bre-B**, el sistema de pagos inmediatos del Banco de la República. El caso habla de "CBU/QR"; CBU (Clave Bancaria Uniforme) es argentino, así que se puede comentar con tacto.
</details>

**E7.1** [Nombre — repaso estricto] Recita de memoria los pilares de Well-Architected y di cuál cubre esta prueba.
<details><summary>Respuesta</summary>

**Operational Excellence**, **Security**, **Reliability**, **Performance Efficiency**, **Cost Optimization** y **Sustainability** (los 6 de AWS; Azure tiene 5, sin Sustainability como pilar). La prueba cubre sobre todo Reliability y Operational Excellence, con Cost Optimization (FinOps) y Security (PII).
</details>

---

## Bloque F — Entregable

**F1.1** [Nombre] ¿Cómo se llama el modelo de diagramas de Simon Brown con 4 niveles de zoom, y cuáles son?
<details><summary>Respuesta</summary>

**Modelo C4**: **Context** (sistema y actores), **Container** (aplicaciones, bases de datos, colas), **Component** (piezas dentro de un container) y **Code**. Para la presentación bastan Context y Container, más un diagrama de flujo de la telemetría.
</details>

**F2.1** Cuenta en 60 segundos la historia completa de tu propuesta (SLO → telemetría → IA → incidente).
<details><summary>Respuesta</summary>

Se evalúa en vivo: debe salir en orden y con al menos un número por eje (por ejemplo, 99,9% → 43,2 min; −30% de costo con tail sampling; MTTR de X a Y).
</details>
