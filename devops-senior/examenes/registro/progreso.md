# Nivel de dominio por tema

Esto **no es** "visto / no visto" — es qué tan sólido estás en cada tema
**hoy**, medido por cómo respondiste la última vez que se puso a prueba
(examen, repaso espaciado, o una entrevista real). Sube o baja con el
tiempo; nunca queda fijo en 100% solo porque se explicó una vez.

## Escala

| Nivel | Qué significa |
|---|---|
| 🔴 **Novato** | Recién visto, no se puso a prueba todavía |
| 🟡 **Intermedio** | Repasado, quedan dudas puntuales o no se testeó a fondo |
| 🟢 **Sólido** | Defendible en una entrevista real, sin ayuda |
| 🔵 **Senior** | Lo puede explicar con matices/trade-offs, enseñarlo, sin dudar |

## Kubernetes

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Arquitectura (control plane, nodos, reconciliation loop) | 🟢 Sólido | 2026-09-14/15, sesión guiada completa |
| Scheduling/recursos (QoS, HPA/VPA, RBAC de K8s) | 🟡 Intermedio | Tocado vía `Pending`, sin examen dedicado |
| Networking (Services, Headless, NetworkPolicy, Istio, kube-proxy) | 🟢 Sólido | 2026-09-16/17, varias correcciones bien asimiladas |
| Troubleshooting (`CrashLoopBackOff`, `Pending`, `OOMKilled`) | 🟡 Intermedio | Repasado vía preguntas reales de entrevista, falta sesión dedicada (Fase 8) |
| Operators/CRDs, AKS vs EKS vs GKE | 🟡 Intermedio | Mencionado, no testeado a fondo |

## Redes

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| VNet/VPC, modelo de 3 capas, NSG | 🟢 Sólido | 2026-09-16/17, con diagrama de apoyo |
| Private Endpoint / Private DNS Zone | 🟢 Sólido | Corregiste vos mismo el error de ubicación tras la explicación |
| NAT Gateway, WAF, Firewall centralizado | 🟡 Intermedio | Recién explicado, sin repaso |
| AWS Load Balancers (ALB/NLB/GWLB) | 🟡 Intermedio | Repasado tras fallarlo en entrevista real (EY) |

## Terraform

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| State file, locking, drift, import | 🟢 Sólido | 2026-09-24/25, buenas respuestas propias antes de la corrección |
| Backends multi-cloud (S3/Blob/GCS) | 🟢 Sólido | Explicaste vos mismo el mecanismo de DynamoDB |
| Buenas prácticas y ecosistema (Terragrunt, tflint, Terratest, Atlantis, Infracost) | 🟡 Intermedio | Recién explicado en profundidad, sin repaso |

## Arquitectura / Platform Engineering

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Arquitectura completa (frontend+backend, diagrama grande) | 🟡 Intermedio | Construida junto con vos, no evaluada de forma independiente |
| Compute hierarchy y curva de costos (VM→K8s→serverless→FaaS→PaaS) | 🟡 Intermedio | Explicado con gráfico, sin examen |
| Variante serverless de la arquitectura | 🟡 Intermedio | Explicado, sin repaso |

## Otros

| Tema | Nivel | Última vez puesto a prueba |
|---|---|---|
| Distribuciones de Kubernetes (AKS/EKS/GKE/OpenShift/k3s) | 🟢 Sólido | Diste la respuesta correcta en inglés sin ayuda |
| Proxies (NGINX/HAProxy/Envoy) | 🟡 Intermedio | Explicado a fondo, sin repaso |
| Replicación vs. sharding de bases de datos | 🟡 Intermedio | Explicado, sin repaso |

---

**Cómo se actualiza**: cada vez que se hace un repaso espaciado o un examen
de práctica, se revisa este archivo — un tema sube de nivel si lo
respondiste bien **sin ayuda**, se mantiene si tuviste que pensarlo mucho, y
puede bajar si quedó claro que se te olvidó. Pendiente de definir la
frecuencia del repaso espaciado con el usuario (ver `resultados.md`).
