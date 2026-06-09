# Module 03: IP Networking

[← Previous](../02_physical-and-datalink/) | [Topic Home](../../README.md) | [Next →](../04_transport-layer/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-blue)
![Time](https://img.shields.io/badge/time-6h-orange)

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

This module covers IPv4 and IPv6 addressing, subnetting with CIDR notation, routing fundamentals, NAT, and DHCP. These are the core skills every engineer uses when configuring servers, designing networks, or debugging connectivity issues. Subnetting is a skill that requires practice — the exercises in this module will build fluency.

---

## Prerequisites

- Module 01: Introduction — OSI model, packets, and encapsulation
- Module 02: Physical and Data Link — frames, MAC addresses, and ARP (helps understand how IP interacts with Layer 2)

---

## Objectives

By the end of this module, you will be able to:

1. Explain the structure of an IPv4 address and classify addresses by class and purpose (private, public, loopback, multicast)
2. Subnet a given IPv4 address space using CIDR notation without a calculator
3. Explain IPv6 addressing, the differences from IPv4, and why IPv6 was necessary
4. Describe how IP routing works: routing tables, next-hop forwarding, and the longest-prefix match rule
5. Explain NAT (Network Address Translation) — how it works, why it exists, and its limitations
6. Describe the DHCP process (DORA: Discover, Offer, Request, Acknowledge) and what information DHCP provides

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.
> The objectives above define what you need to learn. Use the resources in RESOURCES.md
> and the key concepts below as a guide.

### IPv4 Addressing

An IPv4 address is a 32-bit number written in dotted-decimal notation (e.g., `192.168.1.100`). It has two parts: a network prefix and a host identifier. The prefix length (CIDR notation) determines where the boundary is.

**Special address ranges:**
- `127.0.0.0/8` — loopback (localhost)
- `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` — RFC 1918 private space
- `169.254.0.0/16` — link-local (APIPA, assigned when DHCP fails)
- `224.0.0.0/4` — multicast
- `255.255.255.255` — limited broadcast

### Subnetting

Subnetting divides a large address block into smaller blocks. The key operations:
- **Network address:** IP AND subnet_mask
- **Broadcast address:** IP OR (NOT subnet_mask)
- **Usable hosts:** 2^(host_bits) - 2

```python
import ipaddress

# Python ipaddress module for subnetting
network = ipaddress.IPv4Network('192.168.1.0/24')
print(f"Network: {network.network_address}")
print(f"Broadcast: {network.broadcast_address}")
print(f"Usable hosts: {network.num_addresses - 2}")
print(f"Subnet mask: {network.netmask}")

# Subnet into 4 equal subnets (/26 each)
subnets = list(network.subnets(prefixlen_diff=2))
for subnet in subnets:
    print(f"  Subnet: {subnet}")
```

### IPv6

IPv6 uses 128-bit addresses written in colon-separated hexadecimal groups:
`2001:0db8:85a3:0000:0000:8a2e:0370:7334`

Can be abbreviated by removing leading zeros and replacing consecutive all-zero groups with `::`:
`2001:db8:85a3::8a2e:370:7334`

IPv6 was necessary because IPv4's 4 billion addresses were exhausted. IPv6 provides 3.4×10^38 addresses — effectively unlimited. IPv6 also simplifies routing (no NAT needed), includes mandatory IPsec support, and has stateless address autoconfiguration (SLAAC).

### Routing Tables and Longest-Prefix Match

A routing table maps destination prefixes to next hops. When a router receives a packet, it finds the most specific (longest prefix) matching route:

```bash
# View the routing table
ip route show

# Example output:
# default via 192.168.1.1 dev eth0       # /0 — default route
# 192.168.1.0/24 dev eth0 proto kernel   # /24 — directly connected
# 10.0.0.0/8 via 192.168.1.254 dev eth0  # /8 — static route

# If destination is 10.0.0.50:
# Match: 10.0.0.0/8 (prefix length 8) beats default (prefix length 0)
# → forward to 192.168.1.254
```

### NAT

NAT (Network Address Translation) allows multiple devices with private IPs to share a single public IP. The router maintains a NAT table mapping (private_ip, private_port) ↔ (public_ip, public_port).

NAT breaks the end-to-end principle of the internet: a server on the internet cannot initiate a connection to a host behind NAT without additional mechanisms (port forwarding, UPnP, hole-punching).

### DHCP

DHCP (Dynamic Host Configuration Protocol) automatically assigns IP configuration to hosts. The DORA process:

```
Client                          DHCP Server
  │── DISCOVER (broadcast) ────►│
  │◄── OFFER ────────────────────│  (offers IP: 192.168.1.100)
  │── REQUEST (broadcast) ─────►│  (requests offered IP)
  │◄── ACKNOWLEDGE ──────────────│  (confirmed; lease time: 24h)
```

DHCP provides: IP address, subnet mask, default gateway, DNS server(s), and lease duration.

---

## Key Concepts

**CIDR** — Classless Inter-Domain Routing; expresses network prefix as `address/prefix-length`. See [[networks#cidr]].

**Subnet mask** — Defines the network/host boundary. `/24` = `255.255.255.0`. See [[networks#subnet-mask]].

**Default gateway** — The router an end host sends packets to when the destination is not on the local subnet.

**Longest-prefix match** — When multiple routes match a destination, the router chooses the most specific (longest prefix). This is how the internet's routing system works at scale.

**NAT** — Maps private IP:port to public IP:port; hides internal addresses; breaks end-to-end connectivity. See [[networks#nat]].

**DHCP** — Automatically assigns IP configuration; eliminates manual configuration at scale.

---

## Examples

```python
# Subnetting with the ipaddress module
import ipaddress

# Check if an IP is in a network
network = ipaddress.IPv4Network('10.0.0.0/8')
host = ipaddress.IPv4Address('10.5.3.100')
print(host in network)  # True

# Calculate the subnet for a given IP/prefix
interface = ipaddress.IPv4Interface('192.168.1.50/26')
print(f"Network: {interface.network}")      # 192.168.1.32/26
print(f"Host: {interface.ip}")              # 192.168.1.50
print(f"Broadcast: {interface.network.broadcast_address}")  # 192.168.1.63
```

---

## Common Pitfalls

**Forgetting that /31 and /32 are valid prefixes:** `/31` (2 addresses, used for point-to-point links per RFC 3021) and `/32` (1 host, used for loopback or policy routing) are valid. Don't assume every subnet has a network and broadcast address consuming 2 addresses.

**Confusing NAT with a firewall:** NAT translates addresses; it is not a security mechanism (though NAPT happens to block unsolicited inbound connections as a side effect). See [[networks/modules/08_network-security]] for proper firewall design.

**Overlapping subnets in VPNs:** When connecting two offices via VPN, their IP ranges must not overlap. If both use `192.168.1.0/24`, routing will be ambiguous. Always plan IP ranges before deploying.

---

## Cross-Links

- [[networks/modules/02_physical-and-datalink]] — ARP bridges Layer 2 and Layer 3; understanding MAC addresses is prerequisite
- [[networks/modules/04_transport-layer]] — TCP/UDP ports combine with IP addresses to form socket endpoints
- [[networks/modules/06_routing-protocols]] — builds on routing table concepts; covers OSPF and BGP
- [[networks#cidr]] — glossary entry for CIDR notation
- [[devops-platform-engineering]] — VPC subnetting, security groups, and route tables are applied IP networking

---

## Summary

- IPv4 addresses are 32 bits; written as four decimal octets; divided into network (prefix) and host portions by CIDR
- Private ranges (RFC 1918): 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 — not routable on the internet
- Subnetting: network_address = IP AND mask; broadcast = IP OR NOT(mask); usable hosts = 2^(host_bits) - 2
- IPv6 uses 128-bit addresses; solves IPv4 address exhaustion; simplifies routing (no NAT required)
- Routing uses longest-prefix match: the most specific route wins
- NAT maps private IP:port to public IP:port; necessary because of IPv4 exhaustion; breaks end-to-end connectivity
- DHCP automates IP configuration via DORA (Discover, Offer, Request, Acknowledge)
