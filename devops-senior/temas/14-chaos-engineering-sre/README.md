# Chaos Engineering y SRE avanzado

Tema nuevo motivado por la vacante **Chaos & Resilience Engineer**
(Davivienda) — ver `../../00-diagnostico/gap-analysis-davivienda-chaos-sre.md`.
Es una práctica formal de SRE: en vez de esperar a que el sistema falle en
producción, **provocás la falla vos mismo, de forma controlada**, para
encontrar debilidades antes de que las encuentre un usuario.

## Objetivos

- Explicar qué es **chaos engineering** y en qué se diferencia de
  "romper cosas al azar": es un **experimento científico** (hipótesis,
  variable controlada, medición, "blast radius" limitado).
- Explicar **blast radius** (radio de impacto): por qué todo experimento de
  chaos engineering arranca limitado (un pod, un % pequeño de tráfico) y se
  expande gradualmente, nunca directo a "toda la producción".
- Distinguir las herramientas principales del mercado y cuándo se usa cada
  una: **Chaos Monkey** (pionera, Netflix, mata instancias al azar),
  **Litmus** (nativo de Kubernetes, CNCF), **Chaos Mesh** (también nativo de
  K8s, CNCF), **Gremlin** (SaaS comercial, más "enterprise-ready").
- Explicar cómo se **automatiza** un chaos experiment dentro de un pipeline
  CI/CD (correrlo en staging antes de cada release, o en producción de forma
  programada y con "steady-state hypothesis" verificada antes/después).
- Explicar **OpenTelemetry**: qué problema resuelve (instrumentación
  estándar y neutral de vendor para trazas, métricas y logs) y cómo se
  relaciona con lo que ya sabés de Prometheus (Prometheus es un backend de
  métricas; OpenTelemetry es la capa de instrumentación/recolección que
  puede exportar a Prometheus, a Elastic, o a otros backends).
- Explicar **Elastic Stack** (Elasticsearch, Logstash/Beats, Kibana) para
  logging centralizado, y en qué se diferencia del modelo de series
  temporales de Prometheus (logs/texto buscable vs. métricas numéricas).

## Subtemas

1. Principios de chaos engineering: steady-state hypothesis, variables del
   mundo real, minimizar blast radius, automatizar experimentos
2. Tipos de experimentos: latencia inyectada, fallas de red (packet loss),
   terminación de pods/instancias, saturación de CPU/memoria, fallas de
   dependencias externas (simular que un servicio downstream cae)
3. Litmus y Chaos Mesh: `ChaosExperiment`/`ChaosEngine` (Litmus) vs.
   `PodChaos`/`NetworkChaos` (Chaos Mesh) — ambos son operadores nativos de
   Kubernetes (CRDs)
4. Chaos Monkey y la familia "Simian Army" de Netflix (contexto histórico:
   de dónde viene la disciplina)
5. Gremlin: diferencia principal con las opciones open-source (interfaz
   centralizada, "halt" de emergencia, reportes para compliance — relevante
   en un banco como Davivienda)
6. OpenTelemetry: `traces`, `metrics`, `logs` como los "tres pilares",
   `Collector` como pieza central de recolección/exportación
7. Elastic Stack: Elasticsearch (motor de búsqueda/almacenamiento), Beats o
   Logstash (ingesta), Kibana (visualización)
8. AIOps: detección de anomalías, correlación automática de alertas,
   reducción de "alert fatigue" — vocabulario y casos de uso, sin necesidad
   de profundidad de implementación

## Recursos

- Principles of Chaos Engineering (manifiesto de referencia):
  https://principlesofchaos.org/
- Litmus: https://litmuschaos.io/
- Chaos Mesh: https://chaos-mesh.org/
- Gremlin (documentación): https://www.gremlin.com/docs
- OpenTelemetry: https://opentelemetry.io/docs/
- Elastic Stack: https://www.elastic.co/guide/index.html

## Lab sugerido

Sin necesidad de un cluster propio: sobre un cluster Kubernetes local (minikube/kind),
instalá Chaos Mesh o Litmus y corré un experimento simple de tipo
`PodChaos` (matar un pod al azar de un deployment con 3 réplicas).
Observá en Prometheus/Grafana (o en los logs) cómo se recupera el sistema,
y medí cuánto tarda en volver al steady state.

## Autoevaluación

Pedime: *"Dame un examen de chaos engineering nivel intermedio"* o
*"Explicame la diferencia entre Litmus y Chaos Mesh"*.
