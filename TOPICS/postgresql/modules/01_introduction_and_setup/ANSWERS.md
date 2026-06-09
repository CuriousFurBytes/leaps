# Answers: Module 01 — Introduction and Setup

## Answer Key

### Easy Questions
**Q1:** Any accurate concept from the module, such as relation, SQL statement, transaction, constraint, or query plan.
**Q2:** `psql` is PostgreSQL's interactive command-line client for connecting to a server and running SQL or meta-commands.
**Q3:** Constraints reject invalid data and document invariants near the data.
**Q4:** `SELECT`.
**Q5:** Explicit SQL reduces accidental broad changes, especially missing `WHERE` clauses or wrong-session mistakes.

### Medium Questions
**Q6:** Stored facts are durable data with meaning and rules; displayed values are presentation choices derived from those facts.
**Q7:** Errors identify the violated rule or syntax problem and guide the next correction.
**Q8:** Database rules protect data from every client; application-only validation protects only code paths that remember to call it.
**Q9:** It builds the habit of precise SQL, inspection, and reasoning about durable choices.
**Q10:** Confirm the current database and role, read the statement, use transactions where appropriate, and scope changes with predicates.

### Hard Questions
**Q11:** `SELECT current_database(), current_user;` is a valid answer.
**Q12:** The statement updates every row; add an appropriate `WHERE`, such as `UPDATE users SET email = 'test@example.com' WHERE id = 1;`.
**Q13:** A valid answer includes `CREATE TABLE` with a primary key, `NOT NULL`, `UNIQUE`, `CHECK`, or foreign key constraint.
**Q14:** The insert attempted to store `NULL` in a required column; provide a non-null value or change the schema only if the business rule allows it.

### Expert Questions
**Q15:** Strong answers state a business invariant and use constraints, transactions, types, or locks to protect it.
**Q16:** Strong answers keep durable invariants in PostgreSQL, request-specific behavior in application code, and explain the boundary with examples.

### Bonus Questions
**Bonus 1:** Strong answers connect careful schema/query habits to future indexing, planning, transaction isolation, or operational safety.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
