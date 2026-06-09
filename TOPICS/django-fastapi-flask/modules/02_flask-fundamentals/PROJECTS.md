# Projects: Module 02 — Flask Fundamentals

## Project 1 — Personal Blog (Beginner)

**Difficulty:** Beginner
**Estimated Time:** 4–6 hours

Build a simple blog with Flask. Use Jinja2 templates for the HTML. Organize the code into at least two Blueprints: one for public-facing pages and one for admin pages. Use the application factory pattern. Store posts in a Python list (no database yet — that comes in Module 03).

**Acceptance Criteria:**
- `GET /` lists all blog posts (title, date, excerpt)
- `GET /posts/<slug>` shows a single post
- Jinja2 template inheritance with a base layout (header, footer, nav)
- At least two Blueprints registered on the app
- Application factory pattern (`create_app()`)
