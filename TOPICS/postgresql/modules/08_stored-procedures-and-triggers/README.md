# Module 08: Stored Procedures and Triggers

[← Module 07](../07_json-and-full-text-search/) | [Topic Home](../../README.md) | [Next → Module 09](../09_replication-and-ha/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-red)
![Time](https://img.shields.io/badge/time-7--9h-orange)

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

PostgreSQL includes a full procedural programming language — PL/pgSQL — that runs inside the database server. This module covers writing functions, stored procedures, and triggers in PL/pgSQL. Server-side logic is useful for complex business rules that must be atomically enforced, audit logging, computed columns that would be expensive to calculate in application code, and data transformations.

Triggers in particular are a powerful and frequently misused feature. A trigger that auto-updates an `updated_at` timestamp is benign; a trigger that sends emails or calls external APIs is a recipe for operational pain. This module teaches you to use triggers effectively and know their limits.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/05_transactions-and-concurrency]] — you need to understand: transaction semantics (triggers run inside the calling transaction)
- [[modules/03_querying]] — you need to understand: complex SQL (used inside function bodies)

---

## Objectives

By the end of this module, you will be able to:

1. Write PL/pgSQL functions that accept parameters, perform SQL operations, use conditional logic, and return values
2. Create stored procedures (as distinct from functions in PostgreSQL 11+)
3. Write BEFORE and AFTER triggers on INSERT, UPDATE, and DELETE
4. Implement common trigger patterns: auto-updating timestamps, audit logging, enforcing complex constraints
5. Create generated columns (STORED) as an alternative to update triggers for computed values
6. Understand PL/pgSQL error handling with EXCEPTION blocks

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **PL/pgSQL Basics**
> - CREATE FUNCTION syntax: parameters, return types, language
> - Variable declarations and DECLARE block
> - Control flow: IF/ELSIF/ELSE, CASE, loops (LOOP, FOR, WHILE, FOREACH)
> - RETURN and RETURN NEXT / RETURN QUERY (for set-returning functions)
> - Dollar quoting: $$ ... $$ (avoids escaping inner quotes)
>
> **Functions vs Stored Procedures**
> - Functions: return a value; can be used in SQL expressions; run in caller's transaction
> - Stored procedures (PostgreSQL 11+): no return value; can COMMIT/ROLLBACK inside; called with CALL
> - When to use each
>
> **Triggers**
> - CREATE TRIGGER syntax: BEFORE/AFTER/INSTEAD OF; INSERT/UPDATE/DELETE/TRUNCATE; ROW/STATEMENT
> - The trigger function: returns TRIGGER; uses NEW and OLD pseudo-records
> - BEFORE ROW trigger: can modify NEW before the operation; can cancel the operation by returning NULL
> - AFTER ROW trigger: cannot modify the row; typically used for side effects (audit log, notifications)
> - STATEMENT-level triggers: once per statement, not once per row
> - Transition tables (NEW TABLE / OLD TABLE) for statement-level triggers
>
> **Common Trigger Patterns**
> - Auto-updating updated_at timestamp
> - Audit log table: recording who changed what and when
> - Soft delete: setting a deleted_at column instead of actually deleting
> - Enforcing cross-table constraints that CHECK cannot handle
>
> **Generated Columns**
> - GENERATED ALWAYS AS expr STORED: computed at write time, stored on disk
> - Cannot be written to directly
> - Can be indexed
> - Alternative to triggers for computed columns
>
> **Error Handling**
> - BEGIN ... EXCEPTION ... END block
> - SQLSTATE codes and named exception conditions
> - RAISE NOTICE, RAISE WARNING, RAISE EXCEPTION for debugging and custom errors

---

## Key Concepts

**PL/pgSQL:** PostgreSQL's built-in procedural language, a superset of SQL with variable declarations, control flow, and exception handling. Functions written in PL/pgSQL run entirely inside the database server process.

**Trigger function:** A special PL/pgSQL function that returns `TRIGGER`. It has access to `NEW` (the new row for INSERT/UPDATE) and `OLD` (the old row for UPDATE/DELETE). A BEFORE trigger can modify `NEW` or abort the operation by returning NULL.

**Generated column:** A column whose value is automatically computed from other columns at write time. In PostgreSQL, STORED generated columns are persisted on disk and can be indexed. They eliminate the need for update triggers for simple computed values.

**Dollar quoting:** The `$$ ... $$` syntax used to delimit PL/pgSQL function bodies, avoiding the need to escape single quotes inside the function code. You can use any `$tag$ ... $tag$` delimiter.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: A PL/pgSQL function to validate and process an order with error handling
> - Example 2: A BEFORE UPDATE trigger to auto-set updated_at
> - Example 3: An AFTER INSERT trigger for an audit log table
> - Example 4: Generated column for a full-name field computed from first_name and last_name

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Triggers that do too much: sending emails, calling HTTP APIs — these belong in application code
> - Forgetting that BEFORE triggers can veto operations by returning NULL
> - Using AFTER triggers when BEFORE would be more efficient (AFTER fires even if an error will occur)
> - Generated columns cannot reference mutable functions (like now()) — use triggers for truly dynamic computed values

---

## Cross-Links

- [[modules/05_transactions-and-concurrency]] — triggers run inside the calling transaction; a trigger failure rolls back the whole transaction
- [[modules/06_advanced-sql]] — data-modifying CTEs can sometimes replace trigger-based cascades
- [[modules/11_administration-and-tuning]] — trigger-heavy schemas require careful VACUUM tuning (more dead tuples per row change)

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - PL/pgSQL: variable declarations, control flow, loops, RETURN
> - Functions vs stored procedures: return values, transaction control
> - Triggers: BEFORE/AFTER, ROW/STATEMENT, NEW/OLD pseudo-records
> - Common patterns: updated_at, audit logs, constraint enforcement
> - Generated columns as trigger alternatives for computed values
> - Error handling with EXCEPTION blocks
