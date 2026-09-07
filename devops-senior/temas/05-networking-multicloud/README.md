# Networking: VNet/Private Endpoints, VPC de AWS, VPC de GCP

Brecha declarada en Azure — pero tenés que confirmar tu nivel real en AWS/GCP
también (¿trabajaste VPC peering, Private Link/PrivateLink, o fue más a nivel
de aplicación?). Es la base de cómo se conecta todo de forma segura.

## Objetivos

- Diseñar una red segmentada correctamente (subnets públicas/privadas) en
  cualquiera de las tres nubes.
- Explicar el patrón de **acceso privado a servicios PaaS/gestionados** en
  cada nube (Private Endpoint / PrivateLink+VPC Endpoint / Private Service Connect).
- DNS privado: por qué sin la zona DNS correcta, el endpoint privado "no sirve de nada".
- Reglas de firewall a nivel de red (NSG / Security Groups+NACLs / Firewall Rules de GCP).

## Equivalencias multi-cloud

| Concepto | Azure | AWS | GCP |
|---|---|---|---|
| Red virtual | VNet | VPC | VPC (global, no regional — diferencia clave) |
| Subred | Subnet | Subnet (asociada a una AZ) | Subnet (regional) |
| Acceso privado a un servicio PaaS | **Private Endpoint** + Private DNS Zone | **VPC Endpoint** (Interface o Gateway) / **PrivateLink** | **Private Service Connect** |
| Firewall a nivel instancia/subred | NSG (Network Security Group) | Security Group (stateful, a nivel instancia) + NACL (stateless, a nivel subnet) | Firewall Rules (a nivel VPC, con tags/service accounts) |
| Conexión entre redes | VNet Peering | VPC Peering / Transit Gateway | VPC Peering / Network Connectivity Center |
| DNS privado | Private DNS Zone + VNet Link | Route 53 Private Hosted Zone | Cloud DNS Private Zone |
| Enrutamiento custom | User-Defined Routes (UDR) | Route Tables | Custom Routes |

## Subtemas

1. Segmentación: por qué separar subnets de apps, endpoints privados e infraestructura
2. El patrón "sin DNS privado, el endpoint privado no sirve de nada" — aplica igual en las 3 nubes
3. AWS: diferencia entre Security Groups (stateful) y NACLs (stateless) — no tiene equivalente 1:1 en Azure/GCP
4. GCP: la VPC es global (las subnets son regionales) — a diferencia de Azure/AWS donde la red es regional
5. Troubleshooting de conectividad: Network Watcher (Azure) / VPC Reachability Analyzer (AWS) / Connectivity Tests (GCP)

## Recursos

- Azure Virtual Network: https://learn.microsoft.com/azure/virtual-network/
- Azure Private Link: https://learn.microsoft.com/azure/private-link/private-link-overview
- AWS VPC: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- AWS PrivateLink: https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html
- GCP VPC: https://cloud.google.com/vpc/docs/overview
- GCP Private Service Connect: https://cloud.google.com/vpc/docs/private-service-connect

## Lab sugerido

Elegí un servicio gestionado (base de datos) en cada nube y conectalo de
forma privada desde una VPC/VNet propia: Private Endpoint en Azure, VPC
Endpoint (Interface) en AWS, Private Service Connect en GCP. Verificá en cada
caso que el nombre resuelve a una IP privada.

## Autoevaluación

Pedime: *"Dame un examen de networking multi-cloud nivel senior"*.
