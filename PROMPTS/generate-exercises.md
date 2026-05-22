---
name: Generate Exercises
category: Content Creation
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name
    example: go
  - name: MODULE_NUMBER
    description: The zero-padded module number
    example: 06
  - name: EXERCISE_COUNT
    description: Number of new exercises to add (3–15)
    example: 8
  - name: DIFFICULTY
    description: Target difficulty distribution — Balanced, Beginner-Heavy, Advanced-Heavy, or a specific level (Beginner|Intermediate|Advanced|Expert)
    example: Balanced
---

# Generate Exercises

## Description

Expands a module's `EXERCISES.md` with new, high-quality practice problems. The agent reads the existing exercises to avoid duplication, reads the module content to understand the concept space, and generates new exercises at the appropriate difficulty distribution. Each exercise includes a complete solution and explanation inside a collapsible `<details>` block.

Use this prompt when a module's existing exercise set is too thin, when you want more practice on specific concepts, or when you want additional exercises at a higher difficulty level before attempting the test.

## Usage

1. Copy the prompt text below
2. Replace all four parameters with your values
3. Paste into your AI assistant with access to this repository
4. The agent will append new exercises to the existing EXERCISES.md

## Prompt

```
You are a leaps exercise generation agent. Your task is to create new high-quality exercises for a learning module.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- MODULE_NUMBER: [MODULE_NUMBER]
- EXERCISE_COUNT: [EXERCISE_COUNT]
- DIFFICULTY: [DIFFICULTY]

## Step 1: Read the Context

Read the following files completely:

1. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/README.md` — understand every concept covered
2. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/EXERCISES.md` — read ALL existing exercises carefully
3. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/NOTES.md` — for concept inventory
4. All previous module README.md files — know what was already taught; exercises may reference prior modules

Note: every existing exercise has a number. Your new exercises must be numbered starting from (highest existing number + 1).

## Step 2: Concept Inventory and Gap Analysis

List every testable concept from the module README. For each concept:
- Is there already an exercise that tests it? If so, at what difficulty?
- Is there room for a harder or different-type exercise on the same concept?

Identify gaps: concepts with no exercises, concepts with only easy exercises, and concepts that benefit from multiple approaches.

This gap analysis determines which concepts your new exercises target. Do not create exercises that test the same concept at the same difficulty and type as an existing exercise unless EXERCISE_COUNT demands it.

## Step 3: Determine Difficulty Distribution

Parse DIFFICULTY:
- "Balanced": roughly equal across Beginner, Intermediate, Advanced (weighted toward Intermediate)
- "Beginner-Heavy": 50% Beginner, 35% Intermediate, 15% Advanced
- "Advanced-Heavy": 10% Beginner, 30% Intermediate, 40% Advanced, 20% Expert
- A specific level (e.g., "Advanced"): all new exercises at that level

For [EXERCISE_COUNT] exercises, the exact distribution:
- Calculate how many exercises per difficulty level
- Round to whole numbers; assign remainders to Intermediate

## Step 4: Determine Exercise Type Distribution

Aim for variety. For [EXERCISE_COUNT] exercises, include at minimum:

| Type | Count (if EXERCISE_COUNT ≥ 8) | Count (if < 8) |
|---|---|---|
| Recall | 1 | 1 |
| Conceptual | 2 | 1 |
| Coding | [EXERCISE_COUNT - 5] | [EXERCISE_COUNT - 3] |
| Debugging | 1 | 1 |
| Design | 1 | 0 |
| Research | 1 | 0 |

Adjust proportionally for smaller counts. Never have more than 40% of exercises be pure coding.

## Step 5: Write Each Exercise

For every new exercise, follow this exact format:

```markdown
### Exercise [N]: [Descriptive Title]

**Difficulty:** [Beginner | Intermediate | Advanced | Expert]
**Type:** [Recall | Conceptual | Coding | Debugging | Design | Research]
**Concept:** [Specific concept from module this exercise tests]
**Estimated time:** [N–M minutes]

**Instructions:**

[Clear, complete description of what the learner must do. Leave nothing to interpretation.
For coding exercises: specify the function name, parameter types, return type, and constraints.
For conceptual exercises: specify the expected form of the answer (e.g., "in 2–3 sentences").
For debugging exercises: state the expected correct behavior.]

[If the exercise requires starter code:]
```[language]
[Starter code — syntactically complete but functionally incomplete]
```

**Expected output / acceptance criteria:**

[What a correct answer produces. For code: exact output or behavior.
For conceptual: the key points that must be addressed.
For design: the properties a good design must have.]

**Hints:**

<details>
<summary>Hint 1 (try without first)</summary>

[First hint — minimal. Nudges in the right direction without revealing the answer.
A good hint names the relevant concept or suggests the right approach,
without showing any code or giving the answer away.]

</details>

<details>
<summary>Hint 2 (more specific)</summary>

[Second hint — more specific. Appropriate for someone who read Hint 1 and is still stuck.
May show a relevant pattern or API without giving the full solution.]

</details>

**Solution:**

<details>
<summary>Show solution</summary>

```[language]
[Complete, working solution with inline comments explaining every non-obvious line]
```

**Explanation:**

[WHY the solution works — not just WHAT it does. Must explain:
1. The core mechanism behind the solution
2. Why this approach is idiomatic for this topic
3. What would happen if you tried the most common alternative approach
4. Any edge cases the solution handles and how]

**Common mistakes:**

- [Mistake learners make on this exercise] → [Why it fails / what it produces instead]
- [Another common mistake] → [Why it fails]

</details>
```

### Exercise Type Requirements

**Recall exercises:**
- Ask the learner to define a term, name something, list items, or identify a concept
- Answer should be checkable without running code
- Solution should include full explanation, not just the answer

**Conceptual exercises:**
- Ask the learner to explain why, predict behavior, or compare/contrast
- Specify the expected form: "In 2–3 sentences, explain...", "Compare X and Y by describing..."
- Solution must address the WHY, not just the WHAT
- Include at least one concrete example in the solution

**Coding exercises:**
- Provide a clear function specification including name, parameters, return type, constraints
- Include at least one test case with expected output
- Solution must be complete, runnable, and idiomatic
- Include comments explaining the solution's approach
- Show the simplest correct solution first; then mention more advanced alternatives if relevant

**Debugging exercises:**
- Provide buggy code that compiles (if applicable) but produces wrong output or behavior
- The bug must test a concept from the module — not a typo or unrelated mistake
- State what the code is supposed to do
- State what it actually does (the symptom)
- Solution must fix the bug AND explain the root cause
- Good bugs to use: off-by-one errors, wrong condition, missing edge case, type mismatch, scope issue, mutability issue, wrong algorithm

**Design exercises:**
- Give a problem description, constraints, and requirements
- Ask the learner to sketch a solution: data structures, function signatures, approach
- Evaluative criteria should be explicitly listed
- Solution provides a complete design with rationale, not just code

**Research exercises:**
- Point the learner toward investigating something not explicitly in the module
- Specify what to find and where to look (documentation, the web, other modules)
- Must have a concrete deliverable: "write a 3-sentence summary of what you find"
- Solution provides the answer and the source

## Step 6: Append to EXERCISES.md

Append the new exercises to the END of the existing EXERCISES.md. Do NOT modify existing exercises.

Add a divider before the new exercises:

```markdown

---

## Added Exercises
<!-- Added [DATE] via generate-exercises.md -->

```

Then the numbered exercises in sequence.

## Step 7: Update the Exercise Summary

At the top of EXERCISES.md (after the title and introduction), update or add a table summarizing all exercises — existing and new:

```markdown
## Exercise Summary

| # | Title | Type | Difficulty | Concept |
|---|---|---|---|---|
| 1 | [existing exercise titles] | ... | ... | ... |
| ... | | | | |
| [N] | [new exercise title] | ... | ... | ... |
```

If the table already exists, update it. If it does not exist, add it. This helps learners quickly find exercises at their target difficulty.

## Step 8: Validate

For each new coding exercise, verify:
- The starter code is syntactically correct
- The solution is complete and produces the stated expected output
- The solution is idiomatic for the topic (uses the language/domain conventions properly)
- The solution would not be considered buggy or non-idiomatic in a code review

Mark any unverified examples: `# [VERIFY: check this before submitting]`

## Output Format

1. **Gap Analysis** — from Step 2: which concepts need more exercises and why
2. **Distribution Plan** — exact count by difficulty and type
3. **New exercises** — all new exercises in the correct format, ready to paste into EXERCISES.md
4. **Summary table update** — the updated exercise summary table

The agent should present the exercises formatted as they will appear in the file so they can be copy-pasted or applied directly.
```

## Examples

**Add balanced exercises to Go module 6:**
```
TOPIC_NAME: go
MODULE_NUMBER: 06
EXERCISE_COUNT: 8
DIFFICULTY: Balanced
```
Output: 8 new exercises covering Go module 6's concepts (likely interfaces), mix of types, numbered starting from the next available number.

**Add hard exercises to Rust module 3:**
```
TOPIC_NAME: rust
MODULE_NUMBER: 03
EXERCISE_COUNT: 5
DIFFICULTY: Advanced-Heavy
```
Output: 5 exercises weighted toward Advanced/Expert, testing deep understanding of ownership.

**Add beginner reinforcement to Python:**
```
TOPIC_NAME: python
MODULE_NUMBER: 02
EXERCISE_COUNT: 6
DIFFICULTY: Beginner
```
Output: 6 Beginner exercises on Python module 2's content, good for reviewing before taking the test.

## Notes

- The quality of exercises depends heavily on the quality of the module README. If the README is thin, the exercises will reflect that — run `generate-module.md` first if needed.
- Debugging exercises are often the most educational but also the hardest to write well. A good debugging exercise has a bug that makes sense to make (a real mistake a learner would make), not an arbitrary error.
- Coding exercises should not be solvable by copying code from the module README verbatim. The goal is transfer — applying the concept in a new context.
- If EXERCISE_COUNT is high (10+), it may be better to run this prompt twice with different DIFFICULTY values to ensure variety.
- All exercises appended to EXERCISES.md are numbered consecutively from the existing maximum. If exercises were removed (which should never happen), the numbering may have gaps — note this in the output and use the next sequential number regardless.
