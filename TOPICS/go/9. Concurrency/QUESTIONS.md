# Questions — Module 9: Concurrency

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

### Q001: What exactly happens in the runtime when it detects "all goroutines are asleep"?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README explains that when a deadlock occurs, the Go runtime prints `fatal error: all goroutines are asleep - deadlock!` and terminates. But what is the mechanism? Does the runtime have a background thread watching goroutine states? Is this checked on every context switch? Is there a latency between the deadlock occurring and the crash?

Also: the README notes that if there are background goroutines that are not blocked (e.g., a goroutine running a timer), the runtime will not detect a partial deadlock. How exactly does the runtime determine "all" goroutines are asleep — does it track goroutines globally?

**My current hypothesis:**
I think the runtime checks after every goroutine context switch: if the run queue is empty and the number of goroutines waiting exceeds some threshold, it triggers the deadlock report. But I'm uncertain about the mechanism, especially the "background goroutine prevents detection" case.

**Answer:**
_To be filled in — check [[go/17. Runtime Internals and the Memory Model]] and go.dev/ref/spec_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Can I intentionally trigger this in a test to demonstrate deadlock detection?
- Does `go vet` catch any deadlock patterns statically?

---

### Q002: Is `select` case selection truly uniform random, or is it implementation-defined?

**Asked:** YYYY-MM-DD
**Status:** 🟡 Partial

**Full question:**
The module README states that when multiple `select` cases are ready simultaneously, Go picks one "at random (uniformly)." But is this guaranteed by the language specification, or is it just the current implementation's behavior?

If it is implementation-defined, could a future version of Go or an alternative Go implementation (like TinyGo) choose a different policy — for example, FIFO order? Could programs I write that rely on approximate fairness break in a future Go version?

**My current hypothesis:**
I believe the Go specification says "a uniform pseudo-random selection" when multiple cases are ready (I've seen this stated in the spec). So it is a language guarantee, not just an implementation detail. But I want to verify the exact spec wording and understand whether "pseudo-random" implies any particular distribution.

**Answer:**
_To be filled in — check go.dev/ref/spec#Select_statements_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does the pseudo-random selection use the same source as `math/rand`, or is it a separate internal RNG?
- Can a channel be "starved" in a select even with random selection if one channel always produces values faster than the other?

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
