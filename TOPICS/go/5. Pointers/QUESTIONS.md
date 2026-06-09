# Questions — Module 5: Pointers

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

### Q001: Why can't you take the address of a map element?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README states that `&m["key"]` does not compile — you cannot take the address of a map element. The explanation given is that "map values may be relocated when the map grows." But what exactly happens when a map grows? Why would taking an address be dangerous?

For example:
```go
m := map[string]int{"a": 1}
p := &m["a"]   // compile error: cannot take the address of m["a"]
```

**My current hypothesis:**
When a map grows (its load factor exceeds a threshold), Go's runtime copies all entries to a new, larger backing array — similar to how `append` on a slice reallocates. If `p` pointed to `m["a"]`'s location, and the map then reallocated, `p` would now point to freed or reused memory. The Go spec disallows map element addresses to prevent this class of dangling pointer bug.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check go.dev/ref/spec#Address_operators_

**Follow-up questions:**
- Can you take the address of an element in a slice? (`&s[0]`) — I believe yes, because slices don't relocate existing elements (only `append` may allocate a new backing array, but the old array remains).

---

### Q002: Does passing a pointer to a function always cause escape to the heap?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says that variables "escape to the heap" when their address outlives the function. If I pass `&x` to a function, does `x` always escape to the heap? Or is the compiler smart enough to determine that the function doesn't store the pointer and avoid the heap allocation?

For example:
```go
func readValue(p *int) int {
    return *p  // just reads; doesn't store p anywhere
}

x := 42
result := readValue(&x)
```

Does `x` escape in this case, or does the compiler see that `readValue` doesn't leak the pointer and keep `x` on the stack?

**My current hypothesis:**
I think Go's escape analysis is sophisticated enough to determine that `readValue` doesn't store or return the pointer, so `x` does not need to escape to the heap. The analysis is inter-procedural (it looks at what the called function does with the pointer). But if `readValue` were in a different package (compiled separately), the compiler might have to be conservative and escape the pointer to be safe.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — run `go build -gcflags='-m' .` to check empirically_

**Follow-up questions:**
- Does inlining affect escape analysis? (If `readValue` is inlined, the compiler can see the full picture.)

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
