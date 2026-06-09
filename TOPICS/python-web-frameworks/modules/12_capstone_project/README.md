# Module 12: Capstone Project

> Design and build a production-style Python web platform that combines framework judgment, persistence, APIs, testing, and deployment readiness.

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

## Overview

Design and build a production-style Python web platform that combines framework judgment, persistence, APIs, testing, and deployment readiness. This module is part of a full path from first web request to production-ready framework decisions.

The goal is not memorizing APIs. The goal is recognizing how requests, validation, persistence, templates, JSON, tests, and deployments connect across Django, FastAPI, and Flask.

## Prerequisites

- Modules 01–03 and the advanced modules in this topic.
- Comfortable editing Python files and running shell commands.
- Basic familiarity with [[python]] syntax.

## Objectives

By the end of this module, you will be able to:

- Explain the core framework concepts in practical language.
- Implement small, runnable Python web examples.
- Compare Django, FastAPI, and Flask tradeoffs for this module's scope.
- Debug common beginner mistakes using the request/response mental model.
- Connect this module to later architecture and deployment work.

## Theory

### Project Brief

Build a multi-tenant learning or operations platform with a public marketing page, authenticated user area, admin workflows, and a typed JSON API. You may choose Django as the primary full-stack framework, Flask for a deliberately small service, FastAPI for the API boundary, or a hybrid architecture that justifies each choice.

### Required Architecture

Your artifact must include HTTP routes, persistent data, validation, authentication or authorization, tests, configuration, and deployment notes. It must also explain why each framework was chosen. The point is professional judgment, not using every tool for its own sake.

### Getting Unstuck

Use staged help instead of copying a finished solution. First, sketch domain nouns and workflows. Second, decide whether the project is page-first, API-first, or admin-first. Third, implement one vertical slice from database model to request handler to test. Fourth, repeat the pattern while extracting shared concerns such as configuration, validation, and error handling.

```python
# A minimal acceptance-check script you can adapt for smoke testing.
import httpx

base_url = "http://localhost:8000"
response = httpx.get(f"{base_url}/health")
assert response.status_code == 200
print(response.json())
```

### Historical Context

Professional web projects are rarely framework tutorials. They are negotiation points among product deadlines, user safety, data integrity, observability, and team maintenance. This capstone mirrors that reality by asking you to make explicit tradeoffs and defend them.

## Key Concepts

- **Request/response cycle:** The path from client input to server output. It includes routing, handler execution, and response construction.
- **Route:** A mapping between an HTTP method plus path and application code.
- **View or path operation:** The function or callable that handles a request in Flask, Django, or FastAPI.
- **Validation:** The process of converting untrusted input into trusted application data, linked to [[shared/glossary#validation]].
- **Separation of concerns:** Keeping HTTP plumbing distinct from domain logic so systems remain testable.

## Examples

### Example Milestone Slice

Problem: prove that the app can create an account-like object through a tested request path.

```python
# This is intentionally a smoke-level example, not the full capstone solution.
def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

Approach: start with one testable route so your project has a feedback loop before features expand.

## Common Pitfalls

### Pitfall 1: Hiding Business Logic Inside Routes

Wrong:

```python
@app.get("/total")
def total():
    prices = [499, 250]
    return {"total": sum(prices)}
```

Correct:

```python
def calculate_total(prices):
    return sum(prices)

@app.get("/total")
def total():
    return {"total": calculate_total([499, 250])}
```

The corrected version can be tested without a running web server.

### Pitfall 2: Treating All Frameworks as Interchangeable

Wrong:

```python
choice = "the newest framework"
```

Correct:

```python
choice = "Django for admin-heavy product, FastAPI for typed API, Flask for small custom app"
```

A framework choice should follow product requirements.

### Pitfall 3: Ignoring HTTP Semantics

Wrong:

```python
@app.get("/delete-user")
def delete_user():
    return {"deleted": True}
```

Correct:

```python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"deleted": user_id}
```

Use methods and paths to communicate intent clearly.

## Cross-Links

- [[python]]
- [[http]]
- [[databases]]
- [[software-testing]]

## Summary

- Python web frameworks share the same request/response foundation.
- Flask favors explicit composition, Django favors integrated conventions, and FastAPI favors typed APIs.
- Plain Python domain logic should stay separate from framework adapters.
- Tests and examples should focus on behavior, not only syntax.
- Professional framework work requires tradeoff analysis, not one-size-fits-all rules.
