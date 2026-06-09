# Answer Key — Module 4: Composite Types

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

### 1.1 — The three slice header fields [1 pt]

**Full credit answer:**
A slice header contains three fields:
1. **ptr** (pointer) — a pointer to the first element of the slice within the underlying array; this is what gets shared when two slice variables alias the same backing data
2. **len** (length) — the number of elements currently accessible through the slice; `len(s)` returns this; attempts to access `s[i]` where `i >= len` panic with "index out of range"
3. **cap** (capacity) — the number of elements from the `ptr` position to the end of the underlying array; `cap(s)` returns this; `append` can add elements up to `cap` without reallocating

**Key points required:**
- All three fields named (ptr/pointer, len/length, cap/capacity)
- Correct description of what each field means — particularly that `cap` is "from ptr to end of backing array", not "total array size"

**Common wrong answers:**
- *"size and capacity"* — Missing the pointer; the pointer is what enables sharing
- *"cap is the total size of the underlying array"* — Incorrect; cap is from the slice's start position to the end, not the total array size. Two slices into different positions of the same array have different caps.

---

### 1.2 — Zero value of a map [1 pt]

**Full credit answer:**
The zero value of a map in Go is `nil`. A nil map behaves as follows:
- **Reading** from a nil map is **safe** — it returns the zero value of the value type (e.g., `0` for `map[string]int`, `""` for `map[string]string`), just as if the key were not present
- **Writing** to a nil map causes a **runtime panic** with the message "assignment to entry in nil map"

To use a map for writing, always initialize it with `make(map[K]V)` or a map literal `map[K]V{}`.

**Key points required:**
- Zero value is `nil`
- Reading is safe (returns zero value)
- Writing panics

**Common wrong answers:**
- *"Reading from a nil map panics"* — This is wrong; reads are safe. Only writes panic.
- *"The zero value is an empty map"* — Incorrect; `nil` and an empty initialized map are distinct values

---

### 1.3 — Array vs slice assignment semantics [1 pt]

**Full credit answer:**
- **Arrays:** Assignment copies all data. When you write `b := a` where `a` is `[5]int`, Go copies all 5 integers into a new array. `a` and `b` are completely independent — modifying one does not affect the other.
- **Slices:** Assignment copies only the three-word header (ptr, len, cap), not the underlying array data. When you write `b := a` where `a` is `[]int`, both `a` and `b` share the same backing array. Modifying elements through `b` modifies the same elements visible through `a`.

**Key points required:**
- Arrays: deep copy (all data copied)
- Slices: shallow copy (header copied, backing array shared)

---

### 1.4 — Comma-ok idiom [1 pt]

**Full credit answer:**
The comma-ok idiom is: `v, ok := m[key]`

When `key` is present in the map, `v` is the corresponding value and `ok` is `true`.
When `key` is absent, `v` is the zero value of the map's value type and `ok` is `false`.

You need the comma-ok idiom when you must distinguish between "key not present" and "key present with the zero value." For example, in a `map[string]int`, if `m["alice"]` returns `0`, you cannot tell whether Alice has a score of 0 or was never added. With `v, ok := m["alice"]; ok`, you can distinguish these cases.

A plain `v := m[key]` is sufficient when the zero value for "not present" is acceptable and you don't need to distinguish absence from presence.

**Key points required:**
- Syntax `v, ok := m[key]`
- When `ok=false`, `v` is zero value
- When plain read is insufficient: when you need to distinguish absence from zero

---

### 1.5 — empty struct{} [1 pt]

**Full credit answer:**
`struct{}` is the **empty struct type** — a struct with no fields. It occupies **zero bytes** of memory. Its most common uses are:

1. **Map sets** — `map[T]struct{}` uses `struct{}` as the value type to implement a set with no wasted memory per entry (a `bool` value would cost 1 byte per entry; `struct{}` costs 0)
2. **Channel signals** — `chan struct{}` is used for pure signaling (done, ready, cancel) where no data needs to be sent; closing the channel or sending `struct{}{}` conveys the signal without allocating

**Key points required:**
- Zero bytes
- At least one correct use case (set or signal channel)

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — append and reallocation [2 pts]

**Full credit answer:**
When `append` is called on a slice whose `len` equals its `cap` (the backing array is full), the runtime:

1. **Allocates a new, larger backing array** — typically roughly double the current capacity for small slices; the exact growth factor is an implementation detail that decreases toward 1.25x for large slices
2. **Copies all existing elements** from the old array to the new array — this is an O(n) operation
3. **Returns a new slice header** with `ptr` pointing to the new array, `len = old_len + number_of_new_elements`, and `cap = new_array_size`

The old backing array is still referenced by the original slice variable — it is not freed immediately (the GC frees it when no more references exist).

**Why you must assign the return value:** `append` may return either the original slice (if capacity was sufficient — the header is updated with a new `len`) or a completely different slice pointing to a new backing array (if reallocation occurred). In either case, `append` returns the correct updated slice header. If you don't assign the return value (e.g., `append(s, x)` without `s =`), the update is discarded — whether it was a new length or a new pointer. The function receiving the slice received a copy of the header; without the return value, the caller's variable is unchanged.

**Rubric:**
- 2 pts: Correctly describes all three reallocation steps AND explains both why `append` returns a value AND why you must assign it
- 1 pt: Correct general idea (reallocation happens, must assign return) but missing the step-by-step mechanics or the distinction between capacity-sufficient vs capacity-insufficient cases
- 0 pts: Claims `append` modifies the slice in place, or cannot explain the mechanics

**Teaching note:**
The most common gap is students who know "you must assign append" but cannot explain *why*. The answer requires understanding that a slice value is a header, and function calls receive copies of values. Direct students to re-read the "The Slice Header" section if they struggled here.

---

### 2.2 — Map iteration randomization [2 pts]

**Full credit answer:**
The Go team deliberately randomized map iteration order starting from early versions. The reason: if iteration were deterministic (e.g., insertion order, or hash order), programs would accidentally depend on that order — they would be written and tested with one iteration order and would subtly fail when the internal hash table implementation changed (for example, when the Go runtime was updated). By randomizing the start position on every `range`, the runtime makes it impossible to write code that accidentally relies on iteration order. Any such code will fail immediately during testing.

**How to iterate in sorted key order:**
1. Extract the keys into a `[]K` slice by ranging over the map: `for k := range m { keys = append(keys, k) }`
2. Sort the keys: `slices.Sort(keys)` (or `sort.Strings` for string keys)
3. Iterate over the sorted keys: `for _, k := range keys { process(m[k]) }`

**Rubric:**
- 2 pts: Correctly explains the anti-foot-gun motivation AND gives the correct three-step sorted iteration approach
- 1 pt: Correct reasoning about why (preventing accidental ordering dependencies) but incomplete or incorrect fix, OR correct fix but no explanation of why
- 0 pts: Says "map iteration is random for performance reasons" without mentioning the correctness/safety motivation

---

### 2.3 — String immutability and conversion cost [2 pts]

**Full credit answer:**
"Immutable" means the bytes of a Go string cannot be modified after the string is created. Specifically:
- You **can** reassign a string variable: `s = "new value"` — this changes what string `s` refers to
- You **cannot** modify bytes in-place: `s[0] = 'H'` is a compile error — indexing a string gives a read-only byte
- You **cannot** cast a string to `[]byte` and modify the bytes in a way that affects the original string — a conversion always copies

**Why `string → []byte` allocates:** A string is a pointer to read-only bytes. To give you a `[]byte` that you can modify, Go must copy all the bytes into a new, writable backing array. If it gave you a pointer into the original string's bytes, your modifications would break the immutability guarantee (or worse, corrupt shared strings).

**Why `string → []rune` allocates:** A string stores bytes (UTF-8 encoded). A `[]rune` stores Unicode code points (each 4 bytes). Decoding UTF-8 bytes into runes is a transformation, not just a reinterpretation; the resulting rune slice always has different content and size than the byte representation.

**Rubric:**
- 2 pts: Correctly explains that immutability means bytes cannot be modified in place (not that the variable can't be reassigned), AND explains that both conversions copy because they provide mutable access to what was immutable, AND explains why `[]rune` involves a transformation beyond just copying
- 1 pt: Correct on immutability definition but missing the allocation explanation, OR correct that allocations happen but wrong on why
- 0 pts: Confuses "immutable string variable" (reassignment) with "immutable string contents" (can't modify bytes)

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — invertMap [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

func invertMap(m map[string]int) map[int][]string {
    result := make(map[int][]string)
    for k, v := range m {
        result[v] = append(result[v], k) // append-to-nil handles missing keys
    }
    return result
}

func main() {
    // Test case 1: some values repeat
    m1 := map[string]int{"a": 1, "b": 2, "c": 1, "d": 2, "e": 3}
    fmt.Println(invertMap(m1))
    // e.g.: map[1:[a c] 2:[b d] 3:[e]]  (order within slices may vary)

    // Test case 2: all values unique
    m2 := map[string]int{"x": 10, "y": 20, "z": 30}
    fmt.Println(invertMap(m2))
    // map[10:[x] 20:[y] 30:[z]]
}
```

**Step-by-step reasoning:**
1. Iterate over the input map with `for k, v := range m`
2. Use `v` (the integer) as the new key in `result`
3. `append(result[v], k)` uses the append-to-nil pattern: if `v` is not yet in `result`, `result[v]` returns `nil`, and `append(nil, k)` creates a new slice
4. Assign back: `result[v] = append(result[v], k)`

**Rubric:**
- 3 pts: Correct implementation using the append-to-nil pattern; both test cases shown; compiles and produces correct output
- 2 pts: Correct logic but misses the append-to-nil pattern (e.g., checks if key exists before initializing — works but verbose)
- 1 pt: Correct outer structure but wrong key/value inversion, or missing one test case
- 0 pts: Does not produce a map of slices, or has fundamental logic error

**Acceptable alternatives:**
- Checking existence before appending with `if _, ok := result[v]; !ok { result[v] = []string{} }` — correct but verbose; the append-to-nil pattern is more idiomatic

---

### 3.2 — removeDuplicates [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

func removeDuplicates(s []int) []int {
    if len(s) == 0 {
        return []int{} // return empty non-nil slice for empty input
    }

    result := make([]int, 0, len(s))
    result = append(result, s[0]) // always include the first element

    for i := 1; i < len(s); i++ {
        if s[i] != s[i-1] { // only append if different from previous
            result = append(result, s[i])
        }
    }
    return result
}

func main() {
    fmt.Println(removeDuplicates([]int{1, 1, 2, 3, 3, 3, 2, 2})) // [1 2 3 2]
    fmt.Println(removeDuplicates([]int{}))                         // []
    fmt.Println(removeDuplicates([]int{5}))                        // [5]
    fmt.Println(removeDuplicates([]int{1, 2, 3}))                  // [1 2 3] — no duplicates
    fmt.Println(removeDuplicates([]int{7, 7, 7, 7}))               // [7]
}
```

**Rubric:**
- 3 pts: Correct O(n) implementation; handles empty slice (non-nil result); handles single element; handles no duplicates; handles all-same; all three required test cases shown
- 2 pts: Correct logic but returns nil for empty input (should return `[]int{}`), or missing one required test case
- 1 pt: Correct for non-empty inputs but crashes or panics on empty/single-element input
- 0 pts: Sorts the input (not allowed), or uses O(n²) approach with nested loops, or has fundamental logic errors

**Acceptable alternatives:**
- Using `s[:0]` as the result start instead of `make` — works but has the aliasing subtlety; still acceptable if the student understands it
- Handling the empty case with an explicit guard at the top vs letting the loop handle it naturally — both are valid

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — addAll function doesn't work [3 pts] (1 pt each part)

**(a) Why `result` in main remains unchanged:**
When `addAll(result, items)` is called, Go copies the slice header (ptr, len, cap) into the parameter `s`. The function has its own copy of the header. When `s = append(s, item)` is called inside the loop, either:
- (If enough capacity) `append` writes into the backing array and returns a new header with incremented `len`. The new header is assigned to the local `s`, but the caller's `result` variable still has the old header with the original `len`.
- (If not enough capacity) `append` allocates a new backing array and returns a header pointing to it. The local `s` is updated, but the caller's `result` still points to the original array.

Either way, the caller's `result` variable is never updated — it is a copy that was not returned or passed by pointer.

**(b) Two fixes:**

Fix 1 — Return the slice:
```go
func addAll(s []int, items []int) []int {
    for _, item := range items {
        s = append(s, item)
    }
    return s
}

func main() {
    result := []int{1, 2, 3}
    result = addAll(result, []int{4, 5, 6})
    fmt.Println(result) // [1 2 3 4 5 6]
}
```

Fix 2 — Pass a pointer to the slice:
```go
func addAll(s *[]int, items []int) {
    for _, item := range items {
        *s = append(*s, item)
    }
}

func main() {
    result := []int{1, 2, 3}
    addAll(&result, []int{4, 5, 6})
    fmt.Println(result) // [1 2 3 4 5 6]
}
```

**(c) More idiomatic fix:**
Fix 1 (return the slice) is more idiomatic Go. Functions that build or extend slices conventionally return the new slice — `append` itself follows this convention. The pointer-to-slice pattern (`*[]int`) is less common and signals to readers that the function modifies the slice structure itself; it is appropriate when you have a design where multiple functions must share a single "accumulator" slice. For simple cases like this, returning the slice is cleaner, composable, and consistent with how the standard library works.

**Rubric:**
- 1 pt for (a): Correctly explains that the slice header is copied and the caller's variable is never updated; must mention that the header is what gets copied, not the backing array
- 1 pt for (b): Shows both valid fixes with correct syntax
- 1 pt for (c): Correctly identifies return-value form as more idiomatic AND gives a valid reason why (consistency with append, composability, convention)

---

## Section 5: Discussion — Answer Key

### 5.1 — Value semantics vs reference semantics [2 pts]

**Example strong answer:**
Arrays and structs have value semantics: assigning or passing them copies all the data fields inline. `b := a` where `a` is `[100]int` copies 100 integers; no sharing occurs. Slices and maps have reference semantics: they contain an internal pointer, so assigning copies only the header (for slices: ptr/len/cap; for maps: a pointer to the hash table). Backing data is shared.

**Value semantics bugs:** Passing a large struct by value to a function that "modifies" it — the modifications apply only to the copy; the caller's original is unchanged. This is correctness-critical when the caller expects the function to mutate the struct.

**Reference semantics bugs:** Taking a sub-slice `sub := s[1:4]`, passing it to a function that appends to `sub`, and finding that `s[4]` has been silently overwritten. Both `sub` and `s` share the same backing array; the append wrote into the shared space.

**The slice header as a middle ground:** A slice is a value type (the header is copied on assignment) that contains a reference (the ptr field points to shared data). This means: (1) modifying elements through any alias is visible everywhere (reference semantics for mutation), (2) `append` that reallocates is invisible to other aliases (value semantics for the header), and (3) the header is small (3 words) so passing slices to functions is cheap. The design deliberately makes element mutation cheap and visible while making structural changes (growing) safe by requiring explicit return and assignment.

**Elements that earn full credit:**
- Concrete explanation of what "copies" means for arrays/structs vs slices/maps
- One concrete correctness bug for value semantics (e.g., "large struct passed by value; mutations lost")
- One concrete correctness bug for reference semantics (e.g., "sub-slice aliasing overwrites original")
- Some recognition of the slice header as an intentional design that navigates the tradeoff

**Rubric:**
- 2 pts: Covers both semantics correctly with concrete examples; addresses the slice header's deliberate design; considers both correctness and performance dimensions
- 1 pt: Correctly distinguishes value and reference semantics, gives at least one concrete example, but misses the slice header insight or addresses only one dimension (correctness or performance)
- 0 pts: Conflates value and reference semantics, or gives examples that are incorrect

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Generic Stack [+5 pts]

**Full credit answer:**
```go
package main

import "fmt"

// Stack is a generic LIFO data structure.
// The zero value (Stack[T]{}) is ready to use — no initialization required.
type Stack[T any] struct {
    items []T
}

// Push adds v to the top of the stack.
func (s *Stack[T]) Push(v T) {
    s.items = append(s.items, v)
}

// Pop removes and returns the top element.
// Returns (zero value, false) if the stack is empty.
func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    top := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return top, true
}

// Peek returns the top element without removing it.
// Returns (zero value, false) if the stack is empty.
func (s *Stack[T]) Peek() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    return s.items[len(s.items)-1], true
}

// Len returns the number of elements in the stack.
func (s *Stack[T]) Len() int {
    return len(s.items)
}

func main() {
    var s Stack[int] // zero value is ready to use

    s.Push(1)
    s.Push(2)
    s.Push(3)
    fmt.Println("Len:", s.Len()) // 3

    if v, ok := s.Peek(); ok {
        fmt.Println("Peek:", v) // 3
    }

    for {
        v, ok := s.Pop()
        if !ok {
            break
        }
        fmt.Println("Pop:", v)
    }
    // Output: Pop: 3, Pop: 2, Pop: 1

    // Empty stack — no panic
    _, ok := s.Pop()
    fmt.Println("Empty pop ok:", ok) // false

    v, ok := s.Peek()
    fmt.Println("Empty peek:", v, ok) // 0 false
}
```

**Step-by-step explanation:**
1. `type Stack[T any]` declares a generic type with type parameter `T`; `any` is the constraint (no restrictions)
2. The backing store `items []T` is a nil slice in the zero value — valid to `append` to without initialization
3. `Pop` shrinks the slice with `s.items = s.items[:len(s.items)-1]` — this sets `len` to n-1 but does not zero the last element; this is a minor memory leak for pointer types (the stack still holds a reference in the backing array's position n). For a production implementation, you would zero the element: `s.items[len(s.items)] = zero` before shrinking.
4. `var zero T` is how you get the zero value of a type parameter — you cannot write `nil` or `0` because `T` could be any type.

**Rubric:**
- 5 pts: Correct generic syntax; zero value usable without init; `Pop`/`Peek` return zero value and false on empty (no panic); all operations demonstrated in main; pointer receivers used correctly
- 3 pts: Correct generic syntax and logic; minor issue (e.g., value receiver on `Push` so push doesn't work, or missing the empty-stack case)
- 1 pt: Correct general structure but significant issues (non-generic, or panics on empty stack)
- 0 pts: Does not use generics, or has fundamental logical errors

**Bonus teaching note:**
This question tests the intersection of generics (`[T any]`), slice mechanics (`append` and shrinking), and struct design (zero value usability). Students who score full credit here have a solid grasp of all three. The subtle point about zeroing popped elements is a production-quality concern — don't penalize for missing it, but do reward if mentioned.

---

## Common Wrong Answers Across the Test

These are patterns seen frequently when students haven't fully internalized the material:

1. **"Reading from a nil map panics"** — Only writes panic. Reads safely return the zero value. Students who make this mistake are conflating map behavior with pointer dereferencing. Direct them to re-read the "Maps" section's nil map discussion.
2. **Missing that `append` must be assigned back** — Students write `append(s, x)` without assignment, or write a function that appends to a parameter and expect the caller's slice to change. Direct them to re-read "append and Reallocation" and Example 4 in the README.
3. **Confusing struct embedding with inheritance** — Students write "embedding makes Rectangle a subclass of Dimensions." It does not; Go has no inheritance. Embedding is composition — `Rectangle` contains a `Dimensions` and its fields are promoted for convenience. The types remain distinct. Direct them to re-read the embedding section.
4. **"struct{} uses 1 byte"** — The empty struct uses 0 bytes. This is a specific Go optimization; even though most things require at least 1 byte to have a unique address, multiple instances of `struct{}` may share an address (the `zerobase` variable in the runtime). Direct them to re-read the "Empty Struct" section.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 (conceptual) typically have not run code examples. Recommend re-studying by writing and running the slice aliasing examples from the README, then explaining back what they observe.
- Students who struggle with Section 3 (applied) usually need more exercise practice. Send back to EXERCISES.md exercises 4, 6, and 7 specifically.
- The bonus question (generic stack) tests generics which are partially a preview of Module 10. Don't be concerned if students score 3/5 rather than 5/5 — the core correctness (empty-stack no-panic) is the important part.
- A score below 60% often indicates weak prerequisites — specifically, that the student is not comfortable with `for range` over maps and slices, or with function return values. Ask about Module 2 (Control Flow) and Module 3 (Functions) comfort levels.
- The most reliable indicator of mastery for this module: can the student explain without notes why `append` must always be assigned back? If yes, they have internalized the slice header model. If not, that is the single most important concept to review.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
