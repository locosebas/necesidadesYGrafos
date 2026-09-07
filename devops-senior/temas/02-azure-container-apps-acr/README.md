# Azure Container Apps + Azure Container Registry (ACR)

Partís de una base sólida de Docker y Kubernetes. Azure Container Apps (ACA) es
un serverless container platform sobre Kubernetes/KEDA/Dapr — más simple que
gestionar un AKS propio. El objetivo es entender cuándo usar ACA vs AKS y
dominar el flujo build → push (ACR) → deploy (ACA).

## Objetivos

- Explicar ACA vs AKS vs App Service vs Container Instances (cuándo cada uno).
- Dominar el ciclo de vida de una **revisión** (revision) en ACA (blue/green,
  traffic splitting entre revisiones).
- Configurar autoscaling con KEDA (scale rules: HTTP, CPU, colas, custom).
- Integrar ACA con Dapr (service invocation, pub/sub, state management) — nice to have.
- Push/pull seguro a ACR (autenticación con Managed Identity, no credenciales sueltas).
- Escaneo de imágenes en ACR (Microsoft Defender for Containers / ACR Tasks).

## Subtemas

1. Container Apps Environment (red interna, Log Analytics workspace asociado)
2. Revisions y revision modes (single vs multiple)
3. Ingress: externo vs interno, traffic splitting
4. Scale rules con KEDA (min/max replicas, reglas de escalado a cero)
5. Secrets y variables de entorno (integración con Key Vault via Managed Identity)
6. ACR: repositorios, tags, geo-replicación, ACR Tasks (build automatizado)
7. Autenticación ACA → ACR sin usuario/password (Managed Identity + `AcrPull` role)

## Recursos

- Container Apps overview: https://learn.microsoft.com/azure/container-apps/overview
- Container Registry overview: https://learn.microsoft.com/azure/container-registry/container-registry-intro
- KEDA scalers: https://keda.sh/docs/latest/scalers/

## Lab sugerido

Dockerizá una API simple (podés reusar algo de `08-python-fastapi-docker`),
subila a un ACR de prueba, desplegala en Container Apps con Managed Identity
(sin admin credentials en el ACR) y configurá un scale rule por HTTP concurrency.

## Autoevaluación

Pedime: *"Dame un examen de Azure Container Apps nivel senior"*.
