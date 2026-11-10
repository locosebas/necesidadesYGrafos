# Diagramas C4 - Observabilidad y sus herramientas (entrevista Cardif)

Un diagrama C4 (Context, Containers, Components, Code) por idea. Están en Mermaid, así que GitHub los
dibuja directo. Los usa el [libreto](libreto-diapositivas.md) y el generador de la
[presentación](presentacion.html).

Convenciones de color (las del modelo C4):

- **Azul oscuro**: persona.
- **Azul medio**: sistema propio (la plataforma de observabilidad).
- **Azul claro**: contenedor (un paso del flujo, un servicio, un almacén).
- **Gris**: sistema externo (herramienta de terceros).
- **Recuadro punteado**: límite (capa, clúster, ambiente).

Íconos: cada `ico:nombre` es el logo de la herramienta, guardado en [iconos/](iconos/) (logos de
[Iconify](https://icon-sets.iconify.design/)). En GitHub se ven como texto; en la presentación HTML se
ven como logos.

---

## D1 · Contexto: la plataforma de observabilidad y quién la usa

Panorama. Tipo: Contexto.

```mermaid
flowchart LR
  cli["ico:account-group<br/>Clientes / asegurados<br/>cotizan, pagan, reclaman"]:::person
  sre["ico:account<br/>SRE / DevOps<br/>de guardia"]:::person
  dev["ico:account-group<br/>Equipos de desarrollo"]:::person
  apps["ico:kubernetes ico:server<br/>Aplicaciones<br/>pólizas, pagos, siniestros"]:::container
  obs["ico:opentelemetry-icon ico:grafana ico:datadog<br/>Plataforma de observabilidad<br/>métricas, logs, trazas"]:::system
  pag["ico:pagerduty-icon ico:opsgenie<br/>Gestión de incidentes<br/>on-call"]:::ext
  chat["ico:microsoft-teams ico:slack-icon<br/>Chat del equipo"]:::ext
  cli -->|"usan"| apps
  apps -->|"emiten telemetría"| obs
  obs -->|"alerta cuando se rompe el SLO"| pag
  pag -->|"llama / notifica"| sre
  obs -.->|"avisos"| chat
  sre -->|"investiga: dashboards, trazas, logs"| obs
  dev -->|"instrumenta y consulta"| obs
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D2 · Contenedores: las señales de telemetría (MELT)

Panorama. Tipo: Contenedores.

```mermaid
flowchart LR
  app["ico:server<br/>Servicio<br/>ej. API de pagos"]:::system
  subgraph melt["Señales · MELT"]
    m["ico:chart-line<br/>Metrics · métricas<br/>números en el tiempo<br/>¿QUÉ pasa y cuánto?"]:::container
    e["ico:bell-ring<br/>Events · eventos<br/>deploys, cambios<br/>¿QUÉ cambió?"]:::container
    l["ico:file-document-multiple<br/>Logs · registros<br/>texto con detalle<br/>¿POR QUÉ falló?"]:::container
    t["ico:transit-connection-variant<br/>Traces · trazas<br/>recorrido de una petición<br/>¿DÓNDE se demora?"]:::container
  end
  app --> m
  app --> e
  app --> l
  app --> t
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D3 · Dinámico: los 6 pasos del flujo de telemetría

Panorama. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  p1["ico:opentelemetry-icon<br/>1 · Instrumentar<br/>SDK / agente"]:::container
  p2["ico:fluentbit<br/>2 · Recolectar<br/>Collector / agentes"]:::container
  p3["ico:database<br/>3 · Almacenar<br/>backends por señal"]:::container
  p4["ico:grafana<br/>4 · Visualizar<br/>dashboards"]:::container
  p5["ico:bell-ring<br/>5 · Alertar<br/>SLO y burn rate"]:::container
  p6["ico:account<br/>6 · Actuar<br/>incidente y postmortem"]:::container
  p1 -->|"1"| p2 -->|"2"| p3 -->|"3"| p4 -->|"4"| p5 -->|"5"| p6
  p6 -.->|"6 · mejora: nueva alerta,<br/>runbook, instrumentación"| p1
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
```

## D4 · Componentes: paso 1, instrumentar con OpenTelemetry

Paso 1. Tipo: Componentes.

```mermaid
flowchart LR
  subgraph svc["Servicio de pólizas (contenedor)"]
    code["ico:file-code<br/>Código de negocio"]:::container
    auto["ico:opentelemetry-icon<br/>Auto-instrumentación<br/>HTTP, BD, colas"]:::container
    man["ico:opentelemetry-icon<br/>Instrumentación manual<br/>spans y métricas de negocio"]:::container
    sdk["ico:opentelemetry-icon<br/>OTel SDK<br/>resource: service.name,<br/>env, version"]:::container
  end
  col["ico:opentelemetry-icon<br/>OTel Collector"]:::ext
  code --> auto
  code --> man
  auto --> sdk
  man --> sdk
  sdk -->|"OTLP<br/>gRPC 4317 / HTTP 4318"| col
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D5 · Componentes: paso 2, el OpenTelemetry Collector

Paso 2. Tipo: Componentes (pipeline del Collector).

```mermaid
flowchart LR
  subgraph colr["OpenTelemetry Collector (agente DaemonSet + gateway)"]
    r["ico:opentelemetry-icon<br/>Receivers<br/>otlp, prometheus,<br/>filelog"]:::container
    p["ico:shield-check<br/>Processors<br/>batch, memory_limiter,<br/>filtro de PII, sampling"]:::container
    x["ico:opentelemetry-icon<br/>Exporters<br/>a uno o varios backends"]:::container
  end
  apps["ico:server<br/>Apps (OTLP)"]:::ext
  logs["ico:fluentbit<br/>Logs de nodos<br/>Fluent Bit"]:::ext
  b1["ico:prometheus<br/>Métricas"]:::ext
  b2["ico:elasticsearch<br/>Logs"]:::ext
  b3["ico:jaeger<br/>Trazas"]:::ext
  b4["ico:datadog<br/>o un SaaS"]:::ext
  apps --> r
  logs --> r
  r --> p --> x
  x --> b1
  x --> b2
  x --> b3
  x -.-> b4
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D6 · Contenedores: paso 3, dónde se guarda cada señal

Paso 3. Tipo: Contenedores.

```mermaid
flowchart LR
  col["ico:opentelemetry-icon<br/>Collector"]:::system
  subgraph st["Almacenamiento por señal"]
    m["ico:prometheus<br/>Métricas<br/>Prometheus + Thanos /<br/>Mimir (largo plazo)"]:::container
    l["ico:elasticsearch<br/>Logs<br/>Elasticsearch u<br/>OpenSearch · Loki"]:::container
    t["ico:jaeger<br/>Trazas<br/>Jaeger · Tempo"]:::container
  end
  obj["ico:database<br/>Object storage<br/>S3 / Blob<br/>retención barata"]:::ext
  col --> m
  col --> l
  col --> t
  m -.-> obj
  l -.-> obj
  t -.-> obj
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D7 · Componentes: paso 4, un dashboard útil

Paso 4. Tipo: Componentes (filas de un dashboard).

```mermaid
flowchart TB
  subgraph dash["ico:grafana Dashboard del servicio de pagos"]
    f1["ico:speedometer<br/>Fila 1 · SLO<br/>disponibilidad y error budget"]:::container
    f2["ico:chart-line<br/>Fila 2 · RED<br/>Rate, Errors, Duration (p95, p99)"]:::container
    f3["ico:server<br/>Fila 3 · USE<br/>Utilization, Saturation, Errors<br/>CPU, memoria, pods"]:::container
    f4["ico:bell-ring<br/>Fila 4 · Eventos<br/>anotaciones de deploys"]:::container
  end
  f1 --> f2 --> f3 --> f4
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
```

## D8 · Dinámico: paso 5, de SLI a la alerta

Paso 5. Tipo: Dinámico.

```mermaid
flowchart LR
  sli["ico:chart-line<br/>1 · SLI<br/>% de pagos OK<br/>en menos de 2 s"]:::container
  slo["ico:speedometer<br/>2 · SLO<br/>99,9 % en 30 días"]:::container
  eb["ico:timer-sand<br/>3 · Error budget<br/>0,1 % ≈ 43 min/mes"]:::container
  br["ico:alert<br/>4 · Burn rate<br/>¿qué tan rápido<br/>se gasta?"]:::container
  am["ico:prometheus<br/>5 · Alertmanager<br/>agrupa, silencia,<br/>enruta"]:::ext
  pd["ico:pagerduty-icon ico:opsgenie<br/>6 · On-call<br/>página a la persona"]:::ext
  sli --> slo --> eb --> br --> am --> pd
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D9 · Dinámico: paso 6, el ciclo del incidente

Paso 6. Tipo: Dinámico.

```mermaid
flowchart LR
  a["ico:bell-ring<br/>1 · Detectar<br/>alerta"]:::container
  b["ico:account<br/>2 · Triage<br/>severidad, impacto"]:::container
  c["ico:book-open-variant<br/>3 · Runbook<br/>mitigar primero"]:::container
  d["ico:swap-horizontal<br/>4 · Mitigar<br/>rollback, escalar"]:::container
  e["ico:file-document-multiple<br/>5 · Postmortem<br/>sin culpables"]:::container
  f["ico:check-decagram<br/>6 · Acciones<br/>alertas, pruebas"]:::container
  a --> b --> c --> d --> e --> f
  f -.->|"MTTD y MTTR bajan"| a
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
```

## D10 · Dinámico: correlación con trace_id en 5 microservicios

Correlación. Tipo: Dinámico.

```mermaid
flowchart LR
  u["ico:account<br/>Cliente<br/>paga la póliza"]:::person
  gw["ico:server<br/>1 · API Gateway<br/>trace_id=abc123"]:::container
  pol["ico:server<br/>2 · Pólizas<br/>span 40 ms"]:::container
  pag["ico:server<br/>3 · Pagos<br/>span 3 200 ms ⚠"]:::container
  ban["ico:server<br/>4 · Pasarela bancaria<br/>(externa)"]:::ext
  not["ico:server<br/>5 · Notificaciones<br/>span 15 ms"]:::container
  j["ico:jaeger<br/>Traza completa:<br/>la demora está en Pagos"]:::system
  lg["ico:elasticsearch<br/>Logs filtrados por<br/>trace_id=abc123:<br/>timeout con el banco"]:::system
  u --> gw --> pol --> pag --> ban
  pag --> not
  pag -.-> j
  j -.->|"del span salto al log"| lg
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D11 · Contexto: las tres familias de herramientas

Herramientas. Tipo: Contexto.

```mermaid
flowchart TB
  otel["ico:opentelemetry-icon<br/>OpenTelemetry<br/>estándar abierto: instrumentas una vez<br/>y cambias de backend"]:::system
  subgraph os["Open source (lo administras tú)"]
    o1["ico:prometheus ico:grafana<br/>Prometheus + Grafana<br/>stack LGTM: Loki, Grafana,<br/>Tempo, Mimir"]:::container
    o2["ico:elasticsearch ico:kibana<br/>ELK / EFK<br/>Elasticsearch, Logstash o<br/>Fluent Bit, Kibana"]:::container
  end
  subgraph saas["SaaS (pagas por volumen)"]
    s1["ico:datadog<br/>Datadog"]:::ext
    s2["ico:dynatrace-icon<br/>Dynatrace"]:::ext
    s3["ico:new-relic-icon<br/>New Relic"]:::ext
    s4["ico:splunk<br/>Splunk"]:::ext
  end
  subgraph nat["Nativas de la nube"]
    n1["ico:aws-cloudwatch<br/>AWS CloudWatch<br/>+ X-Ray"]:::ext
    n2["ico:microsoft-azure<br/>Azure Monitor<br/>+ Application Insights<br/>+ Log Analytics"]:::ext
  end
  otel --> os
  otel --> saas
  otel --> nat
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D12 · Despliegue: observabilidad dentro de Kubernetes

Kubernetes. Tipo: Despliegue.

```mermaid
flowchart LR
  subgraph k8s["ico:kubernetes Clúster Kubernetes (AKS / EKS)"]
    subgraph nodo["Cada nodo"]
      ds["ico:opentelemetry-icon ico:fluentbit<br/>DaemonSet: Collector<br/>agente / Fluent Bit"]:::container
      ne["ico:prometheus<br/>node-exporter<br/>CPU, disco, red"]:::container
      pods["ico:docker-icon<br/>Pods de la app<br/>/metrics + OTLP"]:::container
    end
    ksm["ico:prometheus<br/>kube-state-metrics<br/>estado de deployments,<br/>pods, réplicas"]:::container
    prom["ico:helm ico:prometheus<br/>kube-prometheus-stack<br/>Prometheus Operator +<br/>ServiceMonitor"]:::system
    gf["ico:grafana<br/>Grafana"]:::system
  end
  pods --> ds
  pods -->|"scrape"| prom
  ne --> prom
  ksm --> prom
  prom --> gf
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
```

## D13 · Componentes: observabilidad en una aseguradora regulada

Industria. Tipo: Componentes.

```mermaid
flowchart LR
  app["ico:server<br/>Servicio de siniestros"]:::system
  subgraph ctl["Controles antes y después de guardar"]
    pii["ico:incognito<br/>Enmascarar PII<br/>cédula, tarjeta, diagnóstico<br/>en el Collector"]:::container
    rbac["ico:lock<br/>RBAC y SSO<br/>quién ve qué logs"]:::container
    ret["ico:timer-sand<br/>Retención<br/>caliente 15 días ·<br/>archivo según norma"]:::container
    cost["ico:currency-usd<br/>Costo<br/>cardinalidad, sampling,<br/>niveles de log"]:::container
  end
  aud["ico:shield-check<br/>Auditoría<br/>logs de acceso inmutables"]:::ext
  app --> pii --> rbac
  rbac --> ret
  ret --> cost
  rbac -.-> aud
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D14 · Dinámico: IA aplicada a observabilidad (mi caso en MercadoLibre)

Experiencia. Tipo: Dinámico.

```mermaid
flowchart LR
  tk["ico:bell-ring<br/>1 · Ticket /<br/>incidente"]:::container
  ag["ico:anthropic-icon<br/>2 · Agente con LLM<br/>harness + hooks<br/>solo lectura"]:::system
  mcp["ico:robot<br/>3 · Servidor MCP<br/>diseñado con el<br/>equipo de o11y"]:::container
  emb["ico:grafana ico:datadog<br/>4 · Embudo: dependencias →<br/>métricas → trazas → logs"]:::ext
  dx["ico:file-document-multiple<br/>5 · Diagnóstico con<br/>certezas e incertidumbres"]:::container
  hum["ico:account<br/>6 · Humano en el bucle<br/>aprueba la acción"]:::person
  tk --> ag --> mcp --> emb
  emb --> dx --> hum
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```
