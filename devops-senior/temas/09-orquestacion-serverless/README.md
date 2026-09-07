# Orquestación de workflows serverless: Durable Functions, Step Functions, Workflows

Patrón nuevo respecto a tu CV en Azure; en AWS ya tenés experiencia con
serverless (AgroTec) así que Step Functions puede resultarte más natural.

## Objetivos

- Explicar por qué se necesita un orquestador cuando un workflow tiene
  múltiples pasos con estado, reintentos, y posible espera larga (no resolverlo
  con funciones que se llaman entre sí "a mano").
- Patrones clásicos: chaining, fan-out/fan-in, esperar eventos externos
  (aprobaciones humanas), polling periódico.
- Determinismo: por qué el código orquestador no puede hacer I/O directo ni
  usar tiempo/random "crudo" (aplica conceptualmente a Durable Functions;
  Step Functions lo resuelve distinto, por definición declarativa en JSON).

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Orquestador de workflows | **Durable Functions** (código: orchestrator + activity functions) | **Step Functions** (definición declarativa ASL en JSON/YAML, "state machine") | **Workflows** (YAML declarativo) + Cloud Tasks (colas para trabajo async simple) |
| Modelo de definición | Imperativo (código Python/C#/JS con reglas de determinismo) | Declarativo (Amazon States Language) | Declarativo (YAML) |
| Fan-out/fan-in | `context.task_all()` sobre N activities | `Map` state (procesamiento paralelo) | Llamadas paralelas explícitas en el YAML o Cloud Tasks |
| Espera de evento externo (aprobación humana) | External events (`wait_for_external_event`) | `waitForTaskToken` (callback pattern) | HTTP callback + Cloud Tasks |
| Dónde vive el estado | Azure Storage (tables/queues/blobs) internamente | Gestionado por el servicio (no lo ves) | Gestionado por el servicio |

## Subtemas

1. Durable Functions: orchestrator, activity, client functions; reglas de determinismo/replay
2. Step Functions: Amazon States Language, tipos de estado (`Task`, `Choice`, `Map`, `Parallel`, `Wait`)
3. GCP Workflows: sintaxis YAML, conectores nativos a otros servicios GCP
4. Cuándo NO usar un orquestador (over-engineering para 2 pasos simples con una cola)
5. Comparación de costos y modelo de facturación (por transición de estado vs. por tiempo de ejecución)

## Recursos

- Durable Functions: https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview
- AWS Step Functions: https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
- GCP Workflows: https://cloud.google.com/workflows/docs

## Lab sugerido

Implementá el mismo patrón (fan-out/fan-in: "procesar N archivos en
paralelo y agregar el resultado") en Durable Functions y en Step Functions.
Compará el modelo imperativo vs. declarativo.

## Autoevaluación

Pedime: *"Dame un examen de orquestación serverless (Durable Functions/Step Functions) nivel senior"*.
