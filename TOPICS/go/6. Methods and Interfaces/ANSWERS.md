# Answer Key — Module 6: Methods and Interfaces

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

### 1.1 — Method vs function [1 pt]

**Full credit answer:**
A method is a function with a named receiver parameter declared between `func` and the method name. A regular function has no receiver. They are otherwise equivalent — a method can always be called as a function with the receiver as the first argument.

```go
// Function
func areaFunc(r Rectangle) float64 { return r.Width * r.Height }

// Method — r is the receiver
func (r Rectangle) Area() float64 { return r.Width * r.Height }
```

**Key points required:**
- Method has a receiver; function does not
- They are otherwise semantically equivalent

**Common wrong answers:**
- *"Methods are inside classes"* — Go has no classes. Methods are defined outside the type declaration, just like functions.

---

### 1.2 — Method set table [1 pt]

**Full credit answer:**

| Type | Methods in its method set |
|------|--------------------------|
| `T` | All methods with value receiver `(t T)` only |
| `*T` | All methods with value receiver `(t T)` **plus** all methods with pointer receiver `(t *T)` |

**Key points required:**
- `T` only gets value-receiver methods
- `*T` gets both — this is the critical asymmetry

---

### 1.3 — Implicit interface satisfaction [1 pt]

**Full credit answer:**
No, Go does not require explicit `implements` declarations. A type satisfies an interface automatically — implicitly — if it has all the methods the interface requires, with matching signatures. The compiler checks this structural compatibility at the point where a value is assigned to or used as an interface type.

**Key points required:**
- No `implements` keyword
- Satisfaction is structural / implicit
- Checked at compile time

---

### 1.4 — The any type [1 pt]

**Full credit answer:**
`any` is a built-in alias for `interface{}` (the empty interface), introduced in Go 1.18. It has no methods, so every type satisfies it. `any` is preferred over `interface{}` in new code for readability. They are completely interchangeable — there is no semantic difference.

**Key points required:**
- Alias for `interface{}`
- Introduced in Go 1.18
- Every type satisfies it

---

### 1.5 — Three standard interfaces [1 pt]

**Full credit answer (any three of these):**

| Interface | Package | Methods | Description |
|-----------|---------|---------|-------------|
| `error` | built-in | 1: `Error() string` | The standard error interface |
| `fmt.Stringer` | `fmt` | 1: `String() string` | Custom string representation |
| `io.Reader` | `io` | 1: `Read(p []byte) (n int, err error)` | Read bytes |
| `io.Writer` | `io` | 1: `Write(p []byte) (n int, err error)` | Write bytes |
| `sort.Interface` | `sort` | 3: `Len`, `Less`, `Swap` | Sortable collection |

**Key points required:** Name three interfaces with their method counts. Partial credit if the description is right but method count is off.

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Method set asymmetry [2 pts]

**Full credit answer:**
`*T` can call value-receiver methods because the compiler can dereference the pointer to obtain the value — this is always safe and unambiguous. The reverse is not always possible: when a value of type `T` is stored inside an interface, it may have been copied — the interface holds a copy of the value, not the original. Taking the address of that copy and calling a pointer-receiver method through it would mean "mutating a copy," which is silently wrong. Go's specification prevents this ambiguity by simply not including pointer-receiver methods in the method set of `T`.

The rule is asymmetric by design: you can always go from "have pointer, need value" (dereference), but you cannot always go from "have value stored in interface, need pointer" (the value may not be addressable).

**Rubric:**
- 2 pts: Explains both directions and gives the underlying reason (the value in an interface may be a copy; dereferencing a pointer is always safe)
- 1 pt: Correct result stated but without the underlying reason (just "that's the rule")
- 0 pts: States the rule backwards, or fundamentally incorrect

---

### 2.2 — Interface value internal representation [2 pts]

**Full credit answer:**
An interface value is a two-word pair: `(dynamic type, dynamic value)`.

- **Dynamic type**: a pointer to the runtime type descriptor for the concrete type currently stored
- **Dynamic value**: a pointer to the concrete value (or the value itself for small types)

For the three cases:
- **(a) nil interface**: both fields are zero — type is nil, value is nil. `i == nil` is `true`.
- **(b) `os.Stdout` (`*os.File`)**: type = pointer to `*os.File`'s runtime descriptor; value = the actual `*os.File` pointer (pointing to the file struct). The interface is non-nil.
- **(c) Typed nil `(*os.File)(nil)`**: type = pointer to `*os.File`'s runtime descriptor (non-nil); value = nil pointer. **The interface is NOT nil** because the type field is set. This is the typed-nil gotcha: `i == nil` is `false` even though the stored pointer is nil.

**Rubric:**
- 2 pts: Correctly describes both fields AND correctly characterizes all three cases (especially distinguishing b from c)
- 1 pt: Correctly describes the two-field model but misses or incorrectly explains the typed-nil case (c)
- 0 pts: Describes interface as a single pointer, or fundamentally incorrect

---

### 2.3 — Accept interfaces, return structs [2 pts]

**Full credit answer:**
"Accept interfaces, return structs" is a Go design principle with two independent justifications:

**Accepting interfaces:** When a function parameter is an interface, callers can pass any conforming implementation. This enables testing (pass a fake/mock), extension (add a new type later), and decoupling (the function doesn't depend on a specific package). If you accept `*os.File`, you've locked the function to file I/O only; if you accept `io.Writer`, you can pass a file, a buffer, a network connection, or a test spy.

**Returning structs:** When a function returns a concrete struct, callers receive the full, richly-typed value with all its methods available. Returning an interface gives callers only the interface's methods — it hides information and forces type assertions to get it back. Returning a concrete struct is also more stable: you can add new methods to the struct without breaking callers who hold the interface type (adding methods to an interface is a breaking change for all existing implementors).

**Rubric:**
- 2 pts: Explains both directions with distinct justifications; "accept" justification focuses on flexibility/testability, "return" justification focuses on information availability or API stability
- 1 pt: Explains one direction correctly but not the other, or treats them as the same reason
- 0 pts: Gets one or both directions backwards

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Shape interface [3 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "math"
)

type Shape interface {
    Area() float64
    Name() string
}

type Circle struct{ Radius float64 }

func (c Circle) Area() float64  { return math.Pi * c.Radius * c.Radius }
func (c Circle) Name() string   { return "Circle" }

type Square struct{ Side float64 }

func (s Square) Area() float64  { return s.Side * s.Side }
func (s Square) Name() string   { return "Square" }

func largestShape(shapes []Shape) Shape {
    if len(shapes) == 0 {
        return nil
    }
    largest := shapes[0]
    for _, s := range shapes[1:] {
        if s.Area() > largest.Area() {
            largest = s
        }
    }
    return largest
}

func main() {
    shapes := []Shape{
        Circle{Radius: 3},
        Square{Side: 5},
        Circle{Radius: 7},
        Square{Side: 4},
    }
    lg := largestShape(shapes)
    fmt.Printf("Largest: %s with area %.2f\n", lg.Name(), lg.Area())
}
```

**Expected output:**
```
Largest: Circle with area 153.94
```

**Rubric:**
- 3 pts: Interface defined; two types implemented correctly; `largestShape` iterates correctly; `main` uses it correctly; compiles and runs
- 2 pts: Interface and types correct, but `largestShape` has a bug (e.g., off-by-one, returns wrong element), or misses nil/empty slice handling
- 1 pt: Interface and one type correct, or has the right structure but compile error
- 0 pts: Fundamental misunderstanding of interface definition or satisfaction

---

### 3.2 — mustRead and tryRead [3 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "io"
    "strings"
)

// mustRead reads exactly n bytes from r; panics on any error or insufficient bytes
func mustRead(r io.Reader, n int) []byte {
    buf := make([]byte, n)
    total := 0
    for total < n {
        nn, err := r.Read(buf[total:])
        total += nn
        if err == io.EOF && total < n {
            panic(fmt.Sprintf("mustRead: need %d bytes, got %d (EOF)", n, total))
        }
        if err != nil && err != io.EOF {
            panic(fmt.Sprintf("mustRead: read error: %v", err))
        }
    }
    return buf
}

// tryRead reads exactly n bytes from r; returns error instead of panicking
func tryRead(r io.Reader, n int) ([]byte, error) {
    buf := make([]byte, n)
    _, err := io.ReadFull(r, buf)
    if err != nil {
        return nil, fmt.Errorf("tryRead: %w", err)
    }
    return buf, nil
}

func main() {
    r := strings.NewReader("Hello, World!")
    data := mustRead(r, 5)
    fmt.Printf("mustRead: %q\n", data)  // "Hello"

    r2 := strings.NewReader("Hi")
    data2, err := tryRead(r2, 5)
    fmt.Printf("tryRead: data=%q err=%v\n", data2, err)
}
```

**Rubric:**
- 3 pts: `mustRead` panics on insufficient bytes or error; `tryRead` returns an error; both use `io.Reader` as parameter type; both compile correctly
- 2 pts: `mustRead` panics but `tryRead` is missing or wrong; or both functions are correct but use wrong parameter type (`*strings.Reader` instead of `io.Reader`)
- 1 pt: One function correct; the other missing or fundamentally wrong
- 0 pts: Does not use `io.Reader`, or panics are replaced with returns, misunderstanding the distinction

**Acceptable alternatives:**
Using `io.ReadFull(r, buf)` is a clean alternative for both functions — it handles partial reads internally.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Typed-nil bug [3 pts] (1 pt each part)

**(a) The exact bug:**
The bug is on the line `return dbErr`. When `id` is valid (e.g., `id = 42`), `dbErr` is a `*DBError` nil pointer (declared as `var dbErr *DBError` and never assigned). Returning `dbErr` (a typed nil concrete pointer) into the `error` interface return type creates a non-nil interface — the interface holds the type descriptor for `*DBError` but a nil value. The `if err != nil` check in the caller sees a non-nil interface and incorrectly treats it as an error.

Also note: the `Message` field in the `DBError` struct would need to be corrected from `Message` to `Msg` to compile — but the typed-nil bug is the primary issue.

**(b) The (type, value) internal state of `queryDB(42)`:**
The returned `error` interface value has: type = pointer to the runtime descriptor for `*DBError` (non-nil), value = nil (the nil pointer). The interface is NOT nil because the type field is set. `if err != nil` checks whether the interface pair is `(nil, nil)` — it is not, so the check evaluates to true (incorrectly).

**(c) Corrected version:**
```go
func queryDB(id int) error {
    if id <= 0 {
        return &DBError{Code: 404, Msg: "record not found"}
    }
    return nil  // untyped nil — both type and value fields are zero
}
```

**Rubric:**
- 1 pt for (a): Correctly identifies `return dbErr` as the bug and explains that a typed nil concrete pointer wrapped in an interface is not a nil interface
- 1 pt for (b): Correctly describes the `(type=*DBError, value=nil)` state and explains why `!= nil` is true
- 1 pt for (c): Provides a correct fix that returns `nil` directly instead of the typed nil variable

---

## Section 5: Discussion — Answer Key

### 5.1 — Define interfaces at the consumer [2 pts]

**Example strong answer:**
"Define interfaces at the consumer" means that the package which needs to call certain methods defines the interface, not the package that provides the concrete type. Example: a `storage` package ships `FileStore` with a `Save(key, value string) error` method. A `service` package defines `type Storer interface { Save(string, string) error }` and its `NewService` function accepts a `Storer`. The `storage` package never imports `service` — there is no coupling in that direction. `FileStore` satisfies `Storer` implicitly.

This is better than the alternative (producer defines the interface) because: (1) it eliminates import cycles — the provider package doesn't need to know about the consumer, (2) you can add a new provider without modifying any existing code — just create a new type with the right method, (3) you can define a smaller interface than the concrete type exposes, keeping the function's dependencies minimal.

In Java, writing `class FileStore implements Storer` couples `FileStore` to `Storer` at the definition site — `FileStore` must be updated if `Storer` is added later. In Go, the coupling happens at the call site only, and retroactively: a `FileStore` written years before `Storer` existed will satisfy `Storer` automatically if it has the right methods.

**Elements that earn full credit:**
- Explains which side defines the interface (consumer/caller, not producer/implementor)
- Gives a concrete two-package example
- States the benefit: no coupling in the provider; new implementations add without modifying existing code
- Addresses the contrast with explicit `implements`

**Rubric:**
- 2 pts: Explains the principle clearly with a concrete example AND addresses the coupling benefit AND contrasts with explicit `implements`
- 1 pt: Explains the principle or gives an example, but doesn't address the coupling or explicit-`implements` contrast
- 0 pts: Reverses the principle (says the producer defines the interface), or demonstrates fundamental confusion about interface definition

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Plugin system [+5 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "strings"
)

// Plugin defines the behavior every plugin must implement
type Plugin interface {
    Name() string
    Execute(input string) (string, error)
}

// UpperPlugin converts input to uppercase
type UpperPlugin struct{}

func (p UpperPlugin) Name() string { return "Upper" }
func (p UpperPlugin) Execute(input string) (string, error) {
    return strings.ToUpper(input), nil
}

// ReversePlugin reverses the input string
type ReversePlugin struct{}

func (p ReversePlugin) Name() string { return "Reverse" }
func (p ReversePlugin) Execute(input string) (string, error) {
    runes := []rune(input)
    for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
        runes[i], runes[j] = runes[j], runes[i]
    }
    return string(runes), nil
}

// Pipeline chains plugins: output of one becomes input of the next
type Pipeline struct {
    plugins []Plugin
}

func NewPipeline(plugins ...Plugin) *Pipeline {
    return &Pipeline{plugins: plugins}
}

// Name satisfies Plugin — Pipeline itself is a Plugin
func (p *Pipeline) Name() string {
    names := make([]string, len(p.plugins))
    for i, pl := range p.plugins {
        names[i] = pl.Name()
    }
    return strings.Join(names, "→")
}

// Execute passes input through each plugin in sequence
func (p *Pipeline) Execute(input string) (string, error) {
    current := input
    for _, pl := range p.plugins {
        var err error
        current, err = pl.Execute(current)
        if err != nil {
            return "", fmt.Errorf("plugin %s: %w", pl.Name(), err)
        }
    }
    return current, nil
}

// runPlugin accepts any Plugin — demonstrates Pipeline satisfies Plugin
func runPlugin(pl Plugin, input string) {
    result, err := pl.Execute(input)
    if err != nil {
        fmt.Printf("[%s] error: %v\n", pl.Name(), err)
        return
    }
    fmt.Printf("[%s] %q → %q\n", pl.Name(), input, result)
}

func main() {
    pipeline := NewPipeline(UpperPlugin{}, ReversePlugin{})

    // Run the pipeline directly
    result, _ := pipeline.Execute("hello world")
    fmt.Println("Pipeline result:", result)  // !DLROW OLLEH

    // Pass the Pipeline as a Plugin to runPlugin
    runPlugin(pipeline, "hello world")

    // Also run individual plugins
    runPlugin(UpperPlugin{}, "hello world")
    runPlugin(ReversePlugin{}, "hello world")
}
```

**Expected output:**
```
Pipeline result: !DLROW OLLEH
[Upper→Reverse] "hello world" → "!DLROW OLLEH"
[Upper] "hello world" → "HELLO WORLD"
[Reverse] "hello world" → "dlrow olleh"
```

**Rubric:**
- 5 pts: All five items implemented correctly; `Pipeline` satisfies `Plugin`; output correct; compiles and runs
- 3 pts: Plugin interface and two implementations correct; Pipeline executes in sequence; but Pipeline does not implement Plugin, or Name method is wrong
- 2 pts: Interface and one or two implementations correct; Pipeline structure started but execution or name method incomplete
- 1 pt: Interface defined and at least one implementation correct; significant gaps elsewhere
- 0 pts: Fundamental misunderstanding of interface definition or composition

**Teaching note:**
The bonus within the bonus — `Pipeline` implementing `Plugin` — demonstrates that a type can be both a consumer of an interface (holds a `[]Plugin`) and an implementor of it (satisfies `Plugin` itself). This recursive composability is a hallmark of well-designed Go interfaces.

---

## Common Wrong Answers Across the Test

These patterns appear frequently when the material hasn't been fully internalized:

1. **Confusing `T` and `*T` in interface satisfaction** — Students assign `T{}` to an interface variable when a pointer-receiver method is required, and are surprised by the "does not implement" error. The fix is always to use `&T{}`. Redirect to the method-set table in the README.
2. **Missing the typed-nil gotcha** — Students who understand interface values conceptually still fall into the typed-nil trap because they think "a nil pointer is nil." Stress that `if err != nil` tests the interface pair, not the stored pointer. Students who miss question 4.1 should re-read the "Nil Interface Gotcha" section and Example 4.
3. **Defining the interface on the wrong side** — Students from Java backgrounds instinctively put the interface in the "provider" package and have types implement it there. Question 5.1 tests this inversion. Redirect to the Interface Design Guidance section.
4. **Using concrete types in function parameters instead of interfaces** — Students write `func f(buf *bytes.Buffer)` instead of `func f(w io.Writer)`. The test question 3.2 tests this directly; question 5.1 tests the reasoning behind it.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 Q2.2 (the interface value internals) need to work through Example 4 (typed-nil bug) in the README again. The abstract model only clicks after seeing a concrete symptom.
- Students who struggle with Section 3 often have trouble with the method-set rules. Send back to the "Value vs Pointer Receivers and Method Sets" section, specifically the table and the `*T` explanation.
- The bonus question (6.1) exercises a sophisticated pattern — `Pipeline` implementing the same `Plugin` interface it uses. Students who complete this correctly are ready for Module 7 and understand Go's composability model well.
- A score below 60% generally indicates that [[go/5. Pointers]] was not solid. Ask the student whether they can explain pointer vs value semantics without notes — if they struggle with that, the method-set rules will not make sense.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
