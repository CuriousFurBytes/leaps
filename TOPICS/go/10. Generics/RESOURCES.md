# Resources — Module 10: Generics

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[An Introduction To Generics — The Go Blog](https://go.dev/blog/intro-generics)** — Robert Griesemer and Ian Lance Taylor, go.dev

Written by two of the principal designers of Go's generics system, this post explains the design rationale, walks through the type parameter syntax, and introduces constraints with concrete examples. It covers the key insight — "constraints are interfaces" — better than any third-party source. Read this after the module README to reinforce the core syntax and see the designers' intended usage patterns.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[When To Use Generics — The Go Blog](https://go.dev/blog/when-generics)** — Ian Lance Taylor, go.dev. The official guidance on the three scenarios where generics are appropriate and the cases where a plain interface or concrete code is better. The most important single post for writing idiomatic generic Go. Read this before writing any production generic code.

- **[Go 1.18 Release Notes — Type Parameters](https://go.dev/doc/go1.18)** — The release notes for Go 1.18, which introduced generics. The "Type Parameters" section documents the exact syntax, the `any` alias, the `comparable` constraint, and the initial set of limitations (including the restriction on methods having type parameters). Also links to the `golang.org/x/exp/constraints` package that predated the standard `cmp` package.

- **[pkg.go.dev/slices](https://pkg.go.dev/slices)** — The complete API reference for the `slices` standard library package (Go 1.21+). Read through the function list — `Sort`, `SortFunc`, `SortStableFunc`, `Contains`, `ContainsFunc`, `Index`, `IndexFunc`, `BinarySearch`, `BinarySearchFunc`, `Clone`, `Compact`, `DeleteFunc`, and more. These are the generic functions you'll use most often in real Go code.

- **[pkg.go.dev/maps](https://pkg.go.dev/maps)** — The complete API reference for the `maps` standard library package (Go 1.21+). Covers `Keys`, `Values`, `Clone`, `Copy`, `Delete`, `Equal`, and the new `Collect`/iterator-based functions added in Go 1.23.

- **[pkg.go.dev/cmp](https://pkg.go.dev/cmp)** — The complete API reference for the `cmp` standard library package (Go 1.21+). Includes the definition of `cmp.Ordered`, `cmp.Compare`, and `cmp.Or`. The `cmp.Ordered` constraint is the canonical answer to "what constraint do I use for sortable types?"

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 8 (Generics) | Covers generics in depth with the same intermediate-to-advanced audience as this module; explains generic functions, generic types, constraints, type inference, and includes a clear discussion of when generics help vs when interfaces are better. One of the best treatments of the topic outside of the official Go blog posts. |
| *The Go Programming Language* — Donovan & Kernighan | No chapter (pre-generics) | This book predates Go 1.18 and does not cover generics; it remains the authoritative reference for everything else in Go, but for generics use the Go blog posts and Bodner's book. |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/6. Methods and Interfaces]] (Module 6) | Constraints are interfaces; you must understand how interfaces work (structural typing, method sets, type assertions) before constraints make sense |
| [[go/4. Composite Types]] (Module 4) | The `slices` and `maps` packages operate on slices and maps; generic containers like `Stack[T]` and `Set[T]` wrap these composite types |
| [[go/11. Testing and Benchmarking]] (Module 11) | Testing generic functions requires table-driven tests with multiple type arguments; benchmarking generic vs interface vs concrete implementations quantifies the GC shape stenciling overhead discussed in this module |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] The Go specification section on Type parameter declarations (https://go.dev/ref/spec#Type_parameter_declarations) — the formal grammar for type parameter lists; useful if you need to understand edge cases, but dense for first reading
- [ ] `golang.org/x/exp/constraints` package — the experimental constraints package that predated `cmp`; now largely superseded by `cmp.Ordered`, but still useful if you need `Integer`, `Float`, or `Complex` constraints not in the standard library
- [ ] Go by Example — Generics (https://gobyexample.com/generics) — community-maintained; short runnable examples; generally accurate but not an authoritative source
