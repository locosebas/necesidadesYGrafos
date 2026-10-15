# Herramientas del ecosistema + armar una arquitectura con confianza

Complemento de `README.md` (preguntas de la entrevista PayU). El objetivo no es
memorizar todo, sino tener un **mapa mental**: para cada problema, qué
herramienta lo resuelve, por qué esa y no otra, y cómo encaja en el conjunto.

> **Regla de oro en entrevista**: nunca nombres una herramienta sola. Siempre
> *problema → herramienta → por qué → trade-off*.
> Ej.: "Para que los pods lean secretos de Secrets Manager sin credenciales
> estáticas uso **External Secrets Operator** con **IRSA**; la alternativa es
> el CSI Secrets Store driver, pero ESO me da Secrets nativos de K8s y es más
> simple para los equipos."

---

## 1. Mapa de herramientas por categoría

### Infraestructura como código (IaC)

| Herramienta | Para qué sirve | Cuándo mencionarla |
|---|---|---|
| **Terraform / OpenTofu** | IaC declarativa multi-proveedor, con state | Estándar de la industria; OpenTofu es el fork open source |
| **Terragrunt** | Wrapper de Terraform: DRY de backends/providers, dependencias entre stacks | Muchos ambientes y cuentas con el mismo código |
| **Atlantis** | Plan/apply desde comentarios en el PR | GitOps de Terraform self-hosted |
| **Terraform Cloud / Spacelift / env0** | Ejecución remota, state, políticas, RBAC | Plataforma gestionada para equipos grandes |
| **tflint / checkov / trivy config / tfsec** | Lint y escaneo de seguridad de IaC | Pipeline de Terraform (shift-left) |
| **OPA/Conftest, Sentinel** | Policy-as-code ("no se permiten buckets públicos") | Guardrails automáticos en el PR |
| **Infracost** | Estima el costo del cambio en el PR | FinOps |
| **Pulumi / CDK** | IaC con lenguajes de programación | Alternativa si el equipo es muy dev |
| **Crossplane** | Infra cloud gestionada como recursos de Kubernetes | Plataformas internas "todo es K8s" |

### Contenedores y Kubernetes

| Herramienta | Para qué sirve |
|---|---|
| **Helm** | Gestor de paquetes de K8s: plantillas (charts) + releases versionados con rollback |
| **Kustomize** | Overlays por ambiente sin plantillas (nativo en `kubectl -k`) |
| **Argo CD / Flux** | **GitOps**: el clúster se sincroniza con lo que dice git; drift y rollback = git revert |
| **Argo Rollouts / Flagger** | Canary y blue/green con análisis automático de métricas |
| **Karpenter / Cluster Autoscaler** | Agregar/quitar nodos según pods pendientes (Karpenter: más rápido, elige tipo de instancia) |
| **HPA / VPA / KEDA** | Escalar pods por CPU/mem (HPA), ajustar requests (VPA), escalar por eventos: colas, Kafka, cron (KEDA) |
| **Ingress NGINX / AWS Load Balancer Controller / Gateway API** | Exponer servicios HTTP(S) hacia afuera |
| **cert-manager** | Emite y renueva certificados TLS (Let's Encrypt, ACM PCA) automáticamente |
| **external-dns** | Crea registros DNS (Route 53) según los Ingress/Services |
| **External Secrets Operator** | Sincroniza secretos de Secrets Manager/Vault → Secrets de K8s |
| **Istio / Linkerd** (service mesh) | mTLS entre servicios, retries, timeouts, tráfico por porcentaje, telemetría |
| **Cilium** | CNI con eBPF: red, NetworkPolicies L3-L7, observabilidad (Hubble), reemplaza kube-proxy |
| **Kyverno / OPA Gatekeeper** | Admission policies: "no imágenes `latest`", "requests obligatorios", "no root" |
| **Velero** | Backup y restore de recursos y volúmenes del clúster |
| **k9s, kubectx/kubens, stern** | Productividad: UI de terminal, cambiar contexto/namespace, logs de varios pods |

### CI/CD y supply chain

| Herramienta | Para qué sirve |
|---|---|
| **GitHub Actions / GitLab CI / Jenkins / CircleCI** | Orquestar build, test y deploy |
| **Argo CD** | Parte de CD en modelo *pull* (GitOps) |
| **SonarQube / Semgrep / CodeQL** | SAST y calidad de código |
| **Snyk / Dependabot / Renovate** | Vulnerabilidades y actualización de dependencias |
| **Trivy / Grype** | Escanear imágenes, IaC y repos |
| **gitleaks / trufflehog** | Detectar secretos commiteados |
| **Syft + cosign (Sigstore)** | Generar SBOM y firmar imágenes; verificar firma al desplegar |
| **ECR / Artifactory / Harbor** | Registry de imágenes y artefactos |

### Observabilidad

| Herramienta | Para qué sirve |
|---|---|
| **Prometheus + Alertmanager** | Métricas (pull) y alertas; estándar en K8s |
| **Grafana** | Dashboards sobre Prometheus, Loki, Tempo, CloudWatch... |
| **Loki / ELK-OpenSearch / Fluent Bit** | Logs: Fluent Bit los recolecta del nodo y los envía a Loki/OpenSearch/CloudWatch |
| **OpenTelemetry** | Estándar para instrumentar trazas/métricas/logs sin casarte con un proveedor |
| **Jaeger / Tempo / X-Ray** | Tracing distribuido |
| **Datadog / New Relic / Dynatrace** | Todo en uno SaaS (APM, logs, métricas) — más caro, menos operación |
| **PagerDuty / Opsgenie** | On-call, escalamiento de alertas |
| **Thanos / Mimir** | Prometheus a largo plazo y multi-clúster |

### Seguridad e identidad (AWS)

| Herramienta | Para qué sirve |
|---|---|
| **IAM Identity Center (SSO)** | Acceso humano a todas las cuentas con permission sets |
| **IRSA / EKS Pod Identity** | Un pod asume un rol IAM sin access keys |
| **Secrets Manager / Parameter Store / Vault** | Secretos con rotación y auditoría |
| **KMS / CloudHSM** | Cifrado con llaves gestionadas; HSM para llaves críticas (pagos) |
| **WAF + Shield** | Filtrado L7 (OWASP, rate limit, bots) y protección DDoS |
| **GuardDuty / Security Hub / Inspector / Config** | Detección de amenazas, postura centralizada, vulnerabilidades, cumplimiento de reglas |
| **CloudTrail** | Auditoría de toda llamada a la API de AWS |
| **Falco** | Detección en runtime dentro de contenedores (ej. shell abierta en un pod de prod) |

### Datos y mensajería

| Herramienta | Para qué sirve |
|---|---|
| **RDS / Aurora (PostgreSQL/MySQL)** | Transaccional; Multi-AZ, réplicas de lectura, Aurora Global para DR |
| **DynamoDB** | Clave-valor a gran escala, latencia baja; bueno para idempotencia |
| **ElastiCache (Redis)** | Cache, sesiones, rate limiting, locks distribuidos |
| **SQS / SNS / EventBridge** | Colas, pub/sub, bus de eventos — desacoplar servicios |
| **MSK (Kafka) / Kinesis** | Streaming de eventos de alto volumen, replay |
| **S3** | Objetos, backups, data lake; con Object Lock para auditoría inmutable |

---

## 2. Cómo responder "diseñá una arquitectura" (framework de 6 pasos)

No hay que saberse "la" arquitectura: hay que **mostrar un proceso**. Si
seguís siempre estos pasos, suenas senior aunque la pregunta te agarre en frío.

1. **Aclarar requisitos (2 min)** — preguntá antes de dibujar:
   - Funcionales: ¿qué hace el sistema?
   - No funcionales: tráfico (RPS/TPS), latencia, disponibilidad (99.9 vs
     99.99), RPO/RTO, regulación (PCI-DSS, datos personales), presupuesto,
     tamaño del equipo.
2. **Dibujar el camino feliz de una request** de punta a punta (usuario → DNS
   → CDN/WAF → LB → servicio → datos).
3. **Cómputo y datos**: dónde corre (EKS/ECS/Lambda) y dónde persiste (qué
   base y por qué).
4. **Las "-ilities"**: alta disponibilidad (Multi-AZ), escalado, seguridad
   (red, identidad, cifrado, secretos), observabilidad, DR.
5. **Cómo se entrega**: IaC + CI/CD + estrategia de deploy + ambientes/cuentas.
6. **Trade-offs y evolución**: "Arranco así por X; si el tráfico crece 10x
   cambiaría Y". Nombrar lo que **no** hiciste y por qué demuestra criterio.

Frases útiles:
- "Depende de ___; si es ___ haría A, si es ___ haría B."
- "Empezaría simple (ECS/Fargate) y movería a EKS cuando haya N equipos/servicios."
- "Lo gestionado primero: menos operación = menos riesgo."

---

## 3. Arquitectura de referencia: plataforma de pagos en AWS

Es el ejemplo más probable para PayU. Aprendela como "tu" arquitectura y
adaptala a lo que te pregunten.

```
                      Usuarios / comercios (API, checkout)
                                   │
                         Route 53 (DNS, health checks, failover)
                                   │
                    CloudFront + AWS WAF + Shield  (TLS, rate limit, bots)
                                   │
 ┌───────────────── Cuenta: payments-prod (Organizations / Control Tower) ─────────────────┐
 │  VPC en 3 AZs                                                                           │
 │  ┌─ Subnets públicas ─────────────────┐                                                 │
 │  │  ALB (AWS Load Balancer Controller)│   NAT Gateway por AZ                            │
 │  └──────────────┬─────────────────────┘                                                 │
 │  ┌─ Subnets privadas (apps) ─────────────────────────────────────────────────────────┐  │
 │  │  EKS (nodos con Karpenter, en 3 AZs)                                              │  │
 │  │   ├─ api-gateway / checkout-svc  ──►  payments-svc  ──►  fraud-svc                │  │
 │  │   ├─ Istio/Linkerd: mTLS entre servicios        ├─ SQS/Kafka: eventos de pago     │  │
 │  │   ├─ External Secrets (IRSA → Secrets Manager)  └─ workers de conciliación (KEDA) │  │
 │  │   └─ Fluent Bit, OTel collector, Prometheus agent                                 │  │
 │  └───────────────────────────────────────────────────────────────────────────────────┘  │
 │  ┌─ Subnets privadas (datos, sin salida a internet) ─────────────────────────────────┐  │
 │  │  Aurora PostgreSQL Multi-AZ (+ Global DB a otra región)   ElastiCache Redis       │  │
 │  │  DynamoDB (idempotency keys)     S3 (Object Lock: auditoría)   KMS / CloudHSM     │  │
 │  └───────────────────────────────────────────────────────────────────────────────────┘  │
 │  VPC endpoints (S3, ECR, Secrets Manager, STS) → el tráfico a AWS no sale a internet    │
 └─────────────────────────────────────────────────────────────────────────────────────────┘
        │ Transit Gateway                    │ logs/eventos
 Cuenta Network (egress, inspección)   Cuenta Log Archive (CloudTrail org, Config)
                                       Cuenta Security (GuardDuty, Security Hub admin)
 Cuenta Tooling/CI: GitHub Actions (OIDC) + Argo CD + ECR ─► despliega en dev / staging / prod
 Observabilidad: Prometheus/Thanos + Grafana + Loki + Tempo (o Datadog) + PagerDuty
```

### Cómo contarla (guion de ~3 minutos)

1. **Entrada**: "Route 53 con health checks; CloudFront con WAF para
   OWASP y rate limiting, Shield para DDoS. TLS termina en el borde y se
   re-cifra hacia adentro."
2. **Red**: "VPC en 3 AZs con subnets públicas solo para el ALB y los NAT;
   apps y datos en privadas; la capa de datos sin salida a internet. VPC
   endpoints para hablar con servicios de AWS sin pasar por internet."
3. **Cómputo**: "EKS con Karpenter para nodos y HPA/KEDA para pods; pods
   repartidos entre AZs con topology spread y PodDisruptionBudgets. mTLS con
   service mesh porque en pagos todo tráfico interno debe ir cifrado."
4. **Datos**: "Aurora PostgreSQL Multi-AZ para transacciones (ACID es no
   negociable en pagos), Redis para cache y rate limit, DynamoDB para claves de
   idempotencia —así un reintento del cliente no cobra dos veces—, y eventos a
   SQS/Kafka para desacoplar antifraude y conciliación."
5. **Seguridad**: "Cuenta aislada para el entorno PCI (reduce el alcance de
   la auditoría). IRSA para que los pods asuman roles sin llaves; secretos en
   Secrets Manager vía External Secrets; KMS en todo, HSM para llaves de
   tarjetas; Kyverno bloquea imágenes sin firma o que corren como root."
6. **Entrega**: "Terraform por cuenta y ambiente con pipeline plan-en-PR y
   apply con aprobación. Apps: GitHub Actions construye, escanea (Trivy), firma
   (cosign) y publica en ECR; Argo CD sincroniza y Argo Rollouts hace canary
   con análisis de métricas y rollback automático."
7. **Observabilidad**: "OpenTelemetry en las apps, métricas en Prometheus,
   logs con Fluent Bit a Loki, trazas en Tempo, todo en Grafana; alertas por
   SLO (tasa de pagos fallidos, p99 de autorización) a PagerDuty."
8. **DR**: "Multi-AZ cubre la caída de una zona. Para una región: Aurora
   Global Database (RPO de segundos) + infraestructura idéntica en la segunda
   región por Terraform (pilot light / warm standby) y failover con Route 53."
9. **Trade-offs**: "Service mesh agrega complejidad; si el equipo es chico
   empezaría con mTLS en el ALB y NetworkPolicies de Cilium. Multi-región
   activo-activo duplica costo y complica la consistencia; empezaría con
   warm standby."

### Preguntas de repregunta que te pueden hacer (y tu respuesta corta)

- **¿Cómo evitás cobrar dos veces?** → Idempotency key por request, guardada
  en DynamoDB/Postgres con constraint único; reintentos seguros.
- **¿Qué pasa si se cae una AZ?** → ALB deja de enrutar ahí, Karpenter crea
  nodos en las otras AZs, Aurora hace failover al standby (~30 s).
- **¿Cómo desplegás sin downtime?** → Rolling/canary + readiness probes +
  PDB + `preStop` hook para drenar conexiones.
- **¿Cómo controlás costos?** → Tags obligatorios, Savings Plans para la base,
  Spot para workers tolerantes a interrupción (Karpenter), rightsizing con VPA
  en recomendación, Kubecost.
- **¿Cómo sabés que está sano?** → SLOs con error budget; alertar por síntomas
  (errores, latencia) y no por causas (CPU alta).

---

## 4. Plan para ganar confianza (práctica, no solo lectura)

La confianza viene de haberlo **hecho** al menos una vez. Plan corto:

| Día | Práctica | Qué te llevás |
|---|---|---|
| 1 | Clúster local con **kind**; instalar Calico/Cilium, metrics-server, ingress-nginx | Ver con tus ojos los componentes (sección 2 del README) |
| 2 | Desplegar una app con **Helm**, romperla a propósito (imagen mala, OOM, probe mal) y diagnosticar | Troubleshooting real |
| 3 | Instalar **Argo CD** en kind y desplegar desde un repo (GitOps) | Poder contar GitOps en primera persona |
| 4 | **Terraform**: módulo de VPC + backend S3, pipeline en GitHub Actions con plan en PR | Pipeline de IaC en primera persona |
| 5 | Dibujar la arquitectura de la sección 3 **de memoria** y contarla en voz alta en 3 minutos (grabarte) | Fluidez para la entrevista |

Y pedime: "hazme una entrevista de system design" — te hago de
entrevistador con repreguntas.
