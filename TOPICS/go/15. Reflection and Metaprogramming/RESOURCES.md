# Resources — Module 15: Reflection and Metaprogramming

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[The Laws of Reflection — The Go Blog](https://go.dev/blog/laws-of-reflection)** — Rob Pike / go.dev

Rob Pike's 2011 post is still the canonical introduction to reflection in Go. It states the three laws clearly with working code examples, explains why `reflect.ValueOf` takes an `interface{}`, and walks through the addressability requirement that trips up most beginners. Read this before writing any reflection code. It is short (under 15 minutes), accurate, and has not aged.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[pkg.go.dev/reflect](https://pkg.go.dev/reflect)** — The complete `reflect` package reference. The package Overview (at the top) is worth reading in full — it summarizes the Laws and key types. Use the function and method list as a lookup reference when writing reflection code. Pay special attention to `Value.CanSet`, `Value.Elem`, `StructField.Tag`, and `StructTag.Lookup`.

- **[Generating code — The Go Blog](https://go.dev/blog/generate)** — Rob Pike's post (2014) on `go generate`: motivation, the directive syntax, and the `stringer` example. Essential reading before the `go generate` exercise. Explains why code generation is preferable to runtime reflection for performance-sensitive or type-safety-critical use cases.

- **[pkg.go.dev/golang.org/x/tools/cmd/stringer](https://pkg.go.dev/golang.org/x/tools/cmd/stringer)** — Reference for the `stringer` tool: flags, usage, and the format of the `//go:generate` directive. Install with `go install golang.org/x/tools/cmd/stringer@latest`.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 12 (Reflection) | The most thorough book treatment of reflection in Go; works through `Display` (a recursive struct pretty-printer), a generic `encode` function, and a token-based decoder — exactly the skills this module builds; read all of Chapter 12 |
| *The Go Programming Language* — Donovan & Kernighan | Ch. 4 (Composite Types), §4.5 (Structs) | Covers struct tags in their natural context; useful as a prerequisite refresher before tackling tag-reading exercises |

---

## Practice Sites

_Places to get more practice problems for the specific skills in this module._

- **[pkg.go.dev/reflect](https://pkg.go.dev/reflect)** — The package examples embedded in the documentation are runnable; work through the `ValueOf`, `TypeOf`, `Indirect`, and `StructTag` examples directly to build muscle memory for the API.

- **[Go Playground (play.golang.org)](https://go.dev/play/)** — The fastest way to experiment with reflection code without setting up a project; useful for verifying addressability rules and tag parsing behavior with short snippets.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/6. Methods and Interfaces]] (Module 6) | Reflection operates on interface values; type assertions are the static counterpart to `reflect.TypeOf` + kind switching; understanding the interface internal representation (type pointer + data pointer) explains the Laws of Reflection |
| [[go/4. Composite Types]] (Module 4) | Struct declarations with field tags are the primary target of reflection; understanding struct embedding matters when iterating fields — embedded fields appear as promoted fields in `NumField`/`Field(i)` |
| [[go/10. Generics]] (Module 10) | Type parameters are the compile-time alternative to reflection for type-parameterized code; comparing both approaches concretely is the primary skill of this module |
| [[go/16. Performance and Profiling]] (Module 16) | Quantifying reflection overhead with `go test -bench` and `pprof`; this module provides the tools to measure whether reflection is actually your bottleneck and to compare reflection vs. generated code |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[memory-management]] | Runtime memory layout | Reflection's addressability rules are a consequence of Go's memory model; understanding stack vs heap allocation explains why some values cannot be addressed |
| [[concurrency]] | Synchronization primitives | `sync.Mutex`, `sync.WaitGroup`, and similar types are common struct fields; understanding how `reflect.DeepEqual` and reflection-based copiers handle them (or deliberately skip them) requires concurrency context |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Effective Go" — reflection section (https://go.dev/doc/effective_go#interface_conversions) — covers type switches and interface conversions adjacent to reflection; verify it covers reflect.Value directly
- [ ] "Go by Example" — reflection page (https://gobyexample.com/reflection) — community-maintained; generally accurate but not official; useful for quick syntax lookup
