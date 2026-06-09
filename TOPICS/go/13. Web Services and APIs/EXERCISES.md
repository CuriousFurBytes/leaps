# Exercises — Module 13: Web Services and APIs

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read the code mentally — actually type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–15 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 20–35 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 40–70 min | 3 pts |
| ⭐ Expert | Open-ended; more than one good answer | 75+ min | 5 pts |

---

## Exercise 1: Hello Handler [🟢 Easy] [1 pt]

### Context
The most fundamental skill in this module is registering a route and returning a JSON response. This exercise verifies you can wire up a custom mux, write a handler, and drive it with `httptest` — the foundation for every subsequent exercise.

### Task
Write a complete Go program (or test file) that:
1. Creates a new `http.ServeMux` using `http.NewServeMux()`
2. Registers `"GET /hello"` to return the JSON body `{"message":"hello"}` with status 200 and `Content-Type: application/json`
3. Writes a test using `httptest.NewRecorder` that sends `GET /hello` to the mux and asserts: status is 200, `Content-Type` header contains `application/json`, and the body contains `"message"` and `"hello"`

### Requirements
- [ ] Uses `http.NewServeMux()` — not the default mux
- [ ] Sets `Content-Type: application/json` before writing the body
- [ ] Returns HTTP 200
- [ ] Test uses `httptest.NewRecorder` (no real server)
- [ ] Test checks status code, Content-Type header, and body

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Register with `mux.HandleFunc("GET /hello", func(w http.ResponseWriter, r *http.Request) { ... })`. Inside the handler, set the header with `w.Header().Set("Content-Type", "application/json")` before writing anything, then use `json.NewEncoder(w).Encode(map[string]string{"message": "hello"})`.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

In the test:
```go
req := httptest.NewRequest(http.MethodGet, "/hello", nil)
rec := httptest.NewRecorder()
mux.ServeHTTP(rec, req)
// check rec.Code, rec.Header().Get("Content-Type"), rec.Body.String()
```

</details>

### Expected Output / Acceptance Criteria
The test passes. When called with `GET /hello`, the handler returns:
- Status: `200 OK`
- Header: `Content-Type: application/json`
- Body: `{"message":"hello"}` (plus a trailing newline from `json.Encode`)

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func newMux() *http.ServeMux {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /hello", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"message": "hello"})
    })
    return mux
}

func TestHello(t *testing.T) {
    mux := newMux()
    req := httptest.NewRequest(http.MethodGet, "/hello", nil)
    rec := httptest.NewRecorder()
    mux.ServeHTTP(rec, req)

    if rec.Code != http.StatusOK {
        t.Errorf("status = %d, want %d", rec.Code, http.StatusOK)
    }
    if ct := rec.Header().Get("Content-Type"); !strings.Contains(ct, "application/json") {
        t.Errorf("Content-Type = %q, want application/json", ct)
    }
    body := rec.Body.String()
    if !strings.Contains(body, "hello") {
        t.Errorf("body %q does not contain 'hello'", body)
    }
}
```

**Explanation:**
`httptest.NewRecorder()` is an in-memory implementation of `http.ResponseWriter`. After calling `mux.ServeHTTP(rec, req)`, `rec.Code` holds the status code, `rec.Header()` holds the response headers, and `rec.Body` is a `*bytes.Buffer` containing the response body. No network is involved — this runs entirely in process. Setting `Content-Type` before writing the body is essential; any write to `w` implicitly calls `WriteHeader(200)` first, after which header changes are no-ops.

</details>

---

## Exercise 2: Path Parameter Routing [🟢 Easy] [1 pt]

### Context
Go 1.22's path parameter syntax is one of the most useful routing features added to the stdlib. This exercise ensures you can extract path values using `r.PathValue` and respond correctly when the parameter is absent or invalid.

### Task
Register `"GET /users/{id}"` on a mux. The handler should:
1. Extract the `id` path parameter with `r.PathValue("id")`
2. Respond with `{"id": "<id>"}` and status 200

Write a test that requests `/users/42` and asserts the response body contains `"42"`.

### Requirements
- [ ] Pattern uses the Go 1.22 syntax `"GET /users/{id}"`
- [ ] `r.PathValue("id")` is used to extract the parameter
- [ ] Returns JSON with the extracted ID
- [ ] Test verifies the ID appears in the response body

### Hints
<details>
<summary>Hint 1</summary>

`r.PathValue("id")` returns the string value matched by `{id}` in the registered pattern. It returns `""` if the parameter name does not exist in the pattern (not possible here, but worth knowing).

</details>

### Expected Output / Acceptance Criteria
`GET /users/42` → status 200, body contains `"42"`.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestPathParam(t *testing.T) {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
        id := r.PathValue("id")
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"id": id})
    })

    req := httptest.NewRequest(http.MethodGet, "/users/42", nil)
    rec := httptest.NewRecorder()
    mux.ServeHTTP(rec, req)

    if rec.Code != http.StatusOK {
        t.Fatalf("status = %d, want 200", rec.Code)
    }
    if !strings.Contains(rec.Body.String(), "42") {
        t.Errorf("body %q does not contain 42", rec.Body.String())
    }
}
```

**Explanation:**
The pattern `"GET /users/{id}"` restricts the route to GET requests only; a `POST /users/42` request would return 405. `r.PathValue("id")` returns the string that matched the `{id}` wildcard segment — in this case `"42"`. The value is always a string; numeric conversion (e.g., `strconv.Atoi`) is the handler's responsibility.

</details>

---

## Exercise 3: JSON CRUD Endpoint [🟡 Medium] [2 pts]

### Context
A minimal CRUD API is the most common deliverable in professional Go work. This exercise requires you to build a `POST /items` endpoint that decodes a JSON body, validates it, and returns the created item — covering the full decode-validate-respond cycle.

### Task
Build a `POST /items` handler that:
1. Limits the request body to 512 KB using `http.MaxBytesReader`
2. Decodes a JSON body into a struct with fields `name string` (required) and `quantity int` (must be ≥ 0)
3. Returns `400 Bad Request` with `{"error":"..."}` if the JSON is invalid or the body is empty
4. Returns `422 Unprocessable Entity` with `{"error":"name is required"}` if name is blank
5. Returns `422 Unprocessable Entity` with `{"error":"quantity must be non-negative"}` if quantity < 0
6. On success, returns `201 Created` with the decoded item as JSON

Write table-driven tests using `httptest` covering at least: valid input, empty body, missing name, negative quantity.

### Requirements
- [ ] `http.MaxBytesReader` is called before decoding
- [ ] All four validation paths tested
- [ ] Content-Type set before any write
- [ ] `return` called after every error response

### Hints
<details>
<summary>Hint 1</summary>

The struct with JSON tags:
```go
type CreateItemRequest struct {
    Name     string `json:"name"`
    Quantity int    `json:"quantity"`
}
```
Decode with `json.NewDecoder(r.Body).Decode(&req)`.

</details>

<details>
<summary>Hint 2</summary>

Check for `io.EOF` as a special case — it means the body was completely empty (no JSON at all). Check for `*http.MaxBytesError` with `errors.As` to distinguish a too-large body from other decode errors.

</details>

### Expected Output / Acceptance Criteria
Tests pass. Valid request `{"name":"Widget","quantity":5}` → 201 with `{"name":"Widget","quantity":5}`. Empty body → 400. Missing name → 422. Negative quantity → 422.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "encoding/json"
    "errors"
    "io"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

type CreateItemRequest struct {
    Name     string `json:"name"`
    Quantity int    `json:"quantity"`
}

func createItemHandler(w http.ResponseWriter, r *http.Request) {
    r.Body = http.MaxBytesReader(w, r.Body, 512<<10) // 512 KB

    var req CreateItemRequest
    dec := json.NewDecoder(r.Body)
    if err := dec.Decode(&req); err != nil {
        w.Header().Set("Content-Type", "application/json")
        var maxErr *http.MaxBytesError
        switch {
        case errors.As(err, &maxErr):
            w.WriteHeader(http.StatusRequestEntityTooLarge)
            json.NewEncoder(w).Encode(map[string]string{"error": "request body too large"})
        case errors.Is(err, io.EOF):
            w.WriteHeader(http.StatusBadRequest)
            json.NewEncoder(w).Encode(map[string]string{"error": "request body is empty"})
        default:
            w.WriteHeader(http.StatusBadRequest)
            json.NewEncoder(w).Encode(map[string]string{"error": "invalid JSON"})
        }
        return
    }

    if req.Name == "" {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusUnprocessableEntity)
        json.NewEncoder(w).Encode(map[string]string{"error": "name is required"})
        return
    }
    if req.Quantity < 0 {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusUnprocessableEntity)
        json.NewEncoder(w).Encode(map[string]string{"error": "quantity must be non-negative"})
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(req)
}

func TestCreateItem(t *testing.T) {
    tests := []struct {
        name       string
        body       string
        wantStatus int
        wantBody   string
    }{
        {"valid", `{"name":"Widget","quantity":5}`, http.StatusCreated, "Widget"},
        {"empty body", ``, http.StatusBadRequest, "empty"},
        {"missing name", `{"quantity":1}`, http.StatusUnprocessableEntity, "name is required"},
        {"negative quantity", `{"name":"X","quantity":-1}`, http.StatusUnprocessableEntity, "non-negative"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            body := strings.NewReader(tt.body)
            req := httptest.NewRequest(http.MethodPost, "/items", body)
            req.Header.Set("Content-Type", "application/json")
            rec := httptest.NewRecorder()

            createItemHandler(rec, req)

            if rec.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d; body: %s", rec.Code, tt.wantStatus, rec.Body)
            }
            if !strings.Contains(rec.Body.String(), tt.wantBody) {
                t.Errorf("body %q does not contain %q", rec.Body.String(), tt.wantBody)
            }
        })
    }
}
```

**Explanation:**
`http.MaxBytesReader` wraps the body and returns `*http.MaxBytesError` when the limit is exceeded. The `errors.As` check handles that case distinctly. `io.EOF` from `Decode` means the body was empty (as opposed to `io.ErrUnexpectedEOF` which means truncated JSON). The `return` after every error path is mandatory — without it, the handler continues to the success path and writes a second response.

</details>

---

## Exercise 4: Logging Middleware [🟡 Medium] [2 pts]

### Context
Middleware is the standard Go pattern for cross-cutting concerns. This exercise requires you to write a logging middleware that wraps any handler and logs each request's method, path, and duration — demonstrating that you understand the handler-wrapping function signature.

### Task
Write a `WithLogging` middleware function with signature `func WithLogging(next http.Handler) http.Handler`. It should:
1. Record the current time before calling `next.ServeHTTP`
2. Call `next.ServeHTTP(w, r)`
3. After the call returns, log `METHOD /path duration` using `log.Printf`

Then register a `GET /status` handler on a mux, wrap the mux with `WithLogging`, and write a test that calls the endpoint and verifies it returns 200 (the logging itself does not need to be asserted in the test).

### Requirements
- [ ] `WithLogging` signature is `func(http.Handler) http.Handler`
- [ ] Uses `time.Now()` before the call and `time.Since(start)` after
- [ ] The test wraps the whole mux: `handler := WithLogging(mux)`
- [ ] Test drives `handler.ServeHTTP(rec, req)` — not `mux.ServeHTTP`

### Hints
<details>
<summary>Hint 1</summary>

The middleware template is always:
```go
func WithLogging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf(...)
    })
}
```

</details>

### Expected Output / Acceptance Criteria
Test passes. When called, the server logs a line like `GET /status 42µs`.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func WithLogging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start))
    })
}

func TestLoggingMiddleware(t *testing.T) {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /status", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, "ok")
    })

    handler := WithLogging(mux)

    req := httptest.NewRequest(http.MethodGet, "/status", nil)
    rec := httptest.NewRecorder()
    handler.ServeHTTP(rec, req) // drives the full middleware + handler stack

    if rec.Code != http.StatusOK {
        t.Errorf("status = %d, want 200", rec.Code)
    }
}
```

**Explanation:**
The `return http.HandlerFunc(...)` is the core of all Go middleware. `http.HandlerFunc` is a type adapter that converts a function with the `ServeHTTP`-compatible signature into an `http.Handler`. The `next.ServeHTTP(w, r)` call transfers control to the wrapped handler. Code before that call runs as the "before" phase; code after it runs as the "after" phase. In the test, we call `handler.ServeHTTP` (the wrapped version), not `mux.ServeHTTP` — this ensures the middleware actually runs.

</details>

---

## Exercise 5: Panic Recovery Middleware [🟡 Medium] [2 pts]

### Context
In production, a handler that panics should not crash the whole server — it should return a 500 and let other requests continue. This exercise asks you to write a `Recoverer` middleware that uses `defer`/`recover` to catch panics and return a structured JSON error instead.

### Task
Write a `Recoverer` middleware that:
1. Uses `defer func() { ... }()` with `recover()` inside the handler wrapper
2. If `recover()` returns a non-nil value, logs the panic value and writes a JSON `{"error":"internal server error"}` with status 500
3. Otherwise lets the request proceed normally

Write two tests: one where the wrapped handler panics (assert status 500 and JSON error body), and one where it does not (assert status 200).

### Requirements
- [ ] Uses `defer` + `recover()` inside the returned HandlerFunc
- [ ] Panicking handler test → 500 with JSON body containing `"error"`
- [ ] Non-panicking handler test → 200
- [ ] Sets `Content-Type: application/json` on the error response

### Hints
<details>
<summary>Hint 1</summary>

```go
func Recoverer(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                // write 500 here
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

</details>

### Expected Output / Acceptance Criteria
Panicking handler test: status 500, body contains `"error"`. Normal handler test: status 200.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func Recoverer(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                log.Printf("panic recovered: %v", rec)
                w.Header().Set("Content-Type", "application/json")
                w.WriteHeader(http.StatusInternalServerError)
                json.NewEncoder(w).Encode(map[string]string{"error": "internal server error"})
            }
        }()
        next.ServeHTTP(w, r)
    })
}

func TestRecoverer(t *testing.T) {
    t.Run("panicking handler returns 500", func(t *testing.T) {
        panicker := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            panic("something went wrong")
        })
        handler := Recoverer(panicker)
        req := httptest.NewRequest(http.MethodGet, "/", nil)
        rec := httptest.NewRecorder()
        handler.ServeHTTP(rec, req)

        if rec.Code != http.StatusInternalServerError {
            t.Errorf("status = %d, want 500", rec.Code)
        }
        if !strings.Contains(rec.Body.String(), "error") {
            t.Errorf("body %q missing 'error' key", rec.Body.String())
        }
    })

    t.Run("normal handler returns 200", func(t *testing.T) {
        normal := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            fmt.Fprintln(w, "ok")
        })
        handler := Recoverer(normal)
        req := httptest.NewRequest(http.MethodGet, "/", nil)
        rec := httptest.NewRecorder()
        handler.ServeHTTP(rec, req)

        if rec.Code != http.StatusOK {
            t.Errorf("status = %d, want 200", rec.Code)
        }
    })
}
```

**Explanation:**
`recover()` only catches panics when called directly inside a deferred function — this is why the `defer func() { if rec := recover()... }()` pattern is necessary. A bare `defer recover()` would not work because `recover`'s return value would be discarded. Note that headers cannot be set reliably after a panic if the handler has already started writing — the `Recoverer` here assumes the handler panicked before writing any response, which is the common case. A more robust implementation would use a status-capturing `ResponseWriter` wrapper.

</details>

---

## Exercise 6: Graceful Shutdown [🔴 Hard] [3 pts]

### Context
A server that exits immediately on SIGTERM drops in-flight requests. Production services must drain connections gracefully. This exercise requires you to write a full server with signal handling and graceful shutdown — the most important operational pattern in this module.

### Task
Write a complete `main.go` that:
1. Creates a mux with `"GET /slow"` handler that sleeps for 2 seconds and then returns `{"status":"done"}`
2. Configures an `http.Server` with `ReadTimeout: 5s`, `WriteTimeout: 15s`, `IdleTimeout: 30s`
3. Starts the server in a goroutine
4. Uses `signal.NotifyContext` to watch for `SIGINT` and `SIGTERM`
5. Blocks on `<-ctx.Done()`
6. On signal, calls `srv.Shutdown` with a 10-second context timeout
7. Logs "server stopped cleanly" after shutdown completes

You do not need a test for this exercise — describe in a comment how you would manually verify graceful shutdown (start server, curl `/slow` in one terminal, send SIGTERM in another, observe that the curl completes before the server exits).

### Requirements
- [ ] `signal.NotifyContext` used (not `signal.Notify` channel pattern)
- [ ] Server started in a goroutine
- [ ] `http.ErrServerClosed` distinguished from real errors
- [ ] `srv.Shutdown` called with a deadline context, not `context.Background()` directly
- [ ] Appropriate log messages at startup and shutdown

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
defer stop()

go func() {
    if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
        log.Fatalf("server: %v", err)
    }
}()

<-ctx.Done()
// now shutdown
```

</details>

<details>
<summary>Hint 2 (shutdown context)</summary>

After `ctx.Done()` fires, the `ctx` is already cancelled. You need a *fresh* context for the shutdown deadline:
```go
shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
srv.Shutdown(shutdownCtx)
```

</details>

### Expected Output / Acceptance Criteria
Program compiles and runs. Log output shows "listening on :8080" at start. After receiving SIGTERM (Ctrl+C), logs "shutdown signal received" and "server stopped cleanly".

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "encoding/json"
    "log"
    "net/http"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    mux := http.NewServeMux()

    // A deliberately slow handler to demonstrate graceful drain
    mux.HandleFunc("GET /slow", func(w http.ResponseWriter, r *http.Request) {
        select {
        case <-time.After(2 * time.Second):
            // completed normally
        case <-r.Context().Done():
            // client disconnected or server shutting down
            return
        }
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"status": "done"})
    })

    srv := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  30 * time.Second,
    }

    // signal.NotifyContext returns a context that is cancelled on SIGINT/SIGTERM
    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    go func() {
        log.Printf("listening on %s", srv.Addr)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Block until OS signal
    <-ctx.Done()
    log.Println("shutdown signal received")

    // Give in-flight requests up to 10 seconds to complete
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    if err := srv.Shutdown(shutdownCtx); err != nil {
        log.Fatalf("graceful shutdown failed: %v", err)
    }
    log.Println("server stopped cleanly")
}

// Manual verification:
// Terminal 1: go run main.go
// Terminal 2: curl http://localhost:8080/slow  (takes 2s)
// Terminal 3: kill -TERM <pid>  (or press Ctrl+C in Terminal 1 while curl is running)
// Expected: curl completes with {"status":"done"}, server logs "server stopped cleanly"
```

**Step-by-step explanation:**
1. `signal.NotifyContext` returns a context cancelled when SIGINT or SIGTERM is received; `stop()` deregisters the signal handling and should always be called (hence `defer stop()`).
2. The server goroutine's `ListenAndServe` returns `http.ErrServerClosed` after `Shutdown` is called — this is the expected non-error condition; any other error is fatal.
3. `<-ctx.Done()` blocks until the signal arrives.
4. `context.WithTimeout(context.Background(), 10*time.Second)` creates a *new* context for the shutdown — the original `ctx` is already cancelled.
5. `srv.Shutdown` stops accepting new connections and waits for all active handlers to return within the deadline.
6. The `/slow` handler uses `select` with `r.Context().Done()` — if the server shuts down while the handler is sleeping, the handler exits early rather than blocking shutdown.

</details>

---

## Exercise 7: Interface-Based Service with Full Handler Suite [⭐ Expert] [5 pts]

### Context
Professional Go services separate HTTP concerns (routing, encoding, status codes) from business logic (the store/service layer) using interfaces. This exercise asks you to build a small but complete CRUD API — create, read, list, delete — using constructor injection so the handler tests never touch a real store.

### Task
Implement the following:

1. Define an `Item` struct: `ID string`, `Name string`, `Done bool` (JSON tags matching lowercase)
2. Define a `TodoStore` interface with methods: `List(ctx) ([]Item, error)`, `Get(ctx, id string) (*Item, error)`, `Create(ctx, item Item) (*Item, error)`, `Delete(ctx, id string) error` — where the `Get` and `Delete` methods return a sentinel `ErrNotFound` when the ID does not exist
3. Implement `MemoryStore` (an in-memory map protected by `sync.RWMutex`) satisfying `TodoStore`
4. Build a `TodoHandler` with a `NewTodoHandler(store TodoStore) *TodoHandler` constructor and a `RegisterRoutes(mux *http.ServeMux)` method that registers: `GET /todos` (list), `POST /todos` (create), `GET /todos/{id}` (get), `DELETE /todos/{id}` (delete)
5. Write table-driven tests for at least `GET /todos/{id}` and `DELETE /todos/{id}`, using a `fakeTodoStore` test double — no `MemoryStore` in tests

### Requirements
- [ ] `TodoStore` is an interface — `TodoHandler` never imports or references `MemoryStore` directly
- [ ] `ErrNotFound` is a sentinel error returned by `Get` and `Delete`
- [ ] Handlers use `errors.Is(err, ErrNotFound)` and return 404 accordingly
- [ ] All handlers set `Content-Type: application/json` and correct status codes (201 for create, 204 for delete, 404 for missing)
- [ ] Tests use `fakeTodoStore` (not `MemoryStore`)
- [ ] Tests drive `mux.ServeHTTP(rec, req)` — no real server

### Hints
<details>
<summary>Hint 1 (interface design)</summary>

```go
var ErrNotFound = errors.New("not found")

type TodoStore interface {
    List(ctx context.Context) ([]Item, error)
    Get(ctx context.Context, id string) (*Item, error)
    Create(ctx context.Context, item Item) (*Item, error)
    Delete(ctx context.Context, id string) error
}
```

</details>

<details>
<summary>Hint 2 (handler structure)</summary>

```go
type TodoHandler struct {
    store TodoStore
}

func NewTodoHandler(store TodoStore) *TodoHandler {
    return &TodoHandler{store: store}
}

func (h *TodoHandler) RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("GET /todos", h.list)
    mux.HandleFunc("POST /todos", h.create)
    mux.HandleFunc("GET /todos/{id}", h.get)
    mux.HandleFunc("DELETE /todos/{id}", h.delete)
}
```

</details>

<details>
<summary>Hint 3 (fakeTodoStore for tests)</summary>

```go
type fakeTodoStore struct {
    items map[string]*Item
}

func (f *fakeTodoStore) Get(_ context.Context, id string) (*Item, error) {
    if item, ok := f.items[id]; ok {
        return item, nil
    }
    return nil, ErrNotFound
}
// implement other methods returning zero values / ErrNotFound as appropriate
```

</details>

### Expected Output / Acceptance Criteria
All tests pass. `POST /todos` with valid JSON → 201 with created item. `GET /todos/nonexistent` → 404 with JSON error. `DELETE /todos/existing` → 204. `DELETE /todos/nonexistent` → 404.

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "context"
    "encoding/json"
    "errors"
    "fmt"
    "io"
    "net/http"
    "net/http/httptest"
    "strings"
    "sync"
    "testing"
)

// Domain types and sentinel errors

var ErrNotFound = errors.New("not found")

type Item struct {
    ID   string `json:"id"`
    Name string `json:"name"`
    Done bool   `json:"done"`
}

// TodoStore interface — the contract for the handler's dependency

type TodoStore interface {
    List(ctx context.Context) ([]Item, error)
    Get(ctx context.Context, id string) (*Item, error)
    Create(ctx context.Context, item Item) (*Item, error)
    Delete(ctx context.Context, id string) error
}

// MemoryStore — production implementation (not used in tests)

type MemoryStore struct {
    mu    sync.RWMutex
    items map[string]*Item
    next  int
}

func NewMemoryStore() *MemoryStore {
    return &MemoryStore{items: make(map[string]*Item)}
}

func (m *MemoryStore) List(_ context.Context) ([]Item, error) {
    m.mu.RLock()
    defer m.mu.RUnlock()
    out := make([]Item, 0, len(m.items))
    for _, v := range m.items {
        out = append(out, *v)
    }
    return out, nil
}

func (m *MemoryStore) Get(_ context.Context, id string) (*Item, error) {
    m.mu.RLock()
    defer m.mu.RUnlock()
    item, ok := m.items[id]
    if !ok {
        return nil, ErrNotFound
    }
    return item, nil
}

func (m *MemoryStore) Create(_ context.Context, item Item) (*Item, error) {
    m.mu.Lock()
    defer m.mu.Unlock()
    m.next++
    item.ID = fmt.Sprintf("%d", m.next)
    m.items[item.ID] = &item
    return &item, nil
}

func (m *MemoryStore) Delete(_ context.Context, id string) error {
    m.mu.Lock()
    defer m.mu.Unlock()
    if _, ok := m.items[id]; !ok {
        return ErrNotFound
    }
    delete(m.items, id)
    return nil
}

// TodoHandler — HTTP handler depending on TodoStore interface

type TodoHandler struct {
    store TodoStore
}

func NewTodoHandler(store TodoStore) *TodoHandler {
    return &TodoHandler{store: store}
}

func (h *TodoHandler) RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("GET /todos", h.list)
    mux.HandleFunc("POST /todos", h.create)
    mux.HandleFunc("GET /todos/{id}", h.get)
    mux.HandleFunc("DELETE /todos/{id}", h.delete)
}

func writeJSON(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(v)
}

func (h *TodoHandler) list(w http.ResponseWriter, r *http.Request) {
    items, err := h.store.List(r.Context())
    if err != nil {
        writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "internal error"})
        return
    }
    if items == nil {
        items = []Item{}
    }
    writeJSON(w, http.StatusOK, items)
}

func (h *TodoHandler) create(w http.ResponseWriter, r *http.Request) {
    r.Body = http.MaxBytesReader(w, r.Body, 1<<20)
    var item Item
    if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid JSON"})
        return
    }
    if item.Name == "" {
        writeJSON(w, http.StatusUnprocessableEntity, map[string]string{"error": "name is required"})
        return
    }
    created, err := h.store.Create(r.Context(), item)
    if err != nil {
        writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "internal error"})
        return
    }
    writeJSON(w, http.StatusCreated, created)
}

func (h *TodoHandler) get(w http.ResponseWriter, r *http.Request) {
    item, err := h.store.Get(r.Context(), r.PathValue("id"))
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
            return
        }
        writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "internal error"})
        return
    }
    writeJSON(w, http.StatusOK, item)
}

func (h *TodoHandler) delete(w http.ResponseWriter, r *http.Request) {
    err := h.store.Delete(r.Context(), r.PathValue("id"))
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
            return
        }
        writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "internal error"})
        return
    }
    w.WriteHeader(http.StatusNoContent)
}

// fakeTodoStore — test double

type fakeTodoStore struct {
    items map[string]*Item
}

func (f *fakeTodoStore) List(_ context.Context) ([]Item, error) {
    out := make([]Item, 0)
    for _, v := range f.items {
        out = append(out, *v)
    }
    return out, nil
}

func (f *fakeTodoStore) Get(_ context.Context, id string) (*Item, error) {
    if item, ok := f.items[id]; ok {
        return item, nil
    }
    return nil, ErrNotFound
}

func (f *fakeTodoStore) Create(_ context.Context, item Item) (*Item, error) {
    item.ID = "test-id"
    f.items[item.ID] = &item
    return &item, nil
}

func (f *fakeTodoStore) Delete(_ context.Context, id string) error {
    if _, ok := f.items[id]; !ok {
        return ErrNotFound
    }
    delete(f.items, id)
    return nil
}

// Tests

func newTestMux(store TodoStore) *http.ServeMux {
    mux := http.NewServeMux()
    NewTodoHandler(store).RegisterRoutes(mux)
    return mux
}

func TestGet(t *testing.T) {
    store := &fakeTodoStore{items: map[string]*Item{
        "1": {ID: "1", Name: "Buy milk", Done: false},
    }}
    mux := newTestMux(store)

    tests := []struct {
        name       string
        id         string
        wantStatus int
        wantBody   string
    }{
        {"found", "1", http.StatusOK, "Buy milk"},
        {"not found", "99", http.StatusNotFound, "not found"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodGet, "/todos/"+tt.id, nil)
            rec := httptest.NewRecorder()
            mux.ServeHTTP(rec, req)
            if rec.Code != tt.wantStatus {
                t.Fatalf("status = %d, want %d", rec.Code, tt.wantStatus)
            }
            if !strings.Contains(rec.Body.String(), tt.wantBody) {
                t.Errorf("body %q does not contain %q", rec.Body.String(), tt.wantBody)
            }
        })
    }
}

func TestDelete(t *testing.T) {
    tests := []struct {
        name       string
        id         string
        wantStatus int
    }{
        {"existing", "1", http.StatusNoContent},
        {"nonexistent", "99", http.StatusNotFound},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            store := &fakeTodoStore{items: map[string]*Item{
                "1": {ID: "1", Name: "Buy milk"},
            }}
            mux := newTestMux(store)
            req := httptest.NewRequest(http.MethodDelete, "/todos/"+tt.id, nil)
            rec := httptest.NewRecorder()
            mux.ServeHTTP(rec, req)
            if rec.Code != tt.wantStatus {
                t.Fatalf("status = %d, want %d", rec.Code, tt.wantStatus)
            }
        })
    }
}

func main() {
    mux := http.NewServeMux()
    NewTodoHandler(NewMemoryStore()).RegisterRoutes(mux)
    // (graceful shutdown omitted for brevity — see Exercise 6)
    _ = http.ListenAndServe(":8080", mux)
    _ = io.Discard
}
```

**Why this approach:**
Separating `TodoStore` (interface) from `MemoryStore` (implementation) means tests never require a running database, a real file, or any external resource. The `fakeTodoStore` is a minimal in-memory stub that satisfies the interface — it is not a mock framework and does not need to be. Each test creates its own `fakeTodoStore` with precisely the state it needs, making tests deterministic and independent. The `TodoHandler` does not know or care whether it is talking to `MemoryStore`, a PostgreSQL-backed store, or a fake — this is the point of interface-based dependency injection.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Hello Handler | — | —/1 | — | — |
| Exercise 2 — Path Parameter Routing | — | —/1 | — | — |
| Exercise 3 — JSON CRUD Endpoint | — | —/2 | — | — |
| Exercise 4 — Logging Middleware | — | —/2 | — | — |
| Exercise 5 — Panic Recovery Middleware | — | —/2 | — | — |
| Exercise 6 — Graceful Shutdown | — | —/3 | — | — |
| Exercise 7 — Interface-Based Service | — | —/5 | — | — |
| **Total** | | **—/16** | | |

**Passing threshold:** 10/16 (63%). Aim for 13/16 (81%) before taking the test.
