# Gap Analysis — perfil actual vs. vacante Senior Software Engineer (Nu Colombia)

Fuente de los requisitos: publicación de LinkedIn, postulación propia,
2026-09-10. https://www.linkedin.com/jobs/view/4454359559/

> Este análisis es específico de esa vacante puntual (Nubank/Nu Colombia).
> Los temas de `../temas/` sirven igual para cualquier oferta Senior
> Software Engineer con stack similar (sistemas distribuidos, mensajería,
> bases NoSQL), no solo para esta empresa.

## Requisitos de la vacante

| # | Requisito | Nivel actual (según lo documentado en `devops-senior/`) | Estado |
|---|---|---|---|
| 1 | 6+ años desarrollando productos digitales en entornos complejos | Experiencia real en Bizagi, MercadoLibre, AgroTec — a confirmar si suma 6 años en desarrollo de producto (no solo plataforma/infra) | 🟡 Por confirmar |
| 2 | Sistemas distribuidos y arquitectura de microservicios | Kubernetes/Docker en producción de alto volumen (MercadoLibre) — experiencia *operando* microservicios. **Diseñar** la arquitectura de un sistema distribuido desde cero: por confirmar | 🟡 Brecha media |
| 3 | Diseñar sistemas a gran escala (miles/millones de usuarios) | MercadoLibre es un entorno de ese volumen, pero el rol ahí era más infra/plataforma que diseño de arquitectura de producto | 🟡 Brecha media |
| 4 | Programación orientada a objetos o funcional | Python (fuerte). **Clojure específicamente**: no mencionado en el CV — es un lenguaje funcional puro, distinto en paradigma incluso de Python | 🔴 Brecha alta |
| 5 | Liderazgo técnico y mentoring | No documentado formalmente en `devops-senior/gap-analysis.md` | 🔴 Brecha alta (o por confirmar — puede existir experiencia no registrada) |
| 6 | Metodologías ágiles y CI/CD | CI/CD fuerte (Azure Pipelines, Jenkins, GitHub Actions) | 🟢 Brecha baja |
| 7 | Inglés avanzado | No evaluado en este repo | ⚪ Sin dato |
| 8 | **Clojure** (lenguaje principal del rol) | Sin experiencia previa — la oferta aclara que dan entrenamiento, pero conviene llegar con una base | 🔴 Brecha alta |
| 9 | Finagle, arquitectura hexagonal | Sin experiencia documentada | 🔴 Brecha alta |
| 10 | Kafka | Sin experiencia productiva documentada (sí mensajería/eventos en AWS serverless — AgroTec) | 🟡 Brecha media |
| 11 | Datomic | Base de datos poco común (modelo de "hechos" inmutables), sin experiencia previa | 🔴 Brecha alta |
| 12 | DynamoDB | No aparece en el CV documentado (sí Cosmos DB/DynamoDB como brecha en `devops-senior`) | 🔴 Brecha alta (comparte brecha con el track DevOps) |
| 13 | Kubernetes, AWS | Fuerte — MercadoLibre en producción de alto volumen transaccional | 🟢 Fortaleza |
| 14 | Prometheus | Ya identificado como fortaleza en `devops-senior/gap-analysis.md` | 🟢 Fortaleza |

## Fortalezas a favor (no pierdas esto en la entrevista)

- **Kubernetes + AWS en producción de alto volumen** (MercadoLibre) — encaja
  directo con el pedido de la vacante, sin brecha.
- **Prometheus / observabilidad** — ya es fortaleza documentada.
- **CI/CD y metodologías ágiles** — fuerte, transferible directo.
- **Experiencia multi-stack real** (Python, Terraform, Azure/AWS/GCP) muestra
  capacidad de aprender lenguajes/herramientas nuevas rápido — argumento
  directo para la brecha de Clojure (que la vacante ya asume, dando
  entrenamiento).
- **Programación funcional no es terreno cero**: Python soporta funciones de
  orden superior, comprehensions, `map`/`filter`/`reduce` — es un punto de
  entrada real hacia los conceptos de Clojure (inmutabilidad, funciones
  puras), aunque la sintaxis (Lisp, paréntesis prefijos) sea nueva.

## Prioridad de estudio (de mayor a menor brecha)

1. **Programación funcional + Clojure** — es el cambio de paradigma más
   grande y el lenguaje principal del rol; sin esto no se puede avanzar en
   el resto (los demás temas se explican en términos de Clojure/JVM).
2. **Arquitectura hexagonal + sistemas distribuidos (diseño, no solo
   operación)** — pasar de "opero microservicios" a "diseño la arquitectura
   de un sistema distribuido".
3. **Datomic** — modelo de datos nuevo y poco común, alto valor diferencial
   en la entrevista si se puede hablar de él con soltura.
4. **Kafka** — mensajería asíncrona a escala, conceptualmente relacionado
   con lo que ya sabés de sistemas event-driven en AWS (AgroTec).
5. **DynamoDB** — comparte estudio con la brecha ya identificada en
   `devops-senior/temas/06-datos-secretos/`.
6. **Liderazgo técnico y mentoring** — preparar ejemplos concretos (STAR)
   de situaciones reales, no solo teoría.
7. **Kubernetes/AWS/Prometheus** — repaso rápido nomás, ya son fortalezas.

Ver el orden de estudio semana a semana en `roadmap.md`.
