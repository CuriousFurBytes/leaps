# Questions — Module 01: Introduction to JavaScript

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

### Q001: Why does `typeof null` return "object" if null is a primitive?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The module says `typeof null === "object"` is a "historic bug". But how did it happen?
Was it ever fixable? Why didn't they fix it in ES6 when they made so many other changes?

**My current hypothesis:**
Maybe it had something to do with the original 10-day implementation?
And maybe fixing it would break too many websites that accidentally rely on this behavior?

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Are there other similar "unfixable bugs" in JavaScript?

---

### Q002: When should I use a function declaration versus a function expression versus an arrow function?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The module shows three ways to write functions. In practice, which should I use?
The module says arrow functions don't have their own `this` — when does that matter?

**My current hypothesis:**
Arrow functions seem simpler for small callbacks. Function declarations seem better for named top-level functions because of hoisting. I don't understand the `this` difference yet.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- How does `this` work differently in arrow functions vs regular functions?
- Is there a performance difference?

---

### Q003: What exactly is the difference between null and undefined?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
Both `null` and `undefined` seem to mean "no value". When should I use one vs the other?
Why does JavaScript have both?

**My current hypothesis:**
`undefined` seems to be JavaScript's way of saying "this was never set". `null` seems to be the programmer's way of saying "I intentionally set this to nothing". But I'm not sure if this is right.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Why does `typeof null === "object"` but `typeof undefined === "undefined"`?
- What does a function return if it has no return statement?

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
| 🔴 Unanswered | 3 |
| 🟡 Partial | 0 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **3** |
