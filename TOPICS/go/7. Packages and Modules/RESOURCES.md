# Resources — Module 7: Packages and Modules

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Go Modules Reference (go.dev/ref/mod)](https://go.dev/ref/mod)** — go.dev

The authoritative, comprehensive reference for the entire Go module system. Covers every `go.mod` directive (`module`, `go`, `require`, `replace`, `exclude`, `retract`), version queries, the module proxy and checksum database protocols, `go.sum` semantics, workspace files (`go.work`), and every `go mod` subcommand. Dense but precise. Read the "Overview" and "go.mod files" sections first; use the rest as a reference when you need to understand a specific behavior.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Using Go Modules — Go Blog Series](https://go.dev/blog/using-go-modules)** — A five-part official blog series walking through the full module workflow: Part 1 (introducing modules), Part 2 (migrating to modules), Part 3 (publishing a module), Part 4 (module compatibility and semantic versioning), Part 5 (keeping modules compatible). The most readable introduction to modules in practice. Start here before the reference docs.

- **[How to Write Go Code (go.dev/doc/code)](https://go.dev/doc/code)** — The official tutorial for setting up a module, creating packages, and running the full workflow from source to binary. Read once at the start of this module to see the complete picture before diving into details.

- **[Effective Go — Package Names](https://go.dev/doc/effective_go#package-names)** — The authoritative style guidance on package naming: lowercase, singular, short, no underscores, avoid stutter. Brief but dense; every sentence is actionable.

- **[pkg.go.dev](https://pkg.go.dev)** — The Go package documentation browser. Every public Go module published to the module mirror is indexed here with automatically extracted documentation. Use this to explore any third-party module's API, verify that exports are documented, and see what the community considers good Go documentation.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 10 (Packages) | The best-written prose explanation of Go packages: naming, `init()`, blank imports, internal packages, and the `go` tool. The module system content is dated (written before modules), but everything about packages remains accurate and worth reading. |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 9 (Modules, Packages, and Imports) | Covers the module system as it exists today (modules-first, no GOPATH), including workspaces and practical dependency management. Bodner writes for working developers and includes honest discussion of project layout tradeoffs. |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/6. Methods and Interfaces]] (Module 6) | Exported methods and interface types define the API surface of a package; understanding interfaces is essential to designing package boundaries that are stable and composable |
| [[go/8. Error Handling]] (Module 8) | Exported sentinel errors (`var ErrNotFound`) and custom error types are a key part of every package's public API; error design conventions build directly on the export rules from this module |
| [[go/18. Build, Tooling, and Deployment]] (Module 18) | Build tags, `go generate`, cross-compilation, and the release pipeline all build on the module system established in this module; this is where the full lifecycle from source to shipped binary is covered |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[go/0. Introduction]] | Module 0 | The introduction module covers basic `go build`/`go run` usage and `package main`; this module explains the full system underlying those commands |
| [[go/18. Build, Tooling, and Deployment]] | Module 18 | Build constraints, `go install` with version suffixes, and `go generate` are the continuation of the toolchain story started here |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Organizing a Go module" (go.dev/doc/modules/layout) — official documentation on standard project layouts; verify it is current and covers `cmd/`/`internal/`/`pkg/` conventions
- [ ] Go by Example — Modules page (gobyexample.com/modules) — community-maintained; generally accurate but verify it covers workspaces (go.work), which is newer
