# Module 02: Kotlin Fundamentals

[← Module 01: Introduction](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03: Kotlin Advanced](../03_kotlin-advanced/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner--Intermediate-yellowgreen)
![Time](https://img.shields.io/badge/time-10h-orange)

> Object-oriented programming in Kotlin: classes, interfaces, inheritance, sealed classes, data classes, objects, the collections API, and generics.

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

Module 01 gave you the vocabulary and toolset of Kotlin. Module 02 builds on that to teach you how Kotlin models the real world through its object-oriented features — and where those features deliberately diverge from Java's model.

Kotlin's OOP system has several features that Java lacks or handles awkwardly: data classes that auto-generate structural equality, sealed class hierarchies that make state machines type-safe, object declarations for true singletons, companion objects as a replacement for static members, and a collection API that distinguishes read-only from mutable views.

The generics section explains type parameters, variance (`out`/`in`), and reified type parameters — the Kotlin tools for writing type-safe generic code without Java's ceremony.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> See the [Kotlin Official Documentation](https://kotlinlang.org/docs/classes.html) for coverage of these topics while the full module is being written.

---

## Prerequisites

- Module 01: Introduction to Kotlin — null safety, `val`/`var`, functions, basic syntax

---

## Objectives

By the end of this module, you will be able to:

1. Define Kotlin classes with primary and secondary constructors, `init` blocks, and properties
2. Use `data class`, `object`, `companion object`, and `enum class` appropriately
3. Model algebraic data types using `sealed class` hierarchies
4. Implement interfaces and use delegation (`by`) for interface composition
5. Use Kotlin's collections API: `map`, `filter`, `flatMap`, `groupBy`, `fold`, and `reduce`
6. Write generic functions and classes with type parameters, bounds, and `in`/`out` variance
7. Use reified type parameters in inline functions to access generic types at runtime

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Classes and Constructors
> Primary constructors, `init` blocks, secondary constructors, property declarations in constructors.
>
> ### 4.2 Data Classes, Object Declarations, and Companion Objects
> Auto-generated methods, `copy()`, `object` singletons, `companion object` as static replacement.
>
> ### 4.3 Sealed Classes and Enums
> Algebraic data types, exhaustive `when`, `enum class` with properties and methods.
>
> ### 4.4 Interfaces and Delegation
> Interface default methods, multiple interface implementation, `by` for interface delegation.
>
> ### 4.5 Inheritance
> `open` classes, `override`, `abstract`, why Kotlin classes are final by default.
>
> ### 4.6 Collections API
> Immutable vs mutable collections, transformation functions, lazy sequences.
>
> ### 4.7 Generics
> Type parameters, `where` bounds, `in`/`out` variance, `reified` with `inline`.

---

## Key Concepts

- **data class** — generates `equals`, `hashCode`, `toString`, `copy` from constructor parameters. See [[kotlin-spring-android#data-class]].
- **sealed class** — restricted hierarchy; compiler knows all subclasses; enables exhaustive `when`. See [[kotlin-spring-android#sealed-class]].
- **companion object** — singleton associated with a class; replaces Java `static`. See [[kotlin-spring-android#companion-object]].
- **reified type** — allows accessing a generic type parameter at runtime inside `inline` functions. See [[kotlin-spring-android#reified-type]].
- **delegation** — the `by` keyword forwards interface calls to a delegate object. See [[kotlin-spring-android#delegation]].

---

## Examples

> Full worked examples coming in the complete module. Preview:

```kotlin
// Sealed class for a payment result
sealed class PaymentResult
data class PaymentSuccess(val transactionId: String, val amount: Double) : PaymentResult()
data class PaymentFailure(val code: Int, val message: String) : PaymentResult()
object PaymentPending : PaymentResult()

fun handlePayment(result: PaymentResult) = when (result) {
    is PaymentSuccess -> println("Paid: ${result.transactionId}")
    is PaymentFailure -> println("Error ${result.code}: ${result.message}")
    is PaymentPending -> println("Awaiting confirmation...")
}
```

---

## Common Pitfalls

> Full pitfalls section coming in the complete module. Key pitfalls to watch for:
>
> - **Mutable data class fields** — `data class` with `var` properties breaks immutability contracts
> - **Comparing data classes by reference** — use `==` (structural equality), not `===` (referential)
> - **Forgetting `open` on classes intended for inheritance** — Kotlin classes are final by default
> - **Confusing `object` (singleton) with `companion object` (class-scoped singleton)**

---

## Cross-Links

- [[kotlin-spring-android/modules/01_introduction]] — Null safety and basic syntax prerequisites
- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Extension functions and DSLs build on sealed classes and generics
- [[kotlin-spring-android/modules/05_spring-data-and-persistence]] — JPA entities use Kotlin class features; data classes are not ideal for JPA

---

## Summary

> Full summary coming in the complete module. Key takeaways:
>
> - Kotlin classes are `final` by default — use `open` to allow inheritance
> - `data class` is for value objects; avoid using it for JPA entities
> - `sealed class` is the idiomatic way to model algebraic data types
> - `object` is a true singleton; `companion object` provides class-scoped members
> - Kotlin collections distinguish read-only (`List`) from mutable (`MutableList`) views
> - Generics support `in`/`out` variance for type-safe covariant and contravariant parameters
