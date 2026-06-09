# Test — Module 9: Concurrency

**Topic:** [[go]]
**Module:** [[go/9. Concurrency]]

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
| Section 4: Scenario / Debugging | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** What is the difference between concurrency and parallelism? Give a one-sentence definition of each.

> _Your answer:_

---

**1.2** What happens when Go's `main` function returns while goroutines are still running?

> _Your answer:_

---

**1.3** What is the difference between an unbuffered channel and a buffered channel? When does a send on each type block?

> _Your answer:_

---

**1.4** What does `sync.WaitGroup.Add(n)` do, and why must it be called before launching the goroutine (not inside it)?

> _Your answer:_

---

**1.5** What does closing a channel with `close(ch)` signal to receivers? What happens if you send to a closed channel?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain the "loop variable capture" goroutine bug. Why does it happen, what does the incorrect output look like, and what are two ways to fix it?

> _Your answer:_

---

**2.2** Explain the behavior of a `select` statement when:
  a) No case is ready and there is no `default` case
  b) No case is ready and there is a `default` case
  c) Multiple cases are ready simultaneously

> _Your answer:_

---

**2.3** Go's concurrency proverb is "Do not communicate by sharing memory; share memory by communicating." Explain what this means in practice. Give a scenario where channels are the right tool AND a scenario where a `sync.Mutex` is actually the better choice.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go program that:
- Launches 4 goroutines, each computing the square of its goroutine ID (1 through 4)
- Uses a channel of sufficient capacity to collect all 4 results
- Uses `sync.WaitGroup` to close the channel after all goroutines finish
- Iterates the channel with `range` to print all results
- Is free of data races (no shared mutable state other than the channel)

> _Your answer:_

---

**3.2** Write a function `withRetry(fn func() error, attempts int, delay time.Duration) error` that:
- Calls `fn()` up to `attempts` times
- If `fn()` returns `nil`, returns `nil` immediately
- Between attempts, waits `delay` using a goroutine + channel + `select` approach (not `time.Sleep` directly in the function body) — or alternatively uses `time.After` in a `select` to implement the delay
- If all attempts fail, returns the last error

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** The following program is intended to launch 5 goroutines, have them all report their ID through a channel, and print all 5 IDs. Instead it deadlocks. Analyze the program carefully:

```go
package main

import "fmt"

func main() {
    ch := make(chan int)

    for i := 1; i <= 5; i++ {
        go func(id int) {
            ch <- id
        }(i)
    }

    for i := 0; i < 5; i++ {
        fmt.Println(<-ch)
    }

    fmt.Println("all done")
}
```

a) Does this program actually deadlock? Trace through the execution and explain what happens step by step. If it does not deadlock, explain what it actually does.

b) Now consider a variant: what if the loop bounds were `i <= 6` for the goroutines (6 goroutines) but still only `i < 5` in the receive loop (5 receives)? What happens to the 6th goroutine?

c) What change to the program would allow it to also print `"all done"` reliably in the variant from (b)?

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "The Go race detector is not a proof of correctness — a program that passes `-race` may still have data races." Explain why this is true. What does the race detector actually detect, and what can it miss? How should the race detector fit into a testing and CI strategy for a concurrent Go program?

Consider at least two perspectives: what the race detector detects vs. what it can miss, and the practical implication for how much to trust `-race` passing.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Implement a `merge` function with this signature:

```go
func merge(channels ...<-chan int) <-chan int
```

The function takes an arbitrary number of input channels and returns a single output channel that emits all values from all input channels. The output channel is closed when all input channels are closed. Each input channel is drained by a separate goroutine.

Requirements:
- Use `sync.WaitGroup` to coordinate closing the output channel
- Each input goroutine uses `for range` to drain its channel
- The function should work correctly for 0, 1, 2, or N input channels
- The result channel is closed exactly once, after all input channels are exhausted
- Include a `main` function that demonstrates merging 3 channels

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
