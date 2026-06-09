# Answer Key — Module 16: Performance and Profiling

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

### 1.1 — `-benchmem` columns [1 pt]

**Full credit answer:**
`-benchmem` adds two columns: **`B/op`** (bytes allocated per operation — the total heap bytes allocated during one benchmark iteration, averaged over `b.N` iterations) and **`allocs/op`** (number of distinct heap allocations per operation — each call to `runtime.mallocgc` increments this counter). These two numbers are the primary signals for GC pressure reduction work.

**Key points required:**
- `B/op` = heap bytes per operation
- `allocs/op` = number of heap allocations per operation

**Common wrong answers:**
- *"It adds memory usage and CPU time"* — `-benchmem` is specifically about heap allocation counts and sizes, not total process memory or CPU.
- *"B/op is the stack size"* — `B/op` counts heap (GC-managed) bytes only; stack allocation is not counted.

---

### 1.2 — Five pprof profile types [1 pt]

**Full credit answer:**
1. **CPU** — where goroutines spend CPU time (sampled at ~100 Hz); which functions are executing
2. **Heap** — current live heap allocations and/or allocation sites; which code allocated the most memory
3. **Goroutine** — full stack traces of all currently live goroutines
4. **Block** — where goroutines block waiting on channel operations or mutex locks
5. **Mutex** — which mutexes are most contended (fraction of time spent blocked on a specific lock)

**Key points required:**
- All five names
- At least a one-sentence description distinguishing each (CPU ≠ heap, block ≠ mutex)

**Partial credit:** 0.5 pts if at least 3 of the 5 are correctly named and described.

---

### 1.3 — `b.ResetTimer` [1 pt]

**Full credit answer:**
`b.ResetTimer()` resets the benchmark's elapsed time and allocation counters to zero. You call it after any setup code that should not be included in the measurement — for example, after loading test fixtures, building large data structures, or pre-populating caches. Without it, the first few benchmark iterations (which include setup) skew the calibration of `b.N` and inflate the reported `ns/op`.

**Key points required:**
- Resets elapsed time (and allocation counters)
- Called after setup, before the `for range b.N` loop

**Common wrong answers:**
- *"It pauses the timer"* — `b.ResetTimer` resets (zeroes) the timer; `b.StopTimer`/`b.StartTimer` pause and resume it.
- *"It's called inside the loop"* — calling it inside the loop resets measurements on every iteration, making the benchmark meaningless.

---

### 1.4 — GOMEMLIMIT [1 pt]

**Full credit answer:**
`GOMEMLIMIT` is an environment variable (and programmatic equivalent `debug.SetMemoryLimit`) that sets a soft upper bound on the Go runtime's total memory usage. When the heap approaches the limit, the GC runs aggressively — regardless of the `GOGC` percentage — to stay under the cap. It was introduced in **Go 1.19**. It is particularly useful in containerized deployments where a pod has a fixed memory limit.

**Key points required:**
- Sets a hard (or soft) memory cap
- Go 1.19

---

### 1.5 — Escape analysis command [1 pt]

**Full credit answer:**
```bash
go build -gcflags='-m' ./...
```
For more verbose output (shows why each decision was made):
```bash
go build -gcflags='-m -m' ./...
```

**Key points required:**
- `go build` (not `go run` or `go test` — though `go test -gcflags=-m` also works)
- `-gcflags='-m'` (exact flag; `-m` is the escape analysis verbosity flag)

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Dead-code elimination in benchmarks [2 pts]

**Full credit answer:**
Dead-code elimination (DCE) is a compiler optimization that removes code whose output is never observed. If a function has no side effects and its return value is discarded, the compiler can prove it has no observable effect on the program and elides the call entirely.

Assigning to `_` fails because `_` is a syntactic discard — the compiler treats it as equivalent to not assigning at all; the return value is still "thrown away" from the compiler's perspective, and DCE still applies.

The correct fix is to assign the result to a package-level variable: `var sink T`. A package-level variable is accessible from other packages (in principle), so the compiler cannot prove that no one observes its value. Storing a result into `sink` forces the function call to be retained. The final `sink = result` assignment after the loop ensures the last value is "observed."

**Rubric:**
- 2 pts: Correctly explains DCE, why `_` fails, and why package-level sink works
- 1 pt: Correctly identifies the fix (package-level sink) but doesn't explain why `_` fails or why the sink works
- 0 pts: Says `_ = result` is sufficient, or doesn't understand what DCE is

---

### 2.2 — Critiquing the "optimize first" workflow [2 pts]

**Full credit answer:**
The workflow described violates the first and most important rule of performance engineering: measure before optimizing. The colleague optimized the JSON serialization layer based on a guess — not profiling data. This is problematic for two reasons:

1. The JSON serialization may not be the bottleneck. If JSON accounts for 3% of CPU time and a database call accounts for 60%, rewriting JSON has essentially no effect on end-to-end latency (Amdahl's Law: a 10× speedup on 3% of work reduces total time by only 2.7%).

2. Without a baseline measurement, there is no way to know whether the optimization actually helped. "It feels faster" is not engineering.

The correct workflow: (1) write a representative benchmark or attach `net/http/pprof` to the running service, (2) capture a CPU or heap profile, (3) read `top` to identify the actual hotspot, (4) optimize that specific location, (5) re-benchmark and confirm improvement with `benchstat`.

**Rubric:**
- 2 pts: Identifies the "measure first" failure AND explains what the correct workflow is AND mentions Amdahl's Law or the concept of dominant cost
- 1 pt: Identifies the "measure first" failure but doesn't explain the correct workflow or why it matters
- 0 pts: Agrees the approach is fine, or doesn't identify the missing measurement step

---

### 2.3 — Why heap allocations matter [2 pts]

**Full credit answer:**
Each heap allocation has two costs: the immediate allocation cost (~100–300 ns for the `runtime.mallocgc` call) and the deferred GC cost. Go uses a concurrent tricolor mark-and-sweep GC (detailed in [[go/17. Runtime Internals and the Memory Model]]): at collection time, the GC must trace every live heap object. More objects = more tracing work. Additionally, GC cycles compete with the application for CPU: `gcBgMarkWorker` goroutines use 25% of available CPUs by default during a GC cycle.

The consequence: a service that allocates 1 million short-lived objects per second generates constant GC pressure. If `runtime.mallocgc` appears in the top 3 of a CPU profile, the GC is consuming significant CPU — reducing allocations directly reduces GC CPU usage.

There is also a cache-locality effect (from [[memory-management]]): heap objects are scattered across memory; accessing many small heap objects causes cache misses. Stack allocations are contiguous and cache-friendly. Reducing heap allocations improves not just GC behavior but also CPU cache utilization.

**Rubric:**
- 2 pts: Explains GC tracing cost AND mentions GC CPU competition AND either cites cache effects or correctly connects to [[memory-management]] / [[go/17. Runtime Internals and the Memory Model]]
- 1 pt: Explains one of the two mechanisms (GC cost or cache) but misses the other
- 0 pts: Says allocations are "slow" without explaining why

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Benchmark for countVowels [3 pts]

**Full credit answer:**
```go
package main

import (
    "strings"
    "testing"
)

var intSink int // package-level sink prevents DCE

func BenchmarkCountVowels(b *testing.B) {
    // Setup: build a realistic 100-word sentence (excluded from measurement)
    words := make([]string, 100)
    for i := range words {
        words[i] = "Hello World"
    }
    input := strings.Join(words, " ")

    b.ResetTimer() // exclude setup — start measuring here

    var result int
    for range b.N { // Go 1.22+ range-over-integer
        result = countVowels(input)
    }
    intSink = result // prevent DCE: force result to be observed
}
```

**Step-by-step reasoning:**
1. Package-level `intSink` prevents DCE — `countVowels` returns an `int`; storing to a package-level `int` forces the call to be retained.
2. `b.ResetTimer()` is called after `input` is built; setup is excluded from measurement.
3. `for range b.N` is the Go 1.22+ range-over-integer form (equivalent to `for i := 0; i < b.N; i++`).
4. 100 words × ~11 chars/word = ~1100-character string — a realistic input that exercises the loop meaningfully.

**Rubric:**
- 3 pts: Package-level sink, `b.ResetTimer`, realistic input setup before reset, Go 1.22+ range syntax, result assigned to local and then sink
- 2 pts: Missing one element (e.g., no Grow or no ResetTimer) but otherwise correct
- 1 pt: Correct overall structure but two issues (e.g., sink is wrong type, or sink is inside the loop)
- 0 pts: No sink, or benchmark loop is structurally wrong

**Acceptable alternatives:**
- Using any string that is at least 50 characters — the exact input string is not critical as long as setup is excluded and DCE is prevented.
- `var sink any` with `sink = result` also works.

---

### 3.2 — Rewrite midpoint to eliminate escape [3 pts]

**Full credit answer:**

**Analysis:**
`go build -gcflags='-m'` for `midpoint` shows:
```
./midpoint.go: &Point{...} escapes to heap
```
The cause: `midpoint` returns `*Point` — taking the address of a local struct literal forces it to the heap because the caller holds the pointer after the function returns.

**Rewrite:**
```go
// Returns value: Point stays on stack
func midpoint(a, b Point) Point {
    return Point{
        X: (a.X + b.X) / 2,
        Y: (a.Y + b.Y) / 2,
    }
}
```

`go build -gcflags='-m'` for the rewritten version: no escape line for `Point`.

**Explanation:** Returning by value means the `Point` is copied into the caller's stack frame. No pointer escapes the function, so the compiler can keep the struct on the stack entirely. The caller can take the address of their local copy if needed: `p := midpoint(a, b); processPtr(&p)` — as long as `p` lives in the caller's frame and `processPtr` doesn't store the pointer, no escape occurs.

**Rubric:**
- 3 pts: Correctly identifies the escape cause (return pointer), rewrites to return value, explains why it works, and confirms elimination with `-gcflags=-m` output or correct reasoning
- 2 pts: Correct rewrite but incomplete explanation (e.g., doesn't explain why returning by value avoids escape)
- 1 pt: Identifies the problem but rewrite is wrong or changes function behavior
- 0 pts: Cannot identify the escape or cannot rewrite correctly

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Broken benchmark analysis [3 pts] (1 pt each part)

**(a) What is wrong — all bugs:**

**Bug 1: Dead-code elimination** — `decodeImage(imageData)` is called but its return value (`*Image`) is not captured. The compiler can optimize away the call entirely since `decodeImage` (assumed to have no side effects) produces no observable result. This makes the benchmark measure loop overhead (~0.3–1 ns/op) rather than actual image decoding (~microseconds or more).

**Bug 2: Missing `b.ResetTimer`** — `os.ReadFile("testdata/sample.png")` runs before the measurement loop and takes ~5 ms. This setup time is included in the first iteration (b.N=1 probe). The framework calibrates `b.N` based on a total time that is dominated by the file read, not the actual operation, producing an artificially low `ns/op` for all subsequent iterations.

**(b) What each bug causes:**

Bug 1 (DCE): The benchmark reports ~0.8 ns/op because only the loop increment is measured — the actual `decodeImage` call is gone. The developer sees "0.8 ns" and concludes the function is nearly free, which is completely wrong.

Bug 2 (missing ResetTimer): Even if DCE were fixed, the reported time would average in the 5 ms file-read cost. For large `b.N`, this is diluted (5ms / 1000 iterations = 5µs overhead per op — small but nonzero). For small `b.N`, it dominates entirely.

**(c) Corrected benchmark:**
```go
var imgSink any // package-level sink (using any since *Image type not shown)

func BenchmarkDecodeImage(b *testing.B) {
    imageData, err := os.ReadFile("testdata/sample.png")
    if err != nil {
        b.Fatal(err)
    }

    b.ResetTimer() // exclude file read from measurement

    var result *Image
    for range b.N { // Go 1.22+ range-over-integer
        result = decodeImage(imageData)
    }
    imgSink = result // prevent DCE
}
```

**Rubric:**
- 1 pt for (a): Identifies both bugs (DCE and missing ResetTimer); partial credit for identifying only one
- 1 pt for (b): Correctly explains what each bug causes to the reported `ns/op`; partial credit if only one is explained
- 1 pt for (c): Corrected benchmark has package-level sink, `b.ResetTimer` after file read, and result captured before sink assignment

---

## Section 5: Discussion — Answer Key

### 5.1 — When to preallocate [2 pts]

**Example strong answer:**
Preallocation is clearly the right choice when you know (or can cheaply compute) the exact or approximate capacity before populating the collection, and when the collection will be large enough that reallocation overhead is measurable. The classic case: `result := make([]string, 0, len(input))` before a transform loop — each `append` uses the pre-reserved capacity and no reallocation occurs. Similarly, preallocating a map with `make(map[K]V, n)` avoids O(log n) rehashing events during insertion.

However, preallocation can add complexity without benefit when: the capacity is unknown and the estimate requires expensive computation (now setup is more expensive than reallocation); the collection is small (1–5 elements); or the preallocated capacity is frequently wrong (a bad estimate is no better than no estimate, and a wrong estimate wastes memory). A benchmark is the correct decision-making tool: if `-benchmem` shows `1 allocs/op` regardless, preallocation added code for no gain; if it shows 10 or 50 allocs from reallocation, preallocation is worth the line of code.

**Elements that earn full credit:**
- States the clear case for preallocation (known capacity, large collection, measurable reallocation cost)
- States at least one case where it adds complexity without benefit
- Mentions that a benchmark is the right tool for the decision

**Rubric:**
- 2 pts: Covers both perspectives; mentions benchmarking as the decision tool; conclusion is practical and nuanced
- 1 pt: Only one perspective, or vague ("it depends") without examples
- 0 pts: Blanket "always preallocate" or "never preallocate" without reasoning

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Profile-Guided Optimization [+5 pts]

**Full credit answer:**

**(a) Mechanism:**
PGO uses a CPU profile (a `default.pgo` file, in pprof format) as an additional input to the compiler. The profile identifies which functions are "hot" (frequently called) at runtime. With this information, the compiler makes two primary improvements: (1) **more aggressive inlining** at hot call sites — functions that are normally too large to inline get inlined when the profile shows they are called extremely frequently; (2) **devirtualization** — when the profile shows that an interface method call almost always dispatches to one specific concrete type, the compiler can generate a direct call for that case (with a type check), eliminating the interface dispatch overhead.

**(b) Steps to collect and apply:**
```bash
# Step 1: Collect a representative CPU profile
# Option A: from a benchmark
go test -bench=. -cpuprofile=default.pgo ./...

# Option B: from a live service (30-second window)
curl -o default.pgo http://localhost:6060/debug/pprof/profile?seconds=30

# Step 2: Place default.pgo in the module root (where go.mod is)
# (the go build tool picks it up automatically)

# Step 3: Build with PGO applied automatically
go build ./...
# Or verify PGO is being used:
go build -pgo=default.pgo ./...
```

**(c) Programs that benefit most:**
Programs with many hot interface method calls benefit most — gRPC servers, HTTP middleware chains, JSON codecs, and plugin-style architectures where interfaces dispatch to a small set of concrete types. The devirtualization benefit is highest when one concrete type accounts for >90% of calls at a hot interface site. Programs that are already allocation-bound or I/O-bound see less benefit because PGO primarily helps CPU-bound code.

**(d) Limitation/caveat:**
The profile must represent a realistic production workload. A profile from a microbenchmark optimizes for the benchmark's access patterns, which may differ from production (e.g., skewed hot paths, different call frequencies). In a CI pipeline, you must commit the `default.pgo` file and refresh it periodically from production traffic; a stale profile doesn't harm correctness (PGO is a hint, not a constraint) but reduces benefit over time. Also: PGO is not free — build times increase slightly because the compiler does more analysis.

**Rubric:**
- 5 pts: Correctly explains inlining and devirtualization; provides exact commands; identifies interface-heavy programs as best candidates; names a real limitation (stale profile, build-time cost, or workload representativeness)
- 3 pts: Correct explanation of mechanism and commands, but missing one of: candidate program types, or limitation
- 1 pt: Generally correct direction but missing 2+ elements or has conceptual errors
- 0 pts: Incorrect description of PGO's mechanism

**Bonus teaching note:**
PGO is a uniquely Go-first topic at this level. Students who score full credit demonstrate that they have gone beyond the module's core content. The key distinction to check: does the student understand that PGO improves *inlining decisions*, not algorithmic complexity? A student who says "PGO makes the code faster by optimizing the algorithm" misunderstands the mechanism.

---

## Common Wrong Answers Across the Test

1. **Confusing `flat` and `cum` in pprof** — `flat` is time spent *in* the function; `cum` is time spent in the function *and all its callees*. A function with high `cum` but low `flat` is a slow caller, not a slow function. Students who use `top -cum` to find hotspots need to understand they are finding callers, not the actual slow code; use `list` to drill down.

2. **Thinking `-benchmem` measures total process memory** — `-benchmem` measures heap allocations during the benchmark loop only: bytes allocated and number of allocations per operation. It does not measure RSS, virtual memory, or stack usage.

3. **Using `b.StopTimer`/`b.StartTimer` inside the loop as a substitute for `b.ResetTimer`** — Stop/Start are correct for excluding setup that happens *inside each iteration* (e.g., reset a data structure between iterations). `ResetTimer` is for excluding one-time setup before the loop. Confusing these produces incorrect measurements.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who score poorly on Section 2 (conceptual) likely understand the mechanics but haven't internalized the *why* — they can benchmark but don't understand what the numbers mean. Recommend re-reading the "Performance Mindset" section and the "Allocations as Garbage" mental model.
- Students who score poorly on Section 3 (applied) need more hands-on practice — re-do EXERCISES.md Exercises 1–4 and run the commands for real.
- The bonus question distinguishes a learner who has only read the module from one who has engaged with the broader Go ecosystem. Don't be concerned if most students skip it; it tests knowledge of a specialized feature.
- A score below 60% typically means the benchmarking foundations from [[go/11. Testing and Benchmarking]] were not solid. Ask the student to re-read that module before continuing.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
