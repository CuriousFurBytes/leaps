# Questions — Module 11: Testing and Benchmarking

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

### Q001: Does t.Parallel() inside t.Run make the subtest parallel with siblings or with top-level tests?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README shows `t.Parallel()` used both at the top of a test function and inside `t.Run` subtests. When called inside a subtest (i.e., `t.Run("name", func(t *testing.T) { t.Parallel(); ... })`), does it make the subtest run concurrently with its sibling subtests, with other top-level tests in the package, or both?

Specifically:
- If I have TestA and TestB at the package level, and TestA has subtests A/1 and A/2 marked as parallel, do A/1 and A/2 run concurrently with each other, or concurrently with TestB?
- Is there a way to have subtests run in parallel with each other but not with top-level tests outside their parent?

**My current hypothesis:**
I believe `t.Parallel()` inside a subtest makes it parallel with its sibling subtests — other `t.Run` calls inside the same parent. The parent test function blocks until all parallel subtests complete. But I'm not certain whether they can also run concurrently with other package-level tests.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check pkg.go.dev/testing#T.Parallel and the Go blog on subtests_

**Follow-up questions:**
- Is there a maximum number of goroutines that `go test` will use for parallel tests? Does `-parallel N` control this?

---

### Q002: What exactly does b.N mean — is it the total number of iterations or the number of warmup iterations?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says "b.N is set by the framework; it runs until results are stable." But the mechanics are unclear: does the framework run the entire benchmark loop once, look at the time, then choose a larger N and run it again? Or does it run a warmup phase and then a single measurement phase?

For example, if a benchmark prints something for each iteration, does it print once for the warmup and then once for the real measurement, or does it only print during the final measurement run?

**My current hypothesis:**
I think the framework starts with a small N (like 1 or 100), measures the total duration, and then scales N up until the total time exceeds about 1 second. This means the benchmark body runs multiple times with increasing N values. Side effects inside the loop (like printing) would happen multiple times across these iterations, not just once.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check the testing package source or the Go testing documentation_

**Follow-up questions:**
- If my benchmark has a side effect (like writing to a database), would the multiple framework-controlled runs cause problems?

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
