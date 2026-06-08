# leaps Architecture Decisions

This document records the key design decisions behind **leaps** (Learning Environment for Any Progressive Subject): why the system is structured the way it is, what alternatives were considered, and what trade-offs were accepted. It is intended for contributors, AI agents that extend the repository, and anyone curious about the reasoning behind the structure.

---

## 1. Markdown-First

### Decision

All learning content is stored as plain Markdown files. Code, exercises, questions, grades, and notes are all Markdown or Markdown-adjacent (`.toml`/`.yml` config). There is no proprietary database, no CMS, and no binary format for text content.

### Rationale

**Human-readable at rest.** Open any file in any editor — from `cat` in a terminal to Typora to VS Code — and the content is immediately legible. No tool is required to read your own notes.

**Git-native.** Plain text diffs meaningfully. You can `git log` the history of a concept, `git blame` a specific answer, or `git bisect` to find when a module's test scores started dropping. Binary formats make version control nearly useless.

**AI-friendly.** Large language models process Markdown trivially. An AI agent can read a module file, understand its structure from the headings, extract frontmatter, and generate compliant new content without any parsing layer beyond string operations.

**Portable.** No vendor lock-in. The entire knowledge base can be moved to a different tool (Obsidian → VS Code → Notion → a static site) without a migration step. The content is the content.

**Offline-capable.** No API calls needed to read or write notes. The full knowledge base works on an airplane.

### Alternatives Considered

- **Notion / Confluence:** Proprietary, requires internet, poor git integration, opaque export formats.
- **SQLite database:** Queryable but not human-readable at rest; merging concurrent writes requires schema migrations.
- **LaTeX:** Superior for mathematical typesetting but hostile to non-mathematicians and poor for incremental, conversational notes.

---

## 2. Folder Structure and Naming Conventions

### Decision

The repository uses a flat-ish, intentional hierarchy:

```
leaps/
├── TOPICS/          # One directory per subject (all caps = top-level concern)
├── SHARED/          # Cross-topic concepts and references
├── TEMPLATES/       # Canonical file templates
├── SCRIPTS/         # Automation scripts
├── PROMPTS/         # AI prompt templates
├── environments/    # Reproducible setup
├── tools/           # Editor and tool configurations
├── assets/          # Images and diagrams
├── zensical.toml    # Zensical book configuration (docs_dir = TOPICS/)
└── docs/            # Repository meta-documentation
```

Inside each topic:

```
TOPICS/<topic>/
├── README.md            # Module index and status
├── module-<n>-<slug>.md # Ordered learning modules
├── questions.md         # Append-only question log
├── grades.md            # Append-only test records
└── exercises/           # Coding exercises
```

### Rationale

**ALL-CAPS directories are human signals.** `TOPICS/`, `SHARED/`, `TEMPLATES/`, `SCRIPTS/`, and `PROMPTS/` appear at the top of any `ls` output on case-sensitive filesystems (Linux/macOS) and stand out visually. They are the primary concerns of the repository. Lower-case directories (`tools/`, `environments/`, `assets/`) are supporting infrastructure.

**Numbered modules enforce order.** `module-01-introduction.md` before `module-02-types.md` creates a curriculum that is readable from directory listing alone, without opening any file. AI agents generating new modules can infer the next sequence number from the existing files.

**Consistent structure enables automation.** Because every topic follows the same template, scripts can blindly locate `questions.md`, `grades.md`, and module files without topic-specific configuration. The structure is the API.

**Separation of SHARED and TOPICS.** Concepts that appear in multiple topics (memory management, concurrency, error handling) live in `SHARED/concepts/` rather than being duplicated or arbitrarily assigned to one topic. This models the reality that knowledge is a graph, not a tree.

### Alternatives Considered

- **Flat structure (all files in one directory):** Does not scale past ~50 files. Navigation becomes painful.
- **Deep nesting (TOPICS/category/subcategory/topic/):** Over-organization prevents discovery and makes cross-linking paths long and fragile.
- **Database-driven structure (JSON manifest files):** Adds indirection. The filesystem is already a perfectly good manifest.

---

## 3. Wiki-Links (Obsidian-Compatible)

### Decision

Cross-references between notes use `[[wiki-link]]` syntax (e.g., `[[python]]`, `[[memory-management]]`). This is compatible with Obsidian natively and with Foam in VS Code.

### Rationale

**Bidirectional linking is a first-class feature.** Standard Markdown links (`[text](path)`) are one-directional. Wiki-links enable backlink graphs — you can see not just what a note links to but what links *to* it. This is essential for a knowledge graph that grows over time.

**Lower friction than path-based links.** Writing `[[python]]` is faster and more resilient than `[Python](../../TOPICS/python/README.md)`. When files move, wiki-link resolution engines handle the update; relative paths break silently.

**Readable inline.** In raw Markdown, `[[concurrency]]` communicates intent clearly. A reader skimming the raw file understands there is a related concept named "concurrency" without needing to parse a URL.

**Ecosystem support.** Obsidian, Foam, Logseq, and several static site generators all support wiki-link syntax. Choosing it keeps options open.

### Alternatives Considered

- **Standard relative links only:** More portable across tools that do not support wiki-links, but higher maintenance cost and no backlink support.
- **Tags only:** Tags group content but do not establish directed relationships between specific notes.
- **Both, inconsistently:** Rejected — consistency matters for automated graph traversal.

---

## 4. Published as a Zensical Book

### Decision

The learning material is published as a [Zensical](https://zensical.org) book — the modern static-site generator from the Material for MkDocs team. The Markdown in `TOPICS/` is the single source of truth, and Zensical renders it into a searchable static site that is deployed to GitHub Pages.

The publishing pipeline is:

```
zensical.toml  →  docs_dir = TOPICS/  →  zensical build --clean  →  site/  →  GitHub Pages
```

- **`zensical.toml`** at the repository root configures the book. Its `docs_dir` points at `TOPICS/`, so the rendered site is exactly the course content.
- **Navigation is implicit**, derived from the `TOPICS/` directory tree. Each directory's `README.md` becomes that section's index page; no hand-maintained nav file is required.
- **`zensical build --clean`** renders the site into the `site/` output directory.
- **`.github/workflows/docs.yml`** runs that build on every push to `main` (i.e. when a PR is merged) and deploys the result to GitHub Pages.

The book intentionally exposes **only** the course index (`TOPICS/README.md`) and the courses themselves. Repo tooling (`SCRIPTS/`, `PROMPTS/`, `TEMPLATES/`, `docs/`) is excluded from the published site.

### Rationale

**Zero content migration.** Because Zensical reads the same Markdown the repository already stores, publishing is a configuration concern, not a content concern. The content is the content — see Decision 1.

**Implicit navigation tracks the structure.** The directory tree already encodes the curriculum order (numbered modules, per-topic READMEs). Deriving the nav from that tree means the published book stays in sync with the repository automatically, with no separate nav file to drift.

**Automated, reproducible deployment.** GitHub Pages publishing via a workflow means the live book always reflects `main`. There is no manual publish step to forget.

**Local preview matches production.** Contributors run `pip install zensical` and then `zensical serve` (http://localhost:8000) to preview exactly what readers will see, or `zensical build` to produce the static site locally.

### Note on Notebooks

> [!NOTE]
> Earlier versions of leaps embedded Jupyter notebooks (`.ipynb`) alongside Markdown modules for interactive code. Notebooks were **removed entirely** in favour of the Zensical book: their large JSON diffs, merge conflicts, and the extra build tooling they required complicated a clean, automated GitHub Pages deployment. Runnable code now lives in the prose modules and `exercises/` directories as plain Markdown and source files.

---

## 5. Python for Scripts

### Decision

All automation scripts in `SCRIPTS/` and helper utilities are written in Python.

### Rationale

**Ubiquitous in the target audience.** leaps is a learning tool used by people who are, by definition, learning programming. Python is the most accessible systems scripting language for that audience.

**Available in every environment.** All leaps environments (venv, Docker, devcontainer, conda) install Python. No additional tooling is needed to run scripts.

**Readable by AI agents.** LLMs have the strongest Python competency of any scripting language. AI-generated scripts are more likely to be correct and idiomatic in Python than in Bash or Ruby.

**Consistency.** Using Python everywhere means contributors do not need to context-switch between shell scripting idioms, Python idioms, and JavaScript idioms for different tasks.

### Alternatives Considered

- **Bash:** Portable and fast, but error handling is poor and readability degrades quickly past ~50 lines.
- **JavaScript/Node.js:** Not pre-installed in all environments; adds a runtime dependency.
- **Go:** Excellent for compiled tools, but compile step adds friction for quick scripts.

---

## 6. Append-Only for Questions and Grades

### Decision

`questions.md` and `grades.md` files within each topic are append-only. New entries are added at the bottom; old entries are never edited or deleted.

### Rationale

**Honest record of learning.** Editing a past answer to look correct is the learning equivalent of erasing a mistake rather than learning from it. The history of what you did not know is as valuable as the history of what you learned.

**Git-friendly.** Append-only files produce clean, readable diffs: each commit adds lines, never modifies existing ones. You can `git log -p` a grades file and watch scores evolve over time.

**Supports spaced repetition analysis.** If you want to know when you first encountered a concept and how your recall has changed, you need the full timeline. Overwriting destroys this.

**Audit trail for AI agents.** When an AI agent generates test questions, records scores, or logs answers, the append-only constraint ensures the agent cannot accidentally modify past records — only extend them.

### Alternatives Considered

- **Mutable records (edit in place):** Simpler for humans who want to "fix" their notes, but destroys the learning history.
- **Database records with timestamps:** Better for querying, but loses the git-native advantage.
- **Separate dated files (grades-2025-06-10.md):** Avoids the single-file-gets-large problem but makes cross-date analysis harder.

---

## 7. Design Principles

These principles inform every decision in the repository, including future decisions not yet made:

### Human-Readable

The repository must be fully understandable from a terminal with no special software installed. `ls`, `cat`, and `grep` are sufficient to navigate the entire knowledge base.

### AI-Friendly

Every file follows a consistent schema. AI agents can read, parse, extend, and cross-link content without custom parsers or special instructions beyond the templates and the AGENTS.md contract.

### Git-Friendly

Plain text, meaningful diffs, append-only logs, and consistent naming make every change reviewable, reversible, and attributable.

### Offline-Capable

No network requests are required to read, study, or extend content. The full knowledge base works without internet access.

### Composable

Topics, shared concepts, templates, and scripts are independently useful. A contributor can add a new topic without touching shared infrastructure. A script can process any topic without topic-specific configuration.

### Honest

Learning records (grades, questions, answers) are never modified retroactively. The system rewards honesty about what you do and do not know.

---

## 8. Future Considerations

### Static Site Publishing

This is now implemented — see Decision 4. The knowledge base is published as a [Zensical](https://zensical.org) book (`zensical.toml` → `docs_dir = TOPICS/`), built with `zensical build --clean` and deployed to GitHub Pages by `.github/workflows/docs.yml` on every push to `main`. As predicted, it required only configuration and zero content changes. Remaining refinements (custom theming, search tuning, versioned releases) are incremental configuration work.

### Graph Visualization

The wiki-link graph can be exported and visualized. Obsidian does this natively; a Python script using `networkx` and `pyvis` could generate an interactive HTML graph from the `[[link]]` references in all Markdown files.

### Automated Spaced Repetition

The frontmatter fields (`next_review`, `review_interval`, `ease`) documented in the Dataview queries support a manual SRS system. A future script could automatically update these fields after self-reported review sessions, or integrate with Anki via the genanki Python library.

### Multi-Language Content

Most topics currently assume Python for code examples. A `language` frontmatter field on code-heavy modules could allow the same topic to have parallel modules in multiple languages (e.g., `module-03-loops-python.md`, `module-03-loops-rust.md`).

### CI Validation

A GitHub Actions workflow can validate:
- All `[[wiki-links]]` resolve to existing files.
- All Markdown files pass markdownlint rules.
- The Zensical book builds cleanly (`zensical build --clean`) with no broken references.
- Required frontmatter fields are present on all module files.

This enforces the structural contract automatically, reducing the review burden on human contributors.
