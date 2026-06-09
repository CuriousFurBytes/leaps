# Roadmap: Django, FastAPI and Flask — Python Web Frameworks

> This roadmap shows the learning phases and how they build on each other. Follow the phases in order unless you already have solid experience in an earlier phase.

---

## Learning Phases

```mermaid
flowchart TD
    subgraph Phase1["Phase 1 — Flask (Beginner)"]
        M01["01: Introduction\nHTTP, WSGI vs ASGI\nFramework comparison"]
        M02["02: Flask Fundamentals\nRoutes, Jinja2, Blueprints\nApp factory pattern"]
        M03["03: Flask Advanced\nFlask-SQLAlchemy, Flask-Login\nTesting, Gunicorn"]
        M01 --> M02 --> M03
    end

    subgraph Phase2["Phase 2 — Django (Intermediate)"]
        M04["04: Django Fundamentals\nMTV pattern, ORM\nMigrations, Admin"]
        M05["05: Django Advanced\nDRF, Signals\nCelery, Caching"]
        M03 --> M04 --> M05
    end

    subgraph Phase3["Phase 3 — FastAPI (Intermediate → Advanced)"]
        M06["06: FastAPI Fundamentals\nPydantic, Dependency injection\nOpenAPI docs"]
        M07["07: FastAPI Advanced\nWebSockets, OAuth2/JWT\nMiddleware, Lifespan"]
        M05 --> M06 --> M07
    end

    subgraph Phase4["Phase 4 — Expert Production Skills"]
        M08["08: Database Patterns\nSQLAlchemy, N+1, Pooling\nBulk ops, Migrations"]
        M09["09: Auth & Security\nJWT, OAuth2, CSRF\nRate limiting"]
        M10["10: Testing\npytest, TestClient\nfactory_boy, Coverage"]
        M11["11: Deployment\nDocker, nginx\nGunicorn/Uvicorn"]
        M12["12: Capstone Project\nBuild a production API\nEnd-to-end"]
        M07 --> M08
        M08 --> M09
        M09 --> M10
        M10 --> M11
        M11 --> M12
    end
```

_The four phases build linearly. Complete Phase 1 (Flask) before Phase 2 (Django) — Flask's explicit simplicity makes Django's conventions easier to understand._

---

## Phase Descriptions

### Phase 1 — Flask: Learning by Doing

Flask's philosophy is "start small and add what you need." This phase uses that philosophy intentionally: you build a real application piece by piece, adding each component manually. This gives you a hands-on understanding of what web frameworks actually do before you encounter the magic of Django or the type machinery of FastAPI.

**You should be able to after Phase 1:** Build and deploy a Flask web app with database access, user authentication, and templates.

### Phase 2 — Django: Convention Over Configuration

Django's "batteries included" philosophy means there is a right way to do almost everything. This phase teaches you Django's conventions deeply — how the ORM maps Python classes to database tables, how migrations track schema changes, how the admin interface works, and how Django REST Framework turns Django models into a JSON API.

**You should be able to after Phase 2:** Build and deploy a Django application with a REST API, admin interface, and robust data model.

### Phase 3 — FastAPI: Modern Async APIs

FastAPI represents the current state of the art for Python API development. This phase teaches you to use Python's type annotation system as your API contract, understand dependency injection as a design pattern, handle async I/O correctly, and build WebSocket endpoints.

**You should be able to after Phase 3:** Build a fully async FastAPI service with automatic OpenAPI documentation, JWT authentication, and WebSocket support.

### Phase 4 — Expert: Production Cross-Cutting Concerns

The final phase covers the concerns that every production web application shares regardless of framework: database access patterns, security, testing, and deployment. These modules deliberately reference all three frameworks to reinforce that these patterns are universal.

**You should be able to after Phase 4:** Deploy any of the three frameworks to production with Docker, configure nginx as a reverse proxy, write a comprehensive test suite, and make informed security decisions.

---

## Skill Map

The following skills are developed across this topic. Each row shows which modules contribute to it.

| Skill | Modules |
|-------|---------|
| HTTP fundamentals | 01 |
| Flask routing and templates | 02, 03 |
| Database access with SQLAlchemy | 03, 08 |
| Django ORM and migrations | 04, 08 |
| REST API design | 05, 06 |
| Type-driven API design | 06, 07 |
| Authentication (session/JWT/OAuth2) | 03, 05, 07, 09 |
| Testing web applications | 10 |
| Docker and containerization | 11 |
| Production deployment | 11, 12 |
| End-to-end project delivery | 12 |

---

## Prerequisites Map

```mermaid
flowchart LR
    PY["Python basics\n(functions, classes, decorators)"]
    HTTP["HTTP fundamentals\n(requests, responses, methods)"]
    SQL["Basic SQL\n(SELECT, INSERT, JOIN)"]
    ASYNC["[[async-python]]"]

    PY --> M01
    HTTP --> M01
    SQL --> M03

    M01 --> M02 --> M03 --> M04 --> M05 --> M06 --> M07
    M07 --> M08 --> M09 --> M10 --> M11 --> M12

    ASYNC -.-> M06
    ASYNC -.-> M07
```

_Dashed arrows indicate recommended background; solid arrows are required prerequisites._
