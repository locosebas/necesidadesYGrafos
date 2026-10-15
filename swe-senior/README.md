# Plan de aprendizaje — Camino a Senior Software Engineer (sistemas distribuidos)

Carpeta de estudio personal de Sebastián Díaz para prepararse a rol de
**Senior Software Engineer** con foco en **sistemas distribuidos, arquitectura
de microservicios y programación funcional**.

Origen: postulación a la vacante **Senior Software Engineer – Bogotá,
Colombia (Hybrid)** en **Nu Colombia** (Nubank),
https://www.linkedin.com/jobs/view/4454359559/ — sigue siendo la referencia
concreta para el diagnóstico de brechas, pero el alcance de esta carpeta
**no es solo Nubank**: el stack pedido (sistemas distribuidos, mensajería,
bases NoSQL, Kubernetes/AWS) es representativo de muchas ofertas Senior
Backend/Software Engineer, así que sirve como preparación general para ese
tipo de rol.

Esta carpeta es **complementaria** a `../devops-senior/`, no un reemplazo:
esa carpeta cubre infraestructura/plataforma multi-cloud; esta cubre el
lado de **diseño y construcción del software** (arquitectura, lenguaje,
mensajería, datos) que un Senior Software Engineer necesita además de (o en
vez de) la infraestructura. Donde hay solape real (Kubernetes, AWS,
observabilidad) se referencia el tema ya existente en `devops-senior/` en
vez de duplicarlo.

## Estructura

```
swe-senior/
├── 00-diagnostico/        # dónde estás hoy vs. dónde necesitas estar
│   ├── gap-analysis.md
│   └── roadmap.md
├── temas/                 # una carpeta por tema, con teoría + labs + lecturas
│   ├── 01-programacion-funcional-clojure/   # Clojure, Lisp, inmutabilidad, persistent data structures
│   ├── 02-sistemas-distribuidos-hexagonal/  # microservicios, arquitectura hexagonal, Finagle
│   ├── 03-mensajeria-kafka/                 # Kafka: producers/consumers, particiones, at-least-once
│   ├── 04-datos-datomic-dynamodb/           # Datomic (modelo único) + DynamoDB (repaso/profundización)
│   ├── 05-infra-k8s-aws-observabilidad/     # remite a devops-senior/temas/10 y /07, con notas específicas de este rol
│   ├── 06-liderazgo-tecnico-mentoria/       # liderazgo técnico, mentoring, code review, estándares de calidad
│   └── 07-entrevista-senior-swe/            # formato típico de entrevista Senior SWE (system design, coding, behavioral)
├── certificaciones/       # certificaciones relevantes (pocas para este stack; ver por qué)
├── examenes/              # cómo pedir exámenes y dónde queda el registro de resultados
│   ├── README.md
│   └── registro/
└── recursos/              # glosario y enlaces generales
```

## Cómo usar esto día a día

1. **Elegí un tema** de `temas/` (seguí el orden sugerido en `00-diagnostico/roadmap.md`,
   o el que te interese repasar).
2. **Leé** el `README.md` de ese tema: tiene objetivos, subtemas y enlaces oficiales.
3. **Pedime un examen** de ese tema (ver `examenes/README.md` para el formato).
   Resolvelo, te corrijo, y anotamos el resultado en `examenes/registro/`.
4. Revisamos juntos los puntos débiles y volvemos a ese tema o pasamos al siguiente.

Se aplican las mismas preferencias pedagógicas documentadas en
`../devops-senior/00-diagnostico/roadmap.md` (repetición deliberada de
términos, una pregunta por vez en exámenes/explicaciones) — no hace falta
repetirlas acá, valen para todo el repo.

No hace falta pedirme permiso para arrancar: decime "dame un examen de Clojure
nivel básico" o "explicame arquitectura hexagonal" y seguimos desde ahí.
