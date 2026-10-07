# Agentes de IA y MCP (Model Context Protocol)

Un **agente** es un LLM que decide qué herramientas usar, en loop, hasta
cumplir un objetivo. Conecta con el tema 09 (orquestación): un agente es otra
forma de orquestar pasos, pero el que decide el siguiente paso es el modelo,
no un flujo fijo. Saber **cuándo NO usar un agente** es tan importante como
saber construirlo.

## Objetivos

- Explicar la diferencia entre **workflow** (pasos fijos definidos por vos) y
  **agente** (el LLM elige los pasos), y cuándo conviene cada uno.
- Construir un agente con **tool use** en loop: herramientas, memoria,
  condición de corte, límite de pasos/costo.
- Entender **MCP (Model Context Protocol)**: servidores MCP, clientes, cómo
  exponer una herramienta interna (por ejemplo, la API de tu plataforma) a
  cualquier agente.
- Patrones multi-agente: orquestador + subagentes, y sus costos.
- Operar agentes en producción: trazabilidad de cada paso, timeouts,
  **human-in-the-loop** para acciones riesgosas.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Servicio gestionado de agentes | **Azure AI Foundry Agent Service** | **Bedrock Agents** / **Bedrock AgentCore** | **Vertex AI Agent Engine** (Agent Builder) |
| Framework / SDK propio | Microsoft Agent Framework (Semantic Kernel / AutoGen) | Strands Agents | **ADK** (Agent Development Kit) |
| Frameworks agnósticos | LangGraph, Claude Agent SDK, OpenAI Agents SDK | ídem | ídem |
| Protocolo de herramientas | **MCP** (soportado en las tres) | **MCP** | **MCP** |

## Subtemas

1. Workflow vs. agente: árbol de decisión (empezar simple)
2. Loop de agente: tool use, observación, siguiente acción, criterio de parada
3. **MCP**: arquitectura cliente/servidor, escribir un servidor MCP en Python
4. Memoria: de corto plazo (contexto) y de largo plazo (RAG, tema 16)
5. Multi-agente: orquestador + subagentes, cuándo vale la pena
6. Producción: tracing de pasos, límites de costo, idempotencia de herramientas, human-in-the-loop
7. Agentes para DevOps: agentes que leen logs, abren PRs, hacen triage de incidentes

## Recursos

- Anthropic — Building effective agents: https://www.anthropic.com/research/building-effective-agents
- Model Context Protocol: https://modelcontextprotocol.io/
- Bedrock AgentCore: https://docs.aws.amazon.com/bedrock-agentcore/
- Azure AI Foundry Agent Service: https://learn.microsoft.com/azure/ai-foundry/agents/
- Google ADK: https://google.github.io/adk-docs/

## Lab sugerido

Escribí un **servidor MCP** en Python que exponga dos herramientas de
operación (por ejemplo, `listar_pods_con_error` y `ver_logs_pod` sobre un
cluster local de `kind`) y conectalo a un agente. Pedile: *"¿por qué está
fallando el pod X?"*. De paso repasás el troubleshooting de Kubernetes
(pendiente del tema 10).

## Autoevaluación

Pedime: *"Dame un examen de agentes de IA y MCP nivel intermedio"*.
