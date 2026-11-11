# Diagramas C4 - CI/CD con aseguramiento de código y cloud security (HITSS para Claro)

Un diagrama C4 (Context, Containers, Components, Code) por idea. Están en Mermaid, así que GitHub los
dibuja directo. Los usa el [libreto](libreto-diapositivas.md) y el generador de la
[presentación](presentacion.html).

Convenciones de color (las del modelo C4):

- **Azul oscuro**: persona.
- **Azul medio**: sistema propio (la plataforma CI/CD).
- **Azul claro**: contenedor (un paso del pipeline, un servicio, un repositorio).
- **Gris**: sistema externo (herramienta de terceros).
- **Recuadro punteado**: límite (fase CI, fase CD, ambiente, capa).

Íconos: cada `ico:nombre` es el logo de la herramienta, guardado en [iconos/](iconos/) (logos de
[Iconify](https://icon-sets.iconify.design/)). En GitHub se ven como texto; en la presentación HTML se
ven como logos.

Tipos de diagrama C4 que aparecen: **Contexto**, **Contenedores**, **Componentes**, **Dinámico** (pasos
numerados en orden) y **Despliegue**.

---

## D1 · Contexto: el sistema de CI/CD y quién lo toca

Panorama. Tipo: Contexto.

```mermaid
flowchart LR
  dev["ico:account-group<br/>Desarrolladores"]:::person
  rel["ico:account<br/>Líder DevSecOps /<br/>release manager"]:::person
  cicd["ico:gitlab ico:jenkins ico:azuredevops<br/>Plataforma CI/CD<br/>pipeline con quality gates"]:::system
  repo["ico:git-icon<br/>Repositorio Git<br/>código + IaC + config"]:::ext
  sec["ico:sonarqube ico:snyk ico:trivy<br/>Calidad y seguridad<br/>SAST, SCA, imágenes, IaC"]:::ext
  reg["ico:jfrog ico:docker-icon<br/>Registro de artefactos<br/>e imágenes"]:::ext
  env["ico:kubernetes ico:aws ico:azure-icon<br/>Ambientes<br/>stage y producción"]:::ext
  obs["ico:prometheus ico:grafana ico:datadog<br/>Observabilidad"]:::ext
  dev -->|"push / pull request"| repo
  repo -->|"dispara"| cicd
  cicd -->|"analiza"| sec
  cicd -->|"publica versión"| reg
  cicd -->|"despliega la misma versión"| env
  rel -->|"aprueba la promoción"| cicd
  env -.->|"métricas y alertas"| obs
  obs -.->|"rollback / feedback"| cicd
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D2 · Dinámico: el pipeline completo de punta a punta

Panorama. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  subgraph ci["CI · Continuous Integration"]
    p1["ico:source-pull<br/>1 · Commit y PR"]:::container
    p2["ico:jest<br/>2 · Build y<br/>pruebas unitarias"]:::container
    p3["ico:sonarqube<br/>3 · Calidad<br/>quality gate"]:::container
    p4["ico:snyk<br/>4 · Seguridad del código<br/>SAST, SCA, secretos"]:::container
    p5["ico:docker-icon<br/>5 · Empaquetar, escanear<br/>y firmar"]:::container
  end
  subgraph cd["CD · Continuous Delivery"]
    p6["ico:terraform-icon<br/>6 · Infraestructura<br/>IaC escaneada"]:::container
    p7["ico:argo-icon<br/>7 · Desplegar<br/>en stage"]:::container
    p8["ico:owasp<br/>8 · Pruebas en stage<br/>e2e, DAST, carga"]:::container
    p9["ico:check-decagram<br/>9 · Gate y<br/>aprobación"]:::container
    p10["ico:swap-horizontal<br/>10 · Producción<br/>canary / blue-green"]:::container
    p11["ico:grafana<br/>11 · Observar<br/>y rollback"]:::container
  end
  p1 --> p2 --> p3 --> p4 --> p5 --> p6 --> p7 --> p8 --> p9 --> p10 --> p11
  p11 -.->|"feedback"| p1
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D3 · Despliegue: build once, deploy anywhere

Regla de oro. Tipo: Despliegue.

```mermaid
flowchart LR
  ci["ico:gitlab ico:jenkins<br/>Pipeline de CI<br/>crea la versión UNA vez"]:::system
  art["ico:package-variant-closed<br/>Artefacto inmutable<br/>app:1.4.2 + digest"]:::container
  reg["ico:jfrog<br/>Registro"]:::ext
  subgraph stg["Stage · unos días antes"]
    s["ico:kubernetes<br/>app:1.4.2"]:::container
  end
  subgraph prod["Producción · varios ambientes"]
    pa["ico:kubernetes<br/>Prod A · app:1.4.2"]:::container
    pb["ico:kubernetes<br/>Prod B · app:1.4.2"]:::container
  end
  ci --> art --> reg
  reg -->|"despliega"| s
  s -->|"stage sano = evidencia"| pa
  s -->|"stage sano = evidencia"| pb
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D4 · Componentes: paso 1, commit y pull request

CI, paso 1. Tipo: Componentes.

```mermaid
flowchart LR
  dev["ico:account<br/>Desarrollador"]:::person
  subgraph local["Estación del desarrollador"]
    pc["ico:git-icon<br/>pre-commit hooks<br/>linter + Gitleaks"]:::container
  end
  subgraph scm["Repositorio Git"]
    br["ico:source-pull<br/>Rama corta<br/>trunk-based"]:::container
    pr["ico:github-icon ico:gitlab<br/>Pull / Merge Request"]:::container
    bp["ico:lock<br/>Branch protection<br/>revisores + checks obligatorios"]:::container
  end
  ci["ico:jenkins ico:azuredevops<br/>Pipeline de CI"]:::system
  dev --> pc --> br --> pr
  pr -->|"dispara"| ci
  ci -->|"estado de los checks"| bp
  bp -->|"permite merge solo si todo pasa"| pr
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D5 · Componentes: paso 2, build y pruebas unitarias

CI, paso 2. Tipo: Componentes.

```mermaid
flowchart LR
  src["ico:file-code<br/>Código fuente"]:::ext
  subgraph job["Job de build"]
    dep["ico:package-variant-closed<br/>Dependencias<br/>con caché"]:::container
    cmp["ico:server<br/>Compilar<br/>Maven, Gradle, npm, dotnet"]:::container
    ut["ico:jest ico:test-tube<br/>Pruebas unitarias<br/>JUnit, pytest, Jest"]:::container
    cov["ico:chart-line<br/>Cobertura<br/>JaCoCo, Coverage.py, Istanbul"]:::container
  end
  rep["ico:sonarqube<br/>Reportes al<br/>quality gate"]:::ext
  src --> dep --> cmp --> ut --> cov --> rep
  ut -.->|"si falla, el pipeline se detiene"| src
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D6 · Componentes: paso 3, quality gate de calidad

CI, paso 3. Tipo: Componentes.

```mermaid
flowchart LR
  ci["ico:jenkins ico:gitlab<br/>Pipeline"]:::system
  subgraph sq["SonarQube / SonarCloud"]
    an["ico:magnify-scan<br/>Análisis estático<br/>bugs, code smells,<br/>vulnerabilidades, hotspots"]:::container
    cv["ico:chart-line<br/>Cobertura y<br/>duplicación"]:::container
    qg["ico:check-decagram<br/>Quality gate<br/>sobre el código nuevo"]:::container
  end
  pr["ico:source-pull<br/>Pull request<br/>decoración con hallazgos"]:::ext
  ci -->|"sonar-scanner"| an
  ci -->|"reporte de cobertura"| cv
  an --> qg
  cv --> qg
  qg -->|"pasa / falla"| ci
  qg -.->|"comenta"| pr
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D7 · Componentes: paso 4, seguridad del código

CI, paso 4. Tipo: Componentes.

```mermaid
flowchart LR
  ci["ico:gitlab ico:github-actions<br/>Pipeline"]:::system
  subgraph sc["Escaneos de seguridad en paralelo"]
    sast["ico:checkmarx ico:sonarqube<br/>SAST<br/>Semgrep, Checkmarx, Fortify"]:::container
    sca["ico:snyk ico:dependabot<br/>SCA dependencias<br/>Snyk, Dependency-Check, Dependabot"]:::container
    sec["ico:key-chain<br/>Secretos en el código<br/>Gitleaks, TruffleHog"]:::container
    sbom["ico:file-certificate<br/>SBOM<br/>Syft, CycloneDX"]:::container
  end
  pol["ico:shield-check<br/>Política de severidad<br/>falla con Critical / High"]:::container
  dd["ico:bug-check<br/>DefectDojo<br/>consolida hallazgos"]:::ext
  ci --> sast & sca & sec & sbom
  sast & sca & sec --> pol
  pol -->|"pasa / falla"| ci
  pol -.-> dd
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D8 · Dinámico: paso 5, imagen y cadena de suministro

CI, paso 5. Tipo: Dinámico.

```mermaid
flowchart LR
  b["ico:docker-icon<br/>1 · docker build<br/>multi-stage, distroless"]:::container
  t["ico:trivy<br/>2 · Escanear imagen<br/>Trivy, Grype"]:::container
  s["ico:file-certificate<br/>3 · Firmar + atestar<br/>Cosign, SBOM, SLSA"]:::container
  r["ico:jfrog<br/>4 · Publicar con versión<br/>Artifactory, Nexus, Harbor,<br/>ECR, ACR"]:::ext
  k["ico:kubernetes ico:shield-check<br/>5 · Clúster verifica la firma<br/>Kyverno, Gatekeeper"]:::container
  b --> t --> s --> r --> k
  t -.->|"Critical: no se publica"| b
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D9 · Dinámico: paso 6, infraestructura como código segura

CD, paso 6. Tipo: Dinámico.

```mermaid
flowchart LR
  pr["ico:source-pull<br/>1 · PR con cambios<br/>en Terraform"]:::container
  pl["ico:terraform-icon<br/>2 · terraform plan"]:::container
  sc["ico:trivy ico:shield-check<br/>3 · Escaneo IaC<br/>Checkov, tfsec/Trivy, KICS"]:::container
  op["ico:shield-check<br/>4 · Políticas como código<br/>OPA/Conftest, Sentinel"]:::container
  rv["ico:account-group<br/>5 · Revisión humana<br/>del plan"]:::person
  ap["ico:terraform-icon<br/>6 · terraform apply<br/>estado remoto con bloqueo"]:::container
  pr --> pl --> sc --> op --> rv --> ap
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D10 · Contenedores: paso 7, despliegue GitOps en stage

CD, paso 7. Tipo: Contenedores.

```mermaid
flowchart LR
  ci["ico:gitlab ico:jenkins<br/>Pipeline<br/>actualiza la versión"]:::system
  cfg["ico:git-icon ico:helm<br/>Repo de configuración<br/>Helm values / Kustomize"]:::container
  subgraph stage["Clúster de stage"]
    argo["ico:argo-icon<br/>Argo CD / Flux<br/>pull y sincroniza"]:::container
    adm["ico:shield-check<br/>Admission control<br/>Kyverno / OPA Gatekeeper"]:::container
    app["ico:kubernetes<br/>App desplegada"]:::container
    eso["ico:key-chain<br/>External Secrets"]:::container
  end
  vault["ico:aws-secrets-manager ico:key-chain<br/>Vault, Secrets Manager,<br/>Key Vault"]:::ext
  ci -->|"commit de la nueva etiqueta"| cfg
  argo -->|"lee el estado deseado"| cfg
  argo --> adm --> app
  eso -->|"lee secretos"| vault
  eso -.->|"inyecta"| app
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D11 · Componentes: paso 8, pruebas en stage

CD, paso 8. Tipo: Componentes.

```mermaid
flowchart LR
  app["ico:kubernetes<br/>App en stage"]:::system
  subgraph pruebas["Suite de pruebas contra stage"]
    smk["ico:check-decagram<br/>Smoke tests"]:::container
    int["ico:test-tube<br/>Integración y contratos<br/>Pact, Postman/Newman"]:::container
    e2e["ico:cypress-icon ico:selenium<br/>End-to-end<br/>Cypress, Playwright, Selenium"]:::container
    dast["ico:owasp<br/>DAST<br/>OWASP ZAP, Burp Suite"]:::container
    perf["ico:timer-sand<br/>Carga y rendimiento<br/>k6, JMeter, Gatling"]:::container
  end
  ev["ico:chart-line<br/>Evidencia<br/>stage sano por días"]:::ext
  app --> smk --> int --> e2e
  app --> dast
  app --> perf
  e2e & dast & perf --> ev
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D12a · Dinámico: paso 9, gate y aprobación

CD, paso 9. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  subgraph stg["Stage"]
    ev["ico:chart-line<br/>1 · Evidencia de stage<br/>pruebas + días de métricas sanas"]:::container
  end
  gate["ico:check-decagram<br/>2 · Gate automático<br/>quality gate, escaneos,<br/>firma verificada"]:::system
  chg["ico:file-certificate<br/>3 · Solicitud de cambio<br/>ITIL: ServiceNow, Jira SM"]:::ext
  cab["ico:account-group<br/>4 · Aprobación<br/>CAB / release manager"]:::person
  env["ico:azuredevops ico:gitlab ico:github-actions<br/>5 · Ambiente protegido<br/>approvals, checks, ventana de cambio"]:::system
  prod["ico:kubernetes<br/>6 · Libera el<br/>despliegue a producción"]:::container
  ev --> gate --> chg --> cab --> env --> prod
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D12b · Dinámico: paso 10, producción progresiva

CD, paso 10. Tipo: Dinámico (pasos numerados).

```mermaid
flowchart LR
  argo["ico:argo-icon<br/>1 · Argo Rollouts / Flagger<br/>inicia el canary"]:::system
  can["ico:swap-horizontal<br/>2 · Canary<br/>5% → 25% → 50% → 100%"]:::container
  ff["ico:key-chain<br/>Feature flags<br/>LaunchDarkly, Unleash"]:::ext
  ana["ico:prometheus ico:datadog<br/>3 · Análisis automático<br/>errores y latencia vs. versión anterior"]:::container
  ok["ico:check-decagram<br/>4a · Promover<br/>al 100%"]:::container
  rb["ico:alert<br/>4b · Rollback automático<br/>a la versión anterior"]:::container
  argo --> can --> ana
  ff -.->|"activa la funcionalidad<br/>sin redesplegar"| can
  ana -->|"sano"| ok
  ana -->|"degradado"| rb
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D13 · Contenedores: paso 11, observar y cerrar el ciclo

CD, paso 11. Tipo: Contenedores.

```mermaid
flowchart LR
  prod["ico:kubernetes<br/>Producción"]:::system
  subgraph o11y["Observabilidad"]
    met["ico:prometheus<br/>Métricas<br/>Prometheus"]:::container
    dash["ico:grafana ico:datadog<br/>Dashboards y SLO<br/>Grafana, Datadog"]:::container
    al["ico:alert<br/>Alertas<br/>on-call"]:::container
  end
  dora["ico:chart-line<br/>Métricas DORA<br/>frecuencia, lead time,<br/>tasa de fallo, MTTR"]:::ext
  team["ico:account-group<br/>Equipo<br/>postmortem y mejora"]:::person
  prod --> met --> dash --> al --> team
  dash --> dora --> team
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D14 · Contenedores: cloud security por capas

Cloud security. Tipo: Contenedores.

```mermaid
flowchart TB
  subgraph c1["1 · Código y dependencias"]
    a1["ico:sonarqube ico:snyk<br/>SAST, SCA, secretos"]:::container
  end
  subgraph c2["2 · Cadena de suministro"]
    a2["ico:trivy ico:file-certificate<br/>Escaneo de imágenes, firma, SBOM"]:::container
  end
  subgraph c3["3 · Infraestructura como código"]
    a3["ico:terraform-icon ico:shield-check<br/>Checkov, Trivy, OPA"]:::container
  end
  subgraph c4["4 · Postura de la nube · CSPM"]
    a4["ico:cloud-lock ico:radar<br/>Defender for Cloud, Security Hub,<br/>Prisma Cloud, Wiz"]:::container
  end
  subgraph c5["5 · Runtime · CWPP"]
    a5["ico:falco ico:kubernetes<br/>Falco, GuardDuty,<br/>Defender for Containers"]:::container
  end
  subgraph c6["6 · Identidad y secretos"]
    a6["ico:aws-iam ico:aws-kms ico:key-chain<br/>IAM mínimo privilegio, OIDC,<br/>Vault, KMS"]:::container
  end
  a1 --> a2 --> a3 --> a4 --> a5
  a6 -.->|"atraviesa todas las capas"| a3
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D15 · Dinámico: el pipeline sin llaves fijas (OIDC)

Cloud security. Tipo: Dinámico.

```mermaid
flowchart LR
  job["ico:github-actions ico:gitlab<br/>1 · Job del pipeline<br/>pide un token OIDC"]:::system
  idp["ico:lock<br/>2 · Proveedor OIDC<br/>de la plataforma CI"]:::ext
  sts["ico:aws-iam ico:azure-icon<br/>3 · AWS STS / Entra ID<br/>valida repo, rama, ambiente"]:::ext
  cred["ico:key-chain<br/>4 · Credencial temporal<br/>minutos, rol mínimo"]:::container
  cloud["ico:aws ico:azure-icon<br/>5 · Despliega en la nube"]:::ext
  job --> idp --> sts --> cred --> cloud
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```

## D16 · Contexto: mi experiencia con CI/CD

Mi experiencia. Tipo: Contexto.

```mermaid
flowchart LR
  yo["ico:account<br/>Sebastián Díaz<br/>DevOps / Infraestructura cloud"]:::person
  subgraph biz["Bizagi · ene 2022 - jun 2024"]
    b1["ico:azuredevops ico:jenkins ico:gitlab<br/>CI/CD y release management<br/>migración Azure Pipelines → Jenkins"]:::system
  end
  subgraph meli["MercadoLibre · jun 2024 - ago 2026"]
    m3["ico:aws-iam ico:aws-kms<br/>Hardening: IAM, cifrado,<br/>segmentación de red"]:::system
    m4["ico:terraform-icon ico:aws<br/>Terraform en AWS y GCP"]:::system
  end
  subgraph ambas["Desde 2022"]
    m1["ico:github-actions ico:terraform-icon<br/>Terraform plan/apply por PR<br/>en GitHub Actions"]:::system
    m2["ico:argo-icon ico:helm<br/>GitOps con Argo CD y Helm"]:::system
    m5["ico:test-tube<br/>Pruebas automatizadas<br/>integradas al pipeline"]:::system
  end
  yo --> b1
  yo --> m3
  yo --> m4
  yo --> m1
  yo --> m2
  yo --> m5
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#8a8a8a,stroke:#6b6b6b,color:#fff
```
