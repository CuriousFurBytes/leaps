# Kotlin — Backend Web, Spring Boot, and Android Development

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)
![Language](https://img.shields.io/badge/language-Kotlin-7F52FF?logo=kotlin&logoColor=white)

> A pragmatic, statically typed JVM language that powers Android development, Spring Boot backends, and cross-platform Kotlin Multiplatform projects.

> [!NOTE]
> **Topic Overview**
> Kotlin is a modern, concise language created by JetBrains that compiles to JVM bytecode, JavaScript, or native code. It achieved first-class Android support at Google I/O 2017, made Gradle build scripts dramatically more expressive through the Kotlin DSL, and is the preferred language for new Spring Boot applications. This topic covers Kotlin from first principles through expert-level backend and Android development.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty and Time Estimate](#difficulty-and-time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty and Time Estimate](#difficulty-and-time-estimate)
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

Kotlin is a statically typed, object-oriented and functional programming language developed by JetBrains, the company behind IntelliJ IDEA. Released as a stable 1.0 in February 2016, Kotlin was designed from the ground up to be a more pragmatic, expressive, and safer alternative to Java while maintaining 100% interoperability with existing Java code and the entire JVM ecosystem.

The language achieves a rare balance: it is more concise than Java (typical Kotlin programs are 40% shorter), safer by default (null safety is baked into the type system), and yet compiles to the same bytecode the JVM executes. You can call any Java library from Kotlin and vice versa, making adoption gradual and risk-free. In practice, most Kotlin projects start as Java projects — developers introduce Kotlin file by file.

### Why It Matters

Kotlin matters because it sits at the intersection of three massive ecosystems:

- **Android development** — Google declared Kotlin the preferred language for Android in 2019. The Android Jetpack libraries, Jetpack Compose UI framework, and all modern Android documentation are Kotlin-first. A Java-only Android developer is increasingly working against the grain.
- **Spring Boot backend development** — The Spring Framework's Kotlin extensions, coroutine integration, and DSL support make Spring Boot + Kotlin a compelling, production-proven combination used by fintechs, startups, and enterprises across Europe and beyond.
- **Kotlin Multiplatform** — Since 2022, Kotlin Multiplatform (KMP) allows sharing business logic, data models, and networking code across Android, iOS, desktop, and server — a genuine cross-platform strategy backed by JetBrains and adopted by companies such as Netflix and McDonald's.

### Key Features of This Topic

- **Null Safety by Design** — Kotlin's type system distinguishes nullable (`String?`) from non-nullable (`String`) at compile time, eliminating NullPointerExceptions by construction
- **Coroutines for Concurrency** — Kotlin's coroutines model provides structured, readable asynchronous code that replaces callbacks, RxJava chains, and thread pools with `suspend` functions and `Flow`
- **Spring Integration** — Full coverage of Spring Boot with Kotlin: controllers, services, JPA entities, security, WebFlux, and testing
- **Android with Jetpack Compose** — Modern declarative Android UI, navigation, ViewModel, Room, Retrofit, and Hilt dependency injection

---

## Historical Context

Kotlin's origins trace back to Java's evolution — or lack thereof. Sun Microsystems created Java in 1995 as a "write once, run anywhere" language for a world of heterogeneous devices. Java dominated enterprise development for two decades, but its verbosity, lack of null safety, and slow evolution frustrated practitioners. Groovy (2003) and Scala (2004) emerged as JVM alternatives — Groovy for scripting and DSLs, Scala for functional programming — but neither achieved Java's adoption.

JetBrains, whose engineers wrote millions of lines of Java building their IDE products, needed a better language for large-scale JVM development. In 2010, JetBrains began Project Kotlin, led by **Andrey Breslav** as lead language designer. The goals were precise: 100% Java interoperability, compile time on par with Java (not Scala's minutes-long builds), pragmatic OOP rather than Scala's full type-theory-driven design, and null safety as a first-class property.

Spring Boot, created by Pivotal (now VMware/Broadcom), launched in 2014 to simplify Java's notoriously verbose Spring Framework configuration. Its auto-configuration, embedded servers, and "opinionated defaults" model made it the dominant Java web framework within a few years.

### Timeline

| Year | Event |
|------|-------|
| 2010 | JetBrains begins Project Kotlin; Andrey Breslav leads design |
| 2012 | Kotlin first open-sourced on GitHub |
| 2014 | Spring Boot 1.0 released by Pivotal |
| 2016 | Kotlin 1.0 stable release; JetBrains commits to long-term support |
| 2017 | Google I/O: Kotlin announced as first-class Android language |
| 2018 | Kotlin 1.3: coroutines become stable |
| 2019 | Google declares Kotlin the preferred language for Android development |
| 2020 | Kotlin 1.4: improved type inference, new IR compiler backend |
| 2021 | Kotlin 1.5: JVM records, sealed interfaces, stdlib additions |
| 2022 | Kotlin Multiplatform Mobile (KMM) reaches Alpha; Jetpack Compose 1.0 stable |
| 2023 | Kotlin 1.9; K2 compiler enters Beta; Kotlin Multiplatform becomes Stable |
| 2024 | Kotlin 2.0 released with K2 compiler stable; significant performance improvements |
| Today | Actively developed; one of the fastest-growing languages on the JVM |

---

## Real-World Applications

Kotlin is actively used across many domains:

- **Android Mobile** — Pinterest rewrote its Android app in Kotlin; virtually all new Android apps use Kotlin and Jetpack Compose
- **Backend Fintech** — European fintechs such as N26, Monzo (partial), and numerous Dutch and Scandinavian startups run Spring Boot + Kotlin microservices in production
- **Build Tooling** — Gradle migrated its recommended build script format from Groovy to Kotlin DSL; the entire Android Gradle plugin documentation uses Kotlin DSL
- **Cross-Platform Sharing** — Netflix uses Kotlin Multiplatform to share business logic between Android and iOS; McDonald's uses KMP for their ordering app
- **Backend Payments** — Square/Block adopted Kotlin for their server-side systems, cited in their engineering blog as improving safety and code quality
- **Data Pipelines** — Apache Spark's Kotlin API allows writing Spark jobs in idiomatic Kotlin instead of Java or Scala

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Write idiomatic Kotlin using null safety, data classes, sealed classes, coroutines, extension functions, and DSLs
2. Build production-ready REST APIs with Spring Boot, Spring Data JPA, and Spring Security using Kotlin
3. Design and implement Android applications with Jetpack Compose, ViewModel, Room, Retrofit, and Hilt
4. Configure multi-module Gradle projects using the Kotlin DSL and manage dependency versions with version catalogs
5. Write comprehensive test suites using JUnit 5, Mockk, Spring test slices, TestContainers, and Espresso
6. Apply structured concurrency with Kotlin coroutines, `Flow`, and `StateFlow` across both Android and backend contexts
7. Architect a full-stack Kotlin project — a Spring Boot API plus an Android client — sharing a Kotlin Multiplatform model library
8. Debug, profile, and optimize Kotlin JVM applications using IntelliJ IDEA's profiler, bytecode viewer, and coroutine debugger

---

## Difficulty and Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Intermediate → Expert |
| **Estimated Total Hours** | 80–120 hours |
| **Prerequisites** | Basic programming knowledge; OOP concepts in any language; Java exposure is a plus |
| **Recommended Pace** | 5–8 hours/week |
| **Topic Type** | Practical (code-heavy) |
| **Suitable For** | Backend engineers, Android developers, full-stack engineers transitioning from Java |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- Basic programming concepts (variables, loops, conditionals, functions) in any language
- Object-oriented programming concepts (classes, objects, inheritance, interfaces) — even beginner-level exposure helps
- Basic command-line usage (navigating directories, running commands)

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If basic programming concepts feel foreign, spend a week with any introductory course first.
> If you already know Java, Module 01 will move very quickly for you — feel free to skim the Java comparisons.

Related prerequisite topics in this repository:

- [[postgresql]] — used in Modules 05 and 12
- [[graphql-rest]] — REST API design concepts applied in Modules 04 and 12
- [[qa-testing]] — testing principles that Module 11 applies to the Kotlin/JVM ecosystem

---

## Learning Modules

| # | Module | Topic | Difficulty | Status | Score |
|---|--------|-------|-----------|--------|-------|
| 01 | [Introduction to Kotlin](./modules/01_introduction/) | Why Kotlin, environment setup, null safety, basic syntax | Beginner | - [ ] | —/— |
| 02 | [Kotlin Fundamentals](./modules/02_kotlin-fundamentals/) | OOP, sealed classes, data classes, collections, generics | Beginner–Intermediate | - [ ] | —/— |
| 03 | [Kotlin Advanced](./modules/03_kotlin-advanced/) | Coroutines, extension functions, DSL building, delegation | Intermediate | - [ ] | —/— |
| 04 | [Spring Boot Fundamentals](./modules/04_spring-boot-fundamentals/) | Auto-configuration, IoC/DI, REST controllers, request mapping | Intermediate | - [ ] | —/— |
| 05 | [Spring Data and Persistence](./modules/05_spring-data-and-persistence/) | Spring Data JPA, Kotlin entities, repositories, transactions | Intermediate | - [ ] | —/— |
| 06 | [Spring Security](./modules/06_spring-security/) | Authentication, JWT, OAuth2, method-level security, CORS | Advanced | - [ ] | —/— |
| 07 | [Spring Advanced](./modules/07_spring-advanced/) | Actuator, caching, Kafka, WebFlux, scheduled tasks | Advanced | - [ ] | —/— |
| 08 | [Gradle and Build Tooling](./modules/08_gradle-and-build/) | Kotlin DSL, multi-module builds, custom tasks, plugin ecosystem | Advanced | - [ ] | —/— |
| 09 | [Android Fundamentals](./modules/09_android-fundamentals/) | Architecture, Activities, Jetpack Compose, Navigation, lifecycle | Intermediate | - [ ] | —/— |
| 10 | [Android Advanced](./modules/10_android-advanced/) | ViewModel, StateFlow, Room, Retrofit, Hilt, Material3 | Advanced | - [ ] | —/— |
| 11 | [Testing in Kotlin](./modules/11_testing-kotlin/) | JUnit5, Mockk, Spring test slices, TestContainers, Espresso | Advanced | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Full-stack Spring Boot API + Android app + KMP shared library | Expert | - [ ] | —/— |

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
Example: [████████▒░░░░░░░░░░░] 4.5 / 12 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 60 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **624** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to Kotlin)
- [ ] **JVM Fluency** — Complete Modules 01–03 with ≥70% on each test
- [ ] **Backend Ready** — Complete Module 04 and build a working REST API
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Full-Stack Kotlin** — Complete Modules 04–07 (backend) and 09–10 (Android)
- [ ] **Testing Champion** — Complete Module 11 with ≥80%
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Kotlin Master** — Average test score ≥90% across all modules
- [ ] **Project Builder** — Complete the Capstone Project in Module 12

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

**Top picks:**

1. "Kotlin in Action" by Dmitry Jemerov and Svetlana Isakova (Manning) — canonical Kotlin reference
2. [Kotlin Official Documentation](https://kotlinlang.org/docs/home.html) — comprehensive and well-maintained
3. [Spring Boot + Kotlin Guide](https://spring.io/guides/tutorials/spring-boot-kotlin/) — official Spring tutorial

---

## Related Topics

Topics that complement, extend, or are required for this topic:

- [[graphql-rest]] — REST API design principles applied throughout the Spring Boot modules
- [[postgresql]] — Database used in Modules 05 and 12; Spring Data JPA sits on top of it
- [[qa-testing]] — General testing philosophy that Module 11 applies to the Kotlin/JVM ecosystem
- [[go]] — Another pragmatic compiled language; useful comparison for understanding JVM trade-offs
- [[javascript-typescript-react]] — TypeScript's null safety and type system share conceptual roots with Kotlin's

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Topic Created

**What was set up:**
- Topic structure created with 12 modules spanning Kotlin fundamentals through capstone
- Module 01 fully written; Modules 02–12 stubbed

**First open question:**
- See [QUESTIONS.md](./QUESTIONS.md)

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "kotlin-spring-android"
topic_name: "Kotlin — Backend Web, Spring Boot, and Android Development"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 624
completion_percentage: 0
difficulty: "Intermediate → Expert"
estimated_hours: 100
prerequisites:
  - "basic-programming"
  - "oop-concepts"
related_topics:
  - "graphql-rest"
  - "postgresql"
  - "qa-testing"
  - "go"
tags:
  - "kotlin"
  - "spring-boot"
  - "android"
  - "jvm"
  - "backend"
  - "mobile"
creator: "JetBrains"
year_created: "2011"
```
