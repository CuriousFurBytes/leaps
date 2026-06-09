# Resources — Module 16: Performance and Profiling

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Profiling Go Programs — The Go Blog](https://go.dev/blog/profiling-go-programs)** — go.dev / Russ Cox

The canonical introduction to Go profiling. This post walks through a complete, real profiling session: starting from a slow program, capturing a CPU profile with `go test -cpuprofile`, reading the output with `go tool pprof` (top, list, web), identifying the actual bottleneck, and fixing it. It was written in 2011 but remains accurate for Go 1.22+ — the tools are the same, the profile format is the same, and the workflow is unchanged. Every professional Go developer should read this at least once.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[pkg.go.dev/runtime/pprof](https://pkg.go.dev/runtime/pprof)** — The full API reference for the `runtime/pprof` package. Documents `StartCPUProfile`, `StopCPUProfile`, `WriteHeapProfile`, and the `Profile` type used to capture goroutine, block, mutex, and threadcreate profiles. Read the package-level doc comment for the list of all built-in profiles.

- **[pkg.go.dev/net/http/pprof](https://pkg.go.dev/net/http/pprof)** — Documents the HTTP profiling endpoint registered by importing `net/http/pprof` as a side effect. Explains each `/debug/pprof/` route, the `seconds` query parameter for CPU profiles, and the `debug` parameter for text-format output. Also documents the index page at `/debug/pprof/`.

- **[Profile-Guided Optimization — go.dev/doc/pgo](https://go.dev/doc/pgo)** — The official PGO guide. Explains how to collect a representative CPU profile, how to place the `default.pgo` file, how the build system automatically picks it up, and what improvements to expect. Includes a worked example with before/after performance numbers.

- **[pkg.go.dev/golang.org/x/perf/cmd/benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat)** — Reference documentation for `benchstat`. Explains the input format (benchmark output from `go test -bench`), how the statistical comparison works (Welch's t-test, p-values), how to interpret the delta column, and how to use `-col` and `-row` flags for multi-dimensional comparisons.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 11 (Testing) | Covers benchmarking with `testing.B`; the profiling section is brief but correct and points to the right tools |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 13 (Writing Tests), Ch. 14 (Here Be Dragons: Reflect, Unsafe, and Cgo) | Ch. 13 has a solid benchmarking section; Ch. 14's "Using unsafe to Convert External Binary Data" touches on zero-copy string/byte patterns |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/11. Testing and Benchmarking]] (Module 11) | Prerequisite: the benchmarking primitives (`testing.B`, `-bench`, `-benchmem`) used throughout this module come from Module 11; profiling via `go test` flags is an extension of the same infrastructure |
| [[go/17. Runtime Internals and the Memory Model]] (Module 17) | Follow-on: understanding why allocations matter, how GOGC and the tricolor GC work, and what the Go memory model guarantees requires the runtime internals covered in Module 17 |
| [[go/9. Concurrency]] (Module 9) | `sync.Pool` is a concurrency primitive; block and mutex profiles make sense only with an understanding of goroutine scheduling and lock contention |

---

## Related Concepts

_Cross-topic concepts that underpin this module._

| Concept | Relationship |
|---------|-------------|
| [[memory-management]] | The SHARED concept file explains Go's tricolor GC, stack vs. heap allocation, and why allocations create GC pressure — the foundation for understanding why allocation count matters in this module |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "High Performance Go Workshop" by Dave Cheney (github.com/davecheney/high-performance-go-workshop) — a well-known workshop covering many of this module's topics; verify current maintenance status before using
- [ ] "go tool trace" documentation (pkg.go.dev/cmd/trace) — the execution tracer is briefly covered in the module README; the pkg.go.dev page documents the event types and viewer commands
- [ ] Effective Go section on "Allocation" (go.dev/doc/effective_go#allocation_new) — older but covers `new` vs `make` allocation semantics; verify it still reflects current guidance
