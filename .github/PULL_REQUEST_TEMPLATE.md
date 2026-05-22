## Type of Change

<!-- Check all that apply. -->

- [ ] New topic (new directory under `TOPICS/`)
- [ ] New module (new module inside an existing topic)
- [ ] Content improvement (corrections, clarifications, additional depth)
- [ ] Bug fix (broken link, wrong structure, invalid notebook)
- [ ] Script / tooling change (`SCRIPTS/`, `tools/`)
- [ ] Template update (`TEMPLATES/`)
- [ ] GitHub Actions / CI change (`.github/workflows/`)

---

## Topic / Module Affected

<!-- Provide the path(s) affected by this PR. -->

**Path:** `TOPICS/` or `SCRIPTS/` or other:

---

## Summary of Changes

<!-- Describe what this PR adds or changes and why. Be specific. -->

### What changed

-

### Why it changed

-

---

## Educational Quality Checklist

> This checklist applies to any PR that adds or modifies content in `TOPICS/`.
> Check each item that is relevant to this PR. Leave unchecked items that do not apply.

### Content Depth

- [ ] Content has depth beyond surface-level summaries — concepts are explained, not just named
- [ ] Practical, runnable examples are included where applicable
- [ ] Cross-links are added wherever a concept appears in another leaps topic
- [ ] All references are real and verifiable — no hallucinated book titles, authors, or URLs

### Exercises and Assessments

- [ ] Exercises are included (required when adding module content)
- [ ] Exercises span at least two difficulty levels (e.g., easy + medium)
- [ ] Test questions are included (required when adding module content)
- [ ] Test questions cover the full range of Easy / Medium / Hard / Expert

### Structure and Formatting

- [ ] Markdown structure follows `CONTRIBUTING.md` standards
- [ ] Heading hierarchy is correct (no skipped levels, one H1 per file)
- [ ] All code blocks have a language annotation (` ```python `, ` ```rust `, etc.)
- [ ] No trailing whitespace, no Windows line endings

### Notebooks (if applicable)

- [ ] Notebook runs top-to-bottom without errors in a clean kernel
- [ ] Notebook outputs are cleared before committing
- [ ] Notebook is linked from the corresponding module's `README.md`

### Links

- [ ] All internal links (`[[wiki-links]]` and `[text](path)`) have been tested
- [ ] No links point to files or sections that do not yet exist

---

## Testing Done

<!-- Describe any validation you ran before opening this PR. -->

- [ ] Ran `python SCRIPTS/validate_structure.py` — no errors
- [ ] Ran `python SCRIPTS/find_broken_links.py` — no broken links
- [ ] Ran `python SCRIPTS/validate_notebooks.py` — no invalid notebooks (if applicable)
- [ ] Opened changed files in Obsidian and verified rendering (if applicable)

**Notes:**

---

## Screenshots

<!-- If this PR changes rendered output (diagrams, notebook output, Obsidian rendering),
     attach before/after screenshots here. Delete this section if not applicable. -->

---

## Related Issues

<!-- Link any issues this PR closes or relates to. -->

Closes #
Related to #
