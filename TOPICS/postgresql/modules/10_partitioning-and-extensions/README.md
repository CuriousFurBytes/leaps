# Module 10: Partitioning and Extensions

[← Module 09](../09_replication-and-ha/) | [Topic Home](../../README.md) | [Next → Module 11](../11_administration-and-tuning/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-purple)
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

When a single table grows to hundreds of millions of rows, certain operations — range scans, deletes, vacuuming — become slow regardless of indexing. Table partitioning solves this by dividing a logical table into physical sub-tables (partitions), allowing the query planner to skip entire partitions irrelevant to a query and enabling fast partition-level operations like detaching and dropping old partitions.

PostgreSQL's extension ecosystem is equally important. The `pg_trgm` extension enables fuzzy string matching and similarity search. PostGIS turns PostgreSQL into a full geospatial database. TimescaleDB delivers time-series performance on top of standard Postgres. This module surveys the most important extensions and teaches you to evaluate and use them.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/04_indexes-and-performance]] — you need to understand: EXPLAIN ANALYZE (essential for verifying partition pruning)
- [[modules/02_data-types-and-schema]] — you need to understand: table structure and constraints (partitioned tables have special constraint behaviors)

---

## Objectives

By the end of this module, you will be able to:

1. Create RANGE, LIST, and HASH partitioned tables and choose the right strategy for a given use case
2. Manage partitions: create new partitions, attach/detach, and drop old ones efficiently
3. Verify partition pruning in EXPLAIN ANALYZE output
4. Enable and use pg_trgm for similarity search and fuzzy matching
5. Understand PostGIS's capabilities at a conceptual level and know when to use it
6. Understand TimescaleDB's hypertable architecture as an extension of PostgreSQL partitioning

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **Declarative Table Partitioning (PostgreSQL 10+)**
> - PARTITION BY RANGE: most common; dates, timestamps, integer ranges
> - PARTITION BY LIST: categorical data (country, status, tenant_id)
> - PARTITION BY HASH: even distribution across N partitions by hash of key
> - Sub-partitioning: range-within-hash, list-within-range
>
> **Partition Management**
> - Creating child partitions: CREATE TABLE child PARTITION OF parent FOR VALUES ...
> - Attaching an existing table as a partition: ATTACH PARTITION
> - Detaching a partition (fast, no data movement): DETACH PARTITION
> - Dropping a partition (immediate, no DELETE overhead)
>
> **Partition Pruning**
> - Enable_partition_pruning (default on)
> - Query-time pruning: WHERE clause must reference the partition key
> - EXPLAIN output: "Partitions removed during planning: X"
> - Index creation on partitioned tables: indexes created on parent propagate to children
>
> **Performance Trade-offs**
> - When partitioning helps: range scans, partition-level VACUUM, bulk deletes
> - When partitioning hurts: cross-partition joins, small tables, queries without partition key
>
> **pg_trgm Extension**
> - Trigrams: every string decomposed into overlapping 3-character sequences
> - similarity() function: Jaccard similarity between two strings
> - GIN and GiST indexes on trigrams
> - Use case: typo-tolerant search, fuzzy name matching, LIKE '%substr%' acceleration
>
> **PostGIS Overview**
> - Adds geometry, geography types to PostgreSQL
> - Spatial indexes (GiST)
> - Spatial SQL functions: ST_Distance, ST_Within, ST_Intersects, ST_Transform
> - Use cases: mapping, location-based queries, geofencing
>
> **TimescaleDB Overview**
> - Hypertables: automatically partitioned time-series tables
> - Continuous aggregates: materialized views that auto-refresh
> - Compression: columnar compression for old time-series data
> - Retention policies: automatic partition expiry

---

## Key Concepts

**Partition pruning:** The query planner's ability to skip scanning partitions that cannot contain rows matching the WHERE clause. For example, a query with `WHERE created_at > '2024-01-01'` on a monthly-partitioned table will scan only the relevant month partitions. Verified with EXPLAIN ANALYZE.

**Partition key:** The column (or expression) used to determine which partition a row belongs to. The partition key must be included in WHERE clauses for partition pruning to occur.

**RANGE partitioning:** Divides rows into partitions based on a range of values (e.g., rows where `created_at >= '2024-01-01' AND created_at < '2024-02-01'`). Most natural for time-series and event log data.

**LIST partitioning:** Divides rows based on an explicit list of values (e.g., `country IN ('US', 'CA')` in one partition, `country IN ('GB', 'DE')` in another). Natural for categorical data.

**HASH partitioning:** Divides rows by hashing the key across N partitions. Ensures even distribution when there is no natural range or list grouping.

**Trigram:** A sequence of 3 consecutive characters. PostgreSQL's pg_trgm extension indexes every trigram in a string, enabling similarity matching and accelerating `LIKE '%pattern%'` queries.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Monthly RANGE partitioned events table with partition creation and pruning verification
> - Example 2: LIST partitioned multi-tenant table (one partition per tenant region)
> - Example 3: pg_trgm similarity search on product names
> - Example 4: Dropping a month's worth of log data in milliseconds by detaching a partition

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Partitioning small tables (adds overhead with no benefit; usually harmful under ~10M rows)
> - Queries without the partition key in WHERE (no partition pruning; scans all partitions)
> - Forgetting to create indexes on each partition (indexes on parent propagate automatically in PostgreSQL 11+)
> - TimescaleDB changing autovacuum behavior — understand how hypertables interact with regular VACUUM

---

## Cross-Links

- [[modules/04_indexes-and-performance]] — partition pruning verification uses EXPLAIN ANALYZE
- [[modules/11_administration-and-tuning]] — partitioning affects VACUUM strategy; AUTOVACUUM configuration differs per partition
- [[modules/07_json-and-full-text-search]] — pg_trgm complements full-text search for fuzzy matching
- [[systems-architecture]] — partitioning strategy is a fundamental data architecture decision

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - Declarative partitioning: RANGE, LIST, HASH
> - Partition management: create, attach, detach, drop
> - Partition pruning: how it works and how to verify it
> - pg_trgm: trigram similarity, fuzzy matching, GIN/GiST indexes
> - PostGIS: geospatial types and queries at a conceptual level
> - TimescaleDB: hypertable architecture as a Postgres extension
