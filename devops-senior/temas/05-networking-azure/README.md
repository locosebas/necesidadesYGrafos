# Azure Networking: VNet, Private Endpoints, Private DNS, NSG

Tu mayor brecha declarada. Es la base de cómo se conecta todo lo demás
(Container Apps, Key Vault, Cosmos DB) de forma segura, sin exponer nada a
internet público.

## Objetivos

- Diseñar una VNet con subnets segmentadas correctamente (delegated subnets
  para Container Apps, subnet para Private Endpoints, etc.)
- Explicar la diferencia entre **Private Endpoint**, **Private Link** y
  **Service Endpoint** (y por qué Private Endpoint es preferido para PaaS).
- Configurar Private DNS Zones y su vínculo (link) con la VNet para que el
  nombre del recurso PaaS resuelva a la IP privada.
- NSG: reglas de entrada/salida, prioridades, service tags (`Internet`,
  `VirtualNetwork`, `AzureCloud`).
- Troubleshooting básico de conectividad (NSG flow logs, `az network watcher`).

## Subtemas

1. VNet, subnets, address space, peering
2. Private Endpoint: qué es una NIC privada dentro de tu VNet apuntando a un recurso PaaS
3. Private DNS Zone: `privatelink.<servicio>.azure.com`, autorregistro vs manual
4. NSG vs Application Security Groups (ASG)
5. Route Tables (UDR) y su interacción con NSG
6. Container Apps Environment en modo VNet-integrated (internal vs external)
7. DNS resolution: por qué sin la Private DNS Zone bien linkeada el Private Endpoint "no sirve de nada" (sigue resolviendo a IP pública)

## Recursos

- Virtual Network docs: https://learn.microsoft.com/azure/virtual-network/
- Private Link overview: https://learn.microsoft.com/azure/private-link/private-link-overview
- Private DNS overview: https://learn.microsoft.com/azure/dns/private-dns-overview
- NSG overview: https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview

## Lab sugerido

Creá una VNet con 3 subnets (apps, private-endpoints, infra). Desplegá un
Key Vault con acceso público deshabilitado, un Private Endpoint hacia él desde
la subnet correspondiente, y una Private DNS Zone linkeada. Verificá que
resolver el nombre del Key Vault desde dentro de la VNet da la IP privada.

## Autoevaluación

Pedime: *"Dame un examen de Azure Networking nivel senior"*.
