# Notes — Module 10: Generics

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/10. Generics]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Generics))
    Type Parameters
      syntax: func F[T C](...)
      type parameter list in []
      multiple parameters: [K, V]
    Constraints
      interfaces as constraints
      any — no operations
      comparable — == and !=
      cmp.Ordered — < > <= >=
      union elements |
      tilde ~ underlying type
    Generic Types
      struct with type parameters
      Stack[T any]
      Set[T comparable]
      methods reference T, not new params
    Type Inference
      compiler solves T from arguments
      explicit when T only in return type
    Standard Packages
      slices — Sort SortFunc Contains
      maps — Keys Values Clone
      cmp — Compare Ordered
    When NOT to Use
      method dispatch → use interface
      one concrete type → skip it
      no duplication → YAGNI
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **Constraints are interfaces:** _I finally understood that generics don't add a new concept — constraints reuse the existing interface mechanism. An interface that describes a type set is the same thing as an interface that describes a method set, just with type elements instead of method elements._
2. **`~` solves the named-type problem:** _The tilde operator was the insight I needed: without it, `type Celsius float64` doesn't satisfy `float64` in a constraint. With `~float64`, any type whose underlying type is float64 — including Celsius — satisfies the constraint._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### Type Parameters

_Your explanation here_

_What I'm still unsure about:_ (e.g., when does type inference fail and I need to be explicit?)

### Constraints

_Your explanation here_

_What I'm still unsure about:_ (e.g., can I mix method elements and type elements in the same constraint? What does that mean?)

### The `~` Token

_Your explanation here_

_What I'm still unsure about:_ (e.g., what is "underlying type" for a struct vs a named scalar?)

### Generic Types (Stack, Set)

_Your explanation here_

_What I'm still unsure about:_ (e.g., why can't methods add new type parameters?)

### When to Use Generics vs Interfaces

_Your explanation here_

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| Constraints as interfaces | [[go/6. Methods and Interfaces]] | Constraints extend the interface mechanism; an interface used as a constraint can contain type elements (unions) in addition to method elements |
| Generic Stack[T] wrapping []T | [[go/4. Composite Types]] | The Stack stores items in a `[]T` slice internally; all slice operations (append, len, slicing) work on `[]T` just as they do on `[]int` |
| Testing generic functions | [[go/11. Testing and Benchmarking]] | Table-driven tests should include rows for each interesting type instantiation; benchmark generic vs concrete to understand the overhead |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] Can a constraint contain both method elements and type elements? What does that mean at the call site? → added to QUESTIONS.md as Q001
- [ ] What happens with generics and reflect — does reflect.TypeOf return the concrete type T or the type parameter? → might be answered in a later module
- [ ] Is there a way to get the name/kind of T at runtime without reflect? → likely no; add to QUESTIONS.md

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The zero-value pattern for generic returns

```go
func First[T any](s []T) (T, bool) {
    if len(s) == 0 {
        var zero T   // zero value of T, whatever T is
        return zero, false
    }
    return s[0], true
}
```

_Why I'm saving this:_ `var zero T` is the idiomatic way to get a zero value for an unknown type. You cannot write `return nil, false` because T may not be a pointer or interface type.

---

### The constraint with ~ pattern

```go
type Ordered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
    ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
    ~float32 | ~float64 | ~string
}
```

_Why I'm saving this:_ This is the shape of `cmp.Ordered`. The `~` is what makes it inclusive of user-defined named types. Understanding this one interface unlocks most numeric/ordered generic functions.

---

### The method-cannot-have-type-params workaround

```go
// What you want (doesn't compile):
// func (s *Stack[T]) Map[U any](f func(T) U) []U { ... }

// What you write instead (package-level function):
func StackMap[T, U any](s *Stack[T], f func(T) U) []U {
    result := make([]U, s.Len())
    for i, v := range s.items {
        result[i] = f(v)
    }
    return result
}
```

_Why I'm saving this:_ This restriction surprises everyone. The workaround — flip to a package-level function where the receiver becomes a regular parameter — is idiomatic and straightforward.

---

### slices.SortFunc with cmp.Compare

```go
slices.SortFunc(people, func(a, b Person) int {
    if c := cmp.Compare(a.Age, b.Age); c != 0 {
        return c
    }
    return cmp.Compare(a.Name, b.Name)
})
```

_Why I'm saving this:_ This is the modern idiomatic sort pattern. cmp.Compare returns -1/0/+1, the chained-if pattern handles multi-key sorts cleanly, and slices.SortFunc is type-safe unlike the old sort.Slice.

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **`any` vs `comparable`** — I initially tried to use `==` inside a function constrained by `any`, and got a confusing compile error. It clicked when I realized `any` means "you can't do anything type-specific with T" — it only permits assignment and passing.
- **Forgetting `~`** — I wrote a constraint `float32 | float64` and was confused when `type Celsius float64` didn't satisfy it. The fix is always `~float32 | ~float64`.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
