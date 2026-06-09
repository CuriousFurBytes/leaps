# Questions — Module 01: Introduction to APIs

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

### Q001: If REST is stateless, how do authentication cookies work?

**Asked:** 2026-06-09
**Status:** 🟡 Partial

**Full question:**
The module says REST requires statelessness — the server stores no session state about the client.
But many websites use session cookies for authentication, and the server stores the session data.
Is session-cookie authentication not RESTful? How do real-world APIs reconcile this?

**My current hypothesis:**
I think session cookies technically violate the statelessness constraint because the server is
storing session state. But practical REST APIs seem to use JWTs instead, where the token itself
contains all the needed information, so the server doesn't need to store anything.

**Answer:**
_Research in progress. See Module 04 (API Authentication) for the full answer._

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Is a JWT completely stateless? What happens when you need to revoke a JWT before it expires?

---

### Q002: What exactly counts as "breaking the HATEOAS constraint" in practice?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
The module says HATEOAS is one of the uniform interface sub-constraints, but that most real-world
"REST" APIs don't implement it. What does an API that actually implements HATEOAS look like, and
why do most practical APIs skip it?

**My current hypothesis:**
The JSON example in the theory section with `_links` is what HATEOAS looks like. I suspect most
APIs skip it because it adds complexity to both the server (generating links) and the client
(parsing and following links), and most clients are built by developers who know the API structure
anyway.

**Answer:**
_To be filled in — see Module 03 (REST Advanced) which covers this in more depth._

**Source / Confirmed by:**
_To be filled in_

**Follow-up questions:**
- Are there any real-world APIs that implement full HATEOAS? What does it look like to consume them?

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
| 🔴 Unanswered | 1 |
| 🟡 Partial | 1 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **2** |
