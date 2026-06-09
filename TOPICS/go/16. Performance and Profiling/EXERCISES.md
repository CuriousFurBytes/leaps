# Exercises — Module 16: Performance and Profiling

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read the code mentally — actually write and run it.
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

## Exercise 1: Spot the Broken Benchmark [🟢 Easy] [1 pt]

### Context
A trustworthy benchmark requires two things many developers skip: protecting the result from dead-code elimination, and excluding setup from the measurement window with `b.ResetTimer`. This exercise focuses on recognizing both bugs in a realistic benchmark.

### Task
The following benchmark is broken in two ways. Identify both bugs, explain what each causes, and write the corrected version.

```go
package main

import (
    "strings"
    "testing"
)

func normalizeInput(s string) string {
    return strings.TrimSpace(strings.ToLower(s))
}

func BenchmarkNormalize(b *testing.B) {
    // Setup: build a realistic input
    input := strings.Repeat("  Hello World  ", 100)

    for i := 0; i < b.N; i++ {
        normalizeInput(input) // result not used
    }
}
```

### Requirements
- [ ] Identify Bug 1: dead-code elimination (result discarded)
- [ ] Identify Bug 2: setup is included in the measurement window (missing `b.ResetTimer`)
- [ ] Write a corrected version that uses a package-level sink and calls `b.ResetTimer` correctly
- [ ] Explain in a comment why `_ = result` is NOT sufficient to prevent DCE

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The Go compiler can optimize away a function call whose return value is not used and which has no side effects. Assigning to `_` is syntactically a discard — the compiler treats it identically to not assigning at all. You need a package-level variable that "escapes" the compiler's ability to prove the value is unused.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The fix for DCE: declare `var sink string` at package level (outside any function). Assign `sink = result` after the loop. For ResetTimer: `b.ResetTimer()` must be called after all setup and before the `for range b.N` loop.

</details>

### Expected Output / Acceptance Criteria
The corrected benchmark should:
1. Call `b.ResetTimer()` after building `input` and before the loop
2. Assign the function result to a local variable inside the loop
3. Assign that local to a package-level `sink` variable after the loop

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import (
    "strings"
    "testing"
)

func normalizeInput(s string) string {
    return strings.TrimSpace(strings.ToLower(s))
}

// Package-level sink: the compiler cannot prove this is unused
// because it is accessible from other packages (exported) or escapes
// via package-scope. Prevents dead-code elimination of normalizeInput.
var sink string

func BenchmarkNormalize(b *testing.B) {
    // Setup: build a realistic input (excluded from measurement)
    input := strings.Repeat("  Hello World  ", 100)

    b.ResetTimer() // start measuring HERE — setup above is excluded

    var result string
    for range b.N {
        result = normalizeInput(input) // result is used — DCE cannot eliminate call
    }
    sink = result // prevent DCE: force result to be "observed"
}
```

**Explanation:**
Bug 1 (DCE): `normalizeInput(input)` with no assignment — the compiler sees the return value is never used, and since `normalizeInput` has no side effects, it elides the call entirely. The benchmark reports ~0.3 ns/op (loop overhead) instead of ~150 ns/op. Fix: assign to a local `result` and then to a package-level `sink`. The compiler cannot eliminate a store to a package-level variable because it cannot prove no other code reads it.

Bug 2 (setup in measurement): `input := strings.Repeat(...)` runs before the measurement loop with no `ResetTimer`. For `b.N=1` (first probe iteration), setup dominates the time. The framework calibrates `b.N` based on a falsely slow single iteration, producing inaccurate results. Fix: call `b.ResetTimer()` after all setup.

**Common wrong answers and why they fail:**
- Using `_ = normalizeInput(input)` — assigning to `_` is syntactically a discard; the compiler still eliminates the call
- Putting `b.ResetTimer()` inside the loop — this resets the timer on every iteration, making measurement meaningless

</details>

---

## Exercise 2: Read Escape Analysis Output [🟢 Easy] [1 pt]

### Context
`go build -gcflags='-m'` is the primary tool for understanding where variables escape to the heap. This exercise trains you to read that output and correlate it to source code.

### Task
Given the following program, predict which variables will escape to the heap before running `go build -gcflags='-m'`. Then run the command, compare your prediction to the actual output, and explain each escape.

```go
package main

import "fmt"

type Point struct{ X, Y float64 }

// Returns a pointer — does p escape?
func newPoint(x, y float64) *Point {
    p := Point{X: x, Y: y}
    return &p
}

// Returns a value — does p escape?
func makePoint(x, y float64) Point {
    p := Point{X: x, Y: y}
    return p
}

// Stores in interface — does val escape?
func storeInterface(val int) any {
    return val
}

func main() {
    p1 := newPoint(1, 2)
    p2 := makePoint(3, 4)
    v := storeInterface(42)
    fmt.Println(p1, p2, v)
}
```

### Requirements
- [ ] Predict which of `p` in `newPoint`, `p` in `makePoint`, and `val` in `storeInterface` will escape, before running the command
- [ ] Run `go build -gcflags='-m'` and capture the output
- [ ] For each escape the compiler reports, write one sentence explaining the cause

### Hints
<details>
<summary>Hint 1</summary>

Three causes of escape to watch for here: (1) returning a pointer to a local variable forces it to outlive the function frame; (2) passing a value as `any` (interface) causes the value to be heap-copied because the interface stores a pointer to the value; (3) returning a value (not a pointer) does NOT force an escape — the caller's stack frame can hold it.

</details>

### Expected Output / Acceptance Criteria
Your explanation should correctly identify:
- `p` in `newPoint` escapes (pointer returned — outlives function frame)
- `p` in `makePoint` does NOT escape (returned by value)
- `val` in `storeInterface` escapes (stored in interface — interface boxing)

### Solution
<details>
<summary>Show Solution</summary>

```bash
$ go build -gcflags='-m' escape_demo.go
./escape_demo.go:11:2: &p escapes to heap
./escape_demo.go:10:4: moved to heap: p
./escape_demo.go:22:17: val escapes to heap
./escape_demo.go:28:14: p1 escapes to heap    # fmt.Println takes interface{}
./escape_demo.go:28:18: p2 escapes to heap    # same
./escape_demo.go:28:22: v escapes to heap     # same
```

**Explanation:**
- `p` in `newPoint`: `&p` is returned — the pointer escapes the function scope, so `p` must live on the heap (the caller holds the pointer after `newPoint` returns)
- `p` in `makePoint`: returned by value — the `Point` struct is copied to the caller's stack frame; no escape
- `val` in `storeInterface`: stored in `any` — an interface value stores a (type, pointer) pair; a concrete value assigned to an interface is heap-copied so the interface can hold a pointer to it
- `p1`, `p2`, `v` in `main`: `fmt.Println` takes `...any` — all arguments are boxed into interfaces, triggering escapes for each

</details>

---

## Exercise 3: Profile a Function with pprof [🟡 Medium] [2 pts]

### Context
Capturing a CPU profile during a benchmark and reading the output with `go tool pprof` is the core profiling workflow. This exercise walks you through the full cycle: benchmark → profile → read → identify hotspot.

### Task
Write a function `processLines(lines []string) []string` that, for each line: trims whitespace, converts to lowercase, and prepends `"[done] "`. Then:
1. Write a benchmark for it with a realistic input (1000 lines of ~50 chars each)
2. Run the benchmark with `-cpuprofile=cpu.out`
3. Open the profile with `go tool pprof cpu.out` and run `top5`
4. Report what the top-3 functions are and why they appear

### Requirements
- [ ] `processLines` produces correct output (trim + lowercase + prefix)
- [ ] Benchmark uses a package-level sink and calls `b.ResetTimer` correctly
- [ ] Profile is captured with `go test -bench=. -cpuprofile=cpu.out ./...`
- [ ] `top5` output is copied into a comment or noted in your answer
- [ ] At least one hotspot is correctly explained (e.g., string allocation from `+`)

### Hints
<details>
<summary>Hint 1</summary>

Generate the 1000-line input in the benchmark setup, before `b.ResetTimer`. Each line can be `fmt.Sprintf("  Line number %04d with some extra text here  ", i)`. This makes the input realistic: mixed whitespace, mixed case.

</details>

<details>
<summary>Hint 2</summary>

After capturing `cpu.out`, run: `go tool pprof cpu.out` then type `top5` at the prompt. The output will likely show `runtime.mallocgc`, `strings.ToLower`, and `strings.TrimSpace` or similar. `mallocgc` appearing near the top indicates the function is allocation-heavy.

</details>

### Expected Output / Acceptance Criteria
The function should produce correct output. The profile `top5` should show:
- `runtime.mallocgc` or allocation-related functions (from `"[done] " + line` string concatenation)
- `strings.ToLower` and/or `strings.TrimSpace`

Your answer should name the dominant cost and explain it (string `+` allocates a new string each call).

### Solution
<details>
<summary>Show Solution</summary>

```go
// process.go
package process

import "strings"

func processLines(lines []string) []string {
    result := make([]string, len(lines))
    for i, line := range lines {
        trimmed := strings.TrimSpace(line)
        lower := strings.ToLower(trimmed)
        result[i] = "[done] " + lower // string + allocates a new string
    }
    return result
}
```

```go
// process_test.go
package process

import (
    "fmt"
    "testing"
)

var sink []string

func BenchmarkProcessLines(b *testing.B) {
    // Setup: 1000 realistic lines
    lines := make([]string, 1000)
    for i := range lines {
        lines[i] = fmt.Sprintf("  Line number %04d with SOME Mixed Case Text  ", i)
    }

    b.ResetTimer() // exclude setup from measurement

    var result []string
    for range b.N {
        result = processLines(lines)
    }
    sink = result
}
```

```bash
# Capture CPU profile
go test -bench=BenchmarkProcessLines -cpuprofile=cpu.out ./...

# Analyze
go tool pprof cpu.out
(pprof) top5
```

Expected `top5` output (approximate):
```
      flat  flat%   sum%        cum   cum%
     0.41s 32.54% 32.54%      0.41s 32.54%  runtime.mallocgc
     0.28s 22.22% 54.76%      0.28s 22.22%  strings.ToLower
     0.19s 15.08% 69.84%      0.19s 15.08%  strings.TrimSpace
     0.18s 14.29% 84.13%      1.26s   100%  process.processLines
     0.07s  5.56% 89.68%      0.07s  5.56%  runtime.memmove
```

**Hotspot explanation:**
`runtime.mallocgc` dominates because `"[done] " + lower` creates a new heap-allocated string on every iteration. For 1000 lines, that is 1000 allocations per benchmark call. The fix is to use a `strings.Builder` or `fmt.Sprintf` — but actually, for this pattern, `"[done] " + lower` allocates precisely once per line, which is hard to eliminate without pre-allocated byte buffers. A more impactful optimization is to preallocate `result` with `make([]string, 0, len(lines))` (already done here) and to batch the prefix addition using a `strings.Builder` per line.

</details>

---

## Exercise 4: Reduce Allocations Using Escape Analysis [🟡 Medium] [2 pts]

### Context
Escape analysis output directly shows you what to fix. This exercise requires you to read `-gcflags=-m` output for a function that unnecessarily allocates, redesign the function to keep values on the stack, and confirm the fix with both `-gcflags=-m` and `-benchmem`.

### Task
The following function returns a pointer to a small struct (an `Options` value). It is called in a hot loop, creating one heap allocation per call.

1. Run `go build -gcflags='-m'` to confirm the escape
2. Rewrite the function to eliminate the escape (return a value instead of a pointer)
3. Confirm the fix eliminates the escape with `-gcflags=-m`
4. Write a benchmark comparing the two versions with `-benchmem` to show the allocation difference

```go
package main

type Options struct {
    MaxRetries int
    Timeout    int
    Debug      bool
}

func defaultOptions() *Options {
    return &Options{MaxRetries: 3, Timeout: 30, Debug: false}
}

func doWork(opts *Options) int {
    // Simulates using opts
    return opts.MaxRetries * opts.Timeout
}
```

### Requirements
- [ ] Run `go build -gcflags='-m'` and show the "escapes to heap" line for the original
- [ ] Rewrite `defaultOptions` to return `Options` (not `*Options`)
- [ ] Confirm the rewrite eliminates the heap escape with `-gcflags='-m'`
- [ ] Benchmark both versions with `-benchmem`; the fixed version should show `0 allocs/op`

### Hints
<details>
<summary>Hint 1</summary>

To return a value: change the signature to `func defaultOptions() Options { return Options{...} }`. The caller takes its address: `opts := defaultOptions(); doWork(&opts)`. The stack-allocated `opts` remains valid as long as `doWork` doesn't store the pointer somewhere that outlives the call.

</details>

<details>
<summary>Hint 2</summary>

In the benchmark, call `doWork` with a pointer to the local value: `opts := defaultOptions(); result = doWork(&opts)`. This gives the compiler enough information to keep `opts` on the stack (it knows the pointer stays within the benchmark function's lifetime).

</details>

### Expected Output / Acceptance Criteria
Original `-gcflags=-m` output includes: `&Options{...} escapes to heap`
Fixed `-gcflags=-m` output: no escape line for `Options`

Original benchmark: `~1 allocs/op`
Fixed benchmark: `0 allocs/op`

### Solution
<details>
<summary>Show Solution</summary>

```go
// options.go
package main

type Options struct {
    MaxRetries int
    Timeout    int
    Debug      bool
}

// Original: Options escapes to heap (pointer returned)
func defaultOptionsPtr() *Options {
    return &Options{MaxRetries: 3, Timeout: 30, Debug: false}
}

// Fixed: Options stays on caller's stack (value returned)
func defaultOptions() Options {
    return Options{MaxRetries: 3, Timeout: 30, Debug: false}
}

func doWork(opts *Options) int {
    return opts.MaxRetries * opts.Timeout
}
```

```go
// options_test.go
package main

import "testing"

var intSink int

func BenchmarkDefaultOptionsPtr(b *testing.B) {
    var result int
    for range b.N {
        opts := defaultOptionsPtr()
        result = doWork(opts)
    }
    intSink = result
}

func BenchmarkDefaultOptions(b *testing.B) {
    var result int
    for range b.N {
        opts := defaultOptions()   // stack allocated
        result = doWork(&opts)     // pass stack address — safe within function
    }
    intSink = result
}
```

```bash
$ go test -bench=. -benchmem ./...
BenchmarkDefaultOptionsPtr-8    182543021    6.54 ns/op    24 B/op    1 allocs/op
BenchmarkDefaultOptions-8      1000000000    0.89 ns/op     0 B/op    0 allocs/op
```

**Explanation:**
The pointer version forces a heap allocation because the compiler cannot guarantee the `*Options` won't be stored somewhere after `doWork` returns. The value version lets the compiler keep `Options` on the stack — `doWork` receives a pointer to the caller's stack frame, which is valid for the duration of the call. The 7× speedup and zero-allocation result come entirely from eliminating the GC-managed heap allocation.

</details>

---

## Exercise 5: strings.Builder Preallocation Optimization [🔴 Hard] [3 pts]

### Context
String concatenation in a loop is one of the most common Go performance antipatterns. This multi-step exercise requires you to implement three versions of a CSV row builder (naive, Builder, Builder with Grow), benchmark all three with `-benchmem`, and use `benchstat` to confirm statistical significance of the improvement.

### Task
Write a function `buildCSVRow(fields []string) string` that joins fields with commas (no trailing comma). Implement three versions:
1. `buildCSVRowNaive` — concatenation with `+` in a loop
2. `buildCSVRowBuilder` — using `strings.Builder` (no Grow)
3. `buildCSVRowPrealloc` — using `strings.Builder` with `Grow` pre-sized to the exact output length

Then:
- Benchmark all three with `-benchmem -count=10`
- Capture output to `before.txt` (naive) and `after.txt` (prealloc)
- Run `benchstat before.txt after.txt` and include the delta in your answer
- Confirm `buildCSVRowPrealloc` allocates exactly `1 allocs/op`

### Requirements
- [ ] All three functions produce identical, correct output for the same input
- [ ] Each benchmark uses a 20-field input (e.g., `"field_00"` through `"field_19"`) set up before `b.ResetTimer`
- [ ] `benchstat` is run on at least 10 runs per version and the delta is recorded
- [ ] `buildCSVRowPrealloc` shows `1 allocs/op` in `-benchmem` output
- [ ] The `Grow` argument in the prealloc version is the exact total byte count (sum of field lengths + len(fields)-1 commas)

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

For the naive version: `result += field; if i < len(fields)-1 { result += "," }`.

For the Builder version: call `sb.WriteString(field)` and `sb.WriteByte(',')`, with an `if` to skip the trailing comma.

For the prealloc version, compute `totalLen` before the Builder:
```go
totalLen := len(fields) - 1 // commas
for _, f := range fields { totalLen += len(f) }
sb.Grow(totalLen)
```

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

`strings.Builder.Grow(n)` allocates a buffer of at least `n` bytes upfront. If the total written bytes never exceeds `n`, `String()` performs a single allocation (to copy the internal buffer into an immutable string). Without `Grow`, `Builder` uses exponential doubling — typically 2–3 internal reallocations for a 20-field row.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

The `benchstat` invocation:
```bash
go test -bench=BenchmarkCSVNaive    -benchmem -count=10 ./... > before.txt
go test -bench=BenchmarkCSVPrealloc -benchmem -count=10 ./... > after.txt
benchstat before.txt after.txt
```

Expected delta: ~70–85% improvement in time/op, ~95% improvement in allocs/op.

</details>

### Expected Output / Acceptance Criteria
All three functions return `"field_00,field_01,...,field_19"` for a 20-field input.

Expected benchmark output (approximate):
```
BenchmarkCSVNaive-8      228591   5232 ns/op   5568 B/op   19 allocs/op
BenchmarkCSVBuilder-8    721034   1671 ns/op    768 B/op    3 allocs/op
BenchmarkCSVPrealloc-8  1204561    996 ns/op    176 B/op    1 allocs/op
```

### Solution
<details>
<summary>Show Solution</summary>

```go
// csv.go
package csv

import "strings"

// Naive: O(n²) allocations — new string per iteration
func buildCSVRowNaive(fields []string) string {
    result := ""
    for i, f := range fields {
        result += f
        if i < len(fields)-1 {
            result += ","
        }
    }
    return result
}

// Builder: amortized O(n) — exponential doubling, ~3 allocs
func buildCSVRowBuilder(fields []string) string {
    var sb strings.Builder
    for i, f := range fields {
        sb.WriteString(f)
        if i < len(fields)-1 {
            sb.WriteByte(',')
        }
    }
    return sb.String()
}

// Prealloc: single allocation — exact size known upfront
func buildCSVRowPrealloc(fields []string) string {
    totalLen := len(fields) - 1 // commas between fields
    for _, f := range fields {
        totalLen += len(f)
    }
    var sb strings.Builder
    sb.Grow(totalLen) // allocate exact buffer upfront
    for i, f := range fields {
        sb.WriteString(f)
        if i < len(fields)-1 {
            sb.WriteByte(',')
        }
    }
    return sb.String() // single allocation: copy internal buffer to string
}
```

```go
// csv_test.go
package csv

import (
    "fmt"
    "testing"
)

var strSink string

func makeFields(n int) []string {
    fields := make([]string, n)
    for i := range fields {
        fields[i] = fmt.Sprintf("field_%02d", i)
    }
    return fields
}

func BenchmarkCSVNaive(b *testing.B) {
    fields := makeFields(20)
    b.ResetTimer()
    var result string
    for range b.N {
        result = buildCSVRowNaive(fields)
    }
    strSink = result
}

func BenchmarkCSVBuilder(b *testing.B) {
    fields := makeFields(20)
    b.ResetTimer()
    var result string
    for range b.N {
        result = buildCSVRowBuilder(fields)
    }
    strSink = result
}

func BenchmarkCSVPrealloc(b *testing.B) {
    fields := makeFields(20)
    b.ResetTimer()
    var result string
    for range b.N {
        result = buildCSVRowPrealloc(fields)
    }
    strSink = result
}
```

```bash
# Capture baseline (naive)
go test -bench=BenchmarkCSVNaive -benchmem -count=10 ./... > before.txt

# Capture optimized (prealloc)
go test -bench=BenchmarkCSVPrealloc -benchmem -count=10 ./... > after.txt

# Statistical comparison
benchstat before.txt after.txt
```

Expected `benchstat` output:
```
name          old time/op    new time/op    delta
CSVNaive-8      5.23ms ± 2%    0.99ms ± 1%   -81.06%  (p=0.000 n=10+10)

name          old alloc/op   new alloc/op   delta
CSVNaive-8      5.57kB ± 0%    0.18kB ± 0%   -96.79%  (p=0.000 n=10+10)

name          old allocs/op  new allocs/op  delta
CSVNaive-8        19.0 ± 0%      1.00 ± 0%   -94.74%  (p=0.000 n=10+10)
```

**Step-by-step explanation:**
1. The naive version performs 19 string concatenations; each `result += f` copies all accumulated bytes into a new allocation (quadratic total bytes copied for n fields).
2. `strings.Builder` uses an internal `[]byte` that doubles in size when full; for 20 fields, ~3 doublings occur, meaning ~3 allocations total.
3. `Grow(totalLen)` pre-allocates the exact final size; all `WriteString` calls fit within the initial buffer, and `String()` makes one final copy from `[]byte` to immutable `string`.
4. The 81% time improvement and 95% allocation reduction are entirely from eliminating garbage — no algorithmic change was needed.

**Why this approach:**
Preallocating is strictly better than Builder without Grow for known-length outputs. Use Builder without Grow only when the output length is unknown.

**What a weaker solution looks like and why it fails:**
Using `strings.Join(fields, ",")` (which is correct and should be used in production) uses the same Grow-then-copy pattern internally. The exercise builds understanding of why it works — after this exercise, reading the `strings.Join` source will make perfect sense.

</details>

---

## Exercise 6: sync.Pool for Request Buffer Reuse [🔴 Hard] [3 pts]

### Context
`sync.Pool` eliminates repeated allocation of large, short-lived objects. This exercise requires implementing a byte-buffer pool for a request handler, measuring the allocation improvement with `-benchmem`, and understanding the subtle requirement to reset the buffer before each use.

### Task
Write a function `processPayload(data []byte) []byte` that appends a JSON header, the data, and a JSON footer (simulating a response envelope). Implement two versions:
1. `processPayloadAlloc` — allocates a new `[]byte` buffer each call
2. `processPayloadPool` — uses a `sync.Pool` to reuse buffers

Benchmark both with `-benchmem` and confirm the pool version shows significantly fewer allocations per operation.

### Requirements
- [ ] Both functions produce identical output for the same input
- [ ] The pool version uses `sync.Pool` with a `New` function that creates a `*[]byte`
- [ ] The pool version resets the buffer length to 0 (keeps capacity) before use
- [ ] The pool version copies the final result to a new allocation before returning (so the caller owns the result and can safely return the buffer to the pool)
- [ ] Benchmark uses a 512-byte payload, set up before `b.ResetTimer`

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

The pool stores `*[]byte` (pointer to slice header). On Get: `bufPtr := pool.Get().(*[]byte); buf := (*bufPtr)[:0]`. After building, copy: `result := make([]byte, len(buf)); copy(result, buf)`. On Put: `*bufPtr = buf; pool.Put(bufPtr)`.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

Why `*[]byte` not `[]byte`? A `[]byte` stored in the pool as `any` will be heap-copied (interface boxing) on every Get/Put. Storing a `*[]byte` means the pointer is boxed (8 bytes), but the large backing array is not re-boxed each time.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
var bufPool = sync.Pool{
    New: func() any {
        b := make([]byte, 0, 4096)
        return &b
    },
}
```

In the function: get → reset to `[:0]` → append header/data/footer → copy to result → put back.

</details>

### Expected Output / Acceptance Criteria
Both functions produce the same JSON envelope output.

Expected benchmark comparison:
```
BenchmarkPayloadAlloc-8    412034   2913 ns/op   1536 B/op   3 allocs/op
BenchmarkPayloadPool-8    1058921   1132 ns/op    512 B/op   1 allocs/op
```
(The pool version has 1 alloc for the result copy; the input buffer itself is reused.)

### Solution
<details>
<summary>Show Solution</summary>

```go
// payload.go
package payload

import (
    "sync"
)

var header = []byte(`{"status":"ok","data":`)
var footer = []byte(`}`)

// Alloc version: new buffer every call
func processPayloadAlloc(data []byte) []byte {
    buf := make([]byte, 0, len(header)+len(data)+len(footer))
    buf = append(buf, header...)
    buf = append(buf, data...)
    buf = append(buf, footer...)
    return buf
}

// Pool version: reuse buffer across calls
var bufPool = sync.Pool{
    New: func() any {
        b := make([]byte, 0, 4096) // initial capacity
        return &b
    },
}

func processPayloadPool(data []byte) []byte {
    // Get a buffer from pool (or allocate if pool is empty)
    bufPtr := bufPool.Get().(*[]byte)
    buf := (*bufPtr)[:0] // reset length, keep capacity

    buf = append(buf, header...)
    buf = append(buf, data...)
    buf = append(buf, footer...)

    // Copy result: caller owns the copy; buffer goes back to pool
    result := make([]byte, len(buf))
    copy(result, buf)

    // Return buffer to pool
    *bufPtr = buf
    bufPool.Put(bufPtr)

    return result
}
```

```go
// payload_test.go
package payload

import (
    "bytes"
    "testing"
)

var bSink []byte

func BenchmarkPayloadAlloc(b *testing.B) {
    payload := bytes.Repeat([]byte("x"), 512)
    b.ResetTimer()
    var result []byte
    for range b.N {
        result = processPayloadAlloc(payload)
    }
    bSink = result
}

func BenchmarkPayloadPool(b *testing.B) {
    payload := bytes.Repeat([]byte("x"), 512)
    b.ResetTimer()
    var result []byte
    for range b.N {
        result = processPayloadPool(payload)
    }
    bSink = result
}
```

**Step-by-step explanation:**
1. The alloc version creates a new `[]byte` buffer each call, even though every request needs the same ~550-byte buffer. Under load, this creates one GC-managed allocation per request.
2. The pool version reuses the buffer: Get (or allocate if pool is empty), reset length to 0 (keeping the backing array), build the response, copy to a new result slice (the caller needs to own this), return the buffer to the pool.
3. The "1 alloc" in the pool version is the `make([]byte, len(buf))` result copy — unavoidable if the caller must own the data. The buffer itself is reused.
4. Under concurrent load (realistic production conditions), the pool provides one buffer per goroutine, completely eliminating per-request buffer allocation.

**Why this approach:**
`sync.Pool` is the standard Go idiom for per-request buffer reuse. `encoding/json`, `net/http`, and many standard library packages use it internally for exactly this purpose.

**What a weaker solution looks like and why it fails:**
A global `var globalBuf []byte` would create a data race under concurrent access. The pool is goroutine-safe; a global slice without a mutex is not.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Spot the Broken Benchmark | — | —/1 | — | — |
| Exercise 2 — Read Escape Analysis Output | — | —/1 | — | — |
| Exercise 3 — Profile a Function with pprof | — | —/2 | — | — |
| Exercise 4 — Reduce Allocations (Escape Analysis) | — | —/2 | — | — |
| Exercise 5 — strings.Builder Preallocation | — | —/3 | — | — |
| Exercise 6 — sync.Pool for Buffer Reuse | — | —/3 | — | — |
| **Total** | | **—/12** | | |

**Passing threshold:** 8/12 (67%). Aim for 10/12 (83%) before taking the test.
