# Feature Flags, System Monitoring, and Developer Experience — Questions

> This file tracks big-picture, cross-module questions about observability, feature flags, and Developer Experience.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand SLOs" is less useful than "Why does my SLO need to be stricter than my SLA?"
3. **Update status** as you find answers — partial answers count.
4. **Link your answers** to the module or resource where you found the explanation.
5. **Add follow-up questions** — good answers often raise better questions.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Unanswered — needs research |
| 🟡 | Partial — have some understanding but still unclear |
| 🟢 | Answered — well understood |
| ⏸ | Deferred — not urgent; revisit later |

---

## Question Format

```markdown
### Q{{N}}: {{QUESTION_TITLE}}

**Asked:** {{YYYY-MM-DD}}
**Status:** 🔴 Unanswered

**Full question:**
Write the question in full. Include context about what prompted it.

**My current hypothesis:**
What do you think the answer might be, even if you're not sure?

**Answer:**
_To be filled in_

**Source:**
_Where did you find/confirm the answer?_

**Follow-up questions:**
- _Any new questions this answer raised_
```

---

## Questions

### Q001: When should I use Prometheus vs. DataDog vs. OpenTelemetry metrics?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
The topic covers Prometheus, DataDog, and OpenTelemetry — all of which can collect metrics. When would I choose one over another? Are they complementary or competing?

**My current hypothesis:**
Prometheus seems best for infrastructure/self-hosted metrics; DataDog seems better for teams that want a fully managed solution; OpenTelemetry seems like a vendor-neutral abstraction layer. But I'm not sure how these interact in practice.

**Answer:**
_Research in progress. Check Module 02 (Prometheus) and Module 07 (DataDog) for detailed comparisons._

**Source:**
_To be filled in_

**Follow-up questions:**
- Can I use OpenTelemetry to send metrics to both Prometheus and DataDog simultaneously?
- Is there a cost tradeoff between self-hosted Prometheus and managed DataDog at scale?

---

### Q002: What is the difference between a feature flag and a configuration value?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
Both feature flags and configuration values are runtime conditionals. What makes something a "feature flag" specifically? When does a config value become a flag, and when should I use a dedicated flag system like PostHog or LaunchDarkly instead of a config file?

**My current hypothesis:**
Feature flags are configuration values specifically designed for controlling feature visibility, with additional capabilities like user targeting, gradual rollouts, and audit logs that plain config files don't provide.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- What are the failure modes of using a database for feature flags vs. a dedicated service?
- How should stale flags be cleaned up to avoid technical debt?

---

### Q003: How do the three pillars (metrics, logs, traces) complement each other in practice?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The theory says metrics tell you something is wrong, logs tell you what happened, and traces tell you where the problem is in a distributed system. But in practice, when am I reaching for each one? Can you walk through a realistic debugging scenario that uses all three?

**My current hypothesis:**
I think you'd start with a metric alert (latency is high), look at logs to find error messages, and then use traces to identify which service in a call chain is slow. But I haven't verified this workflow.

**Answer:**
_To be filled in — see Module 01 (Introduction) for the initial framework and Module 05 (Distributed Tracing) for the integrated debugging workflow._

**Source:**
_To be filled in_

**Follow-up questions:**
- Is there a name for this "metrics → logs → traces" debugging workflow?
- How does correlation ID help bridge logs and traces?

---

_Add new questions above this line. Keep them numbered sequentially._

---

## Resolved Questions Archive

_Move fully answered questions (🟢) here to keep the active list manageable._

_(none yet)_

---

## Question Stats

| Status | Count |
|--------|-------|
| 🔴 Unanswered | 2 |
| 🟡 Partial | 1 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **3** |
