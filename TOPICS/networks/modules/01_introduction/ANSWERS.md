# Answer Key — Module 01: Introduction to Computer Networks

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — PDU Names by OSI Layer [1 pt]

**Full credit answer:**
- Layer 1 (Physical): Bit
- Layer 2 (Data Link): Frame
- Layer 3 (Network): Packet
- Layer 4 (Transport): Segment (TCP) or Datagram (UDP)
- Layers 5, 6, 7: Data (or Message)

**Key points required:**
- Frame at Layer 2, Packet at Layer 3, Segment/Datagram at Layer 4 are the three that matter most
- Bit at Layer 1 is a nice bonus

**Common wrong answers:**
- Calling Layer 3 a "segment": a segment is Layer 4 (TCP). Layer 3 is a packet.
- Calling Layer 2 a "packet": a packet is Layer 3. Layer 2 is a frame.

---

### 1.2 — TTL Definition and Purpose [1 pt]

**Full credit answer:**
TTL stands for Time To Live. It is an 8-bit field in the IP packet header (values 0–255). Every router that forwards the packet decrements TTL by 1. When TTL reaches 0, the router discards the packet and sends an ICMP Time Exceeded message back to the source. TTL prevents packets from looping forever in the network if a routing loop occurs.

**Key points required:**
- TTL = Time To Live
- Decremented by 1 at each router hop
- Prevents routing loops / infinite packet circulation

---

### 1.3 — Three Differences: Hub vs. Switch [1 pt]

**Full credit answer (any three of these):**
1. A hub operates at Layer 1 (Physical); a switch operates at Layer 2 (Data Link)
2. A hub sends every incoming signal to all ports; a switch sends frames only to the port associated with the destination MAC address
3. A hub causes collisions (all devices share one collision domain); a switch creates a separate collision domain per port
4. A hub has no intelligence; a switch maintains a MAC address table
5. Hubs are effectively obsolete in modern networks; switches are the standard

**Partial credit:** 0.5 pts if only 1–2 differences are identified correctly.

---

### 1.4 — Router: Layer and Addressing [1 pt]

**Full credit answer:**
A router operates at Layer 3 (Network layer). It makes forwarding decisions based on the destination IP address in the IP packet header. It looks up the destination IP in its routing table to determine which interface (and next hop) to forward the packet to.

**Key points required:**
- Layer 3 (not Layer 2)
- Uses IP addresses (not MAC addresses)

---

### 1.5 — Definition of Encapsulation [1 pt]

**Full credit answer:**
Encapsulation is the process by which each layer in the network stack adds its own header (and sometimes trailer) to the data it receives from the layer above it. The entire output of the upper layer (header + payload) becomes the payload of the lower layer's PDU. On the receiving side, each layer strips its own header and passes the inner payload up to the next layer (decapsulation).

**Key points required:**
- Each layer adds its own header
- The upper layer's entire PDU becomes the lower layer's payload
- Reversed (decapsulation) at the receiver

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Why Frames Are Replaced at Every Router Hop [2 pts]

**Full credit answer:**
Ethernet frames contain MAC addresses, which are only meaningful within a single network segment (Layer 2 domain). When a packet crosses a router, it enters a new network segment where the source and destination devices have different MAC addresses. The frame must be recreated with new MAC addresses appropriate for the next segment.

Specifically: the new source MAC is the router's outgoing interface MAC, and the new destination MAC is the MAC of the next hop (either the next router or the final destination, found via ARP). If frames were not replaced, the MAC addresses from the originating LAN would be meaningless on any other segment, and the receiving devices would discard the frames.

The IP packet passes through unchanged (except TTL decrement) because IP addresses are globally routable and don't change meaning as the packet traverses networks.

**Rubric:**
- 2 pts: Correctly explains MAC locality, why new frame is needed, what happens at the router, and why IP packet is preserved
- 1 pt: Correctly identifies that MAC addresses are local but misses the explanation of what the router does
- 0 pts: Incorrect understanding (e.g., "frames are the same throughout" or "routers change the IP address")

---

### 2.2 — TCP/IP vs. OSI Layer Count [2 pts]

**Full credit answer:**
The statement is incorrect. TCP/IP has 4 layers (Link, Internet, Transport, Application), not 7. OSI has 7 layers. The OSI model is a theoretical/conceptual framework for describing network communication. TCP/IP is the actual protocol suite the internet runs on.

The relationship between them: TCP/IP's Application layer roughly covers OSI layers 5, 6, and 7 (Session, Presentation, Application). TCP/IP's Internet layer maps to OSI Layer 3. TCP/IP's Transport layer maps to OSI Layer 4. TCP/IP's Link layer maps to OSI Layers 1 and 2.

Engineers use OSI layer numbers when discussing architecture ("Layer 7 firewall," "Layer 3 switch") as a common vocabulary, even though the underlying protocols are TCP/IP.

**Rubric:**
- 2 pts: Correctly states TCP/IP has 4 layers, explains the relationship to OSI, explains why OSI terminology is still used
- 1 pt: Correctly says TCP/IP has 4 layers but doesn't clearly explain the mapping or why OSI is still relevant
- 0 pts: Agrees with the statement or gives wrong layer count

---

### 2.3 — Packet Switching vs. Circuit Switching [2 pts]

**Full credit answer:**
Circuit switching (used by traditional telephone networks) establishes a dedicated, reserved path between sender and receiver for the duration of the communication. This guarantees bandwidth and latency but wastes capacity when the circuit is idle.

Packet switching (used by the internet) breaks data into packets that are individually routed through the network. Multiple conversations can share the same physical links simultaneously, dramatically improving network utilization. The tradeoff is that packets can arrive out of order, be delayed, or be lost.

**Concrete example:** Consider 10,000 simultaneous phone calls using circuit switching — each requires a dedicated circuit, consuming resources even during pauses in conversation (silence = wasted capacity). With packet switching, those same physical links can carry traffic from millions of users because idle capacity is used by other packets.

The problem packet switching solves that circuit switching cannot: efficient statistical multiplexing — the ability to share physical links among many simultaneous users without reserving dedicated capacity.

**Rubric:**
- 2 pts: Explains both mechanisms, identifies statistical multiplexing as the key benefit, provides a concrete example
- 1 pt: Describes one mechanism clearly or gives a general comparison without depth
- 0 pts: Confuses the two or provides an incorrect description

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Interpret ping Failure with curl Success [3 pts]

**Full credit answer:**

**(a)** The ping failure tells you that ICMP packets are being dropped somewhere between you and the host. This could be the host itself (a host-based firewall blocking ICMP), a network firewall between you, or a firewall on the router. It does NOT indicate the host is unreachable.

**(b)** The successful curl tells you the host is reachable on TCP port 80 and a web server is running. The HTTP response confirms end-to-end TCP connectivity and that the application layer is working.

**(c)** Most likely, the host (192.168.1.1 — a router admin panel) or a firewall in front of it is configured to drop ICMP echo requests (a common security hardening measure). The host is perfectly healthy and serving HTTP traffic. Next steps: check whether other TCP ports respond, check the router's ICMP settings, confirm no packet filtering rule explicitly blocks ICMP from your source.

**Rubric:** 1 pt each for (a), (b), (c) correct. Full credit requires understanding that ping failure ≠ host down.

**Teaching note:** The most common misconception here is treating ping as the definitive reachability test. Many production hosts and firewalls drop ICMP by default. Always verify with a known-open TCP service.

---

### 3.2 — MAC and IP Addresses Across a Router Hop [3 pts]

**Full credit answer:**

**Frame 1** (leaving host A → router):
- Source IP: 10.0.1.5 (host A)
- Destination IP: 10.0.2.7 (host B) — unchanged throughout
- Source MAC: aa:bb:cc:dd:ee:01 (host A's NIC)
- Destination MAC: aa:bb:cc:dd:ee:99 (router's eth0 — the gateway for subnet 10.0.1.0)

**Frame 2** (leaving router → host B):
- Source IP: 10.0.1.5 (host A) — still unchanged
- Destination IP: 10.0.2.7 (host B) — still unchanged
- Source MAC: 11:22:33:44:55:77 (router's eth1)
- Destination MAC: 11:22:33:44:55:66 (host B's NIC)

**Key insight:** The IP addresses never change (they are end-to-end). The MAC addresses change at every router hop (they are hop-by-hop). The router "bridges" between the two Layer 2 domains.

**Rubric:**
- 3 pts: All 8 address fields correct in both frames
- 2 pts: IP addresses correct in both frames, and MAC source/dest mostly correct (1–2 errors)
- 1 pt: IP addresses correct but MAC addresses mostly wrong, or vice versa
- 0 pts: Fundamental misunderstanding of the encapsulation model

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Out-of-Order UDP Messages [3 pts] (1 pt each part)

**(a) Is this expected?**
Yes, this is completely expected behavior with UDP. UDP is a connectionless, unreliable protocol that provides no guarantees about delivery order, delivery itself, or duplication. Out-of-order arrival is one of its well-documented characteristics.

**(b) Protocol-level explanation:**
IP (Layer 3) routes packets independently. Each packet may take a different path through the internet depending on current routing table state. Packets that take different routes naturally arrive in different orders. Even packets on the same path can be reordered by router queuing. UDP provides no mechanism to detect or correct reordering.

**(c) Two options with tradeoffs:**

1. **Switch to TCP:** TCP provides guaranteed in-order delivery using sequence numbers and reordering buffers. Simple to implement — just change `SOCK_DGRAM` to `SOCK_STREAM`. Tradeoff: TCP adds latency (handshake, retransmission), higher overhead per message, and head-of-line blocking. Best choice if message ordering is critical and latency is not the primary concern.

2. **Add sequence numbers to the application protocol:** Include a message sequence number in every UDP packet. On the receiver side, buffer out-of-order packets and reorder them before processing, or simply discard them if ordering is needed and dropped packets are acceptable (e.g., live video). Tradeoff: requires significant application-layer work; you're essentially reinventing part of TCP. Best choice if low latency is critical and some message loss is acceptable (e.g., telemetry, gaming).

---

## Section 5: Discussion — Answer Key

### 5.1 — Why OSI Persists in Practice [2 pts]

**Example strong answer:**
The OSI model persists because it provides a precise, agreed-upon vocabulary that transcends any specific protocol. When an engineer says "Layer 7 load balancer," everyone in the industry immediately understands they mean a device that makes routing decisions based on HTTP content — a precise concept that would take many words to explain without the OSI vocabulary. This shared language is enormously valuable even when the technical implementation uses TCP/IP, not OSI.

From a different perspective, OSI's seven-layer decomposition is genuinely more precise than TCP/IP's four layers for some discussions. TLS, for example, genuinely operates differently from application code and from TCP — having a "Presentation layer" concept, even as a mental model, helps explain why TLS libraries have a specific interface distinct from the application above and the socket below.

**Elements that earn full credit:**
- Identifies the vocabulary/communication value of OSI
- Recognizes that TCP/IP is what's actually implemented
- Addresses whether OSI is still useful (either perspective is valid with good reasoning)

**Rubric:**
- 2 pts: Considers at least two perspectives; reasoning is coherent; doesn't just say "because people are used to it"
- 1 pt: One valid perspective with some reasoning
- 0 pts: Off-topic or fundamental misunderstanding

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Traceroute Alternative When ICMP Is Blocked [+5 pts]

**Full credit answer:**
Windows `tracert` uses ICMP Echo Request packets (like ping) with incrementing TTL, relying on ICMP Time Exceeded responses. Unix `traceroute` by default uses UDP packets to high-numbered ports (typically 33434 and above), which are unlikely to be in use on the destination.

An alternative implementation that bypasses ICMP-blocking could use **TCP SYN packets** — this is what tools like `tcptraceroute` implement. The technique:
- Send TCP SYN packets to a port the destination is known to accept (e.g., port 80 or 443)
- Intermediate routers still generate ICMP Time Exceeded responses (they must, per RFC 792, when TTL hits 0)
- The destination responds with TCP SYN-ACK (or RST if the port is filtered), confirming arrival

**Tradeoffs:**
- Pro: Works through firewalls that allow TCP to the target port; the destination response confirms the target is reached
- Pro: More closely represents the path your actual application traffic takes
- Con: Requires choosing a specific open port; some firewalls still rate-limit ICMP TTL-exceeded
- Con: Slightly more complex to implement; may confuse servers that log unexpected TCP connections

Another option: **UDP to a known-open port** (e.g., DNS port 53) — the destination will respond with a UDP packet or ICMP Port Unreachable, confirming arrival, even when ICMP Echo is blocked.

**Rubric:**
- 5 pts: Identifies TCP SYN or another valid approach; explains the mechanism; identifies at least 2 tradeoffs
- 3 pts: Correct direction (TCP-based traceroute) but incomplete tradeoff analysis
- 1 pt: Identifies that Windows and Unix use different methods but can't explain the technical mechanism

---

## Common Wrong Answers Across the Test

1. **Confusing MAC and IP address roles:** MAC addresses are local to a network segment; IP addresses are end-to-end. Students who mix these up need to re-read the "How Data Travels: Encapsulation" section.

2. **Treating ping failure as proof of host failure:** A host that drops ICMP (very common with firewalls) still serves TCP. Always verify with the actual protocol you care about.

3. **Believing frames contain the final destination MAC:** Frames always address the next hop, never the final destination (unless it's on the same local segment). The frame at hop 1 is addressed to the first router, not the destination.

---

## Teaching Notes

- Students who struggle with Section 2 likely read without testing their understanding. Recommend re-studying with the Feynman technique (explain it aloud to yourself or another person).
- Students who struggle with Section 3 need more hands-on practice. Run the actual commands (`ping`, `traceroute`, `ss`) before attempting the test.
- The bonus question tests understanding of how traceroute exploits TTL — don't be concerned if most students skip it.
- A score below 60% generally indicates the concepts didn't click. Ask which concept feels most foreign and re-read that section of the README with a specific question in mind.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
