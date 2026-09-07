# Preguntas de Entrevista — Dominio Scopes & CoSMOS
> Documento exhaustivo para evaluación de candidatos al equipo Scopes Govern.
> Cubre todo el conocimiento que un empleado del equipo debe dominar.

---

## Índice

1. [Conceptos Fundamentales del Dominio](#1-conceptos-fundamentales-del-dominio)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Ciclo de Vida de un Scope — Máquina de Estados](#3-ciclo-de-vida-de-un-scope--máquina-de-estados)
4. [Little Monster — Sistema de Jobs Asíncronos](#4-little-monster--sistema-de-jobs-asíncronos)
5. [Estrategias de Deploy](#5-estrategias-de-deploy)
6. [Instance Groups y el Proxy](#6-instance-groups-y-el-proxy)
7. [Tipologías de Infraestructura](#7-tipologías-de-infraestructura)
8. [Sharding y Segmentos](#8-sharding-y-segmentos)
9. [Autenticación y Seguridad](#9-autenticación-y-seguridad)
10. [CoSMOS — Migración Arquitectónica](#10-cosmos--migración-arquitectónica)
11. [Observabilidad y Herramientas de Diagnóstico](#11-observabilidad-y-herramientas-de-diagnóstico)
12. [Patrones de Soporte y Troubleshooting](#12-patrones-de-soporte-y-troubleshooting)
13. [Reglas SRE Irrevocables](#13-reglas-sre-irrevocables)
14. [Integraciones del Ecosistema](#14-integraciones-del-ecosistema)
15. [Escenarios Situacionales (Role-play)](#15-escenarios-situacionales-role-play)

---

## 1. Conceptos Fundamentales del Dominio

### Nivel Básico

**P1.1: ¿Qué es un Scope en el ecosistema Fury?**
> **Respuesta esperada:** Un Scope es la unidad de runtime que vincula una aplicación (servicio) con su infraestructura de cómputo, región, estrategia de despliegue y estado de ciclo de vida. Es la abstracción central del sistema: una app puede tener múltiples scopes (test, staging, prod). El scope gestiona escalado automático y determina cómo se provisionan y destruyen los recursos físicos que soportan esa aplicación.

---

**P1.2: ¿Cuál es la diferencia entre una `Application` y un `Scope`?**
> **Respuesta esperada:** Una `Application` es la entidad padre que representa el servicio de software en sí (tiene nombre, tecnología, configuración de middleware). Un `Scope` es una instancia de runtime de esa aplicación en una región y entorno específico. Una `Application` puede tener muchos `Scopes` (ej: test, staging, producción).

---

**P1.3: Explica qué es la `criticality` de un scope y para qué sirve.**
> **Respuesta esperada:** La criticality es una clasificación de importancia de negocio que determina el routing de infraestructura y la política operacional aplicada al scope. Hay 6 niveles:
> - `test`: entornos de prueba, desactivados automáticamente 2 días después del último deploy
> - `low`: cargas no críticas
> - `medium`: cargas intermedias
> - `high`: cargas productivas importantes
> - `business-critical`: servicios críticos de negocio
> - `company-critical`: servicios críticos de plataforma
>
> Los niveles `test`, `low`, `medium` van al shard `prod`; los niveles `high`, `business-critical`, `company-critical` van al shard `core` (mayor aislamiento).

---

**P1.4: ¿Qué es un `segment` en el contexto de Scopes?**
> **Respuesta esperada:** Un segment es la dimensión de segmentación física y lógica del sistema. Define límites de datos, red y cómputo. Cada segment tiene su propio SQS, Aurora MySQL, LM API, worker y Scopes API. Los problemas de un segment no afectan a otros. Ejemplos: `arg-prod`, `bra-core`, `mexbank-prod`, `legacy`. El segment se valida al crear un scope: fury-api consulta Net-API para verificar que la criticality esté permitida en ese segment.

---

**P1.5: ¿Qué es un `Instance Group` y qué relación tiene con un Scope?**
> **Respuesta esperada:** Un Instance Group (IG) es la infraestructura física o lógica que respalda a un scope. Para scopes Serverless, es un grupo de pods en Kubernetes; para Standard, es un Auto Scaling Group de EC2s. Un scope puede tener uno o más IGs activos simultáneamente (ej: durante un deploy Blue-Green hay dos: el viejo y el candidato). El IG es quien recibe el tráfico de producción.

---

**P1.6: ¿Cuáles son los dos paths de orquestación para crear un scope y cuándo se usa cada uno?**
> **Respuesta esperada:**
> - **Path SAPI (moderno):** `create_web_scope` → jobs-scopes. Se usa para Serverless y Standard modernos. Crea red, DNS, Istio e Instance Group. 27 tasks secuenciales.
> - **Path Classic/Legacy:** `create_web_service` → jobs-aws. Se usa para infraestructura off-mesh en AWS: ELB Clásico, Auto Scaling Group y EC2s. En desuso, no crear scopes nuevos de este tipo.

---

**P1.7: ¿Qué significa que `finished` no implica que el scope recibe tráfico?**
> **Respuesta esperada:** En el flujo tradicional (sin SDAPI), un scope en estado `finished` tiene infraestructura creada pero no recibe tráfico hasta que un Initial Deploy finaliza exitosamente. El deploy es quien configura los pods y registra el IG en el Service Mesh. Con SDAPI (paradigma nuevo), el scope nace 100% operativo porque acepta los parámetros de Rate Limit y artefactos en la creación misma, sin necesitar deploy posterior.

---

**P1.8: ¿Qué es SDAPI y qué problema resuelve?**
> **Respuesta esperada:** SDAPI es un paradigma de creación de scopes donde la creación acepta nativamente los parámetros de Rate Limit y la declaración de artefactos (MPIs). Permite que el scope nazca 100% operativo sin requerir un Initial Deploy posterior. Esto simplifica el flujo de creación y elimina la ventana de tiempo donde el scope existe pero no puede recibir tráfico.

---

### Nivel Intermedio

**P1.9: ¿Qué es un `shadow scope` en el contexto de la migración CoSMOS?**
> **Respuesta esperada:** Un shadow scope es un scope creado en fury-api que "sombrea" un scope real que vive en CoSMOS. Tiene toda la metadata actualizada del scope CoSMOS y está marcado para identificarse como shadow. Permite que las lecturas sigan funcionando desde fury-api mientras las escrituras son redirigidas al nuevo sistema. El shadow debe actualizarse sincrónicamente cada vez que el scope en CoSMOS cambia (via eventos).

---

**P1.10: Explica la diferencia entre `inactivating` e `inactive`.**
> **Respuesta esperada:**
> - `inactivating`: estado transitorio donde fury-api está destruyendo los recursos físicos (Instance Groups, Istio, DNS). El registro del scope en base de datos se mantiene. Es el proceso de "apagar" la infraestructura.
> - `inactive`: estado final donde el scope no tiene infraestructura física asociada. El registro existe pero sin recursos. Se puede reactivar con un `activating`.

---

**P1.11: ¿Por qué no se pueden crear scopes de tipo Classic/Legacy nuevos?**
> **Respuesta esperada:** Porque Classic desplegaba recursos nativos exclusivos por scope (ELB + ASG + EC2 propios), lo que tiene altos costos de infraestructura off-mesh y dependencia del proveedor. Además, carece de rollback automático cuando un job falla a mitad de ejecución: los recursos físicos quedan en AWS consumiendo presupuesto sin estar asociados a ningún servicio activo. El ecosistema migró a Standard y Serverless que usan infraestructura compartida y Service Mesh.

---

**P1.12: ¿Qué es el `pool_name` de un scope y cómo se genera?**
> **Respuesta esperada:** Es un identificador interno legacy del scope generado como `(service_group_name || scope_name) + "_#{SecureRandom.hex[0...6]}"`. Es un identificador único corto sin equivalente directo en CoSMOS. No confundir con `cluster_name` que representa el nombre del Instance Group (runtime).

---

## 2. Arquitectura del Sistema

### Nivel Básico

**P2.1: Describe el mapa de componentes del dominio Scopes. ¿Cuáles son los servicios más importantes?**
> **Respuesta esperada:** Los componentes clave son:
> - **fury-api** (Ruby/Rails): Orquestador principal. Valida permisos, resuelve región, enruta jobs a LM. Source of truth actual.
> - **fury-scopes-api** (Go 1.21): Gestiona Instance Groups. Shards `prod` (test/low/medium) y `core` (high+).
> - **instance-groups-proxy** (Python/FastAPI): Gateway → shard correcto por criticidad. Punto de entrada único.
> - **fury-lm-scopes-api** (Ruby): Persiste jobs en DB y publica en SNS/SQS.
> - **fury-lm-jobs-scopes** (Ruby): Worker que consume SQS y ejecuta jobs de provisionamiento.
> - **fury-lm-jobs-deploys** (Ruby): Worker de deploys mesh.
> - **fury-lm-jobs-serverless** (Ruby): Worker K8s para crear IGs.
> - **fury_serverless-api**: Compute K8s + Istio.
> - **fury-pilot**: Gestiona ciclo de vida de EC2/GCE para Standard.
> - **fury-conga-api**: Inventario de instancias sanas (heartbeats, caché Redis 1h).

---

**P2.2: ¿Qué rol cumple fury-api en la arquitectura?**
> **Respuesta esperada:** fury-api es el orquestador central y source of truth del sistema actual. Recibe requests de usuarios (via Fury Web/CLI), valida permisos (Tiger/Florida), resuelve la región y segmento de red (Net-API), y orquesta jobs hacia Little Monster. También resuelve configuraciones de sidecars, versiones de containers, parámetros de deployments, y expone las APIs que consumen otros sistemas como deployments-api y jobs-deploys.

---

**P2.3: ¿Qué es fury-conga-api y cuál es su rol?**
> **Respuesta esperada:** fury-conga-api es el inventario de instancias sanas del dominio. Las instancias (pods/EC2s) le envían heartbeats para registrar que están activas y sanas. Tiene un caché Redis de 1 hora. Es la fuente de verdad para saber qué instancias físicas están recibiendo tráfico en un momento dado. Si una instancia deja de enviar heartbeats, Conga la marca como no saludable.

---

**P2.4: ¿Qué es Configurola y para qué lo usa fury-api?**
> **Respuesta esperada:** Configurola es el servicio de configuración del ecosistema. fury-api lo usa para resolver configuraciones dinámicas según el scope: versiones de AMIs, cantidad de réplicas, configuración de sidecars, feature flags, y valores por defecto. Es especialmente importante para determinar qué versión de cada sidecar usar en función de la criticidad y región del scope.

---

**P2.5: Explica la arquitectura de enrutamiento de tráfico en Serverless vs Standard.**
> **Respuesta esperada:**
> - **Serverless (Service Mesh Completo):** Basado 100% en Istio sobre Kubernetes. No hay Nginx centralizado. El tráfico interno es Peer-to-Peer (P2P) entre pods usando el sidecar `Istio-Proxy` (Envoy), orquestado por el Control Plane de Istio. Menor latencia.
> - **Standard (Service Mesh Parcial):** `ALB compartido → Nginx compartido (routing por host/path) → Sidecar Proxy`. El balancer externo decide si envía tráfico basado en sus propios health checks. Pilot gestiona el ciclo de vida de las VMs pero NO enruta tráfico.

---

### Nivel Intermedio

**P2.6: ¿Qué es el Services Sidecar y cuál es su rol en los deploys de configuración?**
> **Respuesta esperada:** El Services Sidecar es un companion container que corre junto a la aplicación principal. Su rol en Safe Configs:
> 1. Descarga el nuevo archivo de configuración (.tar.gz) desde S3/GCP Storage.
> 2. Descomprime en ruta temporal.
> 3. Hace un swap atómico del symlink `/configs/latest` → nueva versión (operación atómica del SO, zero-downtime).
> 4. Hace POST /refresh_config al puerto interno de la app para que recargue la configuración sin reiniciar el proceso.
> Esto permite aplicar cambios de variables de entorno sin downtime ni reinicio de contenedores.

---

**P2.7: ¿Qué hace el `fury_dump-infrastructure`?**
> **Respuesta esperada:** Es el microservicio canónico para auditar la brecha entre el estado lógico de Fury y los recursos físicos reales en AWS. El LM job `dump_infrastructure` en `fury-lm-jobs-aws` invoca su endpoint `POST /run`. Barre EC2s, ALBs y ASGs en AWS, los enriquece con datos de Conga y almacena una foto en DynamoDB. Se usa especialmente para detectar infraestructura huérfana (scopes en `error_deleting` con recursos físicos aún existentes).

---

**P2.8: Explica el rol del Service Mesh en Scopes. ¿Qué componentes lo forman?**
> **Respuesta esperada:** El Service Mesh es la capa de red que controla el enrutamiento de tráfico entre servicios. Está basado en Istio y está compuesto por:
> - **VirtualService**: define las reglas de routing HTTP/gRPC (host, path, pesos).
> - **DestinationRule**: define políticas de balanceo y subsets por versión.
> - **Sidecar**: controla qué tráfico puede entrar y salir del pod.
> - **PeerAuthentication**: políticas de mTLS entre servicios.
> - **EnvoyFilter**: filtros personalizados en el proxy Envoy.
> - **ServiceEntry**: registra servicios externos al mesh.
> El job `create_web_scope` crea todos estos recursos al provisionar un scope nuevo.

---

**P2.9: ¿Qué es fury-spider y para qué sirve?**
> **Respuesta esperada:** fury-spider es el sistema de grafo de entidades de Fury (usa Neptune/openCypher). Mantiene las relaciones entre aplicaciones, scopes, usuarios, dependencias y otros recursos. Se sincroniza via RAVEN. Se usa para análisis de dependencias, impacto de cambios, y auditoría de recursos. Cuando se borra un scope, fury-api valida en fury-service-constraints que no tenga dependencias activas que lo usen.

---

**P2.10: ¿Qué es LocalAPI y qué rol cumple?**
> **Respuesta esperada:** fury-localapi es el agente que corre en cada instancia EC2 en el puerto 8090. Ejecuta comandos (como instalar y arrancar la aplicación via docker-compose) y envía heartbeats a Conga para registrar la salud de la instancia. Es el punto de control de Fury sobre cada VM de Standard. El provisioner genera el `docker-compose.yml` que LocalAPI descarga desde S3 para arrancar la aplicación.

---

### Nivel Avanzado

**P2.11: ¿Cómo resuelve fury-api la configuración por región? Explica el patrón `configs_as_hash`.**
> **Respuesta esperada:** fury-api tiene un modelo `Region` con subclases STI (AwsRegion, GcpRegion, AwsSingleRegion). Cada región tiene muchos `RegionConfig` (key-value store): URLs de servicios, versiones de sidecars por criticidad, namespaces, tags de containers, etc. El método `configs_as_hash` convierte estos registros a un hash con symbol keys, que se accede como `application_region.region.configs_as_hash[:PILOT_URL]`. Esto permite que fury-api resuelva valores específicos de infra (versión de sidecar-proxy, URL de Serverless API, namespace K8s) dependiendo de la región y criticidad del scope.

---

**P2.12: Explica la jerarquía STI de modelos de Service en fury-api. ¿Por qué importa para el adapter de CoSMOS?**
> **Respuesta esperada:** fury-api usa Single Table Inheritance (STI) donde todos los scopes comparten la tabla `services` pero tienen clases Ruby distintas:
>
> ```
> Service (base)
> └── ComputingService
>     ├── InfrastructureService (EC2: instance_type, memory, spot)
>     │   └── WebService (scope web Standard)
>     └── ServerlessApplicationService (sin instance_type)
>         └── WebServerlessApplicationService (scope web Serverless)
> ```
>
> Para el adapter de CoSMOS esto importa porque cada clase agrega campos distintos a la metadata. El adapter debe conocer qué campos pertenecen a qué clase para mapear correctamente a CoSMOS. Por ejemplo, `InfrastructureService` tiene `instance_type`, `memory`, `spot_percentage` que no existen en `ServerlessApplicationService`.

---

## 3. Ciclo de Vida de un Scope — Máquina de Estados

### Nivel Básico

**P3.1: Enumera todos los estados posibles de un scope y describe brevemente cada uno.**
> **Respuesta esperada:**
> - `creating`: infraestructura siendo provisionada.
> - `finished`: infraestructura activa. Con SDAPI el scope nace 100% operativo; sin él, requiere Initial Deploy.
> - `running`: estado legacy/deprecated. Indica pods activos en scopes Serverless con `scale_to_zero`. No debe aparecer en operación normal.
> - `error`: fallo durante creación o actualización.
> - `updating`: modificación de configuración en curso.
> - `inactivating`: destrucción de recursos físicos (el registro del scope se mantiene).
> - `error_inactivating`: fallo durante la desactivación. Única salida: reintentar.
> - `inactive`: sin infraestructura. Registro existente pero sin recursos.
> - `activating`: reasignación de infraestructura física a un scope inactivo.
> - `deleting`: borrado total del scope y sus recursos.
> - `error_deleting`: fallo durante el borrado. Única salida: reintentar.
> - `deleted`: scope eliminado permanentemente.

---

**P3.2: ¿Cuáles son las transiciones válidas desde el estado `error`?**
> **Respuesta esperada:**
> - `error → updating` (para rescue: forzar con `triggers_jobs: false`)
> - `error → deleting` (DELETE /scopes)
>
> NO hay transición directa `error → inactivating` para scopes productivos. Esta es la regla SRE más crítica.

---

**P3.3: Un scope está en `error`. ¿Cuál es el procedimiento correcto de rescue?**
> **Respuesta esperada:**
> 1. Verificar precondiciones:
>    - ¿Hay job activo en LM para este scope? Si sí, esperar o cancelar primero.
>    - ¿La infra física existe en AWS/K8s? Confirmar con MCP o scopes-api.
>    - ¿El scope tiene tráfico activo?
>    - ¿El error fue en creación o actualización?
>    - ¿La criticality es productiva?
> 2. PUT `{ "status": "updating", "triggers_jobs": false }` → scope pasa a `updating`.
> 3. Si la infra está estable: PUT `{ "status": "finished", "triggers_jobs": false }` → scope operativo.
> 4. Solicitar al usuario que lance un nuevo deployment para validar el estado real.
> 5. Si falla de nuevo: scope vuelve a `error` → evaluar borrado.

---

**P3.4: ¿Cómo se reactiva un scope `inactive`?**
> **Respuesta esperada:** Dos formas:
> - `PUT /applications/{app}/scopes/{scope}` con `{ "status": "activating" }`.
> - `POST /applications/{app}/scopes/{scope}/recreate`.
>
> Ambas funcionan igual que `creating`: reasignan infraestructura física. `on_success` → `finished`.

---

**P3.5: ¿Qué pasa automáticamente con los scopes de criticality `test`?**
> **Respuesta esperada:** Los scopes web con criticidad `test` son desactivados automáticamente dos días después de su último despliegue. Pasan a `inactivating` → `inactive`. Esto es parte de la política de optimización de costos del equipo.

---

### Nivel Intermedio

**P3.6: ¿Qué es el estado `running` y por qué es problemático?**
> **Respuesta esperada:** El estado `running` es un estado legacy/deprecated. Aparece cuando un usuario ejecutó `PUT {"status": "running"}` directamente desde un scope en `inactive`. No es una transición válida del sistema. Desde PR #5086, fury-api rechaza este intento con 422 para tipos scopeable (`InfrastructureService`, `ServerlessApplicationService` y sus hijos).
>
> Es problemático porque el scope queda atascado: no puede inactivarse (`"cannot inactivate a service with status running"`), no puede hacer Blue-Green. El rescue path es `running → updating → finished` (no es posible `running → finished` directo porque falla con `"cannot finish a service with status running"`).

---

**P3.7: Describe dos scenarios distintos de scope stuck en `deleting` y cómo resolverlos.**
> **Respuesta esperada:**
>
> **Caso A — Scope con infra real (cluster_name presente):**
> El job de borrado falló. No forzar `deleted` directamente porque la infra aún existe y saltarse el job dejaría recursos huérfanos. Solución: forzar a `error_deleting` → el usuario reintenta el delete desde la UI → fury-api encola nuevo job de borrado.
> ```bash
> PUT /scopes/{scope} {"status": "error_deleting", "triggers_jobs": false}
> ```
>
> **Caso B — Scope sin infra (`cluster_name: null`):**
> `validate_deletion` en `computing_service.rb` permite `deleting → deleted` cuando `status_was == 'deleting'`. Se puede forzar directamente a `deleted`, lo que dispara `before_update :destroy!` y elimina el registro de BD sin tocar infra.
> ```bash
> PUT /scopes/{scope} {"status": "deleted", "triggers_jobs": false}
> ```

---

**P3.8: Explica el escenario de "initial deploy fallido" y por qué no se debe usar `finished` como estado destino.**
> **Respuesta esperada:** Si el scope cae en `error` durante un initial deploy (nunca completó su primera creación), el rescue no debe usar `finished` como destino porque deja al scope aparentando ser operativo cuando nunca lo fue. Otros sistemas podrían intentar hacer Blue-Green sobre un scope sin initial completo, causando errores en cascada.
>
> El path correcto es: `error → updating → creating` (ambos con `triggers_jobs: false`) → usuario reintenta rollback → scope transiciona a `inactivating → inactive`. Si el scope nunca tuvo tráfico real, es seguro destruir la infra.

---

**P3.9: ¿En qué situaciones el job `delete_web_scope` maneja la transición de estado diferente?**
> **Respuesta esperada:** El job `delete_web_scope` evalúa el estado original del scope al momento de lanzarse para determinar la transición en `on_success` y `on_error`:
> - Si el scope venía de `inactivating` → `on_success` actualiza a `inactive`, `on_error` actualiza a `error_inactivating`.
> - Si el scope venía de `deleting` → `on_success` actualiza a `deleted`, `on_error` actualiza a `error_deleting`.
>
> Ambos estados disparan el mismo job pero con consecuencias distintas.

---

**P3.10: ¿Cuáles son los estados terminales de error de los que no hay rescue posible sin reintentar la operación fallida?**
> **Respuesta esperada:** `error_deleting` y `error_inactivating`. Desde estos estados no hay transición de rescue — solo se puede reintentar la operación que falló (reintentar el delete o el inactivate). No se debe intentar forzar otros estados desde aquí.

---

## 4. Little Monster — Sistema de Jobs Asíncronos

### Nivel Básico

**P4.1: ¿Qué es Little Monster (LM)?**
> **Respuesta esperada:** Little Monster (LM) es el framework de orquestación asíncrona de Fury. Ejecuta jobs compuestos por tasks secuenciales sobre una arquitectura de mensajería SNS → SQS. Los jobs son idempotentes: si una task falla y se reintenta, no genera recursos duplicados. Las tasks comparten estado vía `data[:key]`.

---

**P4.2: Explica la diferencia entre `lm-scopes-api` (LM Scopes API) y `lm-api` (LM API estándar).**
> **Respuesta esperada:**
> - **LM Scopes API** (`fury-lm-scopes-api`): variante especializada usada por fury-api (path SAPI) y fury-scopes-api. Tiene infraestructura propia por segmento (`fury-lm-scopes-api-arg-prod`, etc.). Endpoint: `LITTLE_MONSTER_SCOPES_URL`.
> - **LM API estándar** (`fury-little_monster-api`): variante legacy usada por fury-api (path Classic). Endpoint: `LITTLE_MONSTER_URL`.
>
> Cada una tiene sus propias colas SQS y base de datos, garantizando aislamiento entre paths.

---

**P4.3: ¿Cuáles son los tres repos de workers de LM y qué jobs ejecuta cada uno?**
> **Respuesta esperada:**
> - **`fury-little_monster-jobs-scopes`**: Scopes modernos (Serverless/Standard vía SAPI). Jobs: `create_web_scope`, `delete_web_scope`, `create_instance_group`, `delete_instance_group`, `rolling_update_prepare`, jobs CoSMOS.
> - **`fury-little_monster-jobs-deploys`**: Deploy mesh (Standard + Serverless). Jobs: `do_scopes_api_blue_green_deploy`, `do_initial_deploy`, etc.
> - **`fury-little_monster-jobs-aws`**: Off-mesh/Classic Legacy AWS. Jobs: `create_web_service`, `dump_infrastructure`, VPC, ASGs clásicos.

---

**P4.4: ¿Cuál es el riesgo operativo más crítico de LM relacionado con la publicación de jobs?**
> **Respuesta esperada:** La ausencia de Dead Letter Queue (DLQ). Al encolar un job, si el framework no logra publicar el mensaje en SNS/PubSub tras 3 reintentos (ej: por throttling de AWS), el job se elimina permanentemente de la base de datos. No existe DLQ que lo retenga.
>
> Síntoma: scope queda atascado en `creating` y no hay rastro del job en el backoffice. El scope debe ser rescatado manualmente. Este es el primer punto a verificar ante un scope stuck en `creating` sin job visible.

---

**P4.5: ¿Qué son los heartbeats en LM y qué pasa cuando un worker falla durante un job?**
> **Respuesta esperada:** Cuando un worker consume un mensaje de SQS, reclama el job con un PUT que registra host + PID. Mientras el job corre, el worker envía heartbeats periódicos para mantener el lock. Si el worker muere (crash, OOM, restart) y no envía su heartbeat, el sistema libera el lock automáticamente al pasar el umbral de unlock de la variante.
>
> Un job sin heartbeat vuelve a estado `pending` sin lock activo → otro worker puede reclamarlo. Síntoma de diagnóstico: job aparece como `running` en backoffice pero no avanza. Verificar si el worker que lo tomó sigue vivo.

---

### Nivel Intermedio

**P4.6: ¿Cuáles son los umbrales de unlock por variante de LM y qué implican para el troubleshooting?**
> **Respuesta esperada:**
> - `deployments_critical_production`: 30 segundos de unlock, 15 días de expiración del job.
> - `scopes_production`: 120 segundos de unlock, 2 meses de expiración.
> - `serverless_production`: 120 segundos de unlock, 2 meses de expiración.
>
> Implicación: si un worker de deployments tarda más de 30s sin heartbeat, otro worker puede reclamar el job. Dos workers reclamando el mismo job simultáneamente chocan con el error `"The job is already running"`. Para scopes, el unlock es más permisivo (120s).

---

**P4.7: Explica las 27 tasks del job `create_web_scope`. ¿Qué hace el sub-job `CreateInstanceGroup` dentro de él?**
> **Respuesta esperada:** El job `create_web_scope` provisiona toda la red, Service Mesh e Istio para un scope moderno. Las primeras tasks crean: VIP, DNS, Istio namespace, ServiceEntry, DestinationRule, VirtualScope, VirtualService (dos), Sidecar, PeerAuthentication, EnvoyFilter, refresh traffic catalog, registración en CA, Config Service, configuración en Conga, MySQL proxy, Initial Artifacts, refresh routes, Egress Metadata, esperas de registro.
>
> En la task 24, el job **pausa su ejecución y llama síncronamente** al sub-job `CreateInstanceGroup` sin encolar un nuevo mensaje en LM. Este sub-job: obtiene Kairos DNS, crea target group, obtiene tokens de seguridad, obtiene config, sube docker-compose a S3, genera metadata URL, sube metadata, crea el IG en Serverless API o Pilot API, crea DestinationRule (reordenado después del provider para garantizar que el IG ya existe), notifica rate limit, espera configuración de rate limit.

---

**P4.8: ¿Qué pasa en el `on_error` del job `create_web_scope`?**
> **Respuesta esperada:** El `on_error` transiciona el scope a `inactivating` con descripción `"inactivated scope because creation job failed"`. Esto es seguro porque el scope es nuevo y no tiene tráfico real. Al inactivar, se lanza `delete_web_scope` para limpiar los recursos parcialmente creados.

---

**P4.9: ¿Cuál es el riesgo específico de las variantes `scopes_production` y `serverless_production` que NO tienen staging?**
> **Respuesta esperada:** Cualquier cambio en `fury-little_monster-jobs-scopes` impacta directamente la orquestación productiva de todos los scopes sin pasar por un entorno de staging que filtre errores. Si un bug entra en producción, afecta todos los jobs de creación/borrado/actualización de scopes en tiempo real. Esto exige extremo cuidado en el testing previo al deploy y un monitoreo activo post-release.

---

**P4.10: ¿Por qué el error real cuando falla una task `create_instance_group` en jobs-deploys está en LM Scopes, no en jobs-deploys?**
> **Respuesta esperada:** Porque la task `create_instance_group` en jobs-deploys hace un POST a scopes-api, que registra un nuevo job `CreateInstanceGroup` en LM Scopes y retorna `202 Accepted`. Jobs-deploys no ejecuta la lógica de creación: solo la dispara. La task `verify_instance_group_create_status` luego hace polling al IG hasta que llega a `active`. Si el sub-job de LM Scopes falla internamente, el IG nunca llega a `active` y el timeout de polling da `DeploymentFilesPreparationTimeout` — que es el síntoma, no la causa.
>
> Regla: el job de jobs-deploys muestra el síntoma; el sub-job de LM Scopes muestra la causa.

---

**P4.11: Describe el job `DoConfigRollingUpdateDeploy` (Safe Configs). ¿Por qué pausa el autoscaling?**
> **Respuesta esperada:** Es el job que se ejecuta cuando solo cambian variables de entorno (sin cambio de código). En lugar de crear un cluster candidato (como Blue-Green), opera sobre las instancias existentes. Ejecuta un Rolling Update por bloques:
> 1. Pausa el Auto Scaling Group para evitar que la nube cree o destruya instancias inconsistentes durante la propagación.
> 2. Aplica la configuración en lotes (swap_block_size) a través del Services Sidecar.
> 3. Reanuda el autoscaling al finalizar.
>
> Si una nueva instancia arrancara durante el rolling update, nacería con la configuración vieja mientras otras ya tienen la nueva, creando estado inconsistente en producción. Por eso es crítico pausar el ASG.

---

**P4.12: ¿Cómo se diferencia el tipo de registro DNS según el segmento en el job `delete_web_scope`?**
> **Respuesta esperada:** La task `delete_dns` en `delete_web_scope` diferencia el tipo de registro DNS por segmento. Segmentos `legacy` y `default` usan registros **A** (`route_53_client.delete_dns`); otros segmentos usan **CNAME** (`route_53_client.delete_cname_dns`). La lógica usa `record_type`: `%w[legacy default].include?(segment) ? 'A' : 'CNAME'`. Si una eliminación DNS falla, verificar que el tipo de registro coincida con el segmento del scope.

---

**P4.13: ¿Cómo buscarías un job de LM Scopes si no conoces su ID?**
> **Respuesta esperada:** El UUID de un job sigue el patrón `<operacion>_<scope-name>_<segmento>.<app-name>.t<timestamp>`. Para buscarlo:
> 1. Determinar el cluster correcto según segment + criticality del scope (ver tabla de segmentos).
> 2. Usar `GET /jobs?uuid_search=create_{candidate_cluster_name}` en el host del LM correcto.
> 3. Ojo: `total_count` en la respuesta siempre devuelve 0 aunque haya resultados. Siempre iterar sobre `jobs[]`.
> 4. Para búsquedas históricas (días atrás), usar el script `search_ig_jobs.sh` que hace binary search adaptativo — `uuid_search` directo hace timeout en clusters con mucha historia.

---

## 5. Estrategias de Deploy

### Nivel Básico

**P5.1: ¿Cuáles son las principales estrategias de deploy en Fury Scopes?**
> **Respuesta esperada:**
> - **Blue-Green**: crea un cluster candidato paralelo, hace swap progresivo de tráfico, destruye el viejo. Rollback automático en caso de error.
> - **Canary**: variante de Blue-Green donde el tráfico se mueve porcentualmente (ej: 10% → 50% → 100%).
> - **Rolling Update**: actualiza instancias en lotes dentro del mismo cluster (Safe Configs).
> - **Deploy de Migración**: similar a Blue-Green pero a nivel de scope completo. Crea un scope temporal (`-tmp`) y hace swap del scope entero.
> - **Initial Deploy**: primer deploy de un scope recién creado (sin SDAPI).

---

**P5.2: Explica la diferencia fundamental entre Blue-Green estándar y un Deploy de Migración.**
> **Respuesta esperada:**
> - **Blue-Green estándar**: opera dentro del mismo scope. Crea un cluster candidato nuevo dentro del mismo scope. Al finalizar, destruye el cluster viejo.
> - **Deploy de Migración**: opera a nivel de scope. Se crea un scope temporal completo con sufijo `-tmp` o `-svpc`. Ejecuta el Initial Deploy en el scope temporal, hace swap del scope entero (incluida la red y el DNS), y al finalizar destruye el scope viejo y renombra el temporal al nombre definitivo.
>
> Cuándo se usa migración: cambio de infra profundo (Pilot→Serverless, GCP→AWS, salida de Single VPC).

---

**P5.3: ¿Qué es el Rollback Recommendation y cómo funciona?**
> **Respuesta esperada:** Durante el swap de tráfico en Blue-Green/Canary, el sistema monitorea alertas de Datadog. Si se disparan alertas (ej: aumento de errores 5xx, caída de métricas core):
> 1. El estado del deploy cambia a `warning`.
> 2. Se genera una Recomendación de Rollback notificada vía Slack/Opsgenie.
> 3. El deploy entra en un grace period (`ROLLBACK_RECOMMENDATION_WAIT_MINUTES`).
> 4. El usuario puede ignorar (falso positivo, el deploy continúa) o cancelar (rollback inmediato).
> 5. Si el grace period expira sin intervención, el orquestador ejecuta el rollback automáticamente.
>
> Si un deploy productivo "se cancela solo", buscar las alertas de Datadog activas en ese momento — es la causa más común.

---

**P5.4: ¿Qué es la bifurcación "Deployments Directo" vs "Jobs ScopesApi" y por qué importa para diagnóstico?**
> **Respuesta esperada:**
> - **Jobs Tradicionales (Deployments Directo)**: la task `CreateCluster` llama directamente a Pilot API o Serverless API. Los logs del error están en el job de deploy.
> - **Jobs ScopesApi**: llaman a Scopes API, que encola el mandato a workers `jobs-scopes` (ej. `CreateInstanceGroup`). Los logs del error están en el sub-job `CreateInstanceGroup` en LM Scopes, no en el job de deploy.
>
> Para diagnóstico: si el deploy falla en creación de infra, determinar qué path se usó antes de buscar logs.

---

### Nivel Intermedio

**P5.5: ¿Cómo se inyectan las configuraciones en las instancias EC2 durante un Blue-Green?**
> **Respuesta esperada:** Las configuraciones se inyectan estáticamente en el `user_data` de las instancias EC2 al momento de arrancar. No hay actualización de variables en caliente. El cluster candidato nace ya con la configuración correcta.
>
> El job `DoBlueGreenDeploy` detecta si hubo cambio de configuración:
> - Sin cambio de config: salta la descarga y copia la configuración actual al cluster candidato.
> - Con cambio de config: descarga el tarball desde S3 e inyecta la nueva configuración estáticamente en el `user_data`.

---

**P5.6: ¿Dónde están los logs de un deploy fallido y cómo accedo a ellos?**
> **Respuesta esperada:** Los logs están en dos lugares distintos:
> - **Application logs** (uWSGI / app stdout): errores de la app, startup, model loading. Se accede vía `o11y-mcp → query_logs(application=<app>, scope=<scope>)`.
> - **Fury/localapi logs** (docker, pull, compose): `docker-compose up`, `COMPOSE_HTTP_TIMEOUT`, pull progress. Solo disponibles en Grafana Deployments Dashboard v2. **No están en o11y-mcp.**
>
> Para compartir logs con on-call externo, siempre incluir el export del panel "All logs" de Grafana del deploy fallido.

---

**P5.7: ¿Qué es la política `deny_service_with_vulnerability` y cuándo bloquea un deploy?**
> **Respuesta esperada:** Es una política de seguridad que rechaza un deploy si el servicio contiene dependencias vulnerables (CVEs) no parcheadas. El deploy no llega a crear infraestructura — es bloqueado antes. El ciclo de vida de un CVE es: OSS reporta CVE → IssueModeration clasifica → AdvisingSlack notifica → Dev parchea → Initial Deploy/CreateVersion genera evento `LK_DC_AUDIT_SCOPE` → Fury Lake verifica si fue limpiada.
>
> Si un deploy falla por este motivo, el equipo de desarrollo debe actualizar las dependencias afectadas antes de volver a deployar.

---

**P5.8: Describe el job `rollback_serverless_migration_deploy` y su bug conocido.**
> **Respuesta esperada:** Es el job de rollback para estrategias `gcp_migration`/`aws_migration`. Tiene 16 tasks en orden: format_job_data, get_service_group, fetch_migrated_service, wait_initial_deploy, rollback_current_jobs, unpause_kairos_current_cluster, restore_old_service_traffic, remove_migrated_service_traffic, unpause_current_cluster, set_initial_deploy_to_rollbacked, **delete_migrated_service**, update_old_service_destination_rule, update_istio_virtual_scope_delete_candidate, convert_from_service_group, refresh_traffic_routes_virtual_service, update_istio_destination_rule_delete_candidate.
>
> **Bug conocido en task [10] `delete_migrated_service`**: envía el delete a la región SOURCE en lugar de la región DEST. El job completa en `success` pero los IGs en la región DEST quedan huérfanos. Se detecta con `bash .claude/scripts/get_migration_orphans.sh {app} {scope} {dest_prefix}`.

---

## 6. Instance Groups y el Proxy

### Nivel Básico

**P6.1: ¿Qué es el Instance Groups Proxy y por qué es necesario?**
> **Respuesta esperada:** El Instance Groups Proxy (Python/FastAPI) es el único punto de entrada a fury-scopes-api. Los clientes nunca hablan directamente con los shards de Scopes API. El Proxy actúa como guardián y enrutador:
> - Recibe la petición.
> - Inspecciona la criticidad (en cascada: `body.criticality` → `body.metadata.criticality` → `body.labels.criticality` → `body.envs.SCOPE_CRITICALITY`).
> - Enruta al shard correcto (prod para test/low/medium, core para high+).
>
> Es necesario para reducir el blast radius: los shards de API de scopes están físicamente separados por criticidad. El Proxy abstrae esta topología.

---

**P6.2: ¿Qué sucede cuando el Proxy no sabe en qué shard vive un Instance Group (en GET/PUT/DELETE)?**
> **Respuesta esperada:** El Proxy dispara búsquedas en paralelo contra todos los backends (multiplexado). La primera respuesta exitosa se usa. Si el mismo IG existe en más de un shard (dato inconsistente), el Proxy devuelve un `500 Multiple Responses` — indicador de corrupción de datos entre shards. El Proxy no puede resolver el duplicado por sí solo: hay que operar directamente sobre el shard.

---

**P6.3: ¿Cuánto dura el caché de DNS rules del Proxy y qué implica para operaciones?**
> **Respuesta esperada:** El Proxy mantiene un caché en memoria de las DNS rules con TTL de 5 minutos, refrescado desde el Config Service (melitk-config). Esto implica que si hay un cambio en la configuración de backends, puede tardar hasta 5 minutos en propagarse. Ante un 404 inesperado en el Proxy, verificar si el caché está actualizado antes de concluir que el IG no existe.

---

**P6.4: ¿Qué es `hardDelete=true` en el endpoint DELETE de scopes-api y cuándo se usa?**
> **Respuesta esperada:** `hardDelete=true` borra el registro directamente desde la DB de scopes-api sin crear un job LM de teardown gradual. Se usa cuando el IG no tiene infraestructura activa (es un registro DB huérfano de un cluster tag viejo). Sin `hardDelete`, el DELETE normal crea un job LM de borrado que intenta eliminar instancias EC2/pods que ya no existen.
>
> **Permiso requerido**: el token debe tener autorización Florida `instance-groups:hard-destroy`. Sin este permiso responde `401 "hard delete not authorized"`.

---

### Nivel Intermedio

**P6.5: ¿Cómo se resuelve un error `500 Multiple Responses` del Proxy?**
> **Respuesta esperada:**
> 1. Identificar en qué shard(s) está el duplicado: consultar cada shard directamente por criticidad del scope.
> 2. Determinar cuál es el IG válido (el que tiene tráfico real) y cuál es el zombie (registro de cluster tag viejo sin tráfico).
> 3. Eliminar el IG zombie con `hardDelete=true` directamente en el shard (bypasseando el Proxy).
> 4. Verificar: reintentar la operación original vía Proxy. Sin el duplicado, puede enrutar correctamente.
>
> El Proxy no puede resolver el duplicado por sí solo porque cualquier operación vía Proxy seguirá fallando.

---

**P6.6: Explica el rol del Proxy en la arquitectura Serverless. ¿Qué hace el endpoint `choose-serverless-cluster`?**
> **Respuesta esperada:** En Serverless, la infraestructura está shardeada físicamente por criticidad en distintos clusters de Kubernetes. Antes del Proxy, los clientes debían tener configuradas múltiples URLs y aplicar lógica condicional (una URL por criticidad). Con el Proxy habilitado, el cliente usa una única URL centralizada.
>
> El endpoint `GET /{api_version}/tasks/choose-serverless-cluster?criticality={criticality}` devuelve el cluster de Kubernetes más adecuado para un workload según su criticidad. Es llamado por `jobs-scopes` antes de crear un pod para saber en qué cluster físico inyectarlo.

---

**P6.7: ¿Cómo se consulta el IG productivo real de un scope para confirmar que recibe tráfico?**
> **Respuesta esperada:** Se consulta ControlPlane via:
> ```
> GET /destination_rules?service={lb_id}
> # donde lb_id = {scope}.{app}.melifrontends.com
> ```
> La respuesta contiene las reglas de routing con porcentajes. Un `target_group` con `percentage > 0` es el IG productivo real que recibe tráfico. Si hay más de una regla con porcentaje > 0, hay un deploy en progreso (Canary/BG).
>
> Si `fury_cluster_name` ≠ `target_group` con `percentage > 0` → el promote de la migración quedó incompleto: fury-api actualizó su registro pero ControlPlane sigue sirviendo el IG anterior.

---

**P6.8: ¿Cómo se forma el header `region` para consultas al `serverless-global-proxy`?**
> **Respuesta esperada:** El header tiene el formato `{region}.{vendor}.{segment}.{tier}`:
> - `region`: de `assets.region.name`, sin sufijo Fury (ej: `us-east-1-single` → `us-east-1`).
> - `vendor`: de `assets.region.vendor` en minúscula (`aws` o `gcp`).
> - `segment`: de `metadata.segment` del scope.
> - `tier`: criticality mapeada: `test→test`, `low/medium→medium`, `high/bu-critical/meli-critical→critical`.
>
> Normalización: AWS strip sufijos Fury; GCP strip `-gcp` y el guión antes del dígito (`us-east-4-gcp` → `us-east4`).

---

## 7. Tipologías de Infraestructura

### Nivel Básico

**P7.1: ¿Cuáles son las tres tipologías de infraestructura de Scopes? Describe brevemente cada una.**
> **Respuesta esperada:**
> - **Classic/Legacy (AWS)**: recursos nativos exclusivos por scope (ELB + ASG + EC2). En desuso, no crear nuevos. Sin rollback automático ante falla.
> - **Standard (Pilot)**: instancias EC2 (AWS) o GCE (GCP) compartiendo el Traffic Layer central. Infraestructura dedicada con valores de hardware fijos. Gestionado por Pilot API. En producción pero siendo migrado a Serverless.
> - **Serverless (Kubernetes)**: pods de Kubernetes con Service Mesh local (Istio Ingress/Sidecars). Recursos dinámicos. Beneficios: menor latencia, Scale to Zero, Node Affinities. Tipo recomendado para scopes nuevos.

---

**P7.2: ¿Qué hace Pilot y qué NO hace?**
> **Respuesta esperada:**
> - **Hace**: gestiona el ciclo de vida de las VMs (EC2/GCE): creación, escalado, salud, terminación. Trackea los instance groups de Standard.
> - **NO hace**: enrutar tráfico. El enrutamiento en Standard es responsabilidad del ALB compartido + Nginx compartido. Pilot solo gestiona el ciclo de vida de las máquinas.

---

**P7.3: ¿Qué es un scope en Single VPC y cómo se identifica?**
> **Respuesta esperada:** Los scopes en Single VPC corren en una VPC de AWS dedicada, aislada del pool compartido de Fury. Se identifica porque el `application_region` tiene `type: AwsSingleApplicationRegion`. Para confirmar:
> 1. GET de la aplicación via MCP → leer `application_regions[]`.
> 2. Verificar si el `type == "AwsSingleApplicationRegion"`.
> 3. Para el VPC exacto: leer `application_region.vpc.external_id` (no usar `vpc.id` ni `vpc.name` — pueden haber múltiples registros internos apuntando al mismo AWS VPC).

---

### Nivel Intermedio

**P7.4: Describe el riesgo de infraestructura huérfana en Classic y cómo detectarla.**
> **Respuesta esperada:** En Classic, si un job (`CreateWebService`, `DoWebServiceInitialDeploy`) falla a mitad de ejecución, los recursos físicos quedan vivos en AWS sin asociarse a ningún servicio activo:
> - `CreateWebService` falla en `create_config_service` → ELB Clásico + registro DNS en Route53 huérfanos.
> - `DoWebServiceInitialDeploy` falla en `wait_instances_signals` → ASG lleno de EC2s que no sirven tráfico.
>
> Detección: invocar `fury_dump-infrastructure` (LM job `dump_infrastructure`) que barre EC2s, ALBs y ASGs en AWS, enriquece con Conga y almacena en DynamoDB. Cruzar scopes en `error_deleting` contra ALBs existentes en DynamoDB.

---

**P7.5: ¿Cómo se comportan las Node Affinities en Kubernetes para scopes Serverless?**
> **Respuesta esperada:** Kubernetes abstrae el hardware, pero los pods corren sobre nodos físicos reales. Cuando se crea un scope con `arch: arm64`, Fury traduce este campo en reglas de Node Affinity nativas de K8s, forzando al scheduler a desplegar los pods exclusivamente en nodos con procesadores ARM. Lo mismo aplica para `amd64`, `spot` y `workload_type`. Esto se configura en el JSON Spec que jobs-scopes envía a la Serverless API durante la task `create_instance_group_on_provider`.

---

**P7.6: Describe el patrón general de una migración entre tipologías de infraestructura.**
> **Respuesta esperada:**
> 1. Levantar un cluster candidato en paralelo con la infraestructura existente.
> 2. Swap progresivo de tráfico hacia el nuevo cluster.
> 3. `on_success`: destruir infraestructura vieja.
> 4. `on_failure`: rollback automático a la infraestructura original.
>
> Durante la migración existen dos conjuntos de infraestructura simultáneos. Una intervención manual en este estado puede afectar tráfico productivo. Verificar siempre el estado en state-machine.md antes de actuar.
>
> Migraciones soportadas: Standard→Serverless, GCP→AWS, Classic→Standard o Serverless.

---

## 8. Sharding y Segmentos

### Nivel Básico

**P8.1: ¿Cuántos segmentos existen y cuáles son sus características?**
> **Respuesta esperada:** Los principales segmentos son:
> - `arg` (Argentina): clusters LM `Scopes-arg-prod` y `Scopes-arg-core`.
> - `bra` (Brasil): `Scopes-bra-prod` y `Scopes-bra-core`.
> - `col` (Colombia): `Scopes-col-prod` y `Scopes-col-core`.
> - `mex` (México, excl. banco): `Scopes-mex-prod` y `Scopes-mex-core`.
> - `rla` (Rest of Latam): `Scopes-rla-prod` y `Scopes-rla-core`.
> - `mexbank` (México bancario): incluye `nonprod`.
> - `npmexbank` / `npmexfinn`: solo dev.
> - `nonsite`: recursos sin fragmentación por sitio (CBT, labs).
> - `platform`: infraestructura de plataforma.
> - `legacy`: transitorio durante migración a segmentación. Tiene 3 shards por criticidad.
> - `nonprod`: todos los entornos no productivos.
>
> Cada segmento tiene SQS + Aurora MySQL propios. No hay estado compartido entre segmentos.

---

**P8.2: ¿Cuáles son los dos shards de Scopes API por criticidad y qué criticidades atiende cada uno?**
> **Respuesta esperada:**
> - **Shard Prod** (`fury-scopes-api-{segment}-prod`): atiende `test`, `low`, `medium`.
> - **Shard Core** (`fury-scopes-api-{segment}-core`): atiende `high`, `business-critical`, `company-critical`.
>
> Esta separación física reduce el blast radius: un problema en el shard `prod` (baja criticidad) no afecta al shard `core` (alta criticidad) y viceversa.

---

**P8.3: Si tienes un scope con segment `legacy` y criticality `low`, ¿en qué host de LM Scopes buscarías su job?**
> **Respuesta esperada:** Post-rollout 2026-04-21, el host correcto es `https://us-east-1-aws-lm-scopes-prod.furycloud.io` (cluster `scopes-prod`). Como fallback, si no aparece, buscar en `https://us-east-1-aws-lm-scopes.furycloud.io` (cluster `scopes-aws`) porque puede haber sido creado antes del rollout.

---

**P8.4: ¿Cómo se deriva el host de LM Scopes para un segmento que solo tiene el código de país (sin `-prod`/`-core`)?**
> **Respuesta esperada:** Resolver según criticidad: `high`/`bu-critical`/`cc` → `-core`, resto → `-prod`. Ejemplo: `bra` + criticality `low` → `bra-prod` → host `https://us-east-1-aws-lm-scopes-bra-prod.furycloud.io`.

---

## 9. Autenticación y Seguridad

### Nivel Básico

**P9.1: ¿Qué es Tiger API y cómo se usa para autenticar llamadas al ecosistema?**
> **Respuesta esperada:** Tiger API es el emisor de tokens JWT del ecosistema Fury. Todas las llamadas a APIs requieren autenticación via Tiger.
> - **Tiger Token** (usuario interactivo): `X-Tiger-Token: $(fury get-token)`. Para llamadas manuales desde CLI o scripts.
> - **JWT Bearer** (estándar): `Authorization: Bearer <token>`. Para clientes de servicio modernos.
> - **Fury Token** (legacy): `X-Fury-Token: <token>`. Para Local API y sistemas legacy.
>
> Detalles técnicos: algoritmo RS256, validación local de JWKS cacheada en memoria o Redis ~60 minutos.

---

**P9.2: ¿Cuál es la diferencia entre Tiger y Florida?**
> **Respuesta esperada:**
> - **Tiger**: autenticación (¿quién sos?). Emite tokens JWT que identifican al solicitante.
> - **Florida**: autorización (¿qué podés hacer?). Sistema de permisos que controla si el token puede ejecutar una acción específica sobre un recurso específico.
>
> Son sistemas completamente distintos. Tiger puede estar disponible pero Florida puede rechazar la operación si el usuario/servicio no tiene el rol necesario. Ejemplo: `instance-groups:hard-destroy` en Florida es necesario para el `hardDelete`.

---

**P9.3: ¿Qué son los Shark Tokens y cuándo se usan?**
> **Respuesta esperada:** Los Shark Tokens son tokens de corta duración para comunicación server-to-server y workers → APIs. Un componente envía su Service Account de Kubernetes a Tiger y obtiene un Shark Token. Se usan en:
> - Workers de LM para comunicarse con fury-api en los callbacks (`on_success`, `on_error`).
> - fury-scopes-api → LM Scopes API al crear/cancelar jobs (desde 2026-02, con header `x-tiger-token`).
> - Heartbeats de workers usando credentials `client_id/secret` (`Tiger::Api.app_token`).

---

**P9.4: Menciona los headers HTTP que el Traffic Sidecar inyecta automáticamente y son read-only.**
> **Respuesta esperada:**
> - `X-Api-Client-Application`: app de origen de la llamada.
> - `X-Api-Client-Scope`: scope de origen.
> - `X-Fury-User`: usuario LDAP del solicitante.
>
> Son inyectados por el HTTP Middleware / Traffic Sidecar. No se deben modificar manualmente.

---

### Nivel Intermedio

**P9.5: ¿Qué pasa si Tiger está caído cuando se intenta crear un job en LM desde fury-scopes-api?**
> **Respuesta esperada:** Desde 2026-02, fury-scopes-api incluye header `x-tiger-token` al llamar a LM Scopes API para crear/cancelar jobs. Si Tiger está caído, toda creación de jobs falla con `TigerError::AuthenticationError`. Esto agrega Tiger como punto de fallo en el camino de creación de scopes e IGs. Verificar estado de Tiger es el primer paso si los jobs no aparecen en LM.

---

**P9.6: ¿Qué pasa si las credentials del worker LM (`client_id/secret`) son inválidas durante un job en ejecución?**
> **Respuesta esperada:** Los workers usan `client_id/secret` credentials para los heartbeats. Si las credentials son inválidas o Tiger no responde, los heartbeats fallan. Al superar el umbral de unlock de la variante, el lock expira y el job vuelve a `pending` sin haber terminado. Síntoma: job en `pending` sin lock activo, con tasks parcialmente completadas. El job puede ser reclamado por otro worker, potencialmente causando doble ejecución parcial.

---

## 10. CoSMOS — Migración Arquitectónica

### Nivel Básico

**P10.1: ¿Qué es CoSMOS y por qué se está construyendo?**
> **Respuesta esperada:** CoSMOS es el nuevo ecosistema que reemplaza la gestión de scopes en fury-api. El objetivo es desacoplar la entidad Scope del monolito Ruby/Rails (fury-api) hacia microservicios especializados en Python/FastAPI. La migración es transparente para los usuarios — fury-api sigue siendo el punto de entrada hasta el cutover. CoSMOS opera en paralelo.

---

**P10.2: ¿Cuáles son los cuatro componentes nuevos de CoSMOS y qué reemplazan?**
> **Respuesta esperada:**
> - **scopes-api** (Python/FastAPI): reemplaza la lógica de scopes en fury-api (Ruby/Rails).
> - **instance-groups-api** (Python/FastAPI): reemplaza sco-scopes-api (Go 1.21).
> - **scopes-processes** (Python/asyncio): polling de cambios de estado (no tiene equivalente legacy directo).
> - **scopes-adapter** (Python/FastAPI): capa de traducción fury-api ↔ CoSMOS. Sin equivalente legacy.

---

**P10.3: ¿Cuáles son las 4 fases de la migración a CoSMOS?**
> **Respuesta esperada:**
> - **Fase 1 — Shadow scopes**: CoSMOS recibe eventos de fury-api pero no es productivo. En progreso.
> - **Fase 2 — scopes-adapter**: traduce la interfaz fury-api → interfaz CoSMOS. En progreso.
> - **Fase 3 — Migración de datos**: mover scopes existentes de fury-api a CoSMOS. Bloqueada para Standard hasta que instance-groups-api soporte `compute_provider=pilot`.
> - **Fase 4 — Cutover**: fury-api deja de ser source of truth. Todos los scopes viven en CoSMOS. Pendiente.

---

**P10.4: ¿Cuál es el mapeo de estados entre fury-api y CoSMOS?**
> **Respuesta esperada:**
>
> | fury-api status | CoSMOS Scope status |
> |---|---|
> | `creating` | `creating` |
> | `finished` | `active` |
> | `updating` | `updating` |
> | `deleting` | `deleting` |
> | `error` (en creación) | `error_creating` |
> | `error` (en update) | `error_updating` |
> | `error_deleting` | `error_deleting` |
> | `inactive` | Scope sin IGs (no hay status explícito) |
> | `activating` | `creating` (nuevo IG) |
> | `running` (legacy) | `active` |
>
> En CoSMOS, "inactivo" = scope que existe en scopes-api pero no tiene instance-groups en instance-groups-api.

---

### Nivel Intermedio

**P10.5: Explica cómo se divide el modelo monolítico de fury-api en las 4 entidades de CoSMOS.**
> **Respuesta esperada:**
> En fury-api el scope es una entidad monolítica (WebService) que combina definición lógica e infraestructura. En CoSMOS se separa en:
> - **Scope** (scopes-api): nombre, app, criticality, segment, status, traffic — campos lógicos.
> - **LoadBalancer** (scopes-api): entidad explícita (en fury-api era parte de los metadata). FK a Scope (1-to-many). Status: `pending_create → creating → created → deleting`.
> - **InstanceGroupSpec** (instance-groups-api): blueprint de infraestructura: containers, scaling, compute provider, resources.
> - **InstanceGroup** (instance-groups-api): instancia real de infraestructura creada desde un spec. Tiene contexts: ApplicationContext, ScopeContext, ConfigContext, PlacementContext, etc.

---

**P10.6: ¿Qué rol cumple el scopes-adapter en la migración? ¿Qué endpoints debe cubrir?**
> **Respuesta esperada:** El scopes-adapter recibe requests con la interfaz de fury-api y los traduce a llamadas de scopes-api e instance-groups-api. Cubre TODAS las interfaces de fury-api relacionadas a scopes, incluyendo las internas (deployments-api, jobs-deploys). La idea es que ningún componente tenga que migrarse a CoSMOS para funcionar.
>
> Debe cubrir: CRUD básico (create/show/index/update/destroy), lifecycle (recreate, boost), service groups, deploy support (deployment_params, do_creating_initial_deploy), datos para infra (instance_groups_creation_data, instance_groups_deletion_data), consultas (trafficsidecar_versions, policyagentsidecar_versions), scaling_policies CRUD, instance_groups CRUD.
>
> Estado actual: solo mocks. Debe estar completa antes del cutover.

---

**P10.7: ¿Por qué la reducción de tasks en CoSMOS es significativa? ¿De cuántas tasks a cuántas?**
> **Respuesta esperada:**
> - `CreateWebScope` legacy: 27 tasks. CoSMOS: 18 tasks. Reducción: −33%.
> - `DeleteInstanceGroup` legacy: 23 tasks. CoSMOS: 4 tasks. Reducción: −83%.
>
> CoSMOS extrae la complejidad de red y service mesh fuera de los workers hacia APIs propias o componentes delegados. Los jobs se vuelven más simples porque no tienen que gestionar Istio directamente.

---

**P10.8: ¿Cuál es la diferencia entre `sco-scopes-api` e `instance-groups-api` en el manejo de Instance Groups?**
> **Respuesta esperada:**
>
> | Aspecto | sco-scopes-api (Go) | instance-groups-api (Python) |
> |---|---|---|
> | Datos del scope | Los pide a fury-api via HTTP | Tiene su propio InstanceGroupSpec |
> | Dependencia de fury-api | Alta (creation_data, deletion_data) | Baja (solo service_variables) |
> | Sharding | Por deployment + proxy | No sharding (una instancia) |
> | Contexts | No tiene | Sí: Application, Scope, Config, Placement, etc. |
> | Containers | Definidos en spec, no persistidos | Persistidos como relación 1-to-many |
> | Scaling | Via spec, no persistido | Persistido con behaviours y metrics |
>
> instance-groups-api reemplaza completamente a sco-scopes-api.

---

**P10.9: ¿Qué es el CriticalityFramework en fury-api y cómo lo maneja CoSMOS?**
> **Respuesta esperada:** fury-api maneja dos esquemas de criticality:
> - Nuevo (6 niveles): `test`, `low`, `medium`, `high`, `bu-critical`, `company-critical`.
> - Legacy (4 niveles): `test`, `low`, `medium`, `high` (bu-critical y company-critical se mapean a high).
>
> Métodos clave: `get_new_criticality()` (siempre retorna el nivel nuevo), `get_old_criticality()` (retorna el nivel legacy con mapeo). Validación: no se puede cambiar de `test` a non-test ni viceversa.
>
> CoSMOS usa solo los 6 niveles nuevos (schema enum: TEST, LOW, MEDIUM, HIGH, BU_CRITICAL, COMPANY_CRITICAL). Si el adapter recibe un valor legacy, debe traducirlo al nuevo.

---

**P10.10: ¿Cómo se modela el Scaling en CoSMOS vs fury-api? ¿Qué se pierde en la migración?**
> **Respuesta esperada:** fury-api usa un modelo alarm-based (AWS CloudWatch) con N scaling policies por scope, cada una con CRUD propio. instance-groups-api usa un modelo metric-based (Kubernetes HPA) con 1 ScalingConfig por IGSpec editado como bloque completo.
>
> Lo que se pierde: la customización individual de steps de scaling. En CoSMOS, los multi-step scaling están predefinidos y no son editables por el usuario. Solo se permite configurar el `target_value` de CPU; los steps se derivan de ese valor. Esta pérdida se acepta a cambio de simplicidad.
>
> El adapter traduce CRUD individual de scaling_policies → read-modify-write del ScalingConfig completo.

---

**P10.11: ¿Cuál es la dependencia residual de instance-groups-api en fury-api durante la migración?**
> **Respuesta esperada:** instance-groups-api todavía llama a fury-api para obtener service configs: `GET /applications/{app}/scopes/{scope}/configs` → ServiceVariablesContext. El código tiene un bypass de 404 (retorna dict vacío si no existe). Esto significa que CoSMOS no está 100% desacoplado. Esta dependencia deberá resolverse migrando service configs a scopes-api/instance-groups-api, delegando a Configurola, o manteniendo fury-api como fuente durante la transición (via adapter).

---

**P10.12: ¿Qué requisito operacional debe cumplirse antes del cutover de cualquier región en CoSMOS?**
> **Respuesta esperada:** Verificar con el equipo Serverless que existan clusters Kubernetes configurados para todos los scope types y criticidades habilitadas en esa región. La task `choose_serverless_cluster` en `CreateInstanceGroup` de jobs-scopes llama a la Serverless API para obtener un cluster disponible. Si no hay cluster configurado, el job falla con `Serverless::NoClustersFound`. Este vector de falla existe en CoSMOS igual que en legacy — no es deuda temporal.

---

## 11. Observabilidad y Herramientas de Diagnóstico

### Nivel Básico

**P11.1: ¿Cuáles son las principales herramientas de observabilidad que usa el equipo Scopes?**
> **Respuesta esperada:**
> - **Datadog**: métricas de pods, CPU/memoria, alertas de jobs LM, dashboard de aplicaciones (`fury-application-dynamic-supp`).
> - **Grafana**: Deployments Dashboard v2 para logs de fury/localapi de deploys.
> - **New Relic**: APM overview para jobs-scopes.
> - **Backoffice LM**: `backoffice-compute.furycloud.io` para jobs de LM Scopes. `deployments-bo.furycloud.io` para LM Deploys.
> - **scopes-mcp**: MCP disponible en el workspace para consultar estado de scopes, application_regions y VPC membership en tiempo real.
> - **o11y-mcp**: para consultar logs de aplicaciones y métricas de Datadog.

---

**P11.2: ¿Cómo se diagnostica un job de LM colgado en el backoffice?**
> **Respuesta esperada:**
> 1. Elegir el cluster correcto según el segmento y criticidad del scope.
> 2. Filtrar por job name (`create_instance_group`, `create_web_scope`, `delete_web_scope`, etc.).
> 3. Buscar por UUID (formato: `<operacion>_<scope-name>_<segmento>.<app-name>.t<timestamp>`).
> 4. Ver en qué task está colgado: el backoffice muestra la task actual y logs por task.
> 5. Verificar si el worker que lo tomó sigue vivo (host + PID en el registro).
> 6. Verificar si el umbral de unlock ya pasó (job en `pending` de nuevo = lock liberado).
> 7. Acciones disponibles desde el backoffice: cancelar o reintentar el job.

---

**P11.3: ¿Cómo se accede al backoffice de LM Deploys vs el backoffice de LM Scopes?**
> **Respuesta esperada:**
> - **LM Scopes** (para jobs de creación/borrado de scopes e IGs): `https://backoffice-compute.furycloud.io/#/lm/jobs/{job_id}?cluster={cluster}`.
> - **LM Deploys** (para jobs de deploy): `https://deployments-bo.furycloud.io/#/lm/{job_id}/show`.
>
> Son backoffices completamente diferentes. El de LM Deploys también tiene una vista de deploy record: `https://deployments-bo.furycloud.io/#/deployments/{deploy_id}/show`. Tiene selector de Environment (PreProduction para criticidad test, Production para el resto) — seleccionarlo antes de cargar es obligatorio.

---

**P11.4: ¿Cómo se detecta una EC2 huérfana de un scope Standard mediante Datadog?**
> **Respuesta esperada:** Query de detección:
> ```
> avg:system.cpu.idle{application:{app},scope:{scope},compute_cluster_provider:pilot}
> by {host,autoscaling_group,instance_group_id,cluster_name}
> ```
> Señales de orphan:
> - `cluster_name` distinto al `metadata.cluster_name` actual del scope.
> - CPU idle >90%.
> - `autoscaling_group:N/A` (no está en ningún ASG activo).

---

### Nivel Avanzado

**P11.5: Construye la URL del Grafana Deployments Dashboard v2 para un deploy específico. ¿Qué parámetros necesitas?**
> **Respuesta esperada:** URL base: `https://grafana.furycloud.io/d/a11b9d8f-61ea-4390-af86-34bb7209f828/deployments-dashboard-v2`
>
> Parámetros necesarios:
> - `var-deployment_id`: ID del deploy.
> - `var-version`: del campo `build` en GET /deployments/{id}.
> - `var-app_name` y `var-scope_name`.
> - `var-created_at`: timestamp URL-encoded (ej: `2026-03-25T01%3A44%3A38.000%2B00%3A00`).
> - `var-log_cluster` y `var-logger_allocation`: obtener de un deploy exitoso previo del mismo scope.
> - `var-current_components=$__all` y `var-candidate_components=$__all`.
> - `var-application` y `var-service`.
>
> Buscar en los logs: `connection refused`, `DRAINING`, `error`, `panic`, `OOMKilled`, `CrashLoopBackOff`.

---

## 12. Patrones de Soporte y Troubleshooting

### Nivel Básico

**P12.1: Un usuario reporta que su scope está stuck en `creating` y no hay un job visible en el backoffice de LM. ¿Cuál es tu hipótesis principal y cómo la verificas?**
> **Respuesta esperada:** Hipótesis principal: el job se eliminó silenciosamente por falla en la publicación SNS (ausencia de DLQ). Si el framework no logró publicar el mensaje en SNS tras 3 reintentos, el job se elimina de la DB sin traza.
>
> Verificación:
> 1. Buscar el job por UUID en el LM del segmento correcto.
> 2. Verificar estado de Tiger (punto de fallo: fury-scopes-api necesita token Tiger para encolar).
> 3. Verificar alertas de AWS SNS de ese momento (throttling).
>
> Si confirmado: el scope debe ser rescatado manualmente (error → updating → inactivating/finished según estado de infra), y luego reintentar la creación.

---

**P12.2: Un usuario reporta un `500 pre-creación de deploy` y no hay ningún deploy record. ¿Cuáles son las causas comunes?**
> **Respuesta esperada:** Causa A — Mismatch arquitectura build vs instance type:
> - El scope tiene un instance_type ARM (ej. familia `c8g`) pero el build fue compilado solo para `amd64`.
> - fury-api intenta resolver el equivalente AMD64 vía `InstanceType.get_architecture_equivalent_instance_type`. Si `architecture_equivalents: []`, el método retorna un AR Relation vacío y `ar_relation[:name]` lanza un `no implicit conversion of Symbol into Integer`.
> - Diagnóstico: verificar `architectures` del build en versions.furycloud.io y `instance_type` + `architecture_equivalents` del scope.
> - Resolución: cambiar el instance_type del scope a AMD64, o solicitar al equipo Optimizing que agregue los equivalentes ARM64.

---

**P12.3: ¿Qué causa el error `500 Multiple successful responses` en el Proxy y cómo se resuelve?**
> **Respuesta esperada:** Ocurre cuando un IG quedó registrado en más de un shard (dato inconsistente). Típicamente pasa cuando un deploy creó un nuevo cluster tag pero el anterior no fue eliminado y quedó duplicado.
>
> Resolución:
> 1. Identificar en qué shards está el duplicado consultando cada shard directamente por criticidad.
> 2. Determinar cuál IG tiene tráfico real (ControlPlane) y cuál es zombie.
> 3. Eliminar el zombie con `hardDelete=true` directamente en el shard (requiere permiso Florida `instance-groups:hard-destroy`).
> 4. Verificar: reintentar la operación vía Proxy.

---

**P12.4: ¿Cómo diagnosticarías un deploy que "se cancela solo" sin intervención del usuario?**
> **Respuesta esperada:**
> 1. Verificar el deploy record en Deployments API: buscar el estado actual y el historial.
> 2. Si el deploy llegó a `warning` antes de cancelarse: buscar alertas de Datadog activas en ese momento para la app/scope. El Rollback Recommendation se dispara cuando las alertas se activan durante el swap de tráfico.
> 3. Si no hay alertas de Datadog obvias: revisar si el grace period expiró sin intervención del usuario (flujo automático).
> 4. Revisar logs del deploy en Grafana para descartar errores de infraestructura.

---

**P12.5: Describe el patrón de diagnóstico para un IG zombie post Blue-Green cancelado en Serverless.**
> **Respuesta esperada:** Señal: dos prefijos de timestamp distintos en los `pod_name` del mismo scope en Datadog.
>
> Diagnóstico:
> 1. Confirmar IGs activos en Datadog agrupado por `pod_name` en el dashboard `fury-application-dynamic-supp`.
> 2. Confirmar que el IG zombie NO existe en scopes-api (`GET /v1/applications/{app}/scopes/{scope}/instance-groups/{IG-ZOMBIE}` → "instance group not found").
> 3. Encontrar el job LM cancelado en `lm.furycloud.io/jobs?uuid_search={scope}.{app}&limit=20`.
>
> Resolución:
> - Si el IG **existe en scopes-api**: `DELETE` vía scopes-api.
> - Si el IG **no existe en scopes-api** (huérfano puro en K8s): escalar al equipo Serverless con: cluster name, namespace (= app name), nombre del IG zombie.
>
> Importante: los re-deploys NO resuelven el zombie.

---

**P12.6: ¿Cómo distingues un IG Canary huérfano post-rollback (Causa G) de un IG zombie normal?**
> **Respuesta esperada:** Un IG Canary huérfano tiene el sufijo `.canary` en el nombre (específico de la estrategia `percentage_canary`). La señal característica en el endpoint de infra: `asg_current` apunta al IG `.canary` con instancias OutOfService en ELB (health: Unknown), mientras `asg_candidate` tiene instancias Healthy — el scope funciona 100% en el candidato, el `.canary` huérfano consume recursos sin servir tráfico.
>
> A diferencia de un zombie normal: Pilot sigue gestionando activamente este ASG (recrea instancias si se terminan). Por eso EC2 terminate no sirve: Pilot las recrea para mantener `min_instances`. La resolución es llamar el DELETE de scopes-api (aunque retorne 404 en GET) para que se lance el job de borrado hacia Pilot.

---

### Nivel Avanzado

**P12.7: Un scope en `error` tiene criticidad `business-critical` y está recibiendo tráfico por un IG que sobrevivió. ¿Cuál es el procedimiento exacto?**
> **Respuesta esperada:** Regla crítica: NO pasar a `inactivating` — destruiría la infraestructura y causaría downtime.
>
> Procedimiento:
> 1. Confirmar con scopes-mcp que el IG actual existe y recibe tráfico (confirmar en ControlPlane `destination_rules`).
> 2. Verificar que no hay job activo en LM para este scope.
> 3. Verificar la infra física (IG status en scopes-api).
> 4. PUT `{ "status": "updating", "triggers_jobs": false }` → scope pasa a `updating`.
> 5. PUT `{ "status": "finished", "triggers_jobs": false }` → scope operativo.
> 6. Solicitar al usuario que lance un nuevo deploy para validar el estado real.
> 7. Si falla de nuevo → evaluar con el equipo si hay un bug subyacente en la infra.
>
> Nunca `inactivating` sobre un scope productivo en `error` salvo solicitud explícita del usuario con confirmación de que entiende el riesgo.

---

**P12.8: ¿Cómo verificas que un migrate de scope no dejó instancias EC2 huérfanas después de completarse?**
> **Respuesta esperada:**
> 1. Buscar el deploy de migración en Deployments API (strategy `serverless_migration` o `gcp_migration`).
> 2. Verificar que el job `delete_web_service` (en LM) completó exitosamente y en tiempo razonable (si completó en <90s, la instancia estaba detached cuando corrió → posible orphan).
> 3. Query de detección en Datadog:
>    ```
>    avg:system.cpu.idle{application:{app},scope:{scope},compute_cluster_provider:pilot}
>    by {host,autoscaling_group,instance_group_id}
>    ```
>    Retorno con `autoscaling_group:N/A` + `compute_cluster_provider:pilot` en scope Serverless → EC2 huérfana confirmada.
> 4. Verificar el `instance_group_id` en tags Datadog → GET a scopes-api → si devuelve 404, el IG fue marcado deleted.
> 5. Remediación: Mithril con Expert con permisos EC2 para `aws ec2 terminate-instances`.

---

## 13. Reglas SRE Irrevocables

### (Todas críticas — evaluación de actitud y conocimiento operacional)

**P13.1: Enumera las reglas SRE que son absolutamente irrevocables en el dominio Scopes.**
> **Respuesta esperada:**
>
> **Regla 1 — NUNCA `inactivating` a scope productivo en `error`**: destruirá infraestructura física y causará downtime. Único procedimiento válido: `error → updating → finished` + deploy manual. Solo se omite si el usuario lo solicita explícitamente y confirma que entiende el riesgo.
>
> **Regla 2 — NUNCA ejecutar operaciones destructivas sin confirmación por turno**: las autorizaciones previas no se trasladan a acciones futuras.
>
> **Regla 3 — Estados terminales de reintento**: `error_deleting` y `error_inactivating` solo tienen una salida: reintentar la operación. No forzar otros estados.
>
> **Regla 4 — Scope sin `cluster_name`**: solo en este caso se puede forzar `deleted` directamente. Con `cluster_name` presente, la infra existe y NO se puede saltar el job de borrado.
>
> **Regla 5 — Intervención durante migración**: no intervenir manualmente en un scope que tiene dos conjuntos de infraestructura simultáneos sin entender el estado completo.
>
> **Regla 6 — Durante falla de deploy**: analizar TODAS las tasks pendientes antes de solicitar ABORT o force-finish. Las tasks de Istio (VirtualServices, DestinationRules) y service-groups deben ejecutarse antes del force.

---

**P13.2: Un colega te dice: "el scope en `error` está en el camino crítico, ejecuto `inactivating` rápido y listo". ¿Qué haces?**
> **Respuesta esperada:** Detenerlo de inmediato. `inactivating` destruye la infraestructura física (Instance Groups, Istio, DNS) causando downtime de producción. El procedimiento correcto es:
> 1. Forzar `updating` (sin destruir infra).
> 2. Forzar `finished` (scope operativo).
> 3. Solicitar deploy manual al usuario.
>
> Si el scope ya tiene tráfico, está recibiendo peticiones reales. Destruir la infra = downtime inmediato. El único caso donde `inactivating` es aceptable es si el usuario lo pide explícitamente y confirma que el scope puede ser desactivado (no está en producción activa).

---

**P13.3: ¿Antes de ejecutar qué tipo de operaciones debes analizar el job LM completo y sus tasks pendientes?**
> **Respuesta esperada:** Antes de: ABORT, force-finish, o force-close de cualquier deploy en estado `finish_error`, `rollback_error` o `swap_stuck`.
>
> El análisis debe identificar:
> - Qué task falló y en qué posición del job.
> - Qué tasks quedaron pendientes después de la falla.
> - Para cada task pendiente: ¿gestiona infra de Istio? → debe ejecutarse antes del force. ¿Gestiona service-group? → idem. ¿Gestiona scale-to-zero o unpause? → verificar validaciones internas.
>
> Excepción segura: si la task fallida es la última del job y no hay tasks que le sigan → ABORT es seguro directamente.

---

## 14. Integraciones del Ecosistema

### Nivel Básico

**P14.1: ¿Qué es RAVEN y para qué se usa en el dominio Scopes?**
> **Respuesta esperada:** RAVEN es el sistema de eventos del ecosistema Fury. fury-api le envía eventos HTTP POST en cada create/update/destroy de un scope (concern `Eventable`). Estos eventos son consumidos por otros sistemas como fury-spider (para actualizar el grafo de relaciones) y, en el contexto de CoSMOS, por el consumidor de shadow scopes (para sincronizar los cambios de CoSMOS en fury-api). También se usa para auditar transiciones de estado (quien ejecutó un `inactive → running` es un usuario humano, no un worker).

---

**P14.2: ¿Qué hace Net-API en el contexto de la creación de un scope?**
> **Respuesta esperada:** Net-API gestiona el aislamiento de red: segments, placements y affinities. fury-api lo consulta al crear un scope para:
> 1. `GET Application/Segments` → verifica que la criticality esté en `allowed_criticalities` del segmento.
> 2. `GET Application/Segment/Placements` → obtiene placements disponibles para esa combinación app + segmento.
>
> Si la criticality no está permitida en ese segmento, la creación del scope falla. También determina los placements de red (subnets, VPCs) donde se desplegará la infraestructura.

---

**P14.3: ¿Qué es ControlPlane API y para qué se usa en diagnóstico?**
> **Respuesta esperada:** ControlPlane API es la API que gestiona el routing de tráfico en el Service Mesh (Istio). Se usa para:
> - Listar IGs registrados en el mesh (`GET /target_groups?service={lb_id}`).
> - Ver reglas de routing con porcentajes (`GET /destination_rules?service={lb_id}`).
> - Listar instancias activas (`GET /targets?service={lb_id}`).
>
> Es la fuente de verdad para saber qué IG está recibiendo tráfico real en un momento dado. Especialmente importante para confirmar PROMOTE_MISMATCH (fury-api dice un IG pero ControlPlane sirve otro).

---

**P14.4: Describe la diferencia entre Rate Limit en Fury. ¿Qué es Istio/Envoy en este contexto?**
> **Respuesta esperada:** El Rate Limit en Fury se aplica a nivel de Service Mesh usando Istio/Envoy. El servicio `fury_ratelimit-api` recalcula las políticas via BigQueue `recalculate-{criticality}`. Durante la creación de un scope, la task `notify_rate_limit` notifica al sistema que el scope existe y `wait_rate_limit_configuration` espera a que la configuración sea aplicada. Si el rate limit no se configura correctamente, el scope puede rechazar tráfico o no limitarlo apropiadamente.

---

### Nivel Avanzado

**P14.5: ¿Cómo resuelve fury-api la URL de Scopes API en jobs-deploys según criticidad y feature flag?**
> **Respuesta esperada:** jobs-deploys resuelve la URL con esta prioridad:
> 1. `USE_SCOPES_API_STAGE` env var (si está seteada, la usa directamente).
> 2. Feature toggle `ig_proxy` con contexto (criticality + segment + app_name). Si está ON → usa `serverlessapi_url_proxy` (el Instance Groups Proxy).
> 3. Criticality mapping estático: `test → TEST URL`, `low/medium → PROD URL`, `high+ → CORE URL`.
> 4. Fallback a region config.
>
> Esto tiene impacto en diagnóstico: si `ig_proxy` está OFF y el deploy falla en creación de IG, buscar en los logs de Scopes API directamente (no en el Proxy).

---

## 15. Escenarios Situacionales (Role-play)

### Situación 1 — Urgencia productiva

**P15.1: Son las 3am, el on-call te llama: "el scope `payment-gateway/prod-core` está en `error` y está afectando pagos". ¿Qué haces paso a paso en los primeros 5 minutos?**
> **Respuesta esperada (proceso esperado):**
>
> **T+0 — Entender el estado real:**
> 1. `scopes-mcp: get_scope(payment-gateway, prod-core)` → verificar status, cluster_name, metadata actual.
> 2. Confirmar con ControlPlane si el IG actual está recibiendo tráfico (`GET /destination_rules?service={lb_id}`).
>
> **T+1 — Verificar job LM:**
> 3. Buscar job activo en LM para este scope (backoffice: `backoffice-compute.furycloud.io`).
> 4. Si hay job activo: esperar o cancelar antes de actuar.
>
> **T+2 — Rescue:**
> 5. Si la infra existe y recibe tráfico → aplicar rescue `error → updating → finished`:
>    ```
>    PUT /applications/payment-gateway/scopes/prod-core
>    {"status": "updating", "triggers_jobs": false}
>    ```
>    Luego:
>    ```
>    PUT /applications/payment-gateway/scopes/prod-core
>    {"status": "finished", "triggers_jobs": false}
>    ```
> 6. Verificar que el scope queda en `finished`.
> 7. Notificar al owner del scope que valide un nuevo deploy.
>
> **NUNCA hacer:** `inactivating` sobre un scope de pagos productivo.

---

### Situación 2 — CoSMOS en cutover

**P15.2: El equipo acaba de hacer el cutover de un segmento a CoSMOS. Un usuario reporta que su scope se creó pero no recibe tráfico después de horas. ¿Cómo diagnosticas?**
> **Respuesta esperada:**
> 1. Verificar en scopes-api si el scope existe y está en estado `active`.
> 2. Verificar en instance-groups-api si existe un InstanceGroup en estado `created` para ese scope.
> 3. Consultar ControlPlane: verificar si el IG está registrado como target group (`GET /target_groups?service={lb_id}`).
> 4. Verificar destination_rules: si el IG existe pero con `percentage: 0` → el deploy (Initial Deploy) no completó.
> 5. Verificar jobs de LM Scopes CoSMOS: buscar `CreateCosmosWebScope` o `CreateCosmosInstanceGroup`.
> 6. Verificar si falta un cluster Kubernetes configurado en la región/criticidad (`Serverless::NoClustersFound`).
> 7. Si el scope nunca completó Initial Deploy (recuerda: con SDAPI nace operativo, sin SDAPI necesita deploy): solicitar al usuario que lance un deploy manual.

---

### Situación 3 — Deploy producción bloqueado

**P15.3: Un usuario de alta criticidad reporta que su deploy quedó en `finish_error`. ¿Qué analizas ANTES de solicitar un force-finish?**
> **Respuesta esperada:**
> 1. Obtener el job LM del deploy bloqueado (`deployments-bo.furycloud.io`).
> 2. Identificar la task que falló y su posición en el job.
> 3. Listar todas las tasks pendientes (sin ejecutar) después de la falla.
> 4. Para cada task pendiente:
>    - ¿Gestiona Istio (VirtualServices, DestinationRules)? → Debe ejecutarse antes del force. Si se salta, pueden quedar recursos zombie que bloqueen deploys futuros.
>    - ¿Gestiona service-group? → Idem.
>    - ¿Gestiona scale-to-zero, unpause, o similares? → Verificar si tiene validaciones internas que la saltean.
> 5. Solo si no hay tasks pendientes con impacto en infra → proceder con force-finish.
> 6. Si hay tasks pendientes críticas → ejecutarlas manualmente primero, documentar cada paso.

---

### Situación 4 — Evaluación de arquitectura

**P15.4: El equipo quiere migrar el segmento `mexbank-prod` a CoSMOS en 2 semanas. ¿Qué preguntas harías y qué verificarías antes de dar el OK?**
> **Respuesta esperada:**
>
> **Preguntas de readiness:**
> 1. ¿El scopes-adapter está completamente implementado para todos los endpoints que usan los scopes de mexbank?
> 2. ¿Los jobs CoSMOS (`CreateCosmosWebScope`, `DeleteCosmosWebScope`, `CreateCosmosInstanceGroup`, etc.) fueron probados en staging con scopes de criticidad `high` y `bu-critical`?
> 3. ¿Hay clusters Kubernetes configurados en la región `us-east-1-aws` para todas las criticidades de mexbank? (`choose_serverless_cluster` fallará con `Serverless::NoClustersFound` si no los hay).
> 4. ¿El sistema de shadow scopes está operativo y sincronizando correctamente?
> 5. ¿Cuál es el plan de rollback si el cutover falla? ¿En cuánto tiempo podemos volver a fury-api?
>
> **Verificaciones técnicas:**
> 6. Validar el mapeo de todos los campos de scope del segmento mexbank en el adapter (campos bancarios especiales).
> 7. Confirmar que scopes-processes puede manejar el volumen de eventos de mexbank.
> 8. Verificar que Florida tiene los roles correctos para las operaciones CoSMOS en el segmento bancario.
> 9. Ejecutar una prueba de migración de scope no productivo antes del cutover.
> 10. Coordinar con el equipo regulatorio de mexbank para cualquier requisito de compliance durante la migración.

---

## Bonus — Preguntas de Cultura y Proceso

**PB.1: ¿Cuándo actualizarías un `architecture file` de un componente y cuál es el proceso correcto?**
> **Respuesta esperada:** Se actualiza después de sincronizar un submodulo con nuevos commits. El proceso:
> 1. Correr `check_architecture_drift.sh {submodule-path}` para detectar métodos nuevos/eliminados y task lists cambiadas.
> 2. Actualizar SOLO las secciones con drift. Nunca regenerar el archivo completo — los gotchas y secciones `[VERIFICAR]` son conocimiento verificado manualmente y no pueden auto-generarse.
> 3. Actualizar el frontmatter con `verified_at_commit` (SHA-40 del submodulo) y `last_verified` (fecha actual).
> 4. Sin este paso, el archivo quedará STALE en `validate_architecture_freshness.sh`.

---

**PB.2: Un colega propone resolver un bug de producción haciendo `--no-verify` en el commit para saltar los hooks de git. ¿Cuál es tu posición?**
> **Respuesta esperada:** No se aceptan bypasses de hooks de seguridad. Los hooks del repositorio validan invariantes importantes (ej: frontmatter válido en references/*.md). Si el hook falla, hay que investigar la causa raíz y corregirla. Saltarlo puede introducir documentación inválida que luego cause confusión o fallos en el sistema de validación de arquitectura.
>
> Proceso correcto: identificar por qué falla el hook, corregir el problema (ej: frontmatter incorrecto), y luego commitear. Si el hook es incorrecto, proponer un fix al hook mismo — no saltearlo.

---

**PB.3: ¿Cómo determinas qué reference file leer ante un síntoma que no conoces?**
> **Respuesta esperada:** El proceso de routing:
> 1. `references/glossary.md` primero si el término es desconocido.
> 2. Según el síntoma: scope en error/stuck → `state-machine.md` + `support-patterns.md`. Deploy fallido → `deployments-errors.md`. LM job colgado → `little-monster.md` + `little-monster-catalog.md`. IG/proxy → `instance-groups-proxy.md`. Error string desconocido → `errors.md`. Componente interno → `architecture/{componente}.md`.
> 3. CLAUDE.md del proyecto tiene la tabla de routing completa.
>
> Principio: diagnose before executing. Usar el mínimo contexto necesario. Precisión sobre exhaustividad.

---

**PB.4: ¿Cuál es el proceso correcto para sincronizar un submodulo en este repositorio?**
> **Respuesta esperada:** Este repositorio tiene cambios locales que deben preservarse. Nunca hacer `reset --hard` ni `checkout .`. El flujo correcto:
> 1. `git fetch origin` → ver qué hay en el remoto sin tocar el árbol local.
> 2. `git merge origin/<branch>` → integrar cambios remotos preservando los locales; resolver conflictos si los hay.
> 3. Si hay conflictos: resolverlos manualmente, luego `git add` + `git commit`.
>
> Nunca: `git pull --rebase` sin confirmar con el usuario, ni descartar cambios locales sin aviso explícito.

---

*Documento generado desde las fuentes: fury_scopes-design/references/, fury_scopes-design/architecture/, fury_cosmos-design/references/. Última revisión basada en documentación verificada a 2026.*