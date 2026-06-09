# Module 07: GraphQL Advanced

[← Module 06: GraphQL Resolvers](../06_graphql-resolvers/README.md) | [Topic Home](../../README.md) | [Next → Module 08: API Security](../08_api-security/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-7h-orange)

> GraphQL subscriptions over WebSocket, schema federation (Apollo Federation), persisted queries, schema stitching vs. federation, and advanced error handling patterns.

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

This module covers the features of GraphQL that take you from building a simple API to building
a production-grade API platform. You will implement real-time functionality with subscriptions,
learn how large organisations split a GraphQL schema across multiple services using federation,
understand persisted queries (which improve security and performance), and master GraphQL's
error handling model — including the distinction between expected errors and unexpected errors.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 06: GraphQL Resolvers — resolver execution model, context, DataLoader

---

## Objectives

By the end of this module, you will be able to:

1. Implement a GraphQL subscription using Apollo Server with the `graphql-ws` protocol
2. Explain the Apollo Federation subgraph/supergraph model and describe when to use it
3. Implement persisted queries and explain the security and performance benefits
4. Distinguish between schema stitching and federation and explain when each is appropriate
5. Implement proper GraphQL error handling: expected errors as union types, unexpected errors as top-level errors

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - Subscriptions: the subscription root type, `asyncIterator`, WebSocket transport (`graphql-ws` vs `subscriptions-transport-ws`), real-time use cases (live dashboards, chat, collaborative editing)
> - Apollo Federation: the "supergraph" concept, subgraphs, `@key` directive for entity references, `@external` and `@requires` directives, the Router/Gateway layer
> - Persisted Queries: how they work (client registers query hash; server caches it), security benefit (prevents arbitrary queries), performance benefit (smaller request payload), automatic persisted queries (APQ)
> - Schema Stitching vs. Federation: stitching is gateway-owned (merge schemas at the gateway), federation is service-owned (each service declares its schema portion); why federation is generally preferred for teams
> - Error Handling: GraphQL's partial success model (`data` + `errors`), expected errors as domain types (union result types), unexpected errors as top-level errors, error extensions for machine-readable codes

---

## Key Concepts

- **Subscription**: A GraphQL operation type for real-time data. The server pushes updates to the client over a persistent connection (WebSocket).
- **asyncIterator**: JavaScript's async iteration protocol used to implement subscription source streams.
- **Apollo Federation**: An architecture for splitting a GraphQL API across multiple services (subgraphs), each owning a portion of the schema.
- **Subgraph**: An independently deployed service that owns a portion of a federated GraphQL schema.
- **Supergraph**: The composed schema that the federation gateway presents to clients, assembled from all subgraph schemas.
- **Persisted query**: A pre-registered query identified by a hash, sent as a short identifier instead of the full query string.
- **Partial success**: GraphQL can return both `data` (partial results) and `errors` in the same response. Some resolvers succeeded while others failed.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: subscription implementation with chat messages, Apollo Federation subgraph definition, error handling with union result types.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: not handling WebSocket reconnection, using federation for a monolith (over-engineering), conflating expected errors with unexpected errors, not disabling introspection and persisting queries in production.

---

## Cross-Links

- [[graphql-rest/modules/06_graphql-resolvers]] — Resolver execution model that subscriptions build on
- [[graphql-rest/modules/10_api-gateway-and-platforms]] — Federation gateways (Apollo Router, Cosmo) are API gateways for GraphQL
- [[graphql-rest/modules/11_event-driven-apis]] — WebSockets (used by subscriptions) vs SSE vs polling comparison
- [[systems-architecture]] — Federation is a distributed systems pattern; understanding service decomposition is relevant

---

## Summary

> [!NOTE]
> Full summary pending.
