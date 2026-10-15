# (Opcional) Teoría de grafos para troubleshooting con IA

Pregunta: ¿qué tan fácil y viable es mapear el sistema como una red de grafos para que la búsqueda del
error (por parte de una persona o de una IA) sea más eficiente?

**Respuesta corta: es viable y relativamente barato si ya existe trazabilidad distribuida con
OpenTelemetry.** El grafo sale casi gratis de las trazas. Lo difícil no es la teoría de grafos, sino
los bordes que no están instrumentados (legacy, asíncrono) y no confundir correlación con causalidad.
Además, encaja literalmente con la rúbrica: *"grafos de topología vivos que nutran modelos de IA
Causal e IA Agéntica"* (ítem 5).

## 1. Cómo se construye el grafo

| Elemento | Qué es | De dónde sale |
|---|---|---|
| **Nodo** | Servicio, base de datos, cola, dependencia externa (otro banco, Bre-B, AS400) | `service.name` y `peer.service` / `db.system` / `messaging.system` de los spans (Semantic Conventions) |
| **Arista dirigida** A → B | "A llama a B" (A depende de B) | Pares span cliente → span servidor de una misma traza |
| **Peso de la arista** | Peticiones/s, tasa de error, latencia p99 entre A y B | Connector `servicegraph` del OpenTelemetry Collector |
| **Atributos del nodo** | SLO, burn rate, último despliegue, dueño, versión | Métricas + eventos de CI/CD + catálogo (Backstage/ServiceNow) |

Fuentes alternativas: Istio/Kiali (malla de servicios), **eBPF** (Extended Berkeley Packet Filter) para
ver conexiones de red sin instrumentar código, y el catálogo de servicios como grafo "declarado" para
contrastar con el grafo "observado".

## 2. Qué algoritmos hacen más eficiente la búsqueda

| Pregunta en el incidente | Técnica de grafos | Costo |
|---|---|---|
| ¿A quién afecta que se caiga la base de datos de pagos? (radio de explosión) | **BFS/DFS** (Breadth-/Depth-First Search) sobre el grafo invertido | O(V+E), instantáneo con cientos de servicios |
| ¿Dónde **nace** la falla? | Nodo anómalo cuyos **sucesores (dependencias) están sanos**: recorrer hacia abajo desde el síntoma hasta el nodo anómalo más profundo | O(V+E) |
| Hay varios candidatos, ¿cuál es más probable? | **Random walk / PageRank personalizado** sobre el subgrafo anómalo, ponderado por la correlación de anomalías (enfoque de papers como *MicroRCA*, *CloudRanger*, *MicroCause*) | Bajo |
| Hay ciclos (A ↔ B), ¿cómo ordeno? | Colapsar **componentes fuertemente conexos** (algoritmo de **Tarjan**) para obtener un DAG (Directed Acyclic Graph) y luego **orden topológico** | O(V+E) |
| ¿Qué servicio es un punto único de falla? | **Puntos de articulación** / centralidad de intermediación (betweenness) | O(V·E), aceptable offline |
| ¿Quién causa a quién de verdad? | Grafo **causal** (algoritmo PC, causalidad de Granger) restringido por el grafo de topología | Alto; es investigación aplicada |

**La idea clave:** sin grafo, buscar la causa es revisar N servicios (O(N) dashboards). Con grafo, se
podan las ramas sanas y se revisan solo los nodos del camino anómalo, típicamente 2 a 5 de cientos.

## 3. Cómo lo usa la IA (con MCP)

En vez de meter todos los logs en el prompt, el servidor MCP de observabilidad expone herramientas de
grafo y el agente **navega**:

```
dependencias(servicio)           → hijos en el grafo
dependientes(servicio)           → padres (radio de explosión)
nodos_anomalos(ventana)          → nodos con burn rate o anomalía
camino_anomalo(desde=síntoma)    → recorrido hasta el nodo anómalo más profundo
cambios_recientes(servicio)      → despliegues, configuración, feature flags
```

Ventajas: menos tokens (menos costo), menos alucinación porque el agente razona sobre datos
estructurados, y una explicación verificable ("pagos-api falla porque su dependencia antifraude tiene
p99 de 4 s desde el despliegue v2.3.1 hace 12 min, y antifraude no tiene dependencias anómalas").

## 4. Viabilidad

| Aspecto | Dificultad | Comentario |
|---|---|---|
| Grafo de servicios síncronos (HTTP/gRPC) | 🟢 Fácil | Sale de las trazas con `servicegraph`; Tempo y Kiali ya lo dibujan |
| Algoritmos (BFS, PageRank, Tarjan) | 🟢 Fácil | Librerías maduras (NetworkX en Python); el grafo de un banco tiene cientos o pocos miles de nodos |
| Bordes asíncronos (Kafka/MQ) | 🟡 Medio | Requiere propagar `traceparent` en los headers y usar span links |
| Legacy no instrumentable (AS400) | 🟡/🔴 | Nodo "caja negra" inferido desde el adaptador MQ, eBPF o monitoreo sintético |
| Topología que cambia (despliegues, autoscaling) | 🟡 Medio | Grafo versionado por ventana de tiempo; comparar "antes" vs. "ahora" también da pistas |
| Causalidad real (no solo correlación) | 🔴 Difícil | Usar la topología como restricción y los eventos de cambio; la IA propone y el humano decide |
| Almacenamiento | 🟢 | En memoria para tiempo real; base de grafos (Neo4j) solo si se quiere historial y consultas complejas |

**Conclusión:** como MVP (Minimum Viable Product) es viable en semanas, no meses: `servicegraph` +
detección de anomalías por SLO/burn rate + BFS hacia el nodo anómalo más profundo + herramientas MCP.
Para la presentación, conviene ponerlo como **fase 2 del Eje 3** (después de estandarizar la telemetría),
no como lo primero.

## 5. Cómo decirlo en la exposición (30 segundos)

> "Con la telemetría estandarizada, las trazas nos dan gratis un grafo vivo de dependencias. En un
> incidente no revisamos 200 dashboards: el sistema recorre el grafo desde el síntoma hasta el nodo
> anómalo más profundo cuyas dependencias están sanas, lo cruza con los cambios recientes y le entrega
> al Incident Commander dos o tres hipótesis rankeadas, vía MCP, con evidencia. Ese grafo es la base
> para la IA causal y la auto-remediación del roadmap 2026-2027."
