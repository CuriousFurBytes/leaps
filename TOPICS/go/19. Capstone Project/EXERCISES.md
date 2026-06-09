# Milestone Build Plan — Module 19: Capstone Project

> This is not a drill sheet. There are no small exercises here.
> Each section is a **build checkpoint** — a milestone you must complete before moving on.
> Work through milestones in order. Each one builds on the previous.

---

## Instructions

1. **Build, don't read.** This file is a roadmap. The work happens in your editor and terminal, not here.
2. **Mark criteria as you complete them.** Check each acceptance criterion box honestly.
3. **Use hints only when stuck.** Hints are in the main [README.md](./README.md#help--getting-unstuck) under the corresponding milestone. Open only as many as you need.
4. **Log your progress** in the [Progress Log](#progress-log) table at the bottom.
5. **Commit your work** at the end of each completed milestone — one commit per milestone, with a clear message (e.g., `feat(capstone): M2 - store implementation and table-driven tests`).

---

## Difficulty Legend

| Symbol | Meaning |
|--------|---------|
| M0 | Setup — structural scaffolding, no logic yet |
| M1 | Interface design — no implementation |
| M2 | Core implementation — the hard data layer |
| M3 | HTTP layer — wiring handlers to the store |
| M4 | Middleware — cross-cutting concerns |
| M5 | Testing — verify correctness systematically |
| M6 | Operations — configuration and lifecycle management |
| M7 | Delivery — containerization and CI |

---

## Checkpoint M0: Setup and Module Initialization

**Goal:** A compilable, runnable skeleton with correct project structure.

**Estimated time:** 30–60 minutes

### Definition of Done

- [ ] `go mod init` has been run; `go.mod` exists with the correct module path
- [ ] `cmd/server/main.go` compiles and runs (even if it only prints "starting server")
- [ ] Directory structure approximates the [Suggested Architecture](./README.md#suggested-architecture)
- [ ] Dependencies (database driver) added to `go.mod`
- [ ] `go build ./...` reports no errors
- [ ] Commit message: `feat(capstone): M0 - project skeleton and module init`

### Before Moving to M1

Answer these questions in your [NOTES.md](./NOTES.md) before proceeding:
- Why did you choose SQLite or Postgres?
- What is your module path and why?
- What is the top-level directory layout you've chosen?

<details>
<summary>Stuck? See M0 hints in README.md → Help / Getting Unstuck → M0 Help</summary>

Navigate to [README.md#m0-help--setup](./README.md#m0-help--setup)

</details>

---

## Checkpoint M1: Data Model and Store Interface

**Goal:** Define the data model and the `Store` interface. No SQL yet.

**Estimated time:** 1–2 hours

### Definition of Done

- [ ] `internal/store/store.go` exists and compiles
- [ ] `URLRecord` struct (or equivalent) is defined with all necessary fields
- [ ] `Store` interface is defined with all required methods
- [ ] Each method on `Store` accepts `context.Context` as its first parameter
- [ ] Custom error types are defined: `NotFoundError`, `ValidationError`, `ConflictError` (or equivalents)
- [ ] Each error type implements the `error` interface (has an `Error() string` method)
- [ ] `go build ./...` still passes
- [ ] Commit message: `feat(capstone): M1 - data model and store interface`

### Design Questions (answer in NOTES.md)

- Why does every `Store` method accept `context.Context`? What would break if you omitted it?
- Why are error types defined as structs rather than as `errors.New` sentinels?
- Could your `Store` interface be satisfied by an in-memory implementation for testing? (It should be.)

<details>
<summary>Stuck? See M1 hints in README.md → Help / Getting Unstuck → M1 Help</summary>

Navigate to [README.md#m1-help--data-model-and-store-interface](./README.md#m1-help--data-model-and-store-interface)

</details>

---

## Checkpoint M2: Storage Implementation with SQL

**Goal:** A working SQL implementation that passes table-driven tests.

**Estimated time:** 4–8 hours

### Definition of Done

- [ ] `internal/store/sqlite.go` (or `postgres.go`) contains a struct that implements `Store`
- [ ] `NewSQLiteStore(dsn string) (Store, error)` (or equivalent constructor) opens the database and runs migrations
- [ ] Connection pool is configured (`MaxOpenConns`, `MaxIdleConns`, `ConnMaxLifetime`)
- [ ] All SQL queries use parameterized placeholders — no string concatenation of user input
- [ ] Schema migration runs at startup and is idempotent (`CREATE TABLE IF NOT EXISTS`)
- [ ] `sql.ErrNoRows` is mapped to `*NotFoundError` in `Get` and `Delete`
- [ ] `internal/store/sqlite_test.go` exists with table-driven tests:
  - [ ] `TestCreate` — successful creation
  - [ ] `TestGet_existing` — get a record that exists
  - [ ] `TestGet_missing` — get a record that doesn't exist, expect `*NotFoundError`
  - [ ] `TestIncrementHits` — hit count increases after calling `IncrementHits`
  - [ ] `TestDelete_existing` — successful deletion
  - [ ] `TestDelete_missing` — delete a record that doesn't exist, expect `*NotFoundError`
- [ ] `go test -race ./internal/store/...` passes with no failures and no data races
- [ ] Commit message: `feat(capstone): M2 - sqlite store implementation and tests`

### Design Questions (answer in NOTES.md)

- What happens if two requests try to create the same short code simultaneously? How does your implementation handle this?
- Why use `QueryRowContext` for single-row queries instead of `QueryContext`?
- What is a connection pool and why does it matter for an HTTP service?

<details>
<summary>Stuck? See M2 hints in README.md → Help / Getting Unstuck → M2 Help</summary>

Navigate to [README.md#m2-help--storage-implementation](./README.md#m2-help--storage-implementation)

</details>

---

## Checkpoint M3: HTTP Handlers and Routing

**Goal:** A running HTTP server with correct routing and JSON responses.

**Estimated time:** 4–6 hours

### Definition of Done

- [ ] `internal/api/handler.go` defines `Handler` struct with `store.Store` injected via constructor
- [ ] `internal/api/router.go` registers routes on `http.ServeMux` using Go 1.22 method-prefixed patterns
- [ ] `handleShorten` (POST): validates input, calls `store.Create`, returns 201 with JSON body
- [ ] `handleRedirect` (GET `/{code}`): calls `store.Get` and `store.IncrementHits`, returns 302 redirect
- [ ] `handleStats` (GET `/api/stats/{code}`): returns 200 with JSON record
- [ ] `handleDelete` (DELETE `/api/{code}`): calls `store.Delete`, returns 204 No Content
- [ ] A `writeError` function (or equivalent) maps `*NotFoundError` → 404, `*ValidationError` → 400, `*ConflictError` → 409, other → 500
- [ ] No error details are leaked to clients in 500 responses (log the error internally)
- [ ] Manual `curl` testing confirms all four operations work end-to-end
- [ ] `cmd/server/main.go` wires everything together: opens database, creates handler, starts server
- [ ] Commit message: `feat(capstone): M3 - http handlers and routing`

### Smoke Test (run manually before checking this off)

```bash
# Start the server
go run ./cmd/server -port 8080

# Create a short URL
curl -s -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
# Expected: {"code":"xxxx","short_url":"http://localhost:8080/xxxx"}

# Follow the redirect
curl -s -L http://localhost:8080/xxxx
# Expected: the content of https://example.com (or a redirect)

# Get stats
curl -s http://localhost:8080/api/stats/xxxx
# Expected: JSON with code, long_url, created_at, hit_count

# Delete
curl -s -X DELETE http://localhost:8080/api/xxxx
# Expected: 204 No Content
```

<details>
<summary>Stuck? See M3 hints in README.md → Help / Getting Unstuck → M3 Help</summary>

Navigate to [README.md#m3-help--http-handlers-and-routing](./README.md#m3-help--http-handlers-and-routing)

</details>

---

## Checkpoint M4: Middleware

**Goal:** Structured request logging, per-request timeouts, and panic recovery.

**Estimated time:** 2–4 hours

### Definition of Done

- [ ] `internal/api/middleware.go` exists
- [ ] `LoggingMiddleware`: logs method, path, status code, duration using `log/slog` with JSON handler
- [ ] `TimeoutMiddleware`: cancels request context after configurable duration (default 5s)
- [ ] `RecoveryMiddleware`: recovers from panics, logs stack trace, returns 500
- [ ] Middleware is composed in a chain and applied uniformly — no per-handler logging or timeout setup
- [ ] Starting the server and hitting an endpoint produces a structured JSON log line like:
  ```json
  {"time":"...","level":"INFO","msg":"request","method":"POST","path":"/shorten","status":201,"duration_ms":3}
  ```
- [ ] `go test -race ./...` still passes after adding middleware
- [ ] Commit message: `feat(capstone): M4 - logging, timeout, and recovery middleware`

### Design Question (answer in NOTES.md)

- Why does `TimeoutMiddleware` not just set a global timeout on the `http.Server`? What is the difference between a server-level read/write timeout and a per-request context timeout?

<details>
<summary>Stuck? See M4 hints in README.md → Help / Getting Unstuck → M4 Help</summary>

Navigate to [README.md#m4-help--middleware](./README.md#m4-help--middleware)

</details>

---

## Checkpoint M5: Tests

**Goal:** A test suite with coverage of both the store and HTTP layers.

**Estimated time:** 3–5 hours

### Definition of Done

**Store tests** (`internal/store/sqlite_test.go` or equivalent):
- [ ] Table-driven tests for all `Store` methods (at least 6 test cases across methods)
- [ ] `*NotFoundError` path is tested explicitly
- [ ] `*ConflictError` path is tested explicitly (attempt to create the same code twice)
- [ ] All tests use `":memory:"` SQLite for isolation

**Handler tests** (`internal/api/handler_test.go`):
- [ ] Test for `POST /shorten` with valid input → 201
- [ ] Test for `POST /shorten` with invalid/missing URL → 400
- [ ] Test for `GET /{code}` with a valid code → 302 to original URL
- [ ] Test for `GET /{code}` with non-existent code → 404
- [ ] Test for `GET /api/stats/{code}` → 200 with correct JSON fields
- [ ] Test for `DELETE /api/{code}` → 204
- [ ] Tests use `httptest.NewRecorder` and `httptest.NewRequest`
- [ ] Tests use a real `Store` (SQLite `:memory:`) — no mocks

**Coverage and quality:**
- [ ] `go test -race -cover ./...` passes
- [ ] Coverage on `internal/` packages is at least 60%
- [ ] No `time.Sleep` in any test
- [ ] Commit message: `test(capstone): M5 - comprehensive store and handler tests`

### Design Question (answer in NOTES.md)

- Why do these tests use a real SQLite `:memory:` store rather than a mock? What advantage does this give? What disadvantage?

<details>
<summary>Stuck? See M5 hints in README.md → Help / Getting Unstuck → M5 Help</summary>

Navigate to [README.md#m5-help--tests](./README.md#m5-help--tests)

</details>

---

## Checkpoint M6: Configuration and Graceful Shutdown

**Goal:** Configuration from flags and env vars; clean shutdown on signals.

**Estimated time:** 2–4 hours

### Definition of Done

- [ ] `internal/config/config.go` defines `Config` struct and `Parse() (Config, error)`
- [ ] `PORT` and `DATABASE_URL` environment variables are recognized and override flag values
- [ ] Missing required config produces a clear error message at startup (not a panic)
- [ ] `cmd/server/main.go` handles the shutdown signal correctly:
  - Listens for SIGINT / SIGTERM
  - Calls `srv.Shutdown(ctx)` with a 15-second deadline
  - Closes the database after shutdown completes
  - Logs "server stopped" before exiting
  - Exits with code 0 on clean shutdown
- [ ] Manual test: start the server, send a request, immediately `Ctrl+C` — in-flight request completes before the process exits
- [ ] `go test ./internal/config/...` passes (test env var override behavior)
- [ ] Commit message: `feat(capstone): M6 - config parsing and graceful shutdown`

### Manual Shutdown Test

```bash
# Start the server
go run ./cmd/server

# In another terminal: start a slow request (simulate with a long sleep in a test handler,
# or use curl with a slow endpoint) then immediately Ctrl+C the server.
# The server should wait for the request to complete before exiting.

# Also test:
PORT=9090 go run ./cmd/server
# Confirm the server listens on 9090, not the default.
```

<details>
<summary>Stuck? See M6 hints in README.md → Help / Getting Unstuck → M6 Help</summary>

Navigate to [README.md#m6-help--configuration-and-graceful-shutdown](./README.md#m6-help--configuration-and-graceful-shutdown)

</details>

---

## Checkpoint M7: Docker and CI

**Goal:** A multi-stage Dockerfile and a GitHub Actions CI workflow.

**Estimated time:** 3–6 hours

### Definition of Done

**Dockerfile:**
- [ ] Multi-stage build (at least two `FROM` stages)
- [ ] Final image does not contain Go compiler, source code, or build tools
- [ ] `docker build -t myservice .` succeeds
- [ ] `docker run --rm -p 8080:8080 myservice` starts the service and it responds to requests
- [ ] The binary runs as a non-root user in the container

**GitHub Actions:**
- [ ] `.github/workflows/ci.yml` exists
- [ ] Workflow triggers on push and pull_request
- [ ] Workflow runs: `go vet ./...`, `go test -race ./...`, `go build ./...`
- [ ] Workflow runs a linter (`golangci-lint` or `staticcheck`)
- [ ] Workflow passes on the current main/master branch (push to GitHub to verify)

**Project README:**
- [ ] `README.md` in the project root (not this leaps file) exists and documents:
  - [ ] What the service does (2–3 sentences)
  - [ ] Prerequisites (Go version, Docker)
  - [ ] How to build: `go build ./...`
  - [ ] How to run locally: `go run ./cmd/server`
  - [ ] How to test: `go test -race ./...`
  - [ ] How to build and run via Docker
  - [ ] At least three design decisions with justification
- [ ] Commit message: `feat(capstone): M7 - multi-stage dockerfile and ci workflow`

<details>
<summary>Stuck? See M7 hints in README.md → Help / Getting Unstuck → M7 Help</summary>

Navigate to [README.md#m7-help--docker-and-ci](./README.md#m7-help--docker-and-ci)

</details>

---

## Final Acceptance Check

Run through the [Acceptance Criteria](./README.md#acceptance-criteria) in the main README and confirm every box is checked before recording your project in PROJECTS.md.

| Final Check | Status |
|-------------|--------|
| `go build ./...` passes | [ ] |
| `go vet ./...` passes | [ ] |
| `go test -race ./...` passes | [ ] |
| Linter passes | [ ] |
| Docker build and run works | [ ] |
| All four API operations functional | [ ] |
| Structured JSON logs on requests | [ ] |
| Graceful shutdown works | [ ] |
| Project README complete | [ ] |
| 8+ modules documented in PROJECTS.md | [ ] |
| PROJECTS.md entry recorded | [ ] |

---

## Progress Log

_Record your milestone completions here. One row per milestone, filled in as you complete each one._

| Milestone | Date Completed | Time Spent | Notes / Key Learnings |
|-----------|---------------|------------|----------------------|
| M0 — Setup | — | — | — |
| M1 — Interfaces | — | — | — |
| M2 — SQL Store | — | — | — |
| M3 — HTTP Handlers | — | — | — |
| M4 — Middleware | — | — | — |
| M5 — Tests | — | — | — |
| M6 — Config & Shutdown | — | — | — |
| M7 — Docker & CI | — | — | — |
| **Total** | — | **— hours** | — |

**Hints used:**

| Milestone | Hints opened | Was the hint necessary? |
|-----------|-------------|------------------------|
| M0 | — | — |
| M1 | — | — |
| M2 | — | — |
| M3 | — | — |
| M4 | — | — |
| M5 | — | — |
| M6 | — | — |
| M7 | — | — |

_Reflection: Were there milestones where you used more hints than you expected? What would you study differently next time?_

> _Your reflection here:_
