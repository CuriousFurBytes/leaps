# Notes — Module 5: Pointers

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/5. Pointers]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Pointers))
    Memory Model
      variable has address
      pointer holds an address
      dereference = go to that address
    Operators
      & address-of
      * dereference (type context)
      * dereference (expression context)
    Nil
      zero value for all pointer types
      nil dereference → runtime panic
      always nil-guard before dereferencing
    Call-by-Value
      Go copies all arguments
      pointer arg → shared access to original
      value arg → independent copy
    When to Use Pointers
      mutation by callee
      large structs (avoid copy cost)
      optional / nullable (nil = absent)
      shared identity
    Allocation
      new(T) → zeroed *T
      &T{} → composite literal address
      prefer &T{} for structs
    Struct Pointer Convenience
      p.Field auto-dereferences (*p).Field
      used heavily with method receivers
    Reference-Like Types
      slice header = ptr + len + cap
      map value = pointer to hash table
      channel = pointer to runtime struct
      append may replace underlying array
    No Pointer Arithmetic
      deliberate safety decision
      unsafe package exists but rarely used
    Escape Analysis
      stack = lives only in function
      heap = outlives function call
      compiler decides automatically
      returning &local is safe in Go
    Double Pointer
      **T for reassigning pointer itself
      rare in idiomatic Go
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **Pointer = address, dereference = visit:** _I finally understood pointers when I pictured memory as a row of boxes. A pointer is a box that contains another box's number (address). `*p` means "go to box number `p`, read or write its contents."_
2. **Call-by-value is WHY pointers exist:** _Go always copies function arguments. Pointers are not a special feature — they are just values that happen to be addresses. Passing `&x` gives the function a copy of x's address, which lets it reach back and modify x._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### What a pointer is

_Your explanation here_

_What I'm still unsure about:_ (e.g., the exact definition of "addressable" — why can't you take `&m["key"]`?)

### `&` and `*` operators

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens if I do `**p` when p is `*int`)

### Nil and nil-pointer panics

_Your explanation here_

_What I'm still unsure about:_ (e.g., the difference between a nil pointer and an interface containing a nil pointer)

### When to use pointers vs values

_Your explanation here_

_What I'm still unsure about:_ (e.g., how large does a struct need to be before passing by pointer is worth it?)

### Slices are already reference-like

_Your explanation here_

_What I'm still unsure about:_ (e.g., exactly when does `append` reallocate vs reuse the existing array?)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| Pointer receivers (preview) | [[go/6. Methods and Interfaces]] | Methods with `*T` receivers use pointer semantics from this module; `func (p *Counter) Increment()` is syntactic sugar for a function that mutates through a pointer |
| Escape analysis (preview) | [[go/16. Performance and Profiling]] | The `-gcflags='-m'` flag shows which variables escape; heap allocations show up in pprof heap profiles; reducing unnecessary pointer escapes is a common optimization |
| Slice internals | [[go/4. Composite Types]] | A slice header is a struct with a pointer field; understanding slice-as-pointer explains why mutations propagate but `append` length changes do not |
| nil interface values | [[go/8. Error Handling]] | A nil `*MyError` wrapped in an `error` interface is not nil — this is a classic Go gotcha that connects pointer nil with interface nil |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] Why can't you take the address of a map element (`&m["key"]`)? What would go wrong? → added to QUESTIONS.md as Q001
- [ ] When is using `*[]T` appropriate vs just returning a `[]T`? → might be answered in a later module
- [ ] Does passing a pointer to a function always cause the pointed-to variable to escape to the heap? → added to QUESTIONS.md as Q002

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The fundamental pointer pattern

```go
x := 42
p := &x     // p holds the address of x
*p = 100    // changes x through p
fmt.Println(x)  // 100
```

_Why I'm saving this:_ This is the irreducible minimum. If this clicks, everything else follows.

---

### The nil guard before dereference

```go
func process(p *MyStruct) {
    if p == nil {
        return  // always guard before dereferencing
    }
    p.Field = "something"  // safe: p is not nil
}
```

_Why I'm saving this:_ The nil guard is a mandatory reflex. Every function that receives a pointer should decide whether nil is valid and either handle or reject it explicitly.

---

### `&T{}` preferred over `new(T)`

```go
// Prefer:
p := &MyStruct{Name: "Alice"}

// Over:
p := new(MyStruct)
p.Name = "Alice"
```

_Why I'm saving this:_ `&T{}` is idiomatic, initializes in one expression, and is consistent with all composite type literals. `new` works but is rare in modern code.

---

### Returning a pointer to a local variable (safe in Go)

```go
func newPoint(x, y float64) *Point {
    p := Point{X: x, Y: y}  // p escapes to heap
    return &p                // safe: compiler handles it
}
```

_Why I'm saving this:_ This is legal and idiomatic Go. In C this would be undefined behavior. The reminder prevents me from adding unnecessary indirection to avoid "returning local variable address."

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **Struct mutation without a pointer** — I initially wrote `func update(s MyStruct)` and was confused why the original wasn't changing. The fix was always to use `*MyStruct` and pass `&s` at the call site.
- **Map element address** — I tried `p := &myMap["key"]` and got a compile error. Maps can relocate their entries during growth; the address of a map element is not stable, so Go disallows taking it.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
