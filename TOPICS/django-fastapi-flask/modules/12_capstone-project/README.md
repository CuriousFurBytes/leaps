# Module 12: Capstone Project — Build a Production-Ready REST API

[← Module 11: Deployment and Production](../11_deployment-and-production/README.md) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-20--40h-orange)

> This is the capstone project for the Python Web Frameworks topic. You will build a complete, production-ready REST API that synthesizes skills from all preceding modules. There is no new theory here — only application, engineering judgment, and the satisfaction of shipping something real.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Framework Choice](#framework-choice)
5. [Acceptance Criteria](#acceptance-criteria)
6. [Milestones](#milestones)
7. [Architecture Guidance](#architecture-guidance)
8. [Getting Unstuck](#getting-unstuck)
9. [Evaluation Rubric](#evaluation-rubric)
10. [Submission](#submission)

---

## Overview

You have learned Flask, Django, and FastAPI. You have built databases, written tests, implemented authentication, and deployed with Docker. Now you will put it all together into a single, coherent, production-quality system.

This module is build-oriented, not lecture-oriented. Read the project brief, plan your architecture, and build it. The "Getting Unstuck" sections provide hints and checkpoints — use them when you are genuinely stuck, not as a recipe to follow blindly. The goal is your own engineering judgment, not a copy-paste solution.

> [!IMPORTANT]
> This capstone does not provide a complete solution. That is intentional. The process of making architectural decisions, hitting unexpected problems, and solving them is the learning. Use the hints only when you are well and truly stuck.

---

## Prerequisites

All preceding modules (01–11). Specifically:
- Module 06 or 07 — FastAPI (recommended framework for the capstone)
- Module 08 — Database patterns (SQLAlchemy, migrations)
- Module 09 — Authentication (JWT)
- Module 10 — Testing
- Module 11 — Docker and deployment

---

## Project Brief

**Build a production-ready Task Management API** (or a domain of your choosing — see alternatives below).

The system must support:
1. **User accounts** — registration, login, JWT authentication with refresh tokens
2. **Organizations** — users can create organizations and invite other users as members
3. **Projects** — organizations can have multiple projects
4. **Tasks** — projects contain tasks with title, description, status, assignee, and due date
5. **Role-based access** — organization owners can do everything; members can see and update tasks but not delete projects; non-members cannot see anything

### Alternative Domains

If task management does not interest you, you may substitute another domain, as long as it has equivalent complexity:
- **Inventory management** — warehouses, items, categories, stock movements
- **Event management** — events, tickets, attendees, venues
- **Recipe collection** — recipes, ingredients, collections, sharing
- **Bookmark manager** — URLs, tags, collections, sharing with permissions

Whatever domain you choose, the technical requirements below apply equally.

---

## Framework Choice

**Recommended: FastAPI** — The capstone's requirements (async DB access, JWT auth, OpenAPI docs, Docker) align naturally with FastAPI's strengths.

**Acceptable: Django** — Use Django REST Framework. The capstone's requirements are achievable with Django + DRF.

**Acceptable: Flask** — Use Flask with SQLAlchemy and JWT. This is the hardest path because you assemble more components manually.

Document your choice and your reasoning in the project's README.

---

## Acceptance Criteria

Your completed project must satisfy all of the following. Each criterion corresponds to skills from specific modules.

### Authentication (Module 09)
- [ ] `POST /auth/register` — creates a user with hashed password; returns 201 on success, 409 if email taken
- [ ] `POST /auth/login` — returns a short-lived access token (15 min) and a long-lived refresh token (7 days)
- [ ] `POST /auth/refresh` — exchanges a valid refresh token for a new access token and rotates the refresh token
- [ ] `POST /auth/logout` — invalidates the current refresh token
- [ ] All protected endpoints return 401 for missing/invalid tokens and 403 for insufficient permissions

### Core Resources (Modules 04/06)
- [ ] Full CRUD for Organizations, Projects, and Tasks
- [ ] All resources are properly scoped to the authenticated user's organization memberships
- [ ] List endpoints support pagination (limit/offset or cursor-based)
- [ ] Task list supports filtering by status and assignee

### Database (Module 08)
- [ ] PostgreSQL as the database (not SQLite)
- [ ] Alembic migrations for all schema changes
- [ ] No N+1 queries on any list endpoint (verified with query logging)
- [ ] Appropriate indexes on foreign keys and frequently filtered columns

### Testing (Module 10)
- [ ] `pytest` test suite with at least 30 tests
- [ ] ≥80% line coverage (measured with `pytest-cov`)
- [ ] Tests for the happy path and at least one error case per endpoint
- [ ] Test fixtures use `factory_boy` for test data generation
- [ ] Dependencies are overridden in tests (no real database in unit tests)

### Deployment (Module 11)
- [ ] `Dockerfile` with multi-stage build and non-root user
- [ ] `docker-compose.yml` that starts the app, PostgreSQL, and (if used) Redis with one command
- [ ] A `.env.example` file documenting all required environment variables
- [ ] `GET /health` endpoint that checks database connectivity and returns `{"status": "ok"}` or `{"status": "degraded", "checks": {...}}`

### Documentation
- [ ] OpenAPI docs at `/docs` are complete and accurate (if FastAPI or DRF with drf-spectacular)
- [ ] A `README.md` at the project root that covers: purpose, local setup, running tests, API overview

### CI/CD (Bonus — 15 pts)
- [ ] GitHub Actions workflow that runs tests and linting on every push
- [ ] Lint step uses `ruff` or `flake8`
- [ ] Type checking step uses `mypy` (FastAPI) or `pyright`

---

## Milestones

Work through these in order. Each milestone is a verifiable checkpoint.

### Milestone 1: Project Foundation (Est. 2–4 hours)

- Create the project structure (choose framework, set up virtual environment)
- Initialize git repository
- Write `docker-compose.yml` with the app and PostgreSQL
- Confirm `docker compose up` starts without errors
- Write the `GET /health` endpoint that returns 200
- Write your first test that calls `/health`

**Checkpoint:** `docker compose up && pytest tests/test_health.py` passes.

---

### Milestone 2: User Authentication (Est. 4–6 hours)

- Create the User model with email and hashed password
- Write Alembic migration and apply it
- Implement `POST /auth/register` and `POST /auth/login`
- Generate and validate JWT tokens
- Implement `POST /auth/refresh` with token rotation
- Write tests for the auth flow (register → login → use access token → refresh)

**Checkpoint:** A complete auth flow works end-to-end in tests.

---

### Milestone 3: Core Resources (Est. 6–10 hours)

- Create Organization, Membership, Project, and Task models
- Write migrations
- Implement CRUD endpoints for each resource
- Implement role-based access control
- Add pagination to list endpoints
- Add filtering to the task list

**Checkpoint:** Full CRUD for all resources with auth protection; all list endpoints are paginated.

---

### Milestone 4: Quality and Testing (Est. 4–6 hours)

- Write factory_boy factories for all models
- Write tests for all endpoints: happy path + key error cases
- Check for N+1 queries; fix any found
- Reach ≥80% coverage
- Add indexes for foreign keys and filter columns

**Checkpoint:** `pytest --cov` reports ≥80% coverage; no N+1 queries.

---

### Milestone 5: Production Polish (Est. 3–5 hours)

- Finalize Dockerfile with multi-stage build and non-root user
- Write `.env.example`
- Ensure `/health` checks database connectivity
- Complete the README
- (Optional) Add GitHub Actions CI

**Checkpoint:** `docker compose up` starts the full stack; README explains how to set it up from scratch.

---

## Architecture Guidance

These are suggestions, not requirements. Make your own architectural decisions — but use the hints here if you are stuck.

### Directory Structure (FastAPI)

```text
myapi/
├── alembic/               # Migrations
├── myapi/
│   ├── __init__.py
│   ├── main.py            # FastAPI app creation, lifespan
│   ├── config.py          # pydantic-settings Settings class
│   ├── database.py        # Engine, session factory, get_db dependency
│   ├── models/            # SQLAlchemy models
│   │   ├── user.py
│   │   ├── organization.py
│   │   └── task.py
│   ├── schemas/           # Pydantic request/response schemas
│   │   ├── auth.py
│   │   ├── organization.py
│   │   └── task.py
│   ├── routers/           # APIRouter instances
│   │   ├── auth.py
│   │   ├── organizations.py
│   │   └── tasks.py
│   ├── dependencies/      # Depends() functions
│   │   ├── auth.py        # get_current_user
│   │   └── db.py          # get_db
│   └── services/          # Business logic (optional)
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── factories.py       # factory_boy factories
│   ├── test_auth.py
│   ├── test_organizations.py
│   └── test_tasks.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Getting Unstuck

<details>
<summary><strong>Hint 1: Setting up the async SQLAlchemy session as a FastAPI dependency</strong></summary>

```python
# myapi/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from myapi.config import settings

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
```

Use it in a route: `db: AsyncSession = Depends(get_db)`.

</details>

<details>
<summary><strong>Hint 2: JWT access + refresh token rotation pattern</strong></summary>

Access tokens: short-lived (15 min), stateless, verified by signature alone.
Refresh tokens: long-lived (7 days), stored in the database (`RefreshToken` model), deleted on use.

On `POST /auth/refresh`:
1. Verify the refresh token's signature and expiry
2. Look it up in the database — if not found, it was already used (possible theft); invalidate all tokens for this user
3. If found, delete it from the database
4. Issue a new access token and a new refresh token
5. Store the new refresh token in the database
6. Return both tokens

This pattern is called "refresh token rotation" and prevents replay attacks.

</details>

<details>
<summary><strong>Hint 3: Avoiding N+1 queries on task lists</strong></summary>

If you load tasks and then access `task.project.name` in a loop, you get N+1 queries.

Fix with SQLAlchemy eager loading:

```python
from sqlalchemy.orm import selectinload

stmt = (
    select(Task)
    .options(selectinload(Task.project), selectinload(Task.assignee))
    .where(Task.organization_id == org_id)
)
result = await db.execute(stmt)
tasks = result.scalars().all()
```

Verify with `echo=True` on the engine during development — SQLAlchemy will print every query.

</details>

<details>
<summary><strong>Hint 4: Test fixture pattern with factory_boy and FastAPI dependency overrides</strong></summary>

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from myapi.main import app
from myapi.database import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

TEST_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5433/testdb"

@pytest.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DATABASE_URL)
    yield eng
    await eng.dispose()

@pytest.fixture
async def db_session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal(bind=engine)() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

</details>

<details>
<summary><strong>Hint 5: Multi-stage Dockerfile for a FastAPI app</strong></summary>

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir build && \
    pip install --no-cache-dir --target=/app/deps .

# Stage 2: Production image
FROM python:3.12-slim
RUN useradd -m -u 1000 appuser
WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY myapi/ ./myapi/
COPY alembic/ ./alembic/
COPY alembic.ini .
ENV PYTHONPATH=/app/deps
USER appuser
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "myapi.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

</details>

---

## Evaluation Rubric

| Category | Points | Notes |
|----------|--------|-------|
| Authentication works correctly | 20 | All auth endpoints; refresh token rotation |
| Core CRUD resources | 20 | All resources; correct scoping; pagination |
| Role-based access control | 15 | Owner vs member; 403 for unauthorized ops |
| Database correctness | 10 | No N+1; migrations; indexes |
| Test suite (≥30 tests, ≥80% coverage) | 15 | factory_boy; dependency overrides |
| Docker and deployment | 10 | Dockerfile; docker-compose; health check |
| Documentation | 10 | README; OpenAPI docs (if FastAPI/DRF) |
| **Total** | **100** | |
| GitHub Actions CI | +15 | Bonus |

---

## Submission

When your project is complete:

1. Push your code to a GitHub repository
2. Add the repository URL to this file under "My Project"
3. Confirm all acceptance criteria are checked off above
4. (Optional) Deploy to a cloud provider (Fly.io, Railway, Render) and add the live URL

### My Project

- **Repository:** _Add your GitHub repository URL here_
- **Live URL:** _Add deployment URL here (optional)_
- **Framework used:** _Flask / Django / FastAPI_
- **Completed:** _Add date_
- **Notes:** _Anything you want to record about your approach or what you learned_
