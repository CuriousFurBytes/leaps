# Resources — Module 17: Runtime Internals and the Memory Model

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[The Go Memory Model](https://go.dev/ref/mem)** — go.dev/ref/mem

The authoritative specification for what Go programs are permitted to assume about memory visibility across goroutines. The 2022 revision (aligned with Go 1.19) is the definitive source for happens-before relationships established by channels, mutexes, `sync.WaitGroup`, `sync/atomic`, and package `init`. Read the "Happens Before" section carefully; the examples are the most important part. Without understanding this document, all concurrent Go code you write is guesswork.

---

## Official Documentation

_The canonical references for anything covered in this module._

- **[The Go Memory Model](https://go.dev/ref/mem)** — The full specification, as noted above. Covers happens-before, data race definition, and guarantees for every synchronization primitive in the standard library.

- **[runtime package documentation](https://pkg.go.dev/runtime)** — Reference for `GOMAXPROCS`, `Gosched`, `NumCPU`, `GC`, `ReadMemStats`, `SetFinalizer`, `SetMaxStack`, and the rest of the runtime API. Read the package-level commentary at the top for an overview of what the runtime package exposes.

- **[unsafe package documentation](https://pkg.go.dev/unsafe)** — The official documentation for `unsafe.Pointer` and its six rules of valid use, plus `unsafe.Add`, `unsafe.Slice`, `unsafe.SliceData`, `unsafe.String`, and `unsafe.StringData`. This is the canonical reference for what operations with `unsafe.Pointer` are and are not permitted.

- **[cmd/cgo documentation](https://pkg.go.dev/cmd/cgo)** — Complete reference for the cgo tool: C/Go type correspondence, the pointer-passing rules, `C.CString` / `C.GoString` / `C.free`, build flags, and how `import "C"` works. Required reading before writing any non-trivial cgo code.

---

## Go Blog Posts

_Official blog posts with depth on specific topics in this module._

- **[Getting to Go: The Journey of Go's Garbage Collector](https://go.dev/blog/ismmkeynote)** — Rick Hudson, 2018. Covers the full history of Go's GC from stop-the-world through the concurrent tri-color design; explains the GC pacer, write barriers, and the design philosophy. The best narrative explanation of why Go's GC looks the way it does.

- **[C? Go? Cgo!](https://go.dev/blog/cgo)** — Andrew Gerrand, 2011; still accurate for the fundamentals. A practical introduction to cgo: embedding C in Go files, calling C functions, passing strings, and the basic ownership model. Start here before reading the full cgo command docs.

- **[A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)** — The Go team, 2022. Practical guide to GC tuning: explains GOGC, GOMEMLIMIT, the GC pacer, and how to use `GODEBUG=gccheckmark=1` for verification. Directly useful for applying module 17 knowledge to production tuning.

---

## Third-Party Technical Articles

_Well-regarded external resources. Accuracy verified at time of writing; re-check if reading significantly after 2025._

- **[Scheduling In Go — Parts I, II, and III](https://www.ardanlabs.com/blog/2018/08/scheduling-in-go-part1.html)** — William Kennedy / Ardan Labs. The most thorough public explanation of the G-M-P scheduler model, work-stealing algorithm, and blocking syscall P-handoff mechanics. Part I covers OS thread scheduling context; Part II covers the Go scheduler; Part III covers concurrency patterns. Read in order.

---

## Relevant Book Chapters

_Specific chapters from well-known Go books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 9 (Concurrency with Shared Variables) | Covers the memory model, race detector, and sync primitives from a user perspective; Chapter 9 section 9.4 covers the memory model explicitly |
| *Go in Practice* — Kennedy, Ketelsen, St. Martin | Ch. 3 (Concurrency in Go) | Covers goroutines and channels from a practical angle; does not go deep into scheduler internals but provides good concurrency context |
| *100 Go Mistakes and How to Avoid Them* — Teiva Harsanyi | Mistakes #56–72 (Concurrency) | Many of the concurrency mistakes in this book are data-race or happens-before errors; reading through these after this module reinforces the memory model in real-world mistake scenarios |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/9. Concurrency]] (Module 9) | The mechanisms (goroutines, channels, sync primitives) that module 17 explains at the runtime/memory-model level |
| [[go/12. Advanced Concurrency Patterns]] (Module 12) | The race detector, atomics, and context; module 17 provides the formal basis for why these patterns work |
| [[go/16. Performance and Profiling]] (Module 16) | GC profiling with pprof; module 17 explains the GC internals behind what pprof shows |
| [[go/18. Build, Tooling, and Deployment]] (Module 18) | cgo's impact on cross-compilation, static linking, and CI pipelines |

---

## Related Shared Concepts

| Concept | Relationship |
|---------|-------------|
| [[memory-management]] | Compares Go's concurrent GC to Python reference counting, Rust ownership, and C manual management |
| [[concurrency]] | Compares Go's G-M-P scheduler and goroutines to OS threads, async/await, and the actor model |

---

## Resources to Evaluate

_Links found but not yet independently verified. Do not rely on these without your own review._

- [ ] "Go's hidden pragmas" and related deep-dives on the `//go:linkname` directive — may be found in blog posts; these cover internal runtime access patterns tangentially related to `unsafe`
- [ ] Dmitry Vyukov's original G-M-P scheduler design document (2012) — exists internally at Google; some version may be available in Go issue tracker discussions (golang.org/issue/8189 and related issues)
