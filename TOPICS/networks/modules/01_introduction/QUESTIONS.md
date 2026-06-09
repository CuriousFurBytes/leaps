# Questions — Module 01: Introduction to Computer Networks

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

### Q001: Why does the OSI model have 7 layers instead of 4 (like TCP/IP)?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
The TCP/IP model collapses Session, Presentation, and Application into one layer. Why does OSI separate them? Do those distinctions matter in practice?

**My current hypothesis:**
OSI was designed as an idealized model before the internet existed. TCP/IP was designed pragmatically to solve a real problem. The distinctions might matter theoretically but not practically.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Are there protocols that specifically use the Session or Presentation layer as distinct from Application?

---

### Q002: How does the router know which interface to send a packet out of?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The README explains that routers forward packets based on destination IP, but how? What data structure does a router maintain, and how is it populated?

**My current hypothesis:**
There must be a table of "for this destination range, use this interface." But how does the table get populated? Does someone manually configure it, or is there an automatic mechanism?

**Answer:**
_To be filled in — see Module 03 (routing basics) and Module 06 (routing protocols)._

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- What happens if the router has no matching route?
- How do routers on the internet discover routes to millions of destinations?

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
| 🔴 Unanswered | 1 |
| 🟡 Partial | 1 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **2** |
