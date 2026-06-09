# Exercises: Module 01 — Introduction

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Submit your answers by editing this file or committing a solutions file alongside it.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Identify the components of an HTTP request and response

Given the following HTTP exchange, label each part:

```text
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer eyJhbGci...

{"name": "Alice", "email": "alice@example.com"}

---

HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/users/99

{"id": 99, "name": "Alice", "email": "alice@example.com"}
```

Questions:
1. What is the HTTP method?
2. What is the URL path?
3. List two request headers and explain what each tells the server.
4. What does the `201` status code mean?
5. What does the `Location` response header typically indicate?

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Match HTTP methods to CRUD operations

For each operation below, write the correct HTTP method and a plausible URL:

1. Retrieve a list of blog posts
2. Create a new blog post
3. Replace an entire blog post (full update)
4. Update only the title of a blog post (partial update)
5. Delete a blog post

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Recall the key differences between WSGI and ASGI

Answer these questions without looking at the module:

1. What does WSGI stand for? What PEP defines it?
2. What does ASGI stand for?
3. Name one WSGI server and one ASGI server.
4. Name one Python framework that is WSGI-only and one that is ASGI.
5. What is the function signature of a minimal WSGI application?

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Write and run a minimal WSGI application

Write a WSGI application (no Flask, no external libraries except the standard library) that:
- Returns `{"status": "ok"}` with status 200 for `GET /health`
- Returns `{"message": "Hello, <name>!"}` with status 200 for `GET /hello/<name>` (e.g., `/hello/Alice` → `{"message": "Hello, Alice!"}`)
- Returns `{"error": "not found"}` with status 404 for any other path

```python
# Starter scaffold
def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    # Your implementation here
    pass
```

Test it by running with `python -m wsgiref.simple_server` or gunicorn.

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Extend the Flask hello-world with error handling

Take the Flask application from the module's Theory section and add:

1. A `GET /status` endpoint that returns `{"status": "running", "version": "1.0"}` with status 200
2. A `GET /divide/<float:a>/<float:b>` endpoint that divides `a` by `b` and returns the result
3. Proper error handling: return `{"error": "cannot divide by zero"}` with status 400 if `b == 0`

Run the app and verify each endpoint manually with curl or a browser.

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Explore FastAPI's automatic documentation

Take the FastAPI application from the module's Theory section:

1. Run it with `uvicorn main:app --reload`
2. Visit `http://localhost:8000/docs` and explore the interactive UI
3. Use the interactive UI to:
   - Make a GET request to `/`
   - Make a POST request to `/echo` with `{"content": "hello", "repeat": 3}`
4. Now add a `GET /items/{item_id}` endpoint that accepts an optional query parameter `category: str = None` and returns `{"item_id": item_id, "category": category}`
5. Refresh the `/docs` page. What changed?

Write a short description (3–5 sentences) of what the auto-generated documentation shows and how it differs from documentation you would write by hand.

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Implement a raw ASGI application

Write a minimal ASGI application (no FastAPI, no Starlette) that:

1. Handles `GET /ping` and returns `{"pong": true}` with status 200
2. Handles `POST /reverse` — reads the JSON body `{"text": "hello"}` and returns `{"result": "olleh"}` with status 200
3. Returns `{"error": "method not allowed"}` with status 405 for wrong methods on known paths
4. Returns `{"error": "not found"}` with status 404 for unknown paths

```python
# Starter scaffold — fill in the application function
import json

async def application(scope, receive, send):
    """
    scope: dict with keys 'type', 'method', 'path', etc.
    receive: async callable to read request body
    send: async callable to send response
    """
    if scope["type"] == "http":
        # Your implementation here
        pass

# Run with: uvicorn exercise7:application --reload
```

This exercise forces you to understand the raw ASGI interface before relying on the framework abstractions.

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Compare Flask and FastAPI validation behavior

Write the same endpoint in both Flask and FastAPI:

**Specification:** `POST /calculate` accepts `{"operation": "add|subtract|multiply", "a": number, "b": number}` and returns `{"result": number}`.

Requirements:
- `operation` must be one of "add", "subtract", or "multiply" — return 400/422 for invalid values
- `a` and `b` must be numbers — return 400/422 if they are not
- Both fields are required

Flask version: write your own validation logic.
FastAPI version: use a Pydantic model with field validators.

After writing both, write 5 sentences comparing:
- The amount of code required for validation
- The quality of error messages returned to the client
- The ease of adding a new validation rule

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Build a framework-agnostic middleware layer

Design and implement a Python class `RequestLogger` that works as middleware for **both** WSGI and ASGI applications. It should:

1. Log each request: method, path, and timestamp (to stdout in JSON format)
2. Log each response: status code and response time in milliseconds
3. Work correctly when wrapping a WSGI app (synchronous `__call__`)
4. Work correctly when wrapping an ASGI app (async `__call__`)

```python
# Target usage:

# WSGI usage (Flask)
from flask import Flask
flask_app = Flask(__name__)
wsgi_app = RequestLogger(flask_app, mode="wsgi")

# ASGI usage (FastAPI)
from fastapi import FastAPI
fastapi_app = FastAPI()
asgi_app = RequestLogger(fastapi_app, mode="asgi")
```

Hint: WSGI middleware wraps `application(environ, start_response)`. ASGI middleware wraps `application(scope, receive, send)`. The two modes require different implementations internally.

Document your design choices in a comment block at the top of the file. What trade-offs did you make?
