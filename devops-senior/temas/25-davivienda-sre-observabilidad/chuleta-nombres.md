# Chuleta de nombres — Prueba Davivienda

Leer 5 minutos antes de cada sesión. Cada nombre con su imagen para recordarlo.

## Bloque A — SRE

| Nombre | Imagen | Qué es |
|---|---|---|
| **SLI / SLO / SLA** | Termómetro / meta / contrato | SLI mide; SLO es la meta interna; SLA promete con multa (y es **más flojo** que el SLO) |
| **Golden Signals** | "El servicio **LaTES**" (el pulso) | **La**tency, **T**raffic, **E**rrors, **S**aturation |
| **RED / USE** | RED = el síntoma; USE = la causa | RED (Rate, Errors, Duration) para servicios; USE (Utilization, Saturation, Errors) para recursos |
| **Error Budget** | Margen para fallar | 1 − SLO. 99,9% = 43,2 min/mes; cada nueve divide por 10 |
| **Serie / paralelo** | Serie resta, paralelo suma un nueve | Serie: A×B×C. Paralelo: 1 − (1−A)ⁿ (se multiplican las **fallas**) |
| **Burn rate** | Velocidad de gasto del presupuesto | Error actual ÷ (1 − SLO). 14,4 = se acaba en ~2 días |
| **Multi-window, multi-burn-rate** | Ventana larga + corta, varios niveles | 14,4× 1 h → page; 6× 6 h → page; 1× 3 días → ticket |
| **Error Budget Policy** | El "qué pasa si" firmado con negocio | Reglas por umbral: desplegar normal / solo canary / congelar |
| **Quality Gate** | La puerta del pipeline | Antes: consulta presupuesto. Durante: canary. Después: verificación |
| **Canary / Blue-Green** | Canario en la mina / dos casas | Canary: % creciente de tráfico. Blue-Green: cambio total y vuelta total |
| **Argo Rollouts / Flagger** | Los que revierten solos | Canary con análisis automático contra Prometheus |
| **Feature Flag** | Interruptor | Separa **desplegar** de **liberar** |
| **DORA** | "**DeLiCaTe**" | **De**ployment Frequency, **L**ead T**i**me, **C**h**a**nge Failure Rate, **T**ime to R**e**store |

## Bloque B — OpenTelemetry

| Nombre | Imagen | Qué es |
|---|---|---|
| **Collector** | La **cocina** completa (no es un paso) | Proceso intermedio entre las apps y los backends |
| **Receivers → Processors → Exporters** | "**RePE**": **Re**cibe, **P**rocesa, **E**xporta | Las 3 etapas, en orden |
| **Connector** | El **mesero** entre cocinas | Une pipelines y **cambia de señal** (trazas → métricas) |
| `memory_limiter` | 🚪 El **portero** (1.º siempre) | Rechaza si no hay memoria → **backpressure** |
| `filter` | 🧹 El **colador** (2.º) | Bota DEBUG y health checks |
| `redaction` | ✏️ El **redactor** que tacha (3.º) | Enmascara cédulas y tarjetas |
| `tail_sampling` | ⚖️ El **juez** (4.º): sentencia **al final** | Decide qué trazas guardar viendo la traza completa |
| `batch` | 📦 El **empacador** (último) | Agrupa antes de enviar |
| `spanmetrics` | El mesero que **cuenta todos los platos** antes del juez | Span → metrics: métricas RED exactas antes del muestreo |
| `count` | Hermano de `spanmetrics` para logs | Log-to-Metrics |
| **Agente / Gateway** | El de cada nodo / el central | Agente (DaemonSet): metadatos y logs locales. Gateway: muestreo, PII, enrutamiento |
| **Gateway de dos capas** + `loadbalancing` | La **recepcionista** que sienta a toda la familia (traceID) en la misma mesa | Capa 1 enruta por `traceID`; capa 2 hace `tail_sampling` |
| **OpenTelemetry Operator** | El que **opera** OTel en Kubernetes (nombre literal) | Inyecta auto-instrumentación con una anotación |
| **Head / Tail sampling** | Perro: **cabeza** = inicio, **cola** = final | Head: barato, pierde errores. Tail: guarda errores, necesita memoria |
| **OTLP** | El idioma nativo de OTel | Puertos **4317** (gRPC) y **4318** (HTTP) |
| **Traza / span** | Envío completo / cada tramo | Una traza (`traceID`) contiene muchos spans |
| **SpanKind** | Dos parejas y un solitario | SERVER↔CLIENT, PRODUCER↔CONSUMER, INTERNAL |
| **p99** | 1 de cada 100 clientes espera más que esto | Percentil: nunca se promedia; se calcula con histogramas |
| `traceparent` | **trace + parent** = "el **papá** de la traza" | Header W3C: `00-traceID-parentID-01` |
| **W3C / B3** | Estándar oficial / el viejo de Zipkin ("**B**ig **B**rother **B**ird") | Formatos de propagación de contexto |
| **Kafka / MQ** | Una **carta con sobre** | El `traceparent` va en el **sobre** (headers del mensaje); el consumidor usa un **span link** |
| **Explosión de cardinalidad** | Un **cajón nuevo** por cada valor distinto | Nunca IDs únicos en etiquetas de métricas |
| **AS400 (IBM i)** | El corazón viejo pero confiable | Servidor de IBM donde vive el core bancario |
| **IBM MQ** | Como SQS, pero de banco | Cola de mensajes con entrega garantizada |

## Bloque C — Telemetría para IA

| Nombre | Imagen | Qué es |
|---|---|---|
| **Semantic Conventions** | *Semántica* = **significado** | Mismos nombres de atributos en todo el banco |
| **Resource attributes** | La cédula del servicio | `service.name`, `service.version`, `deployment.environment.name`, equipo |
