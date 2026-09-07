# Certificaciones — qué rendir y en qué orden

Recomendación basada en tu stack actual (Terraform, Azure, AWS, GCP, K8s), el
stack pedido en la vacante (Azure-céntrico) y una investigación de demanda
real de mercado (sept. 2026, fuentes en `../00-diagnostico/roadmap.md`).
Verificá siempre el temario actualizado en el link oficial antes de
inscribirte — Microsoft actualiza los exámenes con cierta frecuencia.

> **Hallazgo de la investigación de mercado:** la combinación de mayor señal
> combinada para roles DevOps/Platform en 2026 es **CKA + Terraform Associate
> + un cert de DevOps del cloud del empleador (AZ-400 en tu caso)** — no
> necesariamente AZ-400 solo. Terraform Associate es además "la certificación
> de mejor relación costo/valor de todo el espacio DevOps" (~$70 USD) dado que
> ya usás Terraform en producción.

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

## Orden sugerido dado tu perfil (ajustado con datos de mercado)

```
Terraform Associate  ←── más rápida y barata, capitaliza tu fortaleza ya hoy
   ↓
CKA  ←── ya tenés Kubernetes productivo, es la certificación técnica más
   |      respetada del ecosistema DevOps según la investigación
   ↓
AZ-400  ←── la más alineada al puesto específico de Julieta (requiere
   |         base de AZ-104/AZ-204, salteable si tu experiencia práctica alcanza)
   ↓
AZ-500 (opcional, si querés inclinar tu perfil hacia seguridad)
```

Cambio respecto a la primera versión de este plan: antes proponía AZ-400
primero por ser la más alineada 1:1 a la vacante. La investigación de mercado
mostró que la combinación **CKA + Terraform Associate** es la de mayor señal
combinada en el mercado general, y ambas son más rápidas/baratas de preparar
dado lo que ya sabés — por eso van primero. AZ-400 sigue siendo la prioridad
específica para *esta* vacante puntual si el proceso de selección avanza rápido.

Si ya te sentís cómodo con fundamentos de Azure (mucha experiencia práctica),
podés saltar **AZ-104** directamente y usar `../00-diagnostico/roadmap.md` +
los exámenes de este repo como preparación en su lugar.

## Cómo preparar cada certificación acá

1. Recorré los temas de `../temas/` relevantes al examen.
2. Pedime exámenes de práctica con el formato de la certificación:
   *"Dame un examen de práctica estilo AZ-400, 20 preguntas"*.
3. Registrá resultados en `../examenes/registro/` para ver evolución antes de
   pagar el examen real.
