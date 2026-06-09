# Exercises — Module 01: Introduction to Computer Networks

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just think through the answer — actually write it out.
3. **Check your answer** against the acceptance criteria, not just the solution.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Name That Layer [🟢 Easy] [1 pt]

### Context
This exercise tests your ability to map protocols and devices to OSI layers — a skill you'll use constantly in troubleshooting conversations.

### Task
For each item below, state which OSI layer it belongs to and briefly explain why.

1. IP packet header
2. Ethernet frame (MAC address header)
3. TCP port number
4. An HTTP `GET /index.html` request
5. A network cable and the electrical signals on it
6. A router
7. A switch
8. TLS encryption/decryption

### Requirements
- [ ] Correctly maps all 8 items to their primary OSI layer
- [ ] Provides a one-sentence justification for each

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Use the mnemonic: Physical (bits), Data Link (frames, MACs), Network (packets, IPs), Transport (segments, ports), Application (everything your app sees directly).

</details>

### Expected Output / Acceptance Criteria

Each item should be mapped as follows (±1 layer with valid justification is acceptable for contested items):

1. IP → Layer 3 (Network)
2. Ethernet frame / MAC → Layer 2 (Data Link)
3. TCP port → Layer 4 (Transport)
4. HTTP GET request → Layer 7 (Application)
5. Cable + electrical signals → Layer 1 (Physical)
6. Router → Layer 3 (Network)
7. Switch → Layer 2 (Data Link)
8. TLS → Layer 6 (Presentation) in OSI; commonly placed in Application in TCP/IP

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

| Item | Layer | Reason |
|------|-------|--------|
| IP packet header | 3 (Network) | IP is the network-layer protocol; its header contains source/destination IPs |
| Ethernet frame / MAC | 2 (Data Link) | Ethernet is the dominant data-link protocol; MAC addresses are Layer 2 |
| TCP port number | 4 (Transport) | Ports identify processes; TCP is the transport protocol |
| HTTP GET request | 7 (Application) | HTTP is an application protocol; its messages are Layer 7 PDUs |
| Cable + electrical signals | 1 (Physical) | Layer 1 concerns the raw transmission medium and signal encoding |
| Router | 3 (Network) | Routers make forwarding decisions based on IP (Layer 3) addresses |
| Switch | 2 (Data Link) | Switches forward frames based on MAC (Layer 2) addresses |
| TLS | 6 (Presentation) in OSI | Handles encryption/decryption and encoding; in TCP/IP model, considered Application-layer code |

**Common wrong answers and why they fail:**
- Saying routers are Layer 2: routers operate at Layer 3 (IP); switches are Layer 2 (MAC)
- Saying TLS is Layer 4: TLS runs on top of TCP (which is Layer 4); TLS itself is Layer 5/6

</details>

---

## Exercise 2: Trace the Encapsulation [🟢 Easy] [1 pt]

### Context
Understanding encapsulation is critical — it explains how a single application message becomes bits on a wire.

### Task
A Python program on Machine A sends the string "Hello, World!" to a Python program on Machine B over TCP. List the headers that wrap the data at each layer as it travels from A's application down to the physical medium. For each layer, name:
- The PDU name
- What addressing information is in the header

### Requirements
- [ ] Lists all 4 relevant TCP/IP layers (Application → Transport → Internet → Link)
- [ ] Names the correct PDU at each layer
- [ ] Identifies the correct addressing info at each layer

### Hints
<details>
<summary>Hint 1</summary>

Work from the application down. What does TCP add? What does IP add? What does Ethernet add?

</details>

### Expected Output / Acceptance Criteria

```
Layer 4 (Application): Data / Message — "Hello, World!" (no extra network header)
Layer 3 (Transport):   TCP Segment    — adds: source port, destination port, seq#, ack#
Layer 2 (Internet):    IP Packet      — adds: source IP, destination IP, TTL, protocol
Layer 1 (Link):        Ethernet Frame — adds: source MAC, destination MAC, EtherType, FCS
Physical:              Bits           — electrical/optical/radio signals
```

### Solution
<details>
<summary>Show Solution</summary>

```
Application:  "Hello, World!"
              ↓ TCP wraps it
Transport:    [TCP Header | "Hello, World!"]
              src_port=52341, dst_port=5000, seq=100, ack=200, checksum
              ↓ IP wraps the TCP segment
Internet:     [IP Header | TCP Segment]
              src_ip=10.0.0.1, dst_ip=10.0.0.2, ttl=64, protocol=6 (TCP)
              ↓ Ethernet wraps the IP packet
Link:         [Eth Header | IP Packet | FCS]
              src_mac=aa:bb:cc:dd:ee:ff, dst_mac=11:22:33:44:55:66, ethertype=0x0800
              ↓ NIC converts to bits
Physical:     01000101 00000000 ...
```

**Key point:** The string "Hello, World!" is just bytes. Each layer treats the layer-above's entire output (header + payload) as its own payload.

</details>

---

## Exercise 3: Hub vs Switch vs Router Decision [🟡 Medium] [2 pts]

### Context
Choosing the right device for a network requires understanding what layer each device operates at and what problem it solves. This exercise tests that decision-making.

### Task
For each of the following scenarios, identify the best device (hub, switch, or router) and explain why. Also explain why the other two options would not work or would be suboptimal.

1. You want to connect 4 computers in a small office so they can share files with each other. All computers are on the same IP subnet (192.168.1.0/24).

2. You want to connect your office network (192.168.1.0/24) to the internet (via your ISP connection).

3. You're setting up a lab to test very old network equipment and you need all traffic broadcast to all ports (even though this is inefficient).

4. You have two buildings on the same campus with the same IP subnet (10.0.0.0/24) and you need to connect them so devices can talk to each other.

### Requirements
- [ ] Selects the correct device for each scenario
- [ ] Explains why the chosen device works
- [ ] Explains why at least one alternative doesn't work for each scenario

### Hints
<details>
<summary>Hint 1</summary>

Think about what each device reads: hub reads nothing (just amplifies), switch reads MAC addresses, router reads IP addresses.

</details>

<details>
<summary>Hint 2</summary>

When devices are on the same IP subnet, they communicate directly (no router needed). When they're on different subnets, they need a router.

</details>

### Expected Output / Acceptance Criteria

Correct answers with clear explanations matching the logic below.

### Solution
<details>
<summary>Show Solution</summary>

1. **Switch** — All 4 computers are on the same subnet; they only need Layer 2 connectivity. A switch forwards frames to the correct port using MAC addresses, reducing unnecessary traffic. A router would require each computer to have a different subnet (overkill). A hub would work but is inefficient (broadcasts everything to all ports, causing collisions).

2. **Router** — Connecting to the internet requires routing between two different networks (your internal 192.168.1.0/24 and the ISP's public IP range). A switch cannot route between subnets. A hub cannot route at all.

3. **Hub** — The scenario explicitly requires broadcast behavior (all traffic to all ports). This is exactly what a hub does. In any real scenario, a hub would be a poor choice because it causes collisions and wastes bandwidth.

4. **Switch** — Both buildings are on the same subnet (10.0.0.0/24), so Layer 2 connectivity is all that's needed. A switch will work. A router would needlessly separate the subnet. A hub would work but with collision problems at scale.

**Alternative approaches:**
For scenario 4, if the buildings are connected by a long cable, a Layer 2 switch with an uplink (or a dedicated network bridge) would be the precise solution. If bandwidth or isolation matters, a router could be used to separate the subnets deliberately.

</details>

---

## Exercise 4: Interpret a traceroute Output [🟡 Medium] [2 pts]

### Context
`traceroute` is one of the most important network diagnostic tools. Being able to read its output and draw conclusions is a fundamental skill.

### Task
Analyze the following `traceroute` output and answer the questions below:

```
traceroute to database.internal (10.2.0.50), 30 hops max
 1  gateway.local (192.168.1.1)    1.2 ms   1.1 ms   1.2 ms
 2  10.0.0.1                       8.5 ms   8.3 ms   8.6 ms
 3  * * *
 4  * * *
 5  10.2.0.50                      45.2 ms  44.9 ms  45.1 ms
```

Questions:
1. How many routers did the packet traverse?
2. What do the three RTT values per line represent?
3. Why do hops 3 and 4 show `* * *`? Does this mean the route is broken?
4. The final RTT is ~45ms but hop 2 is only ~8.5ms. What explains the jump?
5. Is the destination reachable? How do you know?

### Requirements
- [ ] Answers all 5 questions correctly
- [ ] Explains the `***` behavior accurately (most commonly misunderstood)
- [ ] Correctly identifies that the destination is reachable

### Hints
<details>
<summary>Hint 1</summary>

The destination reached on hop 5 means... the route is complete. The `***` on hops 3 and 4 are intermediate hops that don't respond to ICMP, not missing hops.

</details>

### Expected Output / Acceptance Criteria

All 5 questions answered correctly.

### Solution
<details>
<summary>Show Solution</summary>

1. **5 routers** (hops 1 through 5, counting the destination as the final hop).

2. **Three separate probes** are sent at each TTL value to measure RTT consistency. The three values are three independent measurements. High variance between them suggests network congestion or variable path routing.

3. **`***` means those routers dropped or did not respond to ICMP TTL-exceeded messages** — either they're configured to not send ICMP, or a firewall between you and them is dropping ICMP. It does NOT mean the route is broken. The packet still passed through those routers (they decremented TTL and forwarded the packet — they just didn't bother to reply).

4. **The jump from ~8.5ms to ~45ms suggests significant latency was added at hops 3 or 4** — possibly a WAN link, a satellite hop, or a geographically distant data center. Since we can't see those hops, we can't pinpoint where, but the cumulative delay was ~36ms added somewhere between hop 2 and hop 5.

5. **Yes, the destination is reachable.** Hop 5 shows `10.2.0.50` responding with ~45ms RTT. If the destination were unreachable, there would be no response at hop 5.

</details>

---

## Exercise 5: Design a Small Network [🔴 Hard] [3 pts]

### Context
This exercise requires applying OSI layer concepts, device selection, and encapsulation knowledge to design a real network. There is no single correct answer — focus on justifying your decisions.

### Task
A small startup has the following requirements:
- 10 employees on the same floor, all needing internet access
- 1 public web server (must be accessible from the internet)
- 1 internal database server (must NOT be accessible from the internet)
- All devices need IP addresses

Design a network for this office. Your design should specify:
1. What network devices you would use and where
2. What IP address ranges you would assign (use RFC 1918 private space for internal devices)
3. How internet traffic flows from an employee laptop to a website
4. How the web server gets internet-accessible traffic while the database does not
5. Draw a simple ASCII or Mermaid diagram of the topology

### Requirements
- [ ] Names at least 2 distinct devices (router + switch minimum)
- [ ] Uses RFC 1918 private IP ranges for internal devices
- [ ] Explains how external traffic reaches the web server but not the database
- [ ] Traces the path of a packet from employee laptop to google.com
- [ ] The design is plausible (can actually work with real equipment)

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

You need at minimum: a router (to connect to the internet), a switch (to connect local devices), and some mechanism to allow the web server to receive public traffic while blocking the database. A firewall or DMZ can solve this.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

Consider using separate subnets: one for employee devices, one for the "DMZ" where the public web server lives, and one for the database server. The router/firewall controls what can talk to what.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

A typical small office design:
- Internet → Router/Firewall → [DMZ subnet] web server (192.168.10.x)
- Internet → Router/Firewall → [Internal subnet] employee laptops + database (192.168.1.x)
- Firewall rules: allow external port 80/443 → web server; deny external → database

</details>

### Expected Output / Acceptance Criteria

A valid network design that:
- Uses at least a router and a switch
- Has separate IP ranges for internal devices
- Explains traffic isolation between web server and database
- Traces packet flow correctly

### Solution
<details>
<summary>Show Solution</summary>

**Example design (many valid alternatives exist):**

```
Internet
    │
    ▼
[Router/Firewall]  (public IP from ISP: 203.0.113.5)
    │                   Firewall rules:
    │                   - Allow inbound TCP 80/443 → 192.168.10.10 (web server)
    │                   - Deny all other inbound
    │                   - Allow all outbound
    ├──────────────────────────────────────────────────────
    │                                                    │
    ▼                                                    ▼
[Switch A: DMZ]                               [Switch B: Internal]
192.168.10.0/24                               192.168.1.0/24
    │                                                    │
[Web Server]                              [Employee Laptops (x10)]
192.168.10.10                             192.168.1.10 – 192.168.1.19
                                          [Database Server]
                                          192.168.1.50
```

**Packet flow (employee laptop → google.com):**
1. Employee laptop (192.168.1.15) sends HTTP request
2. Destination IP (google.com) is not local → laptop sends to gateway (router: 192.168.1.1)
3. Router performs NAT: rewrites source to its public IP (203.0.113.5:ephemeral)
4. Router forwards packet to ISP
5. ISP routes packet toward Google
6. Response from Google arrives at 203.0.113.5 → router consults NAT table → forwards to 192.168.1.15

**Why the database is protected:**
The firewall only allows inbound connections to 192.168.10.10 on ports 80/443. The database server (192.168.1.50) has no inbound rules allowing external access. An external attacker would need to compromise the web server first before they could reach the database — this is why the DMZ concept exists.

**Step-by-step explanation:**
1. Separate subnets create separate broadcast domains
2. The firewall/router controls what crosses between them
3. NAT on the router hides internal addresses from the internet
4. The web server is in a "DMZ" (demilitarized zone) — accessible from outside but isolated from the internal network

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 | — | —/1 | — | — |
| Exercise 2 | — | —/1 | — | — |
| Exercise 3 | — | —/2 | — | — |
| Exercise 4 | — | —/2 | — | — |
| Exercise 5 | — | —/3 | — | — |
| **Total** | | **—/9** | | |

**Passing threshold:** 6/9 (67%). Aim for 8/9 (89%) before taking the test.
