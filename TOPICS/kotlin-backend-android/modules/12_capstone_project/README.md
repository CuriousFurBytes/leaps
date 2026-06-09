# Module 12: Capstone Project

> Build a production-shaped Kotlin learning system with a Spring backend, Android client, shared contract, tests, and repeatable builds.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Project Brief](#project-brief)
5. [Milestones](#milestones)
6. [Help and Getting Unstuck](#help-and-getting-unstuck)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

The capstone asks you to synthesize the whole topic. You will build a small but realistic system: a Spring Boot API for tracking learning tasks, an Android app for creating and completing tasks, and a build setup that makes testing and delivery repeatable.

This is intentionally build-oriented. The module gives architecture guidance, checkpoints, and hints, but it does not provide a complete copy-paste solution. The goal is to practice judgment: where contracts belong, what belongs in shared code, how clients handle backend failure, and how release tasks stay boring.

## Prerequisites

- Modules 01 through 11 in this topic.
- Working knowledge of Kotlin, Spring Boot, Android architecture, HTTP APIs, persistence, testing, and CI.

## Objectives

By the end of this module, you will be able to:
- Design and implement an end-to-end Kotlin backend plus Android application.
- Create a stable API contract and keep platform-specific code isolated.
- Test service logic, API boundaries, and Android state behavior.
- Explain operational tradeoffs in deployment, monitoring, and release management.

## Project Brief

Build **LeapTask**, a learning task tracker with these capabilities:

- A Spring Boot backend exposes tasks with title, notes, due date, status, and module tag.
- A persistence layer stores tasks and supports list, create, update, complete, and delete operations.
- An Android app displays tasks, creates new tasks, marks tasks complete, and handles offline or server errors clearly.
- Shared DTOs or generated contract types keep request and response shapes consistent.
- Gradle or Maven builds run tests from a clean checkout.

```kotlin
// Shared contract example: keep it free of Spring and Android imports.
data class TaskDto(
    val id: String,
    val title: String,
    val completed: Boolean
)
```

```kotlin
// Backend-shaped service decision: validate before persistence.
fun requireTitle(title: String): String {
    return title.trim().takeIf { it.isNotEmpty() }
        ?: error("Task title is required")
}
```

```bash
# Your final repository should support one documented verification command.
./gradlew test
```

## Milestones

1. Define the API contract and error format.
2. Implement backend domain logic and persistence.
3. Add Spring HTTP endpoints with validation.
4. Build Android screens and state management.
5. Connect Android networking and error handling.
6. Add unit, integration, and UI-oriented tests.
7. Document how to build, test, run, and release.

## Help and Getting Unstuck

### Hint 1: Keep Contracts Small

Start with `TaskDto`, `CreateTaskRequest`, and `UpdateTaskRequest`. Add fields only when the UI and backend both need them.

### Hint 2: Slice the Backend

Implement domain validation before controllers. Then add persistence. Then add HTTP. This avoids debugging Spring wiring and business rules at the same time.

### Hint 3: Android State First

Make the Android UI work against a fake repository before connecting the network client. A fake repository makes loading, success, empty, and error states easy to test.

### Hint 4: Choose One Build Story

Gradle is the default recommendation because Android already requires it, but documenting a Maven backend alongside a Gradle Android app is acceptable if the commands are clear.

## Acceptance Criteria

- Backend exposes documented endpoints and returns structured errors.
- Android app supports the core user flow without crashing on network failure.
- Tests cover validation, API behavior, and at least one Android state transition.
- Build commands are documented and reproducible from a clean checkout.
- Final write-up explains tradeoffs, shortcuts, and what you would improve next.

## Cross-Links

- [[kotlin-backend-android#module-map]]
- [[kotlin-backend-android#quick-reference]]
- [[kotlin-backend-android#why-learn-kotlin-backend-and-android]]

Related future topic areas: Java, Spring, Android, Gradle, Maven, software testing, and DevOps.


## Summary

- The capstone is a synthesis project, not a lecture module.
- Shared contracts should stay platform-neutral.
- Backend implementation is easier when domain logic is tested before web wiring.
- Android reliability depends on explicit loading, empty, success, and error states.
- Production-quality work includes tests, build documentation, and operational reasoning.
