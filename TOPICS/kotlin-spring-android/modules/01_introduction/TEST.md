# Test: Module 01 — Introduction to Kotlin

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What does the `?` suffix on a type (e.g., `String?`) signify in Kotlin?

> Answer:

---

**Q2.** What is the difference between `val` and `var` in Kotlin?

> Answer:

---

**Q3.** What year did Google announce first-class Kotlin support for Android, and at which event?

> Answer:

---

**Q4.** What operator would you use to provide a default value when a nullable expression evaluates to null?

> Answer:

---

**Q5.** True or false: Kotlin requires semicolons at the end of statements. Explain.

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain what a "platform type" (`String!`) is in Kotlin and in what situation it appears. Why is it potentially dangerous?

> Answer:

---

**Q7.** What is the difference between these two declarations? When would you choose each?

```kotlin
val list = listOf(1, 2, 3)
val mList = mutableListOf(1, 2, 3)
```

> Answer:

---

**Q8.** Explain why Kotlin code can call Java libraries without any special bridge or wrapper layer.

> Answer:

---

**Q9.** What is a single-expression function in Kotlin? Rewrite the following as a single-expression function:

```kotlin
fun square(n: Int): Int {
    return n * n
}
```

> Answer:

---

**Q10.** Compare Kotlin's `when` expression to Java's `switch` statement. List at least three differences.

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Find and fix the bug(s) in this code:

```kotlin
fun getLength(text: String?): Int {
    return text!!.trim().length
}

fun main() {
    println(getLength(null))     // should print 0
    println(getLength("  hi  ")) // should print 2
}
```

Write the corrected version and explain what was wrong.

> Answer:

---

**Q12.** Write a Kotlin function `safeDiv(a: Int, b: Int): Int?` that:
- Returns `a / b` when `b` is not zero
- Returns `null` when `b` is zero

Then write a function `printDivision(a: Int, b: Int)` that calls `safeDiv` and prints either the result or `"Division by zero"` using a single expression (no `if` statement — use the Elvis operator or `let`).

> Answer:

---

**Q13.** Given this sealed class hierarchy:

```kotlin
sealed class Shape
data class Circle(val radius: Double) : Shape()
data class Rectangle(val width: Double, val height: Double) : Shape()
data class Triangle(val base: Double, val height: Double) : Shape()
```

Write a function `area(shape: Shape): Double` that computes the area of each shape. Use a `when` expression and make it exhaustive (no `else` branch). Then explain why removing `is Triangle -> ...` would cause a compile error.

> Answer:

---

**Q14.** Write a Kotlin function `buildUserSummary(name: String?, age: Int?, city: String?): String` that returns a string summarizing a user, gracefully handling all combinations of null parameters. Examples:
- All present: `"Alice, 30, from Prague"`
- Name only: `"Alice"`
- Name and city: `"Alice, from Prague"`
- All null: `"Anonymous user"`

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** A Java library's method is declared as:

```java
public class UserService {
    @Nullable
    public String findEmail(long userId) { /* ... */ }
}
```

A Kotlin developer writes:

```kotlin
fun notifyUser(userId: Long) {
    val email = userService.findEmail(userId)
    sendEmail(email.uppercase())   // crashes in production
}
```

Explain precisely why this crashes, what Kotlin's platform type system has to do with it, and rewrite `notifyUser` so it handles null correctly with appropriate logging.

> Answer:

---

**Q16.** Design a `Result<T>` type from scratch in Kotlin. It must:
1. Be a sealed class with two subclasses: `Ok<T>` (holds a value) and `Err` (holds an exception)
2. Have an extension function `Result<T>.getOrDefault(default: T): T`
3. Have an extension function `Result<T>.map(transform: (T) -> R): Result<R>` that applies the transform only on success
4. Have a top-level function `fun <T> runCatching(block: () -> T): Result<T>` that wraps a block and catches exceptions

Show all declarations and provide a usage example demonstrating all four.

> Answer:

---

## Bonus Questions (variable pts)

**Bonus 1.** (+5 pts) Explain the concept of "smart casts" in Kotlin with a code example. What are the conditions under which a smart cast does NOT work? Give at least two examples of situations where smart cast fails and explain why.

> Answer:
