# Questions — Module 16: Performance and Profiling

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

### Q001: Does sync.Pool guarantee you get back the same object you Put in?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The README explains that `sync.Pool` is used for object reuse to reduce allocations. When I call `pool.Put(obj)` and then `pool.Get()`, am I guaranteed to receive the same `obj` back, or might I receive an object that was Put by a different goroutine? And what happens to pooled objects during a GC cycle?

**My current hypothesis:**
I think `sync.Pool` does NOT guarantee you get the same object back — the pool is a concurrent free-list, and any goroutine's Get can receive any available object. I also believe the GC can clear the pool at any collection cycle, which is why the `New` function exists as a fallback. But I haven't verified whether the pool is cleared on every GC or only under memory pressure.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check pkg.go.dev/sync#Pool and the sync package source_

**Follow-up questions:**
- Does the GC clear `sync.Pool` on every major GC cycle, or only when memory is under pressure?
- Can pooled objects contribute to memory leaks if `New` allocates large objects?

---

### Q002: How does GOGC interact with GOMEMLIMIT when both are set?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README explains that `GOGC` sets the GC trigger percentage and `GOMEMLIMIT` sets a hard memory cap. If I set `GOGC=200` (less frequent GC) and `GOMEMLIMIT=256MiB` (strict cap), what happens when the heap grows quickly? Does `GOMEMLIMIT` override `GOGC` and trigger GC earlier than the 200% target? Is there a risk of the GC entering a "thrashing" state if the heap is naturally near the limit?

**My current hypothesis:**
I think `GOMEMLIMIT` takes priority — when the heap approaches the limit, the runtime ignores the `GOGC` percentage and runs GC aggressively to stay under the cap. If the live heap is naturally larger than the limit, the GC would thrash (run constantly without making progress), which is why setting `GOMEMLIMIT` below the actual live set size would be catastrophic.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check the GOMEMLIMIT documentation and the GC guide at go.dev/doc/gc-guide_

**Follow-up questions:**
- Is there a recommended ratio between live heap size and `GOMEMLIMIT`? (e.g., "set GOMEMLIMIT to 2× expected live heap")
- Does `debug.SetMemoryLimit` have the same behavior as the `GOMEMLIMIT` environment variable?

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
