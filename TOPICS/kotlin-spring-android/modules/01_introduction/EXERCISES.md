# Exercises: Module 01 — Introduction to Kotlin

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Use IntelliJ IDEA or the [Kotlin Playground](https://play.kotlinlang.org) to run your code.
Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Understand `val` vs `var` and type inference.

Write a Kotlin program with the following variables:
- An immutable variable `pi` with the value `3.14159`
- A mutable variable `counter` starting at `0`
- An immutable variable `greeting` containing the string `"Hello, Kotlin!"`

Print each variable. Then increment `counter` to `5` and print it again.
Try to reassign `pi` — observe and explain the compiler error.

```kotlin
fun main() {
    // Write your code here
}
```

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Practice string templates and `when` expressions.

Write a function `gradeMessage(score: Int): String` that:
- Returns `"Excellent! Score: $score"` for scores 90–100
- Returns `"Good job! Score: $score"` for scores 70–89
- Returns `"Keep practicing. Score: $score"` for scores 50–69
- Returns `"Please review the material. Score: $score"` for anything below 50

Test it with: 95, 82, 61, 45.

```kotlin
fun gradeMessage(score: Int): String {
    // Write your code here
}

fun main() {
    // Test your function here
}
```

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Practice nullable types and safe calls.

Write a function `getUserCity(user: Map<String, String>): String` that:
- Retrieves the `"city"` key from the map
- Returns the city name if present
- Returns `"Unknown city"` if the key is absent or the value is blank

Test with:
```kotlin
val user1 = mapOf("name" to "Alice", "city" to "Prague")
val user2 = mapOf("name" to "Bob")
val user3 = mapOf("name" to "Carol", "city" to "  ")
```

```kotlin
fun getUserCity(user: Map<String, String>): String {
    // Write your code here
}
```

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Design and use a data class.

Create a `data class Product` with properties: `id: Int`, `name: String`, `price: Double`, `inStock: Boolean`.

Write a function `formatProduct(product: Product): String` that returns a formatted string like:
`"[101] Kotlin in Action - $39.99 (In Stock)"` or `"[102] Old Book - $5.00 (Out of Stock)"`.

Use the `copy` function to create a discounted version of a product (reduce price by 10%) and print both.

```kotlin
// Write your data class and functions here
```

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Practice extension functions and the standard library.

Write the following extension functions on `List<Int>`:
1. `fun List<Int>.secondLargest(): Int?` — returns the second-largest unique value, or `null` if fewer than 2 unique values
2. `fun List<Int>.isMonotonicallyIncreasing(): Boolean` — returns `true` if each element is strictly greater than the previous

Test with:
```kotlin
listOf(3, 1, 4, 1, 5, 9, 2, 6)   // secondLargest → 6, isMonotonically → false
listOf(1, 2, 3, 4, 5)              // secondLargest → 4, isMonotonically → true
listOf(5)                           // secondLargest → null, isMonotonically → true
```

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Model states with a sealed class.

Create a sealed class hierarchy `ParseResult<T>` with:
- `data class ParseOk<T>(val value: T)` — successful parse
- `data class ParseErr(val input: String, val reason: String)` — failed parse

Write a function `parsePositiveInt(input: String): ParseResult<Int>` that:
- Returns `ParseOk(n)` if `input` is a valid integer greater than zero
- Returns `ParseErr(input, "not a number")` if it can't be parsed
- Returns `ParseErr(input, "must be positive")` if it parses but is ≤ 0

Write a `displayResult` function that uses `when` (exhaustively) to print the result.

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Chain null safety operators in a realistic scenario.

You have the following data structure (simulating a JSON response):

```kotlin
data class Address(val street: String?, val city: String?, val country: String?)
data class Contact(val email: String?, val phone: String?, val address: Address?)
data class UserProfile(val name: String, val contact: Contact?)
```

Write a function `getDisplayAddress(profile: UserProfile): String` that:
- Returns `"city, country"` if both city and country are non-null and non-blank
- Returns just the city if only city is available
- Returns just the country if only country is available
- Returns `"No address on file"` otherwise

Use only null safety operators (`?.`, `?:`, `let`) — no explicit `if (x != null)` checks.

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Write a mini text analysis program.

Write a program that takes a multiline string and produces a `TextStats` data class containing:
- `wordCount: Int` — total word count
- `uniqueWords: Int` — count of distinct words (case-insensitive)
- `longestWord: String` — the longest word (if tie, take first)
- `mostFrequent: Pair<String, Int>` — the most frequent word and its count

```kotlin
val text = """
    To be or not to be that is the question
    Whether tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
""".trimIndent()
```

Expected: wordCount=31, uniqueWords=27, longestWord="outrageous", mostFrequent=("to", 3)

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Build a type-safe command dispatch system.

Design a mini command-line interpreter using Kotlin idioms. Implement:

1. A `sealed class Command` with subclasses: `Help`, `Quit`, `Echo(text: String)`, `Calculate(expression: String)`
2. A `fun parse(input: String): Command?` function that parses:
   - `"help"` → `Help`
   - `"quit"` or `"exit"` → `Quit`
   - `"echo <text>"` → `Echo(text)`
   - `"calc <expr>"` → `Calculate(expr)` where expr is like `"3 + 4"` or `"10 * 5"`
   - anything else → `null`
3. A `fun execute(command: Command): String` that runs the command:
   - `Help` → a help message listing available commands
   - `Quit` → `"Goodbye!"` (your main loop should stop)
   - `Echo` → the text back
   - `Calculate` → the arithmetic result (support +, -, *, / on integers)
4. A `main()` that reads lines from stdin in a loop and runs the interpreter

This exercise requires no libraries beyond Kotlin's standard library.
