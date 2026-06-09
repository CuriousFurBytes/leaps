# Module 02: Data and Features

> Learn how data becomes model-ready through measurement, cleaning, splitting, and feature design.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

Models learn from representations, not from reality directly. Data is a measurement of the world, and every measurement has omissions, bias, timing, and context. This module explains why professional ML work often spends more time on data than on algorithms. Good features make useful signals visible; bad features leak answers, encode unfair proxies, or disappear in production.

The practical goal is to become skeptical in a productive way. When a model reports a score, ask what data produced that score, what was held out, what the metric ignores, and what would happen if the world changed. This habit separates demos from reliable systems. Even at the beginner stage, you will practice making assumptions explicit.

## Prerequisites

- Module 01: Foundations in this topic.
- Basic [[python]] syntax: variables, lists, loops, and functions.
- Comfort reading small tables and asking what each column means.

## Objectives

By the end of this module, you will be able to:

- Explain the role of data, models, parameters, and evaluation.
- Implement a tiny runnable experiment in Python.
- Identify common failure modes before trusting a score.
- Connect this module to [[statistics]] and [[python]].
- Describe when a simple baseline is more useful than complexity.

## Theory

### The Core Loop

Machine learning work repeats a loop: define a task, collect examples, choose a representation, fit a pattern, evaluate on held-out data, and revise. This loop matters because each stage can invalidate the next. A beautiful model trained on mislabeled data is still unreliable. A high score on leaked validation data is not evidence of real performance. Historically, AI moved from hand-coded rules toward learned patterns because many tasks were too messy to specify manually.

```python
# A tiny pattern learner: choose a threshold that separates small and large values.
examples = [1, 2, 3, 8, 9, 10]
labels = ["small", "small", "small", "large", "large", "large"]
threshold = (max(examples[:3]) + min(examples[3:])) / 2
prediction = "large" if 7 > threshold else "small"
print(threshold, prediction)
```

### Evidence Before Complexity

A baseline is the simplest defensible solution. It might be a rule, an average, or a linear model. Baselines are not embarrassing; they are scientific controls. Without one, you cannot tell whether a neural network, boosted tree, or retrieval system adds value. Professionals often ship simple models because they are easier to monitor, debug, explain, and improve.

```python
# Baseline classifier: always predict the most common label.
labels = ["no", "no", "yes", "no"]
majority = max(set(labels), key=labels.count)
predictions = [majority for _ in labels]
accuracy = sum(a == b for a, b in zip(labels, predictions)) / len(labels)
print(majority, accuracy)
```

### Evaluation Is a Design Choice

Metrics are compressed stories about performance. Accuracy can hide rare but costly failures. Mean error can hide disastrous outliers. A model can look good overall while failing for a subgroup. Evaluation must reflect the real decision, not just mathematical convenience. The safest habit is to combine aggregate metrics with example-level inspection and slice analysis.

```python
# Simple accuracy with explicit length validation.
def accuracy(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError("Labels and predictions must have the same length")
    correct = sum(actual == predicted for actual, predicted in zip(y_true, y_pred))
    return correct / len(y_true)

print(accuracy([1, 0, 1], [1, 1, 1]))
```

## Key Concepts

- **Artificial intelligence** — The broad field of building systems that perform tasks associated with intelligent behavior. ML is one major approach inside AI.
- **Machine learning** — A method for fitting behavior from data rather than writing every rule manually. It depends on examples, assumptions, and evaluation.
- **Feature** — A measurable part of the workflow that shapes what the model can learn. Poor choices here can dominate algorithm choice.
- **Baseline** — A simple reference solution. It protects you from mistaking complexity for progress.
- **Generalization** — Performance on new examples rather than memorized examples. It is the main reason held-out evaluation exists.
- **[[shared/glossary#overfitting]]** — A model fitting training quirks too closely. It often appears as excellent training performance and weak new-data performance.

## Examples

### Scenario: Decide Whether ML Is Needed

Problem: a team wants AI for routing support tickets. Start by checking whether a simple keyword rule solves enough cases.

```python
# Keyword baseline for routing tickets.
def route_ticket(text):
    text = text.lower()
    if "invoice" in text or "refund" in text:
        return "billing"
    if "password" in text or "login" in text:
        return "account"
    return "general"

print(route_ticket("I need a refund for my invoice"))
```

This approach is transparent and cheap. If it fails often, those failures become training examples for a later model.

## Common Pitfalls

### Pitfall 1: Trusting Training Accuracy

Wrong approach:

```python
training_accuracy = 0.99
print("Ready to deploy", training_accuracy)
```

Correct approach:

```python
validation_accuracy = 0.76
print("Investigate held-out errors before deployment", validation_accuracy)
```

Training accuracy can reward memorization. Held-out examples better estimate generalization.

### Pitfall 2: Skipping the Baseline

Wrong approach:

```python
model = "largest neural network available"
print(model)
```

Correct approach:

```python
baseline = "majority class or simple linear model"
next_model = "chosen only after baseline is measured"
print(baseline, next_model)
```

A baseline tells you whether complexity buys anything.

### Pitfall 3: Ignoring Data Meaning

Wrong approach:

```python
feature = "approved_by_manager"
print("Use as predictor", feature)
```

Correct approach:

```python
feature = "approved_by_manager"
print("Check whether this is only known after the decision", feature)
```

Some features leak the answer because they are created after the event you want to predict.

## Cross-Links

- [[ai-ml]]
- [[python]]
- [[statistics]]
- [[shared/glossary#overfitting]]

## Summary

- AI is broad; ML is a data-driven approach within AI.
- ML projects require problem framing, data, representation, modeling, and evaluation.
- Baselines are necessary controls, not beginner shortcuts.
- Metrics compress reality and must match the decision being supported.
- Generalization matters more than memorizing training examples.
- Responsible practice starts at the first dataset, not after deployment.
