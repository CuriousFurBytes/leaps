---
name: Knowledge Graph Update
category: Knowledge Graph
version: 1.0
parameters: []
---

# Knowledge Graph Update

## Description

Performs a comprehensive scan of all topics in the repository, finds conceptual connections that are not yet cross-linked, adds wiki-links at appropriate points in affected files, and updates `SHARED/concepts.md` and `SHARED/glossary.md` with new entries. This is the global version of `cross-reference.md` — it operates on the entire repository rather than two specific topics.

Run this prompt periodically (after adding new topics or modules) to keep the knowledge graph up to date and densely connected.

## Usage

This prompt has no parameters — it operates on the entire repository.

1. Copy the prompt text below
2. Paste into your AI assistant with access to this repository
3. This is a long-running operation — expect it to take time proportional to the number of topics and modules
4. Review the proposed changes before they are applied (the agent will list all changes before making them)

## Prompt

```
You are a leaps knowledge graph agent. Your task is to perform a comprehensive knowledge graph update across the entire repository.

## Step 1: Discovery — Read All Topics

Read the following:
1. `TOPICS/` directory listing — all topic names
2. For each topic: `TOPICS/[topic]/README.md`
3. For each topic with at least 2 modules: all module README.md files
4. `SHARED/concepts.md` — existing shared concepts
5. `SHARED/glossary.md` — existing glossary terms
6. `SHARED/references.md` — existing shared bibliography

Build a complete inventory:

**Topic Inventory:**
For each topic, extract:
- Topic name and one-sentence description
- Core concepts (list of concept names from section headings and definition blocks)
- Key terms (terms defined in the topic)
- External references (papers, books, people, systems referenced)
- Existing cross-links (wiki-links already present)

**Concept Registry:**
A consolidated list of all concepts across all topics, with:
- Concept name
- Which topic(s) and module(s) cover it
- Whether it is in SHARED/concepts.md already

## Step 2: Find Missing Connections

Compare concepts across topics to find relationships that are not yet linked.

Look for:

### Shared Concepts
Concepts that appear in multiple topics under different names or contexts:
- Same algorithm, different language (e.g., "map" in Haskell vs. Python vs. Rust iterators)
- Same pattern, different domain (e.g., "observer pattern" in software vs. "publish-subscribe" in networking)
- Same mathematical foundation (e.g., "function composition" in calculus and in functional programming)

### Prerequisite Relationships
Where understanding concept X in Topic A helps or is required for understanding concept Y in Topic B:
- Type theory → type systems in programming languages
- Linear algebra → machine learning feature spaces
- Automata theory → regular expressions
- Graph theory → algorithms, networking, database query optimization

### Contrast Pairs
Concepts across topics that illuminate each other by contrast:
- Manual memory management vs. garbage collection vs. ownership
- Mutable state vs. immutable data vs. pure functions
- Synchronous vs. asynchronous vs. concurrent vs. parallel execution

### Historical Lineage
Concepts where one is the descendant, evolution, or reaction to another:
- Go channels ← CSP (Communicating Sequential Processes, Hoare 1978)
- Rust ownership ← region-based memory management (Cyclone language)
- Modern type theory ← Church's lambda calculus

For each connection found:
- Name it
- Classify its type (Shared Concept / Prerequisite / Contrast / Lineage)
- Rate its strength (Strong / Medium / Weak)
- Identify the exact files and sections in each topic that should be linked

## Step 3: Classify Links by Priority

Sort all found connections into:

**Priority 1 (Must Fix):** Strong connections that are not linked at all — a learner reading one topic would benefit significantly from knowing about the other, and there is no current pointer.

**Priority 2 (Should Fix):** Medium connections that are not linked — valuable for most learners.

**Priority 3 (Nice to Have):** Weak connections or connections where there is already some linking but it could be improved.

Present this prioritized list to the user (or if operating autonomously, process Priority 1 and 2 only).

## Step 4: Generate SHARED/concepts.md Updates

For every Strong connection that involves a concept not already in `SHARED/concepts.md`, draft a new entry:

```markdown
## [Concept Name]

**Category:** [Algorithm | Pattern | Principle | Mathematical Object | System Concept | Language Feature]
**First formalized:** [Year, by whom — if known]

**Core idea:** [2–3 sentences describing the concept at its most abstract, domain-independent level]

### Manifestations

| Topic | Manifestation | Notes |
|---|---|---|
| [[topic-a]] | [How it appears in Topic A] | [What is unique about this manifestation] |
| [[topic-b]] | [How it appears in Topic B] | [What is unique about this manifestation] |

### Key Differences Between Manifestations

[2–4 sentences explaining what varies across the topics — what is essential vs. incidental]

### Why Understanding One Deepens the Other

[1–2 sentences explaining the pedagogical value of knowing both manifestations]

### References

- [[topic-a#relevant-section]]
- [[topic-b#relevant-section]]
```

## Step 5: Generate SHARED/glossary.md Updates

For each term that:
- Appears in 3 or more topics
- Is defined differently in different topics
- Is a foundational term that all topics in the repository use

Draft a new glossary entry:

```markdown
## [Term]

**Definition:** [Precise, domain-neutral definition]

**Plain English:** [What this means without jargon]

**In different contexts:**
- **[Topic A]:** [How the term is used in this topic — may differ from the base definition]
- **[Topic B]:** [...]

**See also:** [[related-term]], [[other-related-term]]

**Found in:** [[topic-a]], [[topic-b]], [[topic-c]]
```

Do not duplicate entries that already exist. For existing entries, check whether new topics have added new usages of the term that should be documented.

## Step 6: Plan the Link Additions

For every Priority 1 and Priority 2 connection from Step 3, plan exactly:

1. File A path
2. The sentence in File A where the link should be inserted (quote the sentence)
3. The modified version of that sentence with the wiki-link inserted
4. File B path
5. The sentence in File B for the reciprocal link
6. The modified version of that sentence

Verify that:
- Both files exist (not stubs)
- The target sections exist (not just the file)
- The wiki-link syntax is correct: `[[topic-name#heading-slug]]`

If a file is a stub or the target section does not exist, do not add the link. Record these as "deferred links" that should be added when the content is written.

## Step 7: Apply Changes

Apply changes in this order:

1. **SHARED/concepts.md** — add new entries
2. **SHARED/glossary.md** — add new entries
3. **Topic files** — add cross-links

For each file modification:
1. Read the current content
2. Apply only the planned change
3. Do not restructure or modify any existing content
4. Write the updated file

## Step 8: Validate All Links

After all changes, produce the full list of new wiki-links for validation:

```bash
# Run to verify all added links resolve:
./SCRIPTS/lint.sh --links-only
```

List every new wiki-link added so the user can verify them.

## Step 9: Generate the Update Report

Produce a comprehensive summary:

```markdown
# Knowledge Graph Update Report

**Date:** [DATE]
**Topics scanned:** [N]
**Modules scanned:** [N]
**Total concepts inventoried:** [N]

## New Connections Found

**Priority 1 (applied):** [N]
**Priority 2 (applied):** [N]
**Priority 3 (deferred):** [N]

## Changes Made

### SHARED/concepts.md
- [N] new entries added
- [N] existing entries updated
- New concepts: [list of concept names]

### SHARED/glossary.md
- [N] new entries added
- New terms: [list of terms]

### Topic Files Modified
[For each topic:]
**[topic-name]:** [N] links added in [N] files
  - [file path]: added link to [[target]] in [section]
  - ...

## Deferred Links
[Links that could not be added because the target is a stub:]
- [[link]] in [source file] → waiting for [topic/module] to be written
- ...

## Priority 3 Connections (Not Yet Applied)
[Brief description of weak connections found but not linked, for human review:]
- [Topic A]#[concept] ↔ [Topic B]#[concept]: [reason it was not applied]
- ...

## Recommendations

[Based on the scan, suggest:]
1. [Topics that would benefit most from being created next — they are missing pieces of the knowledge graph]
2. [Existing topics that would benefit most from expansion — they are referenced by many other topics but have thin content]
3. [Concepts that appear in many topics but have no SHARED/ entry — good candidates for future consolidation]
```

## Important Rules

1. **Read before modifying.** Every file must be read before any change is made to it.
2. **Preserve all content.** Only add to files — never delete or restructure.
3. **No broken links.** Only add wiki-links that resolve to real files with real sections.
4. **Batch cautiously.** For large repositories (10+ topics), process one topic pair at a time and pause for review.
5. **Do not over-link.** If adding a link would require rewriting a sentence significantly, skip it and add a standalone "See also" note at the end of the section instead.
6. **Strong connections only (by default).** Only apply Priority 1 and Priority 2 connections without explicit permission. Priority 3 connections should be listed but not applied.
```

## Examples

**Full repository update:**
No parameters — just run the prompt. The agent scans everything and applies Priority 1 and 2 connections.

**After adding a new topic:**
Run this prompt after creating a new topic. It will find all connections between the new topic and existing topics and link them bidirectionally.

**Periodic maintenance:**
Run monthly or after adding 3+ modules to any topic to keep the graph current.

## Notes

- This is the most expensive prompt in the library (longest runtime, most file reads and writes). Reserve it for periodic maintenance rather than running it after every small edit.
- The output report is as valuable as the changes themselves. Read it carefully — the "Recommendations" section often surfaces the highest-leverage next actions for growing the knowledge base.
- For repositories with 5+ topics, consider running this prompt in "dry-run" mode first: ask the agent to produce the update report and the planned changes without applying them, then review and approve before applying.
- The `SHARED/concepts.md` file is the most strategic artifact the knowledge graph update produces. A well-maintained concepts file gives any new learner (or AI agent) a bird's-eye view of how all the topics in the repository relate to each other.
