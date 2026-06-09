# Computer Networks — Resources

> [!WARNING]
> **Verified resources only.** Every entry in this file must be something you have
> personally confirmed exists, is accessible, and is genuinely useful.
> Do not add resources based on hearsay, AI suggestions, or titles that "sound right."
> A short list of excellent resources beats a long list of unverified ones.

---

## Official Documentation

- **[RFC Index](https://www.rfc-editor.org/rfc-index.html)** — The Internet Engineering Task Force (IETF) publishes every internet standard as an RFC. When in doubt about how a protocol works, read the RFC.
- **[IANA Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)** — Authoritative list of well-known port assignments
- **[Cloudflare Learning Center](https://www.cloudflare.com/learning/)** — Excellent, up-to-date explanations of DNS, HTTP, TLS, DDoS, and CDN concepts; free to read

---

## Books

| Title | Author | Level | Format | Notes |
|-------|--------|-------|--------|-------|
| Computer Networks, 5th Edition | Andrew S. Tanenbaum & David J. Wetherall | Beginner → Advanced | Print/eBook | The canonical university textbook; covers all layers with depth; 5th ed. (2010) is widely used |
| TCP/IP Illustrated, Volume 1, 2nd Edition | W. Richard Stevens (updated by Kevin R. Fall) | Intermediate → Advanced | Print/eBook | Exhaustive packet-level treatment of TCP/IP; the definitive reference for protocol internals |
| Computer Networking: A Top-Down Approach, 8th Edition | James Kurose & Keith Ross | Beginner → Intermediate | Print/eBook | Excellent for beginners; starts from applications and works down; widely used in universities |
| Beej's Guide to Network Programming | Brian "Beej" Hall | Beginner → Intermediate | Free online | [Verify: beej.us/guide/bgnet/] — Practical socket programming guide; plain English; highly recommended before Module 10 |

_Use ISBN or direct publisher links where possible to avoid linking to pirated copies._

---

## Online Courses

| Course | Platform | Level | Free? | Notes |
|--------|----------|-------|-------|-------|
| [Verify: "The Bits and Bytes of Computer Networking" — Google/Coursera] | Coursera | Beginner | Audit free | Part of Google IT Support Certificate; solid intro coverage |
| [Verify: CS144 "Introduction to Computer Networking" — Stanford] | YouTube/Stanford | Intermediate | Yes | Lecture videos from Stanford's networking course; excellent depth |

---

## Video Resources

| Title / Channel | URL | Type | Level | Notes |
|-----------------|-----|------|-------|-------|
| [Verify: "How the Internet Works" lecture series — Hussein Nasser] | YouTube | Series | Beginner | Engineering-focused explanations of HTTP, DNS, TCP |
| [Verify: "Networking Fundamentals" — Practical Networking] | YouTube | Series | Beginner → Intermediate | Clear, visual explanations of subnetting and routing |

---

## Blogs & Articles

- **[Cloudflare Blog](https://blog.cloudflare.com/)** — Engineering posts on BGP, DNS, TLS, HTTP/3, QUIC, and DDoS; consistently high quality and technically accurate
- **[The Morning Paper](https://blog.acolyer.org/)** — Adrian Colyer's summaries of CS papers, including many networking papers _(note: archived, not actively updated as of 2023)_
- **[Packet Pushers](https://packetpushers.net/)** — Networking industry blog and podcast; strong on BGP, SD-WAN, and cloud networking

---

## Papers & Research

| Title | Authors | Year | Link | Why It Matters |
|-------|---------|------|------|---------------|
| A Protocol for Packet Network Intercommunication | Vint Cerf & Bob Kahn | 1974 | [IEEE Xplore](https://ieeexplore.ieee.org/document/1092259) | The original TCP/IP paper; foundational reading |
| B4: Experience with a Globally-Deployed Software Defined WAN | Jain et al. (Google) | 2013 | [ACM SIGCOMM](https://dl.acm.org/doi/10.1145/2486001.2486019) | How Google built a software-defined WAN achieving near-100% utilization |
| QUIC: A UDP-Based Multiplexed and Secure Transport | Iyengar & Thomson | 2021 | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) | The QUIC protocol that underlies HTTP/3 |

---

## Tools & Libraries

| Tool / Library | Language / Platform | Purpose | Link |
|---------------|---------------------|---------|------|
| Wireshark | Cross-platform | Packet capture and analysis | [wireshark.org](https://www.wireshark.org/) |
| tcpdump | Linux/macOS | CLI packet capture | [tcpdump.org](https://www.tcpdump.org/) |
| nmap | Cross-platform | Network scanning and host discovery | [nmap.org](https://nmap.org/) |
| iperf3 | Cross-platform | Network bandwidth testing | [github.com/esnet/iperf](https://github.com/esnet/iperf) |
| Scapy | Python | Packet crafting and analysis | [scapy.net](https://scapy.net/) |
| mtr | Linux/macOS | Combined traceroute + ping | [bitwizard.nl/mtr/](https://www.bitwizard.nl/mtr/) |
| GNS3 | Cross-platform | Network simulation environment | [gns3.com](https://www.gns3.com/) |
| Mininet | Python/Linux | Software-defined networking emulation | [mininet.org](http://mininet.org/) |

---

## Communities

| Community | Platform | Focus | Link |
|-----------|----------|-------|------|
| r/networking | Reddit | General networking discussion | [reddit.com/r/networking](https://www.reddit.com/r/networking/) |
| r/netsec | Reddit | Network security | [reddit.com/r/netsec](https://www.reddit.com/r/netsec/) |
| Network Engineering Stack Exchange | Stack Exchange | Technical Q&A | [networkengineering.stackexchange.com](https://networkengineering.stackexchange.com/) |
| IETF Working Groups | Mailing Lists | Protocol standards development | [ietf.org](https://www.ietf.org/) |
| Packet Pushers Community | Forum | Enterprise networking | [packetpushers.net/community/](https://packetpushers.net/community/) |

---

## Cheat Sheets & Quick References

- See the local [CHEATSHEET.md](./CHEATSHEET.md) which you'll build yourself as you study

---

## My Recommendations

_Fill in as you progress — what actually helped you most?_

### Best for Absolute Beginners
> _To be filled in_

### Best for Building Mental Models
> _To be filled in_

### Best for Practical / Hands-On Learning
> _To be filled in_

### Best Deep Reference
> _To be filled in_

---

## Resources to Evaluate

_Drop links here when you find something but haven't verified it yet._

- [ ] [Verify: Julia Evans networking zine "Networking! ACK!"] — reportedly excellent visual intro
- [ ] [Verify: "High Performance Browser Networking" by Ilya Grigorik — O'Reilly] — HTTP/2, QUIC, WebRTC
