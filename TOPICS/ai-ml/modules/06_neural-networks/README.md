# Module 06: Neural Networks

[← Module 05: Model Evaluation](../05_model-evaluation/) | [Topic Home](../../README.md) | [Next → Module 07: Deep Learning](../07_deep-learning/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-14--18h-orange)

> The foundations of neural networks: the perceptron, multi-layer networks, backpropagation derived from scratch in numpy, activation functions, weight initialization, and why depth matters.

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

Neural networks are universal function approximators. Given enough layers and neurons, they can, in principle, approximate any continuous function. But this theoretical power comes with practical challenges: choosing architecture, initializing weights carefully, avoiding vanishing and exploding gradients, and understanding what the network has actually learned.

This module builds neural networks from scratch in numpy — no frameworks. This is the most important learning exercise in the curriculum: when you have implemented backpropagation by hand, you truly understand what PyTorch and TensorFlow are doing when you call `loss.backward()`. Every layer, every gradient, every weight update becomes concrete. After this module, switching to PyTorch will feel natural because the abstraction will be transparent.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/02_math-for-ml]] — Chain rule, gradients, matrix multiplication, gradient descent
- [[ai-ml/modules/03_supervised-learning]] — Supervised learning workflow; loss functions; evaluation

### Required Concepts

- **Calculus** — partial derivatives, the chain rule
- **Linear algebra** — matrix multiplication, transposition
- **Python classes** — object-oriented programming basics

---

## Objectives

By the end of this module, you will be able to:

1. Explain the perceptron and its limitations (XOR problem), and why multi-layer networks are necessary
2. Implement a forward pass through a multi-layer network using numpy
3. Derive and implement backpropagation from scratch using the chain rule
4. Implement and compare sigmoid, tanh, ReLU, and Leaky ReLU activations and explain the vanishing gradient problem
5. Implement Xavier/Glorot and He initialization and explain why random initialization of weights matters
6. Train a 2-layer network on a real classification dataset and achieve competitive accuracy

---

## Theory

### The Perceptron (1957)

Frank Rosenblatt's perceptron was the first trainable neural unit. It takes a weighted sum of inputs and applies a step function: $\hat{y} = \mathbf{1}[\mathbf{w} \cdot \mathbf{x} + b > 0]$. The perceptron learning rule updates weights when it makes a mistake.

The fatal limitation: a single perceptron can only classify linearly separable problems. It cannot learn XOR. Minsky and Papert proved this in 1969, contributing to the first AI winter.

```python
import numpy as np

class Perceptron:
    """The original perceptron — historically important but limited to linear problems."""

    def __init__(self, n_features, learning_rate=0.01, n_iter=1000):
        self.w = np.zeros(n_features)
        self.b = 0.0
        self.lr = learning_rate
        self.n_iter = n_iter

    def predict(self, X):
        """Step activation: output 1 if weighted sum > 0, else 0."""
        return (X @ self.w + self.b > 0).astype(int)

    def fit(self, X, y):
        """Perceptron learning rule: update weights on misclassification."""
        for _ in range(self.n_iter):
            for xi, yi in zip(X, y):
                update = self.lr * (yi - (xi @ self.w + self.b > 0))
                self.w += update * xi
                self.b += update

# Demonstrate: perceptron CAN learn AND
X_and = np.array([[0,0],[0,1],[1,0],[1,1]])
y_and = np.array([0, 0, 0, 1])
p = Perceptron(n_features=2)
p.fit(X_and, y_and)
print("AND predictions:", p.predict(X_and))  # Should be [0, 0, 0, 1]

# Demonstrate: perceptron CANNOT learn XOR
X_xor = np.array([[0,0],[0,1],[1,0],[1,1]])
y_xor = np.array([0, 1, 1, 0])
p2 = Perceptron(n_features=2, n_iter=5000)
p2.fit(X_xor, y_xor)
print("XOR predictions:", p2.predict(X_xor))  # Will NOT converge to [0, 1, 1, 0]
```

### Multi-Layer Networks and Backpropagation

Adding hidden layers with non-linear activation functions allows networks to learn non-linear decision boundaries. Backpropagation, rediscovered by Rumelhart, Hinton, and Williams in 1986, made training these networks feasible by computing gradients efficiently using the chain rule.

The forward pass: compute activations layer by layer.
The backward pass: compute gradients layer by layer, from output to input.

```python
import numpy as np

class TwoLayerNetwork:
    """
    A 2-layer neural network (1 hidden layer) implemented from scratch.
    Architecture: input -> hidden (ReLU) -> output (sigmoid)
    Loss: binary cross-entropy
    """

    def __init__(self, n_input, n_hidden, n_output, lr=0.01):
        # He initialization for ReLU layers
        self.W1 = np.random.randn(n_input, n_hidden) * np.sqrt(2.0 / n_input)
        self.b1 = np.zeros(n_hidden)
        # Xavier initialization for sigmoid output layer
        self.W2 = np.random.randn(n_hidden, n_output) * np.sqrt(1.0 / n_hidden)
        self.b2 = np.zeros(n_output)
        self.lr = lr

    def relu(self, z):
        return np.maximum(0, z)

    def relu_grad(self, z):
        return (z > 0).astype(float)

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))  # Clip for stability

    def forward(self, X):
        """Forward pass: compute predictions and cache intermediates for backprop."""
        self.X = X
        self.z1 = X @ self.W1 + self.b1       # Pre-activation, layer 1
        self.a1 = self.relu(self.z1)            # Activation, layer 1
        self.z2 = self.a1 @ self.W2 + self.b2  # Pre-activation, layer 2
        self.a2 = self.sigmoid(self.z2)         # Output (probability)
        return self.a2

    def backward(self, y):
        """
        Backward pass: compute gradients using chain rule.
        Each gradient flows from output back to input.
        """
        n = len(y)
        y = y.reshape(-1, 1)

        # Output layer gradients
        # dL/dz2 = a2 - y  (gradient of binary cross-entropy + sigmoid combined)
        dz2 = self.a2 - y                              # Shape: (n, n_output)
        dW2 = self.a1.T @ dz2 / n                     # Shape: (n_hidden, n_output)
        db2 = dz2.mean(axis=0)                         # Shape: (n_output,)

        # Hidden layer gradients (chain rule: multiply by ReLU gradient)
        da1 = dz2 @ self.W2.T                          # Shape: (n, n_hidden)
        dz1 = da1 * self.relu_grad(self.z1)            # Shape: (n, n_hidden)
        dW1 = self.X.T @ dz1 / n                       # Shape: (n_input, n_hidden)
        db1 = dz1.mean(axis=0)                         # Shape: (n_hidden,)

        # Gradient descent update
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def loss(self, y_pred, y_true):
        """Binary cross-entropy loss."""
        y_true = y_true.reshape(-1, 1)
        eps = 1e-8  # Prevent log(0)
        return -np.mean(y_true * np.log(y_pred + eps) +
                        (1 - y_true) * np.log(1 - y_pred + eps))


# Train on the moons dataset
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

net = TwoLayerNetwork(n_input=2, n_hidden=16, n_output=1, lr=0.05)

# Training loop
for epoch in range(500):
    y_pred = net.forward(X_train)
    net.backward(y_train)
    if epoch % 100 == 0:
        l = net.loss(y_pred, y_train)
        # Compute accuracy
        acc = ((y_pred.ravel() > 0.5) == y_train).mean()
        print(f"Epoch {epoch:4d}: loss={l:.4f}, train_acc={acc:.3f}")

# Test accuracy
y_test_pred = net.forward(X_test)
test_acc = ((y_test_pred.ravel() > 0.5) == y_test).mean()
print(f"\nTest accuracy: {test_acc:.3f}")
```

### Activation Functions and the Vanishing Gradient Problem

The choice of activation function is critical. Sigmoid and tanh saturate at extreme values — their gradients approach zero. When gradients flow backward through many layers multiplied by near-zero values, they vanish: early layers receive almost no learning signal. This was the main barrier to training deep networks before ReLU.

ReLU (Rectified Linear Unit) — $\text{ReLU}(z) = \max(0, z)$ — has a constant gradient of 1 for positive inputs, breaking the vanishing gradient problem and enabling deep networks to train.

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_grad(z):
    s = sigmoid(z)
    return s * (1 - s)  # Maximum value is 0.25 at z=0; approaches 0 for large |z|

def relu(z):
    return np.maximum(0, z)

def relu_grad(z):
    return (z > 0).astype(float)  # Either 0 or 1 — no saturation

# Demonstrate vanishing gradients through many layers
z = np.array([5.0])  # A value where sigmoid saturates
print("Sigmoid gradient at z=5:", sigmoid_grad(z))     # ~0.007 — very small
print("Sigmoid gradient at z=0:", sigmoid_grad(np.array([0.0])))  # 0.25 — maximum

# After 10 layers with sigmoid:
gradient = 1.0
for _ in range(10):
    gradient *= sigmoid_grad(z)[0]
print(f"\nGradient after 10 sigmoid layers at z=5: {gradient:.2e}")  # Vanishes to ~0

# After 10 layers with ReLU:
gradient_relu = 1.0
for _ in range(10):
    gradient_relu *= relu_grad(z)[0]
print(f"Gradient after 10 ReLU layers at z=5: {gradient_relu:.2e}")  # Stays at 1.0
```

### Weight Initialization

Random initialization breaks symmetry (otherwise all neurons would learn the same thing). The scale of initialization matters: too small leads to vanishing gradients; too large leads to exploding gradients.

**Xavier/Glorot initialization** (for sigmoid/tanh): $W \sim \mathcal{U}(-\sqrt{6/(n_{in}+n_{out})}, \sqrt{6/(n_{in}+n_{out})})$

**He initialization** (for ReLU): $W \sim \mathcal{N}(0, \sqrt{2/n_{in}})$

```python
import numpy as np

n_in, n_out = 512, 256

# Zero initialization — WRONG: all neurons learn identical features
W_zero = np.zeros((n_in, n_out))  # Never do this

# Small random — may lead to vanishing gradients for deep networks
W_small = np.random.randn(n_in, n_out) * 0.01

# Xavier initialization — appropriate for sigmoid/tanh
limit = np.sqrt(6.0 / (n_in + n_out))
W_xavier = np.random.uniform(-limit, limit, (n_in, n_out))

# He initialization — appropriate for ReLU
W_he = np.random.randn(n_in, n_out) * np.sqrt(2.0 / n_in)

print(f"Zero init     — std: {W_zero.std():.4f}")
print(f"Small random  — std: {W_small.std():.4f}")
print(f"Xavier        — std: {W_xavier.std():.4f}  (target: {np.sqrt(2/(n_in+n_out)):.4f})")
print(f"He            — std: {W_he.std():.4f}  (target: {np.sqrt(2/n_in):.4f})")
```

---

## Key Concepts

**Perceptron** — A single neuron that computes a weighted sum and applies a step function. Can only learn linearly separable problems.

**Activation Function** — The non-linear function applied to the pre-activation (weighted sum + bias). Without non-linearity, any depth network reduces to a single linear layer.

**Forward Pass** — Computing the network's output from input to output, layer by layer.

**Backward Pass (Backpropagation)** — Computing gradients of the loss with respect to all weights, from output to input, using the chain rule.

**Vanishing Gradient** — The problem where gradients become exponentially small as they propagate backward through many layers, preventing early layers from learning. Caused by saturating activations (sigmoid, tanh) in deep networks.

**Xavier/He Initialization** — Weight initialization strategies that maintain appropriate gradient magnitudes across layers of different widths.

---

## Examples

### Example 1: Verifying Backpropagation with Gradient Checking

```python
import numpy as np

def numerical_gradient(f, x, epsilon=1e-5):
    """Compute numerical gradient of f at x using central differences."""
    grad = np.zeros_like(x, dtype=float)
    for i in range(x.size):
        x_plus = x.copy(); x_plus.flat[i] += epsilon
        x_minus = x.copy(); x_minus.flat[i] -= epsilon
        grad.flat[i] = (f(x_plus) - f(x_minus)) / (2 * epsilon)
    return grad

# Simple 1-layer network: loss = MSE(sigmoid(X @ w + b), y)
X = np.random.randn(5, 3)
y = np.array([0, 1, 0, 1, 1], dtype=float)
w = np.random.randn(3)
b = np.array([0.1])

def loss_fn(w):
    z = X @ w + b
    pred = 1 / (1 + np.exp(-z))
    return -np.mean(y * np.log(pred + 1e-8) + (1 - y) * np.log(1 - pred + 1e-8))

# Analytical gradient
z = X @ w + b
pred = 1 / (1 + np.exp(-z))
d_loss = (pred - y) / len(y)
analytical_grad_w = X.T @ d_loss

# Numerical gradient
numerical_grad_w = numerical_gradient(loss_fn, w.copy())

rel_error = np.abs(analytical_grad_w - numerical_grad_w) / (np.abs(analytical_grad_w) + 1e-8)
print(f"Max relative error: {rel_error.max():.2e}")  # Should be < 1e-5
```

---

## Common Pitfalls

### Pitfall 1: Zero Initialization (Symmetry Breaking Failure)

If all weights are zero, all neurons in a layer compute the same output and receive the same gradient. The network cannot learn different features. Always use random initialization.

### Pitfall 2: Not Clipping Gradients with Sigmoid Outputs

Computing `log(0)` or `log(1)` causes `-inf` or `nan`. Always add a small epsilon when computing log loss.

```python
# WRONG: can produce nan
loss = -np.mean(y * np.log(y_pred) + (1-y) * np.log(1 - y_pred))

# CORRECT: clip to prevent numerical issues
eps = 1e-8
loss = -np.mean(y * np.log(y_pred + eps) + (1-y) * np.log(1 - y_pred + eps))
```

### Pitfall 3: Forgetting to Divide Gradients by Batch Size

When computing gradients over a batch, the loss is the mean. Forgetting to divide by n makes the gradient scale with batch size — the effective learning rate changes when you change batch size.

---

## Cross-Links

- [[ai-ml/modules/02_math-for-ml]] — Chain rule and gradient descent that backpropagation is built on
- [[ai-ml/modules/07_deep-learning]] — This module's foundations applied to CNNs, RNNs, and modern architectures
- [[ai-ml/modules/08_nlp-and-transformers]] — Transformers are large, specialized neural networks built on the same foundations
- [[shared/glossary#backpropagation]] — Glossary definition and context

---

## Summary

- **Neural networks are compositions of linear transformations and non-linear activation functions.** Without activations, any deep network collapses to a single linear layer.
- **The perceptron cannot learn XOR.** Multi-layer networks with non-linear activations can.
- **Backpropagation is the chain rule applied recursively.** It is not magic — it is calculus, applied systematically from output to input.
- **Vanishing gradients prevented training deep networks until ReLU.** ReLU's constant gradient for positive inputs allows deep networks to train.
- **Initialization matters.** Zero initialization breaks symmetry; too-small initialization causes vanishing gradients; He initialization is the standard for ReLU networks.
- **Implementing backpropagation from scratch is the single most educational exercise in ML.** Do not skip it in favor of "just using PyTorch."
