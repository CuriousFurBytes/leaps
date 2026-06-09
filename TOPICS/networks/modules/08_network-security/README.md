# Module 08: Network Security

[← Previous](../07_wireless-networking/) | [Topic Home](../../README.md) | [Next →](../09_sdn-and-cloud-networking/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
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

Network security is the practice of protecting network infrastructure and the data it carries from unauthorized access, disruption, and manipulation. This module covers firewalls (stateless and stateful), intrusion detection and prevention systems (IDS/IPS), VPN technologies (IPsec, OpenVPN, WireGuard), and the most important network-layer attacks: IP spoofing, ARP poisoning, DNS hijacking, BGP hijacking, and DDoS attacks.

This module is closely related to [[pentesting-security]]; the focus here is on defensive design and understanding attack mechanics at the network level.

---

## Prerequisites

- Module 03: IP Networking — IP addressing, routing
- Module 04: Transport Layer — TCP/UDP and ports
- Module 05: Application Layer — DNS, HTTP, TLS
- Module 06: Routing Protocols — BGP (for BGP hijacking context)

---

## Objectives

By the end of this module, you will be able to:

1. Explain the difference between stateless and stateful firewalls and write basic iptables/nftables rules
2. Describe how IDS (signature-based and anomaly-based) and IPS differ and where they are deployed
3. Explain how IPsec works (AH vs. ESP, transport vs. tunnel mode, IKE key exchange)
4. Configure and explain WireGuard — its advantages over IPsec and OpenVPN
5. Identify and explain: IP spoofing, ARP poisoning, DNS hijacking, BGP hijacking, SYN flood, and DDoS
6. Apply defense-in-depth: which controls belong at each network layer

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### Firewalls

A firewall controls which network traffic is allowed to pass based on defined rules.

**Stateless firewall:** Examines each packet in isolation — matches rules based on IP addresses, ports, and protocol. Fast but cannot distinguish replies from unsolicited traffic.

**Stateful firewall:** Tracks connection state (SYN, ESTABLISHED, FIN). Knows whether a packet is part of an established connection or a new, unsolicited inbound connection. Can allow "ESTABLISHED,RELATED" inbound traffic (reply to outbound connections) without opening ports for unsolicited inbound.

```bash
# iptables: basic stateful firewall on Linux
# Allow established/related inbound (stateful rule)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow new inbound SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -j ACCEPT

# Allow new inbound HTTPS
iptables -A INPUT -p tcp --dport 443 -m state --state NEW -j ACCEPT

# Default deny all other inbound
iptables -A INPUT -j DROP

# Allow all outbound (stateful replies handled by ESTABLISHED rule above)
iptables -A OUTPUT -j ACCEPT
```

### VPN Technologies

**IPsec:**
- Authentication Header (AH): integrity and authentication; no encryption
- Encapsulating Security Payload (ESP): encryption + integrity
- Transport mode: encrypts payload only (end-to-end between hosts)
- Tunnel mode: encrypts entire IP packet (site-to-site VPN); new IP header wraps the original
- IKE (Internet Key Exchange): automates key negotiation; IKEv2 is the modern standard

**OpenVPN:**
- Uses TLS for key exchange and control; AES for data
- Runs over UDP or TCP; good firewall traversal (can use port 443)
- Mature, widely deployed; higher CPU overhead than WireGuard

**WireGuard:**
- Modern, minimal design (~4000 lines of code vs ~70,000 for IPsec)
- Uses fixed, modern cryptography: ChaCha20, Poly1305, Curve25519, BLAKE2s
- Kernel-level implementation in Linux; significantly faster than OpenVPN
- No dynamic key negotiation complexity; simple public-key configuration

```python
# WireGuard configuration is key-based — no certificates
# Generate a key pair
import subprocess

private_key = subprocess.run(
    ['wg', 'genkey'], capture_output=True, text=True
).stdout.strip()

public_key = subprocess.run(
    ['wg', 'pubkey'], input=private_key,
    capture_output=True, text=True
).stdout.strip()

print(f"Private: {private_key}")
print(f"Public:  {public_key}")
```

### Common Network Attacks

**IP Spoofing:** Sending packets with a forged source IP. Used in reflection/amplification DDoS attacks. Mitigated by BCP38 (ingress filtering — ISPs should drop packets with source IPs outside their allocated space).

**ARP Poisoning:** Sending fake ARP replies to associate the attacker's MAC with a legitimate IP (e.g., the gateway). Traffic for that IP is redirected to the attacker (man-in-the-middle). Mitigated by Dynamic ARP Inspection (DAI) on switches, static ARP entries, or using IPv6 with SEND.

**DNS Hijacking:** Redirecting DNS queries to a malicious resolver, or poisoning a resolver's cache (DNS cache poisoning). Mitigated by DNSSEC (authenticates DNS responses), DoH/DoT (encrypts DNS traffic).

**BGP Hijacking:** An AS announces prefixes it doesn't own; traffic for those prefixes is attracted to the hijacker. Example: YouTube route hijack by Pakistan Telecom (2008). Mitigated by RPKI (cryptographic prefix ownership validation) and route filtering.

**SYN Flood:** Attacker sends many TCP SYN packets with spoofed source IPs; server allocates resources for each half-open connection. Mitigated by SYN cookies (don't allocate state until ACK is received).

**DDoS:** Distributed Denial of Service; use a botnet or amplification to overwhelm a target with traffic. Defense: upstream scrubbing (Cloudflare/Akamai), anycast absorption, rate limiting, BCP38.

---

## Key Concepts

**Defense in depth** — Multiple security layers; no single point of failure. Network, host, application, and data-layer controls all work together.

**Zero trust** — Never trust, always verify; the network location of a device is not sufficient basis for granting access. VPNs are being replaced by zero-trust models (e.g., Google BeyondCorp).

**DMZ** — Demilitarized Zone; a network segment containing public-facing servers, isolated from internal networks by firewalls. See Module 12 capstone.

**IDS/IPS** — Intrusion Detection/Prevention System. IDS alerts on suspicious traffic; IPS also blocks it. Can be signature-based (known attack patterns) or anomaly-based (deviation from baseline).

**DNSSEC** — DNS Security Extensions; adds cryptographic signatures to DNS records, allowing resolvers to verify authenticity.

**RPKI** — Resource Public Key Infrastructure; a cryptographic framework validating that an AS is authorized to advertise a given IP prefix.

---

## Examples

```bash
# Show active iptables rules
iptables -L -v -n --line-numbers

# Test firewall rules with nmap
nmap -sS -p 22,80,443 your_server_ip

# Inspect TLS certificate for HSTS and other security headers
curl -I https://example.com | grep -i strict-transport-security

# Check DNS resolution with validation
dig +dnssec example.com
```

```python
# Simple Python port scanner to test firewall rules
import socket
import concurrent.futures

def check_port(host, port, timeout=0.5):
    """Returns True if port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

host = '192.168.1.1'
ports_to_check = [22, 80, 443, 3306, 8080]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check_port, host, port): port for port in ports_to_check}
    for future in concurrent.futures.as_completed(futures):
        port = futures[future]
        status = "OPEN" if future.result() else "closed"
        print(f"Port {port}: {status}")
```

---

## Common Pitfalls

**Relying on NAT for security:** NAT provides a degree of isolation (external hosts can't initiate connections to internal hosts), but it is not a firewall. Explicitly configure firewall rules; don't rely on NAT's side effects.

**Default-allow firewall posture:** New firewall deployments should start with default-deny and explicitly allow what's needed — not default-allow with specific denies. Forgotten rules in default-deny are harmless; forgotten rules in default-allow create security holes.

**Treating VPN as security:** A VPN provides encryption in transit, but if the VPN endpoint is compromised, all traffic is exposed. VPN is not a substitute for encryption at the application layer (TLS) or for proper access control.

---

## Cross-Links

- [[networks/modules/05_application-layer]] — TLS, DNSSEC, HTTPS prerequisite knowledge
- [[networks/modules/06_routing-protocols]] — BGP hijacking context
- [[networks/modules/12_capstone-project]] — the capstone requires designing a secure multi-tier network with firewall rules
- [[pentesting-security]] — the offensive perspective on network attacks covered here
- [[devops-platform-engineering]] — security groups, NACLs, and WAFs in cloud environments

---

## Summary

- Stateless firewalls match packets by IP/port/protocol; stateful firewalls track connection state and distinguish replies from unsolicited inbound
- iptables/nftables rules: default-deny INPUT with explicit ACCEPT for ESTABLISHED,RELATED and specific services
- IPsec: AH (integrity), ESP (encryption); transport mode (host-to-host), tunnel mode (site-to-site); IKEv2 for key exchange
- WireGuard: modern VPN; minimal codebase; kernel integration; ChaCha20/Poly1305 cryptography; faster and simpler than IPsec
- Key attacks: IP spoofing (BCP38 mitigates), ARP poisoning (DAI mitigates), DNS hijacking (DNSSEC/DoH mitigates), BGP hijacking (RPKI mitigates), SYN flood (SYN cookies mitigate)
- Defense in depth: layer controls at network (firewall, IPS), transport (TLS), application (WAF), and data (encryption at rest)
