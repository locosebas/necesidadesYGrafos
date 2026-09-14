# Platform Engineering: diseñar una self-service developer platform

Tema "objetivo final" del plan actualizado: no alcanza con saber cada
herramienta suelta (Kubernetes, Terraform, ArgoCD, Istio, Keycloak, OPA,
AlloyDB, OpenTelemetry...) — un **arquitecto de plataforma** tiene que saber
por qué se combinan así y qué problema de negocio resuelve la combinación.
Es el tema que conecta con la vacante completa de Vule Human Talent (Senior
DevOps/Platform Engineer, healthcare, "self-service developer platform...
desde cero (0→1)").

## Objetivos

- Explicar qué es una **Internal Developer Platform (IDP)** y por qué las
  empresas la construyen: reducir la *cognitive load* de los equipos de
  producto, para que no cada equipo reinvente su propio CI/CD/K8s/observabilidad.
- Explicar el concepto de **golden path / paved road**: el camino
  "recomendado y soportado" para hacer algo común (crear un servicio nuevo,
  desplegar a producción) — no es la única forma posible, es la que la
  plataforma hace fácil y segura por default.
- Ubicar cada herramienta del plan dentro de una arquitectura de referencia
  de plataforma (ver diagrama abajo).
- Vocabulario de **Team Topologies** (el marco más citado en Platform
  Engineering): equipos *stream-aligned* (entregan valor a negocio) vs.
  equipo *platform* (provee la plataforma como producto interno para que los
  stream-aligned no tengan que ser expertos en infra).
- Criterios de **production readiness**: qué tiene que tener un servicio
  antes de ir a producción en la plataforma (health checks, límites de
  recursos, dashboards, alertas, runbook, on-call).

## Arquitectura de referencia (la del posting, con lo que ya estudiaste en otros temas)

```
Developer Platform (self-service)
├── Capa de cómputo: Kubernetes (GKE)                    → temas 02, 10
├── IaC: Terraform                                       → tema 01
├── CD: GitOps (ArgoCD) + CI (GitLab CI/GitHub Actions)  → tema 03
├── Auth & Identity: Keycloak + IAM nativo de la nube    → tema 04
├── Red y seguridad de red: Service Mesh (Istio)         → tema 10 (03-networking-service-mesh.md)
├── Policy as code: OPA/Gatekeeper                       → tema 11
├── Datos: AlloyDB + Cosmos/DynamoDB + Key Vault/Secrets → tema 06
├── Observabilidad: OpenTelemetry → Grafana/cloud-native → tema 07
└── Async/orquestación: Redpanda (eventos) + Temporal    → temas 09, 14
```

Un "Senior Platform Engineer 0→1" es quien puede decidir el **orden de
construcción** de este diagrama, justificar cada elección (por qué Istio y
no solo Ingress, por qué GitOps y no solo pipelines push), y estimar el
costo/complejidad operativa que cada capa suma.

## Subtemas

1. IDP vs. "cada equipo hace lo suyo": el problema de *cognitive load* que resuelve una plataforma.
2. Golden paths: ejemplos reales (crear repo → template con CI/CD ya armado → deploy a un entorno de prueba con un solo comando).
3. Backstage (CNCF): el catálogo de software/plataforma open-source más usado para exponer el self-service (service catalog, software templates, TechDocs).
4. Team Topologies: stream-aligned, platform, enabling, complicated-subsystem teams — y las 3 interacciones (collaboration, X-as-a-Service, facilitating).
5. Production readiness checklist: qué exige la plataforma antes de un deploy a prod.
6. Costos y FinOps de la plataforma completa (conecta con tema 12).
7. Orden real de construcción 0→1: qué se levanta primero (cómputo+red) y qué depende de qué (identidad antes que CD; observabilidad desde el día 1, no al final).

## Recursos

- Team Topologies (resumen oficial): https://teamtopologies.com/key-concepts
- Backstage: https://backstage.io/docs/overview/what-is-backstage
- CNCF Platforms Whitepaper: https://tag-app-delivery.cncf.io/whitepapers/platforms/
- Platform Engineering (definición): https://platformengineering.org/blog/what-is-platform-engineering

## Autoevaluación

Pedime: *"Dame un examen de arquitectura de plataforma / platform engineering nivel senior"*
o *"Hagamos un diseño en vivo: diseñame la plataforma del posting de Vule paso a paso"*.
