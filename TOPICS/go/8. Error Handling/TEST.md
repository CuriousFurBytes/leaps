# Test — Module 8: Error Handling

**Topic:** [[go]]
**Module:** [[go/8. Error Handling]]

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

**1.1** What is the definition of the `error` interface in Go? Write it out exactly (or as close as you can from memory).

> _Your answer:_

---

**1.2** What is the difference between `fmt.Errorf("context: %v", err)` and `fmt.Errorf("context: %w", err)`? When would you choose each?

> _Your answer:_

---

**1.3** What does `errors.Is(err, target)` do that a direct `err == target` comparison does not?

> _Your answer:_

---

**1.4** What is `errors.Join` used for, and in which Go version was it added?

> _Your answer:_

---

**1.5** Inside what kind of function must `recover()` be called for it to actually stop a panic? What happens if you call `recover()` outside that context?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain the "typed-nil error trap." What is it, why does it happen, and how do you avoid it? Include a concrete code example showing the wrong version and the correct version.

> _Your answer:_

---

**2.2** Go uses errors-as-values rather than exceptions. Give two concrete advantages of the errors-as-values approach for a professional engineer reading or debugging a large codebase. Avoid vague claims like "it's simpler" — be specific about what is easier or harder in each model.

> _Your answer:_

---

**2.3** Explain the difference between `errors.Is` and `errors.As`. When would you use each? Give one scenario where `errors.Is` is the right tool and one scenario where `errors.As` is the right tool.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a Go function `openDB(dsn string) (*sql.DB, error)` that:
- Opens a database connection using `sql.Open("postgres", dsn)`
- Pings the database using `db.Ping()`
- Returns the `*sql.DB` on success
- Wraps any error with appropriate context using `fmt.Errorf` and `%w`

You do not need to write an import block or make it compile — focus on the function body and error handling idioms.

> _Your answer:_

---

**3.2** Write a Go function `safeEval(expr string, eval func(string) int) (result int, err error)` that:
- Uses named return values
- Defers a function that recovers from any panic, converting it to an error via `err = fmt.Errorf("safeEval: panic: %v", r)`
- Calls `eval(expr)` and returns its result
- Returns `0, nil` if `eval` succeeds without panicking

Show the function signature and body only — you do not need a full program.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong._

**4.1** The following code has three distinct error handling problems. Identify each one, explain why it is a problem, and describe the correct fix.

```go
func processRequest(userID int) (User, error) {
    var fetchErr *FetchError
    u, err := fetchUser(userID)
    if err != nil {
        log.Printf("fetchUser failed: %v", err)
        return User{}, err
    }

    data, err := loadProfile(u.ProfileID)
    if err != nil {
        if err == ErrNotFound {  // direct == comparison
            return User{}, ErrNotFound
        }
        return User{}, err  // bare return, no context
    }

    return buildUser(u, data), fetchErr  // returns fetchErr which is always nil
}
```

For each problem: name it, explain why it is wrong, and write the corrected line or block.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "Use `panic` only for programmer errors and unrecoverable situations — never for expected failure modes." Explain what this guideline means in practice. Give one example of a situation where `panic` is appropriate and one where it is not. For the inappropriate case, describe the correct alternative. Also explain: what makes a situation "expected" vs. "unrecoverable"?

> _Your answer (aim for 4–7 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Design and implement a `Result[T]` type in Go that encapsulates either a value or an error — similar to Rust's `Result<T, E>` or Haskell's `Either`. Your implementation must:

1. Define `type Result[T any] struct` with appropriate fields (Go 1.18+ generics)
2. Provide `OK(v T) Result[T]` and `Err(e error) Result[T]` constructors
3. Provide `func (r Result[T]) Unwrap() (T, error)` — returns the value or error
4. Provide `func (r Result[T]) Must() T` — returns the value or panics if it's an error
5. Write a brief explanation of when this abstraction is useful and when idiomatic Go `(T, error)` returns are preferable

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
