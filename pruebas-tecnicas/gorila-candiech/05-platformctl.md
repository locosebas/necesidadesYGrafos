# Bloque 5 - Herramienta interna de on-call `platformctl` (Python)

**Escenario (resumen):** utilidad en Python que el on-call corre desde laptops y a veces desde CI para
inspeccionar workloads y hacer mitigaciones acotadas (reiniciar pods). Tras un near-miss, el equipo
quiere que sea más segura, fácil de diagnosticar y predecible.

El script propuesto: `run()` con `subprocess.run(cmd, shell=True)`; `find_context()` que hace
`eks.list_clusters()` sin paginar y devuelve el primer cluster cuyo nombre contiene `env`;
`restart_crashlooping()` que hace `log.info("env_dump=%s", dict(os.environ))`, `kubectl config
use-context`, `kubectl get pods ... | grep CrashLoopBackOff` y `kubectl delete pod` por cada línea;
defaults `ENV=prod`, `NAMESPACE=default`, `SELECTOR=""`; al final siempre imprime `done`.

---

## Pregunta 1 - Hasta 4 problemas relevantes para producción (riesgo + mejora)

```text
1) SECRETS LEAKED TO LOGS
Issue: restart_crashlooping() logs dict(os.environ), the entire environment of the process.
Risk/impact: On laptops and especially in CI, the environment contains AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, CI tokens and other credentials. They end up in CI job logs, shared terminals, log aggregators or pasted incident notes, where anyone with log access can read them. A tool meant to reduce incident risk becomes a credential-leak vector, and the incident turns into a security incident with key rotation on top.
Improvement: Never log the environment. Log only an explicit, non-sensitive set of fields (env, region, cluster, namespace, selector, the identity running the tool from sts get-caller-identity, and the pods acted on), and add a redaction filter/secret scanning on CI logs as defense in depth.

2) IT CAN TARGET THE WRONG CLUSTER (OR PRODUCTION BY DEFAULT)
Issue: find_context() picks the first cluster whose name contains the env string ("prod" also matches "preprod", "prod-old", "nonprod"), ignores pagination (nextToken), so the right cluster may not be in the first page, and returns None without failing. The return value is then passed to "kubectl config use-context None", which fails silently, so the script keeps running against whatever context was already active. The EKS cluster name is also not necessarily the kubeconfig context name. On top of that, ENV defaults to "prod", and use-context permanently changes the engineer's kubeconfig after the script exits.
Risk/impact: Under pressure, the tool can delete pods in the wrong cluster, including production, without anyone noticing, and leave the engineer's terminal pointing to an unexpected cluster for their next manual command.
Improvement: Require ENV explicitly (no "prod" default), resolve the cluster by exact name with full pagination, fail hard if zero or more than one cluster matches, and pass --context (or a dedicated kubeconfig) on every kubectl call instead of switching the global context. Print the resolved cluster/account and ask for explicit confirmation for production.

3) COMMAND INJECTION AND FRAGILE PARSING (shell=True)
Issue: Commands are built with f-strings from environment variables (NAMESPACE, SELECTOR, pod names) and executed with shell=True. Pods are selected by grepping the human-readable text output of kubectl get pods.
Risk/impact: Any unexpected value is interpreted by the shell. A selector like "app=x; kubectl delete ns payments" or a malformed value from a CI variable runs arbitrary commands with the engineer's or CI's cluster credentials. The grep on text output is also unreliable: it can match pod names or other columns that contain the string, and it breaks if kubectl's output format changes.
Improvement: Use subprocess with an argument list and shell=False (or the official Kubernetes Python client), validate inputs (namespace/selector format), and select pods from structured output (-o json), filtering on status.containerStatuses[].state.waiting.reason == "CrashLoopBackOff".

4) FAILS SILENTLY, WITH NO SAFETY LIMITS
Issue: Return codes are never checked (no check=True or returncode handling), there are no timeouts, and the script always prints "done". SELECTOR defaults to an empty string and is not validated, there is no dry-run, no maximum number of pods to delete, and the logger is never configured, so log.info messages are not even shown.
Risk/impact: In an incident, an engineer sees "done" and believes mitigation happened when every command may have failed (wrong context, expired credentials, RBAC denied), which wastes critical minutes and sends the investigation in the wrong direction. A hung kubectl call blocks the tool indefinitely. A broad or empty selector can delete far more pods than intended, possibly taking down all replicas at once, and there is no audit trail of what was actually done.
Improvement: Fail fast with a clear error and a non-zero exit code on any failed step, add timeouts, require a non-empty selector, default to dry-run (show the exact pods to be deleted), cap the number of pods per run (e.g. never all replicas of a workload at once, respecting PodDisruptionBudgets), and configure structured logging that records who ran it, against which cluster, and what was deleted.
```

---

## Pregunta 2 - Diseño de "platformctl v2" (máximo 8 bullets)

```text
- SUBCOMMANDS AND MINIMUM REQUIRED INPUTS: Two subcommands with explicit, required inputs and no dangerous defaults. (1) Read-only: "platformctl rollout status --env <staging|prod> --namespace <ns> --deployment <name>" with optional --watch and --timeout. (2) Mutating: "platformctl pods restart --env <staging|prod> --namespace <ns> --deployment <name> --reason <incident-id or text>", with optional --selector (non-empty, only to narrow further within that deployment), --max <n> and --execute. There is no default environment and no empty selector: if a required input is missing, the tool refuses to run.

- SAFE CLUSTER TARGETING: --env maps through a versioned config file to an exact cluster name, AWS account and region (no substring matching). Before doing anything, the tool verifies the caller identity and AWS account (sts get-caller-identity) and that the target cluster matches the expected account. It passes the context explicitly on every call and never changes the operator's global kubeconfig. If anything doesn't match, it fails before touching the cluster.

- READ-ONLY OUTPUT (rollout status): A clear verdict (HEALTHY, PROGRESSING, DEGRADED or FAILED) followed by the evidence behind it: desired vs updated/ready/available replicas, observedGeneration vs generation, the Progressing/Available conditions (e.g. ProgressDeadlineExceeded), the running image digest(s), the Argo CD sync/health status of the app, and the most recent failing pods with their reasons (CrashLoopBackOff, ImagePullBackOff, OOMKilled). With --watch it polls until a final state or the timeout, never hanging indefinitely.

- WHAT IT SHOWS BEFORE MUTATING: Dry-run is the default. Without --execute, the tool only prints the plan: AWS account, cluster, environment, namespace, deployment, operator identity, reason/incident ID, and the exact list of pods it would restart with their status, restart count, age and node, plus "N of M replicas" and the PodDisruptionBudget headroom. For production, --execute also requires typing the environment or cluster name to confirm (not just "y"). Non-interactive use (--yes) is allowed for CI only with an explicit flag and a known service identity.

- GUARDRAILS DURING THE MUTATION: Pods are restarted through the Eviction API (respecting PodDisruptionBudgets) instead of a raw delete, in small batches, waiting for replacements to become Ready before continuing. A maximum per run (default: never more than a fraction of the replicas, never all at once) protects capacity, and the tool stops automatically if replacements don't become Ready within the timeout. It does not modify the Deployment spec (no "rollout restart" annotation), so it never creates drift against the Git desired state managed by Argo CD. It runs with a narrowly scoped RBAC role (get/list/watch plus pods/eviction only).

- SUCCESS VS FAILURE FOR A HUMAN: It ends with one unambiguous summary line, for example "SUCCESS: 3/3 pods restarted, all Ready in 94s" or "FAILED at step 'wait for Ready': 1/3 replacement pods in CrashLoopBackOff, stopped after 1 pod, no further action taken", plus a suggested next step. Results go to stdout; progress and diagnostics go to stderr. It never prints "done" unless every step was verified.

- SUCCESS VS FAILURE FOR A CALLING SYSTEM: Documented, stable exit codes: 0 = success/healthy; 1 = operation failed or rollout unhealthy; 2 = invalid input/usage; 3 = refused by a guardrail or confirmation not given; 4 = partial success; 5 = timeout, authentication or connectivity error. --output json returns a versioned schema (verdict, env, cluster, account, actions taken, pods affected, errors, duration), so CI jobs and automation can make decisions without parsing human text.

- OBSERVABILITY AND AUDIT: Every call has a timeout. Logs are structured, never include secrets or environment dumps, and record who ran what, against which cluster, why (incident ID), and what changed. Mutating actions also send an audit event to the incident channel or audit log, and the tool prints its own version, so behavior is predictable and easy to troubleshoot under pressure.
```

---

## Pregunta 3 (video, 60 s) - Product engineer: "¿Puedes correr el restart amplio en todo producción?"

**Ideas:**

```text
1. I get it → same goal: fix fast
2. Broad restart risks → healthy pods too / capacity loss / DB hit at once / full outage / lose logs / stuck again
3. Alternative → 2 min: check what's stuck → restart only those, small batches, watch healthy → same time, safer
4. Help me → which customer flows fail? → updates in the channel
```

**Libreto:**

> "I get it, we all want this fixed as fast as possible, and I'm with you on that. But a broad restart would also restart everything that's healthy. We'd lose capacity all at once, every service would hit the database at the same time, and we could turn a partial problem into a full outage. We'd also wipe the logs we need, and if the cause is somewhere else, things just get stuck again.
>
> Here's what I suggest: give me two minutes to check which services are actually stuck with our status command. Then I restart only those, in small batches, watching that they come back healthy. It's about the same time, and much safer.
>
> You can really help here: tell me which customer flows are failing, so we start with those. I'll keep you updated in the channel."
