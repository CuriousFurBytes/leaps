# Resources — Module 01: Introduction to Computer Networks

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Cloudflare Learning: "What is the OSI Model?"](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)** — Cloudflare Learning Center

Clear, accurate, and practical explanation of the OSI model with real-world examples and visual diagrams. Cloudflare explains each layer in terms of their actual CDN/networking work, which grounds the theory in production use.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[RFC 791 — Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)** — The original IPv4 specification; reading Sections 1 and 2 gives you the design rationale directly from Jon Postel
- **[RFC 792 — Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792)** — Defines ICMP; explains why `ping` and `traceroute` work the way they do

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| Computer Networks (Tanenbaum & Wetherall, 5th ed.) | Ch. 1 — "Introduction" | Covers network types, reference models (both OSI and TCP/IP), and network hardware |
| Computer Networking: A Top-Down Approach (Kurose & Ross, 8th ed.) | Ch. 1 — "Computer Networks and the Internet" | Top-down approach; focuses on why the internet works, packet vs. circuit switching |
| TCP/IP Illustrated Vol. 1 (Stevens, 2nd ed.) | Ch. 1 — "Overview" | Terse but precise introduction to TCP/IP architecture |

---

## Videos

_Specific videos that explain this module's concepts well._

- **[Verify: "OSI Model Explained" — PowerCert Animated Videos]** (YouTube, ~9 min) — Visual animated walkthrough; verify URL before relying on it
- **[Verify: Networking Fundamentals series — Practical Networking]** (YouTube) — Systematic coverage of OSI and TCP/IP models; check playlist for "OSI Model" episodes

---

## Practice Sites

_Places to get more practice problems for the specific skills in this module._

- **[Subnet Calculator (verify: subnet.tips or similar)]** — Use any online subnet calculator to check your subnetting work from Exercise 5
- **[Wireshark Sample Captures](https://wiki.wireshark.org/SampleCaptures)** — Download pcap files and open them in Wireshark to observe encapsulation in real packets

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[networks/modules/02_physical-and-datalink]] (Module 02: Physical and Data Link) | Dives deep into Layer 2: Ethernet frames, MAC addresses, and ARP |
| [[networks/modules/03_ip-networking]] (Module 03: IP Networking) | Covers the Layer 3 packet in detail: IP addressing, routing, NAT |
| [[networks/modules/04_transport-layer]] (Module 04: Transport Layer) | Covers TCP and UDP — the Layer 4 protocols introduced here |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Relationship |
|-------|-------------|
| [[pentesting-security]] | Network attacks exploit the layers introduced in this module; understanding OSI is prerequisite to understanding attack surfaces |
| [[devops-platform-engineering]] | Cloud networking, VPCs, and security groups are all built on the Layer 2/3/4 concepts from this module |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] [Verify: "Networking for Web Developers" — Udacity free course] — reportedly a good practical intro
- [ ] [Verify: Julia Evans "Networking! ACK!" zine] — visual explanations of networking fundamentals
