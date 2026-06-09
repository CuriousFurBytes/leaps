# Projects: Module 12 — Capstone Project

> The capstone module IS the project. See the README for the full project brief, milestones, and acceptance criteria.
> This file contains governance memo and architecture documentation templates to support your project.

---

## Governance Memo Template

Use this template when writing the fairness audit governance memo (Milestone 5).

---

**TO:** Engineering Team and Product Stakeholders
**FROM:** [Your name]
**DATE:** [Date]
**RE:** Fairness Audit — [Model Name] v[Version]

**Executive Summary**

[1–2 sentences: what the model does and what the audit found]

**Fairness Metrics**

| Metric | Group A | Group B | Disparity | Threshold |
|--------|---------|---------|-----------|-----------|
| Demographic Parity | | | | |
| TPR (Equalized Opportunity) | | | | |
| Precision (Predictive Parity) | | | | |

**Key Findings**

1. [Finding 1: describe the most significant fairness issue found, or confirm no significant issues]
2. [Finding 2: secondary finding]
3. [Finding 3: third finding if applicable]

**Root Cause Analysis**

[Explain why the bias exists: is it in the training data? In the features? In the label definition?]

**Recommendations**

1. [Recommended action 1 with priority and estimated effort]
2. [Recommended action 2]
3. [Recommended action 3]

**Known Limitations of This Audit**

[What this audit could not assess due to data limitations, time constraints, or methodological gaps]

---

## Architecture Documentation Template

Include an architecture diagram in your project README. Here is a text-based template:

```
                    ┌─────────────────┐
                    │  Data Pipeline  │
                    │  (data_pipeline)│
                    └────────┬────────┘
                             │ train/val/test splits
                             ▼
                    ┌─────────────────┐
                    │  Model Training │
                    │  (train_model)  │
                    └────────┬────────┘
                             │ model artifacts
                             ▼
                    ┌─────────────────┐
                    │  MLflow Registry│
                    └────────┬────────┘
                             │ loads model
                             ▼
              ┌──────────────────────────┐
   request    │   FastAPI Serving API    │    prediction + log
 ──────────►  │   /health  /predict      │ ──────────────────►  SQLite DB
              └──────────────────────────┘
                             │
                             │ logged predictions
                             ▼
                    ┌─────────────────┐
                    │   Monitoring    │
                    │  (monitoring)   │
                    └─────────────────┘
```
