# Glosario rápido

Términos que aparecen seguido en los temas de este repo. Referencia rápida,
no reemplaza leer el tema completo.

| Término | Definición corta |
|---|---|
| Clojure | Lenguaje funcional, dialecto de Lisp, corre sobre la JVM (también existe ClojureScript para JS) |
| Lisp | Familia de lenguajes con sintaxis prefija basada en paréntesis: `(funcion arg1 arg2)` |
| Persistent data structure | Estructura de datos inmutable donde "modificarla" crea una nueva versión sin alterar ni copiar por completo la anterior |
| REPL | Read-Eval-Print Loop — entorno interactivo donde se evalúa código en vivo; forma principal de desarrollar en Clojure |
| Arquitectura hexagonal | Patrón (ports & adapters) que separa el dominio de negocio de los detalles de infraestructura (HTTP, DB, colas) |
| Puerto (port) | Interfaz definida por el dominio, sin conocer la implementación concreta |
| Adaptador (adapter) | Implementación concreta de un puerto (ej. un cliente HTTP, un repositorio sobre DynamoDB) |
| Finagle | Framework de RPC/microservicios de Twitter para la JVM, con balanceo de carga y resiliencia integrados |
| Circuit breaker | Patrón de resiliencia que "corta" temporalmente las llamadas a un servicio que está fallando, para no saturarlo más |
| CAP theorem | En una partición de red, un sistema distribuido debe elegir entre Consistencia y Disponibilidad (no puede garantizar ambas) |
| Idempotencia | Propiedad de una operación que produce el mismo resultado si se ejecuta más de una vez |
| Kafka topic | Canal con nombre al que se publican mensajes, dividido en particiones |
| Partición (Kafka) | Subdivisión de un topic; unidad de paralelismo y de orden garantizado |
| Consumer group | Conjunto de consumidores que se reparten las particiones de un topic para procesarlas en paralelo |
| At-least-once | Garantía de entrega donde un mensaje puede procesarse más de una vez, nunca cero veces (requiere idempotencia del consumidor) |
| Datomic | Base de datos donde los datos son hechos inmutables con historial completo, consultable con Datalog |
| EAVT | Entidad-Atributo-Valor-Transacción — modelo de datos de Datomic (cada "hecho" es una tupla de estos 4 elementos) |
| Datalog | Lenguaje de consulta declarativo usado por Datomic (alternativa a SQL) |
| DynamoDB | Base de datos NoSQL gestionada de AWS, clave-valor/documento, con partition key y sort key |
| Single-table design | Patrón de modelado en DynamoDB donde varias entidades conviven en una sola tabla, optimizado para los patrones de acceso |
| STAR (entrevista) | Situación, Tarea, Acción, Resultado — formato para estructurar respuestas en entrevistas de comportamiento |

## Enlaces generales

- Clojure: https://clojure.org/
- Datomic: https://docs.datomic.com/
- Apache Kafka: https://kafka.apache.org/documentation/
- Finagle: https://twitter.github.io/finagle/
