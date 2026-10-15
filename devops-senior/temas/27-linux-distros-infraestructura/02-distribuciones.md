# Distribuciones de Linux: cuáles hay y para qué sirve cada una

Una **distribución (distro)** es un sistema operativo completo construido
sobre el kernel Linux: gestor de paquetes, herramientas, ciclo de soporte y
filosofía propia.

> ⚠️ **Idea clave**: las bases de datos (PostgreSQL, MySQL, Oracle, MongoDB,
> Redis) casi nunca tienen "su distro". Corren sobre **distros de servidor de
> propósito general**. Lo que cambia es **qué distro eliges** (soporte,
> certificación del fabricante) y **cómo afinas el kernel** (ver
> `03-tuning-por-servicio.md`). Lo que sí existe son **distros de propósito
> específico** (*appliances*) para firewall, NAS, virtualización, nodos de
> Kubernetes, etc.

## 1. Por familia

### Familia Debian
| Distro | Para qué sirve |
|---|---|
| **Debian** | Muy estable y conservadora; servidores; base de muchas otras |
| **Ubuntu** | La más popular: escritorio, servidores y nube; enorme documentación |
| **Linux Mint** | Basada en Ubuntu, interfaz parecida a Windows; ideal para empezar |
| **Pop!_OS** | System76; desarrolladores y gamers, buen soporte de GPU NVIDIA |
| **Kali Linux / Parrot** | Pentesting (pruebas de penetración); no para uso diario |
| **Raspberry Pi OS** | Placas Raspberry Pi |

### Familia Red Hat
| Distro | Para qué sirve |
|---|---|
| **RHEL** (Red Hat Enterprise Linux) | Empresas, soporte comercial de pago |
| **Fedora** | Moderna, software reciente; "laboratorio" de lo que llegará a RHEL |
| **Rocky Linux / AlmaLinux** | Clones gratuitos compatibles con RHEL (reemplazan a CentOS) |
| **Oracle Linux** | Compatible con RHEL, con kernel UEK; referencia para Oracle Database |

### Familia Arch
| Distro | Para qué sirve |
|---|---|
| **Arch Linux** | Minimalista, *rolling release*; armas todo pieza a pieza |
| **Manjaro / EndeavourOS** | Arch con instalación sencilla |
| **SteamOS** | Valve, Steam Deck, juegos |

### Otras
- **openSUSE** (Leap y Tumbleweed) y **SLES** (SUSE Linux Enterprise Server): sólidas, herramienta YaST.
- **Alpine Linux**: diminuta (~5 MB), favorita para contenedores.
- **Gentoo**: todo compilado desde el código fuente.
- **NixOS**: sistema declarativo y reproducible con un solo archivo.
- **Tails**: privacidad, arranca desde USB y usa Tor.
- **Android** y **ChromeOS** usan el kernel Linux.

## 2. Distros de servidor de propósito general (donde corren las bases de datos)

| Distro | Soporte | Cuándo elegirla |
|---|---|---|
| **RHEL** | 10 años o más | Empresas que necesitan certificación de fabricantes (Oracle, SAP, bancos). Incluye **RHEL for SAP Solutions** |
| **Rocky / AlmaLinux** | 10 años | Compatibles con RHEL y gratuitas; muy usadas para PostgreSQL y MySQL on-prem |
| **Oracle Linux** | 10 años o más | **Referencia para Oracle Database**: kernel UEK (Unbreakable Enterprise Kernel) y el paquete `oracle-database-preinstall-*` que configura el kernel automáticamente |
| **SLES** (SUSE) | 10 años o más | **SAP HANA**: SLES for SAP Applications es la plataforma más usada para SAP |
| **Ubuntu Server LTS** (Long Term Support) | 5 años (hasta 10 o más con Ubuntu Pro) | Nube y startups; PostgreSQL, MySQL, MongoDB; la más documentada |
| **Debian stable** | Unos 5 años (con LTS) | Servidores estables sin sorpresas; muchos DBA prefieren Debian para PostgreSQL |

**Regla para bases de datos**:
1. Distro **LTS o empresarial**, nunca *rolling release* (como Arch).
2. **Certificada por el fabricante** si el motor es comercial (Oracle → Oracle Linux o RHEL; SAP HANA → SLES o RHEL).
3. Repositorios **oficiales del proyecto** para tener versiones actuales (ej.: `apt.postgresql.org` en Debian/Ubuntu o el repositorio PGDG (PostgreSQL Global Development Group) en RHEL/Rocky).
4. Revisar la fecha de **EOL** (End Of Life) de la distro **y** del motor: https://endoflife.date/

## 3. Distros especializadas por tipo de servicio (*appliances*)

| Servicio | Distribución | Base | Notas |
|---|---|---|---|
| **Virtualización** | **Proxmox VE** | Debian | KVM + contenedores LXC + Ceph + clustering. Ideal para el laboratorio |
| | **XCP-ng** | Xen | Alternativa libre a Citrix Hypervisor |
| | **Harvester** | SUSE | Hiperconvergente sobre Kubernetes (VMs en K8s) |
| **Backups** | **Proxmox Backup Server** | Debian | Backups deduplicados de VMs y servidores |
| **Almacenamiento / NAS** (Network Attached Storage) | **TrueNAS SCALE** | Debian | ZFS, SMB, NFS, iSCSI y apps |
| | **OpenMediaVault** | Debian | NAS ligero (incluso en Raspberry Pi) |
| | **Unraid** | Slackware | NAS doméstico/laboratorio (de pago) |
| **Router / firewall** | **OpenWrt** | Linux embebido | Routers físicos y VMs |
| | **VyOS** | Debian | Router empresarial con CLI estilo Juniper/Cisco: BGP, OSPF, VPN |
| | **IPFire** | Propia | Firewall con IDS/IPS (Intrusion Detection/Prevention System) |
| | *(pfSense / OPNsense)* | ⚠️ **FreeBSD, no Linux** | Muy populares, pero no son Linux |
| **Oficina / identidad** | **Univention Corporate Server** | Debian | Directorio compatible con Active Directory |
| | **Zentyal** | Ubuntu | Reemplazo de Windows Server en pymes (AD, DNS, DHCP, correo) |
| | **FreeIPA** (no es distro, se instala en RHEL/Rocky/Fedora) | — | Identidad Linux: LDAP + Kerberos + DNS + CA |
| **Seguridad / SIEM** (Security Information and Event Management) | **Security Onion** | Oracle Linux | Detección de intrusiones, análisis de red y logs (Suricata, Zeek, Elastic) |
| | **Kali / Parrot** | Debian | Atacar (pentesting), no defender |
| **Telefonía VoIP** | **FreePBX Distro / Issabel** | Rocky/Debian | Centralitas basadas en Asterisk |
| **Appliances listos** | **TurnKey Linux** | Debian | Más de 100 imágenes listas: PostgreSQL, MySQL, LAMP, GitLab, WordPress… |
| **Domótica / IoT** | **Home Assistant OS** | Buildroot | Automatización del hogar |
| **Embebidos** | **Yocto / Buildroot** | — | No son distros: son *herramientas para construir tu propia distro* (coches, routers, equipos médicos) |
| **Tiempo real** | RHEL for Real Time, Ubuntu Pro real-time kernel | — | Telecomunicaciones, industria, trading |
| **HPC** (High Performance Computing) | Rocky Linux + Warewulf/OpenHPC | — | Supercomputación |

## 4. Imágenes base para contenedores (Fase 3)

| Imagen base | Tamaño aprox. | Uso |
|---|---|---|
| **Alpine** | ~5 MB | Mínima. Usa *musl* en vez de glibc: puede dar problemas con Python o Java |
| **Debian slim** | ~30 MB | Compatibilidad total con glibc; opción segura por defecto |
| **Ubuntu** | ~30 MB | Cuando necesitas paquetes de Ubuntu |
| **Red Hat UBI** (Universal Base Image) | ~40–100 MB | Base de RHEL redistribuible y gratis; certificada en OpenShift |
| **Distroless** (Google) | ~2–20 MB | Sin shell ni gestor de paquetes: mínima superficie de ataque |
| **Wolfi / Chainguard** | Pequeñas | Diseñadas para cero CVEs (Common Vulnerabilities and Exposures), con SBOM (Software Bill of Materials) |
| **scratch** | 0 MB | Imagen vacía, para binarios estáticos (Go, Rust) |

**Imágenes de bases de datos**: usar las **oficiales** (`postgres`, `mysql`,
`mariadb`, `redis`/`valkey`, `mongo`) o las de los operadores (CloudNativePG
publica las suyas). Cuidado con imágenes de terceros sin mantenimiento.

## 5. Distros para nodos de Kubernetes (Fase 4)

| Distro | Características |
|---|---|
| **Ubuntu / Debian / Rocky** | Clásicas con kubeadm; lo que usas para aprender |
| **Talos Linux** | **Sin SSH ni shell**, se gestiona solo por API, inmutable, hecha solo para Kubernetes |
| **Flatcar Container Linux** | Inmutable, actualizaciones atómicas; sucesor de CoreOS |
| **Fedora CoreOS** | Inmutable; base de RHCOS (Red Hat CoreOS) en OpenShift |
| **Bottlerocket** (AWS) | Inmutable, para EKS y ECS |
| **Container-Optimized OS** (Google) | Nodos de GKE |
| **Azure Linux** (Microsoft) | Nodos de AKS |

> Ojo: **RKE2, k3s, OpenShift, Rancher, Tanzu** no son distros de sistema
> operativo: son **distribuciones de Kubernetes**.

## 6. Distros de la nube (Fase 5)

| Distro | Proveedor |
|---|---|
| **Amazon Linux 2023** | AWS (basada en Fedora, optimizada para EC2) |
| **Azure Linux** | Microsoft (nodos de AKS y servicios de Azure) |
| **Container-Optimized OS** | Google Cloud |
| **Ubuntu Pro / RHEL / SLES** en el marketplace | Todas las nubes (licencia incluida en el precio por hora) |

Con **bases de datos gestionadas** (Amazon RDS, Cloud SQL, Azure Database)
**no eliges ni ves el sistema operativo**: el proveedor lo afina y lo
parchea. Ese control perdido es el *trade-off* frente a montarlo tú en una VM
o con un operador en Kubernetes.

## 7. Recomendación rápida según uso

| Uso | Distro |
|---|---|
| Empezar desde Windows | Linux Mint, Ubuntu |
| Programar | Fedora, Ubuntu, Pop!_OS |
| Servidores generales | Debian, Ubuntu Server, Rocky, Alma |
| PostgreSQL / MySQL on-prem | Rocky/Alma, Debian, Ubuntu LTS |
| Oracle Database | Oracle Linux, RHEL |
| SAP HANA | SLES for SAP, RHEL for SAP |
| Laboratorio de virtualización | Proxmox VE |
| NAS | TrueNAS SCALE, OpenMediaVault |
| Router / firewall | VyOS, OpenWrt, IPFire |
| Nodos de Kubernetes on-prem | Talos, Flatcar, Ubuntu/Rocky + kubeadm |
| Contenedores | Alpine, Debian slim, distroless, Wolfi |
| Aprender Linux a fondo | Arch, Gentoo |
| Ciberseguridad ofensiva | Kali, Parrot |
| Equipos viejos | Lubuntu, Xubuntu, antiX |

## Preguntas (de a una)

1. ¿Por qué no se pone Oracle Database sobre Debian aunque "funcione"?
2. ¿Qué diferencia hay entre una distro de propósito general y un *appliance*? Da 3 ejemplos de *appliances*.
3. ¿Por qué una base de datos no debería ir sobre una distro *rolling release*?
4. pfSense y OPNsense: ¿qué tienen de particular frente a VyOS?
5. ¿Qué ataques elimina un sistema operativo inmutable (Talos, Flatcar, Bottlerocket) y cuáles no?
6. ¿Cómo diagnosticas un nodo Talos si no tiene SSH?
7. Una auditoría exige "sistema operativo con soporte vigente": ¿cómo haces el inventario de EOL de 10 servidores y el plan de migración?
8. RHEL vs. Rocky vs. Alma vs. Oracle Linux: ¿cuándo pagas RHEL?
9. Tu app Python va 3 veces más lenta en Alpine que en Debian slim. ¿Por qué?
10. ¿Cómo depuras un contenedor distroless que no tiene shell?
11. RKE2 y OpenShift, ¿son distros de Linux? ¿Qué son?
12. ¿Qué pierdes y qué ganas con una base de datos gestionada (RDS/Cloud SQL) frente a una VM con Rocky afinada por ti?
