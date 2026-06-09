# Questions — Module 01: Introduction to PostgreSQL

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

## Questions

### Q001: Why does PostgreSQL use the term "relation" instead of "table"?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
The module README uses both "relation" and "table." Are they exactly the same thing? When would I use one term vs. the other?

**My current hypothesis:**
I think "relation" is the mathematical/theoretical term from Codd's paper, and "table" is the everyday practical term for the same thing. They seem interchangeable in practice.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does the PostgreSQL documentation consistently use "relation" or "table"?

---

### Q002: What exactly happens when I type `\dt` in psql vs. when I type a SQL statement?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The module mentions that psql meta-commands (starting with `\`) are "processed by psql itself and never sent to the server." So what does `\dt` actually do? Does it run a SQL query behind the scenes? How does it know what tables exist?

**My current hypothesis:**
I think `\dt` probably runs a SQL query against PostgreSQL's internal system tables (like `pg_class` or `information_schema.tables`) but psql handles this automatically so I don't have to write the query myself.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Can I see the SQL that psql uses for `\dt`? (I think you can with `\set ECHO_HIDDEN on`)

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
