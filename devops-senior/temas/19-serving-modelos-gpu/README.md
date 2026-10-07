# Serving de modelos e infraestructura GPU

Cómo desplegar y escalar modelos propios (o abiertos, como Llama) cuando no
alcanza con llamar a una API gestionada. Se apoya en Kubernetes (tema 10) y
en arquitectura/costos (tema 12): las GPUs son el recurso más caro de la
nube y escalarlas mal se nota enseguida en la factura.

## Objetivos

- Decidir entre **API gestionada** (Bedrock, Azure OpenAI, Vertex AI) vs.
  **endpoint gestionado con tu modelo** vs. **self-hosting en Kubernetes**.
- Servir LLMs abiertos con motores de inferencia: **vLLM**, **TGI**,
  **NVIDIA Triton**; y modelos clásicos con **KServe**.
- GPUs en Kubernetes: node pools con GPU, **NVIDIA GPU Operator**, `taints`/`tolerations`,
  requests de `nvidia.com/gpu`.
- Autoscaling de inferencia (por cola de requests / tokens, no solo CPU) y
  **scale-to-zero**.
- Optimización de costo: **quantization**, batching, instancias spot,
  elegir la GPU correcta.

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Endpoint gestionado para tu modelo | Azure ML **managed online endpoints** | **SageMaker endpoints** (real-time, serverless, async) | **Vertex AI endpoints** |
| Kubernetes con GPU | **AKS** + GPU node pools | **EKS** + GPU instances (p/g) | **GKE** + GPU node pools |
| Hardware de IA propio | — (NVIDIA en VMs ND/NC) | **Inferentia** / **Trainium** | **TPU** |
| Serverless con GPU | Container Apps (serverless GPUs) | — (SageMaker serverless sin GPU) | **Cloud Run** con GPU |

## Subtemas

1. API gestionada vs. endpoint propio vs. self-hosting: costos, control, compliance
2. Motores de inferencia: vLLM, TGI, Triton, KServe
3. GPUs en K8s: GPU Operator, node pools, scheduling
4. Autoscaling de inferencia: KEDA, métricas de cola/tokens, scale-to-zero, cold start
5. Optimización: quantization (INT8/4-bit), batching continuo, KV cache
6. Costos: GPU on-demand vs. spot vs. reservada, medir costo por 1.000 tokens

## Recursos

- vLLM: https://docs.vllm.ai/
- KServe: https://kserve.github.io/website/
- GKE — Serve LLMs with GPUs: https://cloud.google.com/kubernetes-engine/docs/tutorials/serve-llm-l4-vllm
- SageMaker inference: https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html
- AKS GPU: https://learn.microsoft.com/azure/aks/gpu-cluster

## Lab sugerido

Serví un modelo abierto chico (por ejemplo, un Qwen o Llama de 1-3B
parámetros) con **vLLM** en Docker (sin GPU, en CPU, si no tenés acceso a una).
Escribí el manifiesto de Kubernetes que lo desplegaría en un nodo con GPU
(`nvidia.com/gpu: 1`, `tolerations`) y la regla de **KEDA** para escalarlo.

## Autoevaluación

Pedime: *"Dame un examen de serving de modelos y GPUs nivel senior"*.
