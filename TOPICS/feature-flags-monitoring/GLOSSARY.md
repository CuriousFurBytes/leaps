# Feature Flags, System Monitoring, and Developer Experience — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in this context.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use.
```

Keep definitions in your own words as much as possible.

---

## A

### alerting fatigue

**Definition:** The state reached when an on-call engineer receives so many alerts — especially noisy, low-signal, or non-actionable ones — that they begin ignoring them. Alert fatigue is a leading cause of missed incidents and a symptom of poorly tuned alerting thresholds.

**Also known as:** alert noise, alert overload

**Related:** [[shared/glossary#alert]], SLO, error budget

**Example:**
A team with 200 Prometheus alert rules, 80% of which fire every week without causing user-visible impact, will see their on-call engineers begin silencing alerts rather than investigating them. The fix is to delete or tune alerts so that every firing alert is urgent and actionable.

---

## C

### canary deployment

**Definition:** A release strategy where a new version of a service is rolled out to a small percentage of production traffic (the "canary") before being promoted to all traffic. If the canary shows no regression in error rate, latency, or business metrics, the rollout proceeds. If it does regress, the canary is reverted with minimal user impact.

**Also known as:** canary release, staged rollout

**Related:** progressive rollout, feature flag, blue-green deployment

**Example:**
Sending 5% of HTTP requests to `v2` of a service while monitoring error rate and p99 latency. If both metrics remain within SLO for 30 minutes, gradually increase to 25%, 50%, and then 100%.

---

### cardinality

**Definition:** In the context of time-series databases (especially Prometheus), cardinality refers to the number of unique label-value combinations for a metric. High cardinality metrics — such as those with a `user_id` label on a service with millions of users — cause Prometheus to create millions of time series, leading to out-of-memory errors and slow queries.

**Also known as:** label cardinality, series cardinality

**Related:** Prometheus, labels, time series

**Example:**
`http_requests_total{method="GET", status="200"}` — 2 labels with ~10 unique combinations = low cardinality. `http_requests_total{user_id="12345"}` — 1 label with millions of unique values = catastrophically high cardinality.

---

### correlation ID

**Definition:** A unique identifier attached to a request at its entry point (e.g., an API gateway) and propagated through every downstream service call. When logs across multiple services share the same correlation ID, engineers can reconstruct the complete request path — enabling distributed debugging without a full tracing solution.

**Also known as:** request ID, trace ID (loosely), X-Request-ID

**Related:** distributed tracing, span, OpenTelemetry

**Example:**
A browser sends an HTTP request; the API gateway generates `correlation_id: "abc123"` and passes it as an HTTP header to every microservice it calls. Each service logs this ID. When a failure occurs, filtering all logs by `"abc123"` reveals the complete failure path.

---

## D

### DX (Developer Experience)

**Definition:** The quality of the environment in which software engineers work. DX encompasses build speed, test reliability, deployment pipeline health, internal tooling usability, documentation quality, and cultural practices. High DX means engineers spend most of their time on value-adding work; low DX means engineers lose time to slow builds, flaky tests, and poor tooling.

**Also known as:** developer productivity, developer ergonomics

**Related:** DORA metrics, SPACE framework, inner loop

**Example:**
If a developer must wait 20 minutes to run the test suite after every code change, the inner loop is slow and DX is poor. If the same tests take 2 minutes and provide clear, actionable failure messages, DX is good — developers can iterate faster and with higher confidence.

---

## E

### error budget

**Definition:** The amount of downtime or errors a service is allowed to have in a given period while still meeting its SLO. If a service has a 99.9% availability SLO over 30 days, its error budget is 0.1% of 30 days = 43.2 minutes. The error budget is "spent" when the service experiences incidents; when it runs out, teams shift focus from feature development to reliability work.

**Also known as:** reliability budget

**Related:** SLO, SLA, SLI

**Example:**
If a service with a 99.9% monthly SLO has already experienced 40 minutes of downtime in week 2, only 3.2 minutes of error budget remain for the rest of the month. The team should pause risky deployments.

---

## F

### feature flag

**Definition:** A runtime conditional in application code that controls whether a feature is enabled or disabled, and for which users. Feature flags allow teams to deploy code to production without releasing it to users, enabling dark launches, gradual rollouts, A/B experiments, and instant kill switches without redeployment.

**Also known as:** feature toggle, feature switch, feature gate, experiment flag

**Related:** progressive rollout, canary deployment, A/B testing

**Example:**
```python
if posthog.feature_enabled("new_checkout_flow", user_id):
    return render_new_checkout()
else:
    return render_old_checkout()
```
This flag can be set to true for 5% of users, then 25%, then 100% — with no code changes or redeployments.

---

## M

### MTTD (Mean Time to Detect)

**Definition:** The average time between when an incident begins (a service starts misbehaving) and when the monitoring system or an engineer detects it. Lower MTTD means faster awareness and shorter total incident duration. Improving MTTD requires better alerting coverage and lower alert latency.

**Also known as:** mean time to detection

**Related:** MTTR, SLI, alerting fatigue

**Example:**
If a database starts returning errors at 14:00 and the on-call engineer receives an alert at 14:08, the MTTD for this incident is 8 minutes.

---

### MTTR (Mean Time to Recover)

**Definition:** The average time between when an incident is detected and when the service is fully restored. MTTR measures how quickly a team can respond to and resolve incidents. Improving MTTR requires runbooks, playbooks, automated rollback, and practiced incident response.

**Also known as:** mean time to recovery, mean time to repair, mean time to restore

**Related:** MTTD, incident response, runbook

**Example:**
If a team detects an incident at 14:08 and restores full service at 14:35, the MTTR for that incident is 27 minutes. Industry targets vary; many teams aim for MTTR under 30 minutes for P1 incidents.

---

## P

### progressive rollout

**Definition:** A deployment strategy where a new version of a feature or service is released to an increasing percentage of users over time, with automatic or manual checks between each stage. If any stage shows degradation, the rollout is paused or reversed. Progressive rollout reduces the blast radius of bad deployments.

**Also known as:** gradual rollout, percentage-based rollout, phased deployment

**Related:** canary deployment, feature flag, error budget

**Example:**
`0% → 1% → 5% → 25% → 50% → 100%` with 15-minute observation windows between stages. At each stage, error rate and p99 latency are checked. If either metric regresses beyond a threshold, the rollout halts.

---

## S

### SLA (Service Level Agreement)

**Definition:** A formal, contractual agreement between a service provider and a customer that specifies the minimum acceptable level of service. SLAs define consequences (credits, penalties) if the service falls below the agreed threshold. SLAs are typically less strict than internal SLOs to allow for buffer.

**Also known as:** service agreement, uptime guarantee

**Related:** SLO, SLI, error budget

**Example:**
"AWS guarantees 99.9% monthly uptime for EC2. If uptime falls below 99.0%, customers receive a 10% service credit." This is an SLA — a legally binding commitment with financial consequences.

---

### SLI (Service Level Indicator)

**Definition:** A quantitative measurement of a specific aspect of service quality. SLIs are the raw metrics that feed into SLOs. Common SLIs include request success rate, latency percentiles (p50, p95, p99), and throughput. A good SLI directly reflects user experience.

**Also known as:** service indicator

**Related:** SLO, SLA, Prometheus, error budget

**Example:**
`(http_requests_total{status!~"5.."} / http_requests_total) * 100` expressed as a percentage over 5 minutes is an SLI for "what fraction of requests succeeded in the last 5 minutes."

---

### SLO (Service Level Objective)

**Definition:** An internal target for a specific SLI over a defined time window. SLOs represent the team's commitment to its users and define the error budget. A service "meets its SLO" when its SLI is at or above the target for the window. SLOs are set more strictly than SLAs.

**Also known as:** service objective, reliability target

**Related:** SLI, SLA, error budget

**Example:**
"99.9% of HTTP requests should succeed (return non-5xx status) over any 30-day rolling window." This SLO implies an error budget of 43.2 minutes of downtime per month. If the team wants an SLA of 99.5%, they would set their internal SLO at 99.9% to maintain buffer.

---

## T

### trace

**Definition:** A complete record of a request's journey through a distributed system, from the first service it enters to the last. A trace is composed of spans — individual units of work — linked by a trace ID. Traces are the primary tool for debugging latency and errors in microservice architectures.

**Also known as:** distributed trace, request trace

**Related:** span, correlation ID, OpenTelemetry, Jaeger

**Example:**
A user clicks "checkout." The browser sends a request to the API gateway (span 1), which calls the cart service (span 2), which calls the payment service (span 3), which calls the payment processor (span 4). All four spans share the same trace ID and together form a complete trace showing total latency and any errors in the chain.

---

### span

**Definition:** A single unit of work within a distributed trace, representing one operation in one service. Each span has a start time, duration, operation name, service name, status (success/error), and a set of attributes. Spans are linked to form a trace via parent-child relationships.

**Also known as:** trace span

**Related:** trace, OpenTelemetry, correlation ID

**Example:**
In a trace for a checkout request, `payment-service: charge_card` is a span that starts at 14:05:00.123 and ends at 14:05:00.267 (144ms duration). It has attributes like `payment.provider: "stripe"` and `payment.amount: 49.99`.

---

## Symbols and Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| `p99` | 99th percentile latency | `p99 = 450ms` means 99% of requests complete within 450ms |
| `p50` | 50th percentile (median) latency | `p50 = 50ms` means half of requests complete within 50ms |
| `SLO%` | Service Level Objective as a percentage | `99.9%` availability SLO |
| `{label="value"}` | Prometheus label selector syntax | `{job="api", status="200"}` |
| `rate()` | PromQL rate function — per-second rate over a window | `rate(http_requests_total[5m])` |

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
