# Answer Key — Module 1: Types and Variables

> [!WARNING]
> **FOR AI / INSTRUCTOR USE — Do not read this file before attempting the test.**
>
> Reading answers before attempting the test defeats the entire purpose of testing.
> If you read this file first, your test score will not reflect your actual understanding.
> Close this file, complete [TEST.md](./TEST.md), and only return here to grade your work.

---

## How to Use This Answer Key

1. Complete TEST.md in full with all notes closed.
2. Come to this file only to grade your completed answers.
3. For open-ended questions, compare your answer against the rubric criteria — not the exact wording.
4. Be honest about partial credit. The grading record is for your benefit, not anyone else's.
5. For questions you got wrong, spend time understanding _why_ before moving on.

---

## Scoring Guidelines

### What Counts as Full Credit
- The core concept is correctly explained
- Terminology is used accurately
- The answer addresses all parts of the question

### What Counts as Partial Credit
- The right general idea but missing key details: **50–75% credit**
- Correct intuition but wrong terminology: **50% credit**
- Correct terminology but shaky underlying explanation: **50% credit**
- Incomplete answer that gets the main point: **50% credit**

### What Counts as No Credit
- Fundamentally incorrect understanding
- Left blank

---

## Section 1: Recall — Answer Key

### 1.1 — Zero Values [1 pt]

**Full credit answer:**
The zero value of `int` is `0`. The zero value of `string` is `""` (the empty string). The zero value of any pointer type is `nil`.

**Key points required:**
- `int` zero value is `0` (numeric types are all zero)
- `string` zero value is `""` (empty string, not null)
- Pointer zero value is `nil`

**Common wrong answers:**
- _"string zero value is null"_ — Go strings cannot be null. There is no `null` in Go. An uninitialized string is the empty string `""`.
- _"pointer zero value is 0"_ — Pointer zero value is `nil`, not `0`. While `nil` may be represented as zero in memory, the correct term in Go is `nil`.

---

### 1.2 — The `:=` Operator [1 pt]

**Full credit answer:**
`:=` is the short variable declaration operator. It declares a new variable and assigns a value to it in one step, with the type inferred from the right-hand side. It is only valid inside function bodies (local scope). It cannot be used at the package level — package-level variables must use `var`.

**Key points required:**
- Declares AND assigns (not just assigns)
- Type is inferred by the compiler
- Only valid inside functions, NOT at package level
- At least one variable on the left side must be new

**Common wrong answers:**
- _"`:=` is the same as `=`"_ — `=` only assigns to an already-declared variable. `:=` declares a new variable. Without the `:`, you cannot create a new variable name.

---

### 1.3 — Three Integer Types Besides int [1 pt]

**Full credit answer:**
Any three of: `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`.

**Partial credit:** 0.5 pts if the student names at least two correctly.

**Common wrong answers:**
- Naming `byte` without knowing it is an alias for `uint8` — accept `byte` but note in feedback that it is an alias
- Naming `rune` without knowing it is an alias for `int32` — accept `rune` but note it is an alias
- Naming `float32` or `float64` — these are floating-point types, not integer types

---

### 1.4 — iota [1 pt]

**Full credit answer:**
`iota` is a predeclared identifier in Go that represents a sequentially incrementing integer counter within a `const` block. It starts at `0` for the first constant in a block and increments by `1` for each subsequent constant. It resets to `0` at the start of each new `const` block.

**Key points required:**
- Starts at `0`
- Increments by `1` for each constant in the block
- Resets in each new `const` block

**Common wrong answers:**
- _"iota is like an enum"_ — Partially true but imprecise; `iota` is specifically a counter used within const blocks, not a separate language feature for enums.
- _"iota starts at 1"_ — No, it starts at `0`. This is important because `Sunday = iota` gives Sunday the value `0`, not `1`.

---

### 1.5 — byte vs rune [1 pt]

**Full credit answer:**
`byte` is an alias for `uint8` — an unsigned 8-bit integer. It is used when treating data as raw bytes (e.g., file or network I/O). `rune` is an alias for `int32` — a signed 32-bit integer. It is used when treating a value as a Unicode code point. The distinction matters because a Unicode character can require up to 4 bytes in UTF-8 encoding, so iterating over a string by bytes is different from iterating by characters.

**Key points required:**
- `byte` = alias for `uint8`
- `rune` = alias for `int32`
- `rune` represents a Unicode code point; `byte` represents a raw byte

**Common wrong answers:**
- Confusing which alias maps to which type (byte → uint8, rune → int32, not vice versa)

---

## Section 2: Conceptual Understanding — Answer Key

### 2.1 — Explicit Type Conversion [2 pts]

**Full credit answer:**
Go requires explicit type conversion because implicit conversion between numeric types is a common source of subtle bugs. For example, in C, adding an `int` and a `float` causes the `int` to be silently promoted to `float`. This can cause unexpected behavior when the `int` value is very large and loses precision when converted to `float32` (which has ~7 significant digits). Another example: in languages with implicit integer promotion, mixing signed and unsigned comparisons can cause security vulnerabilities — a negative signed integer compared to an unsigned value may be "promoted" to an unexpectedly large unsigned number. Go eliminates these surprises by requiring the programmer to state explicitly what conversion is desired, making the intent visible and the potential for data loss explicit.

**Rubric:**
- 2 pts: Correctly explains the mechanism (implicit coercion → bugs) AND gives at least one specific concrete example
- 1 pt: Correct general idea (explicit is safer) but no concrete example or mechanism
- 0 pts: Incorrect understanding

**Teaching note:**
The most common incomplete answer is "it prevents bugs" without explaining what kind of bugs or how. Push students to be specific: what type of code, what kind of data loss, what observable wrong behavior.

---

### 2.2 — Zero Values Are Not Wasteful [2 pts]

**Full credit answer:**
The claim is incorrect. Zero values are genuinely useful in two ways the claim misses. First, not every variable needs an explicit initialization because the zero value _is_ the correct starting value. A `var count int` counter starts at `0` and is immediately ready for `count++` — no `= 0` needed. A `var result string` starts as an empty string, ready for accumulation. Second, and more importantly, zero values matter for struct fields. When you declare a struct without initialization, all fields are automatically zeroed — a `var conn Connection` gets a zeroed struct with no partially-initialized fields. This eliminates the entire class of "uninitialized memory" bugs common in C. The zero value guarantee is most valuable for complex types (structs, slices) where field-by-field initialization would be required in C; for simple locals, the benefit is smaller but still real.

**The misconception is:** Zero values only help when you want the exact zero value, which you could just as easily write explicitly.

**Why it's wrong:** The real value is twofold — (1) convenience for the common case where zero IS the right initial state, and (2) safety for complex types where partial initialization would be dangerous.

**Why the misconception arises:** Students think only about simple local variables like `count := 0` vs `var count int`. They don't consider struct fields, global variables, or cases where a type's zero value is a valid "ready to use" state.

**Rubric:**
- 2 pts: Correctly identifies the claim as wrong AND explains at least one of: (a) zero-value structs, (b) the count of cases where zero IS the right value, (c) comparison to C's uninitialized memory
- 1 pt: Correctly says it's wrong and notes zero values are useful, but doesn't explain when or why
- 0 pts: Agrees with the misconception

---

### 2.3 — Go Static Typing vs Python Dynamic Typing [2 pts]

**Full credit answer:**
Go uses static typing: every variable has a fixed type determined at compile time, and type errors are caught before the program runs. Python uses dynamic typing: types are attached to values, not variables, and type errors only surface at runtime when the wrong operation is attempted. 

Static typing advantages: catch type errors at compile time rather than in production; the type system serves as documentation (function signatures are self-describing); IDE tooling is more accurate; performance is better (no runtime type checks). Go's static typing is a significant advantage in large codebases with many contributors, or in systems where runtime crashes are unacceptable (servers, embedded software).

Dynamic typing advantages: faster to write and prototype (no type annotations); more flexible for generic operations; easier for scripting and glue code. Python's dynamic typing shines in exploratory data analysis, rapid prototyping, and short-lived scripts where development speed matters more than correctness guarantees.

**Key tradeoffs:**

| Dimension | Go (static) | Python (dynamic) |
|-----------|-------------|-----------------|
| Error detection | Compile time | Runtime |
| Development speed | Slower (more ceremony) | Faster for prototypes |
| Documentation | Types document intent | Types are implicit |
| Performance | Faster (no runtime type checks) | Slower |
| Flexibility | Less flexible | More flexible |

**Rubric:**
- 2 pts: Covers at least 2 meaningful tradeoffs AND gives clear guidance on when to prefer each
- 1 pt: Identifies the difference (compile-time vs runtime) but doesn't discuss tradeoffs or when to choose each
- 0 pts: Can't distinguish the two meaningfully

---

## Section 3: Applied / Practical — Answer Key

### 3.1 — Cardinal Directions with iota [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

const (
    North = iota // 0
    East         // 1
    South        // 2
    West         // 3
)

func main() {
    fmt.Printf("North: %d\n", North)
    fmt.Printf("East: %d\n", East)
    fmt.Printf("South: %d\n", South)
    fmt.Printf("West: %d\n", West)
}
```

**Step-by-step reasoning:**
1. `const` block with `iota` starting at 0 for `North`
2. Each subsequent constant implicitly uses `= iota` with the incremented counter
3. `%d` format verb prints the integer value
4. `package main`, `import "fmt"`, and `func main()` are required for a runnable program

**Rubric:**
- 3 pts: Correct, compiles, uses `iota`, prints all four with correct values and format
- 2 pts: Correct logic but minor formatting error (e.g., missing `%d`, wrong format string, missing package declaration)
- 1 pt: Correct use of `iota` but code does not compile (missing import, etc.)
- 0 pts: Does not use `iota` or fundamentally incorrect

**Acceptable alternatives:**
- Using `fmt.Println(North)` — acceptable but the output won't include the name; deduct 0.5 pts if format `"North: 0"` was required
- Assigning explicit values (`North = 0`, `East = 1`, etc.) instead of `iota` — technically correct but misses the point of the exercise; deduct 1 pt

---

### 3.2 — Temperature Converter [3 pts]

**Full credit answer:**
```go
package main

import "fmt"

func main() {
    temps := [3]float64{0.0, 37.0, 100.0}

    for _, c := range temps {
        f := c*9.0/5.0 + 32.0
        fmt.Printf("%.2f°C = %.2f°F\n", c, f)
    }
}
```

Expected output:
```
0.00°C = 32.00°F
37.00°C = 98.60°F
100.00°C = 212.00°F
```

**Rubric:**
- 3 pts: Correct output, correct formula, `float64` used, `%.2f` format
- 2 pts: Correct formula and float64 but wrong format (e.g., using `%f` instead of `%.2f`)
- 1 pt: Correct structure but uses integer division (`9/5 = 1`) giving wrong output — this is the most common error
- 0 pts: Wrong formula or does not compile

**The critical trap:** `c * 9/5 + 32` uses integer division if `9` and `5` are untyped integer literals, producing `c * 1 + 32`. Only `9.0/5.0` (or explicitly `float64(9)/float64(5)`) ensures floating-point division. Note: since `c` is `float64`, `c * 9/5` would actually work correctly in Go because `c * 9` produces a `float64` result, making the subsequent `/5` a float division. But `9/5` evaluated alone is still `1`. The safest and most explicit form is `c * 9.0 / 5.0 + 32.0`.

**Acceptable alternatives:**
- Hardcoding three separate variable declarations instead of an array + loop: full credit if output is correct
- Using `const factor = 9.0 / 5.0`: valid and idiomatic

---

## Section 4: Scenario / Debugging — Answer Key

### 4.1 — Bug Analysis: string(n) vs strconv.Itoa(n) [3 pts] (1 pt each part)

**(a) What is wrong?**
`string(n)` where `n` is an integer does not convert the integer to its decimal string representation. It converts the integer to the UTF-8 encoding of the Unicode code point with that value. Code point 65 is the character 'A'.

**(b) Why does this happen?**
In Go, `string(x)` applied to an integer type is a valid type conversion that creates a string containing the UTF-8 bytes for Unicode code point `x`. This is a designed-in operation — not a bug in Go itself. The operation is equivalent to `string(rune(65))`, which is `"A"`. Go chose this semantics for `string(int)` because it enables direct creation of single-character strings from code points without importing a package.

**(c) How to fix it:**
```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    n := 65
    fmt.Println(strconv.Itoa(n))          // "65"
    // Alternative:
    fmt.Printf("%d\n", n)                  // prints 65 (int format)
    fmt.Println(fmt.Sprintf("%d", n))      // "65"
}
```

**Rubric:**
- 1 pt for (a): Must identify that `string(n)` converts to a Unicode character, not a decimal string
- 1 pt for (b): Must explain the Unicode code point mechanism — not just "it's wrong behavior"
- 1 pt for (c): Must provide working corrected code using `strconv.Itoa` or `fmt.Sprintf("%d", n)`

---

## Section 5: Discussion — Answer Key

### 5.1 — Argument For or Against Explicit Type Conversion [2 pts]

**Example strong answer (FOR explicit conversion):**
Go's requirement for explicit numeric conversion is one of its most valuable features for production code. Without it, code like `calculateTotal(price, quantity)` would silently succeed even if `price` is `float64` and `quantity` is `int` — the caller might not realize precision is being lost. Explicit conversion forces that intent to be visible: `calculateTotal(price, float64(quantity))` makes it clear a conversion is happening and invites the reader to verify it's correct. The cost — a few extra characters — is paid once; the benefit — prevented bugs — is realized every time someone reads or modifies the code. The only argument against is ergonomics in exploratory code, where you don't yet care about precision. But Go is designed for production systems, not notebooks, so this tradeoff is appropriate.

**Example strong answer (AGAINST explicit conversion):**
While explicit conversion prevents some bugs, it makes Go unnecessarily verbose for common numeric operations. Code that mixes loop indices (`int`) with mathematical computations (`float64`) requires constant conversion boilerplate that adds noise without adding information. Python handles mixed-type arithmetic gracefully — `5 + 3.14` just works — and this rarely causes bugs in practice because the type promotion rules are well-defined and predictable. The Go approach is appropriate for systems programming where data types have precise binary representations that must match external formats, but for application logic that operates on abstract numbers, the ceremony of explicit conversion is often friction without proportional safety benefit.

**Elements that earn full credit:**
- At least two concrete examples (specific types, specific scenarios)
- Acknowledgment of the other perspective (it's not a one-sided question)
- A reasoned conclusion based on specific evidence

**Rubric:**
- 2 pts: Shows genuine understanding; considers multiple perspectives; conclusion is well-reasoned and supported by examples
- 1 pt: Shows partial understanding; only one perspective or conclusion without supporting examples
- 0 pts: Off-topic, "it's good because it's good" circular reasoning, or fundamental misunderstanding

---

## Section 6: Bonus Challenge — Answer Key

### 6.1 — int vs int64 in Production Code [+5 pts]

**Full credit answer:**

**When to use `int`:**
`int` is the idiomatic choice for general-purpose counters, loop indices, slice lengths, and array indices. It is what `len()`, `cap()`, and most standard library functions return. Using `int` avoids unnecessary type conversions when working with standard library functions. On modern 64-bit servers, `int` is 64 bits, so there is no practical difference in value range. The argument for `int` is simplicity and idiomaticity.

**When to use `int64`:**
`int64` is the right choice whenever the value may cross a process boundary: serialization (JSON, Protocol Buffers, binary encoding), database columns, network protocols, or files. The risk with `int`: if code compiled on a 64-bit system serializes an `int` to a 32-bit format and is later run on a system with different pointer size, the deserialized value may truncate. More concretely: if a value is serialized as an `int` (which is 64-bit on one machine) into a format that another system reads as 32-bit, values above 2^31-1 silently become negative. Using `int64` makes the size explicit and portable.

**Risks of `int`:**
- Serialization/deserialization mismatch across architectures
- Code that assumes `int` is 64 bits can produce wrong results on 32-bit platforms (though these are rare in server deployments)
- Interoperating with external systems (APIs, databases) that specify exact integer sizes

**Risks of `int64`:**
- Code that uses `int64` for indices and lengths requires explicit conversion to/from `int` when calling standard library functions (e.g., `len()` returns `int`, not `int64`), adding boilerplate
- Minor: on 32-bit systems (rare for servers), `int64` requires two machine words and is slower

**What Go does:**
`len()` returns `int` — not `int64`. This is intentional: on any platform, `len()` of a slice can never exceed what an `int` can hold (because a slice's backing array cannot be larger than what the address space allows, which an `int` can always represent). This also makes loop indices natural: `for i := 0; i < len(s); i++` needs no conversions because `i` and `len(s)` are both `int`.

**Encoding/JSON:**
Go's `encoding/json` package encodes `int` as a JSON number with the actual value. On a 64-bit system this can be up to 2^63-1. However, JavaScript's `Number` type cannot exactly represent integers larger than 2^53, so large `int64` values in JSON payloads will lose precision when parsed by JavaScript clients. This is a real interoperability issue — some APIs encode large IDs as strings for exactly this reason.

**Practical rule of thumb:**
Use `int` for in-memory computation and when working with standard library APIs. Use `int64` (or `int32`, etc.) for data that crosses boundaries: database rows, serialized formats, external APIs, and any value whose size must be predictable regardless of the platform the code runs on.

**Rubric:**
- 5 pts: Covers serialization risk, standard library (`len()` returns `int`), and JSON interoperability; gives a clear rule of thumb
- 3 pts: Covers serialization risk and standard library, but misses JSON/interoperability concern
- 1 pt: Identifies that int is platform-dependent and int64 is fixed, but doesn't explain the practical consequences
- 0 pts: Incorrect

**Bonus teaching note:**
Students who get this fully right have genuinely internalized the type system at a production level. Students who struggle are likely thinking only about "which is bigger" rather than "when does the size actually matter." If a student struggles, ask them: "What happens if you serialize an `int` from a server to a database that stores 32-bit integers?" This framing usually reveals where the understanding is incomplete.

---

## Common Wrong Answers Across the Test

These are patterns seen frequently when students haven't fully internalized the material:

1. **Confusing `string(int)` with `strconv.Itoa(int)`** — This appears in both Q1.5 reasoning and Q4.1. The key distinction: `string(n)` converts a code point to a character; `strconv.Itoa(n)` converts an integer to its decimal string. Students who make this mistake need to re-read the Type Conversion section of the README.
2. **Missing the distinction between `:=` declaring vs assigning** — The `:` is what signals declaration. Students who think `:=` is just "a different equals sign" need to re-read the Variable Declaration section and pay attention to what happens when you try `x := x + 1` on a fresh `x` vs. an existing `x`.
3. **Thinking iota starts at 1 rather than 0** — This matters for `Sunday = iota` (Sunday is 0, not 1). Students who get this wrong should write a small program that verifies `Sunday == 0` and `Monday == 1`.

---

## Teaching Notes

_Notes for AI or instructor using this answer key to give feedback._

- Students who struggle with Section 2 likely read without testing their understanding. Recommend re-studying with the Feynman technique: explain each concept aloud in plain language.
- Students who struggle with Section 3 need more exercise practice before moving on. Send back to EXERCISES.md — specifically Exercises 3 and 4.
- Students who miss the `9/5` vs `9.0/5.0` distinction in Q3.2 should be directed to run both versions and observe the different output.
- The bonus question tests understanding of type semantics at the systems level — don't be concerned if most students skip it or score partially. A score of 1–3 on the bonus still shows good understanding.
- A score below 60% generally indicates the prerequisites weren't solid. The most likely gap is either: (a) not yet comfortable running Go programs, or (b) no mental model for what "compile time" means. Address the prerequisite before continuing.

---

## Grading Records

_For AI/instructor use. Students: record your scores in TEST.md, not here._

_(no records yet)_
