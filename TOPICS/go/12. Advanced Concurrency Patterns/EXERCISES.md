# Exercises — Module 12: Advanced Concurrency Patterns

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read code mentally — compile and run your attempts.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If stuck after a genuine effort, use hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 10–20 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 20–35 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 40–75 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 75+ min | 5 pts |

---

## Exercise 1: Context-Aware Sleeper [🟢 Easy] [1 pt]

### Context
Every context-aware operation follows the same structure: do work OR return early if the context is cancelled. The simplest possible version is a cancellable `time.Sleep`. Mastering this one pattern unlocks the rest of the module.

### Task
Write a function `sleep(ctx context.Context, d time.Duration) error` that:
1. Waits for duration `d` to elapse — and returns `nil`
2. OR returns `ctx.Err()` immediately if the context is cancelled before `d` elapses

Call it from `main` with a context that has a 200ms timeout, but pass a 1-second sleep duration. Show that it returns before 1 second.

### Requirements
- [ ] Uses `select` with `time.After(d)` and `<-ctx.Done()`
- [ ] Returns `nil` when the timer fires normally
- [ ] Returns `ctx.Err()` when the context is cancelled first
- [ ] The function signature is `func sleep(ctx context.Context, d time.Duration) error`

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The body is a single `select`:
```go
select {
case <-time.After(d):
    return nil
case <-ctx.Done():
    return ctx.Err()
}
```

</details>

### Expected Output / Acceptance Criteria
```
sleep returned after ~200ms: context deadline exceeded
```
(The exact error message is `context.DeadlineExceeded.Error()` → `"context deadline exceeded"`.)

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// sleep waits for d or for ctx to be cancelled, whichever comes first.
func sleep(ctx context.Context, d time.Duration) error {
    select {
    case <-time.After(d):
        return nil // timer fired — clean completion
    case <-ctx.Done():
        return ctx.Err() // cancelled or deadline exceeded
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
    defer cancel()

    start := time.Now()
    err := sleep(ctx, 1*time.Second)
    fmt.Printf("sleep returned after %v: %v\n", time.Since(start).Round(time.Millisecond), err)
}
```

**Explanation:**
`time.After(d)` returns a `<-chan time.Time` that receives after `d`. `ctx.Done()` is a `<-chan struct{}` that receives when the context is cancelled or its deadline expires. The `select` races the two — whoever fires first wins. This is the canonical pattern for any "do work with a timeout" operation in Go.

</details>

---

## Exercise 2: Context Cancellation Propagation [🟢 Easy] [1 pt]

### Context
Understanding how cancellation propagates from parent to child context is critical before building any pipeline. When the parent is cancelled, all derived children are automatically cancelled — you don't need to cancel each child explicitly.

### Task
Write a program that:
1. Creates a parent context with a 500ms timeout
2. Creates a child context with `context.WithCancel(parent)` (no deadline on the child)
3. Starts a goroutine that uses the child context: it should loop, printing "tick" every 100ms, and exit when the child context is cancelled
4. The goroutine should NOT be cancelled by calling the child's cancel — it should be cancelled by the parent's deadline expiring

### Requirements
- [ ] Parent uses `context.WithTimeout`; child uses `context.WithCancel`
- [ ] The goroutine selects on `childCtx.Done()`
- [ ] `childCancel` is deferred but is NOT called before the parent expires
- [ ] Output shows approximately 4–5 "tick" prints before the goroutine exits

### Hints
<details>
<summary>Hint 1</summary>

Even though `childCtx` was created with `WithCancel` (no deadline), it inherits the parent's cancellation. When the parent's 500ms deadline fires, `childCtx.Done()` is also closed automatically.

</details>

### Expected Output / Acceptance Criteria
```
tick
tick
tick
tick
tick (approximately)
goroutine: child context cancelled: context deadline exceeded
```
(Number of ticks may vary ±1 depending on scheduling.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "fmt"
    "time"
)

func main() {
    parentCtx, parentCancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
    defer parentCancel()

    childCtx, childCancel := context.WithCancel(parentCtx)
    defer childCancel() // child cancel deferred, but parent will fire first

    done := make(chan struct{})
    go func() {
        defer close(done)
        ticker := time.NewTicker(100 * time.Millisecond)
        defer ticker.Stop()
        for {
            select {
            case <-ticker.C:
                fmt.Println("tick")
            case <-childCtx.Done():
                fmt.Printf("goroutine: child context cancelled: %v\n", childCtx.Err())
                return
            }
        }
    }()

    <-done
}
```

**Explanation:**
`context.WithCancel(parentCtx)` creates a child that is cancelled whenever `parentCtx` is cancelled (or expires). The child does not need its own deadline — it inherits. This is the propagation model: cancelling (or expiring) a context cancels all contexts derived from it. The goroutine exits cleanly because it selects on `childCtx.Done()`.

</details>

---

## Exercise 3: Bounded Worker Pool [🟡 Medium] [2 pts]

### Context
Unbounded goroutine spawning is a common cause of memory exhaustion and cascading failures. A bounded worker pool is the primary tool for controlling concurrency when processing a slice of work items.

### Task
Implement a function `processURLs(ctx context.Context, urls []string, workers int) []string` that:
1. Spawns exactly `workers` goroutines
2. Feeds each URL from a jobs channel to the next available worker
3. Each worker makes a HEAD request and records `"OK: <url>"` or `"ERR: <url>: <error>"`
4. Collects all results (preserving any order is fine — results are nondeterministic)
5. Returns the results slice after all workers finish

### Requirements
- [ ] Exactly `workers` goroutines are running, not one per URL
- [ ] Workers use `context.WithTimeout` for individual requests (2s per request)
- [ ] Workers exit cleanly when the jobs channel is closed
- [ ] Uses `sync.WaitGroup` to wait for all workers before closing the results channel
- [ ] Compile and run; output shows results for all URLs

### Hints
<details>
<summary>Hint 1 (structural)</summary>

Structure:
```go
jobs := make(chan string, len(urls))  // buffer all URLs upfront
for _, u := range urls { jobs <- u }
close(jobs)  // workers exit when jobs is drained

results := make(chan string, len(urls))
var wg sync.WaitGroup
for i := 0; i < workers; i++ {
    wg.Add(1)
    go worker(ctx, &wg, jobs, results)
}
go func() { wg.Wait(); close(results) }()

var out []string
for r := range results { out = append(out, r) }
return out
```

</details>

<details>
<summary>Hint 2 (worker body)</summary>

```go
func worker(ctx context.Context, wg *sync.WaitGroup, jobs <-chan string, results chan<- string) {
    defer wg.Done()
    for url := range jobs {
        reqCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
        req, _ := http.NewRequestWithContext(reqCtx, http.MethodHead, url, nil)
        _, err := http.DefaultClient.Do(req)
        cancel()
        if err != nil {
            results <- "ERR: " + url + ": " + err.Error()
        } else {
            results <- "OK: " + url
        }
    }
}
```

</details>

### Expected Output / Acceptance Criteria
```
OK: https://go.dev
OK: https://pkg.go.dev
ERR: https://nonexistent.example.invalid: ...
(order is nondeterministic)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "fmt"
    "net/http"
    "sync"
    "time"
)

func worker(ctx context.Context, wg *sync.WaitGroup, jobs <-chan string, results chan<- string) {
    defer wg.Done()
    for url := range jobs { // exits when jobs is closed and drained
        reqCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
        req, err := http.NewRequestWithContext(reqCtx, http.MethodHead, url, nil)
        if err != nil {
            cancel()
            results <- fmt.Sprintf("ERR: %s: %v", url, err)
            continue
        }
        resp, err := http.DefaultClient.Do(req)
        cancel() // always cancel the per-request context
        if err != nil {
            results <- fmt.Sprintf("ERR: %s: %v", url, err)
        } else {
            resp.Body.Close()
            results <- fmt.Sprintf("OK: %s (%d)", url, resp.StatusCode)
        }
    }
}

func processURLs(ctx context.Context, urls []string, workers int) []string {
    jobs := make(chan string, len(urls))
    for _, u := range urls {
        jobs <- u
    }
    close(jobs) // pre-fill and close; workers drain and exit

    results := make(chan string, len(urls))
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go worker(ctx, &wg, jobs, results)
    }
    go func() {
        wg.Wait()
        close(results)
    }()

    var out []string
    for r := range results {
        out = append(out, r)
    }
    return out
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    urls := []string{
        "https://go.dev",
        "https://pkg.go.dev",
        "https://nonexistent.example.invalid",
    }
    // NOTE: output order is nondeterministic
    for _, r := range processURLs(ctx, urls, 2) {
        fmt.Println(r)
    }
}
```

**Explanation:**
By pre-filling the jobs channel and closing it, workers read until empty and then exit naturally from the `for url := range jobs` loop. `wg.Wait()` in a goroutine closes `results` once all workers exit, allowing the caller to range over `results` until it drains. The `context.WithTimeout` per request ensures no single HTTP call blocks for more than 2 seconds.

</details>

---

## Exercise 4: Three-Stage Pipeline with Cancellation [🟡 Medium] [2 pts]

### Context
A pipeline composes stages where each stage reads from an upstream channel and writes to a downstream channel. Cancellation must propagate: when the context is cancelled, every stage must stop producing and exit, closing its output channel.

### Task
Build a three-stage pipeline:
1. **Stage 1 `generate`**: emits integers 1..N to a channel
2. **Stage 2 `square`**: receives integers and emits their squares
3. **Stage 3** (in `main`): reads squares and prints them

All stages must:
- Accept `ctx context.Context` as the first parameter
- Use `select` with `ctx.Done()` on every send
- Close their output channel when they exit (`defer close(out)`)

Cancel the context after 5 values have been printed, and verify that the pipeline stops cleanly (no goroutine leak).

### Requirements
- [ ] Three distinct functions: `generate`, `square`, and a consuming loop in `main`
- [ ] Each stage goroutine defers `close(out)`
- [ ] Each stage `select`s on `ctx.Done()` for sends
- [ ] `generate` stops if N is exhausted or ctx is cancelled
- [ ] The consumer cancels after 5 values and confirms no deadlock

### Hints
<details>
<summary>Hint 1</summary>

```go
func generate(ctx context.Context, n int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for i := 1; i <= n; i++ {
            select {
            case out <- i:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}
```

</details>

### Expected Output / Acceptance Criteria
```
1
4
9
16
25
cancelled after 5 values
```
(Exact number depends on when cancel() is called, but should be approximately 5.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "fmt"
)

// generate emits integers 1..n, stopping early if ctx is cancelled.
func generate(ctx context.Context, n int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for i := 1; i <= n; i++ {
            select {
            case out <- i:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// square receives integers and emits their squares.
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
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

    count := 0
    for sq := range square(ctx, generate(ctx, 100)) {
        fmt.Println(sq)
        count++
        if count >= 5 {
            cancel() // cancel the context — upstream stages will stop
            break    // stop consuming
        }
    }
    fmt.Println("cancelled after", count, "values")
}
```

**Explanation:**
When `cancel()` is called and then the consumer `break`s, the `square` stage's `select` will fire on `ctx.Done()` instead of `out <-` (because nobody is reading `out` anymore), and it returns, closing its channel. `generate` similarly exits on `ctx.Done()`. All goroutines exit cleanly — no leak. The `for n := range in` in `square` also exits because `generate`'s `close(out)` will be reached — both paths lead to clean exit.

</details>

---

## Exercise 5: errgroup Fan-Out with Error Handling [🟡 Medium] [2 pts]

### Context
`errgroup.WithContext` is the idiomatic replacement for `sync.WaitGroup + error channel`. It automatically propagates the first error and cancels the shared context, signalling other goroutines to stop early.

### Task
Write a function `checkAll(ctx context.Context, urls []string) error` that:
1. Uses `errgroup.WithContext` to fan out one goroutine per URL
2. Each goroutine makes an HTTP HEAD request for its URL
3. Returns the first error encountered (if any)
4. On error, the other goroutines should respect the cancelled context and stop early

Call it with a mix of valid and invalid URLs and print the result.

### Requirements
- [ ] Uses `errgroup.WithContext` (import `golang.org/x/sync/errgroup`)
- [ ] Each goroutine returns `nil` on success or a non-nil `error` on failure
- [ ] Loop variable capture: `i, url := i, url` before the closure (or Go 1.22+)
- [ ] Uses `http.NewRequestWithContext(ctx, ...)` — respects context cancellation
- [ ] `g.Wait()` returns the first non-nil error

### Hints
<details>
<summary>Hint 1</summary>

```go
g, ctx := errgroup.WithContext(ctx)
for _, url := range urls {
    url := url
    g.Go(func() error {
        req, err := http.NewRequestWithContext(ctx, http.MethodHead, url, nil)
        if err != nil { return err }
        resp, err := http.DefaultClient.Do(req)
        if err != nil { return fmt.Errorf("HEAD %s: %w", url, err) }
        resp.Body.Close()
        return nil
    })
}
return g.Wait()
```

</details>

### Expected Output / Acceptance Criteria
```
error: HEAD https://nonexistent.example.invalid: ...
```
Or `nil` if all URLs succeed.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "fmt"
    "net/http"
    "time"

    "golang.org/x/sync/errgroup"
)

func checkAll(ctx context.Context, urls []string) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, url := range urls {
        url := url // capture — required before Go 1.22
        g.Go(func() error {
            req, err := http.NewRequestWithContext(ctx, http.MethodHead, url, nil)
            if err != nil {
                return fmt.Errorf("build request %s: %w", url, err)
            }
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                return fmt.Errorf("HEAD %s: %w", url, err)
            }
            resp.Body.Close()
            return nil
        })
    }
    return g.Wait() // blocks until all goroutines finish; returns first non-nil error
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    urls := []string{
        "https://go.dev",
        "https://nonexistent.example.invalid",
        "https://pkg.go.dev",
    }
    if err := checkAll(ctx, urls); err != nil {
        fmt.Println("error:", err)
    } else {
        fmt.Println("all OK")
    }
}
```

**Explanation:**
`errgroup.WithContext` derives a child context from the provided one. When any `g.Go` closure returns a non-nil error, the errgroup internally calls `cancel()` on that child context. Other goroutines using `http.NewRequestWithContext(ctx, ...)` will see the context cancelled and their `Do` calls will return early. `g.Wait()` waits for all goroutines and returns the first error. The error is deterministic (it is always the first one returned, not the first one started).

</details>

---

## Exercise 6: Semaphore via Buffered Channel [🟡 Medium] [2 pts]

### Context
A semaphore limits the number of goroutines that can execute a critical section simultaneously. A buffered channel is the idiomatic Go semaphore: trying to send when the buffer is full blocks (acquires a slot); receiving releases it.

### Task
Write a function `concurrentProcess(ctx context.Context, items []int, limit int) []int` that:
1. Launches one goroutine per item
2. Uses a buffered channel semaphore of size `limit` to allow at most `limit` goroutines to "process" simultaneously
3. Each goroutine "processes" its item by squaring it (simulating work with a 10ms sleep)
4. Cancels early if ctx is done
5. Returns a slice of results (order may vary)

### Requirements
- [ ] `sem := make(chan struct{}, limit)` is the semaphore
- [ ] Each goroutine acquires with `sem <- struct{}{}` (or exits on ctx.Done)
- [ ] Each goroutine releases with `defer func() { <-sem }()`
- [ ] Uses `sync.WaitGroup` to wait for all goroutines

### Hints
<details>
<summary>Hint 1</summary>

```go
sem := make(chan struct{}, limit)
results := make([]int, len(items))
var wg sync.WaitGroup
for i, item := range items {
    i, item := i, item
    wg.Add(1)
    go func() {
        defer wg.Done()
        select {
        case sem <- struct{}{}: // acquire
        case <-ctx.Done():
            return
        }
        defer func() { <-sem }() // release
        time.Sleep(10 * time.Millisecond)
        results[i] = item * item
    }()
}
wg.Wait()
return results
```

</details>

### Expected Output / Acceptance Criteria
The function returns `[1, 4, 9, 16, 25]` for input `[1, 2, 3, 4, 5]` with `limit=2`. The 5 goroutines run, but only 2 at a time execute the "work" block.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func concurrentProcess(ctx context.Context, items []int, limit int) []int {
    sem := make(chan struct{}, limit) // semaphore: at most limit goroutines in the work section
    results := make([]int, len(items))
    var wg sync.WaitGroup

    for i, item := range items {
        i, item := i, item
        wg.Add(1)
        go func() {
            defer wg.Done()
            // Acquire semaphore slot — blocks if limit goroutines are already working.
            select {
            case sem <- struct{}{}:
            case <-ctx.Done():
                return
            }
            defer func() { <-sem }() // release when this goroutine finishes work

            // Simulate work.
            time.Sleep(10 * time.Millisecond)
            results[i] = item * item
        }()
    }

    wg.Wait()
    return results
}

func main() {
    ctx := context.Background()
    results := concurrentProcess(ctx, []int{1, 2, 3, 4, 5}, 2)
    fmt.Println(results) // [1 4 9 16 25]
}
```

**Explanation:**
All 5 goroutines start immediately but only 2 can proceed past `sem <- struct{}{}` at once; the rest block. When a goroutine finishes and calls `<-sem`, it releases its slot and one blocked goroutine unblocks. Writing to `results[i]` is safe because each goroutine writes to a unique index — no two goroutines share the same `i`. This is the key safety property of the results-slice pattern.

</details>

---

## Exercise 7: Goroutine Leak Detection and Fix [🔴 Hard] [3 pts]

### Context
Goroutine leaks are among the most common bugs in production Go services. This exercise presents two leaky functions and asks you to diagnose and fix each.

### Task
Each function below has a goroutine leak. For each:
a) Identify the exact leak (which goroutine blocks, and why it will never unblock)
b) Fix it without changing the function's observable behavior

**Function A:**
```go
func doWorkA(input int) int {
    ch := make(chan int)
    go func() {
        ch <- expensiveCompute(input)
    }()
    return <-ch
}
```
*(This function looks correct — what's the leak?)*

**Function B:**
```go
func watchUpdates(ctx context.Context, updates <-chan string, callback func(string)) {
    go func() {
        for update := range updates {
            callback(update)
        }
    }()
}
```
*(When does the goroutine exit? Under what common condition will it never exit?)*

### Requirements
- [ ] Correctly identifies the leak condition for both A and B
- [ ] Provides a fix for both that allows the goroutine to exit
- [ ] Fix for A must handle caller abandoning the returned channel (if applicable)
- [ ] Fix for B must handle ctx cancellation

### Hints
<details>
<summary>Hint 1 — Function A</summary>

Function A actually has no leak when called normally — the goroutine sends and the caller receives. The leak occurs when the caller is itself cancelled before reading from the returned channel. But as written, the goroutine has no escape hatch if the caller disappears. Consider: what if `doWorkA` is called in a goroutine that returns early due to a cancelled context?

</details>

<details>
<summary>Hint 2 — Function B</summary>

The goroutine in B ranges over `updates`. It will exit when `updates` is closed. But what if `updates` is never closed? For example, a long-running server that monitors `updates` might have `ctx` cancelled (on shutdown) but `updates` kept open by another component. The goroutine will block forever.

</details>

<details>
<summary>Hint 3 — Fix structure</summary>

For A: add a context parameter and `select` the send with `ctx.Done()`. For B: add a `select` inside the `for` with `ctx.Done()`.

</details>

### Expected Output / Acceptance Criteria
- Clear explanation of when each goroutine leaks
- Fixed versions compile and the goroutines exit in all scenarios
- Function B fixed version exits when `ctx` is cancelled even if `updates` is never closed

### Solution
<details>
<summary>Show Solution</summary>

**Analysis — Function A:**
`doWorkA` appears safe in isolation — the goroutine sends and the caller receives. The leak occurs when the caller context is cancelled *before* reading from the returned channel: if the caller does `ctx.Done() → return` instead of reading the channel, the goroutine blocks on `ch <- ...` forever.

**Fixed A:**
```go
func doWorkA(ctx context.Context, input int) (int, error) {
    ch := make(chan int, 1) // buffer of 1 — goroutine can always send and exit
    go func() {
        ch <- expensiveCompute(input)
    }()
    select {
    case result := <-ch:
        return result, nil
    case <-ctx.Done():
        return 0, ctx.Err() // caller gives up; goroutine sends to buffered ch and exits
    }
}
```

The buffer-of-1 trick: even if the caller exits via `ctx.Done()`, the goroutine can complete its send to the buffered channel and exit. No goroutine is left waiting.

**Analysis — Function B:**
The goroutine ranges over `updates` and exits only when `updates` is closed. If the sending side never closes `updates` (e.g., it's a long-lived broadcast channel), the goroutine is leaked when `ctx` is cancelled (e.g., at shutdown).

**Fixed B:**
```go
func watchUpdates(ctx context.Context, updates <-chan string, callback func(string)) {
    go func() {
        for {
            select {
            case update, ok := <-updates:
                if !ok {
                    return // channel closed — exit naturally
                }
                callback(update)
            case <-ctx.Done():
                return // context cancelled — exit
            }
        }
    }()
}
```

Adding `ctx.Done()` to the `select` gives the goroutine a second exit path. When the context is cancelled (e.g., on service shutdown), the goroutine exits regardless of whether `updates` is closed.

</details>

---

## Exercise 8: Graceful Shutdown with Drain [🔴 Hard] [3 pts]

### Context
A server must not kill goroutines mid-operation when it receives SIGINT. Graceful shutdown means: stop accepting new work, then wait for in-flight work to complete (up to a maximum drain timeout), then exit.

### Task
Write a simulated server that:
1. Uses `signal.NotifyContext` to listen for SIGINT/SIGTERM
2. Launches 10 "worker" goroutines that each process one item every 300ms (simulate with `time.Sleep`)
3. On shutdown signal: stops sending new work, waits up to 2 seconds for workers to finish current item
4. Prints "clean shutdown" if all workers finish in time, or "forced shutdown" if the drain timeout expires

Test by running the program and pressing Ctrl+C.

### Requirements
- [ ] Uses `signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)`
- [ ] Workers select on `ctx.Done()` — they exit when the context is cancelled
- [ ] A separate `drainCtx` with a 2-second timeout governs the drain phase
- [ ] Uses `sync.WaitGroup` + a done channel to determine clean vs forced shutdown
- [ ] Compiles and runs

### Hints
<details>
<summary>Hint 1</summary>

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
// ... start workers using ctx ...
<-ctx.Done() // block until signal
// ... drain phase with drainCtx ...
```

</details>

<details>
<summary>Hint 2 — drain pattern</summary>

```go
drainCtx, drainCancel := context.WithTimeout(context.Background(), 2*time.Second)
defer drainCancel()
done := make(chan struct{})
go func() { wg.Wait(); close(done) }()
select {
case <-done:     fmt.Println("clean shutdown")
case <-drainCtx.Done(): fmt.Println("forced shutdown")
}
```

</details>

### Expected Output / Acceptance Criteria
```
worker 3: processing item 1
worker 0: processing item 1
... (workers processing)
^C
shutdown signal received; draining...
worker 0: shutting down
... (all workers shut down within ~300ms, well under 2s)
clean shutdown
```

### Solution
<details>
<summary>Show Solution</summary>

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
    numWorkers := 5

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            item := 0
            for {
                select {
                case <-ctx.Done():
                    fmt.Printf("worker %d: shutting down\n", id)
                    return
                case <-time.After(10 * time.Millisecond): // check for work
                }
                item++
                fmt.Printf("worker %d: processing item %d\n", id, item)
                // Simulate processing time.
                select {
                case <-time.After(300 * time.Millisecond):
                case <-ctx.Done():
                    fmt.Printf("worker %d: interrupted mid-item\n", id)
                    return
                }
            }
        }(i)
    }

    // Block until signal arrives.
    <-ctx.Done()
    fmt.Println("shutdown signal received; draining...")

    // Give workers up to 2 seconds to finish.
    drainCtx, drainCancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer drainCancel()

    done := make(chan struct{})
    go func() {
        wg.Wait()
        close(done)
    }()

    select {
    case <-done:
        fmt.Println("clean shutdown")
    case <-drainCtx.Done():
        fmt.Println("forced shutdown — some work incomplete")
    }
}
```

**Explanation:**
`signal.NotifyContext` creates a context that is cancelled when SIGINT or SIGTERM is received — it's the idiomatic replacement for `signal.Notify` + manual channel. Workers select on `ctx.Done()` at two points: before picking up new work and during the simulated processing. The drain phase uses a fresh context (not derived from the cancelled one) with its own 2-second timeout — this is crucial since the original context is already cancelled. The `select` between `done` and `drainCtx.Done()` determines which path wins.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Context-Aware Sleeper | — | —/1 | — | — |
| Exercise 2 — Context Cancellation Propagation | — | —/1 | — | — |
| Exercise 3 — Bounded Worker Pool | — | —/2 | — | — |
| Exercise 4 — Three-Stage Pipeline | — | —/2 | — | — |
| Exercise 5 — errgroup Fan-Out | — | —/2 | — | — |
| Exercise 6 — Semaphore via Buffered Channel | — | —/2 | — | — |
| Exercise 7 — Goroutine Leak Detection and Fix | — | —/3 | — | — |
| Exercise 8 — Graceful Shutdown with Drain | — | —/3 | — | — |
| **Total** | | **—/16** | | |

**Passing threshold:** 11/16 (68%). Aim for 14/16 (87%) before taking the test.
