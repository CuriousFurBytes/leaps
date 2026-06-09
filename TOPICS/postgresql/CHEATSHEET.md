# PostgreSQL — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [psql Meta-Commands](#psql-meta-commands)
- [DDL — Schema Definition](#ddl--schema-definition)
- [DML — Data Manipulation](#dml--data-manipulation)
- [Querying Patterns](#querying-patterns)
- [Indexes](#indexes)
- [Transactions and Locking](#transactions-and-locking)
- [JSON and Full-Text Search](#json-and-full-text-search)
- [Administration](#administration)
- [Decision Guide](#decision-guide)
- [Gotchas & Pitfalls](#gotchas--pitfalls)

---

## psql Meta-Commands

```sql
-- Database navigation
\l              -- list all databases
\c dbname       -- connect to database
\dn             -- list schemas
\dt             -- list tables in current schema
\dt schema.*    -- list tables in a specific schema
\d tablename    -- describe table (columns, indexes, constraints)
\d+ tablename   -- verbose describe (includes storage, triggers)
\di             -- list indexes
\df             -- list functions
\du             -- list roles/users
\dp             -- list table access privileges

-- Query tools
\timing         -- toggle query execution timing
\e              -- edit query in $EDITOR
\i filename.sql -- execute SQL from file
\o filename     -- redirect output to file
\x              -- toggle expanded display (good for wide rows)

-- Help
\h COMMAND      -- help for SQL command (e.g. \h SELECT)
\?              -- help for psql meta-commands
\q              -- quit
```

---

## DDL — Schema Definition

```sql
-- Create and drop database
CREATE DATABASE myapp;
DROP DATABASE myapp;

-- Create schema (namespace)
CREATE SCHEMA app;
SET search_path TO app, public;  -- prefer app schema

-- Create table with common patterns
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,           -- auto-increment 64-bit
    email       TEXT      NOT NULL UNIQUE,
    username    VARCHAR(50) NOT NULL,
    role        TEXT      NOT NULL DEFAULT 'user'
                          CHECK (role IN ('user','admin','moderator')),
    is_active   BOOLEAN   NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Add / modify columns
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
ALTER TABLE users ALTER COLUMN phone SET DEFAULT '';
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users RENAME COLUMN username TO handle;

-- Foreign key patterns
CREATE TABLE posts (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title      TEXT   NOT NULL,
    body       TEXT   NOT NULL DEFAULT ''
);

-- Add constraint after creation
ALTER TABLE posts ADD CONSTRAINT title_not_empty CHECK (length(title) > 0);

-- Remove constraint
ALTER TABLE posts DROP CONSTRAINT title_not_empty;

-- Indexes (see Indexes section for types)
CREATE INDEX idx_posts_user_id ON posts (user_id);
DROP INDEX idx_posts_user_id;
CREATE INDEX CONCURRENTLY idx_posts_created ON posts (created_at);  -- no lock
```

---

## DML — Data Manipulation

```sql
-- INSERT
INSERT INTO users (email, username) VALUES ('a@example.com', 'alice');
INSERT INTO users (email, username)
  VALUES ('b@example.com', 'bob'), ('c@example.com', 'carol');

-- INSERT … SELECT
INSERT INTO archive_orders SELECT * FROM orders WHERE created_at < '2023-01-01';

-- UPSERT (ON CONFLICT)
INSERT INTO settings (user_id, theme) VALUES (1, 'dark')
  ON CONFLICT (user_id) DO UPDATE SET theme = EXCLUDED.theme;

INSERT INTO counters (key, value) VALUES ('pageviews', 1)
  ON CONFLICT (key) DO UPDATE SET value = counters.value + 1;

-- INSERT with RETURNING
INSERT INTO users (email) VALUES ('d@example.com') RETURNING id, created_at;

-- UPDATE
UPDATE users SET updated_at = now() WHERE id = 42;
UPDATE posts SET title = 'New Title' WHERE id = 7 RETURNING id, title;

-- UPDATE with JOIN (using FROM clause)
UPDATE posts
   SET status = 'published'
  FROM users
 WHERE posts.user_id = users.id
   AND users.role = 'admin';

-- DELETE
DELETE FROM posts WHERE created_at < now() - INTERVAL '1 year';
DELETE FROM users WHERE id = 42 RETURNING email;  -- RETURNING works on DELETE too

-- TRUNCATE (fast; no WAL for each row; resets sequences)
TRUNCATE orders RESTART IDENTITY CASCADE;
```

---

## Querying Patterns

```sql
-- Basic SELECT
SELECT id, email, created_at
  FROM users
 WHERE is_active = true
   AND created_at > now() - INTERVAL '30 days'
 ORDER BY created_at DESC
 LIMIT 20 OFFSET 40;   -- page 3 of 20-item pages

-- DISTINCT
SELECT DISTINCT user_id FROM orders;

-- All JOIN types
-- INNER JOIN (only matching rows)
SELECT u.email, o.total
  FROM users u
  JOIN orders o ON o.user_id = u.id;

-- LEFT JOIN (all users, even those with no orders)
SELECT u.email, COUNT(o.id) AS order_count
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.id
 GROUP BY u.id;

-- Aggregation
SELECT user_id,
       COUNT(*)            AS total_orders,
       SUM(total)          AS revenue,
       AVG(total)::NUMERIC(10,2) AS avg_order,
       MIN(created_at)     AS first_order,
       MAX(created_at)     AS last_order
  FROM orders
 GROUP BY user_id
HAVING COUNT(*) > 5
 ORDER BY revenue DESC;

-- Window functions
SELECT user_id, total, created_at,
       ROW_NUMBER()  OVER (PARTITION BY user_id ORDER BY created_at)  AS order_num,
       SUM(total)    OVER (PARTITION BY user_id ORDER BY created_at)  AS running_total,
       LAG(total, 1) OVER (PARTITION BY user_id ORDER BY created_at)  AS prev_order_total
  FROM orders;

-- CTE (WITH clause)
WITH monthly AS (
  SELECT DATE_TRUNC('month', created_at) AS month,
         SUM(total) AS revenue
    FROM orders
   GROUP BY 1
)
SELECT month, revenue,
       SUM(revenue) OVER (ORDER BY month) AS cumulative_revenue
  FROM monthly
 ORDER BY month;

-- Recursive CTE (hierarchy traversal)
WITH RECURSIVE hierarchy AS (
  SELECT id, name, manager_id, 0 AS depth
    FROM employees
   WHERE manager_id IS NULL        -- anchor: root node(s)
  UNION ALL
  SELECT e.id, e.name, e.manager_id, h.depth + 1
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.id
)
SELECT * FROM hierarchy ORDER BY depth, name;

-- LATERAL JOIN (correlated subquery in FROM)
SELECT u.email, recent.total
  FROM users u,
  LATERAL (
    SELECT total FROM orders
     WHERE user_id = u.id
     ORDER BY created_at DESC
     LIMIT 1
  ) AS recent;
```

---

## Indexes

```sql
-- B-tree (default) — equality and range queries
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_created ON orders (created_at DESC);  -- DESC for recent-first queries
CREATE INDEX idx_orders_user_status ON orders (user_id, status);  -- compound index

-- Partial index — only index rows matching a condition
CREATE INDEX idx_orders_pending ON orders (created_at) WHERE status = 'pending';

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users (email);

-- Expression index
CREATE INDEX idx_users_lower_email ON users (LOWER(email));
-- Now: WHERE LOWER(email) = 'alice@example.com' uses the index

-- Hash — equality only, faster than B-tree for equality on large keys
CREATE INDEX idx_sessions_token ON sessions USING HASH (token);

-- GIN — for arrays, JSONB, full-text search
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);
CREATE INDEX idx_docs_body_fts ON docs USING GIN (to_tsvector('english', body));
CREATE INDEX idx_products_attrs ON products USING GIN (attributes jsonb_path_ops);

-- GiST — for geometric types, ranges, nearest-neighbor
CREATE INDEX idx_events_range ON events USING GIST (tsrange(start_at, end_at));

-- BRIN — for naturally ordered large tables (timestamps in append-only tables)
CREATE INDEX idx_logs_created ON logs USING BRIN (created_at);

-- Build index without locking writes (safe in production)
CREATE INDEX CONCURRENTLY idx_big_table_col ON big_table (col);

-- Inspect index usage
SELECT indexname, idx_scan, idx_tup_read, idx_tup_fetch
  FROM pg_stat_user_indexes
 WHERE relname = 'orders';
```

---

## Transactions and Locking

```sql
-- Explicit transaction
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- or ROLLBACK to undo everything

-- Savepoints (partial rollback)
BEGIN;
  INSERT INTO orders (...) VALUES (...);
  SAVEPOINT after_order;
  INSERT INTO payments (...) VALUES (...);  -- this fails
  ROLLBACK TO after_order;  -- undo only the payment insert
  -- order insert is still pending
COMMIT;

-- Isolation levels
BEGIN ISOLATION LEVEL READ COMMITTED;    -- default
BEGIN ISOLATION LEVEL REPEATABLE READ;   -- prevents non-repeatable reads
BEGIN ISOLATION LEVEL SERIALIZABLE;      -- strongest; prevents all anomalies

-- Explicit row locking
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;           -- exclusive lock
SELECT * FROM accounts WHERE id = 1 FOR SHARE;            -- shared lock
SELECT * FROM accounts WHERE id = 1 FOR UPDATE SKIP LOCKED; -- skip locked rows (queue pattern)

-- Advisory locks (application-level)
SELECT pg_advisory_xact_lock(12345);    -- session-level exclusive advisory lock
SELECT pg_try_advisory_lock(12345);     -- non-blocking attempt; returns boolean
```

---

## JSON and Full-Text Search

```sql
-- JSONB operators
SELECT data -> 'key'          -- returns JSON value (keeps type)
SELECT data ->> 'key'         -- returns TEXT value
SELECT data -> 'nested' -> 'key'  -- nested access
SELECT data #> '{a,b,c}'      -- path access
SELECT data #>> '{a,b,c}'     -- path access as text

-- JSONB containment
SELECT * FROM products WHERE attributes @> '{"color": "red"}';

-- JSONB existence
SELECT * FROM products WHERE attributes ? 'color';
SELECT * FROM products WHERE attributes ?| ARRAY['color', 'size'];  -- any key

-- JSONB modification
UPDATE products SET attributes = attributes || '{"in_stock": true}';
UPDATE products SET attributes = attributes - 'discontinued_flag';

-- Full-text search
SELECT title, body
  FROM articles
 WHERE to_tsvector('english', title || ' ' || body) @@ to_tsquery('english', 'postgres & index')
 ORDER BY ts_rank(to_tsvector('english', title || ' ' || body),
                  to_tsquery('english', 'postgres & index')) DESC;

-- Add tsvector column (for performance)
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR
  GENERATED ALWAYS AS (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,''))) STORED;
CREATE INDEX idx_articles_fts ON articles USING GIN (search_vector);
```

---

## Administration

```sql
-- VACUUM
VACUUM articles;               -- reclaim dead tuples, non-blocking
VACUUM ANALYZE articles;       -- also update planner statistics
VACUUM FULL articles;          -- rewrite table compactly (ACCESS EXCLUSIVE lock!)
VACUUM VERBOSE articles;       -- show detailed output

-- Autovacuum tuning (in postgresql.conf or per-table)
ALTER TABLE high_churn_table SET (autovacuum_vacuum_scale_factor = 0.01);

-- Analyze (update planner statistics only)
ANALYZE articles;

-- EXPLAIN
EXPLAIN SELECT * FROM orders WHERE user_id = 42;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 42;
EXPLAIN (FORMAT JSON) SELECT * FROM orders WHERE user_id = 42;

-- Active queries monitoring
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
  FROM pg_stat_activity
 WHERE state != 'idle'
 ORDER BY duration DESC;

-- Kill a long-running query
SELECT pg_cancel_backend(pid);    -- graceful cancel
SELECT pg_terminate_backend(pid); -- forceful termination

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS total_size
  FROM pg_stat_user_tables
 ORDER BY pg_total_relation_size(relid) DESC;

-- Bloat check
SELECT relname, n_dead_tup, n_live_tup,
       round(n_dead_tup::numeric / nullif(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_pct
  FROM pg_stat_user_tables
 WHERE n_dead_tup > 1000
 ORDER BY dead_pct DESC;

-- Backup and restore
-- pg_dump mydb > mydb.sql
-- pg_dump -Fc mydb > mydb.dump        (custom format, compressed)
-- pg_restore -d mydb mydb.dump
-- pg_dumpall > all_databases.sql      (includes roles and tablespaces)
```

---

## Decision Guide

```
Which index type to use?
│
├── Equality and range queries on scalar values
│   └── B-tree (CREATE INDEX ... )  ← the default, use for most cases
│
├── Equality only on large keys (UUIDs, tokens)
│   └── Hash (USING HASH)
│
├── JSONB containment / array @>, ?, ?|
│   └── GIN with jsonb_path_ops (USING GIN)
│
├── Full-text search (tsvector columns)
│   └── GIN (USING GIN)
│
├── Range types, geometric types, nearest-neighbor
│   └── GiST (USING GIST)
│
├── Large append-only tables sorted by a column (time-series logs)
│   └── BRIN (USING BRIN)  ← very small, very fast for range scans on ordered data
│
└── Not sure?
    └── B-tree first; measure with EXPLAIN ANALYZE; switch if not helping
```

```
Which partitioning strategy?
│
├── Date/time ranges (monthly logs, daily events)
│   └── RANGE partitioning on timestamp column
│
├── Discrete categories (country, status, tenant_id)
│   └── LIST partitioning
│
├── Balanced distribution across N shards
│   └── HASH partitioning
│
└── No clear access pattern → probably don't partition yet
```

---

## Gotchas & Pitfalls

> [!WARNING]
> **UPDATE/DELETE without WHERE**
> Without a WHERE clause, you update or delete every row in the table.
>
> Wrong: `UPDATE users SET is_active = false;`
> Right: `UPDATE users SET is_active = false WHERE last_login < now() - INTERVAL '1 year';`
>
> In psql, you can protect yourself: `\set PROMPT1 '%/ (%x) %# '` and always double-check.

> [!WARNING]
> **NULL comparisons with = and !=**
> NULL is not equal to anything, including itself. `WHERE col = NULL` never matches any row.
>
> Wrong: `SELECT * FROM users WHERE phone = NULL;`
> Right: `SELECT * FROM users WHERE phone IS NULL;`

> [!WARNING]
> **Forgetting that SERIAL / BIGSERIAL are not standard SQL**
> SERIAL creates a sequence and sets a DEFAULT; it does not define a type.
> Use `BIGINT GENERATED ALWAYS AS IDENTITY` (SQL standard) or `BIGSERIAL` (Postgres shorthand).
>
> Also: SERIAL does not prevent manual inserts — you can INSERT an explicit id that collides later.

**Other things to watch out for:**

- **VACUUM FULL holds an ACCESS EXCLUSIVE lock** — no reads or writes during the operation; use `pg_repack` for online table compaction in production
- **Indexes do not automatically speed up all queries** — a partial index or expression index may be needed; always verify with EXPLAIN ANALYZE
- **Connection counts are limited** — default is 100; use PgBouncer or similar for high-concurrency applications
- **TEXT vs VARCHAR** — in PostgreSQL there is effectively no performance difference; TEXT is generally preferred; VARCHAR(n) only if you need the length constraint enforced
- **Timestamp without time zone is a footgun** — always use TIMESTAMPTZ (timestamp with time zone) to avoid timezone-related bugs

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| Relational model basics, psql commands | [[modules/01_introduction]] |
| Data types, constraints, normalization | [[modules/02_data-types-and-schema]] |
| JOINs, window functions, CTEs | [[modules/03_querying]] |
| Index types, EXPLAIN ANALYZE | [[modules/04_indexes-and-performance]] |
| ACID, isolation levels, MVCC | [[modules/05_transactions-and-concurrency]] |
| Recursive CTEs, UPSERT, RETURNING | [[modules/06_advanced-sql]] |
| JSONB operators, full-text search | [[modules/07_json-and-full-text-search]] |
| PL/pgSQL, triggers, generated columns | [[modules/08_stored-procedures-and-triggers]] |
| Replication, Patroni, failover | [[modules/09_replication-and-ha]] |
| Partitioning, PostGIS, extensions | [[modules/10_partitioning-and-extensions]] |
| VACUUM, pg_stat_*, tuning, backup | [[modules/11_administration-and-tuning]] |

---

_Last updated: 2026-06-09_
