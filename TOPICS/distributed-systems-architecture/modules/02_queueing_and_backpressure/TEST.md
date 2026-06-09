# Test: Module 02 — Queueing and Backpressure

**Instructions:** Answer all questions. Write your answers directly below each question. Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 3 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** Define one key concept from this module.
> Answer:

**Q2.** Name one operational risk introduced by distributed boundaries.
> Answer:

**Q3.** What is one reason to make failure handling explicit?
> Answer:

**Q4.** Name one signal operators can use to understand system behavior.
> Answer:

**Q5.** What does idempotency protect against?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain one tradeoff between synchronous and asynchronous interaction.
> Answer:

**Q7.** Why can local tests miss production failure modes?
> Answer:

**Q8.** Compare scaling capacity with reducing demand.
> Answer:

**Q9.** Explain how ownership affects architecture.
> Answer:

**Q10.** What makes an architecture operable?
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Write a runnable idempotency check for duplicate IDs.
> Answer:

**Q12.** Debug this code: what is missing, and how would you fix it?

```python
def call_dependency(client):
    return client.get("/status")
```

> Answer:

**Q13.** Given a growing queue, list three likely causes and one measurement for each.
> Answer:

**Q14.** Design a retry policy for a transient dependency failure.
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a small workflow that combines service boundaries, async work, and observability. Justify the tradeoffs.
> Answer:

**Q16.** Write an architecture-review paragraph explaining when you would reject the pattern taught in this module.
> Answer:

---

## Bonus Questions (variable pts)

**Bonus 1.** Connect this module to one real incident pattern or production outage mode. (+3 pts)
> Answer:
