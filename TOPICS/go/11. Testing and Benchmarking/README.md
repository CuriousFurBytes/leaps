# Module 11: Testing and Benchmarking

[← Module 10: Generics](../10.%20Generics/) | [Topic Home](../README.md) | [Module 12: Advanced Concurrency Patterns →](../12.%20Advanced%20Concurrency%20Patterns/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate--advanced-blue)
![Time](https://img.shields.io/badge/time-5--7h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [The testing Package and _test.go Convention](#the-testing-package-and-_testgo-convention)
  - [go test and Key Flags](#go-test-and-key-flags)
  - [Writing Tests: t.Error, t.Fatal, and When to Use Each](#writing-tests-terror-tfatal-and-when-to-use-each)
  - [Table-Driven Tests — The Idiomatic Default](#table-driven-tests--the-idiomatic-default)
  - [Subtests and Parallelism](#subtests-and-parallelism)
  - [Test Helpers and t.Helper](#test-helpers-and-thelper)
  - [Setup, Teardown, and TestMain](#setup-teardown-and-testmain)
  - [Testing with Interfaces and Hand-Written Fakes](#testing-with-interfaces-and-hand-written-fakes)
  - [Testing HTTP Handlers with net/http/httptest](#testing-http-handlers-with-nethttphttptest)
  - [Golden Files](#golden-files)
  - [Benchmarks](#benchmarks)
  - [Fuzzing](#fuzzing)
  - [Example Functions](#example-functions)
  - [Coverage](#coverage)
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

This module covers **Go's built-in testing ecosystem**: the `testing` package, `go test` and its flags, table-driven tests, subtests, test helpers, benchmarks, fuzz tests, example functions, and coverage measurement. Testing in Go is not an afterthought — it is built into the toolchain, requires zero third-party dependencies for most use cases, and follows idioms that are deeply ingrained in the Go community.

By the end of this module, you will understand not just how to write tests but _why_ Go's testing philosophy works the way it does: why errors are reported with `t.Error` rather than assertions, why table-driven tests are the default rather than a pattern to reach for, why Go leans toward hand-written fakes over mocking frameworks, and why fuzz testing was added to the standard toolchain. These are deliberate design choices, and understanding the reasoning makes you a better Go programmer.

**Difficulty:** Intermediate–Advanced &nbsp;|&nbsp; **Estimated time:** 5–7 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Write correct Go tests using the `testing` package, distinguish `t.Error` from `t.Fatal`, and run them with `go test` and its flags — _given a function, write a complete test file that a reviewer would accept_
2. Write idiomatic table-driven tests with subtests (`t.Run`) and parallel execution (`t.Parallel`) — _refactor a series of individual test functions into a single table-driven test_
3. Write and interpret benchmarks with `b.N`, `b.ResetTimer`, and `b.ReportAllocs`; read `ns/op` and `allocs/op` output — _compare two implementations and determine which is faster_
4. Write a fuzz test with `f.Add` and `f.Fuzz`, understand the corpus model, and know how to reproduce a crasher — _protect a parsing function against inputs the developer never considered_
5. Measure and improve test coverage using `-coverprofile` and `go tool cover`, and explain what coverage does and does not guarantee — _identify untested code paths and add tests for them_

---

## Prerequisites

### Required Modules

- [[go/6. Methods and Interfaces]] — you need to understand: how interfaces work in Go, because testing with fakes relies entirely on passing interface values to code under test; the testing philosophy makes no sense without understanding structural typing
- [[go/8. Error Handling]] — you need to understand: how Go functions return errors, how to wrap and unwrap them, and how `errors.Is` works; tests frequently check that a function returns the right error
- [[go/7. Packages and Modules]] — you need to understand: how `go.mod` works, what a package is, and how to run `go test ./...` across a module

### Required Concepts

- **Interfaces for decoupling** — the `io.Reader`, `io.Writer`, and custom domain interfaces pattern is how you make code testable without a framework; tests inject fakes through interfaces
- **Multiple return values and the `(T, error)` pattern** — virtually every function you will test returns an error; knowing how to check and compare errors is essential
- **Closures** — test helpers and table-driven test closures use function values; understanding how closures capture variables is needed to avoid the loop-variable capture bug in tests

> [!TIP]
> If interfaces feel shaky, revisit [[go/6. Methods and Interfaces]] before continuing.
> The testing-with-interfaces section will not make sense without a firm grasp of structural typing.

---

## Why This Matters

Testing is the discipline that separates code that works on the developer's machine from code that works in production under real conditions. In Go, the testing toolchain is a first-class citizen — there is no configuration file to write, no test runner to install, no assertion library to choose. `go test` is always available.

Concretely, mastery of this module enables you to:

- **Ship with confidence** — table-driven tests that cover edge cases, error paths, and boundary values mean you catch regressions before reviewers do; Go codebases like the standard library and Kubernetes rely heavily on this pattern
- **Measure and optimize performance rigorously** — `go test -bench` gives you reproducible, ns/op measurements; using benchstat to compare before/after prevents "felt faster" performance work and catches accidental regressions in hot paths (ties directly to [[go/16. Performance and Profiling]])
- **Find bugs machines find, not humans** — fuzz testing automatically generates inputs that break invariants; the Go team found real bugs in the standard library's JPEG, zip, and crypto packages using the fuzzer introduced in Go 1.18
- **Test HTTP handlers without a live server** — `net/http/httptest` lets you drive handlers in-process (forward ref: [[go/13. Web Services and APIs]]); this is the standard pattern for testing Go web services

Without a solid understanding of Go's testing tools, you would be unable to write tests that scale beyond trivial cases, unable to protect performance-sensitive code from regressions, and unable to participate effectively in Go code reviews where tests are expected to be table-driven and fakes are preferred over mocks.

---

## Historical Context

Go's `testing` package has been part of the language since the first open-source release in **November 2009**. The core API — `*testing.T`, `t.Error`, `t.Fatal`, `t.Log`, and the `TestXxx` function convention — has been stable and essentially unchanged since Go 1.0 in 2012.

The design reflects Go's general philosophy of composability over magic. Rather than providing an assertion library with `assertEqual(expected, actual)`, the `testing` package provides reporting primitives (`t.Error`, `t.Fatal`) and leaves the comparison logic to the test author. This was a deliberate choice: assertion libraries tend to grow complex DSLs, hide the actual comparison logic, and produce opaque failure messages. Go's approach pushes the test author to write `if got != want { t.Errorf(...) }` — explicit, readable, and debuggable.

Key moments in Go's testing history:

- **2009** — `testing` package ships with Go; `go test` is part of the toolchain from day one
- **2012** — Go 1.0; the testing API is stable; subtests (`t.Run`) do not yet exist
- **2015** — Go 1.7 adds `t.Run` for subtests and `b.Run` for sub-benchmarks — the most significant addition to the testing package; table-driven tests become even more powerful
- **2018** — Go 1.10 adds `t.Helper()`, which fixes the long-standing problem of test helper functions reporting the wrong source line in failure messages
- **2022** — Go 1.18 adds fuzzing to the standard toolchain (`testing.F`), making Go one of the first major languages to ship a fuzzer as part of the language distribution

Understanding this history clarifies why Go's testing API looks the way it does: it was built by people who had opinions about what made test code maintainable, and those opinions have proven durable.

---

## Core Concepts

### The testing Package and _test.go Convention

Go's test runner discovers test code by convention, not configuration:

- **Files ending in `_test.go`** are test files. They are compiled only when `go test` is run — never in production builds.
- **Functions named `TestXxx(t *testing.T)`** are test functions. `Xxx` must start with an uppercase letter.
- **Functions named `BenchmarkXxx(b *testing.B)`** are benchmarks.
- **Functions named `FuzzXxx(f *testing.F)`** are fuzz tests (Go 1.18+).
- **Functions named `ExampleXxx()`** are example functions (documentation + test).

Test files may live in the same package (white-box testing, can access unexported identifiers) or in a `package foo_test` package (black-box testing, only the exported API is visible). The two styles coexist in the same directory:

```go
// calculator.go
package calculator

func Add(a, b int) int { return a + b }

func addInternal(a, b int) int { return a + b } // unexported
```

```go
// calculator_test.go — same package (white-box)
package calculator

import "testing"

func TestAddInternal(t *testing.T) {
    // Can access unexported addInternal
    if got := addInternal(2, 3); got != 5 {
        t.Errorf("addInternal(2,3) = %d; want 5", got)
    }
}
```

```go
// calculator_export_test.go — external package (black-box)
package calculator_test

import (
    "testing"
    "calculator"
)

func TestAdd(t *testing.T) {
    // Only exported API visible
    if got := calculator.Add(2, 3); got != 5 {
        t.Errorf("Add(2,3) = %d; want 5", got)
    }
}
```

The convention is: use `package foo_test` (black-box) for public API tests and `package foo` (white-box) only when you need to test unexported logic. Prefer black-box — it tests exactly what your users see.

---

### go test and Key Flags

```bash
# Run all tests in the current package
go test .

# Run all tests in all packages in the module
go test ./...

# Verbose output — print each test name and PASS/FAIL
go test -v ./...

# Run only tests matching a pattern (regex)
go test -run TestAdd ./...
go test -run TestAdd/positive ./...   # matches subtest "positive" inside TestAdd

# Detect data races (adds ~5–10x overhead — run in CI, not every loop)
go test -race ./...

# Coverage — print coverage percentage
go test -cover ./...

# Coverage — write a coverage profile file for go tool cover
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out        # open interactive HTML report

# Run benchmarks (all by default, no tests)
go test -bench=. ./...
go test -bench=BenchmarkAdd -benchmem ./...   # -benchmem adds allocs/op

# Run benchmarks with count=N for more stable results
go test -bench=. -count=5 ./...

# Run a fuzz test for 30 seconds
go test -fuzz=FuzzParse -fuzztime=30s ./...

# Force rerunning tests (bypass cache)
go test -count=1 ./...
```

> [!NOTE]
> `go test` caches results — if the package and its test files haven't changed, it returns the cached result immediately. Use `-count=1` to bypass the cache. Benchmarks are never cached.

---

### Writing Tests: t.Error, t.Fatal, and When to Use Each

The two primary reporting methods differ in one critical way: **`t.Fatal` stops the current test function immediately; `t.Error` marks the test as failed but continues running**.

```go
func TestDivide(t *testing.T) {
    result, err := Divide(10, 2)

    // Use t.Fatal when subsequent assertions are meaningless if this fails.
    // If err != nil, result is garbage — no point checking it.
    if err != nil {
        t.Fatalf("Divide(10, 2) returned unexpected error: %v", err)
    }

    // Use t.Error when you want to accumulate multiple failures.
    // Both checks can run even if one fails — better diagnostic information.
    if result != 5 {
        t.Errorf("Divide(10, 2) = %d; want 5", result)
    }
}
```

The `f` variants (`t.Fatalf`, `t.Errorf`) accept printf-style format strings. **Always prefer `t.Errorf`/`t.Fatalf` over `t.Error`/`t.Fatal` for meaningful failure messages.** The failure message format convention is:

```
got X; want Y
```

This puts the actual value first, which is what you are investigating when debugging. Many Go projects enforce this with linters.

Additional methods:
- `t.Log` / `t.Logf` — print messages only if the test fails or `-v` is set
- `t.Skip` / `t.Skipf` — skip the test (useful for platform-specific or slow tests)
- `t.Cleanup(func())` — register a cleanup function, called when the test ends (Go 1.14+); preferred over `defer` in test helpers

---

### Table-Driven Tests — The Idiomatic Default

Table-driven tests are Go's canonical testing pattern. Instead of writing one test function per case, you define a slice of test cases (the "table") and range over them. This is not just style preference — the Go standard library uses it extensively, and most Go code reviews will ask you to convert repetitive test functions to table-driven form.

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"both positive", 2, 3, 5},
        {"both negative", -2, -3, -5},
        {"mixed signs", 10, -3, 7},
        {"zeros", 0, 0, 0},
        {"large numbers", 1000000, 999999, 1999999},
    }

    for _, tt := range tests {
        // t.Run creates a subtest — enables filtering with -run and
        // provides a clear name in the failure output
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.want {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

Running with `-v` shows each subtest:

```
=== RUN   TestAdd
=== RUN   TestAdd/both_positive
=== RUN   TestAdd/both_negative
=== RUN   TestAdd/mixed_signs
=== RUN   TestAdd/zeros
=== RUN   TestAdd/large_numbers
--- PASS: TestAdd (0.00s)
    --- PASS: TestAdd/both_positive (0.00s)
    --- PASS: TestAdd/both_negative (0.00s)
    --- PASS: TestAdd/mixed_signs (0.00s)
    --- PASS: TestAdd/zeros (0.00s)
    --- PASS: TestAdd/large_numbers (0.00s)
PASS
```

To run a single subtest: `go test -run TestAdd/mixed_signs`.

> [!TIP]
> The struct field `name string` is the key that makes table-driven tests maintainable. When a test fails, the name immediately identifies which case failed — no hunting through numbered cases.

---

### Subtests and Parallelism

`t.Run` creates a subtest: an independent test with its own `*testing.T`, its own name, and its own pass/fail state. Subtests can be run in parallel with `t.Parallel()`:

```go
func TestExpensiveOperation(t *testing.T) {
    tests := []struct {
        name  string
        input int
        want  int
    }{
        {"case A", 1, 10},
        {"case B", 2, 20},
        {"case C", 3, 30},
    }

    for _, tt := range tests {
        tt := tt // capture range variable — critical before Go 1.22
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // run this subtest concurrently with siblings
            got := ExpensiveOperation(tt.input)
            if got != tt.want {
                t.Errorf("ExpensiveOperation(%d) = %d; want %d", tt.input, got, tt.want)
            }
        })
    }
}
```

> [!WARNING]
> **The loop variable capture bug (pre-Go 1.22):** In Go versions before 1.22, the range variable `tt` is reused across iterations. If you pass `tt` to a goroutine or `t.Run` + `t.Parallel()` without first copying it, all subtests will see the same (last) value of `tt`. The fix is `tt := tt` inside the loop before the `t.Run` call. Go 1.22 fixes loop variable scoping, but many projects still run older toolchains.

`t.Parallel()` at the top of a test function (not inside `t.Run`) marks the entire test as parallel with other top-level tests in the package:

```go
func TestA(t *testing.T) {
    t.Parallel() // this test runs concurrently with TestB, TestC, etc.
    // ...
}
```

Use parallelism for tests that are genuinely independent and either slow (I/O) or CPU-bound. Do not use it for tests that share mutable global state.

---

### Test Helpers and t.Helper

Test helpers are functions called from multiple tests to reduce duplication. The problem: without `t.Helper()`, failure messages point to the line inside the helper, not the caller's line — making it hard to find which test case failed.

```go
// Without t.Helper() — failure message points to line 15 (inside assertEqual),
// not the line where assertEqual was called. Unhelpful.
func assertEqual(t *testing.T, got, want int) {
    if got != want {
        t.Errorf("got %d; want %d", got, want) // line 15 — wrong location
    }
}

// With t.Helper() — failure message points to the caller's line. Correct.
func assertEqualInt(t *testing.T, got, want int) {
    t.Helper() // marks this function as a test helper
    if got != want {
        t.Errorf("got %d; want %d", got, want)
    }
}

func TestSomething(t *testing.T) {
    assertEqualInt(t, Compute(5), 25)   // failure message points HERE — useful
    assertEqualInt(t, Compute(10), 100) // or HERE if this one fails
}
```

`t.Helper()` is the single most important thing to call at the start of any helper function that calls `t.Error`, `t.Fatal`, or their variants.

For cleanup after tests, prefer `t.Cleanup` over `defer` in helper functions:

```go
func createTempFile(t *testing.T) string {
    t.Helper()
    f, err := os.CreateTemp("", "test-*")
    if err != nil {
        t.Fatalf("create temp file: %v", err)
    }
    t.Cleanup(func() { os.Remove(f.Name()) }) // runs when the test ends
    return f.Name()
}
```

---

### Setup, Teardown, and TestMain

For package-level setup and teardown — things that should run once per package, not once per test — Go provides `TestMain`:

```go
// TestMain is called instead of running tests directly.
// m.Run() runs all the tests in the package.
func TestMain(m *testing.M) {
    // Setup: runs before any test in the package
    db := setupTestDatabase()

    // Run all tests — capture the exit code
    code := m.Run()

    // Teardown: runs after all tests complete
    db.Close()

    // Exit with the test runner's code (0 = pass, 1 = fail)
    os.Exit(code)
}
```

`TestMain` is used for: setting up shared state (a test database, a listening server), registering global flags, or controlling the test lifecycle. It is not needed for most test packages — use it only when you genuinely need package-level setup/teardown.

For per-test setup, use a helper function that returns a configured value and registers cleanup with `t.Cleanup`:

```go
func newTestServer(t *testing.T) *Server {
    t.Helper()
    s := &Server{Port: 0} // port 0 = OS assigns a free port
    if err := s.Start(); err != nil {
        t.Fatalf("start server: %v", err)
    }
    t.Cleanup(s.Stop)
    return s
}
```

---

### Testing with Interfaces and Hand-Written Fakes

This section ties directly to [[go/6. Methods and Interfaces]]. The key principle: **write production code against interfaces, not concrete types, and inject fakes through those interfaces in tests**.

Go's community strongly prefers hand-written fakes over generated mock frameworks (like `gomock` or `testify/mock`) for several reasons:
- Fakes are explicit Go code — no DSL, no magic, no code generation step
- Fakes reveal exactly what the test cares about
- Interfaces in Go are satisfied implicitly — you can define a narrow interface in your test package that the real type happens to satisfy

```go
// production code: EmailSender interface
type EmailSender interface {
    SendEmail(to, subject, body string) error
}

// NotifyUser depends on EmailSender — not on a concrete SMTP client
func NotifyUser(sender EmailSender, userEmail, message string) error {
    return sender.SendEmail(userEmail, "Notification", message)
}
```

```go
// test code: a fake that records calls
type fakeSender struct {
    sent []struct{ to, subject, body string }
    err  error // set this to simulate failure
}

func (f *fakeSender) SendEmail(to, subject, body string) error {
    if f.err != nil {
        return f.err
    }
    f.sent = append(f.sent, struct{ to, subject, body string }{to, subject, body})
    return nil
}

func TestNotifyUser(t *testing.T) {
    sender := &fakeSender{}
    err := NotifyUser(sender, "alice@example.com", "hello")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if len(sender.sent) != 1 {
        t.Fatalf("expected 1 email sent; got %d", len(sender.sent))
    }
    if sender.sent[0].to != "alice@example.com" {
        t.Errorf("sent to %q; want %q", sender.sent[0].to, "alice@example.com")
    }
}
```

The fake is a few lines of Go. It does exactly what the test needs — no framework required. When the test fails, the failure message is in plain Go, not framework-specific error formatting.

---

### Testing HTTP Handlers with net/http/httptest

`net/http/httptest` provides two utilities for testing HTTP handlers without starting a real network server. This is a forward reference to [[go/13. Web Services and APIs]] — the full HTTP story is there, but testing patterns apply here.

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
)

// Handler under test
func greetHandler(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")
    if name == "" {
        http.Error(w, "name is required", http.StatusBadRequest)
        return
    }
    fmt.Fprintf(w, "Hello, %s!", name)
}

func TestGreetHandler(t *testing.T) {
    tests := []struct {
        name       string
        query      string
        wantStatus int
        wantBody   string
    }{
        {"valid name", "?name=Alice", 200, "Hello, Alice!"},
        {"missing name", "", 400, "name is required\n"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodGet, "/greet"+tt.query, nil)
            w := httptest.NewRecorder()

            greetHandler(w, req)

            res := w.Result()
            if res.StatusCode != tt.wantStatus {
                t.Errorf("status = %d; want %d", res.StatusCode, tt.wantStatus)
            }
            body, _ := io.ReadAll(res.Body)
            if string(body) != tt.wantBody {
                t.Errorf("body = %q; want %q", string(body), tt.wantBody)
            }
        })
    }
}
```

`httptest.NewRecorder()` captures the response written by the handler. `httptest.NewServer(handler)` starts a real but ephemeral HTTP server on a random port — useful when you need to test a full HTTP client-server round-trip.

---

### Golden Files

Golden files store expected output in external files. They are useful when the expected output is large, complex, or formatted (e.g., JSON, HTML, rendered templates):

```go
func TestRenderReport(t *testing.T) {
    got := RenderReport(sampleData)

    // Path to the golden file: testdata/TestRenderReport.golden
    goldenPath := filepath.Join("testdata", t.Name()+".golden")

    // Update mode: run with -update flag to regenerate golden files
    if *update {
        if err := os.WriteFile(goldenPath, []byte(got), 0644); err != nil {
            t.Fatalf("update golden file: %v", err)
        }
        return
    }

    want, err := os.ReadFile(goldenPath)
    if err != nil {
        t.Fatalf("read golden file: %v", err)
    }
    if got != string(want) {
        t.Errorf("output mismatch:\ngot:\n%s\nwant:\n%s", got, want)
    }
}

var update = flag.Bool("update", false, "update golden files")
```

The `testdata/` directory is special: `go test` makes it accessible to tests, and it is never compiled into a binary. Golden files belong there.

---

### Benchmarks

Benchmarks measure the performance of code. The testing framework drives the loop — you never set `N` manually.

```go
// BenchmarkXxx(b *testing.B) — the function signature for benchmarks
func BenchmarkStringConcat(b *testing.B) {
    // b.N is set by the framework; it runs until results are stable
    for i := 0; i < b.N; i++ {
        _ = "Hello" + ", " + "World" + "!"
    }
}

func BenchmarkStringsBuilder(b *testing.B) {
    for i := 0; i < b.N; i++ {
        var sb strings.Builder
        sb.WriteString("Hello")
        sb.WriteString(", ")
        sb.WriteString("World")
        sb.WriteString("!")
        _ = sb.String()
    }
}
```

Running with `-benchmem`:

```bash
$ go test -bench=. -benchmem ./...
BenchmarkStringConcat-8      50000000    28.3 ns/op    16 B/op    1 allocs/op
BenchmarkStringsBuilder-8    20000000    71.4 ns/op    24 B/op    2 allocs/op
```

Reading the output:
- `50000000` — how many times the loop ran (b.N)
- `28.3 ns/op` — nanoseconds per operation
- `16 B/op` — bytes allocated per operation (`-benchmem`)
- `1 allocs/op` — heap allocations per operation (`-benchmem`)

**`b.ResetTimer`** — call this after setup code that you don't want included in the measurement:

```go
func BenchmarkWithSetup(b *testing.B) {
    data := generateLargeDataset() // slow setup — do not include in measurement
    b.ResetTimer()                 // reset after setup
    for i := 0; i < b.N; i++ {
        _ = ProcessDataset(data)
    }
}
```

**`b.ReportAllocs()`** — same as `-benchmem` but explicit in the benchmark function itself.

**Comparing benchmarks with benchstat**: run the benchmark multiple times with `-count=N`, save output to files, and use the `benchstat` tool to compute statistical significance:

```bash
$ go test -bench=BenchmarkXxx -count=10 > before.txt
# ... make your change ...
$ go test -bench=BenchmarkXxx -count=10 > after.txt
$ benchstat before.txt after.txt
```

---

### Fuzzing

Fuzzing automatically generates inputs to find cases where your code panics or violates a stated invariant. Added in Go 1.18.

```go
// FuzzXxx(f *testing.F) — the function signature for fuzz tests
func FuzzParseDate(f *testing.F) {
    // f.Add provides seed corpus entries — known-good starting inputs
    f.Add("2024-01-15")
    f.Add("1999-12-31")
    f.Add("") // edge case to seed

    // f.Fuzz is called with mutated versions of the seed corpus
    f.Fuzz(func(t *testing.T, input string) {
        // The invariant being tested: ParseDate must not panic,
        // and if it succeeds, the result must round-trip back to the same string.
        date, err := ParseDate(input)
        if err != nil {
            return // invalid input is fine — just check no panic
        }
        // Round-trip invariant: format the parsed date and re-parse it
        if date.Format("2006-01-02") != input {
            t.Errorf("ParseDate(%q) round-trip failed", input)
        }
    })
}
```

Running modes:
- `go test -run FuzzParseDate` — runs seed corpus only (fast, like a normal test)
- `go test -fuzz FuzzParseDate -fuzztime=60s` — actively fuzzes for 60 seconds
- When a crasher is found, it is written to `testdata/fuzz/FuzzParseDate/` — commit it to ensure the bug is never re-introduced

The fuzzer mutates inputs by flipping bits, inserting special characters, truncating, and combining corpus entries. It is most effective against: parsers, encoders/decoders, input validation, and mathematical invariants.

---

### Example Functions

Example functions serve two purposes: they are **runnable documentation** and **tests**. An example with an `// Output:` comment is compiled and run as a test; if the actual output doesn't match, the test fails.

```go
func ExampleAdd() {
    fmt.Println(Add(2, 3))
    fmt.Println(Add(-1, 1))
    // Output:
    // 5
    // 0
}

// Example for a method — naming convention: ExampleType_Method
func ExampleStack_Push() {
    s := &Stack{}
    s.Push(1)
    s.Push(2)
    fmt.Println(s.Len())
    // Output:
    // 2
}
```

Examples appear in `go doc` output and on pkg.go.dev. They are the most user-facing kind of test — they simultaneously document how a function is used and verify it works correctly. Unordered output can be tested with `// Unordered output:`.

---

### Coverage

Coverage shows which lines of code were executed during tests. It does not guarantee correctness — a line can be executed without the test actually verifying anything about it.

```bash
# Print coverage percentage
$ go test -cover ./...
ok      mypackage    0.012s  coverage: 84.2% of statements

# Write a coverage profile
$ go test -coverprofile=coverage.out ./...

# View HTML report — highlights covered (green) and uncovered (red) lines
$ go tool cover -html=coverage.out

# Print function-level coverage to terminal
$ go tool cover -func=coverage.out
mypackage/calculator.go:8:  Add     100.0%
mypackage/calculator.go:15: Divide  75.0%
```

**What coverage tells you:** which code paths were not exercised by any test.

**What coverage does not tell you:** whether the tests actually assert anything meaningful about the executed code. A test that calls every function but never checks the return value achieves 100% coverage with zero confidence.

A common target is 70–80% for business logic. Chasing 100% coverage leads to testing internal implementation details that should be free to change. Focus coverage on: error paths, boundary conditions, and public API surface.

---

### How the Concepts Fit Together

```
Code under test
      │
      │  depends on interfaces
      ▼
Interfaces ──────────── Hand-written fakes (in tests)
      │                         │
      │                         │ injected via interface
      ▼                         ▼
go test ./...           Test functions (TestXxx)
      │                   Table-driven tests
      │                   Subtests (t.Run)
      │                   t.Helper for helpers
      │
      ├── Benchmarks (BenchmarkXxx) ─── benchstat for comparisons
      │
      ├── Fuzz tests (FuzzXxx) ──── corpus in testdata/fuzz/
      │
      ├── Examples (ExampleXxx) ─── serve as documentation
      │
      └── Coverage (-coverprofile) ─── go tool cover -html
```

The testing ecosystem is layered: normal tests verify correctness, benchmarks verify performance, fuzz tests find edge cases, examples document usage, and coverage identifies untested paths. All of them run through the single `go test` command.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Using t.Fatal in a loop without t.Run**
>
> `t.Fatal` stops the entire test function. Inside a loop over test cases, calling `t.Fatal` on the first failure means subsequent cases never run — you lose visibility into whether other cases also fail.
>
> **Wrong:**
> ```go
> for _, tc := range tests {
>     got := Compute(tc.input)
>     if got != tc.want {
>         t.Fatalf("got %d; want %d", got, tc.want) // stops here on first failure
>     }
> }
> ```
>
> **Right (use t.Run + t.Errorf):**
> ```go
> for _, tc := range tests {
>     t.Run(tc.name, func(t *testing.T) {
>         got := Compute(tc.input)
>         if got != tc.want {
>             t.Errorf("got %d; want %d", got, tc.want) // reports failure, continues
>         }
>     })
> }
> ```
>
> **Why this matters:** When multiple test cases fail, seeing all failures at once is far more useful than fixing them one by one.

> [!WARNING]
> **Mistake 2: Forgetting tt := tt before t.Parallel() in a loop (pre-Go 1.22)**
>
> The range variable `tt` is reused on each iteration. When `t.Parallel()` is called, the subtest runs after the loop completes — by which time `tt` points to the last element.
>
> **Wrong (all subtests test the last case):**
> ```go
> for _, tt := range tests {
>     t.Run(tt.name, func(t *testing.T) {
>         t.Parallel()
>         // tt is captured by reference — ALL subtests see the last tt
>         got := Compute(tt.input)
>         if got != tt.want { ... }
>     })
> }
> ```
>
> **Right:**
> ```go
> for _, tt := range tests {
>     tt := tt // create a new variable scoped to this loop iteration
>     t.Run(tt.name, func(t *testing.T) {
>         t.Parallel()
>         got := Compute(tt.input)
>         if got != tt.want { ... }
>     })
> }
> ```

> [!WARNING]
> **Mistake 3: Writing a test helper without t.Helper()**
>
> Without `t.Helper()`, the failure message points inside the helper function — not to the test case that triggered the failure. This makes it significantly harder to identify which input caused the problem.
>
> Always call `t.Helper()` as the first line of any function that calls `t.Error`, `t.Fatal`, or their variants.

> [!WARNING]
> **Mistake 4: Measuring setup inside a benchmark without b.ResetTimer**
>
> If a benchmark generates test data before the measurement loop, that setup time is incorrectly included in the ns/op measurement. Always call `b.ResetTimer()` after any setup that should not be counted.

**Other pitfalls:**

- **Over-using t.Fatal in helpers** — a fatal inside a helper that is called from a `t.Run` subtest stops only the subtest (because subtests run in a separate goroutine). This is usually what you want, but be aware that `t.Fatal` in a goroutine spawned by the test (not a subtest) does not work — call `t.FailNow()` only from the test goroutine.
- **Testing implementation details** — tests that assert the internal state of a struct (not the observable behavior) break whenever the implementation changes. Prefer black-box tests (`package foo_test`) that test through the public API.
- **Treating 100% coverage as the goal** — coverage is a tool to find untested paths, not a metric to optimize. Chasing 100% leads to trivial tests that assert nothing meaningful.

---

## Mental Models

### Mental Model 1: Tests as Specifications

Think of a test not as "checking that the code works" but as **a machine-executable specification of how the code should behave**. The test table is a list of (input → expected output) facts about the function. If a test fails, either the code is wrong or the specification is wrong — both are valuable findings.

This model makes it natural to write tests before or alongside code (not after), to add cases for every edge case you can think of, and to keep tests in the same codebase as the code they specify. The test is not extra work — it is the spec made executable.

This model breaks down when tests verify internal implementation details instead of externally observable behavior. A test that checks `len(cache.entries) == 3` is not a specification of behavior — it is a brittle assertion about implementation.

### Mental Model 2: b.N as the Testing Framework's Job

Many beginners try to choose the number of benchmark iterations themselves. **Do not do this.** The framework adjusts `b.N` automatically until the benchmark runs for long enough to produce a stable measurement (by default, 1 second). Your only job is to write the measurement loop correctly:

```go
for i := 0; i < b.N; i++ {
    // One unit of work per iteration
}
```

Think of `b.N` as a dial the framework turns up until the results are statistically trustworthy. You write the loop; the framework chooses the dial setting.

### Mental Model 3: Fuzzing as a Second Programmer

Think of the fuzzer as an adversarial second programmer whose job is to break your function. You provide a few seed inputs and a statement of what should always be true (the invariant). The fuzzer then generates thousands of mutated inputs to find one that violates the invariant.

The invariant is usually one of: "this must not panic", "this must round-trip correctly" (parse then re-serialize gives the same result), or "the output must satisfy some property" (a sorted slice is actually sorted). The most valuable invariants are the ones you might not think to test manually — which is exactly where the fuzzer excels.

> [!NOTE]
> Use Model 1 (tests as specifications) when deciding what to test. Use Model 2 (b.N as the framework's job) when writing benchmarks. Use Model 3 (fuzzer as adversary) when identifying what invariants a fuzz test should assert.

---

## Practical Examples

### Example 1: Table-Driven Test with Error Cases _(Basic)_

**Scenario:** Testing a function that can return errors, where you need to verify both success cases and error cases.

**Goal:** Demonstrate the complete table-driven test pattern with error handling.

```go
package calc_test

import (
    "errors"
    "testing"

    "example.com/calc"
)

func TestDivide(t *testing.T) {
    tests := []struct {
        name    string
        a, b    float64
        want    float64
        wantErr bool
    }{
        {"positive", 10, 2, 5, false},
        {"negative dividend", -10, 2, -5, false},
        {"fractional result", 1, 3, 0.3333333333333333, false},
        {"divide by zero", 10, 0, 0, true},
        {"zero dividend", 0, 5, 0, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := calc.Divide(tt.a, tt.b)

            // Check error expectation first — if wrong, subsequent checks are meaningless
            if (err != nil) != tt.wantErr {
                t.Fatalf("Divide(%v, %v) error = %v; wantErr %v", tt.a, tt.b, err, tt.wantErr)
            }
            if tt.wantErr {
                return // error was expected — no need to check the result
            }
            if got != tt.want {
                t.Errorf("Divide(%v, %v) = %v; want %v", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

**Output (with -v):**
```
=== RUN   TestDivide
=== RUN   TestDivide/positive
=== RUN   TestDivide/negative_dividend
=== RUN   TestDivide/fractional_result
=== RUN   TestDivide/divide_by_zero
=== RUN   TestDivide/zero_dividend
--- PASS: TestDivide (0.00s)
    --- PASS: TestDivide/positive (0.00s)
    --- PASS: TestDivide/negative_dividend (0.00s)
    --- PASS: TestDivide/fractional_result (0.00s)
    --- PASS: TestDivide/divide_by_zero (0.00s)
    --- PASS: TestDivide/zero_dividend (0.00s)
PASS
```

**What to notice:** The `wantErr bool` field is the Go idiom for error case testing — not the specific error message (unless you need to check the error type with `errors.Is`). The `t.Fatalf` on error mismatch uses `t.Fatal` not `t.Error` because checking `got` when `wantErr` is wrong would be meaningless.

---

### Example 2: Benchmark with ResetTimer and ReportAllocs _(Intermediate)_

**Scenario:** Comparing two string-building strategies to determine which allocates less.

**Goal:** Show the complete benchmark pattern including setup, ResetTimer, and reading allocation output.

```go
package strutil_test

import (
    "fmt"
    "strings"
    "testing"
)

// BenchmarkSprintfConcat measures fmt.Sprintf for string building
func BenchmarkSprintfConcat(b *testing.B) {
    b.ReportAllocs() // equivalent to running with -benchmem
    for i := 0; i < b.N; i++ {
        _ = fmt.Sprintf("Hello, %s! You are visitor #%d.", "Alice", 42)
    }
}

// BenchmarkBuilderConcat measures strings.Builder for the same task
func BenchmarkBuilderConcat(b *testing.B) {
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        var sb strings.Builder
        sb.WriteString("Hello, ")
        sb.WriteString("Alice")
        sb.WriteString("! You are visitor #")
        fmt.Fprintf(&sb, "%d", 42)
        sb.WriteString(".")
        _ = sb.String()
    }
}

// BenchmarkWithHeavySetup shows b.ResetTimer usage
func BenchmarkWithHeavySetup(b *testing.B) {
    // This setup should NOT be measured — reset the timer after it
    data := make([]int, 1_000_000)
    for i := range data {
        data[i] = i
    }
    b.ResetTimer() // start measuring only from here

    for i := 0; i < b.N; i++ {
        _ = sumSlice(data)
    }
}

func sumSlice(data []int) int {
    total := 0
    for _, v := range data {
        total += v
    }
    return total
}
```

**Output:**
```
$ go test -bench=. -benchmem ./...
BenchmarkSprintfConcat-8      8523698   140.1 ns/op   64 B/op   2 allocs/op
BenchmarkBuilderConcat-8      7038291   170.3 ns/op   72 B/op   3 allocs/op
BenchmarkWithHeavySetup-8        1744   688213 ns/op   0 B/op   0 allocs/op
```

**What to notice:** `fmt.Sprintf` is faster here because the builder approach has extra method call overhead. The `BenchmarkWithHeavySetup` shows 0 allocs/op — the data structure was allocated in setup (not measured), and `sumSlice` doesn't allocate. The `-8` suffix means the benchmark ran with `GOMAXPROCS=8` (8 CPU threads available).

---

### Example 3: Fuzz Test for a Parser _(Applied)_

**Scenario:** A date parser function that might panic or misbehave on unusual inputs — the kind of thing that shows up in real APIs when user-supplied strings are parsed.

**Goal:** Demonstrate writing a fuzz test with a round-trip invariant.

```go
package dateutil_test

import (
    "testing"
    "time"
)

// ParseDate parses a date string in YYYY-MM-DD format.
// Returns an error for invalid input. Must never panic.
func ParseDate(s string) (time.Time, error) {
    return time.Parse("2006-01-02", s)
}

func FuzzParseDate(f *testing.F) {
    // Seed corpus: valid and interesting inputs
    f.Add("2024-01-15")
    f.Add("1999-12-31")
    f.Add("2000-02-29") // leap day — edge case
    f.Add("")
    f.Add("not-a-date")
    f.Add("9999-99-99")

    f.Fuzz(func(t *testing.T, input string) {
        // Invariant 1: ParseDate must never panic (guaranteed by using testing.F)

        date, err := ParseDate(input)
        if err != nil {
            // Invalid input is fine — the parser correctly rejected it
            return
        }

        // Invariant 2: if parsing succeeds, round-trip must be lossless
        formatted := date.Format("2006-01-02")
        reparsed, err := ParseDate(formatted)
        if err != nil {
            t.Errorf("round-trip failed: ParseDate(%q).Format() = %q, which does not re-parse: %v",
                input, formatted, err)
        }
        if !reparsed.Equal(date) {
            t.Errorf("round-trip value mismatch: ParseDate(%q) = %v, re-parsed = %v",
                input, date, reparsed)
        }
    })
}
```

**Running:**
```bash
# Run with seed corpus only (fast, runs in ~1ms)
$ go test -run FuzzParseDate ./...
PASS

# Actively fuzz for 30 seconds
$ go test -fuzz FuzzParseDate -fuzztime=30s ./...
fuzz: elapsed: 30s, execs: 1424815, new interesting: 42, corpus: 89
ok  	dateutil	30.023s
```

**What to notice:** The fuzz function receives the `*testing.T`, not `*testing.F`. The seed corpus entries become initial test cases when run with `-run FuzzParseDate` (no `-fuzz` flag). If a crasher is found, it is written to `testdata/fuzz/FuzzParseDate/` as a new corpus file.

---

### Example 4: Test Helper with t.Helper and t.Cleanup _(Edge Case)_

**Scenario:** Multiple tests need a temporary directory with specific files — extracting this into a helper avoids duplication but requires proper use of `t.Helper` and `t.Cleanup`.

```go
package processor_test

import (
    "os"
    "path/filepath"
    "testing"
)

// createTestDir creates a temp directory and populates it with files.
// It registers cleanup with t.Cleanup so the caller never needs to defer.
func createTestDir(t *testing.T, files map[string]string) string {
    t.Helper() // failures inside this function point to the caller

    dir, err := os.MkdirTemp("", "processor-test-*")
    if err != nil {
        t.Fatalf("create temp dir: %v", err)
    }
    t.Cleanup(func() { os.RemoveAll(dir) }) // always cleaned up

    for name, content := range files {
        path := filepath.Join(dir, name)
        if err := os.WriteFile(path, []byte(content), 0644); err != nil {
            t.Fatalf("write %s: %v", path, err)
        }
    }
    return dir
}

func TestProcessDirectory(t *testing.T) {
    // createTestDir's cleanup is registered with t.Cleanup — no defer needed here
    dir := createTestDir(t, map[string]string{
        "a.txt": "hello",
        "b.txt": "world",
    })

    count, err := ProcessDirectory(dir)
    if err != nil {
        t.Fatalf("ProcessDirectory: %v", err)
    }
    if count != 2 {
        t.Errorf("processed %d files; want 2", count)
    }
}
```

**Why this is important:** Without `t.Helper()`, a failure inside `createTestDir` (e.g., `os.MkdirTemp` fails) would report the line number inside the helper — the caller would have no idea which test triggered it. With `t.Helper()`, the failure points to the `createTestDir(t, ...)` call in the test that triggered it.

---

## Related Concepts

Within this topic:

- [[go/6. Methods and Interfaces]] — interfaces are the mechanism that makes code testable without frameworks; every fake in a Go test package is an interface implementation
- [[go/8. Error Handling]] — tests verify that functions return the right errors under the right conditions; `errors.Is` and `errors.As` are the correct tools for checking error types in tests
- [[go/16. Performance and Profiling]] — benchmarks are the entry point to performance work; `go test -bench` feeds into `benchstat` and `pprof` for deeper analysis

In other topics:

- [[go/13. Web Services and APIs]] — `net/http/httptest` is covered in this module as a preview; the full HTTP handler and middleware testing patterns live in Module 13
- [[memory-management]] — understanding heap allocations is what makes `allocs/op` in benchmark output meaningful; benchmarks that produce unexpected allocations are a signal to investigate escape analysis

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Table-Driven Test for a String Function** _(Easy)_
>
> Write a complete `_test.go` file with a table-driven test for a `Reverse(s string) string` function. Include at least 5 test cases covering empty string, single character, ASCII, palindrome, and a multi-word string.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-table-driven-test-for-a-string-function--easy--1-pt)

The exercises range from writing a basic table-driven test through benchmarking two implementations with `benchstat`, writing a fuzz test, and testing an HTTP handler with `httptest`. Complete at least the Easy and Medium exercises before taking the test.

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
Add a full test suite to an existing Go package you have written — a calculator, a word counter, or a simple HTTP handler from earlier exercises. Write table-driven tests for all public functions, at least one benchmark comparing two approaches (e.g., string concatenation vs `strings.Builder`), and a fuzz test for any function that accepts string input. Run `go test -race -cover ./...` and achieve at least 70% coverage.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[pkg.go.dev/testing](https://pkg.go.dev/testing)** — The official package documentation for `testing`; covers `*testing.T`, `*testing.B`, `*testing.F`, all methods, and includes examples. The most accurate and up-to-date reference for every method discussed in this module.
2. **[Go Fuzzing — go.dev/security/fuzz](https://go.dev/security/fuzz)** — The official Go fuzzing tutorial and reference; covers `testing.F`, the corpus model, running the fuzzer, and finding/reproducing crashers. Written by the Go team, reflects Go 1.18+ fuzzing exactly.
3. **[The Go Blog — Coverage for Go 1.20](https://go.dev/blog/coverage)** — Explains the coverage tooling, the `-coverprofile` flag, `go tool cover -html`, and the difference between statement coverage and line coverage. Also covers coverage for integration tests.
4. **"Learning Go" by Jon Bodner (2nd ed., O'Reilly) — Chapter 15: Writing Tests** — The most comprehensive book chapter on Go testing from a practitioner's perspective; covers table-driven tests, fakes vs mocks, benchmarks, and the philosophy of what to test. Highly recommended for the sections on when not to use mocking frameworks.

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 11

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
