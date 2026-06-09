# Projects: Module 01 — Introduction to AI and Machine Learning

> Projects that apply the concepts from this module. These are starter projects — build them for real, not just as exercises.

---

## Project 1: End-to-End Iris Classification Pipeline (Beginner)

**Time estimate:** 3–4 hours
**Skills practiced:** Full ML workflow, EDA, train/test split, evaluation

Build a clean, reusable Python script (not a notebook) that:

1. Loads the Iris dataset
2. Performs EDA: prints shape, class distribution, and per-feature statistics
3. Splits with stratification
4. Scales features correctly (no leakage)
5. Trains a `DecisionTreeClassifier`
6. Produces a `classification_report` and saves it to a text file
7. Takes `max_depth` as a command-line argument so it is easy to experiment

**Acceptance criteria:**
- Running `python iris_classifier.py --max_depth 3` produces a clean report
- The preprocessing is correctly implemented (no data leakage)
- The script handles the case where `max_depth` is too large (document the expected behavior)

---

## Project 2: Bias-Variance Explorer (Intermediate)

**Time estimate:** 4–6 hours
**Skills practiced:** Bias-variance tradeoff, validation curves, model comparison

Build a Python script that empirically demonstrates the bias-variance tradeoff on a dataset of your choice.

Requirements:
1. Use a real dataset (not Iris — try the wine, breast cancer, or digits datasets from sklearn)
2. Train a `DecisionTreeClassifier` for each depth from 1 to 25
3. For each depth, compute and store: training accuracy, 5-fold cross-validation accuracy
4. Print a formatted table showing both metrics for every depth
5. Identify and print: the depth with best CV accuracy, the depth where overfitting begins
6. Write a short (3–5 paragraph) analysis of your results

**Bonus:** Repeat the same experiment with a `KNeighborsClassifier` varying `n_neighbors`. How does the bias-variance tradeoff manifest differently for a nearest-neighbor model vs. a tree?

---

## Project 3: ML Problem Classification Guide (Beginner)

**Time estimate:** 2–3 hours
**Skills practiced:** Problem framing, paradigm selection, metric selection

Create a Markdown reference document that classifies 10 real-world ML applications. For each application:

1. State the application in one sentence (e.g., "Predict whether an email is spam")
2. Identify the ML paradigm (supervised/unsupervised/reinforcement) and justify it
3. Identify the specific problem type (classification/regression/clustering/etc.)
4. State what the input features would be
5. State what the label/target is (or what structure you're looking for)
6. Identify the primary evaluation metric and why

Choose applications from at least 3 different domains (healthcare, finance, media, e-commerce, science, etc.).

This project develops the problem-framing skill that practitioners use before writing any code.
