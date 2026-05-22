# Lab: {{LAB_TITLE}}

**Module:** {{MODULE_NUMBER}}: {{MODULE_NAME}}  
**Topic:** {{TOPIC_NAME}}  
**Difficulty:** {{DIFFICULTY}}  
**Estimated Time:** {{HOURS}} hours

---

## Overview

{{LAB_OVERVIEW}}

This lab gives you hands-on experience with {{CORE_SKILL}} in a guided but open-ended format.
Unlike exercises, labs emphasize the _process_ of working with real tools and environments,
not just arriving at the right answer.

**What makes this a lab (vs. an exercise):**
- You'll be working inside a real environment with real tooling
- There are setup and teardown steps
- The goal is a working artifact, not just a correct answer
- Troubleshooting is expected and valuable

---

## Learning Objectives

By completing this lab, you will:

1. {{LAB_OBJECTIVE_1}}
2. {{LAB_OBJECTIVE_2}}
3. {{LAB_OBJECTIVE_3}}
4. {{LAB_OBJECTIVE_4}}

---

## Prerequisites

### Knowledge Required
- [[modules/{{PREREQ_MODULE_1}}]] — specifically: {{PREREQ_KNOWLEDGE_1}}
- [[modules/{{PREREQ_MODULE_2}}]] — specifically: {{PREREQ_KNOWLEDGE_2}}
- Comfort with {{TOOL_OR_CONCEPT}}

### Environment Required
- {{ENVIRONMENT_REQUIREMENT_1}} (e.g., "Python 3.10+ installed")
- {{ENVIRONMENT_REQUIREMENT_2}} (e.g., "Docker available")
- {{ENVIRONMENT_REQUIREMENT_3}} (e.g., "Internet connection")

> [!TIP]
> Use the provided `devcontainer.json` at the topic root to get a pre-configured
> environment that satisfies all requirements.

---

## Environment Setup

Run these commands to prepare your environment before starting the lab exercises.

```bash
# 1. Navigate to the lab directory
cd topics/{{TOPIC_SLUG}}/modules/{{MODULE_SLUG}}/labs/{{LAB_SLUG}}/

# 2. Create and activate a virtual environment (if not using devcontainer)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 3. Install lab dependencies
pip install -r requirements.txt

# 4. Verify setup
{{VERIFICATION_COMMAND}}
```

**Expected output after setup:**
```
{{EXPECTED_SETUP_OUTPUT}}
```

> [!WARNING]
> If the verification command fails, see the [Troubleshooting](#troubleshooting) section
> before continuing. Working through setup issues is itself a valuable learning experience.

---

## Lab Exercises

Work through the exercises in order. Each one builds on the previous.
Check the box when you complete each step.

---

### Exercise 1: {{LAB_EXERCISE_1_TITLE}}

**Goal:** {{LAB_EXERCISE_1_GOAL}}

- [ ] Step 1: {{LAB_EXERCISE_1_STEP_1}}
  ```bash
  {{LAB_EXERCISE_1_STEP_1_COMMAND}}
  ```

- [ ] Step 2: {{LAB_EXERCISE_1_STEP_2}}
  ```bash
  {{LAB_EXERCISE_1_STEP_2_COMMAND}}
  ```

- [ ] Step 3: {{LAB_EXERCISE_1_STEP_3}}

**Checkpoint:** When this exercise is complete, you should see:
```
{{LAB_EXERCISE_1_EXPECTED_RESULT}}
```

**Reflection question:**
{{LAB_EXERCISE_1_REFLECTION_QUESTION}}

> _Your answer:_

---

### Exercise 2: {{LAB_EXERCISE_2_TITLE}}

**Goal:** {{LAB_EXERCISE_2_GOAL}}

- [ ] Step 1: {{LAB_EXERCISE_2_STEP_1}}
  ```bash
  {{LAB_EXERCISE_2_STEP_1_COMMAND}}
  ```

- [ ] Step 2: {{LAB_EXERCISE_2_STEP_2}}
  ```{{LANGUAGE}}
  {{LAB_EXERCISE_2_STEP_2_CODE}}
  ```

- [ ] Step 3: {{LAB_EXERCISE_2_STEP_3}}

- [ ] Step 4: {{LAB_EXERCISE_2_STEP_4}}

**Checkpoint:**
```
{{LAB_EXERCISE_2_EXPECTED_RESULT}}
```

**Reflection question:**
{{LAB_EXERCISE_2_REFLECTION_QUESTION}}

> _Your answer:_

---

### Exercise 3: {{LAB_EXERCISE_3_TITLE}} _(Open-ended)_

**Goal:** {{LAB_EXERCISE_3_GOAL}}

This exercise has less structure. You are given a starting point and a goal;
the path is yours to determine.

**Starting point:**
```
{{LAB_EXERCISE_3_STARTING_POINT}}
```

**Goal:**
{{LAB_EXERCISE_3_GOAL_DESCRIPTION}}

**Constraints:**
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

- [ ] Designed your approach (write it below before coding)
  > _Your design:_

- [ ] Implemented the solution
- [ ] Tested with: {{TEST_INPUTS}}
- [ ] Verified output matches expected behavior

**Reflection questions:**
- What design decisions did you make? Why?
- What did you try that didn't work?
- What would you do differently with more time?

> _Your answers:_

---

## Expected Outcomes

After completing all exercises, you should have:

- [ ] {{OUTCOME_1}}
- [ ] {{OUTCOME_2}}
- [ ] {{OUTCOME_3}}
- [ ] Answered all reflection questions

**Self-assessment:** On a scale of 1–5, how well do you feel you achieved the learning objectives?

| Objective | Score (1–5) | Notes |
|-----------|------------|-------|
| {{LAB_OBJECTIVE_1_SHORT}} | | |
| {{LAB_OBJECTIVE_2_SHORT}} | | |
| {{LAB_OBJECTIVE_3_SHORT}} | | |

---

## Cleanup

Run these commands when you're done to clean up the environment:

```bash
# Remove generated files
{{CLEANUP_COMMAND_1}}

# Deactivate virtual environment
deactivate

# Optional: remove the virtual environment entirely
# rm -rf .venv
```

> [!NOTE]
> If you created any services, databases, or processes during the lab,
> make sure they are stopped before cleanup.

---

## Troubleshooting

### Problem: {{COMMON_PROBLEM_1}}

**Symptom:**
```
{{PROBLEM_1_ERROR_OUTPUT}}
```

**Cause:** {{PROBLEM_1_CAUSE}}

**Solution:**
```bash
{{PROBLEM_1_FIX_COMMAND}}
```

---

### Problem: {{COMMON_PROBLEM_2}}

**Symptom:** {{PROBLEM_2_SYMPTOM}}

**Cause:** {{PROBLEM_2_CAUSE}}

**Solution:** {{PROBLEM_2_SOLUTION}}

---

### Problem: Setup verification fails

**Symptom:** The verification command in Setup returns an error or unexpected output.

**Check:**
1. Are you in the correct directory? Run `pwd` and confirm you're in the lab folder.
2. Is the virtual environment activated? You should see `(.venv)` in your prompt.
3. Did all packages install correctly? Run `pip list` and look for {{KEY_PACKAGE}}.
4. {{SPECIFIC_CHECK_FOR_THIS_LAB}}

---

## Further Exploration

Finished early? These extensions take the lab further:

1. **{{EXTENSION_1_TITLE}}** — {{EXTENSION_1_DESCRIPTION}}
2. **{{EXTENSION_2_TITLE}}** — {{EXTENSION_2_DESCRIPTION}}
3. **{{EXTENSION_3_TITLE}}** — {{EXTENSION_3_DESCRIPTION}}

---

## Connection to Module Content

This lab reinforces:

| Lab Exercise | Module Concept | Module Section |
|-------------|---------------|----------------|
| Exercise 1 | {{CONCEPT_1}} | [Core Concepts](../README.md#core-concepts) |
| Exercise 2 | {{CONCEPT_2}} | [Practical Examples](../README.md#practical-examples) |
| Exercise 3 | {{CONCEPT_3}} | [Mental Models](../README.md#mental-models) |

---

_Lab created: {{YYYY-MM-DD}} · Module: [[modules/{{MODULE_SLUG}}]]_
