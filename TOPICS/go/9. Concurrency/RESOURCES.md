# Resources — Module 9: Concurrency

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[A Tour of Go — Concurrency (go.dev/tour/concurrency/1)](https://go.dev/tour/concurrency/1)** — golang.org / go.dev

The official interactive tour has 11 pages on concurrency (concurrency/1 through concurrency/11), covering goroutines, channels, buffered channels, range and close, select, default select, and sync.Mutex. Each page has a runnable code example editable in the browser. This is the fastest path to seeing all core concurrency primitives in context. Work through the pages in order — they build on each other and are the official first exposure path.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Language Specification — Goroutines](https://go.dev/ref/spec#Go_statements)** — The formal specification of the `go` statement: what it does, when the called function begins executing, and the relationship to the surrounding goroutine's lifetime. Read alongside the Channel types and Channel operations sections.

- **[Go Language Specification — Channel types and operations](https://go.dev/ref/spec#Channel_types)** — Defines channel direction types (`chan T`, `chan<- T`, `<-chan T`), the send and receive operations, and what `close` guarantees. The most precise reference for what channels actually do.

- **[Go Language Specification — Select statements](https://go.dev/ref/spec#Select_statements)** — The formal definition of `select`, including the guarantee that when multiple cases are ready, one is chosen by uniform pseudo-random selection. This is the spec section to cite when someone claims `select` is deterministic.

- **[The Go Memory Model](https://go.dev/ref/mem)** — The definitive reference for what Go guarantees about memory visibility across goroutines. Explains "happens before" relationships established by channel operations, mutex lock/unlock, and `sync.WaitGroup.Wait`. Essential reading before writing production concurrent code.

---

## Go Blog — Concurrency Articles

_Official blog posts that explain Go's concurrency philosophy and patterns._

- **[Share Memory By Communicating](https://go.dev/blog/codelab-share)** — The canonical explanation of Go's concurrency philosophy. Uses a concurrent poller as a worked example to show why channels are preferred over shared memory for communication. Short (15 minutes) and essential.

- **[Go Concurrency Patterns: Pipelines and Cancellation](https://go.dev/blog/pipelines)** — By Sameer Ajmani. Covers the generator, pipeline, and fan-out/fan-in patterns with complete, compilable code. Introduces the `done` channel for cancellation (the predecessor to `context`). This is the primary reference for the patterns introduced at the end of this module and extended in [[go/12. Advanced Concurrency Patterns]].

- **[Go Concurrency Patterns (2012 Google I/O talk)](https://go.dev/blog/concurrency-patterns)** — Rob Pike's original concurrency talk. Covers goroutines, channels, the generator pattern, select, and timeouts. Available as a blog post with the slide deck. Historically important and still highly relevant — Pike's intuition for when to use channels is unmatched.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 8: Goroutines and Channels; Ch. 9: Concurrency with Shared Variables | Ch. 8 covers goroutines, the clock/echo server examples, pipelines, select, and cancellation (8.1–8.9). Ch. 9 covers race conditions, sync.Mutex, sync.RWMutex, memory synchronization, and GOMAXPROCS (9.1–9.8). These two chapters are the most thorough textbook treatment of Go concurrency. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 10: Concurrency in Go | Covers goroutines, channels, select, the race detector, sync package, and common patterns. Notable for its explicit guidance on when to use channels vs mutexes. More opinionated and current-idiom-focused than Donovan & Kernighan. |

---

## Package Documentation

_Official package docs for the specific packages used in this module._

- **[pkg.go.dev/sync](https://pkg.go.dev/sync)** — Documentation for `sync.WaitGroup`, `sync.Mutex`, `sync.RWMutex`, `sync.Once`, `sync.Map`, and `sync.Cond`. Read the documentation for each type before using it — the caveats (e.g., "must not be copied after first use") are stated clearly there.

- **[pkg.go.dev/sync/atomic](https://pkg.go.dev/sync/atomic)** — Documentation for `atomic.AddInt64`, `atomic.LoadInt64`, `atomic.StoreInt64`, and the newer `atomic.Value` and typed atomic types (Go 1.19+). Use for simple integer counters and flags where a full mutex is overkill.

- **[pkg.go.dev/time](https://pkg.go.dev/time)** — Relevant functions: `time.After`, `time.NewTimer`, `time.AfterFunc`. `time.After` returns a channel that fires once after the duration; understanding the difference between `time.After` and `time.NewTimer` (the latter can be stopped to avoid GC pressure in tight loops) is important for production code.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/8. Error Handling]] (Module 8) | Goroutines cannot return errors in the normal sense; the patterns for propagating errors from goroutines (via channels, `(result, error)` pairs) require solid error handling foundations |
| [[go/12. Advanced Concurrency Patterns]] (Module 12) | Direct continuation: `context` for cancellation and deadlines, pipelines with error propagation, worker pools, `sync/atomic`, and the `errgroup` package. This module is the prerequisite. |
| [[go/17. Runtime Internals and the Memory Model]] (Module 17) | Explains the goroutine scheduler (M:N threading, work stealing, preemption in Go 1.14+), GOMAXPROCS, and the formal Go memory model. The "why" behind goroutine behavior. |

---

## Related Concepts

_The cross-topic concept page that connects Go's concurrency to other languages._

| Topic | Concept | Relationship |
|-------|---------|-------------|
| [[concurrency]] | Cross-language comparison | Compares Go's CSP model to Python's asyncio/threading/multiprocessing, Rust's ownership-based concurrency, JavaScript's event loop, and the actor model. Reading this after Module 9 gives perspective on where Go's design fits. |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Effective Go" — Concurrency section (https://go.dev/doc/effective_go#concurrency) — covers goroutines, channels, and a parallel loop example. Older document (2009) but mostly still accurate; verify against current idioms before using as a reference.
- [ ] Go by Example — Goroutines, Channels, Channel Directions, Select pages (https://gobyexample.com) — community-maintained; generally accurate but not official; useful for quick code examples.
