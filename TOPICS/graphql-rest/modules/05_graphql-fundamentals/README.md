# Module 05: GraphQL Fundamentals

[← Module 04: API Authentication](../04_api-authentication/README.md) | [Topic Home](../../README.md) | [Next → Module 06: GraphQL Resolvers](../06_graphql-resolvers/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6h-orange)

> GraphQL Schema Definition Language (SDL), types and fields, queries, mutations, variables, fragments, aliases, directives, and introspection.

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

Module 01 introduced GraphQL at a high level. This module begins hands-on GraphQL development.
You will learn to define a schema using the Schema Definition Language (SDL), understand GraphQL's
type system (scalar types, object types, enums, interfaces, unions, input types), write queries
and mutations with variables and fragments, and use introspection to explore a schema
programmatically. By the end, you will be able to work with any GraphQL API confidently.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 01: Introduction to APIs — REST vs. GraphQL first look; over-fetching and under-fetching
- Module 02: REST Fundamentals — helpful for contrast; understanding what GraphQL improves over REST

---

## Objectives

By the end of this module, you will be able to:

1. Write a GraphQL schema in SDL for a given domain with at least 3 types and meaningful relationships
2. Write GraphQL queries using fields, arguments, variables, aliases, and fragments
3. Write GraphQL mutations to create, update, and delete resources
4. Use the `@skip` and `@include` directives to conditionally include fields
5. Use introspection to explore a GraphQL schema's types and fields
6. Explain the GraphQL execution model: how a query is parsed, validated, and resolved

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - GraphQL vs REST: revisiting the fundamental difference — schema + query language vs. fixed endpoints
> - Schema Definition Language (SDL): object types, scalar types (Int, Float, String, Boolean, ID), custom scalars, enum types, interfaces, unions, input types
> - The Schema Root Types: `type Query`, `type Mutation`, `type Subscription` — the three entry points
> - Non-null and list syntax: `String!`, `[User]`, `[User!]!` — what each combination means
> - Writing Queries: field selection, nested fields, arguments, aliases for fetching the same type twice
> - Variables: why variables exist (prevent injection, enable reuse), `$variable: Type` syntax, `variables` object in requests
> - Fragments: named fragment declarations, spreading fragments, inline fragments for union/interface types
> - Directives: `@skip(if: Boolean)` and `@include(if: Boolean)` for conditional field selection
> - Introspection: `__schema`, `__type`, `__typename` — how GraphQL IDEs use introspection
> - GraphQL Execution Model: parsing → validation → execution → response serialisation

---

## Key Concepts

- **SDL (Schema Definition Language)**: The human-readable language for defining a GraphQL schema. The schema is the contract between client and server.
- **Resolver**: A function that returns the value of a specific field. Every field in a GraphQL response is backed by a resolver (covered in depth in Module 06).
- **Variable**: A parameterised value in a GraphQL operation, declared in the operation signature and passed separately from the query string.
- **Fragment**: A reusable selection set that can be spread into multiple operations using `...FragmentName`.
- **Non-null**: A `!` suffix in SDL means a field can never return null. If the resolver returns null for a non-null field, GraphQL propagates the null upward to the nearest nullable parent.
- **Introspection**: GraphQL's built-in capability to query the schema itself. Enabled by default; often disabled in production for security.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: a complete SDL for a blog domain, queries with variables and fragments, mutations, introspection queries, and side-by-side comparison with equivalent REST calls.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: using mutations when queries are correct, not using variables (string interpolation = injection risk), misunderstanding non-null propagation, not understanding that `__typename` is always available.

---

## Cross-Links

- [[graphql-rest/modules/01_introduction]] — Module 01 introduced over-fetching and under-fetching; this module shows how GraphQL solves them concretely
- [[graphql-rest/modules/06_graphql-resolvers]] — The next module: resolver functions, context, and the N+1 problem
- [[graphql-rest/modules/07_graphql-advanced]] — Subscriptions, federation, and advanced schema patterns
- [[django-fastapi-flask]] — Strawberry and Ariadne are Python GraphQL libraries; Strawberry uses Python type annotations to define the schema

---

## Summary

> [!NOTE]
> Full summary pending.
