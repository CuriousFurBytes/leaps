# Module 09: Replication and High Availability

[← Module 08](../08_stored-procedures-and-triggers/) | [Topic Home](../../README.md) | [Next → Module 10](../10_partitioning-and-extensions/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-purple)
![Time](https://img.shields.io/badge/time-9--11h-orange)

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

A single-node database is a single point of failure. This module covers the mechanisms PostgreSQL provides for replication and high availability: streaming replication (the primary mechanism for maintaining a hot standby), logical replication (for selective table-level replication and zero-downtime schema migrations), and the architectural patterns used to build highly available Postgres clusters.

You will also learn about Patroni — the de facto standard for automated PostgreSQL failover in production — and understand how distributed consensus (via etcd or ZooKeeper) is used to make failover decisions safely.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/05_transactions-and-concurrency]] — you need to understand: WAL (Write-Ahead Log) and durability — the foundation of replication
- [[modules/11_administration-and-tuning]] — this module and Module 11 have a circular dependency; the basics of pg_hba.conf and server configuration are needed

---

## Objectives

By the end of this module, you will be able to:

1. Explain how WAL-based streaming replication works: primary writes WAL, standby streams and replays it
2. Set up a streaming replication pair (primary + hot standby) and verify replication lag
3. Explain the difference between synchronous and asynchronous replication and the trade-off between data safety and performance
4. Configure logical replication for selective table-level replication
5. Describe Patroni's architecture: how it uses distributed consensus to automate failover without split-brain
6. Explain the replication slot mechanism and why unacknowledged slots cause disk space issues

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **WAL and Durability**
> - Write-Ahead Log: how changes are written to WAL before data pages
> - WAL segments and the pg_wal directory
> - WAL level settings: minimal, replica, logical
>
> **Streaming Replication**
> - Primary → standby WAL stream: walsender and walreceiver processes
> - pg_basebackup: creating a base backup for initial standby setup
> - recovery.conf / postgresql.conf standby configuration (PostgreSQL 12+ uses standby.signal)
> - Hot standby: queries on the standby (read replicas)
> - Replication lag: pg_stat_replication view
>
> **Synchronous vs Asynchronous Replication**
> - Async (default): primary commits as soon as WAL is written locally; standby may be behind
> - Sync (synchronous_commit = on): primary waits for standby to confirm WAL receipt before returning to client
> - synchronous_commit = remote_write / remote_apply: intermediate levels
> - Trade-off: data durability vs write latency
>
> **Logical Replication**
> - Publication (publisher) and subscription (subscriber) model
> - Table-level granularity: replicate only specific tables
> - Row filter and column list (PostgreSQL 15+)
> - Use case: zero-downtime major version upgrades, data distribution to separate systems
> - Logical replication slots: tracking progress
>
> **Replication Slots**
> - Purpose: ensure WAL is kept until all subscribers have consumed it
> - Danger: an inactive slot causes WAL accumulation and potential disk exhaustion
> - Monitoring: pg_replication_slots; wal_receiver_status_interval
>
> **High Availability Architectures**
> - VIP (Virtual IP) failover: simplest approach
> - Patroni + etcd/Consul/ZooKeeper: distributed consensus for leader election
> - Patroni's DCS (Distributed Configuration Store): how it prevents split-brain
> - pg_auto_failover: simpler alternative for smaller deployments
> - Connection poolers: PgBouncer for connection management during failover

---

## Key Concepts

**WAL (Write-Ahead Log):** The sequential log to which all changes are written before data pages are modified. WAL provides durability and is the foundation of replication. See [[shared/glossary#WAL]].

**Streaming replication:** PostgreSQL's primary replication mechanism. The primary sends WAL records to standbys in real time via a TCP connection. Standbys replay the WAL and maintain a physically identical copy of the database.

**Hot standby:** A standby server that accepts read-only queries while replaying WAL from the primary. Enables horizontal read scaling and DR (disaster recovery) with low RTO.

**Logical replication:** A replication mode that streams logical changes (INSERT/UPDATE/DELETE on specific tables) rather than physical WAL records. Allows replication between different Postgres versions and selective table replication.

**Patroni:** An open-source Python tool for automated PostgreSQL high availability. It uses a distributed configuration store (etcd, Consul, or ZooKeeper) for leader election, ensuring only one primary at a time and preventing split-brain.

**Split-brain:** The catastrophic scenario where two nodes each believe they are the primary and accept writes, creating divergent data. Patroni's DCS-based leader election prevents this.

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Setting up streaming replication with pg_basebackup
> - Example 2: Querying pg_stat_replication to monitor replication lag
> - Example 3: Creating a logical replication publication and subscription
> - Example 4: Walkthrough of Patroni configuration (conceptual — actual deployment requires infrastructure)

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Replication slots accumulating WAL and filling the disk (most common production emergency)
> - Promoting a standby manually without Patroni: risk of split-brain
> - Synchronous replication causing write latency spikes when standby falls behind
> - Logical replication not replicating schema changes (DDL) — must be applied manually

---

## Cross-Links

- [[modules/05_transactions-and-concurrency]] — WAL is the direct mechanism for durability; understanding transactions helps understand why replication is correct
- [[modules/11_administration-and-tuning]] — backup strategies, WAL configuration, and monitoring all relate to replication
- [[systems-architecture]] — replication and HA are fundamental distributed systems design decisions

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - WAL: the foundation of both durability and replication
> - Streaming replication: primary → standby via walsender/walreceiver
> - Synchronous vs asynchronous replication: durability vs latency trade-off
> - Logical replication: table-level, cross-version, publication/subscription model
> - Replication slots: purpose, danger of unacknowledged slots
> - Patroni: DCS-based leader election, split-brain prevention
