# Module 4: Composite Types

[← Module 3: Functions](../3.%20Functions/) | [Topic Home](../README.md) | [Module 5: Pointers →](../5.%20Pointers/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner--intermediate-blue)
![Time](https://img.shields.io/badge/time-5--7h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Arrays — Fixed-Size Value Types](#arrays--fixed-size-value-types)
  - [Slices — Dynamic Windows into Arrays](#slices--dynamic-windows-into-arrays)
  - [Maps — Hash Tables with Comparable Keys](#maps--hash-tables-with-comparable-keys)
  - [Strings, Runes, and Bytes](#strings-runes-and-bytes)
  - [Structs — Heterogeneous Data Records](#structs--heterogeneous-data-records)
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

This module covers **Go's composite types**: arrays, slices, maps, strings/runes/bytes, and structs. These are the data structures every Go program uses daily. They are the building blocks you reach for to represent lists, dictionaries, Unicode text, and records — and understanding their mechanics, not just their syntax, is what separates fluent Go from imitative Go.

The central tension of this module is **value semantics vs reference semantics**. Arrays and structs are value types — copying them copies all their data. Slices and maps are reference types — they contain an internal pointer, so copying them does not copy the underlying data. This distinction produces some of Go's most common bugs and is the foundational concept that [[go/5. Pointers]] builds on directly.

By the end of this module, you will understand not just how to use these types but *why* they work the way they do — including the slice header (pointer, length, capacity), how `append` triggers reallocation, why map iteration is deliberately random, and how struct memory layout affects performance. That mechanical understanding is what lets you reason about correctness and performance when writing real Go programs.

**Difficulty:** Beginner–Intermediate &nbsp;|&nbsp; **Estimated time:** 5–7 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Explain the difference between arrays and slices, and choose correctly between them — _given a requirement "fixed list of 4 cardinal directions" vs "variable-length list of user input", pick the right type and explain why_
2. Describe the slice header (pointer, length, capacity) and predict what happens when `append` triggers reallocation — _trace through a grow-and-copy scenario in memory, identifying when two slice variables share an underlying array and when they do not_
3. Use maps correctly: create with `make`, read with comma-ok, delete, iterate, and implement a set — _write a word-frequency counter and a deduplication function without bugs_
4. Convert between `string`, `[]byte`, and `[]rune` and explain the memory cost of each conversion — _decide whether to use a `strings.Builder` or a `[]byte` buffer for a given text-processing task_
5. Define structs with embedded types, use struct literals safely, and understand how struct tags work at a high level — _define a `Person` struct with an embedded `Address`, populate it with a composite literal, and forward-reference why struct tags matter for JSON encoding_

---

## Prerequisites

### Required Modules

- [[go/1. Types and Variables]] — you need to understand: Go's basic types (`int`, `string`, `bool`), zero values, short variable declaration (`:=`), and type conversion syntax; composite types are built on top of basic types
- [[go/2. Control Flow]] — you need to understand: `for range` iteration (used everywhere with slices and maps), `if err != nil` for error handling, and `defer` (used in examples)
- [[go/3. Functions]] — you need to understand: function signatures, multiple return values, and closures; the `append` and `copy` built-ins are functions, and several patterns in this module use function values

### Required Concepts

- **Value vs reference semantics** — you should have a vague intuition that some assignments copy data and others copy a pointer; this module makes that intuition precise and correctness-critical
- **The zero value** — every type in Go has a zero value; for slices it is `nil`, for maps it is `nil`, for structs it is a struct with all fields zeroed; knowing this prevents "why is my map nil?" panics
- **UTF-8 encoding basics** — you should know that Go source code is UTF-8, that `len(s)` returns bytes not characters, and that `range` over a string yields runes; the Strings section deepens this

> [!TIP]
> If the phrase "slice header" means nothing to you yet, that is fine — this module defines it from scratch. But if you haven't done Module 2's `range` examples, do those first; this module uses `for range` over slices and maps constantly.

---

## Why This Matters

Composite types are the vocabulary of data in Go. Without them, you can only represent isolated scalar values. With them, you represent the data structures that real programs require: lists of records, lookup tables, text buffers, configuration, API responses.

Concretely, mastery of this module enables you to:

- **Write correct data-processing pipelines** — virtually every Go service reads input (a list of JSON records, a CSV file, a set of command-line arguments) into slices or maps, transforms it, and writes it out; a misunderstanding of slice sharing will produce silent data corruption bugs that are difficult to diagnose
- **Build lookup tables and sets** — Go maps are the standard way to implement frequency counters, caches, deduplication sets, and index structures; knowing the comma-ok idiom and the concurrency caveat (maps are not safe for concurrent access without synchronization — see [[go/9. Concurrency]]) is essential for writing production services
- **Define domain data models** — structs are how Go represents domain objects: a `User`, a `Request`, a `Config`, a `Transaction`; understanding embedding and struct tags is prerequisite to using encoding/json, database/sql, and most third-party libraries, which are covered in [[go/15. Reflection and Metaprogramming]]

Without composite types, you cannot model data, build collections, or define the domain objects that your program operates on — capabilities present in literally every non-trivial Go program.

---

## Historical Context

Go's composite types reflect deliberate design choices made in 2007–2009 during the language's initial design. Understanding the history clarifies why Go's types work differently from their counterparts in Python, Java, or C.

**Arrays** are present because Go is a systems language descended from C. C programmers understand fixed-size arrays directly mapped to memory. Go arrays are safer (bounds-checked) but philosophically similar.

**Slices** are Go's answer to a question that C, Java, and Python each answer differently: "how do you have a list-like abstraction that is efficient and safe?" C uses pointer arithmetic (unsafe). Java uses `ArrayList<T>` (heap-allocated, indirect). Python uses built-in lists (dynamically typed, GC-managed). Go's slice — a three-word header (pointer, length, capacity) backed by an array — gives you the efficiency of C with bounds safety, and the ergonomics of a dynamic list, with explicit control over allocation via `make`.

Key moments:

- **2007–2009** — Rob Pike and Russ Cox designed the slice header explicitly; the "append" built-in was added to make growing slices ergonomic without requiring pointer arithmetic
- **2009** — Go 1 pre-release; maps are built-in (not in the standard library), with deliberate iteration randomization to prevent programs from accidentally depending on insertion order
- **2012** — Go 1.0 release with the compatibility promise; the built-in `delete` function for maps and the three-index slice expression are present
- **2013** — Russ Cox's blog post "Go Slices: usage and internals" becomes the canonical explanation of the slice header; it remains essential reading
- **2021** — Go 1.21 introduces the `slices` and `maps` standard packages, providing generic utility functions (`slices.Sort`, `maps.Keys`, etc.) that previously required manual implementation
- **2022** — Go 1.21's `slices.Contains`, `slices.Index`, and `maps.Clone` reduce boilerplate that Go programmers had written for 10 years by hand

Understanding this history explains why `append` returns a new slice (because the underlying array may be reallocated), why map iteration is random (a deliberate anti-foot-gun decision), and why there are two packages for slice utilities — the original built-ins (`append`, `copy`, `len`, `cap`) and the newer `slices` package for richer operations.

---

## Core Concepts

### Arrays — Fixed-Size Value Types

An array in Go is a **fixed-size, value-typed sequence of elements of the same type**. Its size is part of its type: `[4]int` and `[5]int` are distinct, incompatible types.

```go
// Array declaration — size is part of the type
var dirs [4]string
dirs[0] = "north"
dirs[1] = "south"
dirs[2] = "east"
dirs[3] = "west"

// Array literal — initialize all elements at once
primes := [5]int{2, 3, 5, 7, 11}

// Let the compiler count the elements (... syntax)
vowels := [...]string{"a", "e", "i", "o", "u"} // type is [5]string

fmt.Println(len(primes)) // 5
fmt.Println(primes[0])   // 2
```

**Value semantics** — the critical property. When you assign an array to a variable or pass it to a function, Go copies every element:

```go
a := [3]int{1, 2, 3}
b := a         // b is a full copy — separate data
b[0] = 99

fmt.Println(a) // [1 2 3] — unchanged
fmt.Println(b) // [99 2 3]
```

This makes arrays safe to pass around without aliasing concerns, but also expensive if the array is large. For this reason, arrays are primarily used in two situations:

1. **Fixed-size cryptographic or protocol buffers** — `[32]byte` for a SHA-256 hash, `[16]byte` for a UUID — where the exact size is semantically meaningful and you want a stack-allocatable, copyable value
2. **As the backing store for a slice** — the most common use; you rarely declare arrays directly in application code; instead, `make([]T, n)` allocates an array internally and wraps it in a slice

```go
// Iterating an array
for i, v := range primes {
    fmt.Printf("primes[%d] = %d\n", i, v)
}

// Two-dimensional array
var matrix [3][3]int
matrix[1][2] = 7
```

> [!NOTE]
> In practice, you will rarely write `[N]T` in application code. The vast majority of Go code uses slices (`[]T`), not arrays. Arrays are important to understand because slices are defined in terms of them, and because fixed-size byte arrays appear in cryptographic and low-level code.

---

### Slices — Dynamic Windows into Arrays

A slice is the most important composite type in Go. Every Go programmer needs a deep understanding of how slices work, because slice bugs are the most common category of subtle correctness errors in Go code.

#### The Slice Header

A slice value is a **three-word struct** on the stack:

```
┌─────────────────┐
│  ptr  ─────────────────► [ underlying array in heap ]
├─────────────────┤        [ e1 | e2 | e3 | e4 | e5  ]
│  len = 3        │
├─────────────────┤
│  cap = 5        │
└─────────────────┘
```

- **ptr**: a pointer to the first element of the slice within the underlying array
- **len**: the number of elements currently accessible through the slice
- **cap**: the number of elements from `ptr` to the end of the underlying array

This three-word header is what gets copied when you pass a slice to a function or assign it to a variable. The underlying array is **not** copied — both the original slice and the copy share the same backing array, which is the source of aliasing bugs.

```go
// Creating slices
s1 := []int{10, 20, 30, 40, 50} // slice literal — len=5, cap=5
s2 := make([]int, 3)             // make — len=3, cap=3, zero-initialized
s3 := make([]int, 3, 10)         // make with cap — len=3, cap=10

fmt.Println(len(s1), cap(s1)) // 5 5
fmt.Println(len(s2), cap(s2)) // 3 3
fmt.Println(len(s3), cap(s3)) // 3 10
```

#### Slicing Expressions

A slice expression `a[low:high]` creates a new slice header pointing into the same backing array:

```go
a := []int{0, 1, 2, 3, 4, 5, 6, 7}

s := a[2:5]   // elements [2,5): {2, 3, 4}; len=3, cap=6
fmt.Println(s)           // [2 3 4]
fmt.Println(len(s))      // 3
fmt.Println(cap(s))      // 6  (from index 2 to end of backing array)

// Modifying through s modifies a — they share the array!
s[0] = 99
fmt.Println(a[2]) // 99 — a is affected
```

The three-index slice expression `a[low:high:max]` limits the capacity, preventing the new slice from extending further into the backing array:

```go
s2 := a[2:5:5] // len=3, cap=3 — cannot grow into a[5], a[6], a[7]
// This is the safe form when passing a sub-slice to a function
// that might append to it — it cannot overwrite a's elements beyond index 4
```

#### append and Reallocation

`append` adds elements to a slice, growing it if necessary:

```go
var s []int                 // nil slice: ptr=nil, len=0, cap=0
s = append(s, 1)            // allocates a new backing array
s = append(s, 2, 3)         // may reuse or reallocate
s = append(s, []int{4, 5}...) // append another slice (spread with ...)

fmt.Println(s) // [1 2 3 4 5]
```

**The critical rule**: always assign the return value of `append` back to the slice variable. `append` may or may not return a slice pointing to the original backing array, depending on whether there was enough capacity. If capacity was insufficient, Go allocates a new array (roughly double the current capacity), copies all existing elements, and returns a slice pointing to the new array. The original slice is unaffected.

```go
// Demonstrating reallocation — the original is unaffected
original := make([]int, 3, 3) // len=3, cap=3, fully packed
original[0], original[1], original[2] = 1, 2, 3

// append must reallocate because len == cap
grown := append(original, 4)
grown[0] = 99

fmt.Println(original) // [1 2 3] — original backing array unchanged
fmt.Println(grown)    // [99 2 3 4] — new backing array
```

The growth factor in Go's runtime is roughly 2x for small slices, transitioning to smaller multiples for large slices (Go 1.18+ uses a formula that approaches 1.25x for very large slices). The exact factor is not guaranteed by the specification.

#### copy

`copy(dst, src)` copies elements between slices that may overlap or be separate. It returns the number of elements copied (the minimum of `len(dst)` and `len(src)`):

```go
src := []int{1, 2, 3, 4, 5}
dst := make([]int, 3)
n := copy(dst, src) // copies min(3, 5) = 3 elements
fmt.Println(dst, n)  // [1 2 3] 3

// copy does not grow dst — the destination must already have len >= n
// To copy a whole slice safely:
clone := make([]int, len(src))
copy(clone, src)
// Now clone is an independent copy — modifying clone doesn't affect src
```

#### nil vs empty slice

```go
var nilSlice []int      // nil; len=0, cap=0; ptr=nil
emptySlice := []int{}   // non-nil; len=0, cap=0; ptr points to zerobase

fmt.Println(nilSlice == nil)   // true
fmt.Println(emptySlice == nil) // false
fmt.Println(len(nilSlice), len(emptySlice)) // 0 0

// Both are safe to range over (zero iterations) and to append to
for _, v := range nilSlice { fmt.Println(v) }   // no panic, no iterations
s := append(nilSlice, 1, 2, 3)
fmt.Println(s) // [1 2 3]
```

The distinction matters for JSON encoding (`nil` slice encodes as `null`; empty slice encodes as `[]`) and for API contracts where callers check `len(result) == 0` vs `result == nil`.

#### Removing Elements

Go has no built-in slice removal; it is done with slice expressions and `append`:

```go
s := []int{10, 20, 30, 40, 50}

// Remove element at index i (order-preserving, O(n))
i := 2
s = append(s[:i], s[i+1:]...)
fmt.Println(s) // [10 20 40 50]

// Remove element at index i (order-not-preserved, O(1))
j := 1
s[j] = s[len(s)-1]
s = s[:len(s)-1]
fmt.Println(s) // [10 50 40]  (order changed)
```

#### The slices Package (Go 1.21+)

Go 1.21 added the `slices` standard package with generic utility functions that previously required copy-paste boilerplate:

```go
import "slices"

s := []int{3, 1, 4, 1, 5, 9, 2, 6}

slices.Sort(s)
fmt.Println(s)                     // [1 1 2 3 4 5 6 9]
fmt.Println(slices.Contains(s, 5)) // true
fmt.Println(slices.Index(s, 5))    // 4

// Clone makes a full independent copy
clone := slices.Clone(s)
clone[0] = 99
fmt.Println(s[0]) // 1 — original unchanged
```

---

### Maps — Hash Tables with Comparable Keys

A map (`map[K]V`) is a hash table: an unordered collection of key-value pairs where keys are of type `K` and values are of type `V`. Keys must be **comparable** — any type for which `==` is defined and consistent: booleans, integers, floats, complex numbers, strings, pointers, channels, interfaces, arrays, and structs with all comparable fields. Slices, maps, and functions are not comparable and cannot be used as map keys.

#### Creating and Using Maps

```go
// Always initialize maps before use — a nil map panics on write
var bad map[string]int // nil map — reading returns zero value, but writing panics!

// Use make or a map literal
scores := make(map[string]int)
scores["Alice"] = 92
scores["Bob"] = 85
scores["Carol"] = 78

// Map literal
config := map[string]string{
    "host": "localhost",
    "port": "8080",
    "env":  "production",
}

fmt.Println(len(scores))        // 3
fmt.Println(scores["Alice"])    // 92
fmt.Println(scores["Unknown"])  // 0 — zero value for int, no panic
```

#### The Comma-Ok Idiom

Reading a missing key returns the zero value, making it impossible to distinguish "key not present" from "key present with zero value" using a single return value. Use the comma-ok idiom:

```go
v, ok := scores["Alice"]   // ok=true, v=92
fmt.Println(v, ok)

v, ok = scores["Xavier"]  // ok=false, v=0
fmt.Println(v, ok)

// Idiomatic: check existence before acting
if score, ok := scores["Alice"]; ok {
    fmt.Printf("Alice scored %d\n", score)
} else {
    fmt.Println("Alice not found")
}
```

#### delete and Iteration

```go
delete(scores, "Bob") // safe even if key doesn't exist

// Range over map — order is RANDOMIZED each time
for name, score := range scores {
    fmt.Printf("%s: %d\n", name, score)
}
```

**Map iteration order is deliberately random.** The Go runtime randomizes the starting position on each `range` to prevent programs from accidentally relying on insertion order (which is not guaranteed by the hash table implementation). If you need sorted output, extract keys into a slice and sort:

```go
import "slices"

keys := make([]string, 0, len(scores))
for k := range scores {
    keys = append(keys, k)
}
slices.Sort(keys)
for _, k := range keys {
    fmt.Printf("%s: %d\n", k, scores[k])
}
```

#### Maps as Sets

Go has no built-in set type. Use `map[T]struct{}` — the empty struct `struct{}` occupies zero bytes:

```go
seen := make(map[string]struct{})
words := []string{"apple", "banana", "apple", "cherry", "banana"}

for _, w := range words {
    seen[w] = struct{}{}
}

fmt.Println(len(seen)) // 3 — only unique words

_, ok := seen["apple"]
fmt.Println(ok) // true

// Some code uses map[T]bool instead — also common, slightly more readable
visited := map[string]bool{}
visited["page1"] = true
if visited["page2"] {
    fmt.Println("already visited")
}
```

#### Maps of Slices

A common pattern — map keys to lists of values:

```go
// Group words by their first letter
byLetter := make(map[string][]string)
words := []string{"apple", "ant", "banana", "blueberry", "cherry"}

for _, w := range words {
    letter := string(w[0]) // first byte as string (safe for ASCII)
    byLetter[letter] = append(byLetter[letter], w)
}

fmt.Println(byLetter["a"]) // [apple ant]
fmt.Println(byLetter["b"]) // [banana blueberry]
```

This works because `byLetter["a"]` returns `nil` for a missing key, and `append(nil, w)` creates a new slice — a clean interaction between maps and slices.

#### The maps Package (Go 1.21+)

```go
import "maps"

m := map[string]int{"a": 1, "b": 2, "c": 3}

clone := maps.Clone(m)   // independent copy
keys := maps.Keys(m)     // []string of all keys (unordered)
```

> [!WARNING]
> **Maps are not safe for concurrent use.** Reading and writing a map from multiple goroutines without synchronization causes a data race and will crash with "concurrent map read and write". Use `sync.Mutex`, `sync.RWMutex`, or `sync.Map` when maps are shared across goroutines. This is covered fully in [[go/9. Concurrency]].

---

### Strings, Runes, and Bytes

This section recaps and deepens the string mechanics introduced in [[go/1. Types and Variables]] and [[go/2. Control Flow]].

A Go `string` is an **immutable, read-only slice of bytes** — specifically, a two-word header (pointer to UTF-8 data, byte length). Because strings are immutable, any "modification" creates a new string:

```go
s := "Hello, 世界"

fmt.Println(len(s))            // 13 — byte count, not character count
fmt.Println([]byte(s))         // the raw UTF-8 bytes
fmt.Println([]rune(s))         // Unicode code points; len=9
```

#### Conversions

```go
// string → []byte: copies bytes; safe to mutate
b := []byte("Hello")
b[0] = 'h'
fmt.Println(string(b)) // "hello" — conversion back copies again

// string → []rune: copies; gives character-level access
r := []rune("café")
fmt.Println(len(r))    // 4 — rune count
r[3] = '!'
fmt.Println(string(r)) // "caf!"

// Conversion costs: each string↔[]byte and string↔[]rune conversion
// allocates and copies. For performance-sensitive code, use strings.Builder
// or bytes.Buffer to avoid repeated allocations.
```

#### Building Strings Efficiently

```go
import "strings"

// Naive concatenation in a loop: O(n²) allocations — avoid for large inputs
var bad string
for _, word := range words {
    bad += word + " " // each += creates a new string
}

// Use strings.Builder: O(n) — single allocation amortized
var b strings.Builder
for _, word := range words {
    b.WriteString(word)
    b.WriteByte(' ')
}
result := b.String()
```

#### Rune Literals and Unicode

```go
// Rune literals use single quotes; type is rune (alias for int32)
r := 'é'           // U+00E9
fmt.Printf("%c %d %U\n", r, r, r) // é 233 U+00E9

// Converting an int to a rune and then to string
fmt.Println(string(rune(0x1F600))) // 😀
```

> [!NOTE]
> The `strings` package is your primary tool for string manipulation: `strings.Contains`, `strings.Split`, `strings.Join`, `strings.TrimSpace`, `strings.ReplaceAll`, and more. The `strconv` package handles conversions between strings and numeric types. Prefer these over manual byte manipulation.

---

### Structs — Heterogeneous Data Records

A struct is a composite type that groups fields of different types under a single name. Structs are **value types** — assignment copies all fields.

#### Declaration and Literals

```go
// Struct type declaration
type Point struct {
    X float64
    Y float64
}

type Person struct {
    Name    string
    Age     int
    Email   string
}

// Struct literal — field names make it safe against field reordering
p := Person{
    Name:  "Alice",
    Age:   30,
    Email: "alice@example.com",
}

// Positional literal — fragile; avoid for structs with more than 2 fields
pt := Point{1.5, 2.5} // only acceptable for small, stable structs

fmt.Println(p.Name) // Alice
p.Age++
fmt.Println(p.Age)  // 31
```

#### Value Semantics

```go
a := Point{1, 2}
b := a          // full copy
b.X = 99

fmt.Println(a.X) // 1 — unchanged
fmt.Println(b.X) // 99
```

Passing a large struct to a function copies all fields. For large structs (or when the function needs to modify the original), use a pointer. This is the bridge to [[go/5. Pointers]] and [[go/6. Methods and Interfaces]].

#### Zero Value

A struct variable declared without initialization has all fields set to their zero values:

```go
var z Person
fmt.Println(z.Name)  // "" (empty string)
fmt.Println(z.Age)   // 0
fmt.Println(z.Email) // ""
```

#### Nested Structs and Embedding

Structs can nest other structs:

```go
type Address struct {
    Street string
    City   string
    State  string
}

type Employee struct {
    Name    string
    Age     int
    Address Address // nested — access as e.Address.City
}

e := Employee{
    Name: "Bob",
    Age:  28,
    Address: Address{
        Street: "123 Main St",
        City:   "Springfield",
        State:  "IL",
    },
}
fmt.Println(e.Address.City) // Springfield
```

**Embedding** (anonymous fields) promotes the embedded type's fields and methods to the outer struct — a form of composition that approximates inheritance:

```go
type Base struct {
    ID        int
    CreatedAt string
}

type User struct {
    Base           // embedded (anonymous) field — fields promoted
    Username string
    Email    string
}

u := User{
    Base:     Base{ID: 1, CreatedAt: "2024-01-01"},
    Username: "alice",
    Email:    "alice@example.com",
}

fmt.Println(u.ID)        // 1 — promoted from Base
fmt.Println(u.CreatedAt) // 2024-01-01 — promoted from Base
fmt.Println(u.Base.ID)   // also valid — explicit path
```

Embedding is composition, not inheritance — the embedded type does not become the outer type, and there is no polymorphism. It is a convenience that reduces boilerplate for common field sets (like timestamps, audit fields, or pagination).

#### Struct Comparison

Structs are comparable if all their fields are comparable. Two struct values are equal if all corresponding fields are equal:

```go
type Point struct{ X, Y int }

p1 := Point{1, 2}
p2 := Point{1, 2}
p3 := Point{3, 4}

fmt.Println(p1 == p2) // true
fmt.Println(p1 == p3) // false
```

Structs containing slices, maps, or functions are **not** comparable — `==` does not work on them.

#### The Empty Struct

`struct{}` is a zero-byte type. Its canonical use is as a map value type for sets, and as a channel signal type:

```go
done := make(chan struct{}) // signal channel
go func() {
    // ... do work ...
    close(done)
}()
<-done // wait for signal — no data transfer needed, so struct{}
```

#### Struct Tags (Forward Reference)

Fields can carry metadata called struct tags — string literals after the field type:

```go
type User struct {
    ID       int    `json:"id"         db:"user_id"`
    Username string `json:"username"   db:"username"`
    Password string `json:"-"`          // omit from JSON
}
```

Tags are invisible at runtime unless read through reflection. The `encoding/json` package uses them to map struct field names to JSON keys. The `database/sql` library uses `db` tags. Custom tags can be defined by any library. The mechanism — and how to read tags with `reflect` — is covered in depth in [[go/15. Reflection and Metaprogramming]].

#### Memory Layout and Alignment

Go aligns struct fields according to their type's alignment requirement (an `int64` requires 8-byte alignment; a `bool` requires 1-byte alignment). The compiler may insert padding bytes between fields to satisfy alignment:

```go
// Inefficient layout — 24 bytes due to padding
type Bad struct {
    A bool    // 1 byte + 7 bytes padding
    B float64 // 8 bytes
    C bool    // 1 byte + 7 bytes padding
}

// Efficient layout — 16 bytes, same fields
type Good struct {
    B float64 // 8 bytes
    A bool    // 1 byte
    C bool    // 1 byte + 6 bytes padding (tail padding to align the struct)
}
```

For performance-critical code with large slices of structs, field ordering matters. Use `unsafe.Sizeof(T{})` or the `fieldalignment` linter to inspect padding. In practice, readability should take precedence over layout optimization unless you have a measured performance problem.

---

### How the Concepts Fit Together

```
  Fixed-size, copied wholesale          Dynamic, shared header
  ┌─────────────────────┐              ┌───────────────────────────────┐
  │  Array [N]T         │──backing────►│  Slice []T                    │
  │  value semantics    │  array       │  (ptr | len | cap)            │
  └─────────────────────┘              │  reference semantics          │
                                       └───────────────────────────────┘
                                                   │
                                        append / copy / slicing

  ┌───────────────────────┐            ┌───────────────────────────────┐
  │  Map map[K]V          │            │  Struct type T struct{...}    │
  │  hash table           │            │  value semantics              │
  │  reference semantics  │            │  embedding = composition      │
  │  nil → panic on write │            │  tags = metadata for reflect  │
  └───────────────────────┘            └───────────────────────────────┘

  String (immutable []byte)
  []byte / []rune (mutable)
  strings.Builder (efficient building)
```

Arrays are rarely used directly; their primary role is as the backing store for slices. Slices are the workhorse sequential type. Maps are the workhorse associative type. Structs are the domain-modeling type. Strings are immutable text with UTF-8 encoding; `[]byte` and `[]rune` are the mutable equivalents for text processing.

The value-vs-reference distinction runs through everything: arrays and structs copy on assignment; slices and maps copy only their header, sharing the underlying data. This determines when you need a pointer — the topic of [[go/5. Pointers]].

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Writing to a nil map causes a panic**
>
> A map's zero value is `nil`. Reading from a nil map is safe (returns the zero value), but writing to a nil map panics at runtime. Always initialize a map with `make` or a literal before writing.
>
> **Wrong:**
> ```go
> var counts map[string]int // nil map
> counts["hello"]++         // panic: assignment to entry in nil map
> ```
>
> **Right:**
> ```go
> counts := make(map[string]int) // initialized
> counts["hello"]++              // fine: 0 + 1 = 1
> ```
>
> **Why this matters:** The nil-map panic is a runtime error that will not be caught at compile time. The type system cannot distinguish `nil` from an initialized map.

> [!WARNING]
> **Mistake 2: Forgetting that append may or may not reallocate — never assume the original slice is updated**
>
> `append` returns a new slice value. If you pass a slice to a function that appends to it but doesn't return the new slice, the caller's slice variable is unchanged.
>
> **Wrong:**
> ```go
> func addItem(s []int, item int) {
>     s = append(s, item) // modifies local copy of the header only
> }
>
> items := []int{1, 2, 3}
> addItem(items, 4)
> fmt.Println(items) // [1 2 3] — 4 was NOT added!
> ```
>
> **Right:**
> ```go
> func addItem(s []int, item int) []int {
>     return append(s, item) // return the new slice
> }
>
> items := []int{1, 2, 3}
> items = addItem(items, 4) // caller receives and assigns the result
> fmt.Println(items)        // [1 2 3 4]
> ```
>
> **Why this matters:** This is the most common slice bug in Go. The function receives a copy of the slice header. If `append` reallocates, the new backing array is visible only to the local copy. If `append` does not reallocate (enough capacity), the original backing array is mutated but the caller's header still has the old `len`, so the new element is not visible to the caller. Either way, the caller loses.

> [!WARNING]
> **Mistake 3: Assuming sub-slices are independent — they share the backing array**
>
> When you slice a slice with `a[2:5]`, the result shares the backing array with the original. Mutations through the sub-slice affect the original, and vice versa.
>
> **Wrong (unexpected mutation):**
> ```go
> data := []int{1, 2, 3, 4, 5}
> sub := data[1:3]  // shares backing array with data
> sub[0] = 99
> fmt.Println(data) // [1 99 3 4 5] — data was modified!
> ```
>
> **Right (when you need an independent copy):**
> ```go
> data := []int{1, 2, 3, 4, 5}
> sub := make([]int, 2)
> copy(sub, data[1:3])  // independent copy
> sub[0] = 99
> fmt.Println(data) // [1 2 3 4 5] — data is unchanged
> ```
>
> **Why this matters:** Passing sub-slices to functions that modify them produces action-at-a-distance bugs. When in doubt, use `copy` to make an independent slice.

> [!WARNING]
> **Mistake 4: Using a positional struct literal when field order changes**
>
> Positional struct literals (`Point{1, 2}`) break when someone adds, removes, or reorders struct fields. Named literals are robust to field changes.
>
> **Wrong:**
> ```go
> type Config struct {
>     Host    string
>     Port    int
>     Timeout int
> }
> c := Config{"localhost", 8080, 30} // breaks if fields change order
> ```
>
> **Right:**
> ```go
> c := Config{
>     Host:    "localhost",
>     Port:    8080,
>     Timeout: 30,
> }
> ```
>
> **Why this matters:** Positional struct literals are fragile. The compiler will catch the wrong number of fields but not the wrong order (if the types happen to be compatible). Go's `go vet` tool warns about positional struct literals for types from other packages.

**Other pitfalls:**

- **Ranging over a map and modifying it** — modifying a map during `range` iteration is allowed (unlike some languages), but the behavior for new keys added during iteration is undefined — they may or may not be visited
- **Using `len([]rune(s))` vs `utf8.RuneCountInString(s)`** — both give rune count, but `[]rune(s)` allocates; prefer `utf8.RuneCountInString(s)` when you only need the count
- **Comparing structs with `==` when they contain incomparable fields** — a struct containing a `[]int` field will cause a compile error if you try `s1 == s2`; use `reflect.DeepEqual` or write a custom equals method

---

## Mental Models

### Mental Model 1: The Slice as a View Through a Window

Think of the backing array as a long street, and a slice as a window that reveals a portion of that street. The window has a start position (`ptr`), a width you can see (`len`), and a maximum width it could expand to (`cap`). Multiple windows can look at overlapping or adjacent parts of the same street.

When you `append` beyond the window's maximum width, you get moved to a new, longer street (reallocation) and given a new window. The old street still exists, but your window no longer sees it.

This model breaks down when thinking about `copy` — `copy` is more like photocopying the visible part of the street onto a new piece of paper, giving you a completely independent copy.

### Mental Model 2: The Map as a Phone Book with a Hash Index

A map is like a phone book where the index is computed from the key (the hash), not alphabetical order. Given a name (key), you compute its hash, go to the right page, and either find the entry or not. Adding an entry places it on the hash-determined page. Looking up a missing entry returns a default result (zero value), not an error.

The hash is computed freshly each time — there is no "insertion order" preserved, which is why iteration order is randomized. This is the phone book page being reshuffled each time you open it.

This model is most useful when explaining why maps are O(1) for lookup (hash → direct access), why key types must be comparable (you need `==` to find the exact entry on a page), and why there is no built-in ordering.

### Mental Model 3: Structs as Named Tuples with Value Semantics

Think of a struct as a named tuple (like in Python) but with one crucial difference: in Go, assigning a struct always copies all fields. A `Person{Name: "Alice", Age: 30}` is not a reference to an object — it is the data itself, sitting inline wherever it is stored (on the stack if local, inline in the containing struct if nested).

This is most useful for understanding why Go does not have `null` object references — a `Person` variable always holds a valid `Person` value, never a null pointer (unless you use `*Person`). The zero value is a valid `Person` with empty fields.

This model breaks down when thinking about method dispatch and interfaces, where you sometimes need `*Person` to modify the receiver — the subject of [[go/5. Pointers]] and [[go/6. Methods and Interfaces]].

> [!NOTE]
> No single mental model is perfect. Use Model 1 (window on a street) when reasoning about slice aliasing and `append` reallocation. Use Model 2 (phone book with hash index) when reasoning about map lookup and key requirements. Use Model 3 (named tuple) when reasoning about struct value semantics and zero values.

---

## Practical Examples

### Example 1: Slice Growth and Aliasing _(Basic)_

**Scenario:** Demonstrate that sub-slices share backing arrays and that `append` can cause reallocation, breaking the sharing.

**Goal:** Build intuition for when two slice variables share data and when they become independent.

```go
package main

import "fmt"

func main() {
    // Create a slice with extra capacity
    base := make([]int, 5, 10)
    for i := range base {
        base[i] = i + 1
    }
    fmt.Printf("base:  %v  len=%d cap=%d\n", base, len(base), cap(base))
    // base: [1 2 3 4 5] len=5 cap=10

    // sub shares the backing array with base
    sub := base[1:4]
    fmt.Printf("sub:   %v  len=%d cap=%d\n", sub, len(sub), cap(sub))
    // sub: [2 3 4] len=3 cap=9

    // Mutating sub mutates base — shared backing array!
    sub[0] = 99
    fmt.Printf("base after sub[0]=99: %v\n", base)
    // base: [1 99 3 4 5]

    // Append to sub — fits in capacity, so NO reallocation
    sub2 := append(sub, 88)
    fmt.Printf("sub2:  %v  len=%d cap=%d\n", sub2, len(sub2), cap(sub2))
    // sub2: [99 3 4 88] len=4 cap=9
    fmt.Printf("base after append(sub,88): %v\n", base)
    // base: [1 99 3 4 88] — base[4] was overwritten!

    // Append beyond capacity — reallocation occurs
    bigSub := append(base, 100, 101, 102, 103, 104, 105) // exceeds cap=10
    bigSub[0] = 777
    fmt.Printf("base after overflowing append: %v\n", base)
    // base: unchanged — bigSub now has its own backing array
    _ = bigSub
}
```

**Output / Result:**
```
base:  [1 2 3 4 5]  len=5 cap=10
sub:   [2 3 4]  len=3 cap=9
base after sub[0]=99: [1 99 3 4 5]
sub2:  [99 3 4 88]  len=4 cap=9
base after append(sub,88): [1 99 3 4 88]
base after overflowing append: [1 99 3 4 88]
```

**What to notice:** The sub-slice `sub` initially shares data with `base`. An in-capacity `append` writes into the shared backing array, silently modifying `base[4]`. Only when `append` must reallocate does the new slice become independent. This is why passing a sub-slice to a function that appends is dangerous unless you use the three-index form `base[1:4:4]` to limit capacity.

---

### Example 2: Word Frequency Counter with Maps _(Intermediate)_

**Scenario:** Count word frequencies in a text, sort by count descending, and print the top results.

**Goal:** Demonstrate idiomatic map usage — creation, update via append-to-nil, sorted iteration.

```go
package main

import (
    "fmt"
    "slices"
    "strings"
)

func wordFrequency(text string) map[string]int {
    freq := make(map[string]int)
    // strings.Fields splits on any whitespace, handles multiple spaces
    for _, word := range strings.Fields(strings.ToLower(text)) {
        // Strip simple punctuation
        word = strings.Trim(word, ".,!?;:")
        if word != "" {
            freq[word]++
        }
    }
    return freq
}

func topN(freq map[string]int, n int) []string {
    type entry struct {
        word  string
        count int
    }

    entries := make([]entry, 0, len(freq))
    for word, count := range freq {
        entries = append(entries, entry{word, count})
    }
    // Sort descending by count, then ascending by word for stability
    slices.SortFunc(entries, func(a, b entry) int {
        if b.count != a.count {
            return b.count - a.count // descending count
        }
        return strings.Compare(a.word, b.word) // ascending name
    })

    result := make([]string, 0, min(n, len(entries)))
    for i := range min(n, len(entries)) {
        result = append(result, fmt.Sprintf("%-12s %d", entries[i].word, entries[i].count))
    }
    return result
}

func main() {
    text := "to be or not to be that is the question to be is to exist"
    freq := wordFrequency(text)
    fmt.Println("Top 5 words:")
    for _, line := range topN(freq, 5) {
        fmt.Println(" ", line)
    }
}
```

**Output / Result:**
```
Top 5 words:
  to           4
  be           3
  is           2
  exist        1
  not          1
```

**What to notice:** `freq[word]++` is idiomatic: the missing-key zero value (`0`) means the first increment correctly initializes the count to `1`. The `slices.SortFunc` call uses the new generic sort API from Go 1.21. The `topN` function uses a local struct `entry` to pair words with counts for sorting.

---

### Example 3: Struct Embedding and Composition _(Applied)_

**Scenario:** Model a simple user system where all domain types share audit fields (created/updated timestamps).

**Goal:** Show how embedding eliminates boilerplate while keeping types distinct; forward-reference struct tags.

```go
package main

import (
    "fmt"
    "time"
)

// Timestamps provides audit fields for all domain types.
// It is embedded (not named) to promote its fields.
type Timestamps struct {
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}

type Address struct {
    Street string `json:"street"`
    City   string `json:"city"`
    State  string `json:"state"`
    ZIP    string `json:"zip"`
}

type User struct {
    Timestamps                    // embedded — CreatedAt/UpdatedAt promoted
    ID         int    `json:"id"`
    Name       string `json:"name"`
    Email      string `json:"email"`
    Address    Address            // named (not embedded) — access as u.Address.City
}

func newUser(id int, name, email string) User {
    now := time.Now()
    return User{
        Timestamps: Timestamps{
            CreatedAt: now,
            UpdatedAt: now,
        },
        ID:    id,
        Name:  name,
        Email: email,
    }
}

func (u *User) updateEmail(email string) {
    u.Email = email
    u.UpdatedAt = time.Now() // UpdatedAt promoted from Timestamps
}

func main() {
    u := newUser(1, "Alice", "alice@example.com")
    fmt.Printf("User: %s (id=%d)\n", u.Name, u.ID)
    fmt.Printf("Created: %s\n", u.CreatedAt.Format(time.RFC3339))
    // u.CreatedAt is promoted from the embedded Timestamps

    u.updateEmail("alice@newdomain.com")
    fmt.Printf("Updated email: %s\n", u.Email)
    fmt.Printf("UpdatedAt changed: %v\n", u.UpdatedAt.After(u.CreatedAt))

    // Struct tags (json:...) are used by encoding/json
    // — covered in Module 13: Web Services and APIs
    // and mechanically in Module 15: Reflection and Metaprogramming
}
```

**Output / Result:**
```
User: Alice (id=1)
Created: 2024-01-15T10:30:00Z
Updated email: alice@newdomain.com
UpdatedAt changed: true
```

**What to notice:** `u.CreatedAt` works even though `CreatedAt` is defined on `Timestamps` — it is promoted by embedding. The `updateEmail` method uses a pointer receiver (`*User`) so it can modify the struct in place; without the pointer, the modifications would be lost. Struct tags (`json:"..."`) are visible in the source but have no effect without a library that reads them via reflection.

---

### Example 4: The append-in-a-Function Pitfall _(Edge Case)_

**Scenario:** A function that looks like it builds a result but silently fails because it doesn't return the slice.

```go
package main

import "fmt"

// WRONG: this function doesn't work as intended
func collectEven_WRONG(nums []int) {
    var result []int
    for _, n := range nums {
        if n%2 == 0 {
            result = append(result, n)
        }
    }
    // result is discarded when this function returns!
    // The caller has no way to see it.
    fmt.Println("inside:", result) // prints correctly, but...
}

// RIGHT: return the slice
func collectEven(nums []int) []int {
    var result []int
    for _, n := range nums {
        if n%2 == 0 {
            result = append(result, n)
        }
    }
    return result
}

// ALSO RIGHT: pass a pointer to the slice (less idiomatic for this case)
func collectEvenPtr(nums []int, out *[]int) {
    for _, n := range nums {
        if n%2 == 0 {
            *out = append(*out, n)
        }
    }
}

func main() {
    data := []int{1, 2, 3, 4, 5, 6, 7, 8}

    collectEven_WRONG(data)         // prints inside: [2 4 6 8]
    // but from outside:
    var wrongResult []int
    collectEven_WRONG(data)
    fmt.Println("wrong result:", wrongResult) // [] — never populated

    evens := collectEven(data)
    fmt.Println("correct result:", evens) // [2 4 6 8]
}
```

**Why this is important:** The Go compiler does not warn you when a function builds a slice but doesn't return it — it is syntactically valid. This is the "append doesn't modify the caller" pitfall in a common real-world form. The idiomatic fix is always to return the built slice. The pointer variant is less idiomatic for this use case but appears in libraries that accumulate into a pre-existing slice passed by the caller.

---

## Related Concepts

Within this topic:

- [[go/3. Functions]] — built-in functions `append`, `copy`, `make`, `delete`, `len`, and `cap` are the primary interface to composite types; understanding variadic functions explains `append(s, elems...)` spread syntax
- [[go/5. Pointers]] — the value-vs-reference semantics established in this module are the prerequisite for pointers; passing `*[]int` or `*map[K]V` or `*MyStruct` to functions is the other side of the same coin
- [[go/6. Methods and Interfaces]] — struct methods and interface implementation are the next layer built on top of structs; embedding in this module is the compositional foundation for interface satisfaction
- [[go/9. Concurrency]] — maps are not concurrency-safe; goroutine-shared maps require synchronization; this module introduces the footgun, Module 9 resolves it
- [[memory-management]] — Go's garbage collector manages the backing arrays of slices and maps; understanding escape analysis and heap vs stack allocation is the production-performance complement to the mechanical model in this module

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Slice Header Tracing** _(Easy)_
>
> Given a slice `s := []int{10, 20, 30, 40, 50}`, trace through a series of slicing expressions and `append` calls, predicting `len`, `cap`, and whether two slice variables share a backing array at each step.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-slice-header-tracing--easy--1-pt)

The exercises range from mechanical tracing warm-ups to a full generic data structure implementation. Complete at least the Easy and Medium exercises before taking the test.

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
Word Frequency Analyzer — read a text file (or standard input), tokenize it into words, count frequencies using a map, deduplicate using a set, sort results with `slices.SortFunc`, and format output as a table. Stretch goal: use a struct to represent each result row, with a method that formats it as a CSV line. This exercises all five composite types in a realistic data-processing context.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Go Slices: usage and internals — The Go Blog](https://go.dev/blog/slices-intro)** — Andrew Gerrand's canonical explanation of the slice header (pointer, length, capacity), slicing expressions, `copy`, and `append`; the definitive source for understanding slice mechanics; read before attempting the exercises
2. **[Arrays, slices (and strings): The mechanics of 'append' — The Go Blog](https://go.dev/blog/slices)** — Rob Pike's deeper follow-up covering `append` growth strategy, the three-index slice expression, and building byte buffers; supplements the first post with implementation detail
3. **[Effective Go — Slices and Maps](https://go.dev/doc/effective_go#slices)** — Idiomatic usage patterns from the official style guide; shorter than the blog posts but focuses on how experienced Go programmers actually use these types
4. **"The Go Programming Language" by Donovan & Kernighan — Chapter 4** — The book chapter on composite types (arrays, slices, maps, structs); the most comprehensive prose treatment; particularly strong on the mechanics of `append` and the struct embedding discussion
5. **"Learning Go" by Jon Bodner (2nd ed.) — Chapter 3** — Modern treatment covering the `slices` and `maps` packages (Go 1.21+) alongside the fundamentals; good on the nil-vs-empty slice distinction and the maps-are-not-concurrent-safe caveat
6. **[pkg.go.dev/slices](https://pkg.go.dev/slices)** and **[pkg.go.dev/maps](https://pkg.go.dev/maps)** — Official API documentation for the generic utility packages added in Go 1.21; check the function list before writing any boilerplate slice/map manipulation

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 4

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
