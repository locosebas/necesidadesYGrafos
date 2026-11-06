# Libreto de diapositivas - Entrevista Niuro (AWS Infrastructure Engineer)

Plan de la presentación para repasar la entrevista. Cada diapositiva tiene:

- `Sección`: a qué pregunta pertenece.
- `Diagrama`: el o los diagramas de [diagramas-c4.md](diagramas-c4.md).
- Viñetas: lo que se ve en pantalla.
- `>` guion: lo que dices en voz alta. En la presentación aparece al oprimir **N** (notas).

La presentación [presentacion.html](presentacion.html) se genera con
`python3 generar_presentacion.py` a partir de este archivo y del de diagramas. Si cambias algo aquí,
vuelve a correr el generador.

Regla de oro de toda la presentación (corrección del 5 nov 2026): en **Bizagi y en MercadoLibre**
no había dev; había **stage** y **varios ambientes de producción**, stage iba **unos días antes**, y
para pasar a producción había que **demostrar que stage estaba sano**. Y siempre **build once, deploy
anywhere**: primero se crea la versión, después se despliega esa misma versión.

---

## Entrevista Niuro · AWS Infrastructure Engineer
**Sección:** Portada
- Repaso de las 9 preguntas de la entrevista del 5 nov 2026
- Diagramas C4 (Context, Containers, Components, Code) por respuesta
- Teclas: ← → para moverse · N para ver el guion

> Esta presentación es para estudiar. La idea es que cada diagrama te sirva de mapa mental: si recuerdas el dibujo, recuerdas la respuesta.

---

## Regla de oro: ambientes y versiones
**Sección:** Antes de empezar
- **Sin dev**: stage + varios ambientes de producción
- **Stage va unos días antes** que producción
- Para pasar a producción hay que **demostrar que stage está sano**
- **Build once, deploy anywhere**: crear la versión una vez → desplegar esa misma versión donde haga falta
- Aplica a **Bizagi** y a **MercadoLibre**

> En las dos empresas el flujo era igual: un paso crea la versión, el artefacto, y otro paso la despliega. Primero en stage, se deja correr unos días, se muestra que no hay problemas, y solo ahí va a los ambientes de producción. Nunca se recompila por ambiente.

---

## 1 · Presentación y rol actual
**Sección:** Pregunta 1
**Diagrama:** D1
- **MercadoLibre** (jun 2024 – ago 2026): Software Developer (DevOps), línea bancaria **Mercado Pago**
- AWS y GCP con **Terraform**, cargas en **ECS** y **Kubernetes**, postmortems
- **Bizagi** (ene 2022 – jun 2024): DevOps Engineer en **Azure**, CI/CD, release management
- Disponible de inmediato

> Soy ingeniero DevOps y de infraestructura cloud con unos cinco años de experiencia. Hasta agosto de 2026 estuve en MercadoLibre, en el equipo DevOps de Mercado Pago: infraestructura en AWS y GCP con Terraform, cargas en Kubernetes y ECS, y análisis de causa raíz. Antes estuve dos años y medio en Bizagi como DevOps Engineer, con Azure, CI/CD en Azure Pipelines y Jenkins, y release management. Hoy estoy disponible de inmediato.

---

## 2 · Cargas sensibles en AWS: el contexto
**Sección:** Pregunta 2
**Diagrama:** D2a
- Cargas financieras de **Mercado Pago**: aislamiento y menor privilegio
- Todo aprovisionado con **módulos de Terraform** con línea base segura
- Secretos desde un **gestor de secretos**, nunca en código ni imágenes
- **Recuperación ante desastres** entre regiones

> Mercado Pago maneja datos financieros, así que la arquitectura giraba en torno a dos ideas: aislamiento y mínimo privilegio. El cliente entra por HTTPS a servicios en contenedores, el equipo DevOps solo cambia la infraestructura por pull request con Terraform, y los secretos se leen en tiempo de ejecución.

---

## 2 · Cargas sensibles en AWS: los contenedores
**Sección:** Pregunta 2
**Diagrama:** D2b
- **Red:** subred pública solo con el ALB (Application Load Balancer); app y datos en privadas
- **Cómputo:** ECS (Elastic Container Service) y Kubernetes, **un rol de IAM (Identity and Access Management) por servicio**
- **Datos:** cifrado en reposo con **KMS (Key Management Service)** y TLS (Transport Layer Security) en tránsito
- Terraform: estado remoto con bloqueo, **plan revisado antes del apply**

> En la red, en la subred pública solo estaban los balanceadores, y los contenedores y las bases de datos en subredes privadas. Cada servicio tenía su propio rol de IAM limitado a lo que necesitaba. Cifrado con KMS en reposo y TLS en tránsito. Y en el día a día hacía hardening y remediación de vulnerabilidades en IAM, cifrado y segmentación de red.

---

## 3 · Blue/green con cambios de esquema: el problema
**Sección:** Pregunta 3
**Diagrama:** D3a
- Blue y green **comparten la misma base de datos**
- El esquema tiene que servirle **a las dos versiones a la vez**
- Las migraciones van **versionadas en el pipeline**, separadas del deploy
- Solo cambios **aditivos** mientras las dos versiones conviven

> El riesgo es que green necesite un esquema que rompa a blue. Como las dos versiones comparten la base de datos, el esquema tiene que ser compatible con ambas mientras conviven. Por eso las migraciones se ejecutan antes del deploy y solo agregan, nunca borran ni renombran.

---

## 3 · Expand/contract en cinco fases
**Sección:** Pregunta 3
**Diagrama:** D3b
- **1 Expand:** agregar columnas nulas o con default, tablas nuevas
- **2 Deploy green:** doble escritura, lectura con fallback
- **3 Backfill:** histórico en lotes pequeños
- **4 Switch:** tráfico a green, rollback a blue seguro
- **5 Contract:** borrar lo viejo en un release posterior
- Regla: **nunca un cambio destructivo en el mismo release que lo necesita**

> El patrón se llama expand/contract, o parallel change. Primero expando, después despliego green que escribe en las dos estructuras, migro el histórico en lotes, paso el tráfico, y solo cuando blue ya no existe, contraigo. Herramientas del tipo Flyway o Liquibase versionan las migraciones; ojo, no digas que las usaste en MercadoLibre. Para cambios grandes, feature flags; en tablas grandes, índices concurrentes para no bloquear.

---

## 4 · Terraform: módulos, ambientes y estado
**Sección:** Pregunta 4
**Diagrama:** D4a
- **Módulos** pequeños y **versionados con tags**; cada ambiente fija su versión
- Ambientes: **stage + varios de producción** (sin dev), **cada uno con su estado**
- Estado en **S3** con versionado, cifrado y acceso por IAM + **bloqueo** (DynamoDB o lock nativo de S3)
- Estado **dividido por componente** para reducir el **blast radius** (radio de impacto)

> Los módulos son pequeños, cada uno con una responsabilidad, y versionados con tags, así que un cambio en un módulo no llega a producción hasta que alguien sube la versión a propósito. Teníamos stage y varios ambientes de producción, cada uno con su propio estado en S3, cifrado y con bloqueo. Dividir el estado por componente reduce el blast radius y hace los plan más rápidos.

---

## 4 · Terraform: cómo se promueve un cambio
**Sección:** Pregunta 4
**Diagrama:** D4b
- Nada se aplica desde la máquina de nadie: **pull request → plan → revisión → apply** por el pipeline
- Primero **stage**, unos días en observación
- Solo con **stage sano y con evidencia** se aplica en producción
- Lección real: en una migración remapeamos el estado con `terraform import` **sin downtime**

> El flujo era: pull request, el pipeline corre terraform plan, alguien lo revisa buscando destroys inesperados, y el pipeline hace el apply en stage. Se deja unos días, y si stage está sano lo promovemos a los ambientes de producción. En una migración tuvimos fallas de mapeo del estado y las resolvimos remapeando recursos, sin tiempo de inactividad.

---

## 5 · Pipeline .NET: build once, deploy anywhere
**Sección:** Pregunta 5
**Diagrama:** D5a
- **Crear versión:** `dotnet build` en Release + pruebas unitarias → **artefacto versionado, una sola vez**
- **Desplegar:** esa misma versión va a **stage** (pruebas de integración y de humo)
- Stage **unos días antes**; para pasar a producción hay que **mostrar que stage no tuvo problemas**
- Después, la misma versión a **producción 1 … N**
- Herramientas en Bizagi: **Azure Pipelines** y **Jenkins**

> En Bizagi la plataforma era .NET. El pipeline tenía dos momentos separados: crear la versión y desplegarla. Crear la versión es compilar en Release, correr las pruebas unitarias y guardar un artefacto versionado. Desplegar es tomar esa misma versión, llevarla a stage, dejarla unos días, demostrar que no hubo problemas, y después llevarla a los ambientes de producción. Nunca se recompila por ambiente.

---

## 5 · Despliegue sin tiempo de inactividad
**Sección:** Pregunta 5
**Diagrama:** D5b
- La versión nueva se levanta **en paralelo** a la actual
- **Health checks** y pruebas de humo antes de recibir tráfico
- **Rollback** = redesplegar la versión anterior, que sigue en el repositorio de artefactos
- **Grafana** con el onboarding automatizado que lideré: salud y logs desde el día 1

> La versión nueva se levanta al lado de la actual y solo recibe tráfico si pasa los health checks. Si falla, el tráfico se queda en la versión actual, y el rollback es simplemente redesplegar la versión anterior. No le pongas nombre a un mecanismo específico, como deployment slots, si no lo usaste.

---

## 6 · Imágenes Docker endurecidas
**Sección:** Pregunta 6
**Diagrama:** D6a
- **Multi-stage builds**: la imagen final solo lleva el binario
- Base **distroless o slim**, fijada por versión o digest (nunca `latest`)
- **Usuario no root**, sistema de archivos de solo lectura, sin capabilities extra
- **Cero secretos** en la imagen
- **Escaneo de vulnerabilidades**: una crítica bloquea el build

> Compilo en una etapa con todas las herramientas y la imagen final solo lleva lo necesario, así hay menos superficie de ataque. Base mínima fijada por digest, usuario no root y secretos inyectados en ejecución. El escáner corre en el pipeline y, si hay una vulnerabilidad crítica, el build no pasa. No nombres un escáner que no usaste; Trivy solo como ejemplo de la categoría.

---

## 6 · Límites de recursos y alertas de capacidad
**Sección:** Pregunta 6
**Diagrama:** D6b
- **Requests y limits** de CPU y memoria según el **uso medido**
- Memoria corta → **OOMKilled**
- **HPA (Horizontal Pod Autoscaler)** en Kubernetes o autoscaling de servicios en ECS
- Mis alertas en MercadoLibre: capa **reactiva** + capa **predictiva** + análisis con **LLM (Large Language Model)**

> Los requests los ajustaba con el uso real, no con estimaciones, y con la memoria tengo cuidado porque un límite corto termina en OOMKilled. Para los picos, autoescalado horizontal. Y en MercadoLibre construí alertas de utilización que marcaban sobreaprovisionamiento y riesgo de quedarse sin capacidad, con una capa reactiva, una predictiva entrenada con el histórico, y análisis con un LLM para los picos que la estacionalidad no explicaba.

---

## 7 · ECS: EC2 vs Fargate
**Sección:** Pregunta 7
**Diagrama:** D7a
- **Fargate:** cada tarea en su propio entorno aislado; **AWS parchea el host**
- **EC2 launch type:** tú eres dueño del host: AMI endurecida, parches, agentes, GPU
- **Capacity providers** permiten combinar los dos en el mismo clúster

> Con Fargate cada tarea tiene su propio entorno de cómputo aislado y no tengo que parchear el sistema operativo, eso lo hace AWS. Con EC2 tengo más control, pero también más responsabilidad: AMIs endurecidas, parches, escalado de instancias. Y con capacity providers puedo mezclar los dos según el servicio.

---

## 7 · Cómo decido entre EC2 y Fargate
**Sección:** Pregunta 7
**Diagrama:** D7b
- Cuatro criterios: **seguridad**, **requisitos técnicos**, **costo**, **carga operativa**
- Por defecto: **Fargate** para servicios financieros sensibles
- **EC2** solo con un requisito concreto: GPU, modo privilegiado, agentes en el host, o carga estable y grande con **Savings Plans**

> Para servicios financieros sensibles mi opción por defecto es Fargate, por el aislamiento por tarea y porque elimino la gestión del sistema operativo. Me paso a EC2 solo si hay un requisito de hardware, de control del host o de costo a gran escala.

---

## 8 · VPC en tres zonas para aislar las bases de datos
**Sección:** Pregunta 8
**Diagrama:** D8
- **Tres AZ (Availability Zones)**, tres capas de subredes por zona
- **Pública:** ALB + un **NAT Gateway por zona**
- **Privada de app:** sin IP pública, sale por NAT
- **Aislada de datos:** **RDS (Relational Database Service) Multi-AZ**, **sin ninguna ruta a internet**
- Encima: **VPC Endpoints**, **VPC Flow Logs**, **SSM Session Manager** en vez de bastión

> Tres zonas de disponibilidad, tres capas por zona. En las públicas solo el ALB y un NAT Gateway por zona, para no tener un punto único de falla. Las tareas en subredes privadas. Y las bases de datos en subredes aisladas, cuya tabla de rutas no tiene ninguna ruta a internet, ni siquiera por NAT. Los servicios de AWS se consumen por VPC Endpoints, el tráfico se audita con Flow Logs y el acceso administrativo va por SSM Session Manager.

---

## 9 · Security groups encadenados (menor privilegio)
**Sección:** Pregunta 9
**Diagrama:** D9
- Se **referencian security groups entre sí**, no rangos de IP
- **sg-alb:** entra 443; sale solo al puerto de la app hacia sg-app
- **sg-app:** entra solo desde sg-alb (incluye health checks)
- **sg-db:** entra solo el puerto del motor desde sg-app
- Un SG por rol, todo en **Terraform**, auditoría con **AWS Config** o **Security Hub**
- TLS terminado en el ALB con **ACM (AWS Certificate Manager)**

> La clave es referenciar security groups entre sí en vez de usar IPs. El ALB acepta 443 y solo puede hablar con el backend; el backend solo acepta tráfico del ALB; la base de datos solo acepta tráfico del backend. Así cada salto solo acepta al salto anterior, y comprometer un servicio no abre el camino a los demás.

---

## Nombres clave para repasar
**Sección:** Cierre
- Expand/contract (parallel change) · feature flags · backfill
- Remote state en S3 + locking · blast radius · `terraform import`
- **Build once, deploy anywhere** · stage → producción 1 … N
- Multi-stage builds · distroless · OOMKilled · HPA
- Fargate vs EC2 launch type · capacity providers · Savings Plans
- NAT Gateway por AZ · subredes aisladas · NACLs (Network Access Control Lists) · VPC Endpoints · Flow Logs · SSM Session Manager
- Security groups encadenados · ACM · AWS Config / Security Hub

> Para el repaso: yo te describo el mecanismo y tú dices el nombre. Por ejemplo: "un patrón que primero agrega columnas compatibles y después borra lo viejo en otro release". La respuesta es expand/contract.
