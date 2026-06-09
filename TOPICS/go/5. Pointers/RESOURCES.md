# Resources — Module 5: Pointers

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[A Tour of Go — Pointers (go.dev/tour/moretypes/1)](https://go.dev/tour/moretypes/1)** — go.dev

The official interactive tour introduces pointers in two pages (moretypes/1 and moretypes/2) with live, editable code examples. The first page shows `&` and `*` with an integer; the second page introduces pointer types. These two pages are the fastest path to confirming you can use the syntax before reading deeper explanations. Do them first, then return to the README for the full conceptual treatment.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Language Specification — Address operators](https://go.dev/ref/spec#Address_operators)** — Authoritative definition of `&` (address-of) and its addressability requirements — specifically, which expressions are addressable (variables, pointer dereferences, struct fields, array/slice elements) and which are not (map elements, function call results, constants). Compact and unambiguous.

- **[Go Language Specification — Pointer types](https://go.dev/ref/spec#Pointer_types)** — Defines the type `*T` and its zero value (`nil`). Brief but complete.

- **[Effective Go — Allocation with new](https://go.dev/doc/effective_go#allocation_new)** — Explains `new(T)`, the zeroing guarantee, and why composite literals (`&T{}`) are often preferred. Part of the authoritative Effective Go guide by the Go team.

- **[Effective Go — Composite literals](https://go.dev/doc/effective_go#composite_literals)** — Explains `&T{field: value}` and why it is the idiomatic way to allocate and initialize structs, slices, and maps. Directly relevant to the `new()` vs `&T{}` section of this module.

- **[The Go Blog — "Go Data Structures: Interfaces"](https://go.dev/blog/laws-of-reflection)** — Indirectly relevant: explains how interface values store type and value (including pointers). Useful context for understanding why a nil `*T` stored in an `error` interface is not a nil interface (a common gotcha touched on in [[go/8. Error Handling]]).

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 2.3.2 (Pointers), Ch. 4.4 (Structs with pointers) | Ch. 2.3.2 is the definitive concise treatment of Go pointer semantics: `new`, `&`, `*`, the nil zero value, and variable lifetime. Read the "Lifetime of Variables" subsection alongside Ch. 2.3.2 for escape analysis context. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 6 (Pointers) | A full chapter on Go's pointer model written for programmers who know another language. Covers value vs pointer semantics, when to use each, pointer receivers (preview of Module 6), and the performance implications. More opinionated and practical than the spec or D&K. |

---

## Practice Sites

_Places to get more practice problems for the specific skills in this module._

- **[A Tour of Go — Methods and interfaces (go.dev/tour/methods)](https://go.dev/tour/methods/1)** — While officially the "methods" section, this part of the tour immediately applies pointer semantics to method receivers. Working through the first 10 pages of the methods section immediately after this module is excellent preparation for [[go/6. Methods and Interfaces]].

- **[pkg.go.dev — builtin package: new](https://pkg.go.dev/builtin#new)** — The official godoc for `new`, `make`, and related builtins. Brief but authoritative.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/4. Composite Types]] (Module 4) | Structs are the most common target of pointer operations; slice header internals (pointer + length + capacity) explain reference-like behavior; map values are already pointers to hash tables |
| [[go/6. Methods and Interfaces]] (Module 6) | Pointer receivers (`func (p *T) Method()`) are the direct extension of this module's pointer argument pattern; the decision between value and pointer receivers follows the same logic as value vs pointer function arguments |
| [[go/16. Performance and Profiling]] (Module 16) | Escape analysis in depth; `go build -gcflags='-m'` output; heap profile analysis; reducing allocations by controlling pointer escape; quantifying the performance cost of pointer-heavy code |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[memory-management]] | — | The garbage collector that makes heap-allocated pointer targets safe in Go; tracing GC vs reference counting; the write barrier and its role in GC correctness; direct prerequisite for understanding why Go's pointer model is GC-dependent |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Effective Go" — Pointers vs Values section (https://go.dev/doc/effective_go#pointers_vs_values) — covers when to use pointer vs value receivers; directly relevant once you reach Module 6; verify it's current
- [ ] Go by Example — Pointers (https://gobyexample.com/pointers) — community-maintained; short runnable example; useful quick reference but not authoritative
