# Answer Key — Module 11: Testing and Benchmarking

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

### 1.1 — t.Error vs t.Fatal [1 pt]

**Full credit answer:**
`t.Error`/`t.Errorf` marks the test as failed and continues execution — subsequent lines in the test function still run. `t.Fatal`/`t.Fatalf` marks the test as failed and **stops the current test function immediately** (by calling `runtime.Goexit()`). Subsequent lines do not run.

Use `t.Fatal` when subsequent checks are meaningless if the current check fails. For example: if you check `err != nil` with `t.Fatal`, you can safely dereference the result on the next line without a nil check — you know the function succeeded because `t.Fatal` would have stopped execution otherwise.

```go
result, err := SomeFunc()
if err != nil {
    t.Fatalf("unexpected error: %v", err) // stops here if err != nil
}
// Safe to use result here — t.Fatal guarantees we only reach this line if err == nil
fmt.Println(result.Value) // no nil-pointer risk
```

**Key points required:**
- `t.Error` continues execution; `t.Fatal` stops the current test function
- Use `t.Fatal` when the rest of the test depends on the checked assertion being true

**Common wrong answers:**
- *"`t.Fatal` exits the entire test run"* — it only stops the current test function (by calling `runtime.Goexit`), not the entire `go test` process. Other tests continue to run.
- *"They are the same except for the message format"* — the execution behavior is the critical difference.

---

### 1.2 — What b.N represents [1 pt]

**Full credit answer:**
`b.N` is the number of iterations the testing framework wants the benchmark loop to run. The framework starts with a small N, measures how long the loop takes, and increases N until the total duration is long enough to produce stable, reliable measurements (typically about 1 second by default). The framework sets `b.N` — you must never set it yourself.

You should not set N yourself because the framework needs control to calibrate the measurement. If you hardcode N, you break the calibration mechanism and may measure setup overhead rather than the operation itself. Your only job is to write the loop correctly: `for i := 0; i < b.N; i++ { /* one unit of work */ }`.

**Key points required:**
- `b.N` is set by the testing framework, not the programmer
- The framework increases N until the benchmark runs long enough for stable results

---

### 1.3 — Running tests matching a pattern [1 pt]

**Full credit answer:**
Use the `-run` flag with a regular expression. The command to run only tests containing "Parse" is:

```bash
go test -run Parse ./...
```

Or more precisely, to match any test whose name contains "Parse" (not just starts with it):

```bash
go test -run TestParse ./...
```

The `-run` flag accepts a regular expression matched against the test name. Subtests can be filtered with a slash: `go test -run TestFoo/subtest_name`. The pattern is matched as a substring (not anchored), so `-run Parse` matches `TestParseDate`, `TestParseURL`, etc.

**Key points required:**
- `-run` flag with a regex pattern
- The correct command: `go test -run Parse ./...` (or `TestParse` for more precision)

---

### 1.4 — t.Helper() [1 pt]

**Full credit answer:**
`t.Helper()` marks the calling function as a test helper. When a test fails inside a helper function, Go uses the caller's source location in the failure message instead of the helper's location. Without `t.Helper()`, failure messages point to a line inside the helper function — which tells you nothing about which test or which test case triggered the failure. With `t.Helper()`, the message points to the line in the test function that called the helper.

Call `t.Helper()` as the first line of any function that calls `t.Error`, `t.Fatal`, or their variants and is intended to be used from test functions.

**Key points required:**
- Redirects failure message source location to the caller, not the helper
- Should be the first line of any test helper that reports failures

---

### 1.5 — Naming conventions [1 pt]

**Full credit answer:**
- **Test files:** must end in `_test.go` (e.g., `calculator_test.go`)
- **Test functions (unit tests):** `func TestXxx(t *testing.T)` — `Xxx` must start with an uppercase letter
- **Benchmark functions:** `func BenchmarkXxx(b *testing.B)`
- **Fuzz test functions:** `func FuzzXxx(f *testing.F)` (Go 1.18+)
- **Example functions** (bonus): `func ExampleXxx()` with optional `// Output:` comment

Test files may use `package foo` (same package, white-box) or `package foo_test` (external package, black-box).

**Key points required:**
- `_test.go` file suffix
- `TestXxx(t *testing.T)`, `BenchmarkXxx(b *testing.B)`, `FuzzXxx(f *testing.F)`

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Fakes vs mock frameworks [2 pts]

**Full credit answer:**
Go's community prefers hand-written fakes because Go's **structural typing** (interfaces are satisfied implicitly — no `implements` keyword) makes fakes trivial to write and maintain. A fake is simply a struct that implements the required interface's methods. There is no code generation step, no framework to import, and no mock DSL to learn.

With a mock framework like `gomock`, tests describe expected calls in a domain-specific language (`ctrl.EXPECT().SendEmail(gomock.Any(), ...).Return(nil)`). This coupling tests to call sequences rather than observable behavior, produces opaque failure messages when expectations aren't met, and makes tests brittle — changing how the production code calls the dependency (even if the end behavior is the same) breaks the test.

A hand-written fake is just Go:

```go
type fakeSender struct{ sent int }
func (f *fakeSender) SendEmail(to, subject, body string) error {
    f.sent++
    return nil
}
```

It is readable, debuggable, and only records what the test actually needs to assert.

**Rubric:**
- 2 pts: Explains structural typing as the enabling mechanism, explains why fakes are preferred over mocking DSLs (fragility, readability, or failure message quality), and demonstrates the concept
- 1 pt: Knows fakes are preferred and gives a reason, but doesn't connect it to Go's interface semantics
- 0 pts: Says Go uses mock frameworks by default, or cannot explain the preference

---

### 2.2 — Loop variable capture bug [2 pts]

**Full credit answer:**
In Go versions before 1.22, the range variable (e.g., `tt` in `for _, tt := range tests`) is a single variable that is reassigned on each iteration — not a new variable per iteration. When a `t.Run` subtest calls `t.Parallel()`, the subtest body does not execute immediately; it is queued to run concurrently after the current goroutine continues. By the time the subtest body runs, the loop has finished and `tt` holds the value of the last test case.

The symptom: all parallel subtests test the same case (the last one), so failures are reported only for that case even when other cases would also fail.

The fix is to create a new variable scoped to each loop iteration before the `t.Run` call:

```go
for _, tt := range tests {
    tt := tt  // shadow with a new variable per iteration
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel()
        // tt is now a distinct copy, not a shared reference
    })
}
```

Go 1.22 fixes this by making loop variables have per-iteration scope by default. For code targeting older toolchains, the `tt := tt` fix is required.

**Rubric:**
- 2 pts: Correctly explains why it happens (single variable reused across iterations), what symptom it causes (all subtests test last case), and what the fix is (`tt := tt` shadowing)
- 1 pt: Knows the fix but can't explain why the bug occurs
- 0 pts: Doesn't know about the bug or gives incorrect explanation

---

### 2.3 — -run FuzzXxx vs -fuzz FuzzXxx [2 pts]

**Full credit answer:**
`go test -run FuzzXxx` runs the fuzz function's **seed corpus only** — the inputs you explicitly provided with `f.Add(...)`. Each seed entry becomes one test case, executed like a normal unit test. This is fast (milliseconds), deterministic, and suitable for running in CI.

`go test -fuzz FuzzXxx` actively fuzzes: the engine generates new mutated inputs based on the seed corpus, using coverage feedback to guide mutations toward uncovered code paths. It runs until `-fuzztime` elapses or a failing input is found. This is slow (runs until stopped), non-deterministic, and typically run separately from the main test suite.

Use `-run FuzzXxx` in CI to ensure the seed corpus and any previously-found crashers (stored in `testdata/fuzz/FuzzXxx/`) still pass. Use `-fuzz FuzzXxx` when you want to actively search for new bugs.

**Rubric:**
- 2 pts: Correctly describes both modes (seed corpus vs active fuzzing), their speed/determinism characteristics, and gives guidance on when to use each
- 1 pt: Knows they are different but conflates the behaviors or cannot explain when to use each
- 0 pts: Doesn't know the difference

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Table-driven test for Sqrt [3 pts]

**Full credit answer:**

```go
package mathutil_test

import (
    "fmt"
    "math"
    "testing"
)

func TestSqrt(t *testing.T) {
    tests := []struct {
        name    string
        input   float64
        want    float64
        wantErr bool
    }{
        {"perfect square", 9.0, 3.0, false},
        {"fractional result", 2.0, math.Sqrt2, false},
        {"zero", 0.0, 0.0, false},
        {"negative number", -1.0, 0, true},
        {"large number", 1e12, 1e6, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Sqrt(tt.input)
            if (err != nil) != tt.wantErr {
                t.Fatalf("Sqrt(%v) error = %v; wantErr %v", tt.input, err, tt.wantErr)
            }
            if tt.wantErr {
                return
            }
            // Use a tolerance for floating-point comparison
            if math.Abs(got-tt.want) > 1e-9 {
                t.Errorf("Sqrt(%v) = %v; want %v", tt.input, got, tt.want)
            }
        })
    }
}
```

**Key requirements for full credit:**
- `[]struct{...}` table with at least 4 cases
- `t.Run(tt.name, ...)` subtests
- `(err != nil) != tt.wantErr` error check with `t.Fatalf`
- `return` after confirming expected error
- Floating-point comparison with tolerance (exact equality `==` is wrong for floats)

**Rubric:**
- 3 pts: Correct table structure; all 4 required cases covered; correct error pattern; uses float tolerance for comparison; compiles correctly
- 2 pts: Correct structure but uses exact float equality (which may be fragile), or missing the early return after error case
- 1 pt: Uses `t.Fatalf` in the loop without `t.Run` (stops at first failure), or table structure is fundamentally wrong
- 0 pts: No table structure; individual test functions per case

**Acceptable alternatives:**
- More cases (> 4) — always acceptable
- Different tolerance value (1e-6 etc.) — acceptable as long as it is not `== 0`
- Using `math.IsNaN` if the implementation could return NaN — acceptable

---

### 3.2 — Benchmark for Lookup implementations [3 pts]

**Full credit answer:**

```go
package lookup_test

import (
    "fmt"
    "testing"
)

// buildSlice creates a slice of 1000 key-value pairs
func buildSlice(n int) [][2]string {
    pairs := make([][2]string, n)
    for i := range pairs {
        pairs[i] = [2]string{fmt.Sprintf("key%d", i), fmt.Sprintf("val%d", i)}
    }
    return pairs
}

// buildMap creates a map with 1000 entries
func buildMap(n int) map[string]string {
    m := make(map[string]string, n)
    for i := 0; i < n; i++ {
        m[fmt.Sprintf("key%d", i)] = fmt.Sprintf("val%d", i)
    }
    return m
}

// BenchmarkLookupSlice measures linear search in a slice
// Expected: O(n) — slower as n grows, especially for keys near the end
func BenchmarkLookupSlice(b *testing.B) {
    pairs := buildSlice(1000)
    target := "key500" // middle of the slice
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = LookupSlice(pairs, target)
    }
}

// BenchmarkLookupMap measures O(1) hash map lookup
// Expected: much faster than slice for large n; constant time regardless of position
func BenchmarkLookupMap(b *testing.B) {
    m := buildMap(1000)
    target := "key500"
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = LookupMap(m, target)
    }
}
```

**Rubric:**
- 3 pts: Both benchmarks call `b.ResetTimer()` after setup; setup is outside the loop; `b.N` loop is correct; a comment explains which is expected to be faster and why; compiles correctly
- 2 pts: Correct structure but missing `b.ResetTimer()`, or setup is incorrectly inside the loop
- 1 pt: One benchmark is correct; the other has a significant error
- 0 pts: Does not use `b.N` loop, or measures setup time instead of lookup time

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Broken Benchmark [3 pts] (1 pt each part)

**(a) What is wrong:**
The expensive setup (`generateItems(1000)` taking ~10ms) is **inside the benchmark loop**. This means the 10ms setup is included in every measurement iteration. The benchmark is measuring the cost of setup + ProcessItems, not just ProcessItems.

**(b) Why it produces incorrect results:**
When `generateItems` takes ~10ms and `b.N` starts at 1, the total loop time is ~10ms — which may already exceed the minimum required duration, so the framework might not increase N significantly. This produces measurements that reflect the setup cost, not the operation being benchmarked. Alternatively, the framework sees that the operation is "slow" (because of setup), keeps N low, and the ns/op number is dominated by setup overhead, giving a completely misleading picture of `ProcessItems` performance.

**(c) Correct rewrite:**
```go
func BenchmarkProcessItems(b *testing.B) {
    items := generateItems(1000) // setup OUTSIDE the loop
    b.ResetTimer()               // reset so setup time is not counted

    for i := 0; i < b.N; i++ {
        result := ProcessItems(items)
        _ = result
    }
}
```

The key change: `generateItems` is called once before the loop, and `b.ResetTimer()` is called to reset any time accumulated during setup. Now `b.N` iterations measure only `ProcessItems`.

**Rubric:**
- 1 pt for (a): Correctly identifies that setup is inside the loop (or equivalently, that it should be outside)
- 1 pt for (b): Explains why this is a problem — setup time is included in ns/op measurement, making results misleading
- 1 pt for (c): Moves setup outside the loop AND calls `b.ResetTimer()`; both are required for full credit

---

## Section 5: Discussion — Answer Key

### 5.1 — No assertion library by design [2 pts]

**Example strong answer:**
The design choice is justified and the trade-off is real. Go's `testing` package provides `t.Errorf` (print a failure message, continue) and `t.Fatalf` (print a failure message, stop) — nothing else. This forces test authors to write explicit comparisons (`if got != want`) and explicit failure messages (`t.Errorf("got %v; want %v", got, want)`).

The benefit: when a test fails, the failure message is plain Go, the comparison logic is visible in the test file, and there is no framework-specific error format to decode. The cost: more typing for common patterns like "assert these two structs are deeply equal."

Libraries like `testify/assert` provide `assert.Equal(t, want, got)` which is more concise. But the failure messages are framework-generated, the comparison uses `reflect.DeepEqual` (which has its own edge cases), and the import adds a dependency. When an assertion fails, you read framework output instead of your own message.

The trade-off is legibility vs. conciseness. The Go community has historically preferred legibility — and for teams that want more conciseness, `testify` is widely accepted in the ecosystem even though the standard library doesn't provide it.

**Elements that earn full credit:**
- Acknowledges it is a deliberate design decision with real justifications
- Explains at least one benefit of the explicit approach (failure message clarity, no DSL to learn, no dependency)
- Explains at least one cost (more verbose, especially for struct comparison)
- Compares to a concrete alternative (testify or similar)

**Rubric:**
- 2 pts: Shows genuine understanding; considers both sides; conclusion is well-reasoned
- 1 pt: One-sided (only defends the choice or only criticizes it) without engaging the trade-offs
- 0 pts: Claims Go's testing package is incomplete or that the assertion library absence is an oversight

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Fuzz test for base64 codec [+5 pts]

**Full credit answer:**

```go
package codec_test

import (
    "bytes"
    "encoding/base64"
    "testing"
)

func FuzzBase64RoundTrip(f *testing.F) {
    // Seed corpus: representative byte slice inputs
    f.Add([]byte{})            // empty slice
    f.Add([]byte("hello"))     // simple ASCII
    f.Add([]byte{0, 1, 2, 3}) // arbitrary bytes including zeros
    f.Add([]byte{255, 254})    // high bytes — exercises base64 encoding fully

    f.Fuzz(func(t *testing.T, data []byte) {
        // Invariant 1: Encode + Decode must round-trip for any input
        encoded := Encode(data)
        decoded, err := Decode(encoded)
        if err != nil {
            t.Errorf("Decode(Encode(data)) error for data=%x: %v", data, err)
            return
        }
        if !bytes.Equal(decoded, data) {
            t.Errorf("round-trip mismatch: original=%x, decoded=%x", data, decoded)
        }

        // Invariant 2: Encode of non-empty data must produce non-empty string
        if len(data) > 0 && encoded == "" {
            t.Errorf("Encode(%x) returned empty string for non-empty input", data)
        }
    })
}

// Separate fuzz test for the decode direction
func FuzzBase64Decode(f *testing.F) {
    // Seed with valid base64 strings
    f.Add(base64.StdEncoding.EncodeToString([]byte("hello")))
    f.Add("")
    f.Add("not-valid-base64!")

    f.Fuzz(func(t *testing.T, s string) {
        data, err := Decode(s)
        if err != nil {
            return // invalid base64 — correctly rejected
        }
        // Invariant: if Decode succeeds, Encode of the result must give back the same string
        reencoded := Encode(data)
        if reencoded != s {
            t.Errorf("Decode(%q) round-trip: Encode(decoded) = %q; want %q", s, reencoded, s)
        }
    })
}
```

**Which invariant is most likely to find bugs:**
The decode-direction round-trip (`Decode → Encode → same string`) is most likely to find bugs in a real codec implementation. An encoder that produces correct output can silently truncate or corrupt data on decode; the decode-direction round-trip catches that. In practice, real bugs in base64 implementations are often in the decoder (mishandling padding `=` characters, incorrect byte alignment, off-by-one in block processing) — all of which would be found by `FuzzBase64Decode`.

**Rubric:**
- 5 pts: Both round-trip directions tested; `f.Add` with appropriate types (`[]byte` for encode direction, `string` for decode direction); correct invariants stated and asserted; correct handling of invalid inputs in decode direction; explains which invariant is most valuable
- 3 pts: One direction correctly fuzzed with correct invariants; minor gap in the other direction or the explanation
- 1 pt: Basic fuzz test structure present but invariants are incomplete or incorrect
- 0 pts: No meaningful fuzz test written

**Bonus teaching note:**
This question tests whether the learner can identify good fuzz invariants, not just copy the syntax. The key insight is that round-trip tests in both directions are stronger than one-direction tests. A student who scores full marks here understands that fuzzing is about stating properties that must always hold, not just testing specific inputs.

---

## Common Wrong Answers Across the Test

These are patterns seen frequently when students haven't fully internalized the material:

1. **Confusing `t.Fatal` scope** — Students say `t.Fatal` stops the entire test run. It stops only the current test function (by calling `runtime.Goexit()`). Other tests continue. Students who make this mistake need to re-read the `t.Error` vs `t.Fatal` section and specifically the note about `runtime.Goexit`.

2. **Missing `b.ResetTimer()` after setup** — Students move setup outside the loop (correct) but forget `b.ResetTimer()`. Without the reset, any time spent in setup (even if outside the loop) is still counted if it happened between `b.StartTimer()` (implicit at function entry) and the loop start. Always call `b.ResetTimer()` after any significant setup, even when the setup is outside the loop.

3. **Treating `go test -run FuzzXxx` and `go test -fuzz FuzzXxx` as equivalent** — Many students conflate these. `-run` runs the seed corpus as normal tests (fast, deterministic, always run in CI). `-fuzz` actively generates new inputs (slow, non-deterministic, run separately). The difference is fundamental to how you use fuzzing in practice.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 typically understand the API but not the design rationale. Recommend re-reading the "Testing with Interfaces and Hand-Written Fakes" section with the specific goal of being able to explain why — not just how.
- Students who struggle with Section 3 (benchmark question) almost always forget `b.ResetTimer()`. Send them back to the Benchmarks section with the explicit instruction: "Read the b.ResetTimer subsection and then re-attempt 3.2."
- Section 4 (the broken benchmark) is a diagnostic question. A student who cannot identify the problem likely doesn't understand what `b.N` measures. Recommend Exercise 3 from EXERCISES.md, which requires running benchmarks and observing output.
- The bonus question (base64 fuzz) tests whether the learner can identify invariants independently, not just copy fuzz test syntax. Students who can explain the decode-direction invariant demonstrate genuine understanding of fuzz testing's purpose.
- A score below 60% (below 13/22) typically indicates the interfaces prerequisite is not solid. Ask the student to explain, in their own words, how a hand-written fake satisfies an interface. If they cannot, send them back to [[go/6. Methods and Interfaces]] before continuing.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
