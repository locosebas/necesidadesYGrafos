# Arquitectura y costos: Well-Architected Framework (Azure/AWS) y Architecture Framework (GCP)

Nivel senior implica poder justificar decisiones de arquitectura más allá de
"funciona": costo, resiliencia, operabilidad — en cualquier nube.

## Objetivos

- Explicar los pilares de cada framework y notar que son prácticamente los
  mismos 5 conceptos con nombres distintos.
- Diseñar para alta disponibilidad: zonas/regiones, SLA compuesto de una
  arquitectura multi-servicio, en cualquiera de las tres nubes.
- FinOps básico: reserved instances/savings plans/committed use discounts,
  autoscale a cero como palanca de costo, tagging/labeling para cost allocation.
- Trade-offs reales: serverless vs. Kubernetes gestionado — costo, control,
  complejidad operativa, en cualquiera de las tres nubes.

## Equivalencias multi-cloud

| Pilar | Azure Well-Architected | AWS Well-Architected | GCP Architecture Framework |
|---|---|---|---|
| Confiabilidad | Reliability | Reliability | Reliability |
| Seguridad | Security | Security | Security, Privacy & Compliance |
| Costos | Cost Optimization | Cost Optimization | Cost Optimization |
| Excelencia operacional | Operational Excellence | Operational Excellence | Operational Excellence |
| Rendimiento | Performance Efficiency | Performance Efficiency | Performance Optimization |
| Extra | — | (histórico) Sustainability | AI & ML (pilar adicional propio de GCP) |

## Subtemas

1. Trade-off clásico Cost vs. Reliability: multi-AZ/multi-región cuesta más pero baja el riesgo — ejercicio de justificarlo con números
2. Reserved/Savings Plans/Committed Use Discounts: cuándo tiene sentido comprometerse vs. quedarse on-demand/serverless
3. Tagging/labeling como base de FinOps (cost allocation por equipo/proyecto/ambiente)
4. Disaster Recovery: RTO/RPO, backup vs. multi-región active-active, en cada nube
5. Comparar el "framework de decisión" — los tres ofrecen una herramienta de auto-assessment (Well-Architected Tool en Azure/AWS, Assessment en GCP)

## Recursos

- Azure Well-Architected Framework: https://learn.microsoft.com/azure/well-architected/
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- GCP Architecture Framework: https://cloud.google.com/architecture/framework

## Lab sugerido

Tomá la arquitectura que armaste en los labs de temas anteriores (red +
cómputo serverless + secretos + base de datos + observabilidad) y escribí un
documento corto de decisión (ADR) justificando cada elección desde los 5
pilares — una vez para la versión en Azure, y notá qué cambiaría si la
migraras a AWS o GCP.

## Autoevaluación

Pedime: *"Dame un examen de arquitectura y Well-Architected multi-cloud nivel senior"*.
