# Systems Architecture — Cheat Sheet

> A living quick-reference. Add entries as you study. The goal is a document
> you'd actually open when making a design decision — not a glossary.

---

## Table of Contents

- [CAP Theorem](#cap-theorem)
- [Distributed Systems Patterns](#distributed-systems-patterns)
- [Messaging Delivery Semantics](#messaging-delivery-semantics)
- [Microservices Communication Patterns](#microservices-communication-patterns)
- [Data Consistency Patterns](#data-consistency-patterns)
- [Resilience Patterns](#resilience-patterns)
- [Observability Quick Reference](#observability-quick-reference)
- [Architecture Decision Checklist](#architecture-decision-checklist)

---

## CAP Theorem

The CAP theorem states that a distributed data store can guarantee **at most 2 of 3** properties simultaneously during a network partition:

| Property | Meaning | Practical implication |
|----------|---------|----------------------|
| **C — Consistency** | Every read returns the most recent write or an error | All nodes see the same data at the same time |
| **A — Availability** | Every request receives a non-error response | The system always responds, even with stale data |
| **P — Partition Tolerance** | System continues operating when messages between nodes are delayed or lost | Required in any real distributed system |

> [!IMPORTANT]
> In a real distributed network, **P is non-negotiable** — partitions happen. The real choice is: during a partition, do you prioritize **C (consistency)** or **A (availability)**?

### CAP Placement of Common Databases

| Database | CAP Class | Behavior During Partition |
|----------|-----------|--------------------------|
| Single-node PostgreSQL | CA | No partition (single node); no tolerance by definition |
| CockroachDB / Spanner | CP | Rejects writes that cannot achieve quorum |
| MongoDB (default write concern) | CP | Primary refuses writes; replica reads may be stale |
| Cassandra | AP | Accepts all writes; reconciles conflicts via last-write-wins |
| DynamoDB (eventually consistent) | AP | Accepts all writes; consistency is eventual |
| DynamoDB (strongly consistent reads) | CP for reads | Strong consistency with higher latency and cost |
| Redis Cluster | AP | Prefers availability; may lose recent writes on failover |
| etcd / ZooKeeper | CP | Rejects requests without a quorum |

### PACELC Extension

PACELC extends CAP to also consider the latency/consistency trade-off during **normal operation** (no partition):

```
If Partition → C or A?
Else (normal operation) → Latency or Consistency?
```

Example: DynamoDB is PA/EL — Available during partitions, Low latency (not strongly consistent) during normal operation.

---

## Distributed Systems Patterns

### Complete Pattern Reference Table

| Pattern | Problem | Solution | Trade-offs | When to Use |
|---------|---------|----------|-----------|-------------|
| **Saga (Choreography)** | Distributed transaction without 2PC | Each service publishes events; other services react | Hard to trace; no central view | Loose coupling between services; simple flows |
| **Saga (Orchestration)** | Distributed transaction without 2PC | Central orchestrator sends commands; tracks state | Orchestrator is a coupling point | Complex flows needing visibility; need central state |
| **Outbox Pattern** | Dual-write consistency | Write to DB + outbox table in one TX; relay publishes | Polling delay; extra table | Any time you need to publish events from a DB write |
| **CQRS** | Read/write scaling mismatch | Separate read model from write model | Eventual consistency; more code | High read:write ratio; need custom read projections |
| **Event Sourcing** | Audit trail; temporal queries | Store events, not state; derive state by replaying | Storage growth; query complexity | Audit requirements; need to replay/project events |
| **Circuit Breaker** | Cascading failures from slow services | Stop calling a failing service; fail fast | False trips; state machine overhead | Any synchronous service call to a potentially slow dependency |
| **Bulkhead** | Resource exhaustion from one path | Isolate resource pools per service/path | More infrastructure; configuration overhead | Multi-tenant systems; critical vs non-critical paths |
| **Retry with Backoff** | Transient network failures | Retry with exponential delay + jitter | Increased latency on failure path | Idempotent operations with transient failure modes |
| **Sidecar** | Cross-cutting concerns per service | Co-located proxy handles auth/tracing/retries | Latency per hop; more processes | Service mesh adoption; uniform cross-cutting concerns |
| **BFF** | Multiple clients need different API shapes | One BFF per client type (mobile, web, etc.) | Code duplication; synchronization overhead | Mobile vs web have substantially different data needs |
| **Strangler Fig** | Incremental monolith migration | New functionality in new services; old code strangled out | Long parallel operation; routing complexity | Migrating a live monolith without big-bang rewrite |
| **Sidecar + Service Mesh** | Uniform policy enforcement at network layer | All traffic through mesh; policy in control plane | Operational complexity; learning curve | Organizations with 10+ services; need uniform mTLS/observability |

---

## Messaging Delivery Semantics

| Semantic | Meaning | Risk | Best For |
|----------|---------|------|---------|
| **At-most-once** | Message delivered 0 or 1 times | Messages can be lost | Metrics, logs — loss acceptable |
| **At-least-once** | Message delivered 1+ times | Messages can be duplicated | Most business events with idempotent consumers |
| **Exactly-once** | Message delivered exactly 1 time | Hardest to achieve; requires idempotency at consumer | Financial transactions; anything where duplicates cause data corruption |

> [!NOTE]
> Exactly-once is often achieved via **at-least-once delivery + idempotent consumers** rather than true exactly-once transport. "True" exactly-once (Kafka Transactions) is available but adds latency and complexity.

### Kafka-Specific Quick Reference

```
Producer → Topic (partitioned) → Consumer Group
              │
              └── Each partition consumed by one consumer in a group
              └── Multiple consumer groups = independent processing
```

- **Offset**: position in a partition log; committed by consumer on successful processing
- **Consumer Group**: enables horizontal scaling; Kafka guarantees each partition to one consumer per group
- **Replication Factor**: how many broker copies; typical production: 3
- **`acks=all`**: wait for all in-sync replicas to acknowledge → durability guarantee

---

## Microservices Communication Patterns

### Sync vs Async Decision Matrix

| Situation | Sync (REST/gRPC) | Async (Events/Queues) |
|-----------|-----------------|----------------------|
| Need immediate response | ✓ | ✗ |
| Temporal decoupling needed | ✗ | ✓ |
| Publisher needs consumer result | ✓ | ✗ (use request-reply) |
| Multiple consumers need same event | ✗ (fan-out is complex) | ✓ (pub/sub) |
| High throughput, bursty load | ✗ | ✓ (queue acts as buffer) |
| Simple CRUD | ✓ | ✗ (overkill) |
| Cross-service transaction | ✗ (tight coupling) | ✓ (Saga) |

### gRPC vs REST for Internal Services

| Concern | gRPC | REST (JSON) |
|---------|------|-------------|
| Performance | Higher (binary Protobuf, HTTP/2 multiplexing) | Lower (text JSON, HTTP/1.1 or HTTP/2) |
| Schema enforcement | Strong (`.proto` contracts) | Weak (OpenAPI optional) |
| Code generation | Built-in | Optional (OpenAPI generators) |
| Browser support | Limited (needs grpc-web) | Native |
| Debugging | Harder (binary protocol) | Easy (curl, Postman) |
| Streaming | Native bidirectional streaming | Limited (SSE, WebSockets separate) |
| Best for | Internal service-to-service | Public APIs, browser clients |

---

## Data Consistency Patterns

### The Dual-Write Problem

```
Application
    │
    ├──► Database (write succeeds)
    │
    └──► Message Broker (CRASH — write fails)
         → Event never published
         → Downstream services never notified
         → DATA INCONSISTENCY
```

**Solutions in order of preference:**
1. **Outbox Pattern** — write both in one DB transaction; relay publishes
2. **Change Data Capture (CDC)** — Debezium reads DB WAL; publishes events
3. **Event Sourcing** — the event IS the source of truth; no dual-write

### Saga vs 2PC Comparison

| Property | Saga | Two-Phase Commit (2PC) |
|----------|------|----------------------|
| Blocking on failure | No (compensations run asynchronously) | Yes (participants block waiting for coordinator) |
| Consistency model | Eventual (intermediate states visible) | Strong (all-or-nothing) |
| Failure handling | Explicit compensating transactions | Coordinator-managed abort |
| Performance | High (no distributed lock) | Low (distributed lock held during prepare phase) |
| Complexity | High (must design compensations) | Medium (protocol is standard) |
| Coordinator crash | No global block | Can leave participants in uncertain state |
| Use when | Services are independent; eventual consistency acceptable | Strong consistency required; few participants |

---

## Resilience Patterns

### Circuit Breaker State Machine

```
           failures >= threshold
Closed ─────────────────────────► Open
  ▲                                  │
  │  probe succeeds                  │ cooldown expires
  │                                  ▼
  └─────────────────────────── Half-Open
         (sends one probe request)
```

### Retry Backoff Formula

```python
# Exponential backoff with jitter
import random

def backoff_delay(attempt: int, base: float = 1.0, max_delay: float = 60.0) -> float:
    # exponential: 1s, 2s, 4s, 8s, ...
    delay = min(base * (2 ** attempt), max_delay)
    # full jitter: random between 0 and delay
    return random.uniform(0, delay)
```

**Rule of thumb:** Always add jitter to prevent thundering herd (many clients retrying at the exact same moment).

---

## Observability Quick Reference

### The Three Pillars

| Pillar | What It Answers | Tools |
|--------|----------------|-------|
| **Metrics** | Is anything wrong right now? (aggregate numbers) | Prometheus, Datadog, CloudWatch |
| **Logs** | What happened? (discrete events with context) | ELK Stack, Loki, CloudWatch Logs |
| **Traces** | Where did the latency come from? (request path across services) | Jaeger, Zipkin, AWS X-Ray, Datadog APM |

### Distributed Trace Anatomy

```
TraceID: abc123
  └── Span: API-Gateway (200ms total)
        ├── Span: Order-Service (150ms)
        │     ├── Span: DB query (40ms)
        │     └── Span: Inventory-Service call (80ms)
        │           └── Span: DB query (30ms)
        └── Span: Auth check (20ms)
```

- **TraceID**: one per request, propagated in HTTP headers (`traceparent` in W3C standard)
- **SpanID**: one per operation within a trace
- **Parent SpanID**: links child spans to parent

### OpenTelemetry Trace Propagation Header (W3C)

```
traceparent: 00-{traceId}-{spanId}-{flags}
Example:
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
```

---

## Architecture Decision Checklist

Use this when evaluating any architectural option:

- [ ] **What problem does this solve?** — stated as a problem, not as "we want to use X"
- [ ] **What are the alternatives?** — at least 2 other options considered
- [ ] **What does this cost?** — operational complexity, learning curve, infrastructure, latency
- [ ] **What do we give up?** — the explicit trade-off stated
- [ ] **Is this reversible?** — one-way door or two-way door?
- [ ] **What is the failure mode?** — how does this break, and what happens when it does?
- [ ] **Who owns it?** — which team is responsible for this component?
- [ ] **How do we know if it's working?** — what metrics/alerts prove this is healthy?
