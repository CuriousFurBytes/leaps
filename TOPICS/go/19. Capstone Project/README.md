# Module 19: Capstone Project

[← Module 18: Build, Tooling, and Deployment](../18.%20Build%2C%20Tooling%2C%20and%20Deployment/) | [Topic Home](../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-capstone-purple)
![Time](https://img.shields.io/badge/time-40--80h-red)

---

## Table of Contents

1. [What You'll Build](#what-youll-build)
2. [How This Module Works](#how-this-module-works)
3. [Learning Goals](#learning-goals)
4. [Prerequisites](#prerequisites)
5. [Functional Requirements](#functional-requirements)
6. [Non-Functional Requirements](#non-functional-requirements)
7. [Suggested Architecture](#suggested-architecture)
8. [Milestones](#milestones)
9. [Acceptance Criteria](#acceptance-criteria)
10. [Help / Getting Unstuck](#help--getting-unstuck)
11. [Going Further](#going-further)
12. [Document Your Work](#document-your-work)
13. [Self-Assessment Rubric](#self-assessment-rubric)
14. [Learning Journal](#learning-journal)

---

## What You'll Build

This is the capstone module for the Go topic. You will build and ship a real, production-ready Go service. There is no lecture here. There are no worked examples to follow step-by-step. You design the architecture, write the code, run the tests, and ship the binary — applying everything from all nineteen preceding modules.

### Primary Brief — URL Shortener Service

**Recommendation:** Build a URL shortener service. This is a well-understood, production-relevant problem domain that requires you to exercise the full breadth of Go skills you have developed.

**What a real URL shortener looks like:**

A user submits a long URL (`https://www.example.com/very/long/path?with=query`). The service generates a short code (e.g., `xK9mP2`), stores the mapping, and returns the short URL (`https://short.example.com/xK9mP2`). Anyone who visits `https://short.example.com/xK9mP2` is redirected to the original URL. The service tracks how many times each short URL has been visited (hit count). This is the same fundamental design used by bit.ly, tinyurl.com, and similar services.

Your implementation is a backend HTTP JSON API with the following core operations:
- `POST /shorten` — accepts a long URL, returns a short code and the full short URL
- `GET /:code` — redirects to the original URL (HTTP 302), increments the hit counter
- `GET /api/stats/:code` — returns JSON with the original URL, short code, creation time, and hit count
- `DELETE /api/:code` — removes a short URL from the store

The service persists data across restarts using `database/sql` with SQLite (or Postgres — your choice). It emits structured logs with `log/slog`, shuts down gracefully on SIGINT/SIGTERM, reads configuration from flags and environment variables, and ships with a multi-stage Dockerfile and a CI workflow.

### Alternative Briefs

If the URL shortener does not interest you, choose one of these. All functional and non-functional requirements below apply equally — you are choosing a different domain, not different constraints.

**Alternative A — Task and Notes REST API** — Full CRUD for tasks with title, body, status (`pending`, `in-progress`, `done`), and priority. SQL storage. Filter by status and priority. No auth — use `X-User-ID` header to identify callers.

**Alternative B — Webhook Job Runner** — Accept webhook payloads, queue them, process with N worker goroutines. Store each job in SQL with status (`queued`, `running`, `done`, `failed`) and timestamps. Expose a status query endpoint.

**Alternative C — System Metrics Collector** — At a configurable interval, collect basic host metrics (memory, disk via `/proc` or `os/exec`) and store snapshots in SQL. HTTP API to query last N snapshots and averages over a time range. Linux-specific; note this in your README.

---

## How This Module Works

> [!IMPORTANT]
> **You build it. The help sections exist only to unblock you — not to do the work for you.**
>
> AGENTS.md §5 is explicit: "Let the learner drive. Provide scaffolding, milestones, and acceptance
> criteria, but do not hand over a complete copy-paste solution that removes the work. The help
> sections exist so a stuck learner can move forward on their own — not so they can skip the build."
>
> This module contains no complete solution. It contains staged hints per milestone, function and
> interface signatures, and architecture guidance. When you are stuck, open one hint at a time.
> Use the minimum hint that gets you unblocked, then close it and keep building.

The structure of this module is:

1. **Read the brief and choose your project.** Do this now.
2. **Work through the milestones in order.** Each milestone has acceptance criteria that tell you when you are done with that stage. Do not move to the next milestone until the current one is complete and passing.
3. **When you are stuck**, go to the [Help / Getting Unstuck](#help--getting-unstuck) section. Each milestone has three staged hints. Open only as many as you need.
4. **Test as you go.** Do not leave testing to the end. Write tests for each layer as you build it.
5. **Record your work** in the topic [PROJECTS.md](../PROJECTS.md) using the Project Attempt Template when you are done.

There is intentionally no complete reference implementation available. This is a feature, not an oversight. Synthesizing knowledge under your own power — without a safety net — is what transforms a student into a practitioner.

---

## Learning Goals

By completing this project, you will demonstrate that you can:

1. Design and implement a production-ready HTTP JSON service in Go from scratch
2. Model a data layer with clean interfaces and implement it against a real SQL database
3. Apply `context` for request-scoped cancellation, timeouts, and deadline propagation
4. Design structured error types that map cleanly to HTTP status codes
5. Write a test suite including table-driven unit tests and `httptest`-based integration tests
6. Configure a service from environment variables and command-line flags
7. Implement graceful shutdown that completes in-flight requests and flushes resources
8. Containerize the service with a multi-stage Dockerfile that produces a minimal image
9. Set up a CI workflow that builds, tests, lints, and publishes a release binary
10. Explain every design decision you made and the tradeoffs you accepted

---

## Prerequisites

This module requires all prior modules (0–18). The following modules are especially load-bearing for this project:

| Module | Why it is critical here |
|--------|------------------------|
| [[go/13. Web Services and APIs]] | HTTP handler design, routing with the 1.22 `http.ServeMux`, JSON encoding/decoding, middleware |
| [[go/14. Databases and Persistence]] | `database/sql`, `database/sql/driver`, migrations, repository pattern, transactions |
| [[go/12. Advanced Concurrency Patterns]] | `context` propagation, graceful shutdown with `context.WithCancel`, timeout middleware |
| [[go/11. Testing and Benchmarking]] | Table-driven tests, `httptest`, coverage, test helpers |
| [[go/8. Error Handling]] | Structured errors, `fmt.Errorf` wrapping, custom error types, mapping errors to HTTP status codes |
| [[go/18. Build, Tooling, and Deployment]] | Multi-stage Dockerfile, CI/CD with GitHub Actions, `goreleaser`, linting |
| [[go/9. Concurrency]] | Goroutines for background workers, `sync.WaitGroup`, graceful shutdown patterns |
| [[go/6. Methods and Interfaces]] | Interface-driven store design, dependency injection via constructor functions |

> [!TIP]
> If a milestone is blocking you and the hint does not fully unblock you, go back to the
> prerequisite module listed next to the hint. Read the relevant section, then return here.
> This is the expected workflow — it is not a sign of failure.

---

## Functional Requirements

All requirements apply to every brief. Where brief-specific, the URL shortener version is shown.

1. **HTTP API with the Go 1.22 router** — `net/http` with Go 1.22 pattern-matching `http.ServeMux`. No third-party router. At minimum: `POST` (create), `GET` (read/redirect), `GET` (stats/list), `DELETE`.

2. **Persistence via `database/sql`** — SQLite (`modernc.org/sqlite`, pure Go, no CGO) or Postgres. All queries use parameterized statements — no raw user input in SQL strings.

3. **`context` throughout** — Every store method and HTTP handler accepts `context.Context`. Set a per-request timeout in middleware using `context.WithTimeout`.

4. **Structured error types** — At least `NotFoundError`, `ValidationError`, `ConflictError`. A central `writeError` function maps them to 404/400/409/500.

5. **Table-driven tests + `httptest`** — At least one table-driven unit test for the store and at least one `httptest`-based integration test per handler.

6. **Config from flags and env vars** — `flag` package for flags; env vars (`PORT`, `DATABASE_URL`) override flags. A `Config` struct holds all configuration.

7. **Structured logging with `log/slog`** — All log output through `log/slog`. JSON handler in production. Access logs include method, path, status, duration.

8. **Graceful shutdown** — SIGINT/SIGTERM → stop accepting → wait for in-flight requests → close DB → exit 0.

9. **Multi-stage Dockerfile** — Builder stage compiles; runtime stage (distroless or alpine) contains only the binary.

10. **CI workflow** — GitHub Actions: `go vet`, race-enabled `go test`, linter, binary build on every push; release artifact on tagged push.

---

## Non-Functional Requirements

- No panics in production code paths (only `init()` for unrecoverable config errors)
- No global mutable state — all shared state in structs, injected via constructors
- All error returns handled — `go vet` and `errcheck` must pass
- `go build ./...` and `go test -race ./...` must succeed with no failures
- Docker image must start and serve requests
- At least 8 Go topic modules demonstrably used; documented in [PROJECTS.md](../PROJECTS.md)
- Project `README.md` covers: what it does, build, run, test, and at least three design decisions

---

## Suggested Architecture

You are not required to follow this architecture exactly — these are recommendations, not constraints. If you have a different architecture in mind, explain it in your project README.

### Package Layout

```text
myshortener/          ← module root (go mod init github.com/you/myshortener)
├── cmd/
│   └── server/
│       └── main.go   ← entry point: parse config, wire dependencies, start server
├── internal/
│   ├── api/
│   │   ├── handler.go      ← HTTP handlers (depends on store via interface)
│   │   ├── handler_test.go ← httptest-based integration tests
│   │   ├── middleware.go   ← logging, timeout, recovery middleware
│   │   └── router.go      ← route registration using http.ServeMux
│   ├── store/
│   │   ├── store.go        ← Store interface definition
│   │   ├── sqlite.go       ← SQLite implementation
│   │   ├── sqlite_test.go  ← table-driven unit tests for the store
│   │   └── migrations/
│   │       └── 001_init.sql
│   └── config/
│       └── config.go       ← Config struct, flag and env var parsing
├── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── .goreleaser.yml       ← optional, for release automation
├── go.mod
├── go.sum
└── README.md             ← your project README (not this leaps file)
```

### Key Interfaces

Define these in `internal/store/store.go`. Only signatures are shown here — implementations are yours to write.

```go
// internal/store/store.go — data model and persistence interface
type URLRecord struct {
    Code      string
    LongURL   string
    CreatedAt time.Time
    HitCount  int64
}

type Store interface {
    Create(ctx context.Context, record URLRecord) error   // ConflictError if code exists
    Get(ctx context.Context, code string) (URLRecord, error) // NotFoundError if missing
    IncrementHits(ctx context.Context, code string) error
    Delete(ctx context.Context, code string) error        // NotFoundError if missing
    Close() error
}

// internal/store/errors.go — custom error types
type NotFoundError  struct{ Resource, ID string }
type ValidationError struct{ Field, Message string }
type ConflictError  struct{ Resource, ID string }

// internal/api/handler.go — injected dependencies
type Handler struct {
    store  store.Store
    logger *slog.Logger
}
func NewHandler(s store.Store, logger *slog.Logger) *Handler

// internal/config/config.go
type Config struct {
    Port        int
    DatabaseURL string
    LogLevel    slog.Level
}
func Parse() (Config, error) // env vars override flags
```

> [!NOTE]
> The interface above is a starting point, not a contract. You may add methods, rename fields,
> or restructure as you discover what your implementation needs. Architecture emerges from
> building; it is fine to refactor as you go.

---

## Milestones

Work through milestones in order. Each milestone builds on the previous. Do not skip ahead.

### M0 — Setup and Module Initialization

**Goal:** A compilable, runnable skeleton with the module system configured and basic project structure in place.

**Acceptance Criteria:**
- [ ] `go mod init github.com/you/yourproject` succeeds
- [ ] `cmd/server/main.go` contains a `main()` that prints `"starting server"` and exits cleanly
- [ ] `go build ./...` produces no errors
- [ ] The top-level directory structure matches (approximately) the layout in [Suggested Architecture](#suggested-architecture)
- [ ] Dependencies (SQLite driver or Postgres driver) are added to `go.mod` with `go get`

**Estimated time:** 30–60 minutes

---

### M1 — Data Model and Store Interface

**Goal:** Define the data model and the `Store` interface. No implementation yet.

**Acceptance Criteria:**
- [ ] `internal/store/store.go` defines the `URLRecord` struct (or equivalent for your brief) and the `Store` interface with all methods
- [ ] Custom error types are defined (`NotFoundError`, `ValidationError`, `ConflictError` or equivalents)
- [ ] `internal/store/store.go` compiles cleanly with `go build ./...`
- [ ] You can articulate in your project README: what each interface method does and why you designed it this way

**Estimated time:** 1–2 hours

---

### M2 — Storage Implementation with SQL

**Goal:** A working SQLite (or Postgres) implementation of the `Store` interface.

**Acceptance Criteria:**
- [ ] `internal/store/sqlite.go` (or `postgres.go`) implements the `Store` interface
- [ ] The implementation uses `database/sql` with a connection pool (set `MaxOpenConns`, `MaxIdleConns`, `ConnMaxLifetime`)
- [ ] All SQL queries use prepared statements or the `?` / `$N` placeholder form — no raw user input in query strings
- [ ] A migration (SQL file or embedded schema) creates the required table(s) on startup
- [ ] The `Close()` method closes the `sql.DB` cleanly
- [ ] `internal/store/sqlite_test.go` contains at least 4 table-driven test cases covering: create, get existing, get non-existing (expects `NotFoundError`), and delete
- [ ] `go test -race ./internal/store/...` passes

**Estimated time:** 4–8 hours

---

### M3 — HTTP Handlers and Routing

**Goal:** HTTP handlers wired to the store, with correct status codes and JSON bodies.

**Acceptance Criteria:**
- [ ] `internal/api/handler.go` defines a `Handler` struct that takes a `store.Store` (and `*slog.Logger`) via constructor — not a global variable
- [ ] `internal/api/router.go` registers routes on an `http.ServeMux` using Go 1.22 patterns (e.g., `POST /shorten`, `GET /{code}`)
- [ ] Handlers return correct HTTP status codes: 201 (created), 200 (ok), 302 (redirect), 404 (not found), 400 (bad request), 409 (conflict), 500 (internal error)
- [ ] JSON responses use a consistent envelope (e.g., `{"data": ..., "error": null}` or simply the resource object; pick one and use it everywhere)
- [ ] A central `writeError(w, err)` function (or equivalent) maps custom error types to status codes
- [ ] `curl -s -X POST http://localhost:8080/shorten -d '{"url":"https://example.com"}'` returns a JSON body with a short code
- [ ] `curl -s http://localhost:8080/<code>` redirects to the original URL

**Estimated time:** 4–6 hours

---

### M4 — Middleware: Logging, Timeouts, and Recovery

**Goal:** Request middleware that adds structured logging, per-request timeouts, and panic recovery.

**Acceptance Criteria:**
- [ ] A `LoggingMiddleware` wraps every handler and logs: HTTP method, path, response status code, and duration using `log/slog`
- [ ] A `TimeoutMiddleware` wraps every handler and cancels the request `context.Context` after a configurable deadline (default: 5 seconds)
- [ ] A `RecoveryMiddleware` wraps every handler and catches panics, logging the stack trace and returning HTTP 500
- [ ] Middleware is composed in a chain and applied in `router.go` — handlers themselves do not contain logging or timeout logic
- [ ] Request logs appear in structured JSON format when the server runs (use `slog.NewJSONHandler`)

**Estimated time:** 2–4 hours

---

### M5 — Tests

**Goal:** A test suite that covers the store layer and the HTTP layer, including edge cases.

**Acceptance Criteria:**
- [ ] `internal/store/sqlite_test.go` (or equivalent): table-driven tests covering all `Store` methods; at minimum, a test for the "not found" error path and a test for the "conflict" error path
- [ ] `internal/api/handler_test.go`: at least three `httptest`-based tests: one for the create endpoint (valid input), one for the create endpoint (invalid input → 400), and one for the get/redirect endpoint (non-existent code → 404)
- [ ] Tests use a real, temporary SQLite database (not a mock): call `store.NewSQLiteStore(":memory:")` (or equivalent) in test setup
- [ ] `go test -race -cover ./...` passes and reports at least 60% coverage on the `internal/` packages
- [ ] No test uses `time.Sleep` as a synchronization mechanism

**Estimated time:** 3–5 hours

---

### M6 — Configuration and Graceful Shutdown

**Goal:** Configuration read from flags and environment variables; clean shutdown on signals.

**Acceptance Criteria:**
- [ ] `internal/config/config.go` defines a `Config` struct and a `Parse()` function that reads from `flag` and environment variables; environment variables override flags
- [ ] The `PORT` and `DATABASE_URL` environment variables are respected
- [ ] `cmd/server/main.go` calls `config.Parse()`, validates the config, and returns a clear error message if required configuration is missing
- [ ] On SIGINT or SIGTERM, the server calls `http.Server.Shutdown(ctx)` with a 15-second deadline, closes the database connection, flushes any remaining log output, and exits with code 0
- [ ] `go test` for the config package passes (test that env vars override flags)

**Estimated time:** 2–4 hours

---

### M7 — Docker and CI

**Goal:** A working multi-stage Dockerfile and a CI workflow that builds, tests, lints, and releases.

**Acceptance Criteria:**
- [ ] `Dockerfile` uses at least two stages; the final image does not contain the Go compiler, source code, or development tools
- [ ] `docker build -t myservice .` completes without errors
- [ ] `docker run --rm -p 8080:8080 myservice` starts the service and responds to requests
- [ ] `.github/workflows/ci.yml` runs on push and pull request; it installs Go, runs `go vet ./...`, runs `go test -race ./...`, and builds the binary
- [ ] The CI workflow runs a linter (`golangci-lint` or `staticcheck`)
- [ ] On a git tag push (e.g., `v0.1.0`), the workflow produces and uploads a binary artifact (using `go build -ldflags` to embed the version) or triggers `goreleaser`
- [ ] The project README.md (in your project directory) documents how to build, run, and test the service

**Estimated time:** 3–6 hours

---

## Acceptance Criteria

- [ ] All seven milestone acceptance criteria are met (detailed in [EXERCISES.md](./EXERCISES.md))
- [ ] `go build ./...`, `go vet ./...`, `go test -race ./...` all pass cleanly
- [ ] Linter (`golangci-lint` or `staticcheck`) passes
- [ ] `docker build` and `docker run` produce a working service
- [ ] All four primary operations work (create, read/redirect, stats, delete)
- [ ] Structured JSON logs appear on stdout; graceful shutdown exits cleanly within 20 seconds
- [ ] Project README explains what you built, how to run it, and at least three design decisions
- [ ] At least 8 Go topic modules are demonstrably used; documented in [PROJECTS.md](../PROJECTS.md)

---

## Help / Getting Unstuck

> [!IMPORTANT]
> Open only the hints you need. Each milestone provides three staged hints.
> Hint 1 is a nudge. Hint 2 explains the approach. Hint 3 provides a near-solution
> signature or snippet. Opening Hint 3 without trying Hints 1 and 2 first defeats the purpose.

### M0 Help — Setup

<details>
<summary>Hint 1 — Project initialization nudge</summary>

The quickest way to get the skeleton running is:
```bash
mkdir myshortener && cd myshortener
go mod init github.com/you/myshortener
mkdir -p cmd/server internal/api internal/store internal/config
touch cmd/server/main.go
```
Then write the simplest possible `main()` that compiles.

**Relevant module:** [[go/7. Packages and Modules]] — go.mod, package layout, `go get`

</details>

<details>
<summary>Hint 2 — Adding the SQLite driver</summary>

`modernc.org/sqlite` is a pure-Go SQLite driver (no CGO required, cross-compiles cleanly). Add it with:
```bash
go get modernc.org/sqlite
```
The import path for the blank-import side-effect registration is:
```go
import _ "modernc.org/sqlite"
```
You register it once in the file that calls `sql.Open("sqlite", ...)`.

**Relevant module:** [[go/14. Databases and Persistence]] — `database/sql` driver registration

</details>

<details>
<summary>Hint 3 — Minimal compilable main.go</summary>

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    fmt.Fprintln(os.Stdout, "starting server")
}
```

This is the floor, not the ceiling. Your real `main.go` will parse config, open a database, wire handlers, start an HTTP server, and wait for a shutdown signal. Build toward that incrementally.

</details>

---

### M1 Help — Data Model and Store Interface

<details>
<summary>Hint 1 — What belongs in the interface</summary>

Start by listing every database operation your service needs to support. For a URL shortener: store a new record, retrieve a record by code, increment a counter, delete a record. Each of those becomes a method on the interface. Every method should accept `context.Context` as its first argument — this is not optional; it is how callers propagate cancellation and deadlines into storage operations.

**Relevant module:** [[go/6. Methods and Interfaces]] — interface design, structural typing

</details>

<details>
<summary>Hint 2 — Error type design approach</summary>

Define your error types as structs that implement the `error` interface. Keep them in the `store` package (or a sub-package) so they can be checked with `errors.As` in the handler layer. The handler layer should not import the store's concrete type — only the interface and the error types.

```go
func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s %q not found", e.Resource, e.ID)
}
```

In handlers, map these with a type switch or `errors.As` calls.

**Relevant module:** [[go/8. Error Handling]] — custom error types, `errors.As`

</details>

<details>
<summary>Hint 3 — Interface skeleton</summary>

```go
package store

import (
    "context"
    "time"
)

type URLRecord struct {
    Code      string
    LongURL   string
    CreatedAt time.Time
    HitCount  int64
}

type Store interface {
    Create(ctx context.Context, r URLRecord) error
    Get(ctx context.Context, code string) (URLRecord, error)
    IncrementHits(ctx context.Context, code string) error
    Delete(ctx context.Context, code string) error
    Close() error
}
```

Write this, confirm it compiles, and move on to M2 before writing any implementation.

</details>

---

### M2 Help — Storage Implementation

<details>
<summary>Hint 1 — Opening and configuring the database</summary>

`sql.Open` does not actually open a connection — it prepares the `sql.DB` object. Call `db.PingContext(ctx)` after opening to verify the connection works. Configure pool sizes immediately after opening:

```go
db.SetMaxOpenConns(10)
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute)
```

For SQLite with `modernc.org/sqlite`, the DSN is the file path or `":memory:"` for an in-memory database.

**Relevant module:** [[go/14. Databases and Persistence]] — connection pools, `sql.Open`

</details>

<details>
<summary>Hint 2 — Running schema migrations</summary>

The simplest migration approach for this project: embed your SQL schema with `//go:embed` and run it at startup using `db.ExecContext`. Use `CREATE TABLE IF NOT EXISTS` so it is idempotent. For a more structured approach, use `golang-migrate/migrate` — but the embed approach is sufficient for this project.

```go
//go:embed migrations/001_init.sql
var schema string

func (s *SQLiteStore) migrate(ctx context.Context) error {
    _, err := s.db.ExecContext(ctx, schema)
    return err
}
```

**Relevant module:** [[go/14. Databases and Persistence]] — migrations, `//go:embed`

</details>

<details>
<summary>Hint 3 — Implementing Get with error mapping</summary>

```go
func (s *SQLiteStore) Get(ctx context.Context, code string) (URLRecord, error) {
    var r URLRecord
    var createdAt string // scan as string, parse as time.Time
    err := s.db.QueryRowContext(ctx,
        `SELECT code, long_url, created_at, hit_count FROM urls WHERE code = ?`,
        code,
    ).Scan(&r.Code, &r.LongURL, &createdAt, &r.HitCount)
    if errors.Is(err, sql.ErrNoRows) {
        return URLRecord{}, &NotFoundError{Resource: "short code", ID: code}
    }
    if err != nil {
        return URLRecord{}, fmt.Errorf("store.Get: %w", err)
    }
    r.CreatedAt, err = time.Parse(time.RFC3339, createdAt)
    if err != nil {
        return URLRecord{}, fmt.Errorf("store.Get: parse time: %w", err)
    }
    return r, nil
}
```

Notice: `sql.ErrNoRows` is mapped to your custom `NotFoundError`. All other errors are wrapped with context.

**Relevant module:** [[go/8. Error Handling]], [[go/14. Databases and Persistence]]

</details>

---

### M3 Help — HTTP Handlers and Routing

<details>
<summary>Hint 1 — Handler struct and constructor</summary>

Inject the store and logger via the constructor. Handlers are methods on the struct. This eliminates global state and makes the handlers trivially testable — in tests you pass a different store implementation.

```go
type Handler struct {
    store  store.Store
    logger *slog.Logger
}

func NewHandler(s store.Store, logger *slog.Logger) *Handler {
    return &Handler{store: s, logger: logger}
}
```

**Relevant module:** [[go/6. Methods and Interfaces]] — method receivers, dependency injection via constructors

</details>

<details>
<summary>Hint 2 — Go 1.22 routing patterns</summary>

Go 1.22 extended `http.ServeMux` to support method-prefixed patterns and path parameters:

```go
mux := http.NewServeMux()
mux.HandleFunc("POST /shorten", h.handleShorten)
mux.HandleFunc("GET /{code}", h.handleRedirect)       // {code} is a path parameter
mux.HandleFunc("GET /api/stats/{code}", h.handleStats)
mux.HandleFunc("DELETE /api/{code}", h.handleDelete)
```

In a handler, read the path parameter with `r.PathValue("code")`.

**Relevant module:** [[go/13. Web Services and APIs]] — `http.ServeMux`, path parameters

</details>

<details>
<summary>Hint 3 — Central error mapping</summary>

```go
func writeError(w http.ResponseWriter, err error) {
    var notFound *store.NotFoundError
    var validation *store.ValidationError
    var conflict *store.ConflictError

    switch {
    case errors.As(err, &notFound):
        http.Error(w, notFound.Error(), http.StatusNotFound)
    case errors.As(err, &validation):
        http.Error(w, validation.Error(), http.StatusBadRequest)
    case errors.As(err, &conflict):
        http.Error(w, conflict.Error(), http.StatusConflict)
    default:
        http.Error(w, "internal server error", http.StatusInternalServerError)
    }
}
```

Call `writeError(w, err)` at the end of every handler's error path. Never log the raw error to the HTTP response body — only to structured logs.

</details>

---

### M4 Help — Middleware

<details>
<summary>Hint 1 — Middleware signature</summary>

In Go, middleware is a function that takes an `http.Handler` and returns an `http.Handler`. This lets you chain middleware with a simple function-call pattern.

```go
func LoggingMiddleware(logger *slog.Logger, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        // ... wrap w to capture status code, then:
        next.ServeHTTP(w, r)
        // log after
    })
}
```

**Relevant module:** [[go/13. Web Services and APIs]] — middleware patterns

</details>

<details>
<summary>Hint 2 — Capturing the response status code</summary>

`http.ResponseWriter` does not expose the status code after it has been written. Wrap it in a struct that records the first call to `WriteHeader`:

```go
type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}
```

If `WriteHeader` is never called explicitly, the default is 200. Initialize `statusCode` to 200 before calling `next.ServeHTTP`.

</details>

<details>
<summary>Hint 3 — Timeout middleware</summary>

```go
func TimeoutMiddleware(timeout time.Duration, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx, cancel := context.WithTimeout(r.Context(), timeout)
        defer cancel()
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

The handler receives a context that will be cancelled after `timeout`. Every database call in the handler will respect this cancellation because they accept `context.Context`.

**Relevant module:** [[go/12. Advanced Concurrency Patterns]] — `context.WithTimeout`, deadline propagation

</details>

---

### M5 Help — Tests

<details>
<summary>Hint 1 — Testing the store layer</summary>

For SQLite, use `":memory:"` as the DSN in tests — it creates a fresh in-memory database per test that is automatically garbage-collected. Run `store.NewSQLiteStore(":memory:")` in `TestMain` or in each test function. Table-driven tests for the store look like:

```go
tests := []struct {
    name    string
    code    string
    wantErr bool
    errType interface{}
}{
    {"existing code", "abc123", false, nil},
    {"missing code", "notexist", true, &store.NotFoundError{}},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) { ... })
}
```

**Relevant module:** [[go/11. Testing and Benchmarking]] — table-driven tests, `t.Run`

</details>

<details>
<summary>Hint 2 — httptest-based handler tests</summary>

```go
func TestHandleShorten(t *testing.T) {
    s := store.NewMemoryStore() // or NewSQLiteStore(":memory:")
    h := api.NewHandler(s, slog.Default())
    mux := api.NewRouter(h)

    body := strings.NewReader(`{"url":"https://example.com"}`)
    req := httptest.NewRequest(http.MethodPost, "/shorten", body)
    req.Header.Set("Content-Type", "application/json")
    w := httptest.NewRecorder()

    mux.ServeHTTP(w, req)

    if w.Code != http.StatusCreated {
        t.Errorf("want 201, got %d", w.Code)
    }
}
```

**Relevant module:** [[go/11. Testing and Benchmarking]], [[go/13. Web Services and APIs]]

</details>

<details>
<summary>Hint 3 — Testing error paths</summary>

For the "not found" test, call the GET handler for a code that does not exist in your test store. Assert that the response status is 404. This verifies the entire chain: store returns `NotFoundError`, handler calls `writeError`, which maps it to 404.

```go
req := httptest.NewRequest(http.MethodGet, "/doesnotexist", nil)
w := httptest.NewRecorder()
mux.ServeHTTP(w, req)
if w.Code != http.StatusNotFound {
    t.Errorf("want 404, got %d", w.Code)
}
```

This is why injecting the store via the constructor matters — you can seed the store, or leave it empty, to exercise specific paths.

</details>

---

### M6 Help — Configuration and Graceful Shutdown

<details>
<summary>Hint 1 — Reading env vars with flag fallback</summary>

A clean pattern: define flags with `flag.IntVar` etc., call `flag.Parse()`, then overwrite with environment variable values if they are set. Env vars win.

```go
flag.IntVar(&cfg.Port, "port", 8080, "HTTP listen port")
flag.Parse()
if v := os.Getenv("PORT"); v != "" {
    // parse v and assign to cfg.Port
}
```

**Relevant module:** [[go/18. Build, Tooling, and Deployment]] — configuration patterns

</details>

<details>
<summary>Hint 2 — Signal handling</summary>

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
```

`signal.NotifyContext` (standard library, Go 1.16+) returns a context that is cancelled when the process receives one of the listed signals. Block on `<-ctx.Done()` in `main` to wait for the signal.

**Relevant module:** [[go/12. Advanced Concurrency Patterns]] — `context` cancellation, signal handling

</details>

<details>
<summary>Hint 3 — Graceful shutdown sequence</summary>

```go
// After <-ctx.Done() fires:
shutdownCtx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()

if err := srv.Shutdown(shutdownCtx); err != nil {
    logger.Error("shutdown error", "err", err)
}
if err := db.Close(); err != nil {
    logger.Error("db close error", "err", err)
}
logger.Info("server stopped")
```

`http.Server.Shutdown` stops the listener and waits for active requests to finish. The 15-second context is the maximum time to wait before force-closing. After `Shutdown` returns, close the database and flush logs.

**Relevant module:** [[go/12. Advanced Concurrency Patterns]], [[go/13. Web Services and APIs]]

</details>

---

### M7 Help — Docker and CI

<details>
<summary>Hint 1 — Multi-stage Dockerfile structure</summary>

Two-stage pattern:
1. **Builder stage**: use `golang:1.22-bookworm` (or `golang:1.22-alpine`), copy source, run `go build`
2. **Runtime stage**: use `gcr.io/distroless/static:nonroot` or `alpine:3.20`, copy only the compiled binary

Use `COPY --from=builder` to copy the binary between stages.

**Relevant module:** [[go/18. Build, Tooling, and Deployment]] — multi-stage Docker builds

</details>

<details>
<summary>Hint 2 — Embedding version information</summary>

Pass version information at build time via linker flags:
```bash
go build -ldflags="-X main.version=$(git describe --tags --always)" ./cmd/server
```
In `main.go`, declare `var version = "dev"` and use it in the startup log.

</details>

<details>
<summary>Hint 3 — Minimal GitHub Actions CI workflow</summary>

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - run: go vet ./...
      - run: go test -race ./...
      - run: go build ./...
```

Add a lint step using `golangci-lint-action` from the golangci-lint project. For tagged releases, add a job gated on `startsWith(github.ref, 'refs/tags/')`.

**Relevant module:** [[go/18. Build, Tooling, and Deployment]] — GitHub Actions, CI workflows

</details>

---

## Going Further

Extensions in roughly increasing difficulty:

1. **Authentication** — API key auth via `X-API-Key` header; store keys in the database; return 401 on missing/invalid keys.
2. **Rate limiting** — Per-IP token bucket (use `golang.org/x/time/rate` or implement your own); return 429.
3. **Observability** — Add `net/http/pprof` at `/debug/pprof/` and a `/metrics` endpoint using `expvar` or Prometheus text format.
4. **Custom short codes** — Let callers specify their own code in the `POST` body; handle collision with 409.
5. **In-memory LRU cache** — Implement a cache in front of `Store.Get` using `container/list` and a map; measure hit rate.
6. **Deploy to a real host** — Fly.io, Railway, or a DigitalOcean Droplet with a real domain. This is the moment it becomes a real service.

---

## Document Your Work

When your project is complete, record it in the topic [PROJECTS.md](../PROJECTS.md) using the Project Attempt Template. Your entry must describe what you built, link to the repository, list at least three specific learnings (not platitudes), describe the hardest challenge, and list every Go topic module you used with a one-sentence note on how you used it. Aim for at least 8 modules documented. This entry is part of the project — do not skip it.

---

## Self-Assessment Rubric

Grade yourself honestly after completing the project. The detailed rubric is in [ANSWERS.md](./ANSWERS.md).

| Criterion | 1 — Undeveloped | 2 — Developing | 3 — Proficient | 4 — Expert |
|-----------|----------------|----------------|----------------|------------|
| Interface design | Concrete struct, no interface | Interface defined but handlers import concrete type | Handlers depend only on the interface | Minimal, cohesive; second implementation would be trivial |
| Error handling | Errors ignored or printed | Errors returned but untyped | Custom error types; correct HTTP codes | Wrapped with context at every layer; `errors.As` in handlers |
| Testing | No tests | One layer only | Store + `httptest` handler tests; success and error paths | Table-driven; test helpers; coverage above 70% |
| `context` usage | No context in store | Context accepted but not used | Propagated through all layers; timeout middleware present | Deadlines set in middleware; cancellation respected in DB calls |
| Concurrency safety | Global mutable state | Mutex present but scope too wide | All shared state protected; `-race` passes | Race-free by design; model documented |
| Graceful shutdown | Abrupt stop | `os.Exit` after signal | `Shutdown` called; DB closed | In-flight requests complete; configurable deadline |
| Logging | `fmt.Println` | `log` package | `log/slog` structured; request logging in middleware | JSON handler; warn/error levels used correctly |
| Dockerfile | None | Single-stage | Multi-stage; minimal final image | Distroless/scratch; non-root user; health check |

---

## Learning Journal

_Record your experience building this project. This is the most important journal entry in the entire topic — be specific about what you built, what challenged you, and what changed in how you think about Go._

_Newest entries at the top._

---

### YYYY-MM-DD — Started Capstone

**What I've done so far:**
- Chose the [URL shortener / Task API / Webhook runner / Metrics collector] brief
- Completed milestone M0 (setup)

**First design decision:**
- I chose [SQLite / Postgres] because...

**What's already harder than expected:**
- ...

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

---

_Add new entries above this line._
