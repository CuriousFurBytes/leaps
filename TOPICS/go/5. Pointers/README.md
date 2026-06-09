# Module 5: Pointers

[← Module 4: Composite Types](../4.%20Composite%20Types/) | [Topic Home](../README.md) | [Module 6: Methods and Interfaces →](../6.%20Methods%20and%20Interfaces/)

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
  - [What a Pointer Is — The Memory Mental Model](#what-a-pointer-is--the-memory-mental-model)
  - [Address-Of and Dereference: `&` and `*`](#address-of-and-dereference--and-)
  - [Pointer Types and the Nil Zero Value](#pointer-types-and-the-nil-zero-value)
  - [Value Semantics and Call-by-Value](#value-semantics-and-call-by-value)
  - [When to Use Pointers](#when-to-use-pointers)
  - [`new()` vs `&T{}`](#new-vs-t)
  - [Pointers to Structs and Automatic Field Dereference](#pointers-to-structs-and-automatic-field-dereference)
  - [Slices, Maps, and Channels Are Already Reference-Like](#slices-maps-and-channels-are-already-reference-like)
  - [No Pointer Arithmetic](#no-pointer-arithmetic)
  - [Double Pointers (`**T`)](#double-pointers-t)
  - [Escape Analysis: Stack vs Heap (Preview)](#escape-analysis-stack-vs-heap-preview)
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

This module covers **Go's pointer system**: what a pointer is, how to create and use one, the difference between value semantics and pointer semantics, and the deliberate design decisions that make Go's pointer model safer than C's. Pointers are not optional knowledge in Go — they appear in nearly every non-trivial program, from struct mutation in functions to method receivers to the way the `encoding/json` package optionally omits fields.

By the end of this module, you will have a clear mental model for how variables live in memory, understand exactly when copying a value is different from sharing it, and be able to read and write idiomatic Go code involving pointers with confidence.

This is foundational for the next module: [[go/6. Methods and Interfaces]] uses pointer receivers extensively, and you cannot understand that module without this one.

**Difficulty:** Beginner–Intermediate &nbsp;|&nbsp; **Estimated time:** 3–4 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain what a pointer holds and why it is useful, using the memory address mental model — _draw or describe what `x := 42; p := &x` looks like in memory_
2. Use `&` to take the address of a variable and `*` to dereference a pointer — _write a `double(p *int)` function that modifies the caller's value_
3. Explain the nil zero value for pointers and defend code against nil-pointer dereference panics — _add a nil guard to any function that receives a pointer_
4. Explain Go's call-by-value model and articulate when passing a pointer is necessary — _identify whether a given function call can mutate the caller's variable_
5. Choose between `new(T)` and `&T{}` and explain when each is appropriate — _rewrite any `new(T)` call as `&T{}` or vice versa and explain the difference_
6. Explain why slices, maps, and channels do not require explicit pointer passing to share mutations — _predict whether a function that appends to a slice will affect the caller_

---

## Prerequisites

### Required Modules

- [[go/4. Composite Types]] — you need to understand: structs (field access, composite literals), slices (header internals — pointer + length + capacity), and maps; pointers to structs are a major use case covered in this module
- [[go/3. Functions]] — you need to understand: how Go passes arguments to functions (by value), multiple return values, and function signatures; the entire rationale for pointers rests on understanding call-by-value
- [[go/1. Types and Variables]] — you need to understand: Go's zero values (the nil zero value for pointers is covered here), variable declaration, and type declarations

### Required Concepts

- **Call-by-value** — every function argument in Go is a copy of the original value; understanding this is the *entire* reason pointers exist as a concept
- **Memory as a flat array of bytes** — variables live at specific addresses; a pointer is simply a variable whose value is an address
- **Struct field access** — `s.Field` syntax from [[go/4. Composite Types]]; this module extends it to `p.Field` where `p` is a pointer to a struct

> [!TIP]
> If call-by-value feels abstract, try this before continuing: write a function `addOne(n int)` that tries to add 1 to its argument, call it with a variable `x := 5`, and observe that `x` is still 5 after the call. That observation is the entire motivation for this module.

---

## Why This Matters

Pointers are the mechanism by which Go functions can communicate with the outside world in both directions — not just reading inputs, but modifying state the caller cares about. Without pointers, every function is a pure transformation: it takes a copy of data in and returns a new value out. With pointers, a function can reach back into the caller's memory and change a value in place.

Concretely, mastery of this module enables you to:

- **Write mutation-oriented APIs** — functions like `json.Unmarshal(data, &result)` and `fmt.Sscan(input, &x)` take pointer arguments because they need to write into the caller's variable; you cannot use these functions without understanding why `&` is required
- **Avoid unnecessary copying** — a large struct passed by value copies every field on every call; passing a pointer copies only the address (8 bytes on a 64-bit machine); knowing when to use pointers is a prerequisite for writing efficient Go code (see [[go/16. Performance and Profiling]])
- **Represent optional and nullable values** — a `*string` can be `nil` (absent) or non-nil (present); this is Go's idiomatic way to express optional fields in structs, especially in JSON-mapped types
- **Understand the standard library** — the `sync.Mutex`, `bytes.Buffer`, and virtually every non-trivial type in the stdlib are designed to be used via pointer; understanding why tells you how to design your own types correctly

Without understanding pointers, you will misread half the standard library, be unable to write functions that modify their arguments, and be confused by why your struct modifications do not persist after a function call.

---

## Historical Context

Pointers were invented alongside the first compiled languages. **Fortran** (1957) had no explicit pointers but addressed memory through arrays. **COBOL** (1959) had no pointers. The concept crystallized with **ALGOL 60**, which introduced references, and became central to systems programming with **C** (designed by Dennis Ritchie at Bell Labs, first described in 1972).

In C, pointers are the central abstraction: `*p` dereferences, `p++` advances to the next element, `p + n` accesses the nth element. C's pointer model is extremely powerful but correspondingly dangerous — pointer arithmetic and unchecked casts are the source of most security vulnerabilities in C programs.

**C++** inherited C's pointer model and added references (`int& r = x`) as a safer alternative for some use cases. Java and Python took the opposite approach: they removed manual pointers entirely and replaced them with implicit references for all objects, which eliminates pointer arithmetic but introduces other confusion (Python's `is` vs `==`, Java's reference equality).

**Go's pointer model** (designed 2007–2009 by Griesemer, Pike, and Thompson) is a deliberate middle path:

- **Explicit, like C** — you control when to pass by value and when to pass by pointer; there is no implicit boxing
- **Safe, unlike C** — pointer arithmetic is not allowed; you cannot cast a pointer to an integer and back; you cannot walk off the end of an array via a pointer
- **Simpler than C++** — no references, no const pointers, no pointer-to-pointer-to-const complexities; the mental model is minimal

Key moments in the design:

- **2007** — Initial design explicitly bans pointer arithmetic; Rob Pike's experience with security bugs in C systems at Bell Labs directly informed this choice
- **2009** — Go 1 pre-release ships with the current pointer model, essentially unchanged since
- **2012** — Go 1.0; the language spec's section on address operators and pointer types is concise and has remained stable for over a decade
- **2024 (Go 1.22)** — The `unsafe.SliceData`, `unsafe.StringData` additions to the `unsafe` package give authorized low-level code access to pointer arithmetic, but normal Go code never needs them

Understanding this history explains the shape of Go's pointer design. Every limitation (no pointer arithmetic) is a deliberate safety decision. Every capability (explicit `&`, explicit `*`) is a deliberate clarity decision.

---

## Core Concepts

### What a Pointer Is — The Memory Mental Model

Every variable in a running program lives at a **memory address** — a number identifying its location in the computer's address space. You can think of memory as a large array of bytes, each indexed by its address. When you declare `x := 42`, the runtime reserves space for an `int` somewhere in memory (say, at address `0xc000014098`) and stores the value `42` there.

A **pointer** is a variable whose value is a memory address. Instead of holding an integer or a string, it holds a location. If `p` is a pointer to `x`, then `p` holds the value `0xc000014098` — the address where `42` lives.

```
Memory layout after:  x := 42  and  p := &x

Address         Value     Variable
─────────────   ───────   ────────
0xc000014090    ...
0xc000014098    42        x        ← x lives here
...
0xc0000140b0    0xc000014098   p   ← p holds the address of x
```

This is the only mental model you need: **a pointer is an address; dereferencing it means going to that address to read or write the value there**.

> [!NOTE]
> Actual addresses in a Go program are assigned by the runtime and vary between runs. The specific address `0xc000014098` above is illustrative. What matters is the relationship: `p` holds the address of `x`, so `*p` is another way to access `x`.

---

### Address-Of and Dereference: `&` and `*`

Go provides two operators for working with pointers:

- **`&` (address-of)** — takes a variable and returns a pointer to it (its address)
- **`*` (dereference)** — takes a pointer and returns the value at the address it holds

These are inverse operations:

```go
x := 42
p := &x    // p is a *int; its value is the address of x

fmt.Println(x)   // 42  — direct access to x
fmt.Println(p)   // 0xc000014098  — the address (varies each run)
fmt.Println(*p)  // 42  — dereference: follow the pointer and read the value

*p = 100   // write through the pointer: changes the value at the address
fmt.Println(x)   // 100  — x is now 100, because p pointed to x
```

The `*` symbol is overloaded in Go: in a **type position** (`*int`, `*string`) it means "pointer to"; in an **expression position** (`*p`) it means "dereference". Context always disambiguates:

```go
var p *int        // *int is a type: "pointer to int"
*p = 5            // *p is an expression: "value at the address p holds"
```

A pointer's type specifies what type of value it points to. A `*int` points to an `int`. A `*string` points to a `string`. A `*Person` points to a `Person` struct. Go is statically typed, so you cannot accidentally treat a `*int` as a `*string`.

> [!WARNING]
> The `&` operator can only be applied to **addressable** values — variables, pointer dereferences, struct fields, and array/slice elements. You cannot take the address of a function return value, a map value, or a constant: `&42` does not compile, and `&m["key"]` does not compile. This is a deliberate restriction: map values may be relocated when the map grows.

---

### Pointer Types and the Nil Zero Value

Every pointer type has a **zero value of `nil`**. A nil pointer does not point anywhere. If you declare a pointer variable without initializing it, it is nil:

```go
var p *int      // p is nil — it holds no address
fmt.Println(p)  // <nil>

if p == nil {
    fmt.Println("p does not point anywhere")
}
```

**Dereferencing a nil pointer is a runtime panic** — one of the most common panics in Go programs:

```go
var p *int
*p = 5  // panic: runtime error: invalid memory address or nil pointer dereference
```

The panic name — "nil pointer dereference" — is exactly what it says: you tried to follow a pointer that held no address. Always check for nil before dereferencing a pointer you did not initialize yourself:

```go
func printValue(p *int) {
    if p == nil {
        fmt.Println("(nil)")
        return
    }
    fmt.Println(*p)  // safe: we know p is not nil
}
```

> [!WARNING]
> The nil check must happen before the dereference. `if p != nil && *p > 0` is safe because `&&` short-circuits: if `p == nil`, the right side is never evaluated. `if *p > 0 && p != nil` would panic if `p` is nil because `*p` is evaluated first.

---

### Value Semantics and Call-by-Value

Go uses **call-by-value**: when you pass a variable to a function, the function receives a **copy** of that value. Changes to the copy do not affect the original:

```go
func addOne(n int) {
    n++   // modifying the local copy
}

x := 5
addOne(x)
fmt.Println(x)  // 5 — unchanged; addOne got a copy of 5
```

This applies to structs too — a large struct is copied in full on every call:

```go
type Point struct{ X, Y float64 }

func moveRight(p Point) {
    p.X += 10   // modifying the copy; caller's Point is unchanged
}

pt := Point{1, 2}
moveRight(pt)
fmt.Println(pt)  // {1 2} — unchanged
```

**Passing a pointer changes everything**: now the function receives a copy of the address, but the address still points to the original variable. The function can modify the caller's value through the pointer:

```go
func addOnePtr(n *int) {
    *n++   // dereference and increment: modifies the original
}

x := 5
addOnePtr(&x)   // pass the address of x
fmt.Println(x)  // 6 — modified by addOnePtr
```

The pointer itself is passed by value (the address is copied), but what the pointer points to is shared. This is the fundamental insight: **pointers let you share access to a value, not bypass call-by-value**.

```
Call-by-value (default):            Pointer argument:

Caller     Function                 Caller     Function
  x=5  ──copy──► n=5                  x=5  ◄──── p = &x
                  n++                             *p++
  x=5  (unchanged)                   x=6  (modified through p)
```

---

### When to Use Pointers

Using pointers everywhere is not idiomatic Go. Use a pointer when at least one of these is true:

**1. Mutation — the function needs to modify the caller's value:**
```go
// Must use pointer — json.Unmarshal writes into result
var result MyStruct
json.Unmarshal(data, &result)

// Must use pointer — scan writes into x
var x int
fmt.Scan(&x)
```

**2. Large structs — avoiding expensive copies:**
```go
type BigConfig struct {
    // dozens of fields...
}

// Prefer: pass pointer to avoid copying all fields
func process(cfg *BigConfig) { ... }

// Avoid for large structs: copies every field
func processValue(cfg BigConfig) { ... }
```

> [!NOTE]
> "Large" is contextual. A struct with 2–3 small fields is fine to pass by value; a struct with 20 fields or containing large arrays should be passed by pointer. When in doubt, profile — see [[go/16. Performance and Profiling]].

**3. Optional/nullable — using nil to represent absence:**
```go
type User struct {
    Name     string
    Nickname *string   // nil if no nickname set; non-nil if present
    Age      *int      // nil if unknown age
}

// The difference between "not set" (nil) and "set to empty string" ("") is meaningful
```

**4. Shared identity — multiple parts of the code need to see the same object:**
```go
type Counter struct{ n int }

func (c *Counter) Increment() { c.n++ }  // pointer receiver — method operates on the shared Counter

c := &Counter{}
go func() { c.Increment() }()  // goroutine modifies the same Counter
```

**When NOT to use pointers:**

- Small, immutable data (integers, small structs used as values like `time.Time`)
- When you want to communicate "this is a value, not a shared object" — `time.Time` is passed by value deliberately
- Slices, maps, and channels — they already carry an internal pointer and do not need to be wrapped in an explicit pointer for most use cases (see the next section)

---

### `new()` vs `&T{}`

Go provides two ways to allocate a pointer to a zero-initialized value:

**`new(T)`** — allocates a zeroed `T` and returns a `*T`:
```go
p := new(int)        // *int pointing to a zero int
fmt.Println(*p)      // 0

q := new(MyStruct)   // *MyStruct pointing to a zero MyStruct
```

**`&T{}`** — creates a composite literal and takes its address:
```go
p := &MyStruct{}                   // *MyStruct, all fields zero
q := &MyStruct{Name: "Alice", Age: 30}  // *MyStruct with initialized fields
```

In practice, `&T{}` is almost always preferred because:
1. It works with all composite types (structs, slices, maps, arrays)
2. It allows field initialization in the same expression
3. It reads more naturally — you can see the type and its initial state

`new` is rarely seen in modern Go code. You will encounter it in older code or in cases where you need a pointer to a primitive type with no initial value to specify:

```go
// These are equivalent:
p := new(int)
p := &(0)   // this does NOT compile — can't take address of literal
var i int
p := &i     // this works but requires a named variable

// In practice for a zero pointer-to-int, new(int) is fine
// but most code just declares the variable and takes its address
```

> [!TIP]
> **Rule of thumb:** Use `&T{...}` for structs (with or without field initialization). Use `new(T)` only when you need a pointer to a primitive type and there is no value to initialize with. In practice, you will write `&T{}` 95% of the time.

---

### Pointers to Structs and Automatic Field Dereference

When you have a pointer to a struct, Go provides **automatic field dereference**: you do not need to write `(*p).Field` — you can write `p.Field` directly, and Go inserts the dereference automatically:

```go
type Point struct{ X, Y float64 }

p := &Point{X: 1.0, Y: 2.0}

// These are identical:
fmt.Println((*p).X)  // explicit dereference — verbose
fmt.Println(p.X)     // automatic dereference — idiomatic Go

// Mutation through a pointer field:
p.X = 10.0           // equivalent to (*p).X = 10.0
fmt.Println(p.X)     // 10
```

This convenience is why pointer-to-struct is so common in Go — you write `p.Field` just as if `p` were a struct value, but the field access goes through the pointer. This is particularly important when you learn about method receivers in [[go/6. Methods and Interfaces]]: a method with a pointer receiver `func (p *Point) Scale(factor float64)` can be called as `pt.Scale(2)` even when `pt` is a `Point` value — Go automatically takes the address.

**Passing a pointer to a struct:**

```go
type Person struct {
    Name string
    Age  int
}

func birthday(p *Person) {
    p.Age++  // modifies the caller's Person struct
}

alice := Person{Name: "Alice", Age: 30}
birthday(&alice)
fmt.Println(alice.Age)  // 31
```

Without the pointer, `birthday(alice)` would receive a copy and the original `alice.Age` would remain 30.

---

### Slices, Maps, and Channels Are Already Reference-Like

A common source of confusion: if slices and maps are passed by value, why do mutations inside a function affect the caller?

The answer is that slices, maps, and channels have **internal pointers**. Their value already contains a pointer to the underlying data:

```go
// A slice header contains: [pointer to array | length | capacity]
// Passing a slice copies the header, but both headers point to the same array

func doubleFirst(s []int) {
    if len(s) > 0 {
        s[0] *= 2  // modifies the underlying array through the internal pointer
    }
}

nums := []int{1, 2, 3}
doubleFirst(nums)
fmt.Println(nums)  // [2 2 3] — the first element was modified
```

But there is a crucial caveat: **`append` may replace the underlying array**. If `append` needs to grow the slice beyond its capacity, it allocates a new array and the function's copy of the slice header now points to a different array than the caller's:

```go
func appendOne(s []int) {
    s = append(s, 99)  // may allocate a new array; caller's slice is unaffected
}

nums := []int{1, 2, 3}
appendOne(nums)
fmt.Println(nums)  // [1 2 3] — the append did not affect the caller
```

To let a function grow a slice and have the caller see the new length, you must either **return the new slice** or **pass a pointer to the slice**:

```go
// Idiomatic: return the new slice
func appendOneReturn(s []int) []int {
    return append(s, 99)
}

nums = appendOneReturn(nums)
fmt.Println(nums)  // [1 2 3 99]
```

Maps behave like pointers at the top level — the map value itself is a pointer to the underlying hash table, so mutations are visible to the caller without a pointer argument:

```go
func addEntry(m map[string]int, key string, val int) {
    m[key] = val  // modifies the map the caller sees
}

counts := map[string]int{"a": 1}
addEntry(counts, "b", 2)
fmt.Println(counts)  // map[a:1 b:2]
```

The summary: **use `[]int` (not `*[]int`) for slices when you only need to mutate elements; use `*[]int` only when the function needs to change the slice's length or capacity and you don't want to use a return value**.

---

### No Pointer Arithmetic

Go deliberately does not allow pointer arithmetic. In C, `p++` advances a pointer to the next element of an array. In Go, this is not possible outside the `unsafe` package:

```go
p := &x
p++     // compile error: cannot increment pointer

// This is also not allowed:
q := p + 1  // compile error: invalid operation: p + 1 (types *int and int)
```

This restriction eliminates an entire class of bugs common in C:

- **Buffer overflows** — reading or writing past the end of an allocated region
- **Use-after-free** — accessing memory that has been freed (Go's GC handles this)
- **Wild pointers** — pointers computed by casting integers to pointers

The `unsafe` package exists for interoperability with C and for runtime internals, but it is outside the scope of everyday Go programming. The Go compiler and its test suite use `unsafe`; your application code almost certainly should not.

> [!NOTE]
> If you need array-style sequential access, use slice indexing (`s[i]`) or `for range`. These are bounds-checked and safe. The absence of pointer arithmetic is not a limitation — it is a safety guarantee.

---

### Double Pointers (`**T`)

A pointer to a pointer — `**T` — is occasionally useful when a function needs to reassign the pointer itself (not just the value it points to):

```go
func allocate(pp **int) {
    n := 42
    *pp = &n  // write the address of n into the location pp points to
}

var p *int    // p is nil
allocate(&p)  // pass the address of p
fmt.Println(*p)  // 42 — allocate gave p a value to point to
```

In practice, `**T` is rare in idiomatic Go. You will encounter it occasionally when working with linked list nodes, tree nodes, or when a function must reallocate a pointer that a caller owns. Most use cases that would require `**T` in C are handled more cleanly in Go by returning a new pointer value.

---

### Escape Analysis: Stack vs Heap (Preview)

Where does a variable live — on the stack or on the heap? In Go, this is determined by the compiler's **escape analysis**:

- If the compiler can prove a variable's lifetime does not outlive its enclosing function, it allocates on the stack (fast, no GC pressure).
- If the variable might be accessed after the function returns (e.g., its address is returned or stored somewhere long-lived), it **escapes to the heap**.

```go
func stackAlloc() int {
    x := 42   // x lives on the stack — doesn't escape
    return x  // return the value, not a pointer; x is safe on the stack
}

func heapAlloc() *int {
    x := 42   // x escapes to the heap — its address outlives this function
    return &x // returning a pointer to a local variable is safe in Go (unlike C)
}
```

In C, returning a pointer to a local variable is undefined behavior — the stack frame is gone when the function returns. In Go, **this is safe**: the compiler detects that `x` escapes and allocates it on the heap instead. You never need to worry about use-after-return bugs in Go.

The practical consequences of escape analysis:

- Stack allocation is cheaper (no GC involvement, simpler bookkeeping)
- Heap allocation is more flexible (survives across function calls) but adds GC pressure
- The compiler decides automatically; you do not annotate this

To inspect escape decisions:
```
go build -gcflags='-m' ./...
```

This prints escape analysis decisions for each variable. Understanding escape analysis is important for writing high-performance Go — see [[go/16. Performance and Profiling]] for a full treatment. For now, the key point is: **returning `&x` from a function is safe in Go**. The compiler handles it.

---

### How the Concepts Fit Together

```
A variable has a value and lives at an address
        │
        ├─ & (address-of) ──────────────► pointer (*T)
        │                                  │  zero value is nil
        │                                  │  nil dereference → panic
        │                                  │
        └─ * (dereference) ◄───────────────┘
                │
                ▼
         read or write the
         value at that address
                │
                ▼
         Call-by-value: functions get copies
         ── pointer argument → shares the original
         ── value argument   → independent copy
                │
         ┌──────┴──────┐
         ▼             ▼
    Use pointers    Slices/maps/channels
    for mutation,   already carry internal
    large structs,  pointers — no extra *
    optional nil    pointer usually needed
```

Every pointer concept in Go flows from two facts: variables have addresses, and function arguments are copies. Everything else — `new` vs `&T{}`, nil guards, no arithmetic, escape analysis — is a consequence of or a response to those two facts.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Expecting a function to mutate a struct passed by value**
>
> The single most common pointer mistake: a function modifies a struct argument but the caller's struct is unchanged, because Go copied the struct on the call.
>
> **Wrong (changes are lost):**
> ```go
> type Counter struct{ n int }
>
> func increment(c Counter) {
>     c.n++  // modifying a copy; caller's Counter is unchanged
> }
>
> c := Counter{n: 0}
> increment(c)
> fmt.Println(c.n)  // 0 — not 1; the increment was on a copy
> ```
>
> **Right (use a pointer):**
> ```go
> func increment(c *Counter) {
>     c.n++  // modifies the original Counter through the pointer
> }
>
> c := Counter{n: 0}
> increment(&c)
> fmt.Println(c.n)  // 1 — correctly incremented
> ```
>
> **Why this matters:** This bug is completely silent — the code compiles and runs; the mutation just disappears. The fix is always the same: pass a pointer to the struct (`&c`) and change the function signature to accept `*Counter`.

> [!WARNING]
> **Mistake 2: Dereferencing a nil pointer**
>
> Failing to guard against nil before dereferencing causes a runtime panic. The panic message is "runtime error: invalid memory address or nil pointer dereference" — very explicit, but only at runtime, not compile time.
>
> **Wrong (panics if p is nil):**
> ```go
> func printLength(s *string) {
>     fmt.Println(len(*s))  // panic if s is nil
> }
> ```
>
> **Right (nil guard before dereference):**
> ```go
> func printLength(s *string) {
>     if s == nil {
>         fmt.Println(0)
>         return
>     }
>     fmt.Println(len(*s))
> }
> ```
>
> **Why this matters:** Nil pointer panics crash your program. A function that accepts a pointer should always document whether nil is a valid input. If nil is possible, guard against it before dereferencing.

> [!WARNING]
> **Mistake 3: Using `*[]T` when a plain `[]T` or return value is cleaner**
>
> Beginners sometimes over-use pointers, wrapping a slice in a pointer when it is not necessary.
>
> **Wrong (unnecessary `*[]int`):**
> ```go
> func addItems(s *[]int, items ...int) {
>     *s = append(*s, items...)  // works but the dereference is ugly
> }
>
> nums := []int{1, 2}
> addItems(&nums, 3, 4)  // caller must take address; awkward
> ```
>
> **Right (return the new slice):**
> ```go
> func addItems(s []int, items ...int) []int {
>     return append(s, items...)
> }
>
> nums := addItems([]int{1, 2}, 3, 4)  // clean; caller reassigns
> ```
>
> **Why this matters:** `*[]T` is occasionally correct (when you cannot use a return value), but the idiomatic Go pattern for functions that may grow a slice is to return the new slice. This is how `append` itself works — it returns the (possibly new) slice.

> [!WARNING]
> **Mistake 4: Thinking maps need `*map[K]V` to share mutations**
>
> Maps are already reference types — the map value itself is a pointer to the hash table. Wrapping a map in a pointer adds no benefit and reduces readability.
>
> **Wrong (unnecessary pointer to map):**
> ```go
> func addEntry(m *map[string]int, k string, v int) {
>     (*m)[k] = v  // works but unnecessarily complex
> }
> ```
>
> **Right (map already shares mutations):**
> ```go
> func addEntry(m map[string]int, k string, v int) {
>     m[k] = v  // mutations are visible to the caller
> }
> ```
>
> **Why this matters:** `*map[K]V` is only needed in the rare case where the function must replace the map itself (assign `m = make(map[string]int)`) — not just modify its contents.

**Other pitfalls:**

- **Storing a pointer to a loop variable** — in a `for range` loop, the loop variable is reused each iteration; capturing `&v` in a closure or slice stores the same address each time, so all entries end up pointing to the last value. (Go 1.22 fixed this for `for range` over integers, but the pattern is still a trap with slice iteration in older code or when using a classic `for i` loop.)
- **Returning a pointer to a local variable and then expecting stack behavior** — as covered in the escape analysis section, this is safe in Go (unlike C). Do not worry about it; the compiler handles it.

---

## Mental Models

The right mental model makes pointers click. Here are three complementary ways to think about them.

### Mental Model 1: The House Address Analogy

Imagine a value as a house and a pointer as the house's postal address. The address is not the house — it is a way to locate the house.

- `x := 42` — a house exists at a specific location, containing the number 42
- `p := &x` — you write down the house's address on a piece of paper (`p`)
- `*p` — you visit the house at the address and look at what's inside
- `*p = 100` — you visit the house and change the contents to 100
- Passing a pointer to a function — you give someone else a copy of the address; they can visit the same house and change it
- Passing a value to a function — you build an identical copy of the house and give them that; changes to their copy don't affect the original

**This model breaks down when:** thinking about nil (a piece of paper with no address written on it) or about double pointers (an address of an address book, not an address of a house).

### Mental Model 2: Variables as Named Boxes with Addresses

Think of memory as a row of labeled boxes. Each box has an address (its position in the row) and a value (what's in it). A pointer is a box that contains another box's address.

```
Box name:   x           p
Address:    1098        10b0
Contents:   42          1098   (address of x)
```

When you write `*p`, you look at what's in box `p` (address `1098`), go to box at address `1098`, and read or write its contents. This makes it viscerally clear that `*p` and `x` are literally the same location in memory — not two copies of the same value.

**This model is most useful** for understanding why `*p = 100` changes `x`: they share the same box.

### Mental Model 3: The Two Questions Test

Before using a pointer, ask two questions:
1. **Does this function need to modify the caller's value?** If yes, pass a pointer.
2. **Is this value already reference-like (slice, map, channel, or a type that contains a pointer)?** If yes, you probably don't need an additional pointer.

If both answers are "no," pass by value. This decision tree handles 95% of pointer decisions in idiomatic Go code.

> [!NOTE]
> No single mental model covers every case. Use Model 1 (house address) when explaining pointers to someone new. Use Model 2 (named boxes) when debugging why a mutation did or did not propagate. Use Model 3 (two questions test) when writing new code and deciding whether to use a pointer.

---

## Practical Examples

### Example 1: Swap Function _(Basic)_

**Scenario:** Implementing a function that swaps two integers — impossible without pointers (or multiple return values).

**Goal:** Show the most fundamental use of pointer arguments for mutation.

```go
package main

import "fmt"

// swap exchanges the values of two integers.
// Both parameters must be pointers — we need to modify the caller's variables.
func swap(a, b *int) {
    *a, *b = *b, *a  // dereference both, swap the values
}

func main() {
    x, y := 10, 20
    fmt.Printf("Before: x=%d, y=%d\n", x, y)
    swap(&x, &y)  // pass addresses of x and y
    fmt.Printf("After:  x=%d, y=%d\n", x, y)
}
```

**Output / Result:**
```
Before: x=10, y=20
After:  x=20, y=10
```

**What to notice:** `swap` takes `*int` (pointer to int) parameters. At the call site, `&x` and `&y` take the addresses. Inside `swap`, `*a` and `*b` dereference to access the values. The simultaneous assignment `*a, *b = *b, *a` is idiomatic Go — no temporary variable needed. Without pointers, `swap(x, y)` would swap copies and the caller would see no change.

---

### Example 2: Optional Field with Nil Pointer _(Intermediate)_

**Scenario:** A user profile where some fields may or may not be set. Using `*string` for optional fields allows distinguishing "field not provided" (nil) from "field set to empty string" ("").

**Goal:** Demonstrate the optional/nullable use case for pointers.

```go
package main

import "fmt"

type UserProfile struct {
    Username string
    Email    string
    Nickname *string  // nil if not set; pointer to a string if set
    Age      *int     // nil if unknown
}

// displayProfile prints a profile, handling optional fields safely.
func displayProfile(u UserProfile) {
    fmt.Printf("Username: %s\n", u.Username)
    fmt.Printf("Email:    %s\n", u.Email)

    if u.Nickname != nil {
        fmt.Printf("Nickname: %s\n", *u.Nickname)
    } else {
        fmt.Println("Nickname: (not set)")
    }

    if u.Age != nil {
        fmt.Printf("Age:      %d\n", *u.Age)
    } else {
        fmt.Println("Age:      (unknown)")
    }
}

func main() {
    nick := "gopher"
    age := 29

    full := UserProfile{
        Username: "alice",
        Email:    "alice@example.com",
        Nickname: &nick,
        Age:      &age,
    }

    partial := UserProfile{
        Username: "bob",
        Email:    "bob@example.com",
        // Nickname and Age are nil (zero value for *string and *int)
    }

    fmt.Println("=== Full Profile ===")
    displayProfile(full)
    fmt.Println("\n=== Partial Profile ===")
    displayProfile(partial)
}
```

**Output / Result:**
```
=== Full Profile ===
Username: alice
Email:    alice@example.com
Nickname: gopher
Age:      29

=== Partial Profile ===
Username: bob
Email:    bob@example.com
Nickname: (not set)
Age:      (unknown)
```

**What to notice:** This pattern is ubiquitous in Go structs that map to JSON or database rows where fields may be absent. A `*string` nil pointer is unambiguously absent; a `*string` pointing to `""` is explicitly set to empty. A plain `string` cannot make this distinction. The `if u.Nickname != nil` guard before `*u.Nickname` is mandatory — forgetting it causes a panic if `Nickname` is nil.

---

### Example 3: Struct Mutation Via Pointer _(Applied)_

**Scenario:** A bank account where deposits and withdrawals must modify the shared account state.

**Goal:** Show pointer-receiver-style mutation before the Method receivers module, using a plain pointer argument.

```go
package main

import (
    "errors"
    "fmt"
)

type Account struct {
    Owner   string
    Balance float64
}

// deposit adds amount to the account. Must take *Account to modify the caller's account.
func deposit(a *Account, amount float64) error {
    if amount <= 0 {
        return errors.New("deposit amount must be positive")
    }
    a.Balance += amount  // automatic field dereference: (*a).Balance += amount
    return nil
}

// withdraw subtracts amount from the account if sufficient funds exist.
func withdraw(a *Account, amount float64) error {
    if amount <= 0 {
        return errors.New("withdrawal amount must be positive")
    }
    if a.Balance < amount {
        return fmt.Errorf("insufficient funds: have %.2f, need %.2f", a.Balance, amount)
    }
    a.Balance -= amount
    return nil
}

func main() {
    acc := Account{Owner: "Alice", Balance: 100.00}
    fmt.Printf("Initial: %s has $%.2f\n", acc.Owner, acc.Balance)

    if err := deposit(&acc, 50.00); err != nil {
        fmt.Println("deposit error:", err)
    }
    fmt.Printf("After deposit:   $%.2f\n", acc.Balance)

    if err := withdraw(&acc, 30.00); err != nil {
        fmt.Println("withdraw error:", err)
    }
    fmt.Printf("After withdraw:  $%.2f\n", acc.Balance)

    if err := withdraw(&acc, 200.00); err != nil {
        fmt.Println("withdraw error:", err)
    }
    fmt.Printf("Final balance:   $%.2f\n", acc.Balance)
}
```

**Output / Result:**
```
Initial: Alice has $100.00
After deposit:   $150.00
After withdraw:  $120.00
withdraw error: insufficient funds: have 120.00, need 200.00
Final balance:   $120.00
```

**What to notice:** `a.Balance += amount` inside `deposit` relies on automatic dereference — `a` is `*Account`, but Go lets you access fields directly without writing `(*a).Balance`. The function takes `*Account` because it needs to modify the struct's fields, not just read them. In [[go/6. Methods and Interfaces]], these functions will become methods with pointer receivers (`func (a *Account) Deposit(...)`), which is syntactic sugar for exactly this pattern.

---

### Example 4: Pointer Escape — Returning Address of Local Variable _(Edge Case)_

**Scenario:** Demonstrating that returning a pointer to a local variable is safe in Go (unlike C) and understanding what escape analysis does.

**Goal:** Show the escape behavior and build intuition for when the compiler allocates on the heap vs. stack.

```go
package main

import "fmt"

// newCounter allocates a counter on the heap (it escapes) and returns a pointer.
// In C, returning &count would be undefined behavior (stack frame is gone).
// In Go, the compiler detects the escape and allocates count on the heap.
func newCounter(start int) *int {
    count := start  // count will escape to the heap
    return &count   // safe in Go; unsafe in C
}

// addAndReturn returns a pointer to the sum.
// sum escapes because its address is returned.
func addAndReturn(a, b int) *int {
    sum := a + b  // escapes to heap
    return &sum
}

func main() {
    c := newCounter(10)
    fmt.Println(*c)  // 10

    *c += 5
    fmt.Println(*c)  // 15

    total := addAndReturn(3, 4)
    fmt.Println(*total)  // 7
}
```

To see the escape analysis output:
```
$ go build -gcflags='-m' .
# main
./main.go:9:2:  count escapes to heap
./main.go:16:2: sum escapes to heap
```

**Why this is important:** Returning a pointer to a local variable is idiomatic Go in factory functions like `newCounter`. The Go compiler's escape analysis ensures the variable lives long enough. This is fundamentally different from C, where such code would cause a stack-use-after-return bug. Go's safety here comes at the cost of a heap allocation rather than a stack allocation — a small price, and one you should only optimize away if profiling shows it matters (see [[go/16. Performance and Profiling]]).

---

## Related Concepts

Within this topic:

- [[go/4. Composite Types]] — structs are the most common target of pointer operations; understanding struct field layout is prerequisite to understanding pointer-to-struct; the slice header internals (pointer + length + cap) explain why slices are already reference-like
- [[go/6. Methods and Interfaces]] — pointer receivers (`func (p *T) Method()`) are the next step after this module; everything in this module applies directly to understanding when to use value vs pointer receivers
- [[go/8. Error Handling]] — `errors.New` returns `*errorString` under the hood; nil errors are nil interface values wrapping nil pointers; this module's nil pointer concepts extend directly into error handling

In other topics:

- [[memory-management]] — Go's garbage collector, escape analysis, stack vs heap allocation, and the runtime's memory model; this module previews escape analysis; [[memory-management]] covers the GC's operation, reference counting vs tracing collectors, and the implications for pointer-heavy code
- [[go/16. Performance and Profiling]] — pprof heap profiles, escape analysis with `-gcflags='-m'`, reducing allocations by controlling pointer escape; the performance impact of pointer-heavy code only becomes visible through profiling

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Address-Of and Dereference Basics** _(Easy)_
>
> Write a short program that declares an integer variable, takes its address, prints the pointer, dereferences the pointer to read the value, then modifies the value through the pointer. Print the original variable to confirm the modification went through.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-address-of-and-dereference-basics--easy--1-pt)

The exercises range from basic pointer syntax to a linked list implementation. Complete at least the Easy and Medium exercises before taking the test.

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
Linked List in Go — implement a singly-linked list with `Node` structs (`Value int`, `Next *Node`) and functions to prepend, append, and print the list. This requires creating pointer chains, traversal via dereferencing, and nil-terminated lists — directly exercising every pointer concept from this module.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[A Tour of Go — Pointers (go.dev/tour/moretypes/1)](https://go.dev/tour/moretypes/1)** — The official interactive tour's section on pointers; runnable examples of `&` and `*`, pointer types, and the nil zero value. Start here if you want interactive reinforcement of the syntax.
2. **[Effective Go — Allocation with `new`](https://go.dev/doc/effective_go#allocation_new) and [Allocation with `make`](https://go.dev/doc/effective_go#allocation_make)** — Two short, authoritative sections explaining `new` vs `make` vs composite literals; explains why `&T{}` is preferred in modern code and when `new` is still appropriate.
3. **[The Go Programming Language Blog — "The Go Memory Model"](https://go.dev/ref/mem)** — The formal memory model; more advanced than this module, but the introduction explains how goroutines observe each other's writes through memory — directly relevant to understanding shared pointers in concurrent code (preview of [[go/9. Concurrency]]).
4. **"The Go Programming Language" — Donovan & Kernighan, Chapter 2** — Section 2.3.2 covers pointers directly; subsequent sections cover the `new` function and variable lifetime. This is the standard Go reference text and the pointer chapter is concise and precise.
5. **"Learning Go" — Jon Bodner (2nd ed.), Chapter 6** — "Pointers" chapter with a modern, professional perspective on value vs pointer semantics, when to use pointers, and the implications for performance; explicitly addresses the "should I use a pointer receiver?" question that connects to [[go/6. Methods and Interfaces]].

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 5

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
