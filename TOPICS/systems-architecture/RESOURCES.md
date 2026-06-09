# Systems Architecture — Resources

> [!WARNING]
> **Verified resources only.** Every entry in this file must be something you have
> personally confirmed exists, is accessible, and is genuinely useful.
> Do not add resources based on hearsay, AI suggestions, or titles that "sound right."
> A short list of excellent resources beats a long list of unverified ones.

---

## Books

| Title | Author | Level | Format | Notes |
|-------|--------|-------|--------|-------|
| Designing Data-Intensive Applications | Martin Kleppmann | Intermediate–Advanced | Print/eBook (O'Reilly) | The definitive text on distributed data systems. Covers replication, partitioning, transactions, consistency, and consensus with depth and clarity. Required reading for this topic. |
| Building Microservices (2nd ed.) | Sam Newman | Intermediate | Print/eBook (O'Reilly) | The most comprehensive guide to microservices in practice. Covers decomposition, communication, deployment, and organizational concerns. Highly practical. |
| [Verify: "The Architecture of Open Source Applications" — confirm current URL at aosabook.org] | Various | Intermediate–Advanced | Free online | Case studies of real architectures (nginx, SQLite, etc.). Valuable for seeing how trade-offs play out in real systems. |
| Release It! (2nd ed.) | Michael T. Nygard | Advanced | Print/eBook (Pragmatic) | Covers stability patterns (circuit breakers, bulkheads, timeouts) from the perspective of production experience. Originated the circuit breaker pattern description. |
| [Verify: "Fundamentals of Software Architecture" by Mark Richards and Neal Ford — confirm publisher] | Mark Richards, Neal Ford | Intermediate | Print/eBook (O'Reilly) | Covers architectural styles including microservices, event-driven, and layered architectures with trade-off analysis. |

_Use ISBN or direct publisher links where possible to avoid linking to pirated copies._

---

## Foundational Papers

| Title | Authors | Year | Notes |
|-------|---------|------|-------|
| [Verify: "Dynamo: Amazon's Highly Available Key-value Store" — available on ACM Digital Library] | DeCandia et al. | 2007 | Describes Amazon's internal Dynamo system; introduced consistent hashing, vector clocks, and made AP trade-offs explicit. Essential context for the CAP theorem in practice. |
| [Verify: "MapReduce: Simplified Data Processing on Large Clusters" — available on USENIX] | Dean, Ghemawat | 2004 | Google's MapReduce paper. Foundational for batch distributed processing. |
| [Verify: "Bigtable: A Distributed Storage System for Structured Data" — available on USENIX] | Chang et al. | 2006 | Google's Bigtable paper. Influential for wide-column store design. |
| [Verify: "Time, Clocks, and the Ordering of Events in a Distributed System" — available on ACM] | Lamport | 1978 | The foundational paper on logical clocks and causality in distributed systems. |

---

## Blogs and Articles

_Verify each link is live before adding it permanently. Note the date you verified it._

- **[Netflix Tech Blog](https://netflixtechblog.com)** — Primary source for Netflix's migration stories, Chaos Monkey origins, and resilience patterns. Verified 2026-06-09.
- **[Martin Fowler's website](https://martinfowler.com)** — Articles on microservices, event sourcing, CQRS, bounded contexts, and evolutionary architecture by one of the field's most articulate writers. Verified 2026-06-09.
- **[High Scalability](http://highscalability.com)** — Case studies of real-world architectures at scale. Verified 2026-06-09.
- **[Discord Engineering Blog](https://discord.com/category/engineering)** — Detailed, honest write-ups about Discord's technology choices and migration decisions. Verified 2026-06-09.
- **[Uber Engineering Blog](https://www.uber.com/blog/engineering/)** — Documents Uber's domain-oriented microservice architecture (DOMA) and other large-scale architectural patterns. Verified 2026-06-09.

---

## Tools and Technologies Covered in This Topic

| Tool / Technology | Purpose | Official Docs |
|-------------------|---------|---------------|
| Apache Kafka | Distributed event streaming | [kafka.apache.org](https://kafka.apache.org/documentation/) |
| RabbitMQ | Message broker | [rabbitmq.com/docs](https://www.rabbitmq.com/docs) |
| Istio | Service mesh | [istio.io/docs](https://istio.io/latest/docs/) |
| Linkerd | Service mesh (lightweight) | [linkerd.io/docs](https://linkerd.io/2.15/overview/) |
| OpenTelemetry | Observability instrumentation standard | [opentelemetry.io](https://opentelemetry.io/docs/) |
| Jaeger | Distributed tracing backend | [jaegertracing.io](https://www.jaegertracing.io/docs/) |
| gRPC | High-performance RPC framework | [grpc.io/docs](https://grpc.io/docs/) |

---

## Communities

| Community | Platform | Focus |
|-----------|----------|-------|
| r/softwarearchitecture | Reddit | General architecture discussion |
| r/microservices | Reddit | Microservices-specific questions |
| CNCF Slack | Slack | Cloud-native / Kubernetes / service mesh community |
| Stack Overflow [distributed-systems tag] | Stack Overflow | Technical Q&A |

---

## My Recommendations

_Fill in as you progress — what actually helped you most?_

### Best for Absolute Beginners to Distributed Systems
> _To be filled in_

### Best for Building Mental Models
> _To be filled in — likely: Designing Data-Intensive Applications, Chapters 1 and 5_

### Best for Practical / Hands-On Learning
> _To be filled in_

### Best Deep Reference
> _To be filled in_

---

## Resources to Evaluate

_Drop links here when you find something but haven't verified it yet._

- [ ] Sam Newman's "Monolith to Microservices" — companion to Building Microservices, focused on migration strategies; needs URL verification
- [ ] Chris Richardson's microservices.io pattern catalog — comprehensive pattern reference; needs URL verification
