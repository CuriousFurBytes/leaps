# Exercises — Module 15: Reflection and Metaprogramming

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

## Exercise 1: Read Type and Kind [🟢 Easy] [1 pt]

### Context
`reflect.TypeOf` and `reflect.ValueOf` are the entry points to all reflection. This exercise confirms you can call them correctly and understand the difference between `Type` (the specific named type) and `Kind` (the underlying structural category).

### Task
Write a function `typeInfo(v interface{})` that prints, on one line:
- The `reflect.Type` of the value (via `reflect.TypeOf`)
- The `reflect.Kind` of the value (via `.Kind()`)

Call it with at least five different values: an `int`, a `string`, a struct of your choice, a `[]int` slice, and a `map[string]int`.

### Requirements
- [ ] Uses `reflect.TypeOf(v)` and `.Kind()`
- [ ] Called with at least 5 different values covering: int, string, struct, slice, map
- [ ] Output shows both the type name and the kind for each value
- [ ] The program compiles and runs without errors

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

`reflect.TypeOf(v).Name()` gives the type name (e.g., `"int"`, `"MyStruct"`; empty for unnamed composite types like `[]int`). `reflect.TypeOf(v).Kind()` gives the underlying kind (e.g., `reflect.Int`, `reflect.Slice`). Use `reflect.TypeOf(v).String()` to get a printable representation that works for both named and unnamed types.

</details>

### Expected Output / Acceptance Criteria
Output should look similar to (exact struct name will vary):
```
int        kind=int
string     kind=string
Point      kind=struct
[]int      kind=slice
map[string]int  kind=map
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "fmt"
    "reflect"
)

type Point struct{ X, Y float64 }

func typeInfo(v interface{}) {
    t := reflect.TypeOf(v)
    fmt.Printf("%-20s kind=%-10s\n", t.String(), t.Kind())
}

func main() {
    typeInfo(42)
    typeInfo("hello")
    typeInfo(Point{1, 2})
    typeInfo([]int{1, 2, 3})
    typeInfo(map[string]int{"a": 1})
}
```

**Explanation:**
`reflect.TypeOf(v).String()` is the most reliable way to print the type: it returns `"int"`, `"main.Point"`, `"[]int"`, `"map[string]int"` — covering named, unnamed, and composite types. `.Kind()` returns a `reflect.Kind` constant that prints as a lowercase string (`int`, `struct`, `slice`, `map`). The distinction matters when you have a user-defined type like `type MyInt int`: its `String()` is `"main.MyInt"` but its `Kind()` is still `int`.

**Common wrong answers and why they fail:**
- Using `t.Name()` instead of `t.String()` — `Name()` returns empty string for composite types like `[]int` and `map[string]int`
- Printing `v` directly — prints the value, not the type information

</details>

---

## Exercise 2: Read Struct Tags [🟢 Easy] [1 pt]

### Context
Struct tags are the metadata system used by `encoding/json`, `database/sql`, and countless other packages. This exercise confirms you can read them programmatically using `reflect.StructField.Tag`.

### Task
Define the following struct:

```go
type Employee struct {
    ID         int    `json:"id"               db:"employee_id"`
    FirstName  string `json:"first_name"        db:"first_name"`
    Department string `json:"department,omitempty"`
    secret     string // unexported — no tags accessible
}
```

Write a function `printTags(v interface{})` that iterates over all exported fields of any struct and prints, for each field: the field name, the `json` tag value, and the `db` tag value (empty string if absent).

### Requirements
- [ ] Uses `reflect.TypeOf` to get the struct type, `NumField()` and `Field(i)` to iterate
- [ ] Uses `field.Tag.Get("json")` and `field.Tag.Get("db")` to read tags
- [ ] Skips unexported fields (check `field.IsExported()`)
- [ ] Prints all three exported fields of `Employee` with their tag values

### Hints
<details>
<summary>Hint 1</summary>

`reflect.TypeOf(v)` when `v` is a struct gives you the struct's `reflect.Type`. If `v` might be a pointer, first call `reflect.TypeOf(v).Elem()` after checking `Kind() == reflect.Pointer`. Then `t.NumField()` gives the count, and `t.Field(i)` returns a `reflect.StructField` with `.Name`, `.Tag`, and `.IsExported()`.

</details>

### Expected Output / Acceptance Criteria
```
Field: ID           json:"id"                db:"employee_id"
Field: FirstName    json:"first_name"        db:"first_name"
Field: Department   json:"department,omitempty"  db:""
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "reflect"
)

type Employee struct {
    ID         int    `json:"id"               db:"employee_id"`
    FirstName  string `json:"first_name"        db:"first_name"`
    Department string `json:"department,omitempty"`
    secret     string
}

func printTags(v interface{}) {
    t := reflect.TypeOf(v)
    if t.Kind() == reflect.Pointer {
        t = t.Elem()
    }
    if t.Kind() != reflect.Struct {
        fmt.Println("not a struct")
        return
    }
    for i := 0; i < t.NumField(); i++ {
        f := t.Field(i)
        if !f.IsExported() {
            continue
        }
        jsonTag := f.Tag.Get("json")
        dbTag := f.Tag.Get("db")
        fmt.Printf("Field: %-14s json:%-30q db:%q\n", f.Name, jsonTag, dbTag)
    }
}

func main() {
    printTags(Employee{})
}
```

**Explanation:**
`reflect.StructField.Tag` is of type `reflect.StructTag` — essentially a string. `Tag.Get(key)` parses the tag string to find the value for the given key. It returns `""` if the key is absent, which is correct for `Department`'s missing `db` tag. `f.IsExported()` (Go 1.17+) replaces the older `f.PkgPath == ""` check. The `secret` field is skipped because it is unexported.

</details>

---

## Exercise 3: Struct-to-Map Serializer [🟡 Medium] [2 pts]

### Context
Understanding how `encoding/json` works internally means being able to build a minimal version yourself. This exercise requires combining struct field iteration, tag reading, `omitempty` logic, and `val.Interface()` — the same pattern that powers JSON marshaling, YAML serialization, and ORM field mapping.

### Task
Write a function `ToMap(v interface{}) map[string]interface{}` that:
1. Accepts any struct (or pointer to struct)
2. Returns a `map[string]interface{}` where each key is determined by the `json` struct tag (or the field name if no tag)
3. Skips fields tagged `json:"-"`
4. Skips fields with `omitempty` when their value is the zero value (use `reflect.Value.IsZero()`)
5. Skips unexported fields

Test it with:
```go
type Product struct {
    SKU      string `json:"sku"`
    Name     string `json:"name"`
    Price    float64 `json:"price,omitempty"`
    Internal string  `json:"-"`
    Notes    string  // no tag — use field name
}
```

### Requirements
- [ ] Handles pointer-to-struct input by dereferencing with `Elem()`
- [ ] Uses `field.Tag.Get("json")` and splits on `","` to separate name from options
- [ ] Correctly applies `omitempty` using `val.IsZero()`
- [ ] Fields with `json:"-"` are completely omitted
- [ ] Unexported fields are skipped
- [ ] Returns `nil` (not panic) for non-struct input

### Hints
<details>
<summary>Hint 1</summary>

Parse the tag with `strings.SplitN(tag, ",", 2)`. `parts[0]` is the JSON key name (use the field name if it's empty). Check `len(parts) > 1 && parts[1] == "omitempty"` for the omitempty flag. Use `val.IsZero()` to detect zero values for any kind.

</details>

<details>
<summary>Hint 2</summary>

To get the `reflect.Value` of a field for reading, use `rv.Field(i).Interface()`. This returns the field's value as `interface{}`. Make sure `rv` is the struct value (not pointer) before calling `.Field(i)`.

</details>

### Expected Output / Acceptance Criteria
With `Product{SKU: "ABC-1", Name: "Widget", Internal: "hidden"}` (Price is zero):
```go
// map should contain:
// "sku"   -> "ABC-1"
// "name"  -> "Widget"
// "Notes" -> ""        (no tag, field name used; not omitempty, so included even if zero)
// price and Internal are absent
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "reflect"
    "strings"
)

func ToMap(v interface{}) map[string]interface{} {
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

        tag := field.Tag.Get("json")
        if tag == "-" {
            continue
        }

        name := field.Name
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

        if omitempty && val.IsZero() {
            continue
        }

        result[name] = val.Interface()
    }
    return result
}

type Product struct {
    SKU      string  `json:"sku"`
    Name     string  `json:"name"`
    Price    float64 `json:"price,omitempty"`
    Internal string  `json:"-"`
    Notes    string  // no tag
}

func main() {
    p := Product{SKU: "ABC-1", Name: "Widget", Internal: "hidden"}
    m := ToMap(p)
    for k, v := range m {
        fmt.Printf("  %q: %v\n", k, v)
    }
    // Expected keys: "sku", "name", "Notes"
    // Absent: "price" (omitempty + zero), "Internal" (tagged "-")
}
```

**Explanation:**
`strings.SplitN(tag, ",", 2)` splits on the first comma only, giving at most two parts: the name and the options. `val.IsZero()` correctly identifies zero values for all kinds — `0` for int, `""` for string, `false` for bool, `nil` for pointers. This is the same logic `encoding/json` uses, just spelled out explicitly.

**Alternative approaches:**
You could parse `omitempty` by checking `strings.Contains(parts[1], "omitempty")` to handle future options like `json:"name,omitempty,string"` — that would be more robust.

</details>

---

## Exercise 4: Set Fields via Reflection [🟡 Medium] [2 pts]

### Context
Setting values via reflection is trickier than reading — it requires an addressable value obtained from a pointer. This exercise is the canonical use case: a function that applies default values to any struct whose fields are still at their zero value.

### Task
Write a function `ApplyDefaults(ptr interface{}, defaults map[string]interface{})` that:
1. Takes a pointer to any struct
2. For each key in `defaults`, finds the exported struct field with that name
3. If the field's current value is zero (`IsZero()`), sets it to the default value
4. Skips non-existent field names silently

Use it to populate a `Config` struct:

```go
type Config struct {
    Host    string
    Port    int
    Timeout int
    Debug   bool
}
```

### Requirements
- [ ] Panics (or returns an error) if `ptr` is not a pointer to a struct
- [ ] Uses `reflect.ValueOf(ptr).Elem()` to get the addressable struct value
- [ ] Calls `CanSet()` before calling `Set` or kind-specific setters
- [ ] Uses `reflect.ValueOf(defaultVal)` and a `Set` call to apply the default
- [ ] Does not overwrite fields that are already non-zero

### Hints
<details>
<summary>Hint 1</summary>

Use `s.FieldByName(name)` to find a field by name. It returns a zero `reflect.Value` if the field does not exist — check `f.IsValid()` before proceeding. Then check `f.CanSet()` before calling `f.Set(reflect.ValueOf(defaultVal))`.

</details>

<details>
<summary>Hint 2</summary>

`reflect.ValueOf(defaultVal)` gives you a `reflect.Value` to pass to `f.Set()`. But `Set` requires that the types match exactly. Use `f.Set(reflect.ValueOf(defaultVal).Convert(f.Type()))` to handle cases where the default is an `int` literal but the field is `int64`, etc.

</details>

### Expected Output / Acceptance Criteria
```go
cfg := Config{Host: "prod.example.com"} // Port, Timeout, Debug are zero
ApplyDefaults(&cfg, map[string]interface{}{
    "Host":    "localhost", // already set — should NOT be overwritten
    "Port":    8080,
    "Timeout": 30,
})
// cfg.Host == "prod.example.com" (unchanged)
// cfg.Port == 8080
// cfg.Timeout == 30
// cfg.Debug == false (not in defaults map)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "reflect"
)

func ApplyDefaults(ptr interface{}, defaults map[string]interface{}) {
    rv := reflect.ValueOf(ptr)
    if rv.Kind() != reflect.Pointer || rv.Elem().Kind() != reflect.Struct {
        panic("ApplyDefaults: requires a pointer to a struct")
    }
    s := rv.Elem() // addressable struct

    for name, defaultVal := range defaults {
        f := s.FieldByName(name)
        if !f.IsValid() || !f.CanSet() {
            continue // field doesn't exist or is unexported
        }
        if !f.IsZero() {
            continue // already has a value — don't overwrite
        }
        dv := reflect.ValueOf(defaultVal)
        // Convert if underlying kinds are compatible (e.g., int → int64)
        if dv.Type().ConvertibleTo(f.Type()) {
            f.Set(dv.Convert(f.Type()))
        }
    }
}

type Config struct {
    Host    string
    Port    int
    Timeout int
    Debug   bool
}

func main() {
    cfg := Config{Host: "prod.example.com"}
    ApplyDefaults(&cfg, map[string]interface{}{
        "Host":    "localhost",
        "Port":    8080,
        "Timeout": 30,
    })
    fmt.Printf("Host=%s Port=%d Timeout=%d Debug=%v\n",
        cfg.Host, cfg.Port, cfg.Timeout, cfg.Debug)
    // Host=prod.example.com Port=8080 Timeout=30 Debug=false
}
```

**Explanation:**
`s.FieldByName(name)` returns a zero `reflect.Value` when the field does not exist. `f.IsValid()` is the correct check for a zero `reflect.Value`. `f.CanSet()` is false for unexported fields. The `ConvertibleTo` check handles the case where the default map has an untyped `int` literal (which defaults to `int`) but the field is declared as a different integer type. The `!f.IsZero()` check is the "don't overwrite" guard.

</details>

---

## Exercise 5: go:generate with stringer [🔴 Hard] [3 pts]

### Context
`go generate` is the compile-time alternative to runtime reflection for repetitive code generation. The `stringer` tool is the canonical example: it generates `String()` methods for integer-typed constants, saving both boilerplate writing and runtime reflection overhead.

### Task
1. Create a file `priority.go` in a new directory (`go mod init`) with:
   - A `//go:generate` directive targeting `stringer`
   - A `Priority int` type with at least four constants: `Low`, `Normal`, `High`, `Critical` (using `iota`)
2. Install `stringer` if needed: `go install golang.org/x/tools/cmd/stringer@latest`
3. Run `go generate ./...` to generate `priority_string.go`
4. Write a `main` function that prints all four `Priority` constants and demonstrates that `fmt.Println` uses the generated `String()` method

### Requirements
- [ ] The `//go:generate` directive is a standalone comment at the top of `priority.go`
- [ ] `Priority` uses `iota` for its four constants
- [ ] Running `go generate ./...` produces a `priority_string.go` file without errors
- [ ] The generated file has the `// Code generated by stringer` header comment
- [ ] `fmt.Println(Low)` prints `"Low"`, not `"0"`
- [ ] The generated `String()` method does not use `reflect` internally

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

The `//go:generate` directive must start at column zero — no leading space. The format is:
```go
//go:generate stringer -type=Priority
```
This tells `go generate` to run `stringer -type=Priority` in the package directory. The `-output` flag is optional; by default, stringer writes `priority_string.go`.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

After running `go generate`, open `priority_string.go` and find the compile-time array bounds check:
```go
var _ [1]struct{} = [...]struct{}{}[Priority(0):]
```
or similar. This is the generated code's compile-time safety net: if you add a constant without regenerating, this line fails to compile. That is intentional — it forces regeneration when the type changes.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

The full `priority.go` should look like:
```go
//go:generate stringer -type=Priority

package main

import "fmt"

type Priority int

const (
    Low      Priority = iota
    Normal
    High
    Critical
)

func main() {
    for _, p := range []Priority{Low, Normal, High, Critical} {
        fmt.Println(p)
    }
}
```

Run `go generate ./...`, then `go run .`.

</details>

### Expected Output / Acceptance Criteria
After generating and running:
```
Low
Normal
High
Critical
```

**Key acceptance criterion:** The output uses the constant names, not integers. Inspect `priority_string.go` to confirm it uses a string table and a switch/index — not `reflect` or `fmt.Sprintf("%d")`.

### Solution
<details>
<summary>Show Solution</summary>

```go
// priority.go

//go:generate stringer -type=Priority

package main

import "fmt"

// Priority represents a task priority level.
type Priority int

const (
    Low      Priority = iota // 0
    Normal                   // 1
    High                     // 2
    Critical                 // 3
)

func main() {
    priorities := []Priority{Low, Normal, High, Critical}
    for _, p := range priorities {
        fmt.Printf("Value %d = %s\n", int(p), p)
    }
}
```

After `go generate ./...`, the generated `priority_string.go` will look approximately like:

```go
// Code generated by "stringer -type=Priority"; DO NOT EDIT.

package main

import "strconv"

func _() {
    // Compile-time check that constants haven't changed
    var x [1]struct{}
    _ = x[Low-0]
    _ = x[Normal-1]
    _ = x[High-2]
    _ = x[Critical-3]
}

const _Priority_name = "LowNormalHighCritical"

var _Priority_index = [...]uint8{0, 3, 9, 13, 21}

func (i Priority) String() string {
    if i < 0 || i >= Priority(len(_Priority_index)-1) {
        return "Priority(" + strconv.FormatInt(int64(i), 10) + ")"
    }
    return _Priority_name[_Priority_index[i]:_Priority_index[i+1]]
}
```

**Step-by-step explanation:**

1. The `//go:generate` directive tells `go generate` exactly what command to run — `stringer -type=Priority`. The tool scans the package, finds the `Priority` type and its `iota` constants, and writes the generated file.
2. The generated `String()` uses a packed string constant and an index slice — the fastest possible string lookup with no allocations.
3. The compile-time check `_ = x[Low-0]` is an array bounds check: if `Low != 0`, this fails to compile, ensuring the generated file is always in sync with the constants.
4. The `main` function uses `%s` format (which calls `String()`) to prove the generated method is in effect.

**Why this approach:**
Code generation is superior to reflection for this use case because: (a) zero runtime overhead, (b) compile-time type safety, (c) the generated code is readable and debuggable, (d) the compile-time check prevents stale generated code from silently misbehaving.

**What a weaker solution looks like and why it fails:**
A reflection-based stringer that iterates a list of constants and compares integer values would work but requires maintaining a runtime data structure, calls reflect machinery on every `String()` invocation, and provides no compile-time safety if a constant is added without updating the function.

</details>

---

## Exercise 6: Generic Printer vs Reflect Printer [🔴 Hard] [3 pts]

### Context
One of the most important skills in modern Go is knowing when to reach for reflection versus generics. Since Go 1.18, many tasks that previously required reflection can be expressed as generic functions — with full compile-time type safety and better performance. This exercise asks you to implement the same task two ways and compare them.

### Task
Implement `PrintSlice` in two versions:

**Version A (reflection):** `func PrintSliceReflect(v interface{})` — accepts any slice via `interface{}`, uses `reflect.ValueOf` and `reflect.Value.Index` to iterate, and prints each element.

**Version B (generics):** `func PrintSlice[T any](s []T)` — accepts any slice as a type-parameterized function.

Call both versions with a `[]int`, a `[]string`, and a `[]float64`. Then write a brief comment in your code (3–5 lines) explaining: in what situations would you still choose the reflect version over the generic version?

### Requirements
- [ ] Version A uses `reflect.ValueOf(v)`, checks `Kind() == reflect.Slice`, and uses `.Len()` and `.Index(i).Interface()` to iterate
- [ ] Version B uses a type parameter `[T any]` and a standard `range` loop
- [ ] Both versions produce identical output for the same input
- [ ] The code compiles on Go 1.22+
- [ ] The comment explains at least one scenario where reflection is genuinely preferable

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

For the reflect version: `rv := reflect.ValueOf(v)`, then check `rv.Kind() == reflect.Slice`, then `for i := 0; i < rv.Len(); i++ { fmt.Println(rv.Index(i).Interface()) }`.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

The generic version is strictly simpler and faster. But the generic version requires the caller to know the slice type at compile time. The reflect version accepts `interface{}` — useful when you receive data from a JSON decoder or database scanner that returns `[]interface{}` or some other dynamically typed collection.

</details>

### Expected Output / Acceptance Criteria
Both versions should print identical output for each slice type. The comment should identify at least one real scenario (e.g., "when the slice type is only known at runtime, such as after JSON unmarshaling into interface{}").

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "reflect"
)

// Version A: Reflection-based — accepts any slice as interface{}
func PrintSliceReflect(v interface{}) {
    rv := reflect.ValueOf(v)
    if rv.Kind() != reflect.Slice {
        fmt.Println("(not a slice)")
        return
    }
    for i := 0; i < rv.Len(); i++ {
        fmt.Println(rv.Index(i).Interface())
    }
}

// Version B: Generic — compile-time type safety, no reflection
func PrintSlice[T any](s []T) {
    for _, elem := range s {
        fmt.Println(elem)
    }
}

// When to prefer reflection over generics:
// 1. When the concrete type is only known at runtime (e.g., value came from
//    json.Unmarshal into interface{} or from a plugin loaded via os/exec).
// 2. When writing a framework that must handle user-defined types it cannot
//    import at compile time (e.g., an ORM mapping []MyRow where MyRow is
//    defined by the user, not the library).
// 3. When the value is already in interface{} form and a type assertion to the
//    specific slice type would require a large type switch.

func main() {
    ints := []int{1, 2, 3}
    strs := []string{"a", "b", "c"}
    floats := []float64{1.1, 2.2, 3.3}

    fmt.Println("--- Reflect version ---")
    PrintSliceReflect(ints)
    PrintSliceReflect(strs)
    PrintSliceReflect(floats)

    fmt.Println("--- Generic version ---")
    PrintSlice(ints)
    PrintSlice(strs)
    PrintSlice(floats)
}
```

**Step-by-step explanation:**

1. The reflect version uses `rv.Kind() == reflect.Slice` to guard against non-slice inputs, then `rv.Len()` and `rv.Index(i).Interface()` to iterate and extract elements.
2. The generic version is a single-line range loop — cleaner, faster, and type-safe.
3. The key difference is call-site ergonomics: `PrintSlice(ints)` (generic) vs `PrintSliceReflect(ints)` (reflect). Both work, but the generic version is checked at compile time — passing `42` (not a slice) to `PrintSlice` is a compile error; passing it to `PrintSliceReflect` panics at runtime.

**Why the reflect version still has a place:**
Reflection is valuable when your code receives data from sources that are only typed as `interface{}` at runtime — JSON decoders, plugin systems, RPC frameworks. A framework cannot use generics to handle every user-defined type because it doesn't import those types. In those cases, reflection is not a shortcut but the only viable tool.

</details>

---

## Exercise 7: Method Caller via Reflection [⭐ Challenge] [5 pts]

### Context
Reflection can discover and call methods dynamically — the mechanism behind RPC frameworks, dependency injection containers, and test harnesses that call methods by name. This exercise combines method discovery, argument building, and error handling into a realistic mini-framework.

### Task
Write a function `CallMethod(obj interface{}, methodName string, args ...interface{}) ([]interface{}, error)` that:
1. Finds the method named `methodName` on `obj` (or a pointer to `obj`)
2. Validates that the number of provided `args` matches the method's expected parameter count
3. Converts each arg to a `reflect.Value` using `reflect.ValueOf`
4. Calls the method and returns its results as `[]interface{}`
5. Returns an error (not panic) if the method does not exist or the argument count is wrong

Test it with a `Calculator` struct that has methods `Add(a, b int) int` and `Greet(name string) string`.

### Requirements
- [ ] Uses `reflect.Value.MethodByName` to look up the method
- [ ] Validates argument count against `method.Type().NumIn()`
- [ ] Converts results with `result.Interface()` for each element in the returned `[]reflect.Value`
- [ ] Returns a descriptive `error` (not a panic) for method-not-found and wrong-arg-count
- [ ] Tested with at least two methods of different signatures

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
rv := reflect.ValueOf(obj)
method := rv.MethodByName(methodName)
if !method.IsValid() {
    return nil, fmt.Errorf("method %q not found", methodName)
}
```
`method.Type().NumIn()` gives the number of parameters. Build `[]reflect.Value{reflect.ValueOf(args[0]), ...}` and call `method.Call(argVals)`.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

The value returned by `rv.MethodByName` already has the receiver bound — you only need to pass the non-receiver arguments. So a method `func (c *Calculator) Add(a, b int) int` when called via `method.Call(args)` only needs `args` to contain `[a, b]`, not `[c, a, b]`.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
argVals := make([]reflect.Value, len(args))
for i, a := range args {
    argVals[i] = reflect.ValueOf(a)
}
results := method.Call(argVals)
out := make([]interface{}, len(results))
for i, r := range results {
    out[i] = r.Interface()
}
return out, nil
```

</details>

### Expected Output / Acceptance Criteria
```
Add(3, 4) = 7
Greet("World") = Hello, World!
Error: method "Divide" not found on Calculator
Error: method "Add" expects 2 args, got 1
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "reflect"
)

// CallMethod invokes a named method on obj with the given args.
// Returns the results as []interface{} or an error.
func CallMethod(obj interface{}, methodName string, args ...interface{}) ([]interface{}, error) {
    rv := reflect.ValueOf(obj)
    method := rv.MethodByName(methodName)
    if !method.IsValid() {
        return nil, fmt.Errorf("method %q not found on %T", methodName, obj)
    }

    mt := method.Type()
    if mt.NumIn() != len(args) {
        return nil, fmt.Errorf("method %q expects %d args, got %d",
            methodName, mt.NumIn(), len(args))
    }

    argVals := make([]reflect.Value, len(args))
    for i, a := range args {
        argVals[i] = reflect.ValueOf(a)
    }

    results := method.Call(argVals)
    out := make([]interface{}, len(results))
    for i, r := range results {
        out[i] = r.Interface()
    }
    return out, nil
}

type Calculator struct{ Name string }

func (c Calculator) Add(a, b int) int         { return a + b }
func (c Calculator) Greet(name string) string { return "Hello, " + name + "!" }

func main() {
    calc := Calculator{Name: "MyCalc"}

    if res, err := CallMethod(calc, "Add", 3, 4); err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Printf("Add(3, 4) = %v\n", res[0])
    }

    if res, err := CallMethod(calc, "Greet", "World"); err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Printf("Greet(\"World\") = %v\n", res[0])
    }

    if _, err := CallMethod(calc, "Divide", 10, 2); err != nil {
        fmt.Println("Error:", err)
    }

    if _, err := CallMethod(calc, "Add", 5); err != nil {
        fmt.Println("Error:", err)
    }
}
```

**Step-by-step explanation:**

1. `rv.MethodByName(methodName)` looks up the method in the value's method set. For value receivers, `rv` can be either the struct or a pointer; for pointer receivers, `rv` must be a pointer. A zero `reflect.Value` (IsValid false) is returned when the method does not exist.
2. `method.Type().NumIn()` is the expected argument count. Note that for methods retrieved via `MethodByName`, the receiver is already bound — `NumIn()` counts only the non-receiver parameters.
3. The argument conversion loop is straightforward: `reflect.ValueOf(a)` for each argument. In production code you would add type compatibility checks here.
4. `method.Call(argVals)` may panic if the argument types are wrong. Production frameworks typically use `reflect.Value.Type().AssignableTo()` to validate before calling.

**Why this approach:**
This pattern is used by `net/rpc`, `google/wire`, `testify`, and many CLI frameworks to dispatch to user-defined handlers without knowing the handler signatures at compile time. The error-return approach (instead of panicking) makes it safe to call with untrusted method names.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Read Type and Kind | — | —/1 | — | — |
| Exercise 2 — Read Struct Tags | — | —/1 | — | — |
| Exercise 3 — Struct-to-Map Serializer | — | —/2 | — | — |
| Exercise 4 — Set Fields via Reflection | — | —/2 | — | — |
| Exercise 5 — go:generate with stringer | — | —/3 | — | — |
| Exercise 6 — Generic vs Reflect Printer | — | —/3 | — | — |
| Exercise 7 — Method Caller via Reflection | — | —/5 | — | — |
| **Total** | | **—/17** | | |

**Passing threshold:** 11/17 (65%). Aim for 15/17 (88%) before taking the test.
