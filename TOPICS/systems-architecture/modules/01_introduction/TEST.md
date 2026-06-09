# Test: Module 01 — Introduction to Distributed Systems

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** Name four of the 8 Fallacies of Distributed Computing.

> Answer:

**Q2.** The CAP theorem states a distributed system can only guarantee two of three properties simultaneously. Name all three properties and give a one-sentence definition of each.

> Answer:

**Q3.** What is a network partition?

> Answer:

**Q4.** In one sentence, what is the key difference between synchronous and asynchronous service communication?

> Answer:

**Q5.** True or False: A single-node PostgreSQL database is considered partition-tolerant. Explain your answer in one sentence.

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain why the choice in the CAP theorem is really between Consistency and Availability, and not between any of the three pairs. (Hint: consider why you can't give up P in practice.)

> Answer:

**Q7.** A startup is building a social media platform. They have 4 engineers and have been coding for 3 months. The CTO says: "Let's split into 12 microservices now so we won't have to refactor later." Explain specifically why this is likely the wrong decision, and what you would recommend instead.

> Answer:

**Q8.** What is a "distributed monolith" and why is it considered worse than either a proper monolith or proper microservices?

> Answer:

**Q9.** Explain the "tail latency amplification" problem in synchronous service chains. If 5 services each have p99 latency of 50ms, what is the approximate p99 for a request that calls all 5 sequentially? (Assume calls are sequential and failures are independent.)

> Answer:

**Q10.** A service call to a payment provider times out after 10 seconds. Does this mean the payment was not processed? Explain what might have happened and what the correct handling strategy is.

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Debug the following code. Identify at least 3 specific problems and explain the failure mode each creates in production:

```python
def fetch_recommendations(user_id: int) -> list:
    resp = requests.get(f"http://rec-service/recommend?user={user_id}")
    data = resp.json()
    return data["recommendations"]
```

> Answer:

**Q12.** You are designing the checkout flow for an e-commerce site. The flow involves: (1) reserving inventory, (2) processing payment, (3) confirming the order, (4) sending a confirmation email. For each step, decide: synchronous or asynchronous? Justify each decision individually.

> Answer:

**Q13.** Write a Python function `safe_call(url: str, payload: dict) -> dict | None` that demonstrates at least 4 of the following production practices: timeout handling, retry with exponential backoff, idempotency key, error classification (transient vs. permanent), structured logging.

```python
# Write your implementation here:
```

> Answer:

**Q14.** The PACELC model classifies DynamoDB as PA/EL. Explain what each letter means in the context of DynamoDB's actual behavior, including a concrete example of when each trade-off would be observable by an application developer.

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a system architecture for the following scenario, justifying each major decision: A global real-time multiplayer game needs to track player scores. Requirements: (a) players must be able to see their own score immediately after scoring a point, (b) the global leaderboard can be slightly stale (updated every 30 seconds is acceptable), (c) during a regional network partition, players in the affected region must still be able to play and score points. For each component, explicitly state its CAP classification and explain why you chose it.

> Answer:

**Q16.** Synthesize the 8 Fallacies, the CAP theorem, and the monolith/microservices trade-off into a coherent architectural philosophy. In 200–300 words, explain: what should a team's default architectural position be, and under what specific circumstances should it change? Your answer should cite at least three concepts from this module and show how they inform the same conclusion.

> Answer:

---

## Bonus Questions

**Bonus 1.** (+5 pts) The Google Spanner database claims to offer "external consistency" — behavior that appears to violate CAP's Consistency/Availability trade-off during partitions. Research how Spanner achieves this and explain the key physical mechanism that allows it. What trade-off does Spanner make that "ordinary" distributed databases don't make?

> Answer:
