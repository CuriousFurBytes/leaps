# Notes — Module 8: Error Handling

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/8. Error Handling]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Error Handling))
    error interface
      Error() string method
      nil means success
      typed-nil trap
    creating errors
      errors.New static string
      fmt.Errorf formatted message
      %w wrapping verb
      %v opaque no chain
    error chains
      errors.Unwrap linked list
      errors.Is sentinel matching
      errors.As type extraction
      errors.Join multiple errors Go 1.20
    custom error types
      struct with Error() string
      carry structured data
      return as error not *MyError
    panic and recover
      programmer errors only
      defer + recover at boundary
      re-panic pattern
      never for expected failures
    named returns + defer
      deferred error decoration
      single wrap point
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **error is just an interface:** _I finally understood that `error` is nothing special — it is a built-in interface with one method. Any type with `Error() string` satisfies it. The same structural typing from [[go/6. Methods and Interfaces]] applies._
2. **%w vs %v changes everything:** _Using `%v` in `fmt.Errorf` creates an opaque new error — the chain is cut there. Using `%w` preserves the chain so `errors.Is` and `errors.As` can traverse it. This clicked when I saw `errors.Is` return false on a `%v`-wrapped sentinel._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### The error interface

_Your explanation here_

_What I'm still unsure about:_ (e.g., exactly what happens when you return a typed nil as error)

### errors.Is vs errors.As

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens when errors.Join is used — does errors.Is traverse all joined errors?)

### Panic and recover

_Your explanation here_

_What I'm still unsure about:_ (e.g., can recover be called from a function called by a deferred function, or only directly in the deferred function?)

### Error wrapping with %w

_Your explanation here_

_What I'm still unsure about:_ (e.g., can you wrap multiple errors with a single fmt.Errorf call before Go 1.20?)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| error is an interface | [[go/6. Methods and Interfaces]] | `error` is satisfied structurally — any type with `Error() string` qualifies; the same nil-interface subtleties apply |
| if err != nil pattern | [[go/2. Control Flow]] | The init-statement form `if err := f(); err != nil` is the canonical usage; defer also interacts with named return error decoration |
| Named returns + deferred decoration | [[go/3. Functions]] | Named return values enable deferred functions to modify the error before the function returns |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] What happens when `recover()` is called outside a deferred function — does it panic, return nil, or cause a compile error? → added to QUESTIONS.md as Q001
- [ ] Can `errors.Join(nil, nil)` return nil, or does it return a non-nil joined error? → needs testing
- [ ] Does the `errors.Is` traversal for `errors.Join` check breadth-first or depth-first? → might matter for nested joined errors

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The canonical wrap-and-return pattern

```go
func doWork(path string) error {
    data, err := os.ReadFile(path)
    if err != nil {
        return fmt.Errorf("doWork %s: %w", path, err)
    }
    // ...
    return nil
}
```

_Why I'm saving this:_ This is the single most common error pattern in Go. The function name + operand + `%w` gives context without leaking internals. The `%w` preserves the chain.

---

### The recover-at-boundary pattern

```go
func safeCall(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic: %v", r)
        }
    }()
    fn()
    return nil
}
```

_Why I'm saving this:_ Named return `err` lets the deferred function set the return value. This is the idiomatic recover-to-error conversion used in middleware and plugin systems.

---

### errors.As vs type assertion

```go
// Wrong — fails if the error is wrapped:
pe, ok := err.(*ParseError)

// Right — traverses the chain:
var pe *ParseError
if errors.As(err, &pe) {
    // pe is now the *ParseError from anywhere in the chain
}
```

_Why I'm saving this:_ Forgetting this is the most common `errors.As` mistake. The target must be a pointer (`&pe`), and the type you're looking for (`*ParseError`) is inferred from the type of `pe`.

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **Typed-nil trap** — I initially thought returning `var e *MyError; return e` from a function returning `error` would give a nil error. It actually gives a non-nil interface with a nil value. The fix is always `return nil` for the success case, never return a typed nil.
- **%w vs %v** — I initially used `%v` everywhere in `fmt.Errorf` without realizing it cuts the error chain. Once I tried `errors.Is` on a `%v`-wrapped sentinel and got `false`, the distinction became concrete.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
