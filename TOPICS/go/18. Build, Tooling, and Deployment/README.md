# Module 18: Build, Tooling, and Deployment

[← Module 17: Runtime Internals and the Memory Model](../17.%20Runtime%20Internals%20and%20the%20Memory%20Model/) | [Topic Home](../README.md) | [Module 19: Capstone Project →](../19.%20Capstone%20Project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced--expert-red)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [The go Command Toolchain](#the-go-command-toolchain)
  - [Build Constraints and Build Tags](#build-constraints-and-build-tags)
  - [Version Stamping with -ldflags](#version-stamping-with--ldflags)
  - [Cross-Compilation](#cross-compilation)
  - [The Build Cache and Reproducible Builds](#the-build-cache-and-reproducible-builds)
  - [Linting and Static Analysis](#linting-and-static-analysis)
  - [Automating with Makefile or Taskfile](#automating-with-makefile-or-taskfile)
  - [Multi-Stage Docker Builds](#multi-stage-docker-builds)
  - [CI/CD with GitHub Actions](#cicd-with-github-actions)
  - [Releasing with GoReleaser](#releasing-with-goreleaser)
  - [Supply-Chain Security](#supply-chain-security)
  - [How the Concepts Fit Together](#how-the-concepts-fit-together)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Related Concepts](#related-concepts)
- [Exercises](#exercises)
- [Test](#test)
- [Projects](#projects)
- [Further Reading](#further-reading)
- [Learning Journal](#learning-journal)

---

## Overview

This module covers **Go's build system, developer tooling, and the full path from source code to a shipped binary**. Go's toolchain is famously self-contained — a single `go` command handles compilation, dependency resolution, formatting, vetting, and testing. But shipping production software requires more: cross-compiling for multiple platforms, stamping version information into binaries, containerizing with Docker, running automated checks in CI, and releasing with provenance.

By the end of this module, you will understand how to take a Go program from a developer's laptop to a reproducible artifact running in production — with the right toolchain choices at every step. This is the penultimate module; it equips you with the operational knowledge to ship the capstone project in [[go/19. Capstone Project]].

**Difficulty:** Advanced–Expert &nbsp;|&nbsp; **Estimated time:** 6–8 hours

---

## Learning Goals

By completing this module, you will be able to:

1. Use the full `go` command toolchain (`build`, `install`, `run`, `vet`, `fmt`, `env`, `work`, `clean`) confidently — _given an unfamiliar Go project, describe what each command does without looking at docs_
2. Write and apply build constraints (`//go:build`) to compile platform-specific or feature-specific code — _add a `//go:build linux` file to an existing project without breaking other platforms_
3. Stamp version, commit SHA, and build date into a binary using `-ldflags "-X pkg.Var=value"` — _produce a `myapp --version` flag that prints the correct values from a CI pipeline_
4. Cross-compile a Go binary for Linux/amd64 from macOS or Windows using `GOOS`/`GOARCH`, and explain the role of `CGO_ENABLED=0` for fully static binaries — _ship a container-ready binary without Docker-in-Docker_
5. Write a multi-stage Dockerfile that produces a minimal final image on `scratch` or `distroless`, and explain why layer ordering matters for cache efficiency — _reduce a 1 GB Docker image to under 20 MB_
6. Configure a GitHub Actions CI workflow with separate jobs for tests (with the race detector), linting, and a cross-platform build matrix — _read a failing Actions run and identify which job failed and why_
7. Use `govulncheck`, inspect `go.sum`, set `GOPROXY`, and explain the supply-chain security guarantees provided by the Go module system — _audit a project's dependencies for known CVEs_

---

## Prerequisites

### Required Modules

- [[go/7. Packages and Modules]] — you need to understand: `go.mod`, `go.sum`, the module path, `go get`, and how the module graph works; this module builds directly on those foundations for `GOPROXY`, `govulncheck`, and workspace mode
- [[go/11. Testing and Benchmarking]] — you need to understand: `go test`, the `-race` flag, coverage flags, and how test binaries are built; the CI workflow in this module runs tests with the race detector
- [[go/17. Runtime Internals and the Memory Model]] — you need to understand: why `CGO_ENABLED=0` matters (cgo constraints and the cost of dynamic linking), and what a fully static binary means for deployment

### Required Concepts

- **Module system and go.sum** — the `go.sum` file records cryptographic hashes of every dependency; understanding this is required for the supply-chain section
- **Linux container basics** — knowing that a Docker container runs a Linux process in a namespaced environment helps explain why we cross-compile for `linux/amd64` and why `scratch` images work
- **Environment variables** — `GOOS`, `GOARCH`, `CGO_ENABLED`, `GOFLAGS`, and `GOPROXY` are set as environment variables; comfort with `export VAR=value` and per-command `VAR=value go build` syntax is assumed

> [!TIP]
> If `go.mod` and `go.sum` feel shaky, re-read [[go/7. Packages and Modules]] before starting the Docker and CI sections. Gaps in module knowledge will obscure what `GOPROXY` and `govulncheck` are doing.

---

## Why This Matters

Every line of Go code you write eventually needs to be built, tested, verified, and shipped. The quality of that pipeline determines whether your team can deploy confidently, whether your binaries are reproducible, and whether a dependency vulnerability gets caught before it reaches production.

Concretely, mastery of this module enables you to:

- **Ship reliable cross-platform binaries** — Go's cross-compilation story is exceptional: a single `GOOS=linux GOARCH=amd64 go build` command on a Mac produces a Linux binary that works in any container; understanding this means you never need a Linux build server for compiling
- **Build minimal, secure container images** — a Go binary compiled with `CGO_ENABLED=0` is fully self-contained; the final Docker image can be `FROM scratch` (literally zero base OS), reducing attack surface from hundreds of CVEs to zero OS packages
- **Automate quality gates** — a CI pipeline that runs `go vet`, `golangci-lint`, and `go test -race` on every pull request catches bugs before they reach production; this is standard practice in every serious Go project
- **Audit supply-chain risk** — `govulncheck` scans for known CVEs in your dependencies; the `go.sum` hash database prevents dependency tampering; these are not optional for production software

Without this module's knowledge, you could write correct Go programs but not ship them safely — the code would live on a laptop rather than in production.

---

## Historical Context

Go's toolchain philosophy was shaped by the frustrations of building large C++ codebases at Google. When the language was designed in 2007–2009, one of the explicit goals was **a build system that required no configuration files** — just convention and a single tool.

Key moments in Go's build and deployment history:

- **2009** — Go's initial release includes the `go` command with `build`, `run`, `fmt`, and `test` as first-class subcommands; no separate Makefile is needed for basic projects
- **2012** — Go 1.0 ships with `go vet` as the first static analysis tool; `gofmt` is canonical, not optional — the community adopts it immediately
- **2015** — Go 1.5 introduces the `GOOS`/`GOARCH` cross-compilation matrix as a first-class feature; the Go compiler is rewritten in Go itself (no more C bootstrap)
- **2018** — Go 1.11 introduces `go mod` and Go Modules, replacing `GOPATH`-based dependency management; `go.sum` provides cryptographic integrity for dependencies; the module proxy (`GOPROXY`) is introduced
- **2019** — `sum.golang.org` and `proxy.golang.org` launch as official infrastructure; the checksum database prevents dependency substitution attacks
- **2021** — Go 1.17 introduces workspace mode (`go work`), allowing multi-module development without `replace` directives
- **2022** — `govulncheck` is released by the Go security team as the official vulnerability scanner; it uses the Go Vulnerability Database at `vuln.go.dev`
- **2024** — Go 1.22+ improves reproducible builds; the build cache makes incremental compilation nearly instant for large codebases

The broader ecosystem — `golangci-lint`, `goreleaser`, multi-stage Docker builds — emerged to complement the standard toolchain, not replace it. Understanding what the standard tools provide (and where they stop) clarifies why each third-party tool exists.

---

## Core Concepts

### The go Command Toolchain

The `go` command is a multi-tool: it compiles, tests, formats, vets, and manages dependencies. Every subcommand is worth knowing precisely.

```bash
# Build the package in the current directory; outputs ./myapp (or myapp.exe on Windows)
go build .

# Build and install to $GOPATH/bin (or $GOBIN if set)
go install .

# Compile and run without creating a binary on disk
go run main.go

# Run the official formatter on all .go files in the tree (modifies in place)
go fmt ./...

# Run the built-in static analyzer — always run this before committing
go vet ./...

# Download and tidy module dependencies (removes unused, adds missing)
go mod tidy

# Display effective environment variables used by the toolchain
go env

# Show available GOOS/GOARCH combinations
go tool dist list

# Enter Go workspace mode (multi-module development)
go work init ./module1 ./module2

# Remove cached build artifacts
go clean -cache

# Remove the module download cache
go clean -modcache
```

**`go env` output** — knowing what these variables do is essential for debugging build issues:

```bash
$ go env
GOPATH="/home/user/go"
GOPROXY="https://proxy.golang.org,direct"
GONOSUMCHECK=""
GOROOT="/usr/local/go"
GOOS="linux"
GOARCH="amd64"
CGO_ENABLED="1"
GOMODCACHE="/home/user/go/pkg/mod"
GOCACHE="/home/user/.cache/go-build"
```

---

### Build Constraints and Build Tags

Build constraints restrict which files are compiled based on platform, OS, architecture, or custom tags. They are declared with a `//go:build` directive on the first non-blank, non-comment line of the file.

```go
//go:build linux

// This file is only compiled when GOOS=linux.
// The build constraint must appear before the package clause.
package platform
```

Multiple conditions use boolean expressions:

```go
//go:build (linux || darwin) && amd64 && !cgo

// Compiled only on Linux/amd64 or macOS/amd64, and only when CGO is disabled.
package platform
```

**File name conventions** — Go also applies implicit constraints based on file names:

```
signal_unix.go      → compiled on Unix-like systems (linux, darwin, freebsd, ...)
signal_windows.go   → compiled only on Windows
atomic_amd64.go     → compiled only on amd64
```

**Custom tags** are used to opt in to optional features:

```go
//go:build integration
```

```bash
# Run only tests with the integration tag
go test -tags integration ./...

# Build with the debug tag enabled
go build -tags debug .
```

> [!NOTE]
> Before Go 1.17, build constraints used `// +build` syntax. Go 1.17+ uses `//go:build`. The `gofmt` tool automatically adds the new form when it encounters the old syntax. For Go 1.22+, only `//go:build` is recommended.

---

### Version Stamping with -ldflags

The linker flag `-X` injects a string value into a named package-level variable at link time. This is the canonical way to stamp version information — no build-time file generation required.

```go
// internal/version/version.go
package version

// These variables are set by the linker via -ldflags at build time.
// Default values are used when building without the flags (e.g., go run).
var (
    Version   = "dev"
    Commit    = "none"
    BuildDate = "unknown"
)
```

```bash
# Stamp version, git commit, and build date into the binary
go build \
  -ldflags "-X 'github.com/acme/myapp/internal/version.Version=v1.2.3' \
            -X 'github.com/acme/myapp/internal/version.Commit=$(git rev-parse --short HEAD)' \
            -X 'github.com/acme/myapp/internal/version.BuildDate=$(date -u +%Y-%m-%dT%H:%M:%SZ)'" \
  -o myapp .
```

```bash
# In a Makefile (see Makefile section below)
$ ./myapp --version
myapp v1.2.3 (commit: a3f8b2c, built: 2026-06-09T14:00:00Z)
```

**Additional useful linker flags:**

```bash
# Strip debug symbols and disable DWARF — reduces binary size
go build -ldflags "-s -w" .

# Combine stripping with version stamping
go build -ldflags "-s -w -X main.version=v1.0.0" .
```

> [!WARNING]
> `-s -w` strips the symbol table and debug information. This makes `pprof` and `dlv` (Delve debugger) less useful. Never use these flags in development; reserve them for release builds.

---

### Cross-Compilation

Go's cross-compilation is a first-class feature: set `GOOS` and `GOARCH` as environment variables and run `go build`. No cross-compiler or sysroot is needed for pure Go code.

```bash
# Linux 64-bit (for containers and most servers)
GOOS=linux GOARCH=amd64 go build -o myapp-linux-amd64 .

# Linux ARM64 (Raspberry Pi 4, AWS Graviton, Apple Silicon containers)
GOOS=linux GOARCH=arm64 go build -o myapp-linux-arm64 .

# macOS Intel
GOOS=darwin GOARCH=amd64 go build -o myapp-darwin-amd64 .

# macOS Apple Silicon
GOOS=darwin GOARCH=arm64 go build -o myapp-darwin-arm64 .

# Windows 64-bit
GOOS=windows GOARCH=amd64 go build -o myapp-windows-amd64.exe .

# List all supported GOOS/GOARCH combinations
go tool dist list
```

**`CGO_ENABLED=0` — fully static binaries:**

By default, Go uses cgo for some standard library features (notably `net` and `os/user` on Linux), which links against glibc dynamically. For container images — especially those using `scratch` or `distroless` — you need a fully static binary with no external dependencies.

```bash
# Fully static binary: no shared libraries, no glibc dependency
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o myapp .

# Verify no dynamic dependencies
$ ldd myapp
    not a dynamic executable   # ← this is what you want for scratch/distroless
```

The tradeoff (covered in [[go/17. Runtime Internals and the Memory Model]]): disabling cgo means you lose some platform-specific optimizations (like the OS-provided DNS resolver), but for most services this is an acceptable trade for deployment simplicity.

> [!NOTE]
> Use `go tool dist list` to see all ~50 GOOS/GOARCH combinations. The important production targets are `linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`, and `windows/amd64`.

---

### The Build Cache and Reproducible Builds

Go's build cache (stored in `$GOCACHE`, typically `~/.cache/go-build`) stores compiled package objects keyed by the inputs that produced them. If nothing changed, subsequent builds are instant.

```bash
# Show cache location
go env GOCACHE

# First build — compiles everything
$ time go build ./...
real    0m3.2s

# Second build — nothing changed, cache hit
$ time go build ./...
real    0m0.1s

# Clear cache if you suspect stale artifacts
go clean -cache
```

**Reproducible builds** — Go produces reproducible builds by default as of Go 1.13+: the same inputs (source, flags, Go version) produce byte-for-byte identical output. The important caveats:

- Embedding timestamps or random data breaks reproducibility — use `-ldflags "-X ..."` with a pinned value from `git describe` rather than `$(date)` if reproducibility is a hard requirement
- The Go toolchain version itself is part of the inputs; builds with `go1.22.0` and `go1.22.1` may differ

---

### Linting and Static Analysis

`go vet` is the built-in analyzer — always run it. It catches real bugs: mismatched `Printf` format strings, unreachable code, incorrect mutex copies, and more.

```bash
# Vet all packages in the module
go vet ./...

# Example: vet catches this bug
# fmt.Printf("hello %s\n", 42)  ← wrong type for %s
```

**staticcheck** — a more powerful standalone analyzer that catches additional issues:

```bash
# Install staticcheck
go install honnef.co/go/tools/cmd/staticcheck@latest

# Run on all packages
staticcheck ./...

# Example findings:
# main.go:12:2: this value of err is never used (SA4006)
# main.go:24:5: S1039: unnecessary use of fmt.Sprintf (S1039)
```

**golangci-lint** — a meta-linter that aggregates many linters (including `go vet`, `staticcheck`, `errcheck`, `revive`, and ~50 others) into a single tool with shared configuration:

```bash
# Install (check golangci-lint.run for latest installation method)
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin

# Run with defaults (uses .golangci.yml if present)
golangci-lint run ./...

# Run only specific linters
golangci-lint run --enable errcheck,gocritic ./...
```

**`.golangci.yml` configuration:**

```yaml
# .golangci.yml — golangci-lint configuration
run:
  timeout: 5m

linters:
  enable:
    - errcheck      # check that errors are handled
    - staticcheck   # staticcheck's full suite
    - govet         # go vet
    - revive        # drop-in replacement for golint
    - gosec         # security-focused checks

linters-settings:
  errcheck:
    # Ignore Close() errors on files — acceptable in many cases
    exclude-functions:
      - (*os.File).Close
```

**gofmt and goimports:**

```bash
# Format all files in-place (idempotent — safe to run multiple times)
gofmt -w .

# goimports also organizes and adds/removes import lines
go install golang.org/x/tools/cmd/goimports@latest
goimports -w .
```

---

### Automating with Makefile or Taskfile

A Makefile ties together the build, test, lint, and release commands into a consistent interface that works the same on a developer's machine and in CI.

```makefile
# Makefile — Go project automation
# ──────────────────────────────────────────────────────────────────────────────
# Variables
BINARY      := myapp
VERSION     ?= $(shell git describe --tags --always --dirty)
COMMIT      := $(shell git rev-parse --short HEAD)
BUILD_DATE  := $(shell date -u +%Y-%m-%dT%H:%M:%SZ)
LDFLAGS     := -s -w \
               -X 'github.com/acme/myapp/internal/version.Version=$(VERSION)' \
               -X 'github.com/acme/myapp/internal/version.Commit=$(COMMIT)' \
               -X 'github.com/acme/myapp/internal/version.BuildDate=$(BUILD_DATE)'

# Default target
.PHONY: all
all: fmt vet lint test build

.PHONY: build
build:  ## Build the binary for the current platform
	go build -ldflags "$(LDFLAGS)" -o bin/$(BINARY) .

.PHONY: build-linux
build-linux:  ## Cross-compile for Linux/amd64 (for containers)
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
	  go build -ldflags "$(LDFLAGS)" -o bin/$(BINARY)-linux-amd64 .

.PHONY: test
test:  ## Run tests with race detector
	go test -race -coverprofile=coverage.out ./...

.PHONY: coverage
coverage: test  ## Open HTML coverage report
	go tool cover -html=coverage.out

.PHONY: lint
lint:  ## Run golangci-lint
	golangci-lint run ./...

.PHONY: fmt
fmt:  ## Format code with goimports
	goimports -w .

.PHONY: vet
vet:  ## Run go vet
	go vet ./...

.PHONY: clean
clean:  ## Remove build artifacts and cache
	go clean -cache
	rm -rf bin/ coverage.out

.PHONY: docker-build
docker-build:  ## Build the Docker image
	docker build -t $(BINARY):$(VERSION) .

.PHONY: help
help:  ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
```

---

### Multi-Stage Docker Builds

A multi-stage Dockerfile uses multiple `FROM` statements. The first stage (the builder) contains the Go toolchain and all build dependencies. The final stage copies only the compiled binary into a minimal base image. This is the standard approach for Go containers.

```dockerfile
# syntax=docker/dockerfile:1
# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy module files first — Docker caches this layer separately.
# If go.mod/go.sum haven't changed, `go mod download` is skipped on rebuild.
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build — this layer re-runs only when source changes
COPY . .

# Build a fully static binary (no CGO, no shared libraries)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build \
    -ldflags "-s -w -X 'main.version=${VERSION:-dev}'" \
    -o /app/myapp .

# ── Stage 2: Final image ──────────────────────────────────────────────────────
# scratch = completely empty image; zero OS, zero packages, zero CVEs from the OS
FROM scratch

# Copy CA certificates so HTTPS calls work inside the container
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy the binary from the builder stage
COPY --from=builder /app/myapp /myapp

# Run as non-root (UID 65534 = nobody — numeric because scratch has no /etc/passwd)
USER 65534:65534

EXPOSE 8080
ENTRYPOINT ["/myapp"]
```

**Why layer order matters for cache efficiency:**

```dockerfile
# SLOW — source changes invalidate the go mod download layer
COPY . .
RUN go mod download  # ← re-runs every time any source file changes

# FAST — go.mod/go.sum are stable; source changes don't invalidate module cache
COPY go.mod go.sum ./
RUN go mod download  # ← cached unless dependencies change
COPY . .
RUN go build ...
```

**distroless alternative** — if you need a timezone database, C library, or `/tmp`:

```dockerfile
FROM gcr.io/distroless/static-debian12:nonroot AS final
COPY --from=builder /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

---

### CI/CD with GitHub Actions

A Go project CI workflow typically has three jobs: test (with race detector), lint, and optionally a build matrix across platforms.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # ── Job 1: Tests with race detector ─────────────────────────────────────────
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22"        # pin to a specific minor version
          cache: true               # cache the Go module and build caches

      - name: Download dependencies
        run: go mod download

      - name: Run tests with race detector
        run: go test -race -coverprofile=coverage.out ./...

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.out

  # ── Job 2: Lint ──────────────────────────────────────────────────────────────
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: "1.22"
          cache: true
      - name: Run golangci-lint
        uses: golangci/golangci-lint-action@v6
        with:
          version: latest

  # ── Job 3: Build matrix ──────────────────────────────────────────────────────
  build:
    name: Build (${{ matrix.goos }}/${{ matrix.goarch }})
    runs-on: ubuntu-latest
    needs: [test, lint]             # only run if test and lint pass
    strategy:
      matrix:
        include:
          - goos: linux
            goarch: amd64
          - goos: linux
            goarch: arm64
          - goos: darwin
            goarch: amd64
          - goos: darwin
            goarch: arm64
          - goos: windows
            goarch: amd64
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: "1.22"
          cache: true
      - name: Build
        env:
          GOOS: ${{ matrix.goos }}
          GOARCH: ${{ matrix.goarch }}
          CGO_ENABLED: "0"
        run: |
          go build \
            -ldflags "-s -w -X 'main.version=${{ github.ref_name }}'" \
            -o myapp-${{ matrix.goos }}-${{ matrix.goarch }} .
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myapp-${{ matrix.goos }}-${{ matrix.goarch }}
          path: myapp-${{ matrix.goos }}-${{ matrix.goarch }}
```

---

### Releasing with GoReleaser

GoReleaser automates the creation of a GitHub Release with pre-built binaries for all platforms, a changelog, Docker images, and checksums.

```yaml
# .goreleaser.yml — GoReleaser configuration
project_name: myapp

before:
  hooks:
    - go mod tidy    # ensure go.sum is current before release

builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - darwin
      - windows
    goarch:
      - amd64
      - arm64
    ldflags:
      # Stamp version, commit, and date into the binary
      - -s -w
      - -X github.com/acme/myapp/internal/version.Version={{.Version}}
      - -X github.com/acme/myapp/internal/version.Commit={{.Commit}}
      - -X github.com/acme/myapp/internal/version.BuildDate={{.Date}}

archives:
  - format: tar.gz
    # Windows archives use .zip
    format_overrides:
      - goos: windows
        format: zip

checksum:
  name_template: "checksums.txt"  # SHA256 checksums for all artifacts

changelog:
  sort: asc
  filters:
    exclude:
      - "^docs:"
      - "^test:"
```

```bash
# Test release locally without publishing
goreleaser release --snapshot --clean

# Release (run in CI, triggered by a git tag)
goreleaser release --clean
```

---

### Supply-Chain Security

Go's module system provides several supply-chain security layers, each addressing a different attack vector.

**`go.sum` and the checksum database:**

```bash
# go.sum contains hash entries for every dependency version:
# github.com/pkg/errors v0.9.1 h1:FEBLx1zS214owpjy7qsBeixbURkuhQAwrK5UwLGTwt38=
# github.com/pkg/errors v0.9.1/go.mod h1:bwawxfHBFNV+L2hUp1rHADufV3IMtnDRdf1r5NINEl0=

# The Go toolchain verifies these hashes against sum.golang.org on every download.
# Tampering with a dependency produces a checksum mismatch and fails the build.
```

**`govulncheck` — scanning for known CVEs:**

```bash
# Install
go install golang.org/x/vuln/cmd/govulncheck@latest

# Scan the current module's dependencies against the Go Vulnerability Database
govulncheck ./...

# Example output when a vulnerability is found:
# Vulnerability #1: GO-2024-2687
#   A crafted input to encoding/gob can cause a panic.
#   More info: https://pkg.go.dev/vuln/GO-2024-2687
#   Standard library
#     Found in: encoding/gob@go1.21.0
#     Fixed in: go1.21.6
```

**`GOPROXY` — controlling where modules are fetched from:**

```bash
# Default: use the official proxy (caches modules) with direct fallback
GOPROXY=https://proxy.golang.org,direct

# Require all modules from the proxy; fail if not available there
GOPROXY=https://proxy.golang.org,off

# Use a private proxy (e.g., Athens) for internal modules
GOPROXY=https://my-athens.internal,https://proxy.golang.org,direct

# Bypass the proxy for internal modules (comma or pipe separated patterns)
GONOSUMCHECK=*.internal.company.com
GONOSUMDB=*.internal.company.com
```

**`GOFLAGS` — setting default flags:**

```bash
# Apply -mod=vendor to all go commands without typing it every time
export GOFLAGS="-mod=vendor"

# Useful for CI where you vendor dependencies for reproducibility
go test ./...  # implicitly uses -mod=vendor
```

---

### How the Concepts Fit Together

```
Source code (.go files)
        │
        ├── Build constraints (/go:build)
        │       └── selects which files compile per GOOS/GOARCH/tag
        │
        ▼
go build  ←── GOOS/GOARCH (cross-compile)
              CGO_ENABLED=0 (static binary)
              -ldflags "-X ..." (version stamp)
              -ldflags "-s -w" (strip symbols)
        │
        ▼
Binary artifact
        │
        ├── Makefile / Taskfile  ←── orchestrates all steps
        │
        ├── Docker multi-stage build
        │       ├── Stage 1: builder (Go toolchain)
        │       └── Stage 2: scratch/distroless (binary only)
        │
        ├── GitHub Actions CI
        │       ├── go test -race
        │       ├── golangci-lint
        │       └── build matrix (all GOOS/GOARCH)
        │
        └── GoReleaser
                └── GitHub Release with binaries + checksums
```

Supply-chain (go.sum, GOPROXY, govulncheck) runs across the entire pipeline, not as a single step. The module system's integrity checks happen at `go build` and `go mod download` time; vulnerability scanning should be a CI job on its own schedule.

---

## Common Beginner Mistakes

> [!WARNING]
> **Mistake 1: Forgetting `CGO_ENABLED=0` for container builds**
>
> Building a Linux binary without `CGO_ENABLED=0` may produce a binary that dynamically links against glibc. If you then copy it into a `scratch` or `distroless` image, the container will fail at runtime with `no such file or directory` or `exec format error`, even though the binary is a valid Linux ELF.
>
> **Wrong:**
> ```bash
> GOOS=linux GOARCH=amd64 go build -o myapp .
> # Copies into FROM scratch — fails at runtime if CGO was used
> ```
>
> **Right:**
> ```bash
> CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o myapp .
> ldd myapp  # should print: not a dynamic executable
> ```
>
> **Why this matters:** The failure is silent at build time but crashes in production. Always verify with `ldd` before deploying to scratch/distroless.

> [!WARNING]
> **Mistake 2: Wrong `-ldflags -X` path — the variable is not stamped**
>
> The `-X` flag requires the full import path of the package plus the variable name, not just the variable name. A typo produces no error — the variable simply retains its default value.
>
> **Wrong (wrong package path — silently fails):**
> ```bash
> go build -ldflags "-X version.Version=v1.0.0" .
> # Correct: the package is not "version", it's the full path
> ```
>
> **Right:**
> ```bash
> go build -ldflags "-X 'github.com/acme/myapp/internal/version.Version=v1.0.0'" .
> # Verify it worked:
> ./myapp --version  # should print v1.0.0
> ```

> [!WARNING]
> **Mistake 3: Docker layer order invalidates the module cache on every build**
>
> Copying the entire source tree before running `go mod download` means the module download re-runs every time any source file changes — even changes unrelated to dependencies.
>
> **Wrong:**
> ```dockerfile
> COPY . .                # ← any source change invalidates everything below
> RUN go mod download
> RUN go build .
> ```
>
> **Right:**
> ```dockerfile
> COPY go.mod go.sum ./   # ← stable; only invalidated when deps change
> RUN go mod download     # ← cached until go.mod/go.sum change
> COPY . .
> RUN go build .
> ```

**Other pitfalls:**

- **Running `go vet` only locally** — vet catches real bugs (`go vet ./...` must be a CI step, not just a developer habit); a CI pipeline that skips vet will eventually ship a vetted-away bug
- **Committing `go.sum` deletions** — `go mod tidy` removes entries from `go.sum` if they're no longer needed, but running it in CI and committing the result without review can remove entries for indirect dependencies that are still needed; always review `go mod tidy` diffs before committing
- **Using `latest` in GitHub Actions** — `uses: actions/setup-go@v5` with `go-version: "latest"` means your CI breaks when a new Go minor version ships; pin to a specific version like `"1.22"` or `"1.22.3"`

---

## Mental Models

### Mental Model 1: The Build Pipeline as a Factory Assembly Line

Think of `go build` as a factory assembly line. Raw materials (source files) enter one end. At each station, something is added or verified: build constraints filter which files enter, the compiler processes them, the linker stamps version info with `-ldflags`, and the output is a finished binary. The Makefile is the factory floor manager — it tells each station when to run and in what order.

This model is useful when debugging a build failure: identify which station in the pipeline failed (compile error? linker error? constraint excluded a needed file?).

### Mental Model 2: The Container Image as a Shipping Container

A Docker multi-stage build is like packing a shipping container: you build the product in the factory (builder stage with the full toolchain), then ship only the product — not the factory machinery — in the container (final stage with just the binary). `FROM scratch` means the container is literally empty except for what you explicitly pack into it. This is why `CGO_ENABLED=0` is critical: you're shipping just the binary, and it must bring everything it needs.

### Mental Model 3: Supply-Chain Security as a Chain of Custody

Think of `go.sum` and the module proxy as a chain of custody document for your dependencies. Every dependency version has a cryptographic hash; the hash database is the notary. When you run `go mod download`, the toolchain checks the hash against the notary. If anyone tampers with a dependency, the chain of custody breaks and the build fails. `govulncheck` is like a safety recall notice — it tells you when a part in your supply chain has a known defect.

> [!NOTE]
> Use Model 1 (assembly line) when debugging build failures or designing build scripts. Use Model 2 (shipping container) when reasoning about Docker image size and what to include. Use Model 3 (chain of custody) when thinking about dependency security and audit requirements.

---

## Practical Examples

### Example 1: Version-Stamped Binary _(Basic)_

**Scenario:** Adding a `--version` flag that prints the version, commit, and build date stamped at link time.

**Goal:** Demonstrate the `-ldflags -X` pattern end-to-end with a working `--version` flag.

```go
// main.go
package main

import (
    "flag"
    "fmt"
    "os"
)

// Stamped at build time via -ldflags "-X main.version=..."
var (
    version   = "dev"
    commit    = "none"
    buildDate = "unknown"
)

func main() {
    showVersion := flag.Bool("version", false, "print version and exit")
    flag.Parse()

    if *showVersion {
        fmt.Printf("myapp %s (commit: %s, built: %s)\n", version, commit, buildDate)
        os.Exit(0)
    }

    fmt.Println("Hello from myapp")
}
```

```bash
# Build with stamped values
go build \
  -ldflags "-X 'main.version=v1.0.0' \
            -X 'main.commit=$(git rev-parse --short HEAD)' \
            -X 'main.buildDate=$(date -u +%Y-%m-%dT%H:%M:%SZ)'" \
  -o myapp .

./myapp --version
```

**Output / Result:**
```
myapp v1.0.0 (commit: a3f8b2c, built: 2026-06-09T14:00:00Z)
```

**What to notice:** The variables are declared at the package level and exported (or unexported — either works) with default "dev" values. Building without `-ldflags` produces `myapp dev (commit: none, built: unknown)`, which makes it obvious this is a development build.

---

### Example 2: Multi-Stage Docker Build _(Intermediate)_

**Scenario:** Containerizing a Go HTTP service for production.

**Goal:** Produce the smallest possible secure container image using a multi-stage build.

```dockerfile
# Dockerfile
# syntax=docker/dockerfile:1

# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Separate COPY for go.mod/go.sum enables layer caching for module downloads
COPY go.mod go.sum ./
RUN go mod download  # cached until go.mod or go.sum changes

COPY . .

# Static binary: no CGO, strip symbols for smaller size
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags "-s -w" -o /app/server ./cmd/server

# ── Stage 2: Minimal runtime image ───────────────────────────────────────────
FROM scratch

# HTTPS requires CA certificates — copy from the builder
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy only the binary
COPY --from=builder /app/server /server

# Non-root user (scratch has no /etc/passwd, use numeric UID)
USER 65534:65534

EXPOSE 8080
ENTRYPOINT ["/server"]
```

```bash
docker build -t myservice:latest .
docker images myservice
```

**Output / Result:**
```
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
myservice    latest    a4c7d8e9f1b2   5 seconds ago   8.3 MB
```

**What to notice:** The final image is ~8 MB — just the binary and CA certificates. A typical Alpine-based Go image is 300–400 MB. A `golang:1.22` base image is ~800 MB. The builder stage is discarded entirely; only the binary crosses stages.

---

### Example 3: Build Tags for Platform-Specific Code _(Applied)_

**Scenario:** A command-line tool that uses OS-specific system calls for getting terminal size.

**Goal:** Demonstrate build constraints isolating platform-specific code while keeping a common interface.

```go
//go:build linux || darwin
// termsize_unix.go — compiled only on Linux and macOS

package terminal

import (
    "golang.org/x/sys/unix"
)

// Size returns the terminal width and height using the Unix ioctl syscall.
func Size() (width, height int, err error) {
    ws, err := unix.IoctlGetWinsize(1, unix.TIOCGWINSZ)
    if err != nil {
        return 80, 24, err // sensible defaults
    }
    return int(ws.Col), int(ws.Row), nil
}
```

```go
//go:build windows
// termsize_windows.go — compiled only on Windows

package terminal

import "golang.org/x/sys/windows"

// Size returns the terminal width and height using the Windows Console API.
func Size() (width, height int, err error) {
    var info windows.ConsoleScreenBufferInfo
    err = windows.GetConsoleScreenBufferInfo(windows.Handle(1), &info)
    if err != nil {
        return 80, 24, err
    }
    return int(info.Size.X), int(info.Size.Y), nil
}
```

```bash
# Cross-compile for each platform — each picks the right file
GOOS=linux go build ./...    # compiles termsize_unix.go
GOOS=darwin go build ./...   # compiles termsize_unix.go
GOOS=windows go build ./...  # compiles termsize_windows.go
```

**What to notice:** The package `terminal` exports the same `Size()` signature on all platforms. Callers never see the platform differences. The `//go:build` constraint is the sole mechanism — no `runtime.GOOS` switch needed in shared code.

---

### Example 4: govulncheck in CI _(Edge Case)_

**Scenario:** A dependency you've been using for a year gets a CVE filed. Your code calls the vulnerable function.

```bash
# Add govulncheck to your CI pipeline
govulncheck ./...
```

**Output / Result:**
```
Scanning your code and 72 packages across 8 dependent modules for known vulnerabilities...

Vulnerability #1: GO-2024-3111
  Parsing a crafted JSON payload causes an uncontrolled recursion in
  github.com/acme/jsonparser.
  More info: https://pkg.go.dev/vuln/GO-2024-3111
  Module: github.com/acme/jsonparser
    Found in: github.com/acme/jsonparser@v1.2.0
    Fixed in: github.com/acme/jsonparser@v1.2.4
  Call stacks in your code:
      cmd/server/main.go:42:18: main.parseRequest calls
          github.com/acme/jsonparser.Parse

1 vulnerability found.
```

**Why this is important:** `govulncheck` is smarter than a simple dependency version check: it reports only vulnerabilities that your code actually *calls*. If you depend on a vulnerable package but never call the vulnerable function, `govulncheck` tells you it's a potential vulnerability but not an active one. This reduces false positives dramatically compared to tools that flag all transitive dependencies.

---

## Related Concepts

Within this topic:

- [[go/7. Packages and Modules]] — the module system (`go.mod`, `go.sum`, `go mod tidy`, `GOPROXY`) is the foundation for everything in this module; build constraints interact with the module graph
- [[go/11. Testing and Benchmarking]] — the CI pipeline's test job runs `go test -race`; coverage flags and test caching behavior are properties of the testing system
- [[go/17. Runtime Internals and the Memory Model]] — explains why `CGO_ENABLED=0` matters (cgo links against platform libraries; disabling it produces a fully portable binary); the build cache ties into the compiler's SSA IR pipeline

Forward reference:

- [[go/19. Capstone Project]] — the capstone project will require everything from this module: cross-compiled binaries, a Dockerfile, a CI workflow, and version stamping

---

## Exercises

Practice problems are in [EXERCISES.md](./EXERCISES.md).

**Preview — Exercise 1:**

> **Version Flag with ldflags** _(Easy)_
>
> Write a Go program that exposes a `--version` flag. Add package-level string variables for version, commit, and build date. Build the binary using `-ldflags "-X ..."` to stamp all three values. Verify the output matches what you stamped.
>
> [See full problem and solution →](./EXERCISES.md#exercise-1-version-flag-with-ldflags--easy--1-pt)

The exercises range from stamping versions and cross-compiling binaries to writing a full multi-stage Dockerfile and a GitHub Actions CI workflow.

---

## Test

When you feel ready, take the self-assessment: [TEST.md](./TEST.md)

**Test overview:**
- Section 1: Recall (5 questions, 1 pt each)
- Section 2: Conceptual Understanding (3 questions, 2 pts each)
- Section 3: Applied / Practical (2 questions, 3 pts each)
- Section 4: Scenario / Debugging (1 question, 3 pts)
- Section 5: Discussion (1 question, 2 pts)
- Section 6: Bonus Challenge (1 question, 5 pts bonus)

**Passing:** ≥ 70% of non-bonus points (≥ 15/22). Aim for ≥ 80% (≥ 18/22).

---

## Projects

See the topic-level [PROJECTS.md](../PROJECTS.md) for project ideas.

**Recommended project after this module:**
Production-Ready CLI Tool — take any prior project (word counter, HTTP client, key-value store) and ship it properly: add version stamping, cross-compile to Linux/macOS/Windows, write a multi-stage Dockerfile, publish a GitHub Actions CI workflow that tests and lints on every push, and tag a release with GoReleaser. The project is complete when a `go install` from a published tag works for a fresh user.

---

## Further Reading

These are verified, high-quality resources specifically relevant to this module:

1. **[Compile and install the application — go.dev/doc/tutorial](https://go.dev/doc/tutorial/compile-install)** — Official Go tutorial section on `go build` and `go install`; the fastest path to understanding the basic build workflow
2. **[go command reference — pkg.go.dev/cmd/go](https://pkg.go.dev/cmd/go)** — The authoritative reference for every `go` subcommand, flag, and environment variable; bookmark this for the `build`, `env`, `vet`, and `mod` subcommands
3. **[Download and install Go — go.dev/doc/install](https://go.dev/doc/install)** — Official installation guide including `GOPATH`, `GOROOT`, and `PATH` setup; useful for understanding the toolchain layout
4. **[golangci-lint — golangci-lint.run](https://golangci-lint.run)** — Official site for the meta-linter; the "Usage" and "Configuration" sections explain `.golangci.yml` and the available linters
5. **[staticcheck — staticcheck.dev](https://staticcheck.dev)** — Home for the standalone static analyzer; the "Checks" page lists every check with examples of what it catches
6. **[GoReleaser — goreleaser.com](https://goreleaser.com)** — Official documentation for the release automation tool; the "Quick Start" takes about 15 minutes and produces a real GitHub Release
7. **[govulncheck — go.dev/security/vuln](https://go.dev/security/vuln)** — Official Go vulnerability management page, including the `govulncheck` tool, the Go Vulnerability Database, and guidance on remediation
8. **[Build and push Docker images (Go) — docs.docker.com/guides/go](https://docs.docker.com/guides/go/)** — Official Docker guide for containerizing Go applications, covering multi-stage builds and the scratch base image

For a complete resource list, see the topic-level [RESOURCES.md](../RESOURCES.md).

---

## Learning Journal

_Record your experience studying this module. Be specific — vague entries are useless later._
_Newest entries at the top._

---

### YYYY-MM-DD — Started Module 18

**What I covered today:**
- Read the Overview and Why This Matters sections
- Worked through Core Concepts up to (concept name here)

**What clicked:**
- _Something that made sense_

**What's still unclear:**
- _Something that's still fuzzy — add to QUESTIONS.md_

**Questions logged:**
- See [QUESTIONS.md](./QUESTIONS.md) Q001

**Test score:** _Not taken yet_

---

_Add new entries above this line._
