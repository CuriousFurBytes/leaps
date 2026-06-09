# Answer Key — Module 7: Packages and Modules

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — Directory and package relationship [1 pt]

**Full credit answer:**
In Go, **one directory = one package**. All `.go` files in the same directory must declare the same `package` name (the `package` declaration at the top of the file). A single directory cannot contain two different packages — the compiler will refuse to build it. Conversely, a package can span multiple files, as long as all files are in the same directory and all declare the same package name. The test files (`_test.go`) can declare `package foo_test` (external test package) in the same directory — this is the one common and accepted exception.

**Key points required:**
- One directory = one package (enforced by the compiler)
- Multiple files in one directory form a single package

**Common wrong answer:** *"A directory can have multiple packages if you use different filenames."* — This is incorrect. All files in a directory must be in the same package.

---

### 1.2 — Exported vs unexported (capitalization) [1 pt]

**Full credit answer:**
**Capitalization of the first letter** is Go's only access-control mechanism. An identifier starting with an **uppercase letter** is exported and visible to any package that imports it. An identifier starting with a **lowercase letter** is unexported and visible only within the same package. This applies to all identifiers: functions, types, variables, constants, struct fields, and interface methods. There is no `public`, `private`, or `protected` keyword.

**Key points required:**
- Uppercase = exported (public); lowercase = unexported (private)
- No `public`/`private` keywords — capitalization is the mechanism
- Applies to all identifiers, including struct fields

---

### 1.3 — go.sum purpose and handling [1 pt]

**Full credit answer:**
`go.sum` contains the expected cryptographic hashes (SHA-256) of every module zip and `go.mod` file that the build depends on, directly and transitively. Its purpose is **integrity verification**: if a module's content on the server changes (supply chain attack, accidental mutation), the hash will not match and the build will fail. `go.sum` **should be committed** to version control — it is not a build artifact, it is part of the project's security and reproducibility record. It should **never be edited by hand** — it is maintained automatically by `go get` and `go mod tidy`. Deleting or gitignoring `go.sum` is a security and reproducibility mistake.

**Key points required:**
- Purpose: tamper detection / integrity verification
- Must be committed to version control
- Never edit by hand — tools maintain it

---

### 1.4 — go mod tidy [1 pt]

**Full credit answer:**
`go mod tidy` synchronizes `go.mod` and `go.sum` with what is actually imported in your code. Specifically, it:
1. **Adds** any packages that are imported in code but not listed in `go.mod`
2. **Removes** any packages that are listed in `go.mod` but not imported anywhere in the code

Two situations to run it: (a) after adding a new `import` statement to your code without running `go get` first, and (b) after removing all uses of a dependency from your code (to remove the now-unused entry from `go.mod`). The best practice is to run it before every commit that changes imports.

**Key points required:**
- Adds missing, removes unused dependencies from go.mod/go.sum
- Two concrete situations (any two are fine: after adding import, after removing import, before committing, as a CI check)

---

### 1.5 — Semantic import versioning / the /v2 rule [1 pt]

**Full credit answer:**
For Go modules at **v2 or higher**, the major version must appear in the module path. This is the **semantic import versioning** rule. For v1 (and v0), the path is unchanged. For v2+, the major version suffix is appended:

```go
// v1 — module path unchanged
import "github.com/alice/mylib"          // go.mod: module github.com/alice/mylib

// v2 — /v2 appended to the import path
import "github.com/alice/mylib/v2"       // go.mod: module github.com/alice/mylib/v2

// v3
import "github.com/alice/mylib/v3"
```

**Why:** Two major versions can coexist in the same build because they have different import paths. Without this rule, a program couldn't import both v1 and v2 simultaneously.

**Key points required:**
- v2+ requires `/v2` (or `/v3`, etc.) in the import path
- v0 and v1 have no version suffix
- A concrete example

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Minimal Version Selection [2 pts]

**Full credit answer:**
MVS selects the **minimum version that satisfies all constraints** in the dependency graph — not the latest, not the maximum.

In the given scenario:
- Your module requires A v1.2 (which requires C v1.1) and B v1.0 (which requires C v1.3)
- Both A and B require C; the minimum version that satisfies *both* is **C v1.3** (since v1.3 ≥ v1.1 and v1.3 ≥ v1.3)

Why MVS is better than "pick the latest":
1. **Reproducibility**: The same `go.mod` produces the same build on any machine at any time — there is no floating "latest" version to drift
2. **No surprise upgrades**: Adding a new dependency cannot silently upgrade an existing one; you only get upgrades when you explicitly run `go get -u`
3. **Tested combinations**: The minimum satisfying version is exactly what the authors tested against when they published — you stay as close to tested territory as possible

**Rubric:**
- 2 pts: Correctly identifies C v1.3 as the selected version AND explains reproducibility/no-surprise-upgrades benefit
- 1 pt: Correctly picks C v1.3 but explanation of why is weak or missing
- 0 pts: Picks wrong version (e.g., "latest C") or fundamentally misunderstands the algorithm

---

### 2.2 — internal/ packages [2 pts]

**Full credit answer:**
The `internal/` directory restricts which code can import a package. A package at path `github.com/myorg/myapp/internal/storage` can only be imported by code whose import path starts with `github.com/myorg/myapp/` — code within the same module. Any import of an `internal/` package by code outside the parent tree is rejected at **compile time** with an error like:

```text
use of internal package github.com/myorg/myapp/internal/storage not allowed
```

This is not a naming convention, a linter warning, or a runtime check — it is a hard compiler error that cannot be bypassed.

**Concrete use case:** You are building a library `github.com/alice/httpclient` that has implementation helpers in `internal/retry` and `internal/pool`. You do not want external consumers of your library to depend on `retry` or `pool` — they are implementation details you might change in a minor version. By putting them in `internal/`, the compiler guarantees no external code can import them. If they were in `pkg/retry` instead, any external package could import `github.com/alice/httpclient/pkg/retry` and then you'd be stuck maintaining it as a public API.

**Rubric:**
- 2 pts: Correctly identifies compile-time enforcement AND gives a sensible use case
- 1 pt: Understands the concept but describes it as a convention/lint rule rather than compiler enforcement, or no concrete example
- 0 pts: Thinks `internal/` is just a naming convention with no enforcement

---

### 2.3 — go.work workspaces [2 pts]

**Full credit answer:**
`go.work` solves the problem of developing two related modules simultaneously when one depends on the other, without modifying either module's `go.mod`.

**The problem with `replace`:** If you put `replace github.com/alice/mylib => ../mylib` in `myapp/go.mod`, you must remember to remove it before committing. If you forget, everyone who clones the repo gets a broken build because `../mylib` doesn't exist at their file path. This is a common and frustrating mistake.

**How `go.work` fixes it:** The workspace file lives outside both modules (in a parent directory), is never committed (added to `.gitignore`), and tells the Go toolchain to use local paths for specific modules. The individual `go.mod` files remain clean and publishable.

**When NOT to commit `go.work`:** Always. A `go.work` file is a local development convenience. It contains absolute or relative paths specific to your machine's filesystem layout. Committing it would break the build for everyone else — their filesystem has a different layout. Add `go.work` and `go.work.sum` to `.gitignore`.

**Rubric:**
- 2 pts: Correctly identifies the problem with `replace` (left in go.mod breaks CI/other devs) AND explains that go.work should not be committed + why
- 1 pt: Understands what go.work does but unclear on why it's better than replace, or unclear on the "don't commit" rule
- 0 pts: Thinks go.work should be committed, or fundamentally confuses go.work with go.mod

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Writing go.mod and module commands [3 pts]

**Full credit answer:**

```text
module github.com/myorg/myservice

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    golang.org/x/crypto v0.17.0 // indirect
)
```

Shell commands:
```bash
# Remove unused dependencies and add missing ones:
go mod tidy

# List all modules in the dependency tree (direct and indirect):
go list -m all
```

**Acceptable alternatives:**
- `golang.org/x/crypto` may or may not have `// indirect` depending on whether it's actually imported directly or only transitively — both are correct depending on the scenario; credit the answer if the directive structure is correct
- `go mod verify` is also a valid "verify consistency" command
- `go mod graph` shows the full dependency graph (less useful for "list all modules" but acceptable)

**Rubric:**
- 3 pts: Correct go.mod structure (module, go, require with both dependencies and correct versions) AND two correct commands
- 2 pts: go.mod is correct but only one command given, or minor syntax error in go.mod
- 1 pt: go.mod structure understood but dependencies missing/wrong, or commands missing
- 0 pts: Fundamental misunderstanding of go.mod syntax

---

### 3.2 — Identifying and fixing package problems [3 pts]

**Full credit answer (at least 3 of these):**

**Problem 1: `package Util` — package name starts with uppercase**
Go package names must be lowercase by convention (enforced by `gofmt` and considered idiomatic). `package Util` is technically valid Go but violates strong community conventions. Fix: `package util`

**Problem 2: Giant mixed-responsibility `util` package**
The `util` package contains DB connections, HTTP clients, string utilities, config loading, and email sending — completely unrelated concerns. This makes the package impossible to test in isolation, hard to understand, and tends to grow into a dumping ground. Fix: Split into domain-specific packages:
```text
internal/database/  — DB connection
internal/email/     — email sending
internal/config/    — config loading
# standard library handles HTTP client and strings
```

**Problem 3: `connectDB` is unexported but is the only way to initialize the DB**
If `connectDB` is unexported, nothing outside the package can call it. But `DB` is exported — callers will get a nil `*sql.DB` unless they somehow trigger initialization. The pattern is broken. Fix: either export `ConnectDB(dsn string) error` so callers can initialize it, or use an exported `Init()` function. Alternatively, remove the global entirely and use dependency injection.

**Problem 4: Global mutable state (`var DB *sql.DB`, `var Client`)**
Package-level mutable globals make testing difficult (tests cannot isolate behavior, globals persist between tests), are unsafe for concurrent use without explicit locking, and create hidden dependencies (callers must know the package was initialized before use). Fix: Use dependency injection — pass `*sql.DB` and `*http.Client` as function parameters or struct fields.

**Rubric:**
- 3 pts: Identifies at least 3 distinct problems with correct explanations and concrete fixes
- 2 pts: Identifies 2 problems with explanations, or 3 problems without full fixes
- 1 pt: Identifies 1 problem correctly
- 0 pts: Does not identify any real problems

**Teaching note:** Students who only catch the `package Util` capitalization issue are pattern-matching on syntax without thinking architecturally. The structural issues (mixed responsibilities, globals) are the important problems for professional Go code.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — replace directive in committed go.mod [3 pts] (1 pt each part)

**(a) Root cause:**
The `replace github.com/myorg/mylib => ../mylib` directive substitutes the published module with a **local filesystem path** (`../mylib`). On your colleague's machine, `../mylib` exists as a sibling directory to the project. On the CI runner (and every other developer's machine), `../mylib` does not exist at that relative path — there is no sibling `mylib` directory in their checkout. The build fails because the Go toolchain cannot find the substituted path. The directive should never have been committed; it was a local development convenience.

**(b) The fix:**
Remove the `replace` directive from `go.mod`. The `go.mod` should contain only the published `require` directive:

```text
module github.com/myorg/myservice

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/myorg/mylib v0.3.0
)
```

Commit the updated `go.mod`. The CI build will now fetch `mylib v0.3.0` from the module proxy normally.

**(c) Local multi-module development:**
After removing the `replace` directive from `go.mod`, your colleague should use a **`go.work` file** for local development:

```bash
# From the parent directory containing both modules:
go work init ./myservice ./mylib
echo "go.work" >> .gitignore
echo "go.work.sum" >> .gitignore
```

The workspace transparently uses the local `mylib` without modifying `go.mod`. The `go.work` file stays local (gitignored) and never pollutes the committed module files.

**Rubric:**
- 1 pt for (a): Correctly identifies that the `replace` directive points to a local path that doesn't exist on other machines
- 1 pt for (b): Removes the `replace` directive from `go.mod` (keep the `require`, remove only the `replace`)
- 1 pt for (c): Recommends `go.work` (not `replace`) for local development, with go.work added to gitignore

**Common wrong answer for (b):** Adding `github.com/myorg/mylib` to `.gitignore` or changing the path to an absolute path. Absolute paths are even worse — they would only work on the exact same machine with the exact same home directory layout.

**Common wrong answer for (c):** "Run `go get github.com/myorg/mylib@latest` every time you make a change to mylib" — this requires publishing a new version every time, which is impractical during active development.

---

## Section 5: Discussion — Answer Key

### 5.1 — Why internal/ matters vs convention [2 pts]

**Example strong answer:**
"Just don't document it" and "add a comment saying it's private" rely on human compliance — developers following a convention they read somewhere. The `internal/` directory relies on the **compiler refusing to build code that violates the rule**, regardless of whether the developer knew about or respected the convention. These are fundamentally different guarantees.

Two scenarios where compiler enforcement matters:

1. **Third-party consumers of your library:** If you publish `github.com/alice/mylib` and keep implementation details in `pkg/private/` with a comment "do not use externally," nothing prevents someone from writing `import "github.com/alice/mylib/pkg/private"` in their code. Once they do, you can't remove or change `private` in a minor version without breaking them. With `internal/`, the compiler prevents them from ever importing it — your freedom to evolve internals is protected by the toolchain, not by hope.

2. **Large teams and codebases:** In a team of ten engineers, "the convention is not to import `util/db` from the frontend package" works fine until it doesn't — someone on a deadline adds the import, it sneaks through code review, and now you have an architectural violation that is expensive to undo. With `internal/`, the CI build fails the moment the forbidden import is added, giving you an automatic check that scales to any team size without relying on discipline.

**Elements that earn full credit:**
- Correctly identifies that "convention" is human-compliance based while `internal/` is compiler-enforced
- Gives two concrete scenarios (library consumers OR large teams both count; one each from each scenario type is ideal)
- Describes what the compiler does (compile-time error, not a warning or runtime panic)

**Rubric:**
- 2 pts: Clearly articulates convention vs enforcement AND gives two concrete scenarios
- 1 pt: Understands the benefit of enforcement but only one scenario, or the scenarios are vague
- 0 pts: Claims convention is sufficient, or misunderstands what `internal/` does

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — init() vs explicit initialization [+5 pts]

**(a) Problems with init() for configuration:**

1. **Cannot return an error** — `log.Fatal` calls `os.Exit(1)`, which bypasses `defer` statements and makes testing impossible (you cannot catch a fatal in a test without forking a subprocess). Failing to load config is a legitimate error that deserves to be handled, not a reason to crash silently.
2. **Invisible to callers** — Users of the package cannot see that importing it runs `init()` and calls `log.Fatal`. The side effect is hidden. In tests, importing the package may crash the test runner if the env vars are not set.
3. **Cannot be controlled** — You cannot call `init()` conditionally, skip it for tests, or retry it. An explicit function can be called (or not) at the right moment.
4. **Ordering problems** — If another package's `init()` depends on this package being configured first, the order of `init()` execution becomes critical and fragile.
5. **Not testable** — A test importing this package must always have `DATABASE_URL` set, or the test crashes on import.

**(b) Explicit initialization function:**

```go
package appconfig

import (
    "fmt"
    "os"
)

// Config holds application configuration loaded from the environment.
type Config struct {
    DatabaseURL string
    Port        string
}

// Load reads configuration from environment variables.
// Returns an error if required variables are missing.
func Load() (*Config, error) {
    dbURL := os.Getenv("DATABASE_URL")
    if dbURL == "" {
        return nil, fmt.Errorf("appconfig.Load: DATABASE_URL environment variable is required")
    }
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    return &Config{
        DatabaseURL: dbURL,
        Port:        port,
    }, nil
}
```

**(c) Caller usage:**

```go
// main.go
package main

import (
    "fmt"
    "log"
    "os"

    "github.com/myorg/myservice/internal/appconfig"
)

func main() {
    cfg, err := appconfig.Load()
    if err != nil {
        fmt.Fprintf(os.Stderr, "configuration error: %v\n", err)
        os.Exit(1)
    }

    log.Printf("starting server on port %s", cfg.Port)
    // use cfg.DatabaseURL, cfg.Port, etc.
}
```

**Rubric:**
- 5 pts: Correctly identifies 3+ init() problems, rewrites with proper error return and Config struct, shows correct caller usage
- 3 pts: Identifies 2 problems and provides a working rewrite with error return
- 1 pt: Identifies the problem with log.Fatal but the rewrite still uses init() or ignores errors

---

## Common Wrong Answers Across the Test

1. **Confusing package name with import path** — "The package name in `package calc` must match the last segment of the import path." This is a convention, not a rule. The package name in the `package` declaration and the last path component can differ (though they should match for clarity). Callers use the package name from the `package` declaration, not the directory name.

2. **Thinking go.sum is the lock file** — `go.sum` is an integrity file, not a version lock. The version information is in `go.mod`. Versions are determined by MVS applied to `go.mod` directives. `go.sum` records hashes to detect tampering; it does not choose versions.

3. **Believing replace directives are the right way to do local development** — Before Go 1.18, `replace` was the only option. Since Go 1.18, `go.work` is the correct tool. Committed `replace` directives with local paths are always a mistake.

4. **Not knowing what the `/v2` import path rule implies for coexistence** — Students often know the rule ("add /v2 to the path") without knowing *why* — it allows v1 and v2 of the same module to coexist in the same build because they have distinct import paths. Questions about "why does the path have to change" require this explanation.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 likely have theoretical knowledge without having set up a real Go project. Recommend: do Exercise 6 (multi-package layout) and Exercise 7 (workspace) before re-attempting the test.
- The most predictive question for overall Go module competence is 4.1 (the replace directive scenario). Students who correctly identify all three parts (root cause, fix, go.work alternative) have a solid practical understanding. Students who cannot identify the root cause need to actually try the workflow with real commands.
- For the bonus question (6.1), students who score well tend to have worked on real production Go code where `init()` abuse caused problems in testing. Students who score poorly often haven't yet encountered a test that fails mysteriously because an `init()` ran at import time.
- A score below 60% on Section 3 generally indicates the student has read the material but has not run the commands. The module commands (`go get`, `go mod tidy`, `go list -m all`) need to be practiced, not just read about.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
