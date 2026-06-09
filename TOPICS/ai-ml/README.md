# Artificial Intelligence and Machine Learning

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> A comprehensive, code-first journey through artificial intelligence and machine learning — from foundational concepts and mathematics to production-grade systems and responsible deployment.

> [!NOTE]
> **Topic Overview**
> This topic covers the full spectrum of AI and ML: the mathematical foundations that make learning algorithms possible, classical machine learning with scikit-learn, deep learning with PyTorch, natural language processing and transformers, production ML engineering, large language models, and responsible AI. Each module builds on the last, culminating in an end-to-end ML system as the capstone project.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty & Time Estimate](#difficulty--time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

Artificial Intelligence (AI) is the broad field concerned with building systems that exhibit intelligent behavior. Machine Learning (ML) is a subfield of AI in which systems learn patterns from data rather than following explicitly programmed rules. Deep Learning (DL) is a subfield of ML that uses multi-layer neural networks to learn hierarchical representations — and it is responsible for the dramatic progress in AI over the last decade.

Understanding this hierarchy matters because the terms are often conflated in popular usage. Not every AI system uses ML (rule-based expert systems do not), and not every ML system uses deep learning (random forests and SVMs are powerful without any neural networks). The choice of approach depends on the problem, the data available, and the constraints of deployment.

Machine learning problems are traditionally categorized by the nature of the feedback signal: **supervised learning** trains on labeled input-output pairs and learns a mapping from inputs to outputs; **unsupervised learning** finds structure in unlabeled data; and **reinforcement learning** optimizes a policy through a reward signal. Each paradigm has a distinct mathematical formulation and a distinct set of algorithms — understanding all three gives you a much richer toolkit than knowing only one.

The current state of AI in 2024-2025 is dominated by large language models (LLMs) and foundation models. Models like GPT-4, Claude, and Gemini demonstrate emergent capabilities that were not anticipated from their training objectives. Multimodal models can process text, images, audio, and video together. The engineering challenges have shifted from "can we train a model that does X" to "how do we deploy, evaluate, monitor, and govern models responsibly at scale." This curriculum addresses both the fundamentals and this cutting edge.

### Why It Matters

Machine learning is no longer a niche specialty — it is a core engineering skill. Every major software product now incorporates ML components: recommendation systems, search ranking, fraud detection, content moderation, medical diagnosis, and code generation all rely on learned models. Understanding how these systems work — and where they fail — is essential for any engineer building or integrating them.

Beyond the career case, ML literacy changes how you think about data and uncertainty. The mental models from statistics, optimization, and information theory that underpin ML are broadly useful in systems design, experimentation, and decision-making. Proficiency in this area is expected in roles such as ML Engineer, Data Scientist, Research Engineer, and increasingly in senior Software Engineering roles at companies where models are first-class infrastructure.

### Key Features of This Topic

- **Mathematics-first** — Linear algebra, calculus, and statistics are taught in the context of why ML needs them, not as abstract prerequisites
- **Code-centric** — Every concept is illustrated with runnable Python using numpy, pandas, scikit-learn, PyTorch, and HuggingFace
- **End-to-end** — Covers the full pipeline from raw data to a deployed, monitored model
- **Current** — Includes transformers, LLMs, RAG, prompt engineering, and responsible AI as of 2024-2025

---

## Historical Context

The field of Artificial Intelligence was formally founded at the **Dartmouth Summer Research Project on Artificial Intelligence** in **1956**, organized by John McCarthy, Marvin Minsky, Nathaniel Rochester, and Claude Shannon. McCarthy coined the term "Artificial Intelligence" for this event. But the intellectual foundations stretch back further.

In **1950**, Alan Turing published "Computing Machinery and Intelligence," posing the question "Can machines think?" and proposing the Turing Test as a behavioral criterion for intelligence. This paper established the philosophical framing that would shape the field for decades.

### Timeline

| Year | Event |
|------|-------|
| 1950 | Alan Turing publishes "Computing Machinery and Intelligence" — the Turing Test |
| 1956 | Dartmouth Conference — the term "Artificial Intelligence" is coined by John McCarthy |
| 1957 | Frank Rosenblatt introduces the Perceptron, the first trainable neural unit |
| 1969 | Minsky & Papert's "Perceptrons" reveals limitations of single-layer networks — contributing to the first AI winter |
| 1974–1980 | First AI Winter — reduced funding and interest after symbolic AI fails to scale |
| 1980 | Expert systems gain traction; Japan's Fifth Generation project re-ignites funding |
| 1986 | Rumelhart, Hinton, and Williams publish backpropagation for multi-layer networks |
| 1987–1993 | Second AI Winter — expert systems collapse under maintenance costs |
| 1997 | IBM Deep Blue defeats Garry Kasparov at chess |
| 1998 | LeCun's LeNet demonstrates convolutional neural networks for digit recognition |
| 2006 | Hinton and Salakhutdinov publish deep belief networks, reigniting deep learning research |
| 2012 | AlexNet wins ImageNet by a large margin — the "ImageNet moment" and start of the DL era |
| 2014 | Generative Adversarial Networks (GANs) introduced by Goodfellow et al. |
| 2016 | AlphaGo (DeepMind) defeats Lee Sedol — first program to beat a top human at Go |
| 2017 | "Attention Is All You Need" (Vaswani et al.) introduces the Transformer architecture |
| 2018 | BERT (Google) introduces bidirectional pre-training for NLP |
| 2019 | GPT-2 (OpenAI) demonstrates large-scale language generation |
| 2020 | GPT-3 — 175B parameters; few-shot learning from prompts |
| 2021 | AlphaFold 2 (DeepMind) solves the protein folding problem |
| 2022 | ChatGPT launches; Stable Diffusion democratizes image generation |
| 2023 | GPT-4, Claude 2, Gemini — multimodal LLMs become mainstream |
| 2024–2025 | Reasoning models, agents, and multi-modal foundation models dominate research and products |

The pattern in this timeline is instructive: AI progresses in cycles, driven by compute availability, algorithmic breakthroughs, and data scale. Each AI winter was caused by over-promising and under-delivering. The current era is different in that capabilities are empirically measurable and economically valuable — but the field must still grapple with reliability, alignment, and interpretability.

---

## Real-World Applications

AI and ML are actively used across virtually every domain:

- **Healthcare** — AlphaFold 2 (DeepMind) predicted the 3D structure of nearly all known proteins, a problem that had resisted 50 years of biochemical effort. ML models detect tumors in medical images, predict drug interactions, and personalize treatment recommendations.
- **Language and Communication** — GPT-4 (OpenAI) and similar models demonstrate broad language understanding, code generation, and reasoning. These models power customer support, document summarization, and coding assistants used by millions of developers daily.
- **Autonomous Systems** — Waymo (Alphabet) operates a commercial robotaxi service using ML models for perception, prediction, and planning. Self-driving systems process LiDAR, cameras, and radar in real time to make driving decisions.
- **Recommendation and Personalization** — Netflix uses ML for content recommendations. Spotify's Discover Weekly uses collaborative filtering and audio embeddings to surface music users did not know they would like.
- **Finance and Security** — Stripe, Visa, and Mastercard use ML for real-time fraud detection, making billions of binary classification decisions per day with sub-millisecond latency requirements.
- **Scientific Discovery** — ML accelerates physics simulations, climate modeling, materials discovery, and genomics. Transformer models trained on protein sequences can predict function and guide drug design.

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the AI/ML/DL hierarchy, distinguish supervised, unsupervised, and reinforcement learning, and select the appropriate approach for a given problem
2. Apply the core mathematical tools — linear algebra, calculus, probability, and statistics — to understand why ML algorithms work the way they do
3. Implement and tune classical ML algorithms (regression, classification, clustering, dimensionality reduction) using scikit-learn on real datasets
4. Evaluate models rigorously using cross-validation, precision/recall, AUC-ROC, and calibration — and avoid common evaluation pitfalls like data leakage
5. Build and train deep neural networks using PyTorch, including CNNs for images, RNNs/LSTMs for sequences, and Transformer-based models for text
6. Engineer and serve production ML pipelines using FastAPI, MLflow for experiment tracking, and feature stores — and monitor models for drift in production
7. Understand the architecture of large language models, apply prompt engineering, build RAG systems, and fine-tune models with HuggingFace
8. Audit models for fairness and bias, apply SHAP/LIME for explainability, and articulate the governance considerations for responsible AI deployment

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Intermediate → Expert |
| **Estimated Total Hours** | 120–180 hours |
| **Prerequisites** | Python basics, basic linear algebra, basic statistics |
| **Recommended Pace** | 5–8 hours/week |
| **Topic Type** | Mixed (theoretical foundations + heavy practical implementation) |
| **Suitable For** | Software engineers moving into ML, CS students, data scientists formalizing their understanding |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- [[async-python]] — Python functions, classes, list comprehensions, and the standard library; familiarity with pip and virtual environments
- [[postgresql]] — Basic SQL for data querying; understanding of tabular data and joins
- Basic linear algebra — vectors, matrices, and matrix multiplication (covered in depth in Module 02)
- Basic statistics — mean, variance, probability distributions (covered in depth in Module 02)

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If you can write a Python function, use numpy arrays, and understand what "fitting a model to data" means intuitively, you are ready to begin.
> The math will be developed rigorously in Module 02 — don't let unfamiliarity with eigenvalues stop you from starting.

---

## Learning Modules

| # | Module | Topic | Difficulty | Status | Score |
|---|--------|-------|------------|--------|-------|
| 01 | [Introduction to AI and ML](./modules/01_introduction/) | What AI/ML/DL are, ML workflow, bias-variance tradeoff, environment setup | Beginner | - [ ] | —/— |
| 02 | [Mathematics for ML](./modules/02_math-for-ml/) | Linear algebra, probability, statistics, calculus for gradients | Intermediate | - [ ] | —/— |
| 03 | [Supervised Learning](./modules/03_supervised-learning/) | Regression, classification, trees, forests, SVM, k-NN | Intermediate | - [ ] | —/— |
| 04 | [Unsupervised Learning](./modules/04_unsupervised-learning/) | k-means, DBSCAN, PCA, t-SNE, autoencoders | Intermediate | - [ ] | —/— |
| 05 | [Model Evaluation](./modules/05_model-evaluation/) | Cross-validation, metrics, hyperparameter tuning, A/B testing | Intermediate | - [ ] | —/— |
| 06 | [Neural Networks](./modules/06_neural-networks/) | Perceptron, MLP, backpropagation from scratch, activations | Advanced | - [ ] | —/— |
| 07 | [Deep Learning](./modules/07_deep-learning/) | CNNs, RNNs, LSTMs, batch norm, dropout, transfer learning (PyTorch) | Advanced | - [ ] | —/— |
| 08 | [NLP and Transformers](./modules/08_nlp-and-transformers/) | Embeddings, attention, BERT/GPT, fine-tuning with HuggingFace | Advanced | - [ ] | —/— |
| 09 | [ML Engineering](./modules/09_ml-engineering/) | Feature pipelines, model serving, MLflow, monitoring | Advanced | - [ ] | —/— |
| 10 | [LLMs and Generative AI](./modules/10_llms-and-generative-ai/) | LLM architecture, prompt engineering, RAG, agents | Expert | - [ ] | —/— |
| 11 | [Responsible AI](./modules/11_responsible-ai/) | Fairness, bias detection, SHAP/LIME, privacy, governance | Expert | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | End-to-end ML system: data → model → API → monitoring | Expert | - [ ] | —/— |

**Status key:** ` ` Not started &nbsp;·&nbsp; `~` In progress &nbsp;·&nbsp; `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 12 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 60 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **624** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to AI and ML)
- [ ] **Foundation Built** — Complete Modules 01–03 with ≥ 70% on each test
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Core Mastery** — Score ≥ 80% on all Modules 01–08
- [ ] **First Project Shipped** — Complete at least one project from PROJECTS.md
- [ ] **Deep Practitioner** — Complete Modules 09–11 (Engineering, LLMs, Responsible AI)
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Deep Work** — Complete the Capstone Project end-to-end
- [ ] **Research Ready** — Score ≥ 90% average across all modules

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% &nbsp;·&nbsp; B ≥ 80% &nbsp;·&nbsp; C ≥ 70% &nbsp;·&nbsp; D ≥ 60% &nbsp;·&nbsp; F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for AI and Machine Learning:

- [[async-python]] — Python foundations; async patterns used in ML serving and data pipelines
- [[postgresql]] — SQL for feature stores, experiment tracking databases, and data warehousing
- [[systems-architecture]] — Distributed systems concepts underlying large-scale ML training and inference
- [[devops-platform-engineering]] — CI/CD, containerization, and infrastructure for MLOps pipelines

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Started Topic

**What I did today:**
- Read the topic overview and ROADMAP.md
- Set up the learning environment (numpy, pandas, matplotlib, scikit-learn, PyTorch)
- Reviewed prerequisites: Python functions, basic numpy, statistics fundamentals

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "ai-ml"
topic_name: "Artificial Intelligence and Machine Learning"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 624
completion_percentage: 0
difficulty: "Intermediate → Expert"
estimated_hours: 150
prerequisites:
  - "async-python"
  - "postgresql"
related_topics:
  - "async-python"
  - "postgresql"
  - "systems-architecture"
  - "devops-platform-engineering"
tags:
  - "machine-learning"
  - "deep-learning"
  - "python"
  - "data-science"
  - "neural-networks"
  - "nlp"
  - "llm"
creator: "Various — field established Dartmouth 1956"
year_created: "1956"
```
