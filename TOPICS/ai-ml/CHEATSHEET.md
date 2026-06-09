# Cheat Sheet: Artificial Intelligence and Machine Learning

> Quick reference for the most commonly needed APIs, formulas, and patterns. This is a lookup aid — not a teaching document.

---

## Table of Contents

- [scikit-learn API Cheat Sheet](#scikit-learn-api-cheat-sheet)
- [Loss Functions Reference](#loss-functions-reference)
- [Activation Functions Comparison](#activation-functions-comparison)
- [Evaluation Metrics Quick Reference](#evaluation-metrics-quick-reference)
- [Common Patterns](#common-patterns)

---

## scikit-learn API Cheat Sheet

### The Estimator API (Every model follows this interface)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Preprocess (fit ONLY on train, transform both)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)         # NOT fit_transform

# 3. Train
model = LogisticRegression(C=1.0, max_iter=1000)
model.fit(X_train_scaled, y_train)

# 4. Predict
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]  # probability of class 1

# 5. Evaluate
from sklearn.metrics import classification_report, roc_auc_score
print(classification_report(y_test, y_pred))
print("AUC-ROC:", roc_auc_score(y_test, y_proba))
```

### Pipelines (Prevent data leakage)

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])

# Fit + cross-validate safely (no leakage)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(pipe, X, y, cv=5, scoring="roc_auc")
print(f"AUC: {scores.mean():.3f} ± {scores.std():.3f}")
```

### Common Classifiers

| Class | Key Parameters | Best For |
|-------|---------------|----------|
| `LogisticRegression` | `C` (inverse regularization) | Linear decision boundaries, interpretable |
| `RandomForestClassifier` | `n_estimators`, `max_depth` | Tabular data, handles non-linearity |
| `GradientBoostingClassifier` | `n_estimators`, `learning_rate`, `max_depth` | Best accuracy on tabular data |
| `SVC` | `C`, `kernel`, `gamma` | High-dimensional data, small datasets |
| `KNeighborsClassifier` | `n_neighbors` | Baseline, non-parametric |

### Common Regressors

| Class | Key Parameters | Best For |
|-------|---------------|----------|
| `LinearRegression` | — | Linear relationships, interpretable baseline |
| `Ridge` | `alpha` | When features are correlated (L2 regularization) |
| `Lasso` | `alpha` | Feature selection (L1 regularization, sparsity) |
| `RandomForestRegressor` | `n_estimators`, `max_depth` | Non-linear relationships |
| `GradientBoostingRegressor` | `n_estimators`, `learning_rate` | State-of-the-art on tabular data |

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import loguniform

# Grid search (exhaustive)
param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring="roc_auc")
grid.fit(X_train, y_train)
print(grid.best_params_, grid.best_score_)

# Randomized search (faster for large search spaces)
param_dist = {"model__C": loguniform(1e-3, 1e3)}
rand = RandomizedSearchCV(pipe, param_dist, n_iter=50, cv=5, scoring="roc_auc")
rand.fit(X_train, y_train)
```

---

## Loss Functions Reference

| Loss Function | Formula | Task | Notes |
|--------------|---------|------|-------|
| Mean Squared Error (MSE) | $\frac{1}{n}\sum(y_i - \hat{y}_i)^2$ | Regression | Penalizes large errors heavily; sensitive to outliers |
| Mean Absolute Error (MAE) | $\frac{1}{n}\sum|y_i - \hat{y}_i|$ | Regression | More robust to outliers than MSE |
| Binary Cross-Entropy | $-[y\log\hat{p} + (1-y)\log(1-\hat{p})]$ | Binary classification | Proper scoring rule; use with sigmoid output |
| Categorical Cross-Entropy | $-\sum_c y_c \log \hat{p}_c$ | Multi-class classification | Use with softmax output |
| Huber Loss | MSE if $|e| \leq \delta$, else MAE-like | Regression | Combines MSE smoothness with MAE robustness |
| Hinge Loss | $\max(0, 1 - y\hat{y})$ | SVM / binary classification | Margin-based; requires $y \in \{-1, +1\}$ |

---

## Activation Functions Comparison

| Function | Formula | Range | Pros | Cons |
|----------|---------|-------|------|------|
| ReLU | $\max(0, x)$ | $[0, \infty)$ | Fast, sparse activations, default choice | Dying ReLU problem (neurons stuck at 0) |
| Leaky ReLU | $\max(0.01x, x)$ | $(-\infty, \infty)$ | Fixes dying ReLU | Small negative slope is a hyperparameter |
| Sigmoid | $\frac{1}{1+e^{-x}}$ | $(0, 1)$ | Output interpretable as probability | Vanishing gradients; not zero-centered |
| Tanh | $\frac{e^x - e^{-x}}{e^x + e^{-x}}$ | $(-1, 1)$ | Zero-centered; stronger gradients than sigmoid | Still suffers vanishing gradients |
| GELU | $x \cdot \Phi(x)$ | Approx $(-0.17, \infty)$ | Smooth; used in BERT, GPT | Computationally more expensive |
| Softmax | $\frac{e^{x_i}}{\sum_j e^{x_j}}$ | $(0, 1)$, sums to 1 | Multi-class probability output | Only for output layer in classification |

---

## Evaluation Metrics Quick Reference

### Classification

| Metric | Formula | When to Use |
|--------|---------|-------------|
| Accuracy | $\frac{TP+TN}{TP+TN+FP+FN}$ | Balanced classes only |
| Precision | $\frac{TP}{TP+FP}$ | When false positives are costly (e.g., spam) |
| Recall (Sensitivity) | $\frac{TP}{TP+FN}$ | When false negatives are costly (e.g., cancer screening) |
| F1 Score | $\frac{2 \cdot P \cdot R}{P + R}$ | Imbalanced classes, want balance between P and R |
| AUC-ROC | Area under ROC curve | Overall discriminative ability; threshold-independent |
| AUC-PR | Area under Precision-Recall curve | Heavily imbalanced classes |

### Regression

| Metric | Formula | Notes |
|--------|---------|-------|
| MSE | $\frac{1}{n}\sum(y_i-\hat{y}_i)^2$ | Same units as $y^2$; penalizes outliers |
| RMSE | $\sqrt{MSE}$ | Same units as $y$; interpretable |
| MAE | $\frac{1}{n}\sum|y_i-\hat{y}_i|$ | Robust to outliers |
| R² | $1 - \frac{SS_{res}}{SS_{tot}}$ | Proportion of variance explained; 1 = perfect |
| MAPE | $\frac{100}{n}\sum\left|\frac{y_i-\hat{y}_i}{y_i}\right|$ | Percentage error; undefined when $y_i = 0$ |

---

## Common Patterns

### PyTorch Training Loop

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

model = MyModel()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for epoch in range(num_epochs):
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()           # Clear old gradients
        output = model(batch_X)         # Forward pass
        loss = criterion(output, batch_y)
        loss.backward()                 # Backpropagation
        optimizer.step()                # Update weights

    # Validation
    model.eval()
    with torch.no_grad():
        val_loss = sum(
            criterion(model(X), y).item()
            for X, y in val_loader
        ) / len(val_loader)
    print(f"Epoch {epoch+1}: val_loss={val_loss:.4f}")
```

### MLflow Experiment Tracking

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    mlflow.log_params({"C": 1.0, "max_iter": 1000})

    model = LogisticRegression(C=1.0, max_iter=1000)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")
```

### HuggingFace Inference

```python
from transformers import pipeline

# Zero-shot classification
classifier = pipeline("zero-shot-classification",
                       model="facebook/bart-large-mnli")
result = classifier(
    "This movie was absolutely fantastic!",
    candidate_labels=["positive", "negative", "neutral"]
)
print(result["labels"][0])  # "positive"
```
