# Análisis de alternativas — decisiones del libreto (borrador v1)

> El libreto (`presentacion-libreto.md`) tomó decisiones sin discutirlas. Aquí está cada una con lo que
> se escogió, las alternativas, el trade-off (qué ganas y qué pierdes) y una recomendación.
> La columna **Tu decisión** queda vacía a propósito: se llena en sesión, **de a una decisión por vez**.
>
> Criterio general de la recomendación: el caso premia **viabilidad y pragmatismo**, y la mesa incluye
> DevSecOps (soberanía del dato) y Arquitectura (neutralidad frente al proveedor). Por eso pesa más lo
> estándar y abierto que lo "más potente".

---

## Eje 1 — SLOs, Error Budgets y Quality Gate

### D1. Valor del SLO de disponibilidad del pago QR
| | |
|---|---|
| Escogido | 99,9% en 30 días móviles (43,2 min/mes) |
| Alternativas | 99,95% (21,6 min) · 99,99% (4,32 min) · 99,5% (3,6 h) |
| Trade-off | 99,95% suena más "bancario", pero 3 dependencias en serie de 99,9% ya dan 99,7%: obliga a redundancia en todo. 99,9% es defendible como **punto de partida** que se ajusta con datos |
| Recomendación | 99,9% y decir explícitamente "se calibra con 4 semanas de datos reales" |
| Tu decisión | |

### D2. Ventana del SLO
| | |
|---|---|
| Escogido | 30 días móviles |
| Alternativas | 28 días móviles (todas las ventanas con los mismos días de semana) · mes calendario |
| Trade-off | 28 días es más riguroso; 30 días hace la cuenta de 43,2 min más fácil de recordar. El mes calendario "resetea" el presupuesto el día 1 (mala práctica) |
| Recomendación | 30 días en la diapositiva; 28 como respuesta si preguntan |
| Tu decisión | |

### D3. SLI de latencia y dónde se mide
| | |
|---|---|
| Escogido | 99% de pagos confirmados en < 2 s, medido en el API Gateway |
| Alternativas | Umbral distinto (1 s, 3 s) · medir en el cliente con RUM (Real User Monitoring) desde la app · monitoreo sintético · medir en el balanceador de carga |
| Trade-off | API Gateway: fácil y confiable, pero no ve la red móvil del cliente. RUM: lo más centrado en el cliente, pero ruidoso (celulares y redes que no controlamos). Sintético: detecta caídas sin tráfico, pero no es tráfico real |
| Recomendación | API Gateway para el SLO + RUM y sintético como señales complementarias (responde "customer centric" sin volver ruidoso el SLO) |
| Tu decisión | |

### D4. Umbrales de la Error Budget Policy
| | |
|---|---|
| Escogido | > 50% normal · 25–50% solo canary · < 25% congelado salvo fixes |
| Alternativas | Política binaria (queda presupuesto / no queda) · umbrales por burn rate en vez de presupuesto restante · congelar solo con presupuesto agotado (0%) |
| Trade-off | Tres zonas dan gradualidad pero son más difíciles de negociar con negocio. Binaria es simple pero brusca |
| Recomendación | Tres zonas, presentadas como **propuesta para negociar con negocio**, no como verdad |
| Tu decisión | |

### D5. Herramienta para definir y calcular los SLOs
| | |
|---|---|
| Escogido | Ninguna nombrada ("la fuente de SLOs") |
| Alternativas | **Sloth** o **Pyrra** (generan reglas de Prometheus desde un YAML) · **OpenSLO** (especificación abierta) · Google **SLO Generator** · SaaS: **Nobl9**, SLOs de Datadog / Dynatrace / Grafana Cloud |
| Trade-off | Sloth/Pyrra: abiertos, "SLO como código" en Git, pero hay que operarlos. SaaS: listo rápido, pero amarra al proveedor y cuesta |
| Recomendación | Nombrar "SLO como código (Sloth u OpenSLO) en Git", coherente con el IDP y con GitOps |
| Tu decisión | |

### D6. Plataforma de CI/CD para el gate
| | |
|---|---|
| Escogido | "GitHub Actions o GitLab CI" (las dos del enunciado) |
| Alternativas | Escoger una sola · Jenkins · Azure DevOps · gate en el CD (ArgoCD) en vez del CI |
| Trade-off | Nombrar ambas muestra neutralidad; escoger una permite mostrar un ejemplo concreto. Tu nivel en GitLab CI es 🔴 |
| Recomendación | Ejemplo concreto en GitHub Actions (tu fuerte) + "lo mismo aplica a GitLab CI con environments protegidos" |
| Tu decisión | |

### D7. Cómo se implementa el gate previo
| | |
|---|---|
| Escogido | Un paso del pipeline que consulta la API y termina en `exit 1` |
| Alternativas | **Deployment protection rule** del environment de GitHub (app externa que aprueba o rechaza) · admission controller en el clúster (OPA Gatekeeper / Kyverno) que rechaza el despliegue · gate en ArgoCD (sync window / pre-sync hook) |
| Trade-off | El paso en el pipeline es simple pero un equipo lo puede borrar de su YAML. La protection rule o el admission controller lo hacen **obligatorio y centralizado**, pero son más complejos |
| Recomendación | Mostrar el paso simple, y mencionar que en el banco se impone de forma central (protection rule o política en el clúster) para que nadie se lo salte |
| Tu decisión | |

### D8. Herramienta de progressive delivery (canary)
| | |
|---|---|
| Escogido | Argo Rollouts, pasos 5% → 25% → 50% → 100% |
| Alternativas | **Flagger** (con Istio / Linkerd / NGINX) · **Spinnaker** con Kayenta · canary manual con el service mesh · **feature flags** (OpenFeature, Unleash, LaunchDarkly) en vez de o además del canary |
| Trade-off | Argo Rollouts encaja si ya usan ArgoCD (GitOps). Flagger encaja si ya tienen Istio. Spinnaker es potente pero pesado. Feature flags separan desplegar de liberar, pero no protegen de un binario roto |
| Recomendación | Argo Rollouts + feature flags para lo funcional (OpenFeature para no amarrarse a un proveedor). Pasos y duración: decir que dependen del tráfico (con poco tráfico, 5% no da muestras suficientes) |
| Tu decisión | |

### D9. Umbrales de alertas por burn rate
| | |
|---|---|
| Escogido | 14,4× en 1 h · 6× en 6 h → page · 1× en 3 días → ticket (SRE Workbook) |
| Alternativas | Una sola ventana · umbrales propios calibrados con datos · alertas por anomalía (ML) |
| Trade-off | Los del Workbook son el estándar reconocido y la mesa de SRE los va a reconocer; con SLO de 99,9% y poco tráfico nocturno pueden ser ruidosos |
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
| Recomendación | OTel como estándar (es lo que pide el caso) + eBPF como complemento para lo que no se puede instrumentar |
| Tu decisión | |

### D11. Distribución del Collector
| | |
|---|---|
| Escogido | OpenTelemetry Collector (contrib), construido con OCB |
| Alternativas | **Grafana Alloy** · distribuciones de proveedor (Datadog, Splunk, Elastic, AWS ADOT) · **Vector** · **Fluent Bit** (solo logs) |
| Trade-off | Collector oficial: neutral. ADOT (AWS Distro for OpenTelemetry) tiene soporte de AWS pero sesga a AWS en un banco multi-cloud. Vector/Fluent Bit son excelentes para logs pero no son nativos de trazas OTel |
| Recomendación | Collector oficial construido con OCB (solo componentes aprobados → menos superficie de ataque) |
| Tu decisión | |

### D12. Topología del Collector
| | |
|---|---|
| Escogido | Agente DaemonSet + gateway de dos capas (`loadbalancing` por traceID → `tail_sampling`) por nube |
| Alternativas | Solo agentes, exportando directo · sidecar por pod · gateway de una capa (sin tail sampling) · un gateway central único para las dos nubes · delegar el muestreo al proveedor (Datadog ingestion controls, **Honeycomb Refinery**) |
| Trade-off | Dos capas es lo más robusto pero son más piezas que operar. Gateway central único cruza tráfico entre nubes (latencia y costo de egress). Muestreo en el proveedor: menos operación, pero ya pagaste el transporte y el dato salió del banco |
| Recomendación | La escogida, un gateway por nube (sin tráfico cruzado), y decir que empieza en una capa y crece a dos cuando se activa el tail sampling |
| Tu decisión | |

### D13. Política de muestreo
| | |
|---|---|
| Escogido | Tail: 100% errores, 100% > 2 s, 5% del resto, `decision_wait` 10 s |
| Alternativas | Solo head sampling (barato, pierde errores) · híbrido: head al 20–50% + tail · porcentajes distintos (1%, 10%) · muestreo adaptativo por volumen |
| Trade-off | Tail puro en todo el tráfico exige memoria en el gateway. El híbrido baja la carga del gateway pero puede botar errores en la cabeza |
| Recomendación | Tail como diseño; si preguntan por memoria, el híbrido como optimización. Los porcentajes se ajustan midiendo |
| Tu decisión | |

### D14. Dónde y cómo se enmascara la PII
| | |
|---|---|
| Escogido | Processor `redaction` en el gateway |
| Alternativas | `transform` con OTTL (más flexible, permite hash) · `attributes` (delete / hash) · en el agente (más cerca del origen) · en el SDK de la app · en el proveedor SaaS (**red flag**: el dato ya salió) |
| Trade-off | Solo en el gateway: un punto único fácil de auditar, pero el dato viaja en claro dentro del clúster. En el agente: antes, pero hay muchos más puntos que gobernar |
| Recomendación | Defensa en profundidad: SDK/plantilla evita loguear PII + agente + gateway como red final. Hash (no borrado) donde haga falta correlacionar |
| Tu decisión | |

### D15. Backends de almacenamiento
| | |
|---|---|
| Escogido | Ninguno nombrado ("backends de observabilidad") |
| Alternativas | Abiertos/autogestionados: Prometheus + **Mimir** o **Thanos** o VictoriaMetrics (métricas), **Tempo** o Jaeger (trazas), **Loki**, Elasticsearch u OpenSearch (logs), ClickHouse (SigNoz) · Administrados de nube: Amazon Managed Prometheus, Google Cloud Managed Service for Prometheus, CloudWatch, Cloud Logging · SaaS: Datadog, Dynatrace, New Relic, Grafana Cloud, Elastic Cloud |
| Trade-off | Autogestionado: barato en licencias y el dato no sale, pero cuesta operación (personas). SaaS: rápido y potente, pero caro por volumen y el dato sale del banco. Nativo de cada nube: dos mundos distintos en multi-cloud |
| Recomendación | **No casarse** en la presentación: "OTel nos deja cambiar de backend sin reinstrumentar"; el ejemplo de referencia puede ser el stack de Grafana (Mimir, Tempo, Loki). Si la mesa dice qué usan, adaptarse |
| Tu decisión | |

### D16. Log-to-Metrics
| | |
|---|---|
| Escogido | Connector `count` en el Collector |
| Alternativas | Que la app emita métricas directamente (lo ideal a largo plazo) · métricas derivadas de logs en el proveedor (pagas la ingesta igual) · reglas de grabación en Loki |
| Trade-off | En el Collector: ahorro inmediato sin tocar código. En la app: más limpio, pero exige cambios en cientos de repositorios |
| Recomendación | Collector ahora; la app como meta del SDK/plantilla corporativa |
| Tu decisión | |

### D17. Cifra de ahorro
| | |
|---|---|
| Escogido | −34% sobre una línea base ilustrativa (logs 45 / trazas 35 / métricas 20) |
| Alternativas | Decir solo "≥ 30%" sin desglose · rango (30–45%) · no dar cifra hasta medir |
| Trade-off | La cascada es concreta y convence, pero es inventada: si la mesa pregunta "¿de dónde salen esos porcentajes?", hay que reconocerlo. Sin cifra parece vago |
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
| Recomendación | Combinar: adoptar el del backend escogido y construir solo lo propio (cambios, grafo, SLO de negocio) |
| Tu decisión | |

### D19. Modelo de IA y dónde corre
| | |
|---|---|
| Escogido | No nombrado ("modelo en una red o región aprobada") |
| Alternativas | Modelo vía nube del banco (Amazon Bedrock, Google Vertex AI) · modelo abierto autoalojado · IA del proveedor de observabilidad (Dynatrace Davis, Datadog Bits AI / Watchdog) · plataformas AIOps (BigPanda, Moogsoft) |
| Trade-off | Bedrock/Vertex: el dato queda en la cuenta del banco, buen balance. Autoalojado: máxima soberanía, más costo y menos capacidad. IA del proveedor: lista ya, pero caja negra y amarrada. Plataformas AIOps: fuertes en correlación de alertas, débiles en causalidad |
| Recomendación | Agnóstico gracias a MCP; ejemplo: Bedrock o Vertex dentro de la cuenta del banco |
| Tu decisión | |

### D20. Fuente del grafo de topología
| | |
|---|---|
| Escogido | Connector `servicegraph` (desde trazas) |
| Alternativas | Kiali con Istio (desde el service mesh) · eBPF (conexiones de red reales) · catálogo declarado (Backstage, ServiceNow CMDB) · service map del proveedor |
| Trade-off | Desde trazas: rico en contexto, pero ciego donde no hay instrumentación. eBPF: ve todo lo que se conecta, pero sin semántica. Catálogo: dice lo que debería ser, no lo que es |
| Recomendación | Trazas como fuente principal y comparar con el catálogo: la diferencia entre "declarado" y "observado" es un hallazgo en sí |
| Tu decisión | |

### D21. Algoritmo de causa raíz
| | |
|---|---|
| Escogido | DFS al nodo anómalo más profundo + BFS para radio de explosión |
| Alternativas | Random walk / PageRank personalizado (MicroRCA) · inferencia causal (algoritmo PC, Granger) · dejar que el LLM razone sobre el grafo sin algoritmo |
| Trade-off | DFS/BFS: simple, explicable y barato, pero frágil con dos causas o ciclos. PageRank: rankea mejor varios candidatos, pero menos explicable. Causal pura: es investigación |
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
| Recomendación | No nombrar herramienta en la diapositiva; si preguntan: "integrado con el ITSM (IT Service Management) del banco, probablemente ServiceNow" |
| Tu decisión | |

### D23. Estructura de roles del incidente
| | |
|---|---|
| Escogido | IC + Ops Lead + Comms Lead + Scribe (modelo ICS) |
| Alternativas | Más roles (Subject Matter Experts, enlace con negocio, Planning) · menos roles para SEV2/SEV3 (IC + ingeniero) |
| Trade-off | Cuatro roles es claro para SEV1; para incidentes menores es burocrático |
| Recomendación | Cuatro roles en SEV1 y decir que escala hacia abajo con la severidad |
| Tu decisión | |

### D24. Plazo y método del post-mortem
| | |
|---|---|
| Escogido | ≤ 5 días hábiles, factores contribuyentes, acciones prevenir/detectar/mitigar |
| Alternativas | 48 horas · 5 porqués · análisis de "Learning from Incidents" sin causa raíz única |
| Trade-off | Muy rápido pierde perspectiva; muy lento pierde memoria |
| Recomendación | Mantener |
| Tu decisión | |

### D25. IDP (Internal Developer Platform)
| | |
|---|---|
| Escogido | No nombrado |
| Alternativas | **Backstage** (abierto, de Spotify / CNCF) · Port · Cortex · ServiceNow · portal propio |
| Trade-off | Backstage es el estándar abierto, pero exige un equipo que lo mantenga. Port/Cortex son más rápidos de adoptar, pero son SaaS |
| Recomendación | "IDP (por ejemplo, Backstage)" o adaptarse a lo que ya tenga el banco |
| Tu decisión | |

### D26. Motor de políticas
| | |
|---|---|
| Escogido | OPA |
| Alternativas | **Kyverno** (políticas en YAML, más simple en Kubernetes) · OPA Gatekeeper |
| Trade-off | OPA es general (sirve fuera de Kubernetes, incluso en el CI); Kyverno es más fácil de leer para los equipos |
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
| Recomendación | Mantener, pero decir que el ahorro del tail sampling financia las fases siguientes |
| Tu decisión | |

### D28. Un solo servicio piloto
| | |
|---|---|
| Escogido | Pago QR como piloto |
| Alternativas | Transferencias en tiempo real · varios servicios a la vez |
| Trade-off | El pago QR es el ejemplo del enunciado y el más visible para el cliente |
| Recomendación | Mantener |
| Tu decisión | |

### D29. Mención de experiencia previa
| | |
|---|---|
| Escogido | "Una plataforma de comercio electrónico de alto volumen", sin nombre |
| Alternativas | Nombrar a MercadoLibre sin detalles internos · no mencionarla |
| Trade-off | Nombrarla da credibilidad inmediata; no nombrarla es más prudente con la confidencialidad |
| Recomendación | Decisión tuya: depende de tu acuerdo de confidencialidad |
| Tu decisión | |

### D30. Ejemplo del incidente
| | |
|---|---|
| Escogido | Antifraude v2.3.1 rompe el pago QR (causa = un despliegue) |
| Alternativas | Una falla de infraestructura (nodo, red, certificado vencido) · una dependencia externa (otro banco, Bre-B) · saturación del AS400 en quincena |
| Trade-off | El despliegue conecta los 4 ejes (el gate debió frenarlo), pero es el caso "fácil". Saturación del AS400 es más realista para un banco y lucha con el legado, pero el rollback no lo arregla |
| Recomendación | Mantener el despliegue en la diapositiva y tener preparada la variante "saturación del AS400 en quincena" para preguntas (load shedding + circuit breaker) |
| Tu decisión | |
