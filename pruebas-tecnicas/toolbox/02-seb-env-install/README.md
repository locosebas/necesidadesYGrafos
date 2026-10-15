# seb-env-install: un servidor LEMP en CentOS 7 con un solo comando

## El reto

El tutorial de DigitalOcean
[How To Install Linux, Nginx, MySQL, PHP (LEMP) stack On CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-centos-7)
explica cómo montar un servidor web con **Nginx + MariaDB + PHP**. Son unos 20 comandos, varias
ediciones de archivos a mano con `nano` y un script que hace preguntas por consola.

Hacerlo a mano una vez está bien. Hacerlo en 10 servidores, o repetirlo dentro de seis meses sin
equivocarse, no tanto. Por eso lo automaticé con **Ansible**: describo cómo tiene que quedar el
servidor y Ansible se encarga de llegar ahí, las veces que haga falta y siempre con el mismo resultado.

## El plan

Cada paso del tutorial se volvió un **rol** de Ansible, y el playbook `site.yml` los ejecuta en orden:

| Orden | Rol | Qué hace | Paso del tutorial |
|---|---|---|---|
| 1 | `base` | Deja lista la máquina: repositorios, EPEL y un usuario no-root (`sammy`) | Prerrequisitos |
| 2 | `nginx` | Instala Nginx, lo arranca y lo deja habilitado al iniciar | Paso 1 |
| 3 | `mariadb` | Instala MariaDB y la asegura (clave de root, sin usuarios anónimos ni base de prueba) | Paso 2 |
| 4 | `php` | Instala PHP 7.4 y configura PHP-FPM para trabajar con Nginx | Paso 3 |
| 5 | `app` | Conecta Nginx con PHP, publica `info.php` y **verifica que todo funcione** | Pasos 4 y 5 |

Los valores que pueden cambiar (contraseña, versión de PHP, nombre del servidor) están juntos en
`group_vars/all.yml`, así no hay que tocar los roles.

## ¿Y dónde lo pruebo?

El tutorial asume que tienes un servidor CentOS 7. Para no depender de uno, el proyecto trae uno de
mentira: un **contenedor Docker con CentOS 7** que hace de servidor en tu propia máquina. Ansible lo
configura igual que configuraría uno real.

```
  Tu máquina                                   Contenedor "servidor" CentOS 7
┌──────────────┐    docker exec    ┌──────────────────────────────────────────┐
│   Ansible    │ ────────────────► │  Nginx ──► PHP-FPM 7.4 ──► MariaDB       │
└──────────────┘                   └──────────────────────────────────────────┘
                                          │
                   http://localhost:8080 ◄┘
```

## Cómo correrlo

Solo necesitas **[Docker](https://docs.docker.com/get-docker/)**.

**1. Encender el servidor CentOS 7**

```bash
docker compose up -d --build
```

**2. Dejar que Ansible lo configure** (elige una opción)

- **Opción A: Ansible en un contenedor (recomendada, no instalas nada más)**

  ```bash
  docker compose run --rm ansible
  ```

- **Opción B: Ansible instalado en tu máquina** (requiere Python 3.10, 3.11 o 3.12)

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ansible-playbook site.yml
  ```

  Con [uv](https://docs.astral.sh/uv/) es una sola línea:
  `uvx --python 3.12 --from 'ansible>=9,<10' ansible-playbook site.yml`

Tarda unos 3 minutos. Si quieres una contraseña propia para MariaDB, antes de correrlo ejecuta
`export MARIADB_ROOT_PASSWORD='TuClave'` (si no, se usa `Cambiar-Esta-Clave-123`).

**3. Comprobar el resultado**

Abre **http://localhost:8080/info.php**. Debes ver la página de PHP 7.4 con `Server API: FPM/FastCGI`,
que es la señal de que Nginx le está pasando el PHP a PHP-FPM.

**4. Apagar todo**

```bash
docker compose down
```

## Qué pasa por dentro cuando lo corres

1. Ansible revisa que el servidor sea CentOS 7. Si no lo es, se detiene antes de tocar nada.
2. Arregla los repositorios (CentOS 7 ya no tiene soporte, más abajo explico por qué) e instala EPEL.
3. Instala Nginx, MariaDB y PHP 7.4, y deja los tres servicios corriendo y habilitados.
4. Reemplaza el script interactivo `mysql_secure_installation` por las mismas sentencias SQL, sin preguntas.
5. Edita la configuración de PHP-FPM para que use un socket que Nginx pueda leer.
6. Crea la configuración de Nginx que manda los archivos `.php` a PHP-FPM.
7. Al final pide `info.php` y **falla si PHP no responde**, así no hace falta revisarlo a mano.

Si lo corres una segunda vez, termina con `changed=0`: no hay nada que cambiar porque el servidor ya
está como debe estar. Eso es lo que se llama **idempotencia**.

## Obstáculos que encontré en el camino

- **CentOS 7 ya no tiene soporte (desde junio de 2024).** Sus repositorios originales desaparecieron y
  `yum` fallaba. Lo resolví apuntando a los repositorios de archivo (`vault.centos.org` y el archivo de
  EPEL). En un proyecto nuevo recomendaría Rocky Linux o AlmaLinux 9.
- **El Ansible más reciente no habla con CentOS 7.** CentOS 7 trae Python 2.7 y las versiones nuevas de
  Ansible ya no lo soportan, por eso la versión está fijada en Ansible 9.
- **CentOS 7 dentro de Docker moderno no arranca sus servicios.** Su `systemd` es demasiado viejo, así
  que el contenedor usa [un reemplazo de `systemctl`](https://github.com/gdraheim/docker-systemctl-replacement)
  que acepta los mismos comandos. Esto solo aplica al contenedor de prueba: el playbook es el mismo que
  se usaría en un servidor real.

## ¿Y en un servidor real?

Se copia el inventario de ejemplo, se pone la IP, el usuario y la llave SSH, y se corre el mismo playbook:

```bash
cp inventories/servidor.ini.example inventories/servidor.ini
ansible-playbook -i inventories/servidor.ini site.yml
```

En producción también conviene poner `php_info_page: false` en `group_vars/all.yml`: el playbook borra
`info.php`, que muestra información sensible del servidor (el tutorial recomienda lo mismo).

## Mapa de archivos

```
site.yml              ← punto de entrada: qué roles se ejecutan y en qué orden
group_vars/all.yml    ← los valores que se pueden ajustar
roles/                ← un rol por paso del tutorial (base, nginx, mariadb, php, app)
inventories/          ← a qué servidor se conecta: el contenedor o uno real
ansible.cfg           ← preferencias de Ansible para este proyecto
docker/               ← el servidor CentOS 7 de prueba y el contenedor con Ansible
docker-compose.yml    ← enciende todo lo anterior
```

Cada archivo está comentado línea por línea.
