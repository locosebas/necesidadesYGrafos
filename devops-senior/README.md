# Plan de aprendizaje — Camino a Senior DevOps Engineer

Carpeta de estudio personal de Sebastián Díaz para cerrar brechas hacia un rol
**Senior DevOps / Azure Platform Engineer**, preparar certificaciones y medir
avance con exámenes de autoevaluación.

Origen: mensaje de Julieta García (PlatformX Solutions) sobre una vacante de
**Azure Platform Engineer** (contractor, remoto, largo plazo). El stack pedido
en esa vacante es la referencia principal usada para el diagnóstico de brechas.

## Estructura

```
devops-senior/
├── 00-diagnostico/        # dónde estás hoy vs. dónde necesitas estar
│   ├── gap-analysis.md
│   └── roadmap.md
├── temas/                 # una carpeta por tema, con teoría + labs + lecturas
│   ├── 01-iac-terraform-bicep/
│   ├── 02-azure-container-apps-acr/
│   ├── 03-cicd-github-actions-oidc/
│   ├── 04-identity-entra-id-rbac/
│   ├── 05-networking-azure/
│   ├── 06-keyvault-cosmosdb/
│   ├── 07-observabilidad/
│   ├── 08-python-fastapi-docker/
│   ├── 09-azure-durable-functions/
│   ├── 10-kubernetes-avanzado/
│   ├── 11-seguridad-devsecops/
│   ├── 12-arquitectura-costos-well-architected/
│   └── 13-mercadolibre-scopes-cosmos/   # material interno MELI (confidencial, no compartir)
├── certificaciones/       # qué certificar, en qué orden, y por qué
├── examenes/               # cómo pedir exámenes y dónde queda el registro de resultados
│   ├── README.md
│   └── registro/
└── recursos/               # glosario y enlaces generales
```

## Cómo usar esto día a día

1. **Elegí un tema** de `temas/` (seguí el orden sugerido en `00-diagnostico/roadmap.md`,
   o el que te interese repasar).
2. **Leé** el `README.md` de ese tema: tiene objetivos, subtemas y enlaces oficiales.
3. **Pedime un examen** de ese tema (ver `examenes/README.md` para el formato).
   Resolvelo, te corrijo, y anotamos el resultado en `examenes/registro/`.
4. Revisamos juntos los puntos débiles y volvemos a ese tema o pasamos al siguiente.

No hace falta pedirme permiso para arrancar: decime "dame un examen de Bicep nivel
intermedio" o "explicame Private Endpoints" y seguimos desde ahí.

> ⚠️ **Nota de confidencialidad**: `temas/13-mercadolibre-scopes-cosmos/` contiene
> material interno de MercadoLibre (preguntas de entrevista del equipo Scopes Govern).
> Este repositorio es privado por decisión explícita del dueño. Si en algún momento
> este repo pasa a ser público, esa carpeta debe eliminarse del historial de git antes.
