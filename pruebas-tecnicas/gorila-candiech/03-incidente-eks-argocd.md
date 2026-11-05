# Bloque 3 - Incidente en EKS después de un sync de Argo CD

**Escenario (resumen):** SaaS B2B multi-tenant en EKS (subredes privadas, varias AZ). Apps por GitOps
con Argo CD, infraestructura con Terraform. Tráfico externo por un load balancer creado desde un
Ingress. HPA para pods y node autoscaler para nodos. El incidente arranca justo después de un release.

---

## Pregunta 1 - Nota de incidente con el plan de primera respuesta (máximo 5 bullets)

Evidencia: sync de Argo CD a las 14:01; 5xx desde ~14:03; el HPA pide más réplicas pero los pods
nuevos no arrancan (`FailedCreatePodSandbox ... failed to assign an IP address to pod`); IPs libres
por subred: a = 3, b = 1, c = 900; el ALB devuelve 503 con target group 0 healthy / 6 unhealthy;
Ingress `target-type = instance` y Service `ClusterIP`.

**Clave:** son dos problemas. El 503 total lo explica `target-type: instance` + Service `ClusterIP`
(instance necesita NodePort) y coincide con el sync; la IP exhaustion de la VPC CNI en las subredes a/b
es secundaria (impide escalar, pero no explica que los pods viejos estén unhealthy).

```text
- IMPACT / SCOPE: Full outage of the public API since ~14:03. The load balancer returns HTTP 503 for all customers/tenants, because the target group has 0 healthy / 6 unhealthy targets. Onset is ~2 minutes after the Argo CD production sync at 14:01, so the release is the prime suspect. Secondary issue: new pods cannot start (FailedCreatePodSandbox, no IP) because private subnets a and b are nearly out of IPs (3 and 1 available; subnet c has 900), so we cannot scale out of this.

- CONTAINMENT (now): Roll back the 14:01 release through GitOps (git revert of the release commit, or Argo CD rollback with auto-sync paused so it isn't immediately re-applied), with priority on restoring the previous Ingress/Service configuration. The rollback should not depend on scheduling many new pods in subnets a/b; if it does, the new pods should land in AZ c. No manual kubectl edits on live resources that Argo CD would overwrite.

- CHECK 1 (Kubernetes): Diff the Service and Ingress manifests between the 14:01 sync and the previous revision (Argo CD app diff/history, kubectl get svc,ingress -o yaml), and read the AWS Load Balancer Controller logs (kubectl logs -n kube-system deploy/aws-load-balancer-controller) for reconcile errors such as an instance target type with a ClusterIP service.

- CHECK 2 (AWS): aws elbv2 describe-target-health on the target group to get the unhealthy reason codes (e.g. Target.FailedHealthChecks / Target.Timeout), and compare the registered port and health check port with the Service's NodePort. Also check the subnet IP usage (ENIs and the VPC CNI warm IP pool per node) to size the IP exhaustion as a separate follow-up.

- LEADING HYPOTHESIS: The release changed the Service from NodePort to ClusterIP (or changed the Ingress annotation from target-type ip to instance). With target-type instance the ALB sends traffic to the nodes on a NodePort, and a ClusterIP service has no NodePort, so every target fails its health checks and the ALB returns 503. Expected evidence: the Git diff shows the Service type or target-type annotation changing in the 14:01 commit, the controller logs show reconcile errors, and target health shows failed health checks on all 6 node targets. Once that config is reverted, targets should turn healthy within a few health-check intervals. The IP exhaustion in subnets a/b is a real but secondary capacity problem, handled after service is restored.
```

---

## Pregunta 2 (video, 30 s) - Un compañero propone cambios en vivo fuera de GitOps ("reconciliamos Git/Terraform después")

**Ideas:**

```text
1. Agree → traffic back is the priority
2. Live edits won't stick → Argo CD reverts / add-ons overwritten / lose track
3. Fastest safe fix → revert 14:01 release in Git → Argo CD syncs
4. If needed → ONE scoped break-glass, logged, auto-sync paused, codified right after
```

**Libreto:**

> "I agree, getting traffic back is the priority. But live edits won't stick: Argo CD will revert them, EKS add-ons get overwritten, and we lose track of what actually fixed or broke things. We already have a strong suspect, the 14:01 release, so the fastest safe fix is reverting it in Git and letting Argo CD sync. If that fails, we do one scoped break-glass change, logged here, with auto-sync paused, and codified in Git right after, not 'later'."

---

## Pregunta 3 (video, 30 s) - Un PM pregunta: ¿rollback del release o seguir investigando?

**Ideas:**

```text
1. Roll back now + investigate in parallel
2. Why → started 2 min after release / full outage / known-good version
3. Quick check → nothing irreversible (DB migrations)
4. Evidence saved → root cause later → update in 15 min
```

**Libreto:**

> "We roll back now, and keep investigating in parallel. The errors started two minutes after the release, it's a full outage for every customer, and rolling back returns us to a version we know works. I'll do a quick check that the release has nothing irreversible, like database migrations. We've already saved the evidence, so we'll still find the root cause. I'll update you in fifteen minutes."
