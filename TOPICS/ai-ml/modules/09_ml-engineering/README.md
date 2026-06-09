# Module 09: ML Engineering

[← Module 08: NLP and Transformers](../08_nlp-and-transformers/) | [Topic Home](../../README.md) | [Next → Module 10: LLMs and Generative AI](../10_llms-and-generative-ai/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-12--16h-orange)

> Taking ML from notebook to production: feature engineering pipelines, model serving with FastAPI, experiment tracking with MLflow, model versioning, and monitoring for data and concept drift.

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

The gap between "model works in a notebook" and "model works in production" is larger than most practitioners expect. Production ML requires: reproducible feature pipelines, versioned models, a serving layer that can handle real traffic, experiment tracking so you know what you tried, and monitoring to detect when the model degrades.

This module covers MLOps — the operational practices that turn ML experiments into reliable production systems. A practitioner who cannot deploy and monitor their own models is not yet production-ready. This module changes that.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/03_supervised-learning]] — The models being deployed
- [[ai-ml/modules/05_model-evaluation]] — Evaluation metrics used in monitoring

### Required Concepts

- **REST APIs** — HTTP requests, JSON, status codes
- **Docker basics** — containers, images, Dockerfiles
- **[[async-python]]** — async patterns used in FastAPI

---

## Objectives

By the end of this module, you will be able to:

1. Build reproducible feature engineering pipelines using sklearn `Pipeline` and `ColumnTransformer`
2. Track ML experiments (parameters, metrics, artifacts) with MLflow
3. Register, version, and load models from the MLflow Model Registry
4. Serve a trained model as a REST API using FastAPI with input validation
5. Containerize a model serving API with Docker
6. Monitor a production model for data drift using statistical tests

---

## Theory

### Feature Engineering Pipelines

A scikit-learn `Pipeline` chains preprocessing steps and a model into a single object that can be fit, serialized, and applied consistently. `ColumnTransformer` applies different transformations to different columns.

```python
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

# Example dataset: mixed numeric and categorical features
data = {
    "age": [25, np.nan, 35, 45, 22],
    "income": [50000, 75000, np.nan, 90000, 30000],
    "education": ["bachelor", "master", "bachelor", np.nan, "high_school"],
    "city": ["NYC", "SF", "NYC", "Chicago", "SF"],
    "churn": [0, 0, 1, 0, 1]
}
df = pd.DataFrame(data)
X = df.drop("churn", axis=1)
y = df["churn"]

# Numeric pipeline: impute missing values, then scale
numeric_features = ["age", "income"]
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),  # Fill NaN with median
    ("scaler", StandardScaler()),
])

# Categorical pipeline: impute, then one-hot encode
categorical_features = ["education", "city"]
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

# Combine both pipelines
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features),
])

# Full pipeline: preprocessing + model
full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", GradientBoostingClassifier(n_estimators=100, random_state=42)),
])

# The entire pipeline can be cross-validated and serialized
full_pipeline.fit(X, y)

# Serialize for deployment
import joblib
joblib.dump(full_pipeline, "model.pkl")  # Save entire pipeline
loaded_pipeline = joblib.load("model.pkl")
```

### MLflow Experiment Tracking

```python
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import roc_auc_score

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42
)

# MLflow tracks every experiment run
mlflow.set_experiment("breast-cancer-gbt")

with mlflow.start_run(run_name="gbt-n100-lr01"):
    # Log hyperparameters
    params = {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 3}
    mlflow.log_params(params)

    # Train
    model = GradientBoostingClassifier(**params, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    train_auc = roc_auc_score(y_train, model.predict_proba(X_train)[:, 1])
    test_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

    # Log metrics
    mlflow.log_metrics({"train_auc": train_auc, "test_auc": test_auc})

    # Log the model artifact
    mlflow.sklearn.log_model(model, "model")

    print(f"Run ID: {mlflow.active_run().info.run_id}")
    print(f"Train AUC: {train_auc:.3f}, Test AUC: {test_auc:.3f}")

# View experiments: run `mlflow ui` in the terminal → http://localhost:5000
```

### Model Serving with FastAPI

```python
# app.py — A minimal model serving API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import joblib
import numpy as np
from typing import List

app = FastAPI(title="Churn Prediction API", version="1.0.0")

# Load model at startup (not on every request)
model = joblib.load("model.pkl")

class PredictionRequest(BaseModel):
    """Input schema with validation."""
    age: float
    income: float
    education: str
    city: str

    @validator("age")
    def age_must_be_positive(cls, v):
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v

    @validator("income")
    def income_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Income must be non-negative")
        return v

class PredictionResponse(BaseModel):
    churn_probability: float
    prediction: int  # 0 or 1

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_version": "1.0.0"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    import pandas as pd
    # Convert to DataFrame (pipeline expects this format)
    input_df = pd.DataFrame([request.dict()])
    try:
        prob = model.predict_proba(input_df)[0, 1]
        pred = int(prob >= 0.5)
        return PredictionResponse(churn_probability=round(float(prob), 4),
                                   prediction=pred)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn app:app --reload
# Test with: curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
#   -d '{"age": 35, "income": 60000, "education": "bachelor", "city": "NYC"}'
```

### Monitoring for Drift

```python
import numpy as np
from scipy.stats import ks_2samp

def detect_data_drift(reference_data: np.ndarray,
                      production_data: np.ndarray,
                      feature_names: list,
                      alpha: float = 0.05) -> dict:
    """
    Detect data drift using the Kolmogorov-Smirnov test.
    If p-value < alpha, the distributions are significantly different (drift detected).

    Args:
        reference_data: Data from the training period (baseline)
        production_data: Recent production data
        feature_names: Names of the features
        alpha: Significance level for the KS test

    Returns:
        Dictionary of drift results per feature
    """
    results = {}
    for i, feature in enumerate(feature_names):
        ref = reference_data[:, i]
        prod = production_data[:, i]
        statistic, p_value = ks_2samp(ref, prod)
        drifted = p_value < alpha
        results[feature] = {
            "ks_statistic": round(statistic, 4),
            "p_value": round(p_value, 4),
            "drift_detected": drifted,
        }
        if drifted:
            print(f"[DRIFT] {feature}: KS={statistic:.3f}, p={p_value:.3f} (< {alpha})")
        else:
            print(f"[OK]    {feature}: KS={statistic:.3f}, p={p_value:.3f}")
    return results

# Simulate: training distribution vs. shifted production distribution
np.random.seed(42)
n = 1000
reference = np.column_stack([
    np.random.normal(0, 1, n),   # Feature 1: stable
    np.random.normal(5, 2, n),   # Feature 2: stable
])
production = np.column_stack([
    np.random.normal(0, 1, n),   # Feature 1: no drift
    np.random.normal(7, 2, n),   # Feature 2: DRIFTED (mean shifted from 5 to 7)
])

detect_data_drift(reference, production,
                  feature_names=["feature_1", "feature_2"])
```

---

## Key Concepts

**Feature Store** — A centralized repository that stores computed features for reuse across models and teams. Prevents duplicate computation and ensures consistency between training and serving.

**Model Registry** — A versioned store for trained model artifacts. MLflow, Weights & Biases, and SageMaker all provide model registries. Enables rolling back to a previous version when a new model degrades.

**Data Drift** — When the distribution of input features in production diverges from the training distribution. The model may still be technically correct given the inputs, but the inputs themselves have changed.

**Concept Drift** — When the relationship between inputs and the correct output changes. The world has changed and the model's knowledge is stale. Requires retraining.

**Serving Latency** — The time between receiving a prediction request and returning a response. Common targets: <10ms (real-time), <100ms (interactive), <1s (batch).

---

## Examples

### Example 1: Comparing Two Model Versions in Production (A/B Test)

```python
import random

def ab_test_router(model_a, model_b, features, traffic_split=0.5):
    """
    Route prediction requests to model A or B based on traffic split.
    In production, log which model was used with each prediction for later analysis.
    """
    use_model_b = random.random() < traffic_split

    if use_model_b:
        prediction = model_b.predict([features])[0]
        model_used = "B"
    else:
        prediction = model_a.predict([features])[0]
        model_used = "A"

    # In production: log (features, prediction, model_used, timestamp) to database
    # After enough traffic: compare outcomes for users served by A vs B

    return prediction, model_used
```

---

## Common Pitfalls

### Pitfall 1: Training-Serving Skew

```python
# WRONG: different preprocessing at training vs. serving time
# Training:
X_train_scaled = scaler.fit_transform(X_train)  # Uses training statistics

# Serving (WRONG):
# If you recompute the scaler at serving time, you will use different statistics
new_scaler = StandardScaler()
X_new_scaled = new_scaler.fit_transform(X_new)  # WRONG — different mean/std!

# CORRECT: serialize the ENTIRE pipeline including the fitted scaler
import joblib
pipeline = Pipeline([("scaler", StandardScaler()), ("model", clf)])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, "pipeline.pkl")  # Saves both scaler and model

# At serving time:
pipeline = joblib.load("pipeline.pkl")
prediction = pipeline.predict(X_new)  # Uses same scaler statistics
```

### Pitfall 2: Loading the Model on Every Request

```python
# WRONG: loading model on every API call
@app.post("/predict")
def predict(request):
    model = joblib.load("model.pkl")  # Disk IO on every request — very slow!
    return model.predict(request.features)

# CORRECT: load once at startup
model = joblib.load("model.pkl")  # Module-level: loads once
@app.post("/predict")
def predict(request):
    return model.predict(request.features)
```

### Pitfall 3: Not Logging Predictions for Monitoring

Without logging production predictions (and eventually outcomes), you cannot detect when a model degrades. Log inputs, outputs, and metadata for every prediction.

---

## Cross-Links

- [[ai-ml/modules/03_supervised-learning]] — The models being packaged and served
- [[ai-ml/modules/05_model-evaluation]] — Evaluation metrics monitored in production
- [[async-python]] — Async FastAPI patterns for high-throughput serving
- [[devops-platform-engineering]] — CI/CD pipelines for ML; Docker; Kubernetes for ML workloads
- [[postgresql]] — Database for logging predictions and outcomes

---

## Summary

- **The gap between notebook and production is larger than it looks.** Feature pipelines, serialization, serving, versioning, and monitoring are all required for a production ML system.
- **Always use sklearn Pipelines.** They prevent training-serving skew by bundling preprocessing and model into one serializable object.
- **MLflow experiment tracking makes ML reproducible.** Log every run with parameters, metrics, and model artifacts.
- **FastAPI + Pydantic provides input validation for free.** Validate inputs before they reach the model — bad inputs should return informative errors, not silently produce bad predictions.
- **Monitor for data drift and concept drift.** Production data changes. A model that was excellent at launch may degrade without anyone noticing if you are not monitoring.
- **A/B testing is the gold standard for comparing model versions.** Compare outcomes, not just offline metrics.
