# Exercises — Module 1: Types and Variables

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read through — actually type and run your code.
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
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Zero Value Survey [🟢 Easy] [1 pt]

### Context
Before you can work with Go types confidently, you need to know exactly what each type looks like when it is not explicitly initialized. This exercise forces you to observe zero values directly — and to predict them before running, which is the real test.

### Task
Declare variables of **5 different types** (`int`, `float64`, `string`, `bool`, and one of your choice from: `int64`, `uint8`, `rune`, `complex128`) using `var` with an explicit type but **no initial value**. Print each variable. Before running the code, write down your prediction for each zero value.

### Requirements
- [ ] Use `var name type` syntax (no `=` or `:=`)
- [ ] Declare at least 5 different types
- [ ] Print each variable with a label (e.g., `fmt.Printf("int: %v\n", i)`)
- [ ] Use `%q` for the string so the empty string is visible as `""`

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

`var x int` declares `x` as an int with no explicit value. Go will initialize it to the zero value for `int`.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The `%q` verb in `fmt.Printf` prints strings with surrounding quotes — useful for making an empty string visible: `fmt.Printf("string: %q\n", s)` prints `string: ""`.

</details>

### Expected Output / Acceptance Criteria
```
int:     0
float64: 0
string:  ""
bool:    false
<your chosen type>: <its zero value>
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

func main() {
    var i int
    var f float64
    var s string
    var b bool
    var r rune

    fmt.Printf("int:     %v\n", i)
    fmt.Printf("float64: %v\n", f)
    fmt.Printf("string:  %q\n", s)
    fmt.Printf("bool:    %v\n", b)
    fmt.Printf("rune:    %v\n", r)
}
```

**Explanation:**
Every type in Go has a defined zero value. For numeric types it is `0`, for `bool` it is `false`, for `string` it is `""` (empty string), and for `rune` (which is `int32`) it is also `0`. The `%q` verb for strings makes the empty string visible as `""` rather than just a blank line.

**Common wrong answers and why they fail:**
- Declaring `var s string = ""` — this works but misses the point; the exercise is about observing that you don't need to write `= ""` because Go does it automatically.
- Using `:=` — this requires a value on the right side; you cannot write `s := ` with nothing after it.

</details>

---

## Exercise 2: Type Inference Inspector [🟢 Easy] [1 pt]

### Context
When you use `:=`, Go infers the type from the value. This exercise gives you practice observing what types Go actually infers, which is important for avoiding surprises when you later need a specific type.

### Task
Use the short declaration `:=` to declare **3 variables** with different literal values. Print both the **value** and the **type** of each variable using `fmt.Printf("%T\n", x)`. Include at least one integer literal, one floating-point literal, and one string literal.

### Requirements
- [ ] Use `:=` for all declarations
- [ ] Declare at least 3 variables with different literal types
- [ ] Print each variable's type using `%T`
- [ ] Write down your prediction before running: what type will each literal produce?

### Hints
<details>
<summary>Hint 1</summary>

`fmt.Printf("%T\n", x)` prints the type of `x`. For example, if `x := 42`, it prints `int`. The format verb `%T` (capital T) is the type verb.

</details>

### Expected Output / Acceptance Criteria
```
42 is int
3.14 is float64
hello is string
```
_(Exact values will differ based on your chosen literals.)_

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    a := 42
    b := 3.14
    c := "hello"

    fmt.Printf("%v is %T\n", a, a)
    fmt.Printf("%v is %T\n", b, b)
    fmt.Printf("%v is %T\n", c, c)
}
```

**Explanation:**
Integer literals default to `int`, floating-point literals default to `float64`, and string literals default to `string`. These defaults apply whenever you use `:=` or `var name = value`. If you need a different type — say `int32` or `float32` — you must force it with an explicit conversion: `a := int32(42)`.

</details>

---

## Exercise 3: Days of the Week with iota [🟢 Easy] [1 pt]

### Context
`iota` is Go's mechanism for defining enumerated constants without boilerplate. This exercise builds the muscle memory for the basic `iota` pattern that appears in nearly every real Go codebase.

### Task
Create a `const` block using `iota` to represent the days of the week, with `Sunday = 0` through `Saturday = 6`. In `main`, print the numeric value of each day constant.

### Requirements
- [ ] Use a `const` block with `iota`
- [ ] `Sunday` must equal `0`, `Saturday` must equal `6`
- [ ] Print each constant's value in `main`
- [ ] Confirm that `iota` produces the expected integer values

### Hints
<details>
<summary>Hint 1</summary>

In a `const` block, you only need to write `= iota` on the first constant. Subsequent constants in the same block automatically use the same expression with an incremented `iota` value.

</details>

<details>
<summary>Hint 2</summary>

```go
const (
    Sunday = iota  // 0
    Monday         // 1
    // ...
)
```
Each line below `Sunday` implicitly repeats the `= iota` expression with the next value.

</details>

### Expected Output / Acceptance Criteria
```
Sunday: 0
Monday: 1
Tuesday: 2
Wednesday: 3
Thursday: 4
Friday: 5
Saturday: 6
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

const (
    Sunday = iota
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
)

func main() {
    fmt.Printf("Sunday: %d\n", Sunday)
    fmt.Printf("Monday: %d\n", Monday)
    fmt.Printf("Tuesday: %d\n", Tuesday)
    fmt.Printf("Wednesday: %d\n", Wednesday)
    fmt.Printf("Thursday: %d\n", Thursday)
    fmt.Printf("Friday: %d\n", Friday)
    fmt.Printf("Saturday: %d\n", Saturday)
}
```

**Explanation:**
`iota` starts at `0` in each new `const` block and increments by `1` for each constant specification. Only `Sunday` needs `= iota`; the rest inherit the expression. This is why each day's value is exactly its position in the block.

**Common wrong answers and why they fail:**
- Writing `= iota` on every line — this compiles and works identically, but it is redundant and non-idiomatic.
- Placing the `const` block inside `main` — this works, but note that package-level constants are more common in real code.

</details>

---

## Exercise 4: Temperature Converter [🟡 Medium] [2 pts]

### Context
Floating-point arithmetic and type-safe variables are used constantly in scientific, financial, and engineering code. This exercise requires you to think carefully about float64 vs integer arithmetic — a subtle but important distinction.

### Task
Write a temperature converter that converts **Celsius to Fahrenheit** for a set of hardcoded input values. Use the formula `F = C * 9/5 + 32`. Test with at least these three values: `0°C`, `100°C`, and `-40°C`.

### Requirements
- [ ] Declare all temperature variables as `float64`
- [ ] Use the formula `F = C * 9.0/5.0 + 32.0` (with `.0` suffixes — explain in a comment why)
- [ ] Print both values with exactly 2 decimal places using `fmt.Printf("%.2f°C = %.2f°F\n", c, f)`
- [ ] Verify: 0°C = 32°F, 100°C = 212°F, -40°C = -40°F

### Hints
<details>
<summary>Hint 1</summary>

In Go, `9/5` is integer division and evaluates to `1` (not `1.8`). This would make your formula `F = C * 1 + 32`, which gives completely wrong results. Using `9.0/5.0` or `float64(9)/float64(5)` forces floating-point division.

</details>

<details>
<summary>Hint 2</summary>

The `%.2f` format verb prints a float with exactly 2 decimal places. `%f` prints 6 decimal places by default.

</details>

### Expected Output / Acceptance Criteria
```
0.00°C = 32.00°F
100.00°C = 212.00°F
-40.00°C = -40.00°F
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    // 9.0/5.0 ensures floating-point division; 9/5 would be integer division = 1
    temperatures := [3]float64{0.0, 100.0, -40.0}

    for _, celsius := range temperatures {
        fahrenheit := celsius*9.0/5.0 + 32.0
        fmt.Printf("%.2f°C = %.2f°F\n", celsius, fahrenheit)
    }
}
```

**Explanation:**
The critical detail is `9.0/5.0` instead of `9/5`. In Go, if both operands of `/` are untyped integer literals, the result is integer division. `9/5 = 1`, not `1.8`. Using `9.0` makes both operands floating-point literals, so the division produces `1.8`. Since `celsius` is `float64`, the full expression `celsius*9.0/5.0+32.0` is a `float64` computation throughout.

**Alternative approaches:**
You could also write `celsius*(9.0/5.0) + 32.0` or even precompute `const factor = 9.0 / 5.0` and use `celsius*factor + 32.0`. The key constraint is ensuring no integer division occurs anywhere in the formula.

</details>

---

## Exercise 5: Permission Flags with iota [🟡 Medium] [2 pts]

### Context
Bit-flag constants using `iota` with bit shifts appear in Go's standard library (e.g., `os.FileMode`, HTTP method flags, log level flags) and in nearly every systems-level Go package. This exercise builds familiarity with the pattern so you can read and write it fluently.

### Task
Define file permission constants using `iota` with bit shifts: `ReadPerm = 1`, `WritePerm = 2`, `ExecPerm = 4`. Then write a function `printPerms(p int)` that prints which permissions are set. In `main`, test at least three permission combinations.

### Requirements
- [ ] Define `ReadPerm`, `WritePerm`, and `ExecPerm` using `1 << iota`
- [ ] Write a function that tests each flag using bitwise AND (`&`)
- [ ] Test combinations: read-only, read+write, and all three
- [ ] Print the numeric value of each permission set alongside the flag names

### Hints
<details>
<summary>Hint 1</summary>

To test whether a flag bit is set, use `perms & FlagName != 0`. The bitwise AND isolates the bit: if that bit is 1 in both operands, the result is non-zero; otherwise it is 0.

</details>

<details>
<summary>Hint 2</summary>

To combine multiple flags, use bitwise OR (`|`): `ReadPerm | WritePerm` gives a value with both the read and write bits set.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
const (
    ReadPerm  = 1 << iota // 1 << 0 = 1
    WritePerm             // 1 << 1 = 2
    ExecPerm              // 1 << 2 = 4
)
```
Each successive constant doubles the value because bit position increases by 1.

</details>

### Expected Output / Acceptance Criteria
```
Permissions (1): read
Permissions (3): read write
Permissions (7): read write execute
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

const (
    ReadPerm  = 1 << iota // 1
    WritePerm             // 2
    ExecPerm              // 4
)

func printPerms(p int) {
    fmt.Printf("Permissions (%d):", p)
    if p&ReadPerm != 0 {
        fmt.Print(" read")
    }
    if p&WritePerm != 0 {
        fmt.Print(" write")
    }
    if p&ExecPerm != 0 {
        fmt.Print(" execute")
    }
    fmt.Println()
}

func main() {
    printPerms(ReadPerm)                    // 1
    printPerms(ReadPerm | WritePerm)        // 3
    printPerms(ReadPerm | WritePerm | ExecPerm) // 7
}
```

**Step-by-step explanation:**

1. `ReadPerm = 1 << 0 = 1` (binary: 001)
2. `WritePerm = 1 << 1 = 2` (binary: 010)
3. `ExecPerm = 1 << 2 = 4` (binary: 100)
4. Combining with `|`: `001 | 010 = 011 = 3`; `001 | 010 | 100 = 111 = 7`
5. Testing with `&`: `011 & 001 = 001 ≠ 0` → read is set; `011 & 100 = 000 = 0` → exec not set

**Why this approach:**
Powers of two are the only values where each number has exactly one bit set, so they never "overlap" when combined with OR. This is the mathematical foundation of bitmask flags.

**What a weaker solution looks like and why it fails:**
Using `iota` without the bit shift (`ReadPerm = iota`) gives values 0, 1, 2. The value 0 cannot be a flag — you cannot test for it with `&` because zero AND anything is zero. Bit-shift flags work precisely because each value has exactly one bit set at a unique position.

</details>

---

## Exercise 6: Type Conversion Roundtrip [🟡 Medium] [2 pts]

### Context
Type conversion in Go is explicit — and for good reason. This exercise forces you to observe what actually happens during numeric conversions, particularly the precision loss from float-to-int, and demonstrates the `string(int)` vs `strconv.Itoa(int)` distinction that trips up many beginners.

### Task
Write a program that: (1) starts with an `int` value of `42`, converts it to `float64`, adds `0.9`, then converts back to `int` — and prints what is lost; (2) demonstrates the difference between `string(65)` and `strconv.Itoa(65)`.

### Requirements
- [ ] Show the float64 value after adding 0.9: should be 42.9
- [ ] Show the int value after converting back: should be 42 (not 43 — float-to-int truncates)
- [ ] Print `string(65)` and explain in a comment what it produces
- [ ] Print `strconv.Itoa(65)` and explain in a comment what it produces
- [ ] Import `strconv`

### Hints
<details>
<summary>Hint 1</summary>

`int(3.9)` truncates toward zero in Go — it gives `3`, not `4`. This is different from rounding. `int(-3.9)` gives `-3`, not `-4`.

</details>

<details>
<summary>Hint 2</summary>

`string(n)` where `n` is an integer converts the integer as a Unicode code point. Code point 65 is 'A'. To get the decimal string `"65"`, use `strconv.Itoa(65)` (or `fmt.Sprintf("%d", 65)`).

</details>

### Expected Output / Acceptance Criteria
```
Start:         42 (int)
After float64: 42.9
After int:     42  (truncated, not rounded — 0.9 is lost)
string(65):    A   (Unicode code point 65 = 'A')
Itoa(65):      65  (decimal string representation)
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
    // Part 1: Numeric type conversion roundtrip
    original := 42
    asFloat := float64(original) + 0.9
    backToInt := int(asFloat) // truncates toward zero — does NOT round

    fmt.Printf("Start:         %d (int)\n", original)
    fmt.Printf("After float64: %.1f\n", asFloat)
    fmt.Printf("After int:     %d  (truncated, not rounded — 0.9 is lost)\n", backToInt)

    fmt.Println()

    // Part 2: string(int) vs strconv.Itoa(int)
    n := 65
    asChar := string(n)           // Unicode code point 65 = 'A'
    asDecimal := strconv.Itoa(n)  // decimal string representation = "65"

    fmt.Printf("string(65):    %s   (Unicode code point 65 = 'A')\n", asChar)
    fmt.Printf("Itoa(65):      %s  (decimal string representation)\n", asDecimal)
}
```

**Explanation:**
`int(asFloat)` truncates toward zero — it discards the fractional part without rounding. `42.9` becomes `42`; `42.1` would also become `42`. If you need rounding, you must do it manually: `int(math.Round(asFloat))`.

For the string conversion: `string(n)` interprets `n` as a Unicode code point and returns the UTF-8 encoding of that character. This is a valid and useful operation — it just rarely does what you want when `n` is an integer you're trying to display. `strconv.Itoa` ("Integer to ASCII") converts the integer value to its decimal string representation.

</details>

---

## Exercise 7: Integer Overflow Demonstration [🔴 Hard] [3 pts]

### Context
Go's integer overflow behavior is silent — no panic, no error, just wrapping arithmetic. Understanding this is essential for any code that does numeric computation, especially with fixed-size types. This exercise asks you not just to reproduce the behavior but to explain it at the bit level.

### Task
Write a program that demonstrates integer overflow for `int8`. Declare `var x int8 = 127` (the maximum value for `int8`), increment it with `x++`, and print the result. Do the same for `uint8 = 255`. Print clear before/after labels. Add a comment explaining _why_ the value wraps to what it does.

### Requirements
- [ ] Demonstrate `int8` overflow from `127` to `-128`
- [ ] Demonstrate `uint8` overflow from `255` to `0`
- [ ] Print before and after values with labels
- [ ] Include a comment explaining the two's-complement reason for `int8` wrapping to `-128`
- [ ] Include a comment noting that Go does NOT panic on overflow

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

`var x int8 = 127` declares a signed 8-bit integer at its maximum value. `x++` is equivalent to `x = x + 1`. The compiler will not prevent this.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

`int8` uses 8 bits with two's-complement representation. The bit pattern `01111111` is `127`. Adding 1 produces `10000000`. In two's-complement 8-bit encoding, `10000000` represents `-128`.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

For `uint8`: all 8 bits set (`11111111`) is `255`. Adding 1 produces `100000000`, which is 9 bits — but `uint8` only has 8 bits, so the top bit is dropped, leaving `00000000` = `0`.

</details>

### Expected Output / Acceptance Criteria
```
int8 overflow:
  Before: 127
  After:  -128

uint8 overflow:
  Before: 255
  After:  0
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    // int8 overflow: max value is 127 (binary: 01111111)
    // Adding 1 produces binary: 10000000
    // In two's-complement 8-bit, 10000000 represents -128
    // Go does NOT panic — it silently wraps around
    var x int8 = 127
    fmt.Println("int8 overflow:")
    fmt.Printf("  Before: %d\n", x)
    x++
    fmt.Printf("  After:  %d\n", x) // -128

    fmt.Println()

    // uint8 overflow: max value is 255 (binary: 11111111)
    // Adding 1 produces binary: 100000000 (9 bits)
    // uint8 only holds 8 bits, so the carry bit is discarded
    // Result is 00000000 = 0
    var u uint8 = 255
    fmt.Println("uint8 overflow:")
    fmt.Printf("  Before: %d\n", u)
    u++
    fmt.Printf("  After:  %d\n", u) // 0
}
```

**Step-by-step explanation:**

1. `int8` uses 8 bits with two's-complement encoding. The range is -128 to 127.
2. `127` in binary is `01111111`. The leading `0` indicates a positive number.
3. `127 + 1` in binary is `10000000`. In two's-complement, a leading `1` means negative. `10000000` represents `-(2^7) = -128`.
4. For `uint8`, `255` is `11111111`. Adding `1` produces `100000000` — the carry bit that doesn't fit in 8 bits is dropped, leaving `00000000` = `0`.
5. This behavior is defined in Go's specification — it is not undefined behavior as in C.

**Why this approach:**
Overflow demonstration exercises matter because the consequences are real: a server that accepts an 8-bit age field could have an "age" of 200 silently turn into -56. Fixed-size type overflows are a class of security vulnerability (integer overflow attacks). Knowing the behavior lets you reason about when it can be exploited or cause bugs.

**What a weaker solution looks like and why it fails:**
Simply printing the after value without the before value and without any explanation doesn't achieve the goal — the output alone doesn't communicate why the value changed.

</details>

---

## Exercise 8: Swap Without a Temp Variable [🔴 Hard] [3 pts]

### Context
Go's multiple assignment feature — where the right-hand side is evaluated completely before any assignment happens — enables a clean swap idiom that requires no temporary variable. This exercise solidifies your understanding of how Go's simultaneous assignment works.

### Task
Write a program with two integer variables `a` and `b`. Without declaring any intermediate "temp" variable, swap the values of `a` and `b` using Go's multiple assignment. Print the values before and after the swap. Then explain in a comment why `a, b = b, a` works correctly but sequential `a = b; b = a` does not.

### Requirements
- [ ] Declare `a` and `b` with distinct initial values
- [ ] Swap without a temp variable using `a, b = b, a`
- [ ] Print before and after values
- [ ] Include a comment explaining why sequential assignment fails but simultaneous assignment works
- [ ] Add a third variable `c` and demonstrate a three-way rotation: `a, b, c = b, c, a`

### Hints
<details>
<summary>Hint 1</summary>

In Go's multiple assignment (`a, b = b, a`), all right-hand side expressions are evaluated before any assignment is performed. Both `b` and `a` are read with their original values, then the assignments happen.

</details>

<details>
<summary>Hint 2</summary>

Sequential assignment (`a = b; b = a`) overwrites `a` before `b` is assigned from the old `a`. After `a = b`, the original value of `a` is gone, so `b = a` just copies `b` back to itself.

</details>

### Expected Output / Acceptance Criteria
```
Before swap: a=10 b=20
After swap:  a=20 b=10

Before rotation: a=1 b=2 c=3
After rotation:  a=2 b=3 c=1
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    a, b := 10, 20

    fmt.Printf("Before swap: a=%d b=%d\n", a, b)

    // Go evaluates the entire right side before any assignment.
    // b and a are read with original values, THEN assigned.
    // Sequential would fail: a=b destroys original a before b=a can use it.
    a, b = b, a

    fmt.Printf("After swap:  a=%d b=%d\n", a, b)

    fmt.Println()

    // Three-way rotation using simultaneous assignment
    a, b, c := 1, 2, 3

    fmt.Printf("Before rotation: a=%d b=%d c=%d\n", a, b, c)

    // All three right-hand values (b, c, a) are read first,
    // then assigned to (a, b, c) simultaneously.
    a, b, c = b, c, a

    fmt.Printf("After rotation:  a=%d b=%d c=%d\n", a, b, c)
}
```

**Explanation:**
Go's specification states: "The assignment proceeds in two phases. First, the operands of index expressions and pointer indirections on the left and the expressions on the right are all evaluated in the usual order. Second, the assignments are carried out in left-to-right order."

This means in `a, b = b, a`, both `b` (right side 1st) and `a` (right side 2nd) are evaluated with their current values before either assignment. Then `a` gets the old `b` and `b` gets the old `a` — a true swap.

Sequential `a = b; b = a` is different: after `a = b`, `a` no longer holds its original value. So `b = a` copies the new `a` (which already equals `b`) back to `b` — effectively a no-op. The swap fails silently.

</details>

---

## Exercise 9: Custom Enum Type with String() [⭐ Challenge] [5 pts]

### Context
Go has no built-in `enum` keyword. Instead, the idiomatic pattern is to define a named integer type and use `iota` for its values. When combined with the `fmt.Stringer` interface (a type with a `String() string` method), the enum becomes human-readable automatically. This exercise previews interfaces but is grounded in the types-and-variables concepts from this module.

### Task
Create a custom type `Weekday` based on `int`. Define `Sunday` through `Saturday` as constants of that type using `iota`. Implement a `String() string` method on `Weekday` that returns the human-readable name. Use a `switch` statement inside `String()`. In `main`, create a few `Weekday` values and print them — they should print as names, not numbers.

### Requirements
- [ ] Define `type Weekday int`
- [ ] Define constants `Sunday` through `Saturday` of type `Weekday` using `iota`
- [ ] Implement `func (d Weekday) String() string` using a switch statement
- [ ] Return `"Unknown"` from the default case
- [ ] In `main`, print at least three `Weekday` values using `fmt.Println` — they should print as day names
- [ ] Demonstrate that the `Weekday` type prevents accidental misuse: show that `var d Weekday = 8` compiles but that this value triggers the `"Unknown"` case in `String()`

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

A method with signature `func (d Weekday) String() string` satisfies the `fmt.Stringer` interface. When `fmt.Println` receives a value that implements `Stringer`, it calls `String()` automatically instead of printing the raw integer.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

```go
type Weekday int

const (
    Sunday Weekday = iota
    Monday
    // ...
)
```
Notice `Sunday Weekday = iota` — not just `Sunday = iota`. This gives the constants the type `Weekday`, not just `int`.

</details>

<details>
<summary>Hint 3 (near-solution hint)</summary>

```go
func (d Weekday) String() string {
    switch d {
    case Sunday:
        return "Sunday"
    case Monday:
        return "Monday"
    // ... add remaining days
    default:
        return "Unknown"
    }
}
```

</details>

### Expected Output / Acceptance Criteria
```
Sunday
Wednesday
Saturday
Unknown
```
_(The values print as day names, not numbers, because `fmt.Println` calls `String()` automatically.)_

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Weekday is a named type based on int.
// This gives the type its own identity — Weekday and int are distinct types,
// even though Weekday's underlying type is int.
type Weekday int

const (
    Sunday Weekday = iota // 0
    Monday                // 1
    Tuesday               // 2
    Wednesday             // 3
    Thursday              // 4
    Friday                // 5
    Saturday              // 6
)

// String implements the fmt.Stringer interface.
// When fmt.Println (or any fmt function) encounters a Weekday value,
// it calls String() automatically to get the human-readable representation.
func (d Weekday) String() string {
    switch d {
    case Sunday:
        return "Sunday"
    case Monday:
        return "Monday"
    case Tuesday:
        return "Tuesday"
    case Wednesday:
        return "Wednesday"
    case Thursday:
        return "Thursday"
    case Friday:
        return "Friday"
    case Saturday:
        return "Saturday"
    default:
        return "Unknown"
    }
}

func main() {
    day := Sunday
    fmt.Println(day)       // Sunday (not 0)
    fmt.Println(Wednesday) // Wednesday (not 3)
    fmt.Println(Saturday)  // Saturday (not 6)

    // Out-of-range value
    var invalid Weekday = 8
    fmt.Println(invalid) // Unknown
}
```

**Explanation:**
This exercise combines four concepts: named types (`type Weekday int`), typed iota constants, methods, and the `fmt.Stringer` interface. The critical point is that `type Weekday int` creates a *new type* — `Weekday` and `int` are not interchangeable without explicit conversion. This means `var d Weekday = 3` (Wednesday) and `var n int = 3` are different types even though they hold the same underlying value. The `String()` method is discovered by `fmt.Println` at runtime through Go's interface system: if a value has a `String() string` method, it is used for display. The `default` case in the switch handles invalid values gracefully — in a real program you might log an error or panic depending on context.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Zero Value Survey | — | —/1 | — | — |
| Exercise 2 — Type Inference Inspector | — | —/1 | — | — |
| Exercise 3 — Days of the Week | — | —/1 | — | — |
| Exercise 4 — Temperature Converter | — | —/2 | — | — |
| Exercise 5 — Permission Flags | — | —/2 | — | — |
| Exercise 6 — Type Conversion Roundtrip | — | —/2 | — | — |
| Exercise 7 — Integer Overflow | — | —/3 | — | — |
| Exercise 8 — Swap Without Temp | — | —/3 | — | — |
| Exercise 9 — Custom Enum | — | —/5 | — | — |
| **Total** | | **—/20** | | |

**Passing threshold:** 13/20 (65%). Aim for 17/20 (85%) before taking the test.
