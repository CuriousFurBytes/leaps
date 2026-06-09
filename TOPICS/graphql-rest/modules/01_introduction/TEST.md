# Test — Module 01: Introduction to APIs

**Topic:** [[graphql-rest]]
**Module:** [[modules/01_introduction]]

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

**Passing score:** 15/22 (68%) · **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** Define what an **API** is in your own words. What is the "contract" metaphor referring to?

> _Your answer:_

---

**1.2** List the six REST architectural constraints defined by Roy Fielding. You do not need to
explain each — just name them.

> _Your answer:_

---

**1.3** What is the difference between **over-fetching** and **under-fetching** in the context
of REST APIs?

> _Your answer:_

---

**1.4** What HTTP status code should a server return when a resource is successfully created?
What should the response body typically contain?

> _Your answer:_

---

**1.5** What is the difference between an HTTP **request header** and the HTTP **body**?
Give one example of something that belongs in a header and one example that belongs in the body.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain the **statelessness** REST constraint. Why does it make APIs easier to scale
horizontally? What tradeoff does it introduce for clients?

> _Your answer:_

---

**2.2** A junior developer says: "I don't need to use HTTP status codes — I always return
`200 OK` and put success or failure information in the JSON body. That way I only need to
check the body, not both the body and the status code." Is this correct? If not, explain the
problems this approach causes.

> _Your answer:_

---

**2.3** Compare the **REST multi-request pattern** (for a view that needs data from 3 resources)
with the **GraphQL single-query pattern** for the same view. Under what circumstances would each
approach perform better?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a Python function called `get_posts_by_user(user_id: int) -> list[dict]` that:
- Makes a GET request to `https://jsonplaceholder.typicode.com/posts?userId={user_id}`
- Returns the list of posts if the request succeeds (200)
- Returns an empty list if the user has no posts (also 200, just an empty array)
- Returns `None` if the user ID is not found (404)
- Raises an exception for any other status code

Show your code.

> _Your answer:_

---

**3.2** Design the REST endpoints for a simple **book library API** that allows:
- Listing all books
- Getting a specific book by ID
- Adding a new book
- Updating a book's title
- Deleting a book

For each endpoint, specify: the HTTP method, the URL, and the status code you'd return on success.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A team is building a travel booking API. Here is their current design:

```
POST /api?action=searchFlights&origin=JFK&destination=LAX&date=2026-08-15
POST /api?action=bookFlight&flightId=FL123&passengerId=99
POST /api?action=cancelBooking&bookingId=BK456
POST /api?action=getBooking&bookingId=BK456
```

Identify:

a) What REST constraint(s) does this design violate?

b) What specific problems would this cause in practice (caching, semantics, tooling)?

c) Redesign the endpoints to be more RESTful. Provide at least 4 endpoints.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** Facebook's engineering team chose to build GraphQL rather than redesign their REST API.
Given what you know about the problems they were facing (multiple client types, complex data
relationships, mobile performance), was this the right choice? What were the tradeoffs of
building a new query language rather than improving REST?

Consider at least two perspectives in your answer.
Justify your conclusion based on what you've learned in this module.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Fielding described the stateless constraint as essential for web-scale applications.
Yet many high-traffic applications (e.g., Facebook, Google, Twitter) use some form of session
state (server-side session storage, Redis session caches, etc.) in their architectures.

Does this mean these applications are "not RESTful"? Or is there a way to reconcile the
statelessness constraint with the practical need for efficient session/authentication handling
at massive scale? Synthesise your understanding of statelessness, JWTs, OAuth2 (which you'll
study in Module 04), and distributed systems to construct a coherent answer.

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

**Grade scale:** A ≥ 90% (≥20/22) · B ≥ 80% (≥18/22) · C ≥ 70% (≥15/22) · D ≥ 60% (≥13/22) · F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
