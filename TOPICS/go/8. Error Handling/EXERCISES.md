# Exercises — Module 8: Error Handling

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

## Exercise 1: Sentinel Error and errors.Is [🟢 Easy] [1 pt]

### Context
Sentinel errors are package-level error values used as well-known signals. Callers match against them using `errors.Is`, which traverses wrapped error chains. This exercise builds the core habit: define a sentinel, wrap it, and use `errors.Is` — not `==` — to match it.

### Task
1. Define two package-level sentinel errors: `ErrNotFound` and `ErrExpired`.
2. Write a function `lookup(id int) error` that returns `ErrNotFound` for `id < 0` and `ErrExpired` for `id == 0`, wrapped with `fmt.Errorf("lookup %d: %w", id, ...)`. Return `nil` for positive IDs.
3. Call `lookup` with `-1`, `0`, and `1`. For each result, print whether the error is `ErrNotFound`, `ErrExpired`, or nil.
4. Show that `err == ErrNotFound` returns false for a wrapped error, while `errors.Is(err, ErrNotFound)` returns true.

### Requirements
- [ ] Both sentinel errors are declared at package level using `errors.New`
- [ ] `lookup` wraps the sentinel with `%w` (not `%v`)
- [ ] The caller uses `errors.Is` for all checks
- [ ] One comparison using `==` is demonstrated to show it fails on wrapped errors

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Sentinel error declaration:
```go
var (
    ErrNotFound = errors.New("not found")
    ErrExpired  = errors.New("expired")
)
```
The `%w` verb in `fmt.Errorf` preserves the original error so `errors.Is` can find it.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

To demonstrate the `==` failure:
```go
err := lookup(-1)
fmt.Println(err == ErrNotFound)         // false — err is a *fmt.wrapError, not ErrNotFound
fmt.Println(errors.Is(err, ErrNotFound)) // true — traverses the chain
```

</details>

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "errors"
    "fmt"
)

var (
    ErrNotFound = errors.New("not found")
    ErrExpired  = errors.New("expired")
)

func lookup(id int) error {
    switch {
    case id < 0:
        return fmt.Errorf("lookup %d: %w", id, ErrNotFound)
    case id == 0:
        return fmt.Errorf("lookup %d: %w", id, ErrExpired)
    default:
        return nil
    }
}

func main() {
    ids := []int{-1, 0, 1}
    for _, id := range ids {
        err := lookup(id)
        switch {
        case errors.Is(err, ErrNotFound):
            fmt.Printf("id=%d: not found\n", id)
        case errors.Is(err, ErrExpired):
            fmt.Printf("id=%d: expired\n", id)
        case err == nil:
            fmt.Printf("id=%d: ok\n", id)
        }
    }

    // Demonstrate == fails on wrapped errors
    err := lookup(-1)
    fmt.Println("\nDirect == comparison:", err == ErrNotFound)         // false
    fmt.Println("errors.Is comparison:", errors.Is(err, ErrNotFound)) // true
}
```

**Explanation:** The returned error is `fmt.Errorf(...)` — a `*fmt.wrapError` type that wraps `ErrNotFound`. Its pointer value is not equal to `ErrNotFound`, so `==` returns false. `errors.Is` calls `Unwrap()` on the wrapper, retrieving `ErrNotFound`, and matches it. Always use `errors.Is` for sentinel comparisons in Go 1.13+.

</details>

---

## Exercise 2: Custom Error Type with errors.As [🟢 Easy] [1 pt]

### Context
Custom error types let callers extract structured data from an error — not just a string. `errors.As` finds the first value of the target type anywhere in the error chain and assigns it to the caller's pointer.

### Task
1. Define a `ValidationError` struct with fields `Field string` and `Message string`.
2. Implement the `error` interface on `*ValidationError`.
3. Write a function `validateAge(age int) error` that returns a `*ValidationError` when `age < 0` or `age > 150`, wrapped with `fmt.Errorf("validateAge: %w", ...)`. Return `nil` otherwise.
4. Call `validateAge(-5)`. Use `errors.As` to extract the `*ValidationError` and print its `Field` and `Message`.

### Requirements
- [ ] `ValidationError` has `Field` and `Message` string fields
- [ ] `Error() string` returns a human-readable message including both fields
- [ ] `validateAge` wraps the `*ValidationError` with `%w`
- [ ] The caller uses `errors.As`, not a type assertion

### Hints
<details>
<summary>Hint 1</summary>

The `errors.As` call looks like:
```go
var ve *ValidationError
if errors.As(err, &ve) {
    fmt.Println(ve.Field, ve.Message)
}
```
Note: `ve` is declared as `*ValidationError` (a pointer), and you pass `&ve` (pointer to pointer) to `errors.As`.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "errors"
    "fmt"
)

type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: field %q: %s", e.Field, e.Message)
}

func validateAge(age int) error {
    if age < 0 {
        return fmt.Errorf("validateAge: %w", &ValidationError{
            Field:   "age",
            Message: fmt.Sprintf("must be non-negative, got %d", age),
        })
    }
    if age > 150 {
        return fmt.Errorf("validateAge: %w", &ValidationError{
            Field:   "age",
            Message: fmt.Sprintf("unrealistically large: %d", age),
        })
    }
    return nil
}

func main() {
    err := validateAge(-5)
    if err == nil {
        fmt.Println("valid")
        return
    }

    fmt.Println("Error:", err)

    var ve *ValidationError
    if errors.As(err, &ve) {
        fmt.Printf("Field:   %s\n", ve.Field)
        fmt.Printf("Message: %s\n", ve.Message)
    }
}
```

**Explanation:** `errors.As(err, &ve)` traverses the error chain and finds the `*ValidationError` wrapped inside `fmt.Errorf(...%w...)`. It assigns the found value to `ve`. A direct type assertion `err.(*ValidationError)` would panic or return false because `err` is the `*fmt.wrapError` wrapper, not the `*ValidationError` directly.

</details>

---

## Exercise 3: Building an Error Chain [🟡 Medium] [2 pts]

### Context
A well-structured error chain reads like a stack trace in plain English. Each layer adds context about what it was trying to do, and `errors.Is` can still find the original cause. This exercise builds the habit of consistent wrapping.

### Task
Build a three-layer function stack that returns a wrapped error chain:
1. `readLine(r io.Reader) (string, error)` — reads one line; if `io.EOF` is returned from `bufio.Scanner`, wrap it as `fmt.Errorf("readLine: %w", io.EOF)`
2. `parseLine(line string) (int, error)` — parses the line as an integer using `strconv.Atoi`; wraps any error as `fmt.Errorf("parseLine %q: %w", line, err)`
3. `processFile(path string) ([]int, error)` — opens a file, reads all lines via `readLine`, parses each via `parseLine`, collects results; wraps errors as `fmt.Errorf("processFile %s: %w", path, err)`

Call `processFile` with a path to a temp file containing `"1\n2\nabc\n4\n"`. Verify:
- The returned error message contains all three function names
- `errors.Is(err, strconv.ErrSyntax)` returns true

### Requirements
- [ ] Each function wraps errors with `%w`, not `%v`
- [ ] The error message chain includes at least two function names visible in the string
- [ ] `errors.Is(err, strconv.ErrSyntax)` returns true on the returned error

### Hints
<details>
<summary>Hint 1</summary>

`strconv.Atoi` returns a `*strconv.NumError` whose `Err` field is `strconv.ErrSyntax` for non-numeric input. `errors.Is` traverses into `*strconv.NumError.Err`, so `errors.Is(err, strconv.ErrSyntax)` will be true if you wrap with `%w` at every layer.

</details>

<details>
<summary>Hint 2</summary>

For reading lines without pulling in a full file, use `bufio.NewScanner(f)` and `scanner.Scan()`. When `Scan()` returns false, call `scanner.Err()` — if it's nil, you've reached EOF cleanly.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "bufio"
    "errors"
    "fmt"
    "io"
    "os"
    "strconv"
    "strings"
)

func parseLine(line string) (int, error) {
    n, err := strconv.Atoi(strings.TrimSpace(line))
    if err != nil {
        return 0, fmt.Errorf("parseLine %q: %w", line, err)
    }
    return n, nil
}

func processFile(path string) ([]int, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, fmt.Errorf("processFile %s: %w", path, err)
    }
    defer f.Close()

    var results []int
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := scanner.Text()
        if line == "" {
            continue
        }
        n, err := parseLine(line)
        if err != nil {
            return nil, fmt.Errorf("processFile %s: %w", path, err)
        }
        results = append(results, n)
    }
    if err := scanner.Err(); err != nil {
        return nil, fmt.Errorf("processFile %s: scan: %w", path, err)
    }
    return results, nil
}

func main() {
    // Write a temp file with a bad line
    content := "1\n2\nabc\n4\n"
    if err := os.WriteFile("/tmp/nums.txt", []byte(content), 0644); err != nil {
        fmt.Println("setup error:", err)
        return
    }

    _, err := processFile("/tmp/nums.txt")
    if err != nil {
        fmt.Println("Error:", err)
        // Output: processFile /tmp/nums.txt: parseLine "abc": strconv.Atoi: parsing "abc": invalid syntax

        fmt.Println("Is ErrSyntax?", errors.Is(err, strconv.ErrSyntax)) // true
    }

    _ = io.EOF // suppress unused import
}
```

**Explanation:** The chain is: `processFile` wraps `parseLine`'s error with `%w`; `parseLine` wraps `strconv.Atoi`'s error with `%w`; `strconv.Atoi` returns a `*strconv.NumError` whose `Err` field is `strconv.ErrSyntax`. `errors.Is` traverses all four links and finds `strconv.ErrSyntax`. Using `%v` at any layer would cut the chain and make `errors.Is` return false.

</details>

---

## Exercise 4: errors.Join for Validation [🟡 Medium] [2 pts]

### Context
`errors.Join` (Go 1.20) allows collecting multiple errors and returning them as one. This is the standard pattern for validation functions that should report all problems at once rather than stopping at the first failure.

### Task
Write a `validateUser(name, email string, age int) error` function that:
1. Checks that `name` is not empty; if empty, appends `errors.New("name is required")`
2. Checks that `email` contains `"@"`; if not, appends `errors.New("email must contain @")`
3. Checks that `age` is between 0 and 150 inclusive; if not, appends `fmt.Errorf("age %d out of range [0, 150]", age)`
4. Returns `errors.Join(errs...)` — which returns nil if `errs` is empty

Call `validateUser("", "notanemail", 200)` and verify that the returned error contains all three sub-errors. Also call with valid input and verify nil is returned.

### Requirements
- [ ] All three validation checks run regardless of previous failures
- [ ] `errors.Join` is used to combine errors
- [ ] `errors.Is` works on the joined result to find individual sub-errors

### Hints
<details>
<summary>Hint 1</summary>

Collect errors in a `[]error` slice, append to it conditionally, then return `errors.Join(errs...)`. `errors.Join` returns nil if called with no arguments or all-nil arguments.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "errors"
    "fmt"
    "strings"
)

var (
    ErrNameRequired  = errors.New("name is required")
    ErrEmailInvalid  = errors.New("email must contain @")
)

func validateUser(name, email string, age int) error {
    var errs []error
    if name == "" {
        errs = append(errs, ErrNameRequired)
    }
    if !strings.Contains(email, "@") {
        errs = append(errs, ErrEmailInvalid)
    }
    if age < 0 || age > 150 {
        errs = append(errs, fmt.Errorf("age %d out of range [0, 150]", age))
    }
    return errors.Join(errs...) // nil if len(errs) == 0
}

func main() {
    // Invalid: all three fail
    err := validateUser("", "notanemail", 200)
    if err != nil {
        fmt.Println("Validation errors:")
        fmt.Println(err) // prints all three, newline-separated

        fmt.Println("Is ErrNameRequired?", errors.Is(err, ErrNameRequired))  // true
        fmt.Println("Is ErrEmailInvalid?", errors.Is(err, ErrEmailInvalid))  // true
    }

    fmt.Println()

    // Valid: all pass
    err = validateUser("Alice", "alice@example.com", 30)
    fmt.Println("Valid input error:", err) // <nil>
}
```

**Explanation:** `errors.Join` creates an error that implements `Unwrap() []error`, returning the original slice. `errors.Is` traverses all branches of a joined error, so `errors.Is(err, ErrNameRequired)` is true even though the joined error also contains other sub-errors. The joined error's `Error()` string is all the sub-error messages joined by newlines.

</details>

---

## Exercise 5: Named Returns and Deferred Error Decoration [🟡 Medium] [2 pts]

### Context
Named return values let a deferred function see and modify the error a function is about to return. This pattern provides a single location to add the function name as a prefix to every error, no matter how many return paths exist.

### Task
Write a function `parsePositive(s string) (n int, err error)` that:
1. Uses a named `err` return
2. Defers an anonymous function that, if `err != nil`, wraps it: `err = fmt.Errorf("parsePositive: %w", err)`
3. Uses `strconv.Atoi` to parse `s` — return immediately if parsing fails
4. If the parsed value is zero or negative, sets `err = fmt.Errorf("must be positive, got %d", n)` and returns

Call `parsePositive` with `""`, `"-3"`, and `"42"`. Verify the error message prefix appears in all error cases and that `"42"` returns without error.

### Requirements
- [ ] Named return values are used
- [ ] A single `defer` handles wrapping for all error paths
- [ ] No return site repeats the `"parsePositive:"` prefix

### Hints
<details>
<summary>Hint 1</summary>

The deferred function captures `err` by reference (it's a named return). When the function is about to return, the defer runs and can modify `err` before it leaves the function:
```go
defer func() {
    if err != nil {
        err = fmt.Errorf("parsePositive: %w", err)
    }
}()
```

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "strconv"
)

func parsePositive(s string) (n int, err error) {
    // Single wrap point: every error returned by this function gets the prefix
    defer func() {
        if err != nil {
            err = fmt.Errorf("parsePositive: %w", err)
        }
    }()

    n, err = strconv.Atoi(s)
    if err != nil {
        return // bare return — named values used; defer wraps err
    }
    if n <= 0 {
        err = fmt.Errorf("must be positive, got %d", n)
        return
    }
    return n, nil
}

func main() {
    for _, s := range []string{"", "-3", "42"} {
        n, err := parsePositive(s)
        if err != nil {
            fmt.Printf("parsePositive(%q): %v\n", s, err)
        } else {
            fmt.Printf("parsePositive(%q) = %d\n", s, n)
        }
    }
}
```

**Output:**
```
parsePositive(""):   parsePositive: strconv.Atoi: parsing "": invalid syntax
parsePositive("-3"): parsePositive: must be positive, got -3
parsePositive("42"): parsePositive("42") = 42
```

**Explanation:** The deferred closure captures `err` as a named return — it sees the value `err` will have when the function returns. Every early `return` triggers the deferred function, which adds the function-name prefix. The happy path (`return n, nil`) leaves `err` as nil, so the defer is a no-op. This pattern eliminates redundant wrapping at each return site.

</details>

---

## Exercise 6: Panic and Recover at a Boundary [🔴 Hard] [3 pts]

### Context
`panic` propagates until `recover` stops it in a deferred function. The correct usage is a thin boundary layer that catches panics from called code and converts them to errors, preventing the panic from crashing the whole program. This is essential in server handlers, plugin systems, and any code that invokes user-provided callbacks.

### Task
Implement a `TaskRunner` that runs a slice of functions safely:

1. Define `type Task func() error`
2. Write `func RunAll(tasks []Task) (results []error)` that runs each task in order. For each task:
   a. If the task returns an error, append it to `results`
   b. If the task panics, **recover** from the panic and append `fmt.Errorf("task panicked: %v", recovered)` to `results` — but continue running remaining tasks
3. Create three tasks: one that succeeds, one that returns an error, and one that panics
4. Run all three and print the results slice

### Requirements
- [ ] All three tasks run even after the panicking task
- [ ] The panic is converted to an `error` value, not re-panicked
- [ ] The `recover` is in a deferred function (not called directly)
- [ ] The non-panicking tasks' results are correct

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

The recover must be inside the loop body, inside a helper function — you cannot reuse a single defer across loop iterations (each `defer` is scoped to the function, and a loop iteration is not a function):

```go
func runOne(t Task) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("task panicked: %v", r)
        }
    }()
    return t()
}
```

Then `RunAll` calls `runOne` for each task.

</details>

<details>
<summary>Hint 2</summary>

`results` can hold nil for successful tasks. You might want to print a success indicator for nil entries in `results`.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "errors"
    "fmt"
)

// Task is a unit of work that may fail or panic
type Task func() error

// runOne runs a single task and recovers from any panic, converting it to an error
func runOne(t Task) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("task panicked: %v", r)
        }
    }()
    return t()
}

// RunAll runs all tasks in order, continuing even if a task panics
func RunAll(tasks []Task) []error {
    results := make([]error, len(tasks))
    for i, t := range tasks {
        results[i] = runOne(t)
    }
    return results
}

func main() {
    tasks := []Task{
        // Task 1: success
        func() error {
            fmt.Println("Task 1: running")
            return nil
        },
        // Task 2: normal error
        func() error {
            return errors.New("task 2: something went wrong")
        },
        // Task 3: panic
        func() error {
            panic("catastrophic failure in task 3")
        },
    }

    results := RunAll(tasks)

    fmt.Println("\nResults:")
    for i, err := range results {
        if err == nil {
            fmt.Printf("  Task %d: OK\n", i+1)
        } else {
            fmt.Printf("  Task %d: %v\n", i+1, err)
        }
    }
}
```

**Output:**
```
Task 1: running

Results:
  Task 1: OK
  Task 2: task 2: something went wrong
  Task 3: task panicked: catastrophic failure in task 3
```

**Explanation:** `runOne` is a helper function with its own `defer`/`recover`. This is essential: a single `defer` in `RunAll` would only fire when `RunAll` returns — not at the end of each loop iteration. By extracting `runOne`, each task gets its own defer/recover boundary. After the panic in Task 3 is recovered, `runOne` returns the converted error, and `RunAll` continues with no tasks remaining. The whole program does not crash.

</details>

---

## Exercise 7: Full Error Handling System [⭐ Expert] [5 pts]

### Context
In production Go code, error handling combines all the tools in this module: custom error types, sentinel errors, wrapping, `errors.Is`/`errors.As`, and sometimes a recovery boundary. This exercise asks you to design a small but complete system.

### Task
Implement a mini user-registration service with a full error-handling story:

1. Define `ErrDuplicate` (sentinel) and `ErrInvalid` (sentinel)
2. Define `RegistrationError` struct with fields `Username string`, `Reason string`, and an underlying `Cause error`; implement `Error() string` and `Unwrap() error`
3. Write `Register(username string) error` that:
   - Returns a `RegistrationError` wrapping `ErrInvalid` if `username` is empty or shorter than 3 chars
   - Returns a `RegistrationError` wrapping `ErrDuplicate` if `username == "admin"` (pretend it's taken)
   - Otherwise returns nil
4. Write a caller that calls `Register` with `""`, `"ab"`, `"admin"`, and `"alice"`, and for each error:
   - Checks `errors.Is(err, ErrDuplicate)` and `errors.Is(err, ErrInvalid)` to branch handling
   - Uses `errors.As(err, &re)` to print the `RegistrationError.Reason`

### Requirements
- [ ] `RegistrationError` implements both `Error() string` and `Unwrap() error`
- [ ] `errors.Is` correctly identifies the underlying sentinel through the `RegistrationError` wrapper
- [ ] `errors.As` correctly extracts the `*RegistrationError` from the returned error
- [ ] All four test cases produce the expected output

### Hints
<details>
<summary>Hint 1 (Unwrap pattern)</summary>

For `errors.Is` to traverse through `RegistrationError`, it needs an `Unwrap()` method:
```go
func (e *RegistrationError) Unwrap() error { return e.Cause }
```
This lets `errors.Is(err, ErrDuplicate)` walk from `*RegistrationError` → `e.Cause` → `ErrDuplicate`.

</details>

<details>
<summary>Hint 2 (combined check)</summary>

You can check both `errors.Is` and `errors.As` on the same error:
```go
var re *RegistrationError
if errors.As(err, &re) {
    fmt.Println("reason:", re.Reason)
    if errors.Is(err, ErrDuplicate) {
        fmt.Println("username is taken")
    }
}
```

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "errors"
    "fmt"
)

// Sentinel errors for callers to match against
var (
    ErrDuplicate = errors.New("username already taken")
    ErrInvalid   = errors.New("username invalid")
)

// RegistrationError carries structured details and wraps a sentinel cause
type RegistrationError struct {
    Username string
    Reason   string
    Cause    error // the underlying sentinel
}

func (e *RegistrationError) Error() string {
    return fmt.Sprintf("register %q: %s: %v", e.Username, e.Reason, e.Cause)
}

// Unwrap enables errors.Is and errors.As to traverse into Cause
func (e *RegistrationError) Unwrap() error { return e.Cause }

// Register attempts to register a new username
func Register(username string) error {
    if len(username) < 3 {
        return &RegistrationError{
            Username: username,
            Reason:   "must be at least 3 characters",
            Cause:    ErrInvalid,
        }
    }
    if username == "admin" {
        return &RegistrationError{
            Username: username,
            Reason:   "username is reserved",
            Cause:    ErrDuplicate,
        }
    }
    return nil
}

func main() {
    usernames := []string{"", "ab", "admin", "alice"}
    for _, u := range usernames {
        err := Register(u)
        if err == nil {
            fmt.Printf("Register(%q): OK\n", u)
            continue
        }

        var re *RegistrationError
        if errors.As(err, &re) {
            fmt.Printf("Register(%q): reason=%q\n", u, re.Reason)
        }

        switch {
        case errors.Is(err, ErrInvalid):
            fmt.Printf("  -> invalid username, choose a different one\n")
        case errors.Is(err, ErrDuplicate):
            fmt.Printf("  -> username taken, choose a different one\n")
        }
    }
}
```

**Output:**
```
Register(""):     reason="must be at least 3 characters"
  -> invalid username, choose a different one
Register("ab"):   reason="must be at least 3 characters"
  -> invalid username, choose a different one
Register("admin"): reason="username is reserved"
  -> username taken, choose a different one
Register("alice"): OK
```

**Explanation:** `RegistrationError` implements `Unwrap()` returning its `Cause` field. This creates an error chain: the `*RegistrationError` is at the head, and the sentinel (`ErrDuplicate` or `ErrInvalid`) is one step down. `errors.Is(err, ErrDuplicate)` calls `Unwrap()` on `err`, gets `ErrDuplicate`, and matches. `errors.As(err, &re)` finds the `*RegistrationError` at the head of the chain immediately. This pattern — custom type + sentinel cause + `Unwrap()` — is the standard way to provide both structured data AND matchable signals.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Sentinel Error and errors.Is | — | —/1 | — | — |
| Exercise 2 — Custom Error Type with errors.As | — | —/1 | — | — |
| Exercise 3 — Building an Error Chain | — | —/2 | — | — |
| Exercise 4 — errors.Join for Validation | — | —/2 | — | — |
| Exercise 5 — Named Returns and Deferred Error Decoration | — | —/2 | — | — |
| Exercise 6 — Panic and Recover at a Boundary | — | —/3 | — | — |
| Exercise 7 — Full Error Handling System | — | —/5 | — | — |
| **Total** | | **—/16** | | |

**Passing threshold:** 10/16 (63%). Aim for 14/16 (87%) before taking the test.
