# Exercises — Module 9: Concurrency

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just run code mentally — actually write or type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Expert | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Goroutine Greeting Race [🟢 Easy] [1 pt]

### Context
The simplest concurrency mistake in Go is forgetting that `main` returning kills all goroutines. This exercise forces you to observe that behavior and then fix it with `sync.WaitGroup`.

### Task
Write a Go program that:
1. Launches five goroutines, each printing `"Hello from goroutine N"` (where N is 1–5)
2. First, write the program **without** any synchronization and observe that some or all goroutines may not print
3. Then add a `sync.WaitGroup` to ensure `main` waits for all five goroutines before exiting

### Requirements
- [ ] Goroutines are launched with the `go` keyword
- [ ] `wg.Add(1)` is called before each goroutine is launched (not inside the goroutine)
- [ ] Each goroutine calls `wg.Done()` via `defer`
- [ ] `wg.Wait()` is called in `main` before printing "All done"
- [ ] The program compiles and all 5 greetings print every time

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The WaitGroup pattern:
```go
var wg sync.WaitGroup
for i := 1; i <= 5; i++ {
    wg.Add(1)           // add BEFORE launching
    go func(n int) {
        defer wg.Done() // Done via defer
        fmt.Printf("Hello from goroutine %d\n", n)
    }(i)                // pass i as argument — avoids the closure capture bug
}
wg.Wait()
```

</details>

### Expected Output / Acceptance Criteria
Five lines like `Hello from goroutine N` (order may vary — any ordering is correct), followed by `All done`.

```
Hello from goroutine 3
Hello from goroutine 1
Hello from goroutine 5
Hello from goroutine 2
Hello from goroutine 4
All done
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 5; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            fmt.Printf("Hello from goroutine %d\n", n)
        }(i) // pass i as argument to avoid closure capture of the loop variable
    }

    wg.Wait()
    fmt.Println("All done")
}
```

**Explanation:**
Without `wg.Wait()`, `main` returns before the goroutines run — they are killed. With the WaitGroup, `main` blocks at `Wait()` until all five goroutines call `Done()`. Note that `i` is passed as the argument `n` — this is essential. Without it, all goroutines would capture the same `i` variable and likely all print 5 (the final value after the loop ends).

**Common wrong answers:**
- `time.Sleep` at the end instead of `wg.Wait()` — works in demos, never correct in production
- Calling `wg.Add(1)` inside the goroutine body — races with `wg.Wait()` in main

</details>

---

## Exercise 2: Unbuffered Channel Ping-Pong [🟢 Easy] [1 pt]

### Context
An unbuffered channel is a rendezvous point — send blocks until receive is ready, and vice versa. This exercise demonstrates that synchronization by using an unbuffered channel to create a guaranteed ordering between two goroutines.

### Task
Write a Go program using an unbuffered `chan struct{}` (a signal-only channel carrying no data) to implement the following sequence precisely:
1. Main goroutine prints `"ping"`
2. Background goroutine prints `"pong"` — but only AFTER main prints `"ping"`
3. Main goroutine prints `"done"` — but only AFTER the background goroutine prints `"pong"`

### Requirements
- [ ] Use an unbuffered `chan struct{}` (not `chan bool` or `chan int`)
- [ ] The ordering ping → pong → done is guaranteed every run, not just likely
- [ ] No `time.Sleep` anywhere
- [ ] The program compiles and runs without deadlock

### Hints
<details>
<summary>Hint 1</summary>

Use two channels: one to signal "ping sent" (from main to goroutine), one to signal "pong sent" (from goroutine back to main). Or use one channel where main sends to trigger the goroutine and the goroutine sends back to signal completion.

</details>

<details>
<summary>Hint 2</summary>

`struct{}` is the idiomatic type for signal-only channels because it takes zero bytes. Send with `ch <- struct{}{}` and receive with `<-ch`.

</details>

### Expected Output / Acceptance Criteria
```
ping
pong
done
```
This exact order, guaranteed every run.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    ping := make(chan struct{}) // main sends after printing "ping"
    pong := make(chan struct{}) // goroutine sends after printing "pong"

    go func() {
        <-ping              // wait for main to print "ping"
        fmt.Println("pong")
        pong <- struct{}{} // signal that pong is done
    }()

    fmt.Println("ping")
    ping <- struct{}{} // signal goroutine; blocks until goroutine receives
    <-pong             // wait for goroutine to finish
    fmt.Println("done")
}
```

**Explanation:**
The unbuffered channel enforces ordering: `ping <- struct{}{}` blocks until the goroutine executes `<-ping`. Only then does the goroutine print "pong" and signal back. `<-pong` in main blocks until "pong" is printed. The result is a guaranteed sequence. This is the essence of the rendezvous/handshake pattern: channels as synchronization points, not just data conduits.

</details>

---

## Exercise 3: Buffered Channel Work Queue [🟡 Medium] [2 pts]

### Context
Buffered channels are useful as work queues: a producer can enqueue work ahead of consumers without blocking. This exercise uses a buffered channel as the bridge between a producer goroutine and multiple consumer goroutines, coordinated with a `sync.WaitGroup`.

### Task
Write a Go program that:
1. Creates a buffered channel `jobs` with capacity 10
2. Launches a producer goroutine that sends integers 1–10 to `jobs`, then closes the channel
3. Launches 3 consumer goroutines that each receive from `jobs` using `for range` (the range loop ends automatically when `jobs` is closed)
4. Each consumer prints `"Worker N processed job J"` for each job it receives
5. Uses `sync.WaitGroup` to wait for all consumers to finish
6. After `wg.Wait()`, prints `"All jobs complete"`

### Requirements
- [ ] Channel capacity is 10 (buffered)
- [ ] Producer goroutine closes the channel after all jobs are sent
- [ ] Consumers use `for range` over the channel
- [ ] `sync.WaitGroup` with `Add` before launch, `Done` via defer
- [ ] The program is race-free (run `go run -race` to verify)

### Hints
<details>
<summary>Hint 1</summary>

Structure:
```go
jobs := make(chan int, 10)
// Launch producer goroutine that sends and then closes
// Launch 3 consumer goroutines with wg.Add/Done
// wg.Wait()
```

</details>

<details>
<summary>Hint 2</summary>

When the producer closes the channel, all three consumers' `for range` loops will exit after draining the remaining items. Only `close` needs to be called once — the three consumers do not each need to detect or handle the close manually; `range` handles that automatically.

</details>

### Expected Output / Acceptance Criteria
10 lines like `Worker N processed job J` (N ∈ {1,2,3}, J ∈ {1..10}), followed by `All jobs complete`. Order of the 10 lines is nondeterministic.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    jobs := make(chan int, 10)
    var wg sync.WaitGroup

    // Producer
    go func() {
        for j := 1; j <= 10; j++ {
            jobs <- j
        }
        close(jobs) // signal consumers that no more jobs are coming
    }()

    // Consumers
    for w := 1; w <= 3; w++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for j := range jobs { // range exits when jobs is closed and empty
                fmt.Printf("Worker %d processed job %d\n", workerID, j)
            }
        }(w)
    }

    wg.Wait()
    fmt.Println("All jobs complete")
}
```

**Explanation:**
The buffered channel with capacity 10 means the producer can enqueue all 10 jobs before any consumer picks one up — no blocking on the producer side. The `for range jobs` in each consumer keeps receiving until the channel is closed and empty. When all consumers finish, `wg.Wait()` unblocks. Notice that job distribution between workers is nondeterministic — the scheduler decides which worker goroutine runs next.

**What makes this exercise important:** It demonstrates the canonical producer/consumer pattern: producer owns the channel and closes it; consumers range over it; WaitGroup tracks completion.

</details>

---

## Exercise 4: select with Timeout and Default [🟡 Medium] [2 pts]

### Context
`select` is the tool for working with multiple channels. Its `default` case enables non-blocking checks; `time.After` enables timeouts. This exercise uses both.

### Task
Write a Go function `poll(ch <-chan int, timeout time.Duration) (int, string)` that:
1. Uses `select` to try to receive from `ch`
2. If a value arrives within `timeout`, returns `(value, "received")`
3. If no value arrives within `timeout`, returns `(0, "timeout")`
4. Additionally, before the main `select`, makes a **non-blocking** check using `select` with `default` — if a value is already available, return it immediately with `"immediate"` (no waiting)

In `main`, demonstrate all three outcomes:
- Call `poll` on a channel that already has a value (buffered, pre-loaded)
- Call `poll` on a channel that will have a value before the timeout
- Call `poll` on a channel that will never have a value within the timeout

### Requirements
- [ ] The non-blocking pre-check uses `select { case v := <-ch: ... default: ... }` form
- [ ] The main timeout uses `select { case v := <-ch: ... case <-time.After(timeout): ... }` form
- [ ] All three outcomes are demonstrated in `main`
- [ ] Import: `"fmt"`, `"time"`

### Hints
<details>
<summary>Hint 1</summary>

For the non-blocking check, write a select with only two cases: the receive case and a default. This select never blocks — if the channel has a value, it receives; otherwise it falls through to the default immediately.

</details>

<details>
<summary>Hint 2</summary>

For demonstrating the "value arrives before timeout" case: create a goroutine that sleeps for less than the timeout and then sends a value. For "never arrives in time": use a very short timeout with no sender goroutine.

</details>

### Expected Output / Acceptance Criteria
```
immediate: 42
received: 99
timeout: 0
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "time"
)

func poll(ch <-chan int, timeout time.Duration) (int, string) {
    // Non-blocking check first: is there already a value?
    select {
    case v := <-ch:
        return v, "immediate"
    default:
        // nothing ready right now — fall through to the timed wait
    }

    // Timed wait
    select {
    case v := <-ch:
        return v, "received"
    case <-time.After(timeout):
        return 0, "timeout"
    }
}

func main() {
    // Case 1: value already in buffered channel
    ch1 := make(chan int, 1)
    ch1 <- 42
    v, status := poll(ch1, 100*time.Millisecond)
    fmt.Printf("%s: %d\n", status, v) // immediate: 42

    // Case 2: value arrives before timeout
    ch2 := make(chan int, 1)
    go func() {
        time.Sleep(10 * time.Millisecond)
        ch2 <- 99
    }()
    v, status = poll(ch2, 200*time.Millisecond)
    fmt.Printf("%s: %d\n", status, v) // received: 99

    // Case 3: timeout expires before value arrives
    ch3 := make(chan int) // unbuffered, nobody sends
    v, status = poll(ch3, 50*time.Millisecond)
    fmt.Printf("%s: %d\n", status, v) // timeout: 0
}
```

**Explanation:**
The two-stage select is a practical pattern: check immediately first (avoids creating a timer at all if a value is already ready), then wait with a timeout. `time.After(timeout)` creates a channel that fires after the duration; if the receive case wins, the timer's channel is abandoned (it fires eventually and is GC'd). The buffered channel in `ch1` lets us pre-load it before calling `poll`.

</details>

---

## Exercise 5: Fix the Data Race [🔴 Hard] [3 pts]

### Context
Data races are silent bugs — the program may appear to work on your machine but fail in production under different scheduling. This exercise gives you a racy program, asks you to detect it with the race detector, diagnose it, and fix it correctly.

### Task
The following program is **intentionally broken** — it has a data race. Your tasks:

1. Copy and run the program as-is. Note the output (it may or may not be 1000).
2. Run it with `go run -race main.go` and read the race report.
3. Identify which lines are racing and explain why.
4. Fix the race **using `sync.Mutex`**.
5. Also provide an alternative fix **using `sync/atomic`**.
6. Verify both fixes with `go run -race`.

**Broken program:**
```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    count := 0
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            count++ // RACE: concurrent read-modify-write
        }()
    }

    wg.Wait()
    fmt.Println("Final count:", count) // may not be 1000
}
```

### Requirements
- [ ] Diagnose the race: explain which two operations race and why `count++` is not atomic
- [ ] Provide a mutex-based fix with `sync.Mutex`
- [ ] Provide an atomic fix with `sync/atomic.AddInt64` (change `count` to `int64`)
- [ ] Both fixes compile and pass `go run -race` without warnings
- [ ] Both fixes always print `Final count: 1000`

### Hints
<details>
<summary>Hint 1 — diagnosis</summary>

`count++` is a read-modify-write: the CPU reads `count`, adds 1, and writes back. Between the read and the write, another goroutine can read the same old value. Both increments start from the same base, and one increment is "lost." This is not atomic in Go without explicit synchronization.

</details>

<details>
<summary>Hint 2 — mutex fix</summary>

```go
var mu sync.Mutex
// ...
mu.Lock()
count++
mu.Unlock()
```

Or `defer mu.Unlock()` if there's more code in the critical section. For a single `count++`, the explicit Lock/Unlock without defer is fine and slightly more efficient.

</details>

<details>
<summary>Hint 3 — atomic fix</summary>

```go
import "sync/atomic"
var count int64
atomic.AddInt64(&count, 1)
```

`atomic.AddInt64` performs the read-modify-write as a single atomic CPU instruction — no lock needed. This is the most efficient solution for a simple counter.

</details>

### Solution
<details>
<summary>Show Solution</summary>

**Mutex fix:**
```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    count := 0
    var mu sync.Mutex
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            mu.Lock()
            count++   // protected by mutex — no race
            mu.Unlock()
        }()
    }

    wg.Wait()
    fmt.Println("Final count:", count) // always 1000
}
```

**Atomic fix:**
```go
package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)

func main() {
    var count int64 // must be int64 (or int32) for atomic ops
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            atomic.AddInt64(&count, 1) // atomic read-modify-write — no race
        }()
    }

    wg.Wait()
    fmt.Println("Final count:", atomic.LoadInt64(&count)) // always 1000
}
```

**Explanation of the race:**
`count++` compiles to three operations: (1) read `count` into a register, (2) add 1, (3) write back to `count`. If goroutine A reads `count=500`, goroutine B also reads `count=500` before A writes back, both compute `501`, and both write `501`. One increment is lost. Run enough goroutines and you lose many increments.

**Mutex vs atomic trade-off:**
The atomic approach is faster for simple integer operations because it uses a single CPU instruction (LOCK XADD on x86) rather than acquiring and releasing a kernel-level lock. Use atomics for simple counters/flags; use mutexes for protecting larger critical sections or non-integer data.

</details>

---

## Exercise 6: Fan-Out with Result Collection [🔴 Hard] [3 pts]

### Context
Fan-out is one of the most common concurrency patterns: distribute N units of work to N goroutines, collect the results, and process them. This exercise implements a parallel URL "checker" (using simulated delays instead of real HTTP to keep it self-contained).

### Task
Implement a `checkAll` function that takes a slice of "URLs" (strings) and a `checkFn func(url string) (int, error)` function, and runs all checks concurrently. Each check returns a status code and possibly an error. Collect all results and return them.

Use the following type for results:
```go
type Result struct {
    URL    string
    Status int
    Err    error
}
```

Requirements:
- [ ] All checks run concurrently (one goroutine per URL)
- [ ] Results are collected on a single `chan Result`
- [ ] Use `sync.WaitGroup` to close the results channel after all goroutines finish
- [ ] `checkAll` returns `[]Result` with all results (order may vary)
- [ ] Handle the case where `checkFn` returns an error — store it in `Result.Err`
- [ ] Run with `go run -race` — no data races

Demonstrate in `main` with at least 4 URLs (simulated with a `checkFn` that returns different status codes based on the URL string).

### Hints
<details>
<summary>Hint 1 — structure</summary>

```go
func checkAll(urls []string, checkFn func(string) (int, error)) []Result {
    results := make(chan Result, len(urls))
    var wg sync.WaitGroup
    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            status, err := checkFn(u)
            results <- Result{URL: u, Status: status, Err: err}
        }(url)
    }
    go func() {
        wg.Wait()
        close(results)
    }()
    var out []Result
    for r := range results {
        out = append(out, r)
    }
    return out
}
```

</details>

<details>
<summary>Hint 2 — closing the results channel</summary>

The tricky part: you cannot close `results` in the main goroutine after `wg.Wait()` because `for range results` would block before `wg.Wait()` returns. The pattern is: launch a separate goroutine that calls `wg.Wait()` then `close(results)`, and use `for range` on the results channel in the main function body.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

type Result struct {
    URL    string
    Status int
    Err    error
}

func checkAll(urls []string, checkFn func(string) (int, error)) []Result {
    results := make(chan Result, len(urls)) // buffer avoids goroutine blocking
    var wg sync.WaitGroup

    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            status, err := checkFn(u)
            results <- Result{URL: u, Status: status, Err: err}
        }(url) // pass url as argument to avoid closure capture bug
    }

    // Close results channel after all goroutines finish
    go func() {
        wg.Wait()
        close(results)
    }()

    var out []Result
    for r := range results { // range exits when results is closed and empty
        out = append(out, r)
    }
    return out
}

// simulatedCheck mimics an HTTP check with a short delay
func simulatedCheck(url string) (int, error) {
    time.Sleep(5 * time.Millisecond) // simulate network latency
    switch url {
    case "https://ok.example.com":
        return 200, nil
    case "https://notfound.example.com":
        return 404, nil
    case "https://error.example.com":
        return 500, fmt.Errorf("internal server error")
    default:
        return 200, nil
    }
}

func main() {
    urls := []string{
        "https://ok.example.com",
        "https://notfound.example.com",
        "https://error.example.com",
        "https://another.example.com",
    }

    results := checkAll(urls, simulatedCheck)
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%-35s  status=%d  err=%v\n", r.URL, r.Status, r.Err)
        } else {
            fmt.Printf("%-35s  status=%d\n", r.URL, r.Status)
        }
    }
}
// Output (order nondeterministic):
// https://ok.example.com              status=200
// https://notfound.example.com        status=404
// https://error.example.com           status=500  err=internal server error
// https://another.example.com         status=200
```

**Key design decisions:**
- The results channel is buffered with `len(urls)` capacity so goroutines never block on the send — they can complete immediately, and the main goroutine drains the channel after.
- A separate goroutine calls `wg.Wait()` then `close(results)` — this is the standard pattern for "close after all senders finish."
- `url` is passed as the argument `u` to the goroutine closure, avoiding the loop variable capture bug.

</details>

---

## Exercise 7: Deadlock Diagnosis [🔴 Hard] [3 pts]

### Context
Reading deadlocked programs is a professional skill. This exercise gives you three broken programs. For each one, identify the deadlock, explain why it occurs, and provide a corrected version.

### Task
For each of the three programs below:
1. Identify which goroutines are blocked and on what operation
2. Explain why the deadlock occurs
3. Write the corrected version

**Program A — channel deadlock:**
```go
func main() {
    ch := make(chan int)
    ch <- 1 // ???
    fmt.Println(<-ch)
}
```

**Program B — missing close:**
```go
func main() {
    ch := make(chan int, 3)
    ch <- 10
    ch <- 20
    ch <- 30
    for v := range ch {
        fmt.Println(v)
    }
}
```

**Program C — mutex double-lock:**
```go
var mu sync.Mutex

func getAndProcess() int {
    mu.Lock()
    defer mu.Unlock()
    return process()
}

func process() int {
    mu.Lock()           // ???
    defer mu.Unlock()
    return 42
}

func main() {
    fmt.Println(getAndProcess())
}
```

### Requirements
- [ ] Correctly identify the blocked operation in each program
- [ ] Explain the root cause (not just "it's a deadlock")
- [ ] Provide a working corrected version for each

### Hints
<details>
<summary>Hint — Program A</summary>

An unbuffered channel send blocks until a receiver is ready. In `main`, there is only one goroutine. If the send blocks and there is no other goroutine to receive, there is nobody to unblock the send. The runtime detects all goroutines are asleep and panics.

</details>

<details>
<summary>Hint — Program B</summary>

`for range ch` reads until the channel is closed. If the channel is never closed, the loop blocks after consuming all buffered values, waiting for more that never come.

</details>

<details>
<summary>Hint — Program C</summary>

`sync.Mutex` in Go is **not reentrant** (not recursive). A goroutine that holds a lock and tries to lock it again will deadlock. This is a common surprise for developers coming from Java (where `synchronized` is reentrant).

</details>

### Solution
<details>
<summary>Show Solution</summary>

**Program A — fix: use a goroutine for the send, or use a buffered channel**
```go
// Fix 1: run the send in a goroutine (the receive in main unblocks it)
func main() {
    ch := make(chan int)
    go func() {
        ch <- 1 // goroutine sends; main receives
    }()
    fmt.Println(<-ch) // Output: 1
}

// Fix 2: use a buffered channel (send doesn't need a receiver to be ready)
func main() {
    ch := make(chan int, 1)
    ch <- 1 // doesn't block — buffer has space
    fmt.Println(<-ch) // Output: 1
}
```

**Root cause:** Unbuffered channel sends block until a receiver is ready. In the original, the single goroutine (`main`) blocks at `ch <- 1` and can never reach `<-ch`. No receiver will ever be ready — deadlock.

---

**Program B — fix: close the channel after sending**
```go
func main() {
    ch := make(chan int, 3)
    ch <- 10
    ch <- 20
    ch <- 30
    close(ch) // signal that no more values are coming

    for v := range ch {
        fmt.Println(v) // prints 10, 20, 30, then loop exits
    }
}
```

**Root cause:** `for range ch` does not know when to stop unless the channel is closed. After reading the 3 buffered values, the loop blocks waiting for a 4th value. Nobody sends it, nobody closes the channel — all goroutines (just `main` here) are asleep. Deadlock.

---

**Program C — fix: remove the inner lock (don't hold a lock when calling functions that lock the same mutex)**
```go
var mu sync.Mutex

// Option 1: process() does not lock (only called while mu is held)
func getAndProcess() int {
    mu.Lock()
    defer mu.Unlock()
    return process() // process is called while mu is held
}

func process() int {
    // No lock here — caller is responsible for holding mu
    return 42
}

// Option 2: split into public (locked) and internal (unlocked) versions
func getAndProcessPublic() int {
    mu.Lock()
    defer mu.Unlock()
    return processLocked()
}

func processLocked() int { // unexported, always called with mu held
    return 42
}
```

**Root cause:** `sync.Mutex` in Go is **non-reentrant**. When `getAndProcess` holds `mu` and calls `process`, `process` tries to `mu.Lock()` again — but the same goroutine already holds the lock. Since the same goroutine cannot hold `mu` twice, it blocks waiting for itself to release the lock. Deadlock. Unlike Java's `synchronized`, Go's mutex has no reentrancy — this is a deliberate design choice.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Goroutine Greeting Race | — | —/1 | — | — |
| Exercise 2 — Unbuffered Channel Ping-Pong | — | —/1 | — | — |
| Exercise 3 — Buffered Channel Work Queue | — | —/2 | — | — |
| Exercise 4 — select with Timeout and Default | — | —/2 | — | — |
| Exercise 5 — Fix the Data Race | — | —/3 | — | — |
| Exercise 6 — Fan-Out with Result Collection | — | —/3 | — | — |
| Exercise 7 — Deadlock Diagnosis | — | —/3 | — | — |
| **Total** | | **—/15** | | |

**Passing threshold:** 10/15 (65%). Aim for 13/15 (85%) before taking the test.
