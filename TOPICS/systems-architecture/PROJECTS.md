# Systems Architecture — Projects

> Projects are how architecture knowledge becomes architecture judgment.
> A concept you've read about is not one you understand — a system you've designed (even on paper) is.

---

## Beginner Projects

### Project 1: Monolith Decomposition Analysis

**Difficulty:** Beginner
**Estimated Time:** 3–4 hours
**Modules Covered:** 01, 04

**Brief:**
Take a hypothetical monolithic e-commerce application (user registration, product catalog, shopping cart, order processing, payment, email notifications) and produce a written decomposition analysis:
1. Draw the current monolith as a component diagram
2. Identify at least 3 candidate bounded contexts from the domain
3. Propose a service decomposition with justified boundaries
4. Identify one dependency that would be hardest to extract and explain why

**Acceptance Criteria:**
- Component diagram exists (can be Mermaid or hand-drawn and described in Markdown)
- Each proposed service has a clearly stated responsibility and ownership boundary
- At least one anti-pattern (shared database, distributed monolith) is identified and explained
- Write-up is at least 500 words with reasoning, not just diagrams

---

### Project 2: Message Queue Topology Design

**Difficulty:** Beginner
**Estimated Time:** 3–4 hours
**Modules Covered:** 02, 03

**Brief:**
Design the messaging topology for an order fulfillment system with these services: Order Service, Inventory Service, Payment Service, Notification Service, Shipping Service. Produce:
1. A Mermaid diagram showing topics/queues and which services produce/consume each
2. A delivery semantics decision table (which topics need at-least-once vs exactly-once and why)
3. A consumer group design for the Notification Service (which needs to receive all events without deduplication concerns)

**Acceptance Criteria:**
- Diagram clearly shows direction of data flow
- Delivery semantics are justified, not just named
- Consumer group design correctly handles the fan-out requirement

---

## Intermediate Projects

### Project 3: Implement the Outbox Pattern

**Difficulty:** Intermediate
**Estimated Time:** 6–8 hours
**Modules Covered:** 03, 06

**Brief:**
Implement the Outbox Pattern in Python with SQLite (for simplicity) as the database and a mock "message broker" (a simple in-memory queue or a file). Your implementation must:
1. A `create_order()` function that writes to `orders` table and `outbox` table in one transaction
2. A background relay process that reads from `outbox` and publishes to the broker
3. A simulation of a broker failure (the relay should retry without duplicate-publishing if it uses idempotency keys)
4. Tests that show: (a) no order is lost if the broker is down, (b) no order event is published twice

**Acceptance Criteria:**
- Code runs without external dependencies beyond Python stdlib
- Includes a README explaining the dual-write problem and how your implementation solves it
- Tests pass and demonstrate both failure scenarios

---

### Project 4: Circuit Breaker from Scratch

**Difficulty:** Intermediate
**Estimated Time:** 5–6 hours
**Modules Covered:** 05

**Brief:**
Implement a generic circuit breaker in Python with the three states (Closed, Open, Half-Open). It should:
1. Accept configurable thresholds (failure count, cooldown duration, probe timeout)
2. Wrap any callable (e.g., an HTTP call, a database query)
3. Raise a `CircuitOpenError` immediately when the circuit is open
4. Transition correctly through all three states
5. Include unit tests that drive each state transition

**Acceptance Criteria:**
- All three state transitions covered by tests
- Configurable via constructor arguments, not hardcoded constants
- A short demo script showing the circuit breaker protecting a simulated flaky service

---

## Advanced Projects

### Project 5: Saga Orchestrator Design

**Difficulty:** Advanced
**Estimated Time:** 8–10 hours
**Modules Covered:** 03, 06

**Brief:**
Design and implement (in Python or pseudocode with full detail) a Saga Orchestrator for a hotel booking system with four steps:
1. Reserve room
2. Charge credit card
3. Send confirmation email
4. Update loyalty points

Each step has a compensating transaction. Your orchestrator must:
- Handle failure at any step
- Execute the correct compensating transactions in reverse order
- Be idempotent (safe to retry the whole saga)
- Produce a state machine diagram for the saga

**Acceptance Criteria:**
- State machine diagram shows all happy path and failure states
- Each compensating transaction is explicitly documented
- The orchestrator class handles all failure cases without crashing
- A simulation showing a failure at step 3 and correct rollback of steps 2 and 1

---

### Project 6: Distributed System Observability Setup

**Difficulty:** Advanced
**Estimated Time:** 8–10 hours
**Modules Covered:** 08

**Brief:**
Design a complete observability strategy (in a design document + working code skeleton) for a 3-service system (API Gateway → Order Service → Inventory Service). Your deliverables:
1. Instrument all three services with OpenTelemetry (Python SDK — real code)
2. Show how a correlation ID propagates through all three services in HTTP headers
3. Design the log schema (structured JSON fields) for each service
4. Write a runbook section: "How to debug a slow order request using only your observability setup"

**Acceptance Criteria:**
- Working Python code with OpenTelemetry instrumentation (even if mock HTTP calls)
- Correlation ID visible in all three services' trace spans
- Log schema documented as a JSON example
- Runbook section is concrete and actionable, not generic advice

---

## Expert Projects

### Project 7: Architecture Review — Identify Anti-Patterns

**Difficulty:** Expert
**Estimated Time:** 6–8 hours
**Modules Covered:** 01, 04, 06, 11

**Brief:**
Given the following fictional architecture description (write your own or ask an AI to generate a realistic but flawed one), produce a formal architecture review document:
1. Identify all anti-patterns present (distributed monolith, shared database, synchronous chains, etc.)
2. Prioritize them by risk (likelihood × impact)
3. Propose mitigations for the top 3 issues with estimated effort
4. Write one ADR for the most important change

**Acceptance Criteria:**
- At least 4 anti-patterns identified with specific evidence from the architecture description
- Prioritization includes explicit reasoning, not just intuition
- ADR follows the standard format (Context, Decision, Consequences)

---

### Project 8: Full Capstone Pre-Work

**Difficulty:** Expert
**Estimated Time:** 10–15 hours
**Modules Covered:** All

**Brief:**
Design the architecture for a ride-sharing platform (matching, pricing, driver tracking, payment, notifications). This is a warm-up version of the full capstone (Module 12) focused on a single vertical slice: the ride-matching flow from "rider requests a ride" to "driver accepts". Produce:
1. Service decomposition with bounded context diagram
2. Message topology for the matching flow
3. Data ownership table (which service owns what data)
4. Failure mode analysis for 3 scenarios (driver goes offline mid-match, payment fails, notification service down)
5. One ADR for the most controversial design decision you made

**Acceptance Criteria:**
- All five deliverables present
- Each design decision has explicit reasoning and acknowledged trade-offs
- At least one "I chose X over Y because..." statement per major decision
