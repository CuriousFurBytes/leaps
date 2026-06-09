# Module 02: Physical and Data Link Layers

[← Previous](../01_introduction/) | [Topic Home](../../README.md) | [Next →](../03_ip-networking/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-blue)
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

This module covers Layers 1 and 2 of the OSI model — the foundation on which all higher-layer protocols rest. You will learn how physical signals encode bits, how Ethernet frames structure data for local delivery, how MAC addresses identify devices on a segment, and how the Address Resolution Protocol (ARP) bridges Layer 3 IP addresses to Layer 2 MAC addresses. We also cover how switches build and use MAC address tables, the Spanning Tree Protocol (STP) that prevents switching loops, VLANs for logical network segmentation, and the basics of Wi-Fi (802.11).

Understanding Layer 2 is essential for diagnosing a large class of networking problems — ARP cache poisoning, duplicate MAC addresses, switching loops, and VLAN misconfiguration are all Layer 2 issues that manifest as mysterious connectivity failures.

---

## Prerequisites

- Module 01: Introduction to Computer Networks — OSI model, encapsulation, and the difference between frames, packets, and segments

---

## Objectives

By the end of this module, you will be able to:

1. Describe how Ethernet encodes data in frames including the preamble, MAC addresses, EtherType, payload, and FCS fields
2. Explain what a MAC address is, how it is structured (OUI + device ID), and why it is locally significant only
3. Trace a complete ARP exchange — from ARP Request broadcast to ARP Reply to ARP cache entry
4. Explain how a switch builds its MAC address table and how it handles unknown, known, and broadcast destinations
5. Describe the Spanning Tree Protocol and why it is necessary to prevent switching loops
6. Configure and explain VLANs for logical network segmentation
7. Explain the key differences between 802.11 (Wi-Fi) and Ethernet at the data link layer, including CSMA/CA vs. CSMA/CD

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.
> The objectives above define what you need to learn. Use the resources in RESOURCES.md
> and the key concepts below as a guide.

### Ethernet Frames

Ethernet (IEEE 802.3) is the dominant Layer 2 protocol for wired LANs. An Ethernet frame has the following structure:

| Field | Size | Purpose |
|-------|------|---------|
| Preamble | 7 bytes | Synchronization pattern (10101010 repeated) |
| Start Frame Delimiter | 1 byte | Marks start of frame (10101011) |
| Destination MAC | 6 bytes | Target device's hardware address |
| Source MAC | 6 bytes | Sending device's hardware address |
| EtherType / Length | 2 bytes | Protocol of payload (0x0800=IPv4, 0x0806=ARP, 0x86DD=IPv6) |
| Payload | 46–1500 bytes | The encapsulated IP packet (or other Layer 3 PDU) |
| FCS | 4 bytes | CRC32 checksum for error detection |

The minimum frame size is 64 bytes; the maximum is 1518 bytes (payload = 1500 bytes = MTU). Frames smaller than 64 bytes are "runt" frames and indicate a collision or malformed transmission.

### MAC Addresses

A MAC (Media Access Control) address is a 48-bit (6-byte) hardware address assigned to a network interface. Written in colon-separated hexadecimal: `aa:bb:cc:dd:ee:ff`.

The first 3 bytes are the OUI (Organizationally Unique Identifier) assigned to the manufacturer. The last 3 bytes are assigned by the manufacturer to be unique for each device. The first bit (LSB of first byte) indicates unicast (0) vs. multicast (1). The second bit indicates globally administered (0) vs. locally administered (1).

MAC addresses are **locally significant** — they are used to address devices within a single network segment. Routers discard and recreate frames at each hop; MAC addresses do not travel across router boundaries.

### ARP — Address Resolution Protocol

IP addresses are used to route packets across the internet, but within a local subnet, delivery requires MAC addresses. ARP (RFC 826) is the protocol that maps an IP address to a MAC address.

**ARP Request (broadcast):**
```
Sender: "Who has IP 192.168.1.1? Tell 192.168.1.5 (MAC: aa:bb:cc:dd:ee:01)"
Destination MAC: ff:ff:ff:ff:ff:ff (broadcast — all devices on segment receive this)
```

**ARP Reply (unicast):**
```
Target: "I have 192.168.1.1. My MAC is aa:bb:cc:dd:ee:99"
Sent directly to the requester's MAC address
```

After the exchange, both devices cache the mapping in their ARP table (`arp -n` to view on Linux). ARP cache entries expire after a timeout (typically 20 minutes).

### Switching: MAC Address Tables

A switch builds a MAC address table (also called a CAM table) by examining the source MAC of every incoming frame:

```
Frame arrives on port 3 with source MAC aa:bb:cc:dd:ee:01
→ Switch records: aa:bb:cc:dd:ee:01 is reachable via port 3
```

When forwarding:
- **Known unicast:** forward only to the port associated with the destination MAC
- **Unknown unicast:** flood to all ports except the source port (because the switch hasn't learned the destination yet)
- **Broadcast (ff:ff:ff:ff:ff:ff):** flood to all ports except the source port

### Spanning Tree Protocol (STP)

If you connect switches in a loop (e.g., Switch A ↔ Switch B ↔ Switch C ↔ Switch A), broadcast frames will loop forever, consuming all bandwidth. STP (IEEE 802.1D) prevents this by electing a root bridge and blocking redundant ports, creating a loop-free logical topology while maintaining physical redundancy.

Modern networks use RSTP (Rapid Spanning Tree, 802.1w) which converges in seconds rather than minutes. Large networks use MSTP (Multiple Spanning Tree, 802.1s) to run separate spanning trees per VLAN.

### VLANs

A VLAN (Virtual Local Area Network) is a logical grouping of switch ports that forms a separate Layer 2 broadcast domain, regardless of physical location. Traffic between VLANs must pass through a Layer 3 router (or a "Layer 3 switch" that can route between VLANs).

VLANs are identified by a 12-bit VLAN ID (1–4094) in the 802.1Q tag — a 4-byte field inserted between the source MAC and EtherType fields of an Ethernet frame.

### Wi-Fi Basics (802.11)

Wi-Fi uses a shared radio medium, requiring a different access method than wired Ethernet. Key differences:

- **CSMA/CA** (Collision Avoidance) instead of CSMA/CD (Collision Detection) — because you cannot detect collisions while transmitting on a radio channel
- **ACK for every frame** — since the radio medium is lossy, the receiver explicitly acknowledges every frame
- **Hidden node problem** — two stations may both be in range of the AP but not of each other, causing collisions at the AP that neither sender can detect

```python
# Example: checking your Wi-Fi channel and signal strength on Linux
import subprocess

result = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
print(result.stdout)
# Look for: Frequency, Bit Rate, Signal level
```

---

## Key Concepts

**Ethernet Frame** — The Layer 2 PDU; wraps an IP packet with source/destination MAC addresses and a FCS checksum. Maximum payload size (MTU) is 1500 bytes for standard Ethernet. See [[networks#frame]].

**MAC Address** — A 48-bit hardware address unique to a network interface within a local segment. The first 3 bytes identify the manufacturer (OUI). See [[networks#mac-address]].

**ARP** — Address Resolution Protocol; maps IPv4 addresses to MAC addresses within a local subnet. Operates via broadcast request + unicast reply. Vulnerable to ARP spoofing.

**CAM Table** — The MAC address table a switch maintains; maps MAC addresses to switch ports. Learned dynamically from frame source addresses.

**STP / RSTP** — Spanning Tree Protocol / Rapid Spanning Tree; prevents Layer 2 loops by blocking redundant switch ports. RSTP (802.1w) is the modern standard.

**VLAN** — Virtual LAN; a logical broadcast domain created by tagging frames with an 802.1Q VLAN ID. Separates traffic on shared switch infrastructure.

**CSMA/CA** — Carrier Sense Multiple Access / Collision Avoidance; the access method used by Wi-Fi. Nodes sense the channel and back off randomly before transmitting to reduce collisions.

**MTU** — Maximum Transmission Unit; the largest payload size a Layer 2 frame can carry. Standard Ethernet MTU is 1500 bytes. If an IP packet exceeds the MTU, it must be fragmented (at Layer 3) or the sending TCP stack must use a smaller segment size.

---

## Examples

### Example 1: Reading an ARP Table

```bash
# View the ARP cache on Linux
arp -n
# or
ip neigh show

# Example output:
# 192.168.1.1   dev eth0  lladdr aa:bb:cc:dd:ee:99  REACHABLE
# 192.168.1.10  dev eth0  lladdr 11:22:33:44:55:66  STALE
```

The ARP cache shows which IP addresses have been resolved to MAC addresses recently. "REACHABLE" means the entry was confirmed recently; "STALE" means it hasn't been confirmed but hasn't expired.

### Example 2: Sending an ARP Probe with Python (Scapy)

```python
# Requires: pip install scapy
# Must be run as root/administrator

from scapy.all import ARP, Ether, srp

# Craft an ARP request for a target IP
target_ip = "192.168.1.1"
arp_request = ARP(pdst=target_ip)
broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")  # broadcast frame
packet = broadcast / arp_request  # stack Ethernet over ARP

# Send and receive responses (timeout=1 second)
result = srp(packet, timeout=1, verbose=False)
answered = result[0]

for sent, received in answered:
    print(f"IP: {received.psrc}  MAC: {received.hwsrc}")
```

### Example 3: Inspecting a VLAN Tag

```python
# Scapy: craft and inspect a dot1q (802.1Q) tagged frame
from scapy.all import Ether, Dot1Q, IP, ICMP, hexdump

# Create a tagged frame: VLAN 100
frame = Ether() / Dot1Q(vlan=100) / IP(dst="10.0.0.1") / ICMP()
hexdump(frame)

# The 802.1Q tag appears as 4 bytes between source MAC and EtherType
# Byte pattern: 0x81 0x00 (TPID) + 2 bytes containing priority + VLAN ID
```

---

## Common Pitfalls

**Pitfall 1: Forgetting that ARP is per-subnet**

ARP only works within a single Layer 2 broadcast domain. You cannot ARP for an IP address on a different subnet — that packet will never reach a device on the other subnet. If you try to ping across subnets without a configured default gateway, ARP will try to resolve the remote IP locally and fail.

Wrong: "I'll just ping the server directly without setting a gateway."
Right: Ensure a default gateway is configured; the gateway's MAC will be ARPed instead of the remote server's.

**Pitfall 2: Assuming MAC addresses are globally unique in practice**

MAC addresses are assigned by manufacturers and are supposed to be globally unique, but in practice: VMs often have randomly generated MACs, containers use software MACs, and some devices allow MAC address spoofing. Never design a security system that relies on MAC address uniqueness for authentication.

**Pitfall 3: Forgetting the impact of MTU mismatches**

If one part of the network has an MTU of 1500 bytes and another has 1400 bytes (common with VPNs that add overhead), packets larger than 1400 bytes will either be fragmented or silently dropped (if the DF — Don't Fragment — bit is set). This causes mysterious failures where small packets work but large ones don't.

```bash
# Test MTU by sending large ICMP packets with DF bit set
ping -M do -s 1472 192.168.1.1  # Linux
ping -l 1472 -f 192.168.1.1     # Windows
# If this fails but ping -s 1000 works, you have an MTU mismatch
```

---

## Cross-Links

- [[networks/modules/01_introduction]] — the OSI model and encapsulation concepts that this module builds on
- [[networks/modules/03_ip-networking]] — the Layer 3 (IP) packets that Ethernet frames carry as payload
- [[networks/modules/08_network-security]] — ARP spoofing and VLAN hopping are Layer 2 attacks covered in the security module
- [[pentesting-security]] — ARP poisoning and MAC flooding are classic Layer 2 attack vectors

---

## Summary

- Ethernet frames have: preamble, destination MAC (6 bytes), source MAC (6 bytes), EtherType (2 bytes), payload (up to 1500 bytes), and FCS (4 bytes)
- MAC addresses are 48-bit hardware addresses; the first 3 bytes identify the manufacturer (OUI); they are locally significant only
- ARP resolves IPv4 addresses to MAC addresses via broadcast request + unicast reply; results are cached in the ARP table
- Switches learn MAC-to-port mappings from incoming frames and forward only to the correct port; they flood unknown destinations
- STP/RSTP prevents Layer 2 loops by blocking redundant switch ports
- VLANs create isolated broadcast domains using 802.1Q tags; inter-VLAN routing requires Layer 3
- Wi-Fi uses CSMA/CA (collision avoidance) instead of CSMA/CD, and ACKs every frame due to the lossy radio medium
