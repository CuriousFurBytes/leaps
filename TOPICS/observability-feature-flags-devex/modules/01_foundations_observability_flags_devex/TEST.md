# Test: Module 01 — Foundations of Observability, Feature Flags, and DevEx

**Instructions:** Answer all questions. Write your answers directly below each question. Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 3 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is a feature flag?
> Answer:

**Q2.** Name two types of telemetry.
> Answer:

**Q3.** What is a guardrail metric?
> Answer:

**Q4.** What does DevEx mean in this topic?
> Answer:

**Q5.** Why should a flag have an owner?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain why deployment and release are not the same thing.
> Answer:

**Q7.** Compare product analytics and infrastructure monitoring.
> Answer:

**Q8.** Why can average latency be misleading during a rollout?
> Answer:

**Q9.** Explain how Sentry-style error monitoring complements dashboards.
> Answer:

**Q10.** Describe one way poor DevEx can make production less safe.
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Write a small Python function that returns true for approximately `percent` percent of stable user IDs.
> Answer:

**Q12.** Debug this policy and rewrite it safely.

```yaml
flag: new_checkout
rollout: everyone
action_if_bad: panic
```

> Answer:

**Q13.** Given a rollout with rising errors but flat conversion, what would you inspect before expanding exposure?
> Answer:

**Q14.** Design three telemetry fields that should be attached to product events during a flagged rollout.
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a rollout strategy that uses feature flags, product analytics, error monitoring, and dashboards together.
> Answer:

**Q16.** Explain how an internal platform could improve both reliability and developer speed without hiding operational responsibility.
> Answer:

---

## Bonus Questions (variable pts)

**Bonus 1.** Identify one privacy risk in observability data and one mitigation. (+3 pts)
> Answer:
