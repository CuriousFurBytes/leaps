# Notes — Module 4: Composite Types

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/4. Composite Types]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Composite Types))
    Arrays
      fixed size part of type
      value semantics full copy
      backing store for slices
    Slices
      three-word header ptr len cap
      sharing and aliasing
      append may reallocate
      copy for independent clones
      nil vs empty
      three-index slice expression
      slices package 1.21
    Maps
      hash table unordered
      nil map panics on write
      comma-ok idiom
      delete
      iteration order randomized
      maps as sets struct{}
      maps of slices
      maps package 1.21
      concurrency caveat
    Strings
      immutable byte slice
      rune vs byte
      string to byte to rune
      strings.Builder
    Structs
      value semantics
      named literals vs positional
      embedding promotes fields
      comparable if all fields comparable
      empty struct zero bytes
      struct tags for reflection
      memory layout and alignment
    Connections
      Links to go/5 Pointers
      Links to go/6 Methods and Interfaces
      Links to memory-management
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **Slices are headers, not data:** _I finally understood that assigning a slice copies the three-word header (ptr, len, cap), not the underlying array. Two slice variables can point into the same array without either "knowing" about the other. This is why `append` must return a value — it may have changed the ptr._
2. **nil map reads safely, writes panic:** _A nil map is not like a null pointer — reads return the zero value without panic. Only writes panic. Knowing this lets me read from optional maps safely and reliably diagnose the "assignment to entry in nil map" panic._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### Arrays

_Your explanation here_

_What I'm still unsure about:_ (e.g., when does the compiler allocate an array on the stack vs heap?)

### Slices (the header)

_Your explanation here_

_What I'm still unsure about:_ (e.g., exactly how the growth factor changes for large slices)

### append and reallocation

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens to the old backing array after reallocation — when does it get GC'd?)

### Maps

_Your explanation here_

_What I'm still unsure about:_ (e.g., how does Go implement hash randomization for map iteration?)

### Structs and embedding

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens when two embedded types both have a field with the same name?)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| Slice value semantics | [[go/5. Pointers]] | Passing a `*[]int` to a function lets the function modify the caller's slice header; this is the pointer side of the same coin |
| Struct fields and embedding | [[go/6. Methods and Interfaces]] | Methods are defined on types; embedding promotes not just fields but also methods, enabling interface satisfaction through composition |
| Maps are not concurrent-safe | [[go/9. Concurrency]] | Any map accessed from multiple goroutines needs a mutex or `sync.Map`; this module introduces the footgun, Module 9 fixes it |
| Backing array lifecycle | [[memory-management]] | The GC manages backing arrays; escape analysis determines whether a slice's backing array lives on the stack or heap |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] When two embedded types both have a field with the same name, what does Go do? → added to QUESTIONS.md as Q001
- [ ] After `append` causes a reallocation, when does the old backing array get garbage collected? → might be answered in memory-management module
- [ ] Can you use a struct as a map key if the struct contains an array field? → add to QUESTIONS.md as Q002

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The safe slice copy pattern

```go
// When you need an independent copy of a slice, never do: clone := s
// Instead:
clone := make([]int, len(s))
copy(clone, s)
// Or with the slices package (Go 1.21+):
clone2 := slices.Clone(s)
```

_Why I'm saving this:_ The plain assignment `clone := s` copies the header only. Mutations to `clone` elements will silently affect `s` and vice versa. `copy` is the safe alternative.

---

### Maps as sets

```go
// Set with struct{} (zero bytes)
seen := make(map[string]struct{})
seen["apple"] = struct{}{}
_, ok := seen["apple"] // ok = true if present
```

_Why I'm saving this:_ This pattern comes up constantly for deduplication, visited-node tracking in graph traversal, and indexing. The `struct{}{}` syntax looks weird but `struct{}` is the zero-byte type.

---

### The comma-ok idiom

```go
if v, ok := m[key]; ok {
    // key exists; v is the value
} else {
    // key not present; v is the zero value
}
```

_Why I'm saving this:_ Without comma-ok, a missing key and a key with zero value are indistinguishable. This is the canonical safe map read.

---

### maps of slices (append-to-nil pattern)

```go
byKey := make(map[string][]string)
byKey["a"] = append(byKey["a"], "apple")  // nil + append = new slice
byKey["a"] = append(byKey["a"], "avocado")
// Works because a missing map key returns nil, and append(nil, x) works
```

_Why I'm saving this:_ Idiomatic grouping pattern. No initialization of the inner slice is required — reading a missing key returns `nil`, and `append(nil, x)` correctly creates a new slice.

---

### Three-index slice (capacity-limiting sub-slice)

```go
// Limit capacity to prevent sub-slice from clobbering the original
safe := full[low:high:high] // cap == high - low == len
// Now append to safe will always reallocate, never touch full[high:]
```

_Why I'm saving this:_ This is the defensive form when passing a sub-slice to a function that might `append` to it. Without the third index, the sub-slice has extra capacity into the parent's elements.

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **append must always be assigned back** — I initially thought `append(s, x)` modified `s` in place. It doesn't — it returns a (possibly different) slice that must be assigned back: `s = append(s, x)`. The compiler doesn't warn you if you forget the assignment.
- **Sub-slice aliasing** — I initially thought `sub := s[1:3]` gave me a new, independent slice. It shares the backing array. Modifying `sub[0]` modifies `s[1]`.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
