# Computer Networks — Projects

> Project-based learning cements knowledge in a way that reading and exercises alone cannot.
> Building something real forces you to confront gaps in your understanding and make decisions
> that tutorials never put in front of you.

---

## How to Use This File

1. Choose a project at or slightly above your current level.
2. **Don't use tutorials for your chosen project.** Tutorials are for learning, projects are for applying.
3. Document your attempt using the [Project Attempt Template](#project-attempt-template) at the bottom.
4. When you finish, link the result (repo, demo) in the table in the topic README.

---

## Beginner Projects

_Focus: get comfortable with core networking tools and vocabulary._
_Complete at least one before advancing past Phase 1._

### B1: Network Scanner

**Description:** Write a Python script that takes a CIDR block (e.g. `192.168.1.0/24`) as input and discovers which hosts are online by sending ICMP echo requests or attempting TCP connections to port 80. Print a list of responsive hosts with their IP addresses.

**Concepts Reinforced:**
- IP addressing and CIDR notation (Module 03)
- Socket programming basics (Module 10)
- Network scanning methodology (Module 11)

**Estimated Time:** 3–4 hours

**Starting Point:** Blank Python file; use the `socket` and `ipaddress` standard library modules.

**Success Criteria:**
- [ ] Accepts a CIDR block as a command-line argument
- [ ] Correctly iterates over all host addresses in the range
- [ ] Reports which hosts responded within a configurable timeout
- [ ] The script runs without errors on your local network

---

### B2: Subnet Calculator

**Description:** Build a command-line tool that takes an IP address and prefix length and outputs: network address, broadcast address, first usable host, last usable host, number of usable hosts, and subnet mask in dotted-decimal notation.

**Concepts Reinforced:**
- IPv4 addressing and subnetting (Module 03)
- CIDR notation
- Binary arithmetic for networking

**Estimated Time:** 2–3 hours

**Starting Point:** Blank Python file. Try implementing the bit manipulation yourself before using `ipaddress`.

**Success Criteria:**
- [ ] Handles any valid IPv4 prefix length (/1 through /30)
- [ ] Correctly computes all six output fields
- [ ] Handles edge cases: /31 (point-to-point) and /32 (host route)

---

### B3: HTTP Client from Scratch

**Description:** Write a Python program that opens a raw TCP socket to a web server and sends a manually crafted HTTP/1.1 GET request. Parse and display the response status code and headers. Do not use `urllib`, `requests`, or `httplib` — only `socket`.

**Concepts Reinforced:**
- TCP socket programming (Module 10)
- HTTP/1.1 protocol format (Module 05)
- Application layer over transport layer

**Estimated Time:** 3–4 hours

**Starting Point:** Blank Python file; `socket` standard library only.

**Success Criteria:**
- [ ] Successfully connects to any HTTP (not HTTPS) server
- [ ] Sends a valid HTTP/1.1 GET request with required headers (Host, Connection)
- [ ] Receives and displays the full response headers
- [ ] Can retrieve the HTML content of a simple page

---

## Intermediate Projects

_Focus: combine multiple concepts, handle real-world complexity._
_Complete at least one before completing Phase 2._

### I1: TCP Echo Server and Client

**Description:** Implement a multi-client TCP echo server in Python. The server accepts multiple simultaneous connections (use threading or `select`), echoes back whatever the client sends, and logs connections/disconnections with timestamps. Write a matching client that reads lines from stdin and sends them to the server.

**Concepts Reinforced:**
- TCP socket programming and connection lifecycle (Module 10)
- Concurrent connection handling
- Network protocol design
- Transport layer semantics (Module 04)

**Estimated Time:** 5–7 hours

**Starting Point:** Blank Python file; `socket`, `threading`, `select` standard library modules.

**Success Criteria:**
- [ ] Server handles at least 5 simultaneous clients without blocking
- [ ] Gracefully handles client disconnection (no crash on broken pipe)
- [ ] Logs each connection/disconnection with IP, port, and timestamp
- [ ] Client reads from stdin and sends each line to the server
- [ ] Code is clean, readable, and commented

---

### I2: DNS Resolver

**Description:** Implement a stub DNS resolver in Python that constructs a DNS query packet from scratch (binary format), sends it over UDP to a configured resolver, parses the binary response, and returns A records. Do not use any DNS libraries — build the packet manually using the DNS wire format from RFC 1035.

**Concepts Reinforced:**
- DNS protocol and resolution process (Module 05)
- UDP socket programming (Module 10)
- Binary protocol parsing
- RFC reading skills

**Estimated Time:** 6–9 hours

**Starting Point:** Read RFC 1035 Section 3 (message format) before writing any code.

**Success Criteria:**
- [ ] Constructs a valid DNS query in binary wire format
- [ ] Sends query via UDP and receives response
- [ ] Parses the response and extracts A records (IPv4 addresses)
- [ ] Works for common domains (google.com, github.com, etc.)
- [ ] Handles NXDOMAIN (non-existent domain) gracefully

---

### I3: Network Traffic Analyzer

**Description:** Use Python and the `scapy` library to capture live network packets (or read a `.pcap` file), and produce a summary report showing: top source/destination IP pairs by packet count, protocol distribution (TCP/UDP/ICMP), and the top 10 destination ports.

**Concepts Reinforced:**
- Packet structure and encapsulation (Modules 02–04)
- Protocol identification and parsing
- Network troubleshooting methodology (Module 11)

**Estimated Time:** 4–6 hours

**Starting Point:** Install `scapy`. Start by loading a sample `.pcap` file rather than live capture.

**Success Criteria:**
- [ ] Correctly identifies and counts packets by protocol
- [ ] Produces a readable summary table
- [ ] Works on both live capture and `.pcap` files
- [ ] Handles malformed or truncated packets without crashing

---

## Advanced Projects

_Focus: tackle realistic, open-ended problems. No hand-holding._
_Complete at least one to reach Applied Practitioner status._

### A1: Simple Load Balancer

**Description:** Implement a TCP load balancer in Python that listens on a frontend port and distributes connections across multiple backend servers using round-robin. Track connection counts per backend and implement a health check that removes unresponsive backends from rotation.

**Why This Is Hard:**
You must handle bidirectional data relay (client↔balancer↔backend), connection lifecycle, backend health state, and concurrent connections — all without a framework.

**Concepts Reinforced:**
- TCP connection handling and data relay (Modules 04, 10)
- Concurrent programming for network services
- Health checking and failure detection
- Load balancing algorithms
- Practical socket programming under constraints

**Estimated Time:** 12–16 hours

**Starting Point:** Start with a single-backend TCP proxy, then add multiple backends, then add health checks.

**Success Criteria:**
- [ ] Distributes connections across at least 3 configured backends
- [ ] Correctly relays data in both directions without data loss
- [ ] Removes a backend from rotation when its health check fails
- [ ] Re-adds a backend when it becomes healthy again
- [ ] Handles at least 10 simultaneous client connections
- [ ] You can explain every design decision you made

---

### A2: Firewall Rules Simulator

**Description:** Design and implement a packet filter that reads rules from a YAML configuration file and applies them to packets from a pcap file. Rules specify match criteria (source/destination IP, port, protocol) and actions (ALLOW, DENY, LOG). Output which packets were allowed/denied and why.

**Why This Is Hard:** You must design a rule language, parse binary packets, implement rule matching in order (first-match semantics), and handle the distinction between stateless and stateful matching.

**Concepts Reinforced:**
- Network security and firewall design (Module 08)
- Packet parsing across layers 2–4
- Policy configuration and rule evaluation
- Stateless vs. stateful filtering concepts

**Estimated Time:** 8–12 hours

**Success Criteria:**
- [ ] YAML rule format is clearly documented
- [ ] Processes a pcap file and outputs per-packet decisions
- [ ] Implements at least: src/dst IP matching, port matching, protocol matching
- [ ] First-match semantics: the first matching rule wins
- [ ] Includes a default-deny rule at the end

---

## Expert / Capstone Projects

_Focus: synthesize everything. Build something you're proud to show others._
_Complete one to earn Topic Mastery status._

### E1: Secure Multi-Tier Network Architecture

**Description:** Design and document a complete, secure multi-tier network architecture for a fictional company. This is the same project covered in detail in Module 12 (Capstone).

**Why This Is a Capstone:**
This project requires mastery of all major topic areas. You cannot complete it with gaps —
they will surface quickly. Expect to revisit earlier modules during the build.

**Core Requirements:**
- [ ] Uses concepts from at least 8 different modules
- [ ] Is non-trivial in scope (not achievable in a single sitting)
- [ ] Is documented clearly enough that someone else could understand it
- [ ] Includes a write-up explaining your design decisions and what you learned
- [ ] Network diagram shows DMZ, internal, and management segments with all IP ranges
- [ ] Firewall ruleset is documented and justified
- [ ] Includes a troubleshooting runbook for the 5 most likely failure scenarios

**Estimated Time:** 10–15 hours

**Extension Ideas (if you want more challenge):**
- Implement the design in GNS3 or Mininet and demonstrate it working
- Add IPv6 dual-stack support throughout
- Write a Python script to validate the firewall rules against a set of test cases

> [!NOTE]
> The final module of this topic is a dedicated **Capstone Project** module that walks you
> through building this for real. It gives you a brief, milestones, and a **Help / Getting
> Unstuck** section with staged hints — but it deliberately does **not** hand you a finished
> solution. The help is there so you can get past a blocker and keep going on your own, not so
> you can skip the build. Struggling productively *is* the learning here.

---

## Project Attempt Template

When you attempt a project, create a folder in this topic's directory and copy this template:

```markdown
# Project: {{PROJECT_NAME}}

**Difficulty:** Beginner / Intermediate / Advanced / Expert
**Started:** {{YYYY-MM-DD}}
**Completed:** {{YYYY-MM-DD}} (or "In progress")
**Time Spent:** {{HOURS}} hours

## What I Built

{{DESCRIPTION_OF_WHAT_YOU_ACTUALLY_BUILT}}

## Link / Location

{{LINK_TO_REPO_OR_FILE}}

## What I Learned

- {{LEARNING_1}}
- {{LEARNING_2}}
- {{LEARNING_3}}

## What Was Hard

{{WHAT_WAS_CHALLENGING_AND_HOW_YOU_SOLVED_IT}}

## What I'd Do Differently

{{HONEST_RETROSPECTIVE}}

## Concepts Used

- [[networks/modules/01_introduction]] — how you used it
- [[networks/modules/02_physical-and-datalink]] — how you used it

## Score / Self-Assessment

On a scale of 1–5, how well do I think I executed this project? {{SCORE}}/5

Justification: {{JUSTIFICATION}}
```
