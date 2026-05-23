# Resources — Module 2: Control Flow

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[A Tour of Go — Flow Control (go.dev/tour)](https://go.dev/tour/flowcontrol/1)** — golang.org / go.dev

The official interactive tour has 13 pages on flow control (flowcontrol/1 through flowcontrol/13), covering every form of `for`, `if` with init statement, `switch` (including expression-less switch and type switch), and `defer`. Each page has a runnable code example you can edit directly in the browser. This is the fastest path to seeing all control flow constructs in context. Work through the pages in order — they build on each other.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Language Specification — Statements](https://go.dev/ref/spec#Statements)** — The authoritative formal specification. Read the sub-sections: "For statements" (all three forms plus range), "Switch statements" (expression switch and type switch), "Defer statements", "Goto statements", and "Labeled statements". The spec is dense but unambiguous — check it when you need to know exactly what Go guarantees.

- **[Go Language Specification — For range](https://go.dev/ref/spec#For_range)** — The specific section covering what types can be ranged over, what values are yielded for each type (slice, array, map, string, channel), and the precise semantics of index/value assignment. The string case is especially important: "For a string value, the 'range' clause iterates over the Unicode code points in the string starting at byte index 0."

- **[Go Blog — Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)** — Official blog post by Andrew Gerrand (2010, still accurate). Explains the three rules of defer: (1) deferred function arguments are evaluated when the defer statement evaluates; (2) deferred function calls are executed in LIFO order after the surrounding function returns; (3) deferred functions may read and assign to named return values. Also covers `panic` and `recover`, which are not in this module but are useful context.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 1 (Tutorial), Ch. 5 (Functions) | Ch. 1 introduces `for` and `if` through a word-count program; Ch. 5 covers `defer` in the context of function values and closures. This is the standard Go reference book. |
| *Go in Action* — Kennedy, Ketelsen, St. Martin | Ch. 3 (Packaging and tooling), Ch. 4 (Arrays, slices, maps) | Ch. 4's sections on ranging over slices and maps give applied context for `for range` that complements the syntax-focused module content. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 4 (Blocks, Shadows, and Control Structures) | Entire chapter on control flow with a focus on idiomatic Go; specifically addresses the defer-in-loop pitfall and explains labeled break/continue clearly. |

---

## Practice Sites

_Places to get more practice problems for the specific skills in this module._

- **[Go Tour — Flow Control exercises (go.dev/tour)](https://go.dev/tour/flowcontrol/1)** — The interactive tour doubles as a practice site; each page has an editable example. The exercises at the end of the tour section (fibonacci closure, etc.) use the control flow constructs from this module.

- **[pkg.go.dev — unicode/utf8 package](https://pkg.go.dev/unicode/utf8)** — Reference for `RuneCountInString`, `DecodeRuneInString`, and related functions used in Exercise 5. Reading the package documentation and running the examples directly is the best way to solidify the rune vs byte distinction.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/1. Types and Variables]] (Module 1) | Control flow operates on values; understanding `int`, `bool`, and `string` types is prerequisite to writing correct conditions and range iterations |
| [[go/3. Functions]] (Module 3) | `defer` is deeply tied to function return semantics; named return values and closures interact with defer in ways that require understanding functions first |
| [[go/4. Error Handling]] (Module 4) | The `if v, err := f(); err != nil` pattern from this module is Go's core error-handling idiom; error handling builds directly on the init-statement form of `if` |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[python]] | Module 3: Control Flow | Comparison: Python's `for`/`while`/`if` vs Go's consolidated `for`; Python's `with` statement vs Go's `defer` for resource management |
| [[python]] | Module 1: Variables and Types | Python's string indexing vs Go's range-over-string; both languages iterate differently over Unicode text, and comparing them reinforces the rune vs byte distinction |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Effective Go" section on control structures (https://go.dev/doc/effective_go#control-structures) — covers idiomatic usage but is older; verify it still reflects current best practices
- [ ] Go by Example (https://gobyexample.com) — for, if/else, switch, defer pages — community-maintained; generally accurate but not official
