# AI Agents Guide

This document is for AI agents working in the leaps repository. It complements
`AGENTS.md` (which covers operational instructions) with higher-level principles:
why leaps is structured the way it is, how agents should reason about quality,
and what the common failure modes look like.

If you are an agent reading this for the first time, also read:

- `AGENTS.md` — required operational instructions
- `CONTRIBUTING.md` — structure rules and file conventions
- `docs/educational-philosophy.md` — the learning science behind the design

---

## Why AI-Native Design Matters

Most repositories are designed for human contributors who navigate via IDE,
browser, and intuition built up from years of context. leaps is designed to be
equally legible to an AI agent working from text alone.

This means:

- **Predictable structure.** Every module has the same files in the same places.
  An agent that has read one module understands the schema for all modules.
- **Explicit contracts.** `CONTRIBUTING.md` and `AGENTS.md` state rules that would
  otherwise live in tacit human knowledge. Agents cannot observe tacit knowledge.
- **Machine-readable metadata.** YAML frontmatter, consistent heading formats,
  and named sections (`## Prerequisites`, `## Learning Objectives`) make content
  parseable without heuristics.
- **Validation scripts.** `SCRIPTS/validate_structure.py` tells an agent exactly
  what it got wrong, without requiring a human reviewer in the loop.

The goal is a repository where an agent with no prior context can clone it, read
`AGENTS.md`, and produce a high-quality new module without guessing.

---

## How the Repository Is Structured for AI Consumption

### Layered Specificity

Documentation is organized from most general to most specific:

1. `README.md` (root) — what leaps is
2. `CONTRIBUTING.md` — how to contribute
3. `AGENTS.md` — how agents specifically should operate
4. `docs/` — deep background on philosophy and tooling
5. `TEMPLATES/` — the actual file shapes to produce
6. `TOPICS/<topic>/README.md` — topic-level context
7. `TOPICS/<topic>/modules/<module>/README.md` — module-level content

An agent should read down this hierarchy to the level of specificity needed for
the task at hand. Do not skip levels — the constraints compound.

### Named Sections as a Protocol

Every file type uses named sections that are part of the repository's protocol.
When generating content, agents must preserve these section names exactly. The
TOC generator, validation script, and Dataview queries all depend on them.

Do not rename `## Learning Objectives` to `## Goals` or `## What You Will Learn`.
Do not split `## Prerequisites` into `## Hard Prerequisites` and `## Soft Prerequisites`.
Follow the schema.

### Frontmatter as Structured Data

Module READMEs have YAML frontmatter. Treat it as a database record:

```yaml
---
topic: python
module: 04_functions_and_scope
difficulty: beginner
status: complete
last_reviewed: 2025-01-15
tags: [functions, closures, scope, higher-order-functions]
---
```

- `difficulty` must be one of: `beginner`, `intermediate`, `advanced`, `expert`
- `status` must be one of: `draft`, `in-progress`, `complete`, `needs-review`
- `last_reviewed` must be `YYYY-MM-DD` format
- `tags` should use lowercase, hyphen-separated terms

---

## Key Principles for AI-Assisted Learning

### Principle 1: Depth Is the Goal

The failure mode of AI-generated educational content is **plausible superficiality**:
content that sounds correct and complete but stops exactly at the surface.

A module that lists the names of Python's data structures is not a learning resource.
A module that explains why a `dict` lookup is O(1) while a `list` search is O(n),
demonstrates the performance difference with a notebook, and gives exercises that
require the learner to choose the right structure — that is a learning resource.

Ask yourself: "After working through this module, can a learner solve a new problem
involving this concept without looking anything up?" If the answer is no, the module
is not done.

### Principle 2: Correctness Is Non-Negotiable

Incorrect content in a learning repository is worse than missing content. A gap
leaves a learner uncertain. An error leaves a learner confidently wrong.

Before writing any factual claim, verify it. If you cannot verify a claim within
the context of the current task, either:

1. Mark it with a `<!-- TODO: verify -->` HTML comment and a specific question
2. Omit it entirely

Never generate citations, book titles, author names, paper titles, or URLs that you
have not verified. The `CONTRIBUTING.md` rule against hallucinated references exists
because confident fabrication is a serious failure in an educational context.

### Principle 3: Examples Must Be Runnable

Code examples in module notes must be syntactically correct and produce the stated
output. Jupyter notebooks must run top-to-bottom in a clean kernel.

When writing code examples:
- Test the logic mentally step by step before writing the output comment
- If a cell has a side effect (writes a file, makes a network request), note it
- Use realistic variable names, not `x`, `foo`, `temp`
- Write the example to demonstrate the concept, not to showcase complexity

### Principle 4: Cross-links Are Part of the Work

A module that teaches closures without linking to `SHARED/concepts/memory-management.md`
and `TOPICS/python/modules/01_data_types/` is incomplete. The cross-links are not
decoration — they are what makes leaps a knowledge graph rather than a collection of
isolated documents.

When generating a module, scan the repository for related concepts and add links.
When in doubt, link.

### Principle 5: Use the Validation Scripts

Before considering a contribution complete, run:

```bash
python SCRIPTS/validate_structure.py
python SCRIPTS/find_broken_links.py
python SCRIPTS/validate_notebooks.py   # if adding notebooks
```

These scripts exist precisely so that agents (and humans) have an objective signal
about correctness. A contribution that passes validation is not necessarily good,
but one that fails validation is definitely incomplete.

---

## Common Agent Mistakes and How to Avoid Them

### Mistake 1: Summary Instead of Module

**What it looks like:** The module README covers the topic in 300 words and a few
bullet points. Every concept is named but none are explained. There are no exercises.
The test questions are trivially easy.

**Why it happens:** Agents optimize for coverage and speed. Generating a plausible
summary of a concept is easier than building the genuine understanding needed to
explain it well.

**How to avoid it:** Check the Learning Objectives. If the exercises do not require
the learner to demonstrate each objective, the module is a summary, not a module.
Add depth until the exercises are non-trivial.

### Mistake 2: Hallucinated References

**What it looks like:** The RESOURCES.md cites "Advanced Python Programming" by
John Smith (2021, O'Reilly) with a link to `https://oreilly.com/library/view/...`
that leads to a 404 or a different book.

**Why it happens:** Language models have seen many bibliographic patterns and will
generate plausible-sounding citations that do not exist.

**How to avoid it:** Only cite resources you can verify exist with the stated title,
author, and URL. When uncertain, use the resource's official landing page. For books,
prefer linking to the publisher or author's site, not retail links that change.

### Mistake 3: Wrong Difficulty Level

**What it looks like:** A module marked `difficulty: beginner` requires knowledge of
decorators, closures, and metaclasses. Or a module marked `difficulty: advanced`
explains what a variable is.

**Why it happens:** Agents do not have calibrated intuitions about learner prior knowledge.

**How to avoid it:** Read the module's Prerequisites section and imagine a learner
who just completed exactly those prerequisites and nothing more. Can they understand
this module? If not, add prerequisite material or raise the difficulty level.

### Mistake 4: Ignoring the Schema

**What it looks like:** A module README has `## Goals` instead of `## Learning Objectives`,
or puts exercises in the README instead of `EXERCISES.md`, or uses level-3 headings
as the first heading in a file.

**Why it happens:** Agents generate natural-sounding content that locally makes sense
but violates the repository's conventions.

**How to avoid it:** Read the template before writing. After writing, diff your output
against the template. Run `validate_structure.py`. The script will catch structural
violations.

### Mistake 5: Broken Links That Look Valid

**What it looks like:** `[[python#closures]]` appears in a cross-link, but the Python
topic README has no `## Closures` section — there is a `## Closure Functions` section.
The link resolves to the file but not the section.

**Why it happens:** Agents generate link text that is plausible but not exact.

**How to avoid it:** Run `find_broken_links.py`. For section links, copy the heading
text exactly (lowercased, spaces replaced with hyphens for Markdown links, or kept
as-is for wiki-links depending on your Obsidian resolver).

### Mistake 6: Generating Content Without Context

**What it looks like:** A new module is added to an existing topic, but it introduces
vocabulary that contradicts how the topic's earlier modules used it, or assumes
knowledge that is not in the topic's prerequisite chain.

**Why it happens:** The agent processes the module in isolation without reading the
full topic structure.

**How to avoid it:** Before generating a new module for an existing topic, read the
topic's `README.md` and the READMEs of the preceding modules. Maintain vocabulary
and conceptual continuity.

---

## The Future Vision: AI + Learning

leaps is an experiment in what a repository optimized for AI-assisted learning can
look like. Several directions are worth exploring:

**Adaptive module generation.** Given a learner's progress data (captured in
frontmatter and journal notes), an agent could identify the highest-value next module
to build — the one that connects the most existing knowledge to the most unlearned
territory.

**Automated spaced repetition scheduling.** The `progress_report.py` script currently
surfaces stale modules. A more sophisticated version could recommend specific review
sessions based on the Leitner system or SM-2 algorithm applied to TEST.md answer
history.

**Socratic agents.** Rather than generating content, an agent that asks the learner
questions about a module — and adapts its questions based on the responses — would
produce deeper engagement than any amount of well-written notes.

**Cross-repository knowledge graphs.** leaps is one node. The knowledge graph becomes
most powerful when leaps links to external repositories, papers, and courses in a way
that is machine-navigable — not just human-readable link lists, but structured
relationships with typed edges (is-prerequisite-for, is-example-of, contradicts, etc.).

These are open problems. If you are an agent reading this in a future where some of
them have been solved, update this document.

---

## A Note on Agency and Responsibility

Agents working in leaps are creating content that other people — and other agents —
will use to learn. That is a meaningful responsibility.

The leaps design attempts to make good outcomes the path of least resistance: clear
schemas, validation scripts, quality checklists, and a public PRR process all push
toward correctness and depth. But no toolchain substitutes for the judgment to notice
when content is plausible but wrong, or complete by the checklist but shallow in
substance.

Use that judgment. The checklist is a floor, not a ceiling.
