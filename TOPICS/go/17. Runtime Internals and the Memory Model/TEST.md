# Test — Module 17: Runtime Internals and the Memory Model

**Topic:** [[go]]
**Module:** [[go/17. Runtime Internals and the Memory Model]]

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

**1.1** What are G, M, and P in Go's scheduler? Define each in one sentence.

> _Your answer:_

---

**1.2** What is the approximate initial stack size of a goroutine, and how does the stack grow when it is nearly full? (Name the mechanism — not just "it gets bigger.")

> _Your answer:_

---

**1.3** Go's GC is described as "tri-color." What are the three colors, and what does each color mean for an object during a GC cycle?

> _Your answer:_

---

**1.4** What is `GOMEMLIMIT` (introduced in Go 1.19), and how does it differ in purpose from `GOGC`?

> _Your answer:_

---

**1.5** What is asynchronous preemption in the Go scheduler (introduced in Go 1.14)? Why was it needed?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why write barriers are necessary for the concurrent tri-color mark-and-sweep GC. What invariant do they maintain, and what could go wrong without them?

> _Your answer:_

---

**2.2** A colleague says: "If I use `time.Sleep(100 * time.Millisecond)` before reading a value that was written by a goroutine, I'm safe — the goroutine definitely finished writing." Is this correct? Explain precisely, citing the Go Memory Model.

> _Your answer:_

---

**2.3** Explain the real costs of a cgo call compared to a regular Go function call. Name at least three distinct costs (not just "it's slower") and explain the mechanism behind the scheduler-related cost.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Is the following program correctly synchronized? State whether it has a data race, which variable(s) are affected, and — if it is racy — what the minimal fix is. Cite the specific memory-model rule that applies.

```go
var result int

func compute() {
    result = heavyComputation()
}

func main() {
    go compute()
    // ... do some other work (no synchronization) ...
    fmt.Println(result)
}
```

> _Your answer:_

---

**3.2** You are running a Go microservice in a Docker container limited to 256 MiB. The service's typical live heap is 60 MiB. GC pauses are causing occasional latency spikes. Write the Go code to configure `GOGC` and `GOMEMLIMIT` appropriately, and explain your choices.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A senior engineer shows you this code, claiming it is a correctly synchronized, lock-free counter:

```go
package main

import "fmt"

var counter int // shared between goroutines

func increment() {
    counter++ // not protected by any lock or atomic
}

func main() {
    for i := 0; i < 1000; i++ {
        go increment()
    }
    // Wait "long enough" for all goroutines to finish
    // (no WaitGroup or channel — just trusting the scheduler)
    fmt.Println(counter)
}
```

Identify:

a) What is wrong with `counter++` in a concurrent context? Is this a data race?

b) Why is "trusting the scheduler" (no WaitGroup, no channel) also incorrect, even if `counter++` were atomic?

c) Provide the corrected version using `sync/atomic` for the increment and a `sync.WaitGroup` for synchronization.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** Go's garbage collector is non-generational and non-compacting — both deliberate design choices. Explain what each of these terms means, what tradeoff each choice makes compared to a generational or compacting design, and in what types of workloads the Go GC's design might be a disadvantage.

Consider at least two perspectives in your answer: what you gain from the Go design, and what you might give up compared to a JVM-style generational compacting GC.

> _Your answer (aim for 4–7 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** The following code is intended to be a fast, unsafe conversion from `string` to `[]byte` without allocation. Analyze it critically:

```go
import (
    "reflect"
    "unsafe"
)

func unsafeStringToBytes(s string) []byte {
    sh := (*reflect.StringHeader)(unsafe.Pointer(&s))
    bh := reflect.SliceHeader{
        Data: sh.Data,
        Len:  sh.Len,
        Cap:  sh.Len,
    }
    return *(*[]byte)(unsafe.Pointer(&bh))
}
```

a) Does this code work correctly on current Go versions? What is the danger if the returned `[]byte` is modified?

b) This pattern uses `reflect.StringHeader` and `reflect.SliceHeader`, which are deprecated since Go 1.20. What are the correct Go 1.20+ functions to use instead, and why are they considered safer?

c) Write the corrected version using only the modern API.

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
