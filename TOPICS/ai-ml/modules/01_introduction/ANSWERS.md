# Answers: Module 01 — Introduction to AI and Machine Learning

## Answer Key

### Section 1: Easy Questions

**Q1:** b) An if-else rules engine that flags transactions over $10,000. This is rule-based programming — the rules are hand-coded by a human, not learned from data. All other options involve learning from data.

**Q2:** Machine learning systems learn their behavior from data (examples), rather than having their behavior explicitly programmed by a human as rules. The system improves with exposure to more data.

**Q3:** Supervised learning. The dataset has labeled examples (the churn column = the label), and the goal is to predict a known output (churn/no-churn) for new inputs (new customers). There is direct supervision: the model knows the correct answer for every training example.

**Q4:** Overfitting is when a model performs significantly better on the training data than on unseen test data, because it has memorized training examples (including noise) rather than learning generalizable patterns.

**Q5:** The training set only. The scaler must be fitted using only training data statistics (mean, std), then applied with those same statistics to transform both training and test data. Fitting on test data causes data leakage.

---

### Section 2: Medium Questions

**Q6:** AI is the broadest field — any system exhibiting intelligent behavior, including rule-based systems. ML is a subfield of AI where systems learn from data. Deep learning is a subfield of ML using multi-layer neural networks. A real-world AI-but-not-ML example: IBM Deep Blue (the chess program that defeated Kasparov in 1997) was a rule-based minimax search with handcrafted evaluation functions — no learning from data.

**Q7:** The 98% accuracy matches the majority class baseline (always predict "no disease"). A model that predicts "healthy" for every patient would be 98% accurate while being medically useless. You should ask for the model's recall (sensitivity) on the positive class — specifically, what fraction of diseased patients it correctly identifies. You should also ask for precision (of those it flags as diseased, how many are actually diseased). AUC-ROC is the most appropriate single metric here.

**Q8:** Bias-variance: bias is systematic error from a model too simple to capture the true relationship; variance is sensitivity to the specific training data from a model too complex. In a learning curve (accuracy vs. training set size): underfitting appears as both training and validation accuracy being low and close together (model can't learn even with more data). Overfitting appears as training accuracy high but validation accuracy low with a large gap between them.

**Q9:** Each time you evaluate on the test set and make a decision (e.g., "this model is better, I'll keep it"), you are implicitly fitting to the test set. The test performance reflects your choices, not genuine generalization. This is called "test set leakage" or "p-hacking." The reported test accuracy will be optimistically biased — the model will likely perform worse in production.

**Q10:** `stratify=y` ensures that the class proportions in the training and test sets match the proportions in the full dataset. Without it, by chance you could end up with an unrepresentative split — e.g., all rare-class examples in the training set and none in the test set. This is especially critical for imbalanced datasets and small datasets.

---

### Section 3: Hard Questions

**Q11:** Expected correct code:
```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train_scaled, y_train)

y_pred = clf.predict(X_test_scaled)
print(f"Test accuracy: {accuracy_score(y_test, y_pred):.2%}")
```
Expected test accuracy is approximately 92–95%.

**Q12:** The bug is on line `X_scaled = scaler.fit_transform(X)` — the scaler is fitted on the full dataset (X) before the train/test split, causing data leakage. The test set's mean and standard deviation are used to normalize the training set, giving an optimistic evaluation. Fix: split first, then fit the scaler on `X_train` only.

**Q13:** Training 99.7% vs validation 61.3% is severe overfitting (high variance). The model has memorized the training data including noise. Three interventions in order of likelihood:
1. Reduce model complexity: lower `max_depth` for trees, fewer layers for neural networks, simpler model family altogether
2. Add regularization: L1/L2 penalties, dropout for neural networks, pruning for trees
3. Get more training data: a more complex model may be needed but the training set is too small to constrain it

**Q14:** Supervised learning requires labeled data (input-output pairs), produces a predictive model that can assign labels to new inputs. Unsupervised learning requires only unlabeled inputs, produces discovered structure (clusters, components, anomaly scores). Choose unsupervised even with labels when: labels are noisy or expensive to trust; you want to discover structure not captured by your labels; you want to understand the natural groupings before imposing categories; or as a preprocessing step (feature extraction, dimensionality reduction) before supervised learning.

---

### Section 4: Expert Questions

**Q15:** Complete evaluation framework:
- **Splitting strategy:** Time-based split if temporal (training on older data, testing on newer) to prevent future leakage. Stratified k-fold cross-validation (with k=5 or k=10) on the training portion for model development. The test set must be stratified to preserve the 0.1% fraud rate.
- **Metrics:** Primary: Average Precision (AUC-PR) — more informative than AUC-ROC for highly imbalanced classes. Secondary: Recall@precision_threshold (set a minimum acceptable precision, report recall at that threshold). Also report: dollar value of fraud caught per dollar of review cost (the business metric).
- **Threshold:** Given that false negatives are 50× more costly, set the decision threshold to achieve very high recall (e.g., 95%), accepting lower precision. Compute expected cost = (FN × 50) + (FP × 1) and minimize expected cost rather than maximizing accuracy.
- **Engineering team:** AUC-PR, recall at the chosen threshold, precision at that threshold, model latency, false positive rate, calibration curve.
- **CFO:** Dollar amount of fraud detected per month, false positive rate (% of legitimate transactions incorrectly flagged for review), review queue size, expected monthly savings vs. cost of false positive reviews.

**Q16:** AUC-ROC drop from 91% to 74% over 6 months — possible explanations:
1. **Data drift** — input feature distributions have changed (e.g., customers now use mobile more, changing behavioral patterns). Confirm: compare feature distributions between training time and now using statistical tests (KS test, PSI). Fix: retrain on recent data or add distribution shift features.
2. **Concept drift** — the relationship between features and the target has changed (e.g., fraud patterns evolve). Confirm: compare feature importance and SHAP values over time; check if recent labels follow different patterns. Fix: retrain with recency weighting or online learning.
3. **Label drift** — the base rate of positive cases has changed (6-month seasonality in the target). Confirm: plot positive rate over time. Fix: calibrate the model's threshold or retrain.
4. **Data pipeline issues** — a feature is now being computed differently or has more missing values. Confirm: monitor feature statistics at inference time; compare inference-time feature distributions to training-time. Fix: fix the pipeline.
5. **Sample bias in training data** — the 6-month-old training data was not representative of current distribution. Confirm: look at performance on specific data subgroups. Fix: collect more representative training data.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
