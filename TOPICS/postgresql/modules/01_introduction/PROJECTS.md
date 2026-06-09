# Projects — Module 01: Introduction to PostgreSQL

> Module-level project ideas using only the concepts from this module.
> For the full project list spanning all difficulty levels, see [../../PROJECTS.md](../../PROJECTS.md).

---

## Module 01 Projects

These projects use only what was covered in Module 01: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, basic data types, and constraints.

---

### Project 1.A: Personal Catalog

**Description:** Build a database for something you personally care about cataloging — movies you've watched, books you've read, music albums, video games, recipes, travel destinations, or anything else. The key constraint: design the schema yourself without referencing any template.

**Why this project:** Schema design skill comes from making real decisions, not filling in templates. Designing something you actually care about forces genuine thought about what data matters and what relationships exist.

**Requirements:**
- [ ] At least one table with 6+ columns using varied data types (text, numeric, boolean, date/timestamp, nullable and non-nullable)
- [ ] At least one CHECK constraint enforcing a business rule (e.g., rating between 1 and 5)
- [ ] At least 10 rows of real data inserted
- [ ] Three meaningful SELECT queries: one with WHERE, one with ORDER BY, one with basic aggregate (COUNT or AVG)
- [ ] Document: what is the PRIMARY KEY and why did you choose that column?

**Time estimate:** 2–3 hours

---

### Project 1.B: Contact Book

**Description:** A contact management database. People have names, email addresses, phone numbers (optional), categories (friend/family/work/other), and notes. Some contacts may have multiple phone numbers.

**Challenge question to solve on your own:** How do you handle a contact having multiple phone numbers? (Hint: think about what you learned in Exercise 5 about junction tables.)

**Requirements:**
- [ ] At minimum: a `contacts` table and a `phone_numbers` table
- [ ] Foreign key from phone_numbers to contacts
- [ ] A query that returns all phone numbers for a specific contact
- [ ] A query that finds all contacts with no phone number (hint: use IS NULL or a LEFT JOIN — preview of Module 03)
- [ ] 5+ contacts with varied data (some with multiple phones, some with none)

**Time estimate:** 2–3 hours

---

_See [../../PROJECTS.md](../../PROJECTS.md) for larger projects that span multiple modules._
