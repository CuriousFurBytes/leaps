# Answer Key — Module 14: Databases and Persistence

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with notes and references closed.
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

### 1.1 — sql.DB is a connection pool [1 pt]

**Full credit answer:**
`sql.DB` is **not** a single connection — it is a **managed connection pool**. It creates and reuses multiple database connections automatically. Because it is a pool, it is safe for concurrent use by multiple goroutines simultaneously — each concurrent caller gets its own connection from the pool. The practical implication: create one `sql.DB` at startup and share it across all handlers; never create a new `sql.DB` per request.

**Key points required:**
- `sql.DB` is a pool, not a single connection
- Safe for concurrent use (multiple goroutines can call it simultaneously)
- Should be long-lived (created once, shared throughout the application)

**Common wrong answers:**
- *"sql.DB is a connection that you should create per request"* — This is the most dangerous misconception; creating per-request pools leaks connections and degrades performance dramatically.
- *"sql.DB wraps a single connection but handles concurrency with a mutex"* — Incorrect; the pool can hold and use many connections concurrently.

---

### 1.2 — sql.Open is lazy [1 pt]

**Full credit answer:**
No. `sql.Open` is lazy — it validates the driver name and DSN format but does **not** open an actual network connection to the database. It can succeed even if the database server is down or the DSN is wrong in a way that only manifests at connection time. To actually verify connectivity, call `db.PingContext(ctx)` (or `db.Ping()`). `PingContext` opens a real connection and returns an error if the database is unreachable.

**Key points required:**
- `sql.Open` does NOT connect; it is lazy
- `PingContext` is the real connectivity check
- A successful `sql.Open` does not guarantee the DB is reachable

**Common wrong answers:**
- *"sql.Open connects to the database"* — This is the most common misconception; always follow up with PingContext in startup code.

---

### 1.3 — Four steps of rows iteration [1 pt]

**Full credit answer:**
1. Check the error returned by `QueryContext` — if `err != nil`, return immediately
2. `defer rows.Close()` — placed immediately after the error check (not at the end of the function)
3. `rows.Next()` loop with `rows.Scan(...)` inside to read each row
4. `rows.Err()` check after the loop — returns any error that stopped iteration mid-stream

If you skip step 4, you silently return a partial result set when the database connection drops or the context is cancelled during iteration. `rows.Next()` returns `false` on both exhaustion and error; without `rows.Err()`, you cannot tell which case occurred.

**Key points required:**
- All four steps in order
- Consequence of skipping `rows.Err()`: silent data truncation

---

### 1.4 — Placeholder syntax [1 pt]

**Full credit answer:**
SQLite (both `modernc.org/sqlite` and `mattn/go-sqlite3`) and MySQL (`go-sql-driver/mysql`) use positional `?` placeholders: `WHERE id = ?`. PostgreSQL drivers (`lib/pq`, `pgx/v5/stdlib`) use numbered `$N` placeholders: `WHERE id = $1 AND email = $2`.

This matters because using the wrong placeholder for your driver will produce a runtime error (the query fails with a syntax error or the driver cannot parse the placeholders). Placeholders must match the driver — the `database/sql` package itself is driver-neutral and does not translate between styles.

**Key points required:**
- `?` for SQLite and MySQL
- `$1`, `$2`, … for PostgreSQL
- Wrong placeholder = runtime error (driver-specific)

---

### 1.5 — Sentinel errors [1 pt]

**Full credit answer:**
- **`sql.ErrNoRows`** — returned by `QueryRowContext(...).Scan(...)` when the query matched zero rows. This is a normal condition (not a program bug), so it must be checked with `errors.Is(err, sql.ErrNoRows)` to handle "not found" vs. actual errors.
- **`sql.ErrTxDone`** — returned when you call a method on a transaction (`tx.Commit()`, `tx.Exec()`, etc.) after the transaction has already been committed or rolled back. This indicates a programming error (using a transaction that is already closed).

**Key points required:**
- `sql.ErrNoRows` — zero rows from a `QueryRow` scan
- (Partial credit if they name `sql.ErrNoRows` correctly with its meaning and miss `sql.ErrTxDone`)

**Teaching note:**
`sql.ErrNoRows` is the more important of the two — it appears constantly in real code. `sql.ErrTxDone` is encountered less frequently. Award full credit if `sql.ErrNoRows` is correctly described even if the second sentinel is missed or confused.

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — defer tx.Rollback() safety pattern [2 pts]

**Full credit answer:**
`defer tx.Rollback()` is placed immediately after the `err != nil` check on `db.BeginTx(ctx, ...)` — before any other work inside the transaction — to guarantee the transaction is always rolled back if something goes wrong.

**Success path:** The function calls `tx.ExecContext` for each step, then calls `tx.Commit()`. After `Commit` returns nil (success), the transaction is finalized and closed by the database. When the function returns, the deferred `tx.Rollback()` executes — but it is a **no-op** because the transaction is already done. The database driver's `Rollback` implementation silently ignores calls on an already-closed transaction.

**Error path:** If any `tx.ExecContext` call returns an error, the function returns early. The deferred `tx.Rollback()` then fires and sends a rollback to the database, undoing all changes made so far in the transaction. Even if the function panics, deferred calls execute — the rollback still fires.

The pattern works because calling `Rollback` after `Commit` is explicitly defined to be a no-op by `database/sql`.

**Rubric:**
- 2 pts: Explains both paths (success: Rollback is no-op; error: Rollback fires) with correct reasoning
- 1 pt: Correctly identifies the pattern but only explains one path (typically only the error path)
- 0 pts: Incorrect understanding (e.g., claims you should check if Commit succeeded before deferring Rollback)

---

### 2.2 — NULL scanning into string — misconception [2 pts]

**Full credit answer:**
No, this is incorrect. Scanning a SQL `NULL` value into a Go `string` variable does not produce an empty string — it causes a **runtime error** (a scan conversion error from `database/sql`). The empty-string check would never be reached because `rows.Scan` returns an error before populating the variable.

The correct approaches are:
1. Use `sql.NullString`: a struct with `String string` and `Valid bool` fields. `Valid` is `false` when the column was NULL.
2. Use `*string` (pointer): the driver sets the pointer to `nil` when the column is NULL and allocates a new string otherwise.

An empty string and a NULL are semantically different — a user with `bio = ""` has explicitly set their bio to empty, while `bio = NULL` means the bio was never provided. Using an empty string check would lose this distinction even if the scan didn't fail.

**Rubric:**
- 2 pts: Correctly identifies that the scan fails at runtime (not just "wrong value"), explains the correct approach (NullString or pointer), and mentions the semantic distinction between NULL and empty string
- 1 pt: Correctly identifies the approach is wrong and gives one correct fix, but doesn't explain the runtime error or the NULL vs empty string distinction
- 0 pts: Agrees that the approach works (it doesn't)

---

### 2.3 — Repository pattern and testability [2 pts]

**Full credit answer:**
The repository pattern uses a **storage interface** (e.g., `UserStore`) to decouple how domain objects are retrieved and stored from what the application does with them.

- The **interface** (`UserStore`) defines the contract: a set of method signatures. Handlers depend on this interface, not on any concrete type. The interface is defined in terms of domain concepts (`GetUser`, `CreateUser`) — not database concepts.
- The **SQL implementation** (`SQLUserStore`) satisfies the interface by wrapping `database/sql` operations. It is the real production implementation.
- The **fake implementation** (`FakeUserStore`) also satisfies the interface using an in-memory map. It has no database dependency.

Because handlers accept `UserStore` (the interface), not `*SQLUserStore` (the concrete type), tests can pass a `FakeUserStore` at construction time: `srv := &server{store: NewFakeUserStore()}`. Tests exercise the handler's logic — JSON parsing, error mapping, status codes — without opening a database, running SQL, or managing schema. Test speed improves from seconds to microseconds.

The Go mechanism that makes this work is structural typing from [[go/6. Methods and Interfaces]]: any type with the right method signatures satisfies the interface without explicitly declaring it.

**Rubric:**
- 2 pts: Explains all three components (interface, SQL impl, fake impl), explicitly states that handlers depend on the interface (not the concrete type), and explains how this enables database-free testing
- 1 pt: Understands the pattern at a high level but doesn't clearly connect "handler depends on interface" to "swap the implementation in tests"
- 0 pts: Describes the pattern as an ORM or as a design pattern unrelated to testing

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — getUsersByDomain [3 pts]

**Full credit answer:**
```go
func getUsersByDomain(ctx context.Context, db *sql.DB, domain string) ([]string, error) {
    rows, err := db.QueryContext(ctx,
        `SELECT email FROM users WHERE email LIKE ?`, "%@"+domain,
    )
    if err != nil {
        return nil, fmt.Errorf("query users by domain %s: %w", domain, err)
    }
    defer rows.Close() // Step 2: immediately after error check

    var emails []string
    for rows.Next() { // Step 3: iterate and scan
        var email string
        if err := rows.Scan(&email); err != nil {
            return nil, fmt.Errorf("scan email: %w", err)
        }
        emails = append(emails, email)
    }
    if err := rows.Err(); err != nil { // Step 4: check iteration error
        return nil, fmt.Errorf("rows iteration: %w", err)
    }
    return emails, nil
}
```

**Step-by-step reasoning:**
1. The LIKE pattern `"%@" + domain` matches emails ending in `@domain` — the `%` is a SQL wildcard, not a Go format verb. Passed as a bind parameter, not interpolated.
2. `defer rows.Close()` is placed after the `err != nil` check — not at the end of the function.
3. Scan into a single `string` per row.
4. `rows.Err()` must be checked after the loop.

**Rubric:**
- 3 pts: All four steps present; parameterized query with correct LIKE pattern; errors wrapped with `%w`; compiles correctly
- 2 pts: Correct logic but missing `rows.Err()` check, or `defer rows.Close()` in wrong position
- 1 pt: Correct query but uses string concatenation for the LIKE pattern (injection risk) or missing two or more steps
- 0 pts: Incorrect query or does not use `QueryContext` at all

**Common wrong answers:**
- Concatenating the domain directly into the SQL string: `"WHERE email LIKE '%" + domain + "'"` — SQL injection vulnerability
- Missing `rows.Err()` — the most commonly omitted step; partial credit (2 pts) if everything else is correct

---

### 3.2 — createUserWithProfile transaction [3 pts]

**Full credit answer:**
```go
func createUserWithProfile(ctx context.Context, db *sql.DB, name, email, bio string) (int64, error) {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return 0, fmt.Errorf("begin tx: %w", err)
    }
    defer tx.Rollback() // fires on all non-Commit exits

    // Insert user, get new ID
    res, err := tx.ExecContext(ctx,
        `INSERT INTO users (name, email) VALUES (?, ?)`, name, email,
    )
    if err != nil {
        return 0, fmt.Errorf("insert user: %w", err)
    }
    userID, err := res.LastInsertId()
    if err != nil {
        return 0, fmt.Errorf("last insert id: %w", err)
    }

    // Insert profile using the new user's ID
    if _, err = tx.ExecContext(ctx,
        `INSERT INTO profiles (user_id, bio) VALUES (?, ?)`, userID, bio,
    ); err != nil {
        return 0, fmt.Errorf("insert profile for user %d: %w", userID, err)
    }

    if err := tx.Commit(); err != nil {
        return 0, fmt.Errorf("commit: %w", err)
    }
    return userID, nil
}
```

**Rubric:**
- 3 pts: `defer tx.Rollback()` present immediately after BeginTx; both inserts use `tx.ExecContext` (not `db.ExecContext`); `LastInsertId` used for the foreign key; `Commit` called at end; errors wrapped
- 2 pts: Correct logic but uses `db.ExecContext` instead of `tx.ExecContext` for one insert (operations outside the transaction — serious bug, not just style), OR missing error wrapping
- 1 pt: Missing `defer tx.Rollback()` but otherwise correct structure
- 0 pts: Does not use a transaction (two separate `db.ExecContext` calls — not atomic)

**Teaching note:**
The most critical error is using `db.ExecContext` instead of `tx.ExecContext` — the insert would happen outside the transaction and could not be rolled back. If a student makes this mistake, direct them to re-read the Transactions section.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — SQL Injection in login function [3 pts] (1 pt each part)

**(a) The vulnerability — SQL injection [1 pt]:**
The vulnerability is **SQL injection**. The `fmt.Sprintf` call concatenates user-controlled values (`username` and `password`) directly into a SQL string. An attacker who controls the `username` parameter can inject arbitrary SQL.

The exact input that bypasses the password check: pass `username = "admin'--"` and any string for password. The resulting query becomes:
```sql
SELECT id FROM users WHERE username='admin'--' AND password_hash='anything'
```
`--` starts a SQL comment, making everything after it ignored. The effective query is:
```sql
SELECT id FROM users WHERE username='admin'
```
This returns the admin user's ID without checking the password at all.

An even simpler bypass: `username = "' OR '1'='1" `, which produces `WHERE username='' OR '1'='1'` — matching every user and returning the first one.

**(b) Why this happens [1 pt]:**
String concatenation allows user input to break out of the string literal context. The single quote in `admin'` closes the string literal that the programmer opened with `'%s'`. The attacker is then writing raw SQL syntax, not data. The database engine receives a syntactically valid (but attacker-modified) SQL statement and executes it faithfully — it has no way to distinguish the programmer's intended SQL from the injected SQL.

**(c) The fix [1 pt]:**
```go
func login(ctx context.Context, db *sql.DB, username, password string) (int64, error) {
    var id int64
    err := db.QueryRowContext(ctx,
        // Parameterized: username and password are sent as typed values, never as SQL
        `SELECT id FROM users WHERE username = ? AND password_hash = ?`,
        username, password,
    ).Scan(&id)
    if errors.Is(err, sql.ErrNoRows) {
        return 0, ErrNotFound // "user not found or wrong password"
    }
    if err != nil {
        return 0, fmt.Errorf("login: %w", err)
    }
    return id, nil
}
```

When `username` and `password` are passed as bind parameters, the database driver sends them over the protocol as typed values — separate from the SQL text. The database engine never sees a string with a quote in a position where it could terminate the SQL literal. No amount of SQL syntax in the values can escape this protection.

**Rubric:**
- 1 pt (a): Correctly names SQL injection AND shows a specific exploit input (or describes the mechanism precisely)
- 1 pt (b): Explains why string concatenation is the root cause — the user input can break out of the string literal
- 1 pt (c): Uses parameterized query with `?` placeholders; does NOT use `fmt.Sprintf` or string concatenation; also checks `sql.ErrNoRows`

---

## Section 5: Discussion — Answer Key

### 5.1 — database/sql vs. sqlx vs. sqlc vs. GORM [2 pts]

**Example strong answer:**
The statement is too absolute. The right tool depends on project requirements. Comparing across two dimensions — **query visibility/control** and **developer velocity** — clarifies the tradeoffs.

`database/sql` offers maximum control: every query is explicit, scanning is manual, and there is no generated SQL to debug. It is the right choice when queries are complex, performance-critical, or require precise control over what hits the database. The cost is verbosity — scanning 8-column structs manually is tedious.

`sqlx` adds `StructScan`, `Get`, and `Select` that reduce scanning boilerplate by matching struct field tags to column names. It wraps `database/sql` and does not hide SQL — queries remain explicit strings. It is a pragmatic improvement for teams already using `database/sql` who want less repetition.

`sqlc` generates type-safe Go code from `.sql` files at build time. A query like `-- name: GetUser :one\nSELECT id, name FROM users WHERE id = $1` generates `func GetUser(ctx, id) (User, error)` with proper types. This gives compile-time verification that queries match schema — catching a renamed column at build time rather than production runtime. It is the best choice for new projects where SQL will evolve over time.

`GORM` trades query control for rapid prototyping: `db.Find(&users)` generates the SELECT automatically. The cost is opacity — the generated SQL is often surprising, N+1 query patterns are easy to introduce accidentally, and debugging requires inspecting generated SQL. It is appropriate for quick prototypes or admin tools where correctness and performance are less critical.

For a professional service: prefer `sqlc` (new projects) or `sqlx` (adding to existing code). Avoid `GORM` in performance-critical paths or for complex join-heavy queries.

**Elements that earn full credit:**
- Compares at least two tools across at least two meaningful dimensions
- Acknowledges tradeoffs in both directions (does not say one tool is always best)
- Names a specific use case where each of at least two tools is the right choice

**Rubric:**
- 2 pts: Covers multiple tools, genuine tradeoffs, specific use cases — shows real understanding
- 1 pt: Describes tools accurately but takes a dogmatic position ("always X, never Y") without tradeoff analysis
- 0 pts: Cannot distinguish the tools meaningfully, or gives an opinion without justification

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Connection pool exhaustion [+5 pts]

**Full credit answer:**

**Step-by-step pool exhaustion with `MaxOpenConns=5` and 10 concurrent goroutines:**
1. Goroutines 1–5 call `db.QueryContext`. The pool creates 5 connections (or checks out 5 idle ones). All 5 are now checked out — the pool is at max capacity.
2. Goroutine 6 calls `db.QueryContext`. The pool has no available connections and has hit `MaxOpenConns`. Goroutine 6 **blocks** — it waits in an internal queue inside `sql.DB` for a connection to become available.
3. Goroutines 7–10 also block in the same queue.
4. When goroutine 1 finishes (its query completes and rows are closed), its connection is returned to the pool. The pool immediately checks it out to the first waiting goroutine (goroutine 6).
5. If goroutines 1–5 are very slow (e.g., iterating large result sets), goroutines 6–10 wait for the entire duration.

**Context cancellation resolving pool exhaustion:**
If the waiting goroutine's context is cancelled (e.g., the HTTP client disconnects, or a timeout fires) while it is blocked waiting for a connection, `db.QueryContext` returns `context.DeadlineExceeded` or `context.Canceled` immediately. The goroutine unblocks without acquiring a connection, freeing it to clean up.

**Short demonstration:**
```go
db.SetMaxOpenConns(2)
var wg sync.WaitGroup
for i := range 5 {
    wg.Add(1)
    go func(n int) {
        defer wg.Done()
        ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
        defer cancel()
        // Simulate a slow query by holding the connection open
        rows, err := db.QueryContext(ctx, `SELECT 1`)
        if err != nil {
            fmt.Printf("goroutine %d: %v\n", n, err) // may print context deadline exceeded
            return
        }
        defer rows.Close()
        time.Sleep(200 * time.Millisecond) // hold the connection
    }(i)
}
wg.Wait()
```
With `MaxOpenConns=2`, goroutines 3–5 will likely hit the 500ms timeout waiting for a connection and print `context deadline exceeded`.

**`SetConnMaxIdleTime` and `SetConnMaxLifetime` prevent a different class of issues:**
- **`SetConnMaxIdleTime`** — closes connections that have been idle in the pool longer than the duration. Prevents "ghost" connections: firewalls and load balancers often drop TCP connections silently after they have been idle for minutes. Without this, the pool might hold connections that appear healthy but have been dropped at the network level; the next query attempt would get a network error. Periodic idle expiry forces the pool to reconnect.
- **`SetConnMaxLifetime`** — forces connections to be closed and re-established after a maximum total age. This handles database server restarts and graceful rolling deployments: old connections from before a restart are eventually discarded and replaced with fresh ones.

**Rubric:**
- 5 pts: Correctly describes the blocking behavior (goroutine 6 waits, not panics); explains context cancellation releasing the wait; demonstrates pool exhaustion in code; explains both idle time and lifetime settings with distinct purposes
- 3 pts: Correctly describes blocking and context cancellation; may have incomplete code or miss one of the two tuning parameters
- 1 pt: Understands that pool exhaustion causes blocking but cannot explain the context cancellation mechanism or the tuning parameters
- 0 pts: Thinks pool exhaustion causes a panic or immediate error (not a wait)

**Teaching note:**
The key insight is that goroutines *block* (not panic or error) when the pool is exhausted, and that context cancellation is what unblocks them when waiting too long. Students who score 1 pt here often don't realize that `database/sql` manages a queue internally.

---

## Common Wrong Answers Across the Test

1. **Confusing `sql.Open` success with database connectivity** — These are distinct: `sql.Open` validates the driver name and DSN format; `PingContext` establishes an actual connection. Students who miss this will write startup code that silently fails to verify the database is reachable.
2. **Omitting `rows.Err()` after the rows loop** — The most commonly skipped step. Students who miss this may never encounter the bug in development (no mid-query failures) but will suffer silent data truncation in production when network drops occur.
3. **String concatenation in queries** — The SQL injection question (4.1) is specifically designed to surface this. Any use of `fmt.Sprintf` or string `+` to build a query with user input is wrong. This should trigger an immediate recognition of the vulnerability, not a "it works as long as the input is safe" response.
4. **Depending on concrete type in handler** — Students who write `store *SQLUserStore` instead of `store UserStore` in the server struct have understood the mechanics but missed the point: the interface is what enables swapping implementations for tests.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 1 (especially 1.1 and 1.2) likely read the module without running the code. Recommend: write the `sql.Open` + `PingContext` startup sequence from memory, run it with and without a valid DSN, observe the difference.
- Students who get Section 4 (SQL injection) wrong have a significant gap. Direct them to reread the "SQL Injection and Parameterized Queries" section and look at the OWASP SQL Injection Prevention Cheat Sheet. This is a safety-critical issue that cannot be left as a "soft understanding."
- Students who struggle with Section 2.3 (repository pattern) should go back to [[go/6. Methods and Interfaces]] — specifically the section on depending on interfaces rather than concrete types. The database application of this pattern is direct.
- The bonus question (pool exhaustion) rewards students who have deployed production Go services or read deeply. Don't penalize students who skip it — it tests knowledge beyond the module's explicit scope.
- A score below 60% on this test generally indicates the student rushed through the module. The concepts (pool model, rows protocol, transactions, SQL injection) each require hands-on practice to internalize. Send back to EXERCISES.md — specifically Exercises 3 (CRUD repository), 4 (transaction), and 5 (SQL injection) before re-attempting the test.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
