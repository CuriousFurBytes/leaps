# Answer Key — Module 2: Control Flow

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

### 1.1 — Parentheses in if condition [1 pt]

**Full credit answer:**
No, Go does **not** require parentheses around the condition in an `if` statement. Writing `if (x > 0) { ... }` is technically valid Go but the parentheses are redundant. The `gofmt` tool will remove them automatically, and idiomatic Go omits them. Braces `{ }` around the body, however, are **required** — unlike C, Go does not allow a single-statement body without braces.

**Key points required:**
- Parentheses are NOT required (and idiomatically omitted)
- Braces ARE required (this is the harder-to-remember rule)

**Common wrong answers:**
- *"Yes, parentheses are required"* — This confuses Go with C/Java where parentheses are mandatory. In Go they are optional and conventionally omitted.
- *"Parentheses are optional and braces are also optional"* — Braces are never optional in Go's if/for/switch statements.

---

### 1.2 — How many loop constructs [1 pt]

**Full credit answer:**
Go has **exactly one** loop construct: `for`. There is no `while` keyword, no `do-while` keyword, and no `foreach` keyword. The single `for` keyword supports four forms: (1) the classic `for init; condition; post` form, (2) the while-style `for condition` form, (3) the infinite `for` form with no condition, and (4) the range-based `for i, v := range collection` form.

**Key points required:**
- One loop keyword: `for`
- No `while`, no `do-while`

**Common wrong answers:**
- *"Go has for and range"* — `range` is not a loop keyword; it is an operator used inside a `for` statement. The loop keyword is still `for`.

---

### 1.3 — Switch fallthrough [1 pt]

**Full credit answer:**
No, Go's `switch` does **not** fall through between cases by default. Each case executes independently and terminates automatically. To get explicit fall-through behavior, you use the `fallthrough` keyword at the end of a case. Note that `fallthrough` in Go is unconditional — it transfers control to the next case's body regardless of whether that case's condition would have matched.

**Key points required:**
- No automatic fallthrough (opposite of C/Java)
- `fallthrough` keyword for explicit fallthrough
- Bonus: `fallthrough` is unconditional

---

### 1.4 — When does defer execute [1 pt]

**Full credit answer:**
A deferred function call executes when the **surrounding function returns** — not when the `defer` statement is reached. More precisely: the deferred function is pushed onto a stack when the `defer` statement executes, and all functions on that stack are called (in LIFO order) when the surrounding function returns, whether that return is explicit (`return`), falls off the end of the function, or is triggered by a `panic`.

**Key points required:**
- Runs when the surrounding function returns (not at the defer statement)
- LIFO order if there are multiple defers

**Common wrong answers:**
- *"At the end of the block"* — Defer is scoped to the function, not to the block. `defer` inside an `if` block or `for` loop runs when the enclosing function returns, not when the block ends.
- *"Immediately when the defer statement runs"* — That is when the arguments are evaluated, but the deferred call itself is saved for later.

---

### 1.5 — continue vs break [1 pt]

**Full credit answer:**
`continue` skips the rest of the current loop iteration's body and jumps to the next iteration (re-evaluating the condition in a `for condition` loop, or running the post statement in a classic `for` loop). `break` exits the innermost loop entirely — no more iterations run. In a range loop, `continue` skips to the next element; `break` stops iterating altogether.

**Key points required:**
- `continue` skips to next iteration; `break` exits the loop
- Both apply to the innermost enclosing loop (unless a label is used)

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — The init statement in if [2 pts]

**Full credit answer:**
The init statement is an optional statement that runs before the condition of an `if` expression is evaluated, separated from the condition by a semicolon: `if init; condition { ... }`. The most common form declares a new variable: `if v, err := someFunc(); err == nil { ... }`. The variable declared in the init statement is **scoped to the entire `if`/`else if`/`else` block** — it is visible in the condition, in the `if` body, and in all `else` branches, but it goes out of scope after the closing `}`.

This is useful because it keeps variables that are only needed for a conditional check tightly scoped — they don't pollute the surrounding function's scope. It is especially valuable with Go's `(value, error)` return convention: you can declare both `v` and `err` in the init statement, use `err` in the condition, use `v` in the success branch, and use `err` in the else branch, without either variable being accessible after the if/else block ends.

**Rubric:**
- 2 pts: Correctly explains the syntax AND the scope (scoped to the entire if/else block, not the surrounding function) AND gives a concrete example
- 1 pt: Correct general idea but unclear on scope, or no example
- 0 pts: Confuses the init statement with a regular variable declaration before the if

**Teaching note:**
The most common confusion here is thinking that the init variable is only scoped to the `if` body. It is scoped to the entire `if`/`else if`/`else` chain. If a student got this wrong, direct them to re-read the "if / else" section of the module README, specifically the scope note.

---

### 2.2 — Simulating while and do-while [2 pts]

**Full credit answer:**

**Simulating while:** Use `for condition { ... }` — the `for` keyword with only a condition and no init or post statement. This is syntactically and semantically identical to `while (condition) { ... }` in other languages.

```go
n := 1
for n < 1000 {
    n *= 2
}
```

**Simulating do-while:** Use `for { ...; if !condition { break } }` or equivalently, put the condition check at the end of the loop body:

```go
for {
    doWork()
    if done() {
        break
    }
}
```

This executes the body at least once, then checks the condition, exactly like `do { ... } while (condition)`.

**Why the consolidation is intentional:** The Go designers, particularly Rob Pike, explicitly chose minimalism in the language's surface area. Having three loop keywords (`while`, `do`, `for`) adds cognitive overhead — you must remember which keyword does what. All three patterns are expressible with `for`, so having one keyword is strictly sufficient. This also reduces the temptation to debate which loop form is "correct" for a given situation — there is only one loop.

**Rubric:**
- 2 pts: Correctly demonstrates both patterns with code AND gives a reasonable justification for the design choice
- 1 pt: Correctly demonstrates one of the two patterns, or demonstrates both but without any design rationale
- 0 pts: Cannot correctly demonstrate either pattern using only `for`

---

### 2.3 — LIFO order of defer [2 pts]

**Full credit answer:**
When multiple `defer` statements execute in a function, the deferred calls run in LIFO (last-in, first-out) order — the most recently deferred call runs first. This ordering is not arbitrary; it mirrors the natural order of resource cleanup.

Consider acquiring three resources in sequence:
```go
mu.Lock()
defer mu.Unlock()          // deferred 1st — runs last

f, _ := os.Open("data.txt")
defer f.Close()            // deferred 2nd — runs 2nd

conn, _ := net.Dial("tcp", addr)
defer conn.Close()         // deferred 3rd — runs 1st
```

When the function returns, the order is: close `conn` first, then close `f`, then unlock `mu`. This is the correct teardown order — the most recently acquired resource is released first, matching the reverse of acquisition order. If the order were FIFO (first-in, first-out), you would release resources in the same order you acquired them, which could cause problems if later resources depend on earlier ones still being open.

**Rubric:**
- 2 pts: Correctly describes LIFO order AND gives a concrete scenario that illustrates why it is useful (not just that it exists)
- 1 pt: Correctly describes LIFO order but without any explanation of why it is useful
- 0 pts: Describes the order incorrectly (says FIFO, or says it's non-deterministic)

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Range over map with average [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

func main() {
    scores := map[string]int{"Alice": 90, "Bob": 85, "Carol": 92}

    total := 0
    for name, score := range scores {
        fmt.Printf("%s: %d\n", name, score)
        total += score
    }

    avg := float64(total) / float64(len(scores))
    fmt.Printf("Average: %.2f\n", avg)
}
```

**Step-by-step reasoning:**
1. Declare the map and initialize it with the given values
2. Use `for name, score := range scores` to iterate — map iteration order is non-deterministic, so any order is correct
3. Accumulate the total in a separate variable; compute the average outside the loop
4. Use `float64()` conversion for accurate division (integer division would truncate)

**Rubric:**
- 3 pts: Correct solution; uses `range` for iteration; computes average correctly using float conversion; compiles and runs correctly
- 2 pts: Correct range iteration and printing; average computation has a minor error (e.g., integer division without float conversion, giving a truncated result)
- 1 pt: Correct range iteration but missing the average computation entirely, or major error in map iteration
- 0 pts: Does not use `range`, or has a fundamental misconception about map iteration

**Acceptable alternatives:**
- Using `len(scores)` vs a separate counter variable — both are correct
- Printing with `fmt.Println` instead of `fmt.Printf` — acceptable if the output is still correct
- Storing the average as `int` if the result is a whole number — acceptable, though `float64` is better practice

---

### 3.2 — classify function with switch [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

func classify(n int) string {
    switch {
    case n < 0:
        return "negative"
    case n == 0:
        return "zero"
    case n <= 9:
        return "small"
    case n <= 99:
        return "medium"
    default:
        return "large"
    }
}

func main() {
    testValues := []int{-5, 0, 7, 50, 150}
    for _, n := range testValues {
        fmt.Printf("classify(%d) = %q\n", n, classify(n))
    }
}
```

**Expected output:**
```
classify(-5) = "negative"
classify(0) = "zero"
classify(7) = "small"
classify(50) = "medium"
classify(150) = "large"
```

**Rubric:**
- 3 pts: Correct switch-true form; all 5 categories correctly implemented; tested with at least 5 values covering all categories; compiles and runs correctly
- 2 pts: Correct logic for all categories, but uses `if`/`else if` instead of `switch` (doesn't follow the requirement)
- 1 pt: Switch form used but one or more category boundaries are wrong (e.g., `n < 9` instead of `n <= 9`)
- 0 pts: Does not produce correct output for the test cases, or does not attempt a switch

**Acceptable alternatives:**
Using `case n >= 1 && n <= 9:` instead of `case n <= 9:` is correct but more verbose. Since the cases run in order and `n < 0` and `n == 0` are already handled, `case n <= 9:` is sufficient.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Switch fallthrough bug [3 pts] (1 pt each part)

**(a) What actually happens when n = 2:**
When `n = 2`, execution enters `case 2:`, prints `"two"`, and then hits `fallthrough`. The `fallthrough` statement unconditionally transfers execution to the body of the next case (`case 3:`), which prints `"three"`. Execution then stops (no more `fallthrough`). So the output for `n = 2` is:
```
two
three
```

**(b) Why — what fallthrough does:**
In Go, `fallthrough` transfers control to the **body** of the next case unconditionally — it does **not** evaluate the next case's condition. So even though `case 3:` would only match `n == 3`, the `fallthrough` from `case 2:` causes `case 3:`'s body to run for `n = 2`. This is the opposite of C, where fall-through is automatic (you need `break` to prevent it). In Go, `fallthrough` is explicit and unconditional.

**(c) Correct rewrites:**

For the goal "match 1, 2, or 3 and do the same thing" (comma-separated cases):
```go
switch n {
case 1, 2, 3:
    fmt.Println("one, two, or three")
}
```

For the original goal "each number prints its own word" (no fallthrough needed):
```go
switch n {
case 1:
    fmt.Println("one")
case 2:
    fmt.Println("two")
case 3:
    fmt.Println("three")
}
```

**Rubric:**
- 1 pt for (a): Correctly traces that `n=2` prints both "two" and "three" (not just "two")
- 1 pt for (b): Correctly explains that `fallthrough` is unconditional — it does not check the next case's condition
- 1 pt for (c): Provides both a correct comma-separated form AND a correct per-word form (or at least one valid rewrite with a clear explanation)

---

## Section 5: Discussion — Answer Key

### 5.1 — defer inside a for loop [2 pts]

**Example strong answer:**
The statement is true because `defer` is scoped to the enclosing **function**, not to the loop iteration. When a programmer writes `defer f.Close()` inside a loop, they likely intend "close this file when I'm done with it this iteration." What actually happens is all the `defer f.Close()` calls accumulate on a stack and run only when the surrounding function returns. If the loop processes 1000 files, 1000 file handles stay open simultaneously — a resource leak that can exhaust the OS file descriptor limit.

The correct pattern is to extract the loop body into a helper function:
```go
for _, path := range paths {
    processOne(path)  // defer inside here runs at the end of each call
}

func processOne(path string) {
    f, err := os.Open(path)
    if err != nil { return }
    defer f.Close()  // runs when processOne returns — once per file
    // ...
}
```

This works because now `defer f.Close()` is scoped to `processOne`, which returns once per iteration. Alternatively, use an anonymous function invoked immediately: `func() { defer f.Close(); ... }()`.

**Elements that earn full credit:**
- Correctly explains that `defer` runs at function return, not loop iteration end
- Names the consequence (resource leak — file handles / FDs stay open)
- Describes the helper-function pattern (or IIFE) that fixes it
- Distinguishes what the programmer intended from what actually happens

**Rubric:**
- 2 pts: Explains the root cause (function-scoped defer), names the consequence (resource leak), and describes a correct fix
- 1 pt: Identifies that defer-in-a-loop is problematic, but either the explanation of why or the fix is missing/incorrect
- 0 pts: Claims the code is correct, or shows a fundamental misunderstanding of how defer works

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Unicode rune iteration [+5 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    s := "café"

    // 1. Byte length
    fmt.Printf("Byte length (len):   %d\n", len(s))

    // 2. Rune count
    fmt.Printf("Rune count:          %d\n", utf8.RuneCountInString(s))

    // 3. Range iteration — shows rune index and code point
    fmt.Println("\nRange iteration:")
    for i, r := range s {
        fmt.Printf("  byte index %d: %c  (U+%04X)\n", i, r, r)
    }

    // 4. Comparison: byte indexing vs rune indexing for 'é'
    fmt.Println("\nByte indexing s[3] and s[4] (raw bytes of 'é'):")
    fmt.Printf("  s[3] = 0x%X\n", s[3])
    fmt.Printf("  s[4] = 0x%X\n", s[4])
    fmt.Println("  These are the two UTF-8 bytes of 'é' (U+00E9 → 0xC3 0xA9),")
    fmt.Println("  not a valid character on their own.")
}
```

**Expected output:**
```
Byte length (len):   6
Rune count:          4

Range iteration:
  byte index 0: c  (U+0063)
  byte index 1: a  (U+0061)
  byte index 2: f  (U+0066)
  byte index 3: é  (U+00E9)
  byte index 5: !  (U+0021)

Byte indexing s[3] and s[4] (raw bytes of 'é'):
  s[3] = 0xC3
  s[4] = 0xA9
  These are the two UTF-8 bytes of 'é' (U+00E9 → 0xC3 0xA9),
  not a valid character on their own.
```

Note: "café" has 5 characters but 6 bytes — `c`, `a`, `f` are 1 byte each; `é` (U+00E9) is 2 bytes in UTF-8; and if a trailing `!` is not in your string, adjust accordingly. "café" with no exclamation is 4 runes and 5 bytes.

**Rubric:**
- 5 pts: Demonstrates all four items (byte length, rune count, range iteration with code points, byte-indexing comparison) with correct output and a clear explanation
- 3 pts: Demonstrates three of the four items correctly; minor gap in the explanation
- 1 pt: Demonstrates range iteration correctly but misses the byte-vs-rune distinction or the `len()` vs `RuneCountInString()` difference
- 0 pts: Incorrect understanding of how range works on strings

**Bonus teaching note:**
This question tests the intersection of Go's `for` range semantics and Unicode encoding. Students who score full credit here have a solid grasp of UTF-8 encoding — knowing that ASCII characters are 1 byte, Latin Extended characters (like `é`) are 2 bytes, and emoji are 4 bytes. The practical takeaway is: always use `range` (not `s[i]`) when iterating over text that may contain non-ASCII characters.

---

## Common Wrong Answers Across the Test

These are patterns seen frequently when students haven't fully internalized the material:

1. **Confusing defer scope (block vs function)** — Students write "defer runs when the block ends" or "defer runs when the loop ends." Defer is scoped to the surrounding function, not to any block. Students who make this mistake need to re-read the "defer" section and specifically the "defer in a loop" warning.
2. **Missing the fallthrough-is-unconditional detail** — Many students know that `fallthrough` causes fall-through but don't know it skips the next case's condition check. This is the subtlety in Question 4.1 part (b). See the `fallthrough` section of the Go spec for confirmation.
3. **Thinking range over string gives bytes** — Students may write `for i, b := range s` and say `b` is a byte. It is a `rune` (Unicode code point). Byte indexing requires `s[i]`. See Example 2 in the module README.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 likely read without testing their understanding. Recommend re-studying with the Feynman technique (explain it aloud) — specifically explain `defer`'s execution model and the init statement's scope.
- Students who struggle with Section 3 need more exercise practice before moving on. Send back to EXERCISES.md exercises 3 (init statement), 4 (FizzBuzz with switch), and 5 (range iteration).
- The bonus question tests understanding of UTF-8 encoding alongside Go's range semantics — don't be concerned if most students score partially (3/5) rather than fully (5/5).
- A score below 60% generally indicates the prerequisites weren't solid. Ask the student whether they are comfortable with Go's multiple return values (`value, error`) and the `:=` short declaration — both are fundamental to understanding the init statement.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
