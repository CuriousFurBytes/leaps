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

This module covers **Go's concurrency model**: goroutines, channels, `select`, and the synchronization primitives in the `sync` package. Concurrency is not an afterthought in Go — it is a first-class language feature, designed from day one as the mechanism by which Go programs handle multiple simultaneous tasks.

Go's model descends from **Communicating Sequential Processes (CSP)**, a formal theory of concurrency developed by Tony Hoare. The central idea is that independent concurrent processes coordinate by passing messages through channels, rather than by writing to shared memory and hoping for the best. This is captured in the famous Go proverb: *"Do not communicate by sharing memory; share memory by communicating."*

By the end of this module you will understand not only how goroutines and channels work, but why Go made the design decisions it did, when channels are the right tool and when a mutex is better, and how to avoid the most dangerous concurrent bugs — data races and deadlocks.

This module is a solid foundation. Deeper patterns — `context` cancellation, pipelines, worker pools, and `sync/atomic` — are covered in [[go/12. Advanced Concurrency Patterns]]. The runtime scheduler that makes goroutines efficient is explained in [[go/17. Runtime Internals and the Memory Model]].

**Difficulty:** Intermediate &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain the difference between concurrency and parallelism, and identify which Go programs exhibit each — _given a program description, state whether it needs concurrency, parallelism, or both_
2. Launch goroutines with `go`, understand their relationship to OS threads, and explain the "main returns and kills all goroutines" gotcha — _diagnose why a program exits before goroutines finish_
3. Create unbuffered and buffered channels, send and receive values, close channels correctly, and iterate with `range` — _implement a producer/consumer pair using a channel_
4. Write `select` statements for multiplexing channels, implementing non-blocking receives, and setting timeouts — _add a timeout to a blocking operation using `select` and `time.After`_
5. Use `sync.WaitGroup`, `sync.Mutex`, `sync.RWMutex`, and `sync.Once` correctly — _protect a shared counter from data races using a mutex_
6. Identify data races using the `-race` detector and fix them — _given racy code, run `go test -race`, read the output, and correct the bug_
7. Recognize deadlock conditions and explain what the Go runtime's "all goroutines are asleep" message means — _read a deadlocked program and identify which goroutines are stuck and why_

---

## Prerequisites

### Required Modules

- [[go/8. Error Handling]] — you need to understand: returning errors from functions, wrapping errors with `fmt.Errorf`, and `panic`/`recover`, because concurrent code multiplies error-handling complexity and goroutines have their own panic scope
- [[go/3. Functions]] — you need to understand: closures (goroutines are almost always written as closures), multiple return values, and function values as first-class citizens
- [[go/4. Composite Types]] — you need to understand: slices and maps, because concurrent access to these is one of the most common sources of data races in real Go programs
- [[go/6. Methods and Interfaces]] — you need to understand: how the `sync.Locker` interface works and how embedding structs enables the mutex-embedding idiom

### Required Concepts

- **Closures and variable capture** — goroutine bodies are closures; misunderstanding how closures capture loop variables is one of the most common goroutine bugs (see Common Beginner Mistakes)
- **Multiple return values** — goroutines cannot return values directly; the pattern for communicating results back is through channels or closures that write to outer variables
- **The `error` interface** — goroutines that fail need to communicate their errors somehow; understanding `error` is necessary before designing concurrent error handling

> [!TIP]
> If closures feel shaky, spend 20–30 minutes reviewing [[go/3. Functions]] before continuing.
> The goroutine closure-capture bug (the loop variable capture mistake) trips up even experienced developers; you cannot reliably avoid it without a solid understanding of how closures work.

---

## Why This Matters

Concurrency is the feature that makes Go the language of choice for network services, distributed systems, and infrastructure tooling. A web server that handles one request at a time would be useless. A tool that fetches ten URLs sequentially when it could fetch them concurrently wastes orders of magnitude of time. Understanding Go's concurrency model is not optional for professional Go development.

Concretely, mastery of this module enables you to:

- **Build responsive network services** — Go's `net/http` server handles each request in its own goroutine automatically. Understanding goroutines lets you write handlers that do concurrent work (call two APIs simultaneously, query the database while logging asynchronously) without blocking the whole server.
- **Process data faster** — fan-out patterns let you split a workload across multiple goroutines and collect results through a channel, reducing wall-clock time proportionally to available CPU cores for CPU-bound work, or even more dramatically for I/O-bound work.
- **Avoid catastrophic bugs** — data races and deadlocks are the most dangerous classes of concurrent bugs. They are non-deterministic (they may not manifest in tests), they can cause memory corruption, and they are extremely difficult to debug after the fact. Knowing how to prevent them — and how to use the race detector to catch them — is a critical professional skill.

Without understanding Go's concurrency primitives, you would be writing sequential programs in a language specifically designed for concurrency — and you would be unable to read or maintain the concurrent code that exists in essentially every non-trivial Go codebase.

See also: [[concurrency]] for a cross-language comparison of concurrency models.

---

## Historical Context

Go's concurrency model is rooted in **Communicating Sequential Processes (CSP)**, a mathematical framework for describing concurrent systems developed by **Tony Hoare** and published in 1978 in a landmark paper in the Communications of the ACM. Hoare proposed that the safest way to build concurrent systems was not to share memory and use locks, but to have independent processes that communicate by passing messages through synchronized channels.

**Rob Pike** and **Ken Thompson**, two of Go's three co-designers, had worked extensively on CSP-inspired systems before Go. Pike implemented channels in the **Squeak** and **Newsqueak** languages in the late 1980s at Bell Labs, and later in **Alef** and **Limbo** (for the Plan 9 and Inferno operating systems). By the time Go was being designed in 2007, the team had decades of experience with CSP and knew exactly what they wanted.

Key moments in the development of Go's concurrency:

- **1978** — Tony Hoare publishes "Communicating Sequential Processes" — the theoretical foundation for Go channels
- **1989** — Rob Pike implements channels in Newsqueak; the `go` keyword appears in Alef (1992) and Limbo (1995)
- **2007** — Go design begins; Hoare's CSP model is chosen explicitly over Java-style thread synchronization
- **2009** — Go open-sourced; goroutines and channels are in the language from day one
- **2012** — Go 1.0; the memory model specification is published, defining exactly when goroutines are guaranteed to see writes from other goroutines
- **2014** — `context` package added (later moved into stdlib in Go 1.7), enabling structured goroutine cancellation — covered in [[go/12. Advanced Concurrency Patterns]]

Understanding this history explains why Go's model looks the way it does. Goroutines are not pthreads — they are green threads multiplexed onto OS threads by the Go scheduler (details in [[go/17. Runtime Internals and the Memory Model]]). Channels are not queues — they are synchronization points. The `sync` package exists not because locking is preferred, but because some problems genuinely require shared state.

---

## Core Concepts

### Concurrency vs Parallelism

These two terms are often used interchangeably but mean different things — and the distinction matters for understanding when and why to use goroutines.

**Concurrency** is about *structure*: designing a program as a collection of independent tasks that can be in progress at the same time. A single-core machine can run a concurrent program — it interleaves tasks by rapidly switching between them (time-slicing). The tasks do not actually run at the same time, but the program is structured as if they could.

**Parallelism** is about *execution*: tasks literally running at the same time on multiple CPU cores. Parallelism requires multiple processors. A parallel program is always concurrent, but a concurrent program is not necessarily parallel.

```
Concurrency (structure — single core):
  Goroutine A: ──────╮  ╭────────╮  ╭──────────
  Goroutine B:       ╰──╯        ╰──╯
  (interleaved — only one runs at a time)

Parallelism (execution — multiple cores):
  Goroutine A: ────────────── Core 1
  Goroutine B: ────────────── Core 2
  (truly simultaneous)
```

In Go:

- You control **concurrency** by launching goroutines with `go`.
- The Go **runtime scheduler** decides whether and how to achieve **parallelism**, based on the value of `GOMAXPROCS` (defaults to the number of available CPU cores since Go 1.5).

This means: just because you spawn 100 goroutines does not guarantee 100-way parallelism. On a 4-core machine with `GOMAXPROCS=4`, at most 4 goroutines run simultaneously. But those 4 goroutines can serve as "threads of execution" that interleave all 100 goroutines efficiently.

See [[concurrency]] for a broader comparison of concurrency models across languages.

---

### Goroutines

A goroutine is a **lightweight, independently executing function** managed by the Go runtime. You launch one with the `go` keyword:

```go
package main

import (
    "fmt"
    "time"
)

func sayHello(name string) {
    fmt.Printf("Hello, %s!\n", name)
}

func main() {
    go sayHello("Alice")  // launch as a goroutine — runs concurrently with main
    go sayHello("Bob")
    time.Sleep(10 * time.Millisecond) // give goroutines time to run
    fmt.Println("main done")
}
// Output order of the two hellos is nondeterministic — either may print first
```

**Why goroutines are cheap:** An OS thread typically requires 1–8 MB of stack space at creation. A goroutine starts with around **2 KB** of stack and grows dynamically as needed. The Go runtime can comfortably manage tens of thousands of goroutines in a single process — something utterly impractical with OS threads. This is possible because goroutines are multiplexed onto a small pool of OS threads by the Go scheduler (the M:N threading model). See [[go/17. Runtime Internals and the Memory Model]] for the scheduler internals.

**The "main returns and kills everything" gotcha:** When `main` returns, the entire Go program terminates immediately — all goroutines, even those that are still running, are killed without ceremony. There is no automatic waiting. This is one of the most common first mistakes:

```go
func main() {
    go fmt.Println("I might never print!")
    // main returns here — goroutine is killed before it runs
}
```

The solutions are:
1. Use `sync.WaitGroup` to wait for goroutines to finish (see below)
2. Use a channel to synchronize with the goroutines
3. Use `time.Sleep` (acceptable in tests/demos, not production)

**Goroutines and panics:** A panic in a goroutine will crash the entire program if not recovered. The key rule: **each goroutine must recover its own panics** — a `defer recover()` in `main` will not catch panics in other goroutines.

```go
func riskyWork() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("goroutine recovered:", r)
        }
    }()
    panic("something went wrong")
}

func main() {
    go riskyWork()
    time.Sleep(10 * time.Millisecond)
    fmt.Println("main continues")
}
```

---

### Channels — Unbuffered and Buffered

A channel is a **typed conduit** through which goroutines can send and receive values. Channels are Go's primary concurrency primitive for communication.

```go
// Create a channel of int
ch := make(chan int)        // unbuffered
ch2 := make(chan int, 10)   // buffered with capacity 10

// Send a value (blocks until receiver is ready for unbuffered)
ch <- 42

// Receive a value (blocks until sender sends for unbuffered)
v := <-ch

// Receive and discard
<-ch
```

**Unbuffered channels (capacity 0):** A send on an unbuffered channel **blocks** until another goroutine receives, and a receive blocks until another goroutine sends. This is a **rendezvous** — both the sender and receiver must be ready at the same time. Unbuffered channels are the tightest form of synchronization: they guarantee that the send and receive happen at the same instant in time.

```go
package main

import "fmt"

func main() {
    ch := make(chan string) // unbuffered

    go func() {
        // This goroutine blocks here until main receives
        ch <- "ping"
        fmt.Println("sent ping") // runs only after main has received
    }()

    msg := <-ch               // blocks until goroutine sends
    fmt.Println("received:", msg)
    // Output:
    // received: ping
    // sent ping
    // (both always in this order — send completes only when receive happens)
}
```

**Buffered channels (capacity N):** A send on a buffered channel succeeds without blocking as long as the buffer is not full. A receive succeeds without blocking as long as the buffer is not empty. The buffer decouples the sender and receiver — they no longer need to synchronize at the exact same moment.

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 3) // buffer of 3

    // These sends don't block — there's room in the buffer
    ch <- 1
    ch <- 2
    ch <- 3
    // ch <- 4  // this would block — buffer is full

    fmt.Println(<-ch) // 1
    fmt.Println(<-ch) // 2
    fmt.Println(<-ch) // 3
    // fmt.Println(<-ch) // this would block — buffer is empty
}
```

**When to use unbuffered vs buffered:**

| | Unbuffered | Buffered |
|---|---|---|
| **Semantics** | Rendezvous (both ready at once) | Async (sender can be ahead) |
| **Best for** | Signaling events, guaranteeing handoff, pipelines | Rate smoothing, absorbing bursts, work queues |
| **Blocking** | Always blocks sender until receiver ready | Only blocks when full (send) or empty (receive) |
| **Deadlock risk** | Higher — both sides must be active | Lower — but still possible if buffer fills |

A useful rule of thumb: start with unbuffered channels. Add buffering only when you have a concrete reason (e.g., a benchmark shows contention, or you know the producer will always be ahead of the consumer by exactly N items).

---

### Channel Direction Types

In function signatures, channels can be typed with a **direction** — send-only (`chan<-`) or receive-only (`<-chan`). This is a compile-time restriction that makes APIs self-documenting and prevents misuse:

```go
// chan<- T: can only send, not receive
func producer(ch chan<- int) {
    for i := 0; i < 5; i++ {
        ch <- i // OK: sending
    }
    close(ch)
    // v := <-ch  // compile error: receive from send-only channel
}

// <-chan T: can only receive, not send
func consumer(ch <-chan int) {
    for v := range ch {
        fmt.Println(v)
    }
    // ch <- 99  // compile error: send to receive-only channel
}

func main() {
    ch := make(chan int, 5) // bidirectional chan int
    go producer(ch)         // bidirectional ch is implicitly narrowed to chan<- int
    consumer(ch)            // bidirectional ch is implicitly narrowed to <-chan int
}
```

A bidirectional `chan T` can be passed where `chan<- T` or `<-chan T` is expected — the compiler narrows the type. Direction types are not about ownership; they are a convention enforced by the type system. The standard convention is: **the goroutine that creates a channel owns the full `chan T`; it passes `chan<- T` to producers and `<-chan T` to consumers.**

---

### Closing Channels and range

A channel can be closed with `close(ch)`. Closing signals receivers that no more values will be sent. **Only the sender should close a channel** — closing a channel that a receiver shares would be safe, but closing a closed channel panics, and sending to a closed channel panics.

```go
// Comma-ok receive — detects whether the channel is closed
v, ok := <-ch
// ok == true:  v holds the received value
// ok == false: channel is closed and empty; v is the zero value
```

**`range` over a channel** is idiomatic and handles the close automatically:

```go
package main

import "fmt"

func generate(ch chan<- int, n int) {
    for i := 0; i < n; i++ {
        ch <- i
    }
    close(ch) // receiver's range loop will end when channel is closed
}

func main() {
    ch := make(chan int, 5)
    go generate(ch, 5)

    for v := range ch { // iterates until ch is closed and empty
        fmt.Println(v)
    }
    fmt.Println("done")
}
// Output:
// 0
// 1
// 2
// 3
// 4
// done
```

**Rules for closing channels:**

1. Close a channel only from the **sender side** (the goroutine that owns the channel and sends to it).
2. Never close a channel you might also be receiving from in the same goroutine (that's a design smell).
3. Never close a channel twice — it panics.
4. Sending to a closed channel panics.
5. Receiving from a closed (and empty) channel returns the zero value and `ok == false` — it does **not** panic.
6. If multiple goroutines send to the same channel, use a `sync.WaitGroup` to close after all senders finish (see the fan-in pattern below).

---

### select — Multiplexing Channels

`select` allows a goroutine to wait on **multiple channel operations simultaneously**. It is the channel equivalent of Unix's `select` system call. When `select` runs, it checks all cases; if one or more are ready, it picks one at random (fair selection). If none are ready, it blocks until one becomes ready.

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(1 * time.Millisecond)
        ch1 <- "one"
    }()
    go func() {
        time.Sleep(2 * time.Millisecond)
        ch2 <- "two"
    }()

    for i := 0; i < 2; i++ {
        select {
        case msg := <-ch1:
            fmt.Println("Received from ch1:", msg)
        case msg := <-ch2:
            fmt.Println("Received from ch2:", msg)
        }
    }
}
// Output (deterministic here because of the sleep difference):
// Received from ch1: one
// Received from ch2: two
```

**Non-blocking operations with `default`:** If a `select` includes a `default` case, it never blocks — if no channel is ready, the `default` runs immediately:

```go
select {
case v := <-ch:
    fmt.Println("received:", v)
default:
    fmt.Println("no value ready — non-blocking")
}
```

**Timeouts with `time.After`:** `time.After(d)` returns a `<-chan time.Time` that receives a value after duration `d`. Combined with `select`, this is the standard way to implement timeouts on channel operations:

```go
func fetchWithTimeout(ch <-chan string) (string, error) {
    select {
    case result := <-ch:
        return result, nil
    case <-time.After(500 * time.Millisecond):
        return "", fmt.Errorf("operation timed out")
    }
}
```

> [!NOTE]
> `time.After` creates a timer and a channel for each call; if called in a tight loop, the timers accumulate until GC collects them. For tight loops, use `time.NewTimer` and call `timer.Stop()` explicitly. For most uses (one `select` per operation), `time.After` is fine.

**When multiple cases are ready:** If multiple channels in a `select` are ready simultaneously, Go picks one **at random** (uniformly). This is intentional — it prevents starvation and makes select fair by default. Do not rely on any particular ordering.

---

### Nil Channel Behavior

A nil channel (the zero value of any channel type) blocks forever on both send and receive — it never makes a case in a `select` ready. This is a useful property for dynamically disabling a `select` case:

```go
var ch1, ch2 <-chan int
// ... ch1 and/or ch2 might be set or left nil

select {
case v := <-ch1: // never ready if ch1 is nil
    fmt.Println("ch1:", v)
case v := <-ch2: // never ready if ch2 is nil
    fmt.Println("ch2:", v)
}
// If both are nil: blocks forever (deadlock if nothing else can unblock it)
```

**Pattern — disabling a case in select:**

```go
// Turn off a case by setting the channel to nil
func merge(ch1, ch2 <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for ch1 != nil || ch2 != nil {
            select {
            case v, ok := <-ch1:
                if !ok {
                    ch1 = nil // disable this case — ch1 is done
                    continue
                }
                out <- v
            case v, ok := <-ch2:
                if !ok {
                    ch2 = nil // disable this case — ch2 is done
                    continue
                }
                out <- v
            }
        }
    }()
    return out
}
```

Assigning `nil` to the channel variable inside `select` is the cleanest way to disable a `select` case once the channel closes. Without this technique, a closed channel's case would fire continuously with zero values and `ok == false`.

---

### sync.WaitGroup

`sync.WaitGroup` is the idiomatic way to wait for a collection of goroutines to finish. Think of it as a counter that blocks until it reaches zero.

```go
package main

import (
    "fmt"
    "sync"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done() // decrement counter when this goroutine returns
    fmt.Printf("Worker %d starting\n", id)
    // ... do work ...
    fmt.Printf("Worker %d done\n", id)
}

func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 5; i++ {
        wg.Add(1)        // increment before launching goroutine
        go worker(i, &wg) // pass pointer — WaitGroup must not be copied
    }

    wg.Wait() // block until counter reaches 0
    fmt.Println("All workers done")
}
// Output: all workers print start/done messages (order is nondeterministic),
// then "All workers done" always prints last
```

**Critical rules for WaitGroup:**

1. Call `wg.Add(n)` **before** launching the goroutine — never inside it. If the goroutine calls `Add` and the calling goroutine calls `Wait` before `Add` runs, the wait completes prematurely.
2. Call `wg.Done()` via `defer` at the top of the goroutine — this ensures it runs even if the goroutine panics or returns early.
3. **Never copy a WaitGroup** — always pass a pointer (`*sync.WaitGroup`). Copying a WaitGroup that has been used produces undefined behavior.
4. The WaitGroup counter must never go negative — calling `Done` more times than `Add` panics.

---

### sync.Mutex and sync.RWMutex

A **mutex** (mutual exclusion lock) protects shared data by ensuring only one goroutine accesses it at a time. When a goroutine locks a mutex, any other goroutine that tries to lock it blocks until the mutex is unlocked.

```go
package main

import (
    "fmt"
    "sync"
)

type SafeCounter struct {
    mu sync.Mutex
    v  map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock() // always unlock via defer to prevent deadlock on early return
    c.v[key]++
}

func (c *SafeCounter) Value(key string) int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.v[key]
}

func main() {
    c := SafeCounter{v: make(map[string]int)}
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            c.Inc("somekey")
        }()
    }

    wg.Wait()
    fmt.Println(c.Value("somekey")) // always 1000 — no data race
}
```

**sync.RWMutex** distinguishes between read and write locks, enabling multiple concurrent readers:

```go
type Cache struct {
    mu    sync.RWMutex
    items map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()         // multiple goroutines can hold RLock simultaneously
    defer c.mu.RUnlock()
    v, ok := c.items[key]
    return v, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()         // exclusive — blocks all other readers and writers
    defer c.mu.Unlock()
    c.items[key] = value
}
```

**RWMutex vs Mutex trade-offs:**

- Use `sync.Mutex` for any shared state where reads and writes are similarly frequent.
- Use `sync.RWMutex` when reads are much more frequent than writes (e.g., a configuration cache read thousands of times per second and updated once per minute).
- Do not use `RWMutex` when writes are frequent — the bookkeeping overhead of managing readers and writers can make it slower than a plain `Mutex`.

**The mutex-embedding idiom:** Embed the mutex directly in the struct it protects:

```go
type State struct {
    sync.Mutex       // embedded — State.Lock() and State.Unlock() are promoted
    data map[string]int
}

s := &State{data: make(map[string]int)}
s.Lock()
s.data["key"] = 42
s.Unlock()
```

---

### sync.Once

`sync.Once` ensures a function is called exactly once, regardless of how many goroutines attempt it. This is the idiomatic way to implement lazy initialization of shared state:

```go
package main

import (
    "fmt"
    "sync"
)

var (
    instance *Config
    once     sync.Once
)

type Config struct {
    DSN string
}

func getConfig() *Config {
    once.Do(func() {
        // This runs exactly once, even with 1000 concurrent calls
        fmt.Println("initializing config")
        instance = &Config{DSN: "postgres://localhost/db"}
    })
    return instance
}

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            cfg := getConfig()
            fmt.Println("got config:", cfg.DSN)
        }()
    }
    wg.Wait()
}
// "initializing config" prints exactly once; "got config: ..." prints 5 times
```

`sync.Once` is safe for concurrent use. The function passed to `Do` is called by the first goroutine that arrives; all other goroutines block until the function returns, and then proceed with the guarantee that the initialization is complete.

> [!WARNING]
> If the function passed to `once.Do` panics, the panic propagates out of `Do`, but `once` is considered done — subsequent calls to `once.Do` with any function will be no-ops. Design accordingly.

---

### Data Races and the Race Detector

A **data race** occurs when two goroutines access the same memory location concurrently, at least one of the accesses is a write, and there is no synchronization between them. Data races are undefined behavior in Go's memory model — the program may produce wrong results, silently corrupt data, or crash unpredictably.

**A concrete race example:**

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    counter := 0
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter++ // DATA RACE: read-modify-write is not atomic
        }()
    }

    wg.Wait()
    fmt.Println(counter) // NOT guaranteed to be 1000 — could be anything
}
```

This code has a race on `counter`. The operation `counter++` compiles to:
1. Read `counter` into a register
2. Add 1
3. Write back

Between step 1 and step 3, another goroutine might read the old value. Both goroutines "increment" from the same starting point, and one increment is lost.

**The race detector:** Go includes a built-in data race detector, based on the ThreadSanitizer algorithm. Enable it at build/test time with `-race`:

```bash
go run -race main.go
go test -race ./...
go build -race -o myapp
```

The race detector instruments all memory accesses and reports races when they are actually observed at runtime:

```
==================
WARNING: DATA RACE
Write at 0x00c0000b4010 by goroutine 7:
  main.main.func1()
      /tmp/main.go:13 +0x44

Previous write at 0x00c0000b4010 by goroutine 6:
  main.main.func1()
      /tmp/main.go:13 +0x44
==================
```

**The race detector does not prove absence of races** — it reports races it observes during execution. A race that only manifests under specific timing may not be caught unless your tests exercise that timing. Run `-race` in CI on all tests.

**Fixing the race above:** Use a mutex or an atomic operation:

```go
// Option 1: sync.Mutex
var mu sync.Mutex
mu.Lock()
counter++
mu.Unlock()

// Option 2: sync/atomic (for simple integer operations)
import "sync/atomic"
var counter int64
atomic.AddInt64(&counter, 1)
```

---

### Deadlocks

A **deadlock** occurs when all goroutines are blocked waiting for each other, and none can proceed. Go's runtime detects when all goroutines are asleep and terminates the program with a distinctive error:

```
fatal error: all goroutines are asleep - deadlock!
```

**Simple deadlock — forgetting to close a channel:**

```go
func main() {
    ch := make(chan int)
    go func() {
        ch <- 1
        ch <- 2
        // forgot close(ch)
    }()

    for v := range ch { // range never stops — waits for more values that never come
        fmt.Println(v)
    }
}
// Output:
// 1
// 2
// fatal error: all goroutines are asleep - deadlock!
```

**Mutex deadlock — acquiring locks in different orders:**

```go
var mu1, mu2 sync.Mutex

// Goroutine A: locks mu1 first, then mu2
go func() {
    mu1.Lock()
    defer mu1.Unlock()
    mu2.Lock()       // blocks if goroutine B holds mu2
    defer mu2.Unlock()
}()

// Goroutine B: locks mu2 first, then mu1
go func() {
    mu2.Lock()
    defer mu2.Unlock()
    mu1.Lock()       // blocks if goroutine A holds mu1
    defer mu1.Unlock()
}()
// Both goroutines may block waiting for the other — classic deadlock
```

**Deadlock prevention rules:**

1. **Always close channels when you are done sending** — omitting `close` leaves receivers waiting forever.
2. **Lock mutexes in a consistent order** — if you must hold multiple mutexes, always acquire them in the same order everywhere in the program.
3. **Avoid holding a lock when calling code you don't control** — external code might try to acquire the same lock or one in a conflicting order.
4. **Prefer channels for goroutine communication** — channels have natural ownership and closing semantics that make deadlocks easier to reason about than mutexes.

> [!WARNING]
> The runtime's deadlock detector only fires when **all** goroutines are blocked. If your program has background goroutines (e.g., a timer or HTTP server goroutine) that are not blocked, the runtime will not detect a partial deadlock in your application goroutines. Design tests with that in mind.

---

### The Go Philosophy: Communication vs Sharing

Go's famous concurrency proverb is:

> **"Do not communicate by sharing memory; share memory by communicating."**

This sentence reverses the conventional approach. The traditional model (threads with mutexes) starts with shared memory and adds locks as needed to make access safe. Go's model starts with independent goroutines and uses channels to pass data between them, avoiding shared state altogether.

The distinction:

| Sharing memory (mutexes) | Communicating (channels) |
|---|---|
| Multiple goroutines access the same variable | Data is passed from one goroutine to another |
| Access serialized by locks | Ownership transferred via channel |
| Race condition if lock is missed | Race condition structurally impossible (only one goroutine "owns" the data at a time) |
| Good for: high-frequency updates to shared counters/caches | Good for: pipelines, events, work distribution |

**But: the mutex is not obsolete.** The proverb is a guideline, not a rule. Channels are not always the better tool:

- A simple shared counter incremented by many goroutines is most efficiently protected by `sync/atomic` or a mutex — a channel would require a dedicated goroutine just to serialize updates.
- A cache shared by many goroutines doing mostly reads is a natural fit for `sync.RWMutex`.
- `sync.Once` for initialization, `sync.Map` for concurrent maps — the `sync` package exists because some patterns fit mutexes naturally.

Rob Pike's advice: **"Use whichever is most expressive and correct for your problem."** Channels are preferred for communication and coordination between goroutines. Mutexes are preferred for protecting shared state when channels would require awkward indirection.

---

### Introductory Patterns

Two patterns appear throughout Go code. Fuller treatment — with `context`, pipelines, worker pools, and error propagation — is in [[go/12. Advanced Concurrency Patterns]].

**Generator pattern** — a function that returns a channel and sends values into it from a goroutine:

```go
package main

import "fmt"

// fibonacci returns a channel that yields the first n Fibonacci numbers
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
    return ch // caller gets a receive-only channel
}

func main() {
    for v := range fibonacci(10) {
        fmt.Print(v, " ")
    }
    fmt.Println()
}
// Output: 0 1 1 2 3 5 8 13 21 34
```

The generator hides the goroutine and channel creation — callers just range over the returned channel. This is idiomatic for producing sequences lazily.

**Fan-out / fan-in** — distribute work to N goroutines (fan-out) and collect results on one channel (fan-in):

```go
package main

import (
    "fmt"
    "sync"
)

// fanOut sends jobs to N worker goroutines and collects results
func fanOut(jobs <-chan int, numWorkers int) <-chan int {
    results := make(chan int, numWorkers)
    var wg sync.WaitGroup

    for w := 0; w < numWorkers; w++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := range jobs {
                results <- j * j // square the job
            }
        }()
    }

    // Close results when all workers are done
    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

func main() {
    jobs := make(chan int, 5)
    for i := 1; i <= 5; i++ {
        jobs <- i
    }
    close(jobs)

    for result := range fanOut(jobs, 3) {
        fmt.Println(result) // order is nondeterministic
    }
}
// Output: the squares 1, 4, 9, 16, 25 in some order
```

For `context`-based cancellation, pipelines with error propagation, and bounded worker pools, see [[go/12. Advanced Concurrency Patterns]].

---

### How the Concepts Fit Together

```
goroutines (go keyword)
       │
       │  communicate via
       ▼
   channels  ──────────────────────────────────────────────────────────────┐
  (unbuffered / buffered)                                                   │
       │                                                                    │
       │  coordinate multiple channels via                                  │
       ▼                                                                    │
    select                                                                  │
  (with default / time.After)                                               │
       │                                                                    │
       │  when shared state is unavoidable, protect with                    │
       ▼                                                                    │
    sync package                                                            │
  (WaitGroup / Mutex / RWMutex / Once)                                      │
       │                                                                    │
       │  verify correctness with                                           │
       ▼                                                                    ▼
 -race detector                                                       patterns:
 (data race detection)                                        generator / fan-out / fan-in
                                                      ↳ deeper patterns in [[go/12. Advanced Concurrency Patterns]]
```

In a real Go program, these primitives compose naturally: you launch goroutines with `go`, pass `chan<-` to producers and `<-chan` to consumers, use `select` to multiplex, protect any shared state with a mutex, use `WaitGroup` to know when a batch of goroutines has finished, and run `go test -race` to catch races you missed.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Goroutine closure captures loop variable by reference**
>
> The most famous goroutine bug. When you launch goroutines in a loop and the goroutine body references the loop variable, all goroutines share the same variable — they see its final value, not the value at the time of launch.
>
> **Wrong:**
> ```go
> for i := 0; i < 5; i++ {
>     go func() {
>         fmt.Println(i) // captures i by reference — all goroutines see the same i
>     }()
> }
> // Likely prints: 5 5 5 5 5 (or some similar repeated final value)
> ```
>
> **Right (pass i as an argument):**
> ```go
> for i := 0; i < 5; i++ {
>     go func(id int) {
>         fmt.Println(id) // id is a copy — each goroutine gets its own value
>     }(i)
> }
> // Prints 0 1 2 3 4 in some order
> ```
>
> **Also right (Go 1.22+ loop variable scoping fix):** In Go 1.22 and later, each loop iteration creates a new `i` variable, so the closure captures the per-iteration value. But rely on the argument-passing form for clarity and backward compatibility.
>
> **Why this matters:** This bug is nearly invisible at small loop counts or on fast machines but consistently manifests in larger programs and CI environments.

> [!WARNING]
> **Mistake 2: Sending to or closing a closed channel**
>
> Closing a channel a second time panics. Sending to a closed channel also panics. Both are runtime panics, not compile-time errors.
>
> **Wrong:**
> ```go
> ch := make(chan int, 1)
> close(ch)
> ch <- 1   // panic: send on closed channel
> close(ch) // panic: close of closed channel
> ```
>
> **Right:** Use the ownership rule — only the goroutine that "owns" the channel (typically the sender) should close it. If multiple goroutines send to the same channel, use a `sync.WaitGroup` to coordinate a single close:
> ```go
> var wg sync.WaitGroup
> for i := 0; i < numSenders; i++ {
>     wg.Add(1)
>     go func() {
>         defer wg.Done()
>         ch <- computeResult()
>     }()
> }
> go func() {
>     wg.Wait()
>     close(ch) // only one goroutine ever closes ch
> }()
> ```

> [!WARNING]
> **Mistake 3: Forgetting WaitGroup.Add must happen before the goroutine launches**
>
> Calling `wg.Add(1)` inside the goroutine is a race — if the main goroutine calls `wg.Wait()` before the spawned goroutine calls `wg.Add(1)`, the wait returns immediately.
>
> **Wrong:**
> ```go
> var wg sync.WaitGroup
> go func() {
>     wg.Add(1)          // too late — Wait() might have already returned
>     defer wg.Done()
>     doWork()
> }()
> wg.Wait()
> ```
>
> **Right:**
> ```go
> var wg sync.WaitGroup
> wg.Add(1)              // add BEFORE launching the goroutine
> go func() {
>     defer wg.Done()
>     doWork()
> }()
> wg.Wait()
> ```

> [!WARNING]
> **Mistake 4: Goroutine leak — goroutines that block forever**
>
> A goroutine that is blocked waiting on a channel that will never receive (because the sender goroutine exited or nobody sends) leaks memory for the lifetime of the program. Goroutine leaks are insidious — they silently consume memory and are invisible in normal testing.
>
> **Leaking example:**
> ```go
> func leak() {
>     ch := make(chan int)
>     go func() {
>         v := <-ch // blocks forever — nobody ever sends on ch
>         fmt.Println(v)
>     }()
>     // function returns; goroutine is now blocked forever; ch is unreachable
> }
> ```
>
> **Prevention:** Design goroutine lifetimes explicitly. Use context cancellation to signal goroutines to exit (see [[go/12. Advanced Concurrency Patterns]]). Use `goleak` (github.com/uber-go/goleak) in tests to detect leaked goroutines.

**Other pitfalls:**

- **Copying sync types** — `sync.Mutex`, `sync.WaitGroup`, `sync.Once`, and other `sync` types must never be copied after first use. Always pass pointers or embed them in structs accessed by pointer.
- **Using `time.Sleep` for synchronization in production** — `time.Sleep` is fine in tests and demos but is never a correct synchronization mechanism in production. Use channels or `sync.WaitGroup` instead.

---

## Mental Models

### Mental Model 1: Goroutines as Postal Workers

Think of your program as a post office. Each goroutine is a postal worker operating independently. Workers don't share a single sorting table (no shared memory) — they communicate by passing parcels (data) through a delivery slot (channel). When a worker puts a parcel in the slot, they cannot put another one in until the previous one is picked up (unbuffered channel). A slot with a storage bin (buffered channel) lets the worker drop off several parcels before anyone collects them.

This model works well for understanding why goroutines are cheap (the post office can hire thousands of part-time workers at low cost), why unbuffered channels require synchronization (the delivery slot is a rendezvous point), and why `select` is useful (a worker waiting at multiple slots, taking from whichever one has a parcel first).

This model breaks down when considering: the mutex pattern, where goroutines do share a variable — in that case, the mutex is like a lock on the shared sorting table (only one worker can touch it at a time).

### Mental Model 2: Channels as Pipes with Valves

Think of a channel as a pipe connecting two goroutines. Unbuffered pipes are pressure-balanced — the sender fills the pipe at exactly the rate the receiver empties it; neither can run ahead. Buffered pipes have a tank in the middle; the sender can fill ahead as long as the tank is not full, and the receiver can drain at its own pace as long as the tank is not empty.

`select` is a junction where the goroutine can tap from whichever pipe has liquid available. `close` is turning off the source valve — the receiver drains what remains, then gets a signal that the source is done.

This model is most useful when reasoning about backpressure: a slow receiver will eventually fill the buffer and block the sender.

### Mental Model 3: The Race Detector as a Code Inspector

The race detector instruments every memory access and tracks which goroutine performed it and when. Think of it as a meticulous code inspector who watches every read and write and shouts when two concurrent workers touch the same memory without showing their synchronization credentials (a lock or channel operation). The inspector can only report races that actually happen during the run — races that are possible but require unlucky timing may not be reported if that timing never occurs during tests.

This model explains why `-race` is necessary in CI (the inspector needs to watch many runs to catch all possible races), and why passing `-race` locally is not sufficient by itself.

> [!NOTE]
> No single mental model covers all of concurrency. Use Model 1 (postal workers) when designing goroutine communication. Use Model 2 (pipes) when reasoning about buffering and backpressure. Use Model 3 (inspector) when debugging data races with the `-race` flag.

---

## Practical Examples

### Example 1: WaitGroup to Wait for Goroutines _(Basic)_

**Scenario:** Launch several goroutines to do independent work and wait for all of them before proceeding.

**Goal:** Demonstrate `sync.WaitGroup` as the correct replacement for `time.Sleep` to coordinate goroutine completion.

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func simulate(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    // Simulate variable-duration work
    time.Sleep(time.Duration(id) * time.Millisecond)
    fmt.Printf("Task %d complete\n", id)
}

func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 5; i++ {
        wg.Add(1)           // add before launching
        go simulate(i, &wg) // pass pointer to wg
    }

    wg.Wait() // blocks until all 5 goroutines call Done()
    fmt.Println("All tasks complete")
}
// Output: tasks 1–5 complete in order (because of the sleep), then "All tasks complete"
// In a real scenario without Sleep, the order would be nondeterministic
```

**What to notice:** `wg.Add(1)` is called in the loop body (in the goroutine's parent), not inside the goroutine. `wg.Done()` is called via `defer` so it runs even if the goroutine panics or returns early. The WaitGroup is passed as `*sync.WaitGroup` — passing by value would copy the counter and break synchronization.

---

### Example 2: Pipeline with Channels _(Intermediate)_

**Scenario:** A three-stage pipeline: generate numbers → square them → print them. Each stage is a goroutine.

**Goal:** Show how channels compose into a pipeline where each stage is independent and communicates only through channels.

```go
package main

import "fmt"

// generate sends integers 1..n to a channel
func generate(n int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 1; i <= n; i++ {
            ch <- i
        }
    }()
    return ch
}

// square reads from in and sends squares to a new channel
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for v := range in {
            out <- v * v
        }
    }()
    return out
}

func main() {
    // Build the pipeline: generate → square → print
    nums := generate(5)
    squares := square(nums)

    for v := range squares {
        fmt.Println(v)
    }
}
// Output:
// 1
// 4
// 9
// 16
// 25
```

**What to notice:** Each stage function returns a `<-chan int`, making the data flow explicit in the type system. Closing propagates down the pipeline: when `generate` closes `nums`, `square`'s `range` loop exits and it closes `out`, which causes the final `range` in `main` to exit. No explicit synchronization is needed — the channel sends/receives are the synchronization.

---

### Example 3: Select with Timeout _(Applied)_

**Scenario:** Calling a slow function concurrently and abandoning it if it takes too long.

**Goal:** Show `select` + `time.After` as the idiomatic timeout pattern.

```go
package main

import (
    "errors"
    "fmt"
    "time"
)

// slowOp simulates a slow operation that takes 200ms
func slowOp(resultCh chan<- string) {
    time.Sleep(200 * time.Millisecond)
    resultCh <- "result from slow operation"
}

// withTimeout calls slowOp and returns its result or an error if it takes too long
func withTimeout(timeout time.Duration) (string, error) {
    resultCh := make(chan string, 1) // buffered so goroutine can send without blocking
    go slowOp(resultCh)

    select {
    case result := <-resultCh:
        return result, nil
    case <-time.After(timeout):
        return "", errors.New("operation timed out")
    }
}

func main() {
    // Timeout shorter than the operation — will time out
    result, err := withTimeout(100 * time.Millisecond)
    if err != nil {
        fmt.Println("Error:", err) // Error: operation timed out
    } else {
        fmt.Println("Result:", result)
    }

    // Timeout longer than the operation — will succeed
    result, err = withTimeout(500 * time.Millisecond)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result) // Result: result from slow operation
    }
}
```

**What to notice:** `resultCh` is buffered with capacity 1. This is important: even after the timeout fires, the goroutine running `slowOp` will eventually try to send on `resultCh`. A buffered channel allows that send to complete (the goroutine exits cleanly) rather than blocking forever (goroutine leak). This is a standard technique for "fire and forget with timeout" goroutines.

---

### Example 4: Detecting and Fixing a Data Race _(Edge Case)_

**Scenario:** A program that appears to work correctly but has a data race — and what happens when you run it with `-race`.

```go
// BROKEN: data race on shared slice
package main

import (
    "fmt"
    "sync"
)

func main() {
    var results []int
    var wg sync.WaitGroup

    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(v int) {
            defer wg.Done()
            results = append(results, v) // RACE: concurrent append to shared slice
        }(i)
    }

    wg.Wait()
    fmt.Println(len(results)) // might print less than 10 — some appends lost
}
```

Running `go run -race` on this produces a `DATA RACE` warning pointing at the `append` line.

**Fixed with a mutex:**

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var results []int
    var mu sync.Mutex
    var wg sync.WaitGroup

    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(v int) {
            defer wg.Done()
            mu.Lock()
            results = append(results, v) // protected — no race
            mu.Unlock()
        }(i)
    }

    wg.Wait()
    fmt.Println(len(results)) // always 10
    // Order of results is nondeterministic — depends on goroutine scheduling
}
```

**What to notice:** The results slice's order is nondeterministic even with the mutex fix — goroutines run in any order, so the append order varies. If you need deterministic ordering, collect results in a pre-allocated slice indexed by the goroutine's `v`, or use a channel to impose order. The mutex only ensures safety (no corruption), not ordering.

---

## Related Concepts

Within this topic:

- [[go/8. Error Handling]] — goroutines and channels don't interact well with function return values; patterns for propagating errors from goroutines (via an `error` channel or `(result, error)` channel) require solid error handling fundamentals
- [[go/12. Advanced Concurrency Patterns]] — `context` for cancellation and deadlines, pipelines with error propagation, worker pools, `sync/atomic`, and semaphores; this module is the prerequisite
- [[go/17. Runtime Internals and the Memory Model]] — the Go scheduler (M:N goroutine-to-thread multiplexing, cooperative vs preemptive scheduling in Go 1.14+), the Go memory model, and what "happens before" guarantees channels actually provide

In other topics:

- [[concurrency]] — cross-language comparison: threads (Python/Java), async/await (JavaScript/Python), the actor model (Erlang), and CSP (Go); understanding where Go's model fits in the broader landscape
- The `context` package philosophy connects to [[go/12. Advanced Concurrency Patterns]] — structured concurrency and cancellation propagation across goroutine trees

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Goroutine Greeting Race** _(Easy)_
>
> Launch five goroutines that each print a greeting message. Observe the nondeterministic output ordering. Then add a `sync.WaitGroup` to ensure `main` waits for all goroutines before exiting.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-goroutine-greeting-race--easy--1-pt)

The exercises range from basic goroutine launching to fixing a real data race. Complete at least the Easy and Medium exercises before taking the test.

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
Concurrent URL Fetcher — given a list of URLs, fetch all of them concurrently using goroutines and channels, collect the response status codes and body lengths, and print a summary. Add a timeout per fetch using `select` + `time.After`, and use `sync.WaitGroup` to know when all fetches are done. Run `go test -race` on any shared state. This exercises every major concept in the module.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Share Memory By Communicating — The Go Blog](https://go.dev/blog/codelab-share)** — Andrew Gerrand's official blog post explaining Go's concurrency philosophy with a concrete walker/state machine example; the canonical explanation of when to use channels vs mutexes

2. **[Go Concurrency Patterns — The Go Blog (Rob Pike)](https://go.dev/blog/pipelines)** — "Pipelines and Cancellation" blog post; covers the generator, pipeline, and fan-out/fan-in patterns with complete code; prerequisite reading before tackling [[go/12. Advanced Concurrency Patterns]]

3. **[A Tour of Go — Concurrency](https://go.dev/tour/concurrency/1)** — Interactive tour pages concurrency/1 through concurrency/11; runnable in the browser; covers goroutines, channels, buffered channels, range/close, select, and sync.Mutex with editable examples

4. **"The Go Programming Language" — Donovan & Kernighan, Chapters 8–9** — Chapter 8 covers goroutines and channels (8.1–8.9: goroutines, pipelines, select, cancellation); Chapter 9 covers shared variables (9.1–9.8: race conditions, mutual exclusion, sync.Once, goroutine creation costs, GOMAXPROCS); the standard textbook treatment

5. **"Learning Go" — Jon Bodner (2nd ed.), Chapter 10** — "Concurrency in Go"; covers goroutines, channels, select, the race detector, `sync` package, and common patterns; excellent for a second perspective with current idioms

6. **[pkg.go.dev/sync](https://pkg.go.dev/sync)** — Official package documentation for `sync.WaitGroup`, `sync.Mutex`, `sync.RWMutex`, `sync.Once`, and `sync.Map`; read the documentation for each type before using it in production

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

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
