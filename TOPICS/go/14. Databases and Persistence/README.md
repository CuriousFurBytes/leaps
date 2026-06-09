# Module 14: Databases and Persistence

[← Module 13: Web Services and APIs](../13.%20Web%20Services%20and%20APIs/) | [Topic Home](../README.md) | [Module 15: Reflection and Metaprogramming →](../15.%20Reflection%20and%20Metaprogramming/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [The database/sql Architecture](#the-databasesql-architecture)
  - [sql.DB Is a Connection Pool](#sqldb-is-a-connection-pool)
  - [Opening and Verifying a Connection](#opening-and-verifying-a-connection)
  - [Querying — QueryContext, QueryRowContext, ExecContext](#querying--querycontext-queryrowcontext-execcontext)
  - [Iterating Rows](#iterating-rows)
  - [Scanning into Structs and Handling NULLs](#scanning-into-structs-and-handling-nulls)
  - [Prepared Statements and Placeholder Syntax](#prepared-statements-and-placeholder-syntax)
  - [Transactions](#transactions)
  - [Connection Pool Tuning](#connection-pool-tuning)
  - [SQL Injection and Parameterized Queries](#sql-injection-and-parameterized-queries)
  - [Migrations](#migrations)
  - [The Repository Pattern](#the-repository-pattern)
  - [database/sql vs sqlx, sqlc, and GORM](#databasesql-vs-sqlx-sqlc-and-gorm)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Related Concepts](#related-concepts)
- [Exercises](#exercises)
- [Test](#test)
- [Projects](#projects)
- [Further Reading](#further-reading)
- [Learning Journal](#learning-journal)

---

## Overview

This module covers **Go's standard approach to relational databases**: the `database/sql` package, the driver model, connection pooling, querying, transactions, NULL handling, SQL injection prevention, migrations, and the repository pattern. These primitives are the foundation on which every production Go service that persists data is built.

By the end of this module, you will understand how `database/sql` works at the architecture level — not just how to call its methods, but why the pool-based model exists, why context-aware methods are non-negotiable in servers, and how the repository pattern ties your database layer cleanly to the HTTP handlers you built in [[go/13. Web Services and APIs]].

**Difficulty:** Advanced &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain the `database/sql` driver model (blank-import registration, the `Driver` interface) and why `sql.Open` is lazy — _given a driver import, explain what registration happens and why `Ping` is necessary_
2. Use `QueryContext`, `QueryRowContext`, and `ExecContext` correctly, iterating rows with the full `Next`/`Scan`/`Err`/`Close` protocol — _write a function that returns a slice of structs from a query_
3. Handle NULLable columns using `sql.NullString`, `sql.NullInt64`, and pointer types — _fix a scan crash caused by a NULL column_
4. Write safe, parameterized queries using the correct placeholder syntax for your driver (`?` vs `$1`) — _identify a SQL injection vulnerability and fix it_
5. Implement transactions with `BeginTx`, the `defer tx.Rollback()` safety pattern, and `Commit` — _write a multi-step transfer operation that rolls back on any failure_
6. Define a storage interface and implement the repository pattern over `database/sql` — _wire a repository into an HTTP handler from [[go/13. Web Services and APIs]] and swap it for a fake in tests_

---

## Prerequisites

### Required Modules

- [[go/6. Methods and Interfaces]] — you need to understand: how to define interfaces, write structs that satisfy them, and depend on interface types rather than concrete types; the repository pattern relies entirely on this
- [[go/8. Error Handling]] — you need to understand: error wrapping with `fmt.Errorf("%w")`, `errors.Is`, `errors.As`, and when to propagate vs. handle errors; database code returns errors at every step
- [[go/13. Web Services and APIs]] — you need to understand: `http.Handler`, request context via `r.Context()`, and how to structure a JSON API; this module shows how to add a persistence layer to that API

### Required Concepts

- **Context propagation** — `context.Context` carries deadlines and cancellation signals; every database call in a server must use the request context to avoid runaway queries when clients disconnect
- **Interfaces as contracts** — the repository pattern depends on defining a `Store` interface that handlers depend on; concrete implementations can then be swapped (real DB for tests, fake for unit tests)
- **Defer and cleanup** — `defer rows.Close()` and `defer tx.Rollback()` are the canonical cleanup patterns; misplacing or omitting them causes resource leaks

> [!TIP]
> If error wrapping from [[go/8. Error Handling]] feels shaky, review it now.
> Nearly every `database/sql` function returns an error, and wrapping them with context
> (`fmt.Errorf("get user %d: %w", id, err)`) is what makes debugging production failures tractable.

---

## Why This Matters

Almost every non-trivial service needs to persist state. Understanding Go's database layer means you can build services where:

- **Data survives restarts** — in-memory maps don't survive `os.Exit`; a relational database does
- **Concurrent requests share data safely** — the connection pool and transactions handle concurrent access correctly
- **Queries can be cancelled** — passing `r.Context()` to every DB call means a client disconnect or server shutdown cancels the in-flight query rather than letting it run to completion and waste resources

Concretely, mastery of this module enables you to:

- **Persist users, orders, and events** — any feature that requires reading or writing structured data across requests depends on what you learn here
- **Implement safe multi-step operations** — money transfers, inventory reservations, and order fulfillment require transactions that either fully succeed or fully roll back
- **Write testable persistence code** — the repository pattern (define an interface, inject it) lets you test handlers with a fast in-memory fake instead of a real database, making your test suite orders of magnitude faster

Without this module, the APIs you built in [[go/13. Web Services and APIs]] store all state in-memory — they lose everything on restart. This module is what turns a toy API into a real service.

---

## Historical Context

The `database/sql` package was part of Go's standard library from its earliest releases. Its design was influenced directly by the Java `java.sql` API and the Python DB-API 2.0 specification — both of which established the driver-registration pattern (a driver registers itself, the application only depends on the abstract interface).

Key moments:

- **2009** — Go open-sourced; `database/sql` present as a thin abstraction layer with no bundled drivers, requiring third-party packages to contribute concrete implementations
- **2011** — Russ Cox's `database/sql` rewrite establishes the connection pool model that remains today; `sql.DB` becomes explicitly documented as a long-lived pool, not a single connection
- **2016** — `context.Context` integration added (`QueryContext`, `ExecContext`, etc.) in Go 1.8; this was a significant API expansion that enabled query cancellation — essential for production servers
- **2019** — `sql.DB` connection pool control methods (`SetConnMaxIdleTime`) completed; the pool is now fully tunable without third-party wrappers
- **2019–present** — The ecosystem stratifies: raw `database/sql` for full control; `sqlx` for struct scanning convenience; `sqlc` for type-safe query generation from SQL; GORM/Ent for ORM-style development

The driver-registration model is a direct consequence of Go's import system: a blank import (`_ "github.com/lib/pq"`) runs the driver's `init()` function, which calls `sql.Register("postgres", &postgresDriver{})`. The application never imports the driver directly — it only calls `sql.Open("postgres", dsn)`. This keeps the application code independent of the driver implementation, which is the same separation of concerns that makes the repository pattern work.

---

## Core Concepts

### The database/sql Architecture

`database/sql` is a **thin abstraction layer** over database drivers. The package defines a `driver.Driver` interface that third-party packages implement. Your application code only ever imports `database/sql` and uses its public API; the driver is registered as a side effect of a blank import.

```go
import (
    "database/sql"
    _ "modernc.org/sqlite" // blank import: runs init(), registers "sqlite" driver
)

// sql.Open uses the registered "sqlite" driver
db, err := sql.Open("sqlite", "file:myapp.db?cache=shared")
```

The blank import `_ "modernc.org/sqlite"` triggers the package's `init()` function, which calls `sql.Register("sqlite", driver)`. The string `"sqlite"` is then the driver name you pass to `sql.Open`. You never call anything from `modernc.org/sqlite` directly — the `database/sql` package calls through the `driver.Driver` interface.

An alternative pure-Go SQLite driver uses CGo: `_ "github.com/mattn/go-sqlite3"` registers under the name `"sqlite3"`. `modernc.org/sqlite` is preferred when CGo is unavailable (e.g., cross-compilation, minimal Docker images). For PostgreSQL the most common driver is `_ "github.com/lib/pq"` (name `"postgres"`) or `_ "github.com/jackc/pgx/v5/stdlib"` (name `"pgx"`).

---

### sql.DB Is a Connection Pool

`sql.DB` is **not a single connection** — it is a **managed connection pool**. This is the single most important architectural fact about `database/sql`. Misunderstanding it leads to subtle and hard-to-debug bugs.

- The pool creates connections lazily as they are needed and reuses them across calls.
- Multiple goroutines can call methods on the same `*sql.DB` concurrently — it is safe for concurrent use.
- `sql.DB` is meant to be **long-lived**: create one at startup, pass it (or a repository wrapping it) to your handlers, and close it only when the process shuts down.
- Creating a new `sql.DB` per request is wrong — it defeats the pool, leaks connections, and is dramatically slower.

```go
// CORRECT: create once at startup, share across handlers
func main() {
    db, err := sql.Open("sqlite", "file:app.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close() // closes when main returns (process exit)

    // pass db to your handlers, repositories, etc.
    srv := &server{store: NewSQLStore(db)}
    http.ListenAndServe(":8080", srv.routes())
}
```

---

### Opening and Verifying a Connection

`sql.Open` is **lazy** — it validates the driver name and DSN format but does **not** establish a connection. The first actual connection is opened on the first query (or on `Ping`). This means `sql.Open` can succeed even if the database is unreachable.

Always call `db.PingContext` (or `db.Ping`) after `sql.Open` to verify connectivity at startup:

```go
db, err := sql.Open("sqlite", "file:app.db")
if err != nil {
    // driver name is wrong, or DSN is malformed
    log.Fatalf("sql.Open: %v", err)
}

// PingContext verifies connectivity — actually opens a connection
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
if err := db.PingContext(ctx); err != nil {
    log.Fatalf("db.Ping: %v", err)
}
log.Println("database connection pool ready")
```

---

### Querying — QueryContext, QueryRowContext, ExecContext

There are three query methods. Use the context-aware variants (`Context` suffix) in all server code.

| Method | Use for | Returns |
|--------|---------|---------|
| `QueryContext` | SELECT returning zero or more rows | `*sql.Rows, error` |
| `QueryRowContext` | SELECT expected to return exactly one row | `*sql.Row` |
| `ExecContext` | INSERT, UPDATE, DELETE, DDL | `sql.Result, error` |

```go
// ExecContext: INSERT with parameterized values
res, err := db.ExecContext(ctx,
    `INSERT INTO users (name, email) VALUES (?, ?)`,
    "Alice", "alice@example.com",
)
if err != nil {
    return fmt.Errorf("insert user: %w", err)
}
id, _ := res.LastInsertId() // SQLite; PostgreSQL uses RETURNING instead

// QueryRowContext: fetch a single row
var name string
err = db.QueryRowContext(ctx,
    `SELECT name FROM users WHERE id = ?`, id,
).Scan(&name)
if errors.Is(err, sql.ErrNoRows) {
    return fmt.Errorf("user %d not found", id)
}
if err != nil {
    return fmt.Errorf("get user %d: %w", id, err)
}
```

`sql.ErrNoRows` is the sentinel error returned by `QueryRowContext` when no row matches. Check for it explicitly with `errors.Is` rather than comparing the error string.

---

### Iterating Rows

`QueryContext` returns `*sql.Rows`. The iteration protocol has four required steps — skipping any one of them leaks resources or silently hides errors:

```go
// Full rows iteration protocol
rows, err := db.QueryContext(ctx, `SELECT id, name, email FROM users WHERE active = ?`, true)
if err != nil {
    return fmt.Errorf("query users: %w", err)
}
defer rows.Close() // Step 1: always defer Close immediately after checking err

var users []User
for rows.Next() { // Step 2: iterate
    var u User
    if err := rows.Scan(&u.ID, &u.Name, &u.Email); err != nil { // Step 3: scan
        return fmt.Errorf("scan user: %w", err)
    }
    users = append(users, u)
}
if err := rows.Err(); err != nil { // Step 4: check for iteration error
    return fmt.Errorf("rows iteration: %w", err)
}
return users, nil
```

`rows.Err()` must be checked **after** the loop — it reports errors that occurred during iteration (network errors, context cancellation). `rows.Next()` returns `false` on either exhaustion or error; checking only the loop exit condition misses the error case.

---

### Scanning into Structs and Handling NULLs

`rows.Scan` takes pointers. The scan destination types must be compatible with the column types. When a column is `NULL` in the database, scanning into a Go value type (like `string`) will fail with a runtime error. Handle NULLs with `sql.NullString`, `sql.NullInt64`, `sql.NullFloat64`, etc., or with pointer types.

```go
// Using sql.NullString for a nullable bio column
type User struct {
    ID    int64
    Name  string
    Bio   sql.NullString // valid=false means the column was NULL
}

rows, err := db.QueryContext(ctx, `SELECT id, name, bio FROM users`)
// ... (defer rows.Close, check err)
for rows.Next() {
    var u User
    if err := rows.Scan(&u.ID, &u.Name, &u.Bio); err != nil {
        return fmt.Errorf("scan: %w", err)
    }
    if u.Bio.Valid {
        fmt.Println("bio:", u.Bio.String)
    } else {
        fmt.Println("bio: (not set)")
    }
}

// Alternative: use a *string pointer — nil means NULL
type UserAlt struct {
    ID   int64
    Name string
    Bio  *string // nil if NULL
}
```

---

### Prepared Statements and Placeholder Syntax

Placeholder syntax differs by driver:

| Driver | Placeholder |
|--------|------------|
| SQLite (`modernc.org/sqlite`, `mattn/go-sqlite3`) | `?` |
| MySQL (`go-sql-driver/mysql`) | `?` |
| PostgreSQL (`lib/pq`, `pgx`) | `$1`, `$2`, … |

```go
// SQLite / MySQL style
rows, err := db.QueryContext(ctx,
    `SELECT id, name FROM products WHERE category = ? AND price < ?`,
    "electronics", 500,
)

// PostgreSQL style
rows, err = db.QueryContext(ctx,
    `SELECT id, name FROM products WHERE category = $1 AND price < $2`,
    "electronics", 500,
)
```

`db.PrepareContext` creates a prepared statement that can be reused across calls, avoiding re-parsing by the database on each execution. For a statement called many times in a loop, prepare once outside the loop:

```go
stmt, err := db.PrepareContext(ctx, `INSERT INTO events (type, payload) VALUES (?, ?)`)
if err != nil {
    return fmt.Errorf("prepare: %w", err)
}
defer stmt.Close()

for _, e := range events {
    if _, err := stmt.ExecContext(ctx, e.Type, e.Payload); err != nil {
        return fmt.Errorf("insert event %s: %w", e.Type, err)
    }
}
```

---

### Transactions

A transaction groups multiple SQL statements so they either all succeed (commit) or all fail (rollback). The `defer tx.Rollback()` safety pattern ensures the transaction is always rolled back if `Commit` is never called — including on panics.

```go
func transfer(ctx context.Context, db *sql.DB, fromID, toID int64, amount int) error {
    // BeginTx accepts transaction options including isolation level
    tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
    if err != nil {
        return fmt.Errorf("begin tx: %w", err)
    }
    // Safety pattern: Rollback is a no-op if Commit was already called
    defer tx.Rollback()

    // Debit from sender
    res, err := tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?`,
        amount, fromID, amount,
    )
    if err != nil {
        return fmt.Errorf("debit account %d: %w", fromID, err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("insufficient funds or account %d not found", fromID)
    }

    // Credit receiver
    if _, err = tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance + ? WHERE id = ?`,
        amount, toID,
    ); err != nil {
        return fmt.Errorf("credit account %d: %w", toID, err)
    }

    // Commit — after this, defer tx.Rollback() is a no-op
    if err := tx.Commit(); err != nil {
        return fmt.Errorf("commit transfer: %w", err)
    }
    return nil
}
```

`sql.TxOptions` lets you specify the isolation level. Common levels: `sql.LevelDefault`, `sql.LevelReadCommitted`, `sql.LevelRepeatableRead`, `sql.LevelSerializable`. Use `LevelSerializable` for operations that must be atomic and require the strictest consistency (like the balance transfer above). Use `LevelReadCommitted` for most read-heavy workloads where phantom reads are acceptable.

---

### Connection Pool Tuning

Four methods control pool behavior. Setting them is important for production services:

```go
db.SetMaxOpenConns(25)               // max total open connections (default: unlimited)
db.SetMaxIdleConns(10)               // max idle connections in pool (default: 2)
db.SetConnMaxLifetime(30 * time.Minute) // max time a connection can be reused
db.SetConnMaxIdleTime(5 * time.Minute)  // max time a connection can sit idle
```

- **`SetMaxOpenConns`** — prevents overwhelming the database. Most databases have hard connection limits (PostgreSQL default: 100). Set this below the database limit, accounting for multiple app instances.
- **`SetMaxIdleConns`** — connections in the idle pool are reused immediately, avoiding the latency of establishing a new connection. Set it equal to or slightly below `MaxOpenConns` for connection-heavy workloads.
- **`SetConnMaxLifetime`** — forces periodic connection recycling to avoid issues with firewalls that silently drop idle connections and with database restarts.
- **`SetConnMaxIdleTime`** — closes connections that have been idle longer than this duration, keeping the pool size from ballooning during traffic spikes.

---

### SQL Injection and Parameterized Queries

SQL injection is the most critical database security issue. It occurs when user-controlled input is concatenated directly into a SQL string. The database then executes the attacker's injected SQL.

```go
// WRONG — SQL injection vulnerability
// If username is "admin'--", this drops the password check entirely
userInput := r.FormValue("username")
rows, err := db.QueryContext(ctx,
    "SELECT id FROM users WHERE username = '"+userInput+"'",  // NEVER do this
)

// RIGHT — parameterized query: the driver sends value as a separate parameter
// The database treats it as data, never as SQL syntax
rows, err = db.QueryContext(ctx,
    `SELECT id FROM users WHERE username = ?`,
    userInput, // passed as a bind parameter, not interpolated into SQL
)
```

Parameterized queries are non-negotiable. The `database/sql` package's placeholder system exists precisely for this: when you pass values as arguments to `QueryContext`, `ExecContext`, or `Scan`, the driver sends them as binary parameters over the wire — the database server never concatenates them into SQL. There is no escape function that is a safe alternative; use parameters always.

---

### Migrations

A migration is a versioned SQL script that transforms the database schema from one version to the next. Migrations solve the problem of keeping the database schema in sync with the application code across environments (dev, staging, production) and across time (as the schema evolves).

The concept:

```sql
-- migrations/0001_create_users.sql (up migration)
CREATE TABLE IF NOT EXISTS users (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL,
    email   TEXT    NOT NULL UNIQUE,
    bio     TEXT,           -- nullable
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- migrations/0001_create_users_down.sql (down migration — reverses the up)
DROP TABLE IF EXISTS users;
```

Migration tools track which migrations have been applied (typically in a `schema_migrations` table) and apply only the unapplied ones. Two commonly used Go tools:

- **[golang-migrate/migrate](https://github.com/golang-migrate/migrate)** — runs SQL migration files; has a Go library for embedding and running migrations at startup; supports up/down migrations
- **[pressly/goose](https://github.com/pressly/goose)** — similar approach with slightly different conventions; supports Go-language migration files for complex transformations

Running migrations at startup (rather than manually) ensures every deployed instance has an up-to-date schema:

```go
// Example with golang-migrate (illustrative — see package docs for current API)
m, err := migrate.New("file://migrations", dsn)
if err != nil {
    log.Fatalf("migrate.New: %v", err)
}
if err := m.Up(); err != nil && !errors.Is(err, migrate.ErrNoChange) {
    log.Fatalf("migrate up: %v", err)
}
```

---

### The Repository Pattern

The repository pattern separates "how do I retrieve and store domain objects" from "what does the application do with them." You define a storage interface, implement it over `database/sql`, and inject the interface into your HTTP handlers (from [[go/13. Web Services and APIs]]). Handlers depend only on the interface — they are unaware of whether the backing store is SQLite, PostgreSQL, or an in-memory map.

This ties directly to [[go/6. Methods and Interfaces]]: the interface is the contract; the SQL implementation is one concrete fulfillment of that contract.

```go
// store.go — the storage interface (domain layer)
type UserStore interface {
    GetUser(ctx context.Context, id int64) (User, error)
    CreateUser(ctx context.Context, name, email string) (int64, error)
    ListUsers(ctx context.Context) ([]User, error)
    DeleteUser(ctx context.Context, id int64) error
}

// User is a plain domain struct — no SQL tags, no ORM annotations
type User struct {
    ID    int64
    Name  string
    Email string
    Bio   *string // pointer: nil means "not set" (was NULL)
}
```

```go
// sql_store.go — the SQL implementation
type SQLUserStore struct {
    db *sql.DB
}

func NewSQLUserStore(db *sql.DB) *SQLUserStore {
    return &SQLUserStore{db: db}
}

// GetUser satisfies UserStore. Errors are wrapped with context.
func (s *SQLUserStore) GetUser(ctx context.Context, id int64) (User, error) {
    var u User
    err := s.db.QueryRowContext(ctx,
        `SELECT id, name, email, bio FROM users WHERE id = ?`, id,
    ).Scan(&u.ID, &u.Name, &u.Email, &u.Bio)
    if errors.Is(err, sql.ErrNoRows) {
        return User{}, fmt.Errorf("user %d: %w", id, ErrNotFound)
    }
    if err != nil {
        return User{}, fmt.Errorf("get user %d: %w", id, err)
    }
    return u, nil
}

// ErrNotFound is a sentinel the caller can check with errors.Is
var ErrNotFound = errors.New("not found")
```

```go
// handler.go — handler depends on the interface, not the implementation
type server struct {
    store UserStore // interface, not *SQLUserStore
}

func (s *server) handleGetUser(w http.ResponseWriter, r *http.Request) {
    id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
    user, err := s.store.GetUser(r.Context(), id)
    if errors.Is(err, ErrNotFound) {
        http.Error(w, "not found", http.StatusNotFound)
        return
    }
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

In tests, swap the `SQLUserStore` for an in-memory implementation of `UserStore` — no database needed, tests run in microseconds.

---

### database/sql vs sqlx, sqlc, and GORM

Raw `database/sql` gives you full control but requires manual scanning. The ecosystem offers three popular alternatives:

| Tool | What it adds | When to use |
|------|-------------|-------------|
| **[sqlx](https://github.com/jmoiron/sqlx)** | `StructScan`, `Get`, `Select` — scans rows directly into structs using field tags; wraps `database/sql`, not a replacement | When manual scanning is tedious but you want to keep SQL visible and in control |
| **[sqlc](https://sqlc.dev)** | Generates type-safe Go code from SQL queries at build time; you write SQL, `sqlc` generates Go functions and structs | When you want compile-time type safety for every query; recommended for new projects |
| **[GORM](https://gorm.io)** | Full ORM: struct-to-table mapping, `Find`, `Create`, `Save`, associations, migrations | When you want rapid prototyping or an ORM-style API; carries significant abstraction cost; harder to debug generated SQL |

For a two-years-professional audience: prefer **`sqlc`** for new projects (type-safe, no magic, SQL is first-class), **`sqlx`** when adding convenience to existing `database/sql` code, and avoid **GORM** in performance-critical or complex query paths where the generated SQL is hard to predict.

---

### How the Concepts Fit Together

```
Application startup
        │
        ▼
  sql.Open (lazy)  ──►  db.PingContext (verify)  ──►  Pool tuning
        │                                                (SetMaxOpenConns, etc.)
        ▼
  Repository (implements UserStore interface)
        │
        ├─ Read path:  QueryContext → rows.Next/Scan/Err/Close
        │
        ├─ Write path: ExecContext (parameterized — no injection)
        │
        └─ Multi-step: BeginTx → ExecContext × N → Commit
                            └─ defer tx.Rollback() (safety net)
        │
        ▼
  HTTP Handler (depends on UserStore interface, not SQLUserStore)
        │
        └─ Pass r.Context() to every DB call (cancellation propagation)
```

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Not checking `rows.Err()` after the loop**
>
> `rows.Next()` returns `false` when iteration is complete OR when an error occurs during iteration. If you only check the loop body and ignore `rows.Err()`, you will silently return a partial result set when the database connection drops mid-query.
>
> **Wrong:**
> ```go
> for rows.Next() {
>     var u User
>     rows.Scan(&u.ID, &u.Name)
>     users = append(users, u)
> }
> // rows.Err() never checked — silent data loss on network errors
> return users, nil
> ```
>
> **Right:**
> ```go
> for rows.Next() {
>     var u User
>     if err := rows.Scan(&u.ID, &u.Name); err != nil {
>         return nil, fmt.Errorf("scan: %w", err)
>     }
>     users = append(users, u)
> }
> if err := rows.Err(); err != nil {
>     return nil, fmt.Errorf("rows: %w", err)
> }
> return users, nil
> ```
>
> **Why this matters:** In production, database connections drop. Without `rows.Err()`, your service returns truncated data without the caller knowing.

> [!WARNING]
> **Mistake 2: Creating a new `sql.DB` per request**
>
> `sql.DB` is a connection pool. Creating one per HTTP request means creating a new pool (with new connections) on every request. This is extremely expensive and leaks connections if the pool is not closed promptly.
>
> **Wrong:**
> ```go
> func (s *server) handleGetUser(w http.ResponseWriter, r *http.Request) {
>     db, _ := sql.Open("sqlite", "file:app.db") // WRONG: new pool per request
>     defer db.Close()
>     // ...
> }
> ```
>
> **Right:** Create `*sql.DB` once at startup and inject it into the server struct. See the repository pattern example above.

> [!WARNING]
> **Mistake 3: Using string concatenation for query parameters**
>
> Any user-supplied value concatenated into a SQL string is a SQL injection risk. There are no exceptions — not even if you "sanitize" the input yourself.
>
> **Wrong:**
> ```go
> query := "SELECT * FROM users WHERE name = '" + name + "'"
> rows, _ := db.QueryContext(ctx, query)
> ```
>
> **Right:**
> ```go
> rows, _ := db.QueryContext(ctx, `SELECT * FROM users WHERE name = ?`, name)
> ```

> [!WARNING]
> **Mistake 4: Not deferring `tx.Rollback()` before any error returns**
>
> If you call `db.BeginTx` and then return early on an error without calling `tx.Rollback()`, the transaction remains open until the database times it out — holding locks and wasting a connection.
>
> **Wrong:**
> ```go
> tx, _ := db.BeginTx(ctx, nil)
> if _, err := tx.ExecContext(ctx, ...); err != nil {
>     return err // transaction leaked — never rolled back explicitly
> }
> tx.Commit()
> ```
>
> **Right:** `defer tx.Rollback()` immediately after `BeginTx`. Rollback after Commit is a no-op.

**Other pitfalls:**

- **`sql.Open` success does not mean connectivity** — always call `db.PingContext` at startup; `sql.Open` only validates the driver name and DSN format
- **Forgetting `defer rows.Close()`** — if `rows.Next()` exits the loop early (via `break` or early `return`), the rows are not automatically closed; an explicit defer is required

---

## Mental Models

### Mental Model 1: sql.DB as a Staffing Agency

Think of `sql.DB` as a staffing agency that manages a pool of workers (connections). When your code needs a connection, it asks the agency — the agency either assigns an idle worker or hires a new one (up to `MaxOpenConns`). When the call finishes, the worker goes back to the pool (idle). The agency handles hiring, firing, and vacation (idle timeout, lifetime). Your code never manages individual connections — only the agency does.

This model explains why you should not create `sql.DB` per request (that's like creating a new agency per task), why concurrent calls are safe (the agency has many workers), and why pool tuning matters (too few workers → queue builds up; too many → overwhelms the database).

This model breaks down when thinking about transactions — a transaction holds one specific connection for its duration, not an arbitrary one from the pool. Within a transaction, all calls go to the same connection.

### Mental Model 2: Transactions as a Checkpoint-and-Rollback Savepoint

Think of a transaction like an editor's "track changes" mode: every modification is recorded but not committed to the final document. `Commit` accepts all changes; `Rollback` rejects them all. The database enforces this atomically — it is impossible for a partial transaction to be visible to other connections.

The `defer tx.Rollback()` pattern then makes sense: you're saying "if we ever exit this function without explicitly accepting the changes (Commit), reject everything." The rollback being a no-op after commit is the analog of closing "track changes" normally — there's nothing left to reject.

### Mental Model 3: The Repository Interface as a Plug

The `UserStore` interface is a plug shape. Any type with the right methods fits the plug. The HTTP handler is a lamp — it only knows how to accept power through the plug shape. Whether the power comes from the wall (SQLite), a generator (PostgreSQL), or a battery (in-memory fake) is irrelevant to the lamp. This is dependency injection through interfaces, the principle from [[go/6. Methods and Interfaces]] applied to persistence.

> [!NOTE]
> Use Mental Model 1 (staffing agency) when reasoning about concurrency and pool tuning.
> Use Mental Model 2 (track changes) when reasoning about transactions and rollback safety.
> Use Mental Model 3 (plug) when designing the repository interface and writing tests.

---

## Practical Examples

### Example 1: Open, Migrate, Query _(Basic)_

**Scenario:** Starting up a service — open the database, verify connectivity, create a table if it doesn't exist, and query a count.

**Goal:** Show the full startup sequence in one runnable program.

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "time"

    _ "modernc.org/sqlite" // blank import: registers the "sqlite" driver
)

func main() {
    // sql.Open is lazy — does NOT connect yet
    db, err := sql.Open("sqlite", "file:example.db?_journal=WAL")
    if err != nil {
        log.Fatalf("sql.Open: %v", err)
    }
    defer db.Close()

    // Tune the pool before first use
    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(30 * time.Minute)
    db.SetConnMaxIdleTime(5 * time.Minute)

    // PingContext actually opens a connection — verify connectivity at startup
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    if err := db.PingContext(ctx); err != nil {
        log.Fatalf("db.Ping: %v", err)
    }
    log.Println("connected to database")

    // Simple inline migration — for production use golang-migrate or goose
    _, err = db.ExecContext(context.Background(), `
        CREATE TABLE IF NOT EXISTS notes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            body    TEXT
        )
    `)
    if err != nil {
        log.Fatalf("create table: %v", err)
    }

    // Insert a row
    res, err := db.ExecContext(context.Background(),
        `INSERT INTO notes (title, body) VALUES (?, ?)`,
        "First note", "Hello, database/sql!",
    )
    if err != nil {
        log.Fatalf("insert: %v", err)
    }
    id, _ := res.LastInsertId()
    fmt.Printf("inserted note id=%d\n", id)

    // Count rows
    var count int
    if err := db.QueryRowContext(context.Background(),
        `SELECT COUNT(*) FROM notes`,
    ).Scan(&count); err != nil {
        log.Fatalf("count: %v", err)
    }
    fmt.Printf("total notes: %d\n", count)
}
```

**What to notice:** `sql.Open` does not fail even if the file does not exist (SQLite creates it). `PingContext` is where real connectivity is verified. The pool is tuned before first use. Inline migrations like the `CREATE TABLE IF NOT EXISTS` shown here are fine for simple cases; for production use a migration tool.

---

### Example 2: Full CRUD Repository _(Intermediate)_

**Scenario:** Implementing a `NoteStore` interface over `database/sql`.

**Goal:** Show the complete repository pattern — interface, SQL implementation, NULL handling, and all four CRUD operations.

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

// ErrNotFound is returned when a requested record does not exist.
var ErrNotFound = errors.New("not found")

// Note is the domain struct. Body is nullable (*string nil = no body).
type Note struct {
    ID    int64
    Title string
    Body  *string
}

// NoteStore defines the persistence interface — handlers depend on this.
type NoteStore interface {
    Create(ctx context.Context, title string, body *string) (int64, error)
    Get(ctx context.Context, id int64) (Note, error)
    List(ctx context.Context) ([]Note, error)
    Delete(ctx context.Context, id int64) error
}

// SQLNoteStore implements NoteStore over database/sql.
type SQLNoteStore struct {
    db *sql.DB
}

func NewSQLNoteStore(db *sql.DB) *SQLNoteStore { return &SQLNoteStore{db: db} }

func (s *SQLNoteStore) Create(ctx context.Context, title string, body *string) (int64, error) {
    res, err := s.db.ExecContext(ctx,
        `INSERT INTO notes (title, body) VALUES (?, ?)`, title, body,
    )
    if err != nil {
        return 0, fmt.Errorf("create note: %w", err)
    }
    id, err := res.LastInsertId()
    if err != nil {
        return 0, fmt.Errorf("last insert id: %w", err)
    }
    return id, nil
}

func (s *SQLNoteStore) Get(ctx context.Context, id int64) (Note, error) {
    var n Note
    err := s.db.QueryRowContext(ctx,
        `SELECT id, title, body FROM notes WHERE id = ?`, id,
    ).Scan(&n.ID, &n.Title, &n.Body) // *string scans NULL as nil
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
    defer rows.Close() // always defer Close after checking err

    var notes []Note
    for rows.Next() {
        var n Note
        if err := rows.Scan(&n.ID, &n.Title, &n.Body); err != nil {
            return nil, fmt.Errorf("scan note: %w", err)
        }
        notes = append(notes, n)
    }
    if err := rows.Err(); err != nil { // check iteration errors
        return nil, fmt.Errorf("notes iteration: %w", err)
    }
    return notes, nil
}

func (s *SQLNoteStore) Delete(ctx context.Context, id int64) error {
    res, err := s.db.ExecContext(ctx, `DELETE FROM notes WHERE id = ?`, id)
    if err != nil {
        return fmt.Errorf("delete note %d: %w", id, err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("note %d: %w", id, ErrNotFound)
    }
    return nil
}

func main() {
    db, err := sql.Open("sqlite", "file::memory:?cache=shared")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    _, err = db.ExecContext(context.Background(), `
        CREATE TABLE notes (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body  TEXT
        )`)
    if err != nil {
        log.Fatal(err)
    }

    store := NewSQLNoteStore(db)
    ctx := context.Background()

    // Create with and without body
    body := "Hello, world!"
    id1, _ := store.Create(ctx, "First", &body)
    id2, _ := store.Create(ctx, "Second", nil) // body is NULL

    // Get and show NULL handling
    n1, _ := store.Get(ctx, id1)
    n2, _ := store.Get(ctx, id2)
    fmt.Printf("Note %d: %q body=%v\n", n1.ID, n1.Title, n1.Body)
    fmt.Printf("Note %d: %q body=%v\n", n2.ID, n2.Title, n2.Body)

    // List
    notes, _ := store.List(ctx)
    fmt.Printf("total: %d notes\n", len(notes))

    // Delete
    if err := store.Delete(ctx, id1); err != nil {
        log.Fatal(err)
    }
    fmt.Printf("after delete: %d notes\n", func() int { n, _ := store.List(ctx); return len(n) }())
}
```

**What to notice:** `*string` as the `body` field handles NULL naturally — `nil` means no body set, a non-nil pointer contains the text. The `ErrNotFound` sentinel is wrapped into the error so callers can use `errors.Is`. The handler using this store would only need `NoteStore` — the `SQLNoteStore` concrete type can stay private to the persistence package.

---

### Example 3: Transaction with Rollback Safety _(Applied)_

**Scenario:** A bank transfer that must debit one account and credit another atomically.

**Goal:** Show the `BeginTx` / `defer tx.Rollback()` / `Commit` pattern and verify the rollback fires on failure.

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
    // Rollback is a no-op if Commit was called; safe to always defer
    defer tx.Rollback()

    // Debit — only succeeds if balance is sufficient
    res, err := tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?`,
        amount, fromID, amount,
    )
    if err != nil {
        return fmt.Errorf("debit: %w", err)
    }
    if n, _ := res.RowsAffected(); n == 0 {
        return fmt.Errorf("account %d: %w", fromID, ErrInsufficientFunds)
    }

    // Credit
    if _, err = tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance + ? WHERE id = ?`, amount, toID,
    ); err != nil {
        return fmt.Errorf("credit: %w", err)
    }

    return tx.Commit() // defer Rollback becomes a no-op
}

func main() {
    db, _ := sql.Open("sqlite", "file::memory:")
    defer db.Close()

    db.ExecContext(context.Background(), `CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)`)
    db.ExecContext(context.Background(), `INSERT INTO accounts VALUES (1, 100), (2, 50)`)

    ctx := context.Background()

    // Successful transfer: 30 from account 1 → account 2
    if err := transfer(ctx, db, 1, 2, 30); err != nil {
        log.Fatalf("transfer failed: %v", err)
    }
    printBalances(ctx, db)

    // Failing transfer: account 2 only has 80, can't send 100
    err := transfer(ctx, db, 2, 1, 100)
    fmt.Printf("expected error: %v\n", err)
    fmt.Printf("is ErrInsufficientFunds: %v\n", errors.Is(err, ErrInsufficientFunds))
    printBalances(ctx, db) // balances unchanged — rollback fired
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
```

**What to notice:** After the failed transfer, balances are unchanged because `defer tx.Rollback()` fired when `transfer` returned the `ErrInsufficientFunds` error (before `Commit` was called). The sentinel error `ErrInsufficientFunds` is checkable with `errors.Is` even after being wrapped.

---

### Example 4: Injecting a Fake Store in Tests _(Edge Case)_

**Scenario:** Testing an HTTP handler that depends on `NoteStore` without a real database.

```go
// fakestore_test.go
package main

import (
    "context"
    "errors"
    "sync"
)

// FakeNoteStore is an in-memory NoteStore for testing — no database required.
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
    if !ok { return Note{}, fmt.Errorf("note %d: %w", id, ErrNotFound) }
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
```

**Why this is important:** `FakeNoteStore` satisfies `NoteStore` because it has all four methods with matching signatures — Go's structural typing makes this automatic. The test uses `FakeNoteStore`; production uses `SQLNoteStore`. Neither change touches the handler. Handlers test at microsecond speed. This is the payoff of the repository pattern.

---

## Related Concepts

Within this topic:

- [[go/6. Methods and Interfaces]] — the repository pattern is an application of interface-based design; defining `UserStore` as an interface and injecting it is the same technique you learned there applied to persistence
- [[go/8. Error Handling]] — every database operation returns an error; `sql.ErrNoRows`, wrapping with `%w`, and `errors.Is` for sentinel errors are used throughout this module
- [[go/13. Web Services and APIs]] — this module adds a persistence layer to the HTTP APIs built there; the handler code in Example 4 connects directly to the `net/http` handler pattern from that module

In other topics:

- [[concurrency]] — `database/sql` connection pools manage concurrency internally; transactions acquire single connections; understanding Go's concurrency model helps reason about pool saturation and lock contention under concurrent load
- [[memory-management]] — connection pool sizing affects memory; each idle connection holds OS-level resources; understanding how the pool interacts with the GC is relevant for high-throughput services

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Schema Setup and Basic Insert/Query** _(Easy)_
>
> Write a Go program that opens a SQLite in-memory database, creates a `tasks` table, inserts three rows, and queries them back using `QueryContext` with the full `rows.Next/Scan/Err/Close` protocol.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-schema-setup-and-basic-insertquery--easy--1-pt)

The exercises cover: basic insert/query, a full CRUD repository, NULL handling, a bank-transfer transaction, SQL injection / safe queries, and a full repository wired to an HTTP handler.

---

## Test

When you feel ready, take the self-assessment: [TEST.md](./TEST.md)

**Test overview:**
- Section 1: Recall (5 questions, 1 pt each)
- Section 2: Conceptual Understanding (3 questions, 2 pts each)
- Section 3: Applied / Practical (2 questions, 3 pts each)
- Section 4: Scenario / Debugging (1 question, 3 pts)
- Section 5: Discussion (1 question, 2 pts)
- Section 6: Bonus Challenge (1 question, 5 pts bonus)

**Passing:** ≥ 70% of non-bonus points (≥ 15/22). Aim for ≥ 80% (≥ 18/22).

---

## Projects

See the topic-level [PROJECTS.md](../PROJECTS.md) for project ideas.

**Recommended project after this module:**
Notes REST API with SQLite Persistence — build a full CRUD JSON API for notes using `net/http` (from [[go/13. Web Services and APIs]]), back it with a SQLite database using the repository pattern from this module, add a migration on startup, and write unit tests using a `FakeNoteStore`. This exercises every concept from both modules together.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[pkg.go.dev/database/sql](https://pkg.go.dev/database/sql)** — The official Go standard library documentation for `database/sql`; read the package-level documentation carefully — it explicitly documents that `sql.DB` is a pool, describes all four pool tuning methods, and covers `NullString` and related types
2. **[Accessing relational databases — go.dev/doc/database](https://go.dev/doc/database/)** — The official Go documentation guide for `database/sql`; covers opening a database, executing queries, using transactions, and avoiding SQL injection; more narrative than the API reference
3. **[Tutorial: Accessing a relational database — go.dev](https://go.dev/doc/tutorial/database-access)** — Official step-by-step tutorial that walks through creating a MySQL-backed Go program; the driver and placeholder syntax differ from SQLite but the `database/sql` API is identical
4. **[Managing connections — go.dev/doc/database/manage-connections](https://go.dev/doc/database/manage-connections)** — Official documentation specifically on connection pool tuning (`SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`, `SetConnMaxIdleTime`); explains when and why to set each parameter

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 14

**What I covered today:**
- Read the Overview and Why This Matters sections
- Worked through Core Concepts up to (concept name here)

**What clicked:**
- _Something that made sense_

**What's still unclear:**
- _Something that's still fuzzy — add to QUESTIONS.md_

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

**Test score:** _Not taken yet_

---

_Add new entries above this line._
