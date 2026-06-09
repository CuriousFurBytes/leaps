# Module 01: Introduction to Kotlin

[← Topic Home](../../README.md) | [Next → Module 02: Kotlin Fundamentals](../02_kotlin-fundamentals/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-green)
![Time](https://img.shields.io/badge/time-8h-orange)

> Why Kotlin was created, how to set up the environment, Kotlin's null safety system, and the core syntax every Kotlin program uses.

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

This module is your entry point into Kotlin. Before writing a single line of code, you need to understand *why* Kotlin exists — because the design decisions that make Kotlin powerful (null safety, type inference, immutability by default) all flow directly from the problems its creators were trying to solve. A programmer who understands the motivation learns Kotlin's idioms naturally; one who doesn't keeps writing Java syntax in a Kotlin file.

Kotlin was created by JetBrains, the Prague-based company that makes IntelliJ IDEA, to solve real problems their own engineers faced daily: Java's verbosity, the constant threat of NullPointerExceptions, slow evolution of the Java language, and the tedium of writing boilerplate for simple data containers. The result is a language that feels like Java's pragmatic, safety-conscious successor.

By the end of this module you will have Kotlin running on your machine, an understanding of how the JVM executes Kotlin code, mastery of null safety (Kotlin's most important feature), and fluency with the core syntax you will use in every subsequent module.

---

## Prerequisites

- **Basic programming concepts** — variables, functions, conditional logic (`if/else`), loops. Any language (Python, JavaScript, Java) works.
- **Command-line basics** — opening a terminal, running commands, navigating directories.
- No prior Kotlin or Java knowledge required.

> [!TIP]
> If you already know Java, this module will feel fast. The syntax comparisons will resonate immediately. You can move through sections 4.1–4.3 in an hour and spend most of your time on coroutines and idioms from Module 03 onward.

---

## Objectives

By the end of this module, you will be able to:

1. Explain why Kotlin was created and what problems it solves compared to Java
2. Set up a Kotlin development environment with IntelliJ IDEA and Gradle
3. Use Kotlin's null safety features (`?`, `?.`, `?:`, `!!`) to write NPE-free code
4. Write Kotlin programs using `val`/`var`, type inference, string templates, and `when` expressions
5. Define and call functions with default parameters and named arguments
6. Describe how Kotlin code is compiled to JVM bytecode and why Java interoperability works
7. Run a complete Kotlin program from scratch and read its output

---

## Theory

### 4.1 Why Kotlin Was Created

JetBrains began Project Kotlin in 2010. At the time, their engineers were writing large-scale Java applications — the IntelliJ IDEA codebase alone exceeded 10 million lines of Java. The frustrations accumulated:

**Java verbosity.** A simple data container in Java required writing a class, a constructor, `equals()`, `hashCode()`, `toString()`, and getters/setters — fifty lines for something that should take five. Every experienced Java developer had either memorized the boilerplate or relied on IDE code generation. Neither is satisfying.

**NullPointerExceptions.** Tony Hoare, who invented the null reference in ALGOL in 1965, called it "my billion-dollar mistake." Java's type system cannot distinguish "this variable holds a String" from "this variable might hold a String or might be null." The result: developers write `if (x != null)` defensively everywhere, or they forget and encounter a `NullPointerException` in production.

**Slow language evolution.** Java's famously careful backward-compatibility policy means new features take many years to reach stable form. JetBrains needed a language that could evolve faster.

**Scala was too complex.** JetBrains evaluated Scala as an alternative. Scala's type system and compilation times (sometimes minutes for large codebases) made it impractical for their use case.

The Kotlin design goals were explicit and constrained:

1. **100% Java interoperability** — Kotlin must call any Java library, and Java code must call Kotlin code. This was non-negotiable; JetBrains could not rewrite millions of lines of Java.
2. **Compile as fast as Java** — not Scala's compile times.
3. **Null safety at the type level** — not as an annotation or convention, but enforced by the compiler.
4. **Expressiveness with pragmatism** — concise code without Haskell-level type theory.

Kotlin 1.0 shipped in February 2016. In May 2017, at Google I/O, the Android team announced first-class Kotlin support — the single event that made Kotlin's adoption exponential.

---

### 4.2 Setting Up the Kotlin Environment

You need three things: a JDK, IntelliJ IDEA, and optionally Gradle.

**Install a JDK.** Kotlin targets JVM 8 or higher; use JVM 17 or 21 for new projects (both are Long-Term Support releases). Install via your system package manager, or use SDKMAN!:

```bash
# Install SDKMAN! (macOS/Linux)
curl -s "https://get.sdkman.io" | bash

# Install Java 21 (LTS)
sdk install java 21.0.3-tem

# Verify
java -version
```

**Install IntelliJ IDEA.** Download the free Community Edition from https://www.jetbrains.com/idea/download/. IntelliJ IDEA has built-in Kotlin support — no additional plugin needed.

**Create your first Kotlin project.** In IntelliJ IDEA: File → New Project → Kotlin → JVM | IDEA. This creates the minimal structure: a `src/` directory and a `Main.kt` file.

For a Gradle-based project (used in all subsequent modules), choose "Kotlin | Gradle" and select "Kotlin DSL" as the Gradle script language. The generated project has this structure:

```
my-project/
├── build.gradle.kts       ← Gradle build script (Kotlin DSL)
├── settings.gradle.kts    ← Project name and included subprojects
├── gradle/
│   └── wrapper/           ← Gradle wrapper (use this; avoids global Gradle install)
└── src/
    ├── main/
    │   └── kotlin/
    │       └── Main.kt    ← Your Kotlin source files go here
    └── test/
        └── kotlin/        ← Test files go here
```

**Run Kotlin interactively.** For quick experiments, use the Kotlin REPL (Read-Eval-Print Loop):

```bash
# From IntelliJ IDEA: Tools → Kotlin → Kotlin REPL
# Or from command line after installing Kotlin:
kotlinc -script   # starts interactive REPL
```

Or use the browser-based [Kotlin Playground](https://play.kotlinlang.org) — no installation needed.

**How the JVM runs Kotlin.** When you write Kotlin and press "Run", this happens:

```
Kotlin source (.kt)
       ↓
Kotlin compiler (kotlinc)
       ↓
JVM bytecode (.class files)
       ↓
Java Virtual Machine (JVM)
       ↓
Native machine code (JIT compiled at runtime)
```

The JVM bytecode is identical in structure to what `javac` (the Java compiler) produces. This is why a Java library written in 2010 works perfectly in a Kotlin project: both compile to the same bytecode, and the JVM does not know or care which language produced it.

---

### 4.3 Kotlin vs Java: Key Differences

The fastest way to understand Kotlin's design is to see it next to Java. Here are the five most important differences.

**1. Null safety — the type system distinguishes nullable from non-nullable.**

```java
// Java: any reference can be null — compiler cannot tell you
String name = "Alice";
String nickname = null;   // perfectly valid; same type as name
int len = nickname.length();  // compiles fine, crashes at runtime: NullPointerException
```

```kotlin
// Kotlin: the TYPE tells you whether null is possible
val name: String = "Alice"      // cannot be null — compiler rejects: name = null
val nickname: String? = null    // explicitly nullable with the ? suffix

// Using a nullable value requires explicit handling
val len: Int? = nickname?.length   // safe call — returns null instead of crashing
val len2: Int = nickname?.length ?: 0  // Elvis: use 0 if null
```

**2. Type inference — you rarely need to write types explicitly.**

```java
// Java: types must be stated in most places
Map<String, List<Integer>> map = new HashMap<String, List<Integer>>();
```

```kotlin
// Kotlin: compiler infers types from context
val map = HashMap<String, List<Int>>()  // type inferred from constructor call
val items = listOf(1, 2, 3)             // List<Int> inferred from contents
```

**3. Data classes eliminate boilerplate.**

```java
// Java: a "value object" requires ~40 lines
public class User {
    private final String name;
    private final int age;
    public User(String name, int age) { this.name = name; this.age = age; }
    public String getName() { return name; }
    public int getAge() { return age; }
    @Override public boolean equals(Object o) { /* ... */ }
    @Override public int hashCode() { /* ... */ }
    @Override public String toString() { /* ... */ }
}
```

```kotlin
// Kotlin: one line; equals/hashCode/toString/copy generated automatically
data class User(val name: String, val age: Int)
```

**4. Extension functions — add methods to existing classes.**

```kotlin
// Add a method to String without subclassing or wrapping it
fun String.isPalindrome(): Boolean = this == this.reversed()

println("racecar".isPalindrome())   // true
println("hello".isPalindrome())     // false
```

**5. `when` replaces `switch` — exhaustive, expression-based.**

```kotlin
val grade = when (score) {
    in 90..100 -> "A"
    in 80..89  -> "B"
    in 70..79  -> "C"
    else       -> "F"
}

// On sealed classes, when is exhaustive without else
val message = when (result) {
    is Success -> "Got: ${result.data}"
    is Error   -> "Failed: ${result.message}"
    // No else needed — compiler ensures all cases covered
}
```

---

### 4.4 Null Safety: Kotlin's Most Important Feature

Null safety is not a minor convenience — it fundamentally changes how you design code. Understanding it deeply in Module 01 prevents an entire class of bugs for the rest of your Kotlin career.

**The type system distinguishes nullable from non-nullable.** Every type in Kotlin comes in two forms:

| Form | Syntax | Means |
|------|--------|-------|
| Non-nullable | `String` | This value is always a String. Never null. |
| Nullable | `String?` | This value is either a String or null. |

The Kotlin compiler tracks which type each variable has and refuses to compile code that could cause an NPE:

```kotlin
val city: String = "Prague"
val country: String? = null

// This compiles — city is non-nullable
println(city.length)

// This does NOT compile — country might be null
// println(country.length)  // ERROR: Only safe (?.) or non-null asserted (!!) calls allowed

// Safe call — returns null instead of throwing
println(country?.length)   // prints: null

// Elvis operator — provide a fallback when null
val len = country?.length ?: 0   // len = 0
```

**The four null safety operators.** You will use all four. Learn them now:

```kotlin
// 1. Safe call operator ?.
// Returns null instead of throwing if the left side is null
val upper = nickname?.uppercase()    // String? — could be null

// 2. Elvis operator ?:
// Returns the right side when the left side is null
val display = nickname ?: "Anonymous"   // String — never null

// 3. Non-null assertion !!
// Throws NullPointerException if null — a deliberate "I know this isn't null"
val forced = nickname!!.uppercase()    // String — throws if null

// 4. Safe cast as?
// Returns null if the cast fails, instead of throwing ClassCastException
val n = someValue as? Int    // Int? — null if someValue is not an Int
```

> [!WARNING]
> The non-null assertion `!!` is a code smell in most cases. If you find yourself using it frequently, it means your code's flow isn't communicating null handling clearly. Restrict `!!` to the rare situations where you have external knowledge that the compiler can't infer.

**`let` for null-safe blocks.** The `let` scope function runs a block only when the value is non-null:

```kotlin
val email: String? = getUserEmail()

// Only executes if email is non-null
email?.let { validEmail ->
    sendWelcomeEmail(validEmail)   // validEmail: String (non-nullable inside let)
}
```

---

### 4.5 Basic Kotlin Syntax

**Variables: `val` vs `var`.**

```kotlin
val pi = 3.14159       // immutable — cannot be reassigned
var count = 0          // mutable — can be reassigned
count = count + 1      // OK
// pi = 3.14           // ERROR: Val cannot be reassigned

// Type can be explicit or inferred
val name: String = "Alice"   // explicit type
val name2 = "Alice"          // inferred — same as above
```

The convention in Kotlin is to use `val` by default and only reach for `var` when you genuinely need reassignment. This makes code easier to reason about.

**String templates.** Kotlin string templates embed expressions directly in strings using `$`:

```kotlin
val name = "Alice"
val age = 30

// Simple variable
println("Hello, $name!")                    // Hello, Alice!

// Expression (any expression, not just variables)
println("Next year you'll be ${age + 1}")   // Next year you'll be 31
println("Name has ${name.length} chars")    // Name has 5 chars

// Raw strings (triple-quoted) — no escape sequences needed
val json = """
    {
        "name": "$name",
        "age": $age
    }
""".trimIndent()
```

**`when` expression.** `when` replaces Java's `switch` but is far more powerful — it's an expression (returns a value), works with any type, and supports ranges and conditions:

```kotlin
val score = 85

val grade = when {
    score >= 90 -> "A"
    score >= 80 -> "B"
    score >= 70 -> "C"
    else        -> "F"
}
println(grade)  // B

// when with a value
val day = when (dayOfWeek) {
    1 -> "Monday"
    2 -> "Tuesday"
    6, 7 -> "Weekend"   // multiple values separated by comma
    else -> "Weekday"
}

// when with type checks (smart cast)
fun describe(x: Any) = when (x) {
    is String -> "String of length ${x.length}"   // x smart-cast to String
    is Int    -> "Integer: $x"
    else      -> "Unknown"
}
```

**Ranges.**

```kotlin
val oneToTen = 1..10        // IntRange: 1, 2, ..., 10 (inclusive)
val oneToNine = 1 until 10  // IntRange: 1, 2, ..., 9 (exclusive end)

for (i in 1..5) print("$i ")   // 1 2 3 4 5

// Check containment
if (score in 80..89) println("B grade")

// Downward range
for (i in 5 downTo 1) print("$i ")  // 5 4 3 2 1
for (i in 0..10 step 2) print("$i ")  // 0 2 4 6 8 10
```

---

### 4.6 Functions in Kotlin

Kotlin functions are first-class — they can be stored in variables, passed as arguments, and returned from other functions.

```kotlin
// Standard function declaration
fun add(a: Int, b: Int): Int {
    return a + b
}

// Single-expression function — the return type is inferred
fun add(a: Int, b: Int) = a + b

// Default parameter values
fun greet(name: String, greeting: String = "Hello") = "$greeting, $name!"

greet("Alice")                  // Hello, Alice!
greet("Bob", "Hi")              // Hi, Bob!
greet(greeting = "Hey", name = "Carol")  // Hey, Carol! (named arguments)

// Unit return type (equivalent to Java's void)
fun printInfo(message: String): Unit {
    println(message)
}
// Unit is usually omitted
fun printInfo2(message: String) {
    println(message)
}

// Variable number of arguments (vararg)
fun sum(vararg numbers: Int): Int = numbers.sum()
sum(1, 2, 3, 4, 5)   // 15
```

**Local functions** — functions defined inside other functions:

```kotlin
fun processOrder(orderId: Long) {
    // Local function — visible only inside processOrder
    fun validate(id: Long) {
        require(id > 0) { "Order ID must be positive" }
    }

    validate(orderId)
    // ... rest of processing
}
```

**Lambda expressions** — anonymous functions used as values:

```kotlin
// Full syntax
val double: (Int) -> Int = { n: Int -> n * 2 }

// Inferred parameter type
val double2: (Int) -> Int = { n -> n * 2 }

// `it` — implicit parameter name when there's exactly one parameter
val double3: (Int) -> Int = { it * 2 }

// Passing a lambda to a function (trailing lambda syntax)
val numbers = listOf(1, 2, 3, 4, 5)
val evens = numbers.filter { it % 2 == 0 }  // lambda passed as last argument
```

---

### 4.7 Your First Kotlin Program: From "Hello World" to Data Processing

Every language starts with "Hello, World!" — but that teaches you nothing interesting. Here's a progression from trivial to actually useful:

```kotlin
// Step 1: Hello, World!
fun main() {
    println("Hello, World!")
}
```

```kotlin
// Step 2: Hello with null safety — reading from an environment variable
fun main() {
    // System.getenv returns String? in Kotlin (it can return null)
    val name: String? = System.getenv("USER_NAME")

    // Use the Elvis operator to provide a default
    val greeting = "Hello, ${name ?: "World"}!"
    println(greeting)
}
```

```kotlin
// Step 3: Data processing — reading numbers and computing statistics
fun main() {
    val numbers = listOf(42, 17, 93, 55, 28, 71, 36, 89, 12, 64)

    val stats = computeStats(numbers)
    println("Count:   ${stats.count}")
    println("Sum:     ${stats.sum}")
    println("Average: ${"%.2f".format(stats.average)}")
    println("Min:     ${stats.min}")
    println("Max:     ${stats.max}")
}

// A data class to hold the results — equals/toString/hashCode generated automatically
data class Stats(
    val count: Int,
    val sum: Int,
    val average: Double,
    val min: Int,
    val max: Int
)

fun computeStats(numbers: List<Int>): Stats {
    require(numbers.isNotEmpty()) { "Cannot compute stats for empty list" }

    return Stats(
        count   = numbers.size,
        sum     = numbers.sum(),
        average = numbers.average(),
        min     = numbers.min(),
        max     = numbers.max()
    )
}
```

Output:

```
Count:   10
Sum:     507
Average: 50.70
Min:     12
Max:     93
```

This tiny program uses `data class`, named arguments, string templates, type inference, the `require` precondition check, and standard library functions — all of which are idiomatic Kotlin that you will use constantly.

---

## Key Concepts

**Null Safety** — Kotlin's type system tracks whether values can be null at compile time. Non-nullable types (`String`) can never hold null; nullable types (`String?`) require explicit null handling before use. This prevents NullPointerExceptions by construction. See [[kotlin-spring-android/modules/01_introduction#theory]] and [[shared/glossary#null-safety]].

**`val` vs `var`** — `val` declares an immutable reference (cannot be reassigned after initialization); `var` declares a mutable one. The Kotlin convention is `val` by default, `var` only when you need reassignment. Note: `val` makes the *reference* immutable, not the object the reference points to — a `val list: MutableList<Int>` cannot be reassigned to a different list, but you can still `list.add(1)`.

**Type Inference** — The Kotlin compiler deduces types from context. `val x = 42` is `Int`; `val items = listOf("a", "b")` is `List<String>`. This reduces boilerplate without sacrificing type safety. Types are still checked at compile time; they are simply not *written* everywhere.

**String Templates** — Expressions can be embedded directly in string literals with `$variable` or `${expression}`. This is cleaner than Java's string concatenation or `String.format()`.

**`when` Expression** — A pattern-matching construct that can match values, ranges, types, and conditions. Unlike Java's `switch`, `when` is an expression (it returns a value), handles non-integer types, and is exhaustive when used with sealed classes.

**Extension Functions** — New methods can be added to existing types without subclassing. `fun String.isPalindrome()` adds `isPalindrome()` to every `String`. Extensions are resolved statically — they are syntactic sugar for static utility functions. See [[kotlin-spring-android#extension-function]].

**JVM Bytecode** — Kotlin compiles to the same bytecode format as Java. The JVM executes this bytecode, JIT-compiling hot paths to native machine code. This is why Kotlin code and Java code can coexist in the same project and call each other freely. See [[kotlin-spring-android#jvm-bytecode]].

---

## Examples

### Example 1: Safe null-handling pipeline

**Scenario:** You have a user input that might be blank. Parse it as a number, double it, and return a message.

```kotlin
fun processInput(input: String?): String {
    // Step 1: handle null input — return early
    val trimmed = input?.trim() ?: return "No input provided"

    // Step 2: handle blank input
    if (trimmed.isBlank()) return "Input was empty"

    // Step 3: parse as Int safely (toIntOrNull returns null on failure)
    val number = trimmed.toIntOrNull() ?: return "Not a valid number: $trimmed"

    // Step 4: compute result — at this point number is non-nullable Int
    return "Result: ${number * 2}"
}

fun main() {
    println(processInput(null))      // No input provided
    println(processInput("   "))     // Input was empty
    println(processInput("hello"))   // Not a valid number: hello
    println(processInput("21"))      // Result: 42
}
```

**Approach explanation:** This uses the "early return" pattern with `?: return` — each step validates the input and returns early with an error message if validation fails. By the time we reach step 4, the type system guarantees `number` is a non-null `Int`. No null checks needed at the computation step.

---

### Example 2: Data class with when for modeling states

**Scenario:** Model the result of a network request that can succeed, fail, or be in progress.

```kotlin
// Sealed class hierarchy — the compiler knows all possible states
sealed class NetworkResult<out T>
data class Success<T>(val data: T) : NetworkResult<T>()
data class Failure(val errorCode: Int, val message: String) : NetworkResult<Nothing>()
object Loading : NetworkResult<Nothing>()

fun handleResult(result: NetworkResult<String>) {
    // when is exhaustive — no else needed because all cases are covered
    val message = when (result) {
        is Success -> "Data received: ${result.data}"         // smart cast to Success
        is Failure -> "Error ${result.errorCode}: ${result.message}"  // smart cast to Failure
        is Loading -> "Please wait..."
    }
    println(message)
}

fun main() {
    handleResult(Success("User data loaded"))
    handleResult(Failure(404, "Not found"))
    handleResult(Loading)
}
```

Output:

```
Data received: User data loaded
Error 404: Not found
Please wait...
```

**Approach explanation:** The `sealed class` hierarchy with `data class` variants gives you type-safe state modeling. The `when` expression is exhaustive — if you add a new subclass later and forget to handle it, the compiler will catch it immediately.

---

### Example 3: Extension functions and string manipulation

**Scenario:** Write several useful string utilities as extension functions on `String`.

```kotlin
// Extension functions — add methods to String without modifying it
fun String.isPalindrome(): Boolean =
    this.lowercase().filter { it.isLetter() } == this.lowercase().filter { it.isLetter() }.reversed()

fun String.words(): List<String> = this.trim().split(Regex("\\s+")).filter { it.isNotEmpty() }

fun String.titleCase(): String =
    words().joinToString(" ") { word ->
        word.lowercase().replaceFirstChar { it.uppercase() }
    }

fun String.truncate(maxLength: Int, suffix: String = "..."): String =
    if (this.length <= maxLength) this
    else this.take(maxLength - suffix.length) + suffix

fun main() {
    println("A man a plan a canal Panama".isPalindrome())   // true
    println("  hello   world   foo  ".words())             // [hello, world, foo]
    println("the quick brown fox".titleCase())              // The Quick Brown Fox
    println("Hello, World!".truncate(8))                    // Hello...
    println("Hi".truncate(8))                               // Hi
}
```

**Approach explanation:** Extension functions are one of Kotlin's most elegant features. They make calling code read naturally (`"text".titleCase()` vs `StringUtils.titleCase("text")`) while keeping the implementation cleanly separated. The compiler desugars them to static utility calls — there's no runtime overhead.

---

## Common Pitfalls

### Pitfall 1: Using `!!` (non-null assertion) excessively

The non-null assertion `!!` throws `NullPointerException` if the value is null. Using it carelessly recreates the exact problem Kotlin's null safety is designed to prevent.

**Wrong:**

```kotlin
// This crashes if user.email is null — same as Java NPE
fun sendEmail(user: User) {
    val email = user.email!!      // throws if null
    emailService.send(email)
}
```

**Right:**

```kotlin
// Handle the null case explicitly
fun sendEmail(user: User) {
    val email = user.email ?: run {
        logger.warn("User ${user.id} has no email")
        return
    }
    emailService.send(email)     // email: String (non-nullable here)
}
```

**Why this mistake is made:** Developers migrating from Java or new to Kotlin use `!!` to silence compiler errors without understanding what they mean. The compiler error is the system telling you "this might be null — what do you want to do?" Answering that question with `!!` defers the problem to runtime.

---

### Pitfall 2: Misunderstanding `val` with mutable objects

`val` means the *reference* cannot be reassigned — not that the object itself is immutable.

**Wrong (common confusion):**

```kotlin
val list = mutableListOf(1, 2, 3)
list = mutableListOf(4, 5, 6)   // ERROR: Val cannot be reassigned ← correctly caught
```

**This compiles and runs — but surprises beginners:**

```kotlin
val list = mutableListOf(1, 2, 3)
list.add(4)        // LEGAL — we're not reassigning the reference, just mutating
println(list)      // [1, 2, 3, 4]
```

**Right (prefer immutable collections):**

```kotlin
val list = listOf(1, 2, 3)      // read-only view — no add/remove methods
// list.add(4)                   // ERROR: Unresolved reference: add
val newList = list + 4           // creates a NEW list — list is unchanged
```

**Why this matters:** If you intend a collection to be immutable, use `listOf`, `setOf`, `mapOf` — not `mutableListOf`. This communicates your intent and prevents accidental mutation.

---

### Pitfall 3: Java interop — `@Nullable` and `@NotNull` vs Kotlin types

When you call Java code from Kotlin, Java types have no null information in the Kotlin type system (they are "platform types"). The compiler cannot warn you about potential null values from Java APIs.

**Wrong:**

```kotlin
// Java's String.getenv returns @Nullable String — Kotlin treats it as String! (platform type)
val path = System.getenv("PATH")   // String! (platform type — may or may not be null)
println(path.length)               // Compiles — but crashes if PATH isn't set
```

**Right:**

```kotlin
// Treat Java API return values as nullable when there's any doubt
val path: String? = System.getenv("PATH")   // explicitly nullable
println(path?.length ?: "PATH not set")
```

**Why this matters:** Platform types (`String!`) give you the same lack of safety as Java. When calling Java APIs, always check the Java documentation for `@Nullable`/`@NotNull` annotations, or treat the value as nullable to be safe.

---

### Pitfall 4: `when` without `else` on non-sealed types

`when` is only exhaustive (compiler-enforced to cover all cases) when used with sealed classes. For regular types, forgetting `else` means some cases are silently unhandled.

**Wrong:**

```kotlin
fun describe(n: Int): String = when (n) {
    1 -> "one"
    2 -> "two"
    // No else — if n is 3, the when expression returns Unit, not a String
    // This is a compile error when used as an expression — but easy to miss
}
```

**Right:**

```kotlin
fun describe(n: Int): String = when (n) {
    1 -> "one"
    2 -> "two"
    else -> "many"    // always required for non-sealed types used as expressions
}
```

---

## Cross-Links

- [[kotlin-spring-android]] — Topic home; module map and overview
- [[kotlin-spring-android/modules/02_kotlin-fundamentals]] — Next module: OOP, data classes, sealed classes, and collections
- [[kotlin-spring-android/modules/03_kotlin-advanced]] — Coroutines and extension functions build on the syntax introduced here
- [[graphql-rest]] — REST API concepts that Spring Boot (Module 04) applies; understanding HTTP is a useful parallel read
- [[postgresql]] — The database used in Module 05; null safety concepts apply to nullable database columns

---

## Summary

- **Kotlin was created by JetBrains** in 2010, reached 1.0 in 2016, and became Google's preferred Android language in 2017. The primary motivations: eliminate NullPointerExceptions, reduce boilerplate, improve expressiveness while keeping 100% Java interoperability.
- **Kotlin compiles to JVM bytecode**, the same format as Java. This is why Kotlin and Java can coexist in the same codebase and call each other freely — the JVM cannot distinguish which language produced the bytecode.
- **Null safety is the most important Kotlin feature.** Every type is either non-nullable (`String`) or nullable (`String?`). The compiler enforces null handling at every point where a nullable value might be used. The four null safety operators are: `?.` (safe call), `?:` (Elvis/default), `!!` (non-null assertion — use sparingly), and `as?` (safe cast).
- **`val` is immutable by reference, `var` is mutable.** Prefer `val` by default. `val` on a collection does not prevent mutation of the collection — use `listOf`/`setOf`/`mapOf` for read-only collections.
- **Type inference** eliminates most type annotations. The Kotlin compiler deduces types from context; you only need explicit types at function signatures and when clarity demands it.
- **String templates** (`"Hello, $name!"` and `"${expression}"`) are cleaner than Java string concatenation.
- **`when` expressions** replace Java's `switch` and are more powerful: they work with any type, support ranges and conditions, return a value, and are exhaustive on sealed classes.
- **Functions support default parameters and named arguments**, eliminating most Java-style overloading boilerplate.
- **Extension functions** add methods to existing types without subclassing — a pattern used everywhere in Kotlin standard library and frameworks.
