# PostgreSQL

> PostgreSQL is a production-grade relational database system for storing, querying, protecting, and operating structured data.

## Table of Contents
1. [Why Learn PostgreSQL?](#why-learn-postgresql)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)
6. [How to Use This Topic](#how-to-use-this-topic)

## Why Learn PostgreSQL?

PostgreSQL is one of the most important open-source database systems in modern software. It combines the relational model, transactional safety, SQL, indexing, procedural extensions, JSON support, replication, and mature operational tooling into a database that can run tiny personal projects and large production systems.

Learning PostgreSQL well teaches more than one product. It teaches how applications persist facts, how constraints protect data quality, how query planners reason about work, how transactions prevent subtle race conditions, and how operators keep systems recoverable under failure. Those skills transfer directly to backend engineering, data engineering, analytics engineering, DevOps, and platform work.

This path starts at zero: what a database is, how to install PostgreSQL, and how to run the first query. It then moves through SQL, schema design, indexing, transactions, performance, administration, replication, security, and production architecture. The final module is a capstone project where you design and operate a realistic PostgreSQL-backed system.

## Prerequisites

- Basic command-line comfort: running commands, reading file paths, and editing text files.
- Basic programming literacy from [[go]] or [[javascript-typescript-react]] helps, but this topic does not require professional programming experience.
- A willingness to reason carefully about data models, failure, tradeoffs, and long-lived systems.
- Reference vocabulary lives in [[shared]], [[shared/concepts/concurrency]], and [[shared/concepts/memory-management]].

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Introduction and Setup](./modules/01_introduction_and_setup/README.md) | Beginner | [ ] |
| 02 | [SQL Foundations](./modules/02_sql_foundations/README.md) | Beginner | [ ] |
| 03 | [Schema Design and Constraints](./modules/03_schema_design_and_constraints/README.md) | Intermediate | [ ] |
| 04 | Data Types, Expressions, and Functions | Intermediate | [ ] |
| 05 | Joins, Aggregation, and Analytical Queries | Intermediate | [ ] |
| 06 | Indexes and Query Planning | Advanced | [ ] |
| 07 | Transactions, MVCC, and Concurrency | Advanced | [ ] |
| 08 | Views, CTEs, Procedures, and Triggers | Advanced | [ ] |
| 09 | JSON, Full-Text Search, and Extensions | Advanced | [ ] |
| 10 | Security, Roles, Backups, and Recovery | Expert | [ ] |
| 11 | Replication, Partitioning, and Production Operations | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links

- [[go]] — useful for building typed services that talk to PostgreSQL.
- [[javascript-typescript-react]] — useful for web applications backed by PostgreSQL APIs.
- [[shared]] — shared reference area for cross-topic learning material.
- [[shared/concepts/concurrency]] — core vocabulary for concurrent systems and transactions.
- [[shared/concepts/memory-management]] — useful contrast for storage and resource management ideas.

## Quick Reference

| Task | Command or SQL |
|---|---|
| Open an interactive shell | `psql -d postgres` |
| List databases | `\l` |
| List tables | `\dt` |
| Describe a table | `\d table_name` |
| Create a database | `CREATE DATABASE app_dev;` |
| Create a table | `CREATE TABLE users (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, email text NOT NULL UNIQUE);` |
| Insert a row | `INSERT INTO users (email) VALUES ('learner@example.com');` |
| Read rows | `SELECT id, email FROM users ORDER BY id;` |
| Update rows safely | `UPDATE users SET email = 'new@example.com' WHERE id = 1;` |
| Delete rows safely | `DELETE FROM users WHERE id = 1;` |
| Inspect a query plan | `EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'new@example.com';` |

## How to Use This Topic

Work through the modules in order unless you already operate PostgreSQL professionally. Do the exercises before the tests, write questions in `QUESTIONS.md`, and treat the capstone as proof that you can synthesize modeling, SQL, performance, safety, and operations into one realistic system.
