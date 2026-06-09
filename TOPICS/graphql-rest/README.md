# GraphQL and REST

> Learn how to design, build, evaluate, secure, and operate HTTP APIs using REST and GraphQL from first principles through production architecture.

## Table of Contents
1. [Why Learn GraphQL and REST?](#why-learn-graphql-and-rest)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)
6. [Learning Strategy](#learning-strategy)

## Why Learn GraphQL and REST?

Most modern software is a conversation between systems. Browsers talk to backends, mobile apps synchronize with services, internal tools coordinate with databases, and partners integrate through documented contracts. REST and GraphQL are two of the most important ways teams structure those conversations over HTTP.

REST grew from Roy Fielding's architectural work on the web: resources, representations, links, caches, and uniform interfaces. GraphQL emerged at Facebook to solve product-development pain around evolving client data needs. Knowing both lets you avoid tribal arguments and instead choose based on constraints: cache behavior, client autonomy, operational visibility, schema governance, authorization, and team workflow.

This topic teaches the mechanics and the judgment. You will start at ground zero with HTTP requests and responses, move into REST resource design, learn GraphQL schemas and resolver execution, compare tradeoffs honestly, and finish by building a realistic API platform that exposes both styles for the same domain.

## Prerequisites

- Basic programming literacy in any language: variables, functions, control flow, and data structures.
- Basic command-line comfort: running a script, reading output, and editing text files.
- Helpful but not required: [[web-development]], [[databases]], [[security]], and [[software-architecture]].

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [HTTP API Foundations](./modules/01_http_api_foundations/README.md) | Beginner | [ ] |
| 02 | [REST Resource Design](./modules/02_rest_resource_design/README.md) | Beginner | [ ] |
| 03 | [GraphQL Schema and Queries](./modules/03_graphql_schema_and_queries/README.md) | Intermediate | [ ] |
| 04 | REST Workflows, Versioning, and Hypermedia | Intermediate | [ ] |
| 05 | GraphQL Mutations, Input Design, and Errors | Intermediate | [ ] |
| 06 | Authentication, Authorization, and Abuse Resistance | Advanced | [ ] |
| 07 | Caching, Pagination, and Performance | Advanced | [ ] |
| 08 | Tooling, Documentation, and Contract Testing | Advanced | [ ] |
| 09 | API Evolution, Backward Compatibility, and Governance | Advanced | [ ] |
| 10 | Federation, Gateways, and Backend-for-Frontend Patterns | Expert | [ ] |
| 11 | Observability, Incident Response, and Production Judgment | Expert | [ ] |
| 12 | [Capstone API Platform](./modules/12_capstone_api_platform/README.md) | Expert | [ ] |

## Cross-Links

- [[web-development]] for browsers, HTTP clients, and frontend integration.
- [[databases]] for persistence, indexing, transactions, and query planning.
- [[security]] for authentication, authorization, threat modeling, and input validation.
- [[software-architecture]] for service boundaries, gateways, and maintainability tradeoffs.

## Quick Reference

| Need | REST Habit | GraphQL Habit |
|---|---|---|
| Read one thing | `GET /articles/123` | `query { article(id: "123") { title } }` |
| Create one thing | `POST /articles` | `mutation { createArticle(input: ...) { article { id } } }` |
| Update one thing | `PATCH /articles/123` | `mutation { updateArticle(id: "123", input: ...) { article { id } } }` |
| Delete one thing | `DELETE /articles/123` | `mutation { deleteArticle(id: "123") { deletedId } }` |
| Cache public reads | HTTP cache headers and stable URLs | Persisted queries, response caching, or application caches |
| Discover contract | OpenAPI, examples, docs | Schema introspection, SDL, generated docs |

```bash
# Inspect a REST-style endpoint.
curl -i https://api.example.test/articles/123
```

```graphql
# Ask GraphQL for exactly the fields the client needs.
query ArticleCard($id: ID!) {
  article(id: $id) {
    id
    title
    author {
      name
    }
  }
}
```

## Learning Strategy

Work through the first three modules in order. They establish the vocabulary needed for every later architectural choice. When you reach the capstone, do not copy a complete solution from elsewhere; use the milestones and help sections to make your own design decisions, document tradeoffs, and iterate as a practitioner would.
