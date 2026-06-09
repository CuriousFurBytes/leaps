# Questions — Module 7: Packages and Modules

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

### Q001: Can an unexported type be returned by an exported function?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says exported identifiers start with uppercase and unexported with lowercase. But what happens if an exported function *returns* an unexported type? For example:

```go
package mypackage

type internalResult struct { // unexported type
    Value int
}

func Compute() internalResult { // exported function returning unexported type
    return internalResult{Value: 42}
}
```

Does this compile? Can callers in another package use the returned value, even though they can't name the type `internalResult`? Can they access `.Value` if it's exported?

**My current hypothesis:**
I think this compiles and the caller can use the value — they just can't write the type name explicitly. They'd have to use type inference (`:=`) or an interface. The exported `Value` field would be accessible. This feels like an odd API design choice but I'm not sure if it's valid Go.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Exported_identifiers and try a small example_

**Follow-up questions:**
- Is this considered bad practice even if it compiles?
- Does `go vet` or `golangci-lint` warn about returning unexported types from exported functions?

---

### Q002: What does `// indirect` mean in a go.mod require line?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
After running `go mod tidy`, my `go.mod` contains lines like:

```text
require (
    github.com/rs/zerolog v1.32.0
    github.com/mattn/go-colorable v0.1.13 // indirect
)
```

The `// indirect` comment on `go-colorable` — what does it mean? Is this a dependency I imported directly? One that `zerolog` needs? Do I need to manage it manually?

**My current hypothesis:**
I think `// indirect` means it's a transitive dependency — I don't import it directly, but something I do import requires it. `go mod tidy` adds it explicitly to `go.mod` when the indirect dependency's own `go.mod` doesn't pin a specific version (or in other edge cases I don't fully understand).

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go help mod tidy and go.dev/ref/mod#go-mod-tidy_

**Follow-up questions:**
- Should I ever manually remove `// indirect` lines, or always let `go mod tidy` manage them?
- If the indirect dependency releases a security patch, how do I update it?

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
