# Fórmula 02 — Red interna de una empresa de cero a que funcione

**Resumen en una línea:** *requisitos → físico/topología → plan de IPs →
VLANs → routing → servicios core (DHCP/DNS/NTP/directorio) → seguridad
(firewall, NAC, Wi-Fi) → salida a internet y VPN → conexión a la nube →
monitoreo y documentación → pruebas.*

---

## Paso 0 — Requisitos

- ¿Cuántos usuarios y dispositivos hoy y en 3 años? (diseñá para ×2).
- ¿Cuántas sedes? ¿Trabajo remoto?
- ¿Qué servicios: servidores on-prem, nube, VoIP, cámaras, impresoras, IoT, invitados?
- ¿Disponibilidad requerida? (¿se cae internet y se para el negocio?).
- ¿Compliance? (PCI si hay pagos → segmentar la zona de tarjetas).
- Presupuesto y quién la opera.

## Paso 1 — Capa física y topología

- **Cableado estructurado** Cat6/6A a los puestos, **fibra** entre pisos/racks.
- Rack con **UPS**, patch panels, etiquetado.
- **Modelo jerárquico de 3 capas:**
  - **Core**: switching L3 de alta velocidad, redundante.
  - **Distribución**: routing entre VLANs, políticas.
  - **Acceso**: switches donde se conectan PCs, APs (con **PoE** para APs, teléfonos, cámaras).
  - Empresa chica/mediana → **collapsed core** (core + distribución en un par de switches L3).
- **Redundancia**: dos switches core (stack / MLAG / vPC), uplinks dobles con
  **LACP**, **STP (RSTP/MSTP)** para evitar loops, dos ISP.

## Paso 2 — Plan de direccionamiento IP (IPAM)

- Usar rangos privados **RFC 1918**: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- **Un bloque por sede** y **uno reservado para la nube**, sin solaparse
  (si después conectás VPN a una VPC que usa el mismo rango, no se puede rutear).
- Ejemplo:

| Bloque | Uso |
|---|---|
| `10.10.0.0/16` | Sede central |
| `10.20.0.0/16` | Sucursal 1 |
| `10.100.0.0/14` | Nube (VPC/VNet por entorno) |
| `172.16.0.0/16` | VPN de usuarios remotos |

Subredes dentro de la sede central (una por VLAN):

| VLAN | Nombre | Subred | Hosts útiles |
|---|---|---|---|
| 10 | Gestión (switches, APs, firewall) | `10.10.10.0/24` | 254 |
| 20 | Servidores | `10.10.20.0/24` | 254 |
| 30 | Usuarios cableados | `10.10.32.0/22` | 1022 |
| 40 | VoIP | `10.10.40.0/24` | 254 |
| 50 | Wi-Fi corporativo | `10.10.48.0/22` | 1022 |
| 60 | Invitados | `10.10.60.0/24` | 254 |
| 70 | IoT / cámaras / impresoras | `10.10.70.0/24` | 254 |
| 99 | DMZ (servicios expuestos) | `10.10.99.0/24` | 254 |

Cálculo rápido: hosts útiles = 2^(32−prefijo) − 2 → /24 = 254, /23 = 510,
/22 = 1022, /26 = 62, /30 = 2 (enlaces punto a punto). En la nube restá
más: AWS reserva 5 IPs por subnet, Azure también 5.

## Paso 3 — Segmentación con VLANs

- Una VLAN por **función/nivel de confianza** (tabla de arriba).
- Puertos de acceso: `access` en su VLAN; entre switches: **trunks 802.1Q**
  solo con las VLANs necesarias.
- **No usar la VLAN 1** para nada y cambiar la *native VLAN* a una sin uso
  (evita VLAN hopping).
- Teléfono + PC en el mismo puerto → *voice VLAN*.

## Paso 4 — Routing

- **Inter-VLAN routing** en el switch L3 (SVI por VLAN) o en el firewall
  si querés inspeccionar todo el tráfico entre zonas.
- **Ruta por defecto** hacia el firewall perimetral.
- Varias sedes → **OSPF** (interno) sobre VPN/SD-WAN; **BGP** con ISPs o con la nube
  (Direct Connect / ExpressRoute / Interconnect lo usan).
- Gateway redundante: **VRRP/HSRP**.

Ejemplo estilo Cisco:

```
vlan 30
 name USUARIOS
!
interface GigabitEthernet1/0/5
 switchport mode access
 switchport access vlan 30
 switchport voice vlan 40
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface TenGigabitEthernet1/1/1
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,30,40,50,60,70
!
interface Vlan30
 ip address 10.10.32.1 255.255.252.0
 ip helper-address 10.10.20.10      ! relay DHCP al servidor en VLAN 20
!
ip route 0.0.0.0 0.0.0.0 10.10.10.254  ! default al firewall
```

## Paso 5 — Servicios core de red

- **DHCP**: un scope por VLAN, reservas para impresoras/APs, **DHCP relay**
  (`ip helper-address`) porque el broadcast no cruza VLANs.
  Servidores y equipos de red con **IP estática**.
- **DNS interno**: zona `empresa.local`/`corp.empresa.com`, **split-horizon**
  (distinta respuesta dentro y fuera), forwarders a DNS públicos o a la nube.
- **NTP**: todos sincronizados (Kerberos/AD y los logs dependen de la hora).
- **Directorio / identidad**: Active Directory y/o **Entra ID**, SSO.
  **RADIUS** (NPS, FreeRADIUS, ISE, ClearPass) para autenticar red y VPN.

## Paso 6 — Seguridad

- **Firewall perimetral NGFW** (Fortinet, Palo Alto, pfSense/OPNsense…):
  **deny by default**, NAT de salida, IPS, filtrado web.
- **Reglas entre zonas** (matriz): invitados → solo internet; IoT → solo su
  servidor; usuarios → servidores solo puertos necesarios; gestión solo
  desde la VLAN de administración.
- **DMZ** para lo que se publica a internet (nunca publicar directo la LAN).
- **802.1X / NAC**: el puerto o Wi-Fi solo da acceso tras autenticar
  (certificado o usuario); dispositivo desconocido → VLAN de cuarentena.
- Protecciones L2: **port security**, **DHCP snooping**, **Dynamic ARP
  Inspection**, **BPDU guard**.
- **Wi-Fi**: SSID corporativo **WPA3-Enterprise (802.1X)**, SSID de
  invitados aislado con portal cautivo y límite de ancho de banda.
  Site survey para ubicar APs y canales (5/6 GHz).
- Gestión de equipos por **SSH** (no Telnet), AAA con TACACS+/RADIUS, cuentas
  nominales, configs respaldadas.
- Enfoque moderno: **Zero Trust / ZTNA** — no confiar por estar "adentro".

## Paso 7 — Internet, sedes y usuarios remotos

- **Dos ISP** con failover (o balanceo) en el firewall.
- Entre sedes: **VPN IPsec site-to-site** o **SD-WAN**.
- Usuarios remotos: VPN cliente (IPsec/SSL/WireGuard) o **ZTNA**, con MFA.

## Paso 8 — Conexión híbrida con la nube

- Topología **hub-and-spoke**: una VNet/VPC *hub* (firewall, VPN gateway,
  DNS resolver) y *spokes* por entorno/app.
- Conectividad: **VPN site-to-site** (rápido, barato) o dedicada:
  **ExpressRoute** (Azure) / **Direct Connect** (AWS) / **Cloud Interconnect** (GCP).
- **DNS híbrido**: Azure DNS Private Resolver / Route 53 Resolver endpoints /
  Cloud DNS forwarding, para que on-prem resuelva los private endpoints y viceversa.
- CIDRs de nube **reservados desde el paso 2**.

## Paso 9 — Operación

- **Monitoreo**: SNMP / telemetría + NetFlow/sFlow (Zabbix, LibreNMS, PRTG, Datadog).
- **Syslog** centralizado → SIEM.
- **Backups de configuración** automáticos (Oxidized/RANCID) y en Git.
- **Documentación**: diagrama L2/L3, IPAM (**NetBox**), matriz de reglas.
- Control de cambios y ventanas de mantenimiento; firmware actualizado.
- Idealmente **automatización** (Ansible) para configurar switches.

## Paso 10 — Pruebas "funciona"

1. PC en VLAN 30 obtiene IP por DHCP (`ipconfig /all` / `ip a`) con gateway y DNS correctos.
2. Resuelve nombres internos y externos (`nslookup intranet.corp.empresa.com`).
3. Llega a los servidores permitidos y **no** llega a los prohibidos (probar la matriz del firewall).
4. Invitado solo sale a internet.
5. Desconecto un ISP / un uplink / un switch core → sigue funcionando (failover).
6. Desde on-prem llego a un recurso privado en la nube por nombre.
7. Alertas del monitoreo llegan cuando bajo una interfaz.

## Troubleshooting de red: de abajo hacia arriba (modelo OSI)

| Capa | Pregunta | Herramienta |
|---|---|---|
| 1 Física | ¿Hay link? ¿cable/puerto/PoE? | LEDs, `show interfaces` |
| 2 Enlace | ¿VLAN correcta? ¿MAC aprendida? ¿STP bloqueando? | `show vlan`, `show mac address-table` |
| 3 Red | ¿IP/máscara/gateway? ¿ruta? | `ping`, `traceroute`, `ip route` |
| 4 Transporte | ¿Puerto abierto? ¿firewall? | `nc -vz host 443`, `telnet`, logs del firewall |
| 7 Aplicación | ¿DNS? ¿certificado? ¿la app responde? | `nslookup`/`dig`, `curl -v` |

> "Si no hay IP" → DHCP (¿relay? ¿scope lleno?). "Si hay IP y no navega"
> → gateway/DNS. "Si resuelve y no conecta" → firewall/ruta. "Si conecta
> pero falla" → aplicación/TLS.
