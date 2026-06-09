# Module 09: Android Fundamentals

[← Module 08: Gradle and Build Tooling](../08_gradle-and-build/) | [Topic Home](../../README.md) | [Next → Module 10: Android Advanced](../10_android-advanced/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-12h-orange)

> Android architecture overview, Activities, Fragments, Jetpack Compose basics, Navigation Component, and the Android lifecycle.

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

Android is the world's most widely deployed mobile operating system. Kotlin is its preferred language since Google I/O 2017, and Jetpack Compose is the modern Android UI toolkit that replaced the XML-based View system.

This module teaches the Android fundamentals every Android developer must know: the overall application architecture, the Activity and Fragment lifecycle, Android's permission model, and how to build UIs with Jetpack Compose. The Navigation Component module rounds out the fundamentals by showing how to navigate between screens in a type-safe, declarative way.

> [!NOTE]
> This module is a stub. Full content will be added in a future update.
> See the [Android Developers documentation](https://developer.android.com/docs) while this module is being written.
> You will need Android Studio installed for this module.

---

## Prerequisites

- Modules 01–03: Kotlin language (all three modules)
- Module 08: Gradle and Build Tooling (Android uses Gradle)
- Android Studio installed (download from https://developer.android.com/studio)

---

## Objectives

By the end of this module, you will be able to:

1. Explain Android's application architecture: APK, Activities, Fragments, and the Android manifest
2. Manage the Activity and Fragment lifecycle correctly: handle configuration changes, save and restore state
3. Build UI with Jetpack Compose: composable functions, state, recomposition, layout primitives (`Column`, `Row`, `Box`)
4. Handle user input in Compose: `TextField`, `Button`, `LazyColumn`
5. Request and handle runtime permissions
6. Navigate between screens with the Navigation Component and type-safe arguments
7. Run and debug an app on an emulator and a real device

---

## Theory

> Full theory content coming soon. Topics to be covered:
>
> ### 4.1 Android Architecture Overview
> APK structure, `AndroidManifest.xml`, application components (Activity, Service, BroadcastReceiver, ContentProvider), app entry points.
>
> ### 4.2 Activity and Fragment Lifecycle
> `onCreate`/`onStart`/`onResume`/`onPause`/`onStop`/`onDestroy`, configuration changes, `onSaveInstanceState`.
>
> ### 4.3 Jetpack Compose Fundamentals
> Composable functions, the declarative UI model, recomposition, `remember`, `mutableStateOf`, side effects.
>
> ### 4.4 Compose Layout and UI Components
> `Column`, `Row`, `Box`, `LazyColumn`/`LazyRow`, `Text`, `Button`, `TextField`, `Image`, Modifier.
>
> ### 4.5 Navigation Component
> NavHost, NavController, composable routes, arguments, back stack management, deep links.
>
> ### 4.6 Runtime Permissions
> Permission model, `ActivityResultContracts.RequestPermission`, rationale dialogs.

---

## Key Concepts

- **Activity** — a single focused screen in an Android app; the entry point for user interaction. Modern apps use a single Activity with multiple Compose screens.
- **Composable function** — a function annotated with `@Composable` that describes a piece of UI; Compose re-calls composable functions when their state changes (recomposition).
- **State in Compose** — UI state held in `remember { mutableStateOf(...) }` triggers recomposition when changed; `ViewModel` holds state that survives recomposition.
- **NavController** — manages the navigation back stack; `navController.navigate("route")` pushes a new screen.
- **AndroidManifest.xml** — declares the app's components, permissions, and metadata to the Android OS.

---

## Examples

```kotlin
// Preview: A minimal Jetpack Compose app
@Composable
fun CounterScreen() {
    var count by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(text = "Count: $count", style = MaterialTheme.typography.headlineMedium)

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}

// Preview: Navigation setup
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(onNavigateToDetail = { id -> navController.navigate("detail/$id") })
        }
        composable("detail/{id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id")
            DetailScreen(id = id)
        }
    }
}
```

---

## Common Pitfalls

> - **Memory leaks from context** — storing a reference to `Activity` or `Context` in a long-lived object causes memory leaks; use `applicationContext` for long-lived needs
> - **Ignoring lifecycle** — not unregistering listeners or cancelling coroutines in `onDestroy` leaks resources
> - **State in composables vs ViewModel** — local `remember` state is lost on recomposition-triggered navigation; move persistent state to a `ViewModel`
> - **Modifying state outside the main thread in Compose** — state mutations must happen on the main thread; use `withContext(Dispatchers.Main)` when updating from a background coroutine

---

## Cross-Links

- [[kotlin-spring-android/modules/01_introduction]] — Kotlin basics prerequisite
- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Coroutines used in Android lifecycle-aware code
- [[kotlin-spring-android/modules/10_android-advanced]] — ViewModel, StateFlow, Room, Retrofit, and Hilt build on this module

---

## Summary

> - Android apps are built around Activities (screens) and the Android lifecycle; understanding lifecycle is essential to avoiding memory leaks and crashes
> - Jetpack Compose is the modern Android UI toolkit: composable functions describe UI as a function of state; Compose re-renders when state changes
> - Navigation Component manages the back stack and screen transitions declaratively; use typed arguments to avoid stringly-typed navigation
> - State in Compose lives in `remember { mutableStateOf() }` for local UI state and in `ViewModel` for state that survives recomposition
> - A single-Activity architecture with Compose screens and the Navigation Component is the current recommended Android architecture
