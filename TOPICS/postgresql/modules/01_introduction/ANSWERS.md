# Answer Key — Module 01: Introduction to PostgreSQL

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Copied text without understanding (you'll know)
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — NULL Definition [1 pt]

**Full credit answer:**
NULL is a special marker that means "value unknown" or "value not applicable" — it is the absence of any value. It is not zero (which is a known numeric value), not an empty string (which is a known string with zero length), and not false (which is a known boolean). NULL represents the fact that no value is known or applicable for that attribute in that tuple.

**Key points required:**
- NULL means "unknown" or "not applicable" — not a value itself
- Different from 0, empty string, and false

**Common wrong answers:**
- *"NULL means empty"* — Empty string `''` and NULL are different; `''` is a known value (an empty string), NULL is the absence of any value
- *"NULL is like false"* — Comparisons involving NULL return NULL, not false; this is a fundamental distinction

---

### 1.2 — TIMESTAMP vs TIMESTAMPTZ [1 pt]

**Full credit answer:**
`TIMESTAMP` (without time zone) stores a date and time value with no timezone context — it is just a calendar date and clock time. `TIMESTAMPTZ` (timestamp with time zone) stores the value in UTC internally and converts it to the session's local timezone for display. You should generally use `TIMESTAMPTZ` because it correctly handles applications that span timezones and prevents silent bugs when moving between environments with different timezone settings.

**Key points required:**
- TIMESTAMPTZ stores in UTC, TIMESTAMP stores literally with no timezone
- TIMESTAMPTZ is the recommended type for production use

---

### 1.3 — psql Meta-Commands [1 pt]

**Full credit answer (any 3 of the following):**
- `\l` — list all databases on the server
- `\c dbname` — connect to a specific database
- `\dt` — list all tables in the current schema
- `\d tablename` — describe a table's structure (columns, types, constraints)
- `\du` — list all roles/users
- `\q` — quit psql
- `\h COMMAND` — show help for a SQL command
- `\timing` — toggle query execution time display
- `\x` — toggle expanded display mode

**Partial credit:** 0.5 pts if only 1–2 commands are correctly named and described.

---

### 1.4 — SERIAL [1 pt]

**Full credit answer:**
`SERIAL` in a `CREATE TABLE` statement is shorthand that automatically does two things: (1) creates a database sequence (a counter object), and (2) sets the column's `DEFAULT` to the next value of that sequence. The result is that every new row gets an automatically incrementing integer value if you don't specify one explicitly.

**Key points required:**
- Creates a sequence
- Sets DEFAULT to the next sequence value

**Common wrong answers:**
- *"SERIAL makes the column unique"* — SERIAL does not imply UNIQUE; using it as a PRIMARY KEY adds the UNIQUE constraint, but SERIAL by itself does not
- *"SERIAL is a data type"* — Technically SERIAL is a shorthand notation that creates an INTEGER column with a sequence default, not a true data type

---

### 1.5 — DDL vs DML [1 pt]

**Full credit answer:**
DDL (Data Definition Language) is SQL statements that create, modify, or delete the structure of the database itself — tables, indexes, schemas, constraints. Example: `CREATE TABLE users (...)`. DML (Data Manipulation Language) is SQL statements that manipulate the data within tables. Example: `INSERT INTO users (email) VALUES ('a@b.com')`. Other DML examples: `SELECT`, `UPDATE`, `DELETE`.

**Key points required:**
- DDL changes structure; DML changes data
- Correct example for each

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Declarative vs Imperative SQL [2 pts]

**Full credit answer:**
SQL is declarative because you describe *what* result you want, not *how* to compute it. For example, `SELECT * FROM orders WHERE user_id = 42` says "give me all orders for user 42" — the database's query planner decides how to retrieve them (which index to use, how to scan the table, etc.). An imperative approach would require you to write step-by-step instructions: loop through rows, check each one, collect matches. The declarative approach matters because it allows the database to optimize the plan independently of the code — when you add an index, existing queries automatically improve without code changes.

**Rubric:**
- 2 pts: Correctly explains declarative (what, not how) AND identifies that the query planner handles the how AND explains why this is beneficial (data independence / optimization)
- 1 pt: Correctly explains declarative vs imperative but doesn't mention the practical benefit
- 0 pts: Cannot distinguish the concepts meaningfully

**Teaching note:**
The most common confusion here is students saying SQL is declarative "because it's simpler" — the real reason is the separation of concern between what data is needed and how to retrieve it efficiently.

---

### 2.2 — NULL Comparison Misconception [2 pts]

**Full credit answer:**
No, `WHERE email = NULL` is incorrect and will never return any rows. NULL comparisons always return NULL, not true or false — because NULL means "unknown," asking "is unknown equal to NULL?" produces "unknown," which is treated as false in a WHERE condition. The correct way to find rows with no email is `WHERE email IS NULL`. The misconception arises because NULL looks syntactically similar to other values, so programmers instinctively treat `= NULL` like `= ''` or `= 0`.

**The misconception is:** Using `= NULL` to test for NULL values
**Why it's wrong:** Comparisons with NULL always evaluate to NULL (unknown), never to true
**Why the misconception arises:** NULL looks like a value, so programmers apply normal value-equality syntax to it

**Rubric:**
- 2 pts: Correctly identifies the misconception, gives the right syntax (IS NULL), AND explains why comparisons with NULL return NULL
- 1 pt: Gives the right answer (IS NULL) but doesn't explain the underlying mechanism
- 0.5 pts: Identifies the misconception as wrong but can't correct it
- 0 pts: Agrees with the misconception

---

### 2.3 — TEXT vs VARCHAR [2 pts]

**Full credit answer:**
In PostgreSQL, `TEXT` and `VARCHAR(n)` store variable-length strings, and there is effectively no performance difference between them — they use the same underlying storage mechanism. The practical difference is that `VARCHAR(n)` enforces a maximum length (n characters) as a constraint, while `TEXT` has no length limit. You should use `TEXT` for most string columns where no meaningful length limit exists (names, descriptions, URLs). Use `VARCHAR(n)` only when you specifically want the database to enforce a maximum length as a data integrity rule.

**Key tradeoffs:**
| Dimension | TEXT | VARCHAR(n) |
|-----------|------|------------|
| Max length | Unlimited | n characters |
| Performance | Same | Same |
| When to use | No meaningful length limit | When max length is a business rule |

**Rubric:**
- 2 pts: States no performance difference AND explains when to choose each (TEXT for no limit, VARCHAR(n) when max length matters as a constraint)
- 1 pt: Mentions no performance difference but treats VARCHAR as universally preferred or doesn't give guidance on when to use each
- 0 pts: Claims TEXT and VARCHAR have different performance or cannot distinguish them

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — students Table [3 pts]

**Full credit answer:**
```sql
CREATE TABLE students (
    id              BIGSERIAL    PRIMARY KEY,
    first_name      TEXT         NOT NULL,
    last_name       TEXT         NOT NULL,
    email           TEXT         NOT NULL UNIQUE,
    enrollment_date DATE         NOT NULL DEFAULT CURRENT_DATE,
    gpa             NUMERIC(3,2) CHECK (gpa >= 0.0 AND gpa <= 4.0),
    is_active       BOOLEAN      NOT NULL DEFAULT true
);
```

**Step-by-step reasoning:**
1. `BIGSERIAL PRIMARY KEY` for the 64-bit auto-incrementing ID
2. `TEXT NOT NULL` for first and last name — no meaningful length limit
3. `TEXT NOT NULL UNIQUE` for email — required and must be unique
4. `DATE NOT NULL DEFAULT CURRENT_DATE` for enrollment date (DATE only, not TIMESTAMPTZ)
5. `NUMERIC(3,2)` for GPA — 3 total digits, 2 after decimal (allows 0.00 to 9.99; the CHECK restricts to 0.00–4.00); nullable by not specifying NOT NULL
6. `BOOLEAN NOT NULL DEFAULT true` for active status

**Rubric:**
- 3 pts: All 6 columns correct with appropriate types and constraints; BIGSERIAL PK; GPA is nullable with correct CHECK
- 2 pts: Most correct but one significant error (e.g., using INT for PK instead of BIGSERIAL, forgetting NOT NULL on name/email, missing CHECK on GPA)
- 1 pt: Correct general structure but multiple errors (wrong types, missing constraints)
- 0 pts: Fundamentally incorrect CREATE TABLE syntax

**Acceptable alternatives:**
- `BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY` instead of BIGSERIAL
- `SERIAL PRIMARY KEY` instead of BIGSERIAL (acceptable; BIGSERIAL is better practice)

---

### 3.2 — Products CRUD [3 pts]

**Full credit answer:**

**(a) Insert:**
```sql
INSERT INTO products (name, category, price, in_stock)
VALUES ('Mechanical Keyboard', 'Electronics', 129.99, true);
```

**(b) 10% price increase for Electronics:**
```sql
UPDATE products
   SET price = price * 1.10
 WHERE category = 'Electronics';
```

**(c) Delete not-in-stock items under $5:**
```sql
DELETE FROM products
 WHERE in_stock = false
   AND price < 5.00;
```

**Rubric:**
- 1 pt per part (a), (b), (c) — full credit for each if correct
- 0.5 pt for each part if the logic is right but syntax is imperfect
- Note: `price * 1.10` is equivalent to `price + price * 0.10`; both are acceptable

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Accidental DELETE Bug [3 pts] (1 pt each part)

**(a) What did the query do?**
`DELETE FROM users;` with no WHERE clause deleted every single row in the `users` table — it wiped out all user records.

**(b) Why did this happen?**
In SQL, if you omit the WHERE clause from a DELETE statement, it applies to all rows in the table. There is no warning or confirmation prompt. The SQL standard treats an absent WHERE clause as "all rows match" — which makes sense logically (a WHERE clause with no condition would match everything) but is dangerous in practice.

**(c) How to prevent this:**
Multiple valid answers:
- Use transactions: always run destructive queries inside `BEGIN ... COMMIT`, with a `SELECT` using the same WHERE clause first to verify which rows would be affected before committing
- Use `\set` in psql to require confirmation before destructive queries
- In application code, use an ORM that requires explicit confirmation for bulk deletes
- Code review requiring a second pair of eyes on any DELETE without WHERE
- Database role that does not have DELETE permission in production; deploys go through a migration with oversight

**Rubric:**
- 1 pt for (a): correctly states all rows were deleted
- 1 pt for (b): correctly explains the SQL rule (no WHERE = all rows)
- 1 pt for (c): gives a practical prevention strategy; multiple valid answers

---

## Section 5: Discussion — Answer Key

### 5.1 — Codd's Relational Model [2 pts]

**Example strong answer:**
Before the relational model, databases were navigational — programs had to follow explicit pointers between records, and the query logic was tightly coupled to the physical storage layout. If you changed how data was stored, every program that accessed it had to be rewritten. Codd's insight was to separate the logical structure of data (tables, rows, columns) from its physical representation, and to provide a declarative query language (SQL) that let programmers express *what* they wanted without specifying *how* to retrieve it. For a programmer, this meant writing `SELECT * FROM orders WHERE user_id = 42` instead of writing a loop that follows pointers. For an administrator, it meant that indexes could be added or removed to improve performance without touching application code. PostgreSQL embodies this by having a sophisticated query planner that chooses physical execution strategies automatically — when you add an index, existing queries improve without code changes.

**Elements that earn full credit:**
- Identifies the problem with navigational databases (physical-logical coupling)
- Explains Codd's solution (logical/physical separation + declarative language)
- Connects to PostgreSQL's query planner or data independence

**Rubric:**
- 2 pts: Identifies the historical problem, explains Codd's solution (or declarative/data independence), and connects to modern PostgreSQL
- 1 pt: Shows partial understanding; only covers one perspective or makes a general claim without substance
- 0 pts: Off-topic, circular, or shows fundamental misunderstanding of what the relational model is

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — RETURNING Clause [+5 pts]

**Full credit answer:**

**(a) Get ID after INSERT:**
```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
RETURNING id;
-- Returns: the auto-generated id value
```

**(b) Confirm values after UPDATE:**
```sql
UPDATE products
   SET price = price * 0.9
 WHERE category = 'Books'
RETURNING id, name, price;
-- Returns: all updated rows with their new prices
```

**Practical problem solved:** Without RETURNING, getting the auto-generated `id` after an INSERT requires a second query (usually `SELECT currval('table_id_seq')` or `SELECT lastval()`), which is a second round-trip to the database server and introduces a potential race condition in concurrent environments. RETURNING makes it atomic — you get the ID in the same response as the INSERT, with no race condition possible.

**Rubric:**
- 5 pts: Both examples are correct AND the explanation identifies the round-trip elimination and atomic nature of RETURNING
- 3 pts: Both examples correct but explanation is thin (just says "fewer queries" without explaining why the second query approach is problematic)
- 1 pt: One correct example, incomplete explanation
- 0 pts: Incorrect

**Bonus teaching note:**
RETURNING is a PostgreSQL-specific extension not in the SQL standard (though similar functionality exists in SQL Server via OUTPUT and Oracle via RETURNING INTO). Its practical importance in web application development is significant: generating a new record and immediately needing its ID is one of the most common database operations in CRUD applications.

---

## Common Wrong Answers Across the Test

These are patterns seen frequently when students haven't fully internalized the material:

1. **Confusing TIMESTAMP with TIMESTAMPTZ** — Students who default to `TIMESTAMP` have usually not experienced a timezone bug yet. Emphasize: always use `TIMESTAMPTZ`; it has zero downside. See Section 1.2.
2. **Using `= NULL` instead of `IS NULL`** — Almost universal among beginners. The key is understanding that NULL is not a value; it's the absence of one. Comparisons with NULL produce NULL, not true/false. See Section 2.2.
3. **Making UPDATE/DELETE without WHERE "safe" by mentioning rollback** — Students will suggest "just use transactions." While true, the safer habit is: write the WHERE clause first, always. Transactions are a safety net, not a substitute for careful WHERE clauses. See Section 4.1.

---

## Teaching Notes

- Students who struggle with Section 2 (conceptual) likely read without testing their understanding. Recommend re-studying with the Feynman technique: close the notes and explain each concept aloud.
- Students who struggle with Section 3 (applied) need more hands-on SQL practice. Send back to EXERCISES.md — especially Exercise 5.
- The bonus question tests understanding of RETURNING's atomic nature — don't be concerned if students skip it or only get partial credit. It's a subtle point.
- A score below 60% generally indicates the student needs to actually install PostgreSQL and run the examples rather than just reading. Database concepts solidify dramatically with hands-on practice.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
