# Module 08: Async Databases

[← Module 07](../07_performance-patterns/) | [Topic Home](../../README.md) | [Next → Module 09](../09_testing-async/)

---

![Status](https://img.shields.io/badge/status-stub-orange)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-6h-orange)

> **Stub module** — Full content to be generated. This file defines the scope and
> prerequisites so the topic roadmap is complete.

---

## Overview

Database access is typically the dominant I/O in backend services. Replacing blocking
database calls with async equivalents is one of the highest-impact changes you can make
to a Python service's throughput. This module covers the three layers of async database
access: raw drivers (`asyncpg` for PostgreSQL), the lightweight `databases` library, and
SQLAlchemy 2.x's first-class async session API.

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

## Prerequisites

- Module 07: Performance Patterns (connection pooling)
- Module 04: Async I/O Patterns
- Basic SQL knowledge — SELECT, INSERT, UPDATE, transactions
- [[postgresql]] — recommended familiarity with PostgreSQL

---

## Objectives

By the end of this module, you will be able to:

1. Connect to PostgreSQL asynchronously using `asyncpg` with a connection pool
2. Execute queries, handle results, and use transactions with `asyncpg`
3. Configure SQLAlchemy 2.x for async operation using `AsyncSession` and `async_engine`
4. Write async ORM queries and relationships with SQLAlchemy's async API
5. Use the `databases` library for simple async database access
6. Understand how async database migrations work (Alembic with async engines)

---

## Theory

> **Full content to be generated.** Topics to cover:
>
> - Why blocking database drivers (psycopg2, sqlite3) break the event loop
> - `asyncpg`: direct PostgreSQL protocol client; `create_pool()`, query execution,
>   prepared statements, `asyncpg.Record` objects
> - SQLAlchemy 2.x async API: `create_async_engine()`, `AsyncSession`,
>   `async_sessionmaker`, `AsyncScoped Session`
> - Async ORM patterns: `await session.execute()`, `await session.scalar()`,
>   `selectinload()` and `joinedload()` for async relationship loading
> - Transaction management in async context: `async with session.begin()`
> - `databases` library: simple async queries without ORM overhead
> - Alembic with async engines: running migrations with `asyncio.run()`
> - Connection pool sizing: threads_per_pool, pool_size, pool_timeout

---

## Key Concepts

> To be filled in when this module is fully generated.

---

## Examples

> To be filled in when this module is fully generated.

---

## Common Pitfalls

> To be filled in when this module is fully generated.

---

## Cross-Links

- [[async-python/modules/07_performance-patterns]] — prerequisite; connection pooling
- [[postgresql]] — SQL and PostgreSQL knowledge assumed
- [[async-python/modules/11_capstone-project]] — the capstone uses async database writes

---

## Summary

> To be filled in when this module is fully generated.
