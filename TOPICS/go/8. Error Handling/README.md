# Module 8: Error Handling

[← Module 7: Packages and Modules](../7.%20Packages%20and%20Modules/) | [Topic Home](../README.md) | [Module 9: Concurrency →](../9.%20Concurrency/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-blue)
![Time](https://img.shields.io/badge/time-4--5h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [The error Interface](#the-error-interface)
  - [Errors as Values — the Philosophy](#errors-as-values--the-philosophy)
  - [Creating Errors](#creating-errors)
  - [The if err != nil Idiom](#the-if-err--nil-idiom)
  - [Sentinel Errors and errors.Is](#sentinel-errors-and-errorsis)
  - [Wrapping Errors and Error Chains](#wrapping-errors-and-error-chains)
  - [Custom Error Types and errors.As](#custom-error-types-and-errorsas)
  - [errors.Join — Multiple Wrapping (Go 1.20)](#errorsjoin--multiple-wrapping-go-120)
  - [Adding Context Without Leaking](#adding-context-without-leaking)
  - [Panic and Recover](#panic-and-recover)
  - [Named Return Values and Deferred Error Decoration](#named-return-values-and-deferred-error-decoration)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes and Anti-Patterns](#common-beginner-mistakes-and-anti-patterns)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Related Concepts](#related-concepts)
- [Exercises](#exercises)
- [Test](#test)
- [Projects](#projects)
- [Further Reading](#further-reading)
- [Learning Journal](#learning-journal)

---

## Overview

This module covers **Go's error handling philosophy and mechanics**: the `error` interface, errors-as-values, wrapping, custom error types, `errors.Is`/`errors.As`, `errors.Join`, and the `panic`/`recover` mechanism. These are the tools every Go program beyond "Hello, World!" relies on to communicate and handle failure correctly.

Go's approach to errors is intentionally different from languages that use exceptions. Understanding *why* Go made these choices — and how to use them idiomatically — is the mark of a working Go professional. This module goes beyond syntax: it explains the reasoning behind each tool and shows where each applies.

**Difficulty:** Intermediate &nbsp;|&nbsp; **Estimated time:** 4–5 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain what `error` is in Go and implement the interface yourself — _given a Go value, determine whether it satisfies `error`_
2. Create errors with `errors.New` and `fmt.Errorf`, wrapping with `%w` to form error chains — _given a chain of wrapped errors, trace every link_
3. Distinguish sentinel errors from custom error types; use `errors.Is` and `errors.As` correctly — _rewrite a type assertion on an error to use the idiomatic sentinel or structured error pattern_
4. Write a `panic`/`recover` boundary at a server or library boundary, and explain exactly when `panic` is appropriate vs. not — _read a code review and identify a misuse of panic_
5. Identify and fix the three most common error anti-patterns (swallowed errors, log-and-return, over-wrapping) — _audit a function for error handling quality_

---

## Prerequisites

### Required Modules

- [[go/6. Methods and Interfaces]] — you need to understand: how interfaces work in Go, structural typing, and how a concrete type satisfies an interface; `error` is just an interface with one method
- [[go/3. Functions]] — you need to understand: multiple return values (every fallible function returns `(T, error)`), named return values, defer, and closures; all interact directly with error handling patterns
- [[go/2. Control Flow]] — you need to understand: the `if` init statement (`if err := f(); err != nil`), defer mechanics, and how defer interacts with function returns

### Required Concepts

- **Interfaces and method sets** — `error` is a built-in interface with one method: `Error() string`; any type that implements this method satisfies `error`
- **Multiple return values** — Go functions return `(result, error)` pairs; understanding how to declare, call, and unpack these is essential
- **defer** — deferred functions run at function return; this is the mechanism behind both cleanup and deferred error decoration

> [!TIP]
> If interfaces feel shaky, spend 20 minutes re-reading [[go/6. Methods and Interfaces]] before continuing.
> The entire error handling system is built on the interface mechanism — a fuzzy prerequisite will cause concrete confusion here.

---

## Why This Matters

Error handling is not a secondary concern in Go — it is central to the language's design. Nearly every non-trivial Go function returns an error, and callers are expected to check it explicitly. This is not boilerplate; it is Go's primary mechanism for communicating partial failure, distinguishing recoverable from unrecoverable states, and propagating failure context up the call stack.

Concretely, mastery of this module enables you to:

- **Write robust services that degrade gracefully** — a web server that wraps every handler in `recover` stays alive even when a goroutine panics; a service that properly wraps and checks errors can return meaningful HTTP status codes to callers instead of generic 500s
- **Debug production failures faster** — a properly wrapped error chain (`open config.yaml: parse line 42: unexpected token "}"`) tells you exactly what happened and where; an improperly handled error chain gives you `unexpected token` with no context
- **Design APIs that callers can react to** — using sentinel errors (`io.EOF`, `sql.ErrNoRows`) or custom error types lets callers distinguish "not found" from "permission denied" from "network error" and handle each appropriately

Without understanding Go's error handling, you would produce programs that silently ignore failures, expose raw OS errors to callers, or use `panic` for recoverable conditions — all of which cause unpredictable production behavior.

---

## Historical Context

Go was designed at Google by **Robert Griesemer, Rob Pike, and Ken Thompson** with an explicit decision to use **errors as values** rather than exceptions. This decision was made in **2007** during the initial language design phase and has remained unchanged through Go 1.22.

The exception mechanism — as found in Java, Python, C++, and Ruby — allows a function to "throw" an error that skips multiple stack frames until caught somewhere above. This was considered by the Go designers to have a critical flaw: it makes the control flow of a program non-obvious. An exception can surface anywhere and be caught anywhere, making programs harder to reason about at scale.

Key moments in Go's error handling evolution:

- **2009** — Go 1.0 pre-release: the `error` interface (`type error interface { Error() string }`) is present from the beginning; `os.PathError` is an early custom error type in the standard library
- **2011** — `fmt.Errorf` added to the standard library, enabling formatted error messages; but no wrapping mechanism yet
- **2012** — Go 1.0 release: the `errors` package ships with `errors.New`; Rob Pike publishes "Errors are values" as a design philosophy — errors are first-class values, not exceptional control flow
- **2019** — Go 1.13: the `%w` verb added to `fmt.Errorf`; `errors.Is`, `errors.As`, and `errors.Unwrap` added; this makes error wrapping and inspection idiomatic and standardized for the first time
- **2023** — Go 1.20: `errors.Join` added, enabling a single error to wrap multiple errors — essential for aggregating validation failures or parallel operation results

Understanding this history clarifies why the `errors` package is so minimal and why wrapping was a later addition: Go started with the simplest possible model and added wrapping only when real patterns demanded it.

---

## Core Concepts

### The error Interface

`error` is a built-in interface in Go, defined as:

```go
type error interface {
    Error() string
}
```

That is the entire definition. Any type with an `Error() string` method satisfies the `error` interface. Because [[go/6. Methods and Interfaces]] showed that Go uses structural typing, there is no `implements` keyword — the type automatically satisfies `error` just by having the right method.

The `nil` value of the `error` interface represents "no error". This is the idiomatic success signal:

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil // nil error means success
}
```

This is critically different from how exceptions work: the caller is required to explicitly check for `nil`. There is no hidden control flow.

---

### Errors as Values — the Philosophy

The Go blog post "Errors are values" (2015, Rob Pike) articulates the core philosophy: an error is just a value of type `error`. It is not special. You can store it in a variable, pass it to a function, put it in a struct field, return it from a function, or print it. The same reasoning you apply to any other value applies to errors.

This has practical consequences:

```go
// errors are values — you can store them, pass them, collect them
var firstErr error

for _, path := range paths {
    if err := process(path); err != nil && firstErr == nil {
        firstErr = err // save the first error and keep going
    }
}
return firstErr
```

Compare this to exceptions: you cannot pass an exception to another function as a value, store it in a slice alongside results, or choose to process it later. Errors-as-values gives you full control over how and when you handle failure.

---

### Creating Errors

**`errors.New`** creates a simple error from a static string:

```go
import "errors"

var ErrDivisionByZero = errors.New("division by zero")
// ErrDivisionByZero is a package-level sentinel error value
```

Each call to `errors.New` creates a distinct error value — two calls with the same string are NOT equal:

```go
e1 := errors.New("oops")
e2 := errors.New("oops")
fmt.Println(e1 == e2) // false — different pointer values
```

**`fmt.Errorf`** creates a formatted error message, identical to `fmt.Sprintf` but returning `error`:

```go
import "fmt"

func openConfig(path string) error {
    // adds context: which file, what went wrong
    return fmt.Errorf("open config %s: file not found", path)
}
```

**The `%w` verb** (Go 1.13+) wraps an existing error, preserving it for later inspection:

```go
func readConfig(path string) error {
    data, err := os.ReadFile(path)
    if err != nil {
        // wrap: adds context AND preserves the original error
        return fmt.Errorf("readConfig %s: %w", path, err)
    }
    // ...
    return nil
}
```

Use `%w` when the caller might need to inspect or match the wrapped error. Use `%v` (or `%s`) when the error is purely informational and callers should only read the message, never match it.

---

### The if err != nil Idiom

The canonical Go error check is:

```go
result, err := someFunction()
if err != nil {
    return ..., err // or wrap: return ..., fmt.Errorf("context: %w", err)
}
// use result safely here
```

This pattern is Go's primary control flow for failure. It appears in virtually every non-trivial Go file. Keeping it readable is a legitimate engineering concern.

**Keep the happy path un-indented.** Go style keeps the main logic at the base indentation level and error handling in short `if err != nil` branches:

```go
// Good: happy path at base level, error handling is short
func processFile(path string) ([]Record, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, fmt.Errorf("processFile: %w", err)
    }
    defer f.Close()

    records, err := parseRecords(f)
    if err != nil {
        return nil, fmt.Errorf("processFile: parse: %w", err)
    }

    return records, nil
}
```

**The init-statement form** (from [[go/2. Control Flow]]) is useful for single-use variables:

```go
if err := db.Ping(); err != nil {
    return fmt.Errorf("database unreachable: %w", err)
}
```

**Why not exceptions?** Consider what happens in a language with exceptions: every function call is potentially a jump out of the current function. With `if err != nil`, the control flow is entirely explicit — you can read exactly which calls can fail and exactly how each failure is handled.

---

### Sentinel Errors and errors.Is

A **sentinel error** is a package-level error value used as a signal:

```go
// In the io package:
var EOF = errors.New("EOF")

// In the sql package:
var ErrNoRows = errors.New("sql: no rows in result set")
```

Callers check for these signals using `errors.Is`:

```go
data, err := io.ReadAll(r)
if errors.Is(err, io.EOF) {
    // normal end of stream — not an error in this context
}

row, err := db.QueryRow(query).Scan(&name)
if errors.Is(err, sql.ErrNoRows) {
    // not found — handle as empty result
}
```

**`errors.Is` traverses the entire error chain.** If an error was wrapped with `%w`, `errors.Is` unwraps it recursively until it finds a match:

```go
original := io.EOF
wrapped := fmt.Errorf("read line: %w", original)
rewrapped := fmt.Errorf("parse file: %w", wrapped)

fmt.Println(errors.Is(rewrapped, io.EOF)) // true — traverses the chain
```

**Why `errors.Is` instead of `==`?** Direct comparison (`err == io.EOF`) only works if the error is the sentinel itself, not a wrapped version of it. In modern Go, most errors are wrapped before being returned, so `==` is wrong for sentinel checks. Always use `errors.Is`.

> [!WARNING]
> **Typed-nil trap:** `errors.Is(err, target)` where `target` is a non-nil pointer to a nil value of an error type will NOT match a nil error. The canonical case: a function returns a `*MyError` typed as `error` but with a nil pointer — this is NOT `nil` as `error`. See [Common Beginner Mistakes](#common-beginner-mistakes-and-anti-patterns).

---

### Wrapping Errors and Error Chains

Wrapping adds context to an error without losing the original. A well-wrapped error reads like a stack trace in plain English:

```go
// open config.yaml: no such file or directory
// ^context^         ^original OS error^
```

Build this chain as the error travels up the call stack:

```go
func loadApp(configPath string) error {
    cfg, err := readConfig(configPath)
    if err != nil {
        return fmt.Errorf("loadApp: %w", err)
    }
    // ...
}

func readConfig(path string) error {
    data, err := os.ReadFile(path)
    if err != nil {
        return fmt.Errorf("readConfig %s: %w", path, err)
    }
    // ...
}

// Result when config.yaml is missing:
// loadApp: readConfig config.yaml: open config.yaml: no such file or directory
```

**`errors.Unwrap`** returns the wrapped error (the value passed as `%w`), or `nil` if there is none:

```go
wrapped := fmt.Errorf("context: %w", io.EOF)
inner := errors.Unwrap(wrapped) // returns io.EOF
```

**Error chain traversal:**

```go
// errors.Is walks the chain:
// wrapped → errors.Unwrap → inner → errors.Unwrap → nil
```

The chain is a linked list. `errors.Is` and `errors.As` traverse it automatically.

---

### Custom Error Types and errors.As

When callers need structured data from an error — not just a string — define a custom error type:

```go
// ParseError carries the line number and the bad input
type ParseError struct {
    Line    int
    Column  int
    Message string
}

func (e *ParseError) Error() string {
    return fmt.Sprintf("parse error at line %d col %d: %s", e.Line, e.Column, e.Message)
}
```

Return it from a function (as `error`, not as `*ParseError` — see the typed-nil warning):

```go
func parseFile(path string) error {
    // ...
    return &ParseError{Line: 42, Column: 7, Message: `unexpected token "}"`}
}
```

**`errors.As`** extracts the target type from anywhere in the chain:

```go
err := parseFile("config.yaml")
var pe *ParseError
if errors.As(err, &pe) {
    fmt.Printf("Error on line %d: %s\n", pe.Line, pe.Message)
}
```

`errors.As` traverses the error chain (like `errors.Is`) and assigns the first matching error to the target. The target must be a pointer to the type you want — `*ParseError` above means "find a `*ParseError` anywhere in the chain and assign it to `pe`".

**`errors.As` vs type assertion:** A direct type assertion (`err.(*ParseError)`) only works if `err` is exactly a `*ParseError` — it fails if the error has been wrapped. Always prefer `errors.As` for structured error inspection.

---

### errors.Join — Multiple Wrapping (Go 1.20)

`errors.Join` combines multiple errors into one. The resulting error's `Unwrap() []error` method returns all wrapped errors:

```go
import "errors"

func validateUser(u User) error {
    var errs []error
    if u.Name == "" {
        errs = append(errs, errors.New("name is required"))
    }
    if u.Age < 0 {
        errs = append(errs, errors.New("age must be non-negative"))
    }
    if u.Email == "" {
        errs = append(errs, errors.New("email is required"))
    }
    return errors.Join(errs...) // returns nil if errs is empty
}
```

`errors.Is` and `errors.As` both traverse multi-wrapped errors from `errors.Join`. The message is the joined text of all errors, separated by newlines.

Use `errors.Join` when you need to report all failures at once (validation, batch operations) rather than stopping at the first error.

---

### Adding Context Without Leaking

Adding context means making error messages useful to the caller. Leaking means exposing internal implementation details that callers should not depend on.

**Good context — what, where, why:**

```go
return fmt.Errorf("createUser %q: insert into users: %w", username, err)
// "what" = create user, "where" = insert into users, "why" = the wrapped error
```

**Leaking — over-specific or implementation-revealing:**

```go
// Bad: exposes the SQL query text — now callers might depend on it
return fmt.Errorf("INSERT INTO users (name, email) VALUES ($1, $2) failed: %w", err)

// Bad: exposes the internal package name — unnecessary coupling
return fmt.Errorf("github.com/myco/myapp/internal/db.CreateUser: %w", err)
```

**No context — just as bad:**

```go
// Bad: caller has no idea what file or operation failed
if err != nil {
    return err // bare return — no wrapping, no context
}
```

The right amount of context is: enough to understand the call chain from the error message alone, without exposing implementation internals.

---

### Panic and Recover

`panic` is Go's mechanism for unrecoverable situations — not a general-purpose error signaling tool. When a function calls `panic(v)`, the current goroutine begins unwinding its stack, running all deferred functions as it goes. If no `recover` is called in any deferred function, the program crashes and prints a stack trace.

**When panic is appropriate:**

```go
// 1. Programmer errors — invariants that should never be violated
func mustPositive(n int) int {
    if n <= 0 {
        panic(fmt.Sprintf("mustPositive: got %d, expected > 0", n))
    }
    return n
}

// 2. Initialization that cannot proceed — use in init() or main setup
func main() {
    db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil {
        log.Fatalf("cannot open database: %v", err) // log.Fatal calls os.Exit(1)
    }
    // (log.Fatal is preferred over panic in main — cleaner output)
}

// 3. Truly impossible states — after an exhaustive type switch
switch v := x.(type) {
default:
    panic(fmt.Sprintf("unexpected type %T", v))
}
```

**When panic is NOT appropriate:**

- File not found, network timeout, database error — these are expected failure modes; return `error`
- Input validation — return a descriptive `error`
- Any condition a well-written caller could reasonably encounter and handle

**`recover`** stops the unwinding started by `panic` and returns the value passed to `panic`. It is only useful inside a deferred function:

```go
func safeDiv(a, b int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("recovered panic: %v", r)
        }
    }()
    return a / b, nil // panics if b == 0 (integer division by zero)
}
```

**`recover` at a boundary** — the most common real use is protecting a server from crashing when a handler panics:

```go
// HTTP middleware that recovers from panics in handlers
// (See also [[go/13. Web Services and APIs]] for the full middleware pattern)
func recoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                // log the stack trace for debugging
                log.Printf("panic recovered: %v\n%s", rec, debug.Stack())
                http.Error(w, "Internal Server Error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

**Re-panicking** — sometimes the right action after recovering is to re-panic, after logging or cleanup:

```go
defer func() {
    if r := recover(); r != nil {
        log.Printf("unexpected panic: %v", r)
        panic(r) // re-panic — let it propagate up
    }
}()
```

**The relationship between `defer`, `panic`, and `recover`:**

When `panic` is called:
1. Execution of the current function stops immediately
2. All deferred functions in the current goroutine's stack begin running (LIFO)
3. If a deferred function calls `recover()`, unwinding stops and the goroutine continues normally
4. If no `recover()` is called, the program crashes with a stack trace

---

### Named Return Values and Deferred Error Decoration

Named return values combined with `defer` allow a function to add context to any error it returns, regardless of which return path triggered:

```go
func openAndRead(path string) (data []byte, err error) {
    // The deferred function can see and modify the named 'err' return value
    defer func() {
        if err != nil {
            err = fmt.Errorf("openAndRead %s: %w", path, err)
        }
    }()

    f, err := os.Open(path)
    if err != nil {
        return nil, err // deferred func wraps this automatically
    }
    defer f.Close()

    data, err = io.ReadAll(f)
    return // bare return — named return values are used; defer runs and wraps
}
```

This pattern ensures the function name appears in every error it returns, without repeating the wrapping at every `return` site. It is most useful for functions with many return paths.

> [!NOTE]
> This pattern requires that the `defer` is registered before any of the `return` statements that produce errors — which is always the case since `defer` statements execute during function setup.

---

### How the Concepts Fit Together

```
Failure occurs in a function
         │
         ▼
  Create error value ────────── errors.New / fmt.Errorf
         │
         ▼
  Return (value, error) ──────── if err != nil { return ..., fmt.Errorf("ctx: %w", err) }
         │                        adds context, preserves error chain
         ▼
  Caller inspects error
         ├── Is it a sentinel?  ──────── errors.Is(err, ErrNotFound)
         ├── Does it carry data? ─────── errors.As(err, &myErrPtr)
         └── Is it multiple?  ────────── errors.Join(e1, e2, ...)
                                          + errors.Is / errors.As on the joined result
         │
         ▼
  Unrecoverable? ──────────────── panic(msg)  ← programmer error / invariant violation
         │                        defer + recover at boundary ← server, library API
         ▼
  Propagate or handle
```

In practice: most errors are created low in the call stack, wrapped with context at each layer, and inspected (via `errors.Is`/`errors.As`) by callers that need to react differently to different failure modes. `panic` is reserved for situations where continued execution would be incorrect.

---

## Common Beginner Mistakes and Anti-Patterns

> [!WARNING]
> **Anti-pattern 1: Swallowing errors (ignoring the return value)**
>
> Assigning an error to `_` or simply not checking it means the program continues in a potentially broken state. This is the most dangerous anti-pattern in Go.
>
> **Wrong:**
> ```go
> os.Remove(tempFile) // error silently ignored
> data, _ := io.ReadAll(r) // if this fails, data is empty — caller doesn't know
> ```
>
> **Right:**
> ```go
> if err := os.Remove(tempFile); err != nil {
>     log.Printf("cleanup: remove %s: %v", tempFile, err)
>     // decide: return the error, log it, or handle it — but don't ignore it
> }
> ```
>
> **Why this matters:** Go's `errcheck` linter flags unchecked errors. In production, swallowed errors produce mysterious behavior — a file that should have been deleted wasn't, a connection that should have been closed wasn't.

> [!WARNING]
> **Anti-pattern 2: Logging and returning the same error**
>
> If you log an error and then return it, every layer of the call stack may log it again. The result is three copies of the same error in your logs at different times, making it impossible to trace the actual call site.
>
> **Wrong:**
> ```go
> func readUser(id int) (User, error) {
>     u, err := db.GetUser(id)
>     if err != nil {
>         log.Printf("readUser: %v", err) // logged here
>         return User{}, err              // AND returned to be logged again
>     }
>     return u, nil
> }
> ```
>
> **Right — choose one:**
> ```go
> // Option A: wrap and return (let the top-level handler log)
> return User{}, fmt.Errorf("readUser %d: %w", id, err)
>
> // Option B: log and return a generic error (at a boundary, hide internals)
> log.Printf("readUser %d: %v", id, err)
> return User{}, ErrInternal
> ```

> [!WARNING]
> **Anti-pattern 3: The typed-nil error trap**
>
> A function that returns a non-nil interface value whose underlying concrete value is nil will NOT satisfy `err == nil`, even though the underlying pointer is nil. This is one of Go's most surprising behaviors.
>
> **Wrong:**
> ```go
> func mayFail() error {
>     var e *MyError // nil pointer of type *MyError
>     if somethingFailed {
>         e = &MyError{...}
>     }
>     return e // WRONG: returns (*MyError)(nil) — a non-nil interface with nil data
> }
>
> // Caller:
> if err := mayFail(); err != nil { // TRUE even when nothing failed!
>     // This branch runs unexpectedly
> }
> ```
>
> **Right:**
> ```go
> func mayFail() error {
>     if somethingFailed {
>         return &MyError{...}
>     }
>     return nil // return untyped nil — the interface's nil value
> }
> ```
>
> **Why this happens:** An interface value is `nil` only when both its type and value are nil. `(*MyError)(nil)` has type `*MyError` and value nil — the type field is non-nil, so the interface is non-nil.

**Other pitfalls:**

- **Over-wrapping** — adding `"error:"` or `"failed:"` to every wrap prefix produces `"error: error: error: division by zero"`; use the operation or context name instead: `"parseConfig: readLine: …"`
- **Using `panic` for expected failures** — input validation errors, missing files, or network timeouts are expected; returning `error` is correct; `panic` is for programmer errors and invariant violations
- **Wrapping sentinel errors with `%v` instead of `%w`** — `fmt.Errorf("read: %v", io.EOF)` creates a new opaque error; `errors.Is(err, io.EOF)` will return false; always use `%w` when you need the wrapped error to remain inspectable

---

## Mental Models

### Mental Model 1: Errors as Return Values on a Conveyor Belt

Imagine a factory conveyor belt where each station takes in raw material, processes it, and passes the result to the next station. If a station finds a defect, it sends the defect report back up the line — but wraps it in a note that says "I found this at station 3 while doing step X." Each station adds its note before passing it back.

This is how Go error wrapping works: the bottom of the call stack creates the raw error, each caller wraps it with its own context, and the top of the stack receives a fully annotated chain. `errors.Is` and `errors.As` unwrap the chain to find what they need.

This model breaks down for `panic` — a panic is not a defect note being passed back; it is a fire alarm that stops the entire line.

### Mental Model 2: Errors.Is as a Chain Search

Think of an error chain as a linked list: `head → link1 → link2 → tail`. `errors.Is(err, target)` asks: "Is `target` anywhere in this list?" It walks the list from head to tail using `errors.Unwrap` until it either finds the target or reaches nil.

`errors.As` does the same walk but instead asks: "Is there a node of this type anywhere in the list?" and fills in a pointer to the first match it finds.

This model makes the traversal concrete: if you use `%v` instead of `%w` when wrapping, you cut the linked list — the new error has no `Unwrap` method, so `errors.Is` stops there and cannot see further back.

### Mental Model 3: Panic as a Ejector Seat

`panic` is an ejector seat: it is there for situations where continuing in the plane would certainly cause worse damage than ejecting right now. The ejector seat (recover in a deferred function) catches you before you hit the ground, but you are no longer flying the plane.

Normal error handling is the cockpit's normal controls. Use those for every routine and expected failure. Reserve the ejector seat for genuinely catastrophic situations — a nil pointer dereference, an index out of bounds, a violated invariant. Even then, only use it knowingly; in most code, the runtime will panic for you on those cases, and you only need `recover` at boundary points to prevent crashes from propagating.

> [!NOTE]
> Use Model 1 (conveyor belt) to reason about wrapping context and error chains. Use Model 2 (linked list) to understand what `errors.Is` and `errors.As` actually traverse. Use Model 3 (ejector seat) to calibrate when `panic` is appropriate.

---

## Practical Examples

### Example 1: Wrapping Errors Across Call Layers _(Basic)_

**Scenario:** A config loader reads a YAML file, and the error chain should tell the caller exactly what went wrong and where.

**Goal:** Show how `fmt.Errorf` with `%w` builds a readable error message across three call layers.

```go
package main

import (
    "errors"
    "fmt"
    "os"
)

// parseYAML simulates a YAML parser error
func parseYAML(data []byte) error {
    // pretend we found a syntax error on line 42
    return &ParseError{Line: 42, Message: `unexpected token "}"`}
}

// ParseError carries structured information about a parse failure
type ParseError struct {
    Line    int
    Message string
}

func (e *ParseError) Error() string {
    return fmt.Sprintf("line %d: %s", e.Line, e.Message)
}

// readConfig wraps OS errors with context
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("readConfig %s: %w", path, err)
    }
    return data, nil
}

// loadConfig wraps readConfig and parse errors
func loadConfig(path string) error {
    data, err := readConfig(path)
    if err != nil {
        return fmt.Errorf("loadConfig: %w", err)
    }
    if err := parseYAML(data); err != nil {
        return fmt.Errorf("loadConfig %s: %w", path, err)
    }
    return nil
}

func main() {
    // Case 1: file not found — OS error wrapped through two layers
    if err := loadConfig("missing.yaml"); err != nil {
        fmt.Println("Error:", err)
        // Output: loadConfig: readConfig missing.yaml: open missing.yaml: no such file or directory
    }

    // Case 2: parse error on existing file
    // (write a temp file to simulate)
    _ = os.WriteFile("/tmp/bad.yaml", []byte("bad content"), 0644)
    if err := loadConfig("/tmp/bad.yaml"); err != nil {
        fmt.Println("Error:", err)
        // Output: loadConfig /tmp/bad.yaml: line 42: unexpected token "}"

        // Inspect the chain for the structured ParseError
        var pe *ParseError
        if errors.As(err, &pe) {
            fmt.Printf("Parse failure at line %d\n", pe.Line)
        }
    }
}
```

**What to notice:** Each layer wraps with `%w`, preserving the chain. `errors.As` finds `*ParseError` anywhere in the chain. The error message reads like a stack trace in plain English.

---

### Example 2: Sentinel Errors and errors.Is _(Intermediate)_

**Scenario:** A key-value store returns different errors for different conditions. Callers need to distinguish "key not found" from "permission denied".

```go
package main

import (
    "errors"
    "fmt"
)

// Package-level sentinel errors — exported for callers to match against
var (
    ErrNotFound   = errors.New("key not found")
    ErrPermission = errors.New("permission denied")
)

// Store is a simple in-memory key-value store
type Store struct {
    data     map[string]string
    readOnly bool
}

func NewStore(readOnly bool) *Store {
    return &Store{data: map[string]string{"hello": "world"}, readOnly: readOnly}
}

func (s *Store) Get(key string) (string, error) {
    v, ok := s.data[key]
    if !ok {
        return "", fmt.Errorf("Get %q: %w", key, ErrNotFound)
    }
    return v, nil
}

func (s *Store) Set(key, val string) error {
    if s.readOnly {
        return fmt.Errorf("Set %q: %w", key, ErrPermission)
    }
    s.data[key] = val
    return nil
}

func main() {
    store := NewStore(true) // read-only

    // Get a missing key
    _, err := store.Get("missing")
    fmt.Println(errors.Is(err, ErrNotFound))   // true
    fmt.Println(errors.Is(err, ErrPermission)) // false
    fmt.Println(err) // Get "missing": key not found

    // Try to write to a read-only store
    err = store.Set("foo", "bar")
    fmt.Println(errors.Is(err, ErrPermission)) // true
    fmt.Println(err) // Set "foo": permission denied
}
```

**What to notice:** `errors.Is` works even though the errors are wrapped with `fmt.Errorf %w`. The caller can react differently to different sentinels. Direct `== ErrNotFound` comparison would fail here because the returned error is a wrapped value, not `ErrNotFound` itself.

---

### Example 3: Custom Error Type with errors.As _(Applied)_

**Scenario:** An HTTP client returns errors with the status code embedded so callers can branch on it.

```go
package main

import (
    "errors"
    "fmt"
    "net/http"
)

// HTTPError carries the status code from a failed HTTP response
type HTTPError struct {
    StatusCode int
    Status     string
    URL        string
}

func (e *HTTPError) Error() string {
    return fmt.Sprintf("HTTP %d %s fetching %s", e.StatusCode, e.Status, e.URL)
}

// fetch simulates an HTTP call that may fail
func fetch(url string) error {
    // Simulate a 404
    resp := &http.Response{StatusCode: 404, Status: "404 Not Found"}
    if resp.StatusCode >= 400 {
        return fmt.Errorf("fetch: %w", &HTTPError{
            StatusCode: resp.StatusCode,
            Status:     resp.Status,
            URL:        url,
        })
    }
    return nil
}

func main() {
    err := fetch("https://example.com/api/user/999")
    if err == nil {
        fmt.Println("success")
        return
    }

    // Check for a structured HTTPError anywhere in the chain
    var he *HTTPError
    if errors.As(err, &he) {
        switch he.StatusCode {
        case 404:
            fmt.Printf("Not found: %s\n", he.URL)
        case 403:
            fmt.Println("Access denied")
        default:
            fmt.Printf("HTTP error %d: %s\n", he.StatusCode, he.Status)
        }
    } else {
        fmt.Printf("Non-HTTP error: %v\n", err)
    }
}
```

**Output:**
```
Not found: https://example.com/api/user/999
```

**What to notice:** `errors.As` finds the `*HTTPError` inside the wrapped error. The caller can branch on `StatusCode` without the error being a sentinel. The `fetch` function adds its own wrapping layer (`"fetch: ..."`) but `errors.As` traverses it.

---

### Example 4: Panic/Recover at a Boundary _(Edge Case)_

**Scenario:** A pluggable handler system needs to recover from panics in user-provided handlers without crashing the host process.

```go
package main

import (
    "fmt"
    "runtime/debug"
)

// Handler is a user-provided function that might panic
type Handler func(input string) string

// SafeRun wraps a Handler invocation, recovering from any panic
func SafeRun(h Handler, input string) (result string, err error) {
    defer func() {
        if r := recover(); r != nil {
            // r is whatever was passed to panic()
            err = fmt.Errorf("handler panicked: %v\n%s", r, debug.Stack())
        }
    }()
    // If h panics, the deferred func above intercepts it and sets err
    result = h(input)
    return
}

func main() {
    // A well-behaved handler
    good := func(s string) string { return "processed: " + s }

    // A handler that panics (simulating a bug in user code)
    bad := func(s string) string {
        var m map[string]string
        return m["key"] // panics: assignment to entry in nil map (actually read here, nil ptr)
        // Actually: reading from nil map returns zero value — use index OOB instead:
    }
    // Simpler panic-inducing handler:
    panicky := func(s string) string {
        panic("something went terribly wrong")
    }

    // Safe invocations
    if result, err := SafeRun(good, "hello"); err != nil {
        fmt.Println("error:", err)
    } else {
        fmt.Println(result) // processed: hello
    }

    _ = bad // suppress unused warning

    if _, err := SafeRun(panicky, "hello"); err != nil {
        // err contains the panic value + stack trace
        fmt.Println("Recovered from panic in handler")
        fmt.Println("Error type: wrapped panic")
    }
}
```

**Output:**
```
processed: hello
Recovered from panic in handler
Error type: wrapped panic
```

**Why this is important:** The process does not crash. The panic in `panicky` is caught by `SafeRun`'s deferred `recover`, converted to an `error`, and returned normally. The host loop continues with the next invocation. This is the canonical pattern for plugin systems, HTTP middleware, and any code that runs user-provided callbacks.

---

## Related Concepts

Within this topic:

- [[go/6. Methods and Interfaces]] — `error` is an interface; implementing it correctly, understanding nil interface values, and structural typing are all directly relevant to every custom error type
- [[go/3. Functions]] — multiple return values, named returns, defer, and closures are the mechanical building blocks error handling is assembled from
- [[go/9. Concurrency]] — in concurrent programs, errors from multiple goroutines must be collected and returned together; `errors.Join` and channel-based error aggregation connect directly to concurrency patterns

In other topics:

- [[go/13. Web Services and APIs]] — the `recover`-in-middleware pattern shown in the panic/recover section is fully developed there, alongside HTTP error responses and status code conventions
- [[go/11. Testing and Benchmarking]] — testing error paths, using `errors.Is` in assertions, and table-driven tests for error conditions build directly on the types introduced here

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Sentinel Error and errors.Is** _(Easy)_
>
> Define two package-level sentinel errors. Write a function that returns one of them based on input. Verify that `errors.Is` works correctly on the wrapped result — and that `==` does not.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-sentinel-error-and-errorsis--easy--1-pt)

The exercises build from basic sentinel usage through custom error types, wrapping chains, and a final panic/recover exercise.

---

## Test

When you feel ready, take the self-assessment: [TEST.md](./TEST.md)

**Test overview:**
- Section 1: Recall (5 questions, 1 pt each)
- Section 2: Conceptual Understanding (3 questions, 2 pts each)
- Section 3: Applied / Practical (2 questions, 3 pts each)
- Section 4: Scenario / Debugging (1 question, 3 pts)
- Section 5: Discussion (1 question, 2 pts)
- Section 6: Bonus Challenge (1 question, 5 pts bonus)

**Passing:** ≥ 70% of non-bonus points (≥ 15/22). Aim for ≥ 80% (≥ 18/22).

---

## Projects

See the topic-level [PROJECTS.md](../PROJECTS.md) for project ideas.

**Recommended project after this module:**
Config Loader CLI — write a command-line tool that reads a YAML or JSON config file. Use custom error types to distinguish parse errors from file-not-found errors. Add a recovery boundary in the main function. Return structured errors to the user with enough context to diagnose any failure.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Error handling and Go — The Go Blog](https://go.dev/blog/error-handling-and-go)** — Andrew Gerrand's 2011 post; still the canonical introduction to Go's errors-as-values philosophy, the `error` interface, and custom error types
2. **[Working with Errors in Go 1.13 — The Go Blog](https://go.dev/blog/go1.13-errors)** — Official post introducing `%w`, `errors.Is`, `errors.As`, and `errors.Unwrap`; the reference for all Go 1.13+ error wrapping features
3. **[Effective Go — Errors](https://go.dev/doc/effective_go#errors)** — The idiomatic Go style guide's section on error handling; covers `error` interface, custom types, and formatting conventions
4. **[pkg.go.dev/errors](https://pkg.go.dev/errors)** — The standard library `errors` package documentation; includes `New`, `Is`, `As`, `Unwrap`, and `Join` with examples
5. **"The Go Programming Language" by Donovan & Kernighan — Chapter 5.4 (Errors) and Chapter 5.9 (Panic), Chapter 5.10 (Recover)** — The definitive Go book; Chapter 5 covers error handling and panic/recover in depth
6. **"Learning Go" by Jon Bodner (2nd ed.) — Chapter 9** — Modern treatment including Go 1.13 wrapping, `errors.Join`, and idiomatic error handling patterns; highly practical

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 8

**What I covered today:**
- Read the Overview and Why This Matters sections
- Worked through Core Concepts up to (concept name here)

**What clicked:**
- _Something that made sense_

**What's still unclear:**
- _Something that's still fuzzy — add to QUESTIONS.md_

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

**Test score:** _Not taken yet_

---

_Add new entries above this line._
