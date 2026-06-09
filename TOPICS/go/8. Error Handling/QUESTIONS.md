# Questions — Module 8: Error Handling

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

### Q001: What does recover() return when called outside a deferred function?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says `recover` is "only useful inside a deferred function." If `recover()` is called from a normal (non-deferred) function while no panic is in progress — for example, called directly in the middle of main — what does it return? Does it return nil? Does it itself panic? Is it a compile error?

And a related case: if `recover()` is called from a function that is called *by* a deferred function (two levels deep), does it still work, or must it be directly in the deferred function?

**My current hypothesis:**
I think `recover()` called outside a panic's unwind just returns `nil` — so it is safe to call but a no-op. For the two-levels-deep case, I suspect it does NOT work — the Go spec likely requires `recover` to be called directly in a deferred function, not in a function called by a deferred function.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Handling_panics_

**Follow-up questions:**
- Does calling `recover()` unnecessarily (when not panicking) have any performance cost?
- Can you call `recover()` inside a goroutine spawned from a deferred function?

---

### Q002: Does errors.Is traverse all branches when errors.Join is used?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
`errors.Join` creates an error that wraps multiple errors — its `Unwrap() []error` method returns a slice rather than a single error. When I call `errors.Is(joinedErr, target)`, does `errors.Is` traverse all branches of the joined error, or just the first one?

For example:
```go
e1 := errors.New("alpha")
e2 := errors.New("beta")
joined := errors.Join(e1, e2)
fmt.Println(errors.Is(joined, e2)) // true or false?
```

**My current hypothesis:**
I believe `errors.Is` traverses all branches — the Go 1.20 release notes said `errors.Is` and `errors.As` were updated to support the `Unwrap() []error` method. So `errors.Is(joined, e2)` should return `true`.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check pkg.go.dev/errors and Go 1.20 release notes_

**Follow-up questions:**
- Does `errors.As` also traverse all branches of a joined error?
- What is the traversal order — depth-first left-to-right? Does it matter?

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
