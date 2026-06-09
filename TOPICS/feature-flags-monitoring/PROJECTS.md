# Feature Flags, System Monitoring, and Developer Experience — Projects

> Project-based learning cements knowledge in a way that reading and exercises alone cannot.
> Building something real forces you to confront gaps in your understanding and make decisions
> that tutorials never put in front of you.

---

## How to Use This File

1. Choose a project at or slightly above your current level.
2. **Don't use tutorials for your chosen project.** Tutorials are for learning, projects are for applying.
3. Document your attempt using the [Project Attempt Template](#project-attempt-template) at the bottom.
4. When you finish, link the result (repo, demo) in the table in the topic README.

---

## Beginner Projects

_Focus: get comfortable with the core tools and vocabulary._
_Complete at least one before advancing past Phase 1._

### B1: Instrument a Flask App with Prometheus

**Description:** Take an existing (or simple new) Flask application and add Prometheus metrics to it. Expose a `/metrics` endpoint, define at least 3 meaningful metrics (a counter for requests, a histogram for request latency, and a gauge for something application-specific), and visualize them in Grafana.

**Concepts Reinforced:**
- Prometheus metric types (counter, histogram, gauge)
- The `prometheus_client` Python library
- Grafana data source configuration and panel creation

**Estimated Time:** 4–6 hours

**Starting Point:** A minimal Flask "hello world" app, or any existing Python web app

**Success Criteria:**
- [ ] App exposes `/metrics` endpoint consumed by Prometheus
- [ ] At least 3 metric types implemented with meaningful labels
- [ ] Grafana dashboard shows all 3 metrics with appropriate visualizations
- [ ] One alert rule configured that would fire under a simulated error condition
- [ ] The project runs without errors

---

### B2: Basic Sentry Integration

**Description:** Add Sentry error tracking to a Python script or web application. Deliberately trigger several different error types, confirm they appear in Sentry, and configure at least one alert rule. Document what information Sentry captures automatically vs. what requires manual instrumentation.

**Concepts Reinforced:**
- Sentry SDK initialization and basic configuration
- Automatic vs. manual error capture
- Error grouping and issue triage in the Sentry UI

**Estimated Time:** 3–4 hours

**Starting Point:** Any Python script or web app with potential error paths

**Success Criteria:**
- [ ] Sentry SDK initialized with correct DSN and environment tags
- [ ] At least 3 distinct error types captured and visible in Sentry
- [ ] At least one custom `capture_message` and one `set_extra` call added
- [ ] One Sentry alert rule configured

---

### B3: Feature Flag with a Simple Toggle

**Description:** Implement a minimal feature flag system from scratch (without a dedicated flag service) that reads flag state from a JSON file or environment variable. Wrap a feature in the flag so it can be enabled/disabled without redeployment. Then refactor to use PostHog's feature flag SDK and compare the two approaches.

**Concepts Reinforced:**
- The concept of separating deployment from release
- Basic flag implementation patterns
- PostHog SDK initialization and `feature_enabled()` usage

**Estimated Time:** 4–5 hours

**Starting Point:** Blank file or any existing Python application

**Success Criteria:**
- [ ] Homegrown flag toggles a feature on/off via config change (no redeploy)
- [ ] PostHog SDK version achieves the same with remote flag management
- [ ] Written comparison of the two approaches (3–5 sentences)

---

## Intermediate Projects

_Focus: combine multiple concepts, handle edge cases, write clean code._
_Complete at least one before completing Phase 2._

### I1: Full Observability Stack for a REST API

**Description:** Build a REST API (Python + FastAPI or Flask) and instrument it with the complete observability stack: Prometheus metrics, Sentry error tracking, and structured JSON logging with correlation IDs. Set up Grafana to display the metrics with a realistic SLO dashboard including error rate and latency percentiles.

**Concepts Reinforced:**
- Prometheus metrics (counter, histogram)
- Sentry SDK with release tracking
- Structured logging with correlation ID propagation
- Grafana SLO dashboard design
- SLI/SLO calculation

**Estimated Time:** 10–14 hours

**Starting Point:** A FastAPI or Flask app scaffold; Docker Compose to run Prometheus and Grafana locally

**Success Criteria:**
- [ ] API tracks request count, error rate, and latency histogram per endpoint
- [ ] Sentry captures unhandled exceptions with release version tag
- [ ] Every log entry includes a correlation ID matching the request
- [ ] Grafana dashboard shows error rate SLI and latency p50/p99
- [ ] Grafana alert fires if error rate exceeds 1% over 5 minutes
- [ ] Code is clean, readable, and commented

---

### I2: OpenTelemetry Trace Propagation Between Two Services

**Description:** Build two minimal services (service A calls service B) and instrument both with OpenTelemetry. Implement trace context propagation via HTTP headers so that a single user request results in a trace spanning both services. Export traces to a local Jaeger instance and inspect the trace waterfall.

**Concepts Reinforced:**
- OpenTelemetry SDK initialization
- Manual span creation and attribute setting
- W3C Trace Context header propagation
- Jaeger trace visualization

**Estimated Time:** 8–10 hours

**Starting Point:** Two FastAPI stubs; Docker Compose for Jaeger

**Success Criteria:**
- [ ] Both services instrumented with OTel SDK
- [ ] A single request to service A produces a trace with spans from both services
- [ ] Trace visible in Jaeger with correct parent-child span relationships
- [ ] At least one custom span attribute per service (e.g., `user.id`, `db.query`)

---

### I3: PostHog Funnel Analysis

**Description:** Add PostHog tracking to a multi-step user flow (e.g., a 3-step registration flow, a checkout flow, or a survey). Track events at each step, build a funnel in PostHog to visualize drop-off, and implement a feature flag that changes the flow for 50% of users. Compare completion rates between the two variants.

**Concepts Reinforced:**
- PostHog event schema and SDK usage
- Funnel analysis and drop-off interpretation
- A/B testing with PostHog feature flags
- Statistical interpretation of experiment results

**Estimated Time:** 6–8 hours

**Starting Point:** A multi-step HTML/JS form or Python web app

**Success Criteria:**
- [ ] Events tracked at every step of the flow with relevant properties
- [ ] Funnel created in PostHog showing step-by-step conversion
- [ ] Feature flag implemented splitting users into control and variant
- [ ] Written interpretation of the A/B test results (what would you do next?)

---

## Advanced Projects

_Focus: tackle realistic, open-ended problems. No hand-holding._
_Complete at least one to reach Applied Practitioner status._

### A1: Production-Grade SLO Dashboard

**Description:** Design and build a Grafana dashboard that tracks SLOs for a realistic multi-endpoint API. The dashboard must show error budgets (not just raw error rates), p99 latency trends, burn rate alerts (alerting before the error budget is exhausted), and a 30-day rolling availability window. Write the dashboard in dashboard-as-code using Grafonnet or raw JSON.

**Why This Is Hard:**
Burn rate alerting requires composing multiple PromQL expressions, and dashboard-as-code requires learning Grafonnet's Jsonnet-based DSL. Getting the error budget maths right requires careful SLO design and query validation.

**Concepts Reinforced:**
- Error budget calculation in PromQL
- Burn rate alerting (Google SRE Chapter 5 method)
- Grafana variables and templating
- Dashboard-as-code with Grafonnet
- SLO window calculation (30-day rolling)
- Prometheus recording rules for performance

**Estimated Time:** 15–20 hours

**Starting Point:** An instrumented API (from I1 or new), Prometheus, Grafana

**Success Criteria:**
- [ ] Dashboard shows current error budget remaining as a percentage
- [ ] Burn rate alert fires before error budget is fully exhausted
- [ ] Dashboard is parameterized with Grafana variables (environment, service)
- [ ] Dashboard definition is committed as code (JSON or Grafonnet)
- [ ] All PromQL queries have recording rules for performance
- [ ] You can explain every design decision you made

---

### A2: Incident Response Simulation

**Description:** Design and conduct a full incident response simulation. Define at least one SLO for a service, write a runbook for a plausible failure scenario, inject the failure (e.g., a deliberate error rate spike), trigger the alerting chain, work through the runbook, mitigate the failure, and write a blameless post-mortem.

**Why This Is Hard:** Running a realistic incident simulation requires setting up the full alerting chain (Prometheus → Alertmanager → notification), writing a runbook that is actually useful under pressure, and conducting a post-mortem that identifies systemic causes rather than individual blame.

**Concepts Reinforced:**
- Prometheus Alertmanager configuration
- Runbook writing
- Blameless post-mortem structure
- Incident command roles
- Alert hygiene

**Estimated Time:** 12–16 hours

**Success Criteria:**
- [ ] SLO defined and recorded in Prometheus
- [ ] Alertmanager configured to send a notification when SLO is breached
- [ ] Runbook written with diagnosis steps, mitigation steps, and escalation path
- [ ] Incident simulation conducted and documented (timeline + decisions made)
- [ ] Post-mortem written following the blameless format from Module 10
- [ ] Action items identified with owners and timelines

---

## Expert / Capstone Projects

_Focus: synthesize everything. Build something you're proud to show others._
_Complete one to earn Topic Mastery status._

### E1: Fully Instrumented Multi-Service Application

**Description:** Build or adapt a multi-service application (at least 3 services: e.g., API gateway + backend service + background worker) and instrument it with the complete observability stack: Prometheus metrics (with Grafana SLO dashboard), Sentry error tracking, OpenTelemetry distributed traces, PostHog product analytics, and feature flags controlling at least one feature. Write a complete runbook for at least two failure scenarios.

**Why This Is a Capstone:**
This project requires mastery of all major topic areas. You cannot complete it with gaps — they will surface quickly. Expect to revisit earlier modules during the build. Integrating all the tools into a coherent system requires judgment that no individual module can teach.

**Core Requirements:**
- [ ] Uses concepts from at least 8 different modules
- [ ] Is non-trivial in scope (not achievable in a single sitting)
- [ ] Is documented clearly enough that someone else could understand it
- [ ] Includes a write-up explaining your design decisions and what you learned
- [ ] All services emit Prometheus metrics consumed by a single Grafana SLO dashboard
- [ ] All errors are captured in Sentry with releases and environments configured
- [ ] Distributed traces span all 3 services and are visible in Jaeger or Tempo
- [ ] PostHog tracks key user actions with at least one funnel analysis
- [ ] At least one feature is controlled by a feature flag with targeting rules
- [ ] Two runbooks written, one for a latency SLO breach and one for a high error rate

**Estimated Time:** 20–30 hours

**Extension Ideas (if you want more challenge):**
- Add a canary deployment pipeline using Argo Rollouts and connect it to feature flags
- Implement DataDog APM as an alternative or complement to Prometheus/Grafana
- Add a DX metrics dashboard measuring build times, deploy frequency, and MTTR for the project itself

> [!NOTE]
> The final module of this topic (Module 12: Capstone Project) is a dedicated module that walks you
> through building this for real. It gives you a brief, milestones, and a **Help / Getting
> Unstuck** section with staged hints — but it deliberately does **not** hand you a finished
> solution. The help is there so you can get past a blocker and keep going on your own, not so
> you can skip the build. Struggling productively *is* the learning here.

---

## Project Attempt Template

When you attempt a project, create a folder in this topic's directory and copy this template:

```markdown
# Project: {{PROJECT_NAME}}

**Difficulty:** Beginner / Intermediate / Advanced / Expert
**Started:** {{YYYY-MM-DD}}
**Completed:** {{YYYY-MM-DD}} (or "In progress")
**Time Spent:** {{HOURS}} hours

## What I Built

{{DESCRIPTION_OF_WHAT_YOU_ACTUALLY_BUILT}}

## Link / Location

{{LINK_TO_REPO_OR_FILE}}

## What I Learned

- {{LEARNING_1}}
- {{LEARNING_2}}
- {{LEARNING_3}}

## What Was Hard

{{WHAT_WAS_CHALLENGING_AND_HOW_YOU_SOLVED_IT}}

## What I'd Do Differently

{{HONEST_RETROSPECTIVE}}

## Concepts Used

- [[modules/01_introduction]] — how you used it
- [[modules/02_metrics-and-prometheus]] — how you used it

## Score / Self-Assessment

On a scale of 1–5, how well do I think I executed this project? {{SCORE}}/5

Justification: {{JUSTIFICATION}}
```
