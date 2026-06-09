# Module 05: Transactions and Concurrency

[← Module 04](../04_indexes-and-performance/) | [Topic Home](../../README.md) | [Next → Module 06](../06_advanced-sql/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
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

Concurrency is where databases get hard. What happens when two users try to update the same bank account balance simultaneously? What does "isolation" really mean, and what anomalies can occur when transactions are not fully isolated? This module covers PostgreSQL's ACID guarantees in depth, explains how MVCC (Multi-Version Concurrency Control) implements isolation without blocking reads, and teaches you to reason about locking and deadlocks.

Understanding transactions is not optional for production database work. Every day, applications unknowingly create race conditions, lost updates, and phantom reads because developers don't understand isolation levels. This module gives you the vocabulary and tools to design concurrency-correct code.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/01_introduction]] — you need to understand: BEGIN/COMMIT/ROLLBACK basics
- [[modules/04_indexes-and-performance]] — you need to understand: how rows are stored (heap tuples) — relevant to MVCC internals

---

## Objectives

By the end of this module, you will be able to:

1. Explain each of the four ACID properties with a concrete example showing why each matters
2. Describe the three classic concurrency anomalies: dirty reads, non-repeatable reads, and phantom reads
3. Explain how PostgreSQL's MVCC mechanism prevents blocking reads with xmin/xmax tuple visibility
4. Choose the appropriate isolation level (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) for a given use case
5. Use `SELECT ... FOR UPDATE` and `FOR SHARE` for explicit row locking and explain when they are needed
6. Recognize and resolve deadlocks

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **ACID Deep Dive**
> - Atomicity: the transaction as a logical unit; what happens on a crash mid-transaction
> - Consistency: constraint checking at commit; deferrable constraints
> - Isolation: the spectrum from READ UNCOMMITTED to SERIALIZABLE
> - Durability: WAL (Write-Ahead Log) as the durability mechanism; fsync
>
> **Concurrency Anomalies**
> - Dirty read: reading uncommitted data from another transaction
> - Non-repeatable read: same row reads differently within a transaction
> - Phantom read: a query returns different rows on two executions within a transaction
> - Lost update: two transactions read-modify-write the same row; one overwrites the other
>
> **MVCC Internals**
> - xmin and xmax: the visibility stamps on every tuple
> - Snapshot isolation: each transaction sees the database as of its start
> - Dead tuples: why VACUUM is needed (MVCC leaves old versions around)
> - Transaction ID (XID) wraparound: the oldest danger in PostgreSQL administration
>
> **Isolation Levels in PostgreSQL**
> - READ COMMITTED (default): sees committed data as of each statement
> - REPEATABLE READ: snapshot taken at transaction start; prevents non-repeatable reads
> - SERIALIZABLE: SSI (Serializable Snapshot Isolation); prevents all anomalies
> - Note: PostgreSQL does not implement READ UNCOMMITTED (it behaves as READ COMMITTED)
>
> **Locking**
> - Table-level locks: ACCESS SHARE, ROW EXCLUSIVE, ACCESS EXCLUSIVE, etc.
> - Row-level locks: acquired on UPDATE, DELETE; SELECT FOR UPDATE/SHARE
> - Advisory locks: application-level locks (pg_advisory_lock)
> - Deadlock detection and automatic resolution
> - SKIP LOCKED: the queue pattern

---

## Key Concepts

**ACID:** Atomicity, Consistency, Isolation, Durability — the four properties that define reliable transaction processing. See [[shared/glossary#ACID]] for the definition.

**MVCC (Multi-Version Concurrency Control):** PostgreSQL's mechanism for allowing concurrent reads without blocking writes. Each transaction sees a snapshot of the database; writers create new tuple versions rather than overwriting existing ones. See [[shared/glossary#MVCC]].

**Isolation level:** The degree to which a transaction is isolated from changes made by concurrent transactions. PostgreSQL offers READ COMMITTED (default), REPEATABLE READ, and SERIALIZABLE. Higher isolation prevents more anomalies but may increase contention.

**Deadlock:** A cycle of transactions each waiting for a lock held by another. PostgreSQL detects deadlocks automatically and kills one transaction to break the cycle. Applications must be prepared to retry killed transactions.

**FOR UPDATE:** A row-level lock acquired by `SELECT ... FOR UPDATE`. Prevents other transactions from updating, deleting, or locking the selected rows until the current transaction commits.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Demonstrating lost update without explicit locking, and fixing it with FOR UPDATE
> - Example 2: Demonstrating REPEATABLE READ vs READ COMMITTED behavior with concurrent updates
> - Example 3: The SKIP LOCKED queue pattern for background job processing
> - Example 4: A deadlock scenario and how to resolve it by consistent lock ordering

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Assuming READ COMMITTED prevents all anomalies (it doesn't — lost update is still possible)
> - Long-running transactions holding locks and causing queue buildup
> - Not handling serialization failures in SERIALIZABLE mode (must retry on 40001 error)
> - Transaction ID wraparound: the consequence of not running VACUUM on old databases

---

## Cross-Links

- [[modules/04_indexes-and-performance]] — MVCC dead tuples affect index performance; understanding MVCC helps explain bloat
- [[modules/11_administration-and-tuning]] — VACUUM is the direct consequence of MVCC's dead tuple accumulation
- [[modules/09_replication-and-ha]] — replication and WAL are directly related to durability and consistency
- [[async-python]] — async database clients must handle transaction lifecycle correctly to avoid connection state bugs

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - ACID: Atomicity, Consistency, Isolation, Durability
> - Three concurrency anomalies: dirty read, non-repeatable read, phantom read
> - MVCC: xmin/xmax visibility, snapshot isolation, why readers don't block writers
> - Isolation levels: READ COMMITTED, REPEATABLE READ, SERIALIZABLE
> - Explicit locking: FOR UPDATE, FOR SHARE, SKIP LOCKED
> - Deadlocks: detection, resolution, prevention
