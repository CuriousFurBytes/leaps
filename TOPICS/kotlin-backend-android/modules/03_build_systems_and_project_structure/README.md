# Module 03: Build Systems and Project Structure

> Organize Kotlin projects with Gradle and Maven so builds are reproducible, testable, and understandable.

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

## Overview

Build systems are where source code becomes a reliable artifact. Kotlin projects often use Gradle, especially for Android and Kotlin-first applications, while many Spring organizations still use Maven because it is predictable and widely understood.

The historical difference matters. Maven popularized convention-over-configuration and dependency coordinates; Gradle introduced a programmable task graph better suited to complex builds. Expert Kotlin developers avoid tool tribalism and choose based on project constraints, team skill, plugin ecosystem, and reproducibility needs.

## Prerequisites

- Module 01: Orientation and Tooling in this topic.
- Module 02: Kotlin Language for Services in this topic.

## Objectives

By the end of this module, you will be able to:
- Explain Gradle and Maven project structure.
- Read dependency declarations and identify scopes.
- Run tests and builds consistently with wrappers.
- Design a small multi-module layout for backend, Android, and shared code.

## Theory

### Project Layout Is Communication

A conventional Kotlin JVM project separates production code from tests. The folder names tell tools and teammates what code is shipped and what code verifies behavior.

```text
src/main/kotlin/com/example/App.kt
src/test/kotlin/com/example/AppTest.kt
build.gradle.kts
```

### Gradle Kotlin DSL

Gradle's Kotlin DSL uses Kotlin syntax to configure plugins, repositories, and dependencies. This is common in Kotlin-first and Android projects.

```kotlin
plugins {
    kotlin("jvm") version "2.0.0" // Applies Kotlin JVM compilation tasks.
}

repositories {
    mavenCentral() // Resolves public dependencies from Maven Central.
}

dependencies {
    testImplementation(kotlin("test")) // Adds Kotlin test helpers to test source sets.
}
```

### Maven POMs

Maven configuration is XML-based and lifecycle-oriented. Its explicit phases and inherited conventions remain valuable in enterprise Java and Spring projects.

```xml
<dependency>
  <groupId>org.jetbrains.kotlin</groupId>
  <artifactId>kotlin-test</artifactId>
  <scope>test</scope>
</dependency>
```

## Key Concepts

- **Build lifecycle:** The ordered phases or tasks that compile, test, package, and publish code.
- **Dependency scope:** A rule describing where a dependency is available, such as implementation or test only.
- **Source set:** A named group of source files with its own compile and dependency configuration.
- **Multi-module build:** A repository containing separately built modules with explicit dependencies.
- **Wrapper:** A checked-in script that pins the build tool version for reproducibility.

## Examples

### Scenario: Shared DTO Module

```kotlin
// In a shared JVM module, avoid Android or Spring imports.
data class TaskDto(val id: String, val title: String, val completed: Boolean)
```

A shared module should contain portable models and validation rules, not platform-specific framework code.

## Common Pitfalls

### Putting Tests in Main Source

Wrong:

```text
src/main/kotlin/com/example/UserServiceTest.kt
```

Correct:

```text
src/test/kotlin/com/example/UserServiceTest.kt
```

Test source sets keep verification code out of production artifacts.

### Using Dynamic Dependency Versions

Wrong:

```kotlin
implementation("com.example:library:+")
```

Correct:

```kotlin
implementation("com.example:library:1.4.2")
```

Pinned versions make builds repeatable and reviewable.

### Letting Android Depend on Spring

Wrong:

```kotlin
implementation("org.springframework.boot:spring-boot-starter-web")
```

Correct:

```kotlin
implementation("com.squareup.retrofit2:retrofit:2.11.0")
```

Android clients call APIs; they should not embed server frameworks.

## Cross-Links

- [[kotlin-backend-android#module-map]]
- [[kotlin-backend-android#quick-reference]]
- [[kotlin-backend-android#why-learn-kotlin-backend-and-android]]

Related future topic areas: Java, Spring, Android, Gradle, Maven, software testing, and DevOps.


## Summary

- Build files are executable documentation for dependencies, plugins, and tasks.
- Gradle is common for Android and Kotlin-first builds; Maven is common in established JVM organizations.
- Source sets keep production and test code separated.
- Multi-module designs should preserve clear platform boundaries.
- Reproducibility depends on wrappers, pinned versions, and explicit dependency scopes.
