# Fórmula 07 — Llevar una API (FastAPI) a producción: contenedor y serverless

**Resumen en una línea:** *app con health checks y config por entorno →
Dockerfile seguro → registry → runtime (Container Apps / Cloud Run / Fargate
o K8s) → identidad y secretos → red privada a la base → CI/CD → observabilidad
→ escalado.*

---

## Paso 1 — La app lista para producción ("12-factor")

- Config por **variables de entorno**, no hardcodeada.
- Endpoints `/healthz` (liveness) y `/readyz` (readiness: chequea la DB).
- Logs a **stdout** en JSON. Stateless (sesiones/archivos en servicios externos).
- Apagado ordenado (manejar SIGTERM).

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
```

## Paso 2 — Dockerfile seguro (multi-stage, no root)

```dockerfile
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /install /usr/local
COPY app/ ./app
RUN useradd -r -u 10001 appuser
USER 10001
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Claves: imagen base chica, dependencias antes del código (cache de capas),
`.dockerignore`, usuario no root, sin secretos en la imagen.

## Paso 3 — Registry

ACR / ECR / Artifact Registry, **privado**, escaneo de vulnerabilidades
activado, el runtime hace pull con **identidad** (no con usuario/password).

## Paso 4 — Elegir el runtime

| Necesidad | Azure | AWS | GCP |
|---|---|---|---|
| Contenedor sin gestionar clúster | **Container Apps** | **ECS Fargate** / App Runner | **Cloud Run** |
| Control total / muchos servicios | AKS | EKS | GKE |
| Funciones por evento | Azure Functions | Lambda | Cloud Run functions |
| Orquestación de pasos largos | **Durable Functions** | **Step Functions** | **Workflows** |

Regla: pocos servicios HTTP/eventos → serverless de contenedores
(escala a cero, cero ops de nodos). Muchos equipos/servicios, necesidades
especiales (sidecars, GPU, operators) → Kubernetes (fórmula 01).

## Paso 5 — Identidad y secretos

- **Managed Identity / task role / service account** para la app.
- Permisos mínimos: leer *sus* secretos en Key Vault, escribir en *su* cola.
- Secretos referenciados desde Key Vault / Secrets Manager (Container Apps y
  ECS los inyectan como env vars sin exponerlos en la config).

## Paso 6 — Red y datos

- App en VNet/VPC (Container Apps environment con VNet, Fargate en subnets
  privadas, Cloud Run con Direct VPC egress).
- Base de datos gestionada (PostgreSQL Flexible Server / RDS / Cloud SQL,
  o Cosmos DB / DynamoDB / Firestore para NoSQL) **solo con acceso privado**
  (Private Endpoint / subnet privada).
- Entrada pública solo por el ingress gestionado / ALB / API Gateway / Front Door + WAF.

## Paso 7 — CI/CD

Fórmula 04: test → build → scan → push con tag SHA → deploy con OIDC →
revisiones/traffic splitting (Container Apps y Cloud Run lo traen nativo
para canary).

## Paso 8 — Observabilidad y escalado

- OpenTelemetry → App Insights / CloudWatch / Cloud Trace (fórmula 05).
- Autoscaling por requests concurrentes / CPU / largo de cola
  (Container Apps usa reglas **KEDA**).
- `min replicas ≥ 1` en prod si el cold start importa.

## Serverless orquestado (Durable Functions y equivalentes)

- **Orchestrator** (código determinista que coordina, se "rehidrata" por
  event sourcing) + **activities** (el trabajo real, con efectos).
- Patrones: function chaining, **fan-out/fan-in**, async HTTP API
  (202 + URL de estado), monitor, **human interaction** (esperar evento externo con timeout).
- Equivalentes: Step Functions (estados en JSON/ASL), GCP Workflows (YAML).
- En el orchestrator **no** usar `datetime.now()`, random ni I/O directo:
  rompe el replay.

## Prueba "funciona"

`curl https://api.empresa.com/healthz` → 200 por HTTPS, la app lee su secreto
de Key Vault sin credenciales en la config, llega a la DB por red privada
(y la DB **no** es accesible desde internet), la request aparece en las
trazas, y con carga suben las réplicas.
