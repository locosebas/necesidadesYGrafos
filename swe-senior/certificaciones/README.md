# Certificaciones — por qué esta lista es corta

A diferencia de `../../devops-senior/certificaciones/README.md` (donde las
certificaciones de cloud/DevOps son un estándar de la industria muy
reconocido), el stack de esta vacante (**Clojure**, **Datomic**, **Finagle**)
**no tiene certificaciones formales reconocidas por la industria** — es un
ecosistema donde lo que pesa es demostrar código real (proyectos propios,
contribuciones open source) y desempeño en la entrevista técnica, no un
certificado.

## Qué sí tiene sentido certificar (transferible)

Estas sí son reconocidas y **suman igual** para este rol, porque cubren la
parte de infraestructura (Kubernetes/AWS) que la vacante también pide — ver
el detalle completo en `../../devops-senior/certificaciones/README.md`, no
se duplica acá:

- **CKA — Certified Kubernetes Administrator**: ya identificada como
  prioritaria en `devops-senior/`, sirve igual para este rol.
- **AWS Certified Solutions Architect – Associate** o **AWS Certified
  Developer – Associate**: esta última es más relevante acá que la de
  Solutions Architect, porque el rol es de desarrollo de producto (no
  infraestructura pura) — cubre SDKs, DynamoDB, mensajería (SQS/SNS,
  conceptualmente cercano a Kafka).
  https://aws.amazon.com/certification/certified-developer-associate/

## Qué demuestra más que un certificado, para este stack puntual

En lugar de buscar una certificación de Clojure (no existe una reconocida),
priorizá:

1. **Un proyecto propio en Clojure** publicado en GitHub (aunque sea
   pequeño) — resuelve un problema real usando al menos 2-3 de los
   conceptos de `../temas/01-programacion-funcional-clojure/`.
2. **4Clojure / Exercism (track Clojure)**: ejercicios cortos, buen
   termómetro de progreso real sin necesidad de un proyecto completo.
   https://exercism.org/tracks/clojure
3. **Katas de system design** documentadas (diagramas + decisiones) usando
   el vocabulario de `../temas/02-sistemas-distribuidos-hexagonal/` — más
   valioso en la entrevista que un certificado, porque es lo que
   literalmente te van a pedir en la ronda de system design.
