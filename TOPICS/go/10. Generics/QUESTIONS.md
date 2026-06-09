# Questions — Module 10: Generics

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

### Q001: Can a constraint combine method elements and type elements?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
An interface can contain method elements (like `String() string`) and it can contain type elements (like `~int | ~float64`). Can a constraint contain *both* at the same time? For example:

```go
type StringableNumber interface {
    ~int | ~float64
    String() string
}
```

If this is valid, what does it mean at the call site? Does `T` have to be a type that is (a) an int or float64 *and* (b) also has a `String()` method? And is there any concrete type that would satisfy both?

**My current hypothesis:**
I think the syntax is valid — the type set is the intersection of the type-element set and the method-element set. In practice, no predeclared type like `int` or `float64` has a `String()` method, so only a user-defined named type (e.g., `type MyInt int` with `func (m MyInt) String() string { ... }`) would satisfy this constraint. But I haven't verified this or confirmed whether such a constraint is actually useful.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Check go.dev/ref/spec#Interface_types and the Go 1.18 blog post_

**Follow-up questions:**
- If no predeclared type satisfies the combined constraint, is this pattern ever actually useful, or is it a footgun?
- What does the compiler error look like when a type satisfies the type elements but not the method elements?

---

### Q002: What does `reflect.TypeOf` return for a generic type parameter?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
If I have a generic function `func Inspect[T any](v T)` and I call `reflect.TypeOf(v)` inside it, does the result reflect the concrete type argument (`int`, `string`, etc.) or the type parameter (`T`)?

For example:
```go
func Inspect[T any](v T) {
    fmt.Println(reflect.TypeOf(v))
}

Inspect(42)      // prints "int"?
Inspect("hello") // prints "string"?
```

**My current hypothesis:**
I believe `reflect.TypeOf(v)` would return the concrete type (`int`, `string`, etc.) because the type parameter is resolved at compile time. At runtime, `v` holds a concrete value, and `reflect` operates on runtime values — it wouldn't know or care that the function was declared with a type parameter.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Write a small test program to verify, or check the reflect package docs_

**Follow-up questions:**
- Does the answer change if the constraint is a non-empty interface (method set constraint) vs `any`?
- Is there a way to get the *static* type parameter T's name (not the concrete type) at runtime?

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
