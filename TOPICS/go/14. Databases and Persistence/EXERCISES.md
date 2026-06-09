# Exercises — Module 14: Databases and Persistence

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just run code mentally — actually write or type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–15 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 20–35 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 40–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Schema Setup and Basic Insert/Query [🟢 Easy] [1 pt]

### Context
Every `database/sql` program starts with the same sequence: open, ping, create schema, use it. This exercise confirms you can write the full startup boilerplate and the basic `QueryContext` rows iteration protocol. Using `file::memory:` keeps the exercise self-contained.

### Task
Write a Go program that:
1. Opens a SQLite in-memory database (`"file::memory:"` as the DSN, driver name `"sqlite"` from `modernc.org/sqlite`)
2. Calls `db.PingContext` to verify connectivity
3. Creates a `tasks` table: `id INTEGER PRIMARY KEY AUTOINCREMENT`, `title TEXT NOT NULL`, `done INTEGER NOT NULL DEFAULT 0`
4. Inserts three rows: `"Buy groceries"`, `"Write tests"`, `"Deploy service"`
5. Queries all rows with `QueryContext` and prints each task using the full `rows.Next / rows.Scan / rows.Err / defer rows.Close` protocol

### Requirements
- [ ] Uses `_ "modernc.org/sqlite"` blank import
- [ ] Calls `db.PingContext` after `sql.Open` with a 5-second timeout context
- [ ] Uses `ExecContext` for table creation and inserts
- [ ] Iterates rows using `rows.Next` with `defer rows.Close()` placed immediately after the `QueryContext` error check
- [ ] Checks `rows.Err()` after the loop

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The DSN for an in-memory SQLite database is `"file::memory:"`. Use `sql.Open("sqlite", "file::memory:")`. If you get "unknown driver", check your blank import — `_ "modernc.org/sqlite"` must be present.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The rows protocol skeleton:
```go
rows, err := db.QueryContext(ctx, `SELECT id, title, done FROM tasks`)
if err != nil { log.Fatal(err) }
defer rows.Close()  // here, NOT at the end of the function
for rows.Next() {
    var id int64; var title string; var done int
    rows.Scan(&id, &title, &done)
    fmt.Printf("%d: %s (done=%d)\n", id, title, done)
}
if err := rows.Err(); err != nil { log.Fatal(err) }
```

</details>

### Expected Output / Acceptance Criteria
```
1: Buy groceries (done=0)
2: Write tests (done=0)
3: Deploy service (done=0)
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "time"

    _ "modernc.org/sqlite" // registers the "sqlite" driver via init()
)

func main() {
    db, err := sql.Open("sqlite", "file::memory:")
    if err != nil {
        log.Fatalf("sql.Open: %v", err)
    }
    defer db.Close()

    // PingContext actually opens a connection — verifies driver + DSN
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    if err := db.PingContext(ctx); err != nil {
        log.Fatalf("ping: %v", err)
    }

    // Create table
    _, err = db.ExecContext(context.Background(), `
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
    `)
    if err != nil {
        log.Fatalf("create table: %v", err)
    }

    // Insert three rows
    for _, title := range []string{"Buy groceries", "Write tests", "Deploy service"} {
        if _, err := db.ExecContext(context.Background(),
            `INSERT INTO tasks (title) VALUES (?)`, title,
        ); err != nil {
            log.Fatalf("insert: %v", err)
        }
    }

    // Query and print with full rows protocol
    rows, err := db.QueryContext(context.Background(), `SELECT id, title, done FROM tasks ORDER BY id`)
    if err != nil {
        log.Fatalf("query: %v", err)
    }
    defer rows.Close() // must be here, right after error check

    for rows.Next() {
        var id int64
        var title string
        var done int
        if err := rows.Scan(&id, &title, &done); err != nil {
            log.Fatalf("scan: %v", err)
        }
        fmt.Printf("%d: %s (done=%d)\n", id, title, done)
    }
    if err := rows.Err(); err != nil { // check for iteration errors
        log.Fatalf("rows.Err: %v", err)
    }
}
```

**Explanation:**
The blank import `_ "modernc.org/sqlite"` is what makes `sql.Open("sqlite", ...)` work — the package's `init()` calls `sql.Register`. `sql.Open` is lazy; `PingContext` is the real connectivity check. `defer rows.Close()` is placed immediately after the `err != nil` check (not at the bottom of the function) so it is guaranteed to fire even if the loop exits early. `rows.Err()` after the loop catches errors that stopped iteration mid-stream.

**Common wrong answers:**
- Placing `defer rows.Close()` at the bottom of `main` instead of right after the error check — misses the close if an early return exists elsewhere
- Not checking `rows.Err()` — compiles and usually works, but silently truncates results on network errors

</details>

---

## Exercise 2: NULL Handling — Scanning Nullable Columns [🟢 Easy] [1 pt]

### Context
NULL in SQL maps awkwardly to Go's value types. Scanning a NULL `TEXT` column into a `string` panics at runtime. This exercise forces you to encounter the problem and fix it using both `sql.NullString` and a `*string` pointer — two different idiomatic approaches.

### Task
Write a Go program that:
1. Creates a `profiles` table: `id INTEGER PRIMARY KEY`, `username TEXT NOT NULL`, `bio TEXT` (nullable)
2. Inserts two rows: one with a bio (`"Gopher"`) and one with NULL bio
3. Queries both rows and prints them — showing that NULL is represented as either `sql.NullString{Valid: false}` or a nil `*string`

Implement the scan twice: first using `sql.NullString` for the bio column, then using `*string`.

### Requirements
- [ ] The `bio` column is nullable (`TEXT` with no `NOT NULL` constraint)
- [ ] First scan approach: use `sql.NullString`; print `"(no bio)"` when `Valid == false`
- [ ] Second scan approach: use `*string`; print `"(no bio)"` when the pointer is nil
- [ ] Both approaches produce identical output
- [ ] Using a plain `string` to scan the nullable column (without fixing it) is shown to be wrong in a comment

### Hints
<details>
<summary>Hint 1</summary>

For `sql.NullString`: declare `var bio sql.NullString` and pass `&bio` to `Scan`. Check `bio.Valid` before using `bio.String`.

For `*string`: declare `var bio *string` and pass `&bio` to `Scan`. When the column is NULL, `bio` will be `nil` after scanning.

</details>

### Expected Output / Acceptance Criteria
```
--- Using sql.NullString ---
1: alice bio="Gopher"
2: bob bio=(no bio)

--- Using *string ---
1: alice bio="Gopher"
2: bob bio=(no bio)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"

    _ "modernc.org/sqlite"
)

func main() {
    db, _ := sql.Open("sqlite", "file::memory:")
    defer db.Close()

    db.ExecContext(context.Background(), `
        CREATE TABLE profiles (
            id       INTEGER PRIMARY KEY,
            username TEXT    NOT NULL,
            bio      TEXT    -- nullable: no NOT NULL constraint
        )
    `)

    // Insert one row with bio, one without (NULL)
    db.ExecContext(context.Background(), `INSERT INTO profiles VALUES (1, 'alice', 'Gopher')`)
    db.ExecContext(context.Background(), `INSERT INTO profiles VALUES (2, 'bob', NULL)`)

    ctx := context.Background()

    // --- Approach 1: sql.NullString ---
    fmt.Println("--- Using sql.NullString ---")
    rows, err := db.QueryContext(ctx, `SELECT id, username, bio FROM profiles ORDER BY id`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()
    for rows.Next() {
        var id int64
        var username string
        var bio sql.NullString // Valid=false when column is NULL
        if err := rows.Scan(&id, &username, &bio); err != nil {
            log.Fatal(err)
        }
        if bio.Valid {
            fmt.Printf("%d: %s bio=%q\n", id, username, bio.String)
        } else {
            fmt.Printf("%d: %s bio=(no bio)\n", id, username)
        }
    }
    rows.Err()

    // --- Approach 2: *string pointer ---
    fmt.Println("\n--- Using *string ---")
    rows2, err := db.QueryContext(ctx, `SELECT id, username, bio FROM profiles ORDER BY id`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows2.Close()
    for rows2.Next() {
        var id int64
        var username string
        var bio *string // nil when column is NULL
        if err := rows2.Scan(&id, &username, &bio); err != nil {
            log.Fatal(err)
        }
        if bio != nil {
            fmt.Printf("%d: %s bio=%q\n", id, username, *bio)
        } else {
            fmt.Printf("%d: %s bio=(no bio)\n", id, username)
        }
    }
    rows2.Err()

    // WRONG (shown for contrast — do not use):
    // var bio string
    // rows.Scan(&id, &username, &bio) // panics at runtime when bio is NULL
}
```

**Explanation:**
`sql.NullString` is an explicit struct: `{String string; Valid bool}`. The `*string` approach is terser — Go's driver converts NULL to a nil pointer. Both are idiomatic; prefer `*string` for simpler code and `sql.NullString` when you need to distinguish "not provided" from "explicitly set to empty string". Scanning a NULL value into a non-pointer Go value type will fail at runtime with a conversion error — not a compile-time error, which makes it a dangerous mistake.

</details>

---

## Exercise 3: CRUD Repository [🟡 Medium] [2 pts]

### Context
The repository pattern is the core design principle of this module. This exercise asks you to build a complete `TaskStore` interface and its SQL implementation — all four CRUD operations. This represents the pattern you will use in real services.

### Task
Define a `Task` struct (fields: `ID int64`, `Title string`, `Done bool`) and a `TaskStore` interface with methods:
- `Create(ctx, title string) (int64, error)`
- `Get(ctx, id int64) (Task, error)`
- `SetDone(ctx, id int64, done bool) (error)`
- `List(ctx) ([]Task, error)`
- `Delete(ctx, id int64) (error)`

Implement `SQLTaskStore` that satisfies `TaskStore` over `database/sql`. Include a `var ErrNotFound = errors.New("not found")` sentinel. In `main`, exercise all five methods and print the results.

### Requirements
- [ ] `TaskStore` is an interface (not a concrete type)
- [ ] `SQLTaskStore` has all five methods with correct error wrapping using `fmt.Errorf("...: %w", err)`
- [ ] `Get` and `Delete` return `ErrNotFound` (wrapped) when the row does not exist
- [ ] `List` uses the full `rows.Next / Scan / Err / defer Close` protocol
- [ ] `main` demonstrates Create, Get, List, SetDone, Delete and prints results

### Hints
<details>
<summary>Hint 1</summary>

For `Get`: use `QueryRowContext(...).Scan(...)`. Check `errors.Is(err, sql.ErrNoRows)` and return `fmt.Errorf("task %d: %w", id, ErrNotFound)` in that case.

</details>

<details>
<summary>Hint 2</summary>

For `Delete` and `SetDone`: use `res.RowsAffected()` to detect when the WHERE clause matched zero rows — that means the task doesn't exist.

</details>

### Expected Output / Acceptance Criteria
Your output should show all five operations working correctly. For example:
```
created task id=1 title="Buy groceries"
created task id=2 title="Write tests"
got task: {1 Buy groceries false}
list: [{1 Buy groceries false} {2 Write tests false}]
set task 1 done
list: [{1 Buy groceries true} {2 Write tests false}]
deleted task 1
list: [{2 Write tests false}]
get deleted task: task 1: not found
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"
    "log"

    _ "modernc.org/sqlite"
)

var ErrNotFound = errors.New("not found")

type Task struct {
    ID    int64
    Title string
    Done  bool
}

type TaskStore interface {
    Create(ctx context.Context, title string) (int64, error)
    Get(ctx context.Context, id int64) (Task, error)
    SetDone(ctx context.Context, id int64, done bool) error
    List(ctx context.Context) ([]Task, error)
    Delete(ctx context.Context, id int64) error
}

type SQLTaskStore struct{ db *sql.DB }

func NewSQLTaskStore(db *sql.DB) *SQLTaskStore { return &SQLTaskStore{db: db} }

func (s *SQLTaskStore) Create(ctx context.Context, title string) (int64, error) {
    res, err := s.db.ExecContext(ctx, `INSERT INTO tasks (title) VALUES (?)`, title)
    if err != nil {
        return 0, fmt.Errorf("create task: %w", err)
    }
    id, err := res.LastInsertId()
    if err != nil {
        return 0, fmt.Errorf("last insert id: %w", err)
    }
    return id, nil
}

func (s *SQLTaskStore) Get(ctx context.Context, id int64) (Task, error) {
    var t Task
    var done int // SQLite stores booleans as 0/1
    err := s.db.QueryRowContext(ctx,
        `SELECT id, title, done FROM tasks WHERE id = ?`, id,
    ).Scan(&t.ID, &t.Title, &done)
    if errors.Is(err, sql.ErrNoRows) {
        return Task{}, fmt.Errorf("task %d: %w", id, ErrNotFound)
    }
    if err != nil {
        return Task{}, fmt.Errorf("get task %d: %w", id, err)
    }
    t.Done = done != 0
    return t, nil
}

func (s *SQLTaskStore) SetDone(ctx context.Context, id int64, done bool) error {
    doneInt := 0
    if done {
        doneInt = 1
    }
    res, err := s.db.ExecContext(ctx,
        `UPDATE tasks SET done = ? WHERE id = ?`, doneInt, id,
    )
    if err != nil {
        return fmt.Errorf("set done task %d: %w", id, err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("task %d: %w", id, ErrNotFound)
    }
    return nil
}

func (s *SQLTaskStore) List(ctx context.Context) ([]Task, error) {
    rows, err := s.db.QueryContext(ctx, `SELECT id, title, done FROM tasks ORDER BY id`)
    if err != nil {
        return nil, fmt.Errorf("list tasks: %w", err)
    }
    defer rows.Close()

    var tasks []Task
    for rows.Next() {
        var t Task
        var done int
        if err := rows.Scan(&t.ID, &t.Title, &done); err != nil {
            return nil, fmt.Errorf("scan task: %w", err)
        }
        t.Done = done != 0
        tasks = append(tasks, t)
    }
    if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("tasks iteration: %w", err)
    }
    return tasks, nil
}

func (s *SQLTaskStore) Delete(ctx context.Context, id int64) error {
    res, err := s.db.ExecContext(ctx, `DELETE FROM tasks WHERE id = ?`, id)
    if err != nil {
        return fmt.Errorf("delete task %d: %w", id, err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("task %d: %w", id, ErrNotFound)
    }
    return nil
}

func main() {
    db, _ := sql.Open("sqlite", "file::memory:")
    defer db.Close()
    db.ExecContext(context.Background(), `
        CREATE TABLE tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
    `)

    store := NewSQLTaskStore(db)
    ctx := context.Background()

    id1, _ := store.Create(ctx, "Buy groceries")
    id2, _ := store.Create(ctx, "Write tests")
    fmt.Printf("created task id=%d title=%q\n", id1, "Buy groceries")
    fmt.Printf("created task id=%d title=%q\n", id2, "Write tests")

    t, _ := store.Get(ctx, id1)
    fmt.Printf("got task: %+v\n", t)

    tasks, _ := store.List(ctx)
    fmt.Printf("list: %+v\n", tasks)

    store.SetDone(ctx, id1, true)
    fmt.Printf("set task %d done\n", id1)

    tasks, _ = store.List(ctx)
    fmt.Printf("list: %+v\n", tasks)

    store.Delete(ctx, id1)
    fmt.Printf("deleted task %d\n", id1)

    tasks, _ = store.List(ctx)
    fmt.Printf("list: %+v\n", tasks)

    _, err := store.Get(ctx, id1)
    fmt.Printf("get deleted task: %v\n", err)
    fmt.Printf("is ErrNotFound: %v\n", errors.Is(err, ErrNotFound))
}
```

**Explanation:**
SQLite represents booleans as integers (0/1), so the `done` field is scanned as `int` and converted. `RowsAffected() == 0` after DELETE or UPDATE is how you detect "row didn't exist" — there's no `sql.ErrNoRows` for modification statements. All errors are wrapped with `%w` so callers can use `errors.Is`. The `TaskStore` interface is the key: if the exercise asked for tests, you'd write a `FakeTaskStore` that satisfies the same interface without a database.

**Alternative approaches:**
You could use `sql.NullBool` for the done field instead of converting int — both are idiomatic. For PostgreSQL you would use `$1` placeholders and the `done` column could be `BOOLEAN` natively.

</details>

---

## Exercise 4: Transaction — Atomic Balance Transfer [🔴 Hard] [3 pts]

### Context
Transactions are the database mechanism for atomicity. The transfer exercise is the canonical example: debit one account, credit another — if either step fails, neither should take effect. This exercise exercises `BeginTx`, the `defer tx.Rollback()` safety pattern, `Commit`, and sentinel error wrapping.

### Task
Write a function `Transfer(ctx, db, fromID, toID int64, amount int) error` that:
1. Begins a transaction
2. Deducts `amount` from `fromID`'s balance (using `balance >= amount` in the WHERE clause to prevent negatives)
3. Adds `amount` to `toID`'s balance
4. Returns `ErrInsufficientFunds` (wrapped) if the debit affected 0 rows
5. Commits the transaction

Verify in `main` that:
- A successful transfer changes both balances correctly
- A failed transfer (insufficient funds) leaves both balances unchanged

### Requirements
- [ ] `defer tx.Rollback()` is the first statement after the `BeginTx` error check
- [ ] Uses `RowsAffected() == 0` to detect insufficient funds
- [ ] Defines and uses a `var ErrInsufficientFunds = errors.New("insufficient funds")` sentinel
- [ ] The caller can check `errors.Is(err, ErrInsufficientFunds)`
- [ ] Prints balances before, after a successful transfer, and after a failed transfer to prove atomicity

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

The transaction skeleton:
```go
tx, err := db.BeginTx(ctx, nil)
if err != nil { return fmt.Errorf("begin: %w", err) }
defer tx.Rollback() // no-op after Commit

// ... tx.ExecContext for debit and credit ...

return tx.Commit()
```

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

For the debit, the WHERE clause `AND balance >= ?` with the amount ensures the UPDATE only modifies the row if the balance is sufficient. If `RowsAffected()` returns 0, either the account doesn't exist or the balance was too low.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
res, err := tx.ExecContext(ctx,
    `UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?`,
    amount, fromID, amount,
)
if err != nil { return fmt.Errorf("debit: %w", err) }
if n, _ := res.RowsAffected(); n == 0 {
    return fmt.Errorf("account %d: %w", fromID, ErrInsufficientFunds)
}
```

When you return this error, `defer tx.Rollback()` fires and rolls back the transaction.

</details>

### Expected Output / Acceptance Criteria
```
initial balances:
  account 1: 200
  account 2: 50
after transfer 80 from 1→2:
  account 1: 120
  account 2: 130
transfer 150 from 2→1 failed: account 2: insufficient funds
is ErrInsufficientFunds: true
balances unchanged (rollback worked):
  account 1: 120
  account 2: 130
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"
    "log"

    _ "modernc.org/sqlite"
)

var ErrInsufficientFunds = errors.New("insufficient funds")

func transfer(ctx context.Context, db *sql.DB, fromID, toID, amount int64) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return fmt.Errorf("begin tx: %w", err)
    }
    // Safety net: Rollback is a no-op after Commit; fires on all other exits
    defer tx.Rollback()

    // Debit — WHERE balance >= amount prevents negative balances
    res, err := tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?`,
        amount, fromID, amount,
    )
    if err != nil {
        return fmt.Errorf("debit account %d: %w", fromID, err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("account %d: %w", fromID, ErrInsufficientFunds)
    }

    // Credit
    if _, err = tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance + ? WHERE id = ?`, amount, toID,
    ); err != nil {
        return fmt.Errorf("credit account %d: %w", toID, err)
    }

    return tx.Commit() // defer Rollback becomes a no-op after this returns nil
}

func printBalances(ctx context.Context, db *sql.DB) {
    rows, _ := db.QueryContext(ctx, `SELECT id, balance FROM accounts ORDER BY id`)
    defer rows.Close()
    for rows.Next() {
        var id, bal int64
        rows.Scan(&id, &bal)
        fmt.Printf("  account %d: %d\n", id, bal)
    }
}

func main() {
    db, _ := sql.Open("sqlite", "file::memory:")
    defer db.Close()

    db.ExecContext(context.Background(), `
        CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL)
    `)
    db.ExecContext(context.Background(), `INSERT INTO accounts VALUES (1, 200), (2, 50)`)

    ctx := context.Background()

    fmt.Println("initial balances:")
    printBalances(ctx, db)

    if err := transfer(ctx, db, 1, 2, 80); err != nil {
        log.Fatalf("transfer: %v", err)
    }
    fmt.Println("after transfer 80 from 1→2:")
    printBalances(ctx, db)

    err := transfer(ctx, db, 2, 1, 150)
    fmt.Printf("transfer 150 from 2→1 failed: %v\n", err)
    fmt.Printf("is ErrInsufficientFunds: %v\n", errors.Is(err, ErrInsufficientFunds))
    fmt.Println("balances unchanged (rollback worked):")
    printBalances(ctx, db)
}
```

**Step-by-step explanation:**
1. `BeginTx` opens a transaction on a dedicated connection; all subsequent calls on `tx` use that same connection.
2. `defer tx.Rollback()` is the safety net — if the function returns before `Commit`, the transaction is rolled back.
3. The debit UPDATE uses `AND balance >= ?` so it only affects the row when funds are sufficient; zero affected rows signals the error.
4. If the debit returns `ErrInsufficientFunds`, the function returns immediately, and `defer tx.Rollback()` fires.
5. `tx.Commit()` finalizes the transaction; after this, the deferred `Rollback` is a no-op (the transaction is already closed).

**Why this approach:**
The `WHERE balance >= ?` in the debit is a concurrency-safe check — even with multiple concurrent transfers, the condition is evaluated inside the transaction and protected by the database's row-level lock. A separate SELECT then UPDATE (check-then-act) pattern would have a TOCTOU race condition without Serializable isolation.

</details>

---

## Exercise 5: SQL Injection — Spot and Fix [🟡 Medium] [2 pts]

### Context
SQL injection is the most critical security vulnerability in database code. This exercise starts with a deliberately broken program that is vulnerable to injection, asks you to identify the vulnerability, and then fix it using parameterized queries.

### Task
The following function is vulnerable to SQL injection:

```go
func findUser(ctx context.Context, db *sql.DB, username string) (int64, error) {
    query := "SELECT id FROM users WHERE username = '" + username + "'"
    var id int64
    err := db.QueryRowContext(ctx, query).Scan(&id)
    if errors.Is(err, sql.ErrNoRows) {
        return 0, ErrNotFound
    }
    return id, err
}
```

1. Write a `main` that shows the vulnerability: pass `username = "alice' OR '1'='1"` and print what the constructed SQL string looks like (without running it against a real DB — just `fmt.Println(query)`)
2. Explain in a comment WHY this is dangerous
3. Rewrite `findUser` to be safe using a parameterized query

### Requirements
- [ ] Shows the constructed SQL string for the malicious input (to make the injection visible)
- [ ] Adds a comment explaining why the injection works
- [ ] Rewrites the function to use a `?` placeholder and pass `username` as an argument
- [ ] The safe version compiles and would work correctly if run against a real database

### Hints
<details>
<summary>Hint 1</summary>

Construct the injection query manually to see what it looks like:
```
SELECT id FROM users WHERE username = 'alice' OR '1'='1'
```
The `OR '1'='1'` part is always true — it turns the WHERE clause into "always match", returning the first user in the table regardless of the actual username.

</details>

### Expected Output / Acceptance Criteria
```
VULNERABLE query: SELECT id FROM users WHERE username = 'alice' OR '1'='1'
This returns ALL users because OR '1'='1' is always true.

SAFE query would use: SELECT id FROM users WHERE username = ?
with username passed as a bind parameter — the DB treats it as data, not SQL.
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"

    _ "modernc.org/sqlite"
)

var ErrNotFound = errors.New("not found")

// VULNERABLE: username is concatenated directly into SQL.
// An attacker can pass username = "alice' OR '1'='1" to bypass authentication.
func findUserVulnerable(ctx context.Context, db *sql.DB, username string) (int64, error) {
    // NEVER DO THIS — shown only to demonstrate the vulnerability
    query := "SELECT id FROM users WHERE username = '" + username + "'"
    fmt.Printf("VULNERABLE query: %s\n", query)
    // If username is "alice' OR '1'='1", the query becomes:
    //   SELECT id FROM users WHERE username = 'alice' OR '1'='1'
    // The OR '1'='1' is always true — the WHERE clause matches EVERY row.
    var id int64
    err := db.QueryRowContext(ctx, query).Scan(&id)
    if errors.Is(err, sql.ErrNoRows) {
        return 0, ErrNotFound
    }
    return id, err
}

// SAFE: username is passed as a bind parameter — never interpolated into SQL.
// The database driver sends it as a separate typed value over the protocol.
// The DB engine treats it as data, not as SQL syntax — injection is impossible.
func findUserSafe(ctx context.Context, db *sql.DB, username string) (int64, error) {
    var id int64
    err := db.QueryRowContext(ctx,
        `SELECT id FROM users WHERE username = ?`, // ? is a placeholder
        username,                                  // passed separately — never interpolated
    ).Scan(&id)
    if errors.Is(err, sql.ErrNoRows) {
        return 0, ErrNotFound
    }
    if err != nil {
        return 0, fmt.Errorf("find user: %w", err)
    }
    return id, nil
}

func main() {
    maliciousInput := "alice' OR '1'='1"

    // Show what the vulnerable query looks like
    query := "SELECT id FROM users WHERE username = '" + maliciousInput + "'"
    fmt.Printf("VULNERABLE query: %s\n", query)
    fmt.Println("This returns ALL users because OR '1'='1' is always true.")
    fmt.Println()
    fmt.Printf("SAFE query would use: SELECT id FROM users WHERE username = ?\n")
    fmt.Println("with username passed as a bind parameter — the DB treats it as data, not SQL.")
}
```

**Explanation:**
The injection works because `'alice' OR '1'='1'` is valid SQL syntax — the single quotes in the user input close the string literal opened by the programmer's `'`, then inject a new condition. The `?` placeholder approach sends `username` as a separate binary value to the database engine over the protocol. The database never concatenates it into SQL text — it is processed as a typed value, not as SQL syntax. There is no string escaping function that is a safe alternative; parameterization is the only correct solution.

**Why string escaping is not a safe alternative:**
Every escaping function has edge cases (character encoding, multi-byte characters, database-specific behavior). Parameterized queries have no such edge cases — the value is never part of the SQL text.

</details>

---

## Exercise 6: Connection Pool Tuning and Startup Wiring [🟡 Medium] [2 pts]

### Context
Configuring the connection pool and wiring a repository into an HTTP-style server struct is how `database/sql` is used in real applications. This exercise brings together everything: pool tuning, repository interface, and passing context from a simulated request to the database.

### Task
Write a program that:
1. Opens a SQLite database with the pool tuned: `MaxOpenConns=10`, `MaxIdleConns=5`, `ConnMaxLifetime=30min`, `ConnMaxIdleTime=5min`
2. Defines a `UserStore` interface with `CreateUser(ctx, name, email string) (int64, error)` and `GetUser(ctx, id int64) (User, error)`
3. Implements `SQLUserStore` satisfying `UserStore`
4. Defines a `server` struct with a `store UserStore` field (interface, not concrete type)
5. Simulates a request by creating a context with a 3-second deadline and calling `store.CreateUser` and `store.GetUser` through it

### Requirements
- [ ] Pool tuning calls appear before first DB use
- [ ] The `server` struct holds `UserStore` (interface), not `*SQLUserStore`
- [ ] Context with deadline is used for all DB calls
- [ ] If context deadline is hit during a query, the error is printed (simulate with a very short deadline if you want to test the path)

### Hints
<details>
<summary>Hint 1</summary>

```go
type server struct {
    store UserStore // interface — swap for fake in tests
}
```

Create the server as `srv := &server{store: NewSQLUserStore(db)}`. The handler calls `srv.store.CreateUser(ctx, ...)`.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"
    "log"
    "time"

    _ "modernc.org/sqlite"
)

var ErrNotFound = errors.New("not found")

type User struct {
    ID    int64
    Name  string
    Email string
}

// UserStore is the persistence interface. Handlers depend on this, not on *SQLUserStore.
type UserStore interface {
    CreateUser(ctx context.Context, name, email string) (int64, error)
    GetUser(ctx context.Context, id int64) (User, error)
}

type SQLUserStore struct{ db *sql.DB }

func NewSQLUserStore(db *sql.DB) *SQLUserStore { return &SQLUserStore{db: db} }

func (s *SQLUserStore) CreateUser(ctx context.Context, name, email string) (int64, error) {
    res, err := s.db.ExecContext(ctx,
        `INSERT INTO users (name, email) VALUES (?, ?)`, name, email,
    )
    if err != nil {
        return 0, fmt.Errorf("create user: %w", err)
    }
    id, _ := res.LastInsertId()
    return id, nil
}

func (s *SQLUserStore) GetUser(ctx context.Context, id int64) (User, error) {
    var u User
    err := s.db.QueryRowContext(ctx,
        `SELECT id, name, email FROM users WHERE id = ?`, id,
    ).Scan(&u.ID, &u.Name, &u.Email)
    if errors.Is(err, sql.ErrNoRows) {
        return User{}, fmt.Errorf("user %d: %w", id, ErrNotFound)
    }
    if err != nil {
        return User{}, fmt.Errorf("get user %d: %w", id, err)
    }
    return u, nil
}

// server holds a UserStore interface — can be swapped for a fake in tests
type server struct {
    store UserStore
}

func (s *server) simulateRequest() {
    // Simulate an HTTP request context with a deadline
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()

    id, err := s.store.CreateUser(ctx, "Alice", "alice@example.com")
    if err != nil {
        log.Printf("create user: %v", err)
        return
    }
    fmt.Printf("created user id=%d\n", id)

    u, err := s.store.GetUser(ctx, id)
    if err != nil {
        log.Printf("get user: %v", err)
        return
    }
    fmt.Printf("got user: %+v\n", u)
}

func main() {
    db, err := sql.Open("sqlite", "file::memory:")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Tune the pool before first use
    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(30 * time.Minute)
    db.SetConnMaxIdleTime(5 * time.Minute)

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    if err := db.PingContext(ctx); err != nil {
        log.Fatalf("ping: %v", err)
    }

    db.ExecContext(context.Background(), `
        CREATE TABLE users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    `)

    srv := &server{store: NewSQLUserStore(db)}
    srv.simulateRequest()
}
```

**Explanation:**
The `server` struct holds `UserStore` (the interface), not `*SQLUserStore` (the concrete type). This means in tests you can write `srv := &server{store: NewFakeUserStore()}` — no database required. Pool tuning is done before the first query. The `WithTimeout` context simulates the deadline a real HTTP request would carry via `r.Context()`.

</details>

---

## Exercise 7: Full CRUD API with FakeStore Test [⭐ Challenge] [5 pts]

### Context
This is the capstone exercise for the module: wire everything together. You will build a minimal but complete HTTP JSON API backed by a SQLite repository, using the repository pattern, and write a test that uses a `FakeStore` instead of a real database. This is the pattern that production Go services use.

### Task
Build an HTTP server that:
1. Has `POST /notes` (create), `GET /notes/{id}` (get by id), `GET /notes` (list), `DELETE /notes/{id}` endpoints
2. Uses the `NoteStore` interface and `SQLNoteStore` implementation from the module README
3. Writes a `FakeNoteStore` that satisfies `NoteStore` using an in-memory map
4. Writes at least two `httptest.NewRecorder` tests: one for `POST /notes` and one for `GET /notes/{id}` using `FakeNoteStore` — no database needed

### Requirements
- [ ] All four HTTP endpoints are implemented
- [ ] Handlers depend on `NoteStore` interface
- [ ] `FakeNoteStore` satisfies `NoteStore` without a database
- [ ] At least two tests use `httptest.NewRecorder` with `FakeNoteStore`
- [ ] JSON encoding/decoding is used for request/response bodies
- [ ] Tests pass with `go test ./...`

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

Route matching without a third-party router: use `http.NewServeMux()` with patterns like `"POST /notes"` and `"GET /notes/{id}"` (Go 1.22+ supports method+path patterns natively). For `{id}`, use `r.PathValue("id")`.

</details>

<details>
<summary>Hint 2 (test structure hint)</summary>

```go
func TestCreateNote(t *testing.T) {
    store := NewFakeNoteStore()
    srv := &server{store: store}
    body := strings.NewReader(`{"title":"test"}`)
    req := httptest.NewRequest("POST", "/notes", body)
    rr := httptest.NewRecorder()
    srv.routes().ServeHTTP(rr, req)
    if rr.Code != http.StatusCreated { t.Errorf(...) }
}
```

</details>

<details>
<summary>Hint 3 (FakeNoteStore skeleton)</summary>

```go
type FakeNoteStore struct {
    mu    sync.Mutex
    notes map[int64]Note
    next  int64
}
func NewFakeNoteStore() *FakeNoteStore {
    return &FakeNoteStore{notes: make(map[int64]Note), next: 1}
}
```

Implement all methods of `NoteStore` on `*FakeNoteStore`.

</details>

### Expected Output / Acceptance Criteria
`go test ./...` passes. The tests cover create (status 201, response body has `id`) and get (status 200, response body matches created note). The HTTP server runs with `go run .` and responds to `curl` commands correctly.

### Solution
<details>
<summary>Show Solution (attempt first — this is the capstone!)</summary>

```go
// main.go
package main

import (
    "context"
    "database/sql"
    "encoding/json"
    "errors"
    "fmt"
    "log"
    "net/http"
    "strconv"

    _ "modernc.org/sqlite"
)

var ErrNotFound = errors.New("not found")

type Note struct {
    ID    int64   `json:"id"`
    Title string  `json:"title"`
    Body  *string `json:"body,omitempty"`
}

type NoteStore interface {
    Create(ctx context.Context, title string, body *string) (int64, error)
    Get(ctx context.Context, id int64) (Note, error)
    List(ctx context.Context) ([]Note, error)
    Delete(ctx context.Context, id int64) error
}

type SQLNoteStore struct{ db *sql.DB }

func NewSQLNoteStore(db *sql.DB) *SQLNoteStore { return &SQLNoteStore{db: db} }

func (s *SQLNoteStore) Create(ctx context.Context, title string, body *string) (int64, error) {
    res, err := s.db.ExecContext(ctx, `INSERT INTO notes (title, body) VALUES (?, ?)`, title, body)
    if err != nil {
        return 0, fmt.Errorf("create note: %w", err)
    }
    id, _ := res.LastInsertId()
    return id, nil
}

func (s *SQLNoteStore) Get(ctx context.Context, id int64) (Note, error) {
    var n Note
    err := s.db.QueryRowContext(ctx,
        `SELECT id, title, body FROM notes WHERE id = ?`, id,
    ).Scan(&n.ID, &n.Title, &n.Body)
    if errors.Is(err, sql.ErrNoRows) {
        return Note{}, fmt.Errorf("note %d: %w", id, ErrNotFound)
    }
    if err != nil {
        return Note{}, fmt.Errorf("get note %d: %w", id, err)
    }
    return n, nil
}

func (s *SQLNoteStore) List(ctx context.Context) ([]Note, error) {
    rows, err := s.db.QueryContext(ctx, `SELECT id, title, body FROM notes ORDER BY id`)
    if err != nil {
        return nil, fmt.Errorf("list notes: %w", err)
    }
    defer rows.Close()
    var notes []Note
    for rows.Next() {
        var n Note
        if err := rows.Scan(&n.ID, &n.Title, &n.Body); err != nil {
            return nil, fmt.Errorf("scan: %w", err)
        }
        notes = append(notes, n)
    }
    return notes, rows.Err()
}

func (s *SQLNoteStore) Delete(ctx context.Context, id int64) error {
    res, err := s.db.ExecContext(ctx, `DELETE FROM notes WHERE id = ?`, id)
    if err != nil {
        return fmt.Errorf("delete note: %w", err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("note %d: %w", id, ErrNotFound)
    }
    return nil
}

type server struct{ store NoteStore }

func (s *server) routes() http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("POST /notes", s.handleCreate)
    mux.HandleFunc("GET /notes/{id}", s.handleGet)
    mux.HandleFunc("GET /notes", s.handleList)
    mux.HandleFunc("DELETE /notes/{id}", s.handleDelete)
    return mux
}

func (s *server) handleCreate(w http.ResponseWriter, r *http.Request) {
    var req struct {
        Title string  `json:"title"`
        Body  *string `json:"body"`
    }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "bad request", http.StatusBadRequest)
        return
    }
    id, err := s.store.Create(r.Context(), req.Title, req.Body)
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(map[string]int64{"id": id})
}

func (s *server) handleGet(w http.ResponseWriter, r *http.Request) {
    id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
    if err != nil {
        http.Error(w, "bad id", http.StatusBadRequest)
        return
    }
    note, err := s.store.Get(r.Context(), id)
    if errors.Is(err, ErrNotFound) {
        http.Error(w, "not found", http.StatusNotFound)
        return
    }
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(note)
}

func (s *server) handleList(w http.ResponseWriter, r *http.Request) {
    notes, err := s.store.List(r.Context())
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    if notes == nil {
        notes = []Note{}
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(notes)
}

func (s *server) handleDelete(w http.ResponseWriter, r *http.Request) {
    id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
    if err != nil {
        http.Error(w, "bad id", http.StatusBadRequest)
        return
    }
    if err := s.store.Delete(r.Context(), id); errors.Is(err, ErrNotFound) {
        http.Error(w, "not found", http.StatusNotFound)
        return
    }
    w.WriteHeader(http.StatusNoContent)
}

func main() {
    db, err := sql.Open("sqlite", "file:notes.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
    db.ExecContext(context.Background(), `
        CREATE TABLE IF NOT EXISTS notes (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            body  TEXT
        )
    `)
    srv := &server{store: NewSQLNoteStore(db)}
    log.Println("listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", srv.routes()))
}
```

```go
// main_test.go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "net/http/httptest"
    "strings"
    "sync"
    "testing"
)

// FakeNoteStore is an in-memory NoteStore for testing — no DB required.
type FakeNoteStore struct {
    mu    sync.Mutex
    notes map[int64]Note
    next  int64
}

func NewFakeNoteStore() *FakeNoteStore {
    return &FakeNoteStore{notes: make(map[int64]Note), next: 1}
}

func (f *FakeNoteStore) Create(_ context.Context, title string, body *string) (int64, error) {
    f.mu.Lock(); defer f.mu.Unlock()
    id := f.next; f.next++
    f.notes[id] = Note{ID: id, Title: title, Body: body}
    return id, nil
}

func (f *FakeNoteStore) Get(_ context.Context, id int64) (Note, error) {
    f.mu.Lock(); defer f.mu.Unlock()
    n, ok := f.notes[id]
    if !ok {
        return Note{}, fmt.Errorf("note %d: %w", id, ErrNotFound)
    }
    return n, nil
}

func (f *FakeNoteStore) List(_ context.Context) ([]Note, error) {
    f.mu.Lock(); defer f.mu.Unlock()
    notes := make([]Note, 0, len(f.notes))
    for _, n := range f.notes { notes = append(notes, n) }
    return notes, nil
}

func (f *FakeNoteStore) Delete(_ context.Context, id int64) error {
    f.mu.Lock(); defer f.mu.Unlock()
    if _, ok := f.notes[id]; !ok {
        return fmt.Errorf("note %d: %w", id, ErrNotFound)
    }
    delete(f.notes, id)
    return nil
}

func TestCreateNote(t *testing.T) {
    srv := &server{store: NewFakeNoteStore()}
    body := strings.NewReader(`{"title":"Test note"}`)
    req := httptest.NewRequest(http.MethodPost, "/notes", body)
    rr := httptest.NewRecorder()
    srv.routes().ServeHTTP(rr, req)

    if rr.Code != http.StatusCreated {
        t.Errorf("expected 201, got %d", rr.Code)
    }
    var resp map[string]int64
    json.NewDecoder(rr.Body).Decode(&resp)
    if resp["id"] == 0 {
        t.Error("expected non-zero id in response")
    }
}

func TestGetNote(t *testing.T) {
    store := NewFakeNoteStore()
    id, _ := store.Create(context.Background(), "My note", nil)
    srv := &server{store: store}

    req := httptest.NewRequest(http.MethodGet, fmt.Sprintf("/notes/%d", id), nil)
    rr := httptest.NewRecorder()
    srv.routes().ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Errorf("expected 200, got %d", rr.Code)
    }
    var note Note
    json.NewDecoder(rr.Body).Decode(&note)
    if note.Title != "My note" {
        t.Errorf("expected title %q, got %q", "My note", note.Title)
    }
}
```

**Step-by-step explanation:**
1. `NoteStore` is the interface; `SQLNoteStore` and `FakeNoteStore` both satisfy it.
2. `server.store` is `NoteStore` — not a concrete type. This is what makes the test swap possible.
3. Tests use `httptest.NewRecorder` and `httptest.NewRequest` — no real server, no port, no goroutines. Runs in microseconds.
4. `FakeNoteStore` uses `sync.Mutex` to be safe if tests run in parallel.
5. `go test ./...` runs both tests; neither requires a database.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Schema Setup and Basic Insert/Query | — | —/1 | — | — |
| Exercise 2 — NULL Handling | — | —/1 | — | — |
| Exercise 3 — CRUD Repository | — | —/2 | — | — |
| Exercise 4 — Atomic Balance Transfer | — | —/3 | — | — |
| Exercise 5 — SQL Injection: Spot and Fix | — | —/2 | — | — |
| Exercise 6 — Connection Pool Tuning and Startup | — | —/2 | — | — |
| Exercise 7 — Full CRUD API with FakeStore Test | — | —/5 | — | — |
| **Total** | | **—/16** | | |

**Passing threshold:** 10/16 (63%). Aim for 13/16 (81%) before taking the test.
