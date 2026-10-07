# Desarrollo de aplicaciones con LLMs

El "desarrollo IA" del plan: construir aplicaciones reales sobre LLMs.
Aprovecha tu base fuerte de Python y FastAPI (tema 08) — una API de IA en
producción es, en gran parte, una API FastAPI bien hecha que llama a un
modelo.

## Objetivos

- Integrar un LLM por API desde Python: SDK oficial, autenticación,
  manejo de errores, **retries** y **rate limits**.
- **Prompt engineering** práctico: system prompt, few-shot, instrucciones
  claras, separar datos de instrucciones.
- **Structured output**: obtener JSON válido y validarlo con **Pydantic**.
- **Tool use / function calling**: que el modelo llame a funciones tuyas.
- **Streaming** de respuestas (Server-Sent Events) desde FastAPI.
- Control de costos y latencia: **prompt caching**, elegir el modelo más chico
  que alcance, limitar tokens de salida.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| API de modelos | Azure OpenAI / Azure AI Foundry Models | Bedrock (`InvokeModel`, **Converse API**) | Vertex AI (Gemini API, Model Garden) |
| Autenticación sin secretos | **Managed Identity** + Entra ID | **IAM Role** | **Service Account** |
| Límite de uso | Cuota de TPM (tokens por minuto) por deployment | Service quotas por modelo / Provisioned Throughput | Cuotas por modelo / Provisioned Throughput |
| Playground para probar prompts | Azure AI Foundry playground | Bedrock playground | Vertex AI Studio |

## Subtemas

1. SDKs: Anthropic SDK, OpenAI SDK, `boto3` (Bedrock), `google-genai` (Vertex AI)
2. Prompt engineering: system prompt, few-shot, cadena de razonamiento, plantillas versionadas
3. Structured output + validación con Pydantic
4. **Tool use / function calling**: definir herramientas, loop de llamadas
5. Streaming desde FastAPI (`StreamingResponse`, SSE)
6. Resiliencia: retries con backoff, timeouts, fallback a otro modelo/región
7. Costos: prompt caching, batch API, elección de modelo
8. Testing de apps LLM: tests con respuestas mockeadas + evaluaciones (ver tema 18)

## Recursos

- Anthropic — Build with Claude: https://docs.anthropic.com/
- Amazon Bedrock Converse API: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
- Azure OpenAI: https://learn.microsoft.com/azure/ai-services/openai/
- Vertex AI Generative AI: https://cloud.google.com/vertex-ai/generative-ai/docs

## Lab sugerido

Una API FastAPI con un endpoint `/resumir` que recibe un texto, llama a un LLM
con **structured output** (JSON con `resumen`, `temas`, `sentimiento`),
valida con Pydantic, hace **streaming** de la respuesta y se autentica contra
la nube con **Managed Identity / IAM Role / Service Account** (sin API keys
en el código). Dockerizala y desplegala en Container Apps / Fargate / Cloud Run
(tema 02).

## Autoevaluación

Pedime: *"Dame un examen de desarrollo de apps con LLMs nivel intermedio"*.
