# Notes — Module 12: Advanced Concurrency Patterns

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/12. Advanced Concurrency Patterns]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Advanced Concurrency))
    context.Context
      WithCancel / WithTimeout / WithDeadline
      WithValue pitfalls
      first-parameter convention
      ctx.Done() and ctx.Err()
      propagation through call tree
    Pipelines
      stages linked by channels
      defer close(out)
      cancellation via ctx.Done() on sends
    Fan-Out / Fan-In
      one input to many workers
      merge channels with WaitGroup
    Worker Pools
      fixed N workers
      jobs channel with back-pressure
      semaphore via buffered channel
    Rate Limiting
      time.Ticker simple case
      golang.org/x/time/rate token bucket
    Atomics
      atomic.Int64 / atomic.Pointer
      CAS for conditional updates
      non-composable
    sync.Pool
      object reuse / allocation reduction
      GC may clear at any time
    errgroup
      WithContext pattern
      first error cancels group
      g.Wait() return
    Goroutine Leaks
      always provide exit path
      buffer-of-1 trick
      goleak in tests
    Graceful Shutdown
      signal.NotifyContext
      drain phase with timeout
      wg.Wait + select
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **Context is not optional plumbing:** _I finally understood that `context.Context` is not boilerplate — it's the mechanism by which every function in a call tree can be told "stop, the client gave up". Without it, goroutines and database queries continue running after the HTTP response has already been sent._
2. **Every goroutine needs a termination condition:** _The goroutine leak mental model clicked when I realized: a goroutine is like a thread you start but forget to join. Unless it has a `ctx.Done()`, a closed channel, or a done condition, it runs until the process exits — silently consuming memory._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### context.Context

_Your explanation here_

_What I'm still unsure about:_ (e.g., when exactly the deadline timer goroutine is cleaned up)

### Pipelines and cancellation

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens if a stage panics — does the pipeline drain cleanly?)

### Worker pool vs semaphore

_Your explanation here_

_What I'm still unsure about:_ (e.g., when to prefer a semaphore over a pool)

### errgroup

_Your explanation here_

_What I'm still unsure about:_ (e.g., whether errgroup.SetLimit sets a semaphore on goroutine count)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| context.Context cancellation | [[go/9. Concurrency]] — channels and select | ctx.Done() is just a receive-only channel; the select pattern is from Module 9 |
| errgroup error propagation | [[go/8. Error Handling]] | errgroup returns the first non-nil error using the same `error` interface and wrapping conventions |
| atomic.Int64 memory guarantees | [[go/17. Runtime Internals and the Memory Model]] | atomics provide sequential consistency — the happens-before guarantees are formally defined in the memory model |
| Goroutine leaks | [[concurrency]] | Shared concept across languages: a goroutine is like a thread that must be explicitly given a way to terminate |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] Does `errgroup` limit the number of concurrent goroutines (like a pool), or does it just aggregate errors? → added to QUESTIONS.md as Q001
- [ ] Is `sync.Pool` safe to use for objects that contain `sync.Mutex`? → needs investigation
- [ ] What happens if `context.WithValue` is called with the same key twice? Does the second value shadow the first? → might be in pkg.go.dev/context docs

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The canonical context-aware operation

```go
select {
case result := <-workCh:
    process(result)
case <-ctx.Done():
    return ctx.Err()
}
```

_Why I'm saving this:_ Every context-aware operation is a `select` that races work against `ctx.Done()`. This is the atomic unit of context integration.

---

### defer cancel() — always, immediately

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel() // line 2, right after line 1. Never skip this.
```

_Why I'm saving this:_ The resource leak from missing `cancel()` is invisible until the service is under load. Defer it immediately — it's always safe to call and always required.

---

### Worker pool skeleton

```go
jobs := make(chan T, N)
results := make(chan R)
var wg sync.WaitGroup
for i := 0; i < numWorkers; i++ {
    wg.Add(1)
    go worker(&wg, jobs, results)
}
go func() { wg.Wait(); close(results) }()
```

_Why I'm saving this:_ This is the repeatable structure for every bounded worker pool. Fill `jobs`, close it, range over `results`.

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **Missing `defer cancel()`** — I initially skipped it when the timeout fires before `cancel()` anyway, but learned that the timer goroutine leaks without it even after the context expires.
- **Closing a channel from the receiver** — I tried to close the `out` channel from the fan-in consumer goroutine, which panics if any sender fires a send after the close.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
