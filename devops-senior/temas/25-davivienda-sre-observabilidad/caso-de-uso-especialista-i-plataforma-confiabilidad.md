# Caso de Uso Práctico: Especialista I – Plataforma de Confiabilidad

> Transcripción fiel de `pdf/caso-de-uso-especialista-i-plataforma-confiabilidad-v1.pdf`
> (adjunto del correo "Corrección caso - Proceso de selección Especialista Senior SRE Davivienda", 2026-10-07).

**Empresa:** Banco Plus
**Área:** Dirección de Operaciones y Confiabilidad Tecnológica
**Rol al que postula:** Especialista I - Plataforma de Confiabilidad
**Formato de entrega:** Presentación ejecutiva/técnica (máximo 10 diapositivas) + Exposición oral de 20 minutos ante Mesa Multidisciplinar + 10 minutos de preguntas y respuestas.

## 1. Introducción y Propósito del Ejercicio

Bienvenido al proceso de selección para el rol de Especialista I de Plataforma de Confiabilidad. Este ejercicio práctico busca evaluar tu capacidad técnica, visión estratégica y habilidades de liderazgo técnico para enfrentar los desafíos reales de nuestra arquitectura transaccional distribuida y llevar nuestras prácticas de SRE y Observabilidad al siguiente nivel.

## 2. Contexto Operativo del Banco Plus

Banco Plus se encuentra acelerando la modernización de su plataforma core transaccional hacia una arquitectura nativa de la nube basada en microservicios, desplegada en entornos multi-cloud híbridos (AWS y GCP) y orquestada con Kubernetes. En el último trimestre, debido al crecimiento acelerado del volumen transaccional (pagos digitales, CBU/QR, transferencias en tiempo real), la Dirección de Operaciones ha identificado los siguientes cuatro grandes retos estratégicos:

- **Inestabilidad y falta de salvaguardas en despliegues:** Se presentan frecuentes liberaciones de software que degradan la latencia y disponibilidad de los servicios críticos sin que las herramientas de CI/CD detengan o reviertan automáticamente el paso a producción.
- **Disipación de costos de telemetría (FinOps):** La ingesta masiva y no estructurada de logs, trazas y métricas ha elevado exponencialmente la factura en plataformas cloud sin traducirse en una mejor visibilidad técnica.
- **Tiempos prolongados de resolución de incidentes (MTTR):** Durante las crisis transaccionales, las mesas de ingeniería tardan demasiado tiempo en aislar la causa raíz debido a la fragmentación de la información y la falta de estándares unificados de telemetría distribuida.
- **Evolución hacia AIOps y Automatización Semántica:** Existe la iniciativa institucional de preparar la infraestructura de observabilidad para consumir modelos de Inteligencia Artificial Causal y contextual mediante protocolos modernos que permitan detección predictiva e hiper-automatización.

## 3. Reto Técnico y Estructura de la Presentación

Como Especialista I, deberás diseñar una propuesta integral y exponerla ante la Mesa Multidisciplinar (conformada por Líderes de SRE, Arquitectura, DevSecOps y Operaciones). Tu propuesta debe estar estructurada en torno a los siguientes 4 ejes temáticos obligatorios:

### Eje 1: Gobierno de SLOs, Error Budgets y Quality Gates

- Define los Service Level Indicators (SLIs) y Service Level Objectives (SLOs) para una transacción crítica (ejemplo: Procesamiento de Pagos con QR/CBU), fundamentándose en las Golden Signals (Latencia, Tráfico, Errores y Saturación) y customer centric.
- Diseña el flujo de trabajo para implementar un Quality Gate autoejecutable en el pipeline de CI/CD (GitHub Actions / GitLab CI) que consuma el estado del Error Budget y detenga automáticamente los despliegues cuando la tasa de consumo de presupuesto sea crítica.

### Eje 2: Arquitectura de Telemetría Avanzada y FinOps

- Propón un esquema de arquitectura para la recolección y canalización de telemetría estandarizada utilizando OpenTelemetry (OTel Collector) en un entorno multi-cloud (AWS/GCP / Kubernetes).
- Detalla la estrategia de Smart Sampling (muestreo inteligente basado en cola/cabeza) y filtrado de datos en el borde para reducir costos de almacenamiento e ingesta en un 30% sin perder trazas de errores o anomalías críticas.

### Eje 3: Estandarización Semántica para AIOps y Protocolo MCP

- Describe cómo transformamos la telemetría actual en un formato AI-Ready implementando Model Context Protocol (MCP) u orquestación de contexto semántico.
- Explica de qué manera esta estandarización semántica permitirá alimentar modelos de IA Causal para automatizar el Análisis de Causa Raíz (RCA) y reducir drásticamente el MTTR.

### Eje 4: Comando de Incidentes y Cultura Blameless

- Describe tu plan de acción y liderazgo como Incident Commander durante una interrupción crítica del servicio en hora pico. Incluye la toma de decisiones técnicas de mitigación inmediata.
- Explica cómo lideras la transición posterior al incidente hacia un post-mortem bajo una cultura Blameless (sin culpa), enfocándose en mejoras sistémicas y accionables en el software e infraestructura.

## 4. Lineamientos de Entrega y Evaluación

| Aspecto | Detalle |
|---|---|
| Formato | Presentación gráfica en formato PDF o PPTX (máximo 10 diapositivas). Se valora el uso de diagramas de arquitectura claros (ej. C4 Modelo flujo conceptual). |
| Tiempo de Exposición | 20 minutos de exposición técnica continua. |
| Sesión de Preguntas | 10 minutos de sustentación e interacción con la mesa evaluadora. |
| Criterios Clave | Profundidad técnica, viabilidad de la solución, pragmatismo, claridad de comunicación y liderazgo técnico. |
