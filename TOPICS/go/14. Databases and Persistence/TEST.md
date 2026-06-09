# Test — Module 14: Databases and Persistence

**Topic:** [[go]]
**Module:** [[go/14. Databases and Persistence]]

---

## Before You Begin

> [!WARNING]
> **Do not look at ANSWERS.md or your notes during the test.**
> The purpose of this test is to surface what you truly know vs. what you think you know.
> An inflated score is worthless. An honest score shows you exactly where to focus next.

**Instructions:**
1. Close all notes, the module README, and any reference materials.
2. Set a timer. Note your start time below.
3. Attempt every question — partial credit exists.
4. After finishing, grade yourself using ANSWERS.md.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Start time:** ___________
**End time:** ___________
**Total time:** ___________

---

## Scoring Table

| Section | Question Type | Points Each | # Questions | Max Points |
|---------|--------------|-------------|-------------|------------|
| Section 1: Recall | Easy | 1 pt | 5 | 5 pts |
| Section 2: Conceptual | Medium | 2 pts | 3 | 6 pts |
| Section 3: Applied | Hard | 3 pts | 2 | 6 pts |
| Section 4: Scenario | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** Is `sql.DB` a single database connection? Explain what it actually is, and what that means for concurrent use.

> _Your answer:_

---

**1.2** `sql.Open` returns no error and `err == nil`. Does this mean the database is reachable and accepting connections? Why or why not? What should you call to actually verify connectivity?

> _Your answer:_

---

**1.3** List the four steps in the correct order for iterating over rows returned by `db.QueryContext`. What happens if you skip step 4?

> _Your answer:_

---

**1.4** What is the placeholder syntax for parameterized queries in SQLite/MySQL drivers? How does it differ for PostgreSQL drivers, and why does it matter?

> _Your answer:_

---

**1.5** Name the two sentinel errors from `database/sql` that you must check for by name (using `errors.Is`). When does each occur?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain the `defer tx.Rollback()` safety pattern for transactions. Specifically: why is `Rollback` placed in a `defer` statement immediately after `BeginTx`? What happens to the deferred `Rollback` call after `tx.Commit()` succeeds? Walk through both the success path and the error path.

> _Your answer:_

---

**2.2** A colleague says: "I need to handle NULLable columns in my query result, so I'll just scan them into `string` variables and check if the string is empty." Is this approach correct? If not, explain what will happen and what the correct approach is.

> _Your answer:_

---

**2.3** Explain the repository pattern and why it improves testability. What is the role of the interface (`UserStore`), the concrete implementation (`SQLUserStore`), and the fake implementation (`FakeUserStore`)? Specifically: what does a handler depend on, and how does this enable testing without a database?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a Go function `getUsersByDomain(ctx context.Context, db *sql.DB, domain string) ([]string, error)` that:
- Queries `SELECT email FROM users WHERE email LIKE ?` with a pattern `"%@" + domain`
- Returns all matching email addresses as a `[]string`
- Uses the complete rows iteration protocol (all four steps)
- Wraps errors with context using `fmt.Errorf`

> _Your answer:_

---

**3.2** Write a Go function `createUserWithProfile(ctx context.Context, db *sql.DB, name, email, bio string) (int64, error)` that:
- Starts a transaction
- Inserts a row into `users (name, email)` and retrieves the new ID via `LastInsertId`
- Inserts a row into `profiles (user_id, bio)` using the retrieved ID
- Returns the user ID on success
- Uses the `defer tx.Rollback()` safety pattern

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A developer writes the following login function:

```go
func login(ctx context.Context, db *sql.DB, username, password string) (int64, error) {
    query := fmt.Sprintf(
        "SELECT id FROM users WHERE username='%s' AND password_hash='%s'",
        username, password,
    )
    var id int64
    err := db.QueryRowContext(ctx, query).Scan(&id)
    if err != nil {
        return 0, err
    }
    return id, nil
}
```

Identify:

a) What specific security vulnerability does this code contain? Name it and explain precisely how an attacker would exploit it. Show the exact input that would bypass the password check.

b) Why does this vulnerability exist at the code level? What property of string concatenation makes it dangerous here?

c) Rewrite `login` correctly, fixing the vulnerability. Your fix must use the standard `database/sql` mechanism — not a string escaping function.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "For a professional Go service, you should always use `database/sql` directly and avoid ORMs like GORM entirely." Do you agree or disagree with this statement? Justify your position by comparing `database/sql`, `sqlx`, `sqlc`, and GORM across at least two meaningful dimensions (e.g., type safety, query visibility, prototyping speed, debugging complexity). Name at least one situation where each tool is the right choice.

Consider tradeoffs honestly — an answer that only advocates one tool without acknowledging its weaknesses will receive partial credit.

> _Your answer (aim for 4–8 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Connection pool exhaustion is a production incident pattern. Describe what happens step-by-step when `db.SetMaxOpenConns(5)` is set and 10 concurrent goroutines all call `db.QueryContext` at the same time. What does the 6th goroutine experience? What role does context cancellation play in resolving a pool exhaustion situation? Write a short Go program (or pseudocode) that demonstrates pool exhaustion and shows context cancellation freeing a waiting goroutine.

Bonus points for also explaining what `SetConnMaxIdleTime` and `SetConnMaxLifetime` do to the pool over time and why they prevent a different class of production issues.

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the next module?**
> _Your reflection:_

**What score did I get? Do I feel it accurately reflects my understanding?**
> _Your reflection:_

---

## Grading Record

_Append a new row each time you take this test. Do not overwrite previous attempts._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
