# Answer Key — Module 5: Pointers

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

### 1.1 — The `&` operator [1 pt]

**Full credit answer:**
`&` is the **address-of operator**: it takes a variable and returns a pointer to it — a `*T` holding the variable's memory address. Example: `x := 42; p := &x` — `p` is now a `*int` whose value is the address of `x`.

**Key points required:**
- `&` yields the address (a pointer) of a variable
- The type of the result is `*T` when applied to a variable of type `T`

**Common wrong answers:**
- *"& is the bitwise AND operator"* — that is also `&` in a different context (binary expression, e.g., `a & b`). In a unary prefix position before a variable (`&x`), it is address-of. Context disambiguates.
- *"& dereferences a pointer"* — no, that is `*`. `&` takes an address; `*` follows an address.

---

### 1.2 — Zero value of pointer types and nil dereference [1 pt]

**Full credit answer:**
The zero value of any pointer type in Go is `nil`. A nil pointer holds no address. Dereferencing a nil pointer (`*p` when `p` is nil) causes a **runtime panic** with the message "runtime error: invalid memory address or nil pointer dereference." This is not a compile-time error — the program builds successfully but crashes at the point of the dereference if the pointer is nil.

**Key points required:**
- Zero value is `nil`
- Dereferencing nil causes a runtime panic (not a compile error)

---

### 1.3 — `new(T)` vs `&T{}` [1 pt]

**Full credit answer:**
Both allocate memory and return a pointer, but they differ in usage:
- `new(T)` allocates a zero-value `T` and returns `*T`. It cannot initialize fields — you must set them afterward.
- `&T{}` creates a composite literal of type `T` and takes its address. It can initialize fields in the same expression: `&Point{X: 1.0, Y: 2.0}`.

Prefer `&T{}` for structs because it combines allocation and initialization in one expression and makes the type and initial values visible. Use `new(T)` for primitive types (like `new(int)`) when there is no composite literal form, or in older code.

**Key points required:**
- `new` zeroes and returns a pointer; `&T{}` allows field initialization
- `&T{}` is preferred for structs in modern Go code

---

### 1.4 — Field access through a struct pointer [1 pt]

**Full credit answer:**
Go provides **automatic field dereference** for struct pointers. If `p` is `*Point` and `Point` has field `X float64`, you can write `p.X` to read and `p.X = 5.0` to write. You do not need to write `(*p).X`, though that form is also valid. `p.X` is idiomatic Go.

**Key points required:**
- `p.X` is equivalent to `(*p).X` for struct pointer access
- Both forms compile; `p.X` is idiomatic

---

### 1.5 — Why pointer argument allows mutation despite call-by-value [1 pt]

**Full credit answer:**
When a function receives `*MyStruct`, it receives a copy of the pointer — but the copy holds the same address as the original. The function writes through the pointer to the memory at that address, which is the caller's struct. The pointer itself is copied, but it still points to the same original value.

**Key points required:**
- The pointer value (the address) is copied — but both the original and the copy point to the same memory
- Writing through the pointer (`p.Field = x`) modifies the memory at the shared address

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Call-by-value and memory for pointer vs value arguments [2 pts]

**Full credit answer:**
Go's call-by-value means every function argument is a copy. For a `Person` value argument, Go copies all fields of the struct into a new `Person` on the stack of the called function. Modifications to that copy are discarded when the function returns — the caller's `Person` is untouched.

For a `*Person` pointer argument, Go copies the pointer value (the address — typically 8 bytes on a 64-bit machine). The copy of the pointer still holds the same address as the original. When the function writes `p.Name = "Alice"` (which is `(*p).Name = "Alice"`), it follows the address in the pointer and modifies the struct at that address — the same struct the caller owns. The mutation is visible to the caller because both the caller's pointer and the function's copy point to the same memory.

```
Value argument (Person copy):          Pointer argument (*Person):

Caller frame:  [person: {Name:"Bob"}]  Caller frame:  [person: {Name:"Bob"}]
                      ↓ copy all fields              ↓ copy address only
Callee frame:  [p: {Name:"Bob"}]       Callee frame:  [p: 0xc000014098] ─→ {Name:"Bob"}
               p.Name = "Alice"                       p.Name = "Alice" writes here ↑
               discarded on return                    caller sees the change
```

**Rubric:**
- 2 pts: Correctly explains what is copied in each case AND why the pointer version allows mutation
- 1 pt: Correct general idea but the explanation of what specifically gets copied is missing or imprecise
- 0 pts: Confuses what is copied, or claims Go uses pass-by-reference

---

### 2.2 — Maps do not need `*map[K]V` for mutation [2 pts]

**Full credit answer:**
The colleague is partially right (that mutations need to be shared) but wrong about the solution. A `map[K]V` value in Go is already a pointer to an underlying hash table data structure. When you pass a `map[string]int` to a function, you pass a copy of this pointer — but both the caller and the function have pointers to the same hash table. Mutations like `m["key"] = value` modify the shared hash table and are visible to the caller.

`*map[K]V` is only needed in the rare case where the function must replace the map itself — assign `m = make(map[string]int)` — and have the caller see the new map. Wrapping a map in `*map[K]V` for ordinary mutations is unnecessary indirection that makes the code less readable.

**Rubric:**
- 2 pts: Correctly identifies that a map value is already a pointer/reference AND explains when `*map[K]V` is and is not appropriate
- 1 pt: Says `*map[K]V` is unnecessary but does not explain why (what a map value is)
- 0 pts: Agrees with the colleague that `*map[K]V` is needed for mutations

---

### 2.3 — Escape analysis and returning address of local variable [2 pts]

**Full credit answer:**
Escape analysis is the compiler's static analysis that determines where to allocate a variable: on the stack (cheaper, lives only for the duration of the function call) or on the heap (more expensive, can survive after the function returns). If the compiler can prove a variable's address never outlives the function (no pointer to it is stored or returned), the variable is stack-allocated. If the address might escape — for example, if it is returned or stored in a long-lived data structure — the variable escapes to the heap.

In Go, `return &x` is safe because the compiler detects that `x`'s address is returned and therefore automatically allocates `x` on the heap instead of the stack. When the function returns, the caller holds a valid pointer to heap-allocated memory that will remain valid until the garbage collector frees it (once no more references exist).

In C, the equivalent `return &x` is undefined behavior because C allocates locals on the stack by default; when the function returns, the stack frame is gone and the pointer is dangling. C has no garbage collector and no escape analysis, so the programmer is responsible for managing lifetime manually.

The runtime cost of escaping to the heap vs staying on the stack: heap allocation requires the garbage collector to eventually reclaim the memory; stack allocation is "free" — the stack pointer moves once.

**Rubric:**
- 2 pts: Correctly explains what escape analysis does AND why returning `&x` is safe in Go (compiler allocates on heap) AND contrasts with C's dangling pointer problem
- 1 pt: Explains that Go handles this safely but without explaining the mechanism (escape analysis / heap allocation)
- 0 pts: Claims returning `&x` is unsafe in Go, or cannot explain the difference from C

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — BankAccount with deposit and withdraw [3 pts]

**Full credit answer:**
```go
package main

import (
    "errors"
    "fmt"
)

type BankAccount struct {
    Owner   string
    Balance float64
}

func deposit(a *BankAccount, amount float64) {
    a.Balance += amount
}

func withdraw(a *BankAccount, amount float64) error {
    if a.Balance < amount {
        return fmt.Errorf("insufficient funds: have %.2f, need %.2f", a.Balance, amount)
    }
    a.Balance -= amount
    return nil
}

func main() {
    acc := BankAccount{Owner: "Alice", Balance: 0}

    deposit(&acc, 200.00)
    fmt.Printf("After deposit:   $%.2f\n", acc.Balance)  // 200.00

    if err := withdraw(&acc, 50.00); err != nil {
        fmt.Println("error:", err)
    } else {
        fmt.Printf("After withdraw:  $%.2f\n", acc.Balance)  // 150.00
    }

    if err := withdraw(&acc, 500.00); err != nil {
        fmt.Println("error:", err)  // insufficient funds
    }

    fmt.Printf("Final balance:   $%.2f\n", acc.Balance)  // 150.00
}
```

**Rubric:**
- 3 pts: Both `deposit` and `withdraw` take `*BankAccount`; `withdraw` returns an error; all three operations demonstrated; final balance is printed; compiles and runs correctly
- 2 pts: Correct pointer usage but minor error in error handling, or the insufficient funds case is not demonstrated
- 1 pt: One of the functions incorrectly takes `BankAccount` by value, or the mutation doesn't work; basic structure is present but doesn't meet the requirements
- 0 pts: Fundamental misunderstanding — functions take values and no mutation occurs, or code doesn't compile

**Acceptable alternatives:**
- Adding a nil guard in `deposit`/`withdraw` is fine and shows extra care
- Using `errors.New` vs `fmt.Errorf` is fine for the error creation
- Printing format variations are fine as long as the content is correct

---

### 3.2 — `findFirst` returning a pointer to a slice element [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

// findFirst returns a pointer to the first element satisfying pred,
// or nil if no element qualifies.
func findFirst(s []int, pred func(int) bool) *int {
    for i := range s {
        if pred(s[i]) {
            return &s[i]  // address of the slice element — safe
        }
    }
    return nil
}

func main() {
    nums := []int{4, 7, 2, 9, 1}
    isOdd := func(n int) bool { return n%2 != 0 }

    if p := findFirst(nums, isOdd); p != nil {
        fmt.Printf("First odd: %d\n", *p)  // 7
    } else {
        fmt.Println("No odd number found")
    }

    // Also demonstrate the nil case
    evens := []int{2, 4, 6}
    if p := findFirst(evens, isOdd); p != nil {
        fmt.Printf("First odd: %d\n", *p)
    } else {
        fmt.Println("No odd number found")  // prints this
    }
}
```

**Expected output:**
```
First odd: 7
No odd number found
```

**Rubric:**
- 3 pts: Correct function signature (`*int` return type); returns `&s[i]` for found element; returns `nil` if not found; `main` dereferences the pointer safely with a nil check; compiles and runs correctly
- 2 pts: Correct general approach but the nil check is missing in `main` (potential panic), or the return type is wrong
- 1 pt: Function returns an index or value rather than a pointer; or returns a copy of the value as a pointer (`val := s[i]; return &val` — technically works but is not what "return a pointer to the element" means)
- 0 pts: Does not attempt to return a pointer, or the function signature is fundamentally wrong

**Teaching note:**
`&s[i]` for a slice element is valid and points directly into the slice's backing array. Students who write `val := s[i]; return &val` are returning a pointer to a copy — it works but misses the intent of "pointer to the element." Full credit requires `&s[i]`.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Call-by-value bug in countWords [3 pts] (1 pt each part)

**(a) What actually happens:**
`total` is declared as 0 in `main`. When `countWords(words, total)` is called, Go copies the value 0 into the parameter `count` inside `countWords`. The loop runs and increments `count` to 3. But `count` is a local variable inside `countWords` — it is not `total`. When `countWords` returns, `count` is discarded. `total` in `main` was never touched; it remains 0. `fmt.Println("Total:", total)` prints 0.

**(b) Why it happens:**
This is **Go's call-by-value model**. All function arguments are copies of the caller's values. `count` inside `countWords` is a copy of `total`, not an alias for it. No matter how many times `count` is incremented, the original `total` in `main` is unaffected.

**(c) Two fixes:**

**Fix 1 — Pointer argument:**
```go
func countWords(words []string, count *int) {
    for _, w := range words {
        if len(w) > 0 {
            *count++  // increment through the pointer
        }
    }
}

func main() {
    words := []string{"hello", "world", "", "go"}
    total := 0
    countWords(words, &total)  // pass the address of total
    fmt.Println("Total:", total)  // 3
}
```

**Fix 2 — Return value:**
```go
func countWords(words []string) int {
    count := 0
    for _, w := range words {
        if len(w) > 0 {
            count++
        }
    }
    return count  // return the result to the caller
}

func main() {
    words := []string{"hello", "world", "", "go"}
    total := countWords(words)  // assign the return value
    fmt.Println("Total:", total)  // 3
}
```

**Rubric:**
- 1 pt for (a): Correctly traces that `total` remains 0 and explains that `count` is a separate local variable
- 1 pt for (b): Names "call-by-value" as the cause, with an explanation of what was copied
- 1 pt for (c): Provides at least one correct fix with the right syntax; bonus for providing both pointer and return-value versions

**Teaching note:**
This is the canonical call-by-value bug. Students who don't get this should go back to the "Value Semantics and Call-by-Value" section in the README and the "Mutating a Struct Through a Pointer" exercise. The return-value fix is often preferable in Go over the pointer-argument fix for simple computations — it makes the data flow explicit.

---

## Section 5: Discussion — Answer Key

### 5.1 — Pointer use philosophy [2 pts]

**Example strong answer:**
The statement is largely correct and reflects idiomatic Go. Go's standard library and most well-regarded Go code pass values by default and use pointers only for specific reasons: mutation intent, avoiding large struct copies, representing optional/absent values via nil, or sharing identity across concurrent goroutines. This default communicates API intent clearly — a function accepting `Person` promises it will not modify the caller's person, while `*Person` signals it may.

The three most important considerations: (1) **Mutation** — if a function must modify its argument, it must take a pointer; this is non-negotiable. (2) **Struct size** — for structs with many fields, passing by pointer avoids per-call copy overhead, which matters in hot paths (see [[go/16. Performance and Profiling]]). (3) **Reference-like types** — slices and maps already contain internal pointers, so wrapping them in `*[]T` or `*map[K]V` is usually unnecessary indirection. The garbage collection consideration: heap-allocated values (from pointer escaping) increase GC pressure; excessive pointer use in tight loops can measurably slow a program down.

**Elements that earn full credit:**
- Correctly identifies that values are the safe default and lists at least two of: mutation, struct size, optional nil, reference-like types
- Addresses the communication/API design angle (value = immutable intent, pointer = may mutate)
- Acknowledges the GC/performance angle without overstating it

**Rubric:**
- 2 pts: Well-reasoned answer addressing at least three distinct considerations with accurate technical content
- 1 pt: Correct general position but only one or two considerations addressed, or the reasoning is imprecise
- 0 pts: Claims pointers should always be used everywhere, or cannot articulate any criterion for choosing

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Generic Set with pointer vs value receivers [+5 pts]

**Full credit answer:**
```go
package main

import "fmt"

// Set is a generic set type backed by a map.
type Set[T comparable] struct {
    m map[T]struct{}
}

// Add inserts value into the set. Uses pointer receiver because it modifies
// the set's internal map (and may need to initialize it).
func (s *Set[T]) Add(value T) {
    if s.m == nil {
        s.m = make(map[T]struct{})
    }
    s.m[value] = struct{}{}
}

// Contains reports whether value is in the set.
// Could use a value receiver (read-only), but pointer receiver is fine for consistency.
func (s *Set[T]) Contains(value T) bool {
    _, ok := s.m[value]
    return ok
}

// Size returns the number of elements in the set.
func (s *Set[T]) Size() int {
    return len(s.m)
}

func main() {
    s := &Set[int]{}
    s.Add(1)
    s.Add(2)
    s.Add(3)
    s.Add(2)  // duplicate — set should not grow

    fmt.Println("Size:", s.Size())             // 3
    fmt.Println("Contains 2:", s.Contains(2)) // true
    fmt.Println("Contains 5:", s.Contains(5)) // false
}
```

**Expected output:**
```
Size: 3
Contains 2: true
Contains 5: false
```

**Explanation of receiver choice:**

`Add` **must** use a pointer receiver for two reasons: (1) it modifies the set's internal state (`s.m[value] = struct{}{}`), and (2) if `s.m` is nil (zero-value `Set`), it needs to initialize the map. A value receiver would work for the map mutation (since map values are already reference-like), but the nil initialization (`s.m = make(...)`) would require a pointer receiver to persist.

`Contains` and `Size` are read-only operations. They could technically use value receivers. However, Go's convention is: **once any method on a type uses a pointer receiver, all methods should use pointer receivers** — mixed receiver types cause confusion about whether the value or pointer satisfies an interface. Since `Add` must use `*Set[T]`, `Contains` and `Size` should also use `*Set[T]` for consistency.

This directly connects to pointer semantics: the decision between value and pointer receiver follows the same logic as deciding whether a function argument should be `T` or `*T` — does the method need to mutate the receiver, and is consistency with other methods required?

**Rubric:**
- 5 pts: Correct generic syntax, correct implementation of all three methods, pointer receiver on `Add` with valid justification, explanation of the consistency rule for mixed receivers
- 3 pts: Correct implementation but incorrect or missing explanation of receiver choice, or minor generic syntax error
- 1 pt: Demonstrates understanding of pointer receivers and sets but fails to implement generics correctly (uses `interface{}` instead of type parameters, for example)
- 0 pts: Does not attempt or fundamentally misunderstands pointer receivers

**Teaching note:**
Students who attempt this are previewing [[go/6. Methods and Interfaces]] (pointer receivers) and [[go/10. Generics]] (type parameters). Full credit is intentionally demanding — it requires synthesizing pointer semantics with two concepts from future modules. Partial credit for a working `Set[any]` or `Set[int]` without generics, but with correct pointer reasoning.

---

## Common Wrong Answers Across the Test

1. **Confusing pointer to a map with map as a pointer** — students sometimes think `*map[K]V` is the same as `map[K]V` or that both equally share mutations. The distinction: `map[K]V` already shares mutations (it's a reference type); `*map[K]V` is needed only to replace the map itself.
2. **Forgetting the nil guard** — students write functions that accept pointers and immediately dereference without checking for nil. Always ask: "what happens if someone passes nil to this?"
3. **Returning `&localVar` from a function and worrying it's unsafe** — this is safe in Go (unlike C). Students from C/C++ backgrounds are conditioned to avoid it. The compiler allocates on the heap. No action needed.
4. **Using `*[]T` for slice mutation** — for modifying elements, a plain `[]T` works because the slice already contains an internal pointer. `*[]T` is needed only when the length must change and you cannot use a return value.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who miss Section 1.5 (why pointer argument allows mutation despite call-by-value) likely have not internalized the call-by-value model. Send them back to the "Value Semantics and Call-by-Value" core concept and Exercise 5.
- Students who miss Section 2.2 (maps don't need `*map[K]V`) likely have a misconception about reference types. Recommend reading [[go/4. Composite Types]] section on map internals and then reviewing the "Slices, Maps, and Channels Are Already Reference-Like" section of this module.
- Section 4.1 (debugging countWords) tests the same concept as Section 2.1 but in a concrete scenario. If a student gets 2.1 right but misses 4.1, they understand the concept abstractly but not concretely — more exercise practice is the fix.
- Bonus question 6.1 is genuinely hard for a student who hasn't seen generics yet. Be generous with partial credit: if the pointer receiver reasoning is sound, award 3/5 even if the generic syntax is off.
- A score below 60% suggests either the prerequisite modules (especially [[go/3. Functions]] and [[go/4. Composite Types]]) were not solid, or the learner read without practicing. In either case, return to EXERCISES.md exercises 3 and 5 before re-taking the test.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
