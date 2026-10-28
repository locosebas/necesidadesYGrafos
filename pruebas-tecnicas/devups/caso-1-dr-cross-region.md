# Caso 1 — Disaster Recovery Cross-Region (DevUps)

## Enunciado

Una plataforma productiva está desplegada en **una sola región AWS** con: Route 53, Application Load
Balancer (ALB), ECS (Elastic Container Service) sobre Fargate, ECR (Elastic Container Registry),
Aurora, S3 (Simple Storage Service), Terraform y Terragrunt.

Objetivos del negocio:

- **RPO (Recovery Point Objective) máximo: 5 minutos** → como máximo se pueden perder 5 minutos de datos.
- **RTO (Recovery Time Objective) máximo: 30 minutos** → el servicio debe volver en menos de 30 minutos.
- Recuperarse ante la **pérdida completa de la región primaria**.

Se pide explicar: estrategia de DR (Disaster Recovery), componentes en la región secundaria, Aurora,
S3, ECR, DNS (Domain Name System) y cambio de región, papel de Terraform/Terragrunt, cómo verificar
RPO/RTO y cómo probar el DR periódicamente.

---

## 0. Panorama: las cuatro estrategias de DR en AWS

De más barata/lenta a más cara/rápida:

| Estrategia | Qué hay en la región secundaria | RPO típico | RTO típico |
|---|---|---|---|
| **Backup & Restore** | Solo backups copiados | Horas | Horas (24h) |
| **Pilot Light** | Datos replicándose; cómputo apagado (ECS en 0 tareas) | Segundos/minutos | Decenas de minutos a horas |
| **Warm Standby** | Datos replicándose + copia **reducida pero funcionando** de toda la plataforma | Segundos | Minutos |
| **Multi-site Active/Active** | Copia completa recibiendo tráfico | Casi cero | Casi cero |

Con RPO 5 min y RTO 30 min, **Backup & Restore queda descartado** (restaurar Aurora desde snapshot y
levantar todo toma horas, y el RPO sería el del último snapshot). Active/Active es posible pero caro
y complejo: Aurora tiene un solo writer, habría que resolver escrituras en dos regiones.

## 1. Estrategia elegida: **Warm Standby**

**Warm Standby**: la región secundaria tiene toda la plataforma desplegada y **funcionando a escala
reducida** (por ejemplo ECS con 1-2 tareas por servicio, Aurora con 1 instancia lectora).

Por qué Warm Standby y no Pilot Light:

- **RTO de 30 minutos es justo para Pilot Light**: arrancar desde cero significa provisionar
  cómputo, que pasen health checks, calentar cachés y descubrir errores de configuración *durante el
  desastre*. En Warm Standby la plataforma secundaria **ya está probada y viva todos los días**.
- Un evento regional hace que muchos clientes de AWS fallen hacia la misma región secundaria al mismo
  tiempo: tener capacidad ya corriendo reduce el riesgo de no conseguirla.
- El costo extra de Warm Standby es bajo con Fargate (se paga por tarea corriendo, no por servidores).

En el failover solo hay que hacer **tres cosas**: promover Aurora, escalar ECS y mover el DNS.

## 2. Componentes preparados en la región secundaria

Todo desplegado con el **mismo código Terraform/Terragrunt** que la primaria:

- **Red**: VPC (Virtual Private Cloud), subredes privadas/públicas en varias AZ (Availability Zones),
  NAT Gateways, VPC Endpoints, Security Groups.
- **ALB** con sus target groups y listeners, y su **certificado en ACM (AWS Certificate Manager)** —
  ACM es regional, el certificado de la primaria no sirve en la secundaria.
- **ECS cluster + servicios + task definitions** apuntando a la imagen en el **ECR de la secundaria**,
  con `desired_count` reducido y **Auto Scaling** ya configurado para crecer al tamaño de producción.
- **Aurora Global Database**: clúster secundario con al menos 1 instancia (ver punto 3).
- **Bucket S3 destino** de la replicación (ver punto 4).
- **Secrets Manager con secretos replicados** a la secundaria (replica secrets) y **KMS (Key Management
  Service) multi-Region keys** para que los datos cifrados se puedan descifrar allá.
- **IAM (Identity and Access Management)**: es global, pero los roles de tarea deben referenciar los
  recursos de ambas regiones.
- **Observabilidad**: alarmas de CloudWatch, dashboards y logs **en la secundaria también** — si el
  monitoreo vive solo en la primaria, se pierde justo cuando más se necesita.
- **Service Quotas** de la secundaria revisadas (vCPU de Fargate, IPs, ALB) para soportar el 100% de la
  carga, no solo la reducida.
- WAF (Web Application Firewall) y demás reglas de borde, si existen.

## 3. Datos de Aurora

**Aurora Global Database**:

- Replicación **a nivel de almacenamiento** (no de motor) hacia la región secundaria, con lag típico
  **menor a 1 segundo** → RPO de segundos, muy por debajo de los 5 minutos.
- La primaria escribe; la secundaria es de solo lectura hasta que se promueve.
- Failover:
  - **Switchover** (planeado, para pruebas y failback): sin pérdida de datos (RPO 0).
  - **Failover gestionado / no planeado** (`failover-global-cluster --allow-data-loss`) cuando la
    primaria murió: promueve la secundaria en minutos. Se pierde solo lo que estaba en el lag.
- En **Aurora PostgreSQL** se puede fijar el parámetro `rds.global_db_rpo` para que la base
  **bloquee commits** si la secundaria se atrasa más de X segundos → garantiza el RPO a cambio de
  disponibilidad de escritura.
- Monitoreo: métricas `AuroraGlobalDBReplicationLag` y `AuroraGlobalDBRPOLag` con alarma (ej.: > 60 s).

**Global Database no protege contra errores lógicos** (un `DELETE` sin `WHERE` o un ransomware se
replica en menos de un segundo). Por eso se suma:

- **AWS Backup** con snapshots y **copia cross-region** a la secundaria, más PITR (Point-In-Time
  Recovery) habilitado.
- Idealmente un **vault de AWS Backup en otra cuenta** con Vault Lock (inmutable).

## 4. Objetos en S3

**S3 Cross-Region Replication (CRR)** hacia un bucket en la secundaria:

- Requiere **Versioning** en ambos buckets.
- Activar **S3 Replication Time Control (RTC)**: SLA (Service Level Agreement) de replicar el
  **99,99% de los objetos en 15 minutos**, y métricas `ReplicationLatency` y
  `OperationsPendingReplication`.
- **Ojo — punto clave a decir en la entrevista**: el SLA de S3 RTC es **15 minutos, no 5**. En la
  práctica la mayoría se replica en segundos, pero **AWS no garantiza contractualmente** RPO 5 min para
  S3. Por eso el enunciado dice "intentar cumplir". Mitigación: alarma si `ReplicationLatency` > 5 min,
  y para objetos críticos que la aplicación escriba en ambas regiones (o use colas para reintentar).
- Objetos que ya existían antes de la regla: **S3 Batch Replication**.
- Decidir si se replican los **delete markers** y usar **S3 Object Lock** para buckets críticos (contra
  borrados maliciosos).
- Para que la aplicación no tenga que cambiar el nombre del bucket: **S3 Multi-Region Access Points**
  con failover controls, o configurar el nombre del bucket por región vía variable de entorno.

## 5. Imágenes de ECR

- **ECR replication** (cross-region replication a nivel de registry): cada `push` en la primaria se
  copia automáticamente a la secundaria. Las imágenes anteriores a la regla no se replican → hacer un
  push inicial.
- Las task definitions de la secundaria apuntan al **ECR de su propia región** (nunca al de la
  primaria: si la región cae, el `pull` falla).
- Tags **inmutables** o desplegar por **digest** (`@sha256:...`) para garantizar que ambas regiones
  corren exactamente la misma imagen.
- Alternativa/complemento: que el pipeline de CI/CD haga push a ambas regiones.
- El pipeline de CI/CD tampoco debe depender solo de la región primaria.

## 6. DNS y cambio de región

**Route 53** (su plano de datos es global y con SLA del 100%):

- **Failover routing policy**: registro *primary* → ALB de la región A, registro *secondary* → ALB de la
  región B, con **health checks** contra un endpoint profundo (`/health` que verifique app + base de
  datos).
- **TTL (Time To Live) bajo** (60 s) para que los clientes resuelvan la nueva IP rápido.
- **Recomendación senior**: no dejar que el health check solo dispare el failover completo, porque
  Aurora necesita ser promovida antes (si el DNS cambia y la base de la secundaria sigue en solo
  lectura, la app falla igual). Mejor:
  - **Amazon Application Recovery Controller (ARC)**: *routing controls* (interruptores on/off sobre
    los registros de Route 53, operados desde el plano de datos, que funciona aunque una región esté
    caída) y **ARC Region switch** para orquestar el plan completo (promover Aurora → escalar ECS →
    cambiar DNS) como un runbook automatizado.
  - Decisión de failover **humana pero de un clic**: evita *split brain* (dos regiones creyéndose
    primarias) por un falso positivo del health check.
- Evitar operaciones del **plano de control** durante el desastre (crear/editar registros, que depende
  de `us-east-1`): todo debe estar pre-creado y solo se "voltean interruptores".

## 7. Papel de Terraform/Terragrunt

**Antes del desastre (el papel principal)**:

- Los mismos **módulos** de Terraform desplegados en ambas regiones; **Terragrunt** con una carpeta por
  región (`live/prod/us-east-1`, `live/prod/us-west-2`) que solo cambia inputs: `region`,
  `desired_count`, `is_primary`. Así se garantiza que la secundaria es idéntica (sin *drift*).
- `terragrunt run-all plan` en CI para detectar diferencias entre regiones.

**Durante el desastre: Terraform NO debe estar en el camino crítico**:

- El **state** de Terraform (backend S3 + DynamoDB de locks) suele vivir en la región primaria: si
  esa región cae, Terraform no puede leer su estado. Solución: **backend por región** (el state de la
  secundaria vive en la secundaria) o bucket de state replicado con CRR.
- El failover se ejecuta con **ARC / AWS CLI / SSM Automation**, que son rápidos y no dependen del
  state. Terraform puede usarse para escalar (`desired_count` a producción) solo si su state está
  disponible.

**Después del desastre**:

- **Reconciliar el state** (la topología de Aurora Global Database y los conteos cambiaron) y usar
  Terraform/Terragrunt para **reconstruir la región caída** como nueva secundaria y preparar el
  **failback**.

## 8. Cómo verificar técnicamente RPO y RTO

**RPO**:

- **Heartbeat / canary write**: un job escribe cada 10 s una fila `(id, timestamp)` en una tabla de
  Aurora y un objeto pequeño en S3. Tras el failover se lee el último heartbeat presente en la
  secundaria: **RPO real = momento de la caída − último timestamp replicado**.
- Continuamente: alarmas de CloudWatch sobre `AuroraGlobalDBRPOLag`, `AuroraGlobalDBReplicationLag` y
  S3 `ReplicationLatency` con umbral **por debajo** de 5 min (ej.: 60 s) para actuar antes de violar el
  objetivo.

**RTO**:

- Marcar **T0** (declaración del desastre o inicio de la prueba) y **T1** = primer éxito sostenido de
  un **CloudWatch Synthetics canary** (prueba sintética de un flujo de negocio real, ej.: login +
  consulta + escritura) contra el **dominio público**, ejecutado desde fuera de la región primaria.
- **RTO real = T1 − T0**, desglosado por paso (detección, decisión, promoción de Aurora, escalado de
  ECS, propagación de DNS) para saber dónde se va el tiempo.
- Registrar cada medición en un histórico: el RTO/RPO se demuestra con datos de pruebas, no con
  diagramas.

## 9. Pruebas periódicas del DR

"Un DR que no se prueba no existe":

1. **Tabletop mensual**: recorrer el runbook en papel con el equipo de guardia.
2. **Prueba de componentes en no-producción (mensual)**: switchover de Aurora, despliegue en la
   secundaria, failover de DNS en staging.
3. **GameDay de región completa (trimestral)**, primero en staging y luego en producción en ventana
   controlada, usando:
   - **AWS FIS (Fault Injection Service)**: inyectar fallas reales (ej.: escenario de interrupción de
     conectividad de una región, detener tareas ECS, failover de Aurora).
   - **ARC Region switch** para ejecutar y cronometrar el plan.
   - Medir RPO/RTO con el heartbeat y los canaries del punto 8.
4. **Failback probado también** (volver a la región original con switchover, RPO 0).
5. Después de cada prueba: **postmortem**, actualizar el runbook y los tiempos medidos; abrir tareas
   para cada paso que haya sido más lento de lo esperado.
6. Validación continua: alarma si la secundaria tiene drift (Terraform plan con cambios), si una imagen
   falta en ECR secundario, o si las quotas no alcanzan.

---

## Resumen de 30 segundos (para decir en voz alta)

> "Usaría **Warm Standby**: la región secundaria tiene toda la plataforma desplegada por
> Terraform/Terragrunt a escala reducida. **Aurora Global Database** da RPO de segundos, con AWS Backup
> cross-region contra errores lógicos. **S3 CRR con Replication Time Control** para los objetos —
> aclarando que su SLA es de 15 minutos, así que monitoreo la latencia contra los 5 minutos. **ECR
> replication** para las imágenes. **Route 53 failover** con health checks, controlado con **Application
> Recovery Controller** para que la promoción de Aurora, el escalado de ECS y el cambio de DNS vayan en
> orden. Terraform prepara todo antes y reconstruye después, pero no está en el camino crítico del
> failover. RPO y RTO los demuestro con heartbeats y canaries sintéticos en GameDays trimestrales con
> **AWS FIS**."
