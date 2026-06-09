# Test — Module 16: Performance and Profiling

**Topic:** [[go]]
**Module:** [[go/16. Performance and Profiling]]

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

**1.1** What does the `-benchmem` flag add to the output of `go test -bench`? Name the two additional columns and what each measures.

> _Your answer:_

---

**1.2** Name the five profile types that Go's `pprof` supports and state in one sentence what each measures.

> _Your answer:_

---

**1.3** What does `b.ResetTimer()` do in a Go benchmark, and when should you call it?

> _Your answer:_

---

**1.4** What is `GOMEMLIMIT` and in which Go version was it introduced?

> _Your answer:_

---

**1.5** What command-line flag do you pass to `go build` to see escape analysis output? Write the exact command.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain what "dead-code elimination" means in the context of Go benchmarks. Why does assigning a function's return value to `_` fail to prevent it? What is the correct fix, and why does it work?

> _Your answer:_

---

**2.2** A colleague says: "I noticed our service is slow, so I rewrote the JSON serialization layer — it's much faster now." Critique this workflow from the perspective of the performance mindset taught in this module. What should they have done first, and why?

> _Your answer:_

---

**2.3** Explain why heap allocations matter for performance in Go. What is the mechanism by which many small allocations slow down a program? Connect your answer to Go's garbage collector. Reference [[memory-management]] and [[go/17. Runtime Internals and the Memory Model]] in your explanation.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a correct, complete benchmark for the following function. Your benchmark must:
- Use a package-level sink variable to prevent dead-code elimination
- Call `b.ResetTimer` after setup
- Use a realistic 100-element input
- Work with Go 1.22+ range-over-integer syntax

```go
func countVowels(s string) int {
    count := 0
    for _, r := range s {
        switch r {
        case 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U':
            count++
        }
    }
    return count
}
```

> _Your answer:_

---

**3.2** You are given the following function. Run `go build -gcflags='-m'` in your head (or actually run it) and identify which allocations occur. Then rewrite the function to eliminate all heap allocations without changing the function's behavior.

```go
type Point struct{ X, Y float64 }

func midpoint(a, b Point) *Point {
    return &Point{
        X: (a.X + b.X) / 2,
        Y: (a.Y + b.Y) / 2,
    }
}
```

Explain your change and confirm (with `-gcflags=-m` output or reasoning) that the rewrite eliminates the escape.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze the following broken benchmark and identify all issues._

**4.1** A developer reports that their image-decoding function is "incredibly fast — only 0.8 ns/op!" Here is their benchmark:

```go
func BenchmarkDecodeImage(b *testing.B) {
    imageData, _ := os.ReadFile("testdata/sample.png") // takes ~5ms

    for i := 0; i < b.N; i++ {
        decodeImage(imageData) // returns *Image — result not captured
    }
}
```

Identify:

a) What is wrong with this benchmark? List every bug you can find.

b) What do each of the bugs cause — specifically, how does each distort the reported `ns/op`?

c) Write the corrected benchmark.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "You should always preallocate slices and maps with a capacity hint." Evaluate this statement. Under what conditions is preallocation clearly the right choice? Are there cases where it adds complexity without benefit? How do you decide whether to preallocate in practice?

Consider at least two perspectives in your answer: the performance case for preallocation and the cases where it is overkill or misleading.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Profile-Guided Optimization (PGO) was enabled by default in Go 1.21. Explain:

a) The mechanism by which PGO improves performance — what specifically does the compiler do differently when a `default.pgo` file is present?

b) The steps required to collect a profile and apply it (write the exact commands)

c) What types of Go programs benefit most from PGO, and why?

d) A limitation or caveat of PGO that engineers should be aware of when adopting it in a CI pipeline

This question may require combining knowledge from this module with [[go/17. Runtime Internals and the Memory Model]] and independent reasoning.

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
