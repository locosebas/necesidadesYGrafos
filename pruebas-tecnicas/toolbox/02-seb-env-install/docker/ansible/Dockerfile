# Ansible empaquetado en un contenedor: el único requisito local es Docker.
# Python 3.12: la versión más nueva que soporta ansible-core 2.16
FROM python:3.12-slim

# Copia solo el binario del cliente de Docker desde la imagen oficial:
# Ansible lo usa para entrar al contenedor destino con "docker exec".
COPY --from=docker:27-cli /usr/local/bin/docker /usr/local/bin/docker

# ansible 9.x (ansible-core 2.16): última versión con soporte para el
# Python 2.7 de CentOS 7 en el destino. --no-cache-dir = imagen más liviana.
# --root-user-action=ignore: en un contenedor es normal instalar como root (evita el aviso).
RUN pip install --no-cache-dir --root-user-action=ignore "ansible>=9,<10"

# Carpeta donde se monta el proyecto (ver volumes en docker-compose.yml)
WORKDIR /proyecto
# El contenedor se comporta como el comando ansible-playbook
ENTRYPOINT ["ansible-playbook"]
# Argumento por defecto: el playbook principal (se puede sobreescribir)
CMD ["site.yml"]
