# Module 12: Capstone Project

> Build and document a realistic PostgreSQL-backed service data layer with schema, queries, safety checks, and operations notes.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Project Brief](#project-brief)
5. [Milestones](#milestones)
6. [Help and Getting Unstuck](#help-and-getting-unstuck)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

This capstone is the final proof of PostgreSQL competence. You will build a realistic data layer for a multi-tenant issue tracker, inventory system, booking system, or other domain with enough complexity to require thoughtful schema design, queries, transactions, indexes, security, and recovery notes.

The goal is not to copy a finished solution. The goal is to make professional decisions, document tradeoffs, measure important queries, and leave behind a database project that another engineer could review and operate.

## Prerequisites

- Modules 01 through 11 in this topic.
- Comfort writing SQL, reading query plans, and explaining data integrity rules.

## Objectives

By the end of this module, you will be able to:

- Design a normalized PostgreSQL schema for a realistic application domain.
- Implement constraints, indexes, seed data, and representative queries.
- Use transactions to protect multi-step business workflows.
- Document backup, recovery, access-control, and performance decisions.
- Present the database as a maintainable professional artifact.

## Project Brief

Build a PostgreSQL-backed data layer for one realistic product. Your repository should contain Markdown design notes and SQL scripts for setup, seed data, verification queries, and operational checks.

```sql
-- Example audit table pattern you may adapt, not copy as a full solution.
CREATE TABLE audit_events (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, happened_at timestamptz NOT NULL DEFAULT now(), event_type text NOT NULL);
```

```sql
-- Example performance inspection pattern for your own representative query.
EXPLAIN (ANALYZE, BUFFERS) SELECT event_type, count(*) FROM audit_events GROUP BY event_type;
```

```sql
-- Example transactional safety pattern for a workflow checkpoint.
BEGIN; INSERT INTO audit_events (event_type) VALUES ('capstone.started'); COMMIT;
```

## Milestones

1. Choose a domain and write the core business rules.
2. Draw the entities, relationships, and invariants in prose or Mermaid.
3. Create tables with primary keys, foreign keys, unique constraints, and checks.
4. Add seed data that includes normal and edge cases.
5. Write at least ten representative queries, including joins and aggregation.
6. Add indexes only after explaining the query each index supports.
7. Demonstrate one transaction that prevents a realistic consistency bug.
8. Write operations notes for roles, backups, restore testing, and monitoring.

## Help and Getting Unstuck

- **If the schema feels too small:** add users, organizations, lifecycle states, audit events, and at least one many-to-many relationship.
- **If constraints feel unclear:** write the invariant in English first, then decide whether it belongs in `NOT NULL`, `UNIQUE`, `CHECK`, a foreign key, or a transaction.
- **If performance work feels abstract:** choose three important user-facing screens and write the query each screen needs.
- **If operations feel unfamiliar:** document the simplest backup and restore rehearsal you could run in a development environment.

Do not turn these hints into a copy-paste solution. Use them as checkpoints that help you keep ownership of the design.

## Acceptance Criteria

- The project includes setup SQL, seed SQL, verification queries, and design notes.
- Every important table has a stated purpose and at least one integrity rule.
- At least three queries include `EXPLAIN` output or written plan observations.
- The project explains at least two tradeoffs you considered and rejected.
- The final write-up links decisions back to earlier PostgreSQL modules.

## Cross-Links

- [[postgresql]] — the full topic sequence synthesized by this project.
- [[go]] — a possible service implementation language for the capstone.
- [[javascript-typescript-react]] — a possible client/API context for the capstone.
- [[shared/concepts/concurrency]] — shared vocabulary for concurrent systems and transactions.

## Summary

- The capstone turns isolated PostgreSQL skills into one realistic database artifact.
- A strong solution explains not just what SQL exists, but why each decision was made.
- Correctness, performance, security, and recovery all matter at the same time.
- The learner drives the build; hints unblock without replacing the work.
- Completion means the database is reviewable, testable, and operable.
