# Contraargumentos y matices — revisión de decisiones (D1–D30)

> Al corregir cada decisión del [análisis de alternativas](analisis-alternativas.md), aquí quedan los
> **contraargumentos y matices** que la mesa podría usar contra tu decisión, y cómo responderlos. Léelos antes
> del ensayo.

## D7 — Gate con deployment protection rule

**Tu decisión:** la deployment protection rule es el gate principal (Plataforma controla, tribus extienden).

**Contraargumentos que puede hacer la mesa:**
1. *"Si el job no declara `environment: production`, la regla nunca se activa."* → La confianza OIDC (OpenID
   Connect) de AWS y GCP solo entrega credenciales de producción a tokens con `sub` = `environment:production`
   (y `job_workflow_ref` = plantilla oficial). Sin environment, no hay credenciales.
2. *"Soy administrador del repositorio: le quito la regla al environment."* → Los environments y sus reglas se
   definen como código (Terraform, provider de GitHub) y los gestiona Plataforma; las tribus no son
   administradoras. Cualquier cambio pasa por pull request y queda auditado.
3. *"¿Y si despliegan a mano con `kubectl`, por fuera del pipeline?"* → Admission controller (OPA Gatekeeper o
   Kyverno) que rechaza imágenes sin firma o sin SBOM; y nadie tiene credenciales de escritura directa en
   producción (solo el pipeline / GitOps).
4. *"Plataforma se vuelve cuello de botella."* → Solo imponemos el piso; las tribus extienden sin pedir permiso
   y contribuyen por inner source.

## D8 — Argo Rollouts o automatizar el service mesh existente

**Tu decisión:** dos opciones según el stack del banco; no imponer herramientas nuevas; considerar licencias.

**Matices y contraargumentos:**
1. **Argo Rollouts no exige Argo CD.** Es un controlador independiente. Si te dicen *"no tenemos Argo CD"*, la
   opción A sigue viva: Argo Rollouts usa el ingress, el balanceador (AWS ALB) o el mesh que ya tengan.
2. *"Argo Rollouts nos obliga a cambiar todos los Deployments."* → `workloadRef` permite que el `Rollout`
   reutilice el Deployment existente; o se va por la opción B (Flagger no toca los Deployments).
3. **Linkerd ya no es "gratis" para un banco:** desde 2024 las versiones *stable* requieren licencia de Buoyant
   para empresas de más de 50 empleados. Si el banco usa Linkerd, hay que contar ese costo (o usar *edge*).
4. **AWS App Mesh está descontinuado** (fin de soporte: 30 de septiembre de 2026). Si lo usan, no construir el
   canary encima: es la oportunidad de migrar.
5. *"¿Por qué no instalar Istio y listo?"* → Un mesh solo para canary es caro (+10–20% de recursos por los
   sidecars) y es otra pieza crítica. Se usa si ya existe o si hay otras razones (mTLS, políticas de tráfico).

## D8-bis — Estrategias de despliegue

**Tu decisión:** sin cambios.

## D10 y D11 — OpenTelemetry y la distribución del Collector

**Tu decisión:** no son decisiones propias; el enunciado exige OpenTelemetry y el OTel Collector.

**Matices por si la mesa insiste:**
1. *"¿Por qué OpenTelemetry y no el agente de Datadog o Dynatrace, que es más fácil?"* → Además de que lo pide
   el caso: neutralidad (cambiar de backend sin reinstrumentar), un solo estándar para AWS, GCP y el
   datacenter, y control de los datos dentro del banco (PII, costos) antes de enviarlos a cualquier proveedor.
2. **eBPF no compite con OpenTelemetry:** Grafana donó Beyla al proyecto OpenTelemetry (OpenTelemetry eBPF
   Instrumentation, OBI), así que la instrumentación sin código también cabe dentro del estándar que pide el caso.
3. **Dentro de la restricción todavía hay una sub-decisión: qué distribución del Collector.** Opciones: la
   distribución *contrib* (trae todos los componentes), una construida con OCB (OpenTelemetry Collector Builder,
   solo los componentes aprobados) o la de un proveedor (AWS ADOT, Grafana Alloy, Splunk). Respuesta: *"OCB,
   porque menos componentes es menos superficie de ataque y menos parches; las de proveedor sesgan a ese
   proveedor en un banco multi-cloud"*. Le suma a DevSecOps.
