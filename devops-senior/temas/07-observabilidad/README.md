# Observabilidad: Azure Monitor, Application Insights, Log Analytics

Ya tenés Prometheus/Grafana — el modelo mental de "métricas + logs + alertas"
ya lo tenés. Acá es mapear ese modelo al stack nativo de Azure.

## Objetivos

- Explicar la relación entre los tres: **Azure Monitor** (paraguas general),
  **Log Analytics Workspace** (donde vive todo el log/telemetry data, consultable
  con KQL), **Application Insights** (APM sobre Log Analytics, para tracing de
  requests/dependencias/excepciones).
- Escribir queries KQL básicas (equivalente a lo que hoy hacés con PromQL/LogQL).
- Diseñar alertas basadas en métricas y en queries de logs.
- Distributed tracing con Application Insights (correlación de requests entre
  microservicios — relevante si hay Durable Functions + Container Apps).
- Dashboards y Workbooks.

## Subtemas

1. Log Analytics Workspace: tablas (`AppRequests`, `AppExceptions`, `ContainerAppConsoleLogs`, etc.)
2. KQL básico: `where`, `summarize`, `join`, `render`
3. Application Insights: instrumentación automática vs manual (SDK), sampling
4. Alertas: metric alerts vs log query alerts, action groups
5. Diagnostic settings: cómo enrutar logs de cualquier recurso Azure al workspace
6. Costos: por qué la retención y el volumen de logs importan en la factura

## Recursos

- Azure Monitor overview: https://learn.microsoft.com/azure/azure-monitor/overview
- Application Insights overview: https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview
- KQL quick reference: https://learn.microsoft.com/azure/data-explorer/kql-quick-reference

## Lab sugerido

Sobre el mismo Container App del lab de la carpeta 02, activá Application
Insights, generá tráfico, y escribí 3 queries KQL: requests con error 5xx en
la última hora, latencia p95 por endpoint, y top 5 excepciones.

## Autoevaluación

Pedime: *"Dame un examen de Azure Monitor / KQL nivel senior"*.
