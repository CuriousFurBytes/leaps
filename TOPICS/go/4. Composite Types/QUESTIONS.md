# Questions — Module 4: Composite Types

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

### Q001: What happens when two embedded types both have a field with the same name?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module explains that embedding promotes fields from the inner type to the outer type. But what if two different types are embedded in the same struct and both define a field (or method) with the same name? For example:

```go
type A struct{ Name string }
type B struct{ Name string }

type C struct {
    A
    B
}

var c C
c.Name // ???  -- which Name? A.Name or B.Name?
```

Does this compile? Does it panic at runtime? Does Go require explicit disambiguation?

**My current hypothesis:**
I think Go will compile the struct definition but accessing `c.Name` directly will be a compile error due to ambiguity. You would need to use `c.A.Name` or `c.B.Name` to disambiguate. This would be consistent with Go's philosophy of making implicit choices visible.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Selectors and the "Ambiguous selector" section_

**Follow-up questions:**
- Does the same ambiguity rule apply to promoted methods?
- What if only one of the two embedded types defines a field at the top level and the other has it nested deeper — does depth resolve the ambiguity?

---

### Q002: Can a struct with an array field be used as a map key?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module says keys must be comparable, and arrays are comparable (because `==` works on arrays element-by-element). What about a struct that contains an array? For example:

```go
type Key struct {
    ID    [16]byte  // array — comparable
    Label string    // comparable
}

m := map[Key]int{}
k := Key{ID: [16]byte{1, 2, 3}, Label: "test"}
m[k] = 42
```

Is this valid? Does the comparable requirement propagate recursively through struct fields?

**My current hypothesis:**
I believe this is valid — a struct is comparable if and only if all its fields are comparable. Since `[16]byte` is an array (comparable), and `string` is comparable, the struct `Key` should be comparable and usable as a map key. I think `map[[16]byte]int` (with an array directly as the key) is also valid.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Comparison_operators and the definition of "comparable"_

**Follow-up questions:**
- Is there a performance difference between using a struct key vs a string key? (hashing a struct might be slower than hashing a string)
- What about using `[32]byte` as a key (like a SHA-256 hash)? Common in practice?

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
