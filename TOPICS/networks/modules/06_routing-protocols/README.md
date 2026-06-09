# Module 06: Routing Protocols

[← Previous](../05_application-layer/) | [Topic Home](../../README.md) | [Next →](../07_wireless-networking/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

This module covers how routers learn about network topology and populate their routing tables automatically. We start with static routes, then cover the distance-vector protocol (RIP), link-state routing (OSPF — the dominant enterprise interior routing protocol), and BGP — the path-vector protocol that exchanges routes between organizations and is literally "the protocol that runs the internet."

Understanding routing protocols is essential for network engineers and increasingly for DevOps/SRE practitioners working with cloud networking, BGP-based load balancing (e.g., with Kubernetes and MetalLB), and anycast CDN design.

---

## Prerequisites

- Module 03: IP Networking — routing tables, CIDR, longest-prefix match
- Module 04: Transport Layer — TCP and UDP (OSPF runs over IP directly; BGP uses TCP)

---

## Objectives

By the end of this module, you will be able to:

1. Configure and explain static routes and describe their limitations
2. Explain how RIP works (distance-vector, hop count metric, convergence issues)
3. Describe OSPF's link-state approach: LSA flooding, SPF algorithm, areas, DR/BDR election
4. Explain BGP's role in inter-domain routing: autonomous systems, path-vector, policy routing
5. Describe common BGP operations: peering, prefix advertisement, AS path, route filtering
6. Identify BGP security issues: route leaks, hijacking, and RPKI as a mitigation

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### Static Routing

Static routes are manually configured entries in the routing table. They are simple, predictable, and have no overhead — but they do not adapt to topology changes.

```bash
# Add a static route: traffic to 10.1.0.0/24 via gateway 192.168.1.254
ip route add 10.1.0.0/24 via 192.168.1.254

# Add a default route (gateway of last resort)
ip route add default via 192.168.1.1

# View routing table
ip route show
```

Static routes are appropriate for: stub networks (one path in/out), default routes, and small networks where simplicity beats automation.

### RIP — Routing Information Protocol

RIP is a distance-vector protocol (RFC 2453): routers share their entire routing table with neighbors, using hop count as the metric. Maximum hop count = 15 (16 = unreachable). RIP sends full routing table updates every 30 seconds.

Problems with RIP: slow convergence (count-to-infinity problem), maximum 15 hops, sends full tables (bandwidth waste), no authentication in RIPv1. RIP is obsolete in most modern networks but is useful for understanding routing concepts.

### OSPF — Open Shortest Path First

OSPF (RFC 2328) is a link-state protocol. Each router:
1. Discovers neighbors (Hello packets)
2. Floods Link State Advertisements (LSAs) describing its links to all routers in the area
3. Builds a complete map of the network topology (Link State Database)
4. Runs Dijkstra's SPF (Shortest Path First) algorithm to find the best path to each destination

OSPF converges faster than RIP, has no hop count limit, and supports authentication. Large networks are divided into areas (with Area 0 = backbone) to limit LSA flooding.

### BGP — Border Gateway Protocol

BGP (RFC 4271) is the routing protocol of the internet. It connects autonomous systems (ASes) — independently managed networks identified by a 16 or 32-bit AS number (ASN).

BGP is a path-vector protocol: route advertisements include the full AS path. This allows policy-based routing (prefer routes through certain ASes) and loop prevention (don't accept routes containing your own AS number).

```
AS 65001 (your company) ─────BGP──────► AS 15169 (Google)
AS 65001                 ◄────BGP─────── AS 13335 (Cloudflare)

BGP route advertisement example:
  Prefix: 8.8.8.0/24
  AS Path: 15169 (single hop, Google's own prefix)
  Next Hop: 203.0.113.1 (Google's BGP peer address)
```

BGP peers (neighbors) are configured manually. iBGP connects routers within an AS; eBGP connects routers between ASes. BGP policies control which routes are accepted, preferred, and re-advertised.

BGP security is critical: a misconfigured or malicious AS can announce someone else's prefixes (BGP hijacking) or leak routes it shouldn't (route leak). RPKI (Resource Public Key Infrastructure) provides cryptographic validation of prefix ownership.

---

## Key Concepts

**Autonomous System (AS)** — A network or group of networks under a common routing policy, identified by an ASN. BGP connects ASes. See [[networks#bgp]].

**Interior Gateway Protocol (IGP)** — Routing protocol within an AS (OSPF, RIP, EIGRP).

**Exterior Gateway Protocol (EGP)** — Routing protocol between ASes (BGP).

**Link-state** — Routing approach where every router knows the complete topology; Dijkstra computes shortest paths. OSPF uses this.

**Distance-vector** — Routing approach where routers share their routing table with neighbors; each router infers topology indirectly. RIP uses this.

**OSPF Area** — Subdivision of an OSPF network; LSA flooding is contained within an area. All areas connect to Area 0 (backbone).

**BGP Prefix Advertisement** — When an AS announces to BGP peers that it can route traffic to a specific IP prefix.

**Route Leak** — BGP event where routes are re-advertised to peers that shouldn't see them; can cause traffic misdirection.

---

## Examples

```bash
# View BGP routes on a Linux system with FRRouting
vtysh
show ip bgp summary          # BGP peer status
show ip bgp 8.8.8.0/24       # details for a specific prefix
show ip ospf database         # OSPF link state database
show ip route                 # full routing table

# Inspect BGP from a looking glass (public tool — no installation needed)
# Example: RIPE NCC looking glass at https://lg.ripe.net
```

```python
# Using Python to read the Linux routing table
import subprocess

result = subprocess.run(['ip', 'route', 'show'], capture_output=True, text=True)
for line in result.stdout.splitlines():
    print(line)

# Parse routes programmatically
import ipaddress

# Determine which interface to use for a given destination
def find_route(destination_ip):
    """Find the route that would be used to reach destination_ip."""
    result = subprocess.run(
        ['ip', 'route', 'get', destination_ip],
        capture_output=True, text=True
    )
    return result.stdout.strip()

print(find_route('8.8.8.8'))   # shows which interface and gateway
```

---

## Common Pitfalls

**Forgetting that BGP is trust-based:** BGP peers trust each other's announcements by default. Without RPKI and route filtering, any AS can announce any prefix. Always implement route filters and AS path filtering with BGP peers.

**OSPF area design mistakes:** All OSPF areas must connect to Area 0. Non-zero areas that are not directly connected to Area 0 require a virtual link (complex, error-prone). Plan your area design before deploying OSPF.

**Static route administrative distance:** In most routing stacks, static routes have lower administrative distance (higher priority) than dynamic routing protocols. A static default route will override BGP-learned routes unless you adjust administrative distances.

---

## Cross-Links

- [[networks/modules/03_ip-networking]] — routing tables and CIDR; prerequisite knowledge for this module
- [[networks/modules/08_network-security]] — BGP security (RPKI, route filtering); firewall rules affecting routing
- [[networks/modules/09_sdn-and-cloud-networking]] — cloud routing uses BGP internally (AWS VPC peering, Direct Connect)
- [[networks#bgp]] — BGP glossary entry
- [[devops-platform-engineering]] — BGP is used in Kubernetes for MetalLB, anycast CDN routing, and cloud interconnects

---

## Summary

- Static routes: manually configured; reliable; do not adapt to failures; suitable for small networks and default routes
- RIP: distance-vector; hop count metric (max 15); slow convergence; essentially obsolete
- OSPF: link-state; each router has full topology map; Dijkstra SPF; fast convergence; areas limit flooding; enterprise standard
- BGP: path-vector; connects autonomous systems (ASes); policy-based routing; the internet's routing protocol
- BGP security: route leaks and hijacking are major risks; RPKI provides cryptographic prefix ownership validation
- BGP peering is manual: iBGP within an AS, eBGP between ASes; policies control route acceptance and re-advertisement
