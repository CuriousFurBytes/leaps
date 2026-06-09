# Module 03: Async Patterns

[← Module 02: Messaging and Queues](../02_messaging-and-queues/README.md) | [Topic Home](../../README.md) | [Next → Module 04: Microservices Fundamentals](../04_microservices-fundamentals/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-8h-orange)

> The Saga pattern (choreography and orchestration), the Outbox pattern, event sourcing, CQRS, and process managers — the patterns that make distributed workflows reliable and auditable.

---

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

---

## Overview

Once you have message brokers, you can build asynchronous workflows. But async workflows spanning multiple services introduce a critical problem: how do you coordinate a multi-step business operation when each step runs in a different service, with no shared transaction? How do you roll back a hotel booking when the car rental step fails — three services and two asynchronous messages later?

This module covers the patterns that solve this problem. The **Saga pattern** is the primary mechanism for managing distributed "transactions" without two-phase commit. **Choreography sagas** use events and reactive services; **orchestration sagas** use a central coordinator. Both have advantages and trade-offs, and knowing when to choose each is a key architectural skill.

The **Outbox pattern** solves a lower-level problem: the dual-write problem — how do you atomically publish an event to a message broker *and* write to a database in the same operation? Without the Outbox, you risk publishing events that your database didn't commit, or committing database changes that never trigger downstream events.

**Event sourcing** and **CQRS** are patterns that go deeper: instead of storing current state, you store the sequence of events that *led to* the current state. This gives you a complete audit trail, the ability to replay events to rebuild state, and the natural separation of read and write models.

---

## Prerequisites

- Module 01: Introduction to Distributed Systems — distributed transactions, complexity tax
- Module 02: Messaging and Queues — message brokers, delivery semantics, topics
- Basic Python programming

---

## Objectives

By the end of this module, you will be able to:

1. Implement a Saga using the choreography style, designing the event flow and compensating transactions
2. Implement a Saga using the orchestration style, with an explicit state machine
3. Implement the Outbox pattern to solve the dual-write problem
4. Explain event sourcing and its trade-offs compared to state-based persistence
5. Design a CQRS architecture with separate read and write models
6. Identify when each pattern is appropriate and when it is over-engineering

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a subsequent pass.
> The Objectives above define the scope. The Key Concepts below provide a vocabulary reference.

### Core Concepts to Cover

**The Saga Pattern:**
A Saga is a sequence of local transactions that together accomplish a distributed business operation. Each local transaction updates its service's database and publishes a message or event. If one step fails, the saga executes compensating transactions for all previously completed steps.

Two implementation styles:
- **Choreography:** Services react to events and publish their own events. No central coordinator. Loose coupling, but hard to track overall saga state. Good for simple flows.
- **Orchestration:** A dedicated orchestrator service sends commands to participants and tracks state. Easier to reason about, but the orchestrator is a coupling point.

```python
# Choreography saga: Order Service listens for PaymentFailed and cancels order
# Each service knows its role in the saga via the events it handles

class OrderService:
    def on_order_created(self, order: Order) -> None:
        # Step 1: Order created, trigger payment
        self.db.save(order)
        self.events.publish("PaymentRequested", {
            "order_id": order.id,
            "amount": order.total
        })

    def on_payment_failed(self, event: dict) -> None:
        # Compensating transaction: cancel the order
        order = self.db.get(event["order_id"])
        order.status = "CANCELLED"
        self.db.save(order)
        self.events.publish("OrderCancelled", {"order_id": order.id})
```

**The Outbox Pattern:**
Write to the database and the outbox table in one transaction. A relay process publishes from the outbox. Guarantees at-least-once event publishing without distributed transactions.

```python
# Outbox pattern: single database transaction covers both business data and event
def create_order(order_data: dict) -> Order:
    with db.transaction():
        order = Order(**order_data)
        db.save(order)
        # Outbox row in the same transaction — atomically linked
        db.save(OutboxMessage(
            event_type="OrderCreated",
            payload=order.to_json(),
            status="PENDING"
        ))
    # A separate relay process reads PENDING outbox rows and publishes them
    return order
```

**Event Sourcing:**
Store events, not current state. Derive current state by replaying events. Provides audit trail, temporal queries, and event replay.

```python
# Event sourced account balance
events = [
    AccountOpened(amount=0),
    MoneyDeposited(amount=100),
    MoneyWithdrawn(amount=30),
    MoneyDeposited(amount=50),
]

def current_balance(events: list) -> float:
    balance = 0.0
    for event in events:
        if isinstance(event, MoneyDeposited):
            balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            balance -= event.amount
    return balance  # 120.0
```

**CQRS:**
Separate the write model (handles commands, validates business rules, persists to command store) from the read model (optimized views, pre-computed joins, possibly different storage).

---

## Key Concepts

**Saga:** A pattern for distributed transactions composed of a sequence of local transactions with compensating transactions for rollback. No distributed lock is held.

**Compensating transaction:** A business-level semantic undo for a previously committed local transaction. Distinct from a database rollback — it must be explicitly designed. See [[shared/glossary#compensating-transaction]].

**Choreography (saga):** Saga coordination via events — each service reacts to events and produces events. No central coordinator. More decoupled, harder to trace.

**Orchestration (saga):** Saga coordination via a dedicated orchestrator that sends commands and tracks state. More visible, creates coupling to orchestrator.

**Outbox pattern:** Pattern for reliable message publishing: write business data and outbox record in one DB transaction; a relay publishes from the outbox. See [[shared/glossary#outbox-pattern]].

**Event sourcing:** Persistence strategy where entity state is derived from an immutable sequence of events rather than stored directly. See [[shared/glossary#event-sourcing]].

**CQRS:** Command Query Responsibility Segregation — separate read and write models. Write model enforces business rules; read model is optimized for query performance. See [[shared/glossary#cqrs]].

**Process manager:** A stateful object that coordinates a multi-step process, routing messages between services based on current state. Similar to an orchestrator but more general — handles long-running, non-linear workflows.

---

## Examples

> Full worked examples to be written. Planned examples:
> 1. Complete choreography saga for a 3-step booking system (with compensating transactions)
> 2. Complete orchestration saga with state machine and persistence
> 3. Outbox relay process with idempotency
> 4. Event-sourced bank account with snapshot optimization

---

## Common Pitfalls

**Pitfall 1: Forgetting compensating transactions for all steps.**
Every step in a saga needs an explicitly designed compensating transaction. A saga where step 3 has no compensation is a saga that leaves the system in an inconsistent state when step 4 fails.

**Pitfall 2: Using choreography for complex flows.**
Choreography works well for 2–3 steps. For 5+ steps with conditional branches and retries, the event flow becomes very hard to trace. Orchestration is almost always better for complex flows — the coupling cost is worth the visibility.

**Pitfall 3: Event sourcing as the default.**
Event sourcing adds significant complexity: snapshot management, event schema evolution, projection rebuilding time. It should only be used when audit trail, temporal query, or event replay requirements genuinely justify the added complexity.

---

## Cross-Links

- [[systems-architecture/modules/02_messaging-and-queues]] — Message brokers are the infrastructure sagas and outbox patterns run on
- [[systems-architecture/modules/06_data-consistency]] — Distributed transactions and the dual-write problem in full depth
- [[systems-architecture/modules/12_capstone-project]] — The capstone requires designing a complete async workflow using patterns from this module
- [[postgresql#transactions]] — The ACID transaction that makes the Outbox pattern atomically safe

---

## Summary

- The Saga pattern manages distributed transactions without 2PC: a sequence of local transactions with explicit compensating transactions for rollback.
- Choreography sagas use events and reactive services — more decoupled, harder to debug at scale.
- Orchestration sagas use a central coordinator — more visible, creates coupling to orchestrator.
- The Outbox pattern solves the dual-write problem by writing to the database and outbox table in one transaction, with a relay publishing from the outbox.
- Event sourcing stores events, not state — enabling audit trails, replay, and temporal queries at the cost of query complexity and snapshot management.
- CQRS separates write and read models, allowing each to be optimized independently, at the cost of eventual consistency between them.
- Process managers coordinate long-running, stateful, multi-step workflows that don't fit the Saga's linear structure.
