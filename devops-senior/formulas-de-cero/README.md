# Fórmulas "de cero a que funcione"

Recetas paso a paso para responder en entrevista las preguntas del tipo
**"¿cómo armarías X desde cero?"**. Cada archivo es una checklist ordenada:
si la recitás en ese orden, sonás senior.

| # | Fórmula | Para preguntas tipo… |
|---|---|---|
| 01 | [Plataforma Kubernetes](01-plataforma-kubernetes.md) | "Montá una plataforma K8s para N equipos" |
| 02 | [Red interna de una empresa](02-red-interna-empresa.md) | "Diseñá la red de una oficina / empresa (y conectala a la nube)" |
| 03 | [Proyecto Terraform de toda la empresa](03-terraform-empresa.md) | "¿Cómo organizarías el IaC de toda la infraestructura?" |
| 04 | [CI/CD de cero](04-cicd-de-cero.md) | "Diseñá el pipeline de un servicio" |
| 05 | [Observabilidad de cero](05-observabilidad-de-cero.md) | "¿Cómo sabés que tu sistema está sano?" |
| 06 | [Landing zone: cuentas, identidad, secretos, seguridad](06-landing-zone-identidad-seguridad.md) | "Empresa nueva en la nube, ¿por dónde empezás?" |
| 07 | [App en contenedor / serverless de cero](07-app-contenedor-serverless.md) | "Llevá esta API FastAPI a producción" |
| 08 | [Chuleta de último minuto](08-chuleta-entrevista.md) | Repaso de 15 minutos antes de entrar |

---

## La meta-fórmula (sirve para CUALQUIER "¿cómo lo harías de cero?")

Memorizá este orden. Casi todas las respuestas senior son esta lista
aplicada a un tema distinto:

1. **Requisitos antes que herramientas** — ¿quién lo usa?, ¿cuánta carga?,
   ¿qué SLO/disponibilidad?, ¿compliance (PCI, GDPR, datos personales)?,
   ¿presupuesto?, ¿qué ya existe? *Arrancar preguntando es señal de seniority.*
2. **Fundaciones** — organización de cuentas/suscripciones/proyectos,
   **identidad** (SSO, grupos, roles, mínimo privilegio) y **red** (plan de IPs,
   segmentación, conectividad privada, DNS).
3. **Todo como código** — Terraform/Bicep para infra, GitOps para K8s,
   estado remoto con lock, nada creado a mano ("ClickOps").
4. **Cómputo** — el runtime correcto para el caso (VM, K8s, Container Apps /
   Cloud Run / Fargate, Functions).
5. **Datos y secretos** — base de datos gestionada, backups probados,
   secretos en Key Vault / Secrets Manager / Secret Manager, nunca en el repo.
6. **Entrega (CI/CD)** — build → test → scan → artefacto inmutable → deploy
   por entornos con aprobación, OIDC en vez de claves.
7. **Observabilidad** — métricas, logs, trazas, dashboards, alertas sobre
   SLOs (no sobre CPU).
8. **Seguridad transversal** — mínimo privilegio, cifrado en tránsito y en
   reposo, escaneo de imágenes/IaC, políticas (deny by default).
9. **Resiliencia** — multi-AZ, autoscaling, backups + **restore probado**, DR
   con RPO/RTO definidos.
10. **Operación y costos** — runbooks, on-call, tags para costos, rightsizing,
    documentación.
11. **Validación "funciona"** — una prueba end-to-end concreta (ej: "despliego
    un hello-world por HTTPS, veo sus métricas y logs, y me llega la alerta
    cuando lo rompo").

> 💡 Frase para abrir cualquier respuesta: *"Antes de elegir herramientas
> preguntaría X, Y, Z. Asumiendo [supuesto], lo armaría en capas: fundaciones,
> plataforma, entrega, observabilidad y operación."*

## Cómo practicar hoy

1. Leé una fórmula, cerrala y **decila en voz alta** en 3 minutos.
2. Pedime: *"Haceme de entrevistador sobre la fórmula 01"* y te repregunto
   como lo haría un entrevistador senior.
3. Antes de entrar, leé solo la [chuleta](08-chuleta-entrevista.md).
