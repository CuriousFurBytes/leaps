# QA and Testing — Questions

> This file tracks big-picture, cross-module questions about QA and Testing.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand mocking" is less useful than "When should I use a mock vs. a stub vs. a fake?"
3. **Update status** as you find answers — partial answers count.
4. **Link your answers** to the module or resource where you found the explanation.
5. **Add follow-up questions** — good answers often raise better questions.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Unanswered — needs research |
| 🟡 | Partial — have some understanding but still unclear |
| 🟢 | Answered — well understood |
| ⏸ | Deferred — not urgent; revisit later |

---

## Question Format

```markdown
### Q{{N}}: {{QUESTION_TITLE}}

**Asked:** {{YYYY-MM-DD}}
**Status:** 🔴 Unanswered

**Full question:**
Write the question in full. Include context about what prompted it.

**My current hypothesis:**
What do you think the answer might be, even if you're not sure?

**Answer:**
_To be filled in_

**Source:**
_Where did you find/confirm the answer?_

**Follow-up questions:**
- _Any new questions this answer raised_
```

---

## Questions

### Q001: When does testing slow down development vs. speed it up?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
I keep hearing that testing saves time, but writing tests also takes time. When does investing in tests pay off, and when is it overkill? Are there situations where testing slows a team down permanently?

**My current hypothesis:**
Testing probably pays off when the codebase is large and long-lived, but might be overkill for small scripts or throwaway prototypes. Not sure about the inflection point.

**Answer:**
_Research in progress. See Module 07 (TDD) and Module 11 (QA Strategy) for framework._

**Source:**
_To be filled in_

**Follow-up questions:**
- How do I measure the ROI of testing on an existing project?
- What does "good enough" testing look like for a startup vs. an enterprise?

---

### Q002: What is the most common mistake teams make with automated testing?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I want to understand the pitfalls before developing bad habits. What do experienced QA engineers and developers wish they'd known earlier about automated testing?

**My current hypothesis:**
Based on what I've heard, it might be over-relying on end-to-end tests (slow, flaky) or having tests that test implementation details instead of behavior.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- How do I recognize "testing the implementation" in my own code?
- What does a healthy test suite look like vs. one that's technically high-coverage but still low-value?

---

### Q003: How does QA and Testing relate to type systems and formal verification?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
TypeScript and Rust's type systems catch entire categories of bugs at compile time. Does this reduce the need for unit tests? How do testing and type systems complement each other?

**My current hypothesis:**
Type systems and tests seem to catch different kinds of bugs — types catch structural/type-related bugs, tests catch behavioral/logic bugs. But I'm not sure where the boundary is.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Is there a point at which a sufficiently strong type system makes unit tests redundant?
- What does property-based testing (Hypothesis, fast-check) add beyond example-based tests?

---

_Add new questions above this line. Keep them numbered sequentially._

---

## Resolved Questions Archive

_Move fully answered questions (🟢) here to keep the active list manageable._

_(none yet)_

---

## Question Stats

| Status | Count |
|--------|-------|
| 🔴 Unanswered | 2 |
| 🟡 Partial | 1 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **3** |
