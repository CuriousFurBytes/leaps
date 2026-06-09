# Resources — Module 12: Advanced Concurrency Patterns

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Go Concurrency Patterns: Pipelines and cancellation — The Go Blog](https://go.dev/blog/pipelines)** — go.dev/blog

Sameer Ajmani's 2014 article is the authoritative source for the pipeline pattern and cancellation. It introduces the done-channel pattern (the precursor to `context.Context`), builds a multi-stage pipeline from scratch, demonstrates fan-out and fan-in, and explicitly addresses goroutine leaks. Although the article predates the `context` package, the patterns are directly translated in this module using `context.Context` instead of a done channel. Reading this once gives you the foundation for everything else.

---

## Official Documentation

_The canonical reference for everything covered in this module._

- **[pkg.go.dev/context](https://pkg.go.dev/context)** — Complete documentation for the `context` package. Read the package-level doc comment in full — it states the usage rules explicitly (first parameter, do not store in structs, typed keys for WithValue). The individual function docs for `WithCancel`, `WithDeadline`, `WithTimeout`, and `WithValue` each include caveats that are easy to miss.

- **[Go Concurrency Patterns: Context — The Go Blog](https://go.dev/blog/context)** — Sameer Ajmani's companion article to the pipelines post. Explains the `context` package design rationale, when (and when not) to use `context.Value`, and how context propagates across API boundaries in a real server. The canonical explanation of why context is the first parameter by convention.

- **[pkg.go.dev/sync/atomic](https://pkg.go.dev/sync/atomic)** — Documentation for the `sync/atomic` package, including the typed atomic types (`atomic.Int64`, `atomic.Uint32`, `atomic.Bool`, `atomic.Pointer[T]`) introduced in Go 1.19. The package-level overview explains memory ordering guarantees; read it before using atomics in production code.

- **[pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)** — Documentation for the `errgroup` package. Includes examples for `WithContext`, the `SetLimit` method (bounded concurrency within errgroup), and `TryGo`. Short and worth reading in full.

---

## Talks

- **"Advanced Go Concurrency Patterns" — Sameer Ajmani, Google I/O 2013** — The talk that formalized the pipeline and cancellation patterns for the Go community. Available on the Go YouTube channel. Covers the same material as the blog post but with live code demonstrations and audience Q&A. Approximately 45 minutes.

---

## Relevant Book Chapters

_Specific chapters from the Go topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *Concurrency in Go* — Katherine Cox-Buday (O'Reilly) | Ch. 4 "Concurrency Patterns in Go", Ch. 5 "Concurrency at Scale" | Ch. 4 covers pipelines, fan-out/fan-in, queuing, and the context pattern in depth. Ch. 5 covers error propagation, timeouts, rate limiting, and healing. This is the most comprehensive treatment of the exact patterns in this module. |
| *The Go Programming Language* — Donovan & Kernighan | Ch. 8 "Goroutines and Channels", Ch. 9 "Concurrency with Shared Variables" | Ch. 8 covers pipelines with channels; Ch. 9 covers sync.Mutex, sync.Once, and the race detector. Does not cover context or errgroup (predates their standardization). |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 12 "Concurrency in Go" | Covers context, goroutine patterns, and errgroup with modern Go 1.21+ idioms. Good complement to the Cox-Buday book for a more concise treatment. |

---

## External Packages Covered in This Module

| Package | Import Path | Purpose |
|---------|------------|---------|
| errgroup | `golang.org/x/sync/errgroup` | Goroutine groups with error propagation and context cancellation |
| rate | `golang.org/x/time/rate` | Token-bucket rate limiter; `rate.Limiter` is context-aware |
| goleak | `go.uber.org/goleak` | Goroutine leak detection in tests |

Install with:
```bash
go get golang.org/x/sync/errgroup
go get golang.org/x/time/rate
go get go.uber.org/goleak
```

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/9. Concurrency]] (Module 9) | Foundation module; all patterns here are built on goroutines, channels, `select`, `sync.Mutex`, and `sync.WaitGroup` |
| [[go/11. Testing and Benchmarking]] (Module 11) | `go test -race` and `goleak` are used throughout this module's exercises |
| [[go/17. Runtime Internals and the Memory Model]] (Module 17) | Formal happens-before guarantees for channels and atomics; essential before writing lock-free code |

---

## Related Concepts in Other Topics

| Topic | Concept | Relationship |
|-------|---------|-------------|
| [[concurrency]] (SHARED) | CSP model, race conditions, deadlocks | The general concurrency concepts behind goroutines and channels; Go's model compared to threads, async/await, and actors |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "The Go Memory Model" — https://go.dev/ref/mem — the official specification for happens-before in Go; relevant to atomics section but dense; evaluate before adding as primary resource
- [ ] Go by Example — context, goroutines, channels pages — https://gobyexample.com — community-maintained; generally accurate but verify examples against current Go version
