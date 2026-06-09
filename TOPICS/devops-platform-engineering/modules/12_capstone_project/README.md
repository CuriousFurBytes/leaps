# Module 12: Capstone Project

> A realistic internal developer platform slice that integrates infrastructure, ci/cd, observability, and operational runbooks.

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

A realistic internal developer platform slice that integrates infrastructure, ci/cd, observability, and operational runbooks. This module gives you a practical mental model before adding more tools. The emphasis is on decisions, feedback loops, and operational clarity.

A platform engineer should be able to explain both the command being run and the organizational problem it solves. That balance prevents tool-first learning and prepares you to adapt as stacks change.

## Prerequisites

- Module 11 in this topic.
- Basic terminal literacy and willingness to run small commands locally.

## Objectives

By the end of this module, you will be able to:
- Explain the purpose of this layer of DevOps/platform work.
- Implement small, reviewable Markdown or shell-based scaffolds.
- Debug common misunderstandings before they become production habits.
- Connect this module to adjacent platform engineering concerns.

## Theory

The capstone is a build module, not a lecture module. Your goal is to design a small internal developer platform for a team that runs one HTTP service. The platform should let a developer commit code, receive automated feedback, deploy to a controlled runtime, view health and logs, and follow a runbook when the service fails. The artifact can be a repository, design document, scripts, diagrams, and demonstration notes.

Platform engineering emerged because ad hoc DevOps practices did not scale well across many teams. A single expert could automate a deployment for one service, but an organization with dozens of services needs reusable paths, documentation, ownership boundaries, and guardrails. Treat your platform as a product: name the users, define the jobs they need done, and choose a narrow first version that makes their work safer and easier.

```bash
# Example smoke-test contract for the capstone service.
# A platform pipeline can run this after deployment to decide whether to continue.
curl -fsS "http://localhost:8080/health"
```

```yaml
# Example minimal service metadata a platform could consume.
# Keep metadata boring, explicit, and reviewable.
service: example-api
owner: platform-learner
runtime: container
slo:
  availability: "99.5%"
```

```bash
# Example rollback interface; your implementation can be a script or documented command.
# The important part is that recovery is practiced before an incident.
./platform rollback example-api --to previous
```


## Key Concepts

- **Feedback loop:** A path from action to evidence. Fast feedback lets teams correct mistakes while context is still fresh.
- **Golden path:** A supported, documented way to build or operate a service. It should be easy enough that teams prefer it voluntarily.
- **Guardrail:** A control that prevents or detects unsafe behavior without requiring every developer to memorize every rule.
- **Runbook:** A written operational procedure for diagnosis or recovery. A good runbook is practiced before it is needed.
- **Service ownership:** The expectation that a team understands how its software is built, deployed, observed, and supported.

## Examples

### Scenario: Golden Path for a Small API

Problem: a product developer needs to ship a simple API without hand-building every operational concern.

```yaml
# platform-request.yaml
service: orders-api
language: python
exposes_http: true
needs_database: false
```

A good platform turns that small request into a predictable workflow: repository checks, image build, deployment, health check, dashboards, and rollback instructions. The tradeoff is scope discipline: a narrow golden path is more useful than a universal platform that nobody can finish.

### Help and Getting Unstuck

Use these staged hints only when blocked. They are meant to restore momentum, not to provide a full solution.

1. If the scope feels too large, support exactly one service and one environment.
2. If CI/CD feels unclear, draw the pipeline as stages: lint, test, build, scan, deploy, verify.
3. If observability feels unclear, start with three signals: health endpoint, structured logs, and one latency metric.
4. If security feels unclear, list every secret and explain where it should live and who can read it.
5. If the platform product feels unclear, write a one-page README for developers before adding more automation.


## Common Pitfalls

### Pitfall 1: Automating an Unknown Manual Process

Wrong approach:

```bash
# This hides risk because nobody wrote down what each step assumes.
./mystery-deploy.sh
```

Correct approach:

```bash
# Start with explicit checks that reveal assumptions.
git status --short
curl -fsS "http://localhost:8080/health"
```

Teams make this mistake because automation feels like progress. The safer path is to document and verify the manual process first.

### Pitfall 2: Treating Tools as the Goal

Wrong approach:

```yaml
# Tool names without a delivery problem are not a strategy.
tools:
  - kubernetes
  - terraform
  - prometheus
```

Correct approach:

```yaml
# Start from outcomes, then choose tools.
outcomes:
  - repeatable deployments
  - observable service health
  - reversible changes
```

Tools matter, but only after you understand the operational outcome they support.

### Pitfall 3: Ignoring the Human User

Wrong approach:

```text
Build a platform with every possible option exposed.
```

Correct approach:

```text
Build one documented path for one common service type, then improve it from feedback.
```

Internal platforms fail when they optimize for theoretical completeness instead of developer experience.

## Cross-Links

- [[devops-platform-engineering]]
- [[linux]]
- [[networking]]
- [[cloud-computing]]
- [[security]]

## Summary

- DevOps/platform engineering is about improving the whole delivery and operations loop.
- Reliable systems combine automation, controls, feedback, and human-readable procedures.
- Small, explicit examples are better than large hidden scripts when learning.
- Platform work should be evaluated by user outcomes, not tool count.
- Later modules deepen these ideas through infrastructure, runtime, observability, and governance.
