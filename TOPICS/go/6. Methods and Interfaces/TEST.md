# Test — Module 6: Methods and Interfaces

**Topic:** [[go]]
**Module:** [[go/6. Methods and Interfaces]]

---

## Before You Begin

> [!WARNING]
> **Do not look at ANSWERS.md or your notes during the test.**
> The purpose of this test is to surface what you truly know vs. what you think you know.
> An inflated score is worthless. An honest score shows you exactly where to focus next.

**Instructions:**
1. Close all notes, the module README, and any reference materials.
2. Set a timer. Note your start time below.
3. Attempt every question — partial credit exists.
4. After finishing, grade yourself using ANSWERS.md.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Start time:** ___________
**End time:** ___________
**Total time:** ___________

---

## Scoring Table

| Section | Question Type | Points Each | # Questions | Max Points |
|---------|--------------|-------------|-------------|------------|
| Section 1: Recall | Easy | 1 pt | 5 | 5 pts |
| Section 2: Conceptual | Medium | 2 pts | 3 | 6 pts |
| Section 3: Applied | Hard | 3 pts | 2 | 6 pts |
| Section 4: Scenario | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** What is the difference between a method and a function in Go? Give a one-line example of each that does the same thing.

> _Your answer:_

---

**1.2** Complete the method-set table from memory:

| Type | Methods in its method set |
|------|--------------------------|
| `T` | ? |
| `*T` | ? |

> _Your answer:_

---

**1.3** Does Go require a type to explicitly declare which interfaces it implements (like Java's `implements`)? How does Go determine whether a type satisfies an interface?

> _Your answer:_

---

**1.4** What is the `any` type in Go? When was it introduced, and what is it an alias for?

> _Your answer:_

---

**1.5** Name three important standard library interfaces covered in this module and state how many methods each has.

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why `*T` can call value-receiver methods, but `T` cannot call pointer-receiver methods when stored in an interface. What is the underlying reason for this asymmetry?

> _Your answer:_

---

**2.2** Describe the internal representation of an interface value. What are the two components? Explain what each component contains for: (a) a nil interface, (b) an interface holding `os.Stdout` (a `*os.File`), and (c) an interface holding a typed nil `(*os.File)(nil)`.

> _Your answer:_

---

**2.3** What is the "accept interfaces, return structs" principle? Explain why it applies to both parameters (accept interfaces) and return values (return structs) with a concrete justification for each direction.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go program that:
- Defines an interface `Shape` with methods `Area() float64` and `Name() string`
- Implements `Shape` with two types: `Circle` (with a `Radius float64` field) and `Square` (with a `Side float64` field)
- Writes a function `largestShape(shapes []Shape) Shape` that returns the shape with the largest area
- In `main`, creates a slice of at least 4 shapes and prints the name and area of the largest one

> _Your answer:_

---

**3.2** Write a function `mustRead(r io.Reader, n int) []byte` that reads exactly `n` bytes from `r`, panics with a descriptive message if fewer than `n` bytes are available (or any error occurs), and returns the bytes. Then write a brief `main` demonstrating it with a `strings.Reader`. Also write a version `tryRead(r io.Reader, n int) ([]byte, error)` that returns an error instead of panicking.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague shows you this code and says "the error handling is broken — it always reports an error even for valid inputs":

```go
type DBError struct {
    Code int
    Msg  string
}

func (e *DBError) Error() string {
    return fmt.Sprintf("DB error %d: %s", e.Code, e.Msg)
}

func queryDB(id int) error {
    var dbErr *DBError
    if id <= 0 {
        dbErr = &DBError{Code: 404, Message: "record not found"}
    }
    return dbErr
}

// Caller:
if err := queryDB(42); err != nil {
    log.Fatal("unexpected error:", err)  // always fires!
}
```

a) Identify the exact bug (which line, and why it is a bug).

b) Explain what the interface value `queryDB(42)` returns — describe its internal state using the `(type, value)` model.

c) Write the corrected `queryDB` function.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "Define interfaces at the consumer, not the producer." Explain what this means with a concrete example involving two packages. Why is this better than the alternative? What problem does it solve that exists in languages with explicit `implements` declarations?

Consider at least two perspectives: coupling between packages, and the practical ability to add a new implementation without modifying existing code.

> _Your answer (aim for 4–7 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Design and implement a small plugin system using interfaces:

1. Define an interface `Plugin` with methods `Name() string` and `Execute(input string) (string, error)`
2. Implement two plugins: `UpperPlugin` (converts input to uppercase) and `ReversePlugin` (reverses the input string)
3. Write a `Pipeline` struct that holds a `[]Plugin` and has an `Execute(input string) (string, error)` method that passes the input through each plugin in sequence (output of one is input of next); return on first error
4. In `main`, create a pipeline of `[UpperPlugin, ReversePlugin]`, run it on `"hello world"`, and print the result
5. Bonus within the bonus: make `Pipeline` itself implement `Plugin` (its `Name()` returns the names of all plugins joined by `"→"`) and verify this by passing a `Pipeline` as a `Plugin` to a function that accepts `Plugin`

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the next module?**
> _Your reflection:_

**What score did I get? Do I feel it accurately reflects my understanding?**
> _Your reflection:_

---

## Grading Record

_Append a new row each time you take this test. Do not overwrite previous attempts._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
