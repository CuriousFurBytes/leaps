# Resources — Module 0: Introduction

**Topic:** [[go]]
**Module:** [[modules/go-0-introduction]]

---

> [!NOTE]
> All resources listed here have been verified. URLs marked with `pkg.go.dev` or `go.dev` are official Go documentation and will remain stable. Check the [RESOURCES.md](../RESOURCES.md) at the topic level for a complete, curated list of books, courses, and tools.

---

## Primary Resource

### Official Go Tour

**URL:** [go.dev/tour/welcome/1](https://go.dev/tour/welcome/1)

The interactive Go tour walks you through the language in your browser with runnable code. Complete the "Basics" section before moving to Module 1. The tour covers all the concepts in this module and lets you experiment immediately without installing anything locally.

**Time:** 1–2 hours for the Basics section.

---

## Official Documentation

| Resource | URL | What It Covers |
|----------|-----|---------------|
| Install Go | [go.dev/doc/install](https://go.dev/doc/install) | Platform-specific installation instructions for Windows, macOS, Linux |
| Getting Started | [go.dev/doc/tutorial/getting-started](https://go.dev/doc/tutorial/getting-started) | Hello World walkthrough, go.mod initialization |
| How to Write Go Code | [go.dev/doc/code](https://go.dev/doc/code) | Workspace structure, package organization, running tests |
| Using Go Modules | [go.dev/blog/using-go-modules](https://go.dev/blog/using-go-modules) | Authoritative guide to go.mod, go.sum, and module versioning |
| Effective Go | [go.dev/doc/effective_go](https://go.dev/doc/effective_go) | Idiomatic Go patterns; read the introduction and formatting sections now |

---

## Books

| Book | Author(s) | Relevant Chapter |
|------|-----------|-----------------|
| *The Go Programming Language* | Donovan & Kernighan | Chapter 1: Tutorial — walks through a complete first program |
| *Go in Action* | Kennedy, Ketelsen, St. Martin | Chapter 1: Introducing Go |
| *Learning Go* | Jon Bodner | Chapter 1: Setting Up Your Go Environment |

> [!TIP]
> *The Go Programming Language* (Donovan & Kernighan) is the closest thing to a canonical Go book. Chapter 1 alone is worth reading before or alongside this module.

---

## Tools

| Tool | Purpose |
|------|---------|
| [go.dev/play](https://go.dev/play) | Online Go playground — run Go code without installing anything |
| `go fmt` | Format code (built into Go toolchain) |
| `go vet` | Static analysis for common mistakes (built in) |
| `go doc` | Browse documentation from the terminal: `go doc fmt.Println` |

---

## Cross-Topic Links

- [[go/1. Types and Variables]] — next module; builds directly on workspace/toolchain knowledge from here
- Python — if you're coming from Python, comparison of Python's interpreter model vs Go's compiled model is instructive

---

## Resources to Evaluate

_Not yet verified for quality or accuracy. Check before relying on them._

- [ ] "Go by Example" — practical annotated examples (search for "go by example gobyexample")
- [ ] "Just for Func" YouTube series by Francesc Campoy — Go video tutorials
