# Questions — Module 6: Methods and Interfaces

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

### Q001: Can you define a method on a pointer to an interface?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says you can define methods on any named local type. An interface is a named local type. Can you write `func (r *io.Reader) DoSomething()` — i.e., a method with a pointer-to-interface receiver? If not, what is the exact compile-time error, and why does Go prohibit it?

**My current hypothesis:**
I suspect Go prohibits this because defining methods on a pointer to an interface creates ambiguity — the method receiver would be a pointer to an interface value, not a pointer to the concrete type. The compiler likely requires that the receiver type be a non-interface named type. But I'm not certain.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Method_declarations_

**Follow-up questions:**
- Is there ever a legitimate reason to pass a `*io.Reader` instead of `io.Reader`? (I've seen it in some codebases and it always looked wrong.)

---

### Q002: Does struct embedding automatically satisfy interfaces?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
If `type Writer struct {}` has a method `Write(p []byte) (int, error)`, and `type LogWriter struct { Writer }` embeds `Writer`, does `LogWriter` automatically satisfy `io.Writer`? The README mentions that struct embedding promotes methods — I want to confirm whether promoted methods count toward interface satisfaction, and whether they count for both value and pointer receiver embeddings.

**My current hypothesis:**
I believe promoted methods do count toward interface satisfaction, because method promotion makes the embedded type's methods part of the outer type's method set. So `LogWriter` would satisfy `io.Writer` through the promoted `Write` method. But I'm not certain whether the pointer/value distinction matters here — e.g., does embedding a value type vs a pointer type affect which methods are promoted?

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- If two embedded types both have a method with the same name, which one is promoted? Is this a compile error?

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
