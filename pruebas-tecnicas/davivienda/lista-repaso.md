# Lista de repaso — sustentación Banco Plus

> Formato conversación: **una pregunta por vez**. Se describe el mecanismo y tú dices el **nombre**.
> Las listas (L) se recitan completas y sin pistas antes de recibir corrección.
> Orden: sigue el hilo de la presentación, empezando por los nombres que no salieron en los repasos.
> Escala: ⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior.

| # | Mecanismo que se describe | Nombre a recordar | Nivel |
|---|---|---|---|
| 1 | Acuerdo firmado con negocio: qué pasa con los despliegues según cuánto presupuesto de errores queda | Error Budget Policy | 🟡 (10-19: dijo "agreement", luego exacto) |
| 2 | Qué tan rápido se está gastando el presupuesto frente a lo sostenible (y el umbral de página en 1 h) | Burn rate (14,4×) | 🟢 (10-19: + 2% en 1 h) |
| 3 | Regla del environment de producción: una app de Plataforma aprueba o rechaza cada despliegue | Deployment protection rule | 🔴 (10-19: no salió; defensa con OIDC + `job_workflow_ref` + Terraform 8/10 con los nombres dados) |
| 4 | Automatiza el canary sobre un service mesh existente, sin tocar los Deployments | Flagger | 🟡 (10-19: no salió y lo confundió con feature flags; luego bien elegido frente a Argo Rollouts) |
| 5 | Automatiza el canary reemplazando el Deployment, sin exigir Argo CD | Argo Rollouts | 🟢 (10-19: sin pistas) |
| 6 | Cambiar el esquema de la base de datos sin romper el rollback: agregar, migrar, borrar | Expand/contract (+ dual write, backfill, CDC/trigger) | 🟡 (10-19: no salió; luego exacto. Buena pregunta propia sobre sincronizar columnas) |
| 7 | Componente del Collector que une pipelines y cambia de señal (spans → métricas) | Connector (`spanmetrics`) | 🔴 (10-19: nombre visto en la sugerencia; dijo processor y luego invirtió `redaction`/`count`; corregido con la imagen del gas: filtro = processor, planta gas→electricidad = connector) |
| 8 | El processor que va primero y protege al Collector de quedarse sin RAM | `memory_limiter` (+ backpressure) | 🟡 (10-19: describió "rechazo de carga por memoria"; luego nombre y por qué va primero bien) |
| 9 | Protocolo nativo de OpenTelemetry y sus dos puertos | OTLP (OpenTelemetry Protocol) — 4317 gRPC / 4318 HTTP | 🔴 |
| 10 | Inyecta la auto-instrumentación en Kubernetes con una anotación en el pod | OpenTelemetry Operator | 🔴 |
| 11 | Muestreo que decide al final de la traza y conserva los errores | Tail-based sampling | 🔴 |
| 12 | Exporter de la capa 1 que manda todos los spans de una traza a la misma réplica | `loadbalancing` (por traceID) | 🔴 |
| 13 | Header del W3C que lleva el ID de la traza entre servicios (y el formato viejo de Zipkin) | `traceparent` (W3C Trace Context); B3 | 🔴 |
| 14 | Una etiqueta de métrica con el número de cliente crea una serie por cliente | Explosión de cardinalidad | 🔴 |
| 15 | Convertir logs repetitivos en contadores para no pagar por cada línea | Log-to-Metrics | 🔴 |
| 16 | Convenciones para que todo el banco llame igual a lo mismo | Semantic Conventions | 🔴 |
| 17 | Un pico en una métrica guarda el ID de una traza de ejemplo | Exemplar | 🔴 |
| 18 | Lo nuevo crece alrededor de lo viejo y lo reemplaza por partes | Strangler fig | 🟡 |
| 19 | Instrucciones escondidas en un dato (log, descripción de transferencia) que la IA lee | Indirect prompt injection | 🟡 |
| 20 | Corta las llamadas a una dependencia que falla y las reabre de a poco (y sus estados) | Circuit breaker (cerrado/abierto/semi-abierto) | 🟡 |
| 21 | Rechazar a propósito parte del tráfico para que el resto sobreviva | Load shedding | 🟡 |
| 22 | Quien coordina el incidente y no arregla nada | Incident Commander | 🟡 |
| 23 | Cuánto tiempo puedo estar caído vs. cuántos datos puedo perder | RTO / RPO | 🔴 |
| 24 | Clave que manda el cliente para que un pago reintentado no se cobre dos veces | Idempotency key (+ backoff con jitter) | 🟡 |
| 25 | Trabajo manual, repetitivo, automatizable, que crece con el servicio | Toil | 🔴 |
| 26 | Ejercicio programado de caos con el equipo (no es prueba de carga) | Game Day | 🔴 |
| 27 | Herramienta que convierte un SLO en YAML en reglas de Prometheus | Sloth (spec: OpenSLO) | ⬜ |
| 28 | La nube entrega credenciales temporales solo a un token firmado con ciertos datos (sin llaves guardadas) | OIDC (OpenID Connect) | 🟡 |
| 29 | Dato del token OIDC que dice de qué plantilla de workflow viene el job | `job_workflow_ref` | 🔴 |
| 30 | Quien escribe el código no es quien autoriza ni ejecuta el paso a producción | Segregación de funciones (SoD) | 🟡 |
| 31 | Herramienta ITSM donde viven los cambios que aprueba el comité | ServiceNow; comité = CAB (Change Advisory Board) | 🟡 |
| 32 | Proxy que Istio pega al lado de cada pod | Envoy (sidecar) | 🟢 (10-19: lo recordó tras explicarlo) |
| 33 | Una sola versión desplegada; un interruptor decide la función por usuario (≠ canary) | Feature flag (Flipt, LaunchDarkly) | 🟢 |

## Listas de recitación estricta

| # | Lista | Nivel |
|---|---|---|
| L1 | Las 10 preguntas de la presentación, en orden | ⬜ |
| L2 | Los 4 ejes del caso | ⬜ |
| L3 | Las 5 reglas del libreto | ⬜ |
| L4 | Las 4 Golden Signals | 🟡 |
| L5 | Las 4 métricas DORA | 🔴 (0/4 dos veces) |
| L6 | Los 4 niveles del modelo C4 | ⬜ |
| L7 | Las 5 herramientas del servidor MCP | 🟡 |
| L8 | Los 4 hitos de la hoja de ruta | ⬜ |

Las respuestas largas están en [ruta-sustentacion.md](ruta-sustentacion.md) y [chuleta-nombres.md](chuleta-nombres.md).
Al cerrar cada tanda, actualizar la columna Nivel aquí y en `../../devops-senior/examenes/registro/progreso.md`.
