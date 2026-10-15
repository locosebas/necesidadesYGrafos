# Ruta para la sustentación — Banco Plus (después de la entrega del 12 de octubre)

> La prueba se entregó el 12 de octubre de 2026 (PDF de 10 diapositivas). Lo que sigue es la **exposición de 20
> minutos + 10 minutos de preguntas**. Meta: ser experto, no "haberlo leído".
>
> **Cómo se usa:** las preguntas se hacen **de a una**, sin ver la respuesta (está plegada en "Respuesta").
> En los repasos se **describe el mecanismo y se pide el nombre**. Las listas (las 10 preguntas del hilo, las 5
> reglas, los 4 ejes) se recitan **completas y sin pistas** antes de recibir corrección.
> Escala: ⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior (la de `../../devops-senior/examenes/registro/progreso.md`).

**Material de apoyo:** [libreto](presentacion-libreto.md) · [análisis de alternativas](analisis-alternativas.md) ·
[contraargumentos](contraargumentos.md) · [chuleta de nombres](chuleta-nombres.md) · [banco de preguntas](banco-preguntas.md).

---

## Parte 1 — Dominar la presentación

| Etapa | Qué | Meta |
|---|---|---|
| 1.1 | El hilo: las 10 preguntas en orden, los 4 ejes, las 5 reglas | Recitar sin pistas |
| 1.2 | Diapositiva por diapositiva: qué dice, qué muestra el diagrama, por qué se decidió así | 🟢 en las 10 |
| 1.3 | Defender las decisiones contra la mesa (contraargumentos) | 🔵 |
| 1.4 | Ensayo cronometrado (20 min) + simulacro de 10 min de preguntas | Dentro del tiempo, sin leer |

### 1.1 El hilo (repaso estricto de listas)

**P1.1** Recita, en orden, las 10 preguntas que responde la presentación.
<details><summary>Respuesta</summary>

1. ¿Por qué el pago QR de Banco Plus no es confiable hoy? 2. ¿Dónde duele hoy, en la arquitectura? 3. ¿Qué es
"estar bien" para el cliente? 4. ¿Cómo evitamos que un despliegue lo rompa? 5. ¿De dónde salen los datos?
6. ¿Cómo los vemos sin pagar de más? 7. ¿Cómo hacemos que una IA los entienda? 8. ¿Cómo encuentra la IA dónde
nace la falla? 9. ¿Qué hacemos cuando, aun así, falla en hora pico? 10. ¿Cómo aprendemos para que no vuelva a pasar?
</details>

**P1.2** Recita los 4 ejes del caso con lo que pide cada uno.
<details><summary>Respuesta</summary>

1. Gobierno de SLOs, Error Budgets y Quality Gates (SLIs/SLOs del pago QR + gate autoejecutable en CI/CD).
2. Telemetría avanzada y FinOps (OpenTelemetry Collector multi-cloud + Smart Sampling, −30% de costo sin perder errores).
3. Estandarización semántica para AIOps y MCP (datos AI-Ready + IA causal para RCA).
4. Comando de incidentes y cultura blameless (Incident Commander en hora pico + post-mortem).
</details>

**P1.3** Recita las 5 reglas que atraviesan el libreto.
<details><summary>Respuesta</summary>

1. Ningún número inventado (solo el SLO de partida 99,9%, la meta del caso −30%, valores con fuente y casos públicos).
2. Lo que el banco ya tiene no se escoge, se integra. 3. Lo que proponemos se nombra. 4. Plataforma es
habilitador: el piso, no el techo. 5. No mencionar sistemas que el caso no nombra (core bancario, CBU/QR).
</details>

**P1.4** ¿Cuál es la "causa común" de los cuatro retos? Dila en una frase.
<details><summary>Respuesta</summary>No hay una definición compartida de qué es "estar bien" ni datos estandarizados para saber cuándo dejamos de estarlo.</details>

**P1.5** Recita las 6 preguntas que le haces a la mesa (el backlog de la Fase 0).
<details><summary>Respuesta</summary>

Dueño de los pipelines y plantillas · con qué despliegan en Kubernetes y si hay service mesh · backend de
observabilidad contratado · modelo de IA o plataforma con IA contratada · herramienta de on-call e ITSM ·
motor de políticas.
</details>

### 1.2 Diapositiva por diapositiva

**Diapositiva 3 — SLOs**

**P1.6** Define el SLI de disponibilidad del pago QR. ¿Por qué un saldo insuficiente no cuenta?
<details><summary>Respuesta</summary>Pagos aceptados sin error de sistema ÷ pagos válidos. El saldo insuficiente es un rechazo de negocio correcto, no una falla del sistema.</details>

**P1.7** ¿Cuántos minutos al mes da un SLO de 99,9% en 30 días? Haz la cuenta en voz alta.
<details><summary>Respuesta</summary>30 × 24 × 60 = 43.200 min; 0,1% = 43,2 minutos.</details>

**P1.8** Te piden el SLO de latencia. ¿Qué respondes y de dónde sale el umbral?
<details><summary>Respuesta</summary>El SLI está definido (proporción de pagos bajo un umbral, medido en el API Gateway, en percentil). El umbral sale de la curva de abandono del cliente, los timeouts del flujo y el histograma real de 4 semanas, en la Fase 0. Un número inventado nace roto o no protege.</details>

**P1.9** Describe las zonas de la Error Budget Policy de conservación y qué se permite en cada una.
<details><summary>Respuesta</summary>Sano: canary por defecto (la estrategia que menos gasta). En riesgo: solo canary lento y estricto, sin Blue/Green. Crítico: congelado salvo arreglos de confiabilidad. Agotado: congelado + post-mortem del consumo. Umbrales: se negocian con negocio con datos.</details>

**Diapositiva 4 — Quality Gate**

**P1.10** El gate tiene tres momentos. Nómbralos y di qué pasa en cada uno.
<details><summary>Respuesta</summary>Antes: deployment protection rule consulta el Error Budget. Durante: canary con análisis automático y rollback. Después: verificación del burn rate y evento "cambio desplegado".</details>

**P1.11** Una regla vive en el environment de producción y una app de Plataforma aprueba o rechaza cada despliegue, aunque la tribu borre pasos de su YAML. ¿Cómo se llama?
<details><summary>Respuesta</summary>Deployment protection rule (de GitHub Actions).</details>

**P1.12** ¿Con qué dos mecanismos se cierran los huecos de esa regla?
<details><summary>Respuesta</summary>OIDC solo entrega credenciales a tokens con `environment:production` (y `job_workflow_ref` de la plantilla); los environments se definen como código en Terraform, gestionados por Plataforma.</details>

**P1.13** ¿Por qué propones dos herramientas para el canary y cuándo usas cada una?
<details><summary>Respuesta</summary>No se impone tecnología: si ya usan Argo CD, Argo Rollouts (no exige Argo CD); si ya tienen service mesh, Flagger lo automatiza sin tocar los Deployments.</details>

**P1.14** Recita los tres umbrales de alerta del SRE Workbook con su ventana y su acción.
<details><summary>Respuesta</summary>14,4× en 1 h → page · 6× en 6 h → page · 1× en 3 días → ticket.</details>

**Diapositivas 5 y 6 — OpenTelemetry y FinOps**

**P1.14b** Recorre el camino de la telemetría de izquierda a derecha, nombrando cada pieza.
<details><summary>Respuesta</summary>Apps (enmascaran su PII) → agente DaemonSet → gateway capa 1 (loadbalancing por traceID) → gateway capa 2 (imagen OCB: redaction, spanmetrics + servicegraph, tail_sampling) → backend del banco por OTLP + mTLS. Aparte: conector del core con traceparent y pipeline de auditoría.</details>

**P1.15** ¿Por qué el gateway necesita dos capas?
<details><summary>Respuesta</summary>El tail sampling necesita la traza completa; la capa 1 enruta por traceID para que todos los spans de un pago lleguen a la misma réplica de la capa 2.</details>

**P1.16** ¿Por qué no das cifra de ahorro y qué dos casos públicos citas?
<details><summary>Respuesta</summary>Sin la línea base de Banco Plus sería inventarla. Capital One: ~70% menos volumen de trazas con OpenTelemetry. Pismo (pagos): ~80% menos costo de observabilidad con tail sampling.</details>

**Diapositivas 7 y 8 — IA**

**P1.17** Nombra las cinco herramientas del servidor MCP y cuál es la más valiosa.
<details><summary>Respuesta</summary>obtener_grafo, consultar_slo, buscar_trazas, buscar_logs(trace_id), cambios_recientes. La más valiosa: cambios_recientes (la alimenta el Quality Gate).</details>

**P1.18** Lo nuevo crece alrededor de lo viejo y lo va reemplazando por partes, sin "big bang". ¿Cómo se llama el patrón y por qué justifica un MCP propio?
<details><summary>Respuesta</summary>Strangler fig. Las herramientas MCP responden igual sobre telemetría vieja o nueva: la IA sirve desde el día uno.</details>

**P1.19** Distingue modelo, canal y modo de ejecución del agente de RCA.
<details><summary>Respuesta</summary>Modelo: Claude o Gemini. Canal: Amazon Bedrock o Vertex AI en la cuenta del banco. Modo: automático, disparado por la alerta, dentro del banco (más el modo interactivo).</details>

**P1.20** Aplica la regla de causa raíz al ejemplo: ¿por qué la API de pagos no es la causa?
<details><summary>Respuesta</summary>La causa es el nodo anómalo más profundo con dependencias sanas. La API de pagos tiene una dependencia anómala (Antifraude): es víctima.</details>

**Diapositivas 9 y 10 — Incidentes y cierre**

**P1.21** ¿Cuáles son los roles mínimos y la única regla que no se negocia?
<details><summary>Respuesta</summary>Incident Commander + responsable técnico (comunicaciones solo si hace falta, casi siempre en SEV1). El IC no arregla.</details>

**P1.22** Recita el menú de mitigación si no hay un cambio claro.
<details><summary>Respuesta</summary>Apagar el feature flag, failover a la otra nube, load shedding, circuit breaker.</details>

**P1.23** Recita la hoja de ruta con sus cuatro hitos.
<details><summary>Respuesta</summary>Fase 0 (2–4 semanas) caracterizar lo que existe · 30 días SLO calibrado + burn rate · 60 días Quality Gate + gateway con PII · 90 días tail sampling medido + servidor MCP.</details>

### 1.3 Defender las decisiones (simulacro de mesa)

Responde como en la mesa, en menos de 45 segundos. Las respuestas modelo están en [contraargumentos.md](contraargumentos.md).

| # | Pregunta de la mesa | Decisión |
|---|---|---|
| P1.24 | "Soy administrador del repo: le quito la regla al environment." | D7 |
| P1.25 | "¿Por qué canary y no Blue/Green, si el rollback de Blue/Green es instantáneo?" | D4, D8-bis |
| P1.26 | "No tenemos Argo CD." | D8 |
| P1.27 | "Si cada aplicación ya enmascara la PII, ¿para qué el gateway?" | D14 |
| P1.28 | "¿Por qué no Mimir? Ya tenemos Prometheus + Thanos." | D15 |
| P1.29 | "Entonces, ¿cuánto nos vamos a ahorrar?" | D17 |
| P1.30 | "¿Los datos del banco entrenan el modelo? ¿Y si la IA se equivoca?" | D19 |
| P1.31 | "El estándar tiene más roles: Comms Lead, Scribe..." | D23 |
| P1.32 | "¿La Fase 0 no es perder un mes?" | D27 |
| P1.33 | "Se acabó el Error Budget y negocio exige lanzar el viernes." | D4 |

### 1.4 Ensayos

- **Ensayo 1:** leyendo el guion, cronometrado por diapositiva (meta: ~16 minutos).
- **Ensayo 2:** sin guion, solo con las diapositivas (meta: menos de 20 minutos).
- **Simulacro:** 10 minutos de preguntas al azar de 1.3 y de la Parte 2.

---

## Parte 2 — Reforzar lo flojo

Ordenado por prioridad: primero lo 🔴 que aparece en la presentación, después lo 🟡.

| # | Tema (progreso.md) | Nivel hoy | Meta | Preguntas |
|---|---|---|---|---|
| 67 | Error Budget Policy, Quality Gate, progressive delivery | 🔴 | 🔵 | P2.1–P2.4 |
| 68 | OpenTelemetry Collector por dentro | 🔴 | 🟢 | P2.5–P2.8 |
| 69 | Agente vs. gateway, OpenTelemetry Operator | 🔴 | 🟢 | P2.9–P2.10 |
| 70 | Head vs. tail sampling | 🔴 | 🔵 | P2.11–P2.12 |
| 71 | Propagación de contexto | 🔴 | 🟢 | P2.13–P2.14 |
| 72 | FinOps: cardinalidad, Log-to-Metrics | 🔴 | 🟢 | P2.15–P2.16 |
| 74 | Semantic Conventions, exemplars, service graph | 🔴 | 🟢 | P2.17–P2.19 |
| 78 | Toil, chaos engineering | 🔴 | 🟢 | P2.20–P2.21 |
| 80 | Modelo C4 | ⬜ | 🟢 | P2.22–P2.23 |
| 64–66 | SLI/SLO/SLA, Golden Signals, burn rate | 🟡 | 🔵 | P2.24–P2.27 |
| 73 | PII: técnicas de enmascaramiento | 🟡 | 🟢 | P2.28 |
| 75–76 | MCP, prompt injection, grafos | 🟡 | 🟢 | P2.29–P2.30 |
| 77 | Incident Command y post-mortem | 🟡 | 🔵 | P2.31–P2.32 |
| 79 | Idempotencia, RTO/RPO, percentiles | 🟡 | 🟢 | P2.33–P2.35 |
| — | Licencias y herramientas nuevas de la revisión | ⬜ | 🟡 | P2.36–P2.38 |

**67 — Error Budget Policy y progressive delivery**

**P2.1** Es un acuerdo firmado con negocio que dice qué pasa con los despliegues según cuánto presupuesto de errores queda. ¿Cómo se llama?
<details><summary>Respuesta</summary>Error Budget Policy (en el repaso final dijiste "SLA": el SLA es el contrato con el cliente, con penalidades).</details>

**P2.2** Herramienta que automatiza el canary sobre un service mesh existente, sin reemplazar los Deployments. ¿Nombre?
<details><summary>Respuesta</summary>Flagger.</details>

**P2.3** Ordena por gasto de Error Budget si la versión nueva sale mala: Blue/Green, canary, shadow, recreate.
<details><summary>Respuesta</summary>Shadow (ninguno) < canary (fracción × minutos) < Blue/Green (todos × segundos, si el rollback es automático) < recreate (caída segura).</details>

**P2.4** Patrón para cambiar el esquema de base de datos sin romper el rollback: primero agregas, luego migras, al final borras. ¿Nombre?
<details><summary>Respuesta</summary>Expand/contract (parallel change).</details>

**68 — Collector por dentro**

**P2.5** Recita los cuatro tipos de componentes del Collector y qué hace cada uno.
<details><summary>Respuesta</summary>Receivers (reciben), processors (transforman/filtran), exporters (envían), connectors (unen pipelines y cambian de señal, por ejemplo spans → métricas).</details>

**P2.6** Un componente lee trazas y produce métricas de tasa, errores y duración. ¿Es processor o connector? ¿Cómo se llama?
<details><summary>Respuesta</summary>Connector: `spanmetrics` (regla: si cambia de señal, es connector).</details>

**P2.7** ¿Qué processor va primero en el pipeline y por qué?
<details><summary>Respuesta</summary>`memory_limiter`: protege al Collector de quedarse sin memoria antes de hacer cualquier trabajo.</details>

**P2.8** Recita los puertos de OTLP por gRPC y por HTTP.
<details><summary>Respuesta</summary>4317 (gRPC) y 4318 (HTTP).</details>

**69 — Despliegue del Collector**

**P2.9** Componente de Kubernetes que inyecta la auto-instrumentación de OpenTelemetry con una anotación en el pod. ¿Nombre?
<details><summary>Respuesta</summary>OpenTelemetry Operator (en el repaso dijiste "Istio").</details>

**P2.10** El gateway se cae en plena crisis. Nombra cuatro mecanismos de resiliencia.
<details><summary>Respuesta</summary>Varias réplicas con HPA, `sending_queue` persistente con reintentos, `memory_limiter`, buffer en los agentes, meta-monitoreo del Collector.</details>

**70 — Muestreo**

**P2.11** ¿Cuál de los dos muestreos puede botar justo la traza que iba a fallar, y por qué?
<details><summary>Respuesta</summary>Head-based: decide al inicio, antes de saber cómo termina la traza. Tail-based decide al final y conserva los errores.</details>

**P2.12** ¿Por qué un balanceo round-robin entre réplicas rompe el tail sampling?
<details><summary>Respuesta</summary>Los spans de una traza quedan repartidos; ninguna réplica ve la traza completa. Se arregla con `loadbalancing` por traceID.</details>

**71 — Propagación de contexto**

**P2.13** Header estándar del W3C que lleva el ID de la traza entre servicios. ¿Nombre? ¿Y el formato antiguo de Zipkin?
<details><summary>Respuesta</summary>`traceparent` (W3C Trace Context); B3.</details>

**P2.14** En Kafka, ¿cómo se conecta el span del productor con el del consumidor sin acoplarlos?
<details><summary>Respuesta</summary>El contexto viaja en los headers del mensaje de Kafka; el consumidor crea un span con span link al del productor (no llama al productor).</details>

**72 — FinOps de telemetría**

**P2.15** Una etiqueta de métrica con el número de cliente crea una serie nueva por cliente. ¿Cómo se llama el problema?
<details><summary>Respuesta</summary>Explosión de cardinalidad. Los IDs van en trazas y logs, no en métricas.</details>

**P2.16** ¿Por qué recortar la retención a la mitad es mala primera medida?
<details><summary>Respuesta</summary>Recorta a ciegas y no ataca el origen del volumen. Primero se reduce lo que entra; la retención se escalona por niveles.</details>

**74 — Datos AI-Ready**

**P2.17** Convenciones de OpenTelemetry para que todo el banco llame igual a lo mismo. ¿Nombre?
<details><summary>Respuesta</summary>Semantic Conventions.</details>

**P2.18** Un pico en una métrica guarda el ID de una traza de ejemplo. ¿Cómo se llama?
<details><summary>Respuesta</summary>Exemplar.</details>

**P2.19** ¿Qué connector arma el grafo de servicios y qué parte construimos nosotros?
<details><summary>Respuesta</summary>`servicegraph` (del Collector). Nosotros: la herramienta MCP `obtener_grafo`.</details>

**78 — Toil y caos**

**P2.20** Trabajo manual, repetitivo, automatizable y que crece con el servicio. ¿Nombre? ¿Y el límite de Google?
<details><summary>Respuesta</summary>Toil; por debajo del 50% del tiempo del equipo.</details>

**P2.21** Herramienta de Netflix que apaga instancias al azar en producción. ¿Y cómo se llama el ejercicio programado de caos con el equipo?
<details><summary>Respuesta</summary>Chaos Monkey; Game Day (no es una prueba de carga).</details>

**80 — Modelo C4**

**P2.22** Recita los cuatro niveles del modelo C4.
<details><summary>Respuesta</summary>Context, Container, Component, Code.</details>

**P2.23** ¿Qué nivel usas en la diapositiva 2 y cuál en la 5, y por qué no Component?
<details><summary>Respuesta</summary>Diapositiva 2: Context; diapositiva 5: Container. Para una mesa de decisión bastan esos; Component lo dibuja cada tribu en su repositorio.</details>

**64–66 — SLOs y burn rate**

**P2.24** Recita las cuatro Golden Signals y los métodos RED y USE.
<details><summary>Respuesta</summary>Latency, Traffic, Errors, Saturation. RED: Rate, Errors, Duration (servicios). USE: Utilization, Saturation, Errors (recursos).</details>

**P2.25** Dos servicios de 99% en paralelo, independientes: ¿qué disponibilidad dan?
<details><summary>Respuesta</summary>1 − 0,01² = 99,99%.</details>

**P2.26** ¿Qué significa un burn rate de 14,4 y cuánto presupuesto consume en una hora?
<details><summary>Respuesta</summary>Se gasta 14,4 veces más rápido de lo sostenible; en 1 hora consume el 2% del presupuesto mensual (agota el mes en ~2 días).</details>

**P2.27** ¿Por qué la alerta lleva dos ventanas (larga y corta)?
<details><summary>Respuesta</summary>La larga confirma que es serio (no un pico); la corta hace que la alerta se apague rápido cuando se arregla.</details>

**73 — PII**

**P2.28** Necesitas correlacionar eventos de un mismo cliente sin guardar su cédula. ¿Qué técnica usas? ¿Y qué permite PCI DSS mostrar de una tarjeta?
<details><summary>Respuesta</summary>Hash con sal; los primeros 6 y los últimos 4 dígitos.</details>

**75–76 — MCP y grafos**

**P2.29** Un atacante escribe instrucciones en la descripción de una transferencia y la IA las lee en un log. ¿Cómo se llama el ataque y cuáles son tres defensas?
<details><summary>Respuesta</summary>Indirect Prompt Injection. Solo lectura, tratar los logs como datos (no instrucciones), humano en el bucle, auditoría.</details>

**P2.30** Dos nodos anómalos en ramas distintas del grafo. ¿Qué sospechas?
<details><summary>Respuesta</summary>Una dependencia oculta compartida que no está en el grafo (nodo de Kubernetes, red, bus de mensajes, certificado).</details>

**77 — Incidentes**

**P2.31** ¿Por qué "factores contribuyentes" y no "la causa raíz" en el post-mortem?
<details><summary>Respuesta</summary>Los sistemas complejos fallan por varios factores; una sola causa sesga hacia el último humano de la cadena.</details>

**P2.32** Patrón que corta las llamadas a una dependencia que falla y las reabre de a poco. ¿Nombre y estados?
<details><summary>Respuesta</summary>Circuit breaker: cerrado → abierto → semi-abierto.</details>

**79 — Temas aledaños**

**P2.33** Clave que manda el cliente para que un pago reintentado no se cobre dos veces. ¿Nombre? ¿Y cómo se espacian los reintentos?
<details><summary>Respuesta</summary>Idempotency key; backoff exponencial con jitter (evita la retry storm).</details>

**P2.34** Distingue RTO de RPO.
<details><summary>Respuesta</summary>RTO: cuánto tiempo puedo estar caído. RPO: cuántos datos puedo perder (hasta qué punto en el tiempo recupero).</details>

**P2.35** ¿Por qué no se promedian percentiles entre réplicas y qué tipo de métrica sí permite agregarlos?
<details><summary>Respuesta</summary>El promedio de percentiles no es un percentil; se usa un Histogram (se suman los buckets y se calcula después). El Summary no se agrega.</details>

**Herramientas y licencias nuevas (de la revisión del análisis)**

**P2.36** Herramienta que convierte un SLO escrito en YAML en Git en reglas de Prometheus. ¿Nombre? ¿Y la especificación abierta?
<details><summary>Respuesta</summary>Sloth; OpenSLO.</details>

**P2.37** ¿Qué licencia tienen Mimir, Tempo y Loki y por qué la revisa el área jurídica de un banco?
<details><summary>Respuesta</summary>AGPLv3. Uso interno sin modificar no obliga a nada, pero el área jurídica la revisa con lupa; alternativa: Grafana Enterprise o Grafana Cloud.</details>

**P2.38** ¿Qué service mesh dejó de ser gratis para empresas de más de 50 empleados, y cuál de AWS está descontinuado?
<details><summary>Respuesta</summary>Linkerd (versiones stable bajo licencia de Buoyant); AWS App Mesh (fin de soporte: 30 de septiembre de 2026).</details>

---

## Registro

Al terminar cada sesión, actualizar los niveles de los temas 64 a 80 en `../../devops-senior/examenes/registro/progreso.md` y
la sesión en `resultados.md`. El ítem 80 (Modelo C4 y presentación) sube con la Parte 1.
