# MLOps y LLMOps

Donde DevOps e IA se juntan del todo: aplicar CI/CD, versionado,
observabilidad y gobierno (temas 03 y 07) a modelos y aplicaciones de IA.
Es el núcleo de roles como **MLOps Engineer** o **AI Platform Engineer**, y
tu mayor ventaja competitiva: la mayoría de la gente de IA no sabe operar
producción, y la mayoría de DevOps no entiende el ciclo de vida de un modelo.

## Objetivos

- Explicar el ciclo de vida de un modelo: datos → entrenamiento →
  evaluación → registro → despliegue → monitoreo → reentrenamiento.
- **Versionado** de todo lo que cambia el comportamiento: código, datos,
  modelo, **prompts**.
- **Model registry** y promoción entre ambientes (dev → staging → prod).
- Pipelines de ML automatizados (entrenamiento y evaluación como pasos de CI/CD).
- **LLMOps**: evaluaciones automáticas (**evals**) como "tests" de una app
  LLM, que bloquean un deploy si la calidad baja.
- Monitoreo en producción: **data drift**, **model drift**, calidad de
  respuestas, costo por request, latencia.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Plataforma de MLOps | **Azure Machine Learning** | **SageMaker AI** | **Vertex AI** |
| Pipelines de ML | Azure ML pipelines | **SageMaker Pipelines** | **Vertex AI Pipelines** (Kubeflow) |
| Model registry | Azure ML model registry | SageMaker Model Registry | Vertex AI Model Registry |
| Monitoreo de modelos | Azure ML model monitoring | SageMaker Model Monitor | Vertex AI Model Monitoring |
| Evaluación de LLMs | Azure AI Foundry evaluations | Bedrock model evaluation | Vertex AI Gen AI evaluation |
| Tracing de apps LLM | Azure AI Foundry tracing (OpenTelemetry) | Bedrock invocation logging + CloudWatch / X-Ray | Cloud Trace + Vertex AI |
| Agnóstico | **MLflow**, Kubeflow, **Langfuse**, OpenTelemetry GenAI | ídem | ídem |

## Subtemas

1. Ciclo de vida de ML y niveles de madurez de MLOps (manual → pipeline → CI/CD de ML)
2. **MLflow**: tracking de experimentos, model registry
3. Pipelines de entrenamiento en SageMaker / Azure ML / Vertex AI
4. CI/CD para modelos: tests de datos, evaluación automática, despliegue gradual (canary, shadow)
5. **LLMOps**: versionado de prompts, **evals** en CI (promptfoo, DeepEval, Ragas), LLM-as-judge
6. Observabilidad de LLMs: tokens, costo, latencia, trazas por request (**Langfuse**, OpenTelemetry)
7. Drift y reentrenamiento: detectar que el modelo se degradó

## Recursos

- Google — MLOps: Continuous delivery and automation pipelines in ML: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- MLflow: https://mlflow.org/docs/latest/
- SageMaker Pipelines: https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html
- Azure Machine Learning MLOps: https://learn.microsoft.com/azure/machine-learning/concept-model-management-and-deployment
- Langfuse: https://langfuse.com/docs

## Lab sugerido

Al proyecto del tema 15 o 16 agregale un workflow de **GitHub Actions** que
corra un set de **evals** (20 preguntas con respuesta esperada) en cada PR y
falle si el puntaje baja de un umbral. Instrumentá la app con **Langfuse** u
OpenTelemetry para ver tokens, costo y latencia por request.

## Autoevaluación

Pedime: *"Dame un examen de MLOps y LLMOps nivel senior"*.
