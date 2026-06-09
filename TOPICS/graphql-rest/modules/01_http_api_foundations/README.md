# Module 01: HTTP API Foundations

> HTTP messages, URLs, methods, status codes, headers, and JSON API contracts.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

HTTP API Foundations teaches the mental model behind http messages, urls, methods, status codes, headers, and json api contracts. APIs are not just routes or schemas; they are long-lived contracts between people, programs, teams, and operational systems. A good API lets clients ask for useful work while protecting invariants, performance, and security.

Historically, HTTP gave the web a simple message protocol, REST described architectural constraints that made the web scalable, and GraphQL later introduced a typed query language for client-directed data selection. This module keeps those histories practical: each concept is tied to what you would actually type, observe, debug, and document.

## Prerequisites

- No prior module required; this is the starting point.
- Basic programming literacy and familiarity with JSON-like data.
- Ability to run command-line examples and read request-response output.

## Objectives

By the end of this module, you will be able to:

- Explain the main design problem this module solves.
- Read and write small API examples using the relevant protocol style.
- Debug common mistakes by inspecting requests, responses, schemas, or resource models.
- Compare REST and GraphQL choices without treating either as universally superior.
- Document API behavior clearly enough for another developer to use it.

## Theory

### Contracts, Not Just Endpoints

An API contract says what a client may ask, what the server promises in return, and what both sides must not assume. In REST, much of the contract is distributed across URLs, HTTP methods, status codes, headers, and representations. In GraphQL, much of the contract is centralized in the schema and expressed through typed operations. Both styles still need examples, error semantics, authorization rules, rate limits, and evolution policies.

```bash
# A simple HTTP request shows method, path, headers, and response metadata.
curl -i -H "Accept: application/json" https://api.example.test/articles/123
```

The important habit is to read the whole exchange. A status code without a response body may be ambiguous. A JSON body without headers may be hard to cache. A GraphQL response with `errors` and partial `data` can be successful at the transport layer but still require application-level handling.

### Shape, Identity, and Change

REST usually starts with resource identity: what things exist, what stable URLs identify them, and which representations clients need. GraphQL usually starts with a graph-shaped type system: what objects exist, how they relate, and which fields clients may select. These starting points influence everything downstream. REST makes HTTP infrastructure useful because URLs and methods are visible to caches and logs. GraphQL makes client evolution easier because clients can request different field selections without asking the server team for a new endpoint each time.

```json
{
  "id": "art_123",
  "title": "Designing APIs",
  "author": {
    "id": "usr_9",
    "name": "Ada"
  }
}
```

This JSON representation could be returned by a REST endpoint or selected by a GraphQL query. The difference is not JSON itself; it is where the selection logic, evolution rules, and operational controls live.

### Operational Reality

Production APIs are shaped by constraints: latency, authorization, caching, observability, backward compatibility, and abuse resistance. A beautiful schema can fail if resolvers create an N+1 query storm. A clean REST resource model can fail if pagination is unstable or error messages leak sensitive details. Expert practice means designing for the system that will operate the API, not just for the first demo.

```graphql
query ArticlePreview($id: ID!) {
  article(id: $id) {
    id
    title
    author {
      name
    }
  }
}
```

The query above is readable and client-friendly, but the server must still enforce authorization, limit complexity, batch data loading, and return errors consistently. REST has equivalent responsibilities, usually distributed across route handlers, middleware, and OpenAPI documentation.

## Key Concepts

- **API contract** — The durable agreement between client and server. It includes inputs, outputs, errors, side effects, and compatibility promises.
- **Resource** — A conceptual thing exposed by an API, such as an article, account, invoice, or search result. REST emphasizes resources as stable identities with representations.
- **Representation** — The serialized form of a resource at a moment in time, commonly JSON. A representation is not the same thing as the database row behind it.
- **Schema** — A typed description of available GraphQL operations and fields. The schema is executable documentation because tools can validate queries against it.
- **Resolver or handler** — Server code that fulfills part of an API request. REST handlers usually map to routes; GraphQL resolvers usually map to fields.
- **Backward compatibility** — The discipline of evolving an API without breaking existing clients. It is a product and operations concern, not merely a syntax concern.

## Examples

### Example 1: Read a Resource with REST

Problem: a client needs the title and author for one article.

```bash
# Request one article representation from a stable URL.
curl -s https://api.example.test/articles/art_123
```

A REST design makes the article URL easy to log, cache, bookmark, and document. If the representation becomes too large for some clients, you can introduce sparse fields, a separate projection endpoint, or a GraphQL layer depending on product needs.

### Example 2: Select Fields with GraphQL

Problem: a card component needs only three fields from an article graph.

```graphql
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

GraphQL moves selection power to the client. That helps fast-moving UI teams, but the server must measure query cost and prevent overly expensive graph traversals.

## Common Pitfalls

### Pitfall 1: Treating JSON as the Architecture

Wrong approach:

```json
{
  "endpoint": "anything that returns JSON is REST"
}
```

Correct approach:

```text
REST is about resources, representations, uniform interface constraints, cacheability, and stateless interactions; JSON is only one possible representation format.
```

The mistake happens because many tutorials call every HTTP JSON API "REST." Use the architectural constraints to reason about design quality.

### Pitfall 2: Ignoring Error Semantics

Wrong approach:

```json
{
  "success": false,
  "message": "failed"
}
```

Correct approach:

```json
{
  "type": "validation_error",
  "message": "Title is required.",
  "fields": {
    "title": "required"
  }
}
```

Vague errors slow down client developers and make operations harder. Good APIs distinguish validation, authentication, authorization, conflict, not-found, and server failures.

### Pitfall 3: Designing for the First Screen Only

Wrong approach:

```graphql
query HomePageOnly {
  articles {
    title
  }
}
```

Correct approach:

```graphql
query Articles($first: Int!, $after: String) {
  articles(first: $first, after: $after) {
    edges {
      cursor
      node {
        id
        title
      }
    }
  }
}
```

The first screen is not the full lifecycle. Plan for pagination, stable identifiers, authorization, and future fields before clients depend on fragile shortcuts.

## Cross-Links

- [[web-development]]
- [[databases]]
- [[security]]
- [[software-architecture]]

## Summary

- REST and GraphQL are different ways to structure API contracts over HTTP.
- REST emphasizes resources, representations, and HTTP semantics.
- GraphQL emphasizes a typed schema and client-selected fields.
- Production API design must consider errors, caching, security, compatibility, and observability.
- The best choice depends on constraints, not fashion.
