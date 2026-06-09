# Module 02: Kotlin Language for Services

> Learn the Kotlin language features that make service code safer, clearer, and easier to test.

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

Kotlin service code succeeds when domain data is explicit, nulls are handled intentionally, and behavior is separated from framework wiring. The language gives you tools for those goals: nullable types, data classes, default parameters, sealed classes, collection operators, and coroutines.

Historically, Kotlin's null-safety was a direct answer to the runtime null pointer failures common in Java codebases. For backend and Android work, that matters because JSON fields, database values, user input, and network responses are all places where absence must be modeled rather than wished away.

## Prerequisites

- Module 01: Orientation and Tooling in this topic.
- Basic comfort running short Kotlin snippets.

## Objectives

By the end of this module, you will be able to:
- Model request and response data with Kotlin data classes.
- Use nullable types and safe calls instead of unsafe assumptions.
- Represent success and failure with sealed classes.
- Write small service functions that can later be wired into Spring or Android.

## Theory

### Null-Safety as a Type-Level Contract

Kotlin separates `String` from `String?`. That single question mark moves a common runtime failure into the compiler's field of vision. Service code benefits because external input is rarely trustworthy.

```kotlin
fun normalizeEmail(raw: String?): String? {
    // safe-call returns null when raw is null; no exception is thrown.
    return raw?.trim()?.lowercase()?.takeIf { it.contains("@") }
}
```

### Data Classes for API Boundaries

Data classes are a natural fit for DTOs because they make fields visible and provide equality, copying, and readable output. They should still represent a deliberate contract, not an automatic dump of database tables.

```kotlin
data class CreateUserRequest(val email: String, val displayName: String?)
data class UserResponse(val id: Long, val email: String, val displayName: String)

fun toResponse(id: Long, request: CreateUserRequest): UserResponse {
    return UserResponse(id, request.email, request.displayName ?: "Anonymous")
}
```

### Sealed Results and Coroutines

A sealed class gives callers a closed set of outcomes. Coroutines let asynchronous code read sequentially, though real Spring and Android coroutine integration requires dispatcher and lifecycle awareness.

```kotlin
sealed class LookupResult {
    data class Found(val email: String) : LookupResult()
    data object Missing : LookupResult()
}

fun describe(result: LookupResult): String = when (result) {
    is LookupResult.Found -> "Found ${result.email}"
    LookupResult.Missing -> "No user found"
}
```

## Key Concepts

- **Nullable type:** A type such as `String?` that explicitly allows absence.
- **Elvis operator:** The `?:` operator that provides a fallback when the left side is null.
- **Data class:** A concise class form for immutable-ish data carriers and API models.
- **Sealed class:** A restricted hierarchy useful for modeling known outcomes.
- **Coroutine:** A language-supported unit of suspendable work used for asynchronous flows.

## Examples

### Scenario: Validate Input Before Framework Wiring

```kotlin
data class ValidationError(val field: String, val message: String)

fun validateEmail(email: String?): List<ValidationError> {
    if (email.isNullOrBlank()) return listOf(ValidationError("email", "required"))
    if (!email.contains("@")) return listOf(ValidationError("email", "must contain @"))
    return emptyList()
}
```

The function is framework-free, so it can be tested before adding a Spring controller or Android form.

## Common Pitfalls

### Forcing Nulls With `!!`

Wrong:

```kotlin
fun length(input: String?): Int = input!!.length
```

Correct:

```kotlin
fun length(input: String?): Int = input?.length ?: 0
```

`!!` converts a type warning back into a runtime crash.

### Exposing Database Models as API Models

Wrong:

```kotlin
data class UserEntity(val id: Long, val passwordHash: String)
```

Correct:

```kotlin
data class UserResponse(val id: Long)
```

API models should reveal only the contract clients need.

### Ignoring Exhaustive `when`

Wrong:

```kotlin
fun label(result: LookupResult): String = "maybe found"
```

Correct:

```kotlin
fun label(result: LookupResult): String = when (result) {
    is LookupResult.Found -> "found"
    LookupResult.Missing -> "missing"
}
```

Exhaustive handling protects you when outcomes change.

## Cross-Links

- [[kotlin-backend-android#module-map]]
- [[kotlin-backend-android#quick-reference]]
- [[kotlin-backend-android#why-learn-kotlin-backend-and-android]]

Related future topic areas: Java, Spring, Android, Gradle, Maven, software testing, and DevOps.


## Summary

- Kotlin null-safety makes absence explicit and testable.
- Data classes are strong candidates for request and response DTOs.
- Sealed classes model known outcomes better than strings or magic numbers.
- Keep early service functions framework-free so behavior is easy to test.
- Coroutines are powerful, but production use must respect runtime context.
