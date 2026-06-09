# Django, FastAPI and Flask — Python Web Frameworks

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> A comprehensive journey through Python's three dominant web frameworks — from building a first route in Flask to deploying a production-grade FastAPI service with authentication, tests, and CI/CD.

> [!NOTE]
> **Topic Overview**
> This topic covers Flask, Django, and FastAPI — the three frameworks that define modern Python web development. You will learn each framework from its philosophical foundations through to production deployment patterns. By the end you will be able to choose the right tool for any project, build secure and tested APIs, and reason confidently about WSGI vs ASGI, synchronous vs asynchronous I/O, and the trade-offs between a microframework and a batteries-included alternative.
>
> This topic is organized into 12 progressive modules. Work through them in order. Modules 01–03 cover Flask, 04–05 cover Django, 06–07 cover FastAPI, and 08–12 cover cross-cutting production concerns.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

Python's web framework ecosystem offers three distinct approaches to building HTTP services, each with a distinct philosophy and a different set of trade-offs.

**Flask** (2010) is a microframework. It provides routing and request handling, and deliberately stops there. You assemble the stack yourself — choose your database layer, your templating engine, your authentication library. This minimalism makes Flask ideal for small services, APIs, and learning, but it means discipline and structure must come from the developer rather than the framework.

**Django** (2005) is the opposite philosophy: batteries included. It ships with an ORM, migrations, an admin interface, form handling, authentication, a templating engine, and security middleware. Django's convention-over-configuration approach means you spend less time making architectural decisions and more time solving domain problems. The cost is a steeper learning curve and a framework that exerts strong opinions about your project structure.

**FastAPI** (2019) represents a third way: a modern, standards-first async framework built on Python's type annotation system. FastAPI uses Pydantic for data validation and generates OpenAPI documentation automatically from your function signatures. It is built on Starlette and runs on ASGI, making it naturally async and among the fastest Python frameworks available. It is the youngest of the three and has achieved remarkable adoption in data science, machine learning infrastructure, and high-throughput API work.

### Why It Matters

Web frameworks are the tools that turn Python into a server. Understanding at least one framework is a baseline requirement for most Python developer roles. Understanding all three gives you the judgment to pick the right tool and to read and contribute to any Python web codebase — a significant practical advantage.

Proficiency in Python web frameworks is expected in roles such as **backend engineer** and **full-stack Python developer**, and is increasingly required in **data engineering** and **ML engineering** roles where serving models over HTTP is routine work.

### Key Features of This Topic

- **Framework comparison** — Deep understanding of when to choose Flask, Django, or FastAPI and why
- **Full-stack coverage** — Routes, templates, databases, authentication, testing, and deployment
- **Production patterns** — Gunicorn, Uvicorn, Docker, environment configuration, health checks
- **Modern Python** — Type annotations, async/await, Pydantic, and ASGI throughout

---

## Historical Context

Python web development has evolved through several distinct eras, each responding to the limitations of its predecessor.

**1993–2002: CGI and the beginning.** The earliest Python web applications used CGI (Common Gateway Interface), spawning a new Python process per request. Performance was poor and the model was cumbersome, but it proved the concept.

**2003–2004: mod_python and Zope.** Frameworks like Zope offered structure but were complex. mod_python embedded Python in Apache, improving performance but coupling frameworks to a specific web server.

**2005: Django.** Adrian Holovaty and Simon Willison, working at a Kansas newspaper, extracted their internal framework and open-sourced it as Django. It introduced the MTV pattern (Model–Template–View), an ORM, automatic admin generation, and URL routing as first-class citizens.

**2007: WSGI standardized.** The Python community standardized the interface between web servers and Python applications with WSGI (Web Server Gateway Interface, PEP 333). This decoupled frameworks from servers, enabling Gunicorn, uWSGI, and other production servers to work with any WSGI-compliant application.

**2010: Flask.** Armin Ronacher released Flask as an April Fools' joke that turned serious. Built on Werkzeug (a WSGI toolkit) and Jinja2, Flask proved that a microframework could be production-worthy. Its simplicity and extensibility made it wildly popular in the following decade.

**2015–2018: ASGI emerges.** As Python's async ecosystem matured with `asyncio`, the community recognized that WSGI's synchronous model was a bottleneck. ASGI was proposed as the async successor, and Starlette (by Tom Christie) became its first major production-grade implementation.

**2019: FastAPI.** Sebastián Ramírez released FastAPI, built on Starlette and Pydantic. It made Python type annotations first-class citizens of API design, generated documentation automatically, and ran asynchronously. It found rapid adoption in data science and ML infrastructure.

### Timeline

| Year | Event |
|------|-------|
| 2005 | Django released by Holovaty and Willison (Lawrence Journal-World) |
| 2007 | PEP 333 formalizes WSGI; Werkzeug and Jinja2 released |
| 2010 | Flask 0.1 released by Armin Ronacher |
| 2013 | Django 1.5; class-based views and Python 3 support |
| 2015 | ASGI proposed as async successor to WSGI |
| 2017 | Django REST Framework achieves wide industry adoption |
| 2019 | FastAPI released by Sebastián Ramírez |
| 2021 | Django 4.0 drops Python 2; async views added natively |
| 2023 | FastAPI among the most-starred Python repos on GitHub |
| Today | All three frameworks actively maintained and widely deployed |

---

## Real-World Applications

Python web frameworks power some of the world's most demanding services:

- **Instagram (Django)** — Built on Django from its 2010 launch; has scaled to over a billion users with extensive internal customization
- **Pinterest (Django)** — Uses Django for its core application layer with custom sharding and caching strategies
- **Netflix (Flask)** — Uses Flask extensively in internal tooling and microservices, favoring its minimal footprint for composable services
- **Reddit (Flask)** — The Reddit API and several internal services use Flask-family tooling
- **Microsoft Azure ML (FastAPI)** — Several Azure Machine Learning teams use FastAPI for ML inference endpoints
- **Uber (FastAPI)** — Internal high-throughput APIs where async performance and automatic documentation are valued

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the difference between WSGI and ASGI and describe the request-response lifecycle in each
2. Build a complete Flask application using blueprints, the application factory pattern, and Flask-SQLAlchemy
3. Build a complete Django application with models, migrations, class-based views, and the Django admin
4. Build a FastAPI service with Pydantic validation, dependency injection, JWT authentication, and WebSocket support
5. Design and query relational databases from all three frameworks, avoiding N+1 query problems and using connection pooling correctly
6. Implement session-based and JWT-based authentication, CSRF protection, and rate limiting
7. Write comprehensive test suites using pytest, TestClient, and factory_boy for all three frameworks
8. Deploy any of the three frameworks to production using Docker, Gunicorn or Uvicorn, and nginx
9. Choose the appropriate framework for a given project based on requirements, team size, and performance needs
10. Build and ship a complete, production-ready REST API with documentation, authentication, tests, and CI/CD

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Intermediate → Expert |
| **Estimated Total Hours** | 80–120 hours |
| **Prerequisites** | Python functions and classes, basic HTTP concepts, basic terminal usage |
| **Recommended Pace** | 6–8 hours/week |
| **Topic Type** | Computational (Python code required throughout) |
| **Suitable For** | Python developers moving into web development; developers adding a second or third framework |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- **Python functions and classes** — comfortable writing functions, using decorators, and defining classes with methods and inheritance
- **Basic HTTP concepts** — understand requests and responses, status codes (200, 404, 500), and HTTP methods (GET, POST, PUT, DELETE, PATCH)
- **Terminal usage** — able to run Python scripts, install packages with pip, create and activate virtual environments
- **Basic SQL** — know how to SELECT, INSERT, UPDATE, and DELETE rows; understand tables, columns, primary keys, and foreign keys

> [!TIP]
> Not sure if you're ready? Read Module 01's Overview section. If the HTTP and WSGI discussion feels completely foreign, spend an hour reviewing HTTP fundamentals first. If you can follow along but things feel shaky, press on — the concepts solidify quickly once you have running code.

---

## Learning Modules

| # | Module | Topics Covered | Difficulty | Status |
|---|--------|---------------|------------|--------|
| 01 | [Introduction](./modules/01_introduction/) | HTTP, WSGI vs ASGI, framework comparison, first apps | Beginner | - [ ] |
| 02 | [Flask Fundamentals](./modules/02_flask-fundamentals/) | Routes, Jinja2 templates, request/response, Blueprints, app factory | Beginner | - [ ] |
| 03 | [Flask Advanced](./modules/03_flask-advanced/) | Flask-SQLAlchemy, Flask-Login, Flask-WTF, pytest, gunicorn | Intermediate | - [ ] |
| 04 | [Django Fundamentals](./modules/04_django-fundamentals/) | MTV pattern, ORM, migrations, admin, URL routing, CBV vs FBV | Intermediate | - [ ] |
| 05 | [Django Advanced](./modules/05_django-advanced/) | Django REST Framework, signals, Celery, caching, security middleware | Intermediate | - [ ] |
| 06 | [FastAPI Fundamentals](./modules/06_fastapi-fundamentals/) | Path/query params, Pydantic validation, dependency injection, OpenAPI docs | Intermediate | - [ ] |
| 07 | [FastAPI Advanced](./modules/07_fastapi-advanced/) | Background tasks, WebSockets, OAuth2/JWT, middleware, lifespan events | Advanced | - [ ] |
| 08 | [Database Patterns](./modules/08_database-patterns/) | SQLAlchemy Core vs ORM, connection pooling, N+1 queries, bulk ops, migrations | Advanced | - [ ] |
| 09 | [Authentication and Security](./modules/09_authentication-and-security/) | Session auth, JWT, OAuth2 flows, CSRF protection, rate limiting | Advanced | - [ ] |
| 10 | [Testing Web Applications](./modules/10_testing-web-applications/) | pytest fixtures, TestClient, mocking DB, factory_boy, coverage reports | Advanced | - [ ] |
| 11 | [Deployment and Production](./modules/11_deployment-and-production/) | Docker, gunicorn/uvicorn, nginx, env config, health checks | Expert | - [ ] |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Build a production REST API with auth, tests, Docker, CI/CD, docs | Expert | - [ ] |

**Status key:** ` ` Not started · `~` In progress · `x` Complete

---

## Progress

### Overall Progress

```text
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```text
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 20 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 90 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **654** | **0%** |

---

## Milestones

- [ ] **First Route** — Complete Module 01 (Introduction)
- [ ] **Flask Developer** — Complete Modules 01–03 with ≥70% on each test
- [ ] **Django Developer** — Complete Modules 04–05 with ≥70% on each test
- [ ] **FastAPI Developer** — Complete Modules 06–07 with ≥70% on each test
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Production Ready** — Complete Modules 08–11
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Framework Master** — Average test score ≥90% across all modules
- [ ] **Capstone Shipped** — Complete the capstone project with all acceptance criteria met

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% · B ≥ 80% · C ≥ 70% · D ≥ 60% · F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for Python web frameworks:

- [[async-python]] — async/await, event loops, and asyncio; essential background for FastAPI and Django async views
- [[postgresql]] — the most common production database for all three frameworks; covers indexes, transactions, and query optimization
- [[graphql-rest]] — REST API design principles and GraphQL; complements the API-building modules in this topic

<!-- TODO: cross-link to [[docker]] once that topic is created -->
<!-- TODO: cross-link to [[testing-python]] once that topic is created -->

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Topic Created

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed prerequisites

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "django-fastapi-flask"
topic_name: "Django, FastAPI and Flask — Python Web Frameworks"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 654
completion_percentage: 0
difficulty: "Intermediate → Expert"
estimated_hours: 100
prerequisites:
  - "python-basics"
  - "http-concepts"
related_topics:
  - "async-python"
  - "postgresql"
  - "graphql-rest"
tags:
  - "python"
  - "web"
  - "backend"
  - "flask"
  - "django"
  - "fastapi"
creator: "various"
year_created: "2005"
```
