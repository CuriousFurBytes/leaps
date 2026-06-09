# Answer Key — Module 15: Reflection and Metaprogramming

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Copied text without understanding (you'll know)
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — TypeOf vs ValueOf [1 pt]

**Full credit answer:**
`reflect.TypeOf(x)` returns a `reflect.Type` value — a descriptor for the type of `x`. It gives you the type's name, kind, method set, struct fields, etc., but it does not hold the data itself. `reflect.ValueOf(x)` returns a `reflect.Value` — a container that holds both the type information and the actual data value. A `reflect.Value` lets you read the data (`.Int()`, `.String()`, `.Interface()`) and, if settable, modify it. The key difference: `reflect.Type` is a static description; `reflect.Value` is a live handle to a value.

**Key points required:**
- `TypeOf` → metadata about the type (no data)
- `ValueOf` → a handle holding both type info and data

**Common wrong answers:**
- *"They return the same thing"* — They do not; Type carries no data, Value carries both type and data.

---

### 1.2 — The Third Law of Reflection [1 pt]

**Full credit answer:**
The Third Law states: to modify (set) a reflection object, the value must be **settable**. Settability requires two conditions: (1) the `reflect.Value` was obtained by following a pointer — you must pass a pointer to `reflect.ValueOf` and call `.Elem()` to get the value the pointer addresses; and (2) the field must be **exported** (not unexported). Use `CanSet()` to test settability before calling any Set method.

**Key points required:**
- Must pass a pointer and call `.Elem()` (or use `FieldByName` on the Elem value)
- Field must be exported
- `CanSet()` is the runtime check

**Common wrong answers:**
- *"You just need to call CanSet() first"* — CanSet is a check, not what makes something settable; passing a pointer is what makes it settable.

---

### 1.3 — Kind vs Type [1 pt]

**Full credit answer:**
`reflect.Type` is the full, specific type — it distinguishes between `int`, `int32`, `float64`, `MyCustomInt`, `[]string`, and `map[string]int`. `reflect.Kind` is the underlying structural category — a coarser classification into ~26 buckets like `Int`, `Float64`, `Slice`, `Map`, `Struct`. A user-defined `type Celsius float64` has Type `main.Celsius` but Kind `float64` — the same Kind as `type Fahrenheit float64` and as plain `float64`, but a different Type from both.

**Key points required:**
- Type is specific (includes named type name); Kind is the underlying category
- Concrete example showing same Kind, different Type

---

### 1.4 — Reading a struct tag [1 pt]

**Full credit answer:**
Call `field.Tag.Get(key)` where `field` is a `reflect.StructField` and `key` is the tag namespace (e.g., `"json"`, `"db"`). It returns the tag value as a string — e.g., `"name,omitempty"`. It returns the **empty string** `""` if the key is absent. If you need to distinguish "key is absent" from "key is present with empty value", use `field.Tag.Lookup(key)` which returns `(string, bool)` — the bool is `false` when the key is genuinely absent.

**Key points required:**
- `Tag.Get(key)` is the method
- Returns `""` if key is absent
- Bonus: `Lookup` for the absent-vs-empty distinction

---

### 1.5 — go generate [1 pt]

**Full credit answer:**
`go generate` is a Go toolchain command that finds all `//go:generate` directive comments in the Go source files of a package and executes the specified commands as shell commands. The directive is a comment of the form `//go:generate command arg1 arg2...` placed in any `.go` file. `go generate` is **not** automatically run by `go build` or `go test` — you run it explicitly (`go generate ./...`) whenever you need to regenerate derived files. It is a convention-based code generation workflow: the directive documents what command produces a generated file, making regeneration reproducible.

**Key points required:**
- `//go:generate command` directive in source
- Run explicitly with `go generate` — not run by build automatically
- Used for generating `.go` files (String methods, mocks, protocol buffers, etc.)

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Why pointer + Elem() is required for setting [2 pts]

**Full credit answer:**
When you call `reflect.ValueOf(x)`, Go passes `x` as an `interface{}` argument. Passing to a function copies the value. The resulting `reflect.Value` holds a copy of `x` — not the original. Setting the copy has no effect on the caller's variable. Calling `SetInt` on this unaddressable copy panics with "reflect.Value.SetInt using unaddressable value" — a runtime panic, not a compile-time error.

To modify the original, you pass a pointer (`&x`). `reflect.ValueOf(&x)` gives a `reflect.Value` of kind `Pointer`. Calling `.Elem()` on it follows the pointer and returns a `reflect.Value` that represents the memory the pointer addresses — which is both addressable and settable. Now `SetInt` writes through the pointer to the original variable.

**Rubric:**
- 2 pts: Explains that passing by value copies the data (not just "you need a pointer"), explains why `.Elem()` is required, and notes the runtime-only error
- 1 pt: Correct that a pointer is needed but doesn't explain the copy-vs-original distinction
- 0 pts: Thinks `CanSet()` alone determines settability, or doesn't understand why a pointer is required

**Teaching note:**
The most common confusion is students who know the recipe (`&x` + `.Elem()`) but can't explain why. If they can't explain why, they won't know what to do in novel situations (like a struct field that's already a pointer).

---

### 2.2 — What encoding/json extracts from struct tags [2 pts]

**Full credit answer:**
`encoding/json` uses `reflect.StructField.Tag.Get("json")` on each exported field and parses the result:

1. **Key name:** The first part (before any comma) is the JSON object key name. If it's empty or the tag is absent, the field name itself is used. For example, `json:"user_id"` makes the JSON key `"user_id"` instead of `"UserID"`.

2. **`omitempty` option:** If the tag contains `,omitempty`, the field is omitted from the JSON output when its value is the zero value for its type (empty string, 0, false, nil). Example: `json:"score,omitempty"` omits the `score` key when score is 0.

3. **`"-"` skip marker:** A tag of exactly `json:"-"` causes the field to be completely excluded from marshaling and unmarshaling. Useful for fields that carry runtime state or secrets that should never appear in JSON.

**Rubric:**
- 2 pts: Names and explains at least two distinct tag behaviors (key renaming, omitempty, skip) with accurate descriptions
- 1 pt: Names one behavior correctly but misses the others, or explains them inaccurately
- 0 pts: Cannot name any specific tag behavior

---

### 2.3 — Reflection vs generics [2 pts]

**Full credit answer:**

**Reflection is better when:**
The concrete type is only known at runtime — for example, a JSON decoder that receives arbitrary data as `interface{}`, or a plugin system that loads and calls user-defined handlers. Generics require all type parameters to be resolved at compile time; if the type is genuinely runtime-only, generics cannot help. Reflection is also the right tool for code that must work with any user-defined struct that cannot be imported (e.g., an ORM library that maps user-defined row structs it has never seen).

**Generics are better when:**
You know the types at compile time but want to avoid repeating code for multiple types. `func Sum[T int | float64](s []T) T` is type-safe, fast, and readable — a reflection-based version would be slower, could panic on type mismatch at runtime, and would lose the ability to return the same type as the input. Generics also preserve IDE auto-complete and catch type errors at compile time.

**Key tradeoffs:**

| Dimension | Reflection | Generics |
|-----------|-----------|---------|
| Type checking | Runtime (can panic) | Compile time (safe) |
| Performance | 3–10× slower | Same as direct code |
| Type known at compile time? | Not required | Required |
| IDE support | Poor | Full |

**Rubric:**
- 2 pts: Gives a concrete scenario for each approach AND explains why the other approach would be worse in that scenario
- 1 pt: Identifies differences but doesn't give concrete scenarios, or gives scenarios without explaining the tradeoffs
- 0 pts: Cannot distinguish the two in practice

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — PrintStructFields [3 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string
    Age  int
}

func PrintStructFields(v interface{}) {
    rv := reflect.ValueOf(v)
    rt := reflect.TypeOf(v)

    // Normalize: dereference pointer
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
        if !field.IsExported() {
            continue
        }
        fmt.Printf("  %-12s kind=%-10s value=%v\n",
            field.Name, value.Kind(), value.Interface())
    }
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    PrintStructFields(p)
    PrintStructFields(&p) // should also work
}
```

Expected output:
```
  Name         kind=string    value=Alice
  Age          kind=int       value=30
  Name         kind=string    value=Alice
  Age          kind=int       value=30
```

**Rubric:**
- 3 pts: Handles both T and *T, skips unexported fields, prints name/kind/value for each exported field, handles non-struct gracefully
- 2 pts: Correct logic but missing one of: pointer normalization, unexported skip, or non-struct guard
- 1 pt: Iterates fields but has fundamental issues (e.g., doesn't call `.Interface()` correctly, panics on non-struct)
- 0 pts: Incorrect approach or does not compile

**Acceptable alternatives:**
Using `field.PkgPath == ""` instead of `field.IsExported()` — equivalent and acceptable (older idiom).

---

### 3.2 — ZeroFields [3 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "reflect"
)

func ZeroFields(ptr interface{}, names ...string) error {
    rv := reflect.ValueOf(ptr)
    if rv.Kind() != reflect.Pointer || rv.Elem().Kind() != reflect.Struct {
        return fmt.Errorf("ZeroFields: requires a pointer to a struct, got %T", ptr)
    }
    s := rv.Elem() // addressable struct

    for _, name := range names {
        f := s.FieldByName(name)
        if !f.IsValid() {
            continue // field not found — skip silently
        }
        if !f.CanSet() {
            continue // unexported — skip silently
        }
        f.Set(reflect.Zero(f.Type()))
    }
    return nil
}

type Config struct {
    Host    string
    Port    int
    secret  string
}

func main() {
    cfg := Config{Host: "prod.example.com", Port: 8080}
    if err := ZeroFields(&cfg, "Host", "Port", "secret", "NonExistent"); err != nil {
        fmt.Println("Error:", err)
    }
    fmt.Printf("%+v\n", cfg)
    // {Host: Port:0 secret:}
    // secret is unexported — CanSet false, silently skipped
}
```

**Rubric:**
- 3 pts: Returns error for non-pointer-to-struct input; uses `FieldByName` with `IsValid` check; uses `CanSet` check; uses `reflect.Zero(f.Type())` for zeroing
- 2 pts: Correct logic but uses panic instead of error return for invalid input, or missing one safety check
- 1 pt: Right idea but panics in normal operation (missing IsValid or CanSet)
- 0 pts: Does not solve the problem

**Key detail:** `reflect.Zero(t)` returns a `reflect.Value` representing the zero value for type `t`. This is the correct way to zero a field — not `f.Set(reflect.ValueOf(0))` which only works for int fields.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Bug Analysis [3 pts] (1 pt each part)

**(a) How many bugs and what are they:**
There are **two** distinct bugs:

**Bug 1 (lines A and B):** `cfg` is passed by value, not by pointer. `reflect.ValueOf(cfg)` receives a copy of `cfg`. The resulting `reflect.Value` is not addressable. Calling `SetInt` or `SetString` on it panics: "reflect.Value.SetInt using unaddressable value".

**Bug 2 (line C):** Even if addressability were fixed, `verbose` is an unexported field. Calling `Set` or `SetBool` on an unexported field panics: "reflect.Value.SetBool using value obtained using unexported field". `CanSet()` returns false for unexported fields.

**(b) Why runtime panics, not compile errors:**
The Go compiler does not analyze what `reflect.ValueOf` does with its argument — it only sees that a valid `interface{}` is being passed. Whether the resulting `reflect.Value` is addressable, and whether a specific field is exported, are properties that only exist at runtime. There is no static analysis that can prevent these misuses at compile time (short of a specialized linter).

**(c) Correct rewrite:**
```go
func updateConfig(cfg *AppConfig) {
    v := reflect.ValueOf(cfg).Elem() // pointer + Elem = addressable

    // MaxWorkers: exported + addressable = settable
    if f := v.FieldByName("MaxWorkers"); f.IsValid() && f.CanSet() {
        f.SetInt(8)
    }

    // LogLevel: exported + addressable = settable
    if f := v.FieldByName("LogLevel"); f.IsValid() && f.CanSet() {
        f.SetString("debug")
    }

    // verbose: unexported, CanSet() returns false — silently skipped
    if f := v.FieldByName("verbose"); f.IsValid() && f.CanSet() {
        f.SetBool(true) // this branch never executes
    }
}
```

**Rubric:**
- 1 pt for (a): Identifies both bugs — passed-by-value/unaddressable AND unexported field (must identify both for full credit)
- 1 pt for (b): Correctly explains that both checks only happen at runtime because the compiler cannot analyze reflect operations statically
- 1 pt for (c): Changes parameter to `*AppConfig`, uses `.Elem()`, uses `CanSet()` guard, skips `verbose` gracefully

---

## Section 5: Discussion — Answer Key

### 5.1 — On using reflection sparingly [2 pts]

**Example strong answer:**
I agree that reflection should be used sparingly, for three specific reasons beyond "it's slow":

First, reflection sacrifices compile-time type safety. A type mismatch, a wrong field name, or a non-settable value all produce runtime panics rather than compiler errors — bugs that only surface when the specific code path is exercised, which may be rare in testing.

Second, reflection is significantly slower: `reflect.Value.FieldByName` with a string lookup and `SetInt` is 10–30× slower than direct field access. On hot paths (inner loops, per-request operations), this matters; for initialization code (loading config once at startup), it usually doesn't.

Third, reflect-heavy code is harder to read and refactor. IDE tooling cannot trace field accesses through string arguments to `FieldByName`, so renaming a struct field doesn't automatically update reflection code.

My decision process: if the types are known at compile time and expressible as type parameters, use generics. If the behavior varies by type but the set of types is finite and known, use interfaces or a type switch. If the types are not known at all at compile time (truly arbitrary user types from a library's perspective), or if the task is "iterate all fields of any struct", reflection is correct. For repetitive code generation over known types (String() methods, mocks), use `go generate` — zero runtime cost, full compile-time safety, IDE support.

**Concrete scenario for reflection:** An ORM library mapping SQL rows to user-defined struct types it cannot import: `db.ScanRow(row, &myStruct)`. The library must work with any struct; it cannot import `myStruct`'s package. Reflection is the only tool.

**Concrete scenario against reflection:** `func Sum[T constraints.Integer](s []T) T` — a generic sum over any integer type. A reflection-based version would be 10–30× slower, could panic on non-integer input, and would return `interface{}` instead of `T`, requiring a type assertion at the call site. Generics are strictly better.

**Elements that earn full credit:**
- Names at least two specific costs beyond "it's slow" (type safety, readability, or panics)
- Provides a concrete scenario where reflection is genuinely needed
- Provides a concrete scenario where generics or interfaces are better
- Shows awareness of `go generate` as a compile-time alternative

**Rubric:**
- 2 pts: Discusses multiple specific costs; gives two concrete scenarios with clear reasoning; mentions at least one alternative approach
- 1 pt: Identifies that reflection has costs and gives one scenario, but reasoning is superficial or only one-sided
- 0 pts: Disagrees with no substantive reasoning, or only restates that reflection is "slow" without specifics

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — DeepCopy via reflection [+5 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "reflect"
)

// DeepCopy returns a deep copy of any struct value (not pointer).
// Handles nested structs recursively.
// For simplicity, does not handle maps, channels, or function fields.
func DeepCopy(src interface{}) interface{} {
    sv := reflect.ValueOf(src)
    if sv.Kind() != reflect.Struct {
        panic("DeepCopy: requires a struct value")
    }

    // Allocate a new value of the same type
    dst := reflect.New(sv.Type()).Elem()
    deepCopyStruct(dst, sv)
    return dst.Interface()
}

func deepCopyStruct(dst, src reflect.Value) {
    for i := 0; i < src.NumField(); i++ {
        srcField := src.Field(i)
        dstField := dst.Field(i)

        if !dstField.CanSet() {
            continue // skip unexported fields
        }

        switch srcField.Kind() {
        case reflect.Struct:
            // Recurse for nested structs
            deepCopyStruct(dstField, srcField)
        case reflect.Slice:
            // Bonus: copy slice contents
            if !srcField.IsNil() {
                newSlice := reflect.MakeSlice(srcField.Type(), srcField.Len(), srcField.Len())
                reflect.Copy(newSlice, srcField)
                dstField.Set(newSlice)
            }
        default:
            dstField.Set(srcField)
        }
    }
}

type Address struct {
    City    string
    Country string
}

type Person struct {
    Name    string
    Age     int
    Address Address
    Tags    []string
}

func main() {
    original := Person{
        Name:    "Alice",
        Age:     30,
        Address: Address{City: "NYC", Country: "US"},
        Tags:    []string{"admin", "user"},
    }

    copyVal := DeepCopy(original).(Person)

    // Modify copy — original must be unchanged
    copyVal.Name = "Bob"
    copyVal.Address.City = "LA"
    copyVal.Tags[0] = "guest"

    fmt.Println("Original:", original.Name, original.Address.City, original.Tags[0])
    // Alice NYC admin
    fmt.Println("Copy:    ", copyVal.Name, copyVal.Address.City, copyVal.Tags[0])
    // Bob LA guest
}
```

**Step-by-step reasoning:**
1. `reflect.New(sv.Type()).Elem()` allocates a new zero-value of the same struct type; `.Elem()` gives the settable struct value.
2. Recursing on nested struct fields ensures that nested struct copies are independent.
3. For slices, `reflect.MakeSlice` allocates a new backing array; `reflect.Copy` copies the elements — this prevents copy and original sharing the same array.
4. Unexported fields are skipped via `CanSet()` — this is correct; unexported fields are package-private by design.

**Rubric:**
- 5 pts: Correct recursive deep copy; handles nested structs; demonstrates independence of copy and original; slice copying is correct (bonus)
- 3 pts: Correct for flat structs; misses nested struct recursion or slice independence
- 1 pt: Creates a new value but uses shallow copy (`dst.Set(src)`) — does not actually deep copy nested structs
- 0 pts: Incorrect or does not compile

**Bonus teaching note:**
This question tests whether students understand that `reflect.New` + `reflect.Value.Set` does a shallow copy by default — just like assigning a struct in Go. Achieving a true deep copy requires recursion or special handling for each composite kind. Many students will write the shallow version and think it's deep; demonstrate independence of original and copy to force them to notice.

---

## Common Wrong Answers Across the Test

These are patterns seen frequently when students haven't fully internalized the material:

1. **Confusing settability with validity** — `IsValid()` checks whether a `reflect.Value` holds any value at all (a zero `reflect.Value` from a failed `FieldByName` is invalid). `CanSet()` checks whether the valid value can be modified. Students who conflate these fail to guard against `FieldByName` returning a zero value, leading to panics. See the Addressability and Settability section of the README.

2. **Thinking Kind and Type are the same** — Students use `v.Type() == reflect.TypeOf(int(0))` to check for integers, which fails for `type MyInt int`. The correct pattern is `v.Kind() == reflect.Int` (or the full switch). See Example 4 (Kind vs Type) in the README.

3. **Not knowing go generate is explicit** — Students assume `go generate` runs automatically as part of `go build`. It does not. Students who make this mistake ship code that depends on generated files without documenting the generation step, causing build failures when a colleague clones the repo without generating. The generated files must be committed, or the Makefile/CI must call `go generate` explicitly.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2.1 (pointer + Elem) need to revisit [[go/5. Pointers]] — specifically the difference between passing a value and passing a pointer, and what "addressable" means in Go. The reflect rules are a direct consequence of pointer semantics.
- Students who struggle with Section 3 need more exercise practice: send them back to EXERCISES.md exercises 3 (struct-to-map), 4 (set fields), and 7 (method caller). These are the closest analogs to the applied questions.
- The bonus question separates students who understand reflection deeply from those who know the API. A student who writes `dst.Set(src)` for the deep copy has learned the API but not the semantics. Walk them through why slice fields share backing arrays after a `Set` call.
- A score below 60% generally indicates weak prerequisite coverage. Ask whether the student is comfortable with: interface values and type assertions (from [[go/6. Methods and Interfaces]]), pointer semantics (from [[go/5. Pointers]]), and struct field declarations (from [[go/4. Composite Types]]). Any gap in these will cascade into confusion about reflection.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
