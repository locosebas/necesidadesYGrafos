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

## Herramientas externas (third-party) — el otro medio del mercado

Muchas ofertas piden el stack nativo de la nube **más** una herramienta
externa. Ya conocés **Prometheus** + **Grafana** (tu fortaleza) — el resto,
ventaja principal de cada una:

| Herramienta | Qué es | Ventaja principal |
|---|---|---|
| **Prometheus** | Motor de métricas open-source, *pull-based* (él va a buscar las métricas, no se las mandan) | Estándar de facto en Kubernetes; **PromQL** es el lenguaje que también hablan muchas herramientas cloud-native |
| **Grafana** | Capa de dashboards open-source, se conecta a Prometheus, **Loki** (logs), **Tempo** (traces), y también a Azure Monitor/CloudWatch/Cloud Monitoring | Mejores dashboards del mercado, self-hosteable, evita *vendor lock-in* |
| **Datadog** | Plataforma SaaS todo-en-uno (infra + APM + logs + RUM) | +800 integraciones listas, UX pulida, "un solo panel para todo" — pero el precio escala rápido (por host + por GB) |
| **New Relic** | Similar a Datadog, uno de los pioneros del **APM** | Full-stack observability, tier gratuito históricamente generoso |
| **Splunk** | Analítica de logs de nivel enterprise, lenguaje propio **SPL** | Muy usado en seguridad/SOC y compliance; potentísimo pero caro ("el impuesto Splunk", un chiste común en la industria) |
| **Elastic Stack / ELK** (Elasticsearch + Logstash + Kibana) | Motor de búsqueda full-text aplicado a logs | Mejor para búsqueda de logs a gran volumen; self-hosteable, pero pide más esfuerzo operativo |
| **Dynatrace** | APM enterprise con IA propia ("Davis AI") | Auto-instrumentación y causa-raíz automática — apunta a "no configures nada, la IA te dice qué falló" |
| **Honeycomb** | Pionero del concepto moderno de "**observability**" (distinto de "monitoring") | Foco en *high-cardinality* y debugging exploratorio de sistemas distribuidos — más orientado a *engineers*, menos a dashboards fijos |
| **OpenTelemetry (OTel)** | No es una herramienta, es el **estándar** neutral de instrumentación (CNCF) | Instrumentás tu app UNA vez con OTel y podés exportar a Datadog, Grafana, New Relic, Azure Monitor, etc. sin reescribir código — es lo que evita quedar atado a un solo proveedor |

**Dato de color:** *Prometheus* nació en SoundCloud (2012), inspirado en un
sistema interno de Google llamado *Borgmon* — el mismo linaje de donde salió
después *Azure Monitor for containers* y buena parte del monitoreo moderno de
Kubernetes. Y el término *"observability"* no lo inventó la industria del
software: viene de la teoría de control (*control theory*) de los años 60,
del ingeniero húngaro-estadounidense Rudolf Kálmán — mucho antes de que
existieran los contenedores.

## Lab sugerido

Sobre el mismo servicio desplegado en el lab del tema 02 (Container Apps y
Cloud Run), activá la observabilidad nativa de cada nube, generá tráfico, y
escribí una query equivalente en KQL y en el lenguaje de Cloud Logging:
"requests con error 5xx en la última hora".

## Autoevaluación

Pedime: *"Dame un examen de observabilidad multi-cloud (Monitor/CloudWatch/Cloud Logging) nivel senior"*.

