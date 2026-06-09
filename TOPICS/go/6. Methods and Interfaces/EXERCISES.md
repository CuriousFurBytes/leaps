# Exercises — Module 6: Methods and Interfaces

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

## Exercise 1: Implementing fmt.Stringer [🟢 Easy] [1 pt]

### Context
`fmt.Stringer` is the most commonly implemented interface in Go. Any type that has a `String() string` method will have that method called automatically by `fmt.Println`, `fmt.Printf("%v", ...)`, and `fmt.Sprintf`. Implementing it makes your types first-class citizens in any code that uses `fmt`.

### Task
Define a named type `Temperature` as a `float64`. Implement `fmt.Stringer` on it so that it prints in the format `"23.5°C"` (one decimal place, degree symbol, C). Call `fmt.Println` with at least three Temperature values to confirm the output uses your `String()` method.

### Requirements
- [ ] `Temperature` is a named type based on `float64`, not a struct
- [ ] The `String()` method uses a value receiver (not pointer)
- [ ] `fmt.Println` output matches the `"23.5°C"` format exactly (one decimal, `°C`)
- [ ] The program compiles and runs without errors

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The `fmt.Stringer` interface is:
```go
type Stringer interface {
    String() string
}
```
Your `String()` method must have exactly this signature. Use `fmt.Sprintf("%.1f°C", float64(t))` to format the value — cast to `float64` first to avoid an infinite recursion (calling `fmt.Sprintf` on a `Temperature` would call `String()` again).

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The degree symbol `°` is a Unicode character (U+00B0). You can include it directly in a string literal: `"%.1f°C"`. Alternatively, use the Unicode escape `"°"`. Both work in Go string literals.

</details>

### Expected Output / Acceptance Criteria
```
0.0°C
100.0°C
-40.0°C
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

// Temperature represents a temperature in Celsius
type Temperature float64

// String satisfies fmt.Stringer — called automatically by fmt verbs
func (t Temperature) String() string {
    return fmt.Sprintf("%.1f°C", float64(t))
    // Cast to float64 to avoid infinite recursion:
    // if we passed t directly, fmt.Sprintf would call t.String() again
}

func main() {
    fmt.Println(Temperature(0))    // 0.0°C
    fmt.Println(Temperature(100))  // 100.0°C
    fmt.Println(Temperature(-40))  // -40.0°C

    // Also works in other fmt contexts:
    t := Temperature(23.5)
    fmt.Printf("Current temperature: %v\n", t)  // Current temperature: 23.5°C
    fmt.Printf("Current temperature: %s\n", t)  // Current temperature: 23.5°C
}
```

**Explanation:**
`Temperature` is a named type based on `float64`, so it can have methods. The `String() string` method satisfies `fmt.Stringer` implicitly — `fmt` checks at runtime whether a value has a `String()` method and calls it when formatting with `%v`, `%s`, or `fmt.Println`. The cast `float64(t)` is necessary to break the recursion: without it, `fmt.Sprintf("%.1f°C", t)` would call `t.String()` again because `t` is a `Temperature`, which has a `String()` method.

**Common wrong answers:**
- Using a pointer receiver `func (t *Temperature) String()` — this works but the value type `Temperature` would no longer satisfy `Stringer` directly; you'd need `&t` to call it. For a scalar type, value receivers are idiomatic.
- Passing `t` directly to `fmt.Sprintf` without the `float64(t)` cast — this compiles but causes infinite recursion at runtime.

</details>

---

## Exercise 2: Pointer Receiver and Interface Satisfaction [🟢 Easy] [1 pt]

### Context
The method set of `T` and `*T` differ: `T` only includes value-receiver methods, while `*T` includes both. This affects interface satisfaction. This exercise isolates that rule so you can see it clearly.

### Task
Define a `Counter` struct with a single `int` field `n`. Add two methods:
- `Value() int` with a value receiver — returns the current count
- `Increment()` with a **pointer receiver** — increments the count by 1

Define an interface `Incrementer` with both methods. Demonstrate:
1. That `*Counter` satisfies `Incrementer` (assign `&Counter{}` to an `Incrementer` variable)
2. That `Counter` (a value) does NOT satisfy `Incrementer` (show the compile-time error in a comment)
3. That calling `Increment()` through the `Incrementer` interface correctly modifies the original

### Requirements
- [ ] `Value()` has a value receiver; `Increment()` has a pointer receiver
- [ ] Assignment `var inc Incrementer = &Counter{}` compiles
- [ ] A comment shows what `var inc Incrementer = Counter{}` would produce (the error message)
- [ ] After calling `inc.Increment()` three times, `inc.Value()` returns 3

### Hints
<details>
<summary>Hint 1</summary>

The compile error for `var inc Incrementer = Counter{}` will be something like:
`cannot use Counter{} (type Counter) as type Incrementer: Counter does not implement Incrementer (Increment method has pointer receiver)`

You don't have to trigger this error — just include it as a comment.

</details>

### Expected Output / Acceptance Criteria
```
after 3 increments: 3
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type Counter struct{ n int }

// Value receiver: Counter satisfies this method in its method set
func (c Counter) Value() int { return c.n }

// Pointer receiver: only *Counter satisfies this method
func (c *Counter) Increment() { c.n++ }

// Incrementer requires both Value and Increment
type Incrementer interface {
    Value() int
    Increment()
}

func main() {
    // *Counter implements Incrementer — has both Value() and Increment()
    var inc Incrementer = &Counter{}

    // Counter (value) does NOT implement Incrementer:
    // var inc2 Incrementer = Counter{}
    // compile error: Counter does not implement Incrementer
    //               (Increment method has pointer receiver)

    inc.Increment()
    inc.Increment()
    inc.Increment()

    fmt.Printf("after 3 increments: %d\n", inc.Value()) // 3
}
```

**Explanation:**
`Counter` (a value type) only has `Value()` in its method set because `Increment()` uses a pointer receiver. `*Counter` has both `Value()` (from the value receiver, promoted to `*Counter`) and `Increment()`. The interface variable `inc` holds a `*Counter`, so mutations via `inc.Increment()` affect the underlying `Counter` through the pointer.

</details>

---

## Exercise 3: Interface Composition with io Interfaces [🟡 Medium] [2 pts]

### Context
Go's `io` package achieves enormous flexibility through small, composable interfaces. `io.Reader`, `io.Writer`, and `io.ReadWriter` (their composition) are used everywhere. This exercise builds a function that accepts the most general interface it needs — demonstrating why small interfaces and composition are powerful.

### Task
Write a function `copyAndCount(dst io.Writer, src io.Reader) (int64, error)` that copies all bytes from `src` to `dst` using `io.Copy`, and returns the number of bytes copied and any error. Then write a `main` that:
1. Copies from a `strings.NewReader("Hello, interfaces!")` to a `bytes.Buffer`
2. Prints the number of bytes copied and the buffer's contents

Neither `strings.Reader` nor `bytes.Buffer` appears in the function signature — only the interfaces do.

### Requirements
- [ ] Function signature is exactly `func copyAndCount(dst io.Writer, src io.Reader) (int64, error)`
- [ ] Uses `io.Copy` internally (do not write your own byte loop)
- [ ] `main` calls the function and prints both the byte count and the copied content
- [ ] Imports: `"bytes"`, `"fmt"`, `"io"`, `"strings"`

### Hints
<details>
<summary>Hint 1</summary>

`io.Copy(dst, src)` returns `(int64, error)` — it copies from `src` to `dst` and returns the total bytes written. Your function can simply return `io.Copy(dst, src)`.

</details>

<details>
<summary>Hint 2</summary>

`strings.NewReader(s)` returns a `*strings.Reader` which implements `io.Reader`. `bytes.Buffer` (use `var buf bytes.Buffer` or `new(bytes.Buffer)`) implements `io.Writer`. Both can be passed directly to your function because they satisfy the interfaces.

</details>

### Expected Output / Acceptance Criteria
```
copied 18 bytes
content: Hello, interfaces!
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "bytes"
    "fmt"
    "io"
    "strings"
)

// copyAndCount accepts the minimal interfaces it needs — not *os.File or bytes.Buffer
func copyAndCount(dst io.Writer, src io.Reader) (int64, error) {
    return io.Copy(dst, src)
}

func main() {
    src := strings.NewReader("Hello, interfaces!")  // *strings.Reader implements io.Reader
    var dst bytes.Buffer                             // bytes.Buffer implements io.Writer

    n, err := copyAndCount(&dst, src)
    if err != nil {
        fmt.Println("error:", err)
        return
    }

    fmt.Printf("copied %d bytes\n", n)
    fmt.Printf("content: %s\n", dst.String())
}
```

**Explanation:**
`copyAndCount` takes `io.Writer` and `io.Reader` — it does not know or care whether those are files, buffers, network connections, or in-memory strings. In `main`, `strings.NewReader` returns `*strings.Reader` which has a `Read` method matching `io.Reader`; `bytes.Buffer` has a `Write` method matching `io.Writer`. Both satisfy their respective interfaces implicitly. Note: `&dst` is used because `bytes.Buffer`'s `Write` method has a pointer receiver — the `*bytes.Buffer` type satisfies `io.Writer`, not the value type.

</details>

---

## Exercise 4: Type Switch on Interface Values [🟡 Medium] [2 pts]

### Context
A type switch lets you dispatch on the concrete type inside an interface value. This is essential for functions that accept `any` (or a broad interface) and need to behave differently based on the actual type. This exercise practices the full type switch syntax including an interface type case.

### Task
Write a function `formatValue(v any) string` that returns a formatted string based on the concrete type of `v`:
- `nil` → `"<nil>"`
- `int` → `"int: <value>"`
- `float64` → `"float64: <value>"`  (use `%g` format)
- `string` → `"string: <value>"` (use `%q` format)
- `bool` → `"bool: <value>"`
- `fmt.Stringer` → `"Stringer: <value.String()>"` (any type that implements Stringer)
- anything else → `"other: <Go type name>"`

Call `formatValue` with at least 7 different values (one per case, including a type that satisfies `fmt.Stringer`) and print the results.

### Requirements
- [ ] Uses a type switch `switch t := v.(type) { ... }`
- [ ] The `fmt.Stringer` case is an interface type case (not a concrete type)
- [ ] All 7 case types are covered
- [ ] A custom type implementing `fmt.Stringer` is used to exercise that case

### Hints
<details>
<summary>Hint 1</summary>

In a type switch, a case can be an interface type: `case fmt.Stringer:`. Within that case, `t` will be typed as `fmt.Stringer`. Order matters: the `fmt.Stringer` case must come after the concrete type cases (int, string, etc.) that also happen to satisfy Stringer — or those concrete types will match the Stringer case first. Put the specific concrete types before the interface case.

</details>

<details>
<summary>Hint 2</summary>

For a custom type that satisfies `fmt.Stringer`, you can reuse the `Temperature` type from Exercise 1, or define a new simple type with a `String() string` method.

</details>

### Expected Output / Acceptance Criteria
```
<nil>
int: 42
float64: 3.14
string: "hello"
bool: true
Stringer: 100.0°C
other: []int
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Reuse Temperature from Exercise 1
type Temperature float64

func (t Temperature) String() string {
    return fmt.Sprintf("%.1f°C", float64(t))
}

func formatValue(v any) string {
    switch t := v.(type) {
    case nil:
        return "<nil>"
    case int:
        return fmt.Sprintf("int: %d", t)       // t is typed int here
    case float64:
        return fmt.Sprintf("float64: %g", t)   // t is typed float64 here
    case string:
        return fmt.Sprintf("string: %q", t)    // t is typed string here
    case bool:
        return fmt.Sprintf("bool: %v", t)
    case fmt.Stringer:
        return fmt.Sprintf("Stringer: %s", t.String()) // t is typed fmt.Stringer here
    default:
        return fmt.Sprintf("other: %T", t)     // %T prints the Go type name
    }
}

func main() {
    values := []any{
        nil,
        42,
        3.14,
        "hello",
        true,
        Temperature(100),
        []int{1, 2, 3},
    }
    for _, v := range values {
        fmt.Println(formatValue(v))
    }
}
```

**Explanation:**
The type switch evaluates `v`'s dynamic type against each case in order. Concrete type cases (`int`, `float64`, etc.) must come before the `fmt.Stringer` interface case — if `fmt.Stringer` came first, and `Temperature` also happened to match an earlier concrete case, the concrete case would win anyway. Placing `fmt.Stringer` after the specific concrete types means it catches any remaining types that implement `String() string`, including `Temperature`. In the `default` case, `%T` formats the underlying Go type name (e.g., `[]int`).

</details>

---

## Exercise 5: Sorting a Custom Type with sort.Interface [🟡 Medium] [2 pts]

### Context
`sort.Interface` is the canonical example of a three-method interface that makes any collection sortable. Before `sort.Slice` existed (Go 1.8), this was the only way to sort custom types. Understanding it deeply illustrates how interface-based extensibility works: the `sort` package knows nothing about your type, yet it can sort it.

### Task
Define a `Product` struct with fields `Name string` and `Price float64`. Create a named type `ByPrice` as `[]Product`. Implement `sort.Interface` on `ByPrice` (Len, Less, Swap). In `main`, create a slice of at least 5 products, sort it by price ascending, and print the results. Then sort the same slice by price descending using `sort.Reverse` and print again.

### Requirements
- [ ] `ByPrice` implements all three methods: `Len`, `Less`, `Swap`
- [ ] Products are sorted ascending by price first, descending second
- [ ] `sort.Reverse(ByPrice(products))` is used for the descending sort — do not re-implement Less
- [ ] Output clearly labels which sort is which

### Hints
<details>
<summary>Hint 1</summary>

`sort.Reverse(data sort.Interface)` returns a `sort.Interface` that sorts in reverse order — it wraps your `ByPrice` and inverts the `Less` method. Usage: `sort.Sort(sort.Reverse(ByPrice(products)))`. You do not need a separate `ByPriceDesc` type.

</details>

<details>
<summary>Hint 2</summary>

`Len` returns `len(b)`, `Swap` does `b[i], b[j] = b[j], b[i]`, `Less` returns `b[i].Price < b[j].Price`. These are the standard implementations.

</details>

### Expected Output / Acceptance Criteria
```
--- Ascending by price ---
Pen       $1.99
Notebook  $4.99
Stapler   $8.50
Backpack  $29.99
Laptop    $999.00

--- Descending by price ---
Laptop    $999.00
Backpack  $29.99
Stapler   $8.50
Notebook  $4.99
Pen       $1.99
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "sort"
)

type Product struct {
    Name  string
    Price float64
}

// ByPrice implements sort.Interface for []Product sorted by Price
type ByPrice []Product

func (p ByPrice) Len() int           { return len(p) }
func (p ByPrice) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p ByPrice) Less(i, j int) bool { return p[i].Price < p[j].Price }

func main() {
    products := []Product{
        {"Laptop", 999.00},
        {"Pen", 1.99},
        {"Backpack", 29.99},
        {"Notebook", 4.99},
        {"Stapler", 8.50},
    }

    sort.Sort(ByPrice(products))
    fmt.Println("--- Ascending by price ---")
    for _, p := range products {
        fmt.Printf("%-10s $%.2f\n", p.Name, p.Price)
    }

    sort.Sort(sort.Reverse(ByPrice(products)))
    fmt.Println("\n--- Descending by price ---")
    for _, p := range products {
        fmt.Printf("%-10s $%.2f\n", p.Name, p.Price)
    }
}
```

**Explanation:**
`sort.Sort` accepts `sort.Interface`; `ByPrice` satisfies it with three methods. `sort.Reverse` is itself a wrapper that implements `sort.Interface` by inverting `Less` — it uses the method set of the wrapped type, which demonstrates interface composition in action. Note that `ByPrice(products)` is a type conversion (from `[]Product` to `ByPrice`), not a function call. Both types have the same underlying memory; the conversion just changes which method set is attached.

</details>

---

## Exercise 6: Designing a Domain Interface [🔴 Hard] [3 pts]

### Context
Good Go interface design means defining the interface at the consumer, keeping it small, and letting multiple unrelated types satisfy it implicitly. This exercise gives you practice designing an interface from scratch and satisfying it with two independent types.

### Task
Design a small notification system:

1. Define an interface `Notifier` with a single method `Notify(message string) error`
2. Implement `EmailNotifier` (a struct with `ToAddress string`) whose `Notify` method prints `"[EMAIL to <addr>]: <message>"` and returns nil
3. Implement `SlackNotifier` (a struct with `Channel string`) whose `Notify` method prints `"[SLACK #<channel>]: <message>"` and returns nil
4. Write a function `notifyAll(notifiers []Notifier, message string) []error` that calls `Notify` on each notifier, collects non-nil errors into a slice, and returns it
5. In `main`, create a mixed slice of `EmailNotifier` and `SlackNotifier`, call `notifyAll`, and print any errors (there should be none)

### Requirements
- [ ] `Notifier` interface defined in the same file/package as the function that uses it (consumer-side)
- [ ] Both types satisfy `Notifier` implicitly — no `implements` keyword
- [ ] `notifyAll` accepts `[]Notifier`, not `[]EmailNotifier` or `[]SlackNotifier`
- [ ] `notifyAll` collects errors and returns them — does not abort on first error
- [ ] The output shows both email and Slack notifications interleaved

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

Since `Notify` returns `nil` (no error) in both implementations, `notifyAll` will return an empty slice. To make the function more robust, collect non-nil errors: `if err := n.Notify(message); err != nil { errs = append(errs, err) }`.

</details>

<details>
<summary>Hint 2 (the interface assignment)</summary>

To create a `[]Notifier` with mixed types, you cannot use a typed slice literal directly. Either declare the slice as `[]Notifier` and append elements, or use a composite literal: `[]Notifier{EmailNotifier{...}, &SlackNotifier{...}}`. If your Notify method uses a pointer receiver, you'll need `&SlackNotifier{...}`.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
notifiers := []Notifier{
    EmailNotifier{ToAddress: "alice@example.com"},
    EmailNotifier{ToAddress: "bob@example.com"},
    SlackNotifier{Channel: "alerts"},
}
errs := notifyAll(notifiers, "system maintenance at midnight")
```

</details>

### Expected Output / Acceptance Criteria
```
[EMAIL to alice@example.com]: system maintenance at midnight
[EMAIL to bob@example.com]: system maintenance at midnight
[SLACK #alerts]: system maintenance at midnight
errors: 0
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Notifier is defined at the consumer — the notification service.
// EmailNotifier and SlackNotifier don't need to know about this interface.
type Notifier interface {
    Notify(message string) error
}

// EmailNotifier sends notifications via email (simulated here as a print)
type EmailNotifier struct {
    ToAddress string
}

func (e EmailNotifier) Notify(message string) error {
    fmt.Printf("[EMAIL to %s]: %s\n", e.ToAddress, message)
    return nil
}

// SlackNotifier sends notifications to a Slack channel (simulated)
type SlackNotifier struct {
    Channel string
}

func (s SlackNotifier) Notify(message string) error {
    fmt.Printf("[SLACK #%s]: %s\n", s.Channel, message)
    return nil
}

// notifyAll sends message to all notifiers, collecting errors
func notifyAll(notifiers []Notifier, message string) []error {
    var errs []error
    for _, n := range notifiers {
        if err := n.Notify(message); err != nil {
            errs = append(errs, err)
        }
    }
    return errs
}

func main() {
    notifiers := []Notifier{
        EmailNotifier{ToAddress: "alice@example.com"},
        EmailNotifier{ToAddress: "bob@example.com"},
        SlackNotifier{Channel: "alerts"},
    }

    errs := notifyAll(notifiers, "system maintenance at midnight")
    fmt.Printf("errors: %d\n", len(errs))
}
```

**Explanation:**
`Notifier` is defined in the package that uses it (`main` here), not in the packages that provide the implementations. Both `EmailNotifier` and `SlackNotifier` satisfy `Notifier` implicitly — they don't import or reference the `Notifier` type at all. `notifyAll` takes `[]Notifier`, making it work with any type that has `Notify(string) error`. This design means you can add a `SMSNotifier`, `PagerDutyNotifier`, etc. without modifying `notifyAll` or the interface — the extension happens by adding a new type.

</details>

---

## Exercise 7: The Typed-Nil Bug Hunt [🔴 Hard] [3 pts]

### Context
The typed-nil interface bug is subtle and common. This exercise presents buggy code and asks you to find and fix it, explain why it happens at the interface value level, and write a test that would catch it.

### Task
The following function is broken. Find the bug, fix it, explain why the original was wrong at the `(type, value)` pair level, and write a test (using `if err != nil`) that demonstrates the fix works:

```go
type AppError struct {
    Code    int
    Message string
}

func (e *AppError) Error() string {
    return fmt.Sprintf("error %d: %s", e.Code, e.Message)
}

// validate returns an error if n is negative; nil otherwise.
func validate(n int) error {
    var err *AppError
    if n < 0 {
        err = &AppError{Code: 400, Message: "negative value not allowed"}
    }
    return err  // BUG IS HERE
}
```

### Requirements
- [ ] Correctly identify the line with the bug and explain why it is a bug
- [ ] Provide a corrected version of `validate`
- [ ] Explain the `(type, value)` pair state of the return value when `n >= 0`  in the buggy version
- [ ] Write a `main` that calls `validate(5)` and `validate(-1)` and shows that the fixed version returns `nil` for `n=5` and non-nil for `n=-1`

### Hints
<details>
<summary>Hint 1 (what to look for)</summary>

The bug is on the `return err` line. When `n >= 0`, `err` is a `*AppError` variable holding a nil pointer. When you return `err` (a typed nil) as an `error` interface, what are the type and value fields of the resulting interface?

</details>

<details>
<summary>Hint 2 (the fix)</summary>

The fix requires changing the return path when there is no error. Instead of declaring `var err *AppError` and returning it unconditionally, return `nil` (the untyped nil) directly when there is no error:
```go
func validate(n int) error {
    if n < 0 {
        return &AppError{Code: 400, Message: "negative value not allowed"}
    }
    return nil  // untyped nil — interface has no type
}
```

</details>

### Expected Output / Acceptance Criteria
```
validate(5):  err == nil? true   (correct)
validate(-1): err == nil? false  (correct, error: error 400: negative value not allowed)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type AppError struct {
    Code    int
    Message string
}

func (e *AppError) Error() string {
    return fmt.Sprintf("error %d: %s", e.Code, e.Message)
}

// BUGGY version — left here for comparison
func validateBuggy(n int) error {
    var err *AppError        // typed nil: *AppError, value == nil
    if n < 0 {
        err = &AppError{Code: 400, Message: "negative value not allowed"}
    }
    return err
    // When n >= 0: returns interface{type=*AppError, value=nil}
    // This interface is NOT nil — the type field is set.
    // caller's "if err != nil" is ALWAYS true.
}

// CORRECT version — return untyped nil directly
func validate(n int) error {
    if n < 0 {
        return &AppError{Code: 400, Message: "negative value not allowed"}
    }
    return nil // interface{type=nil, value=nil} — truly nil
}

func main() {
    // Demonstrate the bug:
    err := validateBuggy(5)
    fmt.Printf("buggy validate(5):  err == nil? %v  (BUG: should be true)\n", err == nil)

    // Demonstrate the fix:
    err = validate(5)
    fmt.Printf("validate(5):  err == nil? %v   (correct)\n", err == nil)

    err = validate(-1)
    fmt.Printf("validate(-1): err == nil? %v  (correct, error: %v)\n", err == nil, err)
}
```

**Why the bug occurs at the `(type, value)` level:**
An `error` interface value stores two words: a type pointer and a value pointer. When `validateBuggy` returns `err` (a `*AppError` nil pointer), the interface is populated as: type=`*AppError` (non-nil type descriptor), value=`nil`. The interface is NOT nil because the type field is non-zero. The `if err != nil` check tests whether the interface itself is nil (both fields zero), not whether the stored pointer is nil. Only returning the untyped `nil` literal produces an interface where both fields are zero.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — fmt.Stringer | — | —/1 | — | — |
| Exercise 2 — Pointer Receiver & Interface | — | —/1 | — | — |
| Exercise 3 — io Interface Composition | — | —/2 | — | — |
| Exercise 4 — Type Switch | — | —/2 | — | — |
| Exercise 5 — sort.Interface | — | —/2 | — | — |
| Exercise 6 — Domain Interface Design | — | —/3 | — | — |
| Exercise 7 — Typed-Nil Bug Hunt | — | —/3 | — | — |
| **Total** | | **—/14** | | |

**Passing threshold:** 9/14 (65%). Aim for 12/14 (85%) before taking the test.
