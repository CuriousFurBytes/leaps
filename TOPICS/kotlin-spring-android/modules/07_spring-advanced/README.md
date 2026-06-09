# Module 07: Spring Advanced

[← Module 06: Spring Security](../06_spring-security/) | [Topic Home](../../README.md) | [Next → Module 08: Gradle and Build Tooling](../08_gradle-and-build/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-10h-orange)

> Spring Actuator, caching with @Cacheable, Apache Kafka integration, reactive programming with WebFlux and coroutines, and @Scheduled tasks.

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

Module 07 covers the Spring Boot features that separate basic applications from production-grade systems. These are the patterns you encounter when scaling a service beyond a simple CRUD API.

**Spring Actuator** provides production-ready observability: health checks, metrics, info endpoints, and integration with Prometheus/Grafana. **Caching** with `@Cacheable` and Caffeine/Redis dramatically reduces database load for frequently-read data. **Apache Kafka** enables event-driven architecture — decoupled, scalable inter-service communication. **Spring WebFlux** with Kotlin coroutines provides reactive, non-blocking I/O for high-throughput scenarios. **`@Scheduled`** tasks handle time-based background jobs.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.

---

## Prerequisites

- Modules 04–06: Spring Boot, Spring Data, Spring Security
- Module 03: Kotlin Advanced (coroutines, for WebFlux section)
- Basic understanding of message queues (helpful but not required for Kafka section)

---

## Objectives

By the end of this module, you will be able to:

1. Expose and configure Spring Actuator endpoints for health, metrics, and info
2. Implement application caching with `@Cacheable`, `@CacheEvict`, and `@CachePut`
3. Produce and consume Kafka messages with `KafkaTemplate` and `@KafkaListener`
4. Build reactive HTTP handlers with Spring WebFlux using Kotlin coroutines
5. Schedule background tasks with `@Scheduled` (fixed rate, fixed delay, and cron expressions)
6. Understand when to choose reactive (WebFlux) vs imperative (MVC) Spring

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Spring Actuator
> Health indicators, metrics (Micrometer), Prometheus export, info endpoint, custom actuator endpoints.
>
> ### 4.2 Caching
> `@EnableCaching`, `@Cacheable`, `@CacheEvict`, `@CachePut`, Caffeine for in-process caching, Redis for distributed caching.
>
> ### 4.3 Apache Kafka Integration
> Kafka concepts (topics, partitions, consumer groups), `KafkaTemplate`, `@KafkaListener`, error handling, idempotent consumers.
>
> ### 4.4 Spring WebFlux with Kotlin Coroutines
> Reactive vs imperative, `RouterFunction`, handler functions, `suspend` functions in WebFlux, `Flow` as response body.
>
> ### 4.5 Scheduled Tasks
> `@EnableScheduling`, `@Scheduled` with `fixedRate`, `fixedDelay`, and `cron`, distributed scheduling considerations.

---

## Key Concepts

- **Spring Actuator** — adds production-ready management endpoints to a Spring Boot app: `/health`, `/metrics`, `/info`, `/env`.
- **`@Cacheable`** — caches the return value of a method by key; subsequent calls with the same key return the cached value without executing the method.
- **Kafka topic** — a durable, ordered, append-only log of messages; consumers read at their own pace without blocking producers.
- **WebFlux** — Spring's reactive web framework; handles I/O asynchronously without blocking threads; supports Kotlin coroutines natively.
- **`@Scheduled`** — marks a method to be run by Spring's task scheduler; `fixedRate = 5000` runs every 5 seconds.

---

## Examples

```kotlin
// Preview: caching and eviction
@Service
class ProductService(private val repo: ProductRepository) {

    @Cacheable("products", key = "#id")
    fun findById(id: Long): Product? = repo.findById(id).orElse(null)

    @CacheEvict("products", key = "#product.id")
    fun update(product: Product): Product = repo.save(product)
}

// Preview: Kafka producer and consumer
@Service
class OrderEventProducer(private val kafka: KafkaTemplate<String, OrderEvent>) {
    fun publish(event: OrderEvent) = kafka.send("order-events", event.orderId.toString(), event)
}

@Component
class OrderEventConsumer {
    @KafkaListener(topics = ["order-events"], groupId = "order-processor")
    fun consume(event: OrderEvent) {
        println("Processing order: ${event.orderId}")
    }
}

// Preview: WebFlux with coroutines
@RestController
class ReactiveProductController(private val service: ProductService) {

    @GetMapping("/api/products")
    suspend fun getAll(): Flow<ProductDto> = service.findAll()
}
```

---

## Common Pitfalls

> - **`@Cacheable` on the same class** — Spring caching uses proxies; calling a `@Cacheable` method from within the same class bypasses the cache. Call through the proxy (inject self, or use a separate class).
> - **Kafka consumer groups** — all consumers in the same group share partitions; use different group IDs for independent consumers of the same topic
> - **Blocking in WebFlux** — blocking calls (JDBC, synchronized) in a WebFlux handler stall the event loop; use `Dispatchers.IO` to offload blocking work
> - **Actuator security** — exposing all actuator endpoints publicly leaks sensitive system information; configure authentication for sensitive endpoints

---

## Cross-Links

- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Coroutines and Flow prerequisite for WebFlux section
- [[kotlin-spring-android/modules/06_spring-security]] — Securing Actuator endpoints
- [[kotlin-spring-android/modules/11_testing-kotlin]] — Testing Kafka consumers with embedded Kafka and TestContainers

---

## Summary

> - Actuator gives you production observability for free; configure Prometheus export for metrics
> - `@Cacheable` is simple to add and dramatically reduces database load — but requires careful cache eviction strategy
> - Kafka enables event-driven, decoupled architecture; `@KafkaListener` makes consumption declarative
> - WebFlux + coroutines is the right choice for high-throughput I/O-bound workloads; MVC is simpler for most CRUD applications
> - `@Scheduled` tasks are easy to implement but require careful thought about distributed environments (only one instance should run a task in a cluster)
