# Resources — Module 01: Introduction to APIs

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[MDN HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)** — Mozilla Developer Network

Covers the fundamentals of HTTP that underpin everything in this module: request/response model,
methods, headers, status codes, and the stateless nature of HTTP. Free, accurate, and maintained
by Mozilla. Read before or alongside this module to reinforce the theory.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[MDN HTTP Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP)** — Complete HTTP reference: methods, status codes, headers. The authoritative free reference.
- **[GraphQL Introduction](https://graphql.org/learn/)** — Official GraphQL introduction at graphql.org. Covers why GraphQL exists and the basics of the query language.
- **[Python requests library](https://requests.readthedocs.io/en/latest/)** — Official documentation for the `requests` library used in this module's code examples.
- **[curl documentation](https://curl.se/docs/)** — Official curl documentation. The "Everything curl" book at curl.se/book is particularly useful.

---

## Relevant Background

_For the historical context covered in this module._

| Resource | Notes |
|----------|-------|
| Roy Fielding's Dissertation, Chapter 5 | [Verify URL at UCI repository] — The original REST definition. Chapter 5 is surprisingly readable. Recommended for understanding why each constraint exists. |
| [GraphQL: A data query language (Facebook Engineering Blog)](https://engineering.fb.com/2015/09/14/core-data/graphql-a-data-query-language/) | Facebook's original 2015 announcement post. Explains the problems GraphQL solved at Facebook's scale. |

---

## Videos

_Specific videos that explain this module's concepts well._

- **[Verify: "What is REST?" video — confirm specific recommended video title and creator]** — _Add after verifying a specific high-quality video_
- **[Verify: Roy Fielding explaining REST constraints in a talk — confirm existence and URL]** — _Add after verifying_

---

## Practice Sites

_Places to get more practice with the skills in this module._

- **[JSONPlaceholder](https://jsonplaceholder.typicode.com/)** — Free fake REST API for testing. Used in the module exercises. Perfect for practicing curl and Python requests without setting up a server.
- **[httpbin.org](https://httpbin.org/)** — A simple HTTP request and response service. Send requests and inspect exactly what the server received — invaluable for understanding HTTP headers.
- **[ReqRes](https://reqres.in/)** — Another fake REST API with realistic user/resource data. Good for practicing POST/PUT/DELETE with realistic responses.

---

## Related Modules in This Topic

_Other modules in this topic that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[modules/02_rest-fundamentals]] (Module 02: REST Fundamentals) | Builds directly on the HTTP and REST concepts introduced here; covers resource modeling and status codes in depth |
| [[modules/05_graphql-fundamentals]] (Module 05: GraphQL Fundamentals) | This module gives the "why" for GraphQL; Module 05 gives the "how" — schemas, queries, mutations |
| [[modules/04_api-authentication]] (Module 04: API Authentication) | Module 01 introduces the statelessness question; Module 04 answers how authentication works in a stateless context |

---

## Related Modules in Other Topics

_Modules from other topics in the knowledge base that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[networks]] | HTTP module | HTTP fundamentals from the network perspective — transport layer, TLS, DNS resolution |
| [[django-fastapi-flask]] | FastAPI module | Building REST APIs in Python — the server side of what Module 01 shows from the client side |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] Roy Fielding dissertation URL at UCI — needs direct link verification
- [ ] Recommended introductory REST video — not yet identified; evaluate before adding
