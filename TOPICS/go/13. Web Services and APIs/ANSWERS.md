# Answer Key — Module 13: Web Services and APIs

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
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — http.Handler interface [1 pt]

**Full credit answer:**
```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```
Any type that implements `ServeHTTP(w http.ResponseWriter, r *http.Request)` satisfies `http.Handler`. The `http.HandlerFunc` type is an adapter that converts a compatible function to an `http.Handler`.

**Key points required:**
- The interface has exactly one method: `ServeHTTP`
- The signature takes `http.ResponseWriter` and `*http.Request`

**Common wrong answers:**
- Writing `Handle` or `HandleFunc` as the method name — those are `ServeMux` methods, not the interface method

---

### 1.2 — Go 1.22 routing syntax [1 pt]

**Full credit answer:**
The pattern string is `"GET /items/{id}"`. Inside the handler, retrieve the parameter with `r.PathValue("id")`.

```go
mux.HandleFunc("GET /items/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
})
```

**Key points required:**
- Method prefix `GET` followed by a space before the path
- Curly braces `{id}` for the path parameter
- `r.PathValue("id")` — not `r.URL.Query().Get("id")` (that is a query parameter)

---

### 1.3 — Content-Type header ordering [1 pt]

**Full credit answer:**
`Content-Type` (and all headers) must be set **before** the first call to `w.WriteHeader(status)` and before any write to the response body. Once `WriteHeader` is called, the headers are flushed to the network and cannot be changed. The first call to `w.Write(b)` implicitly calls `WriteHeader(200)` if it hasn't been called yet — so any header set after the first `Write` is too late.

**Key points required:**
- Headers must be set before `WriteHeader` AND before `Write`
- First `Write` implicitly calls `WriteHeader(200)`
- Setting headers after a write is silently ignored (they are not sent)

**Common wrong answers:**
- "You can set headers any time before the response is sent" — incorrect; headers are flushed at the first write

---

### 1.4 — http.MaxBytesReader [1 pt]

**Full credit answer:**
`http.MaxBytesReader(w, r.Body, n)` wraps the request body reader and returns an error if more than `n` bytes are read. When the limit is exceeded, it returns a `*http.MaxBytesError`. Detect it with `errors.As(err, &maxBytesErr)`:

```go
r.Body = http.MaxBytesReader(w, r.Body, 1<<20) // 1 MB
var item Item
if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
    var maxErr *http.MaxBytesError
    if errors.As(err, &maxErr) {
        // body too large
    }
}
```

**Key points required:**
- Wraps `r.Body` before decoding
- Returns `*http.MaxBytesError` on overflow
- `errors.As` is the correct way to check for it

---

### 1.5 — http.Server timeout fields [1 pt]

**Full credit answer:**
| Field | Covers |
|-------|--------|
| `ReadTimeout` | Time to read the complete request header and body |
| `WriteTimeout` | Time to write the complete response |
| `IdleTimeout` | Time an idle keep-alive connection can remain open between requests |

**Key points required:**
- All three names: `ReadTimeout`, `WriteTimeout`, `IdleTimeout`
- At least a one-sentence description of what each one limits

**Common wrong answers:**
- Confusing `ReadTimeout` and `WriteTimeout` — `ReadTimeout` protects against slow clients sending large request bodies; `WriteTimeout` protects against handlers that take too long to produce a response

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Middleware pattern [2 pts]

**Full credit answer:**
A middleware function has the signature `func(http.Handler) http.Handler`. It takes the next handler in the chain and returns a new handler that wraps it. The returned handler can run code before and after calling `next.ServeHTTP(w, r)`.

```go
func MyMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // "before" phase — runs before the handler
        next.ServeHTTP(w, r) // call the inner handler
        // "after" phase — runs after the handler returns
    })
}
```

For `WithLogging(WithRequestID(mux))`:
- `WithRequestID(mux)` returns a handler that, when called, injects a request ID and then calls `mux`
- `WithLogging(...)` wraps that — so `WithLogging` runs first on every request

Execution order for a request:
1. `WithLogging` before phase (record start time)
2. `WithRequestID` before phase (inject ID into context)
3. `mux.ServeHTTP` — route dispatch and handler
4. `WithRequestID` after phase (none in this case)
5. `WithLogging` after phase (log method, path, duration)

**Rubric:**
- 2 pts: Correct signature, correct execution order (outermost middleware runs first in before-phase, last in after-phase), concrete explanation of the wrapping chain
- 1 pt: Correct general idea but execution order incorrect or vague
- 0 pts: Describes middleware as something other than the handler-wrapping pattern

---

### 2.2 — Why explicit http.Server [2 pts]

**Full credit answer:**
`http.ListenAndServe(addr, handler)` creates an internal `http.Server` with **zero timeouts** — `ReadTimeout`, `WriteTimeout`, and `IdleTimeout` are all 0, which means no timeout. This creates at least two concrete risks:

1. **Slowloris / slow client attack**: A client that sends request headers byte by byte, very slowly, keeps the connection open indefinitely. With `ReadTimeout: 0`, the server never drops the slow connection, and a modest number of such clients can exhaust the server's goroutine/file-descriptor pool.

2. **Long-running handler**: A handler that takes 10 minutes to generate a response ties up a goroutine and a connection for that entire time. With `WriteTimeout: 0`, there is nothing preventing a misbehaving client or a slow database query from holding resources open indefinitely.

An explicit `http.Server` struct also lets you configure `MaxHeaderBytes`, `TLSConfig`, error logging, and other production-relevant settings.

**Rubric:**
- 2 pts: Names at least two concrete risk scenarios (not just "it's risky") with clear cause-and-effect; mentions the timeout fields by name
- 1 pt: Correct general idea (no timeouts = risk) without specific scenarios or without naming the fields
- 0 pts: Claims `http.ListenAndServe` is fine or equivalent

---

### 2.3 — Graceful shutdown sequence [2 pts]

**Full credit answer:**
1. `signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)` returns a context that is cancelled when the OS sends SIGINT or SIGTERM (Ctrl+C or `kill`). The server goroutine starts normally. `<-ctx.Done()` blocks the main goroutine until the signal arrives.
2. When the signal fires, the main goroutine unblocks.
3. `srv.Shutdown(shutdownCtx)` tells the server to: stop accepting new connections, wait for all active handler goroutines to return, then close idle connections. It returns when all active requests have completed or the context deadline fires — whichever comes first.

`srv.Shutdown` is different from killing the process because it lets in-flight requests complete — clients do not see connection resets. A killed process drops all connections immediately, causing errors for in-flight requests.

A fresh context is needed because the signal context is already cancelled when the shutdown starts. Using the cancelled context as the shutdown deadline would cause `srv.Shutdown` to return immediately (the deadline is already past), potentially before in-flight requests complete.

**Rubric:**
- 2 pts: Explains the sequence correctly, explains what `srv.Shutdown` does differently from a kill, explains why a fresh context is needed
- 1 pt: Correct sequence but unclear on why a fresh context is needed, or correct on shutdown semantics but vague on the sequence
- 0 pts: Confuses `Shutdown` with `Close` (which is more abrupt), or misunderstands why the fresh context is needed

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — handleCreateProduct function [3 pts]

**Full credit answer:**
```go
type CreateProductRequest struct {
    Name  string  `json:"name"`
    Price float64 `json:"price"`
}

func writeJSONError(w http.ResponseWriter, status int, msg string) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(map[string]string{"error": msg})
}

func handleCreateProduct(w http.ResponseWriter, r *http.Request) {
    r.Body = http.MaxBytesReader(w, r.Body, 256<<10) // 256 KB

    var req CreateProductRequest
    dec := json.NewDecoder(r.Body)
    if err := dec.Decode(&req); err != nil {
        var maxErr *http.MaxBytesError
        switch {
        case errors.As(err, &maxErr):
            writeJSONError(w, http.StatusRequestEntityTooLarge, "request body too large")
        case errors.Is(err, io.EOF):
            writeJSONError(w, http.StatusBadRequest, "request body is empty")
        default:
            writeJSONError(w, http.StatusBadRequest, "invalid JSON")
        }
        return
    }

    if req.Name == "" {
        writeJSONError(w, http.StatusUnprocessableEntity, "name is required")
        return
    }
    if req.Price <= 0 {
        writeJSONError(w, http.StatusUnprocessableEntity, "price must be greater than zero")
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(req)
}
```

**Rubric:**
- 3 pts: All four error paths handled with correct status codes; `MaxBytesReader` used; `Content-Type` set before every write; `return` after every error; status 201 on success
- 2 pts: Correct logic but missing `MaxBytesReader`, or one error path uses the wrong status code, or missing `return` after one error
- 1 pt: Correct structure but multiple missing pieces
- 0 pts: Fundamental error handling mistakes (no error checking, wrong interface usage)

---

### 3.2 — TestHandleCreateProduct [3 pts]

**Full credit answer:**
```go
func TestHandleCreateProduct(t *testing.T) {
    tests := []struct {
        name       string
        body       string
        wantStatus int
        wantBody   string
    }{
        {"valid", `{"name":"Widget","price":9.99}`, http.StatusCreated, "Widget"},
        {"empty body", ``, http.StatusBadRequest, "empty"},
        {"missing name", `{"price":5.0}`, http.StatusUnprocessableEntity, "name is required"},
        {"zero price", `{"name":"X","price":0}`, http.StatusUnprocessableEntity, "greater than zero"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodPost, "/products",
                strings.NewReader(tt.body))
            rec := httptest.NewRecorder()

            handleCreateProduct(rec, req)

            if rec.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d; body: %s",
                    rec.Code, tt.wantStatus, rec.Body)
            }
            if tt.wantBody != "" && !strings.Contains(rec.Body.String(), tt.wantBody) {
                t.Errorf("body %q does not contain %q", rec.Body.String(), tt.wantBody)
            }
        })
    }
}
```

**Rubric:**
- 3 pts: Table-driven structure; `httptest.NewRequest` and `httptest.NewRecorder` used; at least four distinct test cases; both status code and body asserted; tests pass
- 2 pts: Correct structure but fewer than four test cases, or missing body assertions, or tests do not pass
- 1 pt: Tests exist and demonstrate correct usage of `httptest` but are incomplete
- 0 pts: Does not use `httptest`, or tests have fundamental structural errors

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — getUser handler bugs [3 pts] (1 pt each part)

**(a) Bugs identified:**

**Bug 1: Header set after WriteHeader in the error path.**
```go
w.WriteHeader(http.StatusNotFound) // headers flushed here
w.Header().Set("Content-Type", "application/json") // too late — ignored
```
`WriteHeader` flushes the headers. Setting `Content-Type` afterward has no effect — the client receives a response with no `Content-Type` header, and the status is 404.

**Bug 2: Missing `return` after the error branch.**
After writing the 404 response, execution continues to the success path:
```go
w.Header().Set("Content-Type", "application/json") // sets header for second write
json.NewEncoder(w).Encode(user)                     // writes a second response body
```
The client receives the error JSON body *followed immediately* by the user JSON body concatenated — making the body invalid JSON. The status code appears as 200 to the client because `w.WriteHeader(http.StatusNotFound)` was already called, but the second `WriteHeader`/write sequence produces a superposition effect (Go logs "superfluous response.WriteHeader call" to stderr).

**Bug 3: `Content-Type` not set before the first write in the success path.**
In the success path (when `err == nil`), `w.Header().Set` is called before `json.NewEncoder(w).Encode(user)`, which is correct for the success path — but only if there was no error. With Bug 2 present, the 404 path's `w.WriteHeader` has already been called so this header set in the success path may or may not take effect depending on buffering.

**(b) Corrected handler:**
```go
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    user, err := userStore.Get(r.Context(), id)
    if err != nil {
        w.Header().Set("Content-Type", "application/json") // set BEFORE WriteHeader
        w.WriteHeader(http.StatusNotFound)
        json.NewEncoder(w).Encode(map[string]string{"error": "user not found"})
        return // MUST return after error response
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}
```

**Rubric:**
- 1 pt for (a) Bug 1: Identifies header-after-WriteHeader ordering issue and explains the consequence
- 1 pt for (a) Bug 2: Identifies missing `return` and explains that the handler continues to write a second response
- 1 pt for (b): Corrected handler has `Content-Type` set before `WriteHeader`, `return` after the error response, and correct error handling pattern

**Teaching note:** Bug 2 (missing `return`) is the most common handler bug in production Go code. It is not detected at compile time and may not be obvious in testing if the success path's encoding fails silently.

---

## Section 5: Discussion — Answer Key

### 5.1 — stdlib vs third-party router [2 pts]

**Example strong answer:**
The claim is largely true for new services. Go 1.22's `http.ServeMux` now supports method-qualified patterns (`"GET /items/{id}"`), path parameters (`r.PathValue("id")`), wildcard suffixes (`{rest...}`), and automatic 405 responses for unregistered methods. For a service with 10–30 routes and straightforward middleware needs (logging, auth, recovery), the stdlib is sufficient and introduces zero dependencies.

**Scenarios where stdlib is sufficient:**
1. An internal microservice with a handful of REST endpoints — method routing and path parameters cover all routing needs
2. A CLI tool that exposes a local health/metrics HTTP server — minimal routing with no complex middleware requirements

**Scenarios where a third-party router may be worth it:**
1. A public API with 100+ routes needing route grouping, sub-routers with per-group middleware, and shared middleware that only applies to `/admin/...` but not `/public/...` — chi handles this cleanly; the stdlib has no route grouping primitive
2. A team already using gin with parameter binding, request validation middleware, and JSON rendering helpers — the productivity gain from gin's ecosystem exceeds the cost of the dependency

**Cost of each choice:**
- Stdlib: zero external dependencies, slightly more boilerplate for middleware chains and route grouping. `go vet` and `go build` always work without network access.
- Third-party router: one or more dependencies with their own upgrade cycles, security advisories, and API breaking changes. chi is very stable; gin has had occasional minor breaking changes.

**Rubric:**
- 2 pts: Correctly identifies that stdlib is sufficient for most services post-1.22; names concrete scenarios for both stdlib-sufficient and third-party-preferable cases; acknowledges the dependency cost tradeoff
- 1 pt: Correct general position but examples are vague or one-sided
- 0 pts: Incorrect claim (e.g., "stdlib routing is still inadequate in 1.22") or no concrete examples

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — statusRecorder and logging middleware [+5 pts]

**Full credit answer:**
```go
// statusRecorder captures the HTTP status code written by a handler
type statusRecorder struct {
    http.ResponseWriter
    code    int
    written bool
}

func (sr *statusRecorder) WriteHeader(code int) {
    if !sr.written {
        sr.code = code
        sr.written = true
    }
    sr.ResponseWriter.WriteHeader(code)
}

func (sr *statusRecorder) Write(b []byte) (int, error) {
    if !sr.written {
        // Implicit WriteHeader(200)
        sr.code = http.StatusOK
        sr.written = true
    }
    return sr.ResponseWriter.Write(b)
}

// WithLogging logs METHOD /path STATUS duration after every request
func WithLogging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        rec := &statusRecorder{ResponseWriter: w, code: http.StatusOK}
        next.ServeHTTP(rec, r)
        log.Printf("%s %s %d %s", r.Method, r.URL.Path, rec.code, time.Since(start))
    })
}

// Test
func TestWithLogging(t *testing.T) {
    var logBuf bytes.Buffer
    log.SetOutput(&logBuf)
    defer log.SetOutput(os.Stderr)

    t.Run("404 handler", func(t *testing.T) {
        logBuf.Reset()
        h404 := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            w.WriteHeader(http.StatusNotFound)
        })
        handler := WithLogging(h404)
        req := httptest.NewRequest(http.MethodGet, "/missing", nil)
        rec := httptest.NewRecorder()
        handler.ServeHTTP(rec, req)
        if !strings.Contains(logBuf.String(), "404") {
            t.Errorf("log %q does not contain 404", logBuf.String())
        }
    })

    t.Run("200 handler", func(t *testing.T) {
        logBuf.Reset()
        h200 := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            fmt.Fprintln(w, "ok")
        })
        handler := WithLogging(h200)
        req := httptest.NewRequest(http.MethodGet, "/ok", nil)
        rec := httptest.NewRecorder()
        handler.ServeHTTP(rec, req)
        if !strings.Contains(logBuf.String(), "200") {
            t.Errorf("log %q does not contain 200", logBuf.String())
        }
    })
}
```

**Rubric:**
- 5 pts: `statusRecorder` correctly implements both `WriteHeader` (stores code, delegates) and `Write` (handles implicit 200, delegates); `WithLogging` uses `statusRecorder` and logs status; tests verify both 404 and 200 cases
- 3 pts: `statusRecorder` works for the `WriteHeader` case but misses the implicit `Write`→200 case; or tests are present but incomplete
- 1 pt: `statusRecorder` struct defined but not fully implemented; or middleware pattern correct but does not capture status
- 0 pts: Fundamental misunderstanding of `http.ResponseWriter` embedding

---

## Common Wrong Answers Across the Test

1. **Setting headers after writing** — The most common mistake throughout this module. Reinforce: set `Content-Type` as the very first thing in any code path that writes a response. Create a `writeJSON` helper that always does this in the right order.

2. **Missing `return` after error responses** — If a student missed this in 4.1, send them back to exercises 3 and 7 where the pattern is demonstrated explicitly. This is a logic error the compiler does not catch.

3. **Using the cancelled signal context for srv.Shutdown** — Common in 2.3 answers. The signal context is already cancelled when the shutdown starts; passing it to `srv.Shutdown` gives the shutdown zero time. Always create a fresh `context.WithTimeout(context.Background(), ...)`.

4. **Confusing query parameters with path parameters** — `r.URL.Query().Get("id")` reads `?id=42`; `r.PathValue("id")` reads `{id}` from the route pattern. A student who answered `r.URL.Query().Get` for 1.2 does not yet understand Go 1.22 routing.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 1 need to re-read the Core Concepts section before attempting Section 2. The recall questions directly mirror the most important one-liners from each subsection.
- Students who miss 3.1 entirely (the `handleCreateProduct` function) should be directed to Exercise 3 and asked to redo it without hints before retaking the test.
- Section 4 (the debugging scenario) has three separable bugs; partial credit (1 or 2 bugs found) is common and appropriate. A student who finds two of three bugs is close to proficiency.
- The bonus question (statusRecorder) tests understanding at the `http.ResponseWriter` interface level — the ability to compose interface implementations. A student who scores 3/5 here is doing well; 5/5 requires understanding the implicit `WriteHeader(200)` triggered by `Write`.
- A score below 13/22 generally indicates the student needs more practice with the handler lifecycle (header ordering, the `return`-after-error pattern) before moving to [[go/14. Databases and Persistence]].

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
