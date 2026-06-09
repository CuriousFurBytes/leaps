# Resources: Django, FastAPI and Flask — Python Web Frameworks

> A curated list of verified, high-quality resources for this topic. Resources are organized by type and framework. All URLs were verified at time of writing.

---

## Table of Contents

- [Official Documentation](#official-documentation)
- [Books](#books)
- [Online Courses and Tutorials](#online-courses-and-tutorials)
- [Reference Projects and Examples](#reference-projects-and-examples)
- [Tools](#tools)

---

## Official Documentation

The official docs are authoritative and kept up to date. Always check the version number — Flask, Django, and FastAPI all have multiple active versions with API differences.

- **[Flask Documentation](https://flask.palletsprojects.com/)** — The official Flask docs. The "Quickstart" and "Tutorial" sections are excellent starting points. The "API Reference" section is the ground truth for every object and function.
- **[Django Documentation](https://docs.djangoproject.com/)** — Exceptionally well-written official docs. The "Tutorial" (Parts 1–7) is among the best framework tutorials in any language. The "Topic guides" section covers ORM, migrations, forms, and testing in depth.
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)** — Sebastián Ramírez wrote the FastAPI docs himself and they are extremely detailed. The "Tutorial - User Guide" is step-by-step and covers every major feature. The "Advanced User Guide" covers WebSockets, background tasks, lifespan events, and security.
- **[Pydantic v2 Documentation](https://docs.pydantic.dev/)** — FastAPI's data validation layer. Understanding Pydantic deeply is essential for effective FastAPI use.
- **[SQLAlchemy Documentation](https://docs.sqlalchemy.org/)** — The ORM and Core layers used by Flask and FastAPI (and optionally with Django). The 2.0 docs cover the new "2.0 style" query API.
- **[Django REST Framework Documentation](https://www.django-rest-framework.org/)** — The de facto standard for building JSON APIs with Django. Covers serializers, viewsets, routers, authentication, and permissions.

---

## Books

- **"Two Scoops of Django" by Daniel Audrey Roy Greenfeld and Daniel Roy Greenfeld** — The practical guide to Django best practices. Covers project layout, settings management, security, testing, and deployment patterns that the official docs don't emphasize. [Verify: confirm current edition covers Django 4.x at https://www.feldroy.com/books/two-scoops-of-django-3-x]
- **"Flask Web Development" by Miguel Grinberg (O'Reilly)** — The definitive Flask book. Covers the full development lifecycle: templates, databases, forms, user authentication, email, testing, deployment. The second edition covers Flask 1.x; the third edition covers newer versions. Available at O'Reilly Learning.
- **"Django for Professionals" by William S. Vincent** — Covers building production Django applications with Docker, PostgreSQL, and deployment. Good for learners who want a practical, project-driven approach.
- **"Architecture Patterns with Python" by Harry Percival and Bob Gregory (O'Reilly)** — Advanced book covering domain-driven design and clean architecture patterns using Flask as the example framework. Relevant to Module 03 and the capstone. [Available free online at https://www.cosmicpython.com/]

---

## Online Courses and Tutorials

- **[The Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)** — A free, comprehensive 23-part tutorial series that walks through building a complete Flask social blogging application. One of the best free Flask learning resources available.
- **[Django Girls Tutorial](https://tutorial.djangogirls.org/)** — A beginner-friendly Django tutorial that builds a blog application end-to-end. Excellent for absolute beginners; covers deployment to PythonAnywhere.
- **[Real Python — Flask Tutorials](https://realpython.com/tutorials/flask/)** — High-quality Flask tutorials covering specific topics. The "Flask by Example" series and "Python Web Applications" tutorial are particularly useful.
- **[TestDriven.io](https://testdriven.io/)** — Paid platform with high-quality courses on FastAPI, Django, and Flask that emphasize testing, Docker, and production patterns. The FastAPI course and Django course are among the most thorough available.

---

## Reference Projects and Examples

- **[FastAPI full-stack example](https://github.com/fastapi/full-stack-fastapi-template)** — Official FastAPI project template with PostgreSQL, Docker, authentication, and frontend. Good reference for production project structure.
- **[cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)** — The most widely used Django project template. Studying its structure teaches real-world Django project organization, settings management, and deployment configuration.
- **[Pallets Projects — Flask examples](https://github.com/pallets/flask/tree/main/examples)** — Official Flask example applications including a simple todo app and a blog (Flaskr, the same app used in the official tutorial).

---

## Tools

- **[Postman](https://www.postman.com/)** or **[Insomnia](https://insomnia.rest/)** — GUI tools for testing HTTP APIs. Useful for manually testing endpoints while developing.
- **[httpie](https://httpie.io/)** — Command-line HTTP client with a more human-friendly interface than curl. Install with `pip install httpie`.
- **[SQLite Browser (DB Browser for SQLite)](https://sqlitebrowser.org/)** — GUI tool for inspecting SQLite databases, useful in early development before switching to PostgreSQL.
- **[pgAdmin](https://www.pgadmin.org/)** — GUI administration tool for PostgreSQL. Useful in Modules 08 and beyond when working with production database patterns.
- **[pytest](https://docs.pytest.org/)** — The testing framework used throughout this topic. The docs are essential reading before Module 10.
- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** — Required for Module 11. Install early so it is ready when you reach the deployment module.
