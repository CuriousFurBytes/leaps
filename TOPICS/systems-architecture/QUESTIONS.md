# Systems Architecture — Questions

> This file tracks big-picture, cross-module questions about Systems Architecture.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand X" is less useful than "Why does X behave Y when Z?"
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

### Q001: When should I choose microservices over a monolith?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
Everyone says microservices are the modern way to build, but I keep reading about teams going back to monoliths. What are the actual criteria for choosing one over the other? Is there a framework for making this decision?

**My current hypothesis:**
Microservices seem better for large teams and high scale, but monoliths seem better for small teams and early-stage products. I'm not sure if this is the full picture.

**Answer:**
_Research in progress. See Module 01 and Module 04 for the trade-off framework._

**Source:**
_To be filled in_

**Follow-up questions:**
- What is a "distributed monolith" and why is it considered the worst of both worlds?
- At what team size does the coordination overhead of microservices start to pay off?

---

### Q002: What are the most common mistakes teams make when adopting distributed systems?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I want to understand the pitfalls before I develop bad habits or make expensive architectural mistakes. What do experienced architects wish they'd known earlier?

**My current hypothesis:**
Based on the topic overview, I suspect the most common mistakes involve premature decomposition and underestimating the complexity of distributed transactions, but I haven't confirmed this.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- How do I recognize a "distributed monolith" when I see one?
- What does good service decomposition actually look like in practice?

---

### Q003: How does the CAP theorem relate to the databases I already use?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I use PostgreSQL daily. I've heard of MongoDB and Cassandra. The quick reference says they all sit differently in CAP space. What does this mean practically — when would I actually see consistency vs. availability trade-offs in a real application?

**My current hypothesis:**
I think CAP is more of a theoretical construct and in practice databases try to give you everything most of the time. The trade-offs only show up during failures.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Is the CAP theorem still relevant now that we have things like Google Spanner?
- What is the PACELC model and how does it extend CAP?

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
