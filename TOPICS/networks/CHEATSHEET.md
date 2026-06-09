# Computer Networks — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [OSI Layers Quick Reference](#osi-layers-quick-reference)
- [Common Port Numbers](#common-port-numbers)
- [Subnetting Cheat Sheet](#subnetting-cheat-sheet)
- [TCP State Machine Summary](#tcp-state-machine-summary)
- [DNS Record Types](#dns-record-types)
- [Key Command Reference](#key-command-reference)
- [Decision Guides](#decision-guides)
- [Gotchas & Pitfalls](#gotchas--pitfalls)

---

## OSI Layers Quick Reference

| Layer | Name | PDU | Key Protocols | Key Devices |
|-------|------|-----|--------------|-------------|
| 7 | Application | Data | HTTP, HTTPS, DNS, SMTP, FTP, SSH | Proxy, Load Balancer |
| 6 | Presentation | Data | TLS/SSL, JPEG, ASCII encoding | — |
| 5 | Session | Data | NetBIOS, RPC | — |
| 4 | Transport | Segment (TCP) / Datagram (UDP) | TCP, UDP | Firewall (stateful) |
| 3 | Network | Packet | IP, ICMP, OSPF, BGP | Router |
| 2 | Data Link | Frame | Ethernet (802.3), Wi-Fi (802.11), ARP | Switch, Bridge |
| 1 | Physical | Bit | Ethernet (copper/fiber), Wi-Fi (radio) | Hub, NIC, Cable |

**Memory aid:** "Please Do Not Throw Sausage Pizza Away" (Physical, Data Link, Network, Transport, Session, Presentation, Application)

**TCP/IP 4-Layer Mapping:**

| TCP/IP Layer | Covers OSI Layers | Examples |
|-------------|-------------------|---------|
| Application | 5, 6, 7 | HTTP, DNS, TLS, SMTP |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP |
| Link | 1, 2 | Ethernet, Wi-Fi |

---

## Common Port Numbers

| Port | Protocol | Service |
|------|----------|---------|
| 20/21 | TCP | FTP (data/control) |
| 22 | TCP | SSH |
| 23 | TCP | Telnet (insecure — avoid) |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67/68 | UDP | DHCP (server/client) |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 179 | TCP | BGP |
| 443 | TCP | HTTPS (HTTP over TLS) |
| 465 | TCP | SMTPS (SMTP over TLS) |
| 500 | UDP | IKE (IPsec key exchange) |
| 514 | UDP | Syslog |
| 587 | TCP | SMTP Submission |
| 993 | TCP | IMAPS |
| 1194 | UDP | OpenVPN |
| 3306 | TCP | MySQL |
| 3389 | TCP | RDP (Windows Remote Desktop) |
| 5432 | TCP | PostgreSQL |
| 6443 | TCP | Kubernetes API server |
| 8080 | TCP | HTTP alternate / dev servers |
| 51820 | UDP | WireGuard |

---

## Subnetting Cheat Sheet

### IPv4 CIDR Quick Reference

| Prefix | Subnet Mask | Usable Hosts | Example Use |
|--------|-------------|-------------|-------------|
| /30 | 255.255.255.252 | 2 | Point-to-point links |
| /29 | 255.255.255.248 | 6 | Small office segment |
| /28 | 255.255.255.240 | 14 | Small office |
| /27 | 255.255.255.224 | 30 | Small-medium segment |
| /26 | 255.255.255.192 | 62 | Medium segment |
| /25 | 255.255.255.128 | 126 | Medium-large segment |
| /24 | 255.255.255.0 | 254 | Standard LAN |
| /23 | 255.255.254.0 | 510 | Large LAN |
| /22 | 255.255.252.0 | 1022 | Campus network |
| /16 | 255.255.0.0 | 65534 | Large enterprise |
| /8 | 255.0.0.0 | 16777214 | Major ISP block |

**Formula:** Usable hosts = 2^(32 - prefix) - 2

### Private IPv4 Address Ranges (RFC 1918)

| Range | CIDR | Typical Use |
|-------|------|-------------|
| 10.0.0.0–10.255.255.255 | 10.0.0.0/8 | Large enterprises, VPNs |
| 172.16.0.0–172.31.255.255 | 172.16.0.0/12 | Medium enterprises |
| 192.168.0.0–192.168.255.255 | 192.168.0.0/16 | Home/small office |

### IPv6 Quick Reference

| Type | Prefix | Notes |
|------|--------|-------|
| Global Unicast | 2000::/3 | Routable on internet |
| Link-Local | fe80::/10 | Not routed; one hop only |
| Loopback | ::1/128 | Same as 127.0.0.1 in IPv4 |
| Documentation | 2001:db8::/32 | Use in examples/docs (like this file) |

---

## TCP State Machine Summary

```
CLOSED → (SYN sent) → SYN_SENT → (SYN-ACK received, ACK sent) → ESTABLISHED
                                                                        │
LISTEN → (SYN received, SYN-ACK sent) → SYN_RCVD → (ACK received) → ESTABLISHED
                                                                        │
                                                           (FIN sent) → FIN_WAIT_1
                                                           (FIN received) → CLOSE_WAIT
                                                                        │
                                                           (ACK received) → FIN_WAIT_2
                                                           (FIN sent, ACK received) → LAST_ACK
                                                                        │
                                                           (FIN received, ACK sent) → TIME_WAIT → CLOSED
```

**3-Way Handshake:**
```
Client          Server
  │──── SYN ────►│   (Client ISN: x)
  │◄── SYN-ACK ──│   (Server ISN: y, ACK: x+1)
  │──── ACK ────►│   (ACK: y+1)
  │   ESTABLISHED│
```

**4-Way Teardown:**
```
Active Closer   Passive Closer
  │──── FIN ────►│
  │◄──── ACK ────│
  │◄──── FIN ────│
  │──── ACK ────►│
  │  TIME_WAIT   │  (waits 2×MSL before CLOSED)
```

---

## DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| A | IPv4 address | `example.com. A 93.184.216.34` |
| AAAA | IPv6 address | `example.com. AAAA 2606:2800:220:1:248:1893:25c8:1946` |
| CNAME | Canonical name (alias) | `www.example.com. CNAME example.com.` |
| MX | Mail exchanger | `example.com. MX 10 mail.example.com.` |
| NS | Name server | `example.com. NS ns1.example.com.` |
| TXT | Arbitrary text | `example.com. TXT "v=spf1 include:..."` |
| PTR | Reverse DNS (IP→hostname) | `34.216.184.93.in-addr.arpa. PTR example.com.` |
| SOA | Start of Authority | Zone metadata; serial number for replication |

---

## Key Command Reference

| Command | What It Does | Example |
|---------|-------------|---------|
| `ping <host>` | Test reachability and measure RTT | `ping google.com` |
| `traceroute <host>` | Trace hop-by-hop path | `traceroute 8.8.8.8` |
| `mtr <host>` | Combined traceroute + ongoing RTT stats | `mtr github.com` |
| `nslookup <name>` | DNS query (basic) | `nslookup example.com` |
| `dig <name>` | DNS query (detailed) | `dig +short A example.com` |
| `dig +trace <name>` | Full DNS resolution trace | `dig +trace github.com` |
| `netstat -tulnp` | Show listening ports and processes | `netstat -tulnp` |
| `ss -tulnp` | Modern replacement for netstat | `ss -tulnp` |
| `ip addr` | Show network interfaces and IPs | `ip addr show eth0` |
| `ip route` | Show routing table | `ip route show` |
| `tcpdump -i eth0` | Capture packets on interface | `tcpdump -i eth0 port 80` |
| `nmap -sS <host>` | TCP SYN scan of host | `nmap -sS 192.168.1.0/24` |
| `iperf3 -s` | Start iperf server | `iperf3 -s -p 5201` |
| `iperf3 -c <host>` | Measure bandwidth to server | `iperf3 -c 192.168.1.1` |
| `curl -v <url>` | HTTP request with verbose headers | `curl -v https://example.com` |
| `openssl s_client` | Inspect TLS certificate and handshake | `openssl s_client -connect example.com:443` |

---

## Decision Guides

### Which transport protocol should I use?

```
Need to choose TCP vs UDP?
│
├── Need guaranteed delivery and ordering?
│   └── YES → Use TCP
│       (HTTP, HTTPS, SSH, database connections, file transfer)
│
├── Can tolerate packet loss? Is low latency critical?
│   └── YES → Consider UDP
│       (DNS queries, NTP, VoIP, live video streaming, games)
│
├── Are you implementing a request-response in a single packet?
│   └── YES → UDP is simpler (DNS, SNMP)
│
└── Not sure? → Default to TCP unless you have a specific reason not to
```

### Which IP address range for a new network?

```
Designing a new private network?
│
├── Huge enterprise (>65k hosts)?
│   └── Use 10.0.0.0/8 with careful subnetting
│
├── Medium enterprise (1k–64k hosts)?
│   └── Use 172.16.0.0/12 or a large block from 10.0.0.0/8
│
├── Home / small office (<254 hosts per segment)?
│   └── Use 192.168.0.0/16 with /24 subnets
│
└── Need to avoid conflicts with RFC 1918 (e.g., VPNs)?
    └── Use 100.64.0.0/10 (CGNAT range, RFC 6598) or coordinate with your ISP
```

---

## Gotchas & Pitfalls

> [!WARNING]
> **Forgetting that subnet masks affect routing, not just addressing**
> A common mistake is assigning an IP with the wrong prefix length. If your server is `10.0.1.5/24` but the router has `10.0.1.5/16`, they have different views of what's local vs. what needs a gateway.
>
> Wrong: `ip addr add 10.0.1.5/16 dev eth0` (when all other hosts are /24)
> Right: `ip addr add 10.0.1.5/24 dev eth0`

> [!WARNING]
> **Assuming TCP delivers message boundaries**
> TCP is a byte stream, not a message protocol. `send("hello")` on one side does NOT guarantee `recv()` on the other side returns exactly `"hello"`. TCP may split or merge writes arbitrarily.
>
> Wrong: Assuming one `send()` = one `recv()`
> Right: Prefix messages with their length, or use a delimiter, and read in a loop until you have a complete message.

> [!WARNING]
> **Confusing NAT with a firewall**
> NAT (Network Address Translation) is not a security mechanism — it's an address translation mechanism. A NAT device that happens to block unsolicited inbound connections provides some protection, but this is a side effect, not the purpose. Use explicit firewall rules for security.

**Other things to watch out for:**

- **TTL expires on traceroute** — `traceroute` works by sending packets with TTL=1, 2, 3… Each router decrements TTL and sends ICMP Time Exceeded when it hits 0. Some routers rate-limit ICMP, causing `***` hops that don't indicate a real outage.
- **TIME_WAIT sockets** — After a TCP connection closes, the active closer stays in TIME_WAIT for 2×MSL (typically 60–120 seconds). Under high connection rates, this can exhaust ephemeral ports. Use `SO_REUSEADDR` on servers.
- **BGP is trust-based** — BGP announcements are not authenticated by default. A misconfigured (or malicious) router can announce someone else's IP prefixes, causing traffic to be misdirected. This is called BGP hijacking.
- **DNS is not encrypted by default** — Plain DNS queries over UDP are visible to anyone between you and the resolver. DNS over HTTPS (DoH) and DNS over TLS (DoT) address this.

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| OSI model and encapsulation | [[networks/modules/01_introduction]] |
| Ethernet frames and MAC addresses | [[networks/modules/02_physical-and-datalink]] |
| IP addressing and subnetting | [[networks/modules/03_ip-networking]] |
| TCP mechanics and states | [[networks/modules/04_transport-layer]] |
| DNS and HTTP details | [[networks/modules/05_application-layer]] |
| BGP and routing protocols | [[networks/modules/06_routing-protocols]] |
| Firewall and VPN configuration | [[networks/modules/08_network-security]] |
| Python socket programming | [[networks/modules/10_network-programming]] |
| Troubleshooting methodology | [[networks/modules/11_troubleshooting-and-tools]] |

---

_Last updated: 2026-06-09_
