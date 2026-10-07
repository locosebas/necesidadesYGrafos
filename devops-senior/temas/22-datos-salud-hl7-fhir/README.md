# Dominio salud: HL7, FHIR e interoperabilidad clínica

Tema **de dominio** (como el 13 de MercadoLibre): solo hace falta si apuntás a
ofertas de salud / healthtech. No hace falta ser experto clínico; las ofertas
piden *exposure*: conocer los estándares, las herramientas y las
restricciones de seguridad y compliance que imponen los datos de pacientes.

## Objetivos

- Explicar qué es **HL7 v2** (mensajes de texto delimitados por `|`,
  estándar viejo pero todavía el más usado en hospitales) y qué es **FHIR**
  (estándar moderno, API REST + JSON, organizado en *resources*).
- Conocer los **resources** principales de **FHIR**: `Patient`,
  `Practitioner`, `Encounter`, `Observation`, `Condition`,
  `MedicationRequest`, `Bundle`.
- Saber qué es un **FHIR server** (**HAPI FHIR**, **Medplum**) y qué es un
  **motor de integración** (**OIE**, Mirth Connect): el que traduce HL7 v2 ↔ FHIR
  entre sistemas.
- Entender por qué los datos de salud son **PHI** (Protected Health
  Information) y qué implica para la plataforma: cifrado, auditoría, acceso
  mínimo, residencia de datos (**HIPAA** en EE.UU.; en Latinoamérica, leyes de
  datos personales sensibles).

## Herramientas

| Herramienta | Qué es |
|---|---|
| **HAPI FHIR** | Implementación open source de referencia de **FHIR** en Java; se usa como **FHIR server** o como librería |
| **Medplum** | Plataforma open source para apps de salud construida sobre **FHIR** (FHIR server + auth + bots + SDK TypeScript); muy usada por startups |
| **OIE (Open Integration Engine)** | Motor de integración open source, fork comunitario de **Mirth Connect** (que pasó a licencia comercial en 2025). Recibe mensajes **HL7 v2**, los transforma y los manda a otros sistemas (por ejemplo, a un **FHIR server**) |
| **SMART on FHIR** | Estándar de autorización (sobre **OIDC/OAuth2**, tema 04 y **Keycloak**) para apps que acceden a datos FHIR |

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| FHIR server gestionado | **Azure Health Data Services** (FHIR service) | **AWS HealthLake** | **Cloud Healthcare API** (FHIR stores) |
| HL7 v2 gestionado | Azure Health Data Services (conversión `$convert-data`) | — (se resuelve con integración propia) | Cloud Healthcare API (HL7v2 stores) |
| Compliance | HIPAA BAA | HIPAA BAA | HIPAA BAA |

## Subtemas

1. HL7 v2: estructura de un mensaje (segmentos `MSH`, `PID`, `OBX`), tipos de mensaje (`ADT`, `ORU`)
2. FHIR: resources, REST API (`GET /Patient/123`), búsquedas, `Bundle`, profiles
3. FHIR servers: **HAPI FHIR** vs. **Medplum** vs. los gestionados de cada nube
4. Integración: **OIE** / Mirth Connect, canales, transformación HL7 v2 → FHIR
5. Seguridad y compliance de **PHI**: cifrado en reposo/tránsito, logs de auditoría, de-identificación, BAA con el proveedor de nube
6. **SMART on FHIR** y autorización con **Keycloak**

## Recursos

- HL7 FHIR (especificación): https://hl7.org/fhir/
- HAPI FHIR: https://hapifhir.io/
- Medplum: https://www.medplum.com/docs
- Open Integration Engine: https://github.com/OpenIntegrationEngine/engine
- Azure Health Data Services: https://learn.microsoft.com/azure/healthcare-apis/

## Lab sugerido

Levantá **HAPI FHIR** (o **Medplum**) en Docker, creá un `Patient` y un
`Observation` por la API REST, y buscalos. Después pasá un mensaje **HL7 v2**
`ADT^A01` de ejemplo por **OIE** y transformalo en un `Patient` de **FHIR**.

## Autoevaluación

Pedime: *"Dame un examen de HL7/FHIR nivel básico"*. Igual que el tema 13,
este tema **no entra** en los diagnósticos generales salvo que lo pidas.
