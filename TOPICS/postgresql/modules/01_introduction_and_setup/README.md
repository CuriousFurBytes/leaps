# Module 01: Introduction and Setup

> Install PostgreSQL, connect with psql, and understand databases, clusters, roles, and first queries.

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

Install PostgreSQL, connect with psql, and understand databases, clusters, roles, and first queries. This module is intentionally practical: every idea is tied to SQL you can run in `psql` or in any PostgreSQL client.

PostgreSQL rewards careful thinking. The database will remember decisions longer than most application code, so each module trains you to choose names, types, constraints, queries, and operational habits that still make sense after the first prototype becomes a real system.

## Prerequisites

- No PostgreSQL experience required. Basic terminal usage helps.
- Basic comfort reading plain-text error messages and changing a command after PostgreSQL explains what failed.

## Objectives

By the end of this module, you will be able to:

- Explain the purpose of the module's core PostgreSQL concepts in your own words.
- Run small SQL examples and predict their results.
- Debug common mistakes by reading PostgreSQL errors carefully.
- Connect this module to later concerns such as performance, safety, and operations.

## Theory

### The central idea

PostgreSQL is a relational database: it stores data as named relations, usually tables, and lets you ask questions about that data with SQL. A relation is not just a spreadsheet. It is a contract about the shape of facts: which columns exist, what types they hold, which values are required, and which relationships must remain valid. This contract is valuable because application code changes often, but persisted data can outlive frameworks, services, and teams.

PostgreSQL descends from the POSTGRES research project at UC Berkeley and later adopted SQL compatibility. Its design favors correctness, extensibility, and standards-aware relational behavior.

```sql
-- Example 1: create or inspect a durable database object for this module.
CREATE DATABASE learning_pg;
```

### The working loop

The professional PostgreSQL loop is small and repeatable: state the fact you want to represent, write the SQL, run it, inspect the result, and adjust the design when the database exposes an ambiguity. Beginners often try to memorize syntax first. Memorization helps, but judgment comes from seeing how SQL statements change stored state and how PostgreSQL enforces or rejects those changes.

```sql
-- Example 2: run a query or data-changing statement, then inspect what happened.
SELECT version();
```

### Why correctness belongs in the database

A database is shared infrastructure. Many clients may write to it: web servers, migration scripts, batch jobs, admin tools, or future services that do not exist yet. If an invariant matters, keeping it only in application code creates multiple chances to forget it. PostgreSQL features such as transactions, constraints, indexes, and roles let you move critical rules closer to the data.

```sql
-- Example 3: make a change deliberately and keep it explicit.
CREATE TABLE notes (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, body text NOT NULL);
```

## Key Concepts

- **Relation:** A named set of rows with columns. In day-to-day PostgreSQL work, a table is the most common relation.
- **SQL statement:** A complete command such as `SELECT`, `INSERT`, or `CREATE TABLE` sent to PostgreSQL for parsing, planning, and execution.
- **Transaction:** A unit of work that succeeds or fails as a whole. Transactions become central when multiple statements must preserve one business fact.
- **Constraint:** A database rule that rejects invalid data. Constraints are executable documentation for important assumptions.
- **Query plan:** PostgreSQL's chosen strategy for answering a query. Plans become visible later with `EXPLAIN` and are essential for performance work.

## Examples

### Scenario: verify your current database

Run this query when you need to confirm which database and user your session is using.

```sql
-- Show session identity before changing data.
SELECT current_database() AS database_name, current_user AS role_name;
```

The result prevents a common operational mistake: running a correct command in the wrong environment.

### Scenario: make a tiny learning table

```sql
-- A small table keeps experiments isolated and easy to delete later.
CREATE TABLE IF NOT EXISTS module_scratch (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    label text NOT NULL
);
```

This creates a safe place to practice without touching application tables.

## Common Pitfalls

### Pitfall 1: changing every row by accident

Wrong:

```sql
-- Missing WHERE updates every row.
UPDATE module_scratch SET label = 'changed';
```

Correct:

```sql
-- The WHERE clause limits the change to the intended row.
UPDATE module_scratch SET label = 'changed' WHERE id = 1;
```

### Pitfall 2: assuming text dates behave like dates

Wrong:

```sql
-- Text sorts lexicographically, not by date semantics in all formats.
CREATE TABLE bad_events (happened_on text);
```

Correct:

```sql
-- Use a date/time type when the value represents time.
CREATE TABLE good_events (happened_on date NOT NULL);
```

### Pitfall 3: ignoring errors instead of reading them

Wrong:

```sql
-- Re-running blindly hides the actual cause.
INSERT INTO module_scratch (id, label) VALUES (1, NULL);
```

Correct:

```sql
-- Satisfy the NOT NULL rule and let the identity column generate the id.
INSERT INTO module_scratch (label) VALUES ('valid row');
```

## Cross-Links

- [[postgresql]] — the topic roadmap and quick reference.
- [[go]] — an application language commonly connected to PostgreSQL.
- [[javascript-typescript-react]] — a web stack often backed by PostgreSQL APIs.
- [[shared/concepts/concurrency]] — shared terminology for multi-client and transactional behavior.

## Summary

- PostgreSQL stores long-lived facts and enforces rules near the data.
- SQL statements are both a query language and a schema/data change language.
- Constraints, transactions, and types are correctness tools, not ceremony.
- Reading PostgreSQL errors is part of the learning loop.
- Safe database work requires explicit scope, especially for data-changing statements.
