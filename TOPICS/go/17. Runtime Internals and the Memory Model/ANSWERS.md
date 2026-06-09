# Answer Key — Module 17: Runtime Internals and the Memory Model

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with all notes closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding *why* before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately (e.g., "G," "P," "write barrier" — not vague paraphrases)
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — G, M, P definitions [1 pt]

**Full credit answer:**
- **G (goroutine):** A lightweight unit of execution — a function plus its call stack (~2 KB initial) and register state; managed entirely by the Go runtime.
- **M (machine):** A 1:1 mapping to an OS thread; M's execute Go code and can be created freely when goroutines block in syscalls.
- **P (processor):** A scheduling context that an M must hold to run Go code; owns a local run queue; there are exactly `GOMAXPROCS` P's.

**Key points required:** All three defined correctly. P described as a "scheduling context" or "license to run Go code," not merely as "a processor."

**Common wrong answers:**
- Saying M is "a CPU" — M is an OS thread, not a physical CPU
- Saying P controls threads — P controls *Go code execution*, M's are the threads

---

### 1.2 — Goroutine stack size and growth [1 pt]

**Full credit answer:**
Goroutines start with approximately **2 KB** of stack (exact value is implementation-defined; has been 2–8 KB across Go versions). When the stack is nearly full, the runtime allocates a **new, larger contiguous stack** (typically 2× the current size), **copies all existing stack frames** to the new allocation, **updates all pointers** within those frames to reflect the new addresses, and frees the old stack. This is called a **contiguous (or copying) stack** — introduced in Go 1.3 to replace the older split-stack design.

**Key points required:** Small initial size (~2 KB); copying mechanism named ("copying stacks" or "contiguous stacks"); mention of pointer update or relocation.

**Common wrong answers:**
- Saying "split stacks" — Go replaced split stacks with copying stacks in Go 1.3; split stacks are no longer used
- Saying the stack "grows in place" — no, a new allocation is made and the old one is freed

---

### 1.3 — Tri-color GC [1 pt]

**Full credit answer:**
- **White:** Objects not yet visited by the GC; potentially garbage. At the end of the mark phase, any object still white is unreachable and will be swept (freed).
- **Gray:** Objects discovered as reachable (pointed to by roots or black objects) but whose children have not yet been scanned. The GC still has work to do on these objects.
- **Black:** Objects that have been fully scanned — all of their outgoing pointers have been processed and their children shaded gray. Black objects will not be freed.

**Key points required:** White = not visited/garbage candidate; gray = discovered but not fully scanned; black = fully scanned/safe.

---

### 1.4 — GOMEMLIMIT vs GOGC [1 pt]

**Full credit answer:**
`GOGC` sets the **target heap growth ratio** — for example, `GOGC=100` (the default) means the GC triggers when the live heap doubles. It is a **relative** control; the actual memory consumed depends on the live heap size.

`GOMEMLIMIT` (Go 1.19+) sets a **hard upper bound on the process's total memory usage**. When the process approaches this limit, the GC becomes more aggressive regardless of `GOGC`. It is an **absolute** control in bytes.

**Key difference:** `GOGC` controls GC *frequency relative to live heap size*; `GOMEMLIMIT` is a *hard ceiling* on total memory.

---

### 1.5 — Asynchronous preemption [1 pt]

**Full credit answer:**
Before Go 1.14, Go's scheduler was **cooperative** at safe points — goroutines could only be preempted at function calls (where the compiler inserted preemption checks). A goroutine executing a tight loop with no function calls could monopolize a P indefinitely, starving other goroutines.

**Asynchronous preemption** (Go 1.14) solves this by delivering a signal (**SIGURG** on Unix) to threads running goroutines that need to yield. The signal handler injects a call to `runtime.asyncPreempt`, which yields the goroutine back to the scheduler. This means any goroutine can be preempted at any point, even inside a tight loop.

**Key points required:** Prior problem (tight loop could monopolize P); mechanism (signal-based injection); SIGURG is a bonus.

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Write barriers and the tri-color invariant [2 pts]

**Full credit answer:**
The concurrent GC mark phase runs at the same time as the mutator (the application). This creates a problem: during concurrent marking, the mutator might create a new pointer from a **black** object (already fully scanned) to a **white** object (not yet discovered). Because the GC won't re-scan black objects, this white object would never be grayed and would be incorrectly collected — a use-after-free bug.

Write barriers maintain the **tri-color invariant**: a black object must never point directly to a white object. When the mutator writes a pointer (including stack-to-heap and heap-to-heap), the write barrier shades the target gray if necessary. This ensures the GC will discover and scan it before the sweep phase.

Without write barriers: the GC could free memory that is still reachable, causing arbitrary memory corruption.

**Rubric:**
- 2 pts: Correctly describes the invariant (no black→white), the problem (GC misses newly-reachable objects), and the write barrier's role (shades target gray)
- 1 pt: Correct intuition but imprecise — e.g., "write barrier prevents GC from collecting live objects" without explaining the black→white mechanism
- 0 pts: Says "write barrier is for performance" or misidentifies its purpose

---

### 2.2 — time.Sleep is not synchronization [2 pts]

**Full credit answer:**
This is **not correct** — `time.Sleep` establishes **no happens-before relationship** in the Go Memory Model. The model only defines happens-before through specific synchronization operations: channel sends/receives, mutex lock/unlock, `sync.WaitGroup` Done/Wait, atomic operations, and package `init`. Time-based ordering is entirely absent from the model.

Even if in practice the goroutine always finishes within 100 ms, this is not a guarantee the compiler or runtime is required to honor. The compiler is permitted to reorder writes, and the hardware can delay visibility of writes across cores. The race detector will flag this as a data race. To be correct, the program must use a channel receive or `wg.Wait()` to synchronize.

**Rubric:**
- 2 pts: Clearly states `time.Sleep` does NOT establish happens-before, cites the memory model, and names a correct alternative
- 1 pt: Says it's incorrect but doesn't explain the memory model basis, or says "it's a race" without explaining why time doesn't help
- 0 pts: Agrees that sleep is sufficient for synchronization

---

### 2.3 — cgo call costs [2 pts]

**Full credit answer:**
At minimum, three distinct costs:

1. **Call overhead (~170 ns):** Each cgo call must save the Go register state, switch from the goroutine's (small, growing) stack to a C-compatible system stack (fixed, larger), call the C function, then restore Go state on return. A pure Go function call costs ~1–5 ns; the cgo boundary adds ~40× overhead.

2. **Scheduler interaction (P handoff):** When a goroutine makes a cgo call, the Go runtime treats it like a blocking syscall — it immediately hands the P to another M (or parks the current M). This means every cgo call may cause a P to be transferred, increasing scheduler pressure. Long-running C code will starve other goroutines of that P.

3. **Build complexity / loss of cross-compilation:** cgo requires a C compiler on every build machine. `CGO_ENABLED=0` — which enables pure-Go cross-compilation — cannot be used when cgo is present. CI pipelines become more complex.

Additional valid costs: the race detector does not instrument C code; C code does not obey Go's memory model.

**Rubric:**
- 2 pts: Names at least 3 distinct costs, correctly describes the scheduler handoff mechanism
- 1 pt: Names 1–2 costs, or names 3 but describes them vaguely
- 0 pts: Only says "it's slower" without any specific cost

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Racy compute + main [3 pts]

**Full credit answer:**
Yes, this program has a **data race** on `result`. There are two accesses:
1. The goroutine writes `result = heavyComputation()` (in `compute`)
2. `main` reads `result` in `fmt.Println(result)`

There is **no happens-before** relationship between these two events. The `go compute()` statement does not synchronize — it fires the goroutine without any guarantee that `compute` has started, let alone finished, before `main` continues. The main goroutine proceeds immediately to `fmt.Println(result)`, which may execute before, during, or after `compute` writes to `result`. This is undefined behavior.

**Minimal fix — channel:**
```go
var result int

func compute(ch chan<- int) {
    ch <- heavyComputation() // channel send establishes happens-before receive
}

func main() {
    ch := make(chan int)
    go compute(ch)
    result := <-ch // channel receive: compute's write HB this read
    fmt.Println(result)
}
```

**Or with WaitGroup:**
```go
var result int
var wg sync.WaitGroup
wg.Add(1)
go func() {
    result = heavyComputation()
    wg.Done() // Done HB Wait's return
}()
wg.Wait()
fmt.Println(result) // safe
```

**Memory-model rule:** Channel send is synchronized before the corresponding receive completes (for any channel). `wg.Done` is synchronized before `wg.Wait` returns.

**Rubric:**
- 3 pts: Correctly identifies the race, names both accesses, explains the absence of happens-before, provides a correct fix citing the specific rule
- 2 pts: Identifies the race and provides a correct fix, but explanation of why is incomplete
- 1 pt: Identifies a race exists but does not explain the memory-model basis or fix
- 0 pts: Claims the program is correct ("the goroutine will probably finish first")

---

### 3.2 — GC tuning for 256 MiB container [3 pts]

**Full credit answer:**
```go
import "runtime/debug"

func init() {
    // Allow the heap to grow to ~3× live before GC (live heap ~60 MiB → GC at ~180 MiB)
    // Reduces GC frequency, reducing pause frequency
    debug.SetGCPercent(200)

    // Hard ceiling at 230 MiB (~90% of 256 MiB container limit)
    // GC becomes aggressive when approaching this limit, preventing OOM
    debug.SetMemoryLimit(230 << 20) // 230 MiB
}
```

**Explanation:**
- `GOGC=200` means the GC triggers when live heap grows to 3× its size after the last collection (~180 MiB from ~60 MiB live). This reduces GC frequency — fewer cycles means fewer latency spikes.
- `GOMEMLIMIT=230 MiB` ensures the process never exceeds ~90% of the container memory limit. If the live heap grows unexpectedly, the GC becomes more aggressive before the container is OOM-killed. The 10% buffer accommodates Go runtime overhead, goroutine stacks, and other non-heap allocations.
- Setting `GOGC=off` without `GOMEMLIMIT` would be dangerous — the heap could grow without bound. The combination of high GOGC + GOMEMLIMIT is the recommended pattern.

**Rubric:**
- 3 pts: Correct `GOGC` value (any higher-than-default value with correct reasoning), correct `GOMEMLIMIT` value (~90% of limit), explains both choices and their interaction
- 2 pts: Sets one correctly with explanation, other is missing or incorrect
- 1 pt: Sets values without understanding the reasoning, or gets one direction right and one backwards (e.g., suggests lowering GOGC to reduce pauses — incorrect)
- 0 pts: Sets GOGC=off without GOMEMLIMIT, or disables GC without acknowledging the memory growth risk

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Racy counter [3 pts] (1 pt each part)

**(a) Data race on `counter++`:**
Yes, `counter++` is a data race. `counter++` is not atomic — it compiles to three operations: read `counter`, add 1, write `counter` back. When 1000 goroutines execute this concurrently with no synchronization, multiple goroutines may read the same value, increment it, and write back — causing increments to be lost. Per the Go Memory Model, this is a **data race**: two goroutines access the same memory location concurrently, at least one write is involved, and there is no happens-before ordering. The race detector (`go run -race`) will report it.

**(b) "Trusting the scheduler" is also wrong:**
Even if `counter++` were somehow atomic, `fmt.Println(counter)` in `main` has **no happens-before relationship** with any of the goroutine launches. The `go` statement does not synchronize. `main` might read `counter` before any goroutines have run, or partway through. Without a `WaitGroup.Wait()` or channel receive in `main`, there is no synchronization guarantee. The final `fmt.Println` could print any value from 0 to 1000.

**(c) Corrected version:**
```go
package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)

var counter atomic.Int64 // zero value is ready to use (Go 1.19+)

func increment(wg *sync.WaitGroup) {
    defer wg.Done()
    counter.Add(1) // atomic add — sequentially consistent; no data race
}

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go increment(&wg)
    }
    wg.Wait() // Done() HB Wait() return → all increments visible
    fmt.Println(counter.Load()) // safe: prints 1000
}
```

`atomic.Int64.Add` is sequentially consistent and eliminates the read-modify-write race. `wg.Wait()` establishes happens-before between all goroutine completions and the read in `main`.

**Rubric:**
- 1 pt for (a): Correctly identifies data race on `counter++`; explains the non-atomic read-modify-write
- 1 pt for (b): Correctly explains that the `go` statement provides no synchronization and main may read before goroutines complete
- 1 pt for (c): Provides a correct fix using `atomic.Int64` (or `atomic.AddInt64`) AND a `WaitGroup` — both needed; fixing only one earns 0.5 pts

---

## Section 5: Discussion — Answer Key

### 5.1 — Non-generational, non-compacting GC tradeoffs [2 pts]

**Example strong answer:**
Go's GC is **non-generational**, meaning there is no young/old heap split — every GC cycle scans the entire live heap. Generational GCs (JVM, Python's cyclic collector) exploit the observation that most objects die young ("infant mortality"), collecting the young generation cheaply and frequently. Go's choice means the GC is simpler and has more predictable pause characteristics, but pays a higher per-cycle CPU cost for workloads with large long-lived heaps because those objects are rescanned every cycle.

Go's GC is also **non-compacting**, meaning objects are never moved during collection. This keeps pointer semantics simple — a pointer to a heap object remains valid forever — and allows the use of `unsafe.Pointer` patterns that depend on stable addresses. Compacting GCs (JVM HotSpot G1/ZGC) move objects to defragment the heap and improve cache locality for allocation. Go's choice means the heap can fragment over time, and allocation of large objects may require finding large contiguous free regions.

**Where Go's GC is a disadvantage:** Long-running services with multi-GB heaps of stable long-lived data (e.g., large in-memory databases or caches). The non-generational design rescans all of that data every GC cycle, wasting CPU. A generational GC would mostly collect the small young-generation area, ignoring the stable old data.

**Elements that earn full credit:**
- Correctly explains non-generational: no young/old split; whole heap scanned each cycle
- Names the generational optimization (infant mortality hypothesis) and why Go doesn't exploit it
- Correctly explains non-compacting: objects don't move; simpler pointers but potential fragmentation
- Identifies a workload where Go's design is weaker (large stable long-lived heap)
- Identifies what Go gains (simpler GC, predictable pauses, stable pointers)

**Rubric:**
- 2 pts: Correctly explains both terms AND identifies at least one tradeoff for each AND names a workload where the design is a disadvantage
- 1 pt: Explains the terms but analysis of tradeoffs is superficial or one-sided
- 0 pts: Misdefines generational or compacting GC, or claims Go's design is superior in all cases

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Deprecated reflect.StringHeader pattern [+5 pts]

**(a) Does it work? What is the danger?**
The code works correctly on current Go versions in the sense that it produces a valid `[]byte` slice that points to the string's backing memory without allocation. The danger is if the returned `[]byte` is modified: strings in Go are immutable by contract. The backing array of a string literal may be stored in a **read-only data segment** of the binary — writing to it causes a segmentation fault (panic: "unexpected fault address"). Even for strings not in read-only memory, modifying the slice breaks Go's immutability contract for strings and may corrupt the string's value wherever else it is referenced.

**(b) Why `reflect.StringHeader` and `reflect.SliceHeader` are deprecated:**
These types expose the internal memory layout of strings and slices as structs with `Data uintptr` and `Len int` fields. Storing an address as a `uintptr` (rather than `unsafe.Pointer`) violates the `unsafe.Pointer` Rule 4: the GC may move the backing data (e.g., via a stack copy for strings derived from stack variables), invalidating the stored `uintptr` before it is used. Additionally, these types expose internal runtime representation details that the Go team may want to change.

The Go 1.20+ alternatives — `unsafe.StringData`, `unsafe.SliceData`, `unsafe.String`, `unsafe.Slice` — operate on `unsafe.Pointer` directly (never storing `uintptr`), and the compiler understands them well enough to keep the GC pinning correct.

**(c) Corrected version:**
```go
import "unsafe"

// Go 1.20+: unsafe.StringData returns a pointer to the string's backing array.
// unsafe.Slice constructs a []byte from that pointer with the given length.
func stringToBytes(s string) []byte {
    if len(s) == 0 {
        return nil
    }
    // unsafe.StringData returns *byte pointing to s's backing array
    // unsafe.Slice(p, n) creates []byte{ptr: p, len: n, cap: n}
    // MUST NOT modify the returned slice.
    return unsafe.Slice(unsafe.StringData(s), len(s))
}
```

**Rubric:**
- 5 pts: Correctly explains danger of modification, correctly explains why `uintptr` in StringHeader is dangerous (GC movement / stack copy), and provides a correct Go 1.20+ version
- 3 pts: Correctly identifies danger of modification and provides a correct fix, but explanation of why StringHeader is deprecated is incomplete
- 1 pt: Identifies the immutability concern but misses the `uintptr` GC hazard, or provides an incomplete fix

---

## Common Wrong Answers Across the Test

1. **Confusing P count with M count** — Students say "GOMAXPROCS controls the number of OS threads." It controls P's. M's can exceed GOMAXPROCS when blocked in syscalls or cgo.
2. **Claiming time.Sleep synchronizes** — This is incorrect and a common pitfall. The memory model is explicit: only specific synchronization operations establish happens-before.
3. **Saying "non-generational means faster"** — Non-generational means simpler and more predictable, but it scans more per cycle than a generational GC would for the same live heap. It is a tradeoff, not a strict improvement.
4. **Mixing up GOGC direction** — Higher GOGC means *less frequent* GC (not more). GOGC=100 means GC when heap doubles; GOGC=200 means GC when heap triples. Students sometimes invert this.
5. **Saying `unsafe.Pointer` is always dangerous** — It is dangerous if the rules are violated. Code that follows all six rules is safe and is used in the standard library. The point is that you must know and follow the rules.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 likely read the README but did not work through the reasoning carefully. The write-barrier and memory-model questions require understanding *mechanism*, not just facts. Recommend re-studying with the Feynman technique.
- Students who struggle with Section 3 (especially 3.1) likely still have an intuition that "goroutines are threads" and that some implicit synchronization exists. Emphasize: the `go` statement is fire-and-forget with zero synchronization.
- A score below 60% on this module suggests the prerequisites (module 9 and 12) may not be solid. Ask the student to re-verify their comfort with sync.WaitGroup, channels as synchronization, and the race detector before retrying.
- The bonus question (6.1) is primarily for students who have used unsafe.Pointer in practice or who want to understand Go's internal package implementations. Do not expect all students to score full marks here.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
