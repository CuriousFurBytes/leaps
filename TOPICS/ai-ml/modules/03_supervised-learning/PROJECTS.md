# Projects: Module 03 — Supervised Learning

## Project 1: Titanic Survival Predictor (Beginner)
**Time estimate:** 8–10 hours
Use the Titanic dataset (https://www.kaggle.com/c/titanic). Engineer features (title from name, family size, fare per person). Compare at least 4 classifiers. Submit to Kaggle and document your approach.

## Project 2: Salary Prediction Engine (Intermediate)
**Time estimate:** 10–14 hours
Build a regression pipeline to predict salaries from job postings. Use the UCI Adult Income dataset. Handle categorical features with encoding. Use Lasso for feature selection. Explain the top 5 factors driving salary in plain language.

## Project 3: Algorithm Benchmarking Suite (Advanced)
**Time estimate:** 12–16 hours
Build a reusable benchmarking harness that:
- Accepts any sklearn-compatible dataset
- Trains all 6 algorithms from this module with default settings
- Runs proper 5-fold stratified CV
- Produces a comparison table with mean ± std for accuracy, AUC-ROC, and F1
- Runs on at least 5 different datasets and identifies which algorithm wins most often
