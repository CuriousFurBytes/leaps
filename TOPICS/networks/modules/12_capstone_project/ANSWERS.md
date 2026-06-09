# Answers: Module 12 — Capstone Project

## Answer Key

### Easy Questions
**Q1:** A host is a device or virtual machine that sends or receives network traffic.
**Q2:** A packet is a unit of data plus headers used to move information through a network.
**Q3:** `dig` or `nslookup`.
**Q4:** A route describes where traffic for a destination network should be sent next.
**Q5:** A protocol is a shared rule set for message format and behavior.

### Medium Questions
**Q6:** A web request depends on DNS, routing, transport, TLS, and application behavior; failure in any one can produce the same user symptom.
**Q7:** An IP address identifies a host or interface location; a port identifies a service or conversation endpoint on a host.
**Q8:** Layers isolate responsibilities so tests can target one kind of failure at a time.
**Q9:** Reachability means packets can get to a host; application health means the intended service is listening and responding correctly.
**Q10:** Standardization let heterogeneous machines interoperate without sharing one vendor or implementation.

### Hard Questions
**Q11:** A good answer includes commands such as `dig example.com`, `ping -c 3 example.com`, and `curl -Iv https://example.com`.
**Q12:** The host may be reachable while the service is stopped, blocked by a firewall, listening on another port, or returning an application error.
**Q13:** A correct answer uses `socket.create_connection(("example.com", 80), timeout=...)` or equivalent.
**Q14:** Local subnet traffic may still work; off-subnet or Internet traffic likely fails because the host has no next hop for remote destinations.

### Expert Questions
**Q15:** A strong answer separates user context, DNS, local configuration, path, transport, TLS, service, and recent changes with evidence for each step.
**Q16:** A strong answer maps signals to layers: DNS response codes and latency, route/path changes, packet loss, TCP failures, TLS errors, HTTP status, and application metrics.

### Bonus Questions
**Bonus 1:** Any real relevant RFC or standard with a clear explanation of interoperability earns credit.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
