# Test — Module 12: Advanced Concurrency Patterns

**Topic:** [[go]]
**Module:** [[go/12. Advanced Concurrency Patterns]]

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

**1.1** What does `defer cancel()` do after `context.WithTimeout`, and why is it necessary even if the timeout expires before `cancel()` is explicitly called?

> _Your answer:_

---

**1.2** Name the four `context` constructor functions and, for each, state whether the caller gets a `cancel` function back and what triggers cancellation.

> _Your answer:_

---

**1.3** In a pipeline, what is the significance of `defer close(out)` inside a stage's goroutine? What happens to a downstream stage that is blocked on `for n := range in` if `close(in)` is never called?

> _Your answer:_

---

**1.4** What is the difference between `atomic.Int64.Add` and `atomic.Int64.CompareAndSwap`? Give a brief example of when you would use `CompareAndSwap` instead of `Add`.

> _Your answer:_

---

**1.5** What does `goleak.VerifyNone(t)` (or `runtime.NumGoroutine()`) catch, and at what point in a test should you check it?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why `context.Context` should be the **first parameter** of any function that does I/O or starts goroutines, rather than a global variable or a struct field. What goes wrong if you store a context in a struct field and reuse that struct across multiple requests?

> _Your answer:_

---

**2.2** Explain the difference between a bounded **worker pool** and an unbounded **fan-out** (one goroutine per work item). In what scenario would each be appropriate? What are the failure modes of unbounded fan-out at scale?

> _Your answer:_

---

**2.3** `sync/atomic` operations are described as "lock-free." Explain what makes an atomic operation different from a mutex-protected read-modify-write. Then explain the key limitation: why can't you use `atomic.Int64` to safely implement a "check-then-act" operation on two separate variables?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete, runnable Go function `fanIn(ctx context.Context, channels ...<-chan int) <-chan int` that merges multiple input channels into a single output channel. The output channel must be closed when all input channels are drained (or when `ctx` is cancelled). Do not use reflection.

> _Your answer:_

---

**3.2** Write a function `withRetry(ctx context.Context, maxAttempts int, fn func(ctx context.Context) error) error` that calls `fn` up to `maxAttempts` times. Between attempts, sleep for an exponentially increasing backoff (100ms, 200ms, 400ms…). Stop early if `ctx` is cancelled. Return the last error if all attempts fail, or `nil` on success.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong._

**4.1** A teammate submits the following code to a code review. It is a function that launches a goroutine to perform a database query and returns the result:

```go
func queryAsync(userID int) <-chan string {
    result := make(chan string)
    go func() {
        name, err := db.QueryRow("SELECT name FROM users WHERE id = $1", userID).Scan()
        if err != nil {
            result <- "error: " + err.Error()
        } else {
            result <- name
        }
    }()
    return result
}

// Usage:
func handler(w http.ResponseWriter, r *http.Request) {
    ch := queryAsync(42)
    select {
    case name := <-ch:
        fmt.Fprintln(w, name)
    case <-r.Context().Done():
        http.Error(w, "timeout", http.StatusGatewayTimeout)
        return // handler returns here — who reads from ch?
    }
}
```

Identify **all** problems in this code:

a) What is the goroutine leak? Describe precisely which goroutine is stuck and why.

b) What other problem exists with the `db.QueryRow` call that has nothing to do with goroutines?

c) Rewrite `queryAsync` to fix the goroutine leak. Your rewrite should have the signature `func queryAsync(ctx context.Context, userID int) <-chan string`.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "Always run `go test -race` in CI, but never ship race-instrumented binaries to production." Explain both halves of this statement. What does the race detector instrument, what overhead does it add, and what class of bugs does it catch that normal testing does not? Why would those same properties make it inappropriate for production?

Consider at least two concrete scenarios: one where the race detector would catch a bug that passed all tests without `-race`, and one where running `-race` in production would be problematic.

> _Your answer (aim for 4–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Implement a generic, reusable `RateLimitedPool[T any]` type that combines a bounded worker pool with a token-bucket rate limiter. Specifically:

- The pool has a configurable number of workers and a configurable `rate.Limiter`
- `Submit(ctx context.Context, item T) error` adds an item to the work queue; blocks (or returns ctx error) if the queue is full
- Workers call `limiter.Wait(ctx)` before processing each item — this enforces the rate limit across all workers combined
- `Close()` closes the jobs channel and waits for all workers to finish

Write the type definition, `New`, `Submit`, `Close`, and a worker function. Show a usage example in `main`.

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
