# Exercises — Module 5: Pointers

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just run code mentally — actually write or type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Address-Of and Dereference Basics [🟢 Easy] [1 pt]

### Context
The foundation of pointers is two operators: `&` (take the address of a variable) and `*` (follow the address to read or write the value). This exercise confirms you can use both in a simple program before moving to more complex use cases.

### Task
Write a Go program that:
1. Declares an integer variable `n := 7`
2. Takes its address and stores it in `p`
3. Prints `p` (the address itself — a hex number) and `*p` (the value at the address)
4. Modifies `n` through the pointer: `*p = 42`
5. Prints `n` to confirm it changed (even though you wrote through `p`, not `n` directly)

### Requirements
- [ ] `p` is declared as a `*int` (either explicitly or via `:=` from `&n`)
- [ ] The program prints the pointer value (the address) and the dereferenced value
- [ ] The modification is done via `*p = 42`, not via `n = 42`
- [ ] The final print of `n` shows `42`, confirming the pointer write affected the original variable

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Use `p := &n` to get the pointer. `fmt.Println(p)` prints the address (a hex number like `0xc000014098`). `fmt.Println(*p)` prints the value at that address.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

To modify through the pointer: `*p = 42`. This writes 42 to the memory location that `p` holds — the same location as `n`. After this line, both `*p` and `n` are 42.

</details>

### Expected Output / Acceptance Criteria
The exact address will differ each run; the key results are the values:
```
p (address): 0xc000014098   (varies each run)
*p (value):  7
After *p = 42:
n = 42
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

func main() {
    n := 7
    p := &n  // p is *int; holds the address of n

    fmt.Printf("p (address): %p\n", p)  // %p prints pointer in hex
    fmt.Printf("*p (value):  %d\n", *p)

    *p = 42  // write through the pointer: sets n to 42

    fmt.Println("After *p = 42:")
    fmt.Printf("n = %d\n", n)  // 42 — same memory as *p
}
```

**Explanation:**
`p := &n` creates a `*int` whose value is the memory address of `n`. `*p` dereferences the pointer — it follows the address and reads the value stored there, which is the same value `n` holds. `*p = 42` writes 42 to that address, which is the same location as `n`. After the write, `n` is 42 — not because we assigned to `n` directly, but because `p` points to the same memory. `%p` in `fmt.Printf` formats a pointer as a hex address.

**Common wrong answers and why they fail:**
- `p := n` — this copies the value of `n` into `p`; `p` would be an `int`, not a `*int`; modifying `p` would have no effect on `n`
- `n := *p` after `p := &n` — this dereferences before n is initialized, which is syntactically incorrect and logically reversed

</details>

---

## Exercise 2: Mutating a Struct Through a Pointer [🟢 Easy] [1 pt]

### Context
A function that modifies a struct must receive a pointer to the struct, not a copy of it. This is the most common real-world use of pointers in Go: passing `*MyStruct` to a function so it can modify the caller's struct.

### Task
Write a Go function `rename(p *struct{ Name string }, newName string)` — or use a named struct type — that changes the `Name` field of the struct it receives. Call the function with a struct and verify the change is visible in the caller.

More specifically:
1. Define a struct type `Person` with a `Name string` field
2. Write a function `rename(p *Person, newName string)` that sets `p.Name = newName`
3. In `main`, create `alice := Person{Name: "Alice"}`, call `rename(&alice, "Alicia")`, and print `alice.Name` to confirm it changed

### Requirements
- [ ] `rename` takes `*Person`, not `Person`
- [ ] The assignment inside `rename` uses `p.Name = newName` (automatic dereference — not `(*p).Name`)
- [ ] The caller passes `&alice`
- [ ] After the call, `alice.Name` is `"Alicia"`

### Hints
<details>
<summary>Hint 1</summary>

Define the struct: `type Person struct { Name string }`. The function signature is `func rename(p *Person, newName string)`. Inside, `p.Name = newName` — Go automatically dereferences `p` for field access, so you don't need `(*p).Name`.

</details>

### Expected Output / Acceptance Criteria
```
Before: Alice
After:  Alicia
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type Person struct {
    Name string
}

// rename modifies the Name field of the Person p points to.
// Must take *Person — a plain Person parameter would modify a copy.
func rename(p *Person, newName string) {
    p.Name = newName  // automatic dereference: equivalent to (*p).Name = newName
}

func main() {
    alice := Person{Name: "Alice"}
    fmt.Println("Before:", alice.Name)

    rename(&alice, "Alicia")  // pass the address of alice
    fmt.Println("After: ", alice.Name)
}
```

**Explanation:**
`p.Name = newName` inside `rename` uses Go's automatic field dereference: since `p` is `*Person`, accessing `p.Name` is shorthand for `(*p).Name`. This writes directly to the `Name` field of the `Person` that `alice` refers to. If `rename` took `Person` instead of `*Person`, it would receive a copy of `alice`, modify the copy's name, and the caller would see no change.

</details>

---

## Exercise 3: nil Guard in Practice [🟡 Medium] [2 pts]

### Context
Any function that accepts a pointer parameter must decide: is nil a valid input? If yes, handle it. If no, document that nil is invalid and detect it early. This exercise practices writing safe pointer-accepting functions with explicit nil guards and demonstrates the panic that occurs without them.

### Task
Write a Go function `safeDouble(p *int) (int, error)` that:
1. Returns an error with message `"nil pointer"` if `p` is nil
2. Otherwise doubles the value at `p` in place (`*p *= 2`) and returns the new value and a nil error

Then demonstrate both paths in `main`:
- Call with a valid pointer to an integer and print the result
- Call with `nil` and print the error
- (Optional) Show what happens with a raw nil dereference in a comment or a separate function with `recover`

### Requirements
- [ ] `safeDouble` checks `p == nil` before any dereference
- [ ] Returns `(int, error)` — idiomatic Go error handling
- [ ] The nil path returns `(0, errors.New("nil pointer"))` (or similar)
- [ ] The happy path returns `(*p, nil)` after doubling
- [ ] `main` demonstrates both paths and prints results

### Hints
<details>
<summary>Hint 1</summary>

The function signature is `func safeDouble(p *int) (int, error)`. Import `"errors"`. The nil check is `if p == nil { return 0, errors.New("nil pointer") }`. Then `*p *= 2` modifies in place; `return *p, nil` returns the new value.

</details>

<details>
<summary>Hint 2</summary>

In `main`:
```go
n := 5
if val, err := safeDouble(&n); err == nil {
    fmt.Println(val)  // 10
} else {
    fmt.Println("error:", err)
}

if _, err := safeDouble(nil); err != nil {
    fmt.Println("error:", err)  // error: nil pointer
}
```

</details>

### Expected Output / Acceptance Criteria
```
doubled: 10
error: nil pointer
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "errors"
    "fmt"
)

// safeDouble doubles the value at p in place and returns the new value.
// Returns an error if p is nil.
func safeDouble(p *int) (int, error) {
    if p == nil {
        return 0, errors.New("nil pointer")
    }
    *p *= 2
    return *p, nil
}

func main() {
    n := 5
    if val, err := safeDouble(&n); err == nil {
        fmt.Println("doubled:", val)  // 10
    } else {
        fmt.Println("error:", err)
    }

    // nil path
    if _, err := safeDouble(nil); err != nil {
        fmt.Println("error:", err)  // error: nil pointer
    }
}
```

**Explanation:**
The nil guard `if p == nil` runs before any dereference. Without it, calling `safeDouble(nil)` would immediately panic on `*p *= 2` with "invalid memory address or nil pointer dereference." Returning `(int, error)` follows the standard Go idiom — callers must handle the error case explicitly. `*p *= 2` modifies the integer at the address `p` holds; `return *p, nil` reads back the modified value. Both the modification (`*p *= 2`) and the return read (`*p`) are safe because we already confirmed `p` is not nil.

**Alternative approaches:**
You could also `panic` instead of returning an error when `p == nil` — that is appropriate if nil is considered a programming error (not a recoverable condition). The choice between error return and panic depends on whether nil is a valid caller mistake or a bug.

</details>

---

## Exercise 4: `new()` vs `&T{}` [🟡 Medium] [2 pts]

### Context
Go provides two ways to get a pointer to a heap-allocated value: `new(T)` (allocates and zeroes) and `&T{...}` (composite literal then address). Understanding the difference and knowing which to use is an important practical skill.

### Task
Write a Go program that:
1. Creates a `*int` using `new(int)`, sets its value to `100`, and prints it
2. Creates a `*Point` (where `Point` has `X, Y float64`) using `new(Point)`, sets `X = 1.0` and `Y = 2.0` through the pointer, and prints it
3. Creates a `*Point` using `&Point{X: 3.0, Y: 4.0}` (composite literal) and prints it
4. Creates a `*Point` using `&Point{}` (zero value) and prints it
5. Adds a comment explaining which form you would prefer in real code and why

### Requirements
- [ ] At least one use of `new(T)` for a primitive type
- [ ] At least one use of `new(T)` for a struct (with post-construction field assignment)
- [ ] At least one use of `&T{field: value}` with initialization
- [ ] At least one use of `&T{}` for zero value
- [ ] A comment explaining the preference

### Hints
<details>
<summary>Hint 1</summary>

For `new(Point)`: `p := new(Point)` gives you `*Point` with `X=0, Y=0`. Then `p.X = 1.0; p.Y = 2.0` sets the fields. For `&Point{X: 3.0, Y: 4.0}`: this creates the struct and takes its address in one expression.

</details>

### Expected Output / Acceptance Criteria
```
new int:    100
new Point:  &{1 2}
&Point{}: &{3 4}
zero:      &{0 0}
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type Point struct {
    X, Y float64
}

func main() {
    // 1. new for a primitive type
    p := new(int)
    *p = 100
    fmt.Printf("new int:    %d\n", *p)

    // 2. new for a struct — fields set after allocation
    pt1 := new(Point)
    pt1.X = 1.0
    pt1.Y = 2.0
    fmt.Printf("new Point:  %v\n", pt1)

    // 3. &T{} with field initialization — preferred for structs
    pt2 := &Point{X: 3.0, Y: 4.0}
    fmt.Printf("&Point{}:   %v\n", pt2)

    // 4. &T{} zero value
    pt3 := &Point{}
    fmt.Printf("zero:       %v\n", pt3)

    // Preference: &T{} is preferred because it initializes fields in one expression,
    // makes the type visible at the allocation site, and is consistent with
    // all composite type literals. new(T) is fine for primitives but
    // rarely used for structs in modern Go code.
}
```

**Explanation:**
`new(int)` returns a `*int` pointing to a zero `int`; you must set the value separately (`*p = 100`). `new(Point)` returns a `*Point` with all fields zeroed; you set fields afterward. `&Point{X: 3.0, Y: 4.0}` creates the struct with initial values and returns a pointer in one expression — more compact and readable. For structs, `&T{...}` is almost always preferred because the initialization is co-located with the allocation. `new(T)` is occasionally useful for primitive types where there is no composite literal syntax.

</details>

---

## Exercise 5: Value vs Pointer Semantics for a Struct [🔴 Hard] [3 pts]

### Context
This exercise directly confronts the most common pointer mistake: writing a function that appears to modify a struct but doesn't, because the struct was passed by value. You will write two versions of an update function, observe the difference, and fix the broken one.

### Task
1. Define a struct `Rectangle` with `Width float64` and `Height float64` fields
2. Write a function `scaleValue(r Rectangle, factor float64)` that multiplies both dimensions by `factor` — passing by value
3. Write a function `scalePointer(r *Rectangle, factor float64)` that does the same — passing by pointer
4. In `main`, create `rect := Rectangle{Width: 10, Height: 5}`
5. Call `scaleValue(rect, 2)` and print `rect` — observe it is unchanged
6. Call `scalePointer(&rect, 2)` and print `rect` — observe it doubled

Then answer (as a comment in your code): why did `scaleValue` not change the original rectangle?

### Requirements
- [ ] Both functions are implemented and the distinction is visible in the output
- [ ] `scaleValue` uses a value receiver (`Rectangle`) — it modifies a copy
- [ ] `scalePointer` uses a pointer (`*Rectangle`) — it modifies the original
- [ ] A comment in the code explains why `scaleValue` doesn't affect the original
- [ ] Output clearly shows rectangle unchanged after `scaleValue` and doubled after `scalePointer`

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

`scaleValue` takes `r Rectangle` — inside the function, `r` is a copy. Modifying `r.Width` and `r.Height` modifies the copy's fields; the caller's `rect` is untouched.

`scalePointer` takes `r *Rectangle` — `r.Width *= factor` uses automatic dereference to modify the caller's fields.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

Go's call-by-value copies the struct on every call. When `scaleValue` runs, it has its own private copy of the Rectangle. The copy is discarded when the function returns. The original `rect` in main was never touched.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
func scaleValue(r Rectangle, factor float64) {
    r.Width *= factor   // modifying the copy
    r.Height *= factor  // discarded on return
}

func scalePointer(r *Rectangle, factor float64) {
    r.Width *= factor   // automatic dereference: (*r).Width *= factor
    r.Height *= factor  // modifies the caller's Rectangle
}
```

</details>

### Expected Output / Acceptance Criteria
```
Initial:              {10 5}
After scaleValue(2):  {10 5}    ← unchanged (value copy)
After scalePointer(2): {20 10}  ← doubled (modified through pointer)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type Rectangle struct {
    Width  float64
    Height float64
}

// scaleValue receives a COPY of the rectangle.
// Modifications to r do not affect the caller's variable.
func scaleValue(r Rectangle, factor float64) {
    r.Width *= factor   // modifying a copy — caller's Rectangle is unchanged
    r.Height *= factor  // this copy is discarded when the function returns
}

// scalePointer receives a POINTER to the rectangle.
// Modifications through r affect the caller's variable.
func scalePointer(r *Rectangle, factor float64) {
    r.Width *= factor   // automatic dereference: (*r).Width *= factor
    r.Height *= factor  // modifies the Rectangle that the caller owns
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}
    fmt.Printf("Initial:              %v\n", rect)

    // Pass by value — rect is unaffected
    scaleValue(rect, 2)
    fmt.Printf("After scaleValue(2):  %v\n", rect)  // {10 5} — unchanged

    // Pass by pointer — rect is modified
    scalePointer(&rect, 2)
    fmt.Printf("After scalePointer(2): %v\n", rect)  // {20 10} — doubled

    // Why scaleValue doesn't work: Go copies all function arguments.
    // scaleValue receives a new Rectangle with the same field values.
    // Any changes inside scaleValue affect only that private copy,
    // which is thrown away when the function returns.
    // scalePointer receives the ADDRESS of rect — the function
    // reaches back through the pointer and modifies the original.
}
```

**Step-by-step explanation:**

1. `rect := Rectangle{Width: 10, Height: 5}` — creates a Rectangle on the stack (or heap; the compiler decides) in `main`'s frame.
2. `scaleValue(rect, 2)` — Go evaluates `rect` and copies all its fields into a new local variable `r` inside `scaleValue`. The copy is modified, then discarded.
3. `fmt.Printf(rect)` — `rect` still holds `{10 5}`; it was never touched by `scaleValue`.
4. `scalePointer(&rect, 2)` — `&rect` takes the address of `rect`; the address is copied into `r *Rectangle` inside `scalePointer`. `r.Width *= factor` follows the pointer and modifies the field in `main`'s Rectangle.
5. `fmt.Printf(rect)` — `rect` now holds `{20 10}`.

**Why this approach:**
This side-by-side comparison makes the difference concrete and undeniable. The output proves the point. In real code, always use `scalePointer` (or a pointer receiver method) when mutation is the intent.

**What a weaker solution looks like and why it fails:**
Using `scaleValue` and returning the modified copy (`func scaleValue(r Rectangle, ...) Rectangle`) is a valid alternative — it communicates "I produce a new value, not modify the existing one." The choice between "modify in place via pointer" and "return a new value" is a deliberate API decision, not just a correctness issue.

</details>

---

## Exercise 6: Optional Config with Nil Pointer [🔴 Hard] [3 pts]

### Context
Using a pointer to represent an optional value is a common Go idiom, especially in configuration structs and JSON-mapped types. A `*int` can be nil (the option was not specified) or point to a value (the option was specified, even if that value is the type's zero value). This exercise practices that pattern in a realistic scenario.

### Task
Implement a `ServerConfig` struct and a `configureServer` function:

1. Define `ServerConfig` with:
   - `Host string` (required)
   - `Port *int` — optional; if nil, use port 8080 as the default
   - `MaxConns *int` — optional; if nil, use 100 as the default
   - `TLSEnabled *bool` — optional; if nil, default to false

2. Write `applyDefaults(cfg *ServerConfig)` that fills in nil fields with their defaults

3. Write `printConfig(cfg ServerConfig)` that prints all fields (dereferencing pointers safely)

4. In `main`:
   - Create a config with only `Host` set; call `applyDefaults`; print it
   - Create a config with all fields set; call `applyDefaults`; print it (defaults should not override explicit values)

### Requirements
- [ ] All three pointer fields are `*int` / `*bool` in the struct definition
- [ ] `applyDefaults` checks each pointer field for nil before assigning a default
- [ ] `printConfig` dereferences pointer fields safely (nil guard or confirm non-nil after applyDefaults)
- [ ] The "all set" config shows the explicit values, not the defaults

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

To set a default: `if cfg.Port == nil { defaultPort := 8080; cfg.Port = &defaultPort }`. You cannot write `cfg.Port = &8080` — you must use a named variable.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

After `applyDefaults` runs, all pointer fields are guaranteed non-nil. So in `printConfig`, you can safely dereference them without additional nil guards (assuming `applyDefaults` is always called first). Alternatively, use a helper like `derefInt(p *int) int` that returns 0 if nil.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
func applyDefaults(cfg *ServerConfig) {
    if cfg.Port == nil {
        port := 8080
        cfg.Port = &port
    }
    // ... same for MaxConns and TLSEnabled
}
```

</details>

### Expected Output / Acceptance Criteria
```
=== Minimal config (after defaults) ===
Host:     localhost
Port:     8080
MaxConns: 100
TLS:      false

=== Full config (after defaults) ===
Host:     myserver.com
Port:     9443
MaxConns: 500
TLS:      true
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type ServerConfig struct {
    Host       string
    Port       *int  // nil = use default (8080)
    MaxConns   *int  // nil = use default (100)
    TLSEnabled *bool // nil = use default (false)
}

// applyDefaults fills nil optional fields with their defaults.
// Takes *ServerConfig to modify the caller's config.
func applyDefaults(cfg *ServerConfig) {
    if cfg.Port == nil {
        port := 8080
        cfg.Port = &port
    }
    if cfg.MaxConns == nil {
        maxConns := 100
        cfg.MaxConns = &maxConns
    }
    if cfg.TLSEnabled == nil {
        tls := false
        cfg.TLSEnabled = &tls
    }
}

// printConfig prints all fields. Assumes applyDefaults was called first.
func printConfig(cfg ServerConfig) {
    fmt.Printf("Host:     %s\n", cfg.Host)
    fmt.Printf("Port:     %d\n", *cfg.Port)
    fmt.Printf("MaxConns: %d\n", *cfg.MaxConns)
    fmt.Printf("TLS:      %v\n", *cfg.TLSEnabled)
}

func main() {
    // Minimal config — only Host set
    minimal := ServerConfig{Host: "localhost"}
    applyDefaults(&minimal)
    fmt.Println("=== Minimal config (after defaults) ===")
    printConfig(minimal)

    // Full config — all fields explicit
    port := 9443
    maxConns := 500
    tls := true
    full := ServerConfig{
        Host:       "myserver.com",
        Port:       &port,
        MaxConns:   &maxConns,
        TLSEnabled: &tls,
    }
    applyDefaults(&full)  // should not change anything
    fmt.Println("\n=== Full config (after defaults) ===")
    printConfig(full)
}
```

**Step-by-step explanation:**

1. `ServerConfig` uses `*int` and `*bool` for optional fields. A nil pointer means "not specified by the caller" — this is distinct from "specified as 0" or "specified as false."
2. `applyDefaults` takes `*ServerConfig` because it needs to modify the config's pointer fields. If it took `ServerConfig`, it would modify a copy and the caller would see unchanged nil pointers.
3. Inside `applyDefaults`, `port := 8080; cfg.Port = &port` creates a local variable and stores its address. The variable escapes to the heap because its address outlives `applyDefaults` — the compiler handles this automatically.
4. `printConfig` takes `ServerConfig` by value — it only reads, so a copy is fine. After `applyDefaults`, all pointer fields are non-nil, so the dereferences in `printConfig` are safe.

**Why this approach:**
The `*T` optional pattern is how Go handles "present vs absent" without a separate `Optional[T]` wrapper type. JSON marshaling uses `omitempty` with pointer fields to omit nil values. This is a real pattern you will encounter in configuration packages, API request/response types, and database row mappers.

</details>

---

## Exercise 7: Singly-Linked List [⭐ Challenge] [5 pts]

### Context
A singly-linked list is the canonical data structure for practicing pointer manipulation. Each node holds a value and a pointer to the next node; the last node's `Next` pointer is nil, terminating the list. This exercise requires building and traversing a pointer chain — directly exercising every pointer concept from this module.

### Task
Implement a singly-linked list of integers:

1. Define `Node` struct with `Value int` and `Next *Node`
2. Write `prepend(head **Node, value int)` that inserts a new node at the beginning of the list (modifies the head pointer)
3. Write `printList(head *Node)` that traverses and prints all values
4. Write `length(head *Node) int` that counts nodes
5. In `main`, build a list by prepending 1, 2, 3, 4, 5 (so the list ends up as 5 → 4 → 3 → 2 → 1), print it, and print its length

### Requirements
- [ ] `Node` struct is defined with `Value int` and `Next *Node`
- [ ] `prepend` takes `**Node` (a pointer to the head pointer) so it can replace the head
- [ ] `printList` traverses via `for current := head; current != nil; current = current.Next`
- [ ] `length` counts nodes by traversing the list
- [ ] The list after prepending 1–5 is: 5 → 4 → 3 → 2 → 1 → nil

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

`prepend` needs `**Node` because it must change what the head points to. The pattern:
```go
func prepend(head **Node, value int) {
    newNode := &Node{Value: value, Next: *head}
    *head = newNode
}
```
`*head` is the current head pointer; `newNode.Next = *head` links the new node to the existing list; `*head = newNode` makes the new node the head.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

Why `**Node` and not `*Node`? If `prepend` took `*Node`, it would receive a copy of the head pointer. Assigning to the parameter would change the local copy, not the caller's `head` variable. `**Node` lets `prepend` write to the address of the caller's head pointer, updating it in place.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

Traversal pattern:
```go
func printList(head *Node) {
    for current := head; current != nil; current = current.Next {
        fmt.Printf("%d", current.Value)
        if current.Next != nil {
            fmt.Print(" → ")
        }
    }
    fmt.Println(" → nil")
}
```

</details>

### Expected Output / Acceptance Criteria
```
List: 5 → 4 → 3 → 2 → 1 → nil
Length: 5
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// Node is a singly-linked list node.
type Node struct {
    Value int
    Next  *Node  // nil for the last node
}

// prepend inserts a new node with value at the front of the list.
// Takes **Node so it can replace the caller's head pointer.
func prepend(head **Node, value int) {
    newNode := &Node{
        Value: value,
        Next:  *head,  // new node points to the current head
    }
    *head = newNode  // update the caller's head to the new node
}

// printList prints all values in the list, showing the nil terminator.
func printList(head *Node) {
    fmt.Print("List: ")
    for current := head; current != nil; current = current.Next {
        fmt.Printf("%d", current.Value)
        if current.Next != nil {
            fmt.Print(" → ")
        }
    }
    fmt.Println(" → nil")
}

// length returns the number of nodes in the list.
func length(head *Node) int {
    count := 0
    for current := head; current != nil; current = current.Next {
        count++
    }
    return count
}

func main() {
    var head *Node  // starts as nil (empty list)

    // Prepend 1, 2, 3, 4, 5 — result: 5 → 4 → 3 → 2 → 1 → nil
    for i := 1; i <= 5; i++ {
        prepend(&head, i)
    }

    printList(head)
    fmt.Printf("Length: %d\n", length(head))
}
```

**Step-by-step explanation:**

1. `var head *Node` — `head` starts as nil, representing an empty list.
2. `prepend(&head, i)` — passes the address of `head` (a `**Node`). Inside `prepend`, `*head` is the current head pointer value. A new node is created with `Next: *head` (pointing to the old head). Then `*head = newNode` updates the caller's `head` variable.
3. After prepending 1: `head → {1, nil}`. After prepending 2: `head → {2, *} → {1, nil}`. Each prepend inserts at the front, so the final order is 5→4→3→2→1.
4. `printList` traverses with `current = current.Next` until `current` is nil. The nil check `current != nil` in the loop condition prevents dereferencing a nil `Next` pointer.
5. `length` follows the same traversal pattern but counts instead of printing.

**Why this approach:**
The linked list requires `**Node` for `prepend` because the head itself must be reassigned — a concrete case where a pointer to a pointer is necessary. The traversal pattern (`for current := head; current != nil; current = current.Next`) is the canonical linked list walk and appears verbatim in many Go programs working with tree or list structures.

**What a weaker solution looks like and why it fails:**
Using a global variable for the head avoids `**Node` but is not idiomatic Go. Using a wrapper struct `type List struct { Head *Node }` and passing `*List` to `prepend` also avoids `**Node` — this is the more common approach in real Go code, because `**T` is confusing. Both are valid; the exercise uses `**Node` specifically to exercise the double-pointer concept.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Address-Of and Dereference Basics | — | —/1 | — | — |
| Exercise 2 — Mutating a Struct Through a Pointer | — | —/1 | — | — |
| Exercise 3 — nil Guard in Practice | — | —/2 | — | — |
| Exercise 4 — `new()` vs `&T{}` | — | —/2 | — | — |
| Exercise 5 — Value vs Pointer Semantics | — | —/3 | — | — |
| Exercise 6 — Optional Config with Nil Pointer | — | —/3 | — | — |
| Exercise 7 — Singly-Linked List | — | —/5 | — | — |
| **Total** | | **—/17** | | |

**Passing threshold:** 11/17 (65%). Aim for 14/17 (82%) before taking the test.
