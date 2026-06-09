# Test — Module 15: Reflection and Metaprogramming

**Topic:** [[go]]
**Module:** [[go/15. Reflection and Metaprogramming]]

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

**1.1** What does `reflect.TypeOf(x)` return, and what does `reflect.ValueOf(x)` return? How are they different?

> _Your answer:_

---

**1.2** State the Third Law of Reflection in your own words. What concrete requirement must be met for a `reflect.Value` to be settable?

> _Your answer:_

---

**1.3** What is the difference between a value's `reflect.Type` and its `reflect.Kind`? Give a concrete example where the Type and Kind are different strings.

> _Your answer:_

---

**1.4** What method on `reflect.StructField` do you call to retrieve a struct tag value for a specific key (e.g., `"json"`)? What does it return if the key is absent?

> _Your answer:_

---

**1.5** What is `go generate`? What does the `//go:generate` directive do, and when is it executed?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why you must pass a pointer and call `.Elem()` to modify a struct's fields via reflection. What happens if you pass the struct directly (not a pointer) and try to call `SetInt` on one of its fields?

> _Your answer:_

---

**2.2** `encoding/json` uses reflection to marshal and unmarshal structs. Explain at least two things it does using struct tags — specifically, what information does it extract from the `json` struct tag, and how does it use each piece?

> _Your answer:_

---

**2.3** Compare reflection and generics as tools for writing code that works across multiple types. For each approach, describe one situation where it is clearly the better choice, and explain why the other approach would be worse in that situation.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete Go function `PrintStructFields(v interface{})` that:
- Accepts any struct (or pointer to struct)
- Iterates over all exported fields
- Prints each field's name, its `reflect.Kind`, and its current value
- Handles both `T` and `*T` input (normalizes pointers)
- Does not panic for non-struct input (print a message and return)

Show how you would call it with a `Person{Name: "Alice", Age: 30}` struct.

> _Your answer:_

---

**3.2** Write a complete Go function `ZeroFields(ptr interface{}, names ...string)` that:
- Takes a pointer to any struct plus a list of field names to zero out
- For each named field, if it exists and is settable, sets it to its zero value using `reflect.Zero(field.Type())`
- Returns an error (not a panic) if `ptr` is not a pointer to a struct

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague writes the following code intending to update a configuration struct via reflection:

```go
type AppConfig struct {
    MaxWorkers int
    LogLevel   string
    verbose    bool // unexported
}

func updateConfig(cfg AppConfig) {
    v := reflect.ValueOf(cfg)
    v.FieldByName("MaxWorkers").SetInt(8)    // line A
    v.FieldByName("LogLevel").SetString("debug") // line B
    v.FieldByName("verbose").SetBool(true)   // line C
}
```

Identify:

a) What is wrong with this code? How many distinct bugs are present? List each one.

b) For each bug, explain why it causes a panic (or incorrect behavior) rather than a compile error.

c) Rewrite `updateConfig` correctly. It should update `MaxWorkers` and `LogLevel`, skip `verbose` gracefully, and not panic.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "Reflection is a powerful tool, but it should be used sparingly in Go." Do you agree or disagree? Discuss the specific costs of reflection (not just "it's slow") and describe the decision process you would use to choose between reflection, generics, interfaces, and `go generate` when writing a library that needs to handle arbitrary user-defined types.

Consider at least two concrete scenarios in your answer — one where you would reach for reflection and one where you would not.

> _Your answer (aim for 4–8 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Implement a function `DeepCopy(src interface{}) interface{}` that uses reflection to create a deep copy of any struct (not pointer to struct). The copy should:
- Be a new allocation with the same type as `src`
- Have all exported fields copied by value
- Handle nested structs recursively (i.e., if a field is itself a struct, deep copy it too)
- Return the copy as `interface{}`

Show that modifying a field in the copy does not affect the original, and vice versa. You do not need to handle slices, maps, pointers, or channels — only flat and nested structs with scalar fields.

Bonus points for also handling slice fields (making a new slice with copied elements).

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
