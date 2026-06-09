# Test — Module 4: Composite Types

**Topic:** [[go]]
**Module:** [[go/4. Composite Types]]

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

**1.1** What are the three fields of a slice header? For each field, briefly describe what it contains.

> _Your answer:_

---

**1.2** What is the zero value of a map in Go? Is it safe to read from a zero-value map? Is it safe to write to a zero-value map?

> _Your answer:_

---

**1.3** Does assigning an array to a new variable copy the array's data, or does the new variable share the same underlying data as the original? Answer for both arrays and slices.

> _Your answer:_

---

**1.4** What is the comma-ok idiom for maps? Write the syntax and explain when you need to use it (as opposed to a simple `v := m[key]` read).

> _Your answer:_

---

**1.5** In Go, what is `struct{}`? What is it most commonly used for?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain what happens in memory when `append` is called on a slice that has reached its capacity. Walk through the steps: what does the runtime do, what happens to the original backing array, and why must you always assign the return value of `append`?

> _Your answer:_

---

**2.2** Map iteration order in Go is deliberately randomized. Explain why the Go team made this design decision (what problem does it prevent?), and describe the correct approach when you need to iterate over a map in sorted key order.

> _Your answer:_

---

**2.3** Go's `string` type is described as "an immutable, read-only slice of bytes." Explain what "immutable" means in this context — specifically, what you can and cannot do with a `string` variable, and why the conversions `string → []byte` and `string → []rune` each allocate new memory.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go function `invertMap(m map[string]int) map[int][]string` that inverts a `map[string]int` into a `map[int][]string` — the original values become keys, and the original keys are grouped into slices under their former value.

For example: `{"a": 1, "b": 2, "c": 1}` → `{1: ["a", "c"], 2: ["b"]}` (slice order within each group may vary).

Call this function in `main` with at least two test cases: one where values repeat and one where all values are unique.

> _Your answer:_

---

**3.2** Write a Go function `removeDuplicates(s []int) []int` that returns a new slice with consecutive duplicate integers removed (keeping the first occurrence of each run). For example: `[1, 1, 2, 3, 3, 3, 2, 2]` → `[1, 2, 3, 2]`.

Do not sort the input. The function should run in O(n) time and O(n) space.

Show at least three test cases including an empty slice and a single-element slice.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague writes the following function to add items to a shared slice and is confused why it "doesn't work":

```go
func addAll(s []int, items []int) {
    for _, item := range items {
        s = append(s, item)
    }
    // The caller's slice never gets the new items
}

func main() {
    result := []int{1, 2, 3}
    addAll(result, []int{4, 5, 6})
    fmt.Println(result) // prints [1 2 3], not [1 2 3 4 5 6]
}
```

Answer:

a) Explain precisely why `result` in `main` still contains only `[1 2 3]` after calling `addAll`. Your explanation must mention the slice header and what gets copied when the function is called.

b) Describe two different ways to fix this: one that involves returning the slice from `addAll`, and one that uses a pointer.

c) Which of the two fixes is more idiomatic Go and why?

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "In Go, arrays and structs have value semantics while slices and maps have reference semantics." Explain what this statement means in concrete terms — what actually happens in memory when you assign or pass each type. Then explain the practical consequence: when does value semantics cause a bug, and when does reference semantics cause a bug? Give one concrete example of each.

Consider both correctness and performance in your answer: value semantics can cause performance problems (copying large data unnecessarily), and reference semantics can cause correctness problems (unexpected mutations). How does Go's design of the slice header (a value type containing a reference) navigate this tradeoff?

> _Your answer (aim for 4–8 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Implement a generic stack data structure in Go using a struct and a slice as its backing store. The stack should support:
- `Push(v T)` — add an element to the top
- `Pop() (T, bool)` — remove and return the top element; `bool` is false if empty
- `Peek() (T, bool)` — return the top element without removing; `bool` is false if empty
- `Len() int` — return the number of elements

Requirements:
- Use Go generics (`type Stack[T any] struct { ... }`)
- The zero value of `Stack[T]` should be usable without initialization (no `New` function required)
- `Pop` and `Peek` on an empty stack must not panic — return the zero value and `false`
- Write a `main` function demonstrating all operations including the empty-stack edge case

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
