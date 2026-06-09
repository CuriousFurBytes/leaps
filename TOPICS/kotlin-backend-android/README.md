# Kotlin Backend and Android

> A zero-to-expert path for building Kotlin Spring web backends, Android apps, and Maven or Gradle build systems that connect them.

## Table of Contents
1. [Why Learn Kotlin Backend and Android?](#why-learn-kotlin-backend-and-android)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn Kotlin Backend and Android?

Kotlin is unusual because it is both a modern application language and a pragmatic bridge into the existing JVM ecosystem. On the backend, Kotlin can use mature Java libraries, Spring Boot infrastructure, Maven repositories, and production observability tools. On Android, Kotlin is the primary language for app development, UI state, platform APIs, and asynchronous work.

This topic matters when you want one language to span server APIs, mobile clients, shared domain models, and build automation. The learner begins at ground zero: what Kotlin is, why the JVM still matters, how Android differs from a server process, and why build tools are part of professional software engineering rather than incidental setup.

The expert end of the path is not just syntax familiarity. It includes designing stable HTTP contracts, choosing Gradle or Maven intentionally, testing across service and app boundaries, shipping Android releases, operating Spring services, and debugging failure modes that appear only under real users and real traffic.

## Prerequisites

- Basic command-line comfort: opening a terminal, editing files, and running commands.
- General programming familiarity from programming is helpful but not assumed deeply.
- Basic web concepts from web development help with HTTP, JSON, and APIs.
- Basic database ideas from databases help later persistence modules.

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Orientation and Tooling](./modules/01_orientation_and_tooling/) | Beginner | [ ] |
| 02 | [Kotlin Language for Services](./modules/02_kotlin_language_for_services/) | Beginner | [ ] |
| 03 | [Build Systems and Project Structure](./modules/03_build_systems_and_project_structure/) | Intermediate | [ ] |
| 04 | Spring Boot Fundamentals | Intermediate | [ ] |
| 05 | Persistence and Transactions | Intermediate | [ ] |
| 06 | HTTP APIs and Security | Advanced | [ ] |
| 07 | Android App Architecture | Advanced | [ ] |
| 08 | Networking Between Android and Backend | Advanced | [ ] |
| 09 | Testing Strategy Across the Stack | Advanced | [ ] |
| 10 | Deployment, CI, and Release Engineering | Expert | [ ] |
| 11 | Performance, Reliability, and Operations | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/) | Expert | [ ] |

## Cross-Links

- [[kotlin-backend-android#module-map]] — the complete zero-to-expert sequence for this topic.
- [[kotlin-backend-android#quick-reference]] — build commands used throughout the path.
- [[kotlin-backend-android#why-learn-kotlin-backend-and-android]] — motivation for spanning backend and Android in one Kotlin learning arc.

Related areas to study as separate topics when they are available: Java, Spring, Android, software testing, databases, and DevOps.

## Quick Reference

| Task | Gradle | Maven |
|---|---|---|
| Run tests | `./gradlew test` | `mvn test` |
| Build artifact | `./gradlew build` | `mvn package` |
| Run Spring app | `./gradlew bootRun` | `mvn spring-boot:run` |
| Inspect dependencies | `./gradlew dependencies` | `mvn dependency:tree` |

```kotlin
// Minimal Kotlin entry point: compile with Kotlin tooling or run in an IDE.
fun main() {
    val serviceName = "learning-api" // Immutable local value.
    println("Starting $serviceName with Kotlin")
}
```
