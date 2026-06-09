# Module 10: Generics

[← Module 9: Concurrency](../9.%20Concurrency/) | [Topic Home](../README.md) | [Module 11: Testing and Benchmarking →](../11.%20Testing%20and%20Benchmarking/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate--advanced-blue)
![Time](https://img.shields.io/badge/time-4--6h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Type Parameters](#type-parameters)
  - [Constraints](#constraints)
  - [Built-in Constraints: any and comparable](#built-in-constraints-any-and-comparable)
  - [Union Elements and the ~ Token](#union-elements-and-the--token)
  - [Generic Types — Structs and Containers](#generic-types--structs-and-containers)
  - [Type Inference and Explicit Instantiation](#type-inference-and-explicit-instantiation)
  - [Methods Cannot Introduce New Type Parameters](#methods-cannot-introduce-new-type-parameters)
  - [The Standard Generic Packages: slices, maps, cmp](#the-standard-generic-packages-slices-maps-cmp)
  - [Implementation: GC Shape Stenciling and Dictionaries](#implementation-gc-shape-stenciling-and-dictionaries)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Common Pitfalls](#common-pitfalls)
- [Related Concepts](#related-concepts)
- [Summary](#summary)
- [Exercises](#exercises)
- [Test](#test)
- [Further Reading](#further-reading)
- [Learning Journal](#learning-journal)

---

## Overview

This module covers **Go generics**: the type parameter system added in Go 1.18 (March 2022) that allows you to write functions and types that work across a range of types while preserving compile-time type safety. Before generics, writing type-safe reusable code in Go required either `interface{}` with type assertions at runtime, or copy-pasting the same code for each concrete type. Both approaches had real costs — the first lost type safety, the second lost maintainability.

By the end of this module you will understand the syntax of type parameters and constraints, how to define and use generic functions and types, the rules the compiler enforces, how the Go standard library uses generics in the `slices`, `maps`, and `cmp` packages, and — crucially — when to reach for generics versus a plain interface or simple concrete code.

**Difficulty:** Intermediate–Advanced &nbsp;|&nbsp; **Estimated time:** 4–6 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Write generic functions using type parameter syntax `func Name[T constraint](...)` — _given a "find the minimum" problem, write one generic function instead of one per numeric type_
2. Define custom constraints as interfaces with type sets, union elements, and the `~` underlying-type token — _write a `Numeric` constraint that covers all integer and float types_
3. Build generic container types: a `Stack[T]`, a `Set[T]`, and a generic linked list — _implement a Stack and use it with both `int` and `string` without code duplication_
4. Use the standard `slices`, `maps`, and `cmp` packages — _replace hand-written sort boilerplate with `slices.SortFunc` and use `cmp.Compare` for ordered comparisons_
5. Explain the rule that methods cannot introduce new type parameters, and work around it using package-level generic functions — _convert a method-based generic design to the function-receiver pattern when the compiler rejects it_
6. Decide when generics are the right tool and when an interface or plain code is better — _given a design problem, argue for or against generics with reference to the three scenarios where generics help_

---

## Prerequisites

### Required Modules

- [[go/6. Methods and Interfaces]] — you need to understand: how interfaces work as type sets, structural typing, method sets, and type assertions — constraints are defined as interfaces; understanding how interfaces describe behavior is prerequisite to understanding how they describe type sets
- [[go/4. Composite Types]] — you need to understand: slices, maps, and structs — the most important generic packages (`slices`, `maps`) operate on these types, and generic containers like `Stack[T]` wrap slices
- [[go/3. Functions]] — you need to understand: function signatures, multiple return values, closures, and first-class functions — generic functions extend the function syntax; the standard generic packages take function arguments (e.g., `slices.SortFunc` takes a comparator)

### Required Concepts

- **Interfaces as behavior contracts** — Go interfaces describe the set of methods a type must implement; generic constraints extend this idea to describe the set of types a type parameter can be instantiated with — if interfaces are opaque to you, constraints will be opaque too
- **Type assertions and type switches** — before generics, `interface{}` + type assertion was the workaround; understanding what was painful about that pattern explains what generics solve
- **Structural typing** — Go uses structural (duck) typing rather than nominal typing; constraints follow the same philosophy — a type satisfies a constraint by having the required properties, not by declaring it explicitly

> [!TIP]
> If interfaces feel shaky, do a 30-minute review of [[go/6. Methods and Interfaces]] before continuing.
> The syntax of generics is simple; the conceptual difficulty is understanding *what a constraint is* — and that requires solid interface understanding.

---

## Why This Matters

Before Go 1.18, two patterns dominated reusable Go code: `interface{}` and copy-paste.

The `interface{}` approach forced runtime type assertions that the compiler could not check. If you wrote `func Max(a, b interface{}) interface{}`, the caller received an `interface{}` back — they had to assert it to the concrete type they expected, and if they got it wrong, the program panicked at runtime. The compiler was blind to the type mismatch.

The copy-paste approach was type-safe but unmaintainable. Standard library packages like `sort` accumulated per-type implementations (`sort.Ints`, `sort.Float64s`, `sort.Strings`). Any utility function you wanted for multiple types required duplicating the code. Bug fixes had to be applied everywhere.

Concretely, generics enable you to:

- **Write container types once** — a `Stack[T]`, `Set[T]`, or `OrderedMap[K, V]` is written once and works for any compatible type; before generics, every team had its own copy-pasted version for each concrete type it needed
- **Use the standard `slices` and `maps` packages** — these packages, added in Go 1.21, replace decades of boilerplate with generic functions (`slices.Sort`, `slices.Contains`, `maps.Keys`, `maps.Values`) that are type-safe and readable
- **Express algorithms that work across numeric or ordered types** — a `Min[T]` or `Sum[T]` function that works for any numeric type, without the `interface{}` performance overhead or the type-assertion safety risk

Without generics, you would be forced back to the pre-1.18 patterns when writing reusable Go code — `interface{}` casts or copy-pasted implementations. Understanding generics is now a required competency for reading any modern Go library or codebase.

---

## Historical Context

Generics were the single most-requested feature in Go's history — and also the most controversial. The Go team resisted adding them for over a decade, not from laziness, but from a genuine commitment to keeping the language simple. The official position before 2018 was: "generics would be nice to have, but we don't have a design that doesn't significantly complicate the language." That position held for nine years.

Key moments in the evolution:

- **2009** — Go 1.0 design; no generics. Rob Pike and Ken Thompson are skeptical. The language uses `interface{}` for polymorphism
- **2010–2018** — Several proposals fail. The fundamental problem: how do you express constraints? Early proposals required explicit marker interfaces or complicated syntax. None felt like Go
- **2018** — Ian Lance Taylor and Robert Griesemer propose the "contracts" approach, which eventually evolves into the interface-as-constraint design
- **2020** — The design draft published as "Type Parameters" by Griesemer, Taylor, and others. The key insight: constraints *are* interfaces — no new concept needed, just an extension of the existing interface mechanism
- **March 2022 — Go 1.18** — Generics ship. Type parameters with interface constraints. The `any` alias for `interface{}` and the `comparable` constraint are added to the language. `golang.org/x/exp/constraints` provides `Ordered`, `Integer`, and other common constraints on an experimental basis
- **August 2023 — Go 1.21** — `slices`, `maps`, and `cmp` packages added to the standard library. `cmp.Ordered` becomes the standard way to express "this type supports `<`, `<=`, etc." The `golang.org/x/exp` constraints are formalized into `cmp.Ordered`

The "why now?" question has a practical answer: the design that finally shipped solved the constraint problem cleanly by reusing interfaces. The `comparable` constraint solved the map-key problem. And the `~` operator (underlying type) solved the "I want this constraint to work with my named type `type Celsius float64`" problem — without it, custom numeric types would be excluded from numeric constraints.

---

## Core Concepts

### Type Parameters

A **type parameter** is a placeholder for a concrete type, specified in square brackets between the function name and the parameter list. The type parameter has a name (by convention a single uppercase letter like `T`, or a descriptive name like `Elem`) and a **constraint** that specifies which types can be used as arguments.

The basic syntax:

```go
// A generic function: T is the type parameter, any is its constraint.
// "any" means T can be any type at all.
func Print[T any](v T) {
    fmt.Println(v)
}

// Call with explicit type argument:
Print[int](42)

// Call with type inference — compiler figures out T = string:
Print("hello")
```

A function can have multiple type parameters:

```go
// Two type parameters: K for key, V for value.
// comparable is the constraint for K (required for map keys).
func MapContains[K comparable, V any](m map[K]V, key K) bool {
    _, ok := m[key]
    return ok
}
```

The type parameter list `[T constraint]` appears after the function name and before the regular parameter list. Inside the function body, `T` behaves exactly like a concrete type — you can declare variables of type `T`, pass values of type `T`, return values of type `T`, and use whatever operations the constraint permits.

```go
// Returns the minimum of two values.
// cmp.Ordered is a constraint meaning T must support <, <=, etc.
func Min[T cmp.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Works for any ordered type — int, float64, string, etc.
fmt.Println(Min(3, 7))         // Output: 3
fmt.Println(Min(3.14, 2.71))   // Output: 2.71
fmt.Println(Min("cat", "bat")) // Output: bat
```

---

### Constraints

A **constraint** is an interface that specifies what operations and types are valid for a type parameter. The key insight of Go's generics design: **constraints are interfaces**. No new concept was invented — the existing interface mechanism was extended to describe type sets, not just method sets.

Before Go 1.18, an interface described a set of *methods*. From Go 1.18 onward, an interface can also describe a set of *types*. An interface that contains only type elements is a **type set constraint** — it says "T must be one of these types." An interface that contains only method elements is a **method set constraint** — it says "T must implement these methods." An interface can contain both.

```go
// Method-set constraint: T must implement the Stringer interface.
// Any type with a String() string method satisfies this.
type Stringer interface {
    String() string
}

func PrintString[T Stringer](v T) {
    fmt.Println(v.String())
}

// Type-set constraint: T must be exactly int, float64, or string.
// (You almost always want ~ variants instead — see next section.)
type Numeric interface {
    int | float64
}
```

When writing code parameterized by `T`, **you can only use operations permitted by the constraint**. If the constraint is `any` (the empty interface), you can only do things every type supports: assign, pass around, and compare to nil (for pointer/interface types). If the constraint is `cmp.Ordered`, you can additionally use `<`, `<=`, `>`, `>=`. If the constraint includes method signatures, you can call those methods.

```go
// This does NOT compile — the constraint "any" doesn't permit <
func WrongMin[T any](a, b T) T {
    if a < b { // compile error: cannot use < with type T (constrained by any)
        return a
    }
    return b
}
```

The compiler enforces constraints at the call site and inside the function body. This is the key improvement over `interface{}`: the type mismatch is caught at compile time, not at runtime.

---

### Built-in Constraints: any and comparable

Go 1.18 added two predeclared identifiers that are used as constraints:

**`any`** is an alias for `interface{}`. It means "T can be any type at all." Use it when your function doesn't need to perform any type-specific operations — it just passes values around, stores them, or returns them.

```go
// any constraint: works with any type, but you can't do type-specific operations
func First[T any](s []T) (T, bool) {
    if len(s) == 0 {
        var zero T // zero value of T
        return zero, false
    }
    return s[0], true
}
```

**`comparable`** is a predeclared constraint meaning "T supports `==` and `!=`". This constraint exists because not all Go types are comparable — slices, maps, and functions are not comparable with `==`. The `comparable` constraint is required whenever your type parameter will be used as a map key or compared with `==`/`!=`.

```go
// comparable constraint: T can be used as a map key
func Contains[T comparable](s []T, target T) bool {
    for _, v := range s {
        if v == target { // requires comparable
            return true
        }
    }
    return false
}

fmt.Println(Contains([]int{1, 2, 3}, 2))           // true
fmt.Println(Contains([]string{"a", "b"}, "c"))      // false
```

> [!NOTE]
> `comparable` is subtly different from "all types that can be compared with `==` at runtime." The constraint `comparable` means the type is *statically* comparable — it excludes interface types (which might hold non-comparable concrete types) and types containing non-comparable fields. The practical rule: use `comparable` when you need `==`/`!=` or map keys.

---

### Union Elements and the ~ Token

A **union element** in a constraint lists multiple types separated by `|`. The type parameter must be one of those listed types:

```go
type Integer interface {
    int | int8 | int16 | int32 | int64 |
        uint | uint8 | uint16 | uint32 | uint64 | uintptr
}
```

But there is a problem with bare union types: they exclude named types with the same underlying type. If a user defines `type Celsius float64`, a constraint of `float32 | float64` would not be satisfied by `Celsius` — even though `Celsius` is fundamentally a `float64`.

The **`~` (tilde) operator** solves this: `~T` means "any type whose *underlying type* is T." This is the most important piece of the constraint syntax for practical use.

```go
// Without ~: named types like Celsius are excluded
type FloatBad interface {
    float32 | float64
}

// With ~: named types with float64 underlying type are included
type Float interface {
    ~float32 | ~float64
}

type Celsius float64   // underlying type is float64
type Fahrenheit float32 // underlying type is float32

// Works with ~Float, fails with FloatBad
func ToFloat[T Float](v T) float64 {
    return float64(v)
}

_ = ToFloat(Celsius(100))    // OK — ~float64 matches
_ = ToFloat(3.14)            // OK — float64 itself also matches ~float64
```

The `cmp.Ordered` constraint in the standard library uses `~` on all its member types:

```go
// From the cmp package (simplified):
type Ordered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
        ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
        ~float32 | ~float64 |
        ~string
}
```

This means any custom type based on an integer, float, or string (e.g., `type Priority int`, `type Celsius float64`, `type Tag string`) automatically satisfies `cmp.Ordered`.

---

### Generic Types — Structs and Containers

Type parameters work not just on functions but on **type declarations**. A generic type is a struct (or other composite type) parameterized by one or more type parameters.

**Generic Stack:**

```go
// Stack[T] is a generic last-in, first-out container.
// T can be any type — the constraint is "any".
type Stack[T any] struct {
    items []T
}

// Push adds an item to the top of the stack.
func (s *Stack[T]) Push(v T) {
    s.items = append(s.items, v)
}

// Pop removes and returns the top item.
// Returns the zero value and false if the stack is empty.
func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    top := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return top, true
}

// Len returns the number of items in the stack.
func (s *Stack[T]) Len() int {
    return len(s.items)
}
```

Using the generic Stack:

```go
// Integer stack
var ints Stack[int]
ints.Push(1)
ints.Push(2)
v, _ := ints.Pop()
fmt.Println(v) // Output: 2

// String stack — same type, different instantiation
var strs Stack[string]
strs.Push("hello")
strs.Push("world")
w, _ := strs.Pop()
fmt.Println(w) // Output: world
```

> [!NOTE]
> When writing methods on a generic type, the type parameter appears in the receiver: `func (s *Stack[T]) Push(v T)`. You are using `T` in the receiver, not introducing a new type parameter — the type parameter was declared on the type itself.

**Generic Set:**

```go
// Set[T] is an unordered collection with no duplicate elements.
// T must be comparable because map keys must be comparable.
type Set[T comparable] struct {
    m map[T]struct{}
}

func NewSet[T comparable]() *Set[T] {
    return &Set[T]{m: make(map[T]struct{})}
}

func (s *Set[T]) Add(v T) {
    s.m[v] = struct{}{}
}

func (s *Set[T]) Contains(v T) bool {
    _, ok := s.m[v]
    return ok
}

func (s *Set[T]) Len() int {
    return len(s.m)
}
```

---

### Type Inference and Explicit Instantiation

Go's compiler can almost always **infer** the type argument for a generic function from the types of the actual arguments passed. Explicit instantiation (spelling out `[int]`) is rarely needed in practice.

```go
// Type inference: the compiler infers T = int from the argument 3 and 7.
result := Min(3, 7)         // inferred: Min[int](3, 7)

// Type inference from slice element type:
nums := []float64{1.1, 2.2, 3.3}
first, _ := First(nums)     // inferred: First[float64](nums)

// Explicit instantiation: useful when inference is impossible
// (e.g., no argument of type T, or ambiguous situation)
var zero = *new(int)
_ = zero
```

Type inference works through **type unification**: the compiler matches the types of the actual arguments against the function's parameter types and solves for the type parameters. If the arguments provide enough information, inference succeeds. If the function has a type parameter that doesn't appear in the argument types (e.g., it only appears in the return type), you must be explicit:

```go
// T only appears in the return type — must be explicit
func Zero[T any]() T {
    var v T
    return v
}

z := Zero[int]()    // explicit: Zero[int]()
// z := Zero()      // would not compile — T cannot be inferred
```

---

### Methods Cannot Introduce New Type Parameters

This is the most surprising restriction in Go's generics system: **methods on a type cannot declare their own new type parameters**. Type parameters may only be introduced on function declarations and type declarations.

```go
type Container[T any] struct { ... }

// LEGAL: method uses the type's existing type parameter T
func (c *Container[T]) Add(v T) { ... }

// ILLEGAL: method tries to introduce a new type parameter U
// func (c *Container[T]) Convert[U any]() *Container[U] { ... }
// compile error: method must have no type parameters
```

This restriction exists to keep the method dispatch mechanism simple and efficient — allowing methods to introduce type parameters would significantly complicate the compiler and the runtime's interface dispatch tables.

The workaround is to write **package-level generic functions** that take the receiver as an argument:

```go
// Package-level generic function as a workaround
func ConvertContainer[T, U any](c *Container[T], convert func(T) U) *Container[U] {
    // ...
}
```

---

### The Standard Generic Packages: slices, maps, cmp

Go 1.21 added three standard library packages that use generics heavily:

**`slices` package** (pkg.go.dev/slices) — generic operations on slices:

```go
import "slices"

// Sort a slice of any ordered type
nums := []int{3, 1, 4, 1, 5, 9}
slices.Sort(nums)
fmt.Println(nums) // [1 1 3 4 5 9]

// Sort with a custom comparator
type Person struct{ Name string; Age int }
people := []Person{{"Alice", 30}, {"Bob", 25}, {"Carol", 35}}
slices.SortFunc(people, func(a, b Person) int {
    return cmp.Compare(a.Age, b.Age) // sort by Age
})
fmt.Println(people) // [{Bob 25} {Alice 30} {Carol 35}]

// Binary search
idx, found := slices.BinarySearch([]int{1, 2, 3, 4, 5}, 3)
fmt.Println(idx, found) // 2 true

// Contains check
fmt.Println(slices.Contains([]string{"a", "b", "c"}, "b")) // true

// Collect a filtered subset
evens := slices.DeleteFunc(slices.Clone(nums), func(n int) bool { return n%2 != 0 })
fmt.Println(evens) // [4]
```

**`maps` package** (pkg.go.dev/maps) — generic operations on maps:

```go
import "maps"

m := map[string]int{"a": 1, "b": 2, "c": 3}

// Collect all keys (order is non-deterministic)
keys := slices.Collect(maps.Keys(m))

// Collect all values
values := slices.Collect(maps.Values(m))

// Clone a map
m2 := maps.Clone(m)

// Copy one map into another (keys from src overwrite dst)
maps.Copy(m2, map[string]int{"d": 4})
```

**`cmp` package** (pkg.go.dev/cmp) — comparison utilities:

```go
import "cmp"

// cmp.Compare returns -1, 0, or +1 — like C's strcmp but for any Ordered type
fmt.Println(cmp.Compare(3, 5))     // -1 (3 < 5)
fmt.Println(cmp.Compare(5, 5))     // 0
fmt.Println(cmp.Compare(7, 5))     // 1 (7 > 5)
fmt.Println(cmp.Compare("a", "b")) // -1

// cmp.Ordered is the constraint — any type with <, <=, >, >=, ==, !=
// Works with ~int, ~float64, ~string and their named aliases
```

> [!TIP]
> When you need to sort a slice of structs, the idiomatic pattern is `slices.SortFunc` with `cmp.Compare` inside the comparator. This replaces the old `sort.Slice` + anonymous function pattern and is both more readable and type-safe.

---

### Implementation: GC Shape Stenciling and Dictionaries

Understanding Go's implementation approach helps set expectations for performance.

Go compiles generics using a hybrid strategy called **GC shape stenciling**. The compiler groups type arguments by their *GC shape* — their memory layout as seen by the garbage collector. All pointer types share one GC shape (a pointer); all `int`-sized scalars share another; etc.

For each unique GC shape, the compiler generates one copy of the function's machine code. A **dictionary** is passed alongside each call to carry type-specific information (size, comparison functions, method tables). This means:

- Generic code over `*T` for different types of `T` all share the same machine code (one stencil for all pointer types)
- Generic code over `int`, `int32`, and `float64` may get separate stencils (different sizes)
- There is a small overhead compared to a fully monomorphized implementation (C++ templates generate one copy per concrete type)

**Practical implications:**

- Generic code is generally slightly slower than monomorphized code (C++ templates), but often equal to or faster than equivalent `interface{}` code (which requires heap allocation and indirection)
- For tight numeric inner loops, manually instantiating or writing concrete code may still outperform a generic equivalent
- For container types and utility functions, the overhead is negligible

> [!NOTE]
> The implementation details are stable as of Go 1.22 but remain an implementation detail, not a spec guarantee. The spec guarantees correctness; performance characteristics may improve in future releases. For deep profiling, see [[go/11. Testing and Benchmarking]] and the `pprof` tooling in later modules.

---

### How the Concepts Fit Together

```
Type Parameter [T constraint]
        │
        ├── Constraint (interface)
        │       ├── Method set: T must implement these methods
        │       ├── Type set: T must be one of these types (|)
        │       └── Underlying type (~T): named types included
        │
        ├── Type Inference
        │       └── Compiler solves for T from call-site arguments
        │
        ├── Generic Functions
        │       └── func F[T C](args) → operates on T values using C operations
        │
        ├── Generic Types (structs)
        │       └── type S[T C] struct{} → data structure for any T
        │           └── Methods on S[T] use T but cannot introduce new params
        │
        └── Standard Packages
                ├── slices — Sort, SortFunc, Contains, BinarySearch, ...
                ├── maps  — Keys, Values, Clone, Copy, ...
                └── cmp   — Compare, Ordered constraint
```

Generic functions and types are the mechanism. Constraints are the grammar that specifies what the mechanism can do. Type inference is the ergonomic layer that removes boilerplate. The standard packages are the immediate practical payoff.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Using `any` when you need `comparable`**
>
> A type parameter constrained by `any` cannot be compared with `==`, used as a map key, or stored in a set. The constraint `any` permits no type-specific operations — it only permits assigning, passing, and returning values.
>
> **Wrong (compile error):**
> ```go
> func Contains[T any](s []T, target T) bool {
>     for _, v := range s {
>         if v == target { // error: invalid operation: v == target (T is not comparable)
>             return true
>         }
>     }
>     return false
> }
> ```
>
> **Right:**
> ```go
> func Contains[T comparable](s []T, target T) bool {
>     for _, v := range s {
>         if v == target { // OK: comparable constraint permits ==
>             return true
>         }
>     }
>     return false
> }
> ```
>
> **Why this matters:** The compiler catches this at function definition time (not call time), so you'll see the error immediately. The fix is mechanical: change the constraint to `comparable`.

> [!WARNING]
> **Mistake 2: Forgetting `~` and wondering why named types don't work**
>
> If you write a constraint like `int | float64` (without `~`), then a user-defined type like `type Celsius float64` will not satisfy the constraint — even though its underlying type is `float64`. The bare union requires the *exact* predeclared types.
>
> **Wrong (Celsius does not satisfy Float):**
> ```go
> type Float interface { float32 | float64 }
>
> func ToFloat[T Float](v T) float64 { return float64(v) }
>
> type Celsius float64
> _ = ToFloat(Celsius(100)) // compile error: Celsius does not satisfy Float
> ```
>
> **Right (use ~ to include named types with matching underlying types):**
> ```go
> type Float interface { ~float32 | ~float64 }
>
> func ToFloat[T Float](v T) float64 { return float64(v) }
>
> type Celsius float64
> _ = ToFloat(Celsius(100)) // OK now
> ```
>
> **Why this matters:** Most useful constraints should use `~` to be inclusive of named types. The `cmp.Ordered` constraint already does this. If you write raw union constraints for library code, always ask: "should custom types based on this underlying type be included?" — usually the answer is yes.

> [!WARNING]
> **Mistake 3: Trying to add a new type parameter to a method**
>
> Methods on a generic type can reference the type's existing type parameters, but cannot introduce new ones. This compiles fine for `T`:
> ```go
> func (s *Stack[T]) Push(v T) { ... } // OK
> ```
> But this does not compile:
> ```go
> // compile error: method cannot have type parameters
> func (s *Stack[T]) Map[U any](f func(T) U) []U { ... }
> ```
>
> **Right (package-level function instead):**
> ```go
> func StackMap[T, U any](s *Stack[T], f func(T) U) []U {
>     result := make([]U, s.Len())
>     for i, v := range s.items {
>         result[i] = f(v)
>     }
>     return result
> }
> ```
>
> **Why this matters:** This restriction surprises everyone coming from languages where generic methods are allowed (Java, C#, Rust). The workaround — package-level functions — is idiomatic Go and works well in practice.

**Other pitfalls:**

- **Reaching for generics when an interface suffices** — if your function only calls methods on its argument (not operators like `<`, not equality), a plain interface is simpler and more readable than a generic function; use generics when you need operators or need to preserve the concrete type
- **Instantiating the same generic function millions of times with different types** — each unique GC shape may produce a separate stencil; in hot loops with many distinct pointer types this can increase binary size; profile before optimizing

---

## Mental Models

### Mental Model 1: Constraints as "What You Can Do"

Think of a type parameter `T constraint` not as "T is one of these types" but as "T supports these operations." The constraint defines a *capability set*. `any` means no operations beyond assignment and passing. `comparable` adds `==` and `!=`. `cmp.Ordered` adds `<`, `<=`, `>`, `>=`. A method-set constraint like `io.Reader` adds `.Read()`.

When writing a generic function, ask: "What do I actually need to *do* with T?" Then pick the tightest constraint that permits exactly those operations. Tight constraints make the function's contract clear to callers.

This model breaks down slightly for union-type constraints (where the constraint is about which types are valid, not just what you can do), but it's the right starting point.

### Mental Model 2: Type Parameters as "Fill in the Blank"

A generic function is a function with a blank for the concrete type. `func Min[T cmp.Ordered](a, b T) T` is like a template with a blank: `Min[___](a, b ___) ___`. The blank gets filled in at each call site — `Min[int]`, `Min[float64]`, `Min[string]` — and the compiler checks that the filled-in type satisfies the constraint.

This model makes type inference intuitive: the compiler sees `Min(3, 7)`, observes that `3` and `7` are `int`, and fills in the blank automatically. You don't need to write `Min[int](3, 7)` because the blank fills itself.

This model breaks down for constraints that combine type sets and method sets — at that point, you need the "capability set" model.

### Mental Model 3: When to Use Generics (The Three Scenarios)

The Go blog post "When To Use Generics" identifies three scenarios where generics genuinely help:

1. **Functions that work on slices, maps, or channels of any element type** — the operations you perform are on the container (append, range, `[]`) not on the elements themselves; `func Keys[K comparable, V any](m map[K]V) []K` is a perfect example
2. **General-purpose data structures** — a stack, queue, set, ordered map, graph — the data structure's logic is independent of what it stores; write it once with generics
3. **Functions that work on both integer and float types** (or other type groups with shared operators) — `Min`, `Max`, `Abs`, `Sum` over numeric types; `cmp.Compare` over ordered types

Scenarios where generics are *not* the right tool:

- The function only calls methods defined on an interface — use the interface directly
- The different types require different logic for each type (not a shared algorithm) — use overloading patterns or separate functions
- You are prototyping or the function is called only once — don't add complexity for future flexibility you may never need

> [!NOTE]
> The official "When To Use Generics" blog post (go.dev/blog/when-generics) is worth reading in full. It distills the Go team's guidance on when generics help versus when they add complexity without benefit. The short version: write concrete code first, reach for generics when you are actually writing the same algorithm more than once.

---

## Practical Examples

### Example 1: Generic Min and Max _(Basic)_

**Scenario:** You need `Min` and `Max` for both integers and floats. Pre-generics, you'd write `MinInt`, `MinFloat64`, etc. With generics, one function works for all ordered types.

**Goal:** Show the simplest useful generic function and type inference.

```go
package main

import (
    "cmp"
    "fmt"
)

// Min returns the smaller of two values.
// T must be cmp.Ordered (supports <, <=, etc.)
func Min[T cmp.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Max returns the larger of two values.
func Max[T cmp.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

func main() {
    // Type inference in action — no need to write Min[int] or Max[float64]
    fmt.Println(Min(3, 7))             // 3
    fmt.Println(Max(3, 7))             // 7
    fmt.Println(Min(3.14, 2.71))       // 2.71
    fmt.Println(Max("apple", "zebra")) // zebra

    // Named types based on int also satisfy cmp.Ordered via ~int
    type Priority int
    fmt.Println(Min(Priority(1), Priority(5))) // 1
}
```

**Output:**
```
3
7
2.71
zebra
1
```

**What to notice:** The single `Min` function works for `int`, `float64`, `string`, and the user-defined `Priority` type — all without type assertions or runtime checks. The compiler verifies at each call site that the argument types satisfy `cmp.Ordered`.

---

### Example 2: Generic Stack Container _(Intermediate)_

**Scenario:** You want a last-in, first-out stack that is type-safe for any element type. Pre-generics, you'd either use `[]interface{}` (no type safety) or write one stack per element type (code duplication).

**Goal:** Demonstrate a complete generic type with methods — the idiomatic container pattern.

```go
package main

import "fmt"

// Stack[T] is a generic LIFO container.
type Stack[T any] struct {
    items []T
}

// Push adds v to the top.
func (s *Stack[T]) Push(v T) {
    s.items = append(s.items, v)
}

// Pop removes and returns the top item.
// Returns zero value and false if empty.
func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    last := len(s.items) - 1
    v := s.items[last]
    s.items = s.items[:last]
    return v, true
}

// Peek returns the top item without removing it.
func (s *Stack[T]) Peek() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    return s.items[len(s.items)-1], true
}

// Len returns the number of items.
func (s *Stack[T]) Len() int { return len(s.items) }

func main() {
    // Integer stack
    var nums Stack[int]
    nums.Push(1)
    nums.Push(2)
    nums.Push(3)
    fmt.Printf("len=%d, peek=%v\n", nums.Len(), func() int { v, _ := nums.Peek(); return v }())
    for nums.Len() > 0 {
        v, _ := nums.Pop()
        fmt.Print(v, " ")
    }
    fmt.Println()
    // Output: len=3, peek=3
    //         3 2 1

    // String stack — same code, different type argument
    var words Stack[string]
    words.Push("hello")
    words.Push("world")
    w, _ := words.Pop()
    fmt.Println(w) // world
}
```

**Output:**
```
len=3, peek=3
3 2 1
world
```

**What to notice:** The `Stack` type is defined once. `Stack[int]` and `Stack[string]` are distinct types at compile time — you cannot push a string onto a `Stack[int]`. The zero value of `T` is obtained with `var zero T`, a common pattern when you need to return a zero value for an unknown type.

---

### Example 3: Generic Map, Filter, and Reduce _(Applied)_

**Scenario:** Functional-style slice transformations are common. Without generics they require `interface{}` and type assertions or one version per type. With generics, they are clean and type-safe.

**Goal:** Implement Map, Filter, and Reduce as generic functions and compose them.

```go
package main

import "fmt"

// Map applies f to each element of s and returns the results.
// Input slice has element type T; output slice has element type U.
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

// Filter returns elements of s for which keep returns true.
func Filter[T any](s []T, keep func(T) bool) []T {
    var result []T
    for _, v := range s {
        if keep(v) {
            result = append(result, v)
        }
    }
    return result
}

// Reduce combines elements of s into a single value using f.
// init is the initial accumulator value.
func Reduce[T, Acc any](s []T, init Acc, f func(Acc, T) Acc) Acc {
    acc := init
    for _, v := range s {
        acc = f(acc, v)
    }
    return acc
}

func main() {
    nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    // Map: square each number
    squares := Map(nums, func(n int) int { return n * n })
    fmt.Println("squares:", squares)
    // [1 4 9 16 25 36 49 64 81 100]

    // Filter: keep only evens
    evens := Filter(nums, func(n int) bool { return n%2 == 0 })
    fmt.Println("evens:", evens)
    // [2 4 6 8 10]

    // Reduce: sum
    sum := Reduce(nums, 0, func(acc, n int) int { return acc + n })
    fmt.Println("sum:", sum)
    // 55

    // Compose: sum of squares of even numbers
    result := Reduce(
        Filter(Map(nums, func(n int) int { return n * n }),
            func(n int) bool { return n%2 == 0 }),
        0,
        func(acc, n int) int { return acc + n },
    )
    fmt.Println("sum of squares of evens:", result)
    // 4 + 16 + 36 + 64 + 100 = 220

    // Map across types: int → string
    strs := Map(nums, func(n int) string { return fmt.Sprintf("item%d", n) })
    fmt.Println("first 3 strings:", strs[:3])
    // [item1 item2 item3]
}
```

**Output:**
```
squares: [1 4 9 16 25 36 49 64 81 100]
evens: [2 4 6 8 10]
sum: 55
sum of squares of evens: 220
first 3 strings: [item1 item2 item3]
```

**What to notice:** `Map` has two type parameters `[T, U any]` because the input and output element types can differ (e.g., `[]int` → `[]string`). The compiler infers both type parameters from the slice argument and the function argument. `Reduce` also uses two type parameters to allow the accumulator type to differ from the element type.

---

### Example 4: Using slices.SortFunc with cmp.Compare _(Applied)_

**Scenario:** You need to sort a slice of structs by a field. The old approach (`sort.Slice`) uses `interface{}` internally; the new approach (`slices.SortFunc`) is generic and type-safe.

**Goal:** Show idiomatic use of the standard generic packages, replacing the pre-1.21 boilerplate.

```go
package main

import (
    "cmp"
    "fmt"
    "slices"
)

type Employee struct {
    Name   string
    Salary int
    Dept   string
}

func main() {
    employees := []Employee{
        {"Alice", 95000, "Engineering"},
        {"Bob", 72000, "Marketing"},
        {"Carol", 110000, "Engineering"},
        {"Dave", 85000, "Marketing"},
        {"Eve", 72000, "Engineering"},
    }

    // Sort by Salary ascending
    slices.SortFunc(employees, func(a, b Employee) int {
        return cmp.Compare(a.Salary, b.Salary)
    })
    fmt.Println("By salary:")
    for _, e := range employees {
        fmt.Printf("  %-8s %6d  %s\n", e.Name, e.Salary, e.Dept)
    }

    // Sort by Dept then by Name (multi-key sort)
    slices.SortFunc(employees, func(a, b Employee) int {
        if c := cmp.Compare(a.Dept, b.Dept); c != 0 {
            return c // primary sort: department
        }
        return cmp.Compare(a.Name, b.Name) // tiebreak: name
    })
    fmt.Println("\nBy dept then name:")
    for _, e := range employees {
        fmt.Printf("  %-8s %-12s %6d\n", e.Name, e.Dept, e.Salary)
    }

    // slices.Contains, slices.Index for searching
    names := []string{"Alice", "Bob", "Carol"}
    fmt.Println("\nContains Bob:", slices.Contains(names, "Bob"))   // true
    fmt.Println("Index of Carol:", slices.Index(names, "Carol"))    // 2
}
```

**Output:**
```
By salary:
  Bob       72000  Marketing
  Eve       72000  Engineering
  Dave      85000  Marketing
  Alice     95000  Engineering
  Carol    110000  Engineering

By dept then name:
  Alice    Engineering   95000
  Carol    Engineering  110000
  Eve      Engineering   72000
  Bob      Marketing     72000
  Dave     Marketing     85000

Contains Bob: true
Index of Carol: 2
```

**What to notice:** `slices.SortFunc` is fully type-safe — the comparator receives `Employee` values directly, not `interface{}`. `cmp.Compare` returns `-1`, `0`, or `+1`, making multi-key sorts a natural chained expression. The entire pattern is shorter and more readable than the equivalent `sort.Slice` + manual field access.

---

### Example 5: When NOT to Use Generics — The Interface Alternative _(Edge Case)_

**Scenario:** You have a `Writer` abstraction and want to write a function that works with multiple concrete types. Is this a generics use case?

**Goal:** Illustrate the key design decision: method-dispatch polymorphism belongs to interfaces, not generics.

```go
package main

import (
    "fmt"
    "os"
)

// --- The WRONG approach: unnecessary generic ---
// This is overcomplicated. The function only calls Write() — use the interface.
func WriteAllGeneric[T interface{ Write([]byte) (int, error) }](w T, data []byte) error {
    _, err := w.Write(data)
    return err
}

// --- The RIGHT approach: plain interface ---
// io.Writer is already an interface. Just use it.
// This is simpler, more readable, and works with dynamic dispatch.
func WriteAll(w interface{ Write([]byte) (int, error) }, data []byte) error {
    _, err := w.Write(data)
    return err
}

// --- When generics ARE appropriate ---
// We need to return a *value of the concrete type*, not an interface.
// A function that creates a new writer of the same type as the input needs generics.
func Tee[W interface{ Write([]byte) (int, error) }](w W, mirror *os.File) WriterPair[W] {
    return WriterPair[W]{primary: w, mirror: mirror}
}

type WriterPair[W interface{ Write([]byte) (int, error) }] struct {
    primary W
    mirror  *os.File
}

func main() {
    // The plain interface function is cleaner for simple dispatch
    err := WriteAll(os.Stdout, []byte("hello interface\n"))
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
    }
    // Output: hello interface
}
```

**What to notice:** When a function only calls methods on its argument and does not need to preserve or return the concrete type, a plain interface is the right tool. Generics add syntax complexity without benefit in this case. The rule of thumb: if your constraint is entirely method-based and you don't need the concrete type in the return value, use a plain interface.

---

## Common Pitfalls

### Pitfall: Over-generalizing Everything

Generics are a powerful abstraction, and a freshly-exposed Go developer may be tempted to make every function generic. Resist this. Generics make code harder to read at a glance (more syntax, more indirection) and may incur a small performance cost. The right question is always: "Is there actual duplication or type-safety loss I'm solving?"

If you find yourself writing `[T any]` where `T` only appears once and is never constrained, that is almost always a sign the function should either use a concrete type or a plain interface.

### Pitfall: Constraint Proliferation

Defining many bespoke constraints (`type NumberLike interface { ~int | ~float64 }`, `type Addable interface { ... }`, etc.) leads to constraint soup. Prefer:

1. `cmp.Ordered` for anything orderable
2. `comparable` for anything that needs `==`
3. `any` for anything you only need to store or pass
4. Method-set interfaces from `io`, `fmt`, etc. for behavior

Create a custom constraint only when none of the above suffice.

### Pitfall: Forgetting the Zero Value Pattern

When a generic function needs to return a "nothing" value for type `T`, you cannot write `return nil` (nil is only valid for pointer, slice, map, function, channel, and interface types). The correct pattern is:

```go
var zero T
return zero, false
```

Or, more concisely using the two-expression return idiom for named returns. The `var zero T` pattern is idiomatic Go and produces the zero value of whatever `T` is instantiated with.

---

## Related Concepts

Within this topic:

- [[go/6. Methods and Interfaces]] — constraints are interfaces; understanding interface mechanics (method sets, structural typing, type assertions) is prerequisite to understanding constraints
- [[go/4. Composite Types]] — the generic packages `slices` and `maps` operate on slices and maps; the `Stack[T]` and `Set[T]` containers wrap slices and maps internally
- [[go/11. Testing and Benchmarking]] — testing generic functions requires table-driven tests with multiple type arguments; benchmarking generic vs concrete vs interface implementations reveals the performance tradeoffs described in the implementation section

In other areas of this knowledge base:

- [[concurrency]] — generic patterns interact with concurrency when building thread-safe generic containers; a `sync.Mutex`-protected `Stack[T]` is a common pattern in concurrent programs
- [[memory-management]] — GC shape stenciling (the generics implementation) directly affects memory layout; understanding which GC shapes produce separate stencils is relevant for performance-critical generic code

---

## Summary

Go generics, added in Go 1.18, solve the long-standing tension between reusability and type safety. The core syntax is `func Name[T constraint](args)` for generic functions and `type Name[T constraint] struct{}` for generic types. Constraints are interfaces: they describe what a type parameter can *do*, using method sets, type unions (`|`), and the `~` underlying-type operator to include named types.

The two most important built-in constraints are `any` (no operations) and `comparable` (equality). For ordered operations, use `cmp.Ordered`. The standard `slices`, `maps`, and `cmp` packages (Go 1.21) are the immediate practical payoff — they replace decades of boilerplate with generic, type-safe functions.

Key restrictions to remember: methods cannot introduce new type parameters (use package-level functions instead), and the Go implementation uses GC shape stenciling rather than full monomorphization. Key design guidance: reach for generics when you are writing the same algorithm for multiple types, not when a plain interface suffices.

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Generic Min/Max** _(Easy)_
>
> Write `Min[T]` and `Max[T]` functions constrained by `cmp.Ordered` and verify they work for `int`, `float64`, and `string`.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-generic-minmax--easy--1-pt)

The exercises range from basic generic function writing through building a complete generic Stack and implementing Map/Filter/Reduce.

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

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[An Introduction To Generics — The Go Blog](https://go.dev/blog/intro-generics)** — Robert Griesemer and Ian Lance Taylor; the canonical first read after this module; explains the design rationale, type parameter syntax, and the constraint-as-interface insight with concrete examples
2. **[When To Use Generics — The Go Blog](https://go.dev/blog/when-generics)** — Ian Lance Taylor; the official guidance on the three scenarios where generics help and the cases where a plain interface or concrete code is better; essential for writing idiomatic code
3. **[Go 1.18 Release Notes — Generics](https://go.dev/doc/go1.18)** — the release notes section on generics documents the exact syntax, the `any` alias, `comparable`, and the `golang.org/x/exp/constraints` package that predated `cmp`
4. **[pkg.go.dev/slices](https://pkg.go.dev/slices)** — the complete API reference for the standard `slices` package; read the function list to understand what operations are now available generically
5. **[pkg.go.dev/maps](https://pkg.go.dev/maps)** — the complete API reference for the standard `maps` package
6. **[pkg.go.dev/cmp](https://pkg.go.dev/cmp)** — the complete API reference for the `cmp` package; includes the definition of `cmp.Ordered` and `cmp.Compare`
7. **"Learning Go" — Jon Bodner (2nd ed.), Chapter 8** — covers generics in depth with the same professional audience in mind; includes worked examples of generic containers and a clear explanation of when to use generics vs interfaces

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 10

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
