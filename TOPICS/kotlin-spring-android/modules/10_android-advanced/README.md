# Module 10: Android Advanced

[← Module 09: Android Fundamentals](../09_android-fundamentals/) | [Topic Home](../../README.md) | [Next → Module 11: Testing in Kotlin](../11_testing-kotlin/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-12h-orange)

> ViewModel, LiveData/StateFlow, Room database, Retrofit + OkHttp networking, Hilt dependency injection, and Material You/Material3.

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

Module 09 taught you how to build screens and navigate between them. Module 10 adds the production-grade architecture on top: **ViewModel** for lifecycle-aware state management, **Room** for local database persistence, **Retrofit** for HTTP networking, **Hilt** for dependency injection, and **Material3** for modern Android design.

Together, these libraries constitute the "Android Jetpack" stack — Google's recommended architecture for production Android apps. By the end of this module, you have all the tools to build a full, production-ready Android application that fetches data from a REST API, caches it locally, and presents it with Material3 design.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> See the [Android Architecture documentation](https://developer.android.com/topic/architecture) while this module is being written.

---

## Prerequisites

- Module 09: Android Fundamentals
- Module 03: Kotlin Advanced (coroutines and Flow)

---

## Objectives

By the end of this module, you will be able to:

1. Implement ViewModel with `StateFlow` for lifecycle-aware state management
2. Design a Room database schema with entities, DAOs, and the database class
3. Perform network requests with Retrofit and OkHttp, with proper error handling
4. Inject dependencies with Hilt: `@HiltViewModel`, `@Inject`, modules, and component scopes
5. Implement the Repository pattern to abstract local (Room) and remote (Retrofit) data sources
6. Apply Material3 design: themes, typography, color schemes, and Material3 components
7. Implement offline-first architecture: show cached data while fetching fresh data from the network

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 ViewModel and StateFlow
> `ViewModel` lifecycle, `viewModelScope`, `MutableStateFlow`, `StateFlow`, collecting in Compose with `collectAsStateWithLifecycle`.
>
> ### 4.2 Room Database
> `@Database`, `@Entity`, `@Dao`, type converters, migrations, Flow queries from DAO.
>
> ### 4.3 Retrofit and OkHttp
> Service interfaces with `@GET`/`@POST`, OkHttp interceptors, authentication header injection, error handling, JSON parsing with Moshi/Gson.
>
> ### 4.4 Hilt Dependency Injection
> `@HiltAndroidApp`, `@HiltViewModel`, `@Inject`, `@Module`, `@Provides`, `@Singleton`, `@ViewModelScoped`.
>
> ### 4.5 Repository Pattern
> Abstracting local (Room) and remote (Retrofit) data sources behind a Repository interface; single source of truth.
>
> ### 4.6 Offline-First Architecture
> Fetch from local → show immediately → fetch from network → update local → emit to UI.
>
> ### 4.7 Material3
> `MaterialTheme`, dynamic color (Android 12+), `colorScheme`, typography, `TopAppBar`, `BottomNavigationBar`, `FloatingActionButton`.

---

## Key Concepts

- **ViewModel** — a lifecycle-aware holder for UI state; survives configuration changes (screen rotation); scoped to a screen's lifecycle.
- **StateFlow** — a hot observable flow that always holds the latest value; the replacement for LiveData in Kotlin coroutine-based apps.
- **Room** — Google's SQLite abstraction library; provides compile-time verification of SQL queries, DAO interfaces, and coroutine support.
- **Retrofit** — a type-safe HTTP client; you define a Kotlin interface with annotations and Retrofit generates the implementation.
- **Hilt** — Google's Android dependency injection framework built on top of Dagger; provides Android-specific DI components for Activity, Fragment, and ViewModel scopes.

---

## Examples

```kotlin
// Preview: ViewModel with StateFlow
@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val repository: ProductRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState<List<Product>>>(UiState.Loading)
    val uiState: StateFlow<UiState<List<Product>>> = _uiState.asStateFlow()

    init {
        loadProducts()
    }

    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            repository.getProducts()
                .catch { e -> _uiState.value = UiState.Error(e.message ?: "Unknown error") }
                .collect { products -> _uiState.value = UiState.Success(products) }
        }
    }
}

// Preview: Retrofit service
interface ProductApiService {
    @GET("api/products")
    suspend fun getProducts(@Query("page") page: Int = 0): List<ProductDto>

    @POST("api/products")
    suspend fun createProduct(@Body request: CreateProductRequest): ProductDto
}

// Preview: Room DAO
@Dao
interface ProductDao {
    @Query("SELECT * FROM products ORDER BY name")
    fun observeAll(): Flow<List<ProductEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(products: List<ProductEntity>)
}
```

---

## Common Pitfalls

> - **Using LiveData instead of StateFlow** — prefer `StateFlow` for new code; `LiveData` is lifecycle-aware but not coroutine-native; `StateFlow` integrates naturally with coroutines
> - **Calling `collect` in a coroutine not tied to the lifecycle** — in Compose, always use `collectAsStateWithLifecycle()` or `lifecycleScope.launch { repeatOnLifecycle(STARTED) { ... } }` to avoid collecting when the screen is in the background
> - **Exposing `MutableStateFlow` from ViewModel** — expose only `StateFlow` (the read-only interface) to the UI; keep `MutableStateFlow` private
> - **Not using Room's coroutine support** — Room's `Flow`-returning DAO methods automatically emit updates when the table changes; use them instead of polling

---

## Cross-Links

- [[kotlin-spring-android/modules/09_android-fundamentals]] — Compose, Navigation, and Activity lifecycle prerequisite
- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Coroutines and Flow prerequisite for ViewModel/StateFlow patterns
- [[kotlin-spring-android/modules/11_testing-kotlin]] — Testing Room DAOs, Retrofit, and ViewModels with Hilt

---

## Summary

> - ViewModel holds UI state and survives configuration changes; use `viewModelScope` for coroutines and `StateFlow` for observable state
> - Room provides type-safe SQLite access with DAO interfaces; `Flow`-returning queries automatically emit updates
> - Retrofit turns a Kotlin interface into an HTTP client; pair it with OkHttp interceptors for authentication headers and logging
> - Hilt provides Android-aware dependency injection; `@HiltViewModel` injects into ViewModels; `@Singleton` for shared repository instances
> - The Repository pattern — abstracting Room and Retrofit behind an interface — enables offline-first architecture and simplifies testing
