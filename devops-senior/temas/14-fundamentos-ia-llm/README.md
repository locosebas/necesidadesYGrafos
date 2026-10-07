# Fundamentos de IA, Machine Learning y LLMs

Base conceptual de toda la parte de IA del plan. No es "matemática de
paper": es el vocabulario y los modelos mentales que necesitás para poder
desarrollar, desplegar y operar sistemas de IA (y para no perderte en una
entrevista cuando aparezcan términos como **embedding**, **context window**
o **fine-tuning**).

## Objetivos

- Explicar la diferencia entre **Machine Learning clásico**, **Deep Learning**
  y **LLMs (Large Language Models)**, y cuándo conviene cada uno.
- Entender el ciclo **entrenamiento (training) vs. inferencia (inference)**:
  qué pasa en cada uno, qué recursos consume (GPU, memoria) y quién lo hace
  (casi siempre vos solo hacés **inferencia** sobre un modelo ya entrenado).
- Manejar el vocabulario de LLMs: **token**, **context window**,
  **temperature**, **embedding**, **transformer**, **hallucination**.
- Saber elegir entre las tres formas de "adaptar" un LLM:
  **prompting** → **RAG** → **fine-tuning** (de más barata a más cara).
- Métricas básicas de evaluación de modelos de ML clásico: **accuracy**,
  **precision**, **recall**, **F1**, **overfitting**.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Plataforma de IA "paraguas" | **Azure AI Foundry** | **Amazon Bedrock** (GenAI) + **SageMaker AI** (ML) | **Vertex AI** |
| Acceso a LLMs por API (modelos de terceros) | Azure OpenAI + catálogo de modelos de Foundry | Bedrock (Claude, Llama, Mistral, Amazon Nova…) | Vertex AI Model Garden (Gemini, Claude, Llama…) |
| ML clásico gestionado (entrenar tus modelos) | **Azure Machine Learning** | **SageMaker AI** | Vertex AI Training |
| Servicios de IA "pre-armados" (OCR, voz, visión) | Azure AI Services | Textract, Transcribe, Rekognition | Document AI, Speech-to-Text, Vision AI |

## Subtemas

1. ML clásico: supervisado / no supervisado, features, train/validation/test split, overfitting
2. Métricas: accuracy, precision, recall, F1, matriz de confusión
3. Deep Learning y la arquitectura **transformer** (a nivel intuición, no matemática)
4. LLMs: tokens, context window, temperature/top-p, costo por token, latencia
5. **Embeddings**: qué son, por qué permiten "búsqueda por significado"
6. Prompting vs. **RAG** vs. **fine-tuning**: árbol de decisión
7. Modelos abiertos (Llama, Mistral, Qwen) vs. cerrados (Claude, GPT, Gemini): trade-offs

## Recursos

- Google — Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course
- Anthropic — documentación de modelos: https://docs.anthropic.com/
- Microsoft Learn — AI-900 learning path: https://learn.microsoft.com/credentials/certifications/azure-ai-fundamentals/

## Lab sugerido

Llamá a un LLM por API (por ejemplo, Claude en Bedrock o Vertex AI, o la API
de Anthropic directa) con el mismo prompt variando la **temperature** (0, 0.5,
1). Contá los **tokens** de entrada/salida y calculá el costo de 1.000 llamadas.

## Autoevaluación

Pedime: *"Dame un examen de fundamentos de IA y LLMs nivel básico"*.
