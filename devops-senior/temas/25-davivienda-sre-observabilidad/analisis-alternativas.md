# Análisis de alternativas — decisiones del libreto (borrador v1)

> El libreto (`presentacion-libreto.md`) tomó decisiones sin discutirlas. Aquí está cada una con lo que
> se escogió, las alternativas, el trade-off (qué ganas y qué pierdes) y una recomendación.
> La columna **Tu decisión** queda vacía a propósito: se llena en sesión, **de a una decisión por vez**.
>
> Criterio general de la recomendación: el caso premia **viabilidad y pragmatismo**, y la mesa incluye
> DevSecOps (soberanía del dato) y Arquitectura (neutralidad frente al proveedor). Por eso pesa más lo
> estándar y abierto que lo "más potente".

---

## Componente económico: supuestos y escala

Cada decisión tiene una fila **Costo**. Son **órdenes de magnitud** para comparar alternativas, no
cotizaciones: precios de lista públicos aproximados en USD (2025–2026), que cambian y se negocian
(un banco casi nunca paga lista). **Verificar antes de citar una cifra exacta ante la mesa**; lo seguro
es hablar en **valores relativos** ("el SaaS cuesta 3–5× más por GB que el autogestionado").

**Escala relativa** (costo recurrente):

| Símbolo | Rango aproximado |
|---|---|
| ≈0 | Gratis o costo marginal despreciable (software abierto, cambio de configuración) |
| $ | < USD 1.000/mes |
| $$ | USD 1.000–10.000/mes |
| $$$ | USD 10.000–50.000/mes |
| $$$$ | > USD 50.000/mes |

**Supuestos de referencia** (ilustrativos, los mismos de la diapositiva 6):

- **Factura de observabilidad base: USD 100.000/mes**, repartida como en D17: logs 45 · trazas 35 · métricas 20.
  Equivale a unos ~3 TB/día de logs y ~2,3 TB/día de trazas a ~USD 0,50/GB ingerido, y ~3 millones de
  series activas de métricas. Con el −34% de D17, el ahorro sería **~USD 34.000/mes ≈ USD 400.000/año**.
- **Costo de personas: 1 FTE (Full-Time Equivalent, persona de tiempo completo) de ingeniería senior en
  Colombia ≈ USD 6.000/mes de costo empresa** (≈ COP 24 millones con TRM, Tasa Representativa del Mercado,
  de ~4.000; verificar la del día). El software abierto no tiene licencia, pero sí cuesta personas: esa es
  la comparación honesta frente al SaaS.
- **Precios de referencia por unidad** (lista, aproximados):

| Concepto | Precio aproximado |
|---|---|
| Ingesta de logs en SaaS (Grafana Cloud, CloudWatch, Cloud Logging) | ~USD 0,50/GB |
| Logs en Datadog | ~USD 0,10/GB ingerido + ~USD 1,70 por millón de eventos indexados (15 días) |
| APM (Application Performance Monitoring) de Datadog | ~USD 31–40 por host al mes |
| Métricas en Grafana Cloud | ~USD 6–8 por cada 1.000 series activas al mes |
| Almacenamiento de objetos (S3 / GCS) | ~USD 0,02/GB al mes (clases frías: 4–20× menos) |
| Tráfico de salida de la nube (egress a internet / a otra nube) | ~USD 0,08–0,12/GB |
| Tráfico entre regiones de la misma nube | ~USD 0,02/GB |
| Nodo de cómputo mediano (4 vCPU, 16 GB) | ~USD 120–150/mes |
| LLM (Large Language Model) de gama media vía Amazon Bedrock / Vertex AI | ~USD 3 por millón de tokens de entrada, ~USD 15 de salida |

- **Costo del minuto caído del pago QR** (para hablar del Error Budget en plata):
  `pagos por minuto × valor promedio × margen por transacción` + costo regulatorio y reputacional.
  En pagos inmediatos el dinero perdido directo suele ser pequeño (mucho cliente reintenta); lo caro es
  la **reputación**, el reporte a la SFC (Superintendencia Financiera de Colombia) y la fuga de clientes.
  Por eso conviene presentarlo como "minutos de Error Budget", no como pesos exactos.

---

## Eje 1 — SLOs, Error Budgets y Quality Gate

### D1. Valor del SLO de disponibilidad del pago QR
| | |
|---|---|
| Escogido | 99,9% en 30 días móviles (43,2 min/mes) |
| Alternativas | 99,95% (21,6 min) · 99,99% (4,32 min) · 99,5% (3,6 h) |
| Trade-off | 99,95% suena más "bancario", pero 3 dependencias en serie de 99,9% ya dan 99,7%: obliga a redundancia en todo. 99,9% es defendible como **punto de partida** que se ajusta con datos |
| Costo | Cada nueve adicional **multiplica** el costo de infraestructura y operación (regla práctica: ×2 a ×10 por nueve), porque obliga a redundancia en todas las dependencias, multi-zona o multi-región y on-call más exigente. 99,9% → 99,95% suele exigir activo-activo en dos zonas para todo ($$ a $$$ adicional); 99,99% casi siempre exige activo-activo **multi-región**, que puede duplicar la factura de cómputo y base de datos del servicio ($$$ a $$$$) y sumar 1–2 FTE de SRE. Pasar de 43,2 a 4,3 min/mes de presupuesto rara vez compensa ese gasto si el cliente reintenta |
| Recomendación | 99,9% y decir explícitamente "se calibra con 4 semanas de datos reales" |
| Tu decisión | |

### D2. Ventana del SLO
| | |
|---|---|
| Escogido | 30 días móviles |
| Alternativas | 28 días móviles (todas las ventanas con los mismos días de semana) · mes calendario |
| Trade-off | 28 días es más riguroso; 30 días hace la cuenta de 43,2 min más fácil de recordar. El mes calendario "resetea" el presupuesto el día 1 (mala práctica) |
| Costo | ≈0: es una decisión de configuración. Ningún costo diferencial entre 28 y 30 días |
| Recomendación | 30 días en la diapositiva; 28 como respuesta si preguntan |
| Tu decisión | |

### D3. SLI de latencia y dónde se mide
| | |
|---|---|
| Escogido | 99% de pagos confirmados en < 2 s, medido en el API Gateway |
| Alternativas | Umbral distinto (1 s, 3 s) · medir en el cliente con RUM (Real User Monitoring) desde la app · monitoreo sintético · medir en el balanceador de carga |
| Trade-off | API Gateway: fácil y confiable, pero no ve la red móvil del cliente. RUM: lo más centrado en el cliente, pero ruidoso (celulares y redes que no controlamos). Sintético: detecta caídas sin tráfico, pero no es tráfico real |
| Costo | API Gateway: ≈0 (las métricas ya existen). RUM (Real User Monitoring) en SaaS: $ a $$ (se cobra por sesión: del orden de USD 1–2 por cada 1.000 sesiones; con millones de sesiones al mes se vuelve $$). Monitoreo sintético: $ (centavos por ejecución; unas decenas de pruebas cada minuto ≈ cientos de USD/mes). Recomendación: muestrear el RUM (por ejemplo, 10% de las sesiones) para que no infle la factura que justamente queremos bajar |
| Recomendación | API Gateway para el SLO + RUM y sintético como señales complementarias (responde "customer centric" sin volver ruidoso el SLO) |
| Tu decisión | |

### D4. Umbrales de la Error Budget Policy
| | |
|---|---|
| Escogido | > 50% normal · 25–50% solo canary · < 25% congelado salvo fixes |
| Alternativas | Política binaria (queda presupuesto / no queda) · umbrales por burn rate en vez de presupuesto restante · congelar solo con presupuesto agotado (0%) |
| Trade-off | Tres zonas dan gradualidad pero son más difíciles de negociar con negocio. Binaria es simple pero brusca |
| Costo | ≈0 en herramientas. El costo real es de **oportunidad**: un congelamiento demora funcionalidades de negocio. Por eso las tres zonas son una conversación de plata con negocio: cada zona más estricta cambia velocidad por menos riesgo de minutos caídos |
| Recomendación | Tres zonas, presentadas como **propuesta para negociar con negocio**, no como verdad |
| Tu decisión | |

### D5. Herramienta para definir y calcular los SLOs
| | |
|---|---|
| Escogido | Ninguna nombrada ("la fuente de SLOs") |
| Alternativas | **Sloth** o **Pyrra** (generan reglas de Prometheus desde un YAML) · **OpenSLO** (especificación abierta) · Google **SLO Generator** · SaaS: **Nobl9**, SLOs de Datadog / Dynatrace / Grafana Cloud |
| Trade-off | Sloth/Pyrra: abiertos, "SLO como código" en Git, pero hay que operarlos. SaaS: listo rápido, pero amarra al proveedor y cuesta |
| Costo | Sloth / Pyrra / OpenSLO: licencia ≈0; operación ~0,1–0,2 FTE (≈ USD 600–1.200/mes) mientras se adopta. SaaS de SLOs: **Nobl9** es licencia empresarial (del orden de decenas de miles de USD al año, $$); los SLOs de Datadog / Dynatrace / Grafana Cloud vienen incluidos si ya pagas esa plataforma (≈0 marginal), pero refuerzan el amarre al proveedor |
| Recomendación | Nombrar "SLO como código (Sloth u OpenSLO) en Git", coherente con el IDP y con GitOps |
| Tu decisión | |

### D6. Plataforma de CI/CD para el gate
| | |
|---|---|
| Escogido | "GitHub Actions o GitLab CI" (las dos del enunciado) |
| Alternativas | Escoger una sola · Jenkins · Azure DevOps · gate en el CD (ArgoCD) en vez del CI |
| Trade-off | Nombrar ambas muestra neutralidad; escoger una permite mostrar un ejemplo concreto. Tu nivel en GitLab CI es 🔴 |
| Costo | GitHub Actions / GitLab CI: si el banco ya tiene licencia, el gate es ≈0 marginal (segundos de runner por despliegue). Cambiar de plataforma de CI/CD solo por el gate sería $$$ en migración y personas; nunca lo propongas. Jenkins: licencia ≈0 pero alto costo de operación (servidores, plugins, parches) |
| Recomendación | Ejemplo concreto en GitHub Actions (tu fuerte) + "lo mismo aplica a GitLab CI con environments protegidos" |
| Tu decisión | |

### D7. Cómo se implementa el gate previo
| | |
|---|---|
| Escogido | Un paso del pipeline que consulta la API y termina en `exit 1` |
| Alternativas | **Deployment protection rule** del environment de GitHub (app externa que aprueba o rechaza) · admission controller en el clúster (OPA Gatekeeper / Kyverno) que rechaza el despliegue · gate en ArgoCD (sync window / pre-sync hook) |
| Trade-off | El paso en el pipeline es simple pero un equipo lo puede borrar de su YAML. La protection rule o el admission controller lo hacen **obligatorio y centralizado**, pero son más complejos |
| Costo | Paso en el pipeline: ≈0. Deployment protection rule: ≈0 si el plan de GitHub lo incluye (GitHub Enterprise), más una app pequeña que la responda ($). OPA Gatekeeper / Kyverno: licencia ≈0, unos pods por clúster ($) y ~0,1 FTE para mantener las políticas. Todas son baratas comparadas con **un** incidente SEV1 evitado |
| Recomendación | Mostrar el paso simple, y mencionar que en el banco se impone de forma central (protection rule o política en el clúster) para que nadie se lo salte |
| Tu decisión | |

### D8. Herramienta de progressive delivery (canary)
| | |
|---|---|
| Escogido | Argo Rollouts, pasos 5% → 25% → 50% → 100% |
| Alternativas | **Flagger** (con Istio / Linkerd / NGINX) · **Spinnaker** con Kayenta · canary manual con el service mesh · **feature flags** (OpenFeature, Unleash, LaunchDarkly) en vez de o además del canary |
| Trade-off | Argo Rollouts encaja si ya usan ArgoCD (GitOps). Flagger encaja si ya tienen Istio. Spinnaker es potente pero pesado. Feature flags separan desplegar de liberar, pero no protegen de un binario roto |
| Costo | Argo Rollouts / Flagger: licencia ≈0, costo de cómputo menor ($). El canary sí cuesta algo de capacidad extra durante el despliegue (pods de la versión nueva conviviendo con los de la vieja, ~5–25% más por minutos). Spinnaker: licencia ≈0 pero pesado de operar (varios microservicios propios, ~0,5 FTE, $$ en personas). Feature flags: **OpenFeature + Unleash / flagd** autogestionado ≈0–$; **LaunchDarkly** es SaaS por conexiones de servicio / usuarios, del orden de $$ para un banco |
| Recomendación | Argo Rollouts + feature flags para lo funcional (OpenFeature para no amarrarse a un proveedor). Pasos y duración: decir que dependen del tráfico (con poco tráfico, 5% no da muestras suficientes) |
| Tu decisión | |

### D9. Umbrales de alertas por burn rate
| | |
|---|---|
| Escogido | 14,4× en 1 h · 6× en 6 h → page · 1× en 3 días → ticket (SRE Workbook) |
| Alternativas | Una sola ventana · umbrales propios calibrados con datos · alertas por anomalía (ML) |
| Trade-off | Los del Workbook son el estándar reconocido y la mesa de SRE los va a reconocer; con SLO de 99,9% y poco tráfico nocturno pueden ser ruidosos |
| Costo | ≈0: son reglas de Prometheus. Costo indirecto: alertas ruidosas en la noche = horas de on-call y desgaste del equipo. Alertas por anomalía con ML (Machine Learning): suelen venir en planes SaaS caros ($$ a $$$) y son menos explicables |
| Recomendación | Mantener los del Workbook; mencionar que se calibran |
| Tu decisión | |

---

## Eje 2 — Telemetría y FinOps

### D10. Estándar de instrumentación y recolección
| | |
|---|---|
| Escogido | OpenTelemetry (SDK + auto-instrumentación con el OpenTelemetry Operator) |
| Alternativas | Agentes propietarios (Datadog Agent, Dynatrace OneAgent, New Relic) · **eBPF** sin tocar código (Grafana Beyla, Pixie, Cilium Hubble) · mezcla |
| Trade-off | OTel: neutral y estándar, pero más trabajo de operación. Agente propietario: más rápido y con mejor "magia", pero amarra al proveedor (cambiar cuesta reinstrumentar todo). eBPF: cero código, pero menos contexto de negocio |
| Costo | OTel: licencia ≈0; costo de instrumentación (personas) y de operar el Collector (ver D11–D12). Agente propietario: típicamente $$$ a $$$$ para cientos de hosts (por ejemplo, APM de Datadog ~USD 31–40/host/mes + infraestructura ~USD 15–23/host/mes ⇒ 500 hosts ≈ USD 25.000–30.000/mes antes de logs y trazas), y el costo de salida es reinstrumentar todo. eBPF (Grafana Beyla, Pixie, Cilium Hubble): licencia ≈0, CPU/memoria en cada nodo ($) |
| Recomendación | OTel como estándar (es lo que pide el caso) + eBPF como complemento para lo que no se puede instrumentar |
| Tu decisión | |

### D11. Distribución del Collector
| | |
|---|---|
| Escogido | OpenTelemetry Collector (contrib), construido con OCB |
| Alternativas | **Grafana Alloy** · distribuciones de proveedor (Datadog, Splunk, Elastic, AWS ADOT) · **Vector** · **Fluent Bit** (solo logs) |
| Trade-off | Collector oficial: neutral. ADOT (AWS Distro for OpenTelemetry) tiene soporte de AWS pero sesga a AWS en un banco multi-cloud. Vector/Fluent Bit son excelentes para logs pero no son nativos de trazas OTel |
| Costo | Todas son de licencia ≈0. El costo está en el cómputo y en las personas: el Collector oficial con OCB (OpenTelemetry Collector Builder) exige un pipeline para construir y parchar la imagen (~0,1–0,2 FTE). Las distribuciones de proveedor traen soporte "incluido" si ya pagas al proveedor, pero empujan a mandarle los datos a él. Diferencia económica pequeña entre opciones: decide la neutralidad, no el precio |
| Recomendación | Collector oficial construido con OCB (solo componentes aprobados → menos superficie de ataque) |
| Tu decisión | |

### D12. Topología del Collector
| | |
|---|---|
| Escogido | Agente DaemonSet + gateway de dos capas (`loadbalancing` por traceID → `tail_sampling`) por nube |
| Alternativas | Solo agentes, exportando directo · sidecar por pod · gateway de una capa (sin tail sampling) · un gateway central único para las dos nubes · delegar el muestreo al proveedor (Datadog ingestion controls, **Honeycomb Refinery**) |
| Trade-off | Dos capas es lo más robusto pero son más piezas que operar. Gateway central único cruza tráfico entre nubes (latencia y costo de egress). Muestreo en el proveedor: menos operación, pero ya pagaste el transporte y el dato salió del banco |
| Costo | Agentes DaemonSet: ~0,1–0,5 vCPU y 200–500 MB por nodo (≈ $ por cientos de nodos). Gateway de tail sampling: la memoria crece con `spans por segundo × decision_wait × tamaño del span` (ej.: 20.000 spans/s × 10 s × 1 KB ≈ 200 MB por réplica, ×2–3 de margen). Dos capas por nube: unos pocos nodos medianos ⇒ **$ a $$** al mes. Gateway central único: suma **egress entre nubes** (~USD 0,08–0,12/GB: 2 TB/día ≈ USD 5.000–7.000/mes extra, $$). Muestreo en el proveedor: pagas el transporte y a veces la ingesta de todo antes de descartar |
| Recomendación | La escogida, un gateway por nube (sin tráfico cruzado), y decir que empieza en una capa y crece a dos cuando se activa el tail sampling |
| Tu decisión | |

### D13. Política de muestreo
| | |
|---|---|
| Escogido | Tail: 100% errores, 100% > 2 s, 5% del resto, `decision_wait` 10 s |
| Alternativas | Solo head sampling (barato, pierde errores) · híbrido: head al 20–50% + tail · porcentajes distintos (1%, 10%) · muestreo adaptativo por volumen |
| Trade-off | Tail puro en todo el tráfico exige memoria en el gateway. El híbrido baja la carga del gateway pero puede botar errores en la cabeza |
| Costo | Es la decisión que más plata mueve en trazas. Con la línea base (trazas = USD 35.000/mes), quedarse con 100% de errores + lentas + 5% del resto puede bajar el volumen de trazas 70–90% en un sistema sano. Ser conservador en la diapositiva: −30 a −50% del costo de trazas ≈ **USD 10.000–17.000/mes de ahorro**. El costo de la decisión es el cómputo del gateway (D12, $ a $$). Head sampling solo: igual de barato, pero pierde errores (costo en MTTR, Mean Time To Restore) |
| Recomendación | Tail como diseño; si preguntan por memoria, el híbrido como optimización. Los porcentajes se ajustan midiendo |
| Tu decisión | |

### D14. Dónde y cómo se enmascara la PII
| | |
|---|---|
| Escogido | Processor `redaction` en el gateway |
| Alternativas | `transform` con OTTL (más flexible, permite hash) · `attributes` (delete / hash) · en el agente (más cerca del origen) · en el SDK de la app · en el proveedor SaaS (**red flag**: el dato ya salió) |
| Trade-off | Solo en el gateway: un punto único fácil de auditar, pero el dato viaja en claro dentro del clúster. En el agente: antes, pero hay muchos más puntos que gobernar |
| Costo | Los processors `redaction` / `transform` / `attributes`: ≈0 (algo de CPU en el Collector). El costo grande es el **riesgo**: una fuga de cédulas o tarjetas implica sanciones de la SIC (Superintendencia de Industria y Comercio) por Ley 1581 (multas de hasta 2.000 SMMLV, salarios mínimos mensuales legales vigentes, del orden de miles de millones de pesos), además de hallazgos de PCI DSS (Payment Card Industry Data Security Standard) y de la SFC. Defensa en profundidad cuesta horas de personas (plantilla del SDK), no licencias |
| Recomendación | Defensa en profundidad: SDK/plantilla evita loguear PII + agente + gateway como red final. Hash (no borrado) donde haga falta correlacionar |
| Tu decisión | |

### D15. Backends de almacenamiento
| | |
|---|---|
| Escogido | Ninguno nombrado ("backends de observabilidad") |
| Alternativas | Abiertos/autogestionados: Prometheus + **Mimir** o **Thanos** o VictoriaMetrics (métricas), **Tempo** o Jaeger (trazas), **Loki**, Elasticsearch u OpenSearch (logs), ClickHouse (SigNoz) · Administrados de nube: Amazon Managed Prometheus, Google Cloud Managed Service for Prometheus, CloudWatch, Cloud Logging · SaaS: Datadog, Dynatrace, New Relic, Grafana Cloud, Elastic Cloud |
| Trade-off | Autogestionado: barato en licencias y el dato no sale, pero cuesta operación (personas). SaaS: rápido y potente, pero caro por volumen y el dato sale del banco. Nativo de cada nube: dos mundos distintos en multi-cloud |
| Costo | La decisión de mayor impacto económico de toda la propuesta. **SaaS** (Datadog, Dynatrace, New Relic, Grafana Cloud): con la línea base ≈ **USD 100.000/mes ($$$$)**; rápido y sin operación. **Autogestionado** (Mimir / Tempo / Loki sobre almacenamiento de objetos): el almacenamiento es barato (~USD 0,02/GB/mes), cómputo $$ a $$$, más **2–4 FTE** de plataforma (≈ USD 12.000–24.000/mes). Suele quedar en **30–50% del costo del SaaS** a este volumen, pero solo si hay equipo. **Nativo de cada nube** (CloudWatch, Cloud Logging, Managed Prometheus): precio parecido al SaaS por GB (~USD 0,50/GB de logs), y dos consolas distintas. Regla práctica: a poco volumen gana el SaaS; a volumen de banco gana el autogestionado |
| Recomendación | **No casarse** en la presentación: "OTel nos deja cambiar de backend sin reinstrumentar"; el ejemplo de referencia puede ser el stack de Grafana (Mimir, Tempo, Loki). Si la mesa dice qué usan, adaptarse |
| Tu decisión | |

### D16. Log-to-Metrics
| | |
|---|---|
| Escogido | Connector `count` en el Collector |
| Alternativas | Que la app emita métricas directamente (lo ideal a largo plazo) · métricas derivadas de logs en el proveedor (pagas la ingesta igual) · reglas de grabación en Loki |
| Trade-off | En el Collector: ahorro inmediato sin tocar código. En la app: más limpio, pero exige cambios en cientos de repositorios |
| Costo | Connector `count`: ≈0 (CPU del Collector). Ahorro: una línea de log informativa que solo se contaba puede costar ~USD 0,50/GB; convertirla en una métrica cuesta unas pocas series (centavos). Si el 20–30% de los logs son de ese tipo, con la línea base (logs = USD 45.000/mes) son **USD 9.000–13.000/mes**. Métricas derivadas en el proveedor: pagas la ingesta completa igual, el ahorro es casi nulo |
| Recomendación | Collector ahora; la app como meta del SDK/plantilla corporativa |
| Tu decisión | |

### D17. Cifra de ahorro
| | |
|---|---|
| Escogido | −34% sobre una línea base ilustrativa (logs 45 / trazas 35 / métricas 20) |
| Alternativas | Decir solo "≥ 30%" sin desglose · rango (30–45%) · no dar cifra hasta medir |
| Trade-off | La cascada es concreta y convence, pero es inventada: si la mesa pregunta "¿de dónde salen esos porcentajes?", hay que reconocerlo. Sin cifra parece vago |
| Costo | Desglose ilustrativo de los −34% sobre USD 100.000/mes ⇒ **~USD 34.000/mes ≈ USD 400.000/año**: tail sampling en trazas, Log-to-Metrics y filtrado de logs, retención por niveles (caliente 7–15 días, fría en almacenamiento de objetos 4–20× más barato) y control de cardinalidad en métricas. Contra eso, la inversión es ~1–2 FTE durante 3–6 meses + unos pocos nodos para los gateways: el **retorno es de meses**, no de años. Frase para la mesa: "el ahorro del primer trimestre paga el equipo que lo implementa" |
| Recomendación | Mantener la cascada con la etiqueta "ilustrativa" bien visible y la frase "lo primero es medir la línea base" |
| Tu decisión | |

---

## Eje 3 — AI-Ready, MCP e IA causal

### D18. Servidor MCP: construir o adoptar
| | |
|---|---|
| Escogido | Construir un servidor MCP propio de solo lectura con 5 herramientas |
| Alternativas | Servidores MCP de los proveedores (Grafana, Datadog, Dynatrace, Prometheus ya publican uno) · combinar: los de proveedor para consultas + uno propio para `cambios_recientes` y el grafo |
| Trade-off | Propio: control total, herramientas de negocio y auditoría a la medida, pero hay que mantenerlo. De proveedor: gratis y rápido, pero herramientas genéricas y permisos a veces más amplios |
| Costo | Servidor MCP propio: licencia ≈0, desarrollo ~1 persona durante 4–8 semanas (≈ USD 6.000–12.000 una sola vez) + mantenimiento ~0,1–0,2 FTE. Servidores MCP de proveedor: ≈0 (vienen con el producto), pero **cada consulta del agente** contra un SaaS puede tener costo (llamadas a la API, límites de tasa). El cómputo para correr el servidor MCP es $ |
| Recomendación | Combinar: adoptar el del backend escogido y construir solo lo propio (cambios, grafo, SLO de negocio) |
| Tu decisión | |

### D19. Modelo de IA y dónde corre
| | |
|---|---|
| Escogido | No nombrado ("modelo en una red o región aprobada") |
| Alternativas | Modelo vía nube del banco (Amazon Bedrock, Google Vertex AI) · modelo abierto autoalojado · IA del proveedor de observabilidad (Dynatrace Davis, Datadog Bits AI / Watchdog) · plataformas AIOps (BigPanda, Moogsoft) |
| Trade-off | Bedrock/Vertex: el dato queda en la cuenta del banco, buen balance. Autoalojado: máxima soberanía, más costo y menos capacidad. IA del proveedor: lista ya, pero caja negra y amarrada. Plataformas AIOps: fuertes en correlación de alertas, débiles en causalidad |
| Costo | **Bedrock / Vertex AI**: pago por token. Una investigación de RCA (Root Cause Analysis) consume ~50.000–200.000 tokens ⇒ **~USD 0,30–3 por incidente** con un modelo de gama media: incluso 1.000 investigaciones al mes son $ a $$. **Modelo abierto autoalojado**: GPU encendida 24/7; un modelo grande (~70B parámetros) necesita 2–4 GPU de gama alta ⇒ **USD 5.000–20.000/mes ($$ a $$$)** + personas, aunque se use poco. **IA del proveedor de observabilidad**: suele venir en planes superiores o con cargos por uso ($$). **Plataformas AIOps** (BigPanda, Moogsoft): licencia empresarial ($$ a $$$). Comparación clave: el costo por token es despreciable frente a un minuto caído del pago QR |
| Recomendación | Agnóstico gracias a MCP; ejemplo: Bedrock o Vertex dentro de la cuenta del banco |
| Tu decisión | |

### D20. Fuente del grafo de topología
| | |
|---|---|
| Escogido | Connector `servicegraph` (desde trazas) |
| Alternativas | Kiali con Istio (desde el service mesh) · eBPF (conexiones de red reales) · catálogo declarado (Backstage, ServiceNow CMDB) · service map del proveedor |
| Trade-off | Desde trazas: rico en contexto, pero ciego donde no hay instrumentación. eBPF: ve todo lo que se conecta, pero sin semántica. Catálogo: dice lo que debería ser, no lo que es |
| Costo | Connector `servicegraph`: ≈0 (genera métricas en el Collector, unas pocas series por cada par de servicios). Kiali: ≈0 si ya existe Istio; desplegar Istio solo para esto es caro en operación y CPU de sidecars (+10–20% de recursos, $$). eBPF: ≈0 de licencia, $ de CPU. Catálogo (Backstage): ver D25. Service map del proveedor: incluido en el APM que ya pagas, pero amarrado |
| Recomendación | Trazas como fuente principal y comparar con el catálogo: la diferencia entre "declarado" y "observado" es un hallazgo en sí |
| Tu decisión | |

### D21. Algoritmo de causa raíz
| | |
|---|---|
| Escogido | DFS al nodo anómalo más profundo + BFS para radio de explosión |
| Alternativas | Random walk / PageRank personalizado (MicroRCA) · inferencia causal (algoritmo PC, Granger) · dejar que el LLM razone sobre el grafo sin algoritmo |
| Trade-off | DFS/BFS: simple, explicable y barato, pero frágil con dos causas o ciclos. PageRank: rankea mejor varios candidatos, pero menos explicable. Causal pura: es investigación |
| Costo | DFS/BFS: ≈0, son algoritmos que corren en milisegundos sobre un grafo de cientos de nodos. PageRank personalizado: ≈0 en cómputo, ~2–4 semanas de una persona para implementarlo y validarlo. Inferencia causal pura: investigación, meses de personas ($$$ en tiempo). Dejar todo al LLM: más tokens por investigación (centavos a pocos dólares) y respuestas menos reproducibles |
| Recomendación | DFS/BFS en la diapositiva (explicable ante la mesa); PageRank como evolución si preguntan |
| Tu decisión | |

---

## Eje 4 — Incidentes y cultura

### D22. Herramienta de gestión de incidentes y on-call
| | |
|---|---|
| Escogido | No nombrada |
| Alternativas | PagerDuty · incident.io · FireHydrant · Grafana IRM · ServiceNow (probable en un banco) · Opsgenie (Atlassian anunció su fin de venta; verificar fechas antes de mencionarlo) |
| Trade-off | Lo que importa es el proceso; la herramienta es secundaria. ServiceNow suele ser el sistema de registro en banca; las otras son mejores para el flujo en vivo |
| Costo | **PagerDuty**: ~USD 20–40+ por usuario al mes según el plan; 50 personas en on-call ≈ **USD 1.000–2.000/mes ($$)**. **incident.io / FireHydrant**: rango parecido. **Grafana IRM**: incluido en algunos planes de Grafana Cloud. **ServiceNow**: licencia cara (del orden de USD 100 por agente al mes), pero en un banco **ya está pagada**: el costo marginal es ≈0. Argumento económico: reutilizar el ITSM (IT Service Management) del banco y solo pagar la herramienta de on-call si hace falta |
| Recomendación | No nombrar herramienta en la diapositiva; si preguntan: "integrado con el ITSM (IT Service Management) del banco, probablemente ServiceNow" |
| Tu decisión | |

### D23. Estructura de roles del incidente
| | |
|---|---|
| Escogido | IC + Ops Lead + Comms Lead + Scribe (modelo ICS) |
| Alternativas | Más roles (Subject Matter Experts, enlace con negocio, Planning) · menos roles para SEV2/SEV3 (IC + ingeniero) |
| Trade-off | Cuatro roles es claro para SEV1; para incidentes menores es burocrático |
| Costo | Costo en **horas de personas por incidente**: un SEV1 de 2 horas con 4 roles + 3 expertos = ~14 horas-persona (≈ USD 500 a costo empresa). Es despreciable frente al minuto caído; el riesgo es aplicar los 4 roles a incidentes menores (SEV3) y gastar horas sin necesidad |
| Recomendación | Cuatro roles en SEV1 y decir que escala hacia abajo con la severidad |
| Tu decisión | |

### D24. Plazo y método del post-mortem
| | |
|---|---|
| Escogido | ≤ 5 días hábiles, factores contribuyentes, acciones prevenir/detectar/mitigar |
| Alternativas | 48 horas · 5 porqués · análisis de "Learning from Incidents" sin causa raíz única |
| Trade-off | Muy rápido pierde perspectiva; muy lento pierde memoria |
| Costo | Un post-mortem cuesta ~4–8 horas-persona entre preparación, reunión y redacción (≈ USD 150–300). Las **acciones** que salen de él son las que cuestan (y las que ahorran): priorizarlas por minutos de Error Budget que evitan |
| Recomendación | Mantener |
| Tu decisión | |

### D25. IDP (Internal Developer Platform)
| | |
|---|---|
| Escogido | No nombrado |
| Alternativas | **Backstage** (abierto, de Spotify / CNCF) · Port · Cortex · ServiceNow · portal propio |
| Trade-off | Backstage es el estándar abierto, pero exige un equipo que lo mantenga. Port/Cortex son más rápidos de adoptar, pero son SaaS |
| Costo | **Backstage**: licencia ≈0, pero exige un equipo de plataforma de **2–4 FTE** (≈ USD 12.000–24.000/mes) para mantenerlo y escribir plugins. **Port / Cortex**: SaaS por desarrollador (del orden de USD 30–70 por desarrollador al mes; 500 desarrolladores ≈ $$ a $$$). **ServiceNow** (si ya existe): costo marginal bajo. Para la mesa: el IDP (Internal Developer Platform) no es parte del costo de esta propuesta; se reutiliza lo que ya tenga el banco |
| Recomendación | "IDP (por ejemplo, Backstage)" o adaptarse a lo que ya tenga el banco |
| Tu decisión | |

### D26. Motor de políticas
| | |
|---|---|
| Escogido | OPA |
| Alternativas | **Kyverno** (políticas en YAML, más simple en Kubernetes) · OPA Gatekeeper |
| Trade-off | OPA es general (sirve fuera de Kubernetes, incluso en el CI); Kyverno es más fácil de leer para los equipos |
| Costo | OPA y Kyverno: licencia ≈0, unos pods por clúster ($). Diferencia económica real: el tiempo de las personas escribiendo y leyendo políticas (Rego de OPA es más difícil de aprender que el YAML de Kyverno). Existen versiones empresariales con soporte (Styra para OPA, Nirmata para Kyverno), $$ |
| Recomendación | OPA (lo conoces en 🟢) |
| Tu decisión | |

---

## Decisiones de narrativa (no son de herramientas)

### D27. Orden de la hoja de ruta
| | |
|---|---|
| Escogido | 30 días SLO + burn rate · 60 días Quality Gate + gateway con PII · 90 días tail sampling + MCP |
| Alternativas | Empezar por FinOps (el ahorro paga el resto) · empezar por el gateway con PII (requisito regulatorio primero) |
| Trade-off | Empezar por el SLO es lo más coherente con la historia; empezar por el ahorro es lo que más le gusta a un CFO (Chief Financial Officer) |
| Costo | Hoja de ruta en plata: 30 días (SLO + burn rate) ≈0 en licencias, ~1 FTE. 60 días (Quality Gate + gateway con PII): unos nodos para el gateway ($) + ~1–2 FTE. 90 días (tail sampling + MCP): $ a $$ en cómputo y tokens, y aquí **empieza el ahorro** (D13, D16, D17). Empezar por FinOps traería el ahorro 1–2 meses antes, pero sin SLOs no sabes qué datos son seguros de descartar |
| Recomendación | Mantener, pero decir que el ahorro del tail sampling financia las fases siguientes |
| Tu decisión | |

### D28. Un solo servicio piloto
| | |
|---|---|
| Escogido | Pago QR como piloto |
| Alternativas | Transferencias en tiempo real · varios servicios a la vez |
| Trade-off | El pago QR es el ejemplo del enunciado y el más visible para el cliente |
| Costo | Un piloto acota la inversión: ~1–2 FTE durante el trimestre (≈ USD 18.000–36.000) para un servicio, con un resultado medible antes de escalar. Ir con varios servicios a la vez multiplica el costo de personas y el riesgo, sin multiplicar la evidencia |
| Recomendación | Mantener |
| Tu decisión | |

### D29. Mención de experiencia previa
| | |
|---|---|
| Escogido | "Una plataforma de comercio electrónico de alto volumen", sin nombre |
| Alternativas | Nombrar a MercadoLibre sin detalles internos · no mencionarla |
| Trade-off | Nombrarla da credibilidad inmediata; no nombrarla es más prudente con la confidencialidad |
| Costo | Sin componente económico |
| Recomendación | Decisión tuya: depende de tu acuerdo de confidencialidad |
| Tu decisión | |

### D30. Ejemplo del incidente
| | |
|---|---|
| Escogido | Antifraude v2.3.1 rompe el pago QR (causa = un despliegue) |
| Alternativas | Una falla de infraestructura (nodo, red, certificado vencido) · una dependencia externa (otro banco, Bre-B) · saturación del AS400 en quincena |
| Trade-off | El despliegue conecta los 4 ejes (el gate debió frenarlo), pero es el caso "fácil". Saturación del AS400 es más realista para un banco y lucha con el legado, pero el rollback no lo arregla |
| Costo | Para la narrativa: un despliegue malo cuesta los minutos que tarde el rollback (con Argo Rollouts: minutos, casi todo el Error Budget a salvo). La variante de saturación del AS400 en quincena es más cara: el rollback no la arregla, y escalar el AS400 es caro (licencias y capacidad de IBM i, decenas a cientos de miles de USD). Por eso ahí la respuesta barata y rápida es **load shedding + circuit breaker**, no comprar más capacidad |
| Recomendación | Mantener el despliegue en la diapositiva y tener preparada la variante "saturación del AS400 en quincena" para preguntas (load shedding + circuit breaker) |
| Tu decisión | |
