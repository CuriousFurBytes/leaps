# Self-Evaluation Guidance — Module 19: Capstone Project

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before completing the project and TEST.md.**
>
> Reading this file first defeats the purpose of the self-assessment. There is no trick here —
> you will know if you read the rubric before answering the questions. The evaluation is for
> your benefit, and an inflated self-score is worthless.
>
> Close this file, complete your project, complete [TEST.md](./TEST.md), and return here only
> to evaluate your work.

---

> [!IMPORTANT]
> **There is no complete reference solution in this file — by design.**
>
> AGENTS.md §5 states: "Do not hand over a complete copy-paste solution that removes the
> work." This file contains rubrics describing what good looks like, not a working
> implementation. If you are looking for a shortcut, you have missed the point of the
> capstone.

---

## How to Use This File

1. Complete the project and all milestone acceptance criteria.
2. Complete TEST.md in full, examining your actual code as you answer.
3. Come to this file to evaluate your answers against the rubrics below.
4. For each criterion: score yourself honestly. Partial credit exists.
5. Record your total in the Grading Records section at the bottom.
6. For any criterion where you scored below full credit: note what to improve in your NOTES.md.

---

## Scoring Guidelines

### What Earns Full Credit

- The answer demonstrates that you understand *why*, not just *what*
- Claims are backed by specific references to your actual code (file names, function names, line numbers)
- Honest acknowledgment of weaknesses without deflection
- Multiple perspectives considered for open-ended questions

### What Earns Partial Credit

- Correct general direction but missing specifics or lacking code references: **50–75%**
- Correct answer for a simple case but missing the edge cases: **50%**
- Honest identification of a problem without a solution: **25–50%**

### What Earns No Credit

- "I don't know" without any attempt at reasoning
- Answers that contradict what your code actually does (you checked, right?)
- Platitudes: "I learned a lot" without specifics

---

## Section 1: Project Verification — Evaluation Rubric

### 1.1 — `go test -race` (2 pts)

**Full credit:** Tests pass, race detector reports no issues, coverage is reported (even if below 60%). If tests fail, the answer describes the failure specifically and shows understanding of the root cause.

**Partial credit (1 pt):** Tests pass but no coverage reported, or coverage is reported but the answer does not reflect on whether 60% is a meaningful threshold for this codebase.

**What good looks like:** Coverage on `internal/store` and `internal/api` packages combined is at least 60%. The store's error paths (`NotFoundError`, `ConflictError`) are tested. The handler's 4xx paths are tested.

---

### 1.2 — Static analysis (2 pts)

**Full credit:** Both tools pass cleanly. If issues are reported, the answer distinguishes between genuine problems (should be fixed) and false positives (can be suppressed with a comment and an explanation).

**What good looks like:** `go vet` should always pass cleanly in a production service. Linter warnings about exported identifiers without documentation comments are acceptable to suppress for a capstone project; security warnings, errcheck failures, and race condition warnings are not.

---

### 1.3 — Four core operations (2 pts)

**Full credit:** All four operations return correct status codes. Hit count is reflected in stats after a redirect. Stats return 404 after deletion.

**Common gap:** Forgetting to call `IncrementHits` from the redirect handler, or calling it before checking whether the code exists, so the count is wrong on error paths.

---

### 1.4 — Graceful shutdown (2 pts)

**Full credit:** Process exits 0. Logs confirm clean shutdown sequence. Any error messages during shutdown are explained (e.g., `context deadline exceeded` on the shutdown context if you are testing with in-flight requests).

**What good looks like:** The log sequence on shutdown is:
```
INFO  received shutdown signal
INFO  shutting down HTTP server
INFO  database closed
INFO  server stopped
```
or equivalent. Exit code is 0, verified with `echo $?`.

---

### 1.5 — Docker (2 pts)

**Full credit:** Build succeeds, container serves requests, image size is reasonable (under 50 MB is good; under 15 MB with distroless is excellent). The learner understands why a multi-stage build produces a smaller image.

**What good looks like:** A distroless or alpine final image with a statically compiled Go binary is typically 5–20 MB. A `golang:1.22` single-stage image would be 300–500 MB. If the image is over 100 MB, the multi-stage build is likely not working correctly.

---

### 1.6 — Structured logging (2 pts)

**Full credit:** Logs are JSON. Each access log has method, path, status, duration. Error responses log at WARN or ERROR level, not INFO.

**Common gap:** Logging at INFO level for all responses, including 4xx and 5xx. A 404 for a non-existent resource is a client error (WARN is appropriate); a 500 is a server error (ERROR is appropriate).

---

### 1.7 — Configuration (2 pts)

**Full credit:** `PORT` env var changes the listen port. Invalid `DATABASE_URL` produces a clear, user-readable error at startup, not a panic with a stack trace. The learner can point to the exact lines where the env var override happens.

**What good looks like:**
```go
if v := os.Getenv("PORT"); v != "" {
    port, err := strconv.Atoi(v)
    if err != nil {
        return Config{}, fmt.Errorf("invalid PORT: %w", err)
    }
    cfg.Port = port
}
```
This is explicit, testable, and produces a clear error. A startup panic with `os.MustGetenv` is not acceptable for production configuration.

---

## Section 2: Design Justification — Evaluation Rubric

### 2.1 — Storage Interface Design (3 pts)

**Full credit:** Explains that the interface enables testing handlers without a real database (pass `:memory:` SQLite or a fake implementation). Also identifies that a second storage backend (Postgres, Redis) could be added without changing the handler code. The answer references the specific interface file.

**What distinguishes a 3 from a 1:** A 1-point answer says "interfaces are good practice." A 3-point answer says "because handlers take `store.Store` not `*SQLiteStore`, I can write a `MemoryStore` for unit tests and swap the `SQLiteStore` for a `PostgresStore` in production without touching the handler package at all."

**Common gap:** Not recognizing that `errors.As` in the handler layer requires the error types to be exported from the `store` package, creating a dependency between handler and store regardless of the interface.

---

### 2.2 — Error Handling and HTTP Status Code Mapping (3 pts)

**Full credit:** Traces the path: `SQLiteStore.Get` returns `&NotFoundError{...}` → wrapped with `fmt.Errorf("store.Get: %w", err)` → handler receives the wrapped error → `errors.As(err, &notFound)` unwraps through the chain → `writeError` maps to 404. All three parts answered.

**For part (c):** Leaking raw error strings to HTTP responses is a security issue (information disclosure) and an API contract issue (internal error messages are not stable, versioned API responses). The correct pattern: log the raw error with slog at ERROR level; return a generic "internal server error" or a sanitized message to the client.

**Common gap:** Not explaining that `errors.As` works through wrapped errors (i.e., even if the error is wrapped with `%w` multiple times, `errors.As` will still find the underlying `*NotFoundError`).

---

### 2.3 — Context Propagation (3 pts)

**Full credit:** Correctly identifies that `r.Context()` is the per-request context created by `net/http` for each incoming request. Explains that `TimeoutMiddleware` calls `context.WithTimeout(r.Context(), 5*time.Second)` and passes `r.WithContext(ctx)` to the next handler. The store methods receive this derived context and pass it to `db.QueryRowContext(ctx, ...)`. When the client disconnects, `r.Context()` is cancelled, which cascels the derived context, which causes the in-progress `QueryRowContext` to return `context.Canceled`.

**Common gap:** Not knowing that `database/sql`'s context-aware methods (`QueryRowContext`, `ExecContext`) actually check for context cancellation. Some implementations accept context but ignore it — the learner should verify their store actually uses `ctx` and not `context.Background()`.

---

### 2.4 — Test Strategy (3 pts)

**Full credit:** Explains that using real SQLite `:memory:` tests the actual SQL behavior (type coercions, constraint violations, transaction semantics) that a mock cannot test. Identifies gaps: concurrent request tests (two goroutines calling `Create` simultaneously), testing the hit count atomicity under load, testing context cancellation behavior. Confirms that handler tests would work with a Postgres implementation of `Store` because they depend only on the interface.

**Common gap:** Not recognizing that mocks test the mock, not the real implementation. If your mock `Store` always returns `nil` for errors, your handler tests will pass even if the real store returns an error that the handler does not handle.

---

### 2.5 — Graceful Shutdown (3 pts)

**Full credit:** States the maximum shutdown time (15 seconds for `http.Server.Shutdown` + time for any final cleanup). Explains that an in-progress database query will receive context cancellation when the request context is cancelled during shutdown — the query will return `context.Canceled`, the handler will receive this error, and the handler should return an appropriate error to the client before the connection is closed. Honest about gaps (e.g., "I don't close background goroutines during shutdown," or "I haven't tested what happens to a long-running transaction").

**What good looks like — a common gap identified honestly:** Many first implementations do not handle the case where a background goroutine (e.g., a metrics emitter, a cleanup job) is still running when `main` exits. Go's `sync.WaitGroup` or a `context` passed to background goroutines is the solution.

---

## Section 3: Hard Problems — Evaluation Rubric

### 3.1 — The Hardest Bug (4 pts)

**Full credit:** The answer is specific (not "I had a bug with context"), describes a real investigation process, and identifies a genuine learning. Example excellent answers:

- "I had a data race in the hit counter because I was reading and incrementing it in two separate SQL queries instead of one atomic `UPDATE`. `go test -race` reported it. I fixed it by combining the increment and read into `UPDATE urls SET hit_count = hit_count + 1 WHERE code = ? RETURNING hit_count`."
- "The `LoggingMiddleware` was always logging status 200 because `WriteHeader` was only called for non-200 responses. I had initialized `statusCode` to 0 and forgot that `200` is the implicit default when you call `w.Write` without `WriteHeader`."
- "My graceful shutdown was exiting before in-flight requests completed because I was calling `os.Exit(0)` after sending to the shutdown channel, which killed the process before `Shutdown` finished. The fix was to wait for `Shutdown` to return."

**What earns 1–2 pts:** "I had a bug with JSON parsing" with no specifics about root cause or discovery process.

**What earns 0 pts:** "No significant bugs" — this is almost certainly not true for a first production service.

---

### 3.2 — A Design Decision to Change (4 pts)

**Full credit:** Names a specific decision (file + type or function), explains the reasoning that seemed sound at the time, articulates why it is problematic now, and proposes a concrete alternative. Example excellent answers:

- "I put short code generation in the HTTP handler (`handleShorten`). At the time it seemed fine. But now the handler knows too much about code generation logic; if I want to change the algorithm or add retries on collision, I need to change the handler. I'd move it to the store layer or a separate `codec` package."
- "I used a single global `logger` variable instead of injecting it. This made testing messy because test output includes log lines from the service. I'd inject `*slog.Logger` everywhere from the start."
- "My `Config` struct uses exported fields with no validation. I'd add a `Validate() error` method so validation happens once at startup, not scattered across callers."

---

### 3.3 — Concurrency and Data Safety (4 pts)

**Full credit:** Correctly identifies that `database/sql`'s connection pool is thread-safe and handles concurrent access transparently. Explains that handlers are called in goroutines by `net/http` and that the store receives concurrent calls. Notes that SQLite has a limitation: with the `modernc.org/sqlite` driver, concurrent writes may serialize due to SQLite's write locking — this is expected behavior, not a bug. `go test -race` is the canonical tool for finding races.

**What earns partial credit:** "I don't have races because I'm using a database" — partially correct (the DB serializes writes) but misses the possibility of races in in-memory state (e.g., if you added a `map[string]int` cache without a mutex).

**What earns 0 pts:** "Go is automatically thread-safe" — it is not. The race detector exists precisely because Go code can and does have data races.

---

## Section 4: Scale and Evolution — Evaluation Rubric

### 4.1 — Under 10x Load (3 pts)

**Full credit:** Identifies the real bottleneck for this specific service. For a URL shortener: the redirect handler calls two store operations (Get + IncrementHits) per request. Under load, the SQLite write lock becomes the bottleneck for IncrementHits. Solutions: (1) batch hit count updates asynchronously, accepting eventual consistency; (2) switch to Postgres with `FOR UPDATE SKIP LOCKED`; (3) cache the long URL in memory to eliminate the Get query. Each solution introduces tradeoffs: async updates lose some hit counts on crash; Postgres requires operational overhead; an in-memory cache requires cache invalidation logic.

**What earns partial credit:** "Add more servers" — valid but does not identify which specific component fails first.

---

### 4.2 — Adding a New Feature (3 pts)

**Full credit:** Identifies that `Create` needs to accept an optional `customCode` (or the `URLRecord` struct needs a `CustomCode` field), that a collision on a custom code is a `ConflictError` (already handled by the error mapping), and that new test cases are: (1) custom code is accepted and used; (2) custom code that is already taken returns 409; (3) custom code with invalid characters returns 400.

**Common gap:** Not recognizing that the `ConflictError` type is already present and the error mapping already handles it. This is a good example of "the interface was designed well enough to absorb this change without modification."

---

### 4.3 — Production Readiness Assessment (3 pts)

**Full credit:** Ratings are specific and honest. A 2 or 3 with a good justification is worth more than a 4 or 5 with vague justification. Example of good ratings with justifications:

- Error handling: 3 — "I handle NotFoundError and ConflictError, but I don't have a consistent way to distinguish client errors from server errors in logs."
- Observability: 2 — "I have structured access logs but no metrics endpoint, no tracing, and no alerting-ready log format."
- Security: 2 — "No input sanitization beyond URL validation, no rate limiting, no authentication, SQL injection is prevented by parameterized queries."
- Test coverage: 3 — "Store and handler layers are tested at 70%+, but config, middleware, and shutdown are not tested."
- README: 3 — "Build/test/run instructions exist; no runbook for production incidents."

The lowest-rated category with a specific improvement plan earns full credit for this part.

---

## Self-Assessment — What Good Looks Like

For the final four reflection questions, there are no wrong answers — only answers that show depth or shallowness.

**What distinguished an excellent learner's self-assessment:** They name something specific they are proud of (not "the whole project"), identify a concrete weakness without deflection, have a clear and specific plan for the next week (not "clean up the code"), and describe a genuine shift in thinking about Go (not "I learned a lot").

**Example of an excellent shift in thinking:** "Before Module 9, I thought goroutines were complicated and scary. After building this service, I realize goroutines are just the mechanism Go uses for every HTTP request — the complexity I was scared of is actually managed by `net/http` and `database/sql`. What I actually needed to understand was `context` cancellation, which is the real plumbing."

---

## Common Gaps Across All Projects

These are failure modes that appear in most first production services, regardless of experience level. If your self-assessment surfaced any of these, you are in good company — and now you know what to study:

1. **Leaking goroutines on shutdown** — Background goroutines started in `main` or `init` that are not connected to the shutdown signal. Use a `context` derived from the signal context and pass it to all long-running goroutines.

2. **Ignoring the error from `rows.Close()`** — `database/sql`'s `sql.Rows` has a `Close()` method that returns an error. Most code ignores it; production code should check it.

3. **Not setting connection pool limits** — `sql.DB` is a pool, not a single connection. Without `MaxOpenConns`, it will open connections without bound under load, potentially exhausting database or OS limits.

4. **Using `context.Background()` inside a handler** — If a store method receives a `context.Context` but passes `context.Background()` to the database call, the context cancellation has no effect and the point of accepting `context.Context` is defeated.

5. **Logging the raw error in the HTTP response** — Internal error messages contain information about the database schema, internal package paths, and other details that should not be visible to API clients.

6. **Not testing concurrent access** — A test that calls `Create` from one goroutine and `Get` from another simultaneously is the minimal test for a concurrent data race. Without it, the race detector cannot find goroutine-level races during normal unit tests.

---

## Grading Records

_Append a new record below each time a test is graded. Do not overwrite previous records._

```yaml
---
graded_at:
graded_by:
module: go/19_capstone_project
score: /50
percentage:
pass: true|false
breakdown:
  section_1_verification: /14
  section_2_design: /15
  section_3_hard_problems: /12
  section_4_scale_evolution: /9
notes: ""
---
```
