# Roadmap de estudio

Orden sugerido. Cada bloque es aprox. 1-2 semanas de estudio part-time
(mientras trabajás). Ajustalo a tu ritmo real — lo importante es no saltar
el examen de autoevaluación al final de cada tema.

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

## Fase 0 — Diagnóstico general (arranca acá)

Antes de la Fase 1: un examen general de panorama (1-2 preguntas por cada uno
de los 13 temas, nivel conceptual). Con el resultado ajustamos el orden real
de estudio — las brechas del `gap-analysis.md` son una hipótesis basada en el
CV, el diagnóstico general la confirma o la corrige con datos reales.

## Orden de las fases: priorizado por demanda real del mercado

El orden de las fases 1-5 no sigue solo el gap-analysis basado en tu CV — se
reordenó según qué aparece con más frecuencia en ofertas reales de Senior
DevOps Engineer / Azure Platform Engineer (búsqueda de mercado, sept. 2026,
ver fuentes al final del archivo). Señal consistente en las tres búsquedas:

1. **IaC (Terraform/Bicep/ARM)** — "core requirement across most postings"
2. **CI/CD** (Azure DevOps / GitHub Actions, YAML pipelines)
3. **Contenedores/Kubernetes** (AKS, Container Apps, Docker, Helm)
4. **Identidad y seguridad** (RBAC, compliance, identity management) — engloba networking/Private Endpoints como parte de "seguridad de red"
5. **Observabilidad** (monitoring, alerting)
6. Certificación de mayor señal combinada: **CKA + Terraform Associate + AZ-400**
   ("highest-signal combination" según la investigación de mercado)

Esto no anula tus brechas reales (Networking y Durable Functions siguen siendo
temas nuevos para vos) — simplemente prioriza primero lo que más se repite en
procesos de selección, para llegar antes a poder rendir pruebas técnicas.

## Fase 1 — IaC y Kubernetes/Contenedores (semanas 1-4)

Lo más pedido en las ofertas, y donde ya tenés más base (Terraform, Docker, K8s).

1. `temas/01-iac-multicloud` — Bicep, y de paso CloudFormation/CDK (AWS) y Terraform en GCP
2. `temas/10-kubernetes-avanzado` — repaso senior + diferencias AKS/EKS/GKE (cerrar huecos, ya es tu fortaleza)
3. `temas/02-contenedores-serverless` — Container Apps / Fargate / Cloud Run

## Fase 2 — CI/CD (semanas 5-6)

4. `temas/03-cicd-multicloud` — GitHub Actions + OIDC federado a Azure, AWS y GCP

## Fase 3 — Identidad, seguridad y networking (semanas 7-9)

5. `temas/04-identidad-iam` — Entra ID/RBAC, AWS IAM, GCP IAM
6. `temas/05-networking-multicloud` — VNet/VPC, Private Endpoints/PrivateLink/Private Service Connect
7. `temas/11-seguridad-devsecops` — shift-left security, escaneo de imágenes/IaC

Al final de la Fase 3 deberías poder explicar de memoria cómo una app llega a
una base de datos sin exponer secretos ni tráfico a internet público — **en
cualquiera de las tres nubes**.

## Fase 4 — Datos, serverless y observabilidad (semanas 10-12)

8. `temas/06-datos-secretos` — Key Vault/Secrets Manager/Secret Manager, Cosmos DB/DynamoDB/Firestore
9. `temas/09-orquestacion-serverless` — Durable Functions / Step Functions / Workflows
10. `temas/07-observabilidad-multicloud` — Azure Monitor, CloudWatch, Cloud Logging/Monitoring

## Fase 5 — Consolidación de nivel Senior (semanas 13-14)

11. `temas/08-python-fastapi-docker` — repaso y hardening de APIs
12. `temas/12-arquitectura-costos-multicloud` — Well-Architected/Architecture Frameworks, FinOps

## Fase 6 — Certificación y entrevista

- Rendir la certificación elegida (ver `certificaciones/README.md`).
- Repasar `temas/13-mercadolibre-scopes-cosmos` si aplica a una entrevista interna.
- Simulacro de entrevista técnica con Claude usando `examenes/` en modo mixto
  (preguntas de varios temas, formato entrevista).

## Cómo avanzar de fase

No avances de fase hasta tener **≥ 80% en el examen de cada tema** de la fase
anterior (ver `examenes/registro/`). Si un tema queda débil, se repite antes de
seguir — la idea es no acumular huecos.

## Fuentes de la investigación de mercado (sept. 2026)

- [Azure DevOps and Security in 2026: Career Path, Skills & Certs — CloudThat](https://www.cloudthat.com/resources/blog/azure-devops-and-security-roadmap-for-2026-skills-and-certifications)
- [Senior DevOps Engineer Job Description: Skills, Salary, & More — iMocha](https://www.imocha.io/job-description/senior-devops-engineer)
- [Job Opening - Senior Azure DevOps / Cloud Platform Engineer — Randstad USA](https://www.randstadusa.com/jobs/4/1343959/senior-azure-devops-cloud-platform-engineer_woburn/)
- [Top 10 DevOps Certifications Engineers Choose in 2026 — KodeKloud](https://kodekloud.com/blog/top-10-devops-certifications-courses-engineers-are-choosing/)
- [AZ-400 Certification (2026 Guide) — CertDemand](https://certdemand.com/certs/az-400)
- [Platform Engineering Certifications 2026 — ExamCert](https://www.examcert.app/blog/platform-engineering-certifications-2026/)

> Nota: son fuentes secundarias (blogs/agregadores), no un estudio estadístico
> formal. Sirven para priorizar el orden de estudio, no como verdad absoluta —
> el `gap-analysis.md` (basado en tu CV real) sigue siendo la referencia para
> saber qué tan profundo tenés que ir en cada tema.
