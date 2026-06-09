# Module 2: Control Flow

[← Module 1: Types and Variables](../1.%20Types%20and%20Variables/) | [Topic Home](../README.md) | [Module 3: Functions →](../3.%20Functions/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner--intermediate-blue)
![Time](https://img.shields.io/badge/time-3--4h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [if / else](#if--else)
  - [for — Go's Only Loop](#for--gos-only-loop)
  - [switch](#switch)
  - [defer](#defer)
  - [goto](#goto)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes](#common-beginner-mistakes)
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

This module covers **Go's control flow constructs**: `if`/`else`, `for`, `switch`, `defer`, and `goto`. These are the mechanisms by which a Go program makes decisions, repeats work, and manages cleanup. Unlike many languages that accumulate loop keywords over time, Go made deliberate minimalist choices — one loop keyword (`for`) instead of three, a `switch` that does not fall through by default, and `defer` as a first-class cleanup primitive.

By the end of this module, you will have a solid understanding of how Go structures conditional logic, iteration, and deferred execution. This forms the foundation for all meaningful Go programs and is prerequisite knowledge for functions, error handling, and concurrency.

**Difficulty:** Beginner–Intermediate &nbsp;|&nbsp; **Estimated time:** 3–4 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Write `if`/`else` statements using Go's syntax, including the init-statement form — _given a function that returns a value and an error, handle it idiomatically_
2. Use all four forms of Go's `for` loop (classic, while-style, infinite, and range-based) — _rewrite any loop from another language in Go_
3. Write `switch` statements with comma-separated cases, expression-less switch, and type switch — _replace complex `if`/`else if` chains with readable switch blocks_
4. Explain what `defer` does, when deferred calls execute, and in what order — _use defer correctly to close files and release resources_
5. Identify and correct the four most common beginner mistakes in Go control flow — _read a code review and spot defer-in-a-loop and fallthrough bugs_

---

## Prerequisites

### Required Modules

- [[go/1. Types and Variables]] — you need to understand: Go's basic types (`int`, `string`, `bool`), variable declaration with `:=` and `var`, and how multiple return values work (since `if err != nil` is everywhere)
- [[go/0. Introduction]] — you need to understand: how to compile and run a Go program, the `package main` / `func main()` structure, and how to import packages like `fmt`

### Required Concepts

- **Variables and assignment** — understanding `:=` short declaration and `=` assignment; the init statement in `if` introduces a new variable with `:=`
- **Types and zero values** — knowing that `int` zero value is `0`, `bool` is `false`, and `string` is `""` matters when reading switch conditions
- **Multiple return values** — Go functions return `(value, error)` pairs; the idiomatic `if v, err := f(); err != nil` pattern is used throughout this module

> [!TIP]
> If any of these prerequisites feel shaky, spend 15–30 minutes reviewing them before continuing.
> Gaps in prerequisites compound — a small weakness here will cause bigger confusion later.

---

## Why This Matters

Control flow is the skeleton of every program. Without conditional branching, a program could only compute fixed results. Without loops, it could not process collections, retry operations, or implement algorithms. Without cleanup mechanisms, it would leak resources every time a function returned early.

Concretely, mastery of this module enables you to:

- **Write idiomatic Go error handling** — virtually every Go function returns an error as a second return value, and the `if v, err := f(); err != nil { return err }` pattern appears in nearly every non-trivial Go file you will ever read
- **Process data collections** — iterating over slices, maps, channels, and strings with `for range` is the standard way to consume data in Go; understanding rune vs byte iteration is critical for correct Unicode handling
- **Manage resources without leaks** — `defer f.Close()` placed immediately after opening a file guarantees cleanup regardless of how the function exits; this pattern prevents file handle and mutex leaks in production services

Without understanding Go's control flow, you would be unable to write real programs, handle errors, or work with any collection of data — capabilities that appear in every Go program beyond "Hello, World!".

---

## Historical Context

Go was designed at Google by **Robert Griesemer, Rob Pike, and Ken Thompson**, with initial design work beginning in **2007** and the first open-source release in **November 2009**. The language emerged from frustration with C++ and Java build times and complexity in large-scale server software.

The control flow design reflects the team's philosophy: **orthogonality over convenience**. Rather than having `while`, `do-while`, and `for` as separate keywords (as in C, Java, and Python), Go uses a single `for` keyword that subsumes all loop patterns. This was a deliberate choice to reduce the language's surface area.

Key moments in the development of Go's control flow:

- **2007** — Initial design; Rob Pike advocated for a minimal set of keywords, influenced by his experience with Plan 9 and Newsqueak
- **2009** — Go 1 pre-release; `defer` is present from the start, inspired by C++'s RAII (Resource Acquisition Is Initialization) but simpler to reason about
- **2012** — Go 1.0 release; the language specification's control flow section is essentially unchanged to this day — a testament to the solidity of the initial design
- **2022** — Go 1.18 introduces generics, but control flow is untouched; its design was already complete

Understanding the history helps because it explains *why* Go's choices differ from C, Python, and Java. When you wonder "why doesn't Go have a `while` loop?" or "why doesn't `switch` fall through?", the answer is always the same: the designers chose deliberate minimalism and safety over familiarity. These are not omissions — they are decisions.

---

## Core Concepts

### if / else

Go's `if` statement is syntactically close to C and Java, with two important differences: parentheses around the condition are **not required** (and `gofmt` will remove them if you add them), and braces around the body are **required** (unlike C, where `if (x) return;` is legal). These rules apply without exception.

The basic form is exactly what you expect:

```go
x := 42

if x > 0 {
    fmt.Println("positive")
} else if x < 0 {
    fmt.Println("negative")
} else {
    fmt.Println("zero")
}
```

What makes Go's `if` distinctive is the **init statement** — an optional statement that runs before the condition is evaluated. The variable declared in the init statement is scoped to the entire `if`/`else if`/`else` block and is not visible outside it. This is enormously useful for the `(value, error)` return pattern that dominates Go code:

```go
// if with init statement — v and err are scoped to this if block
if v, err := strconv.Atoi("42"); err == nil {
    fmt.Printf("Parsed: %d\n", v)
} else {
    fmt.Printf("Parse error: %v\n", err)
}
// v and err are NOT accessible here — they go out of scope
```

The init statement is separated from the condition by a semicolon. The pattern `if result, err := someFunc(); err != nil` is so common in Go that it is considered idiomatic — it keeps the variable tightly scoped to where it is used and avoids cluttering the outer function scope with intermediate variables.

**Go has no ternary operator.** There is no `x > 0 ? "positive" : "negative"` syntax. This was a deliberate choice by the Go authors: ternary operators tend to encourage writing complex expressions in a single line, which reduces readability. In Go, use an `if`/`else` statement. The verbosity is intentional.

```go
// There is no ternary. Write this:
var label string
if x > 0 {
    label = "positive"
} else {
    label = "negative"
}

// Not this (does not compile in Go):
// label := x > 0 ? "positive" : "negative"
```

---

### for — Go's Only Loop

Go has **exactly one loop keyword: `for`**. There is no `while`, no `do-while`, no `loop`, no `repeat-until`. All loop patterns are expressed using `for`. This sounds limiting but is not — the `for` keyword is flexible enough to cover every case, and the unification reduces cognitive overhead.

**Form 1: Classic C-style loop** — init; condition; post:

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

The init statement (`i := 0`) runs once before the loop starts. The condition (`i < 10`) is checked before each iteration. The post statement (`i++`) runs at the end of each iteration. Any of the three parts can be omitted — but if you omit all three, you get an infinite loop.

**Form 2: While-style loop** — condition only:

```go
n := 1
for n < 1000 {
    n *= 2
}
fmt.Println(n) // 1024
```

This is exactly a `while` loop from other languages. There is no `while` keyword — just `for` with only the condition.

**Form 3: Infinite loop** — no condition at all:

```go
for {
    line, err := readLine()
    if err != nil {
        break
    }
    process(line)
}
```

Use `break` to exit an infinite loop, `continue` to skip to the next iteration. An infinite loop with `break` is the idiomatic way to write `do-while` in Go (execute the body at least once, check condition at the end):

```go
// Simulating do-while: run at least once
for {
    attempt()
    if succeeded() {
        break
    }
}
```

**Form 4: Range-based loop** — iterating over collections:

```go
// Range over a slice: index and value
fruits := []string{"apple", "banana", "cherry"}
for i, v := range fruits {
    fmt.Printf("%d: %s\n", i, v)
}

// Range over a map: key and value (order is random)
scores := map[string]int{"Alice": 90, "Bob": 85}
for name, score := range scores {
    fmt.Printf("%s: %d\n", name, score)
}

// Range over a string: gives rune (Unicode code point), not byte
for i, r := range "Hello, 世界" {
    fmt.Printf("index %d: %c (%d)\n", i, r, r)
}
// Note: index jumps by more than 1 for multi-byte characters
```

The blank identifier `_` discards either the index or the value when you don't need it:

```go
for _, v := range fruits {   // discard index
    fmt.Println(v)
}
for i := range fruits {      // value implicitly discarded
    fmt.Println(i)
}
```

**Labeled break and continue** allow breaking out of nested loops without a flag variable:

```go
outer:
for i := 0; i < 5; i++ {
    for j := 0; j < 5; j++ {
        if i+j > 6 {
            break outer  // exits the outer loop entirely
        }
        fmt.Printf("(%d,%d) ", i, j)
    }
}
```

---

### switch

Go's `switch` has important differences from C, Java, and JavaScript. The most critical: **cases do not fall through by default**. In C, forgetting a `break` causes execution to spill into the next case — a notorious source of bugs. In Go, each case is implicitly terminated. This is the safe default.

**Basic switch:**

```go
day := "Tuesday"
switch day {
case "Monday", "Tuesday", "Wednesday", "Thursday", "Friday":
    fmt.Println("weekday")
case "Saturday", "Sunday":
    fmt.Println("weekend")
default:
    fmt.Println("unknown")
}
```

Cases can be comma-separated (`case "Saturday", "Sunday":` matches either value). The `default` case runs if no other case matches; it can appear anywhere in the switch, not just at the end.

**Explicit fallthrough:** To get C-style fall-through behavior, use the `fallthrough` keyword explicitly. Note that `fallthrough` transfers control unconditionally — the next case's condition is not checked.

```go
n := 2
switch n {
case 1:
    fmt.Println("one")
    fallthrough
case 2:
    fmt.Println("two or fell through from one")
    fallthrough
case 3:
    fmt.Println("three or fell through from two")
}
// For n=2, prints: "two or fell through from one" then "three or fell through from two"
```

**Switch with no condition** (switch-true idiom) — acts like an `if`/`else if` chain but is often more readable:

```go
score := 78
switch {
case score >= 90:
    fmt.Println("A")
case score >= 80:
    fmt.Println("B")
case score >= 70:
    fmt.Println("C")
default:
    fmt.Println("F")
}
```

**Switch with init statement** — just like `if`, a switch can have an init statement:

```go
switch os := runtime.GOOS; os {
case "linux":
    fmt.Println("Linux")
case "darwin":
    fmt.Println("macOS")
default:
    fmt.Printf("Other: %s\n", os)
}
```

**Type switch** — one of Go's unique features; tests the dynamic type of an interface value:

```go
func describe(i interface{}) string {
    switch v := i.(type) {
    case int:
        return fmt.Sprintf("integer: %d", v)
    case string:
        return fmt.Sprintf("string: %q", v)
    case bool:
        return fmt.Sprintf("boolean: %v", v)
    default:
        return fmt.Sprintf("unknown type: %T", v)
    }
}
```

In a type switch, `v` is typed to the matched type within each case — so `v` is an `int` in the `case int:` branch, a `string` in `case string:`, and so on. This is more powerful than a simple type assertion because it handles multiple types cleanly.

---

### defer

`defer` is one of Go's most distinctive features. A `defer` statement pushes a function call onto a stack; all deferred calls are executed when the surrounding function returns, in **LIFO (last-in, first-out) order** — the last `defer` statement executed is the first one called.

The canonical use case is resource cleanup: open a resource, immediately defer its close, then proceed with the function body. This guarantees cleanup even if the function returns early due to an error:

```go
func readFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()  // registered now; runs when readFile returns

    // read and process file contents
    // even if this code panics or returns early, f.Close() will be called
    data, err := io.ReadAll(f)
    if err != nil {
        return err
    }
    fmt.Printf("File contents: %s\n", data)
    return nil
}
```

Without `defer`, every early return would need its own `f.Close()` call, and it is easy to miss one. With `defer`, the cleanup is registered once, immediately after the resource is acquired.

**Arguments are evaluated immediately.** A deferred function's arguments are evaluated at the `defer` statement, not when the deferred function runs. This distinction matters:

```go
func demo() {
    i := 0
    defer fmt.Println(i)  // argument i is captured NOW as 0
    i = 42
    // prints 0, not 42 — because i was evaluated at the defer statement
}
```

**LIFO order** — useful for nested resource acquisition:

```go
func multipleDefers() {
    defer fmt.Println("first deferred — runs last")
    defer fmt.Println("second deferred — runs second")
    defer fmt.Println("third deferred — runs first")
    fmt.Println("body runs first")
}
// Output:
// body runs first
// third deferred — runs first
// second deferred — runs second
// first deferred — runs last
```

This LIFO order is not arbitrary — it mirrors the structure of nested resource acquisition. If you open file A, then open file B, then open file C, you typically want to close them in reverse order: C first, then B, then A. `defer` gives you that automatically.

**Deferred closures can read and modify named return values:**

```go
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
```

**Warning about defer in loops:** Do not use `defer` inside a loop if you need the deferred call to run at the end of each iteration — it will only run when the enclosing function returns. See Common Beginner Mistakes for the pattern that avoids this.

---

### goto

Go has a `goto` statement. It is rarely used — most Go code never needs it — but it exists for completeness and for low-level or machine-generated code.

`goto` jumps to a labeled statement within the same function:

```go
func search(data []int, target int) int {
    i := 0
loop:
    if i >= len(data) {
        return -1
    }
    if data[i] == target {
        goto found
    }
    i++
    goto loop
found:
    return i
}
```

Restrictions: `goto` cannot jump over variable declarations, and it cannot jump into a different block. In practice, any code using `goto` can usually be rewritten more clearly with `for`/`break`/`continue`. The Go community convention is to avoid `goto` except in generated code or when the alternative is genuinely more obscure.

---

### How the Concepts Fit Together

```
Program entry (main)
        │
        ▼
  Decision making ──────────────── if / else
        │                          switch (dispatch)
        │
        ▼
  Repetition ────────────────────── for (all loop forms)
        │                           range (collection iteration)
        │
        ▼
  Cleanup / ordering ──────────── defer (LIFO cleanup stack)
        │
        ▼
  (rare) Direct jump ──────────── goto (avoid except in generated code)
```

In practice, most Go functions combine these constructs naturally: a `for range` loop over a collection, with an `if err != nil` check inside the loop, a `defer` at the top for cleanup, and a `switch` for dispatching on a value. Each construct handles one orthogonal concern, and they compose without interference.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Expecting C-style fallthrough in switch**
>
> Programmers coming from C, Java, or JavaScript expect `switch` cases to fall through automatically. In Go, they do not — each case is independent by default.
>
> **Wrong (thinking this will print "two" for n=2, but it will also reach "three"):**
> ```go
> switch n {
> case 1:
>     fmt.Println("one")
>     fallthrough          // this is EXPLICIT and unconditional
> case 2:
>     fmt.Println("two")
>     fallthrough          // adds unintended behavior
> case 3:
>     fmt.Println("three")
> }
> ```
>
> **Right (to match multiple values, use comma-separated cases):**
> ```go
> switch n {
> case 1, 2:
>     fmt.Println("one or two")
> case 3:
>     fmt.Println("three")
> }
> ```
>
> **Why this matters:** Using `fallthrough` without fully understanding it produces hard-to-debug behavior because the next case runs regardless of its condition.

> [!WARNING]
> **Mistake 2: Using defer inside a loop expecting per-iteration cleanup**
>
> `defer` runs when the enclosing **function** returns, not when the current loop iteration ends. Placing `defer f.Close()` inside a loop means all the deferred closes accumulate and only run when the function returns — which can exhaust file descriptors long before that.
>
> **Wrong:**
> ```go
> func processFiles(paths []string) {
>     for _, path := range paths {
>         f, _ := os.Open(path)
>         defer f.Close()    // WRONG: runs when processFiles returns, not each iteration
>         process(f)
>     }
> }
> ```
>
> **Right (extract to a helper function, or use an anonymous function):**
> ```go
> func processFiles(paths []string) {
>     for _, path := range paths {
>         processOne(path)   // defer inside here runs when processOne returns
>     }
> }
>
> func processOne(path string) {
>     f, err := os.Open(path)
>     if err != nil {
>         return
>     }
>     defer f.Close()        // correct: runs when processOne returns
>     process(f)
> }
> ```

> [!WARNING]
> **Mistake 3: Expecting the init statement variable to be accessible outside the if block**
>
> The variable declared in an `if` init statement is scoped to the entire `if`/`else` block, not to the surrounding function.
>
> **Wrong:**
> ```go
> if x := compute(); x > 0 {
>     fmt.Println(x)
> }
> fmt.Println(x)  // compile error: undefined: x
> ```
>
> **Right (if you need x outside the block, declare it before the if):**
> ```go
> x := compute()
> if x > 0 {
>     fmt.Println(x)
> }
> fmt.Println(x)  // fine now
> ```

> [!WARNING]
> **Mistake 4: Iterating a string by byte when you need runes**
>
> `range` over a string gives Unicode code points (runes), not bytes. The index in a range-over-string is the byte position of the start of the rune, which can jump by 2, 3, or 4 for multi-byte characters. If you use a classic `for i := 0; i < len(s); i++` loop, `s[i]` gives you a raw byte — not a character — which corrupts multi-byte characters.
>
> **Wrong (for Unicode text):**
> ```go
> s := "café"
> for i := 0; i < len(s); i++ {
>     fmt.Printf("%d: %c\n", i, s[i])  // s[i] is a byte, not a rune — garbled output for 'é'
> }
> ```
>
> **Right:**
> ```go
> s := "café"
> for i, r := range s {
>     fmt.Printf("%d: %c\n", i, r)   // r is a rune — correct Unicode character
> }
> ```

**Other pitfalls:**

- **Forgetting braces on if/for/switch** — Go requires `{` on the same line as the keyword; putting `{` on the next line is a syntax error due to automatic semicolon insertion
- **Defer argument evaluation timing** — `defer fmt.Println(x)` captures the current value of `x`, not the future value; use a closure `defer func() { fmt.Println(x) }()` if you need the value at call time

---

## Mental Models

The right mental model makes this module click. Here are the most useful ways to think about it:

### Mental Model 1: `for` as the Swiss Army Knife

Go's `for` is a single tool with multiple modes, not multiple tools. Think of it as a Swiss Army knife: one handle, multiple blades. The `for init; cond; post` blade is the classic loop. The `for cond` blade is the while. The `for` blade with no condition is the infinite loop. The `for range` blade is iteration over collections.

Imagine a Swiss Army knife where each tool is a specialized loop keyword: `while`, `do`, `repeat`, `foreach`. You need to remember which blade does what. Go's approach is one blade that folds into different configurations — less to remember, same capabilities.

This model breaks down when comparing Go to languages with a `do-while` — Go's `for { ... break }` pattern requires understanding the infinite loop form first.

### Mental Model 2: `switch` as a Dispatch Table

Think of `switch` not as "fall-through branching" (C's model) but as a clean **dispatch table**: given an expression, route execution to exactly one case and stop. Each case is an independent destination, not a starting point that bleeds into the next.

This is most useful when you have more than three conditions — at that point, a chain of `if`/`else if` statements becomes hard to scan, while a `switch` makes the mapping from values to behaviors immediately visible. The switch-true form (no condition) makes this even more useful for range-based dispatch.

### Mental Model 3: `defer` as a Cleanup Registration

Think of `defer` not as "execute this later" but as "**register a cleanup obligation right now**". When you acquire a resource (open a file, lock a mutex, start a span), you immediately register the cleanup (`defer f.Close()`, `defer mu.Unlock()`, `defer span.End()`). The registration happens at the point of acquisition, in the same visual location — you never need to scan down to find where the cleanup is.

The LIFO order then makes sense: the last thing you acquired is the first thing you release, just as you would peel an onion from the outside in.

> [!NOTE]
> No single mental model is perfect. Use Model 1 (Swiss Army knife) when you need to choose a loop form. Use Model 2 (dispatch table) when deciding whether `switch` is cleaner than `if`/`else if`. Use Model 3 (cleanup registration) to remember where to place `defer` and understand its execution order.

---

## Practical Examples

### Example 1: FizzBuzz _(Basic)_

**Scenario:** A classic interview problem that exercises both `for` and `switch`.

**Goal:** Print numbers 1 to 30, replacing multiples of 3 with "Fizz", multiples of 5 with "Buzz", and multiples of both with "FizzBuzz".

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

**Output / Result:**
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
...
```

**What to notice:** The switch-true form (`switch { case ...: }`) reads like plain English — "in the case that i is divisible by 15, print FizzBuzz". Checking `i%15 == 0` first avoids the need to check both conditions in one case. The order of cases matters here.

---

### Example 2: Character Counting with Range _(Intermediate)_

**Scenario:** Count the characters in a string that contains emoji (multi-byte Unicode).

**Goal:** Demonstrate that `range` iterates over Unicode runes, and that the byte index can jump by more than 1 for multi-byte characters.

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    s := "Hello 🌍!"

    fmt.Printf("Byte length (len):      %d\n", len(s))
    fmt.Printf("Rune count:             %d\n", utf8.RuneCountInString(s))
    fmt.Println()
    fmt.Println("Range iteration (rune by rune):")

    for i, r := range s {
        fmt.Printf("  byte index %2d: %c  (U+%04X)\n", i, r, r)
    }
}
```

**Output / Result:**
```
Byte length (len):      11
Rune count:             8

Range iteration (rune by rune):
  byte index  0: H  (U+0048)
  byte index  1: e  (U+0065)
  byte index  2: l  (U+006C)
  byte index  3: l  (U+006C)
  byte index  4: o  (U+006F)
  byte index  5:    (U+0020)
  byte index  6: 🌍  (U+1F30D)
  byte index 10: !  (U+0021)
```

**What to notice:** The emoji `🌍` is a single rune at byte index 6, but the next character (`!`) is at byte index 10 — a jump of 4 bytes. The byte index advances by the byte width of each rune, not by 1. Using `len(s)` gives you bytes, not characters. For character count, use `utf8.RuneCountInString(s)` or `len([]rune(s))`.

---

### Example 3: File Reading with defer _(Applied)_

**Scenario:** Reading a file, using defer to guarantee the file handle is closed.

**Goal:** Show the defer-for-cleanup pattern in a realistic context.

```go
package main

import (
    "fmt"
    "io"
    "os"
)

func printFileContents(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("open %s: %w", path, err)
    }
    defer f.Close()  // guaranteed to run when printFileContents returns

    data, err := io.ReadAll(f)
    if err != nil {
        return fmt.Errorf("read %s: %w", path, err)
    }

    fmt.Printf("--- %s ---\n%s\n", path, data)
    return nil
}

func main() {
    if err := printFileContents("/etc/hostname"); err != nil {
        fmt.Fprintf(os.Stderr, "error: %v\n", err)
        os.Exit(1)
    }
}
```

**Output / Result:**
```
--- /etc/hostname ---
myhostname
```

**What to notice:** `defer f.Close()` is placed on the very next line after the successful `os.Open`. This tight pairing — acquire, then immediately defer release — is the Go idiom. Even if `io.ReadAll` returns an error and the function returns early, `f.Close()` will still run. The error from `os.Open` is handled *before* the defer is registered, so there is no risk of calling `Close()` on a nil file handle.

---

### Example 4: Nested Loops with Labeled Break _(Edge Case)_

**Scenario:** Breaking out of an outer loop from inside an inner loop, without a flag variable.

```go
package main

import "fmt"

func main() {
outer:
    for row := 1; row <= 5; row++ {
        for col := 1; col <= row; col++ {
            if row+col > 6 {
                fmt.Printf("\nStopped at row=%d, col=%d (sum=%d)\n", row, col, row+col)
                break outer  // exits the outer for loop entirely
            }
            fmt.Printf("(%d,%d) ", row, col)
        }
        fmt.Println()
    }
}
```

**Output / Result:**
```
(1,1) 
(2,1) (2,2) 
(3,1) (3,2) (3,3) 
(4,1) (4,2) 
Stopped at row=4, col=3 (sum=7)
```

**Why this is important:** Without the label, `break` would only exit the inner loop, and you would need a boolean flag to signal the outer loop to stop — messy and error-prone. The labeled break is Go's solution: it is precise, visible at the loop definition, and avoids the flag variable entirely. Labels are rare in Go code but worth knowing for the nested-loop case.

---

## Related Concepts

Within this topic:

- [[go/1. Types and Variables]] — control flow acts on values; understanding `int`, `string`, `bool`, and zero values is essential to writing correct conditions
- [[go/3. Functions]] — `defer` is deeply tied to function returns; named return values, `panic`/`recover`, and closures all interact with `defer`
- [[go/4. Error Handling]] — the `if v, err := f(); err != nil` pattern from this module is Go's core error-handling idiom, covered in depth in the next modules

In other topics:

- Python — comparison: Python has `if`/`elif`/`else` (similar), `for`/`while`/`do-while` (three keywords vs Go's one), and `with` for resource management (similar to `defer` but lexically scoped rather than function-scoped)
- [[go/0. Introduction]] — the historical context of Go's minimalist design philosophy applies across all control flow constructs

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Two Ways to Loop** _(Easy)_
>
> Write a classic `for` loop that prints numbers 1 to 10. Then rewrite the same loop using the while-style `for` (condition only, no init or post). Both programs must produce identical output.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-two-ways-to-loop--easy--1-pt)

The exercises range from warm-up recall questions to a full state machine implementation. Complete at least the Easy and Medium exercises before taking the test.

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

See the topic-level [PROJECTS.md](../PROJECTS.md) for project ideas, and find beginner projects relevant to this module's concepts under the Beginner section.

**Recommended project after this module:**
Word Frequency Counter — read a text file line by line, split each line into words, count occurrences using a map, and print the top 10 most frequent words. This exercise requires all four loop forms, `if` error handling, `switch` for edge cases, and `defer` for file cleanup.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[The Go Programming Language Specification — Statements](https://go.dev/ref/spec#Statements)** — The authoritative reference for `if`, `for`, `switch`, `defer`, and `goto` syntax and semantics; read the sub-sections on For statements, Switch statements, and Defer statements
2. **[A Tour of Go — Flow Control](https://go.dev/tour/flowcontrol/1)** — Interactive tour with runnable examples of every control flow construct; covers all forms of `for`, `if` with init statement, `switch`, and `defer`; best done in order (flowcontrol/1 through flowcontrol/13)
3. **[Defer, Panic, and Recover — The Go Blog](https://go.dev/blog/defer-panic-and-recover)** — Official blog post by Andrew Gerrand explaining `defer` semantics, LIFO order, argument evaluation, and interaction with `panic`/`recover`; the definitive source for understanding `defer`
4. **"The Go Programming Language" by Donovan & Kernighan — Chapter 1 and Chapter 5** — Chapter 1 introduces `for` and `if` in context; Chapter 5 covers `defer` alongside function values; this book is the standard Go reference text and is worth owning

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 2

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
