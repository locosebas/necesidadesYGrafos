# Entrevista con IA - Niuro: AWS Infrastructure Engineer

Entrevista con un entrevistador de IA ("Casey"), 5 nov 2026. Cargo: **AWS Infrastructure Engineer**.
Temas: arquitectura en AWS para cargas sensibles, Terraform, blue/green con cambios de esquema,
CI/CD (.NET), endurecimiento de contenedores, ECS EC2 vs Fargate, VPC multi-AZ y security groups.

Resultado según Sebastián: **salió bien**. Si llega una **segunda entrevista de Niuro**, se estudia
este archivo primero.

> ⚠️ **Corrección importante (dicha por Sebastián después de la entrevista).** En las respuestas hubo
> una confusión sobre ambientes y modos de despliegue. Lo real, en **Bizagi y en MercadoLibre**:
>
> - **No había ambiente dev.** Había **stage** y **varios ambientes de producción**.
> - **Stage se desplegaba unos días antes que producción**, y para poder pasar a producción había que
>   **demostrar que en stage no había problemas**.
> - **Build once, deploy anywhere** en las dos empresas: siempre hay un paso que **crea una versión**
>   (el artefacto), y después esa misma versión **se despliega** en el ambiente o los ambientes que
>   hagan falta. Nunca se recompila por ambiente.
>
> Las respuestas de abajo ya están corregidas con esto.

## Material de estudio

- [diagramas-c4.md](diagramas-c4.md): 15 diagramas C4 (uno o más por pregunta), con íconos de las herramientas.
- [libreto-diapositivas.md](libreto-diapositivas.md): plan de las 18 diapositivas, con el guion de cada una.
- [presentacion.html](presentacion.html): la presentación (← → para navegar, **N** para ver el guion). Versión para el celular (privada): https://claude.ai/artifact/MpZn3j577bAmoYpbWqC3jg
  Se regenera con `python3 generar_presentacion.py` después de editar el libreto o los diagramas.

## Nombres clave para repasar

Expand/contract (parallel change) · Flyway / Liquibase (solo como ejemplo, no usados) · feature flags ·
remote state en S3 + locking (DynamoDB o lock nativo de S3) · blast radius · `terraform import` /
movimientos de estado · build once, deploy anywhere · multi-stage builds · distroless · OOMKilled ·
HPA (Horizontal Pod Autoscaler) · capacity providers · Fargate vs EC2 launch type · NAT Gateway por AZ ·
subredes aisladas · security groups encadenados (referencia por SG, no por IP) · NACLs · VPC Endpoints
(PrivateLink) · VPC Flow Logs · SSM Session Manager · ACM (AWS Certificate Manager).

## 1. Presentación y rol actual

"Soy ingeniero DevOps y de infraestructura cloud, con unos cinco años de experiencia. Hasta agosto de
2026 trabajé en MercadoLibre como Software Developer en el equipo DevOps, dándole soporte a Mercado
Pago, la línea bancaria: infraestructura en AWS y GCP con Terraform, cargas en Kubernetes y ECS,
análisis de causa raíz y postmortems. Antes, dos años y medio en Bizagi como DevOps Engineer: Azure,
CI/CD con Azure Pipelines y Jenkins, release management, y una plataforma certificada bajo estándares
de cumplimiento de salud. Hoy estoy disponible de inmediato."

## 2. Arquitectura en AWS para cargas sensibles con Terraform y contenedores

"Mercado Pago tenía cargas financieras sensibles, así que todo giraba en torno al aislamiento y al
mínimo privilegio. **Red:** VPC con subredes segmentadas; en las públicas solo los balanceadores, y los
contenedores y bases de datos en privadas. **Cómputo:** ECS y Kubernetes, cada servicio con su propio
rol de IAM. **Datos:** cifrado en reposo con KMS y TLS en tránsito; secretos desde un gestor de
secretos. **Terraform:** módulos reutilizables que daban a cada servicio la misma línea base segura;
estado remoto con bloqueo, y plan revisado antes del apply. **Resiliencia:** blue/green y canary, y
planeación de recuperación ante desastres entre regiones."

## 3. Blue/green con cambios de esquema de base de datos

"Uso **expand/contract**: (1) expand, solo cambios compatibles hacia atrás; (2) despliego green, que
escribe en las dos estructuras; (3) backfill en lotes; (4) cambio el tráfico, y el rollback a blue
sigue siendo seguro; (5) contract en un release posterior. Las migraciones van versionadas en el
pipeline y separadas del despliegue de la aplicación. Regla: nunca un cambio destructivo en el mismo
release que lo necesita."

Confirmación que pidió el entrevistador: "Exacto: el esquema siempre sirve a las dos versiones
mientras conviven, y cada paso es pequeño y reversible."

## 4. Módulos de Terraform y estado remoto en varios ambientes (CORREGIDA)

"**Módulos** pequeños, versionados con tags; cada ambiente fija la versión que consume. **Ambientes:**
teníamos **stage y varios ambientes de producción**, cada uno con su **propio estado**; las diferencias
van en variables, no en código duplicado. **Estado remoto** en S3 con versionado, cifrado y acceso por
IAM, con bloqueo, y dividido por componente para reducir el blast radius. **Flujo:** pull request, el
pipeline corre `terraform plan`, alguien lo revisa, y el apply lo hace el pipeline. Primero se aplica en
**stage**, se deja correr unos días, y solo si stage está sano se promueve a los ambientes de
producción. En una migración remapeamos el estado de Terraform sin tiempo de inactividad."

## 5. Pipeline de producción para una aplicación .NET (CORREGIDA)

"En Bizagi, con Azure Pipelines y Jenkins. **Crear versión:** con cada cambio el pipeline compila
(`dotnet build` en Release), corre las pruebas unitarias y genera **un artefacto versionado, una sola
vez**. **Desplegar:** esa misma versión se despliega primero en **stage**, donde corren las pruebas
automatizadas de integración y de humo. Stage va **unos días antes que producción**, y para pasar a
producción hay que **demostrar que en stage no hubo problemas**. Después la misma versión se despliega
en los **ambientes de producción** que haga falta. **Sin downtime:** la versión nueva se levanta al lado
de la actual, se valida con health checks y solo entonces recibe tráfico; el rollback es redesplegar la
versión anterior, que sigue guardada. **Después del deploy:** Grafana, con el onboarding automatizado
que lideré, daba visibilidad desde el primer día."

## 6. Endurecimiento de imágenes Docker y límites de recursos

"**Imágenes:** multi-stage builds, bases mínimas (distroless o slim) fijadas por versión o digest,
usuario no root, sistema de archivos de solo lectura, sin capabilities innecesarias, cero secretos en
la imagen y escaneo de vulnerabilidades que bloquea el build. **Recursos:** requests y limits según el
uso medido (con cuidado del OOMKilled), CPU y memoria por tarea en ECS, autoescalado con HPA o el
autoscaling de ECS, y las alertas de utilización que construí en MercadoLibre (capa reactiva, capa
predictiva y análisis con LLM)."

## 7. ECS: EC2 vs Fargate para servicios financieros

"Cuatro criterios: **seguridad** (Fargate aísla cada tarea y AWS parchea el host), **requisitos
técnicos** (EC2 si necesito GPU, acceso privilegiado o agentes en el host), **costo** (Fargate para
cargas variables; EC2 con Savings Plans para cargas estables y grandes) y **carga operativa**. Por
defecto, Fargate para servicios financieros sensibles; EC2 solo con un requisito concreto. Con
capacity providers se pueden combinar."

## 8. VPC multi-AZ para aislar bases de datos

"Tres AZ, tres capas de subredes: **públicas** (ALB y un NAT Gateway por zona), **privadas de
aplicación** (sin IP pública, salen por NAT) y **aisladas de datos** (RDS Multi-AZ, sin ninguna ruta a
internet). Encima: security groups encadenados, NACLs, VPC Endpoints, cifrado, VPC Flow Logs y SSM
Session Manager en vez de bastión."

## 9. Security groups entre ALB y backend (menor privilegio)

"Referencio security groups entre sí, no rangos de IP. **ALB:** entra 443; sale solo al puerto de la
app hacia el SG del backend. **Backend:** entra solo desde el SG del ALB; sale a la base de datos y a
los endpoints. **Base de datos:** entra solo desde el SG del backend. Además: health checks solo desde
el ALB, un SG por rol, awsvpc/Fargate para SG por tarea, todo en Terraform, y auditoría con AWS Config
o Security Hub."
