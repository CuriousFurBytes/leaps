# Module 12: Capstone Project — Secure Multi-Tier Network Architecture

[← Previous](../11_troubleshooting-and-tools/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-blue)
![Time](https://img.shields.io/badge/time-15h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Milestones](#milestones)
5. [Acceptance Criteria](#acceptance-criteria)
6. [Getting Unstuck](#getting-unstuck)
7. [Cross-Links](#cross-links)
8. [Submission Checklist](#submission-checklist)

---

## Overview

This is the capstone project for the Computer Networks topic. You will design, document, and partially implement a secure multi-tier network architecture for a fictional company. This project synthesizes concepts from every module in this topic.

> [!IMPORTANT]
> This project is **build-oriented**. The goal is to produce real artifacts that a
> professional network engineer would recognize as production-quality work.
> Resist the urge to look at hints before you've made a genuine attempt.
> The struggle is where the learning happens.

**What you will produce:**
1. A complete network architecture document with diagrams
2. Defined IP address plan with subnets for all segments
3. Firewall ruleset (iptables or equivalent)
4. DNS configuration for internal zones
5. A troubleshooting runbook for the 5 most likely failure scenarios
6. (Optional) Working implementation in GNS3 or Mininet

**What you will NOT find here:** a complete solution to copy. You will find hints, checkpoints, and references to earlier modules — but the design decisions are yours.

---

## Prerequisites

All 11 preceding modules should be complete or you should have studied equivalent material:
- Module 01: Introduction (network topologies, OSI model)
- Module 02: Physical and Data Link (Ethernet, VLANs)
- Module 03: IP Networking (subnetting, CIDR, routing)
- Module 04: Transport Layer (TCP/UDP, ports)
- Module 05: Application Layer (DNS, HTTP, TLS)
- Module 06: Routing Protocols (static routing)
- Module 08: Network Security (firewalls, DMZ concept)
- Module 11: Troubleshooting (diagnostic tools for runbook)

---

## Project Brief

**Fictional company: Acme Technologies**

Acme Technologies is a software company with 50 employees at a single office. They run their own infrastructure (not fully cloud-based). You are the network engineer designing their network from scratch.

**Business requirements:**
1. 50 employees need internet access and access to internal services
2. A public web application (company website + customer portal) must be accessible from the internet on ports 80 and 443
3. A PostgreSQL database server must be accessible from the web application but NOT directly from the internet
4. An internal Git server must be accessible only to employees (not public internet)
5. A management interface must exist for network equipment — accessible only by the IT team
6. All employee workstations must use DHCP
7. All internal DNS names should resolve without contacting public DNS

**Technical constraints:**
- You have been allocated the public IP range `203.0.113.0/29` (documentation range; use this for the exercise)
- Use RFC 1918 private space for all internal addresses
- The design must survive the failure of any single device

---

## Milestones

Work through these milestones in order. Each builds on the previous.

### Milestone 1: IP Address Plan

Design an IP address plan that satisfies all the business requirements.

**Deliverable:** A table showing:
- All network segments (at minimum: DMZ, employee LAN, server LAN, management)
- The subnet (CIDR notation) assigned to each segment
- The gateway address for each subnet
- The number of usable hosts and whether that's sufficient

**Questions to answer:**
- Why did you choose the prefix length you chose for each segment?
- Why did you separate the DMZ from the employee LAN?
- What would happen if you put the web server and the database on the same subnet?

---

### Milestone 2: Network Diagram

Draw a network topology diagram showing:
- All network segments
- All key devices (firewall/router, switches, servers, DHCP server)
- IP addresses of all devices and interfaces
- The internet connection

You may use Mermaid, ASCII art, or a diagram tool (draw.io, Lucidchart). The diagram must be included in your project submission (as a Mermaid block in this file or as a linked image).

---

### Milestone 3: Firewall Ruleset

Design the complete firewall ruleset for the perimeter firewall and any internal firewalls.

**For each rule, document:**
- Source (IP/subnet or "any")
- Destination (IP/subnet or "any")
- Port/protocol
- Action (ALLOW/DENY)
- Justification (why is this rule needed?)

**Required policies:**
- Employees can reach the internet (HTTP/HTTPS/DNS)
- External users can reach the web server (ports 80, 443)
- Web server can reach the database server (port 5432)
- Employees can reach the internal Git server (port 22, 443)
- ONLY the IT management subnet can SSH to network equipment
- Everything else: default deny

Express the rules as iptables commands or as a structured table.

---

### Milestone 4: DNS Configuration

Design the internal DNS infrastructure:

- Choose a private domain name for internal use (e.g., `acme.internal`)
- Define DNS records for: web server, database server, git server, default gateway, DHCP server
- Specify: which DNS server employees use, how it handles external queries (forwarder vs. recursive)

**Deliverable:** A BIND9 zone file stub or equivalent configuration showing your A records.

---

### Milestone 5: Troubleshooting Runbook

Write a troubleshooting runbook for the 5 most likely failure scenarios. For each scenario:

1. **Name:** Short description of the symptom
2. **Probable causes:** List 3–5 likely root causes
3. **Diagnostic steps:** Step-by-step commands to identify the root cause
4. **Resolution:** How to fix each probable cause

**Required scenarios to cover:**
1. "Employees cannot access the internet"
2. "External users report the company website is unreachable"
3. "The web application cannot connect to the database"
4. "DNS resolution is failing for internal names"
5. "Slow network performance for file transfers between segments"

---

### Milestone 6 (Optional): Working Implementation

Implement your design in GNS3, Mininet, or using Docker containers with iptables rules. Demonstrate that:
- Employee workstations can reach the internet
- External traffic reaches the web server (ports 80/443)
- The database is not directly reachable from outside

---

## Acceptance Criteria

Your project is complete when:

- [ ] IP address plan table is complete with all segments, CIDRs, gateways, and justifications
- [ ] Network diagram shows all segments, devices, IPs, and connections
- [ ] Firewall ruleset has at least 10 rules covering all 6 required policies
- [ ] Each firewall rule has a written justification
- [ ] DNS zone file contains at least 5 A records for internal hosts
- [ ] Troubleshooting runbook covers all 5 required scenarios with diagnostic commands
- [ ] You can explain every design decision out loud without consulting notes
- [ ] Design would survive the failure of any single device (redundancy addressed)

---

## Getting Unstuck

> [!NOTE]
> These hints are here so you can get past a specific blocker and keep going on your own.
> Do not read ahead. Work through each milestone first, then use hints only when truly stuck.

<details>
<summary>Hint: IP Address Plan — What segments should I create?</summary>

A typical multi-tier design has at least these segments:
- **DMZ (Demilitarized Zone):** where public-facing servers live (web server). Accessible from internet, but isolated from internal network.
- **Internal LAN:** where employee workstations and printers live. Internet access yes; direct inbound from internet: no.
- **Server LAN:** where the database server and Git server live. Not accessible from internet; accessible from web server (DB) and employees (Git).
- **Management LAN:** for IT team access to routers, switches, firewalls. Very restricted access — even employees can't reach it normally.

See [[networks/modules/03_ip-networking]] for CIDR subnetting help.

</details>

<details>
<summary>Hint: Firewall Ruleset — Where do I start?</summary>

Start with the principle of **default deny**: assume everything is blocked, then add allow rules for what you explicitly need.

Work through each communication path one by one:
1. What needs to come IN from the internet? → web server ports 80/443 only
2. What needs to go OUT from the DMZ? → web server → database (port 5432)
3. What do employees need to reach? → internet (HTTP/HTTPS/DNS), internal Git server
4. What should the management network allow? → SSH to all network devices, only from management subnet

See [[networks/modules/08_network-security]] for iptables syntax and firewall design principles.

</details>

<details>
<summary>Hint: DNS — Internal vs. external resolution</summary>

Your internal DNS server needs to handle two types of queries:
1. Internal names (acme.internal) → answer from local zone file
2. External names (google.com) → forward to an upstream resolver (e.g., 8.8.8.8)

A split-horizon DNS setup serves internal hosts from an internal zone and external hosts from a public zone. For this project, a simple forward resolver with a local zone for `acme.internal` is sufficient.

See [[networks/modules/05_application-layer]] for DNS zone structure.

</details>

<details>
<summary>Hint: Troubleshooting Runbook — Structure of a good runbook entry</summary>

A useful runbook entry looks like this:

```
## Scenario: Web application cannot connect to database

Symptom: Application returns "could not connect to server: Connection refused"

Probable causes:
1. Database service is not running
2. Firewall blocking port 5432 between DMZ and Server LAN
3. Database not listening on the correct interface
4. Wrong DB hostname/IP in application config

Diagnostic steps:
# From web server:
1. nc -zv db.acme.internal 5432    # Is port reachable?
2. ping db.acme.internal           # Is host reachable at Layer 3?

# From database server:
3. ss -tlnp | grep 5432            # Is PostgreSQL running and listening?
4. iptables -L -n | grep 5432      # Any local firewall rules?

# On firewall:
5. iptables -L FORWARD -v -n | grep -E '5432|dmz_subnet'

Resolution:
- If step 1 fails but step 2 succeeds → firewall blocking; update iptables rule
- If step 3 shows no listener → start PostgreSQL service
```

See [[networks/modules/11_troubleshooting-and-tools]] for the full troubleshooting methodology.

</details>

---

## Cross-Links

- [[networks/modules/01_introduction]] — network topologies used in the architecture
- [[networks/modules/02_physical-and-datalink]] — VLANs for segment isolation on physical switches
- [[networks/modules/03_ip-networking]] — IP address planning, subnetting, routing table design
- [[networks/modules/05_application-layer]] — DNS configuration for internal zones
- [[networks/modules/08_network-security]] — firewall design, DMZ concept, defense in depth
- [[networks/modules/11_troubleshooting-and-tools]] — tools for the troubleshooting runbook
- [[devops-platform-engineering]] — cloud equivalent: VPCs, security groups, and ALBs
- [[pentesting-security]] — test your design against real attack scenarios

---

## Submission Checklist

When you've completed the project, verify:

- [ ] IP address plan — all segments, CIDRs, gateways
- [ ] Network diagram — all devices, connections, IPs
- [ ] Firewall ruleset — all 6 required policies covered, each rule justified
- [ ] DNS zone file — at least 5 internal A records
- [ ] Troubleshooting runbook — 5 scenarios with diagnostic steps and resolutions
- [ ] Can explain every design decision without consulting notes
- [ ] Record your completion in the topic-level [PROGRESS.md](../../PROGRESS.md)
- [ ] Add your project to the topic-level [README.md](../../README.md) Projects table
