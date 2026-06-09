# Module 10: API Gateway and Platforms

[← Module 09: API Testing](../09_api-testing/README.md) | [Topic Home](../../README.md) | [Next → Module 11: Event-Driven APIs](../11_event-driven-apis/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-6h-orange)

> Kong, AWS API Gateway, Apigee, GraphQL gateway patterns (Apollo Router, Cosmo), rate limiting at the gateway layer, and authentication delegation.

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

Individual REST and GraphQL APIs work well at small scale. At the scale of organisations with
dozens or hundreds of services, each with its own API, a new problem emerges: cross-cutting
concerns — authentication, rate limiting, logging, routing, caching, TLS termination — get
duplicated in every service. API gateways solve this by providing a single entry point that
handles these cross-cutting concerns centrally. This module covers the major API gateway options
(Kong, AWS API Gateway, Apigee), the specialised GraphQL gateway patterns (Apollo Federation
Router, Cosmo Router), and the architectural patterns for routing, auth delegation, and rate
limiting at the gateway layer.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 07: GraphQL Advanced — Federation architecture is central to GraphQL gateway patterns
- Module 08: API Security — Rate limiting, authentication, and security headers are gateway responsibilities
- Module 04: API Authentication — JWT validation and OAuth2 are commonly handled at the gateway

---

## Objectives

By the end of this module, you will be able to:

1. Explain what an API gateway does and why it exists in a microservices architecture
2. Configure Kong to route, authenticate, and rate-limit a REST API
3. Describe the differences between Kong, AWS API Gateway, and Apigee and when to use each
4. Explain the Apollo Federation Router architecture and how it composes subgraph schemas
5. Implement authentication delegation (JWT validation at gateway; pass claims to upstream services)
6. Design a rate limiting strategy at the gateway layer for a multi-tenant API platform

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - What API Gateways Do: routing (path prefix → upstream service), TLS termination, auth delegation, rate limiting, request/response transformation, logging, caching
> - Kong: open-source API gateway; plugin system; declarative configuration with decK; JWT plugin, rate limiting plugin, key-auth plugin
> - AWS API Gateway: REST API vs. HTTP API vs. WebSocket API; Lambda integration; Cognito authoriser; usage plans
> - Apigee: Google's enterprise API platform; policy model; developer portal; analytics
> - GraphQL Gateway Patterns: Apollo Router (federation gateway); Cosmo Router (alternative); how the router composes subgraph schemas and routes field requests to the right service
> - Auth Delegation: the gateway validates the JWT; it forwards the user identity (claims) to upstream services via headers (`X-User-ID`, `X-User-Role`); upstream services trust the gateway
> - Rate Limiting at Gateway: per consumer, per route, per API key; global vs. distributed rate limiting; Redis-backed counters for multi-instance gateways

---

## Key Concepts

- **API gateway**: A server that acts as the single entry point for API clients, routing requests to backend services and handling cross-cutting concerns centrally.
- **Upstream service**: The backend service that the gateway routes traffic to. The service only sees authenticated, rate-limited, pre-processed requests from the gateway.
- **Plugin/policy**: A modular unit of gateway behaviour. Kong uses plugins (e.g., `rate-limiting`, `jwt`, `key-auth`); Apigee uses policies; AWS API Gateway uses authorisers and integrations.
- **Authentication delegation**: The gateway validates the client's credentials (JWT, API key) and passes the verified identity to upstream services, so upstream services don't need to implement their own auth.
- **Apollo Router**: Apollo's open-source Federation gateway — it composes the supergraph schema from subgraph schemas and routes each field to the appropriate subgraph.
- **Service mesh vs. API gateway**: A service mesh (Istio, Linkerd) handles east-west (service-to-service) traffic; an API gateway handles north-south (external client → services) traffic.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: Kong plugin configuration (declarative), Apollo Router supergraph composition, authentication delegation pattern, rate limiting configuration.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: gateway becoming a single point of failure (need redundancy), leaking implementation details through the gateway (should be transparent), using gateway for business logic (it should be infrastructure only).

---

## Cross-Links

- [[graphql-rest/modules/07_graphql-advanced]] — Apollo Federation subgraphs are what the gateway composes
- [[graphql-rest/modules/08_api-security]] — Security controls are typically implemented at or near the gateway
- [[systems-architecture]] — API gateways are a core distributed systems pattern; service mesh comparison
- [[devops-platform-engineering]] — API gateways are deployed and managed as infrastructure

---

## Summary

> [!NOTE]
> Full summary pending.
