# Answer Key — Module 8: Error Handling

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

### 1.1 — The error interface [1 pt]

**Full credit answer:**
```go
type error interface {
    Error() string
}
```

That is the complete, exact definition. `error` is a built-in interface with a single method `Error()` that returns a `string`. Any type in Go that implements this method automatically satisfies the `error` interface, due to Go's structural typing. The `nil` value of the `error` interface represents no error (success).

**Key points required:**
- The method signature is exactly `Error() string` — no parameters, one string return
- It is an interface, not a struct or type alias
- Satisfying it requires only having the method — no explicit declaration

**Common wrong answers:**
- `type error struct { msg string }` — wrong; `error` is an interface, not a struct
- `Error(string) error` — wrong signature; the method takes no parameters and returns a string

---

### 1.2 — %v vs %w in fmt.Errorf [1 pt]

**Full credit answer:**
`%v` formats the error as a string using its `Error()` method and creates a new, opaque error. The new error has no `Unwrap()` method — it does not preserve the original error in the chain. `errors.Is` and `errors.As` cannot see past a `%v`-wrapped error.

`%w` does everything `%v` does (formats the message) AND stores the original error internally. The resulting error implements `Unwrap() error`, returning the original. `errors.Is` and `errors.As` can traverse through `%w` wrappers.

**When to use each:**
- Use `%w` when callers may need to inspect or match the wrapped error (most cases)
- Use `%v` when you deliberately want to hide the underlying error type from callers — for example, at a public API boundary where internal errors should not leak

**Key points required:**
- `%w` creates a chain-traversable wrapper; `%v` creates an opaque new error
- `errors.Is` / `errors.As` cannot look past `%v`

---

### 1.3 — errors.Is vs == [1 pt]

**Full credit answer:**
`errors.Is(err, target)` traverses the error chain by calling `Unwrap()` repeatedly until it either finds a match (returns true) or reaches nil (returns false). It can find `target` even if `err` is a wrapped error created by `fmt.Errorf("%w", target)` or any other wrapper.

Direct `err == target` only returns true if `err` is the exact same value as `target` — it does not unwrap. In modern Go, most errors are wrapped before being returned, so a direct `==` comparison on a wrapped error will always return false even when the underlying sentinel matches.

**Key points required:**
- `errors.Is` traverses the chain via `Unwrap()`; `==` does not
- Use `errors.Is` for all sentinel error comparisons in Go 1.13+

---

### 1.4 — errors.Join [1 pt]

**Full credit answer:**
`errors.Join` combines multiple errors into a single error value. The resulting error's `Unwrap() []error` method returns the original slice of errors. Both `errors.Is` and `errors.As` traverse all branches of a joined error. It was added in **Go 1.20**. `errors.Join` returns `nil` if all arguments are nil.

**Key points required:**
- Combines multiple errors into one
- Added in Go 1.20
- `errors.Is` / `errors.As` traverse all joined errors

**Common wrong answers:**
- "Go 1.13" — that was the version that added `errors.Is`, `errors.As`, and `%w`; `errors.Join` is Go 1.20

---

### 1.5 — Where recover() must be called [1 pt]

**Full credit answer:**
`recover()` must be called **directly inside a deferred function** — it must be in the immediate deferred function, not in a function called by a deferred function. If called outside a deferred function (e.g., in a normal function body while no panic is in progress), `recover()` simply returns `nil` — it is a no-op. It does not itself panic or cause a compile error.

**Key points required:**
- Must be called directly inside a deferred function
- Calling it outside that context returns nil (no-op)

**Common wrong answers:**
- "It panics if called outside a defer" — it just returns nil
- "It must be called in the function that panicked" — it must be in a deferred function anywhere in the call stack of the panicking goroutine

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — The typed-nil trap [2 pts]

**Full credit answer:**
A Go interface value has two components: a type and a value. An interface is `nil` only when BOTH the type AND the value are nil. The typed-nil trap occurs when a function returns a concrete nil pointer typed as a concrete error type instead of returning an untyped `nil` as the `error` interface.

**Wrong version:**
```go
func mayFail() error {
    var e *MyError // nil pointer, but typed as *MyError
    if failed {
        e = &MyError{...}
    }
    return e // WRONG: returns (*MyError)(nil) — a non-nil interface
}
```

The returned `error` has type `*MyError` and value nil — its type component is non-nil, so the interface itself is non-nil. The caller's `if err != nil` check will be true even when nothing failed.

**Correct version:**
```go
func mayFail() error {
    if failed {
        return &MyError{...}
    }
    return nil // untyped nil — both type and value are nil
}
```

**How to avoid:** Never use a typed variable of an error type to accumulate and return the result. Always `return nil` for the success case using an untyped nil.

**Rubric:**
- 2 pts: Correctly explains the interface representation (type + value), shows the wrong pattern, shows the correct pattern, explains why it happens
- 1 pt: Identifies the trap and shows a fix, but explanation of why it happens is incomplete
- 0 pts: Incorrect explanation or confuses this with other nil interface behavior

---

### 2.2 — Errors as values vs exceptions [2 pts]

**Full credit answer (two specific advantages):**

**Advantage 1 — Explicit call-site control flow:**
With errors-as-values, every function call that can fail shows its failure handling at the call site. There are no hidden `throw`/`catch` paths — you see exactly where errors are handled and what happens to them. When reviewing a code change in pull request, you can audit error handling without needing to understand the entire exception hierarchy.

**Advantage 2 — Errors can be stored, collected, and processed as data:**
Because errors are values, you can store them in slices (for collecting multiple errors), pass them to functions, compare them, and delay handling. Exception-based languages require try/catch blocks and cannot easily collect errors from a loop into a list for later reporting. In Go, `errors.Join` and similar patterns are natural extensions of this.

**Rubric:**
- 2 pts: Two concrete, specific advantages; avoids vague claims like "simpler" or "cleaner"
- 1 pt: One concrete advantage with good explanation, or two vague advantages
- 0 pts: Only restates "errors are values" without explaining the practical benefit

---

### 2.3 — errors.Is vs errors.As [2 pts]

**Full credit answer:**
`errors.Is(err, target)` answers "does the error chain contain a specific value?" — it is used for sentinel error matching. It compares each error in the chain to `target` using `==` (or a custom `Is` method if defined).

`errors.As(err, &target)` answers "does the error chain contain a value of this type?" — it is used for extracting structured data from a custom error type. It sets `target` to the first error in the chain whose type matches the target's type.

**When to use `errors.Is`:**
Checking for a known sentinel: `errors.Is(err, sql.ErrNoRows)`, `errors.Is(err, io.EOF)`. The caller wants to know if a specific well-known condition occurred.

**When to use `errors.As`:**
Extracting data from a custom error type: `errors.As(err, &myErr)` to get the `StatusCode` from an `*HTTPError`. The caller wants structured information, not just "did this specific thing happen."

**Rubric:**
- 2 pts: Correctly distinguishes value matching (`Is`) from type extraction (`As`); gives one appropriate scenario for each
- 1 pt: Correctly describes one but not the other, or describes both but without distinguishing them clearly
- 0 pts: Confuses the two, or says they are interchangeable

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — openDB function [3 pts]

**Full credit answer:**
```go
func openDB(dsn string) (*sql.DB, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, fmt.Errorf("openDB: open connection: %w", err)
    }
    if err := db.Ping(); err != nil {
        return nil, fmt.Errorf("openDB: ping: %w", err)
    }
    return db, nil
}
```

**Key requirements:**
- `sql.Open` and `db.Ping` both checked for errors
- Each error wrapped with `fmt.Errorf("...: %w", err)` using `%w` not `%v`
- Function name (`openDB`) appears in the error context
- `nil` returned alongside the error value (never return a non-nil `*sql.DB` with an error)

**Rubric:**
- 3 pts: Both error checks present; both wrapped with context and `%w`; `nil` returned with errors
- 2 pts: Both error checks present; wrapping uses `%v` instead of `%w`, or context is missing
- 1 pt: Only one error check present, or errors returned bare (no wrapping)
- 0 pts: No error checking, or fundamental misunderstanding of the pattern

**Common wrong answers:**
- Returning `db` alongside an error — if `db.Ping()` fails, `db` should not be returned to callers; return `nil, err`
- Using `%v` — loses the wrapping chain

---

### 3.2 — safeEval with named returns and recover [3 pts]

**Full credit answer:**
```go
func safeEval(expr string, eval func(string) int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("safeEval: panic: %v", r)
        }
    }()
    result = eval(expr)
    return
}
```

**Key requirements:**
- Named return values (`result int, err error`)
- `defer func() { if r := recover(); r != nil { err = ... } }()` — the deferred IIFE (immediately-invoked function expression)
- `recover()` called inside the deferred function, not directly in the function body
- `result = eval(expr)` — assigns to the named return (not `:=`)
- Bare `return` at the end

**Rubric:**
- 3 pts: Named returns used; recover in a deferred function; correctly sets `err` from the named return; bare `return` or explicit return with named values
- 2 pts: Correct recover logic but named returns not used (uses local variables instead), OR named returns used but recover is in wrong location
- 1 pt: The concept is right but there are significant syntax errors, OR recover is called directly (not in defer)
- 0 pts: Does not demonstrate recover, or fundamentally misuses defer/recover

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Three problems in processRequest [3 pts] (1 pt each)

**Problem 1 — Log-and-return (anti-pattern)**

```go
log.Printf("fetchUser failed: %v", err)
return User{}, err   // WRONG: logs here AND returns; each layer will log again
```

**Why it's wrong:** If the caller also logs the returned error, the same error appears in logs multiple times from different call sites, making it impossible to trace the original source.

**Fix — choose one:**
```go
// Option A: wrap and return (let the top-level log once)
return User{}, fmt.Errorf("processRequest fetchUser %d: %w", userID, err)

// Option B: log at this boundary and return an opaque error (for public APIs)
log.Printf("fetchUser %d: %v", userID, err)
return User{}, ErrInternal
```

---

**Problem 2 — Direct == comparison on a potentially-wrapped error**

```go
if err == ErrNotFound {   // WRONG: fails if err is a wrapped ErrNotFound
```

**Why it's wrong:** If `loadProfile` wraps its error (e.g., `fmt.Errorf("loadProfile: %w", ErrNotFound)`), then `err == ErrNotFound` is false even though the underlying cause is `ErrNotFound`. The branch is silently skipped.

**Fix:**
```go
if errors.Is(err, ErrNotFound) {
```

---

**Problem 3 — Bare return with no context, AND returning fetchErr (always nil)**

Two issues on the last lines:
```go
return User{}, err    // bare return — no context added
return buildUser(u, data), fetchErr  // fetchErr is always nil — meaningless
```

**Issue 3a:** The error from `loadProfile` is returned bare — no context telling the caller that `processRequest` failed while loading a profile.

**Fix:**
```go
return User{}, fmt.Errorf("processRequest %d: loadProfile: %w", userID, err)
```

**Issue 3b:** `var fetchErr *FetchError` is declared at the top of the function and never assigned. It is always nil. The success return `buildUser(u, data), fetchErr` is equivalent to `buildUser(u, data), nil` — it is dead code and misleading.

**Fix:**
```go
return buildUser(u, data), nil
```
(Remove `fetchErr` entirely since it is never set.)

**Rubric:**
- 1 pt per correctly identified and explained problem, with a valid fix
- 0.5 pts for identifying the problem but the fix is incomplete or slightly wrong

---

## Section 5: Discussion — Answer Key

### 5.1 — When panic is appropriate [2 pts]

**Example strong answer:**
"Use `panic` only for programmer errors and unrecoverable situations" means: panic when continued execution would produce incorrect or undefined behavior — not when a user made bad input, a file is missing, or a network call failed. These latter situations are *expected* failure modes because any well-written program will encounter them at runtime, and the caller can meaningfully respond.

**Appropriate use:** Calling `panic` in an internal function when an argument violates a documented invariant — e.g., `if n < 0 { panic("mustPositive: negative argument") }`. This is a programmer error; the contract was violated. No caller should ever pass a negative number, so crashing loudly is better than silently computing wrong results.

**Inappropriate use:** Calling `panic` when a config file is not found at startup. This is expected — the file might be missing on a fresh deployment. The correct alternative is `return fmt.Errorf("load config: %w", err)` and letting main print a helpful message and exit with `os.Exit(1)`.

"Expected" means any condition a reasonably-written caller could encounter and handle without it indicating a bug. "Unrecoverable" means the program cannot proceed correctly — a nil pointer in code that assumes non-nil, an invariant that, if violated, means all subsequent computations are wrong.

**Elements that earn full credit:**
- Explains the distinction between expected failure and programmer error
- Gives one concrete appropriate panic use with reasoning
- Gives one concrete inappropriate use with the correct alternative
- Does not claim panic should be used for performance or "cleanliness"

**Rubric:**
- 2 pts: Addresses the expected/unrecoverable distinction; two concrete examples; correct alternative given
- 1 pt: Identifies the distinction but examples are vague, or only one example provided
- 0 pts: Claims panic is appropriate for any non-nil error, or confuses panic with log.Fatal

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Result[T] generic type [+5 pts]

**Full credit answer:**
```go
package main

import "fmt"

// Result holds either a value of type T or an error — never both
type Result[T any] struct {
    value T
    err   error
    ok    bool
}

// OK creates a successful Result
func OK[T any](v T) Result[T] {
    return Result[T]{value: v, ok: true}
}

// Err creates a failed Result
func Err[T any](e error) Result[T] {
    return Result[T]{err: e}
}

// Unwrap returns the value and error, idiomatic Go style
func (r Result[T]) Unwrap() (T, error) {
    return r.value, r.err
}

// Must returns the value or panics if the Result holds an error
func (r Result[T]) Must() T {
    if r.err != nil {
        panic(fmt.Sprintf("Result.Must: called on error result: %v", r.err))
    }
    return r.value
}

// IsOK returns true if the Result holds a value
func (r Result[T]) IsOK() bool { return r.ok }

func main() {
    // Successful result
    r := OK(42)
    v, err := r.Unwrap()
    fmt.Println(v, err) // 42 <nil>

    // Error result
    r2 := Err[int](fmt.Errorf("something failed"))
    v2, err2 := r2.Unwrap()
    fmt.Println(v2, err2) // 0 something failed

    // Must on a good result
    fmt.Println(r.Must()) // 42

    // Must on a bad result (would panic)
    // r2.Must() // panics: Result.Must: called on error result: something failed
}
```

**When `Result[T]` is useful:**
When building a pipeline of operations where you want to pass partial results through channels or slices without losing the error. For example, a concurrent pipeline processing N items could send `Result[Item]` values on a channel, letting the consumer decide whether to continue or abort.

**When idiomatic `(T, error)` is preferable:**
For most Go code, `(T, error)` is simpler, requires no extra type, composes naturally with `if err != nil`, and is universally understood by Go programmers. `Result[T]` adds an abstraction layer that must be explained. Use `(T, error)` by default; reach for `Result[T]` only when the use case specifically requires treating both value and error as a single value.

**Rubric:**
- 5 pts: Correct generic syntax; `OK`, `Err`, `Unwrap`, `Must` all implemented correctly; thoughtful explanation of when each is appropriate
- 3 pts: Implementation works for at least 3 of 4 methods; explanation present but shallow
- 1 pt: Type definition is correct but methods have significant errors; or no explanation
- 0 pts: Generic syntax is wrong or the implementation fundamentally misunderstands the concept

**Teaching note:** Many Go programmers argue this pattern goes against Go's idioms. Full credit requires acknowledging that — the point is not that `Result[T]` is always better, but that the student can implement it and articulate the tradeoffs.

---

## Common Wrong Answers Across the Test

1. **Using `%v` instead of `%w` in wrapping** — Students who don't understand the difference will use `%v` throughout and be confused when `errors.Is` returns false. The fix: `%w` is for wrapping (preserves the chain), `%v` is for formatting (opaque new error). Go back to the "Wrapping Errors" section.
2. **Calling `recover()` in a normal function body** — Students may write `r := recover()` directly in their function. This is not a compile error and returns nil, but it does NOT stop a panic. `recover` only works inside a deferred function. Go back to the "Panic and Recover" section.
3. **Returning a typed nil as error** — The typed-nil trap is consistently the most-missed concept in this module. Students who answer "it works fine" for the wrong version in Q2.1 need to re-read the interface representation section (interface = type + value pair).
4. **Answering Q4.1 with only 1–2 problems** — The debugging question has three distinct issues. Students who find only one or two usually miss the `fetchErr` being always nil. Read the code carefully: declare → never assign → return at the end.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 have likely understood the mechanics but not the reasoning. Feynman technique: ask them to explain to someone else why `errors.Is` is needed instead of `==`. If they can't, they haven't fully internalized error chains.
- Students who miss Q4.1's three problems should re-read "Common Beginner Mistakes and Anti-Patterns." The log-and-return anti-pattern is particularly important to internalize because it produces production log noise that makes incidents harder to debug.
- Students who write `recover()` outside a `defer` are confusing "where it is called" with "when it runs." A concrete mental model: `recover()` is only meaningful while the panic unwind is happening, and that unwind only touches deferred functions.
- The bonus question is meant to be intellectually challenging. A student who implements it but argues strongly against its idiomatic use is showing mature Go judgment — award full points.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
