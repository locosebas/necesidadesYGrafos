# Bloque 1 - E-commerce en AWS con 4x tráfico

**Escenario (resumen):** e-commerce tipo Amazon, ~10.000 usuarios y ~1.000 compras diarias. Una
campaña de marketing multiplica el tráfico por 4. Infraestructura en EE. UU.: Load Balancer → dos
Availability Zones, cada una con subred pública y privada; Kubernetes en las privadas con 3 servicios
(web, payment, image) que se comunican por HTTP. Las subredes privadas no tienen restricciones de red.

---

## Pregunta 1 - El website se volvió lento desde la campaña: explicación y pasos

### 1. Incident management
- Treat it as a production incident: revenue is directly affected (slow site during a campaign = abandoned carts).
- Open an incident channel, assign an Incident Commander, inform stakeholders (Marketing, Support, management) with updates every 15–30 minutes.
- Check if anything was deployed today; if so, consider rollback. Since slowness started with the campaign, the main suspect is load/capacity, not code.
- Priority: stabilize first, find root cause second, prevent third.

### 2. Immediate mitigation
- Scale out manually: more replicas of web/payment/image services (`kubectl scale`), raise the node group's desired/max size.
- Protect the purchase flow: payment service capacity first.
- If the database is the bottleneck: scale it up temporarily or add read replicas.
- Degrade gracefully: disable non-critical features (recommendations, heavy images).

### 3. Root cause analysis (layer by layer, using the Four Golden Signals: latency, traffic, errors, saturation)
- **Load Balancer (ALB):** target response time, request count, 5xx, healthy/unhealthy targets.
- **Nodes:** CPU/memory/network in both AZs, `kubectl top nodes`, Pending pods; Cluster Autoscaler/Karpenter at max nodes or EC2 quota?
- **Pods:** `kubectl top pods`, `kubectl get hpa` (HPA at maxReplicas?), CPU throttling, OOMKilled, failing readiness probes, per-service latency with distributed tracing (OpenTelemetry, Datadog APM, X-Ray).
- **Dependencies:** database (CPU, connection pool, slow queries, locks, IOPS), image service serving images without CDN, external payment API, NAT Gateway limits.
- Most likely: autoscaling missing or capped, database saturated, images served without caching.

### 4. Permanent fix and prevention
- HPA on every service with realistic min/max, Cluster Autoscaler/Karpenter with headroom, correct requests/limits.
- Images in S3 served through CloudFront (CDN).
- ElastiCache (Redis) for frequent queries, read replicas, connection pooling.
- Timeouts, retries, circuit breakers; SQS for non-critical work.
- Load testing before campaigns (k6, JMeter, Locust) and capacity planning with Marketing.
- Golden-signal dashboards, latency SLOs, alerts before users notice.
- Security noted: internal HTTP → TLS/mTLS (service mesh), Network Policies, tighter Security Groups.
- Blameless postmortem.

> *"Stabilize first by scaling out and protecting checkout, then find the bottleneck layer by layer using the golden signals, and finally make sure the system scales automatically and is load-tested before the next campaign."*

---

## Pregunta 2 - Usuarios del Lejano Oriente siguen lentos, sobre todo con las imágenes

**Problem:** everything is served from one US region; Asian users pay ~150–250 ms round trip per request, and images (heaviest, many per page) pay it repeatedly. It is a geographic latency problem, not capacity.

1. **Measure:** Real User Monitoring by country (CloudWatch RUM, Datadog RUM), synthetic tests from Asia, image sizes/formats in DevTools, share of revenue from Asia.
2. **CDN quick win:** CloudFront with edge locations in Asia, images moved to S3 as the origin, Cache-Control headers + versioned file names, Origin Shield.
3. **Lighter images:** WebP/AVIF, resize on demand (`srcset`, Lambda@Edge, Cloudinary/imgix), compression, lazy loading.
4. **Dynamic content:** route through CloudFront (AWS backbone) or AWS Global Accelerator; cache semi-static pages with short TTLs.
5. **Long term, only if the business justifies it:** second region (Tokyo/Singapore), Route 53 latency-based routing, Aurora Global Database / DynamoDB Global Tables for reads, centralized writes for payments; consider cost, complexity, data residency (China ICP). Terraform + Argo CD make it repeatable.

> *"The root cause is physical distance. I'd start with the cheapest, highest-impact fix — a CDN with S3 for images plus image optimization — and only move to multi-region if the Asian market justifies the cost and complexity."*

---

## Pregunta 3 - El payment service se cae al comprar y arrastra a los demás (efecto dominó)

**Two problems:** why payment crashes (root cause) and why it cascades (architecture). Cascade causes: synchronous HTTP without timeouts, retry storms, shared resources without limits, liveness probes that depend on other services.

1. **Mitigate:** incident process, roll back a recent payment deployment, disable checkout with a feature flag so the rest of the site keeps working, scale out payment.
2. **Diagnose the crash:** `kubectl describe pod`/events (OOMKilled, CrashLoopBackOff), logs, distributed tracing, database (connection pool, locks), third-party gateway (slow, rate limiting, credentials), NAT Gateway.
3. **Stop the domino effect:** timeouts everywhere; retries with exponential backoff + jitter; circuit breaker (Istio/Linkerd outlier detection or Resilience4j/Polly); bulkheads (requests/limits, dedicated node group, ResourceQuotas, separate connection pools/databases, PDBs, anti-affinity across AZs); liveness only checks the process, readiness removes the pod from the load balancer; graceful degradation.
4. **Asynchronous purchase flow:** order `PENDING` → queue (SQS, Amazon MQ, MSK/Kafka) → payment workers → `PAID`/`FAILED`; DLQ; idempotency keys (never charge twice); Saga pattern with compensating actions.
5. **Third-party:** Stripe/Adyen/Braintree (PCI DSS, fraud, webhooks), secondary provider, rate limiting with API Gateway/WAF, Network Policies + Security Groups to isolate payments.
6. **Prevention:** load tests of checkout, chaos engineering (AWS FIS, Chaos Mesh, LitmusChaos), observability (circuit breaker state, queue depth, checkout SLO), canary/blue-green with Argo Rollouts/Flagger, blameless postmortem.

> *"Services must fail independently: timeouts, circuit breakers and bulkheads, and payments moved to an asynchronous, queue-based flow with idempotency, so a payment failure never takes down the whole website again."*
