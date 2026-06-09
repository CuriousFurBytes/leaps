# Module 12: Capstone Project — End-to-End ML System

[← Module 11: Responsible AI](../11_responsible-ai/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-purple)
![Time](https://img.shields.io/badge/time-30--50h-orange)

> Build a complete, production-grade ML system end-to-end: data ingestion, model training with experiment tracking, a REST API serving layer, and a monitoring dashboard — then document the design tradeoffs.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Milestones](#milestones)
5. [Help and Getting Unstuck](#help-and-getting-unstuck)
6. [Acceptance Criteria](#acceptance-criteria)
7. [Cross-Links](#cross-links)
8. [A Note on Authenticity](#a-note-on-authenticity)

---

## Overview

This is your capstone project. Everything you have learned across 11 modules — the mathematics, the algorithms, the deep learning, the engineering, and the responsibility practices — comes together here. You will build a real ML system, not a tutorial exercise.

The project is intentionally open-ended. You choose the domain and the dataset. You make the architectural decisions. You document the tradeoffs. This mirrors how real ML engineering work is done.

> [!IMPORTANT]
> **This module does not hand you a solution.** The help sections below provide staged hints, architecture suggestions, and links back to relevant modules. Use them when you are genuinely stuck. The goal is for you to build it yourself — that is the only way it becomes a real learning experience and a real portfolio piece.

---

## Prerequisites

### Required Modules (All of them)

- [[ai-ml/modules/01_introduction]] through [[ai-ml/modules/11_responsible-ai]] — All prior modules
- Strong comfort with Python, scikit-learn, PyTorch or HuggingFace, FastAPI, and MLflow

---

## Project Brief

**Build a complete ML system that includes all five of the following components:**

### Component 1: Data Pipeline

Collect, clean, and version a real dataset. Write a reproducible pipeline that:
- Downloads or generates the data
- Validates data quality (checks for missing values, outliers, data types)
- Splits into train/validation/test sets with proper stratification
- Logs data statistics (shape, class distribution, feature statistics) to MLflow

**Dataset options** (choose one, or propose your own):
- Sentiment analysis: Amazon product reviews (huggingface `datasets`)
- Fraud detection: IEEE-CIS Fraud Detection (Kaggle, requires account)
- Image classification: CIFAR-10 or a custom subset of ImageNet
- Tabular regression: California housing, Ames housing, or NYC taxi trips
- Time series: Energy consumption forecasting (UCI ML repository)

### Component 2: Model Training with Experiment Tracking

Train at least three different model configurations and track all experiments. Requirements:
- At least one classical ML baseline (e.g., logistic regression, random forest)
- At least one deep learning model (if applicable to your dataset)
- All experiments tracked in MLflow: hyperparameters, metrics, model artifacts
- Proper cross-validation or holdout evaluation
- The best model registered in the MLflow Model Registry

### Component 3: Model Serving API

Serve the best model as a REST API with FastAPI. The API must:
- Accept prediction requests with input validation
- Return predictions with confidence scores
- Have a `/health` endpoint
- Log all predictions to a persistent store (SQLite, CSV, or a proper database)
- Be containerized with Docker (or have a working `Dockerfile`)

### Component 4: Fairness and Explainability Audit

Conduct a responsible AI audit of your production model:
- Select at least one protected attribute relevant to your domain
- Compute at least three fairness metrics (demographic parity, equalized odds, calibration)
- Produce SHAP explanations for at least 10 individual predictions
- Write a 1-page governance memo summarizing findings and recommendations

### Component 5: Monitoring

Implement basic production monitoring:
- Log prediction inputs and outputs over time
- Implement a drift detection check (KS test or PSI) on incoming features
- Implement an alerting rule: when drift exceeds a threshold, log a warning
- Write a monitoring report summarizing what you would do if drift were detected

---

## Milestones

Track your progress through these milestones. They are designed so that each one produces a working artifact.

### Milestone 1: Data Ready (Week 1–2)

- [ ] Dataset downloaded, validated, and split into train/val/test
- [ ] Basic EDA completed (distributions, missing values, class balance)
- [ ] Data statistics logged to MLflow
- [ ] Data pipeline is a runnable Python script (not a notebook)

**Deliverable:** `data_pipeline.py` — running it produces the train/val/test splits and logs stats.

### Milestone 2: Baseline Model (Week 2–3)

- [ ] At least one classical ML model trained and evaluated
- [ ] Proper evaluation: appropriate metrics for the problem (not just accuracy)
- [ ] Baseline experiment tracked in MLflow
- [ ] Model registered in MLflow Model Registry

**Deliverable:** `train_baseline.py` — a script that trains and registers the baseline.

### Milestone 3: Improved Model (Week 3–4)

- [ ] At least one additional model trained (neural network, or different algorithm)
- [ ] Hyperparameter tuning with at least 10 different configurations
- [ ] Best model clearly identified based on validation metrics
- [ ] Comparison table of all trained models

**Deliverable:** Experiment comparison in the MLflow UI, `train_model.py` for the best model.

### Milestone 4: Serving API (Week 4–5)

- [ ] FastAPI app with `/predict` and `/health` endpoints
- [ ] Input validation with Pydantic
- [ ] Prediction logging to SQLite (or equivalent)
- [ ] The API loads the best registered model from MLflow
- [ ] Docker container builds and runs successfully

**Deliverable:** Running `docker-compose up` starts the API; `curl http://localhost:8000/health` returns `{"status": "healthy"}`.

### Milestone 5: Fairness and Explainability (Week 5–6)

- [ ] Fairness metrics computed for all relevant groups
- [ ] At least one bias issue identified (or documented absence of bias)
- [ ] SHAP explanations for 10 individual predictions
- [ ] Governance memo written and included in the project

**Deliverable:** `fairness_audit.py` produces a fairness report; `governance_memo.md` is written.

### Milestone 6: Monitoring (Week 6)

- [ ] Drift detection script implemented
- [ ] Monitoring report written
- [ ] Project documentation complete: architecture diagram, design decisions, known limitations

**Deliverable:** `monitoring.py` runs drift checks on logged predictions; `README.md` for the project.

---

## Help and Getting Unstuck

<details>
<summary><strong>Hint 1: Choosing a dataset</strong></summary>

A good capstone dataset is:
- Publicly available (no login required, or Kaggle at most)
- Large enough to be interesting (>1000 examples) but not so large that training takes days
- Has a clear target variable
- Has some complexity (mixed types, some missing values, class imbalance is fine)

The California housing dataset from sklearn is a safe, well-understood choice for regression. For classification, the breast cancer or adult income datasets work well. If you want a NLP challenge, sentiment classification on the IMDb dataset (available via HuggingFace datasets) is excellent.
</details>

<details>
<summary><strong>Hint 2: MLflow setup</strong></summary>

Start MLflow with `mlflow ui` (local) or deploy to a cloud tracking server. The key objects are:
- `mlflow.set_experiment("my-experiment")` — create or select an experiment
- `with mlflow.start_run():` — start a run
- `mlflow.log_params({"n_estimators": 100, ...})` — log hyperparameters
- `mlflow.log_metrics({"test_auc": 0.95})` — log evaluation metrics
- `mlflow.sklearn.log_model(model, "model")` — save the model artifact

See [[ai-ml/modules/09_ml-engineering#theory]] for complete MLflow examples.
</details>

<details>
<summary><strong>Hint 3: FastAPI structure</strong></summary>

Structure your API as:
```
project/
├── app/
│   ├── main.py        # FastAPI app
│   ├── models.py      # Pydantic schemas
│   └── ml_utils.py    # Model loading and prediction logic
├── Dockerfile
├── requirements.txt
└── tests/
    └── test_api.py
```

Load the model at module level (not inside the endpoint function) to avoid re-loading on every request. See [[ai-ml/modules/09_ml-engineering]] for a complete FastAPI example.
</details>

<details>
<summary><strong>Hint 4: SHAP for your model type</strong></summary>

- **Tree-based models** (RandomForest, GradientBoosting, XGBoost): use `shap.TreeExplainer` — fastest
- **Linear models**: use `shap.LinearExplainer`
- **Neural networks / arbitrary models**: use `shap.DeepExplainer` (PyTorch) or `shap.KernelExplainer` (slowest, most general)

See [[ai-ml/modules/11_responsible-ai]] for complete SHAP examples.
</details>

<details>
<summary><strong>Hint 5: Drift detection baseline</strong></summary>

For continuous features, use the Kolmogorov-Smirnov (KS) test:
```python
from scipy.stats import ks_2samp
statistic, p_value = ks_2samp(reference_feature, production_feature)
drift_detected = p_value < 0.05
```

For categorical features, use the chi-squared test or Population Stability Index (PSI).
Log the drift statistics in MLflow or to a monitoring database.
See [[ai-ml/modules/09_ml-engineering]] for the complete drift detection example.
</details>

---

## Acceptance Criteria

Your capstone is complete when you can demonstrate all of the following:

1. **Reproducibility:** Running `python data_pipeline.py && python train_model.py` produces a trained model in the MLflow registry without manual intervention.
2. **Serving:** `docker-compose up` starts the API. `curl /health` returns `{"status": "healthy"}`. A prediction request returns a valid response with a probability score.
3. **Experiment tracking:** The MLflow UI shows at least 3 experiment runs with different hyperparameters. The best model is marked as "production" in the registry.
4. **Fairness:** The fairness audit computes at least 3 fairness metrics and the governance memo is written. If fairness issues are found, at least one mitigation is discussed.
5. **Monitoring:** The drift detection script runs successfully and produces a report. You can answer: "what would you do if drift exceeded the threshold?"
6. **Documentation:** A project-level `README.md` explains: what the system does, how to run it, what dataset was used, what the key design decisions were, and what the known limitations are.

---

## Cross-Links

- [[ai-ml/modules/01_introduction]] — ML workflow overview
- [[ai-ml/modules/05_model-evaluation]] — Evaluation metrics used throughout
- [[ai-ml/modules/09_ml-engineering]] — Feature pipelines, MLflow, FastAPI serving
- [[ai-ml/modules/11_responsible-ai]] — Fairness audit and SHAP explainability
- [[async-python]] — FastAPI async patterns
- [[devops-platform-engineering]] — Docker, CI/CD for the serving layer
- [[postgresql]] — If you use a database for prediction logging

---

## A Note on Authenticity

The value of this capstone comes from the decisions you make and the problems you solve. When you get stuck — and you will — use the hints above. They give you direction, not answers. If you copy code without understanding it, you will be able to run the capstone, but you will not learn from it.

A real ML system built by you, documented honestly (including the parts that did not work perfectly), is more valuable than a flawless copied solution. Write down what you tried, what failed, and what you learned. That documentation is the most important output of this project.
