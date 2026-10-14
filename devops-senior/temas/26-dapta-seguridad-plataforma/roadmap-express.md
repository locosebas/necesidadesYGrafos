# Roadmap express — Propuesta de valor para Dapta (seguridad de infraestructura)

Mismo método que la prueba Davivienda: **de a una pregunta**, de lo general a lo específico, y en
los repasos se describe el mecanismo y **tú dices el nombre**.
Escala: ⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior (la de `../../examenes/registro/progreso.md`).

## Fase 1 — Caracterizar la necesidad → [caracterizacion.md](caracterizacion.md)

| # | Paso | Estado |
|---|---|---|
| 1.1 | Lo público (web, trust center, subprocesadores) | ✅ ver README |
| 1.2 | Lo que te contaron en la entrevista (de a una pregunta) | 🟡 en curso |
| 1.3 | Preguntas abiertas para la próxima entrevista | ⬜ |
| 1.4 | Síntesis: el problema en 3 frases | ⬜ |

## Fase 2 — Aprender lo que la propuesta necesita

| # | Tema | Nivel hoy | Meta |
|---|---|---|---|
| A1 | SOC 2: Trust Services Criteria, Type I vs. Type II, ventana de observación, bridge letter | ⬜ | 🔵 |
| A2 | ISO 27001 (SGSI, Anexo A) vs. SOC 2; ISO 42001 (gestión de IA) | ⬜ | 🟢 |
| A3 | HIPAA (BAA, Business Associate Agreement), PCI DSS para pagos por voz, GDPR / Ley 1581 | ⬜ | 🟡 |
| A4 | Compliance automation (Vanta/Drata): qué automatiza y qué no; "controles en papel" vs. evidencia continua | ⬜ | 🟢 |
| B1 | Seguridad de AWS para una startup: AWS Organizations, SCPs, IAM Identity Center, GuardDuty, Security Hub, CloudTrail | 🟡 (IAM/IRSA 🟢) | 🔵 |
| B2 | Supply chain y CI/CD: SAST/DAST, Trivy, Dependabot, secretos en GitHub, SBOM | 🟡 | 🟢 |
| B0 | **Temporal** (workflows, activities, workers, task queues, versionado) y su migración — puente: Durable Functions 🟢 (#48); material en tema 21 | ⬜ | 🟢 |
| B4 | Kubernetes seguro en AWS: EKS, GitOps (Argo CD), Pod Security Standards, NetworkPolicy, OPA/Kyverno, IRSA/Pod Identity, secretos con External Secrets — puente: K8s 🟢/🔵 (#1, #3, #50), OPA 🟢 (#42), IRSA 🟢 (#27) | 🟢 | 🔵 |
| B3 | Detección y respuesta: SIEM, runbooks, incident response (enlaza con el tema 25) | 🟡 | 🟢 |
| C1 | Seguridad de LLM y agentes de voz: OWASP Top 10 para LLM, prompt injection, guardrails, ZDR | 🟡 | 🔵 |
| C2 | Multi-tenancy y secretos por cliente (tokens OAuth de CRMs) | 🟡 | 🟢 |

## Fase 3 — La propuesta de valor

| # | Entregable | Estado |
|---|---|---|
| 3.1 | Diagnóstico: madurez actual vs. lo que piden los compradores | ⬜ |
| 3.2 | Hoja de ruta 30-60-90 días (y 6-12 meses: certificaciones) | ⬜ |
| 3.3 | Costos y esfuerzo (auditorías, herramientas, personas) | ⬜ |
| 3.4 | One-pager o presentación corta para la siguiente entrevista | ⬜ |

## Fase 4 — Defenderla

| # | Paso | Estado |
|---|---|---|
| 4.1 | Contraargumentos ("ya tenemos Vanta", "somos 14, no hay tiempo para burocracia") | ⬜ |
| 4.2 | Historia en 60 segundos | ⬜ |
| 4.3 | Simulacro de entrevista | ⬜ |
