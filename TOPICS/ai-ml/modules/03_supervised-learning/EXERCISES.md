# Exercises: Module 03 — Supervised Learning

## Instructions
Complete each exercise in order. Use scikit-learn unless otherwise specified.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Implement the basic supervised learning workflow

Load the `load_wine` dataset. Train a `LogisticRegression` model. Report precision, recall, and F1 for each class. Does the model perform equally well on all three wine types?

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Understand decision tree splitting

Train a `DecisionTreeClassifier(max_depth=2)` on the Iris dataset. Use `export_text()` from `sklearn.tree` to print the tree structure. Trace through the tree manually for one example: which features are checked, and what is the prediction?

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Understand the effect of regularization strength

Train Lasso regression on a synthetic dataset with 20 features (15 of which are irrelevant noise). Use `alpha` values from 0.001 to 10. Plot (or print) the number of non-zero weights vs. alpha. At what alpha do the noise features get zeroed out?

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Build and compare an ensemble

On the breast cancer dataset, compare `DecisionTreeClassifier`, `RandomForestClassifier`, and `GradientBoostingClassifier`. Use 10-fold cross-validation and report AUC-ROC (not accuracy). Which performs best? How much does ensemble size matter for random forest?

---

### Exercise 5
**Difficulty:** Medium
**Objective:** SVM kernel comparison

On the moons dataset (`sklearn.datasets.make_moons` with `noise=0.3`), compare SVM with linear kernel, polynomial kernel (degree=3), and RBF kernel. Use 5-fold CV. Which kernel works best for this data shape and why?

---

### Exercise 6
**Difficulty:** Medium
**Objective:** Hyperparameter tuning for random forest

Use `RandomizedSearchCV` to tune a `RandomForestClassifier` on the digits dataset. Search over: `n_estimators` [50, 100, 200], `max_depth` [None, 10, 20], `min_samples_leaf` [1, 2, 5], `max_features` ["sqrt", "log2"]. Report best parameters and compare to default settings.

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Debug a broken logistic regression pipeline

The following pipeline achieves 52% accuracy on the breast cancer dataset (expected: ~95%). Find and fix all bugs.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_test)   # bug?
X_test = scaler.transform(X_train)       # bug?

model = LogisticRegression(max_iter=10)  # bug?
model.fit(X_test, y_test)               # bug?
print(model.score(X_train, y_train))    # bug?
```

---

### Exercise 8
**Difficulty:** Hard
**Objective:** Feature importance analysis

Train a `RandomForestClassifier` on the breast cancer dataset. Extract feature importances. Retrain using only the top 10 most important features. Does accuracy improve, stay the same, or decrease? Try again with only the top 5. What does this tell you about feature redundancy in this dataset?

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Implement gradient boosting from scratch

Implement a minimal gradient boosting classifier in numpy that:
1. Uses decision stumps (depth=1 trees) as base learners
2. Trains each stump on the negative gradient of the log-loss
3. Uses a fixed learning rate (0.1)
4. Trains for 50 rounds

Compare your implementation's accuracy to `sklearn.ensemble.GradientBoostingClassifier` on the breast cancer dataset. They should be close (within 2–3%).
