# Gap Analysis — perfil actual vs. vacante Chaos & Resilience Engineer (Davivienda)

Fuente de los requisitos: publicación en Magneto365, "Especialista II
Confiabilidad" — título real del rol: **Chaos & Resilience Engineer**,
Davivienda (Grupo Bolívar), Bogotá. 2026-09-11.
https://www.magneto365.com/co/empresas/davivienda/empleos/especialista-ii-confiabilidad-1042574

> Este análisis es específico de esa vacante puntual. Es la **segunda**
> vacante concreta usada como referencia en este repo — ver
> `gap-analysis.md` para la primera (Azure Platform Engineer, Julieta
> García). El repo sigue sin ser Azure-only ni de una sola empresa: cada
> vacante nueva se suma como caso de referencia, no reemplaza a la anterior.

## Requisitos de la vacante

| # | Requisito | Nivel actual | Estado |
|---|---|---|---|
| 1 | Mínimo 4 años en roles técnicos (SRE, automatización, observabilidad, infraestructura) | Cumplido de sobra (Bizagi, MercadoLibre, AgroTec) | 🟢 Sin brecha |
| 2 | Terraform, Ansible, Helm, Kubernetes | Terraform y Kubernetes fuertes (MercadoLibre). **Ansible**: no aparece documentado. **Helm**: probable (viene con K8s) pero no confirmado explícitamente | 🟡 Brecha media (Ansible) |
| 3 | AWS o GCP | Fuerte en ambas | 🟢 Sin brecha |
| 4 | CI/CD (GitHub/GitLab) | Fuerte (Azure Pipelines, Jenkins, GitHub Actions) | 🟢 Sin brecha |
| 5 | Observabilidad: OpenTelemetry, Elastic, Prometheus, Grafana | Prometheus/Grafana ya son fortaleza documentada. **OpenTelemetry** y **Elastic (ELK/Elastic Stack)**: no documentados | 🟡 Brecha media |
| 6 | Herramientas de chaos engineering: Litmus, Chaos Mesh, Chaos Monkey o Gremlin | Sin experiencia documentada — es una práctica/herramienta nueva, no una extensión directa de algo que ya sepas | 🔴 Brecha alta |
| 7 | Monitoreo: Dynatrace o SolarWinds | No documentado (viene de Prometheus/Grafana, que es open-source; Dynatrace/SolarWinds son APM comerciales) | 🔴 Brecha alta |
| 8 | Deseable: IA/ML, analítica predictiva, AIOps | No documentado | 🔴 Brecha alta (pero declarado "deseable", no excluyente) |
| 9 | Diseñar y ejecutar experimentos de inyección de fallas (fault injection) | Concepto relacionado con troubleshooting/resiliencia que ya trabajás (HPA, Kubernetes), pero el enfoque **proactivo** (romper el sistema a propósito) es una práctica formal distinta | 🔴 Brecha alta (es el corazón del rol) |
| 10 | Automatizar escenarios de resiliencia dentro de pipelines CI/CD | Extensión natural de tu experiencia en CI/CD — "solo" falta el contenido específico (qué chaos experiment correr) | 🟡 Brecha media |

## Fortalezas a favor (no pierdas esto en la entrevista)

- **Kubernetes + Terraform + AWS/GCP en producción de alto volumen**
  (MercadoLibre) — es la base de infraestructura sobre la que corre
  cualquier experimento de chaos engineering; sin esto, chaos engineering
  no tiene sentido.
- **Prometheus/Grafana** — la mitad del stack de observabilidad pedido ya
  es fortaleza tuya; falta sumar OpenTelemetry y Elastic, no arrancar de
  cero.
- **Experiencia real con incidentes/resiliencia** (aunque no formalizada
  como "chaos engineering"): cualquier troubleshooting de producción a
  volumen (MercadoLibre) ya entrena la mentalidad de "¿qué pasa si esto
  falla?", que es la pregunta central de chaos engineering.
- **CI/CD end-to-end** — la vacante pide automatizar chaos experiments
  *dentro* de pipelines, algo que ya sabés construir; solo cambia el
  contenido del pipeline.

## Prioridad de estudio (de mayor a menor brecha)

1. **Chaos engineering: conceptos y herramientas** (Litmus, Chaos Mesh,
   Chaos Monkey, Gremlin) — es el corazón del rol, tema completamente
   nuevo.
2. **OpenTelemetry** — estándar de instrumentación de trazas/métricas/logs,
   complementa lo que ya sabés de Prometheus/Grafana.
3. **Elastic (Elastic Stack / ELK)** — logging centralizado, distinto del
   modelo de métricas de Prometheus.
4. **Dynatrace o SolarWinds** — al menos vocabulario y conceptos de APM
   comercial (no hace falta profundidad de operador, sí saber de qué se
   habla en la entrevista).
5. **Ansible** — gestión de configuración; complementa (no reemplaza) tu
   experiencia con Terraform (IaC declarativo de infraestructura) con
   automatización de configuración imperativa/declarativa a nivel de host.
6. **AIOps / IA aplicada a operaciones** — deseable, no excluyente; alcanza
   con vocabulario y casos de uso (detección de anomalías, correlación de
   alertas) para la entrevista.

Ver el nuevo tema `../temas/14-chaos-engineering-sre/` para el detalle de
estudio. Los temas de observabilidad, Kubernetes, Terraform y CI/CD ya
existentes en este repo (`07`, `10`, `01`, `03`) cubren el resto de la
vacante — no se duplican acá.
