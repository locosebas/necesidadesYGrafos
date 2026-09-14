# Roadmap de estudio

Orden sugerido. Cada bloque es aprox. 1-2 semanas de estudio part-time
(mientras trabajás). Ajustalo a tu ritmo real — lo importante es no saltar
el examen de autoevaluación al final de cada tema.

## Actualización de objetivo (2026-09-14): de "Senior DevOps" a "Arquitecto de plataforma"

El objetivo dejó de ser solo "cerrar brechas para calificar a una vacante" y
pasó a ser **poder diseñar y construir una self-service developer platform
completa desde cero (0→1)**, como la del posting de Vule Human Talent
(Senior DevOps/Platform Engineer, startup de salud, GKE + Terraform + ArgoCD
+ Istio + GitLab CI + Keycloak + OPA + AlloyDB + OpenTelemetry, sept. 2026).

Esto cambia el orden de estudio en dos puntos concretos:

1. **Kubernetes se adelanta y se abre en capas.** Antes de repasar
   troubleshooting (que ya estaba pendiente), hace falta la **arquitectura**
   del clúster (control plane, nodos, CNI, CSI, cómo se levanta un clúster) —
   sin eso, troubleshooting es memorizar recetas sueltas en vez de entender
   qué componente falló. Ver `temas/10-kubernetes-avanzado/README.md`, que
   ahora es un índice ordenado (arquitectura → scheduling/recursos →
   networking/mesh → operators/managed-k8s → troubleshooting, al final).
2. **Se agrega un tema de cierre: `temas/16-platform-engineering/`.** Saber
   cada herramienta suelta no alcanza para ser arquitecto — hace falta el
   marco que explica cómo se combinan (Internal Developer Platform, golden
   paths, Team Topologies, production readiness) y un diagrama de referencia
   que ubica cada tema del plan dentro de la arquitectura completa del
   posting.

Las fases de abajo (1-9) siguen siendo el contenido técnico por
herramienta/concepto — ahora reordenadas para construir de abajo hacia
arriba (cómputo y red primero, plataforma completa al final) en vez de por
frecuencia en ofertas de trabajo.

## Metodología: de general a específico

Objetivo final: llegar a una entrevista técnica (o certificación) y poder
resolver la prueba, no solo "haber leído sobre el tema". Por eso cada nivel
sigue el mismo patrón general → específico:

1. **General (panorama):** examen diagnóstico amplio que toca los 13 temas a
   nivel conceptual, para medir dónde estás parado hoy en la práctica (no
   solo lo que infiere el CV). Esto define qué temas se profundizan primero.
2. **Específico (por tema):** dentro de cada tema, primero repaso el concepto
   general (qué es, para qué sirve, cómo se relaciona con lo demás) y recién
   después vamos a detalle técnico (sintaxis, configuración, troubleshooting).
3. **Examen del tema:** mezcla teoría + escenario, nivel creciente
   (básico → intermedio → senior) hasta llegar a ≥ 80%.
4. **Repaso mixto/entrevista:** una vez cubiertos varios temas, exámenes que
   combinan temas y simulan formato de entrevista técnica o prueba de
   certificación (preguntas encadenadas, sin decirte de antemano el tema).

## Preferencia pedagógica: repetición de términos

Una de las falencias que identificaste vos mismo: se te olvidan los **términos
y nombres de herramientas**, no los conceptos. Por eso, al enseñar/evaluar,
Claude debe ser **redundante a propósito**: repetir el nombre exacto de cada
término/herramienta varias veces en la misma explicación (en vez de decir
"esto" o "dicho servicio", repetir "Managed Identity", "Managed Identity" de
nuevo), en vez de evitar la repetición por estilo. Es una decisión deliberada
de este plan, no un descuido de redacción — no "corregir" esto a un estilo
más variado en el futuro.

## Preferencia pedagógica: interacción de a poco (problemas de atención)

El usuario también avisó que tiene problemas de atención. Consecuencia
práctica: **nunca tirar una lista larga de preguntas juntas** (por ejemplo,
un examen de 13 preguntas de una sola vez). Las sesiones de examen/enseñanza
deben ser de ida y vuelta — **una pregunta por vez** (excepcionalmente dos si
son muy cortas), esperar la respuesta, corregir/explicar esa respuesta
puntual, y recién ahí pasar a la siguiente. Nada de monólogos largos ni de
tandas de preguntas en batch. Esto aplica a exámenes, explicaciones de temas,
y cualquier interacción de enseñanza en este plan.

## Fase 0 — Diagnóstico general (ya hecho, ver registro)

Antes de la Fase 1: un examen general de panorama (1-2 preguntas por cada uno
de los 13 temas originales, nivel conceptual). Con el resultado se ajustó el
orden real de estudio — ver `examenes/registro/resultados.md` para los
puntos débiles detectados y pendientes de profundización.

## Fase 1 — Kubernetes: arquitectura y fundamentos (arranca acá)

Base de todo lo demás — la plataforma completa (Fase 9) corre sobre
Kubernetes. Por eso va primero, no al final como "repaso de fortaleza".

1. `temas/10-kubernetes-avanzado/01-arquitectura-y-cluster.md` — componentes, reconciliation loop, cómo se arma un clúster, CNI, CSI
2. `temas/10-kubernetes-avanzado/02-scheduling-recursos-autoscaling.md` — scheduling, QoS, HPA/VPA/Cluster Autoscaler, RBAC de K8s
3. `temas/10-kubernetes-avanzado/03-networking-service-mesh.md` — Services, Network Policies, Ingress/Gateway API, Istio
4. `temas/10-kubernetes-avanzado/04-operators-crds-managed-k8s.md` — Operators/CRDs, diferencias AKS/EKS/GKE (foco GKE por el posting)

`05-troubleshooting.md` de este mismo tema se deja para la **Fase 8**, una
vez que el resto del plan (identidad, red, datos, observabilidad) ya esté
visto — la mayoría de los síntomas de troubleshooting son fallas en esas
capas vistas desde Kubernetes.

## Fase 2 — IaC multi-cloud (semanas 3-4)

Para poder provisionar toda la plataforma como código, incluyendo el propio
clúster de Kubernetes.

5. `temas/01-iac-multicloud` — Terraform (ya es tu fortaleza), Bicep, y de paso CloudFormation/CDK (AWS)
6. `temas/02-contenedores-serverless` — Container Apps / Fargate / Cloud Run (contraste con K8s "real" de la Fase 1)

## Fase 3 — CI/CD y GitOps (semanas 5-6)

7. `temas/03-cicd-multicloud` — GitHub Actions + OIDC, **GitOps con ArgoCD**, GitLab CI como alternativa

## Fase 4 — Identidad (semanas 7-8)

8. `temas/04-identidad-iam` — Entra ID/RBAC, AWS IAM, GCP IAM, Managed Identity, y **Keycloak** (IAM propio/self-hosteado, clave para una plataforma multi-cloud real)

## Fase 5 — Networking avanzado y seguridad (semanas 9-10)

9. `temas/05-networking-multicloud` — VNet/VPC, Private Endpoints/PrivateLink/Private Service Connect
10. `temas/11-seguridad-devsecops` — shift-left security, escaneo de imágenes/IaC, **OPA/policy-as-code**

Al final de la Fase 5 deberías poder explicar de memoria cómo una app llega a
una base de datos sin exponer secretos ni tráfico a internet público, **y**
cómo se le impone una regla de seguridad a todo el clúster sin tocar cada
app (OPA/Gatekeeper) — en cualquiera de las tres nubes.

## Fase 6 — Datos y secretos (semanas 11-12)

11. `temas/06-datos-secretos` — Key Vault/Secrets Manager/Secret Manager, Cosmos DB/DynamoDB/Firestore, **AlloyDB**/RDS/Cloud SQL (relacional)

## Fase 7 — Observabilidad y async/orquestación (semanas 13-14)

12. `temas/07-observabilidad-multicloud` — Azure Monitor, CloudWatch, Cloud Logging/Monitoring, OpenTelemetry
13. `temas/09-orquestacion-serverless` — Durable Functions / Step Functions / Workflows, **Temporal**
14. `temas/14-streaming-eventos` — Kafka/**Redpanda**, Event Hubs, Kinesis, Pub/Sub

## Fase 8 — Kubernetes: troubleshooting (semana 15)

15. `temas/10-kubernetes-avanzado/05-troubleshooting.md` — `CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff`, con toda la base de las fases 1-7 ya cubierta

## Fase 9 — Arquitectura de plataforma (capstone) (semanas 16-17)

16. `temas/16-platform-engineering` — Internal Developer Platform, golden paths, Team Topologies, production readiness, y el diagrama de referencia que une **todos** los temas anteriores en la plataforma completa del posting de Vule.
17. `temas/12-arquitectura-costos-multicloud` — Well-Architected/Architecture Frameworks, FinOps (costos de la plataforma completa)
18. `temas/08-python-fastapi-docker` — repaso y hardening de APIs (lo que corre *dentro* de la plataforma)

## Fase 10 — Certificación y entrevista

- Rendir la certificación elegida (ver `certificaciones/README.md`).
- Repasar `temas/13-mercadolibre-scopes-cosmos` si aplica a una entrevista interna.
- Repasar `temas/15-interoperabilidad-salud` si la vacante es de un dominio de salud (HL7/FHIR/Medplum/HAPI).
- Simulacro de entrevista técnica con Claude usando `examenes/` en modo mixto (preguntas de varios temas, formato entrevista), y un simulacro de **diseño de arquitectura en vivo** ("diseñame la plataforma del posting paso a paso") usando el tema 16.

## Cómo avanzar de fase

No avances de fase hasta tener **≥ 80% en el examen de cada tema** de la fase
anterior (ver `examenes/registro/`). Si un tema queda débil, se repite antes de
seguir — la idea es no acumular huecos.

## Fuentes de la investigación de mercado (sept. 2026)

Estas fuentes ya no determinan el **orden** de las fases (eso ahora lo define
la arquitectura de la plataforma objetivo), pero siguen sirviendo para saber
qué certificación/skill tiene más demanda real:

- [Azure DevOps and Security in 2026: Career Path, Skills & Certs — CloudThat](https://www.cloudthat.com/resources/blog/azure-devops-and-security-roadmap-for-2026-skills-and-certifications)
- [Senior DevOps Engineer Job Description: Skills, Salary, & More — iMocha](https://www.imocha.io/job-description/senior-devops-engineer)
- [Job Opening - Senior Azure DevOps / Cloud Platform Engineer — Randstad USA](https://www.randstadusa.com/jobs/4/1343959/senior-azure-devops-cloud-platform-engineer_woburn/)
- [Top 10 DevOps Certifications Engineers Choose in 2026 — KodeKloud](https://kodekloud.com/blog/top-10-devops-certifications-courses-engineers-are-choosing/)
- [AZ-400 Certification (2026 Guide) — CertDemand](https://certdemand.com/certs/az-400)
- [Platform Engineering Certifications 2026 — ExamCert](https://www.examcert.app/blog/platform-engineering-certifications-2026/)

> Nota: son fuentes secundarias (blogs/agregadores), no un estudio estadístico
> formal. Sirven de contexto de mercado — el `gap-analysis.md` (basado en tu
> CV real) y el diagrama de plataforma del tema 16 son la referencia real
> para saber qué tan profundo tenés que ir en cada tema.
