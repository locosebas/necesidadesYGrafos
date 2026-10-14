# Propuesta de valor para Dapta — Cumplimiento ("defensa")

> **v2 (2026-10-14).** La v1 ([propuesta-valor-v1.md](propuesta-valor-v1.md)) estaba enfocada en *seguridad* y
> nombraba demasiadas herramientas. La v2 se reenfoca en lo que de verdad es el cargo: una **propuesta de
> cumplimiento** (igual que en Davivienda), con la **deuda técnica** como hilo conductor, porque fue lo que más
> se mencionó en la entrevista.
> Dolores confirmados: **certificaciones, estabilidad y métricas DORA**, más **deuda técnica**.
> Contexto: migraciones a **Kubernetes** y **Temporal** en curso, ~14 desarrolladores, ronda semilla de USD 6 M
> (13-oct-2026), plan Enterprise que promete **SLAs** y **on-premise**. **No se inventan cifras.**

---

## 1. El problema: una causa, tres síntomas

```
                    DEUDA TÉCNICA
       (atajos acumulados al crecer rápido)
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 CERTIFICACIONES     ESTABILIDAD           DORA
 controles que no    incidentes (Flow      despliegues lentos
 se sostienen sin    Studio: 5 en 5 días)  y que fallan seguido
 trabajo manual
      └──────────────────┼──────────────────┘
                         ▼
     Contratos Enterprise que no se cierran
     (piden certificación + SLA + evidencia)
```

**Tesis:** si se atacan los tres síntomas por separado (un consultor para el SOC 2, bomberos para los
incidentes, presión para desplegar más), se gasta el triple y la deuda sigue. Si se paga la deuda **en el orden
correcto**, los tres mejoran juntos.

## 2. La propuesta, en una frase

> **"Que el cumplimiento sea un subproducto, no un proyecto":** medir la deuda técnica, pagarla en el orden que
> más acerque a Dapta a sus certificaciones y a sus SLAs, y aprovechar las migraciones a Kubernetes y Temporal
> para que la plataforma nueva **genere sola la evidencia** que pide el auditor.

## 3. Los 4 pilares: **Medir, Pagar, Cumplir, Estabilizar** ("**M-P-C-E**")

### Pilar 1 — Medir (no se gestiona lo que no se mide)

| Qué se mide | Cómo, con lo que ya tienen |
|---|---|
| **Métricas DORA** (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Failed Deployment Recovery Time) | API de GitHub + eventos de despliegue → **Grafana** |
| **SLOs** de lo que ve el cliente (llamada conectada, latencia por turno, ejecución de Flow Studio) | Métricas actuales + **Grafana**; la status page se calcula desde ahí |
| **Estado de los controles** de SOC 2 | **Vanta** (ya lo pagan) |
| **Registro de deuda técnica**: qué es, dónde está, cuánto "interés" cobra (incidentes, horas, controles en rojo) | Un tablero en el gestor que ya usan (Jira) |

### Pilar 2 — Pagar la deuda en el orden correcto

- **Criterio de prioridad**: primero la deuda que **más interés cobra** en los tres dolores: la que causa
  incidentes, la que rompe un control de SOC 2 o la que alarga el Lead Time. Lo demás espera.
- **Hotspots**: el código que cambia mucho **y** es complejo es donde la deuda más cuesta (análisis de
  *code churn* sobre Git).
- **Capacidad fija**: un porcentaje acordado de cada sprint para deuda (por ejemplo, 15–20%), y que la
  **Error Budget Policy** lo suba automáticamente cuando un servicio agota su presupuesto.
- **Migraciones con el patrón Strangler Fig**: Kubernetes y Temporal se adoptan **servicio por servicio**, y cada
  servicio que migra **sale sin deuda** (pipeline estándar, secretos fuera del código, observabilidad, ADR).
  Con **criterio de salida**: el sistema viejo se apaga, no quedan dos plataformas para siempre.
- Cada decisión de qué pagar y qué no, escrita en un **ADR** (Architecture Decision Record).

### Pilar 3 — Cumplir (cumplimiento continuo, no por temporada de auditoría)

| Pieza | Control de SOC 2 que evidencia solo |
|---|---|
| Todo cambio por pull request revisado, con **branch protection** | Change management procedures enforced |
| **Un solo pipeline reutilizable** (GitHub Actions) con escaneo nativo de GitHub (Dependabot, secret scanning) | Development lifecycle established · Vulnerabilities scanned and remediated |
| CI sin llaves: **OIDC** hacia AWS; despliegue con **Argo CD** (nadie hace `kubectl` a mano) | Production deployment access restricted |
| Secretos en **AWS Secrets Manager** | Encryption key access restricted |
| Accesos con SSO y **revisión trimestral** desde Vanta | Access reviews conducted |
| Post-mortems y simulacros de incidente | Incident response plan tested |
| Restauración de backups **probada** | Continuity and Disaster Recovery plans tested |

**Hoja de ruta de certificaciones** (se ajusta a lo que pidan los contratos en espera):
1. SOC 2 Type II con **ventana de 12 meses** y, por las SLAs de Enterprise, sumar el criterio de **Availability**.
2. La siguiente según el comprador: **ISO 27001** (LatAm, Europa, empresas globales; reutiliza gran parte de SOC 2),
   **HIPAA** si es salud (no es certificación: BAA y evaluación), **PCI DSS** solo si reciben tarjetas por voz
   (mejor sacarlas del alcance).
3. Después, como diferenciador: **ISO 42001** (gestión de IA).

### Pilar 4 — Estabilizar

- **SLOs y Error Budget** por componente (voz, texto, Flow Studio); la **Error Budget Policy** decide cuándo se
  congelan features y se paga deuda. Es el mecanismo que **pone de acuerdo a "ataque" y "defensa"**.
- **SLAs de Enterprise siempre más laxas** que los SLOs internos.
- **Gestión de incidentes** con roles (Incident Commander, Operations Lead, Communications Lead, Scribe) y
  **post-mortem blameless**: cada acción del post-mortem entra al registro de deuda.
- **Status page honesta**, calculada desde los SLIs.
- **Temporal** para lo que hoy falla en Flow Studio: reintentos con backoff, timeouts, estado durable; con
  activities **idempotentes** y **versionado** de workflows para no romper ejecuciones en curso.

## 4. Lo que **no** se propone (y por qué)

Aplicando el marco **DUCOREA** ([decisiones-herramientas.md](decisiones-herramientas.md)):

- **No** un SIEM completo ni un service mesh: no son el dolor hoy y nadie los operaría.
- **No** cambiar Vanta: rompería la continuidad de la auditoría.
- **No** herramientas pagas para DORA o feature flags el primer mes: GitHub, Grafana y **PostHog** ya lo cubren.
- **No** reescribir: la deuda se paga por hotspots y aprovechando las migraciones, no con un proyecto "big bang".
- Herramientas **nuevas**: solo **Argo CD** y, más adelante, **Kyverno en modo Audit**.

## 5. Plan 30-60-90 días

| Tramo | Qué | Entregable |
|---|---|---|
| **Días 1-30: medir y escuchar** | Línea base de DORA, SLOs e incidentes; leer el informe SOC 2 y sus excepciones; inventario de la deuda (con los desarrolladores, no solo desde el código); estado real de las migraciones. Victorias rápidas: branch protection, OIDC en el CI, MFA, revisión de accesos | **Registro de deuda priorizado** + tablero DORA/SLO + plan de certificaciones validado con el CTO |
| **Días 31-60: pagar lo que más duele** | Pipeline reutilizable + Argo CD en el **primer servicio migrado** (Strangler Fig); Error Budget Policy acordada; primer post-mortem con formato | Golden path funcionando con 1 servicio; deuda #1 y #2 pagadas |
| **Días 61-90: que se sostenga solo** | El resto de servicios migra por el golden path; controles de Vanta en verde de forma continua; simulacro de incidente; capacidad fija para deuda en cada sprint | Evidencia automática para el SOC 2 de 12 meses + decisión de la siguiente certificación |

## 6. Cómo se mide el éxito (sin inventar línea base)

| Dolor | Indicador |
|---|---|
| Certificaciones | % de controles de Vanta en verde de forma continua; cero excepciones en la siguiente auditoría; días para responder un cuestionario de seguridad |
| Estabilidad | Cumplimiento de SLO por componente; incidentes por mes; Failed Deployment Recovery Time |
| DORA | Las 4 métricas en tendencia (sin metas el primer mes: ley de Goodhart) |
| Deuda técnica | Ítems de alto interés pagados; Rework Rate; horas de toil por semana |

## 7. Por qué yo

- Experiencia en **Kubernetes** (troubleshooting y arquitectura), **IAM** y **políticas como código**: la base de
  las dos migraciones.
- Preparación reciente en **SRE y cumplimiento** (proceso Davivienda: SLOs, Error Budget Policy, incidentes,
  post-mortem, PII y regulación).
- Criterio para **no** agregar herramientas: la deuda técnica también se crea comprando de más.

## 8. Preguntas para llevar

1. ¿Qué certificación o requisito concreto está frenando un contrato hoy, y para cuándo?
2. ¿Qué deuda técnica les duele más: la que causa incidentes, la que frena despliegues o la que complica la auditoría?
3. ¿En qué punto van las migraciones a Kubernetes y a Temporal, y quién decide cuándo se apaga lo viejo?
4. ¿Quién mantiene hoy Vanta y la evidencia del SOC 2?
5. ¿Cómo se reparte hoy el tiempo entre "ataque" (producto) y "defensa"?

## 9. Historia en 60 segundos

> "Lo que me contaron se resume en una causa y tres síntomas. La causa es deuda técnica, normal en una empresa
> que creció rápido. Los síntomas son certificaciones que cuestan sostener, incidentes como los de Flow Studio
> y despliegues lentos y frágiles. Mi propuesta es que el cumplimiento sea un subproducto y no un proyecto. En
> 30 días mido: DORA, SLOs, el estado de los controles en Vanta y un registro de deuda priorizado por el interés
> que cobra. En 60 días pago la deuda que más duele aprovechando las migraciones a Kubernetes y Temporal: cada
> servicio que migra sale con un pipeline estándar que genera evidencia sola. En 90 días eso se sostiene sin
> esfuerzo manual, la Error Budget Policy decide cuándo frenar features para pagar deuda, y Dapta llega a su
> SOC 2 de 12 meses y a la siguiente certificación con evidencia continua. Y lo hago sin llenar al equipo de
> herramientas: solo agrego lo que resuelve un dolor medible."
