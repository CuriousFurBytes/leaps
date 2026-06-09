# Module 3: Functions

[← Module 2: Control Flow](../2.%20Control%20Flow/) | [Topic Home](../README.md) | [Module 4: Composite Types →](../4.%20Composite%20Types/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner--intermediate-blue)
![Time](https://img.shields.io/badge/time-4--5h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Function Declarations and Signatures](#function-declarations-and-signatures)
  - [Parameters and Call-by-Value](#parameters-and-call-by-value)
  - [Multiple Return Values](#multiple-return-values)
  - [Named Return Values and Naked Returns](#named-return-values-and-naked-returns)
  - [The error Return Value Idiom](#the-error-return-value-idiom)
  - [Variadic Functions](#variadic-functions)
  - [Functions as First-Class Values](#functions-as-first-class-values)
  - [Function Types](#function-types)
  - [Higher-Order Functions](#higher-order-functions)
  - [Anonymous Functions and Closures](#anonymous-functions-and-closures)
  - [Recursion](#recursion)
  - [defer Interaction with Named Returns](#defer-interaction-with-named-returns)
  - [Method Values vs Function Values](#method-values-vs-function-values)
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

This module covers **Go's function system** — one of the richest and most practically important parts of the language. Functions in Go are not merely named blocks of code: they are **first-class values** that can be stored in variables, passed as arguments, returned from other functions, and captured in closures. Every meaningful Go program depends on a deep understanding of how functions work.

By the end of this module, you will understand how Go functions are declared, how call-by-value works (and what that means for slices, maps, and pointers), how to return multiple values, how closures capture variables from their surrounding scope, how `defer` interacts with named return values, and how to write higher-order functions. You will also have a solid understanding of when these features help — and when they can surprise you.

This module forms the foundation for [[go/8. Error Handling]], [[go/9. Concurrency]] (where closures and function values appear everywhere), and [[go/6. Methods and Interfaces]] (where functions gain receivers).

**Difficulty:** Beginner–Intermediate &nbsp;|&nbsp; **Estimated time:** 4–5 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Declare Go functions with correct syntax, including parameter lists, return types, and multiple return values — _write a function that both parses input and returns a typed error_
2. Explain Go's call-by-value semantics, and predict exactly what changes and what does not change when a slice, map, or pointer is passed to a function — _trace a function call and explain why the caller does or does not see the modification_
3. Write functions with named return values; explain when naked returns are acceptable and when they should be avoided — _refactor a function to use named returns for documentation clarity without introducing naked-return bugs_
4. Write and use variadic functions including the `...` spread operator — _implement a `sum` function that accepts any number of integers and call it with a slice_
5. Assign functions to variables, pass them as arguments, and return them from functions — _implement a `filter` higher-order function and call it with multiple predicate functions_
6. Write closures and explain precisely what they capture; identify and fix the classic loop-variable capture pitfall — _debug a closure bug where all goroutines or callbacks print the same loop variable_
7. Explain how `defer` interacts with named return values and use it deliberately for cleanup and error wrapping — _write a function that uses a deferred closure to add context to all returned errors_

---

## Prerequisites

### Required Modules

- [[go/2. Control Flow]] — you need to understand: `defer` (basic usage and LIFO order), the `if v, err := f(); err != nil` pattern, and all forms of `for` (since closures and higher-order functions are often combined with loops)
- [[go/1. Types and Variables]] — you need to understand: Go's type system, `:=` short declaration, `const`, zero values, and the distinction between value types and reference types
- [[go/0. Introduction]] — you need to understand: `package main`, `func main()`, `import`, and how to compile and run a Go program

### Required Concepts

- **Call stack basics** — understanding that function calls push a stack frame and returns pop it; this is essential for understanding why call-by-value does not affect the caller's variables
- **Pointers (basic awareness)** — you don't need mastery (that's [[go/5. Pointers]]), but knowing that `*T` is a pointer to type `T` and that `&x` takes the address of `x` will help when we discuss why slices and maps behave differently from scalars under call-by-value
- **The `error` type** — introduced in [[go/1. Types and Variables]]; this module builds on it heavily; `error` is an interface with a single method `Error() string`, and `nil` means no error

> [!TIP]
> If the `if v, err := f(); err != nil` pattern from Module 2 still feels mechanical rather than intuitive, spend 15 minutes re-reading that section before continuing. Functions and error handling are inseparable in Go, and this module makes heavy use of that pattern.

---

## Why This Matters

Functions are the atomic unit of abstraction in Go. Every meaningful program is a composition of functions. But Go's function system has several features that are genuinely different from most languages — and understanding them unlocks idiomatic Go:

- **Multiple return values enable the error idiom** — Go has no exceptions. Instead, functions return `(result, error)` pairs. This design forces callers to consciously handle failure, making error paths visible and explicit. The entire Go standard library and every non-trivial Go program you will ever read uses this idiom.
- **First-class functions enable compositional design** — Passing functions as arguments is the foundation of Go's `sort.Slice`, `http.HandleFunc`, `http.Client` middleware chains, `testing` callbacks, and many other standard library APIs. Without understanding first-class functions, you cannot use most of Go's standard library effectively.
- **Closures are everywhere in concurrent code** — In Go's concurrency model ([[go/9. Concurrency]]), goroutines are typically launched as closures: `go func() { ... }()`. The closure captures variables from the surrounding scope. Understanding what closures capture — and the pitfalls when they capture loop variables — is mandatory for writing correct concurrent programs.
- **defer + named returns enable airtight cleanup** — The pattern of using a deferred closure to add context to all returned errors, or to unlock a mutex regardless of how a function returns, appears throughout production Go code. This module shows you how it works mechanically.

Without understanding functions, you cannot write real Go programs. Every module that follows this one — error handling, composite types, concurrency, interfaces — builds directly on the concepts covered here.

---

## Historical Context

Go's function design draws from two very different traditions: the **C tradition** (simple, value-based, explicit) and the **functional programming tradition** (first-class functions, closures, higher-order functions).

**Multiple return values** — one of Go's most distinctive features — were present from the beginning of Go's design in 2007. Rob Pike has described them as one of the decisions the team is most satisfied with. In C, multiple outputs require pointer parameters or out-variables, which are error-prone and hard to read. In Go, `return a, b` and `func f() (int, error)` are as natural as a single return. The `(value, error)` convention emerged organically from this capability: since returning two values costs nothing syntactically, returning an error alongside every result became the standard.

**First-class functions and closures** have been in Go since the beginning, inherited from the Plan 9 C dialect (alef) that Rob Pike worked on at Bell Labs in the 1980s and 90s. In alef and later Newsqueak, function values and closures were fundamental tools. Go carried this forward cleanly.

**The closure loop-variable bug** is a historical artifact that the Go community struggled with for over a decade. Before Go 1.22 (released February 2024), all loop iterations shared a single loop variable — a classic source of bugs in goroutines and deferred closures. **Go 1.22 changed this**: each iteration of a `for` loop now gets its own copy of the loop variable, eliminating the classic bug for most cases. This module covers both the old behavior (which you will encounter in pre-1.22 codebases) and the new Go 1.22+ behavior.

**Named return values** were present from Go 1.0. The Go community's view on naked returns has evolved: early Go code used them frequently; the current consensus in the broader Go community is that naked returns in long functions hurt readability and should be reserved for short functions (≤5 lines) where the names serve as documentation.

Key moments in the development of Go's function system:

- **2007** — Initial design; multiple return values and first-class functions established from day one
- **2009** — Open-source release; the `error` interface and the `(value, error)` return convention codified
- **2012** — Go 1.0 release; function semantics essentially unchanged for over a decade thereafter
- **2022** — Go 1.18 adds generics, enabling generic higher-order functions like `Filter[T any](...)`
- **2024** — Go 1.22 fixes the per-iteration loop variable scoping, resolving a decade-old source of closure bugs

---

## Core Concepts

### Function Declarations and Signatures

A Go function declaration has this form:

```go
func name(param1 type1, param2 type2) returnType {
    // body
}
```

When multiple consecutive parameters share the same type, the type can be written once:

```go
// Long form                     // Shorthand (same type)
func add(x int, y int) int {     func add(x, y int) int {
    return x + y                     return x + y
}                                }
```

Functions that return nothing omit the return type entirely (there is no `void` keyword in Go):

```go
func printBanner(title string) {
    fmt.Printf("=== %s ===\n", title)
}
```

The function signature is everything between `func` and the opening `{`: the name, parameter list, and return type. Understanding signatures precisely matters because in Go, a function's type (e.g., `func(int, int) int`) determines where it can be used — as a variable, as a higher-order function argument, etc.

> [!NOTE]
> Go functions are **not** methods. A method has a **receiver** — a special first parameter that binds the function to a type. Methods are covered in [[go/6. Methods and Interfaces]]. For now, all functions in this module are package-level functions with no receiver.

---

### Parameters and Call-by-Value

Go uses **call-by-value** for all function arguments. When you pass a value to a function, Go copies it. Changes the function makes to its parameter do not affect the caller's variable.

```go
package main

import "fmt"

func double(n int) {
    n = n * 2   // modifies the local copy only
    fmt.Printf("inside double: n = %d\n", n)
}

func main() {
    x := 5
    double(x)
    fmt.Printf("after double:  x = %d\n", x) // still 5
}
// Output:
// inside double: n = 10
// after double:  x = 5
```

This is simple for scalars. It gets subtle for **slices**, **maps**, and **pointers** — because these types are themselves values that contain a reference to underlying data.

**Slices:** A slice value is a three-word struct: a pointer to the backing array, a length, and a capacity. When you pass a slice to a function, Go copies that three-word struct. The copy points to the **same backing array**, so mutations to existing elements are visible to the caller — but `append` operations that grow the slice are not (because `append` may allocate a new backing array and update the copy's pointer, not the caller's).

```go
func modifySlice(s []int) {
    s[0] = 99       // modifies the backing array — caller sees this
    s = append(s, 100) // may allocate a new array — caller does NOT see this
}

func main() {
    nums := []int{1, 2, 3}
    modifySlice(nums)
    fmt.Println(nums) // [99 2 3] — element 0 changed, but 100 was NOT appended
}
```

**Maps:** A map value is a pointer to an internal hash table. Passing a map copies the pointer, so both the caller and the function look at the same hash table. Mutations (insertions, deletions, updates) in the function are visible to the caller:

```go
func addEntry(m map[string]int, key string, val int) {
    m[key] = val  // modifies the shared underlying hash table
}

func main() {
    scores := map[string]int{"Alice": 90}
    addEntry(scores, "Bob", 85)
    fmt.Println(scores) // map[Alice:90 Bob:85] — Bob was added
}
```

**Pointers:** To let a function modify a caller's scalar variable, pass a pointer to it:

```go
func doublePtr(n *int) {
    *n = *n * 2  // dereferences the pointer and modifies the original
}

func main() {
    x := 5
    doublePtr(&x)
    fmt.Println(x) // 10
}
```

> [!WARNING]
> The call-by-value rule is always in effect — it is just that for slices, maps, and pointers, the "value" being copied is itself a reference to underlying data. This is not an exception to call-by-value; it is call-by-value applied to reference-containing types. The distinction matters when you expect `append` inside a function to grow the caller's slice — it will not, unless you return the new slice or pass a `*[]int`.

---

### Multiple Return Values

Go functions can return multiple values. The return types are listed in parentheses after the parameter list:

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 3)
    if err != nil {
        fmt.Println("error:", err)
        return
    }
    fmt.Printf("10 / 3 = %.4f\n", result) // 10 / 3 = 3.3333
}
```

When you call a function with multiple return values, you must receive all of them (unless you discard with `_`):

```go
result, _ := divide(10, 3)   // discard the error (only acceptable when you're certain it won't occur)
_, err := divide(10, 0)      // discard the value, keep the error
```

Multiple return values are used throughout the Go standard library. The `(T, error)` pattern is so universal it has become Go's idiomatic substitute for exceptions. Other common multi-value patterns:

```go
// (ok bool) pattern — used by map lookup and type assertions
value, ok := myMap["key"]      // ok is false if key absent
n, err := fmt.Fprintf(w, "...")  // return (bytes written, error)

// Swap two values without a temporary variable
func swap(a, b int) (int, int) {
    return b, a
}
x, y = swap(x, y)
```

---

### Named Return Values and Naked Returns

Go allows you to give names to return values. The named values are declared as variables at the top of the function body and are initialized to their zero values:

```go
// Named return values — min and max are declared implicitly
func minMax(nums []int) (min, max int) {
    if len(nums) == 0 {
        return  // naked return: returns min=0, max=0 (zero values)
    }
    min, max = nums[0], nums[0]
    for _, n := range nums[1:] {
        if n < min {
            min = n
        }
        if n > max {
            max = n
        }
    }
    return  // naked return: returns current values of min and max
}
```

Named return values serve two legitimate purposes:

1. **Documentation** — the names describe what each return value means, making function signatures self-documenting: `func readConfig(path string) (cfg Config, err error)` is more informative than `func readConfig(path string) (Config, error)`
2. **defer + named returns interaction** — a deferred closure can read and modify named return values, enabling powerful error-wrapping patterns (covered below)

**Naked returns** — calling `return` without arguments, relying on the current values of named returns — are the controversial part. The Go community's current guidance: naked returns are acceptable only in very short functions where the behavior is obvious. In longer functions, they impede readability because the reader must scroll back to find the named return declarations to understand what a bare `return` actually returns.

> [!WARNING]
> **Avoid naked returns in functions longer than ~5 lines.** In a long function, a bare `return` in the middle or at multiple exit points makes the function hard to read and review. Write explicit `return min, max` even when using named returns. Keep the names for documentation; drop the naked returns.

```go
// Acceptable: very short, names serve as docs
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return
}

// Avoid: long function with multiple naked returns — hard to follow
func processData(data []byte) (result []byte, n int, err error) {
    if len(data) == 0 {
        return  // returns nil, 0, nil — OK but...
    }
    // ... 30 more lines ...
    if someCondition {
        return  // what does this return? reader must scroll to top
    }
    // ...
    return  // and this?
}
```

---

### The error Return Value Idiom

The `error` type is a built-in interface:

```go
type error interface {
    Error() string
}
```

By convention, **every function that can fail returns `error` as its last return value**. `nil` means success; a non-nil `error` describes the failure. This is Go's substitute for exceptions.

```go
import (
    "errors"
    "fmt"
    "strconv"
)

// parsePositive parses a string as a positive integer.
func parsePositive(s string) (int, error) {
    n, err := strconv.Atoi(s)
    if err != nil {
        return 0, fmt.Errorf("parsePositive: %w", err)  // wrap with context
    }
    if n <= 0 {
        return 0, fmt.Errorf("parsePositive: expected positive, got %d", n)
    }
    return n, nil
}
```

Three important conventions:

1. **Error last** — when a function returns multiple values, `error` is always last: `(T, error)`, never `(error, T)`
2. **Return zero on error** — when returning an error, return the zero value for other return types: `return 0, err`, `return nil, err`, `return "", err`
3. **Never ignore errors** — in Go, ignoring an error is a deliberate act using `_`. If you assign `result, _ := fn()`, you are saying "I know this can fail and I don't care." This should be rare and justified.

The `fmt.Errorf` with `%w` verb **wraps** an error, preserving it for `errors.Is` and `errors.As` unwrapping (covered in depth in [[go/8. Error Handling]]):

```go
err := fmt.Errorf("open config: %w", originalErr)
// err.Error() returns "open config: <original error message>"
// errors.Is(err, originalErr) returns true (it unwraps)
```

For creating simple errors without wrapping, use `errors.New`:

```go
var ErrNotFound = errors.New("not found")
```

---

### Variadic Functions

A **variadic function** accepts a variable number of arguments of a given type. The last parameter is prefixed with `...`:

```go
// sum accepts zero or more int arguments
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

func main() {
    fmt.Println(sum())          // 0
    fmt.Println(sum(1))         // 1
    fmt.Println(sum(1, 2, 3))   // 6
    fmt.Println(sum(1, 2, 3, 4, 5)) // 15
}
```

Inside the function, the variadic parameter (`nums`) is a slice. You can range over it, take its length, etc.

**Spreading a slice into a variadic call** — use `...` at the call site:

```go
nums := []int{1, 2, 3, 4, 5}
fmt.Println(sum(nums...))  // spreads the slice — same as sum(1, 2, 3, 4, 5)
```

The spread operator converts a slice into individual arguments. This is the Go equivalent of Python's `*args` unpacking.

`fmt.Println`, `fmt.Printf`, and `fmt.Sprintf` are all variadic — `fmt.Println` has signature `func Println(a ...any) (n int, err error)`. The `any` type (an alias for `interface{}`) means they accept any value.

> [!NOTE]
> Only the **last** parameter can be variadic. A function like `func f(a ...int, b string)` is a compile error. If you need a variadic parameter that is not last, the conventional Go approach is to either swap the parameter order or use a slice directly: `func f(b string, a []int)`.

---

### Functions as First-Class Values

In Go, functions are **first-class values**: they have a type, can be assigned to variables, passed as arguments, and returned from other functions. This is not a special feature — it follows from Go's type system treating function types like any other type.

```go
// A function assigned to a variable
greet := func(name string) string {
    return "Hello, " + name + "!"
}
fmt.Println(greet("Alice"))  // Hello, Alice!

// A function stored in a map (dispatch table)
ops := map[string]func(int, int) int{
    "add": func(a, b int) int { return a + b },
    "sub": func(a, b int) int { return a - b },
    "mul": func(a, b int) int { return a * b },
}
fmt.Println(ops["add"](3, 4)) // 7
fmt.Println(ops["mul"](3, 4)) // 12
```

Named functions (declared with `func name(...)`) can also be used as values — just reference the function name without calling it:

```go
func double(n int) int { return n * 2 }

transform := double  // transform is now a func(int) int
fmt.Println(transform(5)) // 10
```

---

### Function Types

Every function has a **type** that describes its signature. The type is written as `func(paramTypes) returnTypes`:

```go
// These are all of type func(int, int) int:
var adder func(int, int) int = func(a, b int) int { return a + b }
var multiplier func(int, int) int = func(a, b int) int { return a * b }

// Type aliases for readability
type BinaryOp func(int, int) int

var op BinaryOp = adder
fmt.Println(op(3, 4)) // 7
op = multiplier
fmt.Println(op(3, 4)) // 12
```

Function types are used in:
- **Higher-order function parameters**: `func apply(op func(int, int) int, a, b int) int`
- **Callbacks and handlers**: `http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) { ... })`
- **Struct fields**: `type Server struct { OnError func(error) }`

The zero value of a function type is `nil`. Calling a nil function panics:

```go
var f func(int) int
f(5) // panic: runtime error: invalid memory address or nil pointer dereference
```

Always check for nil before calling a function value that might not have been set:

```go
if callback != nil {
    callback(result)
}
```

---

### Higher-Order Functions

A **higher-order function** either accepts functions as arguments or returns a function (or both). Higher-order functions enable powerful compositional patterns without inheritance or generics.

**Accepting a function as an argument:**

```go
// filter returns a new slice containing only elements for which predicate returns true
func filter(nums []int, predicate func(int) bool) []int {
    var result []int
    for _, n := range nums {
        if predicate(n) {
            result = append(result, n)
        }
    }
    return result
}

// mapInts applies f to each element and returns a new slice
func mapInts(nums []int, f func(int) int) []int {
    result := make([]int, len(nums))
    for i, n := range nums {
        result[i] = f(n)
    }
    return result
}

func main() {
    nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    evens := filter(nums, func(n int) bool { return n%2 == 0 })
    fmt.Println(evens) // [2 4 6 8 10]

    doubled := mapInts(nums, func(n int) int { return n * 2 })
    fmt.Println(doubled) // [2 4 6 8 10 12 14 16 18 20]
}
```

**Returning a function (function factories):**

```go
// multiplier returns a function that multiplies its argument by factor
func multiplier(factor int) func(int) int {
    return func(n int) int {
        return n * factor  // factor is captured from the enclosing scope — this is a closure
    }
}

func main() {
    double := multiplier(2)
    triple := multiplier(3)

    fmt.Println(double(5))  // 10
    fmt.Println(triple(5))  // 15
    fmt.Println(double(triple(4))) // 24 (triple(4)=12, double(12)=24)
}
```

The standard library uses higher-order functions extensively:

```go
// sort.Slice uses a "less" function
sort.Slice(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})

// http.HandleFunc registers a handler function
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Hello, World!")
})
```

---

### Anonymous Functions and Closures

An **anonymous function** (also called a function literal) is a function without a name, written inline:

```go
add := func(a, b int) int {
    return a + b
}
fmt.Println(add(3, 4)) // 7

// Immediately invoked
result := func(x int) int { return x * x }(5)
fmt.Println(result) // 25
```

A **closure** is an anonymous function that references variables from its enclosing scope. The function "closes over" those variables — it captures them by reference, not by value. The captured variables live as long as the closure does:

```go
func makeCounter() func() int {
    count := 0              // count lives in the enclosing scope
    return func() int {
        count++             // captures and modifies count
        return count
    }
}

func main() {
    counter := makeCounter()
    fmt.Println(counter()) // 1
    fmt.Println(counter()) // 2
    fmt.Println(counter()) // 3

    // Each call to makeCounter creates a fresh count variable
    counter2 := makeCounter()
    fmt.Println(counter2()) // 1  (independent counter)
    fmt.Println(counter())  // 4  (first counter continues)
}
```

**The classic loop-variable capture pitfall:**

Before Go 1.22, all iterations of a `for` loop shared a single loop variable. A closure that captured the loop variable would, by the time it ran, see the variable's final value:

```go
// WRONG in Go < 1.22: all functions see the same variable i
funcs := make([]func(), 3)
for i := 0; i < 3; i++ {
    funcs[i] = func() { fmt.Println(i) }  // captures the variable i, not its value
}
for _, f := range funcs {
    f() // prints 3, 3, 3 — not 0, 1, 2
}
```

**Go 1.22 fix:** Starting with Go 1.22, each iteration of a `for` loop gets its own copy of the loop variable, so the above code works correctly (prints 0, 1, 2) in Go 1.22+.

**The pre-1.22 fix** (still needed for code that must run on older Go versions, and still seen in codebases predating 1.22):

```go
// Fix 1: shadow the variable inside the loop body
for i := 0; i < 3; i++ {
    i := i  // creates a new i scoped to this iteration's block
    funcs[i] = func() { fmt.Println(i) }
}

// Fix 2: pass the value as an argument to an immediately invoked function
for i := 0; i < 3; i++ {
    func(i int) {            // i here is a new parameter, not the loop variable
        funcs[i] = func() { fmt.Println(i) }
    }(i)
}
```

> [!WARNING]
> Even with Go 1.22's fix, the loop-variable capture pitfall still exists in `for range` over channels, and in any code that must maintain compatibility with Go < 1.22. Always be aware of what a closure captures and when it executes relative to the surrounding loop. The safest habit is to pass values explicitly as function arguments rather than relying on closure capture when correctness depends on having a per-iteration value.

---

### Recursion

Go supports recursion naturally. A function can call itself, and the stack grows dynamically (Go uses growable stacks, unlike C where the stack is fixed-size):

```go
// Factorial — classic recursive example
func factorial(n int) int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n-1)
}

// Fibonacci — shows why naive recursion can be slow
func fib(n int) int {
    if n <= 1 {
        return n
    }
    return fib(n-1) + fib(n-2) // exponential time — don't use in production
}

// Fibonacci with memoization — linear time
func fibMemo(n int, memo map[int]int) int {
    if n <= 1 {
        return n
    }
    if v, ok := memo[n]; ok {
        return v
    }
    result := fibMemo(n-1, memo) + fibMemo(n-2, memo)
    memo[n] = result
    return result
}
```

Go does **not** perform tail-call optimization (TCO). A deeply recursive function will eventually exhaust the available goroutine stack. For very deep recursion (thousands of levels), convert to an iterative algorithm or use an explicit stack. For typical recursion depths (tens to hundreds), Go's growable stacks (starting at 8KB, growing as needed) handle it fine.

Mutually recursive functions — where function A calls B and B calls A — are supported without forward declarations, because Go's type-checker processes the entire package before checking function bodies:

```go
func isEven(n int) bool {
    if n == 0 { return true }
    return isOdd(n - 1)
}

func isOdd(n int) bool {
    if n == 0 { return false }
    return isEven(n - 1)
}
```

---

### defer Interaction with Named Returns

This is one of Go's subtler features: a **deferred closure** (not a deferred function call, but a deferred `func() { ... }()`) can **read and modify** named return values. The modification happens after the function body has finished but before the function actually returns to its caller.

This enables a powerful error-wrapping pattern:

```go
// readConfig returns an error wrapped with the function name
func readConfig(path string) (cfg Config, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("readConfig %q: %w", path, err)
        }
    }()
    // ... read and parse the config ...
    // Any error returned here will be wrapped with "readConfig <path>: "
    return cfg, nil
}
```

This works because:
1. The function body runs; if it returns an error, `err` is set to a non-nil value
2. The deferred closure runs next, sees the non-nil `err`, and replaces it with a wrapped version
3. The (now-modified) `err` is what the caller receives

The mechanism: **named return values are variables that exist in the function's scope**. A deferred closure captures them by reference (just like any other closure). When the deferred closure runs (just before the function returns), it reads and modifies those variables, and those modifications are reflected in what the caller sees.

> [!NOTE]
> This only works with **closures** (anonymous functions with no arguments), not with deferred function calls with explicit arguments. `defer fmt.Println(err)` captures the value of `err` at the time the `defer` statement executes. `defer func() { fmt.Println(err) }()` captures a reference to `err` and reads it when the function returns.

---

### Method Values vs Function Values

In [[go/6. Methods and Interfaces]], you will learn that methods are functions with receivers. A **method value** is a function value bound to a specific receiver:

```go
type Counter struct{ n int }

func (c *Counter) Increment() { c.n++ }
func (c *Counter) Value() int { return c.n }

func main() {
    c := &Counter{}

    // Method value: inc is a func() bound to c
    inc := c.Increment
    inc()  // equivalent to c.Increment()
    inc()
    fmt.Println(c.Value()) // 2

    // Method expression: a function that takes the receiver as its first argument
    incExpr := (*Counter).Increment  // type: func(*Counter)
    incExpr(c)
    fmt.Println(c.Value()) // 3
}
```

Method values let you use methods anywhere a function value is expected — passing `c.Increment` to a goroutine, a callback, or a higher-order function is idiomatic Go.

This is a forward reference: full coverage of method receivers, interfaces, and when to use method values vs plain function values is in [[go/6. Methods and Interfaces]]. For now, the key insight is: **method values and function values are the same kind of thing** in Go's type system. A method value has the receiver already bound; a function value does not.

---

### How the Concepts Fit Together

```
Function declaration (signature, params, returns)
        │
        ▼
Call-by-value ──────────────────── scalars copied; slices/maps share backing data
        │
        ▼
Multiple return values ──────────── (result, error) is the universal Go idiom
        │
        ├── Named returns ────────── documentation + defer interaction
        │
        ▼
Variadic functions ──────────────── ...T parameter; slice spreading with ...
        │
        ▼
Functions as values ─────────────── assignable, passable, returnable
        │
        ├── Anonymous functions ──── func literals; immediately invokable
        │
        ├── Closures ────────────── capture variables by reference from enclosing scope
        │       └── Loop capture pitfall (fixed in Go 1.22)
        │
        └── Higher-order functions ─ accept or return function values
                │
                ▼
        Recursion ──────────────── self-referential; no TCO; growable stacks
        defer + named returns ───── deferred closures can modify return values
        Method values ───────────── functions bound to a receiver (→ Module 6)
```

In a real Go program, these concepts combine continuously: a higher-order function accepts a closure that references an outer variable; the closure returns a `(result, error)` pair; a deferred anonymous function wraps any returned error with context. Understanding each piece individually is necessary, but the real skill is seeing how they compose.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Expecting append inside a function to grow the caller's slice**
>
> Because slices are passed by value (the three-word struct is copied), `append` inside a function may allocate a new backing array and update the function's local copy of the slice header — but the caller's slice header is unchanged. The caller's slice does not grow.
>
> **Wrong (expecting s to be modified in-place):**
> ```go
> func addItem(s []int, item int) {
>     s = append(s, item)  // s is a local copy — caller doesn't see this
> }
>
> func main() {
>     nums := []int{1, 2, 3}
>     addItem(nums, 4)
>     fmt.Println(nums) // [1 2 3] — 4 was NOT added from the caller's perspective
> }
> ```
>
> **Right (return the new slice):**
> ```go
> func addItem(s []int, item int) []int {
>     return append(s, item)  // return the (possibly new) slice header
> }
>
> func main() {
>     nums := []int{1, 2, 3}
>     nums = addItem(nums, 4)  // reassign to capture the new slice
>     fmt.Println(nums) // [1 2 3 4]
> }
> ```
>
> **Why this matters:** This is the most common source of "my slice didn't grow" bugs in Go. The standard library convention is to return the modified slice, exactly as `append` itself does.

> [!WARNING]
> **Mistake 2: Loop-variable capture in closures (pre-1.22 behavior)**
>
> Before Go 1.22, all iterations of a `for` loop shared a single loop variable. Closures capturing that variable see its final value, not the value at the time the closure was created. Even in Go 1.22+, code in codebases with `go 1.21` or earlier in go.mod still exhibits this behavior.
>
> **Wrong (pre-1.22, or with go directive < 1.22):**
> ```go
> handlers := make([]func(), 5)
> for i := 0; i < 5; i++ {
>     handlers[i] = func() {
>         fmt.Println(i) // captures the variable i, not its value
>     }
> }
> for _, h := range handlers {
>     h() // prints 5, 5, 5, 5, 5 — not 0, 1, 2, 3, 4
> }
> ```
>
> **Right (works in all Go versions):**
> ```go
> for i := 0; i < 5; i++ {
>     i := i  // shadow i with a new per-iteration variable
>     handlers[i] = func() { fmt.Println(i) }
> }
> ```
>
> **Why this matters:** This bug is subtle and hard to spot in code review. In concurrent code (goroutines launched in a loop), it causes all goroutines to operate on the same variable — a data race and a logic error simultaneously.

> [!WARNING]
> **Mistake 3: Using naked returns in long functions**
>
> Named return values combined with naked `return` statements in functions longer than a few lines are a significant readability hazard. The reader must scroll back to the function signature to know what a bare `return` returns.
>
> **Wrong (for any non-trivial function):**
> ```go
> func processOrder(id int) (order Order, subtotal float64, tax float64, err error) {
>     order, err = fetchOrder(id)
>     if err != nil {
>         return  // returns Order{}, 0, 0, err — but you have to scroll up to know that
>     }
>     subtotal = computeSubtotal(order)
>     tax = subtotal * 0.08
>     return  // returns order, subtotal, tax, nil — invisible at a glance
> }
> ```
>
> **Right:**
> ```go
> func processOrder(id int) (order Order, subtotal float64, tax float64, err error) {
>     order, err = fetchOrder(id)
>     if err != nil {
>         return Order{}, 0, 0, err  // explicit — no ambiguity
>     }
>     subtotal = computeSubtotal(order)
>     tax = subtotal * 0.08
>     return order, subtotal, tax, nil  // explicit
> }
> ```

> [!WARNING]
> **Mistake 4: Calling a nil function value**
>
> The zero value of any function type is `nil`. Calling a nil function panics at runtime. This commonly occurs when a struct has a function field that was never set, or when a function variable was declared but not assigned.
>
> **Wrong:**
> ```go
> type Handler struct {
>     OnError func(error)
> }
>
> h := Handler{} // OnError is nil
> h.OnError(err) // panic: runtime error: nil function call
> ```
>
> **Right:**
> ```go
> if h.OnError != nil {
>     h.OnError(err)
> } else {
>     log.Println("unhandled error:", err)
> }
> ```

**Other pitfalls:**

- **Forgetting that error is the last return value** — writing `func f() (error, int)` instead of `func f() (int, error)` compiles but violates the universal Go convention; every caller in the ecosystem expects error last
- **Ignoring errors from deferred calls** — `defer f.Close()` discards any error returned by `Close()`; in critical code (writing to disk, committing a transaction), capture and check the error: `defer func() { if cerr := f.Close(); cerr != nil && err == nil { err = cerr } }()`

---

## Mental Models

### Mental Model 1: Functions are Values with a Shape

Think of every function as having a **shape**: its parameter types and return types. Two functions with the same shape (same parameter types, same return types, in the same order) have the same type and are interchangeable.

This is why `func(int, int) int` works as a type: it describes the shape. When you pass a function to another function, Go checks that the shapes match. When you store functions in a map, all values must have the same shape.

The mental model: a function's shape is like an electrical plug standard. Any plug that fits the socket works, regardless of what it does internally. `sort.Slice` accepts any `func(i, j int) bool` because it only cares about the shape (takes two ints, returns bool) — not which specific comparison logic is inside.

This model breaks down slightly for method values, because the receiver is bound into the value and no longer appears in the function's type.

### Mental Model 2: Closures are Functions + Snapshots of Their Environment

A closure is not just a function — it is a function paired with a **reference** to the variables it captured from its enclosing scope. Those variables continue to exist as long as the closure exists, even after the outer function has returned.

Imagine a function as a recipe, and the captured variables as the pantry the recipe draws ingredients from. When you return a closure from a factory function, the caller gets both the recipe and a reference to the pantry. If the pantry changes (the captured variable is modified), the closure sees the new value the next time it runs.

This model explains both the power and the danger: the power is shared mutable state between multiple closures (a counter that multiple callbacks increment); the danger is the loop-variable capture bug (all closures share the same pantry slot, which by loop's end holds the final value).

### Mental Model 3: Call-by-Value as Copying a Memo

When you call a function, Go copies your arguments into the function's parameter variables — like handing someone a photocopy of your document. The function works with the copy. Changes to the copy do not affect your original.

For slices and maps, the "photocopy" includes a reference (a pointer to the data). Changing elements through the reference modifies the original data. But replacing the reference itself (reassigning the slice, reinitializing the map) only affects the copy.

This model explains why `s[0] = 99` inside a function is visible to the caller (modifying through the shared reference) but `s = append(s, 100)` is not (replacing the local reference in the copy without touching the caller's reference).

> [!NOTE]
> No single mental model is perfect. Use Model 1 (shapes) when deciding whether a function value is compatible with a parameter type. Use Model 2 (closures as function + environment) when debugging closure behavior, especially around loop variables. Use Model 3 (photocopy) when predicting what a function can and cannot modify in the caller's scope.

---

## Practical Examples

### Example 1: A Multi-Value Returning Parser _(Basic)_

**Scenario:** Parse a temperature string like `"98.6F"` or `"37.0C"` and return the numeric value and the unit, plus an error if the input is malformed.

**Goal:** Show how multiple return values, error returns, and `fmt.Errorf` work together in a real parsing function.

```go
package main

import (
    "fmt"
    "strconv"
    "strings"
)

// parseTemp parses a temperature string like "98.6F" or "37.0C".
// Returns the value, the unit ("C" or "F"), and an error if parsing fails.
func parseTemp(s string) (float64, string, error) {
    s = strings.TrimSpace(s)
    if len(s) < 2 {
        return 0, "", fmt.Errorf("parseTemp: input %q too short", s)
    }

    unit := string(s[len(s)-1]) // last character
    if unit != "C" && unit != "F" {
        return 0, "", fmt.Errorf("parseTemp: unknown unit %q in %q", unit, s)
    }

    val, err := strconv.ParseFloat(s[:len(s)-1], 64)
    if err != nil {
        return 0, "", fmt.Errorf("parseTemp: %w", err)
    }

    return val, unit, nil
}

func main() {
    inputs := []string{"98.6F", "37.0C", "100K", "notatemp", "0C"}
    for _, input := range inputs {
        val, unit, err := parseTemp(input)
        if err != nil {
            fmt.Printf("  %-12s → error: %v\n", input, err)
            continue
        }
        fmt.Printf("  %-12s → %.1f %s\n", input, val, unit)
    }
}
```

**Output / Result:**
```
  98.6F        → 98.6 F
  37.0C        → 37.0 C
  100K         → error: parseTemp: unknown unit "K" in "100K"
  notatemp     → error: parseTemp: unknown unit "p" in "notatemp"
  0C           → 0.0 C
```

**What to notice:** The function returns three values — the numeric result, the unit string, and an error. On every error path, the zero values (`0, "", fmt.Errorf(...)`) are returned. On the success path, `nil` is returned for the error. The caller uses `continue` to skip the success printing when there is an error, which is the standard Go error handling structure.

---

### Example 2: Higher-Order Functions for Data Transformation _(Intermediate)_

**Scenario:** A data pipeline where we filter and transform a list of employee records using functions as arguments.

**Goal:** Show how function types, higher-order functions, and closures compose naturally in a real data-processing scenario.

```go
package main

import "fmt"

type Employee struct {
    Name       string
    Department string
    Salary     float64
}

// filter returns employees for which predicate returns true
func filter(employees []Employee, predicate func(Employee) bool) []Employee {
    var result []Employee
    for _, e := range employees {
        if predicate(e) {
            result = append(result, e)
        }
    }
    return result
}

// mapSalary returns a new slice with f applied to each employee's salary
func mapSalary(employees []Employee, f func(float64) float64) []Employee {
    result := make([]Employee, len(employees))
    copy(result, employees)
    for i := range result {
        result[i].Salary = f(result[i].Salary)
    }
    return result
}

// inDepartment returns a predicate function that matches employees in dept
func inDepartment(dept string) func(Employee) bool {
    return func(e Employee) bool {
        return e.Department == dept
    }
}

// raiseBy returns a function that applies a percentage raise to a salary
func raiseBy(pct float64) func(float64) float64 {
    return func(salary float64) float64 {
        return salary * (1 + pct/100)
    }
}

func main() {
    team := []Employee{
        {"Alice", "Engineering", 120_000},
        {"Bob", "Marketing", 85_000},
        {"Carol", "Engineering", 130_000},
        {"Dave", "Marketing", 90_000},
        {"Eve", "Engineering", 110_000},
    }

    // Give all Engineering employees a 10% raise
    engineers := filter(team, inDepartment("Engineering"))
    raised := mapSalary(engineers, raiseBy(10))

    fmt.Println("Engineering team after 10% raise:")
    for _, e := range raised {
        fmt.Printf("  %-8s  $%.0f\n", e.Name, e.Salary)
    }
}
```

**Output / Result:**
```
Engineering team after 10% raise:
  Alice     $132000
  Carol     $143000
  Eve       $121000
```

**What to notice:** `inDepartment` and `raiseBy` are function factories — they return closures that close over the `dept` and `pct` arguments respectively. `filter` and `mapSalary` are higher-order functions that accept these closures. The caller code reads almost like English: "filter the team to those in the Engineering department, then map salaries by raising 10%."

---

### Example 3: Closures as Stateful Iterators _(Applied)_

**Scenario:** Implement a Fibonacci sequence generator as a closure-based iterator — a function that returns successive Fibonacci numbers on each call.

**Goal:** Show how closures with captured mutable state enable stateful abstractions without needing structs or methods.

```go
package main

import "fmt"

// fibonacci returns a function that yields successive Fibonacci numbers.
// Each call to the returned function returns the next number in the sequence.
func fibonacci() func() int {
    a, b := 0, 1
    return func() int {
        result := a
        a, b = b, a+b  // advance: a becomes b, b becomes a+b
        return result
    }
}

func main() {
    fib := fibonacci()

    fmt.Print("First 10 Fibonacci numbers: ")
    for i := 0; i < 10; i++ {
        if i > 0 {
            fmt.Print(", ")
        }
        fmt.Print(fib())
    }
    fmt.Println()

    // Each call to fibonacci() creates an independent sequence
    fib2 := fibonacci()
    fib2() // advance to 1st
    fib2() // advance to 2nd
    fmt.Printf("fib2 at position 3: %d\n", fib2()) // 1

    fmt.Printf("fib continues from where it left off: %d\n", fib()) // 55
}
```

**Output / Result:**
```
First 10 Fibonacci numbers: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
fib2 at position 3: 1
fib continues from where it left off: 55
```

**What to notice:** `a` and `b` are declared in `fibonacci()`'s scope, but the returned closure keeps them alive after `fibonacci()` has returned. Each call to `fib()` reads and modifies `a` and `b`. Two calls to `fibonacci()` produce two independent closures with independent `a` and `b` variables — there is no sharing. This is the closure-as-object pattern: a closure with captured mutable state is functionally equivalent to an object with fields and a single method.

---

### Example 4: defer + Named Returns for Error Wrapping _(Edge Case)_

**Scenario:** A function that calls multiple sub-operations and wants every returned error to be wrapped with the function's name, without repeating `fmt.Errorf("processRecord: %w", err)` on every error return path.

**Goal:** Show exactly how a deferred closure can modify named return values, and why this is useful.

```go
package main

import (
    "errors"
    "fmt"
)

var (
    ErrInvalidID    = errors.New("invalid ID")
    ErrRecordLocked = errors.New("record is locked")
)

// fetchRecord simulates a database fetch
func fetchRecord(id int) (string, error) {
    if id <= 0 {
        return "", ErrInvalidID
    }
    if id == 42 {
        return "", ErrRecordLocked
    }
    return fmt.Sprintf("record-%d", id), nil
}

// processRecord fetches and processes a record.
// Any error returned is automatically wrapped with "processRecord <id>: ".
func processRecord(id int) (result string, err error) {
    // This deferred closure runs just before processRecord returns.
    // It captures 'err' by reference (not by value), so it sees whatever
    // err was set to when the function body finished executing.
    defer func() {
        if err != nil {
            err = fmt.Errorf("processRecord %d: %w", id, err)
        }
    }()

    var data string
    data, err = fetchRecord(id)
    if err != nil {
        return // naked return: result="", err=<the unwrapped error from fetchRecord>
        // The deferred closure will wrap it before the caller sees it
    }

    result = "[processed] " + data
    return // result=processed data, err=nil — deferred closure does nothing
}

func main() {
    for _, id := range []int{1, -1, 42} {
        result, err := processRecord(id)
        if err != nil {
            fmt.Printf("id=%2d error: %v\n", id, err)
            fmt.Printf("         unwrapped: %v\n", errors.Unwrap(err))
            continue
        }
        fmt.Printf("id=%2d result: %s\n", id, result)
    }
}
```

**Output / Result:**
```
id= 1 result: [processed] record-1
id=-1 error: processRecord -1: invalid ID
         unwrapped: invalid ID
id=42 error: processRecord 42: record is locked
         unwrapped: record is locked
```

**Why this is important:** Without the deferred closure, every `return` statement would need `return "", fmt.Errorf("processRecord %d: %w", id, err)`. With many error return paths (as is common in functions that do I/O), this is verbose and easy to forget on one path. The deferred closure guarantees that every error path gets the same wrapping, with the context (the `id`) always included. The `errors.Unwrap` call shows that `%w` preserves the original error for `errors.Is`/`errors.As` checks in the caller.

---

## Related Concepts

Within this topic:

- [[go/2. Control Flow]] — `defer` was introduced in Module 2; this module shows its full interaction with named return values and closures, which requires understanding function return mechanics
- [[go/4. Composite Types]] — slices and maps are passed to functions by value (copying the header); understanding slice internals is essential to correctly predict when modifications to a slice inside a function are visible to the caller
- [[go/5. Pointers]] — the full explanation of when to use pointer receivers vs value receivers, and when to pass `*T` vs `T` to functions, is in Module 5; this module gives you the call-by-value foundation
- [[go/6. Methods and Interfaces]] — methods are functions with receivers; method values and method expressions are directly related to the function-as-value concept introduced here
- [[go/8. Error Handling]] — the `(T, error)` convention, `fmt.Errorf` with `%w`, and `errors.Is`/`errors.As` build directly on the error return pattern introduced here
- [[go/9. Concurrency]] — goroutines are almost always launched as closures (`go func() { ... }()`); the loop-variable capture pitfall is especially critical in concurrent code

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Basic Function Declaration** _(Easy)_
>
> Write a function `clamp(val, min, max int) int` that returns `val` clamped to the range `[min, max]`. If `val < min`, return `min`. If `val > max`, return `max`. Otherwise return `val`. Call it with at least 5 test cases covering all three branches.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-basic-function-declaration--easy--1-pt)

The exercises range from simple function declarations to a closure-based middleware chain. Complete at least the Easy and Medium exercises before taking the test.

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
Pipeline Calculator — implement a small computation pipeline where each transformation step is a `func(float64) float64`. Write at least 5 transformations (add, multiply, square, clamp, round), chain them in a slice, and apply the pipeline to a list of inputs. This exercises function types, higher-order functions, closures, and variadic functions together in a coherent small program.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[A Tour of Go — More Types: Functions (go.dev/tour)](https://go.dev/tour/moretypes/24)** — Interactive tour section covering function values, closures (moretypes/24 through moretypes/26), with a fibonacci closure exercise; best done after reading the Core Concepts section of this module
2. **[Effective Go — Functions](https://go.dev/doc/effective_go#functions)** — Official idiomatic Go guide covering multiple return values, named result parameters, `defer`, and the error convention; the defer section is especially worth reading for the `trace` pattern
3. **[The Go Blog — Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)** — Andrew Gerrand's canonical explanation of defer semantics; the three rules of defer are the foundation for understanding how defer interacts with named return values
4. **"The Go Programming Language" by Donovan & Kernighan — Chapter 5 (Functions)** — The definitive book-length treatment: function declarations, multiple return values, errors, function values, anonymous functions, closures (including the loop-variable pitfall), variadic functions, deferred function calls, and panic/recover; if you read one chapter alongside this module, it should be this one
5. **"Learning Go" by Jon Bodner (2nd ed.) — Chapter 5 (Functions)** — Modern treatment with emphasis on idiomatic patterns; covers function types, closures, and defer with attention to Go 1.22 changes; good complement to Donovan & Kernighan

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 3

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
