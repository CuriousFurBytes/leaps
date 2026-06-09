# Module 09: API Testing

[← Module 08: API Security](../08_api-security/README.md) | [Topic Home](../../README.md) | [Next → Module 10: API Gateway and Platforms](../10_api-gateway-and-platforms/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-6h-orange)

> Contract testing with Pact, Postman/Newman for REST API testing, REST Assured for Java, Apollo Studio testing tools, and performance/load testing APIs.

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

Testing APIs is fundamentally different from testing UI code. APIs are contracts — they must be
tested at the contract level, the integration level, and the performance level. This module covers
the spectrum of API testing: contract tests that verify the API matches its specification, integration
tests that verify end-to-end behaviour, Postman collections for exploratory and regression testing,
and performance testing to ensure the API meets latency and throughput requirements under load.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 03: REST Advanced — OpenAPI specs are the contracts that contract tests verify
- Module 05: GraphQL Fundamentals — GraphQL schema is the contract for GraphQL tests
- Module 08: API Security — some testing overlap with security testing (fuzzing, auth testing)

---

## Objectives

By the end of this module, you will be able to:

1. Write a consumer-driven contract test using Pact for a REST API endpoint
2. Create a Postman collection with tests and run it with Newman in CI
3. Write integration tests for a GraphQL API using Apollo Studio's built-in testing features
4. Design and run a simple load test for an API endpoint and interpret the results
5. Explain the testing pyramid applied to APIs: unit, integration, contract, and E2E tests

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - The API Testing Pyramid: unit tests (resolver functions in isolation), integration tests (full API call with test database), contract tests (consumer-driven contracts), E2E tests (real system calls)
> - Consumer-Driven Contract Testing with Pact: how Pact works (consumer writes contract, provider verifies it), the Pact broker, why contract tests catch breaking changes that unit tests miss
> - Postman and Newman: collection structure, test scripts (pm.expect() assertions), environments and variables, running collections in CI with Newman
> - REST Assured (Java): BDD-style API testing, `given().when().then()` syntax, response body matchers
> - GraphQL Testing: testing schemas with Jest/Vitest, Apollo Studio's built-in testing, schema diffing to detect breaking changes
> - Performance Testing: k6 for API load testing, key metrics (p95/p99 latency, throughput, error rate), performance budgets, interpreting results

---

## Key Concepts

- **Contract test**: A test that verifies an API matches its published specification (OpenAPI or Pact contract). Catches breaking changes before they reach production.
- **Consumer-driven contract (CDC)**: A testing pattern where the consumer of an API defines what it expects (the "contract"), and the provider verifies it can satisfy that contract.
- **Pact**: A consumer-driven contract testing framework that allows consumers and providers to test their integration point independently.
- **Newman**: The command-line companion for Postman; runs Postman collections in CI environments without the Postman GUI.
- **k6**: An open-source load testing tool for APIs. Tests are written in JavaScript; results are human-readable or exportable to Grafana.
- **p95 latency**: The 95th percentile latency — 95% of requests complete in this time or less. A more meaningful performance metric than average latency.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: Pact consumer contract for a REST endpoint, Postman collection with assertions, k6 load test script with results interpretation.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: testing implementation instead of contract (brittle tests), not running contract tests in CI, interpreting average latency instead of p95/p99, not testing error responses (only happy paths).

---

## Cross-Links

- [[graphql-rest/modules/03_rest-advanced]] — OpenAPI spec is the contract that Pact and spec-based tests verify
- [[graphql-rest/modules/05_graphql-fundamentals]] — GraphQL schema is the contract for GraphQL testing
- [[graphql-rest/modules/12_capstone-project]] — The capstone requires a test suite; this module provides the tools
- [[devops-platform-engineering]] — CI/CD pipelines run contract and integration tests on every PR

---

## Summary

> [!NOTE]
> Full summary pending.
