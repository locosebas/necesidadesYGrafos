# Glosario de IA para leer ofertas de empleo

Las ofertas de IA (AI Engineer, AI Platform, LLMOps, Agentic AI) usan muchas
siglas. Este glosario las explica en el orden en que aparecen dentro de un
sistema real, para que puedas leer una oferta y saber qué te están pidiendo.

Las siglas salieron de las vacantes de IA del
[tablero de postulaciones](https://claude.ai/artifact/1TA5UUU7Tq6bmW71Gp5XaE)
(Robots & Pencils, Grupo Mariposa, BC Tecnología, Niuro, Improving, Curotec,
Accelerant, Blupax y Lemon.io) y de las que se repiten en el mercado.

En la columna **Tú** se marca lo que ya has dicho que tienes:

- ✅ lo has usado en producción.
- 🟡 lo conoces o lo usaste en proyectos personales.
- ⬜ todavía no.

## 1. Panorama: las capas de un sistema de IA

Casi todas las ofertas describen alguna de estas capas. Si ubicas la sigla en
su capa, entiendes qué parte del sistema te piden.

```
  Usuario / negocio
        │
  [5] Aplicación y agentes ── agentes, herramientas (tool calling, MCP), flujos
        │
  [4] Recuperación de datos ── RAG: embeddings + base vectorial + búsqueda
        │
  [3] Modelo ───────────────── LLM vía API (OpenAI, Bedrock, Vertex) o propio
        │
  [2] Servir y operar ──────── inferencia, GPUs, despliegue, monitoreo (LLMOps)
        │
  [1] Plataforma ───────────── Kubernetes, nube, CI/CD, IaC (tu terreno fuerte)
        │
  Transversal: evaluación (evals), guardrails, seguridad, costos
```

Tu perfil es fuerte en la capa 1 y tiene experiencia real en la 3 y la 5:
llevaste a producción el triage de tickets con LLM y construiste servidores MCP.
Lo que más piden y menos tienes está en las capas 2 y 4 y en la evaluación.

## 2. Siglas generales

| Sigla | Significa | Qué es, en una línea | Tú |
|---|---|---|---|
| **AI / IA** | Artificial Intelligence | Sistemas que hacen tareas que normalmente requieren criterio humano. | — |
| **ML** | Machine Learning | Modelos que aprenden patrones de datos en lugar de reglas escritas a mano. | 🟡 |
| **DL** | Deep Learning | ML con redes neuronales de muchas capas; base de los LLM. | ⬜ |
| **GenAI** | Generative AI | IA que genera contenido nuevo: texto, imagen, código. | ✅ |
| **LLM** | Large Language Model | Modelo de lenguaje grande (GPT, Claude, Gemini, Llama) que recibe texto y produce texto. | ✅ |
| **SLM** | Small Language Model | Modelo de lenguaje pequeño, más barato y rápido, para tareas acotadas. | ⬜ |
| **NLP / PLN** | Natural Language Processing | Procesamiento de lenguaje natural: clasificar, extraer y resumir texto. | ✅ (triage) |
| **CV** | Computer Vision | Visión por computador: entender imágenes y video. *(En una oferta también puede significar currículum.)* | ⬜ |
| **OCR** | Optical Character Recognition | Sacar texto de imágenes o PDFs escaneados. | ⬜ |
| **ASR / STT** | Automatic Speech Recognition / Speech-to-Text | Voz a texto. | ⬜ |
| **TTS** | Text-to-Speech | Texto a voz. | ⬜ |
| **AGI** | Artificial General Intelligence | IA de capacidad general a nivel humano; concepto, no algo que pidan saber operar. | — |

## 3. El modelo: cómo se usa y se adapta (capa 3)

| Sigla o término | Significa | Qué es | Tú |
|---|---|---|---|
| **Prompt** / **prompt engineering** | — | Instrucción que se le da al modelo, y el oficio de escribirla bien. | ✅ |
| **Zero-shot / few-shot** | — | Pedirle algo al modelo sin ejemplos, o con unos pocos dentro del prompt. | ✅ |
| **CoT** | Chain of Thought | Hacer que el modelo razone paso a paso antes de responder. | 🟡 |
| **Token** | — | Unidad en que el modelo trocea el texto; se cobra y se limita por tokens. | ✅ |
| **Context window** | Ventana de contexto | Cuántos tokens puede leer el modelo de una vez. | ✅ |
| **Temperature** | — | Qué tan creativo o determinista responde el modelo (0 = más predecible). | ✅ |
| **Fine-tuning** | Ajuste fino | Re-entrenar un modelo con tus datos para especializarlo. | 🟡 conocido, no practicado |
| **SFT** | Supervised Fine-Tuning | Fine-tuning con pares pregunta → respuesta correcta. | ⬜ |
| **PEFT** | Parameter-Efficient Fine-Tuning | Familia de técnicas para ajustar el modelo tocando pocos parámetros. | ⬜ |
| **LoRA / QLoRA** | Low-Rank Adaptation / Quantized LoRA | La técnica PEFT más común; QLoRA la hace sobre un modelo cuantizado para usar menos GPU. | ⬜ |
| **RLHF** | Reinforcement Learning from Human Feedback | Entrenar con preferencias humanas; así se alinean los chatbots. | ⬜ |
| **DPO** | Direct Preference Optimization | Alternativa más simple a RLHF para entrenar con preferencias. | ⬜ |
| **Distillation** | Destilación | Entrenar un modelo pequeño para imitar a uno grande. | ⬜ |
| **Quantization** | Cuantización (INT8, INT4, GPTQ, AWQ) | Guardar los pesos con menos bits para que el modelo ocupe menos y corra más rápido. | ⬜ |
| **MoE** | Mixture of Experts | Arquitectura donde solo una parte del modelo se activa por token. | ⬜ |
| **Multimodal** | — | Modelo que entiende varios tipos de entrada (texto + imagen + audio). | ⬜ |
| **Hallucination** | Alucinación | Cuando el modelo inventa algo con seguridad. RAG y guardrails existen para reducirlo. | ✅ |

## 4. Recuperación de datos: RAG (capa 4)

| Sigla o término | Significa | Qué es | Tú |
|---|---|---|---|
| **RAG** | Retrieval-Augmented Generation | Buscar documentos relevantes y pasárselos al LLM para que responda con datos reales y no de memoria. | 🟡 proyecto propio |
| **Embedding** | — | Vector de números que representa el significado de un texto; textos parecidos quedan cerca. | 🟡 |
| **Vector DB** | Base de datos vectorial | Guarda embeddings y busca los más parecidos. Ejemplos: **pgvector** (PostgreSQL), **Pinecone**, **Qdrant**, **Weaviate**, **Milvus**, **OpenSearch**. | 🟡 |
| **ANN** | Approximate Nearest Neighbor | Búsqueda rápida de vectores cercanos, aproximada en vez de exacta. | ⬜ |
| **HNSW** | Hierarchical Navigable Small World | El índice ANN más usado en bases vectoriales. | ⬜ |
| **Chunking** | Fragmentación | Partir documentos en trozos antes de convertirlos en embeddings. | 🟡 |
| **Hybrid search** | Búsqueda híbrida | Combinar búsqueda por significado (vectores) con búsqueda por palabras (**BM25**). | ⬜ |
| **BM25** | Best Matching 25 | Algoritmo clásico de búsqueda por palabras clave. | ⬜ |
| **Reranker** | Re-ordenador | Segundo modelo que re-ordena los resultados para dejar arriba los más útiles. | ⬜ |
| **Knowledge graph / GraphRAG** | Grafo de conocimiento | RAG que usa relaciones entre entidades, no solo similitud de texto. | ⬜ |

## 5. Agentes y herramientas (capa 5)

| Sigla o término | Significa | Qué es | Tú |
|---|---|---|---|
| **Agent / Agentic AI** | Agente / IA agéntica | LLM que decide pasos, usa herramientas y actúa, no solo responde. | ✅ (triage) |
| **Tool calling / function calling** | Llamado de herramientas | El modelo pide ejecutar una función o API con argumentos estructurados (JSON). | ✅ |
| **MCP** | Model Context Protocol | Estándar abierto de Anthropic para exponer herramientas y datos a modelos mediante "servidores MCP". | ✅ construiste varios |
| **A2A** | Agent-to-Agent protocol | Protocolo de Google para que agentes de distintos sistemas se comuniquen. | ⬜ |
| **ReAct** | Reason + Act | Patrón donde el agente alterna pensar y usar herramientas. | 🟡 |
| **Multi-agent** | Multiagente | Varios agentes especializados que colaboran o se reparten tareas. | ⬜ |
| **HITL** | Human-in-the-Loop | Una persona aprueba o corrige antes de que el agente actúe. | ✅ (escalamiento del triage) |
| **Memory / state** | Memoria / estado | Cómo el agente recuerda la conversación o el progreso entre pasos. | 🟡 |
| **Orchestration** | Orquestación | Coordinar pasos, agentes y herramientas en un flujo. | 🟡 |

**Frameworks de agentes que aparecen por nombre en las ofertas:**
**LangChain** y **LangGraph** (🟡 proyectos personales), **CrewAI**, **AutoGen**
(Microsoft), **Semantic Kernel** (Microsoft, .NET/Python), **LlamaIndex**
(centrado en RAG), **DSPy** (optimiza prompts de forma programática) y
**ADK** (Agent Development Kit, de Google).

## 6. Servir y operar modelos: LLMOps (capa 2)

| Sigla o término | Significa | Qué es | Tú |
|---|---|---|---|
| **MLOps** | ML Operations | DevOps aplicado a modelos: versionar, entrenar, desplegar y monitorear. | 🟡 proyectos personales |
| **LLMOps** | LLM Operations | Lo mismo para LLMs: prompts versionados, evals, costos y trazas. | 🟡 |
| **Inference** | Inferencia | Usar el modelo ya entrenado para responder; es lo que corre en producción. | ✅ vía API |
| **Model serving** | Servir modelos | Exponer un modelo como API. Herramientas: **vLLM**, **TGI**, **Triton**, **KServe**, **Ray Serve**, **BentoML**. | 🟡 (Helm charts de serving) |
| **vLLM** | — | Servidor de inferencia de LLM muy usado, rápido gracias a PagedAttention. | ⬜ |
| **TGI** | Text Generation Inference | Servidor de inferencia de Hugging Face. | ⬜ |
| **Triton** | NVIDIA Triton Inference Server | Servidor de inferencia de NVIDIA para muchos tipos de modelos. | ⬜ |
| **KServe** | — | Serving de modelos sobre Kubernetes (antes KFServing). | ⬜ |
| **ONNX** | Open Neural Network Exchange | Formato estándar para mover modelos entre frameworks. | ⬜ |
| **TensorRT** | — | Optimizador de NVIDIA para acelerar inferencia en GPU. | ⬜ |
| **GPU / TPU** | Graphics / Tensor Processing Unit | Hardware para entrenar e inferir; TPU es el chip de Google. | ⬜ |
| **CUDA** | Compute Unified Device Architecture | Plataforma de NVIDIA para programar GPUs; aparece como "drivers CUDA en Kubernetes". | ⬜ |
| **KV cache** | Key-Value cache | Memoria que reutiliza cálculos de tokens previos; clave para la latencia y la memoria de GPU. | ⬜ |
| **TTFT** | Time To First Token | Cuánto tarda en salir el primer token; métrica de latencia percibida. | ⬜ |
| **TPS / tokens/s** | Tokens per second | Velocidad de generación. | ⬜ |
| **Batching** | Procesamiento por lotes | Agrupar peticiones para aprovechar la GPU. | ⬜ |
| **Model registry** | Registro de modelos | Catálogo de versiones de modelos (p. ej. **MLflow**). | ⬜ |
| **MLflow** | — | Plataforma para registrar experimentos, métricas y modelos. | ⬜ |
| **Kubeflow** | — | Pipelines de ML sobre Kubernetes. | ⬜ |
| **Feature store** | Almacén de features | Base de datos de variables preparadas para entrenar y servir modelos. | ⬜ |
| **Drift** | Deriva | Cuando los datos o el comportamiento del modelo cambian con el tiempo y empeora. | ⬜ |
| **CI/CD for models** | — | Pipelines que prueban y despliegan modelos o prompts como si fueran código. | 🟡 (CI/CD fuerte; en modelos, poco) |

## 7. Evaluación, seguridad y costos (transversal)

| Sigla o término | Significa | Qué es | Tú |
|---|---|---|---|
| **Evals** | Evaluaciones | Conjuntos de pruebas que miden si el sistema de IA responde bien; son los "tests" de la IA. | 🟡 conocido, no practicado |
| **LLM-as-a-judge** | LLM como juez | Usar un modelo para calificar las respuestas de otro. | ⬜ |
| **Golden dataset** | Conjunto de referencia | Preguntas con respuesta correcta conocida, usadas para evaluar. | ⬜ |
| **Guardrails** | Barandas | Validaciones de entrada y salida, límites de acción y escalamiento a humano. | ✅ (triage) |
| **Prompt injection** | Inyección de prompt | Ataque donde el texto de entrada intenta cambiar las instrucciones del modelo. | 🟡 |
| **Jailbreak** | — | Intentar que el modelo se salte sus restricciones. | 🟡 |
| **PII** | Personally Identifiable Information | Datos personales que hay que proteger o enmascarar antes de enviarlos a un modelo. | 🟡 (entornos regulados, sin detalle de LLM) |
| **Red teaming** | — | Atacar tu propio sistema para encontrar fallas antes que otros. | ⬜ |
| **Observability (LLM)** | Observabilidad de LLM | Trazas de prompts, respuestas, costos y latencias. Herramientas: **LangSmith**, **Langfuse**, **Arize**, **Helicone**. | 🟡 (observabilidad fuerte; de LLM, poca) |
| **FinOps / token cost** | — | Controlar el costo por token y por petición. | 🟡 |

## 8. Plataformas de nube para IA (por nombre)

| Nombre | De quién | Qué es | Tú |
|---|---|---|---|
| **Amazon Bedrock** | AWS | Acceso a LLMs (Claude, Llama, Titan) por API, con agentes y bases de conocimiento. | ⬜ |
| **SageMaker** | AWS | Plataforma para entrenar, desplegar y monitorear modelos. | ⬜ |
| **Vertex AI** | Google Cloud | Plataforma de ML y LLM de Google (Gemini, model garden, pipelines). | 🟡 |
| **Vertex AI Agent Builder** | Google Cloud | Herramienta de Google para construir agentes y búsqueda con RAG. | 🟡 |
| **Azure OpenAI (AOAI)** | Microsoft | Modelos de OpenAI servidos dentro de Azure. | ⬜ |
| **Azure AI Foundry** | Microsoft | Portal de Azure para construir, evaluar y desplegar apps y agentes de IA (antes Azure AI Studio). | ⬜ |
| **Copilot Studio / Power Platform** | Microsoft | Herramientas low-code para bots y automatizaciones de negocio. | ⬜ |
| **Azure Logic Apps** | Microsoft | Flujos de integración sin servidor. | 🟡 solo Logic Apps |
| **Hugging Face** | — | El "GitHub de los modelos": repositorio de modelos y datasets abiertos. | ⬜ |
| **OpenAI API / Anthropic API** | — | Acceso directo a GPT o Claude por API. | ✅ |

## 9. Orden sugerido de estudio

Según lo que más repiten las ofertas a las que aplicaste y lo que te falta:

1. **Evals y LLM-as-a-judge.** Lo piden casi todas las ofertas senior de IA y es lo que convierte tu triage en "IA confiable en producción".
2. **RAG completo:** chunking, embeddings, pgvector o Qdrant, búsqueda híbrida y reranker. Ya tienes la base del proyecto propio.
3. **Model serving en Kubernetes:** vLLM, KServe, GPUs, KV cache, TTFT. Encaja con tu fuerte en plataforma, y por ahí es como más rápido se vende tu perfil de DevOps a IA.
4. **Fine-tuning ligero:** LoRA/QLoRA y cuándo NO hacer fine-tuning (casi siempre RAG basta).
5. **Observabilidad de LLM:** Langfuse o LangSmith, y costos por token.
6. **Plataformas:** Amazon Bedrock y Azure AI Foundry; ya tienes AWS y Azure, así que es sumar el servicio.
