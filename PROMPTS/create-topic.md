---
name: Create Topic
category: Content Creation
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The directory-safe name for the topic (lowercase, hyphens, no spaces)
    example: linear-algebra
  - name: TOPIC_DESCRIPTION
    description: A 2–4 sentence description of what this topic covers and why it matters
    example: Linear algebra is the branch of mathematics studying vector spaces and linear transformations. It underpins machine learning, computer graphics, physics simulations, and cryptography.
  - name: DIFFICULTY_LEVEL
    description: Starting difficulty of this topic
    example: Intermediate
---

# Create Topic

## Description

Instructs an AI agent to create a complete new learning topic in the leaps repository — from directory structure through initial module content. The agent will scaffold all required files, fill them with substantive content (not placeholders), plan a complete module sequence, and make the topic immediately usable for learning.

This prompt creates a production-ready topic, not just an empty skeleton. After running it you should be able to start learning immediately from Module 1.

## Usage

1. Copy the prompt text below
2. Replace `[TOPIC_NAME]`, `[TOPIC_DESCRIPTION]`, and `[DIFFICULTY_LEVEL]` with your values
3. Paste into your AI assistant with access to this repository
4. Review the output for accuracy before committing

## Prompt

```
You are a leaps content agent. Your task is to create a complete new learning topic in the leaps repository.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- TOPIC_DESCRIPTION: [TOPIC_DESCRIPTION]
- DIFFICULTY_LEVEL: [DIFFICULTY_LEVEL]

## Step 1: Read and Understand the Repository

Before creating anything, read the following files completely:
- CONTRIBUTING.md — understand all content and naming standards
- TEMPLATES/topic/README.md — the template you will populate
- TEMPLATES/module/README.md — the module template you will use for Module 1
- SHARED/glossary.md — note any terms already defined that this topic will use
- SHARED/concepts.md — note any cross-topic concepts this topic relates to
- TOPICS/ directory listing — confirm [TOPIC_NAME] does not already exist

## Step 2: Plan the Topic

Before writing any files, plan the following and include this plan in your response as a "Topic Plan" section:

1. **Module Sequence (8–20 modules):** Name each module with its number, title, and a one-sentence description of what it covers. The sequence is **mandatory in shape** (see AGENTS.md §5):
   - **Module 0/01 — Introduction:** zero assumptions about the subject. Covers what it is, why it exists, and — when the subject has tooling — **installation and a working environment end-to-end** (compiler/interpreter/runtime/library, or, for non-software subjects, the orientation and reference materials a true beginner needs).
   - **Middle modules:** the full beginner → intermediate → advanced arc.
   - **Expert modules:** the topic must reach **expert / "2+ years working with this professionally"** depth — internals, performance, real-world architecture, tooling, debugging, idioms, and edge cases. Do not stop at intermediate.
   - **Final module — Capstone Project (required):** the learner builds a real, non-trivial project that synthesizes multiple earlier modules. It must include a **Help / Getting Unstuck section** (staged hints, checkpoints) but must **not** hand over a complete copy-paste solution — the learner drives the build and the help only unblocks them. This applies to every subject, software or not.

   This zero-to-expert-plus-capstone shape is required for **all** topics: programming languages, libraries, frameworks, and non-software subjects (science, history, geography, math, spoken languages, music, etc.).

2. **Prerequisites:** List what a learner must know before starting this topic. Identify which of those prerequisites are covered by existing leaps topics (to generate wiki-links).

3. **Key Concepts:** List 10–15 core concepts this topic will cover. For each concept, identify if it exists in SHARED/glossary.md or SHARED/concepts.md already.

4. **Cross-topic Connections:** Identify at least 3 topics in the leaps repository (if they exist) that relate to [TOPIC_NAME] and should be cross-linked.

5. **Resource Categories:** Identify what types of resources this topic will need (books, papers, interactive tools, official documentation).

## Step 3: Create the Directory Structure

Create the following structure. Every directory must be created before any files are written into it.

```
TOPICS/[TOPIC_NAME]/
├── README.md
├── PROGRESS.md
├── ROADMAP.md
├── RESOURCES.md
├── GLOSSARY.md
├── QUESTIONS.md
├── PROJECTS.md
├── CHEATSHEET.md
└── modules/
    ├── 01_introduction/
    │   ├── README.md
    │   ├── NOTES.md
    │   ├── QUESTIONS.md
    │   ├── EXERCISES.md
    │   ├── TEST.md
    │   ├── ANSWERS.md
    │   ├── RESOURCES.md
    │   └── PROJECTS.md
    ├── 02_[second_module_name]/    (stub only — empty files)
    ├── 03_[third_module_name]/     (stub only — empty files)
    └── ... (stubs for all planned modules)
```

For modules 02+, create only the directory and empty README.md files as stubs. Full content will be generated by subsequent `generate-module` prompts.

## Step 4: Write TOPICS/[TOPIC_NAME]/README.md

This is the most important file. It must be complete, not a template with unfilled placeholders.

Required sections (follow the template in TEMPLATES/topic/README.md exactly):

**Title and badges:** Include status badge, module count badge, last updated badge.

**Topic overview (2–4 paragraphs):**
- What [TOPIC_NAME] is — a precise, complete definition
- Why it was created and what problem it solves
- Why it matters in 2026 — specific real-world impact
- How this leaps topic is organized

**Historical context:**
- Who created it and when
- What motivated its creation (what problem was being solved)
- Key milestones in its development (minimum 5 timeline entries)
- Current state: who maintains it, where is it used

**Real-world applications:**
- Minimum 5 specific applications with named companies, systems, or domains
- Not vague ("used in web development") but specific ("used by Netflix for [specific thing]")

**Learning objectives (8–12 items):**
- Each objective must be measurable: start with a verb (explain, implement, analyze, design, compare)
- Cover the full range from beginner to advanced

**Difficulty and time estimate:**
- Difficulty: [DIFFICULTY_LEVEL]
- Estimated hours to complete all modules (be realistic)
- Prerequisites with wiki-links to leaps topics where they exist

**Complete module list:**
- Table with module number, title, topic covered, status (all unchecked), score (all blank)
- Every module from your Step 2 plan must appear here

**Progress tracker:**
- Empty point tracker table
- All milestone checkboxes unchecked

**Related topics:**
- Wiki-links to related leaps topics
- Brief description of the relationship (builds on / is used by / is parallel to)

## Step 5: Write TOPICS/[TOPIC_NAME]/PROGRESS.md

Initialize with:
```markdown
# Progress: [TOPIC_NAME]

## Stats
- Total Points: 0 / [CALCULATE_TOTAL]
- Modules Complete: 0 / [MODULE_COUNT]
- Average Test Score: —
- Last Active: [TODAY'S DATE]

## Module Checklist
[One unchecked checkbox per module]

## Milestone Log
[Empty — will be filled as milestones are reached]

## Grading History
[Empty — will be filled by grade-test prompt]
```

## Step 6: Write TOPICS/[TOPIC_NAME]/modules/01_introduction/README.md

This is the full first module. It must be complete and immediately usable for learning.

**Module README required sections:**

1. **Title and metadata:** Module number, title, estimated time, difficulty (Beginner), prerequisites
2. **Overview:** What this module covers and why it is the right starting point (2–3 paragraphs)
3. **Learning objectives:** 5–8 measurable objectives for this specific module
4. **Historical context:** The origin story of the core concepts in this module
5. **Core concepts (one H2 per major concept, minimum 4):**
   - Full explanation of WHAT it is (precise definition)
   - Full explanation of HOW it works (mechanism)
   - Full explanation of WHY it matters (real-world consequence)
   - At least one working code example (if the topic involves code) or worked example (if mathematical)
   - Diagrams using Mermaid where they aid understanding
6. **Common mistakes and gotchas:** Minimum 3, explained with examples of the mistake and the correct approach
7. **Mental models:** 1–3 analogies or mental models that help intuition
8. **Summary:** Bullet-point recap of key concepts
9. **What comes next:** Link to Module 2 with what it builds on from this module

**Code examples must:**
- Use the correct language identifier in code fences
- Be runnable with no modification
- Have inline comments explaining non-obvious lines
- Be explained in prose before AND after they appear

## Step 7: Write TOPICS/[TOPIC_NAME]/modules/01_introduction/EXERCISES.md

Write 8–10 exercises following the format in CONTRIBUTING.md:
- 2 Recall exercises (Beginner)
- 2 Conceptual exercises (Beginner/Intermediate)
- 3 Coding exercises (Beginner to Intermediate)
- 1 Debugging exercise (Intermediate)
- 1 Design exercise (Intermediate)
- 1 Research exercise (any difficulty)

Every exercise must have:
- A descriptive title
- The concept being tested
- Clear instructions
- A solution inside a <details> block
- An explanation of the solution

## Step 8: Write TOPICS/[TOPIC_NAME]/modules/01_introduction/TEST.md

Write a 25-point test with four difficulty tiers:
- Easy (8 pts): 4 questions × 2 pts each — recall and definition
- Medium (9 pts): 3 questions × 3 pts each — conceptual understanding
- Hard (6 pts): 2 questions × 3 pts each — practical application
- Expert (2 pts): 1 question × 2 pts — synthesis or design

Plus 3 bonus questions (up to 6 bonus pts).

Format:
```markdown
# Test: Module 01 — Introduction to [TOPIC_NAME]

**Total points:** 25 + 6 bonus
**Estimated time:** 45–60 minutes
**Instructions:** Answer all questions. Show your work for full credit on multi-step questions.

---

## Section 1: Easy (8 points)
...

## Section 2: Medium (9 points)
...

## Section 3: Hard (6 points)
...

## Section 4: Expert (2 points)
...

## Bonus
...
```

## Step 9: Write TOPICS/[TOPIC_NAME]/modules/01_introduction/ANSWERS.md

Write the complete answer key for every test question. For each answer:
- State the correct answer
- Explain WHY it is correct (not just what)
- For coding questions: provide the complete working solution with explanation
- Include a scoring rubric for partial credit on multi-step questions

## Step 10: Write TOPICS/[TOPIC_NAME]/modules/01_introduction/RESOURCES.md

Curate minimum 8 resources:
- 2 books (include full citation: author, title, edition, publisher, year)
- 2 official documentation or specification links
- 2 video resources (conference talks, tutorials, lectures)
- 1 interactive tool or playground
- 1 paper or academic resource (if applicable)

For each resource:
- Full citation
- One-sentence description of what it covers and why it is on this list
- Difficulty level: Beginner / Intermediate / Advanced

## Step 11: Write Remaining Topic Files

**ROADMAP.md:** A visual learning path using Mermaid showing:
- Phase 1: Foundation (modules 1–3)
- Phase 2: Core Skills (modules 4–7)
- Phase 3: Advanced (modules 8–11)
- Phase 4: Expert (modules 12+)
With estimated hours per phase and milestone checkpoints.

**GLOSSARY.md:** Define the 15 most important terms in [TOPIC_NAME]. For each:
- Precise technical definition
- A plain-English explanation
- Wiki-link to the module where it is first introduced

**QUESTIONS.md:** Seed with 5 open-ended questions about [TOPIC_NAME] that a curious learner would ask (to be answered by the answer-questions prompt or human study).

**PROJECTS.md:** Define 6 project ideas:
- 2 Beginner projects
- 2 Intermediate projects  
- 1 Advanced project
- 1 Capstone/Expert project

Each project needs a title, description, learning objectives, and acceptance criteria.

**CHEATSHEET.md:** Create a quick-reference sheet covering:
- Core syntax or notation (for code topics: most-used patterns; for math: key formulas)
- Common operations with concise examples
- Error/pitfall quick reference

## Step 12: Cross-Linking

After all files are written:
1. Scan the new content for concepts that exist in other leaps topics
2. Add wiki-links at the relevant points in prose
3. Note (as a comment in your response) which existing topic files should be updated to link back to [TOPIC_NAME] — but do NOT modify those files in this pass (that is the job of knowledge-graph-update.md)

## Output Format

Structure your response as follows:

1. **Topic Plan** — the plan from Step 2
2. **Files Created** — list every file path created
3. **Module Sequence** — the complete planned module list
4. **Cross-Link Notes** — existing topics that should be updated to link to this topic
5. **Next Steps** — suggested order for running `generate-module.md` to fill in modules 02+

Then output each file's full content, clearly delimited by the file path as a header.
```

## Examples

**Create a Rust topic:**
```
TOPIC_NAME: rust
TOPIC_DESCRIPTION: Rust is a systems programming language focused on safety, speed, and concurrency. It eliminates entire classes of memory bugs at compile time through its ownership and borrowing system, with no runtime overhead.
DIFFICULTY_LEVEL: Intermediate
```

**Create a calculus topic:**
```
TOPIC_NAME: calculus
TOPIC_DESCRIPTION: Calculus is the mathematical study of continuous change, encompassing differential calculus (rates of change) and integral calculus (accumulation of quantities). It is the foundation of physics, engineering, economics, and machine learning.
DIFFICULTY_LEVEL: Intermediate
```

**Create a networking topic:**
```
TOPIC_NAME: networking
TOPIC_DESCRIPTION: Computer networking is the study of how data moves between systems, covering protocols, architectures, and the physical and logical layers of the internet. Understanding networking is essential for distributed systems, security, and web development.
DIFFICULTY_LEVEL: Beginner
```

## Notes

- The AI will generate a lot of content. Review the first module's README.md and TEST.md carefully for accuracy before committing.
- For highly specialized topics (e.g., a specific research subfield), provide a richer `TOPIC_DESCRIPTION` with pointers to key papers or textbooks — this improves generation quality significantly.
- If the topic has an existing canonical textbook, mention it in `TOPIC_DESCRIPTION`: "The canonical reference is [Book Title] by [Author]."
- Module stubs (02+) will have empty README.md files. Run `generate-module.md` for each subsequent module.
- This prompt intentionally generates a substantial amount of content. Expect 3,000–8,000 words of output depending on the topic complexity.
