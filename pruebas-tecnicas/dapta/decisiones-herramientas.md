# Decidir herramientas: cuándo usar, cuándo no, y cómo defenderlo

> Lo que más tienes que mostrar en Dapta no es que **conoces** herramientas, sino que sabes **decidir**:
> cuándo adoptar una, cuándo usar lo que ya hay y, sobre todo, **cuándo NO**.
> Las decisiones se trabajan **de a una**: tú decides primero, aplicando el marco, y después se compara con
> la recomendación. La columna **Tu decisión** queda vacía a propósito.

---

## 1. Autocrítica de la propuesta v1

La propuesta v1 nombra **más de 12 herramientas nuevas** (Semgrep, Trivy, Cosign, Argo CD, Argo Rollouts,
Kyverno, External Secrets, Cilium, Atlantis, GuardDuty, Security Hub...) para **14 desarrolladores**.
Un CTO de startup preguntaría, con razón: *"¿Y quién opera todo eso?"*. Eso es **tool sprawl**
(proliferación de herramientas), y en Dapta tiene un costo extra: **cada SaaS nuevo es un subprocesador
más** en el trust center, con revisión de proveedor, DPA (Data Processing Agreement) y evidencia para el
SOC 2. La v2 de la propuesta tiene que pasar por el marco de abajo.

## 2. El marco: 7 preguntas antes de adoptar una herramienta ("**DUCOREA**" — por confirmar la mnemotecnia en sesión)

| # | Pregunta | Qué se busca |
|---|---|---|
| 1 | **Dolor**: ¿qué dolor medible resuelve? (DORA, SLO, control de SOC 2, contrato perdido) | Si no hay dolor ni métrica, no se adopta |
| 2 | **Usar lo que ya hay**: ¿lo resuelve algo que ya pagamos? (GitHub, AWS, Vanta, Grafana, Cloudflare) | Primero lo existente; a veces es solo configurar |
| 3 | **Costo total**: licencia + personas (FTE) para operarla + carga cognitiva del equipo | El software abierto no es gratis: cuesta personas |
| 4 | **Operación**: ¿quién la parcha, la monitorea y está de guardia si se cae? | En 14 personas, administrado (SaaS / AWS) suele ganar a autogestionado |
| 5 | **Reversibilidad**: ¿puerta de una vía o de dos vías? ¿cuánto amarre (lock-in)? | Las decisiones reversibles se toman rápido; las irreversibles, con calma |
| 6 | **Evidencia y riesgo**: ¿genera evidencia para el auditor? ¿agrega un subprocesador o superficie de ataque? | En Dapta, la herramienta también se audita |
| 7 | **Adopción**: ¿frena o acelera a los desarrolladores? ¿se necesita **ahora** o en 6 meses? | YAGNI (You Aren't Gonna Need It): no adelantarse |

**Cómo se deja escrito:** un **ADR** (Architecture Decision Record): contexto, opciones, decisión,
consecuencias. Una página por decisión, en el repo. Además es evidencia del control de SOC 2
"Development lifecycle established".

## 3. Decisiones reales de Dapta

| # | Decisión | Opciones | Recomendación provisional | Criterio que manda | Tu decisión |
|---|---|---|---|---|---|
| D1 | Secretos | HashiCorp Vault autogestionado · **AWS Secrets Manager** + External Secrets · secretos de GitHub/K8s a mano | Secrets Manager: ya están en AWS, administrado, auditado por CloudTrail | 2, 4 | |
| D2 | Temporal | **Temporal Cloud** · autogestionado en su Kubernetes | Cloud (ya es subprocesador); autogestionado solo si el on-premise de Enterprise lo exige | 4, 5 | |
| D3 | ¿Kubernetes o no? | **EKS** · ECS Fargate · seguir como están | EKS se justifica **por el on-premise de Enterprise** (Helm portable); sin eso, ECS sería más simple | 1, 5 | |
| D4 | Políticas en el clúster | **Kyverno** · OPA/Gatekeeper · ninguna al inicio | Una sola; Kyverno por YAML (menos curva que Rego) | 3, 7 | |
| D5 | Despliegue | **Argo CD** · Flux · `kubectl`/Helm desde GitHub Actions | Argo CD: UI que ven los desarrolladores + historial = evidencia | 6, 7 | |
| D6 | Canary / rollback | Argo Rollouts · Flagger · **todavía no** | Después de tener SLOs: sin métrica, el canary no sabe cuándo devolver | 7 (YAGNI) | |
| D7 | Feature flags | LaunchDarkly · Unleash · PostHog flags (ya lo tienen) · casero | **PostHog** (ya es subprocesador): cero proveedores nuevos | 2, 6 | |
| D8 | Medir DORA | LinearB / Sleuth · **API de GitHub + Grafana** · Four Keys | Casero sobre lo que ya tienen; comprar solo si el tablero no basta | 2, 3 | |
| D9 | Escaneo en el pipeline | Snyk · **GitHub Advanced Security / Dependabot + Trivy** · Semgrep | Lo nativo de GitHub primero; agregar Semgrep solo si hace falta | 2, 6 | |
| D10 | Detección en AWS | Splunk / Datadog SIEM · **GuardDuty + Security Hub** · nada | Nativo de AWS; un SIEM completo es para cuando haya alguien que lo mire | 3, 4 | |
| D11 | Service mesh | Istio · Linkerd · **ninguno** | Ninguno: mTLS y tráfico avanzado no son dolor hoy | 1, 3 | |
| D12 | Cumplimiento | **Seguir con Vanta** · cambiar a Drata · consultor | Seguir con Vanta: cambiar ahora rompe la ventana del Type II | 5 | |

**Patrón de las recomendaciones:** de 12 decisiones, en **4 la respuesta es "lo que ya tienen"** (D7, D8,
D9, D12) y en **2 es "todavía no" o "ninguno"** (D6, D11). Ese es el mensaje para la entrevista:
*"Antes de traer herramientas, quito las que sobran y uso bien las que ya pagan."*
