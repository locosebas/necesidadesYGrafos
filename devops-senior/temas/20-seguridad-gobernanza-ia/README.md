# Seguridad, guardrails y gobernanza de IA

Extiende el tema 11 (DevSecOps) a sistemas de IA. Los LLMs agregan riesgos
nuevos que no existen en una API tradicional: el **prompt injection** es al
LLM lo que el SQL injection es a una base de datos.

## Objetivos

- Conocer el **OWASP Top 10 for LLM Applications**: **prompt injection**,
  fuga de datos sensibles, output inseguro, agencia excesiva, entre otros.
- Diferenciar **prompt injection directo** (lo escribe el usuario) e
  **indirecto** (viene escondido en un documento o página que el modelo lee).
- Aplicar **guardrails**: filtros de entrada/salida, detección de PII,
  límites de lo que una herramienta/agente puede hacer (mínimo privilegio, como en IAM).
- Privacidad de datos: qué datos se mandan al proveedor del modelo, retención,
  residencia de datos, acceso privado al modelo (Private Endpoint, tema 05).
- Gobernanza: **Responsible AI**, **NIST AI RMF**, **EU AI Act** a nivel
  "qué tengo que saber como ingeniero".

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Guardrails / filtros de contenido | **Azure AI Content Safety** (incluye **Prompt Shields**) | **Bedrock Guardrails** | **Model Armor** |
| Acceso privado al modelo | Private Endpoint a Azure OpenAI | VPC Endpoint (PrivateLink) a Bedrock | Private Service Connect a Vertex AI |
| Detección de datos sensibles | Microsoft Purview | Amazon Macie / Comprehend PII | Sensitive Data Protection (DLP) |
| Identidad del modelo/agente | Managed Identity | IAM Role | Service Account |

## Subtemas

1. OWASP Top 10 for LLM Applications
2. Prompt injection directo e indirecto, y por qué no se "arregla" solo con el prompt
3. Guardrails gestionados: Content Safety, Bedrock Guardrails, Model Armor
4. Agentes seguros: mínimo privilegio en herramientas, confirmación humana, sandboxing
5. Privacidad: PII, retención de datos del proveedor, acceso privado al endpoint
6. Supply chain de modelos: origen de los pesos, escaneo de modelos, licencias
7. Gobernanza: Responsible AI, NIST AI RMF, EU AI Act (nivel ingeniero)

## Recursos

- OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/
- Azure AI Content Safety: https://learn.microsoft.com/azure/ai-services/content-safety/
- Amazon Bedrock Guardrails: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- GCP Model Armor: https://cloud.google.com/security-command-center/docs/model-armor-overview
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework

## Lab sugerido

Atacá tu propio RAG del tema 16: meté en un documento indexado una
instrucción escondida (*"ignorá las instrucciones anteriores y…"*) y mirá si
el modelo la obedece (**prompt injection indirecto**). Después agregá un
guardrail (Bedrock Guardrails, Content Safety o un filtro propio) y medí si lo frena.

## Autoevaluación

Pedime: *"Dame un examen de seguridad de IA nivel intermedio"*.
