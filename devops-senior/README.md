# Plan de aprendizaje — Camino a Senior DevOps + IA Engineer

Carpeta de estudio personal de Sebastián Díaz para llegar a ser experto en
**DevOps / Platform Engineering multi-cloud** (Azure, AWS y GCP) **y en IA**
(desarrollo de aplicaciones con IA, RAG, agentes, MLOps/LLMOps y serving de
modelos), preparar certificaciones y medir avance con exámenes de
autoevaluación. Ops e IA van en **un solo roadmap**
(`00-diagnostico/roadmap.md`), con fases que combinan las dos partes.

Origen: mensaje de Julieta García (PlatformX Solutions) sobre una vacante de
**Azure Platform Engineer** (contractor, remoto, largo plazo) — sigue siendo
una referencia concreta para el diagnóstico de brechas. Pero el alcance del
repo **no es solo Azure**: ya tenés experiencia real en AWS y GCP (MercadoLibre)
y ofertas en cualquiera de las tres nubes son válidas. Por eso cada tema de
`temas/` está organizado por **concepto** (no por nube) e incluye la
equivalencia en Azure, AWS y GCP.

## Estructura

```
devops-senior/
├── 00-diagnostico/        # dónde estás hoy vs. dónde necesitas estar
│   ├── gap-analysis.md
│   └── roadmap.md
├── temas/                 # una carpeta por tema (concepto), con equivalencias
│   │                       # Azure / AWS / GCP + teoría + labs + lecturas
│   ├── 01-iac-multicloud/                      # Bicep, CloudFormation/CDK, Terraform
│   ├── 02-contenedores-serverless/             # Container Apps, Fargate, Cloud Run
│   ├── 03-cicd-multicloud/                     # GitHub Actions + OIDC a las 3 nubes
│   ├── 04-identidad-iam/                       # Entra ID/RBAC, AWS IAM, GCP IAM
│   ├── 05-networking-multicloud/               # VNet, VPC (AWS), VPC (GCP)
│   ├── 06-datos-secretos/                      # Key Vault/Cosmos DB, Secrets Manager/DynamoDB, Secret Manager/Firestore
│   ├── 07-observabilidad-multicloud/           # Azure Monitor, CloudWatch, Cloud Logging/Monitoring
│   ├── 08-python-fastapi-docker/               # cloud-agnóstico
│   ├── 09-orquestacion-serverless/             # Durable Functions, Step Functions, Workflows
│   ├── 10-kubernetes-avanzado/                 # K8s en general + AKS/EKS/GKE
│   ├── 11-seguridad-devsecops/                 # Defender for Cloud, Security Hub, Security Command Center
│   ├── 12-arquitectura-costos-multicloud/      # los 3 Well-Architected/Architecture Frameworks
│   ├── 13-mercadolibre-scopes-cosmos/          # material interno MELI (confidencial, no compartir)
│   │   # ── Bloque IA ──
│   ├── 14-fundamentos-ia-llm/                  # ML, LLMs, tokens, embeddings (Foundry, Bedrock, Vertex AI)
│   ├── 15-desarrollo-apps-llm/                 # APIs de LLMs, structured output, tool use, streaming
│   ├── 16-rag-bases-vectoriales/               # AI Search, Bedrock Knowledge Bases, Vertex AI Vector Search, pgvector
│   ├── 17-agentes-ia/                          # agentes, MCP, Foundry Agent Service, Bedrock AgentCore, ADK
│   ├── 18-mlops-llmops/                        # Azure ML, SageMaker, Vertex AI Pipelines, MLflow, evals
│   ├── 19-serving-modelos-gpu/                 # vLLM, KServe, GPUs en AKS/EKS/GKE
│   └── 20-seguridad-gobernanza-ia/             # prompt injection, Content Safety, Bedrock Guardrails, Model Armor
├── certificaciones/       # qué certificar, en qué orden, y por qué (DevOps + IA, Azure + AWS + GCP)
├── examenes/               # cómo pedir exámenes y dónde queda el registro de resultados
│   ├── README.md
│   └── registro/
└── recursos/               # glosario y enlaces generales
```

## Cómo usar esto día a día

1. **Elegí un tema** de `temas/` (seguí el orden sugerido en `00-diagnostico/roadmap.md`,
   o el que te interese repasar). El **tablero de avance** al principio del
   roadmap muestra en qué fase estás y qué temas (Ops e IA) te faltan.
2. **Leé** el `README.md` de ese tema: tiene objetivos, subtemas y enlaces oficiales.
3. **Pedime un examen** de ese tema (ver `examenes/README.md` para el formato).
   Resolvelo, te corrijo, y anotamos el resultado en `examenes/registro/`.
4. Revisamos juntos los puntos débiles y volvemos a ese tema o pasamos al siguiente.

No hace falta pedirme permiso para arrancar: decime "dame un examen de Bicep nivel
intermedio", "explicame RAG" o "explicame Private Endpoints" y seguimos desde ahí.

> ⚠️ **Nota de confidencialidad**: `temas/13-mercadolibre-scopes-cosmos/` contiene
> material interno de MercadoLibre (preguntas de entrevista del equipo Scopes Govern).
> Este repositorio es privado por decisión explícita del dueño. Si en algún momento
> este repo pasa a ser público, esa carpeta debe eliminarse del historial de git antes.
