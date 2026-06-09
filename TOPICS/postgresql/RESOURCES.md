# PostgreSQL — Resources

> [!WARNING]
> **Verified resources only.** Every entry in this file must be something you have
> personally confirmed exists, is accessible, and is genuinely useful.
> Do not add resources based on hearsay, AI suggestions, or titles that "sound right."
> A short list of excellent resources beats a long list of unverified ones.

---

## Official Documentation

- **[PostgreSQL Documentation](https://www.postgresql.org/docs/current/)** — The primary reference. Comprehensive, accurate, and searchable. Start here when you have a specific question about any feature.
- **[PostgreSQL Release Notes](https://www.postgresql.org/docs/release/)** — Track changes across major versions; understand what changed and when.
- **[PostgreSQL SQL Commands Reference](https://www.postgresql.org/docs/current/sql-commands.html)** — The canonical reference for every SQL statement PostgreSQL supports.

---

## Books

| Title | Author | Level | Format | Notes |
|-------|--------|-------|--------|-------|
| The Art of PostgreSQL | Dimitri Fontaine | Intermediate–Advanced | Print/eBook | Covers real-world SQL patterns; excellent on CTEs, window functions, and application-database integration. Verify current edition URL at [theartofpostgresql.com](https://theartofpostgresql.com) |
| PostgreSQL: Up and Running (3rd ed.) | Regina Obe & Leo Hsu | Beginner–Intermediate | Print/eBook (O'Reilly) | Good survey of the full feature set; strong chapters on PostGIS and extensions |
| PostgreSQL High Performance Cookbook | Chitij Chauhan & Dhruv Mehta | Advanced | Print/eBook (Packt) | Verify current edition — covers tuning, replication, and partitioning in depth |
| [Verify: "The Internals of PostgreSQL" — confirm URL] | Hironobu Suzuki | Expert | Free online | Deep dive into Postgres internals: heap files, WAL, MVCC, and the executor |

---

## Online Courses

| Course | Platform | Level | Free? | Notes |
|--------|----------|-------|-------|-------|
| [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) | postgresqltutorial.com | Beginner | Yes | Well-structured series covering basics through intermediate; good for following along with Module 01–03 |
| [Learn PostgreSQL](https://www.learnpostgresql.com) | learnpostgresql.com | Beginner | Verify | Covers installation through intermediate queries |
| [Practical SQL](https://nostarch.com/practical-sql-2nd-edition) | No Starch Press | Beginner–Intermediate | No (book) | Anthony DeBarros; good for data analysts learning SQL via Postgres |

---

## Video Resources

| Title / Channel | URL | Type | Level | Notes |
|-----------------|-----|------|-------|-------|
| Hussein Nasser — PostgreSQL internals | [YouTube](https://www.youtube.com/@hnasr) | Series | Intermediate–Advanced | Backend engineering channel; multiple deep-dive Postgres videos on WAL, MVCC, indexing |
| CMU 15-445 Database Systems Lectures | [YouTube](https://www.youtube.com/playlist?list=PLSE8ODhjZXjbj8BMuIrRcacnQh20hmY9g) | Full course lectures | Advanced | Andy Pavlo's Carnegie Mellon course; covers relational internals that underpin Postgres |

---

## Blogs & Articles

- **[PostgreSQL Wiki](https://wiki.postgresql.org/)** — Community-maintained knowledge base; excellent "Don't do this" page listing common anti-patterns
- **[GitLab Database Team Blog](https://about.gitlab.com/handbook/engineering/development/enablement/data_stores/database/)** — Real-world production Postgres operations at scale; covers migration patterns, index strategies, and bloat management
- **[Cybertec PostgreSQL Blog](https://www.cybertec-postgresql.com/en/blog/)** — Technical articles by Postgres core contributors; reliable and accurate
- **[depesz.com](https://www.depesz.com/)** — Hubert Lubaczewski's blog; famous for EXPLAIN ANALYZE visualizer and deep query plan analysis

---

## Papers & Research

| Title | Authors | Year | Link | Why It Matters |
|-------|---------|------|------|---------------|
| A Relational Model of Data for Large Shared Data Banks | E. F. Codd | 1970 | [ACM](https://dl.acm.org/doi/10.1145/362384.362685) | The foundational paper that defined the relational model; understanding it explains every design decision in PostgreSQL |
| The Design of POSTGRES | M. Stonebraker, L. Rowe | 1986 | [ACM](https://dl.acm.org/doi/10.1145/16856.16888) | Describes the original POSTGRES design goals and the extensible type system |
| A Critique of ANSI SQL Isolation Levels | H. Berenson et al. | 1995 | [ACM](https://dl.acm.org/doi/10.1145/223784.223785) | The paper that defines the modern understanding of isolation levels; directly relevant to Module 05 |

---

## Tools & Libraries

| Tool / Library | Language | Purpose | Link |
|---------------|----------|---------|------|
| pgAdmin 4 | Web/Desktop | GUI administration and query editor | [pgadmin.org](https://www.pgadmin.org/) |
| psql | CLI | Primary interactive terminal for PostgreSQL | Built into every Postgres installation |
| pg_dump / pg_restore | CLI | Backup and restore | Built into every Postgres installation |
| EXPLAIN Visualizer (explain.depesz.com) | Web | Visualize and annotate EXPLAIN ANALYZE output | [explain.depesz.com](https://explain.depesz.com/) |
| pgBench | CLI | Built-in benchmarking tool | Built into every Postgres installation |
| pg_activity | Python/CLI | Real-time top-like monitoring for Postgres | [github.com/dalibo/pg_activity](https://github.com/dalibo/pg_activity) |
| asyncpg | Python | High-performance async PostgreSQL driver | [github.com/MagicStack/asyncpg](https://github.com/MagicStack/asyncpg) |
| psycopg2 / psycopg3 | Python | Standard sync and async Postgres adapter | [psycopg.org](https://www.psycopg.org/) |

---

## Communities

| Community | Platform | Focus | Link |
|-----------|----------|-------|------|
| r/PostgreSQL | Reddit | General discussion | [reddit.com/r/PostgreSQL](https://www.reddit.com/r/PostgreSQL/) |
| PostgreSQL Mailing Lists | Email | Developer and user discussion | [postgresql.org/list/](https://www.postgresql.org/list/) |
| Stack Overflow | Stack Overflow | Technical Q&A | [Tag: postgresql](https://stackoverflow.com/questions/tagged/postgresql) |
| PostgreSQL IRC / Slack | IRC / Slack | Real-time community | See [postgresql.org/community/](https://www.postgresql.org/community/) |

---

## Cheat Sheets & Quick References

- **[PostgreSQL cheat sheet (postgresqltutorial.com)](https://www.postgresqltutorial.com/postgresql-cheat-sheet/)** — Compact reference covering common SQL commands
- **[psql commands cheat sheet](https://www.postgresql.org/docs/current/app-psql.html)** — Official reference for all psql backslash meta-commands

See also the local [CHEATSHEET.md](./CHEATSHEET.md) which you'll build yourself as you study.

---

## My Recommendations

_Fill in as you progress — what actually helped you most?_

### Best for Absolute Beginners

> _To be filled in_

### Best for Building Mental Models

> _To be filled in_

### Best for Practical / Hands-On Learning

> _To be filled in_

### Best Deep Reference

> _To be filled in_

---

## Resources to Evaluate

_Drop links here when you find something but haven't verified it yet._

- [ ] Use the Postgres EXPLAIN tool at explain.dalibo.com — needs verification vs. explain.depesz.com
- [ ] "PostgreSQL 14 Internals" book by Egor Rogov — needs edition/URL verification before recommending
