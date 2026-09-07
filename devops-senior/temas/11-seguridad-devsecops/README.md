# Seguridad / DevSecOps

Lo que separa a un DevOps Senior de uno mid es diseñar seguridad desde el
principio (shift-left), no parchearla después.

## Objetivos

- Escaneo de imágenes de contenedor (vulnerabilidades de dependencias/OS base)
  integrado al pipeline, no manual.
- Escaneo de IaC (Bicep/Terraform) antes del deploy (secrets hardcodeados,
  recursos públicos por default, roles demasiado permisivos).
- Supply chain: SBOM (Software Bill of Materials), firma de imágenes.
- Principio de mínimo privilegio aplicado de punta a punta (ya lo venís viendo
  en Entra ID/RBAC — acá se junta todo).
- OWASP Top 10 a nivel conceptual (relevante si tocás las APIs con FastAPI).
- Manejo de secretos: por qué nunca en variables de entorno planas ni en git,
  siempre Key Vault + Managed Identity.

## Subtemas

1. Escaneo de imágenes: Microsoft Defender for Containers, Trivy
2. Escaneo de IaC: Checkov, tfsec, PSRule for Azure
3. Network security: NSG + Private Endpoints como defensa en profundidad (conecta con tema 05)
4. Secrets scanning en el propio repo (gitleaks, GitHub secret scanning)
5. OWASP Top 10: https://owasp.org/www-project-top-ten/

## Lab sugerido

Agregá al pipeline de GitHub Actions del lab del tema 03 un paso de escaneo de
la imagen Docker (Trivy) y uno de escaneo del Bicep/Terraform (Checkov), que
falle el build si encuentra hallazgos críticos.

## Autoevaluación

Pedime: *"Dame un examen de seguridad/DevSecOps nivel senior"*.
