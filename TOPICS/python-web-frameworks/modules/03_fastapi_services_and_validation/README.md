# Module 03: FastAPI Services and Validation

> Build typed FastAPI services with path operations, Pydantic validation, dependency injection, and async-aware design.

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

Build typed FastAPI services with path operations, Pydantic validation, dependency injection, and async-aware design. This module is part of a full path from first web request to production-ready framework decisions.

The goal is not memorizing APIs. The goal is recognizing how requests, validation, persistence, templates, JSON, tests, and deployments connect across Django, FastAPI, and Flask.

## Prerequisites

- Module 02 in this topic.
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

### The Shared HTTP Mental Model

Django, FastAPI, and Flask differ in ergonomics, but all receive an HTTP request, map it to application code, and return an HTTP response. A framework exists to remove repetitive plumbing: parsing paths, matching methods, decoding request bodies, rendering templates, serializing data, and handling errors. Understanding that pipeline makes framework behavior predictable.

```python
# A framework-independent way to imagine a request handler.
def handle_request(method, path):
    if method == "GET" and path == "/health":
        return {"status": 200, "body": "ok"}
    return {"status": 404, "body": "not found"}
```

### Framework Philosophy

Flask emphasizes explicit composition. You add pieces as the application grows, which makes it excellent for learning and for highly customized services. Django emphasizes integrated conventions, which speeds teams building database-backed products. FastAPI emphasizes Python type hints and generated API contracts, which makes service boundaries easier to document and test.

```python
# Flask route shape: minimal and explicit.
from flask import Flask

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}
```

### Interfaces and Boundaries

A framework boundary should not contain all business logic. Keep request parsing, validation, and response formatting near the framework, then call plain Python functions for domain behavior. This pattern keeps tests faster and migrations between frameworks less painful.

```python
# Plain Python domain behavior is easier to test than framework-bound code.
def calculate_total_cents(prices):
    return sum(prices)

assert calculate_total_cents([499, 250]) == 749
```

### Historical Context

Python web frameworks evolved as the web moved from server-rendered pages, to service APIs, to distributed products with typed contracts and continuous deployment. Django solved repetitive publishing and admin needs. Flask made microframework composition approachable. FastAPI made OpenAPI and type-driven validation feel native to Python.

## Key Concepts

- **Request/response cycle:** The path from client input to server output. It includes routing, handler execution, and response construction.
- **Route:** A mapping between an HTTP method plus path and application code.
- **View or path operation:** The function or callable that handles a request in Flask, Django, or FastAPI.
- **Validation:** The process of converting untrusted input into trusted application data, linked to [[shared/glossary#validation]].
- **Separation of concerns:** Keeping HTTP plumbing distinct from domain logic so systems remain testable.

## Examples

### Worked Example: Health Endpoint Shapes

Problem: expose a simple liveness endpoint in each style.

```python
# FastAPI example.
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

```python
# Django view example.
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})
```

The route declaration changes, but the application contract stays the same: a client sends a request and receives a predictable response.

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
