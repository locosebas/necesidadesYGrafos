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
| 4 | [TCS vía Adecco](tcs-adecco/) | Ingeniero DevOps: Azure DevOps, CI/CD, SonarQube, DevSecOps | Brecha en el [README](tcs-adecco/README.md) | Hoja de vida enviada el 22 oct 2026; esperando llamada de Adecco |

## Cómo agregar una empresa nueva

1. Crear `pruebas-tecnicas/<empresa>/` con un `README.md` (origen del proceso, qué piden, fechas).
2. Agregar la ruta de aprendizaje (`roadmap-express.md`) contra `progreso.md`, y su `banco-preguntas.md`.
3. Sumar una fila a la tabla de arriba.

> ⚠️ El repo es público: aquí solo va información pública de cada empresa y lo que decidas contar.
