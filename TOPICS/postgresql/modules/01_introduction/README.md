# Module 01: Introduction to PostgreSQL

[← Topic Home](../../README.md) | [Next → Module 02](../02_data-types-and-schema/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-green)
![Time](https://img.shields.io/badge/time-6--8h-orange)

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

This module introduces the relational database model and PostgreSQL from the ground up. You will learn what a relational database is and why it was invented, install PostgreSQL and navigate the `psql` command-line client, create your first database and tables, and perform the four fundamental operations on data: INSERT, SELECT, UPDATE, and DELETE.

By the end of this module you will have a working PostgreSQL installation and the skills to store and retrieve structured data. This foundation supports everything that follows — query optimization, indexing, transactions, and all the advanced features that make PostgreSQL powerful depend on the concepts introduced here.

No prior database experience is assumed. If you have worked with another SQL database before, this module will feel familiar but still contains PostgreSQL-specific details worth reading.

---

## Prerequisites

### Required Modules

- None — this is the first module.

### Required Concepts

- **Command-line basics** — You need to open a terminal, run commands, and read output. Knowing how to navigate directories with `cd` and run programs is sufficient.
- **Basic programming concepts** — An understanding of variables and data types (strings, numbers, booleans) will help when you encounter SQL data types, but is not strictly required.
- **No prior SQL knowledge needed** — SQL is introduced from first principles in this module.

> [!TIP]
> If you have never used a terminal before, spend 15–30 minutes practicing basic navigation (`cd`, `ls`, `pwd`) before continuing. Everything in this topic is driven from the command line or through `psql`.

---

## Objectives

By the end of this module, you will be able to:

1. Explain the relational model: what a relation, tuple, and attribute are, and why this model was invented
2. Install PostgreSQL on your machine (or run it via Docker) and connect to it with `psql`
3. Navigate the `psql` client: use meta-commands (`\l`, `\dt`, `\d`, `\q`) and execute SQL statements
4. Create a database and define tables using `CREATE DATABASE` and `CREATE TABLE` with appropriate data types
5. Insert, query, update, and delete rows using `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
6. Identify the most common PostgreSQL data types and choose the right one for common use cases

---

## Theory

### The Relational Model

In 1970, IBM researcher Edgar F. Codd published a paper titled "A Relational Model of Data for Large Shared Data Banks." Before Codd's work, databases were navigational: to find a customer's orders, you followed physical pointers from record to record. The structure of the query was tightly coupled to the physical storage layout. Changing how data was stored meant rewriting all the programs that accessed it.

Codd proposed a radical alternative: represent all data as **relations** — mathematical sets of tuples — and provide a declarative query language that described *what* data was wanted, not *how* to retrieve it. The storage engine would figure out the how; the programmer would only need to express the what.

A **relation** is simply a table with rows and columns. Each row (called a **tuple**) represents one instance of the entity being modeled. Each column (called an **attribute**) represents one property of that entity. Every tuple in a relation must have the same set of attributes — this is what makes a table a table and not a free-form blob.

```sql
-- A "relation" in SQL terms is just a table
-- This table has four attributes: id, title, author, year
-- Each row is a tuple representing one book

CREATE TABLE books (
    id     SERIAL PRIMARY KEY,  -- unique identifier for each tuple
    title  TEXT   NOT NULL,     -- the book's title
    author TEXT   NOT NULL,     -- the book's author
    year   INT                  -- publication year (nullable)
);
```

The key insight is **data independence**: the application asks "give me all books by Orwell" using SQL, and the database figures out how to retrieve them efficiently regardless of how they are physically stored on disk. When the database administrator adds an index to speed up author lookups, no application code needs to change.

SQL — Structured Query Language — is the standardized language for expressing these queries. It is declarative: you describe the result you want, not the steps to produce it. The same SQL query runs on PostgreSQL, MySQL, SQLite, and SQL Server with minimal modification.

### PostgreSQL vs. Other Databases

PostgreSQL is not the only SQL database. Understanding its position relative to the alternatives helps you appreciate its strengths.

**PostgreSQL vs. MySQL/MariaDB:** Both are full-featured open source relational databases. PostgreSQL is more strictly standards-compliant, has a richer type system (arrays, JSONB, ranges, custom types), and provides stronger ACID guarantees by default. MySQL has historically been faster for simple web workloads and has a larger installed base, but PostgreSQL has gained significant ground and many teams consider it the default choice today for new projects.

**PostgreSQL vs. SQLite:** SQLite is a serverless, file-based database — there is no server process; the database is a single file your application opens directly. It is ideal for embedded use cases, development, and single-user applications. PostgreSQL is a client-server database designed for multiple concurrent users, large data volumes, and production deployments. You would not use SQLite for a web application serving hundreds of concurrent users.

**PostgreSQL vs. NoSQL (MongoDB, DynamoDB, Redis):** NoSQL databases sacrifice the relational model (and often ACID guarantees) in exchange for horizontal scalability, flexible schemas, or specialized access patterns. PostgreSQL is the right choice when your data has relationships, when you need strong consistency, or when you need to ask complex ad-hoc questions. With JSONB support (Module 07), PostgreSQL can also handle document-style data well, reducing the need to adopt a separate document database.

### Installing PostgreSQL and psql

PostgreSQL runs as a background server process. You interact with it through client programs, the most important being `psql` — the interactive command-line client.

**On macOS (using Homebrew):**
```bash
brew install postgresql@16
brew services start postgresql@16
# psql is included — add it to your PATH as Homebrew suggests
```

**On Ubuntu/Debian Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
# Switch to the postgres system user to get started
sudo -u postgres psql
```

**Using Docker (platform-independent):**
```bash
# Start a PostgreSQL container with a known password
docker run --name pg-learn \
  -e POSTGRES_PASSWORD=learnsql \
  -e POSTGRES_USER=learner \
  -e POSTGRES_DB=learndb \
  -p 5432:5432 \
  -d postgres:16

# Connect to it
psql -h localhost -U learner -d learndb
# Password: learnsql
```

Once connected, you will see the `psql` prompt. The database name appears before the `#` or `>` symbol:

```
learndb=#
```

**Essential psql meta-commands:**

psql meta-commands start with a backslash and are not SQL — they are commands to the client program itself.

```sql
\l          -- list all databases on this server
\c mydb     -- connect to a different database
\dt         -- list all tables in the current database
\d tablename  -- describe a table's structure (columns, types, constraints)
\d+ tablename -- verbose describe (adds storage info, triggers)
\du         -- list all roles (users)
\q          -- quit psql
\h SELECT   -- show help for the SELECT SQL command
\timing     -- toggle timing of query execution
\x          -- toggle expanded display (useful for wide result rows)
```

### Creating Your First Database

PostgreSQL organizes data into **databases**, each of which contains **schemas**, which in turn contain **tables**. By default, every database has a `public` schema.

```sql
-- Create a new database
CREATE DATABASE bookshop;

-- Connect to it in psql
\c bookshop

-- Now create a table in the (default) public schema
CREATE TABLE books (
    id          SERIAL PRIMARY KEY,       -- auto-incrementing integer
    title       TEXT   NOT NULL,          -- required: every book has a title
    author      TEXT   NOT NULL,          -- required: every book has an author
    isbn        VARCHAR(17) UNIQUE,       -- optional, but must be unique if present
    price       NUMERIC(10, 2),           -- decimal with 2 places: up to 99999999.99
    in_stock    BOOLEAN NOT NULL DEFAULT true,  -- defaults to true if not specified
    added_at    TIMESTAMPTZ NOT NULL DEFAULT now()  -- auto-set on insert
);

-- Verify the table was created
\d books
```

`SERIAL` is shorthand for "create a sequence, set the default to the next sequence value, and make this an integer." The result is an auto-incrementing primary key — every new row automatically gets a unique, incrementing id.

`PRIMARY KEY` means: (1) the column is `NOT NULL` and (2) the values must be unique across all rows. The primary key uniquely identifies each tuple in the relation.

### Basic CRUD Operations

CRUD — Create, Read, Update, Delete — describes the four fundamental operations on data. In SQL, these are `INSERT`, `SELECT`, `UPDATE`, and `DELETE`.

**INSERT — adding rows:**

```sql
-- Insert a single book
INSERT INTO books (title, author, isbn, price)
VALUES ('The Pragmatic Programmer', 'Hunt and Thomas', '978-0135957059', 49.99);

-- Insert multiple books at once
INSERT INTO books (title, author, price) VALUES
    ('Clean Code', 'Robert C. Martin', 34.99),
    ('Designing Data-Intensive Applications', 'Martin Kleppmann', 59.99),
    ('PostgreSQL: Up and Running', 'Regina Obe & Leo Hsu', 44.99);

-- Note: we did not specify 'id' or 'added_at' — their defaults are used
```

**SELECT — querying rows:**

```sql
-- Retrieve all books
SELECT * FROM books;

-- Retrieve only specific columns
SELECT title, author, price FROM books;

-- Filter rows with WHERE
SELECT title, price
  FROM books
 WHERE price < 50.00;

-- Sort results
SELECT title, price
  FROM books
 ORDER BY price ASC;   -- ASC is default; DESC for descending

-- Combine filtering and sorting
SELECT title, author, price
  FROM books
 WHERE in_stock = true
 ORDER BY price DESC
 LIMIT 5;   -- return at most 5 rows
```

**UPDATE — modifying existing rows:**

```sql
-- Update the price of a specific book (by id)
UPDATE books
   SET price = 45.00
 WHERE id = 1;

-- Update multiple columns at once
UPDATE books
   SET price = 39.99,
       in_stock = false
 WHERE title = 'Clean Code';

-- Update all rows (no WHERE — dangerous; see Common Pitfalls)
UPDATE books SET in_stock = true;
```

**DELETE — removing rows:**

```sql
-- Delete a specific book
DELETE FROM books WHERE id = 3;

-- Delete books that match a condition
DELETE FROM books WHERE in_stock = false;

-- Delete ALL rows (no WHERE — be careful)
DELETE FROM books;
-- TRUNCATE books;  -- faster for deleting all rows; cannot be easily rolled back
```

### Data Types Overview

PostgreSQL has a rich type system. For a complete reference, see Module 02. The types you need for most beginner work are:

| Type | Description | Example |
|------|-------------|---------|
| `INTEGER` / `INT` | Whole number (4 bytes, ±2.1 billion) | `42`, `-7` |
| `BIGINT` | Large whole number (8 bytes, ±9.2 quintillion) | `9876543210` |
| `SERIAL` | Auto-incrementing integer (shorthand) | (set automatically) |
| `BIGSERIAL` | Auto-incrementing bigint | (set automatically) |
| `NUMERIC(p,s)` | Exact decimal with precision p and scale s | `99.99` |
| `REAL` / `FLOAT8` | Floating-point (approximate) | `3.14159` |
| `TEXT` | Variable-length string, unlimited | `'hello world'` |
| `VARCHAR(n)` | Variable-length string, max n chars | `'alice'` |
| `CHAR(n)` | Fixed-length string, padded to n chars | rarely used |
| `BOOLEAN` | True or false | `true`, `false` |
| `DATE` | Calendar date only | `'2024-01-15'` |
| `TIME` | Time of day only | `'14:30:00'` |
| `TIMESTAMP` | Date and time, no timezone | `'2024-01-15 14:30:00'` |
| `TIMESTAMPTZ` | Date and time, with timezone (recommended) | `'2024-01-15 14:30:00+00'` |
| `UUID` | 128-bit universally unique identifier | `'550e8400-e29b-41d4-a716-446655440000'` |

**A critical note on TEXT vs VARCHAR:** In PostgreSQL, there is essentially no performance difference between `TEXT` and `VARCHAR`. The PostgreSQL documentation explicitly states this. Use `TEXT` for strings that have no meaningful length limit. Use `VARCHAR(n)` only when you want the database to enforce a maximum length as a constraint. Never use `CHAR(n)` unless you specifically need fixed-length, space-padded storage (rare).

**Always use TIMESTAMPTZ, not TIMESTAMP.** Storing timestamps without timezone information is a common source of bugs in applications that span timezones or migrate between servers. `TIMESTAMPTZ` stores the value in UTC internally and converts to the session's timezone for display. `TIMESTAMP` stores the literal value with no timezone information — what you put in is what you get out, which causes silent bugs when your application moves to a different timezone.

---

## Key Concepts

**Relation:** The formal term for a table in the relational model. A relation is a set of tuples (rows), all of which have the same attributes (columns). The term comes from set theory. In practice, "relation" and "table" are used interchangeably, but understanding the mathematical term helps clarify why SQL queries produce predictable results. See also: [[shared/glossary#algorithm]] for general CS vocabulary.

**Tuple:** A single row in a table. In the mathematical sense, a tuple is an ordered list of values, one per attribute. PostgreSQL internally tracks multiple versions of the same logical tuple (for MVCC), making the physical storage more complex than a simple list of rows.

**Attribute:** A column in a table. Each attribute has a name and a data type that constrains the values that can be stored in it. Every tuple in a relation must have a value for every attribute (though the value can be `NULL` if the attribute is nullable).

**Primary Key:** An attribute or combination of attributes whose values uniquely identify every tuple in a relation. No two rows can have the same primary key value, and primary key values cannot be NULL. In PostgreSQL, `PRIMARY KEY` is a constraint — it combines `UNIQUE` and `NOT NULL`.

**NULL:** A special marker meaning "value unknown" or "value not applicable." NULL is not zero, not an empty string, and not false. Comparisons with NULL always produce NULL (not true or false), which means `WHERE column = NULL` never matches anything — you must use `WHERE column IS NULL`.

**DDL vs. DML:** Data Definition Language (DDL) includes statements that create or modify the structure of the database: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`. Data Manipulation Language (DML) includes statements that manipulate data within tables: `INSERT`, `SELECT`, `UPDATE`, `DELETE`. Understanding this distinction is important when thinking about transactions.

**psql:** PostgreSQL's interactive terminal client. It can execute SQL statements and meta-commands (starting with `\`). Meta-commands are processed by psql itself and never sent to the server; SQL statements are sent to the PostgreSQL server for execution.

---

## Examples

### Example 1: Creating a Books Catalog Table

**Scenario:** You are building a bookshop inventory system. You need a table to track books, their authors, prices, and whether they are in stock.

**Goal:** Design and create a `books` table, then verify its structure.

```sql
-- Create the database (do this once)
CREATE DATABASE bookshop;

-- Connect to it
-- \c bookshop

-- Create the books table with appropriate types and constraints
CREATE TABLE books (
    id          SERIAL      PRIMARY KEY,                -- auto-increment PK
    title       TEXT        NOT NULL,                   -- required; no max length
    author      TEXT        NOT NULL,                   -- required
    isbn        VARCHAR(17) UNIQUE,                     -- optional; must be unique
    price       NUMERIC(10, 2) NOT NULL CHECK (price >= 0),  -- non-negative price
    in_stock    BOOLEAN     NOT NULL DEFAULT true,      -- defaults to available
    category    TEXT,                                   -- optional category
    added_at    TIMESTAMPTZ NOT NULL DEFAULT now()      -- auto-set timestamp
);

-- Verify the structure in psql
-- \d books
```

**What to notice:** The `CHECK (price >= 0)` constraint prevents negative prices from being stored — the database enforces this rule, not the application. `DEFAULT true` and `DEFAULT now()` mean we can omit those columns in INSERT statements and they will be set automatically.

---

### Example 2: Inserting and Querying Data

**Scenario:** Add books to the catalog and run queries to find specific ones.

**Goal:** Practice `INSERT` with partial column lists, and `SELECT` with filtering and sorting.

```sql
-- Insert books (note: no id or added_at — defaults handle those)
INSERT INTO books (title, author, isbn, price, category) VALUES
    ('The Pragmatic Programmer', 'Hunt and Thomas', '978-0135957059', 49.99, 'Software Engineering'),
    ('Clean Code', 'Robert C. Martin', '978-0132350884', 34.99, 'Software Engineering'),
    ('Designing Data-Intensive Applications', 'Martin Kleppmann', '978-1449373320', 59.99, 'Databases'),
    ('PostgreSQL: Up and Running', 'Regina Obe', '978-1491963418', 44.99, 'Databases'),
    ('The Algorithm Design Manual', 'Steven Skiena', '978-3030542566', 54.99, 'Algorithms');

-- Query 1: All books under $50, sorted cheapest first
SELECT title, author, price
  FROM books
 WHERE price < 50.00
 ORDER BY price ASC;

-- Query 2: All database books
SELECT title, price
  FROM books
 WHERE category = 'Databases';

-- Query 3: Count books per category
SELECT category, COUNT(*) AS book_count, AVG(price)::NUMERIC(10,2) AS avg_price
  FROM books
 GROUP BY category
 ORDER BY book_count DESC;
```

**Expected output for Query 1:**
```
              title              |      author       | price
---------------------------------+-------------------+-------
 Clean Code                      | Robert C. Martin  | 34.99
 PostgreSQL: Up and Running      | Regina Obe        | 44.99
 The Pragmatic Programmer        | Hunt and Thomas   | 49.99
```

**What to notice:** `COUNT(*)` counts rows; `AVG()` computes the average. `GROUP BY category` divides rows into groups by category before aggregating. The `::NUMERIC(10,2)` is a type cast that rounds the average to two decimal places.

---

### Example 3: Updating and Deleting Data

**Scenario:** Update the price of a book after a sale, then remove a discontinued book.

**Goal:** Practice targeted `UPDATE` and `DELETE` using `WHERE`, and use `RETURNING` to see what changed.

```sql
-- Update the price of a specific book and return the new values
UPDATE books
   SET price = 42.99
 WHERE title = 'Clean Code'
RETURNING id, title, price;

-- Mark a book as out of stock
UPDATE books
   SET in_stock = false
 WHERE isbn = '978-0135957059';

-- Verify the change
SELECT title, price, in_stock
  FROM books
 WHERE isbn = '978-0135957059';

-- Delete a book that is no longer sold
DELETE FROM books
 WHERE title = 'The Algorithm Design Manual'
RETURNING title;  -- confirm what was deleted

-- Verify deletion
SELECT COUNT(*) FROM books;  -- should be 4
```

**What to notice:** `RETURNING` is a PostgreSQL extension to the SQL standard that makes `UPDATE` and `DELETE` return the affected rows. This is extremely useful for confirming which rows were changed and for retrieving auto-generated values (like `id` after an `INSERT`). We will use it extensively in Module 06.

---

## Common Pitfalls

### Pitfall 1: UPDATE or DELETE Without a WHERE Clause

The most dangerous mistake for beginners (and experienced developers who are moving too fast) is running an `UPDATE` or `DELETE` without a `WHERE` clause.

**Wrong:**
```sql
-- This updates EVERY book's price to 9.99 — not just the one you wanted
UPDATE books SET price = 9.99;

-- This deletes EVERY book — not just the out-of-stock ones
DELETE FROM books;
```

**Right:**
```sql
-- Always include WHERE to target specific rows
UPDATE books SET price = 9.99 WHERE id = 3;
DELETE FROM books WHERE in_stock = false;
```

**Why this happens:** In SQL, if you omit `WHERE`, the statement applies to all rows. There is no prompt, no warning, and no undo (unless you are inside a transaction — see Module 05). The habit to build: always write the `WHERE` clause before filling in the rest of the statement.

A safe practice in psql: type `BEGIN;` before any destructive operation, check what would be affected with a `SELECT` using the same `WHERE` clause, then either `COMMIT` or `ROLLBACK`.

---

### Pitfall 2: Comparing with NULL Using = Instead of IS NULL

NULL behaves differently from every other value in SQL. Comparisons involving NULL always return NULL (not true or false), which means WHERE conditions using `= NULL` silently match nothing.

**Wrong:**
```sql
-- This returns zero rows, even if there are books with no isbn
SELECT * FROM books WHERE isbn = NULL;

-- This also returns zero rows
SELECT * FROM books WHERE isbn != NULL;
```

**Right:**
```sql
-- Use IS NULL to find rows where isbn has no value
SELECT * FROM books WHERE isbn IS NULL;

-- Use IS NOT NULL to find rows where isbn has a value
SELECT * FROM books WHERE isbn IS NOT NULL;
```

**Why this happens:** NULL means "value unknown." If we ask "is unknown equal to NULL?", the answer is "unknown" — not true, not false. SQL propagates this uncertainty. The special operators `IS NULL` and `IS NOT NULL` are the only way to test for the absence of a value.

---

### Pitfall 3: Using TIMESTAMP Instead of TIMESTAMPTZ

PostgreSQL has two timestamp types: `TIMESTAMP` (without timezone) and `TIMESTAMPTZ` (with timezone). They look similar but behave very differently.

**Wrong:**
```sql
-- Stores the literal timestamp with no timezone info
CREATE TABLE events (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    happens_at  TIMESTAMP NOT NULL  -- danger: no timezone context
);
INSERT INTO events (name, happens_at) VALUES ('Conference', '2024-06-15 09:00:00');
-- If your server is in UTC but your users are in New York (UTC-5),
-- this 9:00 AM means different things depending on who reads it
```

**Right:**
```sql
-- Stores UTC internally; displays in session timezone
CREATE TABLE events (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    happens_at  TIMESTAMPTZ NOT NULL  -- always correct
);
INSERT INTO events (name, happens_at) VALUES ('Conference', '2024-06-15 09:00:00-04');
-- Now PostgreSQL stores this as 13:00:00 UTC and displays correctly in any timezone
```

**Why this happens:** Most beginners don't think about timezones until they cause a bug — usually when the application is deployed to a server in a different timezone than the developer's laptop, or when users in different regions start reporting time discrepancies. Always use `TIMESTAMPTZ` to avoid the problem entirely.

---

### Pitfall 4: Thinking SELECT * Is Always Fine

`SELECT *` is convenient for exploration but is a bad practice in application code.

**Wrong (in production code):**
```sql
-- Fragile: if someone adds a column to books, this query's result set changes
SELECT * FROM books;
```

**Right:**
```sql
-- Explicit: the columns you get back are predictable regardless of schema changes
SELECT id, title, author, price, in_stock FROM books;
```

**Why this matters:** When you add a column to a table, `SELECT *` queries suddenly return that column too. If your application maps query results to structs or objects by position, a schema change silently breaks everything. Explicit column lists also communicate intent: the reader of the query knows exactly what data is needed.

---

## Cross-Links

- [[django-fastapi-flask]] — Django's ORM and SQLAlchemy generate SQL that runs on PostgreSQL; understanding the SQL they produce (via `EXPLAIN`) helps debug performance issues
- [[async-python]] — asyncpg and psycopg3 are async Python libraries for PostgreSQL; the SQL you write here is exactly what they execute
- [[systems-architecture]] — Database design decisions (table structure, relationships, constraints) are fundamental to overall system architecture

---

## Summary

- The **relational model** (Codd, 1970) represents data as tables of rows and columns. SQL is the declarative language for querying relational data: you describe *what* you want, not *how* to retrieve it.

- **PostgreSQL** originated from the POSTGRES research project at UC Berkeley (1986) and became an open source project in 1996. It is the most feature-rich open source relational database, with strict standards compliance and a powerful extensibility system.

- **psql** is the primary interactive client. Meta-commands (`\l`, `\dt`, `\d tablename`, `\q`) manage navigation; SQL statements manipulate data. Both types of input are entered at the same prompt.

- **`CREATE TABLE`** defines a relation's schema — its attributes and their data types. **`PRIMARY KEY`** uniquely identifies each tuple. **`NOT NULL`** prevents missing values. **`DEFAULT`** sets values automatically on insert.

- The four DML operations are: **INSERT** (add tuples), **SELECT** (read tuples), **UPDATE** (modify tuples), **DELETE** (remove tuples). Every `UPDATE` and `DELETE` should include a `WHERE` clause.

- PostgreSQL's most important data type guidelines for beginners: use `TEXT` (not `VARCHAR`) for strings without a meaningful length limit; use `TIMESTAMPTZ` (not `TIMESTAMP`) for all date-time values; use `BIGSERIAL` or `BIGINT GENERATED ALWAYS AS IDENTITY` for primary keys in large tables.

- **NULL** is not zero, not empty string, not false — it means "unknown." Test for NULL with `IS NULL` and `IS NOT NULL`, never with `=` or `!=`.

- **`RETURNING`** in `INSERT`, `UPDATE`, and `DELETE` is a PostgreSQL-specific clause that returns the affected rows — useful for retrieving auto-generated IDs and confirming changes.
