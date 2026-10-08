# Linux, distribuciones e infraestructura (de Linux puro a Kubernetes)

Tema agregado el 2026-10-08. Llena un hueco del roadmap: ningún tema cubría
**Linux como sistema operativo** (administración, redes, almacenamiento,
afinado del kernel) ni las **distribuciones** (generales, especializadas, para
bases de datos, contenedores, nodos de Kubernetes y nube).

Todo el tema gira alrededor de un mismo proyecto, **NubeShop** (una tienda
en línea con frontend, API, workers, PostgreSQL, Redis, cola de mensajes y
almacenamiento de archivos), que crece fase por fase. Así los retos no son
piezas sueltas sino **arquitecturas completas** que se van acumulando:

```
Fase 1: Linux puro     →  NubeShop v1 en VMs, montado a mano
Fase 2: Automatización →  NubeShop v1 reconstruido con Ansible en minutos
Fase 3: Contenedores   →  NubeShop v2 en Docker/Podman
Fase 4: Kubernetes     →  NubeShop v3 en un clúster propio con alta disponibilidad
Fase 5: Cloud + IaC    →  NubeShop v4 en la nube con GitOps y CI/CD
Fase 6: SRE / Final    →  NubeShop v5 multi-región con DR, SLOs y caos
```

Complementa (no reemplaza) a los temas existentes: `02-contenedores-serverless`,
`10-kubernetes-avanzado`, `01-iac-multicloud`, `03-cicd-multicloud` y
`07-observabilidad-multicloud`. Aquí el foco es **lo que hay debajo**: el
Linux de los nodos y la instalación del clúster a mano.

## Archivos (en orden de estudio)

| # | Archivo | Qué tiene |
|---|---|---|
| 1 | [`01-fundamentos-linux.md`](01-fundamentos-linux.md) | Guía esencial de Linux: kernel, FHS, terminal, permisos, paquetes, procesos, systemd, discos, redes, arranque, Bash, seguridad y diagnóstico |
| 2 | [`02-distribuciones.md`](02-distribuciones.md) | Distros por familia, distros de servidor (dónde corren las bases de datos), distros especializadas por servicio, imágenes base de contenedores, distros para nodos de Kubernetes y distros de nube |
| 3 | [`03-tuning-por-servicio.md`](03-tuning-por-servicio.md) | Cómo se afina el **mismo Linux** según el servicio: PostgreSQL, MySQL, Oracle, Redis, OpenSearch, Kafka, Nginx |
| 4 | [`04-ruta-fases-y-retos.md`](04-ruta-fases-y-retos.md) | Ruta por fases (1, 2, 3, 5 y 6) con retos de arquitectura NubeShop y preguntas de diseño |
| 5 | [`05-kubernetes-instalacion-y-kit.md`](05-kubernetes-instalacion-y-kit.md) | Fase 4 completa: instalar Kubernetes (kind, k3s, **kubeadm HA** paso a paso), kit de herramientas de producción con Helm, retos y preguntas |
| 6 | [`examen.md`](examen.md) | Banco de preguntas por bloques (conceptos y diagnóstico) para responder **de a una**, con columna de nota |

## Objetivos

- Administrar servidores Linux como profesional: usuarios, permisos, systemd,
  almacenamiento (LVM, RAID, NFS), redes (nftables, DNS, DHCP, VPN) y seguridad.
- Entender que un contenedor es **un proceso Linux con namespaces + cgroups +
  overlayfs**, y que un nodo de Kubernetes es **un Linux afinado**.
- Elegir la **distribución correcta** para cada servicio y justificarla
  (soporte, certificación del fabricante, ciclo de vida, superficie de ataque).
- Afinar el kernel según la carga (THP, HugePages, swappiness, overcommit,
  `max_map_count`, límites de archivos).
- Instalar un clúster de Kubernetes con **kubeadm** en alta disponibilidad y
  completarlo con el kit de producción (CNI, LoadBalancer, Gateway API,
  cert-manager, almacenamiento, observabilidad, GitOps, políticas, backups).
- Diseñar y defender arquitecturas completas (alta disponibilidad, DR,
  seguridad en profundidad), no solo piezas sueltas.

## Tiempos orientativos (unas 10 horas por semana)

| Fase | Duración |
|---|---|
| 1. Linux puro | 3–4 meses |
| 2. Automatización | 1–1,5 meses |
| 3. Contenedores | 1–1,5 meses |
| 4. Kubernetes | 3–4 meses |
| 5. Cloud + IaC + CI/CD | 2–3 meses |
| 6. SRE + proyecto final | 2 meses |

Si ya tienes base fuerte en Kubernetes (ver `10-kubernetes-avanzado`), la
Fase 4 se acorta mucho: concéntrate en la instalación con kubeadm y el kit.

## Certificaciones que encajan

LFCS (Linux Foundation Certified System Administrator) o RHCSA (Red Hat
Certified System Administrator) después de la Fase 1 · RHCE (Red Hat
Certified Engineer, Ansible) en la Fase 2 · CKA → CKAD → CKS en la Fase 4 ·
Terraform Associate en la Fase 5.

## Recursos

- *The Linux Command Line* (William Shotts, gratis): https://linuxcommand.org/tlcl.php
- Arch Wiki (sirve aunque no uses Arch): https://wiki.archlinux.org/
- OverTheWire Bandit (aprender jugando): https://overthewire.org/wargames/bandit/
- Linux Journey: https://linuxjourney.com/
- kubeadm: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/
- endoflife.date (fechas de fin de soporte de distros y motores): https://endoflife.date/

> ⚠️ Las versiones (Kubernetes, charts de Helm, recomendaciones de afinado)
> cambian rápido: confírmalas en la documentación oficial antes de instalar.

## Autoevaluación

- Pídeme: *"Dame el examen de Linux, bloque A"* (preguntas de a una, en `examen.md`).
- Pídeme: *"Hagamos el Reto 1.B de NubeShop"* (diseño guiado, pregunta por pregunta).
- Pídeme: *"Instalemos kubeadm HA paso a paso"* (sigue `05-kubernetes-instalacion-y-kit.md`).
