# Resources: Module 01 — Introduction

> Resources specifically relevant to this module's topics: HTTP, WSGI, ASGI, and the Python web framework landscape.

---

## Official Documentation

1. **[Flask Documentation — Quickstart](https://flask.palletsprojects.com/en/latest/quickstart/)** — The official Flask quickstart builds a minimal app step by step. Read this alongside the module to reinforce the concepts.

2. **[FastAPI Documentation — Tutorial: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)** — Sebastián Ramírez's own step-by-step introduction. Covers the same ground as this module's FastAPI section with more depth on each feature.

3. **[PEP 3333 — Python Web Server Gateway Interface v1.0.1](https://peps.python.org/pep-3333/)** — The authoritative specification for WSGI. The "Specification Details" section is dense but worth reading once to understand the standard precisely.

4. **[ASGI Specification](https://asgi.readthedocs.io/en/latest/specs/main.html)** — The ASGI specification document. Covers the `scope`, `receive`, and `send` interface for HTTP, WebSocket, and lifespan connections.

---

## HTTP Fundamentals

5. **[MDN Web Docs — HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)** — Mozilla's HTTP reference. The "HTTP Messages", "HTTP Methods", and "HTTP Status Codes" pages are the most relevant to this module. Free and authoritative.

6. **[HTTP/1.1 RFC 9110](https://httpwg.org/specs/rfc9110.html)** — The authoritative HTTP semantics specification. Not required reading, but useful as a reference when you need the exact definition of an HTTP status code or method behavior.

---

## Framework History and Design

7. **[Armin Ronacher — "Flask: One Year In"](https://lucumr.pocoo.org/2011/6/24/yes-we-can-build-tools/)** — A blog post by Flask's creator reflecting on the framework's design goals. Provides historical context for why Flask was built the way it was. [Verify URL before using — search for Armin Ronacher Flask blog post if link changes]

8. **[FastAPI — Alternatives, Inspiration, and Comparisons](https://fastapi.tiangolo.com/alternatives/)** — Sebastián Ramírez's own comparison of FastAPI to Flask, Django, Hug, APIStar, and other frameworks. Explains exactly what problems FastAPI was designed to solve and what it borrowed from each predecessor.

---

## Tools Used in This Module

- **[uvicorn](https://www.uvicorn.org/)** — The ASGI server used with FastAPI. Install with `pip install uvicorn[standard]`.
- **[gunicorn](https://gunicorn.org/)** — The WSGI server used with Flask and Django in production. Install with `pip install gunicorn`.
- **[httpie](https://httpie.io/docs/cli)** — A human-friendly CLI for testing HTTP endpoints. `pip install httpie`. Use `http GET localhost:5000/` instead of `curl`.
