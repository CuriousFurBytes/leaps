# Module 10: Network Programming

[← Previous](../09_sdn-and-cloud-networking/) | [Topic Home](../../README.md) | [Next →](../11_troubleshooting-and-tools/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-7h-orange)

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

This module teaches you to write network programs using Python's BSD socket API. You will implement TCP and UDP clients and servers, learn how the socket API maps to the underlying TCP/IP concepts from earlier modules, explore raw sockets, and use Scapy for packet crafting and network analysis. This is the "show your work" module — everything abstract becomes concrete when you implement it.

---

## Prerequisites

- Module 04: Transport Layer — TCP, UDP, ports, connection lifecycle
- Module 05: Application Layer — HTTP/DNS concepts you'll implement manually
- Basic Python programming (functions, classes, exception handling)

---

## Objectives

By the end of this module, you will be able to:

1. Write a TCP echo server that handles multiple concurrent clients using threading
2. Write a TCP client that correctly handles partial reads and maintains message framing
3. Write a UDP client and server and explain the differences from TCP socket programming
4. Use `select()` or `selectors` for non-blocking I/O with multiple sockets
5. Use Scapy to craft custom packets and analyze pcap files programmatically
6. Implement a simple application protocol (length-prefixed messages over TCP)

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### The BSD Socket API

The BSD socket API, introduced in 4.2BSD Unix (1983), is the universal interface for network programming. It's available in virtually every language and operating system. Key system calls:

| Function | Purpose |
|----------|---------|
| `socket()` | Create a new socket (specify family, type, protocol) |
| `bind()` | Associate socket with a local address:port |
| `listen()` | Mark socket as passive (server); set backlog queue size |
| `accept()` | Accept incoming connection; returns new socket |
| `connect()` | Initiate a connection to a remote address (client) |
| `send()` / `sendall()` | Send data (sendall retries until all sent) |
| `recv()` | Receive data (may return less than requested) |
| `close()` | Close socket; initiates TCP FIN sequence |

### TCP Server Pattern

```python
import socket
import threading

def handle_client(conn, addr):
    """Handle a single client connection in its own thread."""
    print(f"New connection from {addr}")
    try:
        while True:
            # TCP is a byte stream — recv() may return partial data
            data = conn.recv(4096)
            if not data:
                break  # client closed connection (received FIN)
            print(f"Received {len(data)} bytes from {addr}")
            conn.sendall(data)  # echo back; sendall handles partial sends
    except ConnectionResetError:
        pass  # client disconnected abruptly
    finally:
        conn.close()
        print(f"Connection from {addr} closed")

def run_server(host='0.0.0.0', port=9000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR: allow rebinding immediately after server restart
    # (bypasses TIME_WAIT for bound address)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(10)  # backlog: up to 10 pending connections
    print(f"Listening on {host}:{port}")

    while True:
        conn, addr = server.accept()  # blocks until client connects
        # Spawn a new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
```

### Message Framing Over TCP

TCP is a byte stream — it has no concept of message boundaries. `send("hello")` followed by `send("world")` might be received as `recv("helloworld")` or `recv("hell")` + `recv("oworld")`. You must implement message framing:

```python
import struct

def send_message(sock, message: bytes):
    """Send a length-prefixed message."""
    # Pack the length as a 4-byte big-endian integer, then send length + data
    length = struct.pack('>I', len(message))
    sock.sendall(length + message)

def recv_message(sock) -> bytes:
    """Receive a length-prefixed message."""
    # First, read exactly 4 bytes for the length
    length_bytes = recv_exactly(sock, 4)
    if not length_bytes:
        return b''
    length = struct.unpack('>I', length_bytes)[0]
    # Then read exactly `length` bytes for the payload
    return recv_exactly(sock, length)

def recv_exactly(sock, n: int) -> bytes:
    """Receive exactly n bytes from sock."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return b''  # connection closed
        data += chunk
    return data
```

### UDP Socket Programming

UDP sockets use `sendto()` and `recvfrom()` — no connection, no state:

```python
import socket

# UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 9001))

while True:
    data, addr = server.recvfrom(65535)  # max UDP datagram size
    print(f"Received {len(data)} bytes from {addr}: {data.decode()}")
    server.sendto(b"ACK", addr)  # reply to sender

# UDP client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello UDP", ('127.0.0.1', 9001))
response, addr = client.recvfrom(1024)
print(f"Response: {response}")
client.close()
```

### Non-Blocking I/O with selectors

Using threads for each connection doesn't scale to thousands of connections. The `selectors` module provides `select()`-based I/O multiplexing:

```python
import selectors
import socket

sel = selectors.DefaultSelector()

def accept_connection(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=recv_data)

def recv_data(conn):
    data = conn.recv(1024)
    if data:
        conn.sendall(data)  # echo
    else:
        sel.unregister(conn)
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9000))
server.listen(10)
server.setblocking(False)
sel.register(server, selectors.EVENT_READ, data=accept_connection)

while True:
    events = sel.select(timeout=None)  # blocks until a socket is ready
    for key, mask in events:
        callback = key.data
        callback(key.fileobj)
```

### Scapy for Packet Crafting

Scapy allows constructing arbitrary packets at any layer:

```python
from scapy.all import IP, TCP, ICMP, send, sr1, rdpcap

# Craft and send an ICMP ping
response = sr1(IP(dst="8.8.8.8") / ICMP(), timeout=2, verbose=False)
if response:
    print(f"RTT: {response.time - response.sent_time:.3f}s")

# Craft a TCP SYN packet
syn = IP(dst="192.168.1.1") / TCP(dport=80, flags="S", sport=12345)
syn_ack = sr1(syn, timeout=2, verbose=False)
if syn_ack and syn_ack[TCP].flags == "SA":
    print("Port 80 is OPEN (received SYN-ACK)")

# Analyze a pcap file
packets = rdpcap("capture.pcap")
for pkt in packets:
    if IP in pkt:
        print(f"{pkt[IP].src} → {pkt[IP].dst}")
```

---

## Key Concepts

**Socket** — OS abstraction for a network endpoint; identified by (protocol, local IP, local port, remote IP, remote port). See [[networks#socket]].

**Blocking vs. non-blocking I/O** — Blocking sockets wait until data is available; non-blocking return immediately with EAGAIN. I/O multiplexing (`select`, `poll`, `epoll`) enables efficient non-blocking handling of many connections.

**Message framing** — Application-level protocol to delimit messages in a byte stream. Common approaches: length prefix (4-byte big-endian int + payload), delimiter (\r\n for HTTP/SMTP), or fixed-size messages.

**Backlog** — The queue of pending connections waiting to be `accept()`ed by the server. If full, new connection attempts are rejected with RST.

**sendall() vs send()** — `send()` may send only part of the data; `sendall()` loops internally until all bytes are sent or an error occurs. Always use `sendall()` for TCP.

---

## Examples

```python
# Complete TCP client with message framing and timeout
import socket
import struct
import contextlib

def create_connection(host, port, timeout=10):
    """Create a TCP connection with timeout."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        return sock
    except (socket.timeout, ConnectionRefusedError) as e:
        sock.close()
        raise ConnectionError(f"Cannot connect to {host}:{port}: {e}")

def send_and_receive(host, port, message: str) -> str:
    """Send a framed message and receive a framed response."""
    msg_bytes = message.encode('utf-8')
    with create_connection(host, port) as sock:
        # Send: 4-byte length prefix + payload
        sock.sendall(struct.pack('>I', len(msg_bytes)) + msg_bytes)
        # Receive: 4-byte length prefix
        length_bytes = b''
        while len(length_bytes) < 4:
            chunk = sock.recv(4 - len(length_bytes))
            if not chunk:
                raise ConnectionError("Connection closed while reading length")
            length_bytes += chunk
        length = struct.unpack('>I', length_bytes)[0]
        # Receive: payload
        payload = b''
        while len(payload) < length:
            chunk = sock.recv(length - len(payload))
            if not chunk:
                raise ConnectionError("Connection closed while reading payload")
            payload += chunk
        return payload.decode('utf-8')
```

---

## Common Pitfalls

**Not using sendall():** `send()` can return a smaller value than the requested bytes. If you send 1000 bytes and `send()` returns 600, you need to send the remaining 400. `sendall()` handles this loop for you.

**Assuming recv() returns exactly what send() sent:** TCP is a stream. A single `send("hello world")` might result in `recv("hello ")` and another `recv("world")`. Implement message framing.

**Forgetting to set socket timeout:** A socket with no timeout can block forever. Always set a timeout for client connections. For servers, use non-blocking I/O or per-connection threads with timeouts.

**Not closing sockets properly:** Unclosed sockets leak file descriptors. Use `with` statements or `try/finally` to ensure sockets are always closed.

---

## Cross-Links

- [[networks/modules/04_transport-layer]] — TCP and UDP semantics that the socket API exposes
- [[networks/modules/05_application-layer]] — HTTP and DNS implemented at the socket level
- [[networks/modules/11_troubleshooting-and-tools]] — tools that inspect the packets your programs generate
- [[networks#socket]] — socket glossary entry

---

## Summary

- The BSD socket API maps directly to TCP/IP: `socket()` → `bind()` → `listen()` → `accept()` (server); `socket()` → `connect()` (client)
- TCP is a byte stream: implement message framing (length prefix or delimiter) at the application layer
- Always use `sendall()` for TCP to handle partial sends; use a loop with `recv()` to read complete messages
- UDP uses `sendto()` / `recvfrom()`; no connection; each datagram is independent
- `selectors` module enables non-blocking I/O multiplexing for high-concurrency servers without one-thread-per-connection
- Scapy enables packet crafting at any layer; useful for testing, network analysis, and security research
- Set socket timeouts; use `SO_REUSEADDR` on servers; close sockets with `try/finally` or `with` statements
