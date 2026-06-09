# Module 15: Reflection and Metaprogramming

[← Module 14: Databases and Persistence](../14.%20Databases%20and%20Persistence/) | [Topic Home](../README.md) | [Module 16: Performance and Profiling →](../16.%20Performance%20and%20Profiling/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-5--7h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [The Three Laws of Reflection](#the-three-laws-of-reflection)
  - [reflect.Type and reflect.Value](#reflecttype-and-reflectvalue)
  - [Kind vs Type](#kind-vs-type)
  - [Inspecting Structs and Reading Struct Tags](#inspecting-structs-and-reading-struct-tags)
  - [Addressability and Settability](#addressability-and-settability)
  - [Constructing Values and Calling Methods](#constructing-values-and-calling-methods)
  - [Code Generation with go generate](#code-generation-with-go-generate)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Related Concepts](#related-concepts)
- [Exercises](#exercises)
- [Test](#test)
- [Projects](#projects)
- [Further Reading](#further-reading)
- [Learning Journal](#learning-journal)

---

## Overview

This module covers **Go's `reflect` package, struct tags, and compile-time code generation with `go generate`**. Reflection is the ability of a program to inspect and manipulate its own structure at runtime — to ask "what type is this value?", "what fields does this struct have?", "what methods does this object expose?" — without knowing those answers at compile time.

By the end of this module, you will understand how `encoding/json`, `database/sql` mappers, and ORMs work under the hood; how to read struct tags to build your own serializers; the precise rules governing which values can be set via reflection; and when code generation is the better alternative to runtime reflection. This knowledge sits at the boundary of meta-level programming in Go — essential for building frameworks, writing generic serialization, and understanding the standard library's most powerful packages.

**Difficulty:** Advanced &nbsp;|&nbsp; **Estimated time:** 5–7 hours

---

## Learning Goals

By completing this module, you will be able to:

1. State the three Laws of Reflection and explain what each one means — _given a `reflect.Value`, predict whether it is addressable and settable_
2. Use `reflect.TypeOf` and `reflect.ValueOf` to inspect types, kinds, and field metadata at runtime — _write a function that prints every exported field name and value of any struct_
3. Read struct field tags (e.g., `json:"name,omitempty"`) using the `reflect.StructTag` API — _implement a minimal struct-to-map serializer that respects `json` tags_
4. Set values via reflection correctly, explaining why a pointer's `Elem()` is required — _write a function that takes `interface{}` and zeroes all exported `int` fields of the passed struct pointer_
5. Explain the real costs of reflection — speed, loss of compile-time type safety, reduced readability — and articulate when generics or interfaces are the better choice — _given a code review scenario, argue for or against using reflection_
6. Use `go generate` to invoke a code generator, and explain why compile-time generation is preferable to runtime reflection for hot paths — _add a `//go:generate` directive and run it to produce a `String()` method with `stringer`_

---

## Prerequisites

### Required Modules

- [[go/6. Methods and Interfaces]] — you need to understand: interface types, type assertions (`v.(T)` and the comma-ok form), and the empty interface `interface{}`/`any`; reflection operates on interface values and many reflect functions accept `any`
- [[go/4. Composite Types]] — you need to understand: struct declarations, field names and types, anonymous fields, and embedding; the reflect package exposes struct fields as `reflect.StructField` values, so knowing struct layout is essential
- [[go/10. Generics]] — you need to understand: what type parameters solve and their compile-time nature; the comparison with reflection (runtime introspection) becomes clearer when you have used generics and can articulate what each approach gives up

### Required Concepts

- **Interfaces and dynamic dispatch** — `reflect.ValueOf(x)` takes an `interface{}` argument; understanding that the interface value carries both a type pointer and a data pointer is prerequisite to understanding the three Laws
- **Pointers and addressability** — reflection's settability rules are directly tied to Go's pointer semantics; you cannot set a field in a value-type copy, only in a pointer-based value
- **Struct field tags** — the raw syntax (`` `json:"name,omitempty"` ``) should be familiar from [[go/4. Composite Types]]; this module explains how to read them programmatically

> [!TIP]
> If struct embedding or type assertions feel shaky, spend 20–30 minutes reviewing them before continuing.
> The settability rules in particular will be confusing without solid pointer semantics.

---

## Why This Matters

Reflection is the machinery behind Go's most powerful standard-library packages. Without understanding it, you are using `encoding/json`, `database/sql`, and `text/template` as black boxes — you cannot debug unexpected behavior, extend them, or build analogous tools yourself.

Concretely, mastery of this module enables you to:

- **Understand how `encoding/json` works** — `json.Marshal` and `json.Unmarshal` use `reflect` to inspect struct fields, read `json` struct tags, and set field values dynamically; knowing this lets you debug marshaling surprises (why did this field get omitted? why is this field named differently in JSON?) without guessing
- **Build custom serializers and mappers** — whether you are writing a configuration loader, an ORM field mapper, or a template renderer, the pattern is the same: iterate struct fields, read their tags, map to target representations; this module teaches that pattern directly
- **Make informed tool choices** — reflection has real costs (3–10× slower than direct calls, no compile-time type checking, panics on misuse); knowing when to use generics or interfaces instead — and when reflection is genuinely the right tool — is a senior-level skill

Without understanding reflection, you would be unable to read framework source code, debug mysterious serialization behavior, or build tooling that works generically across user-defined types — capabilities that appear constantly in advanced Go development.

---

## Historical Context

Reflection as a language feature dates to **Lisp in the 1970s** and was formalized in languages like Smalltalk and Java. Java's `java.lang.reflect` package (introduced in **Java 1.1, 1997**) brought reflection to mainstream compiled languages and demonstrated both its power and its pitfalls: Spring Framework, Hibernate, and Jackson all rely on it heavily, but reflection-heavy Java code is notoriously slow and brittle.

Go's designers — **Robert Griesemer, Rob Pike, and Ken Thompson** — were aware of Java's experience. They chose to include reflection in the standard library (`reflect`, introduced in **Go's first public release, 2009**) but designed the language so that reflection is **not required** for ordinary programming. The interface system and, later, generics (Go 1.18, **2022**) provide most of what Java uses reflection for, without the runtime cost.

Key moments in Go's reflection story:

- **2009** — `reflect` package ships with Go's initial open-source release; the three Laws of Reflection are implicit in the design
- **2011** — Rob Pike publishes "The Laws of Reflection" on the Go Blog, formalizing the mental model that remains canonical today
- **2011** — `go generate` concept begins forming; the community develops `stringer` and similar tools as reflection alternatives
- **2014** — `go generate` (`go generate` command) added in Go 1.4, formalizing compile-time code generation as a first-class workflow
- **2022** — Go 1.18 generics give developers a type-safe, compile-time alternative to many reflection use cases; the question "generics or reflection?" becomes a real design choice

Understanding this history helps because it explains the "why not" alongside the "how": Go's designers gave you reflection as a last resort and an implementation tool for frameworks, not as the everyday abstraction mechanism it became in Java.

---

## Core Concepts

### The Three Laws of Reflection

Rob Pike's "Laws of Reflection" (Go Blog, 2011) are the foundational mental model. They are not arbitrary rules — they are consequences of how interface values work in Go.

**Law 1: Reflection goes from interface value to reflection object.**

`reflect.TypeOf(x)` and `reflect.ValueOf(x)` each take an `interface{}` and return a `reflect.Type` or `reflect.Value` representing the concrete value stored in that interface.

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    x := 3.14
    t := reflect.TypeOf(x)   // reflect.Type describing float64
    v := reflect.ValueOf(x)  // reflect.Value holding 3.14

    fmt.Println(t)            // float64
    fmt.Println(v)            // 3.14
    fmt.Println(t.Kind())     // float64 (the Kind)
    fmt.Println(v.Float())    // 3.14 (extract the float64 value)
}
```

When you pass `x` to `reflect.ValueOf`, Go wraps it in an interface value. The reflect package then inspects the interface's internal type pointer and data pointer. This means **everything reflection does starts from an interface value** — that is Law 1.

**Law 2: Reflection goes from reflection object back to interface value.**

You can convert a `reflect.Value` back to an `interface{}` using its `Interface()` method, then use a type assertion to recover the concrete value.

```go
v := reflect.ValueOf(3.14)
iface := v.Interface()          // interface{} holding float64(3.14)
f := iface.(float64)            // type assertion back to float64
fmt.Println(f)                  // 3.14
```

**Law 3: To modify a reflection object, the value must be settable.**

Not every `reflect.Value` can be modified. Setting requires the value to be **addressable** — which requires passing a pointer and calling `Elem()`. See [Addressability and Settability](#addressability-and-settability) for the full treatment.

---

### reflect.Type and reflect.Value

`reflect.Type` describes the type of a value. `reflect.Value` holds a value (and allows inspection and, conditionally, modification).

```go
package main

import (
    "fmt"
    "reflect"
)

type Point struct {
    X, Y float64
}

func main() {
    p := Point{X: 1.0, Y: 2.0}

    t := reflect.TypeOf(p)
    v := reflect.ValueOf(p)

    fmt.Println("Type name:", t.Name())        // Point
    fmt.Println("Type kind:", t.Kind())        // struct
    fmt.Println("Num fields:", t.NumField())   // 2

    // Iterate fields via Type
    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)          // reflect.StructField
        value := v.Field(i)          // reflect.Value of the field
        fmt.Printf("  Field %s (%s) = %v\n", field.Name, field.Type, value)
    }
    // Output:
    //   Field X (float64) = 1
    //   Field Y (float64) = 2
}
```

Key methods on `reflect.Type`:
- `Name()` — type name (empty for unnamed types like `[]int`)
- `Kind()` — the underlying kind (see next section)
- `NumField()`, `Field(i)` — struct fields
- `NumMethod()`, `Method(i)` — methods in the method set

Key methods on `reflect.Value`:
- `Kind()` — same Kind as the type
- `Interface()` — returns the value as `interface{}`
- `Field(i)`, `Index(i)`, `MapIndex(key)` — access composites
- `Call(args)` — call a function or method value
- `Set(v)`, `SetInt(n)`, `SetString(s)` — modify (requires settability)

---

### Kind vs Type

`Kind` and `Type` are frequently confused. The distinction is important:

- **`reflect.Type`** is the full, specific type — `int32`, `Point`, `[]string`, `map[string]int` are all distinct `reflect.Type` values.
- **`reflect.Kind`** is the underlying structural category — there are ~26 kinds: `Bool`, `Int`, `Int8`, `Int16`, `Int32`, `Int64`, `Uint`, ..., `Float32`, `Float64`, `Complex64`, `Complex128`, `Array`, `Chan`, `Func`, `Interface`, `Map`, `Pointer`, `Slice`, `String`, `Struct`, `UnsafePointer`.

```go
type Celsius float64
type Fahrenheit float64

c := Celsius(100)
f := Fahrenheit(212)

tc := reflect.TypeOf(c)
tf := reflect.TypeOf(f)

fmt.Println(tc.Name(), tc.Kind())  // Celsius float64
fmt.Println(tf.Name(), tf.Kind())  // Fahrenheit float64

// Same Kind, different Type
fmt.Println(tc == tf)              // false — different types
fmt.Println(tc.Kind() == tf.Kind()) // true — same kind
```

When writing code that handles arbitrary values (a serializer, an ORM mapper), you almost always switch on `Kind`, not `Type`, because `Kind` tells you how to extract the underlying data. Two user-defined types with the same Kind can be handled by the same code path.

```go
// Generic int-extractor: works for any int-kinded type
func toInt64(v reflect.Value) (int64, bool) {
    switch v.Kind() {
    case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
        return v.Int(), true
    default:
        return 0, false
    }
}
```

---

### Inspecting Structs and Reading Struct Tags

Struct tags are the mechanism by which packages like `encoding/json` and `database/sql` allow users to customize field mapping without writing boilerplate. A tag is a raw string literal attached to a struct field:

```go
type User struct {
    ID       int    `json:"id"              db:"user_id"`
    Name     string `json:"name,omitempty"  db:"full_name"`
    Password string `json:"-"`              // omit from JSON entirely
    internal int    // unexported — invisible to reflection callers
}
```

To read tags at runtime, use `reflect.StructField.Tag` — a value of type `reflect.StructTag` — and call its `Get(key)` or `Lookup(key)` method:

```go
package main

import (
    "fmt"
    "reflect"
)

type User struct {
    ID   int    `json:"id"             db:"user_id"`
    Name string `json:"name,omitempty" db:"full_name"`
}

func printTags(v interface{}) {
    t := reflect.TypeOf(v)
    if t.Kind() == reflect.Pointer {
        t = t.Elem() // dereference pointer to get struct type
    }
    for i := 0; i < t.NumField(); i++ {
        f := t.Field(i)
        jsonTag := f.Tag.Get("json")    // "" if absent
        dbTag := f.Tag.Get("db")
        fmt.Printf("Field: %-8s  json:%q  db:%q\n", f.Name, jsonTag, dbTag)
    }
}

func main() {
    printTags(User{})
    // Output:
    // Field: ID        json:"id"             db:"user_id"
    // Field: Name      json:"name,omitempty" db:"full_name"
}
```

`Tag.Get(key)` returns the empty string if the key is absent. `Tag.Lookup(key)` returns `(string, bool)` — the bool is false if the key is genuinely absent (as opposed to present with an empty value). Prefer `Lookup` when the distinction matters.

> [!NOTE]
> **How `encoding/json` uses this:** When `json.Marshal` encounters a struct, it iterates fields via `reflect.Type.NumField`/`Field(i)`, reads the `json` struct tag, and uses the tag value as the JSON key. When the tag contains `omitempty`, it skips zero-valued fields. When the tag is `"-"`, it skips the field entirely. The full parsing of multi-option tags (splitting on `,`) is a few lines of string manipulation layered on top of `Tag.Get("json")`.

---

### Addressability and Settability

This is where most reflection bugs originate. The rules:

1. A `reflect.Value` obtained by `reflect.ValueOf(x)` where `x` is a non-pointer is **not addressable** and **not settable** — modifying it would modify a copy.
2. To get a settable value, pass a **pointer**: `reflect.ValueOf(&x)`, then call `.Elem()` to get the value the pointer points to. That value is both addressable and settable.
3. Even with an addressable struct, only **exported** fields are settable. Calling `Set` on an unexported field panics.

```go
package main

import (
    "fmt"
    "reflect"
)

type Config struct {
    MaxRetries int
    Host       string
    timeout    int // unexported — cannot be set via reflection
}

func zeroInts(ptr interface{}) {
    v := reflect.ValueOf(ptr)
    if v.Kind() != reflect.Pointer || v.Elem().Kind() != reflect.Struct {
        panic("zeroInts requires a pointer to a struct")
    }
    s := v.Elem() // the struct value — addressable
    for i := 0; i < s.NumField(); i++ {
        f := s.Field(i)
        // CanSet returns false for unexported fields
        if f.Kind() == reflect.Int && f.CanSet() {
            f.SetInt(0)
        }
    }
}

func main() {
    cfg := Config{MaxRetries: 5, Host: "localhost", timeout: 30}
    fmt.Println("Before:", cfg) // {5 localhost 30}
    zeroInts(&cfg)
    fmt.Println("After:", cfg)  // {0 localhost 30}
    // timeout is unchanged — it's unexported, CanSet() returned false
}
```

**Why the pointer dance is necessary:** When you pass a value to a function (including `reflect.ValueOf`), Go copies it. The `reflect.Value` holds a copy — not the original. Setting the copy would have no effect on the caller's variable. Passing a pointer means `reflect.ValueOf` receives the pointer value, `Elem()` follows it to the original data, and `Set` writes through the pointer to the original.

**Checking before setting:**

```go
// Always check CanSet before calling Set — a panic is worse than a no-op
if f.CanSet() {
    f.Set(newValue)
}
```

---

### Constructing Values and Calling Methods

Reflection can create new values and call methods dynamically — the basis for dependency injection frameworks and RPC systems.

```go
package main

import (
    "fmt"
    "reflect"
)

// Adder adds two ints
type Adder struct{ Base int }

func (a Adder) Add(x int) int { return a.Base + x }

func main() {
    // Construct a new Adder using reflection
    t := reflect.TypeOf(Adder{})
    newVal := reflect.New(t)          // *Adder (pointer)
    newVal.Elem().FieldByName("Base").SetInt(10)

    // Call the Add method via reflection
    method := newVal.Elem().MethodByName("Add")
    args := []reflect.Value{reflect.ValueOf(5)}
    results := method.Call(args)

    fmt.Println(results[0].Int()) // 15
}
```

`reflect.New(t)` allocates a new zero value of type `t` and returns a `reflect.Value` of kind `Pointer`. `MethodByName` looks up a method by name in the value's method set; `Call` invokes it with a slice of `reflect.Value` arguments and returns a slice of `reflect.Value` results.

> [!WARNING]
> `Call` panics if the number or types of arguments do not match the method signature. There is no compile-time check. This is one of reflection's main drawbacks — errors surface at runtime, not build time.

---

### Code Generation with go generate

`go generate` is the compile-time alternative to runtime reflection. Instead of inspecting types at runtime, you write a program (or use an existing tool) that reads your Go source, generates new `.go` files, and those generated files are compiled as normal Go code — with full type safety, zero reflection overhead, and IDE support.

The workflow:

1. Add a `//go:generate` directive comment to any `.go` file:

```go
// In types.go
//go:generate stringer -type=Direction

package main

// Direction is a compass direction.
type Direction int

const (
    North Direction = iota
    East
    South
    West
)
```

2. Run `go generate ./...` — Go finds every `//go:generate` directive in your source and executes the specified command.

3. The `stringer` tool reads `types.go`, finds the `Direction` type and its constants, and writes `direction_string.go` containing a `String() string` method that returns `"North"`, `"East"`, etc. — without any runtime reflection.

**Why `go generate` over runtime reflection for `String()` methods:**

```go
// Generated code — zero overhead, type-checked at compile time:
func (d Direction) String() string {
    switch d {
    case North:
        return "North"
    case East:
        return "East"
    case South:
        return "South"
    case West:
        return "West"
    default:
        return fmt.Sprintf("Direction(%d)", int(d))
    }
}
```

A reflection-based `String()` that uses `reflect.TypeOf(d).Name()` and iterates constants would work but runs reflection machinery on every call. The generated version is a single switch — nanoseconds vs. microseconds on hot paths. See [[go/16. Performance and Profiling]] for how to measure this difference with benchmarks.

**Other common `go generate` tools:**
- `stringer` — `String()` methods for enum-like constants
- `mockgen` (gomock) — interface mock implementations
- `protoc-gen-go` — Protocol Buffer marshaling code from `.proto` files
- `sqlc` — type-safe SQL query code from `.sql` files

> [!NOTE]
> Generated files should be committed to version control. Name them with a `_gen.go` or `_string.go` suffix by convention. Add a comment at the top: `// Code generated by ...; DO NOT EDIT.`

---

### How the Concepts Fit Together

```
Any Go value
       │
       ▼
interface{} / any  ──────────────────── Law 1: ValueOf / TypeOf
       │
       ├──► reflect.Type  ─────────────  Name, Kind, NumField, Field(i).Tag
       │
       └──► reflect.Value ─────────────  Kind, Interface(), Field(i)
                 │
                 ├── not addressable ──  read-only (passed by value)
                 │
                 └── addressable ───────  pass pointer + Elem()
                           │
                           └── CanSet() true → Set / SetInt / SetString
                                     │
                                     ▼
                           Law 3: modification through reflect

Struct tags:  reflect.StructField.Tag.Get("json") / .Lookup("json")
       │
       └──► encoding/json, database/sql mappers, ORMs — all use this

Runtime reflection cost is real: 3–10× slower than direct calls
       │
       └──► compile-time alternative: go generate + stringer / mockgen / sqlc
```

The central insight is that reflection is the runtime counterpart to compile-time type information. Everything the compiler knows statically, you can ask at runtime via `reflect` — but at the cost of type safety and performance. Generics ([[go/10. Generics]]) and interfaces ([[go/6. Methods and Interfaces]]) are the compile-time tools that make reflection unnecessary for most cases.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Trying to set a value obtained from a non-pointer**
>
> Calling `Set` or `SetInt` on a `reflect.Value` obtained from a plain value (not a pointer) panics with "reflect: reflect.Value.SetInt using value obtained using unexported field" or "reflect.Value.Set using unaddressable value".
>
> **Wrong:**
> ```go
> x := 42
> v := reflect.ValueOf(x)
> v.SetInt(100) // PANIC: reflect.Value.SetInt using unaddressable value
> ```
>
> **Right:**
> ```go
> x := 42
> v := reflect.ValueOf(&x).Elem() // pointer, then Elem
> v.SetInt(100)
> fmt.Println(x) // 100
> ```
>
> **Why this matters:** The panic only appears at runtime, not at compile time — you can ship this bug to production.

> [!WARNING]
> **Mistake 2: Calling Set on an unexported field**
>
> Even with a properly addressable value, `Set` on an unexported field panics: "reflect.Value.SetInt using value obtained using unexported field". Always call `CanSet()` before `Set`.
>
> **Wrong:**
> ```go
> type T struct{ x int } // unexported
> val := T{x: 5}
> reflect.ValueOf(&val).Elem().FieldByName("x").SetInt(10) // PANIC
> ```
>
> **Right:**
> ```go
> f := reflect.ValueOf(&val).Elem().FieldByName("x")
> if f.CanSet() {
>     f.SetInt(10)
> }
> // silently skips unexported field — no panic
> ```

> [!WARNING]
> **Mistake 3: Switching on Type instead of Kind for generic handlers**
>
> If you write a generic handler that switches on `reflect.Type` (using `==` comparisons), it will not match user-defined types with the same underlying type.
>
> **Wrong:**
> ```go
> if v.Type() == reflect.TypeOf(int(0)) { ... } // misses type Celsius int
> ```
>
> **Right:**
> ```go
> switch v.Kind() {
> case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
>     // handles int, int8, int16, int32, int64, AND all named types with int kind
> }
> ```

**Other pitfalls:**

- **Forgetting to handle pointer-to-struct** — many functions receive `interface{}` that may be either `T` or `*T`; always check `v.Kind() == reflect.Pointer` and call `v.Elem()` to normalize
- **Reflection across package boundaries for unexported fields** — `reflect` respects Go's export rules; unexported fields are not accessible from outside the package; this is intentional and correct
- **Overusing reflection for things generics solve** — since Go 1.18, writing `func Map[T any](s []T, f func(T) T) []T` is better than a reflection-based mapper in almost every case; see [[go/10. Generics]]

---

## Mental Models

The right mental model makes this module click. Here are the most useful ways to think about it:

### Mental Model 1: The X-ray Machine

Think of `reflect.ValueOf` as an X-ray machine. You hand it any opaque box (an `interface{}`), and it produces an image (a `reflect.Value`) that reveals the internal structure — the fields, their types, their current values. The X-ray image is not the original box; it is a picture of it. Reading from the picture is fine. Modifying the original requires going back through the original pointer, not editing the picture.

This model explains addressability intuitively: an X-ray of a copy cannot change the original. To change the original, you need to hand the machine the original itself (a pointer), get an X-ray, and then write back through the pointer.

This model breaks down when thinking about `Call` — calling a method via reflection does execute on the real value, not a copy.

### Mental Model 2: Struct Tags as Metadata Annotations

Think of struct tags as a lightweight annotation system, similar to Java annotations or Python decorators, but evaluated at runtime via `reflect.StructField.Tag.Get()`. The struct is the schema; the tags are its documentation for downstream consumers.

Every package that reads struct tags is effectively implementing a small language. `encoding/json` implements JSON field naming, omitempty, and skip. `database/sql` mappers implement column aliasing. Your own code can implement whatever mapping rules you need. The `reflect.StructTag.Get(key)` API is the universal accessor for all of them.

This is most useful when you are debugging unexpected JSON output: find the struct, find the tag, check whether it says `omitempty` or `"-"`. The tag is the contract between your struct definition and the marshaler.

### Mental Model 3: Reflection as the Runtime Compiler

The Go compiler processes your source code at build time and generates type-checked machine code. Reflection is what you use when you need that same type information at runtime — when the types are not known when you write the code. A JSON marshaler cannot know your specific struct layout at compile time; it must discover it at runtime.

But runtime always costs more than compile time. Every reflection call that the Go compiler could have resolved statically is now resolved dynamically. This is why `go generate` + code generation tools exist: they run a compiler-like analysis at build time and produce static Go code, giving you the flexibility of reflection with the speed of compiled code.

Use this model when deciding reflection vs. generics vs. `go generate`: if the types are constrained and expressible as type parameters, use generics; if the types are truly arbitrary and only known at runtime, use reflection; if the types are known but numerous and writing the code manually is tedious, use `go generate`.

> [!NOTE]
> No single mental model is perfect. Use Model 1 (X-ray machine) when reasoning about addressability and why you need `Elem()`. Use Model 2 (metadata annotations) when working with struct tags and serializers. Use Model 3 (runtime compiler) when choosing between reflection, generics, and code generation.

---

## Practical Examples

### Example 1: Printing Any Struct's Fields _(Basic)_

**Scenario:** A debugging utility that prints every exported field of any struct, regardless of its type.

**Goal:** Demonstrate `reflect.TypeOf`, `reflect.ValueOf`, struct field iteration, and the Kind check.

```go
package main

import (
    "fmt"
    "reflect"
)

// PrintFields prints every exported field name and value of any struct.
func PrintFields(v interface{}) {
    rv := reflect.ValueOf(v)
    rt := reflect.TypeOf(v)

    // Dereference pointer if needed
    if rv.Kind() == reflect.Pointer {
        rv = rv.Elem()
        rt = rt.Elem()
    }

    if rv.Kind() != reflect.Struct {
        fmt.Println("(not a struct)")
        return
    }

    for i := 0; i < rt.NumField(); i++ {
        field := rt.Field(i)
        value := rv.Field(i)

        // PkgPath is empty for exported fields
        if !field.IsExported() {
            continue
        }
        fmt.Printf("  %-12s (%s) = %v\n", field.Name, field.Type, value)
    }
}

type Server struct {
    Host    string
    Port    int
    TLS     bool
    secret  string // unexported — skipped
}

func main() {
    s := Server{Host: "localhost", Port: 8080, TLS: true, secret: "abc"}
    fmt.Println("Server fields:")
    PrintFields(s)
    // Output:
    // Server fields:
    //   Host         (string) = localhost
    //   Port         (int) = 8080
    //   TLS          (bool) = true
}
```

**What to notice:** `field.IsExported()` (Go 1.17+) replaces the older `field.PkgPath == ""` idiom. The function handles both `T` and `*T` inputs by normalizing the pointer. Unexported fields (`secret`) are silently skipped — they are visible to `NumField` but not accessible for reading via `Interface()`.

---

### Example 2: A Struct-to-Map Serializer with Tag Support _(Intermediate)_

**Scenario:** A minimal serializer that converts any struct to `map[string]interface{}`, respecting `json` struct tags for key names, and honoring the `omitempty` option.

**Goal:** Demonstrate struct tag reading, `Tag.Get`, option parsing, and zero-value detection — the same core logic `encoding/json` uses internally.

```go
package main

import (
    "fmt"
    "reflect"
    "strings"
)

// StructToMap converts a struct to map[string]interface{},
// using the `json` struct tag for key names.
// Fields tagged `json:"-"` are omitted.
// Fields tagged with `omitempty` are omitted if zero.
func StructToMap(v interface{}) map[string]interface{} {
    rv := reflect.ValueOf(v)
    rt := reflect.TypeOf(v)
    if rv.Kind() == reflect.Pointer {
        rv, rt = rv.Elem(), rt.Elem()
    }
    if rv.Kind() != reflect.Struct {
        return nil
    }

    result := make(map[string]interface{})
    for i := 0; i < rt.NumField(); i++ {
        field := rt.Field(i)
        val := rv.Field(i)

        if !field.IsExported() {
            continue
        }

        // Parse the json tag
        tag := field.Tag.Get("json")
        if tag == "-" {
            continue // explicitly excluded
        }

        name := field.Name // default key is field name
        omitempty := false

        if tag != "" {
            parts := strings.SplitN(tag, ",", 2)
            if parts[0] != "" {
                name = parts[0]
            }
            if len(parts) > 1 && parts[1] == "omitempty" {
                omitempty = true
            }
        }

        // omitempty: skip zero values
        if omitempty && val.IsZero() {
            continue
        }

        result[name] = val.Interface()
    }
    return result
}

type Article struct {
    ID      int    `json:"id"`
    Title   string `json:"title"`
    Draft   bool   `json:"draft,omitempty"`  // omitted when false
    Secret  string `json:"-"`                // always omitted
    Author  string // no tag — uses field name
}

func main() {
    a := Article{ID: 1, Title: "Hello", Author: "Alice", Secret: "x"}
    m := StructToMap(a)
    for k, v := range m {
        fmt.Printf("  %q: %v\n", k, v)
    }
    // Output (map order varies):
    //   "id": 1
    //   "title": Hello
    //   "Author": Alice
    // (draft omitted — zero bool; Secret omitted — tagged "-")
}
```

**What to notice:** `strings.SplitN(tag, ",", 2)` is the minimal tag parser. `val.IsZero()` (Go 1.13+) checks whether the value equals its type's zero value — the same logic `encoding/json` uses for `omitempty`. The map key defaults to the field name when no tag is present, matching `encoding/json` behavior exactly.

---

### Example 3: Using go generate with stringer _(Applied)_

**Scenario:** An application defines a `Status` type for HTTP-like response codes. Without `go generate`, printing a `Status` value gives a useless integer. With `stringer`, it gives a readable name.

**Goal:** Show the `//go:generate` directive, the workflow, and the result — demonstrating code generation as a compile-time alternative to reflection.

```go
// file: status.go

//go:generate stringer -type=Status -output=status_string.go

package main

import "fmt"

// Status represents an operation result code.
type Status int

const (
    StatusOK      Status = iota // 0
    StatusPending               // 1
    StatusFailed                // 2
    StatusTimeout               // 3
)

func main() {
    s := StatusPending
    fmt.Println(s)        // Before generation: prints "1"
                          // After generation: prints "StatusPending"
    fmt.Println(s == StatusPending) // true
}
```

After running `go generate ./...` (which requires `stringer` to be installed: `go install golang.org/x/tools/cmd/stringer@latest`), the tool produces:

```go
// file: status_string.go — Code generated by stringer; DO NOT EDIT.

package main

import "strconv"

func _() {
    // Compile-time check: this assignment fails if constants are changed
    var x [1]struct{}
    _ = x[StatusOK-0]
    _ = x[StatusPending-1]
    _ = x[StatusFailed-2]
    _ = x[StatusTimeout-3]
}

const _Status_name = "StatusOKStatusPendingStatusFailedStatusTimeout"

var _Status_index = [...]uint8{0, 8, 21, 33, 46}

func (i Status) String() string {
    if i < 0 || i >= Status(len(_Status_index)-1) {
        return "Status(" + strconv.FormatInt(int64(i), 10) + ")"
    }
    return _Status_name[_Status_index[i]:_Status_index[i+1]]
}
```

**What to notice:** The generated `String()` method uses a precomputed string and index table — O(1) lookup, zero allocations, no reflection. The compile-time check (`var x [1]struct{}; _ = x[StatusOK-0]`) ensures the file is regenerated if the constants change. This is the pattern you want on hot paths where a reflection-based stringer would be measurably slower.

---

### Example 4: The Reflection Cost Reality Check _(Edge Case)_

**Scenario:** Comparing the performance of a direct field access, a reflection-based field access, and a generated accessor — showing concretely why reflection should be used sparingly on hot paths.

```go
package main

import (
    "fmt"
    "reflect"
    "time"
)

type Point struct{ X, Y float64 }

func directAccess(p *Point) float64 { return p.X }

func reflectAccess(p *Point) float64 {
    return reflect.ValueOf(p).Elem().FieldByName("X").Float()
}

func main() {
    p := &Point{X: 3.14, Y: 2.71}
    N := 1_000_000

    // Direct access
    start := time.Now()
    for i := 0; i < N; i++ {
        _ = directAccess(p)
    }
    fmt.Printf("Direct:  %v for %d iterations\n", time.Since(start), N)

    // Reflection-based access
    start = time.Now()
    for i := 0; i < N; i++ {
        _ = reflectAccess(p)
    }
    fmt.Printf("Reflect: %v for %d iterations\n", time.Since(start), N)

    // Typical results on modern hardware:
    // Direct:  ~2ms  (≈ 2ns/op)
    // Reflect: ~30ms (≈ 30ns/op) — 10–15x slower
}
```

**Why this is important:** The 10–15× slowdown is real and consistent. For one-off operations (marshaling a struct once per HTTP request), it is rarely a bottleneck. For hot-path operations (processing millions of records per second, inner loops), it matters. The rule of thumb: use reflection freely in initialization code and framework internals; avoid it in per-call hot paths. `go generate` and generics are the escape hatches. See [[go/16. Performance and Profiling]] for how to measure this precisely with `go test -bench`.

---

## Related Concepts

Within this topic:

- [[go/6. Methods and Interfaces]] — reflection operates on interface values; type assertions and type switches are the static equivalents of `reflect.TypeOf` and kind-switching; choosing between a type switch and reflection is a recurring design decision
- [[go/4. Composite Types]] — struct declarations with field tags are the primary target of reflection in practice; understanding struct embedding and anonymous fields matters when iterating fields with `NumField`/`Field(i)` (embedded fields appear as promoted fields)
- [[go/10. Generics]] — type parameters are the compile-time alternative to reflection for type-parameterized code; when you find yourself using `reflect` to handle "any type that supports X", ask whether a type constraint would work instead
- [[go/16. Performance and Profiling]] — quantifying the actual overhead of your reflection code with `pprof` and benchmarks; the Performance module explains the tools for measuring whether reflection is actually your bottleneck

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Read Type and Kind** _(Easy)_
>
> Write a function `typeInfo(v interface{})` that prints the `reflect.Type` name and `reflect.Kind` of any value passed to it. Call it with at least five values of different kinds: an `int`, a `string`, a `struct`, a slice, and a map.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-read-type-and-kind--easy--1-pt)

The exercises progress from basic type inspection through struct tag reading, a struct-to-map serializer, and a `go:generate` task. Complete at least the Easy and Medium exercises before taking the test.

---

## Test

When you feel ready, take the self-assessment: [TEST.md](./TEST.md)

**Test overview:**
- Section 1: Recall (5 questions, 1 pt each)
- Section 2: Conceptual Understanding (3 questions, 2 pts each)
- Section 3: Applied / Practical (2 questions, 3 pts each)
- Section 4: Scenario / Debugging (1 question, 3 pts)
- Section 5: Discussion (1 question, 2 pts)
- Section 6: Bonus Challenge (1 question, 5 pts bonus)

**Passing:** ≥ 70% of non-bonus points (≥ 15/22). Aim for ≥ 80% (≥ 18/22).

---

## Projects

See the topic-level [PROJECTS.md](../PROJECTS.md) for project ideas.

**Recommended project after this module:**
Config Loader — write a function `LoadConfig(path string, cfg interface{})` that reads a YAML or JSON file and populates a struct passed by pointer, using reflection to map file keys to struct fields via `json` or `yaml` struct tags. This requires struct tag reading, settability, type coercion across kinds, and robust error handling for mismatched types — a real-world reflection task.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[The Laws of Reflection — The Go Blog](https://go.dev/blog/laws-of-reflection)** — Rob Pike's canonical post (2011) explaining the three laws with running examples; still the single best introduction; read before anything else in this module
2. **[pkg.go.dev/reflect](https://pkg.go.dev/reflect)** — The complete `reflect` package API reference; the Overview section is worth reading in full; use the function list as a reference when writing reflection code
3. **[Generating code — The Go Blog](https://go.dev/blog/generate)** — Rob Pike's post on `go generate` (2014): motivation, the `//go:generate` directive, and how tools like `stringer` integrate; essential reading before the `go generate` exercise
4. **"The Go Programming Language" — Donovan & Kernighan, Chapter 12** — The most thorough treatment of reflection in any Go book; covers the display, encoding, and format examples that demonstrate both the power and the danger of reflection in real programs

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 15

**What I covered today:**
- Read the Overview and Why This Matters sections
- Worked through Core Concepts up to (concept name here)

**What clicked:**
- _Something that made sense_

**What's still unclear:**
- _Something that's still fuzzy — add to QUESTIONS.md_

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

**Test score:** _Not taken yet_

---

_Add new entries above this line._
