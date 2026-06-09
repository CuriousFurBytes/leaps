# Exercises — Module 3: Functions

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just run code mentally — actually write or type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Expert | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Basic Function Declaration [🟢 Easy] [1 pt]

### Context
The most fundamental skill in this module is writing a function with the correct signature and making it handle multiple cases correctly. `clamp` is a common utility function — it constrains a value to a range. This exercise ensures you can write a basic three-way decision in a function.

### Task
Write a Go function `clamp(val, min, max int) int` that returns `val` constrained to the closed interval `[min, max]`:
- If `val < min`, return `min`
- If `val > max`, return `max`
- Otherwise return `val`

Call the function with at least 5 values that exercise all three branches and print the results.

### Requirements
- [ ] Function signature is exactly `clamp(val, min, max int) int`
- [ ] Returns the correct value for `val` below range, above range, and within range
- [ ] At least 5 test calls covering all three branches
- [ ] Program compiles and runs without errors

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Use an `if`/`else if`/`else` chain in the function body. Check `val < min` first, then `val > max`, then fall through to the default case. A `switch` also works here.

</details>

### Expected Output / Acceptance Criteria
For inputs like -5, 0, 5, 10, 15 with range [0, 10]:
```
clamp(-5, 0, 10) = 0
clamp(0, 0, 10)  = 0
clamp(5, 0, 10)  = 5
clamp(10, 0, 10) = 10
clamp(15, 0, 10) = 10
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

// clamp constrains val to the closed interval [min, max].
func clamp(val, min, max int) int {
    if val < min {
        return min
    }
    if val > max {
        return max
    }
    return val
}

func main() {
    testCases := [][3]int{
        {-5, 0, 10},
        {0, 0, 10},
        {5, 0, 10},
        {10, 0, 10},
        {15, 0, 10},
    }
    for _, tc := range testCases {
        result := clamp(tc[0], tc[1], tc[2])
        fmt.Printf("clamp(%3d, %d, %d) = %d\n", tc[0], tc[1], tc[2], result)
    }
}
```

**Explanation:**
The function signature `clamp(val, min, max int) int` uses the shorthand for consecutive parameters of the same type — `val, min, max int` instead of `val int, min int, max int`. The two `if` statements check the boundary cases; if neither fires, we fall through to `return val`. This is Go's idiomatic early-return style: check for degenerate cases at the top and return immediately, leaving the normal case for the end.

**Common wrong answers and why they fail:**
- Using `if val < min { return min } else if val > max { return max } else { return val }` — this works but the `else` after a `return` is unnecessary and non-idiomatic; Go style is to use early returns without `else`
- Forgetting the inclusive boundaries and using `<` vs `<=` — `clamp(0, 0, 10)` should return 0 (not min), which means the boundary check must be `val < min` (strict less), not `val <= min`

</details>

---

## Exercise 2: Call-by-Value Prediction [🟢 Easy] [1 pt]

### Context
Understanding precisely what call-by-value means for slices and maps is one of the trickiest parts of Go for beginners. This exercise asks you to predict output before running code — the mental exercise of tracing through the call stack is more valuable than just writing code.

### Task
For each of the following three code snippets, predict the output **without running them**. Write down your prediction, then verify by running the code. For any snippet where your prediction was wrong, write a one-sentence explanation of why.

**Snippet A:**
```go
func setFirst(s []int, val int) {
    s[0] = val
}

nums := []int{10, 20, 30}
setFirst(nums, 99)
fmt.Println(nums)
```

**Snippet B:**
```go
func replaceSlice(s []int) {
    s = []int{1, 2, 3}
}

nums := []int{10, 20, 30}
replaceSlice(nums)
fmt.Println(nums)
```

**Snippet C:**
```go
func addKey(m map[string]int) {
    m["new"] = 42
}

scores := map[string]int{"alice": 90}
addKey(scores)
fmt.Println(len(scores))
```

### Requirements
- [ ] Predict the output of all three snippets before running them
- [ ] Run all three to verify
- [ ] For any wrong predictions, write an explanation

### Hints
<details>
<summary>Hint 1 (conceptual hint)</summary>

Remember: call-by-value copies the argument. For slices, the copy shares the backing array with the original — so `s[0] = val` modifies the shared array and the caller sees the change. But `s = []int{1, 2, 3}` replaces the local copy's pointer and length — the caller's slice header is unchanged.

For maps, the "value" being copied is a pointer to the hash table. Both the caller and the function point to the same table, so insertions in the function are visible to the caller.

</details>

### Expected Output / Acceptance Criteria

Snippet A: `[99 20 30]` — mutating through the shared backing array
Snippet B: `[10 20 30]` — replacing the local slice header does not affect the caller
Snippet C: `2` — the map has 2 entries after the function adds one

### Solution
<details>
<summary>Show Solution</summary>

**Snippet A output:** `[99 20 30]`
**Snippet B output:** `[10 20 30]`
**Snippet C output:** `2`

**Explanation:**

Snippet A: `s[0] = val` assigns through the shared backing array. The slice value passed to `setFirst` is a three-word struct (pointer, length, capacity). The pointer still points to the same backing array as `nums`. Modifying `s[0]` modifies the first element of that shared array, which the caller sees.

Snippet B: `s = []int{1, 2, 3}` replaces `s` — the local copy of the slice header — with a new slice header pointing to a brand-new backing array. The caller's `nums` variable still holds its original slice header (pointing to the original array with values `[10, 20, 30]`). The reassignment affects only the local copy.

Snippet C: The map variable `m` received by `addKey` is a copy of the map header — but the map header is essentially a pointer to the hash table. Both `scores` in `main` and `m` in `addKey` point to the same hash table. When `addKey` inserts `"new"`, it modifies that shared table. The caller sees `len(scores) == 2`.

**The rule to remember:** Mutations through a shared pointer (element assignment in a slice, insertion in a map) are visible to the caller. Replacing the pointer itself (reassigning a slice to a new slice, reassigning a map variable) is not visible to the caller.

</details>

---

## Exercise 3: Variadic Sum and Statistics [🟢 Easy] [1 pt]

### Context
Variadic functions are common in Go — `fmt.Println`, `fmt.Printf`, `append`, and many utility functions use them. This exercise builds the basic mechanics: writing a variadic function, using the parameter as a slice inside the function, and using the `...` spread operator at the call site.

### Task
Write two Go functions:
1. `sum(nums ...int) int` — returns the sum of all arguments; returns 0 for no arguments
2. `mean(nums ...int) float64` — returns the arithmetic mean of all arguments; returns 0.0 for no arguments

Call each function:
- With no arguments
- With individual arguments: `sum(1, 2, 3, 4, 5)`
- With a spread slice: `slice := []int{10, 20, 30}; sum(slice...)`

### Requirements
- [ ] Both functions use variadic parameters (`...int`)
- [ ] The `...` spread operator is used at least once at a call site
- [ ] Both functions handle the empty case (no arguments) without panicking
- [ ] `mean` returns `float64` with correct decimal precision (not integer division)

### Hints
<details>
<summary>Hint 1</summary>

Inside a variadic function, the parameter behaves as a slice. Check `len(nums) == 0` to handle the empty case. For `mean`, convert to `float64` before dividing: `float64(sum) / float64(len(nums))`.

</details>

<details>
<summary>Hint 2</summary>

To spread a slice into a variadic call: `sum(slice...)`. The type of `slice` must match the variadic parameter type (`[]int` for `...int`).

</details>

### Expected Output / Acceptance Criteria
```
sum()          = 0
sum(1,2,3,4,5) = 15
sum(slice...)  = 60
mean()         = 0.00
mean(1,2,3)    = 2.00
mean(10,20,30) = 20.00
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// sum returns the sum of all its arguments, or 0 if called with no arguments.
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

// mean returns the arithmetic mean of its arguments, or 0.0 if called with none.
func mean(nums ...int) float64 {
    if len(nums) == 0 {
        return 0.0
    }
    return float64(sum(nums...)) / float64(len(nums))
}

func main() {
    slice := []int{10, 20, 30}

    fmt.Printf("sum()          = %d\n", sum())
    fmt.Printf("sum(1,2,3,4,5) = %d\n", sum(1, 2, 3, 4, 5))
    fmt.Printf("sum(slice...)  = %d\n", sum(slice...))

    fmt.Printf("mean()         = %.2f\n", mean())
    fmt.Printf("mean(1,2,3)    = %.2f\n", mean(1, 2, 3))
    fmt.Printf("mean(10,20,30) = %.2f\n", mean(10, 20, 30))
}
```

**Explanation:**
`sum` iterates over the variadic `nums` slice using `range` — identical to iterating over a regular slice. `mean` reuses `sum` by spreading `nums...` into the call: `sum(nums...)` forwards the variadic arguments to another variadic function. Without the `...`, `sum(nums)` would be a type error (you'd be passing a single `[]int` argument to a function expecting `...int`). The `float64()` conversion in `mean` is essential: without it, `6 / 3` would be integer division (result `2`, correct here) but `7 / 3` would be `2` (wrong), losing the decimal part.

</details>

---

## Exercise 4: Higher-Order Filter and Map [🟡 Medium] [2 pts]

### Context
Higher-order functions are one of Go's most powerful compositional tools. The standard library's `sort.Slice`, `http.HandleFunc`, and testing APIs all rely on them. This exercise builds the pattern from scratch: writing generic (for `[]int`) filter and map functions, then composing them.

### Task
Write three functions:
1. `filter(nums []int, predicate func(int) bool) []int` — returns elements for which `predicate` returns true
2. `transform(nums []int, f func(int) int) []int` — returns a new slice with `f` applied to each element
3. In `main`, use these functions with inline anonymous functions to: (a) filter a list of integers to keep only those divisible by 3, then (b) double each remaining element, and print the result.

Starting list: `[]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}`

### Requirements
- [ ] `filter` and `transform` have the exact signatures above
- [ ] Inline anonymous functions are used as arguments (not named functions)
- [ ] The two operations are chained: transform is called on the output of filter
- [ ] The final result is printed

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
func filter(nums []int, predicate func(int) bool) []int {
    var result []int
    for _, n := range nums {
        if predicate(n) {
            result = append(result, n)
        }
    }
    return result
}
```

`transform` follows the same pattern: iterate, apply `f`, collect into result.

</details>

<details>
<summary>Hint 2 (chaining hint)</summary>

To chain the two operations: `transform(filter(nums, ...), ...)`. The inner call runs first and produces the filtered slice, which is then passed directly to `transform`.

</details>

### Expected Output / Acceptance Criteria
```
Filtered (div by 3): [3 6 9 12]
Doubled:             [6 12 18 24]
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// filter returns elements of nums for which predicate returns true.
func filter(nums []int, predicate func(int) bool) []int {
    var result []int
    for _, n := range nums {
        if predicate(n) {
            result = append(result, n)
        }
    }
    return result
}

// transform returns a new slice with f applied to each element.
func transform(nums []int, f func(int) int) []int {
    result := make([]int, len(nums))
    for i, n := range nums {
        result[i] = f(n)
    }
    return result
}

func main() {
    nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    divisibleBy3 := filter(nums, func(n int) bool {
        return n%3 == 0
    })
    fmt.Println("Filtered (div by 3):", divisibleBy3)

    doubled := transform(divisibleBy3, func(n int) int {
        return n * 2
    })
    fmt.Println("Doubled:            ", doubled)
}
```

**Explanation:**
`filter` uses `append` to build the result, starting from a nil slice. `transform` preallocates with `make([]int, len(nums))` since we know the output size will equal the input size — this is more efficient than appending. The anonymous functions passed as arguments are closures (though these particular ones don't capture any outer variables). Chaining `transform(filter(...), ...)` composes the operations without intermediate named variables, which is clean for simple pipelines. For longer chains, assigning each step to a named variable improves readability.

**Common wrong answers:**
- Using `len(result)` instead of `i` in `transform` — because the result slice is preallocated with `make`, `len(result)` equals `len(nums)` from the start; you need the index `i` from the range, not the length
- Modifying `nums` in-place in `transform` — this mutates the original slice, which breaks the pure-function contract (callers expect their input to be unchanged)

</details>

---

## Exercise 5: Closure Counter with Reset [🟡 Medium] [2 pts]

### Context
Closures with captured mutable state are one of Go's most versatile patterns. They allow you to create stateful objects without defining a struct or a method. This exercise builds a counter factory that returns two closures — increment and reset — that share the same captured state.

### Task
Write a function `newCounter() (increment func(), reset func(), value func() int)` that returns three closures sharing the same internal count:
- `increment()` — increases the count by 1
- `reset()` — sets the count back to 0
- `value()` — returns the current count without modifying it

In `main`, create two independent counters and demonstrate that they are independent.

### Requirements
- [ ] All three returned functions close over the same `count` variable
- [ ] `increment`, `reset`, and `value` have the signatures shown (no parameters)
- [ ] Two counters created by separate calls to `newCounter` are independent
- [ ] Demonstrate independence by incrementing one counter while leaving the other at its current value

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
func newCounter() (func(), func(), func() int) {
    count := 0
    increment := func() { count++ }
    reset := func() { count = 0 }
    value := func() int { return count }
    return increment, reset, value
}
```

Three closures, all referencing the same `count` variable declared in `newCounter`'s scope.

</details>

### Expected Output / Acceptance Criteria
```
Counter A: 0
Counter A: 3
Counter B (independent): 2
Counter A after reset: 0
Counter B still: 2
```
(Exact values may vary based on your increment/reset sequence, but independence must be demonstrated.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// newCounter returns three functions (increment, reset, value) that share
// the same internal count variable via closure capture.
func newCounter() (func(), func(), func() int) {
    count := 0

    increment := func() { count++ }

    reset := func() { count = 0 }

    value := func() int { return count }

    return increment, reset, value
}

func main() {
    // Create counter A
    incA, resetA, valueA := newCounter()

    fmt.Printf("Counter A: %d\n", valueA()) // 0

    incA()
    incA()
    incA()
    fmt.Printf("Counter A: %d\n", valueA()) // 3

    // Create counter B — independent of A
    incB, _, valueB := newCounter()
    incB()
    incB()
    fmt.Printf("Counter B (independent): %d\n", valueB()) // 2

    // Resetting A does not affect B
    resetA()
    fmt.Printf("Counter A after reset: %d\n", valueA()) // 0
    fmt.Printf("Counter B still: %d\n", valueB())       // 2
}
```

**Explanation:**
Each call to `newCounter` creates a new stack frame with a fresh `count` variable. All three returned closures capture `count` **by reference** — they share a reference to the same variable in the same frame's memory (which Go keeps alive via heap escape as long as any closure referencing it lives). Counter A's closures and counter B's closures reference different `count` variables because they came from different `newCounter` calls.

**Why this is useful:** This pattern — a factory function returning closures that share state — is Go's way of implementing the simplest form of an object without needing a struct. The closures are the "methods" and the captured variable is the "field". For more complex objects (multiple fields, more methods), use a struct with methods instead.

</details>

---

## Exercise 6: The Loop-Variable Capture Pitfall [🟡 Medium] [2 pts]

### Context
The loop-variable capture bug is one of the most common sources of subtle bugs in Go, especially in concurrent code. Before Go 1.22, all iterations of a `for` loop shared one loop variable. This exercise demonstrates the bug, then asks you to fix it using the pre-1.22 technique (shadowing), which is important to recognize in existing codebases.

### Task
Part A: Write the following code **exactly** and predict what it prints when run with `go 1.21` semantics (or without a go.mod, which defaults to old behavior):

```go
funcs := make([]func(), 4)
for i := 0; i < 4; i++ {
    funcs[i] = func() { fmt.Println(i) }
}
for _, f := range funcs {
    f()
}
```

Part B: Fix the code using the **variable shadowing** technique (introduce `i := i` inside the loop body) so it prints 0, 1, 2, 3.

Part C: Show the same fix using an **immediately invoked function** (IIFE) that takes `i` as a parameter.

### Requirements
- [ ] Part A: Explain (in a comment or print statement) what the buggy version prints and why
- [ ] Part B: Correct output using variable shadowing
- [ ] Part C: Correct output using IIFE
- [ ] Both B and C print `0\n1\n2\n3\n`

### Hints
<details>
<summary>Hint 1 (pre-1.22 behavior)</summary>

In Go < 1.22, the `for i := 0; i < 4; i++` loop creates one `i` variable that is shared across all iterations. All four closures capture a reference to the same variable. By the time any closure runs (after the loop completes), `i` is 4 (the value that caused the loop condition to fail).

</details>

<details>
<summary>Hint 2 (shadowing fix)</summary>

Inside the loop body, before creating the closure, add: `i := i`. This declares a new variable named `i` in the current block scope, initialized to the current loop iteration's value. The closure captures this block-scoped `i`, not the loop variable.

</details>

<details>
<summary>Hint 3 (IIFE fix)</summary>

Wrap the closure creation in an immediately invoked function that takes `i` as a parameter:
```go
funcs[i] = func(i int) func() {
    return func() { fmt.Println(i) }
}(i)
```
The outer `i` (the parameter) is a new variable that receives a copy of the loop `i` at call time.

</details>

### Expected Output / Acceptance Criteria
Part A output (pre-1.22): `4\n4\n4\n4\n` (or the loop's post-condition value, which is 4)
Parts B and C output: `0\n1\n2\n3\n`

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    // Part A: The bug (pre-Go 1.22 behavior)
    // All closures capture the same 'i' variable. When they run,
    // i == 4 (the value that terminated the loop).
    fmt.Println("Part A (buggy):")
    funcs := make([]func(), 4)
    for i := 0; i < 4; i++ {
        funcs[i] = func() { fmt.Println(i) } // captures the loop variable i
    }
    for _, f := range funcs {
        f() // In Go < 1.22: prints 4, 4, 4, 4
            // In Go 1.22+: prints 0, 1, 2, 3 (each iter gets its own i)
    }

    // Part B: Fix via variable shadowing
    fmt.Println("\nPart B (shadow fix):")
    funcsB := make([]func(), 4)
    for i := 0; i < 4; i++ {
        i := i // shadow: new per-iteration variable, initialized to current i
        funcsB[i] = func() { fmt.Println(i) }
    }
    for _, f := range funcsB {
        f() // prints 0, 1, 2, 3
    }

    // Part C: Fix via immediately invoked function expression (IIFE)
    fmt.Println("\nPart C (IIFE fix):")
    funcsC := make([]func(), 4)
    for i := 0; i < 4; i++ {
        funcsC[i] = func(captured int) func() {
            return func() { fmt.Println(captured) }
        }(i) // i is passed by value to the IIFE — a new 'captured' variable per call
    }
    for _, f := range funcsC {
        f() // prints 0, 1, 2, 3
    }
}
```

**Explanation:**
The shadowing fix (`i := i`) creates a new variable in the current block that masks the outer loop variable for the remainder of the block. The closure captures the new block-scoped variable, which has a fixed value for that iteration.

The IIFE fix uses function call semantics: `i` is passed as an argument `captured` to the immediately-invoked outer function. Because function arguments are passed by value, `captured` receives a copy of `i` at call time. The inner closure closes over `captured`, not the loop's `i`.

**Why Go 1.22 changes this:** In Go 1.22+, the compiler implicitly adds per-iteration variable creation for `for` loops, equivalent to the shadowing fix but automatic. However, code with `go 1.21` (or earlier) in its `go.mod` still exhibits the old behavior — which is why knowing the manual fix remains important.

</details>

---

## Exercise 7: defer + Named Returns for Error Wrapping [🔴 Hard] [3 pts]

### Context
The deferred-closure-modifies-named-return pattern is one of Go's most powerful and subtle idioms. It enables guaranteed error wrapping without repeating `fmt.Errorf("funcName: %w", err)` on every error return path. This exercise builds the pattern step by step.

### Task
Write a function `openAndRead(path string) (content string, err error)` that:
1. Uses named return values `content` and `err`
2. Has a `defer` at the top that wraps any non-nil error with `fmt.Errorf("openAndRead %q: %w", path, err)`
3. Opens the file with `os.Open`, returns immediately on error (the defer will wrap it)
4. Reads the file with `io.ReadAll`, returns immediately on error (the defer will wrap it)
5. Sets `content = string(data)` and returns

Call it with `/etc/hostname` (should succeed on Linux) and with `/nonexistent/file` (should fail), and print both outcomes.

Verify using `errors.Is` that the wrapped error preserves the original `os.PathError` for the failure case.

### Requirements
- [ ] Named return values `content string, err error` in the signature
- [ ] A single `defer func() { if err != nil { ... } }()` at the top of the function body
- [ ] The deferred closure wraps err using `fmt.Errorf("openAndRead %q: %w", path, err)`
- [ ] The function body does NOT manually wrap errors — just `return` on error
- [ ] `errors.Is(wrappedErr, fs.ErrNotExist)` returns true for the missing file case (demonstrating unwrapping)

### Hints
<details>
<summary>Hint 1 (structure)</summary>

```go
func openAndRead(path string) (content string, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("openAndRead %q: %w", path, err)
        }
    }()
    // ... rest of the function
}
```

The `defer` captures `err` by reference. Whenever the function body sets `err` and returns, the deferred closure runs and wraps it.

</details>

<details>
<summary>Hint 2 (errors package)</summary>

To check if an error is "file not found": `errors.Is(err, fs.ErrNotExist)`. Import `"io/fs"`. The `%w` verb in `fmt.Errorf` preserves the error chain, so `errors.Is` can unwrap through multiple layers to find `fs.ErrNotExist`.

</details>

<details>
<summary>Hint 3 (imports)</summary>

You need: `"errors"`, `"fmt"`, `"io"`, `"io/fs"`, `"os"`

</details>

### Expected Output / Acceptance Criteria
```
/etc/hostname: <hostname content>  (varies by system)
/nonexistent/file: error: openAndRead "/nonexistent/file": open /nonexistent/file: no such file or directory
Is ErrNotExist? true
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "errors"
    "fmt"
    "io"
    "io/fs"
    "os"
)

// openAndRead reads the entire content of a file as a string.
// Any error is wrapped with the function name and path for context.
func openAndRead(path string) (content string, err error) {
    // Deferred closure captures 'err' by reference.
    // It runs just before openAndRead returns, after the function body sets err.
    defer func() {
        if err != nil {
            err = fmt.Errorf("openAndRead %q: %w", path, err)
        }
    }()

    f, err := os.Open(path)
    if err != nil {
        return // naked return; deferred closure will wrap err
    }
    defer f.Close()

    data, err := io.ReadAll(f)
    if err != nil {
        return // naked return; deferred closure will wrap err
    }

    content = string(data)
    return // success: err is nil, deferred closure does nothing
}

func main() {
    // Success case
    if content, err := openAndRead("/etc/hostname"); err != nil {
        fmt.Println("unexpected error:", err)
    } else {
        fmt.Printf("/etc/hostname: %q\n", content)
    }

    // Failure case
    _, err := openAndRead("/nonexistent/file")
    if err != nil {
        fmt.Printf("/nonexistent/file: error: %v\n", err)
        fmt.Printf("Is ErrNotExist? %v\n", errors.Is(err, fs.ErrNotExist))
    }
}
```

**Step-by-step explanation:**

1. `defer func() { ... }()` is registered at function entry. It captures a reference to `err`.
2. `os.Open` fails for `/nonexistent/file`; `err` is set to a non-nil `*os.PathError`. The naked `return` exits the function body.
3. The deferred closure runs. It sees `err != nil` and replaces `err` with `fmt.Errorf("openAndRead %q: %w", path, err)` — a new error that wraps the original.
4. The caller receives the wrapped error. `errors.Is(err, fs.ErrNotExist)` returns true because `%w` preserves the error chain, and `*os.PathError` implements `Unwrap()` to expose `fs.ErrNotExist`.

**Why naked returns here:** The naked returns in this function are acceptable — the function is short (fits on screen), and the named returns `content` and `err` document what each return value means. The deferred closure is the reason we used named returns at all.

</details>

---

## Exercise 8: Recursive Tree Traversal [🔴 Hard] [3 pts]

### Context
Recursion is natural for tree-shaped data structures. This exercise builds a simple binary tree and uses mutual recursion (depth calculation calls a helper) alongside a recursive traversal that collects values in order.

### Task
Define a binary tree node type:
```go
type TreeNode struct {
    Value int
    Left  *TreeNode
    Right *TreeNode
}
```

Write two recursive functions:
1. `insert(root *TreeNode, val int) *TreeNode` — inserts `val` into a binary search tree (BST), returning the root. If `root` is nil, return a new node. If `val < root.Value`, recurse left; if `val > root.Value`, recurse right; if equal, don't insert.
2. `inorder(root *TreeNode) []int` — returns the values of the tree in ascending order (in-order traversal: left, root, right).

Build a BST by inserting `5, 3, 7, 1, 4, 6, 8` and print the in-order result.

### Requirements
- [ ] `insert` is recursive and returns the (possibly new) root
- [ ] `inorder` is recursive and returns a `[]int` in sorted order
- [ ] The in-order output of inserting `5, 3, 7, 1, 4, 6, 8` is `[1 3 4 5 6 7 8]`
- [ ] Both functions handle `nil` root correctly (no nil pointer dereference)

### Hints
<details>
<summary>Hint 1 (insert pattern)</summary>

```go
func insert(root *TreeNode, val int) *TreeNode {
    if root == nil {
        return &TreeNode{Value: val}
    }
    if val < root.Value {
        root.Left = insert(root.Left, val)
    } else if val > root.Value {
        root.Right = insert(root.Right, val)
    }
    return root
}
```

</details>

<details>
<summary>Hint 2 (inorder pattern)</summary>

In-order traversal: left subtree, then current node, then right subtree. Use `append` to combine the results:
```go
result = append(result, inorder(root.Left)...)
result = append(result, root.Value)
result = append(result, inorder(root.Right)...)
```

</details>

### Expected Output / Acceptance Criteria
```
In-order traversal: [1 3 4 5 6 7 8]
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// TreeNode is a node in a binary search tree.
type TreeNode struct {
    Value int
    Left  *TreeNode
    Right *TreeNode
}

// insert adds val to the BST rooted at root and returns the (possibly new) root.
// Duplicate values are ignored.
func insert(root *TreeNode, val int) *TreeNode {
    if root == nil {
        return &TreeNode{Value: val}
    }
    switch {
    case val < root.Value:
        root.Left = insert(root.Left, val)   // recurse into left subtree
    case val > root.Value:
        root.Right = insert(root.Right, val) // recurse into right subtree
    // equal: do nothing — no duplicates
    }
    return root
}

// inorder returns the values of the BST in ascending order.
func inorder(root *TreeNode) []int {
    if root == nil {
        return nil
    }
    var result []int
    result = append(result, inorder(root.Left)...)  // left subtree
    result = append(result, root.Value)              // current node
    result = append(result, inorder(root.Right)...)  // right subtree
    return result
}

func main() {
    values := []int{5, 3, 7, 1, 4, 6, 8}

    var root *TreeNode
    for _, v := range values {
        root = insert(root, v)
    }

    fmt.Println("In-order traversal:", inorder(root))
}
```

**Step-by-step explanation:**

1. `insert` handles `nil` by creating and returning a new node. For non-nil nodes, it compares `val` with `root.Value` to decide which subtree to descend into, then reassigns the child pointer to the result of the recursive call (which may be a new node or the unchanged existing subtree).
2. `inorder` has the standard in-order pattern: recurse left, emit current, recurse right. The `nil` base case returns `nil` (a nil slice), which is safe to append to and spread (`nil...`).
3. The spread operator `...` is used to append slices: `append(result, inorder(root.Left)...)` appends all elements of the left subtree's result into `result`.

**Why returning the root matters:** `insert` returns the (possibly new) root and the caller reassigns: `root = insert(root, v)`. If we passed `*TreeNode` and modified it in-place, inserting into an empty tree (nil root) would fail because you can't assign to a nil pointer. The "return the new root" pattern is idiomatic Go for tree operations.

</details>

---

## Exercise 9: Middleware Chain [⭐ Expert] [5 pts]

### Context
Middleware chains are a foundational pattern in Go web servers and many other systems. A middleware wraps a handler: it does some work before calling the next handler, and optionally some work after. Chaining middlewares composes them into a pipeline. This exercise builds a simplified (non-HTTP) version of this pattern using function types.

### Task
Define a `Handler` type as `func(input string) string`. Write a `Middleware` type as `func(Handler) Handler`.

Implement three middlewares:
1. `logger(name string) Middleware` — logs the function name, input, and output to stdout before returning the result
2. `trimSpace() Middleware` — trims leading/trailing whitespace from the input before passing it to the next handler
3. `addPrefix(prefix string) Middleware` — prepends `prefix` to the output of the next handler

Write a `chain(middlewares ...Middleware) Middleware` function that composes middlewares right-to-left (the first middleware in the list is the outermost — applied last to the handler, called first when the chain runs).

Write a simple base handler `func(s string) string { return "hello, " + s }`.

Apply all three middlewares to the base handler using `chain`, call the result with `"  world  "`, and show the output.

### Requirements
- [ ] `Handler` and `Middleware` types are defined as specified
- [ ] All three middleware factories work correctly
- [ ] `chain` composes any number of middlewares
- [ ] The final call with `"  world  "` trims spaces, logs, prepends prefix, and produces a sensible output
- [ ] Explain in a comment what order the middlewares apply

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
type Handler func(input string) string
type Middleware func(Handler) Handler
```

A middleware takes a handler and returns a new handler that wraps it:
```go
func logger(name string) Middleware {
    return func(next Handler) Handler {
        return func(input string) string {
            result := next(input)
            fmt.Printf("[%s] input=%q output=%q\n", name, input, result)
            return result
        }
    }
}
```

</details>

<details>
<summary>Hint 2 (chain composition)</summary>

`chain` should apply middlewares in reverse order so the first middleware in the list is outermost:
```go
func chain(mws ...Middleware) Middleware {
    return func(next Handler) Handler {
        // Apply in reverse so mws[0] is the outermost
        for i := len(mws) - 1; i >= 0; i-- {
            next = mws[i](next)
        }
        return next
    }
}
```

</details>

<details>
<summary>Hint 3 (application)</summary>

To apply the chained middleware to a base handler:
```go
base := func(s string) string { return "hello, " + s }
wrapped := chain(logger("main"), trimSpace(), addPrefix("[RESULT] "))(base)
result := wrapped("  world  ")
```

</details>

### Expected Output / Acceptance Criteria
```
[main] input="world" output="hello, world"
[RESULT] hello, world
```
(Exact format depends on your logger and prefix middleware implementations.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "strings"
)

// Handler processes a string input and returns a string output.
type Handler func(input string) string

// Middleware wraps a Handler, returning a new Handler.
type Middleware func(Handler) Handler

// logger is a middleware factory that logs the handler's name, input, and output.
func logger(name string) Middleware {
    return func(next Handler) Handler {
        return func(input string) string {
            result := next(input)
            fmt.Printf("[%s] input=%q output=%q\n", name, input, result)
            return result
        }
    }
}

// trimSpace is a middleware that trims whitespace from the input.
func trimSpace() Middleware {
    return func(next Handler) Handler {
        return func(input string) string {
            return next(strings.TrimSpace(input))
        }
    }
}

// addPrefix is a middleware factory that prepends prefix to the handler's output.
func addPrefix(prefix string) Middleware {
    return func(next Handler) Handler {
        return func(input string) string {
            return prefix + next(input)
        }
    }
}

// chain composes middlewares: the first middleware listed is the outermost
// (runs first when the chain is called, wraps the rest).
func chain(mws ...Middleware) Middleware {
    return func(next Handler) Handler {
        // Apply in reverse so mws[0] wraps everything else
        for i := len(mws) - 1; i >= 0; i-- {
            next = mws[i](next)
        }
        return next
    }
}

func main() {
    // Base handler: greets its input
    base := Handler(func(s string) string {
        return "hello, " + s
    })

    // Chain: logger is outermost (runs first), then trimSpace, then addPrefix.
    // Execution order when called:
    //   1. logger receives "  world  ", calls next (trimSpace) with "  world  "
    //   2. trimSpace trims to "world", calls next (addPrefix) with "world"
    //   3. addPrefix calls base with "world", gets "hello, world"
    //   4. addPrefix prepends "[RESULT] ", returns "[RESULT] hello, world"
    //   5. trimSpace returns "[RESULT] hello, world" to logger
    //   6. logger prints its log line, returns "[RESULT] hello, world"
    wrapped := chain(
        logger("main"),
        trimSpace(),
        addPrefix("[RESULT] "),
    )(base)

    result := wrapped("  world  ")
    fmt.Println(result)
}
```

**Step-by-step explanation:**

1. `Middleware` is a function type that transforms a `Handler` into a new `Handler`. This is the standard middleware signature pattern.
2. `logger`, `trimSpace`, and `addPrefix` are middleware factories — they return `Middleware` values (closures). Each closure closes over its configuration (`name`, `prefix`).
3. `chain` iterates over middlewares in reverse, applying each one by calling `mws[i](next)`. This builds up a nested chain: `mws[0](mws[1](mws[2](base)))`. The outermost wrapper is `mws[0]`, so it runs first when the chain is called.
4. The final `(base)` call at the end of `chain(...)(base)` applies the composed middleware to the base handler, returning the fully wrapped `Handler`.

**Why this pattern matters:** This is essentially how `net/http` middleware works in production Go web servers (libraries like gorilla/mux and chi use exactly this pattern). Every middleware adds cross-cutting concerns (logging, authentication, rate-limiting) without modifying the core handler logic.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Basic Function Declaration | — | —/1 | — | — |
| Exercise 2 — Call-by-Value Prediction | — | —/1 | — | — |
| Exercise 3 — Variadic Sum and Statistics | — | —/1 | — | — |
| Exercise 4 — Higher-Order Filter and Map | — | —/2 | — | — |
| Exercise 5 — Closure Counter with Reset | — | —/2 | — | — |
| Exercise 6 — Loop-Variable Capture Pitfall | — | —/2 | — | — |
| Exercise 7 — defer + Named Returns | — | —/3 | — | — |
| Exercise 8 — Recursive Tree Traversal | — | —/3 | — | — |
| Exercise 9 — Middleware Chain | — | —/5 | — | — |
| **Total** | | **—/20** | | |

**Passing threshold:** 13/20 (65%). Aim for 17/20 (85%) before taking the test.
