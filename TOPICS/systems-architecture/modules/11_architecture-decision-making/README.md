# Module 11: Architecture Decision-Making

[← Module 10: Scaling Patterns](../10_scaling-patterns/README.md) | [Topic Home](../../README.md) | [Next → Module 12: Capstone Project](../12_capstone-project/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-blue)
![Time](https://img.shields.io/badge/time-7h-orange)

> Architecture Decision Records (ADRs), trade-off analysis frameworks, tech debt quantification, and evolutionary architecture — how to make good architectural decisions, document them, and change your mind gracefully.

---

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

---

## Overview

All the patterns in this topic come with trade-offs. The circuit breaker adds latency. The Saga pattern makes intermediate states visible. Sharding makes cross-entity queries harder. The question is not "which pattern is best?" but "which trade-offs are acceptable for this specific system, right now, given what we know?"

This module is about the meta-skill: how to *make* and *document* architectural decisions well. Most software organizations make architectural decisions implicitly, verbally, and without documentation — which means the same debates recur when team members change, and no one remembers why the current design was chosen. Architecture Decision Records (ADRs) solve this by creating a lightweight, version-controlled log of important decisions.

The module also covers the **trade-off analysis framework** — a structured approach to evaluating options — and **evolutionary architecture**: the insight that architecture should be designed to change, not to be permanent. The fitness functions concept from "Building Evolutionary Architectures" (Ford, Parsons, Kua) provides a way to automatically test architectural properties.

---

## Prerequisites

- All previous modules — this module applies concepts from the entire topic
- Experience with real-world system design (at least through completing modules 01–10)

---

## Objectives

By the end of this module, you will be able to:

1. Write an Architecture Decision Record (ADR) for a real or hypothetical decision, including context, options, decision, and consequences
2. Apply a structured trade-off analysis framework to compare architectural options
3. Identify and quantify technical debt using the "interest rate" metaphor
4. Explain the concept of evolutionary architecture and describe what makes an architecture "evolvable"
5. Design a fitness function that automatically tests an architectural property (e.g., "no service calls the database of another service")
6. Facilitate an architecture review for a proposed design, producing actionable feedback

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a subsequent pass.

### Core Concepts to Cover

**Architecture Decision Records (ADRs):**
Proposed by Michael Nygard in 2011. A short document that records one significant architectural decision, with: context (why was a decision needed), decision (what was decided), and consequences (what will result from this decision, including downsides).

```markdown
# ADR-012: Use the Saga Pattern for Order Fulfillment

## Status
Accepted

## Context
The order fulfillment flow spans three services: Inventory, Payment, and Shipping.
We need to ensure that if the Payment step fails, the Inventory reservation is cancelled.

We evaluated:
1. Two-Phase Commit (2PC): strong consistency but blocking failure mode; our databases
   (PostgreSQL + MySQL) support XA but the operational complexity is high.
2. Choreography Saga: event-driven, no central coordinator.
3. Orchestration Saga: central OrderFulfillmentSaga service manages state.

## Decision
We will use an **Orchestration Saga** (Option 3).

**Rationale:** The fulfillment flow has 5 steps with 3 conditional branches. At this
complexity, choreography's "where is the overall state?" problem would make debugging
very difficult. The orchestrator coupling cost is acceptable given the visibility gain.

## Consequences
**Positive:**
- Single place to view the state of any in-progress fulfillment
- Clear failure handling and retry logic
- Easier to add new steps

**Negative:**
- OrderFulfillmentSaga service is a coupling point — all fulfillment participants
  depend on its command messages
- More infrastructure: the orchestrator needs persistent state storage
- If the orchestrator is unavailable, no new orders can be fulfilled (mitigated by
  making it highly available)

## Date
2026-06-09

## Authors
Engineering Team
```

**The Trade-Off Analysis Framework:**

Architectural decisions should be evaluated using a consistent framework:
1. State the problem clearly (not the solution)
2. Generate at least 3 alternatives (including "do nothing")
3. For each alternative, score on dimensions relevant to the system (performance, consistency, operational complexity, team expertise, cost)
4. Identify the decision's reversibility (one-way door vs. two-way door)
5. State the decision and its explicit costs

**Technical Debt:**
Ward Cunningham's metaphor: technical debt is work you take on for short-term speed that costs extra to service over time, like financial debt. The "interest" is the extra effort every future change requires because of the debt.

```
Technical debt categorization:
1. Deliberate-prudent: "We'll use a monolith now and refactor when we have the traffic"
2. Deliberate-reckless: "We don't have time for good design"
3. Inadvertent-prudent: "Now we know better — we didn't then"
4. Inadvertent-reckless: "What layering?"
```

Quantifying tech debt: estimate the cost of the debt payment (hours to fix) vs. the interest rate (hours per sprint caused by the debt).

**Evolutionary Architecture:**
From "Building Evolutionary Architectures" (Ford, Parsons, Kua): design systems that support guided, incremental change across multiple dimensions without needing to predict the future.

Key mechanism: **fitness functions** — automated tests that verify architectural properties:

```python
# Fitness function: no service directly queries another service's database
# Run as part of CI/CD pipeline

def test_no_cross_service_database_access():
    """
    Architectural constraint: each service may only access its own schema.
    Services are prefixed by name in schema names: orders.*, payments.*, users.*
    """
    for service_name, codebase_path in services.items():
        sql_files = find_sql_files(codebase_path)
        for sql_file in sql_files:
            queries = parse_sql_queries(sql_file)
            for query in queries:
                tables = extract_table_names(query)
                for table in tables:
                    schema = table.split(".")[0] if "." in table else "public"
                    assert schema == service_name or schema == "public", (
                        f"{service_name} is querying table {table} "
                        f"which belongs to schema {schema}"
                    )
```

---

## Key Concepts

**Architecture Decision Record (ADR):** A short document capturing a significant architectural decision, its context, the options considered, the chosen option, and the consequences.

**Trade-off analysis:** A structured method for comparing architectural options by explicitly scoring them on relevant dimensions and acknowledging costs.

**Technical debt:** Work deferred for short-term gain that accumulates "interest" (extra effort) on future changes. Not inherently bad — the problem is debt without awareness.

**Evolutionary architecture:** An architecture designed for guided, incremental change rather than permanence. Characterized by fitness functions that automatically verify architectural properties.

**Fitness function:** An automated check that verifies an architectural property is maintained. Analogous to unit tests for code, but for architectural constraints.

**One-way door vs. two-way door:** Amazon's framework for decision reversibility. One-way doors (database engine choice, fundamental API protocol) require more deliberation; two-way doors (feature flags, A/B tests, deployment strategies) can be made and undone quickly.

**Architecture review:** A structured process for getting feedback on a proposed design before implementation, identifying risks and trade-offs the proposer may have missed.

---

## Examples

> Full worked examples to be written. Planned examples:
> 1. Three complete ADRs for decisions from earlier modules (messaging choice, saga style, sharding strategy)
> 2. Trade-off matrix for choosing between sync REST and async events for a given scenario
> 3. Technical debt inventory: identifying, categorizing, and prioritizing debt in a sample codebase
> 4. Fitness function: automated test for "no service calls another service's database directly"

---

## Common Pitfalls

**Pitfall 1: Writing ADRs retrospectively for decisions already made.**
An ADR written after implementation is just documentation of what happened. The value of an ADR is in the *process* of writing it — forcing explicit consideration of alternatives and consequences before implementation.

**Pitfall 2: Treating all decisions as one-way doors.**
Some teams require lengthy ADR processes for decisions that are easily reversible. This creates process overhead without value. Reserve full ADR treatment for high-stakes, hard-to-reverse decisions.

**Pitfall 3: Architecture that prioritizes elegance over evolvability.**
Beautiful architectures that are hard to change are worse than messy architectures that evolve freely. The best architecture for a system that will change is the one that makes change cheap, not the one that is most theoretically pure.

---

## Cross-Links

- [[systems-architecture/modules/01_introduction]] — The trade-off frameworks here apply to the monolith vs. microservices decision
- [[systems-architecture/modules/12_capstone-project]] — The capstone requires writing ADRs for every major design decision
- [[devops-platform-engineering]] — CI/CD pipelines are where fitness functions run
- [[feature-flags-monitoring]] — Feature flags are the quintessential "two-way door" — architectural decisions that can be changed at runtime

---

## Summary

- ADRs (Architecture Decision Records) are short, version-controlled documents capturing significant decisions, alternatives considered, and consequences.
- Every significant architectural decision should have an ADR — written before implementation, not after.
- The trade-off analysis framework: state the problem, generate 3+ alternatives, score on relevant dimensions, acknowledge costs, state the decision.
- Technical debt is inevitable and not always bad. The problem is unacknowledged debt that silently accumulates interest.
- Evolutionary architecture: design for change by defining fitness functions that automatically verify architectural constraints.
- One-way doors (database choice) require more deliberation; two-way doors (feature flags, deployment strategies) can be decided and reversed quickly.
- Good architecture reviews produce actionable feedback and find risks before they become production incidents.
