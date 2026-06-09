# Test — Module 10: Generics

**Topic:** [[go]]
**Module:** [[go/10. Generics]]

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

**1.1** What Go version introduced generics, and in what year was it released?

> _Your answer:_

---

**1.2** What is the difference between the `any` constraint and the `comparable` constraint? When would you use each?

> _Your answer:_

---

**1.3** What does the `~` (tilde) operator mean in a constraint? For example, what is the difference between `int` and `~int` in a union element?

> _Your answer:_

---

**1.4** Can a method on a generic type introduce a new type parameter? For example, is `func (s *Stack[T]) Map[U any](f func(T) U) []U` valid Go?

> _Your answer:_

---

**1.5** Name the three standard library packages added in Go 1.21 that use generics. What is the primary purpose of each?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Before Go 1.18, Go developers used two main approaches to write reusable code that worked across multiple types: `interface{}` with type assertions, and copy-paste per type. Explain the concrete problem with each approach and how generics solves both problems simultaneously.

> _Your answer:_

---

**2.2** Explain what "constraints are interfaces" means. How does a constraint differ from a plain interface used as a function parameter? Give an example where using a generic constraint is correct and an example where a plain interface is the better choice.

> _Your answer:_

---

**2.3** Explain Go's GC shape stenciling approach to implementing generics. How does it differ from C++'s full monomorphization? What are the practical performance implications for a Go developer using generics in production code?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go generic function `Keys[K comparable, V any](m map[K]V) []K` that returns a slice of all keys in a map. Then write `Values[K comparable, V any](m map[K]V) []V` for values. Demonstrate both with a `map[string]int` containing at least three entries. (Note: map iteration order is non-deterministic — your output order may vary.)

> _Your answer:_

---

**3.2** Write a generic `Stack[T any]` type with `Push`, `Pop` (returning `T, bool`), and `Len` methods. Use it to implement a simple expression evaluator that processes a `[]string` of tokens: for each token, if it's a number push it; if it's `"+"` pop two values and push their sum; print the final result. Use a `Stack[int]`.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague wrote the following generic function and is getting a compile error:

```go
func FindMin[T any](s []T) T {
    if len(s) == 0 {
        return nil
    }
    min := s[0]
    for _, v := range s[1:] {
        if v < min {
            min = v
        }
    }
    return min
}
```

Identify **all** the errors in this function (there are at least two). For each error, explain:

a) What the error is and why it's a compile error (not just a runtime issue)

b) How to fix it

Write the corrected version of the function.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** The Go blog post "When To Use Generics" identifies three scenarios where generics are appropriate and discourages their use in other cases. Summarize those three scenarios in your own words. Then give a concrete example from your own experience or imagination where you would reach for generics, and one where you would deliberately choose a plain interface instead. Explain your reasoning for each choice.

> _Your answer (aim for 4–8 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Implement a generic `OrderedMap[K cmp.Ordered, V any]` type that stores key-value pairs in sorted key order. It should support:
- `Set(key K, value V)` — insert or update
- `Get(key K) (V, bool)` — look up by key
- `Keys() []K` — return all keys in sorted order
- `Values() []V` — return all values in key-sorted order

The internal storage should use two parallel slices (`keys []K`, `values []V`) kept in sorted order. `Set` should maintain sorted order by finding the correct insertion point using binary search.

Demonstrate with `OrderedMap[string, int]` containing at least 5 entries added in non-alphabetical order, showing that `Keys()` returns them sorted.

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
