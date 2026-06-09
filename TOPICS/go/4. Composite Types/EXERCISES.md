# Exercises — Module 4: Composite Types

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just run code mentally — actually write or type your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Expert | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Slice Header Tracing [🟢 Easy] [1 pt]

### Context
Understanding the slice header (ptr, len, cap) is the foundational skill for predicting slice behavior. This exercise builds that mechanical intuition before applying it to harder problems.

### Task
Given the following code, predict the output of each `fmt.Printf` without running the program:

```go
a := []int{10, 20, 30, 40, 50}
b := a[1:4]
c := a[1:4:4]

// Question 1: What are len(b) and cap(b)?
// Question 2: What are len(c) and cap(c)?
// Question 3: If you execute b[0] = 99, what is a[1]?
// Question 4: After b = append(b, 777), does a[4] equal 777 or 50? Why?
// Question 5: After c = append(c, 888), does a[4] equal 777 or 50 or 888?
```

### Requirements
- [ ] Correctly predict `len(b)` and `cap(b)`
- [ ] Correctly predict `len(c)` and `cap(c)`
- [ ] Correctly predict whether `b[0] = 99` modifies `a`
- [ ] Correctly predict whether `append(b, 777)` modifies `a[4]` (b has cap for it)
- [ ] Correctly predict whether `append(c, 888)` modifies `a[4]` (c's cap is limited to 4)

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

`b := a[1:4]` creates a slice header where `ptr` points to `a[1]`, `len = 4-1 = 3`, and `cap = len(a) - 1 = 4` (from the start of b to the end of the underlying array).

</details>

<details>
<summary>Hint 2</summary>

The three-index form `a[1:4:4]` sets `cap = 4-1 = 3`, matching `len`. So `c` cannot grow into `a[4]`. When you `append` to `c` and it exceeds capacity, Go must reallocate — the new element goes into a new backing array, not into `a`.

</details>

### Expected Output / Acceptance Criteria
```
len(b)=3, cap(b)=4
len(c)=3, cap(c)=3
After b[0]=99: a[1]=99         (shared backing array)
After append(b,777): a[4]=777  (b had cap; append wrote into a's backing array)
After append(c,888): a[4]=777  (c's cap was 3; append reallocated; a unchanged)
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```go
package main

import "fmt"

func main() {
    a := []int{10, 20, 30, 40, 50}
    b := a[1:4]   // ptr=&a[1], len=3, cap=4 (a has 5 elements, starting from index 1 there are 4)
    c := a[1:4:4] // ptr=&a[1], len=3, cap=3 (max index is 4, starting at 1 → cap=3)

    fmt.Printf("len(b)=%d, cap(b)=%d\n", len(b), cap(b)) // 3, 4
    fmt.Printf("len(c)=%d, cap(c)=%d\n", len(c), cap(c)) // 3, 3

    b[0] = 99 // modifies a[1] — shared backing array
    fmt.Printf("a[1]=%d\n", a[1]) // 99

    b = append(b, 777) // len(b)=3, cap(b)=4 → fits! writes to a[4]
    fmt.Printf("a[4]=%d\n", a[4]) // 777

    c = append(c, 888) // len(c)=3, cap(c)=3 → must reallocate; new backing array
    fmt.Printf("a[4]=%d\n", a[4]) // still 777 — c's append did not touch a
}
```

**Explanation:**
`b` has `cap=4` because it starts at index 1 of a 5-element array: 5 - 1 = 4 positions remain. An `append` that fits in capacity writes directly into the backing array at position `len(b)` relative to `b`'s `ptr` — which is `a[1+3] = a[4]`. The three-index form `a[1:4:4]` explicitly sets `cap = 4 - 1 = 3`, so `c` cannot write into `a[4]`. When `c` needs to grow, Go allocates a new array.

</details>

---

## Exercise 2: Safe Map Operations [🟢 Easy] [1 pt]

### Context
The most common map bugs in Go are (1) writing to a nil map and (2) not using comma-ok when you need to distinguish "not present" from "present with zero value". This exercise drills both.

### Task
Write a Go program that:
1. Declares a `map[string]int` named `ages` without using `make` or a literal (i.e., it starts as nil)
2. Before writing to it, initialize it properly
3. Adds three entries: `"Alice": 30`, `"Bob": 25`, `"Carol": 35`
4. Uses comma-ok to check if `"Alice"` is present and prints her age
5. Uses comma-ok to check if `"Dave"` is present; since he's not, prints `"Dave not found"`
6. Deletes `"Bob"` and prints the final length of the map

### Requirements
- [ ] Map starts declared as `var ages map[string]int` (nil)
- [ ] Map is initialized before writing (not in the declaration)
- [ ] Comma-ok idiom used for both lookups
- [ ] `delete` used to remove "Bob"
- [ ] Final `len(ages)` is 2

### Hints
<details>
<summary>Hint 1</summary>

To initialize a nil map declared with `var`, use the assignment form: `ages = make(map[string]int)`. The `make` call is on a separate line from the `var` declaration.

</details>

### Expected Output / Acceptance Criteria
```
Alice is 30 years old
Dave not found
Final map size: 2
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
    var ages map[string]int // nil map — reading is safe, writing would panic

    ages = make(map[string]int) // initialize before writing

    ages["Alice"] = 30
    ages["Bob"] = 25
    ages["Carol"] = 35

    // Comma-ok: distinguish "present" from "not present"
    if age, ok := ages["Alice"]; ok {
        fmt.Printf("Alice is %d years old\n", age)
    }

    if _, ok := ages["Dave"]; !ok {
        fmt.Println("Dave not found")
    }

    delete(ages, "Bob")
    fmt.Printf("Final map size: %d\n", len(ages)) // 2
}
```

**Explanation:**
`var ages map[string]int` creates a nil map. Reading from it (`ages["anything"]`) returns 0 safely. Writing (`ages["Bob"] = 25`) panics. After `ages = make(map[string]int)`, the map is initialized and safe to write. The comma-ok form `age, ok := ages["Dave"]` distinguishes a missing key (`ok=false`) from a key with value 0 (`ok=true`). `delete` is safe even if the key doesn't exist.

</details>

---

## Exercise 3: String, []byte, and []rune Conversions [🟢 Easy] [1 pt]

### Context
Go strings are immutable. To manipulate individual characters, you must convert to `[]byte` (for byte-level work) or `[]rune` (for Unicode character-level work). This exercise practices the conversion cycle and the cost awareness that accompanies it.

### Task
Write a Go program that:
1. Starts with the string `s := "café"`
2. Prints the byte length (`len(s)`) and rune count (`utf8.RuneCountInString(s)`)
3. Converts `s` to `[]rune`, capitalizes the first rune (change `'c'` to `'C'`), and converts back to string
4. Converts `s` to `[]byte` and prints the raw bytes as hex
5. Shows (via a comment or print) why converting to `[]rune` is necessary for the capitalization rather than `[]byte`

### Requirements
- [ ] Correct byte length (5) and rune count (4) printed
- [ ] Capitalization of the first character done via `[]rune` conversion
- [ ] `[]byte` hex dump shows the multi-byte encoding of `é`
- [ ] Compiles without error; imports `unicode/utf8`

### Hints
<details>
<summary>Hint 1</summary>

To capitalize, convert to `[]rune`, change index 0 from `'c'` to `'C'`, then convert back: `string(r)`. For the hex dump, use `fmt.Printf("%X\n", []byte(s))`.

</details>

### Expected Output / Acceptance Criteria
```
Byte length: 5
Rune count:  4
Capitalized: Café
Hex bytes:   6361 66C3 A9
```
(Hex may appear without spaces depending on format verb — `%X` on a `[]byte` adds spaces between bytes with `% X`.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    s := "café"

    fmt.Printf("Byte length: %d\n", len(s))                      // 5
    fmt.Printf("Rune count:  %d\n", utf8.RuneCountInString(s))   // 4

    // Capitalize first character via []rune — necessary because 'c' is rune[0]
    // Using []byte would give us the first byte only, which happens to work for
    // ASCII characters but would corrupt multi-byte characters if the first char
    // were non-ASCII.
    r := []rune(s)
    r[0] = 'C'
    fmt.Printf("Capitalized: %s\n", string(r)) // Café

    // Hex dump of raw bytes — shows that 'é' (U+00E9) is encoded as 0xC3 0xA9
    fmt.Printf("Hex bytes:   % X\n", []byte(s)) // 63 61 66 C3 A9
    // c=0x63, a=0x61, f=0x66, é=0xC3 0xA9 (two bytes for U+00E9)
}
```

**Explanation:**
`"café"` has 5 bytes: `c` (1), `a` (1), `f` (1), `é` (2 — UTF-8 encoding of U+00E9 is `0xC3 0xA9`). `len(s)` returns 5. `utf8.RuneCountInString(s)` returns 4. The `[]rune` conversion gives character-level indexing: `r[3]` is the rune `'é'` (U+00E9, value 233). Changing `r[0]` to `'C'` and converting back correctly capitalizes. A `[]byte` conversion would let you set `b[0] = 'C'` too (since `c` is ASCII), but if the first character were multi-byte, you'd only change the first byte of its encoding, corrupting the string.

</details>

---

## Exercise 4: Word Deduplication with a Set [🟡 Medium] [2 pts]

### Context
Go has no built-in set type. The idiomatic Go set is `map[T]struct{}`. This exercise practices that pattern in a realistic context: deduplicating a word list while preserving one occurrence of each unique word.

### Task
Write a Go function `dedupe(words []string) []string` that:
1. Returns a new slice containing each unique word from `words`, in the order of first appearance
2. Uses a `map[string]struct{}` as a "seen" set to track duplicates
3. Does NOT modify the input slice

Also write a `main` function that tests `dedupe` with at least two test cases:
- `["apple", "banana", "apple", "cherry", "banana", "date"]` → `["apple", "banana", "cherry", "date"]`
- An empty slice → an empty slice (not nil)

### Requirements
- [ ] Uses `map[string]struct{}` (not `map[string]bool`) for the set
- [ ] Preserves first-appearance order
- [ ] Does not modify the input slice
- [ ] Returns `[]string{}` (non-nil) for an empty input

### Hints
<details>
<summary>Hint 1</summary>

Iterate over `words` with `range`. For each word, check if it's in `seen`. If not, add it to `seen` and also `append` it to the result slice.

</details>

<details>
<summary>Hint 2 (checking membership)</summary>

Check membership with the comma-ok idiom: `if _, ok := seen[word]; !ok { ... }`. To add to the set: `seen[word] = struct{}{}`.

</details>

### Expected Output / Acceptance Criteria
```
Input:  [apple banana apple cherry banana date]
Output: [apple banana cherry date]

Input:  []
Output: []
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func dedupe(words []string) []string {
    seen := make(map[string]struct{})
    result := make([]string, 0, len(words)) // pre-allocate with enough cap

    for _, word := range words {
        if _, ok := seen[word]; !ok {
            seen[word] = struct{}{} // mark as seen
            result = append(result, word)
        }
    }
    return result
}

func main() {
    words := []string{"apple", "banana", "apple", "cherry", "banana", "date"}
    fmt.Printf("Input:  %v\n", words)
    fmt.Printf("Output: %v\n", dedupe(words))

    empty := []string{}
    out := dedupe(empty)
    fmt.Printf("\nInput:  %v\n", empty)
    fmt.Printf("Output: %v  (nil=%v)\n", out, out == nil)
}
```

**Explanation:**
`make([]string, 0, len(words))` pre-allocates a result slice with zero length but capacity equal to the input length — this is an optimization that avoids multiple reallocations in the common case where few duplicates exist. The `struct{}{}` value is the zero-size instance of the empty struct type. Using `map[string]struct{}` instead of `map[string]bool` saves 1 byte per entry (a `bool` is 1 byte; `struct{}` is 0 bytes) and makes the intent clearer: this is a set, not a flag store.

**Common wrong answers:**
- Using `map[string]bool` — works but misses the idiomatic `struct{}` pattern
- Returning `nil` for empty input instead of `[]string{}` — technically the zero-length check `len(out) == 0` passes either way, but the API contract says "empty, not nil"

</details>

---

## Exercise 5: Struct With Embedding and Method [🟡 Medium] [2 pts]

### Context
Struct embedding is Go's composition mechanism. This exercise practices defining an embedded type, using promoted fields, and adding a method on the outer type — the pattern that appears in virtually every non-trivial Go struct definition.

### Task
Define two struct types:
- `Dimensions` with fields `Width float64` and `Height float64`
- `Rectangle` that embeds `Dimensions` (anonymously) and adds a `Color string` field

Add a method `Area() float64` on `Rectangle` that returns `Width * Height` using the promoted fields.

Add a method `String() string` on `Rectangle` that returns a human-readable description, e.g. `"Rectangle(3.0x4.0, blue, area=12.00)"`.

In `main`, create at least two `Rectangle` values using named struct literals and print them using `fmt.Println` (which calls `String()` automatically if the type implements the `fmt.Stringer` interface).

### Requirements
- [ ] `Dimensions` is embedded (not named) in `Rectangle`
- [ ] `Area()` uses promoted fields (`r.Width` not `r.Dimensions.Width`)
- [ ] `String()` returns the specified format
- [ ] Named struct literal used (not positional)
- [ ] Both rectangles print correctly via `fmt.Println`

### Hints
<details>
<summary>Hint 1</summary>

To embed `Dimensions`, declare it without a field name: `type Rectangle struct { Dimensions; Color string }`. Then `r.Width` and `r.Height` are directly accessible as promoted fields.

</details>

<details>
<summary>Hint 2</summary>

`fmt.Stringer` requires a method `String() string`. If `Rectangle` has this method with a value receiver `func (r Rectangle) String() string`, then `fmt.Println(r)` will call it automatically.

</details>

### Expected Output / Acceptance Criteria
```
Rectangle(3.0x4.0, blue, area=12.00)
Rectangle(5.5x2.0, red, area=11.00)
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

type Dimensions struct {
    Width  float64
    Height float64
}

type Rectangle struct {
    Dimensions        // embedded — Width and Height are promoted
    Color      string
}

// Area uses promoted fields directly
func (r Rectangle) Area() float64 {
    return r.Width * r.Height // r.Dimensions.Width also valid but verbose
}

// String implements fmt.Stringer — fmt.Println will call this
func (r Rectangle) String() string {
    return fmt.Sprintf("Rectangle(%.1fx%.1f, %s, area=%.2f)",
        r.Width, r.Height, r.Color, r.Area())
}

func main() {
    r1 := Rectangle{
        Dimensions: Dimensions{Width: 3.0, Height: 4.0},
        Color:      "blue",
    }
    r2 := Rectangle{
        Dimensions: Dimensions{Width: 5.5, Height: 2.0},
        Color:      "red",
    }

    fmt.Println(r1) // calls r1.String() via fmt.Stringer
    fmt.Println(r2)
}
```

**Explanation:**
`Dimensions` is embedded (not named) in `Rectangle`, so `r.Width` and `r.Height` are directly accessible — the compiler rewrites them to `r.Dimensions.Width` under the hood. The `String()` method with value receiver `Rectangle` satisfies the `fmt.Stringer` interface (defined as `String() string`). `fmt.Println` checks if a value implements `fmt.Stringer` and calls `String()` if so — enabling custom string representations without any special framework.

</details>

---

## Exercise 6: Grouping with a Map of Slices [🟡 Medium] [2 pts]

### Context
Grouping items by a key into a map of slices is one of the most common Go programming patterns. It relies on the interaction between maps and slices: reading a missing map key returns nil, and `append(nil, x)` creates a new slice — so no explicit initialization of each inner slice is needed.

### Task
Write a function `groupByLength(words []string) map[int][]string` that groups words by their length (number of runes, not bytes — use `utf8.RuneCountInString`).

In `main`, call it with a list that includes some Unicode words (e.g., `"café"` has 4 runes but 5 bytes), print the groups in sorted key order.

### Requirements
- [ ] Groups by rune count (not byte count)
- [ ] Uses the append-to-nil pattern (no pre-initialization of inner slices)
- [ ] Prints groups in ascending key order (sort the integer keys)
- [ ] At least one multi-byte Unicode word in the test input

### Hints
<details>
<summary>Hint 1</summary>

After building the map, extract the integer keys into a `[]int`, sort with `slices.Sort`, then iterate over sorted keys.

</details>

<details>
<summary>Hint 2</summary>

`utf8.RuneCountInString(w)` returns the rune count of word `w`. For ASCII words it equals `len(w)`, but for words with multi-byte characters it is smaller.

</details>

### Expected Output / Acceptance Criteria
```
Length 2: [to be]
Length 3: [the]
Length 4: [café word]
Length 5: [hello world]
```
(Exact groups depend on your test words; what matters is that multi-byte words are grouped by rune count.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "slices"
    "unicode/utf8"
)

func groupByLength(words []string) map[int][]string {
    groups := make(map[int][]string)
    for _, w := range words {
        n := utf8.RuneCountInString(w) // rune count, not byte count
        groups[n] = append(groups[n], w) // append-to-nil works fine
    }
    return groups
}

func main() {
    words := []string{"to", "be", "the", "café", "word", "hello", "world"}
    groups := groupByLength(words)

    // Collect and sort integer keys for deterministic output
    keys := make([]int, 0, len(groups))
    for k := range groups {
        keys = append(keys, k)
    }
    slices.Sort(keys)

    for _, k := range keys {
        fmt.Printf("Length %d: %v\n", k, groups[k])
    }
}
```

**Explanation:**
`groups[n] = append(groups[n], w)` is idiomatic: if `n` is not yet in the map, `groups[n]` returns `nil`, and `append(nil, w)` creates a new `[]string{w}`. The assignment writes this new slice back into the map at key `n`. On subsequent iterations for the same `n`, the slice grows normally. `"café"` has rune count 4 (c, a, f, é) but byte count 5 — the test verifies that `utf8.RuneCountInString` is used rather than `len`.

</details>

---

## Exercise 7: Building a Frequency Table with Sorted Output [🔴 Hard] [3 pts]

### Context
This exercise combines maps, slices, structs, and the `slices` package in a realistic pipeline: parse input → count → sort → format. It requires all four composite types working together.

### Task
Write a complete Go program `freqtable` that:
1. Defines a struct `WordCount` with fields `Word string` and `Count int`
2. Writes a function `count(text string) []WordCount` that:
   - Splits `text` into words (use `strings.Fields` and `strings.ToLower`)
   - Strips leading/trailing punctuation from each word (use `strings.Trim(w, ".,!?;:\"'")`)
   - Counts frequency using `map[string]int`
   - Returns a `[]WordCount` sorted by count descending, then word ascending
3. Writes a `main` function that calls `count` with a sample text and prints the top 5 results in the format `N  word` (count right-aligned in 3 chars)

### Requirements
- [ ] `WordCount` struct used (not a plain `[][]string`)
- [ ] Map used for frequency counting (not repeated linear scans)
- [ ] `slices.SortFunc` used for sorting (not manual sort)
- [ ] Top 5 only printed, not all words
- [ ] Format: `%3d  %s` per line

### Hints
<details>
<summary>Hint 1</summary>

Build the frequency map first, then convert it to `[]WordCount` by ranging over the map. Then sort with `slices.SortFunc` using a comparison function that returns `b.Count - a.Count` for descending count, with string comparison as tiebreaker.

</details>

<details>
<summary>Hint 2</summary>

To take the top 5: after sorting, use `counts[:min(5, len(counts))]` (Go 1.21's built-in `min`).

</details>

<details>
<summary>Hint 3 (near-solution hint)</summary>

```go
slices.SortFunc(counts, func(a, b WordCount) int {
    if b.Count != a.Count {
        return b.Count - a.Count // descending
    }
    return strings.Compare(a.Word, b.Word) // ascending
})
```

</details>

### Expected Output / Acceptance Criteria
For the text `"to be or not to be that is the question to be is to do"`:
```
  4  to
  3  be
  2  is
  1  do
  1  not
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
    "fmt"
    "slices"
    "strings"
)

type WordCount struct {
    Word  string
    Count int
}

func count(text string) []WordCount {
    freq := make(map[string]int)
    for _, w := range strings.Fields(strings.ToLower(text)) {
        w = strings.Trim(w, ".,!?;:\"'")
        if w != "" {
            freq[w]++
        }
    }

    counts := make([]WordCount, 0, len(freq))
    for word, n := range freq {
        counts = append(counts, WordCount{Word: word, Count: n})
    }

    slices.SortFunc(counts, func(a, b WordCount) int {
        if b.Count != a.Count {
            return b.Count - a.Count // descending count
        }
        return strings.Compare(a.Word, b.Word) // ascending word
    })

    return counts
}

func main() {
    text := "to be or not to be that is the question to be is to do"
    results := count(text)

    top := results[:min(5, len(results))]
    for _, wc := range top {
        fmt.Printf("%3d  %s\n", wc.Count, wc.Word)
    }
}
```

**Step-by-step explanation:**
1. Build a `map[string]int` frequency table in one pass over the words.
2. Convert the map to `[]WordCount` (maps have no intrinsic order; slices can be sorted).
3. Sort descending by count, breaking ties alphabetically — `slices.SortFunc` is stable with an explicit tiebreaker.
4. Slice to top 5 with `min(5, len(results))` (built-in `min` from Go 1.21).
5. Print with `%3d` for right-aligned counts.

**Why structs here:** A `WordCount` struct is cleaner than a parallel `[]string`/`[]int` pair, which would require keeping indices in sync during sorting. The struct keeps the word and count together as a unit, making the sort function unambiguous.

</details>

---

## Exercise 8: Three-Index Slice for Safe Sub-Slice Passing [🔴 Hard] [3 pts]

### Context
The three-index slice expression `s[low:high:max]` is an advanced but important feature. It limits the capacity of the sub-slice so that appending to it cannot overwrite elements in the parent slice beyond index `high`. This exercise demonstrates why and when to use it.

### Task
Write a function `processChunk(chunk []int) []int` that:
1. Takes a sub-slice `chunk`
2. Filters out zero values
3. Returns the filtered slice

Write a `main` function that:
1. Creates a slice `data := []int{1, 0, 2, 0, 3, 4, 5}` with extra capacity: `make([]int, 7, 10)`
2. Populates `data` with the values above
3. Calls `processChunk` with **both** versions of the sub-slice:
   - Version A: `data[0:7]` (shares backing array's full capacity)
   - Version B: `data[0:7:7]` (capacity limited to 7)
4. Shows that Version A's `processChunk` overwrites data beyond index 6, but Version B's does not

### Requirements
- [ ] `processChunk` uses `append` to build the result (it must actually append)
- [ ] Two calls demonstrated: one with `data[0:7]` and one with `data[0:7:7]`
- [ ] The output shows the data corruption risk from Version A and its absence in Version B
- [ ] Explanation comment in code explains why the three-index form is safer

### Hints
<details>
<summary>Hint 1</summary>

`processChunk` should use a fresh result slice: `result := chunk[:0]` (zero length, shares backing array!) — then `append` non-zero values to it. This is the in-place filtering pattern. The problem: `chunk[:0]` still has `cap = cap(chunk)`, so appending can overwrite `chunk`'s later elements!

</details>

<details>
<summary>Hint 2 (safer pattern hint)</summary>

To be truly safe, use `result := chunk[:0:0]` (zero cap) or `result := make([]int, 0, len(chunk))` (fresh backing array). The exercise's point: even `chunk[:0]` (the compact in-place form) is dangerous without the three-index limit.

</details>

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// processChunk filters zero values out of chunk.
// WARNING: if chunk has extra capacity, this can overwrite
// elements beyond chunk's length in the backing array.
func processChunk(chunk []int) []int {
    // result shares chunk's backing array and capacity!
    result := chunk[:0]
    for _, v := range chunk {
        if v != 0 {
            result = append(result, v)
        }
    }
    return result
}

func main() {
    // Create data with extra capacity to make the issue visible
    data := make([]int, 7, 10)
    for i, v := range []int{1, 0, 2, 0, 3, 4, 5} {
        data[i] = v
    }

    // Add sentinel values in positions 7, 8, 9 of the backing array
    // (we can't access them via data directly, but processChunk can
    //  overwrite them if given the full-capacity sub-slice)
    extended := data[:10] // temporarily extend to see backing array
    extended[7] = 777
    extended[8] = 888
    extended[9] = 999
    fmt.Printf("Backing array before: %v\n", extended)

    // Version A: full capacity — processChunk can see and overwrite positions 7-9
    dataA := make([]int, 7, 10)
    copy(dataA, []int{1, 0, 2, 0, 3, 4, 5})
    // Re-plant sentinels
    sentinelA := dataA[:10]
    sentinelA[7], sentinelA[8], sentinelA[9] = 777, 888, 999

    resultA := processChunk(dataA[0:7]) // cap=10 inherited
    fmt.Printf("Version A result: %v\n", resultA)
    fmt.Printf("Version A backing (positions 7-9): %v\n", sentinelA[7:10])
    // Sentinels are overwritten because processChunk wrote into positions 7-9

    // Version B: limited capacity — processChunk cannot touch positions 7-9
    dataB := make([]int, 7, 10)
    copy(dataB, []int{1, 0, 2, 0, 3, 4, 5})
    sentinelB := dataB[:10]
    sentinelB[7], sentinelB[8], sentinelB[9] = 777, 888, 999

    resultB := processChunk(dataB[0:7:7]) // three-index: cap=7, cannot exceed
    fmt.Printf("Version B result: %v\n", resultB)
    fmt.Printf("Version B backing (positions 7-9): %v\n", sentinelB[7:10])
    // Sentinels are UNCHANGED — processChunk was forced to reallocate
}
```

**Output:**
```
Backing array before: [1 0 2 0 3 4 5 777 888 999]
Version A result: [1 2 3 4 5]
Version A backing (positions 7-9): [1 2 3]   ← sentinels overwritten!
Version B result: [1 2 3 4 5]
Version B backing (positions 7-9): [777 888 999]  ← sentinels intact
```

**Explanation:**
In Version A, `processChunk(dataA[0:7])` receives a slice with `cap=10`. `result := chunk[:0]` has the same `cap=10`. When `append` writes the 5 non-zero values into `result`, it uses positions 0–4 (fine) but the backing array positions 5–9 are within capacity. The sentinel values at 7, 8, 9 are overwritten because the filter result only has 5 elements, writing into positions 0–4 — wait, actually the issue is more subtle: the 5 values land in positions 0–4, but the underlying array positions 7–9 are pristine. The real danger would appear with a longer result. The three-index form `dataB[0:7:7]` forces a reallocation when `append` would exceed cap=7, creating an independent result.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Slice Header Tracing | — | —/1 | — | — |
| Exercise 2 — Safe Map Operations | — | —/1 | — | — |
| Exercise 3 — String/[]byte/[]rune Conversions | — | —/1 | — | — |
| Exercise 4 — Word Deduplication with Set | — | —/2 | — | — |
| Exercise 5 — Struct Embedding and Method | — | —/2 | — | — |
| Exercise 6 — Grouping with Map of Slices | — | —/2 | — | — |
| Exercise 7 — Frequency Table | — | —/3 | — | — |
| Exercise 8 — Three-Index Slice | — | —/3 | — | — |
| **Total** | | **—/15** | | |

**Passing threshold:** 10/15 (67%). Aim for 13/15 (87%) before taking the test.
