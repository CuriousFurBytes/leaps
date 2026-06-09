# Module 02: Mathematics for Machine Learning

[← Module 01: Introduction](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03: Supervised Learning](../03_supervised-learning/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> The mathematical foundations that make machine learning work: linear algebra for data representation, probability and statistics for uncertainty, and calculus for optimization.

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

Machine learning algorithms are, at their core, mathematical procedures. A linear regression model is a dot product. A neural network is a composition of matrix multiplications and non-linear functions. Gradient descent is an application of multivariable calculus. A naive Bayes classifier is a direct application of Bayes' theorem. Without understanding the mathematics, you can use these tools but cannot diagnose why they fail, modify them for new problems, or understand the research literature.

This module develops the mathematical foundation specifically as it applies to ML — not as abstract theory, but as the tools you will use in every subsequent module. The goal is applied mathematical literacy: you should be able to look at an equation in a paper and understand what it is computing, translate that equation into code, and reason about its behavior.

The three pillars are: **linear algebra** (how data and model parameters are represented and transformed), **probability and statistics** (how uncertainty, distributions, and inference work), and **calculus** (how models are optimized by following gradients). Each is treated in its ML-relevant context, not in full generality.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/01_introduction]] — the ML workflow and taxonomy; you need to know what a model, feature, and label are

### Required Concepts

- **Python and numpy** — array creation, broadcasting, matrix operations
- **High school algebra** — variables, equations, functions, graphs
- **Basic statistics** — you have heard of mean, variance, and probability (even if rusty)

> [!TIP]
> If any of these prerequisites feel shaky, spend 15–30 minutes reviewing them before continuing.
> The math in this module is the hardest in the curriculum — take your time.

---

## Objectives

By the end of this module, you will be able to:

1. Represent datasets as matrices and explain what the rows, columns, and matrix operations mean geometrically
2. Compute dot products, matrix multiplications, and inverses — and explain what each computes in the context of ML
3. Compute eigenvalues/eigenvectors and explain their role in PCA and covariance analysis
4. Apply Bayes' theorem to derive posterior probabilities and explain how it underlies Naive Bayes classifiers
5. Compute gradients of multivariate functions using the chain rule and explain why this is the foundation of backpropagation
6. Implement gradient descent from scratch in numpy on a simple optimization problem

---

## Theory

> [!NOTE]
> This module stub will be fully expanded in the next content generation pass.
> Core sections to be written: Vectors and Matrices, Matrix Operations (dot product, multiplication, inverse, transpose), Eigenvalues and Eigenvectors, Probability Basics (conditional probability, Bayes' theorem), Probability Distributions (Gaussian, Bernoulli, categorical), Maximum Likelihood Estimation, Derivatives and Partial Derivatives, Gradients and the Jacobian, Chain Rule and why it enables backpropagation, Gradient Descent from scratch.

### Linear Algebra for ML

Datasets are matrices. A dataset with $n$ examples and $d$ features is an $n \times d$ matrix $X$, where each row is one example and each column is one feature. This representation is why numpy's 2D arrays are the default data structure in scikit-learn.

```python
import numpy as np

# A simple 4-sample, 3-feature dataset
X = np.array([
    [1.2, 0.5, 3.1],   # Sample 1: 3 features
    [2.4, 1.1, 0.9],   # Sample 2
    [0.7, 2.3, 1.5],   # Sample 3
    [3.1, 0.8, 2.2],   # Sample 4
])
# Shape: (4, 3) — 4 rows (samples), 3 columns (features)
print(f"Dataset shape: {X.shape}")          # (4, 3)
print(f"Number of samples: {X.shape[0]}")   # 4
print(f"Number of features: {X.shape[1]}")  # 3

# Linear regression prediction: X @ w + b
# w is a weight vector of shape (3,), b is a scalar bias
w = np.array([0.5, -1.2, 0.3])  # Learned weights
b = 0.1                          # Learned bias
predictions = X @ w + b          # Matrix-vector multiplication: shape (4,)
print(f"Predictions: {predictions.round(2)}")
# Each prediction is a weighted sum of the features for that sample
```

### Probability and Statistics for ML

Every ML model makes assumptions about the data distribution. Understanding probability lets you read these assumptions critically and choose appropriate models.

```python
import numpy as np
from scipy import stats

# The Gaussian (Normal) distribution appears everywhere in ML
# - Assumed by linear regression (Gaussian noise model)
# - Used to initialize neural network weights
# - Central Limit Theorem: means of large samples are approximately Gaussian

mu, sigma = 0, 1  # Mean and standard deviation
samples = np.random.normal(mu, sigma, size=1000)

print(f"Sample mean: {samples.mean():.3f}")  # Close to 0
print(f"Sample std:  {samples.std():.3f}")   # Close to 1

# Bayes' theorem: P(H|E) = P(E|H) * P(H) / P(E)
# P(H|E): posterior — probability of hypothesis given evidence
# P(E|H): likelihood — probability of evidence given hypothesis
# P(H): prior — our belief before seeing evidence
# This is the foundation of Bayesian ML and Naive Bayes classifiers

# Example: medical test
p_disease = 0.01        # Prior: 1% of population has the disease
p_pos_given_disease = 0.95    # Sensitivity: 95% true positive rate
p_pos_given_no_disease = 0.05  # False positive rate: 5%

p_positive = (p_pos_given_disease * p_disease +
              p_pos_given_no_disease * (1 - p_disease))

p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive
print(f"\nP(disease | positive test) = {p_disease_given_pos:.3f}")
# This counterintuitive result (~16%) is Bayes' theorem in action
```

### Calculus for Optimization

Gradient descent, the core optimization algorithm in ML, is pure applied calculus. The gradient tells us which direction to move model parameters to reduce the loss.

```python
import numpy as np

# Gradient descent on a simple 1D quadratic: f(x) = (x - 3)^2
# Minimum is at x=3. Gradient: f'(x) = 2(x - 3)

def f(x):
    return (x - 3) ** 2

def grad_f(x):
    return 2 * (x - 3)   # Analytical derivative

# Gradient descent: x_new = x - learning_rate * gradient
x = 10.0          # Start far from the minimum
learning_rate = 0.1
history = [x]

for step in range(20):
    gradient = grad_f(x)
    x = x - learning_rate * gradient  # Move in the negative gradient direction
    history.append(x)
    if step < 5 or step == 19:
        print(f"Step {step+1:2d}: x={x:.4f}, f(x)={f(x):.4f}, grad={gradient:.4f}")

print(f"\nFinal x: {x:.4f} (true minimum: 3.0)")
# The algorithm converges toward x=3 by always moving downhill on the loss surface
```

---

## Key Concepts

**Vector** — A 1D array of numbers representing a point or direction in space. In ML, a single training example is often represented as a vector of feature values.

**Matrix** — A 2D array of numbers. The entire dataset is a matrix; model weights form matrices in neural networks.

**Dot Product** — The sum of element-wise products of two vectors: $\mathbf{a} \cdot \mathbf{b} = \sum_i a_i b_i$. Produces a scalar. In linear models, predictions are dot products of the weight vector and the feature vector.

**Eigenvalue/Eigenvector** — For a matrix $A$, a vector $v$ and scalar $\lambda$ such that $Av = \lambda v$. The eigenvectors of the covariance matrix define the principal components (PCA directions).

**Gradient** — The vector of partial derivatives of a function with respect to all its inputs. Points in the direction of steepest increase. Gradient descent moves in the negative gradient direction.

**Chain Rule** — The calculus rule for differentiating composite functions: $\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)$. Backpropagation is the chain rule applied repeatedly through the layers of a neural network.

---

## Examples

### Example 1: Matrix Multiplication as Batch Prediction

```python
import numpy as np

# A dataset of 5 examples with 3 features
X = np.random.randn(5, 3)   # Shape: (5, 3)

# A weight matrix that maps 3 features to 2 outputs (e.g., 2 classes)
W = np.random.randn(3, 2)   # Shape: (3, 2)
b = np.array([0.1, -0.2])   # Bias vector: shape (2,)

# Single matrix multiply produces predictions for ALL 5 examples simultaneously
# This is why vectorized computation (numpy, PyTorch) is critical for performance
logits = X @ W + b           # Shape: (5, 2) — one score per class per example
print(f"Input shape: {X.shape}")
print(f"Weight shape: {W.shape}")
print(f"Output shape: {logits.shape}")
```

### Example 2: Numerical Gradient Checking

```python
import numpy as np

# Numerical gradient (finite differences) for verifying analytical gradients
# Used in debugging neural networks: "gradient checking"

def f(x):
    """Example function: f(x) = x^3 - 2x^2 + x + 1"""
    return x**3 - 2*x**2 + x + 1

def analytical_grad(x):
    """Analytical derivative: f'(x) = 3x^2 - 4x + 1"""
    return 3*x**2 - 4*x + 1

def numerical_grad(f, x, epsilon=1e-5):
    """Numerical gradient via central differences"""
    return (f(x + epsilon) - f(x - epsilon)) / (2 * epsilon)

x = 2.0
ag = analytical_grad(x)
ng = numerical_grad(f, x)
print(f"Analytical gradient at x={x}: {ag:.6f}")
print(f"Numerical gradient at x={x}:  {ng:.6f}")
print(f"Relative error: {abs(ag - ng) / abs(ag):.2e}")
# Should be very small (< 1e-5) — confirms the analytical gradient is correct
```

---

## Common Pitfalls

### Pitfall 1: Confusing Row Vectors and Column Vectors

```python
# WRONG: treating a 1D array as a row vector when you need a column vector
import numpy as np
w = np.array([1, 2, 3])     # Shape: (3,) — not (3, 1) or (1, 3)
X = np.random.randn(5, 3)   # Shape: (5, 3)

# This works but the intent is ambiguous:
result = X @ w               # Shape: (5,) — works by broadcasting

# RIGHT: be explicit about the shape
w_col = w.reshape(-1, 1)    # Shape: (3, 1) — explicit column vector
result_explicit = (X @ w_col).ravel()  # Shape: (5,) — same result, clearer intent
```

### Pitfall 2: Misinterpreting Correlation as Causation in Feature Correlations

A high correlation between two features does not mean one causes the other. In ML, correlated features cause issues with collinearity in linear models. Always examine feature correlations during EDA and consider removing or combining highly correlated features.

### Pitfall 3: Numerical Instability in Probability Computations

```python
# WRONG: computing log-likelihood directly can underflow to 0
import numpy as np
probs = np.array([0.1, 0.2, 0.05, 0.3, 0.15])  # Probabilities per example
joint_prob = np.prod(probs)  # = very tiny number — can underflow to 0.0
print(f"Direct product: {joint_prob}")

# CORRECT: work in log space
log_prob = np.sum(np.log(probs))  # Log-sum is numerically stable
print(f"Log probability: {log_prob:.4f}")
print(f"Equivalent probability: {np.exp(log_prob):.6f}")
```

---

## Cross-Links

- [[ai-ml/modules/01_introduction]] — The ML workflow this module provides mathematical grounding for
- [[ai-ml/modules/06_neural-networks]] — Backpropagation is the chain rule applied to neural networks; everything in this module directly enables that
- [[ai-ml/modules/04_unsupervised-learning]] — PCA uses eigendecomposition of the covariance matrix (linear algebra from this module)
- [[shared/glossary#gradient-descent]] — The gradient descent algorithm introduced here

---

## Summary

- **Linear algebra provides the language for data and model parameters.** Datasets are matrices (n samples × d features). Predictions are matrix multiplications. Model parameters are matrices and vectors.
- **The dot product is the fundamental operation in ML.** Linear regression, logistic regression, and neural network layers all reduce to dot products.
- **Eigenvalues and eigenvectors describe the directions of greatest variance in data.** This directly underpins PCA and covariance analysis.
- **Probability is how ML handles uncertainty.** Models output probabilities; loss functions are often negative log-likelihoods; Bayes' theorem connects prior beliefs to posterior estimates.
- **Gradients tell you which direction to move parameters to reduce loss.** Gradient descent iteratively follows the negative gradient.
- **Backpropagation is the chain rule.** The same calculus rule for differentiating composite functions that you learned in high school is what enables training deep neural networks.
