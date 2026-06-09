# Module 06: GraphQL Resolvers

[← Module 05: GraphQL Fundamentals](../05_graphql-fundamentals/README.md) | [Topic Home](../../README.md) | [Next → Module 07: GraphQL Advanced](../07_graphql-advanced/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-6h-orange)

> Resolver functions, the context object, the N+1 problem explained and solved with the DataLoader pattern, batch loading strategies, and resolver performance optimisation.

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

Module 05 introduced GraphQL's schema and query language. This module goes under the hood:
how does GraphQL actually *execute* a query? You will learn how resolver functions work, what
the four resolver arguments are and when to use each, how to share request-scoped data via the
context object, and — critically — how to diagnose and fix the N+1 problem, the most common
performance issue in GraphQL APIs. The DataLoader pattern is the standard solution, and mastering
it is essential for production-quality GraphQL.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 05: GraphQL Fundamentals — SDL, types, queries, mutations

---

## Objectives

By the end of this module, you will be able to:

1. Explain GraphQL's execution model: how the execution engine calls resolvers, in what order, and with what arguments
2. Implement resolver functions for Query, Mutation, and type-level fields
3. Use the context object to share a database connection, authenticated user, and request metadata across resolvers
4. Identify the N+1 problem in a GraphQL API by counting database queries
5. Implement the DataLoader pattern to batch and cache database lookups
6. Measure before/after resolver performance using query logging

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - GraphQL Execution Model: the execution engine resolves the query tree depth-first; Promise.all for parallel sibling field resolution; the resolver chain from root to leaf
> - Resolver Function Signature: `(parent, args, context, info)` — what each argument contains and when to use each
> - Default Resolvers: GraphQL auto-generates resolvers that return `parent[fieldName]`; when this is enough and when it isn't
> - The Context Object: what to put in context (DB connection, authenticated user, loaders, request ID), how to pass it to Apollo Server / Strawberry
> - The N+1 Problem: illustrated with a 100-posts query; how each post's author resolver fires independently; proof via query counting
> - DataLoader Pattern: collect phase (one event loop tick), batch function, cache per request; `new DataLoader(batchFn)` usage; keyed vs. non-keyed batching
> - Advanced DataLoader: priming the cache, clearing the cache, compound keys, handling partial batch failures

---

## Key Concepts

- **Resolver chain**: The sequence of resolver function calls as GraphQL traverses the query tree from root types to leaf scalar fields.
- **Parent argument**: The first resolver argument; contains the value returned by the parent field's resolver. For root-level resolvers (Query/Mutation fields), parent is `null` or `undefined`.
- **Context**: A shared object passed to every resolver in a single operation. Used to pass database connections, authenticated user, DataLoaders, and request metadata.
- **N+1 problem**: A performance anti-pattern where fetching N parent objects triggers N additional queries for related data — one per parent — instead of one batched query.
- **DataLoader**: A utility that batches individual data fetches that occur within a single event loop tick into a single bulk request. Created per-request to avoid cross-request data leakage.
- **Batch function**: The function passed to DataLoader that receives an array of keys and must return an array of values in the same order.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: a complete Apollo Server with context, demonstrating the N+1 problem with query logging, implementing DataLoader and proving the fix, DataLoader with cache priming.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: sharing a DataLoader instance across requests (cache pollution), not maintaining key order in batch functions, over-using context for state that should be in function arguments.

---

## Cross-Links

- [[graphql-rest/modules/05_graphql-fundamentals]] — SDL and query execution model this module builds on
- [[graphql-rest/modules/07_graphql-advanced]] — Subscriptions and federation build on resolver concepts
- [[graphql-rest/modules/09_api-testing]] — Testing resolvers in isolation and testing DataLoader batching
- [[systems-architecture]] — The N+1 problem also appears in REST (the under-fetching problem); DataLoader is GraphQL's solution; SQL JOINs and eager loading are the ORM-level equivalent

---

## Summary

> [!NOTE]
> Full summary pending.
