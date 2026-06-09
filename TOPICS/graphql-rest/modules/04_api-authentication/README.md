# Module 04: API Authentication

[← Module 03: REST Advanced](../03_rest-advanced/README.md) | [Topic Home](../../README.md) | [Next → Module 05: GraphQL Fundamentals](../05_graphql-fundamentals/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6h-orange)

> API keys, Basic Auth, session cookies, OAuth2 flows (authorization code, client credentials, PKCE), and JWT structure and validation.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

Every non-trivial API requires authentication — the client must prove who it is before accessing
protected resources. This module covers the full spectrum of API authentication mechanisms, from
the simplest (API keys) to the most sophisticated (OAuth2 with PKCE). You will understand the
tradeoffs between different approaches, implement JWT validation, and configure OAuth2 flows
correctly. By the end, you will be able to choose the right authentication mechanism for any
API scenario and avoid the common security mistakes that lead to breaches.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 03: REST Advanced — REST API design fundamentals; OpenAPI (auth is documented with security schemes)
- Basic understanding of cryptography concepts (hashing, signatures) is helpful but not required

---

## Objectives

By the end of this module, you will be able to:

1. Implement API key authentication and explain its limitations
2. Explain how Basic Auth works and why it requires HTTPS
3. Describe the OAuth2 authorization code flow step by step, including what each parameter does
4. Explain the difference between authorization code + PKCE and client credentials flows, and when to use each
5. Decode a JWT, explain each section (header, payload, signature), and validate one in Python
6. Choose the appropriate authentication mechanism for a given API use case

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - API Keys: `X-API-Key` header pattern, key generation/storage, key rotation, per-key rate limiting
> - Basic Authentication: base64 encoding of `username:password`, why it requires HTTPS, why it's rarely recommended for modern APIs
> - Session cookies: server-side session storage, the session ID pattern, why this violates REST statelessness
> - OAuth2 Overview: why OAuth2 exists (delegated authorisation), the four roles (resource owner, client, authorisation server, resource server)
> - Authorization Code Flow: step-by-step with annotated request/response examples; state parameter; redirect URI; code exchange
> - PKCE (Proof Key for Code Exchange): why it exists (code interception attacks in public clients), `code_verifier` and `code_challenge`
> - Client Credentials Flow: machine-to-machine authentication; when to use it vs. authorization code
> - JWT (JSON Web Token): header.payload.signature structure; signing algorithms (HS256 vs RS256 vs ES256); claims; validation steps; expiry and refresh tokens
> - Token Storage: where to store JWTs (memory vs. localStorage vs. httpOnly cookie) and the security tradeoffs of each

---

## Key Concepts

- **API key**: An opaque token issued to a client. Simple but not delegated — the key represents the client application, not a user.
- **OAuth2**: An authorisation framework that allows a user to grant a third-party application access to their account without sharing their credentials.
- **Access token**: A short-lived token (typically 15 min – 1 hour) that represents an OAuth2 authorization grant.
- **Refresh token**: A long-lived token used to obtain new access tokens without re-authenticating the user.
- **JWT (JSON Web Token)**: A self-contained token with three base64url-encoded sections: header (algorithm), payload (claims), and signature.
- **PKCE**: Proof Key for Code Exchange — a security extension to the authorization code flow that prevents code interception attacks in public clients (mobile apps, SPAs).

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: complete OAuth2 authorization code + PKCE flow, JWT decoding and validation in Python, API key middleware implementation.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: storing tokens in localStorage (XSS vulnerability), not validating JWT signature, using implicit flow (deprecated), confusing authentication with authorisation (authn vs authz).

---

## Cross-Links

- [[graphql-rest/modules/03_rest-advanced]] — OpenAPI security schemes document the authentication mechanism
- [[graphql-rest/modules/08_api-security]] — Authentication is one layer of API security; Module 08 covers the broader security picture
- [[graphql-rest/modules/10_api-gateway-and-platforms]] — API gateways often handle authentication delegation (JWT validation at the gateway)
- [[networks]] — HTTPS/TLS is the transport security layer that makes Basic Auth and API keys safe

---

## Summary

> [!NOTE]
> Full summary pending.
