# Go — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of Go.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use. Code snippet or real-world scenario.
```

Keep definitions in your own words as much as possible.

---

## B

### blank identifier

**Definition:** The underscore `_` used in place of a variable name to discard a value that the compiler would otherwise require you to name. It tells Go "I know this value exists, but I am intentionally not using it."

**Also known as:** anonymous variable (informal)

**Related:** [[unused-variable]], [[multiple-return-values]]

**Example:**
```go
_, err := strconv.Atoi("42")   // discard the integer, keep the error
for _, v := range slice { }    // discard the index
```

---

## C

### channel

**Definition:** A typed conduit through which goroutines can send and receive values. Channels provide a safe way to communicate between concurrently running goroutines without explicit locking. The Go philosophy: "Do not communicate by sharing memory; share memory by communicating."

**Also known as:** chan (type keyword)

**Related:** [[goroutine]], [[select]], [[buffered-channel]]

**Example:**
```go
ch := make(chan int)         // unbuffered
ch := make(chan string, 10)  // buffered, capacity 10
ch <- 42                     // send
v := <-ch                    // receive
```

---

## D

### defer

**Definition:** A statement that schedules a function call to run immediately before the surrounding function returns. Multiple deferred calls run in LIFO (last-in, first-out) order. Commonly used for cleanup operations like closing files or releasing locks.

**Related:** [[panic]], [[recover]], [[function]]

**Example:**
```go
func readFile(path string) error {
    f, err := os.Open(path)
    if err != nil { return err }
    defer f.Close()   // runs when readFile returns, regardless of how
    // ... use f
}
```

---

## E

### embedding

**Definition:** A mechanism to include one type's fields and methods into another type without explicit inheritance. The embedded type's name (without the package qualifier) becomes a field name, and all of its exported fields and methods are promoted to the outer struct.

**Also known as:** struct embedding, type embedding

**Related:** [[struct]], [[interface]], [[composition-over-inheritance]]

**Example:**
```go
type Animal struct{ Name string }
func (a Animal) Speak() string { return a.Name + " speaks" }

type Dog struct {
    Animal         // embedded — Dog gets Name and Speak()
    Breed string
}
d := Dog{Animal: Animal{Name: "Rex"}, Breed: "Husky"}
fmt.Println(d.Speak())   // "Rex speaks"
```

---

### exported identifier

**Definition:** Any identifier (variable, function, type, method, field) whose name begins with an uppercase letter. Exported identifiers are visible outside their package. Identifiers starting with a lowercase letter are unexported (package-private).

**Also known as:** public (in other languages)

**Related:** [[package]], [[unexported-identifier]], [[visibility]]

**Example:**
```go
package mypackage

var InternalCount int   // exported — accessible from other packages
var internalState int   // unexported — only visible within mypackage

func DoWork() {}    // exported
func helper() {}    // unexported
```

---

## G

### go.mod

**Definition:** The module definition file at the root of a Go module. It declares the module path, the minimum required Go version, and the module's dependencies with their versions. Created by `go mod init`; managed by `go mod tidy` and `go get`.

**Related:** [[module]], [[GOPATH]], [[go.sum]]

**Example:**
```
module github.com/user/myapp

go 1.21

require (
    golang.org/x/text v0.14.0
    github.com/spf13/cobra v1.8.0
)
```

---

### GOPATH

**Definition:** The legacy Go workspace directory structure used before Go modules (pre-1.11). All Go code had to live under `$GOPATH/src/`. In modern Go (1.16+), GOPATH is largely irrelevant for day-to-day work because modules allow code to live anywhere on the filesystem.

**Related:** [[go.mod]], [[module]], [[workspace]]

**Example:**
```
# Old GOPATH structure (legacy):
$GOPATH/
  src/
    github.com/user/project/
  bin/
  pkg/
```

---

### goroutine

**Definition:** A lightweight, cooperatively scheduled function running concurrently with other goroutines in the same process. Goroutines are multiplexed onto OS threads by the Go runtime. They are far cheaper than OS threads — a Go program can have thousands or millions of goroutines simultaneously. Created with the `go` keyword.

**Related:** [[channel]], [[scheduler]], [[sync.WaitGroup]]

**Example:**
```go
go func() {
    fmt.Println("I run concurrently")
}()
go doWork(arg)   // doWork runs in a new goroutine
```

---

## I

### init function

**Definition:** A special function named `init()` that runs automatically when a package is loaded, before `main()` or any other code in the package. A package can have multiple `init()` functions across multiple files; they all run in the order the source files are presented to the compiler. Cannot be called explicitly.

**Related:** [[package]], [[main]]

**Example:**
```go
func init() {
    log.SetFlags(log.LstdFlags | log.Lshortfile)
}
```

---

### interface

**Definition:** A type that defines a set of method signatures. Any type that implements all the methods in an interface satisfies that interface implicitly — there is no `implements` keyword. This is called structural (or duck) typing. Interfaces enable polymorphism and decoupling without inheritance.

**Related:** [[method]], [[type-assertion]], [[embedding]], [[duck-typing]]

**Example:**
```go
type Writer interface {
    Write(p []byte) (n int, err error)
}
// os.File, bytes.Buffer, and many others satisfy Writer implicitly
```

---

### iota

**Definition:** A special predeclared identifier in `const` blocks that starts at 0 for the first constant in the block and increments by 1 for each subsequent constant. Useful for creating sequences of related constants (enumerations). Resets to 0 in each new `const` block.

**Related:** [[const]], [[enumeration]]

**Example:**
```go
const (
    Sunday = iota  // 0
    Monday         // 1
    Tuesday        // 2
    // ...
)
const (
    KB = 1 << (10 * (iota + 1))  // 1024
    MB                            // 1048576
    GB                            // 1073741824
)
```

---

## M

### map

**Definition:** Go's built-in hash table type. Maps associate keys of one type to values of another type. The zero value of a map is `nil`; writing to a nil map panics. Use `make` to initialize, or a map literal.

**Related:** [[slice]], [[struct]], [[zero-value]]

**Example:**
```go
m := make(map[string]int)
m["apples"] = 5
count, ok := m["bananas"]   // ok = false; count = 0
delete(m, "apples")
```

---

### module

**Definition:** The unit of versioning, dependency management, and distribution in Go. A module is a collection of related packages sharing a common module path (declared in go.mod). A module can contain many packages. Introduced in Go 1.11 to replace the GOPATH workspace model.

**Also known as:** Go module

**Related:** [[go.mod]], [[package]], [[GOPATH]]

**Example:**
```bash
go mod init github.com/user/myproject
```

---

## P

### panic

**Definition:** A built-in function that stops normal execution of the current goroutine, unwinds the stack, and runs any deferred functions along the way. If no `recover()` intercepts it, the program crashes with a stack trace. Should only be used for unrecoverable situations (programming errors), not for ordinary error handling.

**Related:** [[recover]], [[defer]], [[error]]

**Example:**
```go
panic("unexpected nil pointer")
panic(fmt.Sprintf("index %d out of range", i))
```

---

## R

### recover

**Definition:** A built-in function that regains control of a panicking goroutine. Must be called directly inside a deferred function to have any effect. Returns the value passed to `panic()`, or `nil` if the goroutine is not panicking.

**Related:** [[panic]], [[defer]]

**Example:**
```go
defer func() {
    if r := recover(); r != nil {
        fmt.Println("recovered:", r)
    }
}()
```

---

### rune

**Definition:** An alias for `int32` representing a Unicode code point. Used when iterating over strings character-by-character (as opposed to byte-by-byte). A `string` in Go is a sequence of bytes; iterating with `range` yields runes. String literals are UTF-8 encoded.

**Also known as:** Unicode code point

**Related:** [[string]], [[byte]], [[unicode]]

**Example:**
```go
for i, r := range "héllo" {
    fmt.Printf("index %d: rune %c (%d)\n", i, r, r)
}
// 'é' is a multi-byte UTF-8 sequence; i jumps by 2
```

---

## S

### slice

**Definition:** A dynamically-sized, flexible view into an array. A slice has three components: a pointer to an underlying array, a length, and a capacity. Multiple slices can share the same underlying array. The zero value is `nil`. Go's most commonly used sequence type.

**Related:** [[array]], [[append]], [[copy]], [[map]]

**Example:**
```go
s := []int{1, 2, 3}
s = append(s, 4)
sub := s[1:3]       // [2 3] — shares array with s
s2 := make([]int, 5)
```

---

### struct

**Definition:** A composite type that groups zero or more named fields of arbitrary types. Structs are the primary way to define custom data types in Go. They are value types: assigning a struct copies all its fields.

**Related:** [[method]], [[embedding]], [[pointer]]

**Example:**
```go
type Point struct {
    X, Y float64
}
p := Point{X: 1.5, Y: 2.5}
fmt.Println(p.X)
```

---

## T

### type assertion

**Definition:** An operation that extracts the concrete type from an interface value, or checks whether an interface holds a specific type. The two-value form (`v, ok := i.(T)`) is safe and does not panic. The single-value form (`v := i.(T)`) panics if the interface does not hold type T.

**Related:** [[interface]], [[type-switch]]

**Example:**
```go
var i interface{} = "hello"
s, ok := i.(string)    // s = "hello", ok = true
n, ok := i.(int)       // n = 0, ok = false (no panic)
```

---

## W

### workspace

**Definition:** A Go workspace (introduced in Go 1.18 with `go work`) allows working on multiple modules simultaneously without replacing dependencies with local copies. A `go.work` file at the root of the workspace lists the modules. Primarily useful for local multi-module development.

**Related:** [[module]], [[go.mod]]

**Example:**
```bash
go work init ./module-a ./module-b
# creates go.work referencing both modules
```

---

## Z

### zero value

**Definition:** The default value assigned to every variable in Go when it is declared without an explicit initializer. Every type has a well-defined zero value: `0` for numeric types, `""` for strings, `false` for booleans, and `nil` for pointers, slices, maps, channels, and interfaces. This eliminates uninitialized variable bugs common in C/C++.

**Related:** [[variable-declaration]], [[nil]], [[initialization]]

**Example:**
```go
var i int        // i == 0
var s string     // s == ""
var b bool       // b == false
var p *int       // p == nil
var sl []int     // sl == nil (len 0, cap 0)
```

---

## Symbols & Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| `:=` | Short variable declaration (inside functions) | `x := 42` |
| `&` | Address-of operator; returns a pointer | `p := &x` |
| `*` | Dereference operator; or pointer type | `*p = 10`; `var p *int` |
| `<-` | Channel send or receive | `ch <- v`; `v := <-ch` |
| `_` | Blank identifier; discard a value | `_, err := fn()` |
| `...` | Variadic parameter or slice spread | `func f(a ...int)`; `f(s...)` |

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 20 |
| Terms pending definition | 0 |
| Last updated | 2026-05-23 |
