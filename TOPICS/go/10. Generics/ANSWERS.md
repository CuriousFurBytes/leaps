# Answer Key — Module 10: Generics

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

### 1.1 — Go version and year for generics [1 pt]

**Full credit answer:**
Generics were introduced in **Go 1.18**, released in **March 2022**. This was the culmination of a multi-year design process (the type parameters proposal was finalized in 2020–2021) and represents the single largest language addition since Go 1.0.

**Key points required:**
- Go 1.18 (or "1.18")
- 2022 (or "March 2022")

**Common wrong answers:**
- "Go 1.21" — that is when the `slices`, `maps`, and `cmp` packages were added; generics themselves shipped in 1.18
- "Go 2.0" — generics shipped in Go 1.18, not a hypothetical Go 2

---

### 1.2 — `any` vs `comparable` [1 pt]

**Full credit answer:**
`any` is an alias for `interface{}` — it means the type parameter can be *any* type, and inside the function body you can only perform operations available to all types: assignment, passing, returning, and comparing to `nil` (for pointer/interface types). You cannot use `==`, `<`, or any other operators.

`comparable` is a predeclared constraint meaning the type supports `==` and `!=`. Use it when you need to compare values for equality — as map keys, in search functions, or in set implementations. It excludes slices, maps, and functions (which are not comparable with `==`).

**Key points required:**
- `any` = any type, no type-specific operations
- `comparable` = supports `==` and `!=`
- `comparable` is required for map keys and equality comparisons

---

### 1.3 — The `~` tilde operator [1 pt]

**Full credit answer:**
The `~` operator in a constraint means "any type whose *underlying type* is T." Without `~`, the constraint matches only the exact predeclared type. With `~`, it also matches user-defined named types whose underlying type is T.

For example: `int` in a union matches only the predeclared `int`. `~int` matches `int` *and* any named type like `type MyInt int` or `type Priority int` — because those types have `int` as their underlying type.

This is critical for writing practical constraints: library code should almost always use `~T` in union elements so that user-defined domain types (e.g., `type Celsius float64`, `type UserID int64`) work with the constraint.

**Key points required:**
- `~T` = T and all named types with underlying type T
- Without `~`, named types are excluded
- Practical implication: use `~` in constraints to be inclusive

---

### 1.4 — Methods cannot introduce new type parameters [1 pt]

**Full credit answer:**
No. Methods on a generic type **cannot** introduce new type parameters. `func (s *Stack[T]) Map[U any](f func(T) U) []U` is a **compile error**: "method must have no type parameters."

The type parameter `T` on `Stack` can be used in methods (it appears in the receiver `*Stack[T]`), but methods cannot declare their own additional type parameters. The workaround is a package-level function: `func StackMap[T, U any](s *Stack[T], f func(T) U) []U`.

**Key points required:**
- Not valid — compile error
- Methods can use the type's existing type parameters
- Workaround: package-level function

**Common wrong answers:**
- "Yes, it's valid" — it is not; this is one of the most surprising restrictions in Go generics

---

### 1.5 — Three standard library packages from Go 1.21 [1 pt]

**Full credit answer:**
- **`slices`** — generic functions for slices: `Sort`, `SortFunc`, `Contains`, `Index`, `BinarySearch`, `Clone`, `DeleteFunc`, etc.
- **`maps`** — generic functions for maps: `Keys`, `Values`, `Clone`, `Copy`, `Delete`, etc.
- **`cmp`** — comparison utilities: `cmp.Compare` (returns -1/0/+1 for ordered comparison) and the `cmp.Ordered` constraint (covers all ordered types)

**Key points required:**
- All three names: `slices`, `maps`, `cmp`
- A reasonable description of each

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Pre-generics pain: interface{} vs copy-paste [2 pts]

**Full credit answer:**

**Problem with `interface{}`:** Writing `func Max(a, b interface{}) interface{}` accepts any type but loses type information. The caller receives an `interface{}` and must type-assert it back to the concrete type they expect. If the assertion is wrong, the program panics at runtime — the compiler cannot catch the mismatch. Additionally, boxing values in `interface{}` may cause heap allocations and adds runtime overhead.

**Problem with copy-paste:** Writing `MaxInt`, `MaxFloat64`, `MaxString` for each type is type-safe but duplicates code. A bug fix must be applied in every copy. New types require new functions. The standard library's `sort` package exemplifies this: it had `sort.Ints`, `sort.Float64s`, `sort.Strings` separately.

**How generics solves both:** A generic `func Max[T cmp.Ordered](a, b T) T` is:
- **Type-safe at compile time** — the compiler verifies at each call site that the argument type satisfies `cmp.Ordered`; no runtime assertions needed
- **Written once** — one function covers all ordered types, including user-defined types based on int, float, or string
- **No boxing** — the compiler generates efficient code for each GC shape; scalar types are not heap-allocated

**Rubric:**
- 2 pts: Correctly explains both pre-generics problems AND explains how generics solves both; mentions compile-time safety
- 1 pt: Correctly describes one problem, or describes both problems but is vague about how generics solves them
- 0 pts: Misunderstands what the pre-generics problem was

---

### 2.2 — Constraints are interfaces; generic vs interface parameter [2 pts]

**Full credit answer:**

"Constraints are interfaces" means the syntax for a generic constraint is exactly the same as the syntax for an interface — it *is* an interface. Before Go 1.18, interfaces described method sets ("this type must implement these methods"). From 1.18 onward, interfaces can also contain type elements (`~int | ~float64`), making them useful as constraints that restrict which concrete types can fill a type parameter.

**When a constraint (generic) is correct:**
Use a generic constraint when:
1. You need to use operators (`<`, `>`, `==`) that can't be expressed as methods
2. You need to preserve the concrete type in the return value
3. You are writing a container or algorithm that works uniformly for multiple types

Example: `func Min[T cmp.Ordered](a, b T) T` — you need `<` (not expressible as a method), and the return type must be `T` (the same type as the input).

**When a plain interface parameter is better:**
Use a plain interface when the function only calls methods on its argument and doesn't need the concrete type preserved.

Example: `func WriteAll(w io.Writer, data []byte) error` — the function only calls `w.Write()`; the concrete type is irrelevant. Making it generic (`[W io.Writer]`) adds syntax with no benefit.

**Rubric:**
- 2 pts: Correctly explains that constraints are interfaces extended with type elements; gives a concrete example of each (generic appropriate vs interface appropriate) with correct reasoning
- 1 pt: Understands that constraints are interfaces but cannot clearly articulate when to choose one vs the other
- 0 pts: Thinks constraints and interfaces are fundamentally different mechanisms

---

### 2.3 — GC shape stenciling vs monomorphization [2 pts]

**Full credit answer:**

**C++ full monomorphization:** C++ templates generate a completely separate copy of the compiled function for every distinct type argument. `vector<int>` and `vector<string>` are completely separate classes in the compiled binary. This produces the fastest possible code (each copy can be optimized for its exact type) but increases binary size.

**Go GC shape stenciling:** Go groups type arguments by their *GC shape* — their memory layout as seen by the garbage collector. All pointer types share one GC shape; `int` and `int32` are different shapes (different sizes). For each unique GC shape, one copy of the machine code is generated. A *dictionary* is passed at call time carrying type-specific information (size, comparison function, method table).

**Practical implications:**
1. Generic code over diverse pointer types (e.g., `*User`, `*Product`, `*Order`) shares one stencil — binary size stays compact
2. There is a small overhead compared to monomorphization (dictionary lookup vs direct code) — typically negligible for most code
3. For tight numeric inner loops, explicitly typed concrete code can outperform generic code — benchmark before optimizing
4. The implementation is an internal detail; correctness is guaranteed; performance may improve in future Go versions

**Rubric:**
- 2 pts: Correctly describes the stenciling/dictionary approach, contrasts it with C++ monomorphization, and gives at least one practical implication
- 1 pt: Knows the approach exists and is different from C++, but cannot describe the dictionary mechanism or practical implications accurately
- 0 pts: Thinks Go generics work exactly like C++ templates (full monomorphization) or has no understanding of the distinction

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Generic Keys and Values functions [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

// Keys returns a slice of all keys in m.
func Keys[K comparable, V any](m map[K]V) []K {
    keys := make([]K, 0, len(m))
    for k := range m {
        keys = append(keys, k)
    }
    return keys
}

// Values returns a slice of all values in m.
func Values[K comparable, V any](m map[K]V) []V {
    vals := make([]V, 0, len(m))
    for _, v := range m {
        vals = append(vals, v)
    }
    return vals
}

func main() {
    scores := map[string]int{"Alice": 90, "Bob": 85, "Carol": 92}
    fmt.Println("Keys:", Keys(scores))   // order non-deterministic
    fmt.Println("Values:", Values(scores)) // order non-deterministic
}
```

**Key points required:**
- `K comparable` (map keys must be comparable)
- `V any` (values can be any type)
- Correct iteration: `for k := range m` for keys, `for _, v := range m` for values
- Pre-allocated with `make([]K, 0, len(m))` is good practice (acceptable without)

**Rubric:**
- 3 pts: Both functions correct; proper constraints; compiles and runs; note about map order non-determinism
- 2 pts: Both functions mostly correct; minor error (e.g., wrong constraint, missing `comparable` for K)
- 1 pt: One function correct; the other has a significant error
- 0 pts: Fundamental misunderstanding of generic function syntax or map iteration

**Acceptable alternatives:**
- `maps.Keys(m)` and `maps.Values(m)` from the standard library are correct alternatives; if the student uses these, they still need to demonstrate understanding of why they need `comparable`

---

### 3.2 — Generic Stack + expression evaluator [3 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "strconv"
)

type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(v T) {
    s.items = append(s.items, v)
}

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

func (s *Stack[T]) Len() int { return len(s.items) }

func main() {
    tokens := []string{"3", "4", "+", "2", "+"}
    // evaluates: 3 + 4 + 2 = 9
    var stack Stack[int]

    for _, tok := range tokens {
        switch tok {
        case "+":
            b, _ := stack.Pop()
            a, _ := stack.Pop()
            stack.Push(a + b)
        default:
            n, err := strconv.Atoi(tok)
            if err == nil {
                stack.Push(n)
            }
        }
    }

    result, _ := stack.Pop()
    fmt.Println("Result:", result) // Output: Result: 9
}
```

**Rubric:**
- 3 pts: Correct generic Stack implementation with `Push`, `Pop` (returning T, bool), and `Len`; correct evaluator that pops two values for `+` and pushes the result; correct output
- 2 pts: Stack implementation mostly correct; evaluator has a minor logical error (e.g., wrong order for a - b)
- 1 pt: Stack is correct but the evaluator is missing or substantially wrong; or the Stack has a significant error (e.g., no zero-value pattern in Pop)
- 0 pts: Does not use generics, or the Stack does not compile

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Bug analysis: FindMin [3 pts] (1 pt per identified error with fix)

**There are three errors in the function:**

**Error 1: `return nil` for type parameter T [1 pt]**
`return nil` is not valid when the return type is `T any`. `nil` is only valid for pointer, slice, map, function, channel, and interface types. For a generic type parameter `T`, the zero value must be obtained with `var zero T; return zero`. 

Fix:
```go
if len(s) == 0 {
    var zero T
    return zero
}
```

**Error 2: `v < min` requires `cmp.Ordered`, not `any` [1 pt]**
The `<` operator is not permitted when the constraint is `any`. `any` means no type-specific operations. To use `<`, the constraint must be `cmp.Ordered` (or any other constraint that permits `<`).

Fix: Change the function signature to `func FindMin[T cmp.Ordered](s []T) T`.

**Error 3: `v < min` should be `cmp.Compare(v, min) < 0` or just `v < min` (once constraint is fixed) [partial — this becomes correct after fixing Error 2]**
Once the constraint is changed to `cmp.Ordered`, `v < min` is valid. No separate fix needed.

**Corrected function:**
```go
func FindMin[T cmp.Ordered](s []T) T {
    if len(s) == 0 {
        var zero T
        return zero
    }
    min := s[0]
    for _, v := range s[1:] {
        if v < min {
            min = v
        }
    }
    return min
}
```

**Rubric:**
- 1 pt: Identifies `return nil` is invalid for `T any`; provides `var zero T; return zero` fix
- 1 pt: Identifies that `any` doesn't permit `<`; changes constraint to `cmp.Ordered`
- 1 pt: Provides the complete corrected function that compiles correctly

**Teaching note:**
These two errors commonly appear together because beginners write `any` by default (it's the most general), then hit both the `<` operator error and the nil-return error at once.

---

## Section 5: Discussion — Answer Key

### 5.1 — When to use generics (three scenarios) [2 pts]

**The three scenarios from the Go blog:**

1. **Functions on slices, maps, or channels of any element type** — when the function's logic operates on the container structure (range, append, len, map key/value access) rather than on the element values directly. Examples: `Keys`, `Values`, `Map`, `Filter`, `Reduce`, `Contains`, `Index`.

2. **General-purpose data structures** — containers where the storage and retrieval logic is independent of what is stored. Examples: `Stack[T]`, `Set[T]`, `Queue[T]`, `OrderedMap[K, V]`, `LRU[K, V]`. The data structure logic doesn't care whether it's storing `int` or `*User`.

3. **Functions that work across numeric/ordered types** — algorithms that rely on operators (`<`, `+`, etc.) rather than methods, and the algorithm is identical for all types. Examples: `Min`, `Max`, `Sum`, `Abs`, sort comparators using `cmp.Compare`.

**Example where generics are right (student's own example):**
Anything that maps cleanly to one of the three scenarios above. A well-reasoned example and clear explanation earn full credit.

**Example where a plain interface is better:**
Any function that only calls methods on its argument and doesn't need the concrete type in the return. Classic example: `func Log(w io.Writer, msg string)` — `io.Writer` is the right tool; `[W io.Writer]` adds syntax with no benefit.

**Rubric:**
- 2 pts: Correctly summarizes all three scenarios (in their own words, not exact quotes); gives a concrete, clearly-explained example of each choice (generic vs interface); reasoning is sound
- 1 pt: Gets two of the three scenarios; or correctly identifies one example but the reasoning for the other is weak or incorrect
- 0 pts: Cannot articulate when generics are appropriate vs when interfaces are better

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Generic OrderedMap [+5 pts]

**Full credit answer:**
```go
package main

import (
    "cmp"
    "fmt"
    "sort"
)

// OrderedMap[K, V] stores key-value pairs in sorted key order.
type OrderedMap[K cmp.Ordered, V any] struct {
    keys   []K
    values []V
}

// Set inserts or updates the value for key, maintaining sorted order.
func (m *OrderedMap[K, V]) Set(key K, value V) {
    // Binary search for the insertion point
    idx := sort.Search(len(m.keys), func(i int) bool {
        return cmp.Compare(m.keys[i], key) >= 0
    })
    if idx < len(m.keys) && m.keys[idx] == key {
        // Key already exists: update value
        m.values[idx] = value
        return
    }
    // Insert at idx to maintain sorted order
    m.keys = append(m.keys, key)
    copy(m.keys[idx+1:], m.keys[idx:])
    m.keys[idx] = key

    m.values = append(m.values, value)
    copy(m.values[idx+1:], m.values[idx:])
    m.values[idx] = value
}

// Get returns the value for key and whether it was found.
func (m *OrderedMap[K, V]) Get(key K) (V, bool) {
    idx := sort.Search(len(m.keys), func(i int) bool {
        return cmp.Compare(m.keys[i], key) >= 0
    })
    if idx < len(m.keys) && m.keys[idx] == key {
        return m.values[idx], true
    }
    var zero V
    return zero, false
}

// Keys returns all keys in sorted order.
func (m *OrderedMap[K, V]) Keys() []K {
    result := make([]K, len(m.keys))
    copy(result, m.keys)
    return result
}

// Values returns all values in key-sorted order.
func (m *OrderedMap[K, V]) Values() []V {
    result := make([]V, len(m.values))
    copy(result, m.values)
    return result
}

func main() {
    var om OrderedMap[string, int]
    om.Set("banana", 2)
    om.Set("apple", 1)
    om.Set("cherry", 3)
    om.Set("date", 4)
    om.Set("apricot", 0)

    fmt.Println("Keys:", om.Keys())
    // [apple apricot banana cherry date]

    fmt.Println("Values:", om.Values())
    // [1 0 2 3 4]

    v, ok := om.Get("cherry")
    fmt.Printf("Get cherry: %d, %v\n", v, ok)

    om.Set("banana", 99) // update
    v2, _ := om.Get("banana")
    fmt.Printf("After update, banana: %d\n", v2)
}
```

**Rubric:**
- 5 pts: Correct generic type `[K cmp.Ordered, V any]`; `Set` maintains sorted order using binary search; `Get` uses binary search; `Keys` and `Values` return slices in sorted order; demo shows keys inserted out of order appear sorted; compiles and runs
- 3 pts: Correct type parameters and interface; sorted order maintained but binary search not used (e.g., linear scan + sort.Slice) — correct but less efficient; all operations work correctly
- 2 pts: Type parameters correct; data structure stores keys and values; but ordering is not maintained (e.g., just appends); `Keys()` sorts at call time rather than maintaining order
- 1 pt: Recognizes the need for `cmp.Ordered` but implementation has significant logical errors
- 0 pts: Does not use generics, or the type parameters are fundamentally wrong

---

## Common Wrong Answers Across the Test

1. **Using `any` where `comparable` is needed** — Students use `any` as the default constraint and are surprised when `==` fails inside the function. The fix is always `comparable` for equality and map keys.

2. **Confusing the Go 1.18 generics release with the Go 1.21 standard library additions** — Generics syntax (1.18) and the `slices`/`maps`/`cmp` packages (1.21) are separate. Students who score 1.1 wrong typically need to review the Historical Context section.

3. **Thinking `~` is optional for numeric constraints** — Students write `int | float64` without `~` and are confused when their `type Celsius float64` doesn't work. The rule: always use `~` in union elements for library-quality constraints.

4. **Thinking methods can have type parameters** — This surprises everyone from Java/C#/Rust backgrounds. The restriction is real; the workaround (package-level function) is idiomatic.

5. **Misidentifying when generics help vs interfaces** — Students who haven't internalized the "three scenarios" often try to make everything generic. The key test: "Do I need operators or do I need to preserve the concrete type?" If no, use an interface.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 likely read without testing. Send them back to the README's "When Not to Use Generics" section and the "Practical Examples — Example 5" which explicitly contrasts generic vs interface.
- Students who struggle with Section 3 need more exercise practice. EXERCISES.md Exercises 4 (Map/Filter/Reduce) and 5 (Stack) are the direct prerequisites for the test's Section 3.
- Question 4.1 (bug analysis) is a diagnostic: if a student identifies `return nil` as wrong but doesn't identify `any` as the constraint problem, they understand the zero-value pattern but not the constraint-operators relationship — review the Constraints section.
- The bonus question (OrderedMap) is genuinely hard — it requires combining generics, binary search, and in-place slice insertion. A score of 3/5 on the bonus is excellent; don't be concerned if most students score 0–2.
- A score below 60% generally indicates that interfaces aren't solid yet — the student needs to return to [[go/6. Methods and Interfaces]] before generics will click.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
