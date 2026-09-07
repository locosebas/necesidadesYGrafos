# Certificaciones — qué rendir y en qué orden

Recomendación basada en tu stack actual (Terraform, Azure, AWS, GCP, K8s) y
el stack pedido en la vacante (Azure-céntrico). Verificá siempre el temario
actualizado en el link oficial antes de inscribirte — Microsoft actualiza
los exámenes con cierta frecuencia.

## Ruta recomendada

### 1. AZ-104: Microsoft Azure Administrator (base)
Si nunca certificaste nada de Azure formalmente, es la base — cubre gestión
de recursos, storage, compute, networking básico, identidad. Aunque tu
experiencia ya cubre buena parte, certifica formalmente lo que ya sabés y
llena huecos de administración pura.
- https://learn.microsoft.com/certifications/azure-administrator/

### 2. AZ-400: Designing and Implementing Microsoft DevOps Solutions ⭐ (la más alineada a la vacante)
Es LA certificación DevOps de Microsoft. Cubre CI/CD, IaC, seguridad en el
pipeline, monitoreo — prácticamente un espejo de todo lo que pide Julieta.
Requiere (o recomienda tener antes) AZ-104 o AZ-204 como base.
- https://learn.microsoft.com/certifications/devops-engineer/

### 3. Terraform Associate (HashiCorp) — opcional pero de alto ROI
Ya usás Terraform en producción. Es rápida de preparar dado tu nivel actual
y valida formalmente tu fortaleza más grande, incluso para un rol Azure/Bicep
(muchas empresas usan Terraform sobre Azure igual).
- https://developer.hashicorp.com/certifications/infrastructure-automation

### 4. CKA — Certified Kubernetes Administrator — opcional, refuerza tu perfil multi-cloud
Ya tenés Kubernetes productivo en MercadoLibre. Certificarlo te distingue en
roles que combinan Azure PaaS con Kubernetes "real" (AKS o self-managed).
- https://www.cncf.io/training/certification/cka/

### 5. AZ-500: Microsoft Azure Security Engineer — opcional, si el rol se inclina a seguridad
No es lo primero que pide la vacante, pero refuerza Entra ID/RBAC/Key
Vault/Networking (temas 04, 05, 06, 11 de este repo) y es un buen
diferenciador para roles senior.
- https://learn.microsoft.com/certifications/azure-security-engineer/

## Orden sugerido dado tu perfil

```
AZ-104 (si no tenés nada de Azure certificado)
   ↓
AZ-400  ←── la prioridad real para esta vacante
   ↓
Terraform Associate (rápida, capitaliza tu fortaleza)
   ↓
CKA o AZ-500 (según hacia dónde quieras inclinar tu perfil)
```

Si ya te sentís cómodo con fundamentos de Azure (mucha experiencia práctica),
podés saltar directo a **AZ-400** y usar `00-diagnostico/roadmap.md` + los
exámenes de este repo como preparación, en vez de perder tiempo en AZ-104.

## Cómo preparar cada certificación acá

1. Recorré los temas de `../temas/` relevantes al examen.
2. Pedime exámenes de práctica con el formato de la certificación:
   *"Dame un examen de práctica estilo AZ-400, 20 preguntas"*.
3. Registrá resultados en `../examenes/registro/` para ver evolución antes de
   pagar el examen real.
