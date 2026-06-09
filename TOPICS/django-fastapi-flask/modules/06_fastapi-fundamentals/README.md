# Module 06: FastAPI Fundamentals — Pydantic, Dependency Injection, and OpenAPI

[← Module 05: Django Advanced](../05_django-advanced/README.md) | [Topic Home](../../README.md) | [Next → Module 07: FastAPI Advanced](../07_fastapi-advanced/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-5--7h-orange)

> **Stub module.** This module covers FastAPI path and query parameters, Pydantic models for request/response validation, dependency injection with `Depends()`, response models, and automatic OpenAPI documentation. Full content to be generated on demand.

---

## Overview

FastAPI's design philosophy is "fast to code, fast to run." It achieves "fast to code" through Python type annotations: your route functions' type hints are the API contract, the validation logic, the documentation, and the test fixtures all at once. FastAPI reads these annotations at startup and generates Pydantic validators and OpenAPI schemas from them automatically.

This module teaches you to think in FastAPI's model: type annotations as the source of truth, Pydantic as the data layer, and `Depends()` as the dependency graph.

---

## Prerequisites

- Module 01: Introduction — ASGI, FastAPI hello world
- Module 03 or 05 — some exposure to API development patterns
- Python type annotations — `str`, `int`, `Optional[str]`, `List[str]`, `Dict[str, Any]`

---

## Objectives

By the end of this module, you will be able to:

1. Define path parameters, query parameters, and request headers in FastAPI route functions using type annotations
2. Create Pydantic models for request body validation with field constraints, optional fields, and nested models
3. Define response models and use `response_model=` to control serialization output
4. Use `Depends()` to declare and inject dependencies (database sessions, authenticated users, shared configuration)
5. Use FastAPI's `status` module and `HTTPException` to return correct status codes and error responses
6. Navigate and use the auto-generated OpenAPI documentation at `/docs` and `/redoc`
7. Organize a FastAPI application using `APIRouter` (FastAPI's equivalent of Flask Blueprints)

---

## Topics Covered

- Path parameters: `{item_id}`, type coercion, `Path()` with validation constraints
- Query parameters: function parameters with defaults, `Query()` with constraints, optional parameters
- Request bodies: `BaseModel`, nested models, `Body()` for embedding or mixing params
- Response models: `response_model=`, `response_model_exclude_unset=True`, `Response` class
- Pydantic v2: `field_validator`, `model_validator`, `Annotated` with `Field()`
- Dependency injection: `Depends()`, nested dependencies, dependency overrides for testing
- `HTTPException`: raising 400/404/409 errors with `detail` strings or dicts
- `APIRouter`: creating, including, URL prefixes, tags
- OpenAPI metadata: `title`, `description`, `version`, `tags` with descriptions

---

## Cross-Links

- [[django-fastapi-flask/modules/01_introduction]] — ASGI, first FastAPI endpoint
- [[django-fastapi-flask/modules/07_fastapi-advanced]] — WebSockets, OAuth2, background tasks
- [[django-fastapi-flask/modules/08_database-patterns]] — injecting database sessions via `Depends()`
- [[shared/glossary#pydantic-model]] — Pydantic model glossary entry
- [[shared/glossary#dependency-injection]] — dependency injection glossary entry
- [[shared/glossary#schema]] — schema glossary entry

---

## Summary

- FastAPI uses Python type annotations as the primary source of truth for validation, docs, and serialization
- Pydantic `BaseModel` is the data contract layer; `Field()` and validators enforce constraints
- `response_model=` controls what is serialized to the client, decoupling input models from output shapes
- `Depends()` builds a dependency graph that FastAPI resolves automatically per request
- `APIRouter` organizes routes the same way Flask Blueprints do; include routers on the app with a prefix and tags
- The `/docs` page is not a nice-to-have — it is a live, executable API specification generated from your code
