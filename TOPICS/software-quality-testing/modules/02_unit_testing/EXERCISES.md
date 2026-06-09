# Exercises: Module 02 — Unit Testing

## Instructions

Complete each exercise in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Identify behavior worth testing.

List five behaviors in a login or checkout workflow that would matter to users if broken.

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Write a basic assertion.

```python
# Add an assertion that proves the function returns the expected greeting.
def greet(name):
    return f"Hello, {name}!"
```

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Classify test types.

Classify each as unit, integration, E2E, or regression: price rounding, database save, full signup flow, and a fixed duplicate-charge bug.

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Convert risk into tests.

Choose three risks from Exercise 1 and describe the cheapest credible test for each.

### Exercise 5
**Difficulty:** Medium
**Objective:** Improve test names.

Rewrite three vague test names so they describe behavior and expected outcome.

### Exercise 6
**Difficulty:** Medium
**Objective:** Explain tradeoffs.

Explain why an E2E test is not always better than a unit test.

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Debug a weak test.

```python
# Explain why this test is weak, then rewrite it.
def test_result():
    result = True
    assert result
```

### Exercise 8
**Difficulty:** Hard
**Objective:** Write runnable code.

Write a small function and two assertions for a discount rule with one normal case and one edge case.

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize a test strategy.

Design a one-page test strategy for a feature that stores user profile changes and displays them in a browser.

