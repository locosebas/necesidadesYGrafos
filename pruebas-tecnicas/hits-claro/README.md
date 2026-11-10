# Entrevista HITSS para Claro: CI/CD con aseguramiento de código

Entrevista con **HITSS** (cargo de perfil DevSecOps, proyecto para **Claro**), noviembre 2026. Tema
central: **construir procesos de CI/CD (Continuous Integration / Continuous Delivery) con aseguramiento
de código** (quality gates, escaneos de seguridad) y **herramientas de cloud security**. Se guarda por si
el proceso vuelve a presentarse.

> Regla de honestidad: **SonarQube** se explica como el estándar del quality gate, pero no se dice que
> lo usaste (está en la lista de estudio). Lo tuyo: Azure Pipelines, Jenkins, GitLab CI (Bizagi),
> migración de pipelines Azure Pipelines → Jenkins, GitHub Actions con Terraform plan/apply por PR,
> Argo CD y Helm, y hardening de IAM, cifrado y segmentación de red (MercadoLibre).

## Material de estudio

- [diagramas-c4.md](diagramas-c4.md): 16 diagramas C4, uno por paso del pipeline, con íconos.
- [libreto-diapositivas.md](libreto-diapositivas.md): plan de las 18 diapositivas, con el guion de cada una.
- [presentacion.html](presentacion.html): la presentación (← → para navegar, **N** para ver el guion).
  Versión para el celular (privada): https://claude.ai/artifact/R1CGvMXRR7bcUfnVfRQsD6
  Se regenera con `python3 generar_presentacion.py` después de editar el libreto o los diagramas.

## Los 11 pasos (para recitar de memoria)

CI: 1 commit y PR · 2 build y pruebas unitarias · 3 quality gate · 4 seguridad del código ·
5 imagen escaneada y firmada. CD: 6 IaC escaneada · 7 deploy en stage (GitOps) · 8 pruebas en stage ·
9 gate y aprobación · 10 producción progresiva · 11 observar y rollback.

## Nombres clave para repasar

Quality gate · SonarQube / SonarCloud · "clean as you code" · SAST (Semgrep, Checkmarx, Fortify) ·
SCA (Snyk, OWASP Dependency-Check, Dependabot) · Gitleaks / TruffleHog · SBOM (Syft, CycloneDX) ·
DefectDojo · multi-stage + distroless · Trivy / Grype · Cosign (Sigstore) · SLSA · JFrog Artifactory /
Nexus / Harbor · Checkov / KICS · OPA / Conftest / Sentinel · Argo CD / Flux · Kyverno / OPA
Gatekeeper · External Secrets + HashiCorp Vault · Pact · Cypress / Playwright / Selenium · DAST con
OWASP ZAP · k6 / JMeter · ambientes protegidos · CAB (ITIL) · canary con Argo Rollouts / Flagger ·
métricas DORA · CSPM (Defender for Cloud, Security Hub, Prisma Cloud, Wiz) · CWPP (Falco, GuardDuty) ·
CNAPP · CIS Benchmarks · OIDC / workload identity federation.
