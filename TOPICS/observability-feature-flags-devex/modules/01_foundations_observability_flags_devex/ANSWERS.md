# Answers: Module 01 — Foundations of Observability, Feature Flags, and DevEx

## Answer Key

### Easy Questions
**Q1:** A feature flag is a runtime control that changes application behavior without a new deployment.
**Q2:** Valid examples include metrics, logs, traces, errors, and product events.
**Q3:** A guardrail metric is a preselected signal that protects users or systems during a rollout.
**Q4:** DevEx is the quality of the workflows developers use to build, ship, debug, and operate software.
**Q5:** Ownership makes decisions, cleanup, and incident response accountable.

### Medium Questions
**Q6:** Deployment moves code into an environment; release exposes behavior to users.
**Q7:** Product analytics measures user behavior and value; infrastructure monitoring measures system health and capacity.
**Q8:** Averages hide tail latency and affected subgroups.
**Q9:** Error monitoring groups real failures and links them to releases, users, and stack traces, complementing aggregate dashboards.
**Q10:** Manual, confusing workflows cause skipped checks, slower rollbacks, and inconsistent incident response.

### Hard Questions
**Q11:** A correct answer uses stable hashing or bucketing and compares the bucket with the requested percentage.
**Q12:** A safe rewrite includes staged exposure, owner, guardrails, and rollback action.
**Q13:** Inspect error grouping, affected cohorts, traces, logs, recent releases, and flag exposure before expanding.
**Q14:** Good fields include flag key/value, release version, user or cohort identifier, environment, and correlation ID.

### Expert Questions
**Q15:** Strong answers combine staged exposure, predeclared guardrails, PostHog-style product events, Sentry-style errors, Datadog/Grafana dashboards, ownership, and rollback rules.
**Q16:** Strong answers discuss paved roads, templates, automation, visibility, guardrails, and preserving clear human ownership.

### Bonus Questions
**Bonus 1:** Valid risks include PII leakage, excessive retention, broad access, or event re-identification; mitigations include redaction, minimization, RBAC, retention limits, and review.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
