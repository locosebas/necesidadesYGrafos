# Streaming y mensajería de eventos: Kafka/Redpanda, Event Hubs, Kinesis, Pub/Sub

Tema no cubierto en el plan original (los 13 temas base) — aparece en
vacantes que construyen plataformas event-driven, sobre todo cuando piden
"self-service developer platform" o arquitecturas con múltiples equipos de
producto publicando/consumiendo eventos entre sí.

## Objetivos

- Diferenciar una **cola** (un mensaje, un consumidor, se borra al leerse) de
  un **log de eventos** (Kafka/Redpanda: el mensaje queda, muchos consumidores
  pueden releerlo, cada uno con su propio offset).
- Conceptos de Kafka (aplican igual a Redpanda, que es *wire-compatible*):
  topic, partition, offset, consumer group, replication factor.
- Cuándo un tema con múltiples consumidores independientes necesita un log de
  eventos en vez de una cola simple (SQS/Service Bus/Pub-Sub clásico).

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP | Self-hosted / open-source |
|---|---|---|---|---|
| Log de eventos (estilo Kafka) | **Event Hubs** (protocolo compatible con Kafka) | **MSK** (Managed Streaming for Kafka) o **Kinesis Data Streams** (API propia, no Kafka) | **Pub/Sub** (API propia, no Kafka) | **Apache Kafka** / **Redpanda** (reescritura en C++, API 100% compatible con Kafka, sin JVM/ZooKeeper) |
| Cola simple (punto a punto) | Service Bus Queues / Storage Queues | SQS | Pub/Sub (con un solo suscriptor) | RabbitMQ |

**Redpanda** es relevante porque aparece cada vez más como "el Kafka sin la
complejidad operativa de Kafka" (un solo binario, sin ZooKeeper/KRaft aparte,
más liviano) — mismos clientes/SDKs que ya funcionan contra Kafka, así que
migrar de uno a otro no cambia el código de la app.

## Subtemas

1. Partition key: por qué determina el orden (solo se garantiza dentro de una partition) y el paralelismo de consumo.
2. Consumer groups: cómo se reparten las partitions entre instancias de un mismo consumidor.
3. Replayability: reprocesar eventos históricos (ventaja clave frente a una cola que borra el mensaje leído).
4. Cuándo NO conviene (over-engineering para un caso de un solo productor/un solo consumidor).

## Recursos

- Apache Kafka: https://kafka.apache.org/documentation/
- Redpanda: https://docs.redpanda.com/
- Azure Event Hubs: https://learn.microsoft.com/azure/event-hubs/
- Amazon MSK: https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html
- GCP Pub/Sub: https://cloud.google.com/pubsub/docs

## Autoevaluación

Pedime: *"Dame un examen de streaming/mensajería de eventos (Kafka/Redpanda) nivel senior"*.
