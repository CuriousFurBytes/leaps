# Exercises: Module 01 — Foundations of Distributed Systems

## Instructions
Complete each exercise in order. Exercises increase in difficulty. Submit answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Define the module's core vocabulary.

Write concise definitions for five key concepts from the module.

### Exercise 2
**Difficulty:** Easy
**Objective:** Connect concepts to examples.

For each key concept, name one real system where it appears.

### Exercise 3
**Difficulty:** Easy
**Objective:** Run a small example.

Run one code sample from the README and explain each output line.

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Compare design choices.

Create a table comparing synchronous calls, queued work, and event publication for one workflow.

### Exercise 5
**Difficulty:** Medium
**Objective:** Identify failure modes.

List three ways the workflow can fail and the signal that would reveal each failure.

### Exercise 6
**Difficulty:** Medium
**Objective:** Improve an architecture sketch.

Revise this sketch with one explicit timeout, one retry rule, and one observability signal.

```yaml
service: example
calls:
  - dependency
```

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Write runnable code.

Implement a small idempotent handler for repeated message IDs in a language you know.

### Exercise 8
**Difficulty:** Hard
**Objective:** Debug realistic behavior.

Given a queue that grows forever during peak traffic, diagnose whether the cause is producer rate, consumer rate, retry storms, or missing backpressure.

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize architecture and operations.

Write a one-page design note that explains the tradeoff you would choose for a high-volume workflow covered by this module.
