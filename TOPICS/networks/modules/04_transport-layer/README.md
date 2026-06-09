# Module 04: Transport Layer

[← Previous](../03_ip-networking/) | [Topic Home](../../README.md) | [Next →](../05_application-layer/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-blue)
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

The transport layer (OSI Layer 4) provides end-to-end communication services for applications. This module covers TCP — the protocol that delivers the internet's reliability guarantee — in depth: the 3-way handshake, flow control, congestion control, connection states, and failure modes. We also cover UDP, its tradeoffs, and when to choose each protocol.

Understanding TCP deeply is one of the highest-leverage investments you can make as an engineer. TCP problems — head-of-line blocking, TIME_WAIT exhaustion, retransmission storms, congestion collapse — cause a large fraction of production network incidents.

---

## Prerequisites

- Module 01: Introduction — OSI model, encapsulation, ports
- Module 03: IP Networking — IP addressing and packet delivery

---

## Objectives

By the end of this module, you will be able to:

1. Describe the TCP 3-way handshake (SYN, SYN-ACK, ACK) and explain what each step achieves
2. Explain TCP's reliability mechanisms: sequence numbers, acknowledgments, and retransmission
3. Describe flow control (receiver window) and congestion control (slow start, congestion avoidance, fast retransmit)
4. List the TCP connection states (CLOSED, LISTEN, SYN_SENT, ESTABLISHED, TIME_WAIT, etc.) and describe the transitions
5. Explain when to use UDP instead of TCP and what you give up
6. Identify TCP pathologies: head-of-line blocking, TIME_WAIT exhaustion, retransmission timeout

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### TCP: The 3-Way Handshake

TCP establishes a connection before any application data is exchanged. The handshake synchronizes sequence numbers between the two sides:

```
Client                    Server
  │──── SYN (seq=x) ──────►│   Client picks initial sequence number x
  │◄── SYN-ACK (seq=y, ack=x+1) ──│   Server picks y, acknowledges x
  │──── ACK (ack=y+1) ────►│   Client acknowledges y
  │        ESTABLISHED     │
```

Why three messages (not two)? Both sides need to: (1) send their initial sequence number, and (2) confirm they received the other side's sequence number. Two messages cannot accomplish both goals simultaneously.

### TCP Reliability

TCP guarantees delivery through:
- **Sequence numbers:** every byte of data has a sequence number; receiver can detect missing bytes
- **Acknowledgments:** receiver sends ACK = next byte it expects; sender retransmits unACKed data after timeout
- **Retransmission:** if an ACK isn't received within the RTO (Retransmission Timeout), the segment is resent

```python
# Observing TCP retransmissions with ss
import subprocess

# Show TCP connections with detailed retransmission stats
result = subprocess.run(
    ['ss', '-ti', 'dst', '10.0.0.1'],  # TCP info for connections to 10.0.0.1
    capture_output=True, text=True
)
print(result.stdout)
# Look for: retrans, cwnd (congestion window), rtt
```

### Flow Control

The receiver tells the sender how much buffer space it has (the "receive window"). The sender must not transmit more data than the window allows. This prevents a fast sender from overwhelming a slow receiver.

### Congestion Control

TCP infers network congestion from packet loss and adapts its send rate:

1. **Slow Start:** begin with 1 MSS (Maximum Segment Size); double every RTT until threshold
2. **Congestion Avoidance:** after threshold, increase by 1 MSS per RTT (linear)
3. **Fast Retransmit:** 3 duplicate ACKs → retransmit without waiting for RTO
4. **Fast Recovery:** after fast retransmit, halve window (multiplicative decrease), continue from there

This is TCP Reno. Modern TCP uses CUBIC (Linux default) or BBR (Google's algorithm) for better performance on high-bandwidth-delay-product paths.

### TCP Connection States

```
CLOSED
  │ (passive open: listen())
  ▼
LISTEN ──(SYN received)──► SYN_RCVD ──(ACK received)──► ESTABLISHED
  │ (active open: connect())                                    │
  ▼                                                             │ (close())
SYN_SENT ──(SYN-ACK received)──────────────────────► FIN_WAIT_1
                                                           │
                                                      FIN_WAIT_2
                                                           │
                                                      TIME_WAIT ──(2×MSL)──► CLOSED
```

**TIME_WAIT:** After the active closer sends its final ACK, it waits 2×MSL (Maximum Segment Lifetime, typically 60s) before closing. This ensures the final ACK was received and prevents old duplicate packets from being accepted by a new connection on the same port.

### UDP

UDP is connectionless and unreliable. It simply sends a datagram with source/destination port and length. No handshake, no acknowledgment, no retransmission, no ordering.

```python
# Simple UDP sender
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# No connect() needed for UDP — just sendto()
sock.sendto(b"Hello, UDP!", ('192.168.1.10', 9000))
sock.close()
```

UDP is preferred for: DNS (single request-response), NTP, VoIP/video (where retransmission would be too late), and games (where a lost frame is less bad than a late one).

---

## Key Concepts

**TCP** — Connection-oriented, reliable, ordered byte-stream transport. See [[networks#tcp]].

**UDP** — Connectionless, unreliable, unordered datagram transport. See [[networks#udp]].

**Port** — 16-bit identifier for a service endpoint. See [[networks#port]].

**Sequence number** — TCP uses sequence numbers to order bytes and detect missing data; initial sequence number (ISN) is random for security.

**RTT (Round-Trip Time)** — The time for a packet to travel to the destination and back; TCP uses RTT to set its retransmission timeout.

**Congestion window (cwnd)** — TCP's estimate of how much data the network can handle; adjusted based on loss signals.

**TIME_WAIT** — Post-close state lasting 2×MSL; prevents port reuse issues and old packets from being misdelivered.

**Head-of-line blocking** — When a lost packet blocks delivery of all subsequent packets in the stream (even those already received). A fundamental limitation of TCP for multiplexed streams; addressed by QUIC/HTTP3.

---

## Examples

```python
# TCP server example: accept one connection and echo data
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoid TIME_WAIT binding issues
server.bind(('0.0.0.0', 9000))
server.listen(5)

print("Waiting for connection...")
conn, addr = server.accept()
print(f"Connected from {addr}")

while True:
    data = conn.recv(1024)  # recv up to 1024 bytes
    if not data:
        break  # client closed connection
    conn.sendall(data)  # echo it back

conn.close()
server.close()
```

```python
# TCP client: connect and send data
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9000))

# TCP is a byte stream — must handle partial sends and reads
message = b"Hello, TCP!"
client.sendall(message)  # sendall() retries until all bytes sent

# recv() may return less than requested — loop until you have all your data
received = b""
while len(received) < len(message):
    chunk = client.recv(1024)
    if not chunk:
        break
    received += chunk

print(f"Received: {received}")
client.close()
```

---

## Common Pitfalls

**Assuming one send() = one recv():** TCP is a byte stream, not a message protocol. `send("hello")` on one side does not guarantee `recv()` returns exactly `"hello"`. Always implement message framing (length prefix or delimiter).

**Not setting SO_REUSEADDR on servers:** Without `SO_REUSEADDR`, a restarted server may fail to bind to its port for up to 2 minutes due to TIME_WAIT sockets from the previous run.

**Using UDP when you need reliability:** UDP is faster, but if your application needs all messages delivered in order, you either need TCP or you need to implement reliability yourself. Implementing reliability correctly in UDP is much harder than it sounds.

---

## Cross-Links

- [[networks/modules/03_ip-networking]] — IP addressing; TCP segments are carried in IP packets
- [[networks/modules/05_application-layer]] — HTTP, TLS, and DNS all run on top of TCP or UDP
- [[networks/modules/10_network-programming]] — Python socket programming for TCP and UDP
- [[networks#tcp]] — TCP glossary entry
- [[networks#udp]] — UDP glossary entry

---

## Summary

- TCP is connection-oriented; the 3-way handshake (SYN/SYN-ACK/ACK) establishes synchronized sequence numbers
- TCP guarantees reliability via: sequence numbers, acknowledgments, and retransmission on timeout
- Flow control: receiver window limits how much the sender can transmit; prevents buffer overflow
- Congestion control: slow start → congestion avoidance → fast retransmit; TCP self-throttles based on loss signals
- TCP connection states: LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT, TIME_WAIT, CLOSED
- TIME_WAIT: active closer waits 2×MSL after final ACK; `SO_REUSEADDR` bypasses for server restarts
- UDP: connectionless, unreliable, unordered; no handshake overhead; used for DNS, NTP, VoIP, gaming
- Choose TCP for: reliable ordered delivery (HTTP, SSH, databases); choose UDP for: latency-sensitive or single-packet exchanges
