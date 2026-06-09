# Resources — Module 18: Build, Tooling, and Deployment

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[go command reference — pkg.go.dev/cmd/go](https://pkg.go.dev/cmd/go)** — pkg.go.dev

The authoritative reference for every `go` subcommand, flag, and environment variable. Read the sections on `go build` (flags, `-ldflags`, output naming), `go env` (the full variable list), `go mod` (tidy, download, verify), and `go work` (workspace mode). This is the definitive source — when in doubt, check here rather than third-party tutorials.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Compile and install the application — go.dev/doc/tutorial/compile-install](https://go.dev/doc/tutorial/compile-install)** — Official tutorial section walking through `go build` and `go install` with a working example; the fastest way to confirm your toolchain is set up correctly.

- **[Download and install Go — go.dev/doc/install](https://go.dev/doc/install)** — Official installation guide; explains `GOPATH`, `GOROOT`, `GOBIN`, and how `go install` puts binaries in `$HOME/go/bin`. Read this if you're confused about where `go install` puts binaries or why `go env GOPATH` matters.

- **[govulncheck and the Go Vulnerability Database — go.dev/security/vuln](https://go.dev/security/vuln)** — The Go security team's official documentation for `govulncheck`, the Go Vulnerability Database, and guidance on handling vulnerability reports. Includes installation, usage, and how to interpret the output.

---

## Linting and Static Analysis

- **[golangci-lint — golangci-lint.run](https://golangci-lint.run)** — Official site for the meta-linter. Read the "Usage" section for CLI flags, the "Configuration" section for `.golangci.yml` options, and the "Linters" page to understand what each linter checks. The GitHub Actions integration section shows the recommended `golangci/golangci-lint-action` configuration.

- **[staticcheck — staticcheck.dev](https://staticcheck.dev)** — The standalone static analyzer by Dominik Honnef. The "Checks" page is the most useful reference: it lists every check (SA, S, ST, QF categories) with code examples of what each one catches and why. Read this to understand the difference between `go vet`'s built-in checks and `staticcheck`'s extended analysis.

---

## Build and Release Automation

- **[GoReleaser — goreleaser.com](https://goreleaser.com)** — Official documentation for the release automation tool. Start with "Quick Start" (15 minutes, produces a real release), then read the "Build" and "Archive" sections to understand the `.goreleaser.yml` format. The "Customization" section covers Docker image publishing, Homebrew tap generation, and more.

---

## Docker

- **[Build and containerize a Go application — docs.docker.com/guides/go](https://docs.docker.com/guides/go/)** — Official Docker guide for Go, covering multi-stage builds, the `scratch` and `distroless` base images, and `CGO_ENABLED=0`. The code examples are directly applicable to production Go services.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| *The Go Programming Language* — Donovan & Kernighan | Ch. 10 (Packages and the Go Tool) | Covers `go build`, `go install`, import paths, internal packages, and the `go` command in depth; the best book coverage of the standard toolchain |
| *Go in Action* — Kennedy, Ketelsen, St. Martin | Ch. 3 (Packaging and tooling) | Concise overview of the Go toolchain, `go vet`, and the build system; useful as a quick reference alongside the Donovan & Kernighan coverage |
| *Cloud Native Go* — Matthew A. Titmus | Ch. 3 (Go Build Pipelines) | Covers Dockerizing Go services, multi-stage builds, and CI patterns specifically for cloud-native deployment; more practical and ops-focused than Donovan & Kernighan |

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[go/7. Packages and Modules]] (Module 7) | The module system (`go.mod`, `go.sum`, `GOPROXY`) is the foundation for supply-chain security and the `govulncheck` tooling in this module |
| [[go/11. Testing and Benchmarking]] (Module 11) | The CI pipeline's test job runs `go test -race`; coverage flags and test caching are properties of the testing system covered there |
| [[go/17. Runtime Internals and the Memory Model]] (Module 17) | Explains why `CGO_ENABLED=0` matters and what "static binary" means in terms of the runtime |
| [[go/19. Capstone Project]] (Module 19) | The capstone requires applying everything from this module: cross-compilation, Dockerfile, CI workflow, and version stamping |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "Effective Go" tooling section (https://go.dev/doc/effective_go) — covers formatting and `gofmt`; older but still accurate on tooling philosophy
- [ ] Go by Example — build flags page (https://gobyexample.com) — community-maintained; generally accurate but not official; verify examples compile against current Go version
