# Decisiones del libreto de la presentación — para revisar

> Al escribir [presentacion-libreto.md](presentacion-libreto.md) se tomaron decisiones (algunas aplicando las
> recomendaciones provisionales de [decisiones-herramientas.md](decisiones-herramientas.md), cuya columna "Tu
> decisión" sigue vacía) y otras quedaron sin tomar. Se revisan **de a una**: tú decides si se mantiene o cambia, y
> la columna **Revisión** se llena con lo acordado. Después se ajusta el libreto y se genera el HTML.

## 0. ⚠️ Reenfoque pendiente (2026-10-14, desde otra sesión)

En la conversación se aclaró que **no es una propuesta de seguridad sino de cumplimiento** (como en Davivienda), y que
en la entrevista **se mencionó mucho la deuda técnica**. Ver [propuesta-valor.md](propuesta-valor.md) **v2** (Medir,
Pagar, Cumplir, Estabilizar). Antes de regenerar el HTML hay que decidir:

| # | Decisión | Propuesta | Afecta | Revisión |
|---|---|---|---|---|
| R1 | Causa común (decisión 4) | Cambiar "lo seguro y lo estable dependen de personas" por **"deuda técnica: una causa, tres síntomas"** | 1, 2 | |
| R2 | Ejes (decisión 2) | Los 3 dolores **más deuda técnica** como hilo; la IA de voz baja de "eje" a "diferencial" dentro de cumplimiento | todas | |
| R3 | Diapositiva nueva o fusionada | Una diapositiva de **deuda técnica**: registro, hotspots, Strangler Fig en las migraciones, capacidad fija por sprint | 2–3 o 6 | |
| R4 | Título | De "defensa de la plataforma" a **"propuesta de cumplimiento"** | 1 | |

## A. Decisiones tomadas — narrativa y formato

| # | Decisión | Qué quedó en el libreto | Alternativa | Por qué | Diap. | Revisión |
|---|---|---|---|---|---|---|
| 1 | Duración | ~16 min en 10 diapositivas (1,5–2 min cada una) | 20 min como Davivienda · 5–8 min si es más una conversación | Dapta no dio formato; 16 min deja espacio para preguntas en una entrevista de 45–60 min | todas | |
| 2 | Ejes de la presentación | Los **3 dolores** de la entrevista (certificaciones, estabilidad, DORA) + **IA de voz** como diferencial | Los 4 pilares de la propuesta v1 (Desplegar, Plataforma, Detectar, IA) | Cada diapositiva le habla a un dolor que ellos mismos dijeron | todas | |
| 3 | Lema | "Una carretera pavimentada, no un peaje" | "Golden path" a secas · otro lema | Se entiende sin saber Platform Engineering y responde al miedo de que seguridad frene | 1 | |
| 4 | Causa común | "Lo seguro y lo estable dependen de personas, no de la plataforma" | No forzar una causa única | Mismo recurso de Davivienda (4 síntomas, 1 causa); une los dolores en una sola solución | 1, 2 | |
| 5 | Mencionar la status page | Sí, con tacto: "muestra incidentes en Flow Studio y aun así marca 100%" | No mencionarla · solo en preguntas | Muestra que se investigó; riesgo: que suene a crítica | 7 | |
| 6 | Mencionar la ronda de USD 6 M | Sí, como parte de "por qué ahora" | No mencionarla | Es pública (13-oct) y explica el crecimiento del equipo y de los compradores | 1 | |
| 7 | Nombrar subprocesadores | Sí (Twilio, LiveKit, Deepgram, OpenAI, Anthropic, Gemini, Groq, Temporal, Vanta) | Hablar en genérico ("proveedores de voz y LLM") | Son públicos en su trust center y hacen concreto el diagrama C4 | 2 | |
| 8 | Presentación personal | Una frase en la portada: Kubernetes, identidades por pod, políticas como código, CI/CD | Diapositiva propia "Por qué yo" · no decir nada | Cabe en 10 diapositivas sin quitar contenido; no se afirma ninguna experiencia que no tengas | 1 | |
| 9 | Plan con piloto | 30-60-90 días con **un servicio piloto** en el tramo 31–60 | Migrar todo a la vez · plan a 6–12 meses | Mismo patrón de Davivienda; baja el riesgo y muestra resultados pronto | 10 | |

## B. Decisiones tomadas — técnicas (las 12 de decisiones-herramientas.md)

| # | Decisión (D#) | Qué quedó en el libreto | Diap. | Revisión |
|---|---|---|---|---|
| 10 | Secretos (D1) | AWS Secrets Manager + External Secrets Operator | 6 | |
| 11 | Temporal (D2) | **Temporal Cloud** (se asume; queda como pregunta para la mesa) | 6 | |
| 12 | ¿Kubernetes? (D3) | Amazon EKS, justificado por el on-premise del plan Enterprise | 6 | |
| 13 | Políticas en el clúster (D4) | Kyverno (no OPA Gatekeeper) | 6 | |
| 14 | Despliegue (D5) | Argo CD (GitOps) | 4 | |
| 15 | Canary / rollback (D6) | **Todavía no** (Argo Rollouts después de tener SLOs) | 7, 10 | |
| 16 | Feature flags (D7) | PostHog (ya es subprocesador) | 5 | |
| 17 | Medir DORA (D8) | API de GitHub + Argo CD → Grafana; comprar LinearB/Sleuth solo si no basta | 5 | |
| 18 | Escaneo en el pipeline (D9) | Nativo de GitHub (Dependabot, secret scanning) + Trivy; Semgrep solo si hace falta | 4 | |
| 19 | Detección en AWS (D10) | GuardDuty + Security Hub + CloudTrail organizacional; SIEM **todavía no** | 9 | |
| 20 | Service mesh (D11) | Ninguno | 10 | |
| 21 | Cumplimiento (D12) | Seguir con Vanta | 3, 4 | |

## C. Decisiones tomadas — nuevas (no estaban en las 12)

| # | Decisión | Qué quedó en el libreto | Alternativa | Por qué | Diap. | Revisión |
|---|---|---|---|---|---|---|
| 22 | Solo 2 piezas nuevas | Argo CD y Kyverno; Trivy cuenta como paso del pipeline, no como herramienta a operar | Contar Trivy como nueva (serían 3) | Responde al "¿quién opera todo eso?" (pregunta N7.3 del banco) | 10 | |
| 23 | Firma de imágenes (Cosign) | **Fuera** de los 90 días: "segunda vuelta", cuando Kyverno pueda exigir la firma | Incluirla en el pipeline desde el día 1 | Firmar sin verificar no protege nada | 10 (preguntas) | |
| 24 | Identidad de los pods | **EKS Pod Identity** primero, IRSA como alternativa | IRSA primero (la que más dominas) | Pod Identity es la opción más reciente y simple de AWS | 6 | |
| 25 | Kyverno por fases | Modo **Audit** en los días 31–60, **Enforce** en los días 61–90 | Enforce desde el inicio | No frenar a los desarrolladores el primer día | 6, 10 | |
| 26 | Cifrado en Temporal | Payload Codec (cifrado del lado del cliente) + Codec Server + mTLS + un namespace por ambiente | Confiar en el cifrado del proveedor | Temporal solo ve texto cifrado: el argumento de privacidad más fuerte | 6 | |
| 27 | Ampliar el SOC 2 | Agregar el criterio de **Availability** por los SLAs de Enterprise | Quedarse en Security | Si se venden SLAs, el comprador va a pedir evidencia de disponibilidad | 3 | |
| 28 | SLIs de la llamada | ① la llamada conecta · ② el agente responde rápido (percentil) · ③ el workflow de Flow Studio termina bien | Uptime de servidores · otros SLIs | Medidos desde el cliente, como en Davivienda | 7 | |
| 29 | Status page desde el SLO | La status page se alimenta del SLO medido | Dejarla como está | Hace defendible el número ante un cliente Enterprise | 7 | |
| 30 | Failover entre LLMs | Timeouts + circuit breaker + failover entre proveedores, probado con las evals | Un solo proveedor | Dependen de varios proveedores externos en tiempo real | 7 | |
| 31 | Evals del agente | Un cambio de prompt es un despliegue: evals en el pipeline | Pruebas manuales | Une IA con DORA (Change Failure Rate) | 8 | |
| 32 | Terraform | Con el `plan` visible en el pull request, desde GitHub Actions (sin Atlantis) | Atlantis | Una herramienta menos que operar | 4 | |
| 33 | On-call | "You build it, you run it", rotación liviana, alertas solo por burn rate | Equipo de guardia central | Con 14 personas no hay equipo de operaciones | 9 (preguntas) | |

## D. Decisiones sin tomar

| # | Decisión pendiente | Por qué quedó abierta | Cómo se cierra |
|---|---|---|---|
| 34 | ¿Qué certificación sigue después del SOC 2? | Depende del contrato que esté esperando | Pregunta a la mesa (anexo, 1) |
| 35 | ¿PCI DSS va en la presentación? | Quedó **fuera** de la diapositiva 3, aunque la cobranza por teléfono podría tocar tarjetas | Decidir si se menciona o solo en preguntas |
| 36 | ¿GDPR, Ley 1581 y la política de privacidad van? | Quedaron fuera; solo aparece la TCPA | Decidir si se menciona la expansión a LatAm |
| 37 | Umbrales del SLO y del SLA | No se inventan: salen de la línea base | Primeras 2 semanas |
| 38 | Contenido de la Error Budget Policy | Solo aparece en una pregunta probable (diap. 7) | Decidir si sube al contenido |
| 39 | ¿Cuál es el servicio piloto? | No se sabe qué servicios hay ni cuál migra primero | Pregunta a la mesa (anexo, 3) |
| 40 | Criterio para traer el canary | Se dijo "después de tener SLOs", sin criterio de entrada | Definir (ej.: SLO estable N semanas) |
| 41 | CNI para NetworkPolicy (Cilium o VPC CNI) | La propuesta v1 lo dejaba abierto; el libreto no nombra ninguno | Decidir o dejarlo fuera |
| 42 | Reparto ataque / defensa | No se sabe qué hace el equipo de ataque | Pregunta a la mesa (anexo, 5) |
| 43 | ¿Se entrega también en PPTX o PDF? | Solo se pidió libreto + HTML | Decidir el formato |
| 44 | ¿Presentación formal o conversación con apoyo visual? | Cambia la duración (decisión 1) y el tono del guion | Confirmar el formato de la entrevista |
