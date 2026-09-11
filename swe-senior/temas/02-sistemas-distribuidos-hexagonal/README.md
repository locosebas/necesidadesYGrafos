# Sistemas distribuidos, microservicios y arquitectura hexagonal

Pasar de **operar** microservicios (tu experiencia actual con
Kubernetes/Docker en MercadoLibre) a **diseñar** la arquitectura de un
sistema distribuido desde cero — que es lo que pide explícitamente la
vacante ("designing and delivering large-scale systems").

## Objetivos

- Explicar los problemas centrales de un sistema distribuido: latencia de
  red, fallas parciales, consistencia vs. disponibilidad (CAP theorem),
  idempotencia.
- Explicar **arquitectura hexagonal** (ports & adapters): por qué separa el
  dominio (lógica de negocio) de los adaptadores (HTTP, base de datos, cola
  de mensajes), y qué gana el sistema con eso (testeable sin infraestructura
  real, reemplazar un adaptador sin tocar el dominio).
- Explicar **Finagle** (framework de RPC/microservicios de Twitter, usado en
  la JVM/Scala/Clojure): qué resuelve (comunicación entre servicios,
  balanceo de carga, circuit breakers) y cómo se relaciona con arquitectura
  hexagonal (Finagle típicamente vive en la capa de adaptadores).
- Explicar patrones de resiliencia: **circuit breaker**, **retry con
  backoff**, **timeout**, **bulkhead** — y por qué son necesarios cuando un
  servicio depende de otros que pueden fallar o estar lentos.

## Subtemas

1. Arquitectura hexagonal: puertos (interfaces que define el dominio) vs.
   adaptadores (implementaciones concretas: HTTP, DB, Kafka)
2. Finagle: `Service`, `Filter`, composición de servicios, balanceo de carga
   del lado del cliente
3. CAP theorem aplicado a decisiones reales (¿qué elige tu sistema cuando
   hay partición de red?)
4. Patrones de resiliencia: circuit breaker (estados: cerrado/abierto/
   semiabierto), retry con backoff exponencial, timeout, bulkhead
5. Idempotencia: por qué una operación distribuida necesita poder repetirse
   sin efectos duplicados (relevante para reintentos y para consumidores de
   Kafka con at-least-once delivery — ver `../03-mensajeria-kafka/`)
6. Trade-offs de diseño: monolito vs. microservicios, tamaño de servicio,
   comunicación síncrona (RPC) vs. asíncrona (eventos)

## Recursos

- "Designing Data-Intensive Applications" (Martin Kleppmann) — referencia
  estándar de la industria para estos temas, especialmente los capítulos de
  replicación, particionamiento y consistencia.
- Arquitectura hexagonal (artículo original, Alistair Cockburn):
  https://alistair.cockburn.us/hexagonal-architecture/
- Finagle: https://twitter.github.io/finagle/

## Lab sugerido

Diseñá (en papel/diagrama, no hace falta código) un sistema pequeño con al
menos 3 servicios (ej. pedidos, inventario, notificaciones) usando
arquitectura hexagonal: definí los puertos de cada servicio y qué
adaptador usarías para cada uno (HTTP, Kafka, base de datos). Identificá
dónde pondrías un circuit breaker y por qué.

## Autoevaluación

Pedime: *"Dame un examen de arquitectura hexagonal y sistemas distribuidos
nivel senior"* o *"Simulá una entrevista de system design de 30 minutos"*.
