# Answers — Module 0: Introduction

**Topic:** [[go]]
**Module:** [[modules/go-0-introduction]]

---

> [!WARNING]
> **Do not open this file until you have completed TEST.md.**
> Looking at answers before attempting questions teaches you nothing and gives you a false sense of progress.

---

## Answer Key

### Section 1: Recall (5 × 1 pt = 5 pts)

**1.1** What does `package main` declare, and why is the name `main` special?

> `package main` declares that this file belongs to the `main` package. The name `main` is special because it signals to the Go toolchain that this package should be compiled into an executable binary (not a reusable library). Only packages named `main` can define a `main()` entry-point function that the runtime calls on startup.
>
> **Partial credit (0.5 pt):** Says it is required for executables but does not explain why `main` is special vs any other package name.

---

**1.2** What command runs a Go source file without producing a binary on disk?

> `go run main.go`
>
> `go run` compiles the file to a temporary binary in a system temp directory, executes it, then discards the binary. It is useful for rapid iteration during development. It is equivalent to `go build -o /tmp/... && /tmp/...` but leaves no artifact in the working directory.
>
> **Partial credit (0.5 pt):** Correct command but no explanation of what it does or that no binary is left on disk.

---

**1.3** What does `go fmt` do, and why is it not optional in Go development?

> `go fmt` reformats Go source code to match the official Go style: tabs for indentation, standardized spacing around operators, consistent brace placement. It is not optional in practice because the entire Go community uses it — code that has not been run through `go fmt` is considered poorly formatted, and most CI pipelines will fail if `go fmt` produces any diff. It eliminates all style debates by providing one canonical format.
>
> **Partial credit (0.5 pt):** Describes formatting but does not explain the community/toolchain expectation.

---

**1.4** What is the entry point function in every runnable Go program?

> `func main()` — no parameters, no return value. The complete signature is `func main()`. It must be defined in a file with `package main`. The Go runtime calls `main()` after initializing all packages (running their `init()` functions in dependency order).
>
> **Partial credit (0.5 pt):** Names `main()` but omits the package requirement or the return type (no return).

---

**1.5** What happens at compile time if you import a package but do not use it?

> The Go compiler produces a compile-time error: `imported and not used: "packagename"`. The program will not compile. This is by design: unused imports slow down compilation (every import must be processed) and clutter the dependency graph with packages that contribute nothing.
>
> **Partial credit (0.5 pt):** Says "compile error" but does not explain the rule or the intent.

---

### Section 2: Conceptual Understanding (3 × 2 pts = 6 pts)

**2.1** Why does Go enforce unused import detection at compile time?

> Go enforces unused imports as a compile error for three interconnected reasons:
>
> 1. **Compilation speed:** The Go compiler must parse and type-check every imported package's exported symbols. Unused imports add real compilation cost with zero benefit. Eliminating them guarantees minimal work for the compiler.
>
> 2. **Code hygiene:** Unused imports are dead code. They mislead readers into thinking a package is used when it is not, increase maintenance burden, and can cause confusion during refactoring.
>
> 3. **Dependency minimization:** In Go's module system, each import is a dependency. Unused imports can pull in transitive dependencies, increase binary size, and expand the security surface area—all for nothing.
>
> This reflects Go's design philosophy: if the compiler can enforce a property with zero false negatives (an import is either used or it isn't), it should. Warnings are easy to ignore; errors are not.
>
> **Partial credit (1 pt):** Gives one valid reason. **Full credit (2 pts):** Gives at least two reasons and connects to Go's design philosophy.

---

**2.2** Explain `go.mod` and why it replaced GOPATH.

> `go.mod` is the module definition file introduced in Go 1.11. It records:
> - The module's canonical import path (e.g., `module github.com/user/project`)
> - The minimum supported Go version
> - All direct dependencies with pinned minimum versions (e.g., `require github.com/gorilla/mux v1.8.0`)
>
> **GOPATH limitations it solves:**
>
> 1. **Single version constraint:** GOPATH stored one copy of each dependency globally. Two projects needing different versions of the same library was impossible without hacks.
>
> 2. **Fixed directory layout:** All Go code had to live under `$GOPATH/src/`. This meant your project path was `$GOPATH/src/github.com/you/project` — you couldn't put code wherever you wanted.
>
> 3. **Non-reproducible builds:** `go get` always fetched the latest version. A project built today might have different dependencies than the same project built tomorrow. Modules pin versions in `go.mod` and record checksums in `go.sum`, ensuring reproducible builds.
>
> **Partial credit (1 pt):** Correctly describes `go.mod` but is vague about GOPATH limitations. **Full credit (2 pts):** At least two concrete GOPATH limitations explained.

---

**2.3** Compare Go's compilation speed design goals with C++.

> Go was explicitly designed for fast compilation — this was one of its founding motivations. The Go designers (Ken Thompson, Rob Pike, Robert Griesemer) were frustrated that large C++ codebases at Google took 45+ minutes to compile.
>
> Key design decisions that make Go compile fast:
>
> 1. **No header files:** C++ `#include` causes the preprocessor to re-parse potentially thousands of lines per translation unit. Go packages are compiled once; importing one reads a binary object file, not source.
>
> 2. **Explicit, enforced imports:** Go knows exactly what each file depends on from its import list. The dependency graph is a DAG that the compiler can process in topological order. C++ transitive includes form unpredictable, overlapping dependency webs.
>
> 3. **Simple, unambiguous grammar:** Go's grammar was deliberately kept small. C++ has one of the most complex grammars of any language, making parsing slow and error-prone.
>
> 4. **No circular imports:** Go prohibits circular package dependencies, keeping the dependency graph a tree and enabling parallel compilation.
>
> **Partial credit (1 pt):** Mentions some differences without explaining mechanisms. **Full credit (2 pts):** Explains the mechanism (headers, grammar, dependency resolution) and mentions the historical motivation.

---

### Section 3: Applied / Practical (2 × 3 pts = 6 pts)

**3.1** Write a Go program using a `greet` function.

```go
package main

import "fmt"

func greet(name string) string {
    return fmt.Sprintf("Hello, %s! Welcome to Go.", name)
}

func main() {
    fmt.Println(greet("Alice"))
    fmt.Println(greet("Bob"))
    fmt.Println(greet("Charlie"))
}
```

Expected output:
```
Hello, Alice! Welcome to Go.
Hello, Bob! Welcome to Go.
Hello, Charlie! Welcome to Go.
```

> **Full credit (3 pts):** Correct `package main`, `import "fmt"`, function signature `func greet(name string) string`, uses `fmt.Sprintf`, calls `greet` three times, compiles and produces correct output.
>
> **Partial credit (1.5 pts):** Correct structure but uses `fmt.Printf` inside `greet` (prints instead of returning), or misses the return type, or does not use a separate function.
>
> **No credit (0 pts):** Does not compile, or does not define a separate `greet` function.

---

**3.2** Commands to initialize a Go module and add a dependency.

```bash
# Step 1: Create and enter the project directory
mkdir myapi && cd myapi

# Step 2: Initialize the Go module
go mod init github.com/yourname/myapi
# Creates go.mod:
#   module github.com/yourname/myapi
#   go 1.21

# Step 3: Write your source file (e.g., main.go) — required before go get

# Step 4: Add the external dependency
go get github.com/gorilla/mux
# Downloads the module, adds a 'require' entry to go.mod,
# creates/updates go.sum with cryptographic hashes of the module

# Step 5: Verify the project builds
go build ./...
```

> **Files created:**
> - `go.mod` — module path, Go version, `require` block listing direct dependencies with minimum versions
> - `go.sum` — cryptographic checksums (SHA-256) for every module and version in the dependency graph; ensures reproducible builds and detects tampering or modification of downloaded modules
>
> **Full credit (3 pts):** Correct commands in order, each command explained, both `go.mod` and `go.sum` identified with their roles.
>
> **Partial credit (1.5 pts):** Correct commands but missing explanation of `go.sum`, or misses `go mod init`.

---

### Section 4: Scenario / Debugging (1 × 3 pts = 3 pts)

**4.1** Debug the program that refuses to compile.

> **Two issues:**
>
> **Issue 1 — Unused import `"os"`:** Imported but never used. Compile error: `"os" imported and not used`.
>
> **Issue 2 — Unused variable `number`:** Declared with `:=` but never used. Compile error: `number declared and not used`.
>
> **Why:** Go enforces that every declared variable is used, and every imported package is used. These are compile errors (not warnings) by design, to keep code clean and dependency-minimal.
>
> **Corrected code:**

```go
package main

import "fmt"

func main() {
    message := "Hello, World!"
    number := 42
    fmt.Println(message)
    fmt.Println(number)
}
```

> **Full credit (3 pts):** Identifies BOTH issues (unused import AND unused variable), explains why each is an error (Go's compile-time rules), provides correct compiling code.
>
> **Partial credit (1.5 pts):** Identifies only one of the two issues.
>
> **No credit (0 pts):** Does not identify any compile error, or fix still does not compile.

---

### Section 5: Essay / Discussion (1 × 2 pts = 2 pts)

**5.1** Why make unused variables a compile error?

> **Strong answer (2 pts)** addresses at least two perspectives:
>
> *In favor:*
> - Unused variables are almost always bugs or leftover debugging code. Making them errors catches an entire class of defects at compile time rather than at runtime or code review.
> - In large codebases and teams, stale variables accumulate and mislead readers. Enforcing their removal keeps code intentional and self-documenting.
> - Go provides the blank identifier (`_ = variable`) as an explicit escape hatch for the rare legitimate case of declaring but intentionally not using a value — so the rule does not block valid use cases.
>
> *Against:*
> - During rapid prototyping, having to remove every variable before running slows exploration. (Though `_` mitigates this.)
> - It can be frustrating when incrementally building code — declaring variables for future use is a natural workflow.
>
> *Conclusion:* The rule is widely regarded as correct by experienced Go developers. The escape hatch exists for legitimate needs; the default eliminates a whole class of defects.
>
> **Partial credit (1 pt):** Only one side argued, or a superficial answer without reasoning.

---

### Section 6: Bonus Challenge (1 × 5 pts)

**6.1** Go cross-compilation.

> **How it works:**
>
> Go achieves cross-compilation via two environment variables: `GOOS` (target operating system: `linux`, `windows`, `darwin`, etc.) and `GOARCH` (target CPU architecture: `amd64`, `arm64`, `386`, etc.).
>
> This works because:
> 1. Go includes its own linker — it does not depend on the system's `ld` or `link.exe`
> 2. The Go standard library is implemented in pure Go (and a small amount of Plan-9-style assembly) for each target platform — no C dependencies in the core
> 3. The compiler generates platform-specific machine code entirely within the Go toolchain
>
> Unlike C/C++, no separate cross-compiler toolchain needs to be installed. The Go distribution ships everything needed to target all supported platforms.
>
> **Commands (from macOS ARM64):**

```bash
# Linux AMD64
GOOS=linux GOARCH=amd64 go build -o myapp-linux-amd64 .

# Windows AMD64
GOOS=windows GOARCH=amd64 go build -o myapp-windows-amd64.exe .
```

> **Real-world scenario:** A developer building a CLI deployment tool on an Apple Silicon MacBook needs to ship binaries for Linux servers (x86_64) and Windows developer workstations. With Go, they produce all target binaries from their local machine in seconds — no Docker, no CI matrix, no remote build agents required. Tools like `goreleaser` automate this for release pipelines.
>
> **Full credit (5 pts):** Explains the mechanism (GOOS/GOARCH, self-contained linker, no external toolchain needed), provides correct commands for both platforms, gives a concrete real-world scenario.
>
> **Partial credit (2.5 pts):** Correct commands but incomplete explanation of why Go can cross-compile without a separate toolchain.

---

## Grading Records

<!-- Grading records are appended below by AI agents after each test submission. Do not edit manually. -->
