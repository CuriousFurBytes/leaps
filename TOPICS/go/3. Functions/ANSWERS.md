# Answer Key — Module 3: Functions

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Copied text without understanding (you'll know)
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — append and call-by-value [1 pt]

**Full credit answer:**
When a slice is passed to a function, Go copies the slice header (a three-word struct containing a pointer to the backing array, the length, and the capacity). If `append` needs to grow the slice beyond its capacity, it allocates a new backing array and updates the **local copy** of the slice header — but the caller's original slice header is unchanged, so the caller still sees the old length and the old pointer.

**Key point required:** The slice header is copied; reassigning the local slice (which is what append does when it grows) does not affect the caller.

**Common wrong answers:**
- *"Because append returns a new slice"* — This is true but incomplete. The reason the caller doesn't see it is that the local copy of the slice header is what gets updated, not the caller's variable.
- *"Because Go uses pass-by-value"* — Correct in spirit but too vague for full credit. The answer needs to explain what specifically is copied (the slice header) and why updating it doesn't propagate back.

---

### 1.2 — zero value of a function type [1 pt]

**Full credit answer:**
The zero value of any function type in Go is `nil`. Calling a nil function value results in a **runtime panic**: `panic: runtime error: invalid memory address or nil pointer dereference`. Before calling a function variable that might be nil, check `if f != nil { f(...) }`.

**Key points required:**
- Zero value is `nil`
- Calling a nil function panics at runtime (not a compile error)

---

### 1.3 — the ... operator [1 pt]

**Full credit answer:**

(a) **In a parameter list** (`func sum(nums ...int) int`): declares a variadic parameter. The function accepts zero or more arguments of the given type. Inside the function, `nums` is a `[]int` — a slice of all the arguments passed.

(b) **At a call site** (`sum(slice...)`): spreads a slice into individual arguments. It unpacks `slice` so each element is passed as a separate argument to the variadic function. The type of the slice must match the variadic parameter type.

**Key points required:**
- In parameter: accepts variable number of arguments; parameter is a slice inside the function
- At call site: unpacks/spreads a slice into individual arguments

---

### 1.4 — naked returns [1 pt]

**Full credit answer:**
A naked return is a `return` statement with no explicit values, used inside a function that has named return values. The function returns the current values of its named return variables at that point. The Go community considers naked returns acceptable only in **very short functions** (typically ≤5 lines) where the named return variables are obvious from context and the function is simple enough that a bare `return` is unambiguous. In longer functions, naked returns harm readability — the reader must scroll to the signature to understand what a bare `return` returns.

**Key points required:**
- Naked return: `return` with no values in a function with named returns
- Acceptable only in short, simple functions — not in long functions

---

### 1.5 — error position in return list [1 pt]

**Full credit answer:**
By universal convention in Go, `error` is **always last** in the return list. For example, `func open(path string) (*File, error)` — the file is first, the error is last. This convention is so strong that violating it (e.g., `func f() (error, *File)`) will confuse every Go programmer who reads the code and will cause linters to flag it.

**Key point required:** Error is last, always.

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — what a closure captures [2 pts]

**Full credit answer:**
A closure captures **variables by reference**, not by value. It holds a reference to the variable itself — not a snapshot of the variable's value at the moment the closure was created. If the variable's value changes after the closure is created, the closure sees the new value the next time it executes.

Example:
```go
func makeCounter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

c := makeCounter()
fmt.Println(c()) // 1
fmt.Println(c()) // 2
fmt.Println(c()) // 3
```

`count` is declared in `makeCounter`'s scope. The returned closure captures a reference to `count`. Each call to `c()` reads and increments the same `count` variable. The output is `1`, `2`, `3` because the closure is modifying the shared captured variable across calls.

**Rubric:**
- 2 pts: Correctly states "by reference" (not by value), demonstrates with code where a closed-over variable is modified and the modification is visible on subsequent calls
- 1 pt: Correct general idea but says "by value" or is unclear on whether the closure sees changes to the variable after creation
- 0 pts: Describes a closure as simply "a function with no name" without addressing what it captures

---

### 2.2 — maps and call-by-value [2 pts]

**Full credit answer:**
Yes, the caller sees the insertion. A map value in Go is internally a pointer to a hash table data structure. When a map is passed to a function, Go copies the map header — but the copy still points to the same underlying hash table. Mutations to the map inside the function (insertions, deletions, updates) operate on the shared hash table and are visible to the caller.

This differs from passing an `int`: an `int` variable contains the integer value directly. When passed to a function, the integer value is copied into a new variable. Reassigning the function's parameter (`n = 5`) only affects the local copy — the caller's variable is unchanged.

The key difference: an `int` is a direct value, so copying the `int` gives an independent copy. A map is a reference type — copying the map header copies the pointer to the shared data structure, not the data structure itself.

**Rubric:**
- 2 pts: Correctly explains that the map copy points to the same hash table (so insertions are visible) AND correctly contrasts with `int` where the value itself is copied
- 1 pt: Correctly says insertions are visible but doesn't clearly explain the pointer-copy mechanism, or gets the int comparison wrong
- 0 pts: Says insertions are NOT visible (fundamental error), or says maps and ints behave the same way

---

### 2.3 — deferred closure and named return values [2 pts]

**Full credit answer:**
Named return values are variables that exist in the function's scope — they are declared implicitly by the function signature. A deferred closure can capture these variables by reference (just like capturing any other variable in the enclosing scope).

Execution order:
1. The function body runs. If an error occurs, `err` (a named return variable) is set to a non-nil value, and the function executes `return` (possibly a naked return).
2. Before the function actually returns to its caller, all deferred functions run in LIFO order. The deferred closure runs here. It reads the current value of `err` (the named return variable), and if non-nil, replaces it with a wrapped version.
3. The function returns to the caller with the modified `err` value — the caller sees the wrapped error, not the original.

The mechanism: named return variables are addressable variables in the function's scope. A deferred closure captures them by reference, so modifications to them in the deferred closure are reflected in the final return value.

One-sentence use case: Wrapping every error from a function with its name and context, without repeating `fmt.Errorf("funcName: %w", err)` on every `return` statement.

**Rubric:**
- 2 pts: Correctly describes all three phases of execution order AND correctly identifies that it works because named returns are variables captured by reference
- 1 pt: Correct general idea but execution order is unclear, or doesn't explain why a regular deferred call (`defer fmt.Println(err)`) captures the value at defer time but a closure captures by reference
- 0 pts: Says deferred closures cannot modify return values, or describes fundamentally wrong execution order

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — divide with named returns and defer wrapping [3 pts]

**Full credit answer:**
```go
package main

import (
    "errors"
    "fmt"
)

func divide(a, b float64) (result float64, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("divide: %w", err)
        }
    }()

    if b == 0 {
        err = errors.New("division by zero")
        return
    }
    result = a / b
    return
}

func main() {
    // Success case
    if r, err := divide(10, 3); err != nil {
        fmt.Println("error:", err)
    } else {
        fmt.Printf("10 / 3 = %.4f\n", r)
    }

    // Error case
    if _, err := divide(5, 0); err != nil {
        fmt.Println("error:", err)
    }
}
```

Expected output:
```
10 / 3 = 3.3333
error: divide: division by zero
```

**Rubric:**
- 3 pts: Correct named return values in signature; deferred closure captures `err` by reference and wraps on non-nil; correct `return` statements; correct caller usage with `if r, err := ...; err != nil` pattern
- 2 pts: Named returns and defer are correct but the caller usage is wrong (e.g., uses `if err != nil` without the init-statement form), or the defer wraps unconditionally (should only wrap when `err != nil`)
- 1 pt: Multiple return values are used but named returns and/or defer are missing or wrong
- 0 pts: Does not produce a correct divide function

---

### 3.2 — makeAdder and applyAll [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

// makeAdder returns a function that adds n to its argument.
func makeAdder(n int) func(int) int {
    return func(x int) int {
        return x + n  // n is captured from makeAdder's scope
    }
}

// applyAll applies each function in fns to x and returns the results.
func applyAll(fns []func(int) int, x int) []int {
    results := make([]int, len(fns))
    for i, f := range fns {
        results[i] = f(x)
    }
    return results
}

func main() {
    adders := []func(int) int{
        makeAdder(1),
        makeAdder(10),
        makeAdder(100),
    }

    results := applyAll(adders, 5)
    fmt.Println(results) // [6 15 105]
}
```

**Rubric:**
- 3 pts: `makeAdder` correctly returns a closure over `n`; `applyAll` correctly applies each function; correct output `[6 15 105]`; compiles and runs
- 2 pts: `makeAdder` is correct but `applyAll` has a minor bug (e.g., wrong loop variable), or `makeAdder` returns a function by value instead of as a closure (though in this case they're equivalent — full credit if the output is correct)
- 1 pt: `makeAdder` concept is right but the syntax is wrong (won't compile), or `applyAll` is missing/wrong
- 0 pts: Does not produce a working solution

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — loop-variable capture bug [3 pts] (1 pt each part)

**(a) Actual output on Go < 1.22:**
```
Handling route: /contact
Handling route: /contact
Handling route: /contact
```
All three handlers print the same route — the last value of `route` after the loop completes, which is `/contact`.

Execution trace: The `for i, route := range routes` loop (in Go < 1.22) creates one `route` variable that is reassigned on each iteration. All three closures capture a reference to the **same** `route` variable. By the time any handler is invoked (after the loop finishes), `route` holds its final value: `/contact`. All three closures print `/contact`.

**(b) Mechanism and Go 1.22 fix:**
The mechanism is loop variable sharing: in Go < 1.22, the `for range` loop creates one variable per loop variable (not one per iteration). All closures created in the loop body reference the same variable in memory. When the closures run after the loop, that variable holds the loop's final value.

Go 1.22 changed this by giving each iteration of a `for` loop its own copy of the loop variable (as if there is an implicit `route := route` at the start of each iteration). This makes the behavior match what most programmers expect — each closure captures the value of `route` at that iteration.

**(c) Pre-1.22 fix using variable shadowing:**
```go
for i, route := range routes {
    route := route  // shadow with a new per-iteration variable
    handlers[i] = func() {
        fmt.Printf("Handling route: %s\n", route)
    }
}
```

**Rubric:**
- 1 pt for (a): Correctly identifies that all three print `/contact` (the last route), with a correct explanation that the loop variable is shared
- 1 pt for (b): Correctly identifies that the mechanism is loop variable sharing (not separate variables per iteration in Go < 1.22), and correctly explains that Go 1.22 gives each iteration its own variable
- 1 pt for (c): Correct use of variable shadowing (`route := route` inside the loop); code compiles and would produce correct output

**Common wrong answers:**
- *"The output is `/home`, `/about`, `/contact`"* — This is what you'd get in Go 1.22+. In Go < 1.22, all closures capture the shared final value.
- For (b): *"Go 1.22 fixed a bug"* — Acceptable but should explain the mechanism; what specifically changed is the per-iteration variable scoping.

---

## Section 5: Discussion — Answer Key

### 5.1 — error as return value vs exceptions [2 pts]

**Example strong answer:**

First advantage (caller perspective): With explicit `(result, error)` returns, error handling is **visible and co-located with the call**. Every `v, err := f()` call site shows immediately that an error is possible. The caller cannot accidentally ignore the error without using `_` — a deliberate act. With exceptions, errors are invisible at the call site: `v = f()` looks like a normal call even if `f` might throw. This makes code review for error handling straightforward in Go, whereas exception-based code requires tracing the call stack to understand which exceptions might propagate.

Second advantage (compiler perspective): Go's compiler can verify that all returned values are **either used or explicitly discarded**. If you write `f()` without capturing any return values, the compiler warns about unused return values in some contexts, and the convention of `_, err := f()` makes deliberate discarding explicit. With exceptions, the compiler typically cannot verify that the caller handled all exception types — languages like Java tried with checked exceptions but it created its own verbosity problems. Go's approach is simpler: errors are values, and the type system tracks them like any other value.

**Elements that earn full credit:**
- Two distinct advantages (not just two phrasings of the same advantage)
- At least one addresses the caller's perspective and one the language/compiler perspective
- Accurate description of how exceptions differ (they are invisible at the call site, propagate silently)

**Rubric:**
- 2 pts: Two clearly distinct, well-reasoned advantages with accurate descriptions of both the Go approach and the exception contrast
- 1 pt: One strong advantage, or two weak/overlapping advantages without clear distinction
- 0 pts: Cannot articulate a concrete advantage, or confuses the two approaches

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — memoize function [+5 pts]

**Full credit answer:**
```go
package main

import "fmt"

// memoize returns a memoized version of f. Results are cached by input value.
// The cache is stored in the closure — no global state.
func memoize(f func(int) int) func(int) int {
    cache := make(map[int]int)  // each call to memoize creates a fresh cache
    return func(n int) int {
        if result, ok := cache[n]; ok {
            return result  // cache hit — return without calling f
        }
        result := f(n)
        cache[n] = result  // store in cache
        return result
    }
}

// slowFib counts calls to demonstrate memoization
var callCount int

func slowFib(n int) int {
    callCount++
    if n <= 1 {
        return n
    }
    return slowFib(n-1) + slowFib(n-2)
}

func main() {
    // Memoized fib — each unique input calls slowFib only once
    fastFib := memoize(slowFib)

    callCount = 0
    fmt.Printf("fib(10) = %d (calls: %d)\n", fastFib(10), callCount)

    callCount = 0
    fmt.Printf("fib(10) again = %d (calls: %d)\n", fastFib(10), callCount) // 0 calls — cached

    callCount = 0
    fmt.Printf("fib(5)  = %d (calls: %d)\n", fastFib(5), callCount)   // 0 calls — also cached

    // Two independent memoize calls have independent caches
    fastFib2 := memoize(slowFib)
    callCount = 0
    fmt.Printf("fib2(10) = %d (calls: %d)\n", fastFib2(10), callCount) // > 0 calls — fresh cache
}
```

**Expected output (approximate):**
```
fib(10) = 55 (calls: 177)
fib(10) again = 55 (calls: 0)
fib(5)  = 5 (calls: 0)
fib2(10) = 55 (calls: 177)
```

Note: The `callCount` for `fib(10)` using the unmemoized `slowFib` internally is 177 (the exponential recursion count for Fibonacci). After the first call, `fib(10)` is cached and subsequent calls take 0 invocations. `fib(5)` is also cached because `slowFib` is called recursively and `memoize` wraps only the outermost call — if you wanted deep memoization, you'd need to pass the memoized function to itself.

**Rubric:**
- 5 pts: Correct `memoize` using a `map[int]int` closure; demonstrates that repeated calls don't invoke `f` again; demonstrates that two calls to `memoize` produce independent caches; compiles and runs
- 3 pts: Correct memoize logic but independence between caches is not demonstrated, or the call counter demonstration is missing
- 1 pt: Correct structure (cache in closure, check before calling `f`) but has a bug (wrong cache key, race condition if concurrent calls were tested, etc.)
- 0 pts: Cache is stored globally (not in the closure) — misses the point of the exercise

---

## Common Wrong Answers Across the Test

1. **"Closures capture by value"** — The single most common error in this module. Closures capture variables by reference. The loop-variable bug (Question 4.1) is a direct consequence of this: the loop variable is shared by reference across all closures. Students who say "by value" will also get Question 2.1 wrong.

2. **"Append modifies the caller's slice"** — Students familiar with other languages (where arrays are reference types) often expect append to work like adding to a JavaScript array. In Go, append may return a new slice header with a new backing array; the caller's header is unchanged unless they reassign.

3. **"error can go anywhere in the return list"** — Some students think the error position is flexible. It is not by convention; it must be last. Linters (`golint`, `staticcheck`) will flag violations.

4. **Naked returns in long functions** — Students who learn named returns first often use naked returns everywhere. Full credit on 3.1 requires using naked returns only where they are clear (acceptable here because the function is short), but the discussion question (5.1) and scenario (4.1) reward students who show awareness of when naked returns are problematic.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who fail Section 2 (all three questions) likely need to re-read the module with active experimentation: write the counter closure, modify the variable from outside, and observe the result. The Feynman technique helps — explain "why does the loop-variable bug happen?" aloud without notes.
- Students who fail 3.1 (divide with named returns + defer) likely understand neither component in isolation. Recommend Exercise 7 from EXERCISES.md before retaking.
- Students who score < 1 on 4.1 part (a) may be running on Go 1.22+ where the bug is fixed. Clarify that the question asks about pre-1.22 behavior. If they correctly describe the 1.22+ behavior, give partial credit (0.5 pt) for demonstrating awareness of both behaviors.
- Section 5 (discussion) rewards students who can think about language design, not just syntax. A student who scores 0 here should be directed to read the "Why This Matters" section again, specifically the comparison with exception-based languages.
- The bonus question (6.1) is genuinely hard — full credit (5 pts) is exceptional. Most students will get 1–3 pts. The key insight being tested is that the cache is in the closure, not global.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
