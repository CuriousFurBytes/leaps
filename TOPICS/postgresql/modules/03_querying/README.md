# Module 03: Querying — SELECT Mastery

[← Module 02](../02_data-types-and-schema/) | [Topic Home](../../README.md) | [Next → Module 04](../04_indexes-and-performance/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
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

SQL's SELECT statement is far more powerful than most developers use in day-to-day work. This module covers the full range of SELECT capabilities in PostgreSQL: all JOIN types (INNER, LEFT, RIGHT, FULL, CROSS, SELF), aggregation with GROUP BY and HAVING, subqueries, window functions, and the LATERAL join. Mastering these transforms you from someone who can write basic queries into someone who can answer complex business questions in a single SQL statement.

Window functions in particular are a paradigm shift. They compute values across rows related to the current row without collapsing those rows (unlike GROUP BY). Once you understand them, you will find yourself reaching for them constantly: running totals, moving averages, rankings, lead/lag comparisons.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/02_data-types-and-schema]] — you need to understand: table relationships (FK), how JOINs work at a high level
- [[modules/01_introduction]] — you need to understand: basic SELECT, WHERE, ORDER BY, GROUP BY fundamentals

---

## Objectives

By the end of this module, you will be able to:

1. Write INNER, LEFT, RIGHT, FULL OUTER, and CROSS JOINs and explain when to use each
2. Use GROUP BY with HAVING to filter aggregated results, and understand how NULL values affect aggregation
3. Write correlated and non-correlated subqueries and recognize when a JOIN is more efficient
4. Use window functions (ROW_NUMBER, RANK, DENSE_RANK, SUM, AVG, LAG, LEAD, FIRST_VALUE) with PARTITION BY and ORDER BY
5. Write LATERAL JOINs for per-row correlated subqueries
6. Understand the SQL query execution order and how it affects WHERE vs HAVING, aliases, and subqueries

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **JOIN Types**
> - INNER JOIN: only rows with matches in both tables
> - LEFT JOIN (LEFT OUTER JOIN): all rows from left table; NULL for unmatched right
> - RIGHT JOIN: all rows from right table; NULL for unmatched left
> - FULL OUTER JOIN: all rows from both; NULL where no match
> - CROSS JOIN: cartesian product
> - SELF JOIN: joining a table to itself (for hierarchies, pairs)
>
> **Aggregation Deep Dive**
> - GROUP BY execution model
> - HAVING vs WHERE: filtering before vs after aggregation
> - GROUPING SETS, ROLLUP, CUBE for multi-dimensional aggregation
> - NULL handling in COUNT(*) vs COUNT(column)
>
> **Subqueries**
> - Non-correlated subqueries in WHERE (IN, NOT IN, EXISTS, ANY, ALL)
> - Correlated subqueries: performance characteristics
> - Scalar subqueries in SELECT clause
>
> **Window Functions**
> - Frame specification (ROWS vs RANGE, UNBOUNDED PRECEDING, etc.)
> - Ranking functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE
> - Aggregate window functions: SUM, AVG, COUNT, MIN, MAX over a window
> - Navigation functions: LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE
>
> **LATERAL Joins**
> - What LATERAL means and when to use it
> - Comparison: LATERAL vs correlated subquery vs window function
> - Common use case: "top N per group" queries

---

## Key Concepts

**Query execution order:** SQL processes clauses in this logical order (not the order they're written): FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT. Understanding this explains why you can't use SELECT aliases in WHERE, and why HAVING can filter on aggregate functions but WHERE cannot.

**Window function:** A function that operates across a set of rows related to the current row without collapsing them into a single output row. The `OVER (PARTITION BY ... ORDER BY ...)` clause defines the "window" of rows the function operates on.

**LATERAL:** A JOIN modifier that allows a subquery in the FROM clause to reference columns from tables to its left. Without LATERAL, FROM subqueries cannot see other tables' columns. LATERAL enables per-row correlated subqueries in the FROM clause.

**Correlated subquery:** A subquery that references columns from the outer query. It is re-evaluated for every row in the outer query — potentially expensive. Window functions often replace correlated subqueries more efficiently.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Customer order summary using LEFT JOIN + GROUP BY
> - Example 2: Top-N-per-group using window functions (ROW_NUMBER + CTE)
> - Example 3: LATERAL JOIN for latest record per group
> - Example 4: Running total and moving average with SUM OVER

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Using NOT IN with a subquery that can return NULL (returns no rows unexpectedly)
> - Confusing WHERE and HAVING (WHERE before aggregation, HAVING after)
> - RANK vs DENSE_RANK vs ROW_NUMBER — subtle differences with ties
> - N+1 query problem: recognizing when a correlated subquery should be a JOIN

---

## Cross-Links

- [[modules/02_data-types-and-schema]] — schema design determines which JOINs are possible
- [[modules/04_indexes-and-performance]] — understanding queries is prerequisite to understanding why indexes help
- [[modules/06_advanced-sql]] — CTEs and recursive queries extend SELECT mastery
- [[django-fastapi-flask]] — ORMs generate SELECT queries; understanding SQL helps debug and optimize ORM code

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - All JOIN types and their use cases
> - Aggregation with GROUP BY, HAVING, GROUPING SETS
> - Subqueries: correlated, non-correlated, scalar
> - Window functions: ranking, aggregate, navigation
> - LATERAL JOINs for per-row subqueries
> - SQL query execution order
