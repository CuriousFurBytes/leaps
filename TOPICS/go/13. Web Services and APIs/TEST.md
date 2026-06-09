# Test — Module 13: Web Services and APIs

**Topic:** [[go]]
**Module:** [[go/13. Web Services and APIs]]

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

**1.1** What is the `http.Handler` interface? Write its method signature from memory.

> _Your answer:_

---

**1.2** In Go 1.22, what is the pattern string syntax for registering a route that handles only `GET` requests to `/items/{id}`? What function do you call inside the handler to retrieve the value of `id`?

> _Your answer:_

---

**1.3** When must you call `w.Header().Set("Content-Type", "application/json")` relative to calling `w.WriteHeader(status)` or writing the body? Why?

> _Your answer:_

---

**1.4** What is the role of `http.MaxBytesReader`? What error type does it produce when the limit is exceeded, and how do you detect it?

> _Your answer:_

---

**1.5** Name the three timeout fields on `http.Server` that you should always configure in production, and briefly describe what each one covers.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain the middleware pattern in Go. What is the signature of a middleware function? Walk through how `WithLogging(WithRequestID(mux))` creates a middleware chain, and explain in what order the "before" and "after" phases of each middleware execute relative to the handler.

> _Your answer:_

---

**2.2** Explain why a production service should configure an explicit `http.Server` struct rather than using `http.ListenAndServe(addr, handler)` directly. Cover at least two concrete risks of using `http.ListenAndServe` without timeout configuration.

> _Your answer:_

---

**2.3** Describe the graceful shutdown sequence using `signal.NotifyContext` and `srv.Shutdown(ctx)`. What does `srv.Shutdown` do that distinguishes it from simply killing the process? Why do you need a fresh context (not the signal context) for the shutdown call?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go function `handleCreateProduct(w http.ResponseWriter, r *http.Request)` that:
- Limits the request body to 256 KB
- Decodes a JSON body into a struct with `name string` (required) and `price float64` (must be > 0)
- Returns appropriate JSON error responses for: empty body (400), invalid JSON (400), missing name (422), non-positive price (422)
- On success returns `201 Created` with the decoded struct as JSON
- Sets `Content-Type: application/json` on all responses

You may define any helper types or functions you need.

> _Your answer:_

---

**3.2** Write a `TestHandleCreateProduct` test function using `httptest.NewRecorder` and `httptest.NewRequest` that covers at least four distinct cases (valid input, empty body, missing name, non-positive price). Use table-driven test structure.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague writes the following handler and notices that clients sometimes receive garbled responses — the body is correct JSON but the HTTP status code is always 200, even when an error occurred. They also notice that `Content-Type` is sometimes missing from the response. Identify all bugs, explain why each one causes the observed symptom, and rewrite the handler correctly.

```go
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    user, err := userStore.Get(r.Context(), id)
    if err != nil {
        w.WriteHeader(http.StatusNotFound)
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"error": "user not found"})
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}
```

a) Identify and explain every bug.

b) Rewrite the handler correctly.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "With Go 1.22, you no longer need a third-party router for most Go services." Evaluate this claim. Describe at least two scenarios where the Go 1.22 stdlib mux is sufficient and at least two scenarios where you might still reach for a third-party router such as chi or gin. What is the cost of each choice?

> _Your answer (aim for 4–8 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Write a `statusRecorder` type that wraps `http.ResponseWriter` and captures the HTTP status code written by a handler. Implement:
- The `statusRecorder` struct with an embedded `http.ResponseWriter` and an integer `code` field
- A `WriteHeader(code int)` method that stores the code and delegates to the embedded writer
- A `Write(b []byte)` method that sets `code` to 200 (the implicit default) if `WriteHeader` was never called, then delegates

Then write a `WithLogging` middleware that uses `statusRecorder` to log `METHOD /path STATUS duration` (e.g., `GET /items/1 200 142µs`) after every request.

Include a test showing that: a 404-returning handler produces a log entry with `404`, and a 200-returning handler produces a log entry with `200`.

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the next module?**
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
