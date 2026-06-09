# Module 04: Unsupervised Learning

[← Module 03: Supervised Learning](../03_supervised-learning/) | [Topic Home](../../README.md) | [Next → Module 05: Model Evaluation](../05_model-evaluation/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> Discovering structure in unlabeled data: k-means and DBSCAN for clustering, PCA and t-SNE for dimensionality reduction, and autoencoders for learned representations.

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

Unsupervised learning solves problems where there is no predefined correct answer — only data. The goal is to find structure: natural groupings (clustering), compact representations (dimensionality reduction), or the underlying data distribution. These techniques are used for customer segmentation, anomaly detection, data exploration before modeling, feature compression for neural networks, and visualization of high-dimensional data.

This module covers the two major categories: **clustering** (assigning data points to groups) and **dimensionality reduction** (representing data in fewer dimensions while preserving important structure). For each, we cover the theory, the algorithm, the hyperparameters, and most importantly — how to evaluate an unsupervised model without labels.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/01_introduction]] — ML workflow; what features and examples are
- [[ai-ml/modules/02_math-for-ml]] — Eigendecomposition (PCA), distance metrics, covariance matrices

### Required Concepts

- **numpy and pandas** — array operations, DataFrame manipulation
- **Distance metrics** — Euclidean distance, and why different metrics suit different data types

---

## Objectives

By the end of this module, you will be able to:

1. Apply k-means clustering to a dataset, choose k using the elbow method and silhouette score, and interpret the resulting clusters
2. Apply DBSCAN to detect clusters of arbitrary shape and identify outliers
3. Implement PCA for dimensionality reduction and explain the variance explained by each component
4. Use t-SNE for 2D visualization of high-dimensional data and explain its limitations
5. Implement a simple autoencoder in PyTorch for non-linear dimensionality reduction
6. Evaluate clustering quality using intrinsic metrics (silhouette, Davies-Bouldin) and extrinsic metrics (ARI, NMI) when labels are available

---

## Theory

### k-Means Clustering

k-means partitions $n$ data points into $k$ clusters by iteratively:
1. Assigning each point to its nearest centroid (using Euclidean distance)
2. Recomputing each centroid as the mean of its assigned points

This iterates until convergence (assignments stop changing). The algorithm minimizes within-cluster sum of squares (WCSS): $\sum_{k} \sum_{x \in C_k} \|x - \mu_k\|^2$.

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

# Generate synthetic clustered data
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)

# Elbow method: plot WCSS vs. k to find the "elbow"
wcss = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    wcss.append(km.inertia_)  # inertia_ = WCSS

# Print WCSS (plot in practice)
print("k  | WCSS       | Silhouette")
print("-" * 35)
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    sil = silhouette_score(X, labels)
    print(f"{k}  | {km.inertia_:10.1f} | {sil:.3f}")
# The "elbow" in WCSS and the peak in silhouette both point to k=4
```

### DBSCAN

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are close together (high-density regions) and marks low-density points as outliers. Unlike k-means, it:
- Does not require specifying k upfront
- Can find arbitrarily-shaped clusters
- Explicitly identifies outliers (noise points)

Two parameters: `eps` (neighborhood radius) and `min_samples` (minimum points for a core point).

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler

# Moons dataset — k-means fails here (non-convex shapes)
X, y_true = make_moons(n_samples=300, noise=0.1, random_state=42)
X = StandardScaler().fit_transform(X)

# k-means fails on non-convex clusters
from sklearn.cluster import KMeans
km_labels = KMeans(n_clusters=2, random_state=42).fit_predict(X)
print("k-means clusters:", set(km_labels))  # Two overlapping blobs

# DBSCAN handles arbitrary shapes
db = DBSCAN(eps=0.3, min_samples=5)
db_labels = db.fit_predict(X)
n_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
n_noise = sum(db_labels == -1)
print(f"DBSCAN clusters: {n_clusters}, noise points: {n_noise}")
# Correctly identifies 2 moon-shaped clusters with few noise points
```

### PCA — Principal Component Analysis

PCA finds the directions of maximum variance in the data (principal components) and projects data onto those directions. The first principal component explains the most variance; the second is orthogonal to the first and explains the next most, etc.

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
import numpy as np

digits = load_digits()
X = StandardScaler().fit_transform(digits.data)  # Standardize first

# Full PCA — keep all components
pca_full = PCA().fit(X)

# Explained variance ratio
cumulative_var = np.cumsum(pca_full.explained_variance_ratio_)

# Find how many components explain 95% of variance
n_components_95 = np.argmax(cumulative_var >= 0.95) + 1
print(f"Components to explain 95% variance: {n_components_95} of {X.shape[1]}")

# Reduce to 2D for visualization
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X)
print(f"Variance explained by 2 components: {pca_2d.explained_variance_ratio_.sum():.1%}")
print(f"Original shape: {X.shape}, Reduced shape: {X_2d.shape}")
```

### t-SNE

t-SNE (t-distributed Stochastic Neighbor Embedding) is a non-linear dimensionality reduction technique designed specifically for visualization. It preserves local structure (nearby points in high dimensions stay nearby in 2D) but sacrifices global structure.

```python
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
import numpy as np

digits = load_digits()
X = StandardScaler().fit_transform(digits.data)

# t-SNE is slow — reduce dimensionality with PCA first (best practice)
from sklearn.decomposition import PCA
X_pca50 = PCA(n_components=50).fit_transform(X)  # Reduce to 50 dims first

# Then apply t-SNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42, n_iter=1000)
X_tsne = tsne.fit_transform(X_pca50)
print(f"t-SNE reduced shape: {X_tsne.shape}")
# X_tsne can be visualized with matplotlib — points colored by y (digit class)
# t-SNE will show clear clusters for each digit
```

> [!WARNING]
> t-SNE is NOT a general-purpose dimensionality reduction technique. It is designed for visualization only. The distances and cluster sizes in a t-SNE plot are not meaningful for downstream ML tasks. Do not use t-SNE as input features for a classifier.

---

## Key Concepts

**Centroid** — The mean position of all points assigned to a cluster in k-means. The centroid is updated at each iteration until convergence.

**Silhouette Score** — A measure of how well a point fits its assigned cluster vs. the nearest neighboring cluster. Ranges from -1 (wrong cluster) to +1 (perfect cluster). Aggregate silhouette score can guide k selection.

**Inertia (WCSS)** — The sum of squared distances from each point to its cluster centroid. The objective k-means minimizes. Lower is better, but decreases monotonically with k — use elbow method to find the right balance.

**Explained Variance Ratio** — For each principal component, the fraction of total variance it captures. The first few components capture the most important structure; later components capture noise.

**Core Point (DBSCAN)** — A point with at least `min_samples` neighbors within radius `eps`. Core points define the dense regions that form clusters.

**Perplexity (t-SNE)** — A hyperparameter (typically 5–50) that balances attention between local and global structure. It roughly corresponds to the number of nearest neighbors each point interacts with.

---

## Examples

### Example 1: Customer Segmentation with k-Means

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Simulate customer RFM (Recency, Frequency, Monetary) data
np.random.seed(42)
n_customers = 500
data = {
    "recency_days": np.random.exponential(30, n_customers),   # Days since last purchase
    "frequency": np.random.poisson(5, n_customers) + 1,       # Number of purchases
    "monetary": np.random.lognormal(5, 1, n_customers),       # Total spend
}
df = pd.DataFrame(data)

# Scale the features — k-means uses Euclidean distance, so scale matters
X = StandardScaler().fit_transform(df.values)

# Find optimal k
best_k, best_sil = 2, -1
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    sil = silhouette_score(X, labels)
    if sil > best_sil:
        best_sil, best_k = sil, k
    print(f"k={k}: silhouette={sil:.3f}")

print(f"\nOptimal k: {best_k}")

# Fit final model and analyze segment profiles
km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["segment"] = km.fit_predict(X)

print("\nSegment profiles (original scale):")
print(df.groupby("segment").agg({"recency_days": "mean",
                                  "frequency": "mean",
                                  "monetary": "mean",
                                  "segment": "count"}).rename(columns={"segment": "count"}))
```

---

## Common Pitfalls

### Pitfall 1: Choosing k Based Only on WCSS (Elbow Method)

The elbow method is a heuristic — the "elbow" is often not obvious. Always combine it with silhouette score and domain knowledge.

### Pitfall 2: Interpreting t-SNE Distances as Meaningful

```python
# WRONG: using t-SNE output as features for a downstream classifier
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression

X_tsne = TSNE(n_components=2).fit_transform(X_train)
model = LogisticRegression()
model.fit(X_tsne, y_train)  # The t-SNE representation of test data would be different!

# CORRECT: use PCA or autoencoders for feature reduction before classification
from sklearn.decomposition import PCA
X_pca = PCA(n_components=50).fit_transform(X_train)
X_test_pca = PCA(n_components=50).fit(X_train).transform(X_test)  # Same transform
```

### Pitfall 3: Not Scaling Before k-Means or PCA

k-means uses Euclidean distance; PCA maximizes variance. Both are dominated by high-scale features if you don't standardize. Always use `StandardScaler` first.

---

## Cross-Links

- [[ai-ml/modules/02_math-for-ml]] — Eigendecomposition is the mathematical foundation of PCA
- [[ai-ml/modules/03_supervised-learning]] — Clustering features can be used as inputs to supervised models
- [[ai-ml/modules/07_deep-learning]] — Autoencoders (covered in the theory section) are neural-network-based dimensionality reduction
- [[ai-ml/modules/05_model-evaluation]] — Cluster evaluation metrics (silhouette, ARI, NMI) are covered in depth there

---

## Summary

- **Unsupervised learning finds structure without labels.** Clustering groups similar examples; dimensionality reduction compresses data while preserving structure.
- **k-means is fast and scalable but assumes spherical clusters.** Use the elbow method + silhouette score to choose k.
- **DBSCAN handles arbitrary cluster shapes and identifies outliers.** It does not require specifying k but is sensitive to `eps` and `min_samples`.
- **PCA is the standard tool for linear dimensionality reduction.** It is deterministic, interpretable, and suitable for downstream ML tasks.
- **t-SNE is for visualization only.** Its output cannot be used as features for another model.
- **Always scale features before clustering or PCA.** Unscaled features will dominate the results.
- **Evaluation without labels is hard.** Intrinsic metrics (silhouette, inertia) measure structure quality; extrinsic metrics (ARI, NMI) compare to known ground truth when available.
