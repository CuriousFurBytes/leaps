# Projects: Artificial Intelligence and Machine Learning

> Project ideas organized by difficulty. Each project is a real, deployable artifact — not a toy exercise. Build these as portfolio pieces.

---

## Table of Contents

- [Beginner Projects](#beginner-projects)
- [Intermediate Projects](#intermediate-projects)
- [Advanced Projects](#advanced-projects)
- [Expert Projects](#expert-projects)
- [My Projects](#my-projects)

---

## Beginner Projects

### Project 1: Titanic Survival Predictor

**Modules required:** 01, 03, 05
**Estimated time:** 6–10 hours

Build a binary classifier to predict survival on the Titanic. This is the classic ML "hello world" problem. Use the Kaggle Titanic dataset (freely available).

**Deliverables:**
- Exploratory data analysis notebook (Markdown + code blocks — no `.ipynb`)
- Feature engineering: handle missing values, encode categorical variables
- Train and compare at least 3 classifiers (logistic regression, random forest, gradient boosting)
- Evaluate with accuracy, precision, recall, F1, and ROC-AUC
- Document the top 5 most important features

**What you learn:**
- End-to-end supervised learning pipeline
- Handling real-world messy data
- Model comparison and selection

---

### Project 2: House Price Regression

**Modules required:** 01, 03, 05
**Estimated time:** 8–12 hours

Predict house prices using the Ames Housing dataset. More features than Titanic — stronger focus on feature engineering.

**Deliverables:**
- Full data exploration with visualizations (matplotlib/seaborn)
- Feature engineering: polynomial features, log transforms, encoding
- Train linear regression, ridge regression, and gradient boosting
- Report RMSE and R² on a held-out test set
- Residual analysis: where does the model fail?

---

### Project 3: Customer Segmentation

**Modules required:** 01, 04
**Estimated time:** 6–8 hours

Segment customers into groups using unsupervised learning. Use a retail or e-commerce dataset (e.g., the UCI Online Retail dataset).

**Deliverables:**
- RFM (Recency, Frequency, Monetary) feature construction
- k-means clustering with elbow method for k selection
- PCA visualization of clusters
- Plain-language description of each customer segment and its business implications

---

## Intermediate Projects

### Project 4: Spam Email Classifier

**Modules required:** 03, 05, 08 (intro)
**Estimated time:** 10–15 hours

Build a spam classifier from scratch using TF-IDF features and classical ML — no neural networks required.

**Deliverables:**
- Text preprocessing pipeline (tokenization, stemming, stopword removal)
- TF-IDF feature extraction
- Naive Bayes, logistic regression, and SVM classifiers
- Precision/recall analysis (explain the tradeoff in the spam context — which matters more?)
- Cross-validation with stratified k-fold

---

### Project 5: Image Classifier with Transfer Learning

**Modules required:** 07
**Estimated time:** 12–18 hours

Build an image classifier using a pre-trained ResNet or EfficientNet (PyTorch). Use a dataset of your choice (e.g., a 10-class subset of ImageNet, or a domain-specific dataset you care about).

**Deliverables:**
- Data loading and augmentation pipeline using `torchvision`
- Fine-tune a pre-trained model on your dataset
- Training and validation loss/accuracy curves
- Confusion matrix and per-class precision/recall
- At least 5 misclassified examples with analysis of why the model failed

---

### Project 6: Time Series Forecasting

**Modules required:** 03, 05, 07
**Estimated time:** 12–16 hours

Forecast a time series (e.g., stock prices, energy consumption, weather) using both classical methods (ARIMA) and ML methods (LSTM or Temporal Convolutional Network).

**Deliverables:**
- Time series decomposition (trend, seasonality, residuals)
- ARIMA baseline
- LSTM or TCN implementation in PyTorch
- Proper train/validation/test split (no data leakage across time)
- RMSE, MAE, and MAPE metrics
- Discussion of when each approach is more appropriate

---

## Advanced Projects

### Project 7: Text Summarization with HuggingFace

**Modules required:** 08
**Estimated time:** 15–20 hours

Fine-tune a sequence-to-sequence model (e.g., T5 or BART) for abstractive text summarization on a dataset of your choice.

**Deliverables:**
- Data preprocessing and tokenization for seq2seq
- Fine-tuning with HuggingFace Trainer API
- ROUGE score evaluation
- Qualitative comparison of pre-fine-tuning vs. post-fine-tuning outputs
- Discussion of failure modes (hallucinations, truncation issues)

---

### Project 8: ML Model Serving API

**Modules required:** 09
**Estimated time:** 15–20 hours

Package a trained model as a production-ready REST API with monitoring.

**Deliverables:**
- FastAPI endpoint for inference (single predictions + batch)
- Request validation with Pydantic
- MLflow tracking of the model used
- Logging of prediction latency and input distribution
- Docker container for the API
- Health check endpoint

---

## Expert Projects

### Project 9: RAG Question-Answering System

**Modules required:** 08, 10
**Estimated time:** 20–30 hours

Build a retrieval-augmented generation (RAG) system that answers questions about a document collection.

**Deliverables:**
- Document ingestion and chunking pipeline
- Embedding model (e.g., `sentence-transformers`) for semantic search
- Vector store (e.g., FAISS or ChromaDB)
- LLM integration for answer generation
- Evaluation: accuracy on a set of held-out questions
- Latency profiling and optimization discussion

---

### Project 10: Fairness Audit of a Production Model

**Modules required:** 11, 03, 05
**Estimated time:** 15–20 hours

Take an existing ML model (e.g., the Titanic classifier from Project 1, or a credit scoring model from a public dataset) and audit it for fairness.

**Deliverables:**
- Define protected attributes (e.g., sex, age group)
- Compute group-specific metrics: accuracy, FPR, FNR
- Apply SHAP to explain individual predictions
- Identify at least 2 fairness violations
- Propose and implement one mitigation strategy
- Write a 1-page governance memo summarizing findings and recommendations

---

## My Projects

_Track your own projects here. Append a row when you start or complete a project._

| Project | Started | Status | Link | Notes |
|---------|---------|--------|------|-------|
| — | — | — | — | — |
