# GraphQL and REST API Design — Questions

> This file tracks big-picture, cross-module questions about GraphQL and REST API Design.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand REST" is less useful than "Why does REST require statelessness if HTTP cookies exist?"
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

### Q001: When should I choose REST over GraphQL, and vice versa?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
Both REST and GraphQL can build APIs for the same domain. How do I decide which to use
for a new project? Are there domains where one is clearly better?

**My current hypothesis:**
GraphQL seems better for complex, nested data (like social graphs or e-commerce with
many related entities). REST seems better for simple CRUD resources and when many clients
(including non-JS clients) need to consume the API.

**Answer:**
_Research in progress. See Module 01 for a first-look comparison, Module 05 for GraphQL fundamentals._

**Source:**
_To be filled in_

**Follow-up questions:**
- Can you use both in the same system? (hint: yes — see Module 10)
- How does team size affect the decision?

---

### Q002: What are the most common real-world mistakes when designing REST APIs?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I want to understand the pitfalls before I develop bad habits.
What do experienced API designers wish they'd known earlier?

**My current hypothesis:**
Based on Module 01, I suspect the most common mistakes involve treating REST as just
CRUD-over-HTTP, not thinking about versioning until it's too late, and overusing POST.

**Answer:**
_To be filled in — see Module 02 (REST Fundamentals) and Module 03 (REST Advanced)_

**Source:**
_To be filled in_

**Follow-up questions:**
- How do I recognize these mistakes when I'm reviewing someone else's API design?
- What does correct versioning look like vs. common bad patterns?

---

### Q003: How does GraphQL relate to REST — are they competing or complementary?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I keep seeing REST and GraphQL mentioned together. Are they competing approaches
for the same problem, or do they solve different problems? When do I need both?

**My current hypothesis:**
They feel like competing approaches because both sit on HTTP and return JSON,
but GraphQL's query model feels fundamentally different from REST's resource model.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Can a GraphQL layer sit on top of REST microservices?
- What does a system that uses both REST and GraphQL look like in practice?

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
