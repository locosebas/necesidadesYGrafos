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
| **Métricas / trazas / logs** | **Qué** pasa / **dónde** / **por qué** | Las tres señales; no compiten, se encadenan |
| **Exemplars** | Un **ejemplar** de muestra, como el de una revista | Punto en la métrica con un `trace_id`: clic del pico a la traza |
| `servicegraph` | El mesero que **dibuja el mapa** | Connector: arma aristas desde parejas CLIENT→SERVER (y nodos virtuales para DB/AS400) |
| **Regla de causa raíz** | El trancón termina donde la calle está libre | El nodo anómalo **más profundo** cuyas dependencias están sanas. El que más grita es víctima |
| **Dos causas a la vez** | Sospecha de lo compartido | Buscar una dependencia oculta (mismo nodo, red, Kafka, certificado) |
| **BFS / DFS** | **B**road: piedra en el lago / **D**eep: laberinto | BFS por niveles → radio de explosión (grafo invertido). DFS al fondo → causa raíz |
| **Servidor MCP de observabilidad** | El embudo | `obtener_grafo`, `consultar_slo`, `buscar_trazas`, `buscar_logs(trace_id)`, **`cambios_recientes`** |
| **Indirect Prompt Injection** | La orden escondida en los datos (OWASP LLM01) | Defensas: mínimo privilegio, **humano en el bucle**, datos marcados como no confiables, hooks + auditoría |

## Bloque D — Incidentes y cultura

| Nombre | Imagen | Qué es |
|---|---|---|
| **Roles del incidente** | "El **comandante** manda, el **operador** opera, el **comunicador** informa, el **escriba** anota" | Incident Commander (no toca teclado), Operations Lead, Communications Lead, Scribe (+ SMEs) |
| **Mitigar antes de diagnosticar** | El jefe de bomberos no coge la manguera | Primero detener el sangrado (rollback, flag, failover); el porqué después |
| **Circuit Breaker** | El **taco** del tablero eléctrico | Cerrado → abierto (fallback) → semi-abierto (prueba). Evita fallas en cascada |
| **Load Shedding / Bulkhead** | **Deslastre de carga** (racionamiento) / **mamparos** del barco | Cortar lo no crítico (saldos) para salvar lo crítico (pagos) / aislar recursos |
| **Graceful degradation** | Tu "bypass" de la tubería | Servicio de menor calidad en vez de parar. El fallback de antifraude lo decide **Riesgo** |
| **Post-mortem blameless** | Se cuenta **qué** pasó, no **quién** | Impacto, línea de tiempo (MTTD/MTTR), causa raíz, factores contribuyentes, acciones prevenir/detectar/mitigar |
| **Timeouts largos** | Más timeout ≠ más capacidad | Un timeout largo agota hilos y propaga la falla en cascada (Ley de Little) |
| **Toil** | **T**areas **O**perativas **I**dénticas y **L**ineales | Manual, repetitivo, automatizable. Meta Google: **< 50%** del tiempo |
| **"You build it, you run it"** | Cada Tribu cuida a sus hijos | Las Tribus atienden sus SLOs; observabilidad solo si falla la plataforma |
| **Chaos Engineering** | Un **mono** suelto desconectando cables (**Chaos Monkey**) | Inyectar fallas controladas; se practica en **Game Days** (el partido amistoso) |
| **Carga vs. caos** | Mucho tráfico vs. cosas rotas | Load testing (k6, JMeter) mide capacidad; Chaos (LitmusChaos, Chaos Mesh, AWS FIS) mide resiliencia |

## Bloque E — Temas aledaños

| Nombre | Imagen | Qué es |
|---|---|---|
| **Idempotency Key** | Una clave por cada intención de pago | El reintento devuelve el mismo resultado sin cobrar dos veces |
| **Retry Storm / Thundering Herd** | La **estampida** de búfalos | Todos reintentan a la vez y vuelven a tumbar el servicio |
| **Exponential Backoff + Jitter** | La salida escalonada del estadio | Esperas crecientes (1, 2, 4, 8 s) con azar para no sincronizarse |
| **RTO / RPO** | Videojuego: cuánto tarda en **cargar** / qué tan vieja es la **partida guardada** | **T**iempo de recuperación / **P**unto de datos perdidos. Pagos: RPO ≈ 0 |
| **Estrategias DR** | De barato a caro | Backup & Restore → Pilot Light → Warm Standby → Activo-activo |
| **Percentiles** | Nunca se promedian (ni ponderados) | Usar **Histogram** (cajones que se suman); **Summary** no se agrega |
| **Ley de Little** | La fila del banco | **L = λ × W**: si la latencia ×4, la concurrencia ×4 con el mismo tráfico |
| **Seguridad de la plataforma** | Tres capas | Datos sin PII; pipeline con mTLS, receivers autenticados, secretos en Key Vault; acceso con SSO, RBAC, auditoría (Zero Trust) |
| **Ley 1581 de 2012** | "1581: tu dato es tuyo" (Habeas Data) | Datos personales en Colombia; la vigila la **SIC** |
| **SFC / SIC** | Policía de los bancos / policía de los datos | SFC: ciberseguridad, nube, terceros |
| **ISO 27001 / SOC 2 / PCI DSS** | Certificados del proveedor / tarjetas | Exigir al SaaS; tarjeta: primeros 6 y últimos 4 |
| **Well-Architected (6 pilares)** | "**Seguro, Confiable, Rápido, Barato, Operable y Verde**" | Security, Reliability, Performance Efficiency, Cost Optimization, Operational Excellence, Sustainability |

## Repaso final (12 oct.)

| Nombre | Imagen | Qué es |
|---|---|---|
| **Error Budget Policy** | La **política de gastos de la casa** cuando se acaba la plata del mes | Reglas internas, firmadas con negocio, por umbral de presupuesto (no es el SLA) |
| **ArgoCD vs. Argo Rollouts** | **Qué** versión vs. **cómo** se reemplaza | ArgoCD = GitOps; Argo Rollouts = canary por etapas con `AnalysisTemplate` y rollback |
| **Flagger** | El **árbitro de línea** que levanta la bandera | Canary con análisis y rollback (con Istio/NGINX) |
| **Ventana móvil de 28 días** | Ventana que **se desliza**, no hoja que se arranca | Sin "reset" el día 1; 28 = 4 semanas exactas |
| **OTLP: 4317 / 4318** | Alfabeto: **g**RPC (17) antes que **h**TTP (18) | Puertos del protocolo nativo de OpenTelemetry |
| **Auditoría vs. telemetría** | Evidencia legal ≠ herramienta de operación | Pipeline de auditoría completo, nunca muestreado, inmutable (**WORM**: S3 Object Lock), retención legal |
| **Roles del incidente** | El **barco en tormenta**: capitán, jefe de máquinas, radio operador, bitácora | **Incident** Commander, Operations Lead, Communications Lead, **Scribe** (2 especiales + 2 Leads) |
| **5 porqués** | Una **cadena** vs. una **red** (grafo de factores) | Lineal y termina en una persona; complementar con factores contribuyentes y "¿qué lo hizo parecer razonable?" |
| **Modelo C4** | **País → ciudad → barrio → casa** (Google Maps) | **C**ontext, **C**ontainer (cualquier cosa desplegable, no Docker), **C**omponent, **C**ode. En la presentación: Context + Container |
