# Key Vault y Cosmos DB

Dos servicios PaaS que no aparecen en tu CV actual. No hace falta ser experto
en modelado de datos de Cosmos DB — el foco senior-DevOps es operarlos:
seguridad, acceso, backup, costos.

## Key Vault

### Objetivos
- Guardar y rotar secrets, keys y certificados.
- Acceder desde una app vía Managed Identity (RBAC de Key Vault, no Access Policies legacy).
- Integrar Key Vault con Container Apps / Functions como referencia de secret (sin copiar el valor).
- Soft-delete y purge protection (por qué son obligatorios en producción).

### Recursos
- Key Vault overview: https://learn.microsoft.com/azure/key-vault/general/overview

## Cosmos DB

### Objetivos
- Entender los modelos de API (NoSQL/Core, MongoDB, Cassandra, Gremlin, Table) —
  saber cuál usar según el caso (tenés experiencia con MongoDB, así que la API
  Mongo de Cosmos DB debería resultarte familiar).
- Modelo de consistencia: los 5 niveles (Strong, Bounded Staleness, Session,
  Consistent Prefix, Eventual) y el trade-off con latencia/disponibilidad.
- RU (Request Units): cómo se calculan, provisioned throughput vs serverless vs autoscale.
- Partition key: por qué es la decisión de diseño más importante (hot partitions).
- Backup (periodic vs continuous) y disaster recovery (multi-region writes).

### Recursos
- Cosmos DB overview: https://learn.microsoft.com/azure/cosmos-db/introduction
- Consistency levels: https://learn.microsoft.com/azure/cosmos-db/consistency-levels
- Partitioning: https://learn.microsoft.com/azure/cosmos-db/partitioning-overview

## Lab sugerido

Desplegá un Cosmos DB (API NoSQL, tier serverless para no gastar), conectate
desde una API FastAPI usando Managed Identity + Key Vault (el connection string
vive en Key Vault, la app lo referencia, no lo copia como env var plano).

## Autoevaluación

Pedime: *"Dame un examen de Key Vault y Cosmos DB nivel senior"*.
