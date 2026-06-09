# Module 07: Wireless Networking

[← Previous](../06_routing-protocols/) | [Topic Home](../../README.md) | [Next →](../08_network-security/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-4h-orange)

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

Wireless networking presents unique challenges compared to wired networking: the medium is shared and lossy, signals interfere with each other, and security requires explicit cryptographic protection rather than the physical security of a cable. This module covers the 802.11 Wi-Fi standard family, the access control mechanisms that prevent collisions on a shared medium, and Wi-Fi security protocols (WPA2/WPA3). We also survey cellular networking (LTE/5G) at a conceptual level.

---

## Prerequisites

- Module 02: Physical and Data Link Layers — MAC addresses, CSMA, frames
- Module 08 cross-awareness: Wi-Fi security (WPA2/3) is covered in the context of the security module

---

## Objectives

By the end of this module, you will be able to:

1. Name the 802.11 standard versions (a/b/g/n/ac/ax) and their key characteristics (frequency bands, max theoretical throughput)
2. Explain CSMA/CA and why Wi-Fi uses collision avoidance instead of collision detection
3. Describe the hidden node problem and how RTS/CTS addresses it
4. Explain WPA2 (CCMP/AES) and WPA3 (SAE) and why WPA2 with weak passwords is vulnerable
5. Explain the conceptual difference between 4G LTE and 5G at a high level

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### 802.11 Standards Overview

| Standard | Year | Bands | Max Throughput | Notes |
|----------|------|-------|---------------|-------|
| 802.11b | 1999 | 2.4 GHz | 11 Mbps | First mainstream Wi-Fi |
| 802.11a | 1999 | 5 GHz | 54 Mbps | Less interference; shorter range |
| 802.11g | 2003 | 2.4 GHz | 54 Mbps | Backward-compatible with b |
| 802.11n (Wi-Fi 4) | 2009 | 2.4/5 GHz | 600 Mbps | MIMO antennas; 40 MHz channels |
| 802.11ac (Wi-Fi 5) | 2013 | 5 GHz | 3.5 Gbps | MU-MIMO; 80/160 MHz channels |
| 802.11ax (Wi-Fi 6) | 2019 | 2.4/5 GHz | 9.6 Gbps | OFDMA; improved dense environments |
| 802.11ax (Wi-Fi 6E) | 2021 | 2.4/5/6 GHz | 9.6 Gbps | Adds 6 GHz band; less congestion |

The 2.4 GHz band has longer range but more interference (overlaps with microwaves, Bluetooth). The 5 GHz band is faster but shorter range. The 6 GHz band (Wi-Fi 6E) offers the most capacity with minimal interference.

### CSMA/CA

Wired Ethernet uses CSMA/CD (Collision Detection): transmit; if a collision is detected, stop and back off. Wi-Fi cannot detect collisions while transmitting (because the transmitted signal overwhelms any incoming signal). Instead, Wi-Fi uses CSMA/CA (Collision Avoidance):

1. **Sense the channel:** wait until the medium is idle
2. **Random backoff:** wait a random time interval before transmitting
3. **Transmit:** send the frame
4. **Wait for ACK:** if no ACK received, retransmit

Every unicast Wi-Fi frame requires an ACK from the receiver. This double-check handles the lossy radio medium.

### Hidden Node Problem

Node A and Node C can both reach Node B (the AP), but A and C cannot hear each other. When A transmits to B, C cannot detect the transmission and may also transmit, causing a collision at B.

**Solution — RTS/CTS:**
- A sends RTS (Request to Send) to B
- B broadcasts CTS (Clear to Send) — all nodes within B's range hear this
- C hears the CTS and defers its transmission
- A transmits its data frame

RTS/CTS adds overhead so it is only used for large frames.

### Wi-Fi Security: WPA2 and WPA3

**WPA2 (802.11i):**
- Uses CCMP (Counter Mode with CBC-MAC Protocol) based on AES-128
- Pre-Shared Key (PSK) mode: all clients share the same passphrase
- Vulnerability: offline dictionary attacks against the 4-way handshake; KRACK (Key Reinstallation Attack)

**WPA3:**
- Uses SAE (Simultaneous Authentication of Equals) — replaces PSK with Dragonfly key exchange
- Provides forward secrecy: capturing the 4-way handshake doesn't allow offline brute-force
- WPA3-Enterprise uses 192-bit security suite

```bash
# Check Wi-Fi security mode on Linux
iwconfig wlan0
nmcli dev wifi list

# Scan for available networks and their security
nmcli device wifi list ifname wlan0
```

### Cellular Networking (LTE/5G Overview)

LTE (4G) and 5G are IP-based cellular networks:
- LTE provides download speeds of 10–300 Mbps with typical latency of 30–50ms
- 5G provides peak speeds of 1–10 Gbps with latency under 10ms (in ideal conditions)
- Both use the same TCP/IP stack as Wi-Fi; the radio access network (RAN) is the mobile-specific part
- 5G's "mmWave" frequencies (24–100 GHz) provide massive capacity but require line-of-sight and many small cells

From a networking perspective, a mobile device has an IP address (assigned by the carrier via DHCP-like mechanism) and communicates via TCP/IP just like a wired device.

---

## Key Concepts

**CSMA/CA** — Collision Avoidance access method used by Wi-Fi; senses channel, backs off randomly, waits for ACK.

**SSID** — Service Set Identifier; the network name broadcast by an access point.

**BSSID** — Basic SSID; the MAC address of the access point's radio interface.

**Channel** — A specific frequency range within a Wi-Fi band. 2.4 GHz has 14 channels (only 1, 6, 11 are non-overlapping in 20 MHz mode).

**WPA3-SAE** — Wi-Fi Protected Access 3 with Simultaneous Authentication of Equals; provides forward secrecy and resistance to offline dictionary attacks.

**MU-MIMO** — Multi-User Multiple Input Multiple Output; allows an AP to communicate with multiple clients simultaneously on different spatial streams.

---

## Examples

```python
# Scan for Wi-Fi networks using Python on Linux (requires root)
import subprocess

result = subprocess.run(
    ['iw', 'dev', 'wlan0', 'scan'],
    capture_output=True, text=True
)

# Parse basic info from the scan
for line in result.stdout.splitlines():
    if 'SSID' in line or 'freq' in line or 'signal' in line:
        print(line.strip())
```

```bash
# Channel utilization: see which channels are busy
# Install: sudo apt install iw
iw dev wlan0 scan | grep -E 'SSID|freq|signal|capability'

# Measure Wi-Fi throughput to a known server
iperf3 -c 192.168.1.1 -t 10  # 10-second test to local server
```

---

## Common Pitfalls

**Co-channel interference from overlapping APs:** In a dense environment, two APs on the same channel will interfere with each other. Always use non-overlapping channels (1, 6, 11 for 2.4 GHz; there are more options on 5 GHz).

**WPA2 PSK with weak passphrase:** The 4-way handshake can be captured passively and attacked offline with dictionary attacks. Use a strong, random passphrase of at least 16 characters, or use WPA3.

**Assuming Wi-Fi latency is similar to wired:** Wi-Fi adds variable latency (10–50ms typical, spikes much higher) due to CSMA/CA contention, retransmissions, and power-saving modes. For latency-sensitive applications, wired Ethernet is significantly more predictable.

---

## Cross-Links

- [[networks/modules/02_physical-and-datalink]] — CSMA/CD (wired) vs CSMA/CA (wireless); MAC addresses and frames
- [[networks/modules/08_network-security]] — WPA3, wireless attacks, rogue APs
- [[pentesting-security]] — Wi-Fi attacks (deauthentication, evil twin, KRACK) are covered in security

---

## Summary

- 802.11 standard evolution: b/g → n (Wi-Fi 4, MIMO) → ac (Wi-Fi 5, MU-MIMO, 5 GHz) → ax (Wi-Fi 6, OFDMA, 6 GHz option)
- CSMA/CA: sense channel → random backoff → transmit → wait for ACK; every unicast frame is acknowledged
- Hidden node problem: RTS/CTS solves collisions at the AP when senders can't hear each other
- WPA2 uses CCMP/AES; vulnerable to offline dictionary attacks; WPA3 with SAE provides forward secrecy
- Use non-overlapping channels (1/6/11 on 2.4 GHz) to minimize interference in dense environments
- LTE and 5G are IP networks; devices use TCP/IP transparently; 5G adds lower latency and higher capacity
