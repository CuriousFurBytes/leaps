# Exercises: Module 01 — Introduction to AI and Machine Learning

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Classify real-world problems by ML paradigm

For each of the following applications, identify whether it is best approached with supervised learning, unsupervised learning, or reinforcement learning. Explain your reasoning in one sentence each.

a) A bank wants to flag potentially fraudulent credit card transactions. They have 3 years of historical transactions labeled as "fraud" or "legitimate."

b) A retail company wants to group its customers into segments based on purchasing behavior, with no pre-existing category definitions.

c) A robot arm in a factory needs to learn to pick up objects of various shapes. It receives a positive signal when it successfully picks up an object and a negative signal when it drops it.

d) A hospital wants to predict whether a patient will be readmitted within 30 days, using their discharge records and 2 years of historical readmissions.

e) A music streaming app wants to discover latent "genres" in its catalog without using human-labeled genres.

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Explain the bias-variance tradeoff in plain language

Answer the following questions in 2–3 sentences each:

a) What does it mean for a model to "underfit"? Give a concrete real-world example.

b) What does it mean for a model to "overfit"? Give a concrete real-world example.

c) You train a polynomial regression model and observe the following: training MSE = 0.05, test MSE = 4.7. Is the model underfitting or overfitting? What would you do to fix it?

d) You train a linear regression model on a clearly non-linear dataset and observe: training MSE = 15.2, test MSE = 15.8. Is the model underfitting or overfitting? What would you do?

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Identify data leakage in a given workflow

Read each workflow description and identify whether it contains data leakage. If it does, explain where the leakage occurs and how to fix it.

a) Workflow A:
   1. Normalize all features using the mean and standard deviation of the entire dataset
   2. Split the normalized data into 80% train, 20% test
   3. Train a logistic regression on the training set
   4. Evaluate on the test set

b) Workflow B:
   1. Split the raw data into 80% train, 20% test
   2. Compute the mean and standard deviation of the training set
   3. Normalize the training set using those statistics
   4. Normalize the test set using those same statistics
   5. Train and evaluate

c) Workflow C:
   1. Select the 10 most correlated features with the target using the full dataset
   2. Split into train/test
   3. Train on the selected features
   4. Evaluate on test

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Set up and run the complete ML workflow

Complete the following tasks using Python and scikit-learn. Write your code in the provided starter template.

Load the `wine` dataset from `sklearn.datasets.load_wine()`. This dataset has 178 wine samples with 13 chemical features and 3 wine cultivar classes.

Tasks:
1. Perform basic EDA: print the shape, class distribution, and any missing values
2. Split into 80% train, 20% test with `stratify=y`
3. Scale features using `StandardScaler` (fit on train only)
4. Train a `DecisionTreeClassifier` with `max_depth=4`
5. Evaluate using `classification_report` and report overall accuracy
6. Train a second `DecisionTreeClassifier` with `max_depth=None` (unlimited)
7. Compare the two models' train and test accuracy. Which is overfitting more?

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

wine = load_wine()
X, y = wine.data, wine.target

# Your code here
```

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Understand cross-validation

Using the wine dataset from Exercise 4:

1. Use `cross_val_score` with `cv=10` (10-fold) to estimate the accuracy of a `DecisionTreeClassifier(max_depth=4)`. Report the mean and standard deviation of the 10 scores.
2. Compare the cross-validation estimate to the single train/test split accuracy from Exercise 4. Why might they differ?
3. Why is 10-fold cross-validation a better estimate of generalization performance than a single 80/20 split?

```python
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_wine

wine = load_wine()
X, y = wine.data, wine.target

# Your code here
```

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Compare ML paradigms on real data

The following code loads the digits dataset (8x8 images of handwritten digits 0–9) and applies k-means clustering (an unsupervised method) to see if the algorithm discovers the 10 digit classes without using labels.

Run the code, interpret the output, and answer the questions.

```python
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
import numpy as np

digits = load_digits()
X = digits.data  # Shape: (1797, 64) — 1797 images, 64 pixel features each
y = digits.target  # Shape: (1797,) — 0-9

# Fit k-means with 10 clusters (one per digit class)
kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X)

# Evaluate: how well do clusters align with true classes?
ari = adjusted_rand_score(y, cluster_labels)
nmi = normalized_mutual_info_score(y, cluster_labels)
print(f"Adjusted Rand Index: {ari:.3f}")
print(f"Normalized Mutual Info: {nmi:.3f}")
# ARI and NMI range from 0 (random) to 1 (perfect alignment)
```

Questions:
a) What ARI and NMI scores did you get? What do they tell you?
b) Without labels, k-means still finds structure that correlates with the digit classes. Why can it do this? What assumption does this rely on?
c) If you trained a supervised classifier (e.g., logistic regression) on the same data, would it achieve higher accuracy? Why?

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Build a validation curve and interpret the bias-variance tradeoff

Write code to produce a validation curve for a `DecisionTreeClassifier` on the breast cancer dataset (`sklearn.datasets.load_breast_cancer`), varying `max_depth` from 1 to 20.

Requirements:
1. Use 5-fold cross-validation (not a simple train/test split)
2. Plot or print both mean training accuracy and mean validation accuracy for each depth
3. Identify the depth at which overfitting begins (the "elbow")
4. Identify the depth with the best validation accuracy
5. At the optimal depth, what is the train/validation accuracy gap? Is this acceptable?

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import validation_curve
from sklearn.tree import DecisionTreeClassifier
import numpy as np

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# Your code here — use validation_curve from sklearn.model_selection
```

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Debug a broken ML pipeline

The following code has multiple bugs. Identify each bug, explain what's wrong, and write a corrected version.

```python
# BUGGY CODE — find and fix all issues
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
X, y = iris.data, iris.target

# Bug 1: scaling before split
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Bug 2: wrong split order
X_test, X_train, y_test, y_train = train_test_split(X, y, test_size=0.8)

# Bug 3: evaluating on training data
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_train)
print(f"Accuracy: {accuracy_score(y_train, y_pred):.2%}")
```

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Design a rigorous evaluation framework for an imbalanced problem

You are building a credit default prediction model. The dataset has 95% non-default and 5% default loans (severely imbalanced).

Part A: Evaluation Design
1. Explain why accuracy is a poor metric for this problem
2. Which metric matters more for this business problem — precision or recall? Justify your answer considering the costs of false positives (decline a good customer) and false negatives (approve a defaulting customer)
3. Define a complete evaluation framework: which metrics you would report, how you would create train/validation/test splits, and how you would interpret results

Part B: Implementation
Implement your evaluation framework on the `creditcard` dataset (you may simulate an imbalanced dataset if you don't have access):

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    classification_report
)

# Simulate an imbalanced binary classification dataset
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=10,
    weights=[0.95, 0.05],  # 95% class 0, 5% class 1
    random_state=42
)

# Your evaluation framework here
# Use StratifiedKFold to preserve class proportions across folds
```

Part C: Write a 150-word memo to a non-technical stakeholder explaining what your chosen metrics mean and what the model's performance numbers imply for business operations.
