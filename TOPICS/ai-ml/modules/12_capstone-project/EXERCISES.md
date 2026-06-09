# Exercises: Module 12 — Capstone Project Milestones

> The capstone project uses this file for milestone checkpoints rather than traditional exercises.
> Each milestone produces a concrete, demonstrable deliverable.

## Instructions

Complete each milestone in order. Check each item as you complete it.
The milestones build on each other — do not skip ahead.

---

## Milestone 1: Data Pipeline (Beginner–Intermediate)

**Objective:** Reproducible, documented data pipeline

- [ ] Dataset selected and downloaded
- [ ] Data validation script written (shape, missing values, data types, class balance)
- [ ] Train/validation/test split created with stratification
- [ ] Data statistics logged to MLflow
- [ ] Script is runnable: `python data_pipeline.py` succeeds from scratch

**Checkpoint:** Show the MLflow UI with the data validation run.

---

## Milestone 2: Baseline Model (Intermediate)

**Objective:** A working, tracked baseline

- [ ] Classical ML baseline trained and evaluated with appropriate metrics
- [ ] Experiment tracked in MLflow with parameters and metrics
- [ ] Model registered in MLflow Model Registry as "staging"

**Checkpoint:** Show the MLflow experiment page with the baseline run.

---

## Milestone 3: Improved Model (Intermediate–Advanced)

**Objective:** Hyperparameter search and model comparison

- [ ] At least 10 different configurations trained and tracked
- [ ] Best model identified and promoted to "production" in MLflow Registry

**Checkpoint:** Show a comparison table of all runs in MLflow.

---

## Milestone 4: Serving API (Advanced)

**Objective:** A working, containerized prediction API

- [ ] FastAPI `/health` and `/predict` endpoints implemented
- [ ] Input validation with Pydantic
- [ ] Prediction logging to SQLite
- [ ] Model loaded from MLflow Registry
- [ ] Docker container builds and runs: `curl http://localhost:8000/health` returns healthy

**Checkpoint:** Live API demonstration.

---

## Milestone 5: Fairness Audit (Advanced)

**Objective:** Documented fairness analysis

- [ ] Three fairness metrics computed
- [ ] SHAP explanations for 10+ predictions
- [ ] Governance memo written

**Checkpoint:** Run `python fairness_audit.py`. Show governance memo.

---

## Milestone 6: Monitoring and Documentation (Expert)

**Objective:** Complete production-ready system with documentation

- [ ] Drift detection script implemented and tested
- [ ] Monitoring report written
- [ ] Project README complete: setup, architecture, design decisions, limitations

**Checkpoint:** Run `python monitoring.py`. Show project README.

---

## Final Submission Checklist

- [ ] `python data_pipeline.py && python train_model.py` succeeds end-to-end
- [ ] Docker API starts and responds to requests
- [ ] MLflow shows 3+ experiment runs with best model as "production"
- [ ] Fairness audit and governance memo complete
- [ ] Monitoring script runs successfully
- [ ] Project README explains the system to a new reader
