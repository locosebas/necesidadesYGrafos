# TCS (Tata Consultancy Services) vía Adecco — Ingeniero DevOps (Azure DevOps)

Memoria para cuando Adecco o TCS vuelvan a llamar. Lee esto primero en una sesión nueva.

## Origen del proceso

- **Empresa final:** TCS (Tata Consultancy Services), consultora; el reclutamiento lo hace **Adecco**.
- **Recruiter:** Deysi Perez, Talent Acquisition Specialist de Adecco (escribió el 22 oct 2026,
  asunto "¡Queremos tu Talento Crack!").
- **Condiciones ofrecidas:** híbrido 3x2 (3 días oficina, 2 casa), Calle 26 – Av. El Dorado, Bogotá;
  contrato a término indefinido directo con TCS; medicina prepagada, escuela de idiomas y apoyo para
  certificaciones.
- **22 oct 2026:** se le respondió en el mismo hilo con la hoja de vida en PDF adjunta.
- **22 oct 2026:** Deysi pidió quitar la experiencia como Diseñador Mecánico y dejar 5 años de
  experiencia. Se reenvió la hoja de vida corregida: 5 años, Bizagi desde 2021, fechas solo con años
  (MercadoLibre 2024 – 2026, Bizagi 2021 – 2024), sin StroTech.
- **Estado:** hoja de vida corregida enviada; esperando la llamada de Adecco.

**Para la entrevista, mantener la misma versión:** 5 años de experiencia en DevOps, Bizagi desde 2021,
sin mencionar meses ni la etapa de diseño mecánico.

**Regla de tono para este proceso:** no declarar niveles bajos ni medios; presentar el perfil como
"gran capacidad" en todo el stack de la vacante.

## Qué pide la vacante (palabras clave para el ATS y la entrevista)

1. Azure DevOps
2. CI/CD (Integración y Entrega Continua)
3. YAML Pipelines (Azure Pipelines multi-stage)
4. Git
5. Estrategias de branching (GitFlow, trunk-based, release branches)
6. SonarQube
7. Quality gates
8. Gestión de releases
9. Soluciones cloud
10. DevSecOps
11. Automatización de despliegues
12. Observabilidad

## Hoja de vida

- **Documento (privado, con datos de contacto):** https://claude.ai/artifact/48zXE375nzCz3eTEQ6pCL5
  — se exporta a Word o PDF desde el mismo documento.
- Pendiente de completar antes de enviar: teléfono y enlace de LinkedIn (no van en este repo porque
  es público).
- Formato ATS: cada trabajo en 4 líneas (cargo / empresa / ciudad / fechas).

## Historias para la entrevista (ya escritas en el repo)

| Tema de la vacante | Historia | Dónde está |
|---|---|---|
| Automatización de despliegues, gestión de releases | Bizagi: de despliegue manual por escritorio remoto a Azure Pipelines + Terraform | [formulario-blossom.md §5](../../devops-senior/formularios/formulario-blossom.md#5-releasedeploy-de-manual-a-automatizado) |
| DevSecOps | Bizagi: Gitleaks detuvo un secreto en un pull request; manejo de falsos positivos | [formulario-blossom.md §6](../../devops-senior/formularios/formulario-blossom.md#6-control-de-seguridad-en-un-pipeline-y-falsos-positivos) |
| Entorno regulado / trazabilidad de releases | MercadoLibre: evidencia SOX y PCI DSS | [formulario-blossom.md §4](../../devops-senior/formularios/formulario-blossom.md#4-entorno-regulado-o-auditado) |
| Observabilidad | MercadoLibre: prueba de carga y pool de conexiones; Datadog y alertas de capacidad | [formulario-blossom.md §1](../../devops-senior/formularios/formulario-blossom.md#1-prueba-de-carga--análisis-de-performance) |
| Panorama de la carrera | Presentación StroTech → Bizagi → MercadoLibre | [presentacion.html](../../devops-senior/presentacion-experiencia/presentacion.html) |

Ojo: los valores entre **[corchetes]** de esas historias son supuestos; cámbialos por los datos reales
antes de la entrevista.

## Brecha contra `progreso.md` (al 22 oct 2026) — repasar antes de la entrevista

| # | Tema | Nivel actual | Qué repasar |
|---|---|---|---|
| 1 | CI/CD tradicional (Azure Pipelines, Jenkins) | 🟢 Sólido | Sintaxis YAML: `stages`/`jobs`/`steps`, `templates`, `variable groups`, `environments` con aprobaciones |
| 2 | Quality Gate en CI/CD | 🔴 Novato | Qué mide un quality gate de SonarQube (cobertura, bugs, vulnerabilidades, code smells, duplicación sobre código nuevo) y cómo bloquea un pull request |
| 3 | SonarQube | ⬜ Sin registrar | Integración con Azure DevOps: tareas `SonarQubePrepare` / `SonarQubeAnalyze` / `SonarQubePublish`, decoración de pull requests |
| 4 | Estrategias de branching | ⬜ Sin registrar | GitFlow vs. trunk-based vs. release branches; políticas de rama en Azure Repos |
| 5 | Observabilidad (OpenTelemetry) | 🟡 Intermedio | Azure Monitor, Application Insights, Log Analytics |
