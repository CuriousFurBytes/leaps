# Module 04: Spring Boot Fundamentals

[← Module 03: Kotlin Advanced](../03_kotlin-advanced/) | [Topic Home](../../README.md) | [Next → Module 05: Spring Data and Persistence](../05_spring-data-and-persistence/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-10h-orange)

> Spring Boot auto-configuration, Inversion of Control, Dependency Injection, REST controllers, request mapping, and building your first Spring Boot + Kotlin API.

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

Spring Boot is the dominant Java/Kotlin backend framework. It builds on the Spring Framework (released in 2003 by Rod Johnson) by adding auto-configuration, embedded servers, and opinionated defaults — dramatically reducing the XML configuration that made early Spring notoriously verbose.

This module teaches the core concepts every Spring Boot developer must understand: **Inversion of Control (IoC)** and **Dependency Injection (DI)** — the mechanisms by which Spring manages your objects and wires them together — and the annotation model that expresses that wiring (`@Component`, `@Service`, `@Repository`, `@Controller`).

The second half of the module covers REST API development with `@RestController`, request mapping annotations, path variables, request bodies, and response entities.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> See the [Spring Boot + Kotlin official guide](https://spring.io/guides/tutorials/spring-boot-kotlin/) while the full module is being written.

---

## Prerequisites

- Modules 01–03: Kotlin language (all three modules)
- Basic understanding of HTTP (GET, POST, PUT, DELETE, status codes)
- Java 17 or 21 installed; IntelliJ IDEA or VS Code

---

## Objectives

By the end of this module, you will be able to:

1. Explain Inversion of Control and Dependency Injection and why they matter for testability
2. Create a Spring Boot project with Kotlin using Spring Initializr
3. Define and wire Spring beans using `@Component`, `@Service`, `@Repository`, and `@Configuration`
4. Build REST endpoints with `@RestController`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`
5. Use `@PathVariable`, `@RequestParam`, and `@RequestBody` to handle request data
6. Return proper HTTP responses with `ResponseEntity<T>`
7. Configure the application using `application.yml` / `application.properties`
8. Run and test the API with curl or an HTTP client

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Spring Framework and Spring Boot: The Origin Story
> Rod Johnson's "Expert One-on-One J2EE Design and Development" (2002), the XML-configuration era, Spring Boot's auto-configuration revolution (2014).
>
> ### 4.2 Inversion of Control and the Spring Application Context
> IoC container, bean lifecycle, `ApplicationContext`, why IoC improves testability and modularity.
>
> ### 4.3 Dependency Injection in Kotlin
> Constructor injection (preferred), `@Autowired`, why Kotlin's data classes and constructor injection pair well, `lateinit var`.
>
> ### 4.4 Component Stereotypes: @Component, @Service, @Repository, @Controller
> Semantic differences, classpath scanning, `@ComponentScan`.
>
> ### 4.5 Building REST APIs with @RestController
> `@RequestMapping`, method-specific shortcuts, `@PathVariable`, `@RequestParam`, `@RequestBody`.
>
> ### 4.6 ResponseEntity and Error Handling
> `ResponseEntity<T>`, status codes, `@ExceptionHandler`, `@ControllerAdvice`.
>
> ### 4.7 Configuration and Profiles
> `application.yml`, `@Value`, `@ConfigurationProperties`, Spring profiles.

---

## Key Concepts

- **IoC (Inversion of Control)** — objects do not create their dependencies; the Spring container provides them. This inverts the traditional flow of control.
- **Dependency Injection** — a specific form of IoC; dependencies are "injected" into a class via constructor, setter, or field.
- **Spring Bean** — any object managed by the Spring IoC container.
- **Auto-configuration** — Spring Boot's mechanism for configuring the application based on what's on the classpath, eliminating most boilerplate configuration.
- **`@RestController`** — a specialization of `@Controller` that adds `@ResponseBody` to every method, meaning return values are serialized to JSON/XML automatically.

---

## Examples

```kotlin
// Preview: a minimal Spring Boot application in Kotlin
@SpringBootApplication
class Application

fun main(args: Array<String>) {
    runApplication<Application>(*args)
}

// Preview: a REST controller
@RestController
@RequestMapping("/api/products")
class ProductController(private val service: ProductService) {

    @GetMapping("/{id}")
    fun getProduct(@PathVariable id: Long): ResponseEntity<ProductDto> {
        val product = service.findById(id)
            ?: return ResponseEntity.notFound().build()
        return ResponseEntity.ok(product.toDto())
    }

    @PostMapping
    fun createProduct(@RequestBody request: CreateProductRequest): ResponseEntity<ProductDto> {
        val product = service.create(request)
        return ResponseEntity.status(HttpStatus.CREATED).body(product.toDto())
    }
}
```

---

## Common Pitfalls

> - **Field injection with `@Autowired`** — prefer constructor injection; field injection makes testing harder and hides dependencies
> - **`open` classes for Spring proxies** — Spring creates proxies for `@Service` classes; Kotlin's `final` by default breaks this without the `kotlin-spring` plugin (which automatically opens Spring-annotated classes)
> - **Forgetting the `kotlin-spring` plugin** — adds `open` to `@Component`, `@Service`, `@Repository`, `@Controller` and their meta-annotations; required in `build.gradle.kts`
> - **Null safety with Jackson** — Jackson deserializes JSON to Kotlin data classes; without `jackson-module-kotlin`, deserialization of non-nullable fields may fail

---

## Cross-Links

- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Kotlin coroutines used in async Spring services
- [[kotlin-spring-android/modules/05_spring-data-and-persistence]] — JPA repositories and database access build directly on this module
- [[kotlin-spring-android/modules/06_spring-security]] — Authentication and authorization layer added on top of this module's REST layer
- [[graphql-rest]] — REST API design principles applied in this module

---

## Summary

> - Spring Boot uses auto-configuration to eliminate boilerplate; you declare what you need via dependencies, and Spring configures it
> - IoC/DI means Spring creates and wires your objects — you express the wiring through annotations
> - Constructor injection is the recommended injection style in Kotlin; it pairs with `val` properties and makes testing straightforward
> - `@RestController` + `@RequestMapping` + HTTP method annotations is the complete picture for building REST endpoints
> - The `kotlin-spring` Gradle plugin is essential — it opens Spring-annotated Kotlin classes for proxying
