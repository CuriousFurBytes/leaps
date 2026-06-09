# Answer Key — Module 18: Build, Tooling, and Deployment

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with the book closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Copied text without understanding (you'll know)
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — `-ldflags "-X pkg.Var=value"` [1 pt]

**Full credit answer:**
The `-X` linker flag injects a string value into a named package-level variable at link time — without recompiling the source file that declares the variable. The variable must be of type `string`; the flag does not work with `int`, `bool`, or any other type. The full flag syntax is `-ldflags "-X 'importpath.VariableName=value'"` where `importpath` is the full module-qualified import path (e.g., `github.com/acme/myapp/internal/version`). For variables in `package main`, the import path is `main`.

**Key points required:**
- Injects at link time (not compile time — no source change)
- Only works for `string` variables
- Requires the full import path, not just the variable name

**Common wrong answers:**
- *"Sets an environment variable at runtime"* — No; this happens at link time and is baked into the binary
- *"Uses the short package name like `-X version.Version=...`"* — The full import path is required

---

### 1.2 — Environment variables for cross-compilation [1 pt]

**Full credit answer:**
Set `GOOS=linux` (target operating system) and `GOARCH=amd64` (target architecture). On macOS, these are set as environment variable prefixes before `go build`:
```bash
GOOS=linux GOARCH=amd64 go build -o myapp-linux .
```
For container deployments, add `CGO_ENABLED=0` to disable cgo and produce a fully static binary.

**Key points required:**
- `GOOS=linux`
- `GOARCH=amd64`

**Bonus credit:** Also mentioning `CGO_ENABLED=0` for container readiness.

---

### 1.3 — `CGO_ENABLED=0` and scratch containers [1 pt]

**Full credit answer:**
`CGO_ENABLED=0` disables Go's cgo feature, which allows Go code to call C libraries. By default, some standard library packages (notably `net` and `os/user` on Linux) use cgo and link dynamically against glibc (`libc.so.6`). A `FROM scratch` Docker image is completely empty — there is no filesystem, no shell, and no dynamic linker. A binary that requires glibc will fail at runtime with "no such file or directory" because the dynamic linker (`/lib64/ld-linux-x86-64.so.2`) doesn't exist. With `CGO_ENABLED=0`, the Go binary is fully self-contained: it has no external shared library dependencies and can run in a scratch container.

**Key points required:**
- `CGO_ENABLED=0` disables cgo and produces a static binary
- Static binary has no shared library dependencies
- `FROM scratch` has no dynamic linker, so a dynamically-linked binary fails to start

---

### 1.4 — Scanning for known vulnerabilities [1 pt]

**Full credit answer:**
`govulncheck ./...` — the official Go vulnerability scanner developed by the Go security team. It scans the module's dependency graph against the Go Vulnerability Database at `vuln.go.dev` and reports only vulnerabilities that are reachable from your code (not all vulnerabilities in all dependencies regardless of usage).

**Key points required:**
- Command: `govulncheck`
- Must be installed first: `go install golang.org/x/vuln/cmd/govulncheck@latest`

---

### 1.5 — Layer ordering in Dockerfile [1 pt]

**Full credit answer:**
Docker builds layer by layer and caches each layer. If the inputs to a layer haven't changed since the previous build, Docker reuses the cached layer without re-running the command. `go mod download` is slow (downloads potentially hundreds of megabytes) but only needs to re-run when dependencies change — i.e., when `go.mod` or `go.sum` change. Source code, on the other hand, changes on every commit. If you copy the source before `go mod download`, any source change invalidates the module download layer and forces a full re-download. By copying `go.mod go.sum` first and running `go mod download` before copying the source, the module download layer is only invalidated when dependencies actually change — which is rare. Most builds reuse the cached download layer and only re-run the `go build` layer.

**Key points required:**
- Docker caches layers; invalidation propagates downward
- `go mod download` is slow and should be cached
- Source changes are frequent; dependency changes are rare
- Correct order: `COPY go.mod go.sum` → `go mod download` → `COPY . .` → `go build`

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Build constraints [2 pts]

**Full credit answer:**
A build constraint (or build tag) is a directive at the top of a `.go` file that controls whether that file is included in the compilation. The syntax is `//go:build <expression>` on the first non-blank line before the `package` clause. The expression supports `&&`, `||`, `!`, and parentheses using standard Go boolean syntax.

**Two concrete use cases:**
1. Platform-specific code: `//go:build linux` — include a file only on Linux (e.g., a file using Linux-specific syscalls like `ioctl`)
2. Optional features: `//go:build integration` — include integration test files only when running `go test -tags integration ./...`, keeping unit tests fast

**File name conventions** are an implicit form of build constraints: `_linux.go`, `_windows.go`, `_amd64.go` suffixes cause the Go toolchain to apply the corresponding constraint automatically without a `//go:build` directive. The file name constraint and the `//go:build` directive can be combined (both must be satisfied for the file to be included).

**Rubric:**
- 2 pts: Correct syntax explanation, two concrete use cases, and explains file name conventions
- 1 pt: Correct syntax and at least one use case, but file name conventions missing or incorrect
- 0 pts: Confuses build constraints with `runtime.GOOS` checks at runtime

---

### 2.2 — `go.sum` and the checksum database [2 pts]

**Full credit answer:**
`go.sum` is a file that records cryptographic hashes (SHA-256) for every version of every dependency module (both the module zip and the `go.mod` file). When the Go toolchain downloads a dependency, it verifies the downloaded content's hash matches the hash in `go.sum`. If they don't match, the build fails.

**The attack it prevents:** Dependency substitution. Without `go.sum`, an attacker who controls a module's hosting (e.g., a compromised GitHub account) could silently replace the content of a specific version with malicious code. The hash in `go.sum` pins the exact bit-for-bit content that was present when the dependency was first added to the module.

**The role of `sum.golang.org`:** The checksum database is a public, append-only, cryptographically verifiable log (based on a transparency tree) that records the hash of every module version ever fetched through the Go module proxy. When `go.sum` entries are first created (on `go mod tidy` or `go get`), the Go toolchain submits the hash to the checksum database and verifies it against any previously recorded hash. This prevents an attacker from targeting a specific user or organization with a different module version — the hash is globally consistent.

**Rubric:**
- 2 pts: Correctly describes `go.sum` as a hash file, names the substitution attack, and explains the checksum database's role as a global consistency check
- 1 pt: Correctly describes `go.sum` as a hash file but doesn't explain the attack or the checksum database's role
- 0 pts: Confuses `go.sum` with `go.mod` or describes it as a dependency list

---

### 2.3 — go vet vs staticcheck vs golangci-lint [2 pts]

**Full credit answer:**
- **`go vet`** is the built-in static analyzer that ships with the Go toolchain. It runs a small, focused set of checks that catch common bugs: mismatched `Printf` format strings, unreachable code, incorrect mutex copies, suspicious composite literals, etc. It produces zero false positives by design — everything it reports is a real bug.

- **`staticcheck`** is a standalone tool by Dominik Honnef that runs a much larger set of analyses, including: unused code, redundant code, deprecated API usage, suspicious code patterns, and more. It has both "certain bugs" checks (SA category) and "style/simplification" checks (S category).

- **`golangci-lint`** is a meta-linter that aggregates many linters (including `go vet` and `staticcheck`, plus `errcheck`, `revive`, `gosec`, and ~50 others) behind a single binary and a single configuration file (`.golangci.yml`). It runs linters in parallel, deduplicates findings, and provides a consistent interface for CI.

**Why all three in CI:** `go vet` catches the highest-confidence bugs with zero false positives — run it first because it's fast. `staticcheck` catches a broader class of real issues that `vet` misses. `golangci-lint` (which includes both) adds domain-specific checks (security via `gosec`, error handling via `errcheck`) that neither standalone tool covers. In practice, most teams use only `golangci-lint` in CI because it subsumes the others.

**Rubric:**
- 2 pts: Correctly distinguishes all three tools, explains the scope difference, and gives a coherent rationale for using them
- 1 pt: Correct on two tools, shaky or missing on the third, or correct descriptions but no rationale
- 0 pts: Confuses the tools or states they are interchangeable

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Cross-compile release build command [3 pts]

**Full credit answer:**
```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
  go build \
  -ldflags "-s -w \
            -X 'github.com/acme/myapp/internal/version.Version=v2.1.0' \
            -X 'github.com/acme/myapp/internal/version.Commit=$(git rev-parse --short HEAD)'" \
  -o myapp-linux-amd64 .
```

**Key elements for full credit:**
- `CGO_ENABLED=0` — static binary
- `GOOS=linux GOARCH=amd64` — correct cross-compile target
- `-ldflags "-s -w"` — strip symbols
- `-X '...version.Version=v2.1.0'` — correct full import path, string value
- `-X '...version.Commit=$(git rev-parse --short HEAD)'` — shell substitution for commit hash
- `-o myapp-linux-amd64` — correct output name

**Rubric:**
- 3 pts: All six elements present and correct
- 2 pts: Four or five elements correct; one or two missing (e.g., missing `-s -w`, or short import path)
- 1 pt: Correct general structure but wrong import path or missing `CGO_ENABLED=0`
- 0 pts: Fundamentally wrong command

**Common wrong answers:**
- `-X 'version.Version=v2.1.0'` — short path silently does nothing; must be the full import path
- `GOOS=linux64` — not a valid `GOOS` value; correct value is `linux`

---

### 3.2 — GitHub Actions `test` job YAML [3 pts]

**Full credit answer:**
```yaml
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22"
          cache: true

      - name: Download dependencies
        run: go mod download

      - name: Run tests with race detector
        run: go test -race -coverprofile=coverage.out ./...
```

**Key elements for full credit:**
- Correct YAML indentation (job under `jobs:`, steps under `steps:`)
- `actions/checkout@v4`
- `actions/setup-go@v5` with `go-version: "1.22"` and `cache: true`
- `go mod download` step (optional but correct)
- `go test -race` with the `-race` flag
- `./...` pattern to test all packages

**Rubric:**
- 3 pts: All elements present, correct YAML syntax, `-race` flag included, Go version pinned
- 2 pts: Correct structure and most elements, but missing `cache: true` or using `latest` for Go version
- 1 pt: Mostly correct but missing `-race` flag or has significant YAML indentation issues
- 0 pts: Not valid YAML or fundamentally wrong structure

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Container startup crash debugging [3 pts] (1 pt per part a–c, combined d)

**(a) Root cause:**
The binary was built with `CGO_ENABLED=1` (the default), which causes Go to link the binary dynamically against glibc (`libc.so.6`). The `FROM scratch` image contains no filesystem at all — no dynamic linker, no libc, no shared libraries. When the container runtime tries to execute the binary, the kernel attempts to locate the dynamic linker (typically `/lib64/ld-linux-x86-64.so.2`), finds nothing, and reports "no such file or directory". This is not a missing *application* file — it's a missing *dynamic linker*.

**(b) Missing environment variable:**
`CGO_ENABLED=0`. The corrected command is:
```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server .
```

**(c) Verification:**
Run `ldd server` on a Linux host or inside a container. For a static binary, the expected output is:
```
not a dynamic executable
```
If you see entries like `linux-vdso.so.1` or `libc.so.6`, the binary is still dynamically linked.

**(d) HTTPS and CA certificates in scratch:**
`FROM scratch` has no filesystem, including no CA certificate bundle. HTTPS calls fail because Go's TLS stack cannot verify the server's certificate chain — there is no root CA store to look up. The fix is to copy the CA certificates from the builder stage:
```dockerfile
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
```
Alpine Linux includes the CA bundle at that path after running `apk add --no-cache ca-certificates`. Alternatively, use `gcr.io/distroless/static-debian12` as the base image, which includes CA certificates by default.

**Rubric:**
- 1 pt for (a): Correctly identifies that the binary is dynamically linked and that `FROM scratch` lacks the dynamic linker
- 1 pt for (b) and (c) combined: Names `CGO_ENABLED=0` as the fix and `ldd` as the verification tool
- 1 pt for (d): Correctly identifies missing CA certificates as the HTTPS failure cause and provides the correct fix (copy certs from builder or use distroless)

---

## Section 5: Discussion — Answer Key

### 5.1 — Three separate CI jobs vs one sequential job [2 pts]

**Example strong answer:**
Separating CI into three jobs — test, lint, and build — provides three distinct benefits. First, **parallelism**: since test and lint have no dependency on each other, they run simultaneously, cutting total CI wall time in half compared to sequential execution. Second, **failure isolation**: if lint fails, you know immediately that it's a code style or static analysis issue — not a test failure. This tells you exactly what kind of problem to fix without needing to scan through interleaved output. Third, **feedback speed**: a lint failure is typically faster to identify than a test failure (no test compilation or test runtime needed), so the developer gets signal in 30 seconds instead of 3 minutes. Fourth, **conditional builds**: the build job can depend on both test and lint passing (`needs: [test, lint]`), so you never waste CI resources building a binary that would be rejected anyway. Each job's failure has a specific meaning: test failure means bugs; lint failure means code quality; build failure means cross-compilation or linker issues.

**Elements that earn full credit:**
- Correctly names parallelism as the first benefit
- Distinguishes the failure signal from each job type
- Mentions `needs:` for conditional execution
- Discusses feedback speed or developer ergonomics

**Rubric:**
- 2 pts: Addresses at least three of the four dimensions (parallelism, failure isolation, feedback speed, conditional execution) with specific reasoning
- 1 pt: Correctly identifies parallelism and failure isolation but doesn't address feedback speed or conditional execution
- 0 pts: Claims there is no benefit to separation, or shows a fundamental misunderstanding of CI concepts

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Complete `.goreleaser.yml` [+5 pts]

**Full credit answer:**
```yaml
# .goreleaser.yml
project_name: myapp

before:
  hooks:
    - go mod tidy   # ensure go.sum is current before release

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
    # Exclude windows/arm64 (uncommon target)
    ignore:
      - goos: windows
        goarch: arm64
    ldflags:
      - -s -w
      - -X github.com/acme/myapp/internal/version.Version={{.Version}}
      - -X github.com/acme/myapp/internal/version.Commit={{.Commit}}
      - -X github.com/acme/myapp/internal/version.BuildDate={{.Date}}

archives:
  - format: tar.gz
    name_template: "{{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}"
    format_overrides:
      - goos: windows
        format: zip

checksum:
  name_template: "checksums.txt"   # SHA256 checksums for all release artifacts

changelog:
  sort: asc
  filters:
    exclude:
      - "^docs:"
      - "^test:"
      - "^chore:"
```

**Local test command (no publishing):**
```bash
# Test the release locally without creating a GitHub Release
goreleaser release --snapshot --clean
# --snapshot: uses a fake version; does not tag or publish
# --clean:    removes the dist/ directory before starting
```

**Key elements for full credit:**
- All five platforms present (linux/amd64, linux/arm64, darwin/amd64, darwin/arm64, windows/amd64)
- `CGO_ENABLED=0` in `env`
- All three `-X` ldflags with GoReleaser template variables (`{{.Version}}`, `{{.Commit}}`, `{{.Date}}`)
- `-s -w` in ldflags
- Archives with format overrides (zip for Windows)
- `checksums.txt` entry
- `go mod tidy` pre-hook
- `goreleaser release --snapshot --clean` for local testing

**Rubric:**
- 5 pts: All elements correct and local test command included with explanation
- 3 pts: Correct structure and most elements; missing one or two (e.g., no format override, or missing one ldflag)
- 1 pt: Correct general structure but significant gaps (wrong GoReleaser template syntax, missing platforms)
- 0 pts: Not a valid GoReleaser configuration

---

## Common Wrong Answers Across the Test

1. **Short import path in `-X` flag** — The most frequent error: writing `-X 'version.Version=...'` instead of `-X 'github.com/acme/myapp/internal/version.Version=...'`. There is no compile or link error — the variable silently retains its default value. Students who make this mistake need to test with `--version` flag and trace back why the output still says "dev".

2. **Omitting `CGO_ENABLED=0` for cross-compilation** — Students who cross-compile but forget `CGO_ENABLED=0` produce a valid Linux ELF binary, but it may be dynamically linked. The error only surfaces at runtime in a scratch container. The diagnostic step (`ldd binary`) is critical to include in any deployment workflow.

3. **Docker layer ordering** — Students who put `COPY . .` before `go mod download` get a working Dockerfile but one with poor cache behavior. This is a correctness vs performance distinction: the build works either way, but only the correct order is efficient. Accepting both orderings but marking down cache-inefficient variants is appropriate.

4. **`go vet`, `staticcheck`, and `golangci-lint` treated as interchangeable** — All three catch bugs, but at different levels of coverage and specificity. `golangci-lint` subsumes the others in CI, but understanding why each exists requires knowing what each one does independently.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who score below 12/22 on this module are likely missing foundational knowledge from [[go/7. Packages and Modules]] — specifically around `go.mod`, `go.sum`, and how the module proxy works. Send them back to that module before the capstone.
- Section 4 (the Docker crash scenario) is the most diagnostic question in the test. A student who can correctly diagnose the crash (CGO_ENABLED=0), verify it (ldd), and explain the CA certificate issue is genuinely ready for production Go deployment.
- The bonus question tests GoReleaser-specific knowledge that most students won't have unless they've used it. Score it generously — the key skill being tested is knowing that the variables use `{{.Version}}` template syntax, not `$(git describe)` shell syntax.
- Students who struggle with Section 3.2 (the GitHub Actions YAML) often have YAML indentation errors. Remind them that YAML indentation must be consistent (2 spaces) and that the `jobs:` key is at the top level of the workflow file.

---

## Grading Records

_Append a new row each time you grade a test attempt. Do not overwrite previous records._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | — |
