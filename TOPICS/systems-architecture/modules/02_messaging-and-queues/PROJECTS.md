# Projects: Module 02 — Messaging and Queues

> See the topic-level [PROJECTS.md](../../PROJECTS.md) for larger multi-module projects.

---

## Project A: Kafka Producer/Consumer Pipeline

**Difficulty:** Intermediate
**Time estimate:** 4–5 hours

**Brief:**
Using Docker Compose to run a local Kafka cluster (single broker for simplicity), implement:
1. A producer that generates fake order events (random OrderCreated JSON messages) at 10 events/second
2. Two consumers in different consumer groups: one for inventory reservation, one for email notification
3. A dead-letter queue that captures messages that fail processing more than 3 times
4. A simple monitoring script that prints consumer lag every 5 seconds

**Acceptance Criteria:**
- Both consumers receive every event independently
- DLQ captures failed messages (simulate by throwing an exception in 5% of messages)
- Lag monitor shows lag decrease as consumers catch up after a simulated slowdown

---

## Project B: Delivery Semantics Comparison

**Difficulty:** Beginner
**Time estimate:** 2–3 hours

**Brief:**
Using Python and a simple in-memory queue (or SQLite as a simple persistent queue), implement three versions of a message consumer demonstrating each delivery semantic:
1. At-most-once: acknowledge before processing
2. At-least-once: acknowledge after processing
3. Idempotent at-least-once: acknowledge after processing, skip if already processed (deduplication table)

Simulate broker crashes and consumer crashes and show how each semantic behaves.
