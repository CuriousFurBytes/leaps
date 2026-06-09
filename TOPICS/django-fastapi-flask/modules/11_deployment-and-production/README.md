# Module 11: Deployment and Production — Docker, Gunicorn/Uvicorn, nginx, Config, and Health Checks

[← Module 10: Testing Web Applications](../10_testing-web-applications/README.md) | [Topic Home](../../README.md) | [Next → Module 12: Capstone Project](../12_capstone-project/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers containerizing Python web applications with Docker, configuring Gunicorn and Uvicorn for production, setting up nginx as a reverse proxy, managing environment-specific configuration, and implementing health check endpoints. Full content to be generated on demand.

---

## Overview

Deploying a web application requires understanding the full stack from your Python code down to the operating system. This module teaches you to containerize any of the three frameworks with Docker, configure the application server correctly, place nginx in front as a reverse proxy, manage configuration across environments, and implement observability through health checks and structured logging.

---

## Prerequisites

- All preceding modules — a complete application to deploy
- Basic Docker concepts — `docker build`, `docker run`, volumes, environment variables
- Basic Linux/shell — file permissions, environment variables, process management

---

## Objectives

By the end of this module, you will be able to:

1. Write a production-quality Dockerfile for a Python web application with multi-stage builds
2. Configure Gunicorn for Flask and Django with correct worker count, timeout, and graceful shutdown
3. Configure Uvicorn (standalone or via Gunicorn) for FastAPI with async worker settings
4. Configure nginx as a reverse proxy that passes requests to Gunicorn/Uvicorn and serves static files directly
5. Manage environment-specific configuration using environment variables, `.env` files, and `pydantic-settings`
6. Implement `/health` and `/ready` endpoints that reflect the application's real operational status

---

## Topics Covered

- Dockerfile best practices: multi-stage builds, non-root users, layer caching, `.dockerignore`
- Docker Compose: `docker-compose.yml` for local development with app + db + redis
- Gunicorn configuration: `--workers`, `--worker-class`, `--timeout`, `--graceful-timeout`, `--bind`, `--preload-app`
- Uvicorn configuration: `--workers`, `--loop`, `--http`, `--ssl-keyfile/certfile`
- nginx as reverse proxy: `proxy_pass`, `upstream`, static file serving, gzip, connection timeouts
- Environment configuration: `os.environ`, `pydantic-settings`, `python-decouple`, `.env` files, 12-factor app
- Health checks: liveness vs readiness probes, `GET /health` returning `{"status": "ok"}`, checking DB connectivity
- Structured logging: JSON log format, log levels, `python-json-logger`, correlating logs with request IDs
- Graceful shutdown: SIGTERM handling, draining in-flight requests, database connection cleanup
- Static files: Django's `collectstatic`, whitenoise for serving static files from Python

---

## Cross-Links

- [[django-fastapi-flask/modules/01_introduction]] — WSGI/ASGI and the role of gunicorn/uvicorn
- [[django-fastapi-flask/modules/12_capstone-project]] — Docker and deployment are capstone requirements
- [[shared/glossary#middleware]] — nginx as middleware layer

---

## Summary

- Multi-stage Docker builds keep production images small by discarding build-time dependencies
- Gunicorn worker count: `(2 × CPU cores) + 1` is the common starting formula; tune based on profiling
- Uvicorn workers for FastAPI: use `gunicorn -k uvicorn.workers.UvicornWorker` in production for process management
- nginx handles TLS termination, static files, gzip compression, and connection queuing — never expose Gunicorn/Uvicorn directly to the internet
- Configuration belongs in environment variables, not in code; the 12-factor app principle is the right model
- Health checks must reflect actual service health: a `/health` endpoint that always returns 200 regardless of DB connectivity is worse than useless
