# Projects: Kotlin — Backend Web, Spring Boot, and Android Development

> Project ideas ranging from beginner to expert. Build real things — not toy examples.
> Each project integrates multiple modules and produces a deployable artifact.

---

## Table of Contents

- [Beginner Projects (Modules 01–02)](#beginner-projects-modules-0102)
- [Intermediate Projects (Modules 03–05)](#intermediate-projects-modules-0305)
- [Advanced Projects (Modules 06–10)](#advanced-projects-modules-0610)
- [Expert Projects (Modules 11–12)](#expert-projects-modules-1112)

---

## Beginner Projects (Modules 01–02)

### Project 1: Command-Line Task Manager

**Description:** A command-line to-do list app that stores tasks in a JSON file. Users can add, list, complete, and delete tasks.

**Skills required:** Kotlin basics (Module 01), data classes, sealed classes, file I/O (Module 02)

**Acceptance criteria:**
- `./tasks add "Buy groceries"` appends a task
- `./tasks list` prints all tasks with status
- `./tasks done 1` marks task #1 complete
- Tasks persist between runs (JSON file)
- Proper error handling when task ID doesn't exist

**Extension ideas:** Add due dates, priorities, or filtering by status.

---

### Project 2: Currency Converter CLI

**Description:** A command-line tool that converts between currencies using hardcoded exchange rates (no external API needed). Demonstrates Kotlin data classes, operator overloading, and string templates.

**Skills required:** Kotlin basics (Module 01), data classes (Module 02)

**Acceptance criteria:**
- Define a `Money(amount: BigDecimal, currency: Currency)` data class
- Support `+`, `-`, and conversion between at least 5 currencies
- Clean output with proper decimal formatting
- Handles invalid currency codes gracefully

---

## Intermediate Projects (Modules 03–05)

### Project 3: Async File Processor

**Description:** A command-line tool that processes a directory of CSV files concurrently using coroutines. Computes statistics (sum, average, min, max) per column and outputs a summary report.

**Skills required:** Kotlin coroutines (Module 03), file I/O, extension functions

**Acceptance criteria:**
- Process each file in a separate coroutine using `async`/`await`
- Combine results without blocking threads
- Handle malformed CSV rows gracefully
- Demonstrate measurable concurrency speedup vs sequential processing

---

### Project 4: Product Catalog REST API

**Description:** A Spring Boot REST API for managing a product catalog. Supports CRUD operations on products and categories.

**Skills required:** Spring Boot (Module 04), Spring Data JPA + PostgreSQL (Module 05)

**Acceptance criteria:**
- `GET /products` returns paginated list
- `POST /products` creates a product
- `GET /products/{id}` returns a single product
- `PUT /products/{id}` updates a product
- `DELETE /products/{id}` soft-deletes a product
- Products belong to categories; `GET /categories/{id}/products` works
- Uses Spring Data JPA with a real PostgreSQL database

---

## Advanced Projects (Modules 06–10)

### Project 5: Authenticated Note-Taking API

**Description:** A REST API for personal notes with JWT authentication. Each user has their own notes; no user can see another user's notes.

**Skills required:** Spring Boot (Module 04), Spring Data (Module 05), Spring Security + JWT (Module 06)

**Acceptance criteria:**
- `POST /auth/register` creates an account
- `POST /auth/login` returns a JWT
- All `/notes` endpoints require a valid JWT
- Notes are scoped to the authenticated user
- Refresh token mechanism (access token expires in 15 minutes)
- Comprehensive integration tests

---

### Project 6: Android Weather App

**Description:** An Android app that shows current weather for the user's location and allows searching by city name. Uses a free weather API (such as Open-Meteo, which requires no API key).

**Skills required:** Android fundamentals (Module 09), Android advanced — Retrofit, ViewModel, StateFlow (Module 10)

**Acceptance criteria:**
- Jetpack Compose UI with Material3 design
- Location permission request handled correctly
- Current conditions and 7-day forecast
- City search with debouncing
- Offline cache (show last known data when no network)
- Handle loading, success, and error states with proper UI feedback

---

## Expert Projects (Modules 11–12)

### Project 7: Event-Driven Order Processing System

**Description:** A distributed order processing system using Spring Boot microservices and Kafka. Service A accepts orders via REST; Service B processes payments via Kafka events; Service C sends confirmation emails (simulated).

**Skills required:** Spring Boot (Module 04), Spring Data (Module 05), Spring Advanced — Kafka (Module 07), Testing (Module 11)

**Acceptance criteria:**
- Three Spring Boot services communicating via Kafka topics
- Eventual consistency: order transitions through PENDING → PAID → CONFIRMED states
- At-least-once delivery with idempotent consumers
- TestContainers-based integration tests for Kafka flows
- Actuator health endpoints on all services
- Docker Compose file to run the full system locally

---

### Project 8: Full-Stack Kotlin App (Capstone Preview)

**Description:** A Spring Boot backend API + Android app that share a Kotlin Multiplatform model library. See Module 12 (Capstone) for the full specification.

**Skills required:** All modules

This project is the Module 12 capstone. See [modules/12_capstone-project/README.md](./modules/12_capstone-project/README.md) for the full brief.

---

## My Projects

_Track your own projects here. Append rows; never delete._

| Project | Started | Completed | Score | Notes |
|---------|---------|-----------|-------|-------|
| — | — | — | — | — |
