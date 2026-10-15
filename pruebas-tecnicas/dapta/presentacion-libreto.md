# Libreto de la presentación — Dapta, "defensa" de la plataforma (versión 1)

> Diez diapositivas, unos dieciséis minutos. Mismo formato que la presentación de Davivienda (tema 25): cada diapositiva
> tiene pregunta, título, contenido, diagrama (descrito aquí y dibujado en [diagramas.py](diagramas.py)), guion y
> preguntas probables. La presentación ([presentacion.html](presentacion.html)) se genera con
> `python3 generar-presentacion.py`.
>
> Es la **versión 2 de la [propuesta de valor](propuesta-valor.md)**, ya pasada por el marco de
> [decisiones-herramientas.md](decisiones-herramientas.md) (menos herramientas, más "lo que ya tienen"). Si en una
> sesión decides distinto alguna de las 12 decisiones, se cambia aquí y se regenera el HTML. Cinco reglas atraviesan
> todo el libreto:
>
> 1. **Ningún número inventado.** Solo se dicen cifras públicas con fuente (trust center, nota de prensa de la ronda,
>    documentación de Dapta) y valores estándar con fuente (las alertas del SRE Workbook de Google). La línea base de
>    DORA, los SLOs y los costos se miden en las **dos primeras semanas**.
> 2. **Lo que Dapta ya paga no se reemplaza, se aprovecha:** GitHub, AWS, Vanta, PostHog, Grafana, Temporal.
> 3. **Solo dos piezas nuevas que operar:** Argo CD y Kyverno (en modo Audit al inicio). Lo demás es configuración
>    de lo que ya existe o pasos del pipeline sin servidor propio (Trivy).
> 4. **Plataforma es un equipo habilitador:** "una carretera pavimentada, no un peaje". Da el piso, no el techo.
> 5. **Repo público:** solo información pública de Dapta y lo que se contó en la entrevista sin carácter confidencial.

> **Hilo conductor:** cada diapositiva responde una **pregunta**, y su respuesta abre la pregunta de la siguiente
> (campo "Puente a la siguiente"). Cada guion **abre respondiendo su pregunta y cierra con el puente**.
> Los "ejes" de la presentación son los **tres dolores de la entrevista** (certificaciones, estabilidad, DORA) más el
> **diferencial** (seguridad propia de la IA de voz).

| # | Diapositiva | Dolor | Tiempo |
|---|---|---|---|
| 1 | Portada: por qué ahora | — | 1,5 min |
| 2 | Contexto (C4 Context) | — | 1,5 min |
| 3 | Certificaciones: qué hay y qué sigue | 1 | 1,5 min |
| 4 | Un solo camino a producción (GitOps) | 1, 3 | 2 min |
| 5 | Métricas DORA con lo que ya tienen | 3 | 1,5 min |
| 6 | Kubernetes y Temporal seguros por defecto | 1, 2 | 1,5 min |
| 7 | SLOs de la llamada y SLAs de Enterprise | 2 | 1,5 min |
| 8 | Seguridad propia del agente de voz con IA | 4 | 1,5 min |
| 9 | Detectar, responder y aprender | 2 | 1,5 min |
| 10 | Qué traigo, qué no, y 90 días | todos | 2 min |

---

## Diapositiva 1 — Portada: por qué ahora (1,5 min)

**Título:** Una carretera pavimentada, no un peaje: seguridad que acelera a Dapta.

**Pregunta:** ¿Por qué este es el mejor momento para organizar la seguridad de Dapta?
**Dolores:** todos
**Puente a la siguiente:** Si este es el momento, ¿dónde duele hoy, exactamente?

**Contenido:**
- Tres dolores que me contaron: **certificaciones**, **estabilidad** y **métricas DORA** (DevOps Research and
  Assessment).
- Un momento que no se repite: la migración a **Kubernetes** y a **Temporal**, la ronda semilla de USD 6 M (13 de
  octubre) y un plan Enterprise con despliegue on-premise y SLAs (Service Level Agreements).
- Si la seguridad llega **después** de la migración, cuesta el doble y frena al equipo; si va **dentro** de la
  plataforma nueva, sale casi gratis.
- La propuesta: que el camino fácil para los 14 desarrolladores sea también el camino seguro, y que **cada despliegue
  genere su propia evidencia** para el auditor.

**Diagrama** (`d1` en [diagramas.py](diagramas.py)): arriba, los tres dolores (Certificaciones, Estabilidad, DORA) y
el diferencial (IA de voz) como cuatro cajas; todas apuntan a una caja central: "Una sola causa: lo seguro y lo
estable dependen de personas, no de la plataforma". Debajo, la ventana: "Migración a Kubernetes + Temporal" → "Carretera
pavimentada (golden path): seguro por defecto + evidencia automática".

**Guion:**
"Buenos días. Les traigo una propuesta, y empieza con una pregunta: ¿por qué este es el mejor momento para organizar
la seguridad de Dapta?
En la primera conversación me contaron tres dolores: les cuesta certificarse, la estabilidad, y las métricas DORA,
DevOps Research and Assessment. Y además están en un momento que no se repite: migrando a Kubernetes y a Temporal al
mismo tiempo, con una ronda semilla recién anunciada y un plan Enterprise que promete on-premise y SLAs.
Si la seguridad llega después de la migración, hay que volver a abrir todo lo que ya migraron, y eso cuesta el doble.
Si la metemos dentro de la plataforma nueva, sale casi gratis.
Mi propuesta es una carretera pavimentada, no un peaje: que el camino más fácil para los catorce desarrolladores sea
también el camino seguro, y que cada despliegue deje solo la evidencia que pide el auditor. Un aviso: no les voy a dar
números que no conozco; lo que no sé de Dapta, lo mido primero.
Traigo Kubernetes a nivel de arquitectura y troubleshooting, identidades por pod, políticas como código y CI/CD.
Si este es el momento, ¿dónde duele hoy, exactamente?"

**Preguntas probables:**
1. *¿Por qué no esperar a terminar la migración y después asegurar?* — Porque cada servicio migrado sin controles
   hay que volver a abrirlo: el doble de trabajo y otra ventana de riesgo. Meter el piso de seguridad en la plantilla
   hace que cada servicio que migra ya llegue seguro.
2. *¿Esto no nos va a frenar?* — La regla es al revés: si un control empeora las métricas DORA, el control está mal
   diseñado. Por eso Kyverno arranca en modo Audit y el pipeline es una plantilla que nadie tiene que escribir.

---

## Diapositiva 2 — Contexto: Dapta en un diagrama C4 Context (1,5 min)

**Título:** Tres dolores, una sola causa: lo seguro depende de personas, no de la plataforma.

**Pregunta:** ¿Dónde duele hoy, en la arquitectura de Dapta?
**Dolores:** todos
**Puente a la siguiente:** Empecemos por lo que piden los compradores: ¿qué tiene Dapta hoy, y qué sigue?

**Contenido:**
- Agentes de voz y de texto (llamada, WhatsApp, SMS, chat web) y Flow Studio, sobre AWS, en migración a Kubernetes y
  Temporal.
- Una sola llamada depende de varios proveedores externos: voz (Twilio, LiveKit, Deepgram) y LLM (Large Language
  Model: OpenAI, Anthropic, Gemini, Groq).
- **Certificaciones:** los compradores grandes piden evidencia; hoy la evidencia depende de que alguien la recoja.
- **Estabilidad:** cada dependencia externa es un punto de falla en tiempo real.
- **DORA:** sin línea base, nadie sabe si un cambio de proceso ayuda o estorba.
- **IA de voz:** el riesgo propio del producto no lo cubre ningún control publicado.

**Diagrama** (`d2`, C4 nivel 1, Context): al centro, "Plataforma Dapta (agentes de voz y texto, Flow Studio) sobre AWS,
migrando a Kubernetes + Temporal". A la izquierda: Clientes pymes, Compradores Enterprise (exigen evidencia) y los 14
desarrolladores. A la derecha: Proveedores de voz (Twilio, LiveKit, Deepgram), Proveedores de LLM (OpenAI, Anthropic,
Gemini, Groq), Temporal y Vanta + auditor. Flechas rojas con los dolores: 1 (evidencia a mano hacia Vanta), 2
(dependencias externas en tiempo real), 3 (despliegues sin medir) y 4 (datos de llamadas hacia los LLM).

**Guion:**
"Lo vemos en un diagrama C4 de nivel Context. Dapta tiene agentes de voz y de texto y Flow Studio, sobre AWS, y está
migrando a Kubernetes y a Temporal. Una sola llamada pasa por Twilio o LiveKit, por Deepgram y por uno o varios LLM,
Large Language Models.
Los dolores se ven en el diagrama. Uno: los compradores Enterprise piden evidencia, y hoy esa evidencia depende de que
alguien la recoja. Dos: cada proveedor externo es un punto de falla en una conversación en tiempo real. Tres: catorce
desarrolladores despliegan, pero sin una línea base de DORA no sabemos si vamos mejor o peor. Y cuatro: los datos de
las llamadas viajan a los proveedores de LLM, y ninguno de los controles publicados habla de IA.
La causa común: lo seguro y lo estable dependen de personas, no de la plataforma. Y parto de lo que ya tienen: GitHub,
AWS, Vanta, PostHog, Grafana. No vengo a cambiarles las herramientas.
Empecemos por lo que piden los compradores: ¿qué tiene Dapta hoy, y qué sigue?"

**Preguntas probables:**
1. *¿De dónde sacaste los proveedores?* — De la lista pública de subprocesadores del trust center. Por eso los nombro:
   no es información interna.
2. *¿Por qué no dibujas el detalle interno?* — Porque no lo conozco todavía: es lo primero que levanto en los primeros
   30 días. Para una conversación de decisión basta el nivel Context.

---

## Diapositiva 3 — Certificaciones: qué hay y qué sigue (1,5 min)

**Título:** El SOC 2 ya está; lo difícil es mantenerlo vivo y escoger la siguiente certificación.

**Pregunta:** ¿Qué piden los compradores, y qué tiene Dapta hoy?
**Dolores:** 1
**Puente a la siguiente:** Si la evidencia tiene que ser continua, ¿cómo hacemos que cada despliegue la genere sola?

**Contenido:**
- **SOC 2 (System and Organization Controls 2) Type II**, emitido el 10 de septiembre de 2026, con una ventana de
  observación de 3 meses, la mínima. La siguiente auditoría observa **12 meses**: ahí se caen los controles "de papel".
- 79 controles publicados en el trust center (Vanta), de la plantilla estándar; **ninguno menciona IA**.
- La siguiente certificación **la escoge el contrato que está esperando**: ISO 27001 (Europa, LatAm, empresas
  globales), HIPAA (salud; no es una certificación, se firma un BAA, Business Associate Agreement) o ISO 42001
  (gestión de IA, el diferencial).
- Por los SLAs del plan Enterprise: ampliar el SOC 2 al criterio de **Availability**.
- Regla: un control que no genera evidencia automática no existe.

**Diagrama** (`d3`): a la izquierda, una escalera de abajo hacia arriba: "SOC 2 Type II, 3 meses ✓ (sep. 2026)" →
"SOC 2 Type II, 12 meses + Availability" → "Siguiente, según el contrato: ISO 27001 · HIPAA (BAA) · ISO 42001". A la
derecha, dos columnas: "Control de papel" (captura de pantalla, alguien se acuerda, se cae en 12 meses) contra
"Evidencia continua" (GitHub, AWS y Kubernetes → Vanta → auditor).

**Guion:**
"Lo bueno primero: Dapta ya tiene SOC 2, System and Organization Controls 2, Type II. Eso no lo tiene cualquier
startup de este tamaño. Pero el informe salió en septiembre con una ventana de observación de tres meses, la mínima.
La siguiente auditoría mira doce meses seguidos, y ahí es donde se caen los controles de papel: la captura de pantalla
que alguien tomó una vez, la revisión de accesos que se hizo un solo trimestre.
En el trust center hay 79 controles, de la plantilla estándar de Vanta, y ninguno habla de IA, que es justamente el
producto.
¿Cuál es la siguiente certificación? No la escojo yo: la escoge el contrato que está esperando. Si es Europa o una
empresa global, ISO 27001, que reutiliza buena parte del SOC 2. Si es salud, HIPAA, que en realidad no es una
certificación sino un acuerdo, el BAA, Business Associate Agreement. Y como diferencial, ISO 42001, gestión de IA. Por
los SLAs del plan Enterprise, además, ampliaría el SOC 2 al criterio de Availability.
Mi regla: un control que no genera evidencia automática, no existe.
Si la evidencia tiene que ser continua, ¿cómo hacemos que cada despliegue la genere sola?"

**Pregunta para hacerle a la mesa:** *"¿Qué certificación o requisito concreto les han pedido los clientes que hoy no
pueden cumplir? ¿Hay un contrato esperando?"*

**Preguntas probables:**
1. *¿Qué diferencia hay entre Type I y Type II?* — Type I dice que el control está bien diseñado en una fecha; Type II
   dice que funcionó durante toda una ventana de observación. Los compradores grandes piden Type II.
2. *¿Por qué no sacar ISO 27001 ya mismo?* — Porque cuesta auditoría y tiempo de personas, y si el contrato que
   espera es de salud, lo que necesitamos es HIPAA. Primero se pregunta a ventas qué contrato está frenado.
3. *¿Qué pasa entre el fin de la ventana y el próximo informe?* — Se entrega una *bridge letter*: una carta de la
   gerencia que dice que los controles siguen funcionando mientras sale el siguiente informe.

---

## Diapositiva 4 — Un solo camino a producción con GitOps (2 min)

**Título:** Un solo camino a producción: todo cambio entra por pull request y deja evidencia.

**Pregunta:** ¿Cómo hacemos que cada despliegue sea confiable y genere su propia evidencia?
**Dolores:** 1, 3
**Puente a la siguiente:** Ya tenemos el camino. ¿Cómo sabemos si nos hace más rápidos o más lentos?

**Contenido:**
- Nadie sube directo a `main`: **GitHub rulesets** + **CODEOWNERS**, todo cambio por pull request revisado.
- Una sola plantilla de pipeline (**reusable workflows de GitHub Actions**) que heredan todos los servicios:
  Dependabot, secret scanning con push protection y **Trivy** para las imágenes.
- Cero llaves de AWS en el CI: **OIDC** (OpenID Connect) → rol de IAM con credenciales temporales; el ambiente
  `production` con aprobación.
- **Argo CD** (GitOps): el clúster se sincroniza con Git; nadie hace `kubectl apply` a mano. **Terraform** con el
  `plan` visible en el pull request.
- La evidencia llega sola a **Vanta**, que ya se integra con GitHub y AWS: el historial de Git **es** la evidencia.

**Diagrama** (`d4`): de izquierda a derecha: Pull request (rulesets, CODEOWNERS) → Plantilla de CI (Dependabot,
secret scanning, Trivy) → OIDC → imagen en Amazon ECR → Argo CD → EKS. Debajo de cada paso, el control de SOC 2 que
evidencia: "Change management procedures enforced", "Vulnerabilities scanned and remediated", "Production deployment
access restricted". Abajo, una franja: todos los pasos → Vanta → auditor, "sin capturas de pantalla".

**Guion:**
"Con un solo camino a producción, igual para todos. Me dijeron que una de las tareas del cargo es montar un proceso
confiable de desarrollo y despliegue, y ese proceso es también la evidencia de tres controles del SOC 2.
Primero: nadie sube directo a main. Con GitHub rulesets y CODEOWNERS, todo cambio entra por pull request revisado.
Segundo: una sola plantilla de pipeline, con reusable workflows de GitHub Actions. Plataforma la mantiene, y cada
servicio la hereda: Dependabot para las dependencias, secret scanning con push protection para que nadie suba una
llave, y Trivy para escanear las imágenes. Damos el piso; cada equipo agrega lo que quiera encima.
Tercero: cero llaves de AWS guardadas en el CI. Con OIDC, OpenID Connect, GitHub pide credenciales temporales a un rol
de IAM, y solo el ambiente production puede pedirlas.
Cuarto: Argo CD. El clúster se sincroniza con Git, nadie hace kubectl apply a mano, y si alguien cambia algo directo,
Argo CD lo devuelve. La infraestructura, con Terraform y el plan visible en el pull request.
El resultado: Vanta ya se integra con GitHub y AWS, así que la evidencia le llega sola al auditor. El historial de Git
es la evidencia.
Ya tenemos el camino. ¿Cómo sabemos si nos hace más rápidos o más lentos?"

**Pregunta para hacerle a la mesa:** *"¿Cómo despliegan hoy, y quién tiene acceso directo a producción?"*

**Preguntas probables:**
1. *¿Por qué Argo CD y no desplegar con `kubectl` desde GitHub Actions?* — Por evidencia y por deriva: con Argo CD, Git
   es la fuente de verdad, cualquier cambio manual se detecta y se revierte, y los desarrolladores ven el estado en una
   interfaz. Desde GitHub Actions, el pipeline necesita credenciales de escritura al clúster.
2. *¿Y si hay una urgencia y hay que saltarse el pull request?* — Existe un procedimiento de emergencia (*break glass*):
   acceso temporal, registrado y con pull request posterior. La excepción también deja evidencia.
3. *¿Por qué no Snyk o Semgrep?* — Primero lo nativo de GitHub, que ya pagan. Agrego Semgrep solo si el análisis de
   código se queda corto; cada herramienta nueva es otro subprocesador que auditar.

---

## Diapositiva 5 — Métricas DORA con lo que ya tienen (1,5 min)

**Título:** Medir antes de cambiar: las cuatro métricas DORA con lo que ya tienen.

**Pregunta:** ¿Cómo sabemos si el proceso nuevo nos hace más rápidos o más lentos?
**Dolores:** 3
**Puente a la siguiente:** Ya medimos el proceso. ¿Sobre qué plataforma corre todo esto, sin frenar a nadie?

**Contenido:**
- **Velocidad:** Deployment Frequency y Lead Time for Changes. **Estabilidad:** Change Failure Rate y Time to Restore
  Service (en el modelo reciente, Failed Deployment Recovery Time).
- Se calculan con lo que ya tienen: eventos de **GitHub** (pull requests, despliegues) y de **Argo CD**, en un tablero
  de **Grafana**. Comprar LinearB o Sleuth solo si eso no basta.
- La **línea base** se mide en las dos primeras semanas: no prometo cifras sin datos.
- Las palancas: lotes pequeños, trunk-based development y **feature flags con PostHog** (ya es subprocesador: cero
  proveedores nuevos).
- Regla: la seguridad **no** puede empeorar las métricas DORA; si las empeora, el control está mal diseñado.

**Diagrama** (`d5`): arriba, cuatro cajas en dos grupos: Velocidad (Deployment Frequency, Lead Time for Changes) y
Estabilidad (Change Failure Rate, Time to Restore Service). A la izquierda, las fuentes: GitHub, Argo CD e incidentes →
tablero de Grafana. Abajo, una línea: "Semanas 1–2: línea base" → "Cada cambio de proceso se compara contra ella" →
"Palancas: lotes pequeños, trunk-based, feature flags (PostHog)".

**Guion:**
"Midiéndolo con las cuatro métricas DORA. Dos de velocidad: Deployment Frequency, cuántas veces desplegamos, y Lead
Time for Changes, cuánto tarda un commit en llegar a producción. Y dos de estabilidad: Change Failure Rate, qué
porcentaje de despliegues causa una falla, y Time to Restore Service, cuánto tardamos en recuperarnos. En el modelo
reciente de DORA, esta última se llama Failed Deployment Recovery Time.
No hace falta comprar nada para empezar. Los pull requests y los despliegues ya están en GitHub y van a estar en Argo
CD; con eso armamos un tablero en Grafana, que ya tienen. Si se queda corto, ahí sí evaluamos LinearB o Sleuth.
¿Cuál es la meta? No se las voy a inventar: en las dos primeras semanas medimos la línea base, y cada cambio de
proceso se compara contra ella.
Las palancas para mejorar son conocidas: lotes pequeños, trunk-based development y feature flags, que ya pueden hacer
con PostHog, sin un proveedor nuevo.
Y una regla para mí mismo: la seguridad no puede empeorar estas métricas. Si un control las empeora, está mal diseñado.
Ya medimos el proceso. ¿Sobre qué plataforma corre todo esto, sin frenar a nadie?"

**Preguntas probables:**
1. *¿Qué cuenta como "falla" para el Change Failure Rate?* — Un despliegue que requiere rollback, un hotfix o causa un
   incidente. Se acuerda la definición una vez y se automatiza: una etiqueta en el pull request del hotfix o el
   rollback en Argo CD.
2. *¿Para qué feature flags si ya tenemos canary?* — Separan desplegar de lanzar: el código llega a producción apagado
   y se enciende por cliente. Y todavía no propongo canary: sin SLOs medidos, el canary no sabe cuándo devolver.
3. *¿No es mejor comprar una herramienta de DORA y ya?* — Puede ser después. Hoy el dolor es no tener línea base, y
   eso se resuelve con lo que ya pagan. Comprar es otra revisión de proveedor y otro subprocesador.

---

## Diapositiva 6 — Kubernetes y Temporal seguros por defecto (1,5 min)

**Título:** Kubernetes y Temporal seguros por defecto: lo inseguro no corre.

**Pregunta:** ¿Sobre qué plataforma corre todo esto, sin frenar a nadie?
**Dolores:** 1, 2
**Puente a la siguiente:** La plataforma es segura. Pero ¿cómo prometemos un SLA de Enterprise sin mentir?

**Contenido:**
- **Amazon EKS**: se justifica por el on-premise del plan Enterprise; los mismos charts de Helm corren en la casa del
  cliente.
- Cada pod con su propio rol de AWS, sin llaves: **EKS Pod Identity** (o IRSA, IAM Roles for Service Accounts).
- Secretos fuera del código: **External Secrets Operator** + **AWS Secrets Manager**, incluidos los tokens OAuth de
  los CRM de cada cliente.
- **Kyverno**: no root, límites de CPU y memoria; primero en modo **Audit**, después **Enforce**. NetworkPolicy por
  namespace.
- **Temporal**: cifrado del lado del cliente con **Payload Codec** (Temporal solo ve texto cifrado) + mTLS (mutual
  TLS) y un namespace de Temporal por ambiente.

**Diagrama** (`d6`): a la izquierda, Argo CD → Kyverno (Audit → Enforce) → un recuadro "Amazon EKS" con dos
namespaces: "servicios" y "workers de Temporal", separados por NetworkPolicy. Del recuadro salen: EKS Pod Identity →
AWS (sin llaves); AWS Secrets Manager → External Secrets → pods; y los workers → Payload Codec (cifra) → Temporal Cloud,
"solo ve texto cifrado", por mTLS.

**Guion:**
"Sobre la plataforma que ya están construyendo: Kubernetes y Temporal, pero seguros por defecto.
Kubernetes en AWS es Amazon EKS. ¿Por qué Kubernetes y no algo más simple? Por el plan Enterprise: si prometen
on-premise, los mismos charts de Helm corren en la casa del cliente.
Dentro del clúster, cuatro piezas. Cada pod tiene su propio rol de AWS con EKS Pod Identity, sin llaves guardadas.
Los secretos viven en AWS Secrets Manager y External Secrets los lleva al clúster, incluidos los tokens OAuth de los
CRM de cada cliente. Kyverno revisa cada despliegue: nada corre como root ni sin límites. Y para no frenar a nadie,
Kyverno arranca en modo Audit, solo reporta, y pasa a Enforce cuando los servicios ya cumplen. NetworkPolicy separa
los namespaces: un servicio comprometido no llega a todos.
Y Temporal. Si un workflow lleva transcripciones o datos del CRM, esos datos quedan en el historial de Temporal. Con
el Payload Codec ciframos del lado de Dapta, antes de que salgan: Temporal solo ve texto cifrado. Es el argumento de
privacidad más fuerte de toda la migración. La conexión, por mTLS, mutual TLS, con un namespace por ambiente.
La plataforma es segura. Pero ¿cómo prometemos un SLA de Enterprise sin mentir?"

**Pregunta para hacerle a la mesa:** *"¿Usan Temporal Cloud o lo operan ustedes? ¿Qué datos viajan dentro de los
workflows?"*

**Preguntas probables:**
1. *¿Por qué Kyverno y no OPA Gatekeeper?* — Las dos sirven; escojo una sola. Kyverno escribe las políticas en YAML,
   el mismo lenguaje de los manifiestos, y el equipo no tiene que aprender Rego.
2. *Si cifras los payloads, ¿cómo depuramos un workflow en la interfaz de Temporal?* — Con un Codec Server: la
   interfaz le pide al servidor de Dapta que descifre, solo para quien tiene permiso. Temporal sigue sin ver nada.
3. *¿Y si el cliente Enterprise no tiene Kubernetes?* — Es una pregunta de producto: o se le entrega con un
   Kubernetes empaquetado (por ejemplo, k3s) o no se ofrece on-premise a ese cliente. Lo resolvemos con ventas antes
   de prometer.

---

## Diapositiva 7 — SLOs de la llamada y SLAs de Enterprise (1,5 min)

**Título:** Prometer solo lo que medimos: SLOs de la llamada, no uptime de servidores.

**Pregunta:** ¿Cómo prometemos un SLA de Enterprise sin mentir?
**Dolores:** 2
**Puente a la siguiente:** Ya medimos la estabilidad. Pero hay un riesgo que hoy no cubre ningún control: ¿cuál es?

**Contenido:**
- **SLI** (Service Level Indicator) desde el cliente: llamadas que conectan, tiempo de respuesta del agente (en
  percentil, nunca en promedio) y workflows de Flow Studio que terminan bien.
- **SLO** (Service Level Objective) interno más exigente que el SLA del contrato; el umbral sale de la línea base, no
  se inventa.
- **Error Budget** + alertas multi-window, multi-burn-rate del SRE Workbook de Google: 14,4× en 1 h → page · 1× en
  3 días → ticket.
- La status page se alimenta del SLO, para que su número sea defendible ante un cliente Enterprise.
- Dependencias externas: timeouts, circuit breaker y **failover entre proveedores de LLM**; reintentos durables con
  Temporal.
- Canary con Argo Rollouts: **todavía no**. Sin un SLO medido, el canary no sabe cuándo devolver.

**Diagrama** (`d7`): el camino de una llamada de izquierda a derecha: Quien llama → Twilio / LiveKit → Agente de voz
(Deepgram: voz a texto → LLM → respuesta) → Flow Studio sobre Temporal → CRM del cliente. Tres marcas de SLI: ① la
llamada conecta, ② el agente responde rápido, ③ el workflow termina bien. Debajo del LLM, el failover: OpenAI ⇄
Anthropic ⇄ Gemini ⇄ Groq. Abajo, la franja: SLO → Error Budget → alertas de burn rate y status page.

**Guion:**
"Prometiendo solo lo que medimos, y medido desde el cliente, no desde los servidores. Al cliente de Dapta le importan
tres cosas: que la llamada conecte, que el agente responda rápido y que lo que tenía que pasar después, en Flow
Studio, de verdad pase. Esos son los SLIs, Service Level Indicators. La latencia, siempre en percentil: el promedio
esconde a los clientes que esperan más.
Sobre esos SLIs ponemos SLOs internos, más exigentes que el SLA que firma ventas, para tener margen. ¿Cuánto? Lo
decide la línea base, no yo.
Con el SLO viene el Error Budget, y las alertas siguen el SRE Workbook de Google: si en una hora se gasta presupuesto
14,4 veces más rápido de lo normal, despertamos a alguien; si es una fuga lenta, se abre un ticket.
Y la status page se alimenta de ese SLO. Hoy muestra incidentes en Flow Studio y aun así marca cien por ciento: ante un
cliente Enterprise, ese número tiene que salir de una medición que podamos defender.
Para las dependencias externas: timeouts, circuit breaker y failover entre proveedores de LLM. Temporal ya da
reintentos durables.
¿Y canary? Todavía no: sin SLO medido, el canary no sabe cuándo devolver.
Ya medimos la estabilidad. Pero hay un riesgo que hoy no cubre ningún control: ¿cuál es?"

**Preguntas probables:**
1. *¿Cuál sería el SLO?* — "Los SLIs ya están definidos; el umbral sale de la línea base de las dos primeras semanas.
   Un número inventado hoy o nace roto o no protege nada."
2. *¿Qué pasa si se acaba el Error Budget y ventas necesita una función?* — Se aplica una Error Budget Policy firmada
   con negocio: con el presupuesto agotado, solo arreglos de confiabilidad, salvo una aceptación de riesgo por escrito.
   La discusión deja de ser técnica y se vuelve una decisión explícita.
3. *Si cambio de LLM en un failover, ¿el agente no se comporta distinto?* — Sí, por eso el failover se prueba con las
   mismas evals del agente en el pipeline. Un proveedor de respaldo que nadie probó no es respaldo.

---

## Diapositiva 8 — Seguridad propia del agente de voz con IA (1,5 min)

**Título:** El diferencial: controles para un agente de voz con IA, que hoy no existen.

**Pregunta:** ¿Qué riesgo de un agente de voz con IA no cubre hoy ningún control?
**Dolores:** 4 · usa 1
**Puente a la siguiente:** Prevenimos lo que podemos. Pero algo va a fallar igual: ¿qué hacemos entonces?

**Contenido:**
- **PII** (Personally Identifiable Information) en grabaciones y transcripciones: redacción en Deepgram (`redact`),
  política de retención y enlaces públicos de llamada apagados por defecto.
- Datos de clientes en los proveedores de LLM: acuerdos de **ZDR** (Zero Data Retention) y de no entrenamiento, y un
  registro de qué dato va a qué proveedor.
- Quien llama manipula al agente (**prompt injection** por voz o WhatsApp): herramientas del agente con mínimo
  privilegio, guardrails y pruebas con el **OWASP Top 10 for LLM Applications**, junto al equipo de "ataque".
- Un cambio de prompt también es un despliegue: **evals** (evaluaciones) del agente en el pipeline.
- Aislamiento entre clientes (multi-tenancy) probado en el pipeline; consentimiento de grabación y **TCPA** (Telephone
  Consumer Protection Act) como configuración por defecto.

**Diagrama** (`d8`): el flujo de una llamada (Quien llama → Agente de voz → Transcripción y grabación → Proveedores de
LLM → Herramientas del agente: CRM, calendario) con cuatro riesgos marcados en rojo y su control en una caja al lado:
⚠ prompt injection → mínimo privilegio + OWASP LLM Top 10 + evals; ⚠ PII → redact + retención; ⚠ datos a terceros →
ZDR; ⚠ fuga entre clientes → pruebas de aislamiento por tenant.

**Guion:**
"Este es el riesgo propio del producto, y es el diferencial. De los 79 controles publicados, ninguno habla de IA, y
eso es lo primero que va a preguntar un cliente grande.
Cuatro riesgos. Uno: la PII, Personally Identifiable Information, dentro de grabaciones y transcripciones. Deepgram
ya tiene la opción redact para números de tarjeta o de identificación; le sumamos una política de retención y los
enlaces públicos de llamada apagados por defecto.
Dos: los datos de los clientes viajan a los proveedores de LLM. Necesitamos acuerdos de ZDR, Zero Data Retention, y
de no entrenamiento, y un registro de qué dato va a qué proveedor.
Tres: quien llama puede intentar manipular al agente, prompt injection por voz o por WhatsApp. El agente solo debe
poder usar las herramientas que necesita, con mínimo privilegio, y lo probamos con el OWASP Top 10 for LLM
Applications, junto al equipo de ataque. Y como un cambio de prompt también es un despliegue, las evals del agente
corren en el pipeline.
Cuatro: que un cliente vea datos de otro. Eso se prueba automáticamente en cada despliegue. Y para Estados Unidos, el
consentimiento de grabación y la TCPA, Telephone Consumer Protection Act, como configuración por defecto.
Prevenimos lo que podemos. Pero algo va a fallar igual: ¿qué hacemos entonces?"

**Pregunta para hacerle a la mesa:** *"¿Qué hace exactamente el equipo de ataque y cómo se coordina con defensa?"*

**Preguntas probables:**
1. *¿Y el Dapta MCP? Tiene herramientas que borran cosas.* — Ya tiene un buen patrón: las 19 herramientas destructivas
   piden "preview → commit". Le sumaría API keys con alcance mínimo por herramienta y auditoría por llamada, y lo
   probaría con el mismo OWASP Top 10 for LLM.
2. *¿Cómo detectas un prompt injection por voz?* — No se detecta todo, así que se limita el daño: el agente no tiene
   permisos que no necesita, las acciones sensibles piden confirmación, y lo que dice quien llama se trata como dato,
   nunca como instrucción.
3. *¿Esto no le toca al equipo de ataque?* — Ataque encuentra; defensa convierte lo encontrado en controles
   permanentes: una prueba en el pipeline, una política o un guardrail. Es trabajo en pareja.

---

## Diapositiva 9 — Detectar, responder y aprender (1,5 min)

**Título:** Detectar en minutos, responder con roles claros y aprender sin culpa.

**Pregunta:** ¿Qué hacemos cuando, aun así, algo falla o nos atacan?
**Dolores:** 2 · usa 1
**Puente a la siguiente:** Ya está todo el diseño. ¿Qué traigo de verdad, qué no traigo, y qué entrego en 90 días?

**Contenido:**
- **Ver:** AWS CloudTrail de toda la organización en una cuenta de logs aparte; **Amazon GuardDuty** con EKS Runtime
  Monitoring; **AWS Security Hub** → Slack.
- **Responder:** Incident Commander (coordina y comunica, no toca el teclado) + responsable técnico; **mitigar antes
  de diagnosticar**: rollback con Argo CD, apagar el feature flag, cambiar de proveedor de LLM.
- **Practicar:** runbooks y un simulacro (*tabletop exercise*) cada trimestre: evidencia del control "Incident response
  plan tested".
- **Aprender:** post-mortem blameless en máximo 5 días hábiles, con acciones con dueño y fecha que vuelven a la
  plataforma.
- Un SIEM (Security Information and Event Management) completo: **todavía no**; es para cuando haya alguien que lo
  mire.

**Diagrama** (`d9`): un ciclo de cuatro cajas: ① Detectar (CloudTrail, GuardDuty, Security Hub, alertas de burn rate)
→ ② Responder (Incident Commander, mitigar primero) → ③ Aprender (post-mortem blameless, acciones con dueño) → ④
Mejorar la plataforma (política de Kyverno, paso del pipeline, SLO más fino) → de vuelta a ①. Al centro: "cada vuelta
deja evidencia para Vanta".

**Guion:**
"Con un ciclo de cuatro pasos: ver, responder, practicar y aprender.
Ver: CloudTrail registra todo lo que pasa en AWS, de todas las cuentas, en una cuenta de logs aparte que nadie puede
borrar. GuardDuty detecta amenazas, incluso dentro de EKS, y Security Hub junta los hallazgos y los manda a Slack.
Todo nativo de AWS, sin un servidor más que operar.
Responder: cuando algo falla, una persona es Incident Commander, coordina y comunica, y no toca el teclado; otra, el
responsable técnico, ejecuta. Y la regla de oro: mitigar antes de diagnosticar. No necesito entender el bug para hacer
rollback con Argo CD, apagar un feature flag o pasar a otro proveedor de LLM.
Practicar: un simulacro cada trimestre. Además de prepararnos, es la evidencia del control de plan de incidentes
probado.
Aprender: un post-mortem blameless, sin culpa, en máximo cinco días hábiles. Las acciones vuelven a la plataforma: una
política nueva en Kyverno, un paso más en el pipeline o un SLO más fino.
¿Y un SIEM completo? Todavía no: es para cuando haya alguien que lo mire todos los días.
Ya está todo el diseño. ¿Qué traigo de verdad, qué no traigo, y qué entrego en 90 días?"

**Preguntas probables:**
1. *¿Quién está de guardia si somos 14?* — "You build it, you run it": cada equipo atiende sus servicios, con una
   rotación liviana y alertas que solo despiertan por burn rate, no por CPU. Plataforma da las herramientas y los
   runbooks.
2. *¿Qué hace GuardDuty que no haga CloudTrail?* — CloudTrail registra qué pasó; GuardDuty lo analiza y avisa cuando
   algo parece un ataque: credenciales usadas desde un lugar raro, un pod que habla con una dirección maliciosa.

---

## Diapositiva 10 — Qué traigo, qué no, y 90 días (2 min)

**Título:** Antes de traer herramientas, quito las que sobran: dos piezas nuevas y 90 días.

**Pregunta:** ¿Qué traigo de verdad, qué no traigo, y qué entrego en 90 días?
**Dolores:** todos
**Puente a la siguiente:** Al día 90, el camino seguro es el camino fácil, y la evidencia le llega sola al auditor.

**Contenido:**
- Cada herramienta pasa **7 preguntas**: dolor, usar lo que ya hay, costo, operación, reversibilidad, evidencia y
  adopción. Cada decisión queda en un **ADR** (Architecture Decision Record).
- **Ya lo tienen:** GitHub, AWS (Secrets Manager, GuardDuty), PostHog, Grafana, Vanta. **Nuevo:** solo Argo CD y
  Kyverno. **Todavía no:** Argo Rollouts, service mesh, SIEM.
- **Días 1–30:** entender y apagar incendios: inventario, línea base de DORA, MFA, OIDC en el CI, CloudTrail +
  GuardDuty.
- **Días 31–60:** la carretera con un servicio piloto: plantilla, Argo CD, Kyverno en Audit, External Secrets,
  Payload Codec.
- **Días 61–90:** todos por el camino nuevo, Kyverno en Enforce, primer simulacro y la hoja de ruta de la siguiente
  certificación.
- Éxito: 100% de despliegues por el pipeline, DORA igual o mejor que la línea base, controles de Vanta en verde.

**Diagrama** (`d10`): a la izquierda, tres columnas: "Ya lo tienen" (GitHub, AWS, Vanta, PostHog, Grafana), "Nuevo" (Argo
CD, Kyverno) y "Todavía no" (Argo Rollouts, service mesh, SIEM). A la derecha, la hoja de ruta: Días 1–30 → 31–60 →
61–90, y abajo los indicadores de éxito (100% de despliegues por el pipeline, DORA contra la línea base, controles de
Vanta en verde, tiempo para responder un cuestionario de seguridad).

**Guion:**
"Antes de traer herramientas, quito las que sobran. Si yo les propusiera doce herramientas nuevas para catorce
desarrolladores, ustedes me preguntarían con razón: ¿y quién opera todo eso? Además, en Dapta cada proveedor nuevo es
un subprocesador más que auditar.
Por eso cada herramienta pasa siete preguntas: qué dolor resuelve, si ya lo resuelve algo que pagamos, cuánto cuesta
de verdad, quién la opera, si la decisión se puede devolver, qué evidencia genera y si frena o acelera al equipo. Cada
decisión queda escrita en un ADR, Architecture Decision Record, que además es evidencia para el SOC 2.
El resultado: casi todo es lo que ya tienen, GitHub, AWS, PostHog, Grafana y Vanta. Nuevo de verdad, solo dos piezas:
Argo CD y Kyverno. Y tres cosas que todavía no: Argo Rollouts, un service mesh y un SIEM.
El plan. Primeros treinta días: entender y apagar incendios, con inventario, línea base y victorias rápidas como MFA y
OIDC. Del 31 al 60: la carretera con un solo servicio piloto. Del 61 al 90: todos por el camino nuevo, Kyverno en
Enforce, el primer simulacro y la hoja de ruta de la siguiente certificación.
¿Cómo sabemos que funcionó? Cien por ciento de despliegues por el pipeline, DORA igual o mejor que la línea base y los
controles de Vanta en verde.
Al día 90, el camino seguro es el camino fácil, y la evidencia le llega sola al auditor. Muchas gracias."

**Preguntas probables:**
1. *¿Qué harías la primera semana?* — Escuchar y medir antes de cambiar: quién tiene acceso a producción, cuántas
   cuentas de AWS hay, dónde están los secretos, en qué va cada migración y qué excepciones dejó el informe del SOC 2.
2. *¿Cuánto cuesta esto?* — Casi todo es software abierto o ya está pagado. Lo nuevo en AWS (GuardDuty, Security Hub,
   CloudTrail organizacional) cobra por volumen; lo mido con la factura real antes de dar una cifra. El costo grande es
   tiempo de personas, y por eso arranco con victorias rápidas y un piloto.
3. *¿Por qué no traes Cosign para firmar imágenes?* — Tiene sentido cuando Kyverno pase a Enforce y pueda exigir la
   firma. Antes, firmar sin verificar no protege nada: va en la segunda vuelta.

---

## Anexo — Preguntas para hacerle a la mesa

Se hacen durante la exposición o al final. Muestran que el diseño parte de Dapta, no de la herramienta. Lo que no se
responda, lo responden los primeros 30 días.

1. ¿Qué certificación o requisito concreto les han pedido los clientes que hoy no pueden cumplir? ¿Hay un contrato
   esperando? (D3)
2. ¿Cómo despliegan hoy, y quién tiene acceso directo a producción? (D4)
3. ¿En qué punto va la migración a Kubernetes y desde dónde migran? (D6)
4. ¿Usan Temporal Cloud o lo operan ustedes? ¿Qué datos viajan dentro de los workflows? (D6)
5. ¿Qué hace exactamente el equipo de ataque y cómo se coordina con defensa? (D8)
6. ¿Quién mantiene hoy Vanta y la evidencia del SOC 2? (D10)
