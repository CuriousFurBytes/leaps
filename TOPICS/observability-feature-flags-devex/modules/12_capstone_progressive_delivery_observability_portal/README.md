# Module 12: Capstone Project: Progressive Delivery Observability Portal

> Expert module for building practical skill in safe delivery, observability, and developer experience.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

This module teaches capstone project: progressive delivery observability portal through the lens of real software delivery. The aim is to make every release observable, controllable, and understandable by the humans responsible for it.

You will practice connecting implementation decisions to operational evidence. That means flags are not merely boolean switches, dashboards are not decorative charts, and alerts are not noise machines; each is part of a feedback loop that helps teams learn safely.

## Prerequisites

- Module 11 in this topic.
- Basic familiarity with web requests, deployments, and reading structured data.
- A willingness to reason from evidence instead of trusting tool screenshots blindly.

## Objectives

By the end of this module, you will be able to:

- Explain the role of this module in a progressive delivery workflow.
- Implement small, runnable examples that model flags, telemetry, or release evidence.
- Distinguish product analytics, infrastructure monitoring, error monitoring, and dashboards.
- Design guardrails that tell a team when to advance, pause, or roll back.
- Improve developer workflows by reducing manual coordination and ambiguity.

## Theory

### Project Context

Professional teams need a shared place to answer four questions before, during, and after a release: what changed, who is exposed, what telemetry says, and what action should happen next. A progressive delivery observability portal is not a replacement for PostHog, Datadog, Sentry, or Grafana. It is a thin coordination layer that links decisions across those systems so a developer does not need to keep the entire release state in memory.

Historically, release management was tied to deployment windows and manual change boards. Continuous delivery improved speed, but speed without runtime evidence created new risk. Feature flags, observability, and product analytics emerged as complementary practices: flags control exposure, metrics and traces reveal service health, errors reveal user-facing defects, and product events reveal whether a change produces value.

Your capstone is deliberately scoped as a realistic internal platform artifact. It should model flags, owners, rollout stages, guardrail metrics, incident notes, and dashboard links. You may implement it as Markdown design documents, a small service, a static site, or a CLI-backed prototype, but it must demonstrate how an experienced team would reason about safe delivery.

### Reference Data Model

```json
{
  "flag_key": "checkout_redesign",
  "owner": "growth-platform",
  "stage": "canary",
  "exposure_percent": 10,
  "guardrails": ["error_rate", "p95_latency", "checkout_completion"],
  "links": {
    "posthog": "https://app.posthog.com/project/example/insights/checkout",
    "sentry": "https://sentry.io/organizations/example/issues/?query=checkout_redesign",
    "grafana": "https://grafana.example/d/checkout",
    "datadog": "https://app.datadoghq.com/apm/service/checkout"
  }
}
```

### Help and Getting Unstuck

Use staged help instead of copying a complete solution. First, draw the release workflow on paper. Second, choose the smallest artifact that can represent flag state, telemetry health, ownership, and rollback criteria. Third, implement one happy path and one rollback path. Finally, add a short operator guide that explains what a new engineer should do at 2 a.m. when a rollout alarm fires.


## Key Concepts

- **Progressive delivery** — Releasing changes gradually while watching evidence. It reduces blast radius and pairs naturally with feature flags.
- **Feature flag** — A runtime decision point that changes behavior without requiring a new deploy. Good flags have owners, defaults, expiry dates, and observability context.
- **Guardrail metric** — A metric that protects users or systems during experimentation. Guardrails should be chosen before rollout begins.
- **Telemetry** — Runtime data emitted by software, including metrics, logs, traces, errors, and product events. Telemetry is useful only when it supports decisions.
- **Developer experience** — The quality of the workflows developers use to build, ship, debug, and operate software. Strong DevEx makes safe behavior the easiest behavior.

## Examples

### Example: Rollout Decision Record

```yaml
flag: checkout_redesign
stage: canary
decision: continue
because:
  - error_rate stayed below 1 percent for 60 minutes
  - p95_latency increased by 12 ms, below the 50 ms guardrail
  - checkout_completion was statistically flat
next_step: raise exposure from 10 percent to 25 percent
```

This record is intentionally small. It captures enough evidence for accountability without forcing readers to reverse-engineer the decision from several dashboards.

### Example: Human-Readable Rollout Note

```markdown
- Change: checkout redesign
- Flag: checkout_redesign
- Owner: growth-platform
- Current exposure: 10 percent
- Healthy signals: p95 latency, checkout completion, Sentry issue count
- Rollback action: disable the flag globally
```

This format is simple enough to paste into an incident channel and structured enough to automate later.

## Common Pitfalls

### Pitfall 1: Treating Flags as Permanent Architecture

```yaml
# Wrong: no owner, no removal plan.
flag: new_ui
status: enabled
```

```yaml
# Better: ownership and cleanup are explicit.
flag: checkout_redesign
owner: growth-platform
expires_after: 2026-07-31
removal_issue: PLATFORM-1842
```

Long-lived flags create hidden branches in production behavior. Add ownership and expiry from the beginning.

### Pitfall 2: Alerting Without an Action

```yaml
# Wrong: noisy and vague.
alert: cpu_is_high
threshold: 70
```

```yaml
# Better: tied to user impact and response.
alert: checkout_p95_latency_high
threshold: "> 500 ms for 10 minutes"
action: "pause checkout_redesign rollout and inspect traces"
```

Alerts should point to a decision. If nobody knows what to do, the alert is unfinished work.

### Pitfall 3: Comparing Users Without Flag Context

```json
{"event":"purchase_completed","user_id":"u_123"}
```

```json
{"event":"purchase_completed","user_id":"u_123","flag_checkout_redesign":true}
```

Without exposure context, analytics cannot reliably connect user outcomes to a rollout.

## Cross-Links

- [[observability-feature-flags-devex#module-map]]
- [[devops-platform-engineering]]
- [[distributed-systems-architecture]]
- [[security-privacy-pentesting]]

## Summary

- Safe delivery depends on both control and evidence.
- Feature flags should be designed with ownership, observability, and removal in mind.
- Metrics, logs, traces, errors, and product events answer different questions.
- Developer experience improves when safe workflows are automated and obvious.
- Rollout decisions should be recorded with enough context for later learning.
