# Questions — Module 2: Control Flow

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

### Q001: Does `fallthrough` check the next case's condition, or skip it?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README explains that `fallthrough` causes execution to continue into the next case. But does Go first evaluate the next case's condition expression, or does it unconditionally fall through regardless of what the condition would be?

For example:

```go
n := 1
switch n {
case 1:
    fmt.Println("one")
    fallthrough
case 2:
    fmt.Println("two")  // does this run when n=1 with fallthrough?
}
```

The README says "fallthrough transfers control unconditionally" — but I want to verify this with a concrete example.

**My current hypothesis:**
I think fallthrough is unconditional — the next case body runs even if its condition would not have matched. This is consistent with the README's warning that `fallthrough` in Go is "unconditional". But I haven't run this code yet to confirm.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Fallthrough_statements_

**Follow-up questions:**
- Can you use `fallthrough` in the last case of a switch? (I suspect it's a compile error.)
- Can you use `fallthrough` in a type switch?

---

### Q002: What happens when you range over a nil slice or nil map?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
In Go, a nil slice and a nil map are both valid zero values. If I write `for i, v := range nilSlice` or `for k, v := range nilMap` where the variable is nil, does the program panic, or does the loop simply execute zero times?

**My current hypothesis:**
I think ranging over a nil slice or nil map is safe and simply executes zero iterations — similar to ranging over an empty slice/map. This would be consistent with Go's general approach of making nil zero values safe to use. But I haven't verified this.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does ranging over a nil channel block or panic?

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
