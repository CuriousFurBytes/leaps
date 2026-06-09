# Resources — Module 11: Testing and Benchmarking

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[pkg.go.dev/testing](https://pkg.go.dev/testing)** — golang.org / Go standard library

The official package documentation for the `testing` package. Every type, method, and function discussed in this module is documented here with examples: `*testing.T` and its methods (`Error`, `Fatal`, `Run`, `Helper`, `Cleanup`, `Parallel`, `Skip`), `*testing.B` (`N`, `ResetTimer`, `ReportAllocs`, `Run`), `*testing.F` (`Add`, `Fuzz`), and `TestMain`. This is the authoritative source — when something doesn't behave as expected, this is the first place to check. Read the package overview, then scan the type documentation for each type you use.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Fuzzing — go.dev/security/fuzz](https://go.dev/security/fuzz)** — The official Go fuzzing reference and tutorial. Covers `testing.F`, the `f.Add` and `f.Fuzz` API, the corpus model, running the fuzzer with `-fuzz` and `-fuzztime`, finding and reproducing crashers, and the `testdata/fuzz/` directory layout. Written by the Go team and reflects Go 1.18+ semantics exactly. The tutorial portion walks through finding a real bug with fuzzing end-to-end.

- **[The Go Blog — Coverage for Go 1.20 (go.dev/blog/coverage)](https://go.dev/blog/coverage)** — Explains the coverage instrumentation system, the `-coverprofile` flag, `go tool cover -html` for interactive HTML reports, `go tool cover -func` for per-function coverage summaries, and the Go 1.20 improvements to coverage for integration tests and programs. Concise and practical.

- **[The Go Blog — Using Subtests and Sub-benchmarks (go.dev/blog/subtests)](https://go.dev/blog/subtests)** — The official blog post introducing `t.Run` and `b.Run` (added in Go 1.7). Covers the motivation, the parallel subtest pattern, filtering with `-run`, and the loop variable capture issue. Written by the Go team; the examples are still accurate and idiomatic.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *Learning Go* — Jon Bodner (2nd ed., O'Reilly) | Ch. 15: Writing Tests | The most practitioner-focused Go testing chapter available; covers table-driven tests, when not to use mocking frameworks (with specific reasons), benchmarks, fuzz testing, and the philosophy of what makes a good test. Highly recommended for the sections on testability through interface design. |
| *The Go Programming Language* — Donovan & Kernighan | Ch. 11: Testing | The foundational chapter on Go testing; covers the `testing` package, table-driven tests, randomized testing (pre-fuzzing), benchmark basics, and profiling hooks. Older (pre-Go 1.18 fuzzing) but the core testing API material is still accurate. |

---

## Practice Sites

_Places to get more practice problems for the specific skills in this module._

- **[pkg.go.dev/testing — Examples section](https://pkg.go.dev/testing#pkg-examples)** — The package documentation includes runnable examples for `T.Run`, `B.Run`, and other key methods. Reading and modifying these examples is a good way to internalize the API.

- **[go.dev/doc/tutorial/fuzz](https://go.dev/doc/tutorial/fuzz)** — The official Go fuzzing tutorial. A step-by-step guide that starts with a broken function (`Reverse`), writes a fuzz test for it, runs the fuzzer, and finds a real bug. The most hands-on introduction to fuzzing available. Takes about 20–30 minutes to complete.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/6. Methods and Interfaces]] (Module 6) | Interfaces are the mechanism that makes code testable; the fake injection pattern in this module only works because Go's structural typing allows you to define a narrow interface in the test package and have the production type satisfy it implicitly |
| [[go/8. Error Handling]] (Module 8) | Tests verify error behavior; `errors.Is` and `errors.As` are the correct tools for checking error types in tests; wrapping errors with `%w` makes them inspectable in tests |
| [[go/16. Performance and Profiling]] (Module 16) | Benchmarks are the entry point to performance work; the `go test -bench` output feeds into `benchstat` and the pprof profiler for deeper analysis; this module introduces benchmarks, Module 16 shows how to act on them |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[go]] | [[go/13. Web Services and APIs]] (Module 13) | `net/http/httptest` is introduced in this module; the full HTTP handler and middleware testing patterns are covered in Module 13 alongside routing, middleware, and JSON APIs |
| [[memory-management]] | — | Understanding heap allocations (escape analysis, when values escape to the heap) is what makes `allocs/op` in benchmark output actionable; the `allocs/op` metric is meaningless without knowing what "an allocation" costs and why reducing them matters |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Go Testing By Example" — GopherCon 2023 talk by Russ Cox — covers the design philosophy behind Go's testing tools and recent improvements; verify availability at research.swtch.com or the GopherCon YouTube channel before relying on this link
- [ ] Effective Go section on testing (https://go.dev/doc/effective_go) — Effective Go does not have a dedicated testing section; the testing guidance is scattered; verify whether this is still the case before pointing learners here
- [ ] `benchstat` tool documentation (https://pkg.go.dev/golang.org/x/perf/cmd/benchstat) — the official tool for comparing benchmark results statistically; verify the install command (`go install golang.org/x/perf/cmd/benchstat@latest`) still works before recommending
