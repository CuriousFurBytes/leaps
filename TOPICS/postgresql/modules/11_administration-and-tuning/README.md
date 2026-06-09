# Module 11: Administration and Tuning

[← Module 10](../10_partitioning-and-extensions/) | [Topic Home](../../README.md) | [Next → Module 12](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-purple)
![Time](https://img.shields.io/badge/time-10--12h-orange)

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

This module covers what you need to know to run PostgreSQL in production responsibly: VACUUM and autovacuum (the maintenance process that prevents table bloat from MVCC), the `pg_stat_*` family of views for real-time monitoring, the critical memory configuration parameters (`shared_buffers`, `work_mem`, `effective_cache_size`), and backup and restore with `pg_dump`, `pg_restore`, and `pg_basebackup`.

Production PostgreSQL administration is as much about monitoring and understanding normal behavior as it is about reacting to problems. This module builds the mental model of a healthy Postgres server and teaches you to recognize when something is wrong.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/05_transactions-and-concurrency]] — you need to understand: MVCC and dead tuples — the root cause of bloat that VACUUM addresses
- [[modules/09_replication-and-ha]] — you need to understand: WAL concepts (relevant to backup and replication configuration)

---

## Objectives

By the end of this module, you will be able to:

1. Explain what VACUUM and autovacuum do, why they are necessary, and how to configure them appropriately for different table sizes and churn rates
2. Diagnose table and index bloat using `pg_stat_user_tables` and `pg_stat_user_indexes`
3. Monitor active queries, lock waits, and replication lag using `pg_stat_activity`, `pg_locks`, and `pg_stat_replication`
4. Configure the three most impactful memory parameters: `shared_buffers`, `work_mem`, and `effective_cache_size`
5. Back up a database with `pg_dump` and `pg_basebackup`, and restore it with `pg_restore`
6. Understand `pg_hba.conf` for access control and `postgresql.conf` for server configuration

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **VACUUM and Autovacuum**
> - Why VACUUM is needed: MVCC dead tuples accumulate; storage grows without bound
> - VACUUM vs VACUUM FULL: reclaiming space vs compacting the table
> - VACUUM ANALYZE: updating planner statistics in the same pass
> - Autovacuum: the background daemon; per-table configuration
> - Key autovacuum parameters: autovacuum_vacuum_scale_factor, autovacuum_vacuum_cost_delay
> - Monitoring autovacuum: pg_stat_user_tables (n_dead_tup, last_autovacuum)
> - Transaction ID wraparound: the critical case where VACUUM must run or the database halts
>
> **Bloat Diagnosis**
> - Table bloat: n_dead_tup / (n_live_tup + n_dead_tup) ratio
> - Index bloat: separate from table bloat; REINDEX CONCURRENTLY to fix
> - pgstattuple extension for precise bloat measurement
> - pg_repack: online table compaction without ACCESS EXCLUSIVE lock
>
> **Monitoring Views**
> - pg_stat_activity: current connections, query text, state, wait events
> - pg_locks: current lock holders and waiters
> - pg_stat_user_tables: per-table statistics (seq scans, index scans, vacuums, analyzes)
> - pg_stat_user_indexes: per-index scan counts (identify unused indexes)
> - pg_stat_replication: replication lag per standby
> - pg_stat_bgwriter: checkpoint activity and shared buffer statistics
>
> **Memory Configuration**
> - shared_buffers: PostgreSQL's buffer pool (typically 25% of RAM)
> - work_mem: memory per sort/hash operation (multiply by max_connections × queries in flight)
> - effective_cache_size: hint to the planner about OS page cache size (does NOT allocate memory)
> - maintenance_work_mem: for VACUUM, CREATE INDEX, pg_dump
> - max_connections vs PgBouncer: why connection poolers are essential at scale
>
> **Backup and Restore**
> - pg_dump: logical backup of a single database; portable; can restore to different Postgres version
> - pg_dumpall: logical backup of all databases plus roles
> - pg_dump formats: plain SQL (-f plain), custom (-Fc), directory (-Fd), tar (-Ft)
> - pg_restore: restore from custom/directory/tar format; selective table restore
> - pg_basebackup: physical backup of the entire cluster; used for standby setup
> - PITR (Point-In-Time Recovery): base backup + WAL archiving
> - Backup testing: a backup you haven't restored is an unverified backup
>
> **Configuration Files**
> - postgresql.conf: server configuration (memory, connections, WAL, logging)
> - pg_hba.conf: host-based access control (who can connect from where, with what authentication)
> - pg_ident.conf: OS username to Postgres username mapping

---

## Key Concepts

**VACUUM:** The PostgreSQL maintenance process that reclaims storage occupied by dead tuples — rows that were deleted or overwritten by UPDATE and are no longer visible to any active transaction. Without VACUUM, tables grow without bound. See [[shared/glossary#VACUUM]].

**Autovacuum:** A background process that runs VACUUM automatically on tables that have accumulated enough dead tuples (based on configurable thresholds). In most configurations, autovacuum runs continuously and requires no manual intervention — but it must be monitored and tuned for tables with high churn rates.

**shared_buffers:** The primary memory configuration parameter. It controls how much memory PostgreSQL uses for its buffer cache (caching data pages to avoid disk reads). The standard starting point is 25% of total RAM.

**work_mem:** The memory allocated per sort or hash operation. Increasing it speeds up complex queries (sorts, hash joins) but is multiplied by all concurrent sort operations — a dangerous parameter to increase globally on a busy server.

**pg_dump:** A utility for creating a logical backup of a PostgreSQL database. The output can be a plain SQL file or a compressed binary format. pg_dump does not require taking the database offline and produces a consistent snapshot.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Diagnosing table bloat with pg_stat_user_tables and deciding whether to VACUUM or VACUUM FULL
> - Example 2: Identifying slow queries with pg_stat_activity and EXPLAIN ANALYZE
> - Example 3: A worked memory configuration for a server with 16 GB RAM
> - Example 4: Backup and restore workflow with pg_dump and pg_restore

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Setting work_mem too high globally (memory exhaustion under concurrent load)
> - Not testing backups (discovering a backup is corrupt only when you need it)
> - Disabling autovacuum on high-churn tables (they must be vacuumed more, not less)
> - Transaction ID wraparound: the one thing that will stop your database cold if ignored

---

## Cross-Links

- [[modules/05_transactions-and-concurrency]] — MVCC dead tuples are the root cause of bloat; VACUUM is the solution
- [[modules/09_replication-and-ha]] — pg_basebackup is both the backup tool and the standby setup tool; WAL archiving enables PITR
- [[modules/04_indexes-and-performance]] — index bloat is a separate problem from table bloat; REINDEX CONCURRENTLY is the solution
- [[systems-architecture]] — memory tuning and backup strategy are core infrastructure decisions

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - VACUUM and autovacuum: dead tuple reclamation, configuration, transaction ID wraparound
> - Bloat diagnosis: pg_stat_user_tables, index bloat, pg_repack
> - Monitoring: pg_stat_activity, pg_locks, pg_stat_user_tables/indexes, pg_stat_replication
> - Memory: shared_buffers (25% RAM), work_mem (per sort, be careful), effective_cache_size
> - Backup: pg_dump (logical, portable), pg_basebackup (physical, for standbys and PITR)
> - Configuration: postgresql.conf, pg_hba.conf
