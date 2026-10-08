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

**Estado (2026-10-05, ✅ cubierto):** síntesis completa de "app a BD sin
exponer secretos" — Managed Identity/IAM Role (tema 04) → Key Vault/Secrets
Manager → Private Endpoint/PrivateLink (tema 05), sin ayuda.

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

**Estado (2026-10-05, ✅ cubierto):** niveles de consistencia (fuerte vs.
eventual) respondido sin ayuda — cierra el hueco marcado desde el
diagnóstico inicial (2026-09-08).

## Bases de datos relacionales gestionadas — ✅ cubierto 2026-10-05

### Objetivos
- Diferenciar una base **relacional gestionada compatible con Postgres/MySQL**
  de una NoSQL (arriba): sigue siendo SQL, pero la nube gestiona parches,
  backups, alta disponibilidad y réplicas de lectura.

### Equivalencias

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Relacional gestionada (Postgres/MySQL) | Azure Database for PostgreSQL/MySQL | **RDS** (Postgres/MySQL/otros motores) | **Cloud SQL** |
| Relacional de alto rendimiento (compatible Postgres) | — | **Aurora** (Postgres/MySQL compatible) | **AlloyDB** (Postgres compatible) |

**AlloyDB** es la apuesta de GCP para cargas relacionales exigentes sin
migrar a NoSQL: mismo lenguaje (SQL/Postgres), separación de
cómputo/almacenamiento, y un motor columnar en memoria para analítica sobre
los mismos datos transaccionales (HTAP) — el equivalente conceptual de
Aurora en AWS.

## Herramientas que piden las ofertas (startup)

| Herramienta | Qué es | Equivalentes |
|---|---|---|
| **AlloyDB** | Base de datos de GCP **compatible con PostgreSQL**, de alto rendimiento (más rápida que Cloud SQL para cargas transaccionales y analíticas), con soporte de vectores (**pgvector**, tema 16) | Azure Database for PostgreSQL · Amazon **Aurora PostgreSQL** |
| **ESO (External Secrets Operator)** | Operador de Kubernetes que **sincroniza secretos** desde Key Vault / Secrets Manager / Secret Manager hacia `Secret` de Kubernetes. Los secretos viven en la nube, no en el repo ni en los manifiestos | Alternativa: **Secrets Store CSI Driver** (monta los secretos como archivos) |
| **Atlas** (Ariga) | Herramienta de **migraciones de schema de base de datos como código** ("Terraform para el schema"): declarás el schema deseado y **Atlas** calcula el plan de migración, lo valida en CI (*lint*) y lo aplica | Flyway, Liquibase, Alembic (Python) |
| **Valkey** | **Cache / key-value en memoria**, fork open source de **Redis** (Linux Foundation, tras el cambio de licencia de Redis en 2024). Misma API que Redis | Azure Managed Redis · Amazon **ElastiCache for Valkey** · **Memorystore for Valkey** (GCP) |

> Si en una oferta "Atlas" aparece junto a MongoDB, se refiere a
> **MongoDB Atlas** (la base MongoDB gestionada). En esta lista, al ir junto
> a AlloyDB, Valkey y Flipt, lo más probable es **Atlas de Ariga**
> (migraciones de schema). Conviene preguntarlo en la entrevista.

Subtemas extra:
- **AlloyDB** vs. Cloud SQL vs. Aurora: cuándo vale la pena pagar más.
- **ESO**: `SecretStore` / `ClusterSecretStore` + `ExternalSecret`; autenticación con Workload Identity / IRSA (tema 10), sin credenciales estáticas.
- **Atlas**: enfoque declarativo vs. versionado, `atlas migrate lint` en el pipeline de CI (tema 03).
- **Valkey**: patrones de cache (*cache-aside*, TTL, invalidación), sesiones, rate limiting.

- AlloyDB: https://cloud.google.com/alloydb/docs
- External Secrets Operator: https://external-secrets.io/
- Atlas: https://atlasgo.io/docs
- Valkey: https://valkey.io/docs/

## Lab sugerido

Desplegá el mismo modelo de datos simple (ítems con partition key) en Cosmos
DB (API NoSQL) y en DynamoDB. Compará cómo se define la partition key y cómo
se estima/factura el throughput en cada una.

## Autoevaluación

Pedime: *"Dame un examen de secretos y bases NoSQL multi-cloud nivel senior"*
o *"Dame un examen de bases relacionales gestionadas (RDS/Cloud SQL/AlloyDB)"*.
