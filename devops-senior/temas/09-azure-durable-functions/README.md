# Azure Durable Functions

Tema completamente nuevo respecto a tu CV. Es una extensión de Azure Functions
para orquestar workflows de larga duración/con estado, sin gestionar vos mismo
la máquina de estados.

## Objetivos

- Explicar los 3 tipos de función en el patrón Durable: **Orchestrator**,
  **Activity**, y **Client** (trigger que arranca la orquestación).
- Entender **event sourcing / replay**: por qué el código del orchestrator debe
  ser determinístico (no `datetime.now()`, no llamadas HTTP directas, no random
  sin las APIs durables equivalentes).
- Patrones clásicos: Function Chaining, Fan-out/Fan-in, Async HTTP APIs
  (long-running operations con polling), Monitor (polling periódico), Human
  interaction (aprobaciones).
- Comparar con alternativas: Logic Apps, Step Functions (AWS, que ya conocés),
  Temporal.

## Subtemas

1. Orchestrator function: reglas de determinismo, replay
2. Activity function: dónde va el trabajo real (I/O, llamadas externas)
3. Fan-out/fan-in: paralelizar N activities y esperar a que todas terminen
4. Durable Timers (`create_timer`) vs `time.sleep` (prohibido en orchestrator)
5. External events y human interaction (aprobar/rechazar una orquestación en curso)
6. Estado y storage: Durable Functions usa Azure Storage (tables/queues/blobs) internamente

## Recursos

- Durable Functions overview: https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview
- Durable Functions en Python: https://learn.microsoft.com/azure/azure-functions/durable/quickstart-python-vscode

## Lab sugerido

Implementá el patrón Fan-out/Fan-in: un orchestrator que dispara N activities
en paralelo (por ejemplo, "procesar N archivos"), espera a que todas terminen,
y agrega el resultado.

## Autoevaluación

Pedime: *"Dame un examen de Azure Durable Functions nivel senior"*.
