# Exercises — Module 11: Testing and Benchmarking

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read the solution — actually write and run it.
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

## Exercise 1: Table-Driven Test for a String Function [🟢 Easy] [1 pt]

### Context
Table-driven tests are the idiomatic default in Go. Before writing any other kind of test, a Go programmer should be fluent at this pattern. This exercise focuses on the core skill: writing a test file with a well-structured table, covering normal cases, edge cases, and boundary inputs.

### Task
Write a complete `reverse_test.go` file containing a table-driven test for the following function:

```go
// Reverse returns the string s with its runes in reversed order.
// It handles multi-byte UTF-8 characters correctly.
func Reverse(s string) string {
    runes := []rune(s)
    for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
        runes[i], runes[j] = runes[j], runes[i]
    }
    return string(runes)
}
```

Your test table must include at least 5 cases covering: empty string, single character, ASCII string, palindrome, and a string containing a multi-byte UTF-8 character (e.g., `"café"`).

### Requirements
- [ ] Use a `[]struct{ name, input, want string }` table (or equivalent)
- [ ] Use `t.Run(tt.name, ...)` for each case
- [ ] Use `t.Errorf` (not `t.Fatalf`) for value mismatch — all cases should run even if one fails
- [ ] Cover all 5 required case types
- [ ] The test file compiles with `go test ./...`

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The package declaration at the top of your test file should be `package yourpkg_test` (or `package yourpkg` if you want white-box access). Import `"testing"`. Your function signature is `func TestReverse(t *testing.T)`.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

For the palindrome case, pick a word that reads the same forwards and backwards (e.g., `"racecar"`). The `Reverse("racecar")` should return `"racecar"`. For the UTF-8 case, `Reverse("café")` should return `"éfac"` — not garbled bytes.

</details>

### Expected Output / Acceptance Criteria
```
$ go test -v -run TestReverse ./...
=== RUN   TestReverse
=== RUN   TestReverse/empty_string
=== RUN   TestReverse/single_character
=== RUN   TestReverse/ascii_string
=== RUN   TestReverse/palindrome
=== RUN   TestReverse/utf8_string
--- PASS: TestReverse (0.00s)
    --- PASS: TestReverse/empty_string (0.00s)
    --- PASS: TestReverse/single_character (0.00s)
    --- PASS: TestReverse/ascii_string (0.00s)
    --- PASS: TestReverse/palindrome (0.00s)
    --- PASS: TestReverse/utf8_string (0.00s)
PASS
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package stringutil_test

import "testing"

func TestReverse(t *testing.T) {
    tests := []struct {
        name  string
        input string
        want  string
    }{
        {"empty string", "", ""},
        {"single character", "a", "a"},
        {"ascii string", "hello", "olleh"},
        {"palindrome", "racecar", "racecar"},
        {"utf8 string", "café", "éfac"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Reverse(tt.input)
            if got != tt.want {
                t.Errorf("Reverse(%q) = %q; want %q", tt.input, got, tt.want)
            }
        })
    }
}
```

**Explanation:**
The anonymous struct inside the slice is the Go idiom for test tables — it is self-documenting (each field has a name) and compact (no need to define a named type elsewhere). `t.Run` creates a subtest for each case, which means all cases run even if one fails, and you can run individual cases with `go test -run TestReverse/palindrome`. The failure message format `Reverse(%q) = %q; want %q` prints the input and both values — essential for diagnosing mismatches.

**Common wrong answers and why they fail:**
- Using `t.Fatalf` instead of `t.Errorf` — stops at the first failing case, hiding subsequent failures
- Not using `t.Run` — all cases share one test function; a failure doesn't tell you which case failed

</details>

---

## Exercise 2: Testing an Error-Returning Function [🟢 Easy] [1 pt]

### Context
Most real Go functions return `(value, error)`. Testing them requires checking both: was an error returned when expected, and is the returned value correct when no error was returned? The `wantErr bool` pattern is the idiomatic way to handle this in a table.

### Task
Write a table-driven test for the following function:

```go
// ParsePositive parses s as a positive integer.
// Returns an error if s is not a valid integer or if it is <= 0.
func ParsePositive(s string) (int, error) {
    n, err := strconv.Atoi(s)
    if err != nil {
        return 0, fmt.Errorf("not an integer: %w", err)
    }
    if n <= 0 {
        return 0, fmt.Errorf("must be positive, got %d", n)
    }
    return n, nil
}
```

Include cases for: valid input ("42"), zero ("0"), negative ("-5"), non-integer ("abc"), and the boundary value ("1").

### Requirements
- [ ] Use a table with `name string`, `input string`, `want int`, `wantErr bool` fields
- [ ] Use `t.Fatalf` when the error expectation is wrong (subsequent checks would be meaningless)
- [ ] When `wantErr` is true, return after confirming the error — do not check `want`
- [ ] When `wantErr` is false, use `t.Errorf` to check the returned value

### Hints
<details>
<summary>Hint 1</summary>

The pattern for the error check is:
```go
if (err != nil) != tt.wantErr {
    t.Fatalf("ParsePositive(%q) error = %v; wantErr %v", tt.input, err, tt.wantErr)
}
if tt.wantErr {
    return
}
```
This checks that got-an-error matches expected-an-error, then skips the value check if an error was expected.

</details>

### Expected Output / Acceptance Criteria
```
$ go test -v -run TestParsePositive ./...
--- PASS: TestParsePositive (0.00s)
    --- PASS: TestParsePositive/valid_42 (0.00s)
    --- PASS: TestParsePositive/zero (0.00s)
    --- PASS: TestParsePositive/negative (0.00s)
    --- PASS: TestParsePositive/not_an_integer (0.00s)
    --- PASS: TestParsePositive/boundary_1 (0.00s)
PASS
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package parseutil_test

import "testing"

func TestParsePositive(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {"valid 42", "42", 42, false},
        {"zero", "0", 0, true},
        {"negative", "-5", 0, true},
        {"not an integer", "abc", 0, true},
        {"boundary 1", "1", 1, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParsePositive(tt.input)
            if (err != nil) != tt.wantErr {
                t.Fatalf("ParsePositive(%q) error = %v; wantErr %v", tt.input, err, tt.wantErr)
            }
            if tt.wantErr {
                return // error was expected — value is undefined, skip check
            }
            if got != tt.want {
                t.Errorf("ParsePositive(%q) = %d; want %d", tt.input, got, tt.want)
            }
        })
    }
}
```

**Explanation:**
The `(err != nil) != tt.wantErr` idiom is the cleanest way to check whether the error expectation was met. If the function returned an error when none was expected (or vice versa), `t.Fatalf` stops the subtest — there is no point comparing the returned value when the error state is wrong. If `tt.wantErr` is true and an error was correctly returned, we `return` immediately — the value is undefined in error cases.

</details>

---

## Exercise 3: Write a Benchmark and Compare Two Implementations [🟡 Medium] [2 pts]

### Context
Benchmarks answer the question "which is faster?" with actual numbers, not intuition. This exercise requires writing two benchmarks for competing string-joining approaches and reading the output to determine which allocates less.

### Task
Write two benchmark functions in a `_test.go` file comparing these two approaches to joining a slice of strings with a separator:

```go
// Approach A: naive loop with string concatenation
func JoinNaive(parts []string, sep string) string {
    result := ""
    for i, p := range parts {
        if i > 0 {
            result += sep
        }
        result += p
    }
    return result
}

// Approach B: strings.Join
func JoinStdlib(parts []string, sep string) string {
    return strings.Join(parts, sep)
}
```

Use a fixed input of 100 strings each of length 10, joined with `", "`. Run the benchmarks and report which approach is faster and which allocates less.

### Requirements
- [ ] Both benchmark functions follow the `BenchmarkXxx(b *testing.B)` signature
- [ ] Each benchmark uses a fixed input prepared _before_ the measurement loop
- [ ] `b.ResetTimer()` is called after input preparation
- [ ] Both benchmarks call `b.ReportAllocs()`
- [ ] You run both with `go test -bench=. -benchmem` and record the output in a comment

### Hints
<details>
<summary>Hint 1</summary>

Prepare the input slice before the loop:
```go
func BenchmarkJoinNaive(b *testing.B) {
    parts := make([]string, 100)
    for i := range parts {
        parts[i] = strings.Repeat("x", 10)
    }
    b.ResetTimer()
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        _ = JoinNaive(parts, ", ")
    }
}
```

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The `_ = result` pattern discards the result to prevent the compiler from optimizing the call away. Without it, a sufficiently smart compiler could theoretically eliminate the entire computation.

</details>

### Expected Output / Acceptance Criteria
Your benchmark output will vary by machine, but should show a clear difference. Record actual numbers from your run. Example (not guaranteed values):

```
BenchmarkJoinNaive-8     20000   75840 ns/op   26080 B/op   99 allocs/op
BenchmarkJoinStdlib-8   300000    4212 ns/op    1168 B/op    2 allocs/op
```

The key finding: `strings.Join` should be significantly faster with far fewer allocations. This is because the naive approach allocates a new string on every `+=`, while `strings.Join` computes the total length once and allocates exactly once.

### Solution
<details>
<summary>Show Solution</summary>

```go
package strjoin_test

import (
    "strings"
    "testing"
)

func BenchmarkJoinNaive(b *testing.B) {
    // Prepare fixed input — not included in the measurement
    parts := make([]string, 100)
    for i := range parts {
        parts[i] = strings.Repeat("x", 10)
    }
    b.ResetTimer()  // measurement starts here
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        _ = JoinNaive(parts, ", ")
    }
}

func BenchmarkJoinStdlib(b *testing.B) {
    parts := make([]string, 100)
    for i := range parts {
        parts[i] = strings.Repeat("x", 10)
    }
    b.ResetTimer()
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        _ = JoinStdlib(parts, ", ")
    }
}
```

**Explanation:**
The `b.ResetTimer()` call excludes the input preparation from the ns/op measurement. Without it, the benchmark would measure both the setup and the join — giving misleading numbers that depend on the number of strings, not just the join strategy. `b.ReportAllocs()` ensures allocation data appears even without `-benchmem`.

The dramatic difference in allocs/op (`99` vs `2`) explains why `strings.Join` is faster: the naive approach creates a new string (and thus a new heap allocation) on every iteration of the loop, while `strings.Join` pre-computes the total size and writes everything into a single allocation.

**Alternative approaches:**
`strings.Builder` with pre-allocated capacity (`sb.Grow(totalLen)`) can also achieve single-allocation joining and is worth benchmarking for comparison.

</details>

---

## Exercise 4: Write a Fuzz Test for a Parser [🔴 Hard] [3 pts]

### Context
Fuzz tests find bugs in input-handling code that you would never think to test manually. This exercise requires identifying the right invariants to assert and writing a fuzz test that would catch real parser bugs. The parser in this exercise is intentionally simple to keep focus on the testing mechanics.

### Task
Write a fuzz test for the following CSV row parser:

```go
// ParseCSVRow parses a single line of comma-separated values.
// It does not handle quoted fields. Returns a slice of field strings.
// Must never panic on any input.
func ParseCSVRow(line string) []string {
    return strings.Split(line, ",")
}
```

Your fuzz test must:
1. Include at least 3 seed corpus entries
2. Assert the round-trip invariant: `strings.Join(ParseCSVRow(line), ",") == line`
3. Assert that the number of fields is always `>= 1` (even for an empty string, Split returns a slice with one empty string)
4. Not panic (guaranteed by the fuzzer's crash detection)

### Requirements
- [ ] Function signature is `func FuzzParseCSVRow(f *testing.F)`
- [ ] At least 3 `f.Add(...)` seed corpus entries including the empty string
- [ ] The fuzz function has signature `func(t *testing.T, line string)`
- [ ] Both invariants (round-trip and len >= 1) are asserted
- [ ] The test passes when run with `go test -run FuzzParseCSVRow ./...` (seed corpus only)

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

The fuzz function body checks invariants. For the round-trip check:
```go
fields := ParseCSVRow(line)
rejoined := strings.Join(fields, ",")
if rejoined != line {
    t.Errorf("round-trip failed: ParseCSVRow(%q) -> Join -> %q", line, rejoined)
}
```

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

This parser does not handle errors, so you cannot do the `if err != nil { return }` early exit. Every input must satisfy both invariants. The `strings.Split` function always returns at least one element, so the `len >= 1` invariant should always hold — but the fuzz test forces you to confirm this explicitly.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```go
func FuzzParseCSVRow(f *testing.F) {
    f.Add("")
    f.Add("a,b,c")
    f.Add("one")
    f.Fuzz(func(t *testing.T, line string) {
        fields := ParseCSVRow(line)
        if len(fields) < 1 {
            t.Errorf("ParseCSVRow(%q) returned empty slice", line)
        }
        if strings.Join(fields, ",") != line {
            t.Errorf("round-trip failed for %q", line)
        }
    })
}
```

</details>

### Expected Output / Acceptance Criteria
```bash
# Seed corpus run — should pass immediately
$ go test -run FuzzParseCSVRow ./...
PASS

# Active fuzzing — should not find any crashers for this simple implementation
$ go test -fuzz FuzzParseCSVRow -fuzztime=10s ./...
fuzz: elapsed: 10s, execs: 843201, new interesting: 15, corpus: 22
ok  	yourpackage	10.023s
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package csvutil_test

import (
    "strings"
    "testing"
)

func FuzzParseCSVRow(f *testing.F) {
    // Seed corpus: representative inputs for the fuzzer to mutate
    f.Add("")               // empty input — edge case
    f.Add("a,b,c")         // typical multi-field case
    f.Add("one")           // single field, no commas
    f.Add(",")             // separator only — two empty fields
    f.Add("a,,b")          // empty field in the middle

    f.Fuzz(func(t *testing.T, line string) {
        // Invariant 1: must return at least 1 field
        fields := ParseCSVRow(line)
        if len(fields) < 1 {
            t.Errorf("ParseCSVRow(%q) returned empty slice (len=%d)", line, len(fields))
        }

        // Invariant 2: round-trip — joining the fields back must reproduce the original line
        rejoined := strings.Join(fields, ",")
        if rejoined != line {
            t.Errorf("round-trip failed:\n  input:    %q\n  rejoined: %q", line, rejoined)
        }
    })
}
```

**Step-by-step explanation:**

1. `f.Add(...)` provides seed inputs. These become the starting corpus that the fuzzer mutates. They also run as normal tests when you use `go test -run FuzzParseCSVRow` (without `-fuzz`).
2. The fuzz function receives `*testing.T` and the fuzzed input. Unlike a regular test, this function may be called millions of times with mutated inputs.
3. Invariant 1 (`len >= 1`) is guaranteed by `strings.Split` semantics — it always returns at least one element. The fuzz test confirms this is never violated.
4. Invariant 2 (round-trip) confirms that no information is lost: parsing and re-joining must give back the original string. For this simple parser this always holds; for a more complex parser with quoting, it might not.

**Why this approach:**
The invariants are properties that must always be true regardless of input — not properties that are only true for specific inputs. This is the key insight of fuzz testing: you state what is always true, and the fuzzer tries to disprove it.

**What a weaker solution looks like and why it fails:**
Testing only the seed corpus without a fuzz test (`f.Add` without `f.Fuzz`) would miss the edge cases the fuzzer generates. Asserting `fields[0] == "..."` for specific inputs is a regression test, not a fuzz invariant.

</details>

---

## Exercise 5: Test an HTTP Handler with httptest [🟡 Medium] [2 pts]

### Context
Testing HTTP handlers requires creating fake HTTP requests and capturing the response — without starting a real network server. `net/http/httptest` is the standard tool for this. This exercise practices the complete pattern: `httptest.NewRequest`, `httptest.NewRecorder`, driving the handler, and checking both status code and body.

### Task
Write a table-driven test for the following HTTP handler:

```go
// EchoHandler echoes the "message" query parameter back as plain text.
// Returns 400 Bad Request if the parameter is missing or empty.
// Returns 200 OK with "Echo: <message>" if the parameter is present.
func EchoHandler(w http.ResponseWriter, r *http.Request) {
    msg := r.URL.Query().Get("message")
    if msg == "" {
        http.Error(w, "message parameter required", http.StatusBadRequest)
        return
    }
    fmt.Fprintf(w, "Echo: %s", msg)
}
```

Include cases for: valid message, missing parameter, and empty parameter.

### Requirements
- [ ] Use `httptest.NewRequest` and `httptest.NewRecorder`
- [ ] Check both the status code (`w.Result().StatusCode`) and the response body
- [ ] Use a table-driven structure with at least 3 cases
- [ ] Import `"net/http"`, `"net/http/httptest"`, `"io"`, `"testing"`

### Hints
<details>
<summary>Hint 1</summary>

```go
req := httptest.NewRequest(http.MethodGet, "/echo?message=hello", nil)
w := httptest.NewRecorder()
EchoHandler(w, req)
res := w.Result()
// res.StatusCode is the status code
// io.ReadAll(res.Body) reads the body
```

</details>

### Expected Output / Acceptance Criteria
```
$ go test -v -run TestEchoHandler ./...
--- PASS: TestEchoHandler (0.00s)
    --- PASS: TestEchoHandler/valid_message (0.00s)
    --- PASS: TestEchoHandler/missing_parameter (0.00s)
    --- PASS: TestEchoHandler/empty_parameter (0.00s)
PASS
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package handler_test

import (
    "io"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestEchoHandler(t *testing.T) {
    tests := []struct {
        name       string
        url        string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "valid message",
            url:        "/echo?message=hello",
            wantStatus: http.StatusOK,
            wantBody:   "Echo: hello",
        },
        {
            name:       "missing parameter",
            url:        "/echo",
            wantStatus: http.StatusBadRequest,
            wantBody:   "message parameter required\n",
        },
        {
            name:       "empty parameter",
            url:        "/echo?message=",
            wantStatus: http.StatusBadRequest,
            wantBody:   "message parameter required\n",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodGet, tt.url, nil)
            w := httptest.NewRecorder()

            EchoHandler(w, req)

            res := w.Result()
            if res.StatusCode != tt.wantStatus {
                t.Errorf("status = %d; want %d", res.StatusCode, tt.wantStatus)
            }

            body, err := io.ReadAll(res.Body)
            if err != nil {
                t.Fatalf("read body: %v", err)
            }
            if string(body) != tt.wantBody {
                t.Errorf("body = %q; want %q", string(body), tt.wantBody)
            }
        })
    }
}
```

**Explanation:**
`httptest.NewRequest` creates a real `*http.Request` without a network connection. `httptest.NewRecorder` implements `http.ResponseWriter` and captures everything the handler writes. After calling the handler, `w.Result()` gives you a `*http.Response` with the captured status and body. The `\n` in the expected body for error cases comes from `http.Error`, which appends a newline.

</details>

---

## Exercise 6: Example Function with Output Comment [🟢 Easy] [1 pt]

### Context
Example functions are simultaneously documentation and tests. A `// Output:` comment makes the example an executable test: if the actual output doesn't match, `go test` fails. This exercise practices writing examples that will appear in `go doc` output and on pkg.go.dev.

### Task
Write example functions for `Reverse` and `ParsePositive` (from Exercises 1 and 2). Each example must have a `// Output:` comment with the expected output. Include at least 2 calls per example function.

### Requirements
- [ ] Both functions are named `ExampleReverse` and `ExampleParsePositive`
- [ ] Each has a `// Output:` comment that matches the actual output exactly
- [ ] The examples compile and pass `go test ./...`
- [ ] The examples are realistic (show useful usage, not trivial inputs)

### Hints
<details>
<summary>Hint 1</summary>

The `// Output:` comment must match the actual output exactly, including spaces and newlines. Use `fmt.Println` (which adds a newline) — the output comment should have one line per `Println` call. `fmt.Printf` without a trailing `\n` won't end with a newline, which changes the output.

</details>

### Expected Output / Acceptance Criteria
```
$ go test -v -run ExampleReverse ./...
=== RUN   ExampleReverse
--- PASS: ExampleReverse (0.00s)
PASS
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package stringutil_test

import "fmt"

func ExampleReverse() {
    fmt.Println(Reverse("hello"))
    fmt.Println(Reverse(""))
    fmt.Println(Reverse("racecar"))
    // Output:
    // olleh
    //
    // racecar
}

func ExampleParsePositive() {
    n, err := ParsePositive("42")
    fmt.Println(n, err)

    _, err = ParsePositive("0")
    fmt.Println(err)
    // Output:
    // 42 <nil>
    // must be positive, got 0
}
```

**Explanation:**
The `// Output:` block is part of the function body (as a comment). The empty line in `ExampleReverse` corresponds to `Reverse("")` printing an empty string followed by a newline. The `// Output:` comment must match character-for-character — even a trailing space will cause the test to fail.

Note the blank line in the Output comment for the empty string case: `Reverse("")` returns `""`, and `fmt.Println("")` prints just a newline, which appears as an empty line in the output.

**Common wrong answers and why they fail:**
- Forgetting the blank line for the empty string case — the output comment must match exactly
- Using `fmt.Printf` without `\n` when `fmt.Println` is expected — the output comment would need to account for the missing newline

</details>

---

## Exercise 7: TestMain with Package-Level Setup [⭐ Challenge] [5 pts]

### Context
Some tests require shared infrastructure that is expensive to set up on a per-test basis — a database connection, a listening server, or a compiled binary. `TestMain` provides package-level setup and teardown. This challenge exercise requires designing the full lifecycle: setup → run all tests → teardown → exit with correct code.

### Task
Write a complete test file with `TestMain` that:

1. Creates a temporary directory and writes a sample config file (`config.json`) into it before any tests run
2. Stores the temp directory path in a package-level variable accessible to all tests
3. Runs all tests with `m.Run()`
4. Cleans up the temp directory after all tests complete
5. Calls `os.Exit(code)` with the exit code from `m.Run()`
6. Includes at least one test (`TestConfigExists`) that reads from the temp directory set up by `TestMain`

### Requirements
- [ ] `TestMain(m *testing.M)` is the entry point — no test runs without it
- [ ] Setup (write config file) happens before `m.Run()`
- [ ] Teardown (`os.RemoveAll`) happens after `m.Run()` but before `os.Exit`
- [ ] A package-level `var testDir string` holds the temp directory path
- [ ] `TestConfigExists` verifies the config file was created in the expected location
- [ ] The test file compiles and passes `go test ./...`

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

```go
var testDir string

func TestMain(m *testing.M) {
    // setup
    var err error
    testDir, err = os.MkdirTemp("", "mytest-*")
    if err != nil {
        fmt.Fprintf(os.Stderr, "setup: %v\n", err)
        os.Exit(1)
    }
    // write files into testDir...

    code := m.Run() // run all tests

    os.RemoveAll(testDir) // teardown
    os.Exit(code)         // must call os.Exit with the code
}
```

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

The `os.Exit(code)` call after `m.Run()` is essential. Without it, `os.Exit` at the end of `TestMain` would exit with code 0 regardless of test results. The code from `m.Run()` is 0 if all tests passed, 1 if any failed.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

For `TestConfigExists`:
```go
func TestConfigExists(t *testing.T) {
    configPath := filepath.Join(testDir, "config.json")
    if _, err := os.Stat(configPath); os.IsNotExist(err) {
        t.Errorf("config file not found at %s", configPath)
    }
}
```

</details>

### Expected Output / Acceptance Criteria
```
$ go test -v ./...
=== RUN   TestConfigExists
--- PASS: TestConfigExists (0.00s)
PASS
ok  	yourpackage	0.005s
```

The cleanup should remove the temp directory — verify with `ls /tmp/mytest-*` before and after.

### Solution
<details>
<summary>Show Solution</summary>

```go
package config_test

import (
    "fmt"
    "os"
    "path/filepath"
    "testing"
)

// testDir is set by TestMain and accessible to all tests in this package
var testDir string

func TestMain(m *testing.M) {
    // Setup: create a temp directory and write a sample config file
    var err error
    testDir, err = os.MkdirTemp("", "configtest-*")
    if err != nil {
        fmt.Fprintf(os.Stderr, "TestMain setup: %v\n", err)
        os.Exit(1)
    }

    configContent := `{"version": 1, "debug": false}`
    configPath := filepath.Join(testDir, "config.json")
    if err := os.WriteFile(configPath, []byte(configContent), 0644); err != nil {
        fmt.Fprintf(os.Stderr, "TestMain write config: %v\n", err)
        os.RemoveAll(testDir)
        os.Exit(1)
    }

    // Run all tests and capture the exit code
    code := m.Run()

    // Teardown: remove the temp directory
    if err := os.RemoveAll(testDir); err != nil {
        fmt.Fprintf(os.Stderr, "TestMain teardown: %v\n", err)
    }

    // Exit with the test runner's exit code — MUST call os.Exit
    os.Exit(code)
}

func TestConfigExists(t *testing.T) {
    configPath := filepath.Join(testDir, "config.json")
    if _, err := os.Stat(configPath); os.IsNotExist(err) {
        t.Errorf("config file not created at %s", configPath)
    }
}

func TestConfigContent(t *testing.T) {
    configPath := filepath.Join(testDir, "config.json")
    data, err := os.ReadFile(configPath)
    if err != nil {
        t.Fatalf("read config: %v", err)
    }
    if string(data) != `{"version": 1, "debug": false}` {
        t.Errorf("config content = %q; want JSON with version and debug", string(data))
    }
}
```

**Step-by-step explanation:**

1. `testDir` is a package-level variable — visible to all test functions in the package.
2. `TestMain` creates a temp directory, writes the config file, then calls `m.Run()`. If setup fails, it calls `os.Exit(1)` directly — no tests should run with a broken setup.
3. After `m.Run()` returns, teardown runs regardless of whether tests passed. The exit code from `m.Run()` is captured and passed to `os.Exit`.
4. Without `os.Exit(code)`, the test binary would exit 0 even if tests failed.

**Why this approach:**
`TestMain` is used when setup is expensive or requires package-level state. For per-test setup (which is more common), prefer a helper function with `t.Cleanup`. Use `TestMain` only when you genuinely need something set up once for the entire package.

**What a weaker solution looks like and why it fails:**
Using `init()` for setup instead of `TestMain` — `init()` runs during test binary initialization (before flags are parsed), and there is no corresponding teardown mechanism. Using `defer os.RemoveAll(testDir)` in `TestMain` does not work because `os.Exit` does not run deferred functions.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Table-Driven Test | — | —/1 | — | — |
| Exercise 2 — Error-Returning Function | — | —/1 | — | — |
| Exercise 3 — Benchmark Comparison | — | —/2 | — | — |
| Exercise 4 — Fuzz Test | — | —/3 | — | — |
| Exercise 5 — HTTP Handler Test | — | —/2 | — | — |
| Exercise 6 — Example Function | — | —/1 | — | — |
| Exercise 7 — TestMain (Challenge) | — | —/5 | — | — |
| **Total** | | **—/15** | | |

**Passing threshold:** 10/15 (67%). Aim for 13/15 (87%) before taking the test.
