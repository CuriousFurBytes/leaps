# Resources — Module 01: Introduction to PostgreSQL

> Resources listed here are specific to **this module's content** (relational model, installation, psql, basic CRUD).
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

**[PostgreSQL Documentation — Tutorial](https://www.postgresql.org/docs/current/tutorial.html)** — PostgreSQL Global Development Group

The official tutorial is the single best starting point. It covers installation, SQL basics, advanced features, and the psql client in a structured progression. Chapters 1–4 are directly relevant to this module. The documentation is authoritative, accurate, and kept up to date with each major release.

---

## Official Documentation

- **[Getting Started — PostgreSQL Docs](https://www.postgresql.org/docs/current/tutorial-start.html)** — Installation and first connection; exact for Module 01 content
- **[SQL Syntax — PostgreSQL Docs](https://www.postgresql.org/docs/current/sql-syntax.html)** — Comprehensive reference for SQL syntax including NULL handling and data types
- **[psql Reference — PostgreSQL Docs](https://www.postgresql.org/docs/current/app-psql.html)** — Complete list of psql meta-commands and options
- **[Data Types — PostgreSQL Docs](https://www.postgresql.org/docs/current/datatype.html)** — Full reference for all PostgreSQL data types; directly relevant to choosing the right type

---

## Relevant Book Chapters

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| PostgreSQL: Up and Running (Obe & Hsu) | Ch. 1–2 | Introduction and basic querying; beginner-friendly |
| The Art of PostgreSQL (Fontaine) | Ch. 1 | Relational model motivation; excellent prose |
| Practical SQL (DeBarros) | Ch. 1–3 | Hands-on introduction via data analysis examples |

---

## Videos

- **[Database Systems — CMU 15-445 Lecture 1](https://www.youtube.com/watch?v=oeYBdghaIjc)** (~80 min) — Andy Pavlo; excellent introduction to the relational model and why it matters historically
- **[SQL Tutorial for Beginners](https://www.youtube.com/watch?v=HXV3zeQKqGY)** (~4 hrs) — freeCodeCamp channel; comprehensive SQL basics using PostgreSQL

---

## Practice Sites

- **[SQLZoo](https://sqlzoo.net/)** — Interactive SQL exercises directly in the browser; good for additional SELECT practice
- **[pgexercises.com](https://pgexercises.com/)** — PostgreSQL-specific exercises with a real Postgres backend; highly recommended for more practice after this module

---

## Related Modules in This Topic

| Module | Relationship |
|--------|-------------|
| [[modules/02_data-types-and-schema]] (Module 02: Data Types and Schema Design) | Directly extends this module; covers the type system and constraints in much greater depth |
| [[modules/03_querying]] (Module 03: Querying — SELECT Mastery) | Builds on basic SELECT; covers JOINs, GROUP BY, window functions |
| [[modules/05_transactions-and-concurrency]] (Module 05: Transactions and Concurrency) | Covers transactions and ACID — the BEGIN/COMMIT pattern introduced here |

---

## Related Modules in Other Topics

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[django-fastapi-flask]] | ORM and database integration | Django's ORM generates SQL like the queries in this module; understanding the SQL helps debug ORM behavior |
| [[async-python]] | asyncpg and database drivers | asyncpg executes raw SQL against PostgreSQL; the SQL you learned here is what you'll write |

---

## Resources to Evaluate

- [ ] "Introduction to Databases" on Stanford Online (Lagunita) — needs verification of current availability
- [ ] PostgreSQL Tutorial at https://www.postgresqltutorial.com/ — excellent site; verify specific module 1 exercises
