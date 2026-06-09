# Exercises — Module 10: Generics

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

## Exercise 1: Generic Min/Max [🟢 Easy] [1 pt]

### Context
The simplest useful generic functions operate over ordered types — types that support `<`, `<=`, etc. This exercise is the "Hello, World" of generics: one function that works for all ordered types.

### Task
Write two generic functions `Min[T cmp.Ordered](a, b T) T` and `Max[T cmp.Ordered](a, b T) T`. Call each function with at least three different types: `int`, `float64`, and `string`. Print the results.

### Requirements
- [ ] Both functions use `[T cmp.Ordered]` as the type parameter list
- [ ] Both functions compile and produce correct results for `int`, `float64`, and `string`
- [ ] Type inference is used at every call site (no explicit `Min[int](...)` required unless you want to show it)
- [ ] Import `"cmp"` and `"fmt"`

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The `cmp.Ordered` constraint is defined in the `cmp` package and covers all integer, float, and string types. The function body is identical to a concrete `MinInt` function, except `T` replaces `int` everywhere.

</details>

### Expected Output / Acceptance Criteria
```
Min(3, 7) = 3
Max(3, 7) = 7
Min(3.14, 2.71) = 2.71
Max(3.14, 2.71) = 3.14
Min("cat", "bat") = bat
Max("cat", "bat") = cat
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "cmp"
    "fmt"
)

// Min returns the smaller of two ordered values.
func Min[T cmp.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Max returns the larger of two ordered values.
func Max[T cmp.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

func main() {
    fmt.Println("Min(3, 7) =", Min(3, 7))
    fmt.Println("Max(3, 7) =", Max(3, 7))
    fmt.Println("Min(3.14, 2.71) =", Min(3.14, 2.71))
    fmt.Println("Max(3.14, 2.71) =", Max(3.14, 2.71))
    fmt.Println("Min(\"cat\", \"bat\") =", Min("cat", "bat"))
    fmt.Println("Max(\"cat\", \"bat\") =", Max("cat", "bat"))
}
```

**Explanation:**
`cmp.Ordered` is an interface constraint that includes `~int`, `~float64`, `~string`, and all other integer and float types. The `<` and `>` operators are permitted inside the function body because the constraint guarantees the type supports them. Type inference works here because both `a` and `b` are the same type `T` — when you call `Min(3, 7)`, the compiler sees two `int` arguments and infers `T = int`.

**Common wrong answers:**
- Using `any` instead of `cmp.Ordered` — `any` doesn't permit `<`; you'll get a compile error inside the function body
- Writing `Min[int](3, 7)` explicitly everywhere — this works but is unnecessarily verbose; type inference handles it

</details>

---

## Exercise 2: Generic Contains and Index [🟢 Easy] [1 pt]

### Context
Two operations are universally needed on slices: checking whether an element exists and finding its position. These require `==`, which requires `comparable`. This exercise reinforces the distinction between `any` and `comparable`.

### Task
Write `Contains[T comparable](s []T, target T) bool` and `Index[T comparable](s []T, target T) int` (returns -1 if not found). Test both with `[]int` and `[]string`.

### Requirements
- [ ] Both functions use `[T comparable]`
- [ ] `Contains` uses `==` to compare elements
- [ ] `Index` returns the zero-based index of the first match, or -1 if not found
- [ ] Tested with at least one integer slice and one string slice

### Hints
<details>
<summary>Hint 1</summary>

The `comparable` constraint permits `==` and `!=`. A `for _, v := range s` loop with `if v == target` is the standard linear scan.

</details>

### Expected Output / Acceptance Criteria
```
Contains([1 2 3], 2) = true
Contains([1 2 3], 9) = false
Index([a b c], "b") = 1
Index([a b c], "z") = -1
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Contains reports whether target is in s.
func Contains[T comparable](s []T, target T) bool {
    for _, v := range s {
        if v == target {
            return true
        }
    }
    return false
}

// Index returns the first index of target in s, or -1 if not present.
func Index[T comparable](s []T, target T) int {
    for i, v := range s {
        if v == target {
            return i
        }
    }
    return -1
}

func main() {
    fmt.Println("Contains([1 2 3], 2) =", Contains([]int{1, 2, 3}, 2))
    fmt.Println("Contains([1 2 3], 9) =", Contains([]int{1, 2, 3}, 9))
    fmt.Println("Index([a b c], \"b\") =", Index([]string{"a", "b", "c"}, "b"))
    fmt.Println("Index([a b c], \"z\") =", Index([]string{"a", "b", "c"}, "z"))
}
```

**Explanation:**
`comparable` is required because the function uses `==`. If you used `any`, the compiler would reject `v == target` with "invalid operation: cannot use == with T (constrained by any)". Note that the standard library's `slices.Contains` and `slices.Index` do exactly this — these generic implementations are the basis for those standard library functions.

</details>

---

## Exercise 3: Custom Constraint with ~ [🟡 Medium] [2 pts]

### Context
The `~` operator is what makes constraints practical for real-world codebases where user-defined named types are common. This exercise builds the muscle memory for writing `~`-inclusive constraints.

### Task
1. Define a `SignedInteger` interface constraint that covers all signed integer types (`~int`, `~int8`, `~int16`, `~int32`, `~int64`) using `~`.
2. Write a function `Abs[T SignedInteger](n T) T` that returns the absolute value.
3. Define `type Offset int64` and verify that `Abs` works with it (it should, because `~int64` includes `Offset`).
4. Also verify that `Abs` correctly rejects `float64` (it should fail to compile — include this as a comment, not as compiled code).

### Requirements
- [ ] `SignedInteger` uses `~` on every member type
- [ ] `Abs` compiles and produces correct results for `int`, `int32`, and the user-defined `Offset` type
- [ ] The program prints at least 3 results covering different instantiations

### Hints
<details>
<summary>Hint 1</summary>

The absolute value for a signed integer: if `n < 0`, return `-n`; otherwise return `n`. The `<` and unary `-` operators are permitted for signed integers.

</details>

<details>
<summary>Hint 2</summary>

The `SignedInteger` constraint cannot use `cmp.Ordered` (which includes floats and strings). You need a custom constraint that is *specifically* signed integers.

</details>

### Expected Output / Acceptance Criteria
```
Abs(-5) = 5
Abs(int32(-100)) = 100
Abs(Offset(-42)) = 42
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// SignedInteger covers all signed integer types, including named types
// whose underlying type is one of these (e.g., type Offset int64).
type SignedInteger interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64
}

// Abs returns the absolute value of a signed integer.
func Abs[T SignedInteger](n T) T {
    if n < 0 {
        return -n
    }
    return n
}

// Offset is a user-defined named type with underlying type int64.
// It satisfies SignedInteger via ~int64.
type Offset int64

func main() {
    fmt.Println("Abs(-5) =", Abs(-5))
    fmt.Println("Abs(int32(-100)) =", Abs(int32(-100)))
    fmt.Println("Abs(Offset(-42)) =", Abs(Offset(-42)))

    // The following would NOT compile — float64 does not satisfy SignedInteger:
    // fmt.Println(Abs(3.14))
    // compile error: float64 does not satisfy SignedInteger
}
```

**Explanation:**
Without `~`, `type Offset int64` would not satisfy a constraint containing `int64` — even though Offset's entire backing storage is an int64. The `~int64` element means "any type whose underlying type is int64," which includes `Offset`. The `<` and unary `-` operators are available because all members of `SignedInteger` support them. `float64` is correctly rejected because it is not in the union — the constraint is for signed integers only.

</details>

---

## Exercise 4: Generic Map, Filter, Reduce [🟡 Medium] [2 pts]

### Context
Functional-style slice transformations are a canonical generic use case — the same algorithm (transform each element, keep some elements, combine elements) applies to any element type. This exercise requires two type parameters (input type and output type), which appear frequently in real codebases.

### Task
Implement three functions:
- `Map[T, U any](s []T, f func(T) U) []U`
- `Filter[T any](s []T, keep func(T) bool) []T`
- `Reduce[T, Acc any](s []T, init Acc, f func(Acc, T) Acc) Acc`

Then use them to compute: the sum of the lengths of all strings in a slice that are longer than 3 characters.

### Requirements
- [ ] `Map` has two type parameters and returns a slice of the output type
- [ ] `Filter` returns a slice of the same element type as the input
- [ ] `Reduce` has two type parameters (element type and accumulator type)
- [ ] Demonstrate the composition: `Reduce(Map(Filter(words, ...), ...), ...)`

### Hints
<details>
<summary>Hint 1</summary>

For the composed example: start with `[]string`, filter to strings longer than 3 chars, map each string to its `len()`, then reduce (sum) the lengths. The types flow as `[]string → []string → []int → int`.

</details>

<details>
<summary>Hint 2</summary>

`Map` needs two type parameters because `f` converts `T` to `U` — input and output element types can differ. `Filter` only needs one because the element type doesn't change. `Reduce` needs two because the accumulator type `Acc` can differ from the element type `T`.

</details>

### Expected Output / Acceptance Criteria
```
words longer than 3 chars: [apple banana cherry date]
lengths: [5 6 6 4]
total length: 21
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Map applies f to each element of s, collecting results.
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

// Filter returns elements for which keep returns true.
func Filter[T any](s []T, keep func(T) bool) []T {
    var result []T
    for _, v := range s {
        if keep(v) {
            result = append(result, v)
        }
    }
    return result
}

// Reduce combines elements into a single accumulator value.
func Reduce[T, Acc any](s []T, init Acc, f func(Acc, T) Acc) Acc {
    acc := init
    for _, v := range s {
        acc = f(acc, v)
    }
    return acc
}

func main() {
    words := []string{"hi", "apple", "banana", "ok", "cherry", "date"}

    // Step 1: filter to words longer than 3 characters
    long := Filter(words, func(s string) bool { return len(s) > 3 })
    fmt.Println("words longer than 3 chars:", long)

    // Step 2: map to lengths ([]string → []int)
    lengths := Map(long, func(s string) int { return len(s) })
    fmt.Println("lengths:", lengths)

    // Step 3: sum the lengths ([]int → int)
    total := Reduce(lengths, 0, func(acc, n int) int { return acc + n })
    fmt.Println("total length:", total)
}
```

**Explanation:**
`Map` uses two type parameters `[T, U any]` because `f` transforms `T` to `U` — the output type can be completely different from the input type. `Reduce` uses `[T, Acc any]` for the same reason: the accumulator might be a completely different type from the elements (e.g., building a string from ints). The type flow in the composed pipeline is `[]string → []string → []int → int`, with the compiler inferring all three instantiations automatically.

</details>

---

## Exercise 5: Generic Stack [🔴 Hard] [3 pts]

### Context
A stack is the canonical example of a generic container. It demonstrates that a generic type (not just a generic function) written once can be used for any element type with full type safety. This exercise also covers the zero-value pattern — how to return a "nothing" value when the type `T` is unknown.

### Task
Implement a complete `Stack[T any]` type with:
- `Push(v T)` — add to top
- `Pop() (T, bool)` — remove and return top; return zero value and false if empty
- `Peek() (T, bool)` — view top without removing; return zero value and false if empty
- `Len() int` — number of elements
- `IsEmpty() bool` — true if no elements

Demonstrate it with both `Stack[int]` and `Stack[string]`, including calling `Pop` on an empty stack to show the zero-value behavior.

### Requirements
- [ ] The type is defined as `type Stack[T any] struct { ... }` with a `[]T` backing slice
- [ ] `Pop` and `Peek` use `var zero T` to get the zero value when empty
- [ ] Both `Stack[int]` and `Stack[string]` are used in the demo
- [ ] Popping from an empty stack returns the zero value and `false` (no panic)

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
type Stack[T any] struct {
    items []T
}
```

Methods on the type use `*Stack[T]` as the receiver (pointer receiver for mutation).

</details>

<details>
<summary>Hint 2 (zero-value pattern)</summary>

To return a zero value of type T:
```go
var zero T
return zero, false
```

You cannot write `return nil, false` or `return 0, false` because T might be any type.

</details>

<details>
<summary>Hint 3 (Pop implementation)</summary>

```go
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
```

</details>

### Expected Output / Acceptance Criteria
```
[int stack] pushed 1, 2, 3. len=3
[int stack] pop: 3
[int stack] pop: 2
[int stack] pop: 1
[int stack] pop from empty: 0, false
[string stack] pushed hello, world. len=2
[string stack] peek: world
[string stack] pop: world
[string stack] pop: hello
[string stack] IsEmpty: true
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Stack[T] is a generic LIFO container backed by a slice.
type Stack[T any] struct {
    items []T
}

// Push adds v to the top of the stack.
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
    last := len(s.items) - 1
    v := s.items[last]
    s.items = s.items[:last]
    return v, true
}

// Peek returns the top item without removing it.
// Returns the zero value and false if the stack is empty.
func (s *Stack[T]) Peek() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    return s.items[len(s.items)-1], true
}

// Len returns the number of items in the stack.
func (s *Stack[T]) Len() int { return len(s.items) }

// IsEmpty reports whether the stack has no items.
func (s *Stack[T]) IsEmpty() bool { return len(s.items) == 0 }

func main() {
    // Integer stack demonstration
    var ints Stack[int]
    ints.Push(1)
    ints.Push(2)
    ints.Push(3)
    fmt.Printf("[int stack] pushed 1, 2, 3. len=%d\n", ints.Len())
    for !ints.IsEmpty() {
        v, ok := ints.Pop()
        fmt.Printf("[int stack] pop: %d\n", v)
        _ = ok
    }
    // Pop from empty — shows zero value behavior
    v, ok := ints.Pop()
    fmt.Printf("[int stack] pop from empty: %d, %v\n", v, ok)

    // String stack demonstration
    var strs Stack[string]
    strs.Push("hello")
    strs.Push("world")
    fmt.Printf("[string stack] pushed hello, world. len=%d\n", strs.Len())
    if top, ok := strs.Peek(); ok {
        fmt.Println("[string stack] peek:", top)
    }
    for !strs.IsEmpty() {
        w, _ := strs.Pop()
        fmt.Println("[string stack] pop:", w)
    }
    fmt.Println("[string stack] IsEmpty:", strs.IsEmpty())
}
```

**Explanation:**
The zero-value pattern `var zero T` is the essential technique here. For `Stack[int]`, the zero value of `T=int` is `0`; for `Stack[string]` it is `""`. The same `Pop` function handles both correctly without any type-specific logic. The backing `[]T` slice stores typed elements — you cannot push a `string` onto a `Stack[int]` because the compiler enforces the type at each `Push` call.

</details>

---

## Exercise 6: Generic Set with Intersection [🔴 Hard] [3 pts]

### Context
A `Set[T]` is a collection with no duplicates. It requires `comparable` (for map keys), not just `any`. This exercise also introduces a package-level generic function for set intersection, demonstrating the workaround for the "methods cannot have new type parameters" restriction.

### Task
Implement `Set[T comparable]` with:
- `NewSet[T comparable]() *Set[T]`
- `Add(v T)`
- `Contains(v T) bool`
- `Remove(v T)`
- `Len() int`
- `Elements() []T` — returns a slice of all elements (any order)

Also implement a package-level function `Intersect[T comparable](a, b *Set[T]) *Set[T]` that returns a new set containing only elements present in both `a` and `b`.

Demonstrate with two `Set[string]` instances.

### Requirements
- [ ] `Set` uses a `map[T]struct{}` internally
- [ ] `Intersect` is a package-level function (not a method), taking two `*Set[T]` arguments
- [ ] Demo shows Add, Contains, Remove, and Intersect all working correctly

### Hints
<details>
<summary>Hint 1 (set backing structure)</summary>

```go
type Set[T comparable] struct {
    m map[T]struct{}
}
```

The empty struct `struct{}` is the conventional "no value" value for map-as-set patterns.

</details>

<details>
<summary>Hint 2 (Intersect logic)</summary>

Iterate over the elements of one set, and for each element, check if it is also in the other set. If yes, add it to the result set.

</details>

### Expected Output / Acceptance Criteria
```
set A: {go python rust}
set B: {rust java go}
A contains "go": true
A contains "java": false
intersection: {go rust}
after removing "go" from A, A contains "go": false
```

(Order of elements within each set may vary.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "slices"
    "sort"
)

// Set[T] is an unordered collection with no duplicate elements.
type Set[T comparable] struct {
    m map[T]struct{}
}

// NewSet returns an empty Set[T].
func NewSet[T comparable]() *Set[T] {
    return &Set[T]{m: make(map[T]struct{})}
}

// Add inserts v into the set (no-op if already present).
func (s *Set[T]) Add(v T) { s.m[v] = struct{}{} }

// Contains reports whether v is in the set.
func (s *Set[T]) Contains(v T) bool {
    _, ok := s.m[v]
    return ok
}

// Remove deletes v from the set (no-op if not present).
func (s *Set[T]) Remove(v T) { delete(s.m, v) }

// Len returns the number of elements.
func (s *Set[T]) Len() int { return len(s.m) }

// Elements returns a slice of all elements in unspecified order.
func (s *Set[T]) Elements() []T {
    result := make([]T, 0, len(s.m))
    for v := range s.m {
        result = append(result, v)
    }
    return result
}

// Intersect returns a new set containing elements present in both a and b.
// This is a package-level function (not a method) because methods cannot
// introduce new type parameters, and T is already the type from both sets.
func Intersect[T comparable](a, b *Set[T]) *Set[T] {
    result := NewSet[T]()
    for v := range a.m {
        if b.Contains(v) {
            result.Add(v)
        }
    }
    return result
}

func main() {
    a := NewSet[string]()
    for _, w := range []string{"go", "python", "rust"} {
        a.Add(w)
    }
    b := NewSet[string]()
    for _, w := range []string{"rust", "java", "go"} {
        b.Add(w)
    }

    // Sort for deterministic output
    ae := a.Elements()
    sort.Strings(ae)
    fmt.Println("set A:", ae)

    be := b.Elements()
    sort.Strings(be)
    fmt.Println("set B:", be)

    fmt.Println("A contains \"go\":", a.Contains("go"))
    fmt.Println("A contains \"java\":", a.Contains("java"))

    inter := Intersect(a, b)
    ie := inter.Elements()
    slices.Sort(ie)
    fmt.Println("intersection:", ie)

    a.Remove("go")
    fmt.Println("after removing \"go\" from A, A contains \"go\":", a.Contains("go"))
}
```

**Explanation:**
The `Set` uses `map[T]struct{}` — the empty struct as the value type is the idiomatic Go pattern for a set (no value needed, just presence/absence). `comparable` is required because map keys must be comparable. `Intersect` is a package-level function rather than a method because, at the time it was designed, you might want to convert between different set types — but even when T is the same, the method restriction means package-level is the only option for operations that conceptually belong to the type.

</details>

---

## Exercise 7: Generic Ordered Map using slices.SortFunc [🔴 Hard] [3 pts]

### Context
The `slices` and `cmp` standard packages are the practical everyday face of generics in Go 1.21+. This exercise builds fluency with `slices.SortFunc`, `cmp.Compare`, and `slices.BinarySearchFunc` — patterns you will use in production code.

### Task
Given a `[]Product` (with `Name string`, `Price float64`, and `Stock int` fields), use the `slices` and `cmp` packages to:
1. Sort by `Price` ascending
2. Re-sort by `Stock` descending, breaking ties by `Name` alphabetically
3. Use `slices.BinarySearchFunc` to find a product by name in a name-sorted slice
4. Filter (using `slices.DeleteFunc` on a clone) to keep only products with `Stock > 0`

### Requirements
- [ ] All sort operations use `slices.SortFunc` with a comparator that uses `cmp.Compare`
- [ ] Multi-key sort (Stock desc, then Name asc) is handled inside a single comparator
- [ ] Binary search uses `slices.BinarySearchFunc` after sorting by name
- [ ] The filter uses `slices.DeleteFunc` on a `slices.Clone` (to avoid mutating the original)

### Hints
<details>
<summary>Hint 1 (multi-key sort pattern)</summary>

```go
slices.SortFunc(products, func(a, b Product) int {
    if c := cmp.Compare(b.Stock, a.Stock); c != 0 { // reversed for descending
        return c
    }
    return cmp.Compare(a.Name, b.Name) // ascending tiebreak
})
```

Reversing the arguments to `cmp.Compare` (`b.Stock, a.Stock` instead of `a.Stock, b.Stock`) gives descending order.

</details>

### Expected Output / Acceptance Criteria
Output will show the products sorted two different ways, a binary search result, and the in-stock filtered list. Exact formatting is flexible; correctness of ordering matters.

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "cmp"
    "fmt"
    "slices"
)

type Product struct {
    Name  string
    Price float64
    Stock int
}

func printProducts(label string, ps []Product) {
    fmt.Printf("%s:\n", label)
    for _, p := range ps {
        fmt.Printf("  %-12s $%6.2f  stock=%d\n", p.Name, p.Price, p.Stock)
    }
}

func main() {
    products := []Product{
        {"Widget", 9.99, 50},
        {"Gadget", 24.99, 0},
        {"Doohickey", 4.49, 100},
        {"Thingamajig", 14.99, 50},
        {"Whatsit", 19.99, 0},
    }

    // 1. Sort by Price ascending
    slices.SortFunc(products, func(a, b Product) int {
        return cmp.Compare(a.Price, b.Price)
    })
    printProducts("By price ascending", products)

    // 2. Sort by Stock descending, then Name ascending
    slices.SortFunc(products, func(a, b Product) int {
        if c := cmp.Compare(b.Stock, a.Stock); c != 0 { // b,a = descending
            return c
        }
        return cmp.Compare(a.Name, b.Name)
    })
    printProducts("\nBy stock desc, name asc", products)

    // 3. Binary search by name (sort by name first)
    byName := slices.Clone(products)
    slices.SortFunc(byName, func(a, b Product) int {
        return cmp.Compare(a.Name, b.Name)
    })
    idx, found := slices.BinarySearchFunc(byName, "Widget", func(p Product, name string) int {
        return cmp.Compare(p.Name, name)
    })
    if found {
        fmt.Printf("\nFound %q at index %d: %+v\n", "Widget", idx, byName[idx])
    } else {
        fmt.Printf("\n%q not found (insertion point: %d)\n", "Widget", idx)
    }

    // 4. Filter to in-stock products only (clone to avoid mutating original)
    inStock := slices.DeleteFunc(slices.Clone(products), func(p Product) bool {
        return p.Stock <= 0
    })
    printProducts("\nIn-stock products", inStock)
}
```

**Explanation:**
`cmp.Compare(b.Stock, a.Stock)` (with arguments reversed) gives descending order because it returns +1 when b > a (meaning a comes after b, i.e., b is "less"). `slices.BinarySearchFunc` takes a custom comparator that compares a `Product` against a search key (the string `"Widget"`) — the key type can differ from the element type. `slices.DeleteFunc` on a clone is the idiomatic in-place filter that doesn't mutate the source.

</details>

---

## Exercise 8: When Generics Are Wrong — Refactor to Interface [⭐ Expert] [5 pts]

### Context
Knowing when *not* to use generics is as important as knowing how to use them. This open-ended exercise starts with an over-generic design and asks you to identify why it's wrong and produce the better design.

### Task
The following code uses generics unnecessarily. Identify the problem, explain why, and rewrite using a plain interface:

```go
// OVER-GENERIC: this function only calls .Write() on its argument.
// Generics add complexity with no benefit here.
func WriteMessage[W interface{ Write([]byte) (int, error) }](w W, msg string) error {
    _, err := w.Write([]byte(msg))
    return err
}

// ALSO OVER-GENERIC: this function only calls .Close() on its argument.
func CloseAll[C interface{ Close() error }](items []C) []error {
    var errs []error
    for _, item := range items {
        if err := item.Close(); err != nil {
            errs = append(errs, err)
        }
    }
    return errs
}
```

Then write a *correctly generic* function `Transform[T, U any](s []T, f func(T) U) []U` and explain why this one *does* benefit from generics.

### Requirements
- [ ] Identify and articulate exactly why `WriteMessage` and `CloseAll` don't need generics
- [ ] Rewrite both using plain interfaces (`io.Writer`, `io.Closer`)
- [ ] Implement `Transform` as a genuinely useful generic function
- [ ] Write a short explanation (3–5 sentences) of the decision criteria

### Hints
<details>
<summary>Hint 1 (the key question)</summary>

Ask: "Does the function need to know the concrete type of its argument? Does it preserve the concrete type in its return value? Does it use operators that interfaces can't express?"

If the answer to all three is "no" — and the function only calls methods — use a plain interface.

</details>

<details>
<summary>Hint 2 (why Transform is different)</summary>

`Transform` has input type `[]T` and output type `[]U`. The connection between the input and output types (`T → U` via `f`) is something only generics can express type-safely. An interface-based version would return `[]interface{}`, losing type information.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "io"
    "os"
    "strings"
)

// WRONG: over-generic. This function only calls Write — use io.Writer.
// func WriteMessage[W interface{ Write([]byte) (int, error) }](w W, msg string) error { ... }

// RIGHT: plain interface is simpler and equally expressive.
// io.Writer is already defined in the standard library — use it.
func WriteMessage(w io.Writer, msg string) error {
    _, err := w.Write([]byte(msg))
    return err
}

// WRONG: over-generic. This function only calls Close — use io.Closer.
// func CloseAll[C interface{ Close() error }](items []C) []error { ... }

// RIGHT: use io.Closer.
func CloseAll(items []io.Closer) []error {
    var errs []error
    for _, item := range items {
        if err := item.Close(); err != nil {
            errs = append(errs, err)
        }
    }
    return errs
}

// CORRECTLY GENERIC: the connection between input type T and output type U
// can only be expressed with generics. An interface-based version would
// return []interface{}, losing type safety.
func Transform[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

func main() {
    // WriteMessage works with any io.Writer — os.Stdout, strings.Builder, etc.
    _ = WriteMessage(os.Stdout, "Hello from WriteMessage\n")

    var sb strings.Builder
    _ = WriteMessage(&sb, "Hello from WriteMessage to Builder\n")
    fmt.Print(sb.String())

    // Transform is genuinely generic: int → string, type-safely
    nums := []int{1, 2, 3, 4, 5}
    strs := Transform(nums, func(n int) string { return fmt.Sprintf("item%d", n) })
    fmt.Println(strs)
}
```

**Why WriteMessage and CloseAll don't need generics:**
Both functions only call a single method on their argument (`Write` and `Close` respectively) and return nothing of the argument's type. An interface captures this perfectly — and the standard library already defines exactly these interfaces (`io.Writer`, `io.Closer`). Generics would add type parameter syntax without providing any additional safety or capability. The rule: if all you need is method dispatch, use an interface.

**Why Transform does need generics:**
`Transform` produces output of type `[]U` where `U` is related to `T` through the transformation function `f`. Without generics, you'd return `[]interface{}`, and callers would need to type-assert every element. Generics allow the return type to be exactly `[]string` when `f` produces strings, `[]int` when `f` produces ints, etc. — the type flows through the transformation, and the compiler verifies it.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Generic Min/Max | — | —/1 | — | — |
| Exercise 2 — Generic Contains and Index | — | —/1 | — | — |
| Exercise 3 — Custom Constraint with ~ | — | —/2 | — | — |
| Exercise 4 — Generic Map, Filter, Reduce | — | —/2 | — | — |
| Exercise 5 — Generic Stack | — | —/3 | — | — |
| Exercise 6 — Generic Set with Intersection | — | —/3 | — | — |
| Exercise 7 — Generic Ordered Map (slices/cmp) | — | —/3 | — | — |
| Exercise 8 — When Generics Are Wrong | — | —/5 | — | — |
| **Total** | | **—/20** | | |

**Passing threshold:** 13/20 (65%). Aim for 17/20 (85%) before taking the test.
