# Formulario Blossom — respuestas preparadas

Respuestas armadas para el formulario de aplicación de **Blossom**
(sesión del 2026-10-13). En cada pregunta se eligió la **primera opción**
(versión A) de las que se propusieron.

> ⚠️ **Antes de enviar o de la entrevista**: todo lo que está entre
> **[corchetes]** son supuestos — cámbialos por lo que realmente pasó
> (herramientas, cifras, plazos). Si no tienes el dato exacto, usa una
> aproximación honesta ("alrededor de"). En la entrevista te pueden
> repreguntar cualquier detalle, así que la historia tiene que ser tuya.

## Índice

1. [Prueba de carga / análisis de performance](#1-prueba-de-carga--análisis-de-performance)
2. [Vulnerabilidad encontrada en una app web o API](#2-vulnerabilidad-encontrada-en-una-app-web-o-api)
3. [Herramientas usadas en proyectos reales](#3-herramientas-usadas-en-proyectos-reales)
4. [Entorno regulado o auditado](#4-entorno-regulado-o-auditado)
5. [Release/deploy de manual a automatizado](#5-releasedeploy-de-manual-a-automatizado)
6. [Control de seguridad en un pipeline y falsos positivos](#6-control-de-seguridad-en-un-pipeline-y-falsos-positivos)

---

## 1. Prueba de carga / análisis de performance

**Pregunta:** Cuéntanos de una prueba de carga o un análisis de performance
que hayas diseñado: qué simulaste, qué encontraste y qué cambió después.

**Respuesta (MercadoLibre, Kubernetes — formato STAR):**

```
En MercadoLibre operábamos un servicio [de APIs internas] sobre Kubernetes en AWS, con picos fuertes de tráfico en eventos como [Hot Sale / Black Friday]. Antes de uno de esos eventos queríamos saber si el servicio aguantaba [3x] el tráfico normal sin degradar la latencia.

Qué simulé: diseñé una prueba de carga con [k6] y tres perfiles:
- Ramp-up gradual, para encontrar el punto donde el p95 de latencia se salía del SLO de [300 ms].
- Spike, para ver si el HPA (Horizontal Pod Autoscaler) reaccionaba a tiempo.
- Soak de [1 hora], para detectar fugas de memoria o agotamiento de conexiones.
Antes de correrla definí la hipótesis: el cuello de botella iba a estar en la CPU de los pods.

Qué encontré: la hipótesis estaba equivocada, y eso fue lo valioso. La CPU nunca pasó del [60%], pero desde unos [800 RPS] el p99 saltaba a [2 segundos] y aparecían errores 5xx. Cruzando métricas de Prometheus/Grafana con los logs vi que el problema era el pool de conexiones a la base de datos: cada pod tenía [10] conexiones, y cuando el HPA escalaba más pods, la base de datos llegaba a su límite de conexiones y los requests quedaban en cola. Escalar más pods empeoraba el problema.

Qué cambió después:
1. Ajusté el tamaño del pool por pod y puse un connection pooler [PgBouncer / ProxySQL] delante de la base de datos.
2. Cambié la métrica del HPA: dejó de mirar solo CPU y pasó a mirar [requests concurrentes / latencia].
3. Subí el mínimo de réplicas antes del evento para no depender del escalado en frío.
Repetí la misma prueba: el servicio aguantó [1.500 RPS] con p95 por debajo de [250 ms] y cero errores. Además dejamos la prueba de carga como paso del pipeline antes de cada evento grande.

Aprendizaje: escalar horizontalmente no sirve si el recurso compartido de atrás no escala igual. Desde entonces, en cada prueba de carga miro primero la saturación de dependencias (base de datos, colas, APIs externas), no solo CPU y memoria del servicio.
```

**Para la entrevista:** 90 segundos a 2 minutos, con números, y sin saltarse
el cierre de aprendizaje.

---

## 2. Vulnerabilidad encontrada en una app web o API

**Pregunta:** Cuéntanos de una vulnerabilidad que hayas encontrado tú en una
aplicación web o API (sin detalles confidenciales): cómo la encontraste y
cómo explicaste el riesgo.

**Concepto clave:** **BOLA (Broken Object Level Authorization)**, también
conocida como **IDOR (Insecure Direct Object Reference)** — #1 del OWASP API
Security Top 10. La API valida **quién** eres (autenticación, el JWT) pero no
si **ese objeto** te pertenece (autorización a nivel de objeto).

**Respuesta (formato STAR):**

```
En [Bizagi / MercadoLibre / AgroTec] teníamos una API REST que exponía [pedidos / documentos de clientes], protegida con OIDC: cada request traía un JWT válido emitido por [Keycloak / Entra ID].

Cómo la encontré: estaba [revisando un pull request / depurando un bug / armando pruebas de integración] y noté que el endpoint GET /orders/{id} validaba bien el JWT —quién eras— pero no comprobaba si ese pedido era tuyo. Lo verifiqué en un ambiente de pruebas con dos usuarios de prueba: con el token del usuario A pedí un id del usuario B y la API devolvió el pedido completo. Además los ids eran secuenciales, así que bastaba ir sumando uno para recorrer los pedidos de todos los clientes. Un BOLA, o IDOR, de manual.

Cómo expliqué el riesgo, en tres capas según el público:
1. Impacto, para negocio y producto: cualquier cliente con una cuenta normal podía descargar [nombres, direcciones, datos de pedido] de todos los demás clientes con un script sencillo. Fuga de datos personales con implicaciones legales [Ley 1581 / GDPR] y de reputación.
2. Probabilidad: alta, porque no hacía falta ninguna herramienta especial, solo una cuenta válida y cambiar un número en la URL.
3. Causa raíz y solución, para el equipo técnico: el JWT resolvía autenticación, pero faltaba la autorización a nivel de objeto. Propuse validar en el backend que el owner_id del recurso coincidiera con el sub del JWT, usar UUIDs en vez de ids secuenciales como defensa adicional, y agregar un test automatizado de BOLA en CI.
Lo clasifiqué como [alta / crítica], lo reporté por el canal privado del equipo y llevé la propuesta de solución lista, no solo el problema.

Qué cambió: el fix salió en [2 días], revisamos los logs de acceso para confirmar que [no había evidencia de explotación], y el chequeo de autorización pasó a ser un middleware común para todos los endpoints, más un test de BOLA en CI. Cubrimos la clase entera de vulnerabilidad, no solo ese endpoint.

Aprendizaje: autenticación y autorización son controles distintos; un JWT válido solo dice quién es el usuario, no qué puede ver. Y un riesgo se prioriza más rápido cuando lo explicas como "quién puede hacer qué, con qué esfuerzo y qué perdemos", no con jerga de seguridad.
```

**Para la entrevista:** decir "lo verifiqué en un ambiente de pruebas con
usuarios de prueba" (nunca "hackeé" ni producción), y mencionar canal privado
y revisión de logs (divulgación responsable).

---

## 3. Herramientas usadas en proyectos reales

**Pregunta:** ¿Qué herramientas has usado en proyectos reales? (CI/CD,
seguridad, carga y observabilidad, nube e infraestructura).

> Antes de enviar, **borra las que no hayas usado de verdad** — la pregunta
> dice "en proyectos reales". Según el CV, las confirmadas son: Azure DevOps,
> Jenkins, Terraform, Docker, Kubernetes, AWS (incl. Lambda), Azure, GCP,
> Prometheus, Grafana, Keycloak, Entra ID/Azure AD, AWS IAM, Python,
> PowerShell.

```
CI/CD: GitHub Actions, GitLab CI, Jenkins, Azure DevOps (Azure Pipelines), CircleCI, Bitbucket Pipelines, TeamCity, AWS CodePipeline/CodeBuild, Google Cloud Build, Tekton

GitOps y despliegue: Argo CD, Flux, Argo Rollouts, Flagger, Spinnaker, Helm, Kustomize, LaunchDarkly, Unleash

Infraestructura como código: Terraform, OpenTofu, Terragrunt, Bicep, ARM Templates, AWS CloudFormation, AWS CDK, Pulumi, Crossplane, Ansible, Chef, Puppet, Packer

Contenedores y orquestación: Docker, Podman, containerd, Kubernetes, EKS, AKS, GKE, Azure Container Apps, AWS ECS/Fargate, Google Cloud Run, KEDA, Karpenter, Istio, Linkerd, ACR, ECR, Harbor, Artifact Registry

Nube: AWS, Azure, GCP, AWS Lambda, Azure Functions/Durable Functions, Google Cloud Functions, AWS Step Functions

Seguridad: SonarQube, Snyk, Trivy, Semgrep, OWASP ZAP, Burp Suite, CodeQL, Checkmarx, Fortify, Dependabot, Renovate, OWASP Dependency-Check, Mend, Nuclei, Grype, Clair, Docker Scout, Checkov, tfsec, KICS, Terrascan, Gitleaks, TruffleHog, GitHub Secret Scanning, Cosign/Sigstore, Syft (SBOM), SLSA, OPA/Gatekeeper, Kyverno, Falco, Microsoft Defender for Cloud, AWS GuardDuty, Wiz, Prisma Cloud

Identidad y secretos: Keycloak, Microsoft Entra ID (Azure AD), AWS IAM, Okta, Auth0, HashiCorp Vault, Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, External Secrets Operator, Sealed Secrets

Carga y performance: k6, JMeter, Gatling, Locust, Artillery, Vegeta, wrk, hey, Azure Load Testing, Distributed Load Testing on AWS

Observabilidad: Datadog, Grafana, Prometheus, OpenTelemetry, Thanos, Mimir, VictoriaMetrics, ELK/Elastic Stack, Loki, Fluentd/Fluent Bit, Splunk, Jaeger, Tempo, Zipkin, New Relic, Dynatrace, Elastic APM, Azure Monitor/Application Insights/Log Analytics, AWS CloudWatch/X-Ray, Google Cloud Operations, Alertmanager, PagerDuty, Opsgenie

Chaos engineering: Chaos Mesh, LitmusChaos, AWS Fault Injection Service, Azure Chaos Studio

Datos y mensajería: Kafka, RabbitMQ, AWS SQS/SNS, Azure Service Bus/Event Hubs, Google Pub/Sub, PostgreSQL, MySQL, Redis, MongoDB, Cosmos DB, DynamoDB, Temporal, Airflow

Platform Engineering: Backstage, Port, Crossplane

IA / MLOps / LLMOps: MLflow, Kubeflow, SageMaker, Azure ML, Vertex AI, vLLM, KServe, Ollama, LangChain, LlamaIndex, MCP, pgvector, Pinecone, Qdrant, Azure AI Search, Langfuse, LangSmith, Promptfoo

Lenguajes y scripting: Python, FastAPI, PowerShell, Bash, Go, YAML, HCL
```

---

## 4. Entorno regulado o auditado

**Pregunta:** ¿Has trabajado en un entorno regulado o auditado (banca,
seguros, salud)? Si es así, ¿qué te tocaba entregar o demostrar en las
auditorías?

**Respuesta (MercadoLibre — SOX y PCI DSS):**

```
Sí. En MercadoLibre trabajé en un entorno auditado: la compañía cotiza en bolsa en Estados Unidos, así que aplican controles SOX (Sarbanes-Oxley), y en lo relacionado con pagos aplica PCI DSS. Mi rol no era el de auditor: me tocaba generar y entregar la evidencia técnica de los controles de la plataforma. Concretamente:

1. Gestión de cambios: demostrar que ningún cambio llegaba a producción sin revisión. La evidencia eran los pull requests con aprobación de una persona distinta al autor (segregación de funciones), el historial del pipeline de CI/CD que conectaba cada despliegue con su ticket y su commit, y la infraestructura en Terraform, versionada en Git.
2. Control de accesos: listados de quién tenía acceso a qué en [AWS IAM / Kubernetes], revisiones periódicas de accesos [trimestrales], evidencia de MFA y de que las cuentas de quienes salían de la empresa se desactivaban a tiempo.
3. Protección de datos: evidencia de cifrado en reposo y en tránsito (KMS, certificados TLS), de rotación de llaves y secretos, y de que los secretos no vivían en el código.
4. Logs y trazabilidad: demostrar que los logs de auditoría existían, eran inmutables y se retenían el tiempo exigido [1 año].
5. Gestión de vulnerabilidades: reportes de escaneo de [imágenes de contenedores / dependencias] y evidencia de que los hallazgos críticos se corregían dentro del SLA [15 días].
6. Continuidad: evidencia de backups y de pruebas de restauración, no solo de que el backup existía.

Lo que mejoré: al principio esa evidencia se armaba a mano, con capturas de pantalla, justo antes de cada auditoría. Ayudé a [automatizar la recolección: reportes generados desde el pipeline, exportes de IAM programados, dashboards en Grafana], para que la evidencia se produjera de forma continua y la auditoría dejara de ser un incendio de dos semanas.

Aprendizaje: en un entorno regulado, la plataforma tiene que dejar evidencia como efecto secundario. Si el pipeline, la IaC y el control de accesos están bien hechos, la auditoría se responde exportando datos, no reconstruyendo historia.
```

**Vocabulario útil:** segregación de funciones (SoD), compliance as code
(Azure Policy, AWS Config, OPA), PCI DSS y SOX (banca), Superintendencia
Financiera (Colombia), HIPAA y Ley 1581 (salud/datos), ISO 27001 y SOC 2
(transversales).

---

## 5. Release/deploy de manual a automatizado

**Pregunta:** Cuéntanos de un proceso de release o deploy que hayas llevado
de manual (o casi manual) a automatizado: cómo estaba, qué hiciste tú
directamente y qué cambió (tiempos, fallos, frecuencia).

**Respuesta (Bizagi — Azure DevOps + Terraform):**

```
En Bizagi, el despliegue de [la plataforma / los ambientes de clientes] en Azure era casi manual. Un ingeniero entraba por escritorio remoto a los servidores, copiaba los paquetes de la versión, ejecutaba scripts sueltos en orden y ajustaba a mano la configuración de cada ambiente (dev, QA, producción). Un release tomaba alrededor de [4 horas], se hacía [cada 2-4 semanas] en ventanas nocturnas y cerca de [1 de cada 4] despliegues tenía algún problema por pasos olvidados o configuraciones distintas entre ambientes. Hacer rollback era volver a repetir el proceso a mano, [1-2 horas].

Lo que hice yo directamente:
1. Documenté el proceso real paso a paso con quienes lo ejecutaban, porque nadie tenía la lista completa, y separé lo que era igual en todos los ambientes de lo que cambiaba.
2. Diseñé y construí el pipeline en Azure DevOps (Azure Pipelines) en etapas: build, pruebas automáticas, publicación del artefacto versionado y despliegue por ambiente (dev → QA → producción), con aprobación manual solo antes de producción.
3. Pasé la infraestructura a Terraform, para que los ambientes se crearan iguales y dejara de existir la "configuración que solo estaba en un servidor".
4. Convertí los scripts sueltos en scripts de PowerShell/Python idempotentes y parametrizados por ambiente, y saqué los secretos a [Azure Key Vault / variables seguras del pipeline].
5. Agregué un smoke test después del despliegue y el rollback automático a la versión anterior del artefacto si fallaba.

Resultados:
- Tiempo de despliegue: de ~[4 horas] a ~[20 minutos], sin intervención manual salvo la aprobación.
- Frecuencia: de [cada 2-4 semanas] a [varias veces por semana], y sin ventana nocturna para los ambientes no productivos.
- Fallos en despliegue: de ~[25%] a menos de [5%], y los que ocurrían se detectaban en QA, no en producción.
- Rollback: de [1-2 horas] a [unos minutos].

Lo que aprendí: el mayor problema no era la lentitud sino la variación entre ambientes. Al volver todo código (pipeline + Terraform + scripts idempotentes), el despliegue dejó de depender de quién lo ejecutaba, y eso es lo que permitió desplegar más seguido con menos riesgo.
```

**Repreguntas probables:** lo más difícil (resistencia al cambio / pasos no
documentados); cómo se midieron los números (historial de Azure Pipelines,
tickets); por qué aprobación manual antes de producción (control de cambios
/ auditoría). Conectar con las **métricas DORA**: frecuencia de despliegue,
lead time, tasa de fallos en cambios y MTTR.

---

## 6. Control de seguridad en un pipeline y falsos positivos

**Pregunta:** ¿Qué control de seguridad has puesto en un pipeline que haya
detenido algo real? ¿Cómo manejaste los falsos positivos?

**Respuesta (continuación de la pregunta 5 — Gitleaks en Azure DevOps):**

```
Sobre el mismo pipeline de Azure DevOps que automaticé en Bizagi, agregué una etapa de seguridad que corría en cada pull request y antes de cada despliegue:
- Detección de secretos con [Gitleaks] sobre el código y los scripts de despliegue.
- Análisis de dependencias (SCA) con [Snyk / OWASP Dependency-Check] y escaneo de imágenes de contenedor con [Trivy].
- Escaneo de la infraestructura en Terraform con [Checkov / tfsec].

Lo que detuvo algo real:
A las [pocas semanas], Gitleaks bloqueó un pull request que traía, dentro de un script de PowerShell de despliegue, [la cadena de conexión de una cuenta de Azure Storage / un token SAS] de un ambiente [de QA con datos de un cliente]. El desarrollador lo había puesto "temporalmente" para probar. El pipeline frenó el merge, así que el secreto nunca llegó a la rama principal ni a producción.
Igual lo traté como secreto comprometido, porque ya estaba en el historial de la rama y en el servidor de Git: roté la llave en Azure, moví el valor a Azure Key Vault, cambié el script para leerlo desde ahí con [la identidad del pipeline / Managed Identity] y revisé los logs de la cuenta de Storage para confirmar que no hubiera accesos raros. Ese caso me sirvió para que el equipo entendiera por qué el control existía.

Cómo manejé los falsos positivos:
1. Arranqué en modo "solo reporte" durante [2-3 semanas], sin bloquear, para medir cuánto ruido había antes de afectar a los equipos.
2. Tomé una línea base (baseline) de los hallazgos que ya existían: el pipeline bloqueaba solo hallazgos NUEVOS, y lo heredado quedó como deuda con dueño y fecha.
3. Ajusté los umbrales: bloquear solo críticos y altos que tuvieran corrección disponible; lo demás quedaba como advertencia.
4. Las excepciones se hacían en un archivo versionado en el repositorio (por ejemplo .gitleaksignore o la lista de supresiones del scanner), siempre por pull request, con justificación, aprobación de [seguridad / un líder técnico] y fecha de vencimiento. Así nadie apagaba el control por su cuenta y quedaba trazabilidad para auditoría.
5. Afiné las reglas con los falsos positivos repetidos (por ejemplo, valores de ejemplo en tests o hashes que parecían llaves) en vez de suprimirlos uno a uno.

Resultado: los falsos positivos bajaron de ~[40%] de los bloqueos al principio a menos de [10%], los equipos dejaron de pedir que se quitara el control, y en [X meses] no volvió a llegar ningún secreto a la rama principal.

Lo que aprendí: un control de seguridad solo sirve si los equipos confían en él. Si bloquea por ruido, lo terminan saltando; por eso medir y calibrar los falsos positivos es parte del control, no un extra.
```

**Repreguntas probables:** por qué rotar si nunca llegó a main (quedó en el
historial y en el servidor → se considera comprometido); quién aprobaba las
excepciones (alguien distinto a quien las pedía → segregación de funciones);
cómo evitar que el secreto llegue al servidor de Git (pre-commit hook de
Gitleaks + push protection, con el pipeline como segunda barrera).
