# Chubb — L1 Interview "Cloud Engineer Ops" (2026-11-09, 2:30–3:00 pm Bogotá)

- **Plataforma:** Webex. **Organiza:** Paloma (Ana) Muñoz Quintero (reclutadora).
  **Entrevistadores:** Andre Meireles, Luis F. Arévalo. Probablemente en **inglés**.
- **Postulación de origen:** "Senior Cloud Engineer", Chubb, Bogotá (LinkedIn,
  job 4483593450, 2026-10-27).
- **Ojo:** el rechazo del 2026-11-09 es de **otro cargo** (Sr. SRE Lead 37279),
  no de este.

## Material de estudio

- [diagramas-c4.md](diagramas-c4.md): 26 diagramas C4 (4 de presentación personal + 22 de preguntas), con íconos.
- [libreto-diapositivas.md](libreto-diapositivas.md): 32 diapositivas, **bilingües**: viñetas y guion en inglés y en español.
- [presentacion.html](presentacion.html): la presentación (← → navegar, **L** inglés/español, **N** guion en los dos idiomas).
  Versión para el celular (privada): https://claude.ai/artifact/UpDBko5VcyAZ6mGZCscNh8 · Se regenera con `python3 generar_presentacion.py`.
- Parte A (presentación personal): quién soy, Bizagi, MercadoLibre, por qué encajo.
- Parte B (25 preguntas): Azure, landing zone en GCP, Cloud Adoption Framework, Terraform (estructura,
  pipeline en Jenkins, drift), Ansible, Kubernetes (arquitectura, AKS/EKS/GKE, CrashLoopBackOff),
  incidentes mayores, Prometheus + ELK, ServiceNow, gobierno como código, red hub-and-spoke, IAM,
  autoservicio, FinOps, resiliencia y DR, migración a cloud native, Linux y Windows, los 15 años,
  un error del que aprendiste, y preguntas para ellos.

## Descripción del cargo (resumen)

Chubb (aseguradora, "Underwriting Engineering and Data Analytics company") está
migrando aplicaciones a contenedores y **construyendo su nueva plataforma en
GCP (Google Cloud Platform)**, sobre una base actual fuerte en **Azure**.

**Responsabilidades clave:**
- Operación de la infraestructura cloud dentro del equipo global de cloud.
- Guía de arquitectura a equipos de aplicación; patrones de resiliencia y
  rendimiento; cumplimiento del **Cloud Adoption Framework** y estándares Chubb.
- Diseñar servicios cloud nuevos y construir **autoservicio** (self-service)
  con **CI/CD (Continuous Integration / Continuous Delivery) de infraestructura**.
- Capacidades operativas para el equipo de Operaciones.
- **Gobierno y políticas de seguridad en Azure** automatizadas (policy-as-code).
- Atender **escalamientos y incidentes mayores de producción**.
- Evaluar madurez cloud-native y dirigir migraciones.
- **Gestión y optimización de costos** (FinOps).

**Requisitos:**
- Transformación cloud grande, idealmente **GCP**; **Azure/GCP** con diseño de
  **IAM (Identity and Access Management), seguridad, monitoreo y red**.
- IaC (Infrastructure as Code): **Terraform, Ansible, Bash, Jenkins** + pruebas automatizadas.
- **Windows y Linux**; **Kubernetes, AKS (Azure Kubernetes Service), EKS (Elastic Kubernetes Service)**, Docker.
- **ELK (Elasticsearch, Logstash, Kibana)**, **Prometheus**, **ServiceNow** (gestión de cambios).
- Certificación Azure/GCP deseable.

## Cruce con `progreso.md`

| # | Tema del cargo | Nivel | Material |
|---|---|---|---|
| 1 | Kubernetes (arquitectura, control plane, Pods) | 🟢 | `devops-senior/temas/10-kubernetes-avanzado/`, `31-entrevista-2026-11-04/` |
| 2 | Terraform (state, backends, módulos) | 🟢 | `devops-senior/temas/` fase 2 |
| 3 | Jenkins / CI/CD | 🟢 | `31-entrevista-2026-11-04/` (#5, #13) |
| 4 | Azure RBAC (Role-Based Access Control) | 🟢 | — |
| 5 | Policy-as-code (OPA/Gatekeeper; Azure Policy) | 🟢 / 🟡 | — |
| 6 | Incidentes mayores en producción | 🟡/🟢 | `devops-senior/temas/28-respuesta-incidentes-l2-l3/` |
| 7 | Ansible | 🟡 | fase 2 |
| 8 | FinOps / Well-Architected | 🟡 | (pilares: repaso estricto pendiente) |
| 9 | GCP (Landing zone, IAM, VPC compartida, GKE) | 🔴 / sin examen | por reforzar |
| 10 | ELK, Prometheus, ServiceNow | sin examen dedicado | por reforzar |
| 11 | Cloud Adoption Framework (Azure CAF) | sin examen dedicado | por reforzar |
