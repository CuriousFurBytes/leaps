---
name: Continue Topic
category: Learning Continuation
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name to resume (must exist in TOPICS/)
    example: rust
---

# Continue Topic

## Description

Resumes learning in an existing topic from exactly where you left off. The agent reads your current progress, identifies the last completed module, and determines the optimal next action — whether that is completing the current module's exercises, taking a test, or beginning the next module.

This prompt is designed to be run at the start of any study session. It acts as your "pick up where I left off" command, giving you orientation and a focused agenda for the session rather than requiring you to remember your own state.

## Usage

1. Copy the prompt text below
2. Replace `[TOPIC_NAME]` with the topic you want to resume
3. Paste into your AI assistant with access to this repository
4. Follow the session agenda the agent generates

## Prompt

```
You are a leaps learning continuation agent. Your task is to resume learning in an existing topic and prepare a focused study session.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]

## Step 1: Read the Current State

Read the following files completely and in order:

1. `TOPICS/[TOPIC_NAME]/README.md` — understand the topic, module list, and prerequisites
2. `TOPICS/[TOPIC_NAME]/PROGRESS.md` — identify completed modules, current points, milestone status, and grading history
3. List the contents of `TOPICS/[TOPIC_NAME]/modules/` — see all existing module directories

For each module directory that exists:
- Read its `README.md` to understand its content
- Check whether `TEST.md` contains any filled-in answers (indicating the learner has attempted the test)
- Check whether `ANSWERS.md` contains any grading records (indicating the test was graded)
- Check `QUESTIONS.md` for any unanswered questions

## Step 2: Determine Current Position

Based on what you have read, identify:

**A. Last Completed Module:**
A module is "complete" if:
- Its checkbox in `TOPICS/[TOPIC_NAME]/PROGRESS.md` is checked, OR
- Its `ANSWERS.md` contains a grading record with `pass: true`

If no modules are complete, the current position is "start of Module 01."

**B. Current Module (in-progress):**
The first module that has been started but not completed. A module is "started" if:
- `NOTES.md` has content beyond the template boilerplate, OR
- `EXERCISES.md` has attempted answers, OR
- `TEST.md` has filled-in answers without a grading record in `ANSWERS.md`, OR
- `QUESTIONS.md` has questions that appear to be learner-authored

**C. Blockers:**
Identify anything preventing progress:
- Unanswered questions in `QUESTIONS.md` that might be blocking understanding
- A test that has been attempted but not graded (answers in `TEST.md`, no grading record in `ANSWERS.md`)
- A module with no content yet created (stub directory with empty files)
- An exercise set that appears incomplete

**D. Next Module:**
The lowest-numbered module that has no started status and no content.

## Step 3: Assess Knowledge Gaps

Read the grading history in `ANSWERS.md` files for all completed modules. Identify:
- Topics where test scores were below 80%
- Specific question types where the learner consistently struggled
- Any modules flagged in the grading feedback for reinforcement

## Step 4: Generate Session Agenda

Based on your analysis, produce a structured session agenda. The agenda should be actionable and completable in 45–90 minutes.

Format the agenda as:

---
## Session Agenda: [TOPIC_NAME] — [TODAY'S DATE]

### Your Current Position
- **Last completed module:** [Module N: Title] — [Score if known]
- **Currently in progress:** [Module N: Title or "None"]
- **Next module to begin:** [Module N: Title]
- **Total progress:** [X/Y modules complete] ([Z%])
- **Total points:** [X/Y pts]

### What Needs Attention First
[Ordered list of blockers, if any. Examples:
- "Module 03 test is answered but ungraded — run grade-test.md first"
- "Module 02 QUESTIONS.md has 3 unanswered questions — run answer-questions.md"
- "Module 04 directory is a stub — needs content generation via generate-module.md"]

### Today's Study Agenda

**Priority 1: [Action]**
[What to do and why this is the highest priority]

**Priority 2: [Action]**
[What to do next]

**Priority 3: [Action]**
[Optional — do this if time allows]

### Knowledge Gaps to Watch
[List any concepts from past grading records where score was below 80%. These are the areas to pay extra attention to in the current module.]

### What's Coming Up
[Brief preview of the next 2 modules after the current one — what concepts they introduce, how they build on what you are studying now]

---

## Step 5: Generate Content If Needed

If the current module's `README.md` is a stub (empty or just the template without real content), generate the full module content using the same requirements as the `generate-module.md` prompt. Do this before presenting the agenda.

If the current module exists but the learner appears to have questions (per `QUESTIONS.md`), quote those questions in the agenda and offer to answer them immediately.

## Step 6: Offer Next Actions

End your response with a menu of concrete next actions the learner can take:

```
What would you like to do now?

1. Answer my open questions in Module [N]
   → Run: answer-questions.md with TOPIC_NAME=[TOPIC_NAME] MODULE_NUMBER_OR_ALL=[N]

2. Grade my test in Module [N]
   → Run: grade-test.md with TOPIC_NAME=[TOPIC_NAME] MODULE_NUMBER=[N]

3. Generate the next module content (Module [N])
   → Run: generate-module.md with TOPIC_NAME=[TOPIC_NAME] MODULE_NUMBER=[N] MODULE_NAME=[Title]

4. Start a reinforcement session on weak areas
   → Run: reinforcement-session.md with TOPIC_NAME=[TOPIC_NAME] WEAK_AREAS_OR_AUTO=auto

5. Continue studying the current module
   → I'll summarize where Module [N] left off and what's next in the content
```

Fill in the actual module numbers and titles based on your analysis.

## Important Rules

- Do NOT modify any existing files unless explicitly asked. Your role here is to read, assess, and advise.
- Do NOT delete any content from any file.
- If PROGRESS.md is missing or empty, initialize it using the template in TEMPLATES/ but use the data you found by reading the module files.
- If the topic does not exist at all, respond: "Topic '[TOPIC_NAME]' does not exist in TOPICS/. Did you mean to run create-topic.md instead?"
```

## Examples

**Resume after a break:**
```
TOPIC_NAME: rust
```
Output: reads all module state, finds you completed modules 1–3, module 4 is in progress with unanswered questions, proposes agenda.

**Resume at start of a new topic:**
```
TOPIC_NAME: calculus
```
Output: finds module 01 with no progress, offers to generate the first module or walks through what to study first.

**Resume with a pending graded test:**
```
TOPIC_NAME: python
```
Output: finds a completed TEST.md with no grading record, prioritizes running grade-test.md, then gives the study agenda.

## Notes

- This prompt is designed as a daily driver — run it every time you open a study session to get oriented without having to remember where you were.
- The session agenda is advisory. You are not required to follow it exactly.
- If PROGRESS.md is severely out of sync with the actual module files (can happen if you studied without an agent), the agent will reconcile the state by reading the individual module files directly and offer to update PROGRESS.md.
- For topics with more than 10 modules, the agent reads only the completed and in-progress modules in detail; stubs are only scanned.
