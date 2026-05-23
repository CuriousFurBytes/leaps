# Test — Module 1: Types and Variables

**Topic:** [[go]]
**Module:** [[go/1. Types and Variables]]

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

**1.1** What is the zero value of an `int` in Go? What is the zero value of a `string`? What is the zero value of a pointer?

> _Your answer:_

---

**1.2** What does the `:=` operator do, and where can it be used? Where is it **not** allowed?

> _Your answer:_

---

**1.3** Name three integer types available in Go besides `int`.

> _Your answer:_

---

**1.4** What does `iota` represent in a Go constant block? What value does it start at, and when does it reset?

> _Your answer:_

---

**1.5** What is the difference between `byte` and `rune` in Go? What underlying types are they aliases for?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why Go requires explicit type conversion between numeric types and what class of bugs this prevents. Give a specific example of a bug that implicit conversion could cause.

> _Your answer:_

---

**2.2** A colleague says: _"Go's zero values are wasteful because you always have to initialize variables anyway — you end up writing `count := 0` instead of just `count :=`, so zero values don't save you any work."_

Is this claim correct? If not, what is the accurate understanding, and under what circumstances do zero values genuinely save effort?

> _Your answer:_

---

**2.3** Compare Go's type system to Python's. What are the tradeoffs of each approach? Under what circumstances would Go's static typing be a significant advantage? Under what circumstances might Python's dynamic typing be preferable?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete, runnable Go program that declares a `const` block using `iota` to represent the four cardinal directions (`North = 0`, `East = 1`, `South = 2`, `West = 3`) and prints each one with its numeric value.

Requirements:
- Use a `const` block with `iota`
- Print all four directions with their values in the format `North: 0`
- The program must compile (use correct `package main`, `import "fmt"`, and `func main()`)

> _Your answer:_

---

**3.2** Write a complete, runnable Go program that converts temperatures. Take three hardcoded Celsius values (`0.0`, `37.0`, `100.0`), convert each to Fahrenheit using the formula `F = C * 9/5 + 32`, and print both with exactly 2 decimal places using `fmt.Printf("%.2f°C = %.2f°F\n", c, f)`.

Requirements:
- Use `float64` for all temperature variables
- Use the correct formula (beware integer division)
- Output must match the format: `0.00°C = 32.00°F`

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** The following code is supposed to print the string `"65"` but prints `"A"` instead:

```go
package main

import "fmt"

func main() {
    n := 65
    fmt.Println(string(n))
}
```

Identify:

a) What is wrong?

b) Why does this happen? Explain the underlying mechanism.

c) How would you fix it? Write the corrected code.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** Go has no implicit type conversion between numeric types. Some developers find this verbose and frustrating — for example, you cannot add an `int` and a `float64` without an explicit cast. Others consider it one of Go's best features. Argue **for** or **against** this design decision with at least two specific examples. Justify your conclusion based on what you've learned in this module.

Consider at least two perspectives in your answer.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Go's integer types (`int8`, `int16`, `int32`, `int64`, `uint8`, etc.) have fixed sizes, but `int` and `uint` are platform-dependent (32-bit on 32-bit systems, 64-bit on 64-bit systems).

Explain when you would choose `int` vs. `int64` in production code. Your answer should specifically address:
- What risks arise from choosing `int` for values that may be stored, serialized, or sent over a network
- What risks arise from choosing `int64` for general-purpose counters and indices
- How the choice interacts with Go's `encoding/json` package and other serialization formats
- What the Go standard library itself does (for example, what type does `len()` return, and why?)

This may require combining knowledge from this module with independent reasoning beyond the module content.

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
|------|---------|--------|--------|--------|--------|--------|-----------|------------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
