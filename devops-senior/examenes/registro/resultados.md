# Registro de resultados

| Fecha | Tema | Nivel | Formato | % Aciertos | Puntos débiles detectados |
|---|---|---|---|---|---|
| 2026-09-08 | Diagnóstico general (12 temas, tema 13 MELI excluido) | Panorama | Preguntas abiertas, de a una | ~5/12 sólidas, 2/12 parciales, 5/12 débiles | IAM/Managed Identity, consistencia de bases NoSQL, Durable Functions (activity/orchestrator), Kubernetes troubleshooting, DevSecOps/shift-left |
| 2026-09-14/15 | Kubernetes — arquitectura (`10-kubernetes-avanzado/01-arquitectura-y-cluster.md`) | Fundamentos, desde cero | Guiado, de a una pregunta | Base real de partida: no conocía Kubernetes más allá de "un motor de contenedores ordenado" (confundía con Docker). Al cierre: entendió correctamente las 7 piezas del clúster (kube-apiserver, etcd, kube-scheduler, kube-controller-manager, kubelet, kube-proxy, container runtime), el reconciliation loop, y las 3 formas de levantar un clúster (kubeadm/managed/serverless-node) | Ninguno pendiente de este archivo — completado en la sesión |
| 2026-09-14/15 | Entrevista real (EY) — feedback | — | Feedback post-entrevista, no autoevaluación | Se trabó en 2 preguntas reales: tipos de Load Balancer de AWS (ALB/NLB/GWLB) y Kubernetes Pod en estado `Pending`. Ambos repasados en la sesión | AWS Load Balancers: revisar con examen formal más adelante (`temas/02-contenedores-serverless`/`temas/05-networking-multicloud`) |
| 2026-09-16/17 | Redes multi-cloud (`05-networking-multicloud`) + Kubernetes networking/service mesh | Fundamentos, guiado | Guiado, de a una pregunta | Buen nivel: entendió aislamiento de red (VNet/VPC), modelo de 3 capas (pública/aplicación/datos), NSG, y corrigió solo el error común de ubicar el Private Endpoint "del lado del proveedor" en vez de "del lado del consumidor" (se hizo diagrama de apoyo). En Kubernetes: entendió que los pods NO están aislados por default (red plana) a diferencia de las subnets, la diferencia entre NetworkPolicy (filtro L3/L4, kernel) e Istio/mTLS (identidad+cifrado, L7, Envoy), y que Istio en balanceo de tráfico **reemplaza** la decisión de kube-proxy en vez de sumarse a ella. Razonamiento estadístico correcto sobre distribución binomial en canary releases | Ninguno crítico — dos preguntas de profundización quedaron guardadas (ver abajo) |
| 2026-09-29 | Ansible — fundamentos (gestión de configuración, agentless, Inventory/Playbook/Módulos, idempotencia, Handlers, Roles, variables, Jinja2) | Fundamentos, desde cero | Guiado, de a una pregunta | Buen nivel general — entendió y explicó solo la diferencia Terraform (provisioning, con state) vs. Ansible (configuration management, sin state, verificación en vivo), el rol del Inventory, y `template` vs. `copy`. Dos confusiones puntuales corregidas en la sesión: Docker vs. Ansible (pensó que Ansible modificaba contenedores en ejecución) y `ok` vs. `changed` (pensó que `ok` significaba que la acción se ejecutó) | Falta examen dedicado que lo ponga a prueba a fondo antes de subir a 🟢 Sólido; falta crear el contenido de referencia en `temas/` |
| 2026-09-30 | CI/CD y GitOps (`03-cicd-multicloud`) — CI/CD tradicional, modelo pull vs. push, ArgoCD, OIDC | Repaso guiado sobre base real previa (Jenkins/Azure Pipelines) | Guiado, de a una pregunta | Buena base real de CI/CD, con un ajuste de orden (pruebas unitarias antes del build, no después). En GitOps: corrigió solo tras una confusión sobre dónde vive ArgoCD (pensó que estaba "del lado de GitHub"; en realidad vive dentro del clúster) y ubicó bien, sin ayuda, dónde cabe una ventana de despliegue manual (merge a `main`). En OIDC: buena intuición inicial (mínimo privilegio, tiempo corto), necesitó precisión sobre el mecanismo real de dos pasos (JWT firmado por GitHub + credencial temporal emitida por la nube) | Falta profundizar la configuración práctica de ArgoCD (pospuesto a pedido propio, ver nota abajo); falta GitLab CI como alternativa |

**Fortalezas confirmadas en el diagnóstico:** IaC (Terraform/Bicep), CI/CD +
OIDC, Networking (Private Endpoint + DNS privado), FastAPI async/await,
Well-Architected trade-offs (buen ejemplo propio con HPA).

> Se completa cada vez que rendís un examen de autoevaluación. Pedime que lo
> actualice al terminar un examen, o hacelo vos mismo siguiendo el formato.

## Pendientes de profundización (retomar después)

- **Durable Functions — `activity` vs. `orchestrator`**: entendido el mecanismo
  de `replay`/determinismo en general, pero el rol específico de una
  `activity` (por qué no se repite en el replay) quedó para repasar con más
  ejemplos. Ver `../../temas/09-orquestacion-serverless/`.
- **Kubernetes — troubleshooting (`CrashLoopBackOff`, `OOMKilled`, exit codes)**:
  tema declarado como no manejado (nunca lo hizo en la práctica). Ver
  `../../temas/10-kubernetes-avanzado/05-troubleshooting.md` — sesión dedicada
  con varios escenarios de `describe pod`/`logs --previous`/exit codes
  reales. **Reordenado (2026-09-14)**: antes de esta sesión, repasar primero
  `01-arquitectura-y-cluster.md` a `04-operators-crds-managed-k8s.md` del
  mismo tema (arquitectura del clúster) — ver `../../00-diagnostico/roadmap.md`,
  troubleshooting pasó a la Fase 8.
- **Identidad — Managed Identity system-assigned vs. user-assigned**: no lo
  tenía claro (adivinó), quedó explicado pero conviene repasar con ejemplo
  práctico. Ver `../../temas/04-identidad-iam/`.
- **Consistencia de bases NoSQL (Cosmos DB/DynamoDB/Firestore)**: no conocía
  el concepto de "nivel de consistencia" en absoluto. Ver `../../temas/06-datos-secretos/`.
- **DevSecOps / "shift-left"**: no conocía el término ni herramientas como
  **Trivy**; el concepto general de seguridad temprana sí, pero la
  terminología específica no. Ver `../../temas/11-seguridad-devsecops/`.
  **Actualización (2026-10-05)**: sigue siendo un hueco específico de
  **nombre** (dijo "Stribi" en vez de "Trivy") aunque el funcionamiento ya
  lo describió bien sin ayuda — marcar como prioridad alta de recuerdo de
  NOMBRE (no de concepto) en el próximo repaso espaciado.

## Repaso espaciado pendiente de programar (2026-09-25)

El usuario pidió explícitamente que, más adelante, se programe una
**revisión/evaluación** de los temas ya vistos (Kubernetes, redes, Terraform)
— aclaró que entiende los conceptos en el momento pero **no se le quedan
grabados** con el tiempo sin repaso. Es un pedido de **repetición espaciada**
(*spaced repetition*), no una autoevaluación puntual como las de
`examenes/registro/`. Pendiente: definir con el usuario la frecuencia
(¿diario? ¿semanal?) y, si tiene sentido, armar un recordatorio/trigger
automático para disparar esas sesiones de repaso sin que él tenga que
acordarse de pedirlo.

**Actualización (2026-10-02):** el usuario reforzó el pedido — cuando se
haga ese repaso espaciado, quiere **preguntas más exigentes** (no las
preguntas guiadas de primera pasada que se usan para enseñar un tema nuevo),
específicamente para comprobar qué tanto quedó interiorizado de verdad, no
solo si lo entendió en el momento en que se explicó.

**Actualización (2026-10-04):** el usuario reiteró que esto sigue pendiente
y aplica también a la **Fase 4 (Identidad)**, recién marcada como completa —
"completa" en el roadmap significa primera pasada cubierta, no que ya no
necesite repaso (coherente con la escala no binaria de `progreso.md`).
Además pidió una regla específica para esos repasos: **forzar el recuerdo
del NOMBRE del servicio/herramienta, no solo del funcionamiento** — describir
cómo funciona algo y que él diga qué lo resuelve, no al revés (ver regla
nueva en `CLAUDE.md`, sección "Formato de enseñanza/examen").

**Actualización (2026-10-05):** para esos repasos de nombres, el usuario
pidió específicamente el formato de **selección múltiple** (dar el
funcionamiento + varias opciones de nombre para elegir) en vez de recuerdo
abierto directo, como paso intermedio para ir progresando. Pendiente de
implementar en el próximo repaso espaciado, no en sesiones de enseñanza
normales.

## Ansible — tema nuevo pendiente de agregar (2026-09-25)

El usuario pidió agregar **Ansible** al temario. Es **gestión de
configuración** (*configuration management*), agentless, basado en YAML
(*playbooks*) — distinto de Terraform (que es **aprovisionamiento**,
*provisioning*, declarativo). No confundir las dos categorías al armar el
tema: van de la mano en una arquitectura real (Terraform crea la VM,
Ansible la configura por dentro) pero no son lo mismo. Pendiente crear
`../../temas/01-iac-multicloud/` con una sección de Ansible, o un tema
aparte si termina siendo lo bastante grande.

**Actualización (2026-09-29):** ya se dio la sesión guiada de fundamentos
(ver fila en la tabla de arriba y `progreso.md`, nivel 🟡 Intermedio). Sigue
pendiente crear el archivo de referencia en `../../temas/01-iac-multicloud/`.

## Preguntas guardadas para profundizar (2026-09-16/17)

- **¿El tamaño de los pods es estándar o hay variabilidad?** Respuesta corta
  dada en la sesión: no hay estándar, lo definen los `requests`/`limits` de
  cada pod (ver `../../temas/10-kubernetes-avanzado/02-scheduling-recursos-autoscaling.md`).
  Lo más cerca de "estandarizar" es **LimitRange** (tamaño default por
  namespace) y **ResourceQuota** (techo total por namespace) — **pendiente
  de una sesión dedicada a estos dos objetos**, no se profundizó todavía.
- **¿Qué otros elementos de Kubernetes reemplaza o sustituye Istio?**
  Respuesta corta dada en la sesión: reemplaza el Ingress Controller (vía
  Istio Gateway) y librerías de resiliencia en el código de la app
  (reintentos/timeouts/circuit breaking); NO reemplaza NetworkPolicy ni
  kube-proxy por completo, y complementa (no sustituye) OpenTelemetry.
  **Pendiente de profundizar**: comparación más detallada Istio Gateway vs.
  Ingress vs. Gateway API (ver `../../temas/10-kubernetes-avanzado/03-networking-service-mesh.md`).

## Claude Certified Architect (CCA-F) — temario completo cubierto (2026-09-25 a 09-29)

Primera pasada completa por las 5 áreas del examen: 3 en 🟢 Sólido (Agentic
Architecture 27%, Configuración/Workflows 20%, Contexto/Confiabilidad 15%),
2 en 🟡 Intermedio (Tool Design/MCP 18%, Prompt Engineering 20%) — ver
`progreso.md` para el detalle. Pendiente: un repaso mixto (preguntas
encadenadas de las 5 áreas sin avisar el tema, como ya se hace con los
temas de nube) antes de considerar rendir el examen real.

| 2026-10-01/02 | Identidad (`04-identidad-iam`) — Managed Identity/IAM Role/Service Account, Keycloak, federación OIDC Kubernetes↔AWS IAM (IRSA) | Repaso guiado sobre base real previa (AWS IAM, Azure AD) | Guiado, de a una pregunta | Buena base real en roles/políticas. Corrigió el eje real de Managed Identity (ciclo de vida/compartibilidad) tras una confusión inicial; aplicó bien el trade-off de blast radius en Keycloak (Client por app) sin ayuda; conectó de forma espontánea su experiencia real en MercadoLibre (K8s self-managed sobre EC2, "MRN") con el patrón IRSA recién explicado | Quedó sin cerrar la pregunta de síntesis final de IRSA y sin profundizar RBAC específico de cada nube — la sesión se desvió a la ruta de IA/MLOps (pedido del usuario) antes de terminar |
| 2026-10-04 | Identidad (`04-identidad-iam`) — cierre: síntesis de IRSA y RBAC scope/herencia en Azure | Repaso guiado | Guiado, de a una pregunta | Cerró sin ayuda la síntesis completa de la federación OIDC Kubernetes↔AWS IAM (qué pasa al borrar el ServiceAccount) y respondió bien la herencia de RBAC por scope jerárquico en Azure | **Fase 4 completa.** Ninguno pendiente de este tema |
| 2026-10-05 | Fase 5 — Networking (equivalencias Private Endpoint/PrivateLink/PSC) y Seguridad/DevSecOps (Trivy, OPA/Gatekeeper) | Repaso guiado, selección múltiple para nombres | Guiado, de a una pregunta | Networking ya era 🟢 Sólido de antes, solo se agregaron equivalencias multi-cloud. En seguridad: describió bien el funcionamiento de Trivy y OPA sin ayuda, pero no recordó ninguno de los dos nombres a la primera (seleccionó correctamente en el formato de opción múltiple que pidió el propio usuario) | **Fase 5 completa** dentro de su alcance real — la síntesis "app a BD sin exponer secretos" del roadmap queda pendiente de cerrar en la Fase 6 (Key Vault/Secrets Manager, todavía no enseñado) |

| 2026-10-03 | IA/MLOps — fundamentos (entrenamiento/inferencia, pre-entrenamiento/fine-tuning, RAG) | Fundamentos, desde cero (nivel vocabulario AI-900) | Guiado, de a una pregunta | Buena intuición general de redes neuronales y entrenamiento sin ayuda; corrigió inferencia (no es ajuste manual) y pre-entrenamiento (no sigue aprendiendo solo) tras explicación. En RAG: identificó la técnica sin ayuda y agregó por cuenta propia la variante "agentic RAG" (búsqueda vía tool call en vez de vector DB), conectándolo correctamente con Tool Design/MCP del CCA-F | Falta profundizar embeddings/bases de datos vectoriales y el resto del vocabulario de AI-900/AWS AI Practitioner/Generative AI Leader |
| 2026-10-03/04 | IA/MLOps — fundamentos completos (embeddings, visión por computador, NLP, IA responsable) | Fundamentos, desde cero (nivel vocabulario AI-900) | Guiado, de a una pregunta | Cierra el nivel de fundamentos de la Ruta IA/MLOps. Embeddings y NLP sin ayuda. En visión por computador aportó un caso real propio (clasificador de flores, MercadoLibre/Bizagi) y corrigió con precisión que lo que usó fue transfer learning vía feature extraction, no fine-tuning real — duda suya, bien fundamentada. En IA Responsable no recordaba los seis pilares de memoria, pero una vez definidos identificó bien cuál aplicaba a su propio caso (Reliability & Safety) | El usuario confirmó su meta de certificación: **AWS Certified AI Practitioner** (motivo: más peso comercial) + seguir hacia el **CCA-F**. Falta el nivel técnico de la ruta (AI-102/AWS ML Engineer Associate/GCP ML Engineer) si se decide profundizar más allá de fundamentos |

## ArgoCD — configuración en profundidad pendiente (2026-09-30)

Se cubrió el panorama conceptual de GitOps/ArgoCD (modelo pull, dónde vive
ArgoCD, dónde cabe la ventana de despliegue manual — ver fila de abajo y
`progreso.md`), pero **no la configuración práctica**: instalación, objetos
`Application`/`AppProject`, políticas de sincronización (`sync policies`,
manual vs. automático, `self-heal`). El usuario pidió explícitamente
posponerlo para una sesión futura, después de avanzar con la Fase 4
(Identidad).

| 2026-10-05 | Fase 6 — Datos y secretos (completa): Key Vault/Secrets Manager + Managed Identity, niveles de consistencia NoSQL, relacional administrada | Guiado, de a una pregunta | Guiado, de a una pregunta | Cerró sin ayuda la síntesis "app a BD sin exponer secretos" (Managed Identity/IAM Role → Key Vault/Secrets Manager → Private Endpoint/PrivateLink). Respondió bien consistencia eventual vs. fuerte (cierra hueco del diagnóstico inicial 2026-09-08) y la ventaja de gestión reducida de RDS/Cloud SQL/AlloyDB, todo sin ayuda | **Fase 6 completa.** Ninguno pendiente de este tema |

## Ronda de vocabulario pendiente

El usuario pidió una ronda rápida de repaso de términos/nombres de
herramientas (sin conceptos nuevos) una vez cerrado el diagnóstico general —
pendiente de hacer.
