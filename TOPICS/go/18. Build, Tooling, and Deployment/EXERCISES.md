# Exercises — Module 18: Build, Tooling, and Deployment

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read — actually run the commands and observe the output.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–15 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 20–35 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 40–75 min | 3 pts |
| ⭐ Expert | Open-ended; more than one good answer | 90+ min | 5 pts |

---

## Exercise 1: Version Flag with ldflags [🟢 Easy] [1 pt]

### Context
Stamping version information into a binary at link time is the canonical Go approach — no generated files, no runtime lookups, no configuration. This exercise establishes the `-ldflags -X` pattern that every other exercise and the CI workflow will build on.

### Task
Write a Go program (`main.go`) that:
1. Declares three package-level string variables: `version`, `commit`, and `buildDate` with default values `"dev"`, `"none"`, and `"unknown"`
2. Exposes a `--version` flag that prints all three values and exits
3. Has a normal code path that prints `"Hello from myapp"`

Build the binary twice: once with plain `go build` (showing the defaults), and once with `-ldflags "-X ..."` stamping real values.

### Requirements
- [ ] Three package-level variables with sensible defaults
- [ ] `--version` flag implemented with the `flag` package
- [ ] `go build` without ldflags produces `"myapp dev (commit: none, built: unknown)"`
- [ ] `go build -ldflags "-X 'main.version=v1.0.0' -X 'main.commit=abc1234' -X 'main.buildDate=2026-06-09'"` produces the stamped values

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Declare the variables at the package level (outside `main`), not inside `main`. They must be package-level `var` declarations for the linker's `-X` flag to target them.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

The `-X` flag syntax is: `-X 'importpath.VariableName=value'`. For variables in `package main`, the import path is just `main`. Example: `-X 'main.version=v1.0.0'`.

</details>

### Expected Output / Acceptance Criteria
```
# Without ldflags:
$ ./myapp --version
myapp dev (commit: none, built: unknown)

# With ldflags:
$ ./myapp --version
myapp v1.0.0 (commit: abc1234, built: 2026-06-09)
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
// main.go
package main

import (
    "flag"
    "fmt"
    "os"
)

// Stamped by the linker via -ldflags "-X main.version=..." at build time.
// Default values are used for development builds.
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
# Build without stamping — shows defaults
go build -o myapp .
./myapp --version
# myapp dev (commit: none, built: unknown)

# Build with stamped values
go build \
  -ldflags "-X 'main.version=v1.0.0' -X 'main.commit=abc1234' -X 'main.buildDate=2026-06-09'" \
  -o myapp .
./myapp --version
# myapp v1.0.0 (commit: abc1234, built: 2026-06-09)
```

**Explanation:**
The `-X` flag injects a string value into a named variable at link time. The package-level declaration provides a default so the program is still usable without the flags. Note that `-X` only works for `string` variables — not `int`, `bool`, or any other type. The `flag` package's `Bool` returns a pointer; dereference it with `*showVersion`.

**Common wrong answers:**
- Declaring the variables inside `main()` — the linker cannot target local variables, only package-level ones
- Using a short import path like `-X 'version.Version=...'` when the actual package is `main` — this silently does nothing

</details>

---

## Exercise 2: go vet and Build Tag [🟢 Easy] [1 pt]

### Context
`go vet` catches real bugs that the compiler doesn't. Build constraints restrict compilation to specific platforms. Both tools are the first line of defense before code reaches a CI system.

### Task
1. Write a Go file with a deliberate `go vet` error: a `fmt.Printf` call with a mismatched format verb (e.g., `fmt.Printf("%s\n", 42)` — using `%s` for an integer).
2. Run `go vet ./...` and observe the error.
3. Fix the error and run `go vet ./...` again to confirm it passes.
4. Add a second file with `//go:build integration` at the top. Add a function in it. Demonstrate that `go build .` ignores it, but `go build -tags integration .` includes it.

### Requirements
- [ ] `go vet` reports the format mismatch before the fix
- [ ] `go vet` passes cleanly after the fix
- [ ] The `//go:build integration` file is excluded from `go build .` and included with `go build -tags integration .`

### Hints
<details>
<summary>Hint 1</summary>

For the build tag demonstration, the simplest approach is to have the integration file define a function or variable that causes a compile error if included twice — like a duplicate `main` function — so you can clearly see when it's included vs excluded.

</details>

### Expected Output / Acceptance Criteria
```
# Before fix:
$ go vet ./...
./main.go:8:2: fmt.Printf format %s has arg 42 of wrong type int

# After fix:
$ go vet ./...
(no output — clean)

# Without the tag:
$ go build .
(succeeds, integration file excluded)

# With the tag:
$ go build -tags integration .
(succeeds, integration file included)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
// main.go
package main

import "fmt"

func main() {
    n := 42
    // BUG: %s expects a string, but n is an int — go vet will catch this
    fmt.Printf("%s\n", n) // ← change to %d to fix
}
```

```go
//go:build integration

// integration.go — only compiled when -tags integration is passed
package main

import "fmt"

func init() {
    fmt.Println("integration mode enabled")
}
```

```bash
go vet ./...
# ./main.go:7:2: fmt.Printf format %s has arg n of wrong type int

# Fix: change %s to %d, then:
go vet ./...
# (no output)

# Test the build tag:
go build .            # excludes integration.go
go build -tags integration .  # includes integration.go
```

**Explanation:**
`go vet` catches the `%s`/`int` mismatch because the `printf` analyzer knows that `%s` expects a `string` (or `Stringer`). This class of bug — wrong format verbs — would panic or produce garbage output at runtime. `go vet` catches it statically.

Build tags (`//go:build integration`) appear on the first non-blank line before the `package` clause. The `go build` command evaluates these constraints; without `-tags integration`, the file is as if it doesn't exist.

</details>

---

## Exercise 3: Cross-Compile a Binary [🟡 Medium] [2 pts]

### Context
Cross-compilation is one of Go's most powerful features for distribution. This exercise builds the same binary for Linux and macOS from whatever platform you're on, verifies the output is a static binary, and confirms the file type.

### Task
Using the program from Exercise 1 (or any `main` package):
1. Cross-compile for `linux/amd64` with `CGO_ENABLED=0`, outputting to `bin/myapp-linux-amd64`
2. Cross-compile for `darwin/arm64` with `CGO_ENABLED=0`, outputting to `bin/myapp-darwin-arm64`
3. Run `file bin/myapp-linux-amd64` to confirm it's an ELF 64-bit binary
4. Run `ldd bin/myapp-linux-amd64` (if on Linux) or explain what the expected output would be

### Requirements
- [ ] Both binaries are produced without error
- [ ] The Linux binary is confirmed as ELF 64-bit (via `file`)
- [ ] You can explain why `CGO_ENABLED=0` is necessary for container deployment
- [ ] Version ldflags are included in the build commands

### Hints
<details>
<summary>Hint 1</summary>

Set `GOOS`, `GOARCH`, and `CGO_ENABLED` as environment variable prefixes before `go build`: `CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build ...`. This is equivalent to `export`ing them but only applies to that single command.

</details>

<details>
<summary>Hint 2</summary>

`mkdir -p bin` before running the build commands, since Go won't create the output directory for you.

</details>

### Expected Output / Acceptance Criteria
```bash
$ file bin/myapp-linux-amd64
bin/myapp-linux-amd64: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, ...

$ ldd bin/myapp-linux-amd64
    not a dynamic executable
```

### Solution
<details>
<summary>Show Solution</summary>

```bash
mkdir -p bin

# Linux/amd64 — static binary for containers
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
  go build \
  -ldflags "-s -w -X 'main.version=v1.0.0' -X 'main.commit=abc1234'" \
  -o bin/myapp-linux-amd64 .

# macOS/arm64 — Apple Silicon
CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 \
  go build \
  -ldflags "-s -w -X 'main.version=v1.0.0' -X 'main.commit=abc1234'" \
  -o bin/myapp-darwin-arm64 .

# Verify:
file bin/myapp-linux-amd64
# bin/myapp-linux-amd64: ELF 64-bit LSB executable, x86-64, statically linked, ...

ldd bin/myapp-linux-amd64
# not a dynamic executable   ← correct for scratch/distroless containers
```

**Explanation:**
`CGO_ENABLED=0` disables the cgo bridge to C libraries. Without it, Go's `net` package and other parts of the standard library that use cgo would produce a binary that dynamically links against glibc. Such a binary runs on a standard Linux machine but fails in a `scratch` or `distroless` container because those images lack `/lib/x86_64-linux-gnu/libc.so.6`. The `file` command reveals the binary type; `ldd` reveals its dynamic link requirements (none for a static binary).

</details>

---

## Exercise 4: Makefile with Build Targets [🟡 Medium] [2 pts]

### Context
A Makefile consolidates all project commands into a consistent interface. This is the single document a new contributor reads to understand how to build, test, and release the project. Writing a good Makefile is a professional skill.

### Task
Write a `Makefile` for the project from the previous exercises with the following targets:
- `build` — builds a binary with version stamping (using `git describe --tags --always`)
- `build-linux` — cross-compiles for `linux/amd64` with `CGO_ENABLED=0`
- `test` — runs `go test -race ./...`
- `lint` — runs `go vet ./...` (substitute `golangci-lint run ./...` if installed)
- `clean` — removes `bin/` and runs `go clean -cache`
- `help` — prints a list of targets with descriptions

### Requirements
- [ ] Variables `BINARY`, `VERSION`, `COMMIT`, and `LDFLAGS` are defined at the top
- [ ] All targets are declared `.PHONY`
- [ ] `help` target prints target descriptions extracted from `##` comments
- [ ] Running `make` (no target) runs `build` by default
- [ ] Running `make help` outputs readable target descriptions

### Hints
<details>
<summary>Hint 1</summary>

Set `VERSION` using `$(shell git describe --tags --always --dirty)` — this produces `v1.0.0-dirty` if there are uncommitted changes, or `v1.0.0` for a clean tag. If no tags exist, it falls back to the commit hash.

</details>

<details>
<summary>Hint 2 (help target)</summary>

The `help` target uses `grep` to extract lines with `##` comments: `grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'`

</details>

### Expected Output / Acceptance Criteria
```
$ make help
  build                Build binary for current platform
  build-linux          Cross-compile for linux/amd64
  test                 Run tests with race detector
  lint                 Run go vet
  clean                Remove build artifacts

$ make build
go build -ldflags "..." -o bin/myapp .

$ make test
go test -race ./...
ok      github.com/acme/myapp  0.042s
```

### Solution
<details>
<summary>Show Solution</summary>

```makefile
# Makefile
BINARY     := myapp
VERSION    ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
COMMIT     := $(shell git rev-parse --short HEAD 2>/dev/null || echo "none")
BUILD_DATE := $(shell date -u +%Y-%m-%dT%H:%M:%SZ)
LDFLAGS    := -s -w \
              -X 'main.version=$(VERSION)' \
              -X 'main.commit=$(COMMIT)' \
              -X 'main.buildDate=$(BUILD_DATE)'

.DEFAULT_GOAL := build

.PHONY: build
build:  ## Build binary for current platform
	mkdir -p bin
	go build -ldflags "$(LDFLAGS)" -o bin/$(BINARY) .

.PHONY: build-linux
build-linux:  ## Cross-compile for linux/amd64
	mkdir -p bin
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
	  go build -ldflags "$(LDFLAGS)" -o bin/$(BINARY)-linux-amd64 .

.PHONY: test
test:  ## Run tests with race detector
	go test -race ./...

.PHONY: lint
lint:  ## Run go vet (or golangci-lint if available)
	go vet ./...

.PHONY: clean
clean:  ## Remove build artifacts and build cache
	rm -rf bin/
	go clean -cache

.PHONY: help
help:  ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
```

**Explanation:**
`.PHONY` declares targets that are not file names — without it, Make would skip a target if a file with that name existed. `?=` for `VERSION` allows overriding from the command line: `make build VERSION=v2.0.0`. The `2>/dev/null || echo "dev"` fallback handles repositories with no git history.

</details>

---

## Exercise 5: Multi-Stage Dockerfile [🔴 Hard] [3 pts]

### Context
Multi-stage Docker builds are the standard approach for Go containers. This exercise produces a production-quality Dockerfile that creates a minimal final image using `scratch` or `distroless`, with correct layer caching.

### Task
Write a complete `Dockerfile` for the program from Exercise 1 that:
1. Uses `golang:1.22-alpine` as the builder stage
2. Copies `go.mod` and `go.sum` first and runs `go mod download` (for layer caching)
3. Copies the source and builds a static binary with `CGO_ENABLED=0` and stripped symbols (`-s -w`)
4. Creates a second stage from `gcr.io/distroless/static-debian12:nonroot` (or `scratch` with CA certs)
5. Copies only the binary into the final image
6. Sets a non-root user and exposes port 8080

Build the image and verify its size.

### Requirements
- [ ] Two stages: `builder` and a minimal final image
- [ ] `go.mod go.sum` are copied before source for cache efficiency
- [ ] `CGO_ENABLED=0` in the build command
- [ ] Final image contains only the binary (and CA certs if using scratch)
- [ ] Final image runs as non-root
- [ ] `docker images` shows the final image is under 25 MB

### Hints
<details>
<summary>Hint 1</summary>

`gcr.io/distroless/static-debian12:nonroot` already runs as non-root and includes CA certificates and a minimal filesystem. It's simpler than `scratch` for services that need HTTPS. Use `scratch` if you want the absolute minimum and don't need HTTPS calls from inside the container.

</details>

<details>
<summary>Hint 2 (scratch with CA certs)</summary>

To use `FROM scratch` with HTTPS, copy the CA bundle from the builder:
```dockerfile
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
```
Alpine includes this file at `/etc/ssl/certs/ca-certificates.crt`.

</details>

<details>
<summary>Hint 3 (non-root on scratch)</summary>

`scratch` has no `/etc/passwd`, so you cannot use `USER nobody`. Use the numeric UID: `USER 65534:65534` (nobody/nogroup on most Linux systems).

</details>

### Expected Output / Acceptance Criteria
```bash
$ docker build -t myapp:latest .
[+] Building 12.3s

$ docker images myapp
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
myapp        latest    a1b2c3d4e5f6   5 seconds ago   9.2 MB

$ docker run --rm myapp:latest --version
myapp dev (commit: none, built: unknown)
```

### Solution
<details>
<summary>Show Solution</summary>

```dockerfile
# syntax=docker/dockerfile:1

# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM golang:1.22-alpine AS builder

# Install CA certificates (needed to copy into scratch later)
RUN apk add --no-cache ca-certificates

WORKDIR /app

# Copy module files first — this layer is cached until deps change
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build static binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build \
    -ldflags "-s -w" \
    -o /app/myapp .

# ── Stage 2: Minimal final image ─────────────────────────────────────────────
FROM scratch

# CA certificates for outbound HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Only the binary crosses into the final image
COPY --from=builder /app/myapp /myapp

# Run as non-root (65534 = nobody — numeric because scratch has no /etc/passwd)
USER 65534:65534

EXPOSE 8080
ENTRYPOINT ["/myapp"]
```

```bash
docker build -t myapp:latest .
docker images myapp
# REPOSITORY   TAG       IMAGE ID       SIZE
# myapp        latest    ...            ~8-10 MB

docker run --rm myapp:latest --version
# myapp dev (commit: none, built: unknown)
```

**Explanation:**
The builder stage uses Alpine (small but functional) to compile the binary. `go mod download` is on its own layer with only `go.mod`/`go.sum` — Docker caches this layer independently of source changes, so rebuilds skip the module download as long as dependencies don't change. The final `FROM scratch` stage is truly empty: no shell, no `/tmp`, no `/etc`. The binary must be statically compiled (`CGO_ENABLED=0`) or it will fail with "no such file or directory" at runtime because the dynamic linker doesn't exist in the scratch image.

</details>

---

## Exercise 6: GitHub Actions CI Workflow [🔴 Hard] [3 pts]

### Context
A CI workflow that runs on every pull request is the minimum viable quality gate for a professional Go project. This exercise writes the real workflow YAML, with separate jobs for tests, linting, and a two-platform build.

### Task
Write a `.github/workflows/ci.yml` GitHub Actions workflow that:
1. Triggers on `push` to `main` and on `pull_request`
2. Has a `test` job that: checks out the code, sets up Go 1.22, runs `go mod download`, and runs `go test -race -coverprofile=coverage.out ./...`
3. Has a `lint` job that: runs `golangci/golangci-lint-action@v6`
4. Has a `build` job that: depends on `test` and `lint`, runs a matrix for `linux/amd64` and `linux/arm64`, cross-compiles with `CGO_ENABLED=0`, and uploads each binary as an artifact

### Requirements
- [ ] Jobs are independent (`test` and `lint` run in parallel)
- [ ] `build` only runs after both `test` and `lint` pass (`needs: [test, lint]`)
- [ ] The build matrix produces two binaries with distinct names
- [ ] Go version is pinned (not `latest`)
- [ ] Module cache is enabled (`cache: true` in `setup-go`)

### Hints
<details>
<summary>Hint 1</summary>

The `matrix` strategy uses `include:` with explicit objects when you want both `goos` and `goarch` to vary together:
```yaml
strategy:
  matrix:
    include:
      - goos: linux
        goarch: amd64
      - goos: linux
        goarch: arm64
```
Reference them in steps with `${{ matrix.goos }}` and `${{ matrix.goarch }}`.

</details>

<details>
<summary>Hint 2</summary>

Pass `GOOS` and `GOARCH` as step-level environment variables using the `env:` key on the step:
```yaml
- name: Build
  env:
    GOOS: ${{ matrix.goos }}
    GOARCH: ${{ matrix.goarch }}
    CGO_ENABLED: "0"
  run: go build -o myapp-${{ matrix.goos }}-${{ matrix.goarch }} .
```

</details>

### Expected Output / Acceptance Criteria
- The workflow file is valid YAML with correct indentation
- The three jobs are visible in the GitHub Actions UI: `Test`, `Lint`, and `Build (linux/amd64)` / `Build (linux/arm64)`
- A pull request shows all three jobs passing (or failing independently with useful error messages)

### Solution
<details>
<summary>Show Solution</summary>

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # ── Tests with race detector ─────────────────────────────────────────────────
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22"   # pin to a minor version; update deliberately
          cache: true           # caches $GOCACHE and $GOMODCACHE

      - name: Download dependencies
        run: go mod download

      - name: Run tests with race detector
        run: go test -race -coverprofile=coverage.out ./...

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.out

  # ── Lint ─────────────────────────────────────────────────────────────────────
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22"
          cache: true

      - name: Run golangci-lint
        uses: golangci/golangci-lint-action@v6
        with:
          version: latest

  # ── Build matrix ─────────────────────────────────────────────────────────────
  build:
    name: Build (${{ matrix.goos }}/${{ matrix.goarch }})
    runs-on: ubuntu-latest
    needs: [test, lint]   # only build if tests and lint pass
    strategy:
      matrix:
        include:
          - goos: linux
            goarch: amd64
          - goos: linux
            goarch: arm64
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22"
          cache: true

      - name: Build binary
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

**Explanation:**
The three jobs form a dependency graph: `test` and `lint` run in parallel; `build` runs only after both pass. This means a lint failure stops the build from running (wasting CI minutes), but a test failure and a lint failure are reported independently. `cache: true` in `setup-go` uses Actions cache to store the module and build caches between runs — this is the single most impactful performance improvement for Go CI. The `matrix.include` form with explicit pairs ensures `linux/amd64` and `linux/arm64` are the only two combinations, not a full cross-product.

</details>

---

## Exercise 7: govulncheck Audit [🟡 Medium] [2 pts]

### Context
`govulncheck` is the Go team's official tool for scanning a module's dependencies against the Go Vulnerability Database. This exercise runs a real scan on a module with a known-old dependency to observe what a vulnerability finding looks like.

### Task
1. Create a new Go module with `go mod init example.com/vulntest`
2. Add a dependency on an older version of a package known to have had a vulnerability — use `github.com/tidwall/gjson v1.9.0` (which had a ReDoS vulnerability fixed in v1.9.3)
3. Add a minimal `main.go` that imports and calls `gjson.Get`
4. Run `govulncheck ./...` and observe the output
5. Run `go get github.com/tidwall/gjson@latest` to update to the fixed version
6. Run `govulncheck ./...` again and confirm the vulnerability is gone

### Requirements
- [ ] The initial scan with v1.9.0 reports at least one vulnerability
- [ ] The finding includes the CVE/GO identifier, the fixed version, and which call in your code is affected
- [ ] After updating, `govulncheck ./...` reports no vulnerabilities

### Hints
<details>
<summary>Hint 1</summary>

Install `govulncheck` first: `go install golang.org/x/vuln/cmd/govulncheck@latest`. Then run `go get github.com/tidwall/gjson@v1.9.0` to pin the vulnerable version.

</details>

<details>
<summary>Hint 2 (minimal main.go)</summary>

```go
package main

import (
    "fmt"
    "github.com/tidwall/gjson"
)

func main() {
    result := gjson.Get(`{"name":"Alice"}`, "name")
    fmt.Println(result.String())
}
```

</details>

### Expected Output / Acceptance Criteria
```
$ govulncheck ./...
Scanning your code and N packages across M dependent modules for known vulnerabilities...

Vulnerability #1: GO-2021-0085
    ...gjson: ReDoS vulnerability in Get and GetMany functions
    More info: https://pkg.go.dev/vuln/GO-2021-0085
    Module: github.com/tidwall/gjson
      Found in: github.com/tidwall/gjson@v1.9.0
      Fixed in: github.com/tidwall/gjson@v1.9.3
    Call stacks in your code:
        main.go:9:28: main.main calls github.com/tidwall/gjson.Get

1 vulnerability found.

# After `go get github.com/tidwall/gjson@latest`:
$ govulncheck ./...
No vulnerabilities found.
```

### Solution
<details>
<summary>Show Solution</summary>

```bash
# Set up the vulnerable module
mkdir vulntest && cd vulntest
go mod init example.com/vulntest
go get github.com/tidwall/gjson@v1.9.0
```

```go
// main.go
package main

import (
    "fmt"
    "github.com/tidwall/gjson"
)

func main() {
    result := gjson.Get(`{"name":"Alice"}`, "name")
    fmt.Println(result.String())
}
```

```bash
# Run the vulnerability scan
govulncheck ./...
# Vulnerability #1: GO-2021-0085 — ReDoS in gjson.Get
# Found in: github.com/tidwall/gjson@v1.9.0
# Fixed in: github.com/tidwall/gjson@v1.9.3

# Update to fixed version
go get github.com/tidwall/gjson@latest
go mod tidy

# Confirm clean
govulncheck ./...
# No vulnerabilities found.
```

**Explanation:**
`govulncheck` performs call-graph analysis: it only reports vulnerabilities if your code actually calls the vulnerable function (in this case, `gjson.Get`). If you imported gjson but never called the vulnerable function, the output would say "Vulnerability found in dependency (not called from your code)". This precision is what distinguishes `govulncheck` from naive version-based scanners. After updating with `go get ...@latest`, `go mod tidy` cleans up `go.sum` entries for the old version.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Version Flag with ldflags | — | —/1 | — | — |
| Exercise 2 — go vet and Build Tag | — | —/1 | — | — |
| Exercise 3 — Cross-Compile a Binary | — | —/2 | — | — |
| Exercise 4 — Makefile with Build Targets | — | —/2 | — | — |
| Exercise 5 — Multi-Stage Dockerfile | — | —/3 | — | — |
| Exercise 6 — GitHub Actions CI Workflow | — | —/3 | — | — |
| Exercise 7 — govulncheck Audit | — | —/2 | — | — |
| **Total** | | **—/14** | | |

**Passing threshold:** 9/14 (65%). Aim for 12/14 (86%) before taking the test.
