# Projects: Django, FastAPI and Flask — Python Web Frameworks

> Six project ideas spanning beginner to expert. Work through them in order, or jump to one that matches your current skill level. Each project builds on the modules listed in its Prerequisites section.

---

## Project 1 — Personal URL Shortener (Beginner)

**Difficulty:** Beginner
**Framework:** Flask
**Prerequisites:** Modules 01–02
**Estimated Time:** 4–6 hours

### Brief

Build a URL shortener service in Flask. Users POST a long URL and receive a short code. Visiting the short URL redirects to the original. Store URL mappings in a SQLite database using raw SQL or SQLite's built-in Python module (not SQLAlchemy — this project is about understanding routing and redirects without an ORM).

### Acceptance Criteria

- `POST /shorten` accepts `{"url": "https://example.com/long/path"}` and returns `{"short_code": "abc123"}`
- `GET /<short_code>` performs a 301 redirect to the original URL
- Returns 404 for unknown short codes
- Stores mappings in a SQLite file; data persists across app restarts
- No third-party libraries except Flask itself

### Extension Ideas

- Add a click counter and a `GET /<short_code>/stats` endpoint
- Add expiry timestamps to shortened URLs
- Add a simple HTML form at the root route

---

## Project 2 — Task Manager REST API (Beginner → Intermediate)

**Difficulty:** Beginner → Intermediate
**Framework:** Flask with Flask-SQLAlchemy
**Prerequisites:** Modules 01–03
**Estimated Time:** 8–12 hours

### Brief

Build a task management REST API with user authentication. Users can register, log in, create tasks, mark them complete, and delete them. Each user sees only their own tasks.

### Acceptance Criteria

- `POST /auth/register` creates a new user (hashed password with bcrypt)
- `POST /auth/login` returns a session cookie or JWT
- `GET /tasks` returns the authenticated user's tasks
- `POST /tasks` creates a task with title, description, and due date
- `PATCH /tasks/<id>` updates a task (partial update supported)
- `DELETE /tasks/<id>` deletes a task (user can only delete their own)
- Returns 401 for unauthenticated requests; 403 for unauthorized operations
- Uses the application factory pattern and Blueprints
- Has at least 10 pytest tests covering the happy path and error cases

---

## Project 3 — Django Blog with Admin (Intermediate)

**Difficulty:** Intermediate
**Framework:** Django
**Prerequisites:** Modules 04–05
**Estimated Time:** 10–15 hours

### Brief

Build a blog platform using Django. Authors can create, edit, and publish posts. Readers can view published posts and leave comments. The Django admin interface should be customized to give authors a usable content management experience.

### Acceptance Criteria

- `Post` model with title, slug, body (Markdown), author (FK to User), status (draft/published), and published_at
- `Comment` model with body, author name (non-authenticated), and FK to Post
- Public views: post list, post detail, comment submission
- Admin: customized `PostAdmin` with list display, search, filtering by status and author
- Slug is auto-generated from title but editable
- Comments are held for moderation by default (published by admin)
- Uses Django's built-in authentication for the author login
- At least 5 model tests and 5 view tests with Django's test client

---

## Project 4 — Inventory API with FastAPI (Intermediate → Advanced)

**Difficulty:** Intermediate → Advanced
**Framework:** FastAPI with SQLAlchemy 2.0
**Prerequisites:** Modules 06–08
**Estimated Time:** 12–18 hours

### Brief

Build an inventory management REST API for a small warehouse. Items have categories, quantities, and location codes. Users with different roles (viewer, editor, admin) have different permissions. The API auto-documents itself via FastAPI's OpenAPI integration.

### Acceptance Criteria

- Full CRUD for `Item` and `Category` resources
- JWT authentication with role-based access control (RBAC)
- `GET /items` supports filtering by category and pagination (limit/offset)
- Pydantic schemas for all request and response bodies (no raw dicts in routes)
- SQLAlchemy 2.0 async session with connection pooling
- Database migrations via Alembic
- OpenAPI docs at `/docs` with all endpoints documented
- 100% test coverage on the route layer using FastAPI's `TestClient`

---

## Project 5 — Multi-Framework Microservices System (Advanced)

**Difficulty:** Advanced
**Framework:** All three
**Prerequisites:** Modules 01–11
**Estimated Time:** 20–30 hours

### Brief

Build a three-service system where each service uses a different framework. The services communicate via HTTP. Choose a domain that makes sense for a microservices split — for example: a user/auth service (Django), a notification service (Flask), and a real-time event stream service (FastAPI with WebSockets).

### Acceptance Criteria

- Each service runs in its own Docker container
- Services communicate via documented internal APIs
- A Docker Compose file starts the entire system with `docker compose up`
- An nginx reverse proxy routes external traffic to the right service
- Each service has its own database (no shared databases)
- A README explains the architecture, each service's responsibilities, and the communication protocol
- At least 5 integration tests that test across service boundaries

### Extension Ideas

- Add a message queue (Redis or RabbitMQ) between services
- Add centralized logging (structured JSON logs shipped to a common endpoint)
- Add health check endpoints and a simple status dashboard

---

## Project 6 — Production SaaS Starter (Expert / Capstone)

**Difficulty:** Expert
**Framework:** FastAPI (with guidance to swap in Django if preferred)
**Prerequisites:** All 12 modules
**Estimated Time:** 30–50 hours

### Brief

Build a complete, production-ready SaaS-style backend. This is the kind of project you would ship at work or use as the foundation of a real product. It must handle authentication, billing-adjacent tenant logic (organizations with members), a real feature domain (your choice), comprehensive tests, containerized deployment, and CI/CD.

See [Module 12: Capstone Project](./modules/12_capstone-project/README.md) for the detailed brief, milestones, and graduated hints.

### Acceptance Criteria

- Organization and user management with role-based access control
- JWT authentication with refresh token rotation
- At least two feature domain resources (your choice of domain)
- PostgreSQL database with Alembic migrations
- Comprehensive test suite: unit, integration, and end-to-end tests with ≥80% coverage
- Docker Compose for local development
- GitHub Actions CI pipeline that runs tests and lints on every push
- OpenAPI documentation complete and accurate
- Deployed to a cloud provider (Fly.io, Railway, Render, or equivalent) with a public URL
