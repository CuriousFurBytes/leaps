# Projects: Module 01 — Introduction

> These projects apply the concepts from Module 01. They use only the standard library and Flask or FastAPI with no database or authentication — just routing, request handling, and responses.

---

## Project 1 — Build a Raw WSGI API

**Difficulty:** Beginner
**Estimated Time:** 2–3 hours
**Requires:** Python standard library only (no Flask, no FastAPI)

### Brief

Build a complete REST-style WSGI application without using any framework. The application should manage an in-memory list of to-do items. Implement all four CRUD operations:

- `GET /todos` — returns all to-do items as a JSON array
- `POST /todos` — creates a new to-do item from the JSON request body
- `GET /todos/{id}` — returns a single to-do item by ID
- `DELETE /todos/{id}` — deletes a to-do item by ID

### Constraints

- No `flask`, `django`, `fastapi`, `starlette`, or any other web framework
- Use only `wsgiref`, `json`, and the Python standard library
- Store items in a module-level list (in-memory; does not need to persist)
- Parse the URL yourself to extract the `id` from `/todos/{id}`

### Why This Project

After building this, you will genuinely understand what every web framework is doing for you. The URL parsing, response header construction, status code selection, and body serialization that you write here are things Flask and FastAPI handle invisibly. Having built it yourself, you will read framework source code with much better comprehension.

---

## Project 2 — HTTP Method Inspector

**Difficulty:** Beginner
**Estimated Time:** 1–2 hours
**Requires:** Flask

### Brief

Build a Flask application that helps you understand HTTP methods by reflecting them back at you. Every route should return a JSON response describing the request it received.

- `GET /inspect` — returns `{"method": "GET", "args": {...query params...}, "headers": {...selected headers...}}`
- `POST /inspect` — returns `{"method": "POST", "body": {...parsed JSON body...}, "content_type": "..."}`
- `PUT /inspect`, `PATCH /inspect`, `DELETE /inspect` — similar reflection for each method

The root route `GET /` should return a plain-text or HTML "method tester" that lists all the routes and what each expects.

### Goal

This project is intentionally small — the point is to get comfortable with `request.method`, `request.args`, `request.get_json()`, and `request.headers` in Flask, and to verify your understanding by observing exactly what Flask gives you for each request type.

---

## Project 3 — FastAPI Type Exploration

**Difficulty:** Beginner → Intermediate
**Estimated Time:** 2–4 hours
**Requires:** FastAPI, Pydantic

### Brief

Build a FastAPI application that explores how Pydantic validation interacts with HTTP. Create a series of endpoints that each demonstrate a different validation behavior:

1. `POST /validate/types` — accepts a body with `int_field`, `str_field`, `float_field`, `bool_field` — use it to observe how FastAPI coerces `"42"` to `42` (or rejects it)
2. `POST /validate/constraints` — accepts a body with constrained fields: `username` (min 3 chars, max 20 chars), `score` (0–100), `tags` (list of strings, max 5 items)
3. `POST /validate/nested` — accepts a body with a nested object: `{"user": {"name": "Alice"}, "address": {"city": "NYC", "country": "US"}}`
4. `GET /validate/query` — accepts query parameters with types and constraints: `?page=1&size=10&filter=active`

After building the endpoints, document what happens when you send invalid data to each one — what does the 422 error response look like? What information does it give the client?

Write a brief README (in the project directory) summarizing what you learned about Pydantic's validation model.
