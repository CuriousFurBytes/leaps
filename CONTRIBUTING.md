# Contributing to leaps

> **Learning Environment for Any Progressive Subject**

Welcome to leaps. This guide covers everything you need to know to contribute meaningfully — whether you are a human learner expanding an existing topic, an AI agent generating new content, or an educator designing a curriculum. Contributions of all sizes matter. A single corrected explanation, a better exercise, or a newly discovered cross-link can improve the learning experience for everyone who studies this material after you.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Philosophy](#philosophy)
3. [Getting Started](#getting-started)
4. [Repository Structure Overview](#repository-structure-overview)
5. [Content Standards](#content-standards)
6. [Markdown Standards](#markdown-standards)
7. [Naming Conventions](#naming-conventions)
8. [Adding a New Topic](#adding-a-new-topic)
9. [Improving Existing Content](#improving-existing-content)
10. [Adding Exercises](#adding-exercises)
11. [Adding Tests](#adding-tests)
12. [Previewing the Book](#previewing-the-book)
13. [Cross-Linking](#cross-linking)
14. [Citation Standards](#citation-standards)
15. [Pull Request Process](#pull-request-process)
16. [Code of Conduct](#code-of-conduct)
17. [Educational Quality Review Checklist](#educational-quality-review-checklist)

---

## Introduction

### Welcome

leaps is a living knowledge base. It is not a static textbook. Every module grows richer each time someone asks a better question, writes a clearer explanation, or finds a connection that was not obvious before. Your contribution — however small — makes the entire base more valuable.

### Why Contributions Matter

- **Depth compounds.** A concept explained once is understood once. A concept explained five different ways, with three exercises and two cross-links to related ideas, is understood deeply and retained permanently.
- **Questions are assets.** A logged question in `QUESTIONS.md` is a permanent record that other learners will encounter and benefit from. An answer to that question doubles its value.
- **Structure is leverage.** When every module follows the same structure, AI agents, search tools, and human readers can navigate, expand, and build on the material without friction. Consistent structure multiplies every contribution's reach.
- **Public learning accelerates learning.** Writing what you know — even imperfectly — forces clarity. Being corrected in public is faster than being confused in private.

### Who Can Contribute

| Contributor | What They Add |
|---|---|
| **Learners** | Notes, questions, exercise solutions, journal entries, resource recommendations |
| **Experts** | Deep explanations, historical context, edge cases, advanced modules |
| **Educators** | Module structure improvements, pedagogical sequencing, test design |
| **AI agents** | Content generation, cross-linking, test grading |
| **Developers** | Tooling, scripts, validators, CI workflows |
| **Everyone** | Typo fixes, broken link repairs, clarity improvements |

> [!NOTE]
> You do not need to be an expert in a topic to contribute to it. Learners asking good questions and documenting their confusion are among the most valuable contributors — they surface exactly the places where explanations need work.

---

## Philosophy

### Deep Learning, Not Surface Coverage

leaps is built on the conviction that shallow coverage is worse than no coverage. A module that lists definitions without explaining mechanisms, or shows code without explaining why it works, actively misleads learners by creating the illusion of understanding.

Every contribution should aim to help a reader understand **why** something is true, not just **what** is true. Ask yourself: "If someone reads only this file, will they understand not just the mechanics but the reasoning behind those mechanics?"

### Quality Over Quantity

One well-written module with clear explanations, working examples, thoughtful exercises, and accurate citations is worth more than five modules that are superficially complete. Reviewers will reject content that:

- Uses placeholder text without filling it in
- Copies definitions verbatim from a source without explanation
- Provides examples that do not run, do not illustrate the point, or are not explained
- Makes claims without citing sources or providing verifiable reasoning

### Educational Standards

Content in leaps is held to the standard of a well-written technical textbook, not a blog post or Stack Overflow answer. That means:

- **Precision:** Use terms correctly and define them when first introduced
- **Progression:** Each module builds explicitly on prior modules
- **Completeness:** Cover not just the happy path but common errors, edge cases, and gotchas
- **Context:** Place every concept in its historical, theoretical, and practical context
- **Honesty:** Acknowledge when something is complex, debated, or incompletely understood

### Learning in Public

leaps is a "learn in public" repository. Your questions, test scores, and journal entries are recorded and visible. This is intentional. The vulnerability of public learning is a feature: it creates accountability, invites correction, and models intellectual honesty for future learners.

---

## Getting Started

### Prerequisites

- Git installed and configured
- A GitHub account
- Familiarity with Markdown
- (Optional) Obsidian for wiki-link navigation
- (Optional) Python 3.10+ for tooling and previewing the book (`pip install zensical`)

### Fork and Clone

```bash
# Fork via GitHub UI, then:
git clone https://github.com/YOUR_USERNAME/leaps.git
cd leaps

# Add the upstream remote to stay in sync
git remote add upstream https://github.com/your-org/leaps.git
```

### Sync Before Working

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

### Branch Naming

Branches must follow this convention so that CI and reviewers can immediately understand their scope:

| Branch Type | Pattern | Example |
|---|---|---|
| New content (topic or module) | `content/topic-name` | `content/rust-lifetimes` |
| Fixing an issue in a module | `fix/topic-module-issue` | `fix/python-module-03-broken-examples` |
| Tooling or scripts | `tooling/description` | `tooling/lint-improvements` |
| Documentation | `docs/description` | `docs/contributing-update` |
| Templates | `template/description` | `template/module-format` |

```bash
# Example: adding a new module to rust
git checkout -b content/rust-module-05-traits
```

### Install Tooling (Optional but Recommended)

```bash
# Run the structure linter before opening a PR
./SCRIPTS/lint.sh

# Check for broken cross-links
./SCRIPTS/lint.sh --links-only

# View statistics
./SCRIPTS/stats.sh
```

---

## Repository Structure Overview

```
leaps/
├── README.md                  # Project overview
├── CONTRIBUTING.md            # This file
├── AGENTS.md                  # AI agent operational contract
│
├── PROMPTS/                   # Reusable AI prompt templates
├── SCRIPTS/                   # Automation and validation scripts
├── TEMPLATES/                 # File templates for topics and modules
├── SHARED/                    # Cross-topic shared knowledge
│   ├── glossary.md
│   ├── concepts.md
│   └── references.md
│
├── TOPICS/                    # All learning topics
│   └── [topic]/
│       ├── README.md          # Topic overview
│       ├── PROGRESS.md        # Running progress tracker
│       └── modules/
│           └── [NN_module-name]/
│               ├── README.md
│               ├── NOTES.md
│               ├── QUESTIONS.md
│               ├── EXERCISES.md
│               ├── TEST.md
│               ├── ANSWERS.md
│               ├── RESOURCES.md
│               └── PROJECTS.md
│
├── assets/                    # Images and diagrams
├── environments/              # Reproducible learning environments
├── tools/                     # Developer tooling
├── zensical.toml              # Published-book config (docs_dir = TOPICS/)
└── docs/                      # Extended documentation
```

For the full annotated structure, see [`README.md`](README.md#repository-structure).

---

## Content Standards

### Writing Quality

All prose in leaps must be:

- **Clear:** Write for an intelligent reader encountering the topic for the first time. Do not assume context that has not been established in the current file or a linked prerequisite.
- **Active voice:** Prefer "the compiler checks types" over "types are checked by the compiler."
- **Concrete:** Abstract claims must be accompanied by a concrete example. Never write "this is useful in many contexts" without naming at least two specific contexts.
- **Concise:** Remove filler phrases. "It is important to note that" → delete. "In order to" → "to."
- **Consistent terminology:** Choose terms and stick to them. If you introduce "goroutine" in module 1, do not call it a "lightweight thread" in module 4 without a cross-reference.

### Explanation Depth: WHY, Not Just WHAT

Every technical explanation must answer all three questions:

1. **What is it?** — A precise definition or description
2. **How does it work?** — The mechanism, algorithm, or process
3. **Why does it matter?** — The real-world consequence of using (or misusing) it

**Insufficient:**
> A closure captures variables from its enclosing scope.

**Sufficient:**
> A closure is a function that retains access to the variables in the lexical scope where it was defined, even after that scope has exited. This works because the runtime allocates captured variables on the heap rather than the stack, extending their lifetime. This matters for callback-heavy code (event handlers, async operations, higher-order functions) where you need a function to "remember" context from when it was created — and it matters for memory management because long-lived closures can unintentionally keep large objects alive.

### Example Quality

Examples must be:

- **Working:** Every code example must compile and run correctly with no modification. Include the exact command needed to run it if it is not obvious.
- **Minimal:** Remove everything not needed to illustrate the point. If an example requires 100 lines of boilerplate, extract the relevant 10 lines and link to the full example.
- **Explained:** Every non-trivial line in a code example should either be obvious to the target audience or have an inline comment. Do not paste code without explanation.
- **Real-world relevant:** Prefer examples that resemble actual usage. `foo`, `bar`, and `baz` are acceptable for illustrating syntax. They are not acceptable for illustrating concepts.
- **Progressive:** If a file contains multiple examples, they should increase in complexity. The first example should be the simplest possible illustration of the concept.

### Reference Quality

- Only cite sources you have verified are accurate and accessible
- Prefer primary sources (official documentation, original papers, specification documents) over secondary sources (blog posts, tutorials)
- For books, include author, title, edition, publisher, and year
- For online sources, include URL and date accessed
- For academic papers, include full citation in a standard format (APA, IEEE, or ACM)
- Do not cite sources behind paywalls without noting that they require access

### Historical Context Requirements

Every topic README must include historical context. Every module that introduces a non-obvious design decision (e.g., why Go has no exceptions, why Rust uses ownership instead of GC) must explain the historical and technical reasons for that decision. Context transforms isolated facts into connected understanding.

---

## Markdown Standards

### Heading Hierarchy

- **H1 (`#`):** Title only. One per file, at the top.
- **H2 (`##`):** Major sections. These should correspond to entries in the table of contents.
- **H3 (`###`):** Subsections within an H2. Named clearly enough that a reader skimming headings understands the document structure.
- **H4 (`####`):** Deep subsections. Use sparingly. If you need H5+, restructure.
- **Never skip levels.** Do not jump from H2 to H4.

### Table of Contents Format

Every file with more than three H2 sections must include a table of contents immediately after the opening paragraph or metadata block. Use anchor links:

```markdown
## Table of Contents

1. [Section One](#section-one)
2. [Section Two](#section-two)
3. [Sub-section Example](#sub-section-example)
```

Anchor format: lowercase, spaces replaced by hyphens, special characters removed. GitHub renders these automatically from headings.

### Code Blocks

Always specify the language immediately after the opening fence. This enables syntax highlighting and is required by the linter:

```markdown
    ```python
    def greet(name: str) -> str:
        return f"Hello, {name}"
    ```
```

For shell commands, use `bash` or `sh`. For output that is not code, use `text`. For configuration files, use the appropriate format (`yaml`, `toml`, `json`, `dockerfile`, etc.). For abstract pseudocode, use `text` or `pseudocode`.

For inline code, use backtick wrapping: `variable_name`, `function()`, `--flag`.

### Tables

Use tables for:
- Comparing multiple items across consistent attributes (e.g., language feature comparison)
- Structured reference data (e.g., command flags, API parameters)
- Progress tracking and checklists

Do not use tables for prose that reads naturally as paragraphs. Tables require effort to read — use them only when the tabular structure genuinely aids comprehension.

Table formatting: align pipes, use a header row, and add a blank line before and after the table.

### Callouts / Admonitions

Use GitHub-Flavored Markdown callouts for contextual annotations. Four types are supported:

```markdown
> [!NOTE]
> Supplementary information that adds value but is not essential to the main flow.

> [!TIP]
> Practical advice, a shortcut, or a best practice worth highlighting.

> [!WARNING]
> A common mistake, pitfall, or gotcha that can cause bugs or confusion.

> [!IMPORTANT]
> Critical information that the reader must not skip.
```

Use callouts sparingly. If every other paragraph is a callout, none of them carry weight. Reserve them for genuinely exceptional information.

### Mermaid Diagrams

Use Mermaid for diagrams that illustrate flow, structure, or relationships. Mermaid renders natively in GitHub and Obsidian:

```markdown
    ```mermaid
    flowchart TD
        A[Start] --> B{Condition}
        B -->|Yes| C[Do This]
        B -->|No| D[Do That]
    ```
```

Supported diagram types: `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram`, `erDiagram`, `gantt`, `pie`. Choose the type that most clearly represents the relationship you are illustrating.

Every diagram must have a text caption immediately below it explaining what the diagram shows.

### Wiki-Links

leaps uses Obsidian-compatible wiki-link syntax for internal cross-references:

| Syntax | Resolves To |
|---|---|
| `[[rust]]` | `TOPICS/rust/README.md` |
| `[[rust#ownership]]` | Ownership section in `TOPICS/rust/README.md` |
| `[[rust/module-04-traits]]` | `TOPICS/rust/modules/04_traits/README.md` |
| `[[shared/glossary#closure]]` | Closure entry in `SHARED/glossary.md` |
| `[[concepts#zero-cost-abstractions]]` | Entry in `SHARED/concepts.md` |

Wiki-links are validated by `./SCRIPTS/lint.sh`. A broken wiki-link (pointing to a file or anchor that does not exist) is a lint error and will block the PR.

### Image Handling

- Store all images in `assets/images/[topic]/` for topic-specific images, or `assets/images/shared/` for images used across topics
- Store Mermaid source files in `assets/diagrams/` alongside exported SVGs
- Reference images using relative paths from the file that contains them:
  ```markdown
  ![Description of image](../../../assets/images/rust/ownership-diagram.svg)
  ```
- Provide meaningful alt text for every image — this serves both accessibility and search indexing
- Do not commit binary images larger than 1 MB. For diagrams, prefer Mermaid (rendered natively in the book) or a committed, optimized SVG

### Line Length

There is no hard line-length limit for prose in Markdown files. Write sentences and paragraphs naturally. However, prefer to break lines at sentence boundaries or clause boundaries to make diffs more readable in code review. Code blocks and tables are exempt.

---

## Naming Conventions

### Folders

- Use **lowercase only**
- Use **hyphens** to separate words (not underscores, not spaces, not camelCase)
- No trailing hyphens, no leading hyphens, no double hyphens
- Names must be filesystem-safe and URL-safe

| Good | Bad |
|---|---|
| `data-structures` | `data_structures` |
| `machine-learning` | `Machine Learning` |
| `go` | `Go_Programming` |

### Topic Folders

Topic folders live in `TOPICS/` and should use a **single descriptive word** where possible:

```
TOPICS/go/
TOPICS/rust/
TOPICS/python/
TOPICS/calculus/
TOPICS/statistics/
TOPICS/networking/
```

Multi-word topics use hyphens:
```
TOPICS/linear-algebra/
TOPICS/machine-learning/
TOPICS/data-structures/
TOPICS/operating-systems/
```

### Module Folders

Module folders use the format: `[zero-padded-number]_[snake_case_name]`

The number is always two digits (three for topics with more than 99 modules, which is rare):

```
modules/01_introduction/
modules/02_data_types/
modules/03_control_flow/
modules/10_advanced_patterns/
```

The human-readable module title (used in README headings, links, and UI) uses Title Case: `3. Memory Management`, `10. Advanced Patterns`.

### Files

- Structured documentation files: `UPPERCASE.md` — `README.md`, `NOTES.md`, `QUESTIONS.md`, `EXERCISES.md`, `TEST.md`, `ANSWERS.md`, `RESOURCES.md`, `PROJECTS.md`, `PROGRESS.md`, `ROADMAP.md`
- Source code files: `lowercase_with_underscores.ext` or `kebab-case.ext` per language convention
- Scripts: `kebab-case.sh`, `kebab-case.py`
- Templates: `lowercase-kebab.md`

---

## Adding a New Topic

Before creating a new topic, search existing `TOPICS/` to confirm it does not already exist under a different name. Also check open issues for a `topic-request` label covering the same subject.

### Step 1: Open an Issue (for human contributors)

Open an issue with label `topic-request`. Include:
- Topic name and brief description
- Proposed module outline (5–15 modules)
- Why this topic belongs in leaps
- Your familiarity with the subject

### Step 2: Create the Branch

```bash
git checkout -b content/[topic-name]
```

### Step 3: Scaffold the Directory

Use the scaffold script for consistency:

```bash
./SCRIPTS/new-topic.sh [topic-name]
```

This creates the standard directory structure from templates. If the script is unavailable, create manually:

```bash
mkdir -p TOPICS/[topic-name]/modules
cp TEMPLATES/topic/README.md TOPICS/[topic-name]/README.md
cp TEMPLATES/topic/ROADMAP.md TOPICS/[topic-name]/ROADMAP.md
cp TEMPLATES/topic/RESOURCES.md TOPICS/[topic-name]/RESOURCES.md
cp TEMPLATES/topic/GLOSSARY.md TOPICS/[topic-name]/GLOSSARY.md
cp TEMPLATES/topic/QUESTIONS.md TOPICS/[topic-name]/QUESTIONS.md
cp TEMPLATES/topic/PROJECTS.md TOPICS/[topic-name]/PROJECTS.md
touch TOPICS/[topic-name]/PROGRESS.md
```

### Step 4: Fill In the Topic README

Replace all `{{PLACEHOLDER}}` values in `TOPICS/[topic-name]/README.md` with real content. Do not leave placeholders in a PR. A topic README must include:

- A clear one-paragraph description of what the topic covers
- Historical context (when was it created, by whom, why)
- Real-world applications (minimum three concrete examples)
- Learning objectives (minimum five measurable outcomes)
- Difficulty rating and time estimate
- Prerequisites (with wiki-links to other leaps topics where possible)
- A complete module list (even if the modules are not yet written — stubs are acceptable)

### Step 5: Create the First Module

```bash
./SCRIPTS/new-module.sh [topic-name] 01_introduction
```

Or manually:

```bash
mkdir -p TOPICS/[topic-name]/modules/01_introduction
for f in README NOTES QUESTIONS EXERCISES TEST ANSWERS RESOURCES PROJECTS; do
  cp TEMPLATES/module/$f.md TOPICS/[topic-name]/modules/01_introduction/$f.md
done
```

### Step 6: Write the First Module

At minimum, the first module must be complete before a topic PR is opened. Complete means: `README.md` has full content, `EXERCISES.md` has at least five exercises, `TEST.md` has a full test with answer key in `ANSWERS.md`, and `RESOURCES.md` has at least three verified resources.

### Step 7: Run the Linter

```bash
./SCRIPTS/lint.sh
```

Fix all errors before opening a PR.

### Step 8: Open the Pull Request

Follow the [Pull Request Process](#pull-request-process) below.

---

## Improving Existing Content

Improvements to existing content are among the most valuable contributions. Before editing:

1. Read the entire file you are modifying
2. Read the module's README.md if you are editing a non-README file
3. Check `QUESTIONS.md` for open questions relevant to your improvement
4. Check the git log to understand the history of the file

### What to Improve

- Explanations that are technically correct but unclear
- Examples that do not run or do not illustrate the stated point
- Missing "why" reasoning behind design decisions
- Broken or missing cross-links
- Resources that are dead links or have been superseded
- Test questions that are ambiguous or have incorrect answer keys
- Historical context that is incomplete or inaccurate

### What Not to Change Without Discussion

- The overall structure of a module (number of sections, names of standard files)
- The difficulty or prerequisite chain of a topic without opening an issue first
- Grading records in `ANSWERS.md` — these are append-only
- Existing entries in `QUESTIONS.md` — only append, never delete

### Style of Edits

For significant content changes (rewriting an explanation, adding a new section, restructuring examples), open a PR with a clear description of what you changed and why. For minor fixes (typos, dead links, formatting), you may batch multiple small fixes into a single PR.

---

## Adding Exercises

### Exercise Quality Standards

Exercises are the core learning mechanism in leaps. They are not afterthoughts. Each exercise must:

- **Test a specific, named concept** from the module, not a vague combination of things
- **Be completable** by a learner who has studied only the current module and its stated prerequisites
- **Have a clear success criterion** — the learner should be able to self-assess whether their answer is correct
- **Include a solution** in the accompanying solution section or a hint that makes the path to the solution clear
- **Escalate in difficulty** within the exercise set — the first exercise is easy, the last is hard

### Exercise Format

```markdown
### Exercise N: [Descriptive Title]

**Difficulty:** Beginner | Intermediate | Advanced | Expert

**Concept tested:** [Name the specific concept this tests]

**Instructions:**
[Clear, unambiguous description of what the learner must do]

**Starter code (if applicable):**
```[language]
// starter code here
```

**Expected output / acceptance criteria:**
[What a correct solution produces or satisfies]

**Hints:**
1. [First hint — minimal, does not give away the answer]
2. [Second hint — more specific if the first was not enough]

**Solution:**
<details>
<summary>Show solution</summary>

```[language]
// solution code here
```

**Explanation:** [Why this solution works, what to learn from it]
</details>
```

### Exercise Variety

Each module's `EXERCISES.md` should include a mix:

| Type | Description | Minimum |
|---|---|---|
| **Recall** | Define, name, or list something | 1 |
| **Conceptual** | Explain why, compare/contrast, predict behavior | 2 |
| **Coding** | Write a working implementation | 2 |
| **Debugging** | Find and fix a broken piece of code | 1 |
| **Design** | Design a solution given constraints | 1 |
| **Research** | Investigate a related concept not covered in the module | 1 |

---

## Adding Tests

Tests in leaps are formal assessments. They are distinct from exercises: exercises are practice, tests are measurement.

### Test Question Types

| Type | Description | Typical Points |
|---|---|---|
| **Multiple choice** | One correct answer from four options | 1 pt |
| **True/False with justification** | T/F statement plus required explanation | 1 pt |
| **Fill in the blank** | Complete a code snippet or sentence | 1 pt |
| **Short answer** | 1–3 sentences answering a conceptual question | 2 pts |
| **Code reading** | Given code, predict output or identify behavior | 2 pts |
| **Code writing** | Write a working implementation | 3 pts |
| **Debugging** | Identify and fix a bug in provided code | 3 pts |
| **Essay / design** | Explain a design decision or architect a solution | 5 pts |

### Difficulty Distribution

A balanced module test should have:

- **Easy (40%):** Recall and definition questions. A student who has read the material once should pass these.
- **Medium (35%):** Conceptual questions requiring genuine understanding. Requires thinking, not just recall.
- **Hard (20%):** Practical and debugging questions. Requires applying knowledge in unfamiliar ways.
- **Expert (5%):** Architecture and synthesis questions. Tests whether the learner can reason at the level of the topic, not just recall facts.

Aim for 20–30 points total per module test. Include 2–3 bonus questions worth additional points.

### Answer Key Format

`ANSWERS.md` contains:

1. The complete answer key with explanations for every answer
2. Scoring rubric for partial credit (especially for essay and coding questions)
3. Grading records appended by AI agents (see [Testing & Grading](README.md#testing--grading))

Answer keys must explain **why** each answer is correct, not just state the answer. A learner reading the answer key should learn something, not just be corrected.

---

## Previewing the Book

The learning material is published as a static book built with
[Zensical](https://zensical.org) and deployed to GitHub Pages automatically on
every push to `main` (see [`.github/workflows/docs.yml`](.github/workflows/docs.yml)).
The book is generated from the `TOPICS/` directory, so any topic or module you
add appears in it automatically — there is no separate authoring step and no
navigation file to maintain.

### Preview your changes locally

```bash
pip install zensical
zensical serve        # live-reloading preview at http://localhost:8000
```

### Build it the way CI does

```bash
zensical build --clean   # renders the static site into ./site/ (git-ignored)
```

> [!TIP]
> Before opening a PR, run `zensical build --clean` and confirm it completes
> without errors and that your new pages render correctly (code blocks, Mermaid
> diagrams, callouts, and relative links).

> [!NOTE]
> Authoring rule: write learning content as **Markdown only**. Jupyter notebooks
> are not part of leaps — notebook integration was removed to keep GitHub Pages
> deployment simple. Use fenced code blocks, Mermaid diagrams, admonitions, and
> committed static images for rich content.

---

## Cross-Linking

Cross-links are the connective tissue of leaps. They transform isolated notes into a knowledge graph. Every contribution should consider: "Is there a related concept, pattern, or approach elsewhere in this repository that a reader should know about?"

### When to Add a Cross-Link

Add a cross-link when:

- A concept in the current module was introduced or is covered more deeply in another module or topic
- A prerequisite concept is formally covered elsewhere and you want to direct the reader there
- A pattern, algorithm, or technique in the current module has a named parallel in another domain (e.g., Rust's ownership system ↔ C manual memory management)
- A term used in the current file has an entry in `SHARED/glossary.md`
- A module's learning objectives overlap significantly with another module in a different topic

### When NOT to Add a Cross-Link

Do not add cross-links:

- To topics that do not yet exist in the repository (create a stub first, or use a TODO comment)
- To external URLs (use `RESOURCES.md` for those)
- Excessively — if every other word is a link, readers stop clicking any of them. Link concepts, not every mention of a word

### How to Add a Cross-Link

1. Identify the target file and the relevant heading anchor
2. Add a wiki-link at the appropriate point in the prose: `[[rust#ownership]]`
3. Run `./SCRIPTS/lint.sh` to verify the link resolves
4. Consider adding a reciprocal link in the target file pointing back to your file

### Cross-Link Format in Context

```markdown
Rust's ownership system (see [[rust#ownership]]) addresses the same memory safety
problems that C++ solved with RAII (see [[cpp#raii]]). Both approaches eliminate
entire classes of bugs at compile time rather than relying on runtime checks.
```

---

## Citation Standards

All claims in leaps that are not common knowledge must be supported by a citation. This is especially important for:

- Historical claims ("Go was designed at Google in 2007...")
- Performance claims ("This approach is O(n log n)...")
- Design rationale ("The Rust team chose ownership over garbage collection because...")
- Specifications ("According to the C++ standard, undefined behavior occurs when...")

### Books

```markdown
Kernighan, B. W., & Ritchie, D. M. (1988). *The C Programming Language* (2nd ed.). Prentice Hall.
```

### Academic Papers

```markdown
Hoare, C. A. R. (1978). Communicating sequential processes. *Communications of the ACM*, 21(8), 666–677. https://doi.org/10.1145/359576.359585
```

### Official Documentation

```markdown
The Rust Reference. (2024). *Ownership*. The Rust Programming Language. https://doc.rust-lang.org/reference/ownership.html (accessed 2026-05-22)
```

### Videos / Talks

```markdown
Pike, R. (2012). *Concurrency is not parallelism* [Talk]. GopherCon. https://www.youtube.com/watch?v=oV9rvDllKEg
```

### Where to Put Citations

- **In-line:** Brief references in the body of a file using author-date format: "(Knuth, 1997)"
- **`RESOURCES.md`:** The full citation in a numbered reference list
- **`SHARED/references.md`:** For sources cited in more than one topic, add them here

---

## Pull Request Process

### Before Opening a PR

Run the full checklist in [Educational Quality Review Checklist](#educational-quality-review-checklist). Fix all linter errors. Make sure every file you modified matches the naming and structure conventions in this guide.

### PR Title Format

Titles must be descriptive and follow this pattern:

```
[type]: [scope] — [brief description]
```

| Type | When to Use |
|---|---|
| `content` | Adding or significantly expanding topic/module content |
| `fix` | Correcting errors, broken links, or wrong information |
| `exercise` | Adding or improving exercises |
| `test` | Adding or improving module tests |
| `tooling` | Scripts, validators, CI configuration |
| `docs` | CONTRIBUTING.md, AGENTS.md, README.md changes |
| `template` | Template file changes |
| `chore` | Minor cleanup, formatting, renaming |

**Examples:**
```
content: rust/module-05 — add traits and generics module
fix: python/module-03 — correct output in control flow examples
exercise: go/module-02 — add debugging exercises
docs: contributing — document the Zensical book workflow
```

### PR Description Requirements

Every PR must include:

1. **Summary** — What does this PR add or change, and why?
2. **Scope** — Which files were modified? Which topic and modules are affected?
3. **Testing** — Did you run `./SCRIPTS/lint.sh`? Did you run the examples? Did `zensical build --clean` succeed?
4. **Checklist** — Confirm all items in the [Educational Quality Review Checklist](#educational-quality-review-checklist)
5. **Related issues** — Reference any issues this closes: `Closes #42`

### Review Criteria

Reviewers will assess:

- **Correctness:** Is all technical content accurate? Are examples verified?
- **Completeness:** Does the module/exercise/test meet the minimum requirements in this guide?
- **Quality:** Does the explanation depth meet the "WHY, not just WHAT" standard?
- **Structure:** Does every file follow the naming conventions and templates?
- **Cross-links:** Are relevant connections to other topics/modules present?
- **Lint:** Does `./SCRIPTS/lint.sh` pass with no errors?

### Review Response

- Respond to all reviewer comments, even if only to acknowledge ("Good catch, fixed in [commit]")
- Do not dismiss review threads unless the reviewer approves the dismissal
- If you disagree with a reviewer's suggestion, explain your reasoning; do not simply ignore it
- PRs that go 14 days without author response will be closed (and can be reopened)

---

## Code of Conduct

### Respectful Collaboration

leaps is a learning environment. Everyone here — from beginners asking basic questions to experts contributing advanced modules — deserves to be treated with respect.

**Required:**
- Critique ideas and content, not people
- Give specific, actionable feedback ("This example doesn't compile because X" not "This is wrong")
- Acknowledge when you do not know something
- Welcome questions from learners at all levels

**Not tolerated:**
- Condescending language ("Obviously...", "You should know this by now...")
- Dismissing contributions for being imperfect — a 70% complete module is better than none
- Discouraging learners from asking questions publicly
- Personal attacks, harassment, or discriminatory language of any kind

### Constructive Feedback

When reviewing a PR or responding to a question, follow this structure:

1. **Acknowledge** what is good about the contribution first
2. **Identify** specific issues with specific evidence
3. **Suggest** a concrete improvement, not just "this is wrong"
4. **Explain** why the suggestion makes the content better for learners

### Intellectual Honesty

- If you made a mistake in content you contributed, acknowledge it and fix it
- If you are not certain about a claim, mark it explicitly: "> [!NOTE]\n> This is the author's interpretation based on [source]; see the original for authoritative guidance."
- Do not present your mental model as definitive truth if it is one of several valid perspectives

---

## Educational Quality Review Checklist

Complete this checklist before opening a PR. Every unchecked item is a reason for the PR to be returned for revision.

### Content

- [ ] Every technical claim is accurate and verifiable
- [ ] Every claim that is not common knowledge has a citation
- [ ] Explanations answer WHY, not just WHAT and HOW
- [ ] No placeholder text remains (no `{{PLACEHOLDER}}`, "TODO", "Fill in later")
- [ ] Historical context is included where relevant
- [ ] Real-world applications are named concretely

### Examples

- [ ] Every code example compiles and runs without modification
- [ ] Every code example includes the language identifier in the code fence
- [ ] Every code example is explained (not just shown)
- [ ] Examples progress from simple to complex within the file

### Structure

- [ ] File follows the correct template from `TEMPLATES/`
- [ ] Headings follow the H1 > H2 > H3 hierarchy (no skipped levels)
- [ ] A table of contents is present (for files with more than 3 H2 sections)
- [ ] All files use the correct UPPERCASE.md or lowercase.ext naming
- [ ] All folder names use lowercase-hyphens

### Cross-Links

- [ ] All wiki-links resolve (verified by `./SCRIPTS/lint.sh`)
- [ ] Related concepts in other topics are linked
- [ ] Shared glossary terms are linked where first introduced in the module

### Exercises (if applicable)

- [ ] At least five exercises are present
- [ ] Exercises include a mix of types (recall, conceptual, coding, debugging, design)
- [ ] Every exercise has a solution or detailed hints
- [ ] Exercises are labeled with difficulty level

### Tests (if applicable)

- [ ] TEST.md follows the four-tier difficulty structure
- [ ] ANSWERS.md contains the complete answer key with explanations
- [ ] Answer key explains WHY each answer is correct
- [ ] Point values are assigned to every question
- [ ] Total points are stated

### Book Build

- [ ] Content is Markdown only (no `.ipynb` files)
- [ ] `zensical build --clean` completes without errors
- [ ] New pages render correctly (code blocks, Mermaid diagrams, callouts, relative links)
- [ ] All cell outputs are cleared before committing

### Resources

- [ ] At least three resources are listed in RESOURCES.md
- [ ] All resource links are live and accessible
- [ ] All citations include the minimum required fields (author, title, year)

### Lint

- [ ] `./SCRIPTS/lint.sh` passes with zero errors
- [ ] No broken wiki-links
- [ ] No broken relative file links

---

*Thank you for contributing to leaps. Every improvement, however small, makes the knowledge base richer for every learner who comes after you.*
