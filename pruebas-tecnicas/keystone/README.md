# Entrevista con IA - Keystone

Entrevista por voz con un entrevistador de IA, 5 nov 2026. Rol de backend/plataforma con Python,
FastAPI, AWS (SQS, ECS, RDS), PostgreSQL, Elasticsearch/OpenSearch, GraphQL y runtimes de agentes LLM.
Las preguntas son las que el entrevistador listó; las respuestas son para decirlas en voz alta
(60–90 segundos cada una), en primera persona.

> Lo marcado con **[confirmar]** depende de un detalle que solo tú sabes. Si no es cierto, quítalo:
> todo lo que digas lo tienes que poder defender.

## 1. Canalización de datos de alto rendimiento con Python y FastAPI

"En MercadoLibre construí buena parte de las canalizaciones del sistema de triage automático de
incidentes. Llegaban tickets y alertas, había que traer logs de varias aplicaciones, cruzarlos con el
mapa de dependencias y pasarlos a un LLM. Para la concurrencia usé Python con asyncio y un semáforo
que limitaba cuántas llamadas simultáneas hacíamos al LLM y a la API de observabilidad, porque los dos
tenían límites de tasa. Para la presión de flujo, o backpressure, puse una cola SQS entre la ingesta y
el procesamiento: si el procesamiento iba lento, los mensajes esperaban en la cola en vez de tumbar el
servicio, y los consumidores escalaban según la profundidad de la cola. Los cuellos de botella eran
las llamadas externas, así que cacheé el mapa de dependencias, agrupé consultas de logs y medí la
latencia de cada etapa para saber dónde estaba el tiempo. La capa de entrada la expondría con FastAPI
con endpoints async que solo validan y encolan, sin hacer el trabajo pesado dentro de la petición."

**[confirmar]** si usaste FastAPI en ese sistema o solo en proyectos propios; dilo como corresponda.

## 2. Índices en Elasticsearch / OpenSearch con mucho dato no estructurado

"He trabajado con el stack ELK sobre todo para logs. Lo que hago para mantener la latencia baja:
primero, mapping explícito en vez de dejar el dynamic mapping, para no tener explosión de campos, y
distinguir `keyword` para filtros y agregaciones de `text` para búsqueda completa. Segundo, índices por
tiempo con rollover y ILM (Index Lifecycle Management), detrás de un alias, para que los shards queden
en un tamaño sano, más o menos entre 10 y 50 GB, y mover lo viejo a nodos más baratos. Tercero, en las
consultas uso filter context siempre que no necesito puntaje, porque se cachea y es más rápido. Y
para cargas masivas uso la Bulk API y subo el `refresh_interval` durante la carga."

## 3. Runtime de agentes o tool calling de LLM en producción

"Sí. En MercadoLibre participé en el sistema de triage de tickets con Claude de Anthropic en
producción. El modelo estaba envuelto en un harness con hooks que bloqueaban acciones peligrosas o no
deseadas antes de ejecutarse. Las herramientas se las dimos al modelo con un servidor MCP (Model
Context Protocol) que diseñé junto con el equipo de observabilidad: consultar logs, recorrer el mapa
de dependencias y buscar runbooks y casos pasados. El flujo era: ubicar el servicio que fallaba y su
radio de impacto, leer los logs, diagnosticar con los runbooks, y entregar al dueño del ticket un
diagnóstico con una sección de certezas e incertidumbres y un camino de acción. Siempre con humano en
el ciclo: una persona revisaba y aprobaba antes de ejecutar cualquier acción."

## 4. Falla crítica con SQS y ECS

"**[confirmar: cuenta tu caso real; si no tienes uno, usa este patrón como 'un caso típico que
enfrentamos']**. Tuvimos consumidores en ECS leyendo de SQS donde el procesamiento de algunos mensajes
tardaba más que el visibility timeout. El mensaje volvía a la cola, otro consumidor lo tomaba y se
procesaba dos veces; y un mensaje mal formado hacía fallar al consumidor una y otra vez, un poison
message, que bloqueaba el avance. Las medidas fueron: subir el visibility timeout por encima del tiempo
real de procesamiento; claves de idempotencia, guardando el id del mensaje con una restricción única en
la base de datos para que un duplicado no tuviera efecto; una DLQ (Dead Letter Queue) con
`maxReceiveCount` para sacar los mensajes que fallan varias veces; reintentos con backoff exponencial
y jitter; y alarmas en CloudWatch sobre la profundidad de la DLQ y la edad del mensaje más viejo. Luego
reprocesábamos la DLQ con redrive cuando el error estaba corregido."

## 5. Consistencia entre PostgreSQL y Elasticsearch en microservicios

"PostgreSQL es la fuente de verdad y Elasticsearch es una vista para búsqueda, con consistencia
eventual. Evito la escritura doble desde la aplicación, porque si una de las dos falla quedan
desincronizadas. Uso el patrón transactional outbox: en la misma transacción que cambia el dato,
escribo un evento en una tabla outbox, y un proceso aparte lo publica e indexa. La otra opción es CDC
(Change Data Capture) con Debezium leyendo el log de PostgreSQL. La indexación es idempotente, por id
del documento, con versión externa para que un evento viejo que llega tarde no pise uno nuevo. Y dejo
un job de reconciliación periódico que compara conteos o checksums y reindexa lo que falte."

## 6. GraphQL: problema N+1 y joins complejos

"El problema N+1 lo he enfrentado sobre todo con ORMs y APIs REST, y en GraphQL aparece igual porque
cada resolver pide su dato por separado. La solución estándar es DataLoader: agrupa en una sola
consulta todas las claves que piden los resolvers en el mismo ciclo, con un `WHERE id IN (...)`, y
cachea por petición. Para joins complejos o agregaciones prefiero resolverlos en la base de datos, con
una vista o una consulta preagregada, en vez de armarlos en los resolvers. Y pongo límites de
profundidad y de complejidad de la consulta para que un cliente no pueda pedir algo que tumbe la base."

## 7. Decisión de arquitectura independiente sin requisitos claros

"El sistema de triage es el mejor ejemplo. Nadie sabía bien cómo debía funcionar; el pedido era
'reducir el tiempo de diagnóstico'. Lo primero fue definir una métrica: tiempo desde que llega el
ticket hasta tener un diagnóstico útil. Tuve que decidir cómo hacer el mapeo de dependencias para
ubicar el servicio que fallaba. Lo validé con una prueba de concepto sobre casos pasados, donde ya
conocíamos la causa, y comparé el diagnóstico del sistema contra lo que había pasado de verdad. Luego
lo corrimos con humanos revisando cada salida antes de confiar en él, y fuimos ajustando los runbooks
con lo que fallaba."

## 8. Despliegues sin inactividad, migraciones y monitoreo (ECS + RDS)

"En ECS uso despliegues rolling con `minimumHealthyPercent` en 100, para que las tareas nuevas pasen
el health check del balanceador antes de apagar las viejas, o blue/green cuando el cambio es más
riesgoso, con rollback automático si saltan las alarmas. Para las migraciones de esquema en RDS uso
expand-contract: primero agrego lo nuevo sin romper lo viejo, despliego código que funciona con
ambos, migro los datos, y solo al final quito lo viejo. Así cada versión es compatible con el esquema
anterior y el rollback es posible. En Python las migraciones van versionadas, por ejemplo con
Alembic **[confirmar]**. Para monitoreo, CloudWatch con las cuatro señales doradas: latencia, tráfico,
errores y saturación, con alarmas atadas al despliegue."

## 9. Parsear, enriquecer y validar datos no estructurados y ruidosos

"Lo hago por etapas. Primero normalizo: codificación, fechas, mayúsculas, espacios. Luego valido
contra un esquema, en Python con modelos tipo Pydantic, que rechazan lo que no cumple en vez de
dejarlo pasar a medias. Después enriquezco con datos de referencia, por ejemplo en el triage
agregábamos a cada log el servicio, el dueño y sus dependencias. Lo que no pasa la validación no se
pierde: va a una cola o tabla de cuarentena con el motivo del rechazo, para revisarlo o reprocesarlo.
La escritura final es idempotente, y mido la tasa de rechazo: si sube de golpe, normalmente cambió el
formato de la fuente."

## 10. Deuda técnica vs refactorizar, en remoto y con poca burocracia

"Mi criterio es qué tan reversible es la decisión. Si es fácil de cambiar después, acepto la deuda y
avanzo rápido. Si es difícil de revertir, como el modelo de datos, un contrato de API público o la
seguridad, me detengo a hacerlo bien desde el principio. La deuda que acepto la dejo escrita, en un
ticket o un registro de decisión, para que no sea invisible. Y me detengo a refactorizar cuando esa
deuda empieza a costar: cuando cada cambio en esa parte tarda más, cuando causa incidentes, o justo
antes de escalar ese componente. Con alta responsabilidad, eso lo comunico al equipo en vez de
decidirlo en silencio."

## Tu pregunta sobre el uso de IA

La transcripción se corta en tu pregunta. Una forma clara de hacerla:

"¿Qué tanto se usa la IA en el trabajo diario del equipo? Yo la uso mucho para diagnóstico repetitivo
y para aprender rápido, y me hace bastante más productivo, siempre revisando lo que produce."

## Nombres clave para repasar

- **Concurrencia:** asyncio, semáforo, backpressure, rate limit, token bucket.
- **Elasticsearch:** explicit mapping, `keyword` vs `text`, ILM (Index Lifecycle Management), rollover, alias, filter context, Bulk API, `refresh_interval`.
- **SQS:** visibility timeout, poison message, DLQ (Dead Letter Queue), `maxReceiveCount`, redrive, idempotency key, backoff con jitter.
- **Sincronización:** transactional outbox, CDC (Change Data Capture), Debezium, versión externa, reconciliación.
- **GraphQL:** N+1, DataLoader, query depth/complexity limits.
- **Despliegue:** rolling con `minimumHealthyPercent`, blue/green, expand-contract, Alembic.
