---
name: Generate Notebook
category: Interactive Content
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name
    example: calculus
  - name: MODULE_NUMBER
    description: The zero-padded module number this notebook corresponds to
    example: 04
  - name: NOTEBOOK_FOCUS
    description: What the notebook emphasizes — Visualization, Interactive, Proof, Algorithm, or Mixed
    example: Visualization
---

# Generate Notebook

## Description

Generates a complete Jupyter notebook for a specific module. The notebook provides an interactive, visual, and hands-on complement to the module's README.md — it does not duplicate the text, but brings the concepts to life with runnable code, visualizations, interactive exercises, and challenges. The notebook follows the leaps notebook template and is immediately runnable from top to bottom in a fresh kernel.

## Usage

1. Copy the prompt text below
2. Replace `[TOPIC_NAME]`, `[MODULE_NUMBER]`, and `[NOTEBOOK_FOCUS]` with your values
3. Paste into your AI assistant with access to this repository
4. The agent will create the notebook at `notebooks/[TOPIC_NAME]/[MODULE_NUMBER]_[slug].ipynb`

**NOTEBOOK_FOCUS values:**
- `Visualization` — heavy use of matplotlib/plotly/seaborn for visual intuition
- `Interactive` — heavy use of ipywidgets for interactive exploration
- `Proof` — step-by-step derivations with symbolic math (sympy)
- `Algorithm` — implementing and visualizing algorithms step by step
- `Mixed` — balanced across all types

## Prompt

```
You are a leaps notebook generation agent. Your task is to create a production-quality Jupyter notebook for a learning module.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- MODULE_NUMBER: [MODULE_NUMBER]
- NOTEBOOK_FOCUS: [NOTEBOOK_FOCUS]

## Step 1: Read the Module Content

Before writing any notebook content, read:

1. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/README.md` — all concepts, examples, and explanations
2. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/NOTES.md` — key points and concept map
3. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/EXERCISES.md` — to understand what practice looks like
4. `TEMPLATES/notebook/notebook_template.ipynb` — the structure you must follow
5. `environments/[TOPIC_NAME]/requirements.txt` — existing dependencies (add to, do not subtract from)

Check: does `notebooks/[TOPIC_NAME]/[MODULE_NUMBER]_[slug].ipynb` already exist? If yes, read it and note what it covers. Do not duplicate existing content — extend it.

## Step 2: Design the Notebook

Based on NOTEBOOK_FOCUS and the module content, design the notebook structure:

**For Visualization focus:**
- Primary tool: matplotlib, seaborn, or plotly (choose based on topic)
- Each major concept gets at least one visualization
- Visualizations should show behavior, not just data — animate if useful
- Use subplots to show contrasts (correct vs. incorrect, before vs. after, case A vs. case B)

**For Interactive focus:**
- Primary tool: ipywidgets
- Each key concept has a slider, dropdown, or toggle that lets the learner modify a parameter and observe the effect
- Interactive cells should have clear labels on all controls
- Include a "reset to defaults" mechanism for each interactive section

**For Proof focus:**
- Primary tool: sympy for symbolic computation
- Each proof step is a separate cell with the reasoning in Markdown before it
- Intermediate results are displayed explicitly, not hidden inside functions
- Numeric verification follows each symbolic proof

**For Algorithm focus:**
- Primary tool: core Python with matplotlib for visualization
- Implement the algorithm from scratch (not just call a library)
- Show each step of the algorithm with print statements or animated visualization
- Compare naive and optimized versions where applicable

**For Mixed:**
- Balance all types above. At least one visualization, one interactive element, one proof or derivation, and one algorithm implementation.

## Step 3: Plan the Cell Sequence

Write out the notebook plan as an ordered list of cells before generating the actual notebook JSON. Each cell in the plan should have:
- Cell type: Markdown (M) or Code (C)
- Title or purpose
- Estimated number of lines
- Dependencies from previous cells

This plan prevents orphaned variables, import errors, and logical gaps.

## Step 4: Generate the Notebook

Generate the complete notebook as valid `.ipynb` JSON. Every notebook must follow this structure:

### Cell 1: Title (Markdown)
```markdown
# [MODULE_NUMBER]. [Module Name] — Interactive Notebook
**Topic:** [TOPIC_NAME] | **Focus:** [NOTEBOOK_FOCUS] | **Generated:** [DATE]

> This notebook is an interactive companion to [Module README link].
> It brings the module's concepts to life through visualization and hands-on code.
> Run cells in order from top to bottom. Do not skip cells.
```

### Cell 2: Setup (Code)
ALL imports and configuration go in this single cell. This cell must:
- Import every library used in the notebook
- Set plotting style and figure size defaults
- Set random seeds
- Define any helper functions used throughout (small utilities only)
- Print the Python version and key package versions for reproducibility

```python
# ============================================================
# Setup — run this cell first, before any other cell
# ============================================================

import sys
import numpy as np
import matplotlib.pyplot as plt
# ... all other imports

# Reproducibility
np.random.seed(42)
import random; random.seed(42)

# Plotting defaults
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Version check
print(f"Python {sys.version}")
print(f"NumPy {np.__version__}")
# ... other versions

print("Setup complete.")
```

### Cell 3: Learning Objectives (Markdown)
```markdown
## Learning Objectives

By the end of this notebook, you will have:

1. [Concrete, hands-on objective — what you will have built or seen]
2. [...]
3. [...]

**Prerequisites:** [What you need to know before running this notebook]
```

### Cells 4–N: Content Sections

Organize into major sections matching the module's core concepts. For each concept:

**Markdown cell (explanation):**
- H2 heading with the concept name
- 2–4 sentence explanation of what this section demonstrates
- What to look for in the output

**Code cell (demonstration):**
- Well-commented code
- Output that is immediately interpretable
- A `# Why this matters:` comment at key lines

**Markdown cell (analysis):**
- What the output shows
- What to try changing and why

**Interactive/Visualization cell (if applicable):**
- For NOTEBOOK_FOCUS=Interactive: ipywidgets
- For NOTEBOOK_FOCUS=Visualization: formatted plots with titles, axis labels, legends

### Penultimate Section: Exercises

Create 3–4 scaffolded exercises. Each exercise has:
- A Markdown cell describing the task
- A Code cell with starter code (function signature, input/output specification, hints in comments)
- A blank Code cell for the learner's solution
- A hidden solution in a Code cell that starts with `# SOLUTION — uncomment to see` and has all code commented out

Format:
```python
# Exercise [N]: [Title]
# 
# Task: [Clear description of what to implement]
# 
# Input: [description]
# Output: [description]
# 
# Hint: [Optional hint]

def exercise_N(param):
    # Your code here
    pass

# Test your implementation:
# result = exercise_N(test_input)
# print(result)  # Expected: [expected output]
```

### Final Section: Challenges (unscaffolded)

2–3 open challenges with minimal scaffolding:
- No starter code
- A clear problem statement
- Expected behavior described, not required signature

```python
# Challenge [N]: [Title]
#
# [Problem statement]
#
# Expected behavior: [what a correct solution does]
# Difficulty: [Beginner | Intermediate | Advanced]
```

### Last Cell: Summary and Next Steps (Markdown)
```markdown
## Summary

In this notebook you:

- [What was built/shown]
- [What was interactive]
- [Key insight from the visualizations]

## Next Steps

- **Continue:** Read the next section in the [module README link]
- **Practice:** Complete the [EXERCISES.md link] for this module
- **Test yourself:** Take the [TEST.md link] for this module
- **Next module:** [[TOPIC_NAME/module-NN-name]] covers [what comes next]

## References

- [Module README](../../TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/README.md)
- [Resource from RESOURCES.md]
- [Another relevant resource]
```

## Step 5: Verify Notebook Quality

Before finalizing, check:

1. **Imports:** Every library used is imported in Cell 2. No library is imported inside a later cell.
2. **Variables:** No cell uses a variable defined in a later cell (no forward references).
3. **Outputs:** Every code cell that produces output has that output described in the surrounding Markdown.
4. **Visualizations:** Every plot has a title, axis labels, and a legend (if multiple series). Every plot has a clear caption in the Markdown below.
5. **Exercises:** Each exercise has a clear task, starter code, and a commented-out solution.
6. **Clean outputs:** The notebook is written with empty outputs (the learner will produce outputs by running it).
7. **Reproducibility:** With the setup cell run first, every subsequent cell will produce the same output on any machine with the required packages.

## Step 6: Create or Update the Environment File

If `environments/[TOPIC_NAME]/requirements.txt` does not exist, create it. If it exists, add any new packages required by this notebook that are not already listed:

```
numpy>=1.24.0
matplotlib>=3.7.0
ipywidgets>=8.0.0
# ... other requirements
```

Pin to minimum versions that are known to work, not exact versions — this allows compatibility with newer versions while preventing breakage from very old ones.

## Step 7: Update Cross-References

1. Add a link to the notebook in the module's README.md:
   ```markdown
   > [!TIP]
   > An interactive notebook for this module is available at
   > [`notebooks/[TOPIC_NAME]/[MODULE_NUMBER]_[slug].ipynb`](../../../notebooks/[TOPIC_NAME]/[MODULE_NUMBER]_[slug].ipynb).
   ```

2. Add the notebook to `TOPICS/[TOPIC_NAME]/README.md` in the module list table (as a link in the module row).

## Output Format

1. **Notebook Design Plan** — the cell sequence from Step 3
2. **Environment Requirements** — new packages needed
3. **The notebook JSON** — complete, valid `.ipynb` file content
4. **Cross-reference updates** — which README files were updated

Output the notebook as a code block containing valid JSON so it can be copied directly to the target file path.
```

## Examples

**Visualize calculus derivatives:**
```
TOPIC_NAME: calculus
MODULE_NUMBER: 03
NOTEBOOK_FOCUS: Visualization
```
Output: Notebook with plots of functions and their derivatives, animated limit definition, interactive tangent line explorer.

**Interactive Rust ownership explorer:**
```
TOPIC_NAME: rust
MODULE_NUMBER: 03
NOTEBOOK_FOCUS: Interactive
```
Output: Notebook with interactive ownership state diagrams, borrowing rule visualizer (using Python to model Rust's rules symbolically).

**Algorithm: sorting implementations:**
```
TOPIC_NAME: algorithms
MODULE_NUMBER: 02
NOTEBOOK_FOCUS: Algorithm
```
Output: Notebook with step-by-step implementations of sorting algorithms, animated comparison, complexity visualization.

## Notes

- For topics like Rust, Go, or C that cannot run natively in Python notebooks: the notebook models and visualizes the concepts using Python analogies, not the actual language. This is valid and useful — it separates the concept from the syntax.
- For mathematics-heavy topics: use sympy for symbolic computation and matplotlib for plots. Avoid large numeric computations that would take more than 30 seconds.
- ipywidgets requires the `ipywidgets` package and Jupyter to be configured properly. Include setup instructions in the notebook's first Markdown cell.
- Keep cell outputs cleared before committing — generated outputs can be very large and clutter diffs. The CI linter enforces this.
- Notebooks that require more than 5 minutes to run from top to bottom should include a `# Approximate runtime: N minutes` comment in the setup cell and a warning in the first Markdown cell.
