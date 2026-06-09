# Systems Architecture — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of Systems Architecture.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use.
```

Keep definitions in your own words as much as possible. If you're copying from a source, add attribution.

---

## B

### bounded context

**Definition:** A bounded context is an explicit boundary within which a domain model applies consistently. Within a bounded context, all terms, concepts, and rules have a single, unambiguous meaning. Across contexts, the same word can mean different things. Introduced by Eric Evans in Domain-Driven Design.

**Also known as:** service boundary, domain boundary

**Related:** [[domain-driven-design]], [[microservices-fundamentals]]

**Example:**
In an e-commerce system, "customer" means different things to the billing service (a payer with a payment method) and the shipping service (a recipient with an address). Each service maintains its own bounded context with its own Customer model.

---

### bulkhead

**Definition:** A resilience pattern borrowed from ship design: isolate resources (thread pools, connection pools, memory) so that a failure in one service cannot exhaust shared resources and cascade to unrelated services. Named after the watertight compartments in a ship hull.

**Also known as:** bulkhead isolation, resource isolation

**Related:** [[circuit-breaker]], [[resilience-patterns]]

**Example:**
Instead of one shared HTTP connection pool for all downstream services, give each service its own pool of 20 connections. If Service A becomes slow and fills its 20-connection pool, Services B and C are unaffected.

---

## C

### CAP theorem

**Definition:** A theorem in distributed systems stating that a distributed data store can guarantee at most two of the following three properties simultaneously: Consistency (every read gets the most recent write), Availability (every request receives a response), and Partition Tolerance (the system continues to operate when network messages are delayed or lost). Proposed by Eric Brewer in 2000, formally proven by Gilbert and Lynch in 2002.

**Also known as:** Brewer's theorem

**Related:** [[eventual-consistency]], [[pacelc-model]]

**Example:**
During a network partition, a CP system (like MongoDB with default settings) will reject writes to maintain consistency. An AP system (like Cassandra) will accept writes and reconcile conflicts later, sacrificing consistency for availability.

---

### circuit breaker

**Definition:** A resilience pattern that monitors calls to a downstream service and, when a failure threshold is reached, "opens" the circuit to stop sending requests for a cooldown period. After the cooldown, it sends a probe request ("half-open" state); if successful, the circuit closes. If not, it opens again. Prevents cascading failures by fast-failing rather than queueing and timing out.

**Also known as:** circuit breaker pattern

**Related:** [[bulkhead]], [[retry-pattern]], [[resilience4j]]

**Example:**
A payment service calls a fraud-detection service. If 5 of the last 10 calls fail, the circuit opens and all payment requests immediately return a "degraded" response (skip fraud check) for 30 seconds instead of waiting for timeouts.

---

### compensating transaction

**Definition:** In the Saga pattern, a compensating transaction is a semantic undo: a business-level operation that reverses the effect of a previously committed transaction. Unlike database rollbacks, compensating transactions are not automatic — they must be explicitly designed and implemented.

**Also known as:** compensating action, semantic rollback

**Related:** [[saga-pattern]], [[distributed-transactions]]

**Example:**
In a travel booking saga: book flight → book hotel → book car. If "book car" fails, the compensating transaction for "book flight" is "cancel flight" and for "book hotel" is "cancel hotel reservation". Each step has its own compensation.

---

### CQRS

**Definition:** Command Query Responsibility Segregation — an architectural pattern that separates the model used to handle write operations (Commands) from the model used to handle read operations (Queries). This allows the read side to be optimized independently (e.g., pre-computed views, different storage engines, separate scaling).

**Also known as:** Command Query Responsibility Segregation

**Related:** [[event-sourcing]], [[read-replica]], [[eventual-consistency]]

**Example:**
An order service writes orders through a Command model that validates business rules and persists to PostgreSQL. The read side maintains a denormalized, pre-joined view in Redis, updated asynchronously from domain events. Read performance is milliseconds; write performance involves proper validation.

---

## D

### data mesh

**Definition:** An organizational and architectural approach to data infrastructure in which data ownership is decentralized to domain teams, who treat their data as a product. Each domain exposes its data through standardized interfaces. A shift from centralized data lakes/warehouses to a federated model. Proposed by Zhamak Dehghani.

**Also known as:** federated data architecture

**Related:** [[domain-driven-design]], [[event-sourcing]], [[bounded-context]]

**Example:**
Instead of a central data engineering team owning all pipelines, the Orders team owns and publishes an "orders data product" via a standardized API. The Analytics team subscribes to it. The Orders team is responsible for quality, schema evolution, and SLAs.

---

## E

### eventual consistency

**Definition:** A consistency model where, given no new updates are made, all replicas of data will eventually converge to the same value. Does not guarantee that all readers see the same data at any given instant — only that they will agree eventually. The dominant consistency model in AP distributed systems.

**Also known as:** BASE (Basically Available, Soft-state, Eventually consistent)

**Related:** [[CAP-theorem]], [[CQRS]], [[conflict-resolution]]

**Example:**
After an update to a user profile in Cassandra, two replicas may briefly show different values. Within milliseconds to seconds (depending on replication settings), all replicas converge. Any read during this window might see either the old or new value.

---

### event sourcing

**Definition:** A pattern where the state of an entity is not stored directly but derived from an ordered sequence of immutable events. Instead of saving "current state = X", you store "event1 happened, then event2, then event3" and replay them to compute current state. Provides a complete audit log and enables temporal queries.

**Also known as:** event store pattern

**Related:** [[CQRS]], [[outbox-pattern]], [[saga-pattern]]

**Example:**
Instead of storing `account.balance = 100`, you store events: `AccountOpened(initial=0)`, `MoneyDeposited(amount=150)`, `MoneyWithdrawn(amount=50)`. Current balance is computed by replaying. You can also query "what was the balance on any past date?".

---

## I

### idempotency key

**Definition:** A client-generated unique identifier included with a request that allows the server to detect and safely ignore duplicate requests. If the same request is retried (due to network failure or timeout), the server can recognize it has already processed that request and return the original result without processing it again.

**Also known as:** idempotency token, deduplication key

**Related:** [[at-least-once-delivery]], [[exactly-once-semantics]]

**Example:**
A mobile app sends `POST /payments` with header `Idempotency-Key: order-789-attempt-1`. If the network drops before the response arrives, the app retries with the same key. The server checks its idempotency log, finds it already processed this request, and returns the original response without charging the customer twice.

---

## O

### outbox pattern

**Definition:** A pattern for reliable message publishing that solves the dual-write problem. Instead of writing to a database AND sending a message to a broker in the same operation (which can fail atomically), you write to a local "outbox" table in the same database transaction, then a separate process reads from the outbox and publishes to the broker. Guarantees at-least-once delivery without distributed transactions.

**Also known as:** transactional outbox

**Related:** [[dual-write-problem]], [[change-data-capture]], [[saga-pattern]]

**Example:**
Order service commits `INSERT orders (...)` and `INSERT outbox (event='OrderCreated', payload='{...}')` in one transaction. A background process reads the outbox and publishes `OrderCreated` to Kafka, then marks the outbox row as processed.

---

## S

### saga pattern

**Definition:** A pattern for managing distributed transactions across multiple services without using two-phase commit (2PC). A saga is a sequence of local transactions, each of which publishes events or sends messages that trigger the next step. If any step fails, compensating transactions are executed for all completed steps to undo the work.

**Also known as:** choreography saga, orchestration saga

**Related:** [[compensating-transaction]], [[outbox-pattern]], [[distributed-transactions]]

**Example:**
Order fulfillment saga: (1) Reserve inventory, (2) Charge payment, (3) Create shipment. If "Charge payment" fails, the saga executes: (1b) Release inventory reservation. No distributed lock is held; each step commits locally and publishes an event.

---

### service mesh

**Definition:** An infrastructure layer for service-to-service communication in a microservices architecture. Typically implemented as a network of sidecar proxies (e.g., Envoy) deployed alongside each service instance. The mesh handles cross-cutting concerns: mTLS, load balancing, circuit breaking, retry logic, observability, and traffic management — without requiring changes to application code.

**Also known as:** sidecar mesh, service mesh infrastructure

**Related:** [[sidecar-proxy]], [[istio]], [[linkerd]]

**Example:**
With Istio installed, every pod has an Envoy sidecar. When Service A calls Service B, the call goes through A's sidecar, which enforces mTLS, collects trace data, applies circuit-breaking rules, and retries failed requests — all transparently, without Service A's code knowing.

---

### sidecar proxy

**Definition:** A sidecar proxy is a process co-located with a service instance (e.g., in the same Kubernetes pod) that intercepts all inbound and outbound network traffic. It implements cross-cutting concerns — authentication, traffic shaping, observability, retry — so the main service doesn't have to. The "sidecar" metaphor comes from a motorcycle sidecar attached to the main vehicle.

**Also known as:** sidecar pattern, proxy sidecar

**Related:** [[service-mesh]], [[envoy-proxy]]

**Example:**
Envoy sidecar injected by Istio: all HTTP calls from a Python service go through the local Envoy process on port 15001. Envoy adds distributed trace headers, enforces circuit breaking, and records metrics — invisible to the Python code.

---

## T

### two-phase commit

**Definition:** A distributed transaction protocol (2PC) in which a coordinator manages a two-phase process: (1) Prepare — all participants signal they are ready to commit; (2) Commit — coordinator tells all participants to commit. If any participant fails to prepare, the coordinator sends Abort to all. Guarantees atomicity across multiple resources but is blocking (coordinator failure can leave participants in an uncertain state) and introduces high latency.

**Also known as:** 2PC, XA transactions

**Related:** [[saga-pattern]], [[distributed-transactions]], [[CAP-theorem]]

**Example:**
A banking transaction that debits account A and credits account B across two database shards. 2PC asks both shards "ready to commit?", then either "commit" or "abort" based on all responses. If the coordinator crashes after Prepare but before Commit, both shards are stuck in a locked prepared state.

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
