# Platform Engineering: plataforma interna para múltiples equipos de producto

Las ofertas piden *"experiencia en un equipo de platform engineering que
da soporte a múltiples equipos de producto"*. No es una herramienta: es una
forma de trabajar. Este tema junta todo lo anterior (IaC, CI/CD, Kubernetes,
GitOps, observabilidad, seguridad) bajo la pregunta: *¿cómo hago que diez
equipos desplieguen solos, seguros y sin pedirme nada?*

## Objetivos

- Explicar qué es una **IDP (Internal Developer Platform)** y la idea de
  **plataforma como producto**: los equipos de producto son tus clientes.
- Diseñar **golden paths** (caminos pavimentados): plantillas de servicio
  que ya traen CI/CD, observabilidad, seguridad y despliegue resueltos.
- **Self-service** con guardrails: los equipos crean recursos solos, pero
  dentro de políticas (**OPA**, tema 11) y con costos visibles.
- **Multi-tenancy** en Kubernetes: namespaces por equipo, RBAC, quotas,
  network policies, un cluster compartido vs. clusters por equipo.
- Medir la plataforma: **métricas DORA** (deployment frequency, lead time,
  change failure rate, time to restore) y satisfacción de los desarrolladores.

## Arquitectura de referencia (ejemplo real: posting de Vule Human Talent)

```
Developer Platform (self-service)
├── Capa de cómputo: Kubernetes (GKE)                    → temas 02, 10
├── IaC: Terraform                                       → tema 01
├── CD: GitOps (ArgoCD) + CI (GitLab CI/GitHub Actions)  → tema 03
├── Auth & Identity: Keycloak + IAM nativo de la nube    → tema 04
├── Red y seguridad de red: Service Mesh (Istio)         → tema 10
├── Policy as code: OPA/Gatekeeper                       → tema 11
├── Datos: AlloyDB + Cosmos/DynamoDB + Key Vault/Secrets → tema 06
├── Observabilidad: OpenTelemetry → Grafana/cloud-native → tema 07
└── Async/orquestación: Redpanda (eventos) + Temporal    → temas 09, 21
```

Un "Senior Platform Engineer 0→1" es quien puede decidir el **orden de
construcción** de este diagrama, justificar cada elección (por qué Istio y
no solo Ingress, por qué GitOps y no solo pipelines push), y estimar el
costo/complejidad operativa que cada capa suma: identidad antes que CD,
observabilidad desde el día 1, no al final.

## Herramientas y equivalencias

| Pieza de la plataforma | Herramientas típicas | Tema relacionado |
|---|---|---|
| Portal / catálogo de servicios | **Backstage** (CNCF), Port | — |
| GitOps / despliegue | **ArgoCD**, Flux | 03 |
| Infra self-service | Terraform modules, **Crossplane**, Azure Deployment Environments, AWS Service Catalog / Proton, GCP Infrastructure Manager | 01 |
| Políticas y guardrails | **OPA Gatekeeper**, Kyverno | 11 |
| Service mesh | **Istio** | 10 |
| Secretos | **ESO** + gestor de secretos de la nube | 06 |
| Identidad | **Keycloak** / Entra ID / IAM | 04 |
| Observabilidad estándar | **OpenTelemetry** + Grafana / nativo de la nube | 07 |
| Feature flags | **Flipt** | 03 |

## Subtemas

1. Platform as a product: roadmap, usuarios internos, documentación, soporte
2. **Team Topologies**: *platform team*, *stream-aligned teams*, *enabling teams*; reducir la carga cognitiva
3. Golden paths con **Backstage** Software Templates
4. Multi-tenancy en Kubernetes: aislamiento, quotas, costo por equipo (conecta con FinOps del tema 12)
5. Métricas **DORA** y cómo instrumentarlas
6. Contar tu experiencia: preparar 2-3 historias (formato STAR) de cuando ayudaste a varios equipos (por ejemplo, en MercadoLibre)

## Recursos

- CNCF Platforms White Paper: https://tag-app-delivery.cncf.io/whitepapers/platforms/
- Backstage: https://backstage.io/docs/
- platformengineering.org: https://platformengineering.org/
- DORA: https://dora.dev/
- Team Topologies: https://teamtopologies.com/key-concepts

## Lab sugerido

Escribí un **golden path** mínimo: un template (Backstage o un repo template
de GitHub) que genere un servicio FastAPI con Dockerfile, workflow de GitHub
Actions, manifiestos que despliega **ArgoCD**, instrumentación
**OpenTelemetry** y un `ExternalSecret` de **ESO**. Un equipo nuevo debería
poder tener un servicio en producción en menos de una hora.

## Autoevaluación

Pedime: *"Simulá una entrevista de platform engineering: diseñá la plataforma
para 10 equipos de producto"*. Es un tema para preguntas **de escenario y de
experiencia**, más que teóricas.
