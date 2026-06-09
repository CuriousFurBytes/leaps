# Systems Architecture

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> A comprehensive curriculum covering distributed systems fundamentals, asynchronous patterns, microservices design, and the trade-offs every architect must understand to build systems that scale without breaking.

> [!NOTE]
> **Topic Overview**
> Systems Architecture covers the full spectrum of concerns in designing software systems that run across multiple machines, communicate asynchronously, and must remain reliable despite partial failures. This is the discipline that separates engineers who can build features from engineers who can build infrastructure that supports millions of users.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty & Time Estimate](#difficulty--time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Quick Reference](#quick-reference)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

Systems Architecture is the discipline of designing software systems at the level above individual applications — deciding how services communicate, where data lives, how failures are handled, and what trade-offs are acceptable for a given problem. It is the domain where engineering decisions have the largest and longest-lasting consequences.

A distributed system is any system where components run on separate machines and communicate over a network. This definition is deceptively simple: the moment you add a second machine, you inherit an entirely new class of problems. Networks partition. Clocks drift. Processes crash. Operations that were trivially atomic on a single machine become coordination nightmares. The core challenge of systems architecture is not adding features — it is managing the inherent complexity that distribution introduces.

This topic is deliberately nuanced. Monoliths are not inherently bad. Microservices are not inherently good. The right architecture for a 5-person startup is almost certainly wrong for a 500-person engineering organization, and vice versa. The goal of this curriculum is not to teach you a set of rules to follow but to build the judgment to make the right call in context.

### Why It Matters

Every production application above a certain scale is a distributed system, whether intentionally designed as one or not. A web application talking to a database is already distributed. Add a cache, a background job processor, and a third-party payment provider, and you have a multi-node system with all the associated failure modes.

Understanding systems architecture is valuable because:

- It underpins every backend engineering role at scale — distributed systems knowledge is the single largest distinguishing factor between junior and senior backend engineers
- It develops the mental model for reasoning about failure — a skill that transfers directly to reliability engineering, platform engineering, and technical leadership
- Proficiency in it is expected in roles such as Senior Software Engineer, Staff Engineer, Solution Architect, and Site Reliability Engineer

### Key Features of This Topic

- **Trade-off focused** — every pattern is presented with its costs, not just its benefits
- **Historically grounded** — concepts are explained in the context of the real problems that motivated them
- **Pattern-oriented** — industry-standard patterns (Saga, Outbox, Circuit Breaker, CQRS) taught at the level of understanding, not just recognition
- **Diagram-heavy** — Mermaid architecture diagrams and sequence diagrams throughout to build visual intuition

---

## Historical Context

The discipline of distributed systems grew from a fundamental tension: single machines have physical limits, but users' demands for data and compute are unbounded.

### Timeline

| Year | Event |
|------|-------|
| 1960s–1970s | Mainframe era — centralized compute, terminals as thin clients. All logic and data on one machine |
| 1978 | Leslie Lamport publishes "Time, Clocks, and the Ordering of Events in a Distributed System" — foundational theory for reasoning about distributed state |
| 1990s | Client-server architecture dominates — application logic split between fat clients and database servers. Early web stacks are 2-tier or 3-tier monoliths |
| 2000 | Eric Brewer presents the CAP conjecture at PODC; formally proven by Gilbert and Lynch in 2002 |
| 2003–2004 | Google publishes the GFS, MapReduce, and Bigtable papers — foundational for modern distributed data systems |
| 2007 | Amazon's Dynamo paper published — describes a highly available key-value store and makes the AP trade-off explicit |
| 2008–2012 | Netflix, Amazon, and Uber begin migrating from monoliths to microservices, driven by deployment and scaling pain |
| 2010 | Netflix publishes Chaos Monkey — systematized chaos engineering enters the industry |
| 2011 | Martin Fowler and James Lewis articulate the microservices architectural style and popularize bounded contexts |
| 2014–2016 | Docker and Kubernetes reshape service deployment; containers make microservice operational complexity more tractable |
| 2016–2018 | Linkerd (first service mesh) released; Istio follows — the service mesh era begins |
| 2022+ | Modular monolith renaissance — teams that over-decomposed begin consolidating; Shopify, Stack Overflow publish retrospectives |
| Today | Edge computing, serverless, and eBPF-based networking continue to reshape architectural options |

---

## Real-World Applications

Systems Architecture principles are applied across every technology company:

- **Netflix** — Migrated from a monolithic DVD-rental application to hundreds of microservices 2009–2015. Pioneered chaos engineering, circuit breakers (Hystrix), and resilience patterns that became industry standards
- **Amazon** — Jeff Bezos's "API mandate" in 2002 forced all internal systems to communicate only through service interfaces; AWS is the product of Amazon externalizing its internal infrastructure services
- **Uber** — Moved from a monolith to microservices circa 2014, then to a "domain-oriented microservice architecture" (DOMA) circa 2019 to manage the coordination complexity of thousands of services
- **Shopify** — Deliberately chose a modular monolith over microservices, citing operational and coordination overhead; their "pods" architecture partitions data and compute while keeping a unified codebase
- **Discord** — Uses a mix of Go, Rust, and Elixir/Erlang services based on problem characteristics; their engineering blog is a primary source for real-world trade-off documentation
- **LinkedIn** — Invented Apache Kafka as an internal solution to high-throughput event streaming; open-sourced it in 2011 where it became the dominant distributed log

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the CAP theorem, the PACELC model, and why distributed consistency is fundamentally different from single-machine consistency
2. Design messaging topologies using appropriate delivery semantics (at-most-once, at-least-once, exactly-once) for a given use case
3. Apply the Saga pattern (choreography and orchestration variants), the Outbox pattern, and CQRS to distributed data problems
4. Decompose a monolithic application into microservices using bounded contexts from Domain-Driven Design, with justified service boundary decisions
5. Implement resilience patterns — circuit breaker, bulkhead, retry with exponential backoff — and explain when each is appropriate
6. Design an observability strategy for a distributed system using distributed tracing, structured logging, and metrics aggregation
7. Conduct architecture decision-making using ADRs, trade-off analysis frameworks, and evolutionary architecture principles
8. Build and document a complete distributed system design for a realistic use case, including service decomposition, data ownership, messaging topology, and failure modes

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Advanced → Expert |
| **Estimated Total Hours** | 80–100 hours |
| **Prerequisites** | Programming experience (any language), basic HTTP/networking, basic databases |
| **Recommended Pace** | 6–8 hours/week over 12–16 weeks |
| **Topic Type** | Mixed (Theoretical foundations + Practical patterns + Design exercises) |
| **Suitable For** | Backend engineers with 1+ years experience, software architects, engineering leads |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- [[networks]] — specifically: HTTP request/response lifecycle, TCP vs UDP, DNS basics, what a network packet is
- [[postgresql]] — specifically: transactions (ACID properties), what a database is, basic SQL, why databases are not just file storage
- [[devops-platform-engineering]] — specifically: what a container is, what a load balancer does, basic deployment concepts

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If terms like "network partition", "database transaction", or "HTTP" are entirely foreign, revisit the prerequisites above first.
> If you can follow along but things feel shaky, press on — it will solidify.

---

## Learning Modules

| # | Module | Topic | Status | Score |
|---|--------|-------|--------|-------|
| 01 | [Introduction to Distributed Systems](./modules/01_introduction/) | Fallacies, CAP theorem, monolith vs microservices, sync vs async | - [ ] | —/— |
| 02 | [Messaging and Queues](./modules/02_messaging-and-queues/) | Kafka, RabbitMQ, pub/sub, delivery semantics, consumer groups | - [ ] | —/— |
| 03 | [Async Patterns](./modules/03_async-patterns/) | Saga, Outbox, event sourcing, CQRS, process managers | - [ ] | —/— |
| 04 | [Microservices Fundamentals](./modules/04_microservices-fundamentals/) | Bounded contexts, DDD, decomposition strategies, inter-service comms | - [ ] | —/— |
| 05 | [Microservices Patterns](./modules/05_microservices-patterns/) | Circuit breaker, bulkhead, retry, sidecar, service mesh | - [ ] | —/— |
| 06 | [Data Consistency](./modules/06_data-consistency/) | Distributed transactions, Saga vs 2PC, dual-write problem, CDC | - [ ] | —/— |
| 07 | [API Design for Services](./modules/07_api-design-for-services/) | BFF pattern, API composition, gRPC vs REST, versioning | - [ ] | —/— |
| 08 | [Observability in Distributed Systems](./modules/08_observability-distributed/) | Distributed tracing, OpenTelemetry, correlation IDs, structured logging | - [ ] | —/— |
| 09 | [Resilience and Chaos Engineering](./modules/09_resilience-and-chaos/) | Chaos Monkey, failure injection, graceful degradation, SLOs | - [ ] | —/— |
| 10 | [Scaling Patterns](./modules/10_scaling-patterns/) | Horizontal scaling, sharding, CQRS read replicas, CDN, rate limiting | - [ ] | —/— |
| 11 | [Architecture Decision-Making](./modules/11_architecture-decision-making/) | ADRs, trade-off analysis, tech debt quantification, evolutionary architecture | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Design a complete distributed system: e-commerce, ride-sharing, or social platform | - [ ] | —/— |

**Status key:** ` ` Not started &nbsp;·&nbsp; `~` In progress &nbsp;·&nbsp; `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 12 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 60 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **624** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to Distributed Systems)
- [ ] **Foundation Built** — Complete Modules 01–03 with ≥ 70% on each test
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Patterns Expert** — Score ≥ 80% on all Modules 02–06 tests
- [ ] **Architect's Eye** — Complete at least one architecture design project
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Deep Work** — Complete the Capstone Project with documented ADRs
- [ ] **Chaos Practitioner** — Score 100% on Module 09 (Resilience and Chaos)

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% &nbsp;·&nbsp; B ≥ 80% &nbsp;·&nbsp; C ≥ 70% &nbsp;·&nbsp; D ≥ 60% &nbsp;·&nbsp; F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for Systems Architecture:

- [[networks]] — Network fundamentals are the physical substrate on which all distributed systems run; understanding TCP/IP, latency, and network topologies is essential
- [[devops-platform-engineering]] — Container orchestration, CI/CD, and infrastructure automation are how distributed systems are deployed and operated
- [[graphql-rest]] — API design for service-to-service and client-to-service communication; REST and GraphQL are the dominant protocols for synchronous service calls
- [[postgresql]] — Understanding database transactions, ACID properties, and replication is required for reasoning about data consistency in distributed systems
- [[feature-flags-monitoring]] — Feature flags enable safe rollout of architectural changes; monitoring and alerting are the operational complement to observability design

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Quick Reference

### CAP Theorem Cheat Sheet

| System | C | A | P | Notes |
|--------|---|---|---|-------|
| Single-node PostgreSQL | ✓ | ✓ | ✗ | No partition tolerance — single point of failure |
| MongoDB (default write concern) | ✓ | ✗ | ✓ | CP: prefers consistency over availability during partitions |
| Cassandra | ✗ | ✓ | ✓ | AP: prefers availability; eventual consistency |
| CockroachDB | ✓ | ~ | ✓ | CP with high availability via multi-region replication |
| DynamoDB | ~ | ✓ | ✓ | AP by default; strongly consistent reads available |

### Distributed Systems Patterns Quick Reference

| Pattern | Problem It Solves | Key Trade-off |
|---------|------------------|---------------|
| Saga (Choreography) | Distributed transactions without 2PC | Harder to debug; no central coordinator |
| Saga (Orchestration) | Distributed transactions without 2PC | Central coordinator = single point of coupling |
| Outbox Pattern | Dual-write problem between DB and message broker | Requires polling or CDC; adds latency |
| CQRS | Read/write scalability mismatch | Eventual consistency between read and write models |
| Event Sourcing | Audit log, temporal queries, event replay | Increased storage; query complexity |
| Circuit Breaker | Cascading failures | Added latency on state transitions; false trips |
| Bulkhead | Resource exhaustion from one failing service | Increases infrastructure footprint |
| Sidecar | Cross-cutting concerns (auth, tracing, retries) | Added per-service latency and memory |
| BFF | Client-specific API shapes | Duplicated API surface; more code to maintain |
| Strangler Fig | Incremental monolith migration | Long-lived parallel systems; routing complexity |

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Started Topic

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed prerequisites

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "systems-architecture"
topic_name: "Systems Architecture"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 624
completion_percentage: 0
difficulty: "Advanced → Expert"
estimated_hours: 90
prerequisites:
  - "networks"
  - "postgresql"
  - "devops-platform-engineering"
related_topics:
  - "networks"
  - "devops-platform-engineering"
  - "graphql-rest"
  - "postgresql"
  - "feature-flags-monitoring"
tags:
  - "distributed-systems"
  - "microservices"
  - "backend"
  - "architecture"
  - "queues"
  - "async"
creator: "Community"
year_created: "2026"
```
