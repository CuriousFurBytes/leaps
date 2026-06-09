# Exercises: Module 04 — Unsupervised Learning

## Instructions
All exercises use scikit-learn and numpy unless otherwise noted.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Apply k-means and choose k

Load the `make_blobs` dataset with 5 centers. Run k-means for k=2 through k=8. For each k, compute the silhouette score and inertia. Identify the correct k.

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Apply PCA for variance analysis

On the digits dataset (64 features), apply PCA. Print the cumulative explained variance ratio. How many components are needed to explain 90%, 95%, and 99% of variance?

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Compare clustering algorithms

On the moons dataset (`make_moons`), apply k-means and DBSCAN. Compare their cluster assignments visually (print cluster counts) and quantify with ARI (adjusted rand index) against ground truth.

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** PCA + supervised learning pipeline

On the digits dataset: train logistic regression on raw features, then train on PCA-reduced features (keep 95% variance). Compare test accuracy and training time. Does dimensionality reduction hurt accuracy?

---

### Exercise 5
**Difficulty:** Medium
**Objective:** Anomaly detection with DBSCAN

Generate a dataset with 200 normal points (Gaussian cluster) and 20 anomalies (uniform random in a wider range). Apply DBSCAN with appropriate parameters to identify the anomalies. How many anomalies does DBSCAN correctly identify?

---

### Exercise 6
**Difficulty:** Medium
**Objective:** Silhouette analysis

For the wine dataset (no labels visible to the algorithm), run k-means for k=2 through k=6. Plot (or print) per-cluster silhouette scores for each k. Which k gives the most balanced, high-silhouette clusters? How does this compare to the true k=3?

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Implement k-means from scratch

Implement k-means in numpy without sklearn. Your implementation must:
- Initialize centroids using k-means++ (not random)
- Iterate until convergence or max_iter
- Return final labels and final WCSS

Verify your results match `sklearn.cluster.KMeans` on `make_blobs`.

---

### Exercise 8
**Difficulty:** Hard
**Objective:** PCA for noise filtering and reconstruction

On the MNIST digits (or digits dataset), apply PCA, keep the top k components, and reconstruct the data. Compute reconstruction error (MSE) for k = 5, 10, 20, 50, 64. At what k does reconstruction become visually acceptable?

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Implement a linear autoencoder and compare to PCA

Build a simple autoencoder using PyTorch (2-layer encoder, 2-layer decoder) on the digits dataset with a bottleneck of 2 dimensions. Train with MSE reconstruction loss for 100 epochs. Compare:
- Reconstruction MSE vs. PCA with 2 components
- Visualization: scatter plot of latent space (color by digit class) vs. PCA 2D projection
- What does the autoencoder learn that PCA cannot?
