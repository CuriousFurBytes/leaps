# Exercises: Module 12 — Capstone Project

## Instructions

Complete each exercise in order. Exercises increase in difficulty. Submit answers by editing this file or committing a separate solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Explain the module's core purpose.

Write a five-sentence explanation of why **Capstone Project** matters for Kotlin backend and Android work.

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Run or reason about a minimal Kotlin example.

```kotlin
fun main() {
    println("Capstone Project")
}
```

Annotate each line and describe how you would run it in a local Kotlin project.

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Identify platform boundaries.

List three responsibilities that belong on a backend and three responsibilities that belong in an Android app.

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Design a small model.

Create a Kotlin `data class` for a learning task and explain which fields are safe to share between backend and Android.

---

### Exercise 5
**Difficulty:** Medium
**Objective:** Compare tool choices.

Write a short comparison of Gradle and Maven for this module's context.

---

### Exercise 6
**Difficulty:** Medium
**Objective:** Practice error thinking.

Describe two realistic failure modes and how you would surface them to a learner or user.

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Write runnable Kotlin.

```kotlin
data class Task(val title: String, val done: Boolean)

fun incompleteTitles(tasks: List<Task>): List<String> {
    TODO("return titles for incomplete tasks only")
}
```

Implement the function and add two example inputs.

---

### Exercise 8
**Difficulty:** Hard
**Objective:** Debug a realistic mistake.

Find the risk in this code and rewrite it safely:

```kotlin
fun displayName(name: String?): String = name!!.trim()
```

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize architecture and implementation.

Sketch a two-module or three-module project layout that supports Spring backend code, Android app code, and shared Kotlin contracts. Explain the dependency direction and why it prevents coupling mistakes.
