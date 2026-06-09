# Module 11: Responsible AI

[← Module 10: LLMs and Generative AI](../10_llms-and-generative-ai/) | [Topic Home](../../README.md) | [Next → Module 12: Capstone Project](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-purple)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> Building ML systems responsibly: fairness metrics, bias detection and mitigation, explainability (SHAP, LIME), privacy-preserving ML (differential privacy, federated learning), and AI governance.

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

ML systems affect people. A credit scoring model determines who gets a loan. A medical imaging system determines who receives treatment. A hiring algorithm determines who gets a job interview. When these systems are biased — or when they fail in ways that disproportionately affect certain groups — the consequences are real and sometimes irreversible.

This module treats responsible AI not as a compliance checkbox but as an engineering discipline. Fairness, explainability, and privacy have precise mathematical formulations, measurable properties, and concrete technical interventions. A responsible ML practitioner can quantify bias in a model, explain a prediction to a stakeholder, and reason about the privacy implications of training on sensitive data.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/03_supervised-learning]] — The models being audited for fairness
- [[ai-ml/modules/05_model-evaluation]] — Evaluation metrics; the module extends them with fairness metrics

### Required Concepts

- **Confusion matrix and derived metrics** — TP, FP, FN, TN, precision, recall
- **Probability and Bayes' theorem** — used in fairness metric derivations

---

## Objectives

By the end of this module, you will be able to:

1. Define and compute group fairness metrics: demographic parity, equalized odds, calibration, and individual fairness
2. Detect bias in a trained model using SHAP and fairness metrics
3. Apply bias mitigation techniques: pre-processing (resampling), in-processing (fairness constraints), and post-processing (threshold adjustment)
4. Use SHAP to explain individual model predictions and global feature importance
5. Use LIME to generate local explanations for model predictions on text and tabular data
6. Explain the privacy-utility tradeoff in differential privacy and describe the federated learning paradigm

---

## Theory

### Fairness Metrics

"Fairness" has multiple mathematical definitions that are often mutually exclusive. Understanding the differences is essential for making defensible choices.

Let $A$ be a protected attribute (e.g., sex, race), $\hat{Y}$ be the model's prediction, and $Y$ be the true label.

```python
import numpy as np
from sklearn.metrics import confusion_matrix

def compute_fairness_metrics(y_true, y_pred, sensitive_attr):
    """
    Compute common group fairness metrics for a binary classifier.

    Args:
        y_true: True labels (0 or 1)
        y_pred: Predicted labels (0 or 1)
        sensitive_attr: Protected attribute (0 or 1, e.g., sex)
    """
    groups = np.unique(sensitive_attr)
    results = {}

    for g in groups:
        mask = sensitive_attr == g
        yt, yp = y_true[mask], y_pred[mask]
        tn, fp, fn, tp = confusion_matrix(yt, yp, labels=[0, 1]).ravel()

        n = len(yt)
        positive_rate = yp.mean()               # Demographic parity
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0  # True positive rate (recall)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # False positive rate
        ppv = tp / (tp + fp) if (tp + fp) > 0 else 0  # Precision

        results[g] = {
            "n": n,
            "positive_rate": positive_rate,   # For demographic parity
            "tpr": tpr,                        # For equalized odds
            "fpr": fpr,                        # For equalized odds
            "precision": ppv,                  # For predictive parity
        }

    print("\n=== Fairness Metrics ===")
    for g, m in results.items():
        print(f"\nGroup {g} (n={m['n']}):")
        print(f"  Positive rate: {m['positive_rate']:.3f}  (demographic parity)")
        print(f"  TPR:           {m['tpr']:.3f}  (equalized opportunity)")
        print(f"  FPR:           {m['fpr']:.3f}  (equalized odds)")
        print(f"  Precision:     {m['precision']:.3f}  (predictive parity)")

    # Compute disparities between groups
    if len(groups) == 2:
        g0, g1 = groups
        print(f"\n=== Disparities (Group {g1} vs. Group {g0}) ===")
        for metric in ["positive_rate", "tpr", "fpr", "precision"]:
            disp = results[g1][metric] - results[g0][metric]
            print(f"  {metric}: {disp:+.3f}")

    return results

# Simulated hiring algorithm data
np.random.seed(42)
n = 1000
sex = np.random.binomial(1, 0.5, n)             # 0=female, 1=male
# Simulate a biased algorithm: males are more likely to be hired
y_true = np.random.binomial(1, 0.3 + 0.1 * sex, n)
y_pred = np.random.binomial(1, 0.2 + 0.25 * sex, n)  # Model is biased

compute_fairness_metrics(y_true, y_pred, sex)
```

### SHAP for Model Explainability

SHAP (SHapley Additive exPlanations) computes how much each feature contributed to a specific prediction, grounded in game theory (Shapley values).

```python
import shap
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

cancer = load_breast_cancer()
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
y = cancer.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# SHAP explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
# shap_values[i, j] = the contribution of feature j to the prediction for example i

# Global feature importance: mean absolute SHAP value
mean_abs_shap = pd.Series(
    abs(shap_values).mean(axis=0),
    index=X.columns
).sort_values(ascending=False)

print("Top 5 features by mean |SHAP| value:")
print(mean_abs_shap.head())

# Local explanation for a single prediction
print(f"\nPrediction for sample 0: {model.predict(X_test.iloc[[0]])[0]}")
print("Feature contributions:")
for feat, val in sorted(zip(X.columns, shap_values[0]), key=lambda x: abs(x[1]), reverse=True)[:5]:
    print(f"  {feat}: {val:+.4f}")
```

### Differential Privacy (Conceptual)

Differential privacy (DP) provides a mathematical guarantee that the output of an algorithm does not reveal whether any individual was in the dataset. It adds calibrated noise to computations.

The formal guarantee: for any two datasets $D$ and $D'$ differing by one individual's record, and any output $S$:

$$P[\mathcal{M}(D) \in S] \leq e^{\epsilon} \cdot P[\mathcal{M}(D') \in S]$$

Lower $\epsilon$ = stronger privacy, higher noise, less utility.

```python
import numpy as np

def private_mean(data: np.ndarray, epsilon: float, sensitivity: float) -> float:
    """
    Compute a differentially private mean using the Laplace mechanism.

    Args:
        data: Array of values
        epsilon: Privacy budget (lower = more private)
        sensitivity: Max change in mean from one individual's contribution

    Returns:
        Differentially private estimate of the mean
    """
    true_mean = data.mean()
    # Laplace noise calibrated to sensitivity / epsilon
    noise = np.random.laplace(0, sensitivity / epsilon)
    return true_mean + noise

# Demonstrate: higher epsilon gives less noisy result
data = np.random.normal(100, 10, 1000)
true_mean = data.mean()
print(f"True mean: {true_mean:.2f}")

for eps in [0.01, 0.1, 1.0, 10.0]:
    estimates = [private_mean(data, eps, sensitivity=1.0) for _ in range(100)]
    print(f"  ε={eps:5.2f}: mean estimate = {np.mean(estimates):.2f} "
          f"± {np.std(estimates):.2f}")
# Higher epsilon → less noise → closer to true mean → weaker privacy
```

---

## Key Concepts

**Demographic Parity** — The positive prediction rate should be equal across groups. $P(\hat{Y}=1 | A=0) = P(\hat{Y}=1 | A=1)$.

**Equalized Odds** — Both TPR and FPR should be equal across groups. Stronger than demographic parity.

**Calibration** — Among all individuals the model assigns probability $p$, approximately $p$ fraction should actually have the positive outcome. This should hold equally across groups.

**Impossibility Theorems** — Chouldechova (2017) and Kleinberg et al. (2016) proved that several fairness criteria cannot be simultaneously satisfied when base rates differ across groups. Choosing a fairness criterion is a values question, not just a technical one.

**SHAP Values** — The average marginal contribution of each feature across all possible feature orderings. Provides both global feature importance and local explanations.

**Differential Privacy** — A mathematical framework for quantifying and bounding the privacy loss from publishing statistics about a dataset.

**Federated Learning** — A distributed training paradigm where the training data stays on users' devices. The model is trained locally and only gradients (not data) are sent to a central server.

---

## Examples

### Example 1: Bias Detection and Threshold Adjustment

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

# Simulated loan application data with biased features
np.random.seed(42)
n = 2000
sex = np.random.binomial(1, 0.5, n)  # 0=female, 1=male
credit_score = np.random.normal(650 + 30 * sex, 100, n)  # Higher for males (biased data)
y = (credit_score > 660).astype(int)  # True creditworthiness

# Model learns the biased credit score
X = np.column_stack([credit_score, sex])
X_train, X_test, y_train, y_test, sex_train, sex_test = train_test_split(
    X, y, sex, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]

# Default threshold: 0.5
y_pred_default = (proba >= 0.5).astype(int)

# Measure positive rates by sex
for s, name in [(0, "female"), (1, "male")]:
    mask = sex_test == s
    print(f"{name}: positive rate = {y_pred_default[mask].mean():.3f}")

# Post-processing: find group-specific thresholds for demographic parity
def find_fair_thresholds(proba, sex, target_positive_rate, n_steps=100):
    thresholds = {0: 0.5, 1: 0.5}
    for g in [0, 1]:
        mask = sex == g
        for t in np.linspace(0.1, 0.9, n_steps):
            preds = (proba[mask] >= t).mean()
            if abs(preds - target_positive_rate) < 0.01:
                thresholds[g] = t
                break
    return thresholds

target = y_pred_default.mean()  # Match the overall positive rate
thresholds = find_fair_thresholds(proba, sex_test, target)

y_pred_fair = np.zeros(len(y_test))
for g, t in thresholds.items():
    mask = sex_test == g
    y_pred_fair[mask] = (proba[mask] >= t).astype(int)

print("\nAfter threshold adjustment for demographic parity:")
for s, name in [(0, "female"), (1, "male")]:
    mask = sex_test == s
    print(f"{name}: positive rate = {y_pred_fair[mask].mean():.3f}")
```

---

## Common Pitfalls

### Pitfall 1: Removing the Protected Attribute Does Not Remove Bias

Removing sex or race from the features does not make the model fair if other features are proxies for the protected attribute (e.g., zip code correlates with race; job title correlates with sex).

### Pitfall 2: Optimizing Accuracy at the Expense of Fairness

Standard ML training maximizes accuracy, which can produce models that are accurate on average but consistently fail for minority groups. Always audit per-group performance, not just overall metrics.

### Pitfall 3: Choosing Fairness Metrics Without Understanding the Impossibility Results

Demographic parity, equalized odds, and calibration are often mutually incompatible when base rates differ across groups. You must explicitly choose which criterion matters for your use case — and document why.

---

## Cross-Links

- [[ai-ml/modules/05_model-evaluation]] — The evaluation metrics extended with fairness considerations in this module
- [[ai-ml/modules/03_supervised-learning]] — The classification models audited for fairness
- [[ai-ml/modules/10_llms-and-generative-ai]] — LLM-specific fairness issues (bias in training data, harmful outputs)
- [[ai-ml/modules/09_ml-engineering]] — Fairness monitoring in production ML systems

---

## Summary

- **Fairness is not a single concept** — demographic parity, equalized odds, and calibration are distinct mathematical criteria that cannot all be simultaneously satisfied when base rates differ.
- **Removing protected attributes does not remove bias.** Proxy features carry the same information. Fairness requires active measurement and mitigation, not just omission.
- **SHAP provides both global and local explanations.** It answers "what features drive the model overall?" (global) and "why did the model predict X for this specific person?" (local).
- **Differential privacy provides a mathematical privacy guarantee.** It quantifies the privacy-utility tradeoff — lower ε = stronger privacy = more noise = less accuracy.
- **Federated learning keeps training data on device.** Only model updates are shared, reducing privacy exposure for users.
- **Responsible AI requires both technical and governance decisions.** Which fairness criterion to use, what level of explainability is required, and what privacy budget is acceptable are ultimately policy questions — but they require technical literacy to make well.
