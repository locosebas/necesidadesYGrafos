# Bloque 4 - Canary con progressive delivery en GitOps

**Escenario (resumen):** Platform Engineering en un SaaS B2B sobre EKS. Cada servicio tiene un repo de
configuración por entorno que Argo CD reconcilia; los servicios críticos salen a producción con canary.
On-call de releases: promociones seguras, diagnóstico con métricas/logs/traces y evitar drift entre Git
y el clúster.

---

## Pregunta 1 - Top 4 acciones en los próximos ~10 minutos

Evidencia: PR de promoción mergeado 10:12; sync 10:14 con ~10% al candidato; 10:17 el canary tiene más
5xx; 10:18 la latencia empeora en todo el servicio, incluido el stable; 10:19 alerta de latencia en una
dependencia downstream compartida; la imagen se referencia por tag (no digest) y ese tag se empujó
varias veces en la última hora; Argo CD con auto-sync.

```text
- Abort the canary now with the rollout controller (e.g. kubectl argo rollouts abort <rollout>), sending 100% of traffic back to the stable cohort. Purpose: contain customer impact from the candidate's 5xx immediately, using the controller's own mechanism, which changes rollout status rather than the spec, so Argo CD's auto-sync does not fight it or create drift.

- Watch the service-wide and downstream dependency metrics/traces for the next few minutes after the abort, and compare the candidate's calls to the dependency (call rate, retries, timeouts) against the stable cohort. Purpose: learn whether the candidate caused the dependency degradation (e.g. a retry storm or connection exhaustion that also hurt the stable cohort) or whether the dependency has an independent problem that needs its own owner and incident track.

- Verify exactly which image is running in each cohort by checking the image digests on the pods (kubectl get pods -o jsonpath on status.containerStatuses[].imageID) and comparing them with the push history of the tag in the registry (ECR describe-images). Purpose: the tag was pushed more than once, so I need to confirm the candidate is the build we think it is, and that the "stable" pods did not pull the new image under the same tag after a restart or scale-up, which would also explain the stable cohort's degradation.

- Make Git match the decision: revert the 10:12 promotion PR in the production environment repo, pinning the service to the last known-good image by digest (image@sha256:...) instead of the tag, and post the status in the incident channel. Purpose: Argo CD then reconciles the cluster to a known-good, immutable desired state with no Git-vs-live drift, and the bad candidate cannot be re-deployed by an auto-sync or a tag overwrite (follow-up: enable ECR tag immutability and reference images by digest in all production overlays).
```

---

## Pregunta 2 (video, 30 s) - Stakeholder: "¿No podemos hacer hot-fix directo en producción y limpiar Git después?"

**Ideas:**

```text
1. Errors already contained → traffic back on stable version
2. Hot-fix won't last → platform undoes manual changes → errors could return
3. Fix through Git → same few minutes → it sticks
4. Doing it now → update in 10 min
```

**Libreto:**

> "Good news: the errors are already contained. We stopped the new version and all traffic is back on the stable one. A direct hot-fix wouldn't even last: our platform automatically undoes manual changes within minutes, so the errors could come back. Making the fix through Git takes the same few minutes, and it actually sticks. I'm doing that now, and I'll update you in ten minutes."

---

## Pregunta 3 (video, 30 s) - Rollout fallido con migración de base de datos: ¿rollback o roll-forward?

**Ideas:**

```text
1. Pause rollback → old version + new schema = second outage
2. Ask → additive or destructive? / fully completed? / new data written?
3. Compatible → roll back app | Not compatible → roll forward with fix
4. Confirm recent DB snapshot first
```

**Libreto:**

> "First, let's pause the rollback: the old version may not work with the new schema, and we could cause a second outage. I need three answers: was the migration additive or destructive, did it fully complete, and has new data already been written in the new format? If it's backward-compatible, we roll back the app. If not, we roll forward with a fix, because undoing the migration could lose data. Either way, I confirm we have a recent database snapshot first."

**Si preguntan cómo evitarlo:** patrón **expand-contract** (parallel change): primero solo se agregan
columnas/tablas, luego se migra el código, y en un release posterior se borra lo viejo. Así el rollback
de la app siempre es seguro.
