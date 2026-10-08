# Examen de Linux: fundamentos, distribuciones y afinado

**Reglas**
- Una pregunta a la vez. Claude califica de 0 a 10, explica qué faltó y pasa a la siguiente.
- En los repasos se describe el mecanismo y se pide el **nombre** de la herramienta (no al revés).
- "paso" = 0 puntos, con la explicación completa.
- Al final: promedio por bloque, promedio general y plan de repaso.

**Escala:** 9-10 experto · 7-8 sólido · 5-6 básico · <5 repasar

**Estado actual:** Pregunta 1 de 45

Las preguntas de diseño de arquitectura (retos NubeShop) están en
`04-ruta-fases-y-retos.md` y `05-kubernetes-instalacion-y-kit.md`.

---

## Bloque A: Distribuciones
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 1 | ¿Qué es una distribución y qué la diferencia del kernel? | | |
| 2 | Nombra las 3 grandes familias de distros, su gestor de paquetes y 2 distros de cada una | | |
| 3 | ¿En qué distro pondrías Oracle Database y por qué? ¿Y SAP HANA? | | |
| 4 | Un servidor solo hace de NAS con ZFS, SMB y NFS: ¿qué distro especializada usarías? | | |
| 5 | Router empresarial con BGP/OSPF y CLI estilo Juniper, basado en Debian: ¿cómo se llama? | | |
| 6 | Distro para nodos de Kubernetes sin SSH ni shell, gestionada solo por API: ¿cuál es? | | |
| 7 | pfSense y OPNsense: ¿son Linux? | | |

## Bloque B: Sistema de archivos y terminal
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 8 | ¿Qué hay en `/etc`, `/var`, `/proc` y `/dev`? | | |
| 9 | Diferencia entre `>`, `>>`, `2>` y `|` | | |
| 10 | Escribe una tubería que muestre las 10 IPs con más peticiones de un `access.log` | | |
| 11 | ¿Qué diferencia hay entre un enlace simbólico y uno duro? | | |
| 12 | ¿Qué hace `set -euo pipefail` en un script de Bash? | | |

## Bloque C: Usuarios y permisos
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 13 | ¿Qué significa `chmod 750` y quién puede hacer qué? | | |
| 14 | ¿Qué son SUID, SGID y sticky bit? Da un ejemplo real de cada uno | | |
| 15 | ¿Dónde se guardan usuarios y contraseñas? ¿Cómo editas sudoers de forma segura? | | |
| 16 | SELinux vs. AppArmor: ¿qué resuelven que los permisos clásicos no? | | |

## Bloque D: Procesos y systemd
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 17 | SIGTERM vs. SIGKILL vs. SIGHUP | | |
| 18 | Proceso zombi vs. huérfano | | |
| 19 | Escribe una unit de systemd para una app con usuario propio, reinicio automático y límite de memoria | | |
| 20 | cron vs. systemd timers: ventajas de cada uno | | |
| 21 | ¿Cómo ves los logs de un servicio desde el último arranque? | | |

## Bloque E: Almacenamiento
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 22 | Explica PV, VG y LV en LVM y cómo amplías un volumen en caliente | | |
| 23 | ¿Por qué RAID no es un backup? | | |
| 24 | `df` muestra espacio libre pero no puedes crear archivos: ¿qué pasa? | | |
| 25 | `df` dice 100 % pero `du` no encuentra los archivos grandes: ¿qué pasa y cómo lo confirmas? | | |
| 26 | Tras reiniciar, el servidor arranca en modo emergencia: ¿causa típica y arreglo? | | |

## Bloque F: Redes
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 27 | Responde al ping pero SSH no conecta: 8 causas, en orden | | |
| 28 | ¿Qué ocurre, a nivel de red y sistema, desde `curl https://nubeshop.lab` hasta ver el HTML? | | |
| 29 | ¿Cómo listas los puertos abiertos y qué proceso escucha en cada uno? | | |
| 30 | ¿Qué es un ProxyJump de SSH y para qué sirve un bastión? | | |
| 31 | ¿Qué hace `net.ipv4.ip_forward=1` y cuándo lo necesitas? | | |
| 32 | Crea un namespace de red con `ip netns` y conéctalo a un bridge: ¿qué acabas de construir? | | |

## Bloque G: Kernel y afinado por servicio
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 33 | ¿Qué son THP y por qué se desactivan en bases de datos? | | |
| 34 | ¿Qué valor de `vm.overcommit_memory` necesita Redis y por qué? | | |
| 35 | ¿Qué valor de `vm.overcommit_memory` se recomienda para PostgreSQL y por qué? | | |
| 36 | OpenSearch no arranca por `vm.max_map_count`: ¿cómo lo corriges de forma persistente? | | |
| 37 | Herramienta de RHEL para aplicar perfiles de afinado (ej. `throughput-performance`): ¿cómo se llama? | | |
| 38 | Paquete de Oracle Linux que deja el sistema listo para Oracle Database: ¿cómo se llama? | | |
| 39 | ¿Cómo limitas una app a 512 MB de RAM y 50 % de un núcleo sin contenedores? | | |
| 40 | ¿Qué tres funciones del kernel forman un contenedor? | | |

## Bloque H: Diagnóstico
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 41 | Carga de 40 en 4 núcleos con CPU al 10 %: ¿qué indica? | | |
| 42 | Un proceso desaparece sin dejar rastro en los logs de la app: ¿dónde buscas? | | |
| 43 | La web va lenta solo a ciertas horas: diseña la investigación paso a paso | | |
| 44 | Un proceso está colgado: ¿qué herramientas usas para ver qué hace y qué archivos tiene abiertos? | | |
| 45 | El OOM killer mató a PostgreSQL: ¿qué configuración del kernel y de systemd lo evita? | | |

---

## Resultados

| Bloque | Promedio | Observaciones |
|---|---|---|
| A | | |
| B | | |
| C | | |
| D | | |
| E | | |
| F | | |
| G | | |
| H | | |
| **General** | | |
