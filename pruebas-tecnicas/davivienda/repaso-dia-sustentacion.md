# Repaso del día de la sustentación (2026-10-20)

Lo que quedó flojo en el repaso del 19 y lo que no alcanzamos a ver, en el orden de la presentación.
Para leer en voz alta antes de entrar. Lista completa con niveles: [lista-repaso.md](lista-repaso.md).

## 0. Las listas que abren y cierran la presentación

**Las 10 preguntas del hilo:** 1. ¿Por qué el pago QR no es confiable hoy? 2. ¿Dónde duele en la arquitectura?
3. ¿Qué es "estar bien" para el cliente? 4. ¿Cómo evitamos que un despliegue lo rompa? 5. ¿De dónde salen los
datos? 6. ¿Cómo los vemos sin pagar de más? 7. ¿Cómo hacemos que una IA los entienda? 8. ¿Cómo encuentra la IA
dónde nace la falla? 9. ¿Qué hacemos cuando, aun así, falla en hora pico? 10. ¿Cómo aprendemos para que no vuelva
a pasar?

**Los 4 ejes:** 1. SLOs (Service Level Objectives), Error Budgets y Quality Gates. 2. Telemetría con OpenTelemetry
y FinOps (−30% de costo). 3. Datos AI-Ready, MCP (Model Context Protocol) e IA causal para RCA (Root Cause
Analysis). 4. Incident Commander y post-mortem blameless.

**Las 5 reglas:** 1. Ningún número inventado. 2. Lo que el banco ya tiene no se escoge, se integra. 3. Lo que
proponemos se nombra. 4. Plataforma es habilitador: el piso, no el techo. 5. No mencionar sistemas que el caso no
nombra.

**Causa común:** no hay una definición compartida de "estar bien" ni datos estandarizados para saber cuándo
dejamos de estarlo.

**Hoja de ruta:** Fase 0 (2–4 semanas): caracterizar lo que existe → 30 días: SLO calibrado + alertas de burn
rate → 60 días: Quality Gate + gateway con PII → 90 días: tail sampling medido + servidor MCP.

## 1. Eje 1 — Lo que quedó flojo

| Nombre | En una frase |
|---|---|
| **Deployment protection rule** | El portero del environment `production`: antes de cada despliegue le pregunta a la app de Plataforma si queda Error Budget. Vive fuera del YAML de la tribu. |
| **OIDC (OpenID Connect)** | GitHub firma un carné temporal; la nube solo entrega credenciales si el carné dice `environment: production`. |
| **`job_workflow_ref`** | Dato del carné OIDC: "¿de dónde vienes?". Exige que el job salga de la plantilla oficial de Plataforma. |
| **Terraform** | El plano del edificio: el environment y su regla están como código; si alguien quita la regla a mano, Terraform la vuelve a poner. |
| **Flagger** | Mueve **tráfico** entre dos versiones montado sobre un service mesh (Istio + sidecar **Envoy**). No es feature flag. |
| **Argo Rollouts** | Canary sin service mesh: reemplaza el Deployment por un recurso `Rollout`. No exige Argo CD. |
| **Feature flag** (Flipt) | Mueve **funciones** dentro de una sola versión, por usuario. Primera opción de mitigación. |
| **Expand/contract** | Agrandar el esquema, convivir (dual write + backfill), y solo al final borrar. El rollback se pierde en el *contract*. |

**Respuesta lista — "soy admin, le quito la regla":** *"Quitar la regla no le sirve, porque la seguridad no está en
el repo. La nube solo entrega credenciales por OIDC si el carné dice `environment: production` y el
`job_workflow_ref` apunta a la plantilla oficial. Y el environment está en Terraform: si alguien quita la regla,
Terraform la vuelve a poner y queda en la auditoría."*

**Si te dicen que despliegan con otra plataforma o con CAB (Change Advisory Board):** *"Perfecto, el gate vive ahí:
antes de ofrecer la ventana consulta el Error Budget. Es segregación de funciones; cambia el lugar del portero, no
la lógica."* Con Error Budget sano, un canary puede pasar a cambio estándar preaprobado.

**Error Budget Policy** (no "agreement", no SLA): sano → canary normal · en riesgo → solo canary lento · crítico →
congelado salvo confiabilidad · agotado → congelado + post-mortem. Alertas del SRE Workbook: **14,4× en 1 h → page ·
6× en 6 h → page · 1× en 3 días → ticket**. 14,4× durante 1 h = 2% del presupuesto del mes.

**Sloth** convierte un SLO escrito en YAML en reglas de Prometheus; la especificación abierta es **OpenSLO**.

## 2. Ejes 2 — El Collector (lo más flojo)

**Regla del gas:** **processor** = filtro en la tubería (entra traza, sale traza). **Connector** = planta gas →
electricidad (entra traza, sale métrica). **Collector** = la cocina entera; no confundir con connector.

Orden en el gateway: `memory_limiter` (portero, primero, hace backpressure) → `filter` → `redaction` → `tail_sampling`
→ `batch` (último). `spanmetrics` y `servicegraph` son connectors y ven el 100% **antes** del muestreo.

**OTLP** = el camión (app → Collector): **4317 gRPC, 4318 HTTP**. **`traceparent`** = la etiqueta entre servicios
(W3C Trace Context; el formato viejo de Zipkin es **B3**). En Kafka el `traceparent` viaja en los **headers del
mensaje** y el consumidor crea un **span link** (no llama al productor).

**OpenTelemetry Operator**: lee la anotación del pod e inyecta la auto-instrumentación; también administra los
Collectors. La tribu no cambia código; solo agrega atributos de negocio si quiere.

## 3. Lo que no alcanzamos a ver (ítems 11–27)

**Muestreo (#11–12).** **Head-based**: decide al inicio, al azar, y puede botar justo la traza que iba a fallar.
**Tail-based**: espera a que termine la traza y conserva errores y lentas. Necesita la traza completa en una sola
réplica: por eso el gateway tiene **dos capas**; la capa 1 usa el exporter **`loadbalancing` por traceID**. Con
round-robin, los spans quedan repartidos y el tail sampling se rompe.

**FinOps (#14–15).** **Explosión de cardinalidad**: una etiqueta con el ID de cliente crea una serie por cliente;
los IDs van en trazas y logs, nunca en métricas. **Log-to-Metrics**: convertir logs repetitivos en contadores
(connector `count`). Red flag: recortar la retención a la mitad como primera medida; primero se reduce lo que entra
y la retención se escalona por niveles. **Sin cifra de ahorro**: Capital One ~70% menos volumen de trazas;
Pismo (pagos) ~80% menos costo con tail sampling. La cifra de Banco Plus sale de la Fase 0.

**Datos AI-Ready (#16–17).** **Semantic Conventions**: que todo el banco llame igual a lo mismo (`service.name`,
`http.response.status_code`). **Exemplar**: un punto del pico de una métrica que guarda un `trace_id`; clic del
pico a la traza y de la traza al log.

**IA (#18–19).** **Strangler fig**: lo nuevo crece alrededor de lo viejo y lo reemplaza por partes; las
herramientas MCP responden igual sobre telemetría vieja o nueva. Herramientas del servidor MCP: `obtener_grafo`,
`consultar_slo`, `buscar_trazas`, `buscar_logs(trace_id)` y **`cambios_recientes`** (la más valiosa; la alimenta el
Quality Gate). **Regla de causa raíz**: el nodo anómalo más profundo con dependencias sanas; el que más grita es
víctima. **Indirect prompt injection**: instrucciones escondidas en un log; defensas: solo lectura, datos marcados
como no confiables, **humano en el bucle**, auditoría. Modelo (Claude o Gemini) ≠ canal (Amazon Bedrock o Vertex
AI) ≠ modo (automático por alerta). La IA propone, el IC decide.

**Incidentes (#20–22).** **Incident Commander** coordina y **no arregla**; con él, un responsable técnico;
comunicaciones solo si hace falta (casi siempre en SEV1). Si te dicen "faltan Comms Lead, Scribe": *"son roles, no
personas; en un SEV1 grande se agregan"*. Menú de mitigación: apagar el feature flag → failover a la otra nube →
**load shedding** (rechazar parte del tráfico para salvar el resto) → **circuit breaker** (cerrado → abierto →
semi-abierto). Post-mortem: "factores contribuyentes", no "la causa raíz".

**Temas aledaños (#23–26).** **RTO** (Recovery Time Objective): cuánto tiempo puedo estar caído. **RPO** (Recovery
Point Objective): cuántos datos puedo perder. **Idempotency key**: el cliente la manda para que un pago
reintentado no se cobre dos veces; reintentos con **backoff exponencial + jitter** para evitar la retry storm.
**Toil**: trabajo manual, repetitivo, automatizable que crece con el servicio (Google: menos del 50%). **Chaos
Monkey** apaga instancias al azar; **Game Day** es el ejercicio programado de caos con el equipo (no es prueba de
carga).

**Otras listas.** Golden Signals: **Latency, Traffic, Errors, Saturation** ("LaTES"). DORA (DevOps Research and
Assessment): **Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore** ("DeLiCaTe").
Modelo **C4**: Context, Container, Component, Code; diapositiva 2 = Context, diapositiva 5 = Container.

## 4. Las preguntas más probables de la mesa

| Te dicen | Respondes |
|---|---|
| "¿Cuánto nos vamos a ahorrar?" | Sin sus datos no doy cifra; en la Fase 0 se mide. Casos públicos: Capital One, Pismo. |
| "Si cada app enmascara la PII, ¿para qué el gateway?" | Defensa en profundidad y único punto auditable (SFC, SIC). `redaction` en lista permitida; hash con sal para correlacionar. |
| "Ya tenemos Prometheus + Thanos." | Se mantiene Thanos; resuelve lo mismo que Mimir. Se integra, no se cambia. |
| "¿Los datos del banco entrenan el modelo?" | En Bedrock y Vertex no (verificar contrato), y al modelo solo llega telemetría sin PII. |
| "¿La Fase 0 no es perder un mes?" | Es ganarlo: evita comprar lo que existe y SLOs que nacen rotos. Entrega inventario y líneas base. |
| "Se acabó el Error Budget y negocio lanza el viernes." | La Policy se firmó antes; si negocio asume el riesgo, piloto con tope de monto y canary lento. |

## 5. Consejos para la mesa

1. Pensar dos segundos en silencio y responder una sola vez.
2. Primero el **nombre**, después la explicación. Si el nombre no sale, describir el mecanismo con seguridad.
3. Nada de "tratamos de": las reglas se cumplen.
4. No afirmar lo que no se puede sostener ("el trigger es menos estable").
5. Cambiar de opinión ante un requisito nuevo es criterio, no debilidad.
