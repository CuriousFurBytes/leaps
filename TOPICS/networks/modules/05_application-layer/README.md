# Module 05: Application Layer Protocols

[← Previous](../04_transport-layer/) | [Topic Home](../../README.md) | [Next →](../06_routing-protocols/)

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

This module covers the application-layer protocols that engineers interact with every day: DNS (the phone book of the internet), HTTP/1.1/2/3 (the protocol powering the web), TLS (the security layer protecting HTTPS), and SMTP (email delivery). Understanding these protocols at the message level — not just as black boxes — is essential for debugging production systems, building web services, and understanding security vulnerabilities.

---

## Prerequisites

- Module 03: IP Networking — IP addressing and routing
- Module 04: Transport Layer — TCP and UDP (DNS uses UDP, HTTP uses TCP or QUIC)

---

## Objectives

By the end of this module, you will be able to:

1. Trace a complete DNS resolution from stub resolver to root server to TLD to authoritative nameserver
2. Read and construct HTTP/1.1 request and response messages from scratch
3. Explain the key improvements of HTTP/2 (multiplexing, header compression, server push) over HTTP/1.1
4. Explain why HTTP/3 uses QUIC instead of TCP and what problems this solves
5. Describe the TLS 1.3 handshake and what properties it provides (confidentiality, integrity, authentication)
6. Explain how SMTP works for email delivery, including MX records and STARTTLS

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### DNS — The Domain Name System

DNS translates human-readable hostnames into IP addresses. It is a distributed, hierarchical database:

```
Browser → Stub Resolver → Recursive Resolver → Root Nameserver
                                              → TLD Nameserver (.com)
                                              → Authoritative Nameserver (example.com)
```

**Full DNS resolution trace:**

```bash
# Trace the full DNS resolution hierarchy
dig +trace example.com

# Query a specific DNS server
dig @8.8.8.8 example.com A

# Reverse DNS lookup
dig -x 93.184.216.34
```

```python
# DNS query using Python's socket module
import socket

# getaddrinfo performs DNS resolution + gives socket-ready address info
results = socket.getaddrinfo('example.com', 80, proto=socket.IPPROTO_TCP)
for family, type_, proto, canonname, sockaddr in results:
    print(f"IP: {sockaddr[0]}, Port: {sockaddr[1]}")
```

DNS record types relevant to every engineer: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (SPF/DKIM/DMARC), NS (nameserver), PTR (reverse lookup).

DNS uses UDP port 53 for queries under 512 bytes; TCP for larger responses and zone transfers. DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) encrypt DNS traffic.

### HTTP/1.1

HTTP is a text-based request-response protocol. Every HTTP/1.1 message has headers separated from the body by a blank line (`\r\n\r\n`):

```
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
Accept: text/html\r\n
Connection: keep-alive\r\n
\r\n
```

Response:
```
HTTP/1.1 200 OK\r\n
Content-Type: text/html; charset=utf-8\r\n
Content-Length: 1256\r\n
\r\n
<html>...</html>
```

Key HTTP/1.1 issues: **head-of-line blocking** (requests on the same connection must be served in order), no multiplexing, redundant headers, no server push.

### HTTP/2

HTTP/2 (RFC 7540, 2015) addresses HTTP/1.1's performance issues:
- **Binary framing:** replaces text; more efficient to parse
- **Multiplexing:** multiple concurrent streams on one TCP connection; responses can be interleaved
- **Header compression (HPACK):** sends only changed headers; dramatically reduces overhead
- **Server push:** server can proactively send resources the client will need

HTTP/2 runs over TCP (with TLS in practice). It still suffers from TCP head-of-line blocking at the transport layer.

### HTTP/3

HTTP/3 (RFC 9114, 2022) replaces TCP with QUIC:
- **QUIC:** a UDP-based transport with TLS 1.3 built in; provides multiplexing without TCP head-of-line blocking
- **0-RTT connections:** QUIC can resume connections without a full handshake (using session tickets)
- **Connection migration:** a QUIC connection can survive IP address changes (useful for mobile)

QUIC provides TLS-level security, stream multiplexing, and reliability at the transport layer. Each QUIC stream is independent — a lost packet in one stream does not block others.

### TLS Handshake (TLS 1.3)

TLS provides: confidentiality (encryption), integrity (authentication codes), and server authentication (certificates).

TLS 1.3 handshake (1-RTT):
```
Client                          Server
  │── ClientHello ──────────────►│   (cipher suites, key share)
  │◄── ServerHello, Certificate, │
  │    Finished ─────────────────│   (server's key share, cert, MAC)
  │── Finished ──────────────────►│
  │        Application Data      │   (now encrypted)
```

The key exchange uses Diffie-Hellman; the server's certificate provides authentication. Forward secrecy means past sessions cannot be decrypted even if the server's private key is later compromised.

```python
# Making an HTTPS request (TLS handled by ssl module)
import socket
import ssl

context = ssl.create_default_context()  # loads system CA certificates

with socket.create_connection(('example.com', 443)) as sock:
    with context.wrap_socket(sock, server_hostname='example.com') as tls_sock:
        # Send HTTP/1.1 request over the TLS connection
        tls_sock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
        response = b""
        while True:
            chunk = tls_sock.recv(4096)
            if not chunk:
                break
            response += chunk

print(response[:500])  # print first 500 bytes of the response
```

### SMTP Basics

SMTP (Simple Mail Transfer Protocol) delivers email between servers. Key facts:
- Port 25 (server-to-server), 587 (submission with STARTTLS), 465 (SMTPS — TLS wrapper)
- DNS MX records direct mail to the correct server for a domain
- Commands: EHLO, MAIL FROM, RCPT TO, DATA, QUIT
- Modern SMTP uses STARTTLS (upgrade to TLS mid-session) or implicit TLS on port 465

---

## Key Concepts

**DNS** — Distributed hierarchical database; resolves hostnames to IP addresses. See [[networks#dns]].

**HTTP** — Hypertext Transfer Protocol; text-based (HTTP/1.1), binary (HTTP/2), QUIC-based (HTTP/3) application protocol.

**TLS** — Transport Layer Security; provides confidentiality, integrity, and server authentication. See [[networks#tls]].

**QUIC** — Quick UDP Internet Connections; UDP-based transport with built-in TLS, multiplexing, and stream independence; used by HTTP/3.

**MX record** — DNS Mail Exchanger record; points to the server(s) responsible for accepting email for a domain.

**Forward secrecy** — TLS property ensuring that session keys are not derivable from the server's long-term private key; past sessions remain confidential even if the key is compromised.

---

## Examples

```bash
# Inspect the full HTTP request/response with curl
curl -v https://example.com 2>&1 | head -60

# Check TLS certificate details
openssl s_client -connect example.com:443 -showcerts < /dev/null 2>/dev/null | openssl x509 -text -noout | grep -E 'Subject:|Issuer:|Not Before:|Not After:'

# Query DNS with detailed output
dig +short A github.com          # just the IP
dig MX gmail.com                  # mail exchangers
dig TXT _dmarc.gmail.com          # DMARC policy
```

---

## Common Pitfalls

**Assuming DNS is instant:** DNS resolution can take 50–500ms on a cold cache. Applications that make many DNS lookups per request (e.g., microservices calling many hostnames) can have significant DNS overhead. Use connection pools and DNS caching to mitigate.

**Not validating TLS certificates:** Always use `ssl.create_default_context()` in Python, which verifies the certificate chain and hostname. Using `ssl.CERT_NONE` or disabling verification silently removes all TLS security.

**Confusing HTTP versions:** HTTP/1.1, HTTP/2, and HTTP/3 are all HTTP — same methods (GET, POST), same status codes (200, 404), same headers. The difference is the framing and transport below the HTTP layer. A web server can speak all three.

---

## Cross-Links

- [[networks/modules/04_transport-layer]] — TCP and UDP underlie HTTP and DNS
- [[networks/modules/08_network-security]] — TLS certificate pinning, HSTS, DNS hijacking are security topics building on this module
- [[networks#dns]] — DNS glossary entry
- [[networks#tls]] — TLS glossary entry
- [[devops-platform-engineering]] — HTTP load balancers, TLS termination, and CDN caching all operate at this layer

---

## Summary

- DNS is a distributed hierarchical database; resolution walks: stub resolver → recursive resolver → root → TLD → authoritative nameserver
- DNS record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (policy/verification), NS (nameserver)
- HTTP/1.1: text-based; sequential requests on a connection; head-of-line blocking; keep-alive reuses connections
- HTTP/2: binary framing; multiplexed streams on one TCP connection; HPACK header compression; server push
- HTTP/3: QUIC transport (UDP + TLS 1.3 built-in); independent streams eliminate TCP head-of-line blocking; 0-RTT resumption
- TLS 1.3: 1-RTT handshake; Diffie-Hellman key exchange; forward secrecy; certificate-based server authentication
- SMTP delivers email via MX records; ports 25 (server), 587 (submission), 465 (TLS)
