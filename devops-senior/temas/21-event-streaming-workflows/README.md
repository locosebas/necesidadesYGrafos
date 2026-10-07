# Event streaming y workflows durables: Redpanda/Kafka y Temporal

Dos piezas que aparecen juntas en plataformas modernas: un **sistema de
event streaming** para mover eventos entre servicios, y un **motor de
workflows durables** para procesos largos con estado. Se apoya en el tema 09
(orquestación serverless): **Temporal** resuelve el mismo problema que
Durable Functions o Step Functions, pero agnóstico de nube.

## Objetivos

- Diferenciar **cola de mensajes** (un consumidor procesa y el mensaje
  desaparece) de **event streaming** (log persistente que varios consumidores
  leen a su ritmo y se puede re-leer).
- Manejar los conceptos de **Kafka** (que **Redpanda** implementa): *topic*,
  *partition*, *offset*, *consumer group*, *retention*, orden por partition key.
- Entender garantías de entrega: *at-most-once*, *at-least-once*,
  *exactly-once*, e **idempotencia** del consumidor.
- Explicar **Temporal**: *workflow* (código determinístico, como el
  orchestrator de Durable Functions), *activity* (el trabajo con I/O,
  que se reintenta), *worker*, *task queue*, *signals*.
- Elegir: ¿cola, streaming o workflow durable? (no son intercambiables).

## Equivalencias multi-cloud

| Concepto | Agnóstico / self-hosted | Azure | AWS | GCP |
|---|---|---|---|---|
| Event streaming (API Kafka) | **Redpanda**, Apache Kafka | **Event Hubs** (con endpoint Kafka) | **Amazon MSK** / Kinesis Data Streams | **Managed Service for Apache Kafka** / Pub/Sub |
| Cola de mensajes simple | RabbitMQ | Service Bus / Storage Queues | SQS | Pub/Sub / Cloud Tasks |
| Workflows durables | **Temporal** (self-hosted o Temporal Cloud) | Durable Functions | Step Functions | Workflows |

**Redpanda** vs. **Kafka**: misma API (los clientes de Kafka funcionan sin
cambios), pero **Redpanda** está escrito en C++, no necesita ZooKeeper ni JVM
y es más simple de operar. Por eso lo eligen muchas startups.

## Subtemas

1. Cola vs. streaming vs. pub/sub: árbol de decisión
2. **Kafka/Redpanda**: topics, partitions, consumer groups, rebalanceo, *consumer lag* (la métrica clave a monitorear)
3. Schema Registry y evolución de eventos (Avro/Protobuf/JSON Schema)
4. Patrones: *event sourcing*, *outbox pattern*, *CDC* (Change Data Capture, por ejemplo con Debezium)
5. **Temporal**: workflows, activities, retries, timeouts, signals/queries, versionado de workflows
6. **Temporal** vs. Durable Functions vs. Step Functions (conecta con el pendiente activity vs. orchestrator del tema 09)
7. Operar en Kubernetes: Redpanda Operator, Temporal Helm chart, observabilidad con **OpenTelemetry**

## Recursos

- Redpanda docs: https://docs.redpanda.com/
- Apache Kafka — conceptos: https://kafka.apache.org/documentation/#gettingStarted
- Temporal docs: https://docs.temporal.io/
- Azure Event Hubs para Kafka: https://learn.microsoft.com/azure/event-hubs/azure-event-hubs-kafka-overview

## Lab sugerido

Con Docker Compose: levantá **Redpanda** y **Temporal**. Un productor publica
eventos `paciente_registrado` en un topic de **Redpanda**; un consumidor los
lee y arranca un workflow de **Temporal** con tres activities (validar datos,
crear registro, mandar notificación). Matá el worker en el medio y mirá cómo
**Temporal** retoma desde la activity donde quedó.

## Autoevaluación

Pedime: *"Dame un examen de event streaming y Temporal nivel intermedio"*.
