# Presentación base para entrevistas (DevOps / Plataforma)

Presentación en inglés que se usa como **base para la mayoría de las
entrevistas**: experiencia (Bizagi, MercadoLibre) con íconos de las
herramientas, preguntas técnicas con respuestas modelo y preguntas para el
entrevistador. Las notas del presentador tienen el guion en inglés y tips en
español ("ES:").

- **Presentación publicada (Slides):** https://claude.ai/artifact/CRWSFU5JbdMHiBarCdxG1G
- Creada para la entrevista del 2026-11-04 (ver `../temas/31-entrevista-2026-11-04/`).

## Estructura (24 diapositivas)

| Bloque | Diapositivas (`project/slides/<id>.html`) |
|---|---|
| Intro | `cover`, `journey`, `toolbox` |
| Bizagi | `bizagi` (CI/CD), `bizagiobs` (observabilidad: Grafana + alertas/on-call), `bizagiint` (SSO/OIDC con Entra ID, proveedores externos, CI) |
| MercadoLibre | `meli` (PaaS de cómputo), `meliterraform` (módulos, state/backends, migraciones), `melitriage` + `melitriage2` (diagnóstico de tickets de Zendesk con Claude: RAG + MCP, certezas/hipótesis, **no auto-resuelve**), `ops` |
| Preguntas | `qdivider`, `egress`, `egresscloud`, `egressdebug` (salida a internet desde un Pod), `incident`, `incidentroles`, `incidentexample` (incidente en producción), `rapidk8s`, `rapidlinux`, `rapidaws`, `morequestions` |
| Cierre | `askthem`, `close` |

## Cómo reutilizarla para otra entrevista

1. Las diapositivas de **experiencia** (intro, Bizagi, MercadoLibre) son fijas.
2. Las de **preguntas** se cambian según lo que mande cada reclutador:
   agregar/quitar archivos en `project/slides/` y ajustar `order` en
   `project/deck.json`.
3. Publicar como una presentación nueva del tipo Slides (o actualizar la
   existente). Los íconos están en `iconos/` como PNG; en la presentación
   publicada ya están subidos como assets (`/_blob/<id>` en los `src`). En
   una presentación nueva hay que volver a subirlos y reemplazar esos `src`.

## Pendientes de completar (marcados en las notas)

- Fuente de datos de Grafana en Bizagi (Azure Monitor / Log Analytics / Prometheus / Loki).
- Nombre del proveedor de correos integrado en Bizagi.
- Backend real del state de Terraform en MercadoLibre.
- Cifra real de ahorro de tiempo del diagnóstico con Claude (si existe).
- Un incidente real propio contado en 4 frases (síntoma, diagnóstico, arreglo, prevención).

Íconos: logos de [devicon](https://devicon.dev) y [Simple Icons](https://simpleicons.org).
