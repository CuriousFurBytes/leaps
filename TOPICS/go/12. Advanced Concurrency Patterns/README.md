# Module 12: Advanced Concurrency Patterns

[← Module 11: Testing and Benchmarking](../11.%20Testing%20and%20Benchmarking/) | [Topic Home](../README.md) | [Module 13: Web Services and APIs →](../13.%20Web%20Services%20and%20APIs/)

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
  - [context.Context — Cancellation, Deadlines, and Request-Scoped Values](#contextcontext--cancellation-deadlines-and-request-scoped-values)
  - [Pipelines](#pipelines)
  - [Fan-Out / Fan-In](#fan-out--fan-in)
  - [Bounded Worker Pools](#bounded-worker-pools)
  - [Semaphores via Buffered Channels](#semaphores-via-buffered-channels)
  - [Rate Limiting](#rate-limiting)
  - [sync/atomic and Typed Atomics](#syncatomic-and-typed-atomics)
  - [sync.Pool — Object Reuse](#syncpool--object-reuse)
  - [errgroup — Grouped Goroutines with Error Propagation](#errgroup--grouped-goroutines-with-error-propagation)
  - [Detecting and Avoiding Goroutine Leaks](#detecting-and-avoiding-goroutine-leaks)
  - [Graceful Shutdown](#graceful-shutdown)
  - [The Race Detector in CI](#the-race-detector-in-ci)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Mistakes](#common-mistakes)
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

This module covers **advanced concurrency patterns** that professional Go engineers use daily: propagating cancellation with `context.Context`, structuring work as pipelines, distributing load with fan-out/fan-in and worker pools, enforcing concurrency limits with semaphores and rate limiters, performing lock-free atomic operations, reusing objects with `sync.Pool`, and managing groups of goroutines with `errgroup`. It also covers the two most important safety practices: avoiding goroutine leaks and running `-race` in CI.

By the end of this module, you will know not just the patterns themselves but the reasoning behind them — why `context` belongs at the top of every call tree, what causes goroutine leaks and how to prevent them, and when atomics are appropriate versus when a mutex is clearer.

This module assumes you are fluent with [[go/9. Concurrency]] fundamentals: goroutines, channels, `select`, `sync.Mutex`, `sync.WaitGroup`, and `sync.Once`.

**Difficulty:** Advanced &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Use `context.WithCancel`, `WithTimeout`, `WithDeadline`, and `WithValue` correctly — _write a function that cancels a pipeline when the first error occurs or a deadline expires_
2. Build a multi-stage pipeline with proper cancellation and cleanup — _implement a grep-like pipeline that reads, filters, and prints lines, stopping cleanly on `ctx.Done()`_
3. Implement a bounded worker pool and a semaphore — _process a slice of URLs with at most N concurrent HTTP requests_
4. Use `atomic.Int64` and `atomic.Pointer` safely — _explain when CAS (compare-and-swap) is appropriate vs a mutex_
5. Use `errgroup.WithContext` to coordinate goroutines with error propagation — _replace a manual WaitGroup + error channel pattern with errgroup_
6. Identify goroutine leaks by reasoning about channel/context lifecycle — _audit a code snippet and name the leak_
7. Implement a graceful-shutdown pattern for a long-running service — _handle `os.Signal` and drain in-flight work before exiting_

---

## Prerequisites

### Required Modules

- [[go/9. Concurrency]] — you need to understand: goroutines, buffered/unbuffered channels, `select`, `sync.Mutex`, `sync.WaitGroup`, and `sync.Once`; this module builds every pattern on top of that foundation
- [[go/8. Error Handling]] — you need to understand: the `error` interface, `fmt.Errorf` wrapping, `errors.Is`/`errors.As`; `context` cancellation surfaces as errors and errgroup propagates them
- [[go/11. Testing and Benchmarking]] — you need to understand: `go test -race`; the race detector is a first-class tool in this module

### Required Concepts

- **Goroutine scheduling** — goroutines are multiplexed onto OS threads by the runtime; you don't control which goroutine runs when, which is why synchronization primitives are necessary
- **Channel directionality** — `chan<- T` (send-only) and `<-chan T` (receive-only) in function signatures communicate ownership; pipeline stages use this convention
- **Zero values and nil channels** — a nil channel blocks forever on send and receive; receiving from a closed channel returns the zero value immediately; these properties are used deliberately in several patterns

> [!TIP]
> If goroutines and channels feel uncertain, re-read the core sections of [[go/9. Concurrency]] before continuing.
> The patterns here compose those primitives in non-trivial ways — gaps in the foundation become real bugs.

---

## Why This Matters

Production Go programs are almost always concurrent: they serve HTTP requests, consume message queues, call downstream services, and process streams of data. The fundamental primitives (goroutines and channels) are easy to understand in isolation but surprisingly easy to misuse at scale: goroutines leak, deadlines are forgotten, errors from parallel workers are dropped, and shared counters race.

Concretely, mastery of this module enables you to:

- **Write correct, leak-free services** — every HTTP handler that fires goroutines, every background worker, every timeout needs the patterns from this module
- **Respond to cancellation and pressure** — `context.Context` propagation is the standard mechanism for deadline/cancellation in the entire Go ecosystem; every major library (database drivers, gRPC, HTTP) accepts a context
- **Scale safely** — worker pools and semaphores prevent a flood of requests from spawning unbounded goroutines that exhaust memory or downstream services

Without these patterns, services develop subtle, hard-to-reproduce bugs that only appear under load: goroutines stuck waiting on channels that nobody will ever close, requests that ignore their deadlines, and counter increments that race.

---

## Historical Context

Go's concurrency model traces to **Communicating Sequential Processes (CSP)**, a formal language published by Tony Hoare in **1978**. Rob Pike brought CSP ideas into Go's design, advocating channels as the primary mechanism for goroutine coordination.

Key moments for the patterns in this module:

- **2009** — Go open-sourced with goroutines and channels; the `sync` package provides `Mutex` and `WaitGroup`
- **2014** — Sameer Ajmani presents "Advanced Go Concurrency Patterns" at Google I/O, formalizing the pipeline and cancellation patterns
- **2014** — The `golang.org/x/net/context` package is published; the `Context` type standardizes cancellation and deadline propagation across library boundaries
- **2016** — Go 1.7 promotes `context` into the standard library as `context.Context`; `net/http` and `database/sql` adopt it immediately
- **2016** — `golang.org/x/sync/errgroup` is published, eliminating the WaitGroup + error channel boilerplate
- **2019** — Go 1.19 introduces typed atomics (`atomic.Int64`, `atomic.Uint32`, `atomic.Pointer[T]`), replacing the stringly-typed `atomic.LoadInt64(&n)` API

Understanding this history explains why `context` feels slightly bolted on compared to channels: it was standardized after Go shipped, once the ecosystem discovered that ad-hoc timeout propagation didn't compose. It is now the canonical approach throughout the standard library.

---

## Core Concepts

### context.Context — Cancellation, Deadlines, and Request-Scoped Values

`context.Context` is the standard way to carry a **cancellation signal**, a **deadline**, and **request-scoped values** through a call tree. Every function that does I/O, calls a goroutine, or might run for a meaningful duration should accept `ctx context.Context` as its first parameter.

The four constructor functions:

```go
// WithCancel: cancel manually by calling cancel()
ctx, cancel := context.WithCancel(parent)
defer cancel() // ALWAYS defer cancel — releases resources even if ctx is never cancelled

// WithTimeout: cancel after a duration
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()

// WithDeadline: cancel at an absolute time
deadline := time.Now().Add(5 * time.Second)
ctx, cancel := context.WithDeadline(parent, deadline)
defer cancel()

// WithValue: attach a request-scoped value (use sparingly — see pitfalls below)
type ctxKey string
ctx = context.WithValue(ctx, ctxKey("requestID"), "abc-123")
```

**Checking for cancellation** — two equivalent patterns:

```go
// Pattern 1: select with ctx.Done()
select {
case result := <-workCh:
    process(result)
case <-ctx.Done():
    return ctx.Err() // context.Canceled or context.DeadlineExceeded
}

// Pattern 2: non-blocking check before starting expensive work
if err := ctx.Err(); err != nil {
    return err // already cancelled, skip the work
}
```

**Propagating context through a call tree:**

```go
func handleRequest(ctx context.Context, userID int) error {
    // Pass the same ctx (or a derived child) to every downstream call.
    user, err := fetchUser(ctx, userID)          // passes ctx to DB query
    if err != nil {
        return err
    }
    return sendWelcome(ctx, user)                 // passes ctx to email service
}

func fetchUser(ctx context.Context, id int) (*User, error) {
    // The database driver respects ctx — it cancels the query if ctx is Done.
    row := db.QueryRowContext(ctx, "SELECT * FROM users WHERE id = $1", id)
    // ...
}
```

**Pitfalls of `context.Value`:**

`context.WithValue` is intentionally limited. It is designed for request-scoped data that crosses API boundaries — trace IDs, authenticated user identities, request IDs. It is **not** a function parameter replacement. Avoid:

```go
// WRONG — using context to pass function arguments
ctx = context.WithValue(ctx, "timeout", 30)   // this is a config parameter, not request scope

// RIGHT — for cross-cutting concerns that don't appear in every function signature
ctx = context.WithValue(ctx, ctxKey("traceID"), traceID)
```

Use typed unexported keys (like `type ctxKey string`) to avoid collisions with other packages using `context.WithValue`.

---

### Pipelines

A pipeline is a series of stages connected by channels. Each stage receives values from an upstream channel, transforms them, and sends results downstream. The key discipline: **every stage must exit when its context is cancelled** and must close its output channel when it is done producing.

```go
package main

import (
    "context"
    "fmt"
    "math"
)

// gen sends integers to a channel and closes it when done or ctx is cancelled.
func gen(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out) // always close — signals downstream that we are done
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return // upstream cancelled; stop producing
            }
        }
    }()
    return out
}

// sq squares each integer received from in.
func sq(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in { // range exits when in is closed
            select {
            case out <- n * n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Stage 1: generate numbers. Stage 2: square them.
    for n := range sq(ctx, gen(ctx, 2, 3, 4, 5)) {
        fmt.Println(n) // 4, 9, 16, 25
    }
    _ = math.Sqrt // imported for illustration
}
```

The invariant: the stage that closes the input channel (or whose context is cancelled) causes downstream stages to drain and return naturally. No goroutine is left waiting forever.

---

### Fan-Out / Fan-In

**Fan-out**: distribute work from one channel to multiple goroutines.
**Fan-in**: merge multiple channels into one.

```go
// fanOut starts n workers, each reading from the same input channel.
// NOTE: output order is nondeterministic — workers race for items.
func fanOut(ctx context.Context, in <-chan int, n int) []<-chan int {
    outs := make([]<-chan int, n)
    for i := 0; i < n; i++ {
        outs[i] = sq(ctx, in) // each worker is a pipeline stage
    }
    return outs
}

// merge fans-in multiple channels into one, closing the output when all inputs close.
func merge(ctx context.Context, cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(len(cs))
    for _, c := range cs {
        go output(c)
    }

    // Close out once all goroutines finish.
    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

> [!NOTE]
> Fan-out is appropriate when work items are independent and can be processed in any order.
> If order must be preserved, fan-out requires additional coordination (e.g., indexed results).

---

### Bounded Worker Pools

An unbounded fan-out spawns one goroutine per work item — dangerous at scale. A **bounded worker pool** limits concurrency to N workers, back-pressuring the sender when all workers are busy.

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Result holds the output of one unit of work.
type Result struct {
    Input int
    Value int
    Err   error
}

// workerPool processes items from jobs using exactly numWorkers goroutines.
func workerPool(ctx context.Context, jobs <-chan int, numWorkers int) <-chan Result {
    results := make(chan Result)
    var wg sync.WaitGroup

    worker := func() {
        defer wg.Done()
        for {
            select {
            case job, ok := <-jobs:
                if !ok {
                    return // jobs channel closed — worker exits cleanly
                }
                // Simulate work (replace with real computation or I/O).
                time.Sleep(10 * time.Millisecond)
                results <- Result{Input: job, Value: job * job}
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(numWorkers)
    for i := 0; i < numWorkers; i++ {
        go worker()
    }

    // Close results once all workers have exited.
    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    jobs := make(chan int, 20)
    for i := 1; i <= 20; i++ {
        jobs <- i
    }
    close(jobs)

    for r := range workerPool(ctx, jobs, 4) { // exactly 4 concurrent workers
        if r.Err != nil {
            fmt.Printf("error for %d: %v\n", r.Input, r.Err)
        } else {
            fmt.Printf("%d² = %d\n", r.Input, r.Value)
        }
    }
    // NOTE: output order is nondeterministic
}
```

---

### Semaphores via Buffered Channels

When you already have goroutines (e.g., one per request) and want to limit how many proceed past a critical section simultaneously, use a buffered channel as a semaphore.

```go
// sem limits concurrent access to at most maxConcurrent goroutines.
sem := make(chan struct{}, maxConcurrent)

func doWork(ctx context.Context, item Item) error {
    // Acquire: send into the buffered channel; blocks if all slots are taken.
    select {
    case sem <- struct{}{}:
    case <-ctx.Done():
        return ctx.Err()
    }
    defer func() { <-sem }() // Release: receive from the channel.

    return expensiveOperation(item)
}
```

This is simpler than a worker pool when goroutines are spawned externally (e.g., per HTTP request) and you just need to limit concurrent calls to one resource.

> [!NOTE]
> For more sophisticated semaphore needs — like weighted semaphores — see `golang.org/x/sync/semaphore`.

---

### Rate Limiting

**Simple rate limiting with `time.Ticker`:**

```go
// Process at most 10 items per second.
ticker := time.NewTicker(100 * time.Millisecond)
defer ticker.Stop()

for _, item := range items {
    <-ticker.C // wait for the next tick
    go process(item)
}
```

**Token-bucket rate limiting with `golang.org/x/time/rate`:**

```go
import "golang.org/x/time/rate"

// Allow 10 events per second with a burst of 3.
limiter := rate.NewLimiter(rate.Limit(10), 3)

func handleRequest(ctx context.Context, req Request) error {
    if err := limiter.Wait(ctx); err != nil { // blocks until a token is available, or ctx cancels
        return err
    }
    return processRequest(req)
}
```

`rate.Limiter` uses the token-bucket algorithm and is safe for concurrent use. It also respects context cancellation. Prefer it over a `Ticker` for any non-trivial rate-limiting requirement.

---

### sync/atomic and Typed Atomics

Atomic operations are lock-free reads and writes that are safe for concurrent use without a mutex. They are appropriate for **simple counters and flags** where the critical section is a single read-modify-write operation. For anything more complex, use a mutex.

**Go 1.19+ typed atomics** (preferred):

```go
import "sync/atomic"

var counter atomic.Int64 // zero value is ready to use — no initialization needed

// Safe for concurrent use from multiple goroutines.
counter.Add(1)
counter.Add(-1)
n := counter.Load()
counter.Store(100)

// Compare-and-swap: atomically set to newVal only if current value == oldVal.
// Returns true if the swap happened.
swapped := counter.CompareAndSwap(oldVal, newVal)
```

**`atomic.Pointer[T]`** for lock-free pointer swaps:

```go
var config atomic.Pointer[Config] // holds a *Config

// Write a new config atomically — readers see the full new struct immediately.
config.Store(&Config{Timeout: 5 * time.Second})

// Read the current config atomically.
cfg := config.Load() // returns *Config
```

> [!WARNING]
> Atomics do not compose. If you need to atomically update two variables together, you need a mutex.
> Also: the Go memory model guarantees atomics provide sequential consistency, but the patterns that
> rely on this are subtle. See [[go/17. Runtime Internals and the Memory Model]] for happens-before guarantees.

---

### sync.Pool — Object Reuse

`sync.Pool` is a concurrent-safe cache of temporary objects that can be reused across goroutines to reduce allocations and GC pressure. The canonical use case is reusing `[]byte` buffers or `bytes.Buffer` instances in hot paths.

```go
var bufPool = sync.Pool{
    New: func() any {
        // Called when the pool is empty — allocate a fresh buffer.
        return make([]byte, 0, 64*1024) // 64 KiB
    },
}

func processRequest(data []byte) {
    // Get a buffer from the pool (or allocate a fresh one via New).
    buf := bufPool.Get().([]byte)
    buf = buf[:0] // reset length, retain capacity

    defer bufPool.Put(buf) // return to pool when done

    // Use buf for this request's work...
    buf = append(buf, data...)
    // ...
}
```

> [!WARNING]
> The GC may clear `sync.Pool` at any time between GC cycles — do not use it for objects that must persist.
> Never store state in a pooled object that you expect to survive across `Get`/`Put` round trips.

---

### errgroup — Grouped Goroutines with Error Propagation

`golang.org/x/sync/errgroup` replaces the common but error-prone pattern of `sync.WaitGroup` + an error channel. It propagates the first non-nil error and cancels the shared context automatically.

```go
import "golang.org/x/sync/errgroup"

func fetchAll(ctx context.Context, urls []string) ([][]byte, error) {
    g, ctx := errgroup.WithContext(ctx) // g.Go goroutines share this derived ctx

    results := make([][]byte, len(urls))
    for i, url := range urls {
        i, url := i, url // capture loop variables — required in Go < 1.22
        g.Go(func() error {
            resp, err := http.Get(url) // in practice: use http.NewRequestWithContext(ctx, ...)
            if err != nil {
                return err // first error cancels the ctx; other goroutines should check ctx.Done()
            }
            defer resp.Body.Close()
            results[i], err = io.ReadAll(resp.Body)
            return err
        })
    }

    if err := g.Wait(); err != nil { // blocks until all goroutines finish; returns first error
        return nil, err
    }
    return results, nil
}
```

`errgroup.WithContext` returns both the group and a derived context. When any `g.Go` goroutine returns a non-nil error, the context is cancelled — other goroutines should respect `ctx.Done()` to exit promptly.

---

### Detecting and Avoiding Goroutine Leaks

A goroutine **leaks** when it is blocked forever with no way to exit. Common causes:

| Cause | Example | Fix |
|-------|---------|-----|
| Waiting on a channel nobody will close | `result := <-ch` with no guarantee `ch` is ever sent to | Use `select` with `ctx.Done()` |
| Sending to a full buffered channel with no reader | `ch <- val` after reader exits | Use `ctx.Done()` or ensure reader outlives sender |
| Blocking on mutex that is never unlocked | Deadlock | Audit lock ordering; use `-race` |

**Principle**: every goroutine must have a clear termination condition. If you start a goroutine, you must own its lifecycle — either it exits when its work is done, or it exits when a context or done channel signals it.

```go
// Leaky — if nobody reads from resultCh, the goroutine blocks forever.
func leaky(input int) <-chan int {
    resultCh := make(chan int)
    go func() {
        resultCh <- expensiveCompute(input) // BLOCKS if caller ignores the channel
    }()
    return resultCh
}

// Fixed — use a buffered channel of size 1 so the goroutine can always send and exit.
func fixed(input int) <-chan int {
    resultCh := make(chan int, 1) // buffer of 1 — goroutine sends and exits immediately
    go func() {
        resultCh <- expensiveCompute(input)
    }()
    return resultCh
}
```

Use the `goleak` package (`go.uber.org/goleak`) in tests to assert that no goroutines are leaked after a test function returns.

---

### Graceful Shutdown

A server or background worker should drain in-flight work when it receives a shutdown signal, rather than killing goroutines mid-operation.

```go
package main

import (
    "context"
    "fmt"
    "os"
    "os/signal"
    "sync"
    "syscall"
    "time"
)

func main() {
    ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
    defer stop()

    var wg sync.WaitGroup

    // Start N workers that respect the context.
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    fmt.Printf("worker %d: shutting down\n", id)
                    return
                case <-time.After(200 * time.Millisecond):
                    fmt.Printf("worker %d: processing\n", id)
                }
            }
        }(i)
    }

    // Block until SIGINT/SIGTERM.
    <-ctx.Done()
    fmt.Println("shutdown signal received; waiting for workers...")

    // Give workers a deadline to finish in-flight work.
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    done := make(chan struct{})
    go func() {
        wg.Wait()
        close(done)
    }()

    select {
    case <-done:
        fmt.Println("clean shutdown")
    case <-shutdownCtx.Done():
        fmt.Println("shutdown timeout — some work may be incomplete")
    }
}
```

`signal.NotifyContext` (Go 1.16+) is the idiomatic way to convert an OS signal into a context cancellation.

---

### The Race Detector in CI

Run `go test -race ./...` in every CI pipeline. The race detector instruments memory accesses and reports data races at runtime with the exact goroutines and stack traces involved.

```bash
# Locally
go test -race ./...
go run -race main.go

# In a GitHub Actions workflow (typical)
- name: Test with race detector
  run: go test -race -count=1 ./...
```

The race detector has a ~2–5× overhead in time and memory — acceptable for CI, but do not ship race-instrumented binaries to production. A detected race is always a bug; zero tolerance is the right policy.

---

### How the Concepts Fit Together

```
OS Signal ──► signal.NotifyContext
                     │
                     ▼
              context.Context  ◄─── WithTimeout / WithDeadline
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Pipeline   Worker    errgroup
     (stages +    Pool       (g.Go +
      fan-out)  (semaphore)   g.Wait)
          │          │          │
          └──────────┴──────────┘
                     │
                     ▼
           Results / Errors
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     atomic.Int64           sync.Pool
   (lock-free counters)  (object reuse)
```

`context.Context` is the backbone: it flows from the top of the call tree to every goroutine. The concurrency patterns (pipelines, pools, errgroup) are all built on channels and goroutines from [[go/9. Concurrency]], with context wired through them. Atomics and `sync.Pool` are complementary optimizations for hot paths.

---

## Common Mistakes

> [!WARNING]
> **Mistake 1: Forgetting `defer cancel()` after `With*` functions**
>
> Every `context.With*` call allocates resources (a goroutine and a timer, in the case of `WithTimeout`). Failing to call `cancel()` leaks these resources until the parent context is cancelled.
>
> **Wrong:**
> ```go
> ctx, _ := context.WithTimeout(parentCtx, 5*time.Second) // cancel is discarded!
> doWork(ctx)
> ```
>
> **Right:**
> ```go
> ctx, cancel := context.WithTimeout(parentCtx, 5*time.Second)
> defer cancel() // always, even if ctx expires before cancel() is called
> doWork(ctx)
> ```
>
> **Why this matters:** In a server that creates thousands of request contexts per second, missing `cancel()` will cause steady memory growth that is difficult to diagnose.

> [!WARNING]
> **Mistake 2: Storing context in a struct field**
>
> Contexts are request-scoped and should flow through function parameters, not be stored in structs. A struct-stored context cannot be cancelled per-call, defeats the call-tree propagation model, and is flagged by `go vet`.
>
> **Wrong:**
> ```go
> type Worker struct {
>     ctx context.Context // DON'T — ctx is request-scoped, not worker-scoped
> }
> ```
>
> **Right:**
> ```go
> func (w *Worker) Do(ctx context.Context, item Item) error {
>     // ctx flows through the method call — correct
> }
> ```

> [!WARNING]
> **Mistake 3: Using `context.Value` as a general key-value store**
>
> `context.Value` is for cross-cutting request metadata (trace IDs, authenticated user IDs). Using it to pass function arguments or configuration makes code untestable and breaks type safety.
>
> **Wrong:**
> ```go
> ctx = context.WithValue(ctx, "db", myDB)    // passing infrastructure through context
> ctx = context.WithValue(ctx, "limit", 100)  // passing function args through context
> ```
>
> **Right:** Pass `db` and `limit` as explicit function parameters.

**Other pitfalls:**

- **Not handling `ctx.Done()` in every goroutine** — a goroutine blocked on a channel with no `ctx.Done()` case will leak when the context is cancelled
- **Racing on `errgroup` results slice** — when `g.Go` closures write to a shared slice, each closure must write to a unique index; never append from multiple goroutines
- **Calling `sync.Pool.Put` with a modified object** — if you grew the `[]byte` slice and `Put` it back, the next caller gets the grown capacity, which may be desirable — but if you corrupted it (e.g., with a nil pointer), the pool is poisoned

---

## Mental Models

### Mental Model 1: Context as a Request's Nervous System

Think of `context.Context` as the nervous system for a single request. The top-level context is the brain — it holds the deadline and the cancel signal. Every function and goroutine working on that request is a nerve ending that must respond when the brain signals "stop". If any nerve ending ignores the signal (doesn't check `ctx.Done()`), that part of the request continues consuming resources after the client has given up.

This model is most useful when deciding where to pass context: pass it everywhere that touches I/O or spawns goroutines. The model breaks down for background work that outlives any single request — use a long-lived context (derived from `context.Background()`) for that.

### Mental Model 2: Channels as Conveyor Belts Between Stages

A pipeline is a factory floor with conveyor belts. Each stage is a workstation: it picks items off the incoming belt, transforms them, and places results on the outgoing belt. The channel is the belt. Closing a channel is like turning off the belt — every downstream station drains the remaining items and stops.

This model makes it intuitive why every stage must `close(out)` when done: a downstream stage using `for n := range in` will block forever if `in` is never closed. The belt never stops.

### Mental Model 3: Worker Pool as a Thread Pool with Back-Pressure

A worker pool with N workers is like a bank with N tellers. The jobs channel is the queue. If all N tellers are busy, new customers must wait in line (the `jobs <- item` send blocks). When a teller finishes, it picks the next customer. You never have more than N tellers serving simultaneously.

The key insight: the buffered `jobs` channel controls the maximum queue depth; the number of workers controls concurrency. Tuning both independently gives you the right trade-off between memory usage (queue depth × item size) and throughput.

> [!NOTE]
> No single model covers everything. Use Model 1 (nervous system) when reasoning about cancellation propagation.
> Use Model 2 (conveyor belt) when designing pipelines. Use Model 3 (bank tellers) when sizing worker pools.

---

## Practical Examples

### Example 1: Context-Aware HTTP Fan-Out _(Basic)_

**Scenario:** Fetch three URLs concurrently, cancelling remaining fetches if any one fails or the overall deadline expires.

**Goal:** Demonstrate `errgroup.WithContext` with a real deadline.

```go
package main

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "time"

    "golang.org/x/sync/errgroup"
)

func fetchAll(urls []string) ([]string, error) {
    // 3-second deadline for all fetches combined.
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()

    g, ctx := errgroup.WithContext(ctx)
    bodies := make([]string, len(urls))

    for i, url := range urls {
        i, url := i, url // capture — required before Go 1.22
        g.Go(func() error {
            req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
            if err != nil {
                return err
            }
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                return err
            }
            defer resp.Body.Close()
            data, err := io.ReadAll(resp.Body)
            if err != nil {
                return err
            }
            bodies[i] = fmt.Sprintf("%s: %d bytes", url, len(data))
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return bodies, nil
}

func main() {
    results, err := fetchAll([]string{
        "https://go.dev",
        "https://pkg.go.dev",
    })
    if err != nil {
        fmt.Println("error:", err)
        return
    }
    for _, r := range results {
        fmt.Println(r)
    }
}
```

**What to notice:** `errgroup.WithContext` derives a child context; if either `g.Go` goroutine returns a non-nil error, the context is cancelled and the other goroutine's `http.DefaultClient.Do(req)` will return promptly.

---

### Example 2: Atomic Request Counter _(Intermediate)_

**Scenario:** Count in-flight requests in an HTTP server with zero lock overhead.

**Goal:** Show `atomic.Int64` in a realistic pattern.

```go
package main

import (
    "fmt"
    "net/http"
    "sync/atomic"
)

var inFlight atomic.Int64

func handler(w http.ResponseWriter, r *http.Request) {
    inFlight.Add(1)
    defer inFlight.Add(-1)

    // ... handle request ...
    fmt.Fprintf(w, "in-flight: %d\n", inFlight.Load())
}

func metricsHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "current_in_flight %d\n", inFlight.Load())
}
```

**What to notice:** No mutex needed for a single counter. `Add` and `Load` are individually atomic; if you need to read-and-conditionally-write, use `CompareAndSwap`.

---

### Example 3: Semaphore-Limited Crawler _(Applied)_

**Scenario:** Crawl a list of URLs with at most 5 concurrent connections.

```go
package main

import (
    "context"
    "fmt"
    "net/http"
    "sync"
    "time"
)

func crawl(ctx context.Context, urls []string, maxConcurrent int) {
    sem := make(chan struct{}, maxConcurrent) // semaphore: at most maxConcurrent goroutines in HTTP
    var wg sync.WaitGroup

    for _, url := range urls {
        url := url
        wg.Add(1)
        go func() {
            defer wg.Done()

            // Acquire semaphore slot (or exit if context cancelled).
            select {
            case sem <- struct{}{}:
            case <-ctx.Done():
                fmt.Printf("skip %s: context done\n", url)
                return
            }
            defer func() { <-sem }() // release slot

            req, _ := http.NewRequestWithContext(ctx, http.MethodHead, url, nil)
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                fmt.Printf("error %s: %v\n", url, err)
                return
            }
            resp.Body.Close()
            fmt.Printf("ok %s: %d\n", url, resp.StatusCode)
        }()
    }
    wg.Wait()
    // NOTE: output order is nondeterministic
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    urls := []string{
        "https://go.dev", "https://pkg.go.dev", "https://golang.org",
        "https://github.com", "https://blog.golang.org",
    }
    crawl(ctx, urls, 2) // max 2 concurrent HTTP requests
}
```

**What to notice:** The semaphore limits concurrent HTTP connections regardless of how many goroutines are active. Each goroutine still runs concurrently — they just block at the `sem <- struct{}{}` acquire when all slots are full.

---

### Example 4: Goroutine Leak via Abandoned Channel _(Edge Case)_

**Scenario:** What happens when a goroutine sends to a channel that the caller never reads?

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

// leaky starts a goroutine that blocks forever if nobody reads from the returned channel.
func leaky() <-chan int {
    ch := make(chan int) // unbuffered — send blocks until someone receives
    go func() {
        result := 42
        ch <- result // BLOCKS FOREVER if caller ignores the channel
        fmt.Println("goroutine exited") // never prints if caller discards ch
    }()
    return ch
}

func main() {
    fmt.Printf("goroutines before: %d\n", runtime.NumGoroutine())

    for i := 0; i < 10; i++ {
        _ = leaky() // discard the channel — 10 goroutines are now stuck
    }

    time.Sleep(100 * time.Millisecond) // let goroutines reach the send
    fmt.Printf("goroutines after:  %d\n", runtime.NumGoroutine()) // likely 11 (main + 10 leaked)
}
```

**Why this is important:** `runtime.NumGoroutine()` in tests (or `goleak.VerifyNone(t)`) surfaces leaks that would otherwise be invisible until the process runs out of memory. The fix is always: give the goroutine a way to exit — buffer of 1, a context, or a done channel.

---

## Related Concepts

Within this topic:

- [[go/9. Concurrency]] — foundation module; all patterns here are built on goroutines, channels, `select`, `sync.Mutex`, and `sync.WaitGroup`
- [[go/11. Testing and Benchmarking]] — `go test -race` is a first-class tool for catching data races introduced by the patterns in this module
- [[go/17. Runtime Internals and the Memory Model]] — the happens-before guarantees that make atomics and channels safe; essential reading before writing lock-free code in production

In other topics:

- [[concurrency]] — the general concept of concurrency, comparing Go's CSP model against threads, async/await, and actors; useful for understanding why `context.Context` solves a real problem

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Context-Aware Sleeper** _(Easy)_
>
> Write a function `sleep(ctx context.Context, d time.Duration) error` that waits for `d` to elapse or for `ctx` to be cancelled, whichever comes first. Return `ctx.Err()` on cancellation and `nil` on clean completion. This is the minimal context-aware operation and the foundation of every pattern in this module.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-context-aware-sleeper--easy--1-pt)

The exercises range from single-function warm-ups to a full bounded pipeline. Complete at least the Easy and Medium exercises before taking the test.

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
Concurrent URL Health Checker — given a text file of URLs (one per line), check each URL's HTTP status concurrently using a bounded worker pool of configurable size, respect a per-request timeout via `context.WithTimeout`, aggregate results (status code, latency, error), and print a summary. Add `-race` to your CI Makefile step.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Go Concurrency Patterns: Pipelines and cancellation — Go Blog](https://go.dev/blog/pipelines)** — Sameer Ajmani's authoritative 2014 article introducing the pipeline pattern, fan-out/fan-in, and cancellation via done channels; this is the original source for the pipeline conventions used in this module
2. **[Go Concurrency Patterns: Context — Go Blog](https://go.dev/blog/context)** — Sameer Ajmani's companion article explaining the `context` package design, the first-parameter convention, and when (not) to use `context.Value`
3. **[pkg.go.dev/context](https://pkg.go.dev/context)** — the standard library package documentation with usage rules stated explicitly; read the package-level doc comment in full
4. **[pkg.go.dev/sync/atomic](https://pkg.go.dev/sync/atomic)** — documentation for typed atomics (`atomic.Int64`, `atomic.Pointer`) introduced in Go 1.19; includes usage notes on memory ordering
5. **[pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)** — errgroup package documentation and examples
6. **[Concurrency in Go by Katherine Cox-Buday](https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/)** — O'Reilly book, the most comprehensive treatment of Go concurrency patterns including pipelines, fan-out/fan-in, context, worker pools, and `sync.Pool`; chapter 4 ("Concurrency Patterns in Go") directly corresponds to this module

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 12

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
