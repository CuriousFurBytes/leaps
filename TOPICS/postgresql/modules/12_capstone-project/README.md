# Module 12: Capstone Project — Production Multi-Tenant SaaS Database

[← Module 11](../11_administration-and-tuning/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-purple)
![Time](https://img.shields.io/badge/time-15--20h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Milestones](#milestones)
5. [Help — Getting Unstuck](#help--getting-unstuck)
6. [Acceptance Criteria](#acceptance-criteria)
7. [Cross-Links](#cross-links)
8. [A Note on Solutions](#a-note-on-solutions)

---

## Overview

This is the capstone module for the PostgreSQL topic. You will design, implement, and optimize a production-grade multi-tenant SaaS database for a task management application — something in the spirit of a simplified Jira or Linear.

This module is **build-oriented**. There is theory embedded in the milestones and help sections, but the primary output is a working PostgreSQL database that you designed and can explain. You should expect to revisit earlier modules during this build — that is intentional.

> [!IMPORTANT]
> **Do not skip to the Help section.** The struggle is the learning. Use the Help section only when you have genuinely tried and cannot move forward. Staged hints are provided for exactly this purpose — read one hint at a time, try again, then read the next only if still stuck.

---

## Prerequisites

- All prior modules (01–11) — specifically: schema design, querying, indexes, transactions, advanced SQL, JSONB, triggers, replication, partitioning, and administration
- This module synthesizes the entire topic. If you have gaps in earlier modules, fill them before attempting the capstone.

---

## Project Brief

### The Application: TaskFlow

**TaskFlow** is a multi-tenant project management SaaS application. Multiple organizations (tenants) use the same application and the same database. Each tenant's data must be completely invisible to other tenants.

### Core Entities

Your database must model:

- **Organizations** — tenants in the system; each has a name, a plan (free/pro/enterprise), and a created_at timestamp
- **Users** — belong to organizations; have email, hashed password (TEXT, not real passwords), display name, role (owner/admin/member), and active/inactive status
- **Projects** — belong to organizations; have a name, description, optional metadata (JSONB for flexible custom fields), and an archive status
- **Tasks** — belong to projects; have a title, description (searchable), status (backlog/todo/in_progress/review/done), priority (low/medium/high/urgent), assignee (nullable FK to users), due date, and created/updated timestamps
- **Comments** — belong to tasks; have body text (searchable), author (FK to users), and timestamps
- **Attachments** — belong to tasks; store metadata only (filename, file_size, content_type, storage_url — no actual binary data)
- **Activity Log** — append-only audit trail; records every create/update/delete action on tasks and comments, with actor, action type, old/new values (JSONB), and timestamp

### Non-Functional Requirements

1. **Multi-tenant isolation via Row-Level Security** — all SELECT, INSERT, UPDATE, DELETE on tenant-scoped tables must be filtered by organization_id through RLS policies. An application role that cannot bypass RLS must be created.

2. **Full-text search** — tasks and comments must be searchable by text. Search must be fast (< 50ms for a 100,000-row table). Use a generated tsvector column with a GIN index.

3. **Partitioned activity log** — the activity_log table must be partitioned by month (RANGE on created_at). The current month's partition and at least two past months' partitions must exist.

4. **Proper indexing** — all foreign keys must be indexed. Additional indexes must be created for the most common access patterns (tasks by status, tasks by assignee, tasks by due date).

5. **Role architecture** — three roles: `taskflow_app` (the application role, no BYPASSRLS), `taskflow_readonly` (read-only access for reporting), `taskflow_superuser` (your admin role, owns objects).

6. **Replication documentation** — document (in a NOTES.md or separate .sql file) the streaming replication configuration you would use for a production deployment. You do not need to actually set it up, but your documentation must be accurate.

---

## Milestones

Work through these milestones in order. Complete each before moving to the next.

### Milestone 1: Schema Design (Paper Phase)

Before writing any SQL, design the schema on paper (or in a text file):

- [ ] Entity-relationship diagram: all entities, relationships, cardinalities
- [ ] For each table: columns, types, constraints, and justification for each choice
- [ ] Which tables will have RLS enabled?
- [ ] What indexes will you need beyond the automatic primary key indexes?
- [ ] How will you partition the activity_log?

**Deliverable:** A schema design document (can be plain text or SQL comments).

---

### Milestone 2: Core Schema and Constraints

Create all tables with:

- [ ] Appropriate data types (no FLOAT for anything numeric, TIMESTAMPTZ for all timestamps)
- [ ] All foreign key constraints with appropriate ON DELETE behavior
- [ ] CHECK constraints for status and priority enums (or use CREATE TYPE ... AS ENUM)
- [ ] NOT NULL on all required columns
- [ ] UNIQUE constraints where business rules require uniqueness

**Verification:** Run `\d tablename` for each table and confirm all constraints are shown.

---

### Milestone 3: Roles and Row-Level Security

- [ ] Create the three roles
- [ ] Grant appropriate privileges to each role
- [ ] Enable RLS on all tenant-scoped tables
- [ ] Create RLS policies that filter by `current_setting('app.organization_id')::BIGINT`
- [ ] Write a test that confirms organization A cannot see organization B's tasks

**Verification:** Set `SET app.organization_id = 1;` and confirm that queries only return org 1's data. Then set it to 2 and confirm only org 2's data appears.

---

### Milestone 4: Full-Text Search

- [ ] Add a generated tsvector column to tasks and comments
- [ ] Create GIN indexes on both tsvector columns
- [ ] Write a search function (or just a query) that searches tasks by title and description
- [ ] Verify search performance with EXPLAIN ANALYZE (should use Index Scan on GIN index)

---

### Milestone 5: Partitioned Activity Log

- [ ] Create the activity_log table partitioned by RANGE on created_at
- [ ] Create partitions for the current month and the two preceding months
- [ ] Create a partition for a future month
- [ ] Insert test data into the activity_log across multiple months
- [ ] Verify partition pruning with EXPLAIN ANALYZE on a date-filtered query

---

### Milestone 6: Indexing Strategy

- [ ] Create indexes for all foreign keys (check: does every FK column have an index?)
- [ ] Create an index for tasks by (organization_id, status) — the most common filter combination
- [ ] Create an index for tasks by (assignee_id, due_date) for "my upcoming tasks" queries
- [ ] Run EXPLAIN ANALYZE on your key queries and confirm indexes are being used

---

### Milestone 7: Replication Documentation

In the module's NOTES.md, document:
- [ ] What streaming replication topology would you use? (Primary + how many standbys? Sync or async?)
- [ ] The postgresql.conf settings you would change on the primary
- [ ] The recovery configuration you would use on the standby
- [ ] How would you verify replication lag? (pg_stat_replication query)
- [ ] What is your RTO (recovery time objective) for this system?

---

### Milestone 8: Demo and Documentation

- [ ] Write a set of representative SQL queries (not schema DDL — actual application queries): list a user's tasks, search for tasks, create an activity log entry
- [ ] Create sample data: at least 2 organizations, 5 users per org, 3 projects per org, 20 tasks per project
- [ ] Write a brief design document explaining your key decisions: why you chose ENUM vs CHECK for statuses, why you used the specific partition range, what trade-offs you made

---

## Help — Getting Unstuck

The hints below are staged. Read only as many as you need. Spoiling yourself on hints you didn't need reduces the learning value.

### Help: RLS Policies

<details>
<summary>Hint 1: How to pass the current organization to RLS policies</summary>

RLS policies can call `current_setting()` to access a session-level setting. In your application, you would run `SET app.organization_id = 42` at the start of each database session (after authenticating the user). Your RLS policy can then read this:

```sql
CREATE POLICY org_isolation ON tasks
  USING (organization_id = current_setting('app.organization_id')::BIGINT);
```

Make sure the application role does NOT have BYPASSRLS. Test by connecting as the application role and setting the organization_id.

</details>

<details>
<summary>Hint 2: Testing RLS</summary>

```sql
-- Connect as the application role (not superuser!)
SET ROLE taskflow_app;
SET app.organization_id = 1;
SELECT COUNT(*) FROM tasks;  -- should only count org 1's tasks
SET app.organization_id = 2;
SELECT COUNT(*) FROM tasks;  -- should only count org 2's tasks
```

If you're still seeing all rows, check: (1) Is RLS enabled on the table? (`ALTER TABLE tasks ENABLE ROW LEVEL SECURITY`) (2) Is FORCE ROW LEVEL SECURITY set? (superusers bypass RLS by default without FORCE) (3) Is the policy using the right column?

</details>

### Help: Partitioned Activity Log

<details>
<summary>Hint 1: Creating a RANGE partitioned table for monthly partitions</summary>

```sql
CREATE TABLE activity_log (
    id          BIGSERIAL,
    org_id      BIGINT    NOT NULL,
    user_id     BIGINT    NOT NULL,
    action_type TEXT      NOT NULL,
    target_type TEXT      NOT NULL,
    target_id   BIGINT    NOT NULL,
    old_values  JSONB,
    new_values  JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE activity_log_2024_04
  PARTITION OF activity_log
  FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');

CREATE TABLE activity_log_2024_05
  PARTITION OF activity_log
  FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
```

Note: the primary key must include the partition key. Add `PRIMARY KEY (id, created_at)`.

</details>

<details>
<summary>Hint 2: Verifying partition pruning</summary>

```sql
EXPLAIN SELECT * FROM activity_log
 WHERE created_at >= '2024-05-01' AND created_at < '2024-06-01';
```

Look for "Partitions removed during planning" in the output. If it says "0 partitions removed," the query is not being pruned — check that your WHERE clause includes the partition key.

</details>

### Help: Full-Text Search

<details>
<summary>Hint 1: Generated tsvector column</summary>

```sql
ALTER TABLE tasks
  ADD COLUMN search_vector TSVECTOR
  GENERATED ALWAYS AS (
    to_tsvector('english',
      coalesce(title, '') || ' ' || coalesce(description, '')
    )
  ) STORED;

CREATE INDEX idx_tasks_fts ON tasks USING GIN (search_vector);
```

The `GENERATED ALWAYS AS ... STORED` syntax ensures the column is automatically updated whenever `title` or `description` changes. The GIN index makes FTS queries fast.

</details>

<details>
<summary>Hint 2: Running a full-text search query</summary>

```sql
SELECT id, title, ts_rank(search_vector, query) AS rank
  FROM tasks, to_tsquery('english', 'authentication & bug') query
 WHERE search_vector @@ query
 ORDER BY rank DESC;
```

</details>

### Help: Schema Design (RLS + Partitioning interaction)

<details>
<summary>Hint: Activity log RLS with partitioning</summary>

Partitioned tables in PostgreSQL support RLS, but you must enable it on the parent table and create the policy on the parent — it propagates to partitions automatically.

```sql
ALTER TABLE activity_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON activity_log
  USING (org_id = current_setting('app.organization_id')::BIGINT);
```

</details>

---

## Acceptance Criteria

Your capstone is complete when:

- [ ] All 7 entities are modeled with appropriate types and constraints
- [ ] RLS is enforced and tested: org A cannot see org B's data, confirmed in SQL
- [ ] Full-text search returns results in < 50ms on a 100,000-row tasks table (verify with EXPLAIN ANALYZE)
- [ ] activity_log is partitioned by month; at least 3 partitions exist; partition pruning is confirmed
- [ ] All foreign keys are indexed; key query patterns use indexes (confirmed with EXPLAIN ANALYZE)
- [ ] Three roles exist with documented privileges
- [ ] Replication topology is documented in NOTES.md
- [ ] Sample data exists: 2+ orgs, 5+ users, 3+ projects, 20+ tasks per project, 10+ activity log entries
- [ ] Key application queries are written and verified
- [ ] A design document explains your major decisions

---

## Cross-Links

- [[modules/01_introduction]] — schema design fundamentals
- [[modules/02_data-types-and-schema]] — type choices and normalization decisions
- [[modules/04_indexes-and-performance]] — indexing strategy and EXPLAIN ANALYZE verification
- [[modules/05_transactions-and-concurrency]] — RLS interacts with transaction isolation
- [[modules/06_advanced-sql]] — CTE patterns for complex queries
- [[modules/07_json-and-full-text-search]] — FTS on tasks and comments; JSONB for activity log values
- [[modules/08_stored-procedures-and-triggers]] — trigger patterns for activity logging
- [[modules/09_replication-and-ha]] — replication documentation milestone
- [[modules/10_partitioning-and-extensions]] — activity log partitioning
- [[modules/11_administration-and-tuning]] — VACUUM and monitoring considerations

---

## A Note on Solutions

This module intentionally does not include a complete solution. The purpose is for you to build it yourself — the design decisions, the debugging, the iteration. If you complete the acceptance criteria, you have succeeded, regardless of whether your schema looks exactly like someone else's.

The help section provides enough guidance to get past any blocker without handing you the answer. Use it as a last resort, not a first step.

If you complete the capstone and want to compare your approach with others, look for PostgreSQL multi-tenancy write-ups from companies like Notion, GitLab, and Citus Data — they all document real production schemas publicly.
