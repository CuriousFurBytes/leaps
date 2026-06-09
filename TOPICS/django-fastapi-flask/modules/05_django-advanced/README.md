# Module 05: Django Advanced — DRF, Signals, Celery, Caching, and Security

[← Module 04: Django Fundamentals](../04_django-fundamentals/README.md) | [Topic Home](../../README.md) | [Next → Module 06: FastAPI Fundamentals](../06_fastapi-fundamentals/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers Django REST Framework for JSON APIs, Django signals for event-driven logic, Celery for background task processing, Django's caching framework, and security middleware. Full content to be generated on demand.

---

## Overview

This module covers the patterns that take Django from a web application framework to the backbone of a production service. Django REST Framework (DRF) is the de facto standard for building JSON APIs with Django. Django signals allow decoupled components to react to model events. Celery handles background work — emails, report generation, webhook delivery — outside the HTTP request cycle. Django's caching framework reduces database load. And Django's security middleware handles CSRF, clickjacking, and XSS at the framework level.

---

## Prerequisites

- Module 04: Django Fundamentals — models, views, URL routing, ORM

---

## Objectives

By the end of this module, you will be able to:

1. Build a JSON REST API using Django REST Framework serializers, views, and routers
2. Configure DRF authentication (SessionAuthentication, TokenAuthentication) and permissions (IsAuthenticated, IsAdminUser)
3. Use Django signals (`post_save`, `post_delete`, `pre_save`) to respond to model events
4. Set up Celery with Redis as the broker and create async background tasks
5. Configure Django's caching framework (in-memory, file-based, Redis) and use `cache.get/set` and the `@cache_page` decorator
6. Explain Django's built-in security middleware and configure `SECURE_*` settings for production

---

## Topics Covered

- Django REST Framework: `Serializer`, `ModelSerializer`, `APIView`, `GenericAPIView`, `ViewSet`, `ModelViewSet`, `Router`
- DRF authentication: `SessionAuthentication`, `TokenAuthentication`, `BasicAuthentication`
- DRF permissions: `IsAuthenticated`, `IsAdminUser`, `IsAuthenticatedOrReadOnly`, custom permission classes
- DRF filtering, pagination, and ordering
- Django signals: `Signal`, `receiver`, `post_save`, `post_delete`, `m2m_changed`
- Celery: setup with Redis, `@shared_task`, `delay()`, `apply_async()`, periodic tasks with Celery Beat
- Django caching: `CACHES` setting, `cache.get/set/delete`, `@cache_page`, `@vary_on_headers`
- Security middleware: `SecurityMiddleware`, `CSRF`, `X-Frame-Options`, `SECURE_SSL_REDIRECT`, `HSTS`, `ALLOWED_HOSTS`

---

## Cross-Links

- [[django-fastapi-flask/modules/04_django-fundamentals]] — models and ORM foundation
- [[django-fastapi-flask/modules/07_fastapi-advanced]] — comparison: DRF vs FastAPI's approach to auth and permissions
- [[django-fastapi-flask/modules/09_authentication-and-security]] — security patterns across frameworks
- [[shared/glossary#serializer]] — serializer glossary entry
- [[shared/glossary#csrf]] — CSRF glossary entry
- [[async-python]] — async background task concepts relevant to Celery

---

## Summary

- DRF's ModelSerializer generates serialization from Django models; ViewSets and Routers reduce boilerplate for RESTful resources
- Signals allow components to react to model events without tight coupling — use them sparingly to avoid hidden dependencies
- Celery offloads slow work from the HTTP request cycle; Redis is the standard broker
- Django's caching framework is a simple `key:value` store; always set TTLs and design for cache misses
- Security middleware handles many common vulnerabilities automatically; understand what each setting does before disabling it
