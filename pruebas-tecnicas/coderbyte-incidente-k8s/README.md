# Prueba técnica en Coderbyte: incidente en Kubernetes

Prueba presentada en la plataforma **Coderbyte** el 4 nov 2026. Caso abierto: plan de respuesta a un
incidente en Kubernetes con OOMKilled después de un despliegue de Jenkins, correlación entre Dynatrace,
Splunk y OpenTelemetry, criterios de rollback y seguimiento del Error Budget. Además, preguntas cortas
de diagnóstico (trazas distribuidas, I/O wait en RHEL).

| Archivo | Contenido |
|---|---|
| [solucion.md](solucion.md) | Respuesta del caso abierto (versión del repo, con tablas) |
| [preguntas-adicionales.md](preguntas-adicionales.md) | Las preguntas cortas de la misma prueba, con su respuesta |

## Lecciones sobre el formato en Coderbyte

- La caja de respuesta de Coderbyte acepta texto con formato de código. La versión que se entregó fue la
  de títulos, negritas, listas y **un bloque de código por cada comando, consulta o pseudocódigo**,
  copiada como texto crudo (Markdown) en un solo bloque.
- Evitar tablas de Markdown en la entrega: se cambiaron por listas o por tablas alineadas dentro de un
  bloque de texto.

## Nombres clave para repasar

- **Kubernetes:** OOMKilled (exit code 137) vs. Evicted / MemoryPressure, `kubectl logs --previous`,
  `kubectl rollout history` / `rollout undo`, `kubectl debug node/`, readiness vs. liveness probe, VPA (Vertical Pod Autoscaler).
- **Linux:** OOM killer, `dmesg -T`, cgroup v2 (`memory.current`, `memory.max`, `memory.events`),
  estado `D` (uninterruptible sleep), I/O wait, `iostat -x`, `vmstat`.
- **Observabilidad:** Davis AI y PurePath (Dynatrace), SPL (Search Processing Language) en Splunk,
  distributed tracing, span, context propagation (`traceparent`), tail-based sampling, `trace_id` en los
  logs, atributo `service.version` de OpenTelemetry, evento de despliegue (Events API v2).
- **SRE:** burn rate, alertas multi-window multi-burn-rate (14,4x / 6x / 1x), política de Error Budget,
  postmortem blameless, MTTD / MTTR, soak test, canary con rollback automático.
