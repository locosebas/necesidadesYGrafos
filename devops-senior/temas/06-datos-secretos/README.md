# Gestión de secretos y bases de datos gestionadas

Key Vault y Cosmos DB (Azure) no aparecen en tu CV. Los equivalentes de
AWS/GCP conviene repasarlos igual, ya que tenés experiencia con MongoDB y
podés compararlos directamente.

## Gestión de secretos

### Objetivos
- Guardar y rotar secrets/keys/certificados sin que vivan en variables de
  entorno planas ni en el repo.
- Acceder desde una app vía identidad gestionada (no credenciales copiadas).

### Equivalencias

| Azure | AWS | GCP |
|---|---|---|
| **Key Vault** | **Secrets Manager** (rotación nativa) o **Parameter Store** (SSM, más simple/barato) | **Secret Manager** |

### Recursos
- Key Vault: https://learn.microsoft.com/azure/key-vault/general/overview
- AWS Secrets Manager: https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html
- GCP Secret Manager: https://cloud.google.com/secret-manager/docs

## Bases de datos NoSQL gestionadas

### Objetivos
- Modelo de consistencia y su trade-off con latencia/disponibilidad (ya
  relevante para vos por tu experiencia con MongoDB).
- Cómo se calcula/factura el throughput en cada una.
- Partition key / sharding: la decisión de diseño más importante en todas (hot partitions).

### Equivalencias

| Concepto | Azure Cosmos DB | AWS DynamoDB | GCP Firestore / Bigtable |
|---|---|---|---|
| Modelo de datos | Multi-modelo (API NoSQL, MongoDB, Cassandra, Gremlin, Table) | Documento/clave-valor | Firestore: documentos. Bigtable: ancho columnar (alto volumen) |
| Unidad de throughput | **RU** (Request Units) | **RCU/WCU** (Read/Write Capacity Units) o On-Demand | Firestore: sin unidad explícita (facturado por operación). Bigtable: nodos |
| Niveles de consistencia | 5 niveles (Strong → Eventual) | Eventually consistent (default) o Strongly consistent (por request) | Firestore: strong consistency por default |
| Partition key | Partition key explícita | Partition key (+ opcional sort key) | Firestore: por colección/documento; Bigtable: row key |
| Multi-región | Multi-region writes configurable | Global Tables | Firestore: multi-región nativo |

### Recursos
- Cosmos DB: https://learn.microsoft.com/azure/cosmos-db/introduction
- DynamoDB: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
- Firestore: https://cloud.google.com/firestore/docs

## Lab sugerido

Desplegá el mismo modelo de datos simple (ítems con partition key) en Cosmos
DB (API NoSQL) y en DynamoDB. Compará cómo se define la partition key y cómo
se estima/factura el throughput en cada una.

## Autoevaluación

Pedime: *"Dame un examen de secretos y bases NoSQL multi-cloud nivel senior"*.
