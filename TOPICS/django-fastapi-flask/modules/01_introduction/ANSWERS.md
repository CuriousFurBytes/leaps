# Answers: Module 01 — Introduction

## Answer Key

### Easy Questions

**Q1:** WSGI stands for **Web Server Gateway Interface**. For Python 3, it is defined in **PEP 3333** (the Python 3 update of the original PEP 333).

**Q2:**
- `GET` → Read / Retrieve
- `POST` → Create
- `PUT` → Update (full replacement)
- `PATCH` → Update (partial)
- `DELETE` → Delete

**Q3:**
- (a) `200 OK`
- (b) `201 Created`
- (c) `400 Bad Request`
- (d) `401 Unauthorized`
- (e) `500 Internal Server Error`

**Q4:**
- **Flask** is a Python microframework that provides routing and request handling with minimal built-in functionality, leaving architectural choices to the developer.
- **Django** is a batteries-included Python web framework that provides an ORM, migrations, admin interface, forms, authentication, and templating out of the box.
- **FastAPI** is a modern Python web framework built on ASGI and Pydantic that uses type annotations for automatic request validation and OpenAPI documentation generation.

**Q5:** The WSGI callable signature is `application(environ, start_response)`.
- `environ` is a dictionary containing all HTTP request data: the request method (`REQUEST_METHOD`), path (`PATH_INFO`), query string (`QUERY_STRING`), headers (as `HTTP_*` keys), and the request body as a file-like object (`wsgi.input`).
- `start_response` is a callable provided by the WSGI server that the application must call with `(status_string, response_headers_list)` to begin the response. It must be called before returning the body.

---

### Medium Questions

**Q6:** WSGI is **synchronous**: each call to the `application` callable blocks until it returns. One worker handles one request at a time. ASGI is **asynchronous**: the `application` coroutine can `await` slow I/O operations, yielding control to the event loop so other requests can make progress concurrently. A concrete advantage: an ASGI application serving 1000 requests that each wait 100ms for a database query can handle all 1000 concurrently with one worker; a WSGI application requires 1000 workers to do the same. ASGI also natively supports **WebSockets** — persistent bidirectional connections — which WSGI cannot represent at all, since WSGI models every interaction as a single request/response pair.

**Q7:**
- (a) **Database support:** Flask has none built in (use SQLAlchemy, Peewee, etc.). Django has a built-in ORM with migrations.
- (b) **Routing:** Flask uses decorators (`@app.route("/path")`). Django uses a `urls.py` file with `path()` or `re_path()` entries.
- (c) **Use case:** Flask is best for small services, APIs, microservices, and learning. Django is best for content sites, admin-heavy applications, and full-featured web apps.
- (d) **API docs:** Flask has no built-in documentation (Flask-RESTX or similar adds it). Django's REST Framework has swagger via third-party packages (drf-spectacular). FastAPI generates interactive OpenAPI docs at `/docs` automatically with no configuration.

**Q8:** The application factory pattern creates the Flask app object inside a function (`create_app(config=None)`) rather than at module level. This matters for testing because each test can call `create_app({"TESTING": True, "DATABASE_URI": "sqlite:///:memory:"})` to get a fresh, isolated app instance with test-specific configuration. Without the factory, all tests would share the same app object and the same database, making test isolation impossible. The factory is also essential for running multiple Flask apps in the same process.

**Q9:** HTTP is stateless because each request is independent — the server does not inherently know that request #2 came from the same client as request #1. Web applications work around this with: **sessions** (server stores a session record keyed by a session ID in a cookie), **cookies** (small pieces of data stored in the browser and sent with every request), and **tokens** (JWT or similar; the client sends a signed token with each request that contains identity claims the server can verify without storing server-side state).

**Q10:** Development servers (Flask's `flask run`, uvicorn's `--reload`) are unsuitable for production because:
1. They are **single-process/single-threaded** and cannot handle concurrent requests — a second request waits while the first is being processed
2. The `--reload` flag continuously watches the filesystem and restarts the process on every code change — expensive and unstable under load
3. They have no **worker process management** — if a worker crashes, nothing restarts it
4. Flask's `debug=True` enables an interactive debugger in the browser that can **execute arbitrary Python code** on the server — a critical security vulnerability

---

### Hard Questions

**Q11:** Three bugs in the Flask application:

```python
# Bug 1: GET /greet tries to read request.json
# GET requests do not have a body; request.json will be None,
# causing a TypeError on None["name"].
# Fix: either change the method to POST, or use request.args.get("name")
@app.route("/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "World")  # Fix: use query parameter
    return {"message": f"Hello, {name}!"}     # Also fix: return JSON, not plain string

# Bug 2: items dict uses int keys but item_id is a string
# URL parameters are strings by default unless typed with <int:item_id>.
# items[item_id] will raise KeyError because "1" != 1.
@app.route("/items/<int:item_id>")          # Fix: add int: type converter
def get_item(item_id):
    items = {1: "apple", 2: "banana"}
    item = items.get(item_id)
    if item is None:
        return {"error": "not found"}, 404  # Fix: handle missing key
    return {"item": item}

# Bug 3: debug=True in production context is a security vulnerability.
# The fix for deployment: use an environment variable, never hardcode True.
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", debug=os.environ.get("DEBUG", "0") == "1")  # Fix
```

**Q12:**

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator
from typing import Annotated
from pydantic import Field

app = FastAPI()

class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    age: Annotated[int, Field(ge=18)]

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: int

@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(body: UserCreate):
    # In a real app, you would save to a database here.
    # The id=1 is a placeholder.
    return UserResponse(id=1, username=body.username, email=body.email, age=body.age)
```

Note: `EmailStr` requires `pip install pydantic[email]` (email-validator package).

**Q13:** Historical progression:
- **CGI** (1990s): The server spawned a **new Python process per request**. This was the critical limitation — process creation is expensive, and there was no shared state between requests.
- **mod_python** (early 2000s): Embedded Python in Apache, so the interpreter was persistent. Key limitation: **tightly coupled to Apache** — applications could not run on other servers without modification.
- **WSGI** (2003–2007, PEP 333/3333): Standardized the interface between servers and applications, decoupling them completely. Key limitation: **synchronous only** — one request per thread, no async I/O, no WebSocket support.
- **ASGI** (2015–present): Introduced an async interface supporting concurrent requests, HTTP/2, and WebSockets. The transition was motivated by Python 3's `asyncio` maturation and the need to support WebSockets and server-sent events at scale.

**Q14:** Both commands run a FastAPI (ASGI) application with 4 worker processes, but:
- **Option A** (`uvicorn --workers 4`) uses uvicorn's built-in multi-process mode. Simpler, but uvicorn's process manager is less mature than gunicorn's — no graceful restarts, less sophisticated signal handling, and fewer configuration options.
- **Option B** (`gunicorn -k UvicornWorker`) uses gunicorn as the process manager with uvicorn workers. Each worker runs a uvicorn ASGI server. Preferred for production: gunicorn has battle-tested process management, graceful restarts (`SIGUSR2`), pre-fork worker management, and configurable worker timeouts.
Use Option A for development or simple deployments. Use Option B for production deployments where operational control matters.

---

### Expert Questions

**Q15:** **Recommendation: FastAPI.**

Justification:
- (a) FastAPI is ASGI and natively supports WebSockets — the streaming requirement is a first-class feature. FastAPI's type annotation system and automatic OpenAPI docs reduce boilerplate for a REST API. The team has 2 years of web experience and should be able to learn FastAPI quickly.
- (b) Deployment: `gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000` behind nginx. Worker count: `(2 × CPU cores) + 1` is a common starting point; tune based on load.
- (c) CPU-bound work (ML inference) is the critical caution: `async def` route handlers that do heavy CPU work **block the event loop** during computation, which negates ASGI's concurrency benefit. The solution is to run the ML inference in a **process pool executor**: `await asyncio.get_event_loop().run_in_executor(None, run_model, inputs)`. This offloads the CPU work to a thread/process pool and returns the event loop immediately.
- (d) WebSocket streaming: FastAPI's `WebSocket` class handles this directly: `@app.websocket("/stream")` with `await websocket.send_text(chunk)` in a loop. For large deployments, add a Redis pub/sub layer to fan results out to multiple worker processes.

**Q16:**

```python
import json
import io
from wsgiref.simple_server import make_server

def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")

    def respond(status, body_dict):
        body = json.dumps(body_dict).encode("utf-8")
        start_response(status, [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ])
        return [body]

    if path == "/":
        if method == "GET":
            return respond("200 OK", {"message": "ok"})
        else:
            return respond("405 Method Not Allowed", {"error": "method not allowed"})

    elif path == "/echo":
        if method == "POST":
            try:
                length = int(environ.get("CONTENT_LENGTH", 0) or 0)
                body_bytes = environ["wsgi.input"].read(length)
                data = json.loads(body_bytes)
                return respond("200 OK", data)
            except (json.JSONDecodeError, ValueError):
                return respond("400 Bad Request", {"error": "invalid json"})
        else:
            return respond("405 Method Not Allowed", {"error": "method not allowed"})

    else:
        return respond("404 Not Found", {"error": "not found"})

if __name__ == "__main__":
    with make_server("", 8000, application) as httpd:
        print("Serving on http://localhost:8000")
        httpd.serve_forever()
```

---

### Bonus

**Bonus 1:** ASGI supports three `scope["type"]` values:

1. **`"http"`** — A standard HTTP/1.1 or HTTP/2 request-response interaction. The most common type. Used for every regular REST API endpoint, web page, form submission, etc. The `receive` coroutine returns the request body; the `send` coroutine is called twice: once with `http.response.start` (headers) and once with `http.response.body`.

2. **`"websocket"`** — A persistent WebSocket connection that remains open for bi-directional messaging. Used for real-time features: chat applications, live dashboards, collaborative editing, game state updates, streaming ML inference results. The `receive` coroutine returns connection events (`websocket.connect`, `websocket.receive`, `websocket.disconnect`) and the `send` coroutine sends messages or acceptance/rejection signals.

3. **`"lifespan"`** — Startup and shutdown lifecycle events for the application itself, not for individual connections. The `receive` coroutine returns `lifespan.startup` and `lifespan.shutdown` events. Used to initialize resources at startup (database connection pools, ML model loading) and clean them up at shutdown. FastAPI exposes this via the `@app.on_event("startup")` decorator or the newer `@asynccontextmanager` lifespan approach.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
