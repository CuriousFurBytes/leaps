# Glossary: Django, FastAPI and Flask — Python Web Frameworks

> Definitions for the key terms used throughout this topic. Entries are listed alphabetically. For the shared repository glossary, see [[shared/glossary]].

---

## ASGI

**ASGI (Asynchronous Server Gateway Interface)** is the successor to WSGI designed to support asynchronous Python web applications. An ASGI application is a callable that receives three arguments: `scope` (a dict describing the connection), `receive` (a coroutine to read incoming messages), and `send` (a coroutine to send outgoing messages). ASGI supports HTTP/1, HTTP/2, and WebSockets in a single interface. FastAPI and Django (since 3.1) are ASGI-compatible. See: [[django-fastapi-flask/modules/01_introduction#asgi-the-async-evolution]].

---

## App Factory

The **application factory pattern** is a design pattern for Flask (and other frameworks) where the Flask app object is created inside a function rather than at module level. This allows the app to be created multiple times with different configurations — essential for testing. The factory function typically accepts a configuration object or string, creates the `Flask` instance, initializes extensions, and registers blueprints. See: [[django-fastapi-flask/modules/02_flask-fundamentals]].

---

## Blueprint

A **Blueprint** in Flask is a way to organize a set of related routes, templates, and static files into a reusable component. Blueprints allow large Flask applications to be split into modules, each with its own routes and URL prefix. A blueprint is registered on the app with `app.register_blueprint(bp, url_prefix="/api")`. Blueprints are Flask-specific; Django uses apps and FastAPI uses APIRouter for similar purposes.

---

## CSRF

**CSRF (Cross-Site Request Forgery)** is a class of web attack in which a malicious website tricks a user's browser into making an authenticated request to another site. Protection involves including an unpredictable token in every state-changing request (POST, PUT, DELETE) that the server validates. Django includes CSRF protection by default via the `CsrfViewMiddleware`. Flask-WTF provides CSRF protection for Flask applications. FastAPI's stateless JWT approach largely sidesteps traditional CSRF, though double-submit cookie patterns are available.

---

## Dependency Injection

**Dependency injection** is a design pattern where a component's dependencies are provided to it externally rather than the component constructing them itself. In FastAPI, `Depends()` is used to declare dependencies: when a route function lists a dependency, FastAPI resolves it automatically and passes the result into the function. This enables sharing database sessions, authenticated users, and configuration across routes without global state.

---

## Migration

A **migration** is a version-controlled script that describes a change to a database schema (adding a table, adding a column, creating an index, etc.) and how to reverse that change. Django's migration system (`django.db.migrations`) generates these scripts automatically from changes to model classes. Flask-Migrate (using Alembic) and FastAPI projects using SQLAlchemy typically use Alembic for migrations. Migrations allow schema changes to be tracked in git and applied consistently across development, staging, and production.

---

## Middleware

**Middleware** is software that sits between the web server and the application, processing every request before it reaches the application and every response before it leaves. Middleware is used for authentication checks, logging, CORS headers, rate limiting, request ID injection, and more. In WSGI frameworks, middleware wraps the `application` callable. In ASGI frameworks, middleware wraps the ASGI app. Django's `MIDDLEWARE` setting is an ordered list of middleware classes.

---

## ORM

An **ORM (Object-Relational Mapper)** translates between Python objects and database tables. You define Python classes (models), and the ORM generates SQL to create, read, update, and delete rows. Django's ORM is built-in and uses `QuerySet` objects with a chaining API. SQLAlchemy is the most widely used Python ORM outside Django and supports both a declarative model API and a lower-level Core SQL expression language. FastAPI projects typically use SQLAlchemy or Tortoise-ORM.

---

## Pydantic Model

A **Pydantic model** is a Python class that inherits from `pydantic.BaseModel` and declares fields using type annotations. Pydantic validates and coerces incoming data against these annotations at runtime. In FastAPI, Pydantic models serve as request bodies, response shapes, and query parameter validators. Pydantic v2 (released 2023) rewrote the validation engine in Rust for significantly improved performance.

---

## Request/Response Cycle

The **request/response cycle** is the fundamental pattern of HTTP: a client (browser, mobile app, another service) sends an HTTP **request** to a server, and the server processes it and returns an HTTP **response**. The request contains a method (GET, POST, etc.), a URL, headers, and optionally a body. The response contains a status code (200, 404, etc.), headers, and optionally a body. Every web framework's core job is to route incoming requests to the right handler function and serialize the handler's return value into a response.

---

## REST Endpoint

A **REST endpoint** is a URL that a client can call to interact with a resource on the server following REST (Representational State Transfer) conventions. REST maps HTTP methods to CRUD operations: GET (read), POST (create), PUT/PATCH (update), DELETE (delete). A well-designed REST API uses nouns in URLs (`/users/42`) not verbs (`/getUser?id=42`), returns appropriate status codes, and is stateless. See: [[graphql-rest]].

---

## Schema

In the context of web frameworks, a **schema** has two related meanings: (1) the definition of the shape of data that an endpoint expects or returns, typically expressed as a Pydantic model in FastAPI or a DRF serializer in Django; (2) the structure of a database (its tables, columns, and relationships), as described by migrations. FastAPI automatically generates an OpenAPI (formerly Swagger) schema from Pydantic models, which powers the interactive `/docs` endpoint.

---

## Serializer

A **serializer** converts complex Python objects (ORM model instances, querysets) into simple Python dicts or JSON, and validates and deserializes incoming JSON back into Python objects or database records. Django REST Framework's `Serializer` and `ModelSerializer` classes are the primary serialization layer for DRF-based APIs. Flask and FastAPI use Pydantic models or marshmallow schemas for the same purpose.

---

## Session

A **session** is a server-side mechanism for maintaining state between HTTP requests (which are stateless by design). When a user logs in, the server creates a session record (typically in a database or in-memory cache) keyed by a session ID stored in a browser cookie. On each subsequent request, the cookie is sent and the server looks up the session to identify the user. Django's session framework is built-in. Flask uses cryptographically signed cookies for client-side sessions by default. FastAPI typically uses stateless JWT tokens rather than server-side sessions.

---

## WSGI

**WSGI (Web Server Gateway Interface)**, defined in PEP 333 (2003) and updated in PEP 3333, is the standard Python interface between web servers and Python web applications. A WSGI application is a callable that accepts two arguments: `environ` (a dict containing the HTTP request data) and `start_response` (a callback to begin the response). WSGI is synchronous — one request at a time per thread. Flask and Django (before 3.1's async support) are WSGI applications. Production WSGI servers include Gunicorn and uWSGI. See: [[django-fastapi-flask/modules/01_introduction#wsgi-the-python-web-standard]].
