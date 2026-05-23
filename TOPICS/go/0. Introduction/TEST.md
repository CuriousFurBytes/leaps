# Test — Module 0: Introduction

**Topic:** [[go]]
**Module:** [[modules/go-0-introduction]]

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

**1.1** What does `package main` declare, and why is the name `main` special compared to other package names?

> _Your answer:_

---

**1.2** What command runs a Go source file without producing a binary on disk? Write the exact command you would use to run a file named `main.go`.

> _Your answer:_

---

**1.3** What does `go fmt` do, and why is it not optional in Go development?

> _Your answer:_

---

**1.4** What is the entry point function in every runnable Go program? Write its complete signature (return type included).

> _Your answer:_

---

**1.5** What happens at compile time if you import a package but do not call anything from it? What error does the compiler produce?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Why does Go enforce unused import detection at compile time rather than treating unused imports as a warning or silently ignoring them? What problem does this rule prevent, and what does it say about Go's design philosophy?

> _Your answer:_

---

**2.2** Explain what `go.mod` is and what problem it solves. Why did Go introduce the module system to replace GOPATH, and what were the concrete limitations of the GOPATH model?

> _Your answer:_

---

**2.3** Compare Go's compilation speed design goals with those of C++. What specific decisions in Go's language design contribute to fast compilation, and why did the Go designers consider compilation speed a first-class concern?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete, syntactically correct Go program that prints a personalized hello for each of the following names: "Alice", "Bob", "Charlie". The program must define a separate `greet` function that takes a name as input and returns the greeting string. `main` should call `greet` three times and print each result.

Requirements:
- Uses `package main` and imports `fmt`
- Defines `func greet(name string) string` outside of `main`
- `greet` uses `fmt.Sprintf` to build the string `"Hello, [name]! Welcome to Go."`
- `main` calls `greet` and passes the result to `fmt.Println`

> _Your answer:_

---

**3.2** Describe the complete sequence of commands you would run to start a new Go project called `myapi` (module path: `github.com/yourname/myapi`), add the external package `github.com/gorilla/mux` as a dependency, and verify the project builds correctly.

Requirements:
- Include the exact commands in the correct order
- Explain what each command does
- Identify which files are created and what they contain
- Explain the role of `go.sum`

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** The following Go program is supposed to print `"Hello, World!"` and the number `42`, but it refuses to compile:

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	message := "Hello, World!"
	number := 42
	fmt.Println(message)
}
```

Identify:

a) What is wrong? (There may be more than one issue.)

b) Why does this happen? What are the compiler rules being violated?

c) How would you fix it? Write the corrected code.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** Go's designers chose to make unused variables a compile error rather than a warning or a lint suggestion. This is an unusual decision — most languages treat unused variables as at most a warning. Why might the Go designers have made this choice? What are the benefits and potential downsides of this approach? Do you think it was the right call?

Consider at least two perspectives or approaches in your answer.
Justify your conclusion based on what you've learned in this module.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Go supports cross-compilation — building a binary for a different operating system or CPU architecture than the one you're developing on. Explain how Go achieves cross-compilation (what makes it possible at the language/toolchain level), write the exact shell commands you would use to compile a Go program from macOS (ARM64 / Apple Silicon) to produce binaries for Linux AMD64 and Windows AMD64, and describe one real-world scenario where cross-compilation is practically useful.

This may require combining knowledge from this module with independent reasoning about Go's compilation model.

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
