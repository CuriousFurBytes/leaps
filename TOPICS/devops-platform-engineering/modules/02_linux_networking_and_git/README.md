# Module 02: Linux, Networking, and Git

> The operating-system, network, and version-control fundamentals that every platform engineer uses daily.

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

The operating-system, network, and version-control fundamentals that every platform engineer uses daily. This module gives you a practical mental model before adding more tools. The emphasis is on decisions, feedback loops, and operational clarity.

A platform engineer should be able to explain both the command being run and the organizational problem it solves. That balance prevents tool-first learning and prepares you to adapt as stacks change.

## Prerequisites

- Module 01 in this topic.
- Basic terminal literacy and willingness to run small commands locally.

## Objectives

By the end of this module, you will be able to:
- Explain the purpose of this layer of DevOps/platform work.
- Implement small, reviewable Markdown or shell-based scaffolds.
- Debug common misunderstandings before they become production habits.
- Connect this module to adjacent platform engineering concerns.

## Theory

DevOps and platform engineering are responses to a coordination problem: software only creates value after it is running reliably for users. Historically, many organizations separated developers, who wrote code, from operations teams, who deployed and ran it. That separation created slow handoffs, incomplete ownership, and repeated failures because each group optimized for local goals. DevOps emphasized shared responsibility, automation, measurement, and fast feedback. Platform engineering adds a product mindset by building reusable internal capabilities that make good operational practices easier to adopt.

A useful mental model is that every delivery system has inputs, transformations, controls, and feedback. Source code is an input. Tests, builds, security scans, and deployments are transformations. Approvals, policies, secrets, and access controls are controls. Logs, metrics, traces, alerts, and user reports are feedback. A platform engineer improves the whole loop rather than treating each tool as an isolated gadget.

```bash
# Inspect repository state before automating anything.
# Automation should make known manual steps repeatable, not hide confusion.
git status --short
```

```bash
# A simple health check creates a machine-readable feedback signal.
# The -f flag makes curl exit nonzero for HTTP errors.
curl -fsS "http://localhost:8080/health"
```

```yaml
# A tiny pipeline sketch shows the intent before tool-specific syntax takes over.
stages:
  - test
  - build
  - deploy
  - verify
```

The most important habit is to ask what failure mode a practice reduces. Version control reduces uncertainty about changes. CI reduces uncertainty about whether code still works. Infrastructure as code reduces uncertainty about how an environment was created. Observability reduces uncertainty after deployment. Incident response reduces uncertainty under stress. Platform work is the deliberate act of turning these practices into a paved road that teams can understand and trust.


## Key Concepts

- **Feedback loop:** A path from action to evidence. Fast feedback lets teams correct mistakes while context is still fresh.
- **Golden path:** A supported, documented way to build or operate a service. It should be easy enough that teams prefer it voluntarily.
- **Guardrail:** A control that prevents or detects unsafe behavior without requiring every developer to memorize every rule.
- **Runbook:** A written operational procedure for diagnosis or recovery. A good runbook is practiced before it is needed.
- **Service ownership:** The expectation that a team understands how its software is built, deployed, observed, and supported.

## Examples

### Scenario: Turning a Manual Deployment into a Checklist

Problem: a team deploys by remembering shell commands from chat history.

```bash
# First safe step: record the deployment inputs before automating them.
APP_NAME="example-api"
IMAGE_TAG="2026-06-09-demo"
echo "Deploying ${APP_NAME}:${IMAGE_TAG}"
```

This is not a complete deployment system, but it makes hidden assumptions visible. From here, you can add validation, tests, rollback, and audit logs.


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
