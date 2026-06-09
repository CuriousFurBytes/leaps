# Test: Module 02 — Mathematics for Machine Learning

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 × 1 pt + Medium: 5 × 2 pts + Hard: 4 × 3 pts + Expert: 2 × 5 pts)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is the shape of the result when you multiply a matrix of shape (5, 3) by a matrix of shape (3, 2)?

> Answer:

**Q2.** What does the gradient of a function tell you, geometrically?

> Answer:

**Q3.** State Bayes' theorem in symbols and explain what each term represents.

> Answer:

**Q4.** What is the dot product of vectors `[1, 2, 3]` and `[4, 5, 6]`? Compute it by hand.

> Answer:

**Q5.** In gradient descent, why do we move in the **negative** direction of the gradient?

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain what eigenvalues and eigenvectors are. Why are they important for PCA?

> Answer:

**Q7.** A neural network uses sigmoid activations everywhere. Explain the "vanishing gradient problem" in terms of the chain rule and the sigmoid function's derivative.

> Answer:

**Q8.** You are computing the joint probability of 1000 independent events, each with probability 0.9. Why does computing this directly (multiplying 0.9 × 0.9 × ... 1000 times) fail numerically? How do you fix it?

> Answer:

**Q9.** The normal equation for linear regression is $\hat{w} = (X^T X)^{-1} X^T y$. What goes wrong if $X^T X$ is not invertible? When does this happen?

> Answer:

**Q10.** Explain the difference between population variance ($\sigma^2 = \frac{1}{n} \sum (x_i - \mu)^2$) and sample variance ($s^2 = \frac{1}{n-1} \sum (x_i - \bar{x})^2$). Why does ML code typically use the sample variance formula with `ddof=1`?

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Implement gradient descent from scratch in numpy to minimize $f(w) = (w_1 - 2)^2 + (w_2 + 3)^2$. Start at $w = [0, 0]$, use learning rate 0.1, run for 50 steps, and print the final $w$. The true minimum is at $w = [2, -3]$.

> Answer:

```python
# Write your code here
```

**Q12.** Implement the logistic function (sigmoid) and its derivative. Then verify: the derivative of $\sigma(z)$ is $\sigma(z)(1 - \sigma(z))$. Show this numerically using central differences at $z = 1.5$.

> Answer:

```python
# Write your code here
```

**Q13.** Compute the covariance matrix of this dataset by hand (show your work) and verify with numpy:

```
X = [[1, 2],
     [3, 4],
     [5, 6],
     [7, 8]]
```

Is this covariance matrix positive semidefinite? How can you tell without computing eigenvalues?

> Answer:

**Q14.** Debug this gradient descent implementation — it is not converging. Identify all issues and write a corrected version.

```python
import numpy as np
def f(x): return x**2 + 4*x + 4
def grad_f(x): return 2*x + 4

x = 10.0
lr = 2.0  # Learning rate
for i in range(100):
    x = x + lr * grad_f(x)  # update step
print(f"Final x: {x:.4f}")  # Should converge to x=-2
```

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Derive the gradient of the binary cross-entropy loss with respect to the logit $z$ (before the sigmoid), for a single training example $(x, y)$. Show each step using the chain rule. Then explain why the gradient has a particularly clean form and what this means for numerical stability.

> Answer:

**Q16.** Maximum likelihood estimation and least squares regression are equivalent under a Gaussian noise assumption. Prove this: show that maximizing the log-likelihood of a linear Gaussian model $y = w \cdot x + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is equivalent to minimizing the mean squared error loss. What does this tell you about the assumptions linear regression is making?

> Answer:

---

## Bonus Question (5 pts)

**Bonus 1.** The learning rate in gradient descent is a hyperparameter that must be set carefully. Derive the condition on the learning rate under which gradient descent is guaranteed to converge for a function with Lipschitz-continuous gradient (L-smooth function). What is the maximum stable learning rate in terms of L, the Lipschitz constant? Demonstrate with a concrete example. (+5 pts)

> Answer:
