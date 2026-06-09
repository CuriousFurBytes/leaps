# Module 12: Capstone Project — Design a Complete Distributed System

[← Module 11: Architecture Decision-Making](../11_architecture-decision-making/README.md) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-blue)
![Time](https://img.shields.io/badge/time-15h-orange)

> Design, document, and defend a complete distributed system for a real-world use case — applying every major concept from this topic in a coherent, reasoned architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [The Project Brief](#the-project-brief)
4. [Deliverables](#deliverables)
5. [Milestones](#milestones)
6. [Evaluation Criteria](#evaluation-criteria)
7. [Getting Unstuck](#getting-unstuck)
8. [Cross-Links](#cross-links)

---

## Overview

This is the capstone for the Systems Architecture topic. It is not a test of memorized patterns — it is a test of judgment. You will design a complete distributed system from scratch, making real trade-off decisions and documenting your reasoning.

The project is not about having the "right" architecture. There is no single correct answer. The goal is to demonstrate that you can:
1. Identify the real requirements and constraints
2. Reason through multiple design alternatives
3. Make deliberate, justified decisions
4. Acknowledge the costs of your choices
5. Document your design so another engineer could build it

> [!IMPORTANT]
> **This project is deliberately hard.** You will encounter situations where this topic's modules don't give you a clear answer. That is intentional. Real architecture work requires extrapolating from patterns you know to problems you haven't seen before. Use the modules as reference, reason from first principles, and commit to a decision.

> [!WARNING]
> **Do not look for a "reference solution" online.** There isn't one. Any system design you find online for similar problems will have made different trade-offs for different contexts. Your design should reflect your reasoning, not a template.

---

## Prerequisites

- All 11 preceding modules completed (or at least studied)
- CHEATSHEET.md reviewed and understood
- GLOSSARY.md populated with at least 10 terms you've encountered
- At least one ADR written from Module 11's content

---

## The Project Brief

Choose **one** of the following three use cases. They vary in the types of challenges they emphasize — choose the one that aligns with what you want to learn most.

---

### Option A: E-Commerce Platform

**System:** A mid-scale e-commerce platform (think: Etsy, small Amazon) with 50,000 daily active users and peak traffic of 5,000 concurrent users during sales events.

**Core user flows to support:**
1. User browses product catalog (search, filter, pagination)
2. User adds items to cart and checks out (inventory reservation → payment → order confirmation)
3. Seller lists a new product with images
4. User receives order confirmation and shipping updates
5. Platform admin monitors sales, fraud flags, and system health

**Functional requirements:**
- Product catalog with full-text search
- Real-time inventory (show "Only 3 left!")
- Payment processing (integrate with external payment processor)
- Order management (status tracking through fulfillment)
- Notifications (email + optional push)
- Seller dashboard

**Non-functional requirements:**
- Checkout must complete within 3 seconds p99
- System must remain available during single-AZ failure
- All financial transactions must be idempotent
- Fraud detection may be temporarily unavailable without blocking checkout

---

### Option B: Ride-Sharing Platform

**System:** A ride-sharing platform (Uber/Lyft scale at one city: 10,000 rides/day, 2,000 active drivers at peak).

**Core user flows to support:**
1. Rider requests a ride (matching algorithm finds nearby driver)
2. Driver accepts, ride begins
3. Real-time location tracking during ride
4. Ride ends, fare calculated, payment processed
5. Rating exchange between rider and driver

**Functional requirements:**
- Geospatial matching (find drivers within X km)
- Real-time location updates (WebSockets or SSE)
- Dynamic pricing (surge pricing)
- Payment processing
- Rating system
- Driver earnings dashboard

**Non-functional requirements:**
- Matching must complete within 5 seconds
- Location updates must be visible within 2 seconds
- Payment must be exactly-once (no double charges)
- System must handle complete failure of the matching service gracefully

---

### Option C: Social Platform

**System:** A social content platform (Twitter/X scale: 100,000 daily active users, 500 posts/minute at peak).

**Core user flows to support:**
1. User posts content (text, optional media)
2. User sees their home timeline (posts from people they follow)
3. User follows/unfollows other users
4. User receives notifications (likes, replies, mentions)
5. Content moderation (flagging inappropriate content)

**Functional requirements:**
- Post creation and storage
- Timeline generation (home feed — most recent posts from followed users)
- Follow graph
- Like and reply system
- Notifications
- Media storage and serving

**Non-functional requirements:**
- Timeline must load within 500ms p99
- A user with 1 million followers posting a new post must be visible in all followers' timelines within 5 minutes (eventual consistency acceptable)
- Notifications may be delayed by up to 30 seconds
- Media serving must use CDN

---

## Deliverables

Your capstone submission is a set of Markdown documents in this module's directory. You are building a design document, not code (though pseudocode and YAML examples are encouraged and expected).

### Required Deliverables

**1. `DESIGN.md` — System Overview**
- Executive summary (3–5 sentences: what the system does, who it serves, what makes it interesting architecturally)
- High-level architecture diagram (Mermaid flowchart showing all major services and their relationships)
- Technology choices with brief justification (database, message broker, caching, CDN, etc.)

**2. `SERVICES.md` — Service Decomposition**
- List of all services with:
  - Name and responsibility (one sentence)
  - Data owned (what tables/collections/schemas)
  - External dependencies (which other services it calls or subscribes to)
  - Bounded context it belongs to
- A context map diagram showing service relationships
- Justification for the most controversial decomposition decision

**3. `DATA.md` — Data Architecture**
- Data ownership table (which service owns what data)
- At least one schema definition for a core entity (SQL or JSON schema)
- How distributed consistency is handled (which flows use Saga? Which use Outbox?)
- How you handle the specific consistency challenge of your chosen use case

**4. `MESSAGING.md` — Messaging Topology**
- All topics/queues with producer and consumer(s) for each
- Delivery semantic for each topic (at-most-once / at-least-once / exactly-once) with justification
- Consumer group design
- Dead-letter queue strategy

**5. `RESILIENCE.md` — Resilience and Operations**
- Which services have circuit breakers and why
- Graceful degradation plan for at least 2 failure scenarios specific to your use case
- One chaos experiment proposal (hypothesis, failure injection, measurement plan)
- SLO definitions for at least 2 services

**6. `ADRS.md` — Architecture Decision Records**
- At least 4 ADRs covering the most significant decisions in your design
- Each ADR must follow the standard format (Status, Context, Options, Decision, Consequences)
- At least one ADR must document a decision you found genuinely difficult

**7. `FAILURE-MODES.md` — Failure Mode Analysis**
- Top 5 failure scenarios specific to your use case
- For each: what fails, what is the user experience, what prevents it, what is the recovery path

---

## Milestones

Work through the project in this order. Don't try to write everything at once.

### Milestone 1: Domain Analysis (2–3 hours)
- Choose your use case
- Identify the core entities (nouns) and operations (verbs)
- Draft the bounded context boundaries — which groupings feel natural?
- Do NOT think about technology yet

### Milestone 2: Service Decomposition (2–3 hours)
- Map bounded contexts to services
- Define data ownership
- Write `SERVICES.md` first draft
- Identify your most controversial decomposition decision and draft ADR-001

### Milestone 3: Data and Communication (3–4 hours)
- Write `DATA.md`
- Write `MESSAGING.md`
- Identify which flows need Sagas, which can be sync REST, which need Outbox
- Draft ADR-002 for your database/messaging choices

### Milestone 4: Resilience and Operations (2–3 hours)
- Write `RESILIENCE.md`
- Identify the 3 most dangerous failure scenarios for your use case
- Write `FAILURE-MODES.md`
- Draft ADR-003 and ADR-004

### Milestone 5: Integration and Review (2–3 hours)
- Write `DESIGN.md` (summary diagram, overview)
- Compile `ADRS.md`
- Review all deliverables: are there inconsistencies? (e.g., a service in SERVICES.md not in MESSAGING.md)
- Write an honest self-assessment: what would you do differently with more time?

---

## Evaluation Criteria

Your design will be evaluated on these criteria (you can self-assess or ask an AI to review):

| Criterion | Description | Weight |
|-----------|-------------|--------|
| **Trade-off awareness** | Does every significant decision acknowledge its costs? | 25% |
| **Completeness** | Are all required deliverables present and populated? | 20% |
| **Consistency** | Do the deliverables agree with each other? (Services in diagram match services in SERVICES.md) | 20% |
| **ADR quality** | Do ADRs show genuine consideration of alternatives? | 20% |
| **Failure mode realism** | Are failure modes specific to the system, or generic? | 15% |

---

## Getting Unstuck

If you get stuck, use these staged hints. Try each stage before moving to the next — the work has to be yours.

<details>
<summary>Stage 1: I don't know how to start the decomposition</summary>

Start with the nouns in the requirements, not with services. For Option A (e-commerce): Product, Order, Cart, User, Payment, Seller, Inventory, Notification, Media. Group nouns that belong together by *business ownership* — which team would own "Cart" vs. "Order"? Each group becomes a bounded context candidate.

</details>

<details>
<summary>Stage 2: I can't decide on sync vs. async for a specific flow</summary>

Ask two questions:
1. Does the caller need the result immediately to continue? → Sync
2. Can the caller proceed without knowing the outcome right now? → Async

For checkout: inventory check = sync (can't proceed without knowing stock); confirmation email = async (user doesn't wait for email to be sent). When in doubt, start sync and migrate to async when scale demands it.

</details>

<details>
<summary>Stage 3: I'm not sure how to handle distributed consistency in my use case</summary>

Look at which flows span multiple services:
- Does a single user action update data in 2+ services? → Potential dual-write problem → Consider Outbox or Saga
- Is eventual consistency acceptable for this specific flow? → Yes for notifications, ratings, activity feeds; No for financial transactions, inventory reservations
- Map out the "what if X fails mid-flow" for your 3 most critical flows

Review Module 06 for the patterns, then decide.

</details>

<details>
<summary>Stage 4: My ADRs feel shallow — I don't have enough alternatives to consider</summary>

For each decision, ask "what would a reasonable senior engineer who disagrees with me propose instead?" Common alternatives for common decisions:
- Sync vs. async: consider both always
- Kafka vs. RabbitMQ vs. cloud-native (SQS/Pub-Sub): consider 3
- Saga style: choreography vs. orchestration — always consider both
- Sharding strategy: range vs. hash vs. don't shard yet
- Service boundary: "should X be its own service or part of Y service?" — justify both directions

</details>

<details>
<summary>Stage 5: I don't know what failure modes to document</summary>

For your specific use case, think through:
1. What is the most critical user flow? What happens if each dependency in that flow fails?
2. What external dependencies does your system have? (Payment processor, email provider, CDN) — what if they're down?
3. What happens if your message broker is unavailable for 5 minutes? For 1 hour?
4. What happens if one service's database is slow (not down, but 10x slower than normal)?
5. What is the "catastrophic data loss" scenario — and how do you detect and recover from it?

</details>

---

## Cross-Links

- [[systems-architecture/modules/01_introduction]] — CAP theorem and monolith/microservices trade-offs apply to your decomposition decisions
- [[systems-architecture/modules/03_async-patterns]] — Saga and Outbox patterns for your consistency-critical flows
- [[systems-architecture/modules/04_microservices-fundamentals]] — Bounded context analysis for your service decomposition
- [[systems-architecture/modules/05_microservices-patterns]] — Circuit breaker and bulkhead for your resilience plan
- [[systems-architecture/modules/06_data-consistency]] — Distributed consistency strategy for multi-service data flows
- [[systems-architecture/modules/08_observability-distributed]] — Observability strategy (optional bonus deliverable)
- [[systems-architecture/modules/11_architecture-decision-making]] — ADR format and trade-off analysis framework
