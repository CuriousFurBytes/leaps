# Exercises: Module 03 — Supervised Learning

## Instructions

Complete each exercise in order. Exercises increase in difficulty. Submit answers by editing this file or committing a separate solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Recall key vocabulary from the module.

Create a glossary with five terms from this module and one original example for each.

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Run a small Python experiment.

Run this starter script and change one value. Describe the result.

```python
values = [1, 2, 3, 4]
mean = sum(values) / len(values)
print(mean)
```

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Identify inputs and outputs.

For a real system you use, list the likely data inputs, model output, and human decision affected.

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Explain a tradeoff.

Compare a simple baseline with a more complex model. When is the baseline better?

### Exercise 5
**Difficulty:** Medium
**Objective:** Interpret a tiny dataset.

Given a table of ten examples, propose two useful features and one feature that may leak the answer.

### Exercise 6
**Difficulty:** Medium
**Objective:** Practice reproducibility.

Write the exact commands needed to create an environment and run a script for this module.

```bash
python -m venv .venv
source .venv/bin/activate
python module_practice.py
```

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Debug model reasoning.

Find a plausible reason a model performs well in training but poorly on new examples. Propose a test.

### Exercise 8
**Difficulty:** Hard
**Objective:** Write runnable code.

Implement a small function that computes accuracy from labels and predictions.

```python
def accuracy(y_true, y_pred):
    correct = sum(1 for actual, pred in zip(y_true, y_pred) if actual == pred)
    return correct / len(y_true)
```

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize concepts into a design.

Design a miniature ML workflow for a domain you care about. Include data, baseline, metric, risk, and monitoring plan.
