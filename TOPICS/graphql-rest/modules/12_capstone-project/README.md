# Module 12: Capstone Project — Public API Platform

[← Module 11: Event-Driven APIs](../11_event-driven-apis/README.md) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-20h-orange)

> Design and implement a production-quality public API: a REST API + equivalent GraphQL API for the same domain, with OpenAPI documentation, OAuth2 authentication, rate limiting, and a test suite.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Milestones](#milestones)
5. [Acceptance Criteria](#acceptance-criteria)
6. [Help / Getting Unstuck](#help--getting-unstuck)
7. [What Not to Do](#what-not-to-do)
8. [Cross-Links](#cross-links)
9. [Submitting Your Work](#submitting-your-work)

---

## Overview

This is the capstone module. You will build a real API platform from design to deployment —
not by following a step-by-step tutorial, but by applying everything you've learned across the
preceding 11 modules to a problem you define.

The capstone is **build-oriented**: you produce a real artifact that synthesises concepts from
multiple modules. It is not a test you pass in 30 minutes. Expect to spend 15–25 hours building,
debugging, reconsidering design decisions, and refining.

> [!IMPORTANT]
> **This module does not hand you a complete solution.** The Help sections below exist so you
> can get past a specific blocker and keep building. They are not a substitute for doing the
> work. A capstone that you built yourself — even imperfectly — teaches you far more than a
> polished copy-paste solution.

---

## Prerequisites

All preceding modules should be complete or substantially understood before starting the capstone:

- Module 01: Introduction — HTTP, REST overview
- Module 02: REST Fundamentals — resource modeling, HTTP methods, status codes
- Module 03: REST Advanced — versioning, pagination, OpenAPI
- Module 04: API Authentication — OAuth2, JWT
- Module 05: GraphQL Fundamentals — SDL, queries, mutations
- Module 06: GraphQL Resolvers — DataLoader, N+1 solution
- Module 07: GraphQL Advanced — subscriptions, federation (optional for basic capstone)
- Module 08: API Security — CORS, rate limiting, input validation
- Module 09: API Testing — contract tests, integration tests

---

## Project Brief

Design and implement a **public API platform** for a domain of your choice.

**Suggested domains** (pick one, or propose your own):
- A bookmarking / read-later service
- A recipe management platform
- A simple content management system (posts, categories, authors)
- A personal finance tracker (accounts, transactions, budgets)
- A public events calendar (events, venues, attendees)

**The platform must expose:**
1. A **REST API** with at least 3 resource types and full CRUD
2. An equivalent **GraphQL API** for the same domain (same data, different interface)
3. **OAuth2 authentication** (client credentials or authorization code flow)
4. **Rate limiting** per client (implement in middleware or gateway)
5. **OpenAPI 3.x documentation** for the REST API
6. A **test suite** with at least: contract tests for 2 REST endpoints, integration tests for 2 GraphQL queries, 1 mutation test

**Optional extensions** (for a more comprehensive capstone):
- A real-time webhook or SSE endpoint for a key event (e.g., "item created")
- Rate limiting at an API gateway layer (Kong or AWS API Gateway) instead of application middleware
- A WebSocket subscription for live updates
- Deployment to a cloud provider (fly.io, Railway, Render, or AWS)

---

## Milestones

Work through these milestones in order. Each one is a meaningful checkpoint.

### Milestone 1: Domain Design (2–3 hours)

Before writing any code:
- [ ] Write a 1-page design document describing your domain
- [ ] List your 3+ resource types and their relationships (draw an entity diagram)
- [ ] Write the REST API resource model (at least 5 endpoints, with methods and URIs)
- [ ] Write the GraphQL schema in SDL (at least the `Query`, `Mutation`, and 3 object types)
- [ ] Define what "authenticated" means in your domain and which endpoints require it

**Checkpoint:** Can you explain your design to a colleague in 5 minutes without notes?

---

### Milestone 2: REST API (4–6 hours)

- [ ] Implement all REST endpoints with correct methods and status codes
- [ ] Add request validation (return 422 for invalid requests)
- [ ] Implement pagination on at least one list endpoint
- [ ] Generate or write the OpenAPI specification
- [ ] All endpoints work with curl / Postman

**Checkpoint:** Every endpoint returns the correct status code for success and for the most likely error case.

---

### Milestone 3: Authentication (2–3 hours)

- [ ] Implement API key authentication OR OAuth2 client credentials
- [ ] Protected endpoints return 401 for missing credentials and 403 for insufficient permissions
- [ ] At least one endpoint is public (no auth required) and at least one is protected

**Checkpoint:** A client without a valid token cannot access protected resources.

---

### Milestone 4: GraphQL API (4–6 hours)

- [ ] Implement the GraphQL schema defined in Milestone 1
- [ ] All queries and mutations work correctly
- [ ] N+1 problem is solved with DataLoader for at least one type relationship
- [ ] Authentication is shared between REST and GraphQL (same token works for both)

**Checkpoint:** A single GraphQL query can fetch data that would require 3+ REST requests.

---

### Milestone 5: Rate Limiting (1–2 hours)

- [ ] Rate limiting is implemented (middleware, gateway plugin, or Redis-backed counter)
- [ ] API returns `429 Too Many Requests` with `Retry-After` header when limit is exceeded
- [ ] Different limits for authenticated vs. unauthenticated clients

**Checkpoint:** Sending 20+ rapid requests triggers a 429 response.

---

### Milestone 6: Test Suite (3–5 hours)

- [ ] Contract tests for at least 2 REST endpoints (Pact, Schemathesis, or OpenAPI-based)
- [ ] Integration tests for at least 2 GraphQL queries
- [ ] At least 1 mutation test with assertion on the response shape
- [ ] Tests run in CI (GitHub Actions or equivalent)

**Checkpoint:** `npm test` or `pytest` runs all tests and they pass.

---

### Milestone 7: Polish and Documentation (2–3 hours)

- [ ] README.md explains how to run the API locally and how to authenticate
- [ ] OpenAPI docs are accessible at `/docs`
- [ ] At least 5 GLOSSARY.md entries added with terms specific to your domain model
- [ ] At least 2 questions added to topic-level QUESTIONS.md reflecting what was learned

**Checkpoint:** A new developer can clone the repo and make a successful API call within 10 minutes.

---

## Acceptance Criteria

Your capstone is complete when it satisfies all of the following:

- [ ] REST API with ≥3 resource types, full CRUD, correct status codes, pagination on ≥1 endpoint
- [ ] GraphQL API with matching domain coverage (same data, different interface)
- [ ] Authentication implemented and enforced on protected endpoints
- [ ] Rate limiting with 429 response and `Retry-After` header
- [ ] OpenAPI 3.x specification that accurately describes the REST API
- [ ] Test suite with ≥ 5 tests covering REST and GraphQL, running without errors
- [ ] README explains how to run locally and authenticate
- [ ] You can explain every significant design decision you made

---

## Help / Getting Unstuck

> [!IMPORTANT]
> Use these hints only after a genuine attempt. The goal is to get you unstuck, not to do the
> work for you. Try for at least 30 minutes on a blocker before opening a hint.

### Stuck on the Domain Design?

<details>
<summary>Hint: How to pick a domain and model resources</summary>

Pick a domain with at least 3 "things" that relate to each other. For a recipe app:
- `Recipe` (has many Ingredients, belongs to a Category, has one Author)
- `Ingredient` (belongs to many Recipes)
- `Category` (has many Recipes)

Draw the entity diagram first. The REST resources map directly to these entities.
The GraphQL types also map to these entities — the difference is that GraphQL can traverse
relationships in a single query, while REST needs multiple requests.

Start with the simplest possible schema that lets you demonstrate the core value. You can add complexity in Milestone 7's polish phase.

</details>

### Stuck on Making REST and GraphQL Share Authentication?

<details>
<summary>Hint: JWT validation in both REST and GraphQL</summary>

The cleanest pattern is:
1. Create a `verify_token(token: str) -> dict` utility function that validates a JWT and returns the claims
2. In REST (FastAPI example): use it as a `Depends()` dependency on protected routes
3. In GraphQL: call it in the context builder — add the user dict to `context["user"]` if the token is valid, or `None` if not
4. Each resolver checks `context["user"]` to decide if the request is authorised

This way, token validation logic lives in one place, and both APIs use the same logic.

See Module 04 (API Authentication) for JWT validation details.

</details>

### Stuck on the N+1 Problem?

<details>
<summary>Hint: Finding and fixing the N+1 problem</summary>

Add query logging first to prove you have an N+1 problem. In SQLAlchemy:
```python
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

Then run a query like `{ recipes { title author { name } } }` for 10 recipes.
If you see 11 queries (1 for recipes + 10 for authors), you have N+1.

The fix is DataLoader:
```python
from promise import Promise
from promise.dataloader import DataLoader

class AuthorLoader(DataLoader):
    def batch_load_fn(self, author_ids):
        # One query for all IDs
        authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
        author_map = {a.id: a for a in authors}
        return Promise.resolve([author_map.get(id) for id in author_ids])
```

Add `AuthorLoader()` to context at request start. In the recipe resolver:
```python
def resolve_author(recipe, info):
    return info.context["author_loader"].load(recipe.author_id)
```

See Module 06 (GraphQL Resolvers) for a full DataLoader walkthrough.

</details>

### Stuck on Rate Limiting?

<details>
<summary>Hint: Simple in-memory rate limiting for development</summary>

For development, a simple sliding window rate limiter using Python's `collections.defaultdict`:

```python
import time
from collections import defaultdict

request_counts = defaultdict(list)

def check_rate_limit(client_id: str, limit: int = 10, window: int = 60) -> bool:
    """Returns True if request is allowed, False if rate limited."""
    now = time.time()
    # Remove requests outside the window
    request_counts[client_id] = [t for t in request_counts[client_id] if now - t < window]
    if len(request_counts[client_id]) >= limit:
        return False
    request_counts[client_id].append(now)
    return True
```

For production, use Redis with INCR + EXPIRE, or a library like `slowapi` for FastAPI.
See Module 08 (API Security) for the rate limiting algorithms in detail.

</details>

### Stuck on the Test Suite?

<details>
<summary>Hint: Minimal test structure that satisfies the acceptance criteria</summary>

For REST contract tests, Schemathesis is the easiest approach — it auto-generates tests from
your OpenAPI spec:

```python
# test_api.py
import schemathesis

schema = schemathesis.from_path("openapi.yaml", base_url="http://localhost:8000")

@schema.parametrize()
def test_api(case):
    case.call_and_validate()
```

For GraphQL integration tests (using `pytest` and `httpx`):

```python
import httpx
import pytest

@pytest.fixture
def client():
    return httpx.Client(base_url="http://localhost:8000")

def test_query_recipes(client):
    response = client.post("/graphql", json={
        "query": "{ recipes { id title } }"
    })
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"]["recipes"], list)
```

See Module 09 (API Testing) for Pact and Newman options.

</details>

---

## What Not to Do

> [!WARNING]
> The following will not give you the learning outcomes of this capstone.

- **Don't copy a tutorial project.** The learning is in the decisions you make when there is no tutorial to follow.
- **Don't skip milestones.** Each one builds on the previous. Jumping to Milestone 6 (testing) without working REST + GraphQL APIs means you're testing something that doesn't work yet.
- **Don't add features before the basics work.** A working API with 5 endpoints is better than a broken one with 20.
- **Don't treat the help sections as solutions.** Each hint answers one specific question. The rest of the implementation is yours.

---

## Cross-Links

- [[graphql-rest/modules/02_rest-fundamentals]] — Resource modeling and HTTP method semantics for the REST API
- [[graphql-rest/modules/03_rest-advanced]] — OpenAPI spec, pagination
- [[graphql-rest/modules/04_api-authentication]] — OAuth2 and JWT implementation
- [[graphql-rest/modules/05_graphql-fundamentals]] — SDL schema definition
- [[graphql-rest/modules/06_graphql-resolvers]] — DataLoader for the N+1 problem
- [[graphql-rest/modules/08_api-security]] — Rate limiting, CORS, input validation
- [[graphql-rest/modules/09_api-testing]] — Contract tests and integration tests
- [[django-fastapi-flask]] — FastAPI is a natural fit for this capstone; it generates OpenAPI automatically

---

## Submitting Your Work

When your capstone is complete:

1. Link your repository or deployed URL in the topic README's "Projects" table
2. Fill in the project attempt template in [PROJECTS.md](../../PROJECTS.md)
3. Update [PROGRESS.md](../../PROGRESS.md) — mark Module 12 complete
4. Add at least 2 entries to [GLOSSARY.md](../../GLOSSARY.md) from what you built
5. Answer or add to the open questions in [QUESTIONS.md](../../QUESTIONS.md)

**Self-assessment questions to answer honestly:**
- Can you explain the key architectural decisions you made (REST vs. GraphQL boundary, auth approach, rate limiting strategy)?
- What would you do differently if you built it again?
- What surprised you during the build?
