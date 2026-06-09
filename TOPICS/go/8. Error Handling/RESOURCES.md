# Resources — Module 8: Error Handling

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Working with Errors in Go 1.13 — The Go Blog](https://go.dev/blog/go1.13-errors)** — golang.org / go.dev

The official blog post introducing `errors.Is`, `errors.As`, `errors.Unwrap`, and the `%w` verb in `fmt.Errorf`. Written by Damien Neil and Jonathan Amsterdam (two core Go team members), it explains the design rationale for error wrapping, how to migrate from older patterns, and how to implement custom `Is` and `As` methods on error types. This is the canonical reference for all Go 1.13+ error features — everything in this module's wrapping, sentinel, and custom-type sections maps directly to material covered here.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Error handling and Go — The Go Blog](https://go.dev/blog/error-handling-and-go)** — Andrew Gerrand's 2011 post, still fully accurate. Introduces the `error` interface, the philosophy of errors as values, custom error types, and the `errorString` type returned by `errors.New`. The best entry point before reading the 2019 post above.

- **[Effective Go — Errors](https://go.dev/doc/effective_go#errors)** — The official idiomatic Go guide's error section. Covers the `error` interface, adding context, and conventions for error message formatting (lower-case, no trailing punctuation, no "Error:" prefix). Essential for writing errors that look idiomatic.

- **[pkg.go.dev/errors](https://pkg.go.dev/errors)** — Standard library documentation for the `errors` package. Lists all exported functions: `New`, `Is`, `As`, `Unwrap`, `Join` (Go 1.20+). Each entry has a runnable example. Check this when you need the exact behavior of any function.

- **[Go Language Specification — Handling panics](https://go.dev/ref/spec#Handling_panics)** — The spec's section on `recover`, `panic`, and their semantics. Authoritative on exactly when `recover` stops a panic and what it returns. Dense but unambiguous.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 5.4 (Errors), Ch. 5.9 (Panic), Ch. 5.10 (Recover) | The definitive Go book. Chapter 5 covers error idioms, custom error types, `fmt.Errorf`, `panic`, and `recover` with careful explanations and examples. The section on panic/recover includes the real-world example of parsing an expression tree using panic for internal error propagation. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 9 (Errors) | The most modern treatment of Go error handling; covers `errors.New`, `fmt.Errorf`, wrapping with `%w`, `errors.Is`, `errors.As`, `errors.Join`, sentinel errors, custom error types, and the panic/recover boundary. Highly practical; explicitly covers anti-patterns including log-and-return. |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/6. Methods and Interfaces]] (Module 6) | `error` is an interface; structural typing, nil interface values, and the typed-nil trap all require understanding interface internals from Module 6 |
| [[go/3. Functions]] (Module 3) | Multiple return values, named returns, defer, and closures are the building blocks of all error handling patterns in this module |
| [[go/9. Concurrency]] (Module 9) | In concurrent programs, errors from goroutines must be collected; `errors.Join` and channel-based error aggregation connect to goroutine patterns |
| [[go/13. Web Services and APIs]] (Module 13) | The `recover`-in-middleware pattern is fully developed in that module, alongside HTTP error response conventions and status code mapping |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[go/11. Testing and Benchmarking]] (Module 11) | Testing error paths uses `errors.Is` in assertions; table-driven tests for error conditions are a direct application of the types introduced here |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Errors are values" — Rob Pike, The Go Blog, Jan 2015 (https://go.dev/blog/errors-are-values) — Rob Pike's post on treating errors as first-class values and avoiding repetitive `if err != nil` chains; complements the 2019 wrapping post
- [ ] Go by Example — Error Wrapping (https://gobyexample.com/errors) — Community-maintained; generally accurate but not official; useful for quick code examples
