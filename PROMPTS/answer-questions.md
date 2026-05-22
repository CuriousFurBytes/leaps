---
name: Answer Questions
category: Learning Continuation
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name
    example: rust
  - name: MODULE_NUMBER_OR_ALL
    description: Specific module number (e.g., 03) or "all" to answer questions across all modules
    example: 03
---

# Answer Questions

## Description

Reads all unanswered questions in a module's (or an entire topic's) `QUESTIONS.md` file and appends thoughtful, detailed answers. Questions are never deleted or overwritten — the agent identifies which questions lack answers and appends answers with timestamps. For each question, the agent also suggests follow-up questions that commonly arise from the answer, deepening the learner's exploration of the concept.

This is one of the most important prompts in leaps: it transforms the `QUESTIONS.md` file from a list of unknowns into a growing dialogue between the learner and the knowledge base.

## Usage

1. Log your questions in `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]/QUESTIONS.md` (or the topic-level `QUESTIONS.md`)
2. Copy the prompt text below
3. Replace `[TOPIC_NAME]` and `[MODULE_NUMBER_OR_ALL]` with your values
4. Paste into your AI assistant with access to this repository

## Prompt

```
You are a leaps question-answering agent. Your task is to read unanswered questions and append detailed, educational answers.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- MODULE_NUMBER_OR_ALL: [MODULE_NUMBER_OR_ALL]

## Step 1: Determine Scope and Read Files

Parse MODULE_NUMBER_OR_ALL:
- If it is a specific module number (e.g., "03"): read only `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/QUESTIONS.md`
- If it is "all": read the following in order:
  - `TOPICS/[TOPIC_NAME]/QUESTIONS.md` (topic-level questions)
  - `QUESTIONS.md` in every module directory under `TOPICS/[TOPIC_NAME]/modules/`

For each QUESTIONS.md file, also read the corresponding README.md to understand the context of the questions. This is essential — answers must be grounded in the content of the module, not just general knowledge.

Additionally read:
- `SHARED/glossary.md` — to provide accurate definitions
- `SHARED/concepts.md` — to ground cross-topic answers
- If a question references another topic, read that topic's relevant module README

## Step 2: Parse Questions and Identify Unanswered Ones

For each QUESTIONS.md file read:

1. **Identify all questions** — look for lines starting with `?`, lines ending with `?`, numbered or bulleted questions, headings that are questions, and any text clearly written as a query.

2. **Determine which are answered** — a question is answered if it is followed by an answer block. Answer blocks are typically:
   - Text immediately below the question not formatted as another question
   - Content within an `> Answer:` blockquote
   - A section starting with `**Answer:**` or `### Answer`
   - A timestamped block: `_Answered [DATE]:_`

3. **List unanswered questions** — these are your targets. If all questions are answered, respond: "All questions in [FILE_PATH] are already answered. Nothing to do." and stop.

## Step 3: Answer Each Question

For each unanswered question, write an answer that meets these standards:

### Answer Quality Requirements

**Accuracy:** Every factual claim in the answer must be accurate. If you are not certain, say so explicitly: "I believe this is the case, but verify against [specific source]." Do not state guesses as facts.

**Depth:** The answer must explain WHY, not just WHAT. A learner who reads the answer should understand the concept better than before — not just have a fact. Explain the mechanism, the reasoning, the consequence.

**Length:** Appropriate to the question. Simple factual questions get 2–4 sentence answers. Conceptual questions get 1–3 paragraphs. Deep or multi-part questions get structured answers with subsections.

**Examples:** Any question about a code concept, algorithm, or mathematical concept should include at least one concrete example. Examples must be runnable and correct.

**Connections:** Connect the answer to:
- Concepts already covered in the module (reference by section name)
- Concepts coming in later modules (preview with a forward reference)
- Related concepts in other leaps topics (use wiki-links)
- Entries in SHARED/glossary.md or SHARED/concepts.md where applicable

**Honesty about uncertainty:** If a question touches on something genuinely complex, debated, or beyond the module's scope, say so. A good answer to a complex question acknowledges the complexity rather than oversimplifying it.

### Answer Format

For each question, append the following structure immediately after the question:

```markdown
> **Answered:** [DATE] | **Source:** [module README section / external source]
>
> [Answer text — full, detailed, explains WHY not just WHAT]
>
> **Example:**
> ```[language]
> [Working code example if applicable]
> ```
>
> **Follow-up questions to explore:**
> - [Natural next question that this answer raises]
> - [Another direction the learner might want to investigate]
>
> **Further reading:** [Specific section of module README, or resource from RESOURCES.md]
```

If the answer is long enough to benefit from structure, use H4 headings within the answer block:

```markdown
> **Answered:** [DATE]
>
> #### Short Answer
> [1–2 sentence direct answer]
>
> #### Full Explanation
> [Detailed explanation]
>
> #### In Practice
> [Code example or worked example]
>
> #### Common Confusion
> [If applicable: what learners often get wrong about this concept]
>
> **Follow-up questions to explore:**
> - [...]
```

## Step 4: Handle Special Question Types

**"Why does X work this way?"** — Provide historical context: when this design decision was made, by whom, what alternatives were considered, and what trade-off was chosen. Reference the module README's Historical Context section.

**"What's the difference between X and Y?"** — Write a structured comparison:
- What they have in common
- Where they diverge (with a concrete example of each)
- When to choose X vs. Y

**"How do I implement X?"** — Provide a working implementation with step-by-step explanation. If this is beyond the current module's scope, provide a pointer to the module where it will be covered.

**"Is it true that X?"** — Evaluate the claim precisely. If true: explain why. If false: explain why and state what is true. If partially true: explain the conditions under which it is and is not true.

**"What happens if X?"** — Predict and explain the behavior. If the answer is "it depends," enumerate the cases.

**Out-of-scope questions** — If a question asks about something not yet covered in the topic:
1. Acknowledge the question is forward-looking
2. Give a brief preview answer if possible
3. Note which module will cover this topic properly

## Step 5: Follow-Up Question Seeding

For every question you answer, generate 2–3 natural follow-up questions that a curious learner would ask after reading the answer. Add these as a bulleted list under "Follow-up questions to explore." These questions are purely suggestions — they are not added to the learner's QUESTIONS.md unless they want them there.

Good follow-up questions:
- Deepen understanding of the same concept
- Connect the concept to something the learner will encounter in the next module
- Challenge an assumption in the original question
- Ask about an edge case or exception

## Step 6: Write the Answers Back to the File

For each QUESTIONS.md file with unanswered questions:

1. Read the current file content
2. For each unanswered question, insert the formatted answer immediately after the question
3. Write the updated content back to the file

**Critical rules:**
- Never delete any existing content — questions or answers
- Never modify or rewrite an existing answer — if a question is already answered, leave it exactly as is
- Preserve all formatting, blank lines, and structure of the original file
- Insert answers in place — immediately after each question — not at the bottom of the file
- If adding an answer would require restructuring the file significantly, add answers at the bottom with clear headers indicating which question they answer

## Step 7: Update PROGRESS.md

Add a note to `TOPICS/[TOPIC_NAME]/PROGRESS.md` under a "Recent Activity" section (create this section if it does not exist):

```markdown
## Recent Activity

- [DATE]: [N] questions answered in Module [N] QUESTIONS.md
```

Do not update point totals — answering questions does not directly affect points.

## Step 8: Generate Summary

Produce a response summary:

```
---
QUESTIONS ANSWERED: [N] questions in [FILE_PATH(S)]
Date: [DATE]

Questions answered:
1. "[First few words of question]..." → [1-sentence summary of answer]
2. "[First few words of question]..." → [1-sentence summary of answer]
[...]

Follow-up questions seeded: [N]

To continue exploration:
- The most important concept that came up: [Concept] — covered in [Module README section]
- Suggested next step: [read section X / try exercise Y / ask follow-up question Z]
---
```

## Important Rules

1. **Never delete questions.** Even if a question is confused, poorly worded, or based on a misconception — keep it. Misconceptions are valuable records of where the learner was at that point.
2. **Never modify the learner's question wording.** Answer the question as asked, not as you wish it had been asked.
3. **If a question is based on a misconception**, answer the misconception directly and then redirect: "Your question assumes X, which is not quite right — here is what is actually happening: [explanation]"
4. **Never leave a question without an answer after running this prompt.** If you cannot answer a question confidently, provide the best answer you can and mark it: "> [!WARNING]\n> This answer is uncertain. Verify against [specific source]."
5. **Append, never overwrite.** The file must be longer after running this prompt than before.
```

## Examples

**Answer questions in a specific module:**
```
TOPIC_NAME: rust
MODULE_NUMBER_OR_ALL: 03
```
Output: Reads module 03 QUESTIONS.md, identifies unanswered questions, appends detailed answers with examples and follow-ups.

**Answer all questions across a topic:**
```
TOPIC_NAME: python
MODULE_NUMBER_OR_ALL: all
```
Output: Reads every QUESTIONS.md in the Python topic (topic-level and all modules), answers all unanswered questions.

**Answer topic-level questions:**
```
TOPIC_NAME: calculus
MODULE_NUMBER_OR_ALL: all
```
Output: Starts with TOPICS/calculus/QUESTIONS.md, then all module QUESTIONS.md files.

## Notes

- For questions that span multiple modules (e.g., "How does concept X from module 2 relate to concept Y from module 5?"), read both modules' README files before answering.
- For questions about performance, benchmarks, or empirical claims ("Is X faster than Y?"), state the conditions under which the claim is true and cite a source if possible. Never state performance claims without context.
- If the same conceptual question appears in multiple modules' QUESTIONS.md files, answer it in full each time (do not write "see Module N for the answer"). Repetition across modules is normal in learning and each context warrants a fresh answer.
- This prompt is one of the most valuable in the library. A well-answered QUESTIONS.md file is a personalized tutoring record that captures exactly what was confusing at the time and exactly what it took to understand it. Treat it accordingly.
