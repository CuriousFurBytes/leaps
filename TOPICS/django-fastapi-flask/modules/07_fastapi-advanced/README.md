# Module 07: FastAPI Advanced — Background Tasks, WebSockets, OAuth2, Middleware, and Lifespan

[← Module 06: FastAPI Fundamentals](../06_fastapi-fundamentals/README.md) | [Topic Home](../../README.md) | [Next → Module 08: Database Patterns](../08_database-patterns/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers FastAPI's background tasks, WebSocket endpoints, OAuth2 with JWT authentication, ASGI middleware, and the lifespan context manager for startup/shutdown events. Full content to be generated on demand.

---

## Overview

This module covers the features that distinguish a FastAPI service from a simple CRUD API. Background tasks allow the HTTP handler to return immediately while non-critical work happens afterwards. WebSockets enable real-time bi-directional communication. OAuth2 with JWT is the modern standard for stateless authentication in APIs. Middleware intercepts every request and response at the ASGI level. And lifespan events allow resources to be initialized once at startup and cleaned up at shutdown.

---

## Prerequisites

- Module 06: FastAPI Fundamentals — Pydantic, Depends, routing
- Module 01: Introduction — ASGI model, async/await
- [[async-python]] — event loops, coroutines, asyncio (recommended)

---

## Objectives

By the end of this module, you will be able to:

1. Use `BackgroundTasks` to perform work after an HTTP response has been sent
2. Implement WebSocket endpoints with connection management and message broadcast
3. Implement OAuth2 password flow with JWT tokens using `python-jose` and `passlib`
4. Write ASGI middleware using `BaseHTTPMiddleware` for request logging, timing, and header injection
5. Use the `@asynccontextmanager` lifespan pattern to manage application-level resources (DB pools, ML models)
6. Explain when to use `async def` vs `def` route handlers and the consequences of each choice

---

## Topics Covered

- `BackgroundTasks`: adding tasks, dependency injection with background tasks, limitations
- WebSockets: `WebSocket`, `connect`, `receive_text/bytes`, `send_text/bytes`, `disconnect`, connection managers
- JWT authentication: `python-jose`, `passlib`, OAuth2PasswordBearer, access and refresh tokens
- ASGI middleware with `BaseHTTPMiddleware`: request timing, CORS, custom headers
- Starlette middleware stack: ordering, middleware dependencies
- Lifespan events: `@asynccontextmanager`, startup initialization (DB pools, model loading), graceful shutdown
- `async def` vs `def`: when FastAPI uses a thread pool for sync functions, why CPU-bound sync work blocks the event loop
- `run_in_executor`: offloading CPU-bound work to a process pool from an async route

---

## Cross-Links

- [[django-fastapi-flask/modules/06_fastapi-fundamentals]] — Depends, routing, Pydantic
- [[django-fastapi-flask/modules/09_authentication-and-security]] — OAuth2, JWT, and security patterns in depth
- [[async-python]] — event loop mechanics, `asyncio.gather`, `asyncio.run_in_executor`
- [[shared/glossary#asgi]] — ASGI scope types including WebSocket

---

## Summary

- `BackgroundTasks` is for fire-and-forget work (emails, webhooks) that should not block the response
- WebSockets in FastAPI use the ASGI WebSocket scope; a connection manager class handles broadcast to multiple clients
- JWT authentication with OAuth2PasswordBearer is the standard stateless auth pattern for FastAPI APIs
- `BaseHTTPMiddleware` wraps the ASGI application; middleware order matters — outer middleware runs first on request and last on response
- The lifespan `@asynccontextmanager` replaces `@app.on_event("startup/shutdown")` as the modern approach
- `async def` route handlers run on the event loop; `def` handlers run in a thread pool — never do CPU-bound work in an `async def` without `run_in_executor`
