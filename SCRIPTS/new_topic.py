#!/usr/bin/env python3
"""
new_topic.py - Create a new learning topic directory structure from templates.

Usage:
    python new_topic.py <topic_name> [options]

Examples:
    python new_topic.py rust --description "Systems programming language" --difficulty intermediate
    python new_topic.py calculus --modules 12 --dry-run
    python new_topic.py linear-algebra --prerequisites "algebra,trigonometry" --difficulty advanced
"""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"
TEMPLATES_DIR = REPO_ROOT / "TEMPLATES"

VALID_DIFFICULTIES = ("beginner", "intermediate", "advanced", "expert")

# Files required at the topic level
TOPIC_LEVEL_FILES = [
    "README.md",
    "ROADMAP.md",
    "RESOURCES.md",
    "GLOSSARY.md",
    "QUESTIONS.md",
    "PROJECTS.md",
]

# Files required in every module directory
MODULE_FILES = [
    "README.md",
    "NOTES.md",
    "QUESTIONS.md",
    "EXERCISES.md",
    "TEST.md",
    "ANSWERS.md",
    "RESOURCES.md",
]

# Default module names for the numbered modules (after introduction)
DEFAULT_MODULE_NAMES = [
    "Basics",
    "Core Concepts",
    "Intermediate Techniques",
    "Applied Skills",
    "Advanced Patterns",
    "Deep Dive",
    "Expert Topics",
    "Capstone Review",
    "Extended Practice",
    "Mastery",
    "Research Topics",
    "Final Synthesis",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


class TopicConfig(NamedTuple):
    """All configuration values for a new topic."""

    name: str               # slug, e.g. "linear-algebra"
    display_name: str       # human-readable, e.g. "Linear Algebra"
    description: str
    difficulty: str
    num_modules: int        # number of modules *after* the Introduction
    prerequisites: list[str]
    today: str              # ISO date string


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="new_topic.py",
        description="Scaffold a new LEAPS topic directory structure from templates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "topic_name",
        help=(
            "Topic slug. Use lowercase letters, digits, and hyphens "
            "(e.g. 'rust', 'linear-algebra', 'machine-learning')."
        ),
    )
    parser.add_argument(
        "--description",
        default="",
        metavar="DESC",
        help="One-line description of the topic.",
    )
    parser.add_argument(
        "--difficulty",
        choices=VALID_DIFFICULTIES,
        default="beginner",
        help="Overall difficulty level (default: beginner).",
    )
    parser.add_argument(
        "--modules",
        type=int,
        default=8,
        metavar="N",
        help=(
            "Number of numbered modules to create after the Introduction "
            "(default: 8). Total directories = N + 1."
        ),
    )
    parser.add_argument(
        "--prerequisites",
        default="",
        metavar="PREREQS",
        help="Comma-separated list of prerequisite topic slugs (e.g. 'algebra,calculus').",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without writing anything to disk.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_topic_name(name: str) -> str:
    """Return a normalised slug or raise ValueError."""
    normalised = name.strip().lower()
    if not normalised:
        raise ValueError("Topic name cannot be empty.")
    if not re.fullmatch(r"[a-z0-9][a-z0-9\-]*", normalised):
        raise ValueError(
            f"Invalid topic name '{name}'. "
            "Use only lowercase letters, digits, and hyphens, "
            "starting with a letter or digit."
        )
    if len(normalised) > 64:
        raise ValueError(f"Topic name too long ({len(normalised)} chars, max 64).")
    return normalised


def validate_modules(n: int) -> int:
    if n < 0:
        raise ValueError("--modules must be >= 0.")
    if n > 50:
        raise ValueError("--modules must be <= 50 (sanity limit).")
    return n


# ---------------------------------------------------------------------------
# Display-name helpers
# ---------------------------------------------------------------------------


def slug_to_display_name(slug: str) -> str:
    """Convert a slug like 'linear-algebra' to 'Linear Algebra'."""
    return " ".join(word.capitalize() for word in slug.split("-"))


def module_dir_name(index: int, label: str) -> str:
    """Return zero-padded module directory name, e.g. '00_introduction'."""
    return f"{index:02d}_{label.lower().replace(' ', '_')}"


def module_display_name(index: int, label: str) -> str:
    """Return human-readable module name, e.g. 'Module 00: Introduction'."""
    return f"Module {index:02d}: {label}"


# ---------------------------------------------------------------------------
# Template rendering
# ---------------------------------------------------------------------------


def make_placeholders(cfg: TopicConfig, module_names: list[str]) -> dict[str, str]:
    """Build a dict mapping every {{PLACEHOLDER}} to its replacement value."""
    prereq_links = "\n".join(
        f"- [[{p}]] — _(describe what you need from this topic)_"
        for p in cfg.prerequisites
    ) or "- _(none required)_"

    # Build module table rows for the topic README
    module_rows = []
    for i, name in enumerate(module_names):
        dir_name = module_dir_name(i, name)
        module_rows.append(
            f"| {i:02d} | [{name}](./modules/{dir_name}/) | — | - [ ] | —/— |"
        )
    module_table = "\n".join(module_rows)

    # Mermaid flowchart module nodes for ROADMAP
    mermaid_nodes = "\n    ".join(
        f"M{i:02d}[{module_display_name(i, name)}]" for i, name in enumerate(module_names)
    )

    hours_map = {"beginner": "40", "intermediate": "60", "advanced": "80", "expert": "120"}
    pace_map = {"beginner": "2–3 hrs/week", "intermediate": "3–4 hrs/week",
                "advanced": "4–5 hrs/week", "expert": "5+ hrs/week"}

    return {
        "{{TOPIC_NAME}}": cfg.display_name,
        "{{TOPIC_SLUG}}": cfg.name,
        "{{ONE_LINE_DESCRIPTION}}": cfg.description or f"A structured learning path for {cfg.display_name}.",
        "{{TOPIC_DESCRIPTION}}": cfg.description or f"A structured learning path for {cfg.display_name}.",
        "{{DIFFICULTY}}": cfg.difficulty.capitalize(),
        "{{YYYY-MM-DD}}": cfg.today,
        "{{YYYY--MM--DD}}": cfg.today,
        "{{DATE}}": cfg.today,
        "{{HOURS}}": hours_map.get(cfg.difficulty, "60"),
        "{{PACE}}": pace_map.get(cfg.difficulty, "3 hrs/week"),
        "{{PREREQUISITES}}": ", ".join(cfg.prerequisites) if cfg.prerequisites else "None",
        "{{PREREQ_LINKS}}": prereq_links,
        "{{TOTAL_MODULES}}": str(len(module_names)),
        "{{MODULE_TABLE}}": module_table,
        # Single placeholder values for template loops
        "{{PREREQ_TOPIC_1}}": cfg.prerequisites[0] if len(cfg.prerequisites) > 0 else "none",
        "{{PREREQ_TOPIC_2}}": cfg.prerequisites[1] if len(cfg.prerequisites) > 1 else "none",
        "{{PREREQ_TOPIC_3}}": cfg.prerequisites[2] if len(cfg.prerequisites) > 2 else "none",
        "{{WHAT_YOU_NEED_FROM_IT}}": "_(describe what you need from this topic)_",
        "{{WHY_IT_MATTERS}}": f"_{cfg.display_name} is important because..._ (fill in after studying)",
        "{{FEATURE_1}}": "Core Concepts",
        "{{FEATURE_1_DESCRIPTION}}": "Fundamental building blocks",
        "{{FEATURE_2}}": "Practical Application",
        "{{FEATURE_2_DESCRIPTION}}": "Real-world usage patterns",
        "{{FEATURE_3}}": "Advanced Techniques",
        "{{FEATURE_3_DESCRIPTION}}": "Expert-level skills and patterns",
        "{{CREATOR}}": "_(research and fill in)_",
        "{{YEAR_CREATED}}": "_(research and fill in)_",
        "{{HISTORICAL_SUMMARY}}": "_(add historical context after researching the topic)_",
        "{{YEAR_1}}": "YYYY", "{{EVENT_1}}": "_(event)_",
        "{{YEAR_2}}": "YYYY", "{{EVENT_2}}": "_(event)_",
        "{{YEAR_3}}": "YYYY", "{{EVENT_3}}": "_(event)_",
        "{{YEAR_4}}": "YYYY", "{{EVENT_4}}": "_(event)_",
        "{{DOMAIN_1}}": "Industry", "{{APPLICATION_1}}": "_(describe)_",
        "{{DOMAIN_2}}": "Research", "{{APPLICATION_2}}": "_(describe)_",
        "{{DOMAIN_3}}": "Education", "{{APPLICATION_3}}": "_(describe)_",
        "{{DOMAIN_4}}": "Engineering", "{{APPLICATION_4}}": "_(describe)_",
        "{{DOMAIN_5}}": "Open Source", "{{APPLICATION_5}}": "_(describe)_",
        "{{OBJECTIVE_1}}": "Understand the core concepts and vocabulary",
        "{{OBJECTIVE_2}}": "Apply basic techniques to solve problems",
        "{{OBJECTIVE_3}}": "Build progressively more complex projects",
        "{{OBJECTIVE_4}}": "Read and understand existing code/works in this area",
        "{{OBJECTIVE_5}}": "Identify and diagnose common mistakes",
        "{{OBJECTIVE_6}}": "Connect this topic to related areas",
        "{{TYPE}}": "Mixed",
        "{{TEST_POINTS_POSSIBLE}}": str(len(module_names) * 30),
        "{{EXERCISE_POINTS_POSSIBLE}}": str(len(module_names) * 10),
        "{{PROJECT_POINTS_POSSIBLE}}": str(len(module_names) * 15),
        "{{TOTAL_POINTS_POSSIBLE}}": str(len(module_names) * 55),
        "{{CUSTOM_MILESTONE_1}}": "Expert Achievement",
        "{{CUSTOM_MILESTONE_1_DESCRIPTION}}": "Achieve ≥ 95% average across all module tests",
        "{{RELATED_TOPIC_1}}": "_(related-topic)_",
        "{{RELATIONSHIP_1}}": "_(describe the relationship)_",
        "{{RELATED_TOPIC_2}}": "_(related-topic)_",
        "{{RELATIONSHIP_2}}": "_(describe the relationship)_",
        "{{RELATED_TOPIC_3}}": "_(related-topic)_",
        "{{RELATIONSHIP_3}}": "_(describe the relationship)_",
        # ROADMAP placeholders
        "{{MODULE_01_NAME}}": module_names[1] if len(module_names) > 1 else "Basics",
        "{{MODULE_02_NAME}}": module_names[2] if len(module_names) > 2 else "Core Concepts",
        "{{MODULE_03_NAME}}": module_names[3] if len(module_names) > 3 else "Intermediate",
        "{{MODULE_04_NAME}}": module_names[4] if len(module_names) > 4 else "Applied Skills",
        "{{MODULE_05_NAME}}": module_names[5] if len(module_names) > 5 else "Advanced",
        "{{MODULE_06_NAME}}": module_names[6] if len(module_names) > 6 else "Deep Dive",
        "{{MODULE_07_NAME}}": module_names[7] if len(module_names) > 7 else "Expert",
        "{{MODULE_08_NAME}}": module_names[8] if len(module_names) > 8 else "Capstone",
        "{{MODULE_01_SLUG}}": module_names[1].lower().replace(" ", "-") if len(module_names) > 1 else "basics",
        "{{MODULE_02_SLUG}}": module_names[2].lower().replace(" ", "-") if len(module_names) > 2 else "core-concepts",
        "{{MODULE_03_SLUG}}": module_names[3].lower().replace(" ", "-") if len(module_names) > 3 else "intermediate",
        "{{MODULE_04_SLUG}}": module_names[4].lower().replace(" ", "-") if len(module_names) > 4 else "applied",
        "{{MODULE_05_SLUG}}": module_names[5].lower().replace(" ", "-") if len(module_names) > 5 else "advanced",
        "{{MODULE_06_SLUG}}": module_names[6].lower().replace(" ", "-") if len(module_names) > 6 else "deep-dive",
        "{{MODULE_07_SLUG}}": module_names[7].lower().replace(" ", "-") if len(module_names) > 7 else "expert",
        "{{MODULE_08_SLUG}}": module_names[8].lower().replace(" ", "-") if len(module_names) > 8 else "capstone",
        "{{MODULE_01_TOPIC}}": "Foundations",
        "{{MODULE_02_TOPIC}}": "Core Patterns",
        "{{MODULE_03_TOPIC}}": "Practical Usage",
        "{{MODULE_04_TOPIC}}": "Applied Problems",
        "{{MODULE_05_TOPIC}}": "Advanced Concepts",
        "{{MODULE_06_TOPIC}}": "Deep Understanding",
        "{{MODULE_07_TOPIC}}": "Expert Skills",
        "{{MODULE_08_TOPIC}}": "Synthesis",
        "{{H_00}}": "4", "{{H_01}}": "6", "{{H_02}}": "6",
        "{{H_03}}": "8", "{{H_04}}": "8", "{{H_05}}": "8",
        "{{H_06}}": "10", "{{H_07}}": "10", "{{H_08}}": "10",
        "{{H_CAPSTONE}}": "12", "{{H_REVIEW}}": "4", "{{H_TEACH}}": "4",
        "{{SKILL_01}}": "Core vocabulary and mental models",
        "{{SKILL_02}}": "Foundational techniques",
        "{{SKILL_03}}": "Pattern recognition",
        "{{SKILL_04}}": "Practical problem solving",
        "{{SKILL_05}}": "Idiomatic usage",
        "{{SKILL_06}}": "Advanced patterns",
        "{{SKILL_07}}": "Performance and internals",
        "{{SKILL_08}}": "Synthesis and cross-domain thinking",
        "{{CORE_SKILL_1}}": "the core patterns of this topic",
        "{{CORE_SKILL_2}}": "practical application in real projects",
        "{{P1_HOURS}}": "16", "{{P2_HOURS}}": "24",
        "{{P3_HOURS}}": "30", "{{P4_HOURS}}": "20",
        "{{P1_P2_HOURS}}": "40", "{{P1_P2_P3_HOURS}}": "70",
        "{{TOTAL_HOURS}}": hours_map.get(cfg.difficulty, "60"),
        "{{HOURS_PER_WEEK}}": "5",
        "{{FAST_TRACK_START}}": "02",
        "{{SUPPLEMENTARY_BOOK_1}}": "_(recommended book)_",
        "{{SUPPLEMENTARY_COURSE}}": "_(recommended course)_",
        "{{CUSTOM_MILESTONE}}": "Personal Goal",
        "{{CUSTOM_CRITERIA}}": "Set your own milestone here",
        "{{TAG_1}}": cfg.difficulty,
        "{{TAG_2}}": cfg.name,
    }


def render_template(template_text: str, placeholders: dict[str, str]) -> str:
    """Replace all {{PLACEHOLDER}} tokens in template_text."""
    result = template_text
    for placeholder, value in placeholders.items():
        result = result.replace(placeholder, value)
    return result


# ---------------------------------------------------------------------------
# Content generators (for files not in TEMPLATES/)
# ---------------------------------------------------------------------------


def make_glossary_content(display_name: str, today: str) -> str:
    return f"""# {display_name} — Glossary

> Add definitions here as you encounter new terms. Keep them concise and precise.
> Cross-reference related terms with [[wiki-links]] where helpful.

---

_Last updated: {today}_

---

## A

_(no entries yet)_

## B

_(no entries yet)_

---

_Add terms alphabetically as you study. Precision matters more than length._
"""


def make_questions_content(display_name: str, today: str) -> str:
    return f"""# {display_name} — Open Questions

> Log big-picture questions here — questions that span multiple modules or that
> you haven't answered yet. AI agents will append answers below each question.
> **Never delete questions** — they are part of your learning history.

---

_Last updated: {today}_

---

## Unanswered Questions

### Q1 — {today}

> _(Write your first question here after reading the topic overview.)_

**Status:** Open

---

_Add new questions above this line, newest last._
"""


def make_resources_content(display_name: str, today: str) -> str:
    return f"""# {display_name} — Resources

> A curated list of books, courses, videos, papers, and tools for this topic.
> Add resources as you discover them. Rate them after using them.

---

_Last updated: {today}_

---

## Books

| Title | Author | Level | Rating | Notes |
|-------|--------|-------|--------|-------|
| _(add books)_ | — | — | —/5 | — |

## Online Courses

| Course | Platform | Level | Rating | URL |
|--------|----------|-------|--------|-----|
| _(add courses)_ | — | — | —/5 | — |

## Videos & Talks

| Title | Speaker/Channel | Length | Rating | URL |
|-------|-----------------|--------|--------|-----|
| _(add videos)_ | — | — | —/5 | — |

## Papers & Articles

| Title | Author(s) | Year | Notes | URL |
|-------|-----------|------|-------|-----|
| _(add papers)_ | — | — | — | — |

## Tools & Software

| Tool | Purpose | URL |
|------|---------|-----|
| _(add tools)_ | — | — |

## Community

| Resource | Type | URL |
|----------|------|-----|
| _(add communities)_ | Forum/Discord/etc. | — |
"""


def make_projects_content(display_name: str, today: str) -> str:
    return f"""# {display_name} — Projects

> Project ideas organized by difficulty. Build these to solidify your understanding.
> Document completed projects in this file and link to your implementation.

---

_Last updated: {today}_

---

## Beginner Projects

### Project B1: Hello, {display_name}

**Goal:** Build the simplest possible working example of this topic.
**Skills tested:** Basic syntax, setup, first working program.
**Estimated time:** 1–2 hours

**Requirements:**
- [ ] Create a minimal working example
- [ ] Add comments explaining each step
- [ ] Verify it works correctly

**My implementation:** _(link when complete)_

---

## Intermediate Projects

### Project I1: Practical Application

**Goal:** Build something you would actually use.
**Skills tested:** Core concepts, error handling, real-world usage.
**Estimated time:** 4–8 hours

**Requirements:**
- [ ] Solve a real problem you have
- [ ] Handle edge cases
- [ ] Write basic tests

**My implementation:** _(link when complete)_

---

## Advanced Projects

### Project A1: Deep Dive

**Goal:** Explore a non-obvious aspect of the topic.
**Skills tested:** Advanced features, performance, internals.
**Estimated time:** 8–16 hours

**Requirements:**
- [ ] Go beyond tutorials
- [ ] Benchmark or profile your solution
- [ ] Write thorough documentation

**My implementation:** _(link when complete)_

---

## Capstone

### Project C1: Showcase Project

**Goal:** Demonstrate mastery of the entire topic.
**Skills tested:** Everything.
**Estimated time:** 20+ hours

**Requirements:**
- [ ] Combines concepts from at least 5 different modules
- [ ] Production-quality code and documentation
- [ ] Could be shown to a potential employer

**My implementation:** _(link when complete)_
"""


def make_module_readme(
    topic_display: str,
    module_display: str,
    module_index: int,
    today: str,
    difficulty: str,
) -> str:
    return f"""# {module_display}

> **Topic:** {topic_display} &nbsp;·&nbsp; **Module:** {module_index:02d} &nbsp;·&nbsp; **Difficulty:** {difficulty.capitalize()}

---

## Overview

_(Write a 2–3 sentence overview of this module after it has been populated by an AI agent or yourself.)_

## Learning Objectives

By the end of this module you will be able to:

1. _(objective 1)_
2. _(objective 2)_
3. _(objective 3)_
4. _(objective 4)_

## Prerequisites

- Completion of previous module(s) in [[{topic_display.lower().replace(" ", "-")}]]
- _(list any specific knowledge required)_

---

## Theory

_(Core content goes here. Add explanations, diagrams, code examples, and references.)_

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| _(concept)_ | _(definition)_ |

---

## Examples

```python
# Example code goes here
```

---

## Summary

_(Summarize the key takeaways from this module.)_

---

## Next Steps

- Complete [EXERCISES.md](./EXERCISES.md)
- Take the [TEST.md](./TEST.md) when ready
- Log questions in [QUESTIONS.md](./QUESTIONS.md)
- Move to the next module when you score ≥ 70%

---

_Last updated: {today}_
"""


def make_module_notes(topic_display: str, module_display: str, today: str) -> str:
    return f"""# Notes — {module_display}

> Personal study notes for this module. Append freely.
> AI agents may also append summaries here. **Nothing is ever deleted.**

---

_Started: {today}_

---

## {today} — Initial Notes

_(Write your first notes here as you study the module README.)_

**Key takeaways:**
-

**Things I want to remember:**
-

**Connections to other topics:**
-

---

_Add new entries above this line, newest last._
"""


def make_module_questions(topic_display: str, module_display: str, today: str) -> str:
    return f"""# Questions — {module_display}

> Log questions here as they arise. AI agents will append answers.
> **Never delete questions** — they are part of your learning record.

---

_Started: {today}_

---

## Open Questions

_(Write questions here as you study. Be specific — vague questions get vague answers.)_

---

_Add new questions above this line._
"""


def make_module_exercises(topic_display: str, module_display: str, today: str) -> str:
    return f"""# Exercises — {module_display}

> Practice problems for this module. Work through them in order.
> Mark each complete with an `x`: `- [x]`.

---

_Last updated: {today}_

---

## Easy Exercises (1 pt each)

- [ ] **E1.** _(exercise description)_

  <details><summary>Hint</summary>_(hint)_</details>

- [ ] **E2.** _(exercise description)_

---

## Medium Exercises (2 pts each)

- [ ] **M1.** _(exercise description)_

---

## Hard Exercises (3 pts each)

- [ ] **H1.** _(exercise description)_

---

## Challenge (5 pts)

- [ ] **C1.** _(open-ended challenge)_

---

**Total possible: __ pts**
"""


def make_module_test(topic_display: str, module_display: str, today: str) -> str:
    return f"""# Test — {module_display}

> Formal self-assessment. Attempt this **after** completing the module content and exercises.
> Write your answers directly in this file, then ask an AI agent to grade it.

---

**Date attempted:** __{today}__
**Time taken:** ____ minutes
**Open-book:** No (attempt from memory first)

---

## Part 1 — Easy (1 pt each)

**Q1.** _(question)_

**Your answer:**

---

**Q2.** _(question)_

**Your answer:**

---

## Part 2 — Medium (2 pts each)

**Q3.** _(question)_

**Your answer:**

---

**Q4.** _(question)_

**Your answer:**

---

## Part 3 — Hard (3 pts each)

**Q5.** _(question)_

**Your answer:**

---

## Part 4 — Expert (5 pts)

**Q6.** _(open-ended or essay question)_

**Your answer:**

---

## Bonus (variable pts)

**B1.** _(bonus question)_

**Your answer:**

---

_When done, ask your AI agent: "Grade my test in {topic_display} module {module_display}"_
"""


def make_module_answers(topic_display: str, module_display: str, today: str) -> str:
    return f"""# Answers — {module_display}

> This file contains the answer key and grading records.
> **AI agents append grading records here. Never delete records.**

---

## Answer Key

_(Populated by AI agent when module content is generated.)_

**Q1.** _(answer)_

**Q2.** _(answer)_

**Q3.** _(answer)_

**Q4.** _(answer)_

**Q5.** _(answer)_

**Q6.** _(answer)_

---

## Grading Records

_(Grading records appended below by AI agents after each test attempt.)_

---
"""


def make_module_resources(topic_display: str, module_display: str, today: str) -> str:
    return f"""# Resources — {module_display}

> Module-specific resources. These supplement the topic-level RESOURCES.md.

---

_Last updated: {today}_

---

## Required Reading

- _(add links and references)_

## Recommended Videos

- _(add video links)_

## Further Reading

- _(add optional deep-dive resources)_

## Documentation

- _(add official docs links)_
"""


# ---------------------------------------------------------------------------
# File creation logic
# ---------------------------------------------------------------------------


def collect_files_to_create(
    cfg: TopicConfig,
    module_names: list[str],
    placeholders: dict[str, str],
) -> list[tuple[Path, str]]:
    """
    Return a list of (path, content) pairs for all files to be written.
    No I/O happens here — this is pure data.
    """
    topic_dir = TOPICS_DIR / cfg.name
    files: list[tuple[Path, str]] = []

    # ---- Topic-level files ------------------------------------------------

    # README.md — from template
    readme_tpl = TEMPLATES_DIR / "topic" / "README.md"
    if readme_tpl.exists():
        content = render_template(readme_tpl.read_text(encoding="utf-8"), placeholders)
    else:
        content = f"# {cfg.display_name}\n\n> {cfg.description}\n"
    files.append((topic_dir / "README.md", content))

    # ROADMAP.md — from template
    roadmap_tpl = TEMPLATES_DIR / "topic" / "ROADMAP.md"
    if roadmap_tpl.exists():
        content = render_template(roadmap_tpl.read_text(encoding="utf-8"), placeholders)
    else:
        content = f"# {cfg.display_name} — Learning Roadmap\n\n_(fill in)_\n"
    files.append((topic_dir / "ROADMAP.md", content))

    # GLOSSARY.md
    files.append((topic_dir / "GLOSSARY.md", make_glossary_content(cfg.display_name, cfg.today)))

    # QUESTIONS.md
    files.append((topic_dir / "QUESTIONS.md", make_questions_content(cfg.display_name, cfg.today)))

    # RESOURCES.md
    files.append((topic_dir / "RESOURCES.md", make_resources_content(cfg.display_name, cfg.today)))

    # PROJECTS.md
    files.append((topic_dir / "PROJECTS.md", make_projects_content(cfg.display_name, cfg.today)))

    # ---- Module files -------------------------------------------------------
    modules_dir = topic_dir / "modules"

    for idx, module_label in enumerate(module_names):
        dir_name = module_dir_name(idx, module_label)
        module_display = module_display_name(idx, module_label)
        mod_dir = modules_dir / dir_name

        files.append((
            mod_dir / "README.md",
            make_module_readme(cfg.display_name, module_display, idx, cfg.today, cfg.difficulty),
        ))
        files.append((
            mod_dir / "NOTES.md",
            make_module_notes(cfg.display_name, module_display, cfg.today),
        ))
        files.append((
            mod_dir / "QUESTIONS.md",
            make_module_questions(cfg.display_name, module_display, cfg.today),
        ))
        files.append((
            mod_dir / "EXERCISES.md",
            make_module_exercises(cfg.display_name, module_display, cfg.today),
        ))
        files.append((
            mod_dir / "TEST.md",
            make_module_test(cfg.display_name, module_display, cfg.today),
        ))
        files.append((
            mod_dir / "ANSWERS.md",
            make_module_answers(cfg.display_name, module_display, cfg.today),
        ))
        files.append((
            mod_dir / "RESOURCES.md",
            make_module_resources(cfg.display_name, module_display, cfg.today),
        ))

    return files


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def print_plan(cfg: TopicConfig, module_names: list[str], files: list[tuple[Path, str]]) -> None:
    """Pretty-print the creation plan."""
    print()
    print("  LEAPS — New Topic Plan")
    print("  " + "─" * 50)
    print(f"  Topic:       {cfg.display_name}  ({cfg.name})")
    print(f"  Description: {cfg.description or '(none)'}")
    print(f"  Difficulty:  {cfg.difficulty.capitalize()}")
    print(f"  Modules:     {len(module_names)}  (0. Introduction + {len(module_names) - 1} numbered)")
    if cfg.prerequisites:
        print(f"  Prereqs:     {', '.join(cfg.prerequisites)}")
    print()
    print("  Directory structure:")
    print(f"    TOPICS/{cfg.name}/")

    topic_dir = TOPICS_DIR / cfg.name
    dirs_seen: set[Path] = set()
    for path, _ in files:
        rel = path.relative_to(topic_dir)
        parent = path.parent
        if parent != topic_dir and parent not in dirs_seen:
            dirs_seen.add(parent)
            rel_dir = parent.relative_to(topic_dir)
            print(f"    ├── {rel_dir}/")
        indent = "    │   " if path.parent != topic_dir else "    ├── "
        print(f"    {indent}{path.name}")

    print()
    print(f"  Total: {len(files)} files across {len(dirs_seen) + 1} directories")
    print()


def print_summary(cfg: TopicConfig, module_names: list[str], files: list[tuple[Path, str]]) -> None:
    """Print a success summary after creation."""
    topic_dir = TOPICS_DIR / cfg.name
    print()
    print("  LEAPS — Topic Created Successfully")
    print("  " + "─" * 50)
    print(f"  Topic:    {cfg.display_name}")
    print(f"  Location: {topic_dir}")
    print(f"  Files:    {len(files)} created")
    print()
    print("  Modules created:")
    for idx, name in enumerate(module_names):
        dir_name = module_dir_name(idx, name)
        print(f"    {idx:02d}. {name:<30}  modules/{dir_name}/")
    print()
    print("  Next steps:")
    print(f"    1. Open TOPICS/{cfg.name}/README.md and fill in the overview")
    print(f"    2. Review TOPICS/{cfg.name}/ROADMAP.md")
    print(f"    3. Start studying: TOPICS/{cfg.name}/modules/00_introduction/README.md")
    print(f"    4. Ask your AI agent: \"Populate module 00 for {cfg.display_name}\"")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    args = parse_args()

    # Validate inputs
    try:
        topic_slug = validate_topic_name(args.topic_name)
        num_modules = validate_modules(args.modules)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # Check for conflicts
    topic_dir = TOPICS_DIR / topic_slug
    if topic_dir.exists():
        print(f"ERROR: Topic '{topic_slug}' already exists at {topic_dir}", file=sys.stderr)
        print("       Use a different name, or remove the existing directory first.", file=sys.stderr)
        return 1

    # Parse prerequisites
    prereqs = [p.strip() for p in args.prerequisites.split(",") if p.strip()] if args.prerequisites else []

    # Build config
    cfg = TopicConfig(
        name=topic_slug,
        display_name=slug_to_display_name(topic_slug),
        description=args.description,
        difficulty=args.difficulty,
        num_modules=num_modules,
        prerequisites=prereqs,
        today=date.today().isoformat(),
    )

    # Build module names: 0 = Introduction, then DEFAULT_MODULE_NAMES up to N
    module_names: list[str] = ["Introduction"]
    for i in range(1, num_modules + 1):
        if i - 1 < len(DEFAULT_MODULE_NAMES):
            module_names.append(DEFAULT_MODULE_NAMES[i - 1])
        else:
            module_names.append(f"Module {i}")

    # Build placeholder map and file list
    placeholders = make_placeholders(cfg, module_names)
    files = collect_files_to_create(cfg, module_names, placeholders)

    # Dry run: print plan and exit
    if args.dry_run:
        print_plan(cfg, module_names, files)
        print("  [DRY RUN] No files written.")
        print()
        return 0

    print_plan(cfg, module_names, files)
    print("  Creating files...")

    # Create all directories and write all files
    for path, content in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    print_summary(cfg, module_names, files)
    return 0


if __name__ == "__main__":
    sys.exit(main())
