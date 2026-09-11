# Mensajería asíncrona: Apache Kafka

La vacante lo menciona explícitamente para "high-throughput jobs and
inter-service communication". Tenés experiencia con eventos/serverless en
AWS (AgroTec) — el objetivo es formalizar eso en el modelo específico de
Kafka.

## Objetivos

- Explicar el modelo de Kafka: **topics**, **particiones**, **producers**,
  **consumers**, **consumer groups**, **offsets**.
- Explicar las garantías de entrega: **at-most-once**, **at-least-once**,
  **exactly-once** — y por qué la mayoría de sistemas reales diseñan para
  at-least-once + idempotencia del lado del consumidor (en vez de depender
  de exactly-once end-to-end).
- Explicar por qué las particiones son la unidad de paralelismo y de orden
  (orden garantizado *dentro* de una partición, no entre particiones).
- Explicar el rol de Kafka como "log distribuido" (append-only log) y en qué
  se diferencia de una cola tradicional (mensaje no se borra al consumirse).

## Subtemas

1. Producers: claves de partición (partition key), acks (0/1/all),
   compresión
2. Consumers: consumer groups, rebalanceo, commit de offsets (automático vs.
   manual)
3. Garantías de entrega y diseño de consumidores idempotentes (relacionar
   con idempotencia en `../02-sistemas-distribuidos-hexagonal/`)
4. Retención y compactación de topics (`log.retention`, compacted topics
   para modelar "último estado conocido")
5. Casos de uso típicos: comunicación entre microservicios (eventos de
   dominio), procesamiento de streams, buffer de alto throughput

## Recursos

- Documentación oficial: https://kafka.apache.org/documentation/
- Confluent, "Kafka: The Definitive Guide" (gratuito): https://www.confluent.io/resources/kafka-the-definitive-guide-v2/

## Lab sugerido

Sin necesidad de un cluster real: diseñá el esquema de topics para el
sistema de 3 servicios que dibujaste en el lab de
`../02-sistemas-distribuidos-hexagonal/` (ej. `pedidos.creados`,
`inventario.reservado`). Definí qué garantía de entrega necesita cada uno y
por qué, y cómo el consumidor evita procesar un mensaje duplicado.

## Autoevaluación

Pedime: *"Dame un examen de Kafka nivel intermedio"* o *"Explicame consumer
groups y rebalanceo"*.
