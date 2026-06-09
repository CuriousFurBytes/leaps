# Questions — Module 12: Advanced Concurrency Patterns

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

### Q001: Does `errgroup` have a concurrency limit, or only error aggregation?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README and exercises use `errgroup.WithContext` to fan out goroutines, one per item. The README notes that `errgroup` replaces the WaitGroup + error channel pattern. But does it place any limit on how many goroutines can run concurrently? If I pass 10,000 URLs to `errgroup`, does it spawn 10,000 goroutines simultaneously, or does it have a built-in concurrency limit?

**My current hypothesis:**
I think `errgroup` by default spawns one goroutine per `g.Go(...)` call with no concurrency limit — it's purely about error aggregation and context cancellation, not about bounding parallelism. The solution for bounded concurrency + error propagation is to combine a worker pool (bounded goroutines) with error handling. But I recall seeing something about `errgroup.SetLimit` — I'm not sure if that's a real API or something I'm confusing.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Check pkg.go.dev/golang.org/x/sync/errgroup for SetLimit method_

**Follow-up questions:**
- If `errgroup.SetLimit(n)` exists, how does it interact with `g.Go`? Does it block or return an error when the limit is reached?

---

### Q002: What exactly happens when a context.Value key collision occurs between packages?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The README warns to use "typed unexported keys" like `type ctxKey string` to avoid collisions. What actually happens if two packages both call `context.WithValue(ctx, "requestID", value)`? Is it a runtime panic? A silent overwrite? Or does the second value shadow the first (so `ctx.Value("requestID")` returns the second package's value)?

The module says the collision is a problem, but I want to understand the exact mechanism of what goes wrong — is it a correctness bug (wrong value returned) or a safety bug (panic)?

**My current hypothesis:**
I believe the second `WithValue` creates a new context that wraps the first, and `ctx.Value("requestID")` searches the chain from innermost to outermost, returning the first match. So the second package's value shadows (not overwrites) the first package's value. This is a correctness bug — package A's code that calls `ctx.Value("requestID")` would get package B's value if package B added theirs later in the call stack.

Using `type ctxKey string` per-package makes the key type different even if the string content is the same, because `ctxKey("requestID") != "requestID"` — they are different types and thus different map keys.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_See pkg.go.dev/context "WithValue" docs and Go spec on comparable types_

**Follow-up questions:**
- Does the Go spec define how `context.Value` searches the chain, or is it implementation-defined?

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
