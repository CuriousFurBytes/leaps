# Test: Module 04 — Unsupervised Learning

**Instructions:** Answer all questions directly below each question.
**Total Points:** 37 pts | **Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What does k-means minimize? Write the objective function in mathematical notation.
> Answer:

**Q2.** Name two scenarios where DBSCAN would outperform k-means.
> Answer:

**Q3.** What does "explained variance ratio" mean in PCA?
> Answer:

**Q4.** What does a silhouette score of -0.3 for a data point indicate?
> Answer:

**Q5.** Why is t-SNE not suitable for generating features for a downstream classifier?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the k-means++ initialization method and why it produces better results than random centroid initialization.
> Answer:

**Q7.** DBSCAN has two hyperparameters: `eps` and `min_samples`. Explain what happens when `eps` is set too large or too small.
> Answer:

**Q8.** PCA projects data onto orthogonal directions. Why must the components be orthogonal?
> Answer:

**Q9.** You run k-means on customer data and get clusters with silhouette score 0.2. A colleague says this is "good enough." How would you evaluate whether this clustering is meaningful from a business perspective?
> Answer:

**Q10.** Explain the relationship between PCA and autoencoders. What does a linear autoencoder with a bottleneck learn?
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Apply k-means to the wine dataset. Use silhouette score to select k. Report the best k and interpret each cluster in terms of the wine features.
> Answer:
```python
# Write your code here
```

**Q12.** A dataset has 10,000 features. You want to apply k-means clustering but it is too slow. Describe a two-step pipeline to make this tractable, including which dimensionality reduction method to use and why.
> Answer:

**Q13.** Implement DBSCAN parameter selection: for a 2D dataset, compute the k-nearest-neighbor distances and use the "knee" in the sorted distance plot to suggest eps. Implement and demonstrate.
> Answer:
```python
# Write your code here
```

**Q14.** Compare PCA and t-SNE on the digits dataset: apply both, project to 2D, and compute the ARI between the 2D k-means clusters and the true labels. Which dimensionality reduction method produces clusters that align better with the true digit classes?
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Prove that PCA finds the directions of maximum variance by deriving the eigenvalue problem from the variance maximization objective. Show that the principal components are the eigenvectors of the covariance matrix.
> Answer:

**Q16.** Design an unsupervised anomaly detection system for a financial transaction dataset (no labels). Specify: which algorithm, how to tune parameters, how to set a threshold for flagging anomalies, and how to evaluate whether the system is working given no ground truth labels.
> Answer:

---

## Bonus Question (5 pts)

**Bonus 1.** Implement Gaussian Mixture Models (GMM) from scratch using the EM algorithm. Compare it to k-means on a dataset with overlapping, elliptical clusters. Why does GMM perform better in this setting? (+5 pts)
> Answer:
