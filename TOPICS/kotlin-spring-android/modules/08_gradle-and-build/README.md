# Module 08: Gradle and Build Tooling

[← Module 07: Spring Advanced](../07_spring-advanced/) | [Topic Home](../../README.md) | [Next → Module 09: Android Fundamentals](../09_android-fundamentals/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-8h-orange)

> Gradle Kotlin DSL, multi-module project builds, custom tasks, dependency management with version catalogs, and the Kotlin plugin ecosystem.

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

Gradle is the dominant build tool in the Kotlin/JVM ecosystem and the only supported build tool for Android. Since Gradle 5.0 (2018), the Kotlin DSL has been the recommended way to write Gradle build scripts — replacing the Groovy DSL with type-safe, IDE-assisted Kotlin code.

Understanding Gradle is not optional at the senior level. You need to know how to structure a multi-module project, write custom tasks for automation, manage dependency versions at scale with version catalogs (`libs.versions.toml`), and optimize build performance with caching and parallel execution.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> The [Gradle Kotlin DSL documentation](https://docs.gradle.org/current/userguide/kotlin_dsl.html) is the reference while this module is being written.

---

## Prerequisites

- Modules 01–03: Kotlin language
- Basic understanding of what a build tool does (compile, test, package)
- Modules 04–07: Spring Boot (to understand what the build scripts configure)

---

## Objectives

By the end of this module, you will be able to:

1. Write complete `build.gradle.kts` files for Spring Boot and Android projects
2. Structure a multi-module Gradle project with shared configuration using `buildSrc` or convention plugins
3. Manage all dependency versions centrally using `libs.versions.toml` (version catalogs)
4. Write and register custom Gradle tasks
5. Configure Kotlin compiler options (JVM target, strict null checks, experimental features)
6. Understand and use Gradle's task graph, incremental builds, and build cache
7. Apply common Kotlin Gradle plugins: `kotlin("jvm")`, `kotlin("plugin.spring")`, `kotlin("plugin.jpa")`, `kotlin("multiplatform")`

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Gradle's Build Model
> Projects, tasks, dependencies, the task graph, incremental build, build cache.
>
> ### 4.2 Kotlin DSL vs Groovy DSL
> Type safety, IDE support, migration from Groovy, `build.gradle.kts` vs `build.gradle`.
>
> ### 4.3 Multi-Module Project Structure
> `settings.gradle.kts`, `includeBuild`, `buildSrc`, convention plugins, sharing common configuration.
>
> ### 4.4 Version Catalogs
> `libs.versions.toml`, TOML format, accessing via `libs.spring.boot`, IDE support.
>
> ### 4.5 Custom Tasks
> `tasks.register`, `doFirst`/`doLast`, task inputs/outputs, `@TaskAction`, incremental task support.
>
> ### 4.6 Kotlin Gradle Plugins
> `kotlin("jvm")`, `kotlin("plugin.spring")` (allopen), `kotlin("plugin.jpa")` (noarg), `kotlin("multiplatform")`.
>
> ### 4.7 Build Performance
> Parallel project execution, build caching, Gradle daemon, configuration cache.

---

## Key Concepts

- **Gradle task** — a named unit of work; Gradle executes tasks in dependency order. See [[kotlin-spring-android#gradle-task]].
- **Task graph (DAG)** — Gradle builds a directed acyclic graph of tasks; it executes them in topological order.
- **Version catalog** — a `libs.versions.toml` file that centralizes all dependency versions; prevents version drift in multi-module projects.
- **Convention plugin** — a precompiled build script in `buildSrc/` that can be applied to multiple modules; the idiomatic way to share build configuration.
- **Incremental build** — Gradle skips tasks whose inputs and outputs have not changed since the last build, dramatically speeding up repeated builds.

---

## Examples

```kotlin
// build.gradle.kts — Spring Boot + Kotlin project
plugins {
    kotlin("jvm") version "2.0.0"
    kotlin("plugin.spring") version "2.0.0"
    kotlin("plugin.jpa") version "2.0.0"
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
}

group = "com.example"
version = "1.0.0"

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    runtimeOnly("org.postgresql:postgresql")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:postgresql")
}

tasks.withType<KotlinCompile> {
    compilerOptions {
        freeCompilerArgs.addAll("-Xjsr305=strict")
        jvmTarget.set(JvmTarget.JVM_21)
    }
}

tasks.withType<Test> { useJUnitPlatform() }

// Custom task
tasks.register("generateApiDocs") {
    group = "documentation"
    description = "Generate API documentation from OpenAPI spec"
    doLast {
        println("Generating API docs...")
    }
}
```

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "2.0.0"
spring-boot = "3.3.0"
testcontainers = "1.19.8"

[libraries]
spring-boot-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
testcontainers-postgresql = { module = "org.testcontainers:postgresql", version.ref = "testcontainers" }

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

---

## Common Pitfalls

> - **Groovy vs Kotlin DSL syntax differences** — copy-pasting Groovy snippets from StackOverflow into a `.kts` file will fail; Kotlin DSL uses string property access syntax
> - **Missing `useJUnitPlatform()`** — JUnit 5 tests don't run without this; it's easy to forget
> - **Not using version catalogs in multi-module projects** — each module defining its own dependency versions leads to version drift and conflicts
> - **`buildSrc` vs included builds** — `buildSrc` is recompiled on every Gradle invocation and pollutes the build classpath; prefer included builds for convention plugins in large projects

---

## Cross-Links

- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Kotlin DSL is Kotlin; extension functions and lambdas appear throughout `build.gradle.kts`
- [[kotlin-spring-android/modules/12_capstone-project]] — Capstone project uses a multi-module Gradle structure

---

## Summary

> - The Kotlin DSL (`build.gradle.kts`) is type-safe and IDE-assisted; it replaces Groovy DSL in modern Kotlin projects
> - Version catalogs (`libs.versions.toml`) centralize dependency versions; essential in multi-module projects
> - Convention plugins (in `buildSrc` or as included builds) share common build configuration across modules
> - The `kotlin("plugin.spring")` plugin makes Spring-annotated classes `open`; `kotlin("plugin.jpa")` generates no-args constructors for JPA entities
> - Gradle's incremental build and caching dramatically speed up development iteration; understand what invalidates a task's cache
