# Libreto de diapositivas - Observabilidad y sus herramientas (entrevista Cardif)

Plan de la presentación para repasar la entrevista cuyo cliente final es **Cardif** (BNP Paribas
Cardif, aseguradora). Ya hubo una entrevista con **Amaris** para el mismo cliente; esta es con otra
empresa. Cada diapositiva tiene:

- `Sección`: a qué parte del tema pertenece.
- `Diagrama`: el o los diagramas de [diagramas-c4.md](diagramas-c4.md).
- Viñetas: lo que se ve en pantalla.
- `>` guion: lo que dices en voz alta. En la presentación aparece al oprimir **N** (notas).

La presentación [presentacion.html](presentacion.html) se genera con
`python3 generar_presentacion.py` a partir de este archivo y del de diagramas.

Regla de honestidad: lo tuyo es **Grafana y Datadog** (uso diario en dashboards, alertas e
investigación), **AWS CloudWatch**, **OpenTelemetry en una prueba de concepto**, Kubernetes/AKS, y el
**servidor MCP diseñado con el equipo de observabilidad de MercadoLibre**. Dynatrace, New Relic,
Splunk, ELK administrado y PagerDuty se explican como opciones del mercado, **no se dice que los
usaste**.

---

## Observabilidad: señales, flujo y herramientas
**Sección:** Portada
- Entrevista para el cliente **Cardif** (aseguradora) · noviembre 2026
- Las **4 señales** (MELT), los **6 pasos** del flujo de telemetría y la **herramienta** de cada paso
- Diagramas C4 (Context, Containers, Components, Code)
- Teclas: ← → para moverse · N para ver el guion

> Esta presentación es un mapa mental: si recuerdas las cuatro señales y los seis pasos, recuerdas en qué lugar va cada herramienta.

---

## Monitoreo vs. observabilidad
**Sección:** Panorama
**Diagrama:** D1
- **Monitoreo**: preguntas que **ya conoces** (¿está arriba?, ¿CPU > 80 %?)
- **Observabilidad**: poder responder preguntas **nuevas** sobre el sistema, solo mirando lo que emite
- El monitoreo dice **QUÉ** se rompió; la observabilidad ayuda a saber **POR QUÉ** y **DÓNDE**
- Objetivo de negocio: bajar **MTTD** (Mean Time To Detect) y **MTTR** (Mean Time To Recover)

> El monitoreo es un tablero de preguntas que ya conozco: si la CPU pasa de ochenta por ciento, me avisa. La observabilidad es poder preguntarle al sistema algo que nunca había pensado, por ejemplo por qué solo los pagos con tarjeta de un banco se demoran desde el deploy de ayer, usando las métricas, los logs y las trazas que el sistema ya emite. Para una aseguradora como Cardif, eso se traduce en detectar antes y recuperar más rápido: menos MTTD y menos MTTR.

---

## Las 4 señales: MELT
**Sección:** Panorama
**Diagrama:** D2
- **Metrics**: números agregados en el tiempo · baratas · disparan alertas
- **Events**: cambios discretos (deploy, cambio de configuración) · la primera sospecha
- **Logs**: el detalle de **qué pasó** dentro del servicio · caros si no se controlan
- **Traces**: el recorrido de **una petición** por todos los servicios, dividida en **spans**
- Se unen con contexto común: `service.name`, `env`, `version` y **trace_id**

> MELT: Metrics, Events, Logs y Traces. Las métricas me dicen que algo anda mal y cuánto; los eventos me dicen qué cambió, y casi siempre el culpable es el último deploy; los logs me dicen por qué falló; y las trazas me dicen dónde se demora una petición. Una alerta no es una traza: la alerta sale de una métrica, y la traza es lo que miro después para encontrar el servicio culpable.

---

## Los 6 pasos del flujo de telemetría
**Sección:** Panorama
**Diagrama:** D3
- **1 Instrumentar** · **2 Recolectar** · **3 Almacenar**
- **4 Visualizar** · **5 Alertar** · **6 Actuar**
- El paso 6 **retroalimenta** el 1: cada incidente deja una alerta, un runbook o más instrumentación

> Para recordar las herramientas, sigo la telemetría desde que nace hasta que alguien actúa. Primero el código se instrumenta; un agente o collector la recolecta; se guarda en un backend por señal; se visualiza en dashboards; se alerta contra un SLO; y una persona actúa con un runbook. Lo que aprendo en el incidente vuelve al paso uno.

---

## Paso 1 · Instrumentar con OpenTelemetry
**Sección:** Flujo de telemetría
**Diagrama:** D4
- **OpenTelemetry (OTel)**: estándar abierto de la CNCF (Cloud Native Computing Foundation) para métricas, logs y trazas
- **Auto-instrumentación**: HTTP, base de datos, colas, sin tocar el código
- **Instrumentación manual**: spans y métricas **de negocio** (pólizas emitidas, pagos fallidos)
- Protocolo **OTLP** (OpenTelemetry Protocol): gRPC 4317, HTTP 4318
- Ventaja: instrumentas **una vez** y cambias de backend sin reescribir (sin vendor lock-in)

> Instrumentar es hacer que la aplicación emita telemetría. El estándar es OpenTelemetry: tiene SDK para cada lenguaje y auto-instrumentación que captura HTTP, base de datos y colas sin cambiar código. Encima agrego métricas de negocio, que son las que le importan a una aseguradora, como pólizas emitidas o pagos rechazados. Lo hice en una prueba de concepto; la gran ventaja es que si mañana se cambia de Datadog a Grafana, la instrumentación no se toca.

---

## Paso 2 · Recolectar con el OpenTelemetry Collector
**Sección:** Flujo de telemetría
**Diagrama:** D5
- **Receivers → Processors → Exporters**: el pipeline del **OpenTelemetry Collector**
- **Processors**: `batch`, `memory_limiter`, **borrar PII**, **tail sampling** de trazas
- Despliegue: **agente** (DaemonSet en cada nodo) + **gateway** central
- Alternativas: **Fluent Bit** / Fluentd / Logstash (logs), **Datadog Agent**, scrape de **Prometheus**

> El Collector es el punto de control de la telemetría. Recibe, procesa y exporta. En el procesamiento es donde se protege el negocio: se borran datos personales antes de guardarlos y se hace sampling para no pagar por millones de trazas iguales. Además, el Collector puede mandar la misma telemetría a dos backends a la vez, lo que facilita una migración.

---

## Paso 3 · Almacenar: un backend por señal
**Sección:** Flujo de telemetría
**Diagrama:** D6
- **Métricas**: **Prometheus** (series de tiempo, PromQL) + **Thanos** o **Mimir** para largo plazo
- **Logs**: **Elasticsearch / OpenSearch** (índice completo) o **Loki** (indexa solo etiquetas, más barato)
- **Trazas**: **Jaeger** o **Grafana Tempo**
- Retención larga y barata en **object storage** (S3, Azure Blob)
- Enemigo número uno del costo: la **cardinalidad** (etiquetas con user_id, póliza_id)

> Cada señal tiene su base de datos. Prometheus guarda métricas como series de tiempo y se consulta con PromQL; para guardar meses se agrega Thanos o Mimir. Los logs van a Elasticsearch u OpenSearch, o a Loki, que es más barato porque solo indexa etiquetas. Las trazas van a Jaeger o Tempo. El error típico es poner el número de póliza como etiqueta de una métrica: eso explota la cardinalidad y el costo.

---

## Paso 4 · Visualizar: dashboards que responden preguntas
**Sección:** Flujo de telemetría
**Diagrama:** D7
- **Grafana** (open source, une todas las fuentes) · **Kibana** (logs de Elasticsearch) · Datadog
- **Golden signals** (Google SRE): latencia, tráfico, errores, saturación
- **RED** para servicios: Rate, Errors, Duration · **USE** para recursos: Utilization, Saturation, Errors
- Arriba el **SLO**, abajo el detalle · **anotaciones de deploys** en las gráficas
- Dashboards como código (JSON en Git, provisioning, Terraform)

> Un dashboard bueno se lee de arriba hacia abajo: primero el SLO y el error budget, después RED del servicio, después USE de la infraestructura, y con los deploys marcados como anotaciones para ver si el problema empezó con un cambio. Es lo que usaba todos los días en Grafana y Datadog en MercadoLibre. Y los dashboards se versionan en Git como cualquier código.

---

## Paso 5 · Alertar sobre SLO, no sobre síntomas sueltos
**Sección:** Flujo de telemetría
**Diagrama:** D8
- **SLI** (Service Level Indicator): la medida · **SLO** (Service Level Objective): la meta · **SLA** (Service Level Agreement): el contrato
- **Error budget**: 99,9 % en 30 días ≈ **43 minutos** de falla permitidos
- Alerta por **burn rate** (multi-ventana): página si el presupuesto se gasta demasiado rápido
- **Alertmanager** agrupa, silencia y enruta → **PagerDuty / Opsgenie** → persona de guardia
- Regla: toda alerta que despierta a alguien debe ser **accionable** y tener **runbook**

> No alerto por CPU alta; alerto cuando el cliente sufre. El SLI es, por ejemplo, el porcentaje de pagos exitosos en menos de dos segundos; el SLO es noventa y nueve coma nueve por ciento en treinta días, lo que deja unos cuarenta y tres minutos de error budget. Con burn rate, si en una hora se está gastando el presupuesto catorce veces más rápido de lo normal, se llama a la persona de guardia; si se gasta lento, se abre un ticket. Así se evita la fatiga de alertas.

---

## Paso 6 · Actuar: el ciclo del incidente
**Sección:** Flujo de telemetría
**Diagrama:** D9
- **Detectar → Triage → Runbook → Mitigar → Postmortem → Acciones**
- **Mitigar primero**, investigar después (rollback, escalar, desviar tráfico)
- **Postmortem sin culpables** (blameless): línea de tiempo, causa raíz, acciones con dueño
- Se mide con **MTTD** y **MTTR**

> Cuando suena la alerta, lo primero es medir el impacto y mitigar, muchas veces con un rollback del último deploy, que es la causa más común. La causa raíz se busca con calma después. Al final viene el postmortem sin culpables, y cada acción del postmortem vuelve al paso uno: una alerta nueva, un runbook mejor o más instrumentación.

---

## Correlación: el trace_id une todo
**Sección:** Correlación
**Diagrama:** D10
- Ejemplo: el pago de una póliza pasa por **5 microservicios**
- La **métrica** avisa: la latencia p99 de pagos subió
- La **traza** (Jaeger / Tempo / Datadog APM) muestra: **Pagos** tarda 3,2 s
- El **log** filtrado por el mismo **trace_id** dice: timeout con la pasarela bancaria
- **Exemplars**: desde un punto de la gráfica se salta directo a una traza

> Este es el valor real de la observabilidad. La métrica me avisa que el p99 subió. Abro una traza de esas peticiones lentas y veo que de los cinco servicios el que tarda tres segundos es Pagos. Copio el trace_id, filtro los logs, y aparece el timeout con la pasarela bancaria. Sin el trace_id en los logs, tendría que buscar a ciegas en cinco servicios.

---

## Herramientas: las tres familias
**Sección:** Herramientas
**Diagrama:** D11
- **Open source**: **Prometheus + Grafana**, stack **LGTM** (Loki, Grafana, Tempo, Mimir), **ELK / EFK**, Jaeger
- **SaaS**: **Datadog**, **Dynatrace**, **New Relic**, **Splunk** · rápido de adoptar, se paga por volumen
- **Nativas de la nube**: **AWS CloudWatch + X-Ray**, **Azure Monitor + Application Insights + Log Analytics**
- **OpenTelemetry** por debajo de las tres: evita quedar amarrado a un proveedor
- Criterio: costo por volumen, equipo para operarlo, multi-nube, cumplimiento

> Hay tres familias. Open source, que es barata en licencias pero hay que operarla: Prometheus, Grafana, Loki, Tempo, Elasticsearch. SaaS, como Datadog, Dynatrace, New Relic o Splunk, que se adoptan rápido pero se pagan por host o por gigabyte. Y las nativas de la nube, CloudWatch en AWS y Azure Monitor con Application Insights en Azure. Yo he trabajado con Grafana, Datadog y CloudWatch. Lo que recomiendo siempre es instrumentar con OpenTelemetry para poder cambiar de familia sin reescribir.

---

## Observabilidad en Kubernetes
**Sección:** Kubernetes
**Diagrama:** D12
- **kube-prometheus-stack** (Helm): Prometheus Operator, Alertmanager, Grafana
- **ServiceMonitor / PodMonitor**: cada equipo declara qué se scrapea
- **node-exporter** (nodos) + **kube-state-metrics** (estado de objetos) + **cAdvisor** (contenedores)
- **DaemonSet** del Collector o de Fluent Bit para logs y trazas
- Alertas clásicas: **CrashLoopBackOff**, **OOMKilled**, pods pendientes, réplicas no disponibles

> En Kubernetes lo estándar es instalar kube-prometheus-stack con Helm. node-exporter da las métricas de las máquinas, kube-state-metrics el estado de deployments y pods, y cada equipo declara con un ServiceMonitor qué quiere que Prometheus scrapee. Los logs y trazas salen por un DaemonSet del Collector. Las primeras alertas que pongo son CrashLoopBackOff, OOMKilled y réplicas no disponibles.

---

## Una aseguradora regulada: datos sensibles y costo
**Sección:** Contexto Cardif
**Diagrama:** D13
- **PII** (Personally Identifiable Information): cédula, tarjeta, datos de salud **nunca** en logs claros
- Enmascarar **en el Collector**, antes de guardar; logs estructurados (JSON) sin payloads completos
- **RBAC** (Role-Based Access Control) + SSO: quién puede leer qué logs; auditoría de accesos
- **Retención** por tipo de dato según la norma (Ley 1581 de habeas data, Superintendencia Financiera)
- **FinOps** de la observabilidad: sampling, niveles de log, cardinalidad, retención caliente vs. archivo

> En una aseguradora la observabilidad toca datos muy sensibles: cédulas, tarjetas, incluso diagnósticos en un siniestro de salud o vida. Por eso enmascaro en el Collector, antes de que el dato llegue al backend; controlo con RBAC quién lee cada índice; y defino la retención según la norma, con la ley de habeas data y la Superintendencia Financiera en Colombia. Y vigilo el costo, porque la observabilidad puede volverse una de las facturas más grandes de la nube.

---

## Mi experiencia con observabilidad
**Sección:** Experiencia
**Diagrama:** D14
- **MercadoLibre**: dashboards, alertas e investigación de incidentes con **Grafana** y **Datadog**
- Agente de **IA** para triage de incidentes con un servidor **MCP** (Model Context Protocol) diseñado con el equipo de **o11y**
- Embudo: **dependencias → métricas → trazas → logs**, diagnóstico con certezas e incertidumbres
- **Humano en el bucle**: el agente solo lee; una persona aprueba cada acción
- **AWS CloudWatch** en la nube; **OpenTelemetry** en una prueba de concepto

> En MercadoLibre la observabilidad era mi día a día con Grafana y Datadog. El proyecto más interesante fue un agente de IA que hacía el triage de incidentes: con un servidor MCP que diseñamos junto al equipo de observabilidad, el agente seguía un embudo, primero el mapa de dependencias para ver el radio de impacto, luego métricas, trazas y logs, y entregaba un diagnóstico con certezas e incertidumbres. Siempre en solo lectura y con una persona aprobando la acción.

---

## Preguntas probables, respuesta corta
**Sección:** Preparación
- **¿Logs, métricas y trazas?** Métrica = qué y cuánto · log = por qué · traza = dónde
- **¿Cómo evitas la fatiga de alertas?** Alertas por SLO y burn rate, accionables, con runbook
- **¿Prometheus pull o push?** **Pull** (scrape); para jobs cortos, **Pushgateway**
- **¿Cómo bajas el costo?** Sampling, cardinalidad, niveles de log, retención por niveles
- **¿Por qué OpenTelemetry?** Estándar abierto, un solo SDK, cambio de backend sin reescribir
- **¿Primer paso en un sistema sin observabilidad?** Golden signals + SLO del flujo crítico (pagar, reclamar)

> Si me preguntan por dónde empezaría en Cardif: identifico los dos o tres viajes críticos del cliente, como cotizar, pagar y reclamar un siniestro, les defino un SLI y un SLO, instrumento con OpenTelemetry, y armo las alertas por burn rate. Después crezco hacia el resto.

---

## Nombres clave para repasar
**Sección:** Repaso
- **Señales**: MELT · spans · trace_id · exemplars · cardinalidad
- **Estándar**: OpenTelemetry · OTLP · Collector (receivers, processors, exporters) · tail sampling
- **Open source**: Prometheus · PromQL · Alertmanager · Thanos / Mimir · Grafana · Loki · Tempo · Jaeger · ELK / OpenSearch · Fluent Bit
- **SaaS**: Datadog · Dynatrace · New Relic · Splunk · **Nativas**: CloudWatch + X-Ray · Azure Monitor + Application Insights
- **SRE**: SLI · SLO · SLA · error budget · burn rate · golden signals · RED · USE · MTTD · MTTR · postmortem
- **Kubernetes**: kube-prometheus-stack · ServiceMonitor · node-exporter · kube-state-metrics

> Repaso rápido antes de entrar: las cuatro señales, los seis pasos, y una herramienta por paso.
