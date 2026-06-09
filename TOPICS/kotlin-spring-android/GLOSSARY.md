# Glossary: Kotlin — Backend Web, Spring Boot, and Android Development

> Key terms and concepts used throughout this topic. Entries are listed alphabetically.
> Cross-linked to relevant modules where the concept is taught in depth.

---

## companion object

A `companion object` is a singleton object declared inside a class using the `companion object` keyword. It provides a place to put factory methods, constants, and utilities that are conceptually associated with the class but do not require an instance. In Java terms, companion object members are similar to `static` members, but Kotlin's companion objects are proper objects that can implement interfaces.

```kotlin
class User(val name: String) {
    companion object {
        fun anonymous() = User("Anonymous")    // factory method
        const val MAX_NAME_LENGTH = 50          // constant
    }
}

val u = User.anonymous()   // called on the class, like Java static
```

See Module 02 for full coverage. See also: [[kotlin-spring-android/modules/02_kotlin-fundamentals]].

---

## coroutine

A coroutine is a suspendable computation — a block of code that can be paused and resumed without blocking a thread. Kotlin's coroutines are implemented as a compiler transformation: the Kotlin compiler rewrites `suspend` functions into state machines that a coroutine dispatcher runs cooperatively. Unlike threads, thousands of coroutines can run on a small thread pool.

```kotlin
// This coroutine pauses at `delay` without blocking the thread
suspend fun fetchData(): String {
    delay(1000)    // non-blocking wait
    return "result"
}
```

See Module 03 for full coverage. See also: **suspend function**, **CoroutineScope**.

---

## data class

A `data class` is a class whose primary purpose is to hold data. The Kotlin compiler automatically generates `equals()`, `hashCode()`, `toString()`, and `copy()` methods based on the constructor parameters. This eliminates several hundred lines of Java boilerplate for what amounts to a value object or DTO.

```kotlin
data class User(val id: Long, val name: String, val email: String)

val u1 = User(1, "Alice", "alice@example.com")
val u2 = u1.copy(email = "newalice@example.com")   // structural copy
println(u1 == u2)  // false — compares by value
```

See Module 02. See also: **sealed class**.

---

## delegation

Delegation in Kotlin refers to two related mechanisms. **Interface delegation** uses the `by` keyword to forward all interface method calls to another object, enabling composition without inheritance. **Property delegation** uses `by` to delegate property get/set logic to a delegate object; the standard library provides `lazy`, `observable`, and `vetoable` delegates.

```kotlin
// Interface delegation: MyList delegates all List<T> calls to innerList
class MyList<T>(private val innerList: MutableList<T> = mutableListOf()) : List<T> by innerList

// Property delegation: computed only on first access
val config: Config by lazy { loadConfigFromDisk() }
```

See Module 03.

---

## DSL (Domain-Specific Language)

A DSL is a mini-language tailored to a specific problem domain. Kotlin enables internal DSLs — type-safe, IDE-supported mini-languages written in Kotlin — through a combination of extension functions, lambda receivers, and operator overloading. Gradle's Kotlin build scripts, Spring's `SecurityDsl`, and Jetpack Compose's UI tree are all Kotlin DSLs.

```kotlin
// A simple HTML DSL using lambda receivers
html {
    head { title("My Page") }
    body { p("Hello, World!") }
}
```

See Module 03 for DSL building. See Module 08 for Gradle Kotlin DSL.

---

## extension function

An extension function adds a new method to an existing class without modifying that class or creating a subclass. The function is defined outside the class, using `ClassName.functionName` syntax. Extension functions are resolved statically at compile time — they are not virtual dispatch.

```kotlin
// Adding a method to String without touching the String class
fun String.isPalindrome(): Boolean = this == this.reversed()

println("racecar".isPalindrome())  // true
println("hello".isPalindrome())    // false
```

See Module 03. Extension functions are used extensively in the Spring Kotlin extensions and Android Jetpack.

---

## gradle task

A Gradle task is a unit of work — a named action that Gradle can execute as part of a build. Tasks have inputs, outputs, and dependencies on other tasks. Gradle models the entire build as a directed acyclic graph (DAG) of tasks. In the Kotlin DSL, tasks are registered and configured using the `tasks` block.

```kotlin
// build.gradle.kts — registering a custom task
tasks.register("hello") {
    doLast {
        println("Hello from a custom Gradle task!")
    }
}
```

See Module 08.

---

## infix function

A function marked with the `infix` keyword can be called without a dot or parentheses, using infix notation. Infix functions must be member functions or extension functions with exactly one parameter. They make certain expressions read more naturally.

```kotlin
infix fun Int.times(str: String) = str.repeat(this)

val result = 3 times "hello "   // "hello hello hello "
```

---

## JVM bytecode

JVM bytecode is the intermediate representation that the Java compiler (javac) and Kotlin compiler (kotlinc) produce. It runs on the Java Virtual Machine — an abstract computing machine that manages memory, garbage collection, and execution. Kotlin compiles to the same bytecode as Java, which is why Kotlin code can call Java libraries and vice versa without any bridging layer.

---

## lambda

A lambda is an anonymous function — a block of code that can be passed as a value, stored in a variable, or returned from a function. In Kotlin, lambdas are the primary mechanism for passing behavior as data. The Kotlin standard library's collection functions (`map`, `filter`, `reduce`) all accept lambdas.

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// Lambda passed to filter
val evens = numbers.filter { n -> n % 2 == 0 }   // [2, 4]

// Lambda with implicit `it` parameter (single-parameter shorthand)
val doubled = numbers.map { it * 2 }              // [2, 4, 6, 8, 10]
```

See Module 02.

---

## null safety

Null safety is Kotlin's type system feature that prevents NullPointerExceptions at compile time by tracking whether a value can be null. Every type in Kotlin is non-nullable by default (`String` cannot be null). Adding `?` makes it nullable (`String?`). The compiler enforces null checks before nullable values are used.

```kotlin
val name: String = "Alice"    // cannot be null — compiler enforces
val nick: String? = null      // can be null

println(name.length)           // safe — name is non-nullable
println(nick?.length)          // safe call — returns null if nick is null
println(nick?.length ?: 0)     // Elvis operator — returns 0 if null
```

See Module 01 for full coverage. This is Kotlin's most important safety feature.

---

## reified type

In generic Kotlin functions marked `inline`, the `reified` keyword allows a type parameter to be accessed at runtime — something not normally possible due to JVM type erasure. Reified type parameters are most useful when you need to check a generic type with `is`, or create instances of a generic type without passing a `Class<T>` parameter.

```kotlin
inline fun <reified T> isInstance(value: Any): Boolean = value is T

println(isInstance<String>("hello"))   // true
println(isInstance<Int>("hello"))      // false
```

See Module 02 (generics) and Module 03 (inline functions).

---

## sealed class

A sealed class is a restricted class hierarchy where all subclasses are defined in the same file (or same package in Kotlin 1.5+). The compiler knows all possible subclasses at compile time, making `when` expressions exhaustive without an `else` branch. Sealed classes are the idiomatic way to model algebraic data types: command patterns, result types, and state machines.

```kotlin
sealed class Result<out T>
data class Success<T>(val data: T) : Result<T>()
data class Error(val message: String) : Result<Nothing>()

fun handle(result: Result<String>) = when (result) {
    is Success -> println("Got: ${result.data}")
    is Error   -> println("Error: ${result.message}")
    // No else needed — compiler knows all cases
}
```

See Module 02.

---

## smart cast

Smart cast is a Kotlin compiler feature that automatically casts a value after a type check, eliminating the need for explicit casting. After `if (x is String)`, the compiler knows `x` is a `String` inside the branch — no `(x as String)` required.

```kotlin
fun describe(x: Any) {
    if (x is String) {
        println(x.length)   // x is automatically cast to String here
    }
    if (x is Int && x > 0) {
        println(x * 2)      // x is automatically cast to Int here
    }
}
```

---

## suspend function

A `suspend` function is a function that can be paused and resumed without blocking the calling thread. Suspend functions can only be called from a coroutine or another suspend function. Under the hood, the Kotlin compiler transforms suspend functions into state machines using continuation-passing style.

```kotlin
suspend fun loadUser(id: Long): User {
    delay(100)                      // non-blocking delay (only works in suspend context)
    return userRepository.find(id)  // may be another suspend call
}
```

See Module 03 (coroutines) and Module 07 (WebFlux reactive programming).
