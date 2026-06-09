# Questions — Module 14: Databases and Persistence

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

### Q001: What happens to an in-flight transaction when the context is cancelled?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README emphasizes passing `r.Context()` to every database call so that context cancellation (client disconnect, server timeout) propagates to the database. But what exactly happens when a context is cancelled while a query is running *inside a transaction*?

Specifically: if I call `tx.ExecContext(ctx, ...)` and `ctx` is cancelled while the query is running, does the database driver:
(a) cancel the in-flight SQL statement and roll back the entire transaction automatically?
(b) cancel the in-flight SQL statement but leave the transaction open for me to roll back?
(c) something else entirely, depending on the driver?

The `defer tx.Rollback()` pattern covers the rollback after an error return — but I'm not sure if the rollback actually reaches the database when the context is already cancelled (you can't cancel the rollback call itself, can you?).

**My current hypothesis:**
I think the database driver cancels the statement and marks the transaction as failed, but the `defer tx.Rollback()` still needs to run to release the connection back to the pool. The rollback call itself probably uses a fresh context or no context. But I haven't verified this.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check the `database/sql` source code and pkg.go.dev/database/sql docs for context cancellation behavior_

**Follow-up questions:**
- Does the answer change between drivers (e.g., SQLite vs PostgreSQL)?
- Is there a way to write a test that exercises this path?

---

### Q002: Does `defer rows.Close()` return the connection to the pool?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says to always `defer rows.Close()` after a successful `QueryContext`. I understand this releases the row cursor. But does `rows.Close()` also return the underlying database connection back to the pool immediately?

The reason I'm asking: if a query returns many rows and I'm iterating slowly, is the connection "checked out" for the entire duration of iteration? If so, a slow consumer with a large result set could starve the pool.

For example:
```go
rows, err := db.QueryContext(ctx, `SELECT * FROM large_table`)
// ... defer rows.Close()
for rows.Next() {
    time.Sleep(100 * time.Millisecond) // simulate slow processing
    // ...
}
```

Is the connection held open for the entire iteration loop?

**My current hypothesis:**
I believe yes — the connection is held for the entire `rows.Next()` iteration because the rows are streamed from the database, not buffered into memory. `rows.Close()` is what releases the connection. This would mean that for large result sets, you should either: (a) fetch all rows into memory quickly and then close, (b) use `LIMIT`/pagination, or (c) accept that a connection is held for the duration.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in — check the database/sql package internals_

**Follow-up questions:**
- Does `sqlx`'s `Select` (which scans all rows into a slice at once) effectively close the rows and return the connection faster than manual iteration?

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
