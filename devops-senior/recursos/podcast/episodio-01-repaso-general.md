# Podcast de repaso — Episodio 1: todo lo visto hasta el 15 de octubre de 2026

Guion del audio `episodio-01-repaso-general.mp3` (misma carpeta). Dos voces
colombianas: **Salomé** y **Gonzalo**. Las marcas `[PAUSA n]` son silencios
de *n* segundos para que intentes decir el nombre **antes** de que lo digan
(regla del repo: forzar el recuerdo del nombre, no solo del mecanismo).

Formato del guion: cada línea `NOMBRE: texto` es un turno; el generador
(`generar.py`) lo convierte en audio.

---

SALOMÉ: Hola, Sebastián. Bienvenido al primer episodio de tu podcast de repaso. Yo soy Salomé.

GONZALO: Y yo soy Gonzalo. Hoy vamos a repasar todo lo que has visto en el plan para llegar a Arquitecto de Plataforma: desde Kubernetes hasta observabilidad, SRE, GitLab e inteligencia artificial.

SALOMÉ: La dinámica es sencilla. Muchas veces te vamos a describir cómo funciona algo y vamos a hacer una pausa corta. En esa pausa, tú dices en voz alta el nombre de la herramienta o del concepto. Después lo decimos nosotros y comparas.

GONZALO: Porque ya sabemos que el mecanismo lo entiendes bien. Lo que se te escapa a veces es el nombre. Y en una entrevista, el nombre es lo que demuestra que lo dominas.

SALOMÉ: Listo. Arranquemos con el panorama general, y después bajamos al detalle.

GONZALO: El plan tiene diez fases. Te las digo con tu nivel actual. Fase uno, Kubernetes, arquitectura y fundamentos: vas en sesenta y ocho por ciento dominado. Fase dos, IaC, o sea Infrastructure as Code, infraestructura como código: cincuenta y dos por ciento. Fase tres, CI/CD, que es Continuous Integration y Continuous Delivery, más GitOps: cuarenta y seis por ciento.

SALOMÉ: Fase cuatro, identidad: sesenta y ocho por ciento. Fase cinco, networking y seguridad: setenta y tres. Fase seis, datos y secretos: setenta y seis. Fase siete, observabilidad y orquestación asíncrona: setenta y tres. Fase ocho, troubleshooting de Kubernetes: cien por ciento, nivel senior. Fase nueve, arquitectura de plataforma: cincuenta y cinco. Y la fase diez, certificación y entrevista final, todavía sin empezar.

GONZALO: En promedio llevas cerca de ochenta y nueve por ciento visto y sesenta por ciento dominado. Son dos números distintos a propósito: uno mide cobertura, el otro mide qué tan defendible es lo que ya viste.

SALOMÉ: Bueno, empecemos por Kubernetes.

## Bloque 1 — Kubernetes

GONZALO: Primera pregunta. En Kubernetes hay un mecanismo que compara todo el tiempo el estado deseado, lo que declaraste en el YAML, con el estado real del clúster, y corrige la diferencia. ¿Cómo se llama ese ciclo?

[PAUSA 4]

SALOMÉ: Es el reconciliation loop, el ciclo de reconciliación. Lo ejecutan los controladores del control plane. El reconciliation loop es la idea central de Kubernetes, y también es la idea central de GitOps, que veremos más adelante.

GONZALO: Ahora, troubleshooting, tu tema estrella. Un contenedor se pasa del límite de memoria que le pusiste, y el kernel lo mata. El código de salida es ciento treinta y siete. ¿Qué estado ves?

[PAUSA 4]

SALOMÉ: OOMKilled. OOM significa Out Of Memory, sin memoria. OOMKilled pasa por el límite del contenedor.

GONZALO: Y ojo con el matiz que tú distinguiste sin ayuda: si no es el contenedor sino el nodo completo el que se queda sin memoria o sin disco, y el kubelet saca Pods para salvar el nodo, ¿cómo se llama eso?

[PAUSA 4]

SALOMÉ: Evicted. OOMKilled es el límite del contenedor; Evicted es la presión del nodo completo. Muchos los confunden; tú no.

GONZALO: Y si la aplicación arranca, falla, Kubernetes la reinicia, vuelve a fallar, y cada vez espera más tiempo entre reinicios?

[PAUSA 3]

SALOMÉ: CrashLoopBackOff. Y si Kubernetes no logra descargar la imagen, por un tag mal escrito o por credenciales del registry, es ImagePullBackOff.

GONZALO: Un dato más: el código ciento cuarenta y tres corresponde a SIGTERM, la terminación ordenada, la terminación graceful. Ciento treinta y siete es SIGKILL, que es lo que pasa en un OOMKilled.

## Bloque 2 — Infraestructura como código

SALOMÉ: Pasemos a IaC, infraestructura como código. En Terraform hay un archivo donde Terraform guarda lo que cree que existe en la nube, para comparar con tu código. ¿Cómo se llama?

[PAUSA 3]

GONZALO: El state file, el archivo de estado de Terraform. Y cuando dos personas corren Terraform al mismo tiempo, el state file se protege con locking. En AWS, el backend clásico es S3 para guardar el state file, más DynamoDB para el lock. En Azure es Blob Storage, y en Google Cloud es GCS, Google Cloud Storage.

SALOMÉ: Y cuando alguien cambia un recurso a mano en la consola, y la nube ya no coincide con el state file de Terraform, ¿cómo se llama esa diferencia?

[PAUSA 3]

GONZALO: Drift. Drift es la deriva entre el código y la realidad. Y si el recurso ya existía y quieres que Terraform lo adopte sin recrearlo, usas terraform import.

SALOMÉ: Ahora Ansible. Ansible no instala ningún agente en los servidores; se conecta por SSH. ¿Cómo se describe esa arquitectura?

[PAUSA 3]

GONZALO: Agentless, sin agente. Y en Ansible, cuando una tarea no tuvo que cambiar nada porque el servidor ya estaba en el estado deseado, el resultado es ok. Si sí cambió algo, el resultado es changed. Esa propiedad, que correr el playbook dos veces deja el mismo resultado, se llama idempotencia.

SALOMÉ: Y el hueco real de esta fase, para que lo tengas presente: Bicep, CloudFormation y CDK, que es Cloud Development Kit, todavía no se han tocado.

## Bloque 3 — CI/CD y GitOps

GONZALO: CI/CD. En el modelo tradicional, el pipeline empuja el despliegue al clúster. En el otro modelo, un agente que vive dentro del clúster mira el repositorio Git y jala los cambios. ¿Cómo se llama ese modelo, y cuál es la herramienta típica?

[PAUSA 4]

SALOMÉ: GitOps, el modelo pull. Y la herramienta típica es ArgoCD, que vive dentro del clúster. Ojo con eso: ArgoCD vive en el clúster, no en el pipeline. Otra herramienta del mismo modelo es Flux.

GONZALO: Ahora, el pipeline necesita autenticarse contra la nube sin guardar una contraseña ni una llave fija. El proveedor de CI emite un token firmado de corta duración, y la nube lo cambia por credenciales temporales. ¿Cómo se llama el estándar?

[PAUSA 3]

SALOMÉ: OIDC, OpenID Connect. Autenticación sin secretos fijos, en dos pasos: el token de identidad de OIDC, y luego el intercambio por credenciales temporales.

## Bloque 4 — Identidad

GONZALO: Identidad. En Azure, una aplicación necesita una identidad propia para acceder a otros servicios sin contraseñas. ¿Cómo se llama? ¿Y su equivalente en AWS? ¿Y en Google Cloud?

[PAUSA 5]

SALOMÉ: En Azure es Managed Identity. En AWS es IAM Role, donde IAM significa Identity and Access Management. Y en Google Cloud es Service Account. Managed Identity, IAM Role, Service Account. El eje que tú corregiste es el ciclo de vida: si la identidad muere con el recurso o si se puede compartir entre varios.

GONZALO: Y cuando un Pod de Kubernetes en EKS, Elastic Kubernetes Service, asume un IAM Role de AWS usando la federación OIDC del clúster, ¿cómo se llama eso?

[PAUSA 3]

SALOMÉ: IRSA, IAM Roles for Service Accounts. Ese lo cerraste completo sin ayuda.

GONZALO: Y si una empresa quiere un solo inicio de sesión para muchas aplicaciones, con Realms, Clients y federación de usuarios desde un directorio, la herramienta open source que viste fue...

[PAUSA 3]

SALOMÉ: Keycloak. Un Realm en Keycloak es un espacio aislado de usuarios; un Client es la aplicación que confía en Keycloak; y el resultado es SSO, Single Sign-On.

## Bloque 5 — Networking y seguridad

GONZALO: Networking. Quieres que tu aplicación se conecte a una base de datos administrada sin pasar por internet, con una IP privada dentro de tu red. En Azure, ¿cómo se llama? ¿Y en AWS? ¿Y en Google Cloud?

[PAUSA 5]

SALOMÉ: En Azure, Private Endpoint. En AWS, PrivateLink. En Google Cloud, Private Service Connect.

GONZALO: Y si tu servidor está en una subred privada y necesita salir a internet a descargar parches, pero nadie de afuera debe poder entrar, ¿qué pones?

[PAUSA 3]

SALOMÉ: Un NAT Gateway, Network Address Translation Gateway. Y recuerda la regla que razonaste bien: importa quién inicia la conexión. El Load Balancer recibe el tráfico que entra; el NAT Gateway resuelve el tráfico que sale. No son lo mismo.

GONZALO: Ahora seguridad. Una herramienta escanea tus imágenes de contenedor buscando vulnerabilidades conocidas, los CVE, Common Vulnerabilities and Exposures, antes de desplegar. Esta te costó el nombre la última vez. ¿Cuál es?

[PAUSA 4]

SALOMÉ: Trivy. T, R, I, V, Y. Trivy. No "Stribi": Trivy. Trivy es el ejemplo clásico de shift-left security, mover la seguridad a la izquierda, temprano en el pipeline.

GONZALO: Y si quieres prohibir en el clúster, con políticas escritas como código, que alguien despliegue un contenedor como root o sin límites de recursos, ¿qué usas?

[PAUSA 4]

SALOMÉ: OPA Gatekeeper. OPA es Open Policy Agent, y Gatekeeper es su integración como admission controller en Kubernetes. Policy as code.

## Bloque 6 — Datos y secretos

GONZALO: Datos y secretos. La aplicación necesita la contraseña de la base de datos, pero no quieres esa contraseña en el código ni en variables de entorno sueltas. ¿Dónde la guardas en Azure, en AWS y en Google Cloud?

[PAUSA 5]

SALOMÉ: Azure Key Vault, AWS Secrets Manager y Google Secret Manager. Y la síntesis completa que tú cerraste sin ayuda es esta: la aplicación usa su Managed Identity o su IAM Role, con eso lee el secreto de Key Vault o Secrets Manager, y se conecta a la base de datos por Private Endpoint o PrivateLink. Cero secretos expuestos.

GONZALO: En bases de datos como Cosmos DB o DynamoDB, a veces lees un dato y no ves todavía la última escritura, pero eventualmente sí. Eso se llama consistencia...

[PAUSA 3]

SALOMÉ: Consistencia eventual. Lo opuesto es consistencia fuerte. Cosmos DB, de Azure, tiene cinco niveles entre esos dos extremos.

## Bloque 7 — Mensajería y orquestación

GONZALO: Mensajería. En una cola tradicional como SQS, Simple Queue Service, cuando un consumidor procesa el mensaje, el mensaje desaparece. Pero hay otra herramienta donde los eventos quedan guardados en un log, varios consumidores independientes los leen cada uno a su ritmo, y puedes volver a leerlos desde el principio. ¿Cuál es?

[PAUSA 3]

SALOMÉ: Kafka, o su alternativa compatible Redpanda. Log retenido, múltiples consumidores, y replay. Y recuerda: Kafka escala mejor, no peor.

GONZALO: Ahora un patrón que conectaste con tu propia experiencia. Guardas el cambio en la base de datos y, en la misma transacción, guardas el evento en una tabla aparte. Después, un proceso lee esa tabla y publica el evento. Así nunca queda el dato guardado sin su evento. ¿Cómo se llama el patrón?

[PAUSA 4]

SALOMÉ: Transactional Outbox. Tu caso real fue RDS, más SNS, más SQS.

GONZALO: Y en Azure, si necesitas orquestar varios pasos en serverless, con un orquestador que se vuelve a ejecutar desde el historial, y actividades que el framework garantiza que se ejecutan una sola vez, ¿qué usas?

[PAUSA 3]

SALOMÉ: Durable Functions. El orchestrator hace replay del historial, y cada activity queda registrada para no repetirse.

## Bloque 8 — SRE: confiabilidad

GONZALO: Ahora el bloque que trabajaste para la prueba de Davivienda: SRE, Site Reliability Engineering. Primero, tres siglas parecidas. La medición real, por ejemplo el porcentaje de peticiones exitosas, es el...

[PAUSA 3]

SALOMÉ: SLI, Service Level Indicator.

GONZALO: La meta interna que se pone el equipo, por ejemplo noventa y nueve coma nueve por ciento, es el...

[PAUSA 3]

SALOMÉ: SLO, Service Level Objective.

GONZALO: Y el compromiso contractual con el cliente, con penalidades, es el...

[PAUSA 3]

SALOMÉ: SLA, Service Level Agreement. Y aquí está el error que cometiste: el SLA es más flojo que el SLO, no al revés. El SLO interno es más estricto, para tener margen antes de violar el SLA con el cliente.

GONZALO: Las cuatro señales de oro de Google para monitorear un servicio. Intenta decir las cuatro.

[PAUSA 6]

SALOMÉ: Latency, latencia. Traffic, tráfico. Errors, errores. Saturation, saturación. La mnemotecnia es "LaTES": La, de Latency; T, de Traffic; E, de Errors; S, de Saturation. Golden Signals.

GONZALO: Si tu SLO es noventa y nueve coma nueve, ese cero coma uno por ciento que te sobra es lo que puedes fallar sin violar la meta. ¿Cómo se llama ese margen?

[PAUSA 3]

SALOMÉ: Error Budget, el presupuesto de errores. Y la velocidad a la que te lo estás gastando se llama burn rate. Las alertas buenas son multi-window, multi-burn-rate: varias ventanas de tiempo y varias velocidades de gasto.

GONZALO: Y el documento que dice qué hace el equipo cuando el Error Budget se acaba, por ejemplo congelar despliegues de funcionalidades nuevas, ¿cómo se llama? Este no te salió la última vez.

[PAUSA 4]

SALOMÉ: Error Budget Policy. No SLA: Error Budget Policy. La mnemotecnia era la política de gastos de una empresa.

GONZALO: Y la herramienta que hace canary automático en Kubernetes, subiendo tráfico de a poco y revirtiendo si las métricas empeoran. Hay dos nombres: uno es Argo Rollouts. ¿Y el otro?

[PAUSA 4]

SALOMÉ: Flagger. Argo Rollouts y Flagger. Eso es progressive delivery.

GONZALO: Ahora dos siglas de recuperación ante desastres. El tiempo máximo que puedes estar caído es el...

[PAUSA 3]

SALOMÉ: RTO, Recovery Time Objective.

GONZALO: Y la cantidad máxima de datos que puedes perder, medida en tiempo hacia atrás, es el...

[PAUSA 3]

SALOMÉ: RPO, Recovery Point Objective. RTO es tiempo de recuperación; RPO es pérdida de datos. Ninguno de los dos es el SLA.

## Bloque 9 — Observabilidad con OpenTelemetry

GONZALO: Observabilidad. El estándar abierto para métricas, logs y trazas es OpenTelemetry. Y el proceso intermedio que recibe la telemetría, la filtra, la transforma y la envía a Datadog o a Grafana es el OpenTelemetry Collector. Dentro del Collector hay cuatro tipos de componentes. El que recibe los datos es el...

[PAUSA 3]

SALOMÉ: Receiver.

GONZALO: El que filtra, enmascara o agrupa en el medio es el...

[PAUSA 3]

SALOMÉ: Processor.

GONZALO: El que envía al destino final es el...

[PAUSA 3]

SALOMÉ: Exporter.

GONZALO: Y el que convierte una señal en otra, por ejemplo trazas en métricas, es el...

[PAUSA 3]

SALOMÉ: Connector. Regla aprendida: si cambia de señal, es un connector. Receiver, processor, exporter, connector. Y el processor que va primero de todos, para que el Collector no se caiga por falta de memoria, es el memory limiter.

GONZALO: Los puertos de OTLP, OpenTelemetry Protocol. Este también se te escapó. gRPC y HTTP. ¿Qué números?

[PAUSA 4]

SALOMÉ: Cuatro tres uno siete para gRPC, y cuatro tres uno ocho para HTTP. Cuatro tres uno siete y cuatro tres uno ocho.

GONZALO: Muestreo. Si decides si guardas una traza apenas empieza, sin saber si va a fallar, es head-based sampling. Si esperas a que termine para quedarte con las que tuvieron errores o fueron lentas, es...

[PAUSA 3]

SALOMÉ: Tail-based sampling. El tail sampling es el que conserva los errores. Y como necesita ver todos los spans de una misma traza en el mismo lugar, se usa un gateway de dos capas, con el exporter de loadbalancing por traceID.

GONZALO: Y la cabecera estándar del W3C que viaja entre servicios para que todos sepan a qué traza pertenecen, ¿cómo se llama?

[PAUSA 3]

SALOMÉ: traceparent. La anterior, de Zipkin, es B3. Y en Kafka, la traza viaja en los headers del mensaje, no llamando al productor.

GONZALO: Y cuando una métrica tiene demasiadas combinaciones de etiquetas, por ejemplo poner el ID de usuario como label, y el costo se dispara, eso se llama...

[PAUSA 3]

SALOMÉ: Explosión de cardinalidad. Y para recortar costos de telemetría, recortar la retención a la mitad es una mala señal. Mejor Log-to-Metrics y tail sampling.

## Bloque 10 — Incidentes y operación

GONZALO: Incidentes. Cuando un servicio está saturado y empiezas a rechazar a propósito parte de las peticiones para que el resto funcione, ¿cómo se llama?

[PAUSA 3]

SALOMÉ: Load shedding, deslastre de carga. Y cuando una dependencia está fallando y dejas de llamarla por un tiempo para no empeorar las cosas, es el circuit breaker, como un taco eléctrico. Tu idea del "bypass" en tuberías de gas es graceful degradation.

GONZALO: El trabajo manual, repetitivo, que no aporta valor duradero y crece con el sistema, en SRE se llama...

[PAUSA 3]

SALOMÉ: Toil. No es carga cognitiva: es toil.

GONZALO: Y la herramienta de Netflix que apaga servidores al azar en producción para probar la resiliencia...

[PAUSA 3]

SALOMÉ: Chaos Monkey. La disciplina es Chaos Engineering. Y los Game Days son simulacros planeados de fallas, no pruebas de carga.

## Bloque 11 — Platform Engineering

GONZALO: Platform Engineering. El portal donde los desarrolladores piden recursos por autoservicio, de Spotify, open source, es...

[PAUSA 3]

SALOMÉ: Backstage. Backstage es la cara de un IDP, Internal Developer Platform. Y el camino recomendado y pavimentado para crear un servicio nuevo se llama golden path.

GONZALO: Y un ataque de API donde el usuario cambia el ID en la URL y ve los datos de otro cliente, el número uno de OWASP API, Open Worldwide Application Security Project...

[PAUSA 3]

SALOMÉ: BOLA, Broken Object Level Authorization. Y recuerda: correr el contenedor sin root no previene BOLA; solo limita el daño.

## Bloque 12 — GitLab y Service Accounts

GONZALO: GitLab. La mnemotecnia para saber quién crea las Service Accounts era "AI y GO". ¿Qué significa?

[PAUSA 4]

SALOMÉ: Admin, Instancia; Grupo, Owner. El Admin crea las Service Accounts de instancia, y el Owner del grupo crea las de grupo. Y en self-managed, el Admin puede crear las dos.

GONZALO: Los roles numéricos de la API de GitLab: diez, veinte, treinta, cuarenta y cincuenta.

[PAUSA 5]

SALOMÉ: Diez es Guest. Veinte es Reporter. Treinta es Developer. Cuarenta es Maintainer. Cincuenta es Owner.

GONZALO: Y las cinco fases del plan de migración a Service Accounts. Intenta decirlas en orden.

[PAUSA 6]

SALOMÉ: Inventario, Diseño, Piloto, Olas y Gobierno. Inventario, Diseño, Piloto, Olas, Gobierno. El piloto lo explicaste perfecto: bajo impacto y reversible.

## Bloque 13 — Inteligencia artificial

GONZALO: Inteligencia artificial. Cuando el modelo, antes de responder, busca documentos relevantes en tu base de conocimiento y los mete en el prompt, se llama...

[PAUSA 3]

SALOMÉ: RAG, Retrieval-Augmented Generation. Y la búsqueda por significado, no por palabras exactas, funciona con vectores numéricos llamados embeddings, guardados en una base de datos vectorial.

GONZALO: Y si en vez de buscar documentos, ajustas los pesos del modelo con tus propios datos de entrenamiento...

[PAUSA 3]

SALOMÉ: Fine-tuning. Primero viene el pre-entrenamiento, con datos masivos; el fine-tuning es el ajuste después.

## Bloque 14 — Las cuatro listas pendientes

GONZALO: Y llegamos a lo más importante del episodio: las cuatro listas que siguen sin salirte de memoria. Aquí la pausa es más larga. Intenta recitar cada lista completa antes de que la digamos.

SALOMÉ: Primera lista. Las métricas que miden el desempeño de entrega de software de un equipo, dos de velocidad y dos de estabilidad. Primero, ¿cómo se llama el marco? Y después, las cuatro.

[PAUSA 10]

GONZALO: Métricas DORA, DevOps Research and Assessment. Las cuatro: Deployment Frequency, frecuencia de despliegue. Lead Time for Changes, tiempo desde el commit hasta producción. Change Failure Rate, porcentaje de cambios que fallan. Y Time to Restore Service, tiempo para restaurar el servicio.

SALOMÉ: La mnemotecnia es "DeLiCaTe": De, de Deployment Frequency; Li, de Lead Time; Ca, de Change Failure Rate; Te, de Time to Restore. Reliability no es una de las cuatro, y "stability" es el nombre de la categoría, no de una métrica.

GONZALO: Repito, despacio: Deployment Frequency. Lead Time for Changes. Change Failure Rate. Time to Restore Service. DeLiCaTe.

SALOMÉ: Segunda lista. El marco de AWS para evaluar una arquitectura tiene seis pilares. Recítalos todos.

[PAUSA 12]

GONZALO: Well-Architected Framework. Los seis pilares: Operational Excellence, excelencia operacional. Security, seguridad. Reliability, confiabilidad. Performance Efficiency, eficiencia de desempeño. Cost Optimization, optimización de costos. Y Sustainability, sostenibilidad.

SALOMÉ: La mnemotecnia es "Seguro, Confiable, Rápido, Barato, Operable y Verde". Seguro es Security. Confiable es Reliability. Rápido es Performance Efficiency. Barato es Cost Optimization. Operable es Operational Excellence. Verde es Sustainability. Y ojo: Key Vault, mínimo privilegio o WAF son buenas prácticas dentro de un pilar, no son pilares.

GONZALO: Otra vez: Operational Excellence. Security. Reliability. Performance Efficiency. Cost Optimization. Sustainability.

SALOMÉ: Tercera lista. Los seis principios de IA Responsable de Microsoft. Esta lleva dos fallas seguidas. Inténtalo.

[PAUSA 12]

GONZALO: Fairness, equidad. Reliability and Safety, confiabilidad y seguridad. Privacy and Security, privacidad y seguridad. Inclusiveness, inclusión. Transparency, transparencia. Y Accountability, responsabilidad.

SALOMÉ: Repito: Fairness. Reliability and Safety. Privacy and Security. Inclusiveness. Transparency. Accountability.

GONZALO: Cuarta lista. Las cinco áreas del examen Claude Certified Architect, con su peso en porcentaje.

[PAUSA 12]

SALOMÉ: Uno: Arquitectura y Orquestación Agéntica, veintisiete por ciento. Dos: Configuración y Workflows de Claude Code, veinte por ciento. Tres: Diseño de Tools e Integración MCP, Model Context Protocol, dieciocho por ciento. Cuatro: Prompt Engineering y Structured Output, veinte por ciento. Cinco: Gestión de Contexto y Confiabilidad, quince por ciento.

GONZALO: Las que nunca te han salido son Prompt Engineering y Structured Output, y Gestión de Contexto y Confiabilidad. Y recuerda que cada área por separado la dominas; lo que falta es la lista como lista.

## Cierre

SALOMÉ: Hagamos el resumen de lo que más tienes que repasar. Uno: las métricas DORA, DeLiCaTe. Dos: los seis pilares de Well-Architected. Tres: los seis principios de IA Responsable. Cuatro: las cinco áreas del examen Claude Certified Architect.

GONZALO: Y de nombres sueltos: Trivy, Error Budget Policy, Flagger, los puertos cuatro tres uno siete y cuatro tres uno ocho, RTO y RPO, toil y Chaos Monkey.

SALOMÉ: Lo que tienes sólido, y lo puedes defender en una entrevista: troubleshooting de Kubernetes, la cadena Managed Identity, Key Vault y Private Endpoint, IRSA, Kafka frente a SQS con Transactional Outbox, y BOLA.

GONZALO: El próximo paso del plan: la fase diez, certificación y entrevista final, y los huecos de Bicep, CloudFormation, GitLab CI y el modelo C4.

SALOMÉ: Gracias por escuchar, Sebastián. Nos oímos en el próximo episodio.
