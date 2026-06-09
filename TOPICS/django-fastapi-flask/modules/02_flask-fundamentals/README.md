# Module 02: Flask Fundamentals — Routes, Templates, Blueprints, and the App Factory

[← Module 01: Introduction](../01_introduction/README.md) | [Topic Home](../../README.md) | [Next → Module 03: Flask Advanced](../03_flask-advanced/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green)
![Time](https://img.shields.io/badge/time-4--6h-orange)

> **Stub module.** This module covers Flask routing, Jinja2 templates, request/response handling, Blueprints, and the application factory pattern. Full content to be generated on demand.

---

## Overview

This module takes you from a single-file Flask app to a structured, maintainable Flask project. You will learn how Flask's URL routing system works, how to use Jinja2 templates to render HTML, how to read query parameters and form data from requests, and how to organize a growing application using Blueprints and the application factory pattern.

By the end of this module, you will have a working multi-blueprint Flask application that could be the foundation of a real project.

---

## Prerequisites

- Module 01: Introduction — WSGI, Flask routing basics, running Flask locally
- Python decorators — the `@app.route()` decorator is central to Flask
- Basic HTML — Jinja2 templates generate HTML; you need to understand HTML structure

---

## Objectives

By the end of this module, you will be able to:

1. Define Flask routes with static and dynamic URL segments, type converters, and multiple HTTP methods
2. Use Jinja2 templates to render HTML responses with variables, loops, conditionals, and template inheritance
3. Read query parameters, form data, and JSON bodies from incoming requests
4. Send responses with custom status codes and headers using `make_response`
5. Organize a Flask application into Blueprints with URL prefixes
6. Implement the application factory pattern with `create_app(config=None)`
7. Configure a Flask application for different environments (development, testing, production)

---

## Topics Covered

- URL routing: static routes, dynamic segments (`<int:id>`, `<string:name>`), URL converters
- Request object: `request.args`, `request.form`, `request.get_json()`, `request.files`, `request.headers`
- Response object: `make_response()`, setting status codes, setting headers, cookies
- Jinja2: variables, filters, loops, conditionals, template inheritance (`{% extends %}`, `{% block %}`)
- Flask Blueprints: creating, registering, URL prefixes, blueprint-specific templates
- Application factory: `create_app()`, `app.config`, `from_object()`, `from_envvar()`
- Flask contexts: application context, request context, `g` object, `current_app`

---

## Key Code Patterns

The application factory pattern — the most important structural pattern in Flask:

```python
# myapp/__init__.py
from flask import Flask

def create_app(config=None):
    app = Flask(__name__)

    # Load default configuration
    app.config.from_object("myapp.config.DefaultConfig")

    # Override with provided config (for testing)
    if config:
        app.config.update(config)

    # Register blueprints
    from myapp.auth import auth_bp
    from myapp.api import api_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
```

---

## Cross-Links

- [[django-fastapi-flask/modules/01_introduction]] — WSGI foundation, first Flask app
- [[django-fastapi-flask/modules/03_flask-advanced]] — adds databases, authentication, and testing to this module's structure
- [[shared/glossary#app-factory]] — glossary entry for the application factory pattern
- [[shared/glossary#blueprint]] — glossary entry for Flask Blueprints

---

## Summary

- Flask routes are defined with `@app.route()` or `@bp.route()` decorators
- Dynamic URL segments extract variables from the URL path; type converters validate them
- The `request` object gives you access to all incoming request data
- Jinja2 templates separate presentation from logic; template inheritance reduces repetition
- Blueprints split a large Flask app into logical, reusable modules
- The application factory pattern is the correct way to structure any non-trivial Flask app
