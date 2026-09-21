# Infraestructura para IA / MLOps: servir y operar modelos en producción

Tema opcional y complementario a los 13 temas core (ver `certificaciones/README.md`
→ sección "Ruta IA / MLOps"). Cada vez más ofertas de DevOps/Platform piden
desplegar y operar cargas de IA (APIs de modelos, RAG, GPUs) — es una
extensión natural de lo que ya tienes: contenedores serverless (tema 02),
FastAPI (tema 08), identidad (tema 04), secretos (tema 06) y observabilidad
(tema 07).

## Objetivos

- Diferenciar tres capas de infraestructura de IA: (1) modelos como servicio
  administrado (Azure OpenAI, Bedrock, Vertex AI) sin gestionar cómputo
  propio, (2) model serving propio sobre contenedores serverless o
  Kubernetes (cuando el modelo es propio o necesita GPU dedicada), (3)
  pipelines de entrenamiento/MLOps (fuera del foco DevOps puro, solo de
  referencia).
- Explicar cuándo conviene Kubernetes para IA (control total, GPU sharing,
  cargas de inferencia de alto volumen) vs. cuándo conviene serverless o un
  servicio administrado (equipos chicos, tráfico variable, no operar GPU
  node pools).
- Diseñar una API de inferencia con FastAPI que llama a un modelo
  administrado (RAG básico: retrieval + prompt + LLM).
- Manejar el vocabulario mínimo: LLM, embeddings, RAG, vector database,
  prompt, token, fine-tuning vs. prompt engineering, inference vs. training.

## Kubernetes: ¿aplica o no?

Depende de la capa:

- **No aplica** si consumes un modelo ya alojado (Azure OpenAI, Bedrock,
  Vertex AI) desde una API propia — ahí Kubernetes ni siquiera entra en la
  conversación, solo necesitas dónde correr tu API (Container Apps/Fargate/
  Cloud Run alcanza, tema 02).
- **Sí aplica** cuando alojas el modelo tú mismo (open-weights, ej. Llama,
  Mistral) y necesitas GPU dedicada: ahí Kubernetes gestiona GPU node
  pools, autoscaling de pods con GPU, y proyectos como KServe/Kubeflow/
  KubeRay orquestan el ciclo de vida del modelo sobre K8s. Esto es una
  extensión de lo que ya sabes de Kubernetes (tema 10), no un tema nuevo
  desde cero.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Modelos como servicio administrado | Azure OpenAI Service / Azure AI Foundry | Amazon Bedrock | Vertex AI (Model Garden) |
| Plataforma end-to-end de ML | Azure Machine Learning | Amazon SageMaker | Vertex AI |
| Vector database gestionada | Azure AI Search (vector search) | Amazon OpenSearch (vector engine) / Aurora pgvector | Vertex AI Vector Search / AlloyDB pgvector |
| GPU en Kubernetes gestionado | AKS con node pools GPU (series NC/ND) | EKS con node groups GPU (series P/G) | GKE con node pools GPU (Autopilot soporta GPU) |
| Serving de modelo propio sobre K8s | KServe / Kubeflow sobre AKS | KServe / Kubeflow sobre EKS, o SageMaker on EKS | KServe / Kubeflow sobre GKE, o Vertex AI Prediction |

## Subtemas

1. Consumir un modelo administrado desde FastAPI (Azure OpenAI / Bedrock /
   Vertex AI) — autenticación con identidad gestionada, no API keys sueltas
   (conecta con el tema 04)
2. RAG básico: vector database + embeddings + retrieval antes de armar el
   prompt para el LLM
3. Cuándo servir un modelo propio: GPU node pools en AKS/EKS/GKE,
   autoscaling basado en cola de requests (KEDA, tema 02)
4. KServe / Kubeflow: qué resuelven sobre Kubernetes puro (InferenceService,
   autoscaling a cero de modelos, canary de versiones de modelo)
5. Costos: la GPU es el recurso más caro de la nube — autoscale a cero y
   right-sizing importan más que en cargas tradicionales
6. Seguridad específica de IA: prompt injection, exfiltración de datos vía
   LLM, por qué el modelo nunca debe tener credenciales de escritura amplias

## Recursos

- Azure OpenAI Service: https://learn.microsoft.com/azure/ai-services/openai/
- Amazon Bedrock: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- Vertex AI: https://cloud.google.com/vertex-ai/docs
- KServe: https://kserve.github.io/website/
- Kubeflow: https://www.kubeflow.org/docs/

## Lab sugerido

Construye una API con FastAPI (tema 08) que reciba una pregunta, haga
retrieval sobre un vector database simple (puede ser local, tipo Chroma,
para el lab) y genere la respuesta llamando a un modelo administrado (Azure
OpenAI o el que tengas disponible). Despliega esa API en Container Apps o
Cloud Run (tema 02) usando identidad gestionada para autenticarte contra el
servicio de IA, sin guardar ninguna API key en el código ni en variables de
entorno planas.

## Autoevaluación

Pídeme: *"Dame un examen de infraestructura de IA / MLOps nivel intermedio"*.
