# Beneficios de usar Docker desde el desarrollo hasta producción

Para mí el beneficio más grande de Docker es que el servicio se empaqueta una sola vez, con todo lo que necesita para correr (código, runtime, librerías y configuración), y esa misma imagen es la que pasa por todas las etapas. Así se acaba el clásico "en mi máquina funciona", porque lo que corre en mi portátil es lo mismo que corre en QA y en producción.

Lo veo por etapas:

**En desarrollo**, cualquier persona del equipo puede levantar el servicio y sus dependencias (base de datos, caché, colas) con un `docker compose up`, sin instalar nada en su máquina ni pelear con versiones. Eso hace que alguien nuevo sea productivo el primer día. Además puedo probar contra versiones específicas de otros servicios sin ensuciar mi entorno. Lo viví en esta misma prueba: necesitaba un CentOS 7 para probar el playbook de Ansible y en vez de montar una máquina virtual lo levanté en un contenedor en un par de minutos.

**En integración continua (CI)**, el pipeline construye la imagen, corre las pruebas dentro de ella y la publica en un registry con una versión (tag). Las pruebas se hacen sobre el mismo artefacto que va a salir a producción, no sobre algo parecido.

**En producción**:
- **Despliegues y rollbacks rápidos:** desplegar es cambiar la imagen por la versión nueva, y si algo falla vuelvo a la anterior en segundos porque sigue guardada en el registry.
- **Escalabilidad:** los contenedores arrancan en segundos y pesan poco comparados con una VM, entonces es fácil escalar horizontalmente, sobre todo con un orquestador como Kubernetes o ECS.
- **Aislamiento y mejor uso de recursos:** varios servicios pueden compartir el mismo servidor sin chocar entre sí (cada uno con sus dependencias), y se les puede limitar CPU y memoria.
- **Infraestructura como código:** el Dockerfile documenta exactamente cómo se construye el servicio, queda versionado en git y se puede revisar como cualquier otro código.

También hay que tener cuidado con algunas cosas: mantener las imágenes livianas y actualizadas, escanearlas por vulnerabilidades, no guardar secretos dentro de la imagen y no correr los procesos como root si no hace falta. Pero bien manejado, Docker hace que el camino de desarrollo a producción sea mucho más predecible, rápido y repetible.
