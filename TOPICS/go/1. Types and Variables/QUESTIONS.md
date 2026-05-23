# Questions — Module 1: Types and Variables

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

### Q001: When should I choose `int` vs `int64`?

**Asked:** _YYYY-MM-DD_
**Status:** 🔴 Unanswered

**Full question:**
The module explains that `int` is platform-dependent (32-bit on 32-bit systems, 64-bit on 64-bit systems), while `int64` is always 64-bit. In practice, most servers are 64-bit, so `int` and `int64` are usually the same size. When does this distinction actually matter in production code?

**My current hypothesis:**
I think `int64` matters when writing data to disk or sending it over a network — where the byte layout must be consistent regardless of where the code runs. But for in-memory loop counters and array indices, `int` is probably fine.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec and "The Go Programming Language" book_

**Follow-up questions:**
- What does the Go standard library itself use — `int` or `int64` for lengths and indices?

---

### Q002: Can I do arithmetic between `int` and `float64` directly?

**Asked:** _YYYY-MM-DD_
**Status:** 🔴 Unanswered

**Full question:**
Go requires explicit type conversion. So `var x int = 5; var y float64 = 3.14; z := x + y` should fail to compile. But what exactly does the error message say, and what is the canonical fix?

**My current hypothesis:**
The compiler error is something like "mismatched types int and float64". The fix is `z := float64(x) + y`, converting `x` to `float64` before the addition.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Test in the Go playground at go.dev/play_

**Follow-up questions:**
- Are there any cases where Go does implicit numeric conversion (perhaps with untyped constants)?

---

### Q003: What exactly happens with `iota` if you skip lines in a const block?

**Asked:** _YYYY-MM-DD_
**Status:** 🔴 Unanswered

**Full question:**
`iota` increments for each constant in a block. But what if I use a blank identifier `_` to skip a value? Does `iota` still increment?

**My current hypothesis:**
I believe `_` in a const block does consume an `iota` value, because `_` is still a constant specification — it just discards the name. So:
```go
const (
    _ = iota  // 0, discarded
    A         // 1
    B         // 2
)
```
`A` should be `1`, not `0`.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — test in go.dev/play_

**Follow-up questions:**
- Is this pattern (`_ = iota` to skip 0) ever used in real Go code?

---

### Q004: Does Go's zero-value guarantee apply to struct fields?

**Asked:** _YYYY-MM-DD_
**Status:** ⏸ Deferred

**Full question:**
The module explains zero values for primitive types. But if I declare a struct variable without initializing it, do all its fields also get their zero values? This seems like it should be true, but I want to confirm.

**My current hypothesis:**
Yes — when you declare `var s MyStruct`, every field of `s` is initialized to its type's zero value. This is part of Go's "no garbage" guarantee. A struct's zero value is the struct with all fields zeroed.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be answered in the Structs module — deferring until then_

**Follow-up questions:**
- Can a struct be "usefully zero-valued" (work correctly without explicit initialization)? Is this a design pattern in Go?

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
| 🔴 Unanswered | 3 |
| 🟡 Partial | 0 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 1 |
| **Total** | **4** |
