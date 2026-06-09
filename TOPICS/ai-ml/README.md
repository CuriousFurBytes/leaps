# AI and ML

> A zero-to-expert learning path for artificial intelligence, machine learning, and responsible model-building practice.

## Table of Contents
1. [Why Learn AI and ML?](#why-learn-ai-and-ml)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)
6. [Study Workflow](#study-workflow)

## Why Learn AI and ML?

Artificial intelligence is the broad effort to build systems that perform tasks normally associated with human judgment: perception, language, planning, decision-making, and adaptation. Machine learning is the family of methods that lets those systems improve from data rather than from only hand-written rules. Together they power search ranking, recommendations, fraud detection, medical imaging support, robotics, forecasting, copilots, and scientific discovery.

Learning AI and ML well means learning more than model names. You need the full loop: framing a problem, measuring data quality, choosing a baseline, training a model, evaluating failure modes, explaining tradeoffs, deploying safely, and monitoring drift. The core habit is evidence-based iteration: make a claim, test it against data, and update your design.

This topic starts from zero and rises to professional-level practice. Early modules emphasize vocabulary and runnable Python experiments; middle modules cover supervised, unsupervised, deep learning, natural language, and evaluation; advanced modules cover systems, MLOps, interpretability, safety, and research literacy. The final capstone requires a realistic project that integrates the full lifecycle.

## Prerequisites

- [[python]] — enough to read functions, lists, dictionaries, and simple scripts.
- [[statistics]] — helpful but not required at the start; probability, averages, variance, and sampling are revisited here.
- [[linear-algebra]] — helpful for expert depth; vectors, matrices, and dot products are introduced gradually.
- Basic command-line comfort: running `python`, creating folders, and reading error messages.

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Foundations](./modules/01_foundations/README.md) | Beginner | [ ] |
| 02 | [Data and Features](./modules/02_data_and_features/README.md) | Beginner | [ ] |
| 03 | [Supervised Learning](./modules/03_supervised_learning/README.md) | Intermediate | [ ] |
| 04 | Model Evaluation and Validation | Intermediate | [ ] |
| 05 | Unsupervised Learning and Representation | Intermediate | [ ] |
| 06 | Neural Networks and Deep Learning | Advanced | [ ] |
| 07 | Natural Language, Vision, and Multimodal AI | Advanced | [ ] |
| 08 | Optimization, Regularization, and Generalization | Advanced | [ ] |
| 09 | Explainability, Fairness, and Responsible AI | Advanced | [ ] |
| 10 | MLOps, Deployment, and Monitoring | Expert | [ ] |
| 11 | Research Literacy and System Design | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links

- [[python]] for implementation fluency and scripting.
- [[statistics]] for uncertainty, sampling, distributions, and inference.
- [[linear-algebra]] for vectors, matrices, embeddings, and neural networks.
- [[data-structures]] for representing datasets, graphs, token sequences, and indexes.
- [[ethics]] for responsible deployment decisions and harm analysis.

## Quick Reference

| Concept | Practical Meaning |
|---|---|
| Dataset | Examples used to train, validate, or test a model. |
| Feature | A measurable input signal used by a model. |
| Label | The target answer in supervised learning. |
| Training | Fitting model parameters to data. |
| Validation | Tuning decisions on data not used for fitting. |
| Test set | Final held-out estimate of performance. |
| Baseline | Simple first model used to prove improvement is real. |
| Overfitting | Memorizing training quirks instead of learning general patterns. |
| Drift | Production data changing after deployment. |

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install numpy pandas scikit-learn matplotlib
```

## Study Workflow

1. Read each module README before touching exercises.
2. Run every code block locally and change one variable to see what breaks.
3. Keep notes in each module's `NOTES.md` without deleting previous notes.
4. Use `QUESTIONS.md` for confusion, edge cases, and project ideas.
5. Treat the capstone as proof that you can connect models to real decisions.
