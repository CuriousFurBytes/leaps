# Module 16: Performance and Profiling

[← Module 15: Reflection and Metaprogramming](../15.%20Reflection%20and%20Metaprogramming/) | [Topic Home](../README.md) | [Module 17: Runtime Internals and the Memory Model →](../17.%20Runtime%20Internals%20and%20the%20Memory%20Model/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [The Performance Mindset](#the-performance-mindset)
  - [Benchmarking Discipline](#benchmarking-discipline)
  - [Comparing Benchmark Runs with benchstat](#comparing-benchmark-runs-with-benchstat)
  - [pprof — Go's Profiler](#pprof--gos-profiler)
  - [Capturing Profiles](#capturing-profiles)
  - [Using go tool pprof](#using-go-tool-pprof)
  - [go tool trace](#go-tool-trace)
  - [Escape Analysis and Heap Allocations](#escape-analysis-and-heap-allocations)
  - [Concrete Optimizations](#concrete-optimizations)
  - [Inlining](#inlining)
  - [GC Tuning — GOGC and GOMEMLIMIT](#gc-tuning--gogc-and-gomemlimit)
  - [Profile-Guided Optimization (PGO)](#profile-guided-optimization-pgo)
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

This module covers **performance measurement and optimization in Go**: how to benchmark correctly, capture CPU and memory profiles, read pprof output, reason about heap allocations through escape analysis, apply concrete optimizations, and tune the garbage collector. It also introduces Profile-Guided Optimization (PGO), available by default since Go 1.21.

By the end of this module, you will have a repeatable workflow for turning a slow Go program into a fast one — without guessing. You will understand *why* allocations matter (GC pressure, cache misses), *how* to find the bottleneck objectively, and *which* techniques to reach for first.

**Difficulty:** Expert &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Articulate the performance mindset (measure first, optimize the right thing, correctness before speed) — _given a "slow" service, describe the workflow you would follow before writing a single line of optimization code_
2. Write correct benchmarks with `testing.B`, use `-benchmem`, and detect common pitfalls like dead-code elimination and missing `b.ResetTimer` — _identify why a benchmark reports suspiciously fast numbers and fix it_
3. Capture CPU, heap, block, mutex, and goroutine profiles using `testing` flags, `runtime/pprof`, and `net/http/pprof` — _add live profiling to a running HTTP service with four lines of code_
4. Use `go tool pprof` (top, list, web/flamegraph) and `go tool trace` to pinpoint bottlenecks — _read a CPU profile and identify the top-3 allocation sites_
5. Run `go build -gcflags=-m` to read escape-analysis output and explain why a variable escapes to the heap — _rewrite a function to keep a value on the stack and confirm with `-gcflags=-m`_
6. Apply at least five concrete optimizations (preallocation, `strings.Builder`, `sync.Pool`, avoiding interface boxing, reducing `string`↔`[]byte` copies) and verify the improvement with a benchmark — _show before/after allocation numbers with `-benchmem`_
7. Tune `GOGC` and `GOMEMLIMIT` for a given workload and explain the tradeoff each knob makes — _choose between raising GOGC and setting GOMEMLIMIT for a latency-sensitive vs. throughput-oriented service_

---

## Prerequisites

### Required Modules

- [[go/11. Testing and Benchmarking]] — you need to understand: how `testing.B` works, the benchmark loop (`for b.N`), `-bench` and `-benchmem` flags, and how to run benchmarks with `go test`
- [[go/4. Composite Types]] — you need to understand: slices and maps deeply — `make` with capacity, `append`, and why over-allocating is sometimes the right move
- [[go/9. Concurrency]] — you need to understand: goroutines, `sync.Mutex`, and `sync.Pool` interface (pool is used as an optimization primitive)

### Required Concepts

- **Garbage collection basics** — understanding that Go's GC is a tricolor mark-and-sweep that runs concurrently, and that allocations on the heap create GC pressure; see [[memory-management]]
- **Stack vs. heap allocation** — knowing that stack allocation is fast and free at function return, while heap allocation is managed by the GC; this is the lens through which escape analysis is understood
- **CPU caches and locality** — intuition that cache-friendly, contiguous-memory access patterns (e.g., slices of values rather than slices of pointers) are faster; this underpins many concrete optimizations

> [!TIP]
> If benchmarking feels fuzzy, re-read [[go/11. Testing and Benchmarking]] before continuing.
> The profiling tools in this module build directly on the benchmarking primitives from Module 11.

---

## Why This Matters

Performance work is the skill that separates engineers who can build a service from engineers who can keep it running under production load. A service that is correct but too slow to handle real traffic is not production-ready.

Concretely, mastery of this module enables you to:

- **Diagnose production latency regressions** — attach `net/http/pprof` to a live service (or grab a heap dump), identify the function spending 40% of CPU time, and fix it without guessing
- **Reduce infrastructure cost** — halving allocations per request often halves memory usage and GC overhead, which can directly reduce cloud instance count; teams routinely cut costs 20–50% with targeted allocation optimizations
- **Write performance-sensitive library code** — libraries used by thousands of callers must be allocation-conscious; understanding escape analysis and `sync.Pool` is expected of a senior Go engineer writing such code

Without this knowledge, you would be limited to "throw more hardware at it" as a response to performance problems — expensive, slow, and often insufficient for fundamentally algorithmic bottlenecks.

---

## Historical Context

Go's profiling story was established early. The `runtime/pprof` package has been part of the standard library since Go 1.0 (2012), and the `go tool pprof` command was available from the start, drawing on the `pprof` profiling tool originally developed at Google as part of the gperftools project (C/C++).

Key milestones:

- **2012 (Go 1.0)** — `runtime/pprof` and `net/http/pprof` shipped in the standard library; the `testing` package supported `-cpuprofile` from the start
- **2014** — Google open-sourced the standalone `pprof` tool; the Go-native `go tool pprof` was rewritten in Go and gained a web-based flamegraph UI
- **2017 (Go 1.9)** — `GOGC` was long-established; `runtime.ReadMemStats` API stabilized
- **2019 (Go 1.13)** — `go tool trace` matured; the execution tracer now shows goroutine scheduling, GC events, and syscall latency on a timeline
- **2022 (Go 1.19)** — `GOMEMLIMIT` introduced, giving operators a hard cap on memory usage independent of `GOGC`, useful for containerized deployments
- **2023 (Go 1.21)** — Profile-Guided Optimization (PGO) enabled by default: if a `default.pgo` file exists in the module root, the compiler automatically applies CPU profile data to optimize inlining and branch prediction

Understanding this history explains why some patterns (e.g., attaching `net/http/pprof`) feel like they were designed for production from day one — they were.

---

## Core Concepts

### The Performance Mindset

Before touching any tooling, internalize these three rules:

1. **Measure before optimizing.** Intuition about what is slow is almost always wrong. The function you think is the bottleneck rarely is. Always profile first.
2. **Optimize the right thing.** A 10× speedup on code that accounts for 1% of runtime saves 0.9% of total time. Amdahl's Law: find the dominant cost and reduce it.
3. **Correctness before speed.** An incorrect program that is fast is still incorrect. Never introduce a bug to gain performance.

```go
// The wrong workflow:
// 1. Notice program is slow
// 2. Guess it's the string formatting
// 3. Rewrite string formatting
// 4. Program is still slow (bottleneck was elsewhere)

// The right workflow:
// 1. Notice program is slow
// 2. Write a benchmark or attach a profiler
// 3. Read the profile — find the actual hotspot
// 4. Optimize THAT
// 5. Re-benchmark to confirm improvement
// 6. Repeat if needed
```

---

### Benchmarking Discipline

Benchmarks in Go use the `testing.B` type, covered in [[go/11. Testing and Benchmarking]]. This section focuses on discipline and correctness — the things that make benchmarks trustworthy.

**The benchmark loop:**

```go
// process_test.go
package main

import (
    "testing"
)

func BenchmarkProcessMessage(b *testing.B) {
    msg := "hello, world — this is a test message for benchmarking"

    b.ResetTimer() // exclude setup above from measurement

    for range b.N { // Go 1.22+: range over integer
        _ = processMessage(msg) // assign to _ to prevent dead-code elimination
    }
}
```

Run with allocation statistics:

```bash
go test -bench=BenchmarkProcessMessage -benchmem -count=5 ./...
```

Realistic output:

```
BenchmarkProcessMessage-8   3842107   310.4 ns/op   128 B/op   3 allocs/op
BenchmarkProcessMessage-8   3901234   308.1 ns/op   128 B/op   3 allocs/op
BenchmarkProcessMessage-8   3855221   312.8 ns/op   128 B/op   3 allocs/op
BenchmarkProcessMessage-8   3870009   309.9 ns/op   128 B/op   3 allocs/op
BenchmarkProcessMessage-8   3843001   311.5 ns/op   128 B/op   3 allocs/op
```

**`-benchmem`** adds `B/op` (bytes allocated per operation) and `allocs/op` (number of distinct allocations). These are the most actionable numbers for GC pressure reduction.

**`-count=N`** runs the benchmark N times, giving you multiple data points to feed into `benchstat`.

---

### Comparing Benchmark Runs with benchstat

Never compare benchmark results by eye — variance is significant. Use `benchstat` from `golang.org/x/perf`:

```bash
# Install once
go install golang.org/x/perf/cmd/benchstat@latest

# Capture baseline
go test -bench=. -benchmem -count=10 ./... > before.txt

# Apply optimization, then capture again
go test -bench=. -benchmem -count=10 ./... > after.txt

# Compare
benchstat before.txt after.txt
```

Realistic `benchstat` output:

```
name                    old time/op    new time/op    delta
ProcessMessage-8          311ms ± 1%     198ms ± 2%   -36.34%  (p=0.000 n=10+10)

name                    old alloc/op   new alloc/op   delta
ProcessMessage-8          128B ± 0%       0B ± 0%    -100.00%  (p=0.000 n=10+10)

name                    old allocs/op  new allocs/op  delta
ProcessMessage-8           3.00 ± 0%      0.00 ± 0%    -100.00%  (p=0.000 n=10+10)
```

The p-value confirms statistical significance. A delta without a p-value is just noise.

---

### pprof — Go's Profiler

Go ships five profile types:

| Profile | Flag | What it measures |
|---------|------|-----------------|
| CPU | `-cpuprofile` | Where goroutines spend CPU time (sampled at ~100 Hz) |
| Heap | `-memprofile` | Current live heap allocations (or allocation sites) |
| Goroutine | — | Stack traces of all live goroutines |
| Block | — | Where goroutines block on channel/mutex operations |
| Mutex | — | Contended mutex operations |

**CPU profile** answers: *where does the program spend time?*
**Heap profile** answers: *which code sites allocate the most memory?*
**Block/Mutex profiles** answer: *where do goroutines wait for each other?*

---

### Capturing Profiles

**Via `go test` flags** — simplest, for code you can benchmark:

```bash
# CPU profile
go test -bench=BenchmarkProcessMessage -cpuprofile=cpu.out ./...

# Heap profile (allocation profile)
go test -bench=BenchmarkProcessMessage -memprofile=mem.out ./...
```

**Via `runtime/pprof`** — for batch programs or custom profiling windows:

```go
package main

import (
    "os"
    "runtime/pprof"
)

func main() {
    // CPU profile: start before work, stop after
    f, _ := os.Create("cpu.out")
    defer f.Close()
    pprof.StartCPUProfile(f)
    defer pprof.StopCPUProfile()

    // ... your program's work here ...

    // Heap profile: capture at the interesting point
    mf, _ := os.Create("mem.out")
    defer mf.Close()
    defer pprof.WriteHeapProfile(mf)
}
```

**Via `net/http/pprof`** — for long-running HTTP services (zero code change to business logic):

```go
package main

import (
    "net/http"
    _ "net/http/pprof" // side-effect import registers /debug/pprof handlers
)

func main() {
    // Your existing server setup...
    http.ListenAndServe(":6060", nil) // pprof available on this port
}
```

Then capture profiles from a live service:

```bash
# 30-second CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Heap profile (live allocations)
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile (all goroutine stacks)
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

> [!WARNING]
> **Never expose `net/http/pprof` on a public port in production.** It leaks internal details and can be used to cause CPU spikes. Always bind it to `localhost` or protect it with authentication.

---

### Using go tool pprof

Once you have a profile file (e.g., `cpu.out`), analyze it:

```bash
go tool pprof cpu.out
```

This opens an interactive shell. Key commands:

| Command | What it shows |
|---------|--------------|
| `top` | Top N functions by self/cumulative CPU time |
| `top -cum` | Sort by cumulative time (includes callees) |
| `list FuncName` | Annotated source for a specific function |
| `web` | Open a call graph in your browser (requires Graphviz) |
| `png` | Save call graph as PNG |

Realistic `top` output from a CPU profile:

```
(pprof) top10
Showing nodes accounting for 2.41s, 82.53% of 2.92s total
Dropping nodes with < 0.01s
      flat  flat%   sum%        cum   cum%
     0.83s 28.42% 28.42%      0.83s 28.42%  runtime.mallocgc
     0.41s 14.04% 42.47%      1.22s 41.78%  strings.(*Builder).WriteString
     0.37s 12.67% 55.14%      0.37s 12.67%  runtime.memmove
     0.29s  9.93% 65.07%      2.14s 73.29%  main.processMessages
     0.21s  7.19% 72.26%      0.21s  7.19%  runtime.gcBgMarkWorker
```

**`flat` time** is time spent in the function itself. **`cum` (cumulative) time** includes all callees. If `mallocgc` or `gcBgMarkWorker` appears near the top, the program is allocation-heavy — reduce allocations before optimizing anything else.

**Flamegraphs** — the most intuitive view:

```bash
go tool pprof -http=:8080 cpu.out
```

Opens a web UI with flamegraph, top, source, and graph views. The flamegraph shows the call stack as stacked horizontal bars; wider bars = more time. Read from bottom (main) to top (leaf functions).

---

### go tool trace

`go tool trace` captures scheduler events, GC events, goroutine creation/blocking, and syscall latency on a microsecond timeline. It is more powerful than pprof for diagnosing goroutine contention, GC latency spikes, and scheduler delays.

```bash
# Capture a trace (from a test)
go test -trace=trace.out ./...

# Open in the browser
go tool trace trace.out
```

The trace viewer shows goroutines as horizontal swim lanes, GC pauses as red bands, and scheduling delays as gaps. If GC pause bands are wide or frequent, the program is over-allocating. If goroutines show long blocking gaps, look at contention with the mutex or block profile.

`go tool trace` is the right tool when:
- pprof shows low CPU time but latency is high (scheduling or GC issue)
- Goroutines are being created/destroyed rapidly
- You need to understand scheduling pauses at microsecond resolution

---

### Escape Analysis and Heap Allocations

The Go compiler performs **escape analysis** at compile time: it determines whether each variable's lifetime is bounded by the function that creates it (stack-safe) or might outlive it (must escape to heap).

**Why it matters:** Stack allocation is free at function return — the stack frame is simply popped. Heap allocation requires the GC to track and eventually collect the object. Each heap allocation has ~100–300 ns overhead, and the aggregate GC pressure from millions of small allocations per second is a real bottleneck in production services.

Read escape analysis output:

```bash
go build -gcflags='-m' ./...
# Or more verbose:
go build -gcflags='-m -m' ./...
```

Example source and output:

```go
// escape_demo.go
package main

import "fmt"

// result does NOT escape — it's returned by value, used and discarded
func sumSlice(nums []int) int {
    result := 0
    for _, n := range nums {
        result += n
    }
    return result
}

// msg DOES escape — taking its address and storing it outside the function
func makeMessage(s string) *string {
    msg := "prefix: " + s // msg escapes because we return its address
    return &msg
}

func main() {
    nums := []int{1, 2, 3, 4, 5}
    fmt.Println(sumSlice(nums))
    m := makeMessage("hello")
    fmt.Println(*m)
}
```

```bash
$ go build -gcflags='-m' escape_demo.go
./escape_demo.go:14:2: msg escapes to heap
./escape_demo.go:7:16: nums does not escape
```

**Common causes of escape to heap:**
- Returning a pointer to a local variable
- Storing a value in an interface (interface boxing — the value is heap-copied)
- Slices/maps passed to functions where the compiler cannot prove the size
- Closures that capture a variable (the variable lives on the heap)
- Values stored in structs that outlive the current frame

**Reducing escapes:**

```go
// Before: msg escapes (pointer returned)
func buildTag(key, val string) *string {
    s := key + "=" + val
    return &s
}

// After: return by value, no escape
func buildTag(key, val string) string {
    return key + "=" + val
}
```

See also [[memory-management]] and [[go/17. Runtime Internals and the Memory Model]] for the GC mechanics that make allocation costs matter.

---

### Concrete Optimizations

**1. Preallocate slices and maps with capacity**

```go
// Bad: repeated reallocation as slice grows
func collectItems(n int) []string {
    var result []string          // starts with nil, len=0, cap=0
    for i := range n {
        result = append(result, fmt.Sprintf("item-%d", i))
    }
    return result
}

// Good: single allocation, known capacity upfront
func collectItems(n int) []string {
    result := make([]string, 0, n) // pre-allocate for n items
    for i := range n {
        result = append(result, fmt.Sprintf("item-%d", i))
    }
    return result
}
```

Similarly for maps: `make(map[K]V, expectedSize)`.

**2. Use `strings.Builder` for string concatenation**

```go
// Bad: O(n²) — each + creates a new string copy
func joinWords(words []string) string {
    result := ""
    for _, w := range words {
        result += w + " "   // new allocation per iteration
    }
    return result
}

// Good: single underlying buffer, amortized O(n)
func joinWords(words []string) string {
    var sb strings.Builder
    sb.Grow(estimatedLen(words)) // optional: pre-grow to avoid reallocation
    for _, w := range words {
        sb.WriteString(w)
        sb.WriteByte(' ')
    }
    return sb.String()
}
```

**3. Avoid unnecessary `string`↔`[]byte` conversions**

```go
// Bad: converts string to []byte, allocates
func toLowerSlice(s string) []byte {
    b := []byte(strings.ToLower(s)) // two allocs: ToLower + conversion
    return b
}

// Good: use bytes package directly when working with []byte
func toLowerSlice(s []byte) []byte {
    return bytes.ToLower(s) // in-place if caller can provide buffer
}

// Also good: when you need to read from a string without allocating,
// use unsafe conversion (only when you do NOT mutate the slice):
// import "unsafe"
// b := unsafe.Slice(unsafe.StringData(s), len(s)) // zero-copy read
```

**4. `sync.Pool` for frequently-allocated, short-lived objects**

```go
var bufPool = sync.Pool{
    New: func() any {
        // allocate a new buffer if the pool is empty
        b := make([]byte, 0, 4096)
        return &b
    },
}

func processRequest(req []byte) []byte {
    // Get a buffer from the pool (or allocate a new one)
    bufPtr := bufPool.Get().(*[]byte)
    buf := (*bufPtr)[:0] // reset length, keep capacity

    defer func() {
        *bufPtr = buf
        bufPool.Put(bufPtr) // return to pool for reuse
    }()

    // ... build response in buf ...
    result := make([]byte, len(buf))
    copy(result, buf)
    return result
}
```

`sync.Pool` is not a cache — the GC can evict pool entries at any time. Use it for objects that are: expensive to allocate, short-lived (within a request), and frequently needed.

**5. Avoid interface boxing in hot loops**

```go
// Bad: storing int in interface{} boxes it onto the heap each iteration
func sumInterface(nums []interface{}) int {
    total := 0
    for _, v := range nums {
        total += v.(int) // type assertion + unbox
    }
    return total
}

// Good: use concrete types in hot paths
func sumConcrete(nums []int) int {
    total := 0
    for _, v := range nums {
        total += v
    }
    return total
}

// When you need generics: use type parameters (Go 1.18+)
func sumGeneric[T int | int64 | float64](nums []T) T {
    var total T
    for _, v := range nums {
        total += v
    }
    return total
}
```

---

### Inlining

The Go compiler inlines small, simple functions automatically. Inlining eliminates the call overhead (stack frame setup, argument passing, return) and enables further optimizations like escape analysis across the call boundary.

```bash
# See what the compiler inlines:
go build -gcflags='-m' ./...
# Look for: "can inline FuncName" and "inlining call to FuncName"
```

Functions that prevent inlining:
- Contains a `for` loop (in older Go versions; improved in recent releases)
- Too many AST nodes (complexity budget exceeded)
- Contains `recover()`
- Is a method on an interface (interface dispatch is dynamic)

To force inlining for a specific function (discouraged except in stdlib/hot paths):

```go
//go:nosplit — prevents stack growth, implicitly limits complexity
// Prefer writing simpler functions and letting the compiler decide
```

The practical takeaway: keep hot-path functions small and focused. If `go build -gcflags=-m` shows "too complex to inline" for a function you care about, consider breaking it into smaller pieces.

---

### GC Tuning — GOGC and GOMEMLIMIT

**`GOGC`** — the GC target percentage. Default is `100`, meaning: trigger GC when live heap has doubled since last collection. Higher `GOGC` = less frequent GC = lower CPU overhead = higher peak memory. Lower `GOGC` = more frequent GC = more CPU overhead = lower peak memory.

```bash
# Reduce GC frequency (better throughput, more memory use)
GOGC=200 ./myservice

# Increase GC frequency (lower latency, more CPU)
GOGC=50 ./myservice

# Disable GC entirely (for batch jobs where you'll exit soon)
GOGC=off ./mybatchjob
```

**`GOMEMLIMIT`** (Go 1.19+) — a hard cap on the Go runtime's memory use. When the heap approaches the limit, GC runs aggressively regardless of `GOGC`. This is the right knob for containerized services with a fixed memory limit:

```bash
# Cap Go runtime memory at 512 MiB (useful in a 512Mi container)
GOMEMLIMIT=512MiB ./myservice
```

The interplay: set `GOGC` higher (e.g., 200) to reduce GC CPU cost, and set `GOMEMLIMIT` to protect against OOM. The GC will stay in the "lazy" GOGC mode until it approaches the limit, then switch to aggressive collection.

```go
// Set programmatically (useful in tests or when value is dynamic)
import "runtime/debug"

debug.SetGCPercent(200)      // equivalent to GOGC=200
debug.SetMemoryLimit(1 << 29) // equivalent to GOMEMLIMIT=512MiB
```

---

### Profile-Guided Optimization (PGO)

PGO uses a CPU profile from a real production workload to guide the compiler's optimization decisions — primarily inlining and devirtualization. The compiler can see which functions are actually hot at runtime and inline more aggressively at those sites.

**How to use PGO (Go 1.21+):**

```bash
# Step 1: Collect a representative CPU profile from production
# (or from a realistic benchmark)
go test -bench=. -cpuprofile=default.pgo ./...

# Step 2: Place the profile at the module root as default.pgo
# (the compiler picks it up automatically)

# Step 3: Build — PGO is applied automatically
go build ./...
# Typical improvement: 2–15% CPU speedup, sometimes more
```

PGO is cumulative: a profile from yesterday's build can guide today's build. The profile does not need to match the current code exactly; the compiler matches by function name and handles mismatches gracefully.

> [!NOTE]
> PGO benefits are workload-dependent. Services with many hot interface method calls (e.g., gRPC handlers, HTTP middleware chains) often see larger improvements because PGO enables devirtualization at those sites.

---

### How the Concepts Fit Together

```
OBSERVE: program is slow or uses too much memory
        │
        ▼
MEASURE: write a benchmark or attach pprof
  ├── go test -bench -benchmem  (microbenchmark)
  └── net/http/pprof             (live service)
        │
        ▼
ANALYZE: read the profile
  ├── go tool pprof (top, list, web)
  ├── go tool trace (scheduling, GC events)
  └── go build -gcflags=-m (escape analysis)
        │
        ▼
IDENTIFY the dominant cost:
  ├── CPU-bound → check inlining, algorithm complexity, PGO
  ├── Allocation-heavy → reduce escapes, preallocate, sync.Pool
  └── GC-bound → GOGC tuning, GOMEMLIMIT, fewer allocations
        │
        ▼
OPTIMIZE one thing at a time
        │
        ▼
VERIFY: re-run benchmark, compare with benchstat
        │
        ▼
REPEAT if needed (Amdahl's Law — diminishing returns)
```

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Benchmarking with dead-code elimination**
>
> The compiler can prove that a function's return value is unused and optimize the call away entirely, producing a benchmark that measures nothing.
>
> **Wrong (result discarded — compiler may eliminate the call):**
> ```go
> func BenchmarkBad(b *testing.B) {
>     for range b.N {
>         processData(largeInput) // return value discarded → may be compiled away
>     }
> }
> ```
>
> **Right (assign to a package-level sink variable):**
> ```go
> var sink any // package-level variable: escapes compiler's DCE analysis
>
> func BenchmarkGood(b *testing.B) {
>     var result []byte
>     for range b.N {
>         result = processData(largeInput)
>     }
>     sink = result // prevent dead-code elimination
> }
> ```
>
> **Why this matters:** A benchmark reporting 0.1 ns/op when the real operation takes 300 ns/op leads to the exact opposite of good engineering — you "optimize" something that was already eliminated.

> [!WARNING]
> **Mistake 2: Forgetting `b.ResetTimer` after expensive setup**
>
> Setup time (loading test fixtures, building large data structures) inflates benchmark results if not excluded.
>
> **Wrong (setup is included in measurement):**
> ```go
> func BenchmarkBad(b *testing.B) {
>     data := loadLargeFixture() // takes 200ms — dominates the benchmark!
>     for range b.N {
>         process(data)
>     }
> }
> ```
>
> **Right:**
> ```go
> func BenchmarkGood(b *testing.B) {
>     data := loadLargeFixture() // setup
>     b.ResetTimer()             // start measuring HERE
>     for range b.N {
>         process(data)
>     }
> }
> ```
>
> **Why this matters:** Without `b.ResetTimer`, the first `b.N=1` iteration includes setup, and the framework calibrates `b.N` based on a misleadingly slow single iteration, skewing all subsequent results.

> [!WARNING]
> **Mistake 3: Optimizing without profiling first**
>
> Developers often rewrite the wrong function — the one they think is slow rather than the one the profiler identifies.
>
> **Wrong workflow:** "This function feels slow, let me optimize it."
> **Right workflow:** "Let me run `go tool pprof` and read the `top` output, then optimize the actual hotspot."
>
> **Why this matters:** On real codebases, the intuitive bottleneck is wrong more than 50% of the time. Profile-driven optimization is not optional hygiene — it is the difference between shipping improvements and shipping changes that don't matter.

**Other pitfalls:**

- **Comparing benchmark results by eye** — use `benchstat`; raw ns/op numbers have 5–15% variance between runs due to CPU frequency scaling, OS scheduling, and cache state
- **Using `b.N` as loop count logic** — `b.N` is set by the framework; do not use it for anything other than the loop counter
- **Enabling the race detector during benchmarks** — `go test -race -bench=.` measures the race detector overhead, not your code; run race detection separately

---

## Mental Models

### Mental Model 1: The Profile as a Map

Think of a CPU profile as a heat map of your code: some functions are bright red (consuming lots of CPU), most are cool blue (barely visible). Your job is to find the red zones and make them cooler — not to repaint the blue zones, which would have no visible effect on the overall temperature.

The `top` command shows you the hottest spots. The `list` command zooms in to the exact line. `web` gives you the full geography. You would not try to cool a room by rearranging furniture in a room that is already cold.

### Mental Model 2: Allocations as Garbage for the Collector

Every heap allocation creates a future job for the GC. Think of allocations as trash: you can throw out one wrapper at a time (many small allocations), or batch your trash (preallocate and reuse). The GC truck (GC cycle) has to pick up all the trash regardless; fewer pieces means less time collecting.

`sync.Pool` is the recycle bin: instead of throwing out a buffer, you put it in the bin so the next request can reuse it without a new allocation.

### Mental Model 3: Escape Analysis as the Compiler's Decision-Making

Think of the compiler as a careful planner who wants to put everything on the stack (free at return, no GC needed). It will move a variable to the heap only if it has no choice — because the variable's lifetime extends beyond the current function frame, or because it is stored in an interface (runtime type is unknown, so size is unknown at compile time).

When you see "escapes to heap" in `-gcflags=-m` output, the compiler is saying: "I was forced to put this on the heap because I couldn't guarantee it would be gone when the function returned." Fix the cause, not the symptom.

> [!NOTE]
> Use Model 1 (heat map) when deciding *where* to focus. Use Model 2 (garbage/recycling) when deciding *what* optimization to apply. Use Model 3 (compiler planner) when reading escape-analysis output to understand *why* something allocates.

---

## Practical Examples

### Example 1: Finding a Hot Allocation with pprof _(Basic)_

**Scenario:** A service that processes JSON requests is consuming more memory than expected and GC is running frequently.

**Goal:** Identify the allocation hot spot using a heap profile.

```go
// handler.go — simplified handler for illustration
package main

import (
    "encoding/json"
    "net/http"
    _ "net/http/pprof" // registers /debug/pprof handlers
)

type Request struct {
    Messages []string `json:"messages"`
}

func handleProcess(w http.ResponseWriter, r *http.Request) {
    var req Request
    json.NewDecoder(r.Body).Decode(&req)

    // processMessages allocates a new string per message — allocation site
    results := make([]string, 0, len(req.Messages))
    for _, msg := range req.Messages {
        results = append(results, "[processed] "+msg) // + allocates
    }

    json.NewEncoder(w).Encode(results)
}

func main() {
    http.HandleFunc("/process", handleProcess)
    http.ListenAndServe(":8080", nil)
}
```

```bash
# While the server is running and handling traffic:
go tool pprof http://localhost:8080/debug/pprof/heap
```

```
(pprof) top5
Showing nodes accounting for 14.50MB, 89.23% of 16.25MB total
      flat  flat%   sum%        cum   cum%
   8.25MB 50.77% 50.77%    8.25MB 50.77%  main.handleProcess
   3.50MB 21.54% 72.31%    3.50MB 21.54%  encoding/json.(*decodeState).object
   2.75MB 16.92% 89.23%    2.75MB 16.92%  strings.(*Builder).copyCheck
```

**What to notice:** `handleProcess` dominates heap allocations. The `"[processed] "+msg` string concatenation inside the loop is the culprit — each `+` creates a new heap string. Fix: use `strings.Builder` or `fmt.Sprintf` once, or better, build the result into a pre-allocated buffer.

---

### Example 2: Escape Analysis in Practice _(Intermediate)_

**Scenario:** A function is allocating on the heap unexpectedly, adding GC pressure.

**Goal:** Use `-gcflags=-m` to find why, then fix it.

```go
// before.go — each call allocates a Config on the heap
package main

type Config struct {
    Host    string
    Port    int
    Timeout int
}

// Returns a pointer — Config ESCAPES to heap
func defaultConfig() *Config {
    return &Config{Host: "localhost", Port: 8080, Timeout: 30}
}

func connect(cfg *Config) {
    // ... use cfg ...
}

func main() {
    for range 1000 {
        cfg := defaultConfig() // 1000 heap allocations
        connect(cfg)
    }
}
```

```bash
$ go build -gcflags='-m' before.go
./before.go:12:9: &Config{...} escapes to heap
```

```go
// after.go — Config stays on stack; zero heap allocations
func defaultConfig() Config {  // return value (not pointer)
    return Config{Host: "localhost", Port: 8080, Timeout: 30}
}

func connect(cfg *Config) { /* unchanged */ }

func main() {
    for range 1000 {
        cfg := defaultConfig() // stack allocated
        connect(&cfg)          // pass pointer to stack variable — safe, cfg lives until end of iteration
    }
}
```

```bash
$ go build -gcflags='-m' after.go
# (no "escapes to heap" for Config)
```

**What to notice:** Returning a pointer forces the compiler to heap-allocate. Returning a value and passing its address (within the same function) keeps it on the stack. This is the most impactful single change for allocation-heavy code: audit function signatures that return pointers to small structs.

---

### Example 3: strings.Builder and Preallocation _(Applied)_

**Scenario:** A report generator concatenates many strings and is profiled as spending 30% of CPU in `runtime.mallocgc` during string builds.

**Goal:** Eliminate repeated string allocations using `strings.Builder` with preallocation.

```go
package main

import (
    "fmt"
    "strings"
    "testing"
)

// Naive: O(n²) allocations
func buildReportNaive(lines []string) string {
    result := ""
    for _, line := range lines {
        result += line + "\n" // new allocation each iteration
    }
    return result
}

// Better: strings.Builder, O(n) amortized
func buildReportBuilder(lines []string) string {
    var sb strings.Builder
    for _, line := range lines {
        sb.WriteString(line)
        sb.WriteByte('\n')
    }
    return sb.String()
}

// Best: pre-grow the builder (single allocation)
func buildReportPrealloc(lines []string) string {
    totalLen := 0
    for _, line := range lines {
        totalLen += len(line) + 1 // +1 for newline
    }
    var sb strings.Builder
    sb.Grow(totalLen) // allocate the final buffer upfront
    for _, line := range lines {
        sb.WriteString(line)
        sb.WriteByte('\n')
    }
    return sb.String()
}

var result string

func BenchmarkNaive(b *testing.B) {
    lines := make([]string, 100)
    for i := range lines {
        lines[i] = fmt.Sprintf("log line number %d with some content", i)
    }
    b.ResetTimer()
    for range b.N {
        result = buildReportNaive(lines)
    }
}

func BenchmarkBuilder(b *testing.B) {
    lines := make([]string, 100)
    for i := range lines {
        lines[i] = fmt.Sprintf("log line number %d with some content", i)
    }
    b.ResetTimer()
    for range b.N {
        result = buildReportBuilder(lines)
    }
}

func BenchmarkPrealloc(b *testing.B) {
    lines := make([]string, 100)
    for i := range lines {
        lines[i] = fmt.Sprintf("log line number %d with some content", i)
    }
    b.ResetTimer()
    for range b.N {
        result = buildReportPrealloc(lines)
    }
}
```

Expected benchmark output:

```
BenchmarkNaive-8       125082   9412 ns/op   29920 B/op   99 allocs/op
BenchmarkBuilder-8     512031   2341 ns/op    6144 B/op    3 allocs/op
BenchmarkPrealloc-8    891204   1342 ns/op    4096 B/op    1 allocs/op
```

**What to notice:** The naive approach (string `+=`) makes 99 allocations. `strings.Builder` brings it to 3. Pre-growing drops it to 1. The allocation count directly corresponds to the time improvement: 7× speedup from Naive to Prealloc, driven entirely by fewer heap allocations, not algorithmic complexity.

---

### Example 4: A Broken Benchmark _(Edge Case)_

**Scenario:** A developer benchmarks a pure computation and reports impossibly fast numbers: 0.3 ns/op for an operation that should take ~50 ns.

```go
// broken_bench_test.go
package main

import "testing"

func isPrime(n int) bool {
    if n < 2 {
        return false
    }
    for i := 2; i*i <= n; i++ {
        if n%i == 0 {
            return false
        }
    }
    return true
}

// BUG: result discarded — compiler eliminates isPrime call entirely
func BenchmarkIsPrimeBroken(b *testing.B) {
    for range b.N {
        isPrime(982451653) // return value not used; call may be optimized away
    }
}
```

Output: `BenchmarkIsPrimeBroken-8   1000000000   0.29 ns/op` — suspiciously fast.

**Why this is important:** The compiler sees that the result of `isPrime` is never used and the function has no side effects, so it eliminates the call entirely. The benchmark measures loop overhead (0.29 ns) rather than the actual computation (~50 ns). This leads to wildly incorrect "before" baselines that make optimizations appear to have negative effect when measured correctly. Always assign the result to a package-level sink.

---

## Related Concepts

Within this topic:

- [[go/11. Testing and Benchmarking]] — benchmarking is the foundation of profiling; the `-bench`, `-benchmem`, `-cpuprofile`, and `-memprofile` flags from that module are used directly throughout this one
- [[go/17. Runtime Internals and the Memory Model]] — the GC mechanics, the goroutine scheduler, and the memory model explain *why* the optimizations in this module work; GOGC and GOMEMLIMIT make more sense after understanding the tricolor GC
- [[go/4. Composite Types]] — slices and maps are the most common allocation sites; preallocating with `make([]T, 0, n)` and understanding append's growth strategy is prerequisite knowledge

Across topics:

- [[memory-management]] — Go's GC is a tricolor mark-and-sweep; understanding heap vs. stack allocation, GC pressure, and why allocations are not free is the cross-language foundation for everything in this module
- [[concurrency]] — `sync.Pool` is a concurrency primitive; block and mutex profiles only make sense if you understand goroutine scheduling and lock contention

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Spot the Broken Benchmark** _(Easy)_
>
> Given a benchmark function reporting 0.2 ns/op for a function that visibly does string processing, identify the two bugs (dead-code elimination and missing ResetTimer) and fix them.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-spot-the-broken-benchmark--easy--1-pt)

The exercises progress from identifying benchmark bugs to profiling a real function with pprof, reducing allocations using escape-analysis output, and implementing a `strings.Builder` preallocation optimization. Complete at least the Easy and Medium exercises before taking the test.

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
Profile-Driven HTTP Service Optimization — take an existing HTTP handler (or write a simple one), load-test it with a tool like `wrk` or `hey`, attach `net/http/pprof`, identify the top allocation site from the heap profile, apply one or more concrete optimizations from this module, and demonstrate the improvement with `benchstat`. Document what you found, what you changed, and the measured before/after numbers.

---

## Further Reading

These are verified resources specifically relevant to this module:

1. **[Profiling Go Programs — The Go Blog](https://go.dev/blog/profiling-go-programs)** — The canonical introduction by Russ Cox; walks through a real profiling session on a Go program, showing exactly how to use `pprof` to find and fix a hotspot. Start here.
2. **[pkg.go.dev/runtime/pprof](https://pkg.go.dev/runtime/pprof)** — Official API reference for `runtime/pprof`; covers `StartCPUProfile`, `WriteHeapProfile`, and the named profile types (goroutine, block, mutex, threadcreate).
3. **[pkg.go.dev/net/http/pprof](https://pkg.go.dev/net/http/pprof)** — Official docs for the HTTP profiling endpoint; explains each `/debug/pprof/` route and the query parameters.
4. **[Profile-Guided Optimization — go.dev/doc/pgo](https://go.dev/doc/pgo)** — The official PGO guide; explains how to collect a profile, how to enable PGO, and what to expect from it.
5. **[pkg.go.dev/golang.org/x/perf/cmd/benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat)** — Reference for `benchstat`; explains the statistical model, input format, and how to interpret the p-values and delta percentages.

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 16

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
