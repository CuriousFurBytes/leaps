# Module 13: Web Services and APIs

[← Module 12: Advanced Concurrency Patterns](../12.%20Advanced%20Concurrency%20Patterns/) | [Topic Home](../README.md) | [Module 14: Databases and Persistence →](../14.%20Databases%20and%20Persistence/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate--advanced-blue)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [net/http Server Fundamentals](#nethttp-server-fundamentals)
  - [Go 1.22 Enhanced Routing](#go-122-enhanced-routing)
  - [Building JSON APIs](#building-json-apis)
  - [Middleware](#middleware)
  - [Request Context and Timeouts](#request-context-and-timeouts)
  - [Server Configuration and Graceful Shutdown](#server-configuration-and-graceful-shutdown)
  - [The http.Client](#the-httpclient)
  - [Structuring a Real Service](#structuring-a-real-service)
  - [Testing HTTP Handlers](#testing-http-handlers)
  - [Third-Party Routers: an Honest Note](#third-party-routers-an-honest-note)
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

This module covers **building production-quality HTTP services and JSON APIs in Go using the standard library**. Go's `net/http` package has been capable of powering real services since Go 1.0; Go 1.22 closed the last common gap by adding method-based routing and path parameters directly to `http.ServeMux`, making third-party routers optional for most services.

By the end of this module you will understand how to register handlers, parse and validate JSON request bodies, chain middleware, propagate cancellation via `context.Context`, configure server timeouts, and shut down gracefully under OS signals. You will also know how to structure a service so that it is testable from day one, using `httptest` to drive handlers without a real network.

**Difficulty:** Intermediate–Advanced &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Register HTTP handlers using `http.Handler`, `http.HandlerFunc`, and `http.ServeMux`, and explain the method dispatch lifecycle — _given an incoming request, trace exactly which handler runs and why_
2. Use Go 1.22 enhanced routing patterns (`"GET /items/{id}"`, `r.PathValue("id")`, wildcard `{rest...}`) to build clean, typed route tables without a third-party router — _convert a flat URL-matching if/else chain into an idiomatic Go 1.22 mux_
3. Build a JSON CRUD API: decode request bodies with size limits and input validation, return structured JSON error responses, and choose appropriate HTTP status codes — _write an endpoint that an external client can call and receive meaningful error messages from_
4. Write and chain middleware functions (logging, panic recovery, auth token extraction) using the handler-wrapping pattern — _add request ID injection and structured logging to any existing handler without modifying it_
5. Configure `http.Server` with read/write/idle timeouts, implement graceful shutdown with `signal.NotifyContext` and `server.Shutdown(ctx)`, and test handlers with `net/http/httptest` — _run a service that handles OS signals and drains in-flight requests before exiting_

---

## Prerequisites

### Required Modules

- [[go/8. Error Handling]] — you need to understand: the `error` interface, `fmt.Errorf` with `%w`, custom error types, and sentinel errors; HTTP error responses are structured errors and you will wrap them the same way
- [[go/11. Testing and Benchmarking]] — you need to understand: `testing.T`, table-driven tests, and `t.Run`; handler tests use the same patterns with an `httptest.ResponseRecorder` in place of a real connection
- [[go/12. Advanced Concurrency Patterns]] — you need to understand: `context.Context`, `context.WithCancel`, `context.WithTimeout`, and `context.WithValue`; every HTTP handler receives a `*http.Request` whose `.Context()` carries cancellation and per-request values

### Required Concepts

- **HTTP fundamentals** — understanding request methods (GET/POST/PUT/DELETE), status codes (200/201/400/404/500), headers (`Content-Type`, `Authorization`), and the request/response cycle; this module builds on those concepts throughout
- **JSON encoding** — knowing what JSON is and that `encoding/json` marshals Go structs to JSON and unmarshals JSON to Go structs; the details are covered here but the basic shape should not be a surprise
- **Interfaces** — `http.Handler` is an interface; middleware works by wrapping interfaces; service dependencies are injected via interfaces; if interfaces feel shaky, review [[go/6. Methods and Interfaces]] first

> [!TIP]
> If any of these prerequisites feel shaky, spend 15–30 minutes reviewing them before continuing.
> Gaps in prerequisites compound — a small weakness here will cause bigger confusion later.

---

## Why This Matters

Go is one of the most popular languages for building HTTP services. Docker, Kubernetes, Prometheus, Terraform, and countless production APIs are written in Go. The `net/http` package is part of the standard library and is performant, stable, and well-understood by the entire Go community.

Concretely, mastery of this module enables you to:

- **Build production APIs without a framework** — Go's standard library is now rich enough that most services need zero third-party router or framework dependencies; understanding `net/http` deeply means you are never at the mercy of a framework's upgrade cycle or breaking changes
- **Write testable services from day one** — `httptest.NewRecorder` and `httptest.NewServer` let you drive your handlers in unit and integration tests without spinning up a real server; the testing habits here tie directly to [[go/11. Testing and Benchmarking]]
- **Operate services safely** — graceful shutdown, per-request context propagation, and configured timeouts are not optional in production; a service that ignores `SIGTERM` drops in-flight requests and causes client errors during deploys

Without mastering this module, you would be unable to contribute meaningfully to any Go backend codebase, which is the primary domain where Go is used professionally.

---

## Historical Context

Go's `net/http` package shipped with Go 1.0 in **March 2012** and was already capable of serving real traffic — the Go playground, the Go documentation server, and various internal Google services used it from the start.

Key moments in the evolution of Go HTTP:

- **2012 — Go 1.0**: `http.ListenAndServe`, `http.ServeMux`, `http.Handler`, `http.HandlerFunc` all present. The mux can match paths but not methods; method checks must be done inside handlers.
- **2014 — Gorilla Mux and httprouter**: Community frustration with the stdlib mux's lack of method routing and path variables drives adoption of third-party routers. `gorilla/mux` and `julienschmidt/httprouter` become de facto standards.
- **2016 — net/http/httptest stabilises**: `httptest.NewRecorder` and `httptest.NewServer` become the idiomatic way to test handlers; no need for a running server in unit tests.
- **2021 — context integration**: `(*http.Request).Context()` has been present since Go 1.7 (2016); by 2021, the pattern of passing `context.Context` through every handler and service layer is firmly established.
- **2024 — Go 1.22**: The Go team ships **method and path pattern routing** directly in `http.ServeMux`. Patterns like `"GET /items/{id}"` and wildcards like `"GET /files/{rest...}"` work out of the box. `r.PathValue("id")` extracts path parameters. This removes the last major reason to reach for a third-party router for most services.

Understanding this history helps when reading Go codebases: pre-1.22 services use a third-party router or a hand-rolled method-dispatch layer; post-1.22 services can use the stdlib mux directly for most routing needs.

---

## Core Concepts

### net/http Server Fundamentals

The foundation of every Go HTTP server is the `http.Handler` interface:

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

Any type that implements `ServeHTTP` is a handler. The most common way to create a handler from a plain function is `http.HandlerFunc`, a type adapter that lets a function with the right signature satisfy `http.Handler`:

```go
package main

import (
    "fmt"
    "log"
    "net/http"
)

// greet is an ordinary function with the HandlerFunc signature
func greet(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Hello, World!")
}

func main() {
    mux := http.NewServeMux()
    // http.HandlerFunc converts greet to an http.Handler
    mux.Handle("/hello", http.HandlerFunc(greet))

    // Shorthand: HandleFunc registers the function directly
    mux.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, "pong")
    })

    log.Println("listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", mux))
}
```

```bash
curl http://localhost:8080/hello
# Hello, World!
curl http://localhost:8080/ping
# pong
```

`http.ListenAndServe` starts the server and blocks. It only returns when the server encounters an error; wrapping it in `log.Fatal` ensures the program exits with a message if that happens. For production use, configure an explicit `http.Server` struct (see [Server Configuration and Graceful Shutdown](#server-configuration-and-graceful-shutdown)).

**The default mux** (`http.DefaultServeMux`) is a package-level global that `http.Handle` and `http.HandleFunc` register into. Avoid it in production: any imported package can silently register routes, including `/debug/pprof` from `net/http/pprof`. Always create your own `http.NewServeMux()`.

---

### Go 1.22 Enhanced Routing

Before Go 1.22, `http.ServeMux` matched only path prefixes; method filtering required boilerplate inside every handler. Go 1.22 added two major enhancements:

**Method + path patterns:**

```go
mux := http.NewServeMux()

// Pattern: METHOD /path — only matches that method
mux.HandleFunc("GET /items", listItems)
mux.HandleFunc("POST /items", createItem)
mux.HandleFunc("GET /items/{id}", getItem)
mux.HandleFunc("PUT /items/{id}", updateItem)
mux.HandleFunc("DELETE /items/{id}", deleteItem)
```

**Extracting path parameters** with `r.PathValue`:

```go
func getItem(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id") // extracts {id} from the URL
    fmt.Fprintf(w, "item id: %s\n", id)
}
```

```bash
curl http://localhost:8080/items/42
# item id: 42
```

**Wildcard suffixes** match the rest of the path:

```go
// {rest...} matches everything after /files/
mux.HandleFunc("GET /files/{rest...}", serveFile)

func serveFile(w http.ResponseWriter, r *http.Request) {
    rest := r.PathValue("rest") // e.g., "images/logo.png"
    fmt.Fprintf(w, "file path: %s\n", rest)
}
```

**Pattern precedence rules** (exact beats prefix, more-specific beats less-specific):

```go
mux.HandleFunc("GET /items/{id}", getItem)   // matches /items/42
mux.HandleFunc("GET /items/new", getNewForm) // more specific — beats {id} for /items/new
```

The Go 1.22 mux uses a longest-match-wins rule: a literal path segment like `/items/new` takes priority over a wildcard `{id}` at the same position. This is deterministic and requires no special ordering.

**Automatic method handling:** If you register `"GET /foo"`, the mux automatically handles `HEAD /foo` as well (returning headers only, no body). An unmatched method returns `405 Method Not Allowed` with an `Allow` header listing registered methods for that path.

---

### Building JSON APIs

JSON APIs in Go follow a consistent four-step pattern for request handling:

1. Limit and decode the request body
2. Validate the decoded data
3. Call the service layer
4. Encode the response

```go
package main

import (
    "encoding/json"
    "errors"
    "fmt"
    "io"
    "log"
    "net/http"
)

// Item is the domain type
type Item struct {
    ID   int    `json:"id"`
    Name string `json:"name"`
    Price float64 `json:"price"`
}

// errorResponse is the standard error shape for all API errors
type errorResponse struct {
    Error string `json:"error"`
}

// writeJSON encodes v as JSON and writes it to w with the given status code
func writeJSON(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(v); err != nil {
        // At this point headers are already sent; log the encoding error
        log.Printf("writeJSON encode error: %v", err)
    }
}

// writeError writes a structured JSON error response
func writeError(w http.ResponseWriter, status int, msg string) {
    writeJSON(w, status, errorResponse{Error: msg})
}

// createItem handles POST /items
func createItem(w http.ResponseWriter, r *http.Request) {
    // Limit body size to 1 MB to prevent memory exhaustion
    r.Body = http.MaxBytesReader(w, r.Body, 1<<20)

    var item Item
    dec := json.NewDecoder(r.Body)
    dec.DisallowUnknownFields() // reject unexpected fields — helps catch client bugs

    if err := dec.Decode(&item); err != nil {
        var maxBytesErr *http.MaxBytesError
        switch {
        case errors.As(err, &maxBytesErr):
            writeError(w, http.StatusRequestEntityTooLarge, "request body too large")
        case err == io.EOF:
            writeError(w, http.StatusBadRequest, "request body is empty")
        default:
            writeError(w, http.StatusBadRequest, fmt.Sprintf("invalid JSON: %v", err))
        }
        return
    }

    // Input validation
    if item.Name == "" {
        writeError(w, http.StatusUnprocessableEntity, "name is required")
        return
    }
    if item.Price < 0 {
        writeError(w, http.StatusUnprocessableEntity, "price must be non-negative")
        return
    }

    // Simulate creation (a real service would call a store here)
    item.ID = 1

    writeJSON(w, http.StatusCreated, item)
}
```

```bash
# Valid request
curl -s -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","price":9.99}' | jq .
# {
#   "id": 1,
#   "name": "Widget",
#   "price": 9.99
# }

# Missing name
curl -s -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d '{"price":9.99}' | jq .
# {
#   "error": "name is required"
# }

# Malformed JSON
curl -s -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d 'not json' | jq .
# {
#   "error": "invalid JSON: ..."
# }
```

**Key rules:**
- Always set `Content-Type: application/json` before calling `WriteHeader` — once `WriteHeader` is called, headers are flushed and cannot be changed
- Use `http.MaxBytesReader` to limit body size — a missing limit allows a client to send an arbitrarily large body and exhaust memory
- `dec.DisallowUnknownFields()` turns extra JSON fields into decode errors — catching client bugs early; omit if your API must be lenient
- Error responses and their connection to [[go/8. Error Handling]]: `errors.As` to unwrap typed errors (`*http.MaxBytesError`) is the same wrapping pattern from error handling

**Status code guide:**

| Situation | Code |
|-----------|------|
| Created successfully | `201 Created` |
| Read/update/delete success | `200 OK` |
| No content to return | `204 No Content` |
| Malformed JSON / bad input | `400 Bad Request` |
| Not authenticated | `401 Unauthorized` |
| Authenticated but forbidden | `403 Forbidden` |
| Resource not found | `404 Not Found` |
| Validation error (semantic) | `422 Unprocessable Entity` |
| Request body too large | `413 Request Entity Too Large` |
| Internal server error | `500 Internal Server Error` |

---

### Middleware

Middleware in Go is a function that takes an `http.Handler` and returns an `http.Handler`. The returned handler wraps the original, adding behaviour before and/or after the inner handler runs.

```go
// Logger wraps h and logs every request's method, path, and duration
func Logger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)  // call the wrapped handler
        log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start))
    })
}

// Recoverer catches panics in the wrapped handler and returns a 500
func Recoverer(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                log.Printf("panic recovered: %v", rec)
                http.Error(w, "internal server error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}

// RequireJSON rejects requests without the correct Content-Type
func RequireJSON(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if r.Header.Get("Content-Type") != "application/json" {
            http.Error(w, `{"error":"Content-Type must be application/json"}`,
                http.StatusUnsupportedMediaType)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

**Chaining middleware** — apply right-to-left so the leftmost wrapper is the outermost:

```go
// chain applies middleware in order: Logger outermost, then Recoverer, then handler
func chain(h http.Handler, middleware ...func(http.Handler) http.Handler) http.Handler {
    for i := len(middleware) - 1; i >= 0; i-- {
        h = middleware[i](h)
    }
    return h
}

mux := http.NewServeMux()
mux.HandleFunc("POST /items", createItem)

// Wrap the entire mux with logging and panic recovery
handler := chain(mux, Logger, Recoverer)
log.Fatal(http.ListenAndServe(":8080", handler))
```

**Request ID injection** — a common middleware pattern using context values:

```go
type contextKey string

const requestIDKey contextKey = "requestID"

// RequestID injects a unique request ID into the context and response header
func RequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := fmt.Sprintf("%d", time.Now().UnixNano())
        ctx := context.WithValue(r.Context(), requestIDKey, id)
        w.Header().Set("X-Request-ID", id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// retrieving the request ID inside a handler:
func someHandler(w http.ResponseWriter, r *http.Request) {
    id, _ := r.Context().Value(requestIDKey).(string)
    log.Printf("handling request %s", id)
}
```

> [!NOTE]
> Always use a private, unexported type as the context key (the `contextKey` type above) rather than a bare `string`. This prevents key collisions between packages that both store values in the same context.

---

### Request Context and Timeouts

Every `*http.Request` carries a `context.Context` accessible via `r.Context()`. This context is cancelled when the client disconnects or when the server's `WriteTimeout` fires. Handlers should propagate this context to any downstream calls.

```go
func getItem(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    ctx := r.Context() // inherits server timeout and client cancellation

    // Pass ctx to the database call — if the client disconnects,
    // the DB query is cancelled too, freeing the DB connection
    item, err := store.GetItem(ctx, id)
    if err != nil {
        switch {
        case errors.Is(err, context.Canceled):
            // Client disconnected — no need to write a response
            return
        case errors.Is(err, ErrNotFound):
            writeError(w, http.StatusNotFound, "item not found")
        default:
            log.Printf("getItem: %v", err)
            writeError(w, http.StatusInternalServerError, "internal error")
        }
        return
    }

    writeJSON(w, http.StatusOK, item)
}
```

**Per-request timeout** — add a shorter timeout than the server-level `ReadTimeout`:

```go
func getItem(w http.ResponseWriter, r *http.Request) {
    // Individual handler gets 5s regardless of the server's WriteTimeout
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel() // always cancel to avoid leaking the timer goroutine

    item, err := store.GetItem(ctx, r.PathValue("id"))
    // ... handle err
}
```

This pattern ties directly to [[go/12. Advanced Concurrency Patterns]] — `context.WithTimeout` and `context.WithCancel` are the same tools used in goroutine fan-out patterns.

---

### Server Configuration and Graceful Shutdown

`http.ListenAndServe` is convenient for demos but bypasses important production settings. Always configure an explicit `http.Server`:

```go
srv := &http.Server{
    Addr:         ":8080",
    Handler:      handler,      // your mux, wrapped in middleware
    ReadTimeout:  5 * time.Second,  // time to read the full request header+body
    WriteTimeout: 10 * time.Second, // time to write the response
    IdleTimeout:  120 * time.Second, // keep-alive idle connection timeout
}
```

| Timeout | What it covers | Recommended value |
|---------|---------------|-------------------|
| `ReadTimeout` | Reading request headers and body | 5–10s |
| `WriteTimeout` | Writing the response | 10–30s (longer for file uploads/downloads) |
| `IdleTimeout` | Idle keep-alive connections | 60–180s |

**Graceful shutdown** with `signal.NotifyContext`:

```go
package main

import (
    "context"
    "log"
    "net/http"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })

    srv := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    // Derive a context that is cancelled on SIGINT or SIGTERM
    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    // Start server in a goroutine so main can wait for the signal
    go func() {
        log.Printf("starting server on %s", srv.Addr)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Block until the OS sends SIGINT or SIGTERM
    <-ctx.Done()
    log.Println("shutdown signal received")

    // Give in-flight requests up to 30 seconds to complete
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(shutdownCtx); err != nil {
        log.Fatalf("graceful shutdown failed: %v", err)
    }
    log.Println("server stopped cleanly")
}
```

`srv.Shutdown` stops accepting new connections, waits for in-flight requests to finish (up to the deadline in the context), then returns. After `Shutdown` returns, `srv.ListenAndServe` returns `http.ErrServerClosed` — that is expected, not an error.

---

### The http.Client

Making outbound HTTP requests uses `http.Client`. The most important rule: **reuse one client** — it manages a connection pool internally, and creating a new client per request bypasses the pool.

```go
// Package-level or injected via constructor — never create per-request
var httpClient = &http.Client{
    Timeout: 10 * time.Second, // total request timeout
}

func fetchUser(ctx context.Context, userID string) (*User, error) {
    url := "https://api.example.com/users/" + userID

    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return nil, fmt.Errorf("fetchUser: build request: %w", err)
    }
    req.Header.Set("Accept", "application/json")

    resp, err := httpClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("fetchUser: do request: %w", err)
    }
    defer resp.Body.Close() // always close the body — even on non-200 responses

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("fetchUser: unexpected status %d", resp.StatusCode)
    }

    var user User
    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        return nil, fmt.Errorf("fetchUser: decode response: %w", err)
    }
    return &user, nil
}
```

Use `http.NewRequestWithContext` (not `http.NewRequest`) so that the context's cancellation propagates to the outbound request. If the context is cancelled while waiting for the remote server, the request is aborted and an error is returned.

---

### Structuring a Real Service

The key principle: **handlers should not contain business logic or global state**. Instead, they depend on a service layer via interfaces, injected through constructors.

```go
// ItemStore is the interface that handlers depend on — not a concrete type
type ItemStore interface {
    GetItem(ctx context.Context, id string) (*Item, error)
    CreateItem(ctx context.Context, item Item) (*Item, error)
    ListItems(ctx context.Context) ([]Item, error)
    DeleteItem(ctx context.Context, id string) error
}

// ItemHandler holds the handler's dependencies
type ItemHandler struct {
    store ItemStore
    log   *log.Logger
}

// NewItemHandler constructs an ItemHandler with its dependencies
func NewItemHandler(store ItemStore, logger *log.Logger) *ItemHandler {
    return &ItemHandler{store: store, log: logger}
}

// RegisterRoutes registers the handler's routes on the given mux
func (h *ItemHandler) RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("GET /items", h.listItems)
    mux.HandleFunc("POST /items", h.createItem)
    mux.HandleFunc("GET /items/{id}", h.getItem)
    mux.HandleFunc("DELETE /items/{id}", h.deleteItem)
}

func (h *ItemHandler) getItem(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    item, err := h.store.GetItem(r.Context(), id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            writeError(w, http.StatusNotFound, "item not found")
            return
        }
        h.log.Printf("getItem %s: %v", id, err)
        writeError(w, http.StatusInternalServerError, "internal error")
        return
    }
    writeJSON(w, http.StatusOK, item)
}
```

This structure has a crucial benefit: `ItemStore` is an interface, so tests can provide a fake implementation (see Testing HTTP Handlers below) without touching a real database. This is the same dependency-injection pattern seen in large Go codebases like Kubernetes and Prometheus.

---

### Testing HTTP Handlers

Use `net/http/httptest` to test handlers without a real network — this ties to [[go/11. Testing and Benchmarking]]:

```go
package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

// fakeStore is a test double for ItemStore
type fakeStore struct {
    items map[string]*Item
}

func (f *fakeStore) GetItem(_ context.Context, id string) (*Item, error) {
    item, ok := f.items[id]
    if !ok {
        return nil, ErrNotFound
    }
    return item, nil
}
// (other methods elided for brevity)

func TestGetItem(t *testing.T) {
    store := &fakeStore{
        items: map[string]*Item{
            "42": {ID: 42, Name: "Widget", Price: 9.99},
        },
    }
    handler := NewItemHandler(store, log.New(io.Discard, "", 0))

    mux := http.NewServeMux()
    handler.RegisterRoutes(mux)

    tests := []struct {
        name       string
        id         string
        wantStatus int
        wantName   string
    }{
        {"found", "42", http.StatusOK, "Widget"},
        {"not found", "99", http.StatusNotFound, ""},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", "/items/"+tt.id, nil)
            rec := httptest.NewRecorder()

            mux.ServeHTTP(rec, req)

            if rec.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", rec.Code, tt.wantStatus)
            }
            if tt.wantName != "" {
                var item Item
                json.NewDecoder(rec.Body).Decode(&item)
                if item.Name != tt.wantName {
                    t.Errorf("name = %q, want %q", item.Name, tt.wantName)
                }
            }
        })
    }
}
```

`httptest.NewRequest` creates a `*http.Request` without a network connection. `httptest.NewRecorder` implements `http.ResponseWriter` and captures the status code, headers, and body in memory for assertion.

For integration tests that need a real network address (e.g., testing client-server interaction), use `httptest.NewServer`:

```go
ts := httptest.NewServer(mux)
defer ts.Close()

resp, err := http.Get(ts.URL + "/items/42")
```

---

### Third-Party Routers: an Honest Note

Before Go 1.22, third-party routers — **chi**, **gin**, **echo**, **gorilla/mux** — were the practical choice for any service needing method routing, path parameters, or middleware chains. They are well-maintained and widely used.

With Go 1.22, the stdlib mux supports method routing and path parameters natively. For most new services — especially internal services, microservices, and APIs with a modest number of routes — the stdlib is now sufficient.

Choose a third-party router when you need:
- A feature-rich middleware ecosystem (chi has a large collection of pre-built middleware)
- Route grouping or sub-routers with shared middleware (chi, gin, and echo all support this well)
- Regex path constraints or complex matching rules
- An opinionated full framework with parameter binding and validation (gin, echo)

The standard library is not inferior — it is intentionally minimal. For a 10-route internal API, `net/http` is the right choice. For a 200-route public API with complex middleware requirements, chi or gin may be worth the dependency.

---

### How the Concepts Fit Together

```
OS Signal (SIGTERM/SIGINT)
        │
        ▼
signal.NotifyContext ──► srv.Shutdown(ctx)  ← graceful drain
        │
        ▼
http.Server (timeouts)
        │ ListenAndServe
        ▼
Middleware chain ────────────────────────────────────┐
  Logger → Recoverer → RequestID → handler           │
        │                                            │
        ▼                                            │
http.ServeMux (Go 1.22 routing)                      │
  "GET /items/{id}" ──► ItemHandler.getItem          │
        │                                            │
        ▼                                            │
ItemStore interface                                  │
  (injected, no global state)                        │
        │                                            │
        ▼                                            │
context.Context (from r.Context())                   │
  WithTimeout → DB/external call ────────────────────┘
        │
        ▼
writeJSON / writeError (Content-Type, status, body)
```

Every layer has a single responsibility: the mux routes, the middleware augments, the handler orchestrates, the store persists. Context flows through every layer, carrying cancellation and per-request values.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Writing response headers after calling WriteHeader or writing the body**
>
> Once you call `w.WriteHeader(status)` or write any bytes to `w`, the HTTP headers are flushed to the client and cannot be changed. A common mistake is setting `Content-Type` after the fact.
>
> **Wrong:**
> ```go
> func handler(w http.ResponseWriter, r *http.Request) {
>     json.NewEncoder(w).Encode(data) // this implicitly calls WriteHeader(200)
>     w.Header().Set("Content-Type", "application/json") // too late — headers already sent
> }
> ```
>
> **Right:**
> ```go
> func handler(w http.ResponseWriter, r *http.Request) {
>     w.Header().Set("Content-Type", "application/json") // set BEFORE any write
>     json.NewEncoder(w).Encode(data)
> }
> ```
>
> **Why this matters:** The client receives the wrong `Content-Type` (or none at all), which breaks JSON parsing in browsers, CLIs, and API clients.

> [!WARNING]
> **Mistake 2: Not closing the response body when using http.Client**
>
> `resp.Body` must always be closed, even if you don't read it. Failing to close it leaks the underlying TCP connection back to the pool, eventually exhausting the connection pool and causing new requests to block or fail.
>
> **Wrong:**
> ```go
> resp, err := client.Get(url)
> if err != nil {
>     return err
> }
> // forgot defer resp.Body.Close()
> json.NewDecoder(resp.Body).Decode(&result)
> ```
>
> **Right:**
> ```go
> resp, err := client.Get(url)
> if err != nil {
>     return err
> }
> defer resp.Body.Close() // always, even on non-200 status
> json.NewDecoder(resp.Body).Decode(&result)
> ```

> [!WARNING]
> **Mistake 3: Returning from a handler after writing an error without a bare return**
>
> After calling `writeError` or `http.Error`, execution continues to the next line unless you return. This results in double-write attempts and confusing log output.
>
> **Wrong:**
> ```go
> func handler(w http.ResponseWriter, r *http.Request) {
>     if id == "" {
>         writeError(w, http.StatusBadRequest, "id required")
>         // forgot return — continues to the next lines!
>     }
>     writeJSON(w, http.StatusOK, item) // writes a second response
> }
> ```
>
> **Right:**
> ```go
> func handler(w http.ResponseWriter, r *http.Request) {
>     if id == "" {
>         writeError(w, http.StatusBadRequest, "id required")
>         return // stop processing
>     }
>     writeJSON(w, http.StatusOK, item)
> }
> ```

**Other pitfalls:**

- **Using http.DefaultServeMux in libraries** — any package that calls `http.Handle(...)` registers on the default mux; in server code this can expose unexpected debug endpoints like `/debug/pprof`; always use `http.NewServeMux()` explicitly
- **Not reading or discarding the request body** — if you return an error before decoding the full body, the connection cannot be reused for keep-alive; call `io.Copy(io.Discard, r.Body)` before returning to drain the body

---

## Mental Models

### Mental Model 1: Middleware as Onion Layers

Each middleware layer wraps the handler like a layer of an onion. The request enters from the outside (outermost middleware first) and the response travels back out the same layers in reverse order.

Imagine peeling an onion from the outside: the Logger layer is the outer skin — it sees the request first and the completed response last. The Recoverer layer is the next skin in. The actual handler is the core. When the handler panics, the Recoverer layer catches it before it propagates to the Logger layer.

This model breaks down when middleware needs to modify the response status code after the inner handler writes it — capturing the status for logging requires a custom `ResponseWriter` wrapper that intercepts `WriteHeader` calls.

### Mental Model 2: The Handler Contract

Think of `ServeHTTP(w, r)` as a contract: **exactly one complete response per call**. The handler receives `w` and must write exactly one response — a status code, headers, and a body. Writing two responses (e.g., a 400 and then a 200) corrupts the connection. Writing no response causes the client to hang.

This is most useful when reading handler code: trace every code path and ask "does this path write a response?" Every `if` branch that returns must have written a response first. The `return` after `writeError` is not optional.

### Mental Model 3: Context as a Request's Lifespan

A request's `context.Context` is the lifespan of the request. When the context is cancelled, the request is over — either because the client disconnected, the server timeout fired, or you explicitly timed out with `context.WithTimeout`. Any goroutine, database query, or outbound HTTP call that is doing work on behalf of that request should accept and check this context.

Think of context as a ticket that says "this work is still needed." The moment the ticket expires, every piece of infrastructure holding that ticket should stop working. This is the same model from [[go/12. Advanced Concurrency Patterns]].

> [!NOTE]
> No single mental model is perfect. Use Model 1 (onion layers) when designing or debugging middleware chains. Use Model 2 (one response per call) when auditing error handling paths in handlers. Use Model 3 (context as lifespan) when thinking about resource cleanup and cancellation propagation.

---

## Practical Examples

### Example 1: Minimal JSON API _(Basic)_

**Scenario:** A simple in-memory key-value store exposed as a JSON API.

**Goal:** Show the full lifecycle of an HTTP server: mux, routes, JSON encode/decode, and a clean shutdown.

```go
package main

import (
    "context"
    "encoding/json"
    "log"
    "net/http"
    "os/signal"
    "sync"
    "syscall"
    "time"
)

type store struct {
    mu   sync.RWMutex
    data map[string]string
}

func (s *store) get(key string) (string, bool) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    v, ok := s.data[key]
    return v, ok
}

func (s *store) set(key, value string) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.data[key] = value
}

func main() {
    kv := &store{data: make(map[string]string)}
    mux := http.NewServeMux()

    // GET /kv/{key}
    mux.HandleFunc("GET /kv/{key}", func(w http.ResponseWriter, r *http.Request) {
        key := r.PathValue("key")
        val, ok := kv.get(key)
        if !ok {
            http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
            return
        }
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"key": key, "value": val})
    })

    // PUT /kv/{key}
    mux.HandleFunc("PUT /kv/{key}", func(w http.ResponseWriter, r *http.Request) {
        key := r.PathValue("key")
        var body struct{ Value string `json:"value"` }
        if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
            http.Error(w, `{"error":"invalid json"}`, http.StatusBadRequest)
            return
        }
        kv.set(key, body.Value)
        w.WriteHeader(http.StatusNoContent)
    })

    srv := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    go func() {
        log.Println("listening on :8080")
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server: %v", err)
        }
    }()

    <-ctx.Done()
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    srv.Shutdown(shutdownCtx)
    log.Println("stopped")
}
```

```bash
# Store a value
curl -X PUT http://localhost:8080/kv/greeting \
  -H "Content-Type: application/json" \
  -d '{"value":"hello"}'

# Retrieve it
curl http://localhost:8080/kv/greeting
# {"key":"greeting","value":"hello"}

# Missing key
curl http://localhost:8080/kv/missing
# {"error":"not found"}
```

**What to notice:** `sync.RWMutex` protects the shared map — the handler is called concurrently by Go's HTTP server. The graceful shutdown waits up to 10 seconds for in-flight requests to complete. `http.ErrServerClosed` is the expected non-error return from `ListenAndServe` after `Shutdown` is called.

---

### Example 2: Middleware Chain _(Intermediate)_

**Scenario:** Adding logging and request-ID injection as reusable middleware.

**Goal:** Show how to chain two middleware functions so every request is logged with a unique ID.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "sync/atomic"
    "time"
)

// requestID is a monotonically increasing counter for demo purposes
// A production service would use a UUID or trace ID
var requestID atomic.Int64

type ctxKey string

const ctxKeyReqID ctxKey = "reqID"

// WithRequestID injects a unique ID into the context and response header
func WithRequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := fmt.Sprintf("req-%d", requestID.Add(1))
        ctx := context.WithValue(r.Context(), ctxKeyReqID, id)
        w.Header().Set("X-Request-ID", id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// WithLogging logs the method, path, duration, and request ID for each request
func WithLogging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        id, _ := r.Context().Value(ctxKeyReqID).(string)
        log.Printf("[%s] %s %s %s", id, r.Method, r.URL.Path, time.Since(start))
    })
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /hello", func(w http.ResponseWriter, r *http.Request) {
        id, _ := r.Context().Value(ctxKeyReqID).(string)
        fmt.Fprintf(w, "hello (request %s)\n", id)
    })

    // Apply middleware: WithRequestID runs first (innermost wrap), WithLogging outermost
    handler := WithLogging(WithRequestID(mux))
    log.Fatal(http.ListenAndServe(":8080", handler))
}
```

```bash
curl -s http://localhost:8080/hello
# hello (request req-1)

# Server logs:
# [req-1] GET /hello 42.1µs
```

**What to notice:** `WithRequestID` runs first (closest to the handler) so by the time `WithLogging` reads the ID from context after the request completes, it is available. The order of wrapping in `WithLogging(WithRequestID(mux))` means `WithLogging.ServeHTTP` calls `WithRequestID.ServeHTTP` which calls `mux.ServeHTTP`.

---

### Example 3: Full CRUD Handler with Testing _(Applied)_

**Scenario:** A testable CRUD handler for items using an injected interface store.

**Goal:** Show interface-based dependency injection and `httptest`-driven table tests.

```go
// item_handler_test.go
package main

import (
    "bytes"
    "context"
    "encoding/json"
    "errors"
    "io"
    "log"
    "net/http"
    "net/http/httptest"
    "testing"
)

var ErrNotFound = errors.New("not found")

type Item struct {
    ID   int    `json:"id"`
    Name string `json:"name"`
}

type ItemStore interface {
    GetItem(ctx context.Context, id string) (*Item, error)
}

type ItemHandler struct {
    store ItemStore
    log   *log.Logger
}

func NewItemHandler(s ItemStore) *ItemHandler {
    return &ItemHandler{store: s, log: log.New(io.Discard, "", 0)}
}

func (h *ItemHandler) RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("GET /items/{id}", h.getItem)
}

func (h *ItemHandler) getItem(w http.ResponseWriter, r *http.Request) {
    item, err := h.store.GetItem(r.Context(), r.PathValue("id"))
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            w.Header().Set("Content-Type", "application/json")
            w.WriteHeader(http.StatusNotFound)
            json.NewEncoder(w).Encode(map[string]string{"error": "not found"})
            return
        }
        w.WriteHeader(http.StatusInternalServerError)
        return
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(item)
}

// fakeStore is a test double
type fakeStore struct{ items map[string]*Item }

func (f *fakeStore) GetItem(_ context.Context, id string) (*Item, error) {
    if item, ok := f.items[id]; ok {
        return item, nil
    }
    return nil, ErrNotFound
}

func TestGetItem(t *testing.T) {
    store := &fakeStore{items: map[string]*Item{
        "1": {ID: 1, Name: "Widget"},
    }}
    mux := http.NewServeMux()
    NewItemHandler(store).RegisterRoutes(mux)

    tests := []struct {
        name       string
        id         string
        wantStatus int
        wantBody   string
    }{
        {"found", "1", http.StatusOK, "Widget"},
        {"not found", "99", http.StatusNotFound, "not found"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodGet, "/items/"+tt.id, nil)
            rec := httptest.NewRecorder()
            mux.ServeHTTP(rec, req)

            if rec.Code != tt.wantStatus {
                t.Fatalf("status = %d, want %d", rec.Code, tt.wantStatus)
            }
            body := rec.Body.String()
            if !bytes.Contains([]byte(body), []byte(tt.wantBody)) {
                t.Errorf("body %q does not contain %q", body, tt.wantBody)
            }
        })
    }
}
```

**What to notice:** No real server runs — `mux.ServeHTTP(rec, req)` drives the full handler stack in-process. The `fakeStore` implements `ItemStore` with a simple map, replacing any real database dependency. The table-driven test structure from [[go/11. Testing and Benchmarking]] applies unchanged.

---

### Example 4: Body Size Limit and Decode Error Handling _(Edge Case)_

**Scenario:** What happens when a client sends a 10 MB request body to an endpoint with a 1 MB limit?

```go
func createItem(w http.ResponseWriter, r *http.Request) {
    // Wrap the body reader with a 1 MB limit
    r.Body = http.MaxBytesReader(w, r.Body, 1<<20) // 1 MB

    var item Item
    if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
        var maxBytesErr *http.MaxBytesError
        if errors.As(err, &maxBytesErr) {
            // The body exceeded the limit — return 413
            w.Header().Set("Content-Type", "application/json")
            w.WriteHeader(http.StatusRequestEntityTooLarge)
            json.NewEncoder(w).Encode(map[string]string{"error": "request body too large"})
            return
        }
        // Some other decode error
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusBadRequest)
        json.NewEncoder(w).Encode(map[string]string{"error": "invalid json"})
        return
    }
    writeJSON(w, http.StatusCreated, item)
}
```

**Why this is important:** Without `http.MaxBytesReader`, a client can send a gigabyte body and the decoder reads it entirely into memory. For a service under load, this is a straightforward denial-of-service vector. `http.MaxBytesReader` stops reading after 1 MB and returns a `*http.MaxBytesError` that you can check with `errors.As` — the same pattern from [[go/8. Error Handling]].

---

## Related Concepts

Within this topic:

- [[go/8. Error Handling]] — structured JSON error responses use the same `fmt.Errorf` wrapping and `errors.Is`/`errors.As` unwrapping patterns; `*http.MaxBytesError` is a concrete error type you unwrap with `errors.As`
- [[go/11. Testing and Benchmarking]] — `httptest.NewRecorder` and `httptest.NewServer` slot directly into table-driven test patterns; handler benchmarks with `httptest` follow the same `b.N` loop structure
- [[go/12. Advanced Concurrency Patterns]] — `context.WithTimeout` and `context.WithCancel` used in handlers are the same tools used in goroutine pipelines and worker pools; graceful shutdown is a concurrency coordination problem
- [[go/14. Databases and Persistence]] — the `ItemStore` interface introduced here is implemented in the next module; the injected-store pattern is how handler tests stay database-free while integration tests use a real DB

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Hello Handler** _(Easy)_
>
> Register a `GET /hello` handler on a custom mux that returns a JSON object `{"message":"hello"}`. Test it with `httptest.NewRecorder`.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-hello-handler--easy--1-pt)

The exercises range from a single route to a full CRUD API with middleware and graceful shutdown. Complete at least Easy and Medium exercises before taking the test.

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
Build a URL shortener API — `POST /links` creates a short code mapping to a long URL (in-memory store), `GET /{code}` redirects. Add request logging middleware, structured JSON errors, and a graceful shutdown. Add handler tests with `httptest`. This exercises routing, JSON, middleware, context, and shutdown in a single cohesive project.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[pkg.go.dev/net/http](https://pkg.go.dev/net/http)** — The official package documentation; read the `ServeMux`, `Handler`, `HandlerFunc`, `Server`, `Client`, and `Request` type docs; the `ServeMux` docs include the full Go 1.22 routing pattern specification
2. **[Writing Web Applications — go.dev/doc/articles/wiki](https://go.dev/doc/articles/wiki)** — The official Go web application tutorial; builds an editable wiki from scratch using `net/http`; good for seeing the full lifecycle in one linear walkthrough
3. **[Routing Enhancements for Go 1.22 — The Go Blog](https://go.dev/blog/routing-enhancements)** — The definitive explanation of Go 1.22 routing patterns, method dispatch, path parameters, and precedence rules, written by the feature's author
4. **[Go 1.22 Release Notes — Enhanced Routing](https://go.dev/doc/go1.22#enhanced_routing_patterns)** — The release notes section covering the routing changes; terse but authoritative
5. **[pkg.go.dev/net/http/httptest](https://pkg.go.dev/net/http/httptest)** — Package documentation for `httptest.NewRecorder` and `httptest.NewServer`; contains runnable examples

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 13

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
