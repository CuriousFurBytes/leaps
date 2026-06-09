# PostgreSQL — Projects

> Project-based learning cements knowledge in a way that reading and exercises alone cannot.
> Building something real forces you to confront gaps in your understanding and make decisions
> that tutorials never put in front of you.

---

## How to Use This File

1. Choose a project at or slightly above your current level.
2. **Don't use tutorials for your chosen project.** Tutorials are for learning, projects are for applying.
3. Document your attempt using the [Project Attempt Template](#project-attempt-template) at the bottom.
4. When you finish, link the result (repo, demo) in the table in the topic README.

---

## Beginner Projects

_Focus: get comfortable with the core tools and SQL vocabulary._
_Complete at least one before advancing past Phase 1._

### B1: Personal Library Tracker

**Description:** Build a database to track your personal book collection. Include books, authors, genres, reading status (to-read, reading, finished), and ratings. Query it to find books by genre, sort by rating, and find your reading history.

**Concepts Reinforced:**
- CREATE TABLE with appropriate data types (TEXT, INTEGER, DATE, BOOLEAN)
- PRIMARY KEY and FOREIGN KEY constraints
- Basic CRUD operations (INSERT, SELECT, UPDATE, DELETE)
- Simple JOIN to connect books and authors

**Estimated Time:** 3–4 hours

**Starting Point:** Blank psql session; design the schema on paper first.

**Success Criteria:**
- [ ] At least 3 tables with proper foreign key relationships
- [ ] Can query "all books I've finished, sorted by rating"
- [ ] Can add a new book and update its status when you finish reading it
- [ ] Schema enforces that a book's rating is between 1 and 5 (CHECK constraint)
- [ ] The project runs without errors

---

### B2: Employee Directory

**Description:** Model a company's employee directory with departments, employees, and reporting relationships (a manager is also an employee). Practice self-referential foreign keys and hierarchical data.

**Concepts Reinforced:**
- Self-referential foreign key (employee.manager_id references employee.id)
- NULL handling (the CEO has no manager)
- Filtering and sorting with WHERE and ORDER BY
- COUNT and aggregate queries per department

**Estimated Time:** 2–3 hours

**Starting Point:** Blank psql session.

**Success Criteria:**
- [ ] Can query "all employees in a given department with their manager's name"
- [ ] Self-referential FK is correct and enforced
- [ ] NULL manager_id for the top-level employee is intentional and handled correctly

---

### B3: Event RSVP System

**Description:** Build a schema for a simple event management system: events, attendees, and RSVPs. Practice many-to-many relationships via a junction table.

**Concepts Reinforced:**
- Many-to-many via junction table (events ↔ attendees via rsvps)
- UNIQUE constraint on the junction table to prevent duplicate RSVPs
- Aggregate queries: how many people RSVPed to each event?
- TIMESTAMPTZ for event date/time

**Estimated Time:** 2–3 hours

**Starting Point:** Blank psql session.

**Success Criteria:**
- [ ] Junction table has a composite primary key (event_id, attendee_id)
- [ ] Can query "events with more than 10 RSVPs"
- [ ] Duplicate RSVPs are prevented by the database, not application code

---

## Intermediate Projects

_Focus: combine multiple concepts, handle edge cases, write clean SQL._
_Complete at least one before completing Phase 2._

### I1: E-commerce Order Database

**Description:** Model a simplified e-commerce system: customers, products (with inventory), orders, and order line items. Implement a price snapshot on order items (so the price at time of purchase is preserved even if the product price changes later). Add proper indexing for common query patterns.

**Concepts Reinforced:**
- Denormalized price snapshot (a deliberate design decision)
- Multi-table JOINs across 4 tables
- Aggregate queries: revenue per customer, top-selling products
- Index strategy: which columns need indexes?
- EXPLAIN ANALYZE to verify your indexes are used

**Estimated Time:** 5–7 hours

**Starting Point:** Blank database; design the schema on paper first.

**Success Criteria:**
- [ ] Can query "total revenue by month for the last 12 months"
- [ ] Can query "top 10 products by units sold"
- [ ] Indexes are in place for the most common query patterns
- [ ] EXPLAIN ANALYZE confirms indexes are being used for the above queries
- [ ] Code is clean, readable, and commented

---

### I2: Forum / Discussion Board Schema

**Description:** Design a threaded discussion forum: users, categories, threads, posts, and a voting/upvote system. Implement a query that retrieves a thread's top-level posts with their reply counts and net vote scores, sorted by score.

**Concepts Reinforced:**
- Self-referential relationship (posts can have parent posts for threading)
- Aggregate with multiple LEFT JOINs (vote counts, reply counts)
- Window functions: rank posts by score within a thread
- CHECK constraint on vote values (+1 or -1 only)

**Estimated Time:** 5–7 hours

**Starting Point:** Blank database.

**Success Criteria:**
- [ ] Can retrieve a full thread with post scores in a single query
- [ ] Votes are constrained to +1 or -1 at the database level
- [ ] Reply count and vote score are computed in SQL, not application code

---

### I3: Full-Text Search Blog

**Description:** Build a blog post schema with full-text search capability. Store posts with title, body, tags (as a PostgreSQL array), and publish date. Implement search that ranks results by relevance and supports filtering by tag and date range.

**Concepts Reinforced:**
- tsvector/tsquery full-text search (Module 07 preview)
- PostgreSQL array type for tags
- GIN index for full-text search
- Ranking search results with ts_rank
- Combined filter (FTS + date range + tag filter)

**Estimated Time:** 4–6 hours

**Starting Point:** Blank database; populate with at least 20 sample posts.

**Success Criteria:**
- [ ] Full-text search returns ranked results in under 10ms for a 10,000-post table
- [ ] Can filter by tag using the array `@>` operator
- [ ] GIN index is present and EXPLAIN confirms it is used for FTS queries

---

## Advanced Projects

_Focus: tackle realistic, open-ended problems. No hand-holding._
_Complete at least one to reach Applied Practitioner status._

### A1: Multi-Tenant SaaS Schema (Preview)

**Description:** Design and implement a multi-tenant database schema for a project management tool (think: a simplified Jira or Trello). Multiple "organizations" share the same database but must be completely isolated from each other. Use PostgreSQL's row-level security (RLS) to enforce isolation at the database level.

**Why This Is Hard:**
You need to design for isolation without simply giving each tenant their own database. Row-level security policies must be airtight — a mistake here is a data breach. You also need to think about performance: queries must be efficient even with an RLS policy filtering every read.

**Concepts Reinforced:**
- Row-level security (RLS) policies
- Schema design for multi-tenancy
- Performance implications of RLS (indexes must include tenant_id)
- Role management (application role vs. superuser)
- EXPLAIN ANALYZE with RLS enabled

**Estimated Time:** 8–12 hours

**Starting Point:** Blank database; sketch the schema and RLS policies on paper first.

**Success Criteria:**
- [ ] Organization A cannot see Organization B's data — enforce this with RLS, not application code
- [ ] All queries include tenant_id in index lookups (verify with EXPLAIN ANALYZE)
- [ ] Application role cannot disable RLS (BYPASSRLS is not granted)
- [ ] You can explain every design decision you made

---

### A2: Analytics Query Engine

**Description:** Load a medium-sized public dataset (e.g., NYC Taxi trips, available from nyc.gov data catalog) into PostgreSQL and build a set of analytical queries using window functions, CTEs, and proper indexing. Optimize until the slowest query runs in under 1 second on a 1-million-row table.

**Why This Is Hard:** You have to design indexes that actually help analytical queries (not just point lookups), understand when partial indexes help, and tune memory settings (work_mem) for sort-heavy queries.

**Concepts Reinforced:**
- Window functions for rolling aggregates and rankings
- CTEs for multi-step analytical pipelines
- Partial indexes for filtered aggregations
- work_mem tuning for sort operations
- COPY command for bulk loading

**Estimated Time:** 6–10 hours

**Success Criteria:**
- [ ] All analytical queries run in under 1 second on a 1M-row table
- [ ] EXPLAIN ANALYZE plans are annotated with your interpretation
- [ ] work_mem setting justification is documented

---

## Expert / Capstone Projects

_Focus: synthesize everything. Build something you're proud to show others._
_Complete one to earn Topic Mastery status._

### E1: Production-Grade Multi-Tenant SaaS Database

**Description:** Design, implement, and optimize a complete production-ready multi-tenant SaaS database for a hypothetical task management application (organizations, users, projects, tasks, comments, file attachments metadata, activity logs). Include: row-level security, table partitioning for activity logs, full-text search on tasks and comments, proper role architecture, replication setup documentation, VACUUM configuration, and a backup/restore procedure.

**Why This Is a Capstone:**
This project requires mastery of all major topic areas. You cannot complete it with gaps — they will surface quickly. Expect to revisit earlier modules during the build.

**Core Requirements:**
- [ ] Uses concepts from at least 8 different modules
- [ ] Is non-trivial in scope (not achievable in a single sitting)
- [ ] Is documented clearly enough that someone else could understand it
- [ ] Includes a write-up explaining your design decisions and what you learned
- [ ] Row-level security isolates all tenant data at the database level
- [ ] Activity log table is partitioned by month (RANGE partitioning)
- [ ] Full-text search is implemented on task titles and descriptions
- [ ] A replication topology is documented (even if not actually deployed)
- [ ] VACUUM/autovacuum configuration is tuned and justified

**Estimated Time:** 15–20 hours

**Extension Ideas (if you want more challenge):**
- Implement logical replication to a reporting replica with a different schema
- Add TimescaleDB for time-series analytics on activity logs
- Implement a connection pooler (PgBouncer) configuration and document it

> [!NOTE]
> The final module of this topic (Module 12) is a dedicated **Capstone Project** module that walks you
> through building this for real. It gives you a brief, milestones, and a **Help / Getting
> Unstuck** section with staged hints — but it deliberately does **not** hand you a finished
> solution. The help is there so you can get past a blocker and keep going on your own, not so
> you can skip the build. Struggling productively *is* the learning here.

---

## Project Attempt Template

When you attempt a project, create a folder in this topic's directory and copy this template:

```markdown
# Project: {{PROJECT_NAME}}

**Difficulty:** Beginner / Intermediate / Advanced / Expert
**Started:** {{YYYY-MM-DD}}
**Completed:** {{YYYY-MM-DD}} (or "In progress")
**Time Spent:** {{HOURS}} hours

## What I Built

{{DESCRIPTION_OF_WHAT_YOU_ACTUALLY_BUILT}}

## Link / Location

{{LINK_TO_REPO_OR_FILE}}

## What I Learned

- {{LEARNING_1}}
- {{LEARNING_2}}
- {{LEARNING_3}}

## What Was Hard

{{WHAT_WAS_CHALLENGING_AND_HOW_YOU_SOLVED_IT}}

## What I'd Do Differently

{{HONEST_RETROSPECTIVE}}

## Concepts Used

- [[modules/01_introduction]] — how you used it
- [[modules/04_indexes-and-performance]] — how you used it

## Score / Self-Assessment

On a scale of 1–5, how well do I think I executed this project? {{SCORE}}/5

Justification: {{JUSTIFICATION}}
```
