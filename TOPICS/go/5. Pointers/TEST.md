# Test — Module 5: Pointers

**Topic:** [[go]]
**Module:** [[go/5. Pointers]]

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

**1.1** What does the `&` operator do in Go? Give a one-line example showing its use with a variable.

> _Your answer:_

---

**1.2** What is the zero value of any pointer type in Go? What happens at runtime if you dereference that zero value?

> _Your answer:_

---

**1.3** What is the difference between `new(T)` and `&T{}`? When would you prefer one over the other?

> _Your answer:_

---

**1.4** If `p` is `*Point` and `Point` has a field `X float64`, how do you read and write the `X` field through `p`? Do you need to write `(*p).X`, or is there a shorter form?

> _Your answer:_

---

**1.5** Go passes all function arguments by value. Given this, explain in one sentence why a function receiving `*MyStruct` can modify the caller's struct, even though the pointer itself is passed by value.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain Go's "call-by-value" model, and walk through what happens in memory when you call `update(p *Person)` vs `update(p Person)`. Why does the pointer version allow mutation and the value version does not? Be specific about what is copied in each case.

> _Your answer:_

---

**2.2** A colleague says: "I always pass maps as `*map[K]V` to functions that modify them, to make sure the changes are visible to the caller." Is this correct? What do they have right, and what do they have wrong? Explain what a map value actually is under the hood.

> _Your answer:_

---

**2.3** Explain escape analysis in your own words. Why is it safe in Go to return the address of a local variable (`return &x`) — something that would be undefined behavior in C? What does the compiler do to make this safe, and what is the runtime cost?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go program that:
- Defines a struct `BankAccount` with `Owner string` and `Balance float64`
- Writes a function `deposit(a *BankAccount, amount float64)` that adds `amount` to `a.Balance`
- Writes a function `withdraw(a *BankAccount, amount float64) error` that subtracts `amount` if sufficient funds exist, or returns an error
- In `main`, creates an account, deposits 200.00, withdraws 50.00, attempts to withdraw 500.00 (expecting an error), and prints the final balance

> _Your answer:_

---

**3.2** Write a function `findFirst(s []int, pred func(int) bool) *int` that returns a pointer to the first element in `s` satisfying `pred`, or `nil` if no element qualifies. Then write a `main` that calls it with `[]int{4, 7, 2, 9, 1}` and `pred` = "is odd", prints the value if found, and handles the nil case.

Note: returning `&s[i]` for a slice element is valid Go.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A developer writes the following code to count words in a slice of strings. The intent is to use a shared counter that both `countWords` and `main` can see:

```go
func countWords(words []string, count int) {
    for _, w := range words {
        if len(w) > 0 {
            count++
        }
    }
}

func main() {
    words := []string{"hello", "world", "", "go"}
    total := 0
    countWords(words, total)
    fmt.Println("Total:", total)  // prints 0, expected 3
}
```

Identify:

a) What is wrong with this code? Trace what happens to `count` and `total`.

b) Why does this happen? Name the Go feature that causes it.

c) Fix the code. Show the corrected `countWords` signature and any changes to `main`. Give two valid fixes: one using a pointer argument, one using a return value.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "In Go, you should use pointers sparingly — only when you have a specific reason to. The default should be to pass values." Do you agree with this statement? Argue for or against it, covering at least three of the following considerations: mutation intent, struct size, reference-like types (slices/maps), optional/nullable values, and the impact on garbage collection.

Consider the perspective of a developer reading your API: what does passing a pointer vs a value communicate about ownership and mutation intent?

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Implement a generic `Set[T comparable]` type as a struct wrapping a `map[T]struct{}`. Provide three methods: `Add(value T)`, `Contains(value T) bool`, and `Size() int`. All methods should use pointer receivers (`*Set[T]`) where appropriate and value receivers where that is preferable. Write a `main` function demonstrating the set with `int` values.

Then explain: why should `Add` use a pointer receiver but `Contains` and `Size` could use either? What rule guides this decision, and how does it connect to what you learned about pointer semantics in this module?

(This question previews [[go/6. Methods and Interfaces]] and [[go/10. Generics]] — use your best reasoning even if you haven't studied those modules yet.)

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
