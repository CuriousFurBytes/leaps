# PostgreSQL — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of PostgreSQL.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use. Code snippet or real-world scenario.
```

Keep definitions in your own words as much as possible. If you're copying from a source, add attribution.

---

## A

### ACID

**Definition:** An acronym describing the four properties that guarantee reliable processing of database transactions: **Atomicity** (a transaction either fully completes or fully rolls back — no partial state), **Consistency** (a transaction brings the database from one valid state to another, never violating defined constraints), **Isolation** (concurrent transactions behave as if they were executed serially), and **Durability** (once a transaction commits, its effects persist even through a system crash).

**Also known as:** ACID properties, ACID guarantees

**Related:** [[postgresql#transactions-and-concurrency]], [[shared/glossary#transaction]]

**Example:**
A bank transfer that debits account A and credits account B is atomic: if the credit fails, the debit is rolled back automatically. The final balance across both accounts always sums to the same total (consistency).

---

_Add more A-terms below this line_

---

## B

_Add B-terms here_

---

## C

_Add C-terms here_

---

## D

_Add D-terms here_

---

## E

### extension

**Definition:** A packaged set of SQL objects (functions, types, operators, index methods) that can be loaded into PostgreSQL with a single `CREATE EXTENSION` command. Extensions allow third-party capabilities to integrate deeply into the database engine. Examples include PostGIS (geospatial), pg_trgm (trigram similarity), and TimescaleDB (time-series).

**Also known as:** Postgres extension, module

**Related:** [[postgresql#partitioning-and-extensions]]

**Example:**
```sql
CREATE EXTENSION pg_trgm;  -- enables trigram similarity functions and GIN/GiST indexes
SELECT similarity('hello', 'helo');  -- returns 0.8 (approximate match)
```

---

_Add more E-terms here_

---

## F

_Add F-terms here_

---

## G

_Add G-terms here_

---

## H

_Add H-terms here_

---

## I

### index

**Definition:** A data structure maintained alongside a table that speeds up lookups by allowing the database to find matching rows without scanning every row in the table. PostgreSQL supports several index types: B-tree (the default), Hash, GIN, GiST, SP-GiST, and BRIN. Each type is optimized for different query patterns. Indexes consume storage and slow down writes slightly in exchange for faster reads.

**Also known as:** DB index, secondary index

**Related:** [[postgresql#indexes-and-performance]]

**Example:**
```sql
-- Without index: sequential scan of all rows
CREATE INDEX idx_orders_user_id ON orders (user_id);
-- Now: index scan; only rows with matching user_id are visited
EXPLAIN SELECT * FROM orders WHERE user_id = 42;
```

---

_Add more I-terms here_

---

## J

_Add J-terms here_

---

## K

_Add K-terms here_

---

## L

_Add L-terms here_

---

## M

### MVCC

**Definition:** Multi-Version Concurrency Control. PostgreSQL's strategy for handling concurrent read and write access without locking readers out. Each transaction sees a *snapshot* of the database as it existed at the start of that transaction. Writers create new row versions (called *tuples*) rather than overwriting existing ones. Old versions are cleaned up by the VACUUM process. MVCC is why readers never block writers and writers never block readers in PostgreSQL.

**Also known as:** Multi-Version Concurrency Control, snapshot isolation

**Related:** [[postgresql#transactions-and-concurrency]], [[postgresql#administration-and-tuning]]

**Example:**
Transaction A begins and reads a row. Transaction B updates that row and commits. Transaction A, still open, reads the same row again and sees the *original* value — its snapshot predates B's commit.

---

_Add more M-terms here_

---

## N

_Add N-terms here_

---

## O

_Add O-terms here_

---

## P

### page

**Definition:** The fundamental unit of storage in PostgreSQL, fixed at 8 KB by default. Tables and indexes are stored as arrays of pages. Each page contains a header, a row pointer array (item identifiers), free space, and the actual row data (tuples). Understanding pages is important for diagnosing table bloat and understanding how VACUUM works.

**Also known as:** block, heap page, 8KB page

**Related:** [[postgresql#administration-and-tuning]], [[postgresql#transactions-and-concurrency]]

**Example:**
A table with 1 million 100-byte rows occupies roughly 100 MB in 8KB pages. After many updates, dead tuples accumulate in those pages until VACUUM reclaims the space.

---

### planner

**Definition:** The PostgreSQL query planner (also called the query optimizer) is the subsystem that takes a parsed SQL query and determines the most efficient execution strategy. It estimates the cost of different execution plans — which indexes to use, in what order to join tables, whether to parallelize — and selects the lowest-cost plan. `EXPLAIN` shows the chosen plan; `EXPLAIN ANALYZE` executes it and shows actual timing.

**Also known as:** query planner, query optimizer, cost-based optimizer

**Related:** [[postgresql#indexes-and-performance]]

**Example:**
```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 42 AND status = 'shipped';
-- Shows: whether the planner uses an index scan, bitmap scan, or seq scan
-- and the estimated cost and row count for each plan node
```

---

_Add more P-terms here_

---

## Q

_Add Q-terms here_

---

## R

### relation

**Definition:** In the relational model and in PostgreSQL's internal vocabulary, a *relation* is any named set of tuples with a fixed set of attributes — the general term for what most people call a "table." PostgreSQL also uses "relation" internally to refer to views, sequences, and indexes, since they are all stored in the system catalog (`pg_class`) as relations.

**Also known as:** table (informal), base relation

**Related:** [[shared/glossary#algorithm]]

**Example:**
The SQL statement `CREATE TABLE orders (...)` creates a base relation called `orders`. PostgreSQL stores its metadata in `pg_class` with `relkind = 'r'` (relation).

---

### role

**Definition:** PostgreSQL's unified concept for both users and groups. A role can log in (if `LOGIN` privilege is granted) making it equivalent to a user, or it can represent a group of privileges. Roles can be granted to other roles, creating hierarchies. Every database object has an owner role, and access control is enforced through `GRANT` and `REVOKE` on roles.

**Also known as:** user (when LOGIN is granted), group (when used to bundle permissions)

**Related:** [[postgresql#administration-and-tuning]]

**Example:**
```sql
CREATE ROLE app_user LOGIN PASSWORD 'secret';
CREATE ROLE readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
GRANT readonly TO app_user;  -- app_user inherits SELECT permission
```

---

_Add more R-terms here_

---

## S

### schema

**Definition:** A namespace within a PostgreSQL database that groups related tables, views, functions, and types. A single database can contain multiple schemas. The default schema is `public`. Schemas are used to organize objects (e.g., separating application tables from audit tables), to support multi-tenancy, and to avoid name collisions between extensions and application objects.

**Also known as:** namespace, PostgreSQL schema

**Related:** [[postgresql#data-types-and-schema]]

**Example:**
```sql
CREATE SCHEMA audit;
CREATE TABLE audit.log (id SERIAL, action TEXT, logged_at TIMESTAMPTZ DEFAULT now());
-- Table is in the 'audit' schema, not the default 'public' schema
SELECT * FROM audit.log;
```

---

_Add more S-terms here_

---

## T

### tablespace

**Definition:** A PostgreSQL tablespace maps a logical name to a physical directory on the filesystem. Tables and indexes can be assigned to specific tablespaces, allowing you to spread data across different storage volumes — for example, placing large archival tables on slower, cheaper disks while keeping hot tables on fast SSDs.

**Also known as:** storage location, filespace

**Related:** [[postgresql#administration-and-tuning]]

**Example:**
```sql
CREATE TABLESPACE fast_ssd LOCATION '/mnt/nvme/pg_data';
CREATE TABLE hot_events (...) TABLESPACE fast_ssd;
```

---

### TOAST

**Definition:** The Oversized-Attribute Storage Technique. When a row's data exceeds roughly 2 KB, PostgreSQL automatically stores large column values (long text, bytea, JSON) in a separate TOAST table linked to the main table. This is transparent to queries but affects storage layout, I/O patterns, and VACUUM behavior. The name is an acronym and also a deliberate pun on "toast" as something that slides under the main table.

**Also known as:** out-of-line storage, TOAST table

**Related:** [[postgresql#data-types-and-schema]], [[postgresql#administration-and-tuning]]

**Example:**
A `TEXT` column storing a 50 KB JSON document will be stored in the TOAST table. The main table row contains only a pointer. `\d+ tablename` in psql will show the associated TOAST table name.

---

### transaction

**Definition:** A logical unit of work in a database that groups one or more SQL statements into an atomic operation. All statements in a transaction either all succeed (COMMIT) or all fail (ROLLBACK). In PostgreSQL, every single SQL statement runs implicitly inside a transaction — you can make it explicit with `BEGIN ... COMMIT` to group multiple statements.

**Also known as:** database transaction, TX

**Related:** [[postgresql#transactions-and-concurrency]], [[shared/glossary#algorithm]]

**Example:**
```sql
BEGIN;
  INSERT INTO orders (user_id, total) VALUES (42, 99.99);
  INSERT INTO order_items (order_id, product_id, qty) VALUES (currval('orders_id_seq'), 7, 2);
COMMIT;  -- Both inserts commit together; if either fails, neither is saved
```

---

### tuple

**Definition:** In the relational model and in PostgreSQL's internal vocabulary, a *tuple* is a single row in a relation (table). The term comes from mathematics: an ordered list of values, one per attribute. PostgreSQL's storage engine tracks multiple versions of the same logical row as separate physical tuples (the MVCC mechanism), each with transaction visibility stamps (`xmin` and `xmax`).

**Also known as:** row, record, heap tuple

**Related:** [[postgresql#introduction]]

**Example:**
The SQL `INSERT INTO users (name) VALUES ('Alice')` creates one new tuple in the `users` relation. After an `UPDATE`, the old tuple is marked dead (its `xmax` is set) and a new tuple is written — both physically exist until VACUUM removes the dead one.

---

_Add more T-terms here_

---

## U

_Add U-terms here_

---

## V

### VACUUM

**Definition:** A PostgreSQL maintenance process that reclaims storage occupied by dead tuples (rows that were deleted or updated and are no longer visible to any transaction). Without VACUUM, tables grow without bound due to MVCC's multi-version storage. PostgreSQL runs autovacuum automatically in the background, but understanding manual VACUUM is important for diagnosing bloat and table age issues.

**Also known as:** vacuuming, autovacuum

**Related:** [[postgresql#administration-and-tuning]], [[postgresql#transactions-and-concurrency]]

**Example:**
```sql
VACUUM ANALYZE orders;
-- Reclaims dead tuples in 'orders' and updates planner statistics
VACUUM FULL orders;
-- Rewrites the table compactly (acquires an ACCESS EXCLUSIVE lock — use with caution)
```

---

_Add more V-terms here_

---

## W

### WAL

**Definition:** Write-Ahead Log. PostgreSQL's durability mechanism: every change to data is first written to the WAL (a sequential log on disk) before the actual data pages are modified. On a crash, PostgreSQL can replay the WAL to recover to a consistent state. WAL is also the foundation of streaming replication: standby servers replay the primary's WAL stream to stay up to date.

**Also known as:** Write-Ahead Log, transaction log, redo log, pg_wal

**Related:** [[postgresql#replication-and-ha]], [[postgresql#administration-and-tuning]]

**Example:**
When you `COMMIT` a transaction, PostgreSQL guarantees the WAL record is flushed to disk before returning to the client. If the server crashes immediately after, the committed data is not lost because it can be recovered from the WAL on restart.

---

_Add more W-terms here_

---

## X Y Z

_Add X/Y/Z-terms here_

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
