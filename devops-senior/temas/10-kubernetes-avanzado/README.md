# Kubernetes — repaso nivel senior

Esta es tu fortaleza (uso en producción de alto volumen en MercadoLibre). El
objetivo acá no es aprender desde cero, sino cerrar huecos específicos que
suelen aparecer en entrevistas senior y no en el uso diario.

## Objetivos (auto-chequeo — si ya dominás esto, saltá directo al examen)

- Scheduling avanzado: affinity/anti-affinity, taints/tolerations, topology spread constraints.
- Resource management: requests vs limits, QoS classes (Guaranteed/Burstable/BestEffort), qué pasa cuando un nodo tiene memory pressure.
- Networking: cómo funciona un Service (ClusterIP/NodePort/LoadBalancer) a nivel de iptables/IPVS, Network Policies, Ingress vs Gateway API.
- Autoscaling: HPA vs VPA vs Cluster Autoscaler — cuándo se pisan entre sí.
- RBAC de Kubernetes (distinto del RBAC de Azure — no confundir en la entrevista).
- Troubleshooting: `CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff` — causa raíz de cada uno.
- Operators y CRDs (concepto, aunque no hayas escrito uno).

## Recursos

- Kubernetes docs: https://kubernetes.io/docs/home/
- Kubernetes API concepts: https://kubernetes.io/docs/reference/using-api/

## Autoevaluación

Pedime: *"Dame un examen de Kubernetes nivel senior/troubleshooting"*.
Este es un buen tema para pedir preguntas **de escenario** ("un pod está en
CrashLoopBackOff, ¿qué revisás primero?") en vez de teóricas puras.
