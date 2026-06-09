# Module 08: API Security

[← Module 07: GraphQL Advanced](../07_graphql-advanced/README.md) | [Topic Home](../../README.md) | [Next → Module 09: API Testing](../09_api-testing/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-6h-orange)

> CORS policies, rate limiting strategies, input validation and sanitization, injection prevention in GraphQL, API abuse patterns, and security headers.

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

Authentication (Module 04) answers "who are you?" Security answers "what can go wrong even
after you know who someone is?" This module covers the security concerns specific to APIs:
the same-origin policy and CORS, rate limiting to prevent abuse, input validation to prevent
injection attacks, GraphQL-specific vulnerabilities (deeply nested queries, introspection abuse,
field suggestion attacks), and the common API abuse patterns that security teams must defend against.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 04: API Authentication — authentication and authorisation concepts
- Module 05: GraphQL Fundamentals — GraphQL-specific attacks require understanding the query model

---

## Objectives

By the end of this module, you will be able to:

1. Configure CORS correctly for a REST API, distinguishing simple and preflight requests
2. Implement rate limiting per client/IP/endpoint and select appropriate rate limit headers
3. Validate and sanitise API inputs to prevent injection and data corruption
4. Protect a GraphQL API against introspection, query depth, and query complexity attacks
5. Identify and describe the OWASP API Security Top 10 threats
6. Implement security headers (HSTS, Content-Security-Policy, X-Content-Type-Options)

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - CORS (Cross-Origin Resource Sharing): same-origin policy, preflight requests (OPTIONS), `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, wildcard `*` dangers, CORS misconfiguration
> - Rate Limiting: token bucket vs. leaky bucket vs. sliding window algorithms, rate limit headers (`X-RateLimit-Remaining`, `Retry-After`), rate limiting by IP vs. by API key vs. by user
> - Input Validation: whitelist vs. blacklist validation, SQL injection via API parameters, JSON Schema validation, type coercion attacks
> - GraphQL-Specific Attacks: introspection schema mapping, deeply nested query attacks (DoS), query complexity limiting, field suggestion attacks (`Did you mean...?`), persisted queries as a mitigation
> - OWASP API Security Top 10: Broken Object Level Authorization, Broken Authentication, Excessive Data Exposure, Lack of Rate Limiting, Broken Function Level Authorization, etc.
> - Security Headers: HSTS, Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Referrer-Policy

---

## Key Concepts

- **CORS (Cross-Origin Resource Sharing)**: An HTTP header mechanism that allows or restricts web applications running at one origin to make requests to a different origin.
- **Preflight request**: An HTTP OPTIONS request sent by browsers before cross-origin requests that use non-simple methods or headers, to check if the server allows the cross-origin request.
- **Rate limiting**: A mechanism to control the number of requests a client can make to an API within a time window.
- **Token bucket**: A rate limiting algorithm where a "bucket" of tokens refills at a fixed rate; each request consumes a token; requests are rejected when the bucket is empty.
- **Query depth limiting**: A GraphQL security control that rejects queries deeper than a configured maximum nesting level, preventing deeply nested DoS attacks.
- **Query complexity**: A calculated score for a GraphQL query based on the number and type of fields requested; used to reject expensive queries before execution.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: CORS configuration for a FastAPI API, rate limiting middleware, GraphQL depth/complexity limiting, input validation with Pydantic.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: `Access-Control-Allow-Origin: *` with credentials, not rate-limiting per user (only per IP), trusting client-side validation, leaving introspection enabled in production without authentication.

---

## Cross-Links

- [[graphql-rest/modules/04_api-authentication]] — Authentication is a prerequisite for access control
- [[graphql-rest/modules/07_graphql-advanced]] — Persisted queries as a GraphQL security control
- [[graphql-rest/modules/09_api-testing]] — Security testing: fuzzing, penetration testing techniques for APIs
- [[networks]] — TLS/HTTPS is the transport-layer security that protects API traffic in transit

---

## Summary

> [!NOTE]
> Full summary pending.
