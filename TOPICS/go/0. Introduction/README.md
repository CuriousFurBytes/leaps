# Module 0: Introduction

← *(First Module)* | [Topic Home](../README.md) | [Next → Types and Variables](../1.%20Types%20and%20Variables/)

![Status](https://img.shields.io/badge/status-Not%20Started-lightgrey)
![Module](https://img.shields.io/badge/module-0%20of%2010-blue)
![Time](https://img.shields.io/badge/time-2--3%20hours-green)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-brightgreen)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Difficulty and Time Estimate](#difficulty-and-time-estimate)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Installing Go](#installing-go)
  - [Hello World](#hello-world)
  - [The Go Workspace: GOPATH vs Modules](#the-go-workspace-gopath-vs-modules)
  - [Essential go Commands](#essential-go-commands)
  - [Go's Philosophy](#gos-philosophy)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Practical Examples](#practical-examples)
- [Module Resources](#module-resources)
- [Further Reading](#further-reading)

---

## Overview

This module is your entry point into Go. By the end, you will have Go installed on your machine, understand the toolchain, have written and run your first Go program, and have a clear picture of what Go is, why it was built, and what problems it solves particularly well.

If you have programmed in another language before, this module will feel approachable — the hello world program is genuinely simple. But do not rush past the toolchain sections. Understanding `go run`, `go build`, `go fmt`, `go vet`, and `go mod init` is not optional background knowledge; these commands are how Go developers actually work every day.

**What you will cover:**
- Installing Go and verifying the installation
- Writing and running a complete Go program
- Anatomy of every line in hello world
- The legacy GOPATH workspace vs the modern module system
- Key go toolchain commands and when to use each
- Go's design philosophy and what it means for how you write code
- Common mistakes that trip up beginners in the first week

---

## Learning Goals

By the end of this module, you will be able to:

1. Install Go 1.21+ (or verify an existing installation) and confirm it with `go version`
2. Write a complete, syntactically correct Go program from scratch
3. Run a Go program with `go run` and build a binary with `go build`
4. Explain what `package main`, `import "fmt"`, and `func main()` each do
5. Initialize a new Go module with `go mod init` and understand what `go.mod` contains
6. Use `go fmt` to format code and `go vet` to find likely bugs
7. Describe Go's design philosophy in your own words
8. Identify at least three common beginner mistakes and how to avoid them

---

## Prerequisites

- **Required:** Comfort with a terminal — you can navigate directories, create files, and run commands
- **Helpful:** Experience with any other programming language — Python, JavaScript, Java, or C all help
- **No Go experience required**

> [!TIP]
> If you are new to the terminal, spend 30 minutes with a "command line basics" tutorial before starting. Go is a compiled language and all its tools are command-line first.

---

## Difficulty and Time Estimate

| Aspect | Value |
|--------|-------|
| **Difficulty** | Beginner |
| **Estimated Time** | 2–3 hours |
| **Time with Exercises** | 3–5 hours |
| **Best Approach** | Type every example by hand — don't copy/paste |

---

## Why This Matters

Go is the language of cloud infrastructure. Docker, Kubernetes, Terraform, Prometheus, CockroachDB, the GitHub CLI, Hugo, and Caddy are all written in Go. When you deploy a container, you are using software written in Go. When you run Kubernetes, you are running Go programs. When your team uses Terraform, that is Go. The language has become load-bearing infrastructure for the modern software industry.

Beyond its ecosystem, Go is worth learning for what it teaches. It forces a discipline that makes codebases maintainable: explicit error handling means you cannot ignore failures; unused imports and variables are compile errors, not warnings; formatting is enforced by the toolchain so code review is never about style. These constraints feel rigid at first and feel liberating once you have worked in a large Go codebase.

Go is also a productive learning environment for understanding how typed, compiled languages work — without the complexity of C++, the weight of Java's ecosystem, or the sharp edges of Rust's borrow checker. It occupies a useful position: compiled, statically typed, and garbage collected, with a small surface area and a toolchain that makes the right thing easy.

---

## Historical Context

Go was conceived on a Tuesday afternoon in September 2007 at Google. The story, as told by Rob Pike, is specific: he and Ken Thompson and Robert Griesemer were waiting for a large C++ program to compile. The build took 45 minutes. During that time, they started sketching on a whiteboard what a new language for systems programming might look like if it addressed the things that frustrated them about C++.

The three designers brought extraordinary pedigree to the project. **Ken Thompson** co-created Unix, co-invented the C programming language, and designed the B language. **Rob Pike** was a colleague of Thompson's at Bell Labs and co-created the Plan 9 operating system, UTF-8 encoding, and the Limbo language. **Robert Griesemer** had worked on the design of the V8 JavaScript engine at Google. This was not a team of newcomers experimenting with language design; it was a team that had already built foundational infrastructure of the computing world.

The frustrations they wanted to address were concrete:

- **Slow compilation:** C++ builds at Google scale took tens of minutes. Go was designed from the start for fast, dependency-clean compilation. A large Go program compiles in seconds.
- **Complexity:** C++ had accumulated features across decades. Go's designers believed that a language's power comes from what it leaves out, not what it includes.
- **Concurrency:** Writing correct concurrent programs in C++ or Java required careful management of threads, locks, and conditions. Go introduced goroutines and channels as first-class language features.
- **Dependency management:** C++ and Java had messy dependency systems. Go modules (introduced later) made this clean.

### Version History Timeline

| Year | Version | Milestone |
|------|---------|-----------|
| 2007 | Pre-release | Language design begins at Google |
| 2009 | Open source | Go released publicly on November 10, 2009 |
| 2012 | 1.0 | Go 1.0 released with the compatibility promise |
| 2015 | 1.5 | Go compiler rewritten entirely in Go (self-hosting) |
| 2018 | 1.11 | Go modules introduced, replacing GOPATH |
| 2019 | 1.13 | Modules become default; improved error wrapping with `%w` |
| 2022 | 1.18 | Generics added (type parameters) — the largest language change since 1.0 |
| 2023 | 1.21 | Built-in min/max/clear; log/slog; slices and maps standard packages |
| 2024 | 1.22 | Range over integers; improved loop variable scoping |

### The Compatibility Promise

When Go 1.0 shipped in March 2012, the team made an unusual commitment: every program written for Go 1.0 would compile and run correctly with every future Go 1.x release. This promise has been kept for over a decade. Code written in 2012 compiles today. In a world where Python 2 to 3 took a decade and Node.js regularly breaks APIs, this stability is a meaningful advantage for production systems and a statement of values.

---

## Core Concepts

### Installing Go

**Verify an existing installation:**

```bash
go version
```

Expected output (version will vary):
```
go version go1.21.5 linux/amd64
```

If you see this, you are ready. If you get `command not found`, Go is not installed or not on your PATH.

**Installation:**

- **Linux**: Download the tarball from `go.dev/dl/` and follow the installation instructions, or use your distribution's package manager (`sudo apt install golang-go` on Debian/Ubuntu — note this may be an older version).
- **macOS**: Use Homebrew (`brew install go`) or download from `go.dev/dl/`.
- **Windows**: Download the MSI installer from `go.dev/dl/` — it sets the PATH automatically.

**After installation, verify everything is working:**

```bash
go version          # prints Go version
go env GOPATH       # prints the GOPATH directory
go env GOROOT       # prints where Go is installed
```

> [!NOTE]
> Install Go 1.18 or later to have access to generics. Install Go 1.21+ to have access to the `log/slog`, `slices`, and `maps` standard library packages used in later modules.

---

### Hello World

Create a directory for your first program and a file named `main.go`:

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

Run it:

```bash
go run main.go
```

Output:
```
Hello, World!
```

That is a complete, working Go program. Now let us look at every single line.

#### Line-by-line anatomy

**`package main`**

Every Go source file begins with a `package` declaration. Go source code is organized into packages — the fundamental unit of code organization. The name `main` is special: it tells the Go compiler that this package is an executable program (as opposed to a library). If you use any other package name, the compiler produces a library, not a runnable binary. There must be exactly one `package main` in your program, and it must contain a `func main()`.

**`import "fmt"`**

The `import` statement brings in a package from the standard library or an external module. `"fmt"` is the formatting package — it provides functions for formatted I/O, including `Println`, `Printf`, `Sprintf`, and `Errorf`. The string `"fmt"` is the package's import path. Every import you add must be used — if you import a package and do not call anything from it, the program will not compile. This is an intentional design decision; unused imports are dead code, and Go refuses to compile dead code.

**`func main()`**

This is the entry point of every Go program. When you run a Go binary, execution begins here. It takes no arguments and returns nothing — if you need command-line arguments, you use `os.Args` or the `flag` package inside `main`. If you need to signal failure, you call `os.Exit(1)`. Every runnable Go program must have exactly one `func main()` in `package main`.

**`fmt.Println("Hello, World!")`**

`fmt.Println` writes its arguments to standard output followed by a newline. The `fmt` prefix is the package name; `Println` is the function. In Go, exported identifiers (callable from other packages) always start with a capital letter. `Println` is exported; if it were `println` it would be package-private. The argument `"Hello, World!"` is a string literal.

**The curly braces and indentation**

Go uses curly braces for all blocks (functions, if statements, loops). The opening brace must be on the same line as the statement that opens it — `func main() {` is correct; putting `{` on the next line is a syntax error. Go uses tabs for indentation. You do not need to think about this manually: `go fmt` enforces it automatically.

#### Building a binary

```bash
go build -o hello .
./hello
```

`go build` compiles the package in the current directory and produces a binary named `hello`. The `.` means "the package in the current directory." The resulting binary has no external dependencies and can be copied to any machine with the same operating system and architecture.

---

### The Go Workspace: GOPATH vs Modules

Understanding the shift from GOPATH to modules is important because you will encounter both in documentation, Stack Overflow answers, and legacy codebases.

#### The old way: GOPATH

Before Go 1.11, all Go code had to live inside a directory structure rooted at `$GOPATH` (typically `~/go`). Your code lived at `$GOPATH/src/github.com/yourname/yourproject`. Dependencies were fetched into `$GOPATH/src` too. There was no version pinning — if two projects needed different versions of the same library, it was a problem with no clean solution. This model was workable for a single developer but created real pain at team and organizational scale.

#### The modern way: Go modules

Go 1.11 introduced modules; they became the default in Go 1.16. A **module** is a collection of Go packages with a shared version identity, defined by a `go.mod` file at the root of the module directory. With modules, your code can live anywhere on the filesystem. Dependencies are versioned and recorded in `go.mod` and `go.sum`.

**Creating a new module:**

```bash
mkdir myproject
cd myproject
go mod init github.com/yourname/myproject
```

This creates `go.mod`:

```
module github.com/yourname/myproject

go 1.21
```

The module path (`github.com/yourname/myproject`) is how other modules refer to your packages. It does not have to be a GitHub URL — it just has to be unique. For local experiments, `example.com/myproject` is conventional.

**After adding an external dependency:**

```bash
go get github.com/spf13/cobra@v1.8.0
```

This updates `go.mod` to add the dependency and `go.sum` to record the cryptographic hashes of the downloaded modules. The `go.sum` file is checked into version control alongside `go.mod` and provides security: if the module contents change, the hash won't match and Go will refuse to use it.

**What you need to know right now:** for every new Go project you start, run `go mod init <module-path>` first. Everything else follows from that.

---

### Essential go Commands

The Go toolchain ships as a single `go` binary with many subcommands. These are the ones you will use every day:

#### `go run`

Compiles and immediately runs a Go program without leaving a binary behind. Useful during development when you want to test changes quickly.

```bash
go run main.go          # run a single file
go run .                # run the package in the current directory
go run ./cmd/server     # run the package in ./cmd/server
```

#### `go build`

Compiles the package and produces a binary. The binary can be distributed and run without the Go toolchain installed.

```bash
go build .                          # build current package; output is package name
go build -o myapp .                 # build with explicit output name
go build ./...                      # build all packages in the module
GOOS=linux GOARCH=amd64 go build .  # cross-compile for Linux/AMD64
```

#### `go fmt`

Formats all Go source files in a package according to the official Go style. This is not optional style guidance — it is the single canonical format, enforced by the tool. `go fmt` removes all style debates from code review. Run it before every commit.

```bash
go fmt ./...    # format all packages in the module
```

#### `go vet`

Runs a static analyzer that catches common mistakes: calling `fmt.Printf` with the wrong number of arguments, comparing a function to nil instead of calling it, unreachable code, and more. Not a linter — these are things that are almost certainly wrong.

```bash
go vet ./...    # vet all packages in the module
```

#### `go test`

Runs all test functions in a package. Tests live in `_test.go` files in the same package. Test functions are named `TestXxx(t *testing.T)`.

```bash
go test ./...              # run all tests
go test -v ./...           # verbose output
go test -run TestMyFunc .  # run a specific test
go test -race ./...        # run with the data race detector
```

#### `go mod init`

Initializes a new Go module in the current directory by creating a `go.mod` file.

```bash
go mod init github.com/yourname/projectname
```

#### `go mod tidy`

Adds any missing module requirements to `go.mod` and removes unused ones. Run after adding or removing imports.

```bash
go mod tidy
```

#### `go get`

Adds or updates a dependency.

```bash
go get github.com/spf13/cobra@v1.8.0    # specific version
go get github.com/spf13/cobra@latest    # latest version
```

#### `go doc`

Shows documentation for a package, function, or type without opening a browser.

```bash
go doc fmt
go doc fmt.Println
go doc net/http.Request
```

---

### Go's Philosophy

Go's design philosophy can be distilled into a handful of principles, each of which has direct consequences for how you write code. Understanding these principles helps you understand why Go makes the choices it does — and helps you write Go that other Go developers will find readable and maintainable.

#### Simplicity over features

Go deliberately omits features found in other popular languages. There is no inheritance. There were no generics until 2022. There are no exceptions. There is no function overloading. There is no operator overloading. There is no implicit type conversion.

This is not an accident or a limitation of the designers' skill. These omissions are intentional and principled. The Go team's view is that feature richness comes with a cost: every feature adds to the cognitive load of reading code, the surface area for misuse, and the complexity of the compiler. A smaller language is a more readable language. When all Go code is written with the same small set of tools, reading unfamiliar Go code is much faster than reading unfamiliar C++ or Scala.

The Go specification can be read in an afternoon. This is a design goal, not an accident.

#### Explicit over implicit

Go prefers that things be stated directly rather than inferred or implied. Errors are returned as values from functions — callers must explicitly handle or propagate them; they cannot silently be swallowed by an exception handler somewhere up the call stack. Type conversions must be explicit — `int(myFloat)` not implicit coercion. Unused imports are errors, not silently ignored. Exported identifiers begin with capital letters — visibility is explicit in the name itself.

This explicitness makes Go code easier to read and reason about. When you see a function call, you know exactly what it does with errors because the code tells you. When you see an import, you know it is used. When you see an identifier beginning with a capital letter, you know it is accessible from outside the package.

#### Composition over inheritance

Go has no inheritance hierarchy. Instead, it has interfaces and embedding. An interface is a set of method signatures; any type that implements all the methods in an interface satisfies it implicitly — no declaration required. This is structural (or duck) typing: if it has an `Area()` method that returns `float64`, it is a `Shape`, whether or not you said so.

This approach avoids the fragile base class problem that plagues deep inheritance hierarchies in Java or C++. It encourages small, focused interfaces. The standard library defines `io.Reader` as a single method (`Read(p []byte) (n int, err error)`), and this single-method interface is implemented by dozens of types in the standard library and thousands more in third-party code. Large inheritance hierarchies accrete; small interfaces compose.

#### Fast compilation as a first-class requirement

Go was designed from the beginning for fast compilation. The import system is clean: each package lists exactly what it imports, and there are no transitive or circular imports. The compiler is designed to be parallelizable. The result is that a large Go codebase compiles in seconds, not minutes. This is not a small thing — fast compilation changes how you develop. You can run the compiler on every save instead of every few minutes, which tightens the feedback loop considerably.

#### Concurrency built into the language

Most languages treat concurrency as a library concern — you reach for threads, futures, or async/await provided by the standard library or third-party packages. Go bakes concurrency into the language itself with two primitives: goroutines and channels. A goroutine is a lightweight concurrent function started with the `go` keyword. A channel is a typed queue for communicating between goroutines. You will study these in Module 9, but it is worth knowing from the beginning that Go's concurrency model is why it is the language of choice for network servers and distributed systems.

---

## Common Beginner Mistakes

> [!WARNING]
> **Importing a package you don't use**
> If you add an import and do not call anything from it, the compiler refuses to compile:
> ```
> ./main.go:5:2: "fmt" imported and not used
> ```
> This is intentional — unused imports are dead code. Either use the package or remove the import. To import a package only for its `init()` side effects, use the blank import: `import _ "net/http/pprof"`.

> [!WARNING]
> **Declaring a variable you don't use**
> Similarly, if you declare a local variable with `:=` and never read its value, the compiler refuses:
> ```
> ./main.go:8:2: x declared and not used
> ```
> Use `_` to discard values you must receive but don't need: `_, err := strconv.Atoi("42")`.

> [!WARNING]
> **Forgetting `package main` or naming it wrong**
> Every file must start with a package declaration. If you want a runnable program, the package must be `main`. A file named `main.go` with `package hello` will not produce an executable — it will be treated as a library package named `hello`.

> [!WARNING]
> **Putting the opening brace on a new line**
> In Go, the opening brace of any block must be on the same line as the statement that opens it. This is a Go syntax rule (related to automatic semicolon insertion). The following is a syntax error:
> ```go
> func main()
> {    // syntax error: unexpected semicolon or newline before {
>     fmt.Println("hello")
> }
> ```
> `go fmt` will enforce the correct placement automatically.

---

## Practical Examples

### Example 1: Hello World with Explanation

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

Run with: `go run main.go`

### Example 2: Greeting with a Function

A slightly more complex program that demonstrates functions, string arguments, and calling `fmt.Printf` for formatted output:

```go
package main

import "fmt"

// greet prints a personalized greeting.
// In Go, functions are declared with 'func', then name, parameters, return type.
func greet(name string) {
	fmt.Printf("Hello, %s! Welcome to Go.\n", name)
}

func main() {
	greet("Alice")
	greet("Bob")
	greet("Charlie")
}
```

Output:
```
Hello, Alice! Welcome to Go.
Hello, Bob! Welcome to Go.
Hello, Charlie! Welcome to Go.
```

Key observations:
- `func greet(name string)` declares a function taking one `string` parameter and returning nothing
- `fmt.Printf` uses format verbs: `%s` means "insert a string here"; `\n` is a newline
- Comments begin with `//` and can appear on their own line or at the end of a line

### Example 3: Simple Calculator

A program demonstrating variables, type conversion, and basic arithmetic:

```go
package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	// os.Args contains command-line arguments.
	// os.Args[0] is the program name; os.Args[1], [2], ... are the arguments.
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "Usage: calc <number1> <number2>")
		os.Exit(1)
	}

	a, err := strconv.ParseFloat(os.Args[1], 64)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid number: %s\n", os.Args[1])
		os.Exit(1)
	}

	b, err := strconv.ParseFloat(os.Args[2], 64)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid number: %s\n", os.Args[2])
		os.Exit(1)
	}

	fmt.Printf("%g + %g = %g\n", a, b, a+b)
	fmt.Printf("%g - %g = %g\n", a, b, a-b)
	fmt.Printf("%g * %g = %g\n", a, b, a*b)
	if b != 0 {
		fmt.Printf("%g / %g = %g\n", a, b, a/b)
	} else {
		fmt.Fprintln(os.Stderr, "Division by zero")
	}
}
```

Run with: `go run main.go 10 3`

Output:
```
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335
```

Key observations:
- Multiple imports use a parenthesized block: `import ( ... )`
- `strconv.ParseFloat` converts a string to a float64; it returns the value and an error
- `err != nil` is the idiomatic Go way to check for errors — you will write this thousands of times
- `os.Exit(1)` exits with a non-zero status code, signaling failure to the shell
- `fmt.Fprintln(os.Stderr, ...)` writes to standard error (not standard output)

### Example 4: Print Go Version via runtime Package

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("Go version:", runtime.Version())
	fmt.Println("OS:", runtime.GOOS)
	fmt.Println("Architecture:", runtime.GOARCH)
	fmt.Println("CPUs:", runtime.NumCPU())
}
```

The `runtime` package provides information about the running Go program and the execution environment. `runtime.Version()` returns the Go version string (e.g., `"go1.21.5"`).

---

## Module Resources

| Resource | Link |
|----------|------|
| Exercises | [EXERCISES.md](./EXERCISES.md) |
| Test | [TEST.md](./TEST.md) |
| Questions | [QUESTIONS.md](./QUESTIONS.md) |
| Notes | [NOTES.md](./NOTES.md) |
| Answers | [ANSWERS.md](./ANSWERS.md) |
| Resources | [RESOURCES.md](./RESOURCES.md) |

---

## Further Reading

- [go.dev/doc/install](https://go.dev/doc/install) — Official installation guide for all platforms
- [go.dev/tour](https://go.dev/tour/) — The official interactive Go tour, runs in the browser
- [go.dev/blog/using-go-modules](https://go.dev/blog/using-go-modules) — The definitive explanation of how Go modules work
- [go.dev/doc/effective_go](https://go.dev/doc/effective_go) — Canonical idiomatic Go patterns (skim now, study in depth after Module 4)
- *The Go Programming Language* by Donovan & Kernighan — Chapter 1 covers the material in this module with more depth

---

## Cross-Links

- Python — Python comparison: `print("hello")` vs `fmt.Println("hello")`; both interpreted-style ease, very different execution model
- [[rust]] — Rust comparison: both compiled, statically typed; Rust optimizes for safety at the cost of complexity, Go optimizes for simplicity
- [[go/1. Types and Variables]] — Next module: variables, types, zero values, and constants

---

*Module 0 of 10 — Go Topic*
