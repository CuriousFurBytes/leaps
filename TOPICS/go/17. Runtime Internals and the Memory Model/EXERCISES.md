# Exercises — Module 17: Runtime Internals and the Memory Model

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

## Exercise 1: G-M-P Vocabulary [🟢 Easy] [1 pt]

### Context
The G-M-P model is the foundation of the Go scheduler. Before reasoning about scheduler behavior, you need to be precise about what each entity is and what constraints govern them.

### Task
Without running any code, write a short explanation (4–6 sentences) answering all of the following:
1. What is a **G** (goroutine), and what state does it carry?
2. What is an **M** (machine), and what is its relationship to OS threads?
3. What is a **P** (processor), and why is the number of P's (not M's) the key limit on Go-code parallelism?
4. What does `GOMAXPROCS` control, and what is its default value?

### Requirements
- [ ] Correctly describes G, M, and P as distinct entities
- [ ] Explains why P is the bottleneck for CPU-bound parallelism (not M)
- [ ] States the default value of `GOMAXPROCS`
- [ ] No code required — this is a written explanation

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Focus on the constraint: to run Go code, an M needs a P. There are exactly `GOMAXPROCS` P's. M's can exceed `GOMAXPROCS` — they are created when blocked in syscalls or cgo — but without a P they cannot execute Go code. The P is the "license to run."

</details>

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

**G (goroutine):** A G is a lightweight unit of execution: essentially a Go function plus its call stack (starting ~2 KB) and register state. Goroutines are managed by the Go runtime, not the OS. Millions can exist simultaneously.

**M (machine):** An M is a 1:1 mapping to an OS thread. M's are created by the runtime as needed — for example, when a goroutine makes a blocking syscall, a new or idle M may be created/activated to hold the P that the blocked M released.

**P (processor):** A P is a scheduling context that an M must hold to execute Go code. A P owns a local run queue (up to 256 runnable G's). There are exactly `GOMAXPROCS` P's at any time. Even if there are thousands of M's, only `GOMAXPROCS` can be running Go code simultaneously — the rest are either blocked in syscalls/cgo or idle.

**`GOMAXPROCS`:** Controls the number of P's. Defaults to `runtime.NumCPU()` (the number of logical CPU cores) since Go 1.5. Setting it to 1 forces sequential execution of Go code regardless of how many goroutines exist.

</details>

---

## Exercise 2: GOMAXPROCS and Scheduler Observation [🟡 Medium] [2 pts]

### Context
Understanding GOMAXPROCS requires observation, not just memorization. This exercise measures the effect of GOMAXPROCS on CPU-bound parallel work and requires you to reason about why the speedup behaves the way it does.

### Task
Write a Go program that:
1. Defines a CPU-bound function `work(n int)` that iterates a loop `n` times doing arithmetic (no I/O, no channel ops)
2. Runs the function in parallel across 8 goroutines, measuring total wall-clock time, first with `GOMAXPROCS=1`, then with `GOMAXPROCS=runtime.NumCPU()`
3. Prints both durations and the speedup ratio

Then, in a comment above `main`, answer: "What speedup would you expect, and why does it not perfectly equal `NumCPU()`?"

### Requirements
- [ ] Uses `sync.WaitGroup` to wait for all 8 goroutines
- [ ] Calls `runtime.GOMAXPROCS(1)` before the first measurement and `runtime.GOMAXPROCS(runtime.NumCPU())` before the second
- [ ] Prints both durations and a speedup ratio
- [ ] Includes a comment explaining the expected speedup and its limitations

### Hints
<details>
<summary>Hint 1</summary>

Use `time.Now()` before launching goroutines and `time.Since(start)` after `wg.Wait()`. The `work` function just needs a loop: `for i := 0; i < n; i++ { _ = i * i }` is sufficient to burn CPU time.

</details>

<details>
<summary>Hint 2</summary>

The speedup will be less than `NumCPU()` for several reasons: scheduling overhead, cache coherency traffic between cores, the overhead of launching and syncing goroutines, and the fact that even one goroutine with a full core monopolized reduces the theoretical maximum.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
// Expected speedup: close to NumCPU() for pure CPU-bound work with enough goroutines,
// but not exactly NumCPU() due to:
// 1. Scheduling overhead (P hand-off, context switching between goroutines)
// 2. Cache contention (multiple cores evicting each other's cache lines)
// 3. WaitGroup synchronization overhead
// 4. The OS may not schedule all M's on separate physical cores simultaneously
// On machines with hyperthreading, speedup may plateau below NumCPU() because
// hyperthreads share the same physical core's execution units.
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

func work(n int) {
    // Pure CPU work: no I/O, no channel ops, no allocations
    sum := 0
    for i := 0; i < n; i++ {
        sum += i * i
    }
    _ = sum // prevent compiler from eliminating the loop
}

func measureParallel(procs, goroutines, iterations int) time.Duration {
    runtime.GOMAXPROCS(procs)
    var wg sync.WaitGroup
    start := time.Now()
    for i := 0; i < goroutines; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            work(iterations)
        }()
    }
    wg.Wait()
    return time.Since(start)
}

func main() {
    ncpu := runtime.NumCPU()
    const goroutines = 8
    const iterations = 20_000_000

    d1 := measureParallel(1, goroutines, iterations)
    dN := measureParallel(ncpu, goroutines, iterations)

    speedup := float64(d1) / float64(dN)
    fmt.Printf("GOMAXPROCS=1:       %v\n", d1)
    fmt.Printf("GOMAXPROCS=%d:      %v\n", ncpu, dN)
    fmt.Printf("Speedup:            %.2fx (theoretical max: %dx)\n", speedup, ncpu)
}
```

**Explanation:**
The speedup should be close to `ncpu` on a multicore machine for pure CPU-bound work. It falls short because: goroutine creation and synchronization have overhead; the OS scheduler may not perfectly distribute M's across cores; and memory/cache effects increase with core count. On machines with fewer than 8 physical cores, some goroutines share cores and the speedup is bounded by the physical core count.

</details>

---

## Exercise 3: Happens-Before Reasoning [🔴 Hard] [3 pts]

### Context
The Go Memory Model defines happens-before as the only guarantee of visibility. This exercise requires you to analyze three code snippets and determine for each: is it correctly synchronized, does it contain a data race, and which specific happens-before rule (if any) applies?

### Task
For each of the following three snippets, write a brief analysis (2–4 sentences each):
- Is there a data race? (Yes/No)
- If no: which happens-before relationship makes it safe?
- If yes: what synchronization primitive would fix it?

**Snippet A:**
```go
var x int
ch := make(chan int, 1) // buffered, capacity 1
go func() {
    x = 42
    ch <- 1
}()
<-ch
fmt.Println(x)
```

**Snippet B:**
```go
var x int
var once sync.Once
go func() {
    once.Do(func() { x = 42 })
}()
once.Do(func() {}) // no-op; ensures once has been called
fmt.Println(x)
```

**Snippet C:**
```go
var x int
var wg sync.WaitGroup
wg.Add(1)
go func() {
    x = 42
    wg.Done()
}()
// No wg.Wait() — main just reads x after a time.Sleep(time.Millisecond)
time.Sleep(time.Millisecond)
fmt.Println(x)
```

### Requirements
- [ ] Correctly classifies each snippet as safe or racy
- [ ] For safe snippets: names the specific happens-before rule from the Go Memory Model
- [ ] For racy snippets: proposes the minimal fix
- [ ] Does not rely on "it will probably work" reasoning — only formal happens-before guarantees

### Hints
<details>
<summary>Hint 1 (conceptual)</summary>

A buffered channel send of capacity C: the k-th receive happens before the (k+C)-th send completes. For capacity 1, the 1st receive happens before the 2nd send. More simply: for a buffered channel, a send to a non-full channel does NOT block, so the send completing does not synchronize with the receive. The receive completing synchronizes with the next send when the channel is full.

Wait — re-read the rule carefully. The Go Memory Model also says: "The closing of a channel is synchronized before a receive that returns a zero value because the channel is closed." And for unbuffered channels: "A send on a channel is synchronized before the completion of the corresponding receive from that channel."

</details>

<details>
<summary>Hint 2 (for Snippet B)</summary>

`sync.Once.Do(f)` guarantees: if two goroutines call `Do`, exactly one will call `f`, and the other will wait until `f` returns. After `Do` returns in both goroutines, the second goroutine's `Do` happens-after the first's `f` completes. Is the relationship between the goroutine's `Do` and the main goroutine's no-op `Do` sufficient to guarantee x=42 is visible?

</details>

<details>
<summary>Hint 3 (for Snippet C)</summary>

`time.Sleep` is NOT a synchronization primitive and establishes NO happens-before relationship. The memory model says nothing about time — only about explicit synchronization operations (channels, mutexes, atomics, WaitGroup).

</details>

### Solution
<details>
<summary>Show Solution</summary>

**Snippet A: Safe — no data race.**

The write `x = 42` happens before `ch <- 1` (sequential within the goroutine). The send `ch <- 1` on a buffered-channel-of-capacity-1 does NOT establish an immediate happens-before with `<-ch` by the buffered-channel rule. However, the unbuffered-channel rule does not apply here.

Wait — let us be precise. For buffered channels, the Go Memory Model states: "The kth receive from a channel with capacity C happens before the (k+C)th send from that channel completes." For capacity 1 and 1 receive: the 1st receive happens before the 2nd send completes — this governs the SENDER waiting for capacity, not the receiver. For the receiver: the send completing happens-before the receive completes? Actually the spec says for all channels: "A send on a channel is synchronized before the completion of the corresponding receive from that channel." This applies to buffered channels too — a send completes when there is space; when the receiver reads the value, that corresponds to the earlier send. So: goroutine writes x, goroutine sends (which completes because there is capacity), main receives (the receive from the buffered channel is the corresponding receive for that send — it sees the value). By the rule "send is synchronized before the corresponding receive completes," x=42 is visible. **Safe.**

**Snippet B: Data race — the reasoning is subtle.**

`sync.Once` guarantees that `Do(f)` runs `f` exactly once, and that all subsequent calls to `Do` return only after `f` has completed. The goroutine calls `once.Do(func() { x = 42 })`. If the goroutine's `Do` call executes `f` first, the main goroutine's no-op `Do` will wait for it. Once the main's `Do` returns, the function `f` (which wrote x=42) is guaranteed to have completed — establishing happens-before. If the main's no-op `Do` runs first (the goroutine hasn't started yet), the main's `Do` completes immediately and the goroutine's `Do` will not run `f` — then x remains 0. But: even if the goroutine's write runs first, there is **no guarantee that `main`'s `once.Do` waits for it**, because the main might call `Do` before the goroutine has. The result is non-deterministic: sometimes safe, sometimes racy. **Data race.** Fix: use `wg.Wait()` or a channel, not Once, for this synchronization pattern.

**Snippet C: Data race.**

`time.Sleep` is NOT a synchronization primitive. The Go Memory Model makes no guarantees about time-based ordering — only about explicit synchronization events. Even if the sleep makes the goroutine's write "almost certainly" complete first on every machine you test, there is no happens-before between `x = 42` and `fmt.Println(x)`. The race detector will flag this. **Fix:** replace `time.Sleep(...)` + read with `wg.Wait()` + read, which establishes happens-before via `wg.Done()` → `wg.Wait()` return.

</details>

---

## Exercise 4: Data-Race Analysis [🔴 Hard] [3 pts]

### Context
Identifying data races requires recognizing not just "is there a mutex?" but "does the synchronization establish happens-before for these specific memory accesses?" This exercise presents a realistic concurrent pattern with a subtle race.

### Task
Analyze the following program. It is supposed to be a simple concurrent cache. Identify:
1. Does it have a data race? If yes, on which variable(s) and between which operations?
2. What would the race detector output look like (describe it, don't run it)?
3. Fix the race with the minimal change that maintains the concurrent-read property.

```go
package main

import (
    "fmt"
    "sync"
)

type Cache struct {
    mu    sync.Mutex
    store map[string]string
}

func (c *Cache) Set(key, val string) {
    c.mu.Lock()
    c.store[key] = val
    c.mu.Unlock()
}

func (c *Cache) Get(key string) (string, bool) {
    // Intentional optimization attempt: skip the lock for reads
    val, ok := c.store[key] // QUESTION: is this safe?
    return val, ok
}

func main() {
    cache := &Cache{store: make(map[string]string)}
    var wg sync.WaitGroup

    for i := 0; i < 100; i++ {
        wg.Add(2)
        go func(n int) {
            defer wg.Done()
            cache.Set(fmt.Sprintf("key%d", n), "value")
        }(i)
        go func(n int) {
            defer wg.Done()
            cache.Get(fmt.Sprintf("key%d", n))
        }(i)
    }
    wg.Wait()
}
```

### Requirements
- [ ] Correctly identifies the data race (on the map)
- [ ] Explains why reading a map without a lock races with concurrent writes
- [ ] Proposes a fix — either `sync.RWMutex` for concurrent-safe reads, or a `sync.Map`
- [ ] Explains why RLock/RUnlock preserves concurrent read performance better than a plain Mutex

### Hints
<details>
<summary>Hint 1</summary>

Go maps are not safe for concurrent use. The Go runtime can detect concurrent map reads and writes and will panic with "concurrent map read and map write." But even without the panic, reading a map while another goroutine is writing is a data race per the memory model: there is no happens-before between the Set's store operation and the Get's read operation, because Get holds no lock.

</details>

<details>
<summary>Hint 2 (fix hint)</summary>

`sync.RWMutex` allows multiple concurrent readers (`RLock`/`RUnlock`) or one writer (`Lock`/`Unlock`), but not both simultaneously. Using `c.mu.RLock()` in `Get` and `c.mu.Lock()` in `Set` is the idiomatic fix for a read-heavy cache.

</details>

### Solution
<details>
<summary>Show Solution</summary>

**The race:** `Get` reads `c.store[key]` without holding any lock. `Set` writes `c.store[key]` while holding `c.mu.Lock()`. When a Set and a Get execute concurrently, there is no happens-before between them. This is a data race on the map. In Go, concurrent map access (one write + any other) is also detected at runtime and causes a panic: "fatal error: concurrent map read and map write." The race detector would report something like:

```
DATA RACE
Read at 0x... by goroutine N:
  main.(*Cache).Get(...)
      .../main.go:20
Previous write at 0x... by goroutine M:
  main.(*Cache).Set(...)
      .../main.go:14
```

**Fix using `sync.RWMutex`:**

```go
type Cache struct {
    mu    sync.RWMutex  // changed from sync.Mutex
    store map[string]string
}

func (c *Cache) Set(key, val string) {
    c.mu.Lock()         // exclusive write lock
    c.store[key] = val
    c.mu.Unlock()
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()        // shared read lock — multiple Readers can hold this simultaneously
    val, ok := c.store[key]
    c.mu.RUnlock()
    return val, ok
}
```

`RWMutex` establishes happens-before: `RUnlock` happens-before a subsequent `Lock`, and `Unlock` happens-before a subsequent `RLock`. Multiple goroutines can hold `RLock` simultaneously, preserving the concurrent-read property.

**Why not `sync.Map`?** `sync.Map` is optimized for the case where keys are written once and read many times, or when many goroutines use disjoint key sets. For a general-purpose cache with mixed read/write, `RWMutex` + regular map is simpler and often faster. Both are valid fixes; `RWMutex` is more idiomatic for a cache type.

</details>

---

## Exercise 5: GC Knobs and Tradeoffs [🟡 Medium] [2 pts]

### Context
`GOGC` and `GOMEMLIMIT` are the two primary knobs for GC behavior. Understanding their interaction and tradeoffs lets you make informed tuning decisions for production workloads.

### Task
Without writing a full program, answer the following in clear prose:
1. You have a batch data-processing job that allocates a lot of intermediate data and does not care about latency — it just needs to complete as fast as possible. Which `GOGC` setting would you choose (higher, lower, or off)? Why?
2. You have a container-hosted microservice limited to 512 MiB of memory. The service's live heap is typically ~100 MiB. What combination of `GOGC` and `GOMEMLIMIT` would you set? Why?
3. A colleague suggests setting `GOGC=off` permanently in the microservice to eliminate GC pauses. What is wrong with this suggestion?

### Requirements
- [ ] Correctly recommends high GOGC or GOGC=off for the batch job with a reason
- [ ] Correctly uses GOMEMLIMIT as the safety ceiling for the container case
- [ ] Identifies the flaw in GOGC=off for a long-running service (unbounded memory growth)

### Hints
<details>
<summary>Hint 1</summary>

`GOGC=off` completely disables the GC. For a job that allocates once and exits, this is fine. For a server that runs indefinitely, the heap grows without bound until the OS kills the process.

</details>

<details>
<summary>Hint 2</summary>

The recommended production pattern for container deployments (Go 1.19+): set `GOGC=off` or very high (e.g., 200–400) to reduce GC frequency, and set `GOMEMLIMIT` to ~90% of the container memory limit as a safety ceiling. The GC will aggressively collect if the limit is approached.

</details>

### Solution
<details>
<summary>Show Solution</summary>

**1. Batch job:** Use a very high `GOGC` (e.g., 400–1000) or even `GOGC=off` (via `debug.SetGCPercent(-1)`). The GC consumes CPU and pauses the program — for a batch job that will exit, letting the heap grow and collecting only at the end (or not at all) maximizes throughput. The risk is OOM if the heap exceeds available memory; set `GOMEMLIMIT` as a safety ceiling if necessary.

**2. Container microservice with 512 MiB limit, ~100 MiB live heap:**
```go
debug.SetGCPercent(200)          // allow heap to grow to 3× live before GC → ~300 MB
debug.SetMemoryLimit(460 << 20)  // 460 MiB ceiling (~90% of 512 MiB)
```
The high `GOGC` reduces GC frequency (fewer pauses), which helps latency. `GOMEMLIMIT` prevents the heap from growing past the container limit, which would cause OOM. The GC becomes more aggressive as memory approaches the limit — this is the safety net.

**3. GOGC=off for a long-running server:** This is wrong because the GC is never triggered. Every allocation adds to the heap permanently (until the process exits). The heap grows without bound — within hours or days the service will be killed by the OS for exceeding its memory limit or exhausting available RAM. `GOGC=off` is only safe for processes with a short, bounded lifetime. For a server, use a high but non-zero `GOGC` with a `GOMEMLIMIT` ceiling instead.

</details>

---

## Exercise 6: unsafe.Pointer Rules Quiz [🟢 Easy] [1 pt]

### Context
`unsafe.Pointer` has six documented rules in the Go spec. Knowing which operations are legal prevents crashes and GC-visible corruption.

### Task
For each code snippet below, state whether it is VALID or INVALID under the `unsafe.Pointer` rules, and give a one-sentence reason.

```go
// A: type-punning
var f float64 = 3.14
bits := *(*uint64)(unsafe.Pointer(&f))

// B: storing uintptr
var x int = 42
addr := uintptr(unsafe.Pointer(&x))
doWork() // may trigger GC or stack copy
y := *(*int)(unsafe.Pointer(addr))

// C: pointer arithmetic with unsafe.Add
s := []byte{1, 2, 3, 4}
p := unsafe.Pointer(&s[0])
third := *(*byte)(unsafe.Add(p, 2))

// D: converting uintptr back in same expression
var arr [4]int
p2 := (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&arr[0])) + unsafe.Sizeof(arr[0])))
```

### Solution
<details>
<summary>Show Solution</summary>

**A: VALID.** Converting `*float64` → `unsafe.Pointer` → `*uint64` in a single expression is the canonical type-punning pattern (rules 1 and 2). No pointer is stored as `uintptr`; the conversion is immediate.

**B: INVALID.** `addr` stores the address as a `uintptr`. After `doWork()` — which may trigger GC, which may copy the goroutine's stack — the `uintptr` value in `addr` may point to old memory that has been freed or repurposed. Converting it back with `unsafe.Pointer(addr)` is undefined behavior.

**C: VALID.** `unsafe.Add(p, 2)` performs pointer arithmetic and returns an `unsafe.Pointer` in a single expression. No `uintptr` is stored in a variable. This is the correct and safe way to do pointer arithmetic (rule 5 / the `unsafe.Add` function, Go 1.17+).

**D: VALID (but unusual style).** The `uintptr` arithmetic is entirely within one expression: `uintptr(unsafe.Pointer(&arr[0])) + unsafe.Sizeof(arr[0])` is computed and immediately converted back to `unsafe.Pointer` before the expression completes. No `uintptr` is stored. Prefer `unsafe.Add` (option C) for clarity.

</details>

---

## Exercise 7: cgo Cost Analysis [⭐ Challenge] [5 pts]

### Context
cgo enables Go programs to call C, but at real costs: call overhead, scheduler interaction, build complexity, and loss of cross-compilation. This challenge requires writing a micro-benchmark, observing the cost, and writing a recommendation memo.

### Task
1. Write a Go program that benchmarks cgo call overhead vs. Go function call overhead. Define a trivial C function `int noop(int x) { return x; }` and a trivially equivalent Go function `func noopGo(x int) int { return x }`. Benchmark both using `testing.B` (or a manual loop with `time.Now`). Aim for 10 million calls per measurement.

2. Below the benchmark code, write a short "when to use cgo" decision framework as a comment block. Address: (a) minimum performance bar before adding cgo, (b) build/CI requirements cgo imposes, (c) one scenario where cgo is clearly worth it and one where it clearly is not.

### Requirements
- [ ] Implements a `/*int noop(int x) { return x; }*/ import "C"` C function and a Go equivalent
- [ ] Measures both with a comparable loop count and prints the per-call cost for each
- [ ] Comments include a "when to use cgo" framework covering overhead, build requirements, and a clear yes/no example
- [ ] Output shows a significant overhead ratio (expect ~10–50× difference)

### Hints
<details>
<summary>Hint 1 (structure)</summary>

A manual benchmark loop:
```go
const N = 10_000_000
start := time.Now()
for i := 0; i < N; i++ {
    C.noop(C.int(i))
}
cgoDuration := time.Since(start)
// repeat for noopGo
```

</details>

<details>
<summary>Hint 2 (decision framework points)</summary>

Address: (1) cgo per-call overhead is ~100–200 ns (vs ~1–5 ns Go); any function called more than a few thousand times per second will have measurable overhead; (2) cgo requires a C compiler, disables `CGO_ENABLED=0` cross-compilation, complicates CI; (3) good example: wrapping libsqlite3 (no good pure-Go equivalent for embedded use); bad example: calling a C math function in a tight numerical loop.

</details>

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

/*
// A trivial C function to measure cgo call overhead
int noop_c(int x) { return x; }
*/
import "C"

import (
    "fmt"
    "time"
)

// Go equivalent — should be inlined by the compiler
func noopGo(x int) int { return x }

const N = 10_000_000

func benchCgo() time.Duration {
    start := time.Now()
    for i := 0; i < N; i++ {
        _ = C.noop_c(C.int(i))
    }
    return time.Since(start)
}

func benchGo() time.Duration {
    start := time.Now()
    for i := 0; i < N; i++ {
        _ = noopGo(i)
    }
    return time.Since(start)
}

// When to use cgo — decision framework:
//
// OVERHEAD: A cgo call costs ~100–200 ns on modern hardware (vs ~1–5 ns for a
// pure Go call). This means any C function called > ~5,000 times/sec adds
// measurable overhead. Before adding cgo, benchmark your hot path.
//
// BUILD REQUIREMENTS: cgo requires a C toolchain (gcc/clang) on every build
// machine, including CI. It disables cross-compilation unless you configure
// a cross-compiling C toolchain. Docker-based cross-compilation becomes
// significantly more complex. Set CGO_ENABLED=0 to verify your code compiles
// without cgo.
//
// USE cgo WHEN:
//   - Wrapping a large, stable C library with no adequate pure-Go equivalent
//     (e.g., libsqlite3 for embedded SQL, OpenSSL for hardware crypto acceleration,
//     BLAS/LAPACK for linear algebra). The integration cost is paid once; the
//     ongoing call overhead is amortized over large C-side computations.
//
// DO NOT USE cgo WHEN:
//   - Calling a simple C utility function in a tight loop (the overhead dominates)
//   - A pure-Go library exists (prefer it: no build complexity, race detector works)
//   - The program must cross-compile easily (e.g., distributing binaries for multiple
//     platforms from a single CI machine without cross-compilers)

func main() {
    cgoDur := benchCgo()
    goDur := benchGo()

    cgoPerCall := float64(cgoDur.Nanoseconds()) / float64(N)
    goPerCall := float64(goDur.Nanoseconds()) / float64(N)

    fmt.Printf("cgo noop:  %v total, %.1f ns/call\n", cgoDur, cgoPerCall)
    fmt.Printf("Go  noop:  %v total, %.1f ns/call\n", goDur, goPerCall)
    fmt.Printf("Overhead ratio: %.1fx\n", cgoPerCall/goPerCall)
    // Expected output on a modern machine:
    // cgo noop:  ~1.5s total, ~150 ns/call
    // Go  noop:  ~30ms total, ~3 ns/call
    // Overhead ratio: ~50x
}
```

**Step-by-step explanation:**

1. The C function `noop_c` is declared in the cgo comment block; `import "C"` must immediately follow with no blank line.
2. `benchCgo` measures 10M cgo calls; `benchGo` measures 10M pure Go calls of a trivially equivalent function.
3. The overhead ratio (typically 20–50×) demonstrates why cgo is inappropriate in hot inner loops.
4. The decision framework in comments addresses the three key dimensions: call overhead, build requirements, and appropriate use cases.

**What a weaker solution looks like:** Only benchmarking cgo without a Go baseline gives no useful comparison. Benchmarking a non-trivial C function conflates call overhead with the C computation time, making the overhead invisible.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — G-M-P Vocabulary | — | —/1 | — | — |
| Exercise 2 — GOMAXPROCS Observation | — | —/2 | — | — |
| Exercise 3 — Happens-Before Reasoning | — | —/3 | — | — |
| Exercise 4 — Data-Race Analysis | — | —/3 | — | — |
| Exercise 5 — GC Knobs and Tradeoffs | — | —/2 | — | — |
| Exercise 6 — unsafe.Pointer Rules Quiz | — | —/1 | — | — |
| Exercise 7 — cgo Cost Analysis | — | —/5 | — | — |
| **Total** | | **—/17** | | |

**Passing threshold:** 11/17 (65%). Aim for 14/17 (82%) before taking the test.
