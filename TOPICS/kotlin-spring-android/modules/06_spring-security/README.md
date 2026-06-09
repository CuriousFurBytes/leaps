# Module 06: Spring Security

[← Module 05: Spring Data and Persistence](../05_spring-data-and-persistence/) | [Topic Home](../../README.md) | [Next → Module 07: Spring Advanced](../07_spring-advanced/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-10h-orange)

> Authentication and authorization with Spring Security: session-based auth, JWT, OAuth2, method-level security, CORS configuration, and security testing.

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

Spring Security is the standard security framework for Spring Boot applications. It provides authentication (who are you?), authorization (what can you do?), protection against common attacks (CSRF, XSS, clickjacking), and integration with OAuth2 identity providers.

This module covers the three most common security patterns for Spring Boot REST APIs: **session-based authentication** (traditional web apps), **JWT (JSON Web Token) authentication** (stateless APIs, preferred for microservices), and **OAuth2** (delegating authentication to an identity provider like Google, GitHub, or Auth0).

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> The [Spring Security Reference](https://docs.spring.io/spring-security/reference/) is the authoritative source while this module is being written.

---

## Prerequisites

- Module 04: Spring Boot Fundamentals
- Module 05: Spring Data and Persistence (for user storage)
- Basic understanding of HTTP authentication mechanisms (Basic Auth, Bearer tokens)

---

## Objectives

By the end of this module, you will be able to:

1. Configure Spring Security's filter chain for a REST API
2. Implement JWT-based authentication with access and refresh tokens
3. Configure OAuth2 login with an external identity provider
4. Apply method-level security with `@PreAuthorize` and SpEL expressions
5. Configure CORS correctly for a frontend-backend separation
6. Test secured endpoints with `@WithMockUser` and `MockMvc`
7. Understand common security vulnerabilities and how Spring Security addresses them

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Spring Security Architecture
> `SecurityFilterChain`, `AuthenticationManager`, `UserDetailsService`, filter execution order.
>
> ### 4.2 JWT Authentication
> JWT structure (header.payload.signature), signing algorithms (HS256, RS256), access token + refresh token pattern, stateless vs stateful auth.
>
> ### 4.3 OAuth2 and OpenID Connect
> Authorization Code flow, resource server configuration, JWT validation against JWKS endpoint.
>
> ### 4.4 Method-Level Security
> `@EnableMethodSecurity`, `@PreAuthorize`, `@PostAuthorize`, SpEL expressions.
>
> ### 4.5 CORS Configuration
> Cross-Origin Resource Sharing, `CorsConfigurationSource`, global vs per-endpoint CORS.
>
> ### 4.6 Security Testing
> `@WithMockUser`, `@WithUserDetails`, `MockMvc` with security, testing JWT filter.

---

## Key Concepts

- **Authentication** — verifying identity ("who are you?"); Spring Security's `AuthenticationManager` handles this.
- **Authorization** — verifying permissions ("what can you do?"); enforced by `SecurityFilterChain` and method security.
- **JWT (JSON Web Token)** — a signed, self-contained token encoding claims (user ID, roles, expiry); stateless — the server does not need a session store.
- **`UserDetailsService`** — the interface Spring Security calls to load a user by username; you implement it to load from your database.
- **`@PreAuthorize`** — method-level annotation that evaluates a SpEL expression before the method runs; e.g., `@PreAuthorize("hasRole('ADMIN')")`.

---

## Examples

```kotlin
// Preview: Security configuration for a JWT REST API
@Configuration
@EnableMethodSecurity
class SecurityConfig(private val jwtFilter: JwtAuthenticationFilter) {

    @Bean
    fun securityFilterChain(http: HttpSecurity): SecurityFilterChain {
        http {
            csrf { disable() }   // disabled for stateless REST APIs
            sessionManagement { sessionCreationPolicy = SessionCreationPolicy.STATELESS }
            authorizeHttpRequests {
                authorize("/api/auth/**", permitAll)
                authorize(anyRequest, authenticated)
            }
            addFilterBefore<UsernamePasswordAuthenticationFilter>(jwtFilter)
        }
        return http.build()
    }
}

// Method-level security
@Service
class OrderService {
    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
    fun getOrdersForUser(userId: Long): List<Order> = TODO()
}
```

---

## Common Pitfalls

> - **Disabling CSRF without understanding the trade-off** — CSRF protection is important for session-based apps; for stateless JWT APIs it can be disabled, but understand why before doing so
> - **Storing JWTs in localStorage** — vulnerable to XSS; prefer httpOnly cookies for web apps
> - **Short JWT expiry without refresh tokens** — a 15-minute JWT with no refresh mechanism logs users out too frequently; implement a refresh token flow
> - **Testing security in isolation** — Spring Security test slices (`@WithMockUser`) bypass the actual JWT filter; test the full security stack with `@SpringBootTest` for authentication tests

---

## Cross-Links

- [[kotlin-spring-android/modules/04_spring-boot-fundamentals]] — Application structure and REST controllers
- [[kotlin-spring-android/modules/05_spring-data-and-persistence]] — User entity and storage
- [[kotlin-spring-android/modules/11_testing-kotlin]] — Security testing with `@WebMvcTest` and `@WithMockUser`

---

## Summary

> - Spring Security's filter chain intercepts every request before it reaches your controllers
> - JWT authentication is the standard approach for stateless REST APIs: issue a short-lived access token and a longer-lived refresh token
> - `@PreAuthorize` with SpEL enables fine-grained method-level authorization without cluttering business logic with security checks
> - CORS must be configured explicitly when your frontend is served from a different origin
> - Always test security configuration — untested security is broken security
