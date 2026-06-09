# Resources — Module 13: Web Services and APIs

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[pkg.go.dev/net/http](https://pkg.go.dev/net/http)** — pkg.go.dev

The official package documentation for `net/http`. Read the top-level overview, then the type docs for `ServeMux` (includes the full Go 1.22 routing pattern specification), `Handler`, `HandlerFunc`, `Server` (all timeout fields), `Client`, and `Request`. The `ServeMux` docs contain the definitive rules for pattern precedence and wildcard matching. Every question about "what does this field do?" or "what happens when two patterns match?" is answered here.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Routing Enhancements for Go 1.22 — The Go Blog](https://go.dev/blog/routing-enhancements)** — The blog post by the feature's author explaining method+path patterns, path parameters (`{id}`), wildcards (`{rest...}`), precedence rules, and the 405 automatic response. This is the definitive source for understanding Go 1.22 routing and should be read fully before writing any production routing code.

- **[Go 1.22 Release Notes — Enhanced Routing Patterns](https://go.dev/doc/go1.22#enhanced_routing_patterns)** — The terse but authoritative release notes section for the routing changes. Read alongside the blog post above for a complete picture.

- **[Writing Web Applications — go.dev/doc/articles/wiki](https://go.dev/doc/articles/wiki)** — The official Go web application tutorial. Builds an editable wiki step by step using `net/http`, `html/template`, and `os`. Good for seeing the full server lifecycle (register routes, parse request, render template, handle errors) in one linear walkthrough. Note: predates Go 1.22, so routing uses the older style, but all other patterns are current.

- **[pkg.go.dev/net/http/httptest](https://pkg.go.dev/net/http/httptest)** — Package documentation for `httptest.NewRecorder`, `httptest.NewRequest`, and `httptest.NewServer`. Each entry has runnable examples. Read this fully before writing handler tests — `NewRecorder` and `NewServer` serve different purposes.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *Let's Go* — Alex Edwards | All — the book is specifically about building web applications with Go's stdlib | Highly recommended; covers `net/http` in depth, middleware patterns, JSON responses, server configuration, and testing. Targets Go 1.21+ and is one of the most practical Go web resources available. See alexedwards.net/lets-go for details. |
| *The Go Programming Language* — Donovan & Kernighan | Ch. 7 (Interfaces) | Understanding `http.Handler` as an interface and `http.HandlerFunc` as an adapter requires comfort with Go interfaces; Ch. 7 is the clearest explanation of that pattern. |
| *Go in Action* — Kennedy, Ketelsen, St. Martin | Ch. 8 (HTTP services) | Covers building HTTP services with the standard library; slightly dated (pre-1.22) but the handler and middleware patterns are unchanged. |

---

## Practice Sites

_Places to get more practice with the specific skills in this module._

- **[pkg.go.dev/net/http — Examples](https://pkg.go.dev/net/http#pkg-examples)** — The package documentation includes runnable Go Playground examples for many types and functions. Look for examples on `ServeMux`, `FileServer`, `StripPrefix`, and `HandleFunc`.

- **[pkg.go.dev/net/http/httptest — Examples](https://pkg.go.dev/net/http/httptest#pkg-examples)** — Runnable examples for `NewRecorder` and `NewServer`, showing the exact patterns used to test handlers.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/8. Error Handling]] (Module 8) | Structured JSON error responses use `fmt.Errorf` wrapping and `errors.Is`/`errors.As` unwrapping; `*http.MaxBytesError` is unwrapped with `errors.As` |
| [[go/11. Testing and Benchmarking]] (Module 11) | `httptest.NewRecorder` and `httptest.NewServer` slot into table-driven test patterns; handler benchmarks use the same `b.N` loop structure |
| [[go/12. Advanced Concurrency Patterns]] (Module 12) | `context.WithTimeout` and `context.WithCancel` in handlers are the same tools used in goroutine pipelines; graceful shutdown is a concurrency coordination problem |
| [[go/14. Databases and Persistence]] (Module 14) | The `ItemStore` interface pattern introduced here is implemented in the next module; handler tests remain database-free while integration tests connect to a real database |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "How I Write HTTP Services in Go After 13 Years" — Mat Ryer (various blog platforms) — frequently cited for structuring Go HTTP services; verify the current version is up to date with Go 1.22 patterns before referencing
- [ ] go-chi/chi README (https://github.com/go-chi/chi) — if you decide to use chi; the README shows middleware chaining and sub-router patterns clearly; useful comparison with stdlib approach
