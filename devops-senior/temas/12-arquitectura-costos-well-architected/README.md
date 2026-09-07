# Arquitectura y costos — Well-Architected Framework

Nivel senior implica poder justificar decisiones de arquitectura más allá de
"funciona": costo, resiliencia, operabilidad.

## Objetivos

- Explicar los 5 pilares del Azure Well-Architected Framework: Reliability,
  Security, Cost Optimization, Operational Excellence, Performance Efficiency.
- Diseñar para alta disponibilidad: Availability Zones vs regiones, SLA
  compuesto de una arquitectura multi-servicio.
- FinOps básico: reserved instances/savings plans, autoscale a cero (Container
  Apps/serverless) como palanca de costo, tagging para cost allocation.
- Trade-offs reales: serverless (Container Apps/Functions) vs AKS dedicado —
  costo, control, complejidad operativa.
- Disaster Recovery: RTO/RPO, backup vs multi-region active-active.

## Recursos

- Azure Well-Architected Framework: https://learn.microsoft.com/azure/well-architected/

## Lab sugerido

Tomá la arquitectura completa que fuiste armando en los labs anteriores
(VNet + Container Apps + Key Vault + Cosmos DB + Monitor) y escribí un
documento corto de decisión (ADR) justificando cada elección desde los 5
pilares del Well-Architected Framework.

## Autoevaluación

Pedime: *"Dame un examen de arquitectura Azure y Well-Architected nivel senior"*.
