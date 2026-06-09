# Django, FastAPI and Flask

> A zero-to-expert learning path for building, testing, deploying, and choosing Python web applications with Django, FastAPI, and Flask.

## Table of Contents

1. [Why Learn Django, FastAPI and Flask?](#why-learn-django-fastapi-and-flask)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn Django, FastAPI and Flask?

Python web development spans three complementary philosophies. Flask is minimal and explicit, making it ideal for understanding the primitives of routing, views, templates, and extensions. Django is batteries-included, optimized for teams that need authentication, ORM models, admin workflows, forms, and security defaults. FastAPI is type-driven and API-first, designed around modern Python annotations, OpenAPI, Pydantic validation, and asynchronous concurrency.

Learning all three prevents framework tribalism. You will learn to choose a tool based on product shape, team maturity, operational constraints, and long-term maintainability rather than popularity alone. A practitioner who understands the common HTTP foundation beneath these frameworks can debug more effectively, migrate systems more safely, and design cleaner boundaries.

Historically, Flask grew from the Werkzeug and Jinja ecosystem, Django emerged from newsroom publishing needs, and FastAPI built on Starlette and Pydantic to make typed API development ergonomic. Together they provide a practical map of Python web architecture from small services to full-featured platforms.

## Prerequisites

- Comfortable Python syntax: functions, classes, imports, exceptions, virtual environments, and package installation.
- Basic command-line usage and file editing.
- Helpful but not required: [[python]], [[databases]], [[web-development]], and [[http]].

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Web Framework Foundations](modules/01_web_framework_foundations/README.md) | Beginner | [ ] |
| 02 | [Flask Routing and Views](modules/02_flask_routing_and_views/README.md) | Beginner | [ ] |
| 03 | [FastAPI Services and Validation](modules/03_fastapi_services_and_validation/README.md) | Intermediate | [ ] |
| 04 | Django Models, Views, Templates, and Admin | Intermediate | [ ] |
| 05 | Persistence, ORMs, and Migrations | Intermediate | [ ] |
| 06 | Forms, Validation, Serialization, and Security | Advanced | [ ] |
| 07 | Authentication, Authorization, and Session Design | Advanced | [ ] |
| 08 | Testing, Debugging, and Observability | Advanced | [ ] |
| 09 | Async, Background Work, and Performance | Advanced | [ ] |
| 10 | Deployment, Configuration, and Operations | Expert | [ ] |
| 11 | Architecture, Tradeoffs, and Framework Selection | Expert | [ ] |
| 12 | [Capstone Project](modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links

- [[python]] for language fundamentals and packaging.
- [[databases]] for relational modeling, transactions, and migrations.
- [[http]] for methods, headers, cookies, caching, and status codes.
- [[software-testing]] for unit, integration, and end-to-end test strategy.
- [[security]] for threat modeling and secure defaults.

## Quick Reference

| Task | Flask | FastAPI | Django |
|---|---|---|---|
| Define an endpoint | `@app.route("/path")` | `@app.get("/path")` | `path("path/", view)` |
| Request data | `request.args`, `request.form`, `request.json` | Function parameters and Pydantic models | `request.GET`, `request.POST`, forms |
| Templates | Jinja | Jinja or separate frontend | Django templates |
| Database style | Extension-driven, often SQLAlchemy | Explicit layer, often SQLAlchemy or SQLModel | Built-in ORM |
| Best fit | Small apps, services, custom architecture | Typed APIs and async-friendly services | Full product platforms |

```bash
# Typical local setup pattern for any framework in this topic.
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```
