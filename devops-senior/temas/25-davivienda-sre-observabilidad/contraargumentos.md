# Contraargumentos y matices — revisión de decisiones (D1–D30)

> Al corregir cada decisión del [análisis de alternativas](analisis-alternativas.md), aquí quedan los
> **contraargumentos y matices** que la mesa podría usar contra tu decisión, y cómo responderlos. Léelos antes
> del ensayo.

## D7 — Gate con deployment protection rule

**Tu decisión:** la deployment protection rule es el gate principal (Plataforma controla, tribus extienden).

**Contraargumentos que puede hacer la mesa:**
1. *"Si el job no declara `environment: production`, la regla nunca se activa."* → La confianza OIDC (OpenID
   Connect) de AWS y GCP solo entrega credenciales de producción a tokens con `sub` = `environment:production`
   (y `job_workflow_ref` = plantilla oficial). Sin environment, no hay credenciales.
2. *"Soy administrador del repositorio: le quito la regla al environment."* → Los environments y sus reglas se
   definen como código (Terraform, provider de GitHub) y los gestiona Plataforma; las tribus no son
   administradoras. Cualquier cambio pasa por pull request y queda auditado.
3. *"¿Y si despliegan a mano con `kubectl`, por fuera del pipeline?"* → Admission controller (OPA Gatekeeper o
   Kyverno) que rechaza imágenes sin firma o sin SBOM; y nadie tiene credenciales de escritura directa en
   producción (solo el pipeline / GitOps).
4. *"Plataforma se vuelve cuello de botella."* → Solo imponemos el piso; las tribus extienden sin pedir permiso
   y contribuyen por inner source.

## D8 — Argo Rollouts o automatizar el service mesh existente

**Tu decisión:** dos opciones según el stack del banco; no imponer herramientas nuevas; considerar licencias.

**Matices y contraargumentos:**
1. **Argo Rollouts no exige Argo CD.** Es un controlador independiente. Si te dicen *"no tenemos Argo CD"*, la
   opción A sigue viva: Argo Rollouts usa el ingress, el balanceador (AWS ALB) o el mesh que ya tengan.
2. *"Argo Rollouts nos obliga a cambiar todos los Deployments."* → `workloadRef` permite que el `Rollout`
   reutilice el Deployment existente; o se va por la opción B (Flagger no toca los Deployments).
3. **Linkerd ya no es "gratis" para un banco:** desde 2024 las versiones *stable* requieren licencia de Buoyant
   para empresas de más de 50 empleados. Si el banco usa Linkerd, hay que contar ese costo (o usar *edge*).
4. **AWS App Mesh está descontinuado** (fin de soporte: 30 de septiembre de 2026). Si lo usan, no construir el
   canary encima: es la oportunidad de migrar.
5. *"¿Por qué no instalar Istio y listo?"* → Un mesh solo para canary es caro (+10–20% de recursos por los
   sidecars) y es otra pieza crítica. Se usa si ya existe o si hay otras razones (mTLS, políticas de tráfico).

## D8-bis — Estrategias de despliegue

**Tu decisión:** sin cambios.

## D10 y D11 — OpenTelemetry y la distribución del Collector

**Tu decisión:** no son decisiones propias; el enunciado exige OpenTelemetry y el OTel Collector.

**Matices por si la mesa insiste:**
1. *"¿Por qué OpenTelemetry y no el agente de Datadog o Dynatrace, que es más fácil?"* → Además de que lo pide
   el caso: neutralidad (cambiar de backend sin reinstrumentar), un solo estándar para AWS, GCP y el
   datacenter, y control de los datos dentro del banco (PII, costos) antes de enviarlos a cualquier proveedor.
2. **eBPF no compite con OpenTelemetry:** Grafana donó Beyla al proyecto OpenTelemetry (OpenTelemetry eBPF
   Instrumentation, OBI), así que la instrumentación sin código también cabe dentro del estándar que pide el caso.
3. **Dentro de la restricción todavía hay una sub-decisión: qué distribución del Collector.** Opciones: la
   distribución *contrib* (trae todos los componentes), una construida con OCB (OpenTelemetry Collector Builder,
   solo los componentes aprobados) o la de un proveedor (AWS ADOT, Grafana Alloy, Splunk). Respuesta: *"OCB,
   porque menos componentes es menos superficie de ataque y menos parches; las de proveedor sesgan a ese
   proveedor en un banco multi-cloud"*. Le suma a DevSecOps.

## D14 — Dónde se enmascara la PII

**Tu decisión:** cada aplicación debe enmascarar la PII (Personally Identifiable Information); Plataforma agrega
una seguridad extra con el processor `redaction` en el gateway.

**Contraargumentos y respuestas:**
1. *"Si cada aplicación ya enmascara, ¿para qué el gateway?"* → Defensa en profundidad: basta un desarrollador
   que loguee el objeto completo de la petición para que una cédula se escape. El gateway es la red final y el
   **único punto auditable** frente a la SFC y la SIC (Superintendencia de Industria y Comercio).
2. *"Entre la aplicación y el gateway el dato viaja en claro."* → Viaja dentro de la red del banco y cifrado con
   mTLS (OTLP sobre TLS mutuo). Y si la aplicación cumple su parte, ni siquiera viaja.
3. *"Las expresiones regulares fallan: un formato nuevo se escapa."* → Por eso el `redaction` se configura en
   **modo lista permitida** (`allowed_keys`): todo atributo que no esté aprobado se borra, en vez de intentar
   adivinar qué es PII. Los patrones (cédula, tarjeta) son una segunda capa.
4. *"¿Y el cuerpo del log (texto libre)?"* → Se complementa con el processor `transform` (OTTL,
   `replace_pattern`). Y la plantilla de logging estructurado evita meter PII en texto libre.
5. *"Si borras la cédula, ¿cómo correlaciono los eventos de un cliente?"* → **Hash** (con sal) en vez de borrar:
   el mismo cliente produce el mismo valor, pero no se puede revertir. Para tarjetas, PCI DSS permite mostrar
   los primeros 6 y los últimos 4 dígitos.
6. *"¿Cómo sabes que funciona?"* → Pruebas con PII sintética en el pipeline del Collector y un escaneo periódico
   de los backends buscando patrones; si aparece algo, es un incidente de seguridad.
7. *"¿No le cuesta rendimiento al gateway?"* → Algo de CPU por las expresiones regulares; es despreciable frente
   al costo de una sanción por la Ley 1581.

## D15 — Backends de almacenamiento

**Tu decisión:** es una decisión general de la organización; si nos dejan sugerir, el stack de Grafana (Mimir,
Tempo, Loki y Grafana).

**Contraargumentos y respuestas:**
1. **Licencia AGPL (ojo, el más importante para un banco).** Mimir, Tempo, Loki y Grafana son **AGPLv3** desde
   2021. Para uso interno sin modificar el código no obliga a nada, pero muchas áreas jurídicas de banca revisan
   el AGPL con lupa. Respuesta: *"Lo usamos sin modificarlo e internamente; si el área jurídica lo prefiere, existe
   Grafana Enterprise (licencia comercial y soporte) o Grafana Cloud"*. Mejor decirlo tú antes de que te lo digan.
2. *"Ya tenemos Datadog / Dynatrace."* → Perfecto: OpenTelemetry nos deja exportar a ambos a la vez y migrar por
   partes (o no migrar). No se propone cambiar el backend en la presentación; se propone que el Collector nos dé
   esa libertad.
3. *"Autogestionar Mimir y Loki es mucho trabajo."* → Cierto: cuesta 2–4 FTE. A volumen de banco, ese costo es
   menor que la factura SaaS (~30–50% del SaaS). A poco volumen, el SaaS gana; por eso es una decisión de escala.
4. *"Loki no busca texto libre tan bien como Elasticsearch."* → Correcto: Loki solo indexa etiquetas, por eso es
   barato; las búsquedas sin filtrar por etiqueta son más lentas. Con trace_id en cada log (que ya proponemos), se
   llega al log exacto desde la traza sin búsquedas de texto libre.
5. *"¿Y la alta cardinalidad?"* → En Loki, las etiquetas deben ser pocas (servicio, ambiente, nivel); el trace_id
   va en el contenido, no como etiqueta. En Mimir, límites de series por tenant para que una tribu no dispare la
   factura de todos.
6. *"¿Una instancia o dos en multi-cloud?"* → Una por nube (sin pagar egress entre nubes) y Grafana consulta
   ambas como fuentes de datos.

**Ajuste a D15 (segunda corrección):** no se fuerza Grafana. Regla: reutilizar lo contratado u operado, llenar
solo los huecos por señal y sugerir Grafana solo desde cero.

7. *"Ya usamos Prometheus + Thanos, ¿para qué Mimir?"* → No hace falta: Thanos y Mimir resuelven lo mismo
   (almacenamiento de largo plazo y escalable para Prometheus, con PromQL). Se mantiene Thanos. Cambiar costaría
   migración y dos sistemas en paralelo, **no licencias** (Mimir es gratis).
8. **Ojo con el argumento del licenciamiento:** el stack de Grafana en su versión abierta **no cobra licencia**.
   El costo de "venir a poner Grafana" sobre algo que ya existe es de **personas y operación** (migrar, operar dos
   sistemas, reentrenar), salvo que se compre Grafana Enterprise o Grafana Cloud. Y casi siempre **Grafana (la
   interfaz de dashboards) ya está** donde hay Prometheus y Thanos: la discusión real es Mimir vs. Thanos, no
   "Grafana sí o no".

## D17 — Cifra de ahorro (se quitó)

**Tu decisión:** no dar cifras de ahorro inventadas; hace falta un estudio previo de la línea base. Solo números
con fuente.

**Contraargumentos y respuestas:**
1. *"Entonces, ¿cuánto nos vamos a ahorrar?"* → *"No les doy una cifra sin sus datos: comprometer un número
   inventado sería irresponsable. En 2–4 semanas de estudio de la línea base les doy la cifra real. Lo que sí sé
   es que la meta del −30% es alcanzable, por casos públicos."*
2. *"¿Qué casos?"* → **Capital One** (banco): ~70% menos volumen de trazas con OpenTelemetry (The New Stack).
   **Pismo** (plataforma de pagos, hoy de Visa): ~80% menos costo de observabilidad con tail sampling (charla en
   KubeCon EU 2024, con Grafana Labs). Ojo: son su volumen y su factura, no los de Banco Plus.
3. *"¿Y si después del estudio no llega al 30%?"* → Se reporta con datos y se ajustan las palancas (más
   Log-to-Metrics, retención por niveles, límites de cardinalidad por tribu). La meta es del caso; el compromiso
   es medirla con honestidad.

## D18 — Servidor MCP propio como puente entre la telemetría vieja y la nueva

**Tu aporte:** el servidor MCP propio permite migrar fácil del desorden al orden: el agente usa las mismas
herramientas mientras por debajo se pasa de la telemetría heredada a OpenTelemetry.

**Contraargumentos y respuestas:**
1. *"Mantener adaptadores para lo viejo es más trabajo."* → Sí, por eso son **temporales**: cada adaptador
   heredado tiene fecha de retiro en la hoja de ruta. Es más barato que esperar a migrar todo antes de usar IA.
2. *"Con logs viejos sin `trace_id` ni Semantic Conventions, la IA no va a correlacionar bien."* → Correcto, y es
   un argumento a favor de migrar: el servidor MCP marca de qué fuente viene cada dato y su calidad, y la
   precisión del RCA (Root Cause Analysis) en los servicios migrados vs. los viejos se vuelve el indicador que
   empuja a las tribus a migrar.
3. *"La capa de abstracción puede esconder la deuda para siempre."* → Por eso se mide: porcentaje de servicios
   que ya responden con OpenTelemetry, visible en el IDP. La capa ayuda a la transición, no la reemplaza.
4. *"Darle acceso a la IA a sistemas heredados es un riesgo."* → Mismas reglas que para lo nuevo: solo lectura,
   mínimo privilegio, enmascaramiento de PII antes de responder y auditoría de cada llamada.
5. **Nombre del patrón para la mesa:** *strangler fig* (higuera estranguladora): lo nuevo crece alrededor de lo
   viejo y lo va reemplazando por partes, sin un "big bang".
