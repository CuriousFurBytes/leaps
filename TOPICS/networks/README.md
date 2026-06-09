# Computer Networks

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> The study of how computers communicate — from the physical signals in a wire to the application protocols that power the web.

> [!NOTE]
> **Topic Overview**
> Computer Networks covers the full stack of technologies, protocols, and design principles that allow billions of devices to exchange data reliably, securely, and at scale. You will build mental models starting from the physics of signal transmission and work all the way up to cloud networking, software-defined infrastructure, and real-world troubleshooting.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty & Time Estimate](#difficulty--time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

Computer networking is the discipline that enables devices to communicate, share resources, and exchange data. At its most fundamental, a network is a collection of nodes (computers, phones, routers, servers) connected by links (copper wire, optical fiber, radio waves) and governed by agreed-upon rules called protocols. Without networks, every computer would be an island — powerful but isolated. With them, we have the internet: a global fabric of interconnected networks that has reshaped commerce, science, governance, and human culture.

The subject spans an enormous range of abstraction levels. At the bottom, it concerns the physics of electromagnetic signals. At the top, it touches the design of distributed systems and cloud architectures. In between lie the protocols — TCP/IP, DNS, HTTP, TLS, BGP — that every engineer interacts with daily, whether or not they are aware of it.

### Why It Matters

Understanding computer networks is essential for every engineer, not just network specialists. When your application is slow, the bottleneck is often the network. When your service is unavailable, the cause is often a routing failure or a misconfigured firewall. When your data is exfiltrated, the attack almost always exploits a network-layer weakness. Network literacy is the difference between engineers who can diagnose production incidents and those who cannot.

Understanding Computer Networks is valuable because:

- It underpins every distributed system — a skill used directly in cloud architecture, microservices, and site reliability engineering
- It develops the mental model for layered abstraction — transferable to operating systems, security, and protocol design
- Proficiency in it is expected in roles such as backend engineer, DevOps/SRE, security engineer, and network engineer

### Key Features of This Topic

- **Protocol-first** — every module explains the protocol's purpose, design decisions, and failure modes, not just how to configure it
- **Practical and runnable** — Python socket examples, Wireshark captures, and command-line tools throughout
- **Bottom-up and top-down** — you build intuition both from the physical layer upward and from applications downward
- **Modern and historical** — covers both the classic TCP/IP stack and modern additions: HTTP/3, WireGuard, QUIC, VXLAN, eBPF

---

## Historical Context

The internet traces its origins to the ARPANET project, funded by the U.S. Department of Defense's Advanced Research Projects Agency (ARPA). ARPANET went live in 1969 connecting four universities: UCLA, SRI, UC Santa Barbara, and the University of Utah. It was the first operational packet-switched network — a radical departure from the circuit-switched telephone networks of the era.

The intellectual breakthrough that made today's internet possible came in 1974, when Vint Cerf and Bob Kahn published "A Protocol for Packet Network Intercommunication," introducing the Transmission Control Program (later split into TCP and IP). This design allowed heterogeneous networks to interconnect without any single authority controlling the whole — the defining characteristic of the internet.

### Timeline

| Year | Event |
|------|-------|
| 1969 | ARPANET goes live; first message sent between UCLA and SRI |
| 1974 | Vint Cerf and Bob Kahn publish the TCP/IP design |
| 1983 | ARPANET transitions to TCP/IP; DNS is introduced (Paul Mockapetris) |
| 1991 | Tim Berners-Lee publishes the World Wide Web at CERN |
| 1993 | Mosaic browser released; the web becomes publicly accessible |
| 1998 | IPv6 standardized (RFC 2460) to address IPv4 address exhaustion |
| 1999 | 802.11b Wi-Fi standard ratified; wireless networking becomes mainstream |
| 2004 | BGP security incidents highlight the fragility of internet routing |
| 2015 | HTTP/2 standardized (RFC 7540); multiplexing and header compression |
| 2018 | TLS 1.3 standardized (RFC 8446); significant security improvements |
| 2022 | HTTP/3 standardized (RFC 9114); QUIC replaces TCP for HTTP |
| Today | Software-defined networking, eBPF, QUIC, and 5G are reshaping the landscape |

---

## Real-World Applications

Computer Networks knowledge is actively applied across every layer of the technology industry:

- **Content Delivery Networks** — Cloudflare and Akamai operate networks with hundreds of PoPs worldwide, using anycast routing, BGP, and HTTP caching to serve content with sub-20ms latency globally
- **Internet Routing at Scale** — BGP (Border Gateway Protocol) is the protocol that holds the internet together, with over 900,000 prefixes exchanged between ~80,000 autonomous systems today
- **Cloud Networking** — AWS VPC, Azure VNet, and GCP VPC implement software-defined overlay networks with VXLAN and BGP EVPN, enabling millions of isolated virtual networks on shared physical infrastructure
- **Google's B4 WAN** — Google operates a private software-defined WAN (B4) across its datacenters that achieves near-100% link utilization, far exceeding the 30-40% typical of traditional WANs
- **Financial Systems** — High-frequency trading firms invest in microwave links and co-location specifically to reduce network latency by microseconds — a direct example of how network performance translates to business outcome
- **Mobile Networks** — LTE and 5G are sophisticated IP networks carrying voice, video, and data for billions of users, incorporating the same TCP/IP principles you will study here

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the OSI and TCP/IP models, map any protocol to its layer, and use this model to systematically diagnose network problems
2. Describe how data travels from an application on one machine to an application on another, including every encapsulation and decapsulation step
3. Design and subnet IPv4 and IPv6 address spaces using CIDR notation for real network architectures
4. Explain the mechanics of TCP's reliability guarantees (3-way handshake, flow control, congestion control) and TCP's failure modes
5. Trace a complete DNS resolution and HTTP/TLS request, identifying where failures can occur at each step
6. Write Python programs that use the BSD socket API for TCP client/server and UDP communication
7. Configure and reason about routing protocols (static, OSPF, BGP) in the context of a multi-site network design
8. Identify and mitigate common network security threats including IP spoofing, ARP poisoning, DNS hijacking, and BGP hijacking
9. Use Wireshark, tcpdump, nmap, MTR, and iperf to diagnose real network issues systematically
10. Design a secure multi-tier network architecture with DMZ, internal, and management segments

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Beginner → Expert |
| **Estimated Total Hours** | 60–80 hours |
| **Prerequisites** | Basic computer literacy; familiarity with the command line is helpful |
| **Recommended Pace** | 5–6 hours/week (12–15 weeks) |
| **Topic Type** | Mixed (Theoretical + Practical) |
| **Suitable For** | Self-taught engineers, CS students, DevOps practitioners, security learners |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- Basic computer literacy — knowing what a file, program, and operating system are
- Command-line basics — navigating a terminal, running programs
- Elementary Python — modules 10 and 11 use Python socket programming; a reading-level familiarity is sufficient

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If the terminology is entirely foreign, spend a day on a basic networking tutorial first.
> If you can follow along but things feel shaky, press on — it will solidify.

---

## Learning Modules

| # | Module | Topic | Status | Score |
|---|--------|-------|--------|-------|
| 01 | [Introduction to Computer Networks](./modules/01_introduction/) | What is a network, OSI model, TCP/IP model, encapsulation, network devices | - [ ] | —/— |
| 02 | [Physical and Data Link Layers](./modules/02_physical-and-datalink/) | Ethernet frames, MAC addresses, ARP, spanning tree, VLANs, Wi-Fi 802.11 | - [ ] | —/— |
| 03 | [IP Networking](./modules/03_ip-networking/) | IPv4/IPv6 addressing, subnetting (CIDR), routing basics, NAT, DHCP | - [ ] | —/— |
| 04 | [Transport Layer](./modules/04_transport-layer/) | TCP handshake, flow control, congestion control, UDP, port numbers | - [ ] | —/— |
| 05 | [Application Layer Protocols](./modules/05_application-layer/) | DNS, HTTP/1.1/2/3, TLS handshake, SMTP | - [ ] | —/— |
| 06 | [Routing Protocols](./modules/06_routing-protocols/) | Static routing, RIP, OSPF, BGP, autonomous systems | - [ ] | —/— |
| 07 | [Wireless Networking](./modules/07_wireless-networking/) | 802.11 standards, CSMA/CA, WPA2/3, LTE/5G overview | - [ ] | —/— |
| 08 | [Network Security](./modules/08_network-security/) | Firewalls, IDS/IPS, VPNs (IPsec, WireGuard), common attacks | - [ ] | —/— |
| 09 | [SDN and Cloud Networking](./modules/09_sdn-and-cloud-networking/) | Software-defined networking, OpenFlow, AWS VPC, VXLAN | - [ ] | —/— |
| 10 | [Network Programming](./modules/10_network-programming/) | Python socket API, TCP/UDP servers, raw sockets, Scapy | - [ ] | —/— |
| 11 | [Troubleshooting and Tools](./modules/11_troubleshooting-and-tools/) | Wireshark, tcpdump, nmap, MTR, iperf, systematic methodology | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Design and implement a secure multi-tier network architecture | - [ ] | —/— |

**Status key:** ` ` Not started &nbsp;·&nbsp; `~` In progress &nbsp;·&nbsp; `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 20 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 264 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 45 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **429** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction)
- [ ] **Foundation Built** — Complete Modules 01–03 with ≥ 70% on each test
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Core Mastery** — Score ≥ 80% on all core module tests (01–05)
- [ ] **First Project Shipped** — Complete at least one Beginner or Intermediate project
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Deep Work** — Complete the Capstone Project
- [ ] **Packet Wrangler** — Use Wireshark/tcpdump to successfully diagnose a real network problem
- [ ] **Socket Coder** — Write a working TCP server and client from scratch in Python

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% &nbsp;·&nbsp; B ≥ 80% &nbsp;·&nbsp; C ≥ 70% &nbsp;·&nbsp; D ≥ 60% &nbsp;·&nbsp; F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for Computer Networks:

- [[pentesting-security]] — network security attacks and defenses build directly on networking fundamentals; packets are the attack surface
- [[devops-platform-engineering]] — cloud networking, VPCs, load balancers, and service meshes are central to platform engineering work
- [[systems-architecture]] — distributed systems design requires deep understanding of network latency, partitions, and protocol semantics

<!-- TODO: cross-link to [[operating-systems]] once that topic is created — network stacks live in the OS kernel -->

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Started Topic

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed prerequisites
- Ready to start Module 01

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "networks"
topic_name: "Computer Networks"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 429
completion_percentage: 0
difficulty: "Beginner → Expert"
estimated_hours: 70
prerequisites:
  - "basic computer literacy"
  - "command-line basics"
related_topics:
  - "pentesting-security"
  - "devops-platform-engineering"
  - "systems-architecture"
tags:
  - "networking"
  - "protocols"
  - "tcp-ip"
  - "internet"
  - "distributed-systems"
creator: "Vint Cerf and Bob Kahn (TCP/IP, 1974)"
year_created: "1969"
```
