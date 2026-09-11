# Certificaciones — qué rendir y en qué orden

Recomendación basada en tu stack actual (Terraform, Azure, AWS, GCP, K8s), el
stack pedido en la vacante de Julieta (Azure-céntrico, un caso concreto entre
varios posibles) y una investigación de demanda real de mercado (sept. 2026,
fuentes en `../00-diagnostico/roadmap.md`). No te limites a Azure: tenés
experiencia real en AWS y GCP, así que abajo hay una ruta por nube — elegí
según hacia dónde se incline la oferta que tengas más cerca en cada momento.
Verificá siempre el temario actualizado en el link oficial antes de
inscribirte — los proveedores actualizan los exámenes con cierta frecuencia.

> **Hallazgo de la investigación de mercado:** la combinación de mayor señal
> combinada para roles DevOps/Platform en 2026 es **CKA + Terraform Associate
> + un cert de DevOps del cloud del empleador (AZ-400 en tu caso)** — no
> necesariamente AZ-400 solo. Terraform Associate es además "la certificación
> de mejor relación costo/valor de todo el espacio DevOps" (~$70 USD) dado que
> ya usás Terraform en producción.

## Ruta transversal (agnóstica de nube) — hacela primero, sirve para cualquier oferta

### Terraform Associate (HashiCorp)
Ya usás Terraform en producción (Bizagi, MercadoLibre). Es la de mejor
relación costo/valor (~$70 USD) y es la única certificación de esta lista que
suma puntos para una entrevista en Azure, AWS **o** GCP por igual.
- https://developer.hashicorp.com/certifications/infrastructure-automation

### CKA — Certified Kubernetes Administrator
Ya tenés Kubernetes productivo (MercadoLibre, sobre AWS/GCP). Es la
certificación técnica más respetada del ecosistema DevOps y, como Kubernetes
es igual en AKS/EKS/GKE a nivel API, también es agnóstica de nube.
- https://www.cncf.io/training/certification/cka/

## Ruta Azure

### AZ-104: Microsoft Azure Administrator (base)
Si nunca certificaste nada de Azure formalmente, es la base — cubre gestión
de recursos, storage, compute, networking básico, identidad. Salteable si tu
experiencia práctica ya alcanza.
- https://learn.microsoft.com/certifications/azure-administrator/

### AZ-400: Designing and Implementing Microsoft DevOps Solutions ⭐ (la más alineada a la vacante de Julieta)
Es LA certificación DevOps de Microsoft. Cubre CI/CD, IaC, seguridad en el
pipeline, monitoreo — prácticamente un espejo de todo lo que pide esa
vacante. Requiere (o recomienda) AZ-104 o AZ-204 como base.
- https://learn.microsoft.com/certifications/devops-engineer/

### AZ-500: Microsoft Azure Security Engineer — opcional, si el rol se inclina a seguridad
Refuerza identidad/RBAC/Key Vault/Networking (temas 04, 05, 06, 11) y es un
buen diferenciador para roles senior.
- https://learn.microsoft.com/certifications/azure-security-engineer/

## Ruta AWS

### AWS Certified Solutions Architect – Associate (base)
Equivalente conceptual a AZ-104: valida fundamentos de la nube (compute,
storage, networking, IAM) de forma amplia. Buen punto de entrada si una
oferta AWS te pide certificación formal.
- https://aws.amazon.com/certification/certified-solutions-architect-associate/

### AWS Certified DevOps Engineer – Professional ⭐ (equivalente a AZ-400)
La certificación DevOps "expert-level" de AWS: CI/CD, IaC (CloudFormation/CDK),
monitoreo, alta disponibilidad. Requiere experiencia real (no es de entrada) —
tu experiencia en AgroTec/MercadoLibre con AWS ya te da buena base práctica.
- https://aws.amazon.com/certification/certified-devops-engineer-professional/

### AWS Certified Security – Specialty — opcional
Equivalente a AZ-500. Útil si el rol se inclina a seguridad/compliance.
- https://aws.amazon.com/certification/certified-security-specialty/

## Ruta GCP

### Google Associate Cloud Engineer (base)
Equivalente a AZ-104/Solutions Architect Associate: gestión operativa general
de GCP.
- https://cloud.google.com/certification/cloud-engineer

### Google Professional Cloud DevOps Engineer ⭐ (equivalente a AZ-400)
Certificación específica de DevOps de GCP: SRE practices, CI/CD, monitoreo,
gestión de incidentes. La más alineada si la oferta es GCP-céntrica.
- https://cloud.google.com/certification/cloud-devops-engineer

### Google Professional Cloud Architect — opcional, más amplia que DevOps Engineer
Diseño de arquitecturas completas en GCP; buen complemento si el rol pide
también decisiones de arquitectura, no solo operación.
- https://cloud.google.com/certification/cloud-architect

## Ruta IA / MLOps — opcional, alto crecimiento

Cada vez más ofertas de DevOps/Platform piden desplegar y operar cargas de
IA (APIs de modelos, RAG, GPUs) — es una extensión natural de lo que ya
sabés (Container Apps/Fargate/Cloud Run para servir modelos, FastAPI para
las APIs de inferencia). No reemplaza la ruta DevOps, la complementa.

### Nivel fundamentos (rápidas, para tener el vocabulario)
- **Azure AI Fundamentals (AI-900)** — https://learn.microsoft.com/certifications/azure-ai-fundamentals/
- **AWS Certified AI Practitioner** — https://aws.amazon.com/certification/certified-ai-practitioner/
- **Google Cloud Generative AI Leader** — https://cloud.google.com/certification/generative-ai-leader

### Nivel técnico ⭐ (el que suma de verdad para un perfil DevOps/MLOps)
- **Azure AI Engineer Associate (AI-102)** — construir soluciones con Azure
  AI Services/Azure OpenAI. https://learn.microsoft.com/certifications/azure-ai-engineer/
- **AWS Certified Machine Learning Engineer – Associate** — la más orientada
  a **MLOps** (pipelines, despliegue, monitoreo de modelos) de las tres.
  https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/
- **Google Professional Machine Learning Engineer** — la más exigente y
  reconocida de las tres, cubre todo el ciclo de vida de ML en producción.
  https://cloud.google.com/certification/machine-learning-engineer

Si el objetivo es un rol tipo "MLOps Engineer" o "AI Platform Engineer" (variante
cada vez más común del DevOps senior), la de mayor señal es la de **AWS
Machine Learning Engineer – Associate** o **Google Professional Machine
Learning Engineer**, según la nube del empleador — son las dos con más foco
en productivizar modelos, no solo entrenarlos.

## Ruta Chaos Engineering / SRE — agregada por la vacante Davivienda

Ver `../00-diagnostico/gap-analysis-davivienda-chaos-sre.md` y
`../temas/14-chaos-engineering-sre/`. A diferencia de las certificaciones de
cloud, en chaos engineering hay una sola certificación con reconocimiento
real en la industria:

### Gremlin Enterprise Chaos Engineering Certification
Certificación de Gremlin (uno de los referentes comerciales del área),
compatible con LinkedIn. Incluye material de preparación y prueba gratis de
la herramienta — buena forma de aprender la práctica y certificarla al
mismo tiempo, sin depender de tener un cluster propio con Litmus/Chaos Mesh
ya armado.
- https://www.gremlin.com/certification

No hay certificación equivalente para Litmus o Chaos Mesh (son proyectos
open source de CNCF, sin programa formal de certificación) — para esos dos,
la demostración es práctica (correr experimentos reales) más que un
certificado.

## Orden sugerido dado tu perfil (ajustado con datos de mercado)

```
Terraform Associate  ←── más rápida y barata, sirve para las 3 nubes
   ↓
CKA  ←── ya tenés Kubernetes productivo, sirve para las 3 nubes
   ↓
Certificación DevOps de la nube de tu próxima oferta concreta:
   AZ-400 (Azure) · AWS DevOps Engineer Professional (AWS) · Cloud DevOps Engineer (GCP)
   ↓
Certificación de seguridad opcional de esa misma nube (AZ-500 / AWS Security Specialty)
```

Empezá siempre por las dos transversales (Terraform Associate + CKA) — no
importa a qué nube apunte la próxima oferta, ya suman. Recién ahí elegí la
certificación específica de nube según la oferta concreta que tengas más
cerca en ese momento (hoy, la de Julieta apunta a AZ-400). La ruta IA/MLOps
es un agregado opcional en paralelo, no un reemplazo de este orden.

## Cómo preparar cada certificación acá

1. Recorré los temas de `../temas/` relevantes al examen — cada uno ya trae
   la tabla de equivalencias Azure/AWS/GCP.
2. Pedime exámenes de práctica con el formato de la certificación:
   *"Dame un examen de práctica estilo AZ-400"* o *"...estilo AWS DevOps
   Engineer Professional"* o *"...estilo Google Cloud DevOps Engineer"*.
3. Registrá resultados en `../examenes/registro/` para ver evolución antes de
   pagar el examen real.
