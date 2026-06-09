# Notes — Module 3: Functions

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/3. Functions]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Functions))
    Declarations and Signatures
      parameter shorthand (x, y int)
      multiple return types
      named return values
    Call-by-Value
      scalars copied independently
      slices share backing array
      maps share hash table
      pointers dereference to original
    Multiple Return Values
      (result, error) convention
      error always last
      _ to discard values
    Named Returns and Naked Returns
      documentation value
      defer interaction
      avoid in long functions
    error idiom
      errors.New
      fmt.Errorf with %w
      nil means success
    Variadic Functions
      ...T parameter is a slice
      spread with slice...
      only last param can be variadic
    First-Class Functions
      function types (func(T) T)
      nil zero value panics
      stored in variables and maps
    Closures
      capture by reference
      loop-variable pitfall
      Go 1.22 per-iteration fix
      stateful iterators
    Higher-Order Functions
      filter, map, reduce patterns
      function factories
      standard library examples
    Recursion
      base case required
      no tail-call optimization
      mutually recursive functions
    defer + Named Returns
      closure modifies named return
      error wrapping pattern
    Method Values
      bound receiver
      same as function value
      forward ref to Module 6
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **Closures capture references, not values:** _I finally understood why the loop-variable bug exists: the closure doesn't make a copy of `i` — it holds a reference to the variable itself. By the time the closures run, the loop is done and `i` is at its terminal value._
2. **Slices are three words, not one:** _The "photocopy" mental model clicked when I thought of a slice as a struct with three fields (pointer, len, cap). Copying a slice copies those three fields, not the underlying array. That's why element mutation is visible but append isn't._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### Call-by-Value

_Your explanation here_

_What I'm still unsure about:_ (e.g., when exactly does append allocate a new backing array vs reuse the existing one?)

### Closures and Capture

_Your explanation here_

_What I'm still unsure about:_ (e.g., how long does a captured variable live if the outer function has returned? Does the GC collect it?)

### The (result, error) Convention

_Your explanation here_

_What I'm still unsure about:_ (e.g., is there a way to make the compiler enforce that callers check the error?)

### defer + Named Returns

_Your explanation here_

_What I'm still unsure about:_ (e.g., what order do deferred closures run in if there are multiple in the same function?)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| defer + named returns | [[go/2. Control Flow]] | defer was introduced in Module 2; named returns reveal the full power of defer by allowing deferred closures to modify what the function returns |
| (result, error) return | [[go/8. Error Handling]] | The convention learned here (error last, nil for success, fmt.Errorf with %w) is the foundation of all error handling in Go |
| Closures in goroutines | [[go/9. Concurrency]] | Goroutines are almost always launched as closures; the loop-variable capture pitfall is especially dangerous in concurrent code where closures run in separate goroutines |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] What happens to captured variables when the outer function returns? Are they moved to the heap? → added to QUESTIONS.md as Q001
- [ ] Can a deferred function itself defer another function? → might be answered experimentally
- [ ] What is the performance cost of closures vs plain function calls? → might be answered in the profiling module

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The error wrapping pattern with defer + named returns

```go
func operation(arg T) (result R, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("operation: %w", err)
        }
    }()
    // any error returned here is automatically wrapped
    return
}
```

_Why I'm saving this:_ This is the cleanest way to ensure every error from a function carries the function's name as context. Used in production Go code to build rich error chains.

---

### The function factory pattern

```go
func multiplier(factor int) func(int) int {
    return func(n int) int { return n * factor }
}

double := multiplier(2)
triple := multiplier(3)
```

_Why I'm saving this:_ Factory functions that return closures are Go's lightweight substitute for objects when you only need one operation. The captured variable (`factor`) is the "field", the returned closure is the "method".

---

### Spreading a slice into a variadic call

```go
nums := []int{1, 2, 3}
result := sum(nums...)  // equivalent to sum(1, 2, 3)
```

_Why I'm saving this:_ Easy to forget the `...` suffix at the call site when passing a slice to a variadic function. Without it, you'd get a compile error (wrong type).

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **Loop-variable capture** — I initially thought each closure captured a copy of the loop variable at the time of creation. The `4, 4, 4, 4` output was a surprise. Now I remember: closures capture references.
- **append and call-by-value** — I expected `append(s, val)` inside a function to grow the caller's slice. It doesn't — the caller's slice header is unchanged. I need to either return the new slice or pass `*[]int`.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
