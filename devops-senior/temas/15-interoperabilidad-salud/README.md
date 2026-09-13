# Interoperabilidad de datos de salud: HL7/FHIR, Medplum, HAPI FHIR

> Nota: a diferencia de los demás temas (conceptos DevOps multi-cloud), este
> es **conocimiento de dominio** (healthcare/health-tech) que aparece como
> "plus" en vacantes puntuales de startups de salud — no es un requisito
> DevOps en sí, pero ayuda a entender qué construye la plataforma que vas a
> operar. Tratamiento similar a `13-mercadolibre-scopes-cosmos`: contexto de
> una vacante concreta, no parte del roadmap general de fases.

## Contexto

Una vacante puede pedir experiencia con estos términos cuando la plataforma
que vas a construir/operar maneja datos clínicos (historias clínicas,
resultados de laboratorio, etc.) y necesita hablar el estándar del rubro
salud, no formatos propios.

## Conceptos

- **HL7 (Health Level 7)**: familia de estándares para intercambiar datos
  clínicos entre sistemas (por ejemplo, entre un hospital y un laboratorio).
  La versión antigua (HL7 v2) usa un formato de texto propio poco amigable;
  la versión moderna es **FHIR**.
- **FHIR (Fast Healthcare Interoperability Resources)**: estándar moderno
  (HL7 lo publica) basado en **recursos** con forma de **JSON/XML sobre una
  API REST** (`Patient`, `Observation`, `Encounter`, etc.) — mucho más
  cercano a como ya trabajás con APIs REST/FastAPI (tema 08) que HL7 v2.
- **HAPI FHIR**: implementación **Java** de referencia, open-source, de un
  servidor FHIR — la más usada para levantar un servidor FHIR propio.
- **Medplum**: plataforma open-source "todo-en-uno" para health-tech
  (servidor FHIR + auth + UI de administración + SDKs), pensada para que una
  startup no tenga que construir el servidor FHIR desde cero — competidor
  directo de montar HAPI FHIR a mano.

## Cómo se conecta con el resto del plan

- El servidor FHIR (HAPI o Medplum) es una app más para desplegar/operar:
  aplica todo lo demás del plan (Kubernetes/contenedores, IaC, CI/CD,
  identidad, observabilidad, secretos) — FHIR no cambia el "cómo" de DevOps,
  cambia "qué" corre arriba.
- Datos clínicos = datos sensibles: reforzar mínimo privilegio (tema 04),
  cifrado y gestión de secretos (tema 06), y compliance (relevante en
  healthcare: HIPAA en EE.UU., no cubierto en este plan salvo que lo pidas).

## Recursos

- FHIR overview: https://www.hl7.org/fhir/overview.html
- HAPI FHIR: https://hapifhir.io/
- Medplum: https://www.medplum.com/docs

## Autoevaluación

Este tema es opcional/contextual — no hace falta un examen formal salvo que
una vacante puntual lo requiera. Si querés, pedime: *"Explicame FHIR como si
nunca hubiera visto una API REST de salud"*.
