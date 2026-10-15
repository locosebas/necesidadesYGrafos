# Libreto de la presentación — Banco Plus (versión 2)

> Diez diapositivas, veinte minutos. Cada diapositiva tiene pregunta, título, contenido, diagrama (descrito aquí y
> dibujado en [diagramas.py](diagramas.py)), guion y preguntas probables de la mesa. La presentación
> ([presentacion.html](presentacion.html)) se genera con `python3 generar-presentacion.py`.
>
> **La versión 2 aplica la revisión del [análisis de alternativas](analisis-alternativas.md)** (las razones y
> los contraargumentos están en [contraargumentos.md](contraargumentos.md)). Cinco reglas atraviesan todo el
> libreto:
>
> 1. **Ningún número inventado.** El único valor propio es el SLO de disponibilidad de partida (99,9%), dicho
>    explícitamente como punto de partida que se calibra. Las demás metas y umbrales (latencia, zonas del Error Budget, ahorro, indicadores
>    DORA) se calibran con datos en la **Fase 0**. Solo se dicen en voz alta la meta que pone el caso (−30%),
>    valores estándar con fuente (las alertas del SRE Workbook y el toil por debajo del 50%, ambos de Google) y casos públicos citados.
> 2. **Lo que el banco seguramente ya tiene no se escoge, se integra** (backend de observabilidad, on-call,
>    ITSM, motor de políticas, IDP): se nombra como ejemplo.
> 3. **Lo que sí proponemos se nombra** (GitHub Actions, Argo Rollouts o Flagger, OpenTelemetry Collector,
>    Sloth, el servidor MCP propio).
> 4. **Plataforma es un equipo habilitador:** da el piso, no el techo.
> 5. **No mencionar sistemas que el caso no nombra:** se habla del "core bancario" y de "CBU/QR", como el caso.

> **Hilo conductor:** cada diapositiva responde una **pregunta**, y su respuesta abre la pregunta de la siguiente
> (campo "Puente a la siguiente"). Cada guion **abre respondiendo su pregunta y cierra con el puente**.

| # | Diapositiva | Eje | Tiempo |
|---|---|---|---|
| 1 | Portada y la historia | — | 1,5 min |
| 2 | Contexto (C4 Context) | — | 1,5 min |
| 3 | SLIs, SLOs y Error Budget Policy | 1 | 2 min |
| 4 | Quality Gate autoejecutable | 1 | 2,5 min |
| 5 | Arquitectura OpenTelemetry (C4 Container) | 2 | 2,5 min |
| 6 | Smart Sampling y FinOps | 2 | 2 min |
| 7 | Telemetría AI-Ready y MCP | 3 | 2 min |
| 8 | Grafo de topología e IA causal | 3 | 2 min |
| 9 | Incident Commander en hora pico | 4 | 2 min |
| 10 | Post-mortem, cultura y hoja de ruta | 4 | 2 min |

---

## Diapositiva 1 — Portada y la historia (1,5 min)

**Título:** Del SLO al post-mortem: confiabilidad medible para el pago QR de Banco Plus.

**Pregunta:** ¿Por qué el pago QR de Banco Plus no es confiable hoy?
**Ejes:** todos
**Puente a la siguiente:** Si el problema es uno solo, ¿dónde lo vemos en Banco Plus?

**Contenido:**
- Una sola historia, no cuatro proyectos: cada eje alimenta al siguiente.
- El cliente define qué es "funcionar": SLO (Service Level Objective) del pago QR.
- El pipeline protege el SLO; la telemetría lo explica; la IA acelera el diagnóstico; las personas aprenden.
- Éxito medido con DORA (DevOps Research and Assessment): Change Failure Rate y Time to Restore, contra la
  línea base de la Fase 0. Telemetría: la meta del caso, −30% de costo, sin perder ninguna traza de error.

**Diagrama** (`d1` en [diagramas.py](diagramas.py)): ciclo de cuatro cajas: ① SLO + Error Budget → ② Quality Gate en
CI/CD → ③ OpenTelemetry + MCP → ④ Incident Commander + post-mortem blameless, con una flecha verde de ④ a ①:
"acciones → mejores SLOs". Al centro: "Una sola causa: falta un 'estar bien' medible y datos estandarizados".

**Guion:**
"Buenos días. Hoy les traigo una sola historia, y empieza con una pregunta: ¿por qué el pago QR de Banco
Plus no es confiable hoy? Los cuatro retos del caso (despliegues que degradan producción, una factura de
telemetría que crece sin dar visibilidad, un MTTR (Mean Time To Restore) largo y la ambición de AIOps) no son
cuatro problemas: son síntomas de uno solo. No tenemos una definición compartida de qué es 'estar bien', ni
datos estandarizados para saber cuándo dejamos de estarlo.
Por eso la propuesta es un ciclo: el SLO define qué es estar bien; el Quality Gate lo protege; OpenTelemetry
y MCP lo explican y le dan a la IA datos limpios; y el Incident Commander y el post-mortem convierten cada
crisis en un SLO mejor.
Lo mediremos con DORA, Change Failure Rate y Time to Restore, contra una línea base real, y con la meta del
caso: −30% en el costo de telemetría. Un aviso: no les voy a dar números inventados; lo que no conozco de
Banco Plus, lo mido primero. En mi experiencia anterior implementé rollback automático durante canary y un
servidor MCP de observabilidad: esto es ejecutable.
Si el problema es uno solo, ¿dónde lo vemos en Banco Plus?"

**Preguntas probables:**
1. *¿Por qué empezar por los SLOs y no por las herramientas?* — Sin SLO no hay criterio: el Quality
   Gate no sabe cuándo frenar, el sampling no sabe qué traza es importante y el Incident Commander no
   sabe qué tan grave es el incidente. Las herramientas se reemplazan; la definición de "estar bien" no.
2. *Esto suena a dos años de programa. ¿Qué entregas en 90 días?* — La hoja de ruta de la diapositiva 10:
   un servicio piloto (pago QR), una Fase 0 de caracterización de lo que ya existe y tres entregas
   medibles a 30, 60 y 90 días.

---

## Diapositiva 2 — Contexto: Banco Plus en un diagrama C4 Context (1,5 min)

**Título:** El problema: cuatro síntomas, una sola causa.

**Pregunta:** ¿Dónde duele hoy, en la arquitectura de Banco Plus?
**Ejes:** todos
**Puente a la siguiente:** Para arreglarlo, primero hay que acordar: ¿qué es “estar bien” para el cliente?

**Contenido:**
- Pagos CBU/QR y transferencias en tiempo real sobre microservicios en Kubernetes, en AWS y GCP.
- El core bancario está fuera de Kubernetes: la traza hoy se corta en esa frontera.
- Despliegues sin freno → Change Failure Rate alto.
- Telemetría sin estándar → factura alta y MTTR largo.
- Los 4 ejes atacan la causa común: falta de un "estar bien" medible y de datos estandarizados.

**Diagrama** (`d2`, C4 nivel 1, Context): al centro, "Plataforma de pagos de Banco Plus (microservicios en
Kubernetes, AWS + GCP)". A la izquierda: Cliente en la app, Tribus de desarrollo e Incident Commander / on-call.
A la derecha: Comercio, Core bancario, Transferencias CBU y otros bancos, y Observabilidad actual del banco.
Flechas rojas con los retos: 1 (despliegues sin freno), 2 (telemetría sin estándar), 3 (la traza se corta en el
core; MTTR largo) y 4 (la IA no entiende datos desordenados).

**Guion:**
"Lo vemos aquí, en un diagrama C4 de nivel Context. El cliente paga con QR desde la app; el pago recorre
microservicios en Kubernetes, en AWS y GCP, y habla con el core bancario y con otros bancos para las transferencias CBU en tiempo real.
Los cuatro síntomas se ven en el diagrama. Uno: las tribus despliegan sin freno; en DORA eso es un Change
Failure Rate alto. Dos: cada componente manda su telemetría sin filtro, y pagamos por volumen, no por valor.
Tres: cuando algo falla, la traza se corta en la frontera con el core y cada equipo nombra los datos
distinto; por eso el MTTR es largo. Cuatro: queremos IA, pero una IA no razona sobre datos desordenados.
Los cuatro ejes atacan la causa en orden: primero la definición, después los datos, después la inteligencia
y, al final, las personas. Y parto de lo que el banco ya tiene: no vengo a cambiarles las herramientas.
Para arreglarlo, primero hay que acordar: ¿qué es 'estar bien' para el cliente?"

**Preguntas probables:**
1. *¿Por qué no incluyes el nivel Component del C4?* — "Para una mesa de decisión bastan Context y
   Container; el detalle de componentes lo dibuja cada tribu en su repositorio, como arquitectura como
   código."

---

## Diapositiva 3 — Eje 1: SLIs, SLOs y Error Budget Policy del pago QR (2 min)

**Título:** Qué es "estar bien" para el cliente que paga con QR.

**Pregunta:** ¿Qué es “estar bien” para el cliente que paga con QR?
**Ejes:** 1
**Puente a la siguiente:** Ya sabemos qué es estar bien. ¿Cómo evitamos que un despliegue lo rompa?

**Contenido:**
- SLI (Service Level Indicator) de disponibilidad: pagos aceptados sin error de sistema ÷ pagos válidos.
  SLO de partida 99,9% en 30 días móviles (Error Budget de 43,2 min al mes), **calibrado con datos de la Fase 0**.
- SLI de latencia: proporción de pagos confirmados por debajo de un umbral, medido en el API Gateway
  (percentil, nunca promedio). **El umbral no se inventa:** sale de la curva de abandono del cliente, los
  timeouts del flujo y el histograma real; se reevalúa cada trimestre.
- Corrección: cero cobros dobles (idempotency key). Saturación como alerta temprana, no como SLO.
- Golden Signals (Latency, Traffic, Errors, Saturation) medidas donde las vive el cliente.
- **Error Budget Policy de conservación**, firmada con negocio: siempre la estrategia de despliegue que menos
  presupuesto gasta (canary por defecto) · en riesgo: solo canary lento · crítico: congelado salvo arreglos de
  confiabilidad. Los umbrales de cada zona se negocian con negocio con datos.

**Diagrama** (`d3`): tres zonas del Error Budget, sin porcentajes: 🟢 sano (canary por defecto), 🟡 en riesgo
(solo canary lento) y 🔴 crítico (congelado salvo arreglos de confiabilidad); debajo, la franja "Error Budget
Policy de conservación, firmada con negocio" y las dependencias en serie: 0,999³ ≈ 99,7%.

**Guion:**
"Eje uno. Al cliente que paga con QR le importan tres cosas: que el pago salga, que salga rápido y que no le
cobren dos veces. Eso se traduce en SLIs, Service Level Indicators.
Disponibilidad: pagos aceptados sin error de sistema sobre pagos válidos; un saldo insuficiente no es culpa
nuestra y no cuenta. Como punto de partida propongo un SLO de 99,9% en 30 días móviles, 43,2 minutos de
Error Budget al mes, que se calibra con datos reales.
Latencia: la proporción de pagos confirmados por debajo de un umbral, medida en el API Gateway, siempre en
percentil. El umbral no lo invento: sale de dónde el cliente abandona o reintenta, de los timeouts del flujo
y del histograma real.
Y corrección: cero cobros dobles, con idempotency key. La saturación la uso como alerta temprana, no como
SLO, porque el cliente no ve la CPU.
Pero lo más importante no es el número: es la Error Budget Policy, firmada con negocio, y es de
conservación. Siempre desplegamos con la estrategia que menos presupuesto gasta, que por defecto es canary.
Si el presupuesto entra en riesgo, solo canary lento y estricto; si queda crítico, se congela todo menos los
arreglos de confiabilidad. Los umbrales de cada zona los negociamos con negocio, con datos. Sin política, el
Error Budget es un número en un dashboard; con política, tiene autoridad.
Ya sabemos qué es estar bien. ¿Cómo evitamos que un despliegue lo rompa?"

**Preguntas probables:**
1. *¿Por qué no 100% si el pago es crítico?* — Es inalcanzable (el cliente depende de su red, su
   celular y otros bancos), congela la innovación porque cero presupuesto es cero despliegues, y cada
   nueve adicional exige redundancia en todas las dependencias. El SLO correcto es donde el cliente deja
   de notar la diferencia, y eso se mide.
2. *El pago QR depende de tres servicios con 99,9% cada uno. ¿Llegas a 99,9%?* — No: en serie se
   multiplican, 0,999³ ≈ 99,7%. Por eso las dependencias críticas necesitan un SLO más exigente o
   redundancia: dos réplicas independientes de 99% en paralelo dan 99,99%.
3. *¿Cuál es tu SLO de latencia?* — "El SLI está definido; el umbral sale de la curva de abandono del
   cliente y del timeout del flujo, en la Fase 0. Un número inventado hoy o nace roto o no protege nada."

---

## Diapositiva 4 — Eje 1: Quality Gate autoejecutable en CI/CD (2,5 min)

**Título:** El pipeline frena solo: antes, durante y después del despliegue.

**Pregunta:** ¿Cómo evitamos que un despliegue rompa lo que el cliente necesita?
**Ejes:** 1
**Puente a la siguiente:** El gate frena y revierte, pero necesita datos. ¿De dónde salen esos datos?

**Contenido:**
- **Quién controla:** Plataforma publica plantillas por lenguaje (reusable workflows de GitHub Actions) con
  mínimos obligatorios: pruebas, seguridad y gate de Error Budget. Cada tribu agrega lo que quiera encima.
- **Antes:** el paso a producción lo aprueba una **deployment protection rule** de Plataforma, que consulta el
  Error Budget y el burn rate (SLO como código con Sloth / OpenSLO → reglas de Prometheus). Sin el environment
  `production`, OIDC (OpenID Connect) no entrega credenciales en AWS ni en GCP.
- **Durante:** canary con análisis automático contra Prometheus, con **Argo Rollouts** o, si ya tienen un
  service mesh, **Flagger**; si empeora, rollback automático.
- **Después:** verificación posterior del burn rate y registro del evento de cambio.
- Alertas multi-window, multi-burn-rate del SRE Workbook de Google: 14,4× en 1 h → page · 6× en 6 h → page ·
  1× en 3 días → ticket.

**Diagrama** (`d4`): tres columnas. ANTES: Commit → Build, pruebas y seguridad (plantilla) → Gate 1, deployment
protection rule (¿hay Error Budget?); si no hay, "congelado". DURANTE: canary con un porcentaje pequeño (Argo
Rollouts o Flagger) → Gate 2, análisis automático → pasos crecientes hasta el 100%, o rollback automático.
DESPUÉS: Gate 3, verificación del burn rate → evento "cambio desplegado" que consulta el MCP. Abajo, las tres
alertas del SRE Workbook (14,4× en 1 h y 6× en 6 h → page; 1× en 3 días → ticket).

**Guion:**
"Con un Quality Gate autoejecutable. El reto uno dice que el CI/CD no detiene ni revierte: son dos verbos, y
por eso el gate tiene tres momentos. Pero primero, ¿quién controla los pipelines? Mi propuesta: Plataforma,
como equipo habilitador, publica plantillas por lenguaje en GitHub Actions con los mínimos de calidad,
seguridad y confiabilidad, y cada tribu agrega lo que quiera encima. Damos el piso, no el techo.
Antes: el paso a producción no depende del YAML de la tribu. Lo aprueba una deployment protection rule de
Plataforma, que pregunta cuánto Error Budget queda y a qué velocidad se gasta. El SLO vive como código con
Sloth, que genera las reglas de Prometheus. Si la política dice congelado, no se despliega; y sin ese
environment, AWS y GCP no entregan credenciales por OIDC. Nadie tiene que acordarse.
Durante: no desplegamos al 100%. No impongo herramientas: si ya usan Argo CD, Argo Rollouts; si tienen un
service mesh, Flagger. La versión nueva recibe un porcentaje pequeño del tráfico y un análisis automático la
compara con la estable en Prometheus; si empeora, revierte sola. Esto lo implementé en mi experiencia
anterior.
Después: una verificación posterior y un evento de 'cambio desplegado' que queda registrado. Guárdenlo,
porque en el eje tres es oro para la IA.
Y las alertas siguen el SRE Workbook de Google, multi-window, multi-burn-rate: un consumo de 14,4 veces en
una hora despierta a alguien; uno de una vez en tres días abre un ticket. Ni despertamos a nadie por un pico
de dos minutos, ni se nos escapa una fuga lenta.
El gate frena y revierte, pero necesita datos. ¿De dónde salen esos datos?"

**Pregunta para hacerle a la mesa:** *"¿Hoy quién es dueño de los pipelines: cada tribu o un equipo
central? ¿Ya existen plantillas corporativas? ¿Y con qué despliegan en Kubernetes: Argo CD, Flux, tienen
service mesh?"*

**Preguntas probables:**
1. *Se acabó el Error Budget, pero negocio exige lanzar una campaña el viernes. ¿Qué haces?* — No es
   un "no" técnico: aplico la Error Budget Policy y escalo con datos. Ofrezco alternativas: feature
   flag a un porcentaje pequeño, ventana de bajo tráfico, canary con rollback automático o aceptación
   formal del riesgo por escrito. Convierto la discusión en una decisión de riesgo explícita.
2. *Soy administrador del repositorio: le quito la regla al environment.* — Los environments y sus reglas
   se definen como código (Terraform) y los gestiona Plataforma; las tribus no son administradoras. Y un
   admission controller en el clúster rechaza imágenes sin firma aunque alguien despliegue a mano.
3. *¿Por qué canary y no Blue/Green?* — Canary ahorra Error Budget en exposición: solo una fracción ve la
   versión mala. Blue/Green ahorra en tiempo, pero en el switch el 100% de los clientes la ve; lo dejo para
   servicios cuyo tráfico no se puede dividir.
4. *¿Eso no convierte a Plataforma en un cuello de botella o en policía?* — No: somos habilitadores.
   Solo imponemos el piso mínimo; las tribus extienden la plantilla sin pedirnos permiso y contribuyen
   mejoras por pull request (inner source). Las excepciones existen, con dueño y fecha de vencimiento.

---

## Diapositiva 5 — Eje 2: arquitectura OpenTelemetry multi-cloud (C4 Container) (2,5 min)

**Título:** Un solo camino para toda la telemetría, en AWS, GCP y el datacenter.

**Pregunta:** ¿De dónde salen los datos que alimentan el gate, el SLO y el diagnóstico?
**Ejes:** 2 · usa 1
**Puente a la siguiente:** Ya tenemos los datos. ¿Cómo los tenemos todos sin pagar de más?

**Contenido:**
- OTel Collector **agente** (DaemonSet) por nodo: metadatos de Kubernetes, logs locales, filtrado barato.
- OTel Collector **gateway de dos capas** por nube: capa 1 con `loadbalancing` por traceID, capa 2 con
  `tail_sampling`. Imagen construida con OCB (OpenTelemetry Collector Builder): solo componentes aprobados.
- PII: **cada aplicación la enmascara** (plantilla de logging); **seguridad extra** de Plataforma con el
  processor `redaction` en el gateway, en modo lista permitida, **dentro de la red del banco** (SFC, Ley 1581).
- `traceparent` W3C en las llamadas y mensajes hacia el core; span links en lo asíncrono.
- OpenTelemetry Operator: auto-instrumentación por anotación, sin cambiar el código de las tribus.
- Exporta al backend de observabilidad que ya tenga el banco (por ejemplo, Mimir, Tempo y Loki).

**Diagrama** (`d5`, C4 nivel 2, Container): dentro de la red del banco, igual en AWS y GCP: Apps (enmascaran su
PII) → Agente (DaemonSet) → Gateway capa 1 (loadbalancing por traceID) → Gateway capa 2 (imagen OCB: redaction,
spanmetrics + servicegraph, tail_sampling) → backend que ya tenga el banco, vía OTLP + mTLS. Abajo: conector del
core instrumentado → core bancario (con traceparent) y el pipeline aparte de auditoría regulatoria.

**Guion:**
"Eje dos. Salen de un solo camino estándar de telemetría, igual en AWS, en GCP y en el datacenter:
OpenTelemetry, como pide el caso. No les pido cambiar su backend de observabilidad: el Collector exporta al
que ya tengan.
En cada nodo corre un OTel Collector agente, como DaemonSet: le pega a la telemetría los metadatos de
Kubernetes y bota lo obvio, como los health checks. Las tribus no cambian su código: el OpenTelemetry
Operator inyecta la instrumentación con una anotación.
Luego, el gateway, con dos capas. Para decidir qué traza guardar hay que verla completa, y si los spans de
un pago caen en réplicas distintas, ninguna la ve entera. La capa uno enruta por traceID, para que todos los
spans de un pago lleguen a la misma réplica; la capa dos hace el muestreo, que les muestro en un momento. La
imagen la construimos con OCB, solo con componentes aprobados.
Para DevSecOps, dos cosas. La PII la enmascara cada aplicación con la plantilla de logging, pero no
confiamos en una sola capa: Plataforma pone una seguridad extra con el processor redaction en el gateway, en
modo lista permitida, dentro de la red del banco. Si lo hiciéramos en la consola del proveedor, el dato ya
habría salido, y eso choca con la Ley 1581 y con la Superintendencia Financiera. Y todo viaja por OTLP con
mTLS.
Por último, la frontera con el core: el header traceparent viaja en las llamadas y mensajes; si el core no
se puede instrumentar, instrumentamos el conector. Así la traza ya no se corta donde más duele.
Ya tenemos los datos. ¿Cómo los tenemos todos sin pagar de más?"

**Preguntas probables:**
1. *¿Qué pasa si el gateway se cae en plena crisis?* — Varias réplicas con HPA (Horizontal Pod
   Autoscaler), `sending_queue` con almacenamiento persistente y reintentos, `memory_limiter` para
   degradar en vez de caerse, buffer en los agentes y meta-monitoreo: el Collector expone sus métricas
   de datos aceptados, rechazados y encolados en un stack mínimo independiente.
2. *Si cada aplicación ya enmascara, ¿para qué el gateway?* — Defensa en profundidad: basta un
   desarrollador que loguee la petición completa para que una cédula se escape. El gateway es la red final
   y el único punto auditable. Donde haga falta correlacionar, se usa hash en vez de borrar.
3. *¿Cómo garantizas que nadie despliegue un Collector sin el redaction?* — El gateway es el único con
   credenciales de salida, y el motor de políticas del banco (por ejemplo, OPA, Open Policy Agent) bloquea
   configuraciones sin el processor `redaction`.

---

## Diapositiva 6 — Eje 2: Smart Sampling y FinOps (2 min)

**Título:** Pagar por señal, no por ruido: la meta del −30% sin perder un solo error.

**Pregunta:** ¿Cómo vemos todo lo importante sin pagar de más?
**Ejes:** 2
**Puente a la siguiente:** Datos limpios y baratos. ¿Cómo hacemos que una IA los entienda?

**Contenido:**
- Tail-based sampling: 100% de errores, 100% de los pagos más lentos que el umbral del SLO de latencia, y
  un porcentaje pequeño de los exitosos, que se ajusta midiendo.
- `spanmetrics` **antes** del muestreo: métricas RED exactas al 100% aunque se descarten trazas.
- Log-to-Metrics (connector `count`) + `filter` de DEBUG en producción.
- Control de cardinalidad: ningún ID único como etiqueta de métrica. Showback de costo por tribu.
- Auditoría regulatoria por un pipeline aparte: nunca se muestrea.
- **La cifra de ahorro no se promete:** sale del estudio de línea base de la Fase 0.

**Diagrama** (`d6`): 1. Estudio de línea base → 2. Palancas (trazas → tail_sampling; logs → Log-to-Metrics y
filtro de DEBUG; métricas → cardinalidad) → 3. Medir antes y después (meta del caso −30%, showback por tribu).
Nota: spanmetrics antes del muestreo. Franja de referencias públicas: Capital One (~70% menos volumen de trazas) y
Pismo (~80% menos costo de observabilidad).

**Guion:**
"Pagando por señal, no por ruido. El caso pide −30% sin perder trazas de errores, y eso descarta la salida
fácil de guardar menos de todo.
La palanca principal es el tail-based sampling. El head-based decide al inicio, al azar, y puede botar justo
el pago que iba a fallar. El tail-based decide al final, con la traza completa: guarda todos los errores,
todos los pagos más lentos que el umbral del SLO y solo un porcentaje pequeño de los exitosos. ¿Y las
métricas? Siguen exactas, porque el connector spanmetrics las calcula antes del muestreo.
Segunda palanca, los logs: miles de líneas de 'pago exitoso' se vuelven un contador con Log-to-Metrics, y el
DEBUG no llega a producción. Tercera, la cardinalidad: ningún ID de cliente como etiqueta de métrica.
¿Cuánto ahorra esto en Banco Plus? No les voy a dar una cifra sin sus datos: primero, un estudio de la línea
base. Lo que sí sé es que la meta es alcanzable: Capital One redujo cerca del 70% del volumen de trazas con
OpenTelemetry, y Pismo, una plataforma de pagos, cerca del 80% de su costo de observabilidad con tail
sampling. Y a cada tribu le mostramos su costo, porque lo que no se ve no se optimiza.
Una aclaración para Riesgo: la telemetría no es el registro de auditoría; la evidencia regulatoria va por
otro pipeline, sin muestreo.
Datos limpios y baratos. ¿Cómo hacemos que una IA los entienda?"

**Preguntas probables:**
1. *Entonces, ¿cuánto nos vamos a ahorrar?* — "Comprometer un número sin sus datos sería irresponsable.
   Con el estudio de línea base les doy la cifra real; los casos públicos muestran que el −30% es
   alcanzable."
2. *¿Y si un regulador pide una transacción cuya traza se descartó?* — La traza nunca fue la evidencia:
   los logs de auditoría y transaccionales van por un pipeline separado, sin muestreo, inmutable y con
   retención legal. El muestreo aplica solo a la observabilidad operativa.
3. *¿Por qué no simplemente bajar la retención a la mitad?* — Porque recorta a ciegas: se pierde
   historia útil para capacidad y post-mortems y no ataca el origen del volumen. Primero se reduce lo
   que entra (muestreo, Log-to-Metrics, cardinalidad); la retención se escalona por niveles (caliente
   corta, fría barata en almacenamiento de objetos) según el uso real.

---

## Diapositiva 7 — Eje 3: telemetría AI-Ready con Semantic Conventions y MCP (2 min)

**Título:** Primero datos que la IA entienda; después, la IA.

**Pregunta:** ¿Cómo hacemos que una IA entienda nuestros datos?
**Ejes:** 3 · usa 2
**Puente a la siguiente:** La IA ya puede leer los datos. ¿Cómo encuentra dónde nace la falla?

**Contenido:**
- Semantic Conventions de OpenTelemetry + resource attributes obligatorios: `service.name`,
  `service.version`, `deployment.environment.name`, equipo dueño, `business.journey=pago_qr`.
- Exemplars y `trace_id` en los logs: de la métrica a la traza y al log en un clic.
- **Servidor MCP propio, de solo lectura:** `consultar_slo`, `obtener_grafo`, `buscar_trazas`,
  `buscar_logs(trace_id)`, `cambios_recientes`. Se combina con el servidor MCP del backend si ya existe.
- **Puente del desorden al orden:** las herramientas MCP tienen el mismo contrato aunque por debajo consulten
  la telemetría vieja o la nueva (patrón *strangler fig*). La IA sirve desde el día uno.
- **Agente de RCA automático:** lo dispara la alerta de burn rate, corre dentro del banco y consume el modelo
  (por ejemplo, Claude o Gemini) por Amazon Bedrock o Vertex AI. Guardarraíles: datos ya sin PII, solo
  lectura, auditoría, defensa contra Indirect Prompt Injection, humano en el bucle.

**Diagrama** (`d7`): alerta de burn rate → (webhook) agente de RCA dentro del banco, con el modelo vía Bedrock o
Vertex AI → servidor MCP propio con sus cinco herramientas → telemetría nueva (OpenTelemetry + Semantic
Conventions), telemetría heredada (adaptadores temporales, strangler fig) y registro de cambios del Quality Gate.
Abajo: "hipótesis rankeadas con evidencia → el Incident Commander decide".

**Guion:**
"Eje tres. Primero se ordenan los datos: una IA no razona donde un equipo dice status, otro http_code y otro
resp. Las Semantic Conventions de OpenTelemetry hacen que todo el banco llame igual a lo mismo, y los
resource attributes son la cédula de cada servicio: nombre, versión, equipo dueño y el journey de negocio,
como pago QR. Con exemplars y trace_id en los logs, se salta de la métrica a la traza y al log.
Encima va MCP, Model Context Protocol, el estándar para que un agente de IA use herramientas. Construimos un
servidor MCP propio, de solo lectura, con cinco herramientas: SLO, grafo, trazas, logs y cambios recientes;
esa última es la más valiosa, y la alimenta el Quality Gate. ¿Por qué propio? Porque es un puente: responde
igual sobre la telemetría vieja o la nueva, así la IA sirve desde el primer día, sin esperar la migración
completa.
¿Quién lo usa? Un agente de RCA que se dispara solo con la alerta, corre dentro del banco y usa un modelo,
por ejemplo Claude o Gemini, por Amazon Bedrock o Vertex AI, en la nube que el banco ya tiene. Cuando el
on-call abre el portátil, la hipótesis ya está en el canal.
Guardarraíles: datos sin PII, solo lectura, auditoría, y los logs se tratan como datos, nunca como
instrucciones. La IA propone; el humano decide.
La IA ya puede leer los datos. ¿Cómo encuentra dónde nace la falla?"

**Pregunta para hacerle a la mesa:** *"¿Ya tienen contratado algún modelo de IA o una plataforma de
observabilidad con IA incluida?"*

**Preguntas probables:**
1. *¿Darle a una IA acceso a la telemetría de producción de un banco no es un riesgo?* — Sí, y se
   controla: servidor MCP de solo lectura con mínimo privilegio, telemetría ya enmascarada en el
   Collector, defensa contra Indirect Prompt Injection (un log puede traer texto de un atacante, por
   ejemplo en la descripción de una transferencia), auditoría de cada llamada, modelo dentro de la cuenta
   del banco y humano en el bucle para cualquier acción.
2. *¿Por qué Bedrock y no la API directa de un proveedor de IA?* — Bedrock y Vertex AI son el canal, no el
   modelo: el banco ya tiene contrato, red privada, permisos y auditoría con su nube, y paga por uso, sin
   GPU ni licencias. Gracias a MCP, cambiar de modelo no cambia nada más.
3. *¿Eso no es lo mismo que prender las alertas inteligentes de la herramienta?* — No. Eso es detección de
   anomalías aislada. Lo que propongo es una capa de contexto estandarizada y neutral: cualquier modelo
   puede usarla, y el razonamiento queda trazable herramienta por herramienta.

---

## Diapositiva 8 — Eje 3, fase 2: grafo de topología e IA causal (2 min)

**Título:** De decenas de dashboards a pocas hipótesis: el grafo encuentra dónde nace la falla.

**Pregunta:** ¿Cómo encuentra la IA dónde nace la falla?
**Ejes:** 3 · usa 2
**Puente a la siguiente:** Todo listo. Pero igual algo va a fallar: ¿qué hacemos en plena crisis?

**Contenido:**
- El grafo de dependencias lo arma OpenTelemetry: connector `servicegraph` (nodos = servicios, aristas =
  llamadas con tasa, errores y latencia). Nuestra herramienta MCP `obtener_grafo` se lo entrega a la IA.
- Regla de causa raíz: el nodo anómalo **más profundo** cuyas dependencias están sanas. El que más
  grita suele ser víctima.
- **DFS** (Depth-First Search) desde el síntoma hacia abajo → causa raíz candidata.
- **BFS** (Breadth-First Search) sobre el grafo invertido → radio de explosión (a quién afecta).
- Cruce con `cambios_recientes` → hipótesis rankeadas con evidencia; el humano decide.

**Diagrama** (`d8`): grafo App QR → API pagos → {Antifraude, Saldos, Notificaciones}; Antifraude → BD de reglas;
Saldos → Conector del core → Core bancario. App QR, API pagos y Antifraude en rojo, dentro del recuadro "radio
de explosión (BFS)"; el resto en verde. Flechas DFS de App QR a Antifraude, que tiene borde amarillo (causa
candidata), y una nota "cambios_recientes: Antifraude v2.3.1, hace 12 min" que apunta a Antifraude.

**Guion:**
"Con el grafo de dependencias. OpenTelemetry lo arma solo con el connector servicegraph: cada servicio es un
nodo y cada llamada una arista con su tasa, errores y latencia; nuestra herramienta obtener_grafo se lo
entrega a la IA.
Sobre ese grafo, una regla simple: la causa raíz es el nodo anómalo más profundo cuyas dependencias están
sanas. Es como un trancón: termina donde la calle vuelve a estar libre.
En el ejemplo alertan la app, la API de pagos y antifraude. La API de pagos es la que más grita, pero es
víctima. Bajamos por el grafo con DFS, búsqueda en profundidad, y llegamos a antifraude: anómalo, con sus
dependencias sanas. El servidor MCP lo cruza con los cambios recientes: versión 2.3.1, desplegada hace 12
minutos. Hipótesis número uno, con evidencia.
En paralelo, BFS, búsqueda en anchura, sobre el grafo invertido, da el radio de explosión: qué servicios y
qué journeys están afectados, justo lo que necesita quien comunica.
Resultado: en vez de revisar decenas de dashboards, el Incident Commander recibe pocas hipótesis rankeadas.
Es barato de calcular, y es la base de la IA causal, siempre con humano en el bucle.
Todo listo. Pero igual algo va a fallar: ¿qué hacemos en plena crisis?"

**Preguntas probables:**
1. *Diez servicios alertan a la vez. ¿Cómo sabe la IA cuál es la causa y no un síntoma?* — Correlación
   no es causalidad: todos se correlacionan con la falla. La topología restringe: la causa candidata es
   el nodo anómalo cuyas dependencias están sanas; se confirma con el orden temporal y los cambios
   recientes.
2. *¿Y si hay dos nodos anómalos en ramas distintas?* — Sospecho de una dependencia oculta compartida
   que no está en el grafo: el mismo nodo de Kubernetes, la red, el bus de mensajes o un certificado.
   Esa brecha se vuelve una acción del post-mortem: instrumentar lo que faltaba.
3. *Si se muestrean las trazas, ¿el grafo queda incompleto?* — No: el `servicegraph` corre antes del tail
   sampling, igual que `spanmetrics`, y ve el 100% de los spans.

---

## Diapositiva 9 — Eje 4: el Incident Commander en hora pico (2 min)

**Título:** 12:30 de un día de quincena: el pago QR empieza a fallar.

**Pregunta:** ¿Qué hacemos cuando, aun así, el pago falla en hora pico?
**Ejes:** 4 · usa 1, 2, 3
**Puente a la siguiente:** El servicio volvió. ¿Cómo evitamos que vuelva a pasar?

**Contenido:**
- Roles, entre más simple mejor: **Incident Commander** (coordina, decide y comunica; no toca teclado) +
  **responsable técnico** (el dueño del servicio: diagnostica y ejecuta). En un SEV1 de un banco, el IC delega
  comunicaciones. La línea de tiempo la registran las herramientas, no una persona.
- Minuto 0–5: la herramienta de on-call del banco despierta al on-call; declarar SEV1, abrir el canal,
  asignar roles, medir el impacto con el SLO y el burn rate; el incidente queda en el ITSM del banco.
- Minuto 5–10: preguntar **qué cambió**: la hipótesis del agente de RCA ya está en el canal. Minuto 10: el IC
  decide el rollback.
- **Mitigar antes de diagnosticar:** rollback, apagar el feature flag, failover a la otra nube, load
  shedding, circuit breaker.
- Comunicar con hechos y con frecuencia fija; confirmar la recuperación con el SLI, no con "parece que ya".

**Diagrama** (`d9`): línea de tiempo de 0 a 60 minutos con cuatro carriles. Incident Commander: 0' alerta,
2–5' SEV1 y roles, 10' decide rollback, post-mortem. Agente de RCA: hipótesis lista en el canal antes de que
llegue el on-call. Responsable técnico: revisa, rollback, 20' SLI recuperado, monitoreo. Comunicaciones (SEV1):
15' primer comunicado y comunicados con frecuencia fija.

**Guion:**
"Eje cuatro. Doce y media de un día de quincena, y el pago QR empieza a fallar. La alerta no llega por CPU:
llega porque el burn rate pasó de 14,4 en una hora, así que ya sabemos que es grave. En ese mismo instante,
el agente de RCA arranca solo.
Como Incident Commander, en cinco minutos declaro SEV1, abro el canal y asigno los roles mínimos: un
responsable técnico, el dueño del servicio, que diagnostica y ejecuta; y, como es un SEV1 en un banco,
alguien de comunicaciones para negocio y la Superintendencia. La línea de tiempo la registran las
herramientas. Mi regla de oro: no toco el teclado; si me pongo a depurar, nadie coordina.
Pregunto lo más rentable: ¿qué cambió? La respuesta ya está en el canal: antifraude 2.3.1, desplegada 12 minutos antes de la alerta.
Y la decisión clave: mitigar antes de diagnosticar. No necesito entender el bug para hacer rollback. Sin un
cambio claro, el menú es apagar el feature flag, failover a la otra nube, load shedding para salvar los
pagos sacrificando consultas, o un circuit breaker.
Comunicaciones publica con hechos y frecuencia fija. Y cierro cuando el SLI lo confirma, no cuando 'parece
que ya'.
Todo lo de los ejes uno, dos y tres sirve aquí: la alerta del SLO, los datos limpios y la hipótesis lista.
Eso baja el Time to Restore.
El servicio volvió. ¿Cómo evitamos que vuelva a pasar?"

**Preguntas probables:**
1. *¿Y si el rollback no resuelve?* — Pasa al siguiente ítem del menú de mitigación (failover a la otra
   nube, load shedding, circuit breaker) mientras el responsable técnico diagnostica, y se escala a los
   dueños de las dependencias que el radio de explosión señala. El IC fija un tiempo límite por hipótesis
   para no quedarse atascado en una.
2. *¿Quién puede declarar un SEV1?* — Cualquiera, sin pedir permiso. Declarar de más y bajar la
   severidad después es barato; declarar tarde es caro. Las severidades se definen por impacto en el
   cliente y el SLO, no por la causa técnica.
3. *El estándar tiene más roles: Comms Lead, Scribe...* — Son roles, no personas: el modelo escala con la
   severidad. La única regla fija es que el IC no arregla.
4. *¿Qué herramienta de incidentes usarías?* — "La que ya tengan. Lo importante es que reciba la alerta por
   webhook, escale por severidad, cree el ticket en el ITSM y deje que el agente publique su hipótesis."

---

## Diapositiva 10 — Eje 4: post-mortem blameless, cultura y hoja de ruta (2 min)

**Título:** Aprender del incidente y cerrar el ciclo: de la crisis a mejores SLOs.

**Pregunta:** ¿Cómo aprendemos para que no vuelva a pasar?
**Ejes:** 4 · cierra en 1
**Puente a la siguiente:** Las acciones vuelven al SLO: el ciclo empieza de nuevo, cada vez mejor.

**Contenido:**
- Post-mortem blameless en ≤ 5 días hábiles: impacto (clientes, minutos, Error Budget gastado), línea de
  tiempo, factores contribuyentes, acciones con dueño y fecha (prevenir · detectar · mitigar).
- Las acciones vuelven al Eje 1: SLOs, alertas y Quality Gate más finos.
- Team Topologies: Plataforma como habilitador; "you build it, you run it": cada tribu atiende su SLO.
- Autoservicio en el IDP del banco (por ejemplo, Backstage): SLO como código, dashboards y alertas por
  plantilla; toil por debajo del 50% (guía del libro de SRE de Google), Runbook as Code, Game Days.
- Hoja de ruta con un servicio piloto (pago QR): **Fase 0 (2–4 semanas) caracterización de lo que ya
  existe** · 30 días SLO calibrado + burn rate · 60 días Quality Gate + gateway con PII · 90 días tail
  sampling medido + servidor MCP de solo lectura.

**Diagrama** (`d10`): a la izquierda, el ciclo ① a ④ → post-mortem blameless, con una flecha verde "acciones →
Eje 1"; a la derecha, la hoja de ruta Fase 0 → 30 → 60 → 90 días y los indicadores de éxito (Change Failure Rate
y Time to Restore contra la línea base, meta −30% de costo, toil por debajo del 50%).

**Guion:**
"Aprendiendo del incidente. En máximo cinco días hábiles hacemos el post-mortem blameless, sin culpa:
asumimos que las personas actuaron razonablemente con lo que sabían, y arreglamos el sistema. Si
castigamos, la próxima vez nos esconden información.
El documento trae impacto, con el Error Budget gastado; línea de tiempo; factores contribuyentes, en plural;
y acciones con dueño y fecha para prevenir, detectar y mitigar. En el ejemplo: el canary de antifraude no
tenía análisis automático. Esa acción vuelve al eje uno.
Para escalar, cultura: Plataforma es habilitador, no policía; cada tribu opera lo que construye y atiende
su SLO, con autoservicio en el IDP del banco, por ejemplo Backstage, y el toil por debajo del 50%, como
recomienda Google.
Y empezamos pequeño, con un piloto: el pago QR. Primero, dos a cuatro semanas caracterizando lo que ya
existe: herramientas, línea base de costo y de confiabilidad, incidentes. Luego, a 30 días, el SLO calibrado
y las alertas; a 60, el Quality Gate y el gateway con PII; a 90, el tail sampling con ahorro medido y el
servidor MCP.
Así se cierra el ciclo: las acciones del post-mortem vuelven al SLO, y cada vuelta lo hace mejor. Muchas
gracias."

**Preguntas probables:**
1. *¿La Fase 0 no es perder un mes?* — Es ganarlo: evita comprar o instalar lo que ya existe, fijar SLOs que
   nacen rotos y prometer un ahorro inventado. Y tiene entregables: inventario, línea base de costo, línea
   base de SLI y DORA, mapa de PII. Las preguntas que les hice durante la presentación son esa Fase 0.
2. *¿Cuándo escalan a otros servicios?* — Cuando el piloto cumple: SLO estable y calibrado, gate sin
   falsos bloqueos, ahorro medido y al menos un incidente o Game Day atendido con el flujo nuevo. Se escala
   con las plantillas y el IDP, no a mano.
3. *¿Los 5 porqués no bastan?* — Son útiles pero lineales: llevan a una sola causa y sesgan hacia el
   último humano de la cadena. Los sistemas complejos fallan por varios factores contribuyentes; se
   complementan con preguntas como "¿qué hizo que esta decisión pareciera razonable en el momento?".
4. *Los equipos tradicionales no quieren instrumentar ni operar. ¿Los obligas?* — No: sin mandato.
   Co-creo las plantillas con ellos, muestro el valor con el pago QR como piloto y uso Error Budgets
   compartidos para alinear velocidad con estabilidad. Si instrumentar es una anotación y el dashboard
   sale solo, la adopción deja de ser una discusión.

---

## Anexo — Preguntas para hacerle a la mesa (backlog de la Fase 0)

Se hacen durante la exposición o en los 10 minutos de preguntas. Muestran que el diseño parte de la
organización, no de la herramienta. Lo que la mesa no responda, lo responde la Fase 0.

1. ¿Quién es dueño hoy de los pipelines: cada tribu o un equipo central? ¿Existen plantillas corporativas? (D7)
2. ¿Con qué despliegan en Kubernetes (Argo CD, Flux, Helm) y tienen service mesh? (D8)
3. ¿Qué backend de observabilidad usan hoy y qué tienen contratado? (D15)
4. ¿Tienen contratado algún modelo de IA o una plataforma de observabilidad con IA incluida? (D19)
5. ¿Qué herramienta de on-call e ITSM usan? (D22)
6. ¿Qué motor de políticas usan en Kubernetes y en el pipeline? (D26)
