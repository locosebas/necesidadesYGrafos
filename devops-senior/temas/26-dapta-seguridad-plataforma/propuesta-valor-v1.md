# Propuesta de valor para Dapta — "Defensa" de la plataforma

> Borrador v1 (2026-10-14). Se construyó con lo público (web, trust center) y lo poco que se supo en la
> entrevista: **migración a Kubernetes**, **migración a Temporal**, **~14 desarrolladores**, **problemas para
> certificarse** y la tarea de montar un **proceso confiable de desarrollo y despliegue**.
> Lo que no sabemos se dice como hipótesis y se valida en las primeras 2 semanas. **No se inventan cifras.**

---

## 1. El problema, en 3 frases

1. Dapta vende agentes de voz con IA a empresas que **exigen evidencia de seguridad** (SOC 2 ya lo tienen,
   pero recién salido y con la ventana mínima de 3 meses; los clientes grandes van a pedir más).
2. Está **migrando a Kubernetes y a Temporal** al mismo tiempo, con 14 desarrolladores que tienen que seguir
   sacando producto.
3. Si la seguridad llega **después** de la migración, cuesta el doble y frena al equipo; si llega **dentro**
   de la plataforma nueva, sale casi gratis y además **produce la evidencia** que pide el auditor.

## 2. La propuesta, en una frase

> **"Una carretera pavimentada, no un peaje":** convertir la migración a Kubernetes y Temporal en una
> plataforma **segura por defecto**, donde el camino fácil para el desarrollador sea también el camino
> seguro, y donde **cada despliegue genere solo su evidencia de cumplimiento**.

En términos de la industria: un **golden path** (camino dorado) de Platform Engineering con
**compliance as code** (cumplimiento como código).

## 3. Los 4 pilares (memorizar en orden: **Desplegar, Plataforma, Detectar, IA** → "**D-P-D-IA**")

### Pilar 1 — Despliegue confiable (GitOps)

Lo que pidieron explícitamente: un proceso confiable de desarrollo y despliegue.

| Pieza | Herramienta propuesta | Control de SOC 2 que evidencia |
|---|---|---|
| Nadie sube directo a `main`; todo entra por pull request revisado | **GitHub branch protection / rulesets** + CODEOWNERS | Change management procedures enforced |
| Pipeline único y reutilizable para todos los servicios | **GitHub Actions reusable workflows** (una plantilla, 14 devs la heredan) | Development lifecycle established |
| Revisión automática de código y dependencias | **Semgrep** (SAST, Static Application Security Testing), **Dependabot/Renovate** (SCA, Software Composition Analysis) | Vulnerabilities scanned and remediated |
| Escaneo de imágenes y secretos | **Trivy** (imágenes), **GitHub secret scanning + push protection** / **Gitleaks** | Vulnerabilities scanned and remediated |
| CI sin llaves de AWS guardadas | **GitHub OIDC → AWS IAM role** (credenciales temporales, cero llaves de larga vida) | Production deployment access restricted |
| Imagen firmada que solo el pipeline puede producir | **Cosign** (Sigstore) + **Amazon ECR** | Configuration management system established |
| El clúster se sincroniza con Git, nadie hace `kubectl apply` a mano | **Argo CD** (GitOps) | Production deployment access restricted |
| Si el despliegue sale mal, se devuelve solo | **Argo Rollouts** (canary + rollback automático) | — (confiabilidad, enlaza con el tema 25) |
| Infraestructura en código, con `plan` visible en el pull request | **Terraform** (+ Atlantis o GitHub Actions) | Change management procedures enforced |
| Ambientes separados | dev → staging → producción, cuentas de AWS separadas con **AWS Organizations** | Network segmentation implemented |

**Resultado:** el historial de Git **es** la evidencia. Vanta ya se integra con GitHub y AWS, así que esa
evidencia llega sola al auditor, sin capturas de pantalla.

### Pilar 2 — Plataforma Kubernetes y Temporal segura por defecto

| Pieza | Herramienta propuesta | Por qué |
|---|---|---|
| Clúster administrado | **Amazon EKS** | AWS ya es su nube (subservice provider del SOC 2) |
| Cada pod con su propio rol de AWS, sin llaves | **EKS Pod Identity / IRSA** (IAM Roles for Service Accounts) | Mínimo privilegio |
| Secretos fuera del código y de los manifiestos | **External Secrets Operator** + **AWS Secrets Manager** | Incluye los tokens OAuth de HubSpot/Salesforce de cada cliente |
| Reglas que el clúster aplica solo | **Kyverno** (o OPA/Gatekeeper): no root, solo imágenes firmadas, límites de CPU/memoria | Primero en modo *audit*, después *enforce*: no frena al equipo el día 1 |
| Aislamiento de red | **NetworkPolicy** (Cilium o VPC CNI) por namespace | Un servicio comprometido no alcanza a todos |
| **Temporal: cifrar lo que viaja en los workflows** | **Payload Codec / Data Converter** de Temporal (cifrado del lado del cliente) + **Codec Server** para ver los datos en la UI | Si un workflow lleva transcripciones o datos del CRM, Temporal Cloud **solo ve texto cifrado**. Es el argumento de privacidad más fuerte de la migración |
| Conexión a Temporal | **mTLS** (mutual TLS) o API keys por namespace de Temporal | Cada ambiente con su namespace y su credencial |

### Pilar 3 — Detectar y responder

| Pieza | Herramienta propuesta | Control de SOC 2 |
|---|---|---|
| Registro de todo lo que pasa en AWS | **AWS CloudTrail** a nivel de organización, en una cuenta de logs aparte | Log management utilized |
| Detección de amenazas (incluye EKS) | **Amazon GuardDuty** (con EKS Runtime Monitoring) | Intrusion detection system utilized |
| Tablero único de hallazgos | **AWS Security Hub** → alertas a **Slack** | Vulnerability and system monitoring procedures established |
| Plan de incidentes que se practica | Runbook + **simulacro (tabletop exercise)** cada trimestre | Incident response plan tested |
| Revisión de accesos sin dolor | **AWS IAM Identity Center** + SSO, revisión trimestral desde Vanta | Access reviews conducted |

### Pilar 4 — Seguridad propia de un producto de voz con IA (el diferencial)

Hoy **ninguno de los 79 controles publicados menciona IA**. Esto es lo que van a preguntar los clientes
grandes y lo que abre la puerta a la siguiente certificación.

| Riesgo | Propuesta |
|---|---|
| PII (Personally Identifiable Information) en grabaciones y transcripciones | Redacción automática en la transcripción (**Deepgram** tiene la opción `redact` para PCI, números, SSN) + política de retención de grabaciones |
| Datos de clientes en proveedores de LLM | Acuerdos de **ZDR** (Zero Data Retention) / no entrenamiento con OpenAI, Anthropic, Gemini; registro de qué dato va a qué proveedor |
| El que llama manipula al agente (**prompt injection** por voz) | Guardrails, herramientas del agente con mínimo privilegio, pruebas guiadas por **OWASP Top 10 for LLM Applications** (aquí trabaja junto al equipo de "ataque") |
| Un cliente ve datos de otro (multi-tenancy) | Pruebas automáticas de aislamiento por tenant en el pipeline |
| Llamadas y grabaciones en EE. UU. | Consentimiento de grabación y reglas de **TCPA** (Telephone Consumer Protection Act) como configuración por defecto |

## 4. Plan 30-60-90 días

| Tramo | Qué | Entregable |
|---|---|---|
| **Días 1-30: entender y apagar incendios** | Inventario: cuentas de AWS, repos, quién tiene acceso a producción, secretos, estado de la migración. Modelo de amenazas del flujo de una llamada. **Victorias rápidas:** MFA en todo, branch protection, secret scanning, CloudTrail + GuardDuty encendidos, quitar llaves de AWS del CI (OIDC) | Mapa de riesgos + backlog priorizado, validado con el CTO |
| **Días 31-60: pavimentar la carretera** | Plantilla de pipeline reutilizable, Argo CD, Kyverno en modo *audit*, External Secrets, cifrado de payloads en Temporal. **Un servicio piloto** migra por el camino nuevo | Golden path funcionando con 1 servicio |
| **Días 61-90: que todos pasen por ahí** | El resto de servicios migra por el golden path; Kyverno pasa a *enforce*; la evidencia llega sola a Vanta; primer simulacro de incidente | 100% de despliegues por el pipeline + hoja de ruta de la siguiente certificación (ISO 27001, HIPAA o ISO 42001 según los compradores) |

## 5. Cómo se mide (sin inventar la línea base: se mide en el día 1)

- **% de despliegues que pasan por el pipeline** → meta: 100%.
- **Métricas DORA** (DevOps Research and Assessment): Deployment Frequency, Lead Time for Changes, Change
  Failure Rate, Time to Restore Service. La seguridad **no** debe empeorarlas.
- **% de controles de Vanta en verde** y días que tarda un control en volver a verde.
- **Edad de las vulnerabilidades críticas abiertas.**
- **Tiempo para responder un cuestionario de seguridad** de un cliente (impacto directo en ventas).

## 6. Costo (órdenes de magnitud, verificar antes de citar)

- Casi todo es **software abierto** (Argo CD, Kyverno, Trivy, Cosign, External Secrets) o ya está pagado
  (GitHub, Vanta, AWS).
- Servicios de AWS nuevos (GuardDuty, Security Hub, CloudTrail organizacional): cobran por volumen; para
  una startup de este tamaño suelen ser cientos, no miles, de dólares al mes. **Medir con la factura real.**
- El costo grande es **tiempo de personas**: por eso el plan empieza con victorias rápidas y un piloto, no
  con una reescritura.

## 7. Por qué yo

- **Kubernetes** a nivel de troubleshooting y arquitectura, IRSA, OPA/políticas como código, secretos con
  identidades administradas.
- Experiencia real en **CI/CD** (Jenkins, Azure Pipelines) y preparación reciente en **SRE**: SLOs, rollback
  automático, gestión de incidentes y post-mortem blameless.
- Visión de **plataforma como habilitador**: la seguridad no puede frenar a 14 desarrolladores que están
  sacando producto.

## 8. Preguntas para llevar (muestran criterio)

1. ¿Qué certificación o requisito concreto les han pedido los clientes que hoy no pueden cumplir?
2. ¿En qué punto va la migración a Kubernetes y desde dónde migran?
3. ¿Usan Temporal Cloud o lo operan ustedes? ¿Qué datos viajan dentro de los workflows?
4. ¿Quién mantiene hoy Vanta y la evidencia del SOC 2?
5. ¿Qué hace exactamente el equipo de "ataque" y cómo se coordina con "defensa"?

## 9. Historia en 60 segundos (para decir en voz alta)

> "Dapta ya tiene SOC 2 Type II, pero los clientes grandes van a pedir más, y justo ahora están migrando a
> Kubernetes y a Temporal. Esa migración es el momento más barato para meter la seguridad. Mi propuesta es
> una carretera pavimentada, no un peaje: un solo pipeline con GitOps donde todo cambio pasa por pull
> request, se escanea, se firma y se despliega con Argo CD; un clúster que por defecto no deja correr nada
> inseguro; detección con GuardDuty; y controles propios de IA de voz, que hoy no tienen ninguno. En 30 días
> entiendo y apago incendios, en 60 hay un servicio piloto en el camino nuevo, y en 90 todos los despliegues
> pasan por ahí y la evidencia le llega sola al auditor. El equipo despliega más rápido, no más lento, y
> ventas tiene con qué responder el próximo cuestionario de seguridad."
