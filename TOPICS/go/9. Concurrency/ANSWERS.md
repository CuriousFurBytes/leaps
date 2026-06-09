# Answer Key — Module 9: Concurrency

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

### 1.1 — Concurrency vs Parallelism [1 pt]

**Full credit answer:**
**Concurrency** is about structure: designing a program as multiple independent tasks that can be in progress at the same time, even on a single core (via interleaving). **Parallelism** is about execution: multiple tasks literally running at the same time on multiple CPU cores. A concurrent program may or may not be parallel depending on the available hardware.

**Key points required:**
- Concurrency = structure / dealing with many things at once
- Parallelism = execution / doing many things at once
- The distinction: concurrent programs can run on a single core; parallel requires multiple cores

**Common wrong answers:**
- *"Concurrency and parallelism are the same thing"* — They are not. This is the most common confusion. Rob Pike's talk "Concurrency is not Parallelism" is the definitive reference.
- *"Parallelism means using goroutines"* — Goroutines enable concurrency; whether they run in parallel depends on GOMAXPROCS and available cores.

---

### 1.2 — What happens when main returns with goroutines running [1 pt]

**Full credit answer:**
When `main` returns, the entire Go program terminates immediately. All goroutines — even those that are still running or blocked — are killed without any opportunity to finish their work. There is no automatic waiting. The programmer is responsible for synchronizing with goroutines before `main` returns (using `sync.WaitGroup`, channels, or other mechanisms).

**Key points required:**
- Program terminates immediately when `main` returns
- All goroutines are killed — there is no waiting
- The programmer must synchronize explicitly (WaitGroup, channel, etc.)

---

### 1.3 — Unbuffered vs buffered channels [1 pt]

**Full credit answer:**
An **unbuffered channel** (capacity 0) requires both a sender and a receiver to be ready at the same time — a send blocks until a goroutine receives, and a receive blocks until a goroutine sends. This is a rendezvous or synchronization point.

A **buffered channel** (capacity N) allows the sender to proceed without a receiver, as long as the buffer is not full. A send blocks only when the buffer is full; a receive blocks only when the buffer is empty.

**Key points required:**
- Unbuffered: both sides must be ready — send always blocks until receive
- Buffered: send blocks only when full; receive blocks only when empty
- Bonus: unbuffered is stronger synchronization (guarantees handoff at the same instant)

---

### 1.4 — WaitGroup.Add and why before launch [1 pt]

**Full credit answer:**
`wg.Add(n)` increments the WaitGroup's internal counter by `n`. `wg.Wait()` blocks until the counter reaches zero (each `wg.Done()` decrements by 1).

`Add` must be called before launching the goroutine because there is a race condition otherwise: if the parent goroutine calls `wg.Wait()` before the newly launched goroutine runs its `wg.Add(1)`, the counter is still 0 at the time of `Wait()`, so `Wait()` returns immediately — before the goroutine has done any work. Calling `Add` in the parent, before the launch, guarantees the counter is non-zero before `Wait()` is ever called.

**Key points required:**
- `Add(n)` increments the counter; `Done()` decrements; `Wait()` blocks until 0
- Race: if `Add` is inside the goroutine, `Wait` may see counter=0 before `Add` runs

---

### 1.5 — Closing a channel [1 pt]

**Full credit answer:**
Closing a channel with `close(ch)` signals to receivers that no more values will be sent. Receivers can detect a closed channel using the comma-ok form (`v, ok := <-ch`; `ok` is `false` when the channel is closed and empty) or by using `for range` (the loop exits when the channel is closed and empty). Receiving from a closed-and-empty channel returns the zero value and `ok == false` — it does **not** panic.

**Sending to a closed channel panics** at runtime.

**Key points required:**
- `close` signals "no more sends" to receivers
- Receiving from a closed channel: safe, returns zero value + `ok=false`
- Sending to a closed channel: **panics**
- Closing a closed channel: also **panics**

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Loop variable capture bug [2 pts]

**Full credit answer:**
When goroutines are launched inside a loop and the goroutine closure references the loop variable `i` directly, all goroutines share the same variable `i`. By the time the goroutines run, the loop has often completed and `i` holds its final value (e.g., 5 after a loop from 1 to 5). Every goroutine sees this final value rather than the value at the time it was launched.

**Incorrect output example:**
```go
for i := 0; i < 5; i++ {
    go func() { fmt.Println(i) }()
}
// Likely prints: 5 5 5 5 5 (or similar repeated value)
```

**Fix 1 — pass as argument:**
```go
for i := 0; i < 5; i++ {
    go func(id int) { fmt.Println(id) }(i)  // i copied into id at launch time
}
```

**Fix 2 — Go 1.22+ loop variable scoping:**
In Go 1.22 and later, each loop iteration creates a new variable for `i`, so the closure captures the per-iteration value. However, passing as an argument is still preferred for clarity and compatibility with older Go versions.

**Rubric:**
- 2 pts: Correctly explains the shared-variable mechanism AND incorrect output AND provides at least one correct fix
- 1 pt: Identifies that it's a variable capture issue and gives a fix, but the explanation of why is unclear
- 0 pts: Doesn't understand that all goroutines share the same variable

---

### 2.2 — select behavior in three scenarios [2 pts]

**Full credit answer:**

**(a) No case ready, no default:** `select` blocks until at least one case becomes ready. The goroutine is suspended and will be resumed when one of the channel operations can proceed.

**(b) No case ready, with default:** The `default` case runs immediately. `select` never blocks when a `default` is present — it is the "try, don't wait" form.

**(c) Multiple cases ready simultaneously:** Go picks **one case at random** (uniform pseudo-random selection, as guaranteed by the specification). No case is guaranteed to be favored — this prevents starvation and ensures fairness over time.

**Rubric:**
- 2 pts: All three scenarios correctly described; specifically mentions "random" for (c) — not "first" or "last" or "any"
- 1 pt: Correctly describes two of the three, or describes all three but says "implementation-defined" instead of "random" for (c)
- 0 pts: Wrong on two or more scenarios

---

### 2.3 — Communication vs sharing + when mutex is better [2 pts]

**Full credit answer:**
"Do not communicate by sharing memory; share memory by communicating" means: instead of having goroutines read and write the same variable (sharing memory) with locks protecting it, have goroutines pass data to each other via channels (the data moves from one goroutine to another, so at any point only one goroutine "owns" it). This eliminates the class of bugs caused by unsynchronized shared access because there is no shared mutable state to accidentally read or write.

**When channels are right:** A pipeline where stage A produces values and stage B processes them — the data naturally flows from A to B via a channel, and neither goroutine needs to share any variable.

**When a mutex is better:** A shared cache (`map[string]string`) accessed by hundreds of goroutines doing mostly reads and occasional writes. Using a channel would require a "cache manager" goroutine to serialize all reads and writes — adding latency for the common case of concurrent reads. A `sync.RWMutex` allows many concurrent readers and only blocks for writes, which is more efficient and more natural.

**Rubric:**
- 2 pts: Correctly explains the philosophy (channels avoid shared mutable state), gives a valid channel scenario, AND gives a valid mutex scenario with reasoning
- 1 pt: Correctly explains the philosophy but only gives one scenario, or gives both but without reasoning for the mutex choice
- 0 pts: Does not correctly explain the philosophy

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Goroutine squares with channel and WaitGroup [3 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    results := make(chan int, 4) // buffered — goroutines never block
    var wg sync.WaitGroup

    for i := 1; i <= 4; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            results <- id * id
        }(i)
    }

    // Close results after all goroutines finish
    go func() {
        wg.Wait()
        close(results)
    }()

    for v := range results {
        fmt.Println(v)
    }
}
// Output: 1, 4, 9, 16 in some order
```

**Rubric:**
- 3 pts: Correct program; `wg.Add` before launch; `wg.Done` via defer; separate goroutine closes channel after `wg.Wait`; `for range` to collect; compiles and is race-free
- 2 pts: Correct logic but minor issue — e.g., not using `defer wg.Done()`, or closing in main (which would deadlock if range is in main), or missing the separate closing goroutine
- 1 pt: Correct structure but incomplete — e.g., forgets to close the channel (range would block forever) or has a data race
- 0 pts: Does not use goroutines and channels, or has a fundamental structural error

**Teaching note:** The key insight is that you need a separate goroutine to call `wg.Wait()` and `close(results)` — you cannot do both `for range results` and `wg.Wait(); close(results)` sequentially in the same goroutine, because `for range` would block before `wg.Wait()` is called.

---

### 3.2 — withRetry using select/time.After [3 pts]

**Full credit answer:**
```go
package main

import (
    "errors"
    "fmt"
    "time"
)

func withRetry(fn func() error, attempts int, delay time.Duration) error {
    var lastErr error
    for i := 0; i < attempts; i++ {
        if err := fn(); err == nil {
            return nil // success
        } else {
            lastErr = err
        }
        if i < attempts-1 {
            // Wait for delay using time.After in a select
            select {
            case <-time.After(delay):
                // delay elapsed — try again
            }
        }
    }
    return lastErr
}

// Demonstration
func main() {
    callCount := 0
    fn := func() error {
        callCount++
        if callCount < 3 {
            return errors.New("not ready yet")
        }
        return nil
    }

    err := withRetry(fn, 5, 10*time.Millisecond)
    fmt.Printf("Result: %v, calls: %d\n", err, callCount)
    // Output: Result: <nil>, calls: 3
}
```

**Acceptable alternative (simpler time.After usage):**
```go
func withRetry(fn func() error, attempts int, delay time.Duration) error {
    var lastErr error
    for i := 0; i < attempts; i++ {
        if err := fn(); err == nil {
            return nil
        } else {
            lastErr = err
        }
        if i < attempts-1 {
            <-time.After(delay) // receive from time.After — waits for delay
        }
    }
    return lastErr
}
```

**Rubric:**
- 3 pts: Correct retry loop (returns nil on first success, returns last error if all fail), uses `time.After` or `select`+`time.After` for delay, no delay after the final attempt
- 2 pts: Correct retry logic but always delays (including after the last attempt), or uses `time.Sleep` directly instead of `time.After`
- 1 pt: Correct general structure but has an off-by-one error (e.g., only tries `attempts-1` times) or doesn't return the last error
- 0 pts: Does not implement retry or does not track the last error

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Channel deadlock analysis [3 pts] (1 pt each part)

**(a) Does this program deadlock?**
**No — this specific program does not deadlock.** Here is the execution:

1. The `for` loop launches 5 goroutines. Each goroutine tries to send its ID on the unbuffered channel `ch`. Since `ch` is unbuffered, each send blocks until a receiver is ready.
2. The second `for` loop in `main` calls `<-ch` five times. Each receive unblocks one of the waiting goroutines.
3. After 5 goroutines have sent and 5 receives have completed, all goroutines have exited and main prints "all done".

The program works correctly. It does not deadlock because the number of sends (5) exactly matches the number of receives (5). Output: the 5 IDs printed in some order, then "all done".

**(b) 6 goroutines, 5 receives — what happens to the 6th?**
The 6th goroutine sends on `ch`, but after 5 receives complete, main reaches the end of its receive loop and calls `fmt.Println("all done")`, then returns — which terminates the program. The 6th goroutine is still blocked on `ch <- id` when the program exits. Its send never completes; the goroutine is simply killed.

If `main` did not exit (e.g., there was more code after the receive loop), the 6th goroutine would block forever, leaking. In this specific program, the exit masks the goroutine leak.

**(c) How to reliably print "all done" and avoid the leak**
Use a buffered channel with capacity 6, or use a `sync.WaitGroup` to track goroutines separately from the channel receives. Or, better yet, close the channel from the sender side and use `for range` to drain exactly what was sent:

```go
// Fix: match goroutines and receives, or use a buffered channel
ch := make(chan int, 6) // buffer all 6 sends without blocking
for i := 1; i <= 6; i++ {
    go func(id int) { ch <- id }(i)
}
close(ch) // wait — actually you can't safely close here; goroutines may not have sent yet
// Better fix: use sync.WaitGroup to count goroutines, separate from counting receives
```

The cleanest fix is to make the number of receives match the number of sends (change the receive loop to `i < 6`), or use a `sync.WaitGroup` and channel combination.

**Rubric:**
- 1 pt for (a): Correctly states the program does NOT deadlock, and traces why (matching sends and receives)
- 1 pt for (b): Correctly identifies that the 6th goroutine is blocked on a send and is killed when main exits; names this as a goroutine leak
- 1 pt for (c): Provides a valid fix — matching the counts, using a buffered channel appropriately, or a WaitGroup-based solution

---

## Section 5: Discussion — Answer Key

### 5.1 — Race detector limitations [2 pts]

**Example strong answer:**
The race detector is a dynamic analysis tool — it reports races that actually occur during a specific program execution, not all possible races. It instruments every memory access and compares timestamps to detect when two goroutines access the same address without proper synchronization between the accesses. If a race requires a specific interleaving of goroutines that doesn't happen to occur during the test run, the race detector will not report it even if the race is theoretically possible.

This means that a program that passes `-race` in CI may still have undetected races that only manifest under high load, different scheduling, or on different hardware. The race detector cannot substitute for careful concurrent design — it is a safety net, not a proof.

In practice, the race detector should be run in CI on every test run (it adds roughly 5–10× overhead to execution time and 2–20× memory overhead, which is acceptable for tests but not production binaries). It should also be enabled on integration/stress tests and load tests, since those exercise more interleavings. The race detector significantly increases confidence but never provides a guarantee of race-freedom.

**Elements that earn full credit:**
- Correctly identifies that the race detector is dynamic (reports observed races, not all possible races)
- Explains what "possible but not observed" means (timing-dependent races)
- Discusses practical CI usage (run `-race` always, use stress tests to exercise more paths)
- Does not overclaim ("passing `-race` means no races") or underclaim ("the race detector is useless")

**Rubric:**
- 2 pts: Correctly explains dynamic vs static analysis, names the timing-dependency limitation, and gives practical guidance on using the detector in CI
- 1 pt: Correctly identifies the limitation (not all races are detected) but without explaining why (timing) or without practical guidance
- 0 pts: Claims the race detector proves absence of races, or claims it is not useful

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — merge function [+5 pts]

**Full credit answer:**
```go
package main

import (
    "fmt"
    "sync"
)

// merge combines multiple input channels into a single output channel.
// The output channel is closed when all input channels are closed.
func merge(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    // Launch one goroutine per input channel
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c { // drain until c is closed
                out <- v
            }
        }(ch) // pass channel as argument — avoids closure capture of loop variable
    }

    // Close out after all input goroutines finish
    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

func makeChannel(vals ...int) <-chan int {
    ch := make(chan int, len(vals))
    for _, v := range vals {
        ch <- v
    }
    close(ch)
    return ch
}

func main() {
    ch1 := makeChannel(1, 2, 3)
    ch2 := makeChannel(4, 5)
    ch3 := makeChannel(6, 7, 8, 9)

    for v := range merge(ch1, ch2, ch3) {
        fmt.Print(v, " ")
    }
    fmt.Println()
}
// Output: 1 2 3 4 5 6 7 8 9 in some order
// (nondeterministic — all 9 values, order varies)
```

**Edge cases handled:**
- `merge()` with no arguments: `wg.Wait()` returns immediately (counter=0), `close(out)` is called, `for range` on the output exits immediately. Correct.
- `merge(ch)` with one argument: works — one goroutine drains `ch`, closes `out`. Correct.

**Rubric:**
- 5 pts: Correct implementation with WaitGroup, separate goroutine for close, per-channel goroutines, channel passed as argument (not captured from loop), works for 0/1/N channels, demonstrates in main
- 3 pts: Correct for N>1 channels but fails the edge case of 0 channels; or doesn't pass the channel as an argument (closure capture bug — may produce wrong results)
- 1 pt: Correct structure but has a race or deadlock in edge cases

---

## Common Wrong Answers Across the Test

1. **Thinking `time.Sleep` is synchronization** — `time.Sleep` is not a correct synchronization mechanism. It may work in practice on most machines most of the time, but it is not a guarantee. Students who use `time.Sleep` in Section 3 answers need to review `sync.WaitGroup` and channels as the correct tools.

2. **Closing a channel from the receiver side** — Only the sender (the goroutine that "owns" the channel) should close it. Closing from the receiver or from multiple goroutines leads to panic. A common mistake is closing in the `for range` loop body rather than after the send loop.

3. **`select` is deterministic when multiple cases are ready** — Some students assume the first case in source order is always chosen. The Go specification guarantees uniform pseudo-random selection. Code that relies on ordering between ready cases is incorrect.

4. **Race detector proves race-freedom** — A common misconception in Section 5. The race detector is dynamic; it can only report races it observes.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 3.1 likely don't understand the "separate goroutine to close" pattern. The key insight: you cannot have `wg.Wait(); close(ch)` and `for range ch` in the same goroutine sequentially, because `for range` blocks the goroutine and `wg.Wait()` never runs. The close goroutine is the standard Go solution.

- Students who struggle with Section 4.1(a) may be over-applying the "deadlock" pattern. Not every program with unbuffered channels deadlocks — the key is whether sends and receives are balanced and have matching partners. Encourage them to trace execution manually with a small example.

- Students who score below 60% on this module may not have solid closure fundamentals. Ask: can they explain the loop variable capture bug from memory without notes? Can they write a WaitGroup program correctly? If not, they need to re-study before proceeding to [[go/12. Advanced Concurrency Patterns]], which builds heavily on this module.

- The bonus question tests understanding of the fan-in pattern. The loop variable capture issue (`go func(c <-chan int) { ... }(ch)`) appears here — students who miss this may get wrong output. This is a good teaching moment about why closures in goroutines need careful attention.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
