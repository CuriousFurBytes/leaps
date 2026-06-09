# Questions — Module 13: Web Services and APIs

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

### Q001: How does Go 1.22 mux handle trailing-slash matching?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
In many routing libraries, `/items` and `/items/` are treated as different paths, and a trailing-slash redirect is common. How does the Go 1.22 `http.ServeMux` handle this? If I register `"GET /items"`, does a request to `/items/` match, fail with 404, or redirect?

Relatedly, if I register `"GET /items/"` (with trailing slash), does that act as a subtree prefix match — matching `/items/`, `/items/42`, `/items/42/tags`, etc.?

**My current hypothesis:**
I believe a trailing slash in the pattern makes it a subtree prefix (matching anything under that path), consistent with the pre-1.22 mux behaviour. A pattern without a trailing slash is an exact match. A request to `/items/` when only `/items` is registered probably returns 301 Redirect or 404 — I haven't confirmed which.

**Answer:**
_To be filled in — check https://pkg.go.dev/net/http#ServeMux and the Go 1.22 routing blog post_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does `{id}` match an empty segment (e.g., `/items/` with no value after the slash)?
- Can I disable the subtree behaviour for a specific pattern?

---

### Q002: How do I capture the response status code in a logging middleware?

**Asked:** YYYY-MM-DD
**Status:** 🔴 Unanswered

**Full question:**
The logging middleware in the module logs the method, path, and duration but not the HTTP status code returned. To log the status code, you need to intercept the `WriteHeader` call. `http.ResponseWriter` doesn't expose the status code after the fact. 

What is the idiomatic Go pattern for wrapping `http.ResponseWriter` to capture the status code?

**My current hypothesis:**
I think you create a custom struct that embeds `http.ResponseWriter` and overrides `WriteHeader` to store the code:

```go
type statusRecorder struct {
    http.ResponseWriter
    code int
}

func (sr *statusRecorder) WriteHeader(code int) {
    sr.code = code
    sr.ResponseWriter.WriteHeader(code)
}
```

Then in the middleware:
```go
rec := &statusRecorder{ResponseWriter: w, code: http.StatusOK}
next.ServeHTTP(rec, r)
log.Printf("%d %s %s", rec.code, r.Method, r.URL.Path)
```

But I'm not sure if this handles all cases — e.g., what if the handler never calls WriteHeader (implicit 200)?

**Answer:**
_To be filled in_

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Does the same wrapper need to intercept `Write` (for the implicit 200 case)?
- Do third-party middleware libraries like chi provide this wrapper?

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
