# Resources — Module 19: Capstone Project

> Resources listed here are specific to **building a production Go service**.
> These are the references you will reach for during the build, not after it.
> For the full topic resource list, see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Reference — Standard Library

_These are the packages you will use most. Bookmark all of them before you start building._

- **[pkg.go.dev/net/http](https://pkg.go.dev/net/http)** — The standard HTTP server and client. Read the `ServeMux`, `Server`, `Handler`, `ResponseWriter`, and `Request` type documentation carefully. The Go 1.22 release notes explain the new pattern-matching routing in `ServeMux`.

- **[pkg.go.dev/database/sql](https://pkg.go.dev/database/sql)** — The standard SQL interface. The `DB`, `Rows`, `Row`, `Stmt`, and `Tx` types are the core. Pay special attention to the connection pool configuration methods (`SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`) and the context-aware query methods.

- **[pkg.go.dev/log/slog](https://pkg.go.dev/log/slog)** — Structured logging, added in Go 1.21. The `Logger`, `Handler`, `JSONHandler`, `TextHandler`, and `LogAttrs` types are the core API. This is the correct logger to use for new production services; the old `log` package is for simple scripts.

- **[pkg.go.dev/context](https://pkg.go.dev/context)** — The full context package documentation. Read the package-level doc comment carefully: it explains when to use `Background`, `TODO`, `WithCancel`, `WithTimeout`, `WithDeadline`, and `WithValue`, and when each is appropriate.

- **[pkg.go.dev/os/signal](https://pkg.go.dev/os/signal)** — Signal handling. The `NotifyContext` function (Go 1.16+) is the correct way to handle SIGINT and SIGTERM in a production service. Read its documentation and the example.

---

## Official Language and Tooling Documentation

- **[go.dev/doc/effective_go](https://go.dev/doc/effective_go)** — Effective Go. The "Errors" and "Interfaces" sections are directly relevant to the design decisions in this project. The "Goroutines" and "Channels" sections are relevant if you add background workers.

- **[go.dev/doc/go1.22](https://go.dev/doc/go1.22)** — Go 1.22 release notes. Read the `net/http` section describing the new `ServeMux` routing patterns (`GET /path`, `{wildcard}` segments). This is the feature that enables method-based routing without a third-party router.

- **[go.dev/blog/context](https://go.dev/blog/context)** — "Go Concurrency Patterns: Context" — the original blog post that introduced the `context` package. Even though `context` is now standard library, this post explains the design rationale clearly.

- **[go.dev/blog/http-tracing](https://go.dev/blog/http-tracing)** — Useful background on how `net/http` works internally; relevant if you need to debug connection lifecycle issues.

---

## SQLite Driver

- **[pkg.go.dev/modernc.org/sqlite](https://pkg.go.dev/modernc.org/sqlite)** — The pure-Go SQLite driver. No CGO required, cross-compiles cleanly. The package index page shows the import path and connection string format. Use `"sqlite"` as the driver name in `sql.Open`.

---

## The Twelve-Factor App

- **[12factor.net](https://12factor.net)** — The Twelve-Factor App methodology. Read factors I (Codebase), III (Config), XI (Logs), and XII (Admin processes) specifically. Factor III (config via environment variables) is directly relevant to M6. Factor XI (logs as event streams, written to stdout) explains why your service should write logs to stdout and let the container runtime handle log collection.

---

## Containerization

- **[docs.docker.com/develop/develop-images/multistage-build](https://docs.docker.com/develop/develop-images/multistage-build/)** — Docker multi-stage build documentation. Read the "Use multi-stage builds" section. Directly relevant to M7.

- **[github.com/GoogleContainerTools/distroless](https://github.com/GoogleContainerTools/distroless)** — Distroless container images from Google. `gcr.io/distroless/static:nonroot` is the recommended base for statically compiled Go binaries: no shell, no package manager, minimal attack surface, typically under 3 MB. Verify this URL is current before using it.

---

## CI and Release Tooling

- **[goreleaser.com/docs](https://goreleaser.com/docs/)** — GoReleaser documentation. GoReleaser automates cross-compilation, binary naming, checksum generation, GitHub Release creation, and Docker image tagging. It is the standard tool for Go release automation. Relevant to M7.

- **[github.com/golangci/golangci-lint — docs/usage/install](https://golangci-lint.com/usage/install/)** — golangci-lint installation guide. `golangci-lint` runs many linters in parallel and is the standard linting tool for Go CI pipelines. Verify this URL is current before using it.

---

## Books (Verified)

| Book | Relevant Sections | Notes |
|------|------------------|-------|
| *Let's Go* — Alex Edwards | All chapters | A complete walkthrough of building an HTTP service with `database/sql`, structured logging, and middleware. Highly recommended as a companion resource while building your capstone. The book is available at [lets-go.alexedwards.net](https://lets-go.alexedwards.net) (paid). |
| *Let's Go Further* — Alex Edwards | Advanced patterns | Extends the Let's Go service with JSON APIs, authentication, rate limiting, and deployment. Directly relevant to the "Going Further" extensions in this module. Available at [lets-go-further.alexedwards.net](https://lets-go-further.alexedwards.net) (paid). |
| *The Go Programming Language* — Donovan & Kernighan | Ch. 7 (Interfaces), Ch. 8 (Goroutines/Channels), Ch. 9 (Concurrency) | The reference book for Go. The interface design in Ch. 7 is especially relevant to the Store interface design in this project. |

---

## Related Modules in This Topic

| Module | What to review for this project |
|--------|---------------------------------|
| [[go/6. Methods and Interfaces]] | Interface definition, structural typing, method receivers — the Store interface design |
| [[go/8. Error Handling]] | Custom error types, `fmt.Errorf` wrapping, `errors.As` — the error handling architecture |
| [[go/9. Concurrency]] | Goroutines, channels, `sync.WaitGroup` — graceful shutdown coordination |
| [[go/11. Testing and Benchmarking]] | Table-driven tests, `httptest`, coverage — the test suite |
| [[go/12. Advanced Concurrency Patterns]] | `context`, signal handling, `context.WithTimeout` — request lifecycle management |
| [[go/13. Web Services and APIs]] | `net/http`, routing, JSON, middleware — the HTTP layer |
| [[go/14. Databases and Persistence]] | `database/sql`, connection pools, prepared statements — the store implementation |
| [[go/18. Build, Tooling, and Deployment]] | Dockerfile, CI, `goreleaser`, linting — the delivery layer |

---

## Resources to Evaluate

_Links found but not yet fully verified. Check before relying on these._

- [ ] [go.dev/blog/slog](https://go.dev/blog/slog) — Official blog post on `log/slog` — verify it covers the full API including custom handlers
- [ ] [go.dev/wiki/SQLInterface](https://go.dev/wiki/SQLInterface) — Go wiki page on the `database/sql` interface — verify it is up to date with current best practices
