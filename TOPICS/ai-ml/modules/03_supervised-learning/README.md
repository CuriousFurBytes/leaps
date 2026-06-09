# Module 03: Supervised Learning

[← Module 02: Mathematics for ML](../02_math-for-ml/) | [Topic Home](../../README.md) | [Next → Module 04: Unsupervised Learning](../04_unsupervised-learning/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-12--16h-orange)

> The core algorithms of supervised learning: linear and logistic regression, decision trees, random forests, support vector machines, and k-nearest neighbors — with scikit-learn implementations and tuning guidance.

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

Supervised learning is the engine of most production ML systems. This module covers the algorithms you will reach for first on any structured data problem: linear models for interpretability and speed, tree-based models for robustness and accuracy on tabular data, SVMs for high-dimensional data, and k-NN as a non-parametric baseline.

The focus is not just on knowing how to call sklearn's `fit()` method — it is on understanding what each algorithm assumes about the data, why those assumptions make it work (or fail), how to tune each algorithm's hyperparameters, and when to use which algorithm. These judgment calls are what separate practitioners from users.

By the end of this module you will have a working understanding of the full suite of classical supervised algorithms and will be able to select, implement, tune, and evaluate them on real datasets using scikit-learn.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/01_introduction]] — ML workflow, train/test split, evaluation basics
- [[ai-ml/modules/02_math-for-ml]] — Linear algebra (dot products, matrix operations), probability, gradients

### Required Concepts

- **numpy arrays** — matrix operations for understanding algorithm implementations
- **pandas DataFrames** — for data loading and EDA
- **scikit-learn basics** — the Estimator API (`fit`, `predict`, `score`)

---

## Objectives

By the end of this module, you will be able to:

1. Implement and tune linear regression, ridge regression, and lasso regression, and explain the geometric and statistical interpretation of each
2. Implement and tune logistic regression for binary and multi-class classification
3. Explain how decision trees work (splitting criteria, information gain, Gini impurity) and use `max_depth` and `min_samples_leaf` to control overfitting
4. Explain how random forests and gradient boosted trees reduce variance through ensemble methods and tune their key hyperparameters
5. Explain the SVM maximum-margin objective and use kernel trick for non-linear classification
6. Implement k-NN and explain its computational tradeoffs vs. parametric methods
7. Select the right algorithm for a given problem based on dataset size, feature type, interpretability needs, and computational constraints

---

## Theory

### Linear Regression

Linear regression models the relationship between input features and a continuous output as a linear function: $\hat{y} = w_0 + w_1 x_1 + w_2 x_2 + ... + w_d x_d = \mathbf{w}^T \mathbf{x} + b$.

Training means finding weights $\mathbf{w}$ that minimize the mean squared error (MSE): $L = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2$.

The normal equation gives a closed-form solution: $\hat{\mathbf{w}} = (X^T X)^{-1} X^T \mathbf{y}$. For large datasets, gradient descent is used instead.

**Regularization** prevents overfitting by adding a penalty on large weights:
- **Ridge (L2):** adds $\lambda \sum w_j^2$ — shrinks all weights toward zero, keeps all features
- **Lasso (L1):** adds $\lambda \sum |w_j|$ — some weights become exactly zero (feature selection)
- **Elastic Net:** combines L1 and L2

```python
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

diabetes = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(
    diabetes.data, diabetes.target, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

models = {
    "LinearRegression": LinearRegression(),
    "Ridge(alpha=1)": Ridge(alpha=1.0),
    "Lasso(alpha=0.1)": Lasso(alpha=0.1),
}

for name, model in models.items():
    model.fit(X_train_s, y_train)
    y_pred = model.predict(X_test_s)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"{name:25s}: R²={r2:.3f}, RMSE={rmse:.2f}")
    if hasattr(model, "coef_"):
        n_zero = np.sum(np.abs(model.coef_) < 1e-4)
        print(f"  Weights zeroed out: {n_zero}/{len(model.coef_)}")
```

### Decision Trees

A decision tree recursively partitions the feature space by choosing the feature and threshold that maximally reduces impurity. For classification, impurity is measured by Gini impurity or information gain (entropy):

- **Gini impurity:** $G = 1 - \sum_c p_c^2$ where $p_c$ is the fraction of class $c$ in the node
- **Entropy / Information gain:** $H = -\sum_c p_c \log_2 p_c$

The tree splits until each leaf is pure (all one class) or a stopping criterion is met (`max_depth`, `min_samples_leaf`). A fully grown tree will overfit — pruning (via `max_depth`) is essential.

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, stratify=iris.target, random_state=42
)

# Compare an unrestricted tree vs. a depth-limited tree
for max_depth in [None, 3]:
    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    clf.fit(X_train, y_train)
    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)
    print(f"max_depth={str(max_depth):4s}: train={train_acc:.3f}, test={test_acc:.3f}, "
          f"leaves={clf.get_n_leaves()}")
    # Unlimited tree: overfits (train≈1.0, test < train)
    # Depth-3 tree: better generalization

# Visualize the tree structure
clf3 = DecisionTreeClassifier(max_depth=3, random_state=42)
clf3.fit(X_train, y_train)
print("\nTree structure:")
print(export_text(clf3, feature_names=iris.feature_names))
```

### Random Forests and Gradient Boosting

**Random forests** reduce overfitting by training many trees on random subsets of the data (bootstrap sampling) and random subsets of features, then averaging predictions. Each tree has high variance individually, but the average is much more stable.

**Gradient boosting** takes a different approach: trees are trained sequentially, each correcting the errors of the previous ensemble. Gradient boosted trees (GBT) consistently achieve state-of-the-art performance on tabular data. XGBoost, LightGBM, and CatBoost are heavily optimized GBT implementations.

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
import numpy as np

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

models = {
    "RandomForest (100 trees)": RandomForestClassifier(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    print(f"{name:30s}: {scores.mean():.3f} ± {scores.std():.3f}")

# Feature importance — what features does the forest rely on most?
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)
importances = rf.feature_importances_
top_features = np.argsort(importances)[::-1][:5]
print("\nTop 5 most important features:")
for i, idx in enumerate(top_features):
    print(f"  {i+1}. {cancer.feature_names[idx]}: {importances[idx]:.4f}")
```

### Support Vector Machines

SVMs find the **maximum-margin hyperplane** — the decision boundary that maximizes the distance (margin) to the nearest training examples of each class. These nearest examples are the **support vectors**.

The key insight: only the support vectors determine the decision boundary. The rest of the training data could be removed and the model would not change.

The **kernel trick** allows SVMs to work in high-dimensional feature spaces without computing the transformation explicitly. Common kernels: linear, polynomial, RBF (Gaussian).

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, stratify=cancer.target, random_state=42
)

# SVMs are sensitive to feature scale — always standardize
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Hyperparameter search: C (regularization) and gamma (RBF width)
param_grid = {"C": [0.1, 1, 10, 100], "gamma": ["scale", "auto", 0.001, 0.01]}
svm = SVC(kernel="rbf", random_state=42)
grid = GridSearchCV(svm, param_grid, cv=5, scoring="accuracy")
grid.fit(X_train_s, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best CV accuracy: {grid.best_score_:.3f}")
print(f"Test accuracy: {grid.score(X_test_s, y_test):.3f}")
```

### k-Nearest Neighbors

k-NN is the simplest supervised algorithm: to classify a new point, find the k nearest training examples (by Euclidean distance) and predict the most common class among them. No training step — all computation is at prediction time.

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X, y = iris.data, iris.target

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Try different k values
for k in [1, 3, 5, 10, 20]:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_scaled, y, cv=10)
    print(f"k={k:2d}: accuracy = {scores.mean():.3f} ± {scores.std():.3f}")

# k=1: zero training error (memorizes data) but poor generalization
# k too large: decision boundary too smooth (underfits)
# Optimal k: found by cross-validation
```

---

## Key Concepts

**Regularization** — A technique that penalizes model complexity to reduce overfitting. Ridge (L2) shrinks weights smoothly; Lasso (L1) can zero out weights entirely, performing implicit feature selection.

**Gini Impurity** — A measure of how "mixed" the classes are at a decision tree node. $G = 1 - \sum p_c^2$. A node with one class has $G = 0$ (pure). Minimizing Gini guides the tree's splitting decisions.

**Bootstrap Aggregation (Bagging)** — Training multiple models on random samples (with replacement) from the training set, then averaging predictions. The foundation of random forests. Reduces variance.

**Boosting** — Sequentially training models where each new model focuses on the errors of the previous ensemble. Reduces bias AND variance when tuned correctly. The basis of gradient boosting.

**Support Vectors** — The training examples closest to the SVM decision boundary. They are the only examples that determine the boundary — all others could be removed without changing the model.

**Kernel Trick** — A mathematical technique that allows SVMs to implicitly compute dot products in a high-dimensional feature space without ever constructing that space explicitly. Enables non-linear classification at the cost of linear-kernel computational efficiency.

---

## Examples

### Example 1: Algorithm Selection on a Real Dataset

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

wine = load_wine()
X, y = wine.data, wine.target

# Models that need scaling
scaled_models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "SVM (RBF)": SVC(kernel="rbf"),
    "k-NN (k=5)": KNeighborsClassifier(n_neighbors=5),
}

# Models that don't need scaling (tree-based)
tree_models = {
    "DecisionTree (d=5)": DecisionTreeClassifier(max_depth=5),
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

print("Algorithm Comparison on Wine Dataset (5-fold CV accuracy):")
print("-" * 55)

for name, model in scaled_models.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
    scores = cross_val_score(pipe, X, y, cv=5)
    print(f"{name:25s}: {scores.mean():.3f} ± {scores.std():.3f}")

for name, model in tree_models.items():
    scores = cross_val_score(model, X, y, cv=5)
    print(f"{name:25s}: {scores.mean():.3f} ± {scores.std():.3f}")
```

---

## Common Pitfalls

### Pitfall 1: Using Linear Regression for Classification

```python
# WRONG: using LinearRegression for a classification problem
from sklearn.linear_model import LinearRegression
import numpy as np

# Predictions can be outside [0, 1] and are not calibrated probabilities
model = LinearRegression()
# model.predict() can return values like 1.3 or -0.2 — not valid probabilities

# CORRECT: use LogisticRegression for binary/multi-class classification
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
# model.predict_proba() returns calibrated probabilities in [0, 1]
```

### Pitfall 2: Not Scaling Features for Distance-Based or Gradient-Based Models

SVMs, k-NN, and logistic regression are all sensitive to feature scale. A feature with range [0, 10000] will dominate a feature with range [0, 1]. Tree-based models (decision trees, random forests, gradient boosting) are NOT sensitive to scale.

```python
# WRONG: running SVM without scaling
from sklearn.svm import SVC
svm_unscaled = SVC()
svm_unscaled.fit(X_train, y_train)  # Will be dominated by high-variance features

# CORRECT: always use a pipeline with StandardScaler for distance-based models
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
pipe = Pipeline([("scaler", StandardScaler()), ("model", SVC())])
```

### Pitfall 3: Ignoring Class Imbalance in Tree Splitting

By default, decision trees and random forests weight all classes equally. For imbalanced datasets, the tree will be biased toward the majority class.

```python
# CORRECT: use class_weight="balanced" for imbalanced datasets
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=5, class_weight="balanced", random_state=42)
```

---

## Cross-Links

- [[ai-ml/modules/01_introduction]] — The ML workflow and evaluation metrics this module's models are evaluated with
- [[ai-ml/modules/02_math-for-ml]] — Gradients (used by logistic regression), dot products (used by linear and SVM), MLE (theoretical basis of these loss functions)
- [[ai-ml/modules/05_model-evaluation]] — Cross-validation and hyperparameter tuning for the models in this module
- [[ai-ml/modules/06_neural-networks]] — Neural networks generalize the linear model family introduced here

---

## Summary

- **Linear models (regression, logistic regression) are the first thing to try** — they are fast, interpretable, and work well when the relationship is approximately linear.
- **Regularization (Ridge/Lasso) is almost always beneficial** — use Ridge when you want to keep all features, Lasso when you want automatic feature selection.
- **Decision trees are interpretable but prone to overfitting** — always set `max_depth` or `min_samples_leaf`. Use them when you need an explainable model.
- **Random forests and gradient boosting are the best defaults for tabular data** — random forests are easier to tune; gradient boosting typically achieves higher accuracy but requires more careful tuning.
- **SVMs work well in high-dimensional spaces** (text, genomics) but scale poorly to large datasets.
- **k-NN is a useful non-parametric baseline** — requires no training, but prediction is slow on large datasets.
- **Always scale features for SVMs, k-NN, and logistic regression.** Tree-based models do not require scaling.
