# Questions — Module 17: Runtime Internals and the Memory Model

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

### Q001: Does work-stealing check the local queue first or the global queue first?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The README says a P checks its local run queue first, then can steal from other Ps or pull from the global run queue. But I'm not sure of the priority order. Specifically:

1. When a P's local queue is empty, does it immediately attempt to steal from other Ps, or does it first check the global queue?
2. The README mentions "every 61 scheduling ticks" for checking the global queue — what exactly counts as a scheduling tick? Is it every goroutine switch?

**My current hypothesis:**
I think the P checks the global queue periodically (every ~61 ticks) for fairness, and steals from other Ps when its local queue is empty. So the order might be: local queue → (periodic) global queue → steal from other Ps. But I haven't verified this against the runtime source code.

**Answer:**
_To be filled in — check runtime/proc.go in the Go source for `findRunnable`_

**Source / Confirmed by:**
_To be filled in — golang.org/src/runtime/proc.go_

**Follow-up questions:**
- What happens when all Ps are empty — does the M park or spin?

---

### Q002: When exactly is it safe to store a uintptr from unsafe.Pointer?

**Asked:** YYYY-MM-DD
**Status:** 🟡 Partial

**Full question:**
The module README says: "only valid if the `uintptr` was derived from `unsafe.Pointer` in the same expression." But what exactly counts as "the same expression"?

For example, are any of these safe?

```go
// Case 1: single assignment then immediate use
p := unsafe.Pointer(&x)
addr := uintptr(p)
q := (*int)(unsafe.Pointer(addr)) // is this safe?

// Case 2: everything in one line
q := (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&x)) + 8))

// Case 3: passing uintptr to a function
func offset(p unsafe.Pointer, n uintptr) unsafe.Pointer {
    return unsafe.Pointer(uintptr(p) + n) // is this safe inside the function?
}
```

**My current hypothesis:**
Case 2 looks safe — it is all one expression. Case 1 might not be safe because a GC can run between the assignment to `addr` and its use. Case 3 might be safe if the conversion from `uintptr` back to `unsafe.Pointer` happens before any function call that could trigger GC, but I'm not sure. The unsafe package docs should clarify.

**Answer:**
_To be filled in — see pkg.go.dev/unsafe#Pointer, specifically the section on uintptr conversion_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does `unsafe.Add` fully replace the need for `uintptr` arithmetic in all normal cases?

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
| 🔴 Unanswered | 1 |
| 🟡 Partial | 1 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **2** |
