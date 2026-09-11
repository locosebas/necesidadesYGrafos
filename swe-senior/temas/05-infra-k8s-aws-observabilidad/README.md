# Infraestructura: Kubernetes, AWS y observabilidad (repaso)

Estos tres ya son **fortalezas documentadas** en
`../../devops-senior/temas/10-kubernetes-avanzado/` y
`../../devops-senior/temas/07-observabilidad-multicloud/` — esta carpeta no
los duplica. Este tema es solo un repaso rápido más las particularidades de
aplicarlos a un servicio Clojure/JVM en este rol.

## Objetivos

- Repasar lo ya cubierto en `devops-senior/` (no reaprender de cero):
  Kubernetes en producción, AWS, Prometheus.
- Particularidades de una app **JVM/Clojure** corriendo en Kubernetes: JVM
  heap sizing vs. límites de memoria del contenedor (`-Xmx` vs.
  `resources.limits.memory`), tiempo de arranque (JVM warm-up) y su impacto
  en probes (`readinessProbe`/`livenessProbe`) y en autoscaling.
- Métricas específicas a exponer en Prometheus para un servicio JVM: GC
  pauses, heap usage, thread pool saturation (relevante si el servicio usa
  Finagle) — además de las métricas de negocio/latencia ya conocidas.
- Guardias/rotación de on-call: la vacante menciona explícitamente
  "participating in on-call incident response rotations".

## Subtemas

1. Repaso dirigido: pedime examen de
   `devops-senior/temas/10-kubernetes-avanzado` si hace tiempo que no lo
   repasás.
2. JVM en contenedores: heap sizing, `-XX:+UseContainerSupport`, por qué un
   JVM mal configurado puede ser OOMKilled aunque el heap "declarado" sea
   menor al límite del contenedor
3. Métricas JVM en Prometheus: JMX exporter o métricas nativas de Clojure
   (`metrics-clojure`), GC pauses como señal de salud
4. On-call: runbooks, SLOs/SLIs, qué hace que una alerta sea "accionable"
   (actionable) en vez de ruido

## Recursos

- Repaso: `../../devops-senior/temas/10-kubernetes-avanzado/README.md` y
  `../../devops-senior/temas/07-observabilidad-multicloud/README.md`
- JVM en contenedores (guía de tuning): https://docs.oracle.com/en/java/javase/17/gctuning/
- Prometheus JMX Exporter: https://github.com/prometheus/jmx_exporter

## Autoevaluación

Pedime: *"Dame un examen de JVM en Kubernetes (heap sizing y probes)"*, o
si necesitás repasar la base, *"Dame un examen de Kubernetes nivel senior"*
(mismo formato que en `devops-senior/`).
