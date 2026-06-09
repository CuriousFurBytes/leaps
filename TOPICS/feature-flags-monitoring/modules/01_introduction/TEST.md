# Test — Module 01: Introduction to Observability

**Topic:** [[feature-flags-monitoring]]
**Module:** [[modules/01_introduction]]

---

## Before You Begin

> [!WARNING]
> **Do not look at ANSWERS.md or your notes during the test.**
> The purpose of this test is to surface what you truly know vs. what you think you know.
> An inflated score is worthless. An honest score shows you exactly where to focus next.

**Instructions:**
1. Close all notes, the module README, and any reference materials.
2. Set a timer. Note your start time below.
3. Attempt every question — partial credit exists.
4. After finishing, grade yourself using ANSWERS.md.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Start time:** ___________
**End time:** ___________
**Total time:** ___________

---

## Scoring Table

| Section | Question Type | Points Each | # Questions | Max Points |
|---------|--------------|-------------|-------------|------------|
| Section 1: Recall | Easy | 1 pt | 5 | 5 pts |
| Section 2: Conceptual | Medium | 2 pts | 3 | 6 pts |
| Section 3: Applied | Hard | 3 pts | 2 | 6 pts |
| Section 4: Scenario/Debugging | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** What is the difference between monitoring and observability? Name the key limitation of monitoring that observability addresses.

> _Your answer:_

---

**1.2** Name the three pillars of observability and state in one sentence what question each one primarily answers.

> _Your answer:_

---

**1.3** Define "error budget" in your own words and explain how it is calculated from an SLO target.

> _Your answer:_

---

**1.4** What is the difference between an SLO and an SLA? Which is typically set more strictly, and why?

> _Your answer:_

---

**1.5** Name two reasons why using `user_id` as a Prometheus label is a mistake.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** A colleague says: "We already have logging — we can skip Prometheus metrics because we can always query logs to count errors and measure latency." Is this correct? Explain your reasoning, including at least one specific scenario where metrics are superior to logs for this purpose.

> _Your answer:_

---

**2.2** Explain why feature flags need to be cleaned up after a rollout completes. What specific technical and operational problems arise when stale flags are left in code indefinitely?

> _Your answer:_

---

**2.3** Compare and contrast the SLI for "service is up (binary)" vs. "99.9% of requests succeed (ratio)". Why is the ratio SLI better for most modern services? Under what circumstance might the binary SLI still be appropriate?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** A team has a 99.9% availability SLO for their payment API over a 30-day window. In the first 20 days of the month, the service experienced 35 minutes of downtime.

a) Calculate the total monthly error budget in minutes.
b) How many minutes of error budget remain?
c) What percentage of the budget has been consumed?
d) Should the team be concerned? What action, if any, should they take?

Show your calculations.

> _Your answer:_

---

**3.2** You are tasked with adding observability to a Flask API endpoint that processes user authentication. Write the Prometheus metric definitions (Counter and Histogram) you would add, with appropriate metric names, help text, and labels. Explain your label choices — specifically why you chose the labels you did and which labels you deliberately excluded.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** The following Prometheus metric definition is used in production on a service with 500,000 daily active users:

```python
from prometheus_client import Counter

LOGIN_EVENTS = Counter(
    'user_login_events_total',
    'Total login events',
    ['user_id', 'method', 'success']
)

# Called on every login attempt
def record_login(user_id: str, method: str, success: bool):
    LOGIN_EVENTS.labels(
        user_id=user_id,    # e.g., "user-12345"
        method=method,       # e.g., "oauth" or "password"
        success=str(success) # "True" or "False"
    ).inc()
```

Identify:
a) What is wrong with this metric definition?
b) Why does this happen and what are the consequences in production?
c) Rewrite the `record_login` function and metric definition to fix the problem while still capturing meaningful data.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** A startup founder tells you: "We're moving fast and can't afford the overhead of observability tooling right now. We'll add it later once the product is stable." Respond to this position. Consider both the founder's concern and the risks they are accepting. What is the minimum viable observability setup you would recommend for an early-stage team?

Consider at least two perspectives or tradeoffs in your answer.
Justify your conclusion based on what you've learned in this module.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** The Google SRE book introduced the concept of "burn rate" alerting, which fires alerts not based on current error rate crossing a threshold, but based on how fast the error budget is being consumed. Explain what burn rate is in your own words, why it is superior to simple threshold alerting (e.g., "alert if error rate > 1%"), and describe a scenario where simple threshold alerting would fail to provide adequate warning before the error budget is exhausted.

Bonus: write the PromQL expression that calculates the burn rate for a service with a 99.9% monthly SLO.

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the next module?**
> _Your reflection:_

**What score did I get? Do I feel it accurately reflects my understanding?**
> _Your reflection:_

---

## Grading Record

_Append a new row each time you take this test. Do not overwrite previous attempts._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
