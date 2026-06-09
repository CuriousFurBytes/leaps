# Networks

> A zero-to-expert path for understanding, designing, troubleshooting, and operating computer networks.

## Table of Contents
1. [Why Learn Networks?](#why-learn-networks)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn Networks?
Computer networks are the systems that let independent machines exchange data reliably across rooms, buildings, continents, and clouds. Every website, API, database connection, video call, software deployment, payment authorization, multiplayer game, and monitoring alert depends on networks doing many small jobs correctly.

Learning networks deeply gives you a practical mental model for failures that otherwise look mysterious. A slow page load might be DNS, routing, congestion, TLS negotiation, packet loss, application queuing, or a bad retry policy. Network fluency helps you separate symptoms from causes and choose the right measurement before changing production systems.

Networks also bridge hardware, operating systems, distributed systems, security, and [[devops-platform-engineering]]. Beginners start by learning packets, addresses, and protocols; experts learn capacity planning, resilience, observability, automation, zero-trust architecture, and tradeoffs in large multi-region systems.

## Prerequisites
- Basic computer literacy: files, terminals, and editing plain text.
- Basic arithmetic for binary and powers of two; Module 03 teaches the networking-specific parts.
- operating systems — helpful for sockets, processes, interfaces, and routing tables.
- security — useful later for TLS, firewalls, segmentation, and threat modeling.
- No prior networking knowledge is assumed; Module 01 starts from ground zero.

## Module Map
| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Introduction to Networks](./modules/01_introduction/README.md) | Beginner | [ ] |
| 02 | [Layered Models and Encapsulation](./modules/02_layered_models/README.md) | Beginner | [ ] |
| 03 | [IP Addressing and Subnetting](./modules/03_ip_addressing_subnetting/README.md) | Intermediate | [ ] |
| 04 | Ethernet, Wi-Fi, and Local Networks | Intermediate | [ ] |
| 05 | Routing, Switching, and Path Selection | Intermediate | [ ] |
| 06 | Transport Protocols: TCP, UDP, and QUIC | Advanced | [ ] |
| 07 | DNS, HTTP, TLS, and Application Protocols | Advanced | [ ] |
| 08 | Firewalls, NAT, VPNs, and Network Security | Advanced | [ ] |
| 09 | Observability, Troubleshooting, and Packet Analysis | Advanced | [ ] |
| 10 | Performance, Congestion, and Reliability Engineering | Expert | [ ] |
| 11 | Cloud, Data Center, and Internet-Scale Architecture | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links
- operating systems — hosts expose network interfaces, sockets, ports, and routing tables.
- [[devops-platform-engineering]] — production platforms depend on load balancing, service discovery, and network observability.
- [[postgresql]] — databases depend on reliable connections, ports, TLS, and latency-aware deployment choices.
- [[javascript-typescript-react]] — browser applications expose network behavior through HTTP requests, errors, caching, and retries.

## Quick Reference
| Need | Tool or Concept |
|---|---|
| Identify local interfaces | `ip addr` or `ifconfig` |
| View routes | `ip route` or `netstat -rn` |
| Test reachability | `ping example.com` |
| Trace path selection | `traceroute example.com` or `tracepath example.com` |
| Query DNS | `dig example.com` or `nslookup example.com` |
| Inspect listening ports | `ss -tulpen` |
| Capture packets | `tcpdump -i any host example.com` |
| Address a network | CIDR, such as `192.0.2.0/24` |
| Separate services | Ports, VLANs, subnets, security groups, and firewall rules |

```bash
# A tiny first diagnostic flow: name resolution, reachability, and path.
dig example.com
ping -c 3 example.com
traceroute example.com
```
