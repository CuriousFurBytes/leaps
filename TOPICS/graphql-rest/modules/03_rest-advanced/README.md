# Module 03: REST Advanced

[← Module 02: REST Fundamentals](../02_rest-fundamentals/README.md) | [Topic Home](../../README.md) | [Next → Module 04: API Authentication](../04_api-authentication/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6h-orange)

> API versioning strategies, pagination patterns (cursor/offset/page-based), filtering and sorting, HATEOAS in practice, and writing OpenAPI/Swagger specifications.

---

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

---

## Overview

With a solid understanding of REST fundamentals, this module explores the challenges that arise
as APIs evolve: versioning (how to make breaking changes without breaking clients), pagination
(how to handle large collections efficiently), filtering and sorting (how to give clients control
over what subset of data they receive), HATEOAS (the hypermedia constraint in practice), and
finally OpenAPI — the machine-readable contract format that allows tools to generate documentation,
test clients, and server stubs automatically from your API design.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 02: REST Fundamentals — resource modeling, HTTP methods, status codes

---

## Objectives

By the end of this module, you will be able to:

1. Choose between URL path, query parameter, and header-based API versioning and justify the choice
2. Implement cursor-based and offset-based pagination and explain the tradeoffs of each
3. Design a filtering and sorting query parameter scheme for a collection endpoint
4. Write an OpenAPI 3.x specification for a 3-resource API with authentication
5. Describe HATEOAS and explain why most practical REST APIs don't fully implement it

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - API Versioning: URL path (`/v1/`, `/v2/`), query param (`?version=2`), header (`Accept: application/vnd.api+json;version=2`), content negotiation — tradeoffs of each
> - Pagination: offset/limit pagination (simple but has drift problem), cursor-based pagination (stable but stateful cursors), page-number pagination (user-friendly but inconsistent with deletions)
> - Filtering: `?field=value`, range filters (`?created_after=2026-01-01`), multiple value filters (`?status=active,pending`)
> - Sorting: `?sort=name&order=asc`, compound sorting `?sort=created_at,name`
> - HATEOAS: what full HATEOAS looks like in practice, why most APIs skip it, HAL format, JSON:API format
> - OpenAPI: document structure, paths, components/schemas, security schemes, Swagger UI

---

## Key Concepts

- **API versioning**: The practice of marking an API version so clients can pin to a version and continue working as the API evolves.
- **Breaking change**: A change to an API that requires existing clients to update their code (e.g., removing a field, changing a type, renaming an endpoint).
- **Cursor-based pagination**: Pagination using an opaque cursor (a pointer to a position in the dataset) rather than a page number. Stable when records are inserted or deleted.
- **Offset pagination**: Pagination using `offset` + `limit` to skip N records. Simple but produces inconsistent results when records change between requests.
- **OpenAPI (Swagger)**: A machine-readable specification format for describing REST APIs. The OAS 3.1 spec is the current version.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: a versioned API with migration guide, a cursor-paginated endpoint, an OpenAPI spec for a simple API.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: versioning too late, not thinking about pagination from day one, OpenAPI drift (spec not matching implementation), offset pagination in high-volume APIs.

---

## Cross-Links

- [[graphql-rest/modules/02_rest-fundamentals]] — builds directly on resource modeling and HTTP method semantics
- [[graphql-rest/modules/04_api-authentication]] — OpenAPI includes security scheme definitions; auth and versioning interact
- [[django-fastapi-flask]] — FastAPI generates OpenAPI automatically; Spring Boot uses Springdoc/Swagger integration
- [[systems-architecture]] — API versioning strategy is an architectural decision with long-term consequences

---

## Summary

> [!NOTE]
> Full summary pending.
