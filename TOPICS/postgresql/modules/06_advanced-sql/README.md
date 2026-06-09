# Module 06: Advanced SQL

[← Module 05](../05_transactions-and-concurrency/) | [Topic Home](../../README.md) | [Next → Module 07](../07_json-and-full-text-search/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-red)
![Time](https://img.shields.io/badge/time-8--10h-orange)

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

This module covers SQL patterns that distinguish intermediate users from advanced practitioners: Common Table Expressions (CTEs) for readable multi-step queries, recursive CTEs for hierarchical and graph traversal, UPSERT for idempotent writes, and the `RETURNING` clause for efficient read-after-write patterns. These are the SQL patterns you will reach for constantly in production applications.

CTEs deserve special attention. They transform deeply nested, unreadable SQL into a sequence of named, understandable steps. Recursive CTEs unlock hierarchical data structures — organization charts, category trees, file systems, graph traversal — that would be impossible to express without recursion or multiple round-trips.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/03_querying]] — you need to understand: SELECT mastery including subqueries
- [[modules/05_transactions-and-concurrency]] — you need to understand: transaction semantics (relevant to UPSERT atomicity)

---

## Objectives

By the end of this module, you will be able to:

1. Write CTEs (WITH clauses) to decompose complex queries into readable, named steps
2. Write recursive CTEs to traverse hierarchical data structures (trees, graphs)
3. Use `INSERT ON CONFLICT DO UPDATE` (UPSERT) for idempotent insert-or-update operations
4. Use `RETURNING` in INSERT, UPDATE, and DELETE to retrieve affected row data efficiently
5. Understand when CTEs are optimization fences and how to work around them
6. Apply DISTINCT ON for "first row per group" patterns

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **Common Table Expressions (CTEs)**
> - WITH clause syntax and multiple CTEs
> - CTEs as optimization fences (pre-PostgreSQL 12 behavior)
> - MATERIALIZED vs NOT MATERIALIZED hints (PostgreSQL 12+)
> - Chaining CTEs: using one CTE's output as input to the next
> - CTEs in UPDATE and DELETE statements
>
> **Recursive CTEs**
> - Anatomy of a recursive CTE: anchor member + recursive member + UNION ALL
> - Traversing a parent-child hierarchy (org charts, categories)
> - Avoiding infinite loops: CYCLE detection (PostgreSQL 14+), LIMIT safety
> - Graph traversal: finding all paths between nodes
> - Generating sequences with recursive CTEs
>
> **UPSERT (INSERT ON CONFLICT)**
> - ON CONFLICT DO NOTHING: skip duplicate inserts silently
> - ON CONFLICT DO UPDATE: atomic check-and-set on conflict
> - The EXCLUDED pseudo-table: accessing the rejected row's values
> - Partial unique indexes as ON CONFLICT targets
> - When NOT to use UPSERT: race conditions in multi-step operations
>
> **RETURNING**
> - RETURNING with INSERT: getting auto-generated IDs
> - RETURNING with UPDATE: confirming new values
> - RETURNING with DELETE: getting deleted row data
> - Using RETURNING in CTEs (data-modifying CTEs)
>
> **Other Advanced Patterns**
> - DISTINCT ON: "first row per group" without window functions
> - VALUES as a table source
> - FILTER clause on aggregate functions: conditional aggregation

---

## Key Concepts

**CTE (Common Table Expression):** A named temporary result set defined in a WITH clause. CTEs make complex queries readable by giving names to intermediate results. In PostgreSQL 12+, simple CTEs are inlined by the planner (not optimization fences) by default.

**Recursive CTE:** A CTE that references itself. It works by starting with an anchor query (base case), then repeatedly applying the recursive member to the prior iteration's results until no new rows are produced. The results of all iterations are combined with UNION ALL.

**UPSERT:** An atomic "insert or update" operation. PostgreSQL implements it with `INSERT ... ON CONFLICT DO UPDATE`. The atomicity means no race condition is possible between the check (does the row exist?) and the action (insert or update).

**EXCLUDED:** In an ON CONFLICT DO UPDATE clause, `EXCLUDED` is a pseudo-table representing the row that was attempted to be inserted but conflicted. You can reference its columns in the SET clause.

**DISTINCT ON:** PostgreSQL-specific syntax for retrieving the first row per group, ordered by a specified expression. More readable than an equivalent window function for simple cases.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Multi-step CTE for calculating cohort retention
> - Example 2: Recursive CTE traversing an employee org chart
> - Example 3: UPSERT for a "view counter" that increments on conflict
> - Example 4: Data-modifying CTE — UPDATE with RETURNING fed into another INSERT

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - CTE as optimization fence: in older Postgres, CTEs were always materialized; this could prevent index use
> - Recursive CTE infinite loop: forgetting the termination condition
> - UPSERT with partial unique index: the ON CONFLICT target must exactly match the constraint definition
> - Using DISTINCT ON without ORDER BY (the result is unpredictable without ordering)

---

## Cross-Links

- [[modules/03_querying]] — CTEs and recursive CTEs are extensions of SELECT mastery
- [[modules/05_transactions-and-concurrency]] — UPSERT atomicity relates to transaction isolation
- [[modules/08_stored-procedures-and-triggers]] — data-modifying CTEs can replace some trigger use cases
- [[django-fastapi-flask]] — ORMs often lack first-class CTE/UPSERT support; raw SQL or query builders needed

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - CTEs: WITH clause, chaining, materialization behavior
> - Recursive CTEs: anchor + recursive member, hierarchy traversal, cycle detection
> - UPSERT: INSERT ON CONFLICT DO NOTHING / DO UPDATE; EXCLUDED pseudo-table
> - RETURNING: in INSERT, UPDATE, DELETE, and data-modifying CTEs
> - DISTINCT ON: first-row-per-group pattern
