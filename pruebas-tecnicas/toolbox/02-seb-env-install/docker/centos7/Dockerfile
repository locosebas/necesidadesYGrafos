# "Servidor" CentOS 7 de laboratorio para probar el playbook en localhost.
# Imagen base oficial de CentOS 7 (trae Python 2.7 y yum, lo que Ansible necesita)
FROM centos:7

# CentOS 7 está en fin de vida: se apuntan los repos a vault.centos.org
# para que yum funcione (el playbook hace lo mismo en un servidor real).
#   1er -e: comenta las líneas mirrorlist= (servicio de mirrors ya apagado)
#   2do -e: descomenta baseurl= y cambia mirror.centos.org por vault.centos.org
#   se aplica a todos los archivos CentOS-*.repo
RUN sed -i -e 's|^mirrorlist=|#mirrorlist=|' \
           -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://vault.centos.org|' \
           /etc/yum.repos.d/CentOS-*.repo

# La imagen mínima no trae sudo (un servidor real sí); Ansible lo usa por "become: true".
# También se actualiza systemd YA: si se actualizara después (como dependencia de
# MariaDB/PHP), yum pisaría el reemplazo de systemctl que se instala abajo.
# ulimit -n 1024: Docker reciente da un límite de archivos abiertos enorme y el rpm
# de CentOS 7 intenta cerrarlos uno por uno (se queda "colgado"); se baja el límite.
# yum clean all borra la caché de paquetes para que la imagen pese menos.
RUN ulimit -n 1024 && yum install -y sudo && yum update -y systemd && yum clean all

# systemd de CentOS 7 no arranca en hosts con cgroup v2 (Docker Desktop,
# WSL2, Ubuntu 22+). Se usa docker-systemctl-replacement como PID 1: entiende
# los mismos comandos "systemctl start/enable/restart" que usa el tutorial,
# así el playbook es idéntico al de un servidor real.
# Versión fija del reemplazo (builds reproducibles)
ARG SYSTEMCTL_VERSION=v1.5.9063
# Descarga el script y lo pone en lugar del systemctl original, con permiso de ejecución
RUN curl -fsSL -o /usr/bin/systemctl \
      https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/${SYSTEMCTL_VERSION}/files/docker/systemctl.py \
 && chmod 755 /usr/bin/systemctl

# Documenta que el contenedor sirve HTTP en el puerto 80
EXPOSE 80
# Proceso principal: el reemplazo de systemctl hace de "init" y arranca los servicios habilitados
CMD ["/usr/bin/systemctl"]
