# Module 12: Capstone Project

[← Module 11: Testing in Kotlin](../11_testing-kotlin/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-red)
![Time](https://img.shields.io/badge/time-20h-orange)

> Build a full-stack Kotlin project: a Spring Boot REST API, an Android app, and a shared Kotlin Multiplatform model library — all tested and documented.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Architecture](#architecture)
5. [Milestones](#milestones)
6. [Acceptance Criteria](#acceptance-criteria)
7. [Getting Unstuck](#getting-unstuck)
8. [Submission and Review](#submission-and-review)
9. [Cross-Links](#cross-links)

---

## Overview

This is the capstone module. You will not be reading theory here — you will be building a real, non-trivial application that synthesizes everything from Modules 01–11.

The project is a **personal bookmark manager**: users can save URLs with titles, tags, and notes; the Android app provides the mobile interface; the Spring Boot API provides the backend with persistence; a shared Kotlin Multiplatform library contains the domain models and validation logic used by both.

> [!IMPORTANT]
> **Do not look for a complete solution.** The help sections below provide staged hints, architecture suggestions, and links back to relevant modules — but they are designed for a stuck learner to move forward on their own, not to hand you the answer. A capstone you built yourself is worth infinitely more than one you copy-pasted.
>
> If you're stuck, read the relevant help section, try to implement it, and come back to the next hint only if you're still blocked after a genuine attempt.

---

## Prerequisites

All 11 prior modules, with particular emphasis on:
- Module 03 (Kotlin coroutines)
- Module 04–07 (Spring Boot)
- Module 08 (Gradle multi-module)
- Module 09–10 (Android)
- Module 11 (Testing)

---

## Project Brief

**Application: KotlinMark — Personal Bookmark Manager**

Build a system with three components:

### Component 1: `shared` — Kotlin Multiplatform Library
A KMP module (targets JVM and Android) containing:
- Domain models: `Bookmark`, `Tag`, `User`
- Validation logic: URL validation, title length limits, tag name rules
- Serialization-ready data classes (with kotlinx.serialization)

### Component 2: `backend` — Spring Boot REST API
A Spring Boot application that:
- Exposes a REST API for bookmarks CRUD
- Requires JWT authentication
- Persists data to PostgreSQL (via Spring Data JPA)
- Uses the `shared` KMP library's domain models
- Has comprehensive tests (unit + integration with TestContainers)
- Exposes Actuator health endpoint

### Component 3: `android` — Android App
An Android app that:
- Uses Jetpack Compose for UI with Material3 design
- Authenticates against the backend API (login screen → JWT stored securely)
- Lists, creates, updates, and deletes bookmarks
- Supports offline mode: shows cached bookmarks when offline (Room)
- Uses the `shared` KMP library's models
- Has at least 5 meaningful UI test cases

---

## Architecture

```
kotlin-mark/
├── settings.gradle.kts          ← includes all three subprojects
├── gradle/
│   └── libs.versions.toml       ← shared dependency versions
├── shared/
│   ├── build.gradle.kts         ← kotlin("multiplatform") plugin
│   └── src/
│       ├── commonMain/kotlin/   ← domain models, validation
│       ├── jvmMain/kotlin/      ← JVM-specific implementations (optional)
│       └── androidMain/kotlin/  ← Android-specific implementations (optional)
├── backend/
│   ├── build.gradle.kts         ← Spring Boot + Kotlin + JPA
│   └── src/
│       ├── main/kotlin/
│       └── test/kotlin/
└── android/
    ├── build.gradle.kts         ← Android application plugin
    └── src/
        ├── main/kotlin/
        └── androidTest/kotlin/
```

---

## Milestones

Complete milestones in order. Each builds on the previous.

### Milestone 1: Project Setup and Shared Module

- [ ] Create the three-module Gradle project structure
- [ ] Configure the Kotlin Multiplatform plugin in the `shared` module
- [ ] Define `Bookmark`, `Tag`, and `User` data classes in `commonMain`
- [ ] Add validation functions for each domain model
- [ ] Write unit tests for all validators

**Done when:** `./gradlew :shared:test` passes.

---

### Milestone 2: Spring Boot API — Core

- [ ] Add the `shared` module as a dependency of `backend`
- [ ] Create JPA entities for Bookmark and User (note: JPA entities are not the same as domain models — you will need mappers)
- [ ] Implement CRUD endpoints for bookmarks: `GET /bookmarks`, `POST /bookmarks`, `GET /bookmarks/{id}`, `PUT /bookmarks/{id}`, `DELETE /bookmarks/{id}`
- [ ] Add JWT authentication: register, login, refresh
- [ ] Add pagination: `GET /bookmarks?page=0&size=20`

**Done when:** All endpoints respond correctly in Postman/curl, authenticated correctly.

---

### Milestone 3: Spring Boot API — Tests and Quality

- [ ] Add `@WebMvcTest` tests for all controller endpoints
- [ ] Add `@DataJpaTest` tests for repository queries
- [ ] Add TestContainers integration test for the full bookmark creation flow (create bookmark → retrieve it → verify stored correctly)
- [ ] Configure Actuator health endpoint
- [ ] Add `docker-compose.yml` to run the API + PostgreSQL locally with one command

**Done when:** `./gradlew :backend:test` passes; `docker-compose up` starts the working system.

---

### Milestone 4: Android App — Core

- [ ] Add the `shared` module as a dependency of `android`
- [ ] Implement authentication screens: Login and Register with proper error handling
- [ ] Implement bookmark list screen: `LazyColumn` with `BookmarkCard` composables
- [ ] Implement create/edit bookmark screen
- [ ] Wire Retrofit to call the Spring Boot API
- [ ] Store JWT securely (`EncryptedSharedPreferences`)

**Done when:** The Android app authenticates against the running backend and shows real bookmarks.

---

### Milestone 5: Android App — Offline and Tests

- [ ] Implement Room for local bookmark caching
- [ ] Implement offline-first: show Room data immediately, refresh from API in background, update Room on success
- [ ] Write 5 Compose UI tests using `createComposeRule()`
- [ ] Handle all error states gracefully: network errors, auth errors, empty state

**Done when:** The app shows bookmarks when offline. `./gradlew :android:connectedAndroidTest` passes (or passes on emulator).

---

### Milestone 6: Polish and Documentation

- [ ] README.md in the project root with setup instructions, architecture diagram, and screenshots
- [ ] All three modules build cleanly with no warnings
- [ ] Code is formatted with `ktlint` or `detekt`
- [ ] At least one non-trivial feature not in the brief (your choice: search, tags filter, share sheet, bookmark import from browser, etc.)

**Done when:** A colleague can clone the repo and get everything running by following the README alone.

---

## Acceptance Criteria

Your capstone is complete when:

- [ ] `./gradlew build` passes for all three modules
- [ ] The backend API has ≥70% test coverage (JaCoCo)
- [ ] All TestContainers tests pass
- [ ] The Android app runs on a real device or emulator, connected to the backend
- [ ] The shared module compiles for both JVM and Android targets
- [ ] The project README documents architecture, setup, and design decisions

---

## Getting Unstuck

<details>
<summary>Hint: KMP module setup is failing</summary>

The Kotlin Multiplatform plugin requires the `kotlin("multiplatform")` plugin (not `kotlin("jvm")`). Your `shared/build.gradle.kts` should look like:

```kotlin
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
}

kotlin {
    jvm()
    androidTarget()

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
            }
        }
        val jvmMain by getting
        val androidMain by getting
    }
}
```

See Module 08 for Gradle Kotlin DSL patterns.
</details>

<details>
<summary>Hint: JPA entities vs KMP domain models</summary>

You cannot use KMP `data class` directly as a JPA entity because:
1. JPA requires no-args constructors on mutable fields
2. KMP `commonMain` code cannot use JPA annotations (they're JVM-only)

The solution is a mapper pattern:
- `shared/commonMain` has `Bookmark(val id: UUID, val url: String, val title: String)` — pure domain model
- `backend` has `BookmarkEntity(@Entity class BookmarkEntity(...))` — JPA entity
- A mapper function converts between them: `fun Bookmark.toEntity(): BookmarkEntity` and `fun BookmarkEntity.toDomain(): Bookmark`

See Module 05 for JPA entity patterns.
</details>

<details>
<summary>Hint: JWT token storage on Android</summary>

Never store JWTs in SharedPreferences in plaintext — they can be extracted on rooted devices. Use `EncryptedSharedPreferences` from the Security library:

```kotlin
val masterKey = MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
val prefs = EncryptedSharedPreferences.create(
    context, "secure_prefs", masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
prefs.edit().putString("access_token", token).apply()
```

See Module 10 for Android security patterns.
</details>

<details>
<summary>Hint: Offline-first with Room + Retrofit</summary>

The standard pattern for offline-first in Android:

```kotlin
fun getBookmarks(): Flow<List<Bookmark>> = flow {
    // Step 1: emit cached data from Room immediately
    emitAll(bookmarkDao.observeAll().map { entities -> entities.map { it.toDomain() } })
}.also {
    // Step 2: fetch from network in parallel and update Room
    viewModelScope.launch {
        try {
            val fresh = api.getBookmarks()
            bookmarkDao.upsertAll(fresh.map { it.toEntity() })
            // Room Flow will automatically emit the updated data
        } catch (e: Exception) {
            // Network failed — cached data is already showing; log and continue
        }
    }
}
```

See Module 10 for the full offline-first pattern.
</details>

<details>
<summary>Hint: TestContainers PostgreSQL configuration</summary>

Use `@DynamicPropertySource` to point Spring Boot at the TestContainers database:

```kotlin
companion object {
    @Container @JvmStatic
    val postgres = PostgreSQLContainer<Nothing>("postgres:16-alpine").apply {
        withDatabaseName("kotlinmark_test")
    }

    @DynamicPropertySource @JvmStatic
    fun props(registry: DynamicPropertyRegistry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl)
        registry.add("spring.datasource.username", postgres::getUsername)
        registry.add("spring.datasource.password", postgres::getPassword)
        registry.add("spring.jpa.hibernate.ddl-auto") { "create-drop" }
    }
}
```

See Module 11 for TestContainers patterns.
</details>

---

## Submission and Review

When you complete the capstone:

1. Push your code to a GitHub repository (public or private)
2. Update `TOPICS/kotlin-spring-android/PROGRESS.md` with your project link
3. Append a journal entry to `TOPICS/kotlin-spring-android/README.md` with what you built and what you learned
4. Ask for a code review by creating a question in `QUESTIONS.md` with a link to your repo

---

## Cross-Links

- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Coroutines used throughout
- [[kotlin-spring-android/modules/04_spring-boot-fundamentals]] — API architecture
- [[kotlin-spring-android/modules/05_spring-data-and-persistence]] — JPA entities and repositories
- [[kotlin-spring-android/modules/06_spring-security]] — JWT authentication
- [[kotlin-spring-android/modules/08_gradle-and-build]] — Multi-module Gradle structure
- [[kotlin-spring-android/modules/09_android-fundamentals]] — Compose UI
- [[kotlin-spring-android/modules/10_android-advanced]] — ViewModel, Room, Retrofit, Hilt
- [[kotlin-spring-android/modules/11_testing-kotlin]] — Tests across all three modules
- [[postgresql]] — PostgreSQL used in the backend
