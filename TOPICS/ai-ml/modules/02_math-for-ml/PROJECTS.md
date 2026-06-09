# Projects: Module 02 — Mathematics for Machine Learning

---

## Project 1: Linear Regression Engine from Scratch (Intermediate)

**Time estimate:** 5–8 hours

Implement a complete linear regression class in numpy — no sklearn. Your class must support:
- Fitting via both the normal equation (for small datasets) and gradient descent (for large)
- Prediction
- R² score computation
- A `plot_loss_curve()` method that shows gradient descent convergence

Test on the California housing dataset from sklearn and compare your results to `sklearn.linear_model.LinearRegression`.

---

## Project 2: Probability Visual Explorer (Beginner)

**Time estimate:** 3–5 hours

Create a Python script that visualizes:
- The effect of changing mean and variance on a Gaussian distribution
- Bayes' theorem applied to a medical screening scenario (interactive: vary sensitivity, specificity, and prevalence)
- The Central Limit Theorem: show that sample means converge to Gaussian regardless of the source distribution

Use matplotlib for all visualizations. Save figures as PNG files (no GUI required).

---

## Project 3: Gradient Descent Optimizer Comparison (Advanced)

**Time estimate:** 8–12 hours

Implement the following gradient descent variants from scratch in numpy, then compare them on a non-convex optimization problem:
- Vanilla gradient descent (fixed learning rate)
- Momentum
- RMSProp
- Adam

For each optimizer: show the convergence curve, the final value, and the number of steps to reach within 1% of the optimum. Write a 1-page analysis of when each optimizer is appropriate.
