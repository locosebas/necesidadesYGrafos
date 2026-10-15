# Fundamentos de Linux: todo lo esencial

Guía de referencia de lo que un administrador o ingeniero de plataforma debe
dominar de Linux. Es la base del temario de la Fase 1 (ver
`04-ruta-fases-y-retos.md`).

## 1. Conceptos fundamentales

- **Kernel**: el núcleo que creó Linus Torvalds en 1991. Gestiona CPU,
  memoria, dispositivos y procesos. Linux es *técnicamente* solo el kernel.
- **GNU/Linux**: el kernel más las herramientas del proyecto GNU (bash,
  coreutils, gcc…). Juntos forman el sistema operativo.
- **Distribución (distro)**: kernel + gestor de paquetes + herramientas +
  (opcionalmente) entorno gráfico + una filosofía propia. Ver `02-distribuciones.md`.
- **Licencia**: el kernel Linux es GPL v2 (GNU General Public License): puedes
  usarlo, estudiarlo, modificarlo y redistribuirlo.
- **Filosofía Unix**: programas pequeños que hacen *una cosa bien* y se
  combinan con tuberías (`|`).
- **"Todo es un archivo"**: dispositivos, procesos y sockets se representan
  como archivos (`/dev/sda`, `/proc/1234`).

## 2. Sistema de archivos: FHS (Filesystem Hierarchy Standard)

No hay `C:\`. Todo cuelga de una sola raíz `/`:

| Ruta | Contenido |
|---|---|
| `/` | Raíz del sistema |
| `/home/usuario` | Archivos personales (`~`) |
| `/root` | Carpeta personal del superusuario |
| `/etc` | Archivos de configuración |
| `/bin`, `/usr/bin` | Programas (comandos) |
| `/sbin`, `/usr/sbin` | Programas de administración |
| `/var` | Datos variables: logs (`/var/log`), cachés, bases de datos |
| `/tmp` | Temporales |
| `/dev` | Dispositivos (discos, USB, terminales) |
| `/proc`, `/sys` | Información virtual del kernel y los procesos |
| `/boot` | Kernel y gestor de arranque |
| `/mnt`, `/media` | Puntos de montaje |
| `/opt` | Software de terceros |
| `/lib` | Bibliotecas compartidas |

**Sistemas de archivos**: ext4 (estándar), XFS (servidores y bases de datos),
Btrfs (snapshots), ZFS; FAT32/exFAT/NTFS para compatibilidad.

**Rutas**: absolutas desde `/` (`/home/ana/doc.txt`) o relativas
(`../doc.txt`). `.` = directorio actual, `..` = padre, `~` = tu home.

## 3. La terminal y el shell

El **shell** interpreta los comandos: **bash** (estándar), **zsh**, **fish**.

### Comandos esenciales

```bash
# Navegación y archivos
pwd; ls -la; cd /ruta; cd -
mkdir -p a/b/c; touch archivo
cp -r origen dest; mv viejo nuevo; rm -r carpeta   # ¡no hay papelera!
ln -s destino enlace

# Ver y buscar
cat archivo; less archivo; head -n 20 archivo; tail -n 20 archivo
tail -f /var/log/syslog
grep -rn "texto" .
find / -name "*.conf"
which python; wc -l archivo

# Ayuda
man comando; comando --help; tldr comando
```

### Redirecciones y tuberías

```bash
comando > archivo      # sobrescribe
comando >> archivo     # añade al final
comando 2> errores     # stderr
comando &> todo.log    # stdout + stderr
comando < entrada
cmd1 | cmd2

# Las 10 IPs que más visitan el servidor
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head
```

**Atajos**: `Tab` autocompletar · `Ctrl+C` cancelar · `Ctrl+R` buscar en el
historial · `Ctrl+L` limpiar · `Ctrl+A`/`Ctrl+E` inicio/fin de línea ·
`sudo !!` repetir el último comando con sudo.

**Herramientas de texto**: `grep`, `sed`, `awk`, `sort`, `uniq`, `cut`, `tr`,
`xargs`, `jq` (JSON).

**Editores de terminal**: `nano` (fácil) y `vim` (potente; para salir sin
guardar, `:q!`).

## 4. Usuarios y permisos

- **root**: superusuario. **sudo**: ejecutar como root (`sudo apt update`).
- Cada archivo tiene **dueño**, **grupo** y permisos para **otros**.

```
-rwxr-xr--  1 ana devs  4096 archivo.sh
│└┬┘└┬┘└┬┘
│ │  │  └─ otros: r-- (leer)
│ │  └──── grupo: r-x (leer y ejecutar)
│ └─────── dueño: rwx (leer, escribir y ejecutar)
└───────── tipo: - archivo, d directorio, l enlace
```

| Permiso | Letra | Número |
|---|---|---|
| Lectura | r | 4 |
| Escritura | w | 2 |
| Ejecución | x | 1 |

```bash
chmod 755 script.sh       # rwxr-xr-x
chmod +x script.sh
chown ana:devs archivo
useradd / usermod / passwd / groups / id
```

- Usuarios en `/etc/passwd`, contraseñas cifradas en `/etc/shadow`, sudo en `/etc/sudoers` (editar con `visudo`).
- Permisos especiales: **SUID**, **SGID** y **sticky bit** (ej.: `/tmp`).
- Control fino: **ACL** (Access Control Lists) con `setfacl`/`getfacl`.
- Control obligatorio: **SELinux** (Security-Enhanced Linux, familia Red Hat) y **AppArmor** (familia Debian/Ubuntu, SUSE).

## 5. Gestión de paquetes

| Familia | Gestor | Instalar | Actualizar todo |
|---|---|---|---|
| Debian/Ubuntu | `apt` | `sudo apt install x` | `sudo apt update && sudo apt upgrade` |
| Fedora/RHEL | `dnf` | `sudo dnf install x` | `sudo dnf upgrade` |
| Arch | `pacman` | `sudo pacman -S x` | `sudo pacman -Syu` |
| openSUSE/SLES | `zypper` | `sudo zypper in x` | `sudo zypper up` |
| Alpine | `apk` | `apk add x` | `apk upgrade` |

**Formatos universales**: Flatpak, Snap, AppImage. Los lenguajes tienen sus
propios gestores (pip, npm, cargo).

## 6. Procesos y servicios

```bash
ps aux; top; htop; btop
kill PID; kill -9 PID; killall nombre
comando &; jobs; fg; bg; nohup comando &
```

**Señales**: `SIGTERM` (15) pide terminar amablemente · `SIGKILL` (9) mata
sin opción · `SIGHUP` (1) suele recargar configuración.

### systemd (sistema de inicio de la mayoría de distros)

```bash
systemctl status nginx
sudo systemctl start|stop|restart|reload nginx
sudo systemctl enable --now nginx
journalctl -u nginx -f
journalctl -b
systemctl list-units --failed
```

- **Units**: `.service`, `.timer`, `.socket`, `.mount`, `.target`.
- Unit propia en `/etc/systemd/system/miapp.service` con `User=`, `Restart=on-failure`, `LimitNOFILE=`, `MemoryMax=`.
- Tareas programadas: **cron** (`crontab -e`) o **systemd timers**.

```
# min hora día mes día_semana comando
0 3 * * * /home/ana/backup.sh
```

## 7. Discos y almacenamiento

```bash
lsblk; df -h; du -sh carpeta; ncdu
mount /dev/sdb1 /mnt; umount /mnt
fdisk / parted       # particionar (GPT)
mkfs.xfs /dev/sdb1   # formatear
blkid                # UUIDs para fstab
```

- `/etc/fstab`: qué se monta al arrancar (usar UUID, no `/dev/sdX`).
- **LVM** (Logical Volume Manager): PV → VG → LV; ampliar en caliente (`lvextend -r`) y snapshots.
- **RAID** (Redundant Array of Independent Disks) por software con `mdadm`. **RAID no es backup.**
- **NFS** (Network File System) e **iSCSI** (Internet Small Computer Systems Interface) para almacenamiento en red.
- Swap: memoria virtual en disco. Nombres: `/dev/sda` (SATA/USB), `/dev/nvme0n1` (NVMe).

## 8. Redes

```bash
ip a; ip r; ip link
ping host; traceroute host; mtr host
ss -tulpn                 # puertos abiertos
curl -v URL; wget URL
dig dominio; nslookup dominio
tcpdump -i eth0 port 443
nmcli                     # NetworkManager
```

**SSH (Secure Shell)**:

```bash
ssh usuario@servidor
ssh -J bastion usuario@interno       # ProxyJump
ssh -L 5432:db:5432 bastion          # túnel local
ssh-keygen -t ed25519
ssh-copy-id usuario@servidor
scp archivo usuario@srv:/ruta
rsync -avz origen/ srv:/destino
```

- **Firewall**: `nftables` (moderno, bajo nivel), `iptables` (clásico), `ufw` (Ubuntu), `firewalld` (RHEL/Fedora).
- **Archivos clave**: `/etc/hosts`, `/etc/resolv.conf`, `/etc/ssh/sshd_config`, `/etc/nsswitch.conf`.
- **Kernel de red**: `net.ipv4.ip_forward`, bridges, VLANs, bonding, namespaces de red (`ip netns`).

## 9. Entorno gráfico (escritorio)

Capas: servidor gráfico (**X11** o **Wayland**) → gestor de pantalla (GDM,
SDDM, LightDM) → entorno de escritorio (GNOME, KDE Plasma, XFCE, Cinnamon,
gestores *tiling* como Hyprland, i3, Sway). En servidores normalmente no se
instala entorno gráfico.

## 10. Arranque del sistema

**BIOS/UEFI** (Unified Extensible Firmware Interface) → **gestor de
arranque** (GRUB, systemd-boot) → **kernel + initramfs** → **systemd** (PID 1)
→ servicios → login. Los runlevels antiguos equivalen a los *targets* de
systemd (`multi-user.target`, `graphical.target`, `rescue.target`).

## 11. Kernel: módulos, sysctl, cgroups y namespaces

```bash
uname -r; lsmod; modprobe br_netfilter
sysctl -a | grep swappiness
sysctl -w vm.swappiness=10                  # temporal
echo "vm.swappiness=10" > /etc/sysctl.d/90-db.conf && sysctl --system   # persistente
```

- **cgroups v2** (control groups): limitan CPU, memoria e I/O de un grupo de procesos. systemd los usa para cada servicio (`systemctl set-property miapp MemoryMax=512M`).
- **Namespaces**: aíslan lo que ve un proceso (pid, net, mnt, uts, ipc, user). Con `unshare` y `ip netns` puedes armar "un contenedor a mano".
- **cgroups + namespaces + overlayfs = contenedor**. Esto es lo que hacen Docker, Podman, containerd y, por debajo, Kubernetes.

## 12. Scripting en Bash

```bash
#!/usr/bin/env bash
set -euo pipefail          # salir ante error, variable no definida o fallo en tubería

ORIGEN="$HOME/documentos"
DESTINO="/backups/docs_$(date +%F).tar.gz"

trap 'echo "Falló en la línea $LINENO" >&2' ERR

if [[ ! -d "$ORIGEN" ]]; then
    echo "Error: no existe $ORIGEN" >&2
    exit 1
fi

tar -czf "$DESTINO" "$ORIGEN" && echo "Backup listo: $DESTINO"
```

Conceptos: variables (siempre entre comillas, `"$VAR"`), argumentos (`$1`,
`$@`), código de salida (`$?`, 0 = éxito), `&&` y `||`, funciones, arrays,
`getopts`, `export`, `$PATH`, `~/.bashrc` (alias). Valida tus scripts con
**ShellCheck**.

## 13. Seguridad básica (hardening)

- Actualizar con frecuencia; no usar root en el día a día.
- SSH: solo claves, `PermitRootLogin no`, `PasswordAuthentication no`, fail2ban.
- Firewall activo con política *default deny*.
- Software solo de fuentes confiables; nunca `curl … | bash` de sitios desconocidos.
- Auditoría: `auditd`, escaneo con **Lynis**, benchmarks **CIS** (Center for Internet Security).
- ⚠️ Comandos peligrosos: `rm -rf /`, `dd` y `mkfs` sobre el disco equivocado, `chmod -R 777`.
- Backups probados: rsync, Borg, restic, Timeshift.

## 14. Diagnóstico y solución de problemas

| Problema | Herramienta |
|---|---|
| ¿Qué falló? | `journalctl -xe`, `dmesg`, `/var/log/` |
| CPU o RAM alta | `htop`, `free -h`, `vmstat 1` |
| Disco lleno | `df -h`, `df -i` (inodos), `ncdu`, `lsof +L1` (borrados pero abiertos) |
| Disco lento | `iostat -x 1`, `iotop` |
| Red | `ping`, `ss`, `tcpdump`, `mtr` |
| Programa colgado | `strace -p PID`, `lsof -p PID` |
| Rendimiento fino | `perf top`, `sar` |
| Hardware | `lscpu`, `lspci`, `lsusb`, `sensors`, `inxi -F` |

**Método**: leer el error completo → logs → reproducir → buscar el error
textual → Arch Wiki / documentación oficial.

## 15. Linux en el mundo profesional

- Servidores web y nube (la gran mayoría corre Linux), el 100 % del TOP500 de supercomputadoras.
- Contenedores (Docker, Podman) y orquestación (Kubernetes) se apoyan en funciones del kernel.
- Automatización e IaC (Infrastructure as Code): Ansible, Terraform.
- Embebidos e IoT (Internet of Things), Android, WSL (Windows Subsystem for Linux) para desarrollo.
