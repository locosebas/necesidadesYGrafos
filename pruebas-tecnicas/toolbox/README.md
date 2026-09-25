# Prueba técnica - Toolbox

| # | Pregunta | Archivo |
|---|---|---|
| 1 | Script en Bash que cada 5 segundos hace un GET a httpbin.org e imprime el tiempo de respuesta y el `origin` | [01-httpbin-monitor.sh](01-httpbin-monitor.sh) |
| 2 | Automatizar en Ansible la instalación de LEMP en CentOS 7 | [02-seb-env-install/](02-seb-env-install/) (entregable: `02-seb-env-install.zip`) |
| 3 | Beneficios de usar Docker desde desarrollo hasta producción | [03-beneficios-docker.md](03-beneficios-docker.md) |

## 1. Monitor de httpbin

Requiere `curl` (usa `jq` si está instalado).

```bash
chmod +x 01-httpbin-monitor.sh
./01-httpbin-monitor.sh
```

La variable `REPETICIONES` al inicio del script limita las peticiones (`0` = infinito, se detiene con Ctrl+C).

## 2. LEMP con Ansible

Las instrucciones completas están en [02-seb-env-install/README.md](02-seb-env-install/README.md). Versión corta (solo requiere Docker):

```bash
cd 02-seb-env-install
docker compose up -d --build
docker compose run --rm ansible
```

Luego abrir http://localhost:8080/info.php
