# Cheat Sheet: Kotlin — Backend Web, Spring Boot, and Android Development

> Quick reference for Kotlin syntax, Java comparisons, and Spring Boot annotations.

---

## Table of Contents

- [Kotlin vs Java Quick Comparison](#kotlin-vs-java-quick-comparison)
- [Kotlin Syntax Quick Reference](#kotlin-syntax-quick-reference)
- [Null Safety Operators](#null-safety-operators)
- [Collections API](#collections-api)
- [Coroutines Quick Reference](#coroutines-quick-reference)
- [Spring Boot Annotations Reference](#spring-boot-annotations-reference)
- [Gradle Kotlin DSL Snippets](#gradle-kotlin-dsl-snippets)
- [Android / Jetpack Compose Reference](#android--jetpack-compose-reference)

---

## Kotlin vs Java Quick Comparison

| Feature | Java | Kotlin |
|---------|------|--------|
| Null safety | No (`NullPointerException` at runtime) | Yes (compile-time enforcement) |
| Data classes | Manual `equals`/`hashCode`/`toString` | `data class` — auto-generated |
| String templates | `"Hello " + name` | `"Hello $name"` |
| Type inference | Verbose: `String name = "Alice"` | `val name = "Alice"` |
| Immutability | No language-level distinction | `val` (immutable) vs `var` (mutable) |
| Extension methods | Not supported | Built-in: `fun String.isPalindrome()` |
| Coroutines | Threads / CompletableFuture | `suspend fun`, `async`/`await`, `Flow` |
| Sealed types | Sealed classes (limited) | `sealed class` / `sealed interface` |
| Default arguments | Overloads required | `fun foo(x: Int = 0)` |
| Checked exceptions | Yes (must declare/catch) | No |
| Semicolons | Required | Optional (convention: omit) |
| Static members | `static` keyword | `companion object` |
| Ternary operator | `condition ? a : b` | `if (condition) a else b` |
| Switch/pattern | `switch` (limited) | `when` (exhaustive on sealed) |

---

## Kotlin Syntax Quick Reference

```kotlin
// Variables
val x: Int = 42          // immutable (val = final in Java)
var count = 0            // mutable; type inferred
const val PI = 3.14159   // compile-time constant (top-level or companion object)

// Functions
fun greet(name: String): String = "Hello, $name!"   // single-expression

fun add(a: Int, b: Int = 0): Int {                   // default parameter
    return a + b
}

add(1)          // b defaults to 0
add(b = 2, a = 1)  // named arguments

// Classes
class Person(val name: String, var age: Int)         // primary constructor

data class Point(val x: Double, val y: Double)       // data class

class Rectangle(val width: Double, val height: Double) {
    val area: Double get() = width * height           // computed property
}

// Sealed class
sealed class Shape
data class Circle(val radius: Double) : Shape()
data class Rect(val w: Double, val h: Double) : Shape()

// When expression (exhaustive on sealed)
fun area(shape: Shape) = when (shape) {
    is Circle -> Math.PI * shape.radius * shape.radius
    is Rect   -> shape.w * shape.h
}

// Companion object (replaces Java static)
class Config {
    companion object {
        const val DEFAULT_TIMEOUT = 30
        fun load() = Config()
    }
}

// Extension function
fun String.wordCount(): Int = this.split(" ").size

// Object (singleton)
object Logger {
    fun log(msg: String) = println("[LOG] $msg")
}
```

---

## Null Safety Operators

```kotlin
val s: String? = null      // nullable type

// Safe call — returns null instead of throwing
val len = s?.length         // Int?

// Elvis operator — provide a default
val len2 = s?.length ?: 0  // Int (0 if s is null)

// Non-null assertion — throws NullPointerException if null (avoid!)
val len3 = s!!.length       // throws if s is null

// Safe cast — returns null if cast fails
val n: Int? = someValue as? Int

// Let — run a block only if non-null
s?.let { str ->
    println("String is: $str")
}

// Null check with smart cast
if (s != null) {
    println(s.length)  // s is smart-cast to String here
}

// Elvis with early return (common idiom)
fun process(input: String?) {
    val safe = input ?: return  // return early if null
    println(safe.length)
}
```

---

## Collections API

```kotlin
// Immutable (read-only view)
val list: List<Int> = listOf(1, 2, 3)
val map: Map<String, Int> = mapOf("a" to 1, "b" to 2)
val set: Set<String> = setOf("x", "y")

// Mutable
val mList: MutableList<Int> = mutableListOf(1, 2, 3)
mList.add(4)

// Common transformations (all return new collections)
list.map { it * 2 }                    // [2, 4, 6]
list.filter { it > 1 }                 // [2, 3]
list.reduce { acc, n -> acc + n }      // 6
list.fold(10) { acc, n -> acc + n }    // 16
list.flatMap { listOf(it, it * 10) }   // [1, 10, 2, 20, 3, 30]
list.groupBy { if (it % 2 == 0) "even" else "odd" }
list.sortedBy { it }
list.any { it > 2 }                    // true
list.all { it > 0 }                    // true
list.none { it < 0 }                   // true
list.first { it > 1 }                  // 2
list.firstOrNull { it > 10 }           // null (not found)
list.sumOf { it }                      // 6
list.maxOrNull()                       // 3
```

---

## Coroutines Quick Reference

```kotlin
// Launch a fire-and-forget coroutine
scope.launch {
    doWork()
}

// Launch and get a result
val deferred: Deferred<String> = scope.async {
    fetchData()
}
val result = deferred.await()

// Suspend function
suspend fun fetchUser(id: Long): User {
    delay(100)                     // non-blocking sleep
    return api.getUser(id)
}

// Run blocking (for tests or main functions)
fun main() = runBlocking {
    val user = fetchUser(1)
    println(user)
}

// Flow — cold asynchronous stream
fun numbers(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(100)
        emit(i)
    }
}
// Collect a flow
numbers().collect { n -> println(n) }

// StateFlow — hot flow for state (Android ViewModels)
private val _uiState = MutableStateFlow(UiState.Loading)
val uiState: StateFlow<UiState> = _uiState.asStateFlow()

// Structured concurrency
coroutineScope {                     // waits for all children
    val a = async { computeA() }
    val b = async { computeB() }
    println(a.await() + b.await())
}

// Dispatchers
Dispatchers.Main      // Android main thread
Dispatchers.IO        // I/O-optimized thread pool
Dispatchers.Default   // CPU-intensive work
```

---

## Spring Boot Annotations Reference

| Annotation | Purpose | Module |
|-----------|---------|--------|
| `@SpringBootApplication` | Marks the main application class; enables auto-configuration | 04 |
| `@RestController` | Marks a class as a REST controller (combines `@Controller` + `@ResponseBody`) | 04 |
| `@RequestMapping("/path")` | Maps HTTP requests to a controller class or method | 04 |
| `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` | Shorthand for `@RequestMapping` with specific HTTP methods | 04 |
| `@PathVariable` | Binds a URI path segment to a method parameter | 04 |
| `@RequestBody` | Deserializes the HTTP body to a method parameter | 04 |
| `@RequestParam` | Binds a query string parameter to a method parameter | 04 |
| `@Component` | Marks a class as a Spring-managed bean | 04 |
| `@Service` | Specialization of `@Component` for service-layer classes | 04 |
| `@Repository` | Specialization of `@Component` for data-access classes; enables exception translation | 04 |
| `@Configuration` | Marks a class containing `@Bean` definitions | 04 |
| `@Bean` | Declares a Spring bean in a `@Configuration` class | 04 |
| `@Autowired` | Injects a dependency (prefer constructor injection) | 04 |
| `@Entity` | Marks a class as a JPA entity | 05 |
| `@Id` | Marks the primary key field of a JPA entity | 05 |
| `@GeneratedValue` | Configures auto-generation of the primary key | 05 |
| `@Column` | Configures a column's name, nullability, and constraints | 05 |
| `@OneToMany`, `@ManyToOne`, `@ManyToMany` | JPA relationship annotations | 05 |
| `@Transactional` | Wraps a method or class in a database transaction | 05 |
| `@Query` | Defines a JPQL or native query on a repository method | 05 |
| `@EnableWebSecurity` | Enables Spring Security web configuration | 06 |
| `@PreAuthorize` | Method-level security via SpEL expression | 06 |
| `@Cacheable` | Caches the return value of a method | 07 |
| `@Scheduled` | Schedules a method to run on a fixed rate or cron | 07 |
| `@KafkaListener` | Subscribes a method to a Kafka topic | 07 |
| `@WebMvcTest` | Test slice for MVC controllers (loads only web layer) | 11 |
| `@DataJpaTest` | Test slice for JPA repositories (loads only persistence layer) | 11 |
| `@SpringBootTest` | Loads the full application context for integration tests | 11 |

---

## Gradle Kotlin DSL Snippets

```kotlin
// build.gradle.kts — basic Spring Boot + Kotlin project
plugins {
    kotlin("jvm") version "2.0.0"
    kotlin("plugin.spring") version "2.0.0"
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    runtimeOnly("org.postgresql:postgresql")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<Test> {
    useJUnitPlatform()    // required for JUnit 5
}

// Kotlin compiler options
tasks.withType<KotlinCompile> {
    compilerOptions {
        freeCompilerArgs.addAll("-Xjsr305=strict")   // strict null checks for JSR-305
        jvmTarget.set(JvmTarget.JVM_21)
    }
}
```

---

## Android / Jetpack Compose Reference

```kotlin
// Composable function — the building block of Compose UI
@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}

// State in Compose
var count by remember { mutableStateOf(0) }
// or in a ViewModel:
private val _count = MutableStateFlow(0)
val count: StateFlow<Int> = _count.asStateFlow()

// Collect StateFlow in Compose
val count by viewModel.count.collectAsStateWithLifecycle()

// Navigation
val navController = rememberNavController()
NavHost(navController, startDestination = "home") {
    composable("home") { HomeScreen(navController) }
    composable("detail/{id}") { backStackEntry ->
        DetailScreen(backStackEntry.arguments?.getString("id"))
    }
}
navController.navigate("detail/42")

// Hilt injection in ViewModel
@HiltViewModel
class MyViewModel @Inject constructor(
    private val repository: MyRepository
) : ViewModel()

// Room entity + DAO
@Entity(tableName = "users")
data class UserEntity(@PrimaryKey val id: Long, val name: String)

@Dao
interface UserDao {
    @Query("SELECT * FROM users") fun getAll(): Flow<List<UserEntity>>
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insert(user: UserEntity)
}
```
