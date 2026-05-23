# Go — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [Variable Declaration](#variable-declaration)
- [Types](#types)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Composite Types](#composite-types)
- [Pointers](#pointers)
- [Methods and Interfaces](#methods-and-interfaces)
- [Error Handling Patterns](#error-handling-patterns)
- [Goroutines and Channels](#goroutines-and-channels)
- [Common Patterns](#common-patterns)
- [Gotchas and Pitfalls](#gotchas-and-pitfalls)
- [go Command Reference](#go-command-reference)
- [Module Cross-References](#module-cross-references)

---

## Variable Declaration

```go
// Short declaration (inside functions only)
x := 42
name := "Alice"
ok := true

// var — explicit type or inferred
var x int = 42
var name string = "Alice"
var x int          // zero value: 0
var s string       // zero value: ""
var b bool         // zero value: false

// Multiple variables
var a, b, c int
a, b := 1, 2

// Constants
const Pi = 3.14159
const MaxRetries = 3
const greeting = "hello"

// iota — auto-incrementing constant generator
type Direction int
const (
    North Direction = iota  // 0
    East                    // 1
    South                   // 2
    West                    // 3
)

// Blank identifier — discard a value
_, err := strconv.Atoi("42")
```

---

## Types

```go
// Basic types
bool
string
int   int8   int16   int32   int64
uint  uint8  uint16  uint32  uint64  uintptr
byte  // alias for uint8
rune  // alias for int32 (Unicode code point)
float32  float64
complex64  complex128

// Zero values
// int/float/byte/rune → 0
// string             → ""
// bool               → false
// pointer/slice/map/chan/func/interface → nil

// Type conversion (always explicit)
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)
s := string(rune(65))  // "A"

// Type checking at runtime
var v interface{} = "hello"
s, ok := v.(string)      // type assertion; ok = true
switch v := v.(type) {   // type switch
case string:
    fmt.Println("string:", v)
case int:
    fmt.Println("int:", v)
}
```

---

## Control Flow

```go
// if / else if / else — no parentheses around condition
if x > 0 {
    fmt.Println("positive")
} else if x < 0 {
    fmt.Println("negative")
} else {
    fmt.Println("zero")
}

// if with initialization statement
if err := doSomething(); err != nil {
    return err
}

// for — Go's only loop keyword (three forms)

// Form 1: C-style for loop
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// Form 2: while-equivalent
for x < 100 {
    x *= 2
}

// Form 3: infinite loop
for {
    // break or return to exit
}

// range — iterate over slice, map, string, channel
for i, v := range slice {
    fmt.Println(i, v)
}
for k, v := range myMap {
    fmt.Println(k, v)
}
for i, ch := range "hello" {
    fmt.Println(i, ch)  // ch is a rune
}

// switch — no fallthrough by default
switch day {
case "Monday", "Tuesday":
    fmt.Println("weekday")
case "Saturday", "Sunday":
    fmt.Println("weekend")
default:
    fmt.Println("unknown")
}

// switch with no expression (replaces if/else chains)
switch {
case score >= 90:
    fmt.Println("A")
case score >= 80:
    fmt.Println("B")
default:
    fmt.Println("C or below")
}

// defer — runs when surrounding function returns (LIFO order)
defer file.Close()
defer fmt.Println("done")  // prints after the function body
```

---

## Functions

```go
// Basic function
func add(a, b int) int {
    return a + b
}

// Multiple parameters of same type — shorthand
func add(a, b int) int { ... }

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Named return values
func minMax(a, b int) (min, max int) {
    if a < b {
        return a, b
    }
    return b, a
}

// Variadic function
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
sum(1, 2, 3)
sum(nums...)  // spread a slice

// First-class functions
add := func(a, b int) int { return a + b }

// Closure
func counter() func() int {
    n := 0
    return func() int {
        n++
        return n
    }
}

// Function as parameter
func apply(nums []int, fn func(int) int) []int {
    result := make([]int, len(nums))
    for i, v := range nums {
        result[i] = fn(v)
    }
    return result
}
```

---

## Composite Types

```go
// Arrays — fixed length, value type
var a [5]int
a := [3]string{"foo", "bar", "baz"}
a := [...]int{1, 2, 3}  // length inferred

// Slices — dynamic, reference type
s := []int{1, 2, 3}
s := make([]int, 5)        // len=5, cap=5
s := make([]int, 0, 10)    // len=0, cap=10
s = append(s, 4, 5)
s2 := s[1:3]               // slice of slice (shares memory)
copy(dst, src)             // copy elements; doesn't share memory

// Maps
m := map[string]int{"a": 1, "b": 2}
m := make(map[string]int)
m["key"] = 42
v, ok := m["key"]   // ok = false if key absent
delete(m, "key")

// Structs
type Point struct {
    X, Y float64
}
type Person struct {
    Name string
    Age  int
}
p := Point{X: 1.0, Y: 2.0}
p := Point{1.0, 2.0}        // positional (avoid)
p.X = 3.0

// Anonymous struct
config := struct {
    Host string
    Port int
}{"localhost", 8080}

// Struct embedding (composition)
type Animal struct {
    Name string
}
type Dog struct {
    Animal          // embedded — Dog gets Animal's fields/methods
    Breed string
}
```

---

## Pointers

```go
// Pointer basics
x := 42
p := &x        // p is *int; points to x
*p = 100       // dereference; x is now 100

var p *int     // nil pointer
p = &x

// new — allocate zero value, return pointer
p := new(int)  // *p == 0

// Value vs pointer receiver
func (p Point) Scale(factor float64) Point {   // value receiver — copy
    return Point{p.X * factor, p.Y * factor}
}
func (p *Point) ScaleInPlace(factor float64) { // pointer receiver — modifies original
    p.X *= factor
    p.Y *= factor
}

// When to use pointer receiver:
// - Method needs to modify the receiver
// - Receiver is a large struct (avoid copying)
// - Consistency: if any method uses pointer, use pointer for all
```

---

## Methods and Interfaces

```go
// Method definition
type Rectangle struct {
    Width, Height float64
}
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}
func (r Rectangle) Perimeter() float64 {
    return 2 * (r.Width + r.Height)
}

// Interface — satisfied implicitly (no "implements" keyword)
type Shape interface {
    Area() float64
    Perimeter() float64
}

// Rectangle satisfies Shape automatically
var s Shape = Rectangle{3, 4}
fmt.Println(s.Area())

// Empty interface — holds any value (use sparingly)
var any interface{} = 42
any = "now a string"

// In Go 1.18+: use 'any' as alias for interface{}
var v any = 42

// Stringer interface (fmt package)
func (r Rectangle) String() string {
    return fmt.Sprintf("Rect(%.1f × %.1f)", r.Width, r.Height)
}

// Type assertion
var i interface{} = "hello"
s := i.(string)           // panics if wrong type
s, ok := i.(string)       // safe form; ok = false if wrong

// Type switch
switch v := i.(type) {
case string:
    fmt.Printf("string: %q\n", v)
case int:
    fmt.Printf("int: %d\n", v)
default:
    fmt.Printf("unknown type: %T\n", v)
}
```

---

## Error Handling Patterns

```go
// Error as a value — always check it
result, err := strconv.Atoi("42")
if err != nil {
    return fmt.Errorf("parsing failed: %w", err)
}

// Creating errors
import "errors"
var ErrNotFound = errors.New("not found")

// Wrapping errors (Go 1.13+)
return fmt.Errorf("getUserByID: %w", ErrNotFound)

// Unwrapping: errors.Is / errors.As
if errors.Is(err, ErrNotFound) {
    // handle not-found specifically
}
var myErr *MyCustomError
if errors.As(err, &myErr) {
    // handle myErr fields
}

// Custom error type
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

// panic / recover (exceptional cases only — not for regular errors)
func safeDivide(a, b int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("recovered from panic: %v", r)
        }
    }()
    return a / b, nil
}
```

---

## Goroutines and Channels

```go
// Goroutine — start with 'go'
go func() {
    fmt.Println("running concurrently")
}()
go myFunction(arg1, arg2)

// Unbuffered channel — synchronous hand-off
ch := make(chan int)
go func() { ch <- 42 }()   // send blocks until receiver is ready
v := <-ch                   // receive blocks until sender sends

// Buffered channel — asynchronous up to capacity
ch := make(chan string, 3)
ch <- "a"   // doesn't block (buffer not full)
ch <- "b"
ch <- "c"
// ch <- "d" would block — buffer full

// Close and range
close(ch)
for v := range ch {    // receives until channel is closed
    fmt.Println(v)
}

// select — wait on multiple channels
select {
case msg := <-ch1:
    fmt.Println("from ch1:", msg)
case msg := <-ch2:
    fmt.Println("from ch2:", msg)
case <-time.After(1 * time.Second):
    fmt.Println("timeout")
default:
    fmt.Println("no channel ready")
}

// sync.WaitGroup — wait for goroutines to finish
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(n int) {
        defer wg.Done()
        fmt.Println(n)
    }(i)
}
wg.Wait()

// sync.Mutex — protect shared state
var mu sync.Mutex
var counter int
mu.Lock()
counter++
mu.Unlock()

// sync.Once — run something exactly once
var once sync.Once
once.Do(func() { initializeOnce() })
```

---

## Common Patterns

### Pattern 1: Functional Options

**When to use:** Configuring a struct with optional parameters without boolean flags or giant constructors.

```go
type Server struct {
    host    string
    port    int
    timeout time.Duration
}
type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}
func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}
func NewServer(host string, opts ...Option) *Server {
    s := &Server{host: host, port: 8080, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

s := NewServer("localhost", WithPort(9090), WithTimeout(5*time.Second))
```

---

### Pattern 2: Table-Driven Tests

**When to use:** Any time you test a function with multiple input/output pairs.

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

---

### Pattern 3: Context for Cancellation

**When to use:** Any I/O-bound or long-running operation that should be cancellable.

```go
func fetchUser(ctx context.Context, id int) (*User, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    // decode response...
}

ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
user, err := fetchUser(ctx, 42)
```

---

### Pattern 4: init Function

**When to use:** One-time package initialization (registering drivers, setting defaults).

```go
func init() {
    // runs automatically before main() or any other code in the package
    // use sparingly — prefer explicit initialization where possible
    log.SetFlags(log.LstdFlags | log.Lshortfile)
}
```

---

## Gotchas and Pitfalls

> [!WARNING]
> **Unused imports are a compile error**
> Adding an import and not using it prevents compilation. Remove unused imports or use `_` to import for side effects: `import _ "net/http/pprof"`.

> [!WARNING]
> **Unused variables are a compile error**
> Declaring a variable with `:=` and never reading it is a compile error. Use `_` to explicitly discard: `_, err := doSomething()`.

> [!WARNING]
> **Loop variable capture in goroutines**
> Classic bug: capturing the loop variable `i` in a goroutine. By the time the goroutine runs, `i` may have changed.
>
> Wrong: `go func() { fmt.Println(i) }()`
> Right: `go func(n int) { fmt.Println(n) }(i)` — pass i as an argument

> [!WARNING]
> **Slice shares underlying array**
> `s2 := s[1:3]` creates a new slice header but shares the same backing array. Modifying `s2[0]` modifies `s[1]`. Use `copy()` to get an independent slice.

**Other things to watch out for:**

- **nil map write panics** — you can read from a nil map (returns zero value), but writing to one panics. Always `make(map[K]V)` before writing.
- **Goroutine leak** — goroutines that block forever on a channel with no sender/receiver are a leak. Use `context` or `select` with a `done` channel.
- **Deferred function evaluates arguments immediately** — `defer fmt.Println(x)` captures the value of `x` at the defer statement, not when it runs. Use a closure to capture the current value at call time.
- **Integer overflow is silent** — Go does not panic on integer overflow; it wraps around silently. Use `math/big` or explicit range checks when overflow is a concern.

---

## go Command Reference

| Command | What It Does | Example |
|---------|-------------|---------|
| `go run` | Compile and run a Go file or package | `go run main.go` |
| `go build` | Compile to a binary | `go build -o myapp .` |
| `go test` | Run tests | `go test ./...` |
| `go fmt` | Format source code (gofmt) | `go fmt ./...` |
| `go vet` | Report likely mistakes | `go vet ./...` |
| `go mod init` | Initialize a new module | `go mod init github.com/user/project` |
| `go mod tidy` | Add missing / remove unused dependencies | `go mod tidy` |
| `go get` | Add or update a dependency | `go get golang.org/x/tools@latest` |
| `go install` | Compile and install a binary | `go install golang.org/x/tools/gopls@latest` |
| `go doc` | Show documentation | `go doc fmt.Println` |
| `go env` | Show Go environment variables | `go env GOPATH` |

**Cross-compilation:**
```bash
GOOS=linux GOARCH=amd64 go build -o app-linux .
GOOS=windows GOARCH=amd64 go build -o app.exe .
GOOS=darwin GOARCH=arm64 go build -o app-mac .
```

---

## Quick Conversions / Tables

### Zero Values by Type

| Type | Zero Value |
|------|-----------|
| `int`, `int8`…`int64` | `0` |
| `uint`, `uint8`…`uint64` | `0` |
| `float32`, `float64` | `0.0` |
| `bool` | `false` |
| `string` | `""` |
| `byte`, `rune` | `0` |
| pointer, slice, map, chan | `nil` |
| interface | `nil` |
| struct | all fields set to their zero values |

### Common fmt Verbs

| Verb | Meaning |
|------|---------|
| `%v` | Default format |
| `%+v` | Struct with field names |
| `%#v` | Go-syntax representation |
| `%T` | Type of the value |
| `%d` | Integer (decimal) |
| `%f` | Floating point |
| `%s` | String |
| `%q` | Quoted string |
| `%t` | Boolean |
| `%p` | Pointer address |
| `%w` | Wrap an error (fmt.Errorf only) |

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| Variable declaration, iota, zero values | [[go/1. Types and Variables]] |
| for loops, switch, defer | [[go/2. Control Flow]] |
| Multiple returns, closures | [[go/3. Functions]] |
| Slices, maps, structs | [[go/4. Composite Types]] |
| Pointer receivers, value semantics | [[go/5. Pointers]] |
| Interface design, type assertions | [[go/6. Methods and Interfaces]] |
| Package organization, go.mod | [[go/7. Packages and Modules]] |
| Error wrapping, errors.Is/As | [[go/8. Error Handling]] |
| Goroutines, channels, select, sync | [[go/9. Concurrency]] |

---

_Last updated: 2026-05-23_
