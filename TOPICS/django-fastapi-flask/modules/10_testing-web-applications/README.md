# Module 10: Testing Web Applications — pytest, TestClient, Mocking, factory_boy, and Coverage

[← Module 09: Authentication and Security](../09_authentication-and-security/README.md) | [Topic Home](../../README.md) | [Next → Module 11: Deployment and Production](../11_deployment-and-production/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-5--7h-orange)

> **Stub module.** This module covers pytest fixtures for web testing, the Flask and FastAPI test clients, mocking database layers, factory_boy for test data generation, and measuring coverage. Full content to be generated on demand.

---

## Overview

A web application without tests is a web application you are afraid to change. This module teaches you to write tests for Flask, Django, and FastAPI applications that give you genuine confidence — not just coverage percentages, but tests that catch real bugs and enable safe refactoring.

The focus is on practical test patterns: fixture design, test isolation, realistic test data generation, and the judgment to know what to test and what not to test.

---

## Prerequisites

- Modules 03, 05, 06 — building applications in each framework
- Basic pytest — writing `def test_` functions, assertions, running pytest

---

## Objectives

By the end of this module, you will be able to:

1. Write pytest fixtures that provide a test application, test database, and authenticated test client for each framework
2. Test Flask routes using `app.test_client()` with the application factory pattern
3. Test FastAPI routes using `fastapi.testclient.TestClient` and override dependencies for testing
4. Test Django views using `django.test.Client` and `TestCase`
5. Use `factory_boy` to generate realistic test data without manually crafting dicts
6. Mock external services and database calls using `unittest.mock` and `pytest-mock`
7. Measure test coverage with `pytest-cov` and interpret coverage reports meaningfully

---

## Topics Covered

- pytest fixtures: `scope` (function/class/module/session), `autouse`, fixture factories
- Flask testing: `app.test_client()`, `app.test_request_context()`, test configuration via factory
- FastAPI testing: `TestClient`, `app.dependency_overrides`, async testing with `httpx.AsyncClient`
- Django testing: `TestCase`, `APITestCase` (DRF), `Client`, `RequestFactory`, `override_settings`
- `factory_boy`: `DjangoModelFactory`, `SQLAlchemyModelFactory`, `LazyAttribute`, `SubFactory`, `Sequence`
- Mocking: `unittest.mock.patch`, `MagicMock`, `pytest-mock` `mocker.patch`
- Database isolation: SQLite for unit tests, transactions and rollback for test isolation, `@pytest.fixture` per-test DB
- `pytest-cov`: `--cov`, branch coverage, excluding lines, interpreting the HTML report
- Testing authenticated endpoints: creating test users, setting session cookies, passing Bearer tokens

---

## Cross-Links

- [[django-fastapi-flask/modules/03_flask-advanced]] — Flask testing setup
- [[django-fastapi-flask/modules/05_django-advanced]] — Django test client
- [[django-fastapi-flask/modules/06_fastapi-fundamentals]] — FastAPI dependency overrides
- [[django-fastapi-flask/modules/12_capstone-project]] — comprehensive test suite is a capstone requirement

---

## Summary

- pytest fixtures replace setUp/tearDown with composable, reusable test setup; scope controls how often they run
- FastAPI's `dependency_overrides` is the correct way to replace real dependencies (DB sessions, auth) in tests
- `factory_boy` generates realistic, relationship-aware test data; use it instead of hand-coding test fixtures
- Test isolation requires per-test databases or transactional rollback; shared test databases cause flaky tests
- Coverage measures which lines run during tests — high coverage is necessary but not sufficient; a covered line is not the same as a tested behavior
- Tests should test behavior, not implementation: if renaming a variable causes a test to fail, the test is testing the wrong thing
