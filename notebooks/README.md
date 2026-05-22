# Notebooks

Cross-topic and methodology notebooks for the **leaps** knowledge base. These notebooks are not tied to any single topic — they exist at the repository level to support learning strategy, mathematical foundations, and algorithmic understanding that spans multiple subjects.

---

## Purpose

Topic-specific notebooks (e.g., a Python notebook walking through decorators) live inside their topic directory at `TOPICS/<topic>/notebooks/`. The notebooks here are different: they teach you *how to use leaps* effectively, provide shared mathematical or computational foundations referenced by many topics, and demonstrate algorithms that appear repeatedly across the curriculum.

Think of this directory as the **meta-layer of learning content**: everything here makes every other topic easier.

---

## Notebooks in This Directory

| Notebook | Description | Topics Referenced |
|---|---|---|
| [`learning_methodology.ipynb`](./learning_methodology.ipynb) | The science of learning: spaced repetition, active recall, interleaving. Includes forgetting curve visualization and SRS interval calculator. | All topics |

### Planned Notebooks

The following notebooks are placeholders for future content. Contributions welcome.

| Notebook | Description |
|---|---|
| `math_foundations.ipynb` | Linear algebra, probability, and calculus refresher with NumPy. Referenced by machine-learning, data-science, and cryptography topics. |
| `algorithm_visualization.ipynb` | Interactive visualizations of sorting, searching, graph traversal, and dynamic programming algorithms. |
| `complexity_analysis.ipynb` | Big-O analysis with empirical timing experiments. Companion to the algorithms and data-structures topics. |
| `regex_playground.ipynb` | Interactive regular expression sandbox with step-by-step explanations. Referenced by most programming language topics. |
| `unicode_and_encoding.ipynb` | UTF-8, Unicode, base64, and binary encoding. Foundational for networking, cryptography, and systems topics. |
| `statistics_for_programmers.ipynb` | Descriptive statistics, distributions, hypothesis testing, and p-values with real code. |

---

## How These Differ from Topic Notebooks

| Dimension | Topic Notebooks (`TOPICS/<topic>/notebooks/`) | Repository Notebooks (here) |
|---|---|---|
| **Scope** | Specific to one topic (e.g., Python async patterns) | Cross-cutting (applies to many topics) |
| **Audience** | Learner progressing through that topic | Any leaps user, regardless of topic |
| **When to use** | During structured study of the topic | Before starting a topic, or as a reference |
| **Dependencies** | May require topic-specific packages | Only core scientific stack (numpy, matplotlib, etc.) |
| **Maintenance** | Updated as topic content grows | Updated as new cross-topic needs emerge |

---

## Running the Notebooks

All notebooks in this directory depend only on the base leaps environment. Any setup approach from [`environments/README.md`](../environments/README.md) works:

```bash
# Option 1: venv
python -m venv .venv && source .venv/bin/activate
pip install jupyter numpy scipy matplotlib sympy pandas ipywidgets
jupyter lab notebooks/

# Option 2: Docker (from repo root)
docker compose -f environments/docker/docker-compose.yml up
# Open http://localhost:8888 → navigate to notebooks/

# Option 3: Devcontainer
# Reopen in Container → all packages pre-installed
```

---

## Contributing a Cross-Topic Notebook

If you build a notebook that teaches a concept referenced by three or more topics, consider moving it here rather than inside a single topic directory.

Guidelines:
1. The notebook must be self-contained — no imports outside the base environment.
2. Add an entry to the table above in this README.
3. Follow the cell structure used in `learning_methodology.ipynb`: title cell, explanation cells, code cells, summary cell.
4. Use `matplotlib` inline output (not interactive widgets) for any plots that need to render in static previews.
5. Clear all cell outputs before committing (`Kernel → Restart & Clear Output`).

---

## Related Directories

- [`TOPICS/`](../TOPICS/) — Topic-specific content including topic-level notebooks.
- [`environments/`](../environments/) — Setup guides for running notebooks.
- [`SHARED/concepts/`](../SHARED/concepts/) — Concept files that cross-reference these notebooks.
