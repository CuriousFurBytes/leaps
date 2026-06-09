# Module 02: Data Types and Schema Design

[← Module 01](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03](../03_querying/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-green)
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

This module covers PostgreSQL's complete type system and the principles of relational schema design. Good schema design is the foundation of every performant, maintainable database. Choosing the wrong data type — using `TEXT` where `INTEGER` belongs, or storing money as `FLOAT` instead of `NUMERIC` — creates bugs that are expensive to fix later. This module teaches you to make the right choices from the start.

You will also learn database normalization: the formal process of organizing a schema to eliminate redundancy and enforce data integrity through the structure of the tables themselves rather than application code. Normalization to at least Third Normal Form (3NF) is standard practice for OLTP (transaction-processing) databases.

> [!NOTE]
> This module stub will be expanded into a full module in a future update. The objectives,
> key concepts, and cross-links below give you a roadmap for the content that will be covered.

---

## Prerequisites

- [[modules/01_introduction]] — you need to understand: CREATE TABLE syntax, basic data types (TEXT, INTEGER, BOOLEAN, TIMESTAMPTZ), PRIMARY KEY

---

## Objectives

By the end of this module, you will be able to:

1. Select the appropriate PostgreSQL data type for any common use case: numeric, text, boolean, date/time, UUID, arrays, and enums
2. Apply table constraints: NOT NULL, UNIQUE, CHECK, PRIMARY KEY, and FOREIGN KEY — and understand when each is appropriate
3. Explain the problem that database normalization solves and apply 1NF, 2NF, and 3NF rules to a schema
4. Design a normalized schema from a natural-language description of business requirements
5. Understand denormalization trade-offs: when and why to deliberately break normal forms for performance

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **PostgreSQL Type System**
> - Numeric types: SMALLINT, INTEGER, BIGINT, NUMERIC(p,s), REAL, DOUBLE PRECISION — when to use each
> - Text types: TEXT vs VARCHAR(n) vs CHAR(n) — and why TEXT wins almost always
> - Date/time: DATE, TIME, TIMESTAMP, TIMESTAMPTZ, INTERVAL — time zones and storage
> - Boolean: TRUE/FALSE/NULL trivalue logic
> - UUID: when to use UUID vs BIGSERIAL as a primary key
> - Arrays: PostgreSQL's native array type — when it helps and when it hurts
> - Enums: CREATE TYPE ... AS ENUM — advantages and limitations
> - Special types: JSONB (preview of Module 07), INET/CIDR (network addresses), MONEY (why to avoid it)
>
> **Constraints**
> - NOT NULL: enforcement and implications for outer joins
> - UNIQUE: single and multi-column unique constraints
> - CHECK: inline and table-level CHECK constraints
> - PRIMARY KEY: choosing natural vs. surrogate keys
> - FOREIGN KEY: ON DELETE CASCADE, RESTRICT, SET NULL, SET DEFAULT; deferrable constraints
>
> **Normalization**
> - The problem: update anomalies, insertion anomalies, deletion anomalies
> - 1NF: atomic values, no repeating groups
> - 2NF: eliminate partial dependencies (relevant when PK is composite)
> - 3NF: eliminate transitive dependencies
> - BCNF: Boyce-Codd Normal Form — the stricter version of 3NF
> - When to denormalize: read-heavy workloads, derived columns, price snapshots

---

## Key Concepts

**Surrogate key vs. natural key:** A surrogate key (like BIGSERIAL id) is an artificial identifier with no business meaning. A natural key uses a real-world attribute (like email or ISBN). Surrogate keys are simpler to index and never need to be updated; natural keys embed meaning but change when the real-world value changes.

**Referential integrity:** The guarantee that a foreign key value always corresponds to an existing row in the referenced table. PostgreSQL enforces this automatically when you define a FOREIGN KEY constraint.

**Normal forms:** A hierarchy of rules (1NF, 2NF, 3NF, BCNF) that progressively eliminate redundancy from relational schemas. Each normal form includes all requirements of the lower forms plus an additional rule.

**Atomic value (1NF):** In First Normal Form, each column must contain a single, indivisible value — not a comma-separated list or a repeating group. PostgreSQL arrays technically violate strict 1NF; use them carefully.

**NUMERIC vs FLOAT for money:** `NUMERIC(precision, scale)` stores exact decimal values with no floating-point approximation. `FLOAT` and `REAL` are approximate — a price stored as `FLOAT` might be `9.9999999` instead of `10.00`. Never use floating-point types for monetary values.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Designing a schema for an invoicing system (entities: customers, invoices, line items, products)
> - Example 2: Applying normalization — taking a denormalized spreadsheet and decomposing it to 3NF
> - Example 3: Using UUID primary keys — when and why

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Using FLOAT for monetary values (causes rounding errors)
> - Storing multiple values in one column (violates 1NF, breaks queries)
> - Not using foreign keys (loses referential integrity enforcement)
> - Over-normalizing: normalizing beyond 3NF in OLTP when the extra joins hurt more than they help

---

## Cross-Links

- [[modules/01_introduction]] — data types and constraints introduced at a basic level in Module 01
- [[modules/03_querying]] — schema design directly affects join performance; well-normalized schemas simplify queries
- [[modules/05_transactions-and-concurrency]] — constraints and foreign keys interact with transaction behavior (deferrable constraints)
- [[django-fastapi-flask]] — Django models and SQLAlchemy Column definitions map directly to the type and constraint choices covered here

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - PostgreSQL's numeric, text, date/time, boolean, UUID, array, and enum types
> - Table constraints: NOT NULL, UNIQUE, CHECK, PRIMARY KEY, FOREIGN KEY
> - Normalization: 1NF through 3NF/BCNF
> - When to denormalize and how to document the decision
