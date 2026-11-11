# Libreto de diapositivas - CI/CD con aseguramiento de código y cloud security (HITSS para Claro)

Plan de la presentación para repasar la entrevista de HITSS (proyecto para Claro). Cada diapositiva tiene:

- `Sección`: a qué parte del proceso pertenece.
- `Diagrama`: el o los diagramas de [diagramas-c4.md](diagramas-c4.md).
- Viñetas: lo que se ve en pantalla.
- `>` guion: lo que dices en voz alta. En la presentación aparece al oprimir **N** (notas).

La presentación [presentacion.html](presentacion.html) se genera con
`python3 generar_presentacion.py` a partir de este archivo y del de diagramas. Si cambias algo aquí,
vuelve a correr el generador.

Regla de honestidad: **SonarQube** se explica como el estándar de la industria para el quality gate,
pero **no se dice que lo usaste**. Lo que sí es tuyo: Azure Pipelines, Jenkins, GitLab CI, GitHub
Actions, Argo CD, Helm, Terraform y el hardening de MercadoLibre.

---

## CI/CD con aseguramiento de código y cloud security
**Sección:** Portada
- Entrevista **HITSS** para **Claro** · noviembre 2026
- Primero, la **base** que todo CI y todo CD deben tener
- Después, los **11 pasos** del pipeline: qué **herramienta** va en cada paso y **para qué** se usa
- Diagramas C4 (Context, Containers, Components, Code) por paso
- Teclas: ← → para moverse · N para ver el guion

> Esta presentación es un mapa mental. Si recuerdas el dibujo del pipeline con sus once pasos, recuerdas qué herramienta va en cada lugar.

---

## Panorama: CI vs CD
**Sección:** Panorama
**Diagrama:** D1
- **CI (Continuous Integration)**: cada cambio se integra, compila, prueba y analiza **automáticamente**
- **CD (Continuous Delivery)**: la versión queda **lista para producción**; el paso a producción lleva **aprobación**
- **Continuous Deployment**: lo mismo, pero **sin aprobación humana**
- **DevSecOps**: la seguridad va **dentro** del pipeline (shift-left), no al final

> CI, Continuous Integration, responde a la pregunta: ¿este cambio está bien hecho? Compila, pasa las pruebas, pasa el quality gate y los escaneos de seguridad. CD, Continuous Delivery, responde: ¿esta versión puede llegar a producción de forma segura? En Continuous Delivery hay una aprobación antes de producción; en Continuous Deployment no la hay. En una empresa como Claro, con control de cambios, lo normal es Continuous Delivery.

---

## La base de un CI · Continuous Integration
**Sección:** Base
**Diagrama:** D1a
- **Control de versiones** (Git): una sola fuente de verdad para código, IaC (Infrastructure as Code) y pipeline
- **Pipeline como código** (Jenkinsfile, `.gitlab-ci.yml`, `azure-pipelines.yml`): el proceso se versiona y se revisa como el código
- **Disparo automático** en cada commit y PR (Pull Request): integrar seguido, no al final del sprint
- **Build reproducible** en runners efímeros: mismo resultado siempre (lockfiles, caché, imagen de build fija)
- **Pruebas y quality gate obligatorios**: si fallan, el pipeline se detiene
- **Secretos fuera del código**: se inyectan desde un vault o variables protegidas
- **Salida**: un **artefacto versionado e inmutable** en un registro, con **feedback en minutos**

> Antes de hablar de herramientas, esto es lo que todo CI, Continuous Integration, debe tener, sea Jenkins, GitLab CI, Azure Pipelines o GitHub Actions. Una sola fuente de verdad en Git. El pipeline escrito como código y versionado. Un disparo automático en cada commit y en cada pull request. Un build reproducible, que dé lo mismo hoy y en seis meses. Pruebas y quality gate obligatorios, que detienen el pipeline si fallan. Los secretos nunca en el código. Y una salida clara: un artefacto versionado e inmutable, con feedback al desarrollador en pocos minutos.

---

## La base de un CD · Continuous Delivery
**Sección:** Base
**Diagrama:** D1b
- **El mismo artefacto** del CI para todos los ambientes: build once, deploy anywhere
- **Ambientes como código** (IaC): stage lo más parecido posible a producción
- **Configuración externalizada**: values, variables y secretos por ambiente, fuera del artefacto
- **Despliegue automatizado y repetible**: sin pasos manuales, idealmente GitOps
- **Pruebas después del despliegue**: smoke, end-to-end y DAST (Dynamic Application Security Testing)
- **Gates y aprobaciones** con evidencia, trazabilidad y auditoría
- **Bajo riesgo**: canary o blue/green, **rollback** probado y **observabilidad** que cierra el ciclo

> Y esto es lo que todo CD, Continuous Delivery, debe tener. Se despliega el mismo artefacto que salió del CI, nunca se recompila. Los ambientes se crean con infraestructura como código, para que stage se parezca a producción. La configuración de cada ambiente vive fuera del artefacto. El despliegue es automático y repetible. Después de cada despliegue hay pruebas. Para pasar a producción hay gates y aprobaciones que dejan auditoría. Y el paso a producción es de bajo riesgo: canary o blue/green, con rollback probado y observabilidad que confirma que todo está sano.

---

## Los 11 pasos de punta a punta
**Sección:** Panorama
**Diagrama:** D2
- **CI**: 1 commit y PR · 2 build y pruebas unitarias · 3 quality gate · 4 seguridad del código · 5 imagen firmada
- **CD**: 6 IaC escaneada · 7 deploy en stage · 8 pruebas en stage · 9 gate y aprobación · 10 producción progresiva · 11 observar y rollback
- Cada paso puede **detener** el pipeline: fallar rápido y barato

> El pipeline tiene dos mitades. La mitad de CI termina con un artefacto inmutable, escaneado y firmado. La mitad de CD toma ese mismo artefacto y lo lleva por stage hasta producción. Cada paso es un control: si falla, el pipeline se detiene, y entre más temprano falla, más barato sale corregir.

---

## Regla de oro: build once, deploy anywhere
**Sección:** Panorama
**Diagrama:** D3
- La versión se crea **una sola vez**; nunca se recompila por ambiente
- Se identifica por **versión semántica + digest** de la imagen
- **Stage va unos días antes**; para pasar a producción hay que **demostrar que stage está sano**
- La configuración por ambiente va **fuera** del artefacto (values, variables, secretos)

> Así trabajábamos en Bizagi y en MercadoLibre: un paso crea la versión, el artefacto, y otro paso la despliega. Primero en stage, se deja correr unos días, se muestra la evidencia de que no hay problemas, y solo ahí va a los varios ambientes de producción. Lo que llega a producción es exactamente lo que se probó.

---

## Paso 1 · Commit y pull request
**Sección:** CI · Continuous Integration
**Diagrama:** D4
- **Git** con **trunk-based development**: ramas cortas para integrar seguido y evitar merges gigantes
- **pre-commit** hooks: corren el linter y **Gitleaks** en tu máquina para que un secreto nunca llegue al repo
- **Pull / Merge Request** (GitHub, GitLab, Azure Repos, Bitbucket): revisión de otro par y disparo del pipeline
- **Branch protection**: impide el merge si algún check está en rojo o falta la aprobación
- **CODEOWNERS**: asigna revisores obligatorios según la carpeta que se toca

> El aseguramiento empieza antes del pipeline. En la máquina del desarrollador, los pre-commit hooks corren el linter y Gitleaks para que un secreto nunca llegue al repositorio. Después, el pull request dispara el pipeline, y la branch protection impide el merge si algún check falla o si falta la revisión de otro par.

---

## Paso 2 · Build y pruebas unitarias
**Sección:** CI · Continuous Integration
**Diagrama:** D5
- **Maven, Gradle, npm, dotnet, go build**: compilar y resolver dependencias con caché, para builds rápidos y reproducibles
- **JUnit, pytest, Jest, xUnit, go test**: pruebas unitarias; si una falla, el pipeline se detiene
- **JaCoCo, Coverage.py, Istanbul/nyc**: medir la cobertura y enviarla al quality gate
- **Jenkins, GitLab CI, Azure Pipelines, GitHub Actions**: orquestar los jobs y guardar los reportes

> El build compila y corre las pruebas unitarias. Si una prueba falla, el pipeline se detiene ahí. El reporte de cobertura, por ejemplo de JaCoCo en Java, no se queda en el job: se envía al quality gate del paso siguiente. He integrado pruebas automatizadas en pipelines de Azure Pipelines, Jenkins y GitLab CI.

---

## Paso 3 · Aseguramiento de calidad: quality gate
**Sección:** CI · Continuous Integration
**Diagrama:** D6
- **SonarQube / SonarCloud**: detectar bugs, code smells, vulnerabilidades, security hotspots y duplicación
- **Quality gate**: umbral que rompe el pipeline (ej. cobertura ≥ 80 % en código nuevo, 0 bugs nuevos)
- **"Clean as you code"**: exigir solo al código nuevo, para que el legado mejore sin bloquear al equipo
- **Decoración del PR**: los hallazgos aparecen en el pull request, donde el desarrollador los ve
- **SonarLint** (en el IDE), **Codacy, Code Climate**: feedback antes del commit o alternativas a SonarQube

> El quality gate es la regla de aseguramiento de código: un umbral que, si no se cumple, rompe el pipeline. El estándar de la industria es SonarQube. La buena práctica es aplicar el quality gate solo al código nuevo, así un proyecto legado puede mejorar poco a poco sin bloquear al equipo. SonarQube lo conozco como estándar y lo estoy reforzando; lo que sí he hecho es poner checks obligatorios que bloquean el merge.

---

## Paso 4 · Seguridad del código
**Sección:** CI · Continuous Integration
**Diagrama:** D7
- **SAST** (Static Application Security Testing) · **Semgrep, Checkmarx, Fortify**: buscar inyecciones y malas prácticas en nuestro propio código
- **SCA** (Software Composition Analysis) · **Snyk, OWASP Dependency-Check, Dependabot**: encontrar CVE (Common Vulnerabilities and Exposures) en librerías de terceros y proponer la actualización
- **Gitleaks, TruffleHog**: detectar llaves y contraseñas en el código y en el historial de Git
- **SBOM** (Software Bill of Materials) · **Syft, CycloneDX**: inventario de componentes, para saber a quién afecta un CVE nuevo
- **DefectDojo**: centralizar y dar seguimiento a los hallazgos de todos los escáneres

> Se corren cuatro escaneos en paralelo. SAST revisa nuestro código buscando inyecciones o malas prácticas. SCA revisa las librerías de terceros contra bases de vulnerabilidades conocidas, los CVE. El escaneo de secretos busca llaves en el código. Y el SBOM es el inventario de todo lo que trae la aplicación. Una política define qué severidad rompe el pipeline, normalmente Critical y High.

---

## Paso 5 · Empaquetar, escanear y firmar la imagen
**Sección:** CI · Continuous Integration
**Diagrama:** D8
- **Docker** multi-stage + **distroless**: imagen final sin compiladores ni shell, menos superficie de ataque
- **Trivy, Grype**: escanear la imagen (sistema operativo y librerías); no se publica si hay Critical
- **Cosign** (Sigstore): firmar la imagen para probar que salió de nuestro pipeline
- **SLSA** (Supply-chain Levels for Software Artifacts): marco para medir qué tan confiable es la cadena de build
- **JFrog Artifactory, Nexus, Harbor, ECR, ACR**: registro versionado e inmutable de imágenes

> Este es el final de CI: la imagen se construye en varias etapas para que en producción no queden compiladores ni herramientas. Trivy la escanea; si hay vulnerabilidades críticas, no se publica. Cosign la firma, y en el clúster una política de Kyverno solo deja correr imágenes firmadas por nuestro pipeline. Eso es seguridad de la cadena de suministro.

---

## Paso 6 · Infraestructura como código segura
**Sección:** CD · Continuous Delivery
**Diagrama:** D9
- **Terraform**: describir la infraestructura como código; el **plan** se revisa en el PR antes del **apply**
- **Checkov, Trivy (antes tfsec), KICS**: detectar configuraciones inseguras (bucket público, puerto 22 abierto)
- **OPA (Open Policy Agent) / Conftest, Sentinel**: políticas como código propias de la empresa (tags, regiones, tamaños)
- **Estado remoto con bloqueo** (S3 + DynamoDB, Azure Storage): evitar que dos apply choquen y perder el estado

> La infraestructura pasa por el mismo rigor que el código. El pull request con cambios de Terraform genera el plan, Checkov o Trivy buscan configuraciones inseguras, como un bucket público o un puerto 22 abierto a internet, y una persona revisa el plan antes del apply. Esto lo hice con GitHub Actions: plan en el pull request, apply después de la aprobación.

---

## Paso 7 · Despliegue en stage con GitOps
**Sección:** CD · Continuous Delivery
**Diagrama:** D10
- **Argo CD / Flux** (GitOps): leen el estado deseado en Git y sincronizan el clúster; el pipeline no necesita credenciales del clúster
- **Helm / Kustomize**: empaquetar los manifiestos y cambiar valores por ambiente
- **Kyverno / OPA Gatekeeper** (admission control): rechazar pods sin firma, privilegiados o sin límites
- **HashiCorp Vault, AWS Secrets Manager, Azure Key Vault** + **External Secrets**: entregar secretos al clúster sin guardarlos en Git

> El pipeline no entra al clúster: solo cambia la versión en el repositorio de configuración. Argo CD ve el cambio y sincroniza. Así el pipeline no necesita credenciales del clúster, todo queda auditado en Git, y el rollback es un revert. Los secretos nunca están en Git: External Secrets los trae desde Vault o desde el gestor de secretos de la nube.

---

## Paso 8 · Pruebas en stage
**Sección:** CD · Continuous Delivery
**Diagrama:** D11
- **Smoke tests**: confirmar en segundos que la versión arrancó y responde
- **Pact, Postman/Newman**: validar contratos e integraciones entre servicios
- **Cypress, Playwright, Selenium**: pruebas end-to-end como las haría un usuario real
- **OWASP ZAP, Burp Suite** (DAST, Dynamic Application Security Testing): atacar la aplicación viva buscando lo que el análisis estático no ve
- **k6, JMeter, Gatling**: confirmar que la versión aguanta la carga esperada

> Con la aplicación corriendo en stage se prueba como lo haría un usuario. Primero smoke tests, después integración y end-to-end. En paralelo, el DAST, por ejemplo OWASP ZAP, ataca la aplicación viva buscando vulnerabilidades que el análisis estático no ve. Y las pruebas de carga confirman que la versión aguanta el tráfico. Todo eso, más unos días de métricas sanas, es la evidencia para pasar a producción.

---

## Paso 9 · Gate y aprobación a producción
**Sección:** CD · Continuous Delivery
**Diagrama:** D12a
- **Gate automático**: confirmar quality gate en verde, escaneos sin Critical/High y **firma verificada**
- **ServiceNow, Jira Service Management**: registrar la solicitud de cambio ITIL (Information Technology Infrastructure Library) con la evidencia de stage
- **CAB** (Change Advisory Board) o release manager: aprobar el paso a producción
- **Ambientes protegidos** (Azure DevOps, GitLab, GitHub environments): pausar el job de producción hasta la aprobación y dejar auditoría
- **Segregación de funciones**: quien escribe el código no aprueba su paso a producción

> El gate es el punto de control entre stage y producción. Tiene una parte automática: el quality gate en verde, los escaneos sin hallazgos Critical o High y la firma de la imagen verificada. Y tiene una parte humana: en una telco como Claro normalmente hay gestión de cambios ITIL, en ServiceNow o Jira Service Management, y el CAB aprueba con la evidencia de stage adjunta. En el pipeline eso se implementa con ambientes protegidos: en Azure DevOps, GitLab o GitHub, el job de producción espera la aprobación antes de correr.

---

## Paso 10 · Producción progresiva
**Sección:** CD · Continuous Delivery
**Diagrama:** D12b
- **Rolling, blue/green, canary**: estrategias para no exponer a todos los usuarios de golpe
- **Argo Rollouts / Flagger**: automatizar el canary 5 % → 25 % → 100 %
- **Prometheus, Datadog**: medir errores y latencia de la versión nueva contra la anterior
- **Rollback automático**: volver a la versión anterior sin esperar a una persona
- **LaunchDarkly, Unleash** (feature flags): separar el **deploy** del **release**

> Después de la aprobación, la versión no llega de golpe a todos los usuarios. Con canary empieza con el cinco por ciento del tráfico; Argo Rollouts o Flagger consultan Prometheus o Datadog y comparan errores y latencia contra la versión anterior. Si está sana, sube al veinticinco, al cincuenta y al cien por ciento. Si se degrada, Argo Rollouts hace rollback solo, sin esperar a una persona. Los feature flags permiten ir más allá: desplegar el código apagado y activarlo después, separando el deploy del release.

---

## Paso 11 · Observar y cerrar el ciclo
**Sección:** CD · Continuous Delivery
**Diagrama:** D13
- **Prometheus**: recolectar métricas de la aplicación y del clúster
- **Grafana, Datadog**: dashboards y SLO (Service Level Objective) para ver si la versión está sana
- **Alertmanager, PagerDuty, Opsgenie**: avisar al on-call cuando un SLO se está rompiendo
- **Métricas DORA** (DevOps Research and Assessment): medir el proceso de entrega: frecuencia, lead time, tasa de fallo, MTTR (Mean Time To Recovery)
- **Postmortems sin culpables**: convertir cada incidente en una mejora del pipeline

> El pipeline no termina en el deploy. La observabilidad confirma que la versión está sana, y las métricas DORA miden al propio proceso de entrega: qué tan seguido desplegamos, cuánto tarda un cambio en llegar, cuántos cambios fallan y qué tan rápido nos recuperamos. Eso es lo que le mostraría a Claro para demostrar que el proceso mejora.

---

## Cloud security por capas
**Sección:** Cloud security
**Diagrama:** D14
- **CSPM (Cloud Security Posture Management)**: Microsoft Defender for Cloud, AWS Security Hub, Prisma Cloud, Wiz
- **CWPP (Cloud Workload Protection Platform)** / runtime: **Falco**, Amazon GuardDuty, Defender for Containers
- **CNAPP (Cloud-Native Application Protection Platform)** = CSPM + CWPP + escaneos del pipeline en una sola plataforma
- Benchmarks: **CIS Benchmarks**, kube-bench; auditoría: CloudTrail, Azure Activity Log

> El pipeline protege lo que se despliega, pero la nube también hay que vigilarla en ejecución. El CSPM revisa la configuración de la cuenta contra los CIS Benchmarks, por ejemplo buckets públicos o llaves sin rotar. El CWPP vigila las cargas corriendo, por ejemplo Falco detecta si alguien abre una shell dentro de un contenedor. Las plataformas CNAPP, como Wiz o Prisma Cloud, juntan todo.

---

## Identidad del pipeline: sin llaves fijas
**Sección:** Cloud security
**Diagrama:** D15
- **OIDC (OpenID Connect)**: el job pide un token y la nube lo cambia por una **credencial temporal**
- AWS: rol IAM con **trust policy** por repo y rama · Azure: **workload identity federation**
- **Mínimo privilegio**: un rol por pipeline y por ambiente
- Cifrado con **KMS (Key Management Service)**, secretos en **Vault** o el gestor de la nube

> El riesgo más grande de un pipeline es una llave de la nube guardada como variable: si se filtra, sirve para siempre. Con OIDC el pipeline no guarda llaves: en cada ejecución pide un token, la nube valida de qué repositorio, rama y ambiente viene, y entrega una credencial que vence en minutos con el rol mínimo. En MercadoLibre hacía hardening justamente en IAM, cifrado y segmentación de red.

---

## Resumen: paso → herramienta
**Sección:** Resumen
- 1 PR: **Git, Gitleaks, branch protection** · 2 Build: **Maven/npm, JUnit/pytest, JaCoCo**
- 3 Calidad: **SonarQube** quality gate · 4 Seguridad: **Semgrep/Checkmarx, Snyk, Gitleaks, Syft**
- 5 Imagen: **Docker, Trivy, Cosign, Artifactory/Harbor** · 6 IaC: **Terraform, Checkov, OPA**
- 7 Deploy: **Argo CD, Helm, Vault, Kyverno** · 8 Pruebas: **Cypress, OWASP ZAP, k6**
- 9 Gate: **ambientes protegidos, ServiceNow, CAB** · 10 Producción: **Argo Rollouts, feature flags**
- 11 Observar: **Prometheus, Grafana, DORA**
- Nube: **Defender for Cloud / Security Hub, Falco, OIDC**

> Si me preguntan por un paso, digo el control y la herramienta: el quality gate es SonarQube, el SCA es Snyk o Dependency-Check, la imagen se escanea con Trivy y se firma con Cosign, la IaC se escanea con Checkov, el DAST es OWASP ZAP, el despliegue es GitOps con Argo CD.

---

## Mi experiencia con CI/CD
**Sección:** Mi experiencia
**Diagrama:** D16
- **Bizagi** (2022–2024): **Azure Pipelines, Jenkins y GitLab CI**, release management; **migré pipelines** de Azure Pipelines a Jenkins
- **MercadoLibre** (2024–2026): hardening y remediación de vulnerabilidades en **IAM, cifrado y segmentación de red**; Terraform en AWS y GCP
- **GitOps** con **Argo CD y Helm** desde 2022; **Terraform plan/apply por PR** en GitHub Actions
- Liderazgo de proyecto: coordinación de alcance, tiempos y áreas

> En Bizagi construí y mantuve pipelines en Azure Pipelines, Jenkins y GitLab CI, y migré pipelines de Azure Pipelines a Jenkins. Siempre con build once, deploy anywhere, stage unos días antes y varios ambientes de producción. En MercadoLibre trabajé la parte de seguridad de la infraestructura: IAM, cifrado y segmentación de red. Lo que propondría para Claro es este mismo proceso de once pasos, con los quality gates de calidad y de seguridad como controles obligatorios.
