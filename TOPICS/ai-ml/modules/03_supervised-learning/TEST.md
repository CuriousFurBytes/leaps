# Test: Module 03 — Supervised Learning

**Instructions:** Answer all questions directly below each question.
**Total Points:** 37 pts | **Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is the key difference between Ridge and Lasso regularization?
> Answer:

**Q2.** What is the "Gini impurity" at a leaf node that contains only examples of class A?
> Answer:

**Q3.** Name three hyperparameters of `RandomForestClassifier` and briefly describe what each controls.
> Answer:

**Q4.** Why must features be scaled before using an SVM or k-NN, but not before using a random forest?
> Answer:

**Q5.** What is the computational complexity of k-NN prediction for a dataset of n training examples and d features? Why is this a problem for large datasets?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain how a random forest reduces variance compared to a single decision tree. What are the two sources of randomness introduced?
> Answer:

**Q7.** A logistic regression model converges but achieves only 60% accuracy on a linearly separable dataset. What are the most likely causes? How would you diagnose and fix each?
> Answer:

**Q8.** Explain the SVM "maximum margin" objective. Why does maximizing the margin improve generalization?
> Answer:

**Q9.** You have a dataset with 500 features and 200 samples. Which algorithm family would you try first — linear models, tree-based, or SVM? Justify your choice.
> Answer:

**Q10.** Explain the difference between hard margin and soft margin SVM. When would you use each?
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Write sklearn code to train a gradient boosting classifier on the wine dataset, tune it with GridSearchCV over at least 3 hyperparameters, and report the best CV accuracy and test accuracy.
> Answer:
```python
# Write your code here
```

**Q12.** The following code for a random forest achieves 68% accuracy. Identify at least 3 problems and write the corrected version.
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
X, y = load_breast_cancer(return_X_y=True)
rf = RandomForestClassifier(n_estimators=1, max_depth=50)
rf.fit(X, y)
print(f"Accuracy: {rf.score(X, y):.2%}")  # evaluating on training data
```
> Answer:

**Q13.** Compare gradient boosting and random forests. When would you choose each? What are the failure modes of each?
> Answer:

**Q14.** You have a text classification problem: 100,000 documents, 50,000 vocabulary features, 2 classes. Which supervised algorithm would you use and why? What preprocessing would you apply?
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Implement logistic regression from scratch in numpy (no sklearn for the model). Use gradient descent with L2 regularization. Train on the Iris dataset (binary classification: setosa vs. not-setosa). Report train and test accuracy. Compare to `sklearn.linear_model.LogisticRegression`.
> Answer:
```python
# Write your code here
```

**Q16.** A production model based on gradient boosting achieves 94% accuracy but 60% recall on the positive class (rare fraud cases, 1% prevalence). Design a comprehensive strategy to improve recall to >85% while keeping precision >70%. Address: threshold tuning, class weighting, resampling, algorithm choice, and evaluation protocol. Show code where appropriate.
> Answer:

---

## Bonus Question (5 pts)

**Bonus 1.** Implement a k-NN classifier using a KD-tree data structure (not sklearn). Explain why KD-trees reduce k-NN query time from O(nd) to O(d log n) in typical cases, and when this speedup fails. (+5 pts)
> Answer:
