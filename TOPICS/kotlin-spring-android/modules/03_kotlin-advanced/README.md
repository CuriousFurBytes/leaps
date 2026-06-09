# Module 03: Kotlin Advanced

[← Module 02: Kotlin Fundamentals](../02_kotlin-fundamentals/) | [Topic Home](../../README.md) | [Next → Module 04: Spring Boot Fundamentals](../04_spring-boot-fundamentals/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-12h-orange)

> Kotlin coroutines, structured concurrency, Flow, extension functions, DSL building, and property delegation.

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

Module 03 introduces the features that make Kotlin distinctively powerful rather than merely a "better Java." Coroutines are Kotlin's structured concurrency model — a way to write asynchronous code that reads like sequential code, using the `suspend` keyword and coroutine builders like `launch`, `async`, and `flow`. `Flow` is the cold asynchronous stream abstraction that replaces RxJava for most use cases.

Extension functions and lambda receivers enable Kotlin's DSL capabilities — the same mechanism behind Gradle Kotlin DSL, Spring's Kotlin extensions, and Jetpack Compose. You will understand how to build type-safe, fluent APIs.

Delegation — both interface delegation and property delegation — is covered in depth, including the standard library delegates (`lazy`, `observable`, `vetoable`) and how to write custom delegates.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> The [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html) covers coroutines thoroughly.

---

## Prerequisites

- Module 01: Introduction to Kotlin — null safety, functions, lambdas
- Module 02: Kotlin Fundamentals — generics, sealed classes, inline functions

---

## Objectives

By the end of this module, you will be able to:

1. Explain what a coroutine is and how it differs from a thread
2. Write and compose `suspend` functions using `launch`, `async`/`await`, and `withContext`
3. Implement `Flow` for cold asynchronous streams and collect them safely with lifecycle awareness
4. Use `StateFlow` and `SharedFlow` for hot streams in both Android and backend contexts
5. Build type-safe DSLs using extension functions with receiver lambdas
6. Apply built-in property delegates (`lazy`, `observable`) and write custom property delegates
7. Use interface delegation (`by`) to compose behavior without inheritance

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Coroutines: The Mental Model
> Coroutines vs threads, cooperative scheduling, the `suspend` modifier, continuation-passing style.
>
> ### 4.2 Coroutine Builders and Scope
> `launch`, `async`/`await`, `runBlocking`, `coroutineScope`, `CoroutineScope`, structured concurrency.
>
> ### 4.3 Flow: Asynchronous Streams
> Cold vs hot streams, `flow { emit() }`, `collect`, operators (`map`, `filter`, `transform`), `StateFlow`, `SharedFlow`.
>
> ### 4.4 Coroutine Dispatchers and Context
> `Dispatchers.Main`, `Dispatchers.IO`, `Dispatchers.Default`, `withContext`, exception handling.
>
> ### 4.5 Extension Functions and Lambda Receivers
> Extension functions with receivers, building DSLs, `apply`, `let`, `run`, `also`, `with`.
>
> ### 4.6 Property Delegation
> `by lazy`, `by observable`, `by vetoable`, writing custom delegates, `ReadWriteProperty`.
>
> ### 4.7 Interface Delegation
> `by` for interface delegation, composition over inheritance, mixin patterns.

---

## Key Concepts

- **coroutine** — a suspendable computation that can be paused and resumed without blocking a thread. See [[kotlin-spring-android#coroutine]].
- **suspend function** — a function that can be paused mid-execution; can only be called from a coroutine or another suspend function. See [[kotlin-spring-android#suspend-function]].
- **Flow** — a cold asynchronous stream that emits values over time; consumed by calling `collect`.
- **DSL** — a domain-specific mini-language built using Kotlin extension functions with receiver lambdas. See [[kotlin-spring-android#dsl-domain-specific-language]].
- **delegation** — forwarding interface calls or property access to a delegate object using `by`. See [[kotlin-spring-android#delegation]].

---

## Examples

```kotlin
// Preview: structured concurrency with async/await
import kotlinx.coroutines.*

suspend fun loadDashboard(): Dashboard {
    return coroutineScope {
        // Both requests run concurrently
        val user = async { api.loadUser() }
        val feed = async { api.loadFeed() }
        Dashboard(user.await(), feed.await())
    }
}
```

```kotlin
// Preview: Flow for a paginated data stream
fun pagedResults(query: String): Flow<List<Result>> = flow {
    var page = 0
    while (true) {
        val results = api.search(query, page++)
        if (results.isEmpty()) break
        emit(results)
    }
}
```

---

## Common Pitfalls

> - **Forgetting `structured concurrency`** — never launch coroutines in `GlobalScope` in production; always use a scoped `CoroutineScope`
> - **Blocking the main thread** — calling blocking code (JDBC, file I/O) without switching to `Dispatchers.IO` stalls the UI or server
> - **Conflating Flow and StateFlow** — `Flow` is cold (starts fresh per collector); `StateFlow` is hot (always has the latest value and replays to new collectors)
> - **Extension functions are not virtual** — they are resolved statically at compile time; subclasses cannot override extension functions

---

## Cross-Links

- [[kotlin-spring-android/modules/02_kotlin-fundamentals]] — Generics and lambdas prerequisite for understanding coroutines
- [[kotlin-spring-android/modules/07_spring-advanced]] — WebFlux reactive programming connects to Kotlin coroutines
- [[kotlin-spring-android/modules/10_android-advanced]] — ViewModel + StateFlow pattern uses coroutines throughout

---

## Summary

> - Coroutines allow non-blocking asynchronous code that reads sequentially — no callbacks, no thread blocking
> - `launch` fires-and-forgets; `async`/`await` produces a result; `coroutineScope` enforces structured hierarchy
> - `Flow` is the cold stream abstraction; `StateFlow` is the observable state holder used in ViewModels and Spring
> - Extension functions with receivers enable Kotlin's DSL pattern — the basis of Gradle DSL, Compose, and Spring Kotlin extensions
> - Property delegation (`by lazy`) defers initialization until first use; `by observable` reacts to property changes
