# Test — Module 11: Testing and Benchmarking

**Topic:** [[go]]
**Module:** [[go/11. Testing and Benchmarking]]

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

**1.1** What is the difference between `t.Error`/`t.Errorf` and `t.Fatal`/`t.Fatalf`? Give one example of when you would choose `t.Fatal` over `t.Error`.

> _Your answer:_

---

**1.2** What does `b.N` represent in a Go benchmark function? Who sets its value, and why should you never set it yourself?

> _Your answer:_

---

**1.3** What flag do you pass to `go test` to run only tests whose names match a pattern? Write the command to run only tests whose names contain "Parse".

> _Your answer:_

---

**1.4** What is `t.Helper()` and why is it important to call it at the start of test helper functions?

> _Your answer:_

---

**1.5** What is the naming convention for Go test files and test functions? Name the three function signature conventions for the three types of automated tests (unit test, benchmark, fuzz test).

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why Go's community prefers hand-written fakes over mock frameworks (like `gomock` or `testify/mock`). What role do Go's interfaces play in making fakes practical? Reference the concept of structural typing in your answer.

> _Your answer:_

---

**2.2** Explain the loop variable capture bug in parallel table-driven tests (pre-Go 1.22). Why does it happen, what symptom does it cause, and what is the fix?

> _Your answer:_

---

**2.3** What is the difference between running a fuzz test with `go test -run FuzzXxx` versus `go test -fuzz FuzzXxx`? What happens in each case, and when would you use each?

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** Write a complete, idiomatic table-driven test for the following function. Your test must include at least 4 cases, use `t.Run` subtests, and follow the `wantErr bool` pattern for error checking:

```go
func Sqrt(x float64) (float64, error) {
    if x < 0 {
        return 0, fmt.Errorf("sqrt of negative number: %v", x)
    }
    return math.Sqrt(x), nil
}
```

> _Your answer:_

---

**3.2** Write a benchmark for the following two implementations. Ensure that the setup (building the input map) is not included in the ns/op measurement. Add a comment explaining which implementation you would expect to be faster and why.

```go
// LookupSlice searches for key in a slice of key-value pairs.
func LookupSlice(pairs [][2]string, key string) (string, bool) {
    for _, p := range pairs {
        if p[0] == key {
            return p[1], true
        }
    }
    return "", false
}

// LookupMap looks up key in a map.
func LookupMap(m map[string]string, key string) (string, bool) {
    v, ok := m[key]
    return v, ok
}
```

Use 1000 key-value pairs and look up a key that exists near the middle of the collection.

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A colleague wrote the following benchmark, but the results seem unreliable — sometimes showing 0 ns/op. Identify what is wrong, explain why it produces incorrect results, and rewrite it correctly.

```go
func BenchmarkProcessItems(b *testing.B) {
    for i := 0; i < b.N; i++ {
        items := generateItems(1000) // expensive setup — takes ~10ms
        result := ProcessItems(items)
        _ = result
    }
}
```

a) What is wrong with this benchmark?

b) Why does it produce incorrect or misleading results?

c) Rewrite it correctly.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** "Go's `testing` package deliberately provides no assertion library — no `assertEqual`, no `assertNotNil`, no `assertContains`. This is a design decision, not an omission."

Do you agree? Explain why this design decision might be justified, what its trade-offs are, and what you gain or lose compared to using a library like `testify/assert`. Consider what happens when a test fails in each approach.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** Write a complete fuzz test for the following base64 codec — one that checks both directions of the round-trip: encode then decode, and also decode then encode (where the input is valid base64).

```go
func Encode(data []byte) string {
    return base64.StdEncoding.EncodeToString(data)
}

func Decode(s string) ([]byte, error) {
    return base64.StdEncoding.DecodeString(s)
}
```

Your fuzz test must:
1. Use `f.Add([]byte(...))` seed entries (including an empty slice)
2. Assert the round-trip invariant: `Decode(Encode(data))` must return data equal to the original
3. Assert that `Encode` never returns an empty string for non-empty input
4. Handle the case where `Decode` is called with arbitrary strings (most will be invalid base64)

Explain which invariant is most likely to find bugs in a real implementation of this codec.

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
