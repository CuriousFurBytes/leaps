# Resources: Artificial Intelligence and Machine Learning

> A curated list of high-quality, verified resources for this topic. Resources are organized by type and annotated with notes on what each is best for. All URLs have been checked for accuracy — do not add resources you cannot verify.

---

## Table of Contents

- [Books](#books)
- [Online Courses](#online-courses)
- [Documentation and References](#documentation-and-references)
- [Papers](#papers)
- [Tools and Libraries](#tools-and-libraries)
- [Communities](#communities)

---

## Books

### Foundational

- **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron** (3rd edition, O'Reilly, 2022)
  The single best practical introduction to ML. Covers the full sklearn API, neural networks, and TensorFlow. Ideal companion for Modules 03–07. Code examples are on GitHub.
  [Verify URL: O'Reilly learning platform or publisher page — confirm before sharing]

- **"Deep Learning" by Ian Goodfellow, Yoshua Bengio, and Aaron Courville** (MIT Press, 2016)
  The canonical textbook for deep learning. Dense and rigorous — best used as a reference alongside Modules 06–08 rather than read cover-to-cover at the start. Available free online at [https://www.deeplearningbook.org](https://www.deeplearningbook.org).

- **"Pattern Recognition and Machine Learning" by Christopher M. Bishop** (Springer, 2006)
  A rigorous, Bayesian-flavored treatment of ML. Best for Modules 02–05 when you want deeper mathematical grounding. Available free at [https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf](https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf).

### Specialized

- **"Natural Language Processing with Transformers" by Lewis Tunstall, Leandro von Werra, and Thomas Wolf** (O'Reilly, 2022)
  The best practical guide to HuggingFace Transformers. Companion to Module 08. Authors are core HuggingFace team members.
  [Verify URL: O'Reilly or HuggingFace course page]

- **"Designing Machine Learning Systems" by Chip Huyen** (O'Reilly, 2022)
  Covers the full ML system lifecycle — data, training, evaluation, deployment, monitoring, and business considerations. Essential companion for Module 09.
  [Verify URL: O'Reilly learning platform]

- **"Mathematics for Machine Learning" by Marc Peter Deisenroth, A. Aldo Faisal, and Cheng Soon Ong** (Cambridge University Press, 2020)
  Covers linear algebra, analytic geometry, matrix decompositions, probability, and optimization in the context of ML. Available free at [https://mml-book.github.io](https://mml-book.github.io). Companion to Module 02.

---

## Online Courses

- **fast.ai — Practical Deep Learning for Coders** ([https://course.fast.ai](https://course.fast.ai))
  Jeremy Howard's top-down approach to deep learning. Free. Companion to Modules 06–08. Uses PyTorch under the hood. Excellent for developing intuition before going deep on theory.

- **fast.ai — Practical Deep Learning Part 2** ([https://course.fast.ai/Lessons/part2.html](https://course.fast.ai/Lessons/part2.html))
  Goes deeper into building models from scratch. Companion to Module 06 (neural networks from scratch).

- **Stanford CS229 — Machine Learning** ([https://cs229.stanford.edu](https://cs229.stanford.edu))
  Andrew Ng's graduate ML course. Lecture notes are freely available and excellent for the mathematical foundations in Modules 02–05. Videos available on YouTube.

- **Stanford CS231n — Convolutional Neural Networks for Visual Recognition** ([http://cs231n.stanford.edu](http://cs231n.stanford.edu))
  The canonical CNNs course. Notes and assignments are freely available. Companion to Module 07.

- **Stanford CS224N — Natural Language Processing with Deep Learning** ([https://web.stanford.edu/class/cs224n](https://web.stanford.edu/class/cs224n))
  The leading NLP course. Companion to Module 08.

---

## Documentation and References

- **scikit-learn Documentation** ([https://scikit-learn.org/stable/](https://scikit-learn.org/stable/))
  The authoritative reference for all sklearn APIs. The User Guide sections on each algorithm are high-quality and include mathematical explanations. Essential companion for Modules 03–05.

- **PyTorch Documentation** ([https://pytorch.org/docs/stable/index.html](https://pytorch.org/docs/stable/index.html))
  Official PyTorch reference. The tutorials section ([https://pytorch.org/tutorials/](https://pytorch.org/tutorials/)) is particularly good for getting started with Modules 06–08.

- **HuggingFace Documentation** ([https://huggingface.co/docs](https://huggingface.co/docs))
  Covers the Transformers, Datasets, and Evaluate libraries. Essential for Module 08. The Model Hub ([https://huggingface.co/models](https://huggingface.co/models)) has thousands of pre-trained models.

- **MLflow Documentation** ([https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html))
  Covers experiment tracking, model registry, and serving. Companion to Module 09.

---

## Papers

These are landmark papers that established key concepts in this curriculum:

- **"Computing Machinery and Intelligence" (Turing, 1950)** — The Turing Test. Short and readable.
- **"Learning Representations by Back-propagating Errors" (Rumelhart, Hinton, Williams, 1986)** — Backpropagation. Companion to Module 06.
- **"ImageNet Classification with Deep Convolutional Neural Networks" (Krizhevsky, Sutskever, Hinton, 2012)** — AlexNet / the ImageNet moment. Companion to Module 07.
- **"Attention Is All You Need" (Vaswani et al., 2017)** — The Transformer architecture. Essential reading before Module 08. Available at [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762).
- **"BERT: Pre-training of Deep Bidirectional Transformers" (Devlin et al., 2018)** — Available at [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805).
- **"Language Models are Few-Shot Learners" (Brown et al., 2020)** — GPT-3 paper. Available at [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165). Companion to Module 10.
- **"A Unified Approach to Interpreting Model Predictions" (Lundberg & Lee, 2017)** — SHAP. Available at [https://arxiv.org/abs/1705.07874](https://arxiv.org/abs/1705.07874). Companion to Module 11.

---

## Tools and Libraries

| Tool | Purpose | Module |
|------|---------|--------|
| numpy | Numerical computing, array operations | 01, 02, 06 |
| pandas | Data manipulation and analysis | 01, 03, 05, 09 |
| matplotlib / seaborn | Data visualization | 01, 03, 04, 05 |
| scikit-learn | Classical ML algorithms, pipelines, evaluation | 03, 04, 05 |
| PyTorch | Deep learning framework | 06, 07, 08 |
| HuggingFace Transformers | Pre-trained NLP/vision models | 08, 10 |
| MLflow | Experiment tracking and model registry | 09 |
| FastAPI | Serving ML models as REST APIs | 09 |
| SHAP | Model explainability | 11 |
| LangChain | LLM application framework | 10 |

---

## Communities

- **Papers With Code** ([https://paperswithcode.com](https://paperswithcode.com)) — State-of-the-art benchmarks with linked code implementations
- **Kaggle** ([https://www.kaggle.com](https://www.kaggle.com)) — Competitions, notebooks, and datasets for practice
- **arXiv cs.LG / cs.CL / stat.ML** ([https://arxiv.org](https://arxiv.org)) — Preprint server for the latest ML research
- **Reddit r/MachineLearning** ([https://www.reddit.com/r/MachineLearning/](https://www.reddit.com/r/MachineLearning/)) — Research discussion community
