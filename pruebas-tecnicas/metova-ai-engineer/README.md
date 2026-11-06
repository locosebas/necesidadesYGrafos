# Llamada de filtro - Metova Talent: AI Engineer

Llamada inicial de 30 minutos con una reclutadora de **Metova Talent** (empresa de reclutamiento con
sede en México), 6 nov 2026. Vacante: **AI Engineer**. Es el filtro de recursos humanos, no la
entrevista técnica.

## Material de estudio

- [diagramas-c4.md](diagramas-c4.md): 10 diagramas C4 (pitch, triage con IA, alertas con LLM, RAG,
  agentes, LLMOps, salario y proceso).
- [libreto-diapositivas.md](libreto-diapositivas.md): plan de las 18 diapositivas con el guion de cada una
  (pitch en español e inglés, preguntas de filtro con su respuesta, repaso técnico y preguntas para la
  reclutadora).
- [presentacion.html](presentacion.html): la presentación (← → para navegar, **N** para el guion).
  Versión para el celular (privada): https://claude.ai/artifact/8WP7sLxViPGcSpHWphsfQq
  Se regenera con `python3 generar_presentacion.py` (mismo generador que [niuro-aws](../niuro-aws/)).

## Regla de oro

Solo afirmar lo que se puede defender en la técnica: "participé", "trabajé en", "en producción",
"siempre con aprobación humana". No decir que usó LangChain o LangGraph ni que construyó agentes
autónomos: se da el ejemplo real más cercano (harness + hooks + MCP + base de conocimiento) y se dice
"me siento cómodo adoptándolo".

## Pendiente de confirmar por Sebastián

- **Por qué salió de MercadoLibre**: el libreto trae una frase neutra ("mi ciclo terminó en agosto y
  aproveché para enfocar mi carrera en IA aplicada"). Hay que ajustarla al motivo real.

## Nombres clave para repasar

RAG (Retrieval-Augmented Generation) · chunking · embeddings · similitud coseno · base vectorial
(pgvector, OpenSearch, Pinecone, Weaviate) · ANN / HNSW · búsqueda híbrida (BM25) · tool calling ·
MCP (Model Context Protocol) · LangChain · LangGraph · human-in-the-loop · guardarraíles ·
golden dataset · LLM-as-a-judge · faithfulness · Ragas · LLMOps · caché y fallback de modelos ·
EOR (Employer of Record).

## Entrevista técnica (6 nov 2026)

Habilidades evaluadas: frameworks de agentes (LangChain, LlamaIndex, AutoGen, CrewAI), Python con
FastAPI, asyncio y Pydantic, liderar discusiones con producto, UX, datos y backend, arquitectura con
agentes y LLM, y MCP + A2A (Agent-to-Agent) para coordinar varios agentes.

- [tecnica/diagramas-c4.md](tecnica/diagramas-c4.md): 16 diagramas C4 (T1 a T16).
- [tecnica/libreto-diapositivas.md](tecnica/libreto-diapositivas.md): 36 diapositivas: plan de 30 min, serie P1-P11, inglés y preguntas para el entrevistador.
- [tecnica/presentacion.html](tecnica/presentacion.html), versión para el celular (privada):
  https://claude.ai/artifact/1zFmgSAGf8qk7NZgqeowUR · se regenera con
  `python3 tecnica/generar_presentacion.py`.
