---
name: Generate Test
category: Assessment
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name
    example: rust
  - name: MODULE_NUMBER_OR_RANGE
    description: Single module number (e.g., 03) or range (e.g., 01-05) for a cumulative test
    example: 03
  - name: DIFFICULTY
    description: Target difficulty emphasis — Balanced, Easy-Heavy, Hard-Heavy, or Expert
    example: Balanced
---

# Generate Test

## Description

Generates a comprehensive assessment test for one or more modules of a leaps topic. The test includes multiple question types across four difficulty tiers, a complete answer key with explanations and scoring rubric, and bonus questions. Tests are designed to be self-administered and self-assessed, with the answer key stored separately in `ANSWERS.md`.

This prompt is also used for cumulative tests (covering a range of modules), mid-point assessments, and final topic assessments.

## Usage

1. Copy the prompt text below
2. Replace `[TOPIC_NAME]`, `[MODULE_NUMBER_OR_RANGE]`, and `[DIFFICULTY]` with your values
3. Paste into your AI assistant with access to this repository
4. The agent will write the test to `TEST.md` and the answer key to `ANSWERS.md`

For cumulative tests covering multiple modules, use a range like `01-05`. The agent will create files in a special `cumulative/` directory within the topic.

## Prompt

```
You are a leaps assessment agent. Your task is to generate a comprehensive test for a learning topic.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- MODULE_NUMBER_OR_RANGE: [MODULE_NUMBER_OR_RANGE]
- DIFFICULTY: [DIFFICULTY]

## Step 1: Determine Test Scope

Parse MODULE_NUMBER_OR_RANGE:
- If it is a single number (e.g., "03"): this is a module-level test. Target file: `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/TEST.md`
- If it is a range (e.g., "01-05"): this is a cumulative test. Target file: `TOPICS/[TOPIC_NAME]/cumulative-test-[MODULE_NUMBER_OR_RANGE].md`

Parse DIFFICULTY:
- "Balanced": 40% Easy, 35% Medium, 20% Hard, 5% Expert (default)
- "Easy-Heavy": 55% Easy, 30% Medium, 15% Hard, 0% Expert — use for introductory review
- "Hard-Heavy": 20% Easy, 30% Medium, 35% Hard, 15% Expert — use for mastery assessment
- "Expert": 10% Easy, 20% Medium, 30% Hard, 40% Expert — use for final assessments

## Step 2: Read the Content Being Tested

For a module-level test, read:
1. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/README.md` — all concepts, examples, common mistakes
2. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/EXERCISES.md` — do NOT reuse exercise questions verbatim; use them to calibrate difficulty
3. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/NOTES.md` — for quick concept inventory
4. Any existing `TEST.md` — if one exists, read it first. If it is already complete and substantive, inform the user and stop. If it is a stub or empty, proceed.

For a cumulative test, read all of the above for each module in the range. Also read:
5. `TOPICS/[TOPIC_NAME]/README.md` — to understand the overall learning arc
6. `TOPICS/[TOPIC_NAME]/PROGRESS.md` — to understand which modules have been tested before

## Step 3: Build a Concept Inventory

List every testable concept from the module(s). For each concept, classify it:
- **Recall-level:** Can be tested by defining, naming, or identifying
- **Understanding-level:** Requires explaining why, predicting behavior, or comparing
- **Application-level:** Requires using the concept to solve a problem
- **Synthesis-level:** Requires combining multiple concepts or designing a solution

This inventory determines which concepts appear in which tier of the test. Do not test the same concept at the same level more than once. Cover at least 70% of the concepts from the content inventory in the test.

For cumulative tests: weight more recent modules slightly higher (60% of questions from the most recent modules, 40% from earlier modules).

## Step 4: Design the Question Set

### Question Type Definitions

**Multiple Choice (MC)**
- One clearly correct answer
- Three plausible-but-wrong distractors
- Distractors should represent common misconceptions, not obviously wrong answers
- Never use "all of the above" or "none of the above"
- Format: `(A)`, `(B)`, `(C)`, `(D)`

**True/False with Justification (TF)**
- A declarative statement that is either true or false
- Learner must circle T or F AND write a 1–2 sentence justification
- The statement tests understanding, not trivia
- Format: `T / F — [statement]` followed by `Justification: _______________`

**Fill in the Blank (FIB)**
- A sentence or code snippet with one critical term/value/expression removed
- The blank must test a specific concept, not just memorization
- Format: A sentence with `___________` marking the blank

**Short Answer (SA)**
- A direct question requiring 2–5 sentences
- Must test understanding or explanation, not recall of a fact
- Format: Question followed by lines for the answer

**Code Reading (CR)**
- Provide a code snippet and ask: predict output, identify a bug, explain behavior, or trace execution
- Code must be correct unless the question is specifically about a bug
- Format: Code block followed by a question

**Code Writing (CW)**
- Ask the learner to implement something working
- Provide a clear specification with input, output, and constraints
- Include scaffolding (function signatures, type hints) appropriate to the difficulty
- Format: Specification + starter code block + space for answer

**Debugging (DB)**
- Provide deliberately buggy code
- Ask the learner to identify what is wrong and fix it
- The bug should test a concept from the module, not a typo or syntax error
- Format: Buggy code block + "What is wrong?" + "Fixed code:" space

**Essay / Design (ES)**
- Open-ended question requiring analysis, design, or synthesis
- Has a clear scoring rubric
- Format: Question + "Consider the following in your answer:" + bullet-point rubric hints

### Point Values by Type

| Type | Points Each | Notes |
|---|---|---|
| Multiple Choice | 1 | Easy and Medium tiers |
| True/False + justification | 1 | Easy tier |
| Fill in the blank | 1 | Easy tier |
| Short Answer | 2 | Medium tier |
| Code Reading | 2 | Medium tier |
| Code Writing | 3 | Hard tier |
| Debugging | 3 | Hard tier |
| Essay / Design | 5 | Expert tier |
| Bonus (any type) | Variable | Clearly marked |

## Step 5: Write the Test File

Write to `TEST.md` (or cumulative path):

```markdown
# Test: [SCOPE] — [TOPIC_NAME]
<!-- SCOPE = "Module [N]: [Module Name]" or "Modules [N]–[M]: Cumulative Assessment" -->

**Total points:** [BASE_POINTS] base + [BONUS_POINTS] bonus
**Difficulty:** [DIFFICULTY]
**Estimated time:** [N] minutes
**Generated:** [DATE]

---

**Instructions:**
- Answer all questions in the spaces provided (or in a separate document if you prefer)
- For coding questions, write code that compiles and runs correctly for full credit
- Show your reasoning on essay and design questions — partial credit is available
- Do not look at ANSWERS.md until you have completed the test and are ready to grade it

---

## Section 1: Easy ([N] points)
<!-- [DIFFICULTY]: these questions test recall and basic understanding -->

### Q1. [TYPE: MC | TF | FIB] — ([N] pt)
[Question text]

[Answer space]

---

### Q2. [TYPE] — ([N] pt)
[Question text]

[Answer space]

---
[Continue for all Easy questions]

---

## Section 2: Medium ([N] points)
<!-- [DIFFICULTY]: these questions test understanding and pattern recognition -->

### Q[N]. [TYPE: SA | CR] — ([N] pts)
[Question text]

[Code block if applicable]

Answer:
_______________________________________________
_______________________________________________
_______________________________________________

---
[Continue for all Medium questions]

---

## Section 3: Hard ([N] points)
<!-- [DIFFICULTY]: these questions test application and practical skill -->

### Q[N]. [TYPE: CW | DB] — ([N] pts)
[Question text / specification]

[Starter code or buggy code block]

Your answer:
```[language]
// Write your solution here
```

---
[Continue for all Hard questions]

---

## Section 4: Expert ([N] points)
<!-- [DIFFICULTY]: these questions test synthesis, design, and deep understanding -->

### Q[N]. [TYPE: ES] — ([N] pts)
[Essay/design question]

Consider addressing in your answer:
- [Rubric point 1]
- [Rubric point 2]
- [Rubric point 3]

Answer (write as much as needed):
_______________________________________________

---

## Bonus Questions

### Bonus 1 — ([N] pts)
[Bonus question — typically a challenging or tricky application question]

### Bonus 2 — ([N] pts)
[Bonus question]

---

## Scoring Summary
Fill this in after grading:

| Section | Your Points | Possible |
|---|---|---|
| Section 1: Easy | | [N] |
| Section 2: Medium | | [N] |
| Section 3: Hard | | [N] |
| Section 4: Expert | | [N] |
| Bonus | | [N] |
| **Total** | | **[BASE]** |

**Percentage:** _____%
**Grade:** _____
**Pass (≥70%)?** Yes / No
```

**Quality requirements for questions:**
- Every question must test a specific named concept from Step 3's concept inventory
- Note the concept name in a comment inside the question: `<!-- Tests: [concept name] -->`
- Questions must not be answerable by Googling a definition — they require understanding
- Code questions must be original — do not reuse examples from the module README verbatim
- Avoid trick questions that rely on ambiguous wording

## Step 6: Write the Answer Key

Write to `ANSWERS.md`. If `ANSWERS.md` already exists and has a grading record section, append the new answer key as a new section headed by the test date. Do not delete existing content.

```markdown
# Answer Key: [SCOPE] — [TOPIC_NAME]

> [!IMPORTANT]
> Do not open this file until you have completed the test. Grading records are appended to the bottom.

---

## Complete Answer Key

### Section 1: Easy

**Q1.** [CORRECT ANSWER]
- *Why:* [Explanation — 2–4 sentences explaining why this is correct and why the distractors are wrong]
- *Source:* [Reference to the relevant section of the module README]
- *Partial credit:* [If applicable]

[Continue for all questions...]

---

## Scoring Rubric

### Code Writing (Section 3)
Full credit (3/3): Code compiles, produces correct output for all test cases, follows language idioms
Partial credit (2/3): Code is logically correct but has minor syntax errors or misses edge cases
Partial credit (1/3): Demonstrates understanding of the approach but has significant errors
No credit (0/3): Does not demonstrate understanding of the concept being tested

### Essay / Design (Section 4)
Full credit: Addresses all rubric points, uses accurate terminology, shows synthesis
Partial credit: Addresses most rubric points with minor gaps or imprecisions
Minimal credit: Addresses some rubric points but shows limited understanding
No credit: Does not address the question or contains fundamental errors

---

## Grading Records

_Grading records appended by the grade-test agent. Do not edit this section manually._
```

## Step 7: Validate the Test

Before finalizing, perform these checks:

1. **Concept coverage:** Does the test cover at least 70% of the concept inventory from Step 3?
2. **Point math:** Do the section totals add up to the stated total?
3. **Question balance:** Is each question testing a different concept or a different level of the same concept?
4. **Answer key completeness:** Does every question have a complete answer with explanation?
5. **Code correctness:** Are all code examples in the test syntactically correct and runnable?
6. **Rubric completeness:** Does every multi-point question have partial credit guidance?

List any validation failures in your response. Fix them before outputting the final files.

## Output Format

1. **Concept Inventory** — the list from Step 3
2. **Test Design Plan** — question count by type and tier, with concept mapping
3. **Validation Results** — pass/fail for each check in Step 7
4. **TEST.md** — full test file content
5. **ANSWERS.md** — full answer key content
```

## Examples

**Balanced module test:**
```
TOPIC_NAME: rust
MODULE_NUMBER_OR_RANGE: 03
DIFFICULTY: Balanced
```
Output: 25-point test on Ownership and Borrowing with MC, TF, SA, code reading, code writing, and one design question.

**Cumulative easy-heavy review:**
```
TOPIC_NAME: python
MODULE_NUMBER_OR_RANGE: 01-04
DIFFICULTY: Easy-Heavy
```
Output: Cumulative test covering modules 1–4, weighted toward recall and understanding, good for a mid-point review.

**Expert final assessment:**
```
TOPIC_NAME: calculus
MODULE_NUMBER_OR_RANGE: 01-10
DIFFICULTY: Expert
```
Output: Comprehensive final assessment with heavy emphasis on Hard and Expert questions, covering the full topic.

## Notes

- Question quality is more important than quantity. Fifteen excellent questions are better than thirty mediocre ones.
- Do not reuse questions verbatim from EXERCISES.md. The test should feel different — it measures the same concepts but from different angles.
- For cumulative tests, ensure each tested module has at least one question. Do not let early modules be entirely absent.
- If an existing TEST.md is found with real content (not just the template), the agent should not overwrite it. Ask the user whether to add questions to the existing test or create a new version.
- Code in tests should be slightly simpler than code in exercises — the goal is to test understanding under time pressure, not to write complex programs.
