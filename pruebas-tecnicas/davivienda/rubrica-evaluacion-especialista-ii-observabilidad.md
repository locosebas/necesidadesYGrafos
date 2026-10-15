# Rúbrica de evaluación – Especialista II Observabilidad

> Transcripción fiel de `pdf/rubrica-evaluacion-especialista-ii-observabilidad.pdf`
> (título original del PDF: "Rublica evaluación - Especialista II Observabilidad - 15 junio"; adjunto del
> correo "Proceso de selección Especialista Senior SRE Davivienda", 2026-10-07). El correo siguiente
> ("Corrección caso") reemplazó este adjunto por el caso de uso: este documento parece ser la rúbrica
> interna de la mesa evaluadora para otro caso (PlusPay), enviada por error.

## Filosofía de Evaluación de Banco Plus

Un **Especialista II (Tech Lead)** en una institución de clase mundial debe demostrar un equilibrio perfecto entre **arquitectura avanzada ejecutable (Hands-on)** y **liderazgo cultural por influencia**. Buscamos un profesional propositivo, apasionado por la excelencia técnica y obsesionado con el servicio al desarrollador y la experiencia final del cliente financiero.

## Desglose Ponderado de la Evaluación (Total: 100%)

### ITEM 1: Arquitectura Target, Migración Transparente y Conexión Legacy (Valor: 20%)

- **Contexto Evaluativo:** Mide la capacidad del candidato para resolver el "silo transaccional" de PlusPay y estructurar la migración APM bajo alta presión de tiempo (3 meses).
- 🚩 **Red Flags (Nivel Medio / Operativo):** Propone migraciones manuales o tipo "Big Bang" (apagar un sistema para encender el otro). Sugiere que los desarrolladores cambien sus librerías app por app. Descarta el AS400 aduciendo que es una caja negra impenetrable.
- ✅ **Green Flags (Nivel Especialista II / Tech Lead):** Domina el uso de **OpenTelemetry Collectors en modo Gateway**. Explica con solvencia la configuración de *pipelines* intermedios para hacer *Dual-Shipping* (enrutamiento simultáneo de telemetría al APM Legacy y al nuevo SaaS) para migrar con cero fricción y sin tocar código de las apps. Propone inyectar/extraer **Trace Context (estándares W3C o B3)** en las cabeceras HTTP o colas de mensajería (MQ) que comunican la nube con el Core Bancario, logrando la trazabilidad distribuida.

### ITEM 2: Observability-Driven Development (ODD) y Business Journeys (Valor: 15%)

- **Contexto Evaluativo:** Evalúa si el candidato puede elevar la conversación de métricas de infraestructura hacia indicadores que entiende el negocio y la Directora de Operaciones.
- 🚩 **Red Flags:** Se limita a hablar de monitorear memoria, uso de CPU o picos de tráfico. Considera que los dashboards de negocio se deben construir manualmente combinando datos después de que ocurre la falla.
- ✅ **Green Flags:** Aplica los principios de **ODD e Instrumentación como Código**. Explica cómo el SDK inyecta metadatos transaccionales para que el Gateway correlacione de inmediato la latencia técnica con un *Business Journey* en tiempo real (ej: caídas en el embudo de conversión de pagos de PlusPay reflejadas en un catálogo vivo como Symphony o ServiceNow).

### ITEM 3: Privacidad Regulatoria (SFC) y Gobierno de SDKs Corporativos (Valor: 15%)

- **Contexto Evaluativo:** Mide la madurez del candidato en seguridad bancaria ("Security by Design") y en la creación de productos de software reusables para la automatización interna.
- 🚩 **Red Flags:** Confía ciegamente en que los desarrolladores recordarán enmascarar los datos en su código. Sugiere redactar los datos sensibles utilizando las consolas de configuración del proveedor SaaS (lo que implica que la PII ya viajó por internet y violó la norma SFC). Propone manuales estáticos de Confluence para actualizar librerías.
- ✅ **Green Flags:** Diseña procesadores de **PII Masking / Redaction basados en expresiones regulares (Regex) que se ejecutan localmente en el OTel Collector (Edge)**, destruyendo los datos confidenciales transaccionales *antes* de que la telemetría abandone la red segura del banco. Diseña el SDK corporativo como un producto vivo con auto-instrumentación (interceptors/middlewares). Propone un modelo de gobierno basado en **InnerSource** y automatización mediante bots (ej: Renovate o Dependabot) que abren Pull Requests de actualización automática en los 400 repositorios de los Devs ante cambios estructurales.

### ITEM 4: FinOps Técnico y Optimización de Ingesta (Valor: 15%)

- **Contexto Evaluativo:** Evalúa la competencia financiera del candidato para resolver el incremento de costos del 300% exigido de manera tajante por el CFO.
- 🚩 **Red Flags:** Recomienda recortar drásticamente los días de retención global de datos sin analizar el uso, apagar el RUM de la aplicación móvil por completo, o pedirle a los Devs por correo que "borren los logs pesados".
- ✅ **Green Flags:** Implementa con precisión el **Paradigma de Muestreo Post-Análisis (UniSage / Tail-Based Sampling)** en la capa de procesamiento intermedio. Explica detalladamente cómo programar el Collector Gateway para que evalúe las trazas en memoria: descarta el 95-98% de las transacciones exitosas repetitivas y retiene el 100% de las trazas lentas, anomalías y errores del 12% de PlusPay. Propone transformar cadenas de logs repetitivas en métricas en tiempo real (**Log-to-Metrics**) en el Edge para salvaguardar la visibilidad reduciendo el costo de almacenamiento en un 60%.

### ITEM 5: Preparación para la IA y Observabilidad Cognitiva (Valor: 10%)

- **Contexto Evaluativo:** Mide la visión estratégica a largo plazo para sentar las bases hacia la automatización autónoma y remediación del roadmap 2026-2027 del banco.
- 🚩 **Red Flags:** Confunde AIOps con simplemente encender las alertas predictivas básicas que vienen por defecto en la interfaz de la herramienta comercial.
- ✅ **Green Flags:** Diseña la telemetría bajo un estándar estricto de **MTL (Metadata Tagging & Labeling)** y normalización semántica universal. Explica que un dato limpio, con taxonomía coherente y marcas temporales (*time-stamps*) milimétricamente sincronizadas, es el requisito obligatorio para alimentar **grafos de topología vivos** que nutran modelos de **IA Causal e IA Agéntica**, permitiendo en el futuro flujos de auto-remediación (Self-Healing y Circuit Breakers automáticos) sin falsos positivos.

### ITEM 6: Influencia sin Autoridad y Topología de Plataformas (Valor: 10%)

- **Contexto Evaluativo:** Mide las habilidades blandas de liderazgo técnico, empatía y la gestión de la resistencia al cambio con ingenieros tradicionales y Tribus de desarrollo.
- 🚩 **Red Flags:** Muestra frustración o arrogancia ante los ingenieros tradicionales. Sugiere que el VP de Ingeniería emita un mandato u orden obligatoria para forzar a los desarrolladores a instrumentar.
- ✅ **Green Flags:** Entiende su rol como un habilitador bajo el marco de **Team Topologies**. Propone un liderazgo servicial: realiza sesiones de *Pair-Programming* (programación en parejas) y talleres prácticos con sus ingenieros tradicionales para co-crear las plantillas base de Terraform/Helm. Demuestra que al automatizar los dashboards comunes, el equipo tradicional verá el valor de convertirse en Ingenieros de Plataforma. Utiliza la estrategia de **Error Budgets (Presupuestos de Error)** compartidos para alinear los incentivos de velocidad de desarrollo con la estabilidad operativa de PlusPay.

### ITEM 7: Rediseño del On-Call y Eliminación de Toil (Valor: 15%)

- **Contexto Evaluativo:** Evalúa la capacidad operativa del candidato para rescatar al equipo del burnout y sacarlo de tareas puramente transaccionales de mesa de ayuda.
- 🚩 **Red Flags:** Acepta mantener el flujo operativo basado en tickets manuales de Jira. Propone "poner turnos rotativos más justos" para hacer dashboards o ventanas de mantenimiento, manteniendo la naturaleza reactiva del equipo.
- ✅ **Green Flags:** Diseña una estrategia contundente para **eliminar y automatizar el Toil**. Lleva las funciones operativas (creación de dashboards base, ventanas de mantenimiento, alertas estándar) al **Portal de Autoservicio (Symphony IDP)** mediante plantillas pre-aprobadas, empoderando al desarrollador. Establece el principio **"You build it, you run it"**: las Tribus atienden directamente sus SLOs de aplicación, y el equipo de observabilidad solo es alertado si la infraestructura central de telemetría falla. Establece que el tiempo libre en las guardias se utilizará para ingeniería proactiva: codificación de runbooks (*Runbook as Code*), simulacros controlados de caos y refinamiento de reglas de supresión inteligente de ruido.

## Resumen de Puntuación para la Mesa Evaluadora

| Pilar | Items | Peso | Foco |
|---|---|---|---|
| Pilar A | 1, 2, 3 | 50% | Arquitectura, Negocio y Privacidad |
| Pilar B | 4, 5 | 25% | FinOps, Eficiencia e IA-Readiness |
| Pilar C | 6, 7 | 25% | Liderazgo, Cultura, On-Call y Reducción de Toil |

**Puntaje Mínimo de Aprobación para Contratación:** 85% (Garantiza perfil de clase mundial).
