# Proceso de selección Davivienda — Especialista Senior SRE

> ⚠️ **Confidencial.** Los correos de origen traen aviso legal de confidencialidad
> (Banco Davivienda S.A.). Este repo es **público** en GitHub: por decisión del dueño solo se
> versionan las transcripciones `.md`; los PDFs originales (`pdf/`) están en `.gitignore` y se
> obtienen de nuevo desde los correos.

## Origen

Dos correos de `paula.patino@davivienda.com` (Centro de Selección Grupo Bolívar), 2026-10-07:

| Correo | Adjunto | Archivo local (no versionado) |
|---|---|---|
| "Proceso de selección Especialista Senior SRE Davivienda" (20:17 UTC) | Rublica evaluación - Especialista II Observabilidad - 15 junio.pdf | `pdf/rubrica-evaluacion-especialista-ii-observabilidad.pdf` → [transcripción](rubrica-evaluacion-especialista-ii-observabilidad.md) |
| "Corrección caso - Proceso de selección..." (21:49 UTC) | Caso de Uso - Candidato_ Especialista I - Plataforma de Confiabilidad - V1.pdf | `pdf/caso-de-uso-especialista-i-plataforma-confiabilidad-v1.pdf` → [transcripción](caso-de-uso-especialista-i-plataforma-confiabilidad.md) |

**Plazo:** lunes 12 de octubre de 2026 a medianoche (pruebas psicotécnicas, perfil en Magneto y prueba técnica).

## Revisión de seguridad de los adjuntos

Los PDFs se descargaron por el MIME crudo del correo a una carpeta de cuarentena, sin abrirlos en ningún
visor, y se analizaron estáticamente antes de copiarlos aquí.

| Verificación | Resultado |
|---|---|
| Autenticidad del remitente | SPF, DKIM (`davivienda.com`) y DMARC: **pass** en ambos correos |
| Tipo real del archivo | PDF 1.4 válido, generado por Google Docs (Skia/PDF) |
| JavaScript / `OpenAction` / `AA` / `Launch` | Ninguno |
| Archivos embebidos / RichMedia / XFA / formularios | Ninguno |
| Enlaces (`/URI`) | Ninguno |
| Cifrado | No |
| Texto oculto (modo invisible, letra diminuta, prompt injection) | No; el texto extraído coincide con la página renderizada |

SHA-256:

```
3168a55f7513da5589fcbd0c94a767cb990e79b50b87f1dacd6515ea515134fb  caso-de-uso-especialista-i-plataforma-confiabilidad-v1.pdf
69073cec11022e79d271e45b9b3598f4d93969483518f6a13d0dc7c9af392ad7  rubrica-evaluacion-especialista-ii-observabilidad.pdf
```

### ⚠️ Señal a vigilar: dominio de entrega

El cuerpo de ambos correos pide enviar el reto a **`paula.patino@davivenda.com`** (sin la "i"), mientras
que el remitente autenticado es `paula.patino@davivienda.com`. Lo más probable es un error de tipeo, pero
`davivenda.com` es un dominio distinto (patrón típico de *typosquatting*). **Enviar la entrega a
`@davivienda.com`** (respondiendo al mismo correo) y, si hay duda, confirmarlo con la reclutadora.

### Nota sobre la rúbrica

El primer correo adjuntó la **rúbrica interna de la mesa evaluadora** de otro caso (Especialista II
Observabilidad, escenario "PlusPay"); el segundo ("Corrección caso") la reemplazó por el caso de uso
real. Parece un envío por error.

## Prueba técnica (resumen)

Presentación de máx. 10 diapositivas + 20 min de exposición + 10 min de preguntas, sobre 4 ejes:

1. SLOs, Error Budgets y Quality Gate en CI/CD → ver [tema 07](../07-observabilidad-multicloud/README.md), [tema 03](../03-cicd-multicloud/README.md)
2. Telemetría con OpenTelemetry Collector multi-cloud + Smart Sampling / FinOps (−30% costo) → [tema 07](../07-observabilidad-multicloud/README.md), [tema 12](../12-arquitectura-costos-multicloud/README.md)
3. Telemetría AI-Ready con MCP + IA causal para RCA → [tema 17](../17-agentes-ia/README.md)
4. Incident Commander + post-mortem blameless → [tema 10](../10-kubernetes-avanzado/README.md)
