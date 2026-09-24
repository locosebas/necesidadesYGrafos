# Proyectos prácticos — de básico a producción

Los exámenes miden si entendés un concepto; los **proyectos** miden si lo
podés construir. En una entrevista senior casi siempre aparece "contame algo
que hayas armado": esta lista sirve para tener proyectos propios, en un repo
público o de portfolio, que respalden cada tema de `../temas/`.

Fuente: post de LinkedIn "DevOps Project Ideas for Every Engineer" (Dipak
Shekokar, sept. 2026). La lista es suya; la columna **Tema** (a qué carpeta de
`temas/` se conecta cada proyecto) y la columna **Equivalencias** son
agregados de este plan para mantener el enfoque multi-cloud.

## Cómo usar esta lista

1. **No hagas todo.** Elegí 1-2 proyectos por tema, empezando por los que
   refuerzan el tema que estás estudiando ahora en el roadmap.
2. **Salteá lo que ya hiciste en producción** (MercadoLibre, Bizagi): marcalo
   como `[x] ya hecho en trabajo` y anotá dónde — eso ya es material para contar
   en una entrevista. Mejor invertir tiempo en las brechas.
3. **Un proyecto = un entregable concreto**: un repo con README, un diagrama y
   un "qué aprendí / qué haría distinto". Eso es lo que se muestra.
4. **Encadenalos.** Muchos proyectos se construyen sobre el anterior (ver
   "Proyecto integrador" al final) — no hace falta empezar de cero cada vez.
5. Al terminar uno, pedime un examen o una "defensa" tipo entrevista del
   proyecto (una pregunta por vez, como siempre).

Estado: `[ ]` pendiente · `[~]` en curso · `[x]` hecho

## Nivel 1 — Beginner

**Foco:** lo básico + entender cómo corren los sistemas.

| Estado | Proyecto | Tema | Equivalencias / notas |
|---|---|---|---|
| [ ] | CI/CD simple (GitHub Actions / Jenkins) | 03 | GitHub Actions es transversal a las 3 nubes |
| [ ] | Dockerizar una app básica | 08 | Usar la app FastAPI del tema 08 |
| [ ] | Nginx como reverse proxy | 05, 08 | Base para entender Ingress (tema 10) |
| [ ] | Analizador de logs Linux (CLI) | 07, 08 | Buen ejercicio de Python + regex |
| [ ] | Monitoreo básico (Prometheus + Grafana) | 07 | Cloud-agnóstico; en K8s via kube-prometheus-stack |
| [ ] | Sitio estático en la nube (S3 + CloudFront) | 02, 05 | Azure: Storage static website + Front Door · GCP: Cloud Storage + Cloud CDN |
| [ ] | Automatización con cron | 09 | Serverless: EventBridge Scheduler / Logic Apps / Cloud Scheduler |
| [ ] | Shell script de backup y limpieza | 06 | Agregar retención y logs de ejecución |
| [ ] | Deploy de un pod básico en Kubernetes | 10 | kind/minikube local; luego AKS/EKS/GKE |
| [ ] | Script de health check de servicios | 07 | Base de liveness/readiness probes (tema 10) |

## Nivel 2 — Intermediate

**Foco:** automatización + flujos de trabajo reales.

| Estado | Proyecto | Tema | Equivalencias / notas |
|---|---|---|---|
| [ ] | CI/CD completo (build → test → deploy) | 03 | Con OIDC a la nube, sin secretos estáticos |
| [ ] | Docker + Kubernetes para una app | 02, 10 | |
| [ ] | Terraform para infra cloud (EC2, VPC, S3) | 01, 05 | Azure: VM + VNet + Storage · GCP: GCE + VPC + GCS |
| [ ] | Helm chart para deploy de la app | 10 | Suma para CKA |
| [ ] | Logging centralizado (ELK / Loki) | 07 | Cloud: Log Analytics / CloudWatch Logs / Cloud Logging |
| [ ] | Autoscaling con HPA | 10 | Probar con carga real (k6, hey) |
| [ ] | Gestión segura de secretos (Vault / AWS Secrets Manager) | 06, 04 | Azure: Key Vault · GCP: Secret Manager |
| [ ] | Pipeline Blue-Green o Canary | 03, 10 | Argo Rollouts o slots de App Service / traffic split de Cloud Run |
| [ ] | GitOps con ArgoCD | 03, 10 | Alternativa: Flux (AKS lo trae como extensión) |
| [ ] | Monitoreo + alertas con Prometheus | 07 | Alertmanager; definir SLOs |

## Nivel 3 — Advanced

**Foco:** nivel producción + diseño de sistemas. Estos son los que más pesan
en una entrevista **senior**.

| Estado | Proyecto | Tema | Equivalencias / notas |
|---|---|---|---|
| [ ] | Plataforma CI/CD end-to-end para microservicios | 03, 10 | |
| [ ] | Infra multi-entorno con módulos de Terraform | 01 | dev/staging/prod con workspaces o directorios |
| [ ] | Arquitectura de deploy multi-región | 05, 12 | Front Door / Route 53 / Cloud Load Balancing global |
| [ ] | Cluster Kubernetes con autoscaling + HA | 10 | Cluster Autoscaler / Karpenter / GKE Autopilot |
| [ ] | Service mesh (Istio / Linkerd) | 10, 05 | mTLS entre servicios |
| [ ] | Logging distribuido + tracing | 07 | OpenTelemetry → App Insights / X-Ray / Cloud Trace |
| [ ] | Plataforma de observabilidad completa (logs + métricas + trazas) | 07 | Grafana LGTM stack o Datadog |
| [ ] | Disaster recovery (backup + failover) | 06, 12 | Definir RPO/RTO y probar el failover de verdad |
| [ ] | Pipeline DevSecOps (SAST, DAST, escaneo de imágenes) | 11, 03 | Trivy, Semgrep, OWASP ZAP; Defender / Inspector / Artifact Analysis |
| [ ] | Dashboard de optimización de costos cloud | 12 | Cost Management / Cost Explorer / Billing export a BigQuery |
| [ ] | Automatización de respuesta a incidentes | 07, 09 | Alerta → runbook automático (Logic Apps / Step Functions / Workflows) |
| [ ] | Platform Engineering (Internal Developer Platform) | 12, 03 | Backstage; es el rol "Platform Engineer" de la vacante |

## Proyecto integrador sugerido

En vez de 32 repos sueltos, un solo repo que crece por niveles cubre la
mayoría de la lista y cuenta una historia coherente en la entrevista:

1. **Nivel 1:** app FastAPI (tema 08) dockerizada + GitHub Actions que corre
   tests + health check.
2. **Nivel 2:** Terraform que levanta un cluster (AKS, EKS o GKE) + Helm chart
   + ArgoCD + secretos en Key Vault/Secrets Manager + Prometheus/Grafana + HPA.
3. **Nivel 3:** módulos de Terraform multi-entorno + canary con Argo Rollouts +
   OpenTelemetry + escaneo de seguridad en el pipeline + dashboard de costos.

Así un mismo proyecto demuestra IaC, CI/CD, Kubernetes, seguridad y
observabilidad — justo las 5 señales de mayor demanda del roadmap.
