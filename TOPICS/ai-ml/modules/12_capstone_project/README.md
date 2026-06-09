# Module 12: Capstone Project

> Build an end-to-end applied machine learning system with documentation, evaluation, and responsible deployment decisions.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Project Brief](#project-brief)
5. [Milestones](#milestones)
6. [Help and Getting Unstuck](#help-and-getting-unstuck)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

The capstone is where the AI and ML learning path becomes a practitioner portfolio artifact. Instead of receiving a complete solution, you will make and defend decisions: what problem is worth solving, what data is appropriate, which baseline is honest, what metric matters, which model is good enough, and what risks remain. The goal is not to maximize a leaderboard score; the goal is to show judgment.

A professional ML project is a system of evidence. Your model is only one part of that system. The surrounding artifacts — data documentation, evaluation design, error analysis, reproducible training commands, model card, monitoring plan, and stakeholder recommendation — are what make the work trustworthy. Historically, many AI failures have come from treating a high validation score as permission to deploy without understanding data collection, feedback loops, or harm.

You should choose a project small enough to finish but real enough that a practitioner would recognize it. Good capstones include text classification, forecasting, tabular risk scoring, recommendation prototypes, or image classification with clear constraints. Avoid projects where labels are vague, stakes are high, or data rights are unclear unless the project is explicitly a risk analysis rather than a deployment proposal.

## Prerequisites

- Modules 01–11 in [[ai-ml]] or equivalent experience.
- Comfort with [[python]], [[statistics]], feature engineering, evaluation, and model comparison.
- Ability to explain uncertainty, tradeoffs, and responsible AI concerns.

## Objectives

By the end of this module, you will be able to:

- Design a realistic AI or ML project from problem framing through evaluation.
- Implement a reproducible baseline and at least one improved model.
- Diagnose errors by segment, feature, and example type.
- Produce data and model documentation suitable for review.
- Defend deployment, delay, or cancellation using evidence.

## Project Brief

Build a decision-support system that uses data to produce a prediction, ranking, grouping, generated recommendation, or alert. Your system must include a human-readable explanation of what the model can and cannot do. The project must not present predictions as unquestionable truth.

```python
from dataclasses import dataclass

@dataclass
class PredictionReport:
    model_name: str
    metric_name: str
    metric_value: float
    known_limitations: list[str]

report = PredictionReport(
    model_name="baseline-logistic-regression",
    metric_name="validation_f1",
    metric_value=0.71,
    known_limitations=["small dataset", "labels reflect historical decisions"],
)
print(report)
```

The example above is deliberately simple: the output combines a metric with limitations. A capstone-worthy system keeps this habit everywhere. Numbers without context are not enough.

## Milestones

1. Problem framing: user, decision, cost of errors, and success criteria.
2. Data audit: source, fields, missingness, leakage risks, sensitive attributes, and licensing.
3. Baseline: simple rule or simple model with reproducible command.
4. Model iteration: at least one justified improvement over the baseline.
5. Evaluation: held-out results, slice analysis, and error examples.
6. Responsible review: privacy, fairness, misuse, uncertainty, and rollback plan.
7. Final recommendation: ship, delay, or cancel with evidence.

## Help and Getting Unstuck

### Hint 1: If the project feels too large

Shrink the decision. Instead of "predict customer behavior," try "classify whether a support ticket needs billing-team review." A smaller decision makes labels, metrics, and errors easier to inspect.

### Hint 2: If the model is not improving

Return to the baseline. Check whether data splits are correct, labels are meaningful, and features are available at prediction time. More complex models cannot fix invalid framing.

```python
def validate_split(train_ids, test_ids):
    overlap = set(train_ids) & set(test_ids)
    if overlap:
        raise ValueError(f"Leakage detected for ids: {sorted(overlap)[:5]}")
    return True
```

### Hint 3: If evaluation is confusing

Write down the decision cost matrix. False positives and false negatives rarely matter equally. Choose a threshold that matches the real cost of mistakes rather than blindly accepting a default.

```python
def expected_cost(false_positives, false_negatives, fp_cost=1, fn_cost=5):
    return false_positives * fp_cost + false_negatives * fn_cost
```

## Acceptance Criteria

- The repository or folder can be run from documented setup commands.
- The project includes a baseline and at least one comparison model.
- The final report includes metrics, error analysis, limitations, and a responsible AI review.
- The recommendation is explicit: ship, delay, or cancel.
- No full copy-paste solution is provided by this module; the learner must drive implementation choices.

## Cross-Links

- [[ai-ml#module-map]]
- [[python]]
- [[statistics]]
- [[ethics]]
- [[data-structures]]

## Summary

- The capstone proves end-to-end judgment, not just modeling ability.
- A trustworthy ML project includes data, evaluation, documentation, and risk controls.
- Baselines are required because they make improvement measurable.
- Error analysis explains where a model fails and whether those failures are acceptable.
- Deployment decisions must balance evidence, impact, uncertainty, and maintainability.
