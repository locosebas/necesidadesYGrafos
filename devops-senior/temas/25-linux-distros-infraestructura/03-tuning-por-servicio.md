# Afinado (tuning) de Linux según el tipo de servicio

Lo que realmente diferencia a un servidor de base de datos de uno web no es
la distro: es **el mismo Linux configurado distinto**. Este archivo es el
bloque 1.11 de la Fase 1 y se automatiza con Ansible en la Fase 2.

## Siglas que se usan aquí

- **THP (Transparent Huge Pages)**: el kernel agrupa páginas de memoria de 4 KB en páginas de 2 MB automáticamente. Suele causar picos de latencia en bases de datos.
- **HugePages explícitas**: páginas grandes reservadas de antemano (`vm.nr_hugepages`). Las usan PostgreSQL y Oracle para su memoria compartida.
- **OOM killer (Out Of Memory killer)**: el kernel mata procesos cuando se queda sin memoria.
- **NUMA (Non-Uniform Memory Access)**: en servidores con varios sockets, cada CPU tiene memoria "cercana" y "lejana".

## Tabla de afinado por servicio

| Ajuste | PostgreSQL | MySQL/MariaDB | Oracle DB | Redis/Valkey | Elasticsearch/OpenSearch | Kafka | Web/API (Nginx) |
|---|---|---|---|---|---|---|---|
| **`vm.swappiness`** | 1–10 | 1 | Lo que fije el paquete preinstall | 1, poca swap | **Swap desactivada** (o `bootstrap.memory_lock`) | 1 | 10–60 |
| **THP** | Desactivar | Desactivar | **Desactivar** | **Desactivar** | Indiferente | Indiferente | Indiferente |
| **HugePages explícitas** | Sí (`huge_pages=on`) | Opcional | **Sí, recomendado** | No | No | No | No |
| **`vm.overcommit_memory`** | 2 (evita que el OOM killer mate a PostgreSQL) | 0 | Lo que fije el paquete preinstall | **1** (necesario para `BGSAVE`) | 0 | 0 | 0 |
| **Sistema de archivos** | XFS o ext4 con `noatime` | XFS o ext4 | XFS u Oracle ASM | Cualquiera | XFS o ext4 | **XFS** | Cualquiera |
| **Otros clave** | `vm.dirty_*`, scheduler `none`/`mq-deadline` en SSD/NVMe | `innodb_flush_method=O_DIRECT` | Límites en `/etc/security/limits.d`, semáforos | `net.core.somaxconn` | **`vm.max_map_count=262144`**, `nofile` 65535 | `nofile` muy alto, discos dedicados | `somaxconn`, `nofile`, ajustes TCP |

> ⚠️ Las recomendaciones cambian entre versiones (ej.: MongoDB 8 cambió su
> recomendación sobre THP). **Verifica siempre la documentación de tu
> versión** del motor.

## Otros factores en bases de datos

- NUMA: `numactl --hardware`; algunos motores recomiendan intercalar memoria (`numactl --interleave=all`).
- CPU governor en `performance` (`cpupower frequency-set -g performance`).
- Volúmenes separados para datos, WAL/redo log y backups.
- Planificador de I/O (`cat /sys/block/nvme0n1/queue/scheduler`).
- Límites de systemd en la unit del servicio: `LimitNOFILE=`, `OOMScoreAdjust=-1000` para proteger el proceso principal.

## Herramientas para aplicar perfiles

```bash
# tuned (RHEL/Rocky/Alma/Fedora)
sudo dnf install tuned && sudo systemctl enable --now tuned
tuned-adm list
sudo tuned-adm profile throughput-performance    # o latency-performance, virtual-guest
tuned-adm active

# Oracle Linux: todo lo que Oracle Database necesita en un comando
sudo dnf install oracle-database-preinstall-23ai   # el nombre cambia según la versión de Oracle

# sysctl persistente
cat <<EOF | sudo tee /etc/sysctl.d/90-postgres.conf
vm.swappiness = 1
vm.overcommit_memory = 2
vm.overcommit_ratio = 80
EOF
sudo sysctl --system

# Desactivar THP (temporal; para persistir: unit de systemd, tuned o parámetro de kernel)
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
cat /sys/kernel/mm/transparent_hugepage/enabled

# OpenSearch / Elasticsearch
echo "vm.max_map_count = 262144" | sudo tee /etc/sysctl.d/90-opensearch.conf
```

## Reto 1.F: granja de servicios con la distro correcta

Monta en tu laboratorio, idealmente sobre **Proxmox VE**:

| VM | Distro | Servicio |
|---|---|---|
| `fw01` | **VyOS** u OpenWrt | Router y firewall entre DMZ, LAN y gestión (reemplaza el router del Reto 1.A) |
| `nas01` | **TrueNAS SCALE** | NFS e iSCSI para el resto, con snapshots ZFS |
| `pbs01` | **Proxmox Backup Server** | Backups de todas las VMs |
| `db01`, `db02` | **Rocky Linux** | PostgreSQL primario + réplica, con `tuned` y sysctl de base de datos |
| `ora01` (opcional) | **Oracle Linux** | Oracle Database Free con el paquete preinstall |
| `cache01` | **Debian** | Redis/Valkey afinado (THP desactivado, overcommit = 1) |
| `search01` | **Ubuntu LTS** | OpenSearch con `max_map_count` y sin swap |
| `web01-03` | **Debian** | Nginx + app |
| `ids01` | **Security Onion** | Monitorea el tráfico de la DMZ (puerto espejo) |
| `dir01` | **Univention** o FreeIPA | Identidad central para todos |

### Preguntas del reto (de a una)

1. Justifica la distro de cada VM. ¿Qué perderías usando Ubuntu en todas? ¿Qué ganarías?
2. Corre `pgbench` en PostgreSQL **antes y después** del afinado (THP, HugePages, swappiness, scheduler). Mide y explica la diferencia.
3. ¿Por qué Redis falla al hacer `BGSAVE` con `vm.overcommit_memory=0` en un servidor con poca RAM libre? Reprodúcelo.
4. OpenSearch no arranca con `max virtual memory areas vm.max_map_count [65530] is too low`. Corrígelo de forma persistente con Ansible.
5. El OOM killer mató a PostgreSQL. ¿Qué configuración del kernel y de systemd lo evita?
6. Tu NAS con TrueNAS se cae. ¿Qué servicios dejan de funcionar? Rediseña para eliminar ese punto único de fallo.
7. Compara VyOS con un router Debian + nftables hecho a mano: mantenimiento, auditoría y rendimiento.
8. Diseña la política de actualizaciones: ¿cada cuánto y en qué orden actualizas firewall, base de datos y web? ¿Por qué ese orden?
9. Haz el inventario de EOL (End Of Life) de las 10 VMs y un plan de migración.
10. ¿Por qué THP perjudica a una base de datos? Explica el mecanismo (compactación de memoria, latencia).
11. Crea con **Packer** una *golden image* de base de datos (Rocky + sysctl + tuned + límites + agentes de monitoreo). ¿Cómo la mantienes parcheada cada mes?
12. ¿Qué parámetros de kernel **no** puedes cambiar en una base de datos gestionada (RDS/Cloud SQL) y cómo compensas?
