# Troubleshooting de Kubernetes

Este archivo va **último a propósito**: troubleshooting real es mucho más
fácil una vez que ya tenés clara la arquitectura (`01`), scheduling/recursos
(`02`) y networking (`03`) — la mayoría de los errores de troubleshooting
son "un componente de esos no hizo lo que esperabas".

> Marcado en `examenes/registro/resultados.md` como brecha declarada: nunca
> se manejó en la práctica. Pedir sesión de escenarios reales acá, no
> preguntas teóricas.

## Objetivos

- `CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff` — causa raíz de cada uno.
- Orden de diagnóstico: `kubectl get` → `kubectl describe` → `kubectl logs` (`--previous` si ya reinició) → eventos del namespace.
- Exit codes comunes de contenedores y qué significan.

## Los tres clásicos

| Síntoma | Causa raíz típica | Dónde se ve |
|---|---|---|
| `CrashLoopBackOff` | El proceso del contenedor termina (crashea) apenas arranca, y Kubernetes lo reintenta con backoff exponencial | `kubectl logs --previous <pod>` (el log del intento anterior, no del actual que puede estar vacío) |
| `OOMKilled` | El contenedor superó su **memory limit** y el kernel lo mató | `kubectl describe pod` → `Last State: Terminated, Reason: OOMKilled`; conecta con QoS classes de `02-scheduling-recursos-autoscaling.md` |
| `ImagePullBackOff` / `ErrImagePull` | No se pudo descargar la imagen: tag mal escrito, imagen no existe, o falta autenticación al registry (ACR/ECR/Artifact Registry) | `kubectl describe pod` → sección `Events` |

## Orden de diagnóstico recomendado

1. `kubectl get pods -n <namespace>` — ver el `STATUS` y `RESTARTS`.
2. `kubectl describe pod <pod>` — sección `Events` (al final): casi siempre dice la causa en texto plano.
3. `kubectl logs <pod>` (y `kubectl logs <pod> --previous` si ya reinició) — el log de la app misma.
4. Si el pod ni siquiera aparece asignado a un nodo: revisar `kubectl describe pod` por eventos de **scheduling** (falta de recursos, taints sin tolerar — conecta con `02`).
5. Si el problema es de red (el pod corre pero no lo alcanzan): revisar `03-networking-service-mesh.md` (Service, NetworkPolicy, o si el sidecar de Istio está healthy).

## Exit codes comunes

| Exit code | Significado |
|---|---|
| `0` | Salida normal |
| `1` | Error genérico de la aplicación |
| `137` | `128 + 9` → mató con `SIGKILL` (típico de `OOMKilled` o `kubectl delete --force`) |
| `143` | `128 + 15` → terminó con `SIGTERM` (shutdown normal que no llegó a tiempo) |

## Recursos

- Debug Pods: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
- Debug Running Pods: https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/

## Autoevaluación

Pedime: *"Dame un examen de Kubernetes troubleshooting nivel senior"* —
preguntas **de escenario** ("un pod está en CrashLoopBackOff, ¿qué revisás
primero?"), no teóricas puras.
