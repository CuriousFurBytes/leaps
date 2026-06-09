# Computer Networks — Questions

> This file tracks big-picture, cross-module questions about Computer Networks.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand TCP" is less useful than "Why does TCP use a 3-way handshake instead of 2?"
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

### Q001: Why does TCP use a 3-way handshake instead of a 2-way handshake?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
It seems like two messages (SYN → SYN-ACK) should be enough to establish a connection.
Why does TCP need a third message (ACK)? What problem does it solve?

**My current hypothesis:**
Maybe it has something to do with both sides needing to confirm the other side's sequence number?

**Answer:**
_To be filled in — see Module 04 for a detailed explanation._

**Source:**
_To be filled in_

**Follow-up questions:**
- Is there a theoretical minimum number of messages needed to establish a reliable connection?

---

### Q002: What are the most common real-world networking mistakes that engineers make?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I want to understand the pitfalls before I develop bad habits.
What do experienced network engineers wish they'd known earlier? Specifically around subnetting, security, and troubleshooting.

**My current hypothesis:**
Based on Module 01, I suspect the most common mistakes involve forgetting about NAT traversal issues, misconfiguring firewalls, and poor subnet planning.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- How do I recognize these mistakes in production?
- What does a well-architected network look like vs. one that was grown organically?

---

### Q003: How does networking relate to security?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I keep seeing Computer Networks and [[pentesting-security]] mentioned together.
Are they complementary, overlapping, or competing approaches?
When do I need both vs. just one?

**My current hypothesis:**
Networks is the foundation and security is built on top — you can't secure what you don't understand.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Is there networking content I should study before starting [[pentesting-security]]?
- Which modules here are most directly useful for security work?

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
