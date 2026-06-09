# Module 05: Spring Data and Persistence

[← Module 04: Spring Boot Fundamentals](../04_spring-boot-fundamentals/) | [Topic Home](../../README.md) | [Next → Module 06: Spring Security](../06_spring-security/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-10h-orange)

> Spring Data JPA with Kotlin: entity classes, repository interfaces, JPQL queries, transactions, pagination, and QueryDSL.

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

Most backend applications exist to store, retrieve, and transform data. Module 05 teaches how Spring Boot applications interact with relational databases through **Spring Data JPA** — a layer that provides automatic repository implementations, query derivation from method names, JPQL/native queries, and transaction management.

The module also covers the specific challenges of using Kotlin with JPA — a framework that was designed for Java and makes assumptions (no-args constructors, non-final classes, mutable fields) that clash with idiomatic Kotlin. You will learn the standard solutions and tradeoffs.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> See the [[postgresql]] topic for deep PostgreSQL knowledge that complements this module.

---

## Prerequisites

- Module 04: Spring Boot Fundamentals — IoC/DI, application structure
- Basic SQL knowledge: SELECT, INSERT, UPDATE, DELETE, JOIN
- [[postgresql]] recommended but not required

---

## Objectives

By the end of this module, you will be able to:

1. Define JPA entities in Kotlin with appropriate annotations, handling the no-args constructor requirement
2. Create Spring Data JPA repository interfaces and use derived query methods
3. Write JPQL and native SQL queries with `@Query`
4. Implement `@Transactional` boundaries correctly
5. Handle relationships (`@OneToMany`, `@ManyToOne`, `@ManyToMany`) and understand lazy vs eager loading
6. Implement pagination and sorting with `Pageable`
7. Understand and apply the repository pattern to separate persistence concerns

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 JPA and Hibernate: The Origin and Model
> Object-relational mapping, JPA specification vs Hibernate implementation, entity lifecycle.
>
> ### 4.2 Defining Kotlin JPA Entities
> `@Entity`, `@Id`, `@GeneratedValue`, the `kotlin-jpa` plugin (no-args constructor), `open` classes requirement.
>
> ### 4.3 Spring Data Repositories
> `JpaRepository<T, ID>`, derived queries from method names (`findByNameAndCity`), `@Query` for JPQL and native SQL.
>
> ### 4.4 Transactions
> `@Transactional`, propagation levels, rollback rules, transaction boundaries in service layer.
>
> ### 4.5 Relationships and Fetch Types
> `@OneToMany`, `@ManyToOne`, `@ManyToMany`, lazy vs eager loading, N+1 query problem, `@EntityGraph`.
>
> ### 4.6 Pagination and Sorting
> `Pageable`, `Page<T>`, `Slice<T>`, `Sort`, exposing pagination via REST.
>
> ### 4.7 QueryDSL (Optional)
> Type-safe dynamic queries, `QEntity` generation, `JPAQueryFactory`.

---

## Key Concepts

- **JPA Entity** — a class mapped to a database table, annotated with `@Entity`. Each instance corresponds to a row.
- **`@Transactional`** — marks a method as a database transaction boundary; Spring wraps it in a transaction that commits on success and rolls back on exception.
- **Derived query methods** — Spring Data generates SQL from method names: `findByEmailIgnoreCase(email: String)` becomes a `WHERE email ILIKE ?` query.
- **N+1 problem** — lazy loading relationships can trigger N additional queries for N entities; solved with JOIN FETCH or `@EntityGraph`.
- **`kotlin-jpa` plugin** — Gradle plugin that generates no-args constructors for `@Entity`, `@Embeddable`, and `@MappedSuperclass` classes, required by JPA.

---

## Examples

```kotlin
// Preview: a Kotlin JPA entity
@Entity
@Table(name = "products")
class Product(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = false, length = 200)
    var name: String,

    @Column(nullable = false)
    var price: BigDecimal,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    var category: Category? = null
)

// Preview: Spring Data JPA repository
interface ProductRepository : JpaRepository<Product, Long> {
    fun findByNameContainingIgnoreCase(name: String, pageable: Pageable): Page<Product>

    @Query("SELECT p FROM Product p WHERE p.price BETWEEN :min AND :max")
    fun findByPriceRange(
        @Param("min") min: BigDecimal,
        @Param("max") max: BigDecimal
    ): List<Product>
}
```

---

## Common Pitfalls

> - **Using `data class` for JPA entities** — `data class` generates `hashCode` based on all fields; using it with JPA (where entities may be in various load states) causes bugs; use regular `class`
> - **Forgetting the `kotlin-jpa` plugin** — JPA requires a no-args constructor; the plugin generates it; without it, JPA cannot instantiate entities
> - **`open` for JPA entities** — Hibernate needs to create proxies of entity classes for lazy loading; Kotlin's final classes block this; the `kotlin-allopen` plugin (or `kotlin-jpa`) handles this
> - **LazyInitializationException** — accessing a lazy-loaded collection outside a transaction session fails; always load associations within a transaction or use `@EntityGraph`

---

## Cross-Links

- [[kotlin-spring-android/modules/04_spring-boot-fundamentals]] — Service and repository architecture prerequisite
- [[kotlin-spring-android/modules/06_spring-security]] — Securing data access with method-level security
- [[kotlin-spring-android/modules/11_testing-kotlin]] — `@DataJpaTest` for testing repositories in isolation
- [[postgresql]] — PostgreSQL-specific features (JSONB, full-text search) used via native queries

---

## Summary

> - JPA entities in Kotlin require the `kotlin-jpa` plugin (no-args constructors) and `kotlin-allopen` (for Hibernate proxies)
> - Use regular `class` for JPA entities, not `data class`
> - Spring Data JPA generates repository implementations automatically from interfaces
> - `@Transactional` should live in the service layer, not the controller or repository
> - The N+1 problem is the most common performance issue with JPA; diagnose with query logging, fix with `JOIN FETCH` or `@EntityGraph`
