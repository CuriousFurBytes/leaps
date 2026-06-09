# Module 11: Troubleshooting and Tools

[← Previous](../10_network-programming/) | [Topic Home](../../README.md) | [Next →](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-blue)
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

Network troubleshooting is a skill that separates engineers who can diagnose production incidents from those who cannot. This module covers the primary tools — Wireshark, tcpdump, nmap, traceroute, MTR, and iperf — and develops a systematic methodology for diagnosing network problems layer by layer. The methodology matters as much as the tools: randomly trying things wastes time; a structured approach pinpoints the issue efficiently.

---

## Prerequisites

- All previous modules — this module synthesizes knowledge from the entire topic
- Comfort with the command line and basic Linux administration

---

## Objectives

By the end of this module, you will be able to:

1. Capture packets with tcpdump using appropriate filters and analyze them in Wireshark
2. Use nmap for host discovery, port scanning, and service identification
3. Use MTR to diagnose path latency and packet loss with persistent statistics
4. Use iperf3 to measure TCP/UDP throughput and identify bandwidth bottlenecks
5. Apply a systematic layer-by-layer troubleshooting methodology
6. Diagnose the five most common network problems: no connectivity, wrong IP/routing, DNS failure, firewall block, MTU mismatch

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### Systematic Troubleshooting Methodology

The core principle: **start at Layer 1, work upward.** Each layer depends on the layer below. A routing problem (Layer 3) cannot exist if Layer 1/2 is broken — so confirming lower layers lets you eliminate them as causes.

```
Layer 1: Is the cable/radio link up? (ip link show, check interface LED)
Layer 2: Is ARP working? (arp -n, ping the gateway)
Layer 3: Does routing work? (ip route, ping a remote IP)
Layer 4: Is TCP/UDP reaching the port? (nc -zv host port, nmap)
Layer 5-7: Is the application responding? (curl, dig, telnet)
```

**The five most common problems:**

1. **No connectivity at all** → check Layer 1 (link down?) then Layer 2 (ARP fails? wrong subnet?)
2. **Wrong IP or routing** → `ip addr`, `ip route`, `ping gateway`
3. **DNS failure** → `dig @8.8.8.8 hostname` (bypass local resolver to test)
4. **Firewall blocking** → `nmap` from outside; `iptables -L` from inside
5. **MTU mismatch** → `ping -M do -s 1472` (large ping with DF bit); symptom: small packets work, large don't

### Wireshark

Wireshark is a GUI packet analyzer. Key skills:
- Capture live traffic on an interface
- Apply display filters: `tcp.port == 443`, `ip.addr == 192.168.1.1`, `http`
- Follow TCP streams: right-click a TCP packet → Follow → TCP Stream
- Analyze TLS (if you have the session key log): Preferences → TLS → key log file
- Export filtered packets to a new pcap

```bash
# Capture to file (Wireshark can open this)
tcpdump -i eth0 -w capture.pcap

# Common tcpdump filters
tcpdump -i eth0 host 8.8.8.8               # traffic to/from 8.8.8.8
tcpdump -i eth0 port 443                    # HTTPS traffic
tcpdump -i eth0 tcp and port 80 -w http.pcap  # save HTTP traffic
tcpdump -i eth0 'tcp[tcpflags] & (tcp-syn) != 0'  # SYN packets only
tcpdump -i any -nn -q                        # all interfaces, no hostname resolution, brief
```

### nmap

nmap discovers hosts and open ports:

```bash
# Host discovery: which hosts are up?
nmap -sn 192.168.1.0/24

# TCP SYN scan: which ports are open?
nmap -sS -p 22,80,443,3306 192.168.1.100

# Service and version detection
nmap -sV 192.168.1.100

# OS detection (requires root)
sudo nmap -O 192.168.1.100

# Full scan with output
nmap -sS -sV -p- -T4 -oN scan_results.txt 192.168.1.100
```

### MTR

MTR (Matt's Traceroute) combines `ping` and `traceroute` into a persistent, updating display:

```bash
mtr --report --report-cycles 100 google.com
# Runs 100 cycles; shows loss% and RTT stats per hop
# Loss at hop 3 but not hop 4+ → that router drops probes (not a real outage)
# Loss at hop 3 AND all subsequent → real packet loss at hop 3
```

### iperf3

iperf3 measures network throughput:

```bash
# On server:
iperf3 -s -p 5201

# On client: TCP test (10 seconds)
iperf3 -c server_ip -p 5201 -t 10

# UDP test (100 Mbps target)
iperf3 -c server_ip -u -b 100M -t 10

# Bidirectional test
iperf3 -c server_ip --bidir -t 10
```

---

## Key Concepts

**Packet capture** — Recording network traffic for later analysis. tcpdump captures to pcap format; Wireshark reads and analyzes.

**BPF filter** — Berkeley Packet Filter syntax used by tcpdump and Wireshark to select which packets to capture or display.

**Port scanning** — Probing a host's ports to determine which services are listening. nmap is the standard tool.

**Round-trip time (RTT)** — Measured by ping/MTR; a key indicator of path latency. See [[networks#latency]].

**Throughput** — Actual data rate achieved over a connection; iperf3 measures this. Affected by RTT, window size, and packet loss.

**MTU mismatch** — A situation where a packet exceeds the MTU at some hop and either gets fragmented (if DF=0) or silently dropped (if DF=1). Symptom: SSH works but `scp` of large files hangs; small pings work but large ones fail.

---

## Examples

```python
# Python: check if a host is reachable on a specific port (like nc -zv)
import socket

def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Return True if TCP port is open on host."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as _:
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

# Test multiple services
services = [('google.com', 443), ('github.com', 22), ('localhost', 3306)]
for host, port in services:
    status = "OPEN" if check_port(host, port) else "closed/filtered"
    print(f"{host}:{port} → {status}")
```

```bash
# Diagnose a "cannot connect to database" problem step by step
# Step 1: Is the host reachable at Layer 3?
ping -c 3 db.internal

# Step 2: Is port 5432 open?
nc -zv db.internal 5432

# Step 3: If nc fails, check the route
traceroute db.internal

# Step 4: If traceroute succeeds, check firewall on the DB server
ssh db.internal "ss -tlnp | grep 5432"
ssh db.internal "iptables -L INPUT -v | grep 5432"

# Step 5: If port is open but connection is refused, check DB config
ssh db.internal "grep -E 'listen_addresses|pg_hba' /etc/postgresql/*/main/postgresql.conf"
```

---

## Common Pitfalls

**Diagnosing from the wrong side:** Network problems are asymmetric. "I can't reach the server" might be a problem on your end, the server's end, or in the middle. Always test from both sides if possible.

**Confusing packet loss at intermediate hops:** In MTR output, `***` or high loss at hop N but zero loss at hop N+1 means hop N deprioritizes ICMP; the path is actually fine. Only interpret loss as real if it persists at that hop AND all subsequent hops.

**Capturing without filters in production:** A full packet capture on a busy production interface can overwhelm the system and capture sensitive data. Always use BPF filters to limit to relevant traffic. Never capture to disk without a size/time limit.

---

## Cross-Links

- [[networks/modules/01_introduction]] — ping, traceroute first introduced here
- [[networks/modules/04_transport-layer]] — TCP state machine; Wireshark can show TCP handshakes and retransmissions
- [[networks/modules/08_network-security]] — nmap is also a security tool; port scanning without permission may be illegal
- [[networks/modules/12_capstone-project]] — the troubleshooting runbook in the capstone uses all tools from this module
- [[networks#latency]] — latency glossary entry
- [[devops-platform-engineering]] — cloud network troubleshooting: VPC flow logs, CloudWatch, Route 53 health checks

---

## Summary

- Start troubleshooting at Layer 1 and work upward: Physical → Data Link → Network → Transport → Application
- The five most common problems: no connectivity, wrong IP/routing, DNS failure, firewall block, MTU mismatch
- tcpdump: capture to pcap; use BPF filters; essential for seeing exactly what's on the wire
- Wireshark: GUI analysis of pcap files; display filters; follow TCP stream; TLS decryption with session key log
- nmap: host discovery (`-sn`), port scanning (`-sS`), service detection (`-sV`)
- MTR: persistent traceroute with loss statistics; loss at intermediate hop only = ICMP filtering (not a real problem)
- iperf3: TCP/UDP throughput measurement; identifies bandwidth bottlenecks
- MTU mismatch: `ping -M do -s 1472`; small packets work, large fail = MTU problem
