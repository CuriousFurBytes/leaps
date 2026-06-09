# Test — Module 01: Introduction to PostgreSQL

**Topic:** [[postgresql]]
**Module:** [[modules/01_introduction]]

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

**1.1** Define **NULL** in the context of a PostgreSQL database column. What does it represent, and how is it different from zero or an empty string?

> _Your answer:_

---

**1.2** What is the difference between `TIMESTAMP` and `TIMESTAMPTZ` in PostgreSQL, and which should you generally use?

> _Your answer:_

---

**1.3** List three psql meta-commands and briefly state what each one does.

> _Your answer:_

---

**1.4** What does `SERIAL` do in a `CREATE TABLE` statement? What are the two things it sets up automatically?

> _Your answer:_

---

**1.5** What is the difference between **DDL** and **DML**? Give one example of each.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why SQL is described as a **declarative** language. How is this different from an imperative (procedural) approach to querying data? Why is this distinction important?

> _Your answer:_

---

**2.2** A colleague says: "I'll use `WHERE email = NULL` to find users with no email address." Is this correct? If not, what is the accurate approach, and why does the mistake arise?

> _Your answer:_

---

**2.3** Compare and contrast `TEXT` and `VARCHAR(n)` in PostgreSQL. Under what circumstances would you choose one over the other? Is there a performance difference?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete `CREATE TABLE` statement for a `students` table with the following requirements:
- Auto-incrementing 64-bit integer primary key
- First name and last name (both required, no length limit)
- Email address (required, must be unique)
- Enrollment date (date only, defaults to today)
- GPA as a decimal (optional; if provided, must be between 0.0 and 4.0)
- Active status boolean that defaults to true and is required

Show your work.

> _Your answer:_

---

**3.2** Given a `products` table with columns `id`, `name`, `price`, `category`, and `in_stock`, write the SQL to:

(a) Insert a new product: "Mechanical Keyboard", category "Electronics", price 129.99, in stock.

(b) Update all products in the "Electronics" category to have a 10% price increase.

(c) Delete all products that are not in stock AND have a price under $5.00.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** The following SQL is supposed to delete only the user with email "deleted@example.com" from a `users` table, but a developer is worried it might do something else:

```sql
DELETE FROM users
WHERE email = 'deleted@example.com'
```

Wait — on second look, the developer's actual code in production is this:

```sql
DELETE FROM users;
```

The developer ran the above query without realizing their WHERE clause was accidentally removed.

Identify:

a) What did the query `DELETE FROM users;` actually do?

b) Why did this happen (what is the SQL rule that caused this)?

c) What practice or tool would have prevented this mistake?

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** Why did Edgar Codd's relational model represent such a significant advance over earlier navigational databases? What specific problem did it solve, and how does PostgreSQL embody that solution today?

Consider at least two perspectives (e.g., the programmer's perspective, the data administrator's perspective, the long-term maintainability perspective) in your answer.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** The `RETURNING` clause in PostgreSQL allows `INSERT`, `UPDATE`, and `DELETE` statements to return data about the rows they affected. Write an example showing how you would use `RETURNING` to:

(a) Get the auto-generated `id` after inserting a new user.

(b) Confirm the new values after updating a row.

Then explain: what practical problem does `RETURNING` solve that would otherwise require a second round-trip to the database?

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
