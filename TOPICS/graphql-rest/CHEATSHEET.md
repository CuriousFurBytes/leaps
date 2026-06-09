# GraphQL and REST API Design — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [HTTP Methods Reference](#http-methods-reference)
- [HTTP Status Codes](#http-status-codes)
- [REST URI Design Patterns](#rest-uri-design-patterns)
- [GraphQL Syntax Quick Reference](#graphql-syntax-quick-reference)
- [GraphQL SDL Types Reference](#graphql-sdl-types-reference)
- [Common curl Commands](#common-curl-commands)
- [OpenAPI Structure Summary](#openapi-structure-summary)
- [OAuth2 Flows Summary](#oauth2-flows-summary)
- [Decision Guide: REST vs. GraphQL](#decision-guide-rest-vs-graphql)
- [Gotchas & Pitfalls](#gotchas--pitfalls)
- [Module Cross-References](#module-cross-references)

---

## HTTP Methods Reference

| Method | Safe? | Idempotent? | Typical Use | Body? |
|--------|-------|-------------|-------------|-------|
| `GET` | Yes | Yes | Read a resource or collection | No |
| `POST` | No | No | Create a new resource | Yes |
| `PUT` | No | Yes | Replace a resource entirely | Yes |
| `PATCH` | No | No* | Partial update of a resource | Yes |
| `DELETE` | No | Yes | Delete a resource | Rare |
| `HEAD` | Yes | Yes | Like GET but returns only headers | No |
| `OPTIONS` | Yes | Yes | Discover allowed methods (also used for CORS preflight) | No |

*PATCH can be designed to be idempotent, but is not required to be.

**Safe** = does not modify server state. **Idempotent** = repeated calls have the same effect as one call.

---

## HTTP Status Codes

### 2xx — Success

| Code | Name | When to Use |
|------|------|-------------|
| `200 OK` | OK | Successful GET, PUT, PATCH, or DELETE with body |
| `201 Created` | Created | Successful POST that created a resource; include `Location` header |
| `202 Accepted` | Accepted | Request accepted but processing not yet complete (async operations) |
| `204 No Content` | No Content | Successful DELETE or action that returns no body |
| `206 Partial Content` | Partial Content | Range request (used in streaming/downloads) |

### 3xx — Redirection

| Code | Name | When to Use |
|------|------|-------------|
| `301 Moved Permanently` | Moved Permanently | Resource has moved; clients should update their bookmarks |
| `302 Found` | Found | Temporary redirect; used in OAuth2 authorization code flow |
| `304 Not Modified` | Not Modified | Conditional GET; client's cached copy is still valid |

### 4xx — Client Errors

| Code | Name | When to Use |
|------|------|-------------|
| `400 Bad Request` | Bad Request | Malformed request syntax, invalid parameters |
| `401 Unauthorized` | Unauthorized | Not authenticated (misleadingly named — means "unauthenticated") |
| `403 Forbidden` | Forbidden | Authenticated but not authorised for this resource |
| `404 Not Found` | Not Found | Resource does not exist |
| `405 Method Not Allowed` | Method Not Allowed | HTTP method not supported on this endpoint |
| `409 Conflict` | Conflict | Request conflicts with current state (e.g., duplicate unique field) |
| `410 Gone` | Gone | Resource existed but has been permanently deleted |
| `422 Unprocessable Entity` | Unprocessable Entity | Validation error — request is syntactically valid but semantically wrong |
| `429 Too Many Requests` | Too Many Requests | Rate limit exceeded; include `Retry-After` header |

### 5xx — Server Errors

| Code | Name | When to Use |
|------|------|-------------|
| `500 Internal Server Error` | Internal Server Error | Unexpected server failure (the generic catch-all) |
| `502 Bad Gateway` | Bad Gateway | Upstream server returned an invalid response |
| `503 Service Unavailable` | Service Unavailable | Server temporarily overloaded or under maintenance |
| `504 Gateway Timeout` | Gateway Timeout | Upstream server timed out |

---

## REST URI Design Patterns

```
# Collections — use plural nouns
GET  /users              ← list all users
POST /users              ← create a user

# Single resources — noun + ID
GET    /users/{id}       ← get one user
PUT    /users/{id}       ← replace a user
PATCH  /users/{id}       ← partial update
DELETE /users/{id}       ← delete a user

# Nested resources — owned sub-resources
GET  /users/{id}/orders          ← orders belonging to a user
POST /users/{id}/orders          ← create an order for a user

# Query parameters — filtering, sorting, pagination
GET /orders?status=pending&sort=created_at&order=desc&page=2&limit=20

# Versioning in the URL path (most common pattern)
GET /v1/users/{id}
GET /v2/users/{id}
```

**Never use verbs in URIs:**

```
# Wrong
GET /getUser/42
POST /createOrder
DELETE /deleteProduct/99

# Right
GET /users/42
POST /orders
DELETE /products/99
```

---

## GraphQL Syntax Quick Reference

### Query

```graphql
# Basic query
query {
  user(id: "42") {
    name
    email
  }
}

# Named query with a variable
query GetUser($id: ID!) {
  user(id: $id) {
    name
    email
    posts {
      title
      createdAt
    }
  }
}
```

### Mutation

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    createdAt
  }
}
```

### Subscription

```graphql
subscription OnNewComment($postId: ID!) {
  commentAdded(postId: $postId) {
    id
    body
    author {
      name
    }
  }
}
```

### Fragment

```graphql
fragment UserFields on User {
  id
  name
  email
}

query {
  currentUser {
    ...UserFields
  }
  adminUsers {
    ...UserFields
    role
  }
}
```

### Aliases

```graphql
# Fetch two different users in one query using aliases
query {
  alice: user(id: "1") { name }
  bob: user(id: "2") { name }
}
```

### Directives

```graphql
query GetUser($withPosts: Boolean!) {
  user(id: "42") {
    name
    posts @include(if: $withPosts) {
      title
    }
    deletedAt @skip(if: true)
  }
}
```

---

## GraphQL SDL Types Reference

```graphql
# Scalar types (built-in)
# Int, Float, String, Boolean, ID

# Object type
type User {
  id: ID!                # Non-null (required)
  name: String!
  email: String          # Nullable (optional)
  posts: [Post!]!        # Non-null list of non-null Posts
  role: Role             # Enum
}

# Enum type
enum Role {
  ADMIN
  EDITOR
  VIEWER
}

# Interface
interface Node {
  id: ID!
}

type Post implements Node {
  id: ID!
  title: String!
}

# Union
union SearchResult = User | Post | Comment

# Input type (for mutations)
input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

# Query root type
type Query {
  user(id: ID!): User
  users: [User!]!
  search(query: String!): [SearchResult!]!
}

# Mutation root type
type Mutation {
  createUser(input: CreateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

# Subscription root type
type Subscription {
  userCreated: User!
}
```

---

## Common curl Commands

```bash
# GET request
curl https://api.example.com/users/42

# GET with verbose output (see headers)
curl -v https://api.example.com/users/42

# GET with Authorization header
curl -H "Authorization: Bearer <token>" https://api.example.com/users/42

# POST with JSON body
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# PATCH (partial update)
curl -X PATCH https://api.example.com/users/42 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith"}'

# DELETE
curl -X DELETE https://api.example.com/users/42

# GraphQL query via curl
curl -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: \"42\") { name email } }"}'

# Follow redirects (-L), show only response code (-o /dev/null -w "%{http_code}")
curl -L -o /dev/null -w "%{http_code}" https://api.example.com/redirect-test
```

---

## OpenAPI Structure Summary

```yaml
openapi: "3.1.0"

info:
  title: "My API"
  version: "1.0.0"
  description: "A brief description"

servers:
  - url: "https://api.example.com/v1"
    description: "Production"

paths:
  /users/{id}:
    get:
      summary: "Get a user by ID"
      operationId: "getUser"
      tags: ["users"]
      parameters:
        - name: id
          in: path          # path | query | header | cookie
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: "The user"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          description: "User not found"

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
      required: [id, name]

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

---

## OAuth2 Flows Summary

| Flow | Use Case | Client Type |
|------|----------|-------------|
| Authorization Code | User-facing web apps | Confidential (has secret) |
| Authorization Code + PKCE | Mobile apps, SPAs | Public (no secret) |
| Client Credentials | Machine-to-machine (no user) | Confidential |
| Implicit | Deprecated — do not use | — |
| Resource Owner Password | Deprecated — do not use | — |

**Authorization Code Flow (simplified):**

```
1. Client redirects user to:
   GET /authorize?response_type=code&client_id=...&redirect_uri=...&scope=...&state=...

2. User logs in and approves

3. Auth server redirects back to:
   GET /callback?code=AUTHCODE&state=...

4. Client exchanges code for tokens:
   POST /token
   grant_type=authorization_code&code=AUTHCODE&client_id=...&client_secret=...

5. Auth server returns:
   { "access_token": "...", "refresh_token": "...", "expires_in": 3600 }
```

---

## Decision Guide: REST vs. GraphQL

```
Designing a new API?
│
├── Multiple different client types (web, mobile, IoT) needing different data shapes?
│   └── Yes → Consider GraphQL (avoids over-fetching for mobile)
│
├── Simple CRUD with few resource types and predictable access patterns?
│   └── Yes → REST is simpler to build and operate
│
├── Public API for external developers (third parties)?
│   └── REST is more familiar; GraphQL requires understanding the query language
│
├── Real-time updates needed?
│   ├── GraphQL subscriptions or
│   └── REST with WebSockets/SSE (see Module 11)
│
├── File uploads needed?
│   └── REST handles multipart/form-data more naturally
│
├── Team already uses GraphQL expertise?
│   └── GraphQL; don't switch just because REST exists
│
└── Unsure → Start with REST; you can add a GraphQL layer later
```

---

## Gotchas & Pitfalls

> [!WARNING]
> **Using verbs in REST URIs**
> `/getUser/42` is not REST — it's RPC-over-HTTP. REST uses nouns (resources) in URIs
> and lets HTTP verbs express the operation.
>
> Wrong: `POST /createUser`
> Right: `POST /users`

> [!WARNING]
> **Returning 200 OK for errors**
> GraphQL returns HTTP 200 even when errors occur (errors are in the `errors` array).
> REST APIs must use 4xx or 5xx for errors. Never return `{ "error": "not found" }` with a 200.
>
> Wrong: `HTTP 200  { "error": "User not found" }`
> Right: `HTTP 404  { "error": "not_found", "message": "User 42 does not exist" }`

> [!WARNING]
> **The N+1 problem in GraphQL**
> Naive resolver implementations fetch one record per list item. Use DataLoader to batch.
>
> Wrong: 100 posts → 100 separate author queries → 101 total queries
> Right: 100 posts → 1 batched author query → 2 total queries

**Other things to watch out for:**

- **401 vs. 403 confusion** — 401 means "you haven't identified yourself"; 403 means "I know who you are, but you can't do this"
- **Not idempotency-testing DELETE** — calling DELETE on a non-existent resource should return 404, not 500
- **Overly broad CORS** — `Access-Control-Allow-Origin: *` is fine for public read-only APIs but dangerous for authenticated ones
- **Exposing stack traces in error responses** — never include exception details or file paths in production API error responses
- **Missing `Content-Type` header on POST/PATCH** — servers may reject requests without `Content-Type: application/json`
- **Forgetting to validate GraphQL variables** — client-supplied variables must be validated; never trust them implicitly

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| HTTP methods and status codes | [[modules/01_introduction]], [[modules/02_rest-fundamentals]] |
| URI design patterns | [[modules/02_rest-fundamentals]] |
| API versioning strategies | [[modules/03_rest-advanced]] |
| OAuth2 and JWT | [[modules/04_api-authentication]] |
| GraphQL query syntax | [[modules/05_graphql-fundamentals]] |
| Resolver execution and N+1 | [[modules/06_graphql-resolvers]] |
| Subscriptions and federation | [[modules/07_graphql-advanced]] |
| CORS and rate limiting | [[modules/08_api-security]] |
| Contract testing | [[modules/09_api-testing]] |
| API gateway configuration | [[modules/10_api-gateway-and-platforms]] |
| Webhooks and SSE | [[modules/11_event-driven-apis]] |

---

_Last updated: 2026-06-09_
