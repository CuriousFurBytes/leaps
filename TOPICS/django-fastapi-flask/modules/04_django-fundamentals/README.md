# Module 04: Django Fundamentals — MTV, ORM, Migrations, Admin, and Views

[← Module 03: Flask Advanced](../03_flask-advanced/README.md) | [Topic Home](../../README.md) | [Next → Module 05: Django Advanced](../05_django-advanced/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers the Django MTV pattern, the ORM and QuerySet API, migrations, the admin interface, URL routing, and class-based vs function-based views. Full content to be generated on demand.

---

## Overview

Django's design philosophy is "convention over configuration." Where Flask made you choose and assemble every component, Django provides a complete, integrated system with strong opinions about how each part should work. This module teaches you Django's core conventions — the ones that every Django developer must internalize to be productive.

The MTV (Model–Template–View) pattern is Django's name for MVC. Models define data; Views handle requests and business logic; Templates render the response. The ORM translates between Python model classes and database tables. Migrations track schema changes. The admin interface is auto-generated from your models.

---

## Prerequisites

- Module 03: Flask Advanced — ORM concepts, migrations, session auth, testing
- Understanding of class-based programming in Python (inheritance, `super()`, class attributes)
- Basic HTML and SQL

---

## Objectives

By the end of this module, you will be able to:

1. Create a Django project and application with `django-admin startproject` and `manage.py startapp`
2. Define Django models with fields, relationships (ForeignKey, ManyToManyField), and `Meta` options
3. Write and apply migrations using `manage.py makemigrations` and `manage.py migrate`
4. Query the database using Django's QuerySet API (filter, exclude, annotate, select_related, prefetch_related)
5. Customize the Django admin interface to make it useful for content management
6. Define URL patterns in `urls.py` with `path()` and `re_path()`
7. Write function-based views (FBVs) and class-based views (CBVs) and explain the trade-offs between them

---

## Topics Covered

- Django project structure: `settings.py`, `urls.py`, `wsgi.py`, `manage.py`
- Django apps: `startapp`, `INSTALLED_APPS`, the app registry
- Models: field types, relationships (`ForeignKey`, `OneToOneField`, `ManyToManyField`), `Meta`, `__str__`
- QuerySet API: `filter()`, `exclude()`, `get()`, `create()`, `update()`, `delete()`, `annotate()`, `values()`, `distinct()`
- `select_related()` and `prefetch_related()` — solving the N+1 problem
- Migrations: `makemigrations`, `migrate`, `showmigrations`, `sqlmigrate`, data migrations
- Django admin: `ModelAdmin`, `list_display`, `list_filter`, `search_fields`, `readonly_fields`, inline models
- URL routing: `path()`, `include()`, named URLs, URL namespaces, `reverse()`
- Function-based views: `HttpRequest`, `HttpResponse`, `JsonResponse`, `render()`, `redirect()`
- Class-based views: `View`, `TemplateView`, `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`

---

## Cross-Links

- [[django-fastapi-flask/modules/03_flask-advanced]] — Flask ORM and migrations comparison
- [[django-fastapi-flask/modules/05_django-advanced]] — DRF, signals, Celery, and more
- [[django-fastapi-flask/modules/08_database-patterns]] — advanced ORM patterns
- [[shared/glossary#orm]] — ORM glossary entry
- [[shared/glossary#migration]] — migration glossary entry

---

## Summary

- Django's MTV pattern separates data (Model), presentation (Template), and request handling (View)
- The ORM maps Python classes to database tables; the QuerySet API provides a lazy, composable query interface
- Migrations are generated automatically from model changes and applied incrementally
- The Django admin is auto-generated from models and customizable for real content management
- URL routing in `urls.py` maps URL patterns to view functions or classes
- CBVs reduce boilerplate for common patterns (list, detail, create, update, delete); FBVs offer more explicit control
