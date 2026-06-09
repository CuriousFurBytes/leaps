# Test — Module 18: Build, Tooling, and Deployment

**Topic:** [[go]]
**Module:** [[go/18. Build, Tooling, and Deployment]]

---

## Before You Begin

> [!WARNING]
> **Do not look at ANSWERS.md or your notes during the test.**
> The purpose of this test is to surface what you truly know vs. what you think you know.
> An inflated score is worthless. An honest score shows you exactly where to focus next.

**Instructions:**
1. Close all notes, the module README, and any reference materials.
2. Set a timer. Note your start time below.
3. Attempt every question — partial credit exists.
4. After finishing, grade yourself using ANSWERS.md.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Start time:** ___________
**End time:** ___________
**Total time:** ___________

---

## Scoring Table

| Section | Question Type | Points Each | # Questions | Max Points |
|---------|--------------|-------------|-------------|------------|
| Section 1: Recall | Easy | 1 pt | 5 | 5 pts |
| Section 2: Conceptual | Medium | 2 pts | 3 | 6 pts |
| Section 3: Applied | Hard | 3 pts | 2 | 6 pts |
| Section 4: Scenario | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** What does the `-ldflags "-X pkg.Var=value"` flag do, and what type must `Var` be for this to work?

> _Your answer:_

---

**1.2** What environment variables do you set to cross-compile a Go binary for Linux on a macOS machine?

> _Your answer:_

---

**1.3** What does `CGO_ENABLED=0` do, and why is it necessary when building a Go binary for a `FROM scratch` Docker container?

> _Your answer:_

---

**1.4** What Go command do you run to check for known security vulnerabilities in your module's dependencies?

> _Your answer:_

---

**1.5** In a multi-stage Dockerfile for a Go service, why should you copy `go.mod` and `go.sum` and run `go mod download` *before* copying the rest of the source code?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain what a build constraint (`//go:build`) is and give two concrete use cases where you would use one. Explain how file name conventions (e.g., `signal_linux.go`) relate to build constraints.

> _Your answer:_

---

**2.2** Describe the purpose of `go.sum` in the Go module system. What attack does it prevent? What is the role of the checksum database (`sum.golang.org`) in this security model?

> _Your answer:_

---

**2.3** Explain the difference between `go vet`, `staticcheck`, and `golangci-lint`. When would you use each? Why is running all three in CI better than running just one?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write the `go build` command(s) that produce a release binary for Linux/amd64 with the following properties:
- Fully static (no shared library dependencies)
- Debug symbols stripped
- Version variable `github.com/acme/myapp/internal/version.Version` set to `v2.1.0`
- Commit variable `github.com/acme/myapp/internal/version.Commit` set to the current git commit hash (show the shell substitution)
- Output binary named `myapp-linux-amd64`

> _Your answer:_

---

**3.2** Write a GitHub Actions workflow job named `test` that:
- Triggers as part of a workflow that runs on `push` to `main` and on `pull_request`
- Checks out code with `actions/checkout@v4`
- Sets up Go 1.22 with module caching enabled
- Runs `go test -race -coverprofile=coverage.out ./...`

Include the full YAML for just this job (not the full workflow file).

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A developer reports the following:

> "I built our Go service on my Mac and it ran fine locally. I built it again with `GOOS=linux GOARCH=amd64 go build -o server .` and pushed the `server` binary into our `FROM scratch` Docker image. When the container starts, it crashes immediately with:
> `standard_init_linux.go:228: exec user process caused: no such file or directory`"

Identify:

a) What is the root cause of this error?

b) What single environment variable was missing from the `go build` command?

c) How would you verify that the fix worked before pushing to the container registry?

d) The developer also mentions their service makes outbound HTTPS calls to a third-party API. They switch to `FROM scratch` but now the HTTPS calls fail with certificate errors. What is missing and how do you fix it?

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "A CI pipeline for a Go service should run at least three separate jobs: one for tests, one for linting, and one for building." Explain why separating these into three jobs (rather than one sequential job) is better practice. Consider: parallelism, failure isolation, feedback speed, and what each job's failure tells you about the codebase.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Write a complete `.goreleaser.yml` configuration file for a Go project at `github.com/acme/myapp` that:
- Builds for `linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`, and `windows/amd64`
- Disables CGO for all builds
- Stamps `Version`, `Commit`, and `BuildDate` into `github.com/acme/myapp/internal/version` variables
- Strips symbols (`-s -w`)
- Produces `.tar.gz` archives (`.zip` for Windows)
- Generates a `checksums.txt` file
- Runs `go mod tidy` as a pre-hook

Explain in a comment or annotation what command you would run to test this configuration locally without publishing a release.

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the capstone project?**
> _Your reflection:_

**What score did I get? Do I feel it accurately reflects my understanding?**
> _Your reflection:_

---

## Grading Record

_Append a new row each time you take this test. Do not overwrite previous attempts._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
