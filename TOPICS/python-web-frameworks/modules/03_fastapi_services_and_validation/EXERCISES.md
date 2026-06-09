# Exercises: Module 03 — FastAPI Services and Validation

## Instructions

Complete each exercise in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Identify the main concepts in this module.

Write a one-paragraph explanation of the request/response cycle.

### Exercise 2

**Difficulty:** Easy
**Objective:** Run a small Python function.

```python
def health():
    return {"status": "ok"}

print(health())
```

Modify the function to include a version field.

### Exercise 3

**Difficulty:** Easy
**Objective:** Compare framework roles.

List one situation where Flask, FastAPI, and Django would each be a reasonable choice.

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Separate framework logic from domain logic.

Write a plain Python function that validates a username and returns either success or a clear error message.

### Exercise 5

**Difficulty:** Medium
**Objective:** Practice route design.

Design five REST-style routes for a small task tracker.

### Exercise 6

**Difficulty:** Medium
**Objective:** Explain tradeoffs.

Explain how integrated defaults can help and hurt a team.

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Debug an HTTP design issue.

Rewrite a `GET /charge-card` endpoint into a safer design and explain the change.

### Exercise 8

**Difficulty:** Hard
**Objective:** Build a vertical slice.

Create one endpoint, one domain function, and one test for a tiny feature.

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Synthesize framework judgment.

Write an architecture note choosing Django, FastAPI, Flask, or a combination for a product with admin users, public pages, and partner APIs.
