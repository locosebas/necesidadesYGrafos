# Chuleta de último minuto (leer 15 min antes de la entrevista)

## 1. Estructura de cualquier respuesta "de cero"

**Requisitos → Fundaciones (cuentas, identidad, red) → IaC → Cómputo →
Datos/secretos → CI/CD → Observabilidad → Seguridad → Resiliencia → Costos →
Prueba end-to-end.**

Arrancá con: *"Antes de elegir herramientas preguntaría…"*.
Cerrá con: *"Y lo validaría así: …"*.

## 2. Las tres fórmulas grandes en una línea

- **Kubernetes**: red con IPs para pods → cluster gestionado por Terraform →
  add-ons (Gateway API, cert-manager, external-dns, CSI, workload identity,
  external secrets, Kyverno) → Argo CD → namespaces + RBAC por grupos +
  quotas + NetworkPolicy default-deny + PSA restricted → CI con scan y firma
  → Prometheus/Grafana/OTel → PDB, probes, HPA, Velero → costos.
- **Red interna**: requisitos → cableado + core/distribución/acceso redundante
  → plan de IPs sin solapar con la nube → VLANs por función → inter-VLAN +
  default al firewall → DHCP relay/DNS/NTP/AD → firewall deny-by-default,
  DMZ, 802.1X, WPA3-Enterprise, invitados aislados → 2 ISP + VPN/SD-WAN →
  hub-spoke con la nube → monitoreo, syslog, backups de config, NetBox.
- **Terraform empresa**: bootstrap del estado (bucket versionado, cifrado,
  lock) → `modules/` + `live/<env>/<capa>` con estados chicos → versiones
  fijadas, tags por defecto → módulos con `for_each`, validaciones, versionados
  por tag → PR: fmt/validate/tflint/checkov/plan comentado → main: aprobación
  + apply del mismo plan con OIDC → drift nocturno → import/moved/removed.

## 3. Números y datos para tener a mano

| Dato | Valor |
|---|---|
| /24 · /23 · /22 · /26 · /30 | 254 · 510 · 1022 · 62 · 2 hosts útiles |
| IPs reservadas por subnet | AWS 5, Azure 5 |
| Rangos privados | 10/8, 172.16/12, 192.168/16 |
| 99,9% mensual | ≈ 43 min de caída |
| 99,99% mensual | ≈ 4,3 min |
| Puertos | SSH 22, DNS 53, HTTP 80, HTTPS 443, RDP 3389, Postgres 5432, MySQL 3306, K8s API 6443, kubelet 10250 |
| PSA niveles | privileged · baseline · restricted |
| QoS K8s | Guaranteed (req = lim) · Burstable · BestEffort (sin req/lim, se mata primero) |

## 4. Diferencias que suelen preguntar

- **Requests vs limits**: requests = lo que reserva el scheduler; limits =
  techo. CPU se *throttlea*, memoria se **OOMKill**.
- **Liveness vs readiness**: liveness reinicia el contenedor; readiness lo
  saca del Service sin reiniciar.
- **HPA vs VPA vs Cluster Autoscaler**: más pods / pods más grandes / más nodos.
- **Service ClusterIP / NodePort / LoadBalancer**, **Ingress vs Gateway API**
  (Gateway separa roles: infra define Gateway, equipos definen Routes).
- **NSG vs Azure Firewall**: filtro L3/L4 por subnet/NIC vs firewall central
  L3–L7 con FQDN. AWS: **Security Group (stateful, por ENI) vs NACL
  (stateless, por subnet)**.
- **Private Endpoint vs Service Endpoint** (Azure): IP privada en tu VNet vs
  ruta optimizada a la IP pública del servicio.
- **Managed Identity system vs user-assigned**: atada al ciclo de vida del
  recurso vs independiente y reutilizable.
- **Blue/green vs canary**: todo el tráfico de golpe con rollback instantáneo
  vs porcentaje gradual midiendo.
- **Terraform state**: mapa código ↔ realidad; remoto, cifrado, con lock.
- **CI vs CD (delivery vs deployment)**: delivery = listo para prod con botón;
  deployment = llega solo a prod.

## 5. Troubleshooting en 1 línea

- Pod **Pending** → `describe` (recursos, taints, PVC).
- **CrashLoopBackOff** → `logs --previous`.
- **OOMKilled** → limit de memoria.
- **ImagePullBackOff** → tag/permiso del registry.
- Service sin respuesta → `get endpoints` (selector/readiness/NetworkPolicy).
- Red: **de abajo hacia arriba** — link → VLAN → IP/gateway → ruta → firewall/puerto → DNS → app/TLS.
- "Anda en dev y no en prod" → diff de config, permisos (identidad), red privada/DNS.

## 6. Respuestas de comportamiento (formato STAR)

Situación → Tarea → Acción (qué hiciste **vos**) → Resultado (con número).
Tené listas 3 historias:
1. Un incidente en producción que resolviste (MercadoLibre, alto volumen).
2. Algo que automatizaste con IaC/CI/CD y cuánto tiempo/errores ahorró (Bizagi).
3. Un desacuerdo técnico y cómo se resolvió.

## 7. Preguntas para hacerle al entrevistador

- ¿Cómo es hoy el flujo desde un commit hasta producción?
- ¿Qué parte de la infra todavía no está en código?
- ¿Cómo es el on-call y cuántos incidentes tienen por mes?
- ¿Cuál es el mayor problema técnico que esperan que resuelva esta persona en los primeros 90 días?

## 8. Actitud

- Si no sabés algo: *"No lo usé directamente, pero lo resolvería así…"* y
  razoná con los principios (mínimo privilegio, todo como código, medir).
- Pensá en voz alta, mencioná **trade-offs** (costo vs disponibilidad,
  simplicidad vs control). Eso es lo que evalúan en un senior.
