# Answers: Module 01 — Foundations of Distributed Systems

## Answer Key

### Easy Questions
**Q1:** A correct answer defines a module concept precisely and includes its operational consequence.
**Q2:** Examples include latency, partial failure, overload, stale data, duplicate messages, or unclear ownership.
**Q3:** Explicit failure handling prevents hidden hangs, retry storms, data corruption, and confusing incidents.
**Q4:** Logs, metrics, traces, queue depth, latency, error rate, saturation, and correlation IDs are valid examples.
**Q5:** Idempotency protects against duplicate delivery, retries, and repeated user or system actions.

### Medium Questions
**Q6:** Strong answers discuss immediacy, latency, durability, coupling, user experience, and operational complexity.
**Q7:** Local tests often lack load, network delay, dependency failure, retries, deployment churn, and shared resource contention.
**Q8:** Strong answers compare adding workers or resources with slowing producers, bounding queues, caching, batching, or shedding load.
**Q9:** Ownership determines who changes data, owns incidents, evolves contracts, and pays coordination cost.
**Q10:** Operable architectures expose useful signals, have clear failure modes, support rollback, and have documented runbooks.

### Hard Questions
**Q11:** Award full credit for runnable code that stores processed IDs and avoids repeating unsafe side effects.
**Q12:** Full credit identifies missing timeout/error policy and proposes an explicit timeout plus failure handling.
**Q13:** Full credit names producer surge, slow consumers, retry storms, or poison messages with metrics such as arrival rate, service rate, retry count, and queue age.
**Q14:** Full credit includes bounded retries, backoff, jitter, timeout, idempotency, and dead-letter or escalation behavior.

### Expert Questions
**Q15:** Full credit synthesizes boundaries, async messaging, retry/idempotency, and observability with clear tradeoff justification.
**Q16:** Full credit explains conditions where the module pattern adds more complexity than value.

### Bonus Questions
**Bonus 1:** Full credit connects concepts to a plausible outage mode and explains prevention or detection.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
