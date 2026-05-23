# Test — Module 2: Control Flow

**Topic:** [[go]]
**Module:** [[go/2. Control Flow]]

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

**1.1** Does Go require parentheses around the condition in an `if` statement? For example, is `if (x > 0) { ... }` valid Go?

> _Your answer:_

---

**1.2** How many loop constructs does Go have? Name them all (including any keyword aliases or variants).

> _Your answer:_

---

**1.3** Does Go's `switch` statement fall through between cases by default? What keyword do you use if you want explicit fall-through behavior?

> _Your answer:_

---

**1.4** When does a deferred function call actually execute — at the `defer` statement, or at some other time? Be specific.

> _Your answer:_

---

**1.5** What does `continue` do inside a Go `for` loop? How does it differ from `break`?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain the "init statement" in a Go `if` expression. Give a concrete example. Why is this pattern useful, and what is the scope of any variable declared in the init statement?

> _Your answer:_

---

**2.2** Go has no `while` keyword and no `do-while` keyword. Explain how you simulate each of these two loop patterns using Go's `for` loop. Why might the Go designers have made this consolidation intentional rather than accidental?

> _Your answer:_

---

**2.3** Explain the LIFO (last-in, first-out) execution order of deferred calls. Give a concrete scenario — for example, acquiring multiple resources in sequence — to illustrate why this ordering is useful rather than arbitrary.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go program that:
- Declares the map `scores := map[string]int{"Alice": 90, "Bob": 85, "Carol": 92}`
- Uses `for range` to iterate over the map and print each name and score (e.g., `Alice: 90`)
- After the loop, computes and prints the average score

Note: map iteration order in Go is not guaranteed — your output order may differ from the expected output, and that is correct.

> _Your answer:_

---

**3.2** Write a Go function `classify(n int) string` that returns:
- `"negative"` for any `n < 0`
- `"zero"` for `n == 0`
- `"small"` for `1 <= n <= 9`
- `"medium"` for `10 <= n <= 99`
- `"large"` for `n >= 100`

Use a `switch` statement (not `if`/`else if`). Show how you would call and test this function with at least 5 different values.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** The following code is supposed to print only the matching case's output — `"one"` when `n` is 1, `"two"` when `n` is 2, `"three"` when `n` is 3. But a programmer who came from C has written it with `fallthrough` everywhere, which causes unexpected behavior:

```go
switch n {
case 1:
    fmt.Println("one")
    fallthrough
case 2:
    fmt.Println("two")
    fallthrough
case 3:
    fmt.Println("three")
}
```

Identify:

a) What actually happens when this code runs with `n = 2`? Trace the execution precisely.

b) Why does this happen? Explain what `fallthrough` does in Go — specifically, does it check the next case's condition or not?

c) The programmer's underlying goal was probably: "I want to match any of 1, 2, or 3 and do the same thing." Rewrite the switch correctly for that goal, and also rewrite it for the original goal (each number prints its own word).

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "Using `defer` inside a `for` loop is a common source of resource leaks in Go." Explain why this statement is true. Describe the pattern that correctly handles per-iteration cleanup, and explain why it works where `defer`-in-a-loop does not.

Consider at least two perspectives in your answer: what the programmer likely intended vs. what actually happens, and how Go's design of `defer` (scoped to function return) makes this a natural pitfall.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Go's `for...range` loop over a string iterates over Unicode **runes**, not bytes. Write a complete Go program that demonstrates this with the string `"café"` and shows all four of the following:

1. The byte length using `len()`
2. The rune count using `utf8.RuneCountInString()`
3. Iteration using `range` — print each rune's byte index and its Unicode code point value
4. A brief explanation (in a comment or print statement) of why `range` is safer than byte indexing for Unicode text, based on what your program's output shows

Bonus points for also showing what byte indexing (`s[i]`) produces vs. rune indexing for the `é` character specifically.

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
