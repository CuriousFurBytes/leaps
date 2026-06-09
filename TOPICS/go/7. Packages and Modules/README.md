# Module 7: Packages and Modules

[← Module 6: Methods and Interfaces](../6.%20Methods%20and%20Interfaces/) | [Topic Home](../README.md) | [Module 8: Error Handling →](../8.%20Error%20Handling/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-blue)
![Time](https://img.shields.io/badge/time-4--5h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [What Is a Package?](#what-is-a-package)
  - [Exported vs Unexported Identifiers](#exported-vs-unexported-identifiers)
  - [Package Naming and Conventions](#package-naming-and-conventions)
  - [Splitting a Package Across Files](#splitting-a-package-across-files)
  - [Package-Level Declarations and init()](#package-level-declarations-and-init)
  - [Import Paths, Aliases, and the Blank Import](#import-paths-aliases-and-the-blank-import)
  - [The Module System — go.mod and go.sum](#the-module-system--gomod-and-gosum)
  - [Semantic Versioning and Semantic Import Versioning](#semantic-versioning-and-semantic-import-versioning)
  - [Key Module Commands](#key-module-commands)
  - [Minimal Version Selection](#minimal-version-selection)
  - [internal/ Packages](#internal-packages)
  - [Vendoring](#vendoring)
  - [Multi-Module Workspaces — go.work](#multi-module-workspaces--gowork)
  - [Standard Project Layout](#standard-project-layout)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Related Concepts](#related-concepts)
- [Exercises](#exercises)
- [Test](#test)
- [Projects](#projects)
- [Further Reading](#further-reading)
- [Learning Journal](#learning-journal)

---

## Overview

This module covers **Go's package and module system**: how Go organizes and encapsulates code, how dependencies are declared and resolved, and how professional Go projects are structured. These mechanisms determine visibility, reusability, and dependency management across every Go project you will ever work on.

By the end of this module, you will understand the difference between a *package* (a unit of code within a directory) and a *module* (a versioned collection of packages with a declared identity). You will know why capitalization is Go's only access-control mechanism, how `go.mod` replaces the old GOPATH workflow, and how to structure a multi-package project that scales without becoming a tangle of imports.

This is prerequisite knowledge for writing any real Go project beyond a single file — which is nearly everything you will do professionally.

**Difficulty:** Intermediate &nbsp;|&nbsp; **Estimated time:** 4–5 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain what a Go package is, why one package maps to one directory, and how multiple files in one directory form a single package — _given a new Go project, decide how to split code into packages and justify the decision_
2. Distinguish exported from unexported identifiers by capitalization and explain the precise visibility rules — _read any Go package's public API from its exported names alone, without reading the implementation_
3. Create a Go module from scratch with `go mod init`, write a `go.mod` file by hand, and explain every directive (`module`, `go`, `require`, `replace`, `exclude`) — _set up a brand-new project or diagnose a broken `go.mod`_
4. Use `go get`, `go mod tidy`, `go mod download`, `go list -m`, and `go mod vendor` correctly — _add, upgrade, downgrade, and remove a dependency without corrupting the module graph_
5. Explain semantic versioning, the `/v2` semantic import versioning rule, and why MVS (minimal version selection) produces builds that are reproducible by default — _read a `require` block and predict exactly which version of each dependency will be compiled_
6. Apply `internal/` packages, multi-module workspaces (`go.work`), and a standard `cmd/` + `internal/` + `pkg/` project layout — _structure a project that enforces encapsulation at the package level_

---

## Prerequisites

### Required Modules

- [[go/6. Methods and Interfaces]] — you need to understand: how Go types, methods, and interfaces work; what it means to export a method vs an unexported method; how the standard library uses interfaces (e.g., `io.Reader`) — because you will import packages that expose interface types
- [[go/0. Introduction]] — you need to understand: `go build`, `go run`, `go fmt`, and basic toolchain usage; `package main` and `func main()` as program entry points

### Required Concepts

- **Directory structure and paths** — Go packages correspond exactly to filesystem directories; understanding how relative and absolute paths work is necessary for understanding import paths
- **Basic types and functions** — package-level `var`, `const`, and `func` declarations are the vocabulary of a package's API; you need to be comfortable reading and writing them
- **Interfaces (conceptual)** — many packages in the standard library and third-party ecosystem are designed around interfaces; you need to know that an interface is a behavioral contract, not an implementation

> [!TIP]
> If you are fuzzy on how `go build` finds source files, or what `package main` means vs `package util`, spend 10 minutes re-reading the introductory module before continuing. The package system builds directly on those fundamentals.

---

## Why This Matters

Every non-trivial Go program is organized into packages. Every Go project that uses a dependency uses the module system. There is no escaping either — understanding packages and modules is not optional knowledge for a working Go developer; it is the foundation on which everything else sits.

Concretely, mastery of this module enables you to:

- **Structure projects that don't become unmaintainable** — a codebase with all logic in `package main` or in a single `utils` package is a codebase that fights you as it grows; understanding package design lets you draw boundaries that keep things understandable
- **Add, update, and remove dependencies confidently** — running `go get` blindly and hoping for the best is not engineering; understanding `go.mod`, `go.sum`, MVS, and `go mod tidy` lets you reason about exactly what version of every dependency gets compiled and why
- **Enforce encapsulation at the package level** — exported vs unexported identifiers and `internal/` packages give you Go's only access-control mechanism; using them correctly is the difference between a package that is easy to evolve and one that accumulates accidental dependencies

Without this module, you will be unable to write multi-package Go programs, add third-party libraries, or structure a real project — all of which appear in the very first real task any Go job requires.

---

## Historical Context

Go's package system has existed since the beginning — packages were part of the initial 2009 design and have never fundamentally changed. The module system, however, is newer and replaced a famously frustrating predecessor.

**The GOPATH era (2009–2018):** In the original Go toolchain, all Go source code had to live inside a single workspace directory defined by the `GOPATH` environment variable (`~/go` by default), under a specific `src/` subtree. A project at `github.com/alice/myapp` literally had to live at `$GOPATH/src/github.com/alice/myapp`. This was workable for small teams but caused real problems: no version pinning (you always got the latest commit of a dependency), no reproducible builds (two machines checking out the same code could end up with different dependency trees), and mandatory GOPATH setup that confused newcomers.

**The module transition (2018–2020):**
- **Go 1.11 (2018)** — `go mod` introduced as an opt-in experiment (`GO111MODULE=on`); projects could now declare their identity and dependencies in `go.mod` files outside GOPATH
- **Go 1.13 (2019)** — modules become the default for projects with a `go.mod`; the `GOPROXY` and module mirror infrastructure launches; `errors.Is`/`errors.As` arrive simultaneously
- **Go 1.16 (2021)** — modules become the *unconditional* default; GOPATH mode is effectively removed for new projects; `go install` requires a version suffix

**Workspaces (2022):**
- **Go 1.18 (2022)** — `go.work` files and `go work` commands arrive, solving the multi-module local development problem that previously required `replace` directives

Understanding this history matters because you will encounter older Go code that uses GOPATH conventions, older blog posts that describe module setup that is no longer required, and `replace` directives in `go.mod` files that are now better handled by `go.work`. Knowing which era a resource comes from saves significant confusion.

---

## Core Concepts

### What Is a Package?

A **package** in Go is the basic unit of code organization and encapsulation. The rules are precise and enforced by the compiler:

1. **One package per directory.** Every `.go` file in a directory must declare the same package name. The directory and the package name are tied together, though they do not need to match (more on this below).
2. **All files in a package share a namespace.** A function defined in `auth.go` and a function defined in `session.go`, both declaring `package user`, can call each other directly — they are in the same package.
3. **Packages are the unit of compilation.** When you `go build`, each package is compiled as a unit. Changed files cause only their package (and packages that import it) to recompile.

```go
// File: math/add.go
package math

// Add returns the sum of a and b.
func Add(a, b int) int {
    return a + b
}
```

```go
// File: math/multiply.go — same package, same directory
package math

// Multiply returns the product of a and b.
func Multiply(a, b int) int {
    return a * b
}
```

```go
// File: main.go — a separate package importing "math"
package main

import (
    "fmt"
    "mymodule/math"  // import path, not just the package name
)

func main() {
    fmt.Println(math.Add(3, 4))      // 7
    fmt.Println(math.Multiply(3, 4)) // 12
}
```

**`package main` is special.** A file declaring `package main` with a `func main()` is an executable entry point. It cannot be imported by other packages. Every other package (a "library package") can be imported but cannot be run directly.

**Documentation comments and `go doc`:** Go's documentation is extracted directly from comments immediately preceding declarations. The comment must start with the name being documented:

```go
// Package math provides basic integer arithmetic operations.
// All functions are safe for concurrent use.
package math

// Add returns the sum of a and b. Both arguments must be non-negative
// for meaningful results.
func Add(a, b int) int {
    return a + b
}
```

```bash
# View package documentation in the terminal
go doc mymodule/math

# View documentation for a specific function
go doc mymodule/math.Add

# View all including unexported identifiers
go doc -all mymodule/math
```

```text
package math // import "mymodule/math"

Package math provides basic integer arithmetic operations.

func Add(a, b int) int
func Multiply(a, b int) int
```

---

### Exported vs Unexported Identifiers

Go's **only access-control mechanism is capitalization**. There is no `public`, `private`, or `protected` keyword.

- **Exported** (visible outside the package): identifier starts with an **uppercase letter** — `Add`, `HTTPClient`, `ErrNotFound`, `Config`
- **Unexported** (visible only within the package): identifier starts with a **lowercase letter** — `add`, `httpClient`, `errNotFound`, `config`

This applies uniformly to: functions, types, variables, constants, struct fields, and interface methods.

```go
package auth

import "errors"

// ErrInvalidCredentials is exported — callers can check for it with errors.Is.
var ErrInvalidCredentials = errors.New("invalid credentials")

// errTooManyAttempts is unexported — it is an internal implementation detail.
var errTooManyAttempts = errors.New("too many login attempts")

// Session holds an authenticated user's session data.
// The struct type is exported, but some fields are unexported.
type Session struct {
    UserID    int    // exported — callers can read and set this
    Token     string // exported — callers need this to make authenticated requests
    csrfToken string // unexported — managed internally; callers should not touch this
    attempts  int    // unexported — internal retry counter
}

// Validate checks whether the session token is still valid.
// Exported — part of the public API.
func (s *Session) Validate() bool {
    return s.Token != "" && s.attempts < 5
}

// resetAttempts resets the internal attempt counter.
// Unexported — only used within this package.
func (s *Session) resetAttempts() {
    s.attempts = 0
}
```

**Visibility is package-wide, not file-wide.** An unexported identifier declared in `auth/session.go` is visible in `auth/token.go` and `auth/middleware.go` — any file in the same package — but not in any other package, even `auth/internal`.

**Struct fields deserve attention:** A struct can be exported while some of its fields are unexported. This is the standard way to provide read access through methods while protecting mutation:

```go
// Counter is an exported type with an unexported field.
type Counter struct {
    n int // callers cannot set this directly
}

// Increment is the only way callers can change n.
func (c *Counter) Increment() { c.n++ }

// Value lets callers read n.
func (c *Counter) Value() int { return c.n }
```

---

### Package Naming Conventions

Go has strong community conventions for package names:

- **Lowercase, single word, no underscores, no camelCase** — `http`, `json`, `os`, `strings`, `sync` (not `httpClient`, `JSON_parser`, `myPackage`)
- **Singular, not plural** — `user` not `users`, `server` not `servers` (the `bytes`, `strings`, `errors` standard packages are the notable exceptions; they are collections of utilities)
- **Short and descriptive** — the package name is the prefix callers type; `http.Get`, not `httputil.HTTPUtilGet`
- **The package name need not match the directory name** — but it should; the convention is that they match, and tooling expects it. The test files' `package foo_test` (external test package) is a common deliberate exception

**Avoid stutter.** If a package is named `user`, its exported type should be `Profile` not `UserProfile` — callers write `user.Profile`, not `user.UserProfile`. The package name already provides the context.

```go
// Good — no stutter
package user

type Profile struct { ... }   // used as user.Profile

// Bad — stutter
package user

type UserProfile struct { ... } // used as user.UserProfile — "user" repeated
```

**Avoid generic names** like `util`, `helpers`, `common`, `misc`. They accumulate unrelated code and provide no information about what they contain. If you find yourself writing `package util`, that is a signal to think harder about what the package actually *does* and name it accordingly.

---

### Splitting a Package Across Files

A package can span any number of `.go` files in the same directory. This is normal and encouraged — large packages are easier to navigate when split into topically coherent files.

```text
user/
  user.go       — type User struct, New(), Validate()
  auth.go       — Login(), Logout(), CheckPermission()
  store.go      — Save(), Load(), Delete() — DB operations
  user_test.go  — tests for the package
```

All four files declare `package user`. They share the same namespace — `store.go` can call `Validate()` defined in `user.go` without any import. The test file `user_test.go` can use `package user` (internal test, sees unexported identifiers) or `package user_test` (external test, sees only exported identifiers — preferred for testing the public API).

**File names have no significance to the compiler.** A file named `store.go` does not need to contain anything related to storage. The file name is only for human readers. By convention, files are named for their primary content, and `_test.go` suffix marks test files.

**Build constraints** can exclude files from a build based on OS, architecture, or custom tags — but that is an advanced topic covered in [[go/18. Build, Tooling, and Deployment]].

---

### Package-Level Declarations and init()

**Package-level declarations** are `var`, `const`, `type`, and `func` declarations outside any function. They are initialized once, in dependency order, when the package is first imported.

```go
package config

import "os"

// Package-level var: initialized once when the package loads.
var DefaultTimeout = 30 // seconds

// Package-level const: compile-time constant.
const Version = "1.4.0"

// Package-level var with initialization expression.
var Hostname, _ = os.Hostname() // _ discards the error
```

**`init()` functions** are special: they run automatically after all package-level variables are initialized, cannot be called manually, and can appear multiple times in a single file (or across files in the same package — each runs in source order). They are used for one-time setup that requires logic, not just an expression.

```go
package db

import (
    "database/sql"
    "log"
    _ "github.com/lib/pq" // blank import: register the postgres driver
)

var db *sql.DB

func init() {
    var err error
    db, err = sql.Open("postgres", "host=localhost dbname=mydb sslmode=disable")
    if err != nil {
        log.Fatalf("init: cannot open db: %v", err)
    }
}
```

**`init()` ordering:** Within a package, `init` functions run in the order the files are presented to the compiler (alphabetical by file name for `go build`). Across packages, `init` functions run after all imported packages have initialized. The full order is: dependency packages initialize before the importing package; within a package, package-level `var` declarations initialize in dependency order, then `init()` functions run.

> [!WARNING]
> **Use `init()` sparingly.** It runs silently, cannot return errors cleanly, makes testing harder (you cannot control initialization order easily), and can cause surprising behavior when a package is imported for the first time deep in a call chain. Prefer explicit initialization functions (`func Setup() error`) that callers call explicitly. Reserve `init()` for registering drivers, codecs, and flags — cases where the side effect *must* happen at import time.

---

### Import Paths, Aliases, and the Blank Import

**Import paths** are the string you write in an `import` statement. They identify a package by its full module path plus any subdirectory:

```go
import (
    "fmt"                          // standard library — no module prefix needed
    "net/http"                     // standard library sub-package
    "github.com/gin-gonic/gin"     // third-party; module path is github.com/gin-gonic/gin
    "mymodule/internal/storage"    // local package within the same module
)
```

The last component of the import path is (conventionally) the package name, which is the identifier you use in code: `http.Get`, `gin.New`, `storage.Save`.

**Import aliases** rename a package for use in the current file — useful when two packages share a name, or when the package name would shadow a local variable:

```go
import (
    "crypto/rand"      // used as rand.Read
    mrand "math/rand"  // used as mrand.Intn — aliased to avoid collision
)
```

```go
import (
    pg "github.com/jackc/pgx/v5"  // alias a verbose name
)

conn, err := pg.Connect(ctx, dsn)
```

**The dot import** merges a package's exported names into the current file's scope — `import . "fmt"` lets you write `Println(...)` instead of `fmt.Println(...)`. It is almost never used in production code because it obscures where names come from.

**The blank import** (`_`) imports a package solely for its side effects (its `init()` function runs, registering drivers, codecs, etc.) without binding any name:

```go
import (
    "database/sql"
    _ "github.com/lib/pq"         // registers the "postgres" driver with database/sql
    _ "github.com/mattn/go-sqlite3" // registers the "sqlite3" driver
)
```

The blank import is one of the few legitimate uses of `init()` in the Go ecosystem — registering implementations into registries that are keyed by string (SQL drivers, image decoders, HTTP handlers).

---

### The Module System — go.mod and go.sum

A **module** is a collection of Go packages with a shared module path and version. Every module is defined by a `go.mod` file at its root. Think of the module as the "project" or "library" — the unit of versioning and distribution.

**Creating a module:**

```bash
# Create a new directory and initialize a module
mkdir myapp && cd myapp
go mod init github.com/alice/myapp
```

```text
# go.mod — the module manifest
module github.com/alice/myapp

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    golang.org/x/crypto v0.17.0
)
```

**Every directive in go.mod explained:**

- `module github.com/alice/myapp` — the module's identity; this is the prefix for all import paths within this module
- `go 1.22` — the minimum Go version required; also gates access to certain language features
- `require` — direct and indirect dependencies with their minimum versions
- `replace` — substitute a module with a different version or a local path (useful for local development; prefer `go.work` for multi-module dev)
- `exclude` — prevent a specific version of a module from being used (rare; used when a version has a known bug)

**go.sum — the integrity database:**

```text
# go.sum — one or two lines per dependency
github.com/gin-gonic/gin v1.9.1 h1:4idEAncQnU5cB7BeOkPtxjfCSye0AAm1R0RVIqJ+Jmg=
github.com/gin-gonic/gin v1.9.1/go.mod h1:hPrL7YrpYKXt5YId3A/Tnip5kqbEAP+KLuI3SUcPTeU=
```

`go.sum` contains the expected cryptographic hashes of every module zip and `go.mod` file your build depends on (directly or transitively). It is a **tamper-evident log**: if a module's content changes on the server (supply chain attack), the hash will not match and the build will fail. You commit `go.sum` to version control. You do not edit it by hand — `go mod tidy` and `go get` maintain it automatically.

**The module proxy and GONOSUMCHECK:** By default, Go fetches modules from `proxy.golang.org` (the Google-operated module mirror) and verifies checksums against `sum.golang.org` (the checksum database). This means `go get` can work even if a repository is temporarily unavailable, and it provides a layer of tamper detection.

---

### Semantic Versioning and Semantic Import Versioning

Go modules use **semantic versioning** (`MAJOR.MINOR.PATCH`):

- `PATCH` bump (v1.0.1 → v1.0.2) — bug fixes, no API changes
- `MINOR` bump (v1.0.0 → v1.1.0) — new features, backward compatible
- `MAJOR` bump (v1.0.0 → v2.0.0) — breaking changes

For versions `v0.x.x` and `v1.x.x`, the module path is unchanged (`github.com/alice/myapp`). For **v2 and above**, Go requires the major version to appear in the module path — this is the **semantic import versioning rule**:

```go
// v1 — module path: github.com/alice/myapp
import "github.com/alice/myapp/client"

// v2 — module path: github.com/alice/myapp/v2
import "github.com/alice/myapp/v2/client"
```

**Why?** Two major versions of a package can coexist in the same build because they have different import paths. A program can import both v1 and v2 of the same module simultaneously — useful during migration. Without the `/v2` suffix, you could not have both in the module graph at the same time.

```go
import (
    clientv1 "github.com/alice/myapp/client"         // v1 API
    clientv2 "github.com/alice/myapp/v2/client"       // v2 API — different path, coexists
)
```

The `go.mod` for v2+ must declare `module github.com/alice/myapp/v2`.

---

### Key Module Commands

```bash
# Add a dependency (fetches and adds to go.mod + go.sum)
go get github.com/gin-gonic/gin@v1.9.1

# Upgrade to latest version of a dependency
go get github.com/gin-gonic/gin@latest

# Upgrade all direct dependencies to their latest minor/patch
go get -u ./...

# Remove unused dependencies and add missing ones
go mod tidy

# Download all dependencies to the local module cache
go mod download

# List all modules in the build, including indirect dependencies
go list -m all

# List a specific module and its available versions
go list -m -versions github.com/gin-gonic/gin

# Print the current module's dependency graph (requires graphviz for visualization)
go mod graph

# Create a vendor directory with all dependencies
go mod vendor

# Verify that dependencies match go.sum hashes
go mod verify
```

```bash
# Practical workflow: adding a new dependency
$ go get github.com/rs/zerolog@latest
go: added github.com/rs/zerolog v1.32.0

$ go mod tidy   # clean up any now-unused entries
$ git add go.mod go.sum
```

---

### Minimal Version Selection

**Minimal Version Selection (MVS)** is the algorithm Go uses to resolve the dependency graph. The key insight: when multiple packages require different versions of the same dependency, Go picks the **minimum version that satisfies all constraints** — not the latest, not the maximum.

Example:

```text
Your module requires:
  A v1.2.0   (which requires C v1.1.0)
  B v1.0.0   (which requires C v1.3.0)

MVS selects C v1.3.0 — the minimum version that satisfies both A and B.
```

MVS guarantees:

1. **Reproducibility**: the same `go.mod` always produces the same build, on any machine, at any time — there is no "latest" floating version
2. **No surprise upgrades**: adding a new dependency cannot silently upgrade an existing dependency
3. **Compatibility by default**: the minimum-satisfying version is the one that was tested against at time of release

This is deliberately different from npm's "semver range" approach, which allows `^1.2.0` to resolve to any compatible version. Go's approach trades flexibility for reproducibility — a deliberate design choice.

---

### internal/ Packages

A directory named `internal` creates a **restricted package** that can only be imported by code in the parent directory tree:

```text
myapp/
  go.mod
  cmd/
    server/
      main.go          — can import myapp/internal/...
  internal/
    storage/
      db.go            — package storage
    auth/
      session.go       — package auth
  api/
    handler.go         — can import myapp/internal/...
```

`myapp/internal/storage` can be imported by `myapp/cmd/server` and `myapp/api`, but **not** by any code outside `myapp/` — including other modules. This makes `internal/` packages a first-class encapsulation tool:

- Implementation details that should never be a public API
- Helper packages shared by multiple packages in your module but that you want to evolve freely
- Preventing accidental external imports of packages you aren't ready to stabilize

```go
// This import is LEGAL — same module, parent of internal/
import "myapp/internal/storage"

// This import FAILS at go build time:
// use of internal package myapp/internal/storage not allowed
import "myapp/internal/storage" // from a different module
```

The `internal/` restriction is enforced by the Go toolchain at build time, not at runtime.

---

### Vendoring

**Vendoring** copies all module dependencies into a `vendor/` directory at the module root. This makes the build fully self-contained — no network, no module proxy, no module cache required:

```bash
# Create or update the vendor directory
go mod vendor

# Build using the vendor directory (required when vendor/ exists and -mod=vendor)
go build -mod=vendor ./...

# Verify that vendor/ is consistent with go.mod and go.sum
go mod verify
```

```text
myapp/
  go.mod
  go.sum
  vendor/
    github.com/gin-gonic/gin/      — source copied here
    modules.txt                    — records which versions are vendored
```

**When to vendor:**

- Corporate environments where the build network cannot reach the internet or a proxy
- Air-gapped deployments
- Audited builds where every line of dependency code must be reviewable

**When not to vendor:**

- Most open-source projects and normal development — the module cache (`$GOPATH/pkg/mod`) already provides caching; vendoring adds size to the repository without benefit

---

### Multi-Module Workspaces — go.work

**`go.work`** (introduced in Go 1.18) solves a common problem: working on two modules simultaneously when one depends on the other. Before workspaces, you had to add a `replace` directive to `go.mod` for local development and remember to remove it before committing.

```bash
# Create a workspace file in the parent directory
go work init ./myapp ./mylib

# Add another module to an existing workspace
go work use ./newservice
```

```text
# go.work
go 1.22

use (
    ./myapp
    ./mylib
)
```

With `go.work` in place, builds inside the workspace automatically use the local version of `mylib` instead of the published version — no `replace` directive needed in `go.mod`. The `go.work` file is typically **not committed to version control** (add it to `.gitignore`); it is a local development convenience.

```bash
# Build with workspace active (automatic when go.work exists)
cd myapp && go build ./...  # uses local mylib

# Disable workspace for a single command
GOWORK=off go build ./...   # uses go.mod's require block instead
```

---

### Standard Project Layout

There is no single official Go project layout, but a widely-adopted community pattern exists. Here it is with honest tradeoffs:

```text
myapp/
  go.mod                     — module declaration
  go.sum                     — dependency hashes
  README.md
  cmd/
    server/
      main.go                — package main for the HTTP server binary
    migrate/
      main.go                — package main for the DB migration tool
  internal/
    user/
      user.go                — core domain logic; cannot be imported externally
      user_test.go
    storage/
      postgres.go
  pkg/
    client/
      client.go              — public API for external consumers of your module
  api/
    v1/
      openapi.yaml           — API contract (if applicable)
```

**`cmd/`** — One subdirectory per binary. Each is `package main`. This pattern scales naturally to multi-binary repositories (a server, a CLI, a migration tool) without ambiguity about which `main.go` builds what.

**`internal/`** — Everything that is an implementation detail. The Go toolchain enforces that nothing outside this module can import these packages. Start here: put almost everything in `internal/` until you have a reason to expose it.

**`pkg/`** — Packages intended to be used by external consumers. This layer is optional and controversial: many Go developers skip `pkg/` entirely and promote packages from `internal/` to the module root only when they're ready to be public. The directory name `pkg/` has no special meaning to the toolchain (unlike `internal/`).

**Tradeoffs:**
- For small projects (one binary, a few thousand lines), this layout is overkill — a flat structure with a few packages is better
- For large projects or libraries with external consumers, the `cmd/internal/pkg` layout pays off quickly
- The standard library itself uses a flat layout with many packages, not this structure — it is an outlier because it is the standard library

---

### How the Concepts Fit Together

```text
Module (go.mod — the project)
        │
        ├─── Package (directory = one package)
        │        │
        │        ├── Exported identifiers (Uppercase) — public API
        │        └── Unexported identifiers (lowercase) — implementation
        │
        ├─── internal/ packages — module-private encapsulation
        │
        ├─── Dependencies (go.mod require + go.sum integrity)
        │        │
        │        └── Resolved by MVS — reproducible, deterministic
        │
        └─── Workspace (go.work — local multi-module dev, not committed)
```

A **module** is the top-level unit. It contains **packages** (one per directory). Each package controls its API surface through **capitalization**. The module's dependencies are declared in **`go.mod`** and locked by **`go.sum`**. The build is reproducible because **MVS** picks deterministic versions. **`internal/`** enforces intra-module encapsulation. **`go.work`** handles local multi-module development without polluting `go.mod`.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Putting everything in `package main` or a `util` package**
>
> The most common structural mistake is writing a large program as a single `package main` file, or extracting "shared" code into a package called `util`, `helpers`, or `common`. Both patterns have the same problem: no meaningful encapsulation, no discoverable API, and a package that accumulates unrelated responsibilities over time.
>
> **Wrong:**
> ```text
> myapp/
>   main.go      — 2000 lines, package main
>   util/
>     util.go    — mix of HTTP helpers, string manipulation, DB queries
> ```
>
> **Right:**
> ```text
> myapp/
>   cmd/server/main.go   — thin entry point only
>   internal/user/       — user domain logic
>   internal/storage/    — persistence layer
>   internal/http/       — HTTP handlers
> ```
>
> **Why this matters:** A `util` package is a growth trap. It starts small and becomes the default dumping ground for anything that doesn't have an obvious home, making it impossible to understand, test, or reuse.

> [!WARNING]
> **Mistake 2: Treating `go.sum` as optional or ignoring it**
>
> Some beginners delete `go.sum` (it looks auto-generated and intimidating) or add it to `.gitignore`. This breaks reproducible builds and defeats supply-chain security.
>
> **Wrong:** `.gitignore` contains `go.sum`
>
> **Right:** Both `go.mod` and `go.sum` are committed to version control. They are not build artifacts — they are part of the project's source of truth. `go.sum` is updated by `go get` and `go mod tidy`; let the tools maintain it, but always commit the result.

> [!WARNING]
> **Mistake 3: Forgetting `go mod tidy` after adding or removing imports**
>
> Running `go get` adds a dependency to `go.mod`, but if you later remove the import from your code, `go.mod` still lists the dependency. Over time this diverges: `go.mod` has dependencies your code doesn't use, or is missing dependencies your code does use.
>
> **Wrong:** Adding `go get` without running `go mod tidy` before committing
>
> **Right:** Run `go mod tidy` before every commit that changes imports. Make it a habit. In CI, add a check: `go mod tidy && git diff --exit-code go.mod go.sum` (fails if tidy would change anything).

> [!WARNING]
> **Mistake 4: Using `replace` directives for local development instead of `go.work`**
>
> Before Go 1.18, the only way to develop two modules simultaneously was a `replace` directive in `go.mod`. Developers sometimes forget to remove this before committing, publishing a module that can never be built by anyone else (because it requires a local path that doesn't exist on their machine).
>
> **Wrong (left in go.mod before commit):**
> ```text
> replace github.com/alice/mylib => ../mylib
> ```
>
> **Right (use go.work instead):**
> ```bash
> go work init ./myapp ./mylib
> ```
> Add `go.work` to `.gitignore`; keep `go.mod` clean.

**Other pitfalls:**

- **Circular imports** — Go prohibits two packages from importing each other. If package A imports package B and package B imports package A, the compiler refuses to build. The fix is to extract the shared dependency into a third package that neither A nor B imports each other through. This is a design signal: the packages have too much mutual knowledge.
- **Naming a package the same as a standard library package** — naming your package `log` or `http` shadows the standard library import. Use distinct, domain-specific names.

---

## Mental Models

### Mental Model 1: Packages as Modules in the OOP Sense

Before Go, "module" or "class" was the unit of encapsulation in most languages. In Go, the **package** is that unit. Think of a package as a class in Java or a module in Python — it has a public API (exported names) and private implementation details (unexported names). The difference is that Go's encapsulation boundary is the package, not the type: all code in the same package shares full visibility, just as methods of the same class do in Java.

This model breaks down at the type level: a Go package can have many types, and they all see each other's unexported fields. This is more permissive than Java's per-class private visibility, and more restrictive than Python's "everything is accessible if you try." It is a deliberate middle ground.

### Mental Model 2: go.mod as a Lock File You Write

In other ecosystems, there is a distinction between a *manifest* (what you declare you need) and a *lock file* (what the resolver computed). Go collapses these: `go.mod` is both the manifest (you write `require` directly) and the resolution (MVS ensures exact versions are recorded). `go.sum` is the integrity check, not the lock.

Think of `go.mod` as the one file that is both `package.json` and `package-lock.json` in the npm world — except that the Go toolchain maintains it for you via `go get` and `go mod tidy`. You rarely write it by hand after `go mod init`.

### Mental Model 3: internal/ as a Firewall

Think of `internal/` as a firewall between your module's internal implementation and its public API surface. Anything behind the firewall (`internal/`) can be changed, renamed, or deleted in any release without concern for external consumers — they literally cannot import it. Anything outside the firewall (`pkg/`, the module root) is part of your public API, and changing it requires a major version bump if breaking.

Starting new projects with everything in `internal/` and promoting packages outward only when they are stable is a low-cost way to avoid premature public API commitments.

> [!NOTE]
> No single mental model is perfect. Use Model 1 (packages as encapsulation units) when designing package boundaries. Use Model 2 (go.mod as managed lock file) when reasoning about dependency changes. Use Model 3 (internal/ as a firewall) when deciding whether a new package should be public or private.

---

## Practical Examples

### Example 1: A Simple Two-Package Module _(Basic)_

**Scenario:** Creating the minimal structure for a module with a library package and a `main` package that uses it.

**Goal:** Demonstrate `go mod init`, a library package with exported and unexported identifiers, and a `main` package importing the library.

```bash
# Create the module structure
mkdir -p greetmod/greeter greetmod/cmd/hello
cd greetmod
go mod init github.com/example/greetmod
```

```go
// File: greeter/greeter.go
package greeter

import "fmt"

// defaultGreeting is unexported — implementation detail.
const defaultGreeting = "Hello"

// Greeter holds the configuration for a greeting.
type Greeter struct {
    Prefix string // exported — callers can customize
    count  int    // unexported — internal use only
}

// New returns a Greeter with the default prefix.
func New() *Greeter {
    return &Greeter{Prefix: defaultGreeting}
}

// Greet returns a formatted greeting for name.
func (g *Greeter) Greet(name string) string {
    g.count++
    return fmt.Sprintf("%s, %s! (call #%d)", g.Prefix, name, g.count)
}

// Count returns the number of greetings issued.
func (g *Greeter) Count() int { return g.count }
```

```go
// File: cmd/hello/main.go
package main

import (
    "fmt"
    "github.com/example/greetmod/greeter"
)

func main() {
    g := greeter.New()
    fmt.Println(g.Greet("Alice"))
    fmt.Println(g.Greet("Bob"))
    fmt.Printf("Total greetings: %d\n", g.Count())
    // g.count        — compile error: g.count is unexported
    // greeter.defaultGreeting — compile error: unexported
}
```

```bash
go run ./cmd/hello/
```

```text
Hello, Alice! (call #1)
Hello, Bob! (call #2)
Total greetings: 2
```

**What to notice:** `g.count` is inaccessible from `main.go` because it is unexported. The compiler enforces this — it is not a runtime check. `greeter.New()` is the only way to create a `Greeter`, which means the `count` field starts at 0 and can only be incremented by `Greet()`. This is the idiomatic Go way to encapsulate state.

---

### Example 2: Adding and Managing a Dependency _(Intermediate)_

**Scenario:** Adding a third-party logging library, using `go get` and `go mod tidy`, and understanding what changes in `go.mod` and `go.sum`.

```bash
# Add the zerolog structured logging library
go get github.com/rs/zerolog@v1.32.0
```

```text
go: added github.com/rs/zerolog v1.32.0
```

```bash
# Inspect go.mod after the addition
cat go.mod
```

```text
module github.com/example/greetmod

go 1.22

require github.com/rs/zerolog v1.32.0
```

```bash
# go.sum now has entries for zerolog and its transitive deps
head -4 go.sum
```

```text
github.com/mattn/go-colorable v0.1.13 h1:8DO...
github.com/rs/zerolog v1.32.0 h1:keLypqis...
github.com/rs/zerolog v1.32.0/go.mod h1:not...
```

```go
// cmd/hello/main.go — updated to use zerolog
package main

import (
    "os"

    "github.com/example/greetmod/greeter"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func main() {
    // Configure zerolog to write human-readable output during development
    log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

    g := greeter.New()
    msg := g.Greet("Alice")
    log.Info().Str("greeting", msg).Int("count", g.Count()).Msg("greeted")
}
```

```bash
go run ./cmd/hello/
```

```text
12:04:05 INF greeted count=1 greeting="Hello, Alice! (call #1)"
```

```bash
# After removing an import from code, clean up go.mod
go mod tidy
# go.mod now only requires what's actually used
```

**What to notice:** `go get` updates both `go.mod` and `go.sum` atomically. Running `go mod tidy` after removing an import removes the dependency from `go.mod` and `go.sum`. The `go.sum` file now contains hashes for zerolog and its transitive dependency `go-colorable` — even though you did not import `go-colorable` directly.

---

### Example 3: internal/ Package Enforcement _(Applied)_

**Scenario:** Demonstrating that `internal/` packages are enforced by the toolchain — you cannot import them from outside the module.

```text
# Directory layout
myapp/
  go.mod          — module github.com/example/myapp
  internal/
    config/
      config.go   — package config (internal)
  api/
    handler.go    — package api (can import internal/config)
```

```go
// internal/config/config.go
package config

// DSN is the database connection string. Internal use only.
// External callers cannot access this — the package is internal.
var DSN = "postgres://localhost/mydb"
```

```go
// api/handler.go — legal: same module, parent of internal/
package api

import "github.com/example/myapp/internal/config"

func DBConn() string {
    return config.DSN // fine
}
```

```go
// Hypothetical code in a DIFFERENT module — this would FAIL to compile:
package external

import "github.com/example/myapp/internal/config" // ERROR
// build error: use of internal package github.com/example/myapp/internal/config not allowed
```

```bash
# From within myapp — this compiles:
go build ./...

# The compiler message for an illegal internal import:
$ go build ./...
../othermodule/main.go:5:2: use of internal package \
  github.com/example/myapp/internal/config not allowed
```

**What to notice:** The error is a compile-time error, not a runtime panic. The toolchain walks the import path and checks whether the importer is within the parent tree of the `internal` directory. There is no way to bypass this at runtime — it is a hard compiler constraint.

---

### Example 4: go.work for Local Multi-Module Development _(Edge Case)_

**Scenario:** You are developing `myapp` and `mylib` simultaneously. `myapp` depends on `mylib`. You want changes to `mylib` to be immediately reflected in `myapp` without publishing a new version.

```text
# Filesystem layout
~/dev/
  mylib/
    go.mod    — module github.com/alice/mylib
    lib.go
  myapp/
    go.mod    — module github.com/alice/myapp, requires github.com/alice/mylib v0.1.0
    main.go
```

```bash
# Create a workspace from the parent directory
cd ~/dev
go work init ./mylib ./myapp
```

```text
# go.work (created in ~/dev/)
go 1.22

use (
    ./mylib
    ./myapp
)
```

```bash
# Build myapp — the workspace makes it use the local ./mylib, not the published version
cd ~/dev/myapp
go build ./...   # uses local mylib automatically

# Verify: without workspace, it would use go.mod's declared version
GOWORK=off go build ./...  # uses published v0.1.0 from go.mod
```

**What to notice:** The `go.work` file is in the *parent* directory of both modules. `myapp/go.mod` is not changed — it still declares `require github.com/alice/mylib v0.1.0`. The workspace transparently overrides this for local builds only. When you push `mylib` changes and publish a new version, you update `require` in `myapp/go.mod` normally. `go.work` never needs to change for that workflow.

---

## Related Concepts

Within this topic:

- [[go/6. Methods and Interfaces]] — exported methods and interface types are the vocabulary of a package's public API; understanding how interfaces work is essential to designing good package boundaries
- [[go/8. Error Handling]] — exported sentinel errors (`var ErrNotFound = errors.New(...)`) and custom error types are a key part of a package's public API; their naming and export conventions are covered in the next module
- [[go/18. Build, Tooling, and Deployment]] — build tags, `go generate`, `go install`, cross-compilation, and the full lifecycle from source to binary build on the module system established here

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Single-Package Module** _(Easy)_
>
> Create a Go module from scratch with `go mod init`. Add a `calculator` package with exported `Add`, `Sub`, `Mul`, `Div` functions and a `package main` that imports and uses them. Verify that unexported helpers are not accessible from `main`.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-single-package-module--easy--1-pt)

The exercises progress from basic package creation to multi-module workspace setup. Complete the Easy and Medium exercises before taking the test.

---

## Test

When you feel ready, take the self-assessment: [TEST.md](./TEST.md)

**Test overview:**
- Section 1: Recall (5 questions, 1 pt each)
- Section 2: Conceptual Understanding (3 questions, 2 pts each)
- Section 3: Applied / Practical (2 questions, 3 pts each)
- Section 4: Scenario / Debugging (1 question, 3 pts)
- Section 5: Discussion (1 question, 2 pts)
- Section 6: Bonus Challenge (1 question, 5 pts bonus)

**Passing:** ≥ 70% of non-bonus points (≥ 15/22). Aim for ≥ 80% (≥ 18/22).

---

## Projects

See the topic-level [PROJECTS.md](../PROJECTS.md) for project ideas.

**Recommended project after this module:**
Multi-Package CLI Tool — build a command-line tool with at least three packages: `cmd/mytool/main.go` (thin entry point), `internal/config` (configuration loading), and `internal/engine` (core business logic). Add one real third-party dependency (e.g., `github.com/spf13/cobra` for CLI parsing or `github.com/rs/zerolog` for logging). Practice `go mod tidy`, review `go.sum`, and use `go doc` to verify your package documentation.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Go Modules Reference (go.dev/ref/mod)](https://go.dev/ref/mod)** — the authoritative, comprehensive reference for everything in the module system: `go.mod` directives, version queries, the module proxy protocol, `go.sum`, workspace files, and every `go mod` subcommand. Read the overview first, then use it as a reference.
2. **[Using Go Modules — Go Blog Series](https://go.dev/blog/using-go-modules)** — a five-part series of official Go blog posts covering the full module workflow from `go mod init` through version management, publishing, and the module mirror. The most readable introduction to modules in practice.
3. **[Effective Go — Package Names](https://go.dev/doc/effective_go#package-names)** — the authoritative Go style guidance on package naming conventions: lowercase, singular, no underscores, avoid stutter. Short but dense with practical guidance.
4. **[How to Write Go Code (go.dev/doc/code)](https://go.dev/doc/code)** — the official tutorial for setting up a module, organizing packages, and the complete workflow from source to runnable program. Best read once, at the start, before diving into the reference docs.
5. **"The Go Programming Language" — Donovan & Kernighan, Chapter 10** — covers packages in depth: the package system, naming, `init`, blank imports, and the `go` tool. The module system content is dated (pre-modules), but the package chapter remains the best written explanation of Go packages.
6. **"Learning Go" — Jon Bodner (2nd ed.), Chapter 9** — covers the module system as it exists today (modules-first, no GOPATH), including workspaces. Bodner's explanations are pitched at working developers and include practical advice on project layout and dependency management.

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 7

**What I covered today:**
- Read the Overview and Why This Matters sections
- Worked through Core Concepts up to (concept name here)

**What clicked:**
- _Something that made sense_

**What's still unclear:**
- _Something that's still fuzzy — add to QUESTIONS.md_

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

**Test score:** _Not taken yet_

---

_Add new entries above this line._
