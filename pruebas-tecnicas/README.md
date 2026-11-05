# Pruebas técnicas y entrevistas por empresa

Una carpeta por empresa. Cada una tiene su **ruta de aprendizaje** enfocada en esa entrevista: qué
estudiar, en qué orden y con qué preguntas, con la misma escala de
[`../devops-senior/examenes/registro/progreso.md`](../devops-senior/examenes/registro/progreso.md)
(⬜ no visto · 🔴 novato · 🟡 intermedio · 🟢 sólido · 🔵 senior).

Método de todas las rutas: preguntas **de a una**, de lo general a lo específico, y en los repasos se
describe el mecanismo y **tú dices el nombre**.

| # | Empresa | Proceso | Ruta de aprendizaje vigente | Estado |
|---|---|---|---|---|
| 1 | [Davivienda](davivienda/) | Especialista Senior SRE — prueba de observabilidad (Banco Plus) | [ruta-sustentacion.md](davivienda/ruta-sustentacion.md) (la de la entrega fue [roadmap-express.md](davivienda/roadmap-express.md)) | Prueba entregada el 12 oct 2026; falta la sustentación |
| 2 | [Dapta](dapta/) | Defensa: propuesta de seguridad y cumplimiento | [roadmap-express.md](dapta/roadmap-express.md) | Entrevista probable el 15 oct 2026 |
| 3 | [Toolbox](toolbox/) | Prueba técnica: Bash, Ansible (LEMP en CentOS 7), Docker | Sin ruta (prueba corta, ya resuelta) | Entregada el 25 sep 2026 |
| 4 | [Gorila / Candiech](gorila-candiech/) | Prueba técnica Senior DevOps/Platform: AWS, EKS, Terraform, GitOps, incidentes (texto + videos) | Sin ruta; repaso con los "nombres clave" del [README](gorila-candiech/README.md) | Resuelta el 4 nov 2026 |
| 5 | [Coderbyte: incidente Kubernetes](coderbyte-incidente-k8s/) | Prueba técnica en Coderbyte: incidente con OOMKilled (Dynatrace, Splunk, OpenTelemetry, rollback, Error Budget) + preguntas cortas (trazas distribuidas, I/O wait en RHEL) | Sin ruta; repaso con los "nombres clave" del [README](coderbyte-incidente-k8s/README.md) | Presentada el 4 nov 2026 |
| 6 | [Keystone](keystone/) | Entrevista por voz con IA: Python/FastAPI, SQS/ECS, Elasticsearch, PostgreSQL, GraphQL, agentes LLM | Sin ruta; repaso con los "nombres clave" del [README](keystone/README.md) | Preguntas recibidas el 5 nov 2026 |
| 7 | [Niuro: AWS Infrastructure Engineer](niuro-aws/) | Entrevista con IA: AWS para cargas sensibles, Terraform, blue/green con esquema, CI/CD .NET, ECS EC2 vs Fargate, VPC y security groups | Sin ruta; repaso con los "nombres clave" del [README](niuro-aws/README.md). **Estudiar antes de una segunda entrevista** | Hecha el 5 nov 2026; salió bien |

## Cómo agregar una empresa nueva

1. Crear `pruebas-tecnicas/<empresa>/` con un `README.md` (origen del proceso, qué piden, fechas).
2. Agregar la ruta de aprendizaje (`roadmap-express.md`) contra `progreso.md`, y su `banco-preguntas.md`.
3. Sumar una fila a la tabla de arriba.

> ⚠️ El repo es público: aquí solo va información pública de cada empresa y lo que decidas contar.
