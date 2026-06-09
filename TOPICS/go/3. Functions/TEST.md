# Test — Module 3: Functions

**Topic:** [[go]]
**Module:** [[go/3. Functions]]

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

**1.1** Go uses call-by-value for all function arguments. Given this, explain in one sentence why a function that calls `append` on a slice parameter does not cause the caller's slice to grow.

> _Your answer:_

---

**1.2** What is the zero value of a function type in Go (e.g., `var f func(int) int`)? What happens if you call a function variable that holds this zero value?

> _Your answer:_

---

**1.3** What does the `...` operator do in each of these two positions: (a) in a function parameter list — `func sum(nums ...int) int`, and (b) at a call site — `sum(slice...)`?

> _Your answer:_

---

**1.4** What is a naked return? In what circumstances does the Go community consider it acceptable to use one?

> _Your answer:_

---

**1.5** Go functions can return multiple values. By convention, if a function can fail, where does the `error` value appear in the return list — first, last, or it doesn't matter?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain precisely what a closure captures — is it the value of a variable at the moment the closure is created, or something else? Illustrate your answer with a short code example that shows a closure modifying a captured variable, and explain what output the code produces and why.

> _Your answer:_

---

**2.2** Explain the call-by-value semantics for maps in Go. Specifically: if you pass a `map[string]int` to a function and the function inserts a new key, does the caller see that insertion? Why or why not? How does this differ from what happens when you pass an `int` to a function and the function reassigns its parameter?

> _Your answer:_

---

**2.3** Explain how a deferred closure can modify a function's named return value. Walk through the execution order: (1) when does the function body run, (2) when does the deferred closure run, and (3) what mechanism allows the closure to affect what the caller receives? Give a one-sentence use case for this technique.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go function `divide(a, b float64) (result float64, err error)` using named return values. The function should:
- Return `0, errors.New("division by zero")` if `b == 0`
- Otherwise return `a/b, nil`
- Include a `defer` that, if `err` is non-nil, wraps it with `fmt.Errorf("divide: %w", err)`

Show how you would call this function for both the error and success cases and handle the result idiomatically.

> _Your answer:_

---

**3.2** Write a function `makeAdder(n int) func(int) int` that returns a closure. The closure, when called with argument `x`, returns `x + n`. Then write a function `applyAll(fns []func(int) int, x int) []int` that applies each function in `fns` to `x` and returns a slice of results.

Use `makeAdder` to create three adder functions (add 1, add 10, add 100) and call `applyAll` with them and the input value `5`. Print the result.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A developer is building a web service. They write the following code to register URL handlers that each remember which route they handle:

```go
routes := []string{"/home", "/about", "/contact"}
handlers := make([]func(), len(routes))

for i, route := range routes {
    handlers[i] = func() {
        fmt.Printf("Handling route: %s\n", route)
    }
}

// Later, when each handler is invoked:
for _, h := range handlers {
    h()
}
```

The developer expects the output to be:
```
Handling route: /home
Handling route: /about
Handling route: /contact
```

But on Go versions before 1.22, the output is different.

a) What is the actual output on Go < 1.22? Trace the execution and explain why.

b) What fundamental mechanism causes this behavior, and how does Go 1.22 address it?

c) Rewrite the loop using the variable shadowing technique so it works correctly on all Go versions (including pre-1.22).

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** Go's choice to make `error` an ordinary return value (rather than using exceptions like Java/Python) is closely tied to functions returning multiple values. Discuss: what are two concrete advantages of the explicit `(result, error)` return convention compared to exception-based error handling? Consider both the caller's perspective (what the calling code looks like) and the compiler's perspective (what guarantees the language can provide).

> _Your answer (aim for 4–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Write a function `memoize(f func(int) int) func(int) int` that returns a memoized version of `f`. The memoized function caches results: on first call with input `n`, it calls `f(n)`, stores the result, and returns it. On subsequent calls with the same `n`, it returns the cached result without calling `f` again.

Requirements:
- The cache must be stored in the closure (no global variables)
- Use a `map[int]int` as the cache
- Demonstrate the memoization by wrapping a slow Fibonacci function and showing that repeated calls with the same argument are fast (you can simulate "slow" with a call counter rather than an actual sleep)
- Show that two calls to `memoize(fib)` produce two independent caches

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
