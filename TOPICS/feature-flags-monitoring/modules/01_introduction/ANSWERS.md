# Answer Key — Module 01: Introduction to Observability

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — Monitoring vs. Observability [1 pt]

**Full credit answer:**
Monitoring is the practice of collecting predefined metrics and alerting when they cross thresholds — it can only detect failures that were anticipated in advance. Observability is the property of a system that allows understanding its internal state from external outputs alone, enabling debugging of unexpected failures. The key limitation monitoring addresses poorly is: you cannot monitor for failure modes you didn't anticipate.

**Key points required:**
- Monitoring = predefined checks for anticipated failures
- Observability = ability to understand state from external outputs, including unexpected failures
- The limitation is that monitoring requires anticipating failures in advance

**Common wrong answers:**
- "Monitoring is old, observability is new" — partially true but misses the conceptual distinction
- "Observability is just better monitoring" — misses the key point about exploring unexpected failures vs. detecting anticipated ones

---

### 1.2 — The Three Pillars [1 pt]

**Full credit answer:**
1. **Metrics** — Numeric measurements aggregated over time. Answers: "Is something wrong? What are the trends?" (e.g., error rate, latency p99)
2. **Logs** — Timestamped records of discrete events. Answers: "What happened? What was the error message? What was the context?"
3. **Traces** — Correlated records of a request's path through a distributed system. Answers: "Where in the distributed system did this request fail or slow down?"

**Key points required:** All three named correctly, each with a distinguishing characteristic and what question it answers.

**Partial credit (0.5 pt):** Names all three correctly but can't articulate what each answers, OR has two correct and one wrong.

---

### 1.3 — Error Budget [1 pt]

**Full credit answer:**
An error budget is the allowable amount of downtime or errors a service can have in an SLO window while still meeting its SLO. It is calculated as: `Error Budget = (1 - SLO target) × window duration`. For a 99.9% monthly SLO: `(1 - 0.999) × 43,200 minutes = 43.2 minutes`. When the error budget is spent, the team should pause risky changes and focus on reliability.

**Key points required:** Definition (allowable downtime within SLO), formula, and an example.

---

### 1.4 — SLO vs. SLA [1 pt]

**Full credit answer:**
An SLO (Service Level Objective) is an internal reliability target — a commitment the team makes to itself. An SLA (Service Level Agreement) is a contractual commitment to customers with financial consequences if violated. SLOs are set more strictly than SLAs, because the gap between them is a buffer: if the internal SLO is 99.9% and the SLA is 99.5%, the team has 172 minutes of error budget margin before contractual penalties apply.

**Key points required:**
- SLO = internal target; SLA = external contractual commitment
- SLO is stricter than SLA (not the other way around)
- The gap is a buffer

---

### 1.5 — Why Not user_id as a Prometheus Label [1 pt]

**Full credit answer:**
Two reasons: (1) High cardinality — each unique user_id creates a separate time series in Prometheus. With millions of users, this creates millions of time series, causing Prometheus to run out of memory and crash. (2) Incorrect use of the tool — per-user data belongs in logs or product analytics (PostHog), which are designed for high-cardinality event data. Prometheus is designed for aggregated, low-cardinality metrics.

**Key points required:** Cardinality problem (OOM risk), and at least one of: wrong tool / data belongs elsewhere.

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Metrics vs. Logs for Counting Errors [2 pts]

**Full credit answer:**
The colleague's claim is incorrect. While logs can be queried to count errors and measure latency, logs are expensive to query at high throughput and introduce latency into alerting. Metrics are pre-aggregated and specifically designed for fast, low-cost threshold queries and alerting. A concrete scenario: at 10,000 requests/second, querying logs to calculate real-time p99 latency would require scanning gigabytes of log data per minute — a serious operational and cost burden. Prometheus stores pre-computed aggregate metrics that can be queried in milliseconds. Additionally, metrics have built-in time-series semantics (counter resets, range queries, alerting rules) that log queries don't provide natively.

**Rubric:**
- 2 pts: Correctly identifies the claim as incorrect, explains the performance/cost difference, and gives a specific scenario
- 1 pt: Correctly identifies the claim as incorrect with a valid reason, but no specific scenario
- 0 pts: Agrees with the misconception or gives an incorrect explanation

**Teaching note:**
The most common wrong answer is "logs don't give you p99 latency" — this is technically false (log aggregation tools can compute percentiles). The right answer is about cost, latency, and architectural fit. Metrics are the right tool for alerting and SLO tracking; logs are the right tool for event investigation.

---

### 2.2 — Feature Flag Cleanup [2 pts]

**Full credit answer:**
Stale flags create several problems: (1) Code complexity — every flag is a conditional branch that must be tested for both states, even when one state is dead in production. (2) Cognitive overhead — engineers reading the code must understand what each flag controls, which becomes impossible for old flags nobody remembers. (3) Test matrix explosion — with N flags, there are 2^N possible flag combinations to test. (4) Risk when removing — after enough time, nobody is confident that removing a "permanently on" flag won't break something, so nobody removes it. Best practice is to set a target removal date at flag creation time and treat old flags as technical debt.

**Rubric:**
- 2 pts: Identifies at least 2 specific technical/operational problems with good explanation
- 1 pt: Identifies that flags are "technical debt" without articulating specific mechanisms
- 0 pts: Says flags don't need to be cleaned up

---

### 2.3 — Binary vs. Ratio SLI [2 pts]

**Full credit answer:**
The ratio SLI ("99.9% of requests succeed") is better for most services because it reflects actual user experience. A binary SLI ("service is up") can be true even while a service is heavily degraded — if 30% of requests are timing out, the service is "up" but users are experiencing significant failures. The ratio SLI captures partial outages, error bursts, and performance degradation that a binary SLI misses entirely.

A binary SLI might still be appropriate for services with no meaningful traffic distribution — for example, a batch job that either runs successfully or crashes entirely, or a scheduled task that either completes or doesn't.

**Rubric:**
- 2 pts: Explains why ratio SLI is better (captures partial degradation) AND gives a valid case for binary SLI
- 1 pt: Explains why ratio is better but can't articulate when binary is appropriate
- 0 pts: Says binary is fine for most cases or can't explain the difference

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Error Budget Calculation [3 pts]

**Full credit answer:**

a) Total monthly error budget: `(1 - 0.999) × 30 × 24 × 60 = 0.001 × 43,200 = 43.2 minutes`

b) Remaining budget: `43.2 - 35 = 8.2 minutes`

c) Budget consumed: `35 / 43.2 × 100 = 81%`

d) Yes, the team should be very concerned. They've consumed 81% of their monthly error budget in only 20 days (67% of the month). At this burn rate (`35 / 20 = 1.75 min/day`), they'll exhaust the budget in approximately `8.2 / 1.75 ≈ 4.7 days` — around day 24–25, with 5–10 days remaining in the month. The appropriate action is: freeze all non-critical deployments, focus engineering resources on the root cause of the downtime, and notify stakeholders that error budget is nearly exhausted.

**Rubric:**
- 3 pts: All 4 parts correct with clear calculations
- 2 pts: Calculations correct for a, b, c but analysis in d is shallow/incomplete
- 1 pt: Formula correct (a) but arithmetic errors in b/c or missing d
- 0 pts: Incorrect formula or blank

---

### 3.2 — Prometheus Metric Definitions for Auth Endpoint [3 pts]

**Full credit answer:**

```python
from prometheus_client import Counter, Histogram

# Counter for total login requests with appropriate low-cardinality labels
# Labels:
#   - method: "password", "oauth", "sso" — bounded set, meaningful for debugging
#   - status: "success", "failure" — two values, always low cardinality
# Deliberately excluded:
#   - user_id: high cardinality; per-user data belongs in logs or product analytics
#   - session_id: high cardinality, per-request identifier
#   - ip_address: unbounded, high cardinality
LOGIN_REQUESTS = Counter(
    'auth_login_requests_total',
    'Total authentication login requests',
    ['method', 'status']
)

# Histogram for login latency
# Buckets chosen to capture typical auth latency:
# OAuth redirects can be slow (0.5–2s); password hashing adds ~100ms
AUTH_LATENCY = Histogram(
    'auth_request_duration_seconds',
    'Authentication request duration in seconds',
    ['method'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
```

**Rubric:**
- 3 pts: Both metrics defined correctly, label choices explained, high-cardinality labels explicitly excluded with explanation
- 2 pts: Metrics defined correctly but label rationale is missing or thin
- 1 pt: One metric correct, or metric names/types wrong but rationale present
- 0 pts: Definitions fundamentally incorrect

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Debugging the High-Cardinality Metric [3 pts]

**(a) What is wrong?**
The `user_id` label is high cardinality. With 500,000 daily active users, Prometheus creates a unique time series for every `user_id` + `method` + `success` combination. That's potentially hundreds of thousands of time series just for this one metric.

**(b) Why does this happen and what are the consequences?**
Prometheus creates one time series per unique combination of label values. With 500,000 user IDs × 2 methods × 2 success states = up to 2,000,000 time series. This causes Prometheus to: (1) run out of memory (OOM crash), (2) slow down queries dramatically, (3) increase disk I/O and WAL write pressure. The service may appear to work normally while the Prometheus instance degrades over hours or days.

**(c) Fixed version:**

```python
from prometheus_client import Counter

# Remove user_id label entirely — per-user data belongs in logs or PostHog
# Keep method and success (or map success to "status" with values "ok"/"error")
LOGIN_EVENTS = Counter(
    'user_login_events_total',
    'Total login events',
    ['method', 'status']  # 'status' = "success" or "failure"
)

def record_login(user_id: str, method: str, success: bool):
    status = "success" if success else "failure"
    LOGIN_EVENTS.labels(method=method, status=status).inc()

    # For per-user debugging, use structured logging instead:
    # logger.info("login_event", user_id=user_id, method=method, success=success)
```

**Rubric:** 1 pt each for (a), (b), (c) answered correctly and specifically.

**Accept alternative fixes:** Any solution that removes `user_id` from labels and preserves `method` and `success/status` is acceptable. The key fix is eliminating the high-cardinality label.

---

## Section 5: Discussion — Answer Key

### 5.1 — Minimum Viable Observability for a Startup [2 pts]

**Example strong answer:**
The founder's concern is understandable — setting up and maintaining observability tools has real overhead. However, the risk they're accepting is operating blind: they'll only discover problems when customers complain, and they'll debug production issues by restarting things and guessing. A minimum viable observability setup for an early-stage team requires almost no infrastructure: (1) structured JSON logging (change two lines in your web framework configuration) and (2) Sentry for error tracking (5 minutes to integrate a free tier account). These two give logs for event investigation and automatic error capture — covering the most critical immediate needs. Prometheus + Grafana can be added later when the team has capacity; Sentry is hard to add retroactively because you lose historical error data. The cost of a major undetected production bug (user data corruption, silent payment failures) far exceeds the cost of one afternoon setting up structured logging and Sentry.

**Elements that earn full credit:**
- Acknowledges the founder's legitimate concern (not dismissive)
- Identifies specific risks of running without observability
- Proposes a minimum viable setup that is genuinely minimal and achievable
- Distinguishes between "add now" (critical) and "add later" (nice to have)

**Rubric:**
- 2 pts: Balanced, specific, practical recommendation with tradeoff awareness
- 1 pt: Either purely dismisses the concern without acknowledging it, or agrees with the founder without articulating the risks
- 0 pts: Off-topic or fundamentally misunderstands the tradeoffs

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Burn Rate Alerting [+5 pts]

**Full credit answer:**
Burn rate measures how fast a service is consuming its error budget relative to the expected pace. A burn rate of 1.0 means the service is consuming error budget at exactly the sustainable rate; a burn rate of 10 means it's consuming budget 10x faster than the expected pace and will exhaust the budget in 1/10th of the normal window.

**Why it's superior to threshold alerting:**
A simple "error rate > 1%" alert can miss a slow, sustained degradation. If the SLO is 99.9% (0.1% error rate budget) and the service is running at 0.5% error rate — below the 1% threshold — a simple threshold alert won't fire. But at 0.5% error rate (5× the budgeted rate), the error budget will be fully exhausted in 6 days, with 24 days remaining in the month. Burn rate alerting detects this early.

**Scenario where threshold alerting fails:**
A service with 99.9% SLO runs at a sustained 0.2% error rate — just above the budget, but well below a typical 1% alert threshold. Simple threshold alerting never fires. But at 0.2%, the service is consuming 2× its error budget allocation: the 43.2-minute monthly budget will be exhausted in about 15 days, with no alerts ever having fired.

**PromQL burn rate expression:**
```promql
# Burn rate for a 99.9% SLO (budget fraction = 0.001)
# 1.0 = consuming exactly on pace; > 1.0 = consuming faster than budget allows
(
  sum(rate(http_requests_total{status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
) / 0.001

# Alert threshold: burn_rate > 14.4 means "budget exhausted in <2 days at this rate"
# (14.4 = 1 hour / (1/720 of monthly budget))
```

**Rubric:**
- 5 pts: Correctly explains burn rate, gives specific scenario where threshold fails, AND writes correct PromQL
- 3 pts: Correctly explains burn rate and scenario, but PromQL is wrong or missing
- 1 pt: General understanding of burn rate but can't give a specific scenario or write the expression
- 0 pts: Incorrect understanding

---

## Common Wrong Answers Across the Test

1. **Confusing SLO and SLA as the same thing** — These are distinct: SLO is internal, SLA is contractual. Students who make this mistake need to re-read the "SLI, SLO, and SLA" section.
2. **Missing the cardinality issue for `user_id`** — Students often say "user_id is a label so you can filter by user" without understanding the time-series explosion. Re-read the "Common Pitfalls" section and the high-cardinality pitfall.
3. **Treating observability as "better monitoring"** — The key distinction is observable systems can debug failures you didn't anticipate; monitoring can only detect failures you set up rules for in advance. Students who miss this need to re-read "Monitoring vs. Observability."

---

## Teaching Notes

- Students who struggle with Section 1 likely read without testing their understanding. Recommend re-studying with the Feynman technique (explain it aloud to an imaginary beginner).
- Students who struggle with Section 3's error budget math should revisit Exercise 2 in EXERCISES.md and practice with different SLO values.
- The bonus question on burn rate is advanced content from the Google SRE book — don't be concerned if most students skip it. It's a topic for Module 10 (Incident Response) in depth.
- A score below 60% generally indicates the concepts haven't solidified yet. Recommend re-reading Module 01 README, focusing on the SLI/SLO section and the cardinality pitfall.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
