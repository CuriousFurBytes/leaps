# Module 6: Methods and Interfaces

[← Module 5: Pointers](../5.%20Pointers/) | [Topic Home](../README.md) | [Module 7: Packages and Modules →](../7.%20Packages%20and%20Modules/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-blue)
![Time](https://img.shields.io/badge/time-5--7h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Methods — Declaring Receivers](#methods--declaring-receivers)
  - [Value vs Pointer Receivers and Method Sets](#value-vs-pointer-receivers-and-method-sets)
  - [Interface Declaration and Implicit Satisfaction](#interface-declaration-and-implicit-satisfaction)
  - [Interface Values — Dynamic Type and Dynamic Value](#interface-values--dynamic-type-and-dynamic-value)
  - [The Nil Interface Gotcha — Typed Nil](#the-nil-interface-gotcha--typed-nil)
  - [The Empty Interface and any](#the-empty-interface-and-any)
  - [Type Assertions and Type Switches](#type-assertions-and-type-switches)
  - [Interface Embedding and Composition](#interface-embedding-and-composition)
  - [Important Standard Interfaces](#important-standard-interfaces)
  - [Interface Design Guidance](#interface-design-guidance)
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

This module covers **Go's method and interface system** — the primary mechanisms for abstraction and polymorphism in Go. Unlike class-based languages, Go has no inheritance. Instead, it uses two orthogonal tools: **methods** (functions with a named receiver) and **interfaces** (implicitly satisfied contracts defined by method sets).

By the end of this module, you will have a deep understanding of how Go achieves polymorphism without inheritance, why interfaces in Go are satisfied implicitly rather than declared, and how the method set rules interact with pointer and value receivers. This is the conceptual core of idiomatic Go design — understanding it well separates programmers who write Go from programmers who write idiomatic Go.

**Difficulty:** Intermediate &nbsp;|&nbsp; **Estimated time:** 5–7 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Declare methods with both value and pointer receivers on any named local type — _given a struct, add both a value receiver method and a pointer receiver method and explain the difference_
2. Explain method sets and how they determine interface satisfaction for `T` vs `*T` — _read code using a pointer receiver and predict whether a value of type `T` satisfies an interface_
3. Declare interfaces and explain implicit structural satisfaction — _create an interface and satisfy it from two unrelated packages without modifying either package_
4. Explain the internal representation of an interface value as a `(type, value)` pair and describe the typed-nil gotcha — _write a function that returns `nil` incorrectly as an interface and identify the bug_
5. Use type assertions (with comma-ok), type switches, and interface embedding — _write a function that handles `io.Reader`, `io.Writer`, and `io.ReadWriter` using a type switch_
6. Apply the "accept interfaces, return structs" principle and define small, consumer-side interfaces — _critique a design that passes a large interface and refactor it to pass a small interface_

---

## Prerequisites

### Required Modules

- [[go/5. Pointers]] — you need to understand: the difference between a pointer `*T` and a value `T`; how `&` and `*` work; when modifications via a pointer are visible to the caller — pointer receivers only make sense if you understand what a pointer is
- [[go/4. Composite Types]] — you need to understand: struct declaration, field access, and how struct values are copied vs referenced — most method examples use structs as receivers
- [[go/3. Functions]] — you need to understand: function signatures, multiple return values, and the concept of a function as a value — methods are syntactic sugar over functions with a receiver parameter

### Required Concepts

- **Pointer vs value semantics** — whether a method call can mutate the receiver depends entirely on whether the receiver is a pointer; this is Module 5's core lesson applied in a new context
- **Struct types** — virtually all real-world method definitions use structs as the receiver type; you need to be comfortable declaring structs with fields before adding methods to them
- **Function signatures and calling conventions** — a method `func (t T) M()` is equivalent to a function `func M(t T)`; understanding function parameter passing makes receiver semantics clear

> [!TIP]
> If pointer semantics feel shaky, spend 15–30 minutes reviewing [[go/5. Pointers]] before continuing.
> The most common confusion in this module — value vs pointer receiver — is simply Module 5 applied in a new context.

---

## Why This Matters

Methods and interfaces are Go's answer to the question "how do you write reusable, testable, extensible code without inheritance?" The answer turns out to be more powerful than inheritance for many use cases: structural typing lets you compose behaviors without coupling types.

Concretely, mastery of this module enables you to:

- **Write testable code** — by accepting interfaces rather than concrete types, functions become testable with fake implementations; the standard library's `io.Reader` interface is why you can test file-reading code without touching the filesystem
- **Implement the standard library's protocols** — `sort.Interface`, `fmt.Stringer`, `error`, `io.Reader`, and `io.Writer` are how the standard library achieves its flexibility; understanding how to implement them opens the entire standard library to you
- **Design extensible APIs** — returning a concrete struct but accepting an interface means your API is stable (callers get a full-featured concrete value) while remaining flexible (callers can pass mock/alternate implementations to functions)

Without understanding methods and interfaces, you cannot implement `error` (covered in [[go/8. Error Handling]]), use `sort.Sort`, plug custom types into `fmt.Printf` via `Stringer`, or write the kind of layered, composable code that makes Go programs maintainable at scale.

---

## Historical Context

Go's interface system was designed by **Rob Pike, Robert Griesemer, and Ken Thompson** as part of Go's original design (2007–2009). The most significant influence was the experience with **Java's explicit `implements` declarations** — the Go designers found that requiring types to explicitly declare which interfaces they implement creates tight coupling between packages and makes the language feel bureaucratic.

The key insight was that interfaces in Go should be **implicitly satisfied by structural compatibility** (duck typing with compile-time checking). A type satisfies an interface if it has the required methods — no declaration needed. This was directly influenced by Rob Pike's experience with Newsqueak and Limbo, which had similar ideas.

Key moments in the development of Go's interface model:

- **2007** — Initial design; Rob Pike argues for implicit interface satisfaction. The separation of "method set" from "type declaration" is established early
- **2009** — Go's open-source release; interfaces are already present with their current semantics. The empty interface `interface{}` is available from day one
- **2011** — Go Blog post "Laws of Reflection" (Rob Pike) clarifies how interface values work internally; the `(type, value)` pair model becomes canonical
- **2022** — Go 1.18 introduces generics, which builds on interfaces (constraints are interfaces); the `any` keyword is introduced as an alias for `interface{}`

Understanding the history explains a core Go decision: the absence of `implements`. When you declare a Java class `class Foo implements Serializable`, you are coupling `Foo` to `Serializable` at the definition site. In Go, that coupling happens at the call site — whoever needs a `Stringer` defines `Stringer`, and `Foo` satisfies it automatically if it has the right methods. This reversal is the foundation of Go's composability.

---

## Core Concepts

### Methods — Declaring Receivers

A **method** is a function with a special first parameter called the **receiver**. The receiver is declared between the `func` keyword and the method name, in parentheses. This is the only syntactic difference between a method and a function:

```go
// This is a regular function
func areaFunc(r Rectangle) float64 {
    return r.Width * r.Height
}

// This is the same logic as a method — r is the receiver
type Rectangle struct {
    Width, Height float64
}

func (r Rectangle) Area() float64 { // value receiver
    return r.Width * r.Height
}
```

The receiver type must be a **named type defined in the same package**. You cannot add methods to a type from another package (including built-in types). To add methods to `int`, you must define a new named type:

```go
// Cannot: func (i int) Double() int { ... }  — int is not local

type Celsius float64 // named type in this package

func (c Celsius) ToFahrenheit() float64 {
    return float64(c)*9/5 + 32
}

// Methods can be on any named type — not just structs
type StringSlice []string

func (s StringSlice) Contains(target string) bool {
    for _, v := range s {
        if v == target {
            return true
        }
    }
    return false
}
```

**A method is just a function with a receiver.** You can always call a method as a function by promoting the receiver to the first argument:

```go
r := Rectangle{Width: 3, Height: 4}

// Method call syntax
fmt.Println(r.Area()) // 12

// Equivalent function call (method expression)
fmt.Println(Rectangle.Area(r)) // 12 — receiver becomes first argument
```

---

### Value vs Pointer Receivers and Method Sets

The choice between a value receiver `(t T)` and a pointer receiver `(t *T)` has concrete consequences for mutability and interface satisfaction.

**Value receiver** — the method receives a copy of the receiver. Modifications to the copy do not affect the original:

```go
type Counter struct{ n int }

func (c Counter) Value() int { return c.n }      // value receiver: reads only

func (c Counter) Broken() {
    c.n++  // modifies a copy — caller's Counter is unchanged
}
```

**Pointer receiver** — the method receives a pointer to the original. Modifications are visible to the caller:

```go
func (c *Counter) Increment() { c.n++ }  // pointer receiver: modifies original

c := Counter{}
c.Increment()
fmt.Println(c.Value()) // 1 — the original was modified
```

Go provides **automatic address-taking and dereferencing** for method calls: if `c` is an addressable value of type `Counter`, then `c.Increment()` is automatically rewritten to `(&c).Increment()` by the compiler. This is syntactic convenience, not a deep semantic equivalence.

**Method sets** govern which methods a type possesses for purposes of **interface satisfaction**:

| Type | Methods in its method set |
|------|--------------------------|
| `T` | All methods with value receiver `(t T)` |
| `*T` | All methods with value receiver `(t T)` **plus** all methods with pointer receiver `(t *T)` |

The asymmetry is intentional and important:

- A `*T` can call value-receiver methods because the compiler can dereference the pointer to get the value.
- A `T` **cannot** call pointer-receiver methods via an interface, because the compiler cannot reliably take the address of the value stored in an interface (it may not be addressable).

```go
type Stringer interface {
    String() string
}

type Point struct{ X, Y int }

func (p *Point) String() string {    // pointer receiver
    return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

var s Stringer

p := Point{1, 2}
s = &p  // OK: *Point has String() in its method set
// s = p  // compile error: Point does not implement Stringer (String method has pointer receiver)
```

**Guideline:** Use a pointer receiver when:
1. The method needs to mutate the receiver, OR
2. The receiver is large and copying is expensive, OR
3. **Any** other method on the type uses a pointer receiver — keep all receivers consistent to avoid method-set confusion.

Use a value receiver when the method is a pure read that needs no mutation and copying is cheap (e.g., small structs or scalars).

---

### Interface Declaration and Implicit Satisfaction

An **interface** is a named collection of method signatures. Any type that has all those methods — with matching signatures — **automatically satisfies** the interface, without any declaration:

```go
// Declare the interface in your package
type Shape interface {
    Area() float64
    Perimeter() float64
}

// Satisfy it implicitly — no "implements Shape" keyword
type Circle struct{ Radius float64 }

func (c Circle) Area() float64      { return math.Pi * c.Radius * c.Radius }
func (c Circle) Perimeter() float64 { return 2 * math.Pi * c.Radius }

// Also satisfies Shape — Circle and Rectangle are in completely separate files/packages
type Rectangle struct{ Width, Height float64 }

func (r Rectangle) Area() float64      { return r.Width * r.Height }
func (r Rectangle) Perimeter() float64 { return 2 * (r.Width + r.Height) }

func printShape(s Shape) {
    fmt.Printf("area=%.2f  perimeter=%.2f\n", s.Area(), s.Perimeter())
}

func main() {
    printShape(Circle{Radius: 5})
    printShape(Rectangle{Width: 3, Height: 4})
    // Both work — no explicit "implements" needed
}
```

The implicit satisfaction model means **interfaces can be defined after the types that satisfy them**. A package that ships `Circle` does not need to know that `printShape` exists. The coupling happens at the call site, not at the type definition site.

To verify that a type satisfies an interface at compile time (useful as documentation), use a blank-identifier assignment:

```go
var _ Shape = Circle{}   // compile error if Circle doesn't implement Shape
var _ Shape = (*Circle)(nil) // checks *Circle satisfies Shape
```

---

### Interface Values — Dynamic Type and Dynamic Value

An interface variable is not a simple pointer. It is internally a **two-word pair**:

1. **Dynamic type** — a pointer to the runtime type descriptor of the concrete value currently stored
2. **Dynamic value** — a pointer to the concrete value itself (or the value directly for small types)

```
  interface value
  ┌──────────────┐
  │  type ptr    │  ──►  *runtime type descriptor for, e.g., *os.File
  ├──────────────┤
  │  value ptr   │  ──►  the concrete *os.File value
  └──────────────┘
```

Understanding this internal model explains several behaviors:

```go
var r io.Reader  // r == nil: both type and value are nil

f, _ := os.Open("/etc/hosts")
r = f            // r: (type=*os.File, value=f)

// Comparing interface values compares BOTH type and value
var r2 io.Reader = f
fmt.Println(r == r2) // true: same type, same pointer value

// Interface values of different concrete types are never equal
var w io.Writer = os.Stdout
// r == w  // compile error: different interface types
```

---

### The Nil Interface Gotcha — Typed Nil

One of Go's most famous bugs: a **non-nil interface holding a nil concrete pointer is not equal to nil**.

When you store a typed nil pointer into an interface variable, the interface's type field is set (it points to the concrete type's descriptor), but the value field is nil. The interface itself is **not** nil — it has a type.

```go
// BUG: this function returns a non-nil error even when err is nil
func buggyOpen(path string) error {
    var f *os.File  // f is nil — a typed nil pointer
    // ... some logic that sets f when successful ...
    return f        // WRONG: returns (*os.File)(nil) stored in error interface
    // The returned error != nil because its type field is set to *os.File
}

// CORRECT: return the untyped nil directly
func correctOpen(path string) error {
    var err *MyError = nil
    if someCondition {
        return nil   // untyped nil: both type and value fields are nil — error == nil
    }
    return err       // typed nil: error != nil — the bug
}
```

The rule: **never store a typed nil in an interface when you mean to signal absence**. Return the untyped `nil` literal directly, or use a concrete type for the return value.

```go
// Safe pattern: return untyped nil when there is no error
func doWork() error {
    if failed {
        return &MyError{msg: "something went wrong"}
    }
    return nil  // untyped nil — caller's err != nil check works correctly
}
```

---

### The Empty Interface and any

The **empty interface** `interface{}` has no methods. Every type satisfies it — it is Go's mechanism for holding a value of any type:

```go
var x interface{}

x = 42
x = "hello"
x = []int{1, 2, 3}
x = nil
```

Since Go 1.18, `any` is a built-in **alias** for `interface{}`. They are identical; `any` is preferred in new code for readability:

```go
func printAnything(v any) {
    fmt.Printf("type=%T  value=%v\n", v, v)
}
```

The empty interface is used in:
- Functions that must accept arbitrary values: `fmt.Println(a ...any)`
- Generic containers before generics existed: `map[string]any` for JSON
- Reflection-based code

**Guidance:** Avoid `any` when you know the concrete type at design time. A function that takes `any` gives up compile-time type checking. Prefer a concrete type or a specific interface. Use `any` when you genuinely need to handle arbitrary types (serialization, logging, testing utilities).

---

### Type Assertions and Type Switches

When you hold an interface value and need the concrete type back, use a **type assertion**:

```go
var r io.Reader = os.Stdin

// Single-return form: panics if r doesn't hold *os.File
f := r.(*os.File)

// Comma-ok form: never panics — ok is false if the assertion fails
f, ok := r.(*os.File)
if ok {
    fmt.Println("it's a file:", f.Name())
} else {
    fmt.Println("not a *os.File")
}
```

When dispatching on multiple concrete types, a **type switch** is cleaner:

```go
func describe(v any) string {
    switch t := v.(type) {
    case nil:
        return "nil"
    case int:
        return fmt.Sprintf("int(%d)", t)       // t is typed as int here
    case string:
        return fmt.Sprintf("string(%q)", t)    // t is typed as string here
    case bool:
        return fmt.Sprintf("bool(%v)", t)
    case fmt.Stringer:
        return fmt.Sprintf("Stringer: %s", t.String()) // t satisfies Stringer
    default:
        return fmt.Sprintf("unknown(%T)", t)
    }
}
```

Note in the type switch: the cases are checked in order. A case can be an interface type (like `fmt.Stringer`), not just a concrete type. When a case is an interface type, `t` is that interface type within the case body.

**Use type assertions sparingly.** Frequent type assertions are often a sign that you should be using a type switch or that the interface is not the right abstraction. If you find yourself asserting on many concrete types, consider whether adding a method to the interface would be cleaner.

---

### Interface Embedding and Composition

Interfaces can embed other interfaces, composing their method sets:

```go
// io package defines:
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// io.ReadWriter is the composition of both:
type ReadWriter interface {
    Reader  // embed: includes Read method
    Writer  // embed: includes Write method
}

// A type that implements both Read and Write automatically satisfies ReadWriter
```

This is Go's primary composition mechanism. Rather than deep inheritance hierarchies, you compose behaviors from small, focused interfaces. `os.File` implements `io.Reader`, `io.Writer`, `io.Closer`, and several other interfaces — all implicitly, just by having the right methods.

Embedding works for struct types too, but interface embedding is purely method-set composition — there is no field inheritance.

```go
// A more complete example from the standard library:
type ReadWriteCloser interface {
    Reader
    Writer
    io.Closer  // Close() error
}
```

---

### Important Standard Interfaces

These interfaces appear throughout the standard library and idiomatic Go code. Implementing them hooks your types into the language's infrastructure:

**`fmt.Stringer`** — controls how a value prints in `fmt.Printf("%v", ...)` and friends:
```go
type Stringer interface {
    String() string
}

type Point struct{ X, Y int }

func (p Point) String() string {
    return fmt.Sprintf("Point(%d, %d)", p.X, p.Y)
}

fmt.Println(Point{3, 4})  // Output: Point(3, 4)
```

**`error`** — the built-in error interface (covered in depth in [[go/8. Error Handling]]):
```go
type error interface {
    Error() string
}

type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}
```

**`io.Reader` and `io.Writer`** — the most-used interfaces in the standard library:
```go
// io.Reader: read up to len(p) bytes into p, return bytes read and error
type Reader interface {
    Read(p []byte) (n int, err error)
}

// io.Writer: write len(p) bytes from p, return bytes written and error
type Writer interface {
    Write(p []byte) (n int, err error)
}

// These interfaces unify: os.File, bytes.Buffer, strings.Reader,
// net.Conn, http.Request.Body, gzip.Reader — all in one abstraction
func copyData(dst io.Writer, src io.Reader) error {
    _, err := io.Copy(dst, src)
    return err
}
```

**`sort.Interface`** — sort any collection by implementing three methods:
```go
type Interface interface {
    Len() int           // number of elements
    Less(i, j int) bool // true if element i should sort before element j
    Swap(i, j int)      // swap elements at positions i and j
}

type ByLength []string

func (s ByLength) Len() int           { return len(s) }
func (s ByLength) Less(i, j int) bool { return len(s[i]) < len(s[j]) }
func (s ByLength) Swap(i, j int)      { s[i], s[j] = s[j], s[i] }

// sort.Sort now works on ByLength
words := ByLength{"banana", "apple", "fig", "kiwi"}
sort.Sort(words)
fmt.Println(words) // [fig kiwi apple banana]
```

---

### Interface Design Guidance

The Go community has converged on several principles for interface design. These are not rules enforced by the compiler — they are judgments earned from large Go codebases.

**1. Accept interfaces, return structs.**

Functions should take the most general interface that satisfies their needs. Functions should return the most specific concrete type they produce. This gives callers maximum flexibility when calling (they can pass any compatible implementation) and maximum information when receiving (they get the full concrete type with all its methods):

```go
// Good: accept io.Writer (any writer), return *os.File (the specific type)
func openLog(path string) (*os.File, error) { ... }
func writeRecord(w io.Writer, record Record) error { ... }

// Poor: accepting a concrete type limits testability
func writeRecord(f *os.File, record Record) error { ... }
```

**2. Keep interfaces small — one to three methods.**

The Go standard library's most-used interfaces are all tiny: `error` (1 method), `io.Reader` (1 method), `io.Writer` (1 method), `fmt.Stringer` (1 method), `sort.Interface` (3 methods). Small interfaces are easier to implement, easier to mock, and compose cleanly. A 15-method interface is a smell — it forces implementors to provide 15 methods, drastically limiting what can satisfy it.

**3. Define interfaces at the consumer, not the producer.**

The package that needs a behavior defines the interface it needs. The package that provides the type does not need to know the interface exists:

```go
// storage package just defines the struct:
package storage
type FileStore struct { ... }
func (s *FileStore) Save(key, value string) error { ... }

// service package defines what it needs:
package service
type Storer interface {
    Save(key, value string) error
}
func NewService(store Storer) *Service { ... }
// FileStore satisfies Storer implicitly — no coupling between packages
```

**4. Avoid interface pollution — don't define an interface unless you need polymorphism.**

Creating an interface "just in case" adds indirection without benefit. If there is only one implementation and you don't need a mock for testing, use the concrete type. Interfaces are best introduced when you have two or more implementations, or when you need to decouple for testing.

---

### How the Concepts Fit Together

```
Named type (struct or otherwise)
        │
        │  add methods (value or pointer receivers)
        ▼
  Method set of T / *T
        │
        │  compared against interface's required methods
        ▼
  Implicit interface satisfaction
        │
        ├──────► Interface value = (dynamic type, dynamic value)
        │                │
        │                ├── nil interface: both fields nil
        │                └── typed nil: type set, value nil  ← the gotcha
        │
        ├──────► Type assertion  i.(T)  — extract concrete type
        ├──────► Type switch     switch v := i.(type)
        └──────► Interface embedding — compose larger interfaces from small ones
```

In practice, this system enables a layered architecture: concrete types (structs with fields) at the bottom, small behavioral interfaces in the middle, and functions accepting those interfaces at the top. Each layer depends only on the interface, not the concrete type, making the system easy to test and extend.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Pointer receiver method not in value type's method set**
>
> Programmers expect that because the compiler auto-dereferences `p.Method()` for addressable values, the same auto-addressing works everywhere — including when storing into an interface. It does not. Auto-addressing only applies to direct method calls on addressable variables; it does not apply when assigning to an interface.
>
> **Wrong:**
> ```go
> type Logger struct{ prefix string }
> func (l *Logger) Log(msg string) { fmt.Println(l.prefix, msg) }
>
> type Loggable interface{ Log(msg string) }
>
> var lg Loggable = Logger{"INFO"}  // compile error: Logger does not implement Loggable
>                                   // (Log method has pointer receiver)
> ```
>
> **Right:**
> ```go
> var lg Loggable = &Logger{"INFO"}  // *Logger implements Loggable — use a pointer
> ```
>
> **Why this matters:** The compiler can auto-take the address of an addressable local variable for a direct method call, but it cannot guarantee that an interface copy remains addressable. The method set of `T` never includes pointer-receiver methods; the method set of `*T` includes both. When satisfying an interface, use `*T` if any method has a pointer receiver.

> [!WARNING]
> **Mistake 2: Returning a typed nil in an interface return value**
>
> A function with return type `error` (or any interface) that returns a typed nil concrete pointer returns a non-nil interface. This is the most confusing bug in Go and affects even experienced programmers.
>
> **Wrong:**
> ```go
> type MyError struct{ msg string }
> func (e *MyError) Error() string { return e.msg }
>
> func check(ok bool) error {
>     var err *MyError  // nil pointer of concrete type *MyError
>     if !ok {
>         err = &MyError{"something failed"}
>     }
>     return err  // BUG: when ok==true, returns (*MyError)(nil) in an error interface
>                 // That interface value != nil, so caller's "if err != nil" is always true
> }
> ```
>
> **Right:**
> ```go
> func check(ok bool) error {
>     if !ok {
>         return &MyError{"something failed"}
>     }
>     return nil  // untyped nil: interface value has no type — correctly == nil
> }
> ```
>
> **Why this matters:** Every `if err != nil` check in Go relies on the error interface being a true nil (both type and value fields zero) to mean "no error". A typed nil breaks this contract silently.

> [!WARNING]
> **Mistake 3: Mixing value and pointer receivers on the same type**
>
> When some methods use value receivers and others use pointer receivers, the method sets of `T` and `*T` diverge in a way that surprises many programmers: a value of type `T` stored in an interface cannot call any pointer-receiver methods, even if the original variable was addressable.
>
> **Wrong (inconsistent receivers):**
> ```go
> type Config struct{ debug bool }
> func (c Config) IsDebug() bool  { return c.debug }       // value receiver
> func (c *Config) SetDebug(v bool) { c.debug = v }        // pointer receiver
>
> type Configurable interface {
>     IsDebug() bool
>     SetDebug(bool)
> }
>
> var cfg Configurable = Config{}   // compile error: Config.SetDebug has pointer receiver
> ```
>
> **Right (consistent pointer receivers when any method mutates):**
> ```go
> func (c *Config) IsDebug() bool   { return c.debug }     // pointer receiver
> func (c *Config) SetDebug(v bool) { c.debug = v }        // pointer receiver
>
> var cfg Configurable = &Config{}  // *Config implements Configurable
> ```

**Other pitfalls:**

- **Defining interfaces with too many methods** — a 10-method interface is hard to satisfy and hard to mock; split it into smaller interfaces and embed them where needed
- **Type-asserting without the comma-ok form** — `v := x.(SomeType)` panics if the assertion fails; always use `v, ok := x.(SomeType)` unless you are 100% certain of the type and want a panic to be a bug signal

---

## Mental Models

### Mental Model 1: Interface as a Protocol Contract

Think of a Go interface not as a class hierarchy but as a **protocol specification**. `io.Reader` is not "a thing you inherit from" — it is a protocol: "any participant in this protocol must be able to Read bytes into a buffer." Any type that speaks the protocol is a valid participant, regardless of its ancestry.

This is like USB: a USB cable doesn't care whether you plug it into a phone, a keyboard, or a hard drive. The protocol specifies the electrical and logical contract. The device satisfies it by conforming to the spec, not by inheriting from `USBDevice`. In Go, the interface specifies the method contract; the type satisfies it by having those methods.

This model breaks down when thinking about default implementations — interfaces in Go have none. There is no equivalent to Java's `default` methods. If you need shared behavior, use struct embedding, not interface default methods.

### Mental Model 2: Method Set as a Permission Table

Think of the method set rules as a **permission table**. The table has two rows (value and pointer) and one column per method:

| Receiver type | Value-receiver methods | Pointer-receiver methods |
|---------------|----------------------|------------------------|
| `T` value | YES | NO |
| `*T` pointer | YES (dereferences) | YES |

A type satisfies an interface only if it has permission to call all the interface's methods. A `T` value does not have permission to call pointer-receiver methods through an interface because the value stored in an interface may not be addressable (it could be a copy).

This model is most useful when you get a "does not implement" compile error: look up which method has a pointer receiver, and change the interface assignment to use a pointer.

### Mental Model 3: Interface Value as a Tagged Union

An interface value internally is a **tagged union**: a tag (the dynamic type) plus a payload (the dynamic value). A nil interface has both the tag and payload set to zero. A non-nil interface always has a tag set — even if the payload is a nil pointer (the typed-nil gotcha).

Think of it like an envelope: a nil interface is an empty envelope with no label. A typed-nil interface is an envelope with a label ("contents: `*os.File`") but an empty interior. An `if err != nil` check tests whether the envelope has a label — not whether the interior is empty.

> [!NOTE]
> Use Model 1 (protocol contract) when designing new interfaces and deciding whether a type should satisfy one. Use Model 2 (permission table) when debugging "does not implement" errors. Use Model 3 (tagged union) when reasoning about nil interface behavior and the typed-nil gotcha.

---

## Practical Examples

### Example 1: Implementing fmt.Stringer _(Basic)_

**Scenario:** A custom `Color` type that should print as a human-readable string.

**Goal:** Implement `fmt.Stringer` so that `fmt.Println` uses your custom format automatically.

```go
package main

import "fmt"

// Color is an RGBA color (each channel 0–255)
type Color struct {
    R, G, B uint8
}

// String satisfies fmt.Stringer — called automatically by fmt verbs
func (c Color) String() string {
    return fmt.Sprintf("#%02X%02X%02X", c.R, c.G, c.B)
}

func main() {
    red := Color{R: 255, G: 0, B: 0}
    teal := Color{R: 0, G: 128, B: 128}

    fmt.Println(red)             // #FF0000
    fmt.Println(teal)            // #008080
    fmt.Printf("color: %v\n", red)  // color: #FF0000
    fmt.Printf("color: %s\n", red)  // color: #FF0000

    // Works in any fmt context that calls String()
    colors := []Color{red, teal}
    fmt.Println(colors) // [#FF0000 #008080]
}
```

**Output:**
```
#FF0000
#008080
color: #FF0000
color: #FF0000
[#FF0000 #008080]
```

**What to notice:** `Color` never declares that it implements `fmt.Stringer`. The `fmt` package checks at runtime whether the value has a `String() string` method. If it does, it calls it. This is implicit satisfaction: the coupling is in `fmt`'s code, not in `Color`'s.

---

### Example 2: Sorting with sort.Interface _(Intermediate)_

**Scenario:** A slice of `Person` structs that needs to be sorted by age, then alphabetically by name as a tiebreaker.

**Goal:** Implement `sort.Interface` to demonstrate the three-method contract and show how any collection can be sorted without modifying the `sort` package.

```go
package main

import (
    "fmt"
    "sort"
)

type Person struct {
    Name string
    Age  int
}

// ByAgeThenName sorts Persons by age, with name as tiebreaker
type ByAgeThenName []Person

func (p ByAgeThenName) Len() int      { return len(p) }
func (p ByAgeThenName) Swap(i, j int) { p[i], p[j] = p[j], p[i] }
func (p ByAgeThenName) Less(i, j int) bool {
    if p[i].Age != p[j].Age {
        return p[i].Age < p[j].Age  // primary: sort by age
    }
    return p[i].Name < p[j].Name    // tiebreaker: sort by name
}

func main() {
    people := []Person{
        {"Charlie", 30},
        {"Alice", 25},
        {"Bob", 30},
        {"Dave", 25},
    }

    sort.Sort(ByAgeThenName(people))

    for _, p := range people {
        fmt.Printf("%-8s %d\n", p.Name, p.Age)
    }
}
```

**Output:**
```
Alice    25
Dave     25
Bob      30
Charlie  30
```

**What to notice:** `sort.Sort` accepts `sort.Interface`, which is satisfied by `ByAgeThenName`. The `sort` package knows nothing about `Person` — it only knows the three-method contract. This is how the standard library achieves generic sorting before Go had type parameters. Note: `sort.Slice` (available since Go 1.8) accepts a less function and is often more convenient; `sort.Interface` is worth knowing because it illustrates the interface pattern clearly.

---

### Example 3: Accept Interfaces, Return Structs _(Applied)_

**Scenario:** A logging system that writes structured records to any output — a file in production, a buffer in tests.

**Goal:** Demonstrate the "accept interfaces, return structs" principle and show how it enables painless testing.

```go
package main

import (
    "bytes"
    "fmt"
    "io"
    "os"
    "strings"
    "time"
)

// Logger accepts io.Writer — not *os.File, not bytes.Buffer
type Logger struct {
    out    io.Writer
    prefix string
}

func NewLogger(out io.Writer, prefix string) *Logger {
    return &Logger{out: out, prefix: prefix}
}

func (l *Logger) Log(msg string) {
    fmt.Fprintf(l.out, "[%s] %s: %s\n",
        time.Now().Format("15:04:05"), l.prefix, msg)
}

func main() {
    // Production: write to stderr
    prodLogger := NewLogger(os.Stderr, "PROD")
    prodLogger.Log("server started")

    // Test: capture into a buffer
    var buf bytes.Buffer
    testLogger := NewLogger(&buf, "TEST")
    testLogger.Log("processing request")
    testLogger.Log("request complete")

    // Inspect what was logged without touching stderr/stdout
    output := buf.String()
    if strings.Contains(output, "processing request") {
        fmt.Println("test passed: log captured correctly")
    }
}
```

**Output:**
```
[HH:MM:SS] PROD: server started
test passed: log captured correctly
```

**What to notice:** `NewLogger` returns `*Logger` (a concrete type — maximum information for the caller) but accepts `io.Writer` (an interface — maximum flexibility for the caller). The production code and test code use the exact same `Logger` type with different backing implementations. No mocking framework needed: `bytes.Buffer` already implements `io.Writer`.

---

### Example 4: The Typed-Nil Interface Bug _(Edge Case)_

**Scenario:** A function that conditionally creates an error — what happens when the condition is false?

```go
package main

import "fmt"

type QueryError struct {
    Query string
    Err   error
}

func (e *QueryError) Error() string {
    return fmt.Sprintf("query %q failed: %v", e.Query, e.Err)
}

// BUG: returns a non-nil error even on success
func runQueryBuggy(query string) error {
    var err *QueryError  // typed nil: *QueryError, value nil
    if query == "" {
        err = &QueryError{Query: query, Err: fmt.Errorf("empty query")}
    }
    return err  // when query != "", returns (*QueryError)(nil) — NOT nil interface
}

// CORRECT: return nil directly when there is no error
func runQueryCorrect(query string) error {
    if query == "" {
        return &QueryError{Query: query, Err: fmt.Errorf("empty query")}
    }
    return nil  // untyped nil — interface value is nil
}

func main() {
    // Buggy version
    err := runQueryBuggy("SELECT 1")
    fmt.Printf("buggy: err == nil? %v  (err = %v)\n", err == nil, err)
    // Prints: buggy: err == nil? false  (err = <nil>)
    // Despite "no error", err != nil — the if check would wrongly enter the error branch

    // Correct version
    err = runQueryCorrect("SELECT 1")
    fmt.Printf("correct: err == nil? %v\n", err == nil)
    // Prints: correct: err == nil? true
}
```

**Why this is important:** This bug is silent — the code compiles, the query runs correctly, but every caller that checks `if err != nil` sees an error that isn't there. The fix is simple (return `nil` directly) but finding the bug requires knowing the typed-nil rule. It appears most often in functions that conditionally construct an error value — the temptation is to declare `var err *MyError` at the top and return it at the bottom.

---

## Related Concepts

Within this topic:

- [[go/5. Pointers]] — pointer receivers, method sets, and interface satisfaction are all grounded in pointer semantics; this module applies Module 5's concepts in a new context
- [[go/8. Error Handling]] — `error` is an interface with one method; everything you learn about interfaces here applies directly to error handling, custom error types, and `errors.As`/`errors.Is`
- [[go/7. Packages and Modules]] — consumer-side interface definition (define interfaces where you use them) requires understanding package boundaries; visibility rules (`Error()` must be exported to satisfy `error`) are a package concern
- [[go/15. Reflection and Metaprogramming]] — reflection in Go works through interface values; `reflect.TypeOf` and `reflect.ValueOf` accept `any` (the empty interface); understanding the `(type, value)` pair model here is prerequisite to understanding reflection

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Implementing fmt.Stringer** _(Easy)_
>
> Define a `Temperature` type (a `float64`) with a `String()` method that prints in the format `"23.5°C"`. Verify that `fmt.Println` uses your String method automatically.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-implementing-fmtstringer--easy--1-pt)

The exercises range from a basic Stringer implementation to a full sort.Interface exercise and a challenge that requires designing a small domain interface and satisfying it with two independent types.

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
Shape Calculator — define a `Shape` interface with `Area()` and `Perimeter()` methods, implement it with at least three types (`Circle`, `Rectangle`, `Triangle`), write a function that prints a summary of a `[]Shape` slice, and implement `fmt.Stringer` on each type. This exercises implicit interface satisfaction, the value vs pointer receiver decision, and the `fmt.Stringer` standard interface all at once.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Effective Go — Interfaces and Methods](https://go.dev/doc/effective_go#interfaces_and_types)** — The authoritative style guide from the Go authors; covers embedding, the `Stringer` pattern, interface conversions, and the design philosophy of small interfaces; essential reading after completing this module
2. **[Go Language Specification — Interface types](https://go.dev/ref/spec#Interface_types)** — The formal definition of interface types, method sets, and the rules for what types satisfy an interface; the method-set rules (T vs *T) are specified precisely in the "Method sets" section
3. **[Go Blog — The Go Programming Language and Environment](https://go.dev/blog/laws-of-reflection)** (Laws of Reflection, Rob Pike) — Explains how interface values work as `(type, value)` pairs; foundational for understanding type assertions, the typed-nil gotcha, and reflection; the first three rules of reflection directly explain interface value mechanics
4. **"The Go Programming Language" — Donovan & Kernighan, Chapter 7** — The definitive book treatment of interfaces; covers interface satisfaction, interface values, the `error` interface, type assertions, and type switches with worked examples from the standard library
5. **"Learning Go" — Jon Bodner (2nd ed.), Chapter 7** — Modern treatment of interfaces with emphasis on idiomatic usage; the "accept interfaces, return concrete types" principle and interface pollution guidance are explained clearly with practical examples; covers `any` and the move away from `interface{}`

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 6

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
