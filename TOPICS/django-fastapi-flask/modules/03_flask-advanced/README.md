# Module 03: Flask Advanced — SQLAlchemy, Authentication, Forms, Testing, and Deployment

[← Module 02: Flask Fundamentals](../02_flask-fundamentals/README.md) | [Topic Home](../../README.md) | [Next → Module 04: Django Fundamentals](../04_django-fundamentals/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers Flask-SQLAlchemy, Flask-Login for session authentication, Flask-WTF for form handling and CSRF, pytest testing with the Flask test client, and deploying Flask with Gunicorn. Full content to be generated on demand.

---

## Overview

This module completes the Flask stack. You will add a real database layer using Flask-SQLAlchemy, implement user authentication with Flask-Login (session-based), add form handling and CSRF protection with Flask-WTF, write a meaningful pytest test suite using Flask's test client, and deploy the application with Gunicorn.

By the end of this module, you will have built a complete, tested, deployable Flask application that is indistinguishable in structure from a production codebase.

---

## Prerequisites

- Module 02: Flask Fundamentals — application factory, Blueprints, routing
- Basic SQL — SELECT, INSERT, UPDATE, DELETE, foreign keys
- Basic pytest — writing a `def test_` function, running `pytest`

---

## Objectives

By the end of this module, you will be able to:

1. Configure Flask-SQLAlchemy with the application factory and define model classes
2. Perform CRUD operations using SQLAlchemy's session API
3. Write and run Alembic migrations through Flask-Migrate
4. Implement user registration and login using Flask-Login with hashed passwords (bcrypt)
5. Handle HTML forms with Flask-WTF and protect state-changing routes with CSRF tokens
6. Write pytest tests for Flask routes using the `app.test_client()` fixture
7. Deploy a Flask application with Gunicorn and understand worker configuration

---

## Topics Covered

- Flask-SQLAlchemy: setup, `db.Model`, `db.Column`, relationships, `db.session`, `db.create_all()`
- Flask-Migrate: `flask db init`, `flask db migrate`, `flask db upgrade`
- Flask-Login: `LoginManager`, `UserMixin`, `login_user()`, `logout_user()`, `current_user`, `@login_required`
- Password hashing with `werkzeug.security` (bcrypt-backed `generate_password_hash`, `check_password_hash`)
- Flask-WTF: `FlaskForm`, `StringField`, `PasswordField`, `SubmitField`, CSRF protection
- pytest with Flask: `@pytest.fixture`, `create_app` with test config, `client.get()`, `client.post()`
- Gunicorn: `gunicorn "myapp:create_app()"`, `--workers`, `--bind`, worker types

---

## Cross-Links

- [[django-fastapi-flask/modules/02_flask-fundamentals]] — application factory and Blueprints foundation
- [[django-fastapi-flask/modules/08_database-patterns]] — deeper coverage of SQLAlchemy patterns (N+1, pooling)
- [[django-fastapi-flask/modules/09_authentication-and-security]] — JWT and OAuth2 authentication patterns
- [[django-fastapi-flask/modules/10_testing-web-applications]] — comprehensive testing module
- [[shared/glossary#session]] — sessions explained
- [[shared/glossary#csrf]] — CSRF explained

---

## Summary

- Flask-SQLAlchemy wraps SQLAlchemy to integrate cleanly with the application factory pattern
- Flask-Migrate uses Alembic to generate and apply schema migrations
- Flask-Login manages user sessions; `@login_required` protects routes
- Flask-WTF makes form handling and CSRF protection simple and automatic
- The Flask test client is synchronous; test the full request-response cycle with `client.get()` and `client.post()`
- Gunicorn is the correct production server for Flask (WSGI); configure workers as `2 × CPU_count + 1`
