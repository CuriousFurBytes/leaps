# GraphQL and REST API Design — Projects

> Project-based learning cements knowledge in a way that reading and exercises alone cannot.
> Building something real forces you to confront gaps in your understanding and make decisions
> that tutorials never put in front of you.

---

## How to Use This File

1. Choose a project at or slightly above your current level.
2. **Don't use tutorials for your chosen project.** Tutorials are for learning, projects are for applying.
3. Document your attempt using the [Project Attempt Template](#project-attempt-template) at the bottom.
4. When you finish, link the result (repo, demo) in the table in the topic README.

---

## Beginner Projects

_Focus: get comfortable with making and interpreting HTTP requests, designing basic resource models._
_Complete at least one before advancing past Phase 1._

### B1: API Explorer — GitHub REST API

**Description:** Use the GitHub REST API (v3) to build a command-line tool (in Python or JavaScript)
that fetches information about any GitHub user: their profile, repositories, and recent commits.
No authentication required for public data.

**Concepts Reinforced:**
- Making HTTP GET requests with `requests` (Python) or `fetch` (JavaScript)
- Reading and interpreting HTTP response status codes
- Parsing JSON responses
- Understanding pagination (GitHub paginates with `Link` headers)

**Estimated Time:** 3–5 hours

**Starting Point:** Blank file. Start by reading the GitHub REST API docs for the `/users/{username}` endpoint.

**Success Criteria:**
- [ ] Can fetch and display a user's profile information
- [ ] Can list their public repositories
- [ ] Handles the case where the user does not exist (404) gracefully
- [ ] Code is readable and has comments explaining what each request does

---

### B2: Design a Resource Model

**Description:** Take a real domain (a library, a recipe app, or a simple e-commerce store) and
design its REST API resource model on paper — without writing any code. Define the resources,
their URIs, the HTTP methods each endpoint supports, and the JSON shape of at least two responses.

**Concepts Reinforced:**
- REST resource modeling
- URI hierarchy design
- HTTP method semantics (which verbs to use for which operations)
- Thinking in nouns (resources) rather than verbs (actions)

**Estimated Time:** 2–3 hours

**Starting Point:** Blank document. Choose a domain you know well.

**Success Criteria:**
- [ ] At least 4 resources defined with correct plural noun URIs
- [ ] Each resource has GET, and at least one mutation method documented
- [ ] Correct status codes documented for success and error cases
- [ ] No verb-based endpoint names (e.g., `/getUser` is wrong; `/users/{id}` is right)

---

### B3: curl Exploration

**Description:** Using only `curl` from the command line, explore a public REST API of your choice
(suggestions: JSONPlaceholder at `jsonplaceholder.typicode.com`, OpenWeatherMap, or the GitHub API).
Document every request you make, the response you received, and what you learned.

**Concepts Reinforced:**
- HTTP request anatomy (method, URL, headers, body)
- Response status codes in the wild
- Authentication headers (Bearer token, API key)
- How to send POST data with curl

**Estimated Time:** 2 hours

**Starting Point:** Install `curl` (it ships with most operating systems). Start with `curl -v https://jsonplaceholder.typicode.com/posts/1`.

**Success Criteria:**
- [ ] Made at least one GET, POST, PUT, and DELETE request
- [ ] Documented the full request and response for each
- [ ] Understood the difference between 200, 201, 204, and 404

---

## Intermediate Projects

_Focus: build a working API with proper design, error handling, and basic auth._
_Complete at least one before completing Phase 2._

### I1: Build a REST API for a Task Manager

**Description:** Build a REST API for a task management app (think Todoist or Things).
Implement in Python (FastAPI or Flask) or JavaScript (Express). The API must support
creating, reading, updating, and deleting tasks and task lists. Include proper status codes,
error handling, and a basic OpenAPI specification.

**Concepts Reinforced:**
- REST resource modeling and URI design
- Correct HTTP method usage and status code responses
- Request validation and error response format
- OpenAPI documentation (auto-generated with FastAPI, or hand-written)
- Pagination for list endpoints

**Estimated Time:** 8–12 hours

**Starting Point:** Set up a new Python virtual environment with FastAPI or an Express project. Start by sketching the resource model before writing any code.

**Success Criteria:**
- [ ] `GET /tasks`, `POST /tasks`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `DELETE /tasks/{id}` all work
- [ ] Returns correct status codes (201 on create, 404 when not found, 422 on validation error)
- [ ] OpenAPI spec is accessible at `/docs` (FastAPI) or written manually
- [ ] List endpoints support `?page=` and `?limit=` query parameters
- [ ] Code is clean, readable, and commented

---

### I2: Explore the GitHub GraphQL API

**Description:** Use the GitHub GraphQL API v4 to perform queries that are difficult or impossible
to do cleanly with the REST API. Examples: fetch a user's profile, their 5 most recently updated
repositories, and the last 3 open issues on each repository — all in a single request.

**Concepts Reinforced:**
- Writing GraphQL queries with variables and fragments
- Understanding what over-fetching and under-fetching mean in practice
- Authentication with Bearer tokens
- Using GraphQL introspection to explore the schema

**Estimated Time:** 4–6 hours

**Starting Point:** Create a GitHub personal access token. Use GraphiQL at `docs.github.com/en/graphql/overview/explorer` to explore the schema before writing code.

**Success Criteria:**
- [ ] At least 5 queries written that use variables, not hardcoded values
- [ ] At least one query that uses fragments to share field selections
- [ ] Can explain the difference in network efficiency vs. equivalent REST calls
- [ ] Used introspection to discover at least one field you wouldn't have known about otherwise

---

### I3: Add API Key Authentication to an Existing REST API

**Description:** Take the task manager API you built in I1 (or build a simpler one), and add
API key authentication. Every request must include a valid API key in the `X-API-Key` header.
Implement key generation, storage, and validation. Return proper 401 and 403 responses.

**Concepts Reinforced:**
- API key authentication pattern
- Middleware/dependency injection for authentication
- Correct use of 401 (unauthenticated) vs. 403 (authenticated but unauthorised)
- Rate limiting per API key (stretch goal)

**Estimated Time:** 4–6 hours

**Starting Point:** Use the task manager from I1, or start fresh. Implement key storage in-memory (a Python dict or JavaScript Map) — no database required.

**Success Criteria:**
- [ ] All endpoints require a valid `X-API-Key` header
- [ ] Returns 401 when no key is provided
- [ ] Returns 403 when key is invalid
- [ ] Key validation is in one place (a middleware or dependency), not copied into each route

---

## Advanced Projects

_Focus: tackle realistic, open-ended problems. No hand-holding._
_Complete at least one to reach Applied Practitioner status._

### A1: Build a GraphQL API with DataLoader

**Description:** Build a GraphQL API for a simple blog (posts, users, comments). Implement it
in JavaScript (Apollo Server) or Python (Strawberry). You must solve the N+1 problem using
DataLoader — measure the number of database queries before and after to prove it works.

**Why This Is Hard:**
Getting DataLoader right requires understanding both the async batch function pattern and how
GraphQL's execution model triggers resolver calls. Most implementations have subtle bugs where
batching doesn't fire as expected.

**Concepts Reinforced:**
- GraphQL schema design with SDL
- Resolver functions (Query, Mutation, and type resolvers)
- The N+1 problem and why it happens
- DataLoader batch function implementation
- Measuring and proving performance improvement

**Estimated Time:** 12–16 hours

**Starting Point:** Use an in-memory data store (arrays of objects in JavaScript, or Python dicts).
Install `apollo-server` and `dataloader` (Node.js) or `strawberry-graphql` (Python).

**Success Criteria:**
- [ ] Schema defines `User`, `Post`, and `Comment` types with relationships
- [ ] Can query posts with their authors without N+1 queries (prove it with logging)
- [ ] Mutations for creating posts and comments work correctly
- [ ] DataLoader is used for all N+1-prone field resolvers
- [ ] You can explain every design decision you made

---

### A2: Design an API Versioning Strategy

**Description:** Take an existing API (yours or a public one) and design a comprehensive versioning
strategy for it. Document: the versioning scheme (URL path, query param, header), a backwards
compatibility policy, a deprecation timeline template, and a migration guide for at least one
breaking change.

**Why This Is Hard:** Versioning forces you to think about your API as a long-lived product with
external consumers — a perspective most developers lack until they've broken a production API.

**Concepts Reinforced:**
- API versioning patterns (URL path, query param, header, content negotiation)
- Semantic versioning applied to APIs
- Breaking vs. non-breaking changes
- Deprecation policy design

**Estimated Time:** 6–10 hours

**Success Criteria:**
- [ ] Documented versioning scheme with clear rationale for the choice
- [ ] Defined what constitutes a breaking change for this API
- [ ] Written a deprecation timeline (e.g. "deprecated in v2, removed in v3 after 6 months")
- [ ] Migration guide covers at least one realistic breaking change
- [ ] You can articulate tradeoffs between the versioning approach you chose and alternatives

---

## Expert / Capstone Projects

_Focus: synthesize everything. Build something you're proud to show others._
_Complete one to earn Topic Mastery status._

### E1: Full REST + GraphQL API Platform

**Description:** Design and build a public API for a domain of your choice (a bookmarking
service, a simple CMS, or an inventory management system). The platform must expose both
a REST API and an equivalent GraphQL API for the same domain, share an authentication layer,
include rate limiting, and have a test suite.

**Why This Is a Capstone:**
This project requires mastery of all major topic areas. You cannot complete it with gaps —
they will surface quickly. Expect to revisit earlier modules during the build.

**Core Requirements:**
- [ ] Uses concepts from at least 8 different modules
- [ ] REST API with full OpenAPI documentation
- [ ] GraphQL API with a complete SDL schema
- [ ] OAuth2 or JWT authentication shared between both APIs
- [ ] Rate limiting per client
- [ ] Contract tests for the REST API (Pact or similar)
- [ ] Integration tests for key GraphQL operations
- [ ] Written design document explaining your decisions

**Estimated Time:** 20–30 hours

**Extension Ideas (if you want more challenge):**
- Add a WebSocket subscription for real-time updates
- Deploy behind Kong or AWS API Gateway
- Implement schema federation if the domain has natural subgraph boundaries

> [!NOTE]
> The final module of this topic (Module 12: Capstone Project) is a dedicated module that walks you
> through building this for real. It gives you a brief, milestones, and a **Help / Getting Unstuck**
> section with staged hints — but it deliberately does **not** hand you a finished solution.
> The help is there so you can get past a blocker and keep going on your own, not so you can
> skip the build. Struggling productively *is* the learning here.

---

## Project Attempt Template

When you attempt a project, create a folder in this topic's directory and copy this template:

```markdown
# Project: {{PROJECT_NAME}}

**Difficulty:** Beginner / Intermediate / Advanced / Expert
**Started:** {{YYYY-MM-DD}}
**Completed:** {{YYYY-MM-DD}} (or "In progress")
**Time Spent:** {{HOURS}} hours

## What I Built

{{DESCRIPTION_OF_WHAT_YOU_ACTUALLY_BUILT}}

## Link / Location

{{LINK_TO_REPO_OR_FILE}}

## What I Learned

- {{LEARNING_1}}
- {{LEARNING_2}}
- {{LEARNING_3}}

## What Was Hard

{{WHAT_WAS_CHALLENGING_AND_HOW_YOU_SOLVED_IT}}

## What I'd Do Differently

{{HONEST_RETROSPECTIVE}}

## Concepts Used

- [[modules/01_introduction]] — how you used it
- [[modules/02_rest-fundamentals]] — how you used it

## Score / Self-Assessment

On a scale of 1–5, how well do I think I executed this project? {{SCORE}}/5

Justification: {{JUSTIFICATION}}
```
