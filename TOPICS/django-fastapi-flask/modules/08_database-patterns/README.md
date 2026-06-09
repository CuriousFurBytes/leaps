# Module 08: Database Patterns — SQLAlchemy, N+1, Connection Pooling, Bulk Operations, and Migrations

[← Module 07: FastAPI Advanced](../07_fastapi-advanced/README.md) | [Topic Home](../../README.md) | [Next → Module 09: Authentication and Security](../09_authentication-and-security/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers SQLAlchemy Core vs ORM, the N+1 query problem and how to solve it, database connection pooling, bulk insert/update operations, and Alembic migrations. Full content to be generated on demand.

---

## Overview

Every production web application eventually runs into the same database performance problems: slow queries, too many queries, database connections exhausted, or migrations that fail on a live database. This module is a cross-framework examination of those problems and how to solve them.

You will learn SQLAlchemy's two API layers (Core and ORM), understand the N+1 problem deeply enough to recognize and fix it in any framework, configure connection pooling correctly, perform bulk operations efficiently, and write Alembic migrations that can run on a live database without downtime.

---

## Prerequisites

- Module 03: Flask Advanced — SQLAlchemy basics
- Module 04: Django Fundamentals — ORM and migrations basics
- [[postgresql]] — basic PostgreSQL knowledge recommended

---

## Objectives

By the end of this module, you will be able to:

1. Explain the difference between SQLAlchemy Core and ORM and choose the right layer for a given query
2. Identify the N+1 query problem in code and fix it using `joinedload`, `selectinload` (SQLAlchemy) or `select_related`/`prefetch_related` (Django)
3. Configure SQLAlchemy's connection pool (`pool_size`, `max_overflow`, `pool_timeout`) and explain the consequences of misconfiguration
4. Perform bulk inserts and updates efficiently (SQLAlchemy `insert().values()`, Django `bulk_create`, `bulk_update`)
5. Write Alembic migrations that are reversible, safe for concurrent access, and suitable for running on a live database
6. Use database indexes correctly and explain when a query will and will not use an index

---

## Topics Covered

- SQLAlchemy Core: `text()`, `select()`, `insert()`, `update()`, `delete()`, compiled expressions
- SQLAlchemy ORM 2.0: `select(Model)`, `session.execute()`, `session.scalars()`, `session.add()`, `session.commit()`
- Lazy loading vs eager loading: `lazy="select"` vs `joinedload` vs `selectinload`
- N+1 query problem: detection with SQLAlchemy event logging, Django `connection.queries`, fixing with eager loads
- Connection pooling: `QueuePool`, `pool_size`, `max_overflow`, `pool_recycle`, `pool_timeout`, `NullPool` for async
- Bulk operations: `session.execute(insert(Model).values([...]))`, Django `Model.objects.bulk_create()`
- Alembic: `alembic init`, `alembic revision --autogenerate`, `alembic upgrade head`, `alembic downgrade`
- Zero-downtime migrations: adding nullable columns, backfilling data, adding constraints after backfill
- Database indexes: B-tree, partial indexes, composite indexes, when `EXPLAIN ANALYZE` matters

---

## Cross-Links

- [[django-fastapi-flask/modules/03_flask-advanced]] — Flask-SQLAlchemy setup
- [[django-fastapi-flask/modules/04_django-fundamentals]] — Django ORM and migrations
- [[postgresql]] — PostgreSQL internals, query planning, EXPLAIN ANALYZE
- [[shared/glossary#orm]] — ORM glossary entry
- [[shared/glossary#migration]] — migration glossary entry

---

## Summary

- SQLAlchemy Core is for raw query control; ORM is for working with Python objects — use Core for bulk operations and complex queries
- The N+1 problem is caused by lazy loading in a loop; always use eager loading (`joinedload`/`select_related`) for related objects you know you will access
- Connection pools have a fixed size; exceeding it causes requests to queue or fail — size the pool to match your expected concurrency
- Bulk operations skip Python-level validation but are orders of magnitude faster for large datasets
- Alembic migrations should be reversible and reviewed as carefully as application code — a bad migration can destroy data
- Zero-downtime migrations require a multi-step process: add nullable column → backfill → add constraint
