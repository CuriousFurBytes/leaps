# GraphQL and REST API Design

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> The complete guide to designing, building, and consuming APIs — from Fielding's REST constraints to GraphQL schemas, federation, and production-grade API platforms.

> [!NOTE]
> **Topic Overview**
> APIs are the backbone of modern software. Every web application, mobile app, microservice,
> and cloud platform communicates through APIs. This topic teaches you to design, build, test,
> and operate APIs that are intuitive, reliable, secure, and scalable — starting from the first
> principles of HTTP through REST architecture, GraphQL schemas, resolvers, real-time subscriptions,
> API gateways, and finally a full capstone project where you ship a production-quality API.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty & Time Estimate](#difficulty--time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

An **API** (Application Programming Interface) is a contract: one piece of software declares what
it can do and how to ask it, and any other piece of software can call it without knowing the
internals. Every cloud service you use, every payment you process, every map that loads on a
website — all of it happens through APIs.

Two paradigms dominate modern API design: **REST** (Representational State Transfer), described by
Roy Fielding in his 2000 doctoral dissertation, and **GraphQL**, created at Facebook in 2012 and
open-sourced in 2015. REST approaches APIs as a set of *resources* accessed via standard HTTP
methods. GraphQL approaches them as a *typed schema* that clients can query with exactly the fields
they need. Neither is universally better — knowing when to use each, and how to use each well,
is the craft this topic teaches.

### Why It Matters

APIs are not just a technical detail — they are the primary interface through which modern systems
communicate. Poorly designed APIs cause cascading failures, painful versioning crises, security
breaches, and developer frustration that slows entire organisations. Well-designed APIs enable
rapid development, clean system boundaries, and long-term maintainability.

Understanding API design and development is valuable because:

- It underpins every web and mobile application — a skill used directly in backend development,
  frontend integration, and platform engineering
- It develops the mental model for distributed systems thinking — transferable to microservices,
  event-driven architectures, and cloud-native development
- Proficiency in it is expected in roles such as backend engineer, full-stack developer, platform
  engineer, API product manager, and solutions architect

### Key Features of This Topic

- **REST from first principles** — not just CRUD-over-HTTP, but Fielding's six constraints and
  why each one matters for scalability and evolvability
- **GraphQL from schema to production** — SDL, resolvers, mutations, subscriptions, the N+1
  problem, and federation for distributed graphs
- **Security at every layer** — authentication, authorization, rate limiting, CORS, injection
  prevention, and API abuse patterns
- **Real-world tooling** — OpenAPI/Swagger, Apollo Studio, Postman, Kong, AWS API Gateway,
  contract testing, and performance testing

---

## Historical Context

The history of API design is a history of escaping the complexity of the previous approach.

### Timeline

| Year | Event |
|------|-------|
| 1990s | **RPC and CORBA era** — Remote Procedure Calls and CORBA enable distributed computing, but are brittle, language-coupled, and hard to evolve |
| 1999 | **SOAP emerges** — XML-based SOAP and WSDL become the enterprise standard; powerful but verbose and heavily tooled |
| 2000 | **Roy Fielding publishes his dissertation** — "Architectural Styles and the Design of Network-based Software Architectures" defines REST and the six constraints that make the web scale |
| 2000–2006 | **The REST revolution** — Web 2.0 companies (Amazon, eBay, Google Maps) ship public REST APIs; developers discover REST is far simpler than SOAP |
| 2005–2015 | **HATEOAS debates** — the community argues about what "true REST" means; most APIs settle for "REST-ish" pragmatism |
| 2010 | **Swagger/OpenAPI created** — Swagger 1.0 gives REST a machine-readable description format; it becomes the de-facto standard |
| 2012 | **GraphQL created at Facebook** — facing mobile client data-shape explosion, Lee Byron and the Facebook team build a query language for APIs |
| 2015 | **GraphQL open-sourced** — Facebook releases the specification; the community explodes |
| 2016–2019 | **GraphQL adoption wave** — GitHub launches GraphQL API v4; Shopify, Twitter, and dozens of others follow; Apollo GraphQL becomes dominant |
| 2019 | **Apollo Federation introduced** — splits a GraphQL schema across multiple services, enabling the API gateway era |
| 2020+ | **API gateway and platform era** — Kong, AWS API Gateway, Apigee, and GraphQL federation become standard; The Graph Protocol applies GraphQL to decentralised data |
| Today | Actively used and developed across every domain of software |

---

## Real-World Applications

GraphQL and REST API design are actively used across every domain of software:

- **Social and content platforms** — GitHub uses both REST API v3 and GraphQL API v4; the GraphQL API allows fetching exactly the fields a client needs from complex repository graphs
- **E-commerce** — Shopify's GraphQL Admin API is the primary interface for building Shopify apps; Stripe's REST API is the gold standard for financial API design with clean resource models and idempotency keys
- **Media streaming** — Netflix operates one of the most studied API gateway architectures, routing traffic from hundreds of device types through a unified interface
- **Developer tooling** — Twitter/X API and npm registry API show how REST versioning and rate limiting work at scale
- **Blockchain and Web3** — The Graph Protocol enables decentralised indexing of blockchain data via GraphQL, allowing dApps to query on-chain data efficiently
- **Enterprise integration** — Salesforce, ServiceNow, and SAP all expose REST and GraphQL APIs for enterprise automation workflows

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain Fielding's six REST constraints and evaluate whether a given API satisfies them
2. Design a REST API resource model with correct URI structure, HTTP method semantics, and status code usage
3. Write an OpenAPI 3.x specification for a REST API and generate documentation from it
4. Implement OAuth2 flows (authorization code, client credentials, PKCE) and explain when to use each
5. Define a GraphQL schema using SDL, write queries, mutations, and subscriptions, and explain the execution model
6. Implement resolver functions, solve the N+1 problem using the DataLoader pattern, and batch-load data efficiently
7. Design and implement API security controls: CORS, rate limiting, input validation, and injection prevention
8. Write contract tests, integration tests, and performance tests for both REST and GraphQL APIs
9. Configure an API gateway for routing, authentication delegation, and rate limiting
10. Architect a production API platform combining REST, GraphQL, authentication middleware, rate limiting, and observability

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Beginner → Expert |
| **Estimated Total Hours** | 60–80 hours |
| **Prerequisites** | Basic HTTP knowledge, some programming experience (any language) |
| **Recommended Pace** | 5–7 hours/week |
| **Topic Type** | Computational (code examples: HTTP, GraphQL SDL, JSON, JavaScript, Python) |
| **Suitable For** | Backend developers, full-stack developers, platform engineers, API product managers |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- Basic HTTP — specifically: what HTTP requests and responses look like, what methods (GET/POST) are, what a status code means. Module 01 reviews this in detail.
- Some programming experience — specifically: comfortable reading Python or JavaScript. All code examples use Python and JavaScript; you do not need to be expert in either.
- [[networks]] — specifically: TCP/IP basics, DNS, what a URL is. Only needed for later modules; Module 01 assumes none of this.

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If you can follow the HTTP examples and understand what `curl` is doing, you're ready.
> If HTTP is entirely foreign, read the "HTTP Fundamentals" section of [[networks]] first.

---

## Learning Modules

| # | Module | Topic | Difficulty | Status | Score |
|---|--------|-------|-----------|--------|-------|
| 01 | [Introduction to APIs](./modules/01_introduction/) | What APIs are, HTTP review, REST vs. GraphQL first look | Beginner | - [ ] | —/— |
| 02 | [REST Fundamentals](./modules/02_rest-fundamentals/) | Resource modeling, URI design, HTTP methods, status codes, statelessness, idempotency | Beginner | - [ ] | —/— |
| 03 | [REST Advanced](./modules/03_rest-advanced/) | Versioning strategies, pagination, filtering, HATEOAS, OpenAPI/Swagger | Intermediate | - [ ] | —/— |
| 04 | [API Authentication](./modules/04_api-authentication/) | API keys, Basic Auth, OAuth2 flows, JWT structure and validation | Intermediate | - [ ] | —/— |
| 05 | [GraphQL Fundamentals](./modules/05_graphql-fundamentals/) | SDL, types and fields, queries, mutations, variables, fragments, introspection | Intermediate | - [ ] | —/— |
| 06 | [GraphQL Resolvers](./modules/06_graphql-resolvers/) | Resolver functions, context, N+1 problem, DataLoader, batch loading | Advanced | - [ ] | —/— |
| 07 | [GraphQL Advanced](./modules/07_graphql-advanced/) | Subscriptions, federation, persisted queries, schema stitching, error handling | Advanced | - [ ] | —/— |
| 08 | [API Security](./modules/08_api-security/) | CORS, rate limiting, input validation, injection prevention, abuse patterns | Advanced | - [ ] | —/— |
| 09 | [API Testing](./modules/09_api-testing/) | Contract testing (Pact), Postman/Newman, REST Assured, Apollo Studio, performance | Advanced | - [ ] | —/— |
| 10 | [API Gateway and Platforms](./modules/10_api-gateway-and-platforms/) | Kong, AWS API Gateway, Apigee, GraphQL gateway patterns, auth delegation | Expert | - [ ] | —/— |
| 11 | [Event-Driven APIs](./modules/11_event-driven-apis/) | Webhooks, SSE, WebSockets vs. SSE vs. polling, delivery guarantees | Expert | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Design and implement a public REST + GraphQL API with auth, rate limiting, and tests | Expert | - [ ] | —/— |

**Status key:** ` ` Not started · `~` In progress · `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 20 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 264 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 45 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **429** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to APIs)
- [ ] **Foundation Built** — Complete Modules 01–02 with ≥ 70% on each test
- [ ] **REST Practitioner** — Complete Modules 01–04 with ≥ 75% on all tests
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **GraphQL Ready** — Complete Modules 05–07 with ≥ 75% on all tests
- [ ] **API Security Aware** — Pass Module 08 test with ≥ 80%
- [ ] **First Project Shipped** — Complete at least one project from PROJECTS.md
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **API Architect** — Score ≥ 85% across all module tests and complete the capstone

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% · B ≥ 80% · C ≥ 70% · D ≥ 60% · F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for API Design:

- [[networks]] — HTTP, TCP/IP, and DNS are the substrate that REST and GraphQL run on; understanding the network layer helps debug API issues that look like application bugs
- [[django-fastapi-flask]] — Python web frameworks for implementing REST APIs; FastAPI in particular is tightly integrated with OpenAPI and makes schema-first API development straightforward
- [[kotlin-spring-android]] — Spring Boot is one of the most widely-used frameworks for building enterprise REST APIs; Android clients consume REST and GraphQL APIs from mobile apps
- [[systems-architecture]] — API design decisions (REST vs. GraphQL, gateways, versioning) are architectural decisions; this topic provides the patterns, systems-architecture provides the broader tradeoffs

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Started Topic

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed prerequisites: basic HTTP understanding

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "graphql-rest"
topic_name: "GraphQL and REST API Design"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 429
completion_percentage: 0
difficulty: "Beginner → Expert"
estimated_hours: 70
prerequisites:
  - "basic HTTP knowledge"
  - "some programming experience"
related_topics:
  - "networks"
  - "django-fastapi-flask"
  - "kotlin-spring-android"
  - "systems-architecture"
tags:
  - "apis"
  - "rest"
  - "graphql"
  - "http"
  - "backend"
  - "web"
creator: "Roy Fielding (REST, 2000), Lee Byron et al. (GraphQL, 2012)"
year_created: "2000 (REST), 2015 (GraphQL open-source)"
```
