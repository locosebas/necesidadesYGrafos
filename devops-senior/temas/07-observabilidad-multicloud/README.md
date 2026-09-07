# Observabilidad: Azure Monitor, CloudWatch, Cloud Monitoring/Logging

Ya tenés Prometheus/Grafana — el modelo mental de "métricas + logs + alertas"
ya lo tenés. Acá es mapearlo al stack nativo de cada nube.

## Objetivos

- Mapear conceptos: métricas, logs, trazas distribuidas (APM) — cómo se llama
  cada pieza en cada nube.
- Escribir queries básicas en el lenguaje de consulta de logs de cada una.
- Diseñar alertas basadas en métricas y en queries de logs.
- Tracing distribuido entre microservicios (relevante si combinás serverless + contenedores).

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Paraguas general | Azure Monitor | Amazon CloudWatch | Google Cloud Observability (ex-Stackdriver) |
| Almacén de logs consultable | Log Analytics Workspace | CloudWatch Logs (+ Logs Insights para queries) | Cloud Logging |
| Lenguaje de consulta | **KQL** (Kusto Query Language) | **CloudWatch Logs Insights QL** | **Logging query language** (similar a Cloud Logging filters) |
| APM / tracing distribuido | Application Insights | AWS X-Ray | Cloud Trace |
| Alertas | Metric alerts / Log query alerts + Action Groups | CloudWatch Alarms + SNS | Cloud Monitoring Alerting Policies + Notification Channels |
| Dashboards | Azure Workbooks / Dashboards | CloudWatch Dashboards | Cloud Monitoring Dashboards |

## Subtemas

1. Diagnostic settings (Azure) / CloudWatch Logs subscription (AWS) / Log Router sinks (GCP) — cómo enrutar logs de cualquier recurso al almacén central
2. KQL básico (`where`, `summarize`, `join`, `render`) — el más usado en la vacante de Julieta
3. Sampling en APM (por qué no se traza el 100% de requests en alto volumen)
4. Costos: retención y volumen de logs como palanca de costo en las tres nubes
5. OpenTelemetry como capa de instrumentación neutral (exportable a las tres)

## Recursos

- Azure Monitor: https://learn.microsoft.com/azure/azure-monitor/overview
- KQL quick reference: https://learn.microsoft.com/azure/data-explorer/kql-quick-reference
- Amazon CloudWatch: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
- Google Cloud Observability: https://cloud.google.com/stackdriver/docs

## Lab sugerido

Sobre el mismo servicio desplegado en el lab del tema 02 (Container Apps y
Cloud Run), activá la observabilidad nativa de cada nube, generá tráfico, y
escribí una query equivalente en KQL y en el lenguaje de Cloud Logging:
"requests con error 5xx en la última hora".

## Autoevaluación

Pedime: *"Dame un examen de observabilidad multi-cloud (Monitor/CloudWatch/Cloud Logging) nivel senior"*.
