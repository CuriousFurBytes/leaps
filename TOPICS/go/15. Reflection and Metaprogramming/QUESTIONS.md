# Questions — Module 15: Reflection and Metaprogramming

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

### Q001: Can you use reflection to send and receive on a channel?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module covers reflection for structs and scalars, but channels are also first-class values in Go. `reflect.Value` has a `Kind()` of `reflect.Chan`. Does the reflect package have `Send` and `Recv` methods analogous to `<-` channel operations? And if so, do they block in the same way?

**My current hypothesis:**
I think `reflect.Value` does have `Send` and `Recv` methods since the package tries to expose all Go operations reflectively. If they exist, they should block just like real channel operations — otherwise the semantics would be inconsistent with the Laws of Reflection. But I haven't verified this.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check pkg.go.dev/reflect and look for Send/Recv/TrySend/TryRecv_

**Follow-up questions:**
- Can you use `reflect.Value.Select` to implement a runtime-constructed `select` statement?

---

### Q002: Does the Go compiler ever optimize or inline reflect calls?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module shows that reflection is 10–15× slower than direct field access. But the Go compiler is sophisticated — it inlines functions, escape-analyzes allocations, and devirtualizes interface calls in many cases. Does it ever optimize away or partially inline `reflect.ValueOf`, `reflect.Value.Field`, or `reflect.Value.SetInt` calls when the types are statically knowable?

**My current hypothesis:**
I doubt it. The reflect package is designed for runtime use, and the compiler would need escape analysis plus call-graph analysis across the reflect package boundary to prove the types are constant — which seems impractical. The 10–15× overhead is probably irreducible for most reflect usage. But the answer might be different in Go 1.21+ with profile-guided optimization (PGO).

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check release notes for pgo or reflect; try `go build -gcflags="-m"` to check escape analysis on a reflect-heavy file_

**Follow-up questions:**
- Does PGO (introduced in Go 1.20) help with reflect overhead at all?
- How does the overhead compare when using `reflect.Value.Pointer()` to get a raw pointer and do unsafe arithmetic?

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
