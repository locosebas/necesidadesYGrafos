# Libreto de diapositivas - Entrevista técnica Gorilla Logic (Senior Platform DevOps)

Plan de la presentación para repasar el **Technical Screening con Carlos Suárez** (Gorilla Logic,
miércoles 11 nov 2026, 4:30–6:00 pm hora de Colombia). Sale de las respuestas del assessment de
Canditech del 4 nov ([README](README.md)) y de la posición "DevOps GCP" de la llamada con la
reclutadora. Cada diapositiva tiene:

- `Sección`: a qué bloque pertenece.
- `Diagrama`: el o los diagramas de [diagramas-c4.md](diagramas-c4.md).
- Viñetas: lo que se ve en pantalla (en español, con los términos técnicos en inglés).
- `>` guion: lo que dices en voz alta, **en inglés**, como lo dirías en la entrevista. En la
  presentación aparece al oprimir **N** (notas).

La presentación [presentacion.html](presentacion.html) se genera con
`python3 generar_presentacion.py` a partir de este archivo y del de diagramas.

Consejo de la reclutadora (Sabrina Díaz): **"ser tú mismo, no leer una presentación, sino dar a
conocer tu experiencia y conocimiento"**. Esta presentación es para estudiar antes, no para leerla en
la llamada. El guion es una guía de ideas, no un texto para recitar palabra por palabra.

---

## Entrevista técnica · Gorilla Logic
**Sección:** Portada
- **Technical Screening** con Carlos Suárez · miércoles 11 nov 2026 · 4:30–6:00 pm (Colombia)
- Posición: **Senior Platform DevOps Engineer** (la llamada con la reclutadora decía "DevOps GCP")
- Repaso de los **5 escenarios** del assessment de Canditech + equivalencias **AWS → GCP**
- Diagramas C4 (Context, Containers, Components, Code)
- Teclas: ← → para moverse · N para ver el guion

> This deck is for studying, not for reading on the call. If I remember the method, stabilize first, diagnose second, fix through Git third and prevent fourth, I can answer any of the five scenarios in my own words.

---

## Los 5 escenarios y un solo método
**Sección:** Panorama
**Diagrama:** D1
- 1 · **E-commerce en AWS** con 4x tráfico · 2 · **Terraform** en producción · 3 · **Incidente en EKS** tras Argo CD
- 4 · **Canary** con progressive delivery · 5 · **platformctl**, la CLI interna en Python
- Método: **1 estabilizar** · **2 diagnosticar** con evidencia · **3 corregir por Git** · **4 prevenir**
- Con stakeholders: **empatía → riesgo concreto → alternativa con tiempo → próximo update**

> All five scenarios follow the same pattern. First I stabilize and protect customers. Then I diagnose with evidence, not guesses. Then I fix it through the normal path, Git and CI, so the fix sticks. And finally I add a guardrail so it doesn't happen again. When a stakeholder pushes for a shortcut, I agree with the goal, explain the concrete risk, offer a safe alternative with a time estimate, and promise the next update.

---

## Bloque 1 · La arquitectura del e-commerce
**Sección:** 1 · E-commerce en AWS
**Diagrama:** D2
- ~10.000 usuarios y ~1.000 compras diarias; una campaña de marketing multiplica el tráfico **por 4**
- **ALB** (Application Load Balancer) → 2 **Availability Zones** → **EKS** (Elastic Kubernetes Service) en subredes privadas
- 3 servicios por **HTTP**: **web**, **payment**, **image**
- Riesgos de seguridad que vale la pena mencionar: HTTP interno sin TLS, subredes privadas **sin restricciones**

> The setup is a classic e-commerce on AWS: an Application Load Balancer in front of two Availability Zones, and three services on EKS, web, payment and image, talking over plain HTTP. Before solving anything, I'd note two security gaps: internal traffic without TLS, and private subnets with no network restrictions. I'd fix those later with mTLS through a service mesh, Kubernetes Network Policies and tighter security groups.

---

## Sitio lento por la campaña: los 4 pasos
**Sección:** 1 · E-commerce en AWS
**Diagrama:** D3
- **1 · Incident management**: Incident Commander, canal, updates cada 15–30 min a Marketing y Soporte
- **2 · Mitigar**: `kubectl scale`, subir el max del node group, **proteger checkout** primero
- **3 · Causa raíz** con las **Four Golden Signals**: latency, traffic, errors, saturation · capa por capa: ALB → nodos → pods (**HPA** en maxReplicas?) → base de datos
- **4 · Prevenir**: **HPA** (Horizontal Pod Autoscaler) + **Karpenter** / Cluster Autoscaler, **CloudFront**, **ElastiCache**, **load testing** (k6, JMeter, Locust)

> I'd treat it as a production incident, because slowness during a campaign means abandoned carts and lost revenue. First, stabilize: scale out the services and the node group, and protect checkout. Then find the bottleneck layer by layer using the four golden signals: latency, traffic, errors and saturation. The usual suspects are an HPA capped at max replicas, a saturated database, or images served without a CDN. Finally, make it permanent: autoscaling with headroom, caching, a CDN, and load tests with Marketing before the next campaign.

---

## Usuarios en Asia lentos, sobre todo las imágenes
**Sección:** 1 · E-commerce en AWS
**Diagrama:** D4
- Causa: **distancia física**, no capacidad · 150–250 ms por viaje, y cada página pide muchas imágenes
- **1 · Medir**: **RUM** (Real User Monitoring) por país, pruebas sintéticas desde Asia
- **2 · CDN** (Content Delivery Network): **CloudFront** con **S3** como origen, Cache-Control, Origin Shield
- **3 · Imágenes livianas**: WebP/AVIF, `srcset`, lazy loading
- **4 · Dinámico**: **Global Accelerator** · **5 · Largo plazo**: segunda región + **Route 53 latency-based routing**, solo si el negocio lo justifica

> The root cause is physical distance, not capacity. Every request from Asia pays a long round trip, and images pay it many times per page. I'd start with the cheapest, highest-impact fix: move images to S3 and serve them through CloudFront, with edge locations in Asia, plus lighter image formats. For dynamic content, Global Accelerator uses the AWS backbone. A second region with Route 53 latency-based routing only makes sense if the Asian market justifies the cost and complexity.

---

## El payment service se cae y arrastra a todos
**Sección:** 1 · E-commerce en AWS
**Diagrama:** D5
- **Cascading failure** (efecto dominó): HTTP síncrono sin timeouts, **retry storms**, recursos compartidos sin límites
- **Timeouts** en todas las llamadas · **retries** con **exponential backoff + jitter**
- **Circuit breaker**, 3 estados: **closed** (llama) · **open** (falla rápido) · **half-open** (prueba unas pocas)
- **Bulkhead**: requests/limits, node group dedicado, pool de conexiones propio, PDB, anti-affinity entre AZ
- **Liveness** solo revisa el proceso; **readiness** saca el pod del balanceador

> There are two problems: why payment crashes, and why it takes everything else down. The cascade happens because calls are synchronous with no timeouts, retries pile up, and resources are shared. To stop the domino effect: timeouts everywhere, retries with exponential backoff and jitter, a circuit breaker, which is closed while payment is healthy, opens after repeated failures to fail fast, and goes half-open to test recovery. And bulkheads, so payment has its own resources and can't starve the rest of the site.

---

## La compra asíncrona con cola
**Sección:** 1 · E-commerce en AWS
**Diagrama:** D6
- Orden **PENDING** → cola (**SQS**, Amazon MQ, **MSK/Kafka**) → **payment workers** → **PAID / FAILED**
- **Idempotency key**: nunca cobrar dos veces aunque el mensaje llegue repetido
- **DLQ** (Dead Letter Queue) para los mensajes que fallan N veces
- **Saga pattern**: acciones de compensación si un paso falla
- Prevención: **chaos engineering** (AWS FIS, Chaos Mesh), canary con **Argo Rollouts**, SLO de checkout

> Long term, I'd move payments to an asynchronous flow. The web service creates the order as pending and puts a message on a queue, like SQS or Kafka. Payment workers consume it, call the gateway with an idempotency key so we never charge twice, and mark the order as paid or failed. Messages that keep failing go to a dead letter queue, and a saga with compensating actions handles partial failures. That way a payment problem never takes down the whole website.

---

## Bloque 2 · Terraform en producción con CI
**Sección:** 2 · Terraform en producción
**Diagrama:** D7
- SaaS en AWS: VPC, subredes, security groups, IAM y node groups de EKS en **Terraform**
- **State remoto** compartido: **S3** con versionado + **lock en DynamoDB**
- Los applies **solo los hace CI** después de revisión; **break-glass** para emergencias
- Principio: Terraform es la **fuente de verdad**; todo cambio manual se **codifica** después

> In this setup, Terraform is the source of truth, the state lives in S3 with versioning and a DynamoDB lock, and only CI applies to production after a review. There's a break-glass process for emergencies, but every manual change must be codified in Terraform within a day or two. Every answer in this block protects those three things: the review, the state, and Terraform as the source of truth.

---

## Revisar un `terraform plan`: split / rework
**Sección:** 2 · Terraform en producción
**Diagrama:** D8
- Decisión: **split / rework**, no aplicar así
- 3 de 4 cambios son **refactors** que Terraform lee como destroy + create → **`moved` blocks** o `terraform state mv`
- Riesgo 1 · **IAM role de nodos**: al recrearlo, los nodos quedan **NotReady**, la VPC CNI no asigna IPs, no se jala de ECR; además cambia el **role ID**
- Riesgo 2 · **Subnet**: la llave pasó de AZ name (`us-east-1b`) a **AZ ID** (`use1-az2`) · `DependencyViolation`, apply a medias
- **PR A**: plan = 0/0/0 · **PR B**: GPU launch template v13 en ventana · `prevent_destroy` · **policy-as-code**

> I would split and rework this plan, not apply it. Three of the four items are code refactors that Terraform reads as destroy and create, even though nothing real should change. The worst is the node IAM role: recreating it leaves every node without identity, so they go NotReady and the cluster goes down. The subnet change comes from switching the for_each key from AZ name to AZ ID. I'd fix both with moved blocks until the plan shows zero changes, ship the GPU launch template in its own PR during a window, and add prevent_destroy plus policy-as-code in CI.

---

## State lock huérfano: 7 pasos antes de `force-unlock`
**Sección:** 2 · Terraform en producción
**Diagrama:** D9
- El lock **no es el problema, nos protege**; el riesgo real es un **state que no coincide con AWS**
- 1 congelar · 2 ¿el proceso sigue **vivo**? (**SIGINT**, no matar) · 3 backup: `terraform state pull`, **`errored.tfstate`**
- 4 ¿qué cambió? **CloudTrail** + plan guardado · 5 **`force-unlock`** solo si todo se cumple
- 6 reconciliar: **`plan -refresh-only`**, **`import` blocks** · 7 reanudar **por CI** + postmortem
- Prevención: timeout del job **mayor** que el apply más largo y **SIGINT con periodo de gracia**

> The lock isn't the problem, it's protecting us. The real risk is a state file that no longer matches AWS. So before any force-unlock I freeze changes, confirm the process is really dead, back up the state and look for an errored.tfstate, and use CloudTrail to see what actually changed. Only then do I force-unlock, reconcile with a refresh-only plan and import blocks, and resume through CI. To prevent it, the CI timeout must be longer than the longest apply, and CI should send SIGINT so Terraform can write the state and release the lock by itself.

---

## Drift por un CIDR agregado a mano en un incidente
**Sección:** 2 · Terraform en producción
**Diagrama:** D10
- **No** `lifecycle { ignore_changes }` amplio: deja un **punto ciego** permanente en un security group
- **No** apply normal: borraría `10.55.8.0/24` y **volvería el outage**
- **Verificar**: CloudTrail (quién, qué puertos), **VPC Flow Logs**, de quién es el CIDR, causa raíz
- **Codificar** la regla en Terraform con ticket → plan limpio · **add before remove** si se angosta
- Guardrails: **drift detection** nocturno (`plan -detailed-exitcode`), **AWS Config** / EventBridge, CODEOWNERS

> I'd neither ignore the drift nor blindly revert it. A broad ignore_changes turns the security group into a permanent blind spot, and a normal apply would remove the rule and bring the outage back. So I verify what the emergency rule really opened and who needs it, using CloudTrail and VPC Flow Logs, codify the right version in Terraform until the plan is clean, and add nightly drift detection and alerts on manual changes, so emergency fixes become code within a day.

---

## Video · "Haz `apply -auto-approve`, `force-unlock` y `-target` hoy"
**Sección:** 2 · Terraform en producción
- 1 · Urgente → **lo quiero sacar hoy**
- 2 · Sin atajos → riesgo de **outage**
- 3 · `-auto-approve` = sin revisión · `force-unlock` = **state corrupto** · `-target` = **apply a medias**
- 4 · Pipeline → revisión del plan en **30 min** → apply por CI hoy → monitorear
- 5 · Si hay sorpresas → riesgo concreto + **nuevo ETA**

> I understand this is urgent, and I want to get it out today. But I won't take those shortcuts, because each one can turn a small change into a production outage. Auto-approve means applying something nobody has reviewed. Force-unlocking a running apply can corrupt our state. And dash target leaves the state half-applied, which usually breaks the next deployment. Here's what I propose: I push the change through our normal pipeline right now, review the plan with a teammate within thirty minutes, and if it only touches the node group, we apply it today through CI while I monitor. If the plan shows anything unexpected, I'll tell you right away with the specific risk and a new ETA.

---

## Bloque 3 · El 503 después del sync de Argo CD
**Sección:** 3 · Incidente en EKS
**Diagrama:** D11
- Sync de **Argo CD** 14:01 → **503** desde 14:03 · target group **0 healthy / 6 unhealthy**
- Son **dos problemas**: el principal es la configuración, el secundario es la capacidad
- **Principal**: Ingress `target-type: instance` necesita un **NodePort**, pero el Service quedó **ClusterIP**
- **Secundario**: **IP exhaustion** de la **VPC CNI** en las subredes a (3) y b (1); la c tiene 900
- La IP exhaustion impide **escalar**, pero no explica que los pods **viejos** estén unhealthy

> There are two problems here, and the trick is not to mix them up. The full outage is explained by configuration: with target-type instance, the ALB sends traffic to a NodePort on the nodes, but the release changed the Service to ClusterIP, which has no NodePort, so every target fails its health checks. It started two minutes after the Argo CD sync, so the release is the prime suspect. The IP exhaustion in subnets a and b is real, it's why new pods can't start, but it doesn't explain why the existing pods are unhealthy. That's a follow-up after service is restored.

---

## La nota de incidente en 5 bullets
**Sección:** 3 · Incidente en EKS
**Diagrama:** D11
- **Impact / scope**: outage total de la API pública desde ~14:03, todos los tenants
- **Containment**: rollback del release **por GitOps** (git revert o rollback de Argo CD con **auto-sync pausado**)
- **Check 1 · Kubernetes**: diff de Service/Ingress, logs del **AWS Load Balancer Controller**
- **Check 2 · AWS**: `aws elbv2 describe-target-health`, puerto registrado vs NodePort, IPs por subred
- **Leading hypothesis**: Service pasó a **ClusterIP** con `target-type: instance` → health checks fallan

> My incident note would have five bullets. Impact: full outage of the public API since about 14:03 for all tenants. Containment: roll back the 14:01 release through GitOps, with auto-sync paused so it isn't re-applied, and no manual kubectl edits that Argo CD would overwrite. Check one, Kubernetes: diff the Service and Ingress and read the load balancer controller logs. Check two, AWS: describe target health to get the reason codes. And the leading hypothesis: ClusterIP with target-type instance, so once we revert, the targets should turn healthy within a few health-check intervals.

---

## Video · "Cambiemos en vivo y reconciliamos Git después"
**Sección:** 3 · Incidente en EKS
- 1 · De acuerdo → **recuperar el tráfico** es la prioridad
- 2 · Los cambios en vivo **no duran**: Argo CD los revierte (**self-heal**), los add-ons de EKS se sobrescriben, perdemos el rastro
- 3 · Lo más rápido y seguro → **revert del release de las 14:01 en Git** → Argo CD sincroniza
- 4 · Si eso falla → **un solo** cambio break-glass, registrado, con auto-sync pausado y codificado **enseguida**

> I agree, getting traffic back is the priority. But live edits won't stick: Argo CD will revert them, EKS add-ons get overwritten, and we lose track of what actually fixed or broke things. We already have a strong suspect, the 14:01 release, so the fastest safe fix is reverting it in Git and letting Argo CD sync. If that fails, we do one scoped break-glass change, logged in the channel, with auto-sync paused, and codified in Git right after, not later.

---

## Video · El PM pregunta: ¿rollback o seguir investigando?
**Sección:** 3 · Incidente en EKS
- 1 · **Rollback ya** + investigar **en paralelo**
- 2 · Por qué: empezó **2 min** después del release, outage **total**, volvemos a una versión **conocida y buena**
- 3 · Revisión rápida: que no haya nada **irreversible** (migraciones de base de datos)
- 4 · La evidencia ya está guardada → causa raíz después → **update en 15 min**

> We roll back now, and keep investigating in parallel. The errors started two minutes after the release, it's a full outage for every customer, and rolling back returns us to a version we know works. I'll do a quick check that the release has nothing irreversible, like database migrations. We've already saved the evidence, so we'll still find the root cause. I'll update you in fifteen minutes.

---

## Bloque 4 · El canary que también dañó al stable
**Sección:** 4 · Canary con GitOps
**Diagrama:** D12
- Sync 10:14 con **~10 %** al candidato · 10:17 más **5xx** en el canary · 10:18 la latencia empeora **también en el stable**
- 10:19 alerta en una **dependencia downstream compartida**
- La imagen va por **tag**, y ese tag se **empujó varias veces** en la última hora · Argo CD con **auto-sync**
- Sospechas: **retry storm** del canary hacia la dependencia, o pods stable que **jalaron el tag nuevo**

> The interesting detail is that the stable version also got worse. That points to two possibilities: the canary is hammering the shared downstream dependency, for example with a retry storm, or some stable pods restarted and pulled the new image under the same mutable tag, because that tag was pushed several times in the last hour. Both hypotheses shape my first actions.

---

## Las 4 acciones de los primeros 10 minutos
**Sección:** 4 · Canary con GitOps
**Diagrama:** D12
- **1 · Abortar el canary** con el controlador: `kubectl argo rollouts abort` → 100 % al stable, **sin drift** con Argo CD
- **2 · Vigilar** métricas y trazas del servicio y de la dependencia; comparar llamadas, retries y timeouts canary vs stable
- **3 · Verificar el digest** real de cada cohorte (`imageID` en los pods) contra el historial del tag en **ECR**
- **4 · Git igual a la decisión**: revert del PR de promoción, imagen fijada por **digest** (`image@sha256:...`)
- Seguimiento: **ECR tag immutability** y digests en todos los overlays de producción

> First, I abort the canary with the rollout controller, which sends all traffic back to stable and changes the rollout status, not the spec, so Argo CD's auto-sync doesn't fight it. Second, I watch the service and the dependency metrics after the abort to see whether the canary caused the degradation. Third, I check the actual image digest running in each cohort, because the tag was overwritten. Fourth, I make Git match the decision: revert the promotion and pin the last known-good image by digest, then enable tag immutability in ECR.

---

## Video · "¿Hot-fix directo en producción y limpiamos Git después?"
**Sección:** 4 · Canary con GitOps
- 1 · Los errores **ya están contenidos** → el tráfico volvió a la versión estable
- 2 · Un hot-fix directo **no dura**: la plataforma **deshace** los cambios manuales → los errores podrían volver
- 3 · Corregir **por Git** toma los mismos minutos y **sí queda**
- 4 · Lo estoy haciendo ya → **update en 10 min**

> Good news: the errors are already contained. We stopped the new version and all traffic is back on the stable one. A direct hot-fix wouldn't even last: our platform automatically undoes manual changes within minutes, so the errors could come back. Making the fix through Git takes the same few minutes, and it actually sticks. I'm doing that now, and I'll update you in ten minutes.

---

## Video · Rollout fallido con migración de base de datos
**Sección:** 4 · Canary con GitOps
**Diagrama:** D13
- **Pausar el rollback**: versión vieja + esquema nuevo = **segundo outage**
- 3 preguntas: ¿migración **aditiva o destructiva**? ¿**terminó** completa? ¿ya hay **datos nuevos** en el formato nuevo?
- Compatible hacia atrás → **rollback** de la app · No compatible → **roll-forward** con un fix
- Antes de todo: confirmar un **snapshot reciente** de la base de datos
- Para evitarlo: **expand-contract** (parallel change)

> First, let's pause the rollback: the old version may not work with the new schema, and we could cause a second outage. I need three answers: was the migration additive or destructive, did it fully complete, and has new data already been written in the new format? If it's backward-compatible, we roll back the app. If not, we roll forward with a fix, because undoing the migration could lose data. Either way, I confirm we have a recent snapshot first. To avoid this in the future, we use expand-contract: add first, migrate the code, and remove the old columns in a later release.

---

## Bloque 5 · platformctl v1: los 4 riesgos
**Sección:** 5 · platformctl
**Diagrama:** D14
- **1 · Secretos en los logs**: `log.info(dict(os.environ))` deja ver `AWS_SECRET_ACCESS_KEY`, tokens de CI
- **2 · Clúster equivocado**: substring (`prod` también es `preprod`), **sin paginación**, `None` silencioso, **ENV=prod por defecto**
- **3 · Command injection**: `subprocess.run(..., shell=True)` con f-strings + `grep` sobre texto
- **4 · Falla en silencio**: no revisa return codes, sin timeouts, **siempre imprime "done"**, selector vacío, sin dry-run

> The four production risks are: first, it logs the entire environment, so AWS keys and CI tokens leak into logs. Second, it can target the wrong cluster: it matches by substring, so prod also matches preprod, it ignores pagination, and it defaults to production. Third, shell=True with f-strings allows command injection. And fourth, it fails silently: no return-code checks, no timeouts, an empty selector, and it always prints done, so during an incident the engineer believes the mitigation worked when nothing happened.

---

## Diseño de platformctl v2
**Sección:** 5 · platformctl
**Diagrama:** D15
- 2 subcomandos: `rollout status` (solo lectura) y `pods restart` con `--env --namespace --deployment --reason`, **sin defaults peligrosos**
- **Targeting seguro**: config versionada env → clúster exacto, **`sts get-caller-identity`**, `--context` en cada llamada
- **Dry-run por defecto**; `--execute` + escribir el nombre del entorno para confirmar en producción
- **Eviction API** + **PodDisruptionBudgets**, lotes pequeños, máximo por corrida, **RBAC** mínimo, sin drift con Argo CD
- **Exit codes** documentados (0 éxito · 1 falló · 2 input · 3 guardrail · 4 parcial · 5 timeout/auth), **`--output json`**, stdout vs stderr

> Version two has two subcommands with required inputs and no dangerous defaults. It resolves the environment to an exact cluster and account from a versioned config, verifies the caller identity, and never changes the global kubeconfig. It's dry-run by default and shows exactly which pods it would restart. When it executes, it uses the Eviction API, so it respects PodDisruptionBudgets, in small batches, waiting for pods to be ready. And it ends with one clear success or failure line, documented exit codes and JSON output, so both humans and CI can trust the result.

---

## Video · "¿Puedes correr el restart amplio en todo producción?"
**Sección:** 5 · platformctl
- 1 · Te entiendo → **mismo objetivo**: arreglarlo rápido
- 2 · Riesgos: reinicia también lo **sano**, se pierde capacidad de golpe, todos pegan a la **base de datos** a la vez, se borran **logs**
- 3 · Alternativa: **2 min** con `rollout status` → reiniciar **solo lo atascado**, en lotes, viendo que vuelva sano
- 4 · Ayúdame: ¿qué **flujos de clientes** fallan? → updates en el canal

> I get it, we all want this fixed as fast as possible. But a broad restart would also restart everything that's healthy. We'd lose capacity all at once, every service would hit the database at the same time, and we could turn a partial problem into a full outage. We'd also wipe the logs we need. Here's what I suggest: give me two minutes to check which services are actually stuck with our status command, then I restart only those, in small batches. It's about the same time, and much safer. You can really help: tell me which customer flows are failing, so we start with those.

---

## La posición dice "DevOps GCP": equivalencias AWS → GCP
**Sección:** GCP
**Diagrama:** D16
- **EKS → GKE** (Google Kubernetes Engine), con modo **Autopilot**
- **IAM roles / IRSA → service accounts + Workload Identity**
- **ECR → Artifact Registry** · **ALB / CloudFront → Cloud Load Balancing / Cloud CDN**
- **S3 → Cloud Storage** · **SQS → Pub/Sub** · **CloudWatch / CloudTrail → Cloud Monitoring, Cloud Logging, Audit Logs**
- Terraform con provider **`google`** y state en un **bucket de Cloud Storage** (el lock lo maneja el backend `gcs`)

> The assessment was all AWS, but the recruiter's call was titled DevOps GCP, so I should be ready to translate. EKS maps to GKE, IAM roles for service accounts map to Workload Identity, ECR to Artifact Registry, S3 to Cloud Storage, SQS to Pub/Sub, and CloudWatch to Cloud Monitoring and Logging. The principles don't change: Terraform as the source of truth, GitOps with Argo CD, and least-privilege identities. I'd say honestly that my deepest hands-on experience is on AWS and Azure, and that the concepts transfer directly.

---

## Para recitar de memoria antes de entrar
**Sección:** Cierre
- **Resiliencia**: timeouts · retries con backoff + jitter · **circuit breaker** · **bulkhead** · cola + **DLQ** · **idempotency key** · **Saga**
- **Terraform**: **`moved` block** · `prevent_destroy` · **`errored.tfstate`** · `force-unlock` · `plan -refresh-only` · **`import` block** · **SIGINT** · drift detection · policy-as-code
- **EKS**: **VPC CNI** e IP exhaustion · `target-type: instance` necesita **NodePort**
- **GitOps**: Argo CD **self-heal** · **Argo Rollouts abort** · **digest** vs tag mutable · **ECR tag immutability**
- **Base de datos**: rollback vs **roll-forward** · **expand-contract** · **CLI**: dry-run · **Eviction API** + PDB · exit codes

> Before the call, I should be able to say each of these names out loud and explain it in one sentence. And remember the recruiter's advice: be myself, don't read, and talk about my real experience at MercadoLibre and Bizagi.
