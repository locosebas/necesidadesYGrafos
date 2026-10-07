# RAG (Retrieval-Augmented Generation) y bases de datos vectoriales

**RAG** es el patrón más pedido en ofertas de IA aplicada: darle al LLM
información propia (documentos de la empresa) sin reentrenarlo. Se conecta
directo con el tema 06 (datos): una **base de datos vectorial** es otra base
de datos más que hay que desplegar, asegurar y operar.

## Objetivos

- Explicar el flujo RAG completo: **ingesta → chunking → embeddings →
  indexación → retrieval → generación**.
- Elegir estrategia de **chunking** (tamaño, overlap, por estructura del documento).
- Entender **búsqueda vectorial** (similitud coseno, índices **HNSW**) y
  **búsqueda híbrida** (vectorial + keyword/BM25) con **reranking**.
- Elegir base vectorial: servicio gestionado vs. **pgvector** en Postgres vs.
  una base dedicada.
- Evaluar un RAG: ¿recupera los documentos correctos? ¿la respuesta es fiel
  a esos documentos (groundedness)?

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| RAG gestionado "end-to-end" | Azure AI Foundry + "On Your Data" | **Bedrock Knowledge Bases** | **Vertex AI RAG Engine** / Vertex AI Search |
| Búsqueda vectorial / híbrida | **Azure AI Search** | **OpenSearch Serverless** (vector), S3 Vectors | **Vertex AI Vector Search** |
| Vectores en tu base existente | Cosmos DB (vector search), Azure Database for PostgreSQL + **pgvector** | Aurora/RDS PostgreSQL + **pgvector** | AlloyDB / Cloud SQL + **pgvector** |
| Modelo de embeddings | text-embedding-3 (Azure OpenAI) | Amazon Titan Embeddings / Cohere Embed | Vertex AI text embeddings / Gemini embeddings |

## Subtemas

1. Pipeline de ingesta: extracción de texto (PDF, HTML), limpieza, chunking
2. Embeddings: elección de modelo, dimensiones, costo
3. Índices vectoriales: HNSW, similitud coseno, filtros por metadata
4. Búsqueda híbrida + **reranking**
5. Prompt de generación con citas a las fuentes
6. Evaluación de RAG: retrieval (recall@k) y generación (groundedness) — herramientas como **Ragas**
7. Seguridad: que cada usuario solo recupere documentos que tiene permiso de ver (filtros por ACL)

## Recursos

- Azure AI Search — RAG overview: https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview
- Amazon Bedrock Knowledge Bases: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- Vertex AI RAG Engine: https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview
- pgvector: https://github.com/pgvector/pgvector

## Lab sugerido

RAG mínimo con **pgvector** en un Postgres en Docker: ingestá 20 documentos
(por ejemplo, los README de este repo), indexalos y armá un endpoint FastAPI
`/preguntar` que responda citando las fuentes. Después repetilo con el
servicio gestionado de una nube (Bedrock Knowledge Bases o Azure AI Search) y
compará esfuerzo y costo.

## Autoevaluación

Pedime: *"Dame un examen de RAG y bases vectoriales nivel intermedio"*.
