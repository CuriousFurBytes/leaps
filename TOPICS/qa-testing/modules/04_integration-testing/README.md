# Module 04: Integration Testing

[← Mocking and Test Doubles](../03_mocking-and-test-doubles/) | [Topic Home](../../README.md) | [Next → End-to-End Testing](../05_e2e-testing/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-6--8h-orange)

---

> Testing across component boundaries — TestContainers for real databases in tests, HTTP client testing, file system integration, in-memory vs. real dependencies.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- What integration testing is and why it complements (not replaces) unit testing
- Testing with real databases using TestContainers (Python and JavaScript) — spinning up PostgreSQL, MySQL, Redis in Docker for tests
- pytest fixtures for database setup and teardown — transaction rollback patterns
- Testing HTTP clients — using `httpx.AsyncClient` with a test app, `supertest` in Node.js
- In-memory vs. real dependency trade-offs — when SQLite is fine, when you need the real database
- File system testing — using `tmp_path` in pytest, `os.tmpdir()` in Node.js
- Test data management — factories, fixtures, and seed data strategies
- Testing Django and Flask applications — the `test_client()` pattern

## Prerequisites

- Module 03: Mocking and Test Doubles in this topic
- Basic understanding of databases (SQL), HTTP (REST), or file I/O

## Objectives

By the end of this module, you will be able to:

1. Write integration tests that use a real PostgreSQL database in a Docker container
2. Test a REST API endpoint with a real HTTP client against a running test application
3. Apply pytest fixtures with appropriate scope for database setup/teardown
4. Distinguish between scenarios where in-memory substitutes are appropriate vs. where real dependencies are required
5. Manage test data effectively across a test suite using factories and seed data

## Cross-Links

- [[qa-testing/modules/03_mocking-and-test-doubles]] — The contrast between mocking (unit) and real dependencies (integration) is the central distinction
- [[qa-testing/modules/06_api-testing]] — API testing extends integration testing to HTTP interfaces specifically
- [[django-fastapi-flask]] — Django's `TestCase` and FastAPI's `TestClient` are integration testing tools
