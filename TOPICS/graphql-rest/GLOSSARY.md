# GraphQL and REST API Design — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of API design.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use. Code snippet or real-world scenario.
```

Keep definitions in your own words as much as possible.

---

## E

### endpoint

**Definition:** A specific URL (path + HTTP method combination) that a REST API exposes to clients. An endpoint represents one operation a client can perform — for example, `GET /users/{id}` is the endpoint for fetching a single user. In contrast, a GraphQL API typically has a single endpoint (`/graphql`) and clients specify the operation in the request body.

**Also known as:** route (in web framework terminology)

**Related:** [[resource]], [[http-verb]], [[rest-constraints]]

**Example:**
```
GET  /api/v1/orders          ← endpoint: list all orders
POST /api/v1/orders          ← endpoint: create an order
GET  /api/v1/orders/42       ← endpoint: fetch order #42
DELETE /api/v1/orders/42     ← endpoint: delete order #42
```

---

## F

### federation

**Definition:** In GraphQL, federation is an architecture pattern where a single GraphQL schema (the "supergraph") is split across multiple independently deployed services (called "subgraphs"). Each subgraph owns a portion of the schema and its resolvers. A gateway stitches the subgraphs together into a unified API that clients query as if it were a single server. Apollo Federation is the most widely-used implementation.

**Also known as:** schema federation, distributed GraphQL, supergraph

**Related:** [[graphql-schema]], [[resolver]], [[api-gateway-and-platforms]]

**Example:**
A users subgraph owns `type User` and a products subgraph owns `type Product`. Apollo Gateway merges them so clients can query `user { name recentOrders { product { name } } }` in one request even though `recentOrders` is resolved in an orders subgraph.

---

## H

### HATEOAS

**Definition:** Hypermedia as the Engine of Application State — one of Fielding's REST constraints. A fully HATEOAS-compliant API includes links in its responses that tell the client what it can do next, rather than requiring the client to have pre-built knowledge of the URL structure. In practice, most "REST" APIs do not implement HATEOAS; it remains aspirational in most commercial APIs.

**Also known as:** hypermedia constraint, self-describing API

**Related:** [[rest-constraints]], [[endpoint]], [[openapi]]

**Example:**
```json
{
  "order_id": 42,
  "status": "pending",
  "_links": {
    "self": { "href": "/orders/42" },
    "cancel": { "href": "/orders/42/cancel", "method": "DELETE" },
    "pay": { "href": "/orders/42/payment", "method": "POST" }
  }
}
```
The client doesn't need to know the cancel URL — the API tells it.

---

## HTTP verb

**Definition:** The HTTP method used in a request, which semantically describes the intent of the operation. The primary verbs in REST API design are GET (read), POST (create), PUT (replace), PATCH (partial update), and DELETE (remove). The choice of verb determines idempotency, cacheability, and safe-operation guarantees.

**Also known as:** HTTP method

**Related:** [[endpoint]], [[idempotency]], [[rest-constraints]]

**Example:**
```
GET    /users/42    → safe, idempotent, cacheable — read a user
DELETE /users/42    → idempotent (deleting twice has the same effect as once)
POST   /users       → not idempotent (calling twice creates two users)
PATCH  /users/42    → partial update; idempotent if designed carefully
```

---

## I

### idempotency

**Definition:** An operation is idempotent if calling it multiple times produces the same result as calling it once. In HTTP, GET, PUT, DELETE, and HEAD are defined as idempotent; POST is not. Idempotency matters for retry logic — if a network failure leaves you unsure whether a request succeeded, you can safely retry an idempotent request without causing side effects. Stripe uses idempotency keys to make even POST requests idempotent.

**Also known as:** idempotent operation

**Related:** [[http-verb]], [[rest-constraints]]

**Example:**
`DELETE /users/42` — deleting a user that doesn't exist returns 404, but doesn't cause errors or data corruption. Calling it twice is safe. Contrast with `POST /emails/send`, which sends a second email if retried.

---

### introspection

**Definition:** GraphQL's built-in capability for a client to query the schema itself — asking the API what types, fields, queries, and mutations are available. The introspection system is exposed via special `__schema` and `__type` queries. GraphQL IDEs (like Apollo Studio or GraphiQL) use introspection to provide auto-complete and documentation. In production, introspection is often disabled to prevent attackers from mapping the schema.

**Also known as:** schema introspection

**Related:** [[graphql-schema]], [[resolver]], [[api-security]]

**Example:**
```graphql
# Ask the API what queries are available
{
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
  }
}
```

---

## M

### mutation

**Definition:** In GraphQL, a mutation is an operation that creates, updates, or deletes data — the GraphQL equivalent of a POST, PUT, PATCH, or DELETE in REST. Mutations are defined in the schema's `Mutation` type. Unlike queries, mutations are not expected to be idempotent by default (though individual mutations can be designed to be idempotent). Multiple mutations in one request are executed sequentially, not in parallel.

**Also known as:** GraphQL mutation operation

**Related:** [[graphql-schema]], [[resolver]], [[subscription]]

**Example:**
```graphql
mutation CreatePost($title: String!, $body: String!) {
  createPost(title: $title, body: $body) {
    id
    title
    createdAt
  }
}
```

---

## N

### N+1 problem

**Definition:** A performance anti-pattern that occurs when fetching a list of N items requires N additional database queries (one per item) instead of a single batched query. It is particularly common in GraphQL because resolvers are called independently for each item in a list. The standard solution is the DataLoader pattern, which collects all individual IDs requested in a single tick and issues one batched query.

**Also known as:** N+1 query problem, N+1 select problem

**Related:** [[resolver]], [[graphql-resolvers]], [[federation]]

**Example:**
Fetching 100 posts and the author of each post naively makes 1 query for posts + 100 queries for authors = 101 queries. With DataLoader, it becomes 2 queries total.

---

## O

### OpenAPI

**Definition:** A machine-readable specification format (formerly called Swagger) for describing REST APIs. An OpenAPI document (typically a JSON or YAML file) defines the API's endpoints, request/response schemas, authentication methods, and examples. Tools like Swagger UI, Redoc, and code generators consume OpenAPI documents to produce interactive documentation, client SDKs, and server stubs. OpenAPI 3.1.x is the current version.

**Also known as:** Swagger (name used before OpenAPI 3.0), OAS (OpenAPI Specification)

**Related:** [[endpoint]], [[rest-constraints]], [[rest-advanced]]

**Example:**
```yaml
openapi: "3.1.0"
info:
  title: "Orders API"
  version: "1.0.0"
paths:
  /orders/{id}:
    get:
      summary: "Get an order by ID"
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: "The order"
```

---

## R

### resource

**Definition:** In REST, a resource is any named concept that can be accessed and manipulated through a URI. Resources are the fundamental abstraction — they map to domain entities (users, orders, products) rather than operations. The key insight is that REST exposes *nouns* (resources) via URIs and uses HTTP *verbs* to express operations on them. A well-modeled resource hierarchy is the foundation of a usable REST API.

**Also known as:** REST resource

**Related:** [[endpoint]], [[http-verb]], [[rest-constraints]]

**Example:**
`/users` is a collection resource. `/users/42` is a single resource. `/users/42/orders` is a sub-resource representing all orders belonging to user 42.

---

### resolver

**Definition:** In GraphQL, a resolver is a function responsible for returning the value of a specific field in the schema. Every field in a GraphQL response is ultimately resolved by a function. If no resolver is defined for a field, GraphQL uses a default that returns the property of the same name from the parent object. Resolvers receive four arguments: `parent` (the parent object), `args` (the field's arguments), `context` (shared request context), and `info` (field and schema metadata).

**Also known as:** field resolver

**Related:** [[graphql-schema]], [[mutation]], [[n1-problem]]

**Example:**
```javascript
// Resolver for Query.user — fetches a single user by ID
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      return context.db.users.findById(id);
    }
  }
};
```

---

### REST constraints

**Definition:** The six architectural constraints that Roy Fielding defined as the properties that make an API "RESTful": (1) client-server separation, (2) statelessness (no session state on the server), (3) cacheability, (4) uniform interface (standardised resource addressing and representation), (5) layered system (intermediaries are allowed), and (6) code-on-demand (optional: servers can send executable code to clients). An API that satisfies all constraints gains the scalability and evolvability properties Fielding described.

**Also known as:** REST architectural constraints, Fielding constraints

**Related:** [[statelessness]], [[HATEOAS]], [[resource]]

**Example:**
Statelessness means each HTTP request must contain all information the server needs to process it — no `session_id` cookie that the server uses to look up state. This is why JWTs are popular: the client sends the full token, and the server can validate it without a database lookup.

---

## S

### statelessness

**Definition:** One of Fielding's REST constraints. A stateless server does not store any session state about the client between requests. Every request from a client must include all the information the server needs to fulfill it. The server derives all context from the request itself. This constraint makes REST APIs horizontally scalable (any server instance can handle any request) and simpler to reason about. The tradeoff is that clients must send credentials or tokens on every request.

**Also known as:** stateless constraint, sessionless

**Related:** [[rest-constraints]], [[api-authentication]]

**Example:**
A stateless API uses `Authorization: Bearer <token>` on every request instead of a session cookie that maps to server-side state. Any server in a load-balanced cluster can process any request without sharing session data.

---

### subscription

**Definition:** In GraphQL, a subscription is a long-lived operation where the server pushes updates to the client when specified events occur. Subscriptions are typically implemented over WebSockets (using the `graphql-ws` or legacy `subscriptions-transport-ws` protocol). They are the GraphQL answer to real-time use cases like live dashboards, chat, notifications, and collaborative editing.

**Also known as:** GraphQL subscription operation

**Related:** [[mutation]], [[graphql-schema]], [[event-driven-apis]]

**Example:**
```graphql
subscription OnNewMessage($channelId: ID!) {
  messageSent(channelId: $channelId) {
    id
    body
    author {
      name
    }
  }
}
```
The server pushes new `messageSent` events over a WebSocket connection whenever a message is posted to the specified channel.

---

## Symbols & Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| `{id}` | Path parameter placeholder in URI | `/users/{id}` → `/users/42` |
| `?` | Query string separator | `/users?page=2&limit=20` |
| `&` | Query parameter separator | `?sort=name&order=asc` |
| `!` | Non-null marker in GraphQL SDL | `name: String!` means `name` cannot be null |
| `[Type]` | List type in GraphQL SDL | `friends: [User]` is a list of User objects |

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
