# Material interno MercadoLibre — Scopes & CoSMOS

> ⚠️ **Confidencial.** Documento interno de MercadoLibre (equipo Scopes Govern),
> incluido en este repo privado por decisión explícita del dueño. No compartir,
> no hacer público este repositorio sin eliminar esta carpeta antes.

`preguntas-entrevista-scopes-cosmos.md` es el documento original, tal cual se
obtuvo de Drive: preguntas de entrevista + respuestas esperadas sobre la
plataforma interna de scopes/infraestructura de MercadoLibre (ciclo de vida de
un Scope, estrategias de deploy, sharding, Instance Groups, observabilidad,
reglas SRE, troubleshooting, etc.).

## Por qué está en este repo de estudio DevOps

Aunque los nombres son específicos de MercadoLibre, los **conceptos** son
100% transferibles a un rol Senior DevOps/Platform Engineer en cualquier
empresa:

- Máquina de estados para el ciclo de vida de un recurso de infraestructura
- Estrategias de deploy (blue/green, canary) y qué es un "Instance Group" en la práctica
- Sharding/segmentación de infraestructura por aislamiento de fallas
- Reglas operacionales tipo SRE ("irrevocables") como forma de codificar buenas prácticas
- Observabilidad y troubleshooting de una plataforma multi-tenant

## Cómo usarlo

- Como preparación si en algún momento te postulás/entrevistás para ese
  equipo internamente.
- Como **caso de estudio real** de diseño de plataforma senior — muchas de
  las preguntas ahí (ciclo de vida, deploy strategies, sharding) son el mismo
  tipo de pregunta que te pueden hacer en cualquier entrevista senior de
  Platform Engineering, aunque cambien los nombres propios.

## Autoevaluación

Pedime: *"Dame un examen basado en el documento de Scopes/CoSMOS"* — puedo
generar preguntas directamente desde ese material.
