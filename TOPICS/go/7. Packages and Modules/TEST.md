# Test — Module 7: Packages and Modules

**Topic:** [[go]]
**Module:** [[go/7. Packages and Modules]]

---

## Before You Begin

> [!WARNING]
> **Do not look at ANSWERS.md or your notes during the test.**
> The purpose of this test is to surface what you truly know vs. what you think you know.
> An inflated score is worthless. An honest score shows you exactly where to focus next.

**Instructions:**
1. Close all notes, the module README, and any reference materials.
2. Set a timer. Note your start time below.
3. Attempt every question — partial credit exists.
4. After finishing, grade yourself using ANSWERS.md.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Start time:** ___________
**End time:** ___________
**Total time:** ___________

---

## Scoring Table

| Section | Question Type | Points Each | # Questions | Max Points |
|---------|--------------|-------------|-------------|------------|
| Section 1: Recall | Easy | 1 pt | 5 | 5 pts |
| Section 2: Conceptual | Medium | 2 pts | 3 | 6 pts |
| Section 3: Applied | Hard | 3 pts | 2 | 6 pts |
| Section 4: Scenario | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** What is the relationship between a directory and a package in Go? Can a single directory contain two different packages?

> _Your answer:_

---

**1.2** Go has no `public` or `private` keywords. What determines whether an identifier (function, type, variable, struct field) is visible outside its package?

> _Your answer:_

---

**1.3** What is the purpose of `go.sum`? Should it be committed to version control? Can you edit it by hand?

> _Your answer:_

---

**1.4** What does `go mod tidy` do? Name two situations where you should run it.

> _Your answer:_

---

**1.5** What is the `/v2` rule in semantic import versioning? Give a concrete example showing how the import path changes between v1 and v2 of a module.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain what Minimal Version Selection (MVS) is and why Go uses it instead of "pick the latest compatible version." Consider a scenario where your module requires package A v1.2 (which requires C v1.1) and package B v1.0 (which requires C v1.3). What version of C does MVS select, and why is this better than picking the absolute latest?

> _Your answer:_

---

**2.2** Explain the purpose of the `internal/` directory and give a concrete example of when you would use it. What exactly does the Go toolchain enforce — and what does that enforcement look like (compile-time error? Runtime panic? Something else)?

> _Your answer:_

---

**2.3** What problem does `go.work` (the workspace file) solve? Why is it better than putting a `replace` directive in `go.mod` for local multi-module development? Under what condition should `go.work` NOT be committed to version control?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write the minimal `go.mod` file for a module named `github.com/myorg/myservice` that:
- Uses Go 1.22
- Depends on `github.com/gin-gonic/gin` at exactly version `v1.9.1`
- Depends on `golang.org/x/crypto` at version `v0.17.0` (this one is an indirect dependency)

Also write the two shell commands you would run to verify the module graph is consistent (no unused or missing dependencies), and to list all modules in the dependency tree.

> _Your answer:_

---

**3.2** Given the following package layout, identify and fix all problems. Explain what each problem is and why it is a problem in Go:

```text
myapp/
  go.mod         — module github.com/myorg/myapp
  util/
    util.go      — package util; contains: DB connection logic, HTTP helpers,
                   string utilities, config loading, email sending
  main.go        — package main; imports util and calls all util functions
```

```go
// util/util.go
package Util   // ← Problem?

import (
    "database/sql"
    "net/http"
    "fmt"
    "strings"
)

var DB *sql.DB  // global
var Client = &http.Client{}

func connectDB(dsn string) {  // ← Problem?
    // ...
}

func SendEmail(to, subject, body string) error { return nil }
func TrimAndLower(s string) string { return strings.TrimSpace(strings.ToLower(s)) }
```

> _Your answer (list at least 3 problems with explanations and fixes):_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague pushes this `go.mod` to the shared repository:

```text
module github.com/myorg/myservice

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/myorg/mylib v0.3.0
)

replace github.com/myorg/mylib => ../mylib
```

The CI build fails for every other engineer on the team with:

```text
go: github.com/myorg/mylib@v0.3.0: reading file:///home/runner/../mylib/go.mod:
  open /home/runner/../mylib/go.mod: no such file or directory
```

Answer all three parts:

**a)** What is the root cause of the CI failure? Explain precisely why it works on your colleague's machine but fails everywhere else.

**b)** What is the correct fix? Provide the exact change to make (to which file, and what change).

**c)** If your colleague needs to continue developing `mylib` and `myapp` simultaneously after the fix, what should they do locally?

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** A new Go developer on your team asks: "Why do we have an `internal/` directory? If I want something private I'll just not document it — no one will use it." Explain why this reasoning is insufficient and why `internal/` provides a stronger guarantee. Consider at least two scenarios where the difference between "convention" and "compiler enforcement" matters in practice.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** The `init()` function is powerful but often misused. Consider the following package which uses `init()` for configuration loading:

```go
package appconfig

import (
    "os"
    "log"
)

var DatabaseURL string
var Port string

func init() {
    DatabaseURL = os.Getenv("DATABASE_URL")
    if DatabaseURL == "" {
        log.Fatal("DATABASE_URL environment variable is required")
    }
    Port = os.Getenv("PORT")
    if Port == "" {
        Port = "8080"
    }
}
```

Answer all three parts:

**a)** List at least three specific problems with using `init()` for this kind of configuration loading.

**b)** Rewrite this as an explicit initialization function (`func Load() (*Config, error)`) that solves the problems you identified. Define a `Config` struct with appropriate fields. The function should return an error (not call `log.Fatal`) and should not use `init()` at all.

**c)** Explain how callers should use your new `Load()` function — show a `main.go` that calls it and handles the error correctly.

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the next module?**
> _Your reflection:_

**What score did I get? Do I feel it accurately reflects my understanding?**
> _Your reflection:_

---

## Grading Record

_Append a new row each time you take this test. Do not overwrite previous attempts._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
