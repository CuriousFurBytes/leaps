# Module 01: Introduction to Networks

> This module builds the first mental model of packets, hosts, links, protocols, and practical network diagnostics.

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

## Overview
Networks exist because useful computing rarely happens on one isolated machine. A network lets hosts exchange messages over shared rules so that humans can browse websites, applications can call APIs, backups can move off-device, and monitoring systems can observe services.

This module focuses on network foundations. It uses small commands and plain-language diagrams so you can connect vocabulary to observable behavior. The goal is to make the invisible visible: names become addresses, data becomes packets, and failures become testable hypotheses.

## Prerequisites
- None; this is the first module.
- Basic comfort with a terminal.
- Curiosity about how operating systems and distributed systems communicate.

## Objectives
By the end of this module, you will be able to:
- Explain the purpose of basic reachability in practical network communication.
- Use basic diagnostic commands to gather evidence.
- Distinguish host, link, network, transport, and application concerns.
- Read simple network examples without treating them as magic.
- Prepare for Module 02: Layered Models and Encapsulation.

## Theory
### Why Networks Are Layered Systems
Early computer networks were built to connect different machines without requiring every application to understand every cable, radio, router, and host implementation. The Internet Protocol family grew from research networks such as ARPANET into a global system by standardizing narrow contracts: addresses identify endpoints or networks, routing moves packets toward destinations, transport protocols coordinate conversations, and applications define useful meaning.

The important lesson is that a network is not one protocol. It is a stack of agreements. Each agreement hides some details and exposes others. This is why a browser can request a page without knowing the voltage on an Ethernet cable, while a switch can forward frames without understanding HTTP.

### Observing a Network
A practical learner should test before guessing. The following commands ask three different questions: can a name become an address, can packets reach a target, and what path seems to be used?

```bash
# Resolve a domain name to addresses.
dig example.com

# Send three ICMP echo requests to test basic reachability.
ping -c 3 example.com

# Show likely router hops toward the destination.
traceroute example.com
```

### Packets, Addresses, and Services
Applications exchange data, but networks carry packets. A packet has headers that describe delivery information and a payload that contains the next layer's data. Addressing and ports let one physical host run many services at once.

```python
# A minimal TCP client that shows a service is identified by host and port.
import socket

with socket.create_connection(("example.com", 80), timeout=5) as conn:
    conn.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    print(conn.recv(200).decode("iso-8859-1"))
```

### From Mental Model to Troubleshooting
Good troubleshooting follows the path of a message. If name resolution fails, routing may be irrelevant. If packets cannot leave the local subnet, the default gateway matters. If TCP connects but the application returns an error, the network path may be healthy while the service is not.

```bash
# Split a web failure into DNS, TCP/TLS, and HTTP observations.
dig example.com
curl -Iv https://example.com
ss -t state established
```

## Key Concepts
- **Host:** A device or virtual machine that sends or receives network traffic. A host may have multiple interfaces and addresses.
- **Packet:** A unit of data plus headers used for delivery decisions. Packet headers make troubleshooting possible because they expose source, destination, and protocol clues.
- **Protocol:** A shared rule set for communication. Protocols work because both sides agree on message format and behavior.
- **Interface:** A network attachment point such as an Ethernet port, Wi-Fi adapter, loopback device, or virtual cloud interface.
- **Route:** A forwarding decision that tells a host or router where to send traffic for a destination network.

## Examples
### Scenario: Check Local Network State
Use this when a host cannot reach a service and you need basic facts before changing configuration.

```bash
# Show addresses, interfaces, and routes on a Linux host.
ip addr
ip route
ss -tulpen
```

The commands reveal whether the host has an address, a default route, and listening services. They do not prove the remote service is correct, but they prevent blind debugging.

### Scenario: Explain a Web Request
A simple web request combines name resolution, routing, transport, security, and application behavior.

```bash
# Verbose output separates connection setup from HTTP response details.
curl -v https://example.com/
```

The tradeoff is noise: verbose output can be long. Read it in phases: DNS result, connection attempt, TLS negotiation, request, and response.

## Common Pitfalls
### Pitfall 1: Treating every failure as a network outage
Wrong approach:

```bash
# This only says the HTTP request failed; it does not identify the layer.
curl https://internal.example.test
```

Correct approach:

```bash
# Test name resolution, reachability, and application behavior separately.
dig internal.example.test
ping -c 3 internal.example.test
curl -Iv https://internal.example.test
```

The mistake happens because users experience one symptom. Engineers need layered evidence.

### Pitfall 2: Confusing an address with a service
Wrong approach:

```bash
# A reachable host does not prove the web service is listening.
ping -c 3 192.0.2.10
```

Correct approach:

```bash
# Test the specific service port.
curl -Iv http://192.0.2.10:8080
```

Reachability and service readiness are related but different facts.

### Pitfall 3: Skipping the local host
Wrong approach:

```bash
# Immediately blaming the remote network can waste time.
traceroute api.example.test
```

Correct approach:

```bash
# First confirm the local host has an address and route.
ip addr
ip route
```

Many incidents begin with local configuration, not distant routers.

## Cross-Links
- [[networks]]
- [[devops-platform-engineering]]
- [[postgresql]]
- [[javascript-typescript-react]]

## Summary
- Networks connect hosts through shared protocols and layered responsibilities.
- Packets carry headers that make delivery and troubleshooting possible.
- Names, addresses, routes, ports, and protocols answer different questions.
- Diagnostic commands are strongest when used to test one hypothesis at a time.
- The next module deepens this model by explaining encapsulation and protocol layers.
