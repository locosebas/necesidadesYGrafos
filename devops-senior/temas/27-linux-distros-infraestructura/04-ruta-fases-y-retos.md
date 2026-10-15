# Ruta por fases y retos de arquitectura NubeShop

Las preguntas de cada reto se trabajan **de a una**: se responde, se
corrige, y se pasa a la siguiente. La Fase 4 (Kubernetes) está en su propio
archivo: `05-kubernetes-instalacion-y-kit.md`.

**Siglas frecuentes**: HA (High Availability, alta disponibilidad) · VIP
(Virtual IP) · VRRP (Virtual Router Redundancy Protocol) · RPO (Recovery
Point Objective, cuántos datos puedes perder) · RTO (Recovery Time
Objective, cuánto puedes tardar en recuperarte) · PITR (Point-In-Time
Recovery) · DR (Disaster Recovery) · SLO (Service Level Objective).

---

# FASE 1: Solo Linux (sin contenedores ni nube)

**Objetivo:** administrar servidores Linux como profesional y entender
*qué hay debajo* de Docker y Kubernetes.

### Laboratorio

- Hipervisor: **KVM/libvirt** (`virt-manager`), VirtualBox o **Proxmox VE**.
- **Vagrant** para VMs reproducibles.
- 6 a 10 VMs ligeras (Debian, Rocky, Ubuntu Server) de 1 a 2 GB de RAM.

### Temario

| Bloque | Contenido |
|---|---|
| **1.1 Usuario avanzado** | Shell, tuberías, grep/sed/awk/jq, vim, tmux, regex, `find` + `xargs` |
| **1.2 Administración** | Usuarios, grupos, sudoers, permisos, ACL, paquetes, repos propios, systemd (units, timers, targets), journald, cron, logrotate |
| **1.3 Arranque y kernel** | UEFI, GRUB, initramfs, módulos, `sysctl`, modo rescate, recuperar contraseña de root |
| **1.4 Almacenamiento** | GPT, ext4/XFS/Btrfs, LVM (snapshots, ampliar en caliente), RAID con mdadm, fstab, swap, NFS, iSCSI, cuotas |
| **1.5 Redes** | TCP/IP, subredes/CIDR, `ip`, routing, bridges, VLANs, bonding, NAT, **nftables**, DNS (BIND/Unbound), DHCP (Kea/dnsmasq), NTP (chrony), `tcpdump` |
| **1.6 Servicios** | Nginx (web y proxy inverso), HAProxy, keepalived (VIP), PostgreSQL (replicación), Redis, SSH avanzado (ProxyJump, túneles) |
| **1.7 Seguridad** | Hardening SSH, fail2ban, SELinux/AppArmor, auditd, PKI propia con openssl, TLS, WireGuard, Lynis, mínimo privilegio |
| **1.8 Rendimiento** | `htop`, `vmstat`, `iostat`, `sar`, `perf`, `strace`, `lsof`, OOM killer, `ulimit`, cgroups v2, namespaces |
| **1.9 Bash avanzado** | Funciones, `set -euo pipefail`, `trap`, `getopts`, arrays, idempotencia, ShellCheck |
| **1.10 Observabilidad clásica** | rsyslog central, Prometheus + node_exporter + Grafana + Alertmanager como binarios con systemd |
| **1.11 Distros por propósito y afinado** | Ver `02-distribuciones.md` y `03-tuning-por-servicio.md` |

## Reto 1.A: Red corporativa simulada

- **Router/firewall Linux** con 3 interfaces: DMZ `10.10.10.0/24`, LAN `10.10.20.0/24`, gestión `10.10.99.0/24`.
- NAT de salida y reglas **nftables**: la DMZ no puede iniciar conexiones a la LAN; solo gestión entra por SSH.
- **DNS interno** (zona `nubeshop.lab` + inversa) y **DHCP** con reservas por MAC.
- **Bastión SSH** como única entrada (`ProxyJump`), claves + 2FA (TOTP).
- **NTP** sincronizado en todas las máquinas.

Preguntas:
1. ¿Por qué no se pone el bastión en la LAN?
2. ¿Cómo demuestras con `tcpdump` que el NAT funciona?
3. Si el DNS cae, ¿qué servicios se rompen y en qué orden?
4. Diseña el plan de direccionamiento IP para crecer a 10 subredes sin rehacer nada.

## Reto 1.B: NubeShop v1, web en alta disponibilidad

- 2 balanceadores **HAProxy** con **keepalived** compartiendo una VIP (VRRP).
- 3 servidores **Nginx** con la app como servicio systemd y usuario sin privilegios.
- **PostgreSQL** primario + réplica por *streaming replication*, con **PgBouncer**.
- **Redis** para sesiones y caché.
- **TLS** de tu CA interna, renovación con un systemd timer.
- **Workers** que procesan pedidos desde una cola (RabbitMQ o Redis Streams).

Preguntas:
1. Apaga el HAProxy maestro: ¿cuánto tarda la VIP en moverse? ¿Se pierden conexiones?
2. El primario de PostgreSQL muere. Escribe el runbook de failover manual. ¿Qué pasa con las escrituras en vuelo?
3. ¿Qué es un *split-brain* en keepalived o PostgreSQL y cómo lo evitas?
4. ¿Dónde termina el TLS, en HAProxy o en Nginx? Justifica seguridad y rendimiento.
5. ¿Cómo haces un despliegue sin caída (*rolling* manual con HAProxy)?
6. Las sesiones se pierden al cambiar de backend: ¿por qué y qué soluciones hay?

## Reto 1.C: Almacenamiento, backups y DR

- Servidor de archivos con **RAID 1 + LVM**, exportado por **NFS** a los 3 Nginx (imágenes de productos).
- Backups con **Borg** o **restic**: PostgreSQL (`pg_basebackup` + WAL archiving para PITR), `/etc` de todos los servidores y el NFS.
- Retención 7 diarios / 4 semanales / 6 mensuales, copia en otra "sede".
- **Simulacro**: borra la base de datos y recupérala al estado de hace 15 minutos.

Preguntas:
1. Define el RPO y el RTO de NubeShop v1 y demuestra que los cumples.
2. ¿Por qué RAID no es un backup?
3. Falla un disco del RAID: reemplázalo en caliente y documenta los pasos.
4. ¿Cómo sabes que un backup sirve sin restaurarlo completo?
5. El NFS es un punto único de fallo: propón 2 alternativas (DRBD + Pacemaker, GlusterFS, Ceph).

## Reto 1.D: Identidad, auditoría y monitoreo central

- **FreeIPA** u **OpenLDAP + SSSD**: login central, grupos `devs`, `ops`, `dba`, sudo por grupo, claves SSH en LDAP.
- **rsyslog** central con TLS y **auditd** (quién ejecutó qué con sudo).
- **Prometheus + Grafana + Alertmanager**: disco > 85 %, lag de réplica, backend caído en HAProxy, certificado por vencer.

Preguntas:
1. Un empleado se va: ¿cómo le quitas el acceso a 10 servidores en 1 minuto?
2. ¿Cuáles son las *golden signals* (latencia, tráfico, errores, saturación) de NubeShop?
3. Diseña alertas que no despierten a nadie por falsos positivos.

## Reto 1.E: Multi-sede con VPN

- Dos "sedes" unidas por **WireGuard** sitio a sitio.
- Réplica de PostgreSQL y destino de backups en la sede B.
- Enrutamiento entre sedes y DNS *split-horizon*.

Preguntas:
1. Cae el enlace VPN: ¿qué deja de funcionar y qué sigue?
2. ¿Cómo promueves la sede B si la sede A se incendia?

## Reto 1.F: Granja de servicios con la distro correcta

Ver `03-tuning-por-servicio.md` (VyOS, TrueNAS, Proxmox Backup Server,
Rocky + PostgreSQL afinado, Oracle Linux, Security Onion, etc.).

✅ **Criterio para pasar de fase:** reconstruyes NubeShop v1 a mano, explicas
cada salto de red y te recuperas de la caída de cualquier componente.

---

# FASE 2: Automatización (Git, Bash avanzado, Ansible)

**Objetivo:** que ningún servidor se configure a mano nunca más.

**Temario**: Git en equipo · **Ansible** (inventarios, playbooks, roles,
precedencia de variables, handlers, Jinja2, **Ansible Vault**, idempotencia,
tests con **Molecule**) · Vagrant + Ansible · **Packer** (*golden images*).

## Retos

- **2.A**: convierte toda la Fase 1 en un repo Ansible con roles (`common`, `hardening`, `tuning-db`, `router`, `dns`, `haproxy`, `nginx`, `app`, `postgres`, `redis`, `monitoring`, `backup`). Meta: `vagrant up && ansible-playbook site.yml` levanta NubeShop v1 en menos de 30 minutos.
- **2.B**: despliegue sin caída: `serial: 1`, sacar cada backend de HAProxy por su socket de administración, desplegar, *health check*, devolverlo; rollback automático si falla.
- **2.C**: entornos `dev`, `staging`, `prod` con el mismo código y distintos inventarios; secretos con Vault.
- **2.D**: roles probados con Molecule en CI en cada push.
- **2.E**: el afinado del archivo `03` (sysctl, THP, tuned, límites) como rol `tuning-db` con variables por motor (PostgreSQL, Redis, OpenSearch).

## Preguntas

1. ¿Qué hace que una tarea sea *idempotente*? Da 3 ejemplos que no lo son y corrígelos.
2. ¿Cómo aplicas un cambio en 200 servidores de forma escalonada?
3. Alguien cambió un servidor a mano: ¿cómo detectas la *deriva de configuración*?
4. ¿Ansible o Bash? ¿Cuándo cada uno?
5. *Push* (Ansible) vs. *pull* (Puppet, Chef): ventajas de cada modelo.
6. Diseña la estructura de repo para 10 personas y 5 proyectos.
7. ¿Cómo rotas la contraseña de PostgreSQL en todos los servicios sin caída?
8. ¿Qué es la *infraestructura inmutable* y cómo cambia tu uso de Ansible?

---

# FASE 3: Contenedores (Docker y Podman)

**Objetivo:** empaquetar NubeShop y entender que un contenedor es **un
proceso Linux con namespaces + cgroups + overlayfs**.

**Temario**: namespaces, cgroups v2, overlayfs, capabilities, seccomp ·
imágenes, capas, Dockerfile multi-etapa, volúmenes, redes, Compose ·
rootless, imágenes base (ver `02-distribuciones.md` sección 4), **Trivy**,
**cosign**, SBOM · registry **Harbor** · 12 factores, logs a stdout,
healthchecks, apagado ordenado (SIGTERM).

## Retos

- **3.A Un contenedor sin Docker**: `unshare`, `chroot`/`pivot_root`, cgroups e `ip netns` para correr un proceso aislado con su red y límite de memoria. Explica cada paso.
- **3.B NubeShop v2 en Compose**: `frontend`, `api` (x3), `worker` (x2), `postgres` + réplica, `redis`, `rabbitmq`, `minio` (S3, reemplaza al NFS), `traefik` con TLS. Redes `public`, `app`, `data` (solo la API llega a la base de datos). Healthchecks, `depends_on` con condición, límites, volúmenes, secretos. Observabilidad: Prometheus, Grafana, Loki, cAdvisor.
- **3.C Cadena de suministro**: CI que construye multi-etapa, escanea con Trivy (falla con CVEs críticos), genera SBOM, firma con cosign y sube a Harbor; solo se aceptan imágenes firmadas.
- **3.D Contenedores sin orquestador**: NubeShop v2 en las VMs de la Fase 1 con **Podman + Quadlet** (units de systemd) y Ansible.
- **3.E Imágenes base**: construye la API con Alpine, Debian slim y distroless; compara tamaño, CVEs y arranque.

## Preguntas

1. Contenedor vs. VM a nivel de kernel.
2. La imagen pesa 1,2 GB: redúcela a menos de 50 MB.
3. ¿Por qué `docker stop` tarda 10 segundos? (PID 1 y señales.)
4. PostgreSQL en contenedor: ¿cómo garantizas no perder datos al recrearlo?
5. ¿Qué riesgos tiene montar `/var/run/docker.sock` en un contenedor?
6. Dos contenedores en redes distintas deben hablar: opciones y la más segura.
7. ¿Qué pasa con los logs si la app escribe en un archivo y no en stdout?
8. ¿Qué le falta a Compose para producción a gran escala? (Esa lista es la motivación de Kubernetes.)
9. `ENTRYPOINT` vs. `CMD`; forma *exec* vs. forma *shell*.
10. Estrategia de etiquetas (`latest` vs. semver vs. SHA del commit). ¿Por qué no `latest` en producción?

---

# FASE 4: Kubernetes

Ver **`05-kubernetes-instalacion-y-kit.md`**.

---

# FASE 5: Cloud, IaC y CI/CD

**Objetivo:** todo en la nube, 100 % como código. (Se apoya en los temas
`01-iac-multicloud`, `03-cicd-multicloud`, `04-identidad-iam` y
`05-networking-multicloud`.)

**Temario**: VPC/subredes, IAM, VMs, balanceadores, objetos, bases de datos
gestionadas, DNS, EKS/GKE/AKS · **Terraform/OpenTofu** (estado remoto con
bloqueo, módulos, entornos, `plan` en PR, deriva, Terragrunt) · GitHub
Actions/GitLab CI con OIDC (OpenID Connect) hacia la nube · SBOM, cosign,
SLSA, Renovate · FinOps (spot, *rightsizing*, OpenCost) · distros de nube
(ver `02-distribuciones.md` sección 6) · *golden images* con Packer.

## Retos

- **5.A Red cloud de producción con Terraform**: VPC en 3 zonas, subredes públicas/privadas/datos, NAT, acceso sin bastión (SSM o IAP), VPN hacia el laboratorio on-prem (nube híbrida).
- **5.B NubeShop v4**: clúster gestionado con Terraform, Karpenter, base de datos gestionada multi-zona, S3/GCS, CDN, DNS gestionado, WAF, secretos vía External Secrets.
- **5.C Pipeline completo**: PR → lint + tests + `terraform plan` comentado + escaneo → merge → build → firma → push → actualizar repo GitOps → Argo CD → canary → producción. Nadie escribe directo en producción.
- **5.D Entornos efímeros**: cada PR crea namespace con URL propia (`pr-123.dev.nubeshop.com`) y base de datos semilla; se destruye al cerrar.
- **5.E Golden image de base de datos**: Packer (Rocky + afinado del archivo `03`) + Terraform. Compárala con la base de datos gestionada.

## Preguntas

1. ¿Dónde guardas el estado de Terraform y por qué necesita bloqueo?
2. Alguien cambió un recurso desde la consola: ¿cómo lo detectas y corriges?
3. Módulos para 3 entornos y 4 regiones sin duplicar código.
4. ¿Por qué OIDC en vez de una access key en la CI?
5. Base de datos gestionada vs. operador en Kubernetes: coste, control, operación.
6. IAM con mínimo privilegio para la CI, Argo CD, los pods de la API (IRSA / Workload Identity) y los desarrolladores.
7. La factura se duplicó este mes: ¿cómo investigas y qué palancas tienes?
8. ¿Cómo conectas de forma segura el clúster en la nube con la base de datos on-prem durante una migración gradual?
9. ¿Qué fuerza a usar NAT Gateway y cómo reduces su coste?
10. ¿Cómo haces un `terraform destroy` que nunca borre la base de datos de producción?
11. PostgreSQL en EC2 con Rocky afinado vs. RDS: coste, rendimiento, control y horas de operación al mes.

---

# FASE 6: SRE y proyecto final

**Temario**: SLIs/SLOs/SLAs, presupuestos de error, guardias, gestión de
incidentes, *postmortems* sin culpables, caos (**Chaos Mesh**, **LitmusChaos**),
carga (**k6**), capacidad, DR multi-región, *platform engineering* (ver tema
`23-platform-engineering`).

## Proyecto final: NubeShop v5 global

- **2 regiones** activo-pasivo (o activo-activo en lecturas), DNS con failover y health checks.
- Réplica de base de datos entre regiones; RPO y RTO definidos **y demostrados**.
- Un clúster por región, un solo Argo CD con ApplicationSets.
- Mesh con mTLS, canary automático y rollback por SLO.
- Observabilidad global (Thanos o Mimir, logs y trazas centralizados, dashboards de SLO).
- Imágenes firmadas, políticas, auditoría, rotación automática de secretos, escaneo continuo.
- Runbooks de los 10 incidentes más probables.
- **Game day**: otra persona rompe cosas sin avisar; tú detectas y resuelves.

## Preguntas finales de arquitectura

1. Cae una región entera de la nube: narra minuto a minuto qué pasa, qué es automático y qué es manual.
2. Un despliegue corrompió datos hace 3 horas y nadie lo notó: ¿cómo recuperas sin perder los pedidos legítimos de esas 3 horas?
3. NubeShop para 10 millones de usuarios: ¿qué cambia (caché, CDN, sharding, colas, CQRS)?
4. ¿Cuánto cuesta pasar de 99,9 % a 99,99 %? ¿Vale la pena para NubeShop?
5. Expiró un certificado y tumbó producción: escribe el postmortem y 3 acciones para que no se repita.
6. etcd de producción está corrupto y el último snapshot tiene 24 horas: ¿qué haces? ¿Qué pierdes realmente si usas GitOps?
7. Un atacante entra a un pod de la API: ¿hasta dónde llega? Diseña la defensa en profundidad capa por capa (Linux, contenedor, Kubernetes, red, nube).
8. El equipo de datos necesita una copia diaria de producción anonimizada: diseña el pipeline.
9. Migrar NubeShop de AWS a GCP sin caída: ¿qué partes lo facilitan y cuáles lo dificultan?
10. Diseña la plataforma interna para que un desarrollador nuevo despliegue un microservicio a producción el primer día sin saber Kubernetes.
