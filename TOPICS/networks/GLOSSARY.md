# Computer Networks — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of Computer Networks.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use.
```

Keep definitions in your own words as much as possible. If you're copying from a source, add attribution.

---

## B

### BGP

**Definition:** Border Gateway Protocol — the routing protocol that exchanges reachability information between autonomous systems (ASes) on the internet. BGP is the protocol that determines which path internet traffic takes between organizations and countries. It is a path-vector protocol: each route advertisement includes the sequence of ASes the traffic will traverse, allowing policy-based routing decisions.

**Also known as:** The protocol that runs the internet; exterior gateway protocol (EGP)

**Related:** [[networks/modules/06_routing-protocols]], [[networks#autonomous-system]]

**Example:**
When Cloudflare (AS13335) announces the prefix `104.16.0.0/12` to its upstream providers via BGP, every router on the internet learns that traffic destined for those IP addresses should flow toward Cloudflare.

---

## C

### CIDR

**Definition:** Classless Inter-Domain Routing — a method for allocating IP addresses and routing using variable-length subnet masks (VLSM) rather than the fixed class boundaries (Class A/B/C) of original IPv4. CIDR notation expresses an IP address and its network prefix length as `address/prefix-length`, e.g. `192.168.1.0/24`.

**Also known as:** Slash notation, prefix notation

**Related:** [[networks/modules/03_ip-networking]], [[networks#subnet-mask]]

**Example:**
`10.0.0.0/8` represents the entire 10.x.x.x space (16,777,216 addresses). `10.0.1.0/24` is a subnet within it with 256 addresses (254 usable).

---

## D

### DNS

**Definition:** Domain Name System — the distributed, hierarchical database that translates human-readable hostnames (e.g. `www.example.com`) into IP addresses (e.g. `93.184.216.34`). DNS operates primarily over UDP port 53 and uses a tree-structured namespace with root servers at the top, then TLD servers, then authoritative name servers for each domain.

**Also known as:** The phone book of the internet

**Related:** [[networks/modules/05_application-layer]]

**Example:**
When you browse to `github.com`, your system sends a DNS query to its configured resolver. The resolver walks the DNS hierarchy to find GitHub's authoritative nameserver, retrieves the A record, and returns the IP address to your browser.

---

## F

### Frame

**Definition:** The Protocol Data Unit (PDU) at the Data Link layer (OSI Layer 2). A frame encapsulates a Layer 3 packet by adding a source MAC address, destination MAC address, an EtherType field identifying the upper-layer protocol, and a Frame Check Sequence (FCS) for error detection. Frames are local to a single network segment — they are discarded and recreated at each router hop.

**Also known as:** Ethernet frame (when referring specifically to IEEE 802.3)

**Related:** [[networks/modules/02_physical-and-datalink]], [[networks#packet]], [[networks#mac-address]]

**Example:**
An Ethernet frame carrying an IP packet has a 14-byte header (6 bytes destination MAC + 6 bytes source MAC + 2 bytes EtherType), the IP packet as payload, and a 4-byte FCS trailer.

---

## I

### IP Address

**Definition:** A numerical label assigned to each device participating in a computer network that uses the Internet Protocol for communication. IPv4 addresses are 32 bits long, written in dotted-decimal notation (`192.168.1.1`). IPv6 addresses are 128 bits, written in colon-separated hexadecimal groups (`2001:db8::1`). IP addresses have two parts: a network portion (identifying the network) and a host portion (identifying the device within that network).

**Also known as:** Internet address, network address (loosely)

**Related:** [[networks/modules/03_ip-networking]], [[networks#cidr]], [[networks#subnet-mask]]

**Example:**
The address `10.0.1.42/24` indicates host 42 on the `10.0.1.0/24` network. The `/24` prefix means the first 24 bits (`10.0.1`) identify the network and the last 8 bits (`.42`) identify the host.

---

## L

### Latency

**Definition:** The time delay between a stimulus and its response in a network. In networking, latency typically refers to the round-trip time (RTT) — the time for a packet to travel from sender to receiver and the acknowledgment to return. Latency has multiple components: propagation delay (speed of light in the medium), transmission delay (time to put bits on the wire), queuing delay (time waiting in router buffers), and processing delay (router lookup time).

**Also known as:** Round-trip time (RTT), ping time (informally)

**Related:** [[networks/modules/04_transport-layer]], [[networks/modules/11_troubleshooting-and-tools]]

**Example:**
A ping from New York to London has a minimum propagation latency of ~35ms one way (the speed of light over ~5,500km of fiber). Total RTT is typically 70–90ms due to transmission and queuing delays.

---

## N

### NAT

**Definition:** Network Address Translation — a technique in which a router or firewall rewrites the source or destination IP address (and often port) of packets as they pass through it. NAT allows multiple devices on a private network to share a single public IP address. The most common form is NAPT (Network Address and Port Translation), also called "masquerade" on Linux.

**Also known as:** PAT (Port Address Translation), IP masquerading

**Related:** [[networks/modules/03_ip-networking]]

**Example:**
Your home router has one public IP from your ISP. When your laptop (`192.168.1.10`) makes a request to a server, the router rewrites the source to its public IP and records the mapping in a NAT table. When the reply arrives, it looks up the table and forwards the packet back to `192.168.1.10`.

---

## P

### Packet

**Definition:** The Protocol Data Unit (PDU) at the Network layer (OSI Layer 3). A packet encapsulates a Transport-layer segment by adding a source IP address, destination IP address, TTL (Time To Live), and protocol identifier. Unlike frames, packets survive router hops — routers read the destination IP, make a forwarding decision, and forward the packet toward its destination.

**Also known as:** IP datagram (specifically for IP-layer packets)

**Related:** [[networks/modules/03_ip-networking]], [[networks#frame]]

**Example:**
An IPv4 packet has a 20-byte minimum header: version (4 bits), IHL, DSCP, total length, identification, flags, fragment offset, TTL, protocol, checksum, source IP (4 bytes), destination IP (4 bytes).

---

### Port

**Definition:** A 16-bit unsigned integer (0–65535) that identifies a specific process or service on a host. Ports allow a single IP address to support many simultaneous connections and services. Ports 0–1023 are "well-known" ports reserved for standard services (HTTP=80, HTTPS=443, SSH=22, DNS=53). Ports 1024–49151 are registered ports. Ports 49152–65535 are ephemeral (temporary, client-side).

**Also known as:** TCP port, UDP port, port number

**Related:** [[networks/modules/04_transport-layer]]

**Example:**
A web server listens on TCP port 443. Your browser opens a connection from ephemeral port 52341 on your machine to port 443 on the server. The 4-tuple (srcIP, srcPort, dstIP, dstPort) uniquely identifies each TCP connection.

---

### Protocol

**Definition:** A set of rules and conventions that govern how data is formatted, transmitted, and received between communicating entities. A protocol specifies the syntax (format of messages), semantics (meaning of each field), and timing (when messages are sent and how long to wait for replies). Protocols at different layers of the network stack cooperate via well-defined interfaces.

**Also known as:** Network protocol, communication protocol

**Related:** [[networks/modules/01_introduction]]

**Example:**
HTTP is a protocol that specifies: requests start with a method (GET, POST) and path, headers follow in `Key: Value\r\n` format, an empty line separates headers from body, and the server responds with a status code, headers, and body.

---

## S

### Socket

**Definition:** An abstraction provided by the operating system that represents one endpoint of a network connection. A socket is identified by an IP address and port number. The Berkeley Sockets API (BSD sockets) — introduced in 4.2BSD Unix in 1983 — is the standard interface that programs use to create network connections; it has been adopted by virtually every operating system.

**Also known as:** Network socket, BSD socket

**Related:** [[networks/modules/10_network-programming]]

**Example:**
In Python: `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` creates a TCP socket. `s.connect(('example.com', 80))` connects it to a remote endpoint. The OS assigns an ephemeral local port automatically.

---

### Subnet Mask

**Definition:** A 32-bit number (for IPv4) that distinguishes the network portion of an IP address from the host portion. In CIDR notation, the prefix length (e.g. `/24`) is equivalent to a subnet mask of `255.255.255.0`. A bitwise AND of the IP address and the subnet mask yields the network address.

**Also known as:** Network mask, netmask

**Related:** [[networks/modules/03_ip-networking]], [[networks#cidr]], [[networks#ip-address]]

**Example:**
IP `192.168.10.45`, mask `255.255.255.0` (`/24`): the network address is `192.168.10.0` and the host is `.45`. The broadcast address is `192.168.10.255`.

---

## T

### TCP

**Definition:** Transmission Control Protocol — a connection-oriented, reliable, ordered byte-stream transport protocol. TCP guarantees delivery (retransmits lost segments), ordering (delivers data in sequence), and flow control (does not overwhelm the receiver). It establishes connections with a 3-way handshake (SYN, SYN-ACK, ACK) and closes them with a 4-way exchange (FIN, ACK, FIN, ACK). TCP is the transport used by HTTP, HTTPS, SSH, and most application protocols.

**Also known as:** TCP/IP (loosely, referring to the combination with IP)

**Related:** [[networks/modules/04_transport-layer]]

**Example:**
When your browser opens an HTTPS connection, it first completes a TCP 3-way handshake (typically in 1 RTT), then performs a TLS handshake (1–2 RTTs), then sends HTTP requests. The TCP layer handles all retransmission and ordering transparently.

---

### TLS

**Definition:** Transport Layer Security — a cryptographic protocol that provides confidentiality, integrity, and authentication for network communications. TLS runs on top of TCP and below application protocols (HTTPS = HTTP over TLS). TLS 1.3 (RFC 8446, 2018) reduced the handshake to 1 RTT and removed weak cipher suites. TLS superseded SSL (Secure Sockets Layer), which should no longer be used.

**Also known as:** SSL (legacy term; technically incorrect for TLS); HTTPS (when TLS protects HTTP)

**Related:** [[networks/modules/05_application-layer]], [[networks/modules/08_network-security]]

**Example:**
In TLS 1.3, the client sends a ClientHello with supported cipher suites and key share. The server responds with ServerHello, its certificate, and the handshake is complete in one round trip. The connection is then encrypted with a symmetric key derived from the key exchange.

---

### UDP

**Definition:** User Datagram Protocol — a connectionless, unreliable transport protocol. UDP sends individual datagrams without establishing a connection, without guaranteeing delivery, and without ensuring order. What it lacks in reliability it makes up for in speed and simplicity: no handshake overhead, no retransmission delay. UDP is used by DNS, NTP, DHCP, video streaming, VoIP, and gaming.

**Also known as:** Connectionless transport

**Related:** [[networks/modules/04_transport-layer]]

**Example:**
A DNS query is sent as a single UDP datagram to port 53. If no response arrives within a timeout, the client retransmits — this application-layer retry is simpler and faster than TCP's built-in machinery for a one-packet exchange.

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
