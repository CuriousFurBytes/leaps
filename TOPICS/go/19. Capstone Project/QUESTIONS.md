# Questions — Module 19: Capstone Project

> Log questions as they arise — don't wait until you understand them fully.
> A question written down is a learning opportunity captured.
> For big-picture questions about the whole topic, use the topic-level QUESTIONS.md instead.
> These questions are specific to the build process and the design decisions in your project.

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
| ⏸ | Deferred — not urgent, revisit later |

---

## Question Format

```markdown
### Q{{N}}: {{SHORT_QUESTION_TITLE}}

**Asked:** {{YYYY-MM-DD}}
**Milestone:** M0 / M1 / ... (which milestone triggered this question)
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

### Q001: When should I use `context.WithTimeout` vs `context.WithDeadline`?

**Asked:** YYYY-MM-DD
**Milestone:** M4
**Status:** 🔴 Unanswered

**Full question:**
The `TimeoutMiddleware` uses `context.WithTimeout(r.Context(), 5*time.Second)`. But the Go standard library also has `context.WithDeadline` which takes an absolute `time.Time`. In what situations is one preferable to the other? Is there a performance difference?

**My current hypothesis:**
I think `WithTimeout` is just syntactic sugar for `WithDeadline(ctx, time.Now().Add(timeout))`, so they're equivalent. But I'm not sure if there's a semantic difference in how the context propagates to child contexts.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check pkg.go.dev/context_

**Follow-up questions:**
- If I set a 5-second timeout in middleware but the database driver also has its own timeout, which one takes effect?

---

### Q002: What happens to a pending database query when the request context is cancelled?

**Asked:** YYYY-MM-DD
**Milestone:** M2 / M4
**Status:** 🔴 Unanswered

**Full question:**
When `TimeoutMiddleware` cancels the context after 5 seconds, and the handler is in the middle of a `db.QueryRowContext(ctx, ...)` call in the store, what happens? Does the query continue running in the database? Does the driver abort the query? Does Go block until the query finishes, or does `QueryRowContext` return immediately with `context.DeadlineExceeded`?

I want to understand what resources are cleaned up and what might be left dangling.

**My current hypothesis:**
I think `QueryRowContext` returns `context.DeadlineExceeded` as soon as the context is cancelled, but I'm not sure if the underlying database query is also cancelled or if it continues running (and just discards its result).

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does the answer differ between SQLite and Postgres?

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
