# Fase 1 — Caracterización de la necesidad de Dapta

> Se llena **de a una pregunta**, con lo que tú sabes de la entrevista. Lo que no sepamos queda como
> **pregunta para la siguiente entrevista** (eso también suma: muestra criterio).
> Columna "Fuente": 🌐 pública · 🗣️ entrevista · ❓ hipótesis sin validar.

## 1. Negocio: ¿quién compra y qué le exige?

| # | Pregunta | Respuesta | Fuente |
|---|---|---|---|
| 1.1 | ¿Qué certificaciones/requisitos exigen los compradores que hoy Dapta no logra cumplir? | No lo concretaron. Lo que sí dijeron del cargo: hay una **migración a Temporal** en curso, y el cargo debe **entender la infraestructura** y montar un **proceso confiable de desarrollo y despliegue**. Lectura: el SDLC (Software Development Life Cycle) y el CI/CD son la **evidencia** de los controles de SOC 2 "Change management procedures enforced", "Development lifecycle established" y "Production deployment access restricted" | 🗣️ |
| 1.2 | ¿Quiénes son esos compradores (segmento, país, vertical: salud, cobranza, fintech...)? | | |
| 1.3 | ¿Cuántos negocios se han perdido o frenado por esto? ¿Hay una fecha límite (un contrato grande esperando)? | | |
| 1.4 | ¿Cómo sacaron el SOC 2 Type II (Vanta + consultor + auditor)? ¿Quién lo mantiene hoy? | | |

## 2. Organización: ¿quién hace qué?

| # | Pregunta | Respuesta | Fuente |
|---|---|---|---|
| 2.1 | ¿Qué es exactamente "ataque" y "defensa"? (¿red team / blue team, o producto vs. plataforma?) | | |
| 2.2 | ¿Hay alguien de seguridad hoy? ¿A quién reportaría el cargo (CTO, CEO)? | | |
| 2.3 | ¿Cómo trabajan los ~14 desarrolladores (equipos, despliegues por día, on-call)? ¿Cómo despliegan hoy? | Dato de la entrevista: migración a Kubernetes en curso, junto con la de Temporal. Proceso actual de despliegue: por preguntar | 🗣️ |

## 3. Técnica: ¿sobre qué corre?

| # | Pregunta | Respuesta | Fuente |
|---|---|---|---|
| 3.1 | Nube y cómputo: AWS confirmado (subservice provider del SOC 2); ¿ECS, EKS, Lambda? ¿IaC (Terraform)? | AWS 🌐. **Están "kubernetizando"**: migración a Kubernetes en curso (¿EKS? ¿desde qué?) 🗣️ | 🌐 🗣️ |
| 3.2 | Voz en tiempo real: LiveKit + Twilio + Deepgram (según subprocesadores) | | 🌐 ❓ |
| 3.3 | LLMs: OpenAI, Anthropic, Gemini, Groq. ¿Con retención cero de datos (ZDR, Zero Data Retention)? | | 🌐 ❓ |
| 3.4 | Identidad: WorkOS (SSO, Single Sign-On, para clientes). ¿Y para empleados (Google Workspace, MFA)? | | 🌐 ❓ |
| 3.5 | Observabilidad: Grafana Labs, PostHog, Metabase. ¿SIEM (Security Information and Event Management)? | | 🌐 ❓ |
| 3.6 | Datos sensibles: grabaciones, transcripciones, datos de CRM de los clientes. ¿Dónde viven, cuánto tiempo, cifrados con qué llaves? | | |
| 3.7 | **Migración a Temporal** (workflows durables; Temporal ya es subprocesador → ¿Temporal Cloud?). ¿Qué se migra (llamadas, secuencias, campañas)? ¿Desde qué (colas, cron, código propio)? | En curso | 🗣️ |

## 4. Riesgos propios de un producto de voz con IA

| # | Riesgo | ¿Lo cubre algún control hoy? |
|---|---|---|
| 4.1 | PII y datos de salud/financieros dentro de grabaciones y transcripciones | ❓ |
| 4.2 | Datos de clientes enviados a proveedores de LLM (subprocesadores, retención, entrenamiento) | ❓ |
| 4.3 | Prompt injection por voz o por WhatsApp (el que llama manipula al agente) | ❌ ningún control de IA |
| 4.4 | Fuga entre clientes (multi-tenancy): un agente que ve datos de otra cuenta | ❓ |
| 4.5 | Consentimiento de grabación y TCPA / leyes de llamadas en EE. UU.; Ley 1581 en Colombia | ❓ |
| 4.6 | Fraude telefónico y abuso de la plataforma (llamadas masivas, spam, suplantación) | ❓ |
| 4.7 | Secretos de integraciones (tokens de HubSpot, Salesforce, GoHighLevel de cada cliente) | ❓ |

## Síntesis (se escribe al final de la fase)

_Pendiente._
