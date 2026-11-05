# Caso: incidente de confiabilidad y observabilidad en Kubernetes

Preparación para una prueba técnica (4 nov 2026): plan de respuesta a un incidente en Kubernetes con
OOMKilled después de un despliegue de Jenkins, correlación entre Dynatrace, Splunk y OpenTelemetry,
criterios de rollback y seguimiento del Error Budget. Solución: [solucion.md](solucion.md).

## Nombres clave para repasar

- **Kubernetes:** OOMKilled (exit code 137) vs. Evicted / MemoryPressure, `kubectl logs --previous`,
  `kubectl rollout history` / `rollout undo`, `kubectl debug node/`, readiness vs. liveness probe, VPA (Vertical Pod Autoscaler).
- **Linux:** OOM killer, `dmesg -T`, cgroup v2 (`memory.current`, `memory.max`, `memory.events`).
- **Observabilidad:** Davis AI y PurePath (Dynatrace), SPL (Search Processing Language) en Splunk,
  `trace_id` en los logs, atributo `service.version` de OpenTelemetry, evento de despliegue (Events API v2).
- **SRE:** burn rate, alertas multi-window multi-burn-rate (14,4x / 6x / 1x), política de Error Budget,
  postmortem blameless, MTTD / MTTR, soak test, canary con rollback automático.
