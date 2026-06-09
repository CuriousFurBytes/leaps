# Resources — Module 3: Functions

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[The Go Programming Language — Chapter 5: Functions (Donovan & Kernighan)](https://www.gopl.io/)** — Addison-Wesley

Chapter 5 of the definitive Go book is the most thorough treatment of Go's function system in print. It covers function declarations, multiple return values, errors, function values, anonymous functions, closures (including the loop-variable pitfall with explicit explanation), variadic functions, deferred function calls, and panic/recover — all the topics in this module, with worked examples. If you buy one Go book, this is it. The book's website (gopl.io) lists errata and the chapter order.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Go Language Specification — Function declarations](https://go.dev/ref/spec#Function_declarations)** — Formal syntax and semantics for function declarations, including parameter lists, result lists, named return values, and variadic parameters. Read alongside the "Function types" and "Function literals" sections for a complete picture.

- **[Go Language Specification — Function literals](https://go.dev/ref/spec#Function_literals)** — The spec section on anonymous functions and closures. Key sentence: "Function literals are closures: they may refer to variables defined in a surrounding function. Those variables are then shared between the surrounding function and the function literal, and they survive as long as they are accessible."

- **[Effective Go — Functions](https://go.dev/doc/effective_go#functions)** — The official idiomatic Go guide. Read the sub-sections: "Multiple return values" (explains the convention and its motivation), "Named result parameters" (explains when named returns help and when they don't), and "Defer" (the trace example is the clearest illustration of defer + named returns modifying return values in the official docs).

- **[The Go Blog — Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)** — Andrew Gerrand's canonical post explaining defer's three rules: (1) deferred function arguments are evaluated when the defer statement executes; (2) deferred functions execute in LIFO order after the surrounding function returns; (3) deferred functions may read and assign to named return values. Rule 3 is the foundation of the error-wrapping pattern in this module.

- **[The Go Blog — First Class Functions in Go](https://go.dev/blog/first-class-functions-in-go-and-new-go)** — Rob Pike's 2011 post demonstrating how first-class functions eliminate the need for certain design patterns (Strategy, Visitor) that require classes in object-oriented languages. Shows function values, closures, and higher-order functions in realistic examples.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 5 (Functions) | The primary resource listed above; covers everything in this module. Sections 5.4 (Errors), 5.6 (Anonymous Functions), 5.8 (Deferred Function Calls) are the most important for this module. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 5 (Functions) | Modern treatment with attention to Go 1.22 changes and idiomatic patterns. Covers function types, closures (including the loop variable discussion), and defer with practical examples from real codebases. Complements Donovan & Kernighan with a more opinionated, best-practices focus. |

---

## Tour of Go Sections

_Interactive exercises directly relevant to this module._

- **[A Tour of Go — Function values (moretypes/24)](https://go.dev/tour/moretypes/24)** — Shows function values assigned to variables and passed as arguments; the first of three Tour pages on closures
- **[A Tour of Go — Function closures (moretypes/25)](https://go.dev/tour/moretypes/25)** — The `adder` closure example; demonstrates shared mutable state across closure calls
- **[A Tour of Go — Closures: fibonacci (moretypes/26)](https://go.dev/tour/moretypes/26)** — Exercise: implement fibonacci as a closure; directly related to Exercise 3 in this module

---

## Package Documentation

_Standard library packages used in this module's examples and exercises._

- **[pkg.go.dev/errors](https://pkg.go.dev/errors)** — The `errors` package: `errors.New`, `errors.Is`, `errors.As`, `errors.Unwrap`. Essential for the error-return idiom. Read the package-level documentation for the rationale behind error wrapping and the `%w` verb.

- **[pkg.go.dev/fmt](https://pkg.go.dev/fmt)** — `fmt.Errorf` with `%w` for error wrapping. The `%w` verb is documented under the "Formatting" section. Also shows that `fmt.Println`, `fmt.Printf`, etc. are themselves variadic: `func Println(a ...any) (n int, err error)`.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/2. Control Flow]] (Module 2) | `defer` was introduced in Module 2; this module completes the picture by showing how deferred closures interact with named return values — the full power of `defer` requires understanding both modules |
| [[go/4. Composite Types]] (Module 4) | Slices and maps are passed to functions by value; the call-by-value discussion in this module is prerequisite to correctly using slices in function parameters |
| [[go/5. Pointers]] (Module 5) | When to use pointer receivers vs value receivers in method signatures builds directly on this module's call-by-value semantics |
| [[go/6. Methods and Interfaces]] (Module 6) | Method values and method expressions extend function values to receiver-bound functions; this module's function-as-value concepts are the prerequisite |
| [[go/8. Error Handling]] (Module 8) | The `(result, error)` convention, `fmt.Errorf` with `%w`, `errors.Is`/`errors.As` — all build on the error-return idiom introduced here |
| [[go/9. Concurrency]] (Module 9) | Goroutines are launched as closures; the loop-variable capture pitfall is critical in concurrent code; higher-order functions appear throughout the concurrency patterns |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] Go by Example — "Closures", "Variadic Functions", "Multiple Return Values" pages (https://gobyexample.com) — community-maintained; generally accurate but not official; good for quick syntax recall
- [ ] "100 Go Mistakes" by Trégarhen — Chapter 5 discusses closures and common function mistakes including loop capture and nil function values; verify the edition covers Go 1.22 changes
