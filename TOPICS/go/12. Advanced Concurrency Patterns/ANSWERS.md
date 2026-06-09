# Answer Key — Module 12: Advanced Concurrency Patterns

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with notes closed.
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
- Right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — defer cancel() semantics [1 pt]

**Full credit answer:**
`cancel()` releases the resources that `context.WithTimeout` allocated — specifically, a goroutine and a timer that monitors the deadline. Even if the timeout fires and the context expires naturally, the internal timer goroutine and resources are not released until `cancel()` is called. Failing to call `cancel()` in a server that creates thousands of request contexts per second causes steady memory growth (a slow leak). Calling `cancel()` after the timeout has already fired is safe and idempotent — it is always correct to call it.

**Key points required:**
- `cancel()` releases resources (timer goroutine, internal data structures)
- Safe to call even after timeout expires (idempotent)
- Omitting it causes resource leaks in long-running servers

**Common wrong answers:**
- "cancel() cancels the context" — partially correct, but misses the resource-release purpose
- "cancel() is only needed if you want to cancel early" — misses that it releases resources regardless

---

### 1.2 — Four context constructors [1 pt]

**Full credit answer:**

| Constructor | Returns cancel? | Cancellation trigger |
|-------------|----------------|----------------------|
| `context.WithCancel(parent)` | Yes, `cancel func()` | Explicit call to `cancel()`, or parent cancelled |
| `context.WithTimeout(parent, d)` | Yes, `cancel func()` | After duration `d` elapses, or explicit `cancel()`, or parent cancelled |
| `context.WithDeadline(parent, t)` | Yes, `cancel func()` | When clock reaches absolute time `t`, or explicit `cancel()`, or parent cancelled |
| `context.WithValue(parent, k, v)` | No | N/A — only attaches a value; cancellation is inherited from parent |

**Key points required:**
- All four names
- `WithValue` does not return a cancel function (it doesn't add cancellation)
- Parent cancellation propagates to all derived children

---

### 1.3 — defer close(out) and range-over-closed-channel [1 pt]

**Full credit answer:**
`defer close(out)` signals to downstream stages that no more values will be sent. A downstream stage using `for n := range in` will exit the loop when `in` is closed — `range` over a channel iterates until the channel is both empty and closed. If `close(in)` is never called, the `for range` loop blocks forever waiting for the next value — the downstream goroutine is leaked. `defer close(out)` ensures that closing happens even if the upstream goroutine returns early due to an error or context cancellation.

**Key points required:**
- `close` signals "no more values coming"
- `for range` on a channel blocks until the channel is closed; never-closed = goroutine leak
- `defer` ensures closing happens on all exit paths

---

### 1.4 — Add vs CompareAndSwap [1 pt]

**Full credit answer:**
`Add(delta)` atomically adds `delta` to the current value and returns the new value — it always succeeds. `CompareAndSwap(old, new)` atomically sets the value to `new` only if the current value equals `old`; it returns `true` if the swap happened, `false` otherwise.

Use `CompareAndSwap` when you need to conditionally update: for example, implementing a lock-free transition from one state to another where the transition should only happen once. Example:

```go
var state atomic.Int64  // 0 = idle, 1 = running

// Start only if idle — prevent double-start.
if state.CompareAndSwap(0, 1) {
    go doWork()
}
```

`Add` is appropriate for simple monotonic counters (request counts, in-flight counts). `CompareAndSwap` is appropriate for state machines or when you need to read-then-conditionally-write atomically.

**Key points required:**
- `Add` always succeeds; `CompareAndSwap` is conditional
- CAS returns bool indicating success
- CAS is appropriate for conditional state transitions

---

### 1.5 — Goroutine leak detection [1 pt]

**Full credit answer:**
`goleak.VerifyNone(t)` (from `go.uber.org/goleak`) asserts that no unexpected goroutines are running at the time of the call. `runtime.NumGoroutine()` returns the current count of goroutines for manual comparison.

Check it **after** the test's work is complete — typically via `defer goleak.VerifyNone(t)` at the start of the test (so it runs after all the test's code). If any goroutines that were started during the test are still running when `VerifyNone` is called, the test fails with a report showing which goroutines are still alive (with stack traces).

**Key points required:**
- Checks for goroutines still running after the test
- Should be called (via defer) at the end of the test
- Reports specific leaked goroutines with stacks

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Context as first parameter, not global/struct field [2 pts]

**Full credit answer:**
A context is **request-scoped** — it carries the deadline and cancellation signal for one specific operation. Passing it as the first parameter threads it through every function in the call tree, allowing each layer to either respect it or derive a shorter-lived child from it.

If you store a context in a struct field and reuse that struct across multiple requests, several things go wrong:
1. **Stale cancellation**: the stored context was created for request 1 and may already be cancelled when request 2 arrives; request 2's work would be cancelled immediately
2. **Incorrect deadline propagation**: request 2 may inherit a deadline that was set for request 1's timeout, which has nothing to do with request 2
3. **Thread safety**: context storage in a struct makes it non-obvious when the context changes, and updating it from multiple goroutines requires synchronization

The `go vet` tool flags `context.Context` stored in a struct: "do not store Contexts inside a struct type; instead, pass a Context explicitly to each function that needs it."

**Rubric:**
- 2 pts: Explains request-scoped semantics AND names at least two concrete failure modes of struct storage
- 1 pt: Correct general idea but only one failure mode named, or explanation is vague
- 0 pts: Claims struct storage is fine

---

### 2.2 — Worker pool vs unbounded fan-out [2 pts]

**Full credit answer:**
**Unbounded fan-out** launches one goroutine per work item. For N items, N goroutines run simultaneously. This is appropriate when N is small and bounded (e.g., fetch 5 specific URLs at startup). Failure modes at scale: if N = 100,000 incoming requests, 100,000 goroutines may all call a downstream service simultaneously, overwhelming it (thundering herd), or consuming gigabytes of stack memory.

**Bounded worker pool** maintains exactly W workers regardless of N items. Workers pick items off a jobs channel as they finish previous items. This is appropriate when N is unbounded or large (e.g., processing a stream, handling incoming HTTP requests). The pool provides **back-pressure**: when all W workers are busy, new items block in the jobs channel rather than spawning more goroutines.

Key comparison:

| | Fan-out | Worker Pool |
|---|--------|------------|
| Goroutines spawned | N (one per item) | W (fixed) |
| Memory scaling | O(N) | O(W) |
| Back-pressure | None | Yes (jobs channel) |
| When appropriate | Small, bounded N | Large or unbounded N |

**Rubric:**
- 2 pts: Correctly defines both, identifies back-pressure as the key property of the pool, names at least one concrete failure mode of unbounded fan-out
- 1 pt: Correct definition of one of the two, or correct definitions without explaining back-pressure
- 0 pts: Confuses the two

---

### 2.3 — Atomics vs mutex, and composability limitation [2 pts]

**Full credit answer:**
A mutex-protected read-modify-write requires three separate operations: lock, read+modify, unlock. Between lock and unlock, the scheduler may run other goroutines — but they will block on the same mutex. Atomic operations are a single hardware instruction (e.g., `LOCK XADD` on x86) that reads and writes in one indivisible step, with no need for a lock.

The limitation: **atomics do not compose**. You cannot atomically update two separate variables in a single operation, even if both are `atomic.Int64`. Between `counter1.Add(1)` and `counter2.Add(1)`, another goroutine may observe `counter1` incremented but `counter2` not yet incremented — an inconsistent snapshot. For operations that must be atomic across multiple variables, you need a mutex covering all of them.

Example of the problem:
```go
var requests atomic.Int64
var errors   atomic.Int64

// UNSAFE: another goroutine could read requests=5, errors=0 between these two lines
requests.Add(1)
errors.Add(1)
// Correct: use a mutex to update both together
```

**Rubric:**
- 2 pts: Explains atomic as a single hardware instruction (no locking overhead) AND clearly explains the non-composability with a concrete example or explanation
- 1 pt: Correct on one of the two parts; or correct explanation but without the composability limitation
- 0 pts: Claims atomics are safe for multi-variable updates

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — fanIn function [3 pts]

**Full credit answer:**
```go
import (
    "context"
    "sync"
)

// fanIn merges multiple input channels into one output channel.
// The output channel is closed when all input channels are drained or ctx is cancelled.
func fanIn(ctx context.Context, channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    // Launch one forwarder goroutine per input channel.
    forward := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(len(channels))
    for _, c := range channels {
        go forward(c)
    }

    // Close out once all forwarders have exited.
    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}
```

**Rubric:**
- 3 pts: One goroutine per input channel; uses WaitGroup; closes output after all goroutines exit; handles ctx cancellation with select; compiles
- 2 pts: Correct structure but missing ctx.Done() in the select (not context-aware), or WaitGroup use is slightly off
- 1 pt: Correct general approach but has a data race (e.g., closing out too early) or missing WaitGroup
- 0 pts: Fundamentally wrong (e.g., using reflect.Select, or sequential drain)

**Common wrong answers:**
- Closing `out` inside the `forward` goroutine — would close it multiple times (panic)
- Not using a WaitGroup — no way to know when all forwarders are done before closing

---

### 3.2 — withRetry with exponential backoff [3 pts]

**Full credit answer:**
```go
import (
    "context"
    "time"
)

// withRetry calls fn up to maxAttempts times with exponential backoff between attempts.
// Returns nil on success, or the last error if all attempts fail.
// Stops early if ctx is cancelled.
func withRetry(ctx context.Context, maxAttempts int, fn func(ctx context.Context) error) error {
    var err error
    backoff := 100 * time.Millisecond

    for attempt := 0; attempt < maxAttempts; attempt++ {
        if err = fn(ctx); err == nil {
            return nil // success
        }

        if attempt == maxAttempts-1 {
            break // last attempt — don't sleep
        }

        // Wait for backoff duration or context cancellation.
        select {
        case <-time.After(backoff):
        case <-ctx.Done():
            return ctx.Err() // cancelled during backoff
        }

        backoff *= 2 // exponential: 100ms, 200ms, 400ms...
    }

    return err
}
```

**Rubric:**
- 3 pts: Correct retry loop; exponential backoff using `backoff *= 2`; context-aware sleep with select; returns `ctx.Err()` on cancellation; returns last error on exhaustion; compiles
- 2 pts: Correct retry and backoff but missing ctx cancellation during sleep, or uses `time.Sleep` instead of select
- 1 pt: Correct retry logic but fixed backoff (not exponential), or missing error return handling
- 0 pts: Does not retry, or does not respect the attempt limit

**Acceptable variations:**
- Starting backoff at a different value (50ms, 200ms) — fine
- Using `jitter` on the backoff — fine, and is actually better practice
- Checking `ctx.Err()` before each attempt — fine (redundant but not wrong)

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Goroutine leak in queryAsync + db bug [3 pts] (1 pt each part)

**(a) The goroutine leak:**
When the HTTP handler's `select` fires on `r.Context().Done()` (timeout or client disconnect), the handler returns without reading from `ch`. The goroutine inside `queryAsync` is blocked on `result <- name` (or `result <- "error: ..."`) because nobody is receiving from the unbuffered channel. Since the handler has returned and there is no other receiver, the goroutine is leaked — it will block on that send forever (or until the process exits). Under high traffic, each timed-out request leaks one goroutine, causing steady goroutine count growth.

**(b) The db.QueryRow bug:**
`db.QueryRow(...).Scan()` is called with zero arguments — `Scan` requires destination pointers for each column being scanned. For `SELECT name FROM users WHERE id = $1`, it should be `db.QueryRow(...).Scan(&name)` where `name` is a declared `string` variable. The current code will return an error (wrong number of arguments to Scan) for every call.

Additionally, `db.QueryRow` does not accept a `context.Context` — it should be `db.QueryRowContext(ctx, ...)` so the database query is cancelled when the HTTP request times out.

**(c) Fixed version:**
```go
func queryAsync(ctx context.Context, userID int) <-chan string {
    result := make(chan string, 1) // buffer of 1 — goroutine can always send and exit
    go func() {
        var name string
        err := db.QueryRowContext(ctx, "SELECT name FROM users WHERE id = $1", userID).Scan(&name)
        if err != nil {
            result <- "error: " + err.Error()
        } else {
            result <- name
        }
        // Goroutine always exits after the send, even if caller has timed out,
        // because the buffer of 1 means the send never blocks.
    }()
    return result
}
```

With `make(chan string, 1)`, the goroutine can always complete its send and exit — even if the handler has already returned after a timeout. The `db.QueryRowContext(ctx, ...)` also means the database query itself is cancelled if the handler's context expires.

**Rubric:**
- 1 pt for (a): Correctly identifies that the goroutine blocks on the unbuffered channel send after the handler returns
- 1 pt for (b): Identifies at least one of: wrong Scan call (no destination pointer) OR missing context propagation to db query
- 1 pt for (c): Fixes the leak with a buffer-of-1 channel AND passes ctx to the db call AND fixes the Scan call

---

## Section 5: Discussion — Answer Key

### 5.1 — Race detector: CI yes, production no [2 pts]

**Example strong answer:**
The race detector instruments every memory access in the program at the assembly level, inserting hooks that record which goroutine last wrote to each memory location. When two goroutines access the same location concurrently and at least one is a write, it reports the race with both goroutines' stack traces. This catches bugs that are invisible to normal testing because they depend on precise goroutine scheduling timing — a race that "never fires" locally might trigger under load in production.

However, the instrumentation adds 2–5× CPU overhead and 5–10× memory overhead. In a production service serving real traffic, that overhead would meaningfully reduce capacity and latency, and could exhaust memory. Additionally, the race detector's reports appear at runtime on stderr, which is not part of production monitoring pipelines.

**Concrete scenario 1 (catching a bug):** An HTTP handler that modifies a shared map under a read lock but writes under a write lock — the race is benign 99.9% of the time (readers rarely clash with writers in tests), but `go test -race` detects it immediately because the instrumentation catches the concurrent access regardless of timing.

**Concrete scenario 2 (production problem):** A service handling 50,000 requests/second with `-race` would see response times 3–5× higher, potentially breaching SLAs. Memory usage 5–10× higher might cause OOM kills. Neither is acceptable.

**Elements that earn full credit:**
- Explains what the race detector instruments (memory access hooks)
- Names the overhead (2–5× CPU, 5–10× memory is accurate)
- Names at least one concrete CI benefit (catches timing-dependent races)
- Names at least one concrete production problem (throughput/latency/memory)

**Rubric:**
- 2 pts: Correctly describes what race detector does, names real overhead values, gives a scenario for each half
- 1 pt: Correct on one half (e.g., good on CI benefit but vague on production problem, or vice versa)
- 0 pts: Claims race detector has negligible overhead, or claims it should be run in production

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — RateLimitedPool[T] [+5 pts]

**Full credit answer:**
```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"

    "golang.org/x/time/rate"
)

// RateLimitedPool processes items from a queue with a bounded number of workers
// and a shared rate limiter applied before each item is processed.
type RateLimitedPool[T any] struct {
    jobs    chan T
    limiter *rate.Limiter
    process func(ctx context.Context, item T)
    wg      sync.WaitGroup
}

// New creates a pool with numWorkers workers, a rate limiter, and a processing function.
func New[T any](numWorkers int, limiter *rate.Limiter, process func(ctx context.Context, item T)) *RateLimitedPool[T] {
    p := &RateLimitedPool[T]{
        jobs:    make(chan T, numWorkers*2), // buffer to reduce blocking
        limiter: limiter,
        process: process,
    }
    for i := 0; i < numWorkers; i++ {
        p.wg.Add(1)
        go p.worker(context.Background()) // workers run until jobs is closed
    }
    return p
}

func (p *RateLimitedPool[T]) worker(ctx context.Context) {
    defer p.wg.Done()
    for item := range p.jobs {
        // Respect the rate limit before processing each item.
        if err := p.limiter.Wait(ctx); err != nil {
            return // context cancelled
        }
        p.process(ctx, item)
    }
}

// Submit adds an item to the work queue. Blocks if the queue is full.
// Returns ctx.Err() if ctx is cancelled before the item can be queued.
func (p *RateLimitedPool[T]) Submit(ctx context.Context, item T) error {
    select {
    case p.jobs <- item:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

// Close stops accepting new work and waits for all workers to finish.
func (p *RateLimitedPool[T]) Close() {
    close(p.jobs) // signal workers to exit after draining
    p.wg.Wait()
}

func main() {
    // Allow 5 items per second with a burst of 2.
    limiter := rate.NewLimiter(rate.Limit(5), 2)

    pool := New[int](3, limiter, func(ctx context.Context, item int) {
        fmt.Printf("processed %d at %s\n", item, time.Now().Format("15:04:05.000"))
    })

    ctx := context.Background()
    for i := 1; i <= 8; i++ {
        if err := pool.Submit(ctx, i); err != nil {
            fmt.Println("submit failed:", err)
        }
    }
    pool.Close()
    fmt.Println("all done")
    // NOTE: output timestamps will show rate limiting in effect
}
```

**Rubric:**
- 5 pts: Correct generic type; workers apply `limiter.Wait(ctx)` before each item; `Submit` is context-aware with select; `Close` closes jobs and calls `wg.Wait()`; compiles with Go 1.18+; usage example shown
- 3 pts: Correct structure but rate limiter not applied per-item (e.g., applied only at submit time), or Close doesn't wait for workers
- 1 pt: Correct idea but not generic, or has a data race (e.g., shared state without synchronization)
- 0 pts: Does not compile or fundamentally wrong design

---

## Common Wrong Answers Across the Test

1. **Calling `cancel()` only on early exit** — students write `if err != nil { cancel(); return err }` but omit `defer cancel()`. This leaks resources on the happy path. Always `defer cancel()` immediately after `With*`.

2. **Forgetting `defer close(out)` in pipeline stages** — the stage goroutine sends on `out` and exits, but the channel remains open. Downstream `for range` blocks forever.

3. **Closing a channel from the receiver, not the sender** — only the sender knows when no more values will be sent. Closing from the receiver side is a panic if the sender tries to send after.

4. **Racing on a shared results slice in fan-out** — appending to the same slice from multiple goroutines is a data race. Either use unique indices (pre-allocated slice), or protect with a mutex, or collect into a channel.

5. **Using `context.Background()` for the drain phase instead of a fresh context** — after the main context is cancelled, you need a fresh context for the drain timeout; deriving from the cancelled context gives a context that is already done.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 often have the right instinct but cannot explain the mechanism. Ask: "What would concretely go wrong?" — forcing a concrete failure scenario usually reveals whether the concept is solid.
- Section 3.1 (fanIn) is the most common place students produce a data race: closing `out` inside each forwarder goroutine (multiple closes → panic). The WaitGroup + separate goroutine for `close` is the canonical fix.
- Section 4.1 is specifically designed to test goroutine leak reasoning — the buffer-of-1 fix is not obvious. Students who get parts (a) and (c) without (b) are strong on concurrency but may need to review database/context integration.
- For the bonus: reward partial credit generously for students who get the generic type definition correct but have a minor bug in the rate limiter integration — generics + concurrency is genuinely hard.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
