# Questions — Module 01: Introduction to Observability

> Log questions as they arise — don't wait until you understand them fully.
> A question written down is a learning opportunity captured.
> For big-picture questions about the whole topic, use the topic-level QUESTIONS.md instead.

---

## How to Use This File

1. Write the question the moment it occurs to you, even if you can't articulate it well yet.
2. Come back and refine the question once you understand it better.
3. Update the status as you research or find answers.
4. Link to the source where you found the answer.
5. Capture follow-up questions — good answers always raise new ones.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Unanswered — needs active research |
| 🟡 | Partial — have some understanding, still incomplete |
| 🟢 | Answered — well understood, could explain to someone else |
| ⏸ | Deferred — not urgent, revisit in a later module |

---

## Questions

### Q001: How does the "three pillars" model apply when all services are in a single monolith?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The module emphasizes traces for debugging distributed systems. But what if I have a monolith — one big service? Is distributed tracing still relevant? Which pillars matter most in a monolith vs. microservices?

**My current hypothesis:**
For a monolith, metrics and logs are probably sufficient for most debugging since all code runs in one process. Traces might still be useful for tracking external API calls (Stripe, databases, etc.) but probably less critical than in a microservices architecture.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- At what point does a monolith become complex enough that traces become worth the overhead?

---

### Q002: How do you choose between setting SLOs at the service level vs. the endpoint level?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The module talks about SLOs for a "service", but real services have many endpoints with different criticality levels. Should I define one SLO for the whole service, or per-endpoint SLOs? What do companies like Google actually do?

**My current hypothesis:**
Critical paths (checkout, login, payment) probably need stricter SLOs than less important endpoints (user profile views, analytics queries). But managing many SLOs seems operationally complex.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does Prometheus / Grafana support per-endpoint SLO tracking natively?
- What's the minimum number of SLOs a team should define for a typical API?

---

_Add new questions below this line. Keep them numbered sequentially._

---

## Resolved Questions Archive

_Move fully answered 🟢 questions here to keep the active list clean._

_(none yet)_

---

## Question Stats

| Status | Count |
|--------|-------|
| 🔴 Unanswered | 2 |
| 🟡 Partial | 0 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **2** |
