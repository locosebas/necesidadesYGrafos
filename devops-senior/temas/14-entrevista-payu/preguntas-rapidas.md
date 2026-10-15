# Preguntas rápidas — ronda de fuego

Banco de preguntas cortas con respuesta de **1-3 líneas**. Objetivo: que la
respuesta salga automática, sin "eh...". Practicar en voz alta, tapando la
respuesta.

## Cómo sonar con expertise (la fórmula)

1. **Respuesta directa primero** (1 frase). Nada de rodeos.
2. **El porqué** (1 frase).
3. **Un ejemplo propio** ("En MercadoLibre lo hicimos así...") o un trade-off.
4. **Callarte.** Dejar que repregunten; respuestas cortas y seguras > largas y dudosas.

Muletillas a cambiar:

| En vez de... | Decí... |
|---|---|
| "Creo que es..." | "Es..." |
| "No sé si está bien, pero..." | "Lo que yo haría es..." |
| "No sé" (a secas) | "No lo usé en producción, pero entiendo que funciona así... y lo validaría con..." |
| "Eh... eh..." | Pausa de 2 segundos en silencio (suena a que pensás, no a que dudás) |

---

## Terraform

1. **¿Qué es el state?** → El mapa entre el código y los recursos reales; Terraform lo usa para calcular el diff en el `plan`.
2. **¿Dónde guardás el state?** → Backend remoto con lock y cifrado: S3 + lock (DynamoDB o `use_lockfile`), nunca local ni en git.
3. **¿Para qué sirve el lock?** → Evita que dos `apply` modifiquen el mismo state a la vez y lo corrompan.
4. **Workspaces vs carpetas por ambiente?** → Prefiero carpetas + cuentas separadas: aislamiento real de credenciales y state; workspaces es fácil equivocarse.
5. **¿Qué es un módulo?** → Código reutilizable con inputs/outputs; se versiona por tag.
6. **Data source vs resource?** → Resource crea/gestiona; data source solo lee algo que ya existe.
7. **¿Qué es drift?** → Diferencia entre el state y la realidad por cambios manuales; se detecta con `plan` programado.
8. **¿Cómo importás algo creado a mano?** → Bloque `import {}` (o `terraform import`) y luego escribir el resource hasta que el plan dé sin cambios.
9. **¿Cómo renombrás un recurso sin destruirlo?** → Bloque `moved {}`.
10. **¿Cómo protegés una base de datos de un destroy?** → `prevent_destroy` + `deletion_protection` del proveedor + revisión del plan.
11. **¿Qué es `.terraform.lock.hcl`?** → Fija las versiones exactas de providers; se commitea.
12. **`count` vs `for_each`?** → `for_each` con mapas: quitar un elemento no reindexa ni recrea los demás.
13. **¿Cómo manejás secretos?** → Fuera del código (Secrets Manager/Vault), variables `sensitive`, y proteger el state porque puede contenerlos.
14. **¿Terraform tiene rollback?** → No nativo: revertís el commit y aplicás de nuevo.
15. **¿Qué es Terragrunt?** → Wrapper que evita repetir backends/providers entre muchos stacks y maneja dependencias entre ellos.

## Kubernetes

16. **Componentes del control plane?** → kube-apiserver, etcd, kube-scheduler, kube-controller-manager (+ cloud-controller-manager en nube).
17. **Componentes de un nodo?** → kubelet, kube-proxy y el container runtime (containerd).
18. **¿Qué es etcd?** → Base clave-valor donde vive todo el estado del clúster; se respalda.
19. **¿Qué hace el scheduler?** → Elige el nodo para cada pod según recursos, affinity, taints y tolerations.
20. **¿Qué hace el kubelet?** → Agente del nodo: corre los pods asignados vía el runtime, ejecuta probes y reporta estado.
21. **¿Qué hace kube-proxy?** → Implementa los Services con reglas iptables/IPVS.
22. **¿Qué es un CNI y por qué es obligatorio?** → Plugin de red que da IP a los pods y los conecta; sin él los nodos quedan `NotReady`. Ej.: Calico, Cilium, AWS VPC CNI.
23. **¿Por qué ya no Docker?** → Desde 1.24 se quitó dockershim; se usa un runtime CRI (containerd/CRI-O). Las imágenes Docker siguen sirviendo.
24. **Deployment vs StatefulSet vs DaemonSet?** → Deployment: apps sin estado; StatefulSet: identidad y disco estables (bases, Kafka); DaemonSet: un pod por nodo (agentes de logs, monitoreo).
25. **Tipos de Service?** → ClusterIP (interno), NodePort (puerto en cada nodo), LoadBalancer (LB del cloud); Ingress/Gateway para HTTP.
26. **Liveness vs readiness?** → Liveness: si falla, reinicia el contenedor. Readiness: si falla, lo saca del Service sin reiniciarlo.
27. **Requests vs limits?** → Requests: lo que se reserva para el scheduling. Limits: el máximo; pasarse de memoria = OOMKilled.
28. **CrashLoopBackOff?** → El contenedor arranca y muere en loop; miro `logs --previous` y el exit code.
29. **Exit code 137?** → SIGKILL, casi siempre OOMKilled por superar el límite de memoria.
30. **Pod en Pending?** → No se puede agendar: sin recursos, taints, affinity o PVC sin bindear; lo veo en `describe pod`.
31. **HPA vs VPA vs Cluster Autoscaler?** → HPA: más pods; VPA: ajusta requests; CA/Karpenter: más nodos.
32. **¿Qué es un PDB?** → PodDisruptionBudget: mínimo de pods disponibles durante drenados/upgrades.
33. **ConfigMap vs Secret?** → Configuración vs datos sensibles (base64, no cifrado por defecto: activar cifrado en etcd o usar External Secrets).
34. **Taints y tolerations?** → El taint repele pods de un nodo; solo los que tienen la toleration entran (ej. nodos GPU).
35. **¿Qué es un Operator?** → Controlador + CRD que automatiza la operación de una app compleja (ej. Postgres, Prometheus).
36. **¿Qué es GitOps?** → Git como fuente de verdad; Argo CD/Flux sincronizan el clúster con el repo.

## Troubleshooting

37. **¿Qué es lo primero que hacés en un incidente?** → Medir impacto, preguntar qué cambió, y mitigar (rollback) antes de investigar.
38. **¿Qué son los golden signals?** → Latencia, tráfico, errores y saturación.
39. **Un Service no responde, ¿qué revisás?** → `get endpoints`: si está vacío, el selector no coincide con los labels o la readiness falla.
40. **¿Qué es un postmortem blameless?** → Análisis del incidente enfocado en el sistema y no en culpables, con acciones concretas.
41. **¿Alertar por causa o por síntoma?** → Por síntoma (errores, latencia vs SLO); CPU alta sola no despierta a nadie.

## AWS y multi-cuenta

42. **¿Por qué varias cuentas?** → Aislamiento (blast radius), cuotas separadas, costos por equipo y compliance (PCI).
43. **¿Qué es una SCP?** → Política de Organizations que limita lo que *cualquiera* puede hacer en una cuenta, incluso el admin. Ej.: prohibir desactivar CloudTrail.
44. **¿Qué es Control Tower?** → Landing zone: crea cuentas con guardrails, logging centralizado y SSO ya configurados.
45. **¿Cómo acceden los humanos?** → IAM Identity Center (SSO) con permission sets; sin usuarios IAM con access keys.
46. **¿Cómo accede un pod a S3?** → IRSA o EKS Pod Identity: el service account asume un rol IAM, sin llaves.
47. **Security Group vs NACL?** → SG: por instancia, stateful. NACL: por subnet, stateless, reglas allow/deny.
48. **¿Qué es un VPC endpoint?** → Acceso privado a servicios de AWS (S3, ECR) sin salir a internet ni pasar por NAT.
49. **Multi-AZ vs multi-región?** → Multi-AZ: alta disponibilidad ante caída de una zona. Multi-región: DR ante caída de una región; más caro y complejo.
50. **RPO vs RTO?** → RPO: cuántos datos puedo perder. RTO: cuánto tiempo puedo estar caído.

## CI/CD

51. **¿Qué no puede faltar en un pipeline?** → Build reproducible, lint, tests, escaneo de seguridad, artefacto versionado, deploy con aprobación y rollback.
52. **¿Qué es "build once, deploy many"?** → Se construye un artefacto una vez y se promueve el mismo por dev → staging → prod.
53. **¿Cómo se autentica el pipeline a AWS?** → OIDC: GitHub Actions asume un rol IAM con token temporal; sin secretos estáticos.
54. **Blue/green vs canary?** → Blue/green: cambio de todo el tráfico entre dos entornos. Canary: un % pequeño primero y se sube según métricas.
55. **¿Qué es shift-left?** → Mover la seguridad y calidad al inicio: SAST, SCA, escaneo de IaC e imágenes en el PR.
56. **SAST vs SCA vs DAST?** → SAST: analiza tu código. SCA: tus dependencias. DAST: la app corriendo.
57. **¿Pipeline de Terraform en una frase?** → Plan en el PR con escaneos, revisión humana, apply del mismo plan al mergear, con aprobación para prod.

---

## Cómo practicar

- **Ronda de fuego conmigo**: pedime "ronda rápida de Kubernetes" (o de lo
  que sea): te hago 10 preguntas de a una, respondés en 1-2 frases, y te
  corrijo al final con puntaje.
- **En voz alta**: 10 minutos por día, tapando la respuesta. Las que falles,
  marcalas con ❌ acá y repetilas al día siguiente.
- **Agregar preguntas**: cada vez que una entrevista te haga una pregunta
  nueva, sumala a este archivo.
