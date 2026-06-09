# Module 05: Model Evaluation

[← Module 04: Unsupervised Learning](../04_unsupervised-learning/) | [Topic Home](../../README.md) | [Next → Module 06: Neural Networks](../06_neural-networks/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-10--12h-orange)

> How to rigorously evaluate ML models: cross-validation, the full suite of classification and regression metrics, hyperparameter tuning strategies, and model selection.

---

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

---

## Overview

The most common reason production ML systems fail is not because the model is wrong — it is because the evaluation was wrong. Overly optimistic test scores, data leakage, wrong metrics, uncalibrated probabilities, and hyperparameter overfitting are all evaluation failures that lead to models that look great in development but underperform in production.

This module is about rigor. You will learn how to get trustworthy estimates of model performance, how to compare models fairly, how to tune hyperparameters without overfitting to the validation set, and how to choose the right metric for the right problem. These skills are prerequisites for everything that follows.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/01_introduction]] — train/test split, overfitting, basic workflow
- [[ai-ml/modules/03_supervised-learning]] — the algorithms being evaluated

### Required Concepts

- **Confusion matrix** — TP, FP, TN, FN (introduced in Module 01)
- **Basic statistics** — mean, variance, confidence intervals

---

## Objectives

By the end of this module, you will be able to:

1. Apply k-fold and stratified k-fold cross-validation and explain when each is appropriate
2. Compute and interpret precision, recall, F1, AUC-ROC, and AUC-PR for classification
3. Choose the appropriate evaluation metric for a given business problem
4. Tune hyperparameters using grid search, random search, and Bayesian optimization
5. Use the holdout test set correctly and explain why it must only be used once
6. Compute and interpret calibration curves to assess whether model probabilities are meaningful

---

## Theory

### Cross-Validation

Cross-validation gives a more reliable estimate of generalization performance than a single train/test split, because it averages over multiple different partitions of the data.

In **k-fold CV**, the data is split into k equal folds. The model is trained on k-1 folds and evaluated on the held-out fold, repeated k times. The final score is the mean (with standard deviation) across all k scores.

**Stratified k-fold** preserves class proportions in each fold — essential for imbalanced datasets.

```python
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
import numpy as np

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Regular k-fold
kf_scores = cross_val_score(clf, X, y, cv=10, scoring="roc_auc")
print(f"K-fold CV AUC:     {kf_scores.mean():.3f} ± {kf_scores.std():.3f}")

# Stratified k-fold — use when classes are imbalanced
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
skf_scores = cross_val_score(clf, X, y, cv=skf, scoring="roc_auc")
print(f"Stratified CV AUC: {skf_scores.mean():.3f} ± {skf_scores.std():.3f}")

# Note: for classifiers, cross_val_score already uses stratified CV by default
# For regressors, it uses regular k-fold
```

### Classification Metrics

Different metrics answer different business questions. Choosing the wrong metric can lead to a technically correct but practically useless model.

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    classification_report, confusion_matrix, roc_curve
)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

# Create imbalanced binary classification problem (10% positive)
X, y = make_classification(n_samples=1000, weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                     stratify=y, random_state=42)
clf = LogisticRegression(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]  # Probability of positive class

print("=== Classification Metrics ===")
print(f"Accuracy:          {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision:         {precision_score(y_test, y_pred):.3f}")
print(f"Recall:            {recall_score(y_test, y_pred):.3f}")
print(f"F1 Score:          {f1_score(y_test, y_pred):.3f}")
print(f"AUC-ROC:           {roc_auc_score(y_test, y_proba):.3f}")
print(f"Average Precision: {average_precision_score(y_test, y_proba):.3f}")

print("\n=== Full Report ===")
print(classification_report(y_test, y_pred))
# Note how accuracy can be high (90%) while recall is low
# This is the imbalanced class trap
```

**Metric selection guide:**
| Business question | Use this metric |
|---|---|
| "How often is the model right overall?" | Accuracy (only for balanced classes) |
| "When it predicts positive, is it right?" | Precision |
| "Does it find all the positives?" | Recall (sensitivity) |
| "Balance between precision and recall?" | F1 |
| "Overall discriminative ability?" | AUC-ROC |
| "Performance on the rare positive class?" | Average Precision (AUC-PR) |

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from scipy.stats import loguniform, randint

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# Grid search — exhaustive, use for small search spaces
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.01, 0.1, 0.2],
}
grid = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="roc_auc",
    n_jobs=-1,  # Use all CPU cores
)
grid.fit(X, y)
print(f"Grid search best params: {grid.best_params_}")
print(f"Grid search best AUC:    {grid.best_score_:.3f}")

# Random search — better for large search spaces
# Samples n_iter combinations randomly
param_dist = {
    "n_estimators": randint(50, 500),
    "max_depth": randint(2, 10),
    "learning_rate": loguniform(0.001, 0.5),
    "subsample": loguniform(0.5, 1.0),
}
rand_search = RandomizedSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_dist,
    n_iter=50,       # Try 50 random combinations
    cv=5,
    scoring="roc_auc",
    random_state=42,
    n_jobs=-1,
)
rand_search.fit(X, y)
print(f"\nRandom search best params: {rand_search.best_params_}")
print(f"Random search best AUC:    {rand_search.best_score_:.3f}")
```

---

## Key Concepts

**Cross-Validation** — A technique for getting reliable performance estimates by training and evaluating the model on multiple different partitions of the data. Reduces the variance of the performance estimate.

**Precision** — Of all the positive predictions the model makes, what fraction are actually positive? $P = TP / (TP + FP)$. High precision = few false alarms.

**Recall (Sensitivity)** — Of all the actual positives, what fraction does the model find? $R = TP / (TP + FN)$. High recall = few missed positives.

**AUC-ROC** — Area under the Receiver Operating Characteristic curve. Measures the model's ability to discriminate between classes at all possible thresholds. 1.0 = perfect, 0.5 = random.

**Calibration** — Whether the model's probability estimates are accurate. A calibrated model that says "70% probability" should be right about 70% of the time. Poor calibration is common and leads to bad downstream decisions.

**Hyperparameter** — A parameter set before training, not learned from data. Examples: tree depth, regularization strength, learning rate. Hyperparameter tuning finds the settings that maximize validation performance.

---

## Examples

### Example 1: The Full Evaluation Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# 1. Hold out a test set — never touch until the very end
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 2. Build pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(random_state=42, max_iter=1000)),
])

# 3. Tune on development set with nested CV
param_grid = {"clf__C": [0.001, 0.01, 0.1, 1, 10, 100]}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring="roc_auc")
grid.fit(X_dev, y_dev)

print(f"Best C: {grid.best_params_['clf__C']}")
print(f"Dev AUC (5-fold CV): {grid.best_score_:.3f}")

# 4. Final evaluation on test set — do this ONCE
best_model = grid.best_estimator_
y_proba = best_model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, y_proba)
print(f"\nFinal test AUC: {test_auc:.3f}")
print(classification_report(y_test, best_model.predict(X_test)))
```

---

## Common Pitfalls

### Pitfall 1: Hyperparameter Overfitting to the Validation Set

Running many hyperparameter combinations on the same validation set is itself a form of overfitting. The solution is nested cross-validation: the inner loop tunes hyperparameters, the outer loop evaluates the tuning process.

```python
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# Nested CV: inner CV tunes, outer CV evaluates
inner_cv = GridSearchCV(
    Pipeline([("sc", StandardScaler()), ("clf", SVC())]),
    {"clf__C": [0.1, 1, 10]},
    cv=5,
)
outer_scores = cross_val_score(inner_cv, X, y, cv=5, scoring="accuracy")
print(f"Nested CV accuracy: {outer_scores.mean():.3f} ± {outer_scores.std():.3f}")
```

### Pitfall 2: Using Default Threshold of 0.5 for All Problems

The 0.5 threshold is arbitrary. For imbalanced problems or when false positives and false negatives have different costs, the optimal threshold is different.

```python
# Find threshold that maximizes F1 on validation set
from sklearn.metrics import f1_score
import numpy as np

thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = [f1_score(y_val, y_proba_val >= t) for t in thresholds]
best_threshold = thresholds[np.argmax(f1_scores)]
print(f"Best threshold for F1: {best_threshold:.2f}")
```

### Pitfall 3: Reporting Mean CV Score Without Standard Deviation

A CV score of 0.95 ± 0.01 is very different from 0.95 ± 0.12. Always report both mean and standard deviation.

---

## Cross-Links

- [[ai-ml/modules/01_introduction]] — First introduction to train/test split and basic evaluation
- [[ai-ml/modules/03_supervised-learning]] — The algorithms evaluated in this module
- [[ai-ml/modules/09_ml-engineering]] — Production monitoring is essentially continuous evaluation
- [[ai-ml/modules/11_responsible-ai]] — Fairness metrics are a specialized form of evaluation

---

## Summary

- **Cross-validation gives more reliable performance estimates** than a single train/test split, because it averages over multiple partitions.
- **Use stratified k-fold for classification** to preserve class proportions in each fold.
- **Choose metrics that match your business objective.** Accuracy is almost never the right metric for production systems.
- **AUC-ROC is threshold-independent** and measures discriminative ability. AUC-PR is better for heavily imbalanced classes.
- **Calibration matters** when your model's probability estimates feed into decisions. Uncalibrated probabilities are dangerous.
- **Hyperparameter tuning must be done on a separate validation set** (or via inner CV), not the test set.
- **Report mean ± std** for all CV scores. A model with high mean but high variance is unreliable.
