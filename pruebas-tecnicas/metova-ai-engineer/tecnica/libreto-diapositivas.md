# Libreto de diapositivas - Entrevista técnica Metova Talent (AI Engineer)

Entrevista técnica del 6 nov 2026. Habilidades que van a preguntar:

1. Frameworks de agentes: LangChain, LlamaIndex, AutoGen, CrewAI o similares.
2. Python con FastAPI, asyncio, Pydantic y arquitecturas asíncronas.
3. Liderar colaboración y discusiones técnicas con producto, UX, datos y backend.
4. Arquitectura de soluciones con agentes inteligentes y LLM.
5. MCP (Model Context Protocol) y A2A (Agent-to-Agent) para coordinar varios agentes y flujos autónomos.

Formato: `Sección`, `Diagrama` (de [diagramas-c4.md](diagramas-c4.md)), viñetas en pantalla y `>`
guion para decir en voz alta (tecla **N**). Se genera con `python3 generar_presentacion.py`.

Regla de oro: **nunca digas "no lo he usado"**. Da el ejemplo real más cercano y di "me siento cómodo
adoptándolo". **Tampoco digas que usaste un framework que no usaste**, porque te pueden pedir código.
**[confirmar]**: si usaste FastAPI en el trabajo o solo en proyectos propios, y en qué lenguaje
escribiste tus servidores MCP.

---

## Entrevista técnica · Metova Talent · AI Engineer
**Sección:** Portada
- **Hoy, viernes 6 nov · 5:00 – 5:30 p. m. hora Colombia** (4:00 p. m. de México) · Google Meet
- Las **5 habilidades** que van a evaluar, en una **serie de 11 preguntas (P1 a P11)**
- Para cada una: **concepto** → **tu experiencia real** → **cómo lo harías**
- Teclas: ← → para moverse · N para ver el guion

> La estrategia para toda la entrevista: primero muestras que entiendes el concepto, después lo conectas con lo que hiciste en producción en MercadoLibre y terminas con cómo lo harías en su caso. Nunca te quedes solo en la teoría.

---

## Plan de los 30 minutos
**Sección:** Antes de empezar
- **0-3 min**: saludo + **P1** (tu sistema con LLM) en **90 segundos**
- **3-22 min**: entre **5 y 7 preguntas** técnicas: **60-90 s por respuesta**, empezando por el ejemplo real
- **22-28 min**: **tus preguntas** técnicas (stack, framework, proveedor de LLM, el equipo)
- **28-30 min**: siguientes pasos
- Si te piden pantalla o código: **piensa en voz alta**, empieza por el diagrama y después el detalle

> En 30 minutos no hay tiempo para respuestas largas. Usa la fórmula de siempre: una frase de concepto, una de tu experiencia real y una de cómo lo harías. Si el entrevistador quiere más detalle, te lo pide. Ten agua y la cámara encendida, y entra al Meet dos minutos antes.

---

## La serie de preguntas (en orden de probabilidad)
**Sección:** Antes de empezar
- **P1** Cuéntame de un sistema con LLM · **P2** ¿Has implementado MCP? · **P3** MCP vs A2A
- **P4** Diseña un sistema multiagente · **P5** ¿Cómo haces seguro un flujo autónomo?
- **P6** ¿Has usado LangChain / LlamaIndex / CrewAI / AutoGen?
- **P7** ¿FastAPI y asyncio? · **P8** Errores comunes con asyncio · **P9** ¿Cómo validas lo que devuelve el LLM?
- **P10** ¿Cómo lideras discusiones entre producto, UX, datos y backend?
- **P11** ¿Cómo evalúas y operas los agentes?

> Las preguntas de la 1 a la 5 son las más probables, porque son el corazón del rol: agentes, MCP y A2A. Si solo alcanzas a repasar cinco antes de la llamada, que sean esas. La 6 seguro sale porque está en la vacante, y ahí se aplica la regla de dar el ejemplo más cercano.

---

## Mapa: lo que piden contra lo que hiciste
**Sección:** Antes de empezar
**Diagrama:** T1
- **Frameworks de agentes** ← tu triage: **orquestación + herramientas + estado + HITL** (human-in-the-loop)
- **FastAPI / asyncio / Pydantic** ← **Python 5 años**, APIs REST en Bizagi
- **MCP** ← **varios servidores MCP** construidos, uno **co-diseñado con observabilidad**
- **A2A** ← el siguiente paso natural de MCP: agente ↔ agente
- **Liderar equipos** ← **líder de proyectos** (alcance, tiempos, equipos, áreas usuarias)

> Tu fortaleza es que ya llevaste un LLM a producción con controles reales. Los frameworks son la forma estándar de hacer lo que tú ya hiciste a mano: orquestar el modelo, darle herramientas, guardar estado y meter una aprobación humana.

---

## P1 · "Cuéntame de un sistema con LLM que hayas construido"
**Sección:** Pitch técnico
**Diagrama:** T6
- **Triage de incidentes** en MercadoLibre, **en producción**, con **Claude (Anthropic)**
- Flujo: **dependencias → logs vía MCP → casos pasados (RAG) → diagnóstico → aprobación humana**
- **Harness + hooks** que bloqueaban vulnerabilidades y acciones no deseadas
- **Mis aportes**: mapeo de dependencias, runbooks, **diseño del MCP**, pruebas y base de conocimiento
- En LangGraph sería: **un nodo por paso + arista condicional + `interrupt()`**

> En MercadoLibre participé en un sistema de triage de incidentes con Claude en producción. Cuando llegaba un ticket, el sistema ubicaba el servicio que fallaba con un mapa de dependencias, leía sus logs a través de un servidor MCP, recuperaba runbooks y casos pasados, que es un patrón RAG, y entregaba un diagnóstico con certezas, incertidumbres y una ruta de acción. Una persona siempre aprobaba antes de ejecutar. Todo iba envuelto en un harness con hooks que bloqueaban acciones no deseadas. Si lo modelara hoy en LangGraph, cada paso sería un nodo, la decisión de aprobar o reenrutar sería una arista condicional y la aprobación humana sería un interrupt con checkpointer.

---

## MCP (Model Context Protocol): cómo funciona
**Sección:** MCP y A2A
**Diagrama:** T2
- Estándar abierto de **Anthropic** para conectar un LLM a **herramientas y datos**
- **Host** (la app) → **cliente MCP** (uno por servidor) ↔ **servidor MCP**
- Mensajes **JSON-RPC 2.0** · transportes **stdio** (local) y **Streamable HTTP** (remoto)
- El servidor expone **tools** (acciones), **resources** (datos) y **prompts** (plantillas)
- El cliente puede ofrecer **sampling**, **roots** y **elicitation** · seguridad remota con **OAuth 2.1**

> MCP, Model Context Protocol, es un estándar abierto que creó Anthropic para conectar modelos con herramientas y datos de una forma uniforme. Hay un host, que es la aplicación de IA, y dentro del host hay un cliente MCP por cada servidor MCP. Hablan en JSON-RPC 2.0, ya sea por stdio si es local o por Streamable HTTP si es remoto, y en ese caso con OAuth 2.1. El servidor expone tres cosas: tools, que son acciones; resources, que son datos para leer, y prompts, que son plantillas. La gran ventaja es que pasas de integrar N modelos por M herramientas a que cada herramienta se integre una sola vez.

---

## P2 · "¿Has implementado MCP?"
**Sección:** MCP y A2A
- **Sí**: he construido **varios servidores MCP**
- En MercadoLibre **co-diseñé** el servidor MCP con el equipo de **observabilidad (o11y)** para que el LLM leyera logs
- Diseño: tools **pequeñas y con nombres claros**, descripciones precisas y schemas estrictos
- Seguridad: **solo lectura por defecto**, menor privilegio, **hooks** que bloquean acciones peligrosas
- Producción: **timeouts, paginación** de resultados grandes, **auditoría** de cada llamada

> Sí, he construido varios servidores MCP. El más importante fue el de MercadoLibre, que co-diseñé con el equipo de observabilidad para que el LLM pudiera consultar logs y métricas. Lo que aprendí es que el diseño de las tools importa mucho: pocas tools, con nombres y descripciones claras y schemas estrictos, porque el modelo decide a partir de esas descripciones. En seguridad, todo era de solo lectura por defecto, con menor privilegio, y los hooks del harness bloqueaban cualquier acción no deseada. También limitábamos el tamaño de las respuestas y auditábamos cada llamada.

---

## A2A (Agent-to-Agent): cómo funciona
**Sección:** MCP y A2A
**Diagrama:** T3
- Protocolo abierto que lanzó **Google** (2025), hoy en la **Linux Foundation**
- **Agent Card**: JSON público con las **skills**, la URL y la autenticación del agente
- **JSON-RPC 2.0 sobre HTTPS** · **SSE** (Server-Sent Events) para streaming · webhooks para push
- **Task** con estados: submitted → working → **input-required** → completed / failed / canceled
- Resultado en **Artifacts** con **parts** (texto, archivo, datos) · los agentes son **opacos**

> A2A, Agent-to-Agent, es un protocolo abierto que lanzó Google en 2025 y que ahora está en la Linux Foundation. Cada agente publica una Agent Card, un JSON que dice qué sabe hacer, dónde está y cómo autenticarse. El agente cliente descubre esa Agent Card y le manda una tarea por JSON-RPC sobre HTTPS. La tarea pasa por estados, y uno importante es input-required, cuando el agente remoto necesita algo más. El avance llega por streaming con SSE o por webhooks, y el resultado llega como artifacts. Los agentes son opacos: no comparten su memoria ni sus herramientas internas, solo el contrato.

---

## P3 · "¿Cuál es la diferencia entre MCP y A2A?"
**Sección:** MCP y A2A
- **MCP = agente ↔ herramienta** (vertical): el agente **usa** una capacidad
- **A2A = agente ↔ agente** (horizontal): el agente **delega** una tarea a otro agente autónomo
- **Son complementarios**: cada agente usa MCP por dentro y A2A para hablar con otros
- A2A sirve cuando **otro equipo u otro proveedor** es dueño del agente
- Si todo está en un solo servicio, basta con un **supervisor** en LangGraph (sin red de por medio)

> MCP conecta un agente con herramientas y datos: el agente llama una tool y recibe un resultado. A2A conecta agentes entre sí: el agente delega una tarea completa a otro agente que razona por su cuenta y puede pedir más información. Son complementarios: cada agente usa MCP por dentro para sus herramientas y A2A hacia afuera para coordinarse. Yo usaría A2A cuando el otro agente es de otro equipo o de otro proveedor. Si todos los agentes viven en el mismo servicio, un supervisor dentro de LangGraph es más simple y no pagas la latencia de la red.

---

## P4 · "Diseña un sistema multiagente para un negocio"
**Sección:** Arquitectura
**Diagrama:** T4
- **1 · Entender el problema**: qué tarea, qué métrica de éxito y qué riesgo tiene equivocarse
- **2 · Entrada**: **API FastAPI** con validación **Pydantic** y streaming **SSE**
- **3 · Orquestación**: **supervisor** con estado y checkpoints (LangGraph) → agentes especialistas
- **4 · Integración**: herramientas por **MCP** y agentes de otros equipos por **A2A**
- **5 · Control**: **guardarraíles**, **aprobación humana** para acciones de riesgo, **observabilidad** (trazas, costo, calidad)

> Primero pregunto qué problema resolvemos, cómo medimos el éxito y qué tan grave es que el agente se equivoque, porque eso define cuánta autonomía le doy. La entrada sería una API en FastAPI que valida con Pydantic y devuelve streaming por SSE. Detrás, un agente supervisor con estado persistente, por ejemplo en LangGraph con checkpointer en Postgres, que reparte el trabajo a agentes especialistas. Las herramientas del negocio, como CRM o tickets, entran por servidores MCP, y los agentes que son de otros equipos se conectan por A2A. Encima, guardarraíles, aprobación humana para lo riesgoso y observabilidad con trazas, costo por token y evaluación. Todo corre en Kubernetes con el CI/CD de siempre.

---

## P5 · "¿Cómo haces seguro un flujo autónomo en producción?"
**Sección:** Arquitectura
- **Autonomía por niveles**: leer = automático · escribir = con aprobación · irreversible = siempre humano
- **Menor privilegio**: cada agente con sus credenciales y solo sus tools
- **Límites**: máximo de pasos, **timeouts**, presupuesto de tokens y costo por tarea
- **Idempotencia** y reintentos seguros · **auditoría** de cada decisión y cada llamada
- **Prompt injection**: tratar el contenido externo como datos, nunca como instrucciones · validar salidas con **Pydantic**

> Lo pienso por niveles de autonomía: leer información puede ser automático, escribir necesita aprobación, y lo irreversible siempre lo aprueba una persona. Así lo teníamos en el triage. Cada agente tiene sus propias credenciales y solo las tools que necesita. Pongo límites de pasos, timeouts y presupuesto de tokens para que un agente no se quede en un ciclo infinito gastando plata. Las acciones son idempotentes para que reintentar sea seguro, y todo queda auditado. Y contra el prompt injection, lo que viene de afuera se trata como dato, y las salidas del modelo se validan con Pydantic antes de ejecutar nada.

---

## Frameworks: la idea central de cada uno
**Sección:** Frameworks
**Diagrama:** T5
- **LangChain**: piezas para armar apps con LLM (modelos, prompts, tools, retrievers) · **LangGraph**: **grafo con estado**
- **LlamaIndex**: centrado en **datos y RAG**: Documents → Nodes → Index → query engine
- **AutoGen** (Microsoft): **agentes que conversan** entre sí (group chat) · su sucesor es el **Microsoft Agent Framework**
- **CrewAI**: agentes **por roles** (role, goal, backstory) que cumplen Tasks dentro de una **Crew**
- **Cuándo cuál**: control fino → **LangGraph** · RAG pesado → **LlamaIndex** · roles rápidos → **CrewAI**

> LangChain da las piezas básicas para trabajar con LLM, y LangGraph, que es de los mismos creadores, modela el agente como un grafo con estado, que es lo que más se usa en producción porque te da control. LlamaIndex está más enfocado en datos y RAG: carga documentos, los parte en nodos, crea índices y consulta. AutoGen, de Microsoft, se basa en agentes que conversan entre sí, y Microsoft lo está unificando con Semantic Kernel en el Microsoft Agent Framework. CrewAI organiza agentes por roles, cada uno con un objetivo, que cumplen tareas dentro de un equipo, o crew. Si necesito control fino y aprobación humana, elijo LangGraph.

---

## LangChain: las piezas
**Sección:** Frameworks
**Diagrama:** T9
- **Chat model** (`ChatAnthropic`, `ChatOpenAI`): misma interfaz para cualquier proveedor de LLM
- **Prompt template** (`ChatPromptTemplate`) · **tools** (`@tool`, `.bind_tools()`) · **retrievers** para RAG
- **Structured output**: `.with_structured_output(ModeloPydantic)`, como tu diagnóstico del triage
- **LCEL** (LangChain Expression Language): `prompt | modelo | parser` · todo es **Runnable**: `invoke`, `ainvoke`, `stream`, `batch`
- **langchain-mcp-adapters**: tus servidores MCP como tools · en **LangChain 1.0** `create_agent` corre sobre **LangGraph**

> LangChain es la caja de piezas: modelos, prompts, tools, retrievers y salida estructurada. Las piezas se encadenan con LCEL usando un pipe, como en Linux: prompt, luego modelo, luego parser. Todas las piezas de LangChain son Runnables, así que tienen invoke y también ainvoke, que es la versión asíncrona. Con langchain-mcp-adapters cargo mis servidores MCP como tools. Y desde LangChain 1.0, los agentes se crean con create_agent, que por debajo corre sobre LangGraph.

---

## LangGraph: los 5 conceptos
**Sección:** Frameworks
**Diagrama:** T6
- **1 · State**: un `TypedDict` con lo que viaja por el grafo (ticket, servicio, diagnóstico)
- **2 · Nodes**: funciones que reciben el estado y devuelven **solo lo que cambiaron**
- **3 · Edges**: `add_edge` y **`add_conditional_edges`** (decisiones y **ciclos**)
- **4 · Checkpointer**: guarda el estado en cada paso (`MemorySaver`, **`PostgresSaver`**) por **`thread_id`**
- **5 · `interrupt()`**: pausa para la aprobación humana · se retoma con **`Command(resume=...)`**
- Extras: **`ToolNode`** + **`tools_condition`** (ciclo ReAct) · **supervisor** y **subgrafos** · `stream` · trazas en **LangSmith**

> LangGraph controla el flujo como un grafo con estado. El estado es un TypedDict. Los nodos son funciones que devuelven solo lo que cambiaron. Las aristas condicionales deciden el camino y permiten ciclos, como volver a leer logs si faltan datos. El checkpointer guarda el estado en cada paso por thread_id, así el grafo se puede pausar, retomar y sobrevivir a un reinicio. Y interrupt pausa el grafo para la aprobación humana, que se retoma con Command resume. Mi triage se traduce uno a uno: cada paso es un nodo, aprobar o reenrutar es una arista condicional y la aprobación es un interrupt. Uso LangChain solo para una cadena lineal, y LangGraph cuando hay ciclos, estado o aprobación humana.

---

## LlamaIndex: el framework de datos para RAG
**Sección:** Frameworks
**Diagrama:** T10
- **Readers** (`SimpleDirectoryReader`, conectores de **LlamaHub**, **LlamaParse** para PDF) → **Documents**
- **Node parser** (`SentenceSplitter`) → **Nodes** · todo en un **`IngestionPipeline`**
- **`VectorStoreIndex`** sobre pgvector, OpenSearch, etc. → **retriever** (top-k + **reranker**)
- **`index.as_query_engine()`** responde · **chat engine** para conversación
- Agentes: **`FunctionAgent`**, **`AgentWorkflow`** · **Workflows** por eventos con `@step`

> LlamaIndex es el framework más fuerte en datos y RAG. Los readers cargan documentos, y para PDF difíciles está LlamaParse. El node parser los parte en nodes, el VectorStoreIndex guarda los embeddings en una base vectorial, el retriever trae los top-k con un reranker y el query engine arma la respuesta. Para agentes tiene FunctionAgent y AgentWorkflow, y los Workflows son pasos que reaccionan a eventos. Si mi problema es sobre todo buscar en documentos, como los runbooks del triage, elijo LlamaIndex.

---

## CrewAI: un equipo de agentes por roles
**Sección:** Frameworks
**Diagrama:** T11
- **Agent**: **role**, **goal**, **backstory**, tools y LLM
- **Task**: **description**, **expected_output**, el agente que la hace, **`context=[otra_task]`**, `output_pydantic`
- **Crew**: agentes + tareas + **Process**: **sequential** o **hierarchical** (un **manager** delega)
- `crew.kickoff(inputs={...})` · `human_input=True` en una Task para la aprobación humana
- **Flows**: control por eventos (`@start`, `@listen`, `@router`) cuando necesitas más control

> CrewAI organiza agentes como un equipo de trabajo. Cada Agent tiene un rol, un objetivo y una historia de fondo, que es su personalidad dentro del prompt. Cada Task tiene una descripción y la salida esperada, y puede usar el resultado de otra tarea como contexto. La Crew junta agentes y tareas con un proceso secuencial, o jerárquico si un manager reparte el trabajo. Se lanza con kickoff. Es el más rápido para armar un prototipo multiagente, y cuando necesitas más control usas Flows.

---

## AutoGen (Microsoft): agentes que conversan
**Sección:** Frameworks
**Diagrama:** T12
- **AgentChat**: **`AssistantAgent`** (LLM + tools) y **`UserProxyAgent`** (la persona)
- **Teams**: **`RoundRobinGroupChat`** (por turnos), **`SelectorGroupChat`** (un LLM elige quién habla), **`Swarm`** (handoffs)
- **Termination**: `TextMentionTermination("APPROVE")`, `MaxMessageTermination`
- **Core**: modelo de **actores asíncronos** que se mandan mensajes (puede ser distribuido) · **todo es `async`**
- Sucesor: **Microsoft Agent Framework** (AutoGen + Semantic Kernel, desde octubre de 2025)

> AutoGen, de Microsoft, modela el trabajo como una conversación entre agentes. Un AssistantAgent es un LLM con tools, y el UserProxyAgent representa a la persona. Los agentes se organizan en equipos: por turnos con RoundRobinGroupChat, con un LLM que elige quién habla con SelectorGroupChat o con traspasos con Swarm. La conversación termina con una condición, por ejemplo cuando alguien dice APPROVE. Por debajo está AutoGen Core, un modelo de actores asíncronos. Microsoft lo está unificando con Semantic Kernel en el Microsoft Agent Framework, y eso vale la pena mencionarlo.

---

## Equivalentes: LangChain / LangGraph y LlamaIndex
**Sección:** Frameworks
- **LangChain / LangGraph** (orquestar LLM y agentes) ≈ **Semantic Kernel** (Microsoft) · **Haystack** (deepset) · **Pydantic AI** · **DSPy** · **smolagents** (Hugging Face) · **Agno**
- SDK de los proveedores: **OpenAI Agents SDK** · **Google ADK** (Agent Development Kit) · **Claude Agent SDK** (Anthropic) · **Strands Agents** (AWS)
- En TypeScript: **Mastra** · **Vercel AI SDK** · **LangGraph.js**
- **LlamaIndex** (datos y RAG) ≈ **Haystack** · retrievers de **LangChain** · **txtai** · **RAGFlow**
- RAG administrado en la nube: **Amazon Bedrock Knowledge Bases** · **Azure AI Search** · **Vertex AI RAG Engine**

> Si te preguntan por un framework que no conoces, ubícalo en una de estas familias: orquestación de agentes, como LangGraph; datos y RAG, como LlamaIndex; o agentes que conversan o trabajan por roles, como AutoGen y CrewAI. Cada proveedor de LLM tiene ya su propio SDK de agentes, y como trabajaste con Claude, el más cercano a tu experiencia es el Claude Agent SDK de Anthropic. Ojo: menciónalo como el equivalente, no como algo que hayas usado.

---

## Equivalentes: AutoGen, CrewAI y en la nube
**Sección:** Frameworks
- **AutoGen** (agentes que conversan) ≈ **Microsoft Agent Framework** (su sucesor) · **AG2** (fork comunitario de AutoGen) · **Semantic Kernel Agents** · **CAMEL**
- **CrewAI** (equipo por roles) ≈ **supervisor en LangGraph** · **OpenAI Agents SDK** (handoffs) · **Google ADK** · **Agno** · **MetaGPT**
- Agentes administrados: **Amazon Bedrock Agents / AgentCore** · **Azure AI Foundry Agent Service** · **Vertex AI Agent Engine**
- Protocolos que unen a todos: **MCP** (herramientas) y **A2A** (agente ↔ agente)
- **Lo tuyo**: orquestación propia = **harness + hooks + MCP** con Claude

> AutoGen tiene dos caminos: Microsoft lo está reemplazando con el Microsoft Agent Framework, y la comunidad siguió con un fork llamado AG2. CrewAI se puede reemplazar con un supervisor en LangGraph o con los handoffs del OpenAI Agents SDK. Las nubes ofrecen agentes administrados: Bedrock Agents y AgentCore en AWS, Azure AI Foundry Agent Service y Vertex AI Agent Engine. Y lo que conecta a todos estos frameworks son los protocolos MCP y A2A, que es tu punto fuerte. Si un framework habla MCP, tus servidores MCP le sirven tal cual.

---

## P6 · "¿Has usado LangChain / LlamaIndex / CrewAI / AutoGen?"
**Sección:** Frameworks
- **No digas "no"**: "En producción orquesté el flujo directamente con el modelo, un harness con hooks y MCP"
- "Esa orquestación es justo lo que resuelve **LangGraph**: nodos, estado, aristas condicionales e `interrupt()`"
- "Me siento **cómodo adoptándolo**: los conceptos son los mismos que ya operé"
- Bonus: **langchain-mcp-adapters** carga servidores MCP como tools de LangGraph
- Ventaja de haberlo hecho a mano: **entiendes qué hace el framework por debajo**

> En producción orquesté el flujo directamente con el modelo, un harness con hooks y servidores MCP, sin framework de por medio. Esa orquestación es justo lo que resuelve LangGraph: cada paso es un nodo, el estado se guarda con un checkpointer y la aprobación humana es un interrupt. Me siento cómodo adoptándolo porque los conceptos son los mismos que ya operé, y además los servidores MCP que tengo se pueden cargar directamente como tools con langchain-mcp-adapters. Haberlo hecho a mano me ayuda a entender qué hace el framework por debajo y dónde falla.

---

## asyncio: la idea y los 6 conceptos
**Sección:** Python asíncrono
**Diagrama:** T13
- **Idea**: **muchas esperas a la vez en un solo hilo** · ideal para **I/O-bound** (LLM, APIs, BD, MCP), no para CPU pesada
- **1 · Event loop** (`asyncio.run`) · **2 · Coroutine** (`async def`) · **3 · `await`**: "mientras espero, atiende a otro"
- **4 · Task** (`create_task`) · **5 · `TaskGroup`** (cancela las demás si una falla) o `gather(return_exceptions=True)`
- **6 · Control**: **`Semaphore(n)`** para el rate limit · **`asyncio.timeout(s)`** · reintentos con `await asyncio.sleep(2 ** intento)`
- Resultado: 10 llamadas de 3 s → **~30 s en secuencia**, **~6 s** con Semaphore(5)

> asyncio permite que un solo hilo atienda muchas esperas al tiempo con un event loop. Es como un mesero que, mientras la cocina prepara un plato, atiende otra mesa. Una función async def es una corrutina, y await le dice al event loop "mientras espero, atiende a otro". Lanzo varias tasks en paralelo con un TaskGroup, que cancela las demás si una falla, y controlo con un Semaphore para no pasarme del rate limit del proveedor, timeouts y reintentos con backoff exponencial. Sirve para esperas de red, como llamar a un LLM, pero no para CPU pesada.

---

## asyncio: llamadas concurrentes al LLM, paso a paso
**Sección:** Python asíncrono
- **Un solo cliente**: `async with httpx.AsyncClient() as cliente` (o `AsyncAnthropic`), abierto una vez, en FastAPI en el **`lifespan`**
- **Paralelo**: `async with asyncio.TaskGroup() as tg:` → `tg.create_task(llamar_llm(cliente, p))`
- **Límite**: `async with sem:` con `sem = asyncio.Semaphore(5)`
- **Nunca colgado**: `async with asyncio.timeout(30):` → `await cliente.post(...)`
- **Reintento**: `except (httpx.HTTPError, TimeoutError):` → `await asyncio.sleep(2 ** intento)`

> En inglés: asyncio lets one thread handle many I/O waits concurrently through an event loop, which is perfect for LLM calls. For concurrent calls I use a TaskGroup, a Semaphore to respect the provider's rate limit, timeouts, and retries with exponential backoff. In FastAPI I never block inside an async def endpoint: I use async clients opened once in the lifespan, and asyncio.to_thread for anything blocking.

---

## P7 · "¿Experiencia con FastAPI y asyncio?" El flujo de una petición
**Sección:** Python asíncrono
**Diagrama:** T7
- **Pydantic** valida el body con `BaseModel` y genera el **schema** (también sirve para las tools del LLM)
- Endpoint `async def` · **`Depends`** para inyectar clientes y auth · **`lifespan`** para abrir y cerrar conexiones
- Llamadas en paralelo con **`asyncio.gather`** o **`TaskGroup`** (Python 3.11+)
- **`Semaphore`** para no pasar el rate limit del LLM · **`asyncio.timeout`** · reintentos con backoff
- **`StreamingResponse`** con **SSE** para mandar los tokens a medida que salen
- **[confirmar]** Abre diciendo dónde lo usaste: "**en el trabajo**" o "**en proyectos propios**", lo que sea cierto

> Una petición llega a FastAPI y Pydantic valida el body contra un BaseModel. Ese mismo modelo de Pydantic genera el JSON schema, que también sirve para definir las tools del LLM. El endpoint es async def, y con Depends inyecto los clientes y la autenticación. Los clientes se abren una sola vez en el lifespan. Si necesito el LLM, la búsqueda vectorial y una tool al tiempo, los lanzo en paralelo con asyncio.gather o TaskGroup, con un Semaphore para no pasarme del rate limit del proveedor, timeouts y reintentos con backoff. Para la experiencia de usuario, devuelvo StreamingResponse con SSE y los tokens van saliendo.

---

## P8 · "¿Errores comunes con asyncio?"
**Sección:** Python asíncrono
- **Bloquear el event loop**: `requests` o `time.sleep` dentro de `async def` → usar **`httpx.AsyncClient`**, **`asyncio.sleep`**
- Código que bloquea sí o sí → **`asyncio.to_thread`** o un worker aparte
- **`async def` vs `def`** en FastAPI: `def` corre en un threadpool; `async def` corre en el loop (no bloquear)
- **`gather` vs `TaskGroup`**: TaskGroup cancela todas las demás si una falla
- **I/O-bound** (LLM, red) = asyncio ✅ · **CPU-bound** (embeddings locales) = procesos o workers

> El error más común es bloquear el event loop: usar requests o time.sleep dentro de una función async, porque eso congela todas las demás peticiones. Se usa httpx.AsyncClient y asyncio.sleep, y si algo bloquea sí o sí, se manda a un hilo con asyncio.to_thread. En FastAPI, un endpoint def normal corre en un threadpool y uno async def corre en el event loop, así que en el async no puedes bloquear. TaskGroup es mejor que gather porque si una tarea falla, cancela las demás. Y asyncio sirve para trabajo de entrada y salida, como llamar a un LLM, pero no para CPU pesada.

---

## Pydantic: qué es y sus piezas
**Sección:** Python asíncrono
**Diagrama:** T14
- **Idea**: **validar y convertir datos usando los type hints de Python** · núcleo en **Rust** (pydantic-core), muy rápido
- **`BaseModel`** con tipos · **`Field(ge=0, le=1, min_length=1, description=...)`** · `Literal`, `Enum`, modelos anidados
- **`@field_validator`** (un campo) · **`@model_validator`** (varios campos) · **`ConfigDict(extra="forbid", strict=True)`**
- Entrar: **`model_validate`** / **`model_validate_json`** · salir: **`model_dump`** / **`model_dump_json`** · **`model_json_schema()`**
- Falla → **`ValidationError`** con `e.errors()` · configuración con **pydantic-settings** (`BaseSettings`)

> Pydantic valida y convierte datos a partir de los type hints de Python, y su núcleo está escrito en Rust, así que es muy rápido. Defino un BaseModel con tipos, uso Field para las reglas como rangos o longitudes, y validators cuando la regla es más compleja. Con extra forbid rechazo campos que no esperaba. Los datos entran con model_validate o model_validate_json, salen con model_dump, y model_json_schema genera el JSON schema. Si algo no cumple, lanza ValidationError con el detalle de cada error.

---

## P9 · "¿Cómo validas lo que devuelve el LLM?" Pydantic
**Sección:** Python asíncrono
- **Pydantic v2**: `BaseModel`, `Field`, `model_validate`, `model_json_schema`
- **Structured output**: le pides al LLM un JSON que cumpla un schema Pydantic → **validas** → si falla, **reintentas** con el error
- Las **tools** de MCP y de los frameworks se definen con **schemas** (muchas veces Pydantic)
- **pydantic-settings** para la configuración y los secretos desde variables de entorno
- En tu triage: el diagnóstico tenía **estructura fija** (certezas, incertidumbres, acción)

> Pydantic es la forma de no confiar ciegamente en lo que devuelve el modelo. Defino un BaseModel con los campos que espero, le pido al LLM una salida estructurada con ese schema, la valido con model_validate y, si falla, reintento pasándole el error al modelo. En el triage el diagnóstico tenía una estructura fija con certezas, incertidumbres y ruta de acción, que es exactamente ese patrón. Las tools también se describen con schemas, y Pydantic los genera con model_json_schema.

---

## P10 · "¿Cómo lideras discusiones con producto, UX, datos y backend?"
**Sección:** Colaboración
**Diagrama:** T8
- **Ejemplo real**: co-diseñé el **servidor MCP con el equipo de observabilidad** (otro equipo, otras prioridades)
- **Líder de proyectos**: coordiné alcance, tiempos, equipos y **áreas usuarias**
- **Producto**: aterrizar "IA" en **un problema + una métrica** + un nivel de riesgo aceptable
- **UX**: streaming, mensajes de error, **mostrar la incertidumbre** y el botón de aprobar
- **Datos y backend**: **contratos primero** (Pydantic / OpenAPI, Agent Card, tools MCP) · decisiones en un **ADR** (Architecture Decision Record)

> Un ejemplo real es el servidor MCP del triage, que co-diseñé con el equipo de observabilidad. Ellos eran dueños de los datos y yo necesitaba que el LLM los consultara de forma segura, así que acordamos primero el contrato: qué tools, qué datos y qué límites. También he sido líder de proyectos coordinando alcance, tiempos, equipos y áreas usuarias. Con producto, lo primero es convertir "queremos IA" en un problema concreto con una métrica. Con UX, definimos cómo se ve el streaming, cómo se muestra la incertidumbre y dónde aprueba la persona. Con datos y backend, contratos primero, y las decisiones quedan escritas en un ADR.

---

## P11 · "¿Cómo evalúas y operas los agentes?"
**Sección:** Operación
- **Golden dataset** + **LLM-as-a-judge** · en RAG: **faithfulness** y relevancia (ej.: **Ragas**)
- Evaluación **dentro del CI/CD**: si no pasa el umbral, **no se despliega**
- **Trazas** de cada paso del agente: **LangSmith**, **Langfuse** u **OpenTelemetry**
- Métricas: **latencia**, **costo por tarea**, tasa de éxito, tasa de **escalamiento a humano**
- Los casos malos de producción **alimentan el dataset** (ciclo de mejora)

> Armo un golden dataset con casos y respuestas esperadas, y uso un LLM como juez. En RAG mido si la respuesta es fiel al contexto y relevante, por ejemplo con Ragas. Esa evaluación corre en el CI/CD y bloquea el despliegue si baja la calidad, igual que una prueba. En producción trazo cada paso del agente con LangSmith, Langfuse u OpenTelemetry, y miro latencia, costo por tarea, tasa de éxito y cuántas veces escala a un humano. Los casos que salen mal se vuelven nuevos casos del dataset. Esa parte de operar con métricas es mi terreno como DevOps.

---

## Respuestas cortas en inglés (si la entrevista es en inglés)
**Sección:** Inglés
- **P1**: "I contributed to an **LLM-based incident triage system in production**, with Claude, MCP and **human approval** before any action."
- **P2**: "Yes, I've built **several MCP servers**; at MercadoLibre I **co-designed** one with the observability team."
- **P3**: "**MCP connects an agent to tools**; **A2A connects agents to other agents**. They're complementary."
- **P5**: "**Tiered autonomy**: reads are automatic, writes need approval, irreversible actions always need a human."
- **P6**: "I orchestrated it **directly with the model, a harness and MCP**. LangGraph solves the same problem and I'm **comfortable adopting it**."

> Si el entrevistador cambia a inglés, abre cada respuesta con estas frases y después desarrolla. Habla despacio y usa frases cortas. No pidas disculpas por tu inglés: es C1.

---

## Tus preguntas para el entrevistador técnico
**Sección:** Preguntas para él
- **1 ·** ¿Qué **framework de agentes** usan hoy (LangGraph, CrewAI, propio) y por qué lo eligieron?
- **2 ·** ¿Qué **proveedor de LLM** usan y si tienen un gateway con caché o fallback?
- **3 ·** ¿Ya tienen **servidores MCP** en producción, o eso sería parte del rol?
- **4 ·** ¿Cómo **evalúan** la calidad de los agentes antes de desplegar?
- **5 ·** ¿Qué tanta **autonomía** tienen los agentes y dónde hay aprobación humana?
- **6 ·** ¿Cómo es el **equipo** con el que trabajaría (producto, datos, backend)?

> Haz al menos tres. La 1 y la 3 te dicen cuánto encaja tu experiencia con MCP, y la 4 y la 5 muestran que piensas en producción, que es tu diferencial frente a otros candidatos de IA.

---

## Cierre: qué sí y qué no decir
**Sección:** Cierre
- ✅ "**En producción**", "**con aprobación humana**", "**co-diseñé el MCP**", "**varios servidores MCP**"
- ✅ "Lo orquesté a mano; **LangGraph** resuelve lo mismo y me siento **cómodo adoptándolo**"
- ❌ "Usé CrewAI / AutoGen / LlamaIndex / A2A en producción" (no lo hiciste)
- ❌ "Sistemas multiagente totalmente autónomos" → di "**autonomía por niveles**"
- Si no sabes algo: "**Lo más cercano que hice fue…**, y aquí lo resolvería con…"

> Tus cartas fuertes son producción, MCP real y control con humanos. Lo que te puede tumbar es afirmar un framework que no has usado y que te pidan código. Si te preguntan algo que no sabes, razona en voz alta desde lo que sí hiciste. Al final pregunta qué framework y qué proveedor de LLM usan, para mostrar interés.
