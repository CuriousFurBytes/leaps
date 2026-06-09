# Module 1: Types and Variables

[← Module 0: Introduction](../0.%20Introduction/) | [Topic Home](../README.md) | [Module 2: Control Flow →](../2.%20Control%20Flow/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-brightgreen)
![Time](https://img.shields.io/badge/time-3--4h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Basic Types](#basic-types)
  - [Zero Values](#zero-values)
  - [Variable Declaration](#variable-declaration)
  - [Constants and iota](#constants-and-iota)
  - [Type Conversion](#type-conversion)
  - [Type Inference with :=](#type-inference-with-)
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

This module covers **Go's type system, variable declaration, constants, and type conversion**. Go is a statically typed, compiled language, which means every variable has a fixed type that is known at compile time. This is one of the most important properties of the language — and understanding it deeply will save you from many bugs.

By the end of this module, you will have a solid understanding of how Go thinks about values: what types exist, how variables are declared, how the compiler infers types, what happens when you don't initialize a variable, and how to safely convert between types. This forms the foundation for every Go program you will ever write.

**Difficulty:** Beginner &nbsp;|&nbsp; **Estimated time:** 3–4 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Name Go's built-in primitive types and explain the difference between them — _given a use case, choose the right type_
2. Explain what zero values are and why every type has one — _predict the zero value of any primitive type without running code_
3. Declare variables using all three forms (`var` with type, `var` with inference, `:=`) and know when each is appropriate — _write idiomatic Go variable declarations_
4. Define constants and constant blocks using `iota` — _implement enumerated sets of values in Go_
5. Perform explicit type conversion correctly and explain why Go requires it — _convert between numeric types without data loss surprises_

---

## Prerequisites

### Required Modules

- [[go/0. Introduction]] — you need to understand: how to run a Go program, the structure of a `main` package, and basic use of `fmt.Println`

### Required Concepts

- **Variables** — the concept of a named storage location that holds a value; what assignment means
- **Functions** — you need to recognize that `:=` is only valid inside function bodies
- **Basic terminal usage** — running `go run main.go` from the command line

> [!TIP]
> If any of these prerequisites feel shaky, spend 15–30 minutes reviewing them before continuing.
> Gaps in prerequisites compound — a small weakness here will cause bigger confusion later.

---

## Why This Matters

Go's type system is not an obstacle — it is a tool. A precise type system catches bugs at compile time that would otherwise silently corrupt data at runtime. Every production Go program you read, write, or maintain depends on the concepts in this module.

Concretely, mastery of this module enables you to:

- **Read and write any Go variable declaration** — production Go code uses all three declaration forms; recognizing them on sight is non-negotiable
- **Avoid silent data corruption** — integer overflow, implicit conversions, and uninitialized variables are the source of subtle bugs; this module shows you exactly how Go handles each
- **Design clear APIs** — choosing `int64` vs `int`, `float64` vs `float32`, `byte` vs `rune` sends a signal to anyone reading your code about what the values represent and how large they can be

Without understanding Go's type system, you would be unable to write correct numeric code, define enumerated constants, or understand any non-trivial Go program — which means every subsequent module builds directly on this one.

---

## Historical Context

Go was designed at Google in **2007** by **Robert Griesemer, Rob Pike, and Ken Thompson**, and publicly released in 2009. The designers were frustrated with the state of systems programming. C++ compile times were unbearable on Google's large codebases. Dynamic languages like Python were expressive but too slow for infrastructure code. Java was verbose and carried too much ceremony.

Go's type system reflects deliberate design decisions that came from this frustration:

- **2007** — Initial design begins; Rob Pike and Ken Thompson bring experience from Plan 9 and Bell Labs; the decision to require explicit type conversion is made early to eliminate the class of bugs caused by C's implicit numeric promotions
- **2009** — Go is open-sourced; `iota` is present from day one, reflecting the designers' view that enumerations should not require a separate `enum` keyword
- **2012** — Go 1.0 is released, with a compatibility guarantee that the core type system will not change in breaking ways; the type system in this module is identical to what was shipped in Go 1.0

Understanding the history helps because the type system's strictness is a feature, not a limitation. Every rule that feels like friction — no implicit conversions, no unused variables, explicit zero values — is a deliberate trade: short-term verbosity for long-term correctness. The designers had seen what implicit conversions cost at scale. The type system is their answer.

---

## Core Concepts

### Basic Types

Go provides a rich set of built-in primitive types. Unlike some languages that offer only a handful of numeric types, Go gives you precise control over memory layout and value ranges. This matters in systems programming: a network protocol might specify a 16-bit unsigned integer, and Go lets you express that exactly.

**Integer types** come in signed and unsigned variants across four sizes:

| Type | Size | Range |
|------|------|-------|
| `int8` | 8 bits | -128 to 127 |
| `int16` | 16 bits | -32,768 to 32,767 |
| `int32` | 32 bits | -2,147,483,648 to 2,147,483,647 |
| `int64` | 64 bits | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `uint8` | 8 bits | 0 to 255 |
| `uint16` | 16 bits | 0 to 65,535 |
| `uint32` | 32 bits | 0 to 4,294,967,295 |
| `uint64` | 64 bits | 0 to 18,446,744,073,709,551,615 |
| `int` | 32 or 64 bits | platform-dependent |
| `uint` | 32 or 64 bits | platform-dependent |
| `uintptr` | large enough to hold a pointer | used in unsafe code |

The platform-dependent types `int` and `uint` are 32-bit on 32-bit systems and 64-bit on 64-bit systems. For most general-purpose code, `int` is what you want — it is the type integer literals default to when inferred. Use the sized types (`int32`, `int64`) when you need a guaranteed size, such as when serializing data or interfacing with external protocols.

**Floating-point types** follow IEEE 754:

- `float32` — 32-bit single precision (~6–7 significant decimal digits)
- `float64` — 64-bit double precision (~15–16 significant decimal digits); this is the default for floating-point literals

**Complex types** are built-in — unusual for a systems language:

- `complex64` — complex number with `float32` real and imaginary parts
- `complex128` — complex number with `float64` real and imaginary parts

**Boolean:** `bool` with values `true` and `false`. There is no numeric equivalent — `1` is not `true` in Go. This is a hard rule.

**String:** `string` is an immutable sequence of bytes, internally stored as UTF-8. Strings in Go are not null-terminated like in C. The length of a string is the number of bytes, not the number of Unicode characters. When you need to work with Unicode code points individually, you work with **runes**.

**Type aliases:**
- `byte` is an alias for `uint8`. Used when you're treating data as raw bytes — network payloads, file contents.
- `rune` is an alias for `int32`. Used when you're treating a value as a Unicode code point. The character 'A' is rune 65; the emoji '😀' is rune 128512.

```go
// Basic type examples
package main

import "fmt"

func main() {
    var x int = 42
    var f float64 = 3.14
    var s string = "hello"
    var b bool = true
    var r rune = 'A'       // rune literal uses single quotes
    var by byte = 255

    fmt.Println(x, f, s, b, r, by)
    // Output: 42 3.14 hello true 65 255
}
```

Note that a rune literal `'A'` prints as `65` because `rune` is just `int32` — it holds the Unicode code point value, not the character itself. To print the character, use `fmt.Printf("%c\n", r)`.

---

### Zero Values

One of Go's most pragmatic guarantees: **every variable is automatically initialized to its type's zero value if you don't provide one**. There is no such thing as an uninitialized variable in Go. This eliminates an entire category of bugs present in C and C++.

The zero values for the common types are:

| Type | Zero Value |
|------|-----------|
| `int`, `int8`, ..., `int64` | `0` |
| `uint`, `uint8`, ..., `uint64` | `0` |
| `float32`, `float64` | `0.0` |
| `complex64`, `complex128` | `(0+0i)` |
| `bool` | `false` |
| `string` | `""` (empty string) |
| pointer | `nil` |
| slice, map, channel, function | `nil` |

```go
package main

import "fmt"

func main() {
    var i int
    var f float64
    var s string
    var b bool

    fmt.Printf("int:     %v\n", i)     // int:     0
    fmt.Printf("float64: %v\n", f)     // float64: 0
    fmt.Printf("string:  %q\n", s)     // string:  ""
    fmt.Printf("bool:    %v\n", b)     // bool:    false
}
```

The key insight: zero values are not arbitrary. They were chosen to be the "safe" or "neutral" starting point for each type. A counter starts at zero. A flag starts at false. An accumulator string starts empty. In practice, this means you can write `var count int` and immediately use `count++` without a separate initialization step.

---

### Variable Declaration

Go provides three syntactic forms for declaring variables. Knowing when to use each form is part of writing idiomatic Go.

**Form 1: `var name type = value`** — the fully explicit form. Declares a variable with an explicit type and an explicit value.

```go
var age int = 30
var name string = "Alice"
var pi float64 = 3.14159
```

Use this form when you want the type to be clearly visible at the declaration site — especially useful when the type is not obvious from the value, or when you are declaring a package-level variable.

**Form 2: `var name = value`** — type is inferred from the value. The compiler determines the type at compile time; it is not dynamic.

```go
var age = 30         // inferred as int
var name = "Alice"   // inferred as string
var ratio = 0.5      // inferred as float64
```

The type is fixed at compile time — `age` is always `int`, not "any number." Type inference just saves you from writing the type explicitly when it is obvious.

**Form 3: `name := value`** — short variable declaration. Declares and assigns in one step. **Only valid inside function bodies.** This is the most common form in Go for local variables.

```go
func main() {
    age := 30           // int
    name := "Alice"     // string
    ratio := 0.5        // float64

    fmt.Println(age, name, ratio)
}
```

The `:=` operator must declare at least one new variable on the left side. You can use it when reassigning as long as one variable on the left is new:

```go
x, err := someFunc()     // both x and err are new
y, err := otherFunc()    // y is new; err is reassigned (ok)
```

**Multiple assignment** works with all forms:

```go
var a, b int = 1, 2
x, y := 10, "hello"
```

**Blank identifier** `_` discards a value you don't need:

```go
value, _ := strconv.Atoi("42")  // discard the error (not recommended in production)
```

```go
package main

import "fmt"

// Package-level: var with explicit type (Form 1)
var globalCount int = 0

func main() {
    // Form 1: explicit type
    var a int = 10

    // Form 2: inferred type
    var b = 20

    // Form 3: short declaration (most common for locals)
    c := 30

    // Multiple assignment
    x, y := 100, "hello"

    // Blank identifier
    _, remainder := 17/5, 17%5

    fmt.Println(a, b, c, x, y, remainder)
    // Output: 10 20 30 100 hello 2
}
```

---

### Constants and iota

Constants in Go are values that are fixed at compile time. Unlike variables, constants cannot be changed after declaration. They are evaluated entirely by the compiler — a constant expression like `60 * 60 * 24` is computed at compile time, not at runtime.

**Basic constant declaration:**

```go
const Pi = 3.14159          // untyped constant
const MaxUsers int = 100    // typed constant
const Greeting = "Hello"    // string constant
```

An **untyped constant** is more flexible than a typed one. `Pi` above is not `float64` — it is an untyped numeric constant with a value of 3.14159. It can be used in expressions with `float32` or `float64` without an explicit conversion because the conversion happens implicitly when the constant is used in context.

**Constant blocks with `iota`:**

`iota` is a special identifier that is only valid inside `const` blocks. It represents an auto-incrementing integer counter that starts at `0` in each new `const` block and increments by `1` for each constant in the block.

```go
const (
    Sunday    = iota  // 0
    Monday            // 1
    Tuesday           // 2
    Wednesday         // 3
    Thursday          // 4
    Friday            // 5
    Saturday          // 6
)
```

`iota` resets to `0` at the start of each `const` block — it is not global. Two separate `const` blocks each have their own `iota` starting at `0`.

**`iota` with expressions — permission flags:**

A common pattern is using `iota` with bit shifts to create non-overlapping bit flags:

```go
const (
    ReadPerm  = 1 << iota  // 1 << 0 = 1
    WritePerm              // 1 << 1 = 2
    ExecPerm               // 1 << 2 = 4
)
```

This works because each constant reuses the same expression (`1 << iota`) with the current value of `iota`. You can then combine flags with bitwise OR: `ReadPerm | WritePerm` equals `3`.

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

const (
    ReadPerm  = 1 << iota // 1
    WritePerm             // 2
    ExecPerm              // 4
)

func main() {
    fmt.Println("Tuesday is day", Tuesday) // Tuesday is day 2

    myPerms := ReadPerm | WritePerm
    fmt.Println("Read+Write permission value:", myPerms) // 3

    fmt.Println("Has read?", myPerms&ReadPerm != 0)   // true
    fmt.Println("Has exec?", myPerms&ExecPerm != 0)   // false
}
```

---

### Type Conversion

Go has **no implicit type conversion between numeric types**. If you want to use an `int` value where a `float64` is expected, you must convert explicitly. This is a deliberate design decision — implicit conversions in C are the source of countless bugs, and Go's designers chose to eliminate them entirely.

**Syntax:** `targetType(value)`

```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    var i int = 42
    var f float64 = float64(i)   // int → float64
    var u uint = uint(f)          // float64 → uint (truncates, does not round)

    fmt.Println(i, f, u) // 42 42 42

    // Precision loss when converting float to int
    var precise float64 = 3.99
    var truncated int = int(precise) // truncates toward zero, not rounds
    fmt.Println(truncated)           // 3, not 4

    // The string(int) gotcha
    n := 65
    fmt.Println(string(n))          // "A" — converts code point to character!
    fmt.Println(strconv.Itoa(n))    // "65" — converts integer to its decimal string representation
}
```

The `string(65)` gotcha is important: `string()` applied to an integer treats the integer as a Unicode code point, not as a decimal number. Code point 65 is the character 'A'. To get the string `"65"`, use `strconv.Itoa(65)` or `fmt.Sprintf("%d", 65)`.

---

### Type Inference with :=

When you use `:=` or `var name = value`, the compiler infers the type from the value. The rules are:

- Integer literals (e.g., `42`) default to `int`
- Floating-point literals (e.g., `3.14`) default to `float64`
- String literals default to `string`
- Boolean literals default to `bool`
- Rune literals (e.g., `'A'`) default to `rune` (= `int32`)

If you need a different type than the default, use an explicit conversion:

```go
x := 42          // int
y := int32(42)   // int32 — forced to a specific type
z := int64(42)   // int64

a := 3.14        // float64
b := float32(3.14) // float32 — some precision may be lost
```

Type inference does not mean dynamic typing. The type is determined at compile time and never changes. If `x := 42` infers `int`, then `x = "hello"` is a compile error — `x` is permanently an `int`.

---

### How the Concepts Fit Together

```
Basic Types (the vocabulary)
       │
       ▼
Zero Values  ──────────────►  Variable Declaration
(safe defaults)               (var / var= / :=)
                                      │
                                      ▼
                              Constants & iota
                              (compile-time values)
                                      │
                                      ▼
                              Type Conversion
                              (explicit bridges between types)
```

Types define what values are possible. Zero values mean every declared variable is immediately safe to use. The three declaration forms give you control over verbosity vs. conciseness. Constants extend the type system to compile-time invariants, and `iota` makes enumeration patterns painless. Type conversion is the explicit bridge when you need a value to move between types. Each concept builds on the previous one — you cannot understand conversion without understanding types, and you cannot appreciate zero values without knowing what types exist.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Using `:=` outside a function**
>
> The short variable declaration `:=` is only valid inside function bodies. Package-level variables must use `var`.
>
> **Wrong:**
> ```go
> package main
>
> name := "Alice"  // compile error: non-declaration statement outside function body
>
> func main() {
>     fmt.Println(name)
> }
> ```
>
> **Right:**
> ```go
> package main
>
> import "fmt"
>
> var name = "Alice"  // use var at package level
>
> func main() {
>     fmt.Println(name)
> }
> ```
>
> **Why this matters:** This is one of the most common errors for beginners coming from Python or JavaScript, where assignments at the top level are perfectly normal. In Go, `:=` is syntactic sugar for local variable declaration only.

> [!WARNING]
> **Mistake 2: Confusing `string(int)` with `strconv.Itoa(int)`**
>
> `string(n)` where `n` is an integer does not give you the decimal representation of `n`. It gives you the UTF-8 string for Unicode code point `n`.
>
> **Wrong:**
> ```go
> n := 65
> fmt.Println(string(n))  // prints "A", not "65"
> ```
>
> **Right:**
> ```go
> import "strconv"
>
> n := 65
> fmt.Println(strconv.Itoa(n))         // "65"
> fmt.Println(fmt.Sprintf("%d", n))    // "65" — alternative
> ```
>
> The underlying reason: in Go, `string(x)` converts a numeric value to its UTF-8 representation as a Unicode code point. This is a valid operation — `string(65)` is `"A"` because Unicode code point 65 is 'A'. But it is almost never what you want when you're trying to display a number.

> [!WARNING]
> **Mistake 3: Declaring a variable and not using it**
>
> Go's compiler treats an unused local variable as a **compile error**, not a warning.
>
> **Wrong:**
> ```go
> func main() {
>     x := 42
>     // x is never used — this will not compile
> }
> ```
>
> **Right:**
> ```go
> func main() {
>     x := 42
>     fmt.Println(x)  // use the variable
> }
> ```
>
> **Why this matters:** This is intentional. Unused variables are often symptoms of incomplete logic or copy-paste errors. The compiler forcing you to either use or explicitly discard (with `_`) every variable eliminates an entire class of subtle bugs.

**Other pitfalls:**

- **Integer overflow is silent** — Go does not panic on integer overflow; it wraps around. `var x int8 = 127; x++` gives `-128`, not a runtime error. Use larger types or add explicit range checks when overflow is a concern.
- **`int` size is platform-dependent** — code that assumes `int` is 64-bit may behave differently on 32-bit platforms. If you need a guaranteed 64-bit integer, use `int64` explicitly.

---

## Mental Models

The right mental model makes this module click. Here are the most useful ways to think about it:

### Mental Model 1: Zero Values as "Clean Slate"

Think of declaring a variable in Go like renting a freshly cleaned hotel room. In C, the room might be left in whatever state the previous guest left it — you might find garbage on the floor. In Go, the room is always cleaned before you check in. A freshly declared `int` is always `0`; a freshly declared `string` is always `""`. You never have to wonder "what was there before?"

This model breaks down when: you think about pointer types. A `nil` pointer's zero value means "points to nothing" — dereferencing it still panics. The clean slate applies to the pointer itself, not to what it might point to.

### Mental Model 2: Types as Documentation

Think of every type annotation as a contract between you and anyone who reads your code. `var userID int64` communicates: this value represents a user ID, it can be very large (up to 9 quintillion), and it is always a whole number. `var ratio float64` communicates: this value is a proportion or measurement where precision matters. `var name string` communicates: this is text.

This model is most useful when designing function signatures and struct fields — the types you choose document the expected values without any comments needed.

### Mental Model 3: `:=` as "Declare and Assign" Shorthand

Think of `:=` as two operations in one: type inference plus assignment. `x := 42` is exactly equivalent to writing `var x int = 42` — the compiler figures out `int` for you. The `:` in `:=` is the key: it signals that something new is being declared. Plain `=` only assigns; `:=` declares AND assigns.

This model breaks down when you try to use `:=` to redeclare an already-existing variable with no new variables on the left side — that is a compile error. At least one variable on the left must be new.

> [!NOTE]
> No single mental model is perfect. Use the "clean slate" model when thinking about initialization and safety. Use the "types as documentation" model when designing APIs and data structures. Use the "declare and assign" model when writing local function logic and choosing between `var` and `:=`.

---

## Practical Examples

### Example 1: Fibonacci Using Variables _(Basic)_

**Scenario:** You want to print the first 10 Fibonacci numbers.

**Goal:** Practice declaring and reassigning variables using multiple assignment.

```go
package main

import "fmt"

func main() {
    a, b := 0, 1

    fmt.Println("Fibonacci sequence:")
    for i := 0; i < 10; i++ {
        fmt.Println(a)
        a, b = b, a+b  // simultaneous assignment — no temp variable needed
    }
}
```

**Output / Result:**
```
Fibonacci sequence:
0
1
1
2
3
5
8
13
21
34
```

**What to notice:** `a, b = b, a+b` evaluates the right side completely before assigning to the left side. Both `b` and `a+b` are computed using the old values of `a` and `b`. This is simultaneous assignment, not sequential — Go evaluates all right-hand-side expressions before performing any assignments.

---

### Example 2: Temperature Converter _(Intermediate)_

**Scenario:** You are building a weather data pipeline that receives temperatures in Celsius and must output Fahrenheit.

**Goal:** Practice `float64` arithmetic and type-safe variable declarations.

```go
package main

import "fmt"

func main() {
    // Formula: F = C * 9/5 + 32
    temperatures := [3]float64{0.0, 100.0, -40.0}

    fmt.Println("Temperature Conversions:")
    for _, celsius := range temperatures {
        fahrenheit := celsius*9.0/5.0 + 32.0
        fmt.Printf("%.2f°C = %.2f°F\n", celsius, fahrenheit)
    }
}
```

**Output / Result:**
```
Temperature Conversions:
0.00°C = 32.00°F
100.00°C = 212.00°F
-40.00°C = -40.00°F
```

**What to notice:** Using `9.0/5.0` rather than `9/5` is critical. `9/5` in Go is integer division, which evaluates to `1`, giving you the wrong answer. The `.0` suffix forces floating-point arithmetic. Also note `%.2f` in the format string for two decimal places.

---

### Example 3: Permission Flags Using iota _(Applied)_

**Scenario:** You are implementing a simple file permission system where permissions are represented as a bitmask.

**Goal:** Use `iota` with bit shifts to model non-overlapping flags.

```go
package main

import "fmt"

const (
    ReadPerm  = 1 << iota // 1
    WritePerm             // 2
    ExecPerm              // 4
)

func describe(perms int) {
    fmt.Printf("Permissions (%d): ", perms)
    if perms&ReadPerm != 0 {
        fmt.Print("read ")
    }
    if perms&WritePerm != 0 {
        fmt.Print("write ")
    }
    if perms&ExecPerm != 0 {
        fmt.Print("execute ")
    }
    fmt.Println()
}

func main() {
    readOnly := ReadPerm
    readWrite := ReadPerm | WritePerm
    all := ReadPerm | WritePerm | ExecPerm

    describe(readOnly)   // Permissions (1): read
    describe(readWrite)  // Permissions (3): read write
    describe(all)        // Permissions (7): read write execute
}
```

**Output / Result:**
```
Permissions (1): read 
Permissions (3): read write 
Permissions (7): read write execute 
```

**What to notice:** Each permission value is a power of two (1, 2, 4). This is why bitwise AND (`&`) can test individual flags without affecting others. `ReadPerm | WritePerm` is `3`, and `3 & ReadPerm` (= `3 & 1`) is `1` (non-zero = true), while `3 & ExecPerm` (= `3 & 4`) is `0` (false).

---

### Example 4: Integer Overflow Demonstration _(Edge Case)_

**Scenario:** What happens when you increment an `int8` past its maximum value?

```go
package main

import "fmt"

func main() {
    var x int8 = 127  // maximum value for int8
    fmt.Println("Before:", x)

    x++  // this does NOT panic — it wraps around silently
    fmt.Println("After x++:", x)  // -128

    // Unsigned overflow also wraps
    var u uint8 = 255  // maximum value for uint8
    u++
    fmt.Println("uint8(255)++:", u)  // 0
}
```

**Why this is important:** Go does not raise a runtime error on integer overflow — the value silently wraps around using modular arithmetic. `int8(127) + 1` becomes `-128` because the bit pattern that represents `128` as a two's-complement 8-bit value is the same as `-128`. This is consistent with how most CPUs handle integer arithmetic, but it means you are responsible for preventing overflow when it matters. For security-sensitive code or financial calculations, always use types large enough for your domain, or add explicit range checks.

---

## Related Concepts

Within this topic:

- [[go/0. Introduction]] — the previous module; provides the runtime environment for all the code in this module
- [[go/2. Control Flow]] — the next module; uses variables and types extensively in loop counters, conditional expressions, and switch statements
- [[go/3. Functions]] — where `:=` is used most heavily; understanding scope and multiple return values deepens your understanding of variable declaration

In other topics:

- Python — comparison: Python uses dynamic typing (types are attached to values, not variables), which trades compile-time safety for flexibility; understanding the contrast helps you see why Go's static typing is a deliberate choice and not just verbosity
- Python (Variables and Types) — Python's type system covers similar ground from a dynamic perspective; useful for comparison if you already know Python

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Zero Value Survey** _(Easy)_
>
> Declare variables of 5 different Go types using `var` with explicit types but no initial value. Print each variable and observe its zero value. Predict all zero values before running the code.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-zero-value-survey)

The exercises range from simple zero-value observation to building a custom enum type with a `String()` method. Complete at least the Easy and Medium exercises before taking the test.

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

**Recommended project after this module:** Unit Converter CLI — a command-line tool that converts between units (length, weight, temperature) using `float64` arithmetic, typed constants for unit names, and `iota` for unit families.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[A Tour of Go — Basics](https://go.dev/tour/basics/1)** — The official interactive tutorial; the "Basics" section covers types and variables exactly as presented in this module, with runnable in-browser examples
2. **[The Go Programming Language Specification — Types](https://go.dev/ref/spec#Types)** — The authoritative reference; dense but precise; use it to answer "exactly what are the rules?" questions
3. **[Effective Go — Constants](https://go.dev/doc/effective_go#constants)** — The official style guide's section on constants, including the `iota` pattern and when to use typed vs. untyped constants

For a complete resource list including books and courses, see [RESOURCES.md](./RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 1

**What I covered today:**
- Read the Overview and Why This Matters sections
- Worked through Core Concepts up to Variable Declaration

**What clicked:**
- _Something that made sense_

**What's still unclear:**
- _Something that's still fuzzy — add to QUESTIONS.md_

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

**Test score:** _Not taken yet_

---

_Add new entries above this line._
