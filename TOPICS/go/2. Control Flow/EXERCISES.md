# Exercises — Module 2: Control Flow

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

## Exercise 1: Two Ways to Loop [🟢 Easy] [1 pt]

### Context
Go has only one loop keyword (`for`), but it supports multiple forms. This exercise focuses on the two most fundamental forms: the classic C-style loop and the while-style loop. Confirming you can write both is the first step before learning the more powerful `range` form.

### Task
Write a Go program that prints the numbers 1 through 10, one per line. Do it **twice**: first using the classic `for init; condition; post` loop, then using the while-style `for condition` loop (no init or post). Both loops must produce identical output.

### Requirements
- [ ] The first loop uses `for i := 1; i <= 10; i++` syntax (or equivalent)
- [ ] The second loop uses `for condition` syntax with a separate variable declaration and manual increment
- [ ] Both loops print numbers 1 through 10 inclusive, one per line
- [ ] The program compiles and runs without errors

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

For the while-style loop, declare the variable before the loop: `n := 1`. Then write `for n <= 10 { ... }`. You need to increment `n` manually inside the loop body or you'll have an infinite loop.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The while-style loop body should be: `fmt.Println(n)` followed by `n++`. The `n++` must be inside the loop body — if it's outside the loop, the loop never terminates.

</details>

### Expected Output / Acceptance Criteria
Both loops should print:
```
1
2
3
4
5
6
7
8
9
10
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

func main() {
    // Classic C-style for loop
    fmt.Println("Classic loop:")
    for i := 1; i <= 10; i++ {
        fmt.Println(i)
    }

    // While-style for loop (condition only)
    fmt.Println("While-style loop:")
    n := 1
    for n <= 10 {
        fmt.Println(n)
        n++
    }
}
```

**Explanation:**
The classic form `for i := 1; i <= 10; i++` declares the loop variable, checks the condition before each iteration, and increments after each iteration — all in the loop header. The while-style form moves the variable declaration and increment out of the header, leaving only the condition. Both compile to equivalent machine code; the difference is purely stylistic. Use the classic form when the loop variable has a clear start, end, and step. Use the while-style form when the termination condition is more complex or involves a variable that already exists in the outer scope.

**Common wrong answers and why they fail:**
- `for i := 1; i < 10; i++` — uses `<` instead of `<=`, so it prints 1–9 (misses 10 by one)
- Forgetting `n++` inside the while-style loop body — the loop runs forever because `n` never changes

</details>

---

## Exercise 2: Day of the Week Switch [🟢 Easy] [1 pt]

### Context
`switch` is Go's preferred tool for dispatching on a value when there are three or more cases. This exercise focuses on the basic switch form with a string value, comma-separated cases for grouping, and a `default` case for unmatched inputs.

### Task
Write a Go function `dayName(n int) string` that takes a day number (1 = Monday through 7 = Sunday) and returns the name of the day. Call the function for all values 1–7, plus an invalid value (0), and print the results.

### Requirements
- [ ] Use a `switch` statement (not if/else)
- [ ] Each day number maps to its correct name (1=Monday, 2=Tuesday, ..., 7=Sunday)
- [ ] Include a `default` case that returns `"unknown"` for any value outside 1–7
- [ ] The function is called for values 0 through 7 and the output is printed

### Hints
<details>
<summary>Hint 1</summary>

The switch expression is the integer `n`. Each `case` is a single integer literal. The `default` case handles everything that didn't match, including 0 and negative numbers or values > 7.

</details>

### Expected Output / Acceptance Criteria
```
0: unknown
1: Monday
2: Tuesday
3: Wednesday
4: Thursday
5: Friday
6: Saturday
7: Sunday
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func dayName(n int) string {
    switch n {
    case 1:
        return "Monday"
    case 2:
        return "Tuesday"
    case 3:
        return "Wednesday"
    case 4:
        return "Thursday"
    case 5:
        return "Friday"
    case 6:
        return "Saturday"
    case 7:
        return "Sunday"
    default:
        return "unknown"
    }
}

func main() {
    for i := 0; i <= 7; i++ {
        fmt.Printf("%d: %s\n", i, dayName(i))
    }
}
```

**Explanation:**
Each `case` in Go's switch is independent — no `break` is needed between cases because Go does not fall through by default. The `default` case handles any value that didn't match, and it can appear anywhere in the switch (not just at the end, though the end is conventional). The function uses `return` inside switch cases, which is idiomatic Go — returning from inside a switch is fine because the switch is an expression-like statement.

</details>

---

## Exercise 3: if with Init Statement [🟢 Easy] [1 pt]

### Context
The `if` init statement is one of Go's most distinctive features. It lets you declare a variable, use it in the condition, and keep it scoped to the `if` block — reducing pollution of the outer scope. This is the preferred pattern for handling function calls that return `(value, error)`.

### Task
Write a Go program that:
1. Uses an `if` statement with an init statement to call `strconv.Atoi("123")`
2. If no error occurred, prints the parsed integer value
3. If an error occurred, prints the error
4. Then does the same for `strconv.Atoi("abc")` (which will produce an error)

### Requirements
- [ ] Both `Atoi` calls use the `if v, err := strconv.Atoi(...); err == nil { ... } else { ... }` form
- [ ] The variable `v` is not declared outside the `if` block
- [ ] The program prints the correct result for the valid input ("123" → 123) and an error message for the invalid input ("abc")
- [ ] Import `strconv` and `fmt`

### Hints
<details>
<summary>Hint 1</summary>

The init statement form is `if v, err := strconv.Atoi(s); err == nil { use v here } else { use err here }`. The semicolon separates the init statement from the condition.

</details>

<details>
<summary>Hint 2</summary>

`strconv.Atoi` returns `(int, error)`. When the input is a valid integer string, `err` is `nil` and `v` holds the integer. When the input is invalid, `err` is non-nil and `v` is 0.

</details>

### Expected Output / Acceptance Criteria
```
Parsed: 123
Parse error: strconv.Atoi: parsing "abc": invalid syntax
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    // Valid input
    if v, err := strconv.Atoi("123"); err == nil {
        fmt.Printf("Parsed: %d\n", v)
    } else {
        fmt.Printf("Parse error: %v\n", err)
    }

    // Invalid input
    if v, err := strconv.Atoi("abc"); err == nil {
        fmt.Printf("Parsed: %d\n", v)
    } else {
        fmt.Printf("Parse error: %v\n", err)
    }
}
```

**Explanation:**
The init statement `v, err := strconv.Atoi("123")` runs before the condition `err == nil` is evaluated. Both `v` and `err` are scoped to the entire `if`/`else` block — they go out of scope after the closing `}`. This is the idiomatic Go way to handle functions that return `(value, error)`: the variables are declared exactly where they're needed and don't clutter the outer scope. If you try to use `v` or `err` after the `if`/`else` block, you'll get a "undefined" compile error.

**Common wrong answers and why they fail:**
- Declaring `v` and `err` before the `if` statement with a separate `:=` — this works but misses the point of the exercise and pollutes the outer scope unnecessarily
- Writing `if err := ...; err != nil` for the success branch — this reverses the logic; the success branch should have `err == nil`

</details>

---

## Exercise 4: FizzBuzz [🟡 Medium] [2 pts]

### Context
FizzBuzz is a classic exercise that exercises `for` loops, modulo arithmetic, and conditional dispatch. In Go, it is a good opportunity to use the `switch` true idiom (switch with no condition), which is often more readable than a chain of `if`/`else if` when there are multiple range conditions.

### Task
Write a Go program that prints the numbers 1 through 30, one per line, with the following substitutions:
- If the number is divisible by both 3 and 5, print `FizzBuzz`
- If the number is divisible by 3 only, print `Fizz`
- If the number is divisible by 5 only, print `Buzz`
- Otherwise, print the number

### Requirements
- [ ] Use a `for` loop from 1 to 30 inclusive
- [ ] Use a `switch` statement (not `if`/`else if`) for the dispatch logic
- [ ] The FizzBuzz case (divisible by both) must be checked first to avoid it being shadowed by the Fizz or Buzz cases
- [ ] Output matches the expected results for all 30 numbers

### Hints
<details>
<summary>Hint 1</summary>

Use the switch-true idiom: `switch { case i%15 == 0: ... case i%3 == 0: ... }`. This form is equivalent to `if`/`else if` but reads more cleanly when there are multiple conditions.

</details>

### Expected Output / Acceptance Criteria
```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
Fizz
22
23
Fizz
Buzz
26
Fizz
28
29
FizzBuzz
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    for i := 1; i <= 30; i++ {
        switch {
        case i%15 == 0:
            fmt.Println("FizzBuzz")
        case i%3 == 0:
            fmt.Println("Fizz")
        case i%5 == 0:
            fmt.Println("Buzz")
        default:
            fmt.Println(i)
        }
    }
}
```

**Explanation:**
The `switch` with no condition is equivalent to `switch true` — each `case` expression is evaluated as a boolean. Cases are checked in order; the first true case wins. Checking `i%15 == 0` before `i%3 == 0` is essential: if you put `i%3 == 0` first, then 15 would print "Fizz" because it is divisible by 3 and the `i%15 == 0` case is never reached. An alternative is to check `i%3 == 0 && i%5 == 0` in the first case instead of `i%15 == 0` — both are equivalent since 15 = 3 × 5.

**Alternative approaches:**
You could also use `if`/`else if`/`else` — it works, but the `switch` form is considered more idiomatic for multiple mutually exclusive conditions. You could also store the result in a variable and use `fmt.Println(result)` once outside the switch, which avoids repeating `fmt.Println` in each branch.

</details>

---

## Exercise 5: Unicode Range Iteration [🟡 Medium] [2 pts]

### Context
Iterating over a string using `range` is a common operation, but the behavior surprises programmers from other languages: `range` yields Unicode code points (runes), not bytes. For strings containing only ASCII characters, rune indices and byte indices are identical. For strings containing multi-byte characters (emoji, accented letters, CJK characters), the byte index skips ahead by the character's byte width.

### Task
Write a Go program that:
1. Declares the string `s := "Hello 🌍!"`
2. Prints the byte length using `len(s)`
3. Iterates over `s` using `range`, printing each rune's byte index and Unicode value in the format `byte index  6: 🌍  (U+1F30D)`
4. Clearly shows in the output that the byte index jumps from 6 to 10 (skipping 7, 8, 9) for the multi-byte emoji character

### Requirements
- [ ] Use `range` to iterate over the string (not a classic index loop)
- [ ] Print `len(s)` to show the byte count
- [ ] For each rune, print its byte index and the rune itself (formatted with `%c`) and its Unicode code point (formatted with `%04X` or `U+%04X`)
- [ ] The output must make it visible that the emoji takes more than 1 byte (index jumps by 4)

### Hints
<details>
<summary>Hint 1</summary>

The `range` loop over a string yields `(int, rune)` — the first value is the byte index of the start of the rune, and the second value is the rune (Unicode code point) itself. Use `%c` to format a rune as its character, and `%04X` to format it as a hexadecimal Unicode code point.

</details>

<details>
<summary>Hint 2</summary>

To import the `unicode/utf8` package for `RuneCountInString`, add `"unicode/utf8"` to your import block. The emoji 🌍 is encoded in UTF-8 as 4 bytes (U+1F30D is in the range U+010000–U+10FFFF, which requires 4 bytes in UTF-8).

</details>

### Expected Output / Acceptance Criteria
Your output should clearly show the byte index jumping by 4 at the emoji position. The exact format can vary slightly, but the byte index jump must be visible:
```
Byte length: 11
Rune iteration:
  byte index  0: H  (U+0048)
  byte index  1: e  (U+0065)
  byte index  2: l  (U+006C)
  byte index  3: l  (U+006C)
  byte index  4: o  (U+006F)
  byte index  5:    (U+0020)
  byte index  6: 🌍  (U+1F30D)
  byte index 10: !  (U+0021)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    s := "Hello 🌍!"

    fmt.Printf("Byte length: %d\n", len(s))
    fmt.Printf("Rune count:  %d\n", utf8.RuneCountInString(s))
    fmt.Println("Rune iteration:")

    for i, r := range s {
        fmt.Printf("  byte index %2d: %c  (U+%04X)\n", i, r, r)
    }
}
```

**Explanation:**
`len(s)` returns the number of bytes in the string's UTF-8 encoding, not the number of characters. "Hello 🌍!" is 11 bytes long: 7 ASCII characters (1 byte each) plus the emoji 🌍 (4 bytes). `utf8.RuneCountInString(s)` returns 8 — the actual character count. The `range` loop yields byte positions: H is at byte 0, space is at byte 5, 🌍 starts at byte 6, and ! follows at byte 10 (because 6 + 4 bytes for the emoji = 10). Using a classic `for i := 0; i < len(s); i++` loop and accessing `s[i]` would give you individual bytes — `s[6]`, `s[7]`, `s[8]`, `s[9]` would be the 4 raw bytes of the emoji encoding, none of which would print as 🌍.

**Step-by-step explanation:**
1. Declare the string with an emoji
2. Use `len()` to show byte count vs `utf8.RuneCountInString()` for rune count
3. `range` over the string yields `(byteIndex int, r rune)` pairs
4. Format with `%2d` for byte index alignment, `%c` for the character, `%04X` for the Unicode code point

**Why this approach:**
This approach is the correct and idiomatic way to iterate over Unicode text in Go. Using `for i := 0; i < len(s); i++` for Unicode text is a common bug — it works for ASCII but corrupts multi-byte characters.

**What a weaker solution looks like and why it fails:**
A byte-indexed loop `for i := 0; i < len(s); i++ { fmt.Printf("%d: %c\n", i, s[i]) }` would print garbage for the emoji — it would print 4 separate unreadable bytes instead of the emoji character.

</details>

---

## Exercise 6: File Reading with defer [🟡 Medium] [2 pts]

### Context
`defer` is Go's primary mechanism for guaranteed cleanup. The canonical pattern is: open a resource, check the error, and immediately defer the close. This exercise demonstrates that pattern with file I/O, which is the most common real-world use of `defer`.

### Task
Write a Go function `printFile(path string) error` that:
1. Opens the file at `path` using `os.Open`
2. Returns the error immediately if the open fails
3. Uses `defer` to close the file — placed on the very next line after the successful open
4. Reads the entire file content using `io.ReadAll`
5. Prints the content to standard output
6. Returns any read error

Call `printFile("/etc/hostname")` from `main`. Handle the error by printing it and exiting with `os.Exit(1)`.

### Requirements
- [ ] `defer f.Close()` appears immediately after the error check for `os.Open`, not at the end of the function
- [ ] The function returns the error from `os.Open` without deferring first (never defer before checking for nil)
- [ ] The function returns the error from `io.ReadAll` if it fails
- [ ] Imports: `"fmt"`, `"io"`, `"os"`

### Hints
<details>
<summary>Hint 1</summary>

The pattern is:
```go
f, err := os.Open(path)
if err != nil {
    return err      // return BEFORE defer — no defer on nil handle
}
defer f.Close()     // defer AFTER successful open
```

</details>

<details>
<summary>Hint 2</summary>

`io.ReadAll(f)` returns `([]byte, error)`. To print it as a string, use `string(data)` or `fmt.Printf("%s", data)`.

</details>

### Expected Output / Acceptance Criteria
On a typical Linux system:
```
myhostname
```
(The actual content depends on your system's `/etc/hostname`.)

The key acceptance criterion is the structure: `defer f.Close()` placed between the error check and the `io.ReadAll` call, not at the bottom of the function.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "io"
    "os"
)

func printFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("open %s: %w", path, err)
    }
    defer f.Close() // runs when printFile returns, regardless of how

    data, err := io.ReadAll(f)
    if err != nil {
        return fmt.Errorf("read %s: %w", path, err)
    }

    fmt.Printf("%s", data)
    return nil
}

func main() {
    if err := printFile("/etc/hostname"); err != nil {
        fmt.Fprintf(os.Stderr, "error: %v\n", err)
        os.Exit(1)
    }
}
```

**Explanation:**
`defer f.Close()` is registered immediately after the successful `os.Open`. This placement is intentional and idiomatic — it keeps the "acquire" and "register cleanup" visually adjacent, making it easy to audit that every opened resource has a deferred close. Even if `io.ReadAll` returns an error and the function returns early on the next line, `f.Close()` will still be called. The `fmt.Errorf("open %s: %w", path, err)` wraps the error with context — the `%w` verb makes the original error unwrappable with `errors.Is`/`errors.As`.

</details>

---

## Exercise 7: Triangle with Labeled Break [🔴 Hard] [3 pts]

### Context
Nested loops are common in grid-based algorithms, matrix operations, and combinatorics. Go's labeled `break` provides a clean way to exit an outer loop from inside an inner loop without a boolean flag variable. This is a multi-step exercise: you need to understand the triangle printing logic and then add the early-exit condition.

### Task
Write a Go program that:
1. Uses nested `for` loops (outer: rows 1–5, inner: cols 1 to current row) to print a right-triangle pattern
2. Labels the outer loop `outer:`
3. Inside the inner loop, if `row + col > 6`, prints a message showing the stopping coordinates and breaks out of the **outer** loop using the label

### Requirements
- [ ] The outer loop iterates `row` from 1 to 5
- [ ] The inner loop iterates `col` from 1 to `row` (inclusive)
- [ ] After each inner loop completes normally, print a newline
- [ ] If `row+col > 6`, print `"\nStopped at row=%d, col=%d"` and break the outer loop
- [ ] Without the early exit, the full triangle would be: rows of 1, 2, 3, 4, and 5 cells respectively

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

The label syntax is:
```go
outer:
    for row := 1; row <= 5; row++ {
        // inner loop here
    }
```
The label must be on the line immediately before the `for` keyword (with no blank line between them is conventional, though both work).

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

`break outer` exits the loop labeled `outer`. A plain `break` without a label only exits the innermost loop. Test your understanding: when does the labeled break fire? It should fire when `row=4, col=3` because 4+3=7 > 6.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

Inside the inner loop:
```go
if row+col > 6 {
    fmt.Printf("\nStopped at row=%d, col=%d (sum=%d)\n", row, col, row+col)
    break outer
}
fmt.Printf("(%d,%d) ", row, col)
```
The check comes before the print so the stopping cell isn't printed as part of the triangle.

</details>

### Expected Output / Acceptance Criteria
```
(1,1) 
(2,1) (2,2) 
(3,1) (3,2) (3,3) 
(4,1) (4,2) 
Stopped at row=4, col=3 (sum=7)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
outer:
    for row := 1; row <= 5; row++ {
        for col := 1; col <= row; col++ {
            if row+col > 6 {
                fmt.Printf("\nStopped at row=%d, col=%d (sum=%d)\n", row, col, row+col)
                break outer
            }
            fmt.Printf("(%d,%d) ", row, col)
        }
        fmt.Println()
    }
}
```

**Step-by-step explanation:**

1. The outer loop runs `row` from 1 to 5; the inner loop runs `col` from 1 to `row`.
2. For rows 1, 2, 3: no cell has `row+col > 6` (max is 3+3=6, which is not strictly greater), so all cells print and we proceed to the next row.
3. For row 4, col 1: 4+1=5, prints `(4,1)`. Col 2: 4+2=6, prints `(4,2)`. Col 3: 4+3=7 > 6 — the break fires.
4. `break outer` exits the outer `for row` loop immediately; the `fmt.Println()` after the inner loop is never reached for row 4, which is why the "Stopped" message provides its own newline.

**Why this approach:**
The labeled break avoids a flag variable (`earlyExit := false`) that would need to be checked after the inner loop. The label makes the intent explicit — the reader sees `break outer` and immediately knows which loop is being exited.

**What a weaker solution looks like and why it fails:**
Using `break` without a label only exits the inner loop. The outer loop would then continue to row 5, which is not the intended behavior. Using a flag variable works but is more verbose and requires the outer loop to check the flag after each inner loop completes.

</details>

---

## Exercise 8: Type Switch Function [🔴 Hard] [3 pts]

### Context
A type switch is a Go construct that tests the dynamic type of an interface value. It is distinct from a regular switch — the cases are types, not values, and the case variable is automatically typed within each branch. This exercise requires understanding both `interface{}` (the empty interface, which accepts any value) and how to use a type switch to dispatch on concrete types.

### Task
Write a Go function `describe(i interface{}) string` that returns a string description based on the runtime type of `i`:
- `int` → `"integer: <value>"`
- `float64` → `"float: <value>"`
- `string` → `"string: \"<value>\""`
- `bool` → `"boolean: <value>"`
- Anything else → `"unknown type: <Go type name>"`

Call `describe` with at least 5 different values covering all 5 cases and print the results.

### Requirements
- [ ] Use a type switch (`switch v := i.(type) { case int: ... }`)
- [ ] The function signature is exactly `func describe(i interface{}) string`
- [ ] All 5 case types are covered (int, float64, string, bool, default)
- [ ] The return value includes the actual value (e.g., `"integer: 42"`, not just `"integer"`)
- [ ] The function is called with at least one value of each type

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

The type switch syntax is:
```go
switch v := i.(type) {
case int:
    // v is typed as int here
case string:
    // v is typed as string here
default:
    // use %T to get the type name: fmt.Sprintf("unknown type: %T", v)
}
```

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

In the `default` branch, `v` has the same type as `i` (interface{}), but you can get the type name as a string with `fmt.Sprintf("%T", v)`. For the `string` case, use `%q` format to include the surrounding quotes.

</details>

### Expected Output / Acceptance Criteria
```
integer: 42
float: 3.14
string: "hello"
boolean: true
unknown type: []int
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func describe(i interface{}) string {
    switch v := i.(type) {
    case int:
        return fmt.Sprintf("integer: %d", v)
    case float64:
        return fmt.Sprintf("float: %g", v)
    case string:
        return fmt.Sprintf("string: %q", v)
    case bool:
        return fmt.Sprintf("boolean: %v", v)
    default:
        return fmt.Sprintf("unknown type: %T", v)
    }
}

func main() {
    values := []interface{}{42, 3.14, "hello", true, []int{1, 2, 3}}
    for _, v := range values {
        fmt.Println(describe(v))
    }
}
```

**Step-by-step explanation:**

1. The function parameter `i interface{}` accepts any value — `interface{}` is the empty interface satisfied by all types.
2. `switch v := i.(type)` is the type switch syntax. `v` is re-typed in each case to the matched concrete type.
3. In `case int:`, `v` is an `int` — you can call integer operations on it.
4. In `default:`, `v` remains an `interface{}`, but `%T` formats its underlying type name.
5. The main function stores different types in a `[]interface{}` slice and ranges over them.

**Why this approach:**
A type switch is cleaner than chaining `_, ok := i.(int)` type assertions for each type. In the type switch, the variable `v` is automatically narrowed to the concrete type in each case, so you don't need an explicit assertion in each branch.

**What a weaker solution looks like and why it fails:**
Using multiple `if` statements with type assertions (`if v, ok := i.(int); ok`) works but is more verbose. Using `reflect.TypeOf(i).Kind()` also works but imports the `reflect` package unnecessarily when a type switch suffices.

</details>

---

## Exercise 9: Traffic Light State Machine [⭐ Expert] [5 pts]

### Context
A state machine transitions between a fixed set of states based on defined rules. This is a fundamental pattern in protocol implementations, parsers, game logic, and UI systems. This exercise combines `iota` constants, a `for` loop as the main driver, and a `switch` as the transition function — three of this module's core concepts working together.

### Task
Implement a traffic light state machine in Go:

1. Define a custom type `Light int` and use `iota` to define three constants: `Red`, `Green`, `Yellow` (in that order, starting from 0)
2. Write a function `next(l Light) Light` that returns the next state: Red → Green → Yellow → Red
3. Write a function `name(l Light) string` that returns the string name of a state
4. In `main`, start with `current := Red` and loop 9 times (3 full cycles), printing the current state on each iteration, then advance to the next state

### Requirements
- [ ] Use `iota` for the Light constants
- [ ] `next` uses a `switch` statement to implement the transition logic
- [ ] `name` uses a `switch` statement to return the state name
- [ ] The main loop runs exactly 9 iterations (cycles 0–8), printing 9 state names
- [ ] The output shows the full cycle Red → Green → Yellow repeating 3 times

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

```go
type Light int

const (
    Red Light = iota  // 0
    Green             // 1
    Yellow            // 2
)
```

`iota` auto-increments in a `const` block. Each constant in the block gets the current `iota` value (starting at 0).

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

The `next` function is a pure transition function: given the current state, return the next. The loop in `main` calls `next` at the end of each iteration: `current = next(current)`.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
func next(l Light) Light {
    switch l {
    case Red:
        return Green
    case Green:
        return Yellow
    case Yellow:
        return Red
    default:
        return Red // safe fallback
    }
}
```

For the main loop: `for i := 0; i < 9; i++ { fmt.Printf("Cycle %d: %s\n", i, name(current)); current = next(current) }`

</details>

### Expected Output / Acceptance Criteria
```
Cycle 0: Red
Cycle 1: Green
Cycle 2: Yellow
Cycle 3: Red
Cycle 4: Green
Cycle 5: Yellow
Cycle 6: Red
Cycle 7: Green
Cycle 8: Yellow
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Light is a custom integer type for traffic light states
type Light int

const (
    Red    Light = iota // 0
    Green               // 1
    Yellow              // 2
)

// next returns the next traffic light state
func next(l Light) Light {
    switch l {
    case Red:
        return Green
    case Green:
        return Yellow
    case Yellow:
        return Red
    default:
        return Red // safe fallback for unknown state
    }
}

// name returns the string name of a Light state
func name(l Light) string {
    switch l {
    case Red:
        return "Red"
    case Green:
        return "Green"
    case Yellow:
        return "Yellow"
    default:
        return "Unknown"
    }
}

func main() {
    current := Red
    for i := 0; i < 9; i++ {
        fmt.Printf("Cycle %d: %s\n", i, name(current))
        current = next(current)
    }
}
```

**Step-by-step explanation:**

1. `type Light int` creates a new named type based on `int`. Using a named type instead of bare `int` prevents accidentally passing an arbitrary integer where a `Light` is expected.
2. `iota` in the `const` block starts at 0 and increments for each constant: `Red=0`, `Green=1`, `Yellow=2`.
3. `next` is a pure function — given a state, return the next. The `switch` makes transitions explicit and exhaustive; the `default` is a safety net.
4. `name` converts a state to its human-readable string — this pattern (a type plus a `switch`-based `String()` method) is so common in Go that there's a tool `stringer` that generates it automatically.
5. The main loop runs 9 times. Each iteration prints the current state and then advances. Because 9 = 3 × 3, three complete Red→Green→Yellow cycles are shown.

**Why this approach:**
Separating `next` (transition logic) from `name` (display logic) keeps each function focused. The state machine is easy to extend: adding a new state requires adding a constant and updating two switch statements. The `for` loop is the event loop — in a real system, it would wait for a timer or user input instead of running 9 fixed iterations.

**What a weaker solution looks like and why it fails:**
Using bare `int` constants instead of a named `Light` type compiles fine but loses type safety — a function expecting a `Light` would accept any `int`. Using `if`/`else if` instead of `switch` works but is less readable for a dispatch-by-value pattern with a fixed set of known states.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Two Ways to Loop | — | —/1 | — | — |
| Exercise 2 — Day of the Week Switch | — | —/1 | — | — |
| Exercise 3 — if with Init Statement | — | —/1 | — | — |
| Exercise 4 — FizzBuzz | — | —/2 | — | — |
| Exercise 5 — Unicode Range Iteration | — | —/2 | — | — |
| Exercise 6 — File Reading with defer | — | —/2 | — | — |
| Exercise 7 — Triangle with Labeled Break | — | —/3 | — | — |
| Exercise 8 — Type Switch Function | — | —/3 | — | — |
| Exercise 9 — Traffic Light State Machine | — | —/5 | — | — |
| **Total** | | **—/20** | | |

**Passing threshold:** 13/20 (65%). Aim for 17/20 (85%) before taking the test.
