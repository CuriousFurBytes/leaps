# Exercises: Module 02 — REST Resource Design

## Instructions

Complete each exercise in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Identify the main contract elements in an API example.

List the request method, path, input shape, output shape, and possible errors for one operation from this module.

```text
Operation: choose one operation and annotate its contract.
```

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Practice reading API examples.

Rewrite one example from the module in your own words and explain what each line does.

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Distinguish REST and GraphQL vocabulary.

Create a two-column table mapping five terms from this module to their meaning.

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Design a small request-response flow.

Design a read operation for an `Article` object. Include success and not-found behavior.

```json
{
  "id": "art_123",
  "title": "Example"
}
```

---

### Exercise 5
**Difficulty:** Medium
**Objective:** Explain tradeoffs.

Explain when this module's approach improves client experience and when it increases server responsibility.

---

### Exercise 6
**Difficulty:** Medium
**Objective:** Improve an API error.

Turn a vague error message into a structured error that a client can act on.

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Debug a realistic API design flaw.

Find two problems in this design and propose corrections.

```text
GET /doEverything?userId=7&action=deleteArticle&articleId=123
```

---

### Exercise 8
**Difficulty:** Hard
**Objective:** Write a runnable client request.

Write a `curl` request or GraphQL operation for one non-trivial scenario from this module and explain expected output.

```bash
curl -i https://api.example.test/articles
```

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize design and operations.

Write a short design note explaining how your operation handles compatibility, authorization, pagination or query cost, and observability.
