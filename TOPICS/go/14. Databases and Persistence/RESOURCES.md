# Resources — Module 14: Databases and Persistence

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Accessing relational databases — go.dev/doc/database](https://go.dev/doc/database/)** — golang.org / go.dev

The official Go documentation guide for `database/sql`. It covers opening a database, executing queries, using prepared statements, handling transactions, and avoiding SQL injection — in a narrative format that explains the *why* alongside the *how*. More approachable than the API reference for first-time readers. Read the full guide from start to finish; it is concise (~15 pages) and accurate.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[pkg.go.dev/database/sql](https://pkg.go.dev/database/sql)** — The standard library API reference. The package-level documentation is essential reading: it explicitly documents that `sql.DB` is a pool (not a single connection), describes the pool tuning methods, explains `NullString` and related types, and documents `ErrNoRows` and `ErrTxDone`. Read the package doc before diving into individual function signatures.

- **[Tutorial: Accessing a relational database — go.dev](https://go.dev/doc/tutorial/database-access)** — Official step-by-step tutorial that builds a Go program accessing a MySQL database. The driver and placeholder syntax (`?`) are the same as SQLite; the `database/sql` API calls are identical. Useful as a guided walkthrough for learners who prefer concrete tutorials over reference documentation.

- **[Managing connections — go.dev/doc/database/manage-connections](https://go.dev/doc/database/manage-connections)** — Official documentation specifically focused on connection pool tuning. Explains `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`, and `SetConnMaxIdleTime` with guidance on when and why to set each. Essential reading before deploying any `database/sql` service to production.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 4 (Composite Types), Ch. 7 (Interfaces) | Does not cover `database/sql` directly, but Ch. 7's discussion of interface design is the conceptual foundation for the repository pattern used in this module |
| *Learning Go* — Jon Bodner (2nd ed.) | Ch. 13 (Writing Tests) + Ch. on database access | Bodner covers `database/sql` with practical examples; his treatment of testing with interfaces maps directly to the repository/fake pattern in this module |

---

## Migration Tools

_The two most commonly used migration tools for Go database applications._

- **[golang-migrate/migrate](https://github.com/golang-migrate/migrate)** — Runs versioned SQL migration files (up and down). Has a Go library for running migrations programmatically at startup. Supports SQLite, PostgreSQL, MySQL, and many others. Each migration is a separate file (`000001_create_users.up.sql` / `000001_create_users.down.sql`). The project page and README contain accurate, up-to-date usage instructions.

- **[pressly/goose](https://github.com/pressly/goose)** — Similar migration tool with slightly different conventions. Supports both SQL and Go-language migration files (for complex data transformations that cannot be expressed in SQL alone). The Go migration file support is useful for backfills and computed column migrations. Check the repository README for current API details.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/6. Methods and Interfaces]] (Module 6) | The repository pattern is a direct application of interface-based design; defining `UserStore` as an interface and depending on it in handlers is the same technique from Module 6 |
| [[go/8. Error Handling]] (Module 8) | Every `database/sql` function returns an error; `sql.ErrNoRows`, wrapping with `%w`, and `errors.Is` for sentinel errors are used in every query function |
| [[go/13. Web Services and APIs]] (Module 13) | This module adds the persistence layer to the HTTP APIs built in Module 13; `r.Context()` propagation connects the two modules |
| [[go/15. Reflection and Metaprogramming]] (Module 15) | `sqlx` and `sqlc` use struct tags for column mapping; Module 15 explains how struct tags work and how tools like `encoding/json` and `sqlx` read them via reflection |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[concurrency]] | Concurrency fundamentals | `database/sql`'s connection pool manages concurrent access internally; understanding Go's concurrency model helps reason about pool saturation and lock contention at high throughput |
| [[memory-management]] | Memory management | Each idle connection in the pool holds OS-level resources (file descriptors, memory); `SetConnMaxIdleTime` and `SetConnMaxLifetime` interact with how the GC and OS manage these resources |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] [Go by Example — SQLite](https://gobyexample.com) — community-maintained; check for current SQLite driver usage (the examples may use `mattn/go-sqlite3` which requires CGo)
- [ ] [jmoiron/sqlx README](https://github.com/jmoiron/sqlx) — verify the `StructScan`, `Get`, `Select` API is still current; the package has been stable for years but the README is the authoritative source
- [ ] [sqlc.dev documentation](https://docs.sqlc.dev) — the `sqlc` code generation tool; the docs are actively maintained but the API evolves; verify the current `sqlc.yaml` configuration format before using
