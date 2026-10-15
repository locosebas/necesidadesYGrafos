# Roadmap de estudio

Orden sugerido. Cada bloque es aprox. 1-2 semanas de estudio part-time
(mientras trabajás). Ajustalo a tu ritmo real — lo importante es no saltar
el examen de autoevaluación al final de cada tema.

## Metodología y preferencias pedagógicas

Se aplican las mismas reglas ya documentadas en
`../../devops-senior/00-diagnostico/roadmap.md`:

- **General → específico**: primero un panorama conceptual de los 7 temas,
  después profundidad técnica tema por tema, después exámenes mixtos tipo
  entrevista.
- **Repetición deliberada de términos**: al enseñar/evaluar, repetir el
  nombre exacto de cada término (p. ej. "arquitectura hexagonal",
  "arquitectura hexagonal" de nuevo) en vez de evitarlo por estilo.
- **Una pregunta por vez**: nunca tirar una lista larga de preguntas juntas,
  ni en exámenes ni en explicaciones — ida y vuelta, corrección puntual, y
  recién ahí la siguiente.

No hace falta repetir estas reglas cada vez que se pide un examen de esta
carpeta — ya están vigentes para todo el repo.

## Fase 0 — Diagnóstico general (arranca acá)

Antes de la Fase 1: un examen general de panorama (1-2 preguntas por cada
uno de los 7 temas, nivel conceptual). Con el resultado ajustamos el orden
real de estudio — las brechas del `gap-analysis.md` son una hipótesis
basada en lo documentado hasta ahora, el diagnóstico general lo confirma o
lo corrige con datos reales.

## Fase 1 — Programación funcional y Clojure (semanas 1-4)

El cambio de paradigma más grande y base para todo lo demás — sin esto, los
temas de arquitectura y datos se explican en un lenguaje que todavía no
manejás.

1. `temas/01-programacion-funcional-clojure` — sintaxis Lisp, inmutabilidad,
   funciones puras, persistent data structures, REPL-driven development

## Fase 2 — Arquitectura y sistemas distribuidos (semanas 5-7)

2. `temas/02-sistemas-distribuidos-hexagonal` — microservicios, arquitectura
   hexagonal (ports & adapters), Finagle, patrones de resiliencia
   (circuit breaker, retries, timeouts)

## Fase 3 — Mensajería y datos (semanas 8-11)

3. `temas/03-mensajeria-kafka` — producers/consumers, particiones,
   garantías de entrega (at-least-once/exactly-once), consumer groups
4. `temas/04-datos-datomic-dynamodb` — modelo de Datomic (hechos
   inmutables, tiempo como dimensión) y repaso/profundización de DynamoDB

## Fase 4 — Infraestructura (repaso, ya es fortaleza) (semana 12)

5. `temas/05-infra-k8s-aws-observabilidad` — repaso rápido: Kubernetes, AWS
   y Prometheus ya están cubiertos a fondo en `devops-senior/`; acá solo se
   agregan las particularidades de este rol (on-call, SLOs de un sistema
   Clojure/JVM en K8s).

## Fase 5 — Liderazgo técnico y preparación de entrevista (semanas 13-14)

6. `temas/06-liderazgo-tecnico-mentoria` — preparar ejemplos concretos
   (formato STAR) de mentoring, code review, decisiones de arquitectura
   defendidas ante el equipo.
7. `temas/07-entrevista-senior-swe` — simulacro de entrevista completa:
   coding en Clojure, system design de un sistema distribuido, preguntas
   de comportamiento/liderazgo.

## Cómo avanzar de fase

No avances de fase hasta tener **≥ 80% en el examen de cada tema** de la
fase anterior (ver `examenes/registro/`). Si un tema queda débil, se repite
antes de seguir — la idea es no acumular huecos, especialmente en Clojure
(Fase 1), que es la base de todo lo que sigue.
