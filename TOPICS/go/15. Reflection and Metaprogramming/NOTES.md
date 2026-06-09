# Notes — Module 15: Reflection and Metaprogramming

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/15. Reflection and Metaprogramming]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Reflection))
    Three Laws
      Law 1: ValueOf/TypeOf from interface
      Law 2: Interface() back to any
      Law 3: settability requires pointer
    reflect.Type
      Name vs Kind distinction
      NumField / Field(i)
      StructTag.Get / Lookup
    reflect.Value
      Addressability
      CanSet check
      Set / SetInt / SetString
      Call for methods
    Struct Tags
      json name + omitempty + dash
      encoding/json uses tags
      database/sql mappers
      custom tag parsers
    go generate
      stringer tool
      directive comment
      generated files committed
      zero reflection overhead
    When to use what
      reflection — truly unknown types
      generics — constrained unknown types
      go generate — known but numerous types
      interfaces — behavioral abstraction
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **The pointer dance:** _I finally understood why you need `reflect.ValueOf(&x).Elem()` instead of `reflect.ValueOf(x)` — passing x copies it into the interface, and you can't set a copy. The pointer gives reflect a path back to the original memory._
2. **Kind over Type for generic handlers:** _Switching on Kind (not Type) was the key insight for writing code that handles both `int` and `type UserID int` in the same branch._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### The Three Laws of Reflection

_Your explanation here_

_What I'm still unsure about:_ (e.g., what exactly is stored in a reflect.Value vs a reflect.Type)

### reflect.Type vs reflect.Value

_Your explanation here_

_What I'm still unsure about:_ (e.g., when do I need Type vs when do I need Value?)

### Struct Tags

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens if I call Tag.Get with an unknown key?)

### Addressability and Settability

_Your explanation here_

_What I'm still unsure about:_ (e.g., are all fields of an addressable struct addressable?)

### go generate

_Your explanation here_

_What I'm still unsure about:_ (e.g., when do I commit generated files vs regenerate each build?)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| reflect.ValueOf takes interface{} | [[go/6. Methods and Interfaces]] | The interface stores a (type, value) pair; reflection unpacks that pair |
| Struct tags and field metadata | [[go/4. Composite Types]] | Tags are part of struct field declarations; must understand structs to iterate fields |
| Reflection vs generics tradeoff | [[go/10. Generics]] | Generics solve at compile time what reflection solves at runtime; different cost/safety profiles |
| Reflection performance overhead | [[go/16. Performance and Profiling]] | Reflection calls are measurably slower; profiling shows where they matter |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] Can you use reflection on channel values — send and receive? → added to QUESTIONS.md as Q001
- [ ] Is reflect.DeepEqual implemented using reflection internally? → probably yes, worth checking
- [ ] Does the compiler inline any reflect calls, or is every call truly dynamic? → added to QUESTIONS.md as Q002

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The settable-value pattern

```go
// To set a field via reflection, always pass a pointer and call Elem()
v := reflect.ValueOf(&myStruct).Elem()
f := v.FieldByName("MyField")
if f.CanSet() {
    f.SetString("new value")
}
```

_Why I'm saving this:_ This is the only correct way to set values. Forgetting the `&` and `.Elem()` causes a panic that only surfaces at runtime.

---

### The tag-parsing idiom

```go
tag := field.Tag.Get("json")        // "" if absent
if tag == "-" { continue }          // explicitly excluded
parts := strings.SplitN(tag, ",", 2)
name := field.Name                  // default
if parts[0] != "" { name = parts[0] }
omitempty := len(parts) > 1 && parts[1] == "omitempty"
```

_Why I'm saving this:_ This is the exact logic encoding/json uses. Internalizing it means I can reason about why a field is or isn't in JSON output.

---

### go:generate directive

```go
//go:generate stringer -type=MyType
```

_Why I'm saving this:_ The comment must start at column 0, there must be no space between `//` and `go:generate`, and the tool invocation follows the same quoting rules as a shell command. Easy to get wrong.

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **CanSet vs IsValid** — I initially confused `CanSet()` (can I modify this value?) with `IsValid()` (does this Value hold anything at all?). A zero `reflect.Value` (returned by failed `FieldByName`) is not valid; calling anything on it panics. Always check `IsValid()` before `CanSet()`.
- **Kind vs Type confusion** — I initially tried to compare `v.Type() == reflect.TypeOf(0)` to check for integers, which missed `type MyInt int`. Switching on `v.Kind()` handles all int-kinded types uniformly.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
