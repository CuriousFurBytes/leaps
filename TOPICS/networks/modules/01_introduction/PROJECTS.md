# Projects — Module 01: Introduction to Computer Networks

> These project ideas are specifically relevant to Module 01 concepts.
> For the full project list covering all modules, see the topic-level [PROJECTS.md](../../PROJECTS.md).

---

## Beginner Project: Network Topology Mapper

**Description:** Write a Python script that reads a list of IP addresses (or a CIDR range) and for each live host, uses `ping` (via `subprocess`) to measure RTT. Produce a simple text-based report showing which hosts are alive and their average ping RTT. This exercises your understanding of ICMP, IP addressing, and the distinction between "host unreachable" and "no ICMP response."

**Concepts from Module 01:**
- ICMP and how `ping` works
- IP addresses as Layer 3 identifiers
- The meaning of timeouts (host down vs. ICMP filtered)

**Estimated Time:** 2–3 hours

**Starting Point:** Use Python's `subprocess` module to invoke `ping`. Parse the output. The `ipaddress` standard library module helps iterate over CIDR ranges.

**Success Criteria:**
- [ ] Takes a CIDR block or list of IPs as input
- [ ] Correctly identifies alive vs. non-responding hosts
- [ ] Reports average RTT for alive hosts
- [ ] Handles timeout correctly (doesn't crash on non-responding hosts)
- [ ] The README of your project explains whether "no response" means the host is down

---

## Intermediate Project: OSI Layer Analyzer

**Description:** Load a sample `.pcap` file using Scapy and write a Python script that categorizes each packet by protocol at each OSI layer. Produce a summary table showing: what percentage of packets are Ethernet/IP/TCP vs. UDP vs. ICMP, the top 5 destination ports, and the top 3 source IP addresses by packet count.

**Concepts from Module 01:**
- OSI layer model and PDU names
- Encapsulation (each layer visible in the packet)
- Protocol identification at each layer

**Estimated Time:** 4–5 hours

**Starting Point:** Install Scapy (`pip install scapy`). Download a sample `.pcap` from the Wireshark sample captures page. Use `rdpcap()` to load it.

**Success Criteria:**
- [ ] Correctly identifies Ethernet, IP, TCP, UDP, ICMP layers in each packet
- [ ] Produces a protocol distribution table
- [ ] Lists top destination ports
- [ ] Code handles packets that don't have all layers (e.g., ARP packets have no IP header)

---

## Note on Full Capstone

The topic's full Capstone Project (Module 12) synthesizes concepts from all modules including this one. Module 01 concepts — topology design, device selection, layered architecture — appear directly in the capstone's network design phase.

See [Module 12: Capstone Project](../12_capstone-project/README.md) for the full brief.
