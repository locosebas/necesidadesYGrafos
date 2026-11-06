# Diagramas C4 - Llamada de filtro Metova Talent (AI Engineer)

Un diagrama C4 (Context, Containers, Components, Code) por idea de la llamada de filtro
([README.md](README.md)). Están en Mermaid, así que GitHub los dibuja directamente. Los usa el
[libreto](libreto-diapositivas.md) y el generador de la [presentación](presentacion.html).

Convenciones de color (las del modelo C4):

- **Azul oscuro**: persona.
- **Azul medio**: sistema propio.
- **Azul claro**: contenedor (servicio, base de datos, pipeline).
- **Gris**: sistema externo.
- **Recuadro punteado**: límite (empresa, sistema, etapa).

Íconos: cada `ico:nombre` es un logo guardado en [iconos/](iconos/) (sacados de
[Iconify](https://icon-sets.iconify.design/): sets `logos`, `mdi`, `devicon` y `simple-icons`).

Regla de honestidad para todos los diagramas: solo aparece lo que Sebastián hizo y puede defender.
LangChain y LangGraph aparecen **solo como el equivalente** de lo que él construyó, nunca como
herramientas que haya usado.

---

## D1 · Contexto: el puente DevOps → AI Engineer

Pitch "cuéntame de ti". Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Sebastián Díaz<br/>DevOps / Platform · ~5 años"]:::person
  subgraph biz["Bizagi · ene 2022 - jun 2024"]
    bz["ico:azuredevops ico:jenkins<br/>CI/CD + onboarding de Grafana<br/>+ APIs REST en Python"]:::system
  end
  subgraph meli["MercadoLibre · jun 2024 - ago 2026"]
    mp["ico:terraform-icon ico:kubernetes ico:aws-ecs<br/>Plataforma de Mercado Pago<br/>(línea de banca)"]:::system
    ia["ico:claude ico:robot<br/>IA en producción<br/>triage de tickets + alertas con LLM"]:::system
  end
  rol["ico:target<br/>Rol AI Engineer<br/>(cliente de Metova Talent)"]:::ext
  yo -->|"automatización<br/>y CI/CD"| bz
  yo -->|"IaC, observabilidad,<br/>on-call"| mp
  mp -->|"de ahí nace"| ia
  ia ==>|"lo que llevo<br/>al nuevo rol"| rol
  bz -.->|"base de ingeniería"| rol
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D2 · Contexto: triage automatizado de tickets con IA

Experiencia con LLM. Tipo: Contexto.

```mermaid
flowchart LR
  rep["ico:account-group<br/>Quien reporta<br/>el incidente"]:::person
  own["ico:account-tie<br/>Responsable del ticket<br/>(aprueba siempre)"]:::person
  tk["ico:ticket-outline<br/>Sistema de tickets"]:::ext
  tri["ico:robot<br/>Triage automatizado<br/>con IA"]:::system
  llm["ico:anthropic<br/>Claude (Anthropic)<br/>el modelo"]:::ext
  obs["ico:datadog ico:aws-cloudwatch<br/>Observabilidad (o11y)<br/>logs y métricas"]:::ext
  kb["ico:book-open-variant<br/>Runbooks +<br/>casos pasados"]:::ext
  rep -->|"abre ticket"| tk
  tk -->|"nuevo ticket"| tri
  tri -->|"prompt + contexto"| llm
  tri -->|"lee logs vía MCP"| obs
  tri -->|"recupera"| kb
  tri -->|"diagnóstico + ruta de acción"| own
  own -->|"aprueba / reenruta"| tk
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D3 · Dinámico: los 4 pasos del triage (human-in-the-loop)

Experiencia con LLM. Tipo: Dinámico.

```mermaid
flowchart TB
  t["ico:ticket-outline<br/>Llega un ticket"]:::ext
  p1["ico:graph-outline<br/>1 · Mapa de dependencias<br/>servicio que falla + blast radius"]:::container
  p2["ico:magnify-scan<br/>2 · Lee los logs de esa app<br/>y diagnostica con runbooks y casos pasados"]:::container
  p3["ico:clipboard-check<br/>3 · Diagnóstico digerido<br/>certezas · incertidumbres · ruta de acción"]:::container
  p4["ico:account-tie<br/>4 · Una persona revisa,<br/>resuelve dudas y aprueba"]:::person
  ok["ico:check-decagram<br/>Ejecutar la acción"]:::system
  re["ico:swap-horizontal<br/>Reenrutar a otro equipo"]:::system
  t --> p1 --> p2 --> p3 --> p4
  p4 -->|"aprueba"| ok
  p4 -->|"no es de aquí"| re
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D4 · Componentes: harness, hooks, MCP y base de conocimiento

Experiencia con LLM y agentes. Tipo: Componentes.

```mermaid
flowchart LR
  subgraph tri["Triage automatizado (por dentro)"]
    h["ico:robot<br/>Harness<br/>orquesta el flujo"]:::container
    hk["ico:hook ico:shield-check<br/>Hooks<br/>bloquean vulnerabilidades<br/>y acciones no deseadas"]:::container
    mcp["ico:swap-horizontal<br/>Servidor MCP<br/>co-diseñado con o11y"]:::container
    kb[("ico:book-open-variant<br/>Base de conocimiento<br/>runbooks + casos pasados")]:::container
    dep["ico:graph-outline<br/>Mapa de dependencias<br/>de aplicaciones"]:::container
  end
  llm["ico:anthropic<br/>Claude"]:::ext
  obs["ico:datadog<br/>Observabilidad"]:::ext
  h -->|"prompt"| llm
  llm -->|"pide herramienta"| hk
  hk -->|"si es segura"| mcp
  mcp -->|"consulta logs"| obs
  h -->|"recupera contexto<br/>(patrón RAG)"| kb
  h -->|"ubica servicio"| dep
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D5 · Contenedores: alertas de capacidad con capa predictiva y LLM

Experiencia con LLM (segundo ejemplo). Tipo: Contenedores.

```mermaid
flowchart LR
  m["ico:datadog ico:aws-cloudwatch<br/>Métricas de cómputo<br/>Datadog + CloudWatch"]:::ext
  subgraph al["Alertas de capacidad"]
    r["ico:alert<br/>Capa reactiva<br/>umbrales"]:::container
    pr["ico:history ico:chart-line<br/>Capa predictiva<br/>sobre el histórico"]:::container
    an["ico:claude<br/>Análisis con LLM<br/>explica y recomienda"]:::container
  end
  eq["ico:account-group<br/>Equipo dueño<br/>del servicio"]:::person
  m --> r
  m --> pr
  r -->|"sobre-aprovisionado<br/>o en riesgo"| an
  pr -->|"se va a quedar corto"| an
  an -->|"alerta con contexto<br/>y recomendación"| eq
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D6 · Dinámico: RAG (Retrieval-Augmented Generation) de punta a punta

Repaso técnico: RAG, embeddings y bases vectoriales. Tipo: Dinámico.

```mermaid
flowchart LR
  subgraph ing["Ingesta (una vez, y al actualizar)"]
    d["ico:file-document-multiple<br/>1 · Documentos"]:::ext
    c["ico:content-cut ico:file-document-multiple<br/>2 · Chunking<br/>pedazos con solapamiento"]:::container
    e["ico:vector-polyline<br/>3 · Modelo de embeddings<br/>texto → vector"]:::container
    v[("ico:database<br/>4 · Base vectorial<br/>pgvector / OpenSearch")]:::container
  end
  subgraph con["Consulta (cada pregunta)"]
    q["ico:account<br/>5 · Pregunta"]:::person
    qe["ico:vector-polyline<br/>6 · Embedding<br/>de la pregunta"]:::container
    k["ico:magnify-scan<br/>7 · Top-k parecidos<br/>búsqueda ANN"]:::container
    l["ico:brain<br/>8 · LLM con contexto<br/>responde y cita"]:::system
  end
  d --> c --> e --> v
  q --> qe --> k
  v -.->|"vecinos más cercanos"| k
  k --> l
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D7 · Componentes: anatomía de un agente (y su equivalente en LangGraph)

Repaso técnico: agentes, LangChain y LangGraph. Tipo: Componentes.

```mermaid
flowchart LR
  u["ico:account<br/>Tarea / objetivo"]:::person
  subgraph ag["Agente"]
    llm["ico:brain<br/>LLM decide<br/>el siguiente paso"]:::container
    tools["ico:swap-horizontal<br/>Herramientas<br/>tool calling / MCP"]:::container
    st[("ico:database<br/>Estado / memoria")]:::container
    g["ico:shield-check<br/>Guardarraíles<br/>+ aprobación humana"]:::container
  end
  lg["ico:langchain<br/>LangGraph<br/>nodos + aristas + estado"]:::ext
  out["ico:check-decagram<br/>Resultado"]:::system
  u --> llm
  llm -->|"pide acción"| g
  g -->|"permitida"| tools
  tools -->|"observación"| st
  st -->|"ciclo hasta terminar"| llm
  llm --> out
  ag -.->|"lo mismo, como framework"| lg
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D8 · Contenedores: LLMOps, donde pesa el perfil DevOps

Repaso técnico: evaluación de LLM y MLOps/LLMOps. Tipo: Contenedores.

```mermaid
flowchart LR
  dev["ico:account-group<br/>Equipo"]:::person
  subgraph ci["CI/CD (build once, deploy anywhere)"]
    pr["ico:source-pull<br/>Pull request<br/>prompt / código / modelo versionado"]:::container
    ev["ico:scale-balance<br/>Evaluación automática<br/>golden dataset + LLM-as-a-judge"]:::container
  end
  subgraph prod["Producción"]
    gw["ico:cached<br/>Gateway de LLM<br/>caché · fallback · límites"]:::container
    app["ico:robot<br/>App de IA<br/>RAG / agente"]:::container
  end
  obs["ico:datadog ico:chart-line<br/>Observabilidad<br/>latencia · costo por token · calidad"]:::ext
  dev --> pr --> ev
  ev -->|"pasa el umbral"| app
  ev -.->|"falla: no se despliega"| dev
  app --> gw
  app -.-> obs
  gw -.-> obs
  obs -.->|"casos malos → nuevo dataset"| ev
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D9 · Dinámico: cómo responder la pregunta del salario

Salario y modelo de contratación. Tipo: Dinámico.

```mermaid
flowchart TB
  q["ico:cash<br/>¿Cuál es tu expectativa?"]:::person
  r["ico:currency-usd<br/>USD 3.000 / mes en remoto<br/>+ ¿qué rango maneja el cliente?"]:::system
  rg{"¿Te dan un rango?"}
  den["ico:target<br/>Ubícate dentro del rango<br/>(si es más alto, súbete)"]:::container
  mon{"¿Moneda y contrato?"}
  usd["ico:currency-usd<br/>USD como contratista<br/>se mantiene 3.000"]:::container
  cop["ico:cash<br/>COP: convertir a la tasa del día<br/>¿fijo o indexado al dólar?"]:::container
  ps["ico:scale-balance<br/>Prestación de servicios vs laboral:<br/>pedir 25-35 % más que un laboral"]:::container
  q --> r --> rg
  rg -->|"sí"| den --> mon
  rg -->|"no"| mon
  mon --> usd
  mon --> cop
  mon --> ps
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D10 · Contexto: quién es quién en el proceso

Preguntas para la reclutadora. Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Sebastián<br/>candidato"]:::person
  rec["ico:phone<br/>Reclutadora<br/>Metova Talent (México)"]:::person
  subgraph proc["Proceso de selección"]
    f["ico:phone<br/>1 · Filtro<br/>(hoy, 30 min)"]:::container
    t["ico:help-circle<br/>2 · Técnica<br/>¿prueba? ¿con quién?"]:::container
    c["ico:handshake<br/>3 · Cliente final<br/>¿entrevista directa?"]:::container
    o["ico:clipboard-check<br/>4 · Oferta<br/>¿EOR, directo o servicios?"]:::container
  end
  cli["ico:account-tie<br/>Cliente final<br/>¿industria? ¿país? ¿stack?"]:::ext
  yo <-->|"llamada"| rec
  rec --> f --> t --> c --> o
  c --- cli
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```
