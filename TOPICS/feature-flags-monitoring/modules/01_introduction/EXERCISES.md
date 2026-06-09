# Exercises — Module 01: Introduction to Observability

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read mentally — actually write or type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Classify the Signal [🟢 Easy] [1 pt]

### Context
Given a list of statements about what data a team is collecting, classify each as primarily a **metric**, **log**, or **trace**.

### Task
Classify each of the following as "metric", "log", or "trace" and briefly explain why (1 sentence each):

1. `http_requests_total{status="200"} = 15432` collected every 15 seconds
2. `2026-06-09T14:05:22Z ERROR user 456 checkout failed: invalid payment method`
3. A record showing that user request A went through services: API Gateway (120ms) → Cart Service (45ms) → Payment Service (850ms) with a shared request ID
4. `memory_usage_bytes = 524288000` at a specific timestamp
5. `{"event": "user_signup", "user_id": "123", "plan": "pro", "timestamp": "..."}`

### Requirements
- [ ] All 5 items classified correctly
- [ ] Each classification includes a 1-sentence justification
- [ ] At least one example of each signal type appears in your answers

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Think about the key properties of each:
- Metrics are numeric, aggregated, and collected at regular intervals
- Logs describe a single event that happened at a specific time
- Traces link multiple operations across services via a shared identifier

</details>

### Expected Output / Acceptance Criteria
```
1. Metric — it's a numeric measurement (counter) collected over time
2. Log — it describes a specific event at a specific timestamp with context
3. Trace — it links operations across multiple services with timing information
4. Metric — it's a numeric measurement (gauge) at a point in time
5. Log — it's a structured event record for a single occurrence
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

1. **Metric** — `http_requests_total` is a Counter metric. The `{status="200"}` label and the numeric value collected at 15-second intervals are the defining characteristics.
2. **Log** — The ISO 8601 timestamp, log level (`ERROR`), and free-form event description are all hallmarks of a log entry.
3. **Trace** — The key signal is "a record showing operations across multiple services with a shared request ID and timing for each." This is the definition of a distributed trace.
4. **Metric** — A Gauge metric (value that can go up or down) measured at a point in time.
5. **Log** — Even though it's structured JSON rather than a free-form string, this is a log entry for a single specific event.

**Common wrong answers and why they fail:**
- Classifying #5 as a "metric" — structured logs are still logs; the JSON format doesn't change their fundamental nature as event records
- Classifying #3 as "logs" — the key distinguishing feature of traces is the causal link between operations via a shared ID and the timing waterfall

</details>

---

## Exercise 2: Calculate Error Budgets [🟢 Easy] [1 pt]

### Context
Your team is defining SLOs for three services. You need to calculate the monthly error budget for each.

### Task
Calculate the monthly error budget in minutes for each of the following SLO targets:

1. Payment service: 99.9% availability SLO, 30-day window
2. Email notification service: 99.5% availability SLO, 30-day window
3. Internal analytics dashboard: 99.0% availability SLO, 30-day window

Additionally, answer: If the payment service has already had 40 minutes of downtime this month, what percentage of its error budget has been consumed?

### Requirements
- [ ] Correct calculation for all 3 services
- [ ] Budget consumption percentage for the follow-up question
- [ ] Show your calculation steps

### Hints
<details>
<summary>Hint 1</summary>

Formula: `Error Budget (minutes) = (1 - SLO%) × 30 × 24 × 60`

30 days × 24 hours × 60 minutes = 43,200 minutes in a 30-day month

</details>

### Expected Output / Acceptance Criteria
```
1. Payment service (99.9%):  43.2 minutes/month
2. Email service (99.5%):   216.0 minutes/month
3. Analytics (99.0%):       432.0 minutes/month

Budget consumed: 40 / 43.2 = 92.6% — nearly exhausted
```

### Solution
<details>
<summary>Show Solution</summary>

```python
def error_budget_minutes(slo_percent: float, window_days: int = 30) -> float:
    window_minutes = window_days * 24 * 60  # 43,200 for 30 days
    return (1 - slo_percent / 100) * window_minutes

# Payment service: 99.9%
payment_budget = error_budget_minutes(99.9)
print(f"Payment service: {payment_budget:.1f} minutes")   # 43.2

# Email service: 99.5%
email_budget = error_budget_minutes(99.5)
print(f"Email service: {email_budget:.1f} minutes")        # 216.0

# Analytics: 99.0%
analytics_budget = error_budget_minutes(99.0)
print(f"Analytics: {analytics_budget:.1f} minutes")        # 432.0

# Budget consumption
consumed = 40 / payment_budget * 100
print(f"Budget consumed: {consumed:.1f}%")                  # 92.6%
```

**Explanation:**
Multiply the error fraction (1 minus SLO as decimal) by the total minutes in the window. For 99.9%, the error fraction is 0.001; multiplied by 43,200 minutes gives 43.2 minutes. With 40 minutes already consumed, 92.6% of the budget is gone — the team should freeze risky changes for the rest of the month.

</details>

---

## Exercise 3: Identify the Right Pillar [🟡 Medium] [2 pts]

### Context
A teammate is debugging a production incident. For each scenario, identify which observability pillar (metrics, logs, traces) would be most useful, explain why, and describe what specific signal you would look for.

### Task
For each incident scenario below, answer:
- Which pillar is most useful for this stage of the investigation?
- What specific query/search/filter would you use?
- What information gap remains that requires another pillar?

**Scenario A:** An alert fires saying "API error rate is 3.5%, above the 1% SLO threshold."

**Scenario B:** After seeing the alert, you know errors are happening but need to understand what type of errors they are and what's causing them.

**Scenario C:** You've found the error message is "database connection timeout" in the logs. You need to understand whether the timeout is in your service's database call or in a downstream service's database call.

### Requirements
- [ ] All 3 scenarios answered with correct pillar identification
- [ ] Each answer includes a concrete, specific query or search approach
- [ ] Information gap identified for each scenario

### Hints
<details>
<summary>Hint 1</summary>

Think about the sequence: alerts come from metrics, context comes from logs, path comes from traces. Each pillar answers a different question.

</details>

<details>
<summary>Hint 2</summary>

For Scenario C specifically: if you have one monolith, logs might be enough. But in a distributed system where "database connection timeout" could come from any of 5 services, traces are what tell you which service's DB is the culprit.

</details>

### Expected Output / Acceptance Criteria
Your answers should demonstrate understanding of when each pillar is the appropriate tool and what it can/cannot tell you.

### Solution
<details>
<summary>Show Solution</summary>

**Scenario A — Metrics is the right starting pillar:**
The alert itself came from a metric. At this stage, you want to understand the _scope_ of the problem. Query: `sum by (endpoint, method) (rate(http_requests_total{status=~"5.."}[5m]))` — this shows which endpoints are failing. Information gap: metrics don't tell you _what_ errors are being thrown or _why_.

**Scenario B — Logs are the right pillar:**
Now you know errors are happening; you need the "what" — the error messages and context. Search: filter logs for `level=ERROR` in the time window of the incident. A structured log query like `error_type:* AND endpoint:/checkout AND timestamp:[now-30m TO now]` surfaces the specific error messages. Information gap: logs tell you the error message but not _which service in a chain_ is the ultimate source.

**Scenario C — Traces are the right pillar:**
"Database connection timeout" could come from any service. A trace shows the full call graph: API Gateway → Order Service → Inventory Service (with its own DB call) → Payment Service (with its own DB call). The trace immediately shows which service's DB call is slow (the span will show high duration). Information gap: traces don't show you error messages in full detail — you'd still want to cross-reference logs for the specific DB error.

**Alternative approaches:**
In a monolith, Scenario C might be solvable with logs alone (add a log entry at the DB call site). But in a microservices architecture, you cannot add instrumentation to a service you don't own — traces are the only tool that works across service boundaries.

</details>

---

## Exercise 4: Design a Feature Flag [🟡 Medium] [2 pts]

### Context
You are building a feature flag system for a new checkout experience. You need to decide how to implement the flag, what types of targeting you need, and how to handle the rollout safely.

### Task
Design a feature flag for rolling out a new payment form to production users. Your design must answer:

1. **Flag type:** Should this be a boolean flag or a percentage-based rollout? Why?
2. **Targeting rules:** Who should get the flag first? Design at least 3 targeting rules in priority order (e.g., "employees first, then beta users, then 5% of general users").
3. **Rollout plan:** Write out the rollout stages as a numbered list with the criteria for advancing to the next stage.
4. **Kill switch:** What condition would cause you to immediately set the flag to 0% (no users)?
5. **Cleanup:** When is it safe to remove the flag entirely and delete the old code path?

### Requirements
- [ ] All 5 questions answered
- [ ] Targeting rules are in a sensible priority order
- [ ] Rollout plan includes observable success criteria for each stage
- [ ] Kill switch condition is specific (not just "if there are bugs")
- [ ] Cleanup criteria are specific and verifiable

### Hints
<details>
<summary>Hint 1</summary>

For the rollout plan, think about what metrics you would check at each stage before advancing. "Error rate stays below 0.5%" is a specific criterion; "seems fine" is not.

</details>

### Expected Output / Acceptance Criteria
A thoughtful design document (bullet points acceptable) that demonstrates understanding of safe progressive rollout principles.

### Solution
<details>
<summary>Show Solution</summary>

**1. Flag type:** Percentage-based rollout. A boolean flag is for on/off with no gradual exposure — not appropriate here because we want to limit blast radius. A percentage-based flag lets us verify the new form works for small groups before full exposure.

**2. Targeting rules (in priority order):**
1. Internal employees (`user.is_employee == true`) — always on; no production risk since employees know it's experimental
2. Beta program members (`user.beta_program == true`) — these users have opted in to early access; their higher tolerance for issues is known
3. 1% of general users (random, stable hash-based assignment)
4. Gradually expand general users: 5% → 25% → 50% → 100%

**3. Rollout stages:**
- Stage 1 (Day 0): Employees + beta users. Success criteria: error rate on /checkout stays below 0.5% for 48 hours; no P1/P2 bugs reported
- Stage 2 (Day 3): Add 1% random users. Success criteria: error rate remains < 0.5%; p99 latency within 10% of old form; zero data integrity issues; 24-hour observation
- Stage 3 (Day 5): 5% general users. Success criteria: same as Stage 2 + no increase in cart abandonment rate
- Stage 4 (Day 10): 25% → 50% → 100% at 24-hour intervals, same criteria each time

**4. Kill switch condition (immediate rollback to 0%):**
Any of the following triggers an immediate kill switch:
- Error rate on /checkout exceeds 2% (double the SLO threshold)
- Payment success rate drops below 98% (data integrity risk)
- Any confirmed data loss or double-charge incident
- p99 checkout latency exceeds 5 seconds (major UX degradation)

**5. Cleanup criteria:**
Safe to remove the flag when ALL of the following are true:
1. 100% rollout has been stable for at least 14 days with no flag-related incidents
2. Old code path (flag=false branch) has zero remaining dependencies
3. No A/B test analysis is still pending
4. Rollback plan documented in the relevant post-rollout retro

</details>

---

## Exercise 5: Instrument a Minimal Flask App [🔴 Hard] [3 pts]

### Context
You have a minimal Flask API. Your task is to add Prometheus metrics instrumentation that would allow you to detect a checkout SLO breach. This is a multi-step practical exercise requiring you to write runnable code.

### Task
Given this stub Flask application, add instrumentation to make it observable:

```python
# starter: app.py
from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)

@app.route('/api/checkout', methods=['POST'])
def checkout():
    # Simulates variable latency
    time.sleep(random.uniform(0.01, 0.5))
    # Simulates ~5% error rate
    if random.random() < 0.05:
        return jsonify({"error": "payment_failed"}), 500
    return jsonify({"order_id": random.randint(1000, 9999)}), 200

@app.route('/api/products', methods=['GET'])
def products():
    time.sleep(random.uniform(0.005, 0.05))
    return jsonify({"products": ["a", "b", "c"]}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

Add:
1. A Counter for total HTTP requests with `method`, `endpoint`, and `status` labels
2. A Histogram for request latency with `endpoint` label and appropriate buckets
3. A `/metrics` endpoint for Prometheus scraping
4. A decorator or middleware that automatically instruments all routes (not per-route manual calls)
5. Write a PromQL query that would fire an alert when the checkout error rate exceeds 1%

### Requirements
- [ ] Counter defined with correct metric name, help text, and labels
- [ ] Histogram defined with appropriate buckets for web request latency
- [ ] All routes automatically instrumented (no manual inc() calls in each route)
- [ ] `/metrics` endpoint returns Prometheus-format output
- [ ] PromQL alert query correctly calculates error rate for /api/checkout

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

Flask's `before_request` and `after_request` hooks run around every request. Use `before_request` to record the start time, and `after_request` to calculate latency and increment the counter with the response's status code.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

For the error rate PromQL query, you need to divide "requests with 5xx status" by "total requests" for the specific endpoint. Use `rate()` with a 5-minute window and `{endpoint="/api/checkout"}` label filter.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```python
# Structure hint:
@app.before_request
def start_timer():
    request._start_time = time.time()  # Store start time

@app.after_request
def record_metrics(response):
    latency = time.time() - request._start_time
    # Use response.status_code to get the status
    # Use request.method, request.path for labels
    return response
```

</details>

### Expected Output / Acceptance Criteria
- Running `curl localhost:5000/metrics` returns Prometheus-format output with both metrics
- After sending 100 requests to `/api/checkout`, the metrics show ~5 errors
- The PromQL alert query, when evaluated, returns > 0.01 when error rate is above 1%

### Solution
<details>
<summary>Show Solution</summary>

```python
# app.py — instrumented Flask application

from flask import Flask, jsonify, request
from prometheus_client import (
    Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
)
import random
import time

app = Flask(__name__)

# --- Prometheus Metric Definitions ---

# Counter: tracks total number of HTTP requests
# Labels: method (GET/POST), endpoint (/api/checkout), status (200/500)
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests processed',
    ['method', 'endpoint', 'status']
)

# Histogram: tracks the distribution of request latency
# Buckets: chosen to be meaningful for web request latency (in seconds)
# Rule of thumb: include your SLO target latency as a bucket boundary
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# --- Automatic Instrumentation via Flask Hooks ---

@app.before_request
def start_timer():
    """Record the request start time for latency calculation."""
    request._start_time = time.time()

@app.after_request
def record_metrics(response):
    """Instrument every request with latency and count metrics."""
    if request.path == '/metrics':
        # Don't instrument the metrics endpoint itself
        return response

    latency = time.time() - request._start_time

    # Record latency for this endpoint
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)

    # Increment request counter with method, endpoint, and status code
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=str(response.status_code)
    ).inc()

    return response

# --- Application Routes ---

@app.route('/api/checkout', methods=['POST'])
def checkout():
    time.sleep(random.uniform(0.01, 0.5))
    if random.random() < 0.05:
        return jsonify({"error": "payment_failed"}), 500
    return jsonify({"order_id": random.randint(1000, 9999)}), 200

@app.route('/api/products', methods=['GET'])
def products():
    time.sleep(random.uniform(0.005, 0.05))
    return jsonify({"products": ["a", "b", "c"]}), 200

# --- Metrics Endpoint ---

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics for scraping."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(port=5000)
```

**PromQL alert query for checkout error rate > 1%:**
```promql
# This expression returns the error rate for /api/checkout
# It fires (returns > 0.01) when error rate exceeds 1%
(
  sum(rate(http_requests_total{endpoint="/api/checkout", status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total{endpoint="/api/checkout"}[5m]))
) > 0.01
```

**Step-by-step explanation:**

1. `before_request` runs before every route handler, recording the start time on the request object
2. `after_request` runs after every route handler, calculating the elapsed time and recording both metrics
3. The `if request.path == '/metrics'` check prevents the metrics endpoint itself from being counted
4. The PromQL query divides 5xx request rate by total request rate, then checks if it exceeds 0.01 (1%)

**Why this approach:**
Using Flask hooks instead of per-route instrumentation means every new route is automatically tracked. This is crucial for completeness — if you forget to add instrumentation to one route, it's invisible. The hook approach eliminates that risk.

**What a weaker solution looks like and why it fails:**
A weaker solution puts `REQUEST_COUNT.labels(...).inc()` in each route handler. This is error-prone (you'll forget to add it to new routes), requires code changes to add new labels, and duplicates code. The hook approach is DRY and automatic.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 | — | —/1 | — | — |
| Exercise 2 | — | —/1 | — | — |
| Exercise 3 | — | —/2 | — | — |
| Exercise 4 | — | —/2 | — | — |
| Exercise 5 | — | —/3 | — | — |
| **Total** | | **—/9** | | |

**Passing threshold:** 6/9 (67%). Aim for 8/9 (89%) before taking the test.
