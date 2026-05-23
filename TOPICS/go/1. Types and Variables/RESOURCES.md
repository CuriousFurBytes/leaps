# Resources — Module 1: Types and Variables

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[A Tour of Go — Basics](https://go.dev/tour/basics/1)** — go.dev (official)

The official interactive Go tutorial. The "Basics" section covers type declarations, variables, zero values, constants, and type conversion in exactly the order this module does — and every example runs directly in the browser without any local installation. Work through "Packages, variables, and functions" through "Basic types" and "Type conversions." This is the most direct complement to this module.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Specification — Types](https://go.dev/ref/spec#Types)** — The authoritative definition of every type in Go: what the sizes are, what the zero values are, what operations are defined. Dense reading, but essential when you need a precise answer.
- **[Go Specification — Declarations and Scope](https://go.dev/ref/spec#Declarations_and_scope)** — Precisely defines where `:=` is valid, what redeclaration means, and how blank identifiers work. Use this when you have a "but why?" question about scoping rules.
- **[Go Specification — Constant expressions and iota](https://go.dev/ref/spec#Iota)** — The exact rules for how `iota` increments. A short, readable section of the spec.
- **[Effective Go — Constants](https://go.dev/doc/effective_go#constants)** — The official style guide's section on constants. Explains typed vs. untyped constants, the `iota` idiom, and when to use each. This is the "how to write it well" complement to the spec's "what is it."

---

## Relevant Book Chapters

_Specific chapters from well-known Go books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| "The Go Programming Language" (Donovan & Kernighan) | Ch. 2: Program Structure | Covers declarations, zero values, short variable declarations, type declarations, and scope. The best book-length treatment of this module's content. |
| "The Go Programming Language" (Donovan & Kernighan) | Ch. 3: Basic Data Types | Covers integers, floats, complex numbers, booleans, strings, and constants with iota. Direct companion to this module's Core Concepts section. |
| "Go in Action" (Kennedy, Ketelsen, St. Martin) | Ch. 2: Quick Start | Shows all three variable declaration forms in context of a real program. |

---

## Standard Library Documentation

_Package documentation directly relevant to this module._

- **[pkg.go.dev/strconv](https://pkg.go.dev/strconv)** — The standard library package for converting between strings and other basic types. Key functions for this module: `strconv.Itoa` (int to string), `strconv.Atoi` (string to int), `strconv.FormatFloat`, `strconv.ParseFloat`. Essential for avoiding the `string(int)` gotcha.
- **[pkg.go.dev/fmt](https://pkg.go.dev/fmt)** — The formatting package used in all examples. The `%T` verb (print type), `%v` (default format), `%d` (integer), `%f` and `%.2f` (float), and `%q` (quoted string) are the verbs most relevant to this module.

---

## Practice Sites

_Places to get more hands-on practice with type and variable problems._

- **[The Go Playground](https://go.dev/play/)** — Run and share Go code directly in the browser. No installation needed. Use this to experiment with type conversion, zero values, and iota patterns as you work through this module.
- **[go.dev/tour — Basics exercises](https://go.dev/tour/basics/1)** — The tour includes small interactive exercises at the end of each section. Work through the Basics section for additional practice beyond this module's exercises.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/0. Introduction]] (Module 0: Introduction) | Provides the foundational Go program structure (`package main`, `func main`, `fmt.Println`) used in all examples in this module |
| [[go/2. Control Flow]] (Module 2: Control Flow) | Uses variables and types as loop counters, condition values, and switch targets; you must be solid on this module before proceeding |
| [[go/3. Functions]] (Module 3: Functions) | Multiple return values, short variable declaration patterns, and named return types all build directly on this module |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[python]] | Module 1: Variables and Types | Python's counterpart to this module. Covers the same ground from a dynamic typing perspective. Useful contrast if you already know Python, or as a reference when comparing how the two languages handle the same programming concepts. |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "100 Go Mistakes" by Teiva Harsanyi — Chapter 1 covers type and variable mistakes; reportedly covers the `int` vs `int64` serialization issue from the bonus question in detail
- [ ] gophercon.com talk archives — several talks on Go's type system; titles and years need verification before recommending specific ones
