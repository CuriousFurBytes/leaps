# Distributed Systems Architecture

> Queueing, async systems, microservices, and the engineering judgment needed to design reliable distributed systems.

## Table of Contents
1. [Why Learn Distributed Systems Architecture?](#why-learn-distributed-systems-architecture)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)
6. [How to Use This Topic](#how-to-use-this-topic)

## Why Learn Distributed Systems Architecture?
Distributed systems are what happen when one computer is no longer enough or when independent teams need independent deployment. The moment work crosses a process, machine, region, queue, or organization boundary, architecture becomes an engineering discipline: failures are normal, latency is variable, and correctness depends on protocols as much as code.

Queueing and async design are central because most production systems do not process every request immediately. They absorb bursts, schedule work, move data between services, and protect fragile dependencies. Without queueing theory and backpressure, a fast-looking system can become unstable precisely when demand rises.

Microservices are not a goal by themselves. They are a way to align software boundaries with team ownership, deployability, reliability requirements, and domain change. This topic teaches when distributed architecture helps, when it hurts, and how experienced engineers reason about tradeoffs rather than cargo-culting patterns.

## Prerequisites
- Basic programming in one language, especially functions, data structures, and error handling.
- Basic command-line usage and comfort reading logs.
- Introductory networking concepts such as HTTP, TCP, latency, and DNS.
- Helpful but not required: [[postgresql]], [[go]], [[devops-platform-engineering]], and [[devops-platform-engineering]].

## Module Map
| # | Module | Difficulty | Focus | Status |
|---|--------|------------|-------|--------|
| 01 | [Foundations of Distributed Systems](./modules/01_foundations/) | Beginner | Mental models, boundaries, latency, failure | [ ] |
| 02 | [Queueing and Backpressure](./modules/02_queueing_and_backpressure/) | Beginner | Queues, capacity, Little’s Law, overload control | [ ] |
| 03 | [Async Execution and Messaging](./modules/03_async_execution_and_messaging/) | Intermediate | Event loops, promises, brokers, delivery semantics | [ ] |
| 04 | Microservice Boundaries and APIs | Intermediate | Service ownership, contracts, REST, RPC, schemas | [ ] |
| 05 | State, Consistency, and Transactions | Intermediate | Consistency models, sagas, idempotency | [ ] |
| 06 | Resilience Patterns | Advanced | Timeouts, retries, circuit breakers, bulkheads | [ ] |
| 07 | Observability and Operations | Advanced | Logs, metrics, traces, SLOs, incident response | [ ] |
| 08 | Performance and Capacity Engineering | Advanced | Load testing, capacity planning, tuning | [ ] |
| 09 | Data-Intensive Architectures | Advanced | Streams, caches, replication, storage tradeoffs | [ ] |
| 10 | Platform, Deployment, and Governance | Expert | Kubernetes, service meshes, versioning, policy | [ ] |
| 11 | Architecture Review and Evolution | Expert | ADR practice, migrations, socio-technical design | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/) | Expert | Design, build, and evaluate a production-shaped system | [ ] |

## Cross-Links
- [[devops-platform-engineering]] — broader interview and design framing for distributed systems.
- [[postgresql]] — storage, transactions, replication, and consistency.
- [[devops-platform-engineering]] — deployment substrates and managed infrastructure.
- [[go]] — testing, maintainability, team practice, and delivery.

## Quick Reference
| Concept | Practical Question | Default Starting Point |
|---|---|---|
| Queue | Can work wait safely? | Use a durable queue for asynchronous, retryable work. |
| Backpressure | What happens when consumers are slower than producers? | Bound queues, shed load, or slow producers deliberately. |
| Microservice | Does this boundary need independent ownership and deployment? | Start coarse; split only when coupling evidence demands it. |
| Idempotency | Can retrying the same operation cause harm? | Attach operation IDs and make repeated commands safe. |
| Timeout | How long should a caller wait? | Set explicit deadlines based on user value and dependency SLOs. |
| Observability | Can operators explain behavior from outside the process? | Emit logs, metrics, and traces with correlation IDs. |

```python
# A tiny capacity sketch: Little's Law says L = λW.
arrival_rate_per_second = 50
average_wait_seconds = 0.2
items_in_system = arrival_rate_per_second * average_wait_seconds
print(f"Expected in-flight work: {items_in_system:.1f}")
```

## How to Use This Topic
Work through Modules 01–03 first; they establish the mental models used by the rest of the roadmap. Later modules can be built as the topic expands, but the final capstone should remain last because it requires synthesis across queueing, asynchronous messaging, service boundaries, resilience, observability, and operational review.
