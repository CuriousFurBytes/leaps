# Module 02: REST Fundamentals

[← Module 01: Introduction](../01_introduction/README.md) | [Topic Home](../../README.md) | [Next → Module 03: REST Advanced](../03_rest-advanced/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green)
![Time](https://img.shields.io/badge/time-5h-orange)

> A deep dive into REST resource modeling, URI design, HTTP method semantics, status code taxonomy, statelessness, and idempotency — the practical foundation for building and consuming real REST APIs.

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

Module 01 introduced REST as an architectural style and HTTP as the transport layer.
This module goes deep on the practical building blocks you need to design and consume
real REST APIs: how to model resources, how to structure URIs, what each HTTP method
actually guarantees, the complete HTTP status code taxonomy, and the crucial concepts
of statelessness and idempotency that determine how clients should handle failures.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.
> See the [ROADMAP.md](../../ROADMAP.md) for the learning sequence.

---

## Prerequisites

- Module 01: Introduction to APIs — HTTP anatomy, REST constraints overview, first API calls

---

## Objectives

By the end of this module, you will be able to:

1. Design a REST resource model for a given domain using correct plural noun URI conventions
2. Apply the correct HTTP method for any given operation and explain its idempotency and safety guarantees
3. Select the appropriate HTTP status code for success, client error, and server error responses
4. Explain what statelessness means in practice and how JWT enables stateless authentication
5. Define idempotency and explain why it matters for retry logic in distributed systems
6. Critique a real-world API's URI design and suggest improvements

---

## Theory

> [!NOTE]
> Full theory content is pending for this stub module.
> The following subsections will be written in full:
> - Resource Modeling: thinking in nouns, not verbs
> - URI Design Patterns: collection resources, singleton resources, sub-resources, query parameters
> - HTTP Method Semantics: GET, POST, PUT, PATCH, DELETE — safety, idempotency, and when to use each
> - HTTP Status Code Taxonomy: 2xx success, 3xx redirect, 4xx client error, 5xx server error
> - Statelessness in Practice: JWT as a stateless auth mechanism
> - Idempotency in Practice: why DELETE and PUT must be idempotent, how to use idempotency keys

---

## Key Concepts

- **Resource**: A named, addressable concept in a REST API. Modeled as a noun, not a verb.
- **Collection resource**: A URI that represents a set of resources (e.g., `/users`).
- **Singleton resource**: A URI that represents a single resource (e.g., `/users/42`).
- **Safe operation**: An HTTP operation that does not modify server state (GET, HEAD, OPTIONS).
- **Idempotent operation**: An operation where multiple identical calls produce the same result as one call (GET, PUT, DELETE, HEAD, OPTIONS).
- **Idempotency key**: A client-generated unique ID sent with a request so the server can detect and ignore duplicate requests (used in Stripe and other payment APIs).

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include:
> - A complete resource model for an e-commerce API (products, orders, users, reviews)
> - A set of cURL examples demonstrating all HTTP methods
> - A Python `requests` client implementing full CRUD for a resource
> - Status code selection for a set of realistic API scenarios

---

## Common Pitfalls

> [!NOTE]
> Full Common Pitfalls section pending. Will cover:
> - Using POST for reads (non-idempotent reads cause problems)
> - Treating 404 and 403 as interchangeable (they have very different security implications)
> - Using 200 instead of 204 for DELETE responses (200 implies a body; 204 means no content)
> - Nesting resources too deeply (`/users/1/orders/2/items/3/discounts/4` is unmaintainable)

---

## Cross-Links

- [[graphql-rest/modules/01_introduction]] — HTTP fundamentals and REST constraints that this module builds on
- [[graphql-rest/modules/03_rest-advanced]] — The next module: versioning, pagination, filtering, OpenAPI
- [[networks]] — The network layer that HTTP runs on; relevant for understanding caching and connection semantics
- [[django-fastapi-flask]] — FastAPI implements all the resource patterns covered in this module; comparing the theory with the framework makes both clearer

---

## Summary

> [!NOTE]
> Full summary pending. Will recap:
> - The resource modeling discipline (nouns not verbs, plural collection URIs)
> - HTTP method semantics and the safety/idempotency matrix
> - HTTP status code taxonomy by category
> - Why idempotency matters for fault-tolerant distributed systems
> - How statelessness and JWT work together in practice
