# Exercises: Module 02 — Mathematics for Machine Learning

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
All exercises require numpy — no external libraries beyond numpy and scipy.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Implement basic matrix operations in numpy

Without using any high-level sklearn functions, implement the following from scratch using numpy:

a) Create a 4×3 matrix `X` and a 3×2 weight matrix `W`. Compute `X @ W` and print its shape.
b) Compute the transpose of `X` and verify its shape.
c) Compute the dot product of two 4-dimensional vectors `a = [1, 2, 3, 4]` and `b = [5, 6, 7, 8]`.
d) Compute the L2 norm (Euclidean length) of vector `a` using numpy.

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Understand probability distributions

Using numpy and/or scipy:

a) Generate 10,000 samples from a standard normal distribution (mean=0, std=1). Print the sample mean and standard deviation. They should be close to 0 and 1.
b) Apply Bayes' theorem: a disease affects 3% of the population. A test has 90% sensitivity (true positive rate) and 8% false positive rate. What is the probability that a random person with a positive test actually has the disease?
c) Show that for a Bernoulli distribution with p=0.3, the mean is p and the variance is p*(1-p) by generating 100,000 samples and checking empirically.

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Implement gradient descent on a 1D function

Implement gradient descent to minimize $f(x) = x^4 - 3x^3 + 2$.

a) Compute the analytical derivative $f'(x)$ by hand. Write it in a comment.
b) Implement gradient descent starting from $x_0 = 4.0$ with learning rate 0.01 for 100 steps.
c) Print the final value of $x$ and $f(x)$.
d) What happens if you use learning rate 0.1? 0.5? Explain what you observe.

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Linear regression via the normal equation

The normal equation provides a closed-form solution for linear regression: $\hat{w} = (X^T X)^{-1} X^T y$.

a) Generate a synthetic dataset: $y = 2x_1 + 3x_2 - 1 + \epsilon$ where $\epsilon \sim \mathcal{N}(0, 0.5)$, with 100 samples.
b) Add a column of ones to `X` to handle the bias term (make it a design matrix).
c) Implement the normal equation in numpy to solve for the weights.
d) Compare your weights to the true weights [2, 3, -1]. Are they close?
e) Why might you prefer gradient descent over the normal equation for very large datasets?

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Understand covariance and correlation

a) Generate a 2D dataset where the two features are correlated: $x_2 = 0.8 x_1 + \epsilon$.
b) Compute the covariance matrix using numpy.
c) Compute eigenvalues and eigenvectors of the covariance matrix.
d) Explain: what does the largest eigenvector represent geometrically? Why is this useful for PCA?
e) Project the data onto the first principal component (largest eigenvector) and print the variance of the projected data. How does it compare to the original feature variances?

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Implement logistic regression from scratch

Logistic regression predicts $P(y=1|x) = \sigma(w \cdot x + b)$ where $\sigma(z) = 1 / (1 + e^{-z})$.
The loss is binary cross-entropy: $L = -[y \log \hat{p} + (1-y) \log (1 - \hat{p})]$.

a) Implement the sigmoid function.
b) Implement the binary cross-entropy loss.
c) Derive the gradient of the loss with respect to `w` and `b` (show your calculus, or at least write the gradient formula in a comment).
d) Implement gradient descent for logistic regression on the breast cancer dataset from sklearn.
e) Compare your accuracy to `sklearn.linear_model.LogisticRegression`.

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Implement gradient checking

Gradient checking verifies that an analytical gradient implementation is correct by comparing it to a numerical approximation.

a) Implement a 2-layer function: $f(w, x) = \text{ReLU}(w_1 x) \cdot w_2$ where ReLU$(z) = \max(0, z)$.
b) Compute the analytical gradient $\partial f / \partial w_1$ and $\partial f / \partial w_2$.
c) Compute the numerical gradient using central differences: $(f(w + \epsilon) - f(w - \epsilon)) / (2\epsilon)$ for each weight.
d) Report the relative error between analytical and numerical gradients. It should be below $10^{-5}$.
e) What does a large gradient checking error tell you about your implementation?

---

### Exercise 8

**Difficulty:** Hard
**Objective:** MLE for a Gaussian

Maximum Likelihood Estimation (MLE) finds parameter values that maximize the probability of the observed data.

a) Generate 200 samples from $\mathcal{N}(\mu=3.5, \sigma=1.2)$.
b) Derive the MLE formulas for $\mu$ and $\sigma^2$ from the log-likelihood (show the derivation in comments).
c) Compute the MLE estimates from your samples. How close are they to the true parameters?
d) Now implement gradient ascent on the log-likelihood to find MLE (instead of the closed form). Confirm you reach the same result.

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Implement PCA from scratch using eigendecomposition

Without using `sklearn.decomposition.PCA`:

a) Load the digits dataset (`sklearn.datasets.load_digits`) — 1797 samples, 64 features.
b) Center the data by subtracting the feature means.
c) Compute the covariance matrix: $\Sigma = \frac{1}{n-1} X^T X$.
d) Compute eigenvalues and eigenvectors of the covariance matrix using `np.linalg.eigh`.
e) Sort by eigenvalue (descending) to get principal components.
f) Project the data onto the first 2 principal components.
g) Compute the explained variance ratio for each component.
h) Compare your results to `sklearn.decomposition.PCA(n_components=2)` — the projections should match (up to sign flips).
i) What fraction of total variance do the first 2 components explain? First 10?
