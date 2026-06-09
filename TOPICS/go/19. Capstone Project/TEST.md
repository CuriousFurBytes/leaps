# Test — Module 19: Capstone Project

**Topic:** [[go]]
**Module:** [[go/19. Capstone Project]]

---

## Before You Begin

> [!IMPORTANT]
> This is not a knowledge quiz. It is a **readiness and reflection assessment**.
> You should only attempt this after your project is complete and all milestone
> acceptance criteria have been met.
>
> The purpose is to verify that your project actually does what it is supposed to do,
> and to help you articulate the design decisions you made. Both are skills you need
> to take into production work.

**Instructions:**
1. Have your completed project open alongside this file.
2. Answer each question by examining your actual implementation — not from memory.
3. For reflection questions, answer honestly. There are no wrong answers to "what would you do differently" — only shallow ones.
4. Grade yourself using [ANSWERS.md](./ANSWERS.md) after completing all sections.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Project brief chosen:** ___________
**Project location / repository URL:** ___________
**Start time:** ___________
**End time:** ___________

---

## Scoring Table

| Section | Focus | Points Each | # Questions | Max Points |
|---------|-------|-------------|-------------|------------|
| Section 1: Project Verification | Does it work? | 2 pts | 7 | 14 pts |
| Section 2: Design Justification | Why did you build it this way? | 3 pts | 5 | 15 pts |
| Section 3: Hard Problems | What did you get wrong and fix? | 4 pts | 3 | 12 pts |
| Section 4: Scale and Evolution | What breaks first? | 3 pts | 3 | 9 pts |
| **Total** | | | **18** | **50 pts** |

**Passing score:** 35/50 (70%) — but this module has no grade ceiling. 50/50 means you built a genuinely excellent service.

---

## Section 1: Project Verification (7 questions × 2 pts = 14 pts)

_Run the commands and observe the actual results. Do not answer from memory._

**1.1** Run `go test -race ./...` in your project directory.

- (a) Does it pass? (yes/no)
- (b) What is the reported coverage percentage on your `internal/` packages?
- (c) If any tests fail, describe what fails and why it is failing.

> _Your answer:_

---

**1.2** Run `go vet ./...` and `staticcheck ./...` (or `golangci-lint run`).

- (a) Do both pass cleanly? (yes/no)
- (b) If not, list the issues reported and explain whether they are legitimate problems or false positives.

> _Your answer:_

---

**1.3** Start your service and run the four core operations manually:

```bash
# Adapt the commands to your brief if not using the URL shortener
curl -s -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" -d '{"url":"https://example.com"}'

# Use the code from the response above:
curl -sv http://localhost:8080/<code>      # should redirect (302)
curl -s http://localhost:8080/api/stats/<code>   # should return JSON with hit_count
curl -s -X DELETE http://localhost:8080/api/<code>  # should return 204
```

- (a) Does each operation return the expected status code?
- (b) Does the hit count in the stats response reflect the redirect you just performed?
- (c) Does a request for the stats of the deleted code return 404?

> _Your answer:_

---

**1.4** Start your service, then send SIGINT (`Ctrl+C`). Examine the log output.

- (a) Does the process exit with code 0?
- (b) Do the log lines include "server stopped" or equivalent?
- (c) Describe any error messages that appear during shutdown and whether they are expected.

> _Your answer:_

---

**1.5** Run `docker build -t myservice .` and `docker run --rm -p 8080:8080 myservice`.

- (a) Does the build complete without errors?
- (b) Does the container start and respond to requests?
- (c) What is the final image size (run `docker images myservice`)? Is it reasonable for a compiled Go binary? (A typical Go HTTP service binary is 5–20 MB; a distroless image adds ~3 MB.)

> _Your answer:_

---

**1.6** Open a log output from your running service (either from stdout or a log file).

- (a) Are log lines in structured JSON format?
- (b) Does each access log line include: method, path, status code, and duration?
- (c) If you deliberately cause a 404 (request a non-existent code), does the log line show status 404 with `level:"ERROR"` or `level:"WARN"` (not `level:"INFO"`)?

> _Your answer:_

---

**1.7** Set `PORT=9090` in your environment and start the service.

- (a) Does the service listen on port 9090?
- (b) Now set `DATABASE_URL` to an invalid path. Does the service fail to start with a clear error message (not a panic)?
- (c) Describe exactly where in your code the environment variable override happens.

> _Your answer:_

---

## Section 2: Design Justification (5 questions × 3 pts = 15 pts)

_For each design decision, explain what you chose and why. Reference specific parts of your codebase._

**2.1 Storage Interface Design**

Look at your `Store` interface in `internal/store/store.go` (or equivalent).

- (a) Why did you define the store as an interface rather than using the concrete `*SQLiteStore` (or `*PostgresStore`) directly throughout the codebase?
- (b) What becomes possible because of this interface that would otherwise require code changes?
- (c) Is there any method on your interface that you added partway through and later regretted, or any method you removed? What did you learn from that?

> _Your answer:_

---

**2.2 Error Handling and HTTP Status Code Mapping**

Find your `writeError` function (or equivalent error dispatch logic) in the handler layer.

- (a) How does a `*NotFoundError` originating in the store reach the HTTP response with a 404 status code? Trace the path step by step.
- (b) What would happen if you wrapped the error at each layer but forgot to check for `*NotFoundError` in the handler layer? What would the client receive?
- (c) Why is it important that the 500 error response body does not contain the raw `error.Error()` string from the store layer?

> _Your answer:_

---

**2.3 Context Propagation**

Pick one complete request flow (e.g., `POST /shorten`) and trace how `context.Context` flows from the incoming HTTP request to the database query.

- (a) Where is the context created? (It comes from `r.Context()` in the handler — but where does that context originate?)
- (b) At what point does the `TimeoutMiddleware` modify the context, and how does the modified context reach the database layer?
- (c) What happens at the database layer if the client disconnects mid-request and the context is cancelled? Walk through the behavior, not just the theory.

> _Your answer:_

---

**2.4 Test Strategy**

Look at your test files.

- (a) Your handler tests use a real SQLite `:memory:` store. Why did you make this choice instead of writing a mock `Store` implementation?
- (b) Are there any scenarios your current test suite does not cover that you would add in a follow-up? Name at least two.
- (c) If you had to add a second `Store` implementation (e.g., a Postgres store), would your existing handler tests still work unchanged? Why or why not?

> _Your answer:_

---

**2.5 Graceful Shutdown**

Describe your graceful shutdown implementation.

- (a) What is the maximum time the shutdown procedure will take in your implementation?
- (b) What happens to a request that is in the middle of a long database query when SIGTERM arrives?
- (c) Is there anything your current shutdown procedure does not clean up correctly? (Be honest — most first implementations have at least one gap.)

> _Your answer:_

---

## Section 3: Hard Problems (3 questions × 4 pts = 12 pts)

_These questions ask about challenges, failures, and recovery. Shallow answers score 0._

**3.1 The Hardest Bug**

Describe the most difficult bug you encountered during this build.

- (a) What was the symptom? (What did you observe?)
- (b) What did you initially think was wrong?
- (c) What was actually wrong?
- (d) How did you find it? (print statements, the debugger, `go test -race`, reading the Go spec, etc.)
- (e) What would you do differently next time to avoid or find this kind of bug faster?

> _Your answer (aim for at least 150 words):_

---

**3.2 A Design Decision You Would Change**

Look at your code honestly. Find one design decision that felt right when you made it but that you would make differently if you started over.

- (a) What is the decision? (Be specific — name the file and the type/function involved.)
- (b) Why did it seem like a good idea at the time?
- (c) Why would you change it?
- (d) What would you do instead?

> _Your answer:_

---

**3.3 Concurrency and Data Safety**

- (a) Are there any places in your code where two goroutines could access the same memory simultaneously? Describe where, and explain how your code prevents a data race.
- (b) If you ran `go test -race ./...` and it reported a data race, describe what it was and how you fixed it. If no race was reported, explain why concurrent access is safe in your implementation.
- (c) What is the difference between thread safety at the HTTP server level (Go's `http.Server` handles each request in a goroutine) and thread safety at the store level? How does your store address this?

> _Your answer:_

---

## Section 4: Scale and Evolution (3 questions × 3 pts = 9 pts)

_These are open-ended design questions. There is no single correct answer. Show your reasoning._

**4.1 Under 10x Load**

Your service currently handles requests adequately on a single machine. Suppose it needed to handle 10 times more traffic.

- (a) What is the first component in your implementation that would fail or degrade under this load? How do you know?
- (b) What would you change to address that bottleneck?
- (c) What new problems would your change introduce?

> _Your answer:_

---

**4.2 Adding a New Feature**

A product manager asks you to add "custom short codes" — instead of a randomly generated code, the user can request a specific code (e.g., `/shorten` with `{"url":"https://example.com", "custom_code":"mycode"}`).

- (a) Which part of your current implementation needs to change?
- (b) What new error condition arises, and how does your current error handling design accommodate it?
- (c) What test cases would you add?

> _Your answer:_

---

**4.3 Production Readiness Assessment**

Rate your implementation on a scale of 1 (prototype) to 5 (production-ready) in each category, and justify each rating with a specific observation about your code.

| Category | Rating (1–5) | Justification |
|----------|-------------|---------------|
| Error handling | | |
| Observability (logging/metrics) | | |
| Security | | |
| Test coverage | | |
| Operational runbook (README quality) | | |

For the lowest-rated category: what is the most important thing you would add to raise it by one point?

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What aspect of this project am I most proud of?**
> _Your reflection:_

**What aspect of this project am I least satisfied with?**
> _Your reflection:_

**If I were to spend one more week on this project, what would I focus on first and why?**
> _Your reflection:_

**How has building this project changed how I think about Go, compared to when I started Module 0?**
> _Your reflection (aim for at least 3 sentences):_

---

## Grading Record

_Append a new row each time you grade this assessment. Do not overwrite previous attempts._

| Date | S1 (14) | S2 (15) | S3 (12) | S4 (9) | Total (50) | Notes |
|------|---------|---------|---------|--------|-----------|-------|
| — | — | — | — | — | —/50 | First self-assessment |

**Grade scale:** A ≥ 90% (≥45/50) &nbsp;·&nbsp; B ≥ 80% (≥40/50) &nbsp;·&nbsp; C ≥ 70% (≥35/50) &nbsp;·&nbsp; D ≥ 60% (≥30/50) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the evaluation rubric. Review it only after completing this assessment._
