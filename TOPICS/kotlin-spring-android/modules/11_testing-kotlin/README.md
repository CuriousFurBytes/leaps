# Module 11: Testing in Kotlin

[← Module 10: Android Advanced](../10_android-advanced/) | [Topic Home](../../README.md) | [Next → Module 12: Capstone Project](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-10h-orange)

> JUnit 5 with Kotlin idioms, Mockk for mocking, Spring test slices (@WebMvcTest, @DataJpaTest), TestContainers for integration tests, and Espresso/Compose UI testing for Android.

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

Production code without tests is a liability. This module teaches testing at every level of the Kotlin stack: **unit tests** with JUnit 5 and Mockk (the Kotlin-native mocking library), **Spring test slices** that test web controllers and JPA repositories in isolation without starting the full application context, **integration tests** with TestContainers that spin up a real PostgreSQL database in Docker, and **Android UI tests** with Compose UI Testing and Espresso.

Understanding the test pyramid — many cheap unit tests, fewer integration tests, a small number of end-to-end tests — is as important as knowing the API of each testing library.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> See [[qa-testing]] for general testing philosophy.

---

## Prerequisites

- Modules 04–07: Spring Boot (for Spring test slices)
- Modules 09–10: Android (for Compose UI testing)
- Module 03: Kotlin Advanced (coroutines, for testing suspend functions)

---

## Objectives

By the end of this module, you will be able to:

1. Write idiomatic JUnit 5 tests in Kotlin using `@Test`, `@BeforeEach`, `@ParameterizedTest`, and `@ExtendWith`
2. Mock dependencies with Mockk: `mockk()`, `every { }`, `verify { }`, and coroutine-aware mocking
3. Test Spring MVC controllers in isolation with `@WebMvcTest` and `MockMvc`
4. Test Spring Data JPA repositories with `@DataJpaTest` and an in-memory H2 or TestContainers PostgreSQL
5. Write integration tests with TestContainers that use a real PostgreSQL instance
6. Test Kotlin coroutines and Flow with `runTest` and `turbine`
7. Write Android UI tests with Compose Testing APIs and Espresso

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 The Test Pyramid
> Unit, integration, end-to-end tests; speed vs fidelity trade-off; the right mix for a Spring Boot + Android project.
>
> ### 4.2 JUnit 5 with Kotlin
> `@Test`, `@BeforeEach`/`@AfterEach`, `@ParameterizedTest`, `@ExtendWith`, `@Nested`, `assertEquals` vs `assertThat`.
>
> ### 4.3 Mockk
> `mockk()`, `spyk()`, `every { }`, `returns`/`throws`/`answers`, `verify { }`, `coEvery`/`coVerify` for coroutines.
>
> ### 4.4 Spring Test Slices
> `@WebMvcTest` (web layer only), `@DataJpaTest` (persistence layer only), `@SpringBootTest` (full context).
>
> ### 4.5 TestContainers
> `PostgreSQLContainer`, `@Container`, `@DynamicPropertySource`, running real databases in tests.
>
> ### 4.6 Testing Coroutines and Flow
> `runTest`, `TestCoroutineDispatcher`, Turbine library for Flow testing.
>
> ### 4.7 Android UI Testing
> Compose `createComposeRule()`, `onNodeWithText`, `performClick`, Espresso `onView`/`withId`/`perform`.

---

## Key Concepts

- **JUnit 5** — the standard Java/Kotlin test framework; uses `@Test`, `@BeforeEach`, and extensions (`@ExtendWith`) to compose test behavior.
- **Mockk** — a Kotlin-native mocking library; unlike Mockito, it supports `suspend` functions, coroutines, and Kotlin-specific patterns natively.
- **`@WebMvcTest`** — a Spring test slice that loads only the web layer (controllers, filters, security); does not load services or repositories; requires mocking dependencies.
- **`@DataJpaTest`** — a Spring test slice that loads only the JPA layer with an in-memory database; ideal for testing repository queries.
- **TestContainers** — a Java library that spins up real Docker containers (PostgreSQL, Kafka, Redis) for integration tests; tests run against real infrastructure.

---

## Examples

```kotlin
// Preview: WebMvcTest for a controller
@WebMvcTest(ProductController::class)
@WithMockUser
class ProductControllerTest {

    @Autowired lateinit var mockMvc: MockMvc
    @MockkBean lateinit var service: ProductService

    @Test
    fun `GET product by ID returns 200 with product body`() {
        val product = Product(1L, "Kotlin in Action", BigDecimal("39.99"))
        every { service.findById(1L) } returns product

        mockMvc.get("/api/products/1") {
            accept = MediaType.APPLICATION_JSON
        }.andExpect {
            status { isOk() }
            jsonPath("$.name") { value("Kotlin in Action") }
        }
    }
}

// Preview: TestContainers integration test
@SpringBootTest
@Testcontainers
class ProductRepositoryIT {

    companion object {
        @Container
        @JvmStatic
        val postgres = PostgreSQLContainer("postgres:16-alpine")

        @DynamicPropertySource
        @JvmStatic
        fun configureProperties(registry: DynamicPropertyRegistry) {
            registry.add("spring.datasource.url", postgres::getJdbcUrl)
            registry.add("spring.datasource.username", postgres::getUsername)
            registry.add("spring.datasource.password", postgres::getPassword)
        }
    }

    @Autowired lateinit var repository: ProductRepository

    @Test
    fun `findByPriceRange returns products within range`() {
        // Given
        repository.saveAll(listOf(
            Product(name = "Cheap", price = BigDecimal("5.00")),
            Product(name = "Mid", price = BigDecimal("25.00")),
            Product(name = "Expensive", price = BigDecimal("100.00"))
        ))

        // When
        val results = repository.findByPriceRange(BigDecimal("10.00"), BigDecimal("50.00"))

        // Then
        assertThat(results).hasSize(1)
        assertThat(results[0].name).isEqualTo("Mid")
    }
}
```

---

## Common Pitfalls

> - **Using Mockito instead of Mockk** — Mockito doesn't support `final` Kotlin classes or `suspend` functions natively; use Mockk for Kotlin projects
> - **`@SpringBootTest` for everything** — loading the full application context is slow; use `@WebMvcTest` or `@DataJpaTest` slices for focused tests
> - **Not testing error cases** — test the unhappy path: what happens with null inputs, database errors, network failures?
> - **TestContainers slow startup** — mark containers as `@Container` with `@Singleton` scope (or use `companion object`) so the container is reused across tests in the same JVM

---

## Cross-Links

- [[kotlin-spring-android/modules/04_spring-boot-fundamentals]] — Spring Boot structure being tested
- [[kotlin-spring-android/modules/05_spring-data-and-persistence]] — JPA repositories tested with `@DataJpaTest`
- [[kotlin-spring-android/modules/06_spring-security]] — Security testing with `@WithMockUser`
- [[qa-testing]] — General testing philosophy, the test pyramid, TDD practices

---

## Summary

> - JUnit 5 with Kotlin uses the same `@Test` annotations; use backtick method names for readable test descriptions
> - Mockk is the Kotlin-native mock library; use `coEvery`/`coVerify` for suspend functions
> - Spring test slices (`@WebMvcTest`, `@DataJpaTest`) give fast, focused tests for specific layers
> - TestContainers tests against real Docker containers — the most reliable way to test database queries and Kafka flows
> - `runTest` from `kotlinx-coroutines-test` is the correct way to test suspend functions and Flow; never use `runBlocking` in tests
