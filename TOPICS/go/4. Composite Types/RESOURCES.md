# Resources — Module 4: Composite Types

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Go Slices: usage and internals — The Go Blog](https://go.dev/blog/slices-intro)** — Andrew Gerrand / go.dev

The canonical explanation of the slice header (pointer, length, capacity), slicing expressions, the `copy` function, and `append`. Written in 2011 and still accurate. This post is the standard reference that every Go programmer should read at least once. It uses diagrams to show the ptr/len/cap layout and traces through append-with-reallocation step by step. Read this before attempting the exercises.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Arrays, slices (and strings): The mechanics of 'append' — The Go Blog](https://go.dev/blog/slices)** — Rob Pike's deeper follow-up to the Gerrand post (2013). Covers the three-index slice expression, `append`'s growth strategy, `copy`, and building efficient byte buffers. More implementation-focused than the Gerrand post; recommended after completing the exercises.

- **[Effective Go — Composite Literals](https://go.dev/doc/effective_go#composite_literals)** — The official style guide's treatment of array, slice, map, and struct literals; covers when to use the short form vs named-field form and how to write idiomatic composite type usage.

- **[Effective Go — Maps](https://go.dev/doc/effective_go#maps)** — Covers map initialization, the zero-value nil map, the comma-ok test idiom, and deletion. Short but precise; a good complement to the longer blog posts.

- **[Go Language Specification — Composite types](https://go.dev/ref/spec#Types)** — The authoritative formal definitions for array types, slice types, struct types, and map types; also covers the definition of "comparable" (essential for understanding map key requirements). Read the sub-sections "Array types", "Slice types", "Struct types", and "Map types".

- **[Go Language Specification — Comparison operators](https://go.dev/ref/spec#Comparison_operators)** — Defines exactly which types are comparable (and therefore usable as map keys). Essential reading for understanding why slices, maps, and functions cannot be map keys.

---

## Standard Library Packages

_Official API documentation for packages introduced in this module._

- **[pkg.go.dev/slices](https://pkg.go.dev/slices)** — The generic `slices` package (added in Go 1.21). Documents `Sort`, `SortFunc`, `Contains`, `Index`, `Clone`, `Compact`, `Reverse`, and more. Check this before writing any manual slice manipulation — there is often an existing function.

- **[pkg.go.dev/maps](https://pkg.go.dev/maps)** — The generic `maps` package (added in Go 1.21). Documents `Clone`, `Keys`, `Values`, `DeleteFunc`, and `Equal`. Smaller than the `slices` package but covers the most common map utilities.

- **[pkg.go.dev/strings](https://pkg.go.dev/strings)** — The `strings` package for string manipulation: `Fields`, `Split`, `Join`, `Contains`, `TrimSpace`, `Builder`, and more. This is the first place to look before writing any string processing code.

- **[pkg.go.dev/unicode/utf8](https://pkg.go.dev/unicode/utf8)** — The `unicode/utf8` package for low-level UTF-8 operations: `RuneCountInString`, `DecodeRuneInString`, `ValidString`. Essential when doing character-level string processing.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 4 (Composite Types) | The book chapter that maps directly to this module — arrays, slices (including the header explanation), maps (with the comma-ok idiom), and structs (with embedding). The most comprehensive prose treatment; highly recommended alongside the blog posts. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 3 (Composite Types) | Modern treatment that covers the `slices` and `maps` packages (Go 1.21+) alongside the fundamentals. Particularly clear on nil vs empty slice (and why the distinction matters for JSON), and on the maps-are-not-concurrent-safe caveat. |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/3. Functions]] (Module 3) | Built-in functions `append`, `copy`, `make`, `delete`, `len`, `cap` are the primary interface to composite types; the variadic `...` spread syntax used in `append(s, other...)` requires understanding variadic functions |
| [[go/5. Pointers]] (Module 5) | Value vs reference semantics established in this module are the direct prerequisite; passing `*[]int` or `*MyStruct` to functions is the other side of the same coin |
| [[go/6. Methods and Interfaces]] (Module 6) | Struct methods and embedding from this module are the foundation; interfaces rely on structs having methods, and embedding promotes methods as well as fields |
| [[go/9. Concurrency]] (Module 9) | Maps are not safe for concurrent access; this module introduces the footgun, Module 9 resolves it with `sync.Mutex` and `sync.Map` |
| [[go/15. Reflection and Metaprogramming]] (Module 15) | Struct tags (introduced briefly in this module) are read via reflection; `encoding/json`, `database/sql`, and most Go frameworks use struct tags for field mapping |

---

## Related Shared Concepts

| Concept | Relationship |
|---------|-------------|
| [[memory-management]] | Go's GC manages backing arrays; escape analysis determines whether a slice's backing array lives on the stack or heap; understanding this is the production-performance complement to the mechanical slice model in this module |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Go Data Structures" by Russ Cox — early blog post on Go's internal representation; may be superseded by the official blog posts but might have useful low-level detail
- [ ] "Go by Example" — slices, maps, structs pages (https://gobyexample.com) — community-maintained; generally accurate but not official; good for quick syntax reference
