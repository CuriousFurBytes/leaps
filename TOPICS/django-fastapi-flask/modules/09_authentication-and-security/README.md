# Module 09: Authentication and Security — Sessions, JWT, OAuth2, CSRF, and Rate Limiting

[← Module 08: Database Patterns](../08_database-patterns/README.md) | [Topic Home](../../README.md) | [Next → Module 10: Testing Web Applications](../10_testing-web-applications/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-6--8h-orange)

> **Stub module.** This module covers session-based authentication, JWT authentication, OAuth2 flows, CSRF protection, and rate limiting — across all three frameworks. Full content to be generated on demand.

---

## Overview

Security is not a feature you add at the end — it is a property of the architecture. This module covers authentication and the most common web security concerns in depth, with implementations in all three frameworks. You will understand not just how to implement these patterns but why they exist and what attacks they defend against.

---

## Prerequisites

- Module 03: Flask Advanced — Flask-Login session auth
- Module 07: FastAPI Advanced — JWT in FastAPI
- Basic cryptography concepts: hashing (bcrypt, argon2), signing (HMAC), tokens

---

## Objectives

By the end of this module, you will be able to:

1. Implement session-based authentication with server-side session storage (Flask, Django)
2. Implement JWT authentication with access/refresh token rotation (all three frameworks)
3. Implement the OAuth2 authorization code flow for third-party login (e.g., GitHub OAuth)
4. Explain CSRF attacks and implement CSRF protection in session-based and token-based applications
5. Implement rate limiting at the application level and explain where it should live in the stack
6. Store passwords securely using bcrypt or argon2 and explain why MD5/SHA256 are insufficient

---

## Topics Covered

- Session-based auth: cookie + server-side session, `SESSION_*` settings in Django, Flask session signing
- JWT: structure (header.payload.signature), `python-jose`, access token expiry, refresh tokens, token rotation
- OAuth2 authorization code flow: redirect, authorization code exchange, access token, scopes
- CSRF: the attack mechanism, double-submit cookie pattern, synchronizer token pattern, when JWT sidesteps CSRF
- Rate limiting: `slowapi` for Flask/FastAPI, Django's `django-ratelimit`, IP-based and user-based limiting
- Password hashing: `passlib` with bcrypt, argon2, why salted hashing matters, timing attack resistance
- `HTTPS`-related security: `Secure` and `HttpOnly` cookie flags, `SameSite`, HSTS
- Security headers: `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`

---

## Cross-Links

- [[django-fastapi-flask/modules/03_flask-advanced]] — Flask-Login sessions
- [[django-fastapi-flask/modules/05_django-advanced]] — Django security middleware
- [[django-fastapi-flask/modules/07_fastapi-advanced]] — JWT in FastAPI
- [[shared/glossary#csrf]] — CSRF glossary entry
- [[shared/glossary#session]] — session glossary entry

---

## Summary

- Session auth stores state server-side; JWT stores state client-side in a signed token — choose based on scalability and revocation requirements
- JWT refresh token rotation is the pattern that makes token invalidation possible without server-side state
- CSRF only affects session-based auth; JWT APIs with `Authorization: Bearer` headers are not vulnerable to CSRF (but must not use cookies for the token)
- Rate limiting belongs at the reverse proxy (nginx) for IP-based limits and at the application for user-based limits
- Always hash passwords with bcrypt or argon2; never with unsalted MD5, SHA1, or SHA256
