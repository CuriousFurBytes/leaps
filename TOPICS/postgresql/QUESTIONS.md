# PostgreSQL — Questions

> This file tracks big-picture, cross-module questions about PostgreSQL.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand indexes" is less useful than "Why does a GIN index outperform a B-tree index on a JSONB column?"
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

### Q001: When should I choose PostgreSQL over a document database like MongoDB?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
Both PostgreSQL (with JSONB) and MongoDB store JSON-like documents. When would I choose PostgreSQL over MongoDB? What are the concrete tradeoffs in terms of query flexibility, schema enforcement, and operational complexity?

**My current hypothesis:**
PostgreSQL seems better for data that has relationships (foreign keys) and needs strict consistency, but MongoDB might be better for very flexible or deeply nested documents. I'm not sure if this is right or if JSONB changes the equation significantly.

**Answer:**
_Research in progress. Relevant modules: 07 (JSON), 05 (Transactions)._

**Source:**
_To be filled in_

**Follow-up questions:**
- Does JSONB support change over time as PostgreSQL evolves?
- Are there situations where you'd use both in the same system?

---

### Q002: What are the most common production mistakes when using PostgreSQL at scale?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I want to understand the pitfalls before I develop bad habits.
What do experienced practitioners wish they'd known earlier about running PostgreSQL in production?

**My current hypothesis:**
Based on the Module 01 overview, I suspect the most common mistakes involve ignoring VACUUM, forgetting to add indexes, and not thinking about connection pooling. But I haven't confirmed this.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- How do I recognize these mistakes before they cause an outage?
- What monitoring would catch these issues early?

---

### Q003: How does PostgreSQL's MVCC compare to locking in other databases like MySQL/InnoDB?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I keep reading that PostgreSQL and MySQL InnoDB both use MVCC, but they behave differently. What is actually different between their implementations, and does it matter in practice?

**My current hypothesis:**
They feel similar but I think they differ in how they handle transaction IDs and how vacuum/purge works. PostgreSQL seems to require more explicit maintenance (VACUUM) while MySQL handles it more automatically.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Is one more suitable than the other for write-heavy workloads?
- How does transaction ID wraparound affect PostgreSQL but not MySQL?

---

### Q004: When does horizontal sharding make sense versus vertical scaling for PostgreSQL?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
Instagram and others have sharded their PostgreSQL deployments across many machines. How do you know when you've hit the limit of a single Postgres instance, and what are the options for scaling out?

**My current hypothesis:**
I think you should stay on a single instance as long as possible because sharding adds enormous complexity. But I don't know what the actual practical limits of a single Postgres instance are (RAM, CPU, storage, connections).

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- What tools exist for sharding Postgres (Citus, Vitess, etc.)?
- How does table partitioning (Module 10) relate to sharding?

---

### Q005: How does PostgreSQL's query planner decide between an index scan and a sequential scan?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I created an index on a column, but EXPLAIN shows the planner doing a sequential scan anyway. Why would the planner ignore an index I created, and how does it make this decision?

**My current hypothesis:**
I think the planner uses some kind of cost estimate and decides that for small tables or queries that return a large percentage of rows, scanning the whole table is actually faster. But I don't know how it estimates this or what parameters control it.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Can I force the planner to use a specific index for testing?
- What statistics does the planner use and how do I keep them up to date?

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
| 🔴 Unanswered | 4 |
| 🟡 Partial | 1 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **5** |
