# Diagramas C4 - Entrevista técnica Metova Talent (AI Engineer)

Diagramas C4 (Context, Containers, Components, Code) para la entrevista técnica del 6 nov 2026. Están
en Mermaid. Los usa el [libreto](libreto-diapositivas.md) y el generador de la
[presentación](presentacion.html). Los íconos están en [../iconos/](../iconos/).

Colores C4: **azul oscuro** = persona, **azul medio** = sistema propio, **azul claro** = contenedor,
**gris** = sistema externo, **punteado** = límite.

Regla de honestidad: LangChain, LangGraph, LlamaIndex, AutoGen, CrewAI y A2A (Agent-to-Agent)
aparecen como **conceptos que conoces y su equivalente en lo que construiste**, no como herramientas
que hayas usado en producción. Lo que sí hiciste: LLM (Claude) en producción con harness, hooks,
servidores MCP (Model Context Protocol), base de conocimiento (patrón RAG) y aprobación humana.

---

## T1 · Contexto: las 5 habilidades contra tu experiencia real

Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Sebastián Díaz"]:::person
  subgraph real["Lo que hiciste (defendible)"]
    tri["ico:claude ico:robot<br/>Triage con LLM en producción<br/>harness + hooks + HITL"]:::system
    mcp["ico:swap-horizontal<br/>Varios servidores MCP<br/>uno co-diseñado con o11y"]:::system
    py["ico:python<br/>Python 5 años<br/>APIs REST, automatización"]:::system
    lid["ico:account-group<br/>Líder de proyectos<br/>alcance, tiempos, equipos"]:::system
  end
  subgraph pide["Lo que pide el rol"]
    fw["ico:langchain ico:crewai<br/>Frameworks de agentes"]:::ext
    fa["ico:fastapi-icon ico:pydantic<br/>FastAPI · asyncio · Pydantic"]:::ext
    a2a["ico:lan-connect<br/>MCP + A2A<br/>multiagente"]:::ext
    col["ico:account-voice<br/>Liderar discusiones<br/>producto, UX, datos, backend"]:::ext
  end
  yo --> tri
  yo --> mcp
  yo --> py
  yo --> lid
  tri -.->|"mismo patrón:<br/>orquestación + herramientas"| fw
  py -.->|"misma base"| fa
  mcp ==>|"directo"| a2a
  lid -.->|"co-diseño con o11y"| col
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T2 · Componentes: arquitectura de MCP (Model Context Protocol)

Tipo: Componentes.

```mermaid
flowchart LR
  subgraph host["Host (la app de IA: Claude Desktop, IDE, tu agente)"]
    llm["ico:brain<br/>LLM"]:::container
    c1["ico:lan-connect<br/>Cliente MCP 1"]:::container
    c2["ico:lan-connect<br/>Cliente MCP 2"]:::container
  end
  s1["ico:swap-horizontal<br/>Servidor MCP local<br/>transporte stdio"]:::system
  s2["ico:swap-horizontal ico:lock<br/>Servidor MCP remoto<br/>Streamable HTTP + OAuth 2.1"]:::system
  obs["ico:datadog<br/>Observabilidad"]:::ext
  db[("ico:database<br/>Base de datos")]:::ext
  llm --> c1
  llm --> c2
  c1 <-->|"JSON-RPC 2.0<br/>1 a 1"| s1
  c2 <-->|"JSON-RPC 2.0<br/>1 a 1"| s2
  s1 -->|"tools · resources · prompts"| db
  s2 -->|"tools · resources · prompts"| obs
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T3 · Dinámico: una tarea con A2A (Agent-to-Agent)

Tipo: Dinámico.

```mermaid
flowchart TB
  a["ico:robot<br/>Agente cliente<br/>(orquestador)"]:::system
  card["ico:card-account-details<br/>1 · Descubre la Agent Card<br/>JSON en /.well-known/: skills, URL, auth"]:::container
  send["ico:code-json<br/>2 · Envía un mensaje / tarea<br/>JSON-RPC 2.0 sobre HTTPS"]:::container
  st["ico:timer-sand<br/>3 · Estados de la tarea<br/>submitted → working → input-required → completed / failed / canceled"]:::container
  sse["ico:flash<br/>4 · Avances por streaming (SSE)<br/>o push notification (webhook)"]:::container
  art["ico:file-document-multiple<br/>5 · Artifacts: el resultado<br/>parts de texto, archivo o datos"]:::container
  b["ico:robot<br/>Agente remoto<br/>(opaco: no comparte memoria ni tools)"]:::ext
  a --> card --> send --> b
  b --> st --> sse --> art --> a
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T4 · Contenedores: arquitectura multiagente de referencia para un negocio

Tipo: Contenedores.

```mermaid
flowchart LR
  u["ico:account-group<br/>Usuario / sistema de negocio"]:::person
  subgraph plat["Plataforma de agentes (Kubernetes)"]
    api["ico:fastapi-icon ico:pydantic<br/>API FastAPI<br/>valida con Pydantic, streaming SSE"]:::container
    sup["ico:sitemap<br/>Agente supervisor<br/>LangGraph: estado + checkpoints"]:::container
    g["ico:shield-check<br/>Guardarraíles<br/>políticas, límites, PII"]:::container
    a1["ico:robot<br/>Agente A<br/>(misma plataforma)"]:::container
    st[("ico:database<br/>Estado y memoria<br/>Postgres / Redis")]:::container
    vec[("ico:vector-polyline<br/>Base vectorial<br/>RAG")]:::container
  end
  a2["ico:robot<br/>Agente de otro equipo<br/>vía A2A"]:::ext
  tools["ico:swap-horizontal<br/>Servidores MCP<br/>CRM, tickets, ERP"]:::ext
  hitl["ico:account-tie<br/>Aprobación humana"]:::person
  o11y["ico:datadog ico:chart-line<br/>Trazas, costo, evaluación"]:::ext
  u --> api --> sup
  sup --> g
  g --> a1
  g -->|"A2A"| a2
  a1 -->|"MCP"| tools
  sup --> st
  a1 --> vec
  sup -.->|"acciones de riesgo"| hitl
  sup -.-> o11y
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T5 · Componentes: los 4 frameworks y su idea central

Tipo: Componentes.

```mermaid
flowchart TB
  subgraph lc["LangChain + LangGraph"]
    lc1["ico:langchain<br/>LangChain: modelos, prompts,<br/>tools, retrievers (LCEL)"]:::container
    lc2["ico:sitemap<br/>LangGraph: StateGraph<br/>nodos, aristas, checkpointer, interrupt"]:::container
  end
  subgraph li["LlamaIndex"]
    li1["ico:file-document-multiple<br/>Documents → Nodes → Index<br/>retriever, query engine"]:::container
    li2["ico:flash<br/>Workflows y agentes<br/>por eventos"]:::container
  end
  subgraph ag["AutoGen (Microsoft)"]
    ag1["ico:microsoft-icon<br/>Agentes que conversan<br/>AssistantAgent, group chat"]:::container
  end
  subgraph cr["CrewAI"]
    cr1["ico:crewai<br/>Agent: role · goal · backstory<br/>Task · Crew · Process"]:::container
  end
  lc1 --> lc2
  li1 --> li2
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T6 · Dinámico: tu triage traducido a un grafo de LangGraph

Tipo: Dinámico.

```mermaid
flowchart LR
  s(["START"])
  n1["ico:graph-outline<br/>nodo: mapear_dependencias"]:::container
  n2["ico:magnify-scan<br/>nodo: leer_logs<br/>(tool MCP)"]:::container
  n3["ico:book-open-variant<br/>nodo: recuperar_casos<br/>(RAG)"]:::container
  n4["ico:clipboard-check<br/>nodo: diagnosticar<br/>certezas / incertidumbres"]:::container
  h["ico:account-tie<br/>interrupt()<br/>aprobación humana"]:::person
  ok["ico:check-decagram<br/>nodo: ejecutar"]:::system
  re["ico:swap-horizontal<br/>nodo: reenrutar"]:::system
  e(["END"])
  s --> n1 --> n2 --> n3 --> n4 --> h
  h -->|"arista condicional:<br/>aprueba"| ok --> e
  h -->|"otro equipo"| re --> e
  n4 -.->|"faltan datos:<br/>ciclo"| n2
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T7 · Dinámico: una petición asíncrona en FastAPI

Tipo: Dinámico.

```mermaid
flowchart LR
  r["ico:web<br/>1 · Request HTTP"]:::person
  v["ico:pydantic<br/>2 · Pydantic valida<br/>el body (BaseModel)"]:::container
  ep["ico:fastapi-icon<br/>3 · async def endpoint<br/>Depends: clientes, auth"]:::container
  subgraph par["4 · En paralelo (asyncio.gather / TaskGroup)"]
    t1["ico:brain<br/>llamada al LLM"]:::container
    t2["ico:vector-polyline<br/>búsqueda vectorial"]:::container
    t3["ico:swap-horizontal<br/>tool MCP"]:::container
  end
  lim["ico:timer-sand<br/>Semaphore + timeout<br/>+ reintentos con backoff"]:::container
  out["ico:code-json<br/>5 · Respuesta Pydantic<br/>o StreamingResponse (SSE)"]:::system
  r --> v --> ep --> lim
  lim --> t1
  lim --> t2
  lim --> t3
  t1 --> out
  t2 --> out
  t3 --> out
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T8 · Contexto: cómo lideras la discusión técnica entre equipos

Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Tú<br/>(AI Engineer)"]:::person
  prod["ico:target<br/>Producto<br/>qué problema, qué métrica"]:::ext
  ux["ico:pencil-ruler<br/>UX<br/>streaming, errores, HITL visible"]:::ext
  data["ico:database<br/>Datos<br/>fuentes, calidad, permisos"]:::ext
  be["ico:code-json<br/>Backend<br/>contratos API, MCP, A2A"]:::ext
  adr["ico:file-document-multiple<br/>ADR + contratos Pydantic/OpenAPI<br/>+ criterios de evaluación"]:::system
  yo -->|"talleres de descubrimiento"| prod
  yo --> ux
  yo --> data
  yo --> be
  prod --> adr
  ux --> adr
  data --> adr
  be --> adr
  adr -->|"decisión escrita"| yo
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T9 · Componentes: LangChain, las piezas y cómo se encadenan (LCEL)

Tipo: Componentes.

```mermaid
flowchart LR
  in["ico:code-json<br/>Entrada<br/>{ticket: ...}"]:::person
  subgraph lc["Cadena LCEL: prompt | modelo | parser"]
    p["ico:file-document-multiple<br/>ChatPromptTemplate<br/>plantilla con variables"]:::container
    m["ico:anthropic<br/>Chat model<br/>ChatAnthropic / ChatOpenAI"]:::container
    o["ico:pydantic<br/>with_structured_output<br/>objeto Pydantic validado"]:::container
  end
  t["ico:swap-horizontal<br/>Tools<br/>@tool · bind_tools · MCP adapters"]:::ext
  r[("ico:vector-polyline<br/>Retriever + vector store<br/>RAG")]:::ext
  in --> p --> m --> o
  m -.->|"pide tool"| t
  r -.->|"contexto"| p
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T10 · Dinámico: LlamaIndex, de documentos a respuestas

Tipo: Dinámico.

```mermaid
flowchart LR
  subgraph ing["Ingesta (IngestionPipeline)"]
    rd["ico:file-document-multiple<br/>1 · Readers<br/>SimpleDirectoryReader, LlamaHub, LlamaParse"]:::container
    np["ico:content-cut<br/>2 · Node parser<br/>Documents → Nodes"]:::container
    ix[("ico:vector-polyline<br/>3 · VectorStoreIndex<br/>embeddings en pgvector, etc.")]:::container
  end
  subgraph q["Consulta"]
    rt["ico:magnify-scan<br/>4 · Retriever<br/>top-k + reranker"]:::container
    qe["ico:brain<br/>5 · Query engine<br/>sintetiza la respuesta"]:::system
    ag["ico:robot<br/>Agentes y Workflows<br/>FunctionAgent · @step por eventos"]:::system
  end
  rd --> np --> ix --> rt --> qe
  qe -.->|"como tool"| ag
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T11 · Componentes: CrewAI, un equipo de agentes por roles

Tipo: Componentes.

```mermaid
flowchart LR
  in["ico:account<br/>crew.kickoff(inputs)"]:::person
  subgraph crew["Crew (process = sequential o hierarchical)"]
    mg["ico:account-tie<br/>Manager<br/>solo en hierarchical"]:::container
    a1["ico:robot<br/>Agent: Analista<br/>role · goal · backstory · tools"]:::container
    a2["ico:robot<br/>Agent: Redactor<br/>role · goal · backstory"]:::container
    t1["ico:clipboard-check<br/>Task 1<br/>description · expected_output"]:::container
    t2["ico:clipboard-check<br/>Task 2<br/>context=[Task 1] · human_input"]:::container
  end
  out["ico:check-decagram<br/>Resultado<br/>output_pydantic"]:::system
  in --> t1
  t1 -->|"lo hace"| a1
  t1 --> t2
  t2 -->|"lo hace"| a2
  mg -.->|"delega"| a1
  mg -.->|"delega"| a2
  t2 --> out
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## T12 · Dinámico: AutoGen, agentes que conversan en equipo

Tipo: Dinámico.

```mermaid
flowchart LR
  task["ico:account<br/>team.run(task)"]:::person
  subgraph team["Team (RoundRobin / Selector / Swarm)"]
    d["ico:robot<br/>AssistantAgent<br/>diagnosticador + tools"]:::container
    r["ico:robot<br/>AssistantAgent<br/>revisor"]:::container
    u["ico:account-tie<br/>UserProxyAgent<br/>la persona"]:::person
  end
  term["ico:timer-sand<br/>Termination<br/>TextMention('APPROVE') · MaxMessage"]:::container
  core["ico:microsoft-icon<br/>AutoGen Core<br/>actores asíncronos por mensajes"]:::ext
  task --> d
  d -->|"turno"| r
  r -->|"turno"| u
  u -->|"turno"| d
  r -.-> term
  team -.->|"corre sobre"| core
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```
