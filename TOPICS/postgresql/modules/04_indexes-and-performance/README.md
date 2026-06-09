# Module 04: Indexes and Performance

[← Module 03](../03_querying/) | [Topic Home](../../README.md) | [Next → Module 05](../05_transactions-and-concurrency/)

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

A query that takes 30 seconds can often be reduced to 30 milliseconds with the right index. This module teaches you how indexes work at a structural level — why a B-tree index makes an equality lookup go from O(n) to O(log n), what GIN indexes store internally and why they are needed for arrays and JSONB, and when BRIN outperforms B-tree for large append-only tables. More importantly, you will learn to read `EXPLAIN ANALYZE` output fluently — the single most valuable skill for diagnosing slow queries.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/03_querying]] — you need to understand: SELECT queries well enough to write non-trivial queries that need optimizing
- [[modules/02_data-types-and-schema]] — you need to understand: table structure and data types (index types depend on the column type)

---

## Objectives

By the end of this module, you will be able to:

1. Explain how B-tree, Hash, GIN, GiST, SP-GiST, and BRIN indexes work structurally and identify which to use for a given query pattern
2. Create single-column, multi-column, partial, and expression indexes
3. Read `EXPLAIN ANALYZE` output: identify seq scans vs. index scans, understand cost estimates, find the expensive nodes
4. Diagnose unused indexes and understand why the planner might ignore an index you created
5. Create indexes concurrently to avoid locking writes in production

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **Index Internals**
> - B-tree: balanced tree structure, O(log n) lookup, range scan support
> - Hash: O(1) equality lookup, no range support, not WAL-logged in older versions
> - GIN (Generalized Inverted Index): maps values to row sets; used for arrays, JSONB, full-text search
> - GiST (Generalized Search Tree): geometric types, ranges, nearest-neighbor search
> - SP-GiST (Space-Partitioned GiST): recursive partitioning; IP addresses, phone numbers
> - BRIN (Block Range Index): stores min/max per block range; tiny size; best for naturally ordered large tables
>
> **Index Strategy**
> - Index selectivity: high-cardinality columns benefit more from indexing
> - Multi-column indexes: column order matters; leftmost prefix rule
> - Partial indexes: index only the rows that matter (e.g., WHERE status = 'pending')
> - Expression indexes: index the result of a function (e.g., LOWER(email))
> - Covering indexes (INCLUDE): add non-key columns to avoid table lookups
>
> **EXPLAIN ANALYZE**
> - Reading the plan tree: each node type and what it means
> - Cost units: what "cost=0.00..45.00" means
> - Actual vs estimated rows: when the planner is wrong and how to fix it
> - Buffers analysis: hits vs reads; identifying I/O bottlenecks
> - Hash Join vs Nested Loop vs Merge Join: when each appears
>
> **Index Maintenance**
> - Index bloat: dead index entries and VACUUM
> - REINDEX CONCURRENTLY
> - pg_stat_user_indexes: monitoring index usage
> - Unused index detection

---

## Key Concepts

**Sequential scan (seq scan):** Reading every row in the table from start to finish. O(n) time. The planner chooses seq scan when fetching a large percentage of rows (often faster than random I/O from index) or when no suitable index exists.

**Index scan:** Using an index to find specific rows, then fetching only those rows from the heap. O(log n) for B-tree. The planner chooses this for high-selectivity predicates (few matching rows).

**Bitmap scan:** An intermediate strategy: scan the index to collect page locations of matching rows, sort them, then fetch pages in order. Reduces random I/O. Used when a moderate number of rows match.

**Cost estimate:** EXPLAIN shows `cost=startup..total`. Startup cost is the time before the first row is returned. Total cost is the time to return all rows. The planner minimizes total cost.

**Index selectivity:** The fraction of rows matching a predicate. An index on a boolean column (50/50 true/false) has low selectivity — the planner may ignore it. An index on a UUID column has very high selectivity.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Creating a B-tree index and reading the EXPLAIN ANALYZE before/after
> - Example 2: Partial index for a "pending jobs" queue pattern
> - Example 3: GIN index for JSONB attribute search
> - Example 4: BRIN index on a time-series log table

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Creating an index and wondering why the planner doesn't use it (selectivity / statistics freshness)
> - Multi-column index column order — index on (a, b) does NOT help queries on just (b)
> - Forgetting CONCURRENTLY — CREATE INDEX locks writes in production
> - Over-indexing: every index slows down writes; index only what queries actually need

---

## Cross-Links

- [[modules/03_querying]] — you need working queries to optimize
- [[modules/05_transactions-and-concurrency]] — indexes interact with MVCC; dead tuple visibility affects index scans
- [[modules/11_administration-and-tuning]] — VACUUM, bloat, and statistics maintenance for index health
- [[systems-architecture]] — index strategy is a key database architecture decision

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - B-tree, Hash, GIN, GiST, SP-GiST, BRIN — structures and use cases
> - Single, multi-column, partial, expression, and covering indexes
> - EXPLAIN ANALYZE: reading plans, cost estimates, actual vs estimated rows
> - Index strategy: selectivity, column order, partial indexes
> - Production index creation with CONCURRENTLY
