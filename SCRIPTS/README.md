# LEAPS Scripts

> Automation scripts for the **L**earning **E**nvironment for **A**ny **P**rogressive **S**ubject knowledge base.

All scripts are written in Python 3.10+ and use only the standard library plus common packages (`pathlib`, `re`, `json`, `argparse`, `datetime`). Run any script with `--help` for full usage details.

---

## Quick Start

```bash
# Make all scripts executable (run once)
chmod +x SCRIPTS/*.py

# Create a new topic
python SCRIPTS/new_topic.py rust --description "Systems programming language" --difficulty intermediate

# Validate the repository structure
python SCRIPTS/validate_structure.py

# Generate a progress report
python SCRIPTS/progress_report.py

# Update the global topic index
python SCRIPTS/update_index.py

# Generate table of contents in a file
python SCRIPTS/generate_toc.py TOPICS/python/README.md

# Find broken internal links
python SCRIPTS/find_broken_links.py

# Build the knowledge graph
python SCRIPTS/knowledge_graph.py --format markdown

# Export learning statistics
python SCRIPTS/export_stats.py

# Set up spaced repetition schedule
python SCRIPTS/spaced_repetition.py

# Set up the learning environment
python SCRIPTS/setup_environment.py

# Validate Jupyter notebooks
python SCRIPTS/validate_notebooks.py
```

---

## Script Index

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| [`new_topic.py`](#new_topicpy) | Scaffold a new topic directory from templates | `--description`, `--difficulty`, `--modules`, `--dry-run` |
| [`progress_report.py`](#progress_reportpy) | Generate a progress report across all topics | `--json`, `--topic` |
| [`validate_structure.py`](#validate_structurepy) | Validate repository structure against conventions | `--fix`, `--topic`, exits 1 on violations |
| [`generate_toc.py`](#generate_tocpy) | Insert/update Table of Contents in markdown files | `--dry-run`, `--dir` |
| [`find_broken_links.py`](#find_broken_linkspy) | Find broken internal links and wiki-links | `--fix`, exits 1 on broken links |
| [`knowledge_graph.py`](#knowledge_graphpy) | Build a knowledge graph from wiki-links | `--format json\|dot\|markdown`, `--output` |
| [`update_index.py`](#update_indexpy) | Regenerate `TOPICS/README.md` index | `--preview` |
| [`export_stats.py`](#export_statspy) | Export aggregated learning statistics | `--output`, `--format json\|markdown` |
| [`validate_notebooks.py`](#validate_notebookspy) | Validate Jupyter `.ipynb` files | `--clear-output`, exits 1 on violations |
| [`spaced_repetition.py`](#spaced_repetitionpy) | Generate SM-2 spaced repetition study schedule | `--topic`, `--days` |
| [`setup_environment.py`](#setup_environmentpy) | Bootstrap the learning environment | `--check-only` |

---

## Detailed Reference

### `new_topic.py`

Creates a complete topic directory structure under `TOPICS/{topic_name}/` using templates from `TEMPLATES/`.

```
usage: new_topic.py [-h] [--description DESC] [--difficulty {beginner,intermediate,advanced,expert}]
                    [--modules N] [--dry-run] [--prerequisites PREREQS]
                    topic_name
```

**Arguments:**

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `topic_name` | positional | — | Topic slug (e.g. `rust`, `linear-algebra`) |
| `--description` | str | `""` | One-line description of the topic |
| `--difficulty` | choice | `beginner` | Difficulty level |
| `--modules` | int | `8` | Number of modules to scaffold (0–Introduction + N modules) |
| `--prerequisites` | str | `""` | Comma-separated prerequisite topic slugs |
| `--dry-run` | flag | false | Print what would be created without writing |

**Example:**

```bash
python SCRIPTS/new_topic.py calculus \
  --description "Differential and integral calculus" \
  --difficulty intermediate \
  --modules 10 \
  --prerequisites "algebra,trigonometry"
```

**What it creates:**

```
TOPICS/calculus/
├── README.md
├── ROADMAP.md
├── RESOURCES.md
├── GLOSSARY.md
├── QUESTIONS.md
├── PROJECTS.md
└── modules/
    ├── 00_introduction/
    │   ├── README.md, NOTES.md, QUESTIONS.md
    │   ├── EXERCISES.md, TEST.md, ANSWERS.md, RESOURCES.md
    ├── 01_basics/
    │   └── (same files)
    └── ... (up to N modules)
```

---

### `progress_report.py`

Scans all topics, reads their `README.md` files for `- [x]` / `- [ ]` checklists and test score tables, and prints a formatted terminal report.

```
usage: progress_report.py [-h] [--json] [--topic TOPIC]
```

**Arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--json` | false | Output raw JSON instead of pretty terminal report |
| `--topic` | all | Show detailed report for one topic only |

**Example output:**

```
LEAPS Progress Report — 2026-05-22
═══════════════════════════════════

  Topic            Modules     Completion   Avg Score
  ─────────────────────────────────────────────────
  python           3/14        21%          82%
  rust             0/8          0%          —

  ─────────────────────────────────────────────────
  Global           3/22        14%

  Recent activity:
    • TOPICS/python/modules/03_control_flow/NOTES.md (2 days ago)
```

---

### `validate_structure.py`

Validates every topic and module against the repository conventions. Exits with code `1` if any violations are found (safe to use in CI).

```
usage: validate_structure.py [-h] [--fix] [--topic TOPIC]
```

**What it checks:**

- Every topic has: `README.md`, `ROADMAP.md`, `RESOURCES.md`, `GLOSSARY.md`, `QUESTIONS.md`, `PROJECTS.md`
- Every module has: `README.md`, `NOTES.md`, `QUESTIONS.md`, `EXERCISES.md`, `TEST.md`, `ANSWERS.md`, `RESOURCES.md`
- Module directory names match `NN_slug` pattern
- Markdown H1 appears exactly once per file
- Code blocks have language annotations (`` ```python ``, not bare ` ``` `)
- Wiki-links `[[topic]]` resolve to existing directories

**Example output:**

```
Validating TOPICS/python/...
  [WARN] TOPICS/python/modules/03_control_flow/TEST.md:42 — code block missing language annotation
  [ERROR] TOPICS/python/README.md: missing required file GLOSSARY.md

2 violations found (1 error, 1 warning).
Exit code: 1
```

---

### `generate_toc.py`

Inserts or updates a Table of Contents in a markdown file between `<!-- TOC -->` and `<!-- /TOC -->` markers. Generates GitHub-compatible anchor links.

```
usage: generate_toc.py [-h] [--dry-run] [--dir DIR] [file]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `file` | Single markdown file to process |
| `--dry-run` | Print the TOC without writing |
| `--dir DIR` | Recursively process all `.md` files in directory |

**Markers in your file:**

```markdown
# My Topic

<!-- TOC -->
<!-- /TOC -->

## Section 1
...
```

Files containing `<!-- NO-TOC -->` are skipped.

---

### `find_broken_links.py`

Scans all markdown files for `[text](path)` and `[[wiki-link]]` references, resolves relative paths, and reports any that don't resolve to an existing file or directory.

```
usage: find_broken_links.py [-h] [--fix] [--dir DIR]
```

**Example output:**

```
TOPICS/python/README.md:45 — broken: [[memory-management]] (no TOPICS/memory-management/ found)
TOPICS/rust/modules/02_ownership/README.md:12 — broken: [notes](../NOTES.md) (file not found)

2 broken links found.
```

---

### `knowledge_graph.py`

Builds a directed knowledge graph by scanning all wiki-links (`[[topic]]`, `[[topic/module]]`) across the repository.

```
usage: knowledge_graph.py [-h] [--format {json,dot,markdown}] [--output FILE]
```

**Output formats:**

- `markdown` — Human-readable summary with hub topics, orphans, most-connected nodes
- `json` — Machine-readable `{nodes: [...], edges: [...]}` for web visualization
- `dot` — Graphviz DOT format; render with `dot -Tsvg graph.dot -o graph.svg`

---

### `update_index.py`

Regenerates `TOPICS/README.md` with an alphabetical table of all topics, auto-detected category groupings, and summary statistics.

```
usage: update_index.py [-h] [--preview]
```

---

### `export_stats.py`

Aggregates learning statistics across all topics and exports them.

```
usage: export_stats.py [-h] [--output FILE] [--format {json,markdown}]
```

**Exported data:**

- Modules created vs. completed
- Test scores per topic/module
- Points earned
- Questions logged
- Global completion percentage
- Strong/weak area identification
- Review recommendations

---

### `validate_notebooks.py`

Validates all `.ipynb` Jupyter notebooks in the repository.

```
usage: validate_notebooks.py [-h] [--clear-output] [--dir DIR]
```

**Checks:**

- Valid JSON structure
- Has title markdown cell and objectives cell
- No stale execution counts (warns)
- All cells have source content
- Complete metadata

---

### `spaced_repetition.py`

Reads test scores and completion dates from all topics and generates an SM-2-inspired review schedule.

```
usage: spaced_repetition.py [-h] [--topic TOPIC] [--days N]
```

**Interval rules:**

| Score | Review in |
|-------|-----------|
| ≥ 80% | 7 days |
| 60–79% | 3 days |
| < 60% | 1 day |
| Not attempted | 1 day after first study |

---

### `setup_environment.py`

Bootstraps the LEAPS environment: checks Python version, required tools, creates directory structure, and sets up git hooks.

```
usage: setup_environment.py [-h] [--check-only]
```

---

## Exit Codes

Scripts that perform validation return meaningful exit codes for CI integration:

| Code | Meaning |
|------|---------|
| `0` | Success / no violations |
| `1` | Validation errors found |
| `2` | Argument / usage error |

---

## Adding New Scripts

1. Place the script in `SCRIPTS/`
2. Add the shebang: `#!/usr/bin/env python3`
3. Add a module docstring
4. Use `argparse` for all arguments
5. Update this README's table and add a section below

---

*Generated by LEAPS tooling. Keep this file up to date when adding scripts.*
