---
name: Generate Module
category: Content Creation
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name (must exist in TOPICS/)
    example: rust
  - name: MODULE_NUMBER
    description: The zero-padded module number
    example: 05
  - name: MODULE_NAME
    description: The human-readable module title in Title Case
    example: Traits and Generics
---

# Generate Module

## Description

Generates a complete, production-quality module within an existing topic. The module is fully coherent with the modules that precede it — the agent reads prior modules before writing to ensure correct progression, appropriate prerequisite references, and consistent terminology.

After running this prompt, the target module will have all eight standard files populated with substantive content, a complete set of exercises, a full test with answer key, and curated resources.

## Usage

1. Copy the prompt text below
2. Replace `[TOPIC_NAME]`, `[MODULE_NUMBER]`, and `[MODULE_NAME]` with your values
3. Paste into your AI assistant with access to this repository
4. Review the generated content for technical accuracy before committing

## Prompt

```
You are a leaps module generation agent. Your task is to generate a complete, production-quality learning module.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- MODULE_NUMBER: [MODULE_NUMBER]
- MODULE_NAME: [MODULE_NAME]

## Step 1: Read Context

Before generating anything, read the following:

1. `TOPICS/[TOPIC_NAME]/README.md` — understand the full topic structure, the module's position in the sequence, and the stated learning objectives for this module
2. All previous module README.md files — understand exactly what has been taught already, what terminology has been established, and what the learner knows coming into this module
3. `TOPICS/[TOPIC_NAME]/PROGRESS.md` — understand the learner's current state
4. `SHARED/glossary.md` and `SHARED/concepts.md` — note any cross-topic concepts relevant to this module
5. `CONTRIBUTING.md` — confirm all standards you must follow
6. `TEMPLATES/module/README.md` — the template structure you will follow

Also check: does the module directory `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/` already exist? If it does, read all existing files before overwriting anything. If a file has non-template content, do NOT overwrite it — append to it or skip it and note this in your response.

## Step 2: Determine Module Scope

Based on the topic README and the preceding modules, determine:

1. **What concepts this module introduces** — list them explicitly. No concept should appear in this module if it was already covered in depth in a prior module (references are fine, but not re-teaching).
2. **What terminology this module assumes** — all terms used without definition must have been defined in prior modules or in SHARED/glossary.md.
3. **Where this module fits in the learning arc** — Beginner / Intermediate / Advanced / Expert based on its position in the sequence.
4. **The most important mental model to convey** — what single insight, if grasped, makes the rest of the module click?

Document this scope plan before writing any files. It will be the first section of your output.

> [!IMPORTANT]
> **If this is the final module of the topic, it must be the Capstone Project module** (see
> AGENTS.md §5). A capstone module is build-oriented, not lecture-oriented: its `README.md` is a
> project brief (goal, requirements, suggested architecture, milestones, acceptance criteria) and
> its `EXERCISES.md` holds project milestones/checkpoints rather than drills. It **must** include a
> **Help / Getting Unstuck** section with staged, collapsible hints and pointers back to the
> relevant teaching modules — but it must **not** contain a complete copy-paste solution. The
> learner builds the project themselves; the help only unblocks them. State this explicitly in the
> module. Also confirm the topic as a whole reaches expert ("2+ years professional") depth — if the
> module you are writing is the last teaching module before the capstone, it should be carrying the
> learner to that expert ceiling.

## Step 3: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/README.md

This is the primary learning document. Write it to textbook quality.

**Required structure:**

### Module Header
```markdown
# Module [MODULE_NUMBER]: [MODULE_NAME]

**Topic:** [[TOPIC_NAME]]
**Difficulty:** [Beginner|Intermediate|Advanced|Expert]
**Estimated time:** [N–M hours]
**Prerequisites:** [Previous module wiki-links and any external prerequisites]
```

### Table of Contents
Link to every H2 section in the file.

### Overview (H2)
- What this module covers (2–3 paragraphs)
- Why these concepts matter — the real-world consequence of understanding or not understanding them
- How this module connects to what came before (link to previous module) and what comes after (mention next module)

### Learning Objectives (H2)
5–8 measurable, action-verb objectives:
- Not "Understand X" — write "Explain X by describing its mechanism and consequence"
- Not "Know Y" — write "Implement Y given Z constraints"
- Cover the range from recall ("Define...") through synthesis ("Design a system that...")

### Historical and Conceptual Background (H2)
Why do these concepts exist? What problem did they solve? Who invented them and why?
- Minimum 3 paragraphs
- Include specific dates, names, and original motivations
- Connect the history to why the design is the way it is today

### Core Concepts (one H2 per major concept, minimum 3 major concepts)

For each concept:

**H2: [Concept Name]**

*H3: What It Is*
Precise definition. If the concept has a formal definition (a mathematical one, a specification, a language standard), quote it and then explain it in plain English.

*H3: How It Works*
The mechanism. Step by step if applicable. Use Mermaid diagrams for flows and structures. Use worked examples for mathematical concepts. Do not assume the reader can infer the mechanism from the definition alone.

*H3: Why It Matters*
Real-world consequences. What goes wrong if you misuse this concept? What becomes possible when you master it? Name at least two specific real-world scenarios.

*H3: In Practice*
Working code example or worked mathematical example. Rules:
- Must compile and run without modification (for code)
- Must be verifiable by hand (for math)
- Must include inline comments explaining non-obvious steps
- Must have a prose explanation before AND after the example
- Must show at least one common mistake and why it fails

### Common Mistakes and Gotchas (H2)
Minimum 4 entries. For each:
- Name the mistake (as a heading)
- Show the incorrect version (as a code block or example)
- Explain why it is wrong
- Show the correct version
- Explain why the correct version is right

Use `> [!WARNING]` callouts for mistakes that are especially dangerous or common.

### Mental Models (H2)
1–3 analogies or mental models that give intuition for the hardest concepts in this module.
A mental model is good if: (a) it is memorable, (b) it correctly predicts behavior in common cases, (c) its limitations are stated explicitly so the reader knows when the analogy breaks down.

### Connections to Other Topics (H2)
- List concepts in this module that appear in other leaps topics
- Add wiki-links: `[[other-topic#relevant-section]]`
- Brief explanation of the connection (1–2 sentences per connection)
- Minimum 2 connections (if the topic has related leaps topics)

### Summary (H2)
Bullet-point recap of the most important ideas. A learner who reads only this section before a test should be able to pass the Easy questions.

### What's Next (H2)
- Link to the next module: `[[TOPIC_NAME/module-NN-name]]`
- Preview the 2–3 concepts the next module will introduce and why they follow naturally from this module

## Step 4: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/NOTES.md

Write a set of structured study notes for this module. These are different from the README — they are more concise, bulleted, and reference-style. A learner should be able to review NOTES.md in 10 minutes and recall the key points of the module.

Format:
```markdown
# Notes: Module [MODULE_NUMBER] — [MODULE_NAME]

_Last updated: [DATE] | These notes are auto-generated and can be extended freely._

---

## Key Concepts at a Glance
[3–5 bullets per major concept: the single most important thing to know about each]

## Concept Map
[Mermaid diagram showing how the concepts in this module relate to each other]

## Key Terms
[Term: one-sentence definition, with wiki-link to glossary if defined there]

## Code Patterns to Remember
[The 2–5 most reusable code patterns introduced in this module]

## Common Errors Reference
[Quick table: error | cause | fix]

## Questions to Keep in Mind
[3–5 questions a learner should be able to answer after mastering this module]
```

## Step 5: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/EXERCISES.md

Write 8–12 exercises following the CONTRIBUTING.md exercise format exactly.

Distribution:
- 1–2 Recall exercises (Beginner): define a term, name something, list items
- 2–3 Conceptual exercises (Beginner–Intermediate): explain why, predict behavior, compare/contrast
- 2–3 Coding exercises (Intermediate): implement something working
- 1–2 Debugging exercises (Intermediate): find and fix a bug
- 1 Design exercise (Intermediate–Advanced): design a solution given constraints
- 1 Research exercise: investigate something not explicitly covered in the module

Every exercise must have:
- Descriptive title
- Difficulty label
- Concept being tested
- Clear instructions
- Solution inside `<details>` with explanation

Number exercises sequentially: `### Exercise 1:`, `### Exercise 2:`, etc.

## Step 6: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/TEST.md

Write a test with the following structure and point distribution:

```markdown
# Test: Module [MODULE_NUMBER] — [MODULE_NAME]

**Topic:** [TOPIC_NAME]
**Total points:** [SUM] base + [BONUS] bonus
**Estimated time:** [N] minutes
**Instructions:** Answer all questions in the spaces provided. For coding questions, write code that compiles and runs correctly. Show reasoning for partial credit on essay questions.

---

## Section 1: Easy ([N] points)

[4–5 questions at 1–2 pts each]
Question types: multiple choice, true/false with justification, fill-in-the-blank

---

## Section 2: Medium ([N] points)

[3–4 questions at 2–3 pts each]
Question types: short answer, code reading (predict output), concept explanation

---

## Section 3: Hard ([N] points)

[2–3 questions at 3 pts each]
Question types: code writing, debugging, scenario analysis

---

## Section 4: Expert ([N] points)

[1–2 questions at 4–5 pts each]
Question types: design, architecture, essay, synthesis

---

## Bonus

[2–3 bonus questions worth 2–3 pts each]
These may exceed the base total. Bonus points are added directly to your score.
```

Total base points should be 20–30. Include space for the learner to write answers.

## Step 7: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/ANSWERS.md

```markdown
# Answer Key: Module [MODULE_NUMBER] — [MODULE_NAME]

> [!IMPORTANT]
> This file contains the full answer key. Attempt the test before reading this file.
> Grading records will be appended to the bottom of this file by the grading agent.

---

## Answer Key

### Section 1: Easy

**Q1.** [Answer]
*Explanation:* [Why this is correct — 1–3 sentences]
*Partial credit:* [If applicable]

[Continue for all questions...]

---

## Grading Rubric

### Short Answer Rubric
[Point allocation for partial credit: what earns full credit, 50% credit, 0 credit]

### Code Writing Rubric
[What makes a code answer earn full, partial, or zero credit]

### Essay Rubric
[Criteria for full credit on design and synthesis questions]

---

## Grading Records

_Grading records are appended here by the grade-test agent. Do not edit manually._
```

## Step 8: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/RESOURCES.md

Curate 6–10 resources specific to this module's content:
- At least 1 book chapter or section
- At least 1 official documentation page
- At least 1 video or talk
- At least 1 interactive exercise or playground (if available for this topic)

For each resource, include:
- Full citation or link
- One-sentence description of what it covers
- Difficulty level
- Why it was chosen for this specific module (what it adds that the README does not cover)

## Step 9: Write TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/PROJECTS.md

Write 3–4 project ideas scoped to this module's content:
- 1 Beginner project: can be completed using only this module's concepts
- 1–2 Intermediate projects: require integrating this module with prior modules
- 1 Advanced/stretch project: requires going beyond the module's content into territory covered in later modules

For each project:
- Title
- Description (2–3 sentences)
- Learning objectives (what the project reinforces)
- Acceptance criteria (how you know it is complete)
- Suggested tools or libraries

## Step 10: Update Parent Files

After generating all module files, update:

**TOPICS/[TOPIC_NAME]/README.md:**
- Change the module's status from "stub" to "created" in the module list table
- Verify the module description in the table matches what was actually generated

**TOPICS/[TOPIC_NAME]/PROGRESS.md:**
- Add the module to the checklist if it is not already there
- Update the total possible points if needed

## Step 11: Cross-Linking Pass

After all files are written:
1. Re-read the module README
2. For every concept that has an entry in SHARED/glossary.md or appears in another leaps topic: add the wiki-link if it is not already present
3. List all cross-links added in your response summary

## Output Format

Structure your response:

1. **Module Scope Plan** — the analysis from Step 2
2. **Files Generated** — list of all file paths
3. **Cross-Links Added** — list of all wiki-links inserted
4. **Review Notes** — anything you were uncertain about that a human should verify
5. **[File Path]** — full content of each file, clearly headed

For large outputs, you may generate files sequentially and ask for confirmation before proceeding to the next file.
```

## Examples

**Generate the third module for a Rust topic:**
```
TOPIC_NAME: rust
MODULE_NUMBER: 03
MODULE_NAME: Ownership and Borrowing
```

**Generate a calculus module:**
```
TOPIC_NAME: calculus
MODULE_NUMBER: 04
MODULE_NAME: The Chain Rule
```

**Generate an advanced Go module:**
```
TOPIC_NAME: go
MODULE_NUMBER: 09
MODULE_NAME: Concurrency Patterns
```

## Notes

- Always read prior modules before generating. The most common failure mode is teaching something already covered, or using terminology not yet introduced.
- For code-heavy topics (programming languages), every code example should be runnable. If you cannot verify it, mark it with `# [UNVERIFIED — review before committing]`.
- For mathematics-heavy topics, every worked example should show all steps. Do not skip algebraic manipulations.
- The NOTES.md file is intentionally shorter and more reference-style than README.md. Do not duplicate the README — distill it.
- If the module directory already exists with partial content, read it first and only fill in the gaps. Do not overwrite human-authored content.
