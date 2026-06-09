# Answers: Module 01 — Introduction to Kotlin

## Answer Key

### Easy Questions (1 pt each)

**Q1:** The `?` suffix means the type is *nullable* — the variable can hold either a value of that type or `null`. Without `?`, the type is non-nullable and the compiler guarantees the variable will never be null.

**Q2:** `val` declares an immutable reference — it cannot be reassigned after initialization (like Java's `final`). `var` declares a mutable reference — it can be reassigned. Convention: prefer `val`; use `var` only when reassignment is necessary. Note: `val` makes the reference immutable, not the object — a `val list: MutableList<Int>` still allows `list.add(1)`.

**Q3:** Google I/O 2017. At the keynote on May 17, 2017, the Android team announced Kotlin as an officially supported and first-class language for Android development.

**Q4:** The Elvis operator `?:`. Example: `val name = input ?: "default"` — evaluates to `"default"` when `input` is null.

**Q5:** False. Kotlin does not require semicolons. They are optional and by strong convention omitted. Kotlin's grammar does not need semicolons to unambiguously parse statements.

### Medium Questions (2 pts each)

**Q6:** A platform type (`String!`) appears when Kotlin interoperates with Java code that has no null-safety annotations. Because Java's type system does not distinguish null from non-null, the Kotlin compiler cannot determine whether a Java value can be null — so it treats it as a "platform type" — it neither enforces non-null nor forces you to handle null. This is dangerous because the compiler will not warn you about potential NPEs from Java API values. The fix: treat Java return values as nullable (`String?`) when there is any doubt, or check the Java source for `@Nullable`/`@NotNull` annotations.

**Q7:** `listOf(1, 2, 3)` creates a read-only `List<Int>` — no `add`, `remove`, or `set` operations are available. `mutableListOf(1, 2, 3)` creates a `MutableList<Int>` with full mutation operations. Choose `listOf` by default to communicate immutability; choose `mutableListOf` only when you need to modify the collection after creation.

**Q8:** Both Kotlin and Java compile to JVM bytecode — the same binary format. The JVM does not know or care which language produced the `.class` files. Since the bytecode is identical in structure, Kotlin code calling a Java library is calling the same bytecode that `javac` produced, and the JVM executes it without any bridging layer.

**Q9:** A single-expression function omits the braces and `return` keyword, using `=` instead:
```kotlin
fun square(n: Int) = n * n
```
The return type is inferred from the expression (`Int` in this case). Use single-expression functions when the entire body fits on one readable line.

**Q10:** Differences between `when` and Java `switch`:
1. `when` is an **expression** (returns a value); Java `switch` is a statement (Java 14+ switch expressions exist, but classic `switch` is a statement)
2. `when` works with **any type** — not just integral types and strings like Java `switch`
3. `when` supports **ranges** (`in 1..10`), type checks (`is String`), and arbitrary conditions
4. `when` on a **sealed class** is exhaustive — the compiler enforces that all cases are handled without requiring `else`
5. `when` cases use `->` instead of `case:` and do **not fall through** by default

### Hard Questions (3 pts each)

**Q11:** The bug is using `!!` on a nullable `text`. When `getLength(null)` is called, `text!!` throws `NullPointerException` instead of returning 0.

Corrected:
```kotlin
fun getLength(text: String?): Int {
    return text?.trim()?.length ?: 0
}
```
Or as a single expression:
```kotlin
fun getLength(text: String?) = text?.trim()?.length ?: 0
```

**Q12:**
```kotlin
fun safeDiv(a: Int, b: Int): Int? = if (b != 0) a / b else null

fun printDivision(a: Int, b: Int) {
    println(safeDiv(a, b)?.toString() ?: "Division by zero")
}
```

**Q13:**
```kotlin
fun area(shape: Shape): Double = when (shape) {
    is Circle    -> Math.PI * shape.radius * shape.radius
    is Rectangle -> shape.width * shape.height
    is Triangle  -> 0.5 * shape.base * shape.height
}
```
Removing `is Triangle -> ...` causes a compile error because `when` used as an expression on a sealed class must cover all possible subclasses. The compiler tracks the full set of sealed subclasses and reports "when expression must be exhaustive" if any case is missing.

**Q14:**
```kotlin
fun buildUserSummary(name: String?, age: Int?, city: String?): String {
    val parts = mutableListOf<String>()
    val displayName = name ?: return "Anonymous user"
    parts.add(displayName)
    age?.let { parts.add(it.toString()) }
    city?.let { parts.add("from $it") }
    return parts.joinToString(", ")
}
```
Or using a more functional style:
```kotlin
fun buildUserSummary(name: String?, age: Int?, city: String?): String {
    val n = name ?: return "Anonymous user"
    return listOfNotNull(n, age?.toString(), city?.let { "from $it" }).joinToString(", ")
}
```

### Expert Questions (5 pts each)

**Q15:** The crash occurs because `findEmail` is annotated `@Nullable` in Java. When called from Kotlin, this becomes a platform type `String!` — the Kotlin compiler does not enforce null-checking. The developer then calls `.uppercase()` on this potentially-null value without any null check, resulting in an NPE when `findEmail` returns null in production.

Corrected:
```kotlin
fun notifyUser(userId: Long) {
    val email: String? = userService.findEmail(userId)
    if (email == null) {
        logger.warn("No email found for userId=$userId, skipping notification")
        return
    }
    sendEmail(email.uppercase())
}
// Or more concisely:
fun notifyUser(userId: Long) {
    val email = userService.findEmail(userId) ?: run {
        logger.warn("No email for userId=$userId")
        return
    }
    sendEmail(email.uppercase())
}
```

**Q16:**
```kotlin
sealed class Result<out T>
data class Ok<T>(val value: T) : Result<T>()
data class Err(val exception: Exception) : Result<Nothing>()

fun <T> Result<T>.getOrDefault(default: T): T = when (this) {
    is Ok  -> value
    is Err -> default
}

fun <T, R> Result<T>.map(transform: (T) -> R): Result<R> = when (this) {
    is Ok  -> try { Ok(transform(value)) } catch (e: Exception) { Err(e) }
    is Err -> this   // propagate error unchanged
}

fun <T> runCatching(block: () -> T): Result<T> = try {
    Ok(block())
} catch (e: Exception) {
    Err(e)
}

// Usage example
fun main() {
    val result: Result<Int> = runCatching { "42".toInt() }
    val doubled: Result<Int> = result.map { it * 2 }
    println(doubled.getOrDefault(-1))   // 84

    val bad: Result<Int> = runCatching { "abc".toInt() }
    println(bad.getOrDefault(-1))       // -1
    println((bad as? Err)?.exception?.message)  // For input string: "abc"
}
```

### Bonus

**Bonus 1:** Smart casts are automatic type casts performed by the Kotlin compiler after a type-check. After `if (x is String)`, inside that branch the compiler knows `x` is a `String` and casts it automatically — no explicit `(x as String)` needed.

```kotlin
fun printLength(x: Any) {
    if (x is String) {
        println(x.length)   // x is smart-cast to String; .length is available
    }
}
```

Smart cast FAILS when:
1. **The variable is a `var` in scope of another thread** — because another thread might reassign it between the check and the use:
```kotlin
var x: Any = "hello"
if (x is String) {
    // Smart cast impossible: x is a mutable var; could be reassigned by another thread
    // println(x.length)  // compile error
    println((x as String).length)  // explicit cast required
}
```
2. **The property is open (overridable) or accessed via a custom getter** — the getter might return a different type on each call:
```kotlin
class Holder {
    val value: Any get() = if (Math.random() > 0.5) "hi" else 42
}
val h = Holder()
if (h.value is String) {
    // Smart cast impossible: h.value has a custom getter that might return different types
    // println(h.value.length)  // compile error
}
```

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
