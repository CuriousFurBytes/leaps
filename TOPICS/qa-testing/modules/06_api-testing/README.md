# Module 06: API Testing and Contract Testing

[← End-to-End Testing](../05_e2e-testing/) | [Topic Home](../../README.md) | [Next → Test-Driven Development](../07_test-driven-development/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

> REST API testing with httpx and Requests; consumer-driven contract testing with Pact; OpenAPI response validation; Newman for Postman collection automation.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- REST API testing strategies — testing HTTP methods, status codes, headers, and response bodies
- Python API testing with `httpx` — async test client, response assertions, auth headers
- Consumer-driven contract testing with Pact — the consumer/provider model, writing consumer tests, provider verification
- OpenAPI validation — using `openapi-core` or `schemathesis` to validate responses against an OpenAPI spec
- Newman — running Postman collections from the command line in CI
- Testing authentication — JWT tokens, API keys, OAuth flows in integration tests
- GraphQL testing — query testing, mutation testing, schema validation
- Fuzz testing APIs — using Schemathesis to generate adversarial inputs automatically

## Prerequisites

- Module 04: Integration Testing in this topic
- Basic understanding of REST APIs — HTTP methods, status codes, JSON

## Objectives

By the end of this module, you will be able to:

1. Write HTTP-level integration tests for a REST API using `httpx` or `supertest`
2. Implement consumer-driven contract tests with Pact to verify service compatibility
3. Validate API responses against an OpenAPI specification
4. Identify the scenarios where contract testing provides more value than full integration tests
5. Run Postman collections in CI using Newman

## Cross-Links

- [[qa-testing/modules/04_integration-testing]] — API testing is a specialized form of integration testing
- [[django-fastapi-flask]] — FastAPI generates OpenAPI specs automatically; this module's validation techniques apply directly
- [[qa-testing/glossary#contract-test]] — Formal definition of contract tests
