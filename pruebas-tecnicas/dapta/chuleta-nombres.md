# Chuleta de nombres — Davivienda + Dapta

Leer 5 minutos antes de cada sesión. Cada nombre con su imagen para recordarlo.

- **Bloques A–E + repaso final:** prueba Davivienda (tema 25). Es la base de la Parte II del
  [banco de preguntas de Dapta](banco-preguntas.md) (repaso).
- **Bloques F–J:** lo nuevo de Dapta (tema 26), en el mismo orden que la Parte I del banco (N1–N8).
- Original de Davivienda: [`../davivienda/chuleta-nombres.md`](../davivienda/chuleta-nombres.md).

## Bloque A — SRE

| Nombre | Imagen | Qué es |
|---|---|---|
| **SLI / SLO / SLA** | Termómetro / meta / contrato | SLI mide; SLO es la meta interna; SLA promete con multa (y es **más flojo** que el SLO) |
| **Golden Signals** | "El servicio **LaTES**" (el pulso) | **La**tency, **T**raffic, **E**rrors, **S**aturation |
| **RED / USE** | RED = el síntoma; USE = la causa | RED (Rate, Errors, Duration) para servicios; USE (Utilization, Saturation, Errors) para recursos |
| **Error Budget** | Margen para fallar | 1 − SLO. 99,9% = 43,2 min/mes; cada nueve divide por 10 |
| **Serie / paralelo** | Serie resta, paralelo suma un nueve | Serie: A×B×C. Paralelo: 1 − (1−A)ⁿ (se multiplican las **fallas**) |
| **Burn rate** | Velocidad de gasto del presupuesto | Error actual ÷ (1 − SLO). 14,4 = se acaba en ~2 días |
| **Multi-window, multi-burn-rate** | Ventana larga + corta, varios niveles | 14,4× 1 h → page; 6× 6 h → page; 1× 3 días → ticket |
| **Error Budget Policy** | El "qué pasa si" firmado con negocio | Reglas por umbral: desplegar normal / solo canary / congelar |
| **Quality Gate** | La puerta del pipeline | Antes: consulta presupuesto. Durante: canary. Después: verificación |
| **Canary / Blue-Green** | Canario en la mina / dos casas | Canary: % creciente de tráfico. Blue-Green: cambio total y vuelta total |
| **Argo Rollouts / Flagger** | Los que revierten solos | Canary con análisis automático contra Prometheus |
| **Feature Flag** | Interruptor | Separa **desplegar** de **liberar** |
| **DORA** | "**DeLiCaTe**" | **De**ployment Frequency, **L**ead t**i**me, **Ca**mbio fallido = Change Failure Rate, **Te** = Time to Restore (hoy: Failed Deployment Recovery Time; ver Bloque G) |

## Bloque B — OpenTelemetry

| Nombre | Imagen | Qué es |
|---|---|---|
| **Collector** | La **cocina** completa (no es un paso) | Proceso intermedio entre las apps y los backends |
| **Receivers → Processors → Exporters** | "**RePE**": **Re**cibe, **P**rocesa, **E**xporta | Las 3 etapas, en orden |
| **Connector** | El **mesero** entre cocinas | Une pipelines y **cambia de señal** (trazas → métricas) |
| `memory_limiter` | 🚪 El **portero** (1.º siempre) | Rechaza si no hay memoria → **backpressure** |
| `filter` | 🧹 El **colador** (2.º) | Bota DEBUG y health checks |
| `redaction` | ✏️ El **redactor** que tacha (3.º) | Enmascara cédulas y tarjetas |
| `tail_sampling` | ⚖️ El **juez** (4.º): sentencia **al final** | Decide qué trazas guardar viendo la traza completa |
| `batch` | 📦 El **empacador** (último) | Agrupa antes de enviar |
| `spanmetrics` | El mesero que **cuenta todos los platos** antes del juez | Span → metrics: métricas RED exactas antes del muestreo |
| `count` | Hermano de `spanmetrics` para logs | Log-to-Metrics |
| **Agente / Gateway** | El de cada nodo / el central | Agente (DaemonSet): metadatos y logs locales. Gateway: muestreo, PII, enrutamiento |
| **Gateway de dos capas** + `loadbalancing` | La **recepcionista** que sienta a toda la familia (traceID) en la misma mesa | Capa 1 enruta por `traceID`; capa 2 hace `tail_sampling` |
| **OpenTelemetry Operator** | El que **opera** OTel en Kubernetes (nombre literal) | Inyecta auto-instrumentación con una anotación |
| **Head / Tail sampling** | Perro: **cabeza** = inicio, **cola** = final | Head: barato, pierde errores. Tail: guarda errores, necesita memoria |
| **OTLP** | El idioma nativo de OTel | Puertos **4317** (gRPC) y **4318** (HTTP) |
| **Traza / span** | Envío completo / cada tramo | Una traza (`traceID`) contiene muchos spans |
| **SpanKind** | Dos parejas y un solitario | SERVER↔CLIENT, PRODUCER↔CONSUMER, INTERNAL |
| **p99** | 1 de cada 100 clientes espera más que esto | Percentil: nunca se promedia; se calcula con histogramas |
| `traceparent` | **trace + parent** = "el **papá** de la traza" | Header W3C: `00-traceID-parentID-01` |
| **W3C / B3** | Estándar oficial / el viejo de Zipkin ("**B**ig **B**rother **B**ird") | Formatos de propagación de contexto |
| **Kafka / MQ** | Una **carta con sobre** | El `traceparent` va en el **sobre** (headers del mensaje); el consumidor usa un **span link** |
| **Explosión de cardinalidad** | Un **cajón nuevo** por cada valor distinto | Nunca IDs únicos en etiquetas de métricas |
| **AS400 (IBM i)** | El corazón viejo pero confiable | Servidor de IBM donde vive el core bancario |
| **IBM MQ** | Como SQS, pero de banco | Cola de mensajes con entrega garantizada |

## Bloque C — Telemetría para IA

| Nombre | Imagen | Qué es |
|---|---|---|
| **Semantic Conventions** | *Semántica* = **significado** | Mismos nombres de atributos en todo el banco |
| **Resource attributes** | La cédula del servicio | `service.name`, `service.version`, `deployment.environment.name`, equipo |
| **Métricas / trazas / logs** | **Qué** pasa / **dónde** / **por qué** | Las tres señales; no compiten, se encadenan |
| **Exemplars** | Un **ejemplar** de muestra, como el de una revista | Punto en la métrica con un `trace_id`: clic del pico a la traza |
| `servicegraph` | El mesero que **dibuja el mapa** | Connector: arma aristas desde parejas CLIENT→SERVER (y nodos virtuales para DB/AS400) |
| **Regla de causa raíz** | El trancón termina donde la calle está libre | El nodo anómalo **más profundo** cuyas dependencias están sanas. El que más grita es víctima |
| **Dos causas a la vez** | Sospecha de lo compartido | Buscar una dependencia oculta (mismo nodo, red, Kafka, certificado) |
| **BFS / DFS** | **B**road: piedra en el lago / **D**eep: laberinto | BFS por niveles → radio de explosión (grafo invertido). DFS al fondo → causa raíz |
| **Servidor MCP de observabilidad** | El embudo | `obtener_grafo`, `consultar_slo`, `buscar_trazas`, `buscar_logs(trace_id)`, **`cambios_recientes`** |
| **Indirect Prompt Injection** | La orden escondida en los datos (OWASP LLM01) | Defensas: mínimo privilegio, **humano en el bucle**, datos marcados como no confiables, hooks + auditoría |

## Bloque D — Incidentes y cultura

| Nombre | Imagen | Qué es |
|---|---|---|
| **Roles del incidente** | "El **comandante** manda, el **operador** opera, el **comunicador** informa, el **escriba** anota" | Incident Commander (no toca teclado), Operations Lead, Communications Lead, Scribe (+ SMEs) |
| **Mitigar antes de diagnosticar** | El jefe de bomberos no coge la manguera | Primero detener el sangrado (rollback, flag, failover); el porqué después |
| **Circuit Breaker** | El **taco** del tablero eléctrico | Cerrado → abierto (fallback) → semi-abierto (prueba). Evita fallas en cascada |
| **Load Shedding / Bulkhead** | **Deslastre de carga** (racionamiento) / **mamparos** del barco | Cortar lo no crítico (saldos) para salvar lo crítico (pagos) / aislar recursos |
| **Graceful degradation** | Tu "bypass" de la tubería | Servicio de menor calidad en vez de parar. El fallback de antifraude lo decide **Riesgo** |
| **Post-mortem blameless** | Se cuenta **qué** pasó, no **quién** | Impacto, línea de tiempo (MTTD/MTTR), causa raíz, factores contribuyentes, acciones prevenir/detectar/mitigar |
| **Timeouts largos** | Más timeout ≠ más capacidad | Un timeout largo agota hilos y propaga la falla en cascada (Ley de Little) |
| **Toil** | **T**areas **O**perativas **I**dénticas y **L**ineales | Manual, repetitivo, automatizable. Meta Google: **< 50%** del tiempo |
| **"You build it, you run it"** | Cada Tribu cuida a sus hijos | Las Tribus atienden sus SLOs; observabilidad solo si falla la plataforma |
| **Chaos Engineering** | Un **mono** suelto desconectando cables (**Chaos Monkey**) | Inyectar fallas controladas; se practica en **Game Days** (el partido amistoso) |
| **Carga vs. caos** | Mucho tráfico vs. cosas rotas | Load testing (k6, JMeter) mide capacidad; Chaos (LitmusChaos, Chaos Mesh, AWS FIS) mide resiliencia |

## Bloque E — Temas aledaños

| Nombre | Imagen | Qué es |
|---|---|---|
| **Idempotency Key** | Una clave por cada intención de pago | El reintento devuelve el mismo resultado sin cobrar dos veces |
| **Retry Storm / Thundering Herd** | La **estampida** de búfalos | Todos reintentan a la vez y vuelven a tumbar el servicio |
| **Exponential Backoff + Jitter** | La salida escalonada del estadio | Esperas crecientes (1, 2, 4, 8 s) con azar para no sincronizarse |
| **RTO / RPO** | Videojuego: cuánto tarda en **cargar** / qué tan vieja es la **partida guardada** | **T**iempo de recuperación / **P**unto de datos perdidos. Pagos: RPO ≈ 0 |
| **Estrategias DR** | De barato a caro | Backup & Restore → Pilot Light → Warm Standby → Activo-activo |
| **Percentiles** | Nunca se promedian (ni ponderados) | Usar **Histogram** (cajones que se suman); **Summary** no se agrega |
| **Ley de Little** | La fila del banco | **L = λ × W**: si la latencia ×4, la concurrencia ×4 con el mismo tráfico |
| **Seguridad de la plataforma** | Tres capas | Datos sin PII; pipeline con mTLS, receivers autenticados, secretos en Key Vault; acceso con SSO, RBAC, auditoría (Zero Trust) |
| **Ley 1581 de 2012** | "1581: tu dato es tuyo" (Habeas Data) | Datos personales en Colombia; la vigila la **SIC** |
| **SFC / SIC** | Policía de los bancos / policía de los datos | SFC: ciberseguridad, nube, terceros |
| **ISO 27001 / SOC 2 / PCI DSS** | Certificados del proveedor / tarjetas | Exigir al SaaS; tarjeta: primeros 6 y últimos 4 |
| **Well-Architected (6 pilares)** | "**Seguro, Confiable, Rápido, Barato, Operable y Verde**" | Security, Reliability, Performance Efficiency, Cost Optimization, Operational Excellence, Sustainability |

## Repaso final (12 oct.)

| Nombre | Imagen | Qué es |
|---|---|---|
| **Error Budget Policy** | La **política de gastos de la casa** cuando se acaba la plata del mes | Reglas internas, firmadas con negocio, por umbral de presupuesto (no es el SLA) |
| **ArgoCD vs. Argo Rollouts** | **Qué** versión vs. **cómo** se reemplaza | ArgoCD = GitOps; Argo Rollouts = canary por etapas con `AnalysisTemplate` y rollback |
| **Flagger** | El **árbitro de línea** que levanta la bandera | Canary con análisis y rollback (con Istio/NGINX) |
| **Ventana móvil de 28 días** | Ventana que **se desliza**, no hoja que se arranca | Sin "reset" el día 1; 28 = 4 semanas exactas |
| **OTLP: 4317 / 4318** | Alfabeto: **g**RPC (17) antes que **h**TTP (18) | Puertos del protocolo nativo de OpenTelemetry |
| **Auditoría vs. telemetría** | Evidencia legal ≠ herramienta de operación | Pipeline de auditoría completo, nunca muestreado, inmutable (**WORM**: S3 Object Lock), retención legal |
| **Roles del incidente** | El **barco en tormenta**: capitán, jefe de máquinas, radio operador, bitácora | **Incident** Commander, Operations Lead, Communications Lead, **Scribe** (2 especiales + 2 Leads) |
| **5 porqués** | Una **cadena** vs. una **red** (grafo de factores) | Lineal y termina en una persona; complementar con factores contribuyentes y "¿qué lo hizo parecer razonable?" |
| **Modelo C4** | **País → ciudad → barrio → casa** (Google Maps) | **C**ontext, **C**ontainer (cualquier cosa desplegable, no Docker), **C**omponent, **C**ode. En la presentación: Context + Container |

---

# Dapta — Seguridad de la plataforma ("defensa")

## La propuesta en 3 nombres

| Nombre | Imagen | Qué es |
|---|---|---|
| **"Una carretera pavimentada, no un peaje"** | El camino fácil **es** el camino seguro | El lema: la seguridad viene dentro de la plataforma, no como un cobro aparte |
| **Golden path + compliance as code** | El **camino dorado** que además deja **recibo** | Platform Engineering donde cada despliegue genera solo su evidencia para el auditor |
| **Los 4 pilares: "D-P-D-IA"** | **D**esplegar, **P**lataforma, **D**etectar, **IA** | GitOps · Kubernetes y Temporal seguros · detección en AWS · seguridad propia de la voz con IA |

## Bloque F — Certificaciones y cumplimiento

| Nombre | Imagen | Qué es |
|---|---|---|
| **SOC 2** (System and Organization Controls 2) | Un **boletín de notas** firmado por un contador, no un diploma | **Atestación**, no certificación. La emite una firma CPA (Certified Public Accountant) bajo normas del AICPA |
| **Type I / Type II** | **Foto** / **video** | Type I: diseño de los controles en un día. Type II: diseño **y funcionamiento** durante 3–12 meses. Dapta: Type II de solo 3 meses (may.–ago. 2026) |
| **Trust Services Criteria (5)** | Una casa: **Security** es la **puerta** (obligatoria); las otras 4 son cuartos opcionales | Security, Availability, Processing Integrity, Confidentiality, Privacy. El siguiente para Dapta: **Availability** (vende SLAs en Enterprise) |
| **Excepción** | Una **mancha** en el boletín que lee el comprador | Control que falló en la muestra del auditor; queda escrita en el informe |
| **Bridge letter** | El **puente** entre dos informes | Carta de la gerencia que cubre el hueco entre el fin del periodo y el siguiente informe |
| **Carve-out / CUECs / CSOCs** | **Recortar** a AWS de la foto / la tarea que le toca al **cliente** / la tarea que le toca a **AWS** | Carve-out: el subservice provider queda fuera del alcance (opuesto: *inclusive*). CUECs: Complementary User Entity Controls. CSOCs: Complementary Subservice Organization Controls |
| **ISO/IEC 27001:2022** | Un **sistema que mejora solo**, no una lista de chequeo. Certificado de 3 años | **SGSI** (Sistema de Gestión de Seguridad de la Información; ISMS). **Declaración de Aplicabilidad** (SoA). Anexo A: 93 controles en 4 temas. Etapa 1 (papeles) → etapa 2 (práctica) → seguimiento anual |
| **HIPAA / PHI / BAA** | El hospital: el dato del paciente (**PHI**) solo viaja con **contrato de socio** (**BAA**) | Health Insurance Portability and Accountability Act; Protected Health Information; Business Associate Agreement. **No hay certificado oficial**; **HITRUST** sí es certificable |
| **PCI DSS 4.0.1 + DTMF masking** | La tarjeta se marca con el **teclado** y los tonos se **tapan**: nunca pasa por el LLM | Payment Card Industry Data Security Standard. Lo correcto es **sacar la tarjeta del alcance** |
| **ISO/IEC 42001:2023** | "**42**, la respuesta a todo"… ahora en IA | AIMS (AI Management System). Diferenciador para Dapta, pero va después |
| **DPA / SCCs** | El contrato del **encargado** / las cláusulas para **sacar** datos de Europa | Data Processing Agreement (art. 28 del GDPR); Standard Contractual Clauses |
| **SIG Lite / CAIQ** | La **hoja de cálculo gigante** del comprador | Standardized Information Gathering (Shared Assessments); Consensus Assessments Initiative Questionnaire (Cloud Security Alliance). Se responden una vez y se reutilizan |
| **STRIDE** | *Stride* = **zancada**: el atacante da 6 pasos | Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Modelo de amenazas de Microsoft |
| **Vanta** | El **vigilante con cámara**: ve y graba, pero no arregla | Compliance automation: conecta AWS, GitHub y Google Workspace, recolecta evidencia y arma el trust center. **No hace** los controles |
| **Trust center** | La **vitrina** | `trust.dapta.ai`: 79 controles (ninguno de IA), 30 subprocesadores |

## Bloque G — DORA y proceso de desarrollo

| Nombre | Imagen | Qué es |
|---|---|---|
| **DORA** (DevOps Research and Assessment) | "**DeLiCaTe**" + el **Re**trabajo | Deployment Frequency, Lead Time for Changes (velocidad) · Change Failure Rate, **Failed Deployment Recovery Time** (estabilidad). Quinta del modelo reciente: **Rework Rate** |
| **Ley de Goodhart** | Si el termómetro se vuelve meta, la gente **calienta el termómetro** | No fijar metas con DORA; ver tendencias del equipo, nunca comparar personas |
| **Four Keys** | Las **cuatro llaves** = las 4 métricas | Proyecto abierto de Google para medir DORA. En Dapta: API de GitHub + Argo CD → Grafana; LinearB/Sleuth solo si no basta |
| **Trunk-Based Development** | Todos al **tronco** del árbol; las ramas viven horas, no semanas | Integrar a `main` varias veces al día, lotes pequeños |
| **Feature Flags en PostHog** | El interruptor que **ya pagan** | Separa desplegar de lanzar; cero proveedores nuevos |
| **Evals** | El **examen** del agente antes de salir a llamar | Conversaciones de prueba con resultado esperado. Un cambio de prompt o de modelo **es un despliegue** |
| **Ambientes efímeros** | **Efímero** = vive un día, como la flor | Un namespace por pull request que se destruye al cerrarlo |
| **DUCOREA** | Las 7 preguntas antes de comprar | **D**olor, **U**sar lo que hay, **Co**sto, **O**peración, **Re**versibilidad, **E**videncia, **A**dopción |
| **Tool sprawl / YAGNI** | El **cajón de herramientas** que nadie opera / "no lo vas a necesitar" | Cada SaaS nuevo = un subprocesador más que auditar. You Aren't Gonna Need It |
| **Puerta de una vía / dos vías** | Puerta que se **cierra con llave** detrás / puerta **giratoria** | Irreversible: con calma. Reversible: rápido |
| **ADR** (Architecture Decision Record) | El **acta** de la decisión | Contexto, opciones, decisión, consecuencias. También es evidencia de "Development lifecycle established" |

## Bloque H — Estabilidad: Temporal, voz y dependencias

| Nombre | Imagen | Qué es |
|---|---|---|
| **Workflow / Activity** | El **director de orquesta** (no improvisa) / los **músicos** que tocan | Workflow: orquesta y **debe ser determinista**. Activity: hace el trabajo con efectos (llamadas, APIs). = orchestrator / activity de Durable Functions |
| **Replay + Event History** | Volver a ver la **grabación del partido** para saber dónde iba | El workflow se reconstruye leyendo su historia; por eso no usa hora, aleatorios ni red |
| **Workers / Task Queues** | Los **trabajadores** que tú contratas / la **fila** de pedidos | Temporal **no ejecuta tu código**: tus workers (en Kubernetes) toman tareas de las colas |
| **Retry Policy + timeouts** | Reintentar con **paciencia creciente** y con reloj | Backoff declarativo; Start-To-Close, Schedule-To-Close |
| **Versionado** (patching / Worker Versioning) | No cambiarle la **partitura** a una canción que ya se está tocando | Cambiar un workflow con ejecuciones en curso rompe el replay |
| **Continue-As-New** | **Pasar a cuaderno nuevo** cuando el viejo se llenó | Corta historias demasiado largas |
| **Payload Codec / Codec Server** | **Candado** en la carta antes de mandarla / la **llave** para leerla en la UI | Cifrado del lado del cliente: Temporal Cloud solo ve texto cifrado |
| **WebRTC / SIP / SIP trunk** | Voz por el **navegador** / el **teléfono** de toda la vida / la **troncal** a la red telefónica | Web Real-Time Communication; Session Initiation Protocol. LiveKit y Twilio |
| **SLIs de la llamada** | Lo que siente **quien llama** | ① la llamada conecta · ② el agente responde rápido (p95 por turno) · ③ el flujo de Flow Studio termina bien |
| **Status page** | El **marcador** público del partido | Se calcula desde los SLIs; 100% con 5 incidentes visibles = nadie le cree |
| **Failover entre LLMs** | La **llanta de repuesto** ya inflada (probada con evals) | Timeouts + circuit breaker por proveedor + modelo de respaldo evaluado de antemano |

## Bloque I — Plataforma Kubernetes y despliegue seguro

| Nombre | Imagen | Qué es |
|---|---|---|
| **OIDC GitHub → AWS** (OpenID Connect) | Un **pase de visitante de un día**, no una llave copiada | GitHub emite un token de corta vida que AWS cambia por un rol: cero llaves en el CI |
| **GitOps + Argo CD** | El clúster **jala** (pull) desde Git; nadie empuja a mano | Sin `kubectl apply` manual; Git = evidencia de change management. Alternativa: Flux |
| **Drift** | La **deriva** del barco | Diferencia entre lo que dice Git y lo que corre en el clúster; Argo CD la corrige |
| **Kyverno: Audit → Enforce** | El policía que primero **avisa** y después **multa** | Políticas en **YAML**. Alternativa: OPA/Gatekeeper (en **Rego**) |
| **IRSA / EKS Pod Identity** | Cada pod con su **carné** de AWS | IRSA (IAM Roles for Service Accounts): federación OIDC por clúster. Pod Identity: lo nuevo y más simple (agente + *associations*) |
| **External Secrets Operator + Secrets Manager** | El **mensajero** que trae el secreto de la **caja fuerte** | Los secretos viven en AWS Secrets Manager y llegan al clúster sin pasar por Git |
| **Trivy / Dependabot / secret scanning + push protection** | El **detector de metales** de la imagen / el que avisa de **piezas vencidas** / el que **frena** el push con una llave adentro | Escaneo nativo de GitHub primero; Semgrep (SAST) solo si hace falta |
| **Cosign (Sigstore)** | La **firma** en la imagen; firmar sin verificar no sirve | Segunda vuelta: cuando Kyverno pueda exigir la firma |
| **Helm** | El **timón** que lleva el mismo barco a otro puerto | Chart portable: por qué EKS y no ECS (el **on-premise** de Enterprise) |
| **CloudTrail / GuardDuty / Security Hub** | La **cámara** que graba todo / el **guardia** de turno / el **tablero** central | Registro organizacional en cuenta aparte · detección (con EKS Runtime Monitoring) · hallazgos → Slack. SIEM **todavía no** |
| **IAM Identity Center** | **Una sola puerta** con SSO para todas las cuentas | Revisión trimestral de accesos desde Vanta |

## Bloque J — IA de voz y telefonía en EE. UU.

| Nombre | Imagen | Qué es |
|---|---|---|
| **Prompt injection** (LLM01) | "Ignora tus instrucciones…" dicho **por teléfono** | OWASP Top 10 for LLM Applications. Una instrucción al LLM **no es un control** |
| **Excessive Agency** | Darle al agente **las llaves de toda la casa** | Herramientas con mínimo privilegio, limitadas al contacto/tenant |
| **Preview → commit** | Mostrar el **borrador** antes de firmar | Dapta MCP: 19 de 139 herramientas son destructivas y usan este patrón |
| **ZDR** (Zero Data Retention) | El proveedor **lee y olvida** | Acuerdos de no retención ni entrenamiento con OpenAI, Anthropic, Gemini, Groq + registro de qué dato va a qué proveedor |
| **URLs firmadas** (S3 pre-signed) | Boleta con **fecha de vencimiento** | Arreglo del "Public call link": vence en minutos/horas, apagado por defecto, log de accesos |
| **TCPA** (Telephone Consumer Protection Act) | La ley de **1991** que en **2024** (FCC) alcanzó a las voces de IA | Consentimiento previo, horarios, *Do Not Call*, decir que es una IA. Multa **por llamada** |
| **STIR/SHAKEN** | "**Agitado, no revuelto**" (James Bond): el número va **firmado** | Atestación A, B, C; si falla, la llamada sale como "Spam Likely" |
| **A2P 10DLC** | **App → Persona** desde un número de **10 dígitos** | Application-to-Person 10-Digit Long Code: registro de marca y campaña en The Campaign Registry para SMS |
