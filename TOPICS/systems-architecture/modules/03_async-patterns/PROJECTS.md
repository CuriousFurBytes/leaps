# Projects: Module 03 — Async Patterns

> See the topic-level [PROJECTS.md](../../PROJECTS.md) for Project 5 (Saga Orchestrator Design) which directly applies this module.

---

## Module Project: Choreography Saga for Hotel Booking

**Difficulty:** Intermediate
**Time estimate:** 4–5 hours

**Brief:**
Implement a choreography saga in Python for a hotel booking system with three steps:
1. Reserve room (HotelService)
2. Charge credit card (PaymentService)
3. Send confirmation email (NotificationService)

Each step must:
- Be triggered by an event from the previous step
- Publish its own success or failure event
- Have an explicit compensating transaction

Simulate failures at each step and verify correct rollback behavior.

**Acceptance Criteria:**
- Failure at step 2 triggers compensation of step 1 (room release)
- Failure at step 3 triggers compensation of steps 1 and 2
- All compensation is logged with clear output
- No shared state between services (each service maintains its own in-memory store)