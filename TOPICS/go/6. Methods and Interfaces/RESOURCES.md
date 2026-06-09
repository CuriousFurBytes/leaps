# Resources — Module 6: Methods and Interfaces

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Effective Go — Interfaces and Methods](https://go.dev/doc/effective_go#interfaces_and_types)** — golang.org / go.dev

The official style guide written by the Go authors. The "Interfaces and other types" section covers implicit satisfaction, the Stringer convention, interface conversion, and the design philosophy of keeping interfaces small. This is the single best starting point for understanding not just the mechanics but the idioms — how Go programmers are expected to use interfaces in production code. Read the full interfaces section before doing the exercises.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Language Specification — Interface types](https://go.dev/ref/spec#Interface_types)** — The formal definition of interface types, including method sets, basic interfaces, general interfaces (used in generics), and the rules for interface implementation. The "Method sets" sub-section specifies exactly which methods are in the method set of `T` vs `*T`. Read this when you need a precise answer about what the compiler guarantees.

- **[Go Language Specification — Method declarations](https://go.dev/ref/spec#Method_declarations)** — Defines what a method is, receiver syntax, and the restriction that the receiver type must be a named type in the same package. Also specifies that you cannot add methods to pointer-to-interface types.

- **[Go Tour — Methods and Interfaces](https://go.dev/tour/methods/1)** — Interactive tour (methods/1 through methods/26) covering: method declarations, value vs pointer receivers, interfaces, the nil interface, the empty interface, type assertions, type switches, and standard interfaces (`Stringer`, `error`, `Reader`). Run the examples in-browser. This is the fastest way to see all the mechanics in context.

- **[pkg.go.dev — io package](https://pkg.go.dev/io)** — Documentation for the `io` package including `Reader`, `Writer`, `Closer`, `ReadWriter`, `ReadWriteCloser`, `ReadWriteSeeker`, `Copy`, `ReadAll`, `ReadFull`. Understanding which types in the standard library implement these interfaces makes the "accept interfaces" principle concrete.

- **[pkg.go.dev — fmt package](https://pkg.go.dev/fmt)** — The `Stringer` interface is defined here. The package-level documentation explains which verbs call `String()` and which call `Error()`. Useful when implementing custom string formatting.

- **[pkg.go.dev — sort package](https://pkg.go.dev/sort)** — Documents `sort.Interface` (Len, Less, Swap), `sort.Sort`, `sort.Reverse`, and `sort.Slice`. Reading the full documentation shows how the package is structured around its interface — a clean example of interface-driven design.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 6 (Methods), Ch. 7 (Interfaces) | The definitive treatment. Ch. 6 covers receiver syntax, method sets, method values/expressions, and embedding. Ch. 7 covers interface values, the `(type, value)` pair, nil interfaces, the typed-nil gotcha, `sort.Interface`, `http.Handler`, the `error` interface, type assertions, and type switches. Work through the examples. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 7 (Types, Methods, and Interfaces) | Modern, idiomatic treatment. Particularly strong on the "accept interfaces, return structs" principle, interface pollution, and when NOT to use interfaces. Also covers `any` and its Go 1.18 introduction clearly. |

---

## Practice Sites

_Places to get more practice problems for the specific skills in this module._

- **[A Tour of Go — Methods and Interfaces (go.dev/tour)](https://go.dev/tour/methods/1)** — The tour exercises at the end of the methods/interfaces section include an `Abser` interface, a `Stringer` implementation for `IPAddr`, and an `error` implementation for `ErrNegativeSqrt`. These are short, runnable in-browser, and test the exact skills in this module.

- **[pkg.go.dev — bufio package](https://pkg.go.dev/bufio)** — `bufio.Scanner` and `bufio.Reader` wrap `io.Reader` with buffering. Reading how these types use `io.Reader` internally illustrates the "accept interfaces" pattern at the standard library level. Try implementing a simple `bufio.Scanner`-like type that reads lines from any `io.Reader`.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/5. Pointers]] (Module 5) | Pointer receivers, method sets, and `*T` vs `T` interface satisfaction all depend on understanding pointer semantics from Module 5 |
| [[go/7. Packages and Modules]] (Module 7) | Consumer-side interface definition requires understanding package boundaries and visibility; an interface's method names must be exported (capitalized) to be satisfiable from other packages |
| [[go/8. Error Handling]] (Module 8) | The `error` interface is the single most important interface in Go; all error handling patterns build on the method-set rules and typed-nil behavior explained in this module |
| [[go/15. Reflection and Metaprogramming]] (Module 15) | `reflect.TypeOf` and `reflect.ValueOf` accept `any`; the `(type, value)` pair model of interface values is the exact model that the `reflect` package exposes programmatically |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[concurrency]] | — | Concurrency patterns in Go often use interface-based design: `http.Handler`, `io.Reader` over network connections, `sync.Locker`. Understanding interfaces is prerequisite to idiomatic concurrent Go code |
| [[memory-management]] | — | Interface values have a specific memory layout (two words); understanding this connects to escape analysis — storing a value in an interface often causes it to escape to the heap |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] Go By Example — Interfaces (https://gobyexample.com/interfaces) — community-maintained; covers basic interface satisfaction, needs verification for accuracy on method-set rules
- [ ] "The Laws of Reflection" — Go Blog (https://go.dev/blog/laws-of-reflection) — explains how reflection operates on interface values; forward-looking resource for Module 15; verify it's still accurate for current Go versions
