# Questions — Module 18: Build, Tooling, and Deployment

> Log questions as they arise — don't wait until you understand them fully.
> A question written down is a learning opportunity captured.
> For big-picture questions about the whole topic, use the topic-level QUESTIONS.md instead.

---

## How to Use This File

1. Write the question the moment it occurs to you, even if you can't articulate it well yet.
2. Come back and refine the question once you understand it better.
3. Update the status as you research or find answers.
4. Link to the source where you found the answer.
5. Capture follow-up questions — good answers always raise new ones.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Unanswered — needs active research |
| 🟡 | Partial — have some understanding, still incomplete |
| 🟢 | Answered — well understood, could explain to someone else |
| ⏸ | Deferred — not urgent, revisit in a later module |

---

## Question Format

```markdown
### Q{{N}}: {{SHORT_QUESTION_TITLE}}

**Asked:** {{YYYY-MM-DD}}
**Status:** 🔴 Unanswered

**Full question:**
The complete question with all relevant context.

**My current hypothesis:**
What you think the answer might be, even if speculative.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Where you found or verified the answer_

**Follow-up questions:**
- _New questions this answer raised_
```

---

## Questions

### Q001: What is the difference between `go build ./...` and `go build .`?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README uses `go build .` to build the current package. But I've seen `go build ./...` in many real-world projects. Do they produce different outputs? Specifically:

- Does `./...` attempt to build all packages in the module, including packages that are not `main` packages and therefore produce no binary output?
- If I have both `./cmd/server` and `./cmd/cli` in my module, does `go build ./...` build both binaries, and where does it put them?

**My current hypothesis:**
I think `go build .` compiles the current directory's package. `go build ./...` compiles all packages recursively, but only actually writes binaries for `main` packages — library packages are compiled for checking but produce no output file. I suspect `go build ./...` puts binaries in the current directory named after the package, while `go install ./...` puts them in `$GOBIN`.

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Check `go help build` and `go help packages` for the `./...` pattern semantics_

**Follow-up questions:**
- Does `go build ./...` fail fast on the first package error, or does it attempt to build all packages and collect all errors?
- Is there a way to build all `main` packages in a module to a specific output directory in a single command?

---

### Q002: Does `govulncheck` scan only directly called functions, or all functions in vulnerable packages?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The module README says govulncheck "reports only vulnerabilities that your code actually calls." But I'm not sure what "calls" means precisely:

1. If my code calls function A in package P, and A internally calls the vulnerable function B in the same package P, does govulncheck consider me affected?
2. If I import a package for one purpose but that package contains a vulnerable function I never import or call, is the vulnerability reported?

**My current hypothesis:**
I think govulncheck does call-graph analysis: it traces from your entry points (`main`, exported functions, test functions) through the call graph and reports only if a path exists from your code to the vulnerable symbol. Transitive calls (A calls B which calls the vulnerable function) would still be reported as affected. Packages that are imported but whose vulnerable code is never reachable would be marked as "informational" rather than "actively vulnerable."

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_Check go.dev/security/vuln and the govulncheck documentation for the call-graph analysis description_

**Follow-up questions:**
- Does govulncheck handle vulnerabilities in the Go standard library (not just third-party modules)?
- How does govulncheck handle interface dispatch — if the vulnerable code is called through an interface, does it still detect the call?

---

_Add new questions below this line. Keep them numbered sequentially._

---

## Resolved Questions Archive

_Move fully answered 🟢 questions here to keep the active list clean._

_(none yet)_

---

## Question Stats

| Status | Count |
|--------|-------|
| 🔴 Unanswered | 2 |
| 🟡 Partial | 0 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **2** |
