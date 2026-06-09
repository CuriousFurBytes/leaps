# Module 01: Orientation and Tooling

> Install the Kotlin/JVM toolchain, understand where backend and Android Kotlin differ, and run the first working examples.

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

Kotlin began as a JetBrains language for the JVM and grew into a practical language for Android, servers, scripts, and multiplatform projects. Its design keeps Java interoperability while adding null-safety, concise data modeling, extension functions, and coroutine-based concurrency.

This module treats tooling as a core skill. Professional Kotlin work depends on the JDK, a build tool, dependency repositories, tests, IDE support, and an understanding of the runtime target. A Spring service runs as a long-lived JVM process; an Android app runs inside a managed mobile environment with lifecycle and resource constraints.

## Prerequisites

- Basic file editing and terminal usage.
- No previous Kotlin, Spring, Android, Maven, or Gradle experience is required.

## Objectives

By the end of this module, you will be able to:
- Explain how Kotlin, the JDK, Gradle, Maven, Spring, and Android relate.
- Run a minimal Kotlin program and identify the entry point.
- Distinguish backend JVM constraints from Android device constraints.
- Choose the next setup step for a Spring project or Android project.

## Theory

### The Kotlin Stack

Kotlin source usually compiles to JVM bytecode for backend work and Android bytecode for Android work. The important mental model is pipeline-based: source code becomes compiled classes, build tools assemble dependencies, tests verify behavior, and a runtime executes the artifact. Kotlin did not replace the JVM ecosystem; it made that ecosystem safer and more expressive.

```kotlin
// main is the program entry point for this tiny JVM application.
fun main() {
    val runtime = System.getProperty("java.version") // Reads the active JDK version.
    println("Kotlin is running on Java $runtime") // Prints runtime evidence.
}
```

### Backend Versus Android Runtime

A Spring backend listens for requests, keeps connection pools, talks to databases, and is monitored in production. An Android app responds to user input, lifecycle callbacks, permissions, battery constraints, and intermittent networks. Both can share Kotlin syntax, but they do not share the same operational assumptions.

```kotlin
// Backend-shaped pure function: easy to test before wiring it into Spring.
fun greetingForUser(name: String): String {
    val safeName = name.trim().ifBlank { "friend" } // Avoids empty display output.
    return "Hello, $safeName"
}
```

### Build Tools as Reproducibility Tools

Gradle and Maven are not just command runners. They record dependencies, plugins, source sets, test tasks, packaging rules, and publication metadata. Gradle is common in Android and many Kotlin-first projects; Maven remains common in Java/Spring organizations. Expert Kotlin developers can read both.

```bash
# Verify the local Java runtime before creating Kotlin JVM projects.
java -version

# Common Gradle wrapper command used after a project has been generated.
./gradlew test
```

## Key Concepts

- **JDK:** The Java Development Kit supplies the compiler tools and runtime used by Kotlin/JVM and Spring applications.
- **Kotlin compiler:** The tool that turns `.kt` source into executable artifacts for the selected target.
- **Gradle wrapper:** A project-local script that pins Gradle version and makes builds reproducible across machines.
- **Maven coordinates:** The `groupId:artifactId:version` identity used to fetch libraries from repositories.
- **Android runtime:** The managed mobile environment where app components run under lifecycle and device constraints.

## Examples

### Scenario: First Domain Model

```kotlin
// A data class gives value-style equality, toString, and copy behavior.
data class HealthCheck(val service: String, val status: String)

fun main() {
    val check = HealthCheck(service = "api", status = "UP")
    println(check)
}
```

Use tiny models early because they work in backend controllers, Android screens, and tests.

## Common Pitfalls

### Installing Kotlin but Not the JDK

Wrong:

```bash
kotlin -version
```

Correct:

```bash
java -version
kotlin -version
```

Kotlin/JVM needs a Java runtime target; checking both avoids confusing build failures.

### Treating Android Like a Server

Wrong:

```kotlin
while (true) {
    println("poll forever") // Wastes battery and ignores lifecycle.
}
```

Correct:

```kotlin
fun refreshOnce() {
    println("refresh when lifecycle or user action requests it")
}
```

Android work must cooperate with lifecycle, battery, and network constraints.

### Depending on Global Gradle

Wrong:

```bash
gradle build
```

Correct:

```bash
./gradlew build
```

The wrapper keeps the whole team on the same build tool version.

## Cross-Links

- [[kotlin-backend-android#module-map]]
- [[kotlin-backend-android#quick-reference]]
- [[kotlin-backend-android#why-learn-kotlin-backend-and-android]]

Related future topic areas: Java, Spring, Android, Gradle, Maven, software testing, and DevOps.


## Summary

- Kotlin can target backend JVM services and Android apps, but each runtime has different constraints.
- The JDK is foundational for Kotlin/JVM development.
- Gradle and Maven encode reproducible builds, dependency resolution, and test execution.
- Spring services are long-running server processes; Android apps are lifecycle-driven clients.
- Small runnable examples are the safest way to validate tooling before adding frameworks.
