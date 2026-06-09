# Module 9: Concurrency

[← Module 8: Error Handling](../8.%20Error%20Handling/) | [Topic Home](../README.md) | [Module 10: Generics →](../10.%20Generics/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-blue)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Concurrency vs Parallelism](#concurrency-vs-parallelism)
  - [Goroutines](#goroutines)
  - [Channels — Unbuffered and Buffered](#channels--unbuffered-and-buffered)
  - [Channel Direction Types](#channel-direction-types)
  - [Closing Channels and range](#closing-channels-and-range)
  - [select — Multiplexing Channels](#select--multiplexing-channels)
  - [Nil Channel Behavior](#nil-channel-behavior)
  - [sync.WaitGroup](#syncwaitgroup)
  - [sync.Mutex and sync.RWMutex](#syncmutex-and-syncrwmutex)
  - [sync.Once](#synconce)
  - [Data Races and the Race Detector](#data-races-and-the-race-detector)
  - [Deadlocks](#deadlocks)
  - [The Go Philosophy: Communication vs Sharing](#the-go-philosophy-communication-vs-sharing)
  - [Introductory Patterns](#introductory-patterns)
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

This module covers **Go's concurrency model**: goroutines, channels, `select`, and the `sync` package. Concurrency is a first-class language feature in Go, designed from day one on the principles of **Communicating Sequential Processes (CSP)**. The central idea: independent concurrent units coordinate by passing messages through channels, rather than by sharing memory and locking.

By the end of this module you will understand not only how goroutines and channels work, but why Go made the design choices it did — when channels are the right tool and when a mutex is actually better — and how to avoid the most dangerous bugs: data races and deadlocks.

Deeper patterns — `context` cancellation, pipelines, worker pools, `sync/atomic` — are in [[go/12. Advanced Concurrency Patterns]]. Runtime internals that explain why goroutines are cheap are in [[go/17. Runtime Internals and the Memory Model]].

**Difficulty:** Intermediate &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain the difference between concurrency and parallelism — _given a program, state which it needs_
2. Launch goroutines with `go`, explain the runtime scheduler at a high level, and diagnose the "main returns and kills all goroutines" gotcha
3. Create unbuffered and buffered channels, send/receive values, close channels, and use `for range` — _implement a producer/consumer pair_
4. Write `select` statements for multiplexing, non-blocking receives, and timeouts via `time.After`
5. Use `sync.WaitGroup`, `sync.Mutex`, `sync.RWMutex`, and `sync.Once` correctly
6. Identify data races with `-race` and fix them — _run `go test -race`, read the output, correct the bug_
7. Recognize deadlock conditions and explain the Go runtime's "all goroutines are asleep" message

---

## Prerequisites

### Required Modules

- [[go/8. Error Handling]] — error propagation from goroutines, `panic`/`recover` per-goroutine scope
- [[go/3. Functions]] — closures (goroutine bodies), first-class functions, multiple return values
- [[go/4. Composite Types]] — slices and maps are the most common targets of data races
- [[go/6. Methods and Interfaces]] — the mutex-embedding idiom, `sync.Locker`

### Required Concepts

- **Closures and variable capture** — the loop variable capture bug (see Common Beginner Mistakes) is impossible to avoid without solid closure fundamentals
- **Multiple return values** — goroutines communicate results via channels; understand `(value, error)` returns
- **The `error` interface** — goroutines that fail must communicate errors through channels or closures

> [!TIP]
> If closures feel shaky, spend 20–30 minutes on [[go/3. Functions]] before continuing.
> The goroutine closure-capture bug trips up experienced developers — you cannot reliably avoid it without understanding how closures work.

---

## Why This Matters

Concurrency is what makes Go the language of choice for network services and infrastructure. A web server handling one request at a time is useless; `net/http` handles each request in its own goroutine automatically.

Mastery of this module enables you to:

- **Build responsive services** — handlers that call two APIs simultaneously, query a database while logging, without blocking the whole server
- **Process data faster** — fan-out distributes work across goroutines, reducing wall-clock time proportional to available cores
- **Avoid catastrophic bugs** — data races and deadlocks are non-deterministic, cause memory corruption, and are extremely difficult to debug. Knowing how to prevent them — and how to use the race detector — is a critical professional skill

See [[concurrency]] for a cross-language comparison of concurrency models (threads, async/await, CSP, actors).

---

## Historical Context

Go's model descends from **Communicating Sequential Processes (CSP)**, published by **Tony Hoare** in 1978 — the theoretical foundation for channels. **Rob Pike** and **Ken Thompson**, two of Go's three co-designers, had decades of CSP experience: Pike implemented channels in Newsqueak (1989), Alef (1992), and Limbo (1995) for Plan 9 and Inferno at Bell Labs.

Key moments:

- **1978** — Hoare publishes CSP; the theoretical foundation
- **1989–1995** — Pike implements channels in Newsqueak, Alef, Limbo; the `go` keyword appears
- **2007** — Go design begins; CSP model chosen over Java-style thread synchronization
- **2009** — Go open-sourced; goroutines and channels present from day one
- **2012** — Go memory model published — defines exactly when goroutines are guaranteed to see writes from other goroutines

This history explains why goroutines are not pthreads (they are green threads multiplexed onto OS threads by the scheduler — see [[go/17. Runtime Internals and the Memory Model]]) and why channels exist as first-class language features rather than library types.

---

## Core Concepts

### Concurrency vs Parallelism

**Concurrency** is about *structure*: designing a program as independent tasks that can be in progress simultaneously. Works on a single core via interleaving. **Parallelism** is about *execution*: tasks literally running simultaneously on multiple CPU cores.

```
Concurrency (single core — interleaved):        Parallelism (multi-core — simultaneous):
  Goroutine A: ──────╮  ╭────────╮  ╭──────    Goroutine A: ────────────── Core 1
  Goroutine B:       ╰──╯        ╰──╯          Goroutine B: ────────────── Core 2
```

In Go: you control concurrency with `go`; the runtime scheduler decides parallelism based on `GOMAXPROCS` (defaults to number of CPU cores since Go 1.5). Spawning 100 goroutines on a 4-core machine gives at most 4-way parallelism, but all 100 goroutines are efficiently interleaved.

---

### Goroutines

A goroutine is a **lightweight, independently executing function** managed by the Go runtime — launch one with `go`:

```go
go sayHello("Alice")  // runs concurrently with caller
```

**Why goroutines are cheap:** An OS thread needs 1–8 MB of stack. A goroutine starts with ~**2 KB** and grows dynamically. The runtime multiplexes thousands of goroutines onto a small pool of OS threads (M:N scheduler). See [[go/17. Runtime Internals and the Memory Model]] for scheduler internals.

**The "main returns kills everything" gotcha:**

```go
func main() {
    go fmt.Println("I might never print!") // killed when main returns
}
```

When `main` returns, all goroutines die immediately — no waiting. Use `sync.WaitGroup` or channels to synchronize before returning.

**Goroutines and panics:** A panic in a goroutine crashes the entire program unless that goroutine recovers it. A `defer recover()` in `main` does **not** catch panics in other goroutines — each goroutine manages its own panic recovery.

---

### Channels — Unbuffered and Buffered

A channel is a **typed conduit** for goroutine communication:

```go
ch := make(chan int)       // unbuffered
ch2 := make(chan int, 10)  // buffered, capacity 10

ch <- 42    // send (blocks for unbuffered until a receiver is ready)
v := <-ch   // receive (blocks for unbuffered until a sender sends)
v, ok := <-ch // comma-ok: ok==false when channel is closed and empty
```

**Unbuffered channels** are a **rendezvous** — send and receive must happen at the same instant. Both sides block until the other is ready. This is the tightest form of synchronization.

**Buffered channels** decouple sender and receiver: sends don't block while buffer has space; receives don't block while buffer has values.

| | Unbuffered | Buffered |
|---|---|---|
| Semantics | Rendezvous — both ready at once | Async — sender can run ahead |
| Send blocks when | Always (until receiver ready) | Buffer is full |
| Receive blocks when | Always (until sender sends) | Buffer is empty |
| Best for | Signaling, guaranteeing handoff | Work queues, rate smoothing |

Start with unbuffered channels. Add buffering only when you have a concrete reason.

---

### Channel Direction Types

Function signatures can restrict a channel to send-only (`chan<-`) or receive-only (`<-chan`). This is a compile-time constraint — it makes APIs self-documenting and prevents misuse:

```go
func producer(ch chan<- int) { ch <- 42 }   // can only send
func consumer(ch <-chan int) { v := <-ch; _ = v } // can only receive

func main() {
    ch := make(chan int, 1)
    go producer(ch) // bidirectional narrowed to chan<- int
    consumer(ch)    // bidirectional narrowed to <-chan int
}
```

Convention: the goroutine that creates the channel holds `chan T`; it passes `chan<- T` to producers and `<-chan T` to consumers.

---

### Closing Channels and range

`close(ch)` signals "no more values will be sent." **Only the sender should close** — closing a closed channel panics; sending to a closed channel panics; receiving from a closed+empty channel returns zero value + `ok==false` (does not panic).

```go
func generate(ch chan<- int, n int) {
    defer close(ch) // close when done sending
    for i := 0; i < n; i++ {
        ch <- i
    }
}

func main() {
    ch := make(chan int)
    go generate(ch, 5)
    for v := range ch { // range exits when ch is closed and empty
        fmt.Println(v)
    }
}
// Output: 0 1 2 3 4
```

If multiple goroutines send to the same channel, use a `sync.WaitGroup` to coordinate a single close after all senders finish.

---

### select — Multiplexing Channels

`select` waits on **multiple channel operations** simultaneously. When one or more cases are ready, one is chosen at random (uniform pseudo-random, guaranteed by the spec):

```go
select {
case msg := <-ch1:
    fmt.Println("from ch1:", msg)
case msg := <-ch2:
    fmt.Println("from ch2:", msg)
}
```

**Non-blocking with `default`:** If no case is ready and there is a `default`, it runs immediately — `select` never blocks.

```go
select {
case v := <-ch:
    fmt.Println("got:", v)
default:
    fmt.Println("nothing ready")
}
```

**Timeouts with `time.After`:** The idiomatic timeout pattern:

```go
select {
case result := <-resultCh:
    return result, nil
case <-time.After(500 * time.Millisecond):
    return "", errors.New("timed out")
}
```

> [!NOTE]
> `time.After` creates a timer for each call; in tight loops, use `time.NewTimer` and call `timer.Stop()` to avoid timer accumulation. For single-use timeouts, `time.After` is fine.

---

### Nil Channel Behavior

A nil channel **blocks forever** on both send and receive — it never makes a `select` case ready. This is useful for disabling a `select` case dynamically:

```go
// Disable a select case by setting its channel to nil
case v, ok := <-ch1:
    if !ok {
        ch1 = nil  // case will never fire again
        continue
    }
```

This pattern is used in fan-in (merge) implementations to stop processing from a closed input channel without restructuring the select.

---

### sync.WaitGroup

`sync.WaitGroup` is the idiomatic way to wait for a collection of goroutines to finish:

```go
var wg sync.WaitGroup

for i := 1; i <= 5; i++ {
    wg.Add(1)          // increment BEFORE launching
    go func(id int) {
        defer wg.Done() // decrement when done; via defer so it runs on panic
        fmt.Println("worker", id)
    }(i)
}

wg.Wait() // block until counter reaches 0
```

**Critical rules:**
1. `Add(n)` must be called in the **parent goroutine, before launch** — never inside the goroutine body
2. `Done()` must be called via `defer` — it runs even on early return or panic
3. **Never copy a WaitGroup** — always pass a pointer (`*sync.WaitGroup`)
4. Counter must never go negative — more `Done()` calls than `Add()` panics

---

### sync.Mutex and sync.RWMutex

A **mutex** ensures only one goroutine accesses shared data at a time:

```go
type SafeCounter struct {
    mu sync.Mutex
    v  map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock() // always unlock via defer to prevent leaking on early return
    c.v[key]++
}
```

**`sync.RWMutex`** allows multiple concurrent readers but only one writer — ideal for read-heavy shared data like caches:

```go
c.mu.RLock()         // many goroutines can hold RLock simultaneously
defer c.mu.RUnlock()
return c.items[key]
```

Use `RWMutex` when reads vastly outnumber writes. For frequent writes, a plain `Mutex` is simpler and often faster.

**Mutex-embedding idiom:** Embed the mutex directly in the struct it protects so callers use `s.Lock()` / `s.Unlock()`:

```go
type State struct {
    sync.Mutex
    data map[string]int
}
```

---

### sync.Once

`sync.Once` ensures a function runs exactly once, regardless of how many goroutines call it — the idiomatic lazy initialization pattern:

```go
var (
    instance *Config
    once     sync.Once
)

func getConfig() *Config {
    once.Do(func() {
        instance = &Config{DSN: "postgres://localhost/db"} // runs once
    })
    return instance // all callers get the same instance
}
```

All goroutines that call `once.Do` before the function completes block until it finishes; subsequent calls are no-ops. If the function panics, `once` is considered done — subsequent `Do` calls are no-ops.

---

### Data Races and the Race Detector

A **data race** occurs when two goroutines access the same memory location concurrently, at least one is a write, and there is no synchronization between them. Data races are undefined behavior in Go's memory model — results are unpredictable.

**A concrete race:**

```go
counter := 0
// 1000 goroutines all do: counter++
// counter++ compiles to: read → add 1 → write
// Two goroutines may read the same value; one increment is lost
fmt.Println(counter) // may not be 1000
```

**The `-race` flag** instruments memory accesses and reports races at runtime:

```bash
go run -race main.go
go test -race ./...
```

**Sample race report:**
```
WARNING: DATA RACE
Write at 0x00c0000b4010 by goroutine 7:
  main.main.func1()  main.go:13

Previous write at 0x00c0000b4010 by goroutine 6:
  main.main.func1()  main.go:13
```

The detector reports races it **observes** — it does not prove absence of races. Run `-race` in CI on all tests.

**Fix options:** `sync.Mutex` (for any data type) or `sync/atomic` (for simple integers/pointers):

```go
// Mutex fix
mu.Lock(); counter++; mu.Unlock()

// Atomic fix (counter must be int64)
atomic.AddInt64(&counter, 1)
```

---

### Deadlocks

A **deadlock** occurs when all goroutines are blocked and none can proceed. The Go runtime detects this and terminates with:

```
fatal error: all goroutines are asleep - deadlock!
```

**Common deadlock patterns:**

```go
// 1. Sending on unbuffered channel with no receiver
ch := make(chan int)
ch <- 1 // blocks forever — no goroutine receives

// 2. Missing close — range never exits
ch := make(chan int, 3)
ch <- 10; ch <- 20; ch <- 30
for v := range ch { fmt.Println(v) } // blocks after reading 3 values

// 3. Non-reentrant mutex — same goroutine locks twice
mu.Lock()
mu.Lock() // deadlock: waiting for itself to unlock (Go's Mutex is NOT reentrant)
```

**Prevention rules:**
1. Close channels when done sending
2. Acquire multiple mutexes in a **consistent order** everywhere
3. Never hold a lock when calling code you don't control
4. `defer mu.Unlock()` immediately after `mu.Lock()` to prevent leaked locks

> [!WARNING]
> The runtime deadlock detector fires only when **all** goroutines are blocked. If your program has any unblocked background goroutine (a timer, HTTP server), a partial deadlock in your application goroutines will not be detected automatically.

---

### The Go Philosophy: Communication vs Sharing

> **"Do not communicate by sharing memory; share memory by communicating."**

The traditional model starts with shared memory and adds locks. Go's model starts with independent goroutines and passes data between them via channels — only one goroutine "owns" the data at any time, eliminating the class of bugs from unsynchronized access.

**But mutexes have their place.** The proverb is a guideline, not a rule:

| Use channels when | Use a mutex when |
|---|---|
| Data flows naturally from one goroutine to another | Many goroutines need concurrent access to the same structure |
| Signaling events or coordinating goroutine lifecycle | Protecting a shared cache with many readers (`RWMutex`) |
| Building pipelines and generators | Simple counter incremented frequently (prefer `sync/atomic`) |

Rob Pike: *"Use whichever is most expressive and correct for your problem."*

---

### Introductory Patterns

Two patterns appear throughout Go code. Deeper treatment — `context`, bounded worker pools, error propagation — is in [[go/12. Advanced Concurrency Patterns]].

**Generator** — returns a `<-chan T` and sends values from an internal goroutine:

```go
func fibonacci(n int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        a, b := 0, 1
        for i := 0; i < n; i++ {
            ch <- a
            a, b = b, a+b
        }
    }()
    return ch // receive-only — caller cannot send or close
}

// Usage
for v := range fibonacci(10) {
    fmt.Print(v, " ") // 0 1 1 2 3 5 8 13 21 34
}
```

**Fan-out / fan-in** — distribute work across N goroutines, collect results on one channel:

```go
func fanOut(jobs <-chan int, n int) <-chan int {
    results := make(chan int, n)
    var wg sync.WaitGroup
    for w := 0; w < n; w++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := range jobs {
                results <- j * j // process job
            }
        }()
    }
    go func() { wg.Wait(); close(results) }()
    return results
}
// Output order of results is nondeterministic
```

---

### How the Concepts Fit Together

```
goroutines (go keyword)
       │
       │  communicate via
       ▼
   channels (unbuffered / buffered)
       │
       │  multiplex with
       ▼
    select (+ default / time.After)
       │
       │  when shared state is unavoidable
       ▼
   sync package (WaitGroup / Mutex / RWMutex / Once)
       │
       │  verify with
       ▼
  -race detector
       │
       ▼
  Patterns: generator, fan-out/fan-in
  (deeper: [[go/12. Advanced Concurrency Patterns]])
```

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Loop variable capture**
>
> All goroutines launched in a loop share the same loop variable. By the time they run, the loop is done and the variable holds its final value.
>
> **Wrong:**
> ```go
> for i := 0; i < 5; i++ {
>     go func() { fmt.Println(i) }() // all goroutines share same i
> }
> // Likely prints: 5 5 5 5 5
> ```
>
> **Right:**
> ```go
> for i := 0; i < 5; i++ {
>     go func(id int) { fmt.Println(id) }(i) // i copied into id at launch
> }
> // Prints 0 1 2 3 4 in some order
> ```
>
> **Why this matters:** Silent, timing-dependent bug that manifests more reliably under load.

> [!WARNING]
> **Mistake 2: Sending to or closing a closed channel**
>
> Both panic at runtime. Only the sender should close; only close once.
>
> ```go
> close(ch); ch <- 1   // panic: send on closed channel
> close(ch); close(ch) // panic: close of closed channel
> ```
>
> **Fix:** If multiple goroutines send, use a `sync.WaitGroup` to let a single goroutine close after all senders finish.

> [!WARNING]
> **Mistake 3: WaitGroup.Add inside the goroutine body**
>
> `wg.Wait()` in the parent may return before the goroutine calls `wg.Add(1)`.
>
> **Wrong:** `go func() { wg.Add(1); defer wg.Done(); ... }()`
> **Right:** `wg.Add(1); go func() { defer wg.Done(); ... }()`

> [!WARNING]
> **Mistake 4: Goroutine leak**
>
> A goroutine blocked on a channel that will never receive leaks for the program's lifetime.
>
> ```go
> ch := make(chan int)
> go func() { v := <-ch; fmt.Println(v) }() // nobody sends — goroutine leaks
> ```
>
> **Prevention:** Design goroutine lifetimes explicitly. Use `context` cancellation (see [[go/12. Advanced Concurrency Patterns]]). Use `goleak` in tests.

**Other pitfalls:**

- **Copying sync types** — `sync.Mutex`, `sync.WaitGroup`, `sync.Once` must never be copied after first use; always use pointers or embed in structs accessed by pointer
- **`time.Sleep` as synchronization** — never correct in production; use channels or WaitGroup

---

## Mental Models

### Mental Model 1: Goroutines as Postal Workers

Each goroutine is a postal worker. Workers don't share a sorting table — they communicate by passing parcels (data) through delivery slots (channels). An unbuffered slot is a direct handoff — both worker and recipient must be present. A buffered slot has a storage bin — the worker drops off parcels without waiting.

`select` is a worker waiting at multiple slots, taking from whichever one has a parcel first. Closing a channel is turning off the parcel source — the recipient gets all remaining parcels, then knows the source is done.

This model breaks down for mutex patterns (shared table), where the mutex is the lock on the sorting table.

### Mental Model 2: Channels as Pipes with Tanks

An unbuffered channel is a direct pipe — sender fills it at exactly the rate receiver empties it. A buffered channel has a tank in the middle — the sender fills ahead as long as the tank is not full; the receiver drains independently. Backpressure: a slow receiver fills the tank and eventually stalls the sender.

Most useful for reasoning about buffering trade-offs and whether producers will outpace consumers.

### Mental Model 3: The Race Detector as a Code Inspector

The race detector instruments every memory access and flags when two goroutines touch the same address without showing synchronization credentials (a lock or channel operation). It can only report races that actually occur during a run — races that require unlucky timing may escape detection in tests.

This explains why `-race` must be run in CI with many test iterations, not just locally, and why stress tests are valuable.

> [!NOTE]
> Use Model 1 (postal workers) when designing goroutine communication topology. Use Model 2 (pipes) when reasoning about buffering and backpressure. Use Model 3 (inspector) when debugging data races.

---

## Practical Examples

### Example 1: WaitGroup to Wait for Goroutines _(Basic)_

**Scenario:** Launch goroutines to do independent work; wait for all before proceeding.

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func simulate(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    time.Sleep(time.Duration(id) * time.Millisecond)
    fmt.Printf("Task %d complete\n", id)
}

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 5; i++ {
        wg.Add(1)
        go simulate(i, &wg)
    }
    wg.Wait()
    fmt.Println("All tasks complete")
}
// Output: tasks complete in id-order (due to sleep), then "All tasks complete" last
```

**What to notice:** `wg.Add(1)` in the loop (parent goroutine), not inside `simulate`. `wg.Done()` via `defer` — runs even on panic. WaitGroup passed as `*sync.WaitGroup` — never copy.

---

### Example 2: Pipeline with Channels _(Intermediate)_

**Scenario:** Three-stage pipeline: generate → square → print.

```go
package main

import "fmt"

func generate(n int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 1; i <= n; i++ { ch <- i }
    }()
    return ch
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for v := range in { out <- v * v }
    }()
    return out
}

func main() {
    for v := range square(generate(5)) {
        fmt.Println(v) // 1, 4, 9, 16, 25
    }
}
```

**What to notice:** Each stage returns a `<-chan int`. Closing propagates down the pipeline automatically — when `generate` closes, `square`'s range exits and closes `out`, which ends the final range in `main`. No explicit synchronization needed beyond the channel sends/receives.

---

### Example 3: select with Timeout _(Applied)_

**Scenario:** Abandon a slow operation if it takes too long.

```go
package main

import (
    "errors"
    "fmt"
    "time"
)

func withTimeout(timeout time.Duration) (string, error) {
    resultCh := make(chan string, 1) // buffered — prevents goroutine leak on timeout
    go func() {
        time.Sleep(200 * time.Millisecond) // simulate slow work
        resultCh <- "result"
    }()

    select {
    case result := <-resultCh:
        return result, nil
    case <-time.After(timeout):
        return "", errors.New("timed out")
    }
}

func main() {
    r, err := withTimeout(100 * time.Millisecond)
    fmt.Println(r, err) // "" timed out

    r, err = withTimeout(500 * time.Millisecond)
    fmt.Println(r, err) // result <nil>
}
```

**What to notice:** `resultCh` has capacity 1. Even after the timeout fires and `withTimeout` returns, the goroutine will eventually send on `resultCh`. The buffer lets it complete without blocking — preventing a goroutine leak.

---

### Example 4: Detecting a Data Race _(Edge Case)_

**Scenario:** Concurrent `append` to a shared slice — a race that looks correct but isn't.

```go
// BROKEN — run with go run -race to see the report
var results []int
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(v int) {
        defer wg.Done()
        results = append(results, v) // RACE: concurrent read-modify-write of results
    }(i)
}
wg.Wait()
fmt.Println(len(results)) // may be less than 10 — appends lost
```

**Fixed with mutex:**

```go
var mu sync.Mutex
go func(v int) {
    defer wg.Done()
    mu.Lock()
    results = append(results, v) // safe — serialized
    mu.Unlock()
}(i)
// len(results) is always 10; order is nondeterministic
```

**What to notice:** The race detector reports the exact lines where concurrent accesses occur. After the fix, `len(results)` is always 10, but the order varies — the mutex ensures safety (no corruption), not ordering. For ordered results, use a pre-allocated slice indexed by goroutine ID, or a channel.

---

## Related Concepts

Within this topic:

- [[go/8. Error Handling]] — goroutines cannot return errors; propagating errors from concurrent code requires channels or closures, building on error handling fundamentals
- [[go/12. Advanced Concurrency Patterns]] — `context` for cancellation, bounded worker pools, pipelines with error propagation, `sync/atomic`; this module is the prerequisite
- [[go/17. Runtime Internals and the Memory Model]] — the Go scheduler (M:N model, GOMAXPROCS, preemption in Go 1.14+), the Go memory model, and formal "happens before" guarantees for channel operations

In other topics:

- [[concurrency]] — cross-language comparison: Python threading/asyncio, Rust ownership-based concurrency, JavaScript event loop, actor model; shows where Go's CSP model fits in the broader landscape

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Goroutine Greeting Race** _(Easy)_
>
> Launch five goroutines that each print a greeting. Observe nondeterministic output. Then add a `sync.WaitGroup` so `main` waits for all goroutines before exiting.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-goroutine-greeting-race--easy--1-pt)

The exercises progress from goroutine basics to data race diagnosis and fan-out implementation. Complete at least the Easy and Medium exercises before taking the test.

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
Concurrent URL Fetcher — fetch a list of URLs concurrently, collect response status codes and body lengths, add a per-fetch timeout using `select` + `time.After`, use `sync.WaitGroup` to know when all fetches finish. Run `go test -race` on any shared state. This exercises every major concept in the module.

---

## Further Reading

1. **[Share Memory By Communicating — The Go Blog](https://go.dev/blog/codelab-share)** — The canonical explanation of Go's CSP philosophy; uses a concurrent poller as a worked example; essential reading

2. **[Go Concurrency Patterns: Pipelines and Cancellation — The Go Blog](https://go.dev/blog/pipelines)** — Sameer Ajmani; covers generator, pipeline, fan-out/fan-in with complete code; prerequisite for [[go/12. Advanced Concurrency Patterns]]

3. **[A Tour of Go — Concurrency](https://go.dev/tour/concurrency/1)** — Interactive tour pages concurrency/1–11; goroutines, channels, buffered channels, range/close, select, sync.Mutex; editable examples in browser

4. **"The Go Programming Language" — Donovan & Kernighan, Chapters 8–9** — Ch. 8: goroutines, channels, pipelines, select, cancellation; Ch. 9: race conditions, sync package, GOMAXPROCS; the standard textbook treatment

5. **"Learning Go" — Jon Bodner (2nd ed.), Chapter 10** — Concurrency in Go; explicit guidance on channels vs mutexes; current idioms

6. **[pkg.go.dev/sync](https://pkg.go.dev/sync)** — Official documentation for `sync.WaitGroup`, `Mutex`, `RWMutex`, `Once`, `Map`; read before using each type in production

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 9

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
