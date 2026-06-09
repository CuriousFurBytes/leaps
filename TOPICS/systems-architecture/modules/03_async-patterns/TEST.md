# Test: Module 03 — Async Patterns

**Instructions:** Answer all questions.

**Total Points:** 37 pts
**Bonus Available:** 5 pts

> [!NOTE]
> Full test questions will be written when Module 03 README is completed.

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is a compensating transaction and how does it differ from a database rollback?

> Answer:

**Q2.** Name the two styles of Saga pattern implementation.

> Answer:

**Q3.** What problem does the Outbox pattern solve?

> Answer:

**Q4.** In event sourcing, how is current state derived?

> Answer:

**Q5.** What does CQRS stand for and what does it separate?

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Compare choreography and orchestration sagas. Give one advantage and one disadvantage of each.

> Answer:

**Q7.** Explain the dual-write problem and why it leads to data inconsistency.

> Answer:

**Q8.** A saga for a travel booking completes steps 1 (flight reserved) and 2 (hotel booked) successfully, but step 3 (car rental) fails. What must happen next and in what order?

> Answer:

**Q9.** What are the main trade-offs of event sourcing vs. state-based persistence?

> Answer:

**Q10.** Why does CQRS usually result in eventual consistency between the read and write models?

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Implement the core of a choreography saga for order fulfillment (inventory → payment → shipping). Show the events published and the compensating logic for each service.



> Answer:

**Q12.** Implement a Python class OutboxRelay that reads pending outbox rows and publishes them to a mock broker, handling failures idempotently.



> Answer:

**Q13.** Debug: An orchestration saga always retries step 2 even after it has succeeded. Identify at least 2 possible causes and how to fix each.

> Answer:

**Q14.** Design the event schema and projection logic for a CQRS read model that shows "orders with total > 00 placed by a given customer in the last 30 days".

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a complete saga (orchestration style) for an insurance claim processing workflow with at least 5 steps, including: state machine diagram, compensating transactions, idempotency handling, and timeout/retry strategy.

> Answer:

**Q16.** Event sourcing and CQRS are often used together. Explain the synergies and the additional complexities this combination introduces, including event schema versioning, projection rebuilding time, and eventual consistency observability.

> Answer:

---

## Bonus

**Bonus 1.** (+5 pts) The "process manager" pattern is sometimes confused with the orchestration saga. Explain the key difference and give an example where a process manager is more appropriate than a saga.

> Answer: