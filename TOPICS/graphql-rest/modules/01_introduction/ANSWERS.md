# Answer Key — Module 01: Introduction to APIs

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

### 1.1 — API Definition [1 pt]

**Full credit answer:**
An API (Application Programming Interface) is a formal contract between a software provider and
a consumer. The provider declares what capabilities it offers and how to invoke them; the consumer
calls the API according to those rules. The "contract" metaphor refers to the guarantee that as
long as both sides follow the interface definition, neither needs to know the internal implementation
of the other.

**Key points required:**
- The word "contract" or equivalent (agreement, interface definition)
- Provider/consumer relationship
- Internal implementation is hidden from the consumer

**Common wrong answers:**
- *"An API is a way for programs to communicate"* — Too vague; doesn't address the contract or provider/consumer model. 0.5 pts.
- *"An API is a URL you can send requests to"* — This confuses an API with a specific HTTP endpoint. 0 pts.

---

### 1.2 — Six REST Constraints [1 pt]

**Full credit answer:**
1. Client-server separation
2. Statelessness
3. Cacheability
4. Uniform interface
5. Layered system
6. Code-on-demand (optional)

**Partial credit:** 0.5 pts if at least 4 of the 6 are correctly named.

**Common wrong answers:**
- Including "idempotency" as a constraint — idempotency is a property of HTTP methods, not a REST constraint. 0.5 pts if otherwise mostly correct.

---

### 1.3 — Over-Fetching vs. Under-Fetching [1 pt]

**Full credit answer:**
**Over-fetching** is when an API endpoint returns more data than the client needs for its current
use case. The client receives fields it discards, wasting bandwidth and processing time.

**Under-fetching** is when a single API endpoint doesn't return all the data a client needs,
forcing the client to make multiple requests to assemble a complete view (also called the N+1
requests problem).

**The key distinction is:** Over-fetching is too much data from one request; under-fetching is
not enough data, requiring multiple requests.

---

### 1.4 — Status Code for Successful Creation [1 pt]

**Full credit answer:**
`201 Created`. The response body typically contains the created resource (with its server-assigned
ID), and the response should include a `Location` header pointing to the URL of the new resource.

**Key distinction:** 201 (not 200) signals that a new resource was created. 200 OK indicates a
successful operation that didn't create a new resource.

---

### 1.5 — Headers vs. Body [1 pt]

**Full credit answer:**
**Headers** are metadata key-value pairs that describe the request or response but are not the
main content. They appear before the body, separated by a blank line.
Examples in headers: `Content-Type: application/json`, `Authorization: Bearer <token>`, `Host: api.example.com`.

**Body** is the main content payload of the request or response.
Examples in the body: the JSON data for a new user being created (`{"name": "Alice"}`),
or the JSON array of search results in a response.

**Partial credit:** 0.5 pts if only one side (headers or body) is correctly explained.

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Statelessness [2 pts]

**Full credit answer:**
Statelessness means the server stores no session state about any client between requests. Every
request must carry all information the server needs to process it. The server has no memory of
previous requests from the same client.

Why it enables horizontal scaling: since any server instance can process any request (none hold
client-specific state), adding more servers is trivial — just put them behind a load balancer.
No "sticky sessions" are needed.

The tradeoff for clients: clients must send their credentials (e.g., a JWT token) with every
request, adding a small overhead to each call. State that would be implicit in a session-based
system (who you are, what you're doing) must be explicit in each request.

**Rubric:**
- 2 pts: Explains the constraint correctly AND explains the scaling benefit AND mentions the client tradeoff
- 1 pt: Explains the constraint and one of (scaling benefit OR tradeoff)
- 0 pts: Incorrect understanding (e.g., "stateless means the data is not stored on disk")

---

### 2.2 — Using 200 for All Responses [2 pts]

**Full credit answer:**
The developer is wrong. Using `200 OK` for error responses causes several concrete problems:

1. **HTTP infrastructure breaks**: Caches, CDNs, load balancers, and monitoring systems use
   HTTP status codes to make decisions. A 200 response may be cached when it shouldn't be.
   Rate limiting and circuit breakers can't distinguish real failures from successful responses.

2. **Client error handling is harder**: Every client must parse the body to detect errors,
   adding boilerplate code. Standard HTTP clients and frameworks can't do automatic retries
   for 5xx errors if errors look like 200s.

3. **Observability breaks**: Log aggregators and APM tools track error rates by status code.
   If all responses are 200, the error rate looks 0% even when the service is broken.

4. **Misleading tooling**: API testing tools, Postman, and browser dev tools highlight 4xx/5xx
   responses. A 200 error response looks like a success.

**Rubric:**
- 2 pts: Identifies that this is incorrect AND gives at least two concrete problems with reasoning
- 1 pt: Identifies it's incorrect with only one concrete problem
- 0 pts: Agrees with the developer, or identifies it's wrong without explaining why

**Teaching note:** GraphQL intentionally returns 200 for schema-level errors (the error is in `errors[]`),
which is a deliberate design choice for a different reason — the HTTP response is for the transport,
not the query result. Make sure students don't confuse this with REST.

---

### 2.3 — REST Multi-Request vs. GraphQL Single-Query [2 pts]

**Full credit answer:**
**REST multi-request pattern:** For a view requiring data from 3 resources (e.g., a post, its
author, and its comment count), the client makes 3 sequential HTTP requests. Each request is
cacheable independently, and the server-side code for each resource is simpler.

**GraphQL single-query:** The client sends one request specifying all needed fields. The server
resolves the relationships internally. One network round trip, one response.

**When REST performs better:**
- When data can be cached aggressively (CDN caching a stable resource like a public profile)
- When the client needs only one resource (no under-fetching problem to solve)
- When clients are diverse and mostly need the same data shape

**When GraphQL performs better:**
- When assembling a view requires 5–50+ REST requests (complex social/e-commerce graphs)
- On slow mobile connections where each additional round trip has significant latency cost
- When different clients (mobile, web, smartwatch) need very different data shapes from the same domain

**Rubric:**
- 2 pts: Correctly characterises both approaches AND gives at least one concrete scenario for each
- 1 pt: Characterises both approaches but gives only generic reasoning without scenarios
- 0 pts: Gets the comparison backwards, or can't distinguish the two

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — get_posts_by_user function [3 pts]

**Full credit answer:**
```python
import requests

def get_posts_by_user(user_id: int) -> list[dict] | None:
    """
    Fetch all posts by a given user ID.
    Returns a list of posts (may be empty), or None if user doesn't exist (404).
    Raises an exception for unexpected status codes.
    """
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": user_id}
    )

    if response.status_code == 404:
        return None    # User not found

    response.raise_for_status()    # Raise for 5xx, 429, etc.

    return response.json()    # May be an empty list — that's valid
```

**Step-by-step reasoning:**
1. Use `params=` for query parameters (cleaner than string concatenation)
2. Check 404 first and return `None` explicitly
3. Call `raise_for_status()` after handling 404 to catch other errors
4. Return `response.json()` — this may be `[]` (empty list), which is distinct from `None`

**Rubric:**
- 3 pts: All 4 requirements satisfied; returns correct types for each case; well-structured
- 2 pts: 3 requirements satisfied, or one logical error (e.g., returns empty list instead of None for 404)
- 1 pt: Correct general approach but missing at least 2 requirements
- 0 pts: Doesn't solve the problem or has fundamental misunderstanding

**Acceptable alternatives:**
- Using `response.status_code == 200` instead of `raise_for_status()` — less idiomatic but acceptable
- Returning an empty list for 404 instead of None — acceptable if the docstring reflects this choice

---

### 3.2 — Book Library REST Endpoints [3 pts]

**Full credit answer:**

| Method | URL | Success Status | Notes |
|--------|-----|---------------|-------|
| `GET` | `/books` | `200 OK` | Returns array of books |
| `GET` | `/books/{id}` | `200 OK` | Returns single book; `404` if not found |
| `POST` | `/books` | `201 Created` | Returns created book; includes `Location` header |
| `PATCH` | `/books/{id}` | `200 OK` | Updates title; `404` if not found |
| `DELETE` | `/books/{id}` | `204 No Content` | No body; `404` if not found |

**Key points:**
- Plural noun for collection (`/books`, not `/book`)
- `POST` to the collection, not to a specific ID
- `201` (not 200) for creation
- `204` (no body) for delete
- `PATCH` for partial update (only title), not `PUT` (full replace)

**Rubric:**
- 3 pts: All 5 endpoints correct with right methods and status codes
- 2 pts: 4 endpoints correct; minor status code errors
- 1 pt: Methods and URLs mostly correct but status codes mostly wrong
- 0 pts: Verb-based URLs or fundamentally incorrect method choices

**Common wrong answers:**
- Using `PUT /books/{id}` for updating a title — PUT replaces the entire resource; PATCH is for partial updates. Accept PUT if the student explains they're replacing the whole book.
- Returning `200` for creation — should be `201`. Deduct 0.5 pts from this endpoint.

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Travel Booking API Design [3 pts] (1 pt each part)

**(a) REST constraints violated:**
The design violates the **Uniform Interface** constraint — specifically, the principle that HTTP
methods should express operation intent and URIs should identify resources. All four operations
use `POST` regardless of their read/write/delete nature. Operations are expressed as query
parameters (`action=searchFlights`) rather than through HTTP method semantics and resource URIs.

**(b) Concrete problems:**
- **Caching broken**: `POST /api?action=searchFlights` is not cacheable. Identical flight search
  results can't be cached by CDN or browsers. With a `GET` to `/flights?origin=JFK&...`, the
  results could be cached.
- **Semantics broken**: Using `POST` for reads means search operations appear to create something.
  HTTP monitoring tools, rate limiters, and circuit breakers behave incorrectly.
- **Tooling degraded**: API documentation tools, testing frameworks, and API explorers expect
  resources and HTTP methods — not `action` parameters. Harder to document and test.
- **No idempotency signals**: Tools can't know that `action=getBooking` is safe to retry but
  `action=cancelBooking` is not.

**(c) RESTful redesign:**
```
GET  /flights?origin=JFK&destination=LAX&date=2026-08-15   → search flights (200)
POST /bookings                                              → create booking (201)
Body: { "flightId": "FL123", "passengerId": 99 }

DELETE /bookings/BK456                                     → cancel booking (204)
GET    /bookings/BK456                                     → get booking details (200)
```

**Rubric:**
- 1 pt for (a): correctly identifies Uniform Interface violation
- 1 pt for (b): gives at least 2 concrete problems with explanation
- 1 pt for (c): redesign uses correct HTTP methods, noun-based URIs, and appropriate status codes

---

## Section 5: Discussion — Answer Key

### 5.1 — Was GraphQL the Right Choice? [2 pts]

**Example strong answer:**
Facebook's choice to build GraphQL rather than redesign REST was justified given their specific
constraints, though it came with significant costs. Their domain — a social graph with hundreds
of entity types, a mobile app that needed to minimise data transfer, and dozens of internal and
external teams consuming the same API — was exactly where REST's fixed data shapes fail most visibly.
A redesigned REST API would still require multiple round trips and versioning complexity for
each new view. GraphQL's "ask for what you need" model was a better fit.

The tradeoffs: they had to design a new query language, build a new execution engine, and train
their entire engineering organisation on a new paradigm. The GraphQL specification itself took
years to stabilise. For a smaller organisation, the investment might not pay off — a well-designed
REST API with thoughtful resource modeling often suffices. Facebook (with thousands of engineers
and billions of API calls per day) had both the scale to justify the investment and the engineering
capacity to build and maintain it.

**Elements that earn full credit:**
- Acknowledges that the decision was justified in Facebook's specific context (not just "GraphQL is better")
- Identifies at least one concrete advantage (over/under-fetching, client flexibility)
- Identifies at least one real tradeoff (complexity, investment, learning curve)
- Shows understanding that context matters — a different organisation might make a different choice

**Rubric:**
- 2 pts: Considers at least two perspectives; uses concrete reasoning; conclusion is well-grounded
- 1 pt: One-sided ("GraphQL is better") or doesn't use facts from the module to support reasoning
- 0 pts: Off-topic or shows fundamental misunderstanding

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — Statelessness at Scale [+5 pts]

**Full credit answer:**
The question contains a false dichotomy. Statelessness in Fielding's sense means the *server*
doesn't store client-specific application state *between requests*. It doesn't preclude server-side
data storage — databases are fine. The question is whether client identity state lives on the
server or in the request.

JWT (JSON Web Token) is the canonical solution at scale: the token itself encodes the user's
identity and claims (who they are, what they can do, when the token expires), cryptographically
signed so the server can validate it without a database lookup. The server is stateless with
respect to authentication — it validates the token in each request independently.

The challenge JWT introduces is revocation: if a token is compromised, you can't invalidate it
before it expires without introducing some server-side state (a "revoked tokens" blacklist). This
is why OAuth2 (Module 04) uses short-lived access tokens (15 minutes) plus refresh tokens. When
a token must be revoked, you wait for the short-lived access token to expire naturally, and revoke
the refresh token (which is stored server-side, but only at token refresh time, not every request).

So large-scale systems like Facebook achieve practical statelessness at the request level while
accepting minimal server-side state at the token-refresh level. This isn't technically "100% pure
Fielding REST" — it's an engineering tradeoff that gets 95% of the scaling benefits while solving
the practical revocation problem. Fielding himself acknowledged that the constraints describe
ideal properties, not rigid rules.

**Rubric:**
- 5 pts: Explains the JWT solution, acknowledges the revocation problem, connects to OAuth2's access/refresh token model, and frames the answer as a practical tradeoff rather than a binary
- 3 pts: Explains JWTs correctly but doesn't address revocation or OAuth2
- 1 pt: Right direction (JWTs solve statelessness) but can't explain how
- 0 pts: Incorrect (e.g., "Redis is stateless because it's fast")

**Bonus teaching note:**
This question tests whether the student can synthesise the module content with knowledge from
Module 04 (preview) and apply it to a real architectural problem. It also tests intellectual
honesty — the correct answer involves acknowledging that even well-designed systems make pragmatic
tradeoffs. Students who give a nuanced answer show they're internalising engineering judgment,
not just memorising definitions.

---

## Common Wrong Answers Across the Test

1. **Confusing REST with HTTP** — REST is an architectural style that *uses* HTTP; HTTP is the
   transport protocol. An API can use HTTP without being RESTful. Students who make this mistake
   need to re-read the "REST: Representational State Transfer" section.

2. **Treating GraphQL as "always better than REST"** — GraphQL solves specific problems (over/under-fetching,
   multiple client types). For simple CRUD APIs with a single client type, REST is often simpler
   and better. Students who miss this need to re-read the "When REST Wins" section.

3. **Missing that 404 and empty list are different** — In question 3.1, a user who exists but has
   no posts returns `200 OK` with `[]`. A user ID that doesn't exist returns `404 Not Found`. These
   are semantically different: one is "user exists, has no posts"; the other is "no such user."

---

## Teaching Notes

- Students who struggle with Section 2 likely read without testing their understanding. Recommend
  re-studying with the Feynman technique (explain it aloud).
- Students who struggle with Section 3 need more exercise practice before moving on. Send back
  to EXERCISES.md.
- The bonus question tests synthesis of HTTP, REST, authentication, and distributed systems.
  Don't be concerned if most students skip it or score partially — it's genuinely advanced.
- A score below 60% generally indicates the prerequisites weren't solid. Ask the student which
  prerequisite concept feels weakest: HTTP fundamentals, the REST constraints, or basic Python.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
