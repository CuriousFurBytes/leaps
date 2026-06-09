# Exercises — Module 7: Packages and Modules

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just think through it — actually create the directories and files.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Expert | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Single-Package Module [🟢 Easy] [1 pt]

### Context
The most fundamental Go project structure is a module containing a single library package and one `package main` that uses it. This exercise practices `go mod init`, package declaration, and the exported/unexported distinction.

### Task
Create a new Go module `github.com/example/calc` with the following structure:

```text
calc/
  go.mod
  calculator/
    calculator.go   — package calculator
  cmd/calc/
    main.go         — package main
```

`calculator.go` must define:
- Exported functions: `Add(a, b int) int`, `Sub(a, b int) int`, `Mul(a, b int) int`, `Div(a, b float64) float64`
- An unexported helper `validate(a, b float64) bool` that returns false if b is zero (used by Div)

`main.go` must import `github.com/example/calc/calculator` and call all four functions, printing the results.

### Requirements
- [ ] `go.mod` exists with `module github.com/example/calc` and `go 1.22`
- [ ] `Add`, `Sub`, `Mul`, `Div` are exported (uppercase)
- [ ] `validate` is unexported (lowercase) and is only used within the `calculator` package
- [ ] `main.go` cannot reference `validate` directly (compile error if attempted)
- [ ] `go run ./cmd/calc/` produces correct output

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Create the structure with:
```bash
mkdir -p calc/calculator calc/cmd/calc
cd calc
go mod init github.com/example/calc
```
Then create the source files. `go mod init` creates `go.mod` for you.

</details>

<details>
<summary>Hint 2 (if structure is right but compile fails)</summary>

The import path in `main.go` must use the full module path, not just the directory name:
```go
import "github.com/example/calc/calculator"
```
You then use the package with its name: `calculator.Add(3, 4)`.

</details>

### Expected Output / Acceptance Criteria
```text
Add(10, 3) = 13
Sub(10, 3) = 7
Mul(10, 3) = 30
Div(10, 3) = 3.3333333333333335
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```bash
mkdir -p calc/calculator calc/cmd/calc && cd calc
go mod init github.com/example/calc
```

```go
// calculator/calculator.go
package calculator

// validate returns false if b is zero, preventing division by zero.
func validate(a, b float64) bool {
    return b != 0
}

// Add returns the sum of a and b.
func Add(a, b int) int { return a + b }

// Sub returns the difference a - b.
func Sub(a, b int) int { return a - b }

// Mul returns the product of a and b.
func Mul(a, b int) int { return a * b }

// Div returns a / b. Returns 0 if b is zero.
func Div(a, b float64) float64 {
    if !validate(a, b) {
        return 0
    }
    return a / b
}
```

```go
// cmd/calc/main.go
package main

import (
    "fmt"
    "github.com/example/calc/calculator"
)

func main() {
    fmt.Printf("Add(10, 3) = %d\n", calculator.Add(10, 3))
    fmt.Printf("Sub(10, 3) = %d\n", calculator.Sub(10, 3))
    fmt.Printf("Mul(10, 3) = %d\n", calculator.Mul(10, 3))
    fmt.Printf("Div(10, 3) = %g\n", calculator.Div(10, 3))
}
```

**Explanation:** `validate` is lowercase, so `main.go` cannot call it directly — any attempt gives a compile error. The full module path `github.com/example/calc/calculator` is the import path; `calculator` (the last component) is the name used in code. `go mod init` only needs to be run once per module.

</details>

---

## Exercise 2: Export Rules — Reading a Package's API [🟢 Easy] [1 pt]

### Context
A core skill in Go is being able to read any package and immediately know its public API just from capitalization — without reading the implementation. This exercise tests that skill.

### Task
Given the following Go file (do not run it — read it), list:
1. Every identifier that is exported (visible to other packages)
2. Every identifier that is unexported (package-private only)
3. What the public API of this package is — what callers can do with it

```go
package cache

import (
    "sync"
    "time"
)

const defaultTTL = 60 // seconds

var ErrNotFound = errors.New("key not found")

type entry struct {
    value   interface{}
    expires time.Time
}

type Cache struct {
    mu      sync.Mutex
    data    map[string]entry
    MaxSize int
}

func New(maxSize int) *Cache {
    return &Cache{
        data:    make(map[string]entry),
        MaxSize: maxSize,
    }
}

func (c *Cache) Set(key string, value interface{}, ttl time.Duration) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = entry{value: value, expires: time.Now().Add(ttl)}
}

func (c *Cache) Get(key string) (interface{}, error) {
    c.mu.Lock()
    defer c.mu.Unlock()
    e, ok := c.data[key]
    if !ok || time.Now().After(e.expires) {
        return nil, ErrNotFound
    }
    return e.value, nil
}

func (c *Cache) evict() {
    // removes expired entries — internal housekeeping
}
```

### Requirements
- [ ] Correctly list all exported identifiers (at least 5)
- [ ] Correctly list all unexported identifiers (at least 4)
- [ ] Describe the public API in one sentence

### Expected Output / Acceptance Criteria

**Exported (public):**
- `ErrNotFound` (var)
- `Cache` (type)
- `Cache.MaxSize` (struct field)
- `New` (function)
- `Cache.Set` (method)
- `Cache.Get` (method)

**Unexported (package-private):**
- `defaultTTL` (const)
- `entry` (type)
- `entry.value` (field)
- `entry.expires` (field)
- `Cache.mu` (field)
- `Cache.data` (field)
- `Cache.evict` (method)

**Public API summary:** The `cache` package provides a thread-safe, TTL-based in-memory cache; callers create one with `New`, store values with `Set`, retrieve them with `Get` (which returns `ErrNotFound` for missing/expired keys), and may check `MaxSize`.

### Solution
<details>
<summary>Show Solution</summary>

The analysis above is the complete solution. The key observation: `Cache` is exported (callers can create and use it), but `mu` and `data` are unexported (callers cannot directly manipulate the lock or the underlying map — they must use `Set` and `Get`). This prevents callers from corrupting the cache's invariants. The `entry` type being unexported means callers never see the internal representation — the cache can change its storage format without breaking callers.

**Why `ErrNotFound` is exported:** Callers need to check for it with `errors.Is(err, cache.ErrNotFound)`. If it were unexported, callers could not distinguish "not found" from any other error. Sentinel error values must be exported to be checkable.

**Common wrong answer:** Listing `MaxSize` as unexported because it's a field. Fields follow the same rule — uppercase first letter = exported. `MaxSize` starts with `M` (uppercase), so it is exported and callers can read and set it.

</details>

---

## Exercise 3: Creating a go.mod with a Real Dependency [🟡 Medium] [2 pts]

### Context
The most common day-to-day module workflow is: create a module, add a dependency, write code that uses it, and verify the `go.mod` and `go.sum` are correct. This exercise practices that full cycle.

### Task
Create a Go module `github.com/example/logger` that:
1. Initializes the module with `go mod init`
2. Adds `github.com/rs/zerolog` as a dependency using `go get`
3. Creates a `cmd/log/main.go` that uses `zerolog` to log one `Info` message and one `Error` message with at least one structured field each
4. Runs `go mod tidy` and commits (or verifies) that `go.mod` and `go.sum` are consistent

### Requirements
- [ ] `go.mod` contains `module github.com/example/logger` and a `require` entry for `github.com/rs/zerolog`
- [ ] `go.sum` exists and is non-empty
- [ ] The program compiles and runs with `go run ./cmd/log/`
- [ ] The Info message includes at least one structured key-value field (e.g., `Str("component", "main")`)
- [ ] The Error message includes at least one structured field and a message string
- [ ] Running `go mod tidy` after the code is written produces no changes to `go.mod` or `go.sum`

### Hints
<details>
<summary>Hint 1 (workflow hint)</summary>

```bash
mkdir logger && cd logger
go mod init github.com/example/logger
mkdir -p cmd/log
go get github.com/rs/zerolog@latest
# write cmd/log/main.go
go mod tidy
go run ./cmd/log/
```

</details>

<details>
<summary>Hint 2 (zerolog usage hint)</summary>

```go
import (
    "os"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

// Configure human-readable console output:
log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stdout})

// Info with a field:
log.Info().Str("component", "main").Msg("started")

// Error with a field:
log.Error().Str("op", "startup").Msg("something went wrong")
```

</details>

### Expected Output / Acceptance Criteria
Output will resemble (exact format depends on zerolog version and console writer configuration):
```text
12:00:00 INF started component=main
12:00:00 ERR something went wrong op=startup
```

The key criterion is that `go.mod` has a `require` entry for `zerolog` and `go.sum` is present and non-empty.

### Solution
<details>
<summary>Show Solution</summary>

```bash
mkdir logger && cd logger
go mod init github.com/example/logger
mkdir -p cmd/log
go get github.com/rs/zerolog@latest
```

```go
// cmd/log/main.go
package main

import (
    "os"

    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func main() {
    // Human-readable output for local development
    log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stdout})

    // Info log with a structured field
    log.Info().
        Str("component", "main").
        Int("pid", os.Getpid()).
        Msg("application started")

    // Error log with a structured field (simulated error)
    log.Error().
        Str("op", "database_connect").
        Str("host", "localhost").
        Msg("connection refused")
}
```

```bash
go mod tidy
go run ./cmd/log/
```

**Explanation:** `go get` adds `zerolog` to `go.mod` and records its hash in `go.sum`. `go mod tidy` removes any dependencies that ended up in `go.mod` but are not actually imported. After tidy, running `git diff go.mod go.sum` should show no changes — the two files are consistent with the actual imports.

</details>

---

## Exercise 4: internal/ Package Enforcement [🟡 Medium] [2 pts]

### Context
The `internal/` directory is Go's first-class mechanism for package-level encapsulation. The toolchain enforces it — it is not just a convention. This exercise demonstrates that the compiler actually refuses to build code that violates the `internal/` boundary.

### Task
Create a module `github.com/example/internal-demo` with this structure:

```text
internal-demo/
  go.mod
  internal/
    secrets/
      secrets.go    — package secrets; exports SecretKey string
  cmd/app/
    main.go         — LEGAL: same module, imports internal/secrets
  cmd/cheat/
    main.go         — attempt to import from a DIFFERENT module (simulate this)
```

1. Write `internal/secrets/secrets.go` with an exported `var SecretKey = "s3cr3t"`
2. Write `cmd/app/main.go` that successfully imports and prints `secrets.SecretKey`
3. Run `go build ./...` and confirm it succeeds
4. Create a *separate* module `github.com/example/outsider` in a sibling directory that tries to import `github.com/example/internal-demo/internal/secrets`
5. Run `go build ./...` inside the outsider module and confirm the compiler error

### Requirements
- [ ] The in-module import (`cmd/app`) compiles successfully
- [ ] The cross-module import attempt produces a compile-time error mentioning "use of internal package"
- [ ] Record the exact error message in your notes

### Hints
<details>
<summary>Hint 1 (structure hint)</summary>

```bash
mkdir -p internal-demo/internal/secrets internal-demo/cmd/app
mkdir -p outsider
cd internal-demo && go mod init github.com/example/internal-demo && cd ..
cd outsider && go mod init github.com/example/outsider && cd ..
```

</details>

<details>
<summary>Hint 2 (what the error looks like)</summary>

When you run `go build` in the `outsider` module, you should see something like:
```text
package github.com/example/outsider: cannot find package ...
```
or if the package is downloaded:
```text
use of internal package github.com/example/internal-demo/internal/secrets not allowed
```

</details>

### Expected Output / Acceptance Criteria
```bash
# Inside internal-demo:
$ go build ./...
# (success, no output)

# Inside outsider (after attempting to import internal/secrets):
$ go build ./...
main.go:5:2: use of internal package \
  github.com/example/internal-demo/internal/secrets not allowed
```

### Solution
<details>
<summary>Show Solution</summary>

```go
// internal-demo/internal/secrets/secrets.go
package secrets

// SecretKey is the application secret. This package is internal —
// only code within github.com/example/internal-demo can import it.
var SecretKey = "s3cr3t"
```

```go
// internal-demo/cmd/app/main.go — LEGAL import
package main

import (
    "fmt"
    "github.com/example/internal-demo/internal/secrets"
)

func main() {
    fmt.Println("Key:", secrets.SecretKey) // Key: s3cr3t
}
```

```go
// outsider/main.go — ILLEGAL import from different module
package main

import (
    "fmt"
    "github.com/example/internal-demo/internal/secrets" // compile error
)

func main() {
    fmt.Println(secrets.SecretKey)
}
```

**Explanation:** The `internal/` restriction is path-based: `github.com/example/outsider` is not within the tree rooted at `github.com/example/internal-demo`, so it cannot import any package under `internal-demo/internal/`. The same restriction applies to any code with a different module path prefix, regardless of where the files physically are on disk. The error is a hard compile error — there is no build tag or flag to bypass it.

</details>

---

## Exercise 5: go mod tidy and Dependency Hygiene [🟡 Medium] [2 pts]

### Context
`go mod tidy` is the command that keeps `go.mod` and `go.sum` synchronized with what is actually imported. This exercise demonstrates what happens when `go.mod` and your imports diverge — and how `go mod tidy` fixes it.

### Task
Starting from Exercise 3's `logger` module (or create a fresh module):
1. Add a second dependency with `go get github.com/google/uuid@latest`
2. Write code that uses `uuid` to generate and print a UUID
3. Then *remove* the uuid import from your code (but do not run `go mod tidy` yet)
4. Observe that `go.mod` still lists `uuid` as a requirement even though no code imports it
5. Run `go mod tidy` and observe that `uuid` is removed from `go.mod` and `go.sum`
6. Now *add* an import for `github.com/fatih/color` in your code WITHOUT running `go get` first
7. Observe that `go build` fails with "no required module provides..."
8. Run `go mod tidy` again and observe that it adds the missing dependency

### Requirements
- [ ] Demonstrate the "stale dependency" case (go.mod has more than code imports)
- [ ] Demonstrate the "missing dependency" case (code imports more than go.mod declares)
- [ ] `go mod tidy` fixes both cases
- [ ] Record the exact error message for the missing dependency case

### Hints
<details>
<summary>Hint 1 (uuid usage)</summary>

```go
import "github.com/google/uuid"
id := uuid.New()
fmt.Println(id.String()) // e.g., "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
```

</details>

<details>
<summary>Hint 2 (color usage)</summary>

```go
import "github.com/fatih/color"
color.Green("this is green text")
```

</details>

### Expected Output / Acceptance Criteria
```bash
# After removing uuid from code but NOT running tidy:
$ cat go.mod
# still shows: require github.com/google/uuid v...

# After running go mod tidy:
$ go mod tidy
$ cat go.mod
# uuid is gone

# After adding fatih/color import but NOT running go get:
$ go build ./...
main.go:5:2: no required module provides package github.com/fatih/color; \
  to add it: go get github.com/fatih/color

# After running go mod tidy:
$ go mod tidy
go: finding module for package github.com/fatih/color
go: added github.com/fatih/color v1.16.0
```

### Solution
<details>
<summary>Show Solution</summary>

```bash
# Step 1: add uuid
go get github.com/google/uuid@latest

# Step 2: use it in code (write uuid import into main.go)
# Step 3: remove the uuid import from main.go
# Step 4: observe go.mod still has uuid
cat go.mod  # uuid is still listed

# Step 5: tidy removes it
go mod tidy
cat go.mod  # uuid is gone

# Step 6: add fatih/color import to code (do NOT run go get)
# edit main.go to add: import "github.com/fatih/color"
# and use color.Green("hello")

# Step 7: build fails
go build ./...
# main.go:5:2: no required module provides package github.com/fatih/color

# Step 8: tidy adds it
go mod tidy
go build ./...  # now succeeds
```

**Explanation:** `go build` does not automatically update `go.mod` — it only uses what is already declared. `go mod tidy` does: it walks all import statements in your code, adds any missing requirements, and removes any unused ones. This is why `go mod tidy` should be run before every commit that changes imports. The CI check `go mod tidy && git diff --exit-code go.mod go.sum` catches divergence before it reaches the repository.

</details>

---

## Exercise 6: Multi-Package Layout with cmd/ and internal/ [🔴 Hard] [3 pts]

### Context
Real Go projects use the `cmd/` + `internal/` layout to separate binaries from implementation and enforce encapsulation. This exercise builds a realistic two-binary module from scratch.

### Task
Create a module `github.com/example/notes` with two binaries and shared internal packages:

```text
notes/
  go.mod
  cmd/
    add/
      main.go        — reads args; calls internal/store to add a note
    list/
      main.go        — calls internal/store to list all notes; prints them
  internal/
    store/
      store.go       — in-memory []Note store; exported: Note type, Add(), List()
    format/
      format.go      — unexported helpers + exported: FormatNote(n Note) string
```

Requirements for `internal/store`:
- `type Note struct { ID int; Text string; CreatedAt time.Time }`
- `func Add(text string) Note` — appends a new note with auto-incremented ID and current time
- `func List() []Note` — returns all notes

Requirements for `internal/format`:
- `func FormatNote(n store.Note) string` — returns `"[1] Hello world (2024-01-15 12:00)"`

`cmd/add/main.go` — reads `os.Args[1]` as the note text, calls `store.Add`, prints the formatted note.
`cmd/list/main.go` — calls `store.List`, formats and prints each note with `format.FormatNote`.

### Requirements
- [ ] Both binaries build with `go build ./cmd/add/ && go build ./cmd/list/`
- [ ] `cmd/add/main.go` imports both `internal/store` and `internal/format`
- [ ] `internal/format` imports `internal/store` (packages within the same module can import each other's internal packages)
- [ ] The in-memory store is shared via package-level state within a single process
- [ ] `go run ./cmd/add/ "Buy milk"` prints the formatted new note
- [ ] `go run ./cmd/list/` prints all previously added notes (note: since the store is in-memory, each invocation starts fresh — that is acceptable)

### Hints
<details>
<summary>Hint 1 (package-level state)</summary>

```go
// internal/store/store.go
package store

var (
    notes   []Note
    nextID  = 1
)
```

Package-level vars are shared across all callers within the same process. Since each `go run` is a fresh process, the store starts empty each time — this is expected for an in-memory store without persistence.

</details>

<details>
<summary>Hint 2 (import path between internal packages)</summary>

`internal/format` can import `internal/store` because both are within the same module:
```go
import "github.com/example/notes/internal/store"
```

</details>

<details>
<summary>Hint 3 (format function)</summary>

```go
func FormatNote(n store.Note) string {
    return fmt.Sprintf("[%d] %s (%s)", n.ID, n.Text, n.CreatedAt.Format("2006-01-02 15:04"))
}
```

Go's time format uses the reference time `Mon Jan 2 15:04:05 MST 2006` — `2006-01-02 15:04` is year-month-day hour:minute.

</details>

### Expected Output / Acceptance Criteria
```bash
$ go run ./cmd/add/ "Buy milk"
[1] Buy milk (2024-06-09 12:00)

$ go run ./cmd/add/ "Call dentist"
[1] Call dentist (2024-06-09 12:01)

$ go run ./cmd/list/
(empty — fresh process, no notes)
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
// internal/store/store.go
package store

import "time"

// Note represents a single text note.
type Note struct {
    ID        int
    Text      string
    CreatedAt time.Time
}

// package-level state: shared within one process
var (
    notes  []Note
    nextID = 1
)

// Add creates and stores a new note with the given text.
func Add(text string) Note {
    n := Note{ID: nextID, Text: text, CreatedAt: time.Now()}
    notes = append(notes, n)
    nextID++
    return n
}

// List returns all notes in creation order.
func List() []Note {
    return notes
}
```

```go
// internal/format/format.go
package format

import (
    "fmt"
    "github.com/example/notes/internal/store"
)

// FormatNote returns a human-readable string for a note.
func FormatNote(n store.Note) string {
    return fmt.Sprintf("[%d] %s (%s)",
        n.ID, n.Text, n.CreatedAt.Format("2006-01-02 15:04"))
}
```

```go
// cmd/add/main.go
package main

import (
    "fmt"
    "os"
    "github.com/example/notes/internal/format"
    "github.com/example/notes/internal/store"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintln(os.Stderr, "usage: add <text>")
        os.Exit(1)
    }
    n := store.Add(os.Args[1])
    fmt.Println(format.FormatNote(n))
}
```

```go
// cmd/list/main.go
package main

import (
    "fmt"
    "github.com/example/notes/internal/format"
    "github.com/example/notes/internal/store"
)

func main() {
    notes := store.List()
    if len(notes) == 0 {
        fmt.Println("(no notes)")
        return
    }
    for _, n := range notes {
        fmt.Println(format.FormatNote(n))
    }
}
```

**Step-by-step explanation:**
1. The module has two independent binaries — each in its own `cmd/` subdirectory, each a `package main`.
2. Both binaries import `internal/store` and `internal/format` — two cross-package dependencies within the same module.
3. `internal/format` imports `internal/store` — `internal` packages within the same module can import each other freely.
4. The store's package-level state (`notes` slice) is shared within a single process invocation. Each `go run` starts a fresh process, so the state is not persisted between runs.

</details>

---

## Exercise 7: Multi-Module Workspace [⭐ Expert] [5 pts]

### Context
Go workspaces (`go.work`) solve the multi-module local development problem: you are actively developing both a library (`mylib`) and an application (`myapp`) that depends on it. Without a workspace, you'd need to publish every `mylib` change before `myapp` can use it.

### Task
Create two sibling modules in a parent directory, then link them with a workspace:

```text
dev/
  go.work            — created by go work init
  mylib/
    go.mod           — module github.com/example/mylib
    greeter.go       — package mylib; exports Greet(name string) string
  myapp/
    go.mod           — module github.com/example/myapp; requires mylib v0.1.0
    main.go          — imports mylib and calls mylib.Greet
```

Steps:
1. Create `mylib` with `go mod init github.com/example/mylib` and a `Greet` function
2. Create `myapp` with `go mod init github.com/example/myapp` — add `require github.com/example/mylib v0.1.0` to its `go.mod` manually (the module does not exist on any proxy, which is fine for workspace use)
3. Create the workspace: `go work init ./mylib ./myapp`
4. Build `myapp` and confirm it uses the local `mylib` (not a proxy version)
5. Modify `mylib`'s `Greet` function to return a different greeting
6. Rebuild `myapp` — confirm it sees the change immediately without any `go get` or `go mod tidy`
7. Demonstrate that `GOWORK=off go build ./...` in `myapp` fails (cannot find the module)

### Requirements
- [ ] `go.work` exists in `dev/` with `use` directives for both modules
- [ ] `myapp/go.mod` does NOT have a `replace` directive
- [ ] `go build` in `myapp/` succeeds with the workspace active
- [ ] Modifying `mylib/greeter.go` is immediately visible in `myapp` without any other command
- [ ] `GOWORK=off go build ./...` inside `myapp/` fails with a "no required module provides" or "cannot find module" error
- [ ] A `go.work` is **not** inside `mylib/` or `myapp/` — it is in the parent `dev/` directory

### Hints
<details>
<summary>Hint 1 (go.mod for myapp without a published mylib)</summary>

You can write a `require` for a module that doesn't exist on any proxy. With the workspace active, the build system uses the local path from `go.work` instead. `go.mod` still needs the `require` line for `go build` to know what the import path resolves to.

```text
# myapp/go.mod
module github.com/example/myapp

go 1.22

require github.com/example/mylib v0.1.0
```

</details>

<details>
<summary>Hint 2 (workspace commands)</summary>

```bash
cd dev
go work init ./mylib ./myapp
# go.work is created in dev/
cat go.work
# go 1.22
# use (
#   ./mylib
#   ./myapp
# )
```

</details>

<details>
<summary>Hint 3 (verifying workspace vs non-workspace behavior)</summary>

```bash
# With workspace (go.work active):
cd dev/myapp
go build ./...  # uses local ./dev/mylib

# Without workspace:
GOWORK=off go build ./...
# error: no required module provides package github.com/example/mylib
```

</details>

### Expected Output / Acceptance Criteria
```bash
# Initial build:
$ cd dev/myapp && go build -o myapp . && ./myapp
Hello, World!

# After modifying mylib/greeter.go to return "Greetings, World!":
$ go build -o myapp . && ./myapp
Greetings, World!   ← change visible immediately, no go get needed

# Without workspace:
$ GOWORK=off go build .
main.go:5:2: no required module provides \
  package github.com/example/mylib; to add it:
  go get github.com/example/mylib
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```bash
mkdir -p dev/mylib dev/myapp
```

```go
// dev/mylib/greeter.go
package mylib

import "fmt"

// Greet returns a greeting string for the given name.
func Greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}
```

```bash
cd dev/mylib && go mod init github.com/example/mylib && cd ..
```

```go
// dev/myapp/main.go
package main

import (
    "fmt"
    "github.com/example/mylib"
)

func main() {
    fmt.Println(mylib.Greet("World"))
}
```

```text
# dev/myapp/go.mod (written manually or via go mod init + manual require)
module github.com/example/myapp

go 1.22

require github.com/example/mylib v0.1.0
```

```bash
cd dev/mylib && go mod init github.com/example/mylib
cd ../myapp && go mod init github.com/example/myapp
# Add require manually to go.mod
cd ..  # back to dev/
go work init ./mylib ./myapp

# Build and run:
cd myapp
go build -o myapp . && ./myapp
# Hello, World!

# Modify mylib/greeter.go: change "Hello" to "Greetings"
# Rebuild immediately:
go build -o myapp . && ./myapp
# Greetings, World!

# Disable workspace:
GOWORK=off go build .
# error: no required module provides package github.com/example/mylib
```

**Step-by-step explanation:**
1. The `go.work` file in `dev/` tells the Go toolchain to use the local `./mylib` and `./myapp` directories when resolving imports.
2. `myapp/go.mod` still has `require github.com/example/mylib v0.1.0` — this is what `go build` uses when the workspace is disabled. With the workspace active, this `require` is effectively overridden by the workspace's `use ./mylib`.
3. After changing `mylib/greeter.go`, there is no need to run `go get` or update any version number — the workspace transparently uses the local source.
4. `GOWORK=off` demonstrates that the workspace is the only reason the build works — without it, the module `github.com/example/mylib` does not exist at any proxy and the build fails.
5. `go.work` belongs in `.gitignore` — it is a local convenience, not part of the project's definition.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Single-Package Module | — | —/1 | — | — |
| Exercise 2 — Export Rules Reading | — | —/1 | — | — |
| Exercise 3 — go.mod with Real Dependency | — | —/2 | — | — |
| Exercise 4 — internal/ Enforcement | — | —/2 | — | — |
| Exercise 5 — go mod tidy Hygiene | — | —/2 | — | — |
| Exercise 6 — Multi-Package Layout | — | —/3 | — | — |
| Exercise 7 — Multi-Module Workspace | — | —/5 | — | — |
| **Total** | | **—/16** | | |

**Passing threshold:** 10/16 (63%). Aim for 13/16 (81%) before taking the test.
