# Fórmula 05 — Observabilidad de cero a que funcione

**Resumen en una línea:** *definir SLIs/SLOs → instrumentar (métricas, logs,
trazas con OpenTelemetry) → recolectar y guardar → dashboards → alertas sobre
síntomas → runbooks y on-call → mejorar con postmortems.*

---

## Los conceptos que tenés que decir

- **3 pilares**: métricas (¿qué pasa?), logs (¿por qué?), trazas (¿dónde?).
- **Golden signals** (Google SRE): latencia, tráfico, errores, saturación.
- **RED** para servicios: Rate, Errors, Duration.
- **USE** para recursos: Utilization, Saturation, Errors.
- **SLI** = medida (ej: % de requests con respuesta < 300 ms y sin 5xx).
  **SLO** = objetivo (99,9% en 30 días). **SLA** = contrato con penalidad.
  **Error budget** = 100% − SLO (0,1% ≈ 43 min/mes) → si se gasta, se frena
  el deploy de features y se prioriza confiabilidad.

## Paso 1 — Definir qué importa

Por cada servicio: 1–3 SLIs orientados al usuario (disponibilidad, latencia
p95/p99, frescura de datos para batch). Acordarlos con producto.

## Paso 2 — Instrumentar

- **OpenTelemetry** SDK en la app (auto-instrumentación de FastAPI, HTTP, DB).
- Logs **estructurados en JSON** con `trace_id`, `request_id`, nivel, servicio.
  Sin datos personales/secretos en logs.
- Métricas de negocio (pagos procesados, órdenes por minuto).

## Paso 3 — Recolectar y almacenar

| Pilar | Open source | Azure | AWS | GCP |
|---|---|---|---|---|
| Métricas | Prometheus / Mimir | Azure Monitor Metrics / Managed Prometheus | CloudWatch / Amazon Managed Prometheus | Cloud Monitoring / Managed Prometheus |
| Logs | Loki / ELK / OpenSearch | **Log Analytics** (KQL) | CloudWatch Logs | Cloud Logging |
| Trazas | Tempo / Jaeger | **Application Insights** | X-Ray / CloudWatch Application Signals | Cloud Trace |
| Dashboards | **Grafana** | Workbooks / Managed Grafana | CloudWatch Dashboards / Managed Grafana | Cloud Monitoring dashboards |

- **OTel Collector** como agente central: recibe y exporta al backend que sea
  (evita lock-in).
- Retención por tipo (logs de debug 7 días, auditoría 1+ año, tier frío para archivo).

## Paso 4 — Dashboards

- Uno por servicio con RED + SLO + error budget restante.
- Uno de plataforma (nodos, clúster, colas, bases).
- Enlazar dashboard → logs → traza (correlación por `trace_id`).

## Paso 5 — Alertas

- Alertar **sobre síntomas que siente el usuario** (SLO en riesgo), no sobre
  "CPU al 80%".
- **Burn rate alerts**: page si se consume el error budget muy rápido
  (ej: 2% del presupuesto mensual en 1 hora); ticket si es lento.
- Cada alerta: **accionable**, con severidad, dueño y **link al runbook**.
- Ruteo: PagerDuty / Opsgenie / Teams / Slack. Evitar la fatiga de alertas.

## Paso 6 — Operación

- On-call con rotación, escalamiento, runbooks.
- **Postmortems blameless** con acciones concretas.
- Synthetic monitoring (chequeos externos) + alertas de certificados por vencer.

## Prueba "funciona"

Genero tráfico → veo la request en el dashboard → abro su traza → salto a los
logs con el mismo `trace_id` → inyecto errores 5xx → se dispara la alerta de
burn rate → llega al canal de on-call con el runbook.
