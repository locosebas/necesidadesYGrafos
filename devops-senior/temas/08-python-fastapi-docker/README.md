# Python / FastAPI + Docker

Partís de una base fuerte de Python. El objetivo es consolidar FastAPI
específicamente (async, dependency injection, validación con Pydantic) y
buenas prácticas de Docker para APIs Python en producción.

## Objetivos

- Escribir endpoints async correctamente (cuándo `async def` ayuda realmente
  vs cuándo es cosmético porque la librería subyacente es sync).
- Dependency Injection de FastAPI (`Depends`) para DB sessions, auth, config.
- Validación y serialización con Pydantic v2 (models, `BaseSettings` para config
  por variables de entorno — relevante para Container Apps).
- Manejo de errores consistente (exception handlers globales).
- Dockerfile multi-stage para apps Python (imagen final chica, sin build tools).
- Health checks (`/healthz`, `/readyz`) — necesarios para probes de Container Apps/K8s.

## Subtemas

1. FastAPI: routing, `Depends`, middlewares, background tasks
2. Pydantic: `BaseModel`, `BaseSettings`, validators
3. Async I/O: cuándo usar `httpx.AsyncClient`, `asyncpg`, drivers async de Cosmos DB
4. Testing: `pytest` + `TestClient`/`httpx` async client
5. Dockerfile multi-stage, `--no-cache-dir`, usuario no-root, `HEALTHCHECK`
6. Observabilidad: instrumentación de OpenTelemetry/App Insights en FastAPI

## Recursos

- FastAPI docs: https://fastapi.tiangolo.com/
- Pydantic docs: https://docs.pydantic.dev/

## Lab sugerido

Reescribí (o extendé) la API del lab de Cosmos DB con: endpoints async,
validación Pydantic estricta, manejo de errores global, health check, y
Dockerfile multi-stage corriendo como usuario no-root.

## Autoevaluación

Pedime: *"Dame un examen de FastAPI y Docker nivel senior"*.
