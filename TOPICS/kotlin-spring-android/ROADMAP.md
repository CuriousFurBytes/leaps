# Roadmap: Kotlin — Backend Web, Spring Boot, and Android Development

> A phased learning path from zero to expert across the full Kotlin ecosystem.

---

## Table of Contents

- [Phase 1: Kotlin Language Foundations](#phase-1-kotlin-language-foundations)
- [Phase 2: Spring Boot Backend](#phase-2-spring-boot-backend)
- [Phase 3: Android Development](#phase-3-android-development)
- [Phase 4: Expert and Cross-Platform](#phase-4-expert-and-cross-platform)
- [How This Topic Fits Broader Learning](#how-this-topic-fits-broader-learning)

---

## Phase 1: Kotlin Language Foundations

**Modules:** 01–03  
**Duration:** ~25 hours  
**Goal:** Become fluent in Kotlin as a language — independent of any framework or platform.

By the end of Phase 1 you will write idiomatic Kotlin: null-safe code, data classes, sealed class hierarchies, coroutines, extension functions, and DSLs. You will understand why Kotlin exists, how it compares to Java, and how the JVM executes it.

| Module | Focus |
|--------|-------|
| 01 Introduction | Why Kotlin, null safety, basic syntax, first programs |
| 02 Kotlin Fundamentals | OOP, collections, sealed classes, generics |
| 03 Kotlin Advanced | Coroutines, extension functions, DSL building, delegation |

**Milestone:** Pass all Phase 1 tests with ≥70%. Write a small command-line tool in pure Kotlin before moving to Phase 2.

---

## Phase 2: Spring Boot Backend

**Modules:** 04–08  
**Duration:** ~35 hours  
**Goal:** Build production-ready Spring Boot backend services in Kotlin.

Phase 2 takes the Kotlin fluency from Phase 1 and applies it to the Spring Boot ecosystem: REST APIs, database access, authentication, advanced patterns, and Gradle build configuration.

| Module | Focus |
|--------|-------|
| 04 Spring Boot Fundamentals | IoC/DI, REST controllers, auto-configuration |
| 05 Spring Data and Persistence | JPA, repositories, transactions, PostgreSQL |
| 06 Spring Security | JWT, OAuth2, method-level security |
| 07 Spring Advanced | Actuator, caching, Kafka, WebFlux |
| 08 Gradle and Build Tooling | Kotlin DSL, multi-module projects |

**Milestone:** Deploy a functioning REST API to a local Docker container. It must authenticate with JWT, query a real PostgreSQL database, and have passing integration tests.

---

## Phase 3: Android Development

**Modules:** 09–10  
**Duration:** ~25 hours  
**Goal:** Build modern Android apps using Jetpack Compose, Hilt, Room, and Retrofit.

Phase 3 applies Kotlin knowledge to Android. The Kotlin language skills from Phase 1 transfer directly; coroutines (Module 03) and the dependency injection concepts from Module 04 reappear in an Android context.

| Module | Focus |
|--------|-------|
| 09 Android Fundamentals | Jetpack Compose, Navigation, Activities, lifecycle |
| 10 Android Advanced | ViewModel, StateFlow, Room, Retrofit, Hilt, Material3 |

**Milestone:** Build and install a working Android app on a real device or emulator that fetches data from the REST API built in Phase 2.

---

## Phase 4: Expert and Cross-Platform

**Modules:** 11–12  
**Duration:** ~20 hours  
**Goal:** Master testing, and synthesize all skills in a full-stack capstone project.

Phase 4 closes the loop: comprehensive testing (Module 11) followed by the Capstone (Module 12), where everything comes together: a Spring Boot API, an Android client, and a shared Kotlin Multiplatform library.

| Module | Focus |
|--------|-------|
| 11 Testing in Kotlin | JUnit5, Mockk, Spring slices, TestContainers, Espresso |
| 12 Capstone Project | Full-stack project: Spring Boot API + Android app + KMP shared library |

**Milestone:** A working, tested, documented, full-stack Kotlin project on GitHub.

---

## How This Topic Fits Broader Learning

This topic assumes basic programming knowledge and optional Java exposure. It connects to:

- **[[postgresql]]** — used in Module 05 for real database persistence; deep understanding of PostgreSQL improves your Spring Data work
- **[[graphql-rest]]** — REST design principles used across Modules 04–07; GraphQL is an optional extension of your API design skills
- **[[qa-testing]]** — general testing philosophy that Module 11 applies concretely to Kotlin
- **[[go]]** — after mastering Kotlin, Go is a natural complement for learning a simpler compiled language used in infrastructure

After completing this topic, natural progressions are:

- **DevOps / Platform Engineering** — deploy your Spring Boot apps with Docker, Kubernetes, and CI/CD
- **Microservices Architecture** — extend Module 07's Kafka integration into a full event-driven architecture
- **Kotlin Multiplatform (advanced)** — extend Module 12's KMP foundation into iOS and desktop targets
