# Networking de Kubernetes y service mesh (Istio)

Cómo circula el tráfico dentro y hacia el clúster, una vez que ya tenés
claro el CNI (`01-arquitectura-y-cluster.md`).

## Objetivos

- Cómo funciona un Service (ClusterIP/NodePort/LoadBalancer) a nivel de iptables/IPVS.
- Network Policies: quién puede hablarle a quién dentro del clúster.
- Ingress vs. Gateway API: cómo entra el tráfico desde afuera.
- Service mesh (Istio): qué agrega por encima de lo anterior.

## Tipos de Service

| Tipo | Qué hace |
|---|---|
| **ClusterIP** (default) | IP virtual solo alcanzable desde dentro del clúster |
| **NodePort** | Abre un puerto fijo en cada nodo, redirige a ClusterIP |
| **LoadBalancer** | El cloud-controller-manager pide un Load Balancer real a la nube, que apunta a NodePort |

`kube-proxy` en cada nodo traduce la IP virtual del Service a las IPs reales
de los pods vía reglas de **iptables** (más simple, más lento a gran escala)
o **IPVS** (pensado para muchos Services, balanceo más eficiente).

## Network Policies

- Por default, en Kubernetes **todos los pods pueden hablarse entre sí**
  (no hay aislamiento de red salvo que lo definas).
- Una **NetworkPolicy** es un firewall a nivel de pod/namespace (selecciona
  pods por label, define ingress/egress permitido) — requiere que el CNI la
  soporte (Calico y Cilium sí; el CNI más básico no).

## Ingress vs. Gateway API

- **Ingress**: objeto más viejo y limitado para enrutar HTTP(S) desde afuera
  hacia Services internos (necesita un Ingress Controller: NGINX, AGIC, ALB
  Controller, GKE Ingress).
- **Gateway API**: reemplazo moderno, más expresivo (soporta más protocolos,
  separa roles entre quien administra la infra de red y quien define rutas
  de su app) — hacia donde se está moviendo el ecosistema.

## Service mesh: Istio

Una capa extra sobre todo lo anterior: un **service mesh** intercepta el
tráfico entre pods (vía un *sidecar proxy*, normalmente Envoy) para dar, sin
tocar el código de la app:

- **mTLS automático** entre servicios (tráfico interno cifrado y autenticado
  por default).
- **Traffic management** fino: canary releases, traffic splitting por
  porcentaje, retries/timeouts/circuit breaking a nivel de red (no en el
  código de la app).
- **Observabilidad de red gratis**: métricas de latencia/error rate por
  servicio sin instrumentar cada app (complementa OpenTelemetry, tema 07).
- **Istio** es la implementación más conocida (alternativas: Linkerd, Cilium
  en modo mesh). Se instala sobre cualquier Kubernetes (AKS/EKS/GKE).

No lo confundas con **Ingress/Gateway API** (tráfico que entra al clúster
desde afuera): Istio gestiona sobre todo el tráfico **este-oeste** (entre
servicios dentro del clúster), aunque también puede reemplazar el Ingress
(Istio Gateway).

## Recursos

- Services: https://kubernetes.io/docs/concepts/services-networking/service/
- Network Policies: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Gateway API: https://gateway-api.sigs.k8s.io/
- Istio docs: https://istio.io/latest/docs/

## Autoevaluación

Pedime: *"Dame un examen de networking de Kubernetes (Services/NetworkPolicy/Ingress)"*
o *"Dame un examen de Istio/service mesh nivel senior"*.
