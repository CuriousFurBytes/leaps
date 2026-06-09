# Questions — Module 3: Functions

> Log questions as they arise — don't wait until you understand them fully.
> A question written down is a learning opportunity captured.
> For big-picture questions about the whole topic, use the topic-level QUESTIONS.md instead.

---

## How to Use This File

1. Write the question the moment it occurs to you, even if you can't articulate it well yet.
2. Come back and refine the question once you understand it better.
3. Update the status as you research or find answers.
4. Link to the source where you found the answer.
5. Capture follow-up questions — good answers always raise new ones.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Unanswered — needs active research |
| 🟡 | Partial — have some understanding, still incomplete |
| 🟢 | Answered — well understood, could explain to someone else |
| ⏸ | Deferred — not urgent, revisit in a later module |

---

## Question Format

```markdown
### Q{{N}}: {{SHORT_QUESTION_TITLE}}

**Asked:** {{YYYY-MM-DD}}
**Status:** 🔴 Unanswered

**Full question:**
The complete question with all relevant context.

**My current hypothesis:**
What you think the answer might be, even if speculative.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Where you found or verified the answer_

**Follow-up questions:**
- _New questions this answer raised_
```

---

## Questions

### Q001: Do captured variables get moved to the heap when a closure outlives the outer function?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
When a closure captures a variable from an outer function, and the outer function returns while the closure still exists (e.g., it was returned or passed to a goroutine), the captured variable clearly cannot live on the call stack anymore — the stack frame has been popped. So where does it live? Does Go automatically move it to the heap? Is there a performance cost to this? And if a closure captures a large struct, does the entire struct move to the heap?

**My current hypothesis:**
Go's escape analysis must detect when a variable's address is captured by a closure that may outlive the declaring function. In that case, Go allocates the variable on the heap instead of the stack. This is called "escape to the heap." There is a real allocation cost compared to a stack variable — the GC must eventually collect it. I believe `go build -gcflags="-m"` shows escape analysis decisions.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check [[go/16. Performance and Profiling]] for escape analysis details, or run `go build -gcflags="-m"` on a simple closure example_

**Follow-up questions:**
- Does Go always move variables to the heap when captured, or only when the closure provably outlives the function?
- What is the typical overhead of a heap-allocated closure variable vs a stack variable?

---

### Q002: If a function has both `defer f.Close()` and `defer func() { err = ... }()`, in what order do they run?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
In the error-wrapping pattern, we use:
```go
func readFile(path string) (data []byte, err error) {
    defer func() {
        if err != nil { err = fmt.Errorf("readFile: %w", err) }
    }()

    f, err := os.Open(path)
    if err != nil { return }
    defer f.Close()  // registered second
    // ...
}
```

The README says defers run in LIFO order. So `f.Close()` (registered second) would run before the error-wrapping closure (registered first). Does that mean `f.Close()` errors won't be captured by the error-wrapping defer? Could `f.Close()` set `err` to something that the outer wrapper would then wrap?

**My current hypothesis:**
`f.Close()` is a regular deferred call, not a closure — it returns an error but nobody captures it (since `defer f.Close()` discards the return value). The error-wrapping closure runs after `f.Close()` because it was deferred first (LIFO means last-in first-out, so it runs last). So `f.Close()`'s error, if any, is silently ignored, and the wrapping closure only sees the error from `io.ReadAll` or `os.Open`. This could be a bug if the file wasn't fully flushed. For write operations, you should check `f.Close()`'s return value.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/blog/defer-panic-and-recover for LIFO ordering, and Effective Go for the f.Close() error pattern_

**Follow-up questions:**
- What is the idiomatic way to handle errors from `f.Close()` when you also have an error from writing?

---

_Add new questions below this line. Keep them numbered sequentially._

---

## Resolved Questions Archive

_Move fully answered 🟢 questions here to keep the active list clean._

_(none yet)_

---

## Question Stats

| Status | Count |
|--------|-------|
| 🔴 Unanswered | 2 |
| 🟡 Partial | 0 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **2** |
